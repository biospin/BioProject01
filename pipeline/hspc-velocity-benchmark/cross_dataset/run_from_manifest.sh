#!/usr/bin/env bash
# run_from_manifest.sh — BIOP01-45 워커 계층 실행 래퍼 (트리거=codex, 형식=YAML 확정 2026-08-04)
#
# codex가 openai.yaml → 이 래퍼를 트리거한다. 래퍼는 runner_manifest.yaml을 읽어
# 각 stage를 올바른 env로 conda run 하고, 산출물이 있으면 skip, 완료 후 required_cols를 검증한다.
# "누가 트리거하나"(codex)와 "무엇을 어떻게 실행하나"(이 래퍼+manifest)를 분리 — 트리거가 바뀌어도 이 래퍼는 불변.
#
# 설계: ORCHESTRATION-WIRING-DESIGN.md §3·§5-2 (얇은 래퍼 — 기존 watchdog/flock 자산과 병행).
# 사용:
#   run_from_manifest.sh --dataset gse205117 [--dry-run] [--conda /path/to/conda]
#   --dry-run : 실행하지 않고 stage별 SKIP/RUN 결정과 명령만 출력 (CPU·GPU 불요, 어디서나 검증 가능)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # cross_dataset/
ROOT="$(cd "$HERE/.." && pwd)"                            # pipeline/hspc-velocity-benchmark
SCRIPTS="$ROOT/scripts"
RESULTS="$ROOT/results"
MANIFEST="$HERE/runner_manifest.yaml"

DATASET=""
DRYRUN=0
CONDA="${CONDA:-/home/kkkim/miniconda3/bin/conda}"       # 서버별 상이 → --conda로 override
while [ $# -gt 0 ]; do
  case "$1" in
    --dataset) DATASET="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    --conda)   CONDA="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$DATASET" ] || { echo "--dataset 필요 (예: gse205117)" >&2; exit 2; }

SUFFIX="_${DATASET}"
CONFIG="../cross_dataset/config_${DATASET}.py"           # scripts/ 기준 상대경로 (기존 규약)

log(){ echo "[$(date '+%F %T')] $*"; }

# manifest에서 stage 메타를 파이프 구분 라인으로 방출 (id|env|gpu|runner|output|required_cols).
# score stage도 kind=score로 함께 (P3 채점까지 한 래퍼에서).
emit_stages() {
python3 - "$MANIFEST" <<'PY'
import sys, yaml
m = yaml.safe_load(open(sys.argv[1]))
def row(kind, s):
    out = s.get("output","") or ""
    req = ",".join(s.get("required_cols",[]) or [])
    print("|".join([kind, s["id"], s["env"], str(s.get("gpu",False)).lower(),
                     s["runner"], out, req]))
for s in m["stages"]: row("fit", s)
for s in m["score"]:  row("score", s)
PY
}

verify_cols() {   # $1=csv 경로, $2=쉼표구분 required_cols → 없으면 exit 1
  local csv="$1" req="$2"
  [ -n "$req" ] || return 0
  python3 - "$csv" "$req" <<'PY'
import sys, csv
path, req = sys.argv[1], sys.argv[2].split(",")
with open(path, newline="") as f: hdr = next(csv.reader(f), [])
missing = [c for c in req if c not in hdr]
sys.exit(1 if missing else 0)
PY
}

log "manifest=$MANIFEST dataset=$DATASET suffix=$SUFFIX dry_run=$DRYRUN"
[ "$DRYRUN" = 1 ] || { [ -x "$CONDA" ] || { echo "conda 실행 불가: $CONDA (--conda로 지정)" >&2; exit 3; }; }

FAIL=0
while IFS='|' read -r kind id env gpu runner output req; do
  # 산출물 경로(있으면). {suffix} 치환.
  outfile=""
  if [ -n "$output" ]; then outfile="$RESULTS/${output/\{suffix\}/$SUFFIX}"; fi

  # skip 판정: 산출물이 있고 ≥2행이면 SKIP
  if [ -n "$outfile" ] && [ -f "$outfile" ] && [ "$(wc -l <"$outfile")" -ge 2 ]; then
    log "[$id] SKIP (산출물 존재: $(basename "$outfile"), $(wc -l <"$outfile")행)"
    # 계약 검증은 skip이어도 수행 (BIOP01-41: 존재해도 컬럼 계약 위반이면 잡는다)
    if [ -n "$req" ]; then
      if verify_cols "$outfile" "$req"; then log "     required_cols OK: $req"
      else log "     ❌ required_cols 위반: $req"; FAIL=1; fi
    fi
    continue
  fi

  # 실행 명령 구성
  cuda=""; [ "$gpu" = "true" ] && cuda="CUDA_VISIBLE_DEVICES=1 "
  cmd="cd $SCRIPTS && ${cuda}CROSS_DATASET_CONFIG=$CONFIG CROSS_DATASET_SUFFIX=$SUFFIX $CONDA run --no-capture-output -n $env python -u $runner"

  if [ "$DRYRUN" = 1 ]; then
    log "[$id] RUN (dry) env=$env gpu=$gpu → ${output:-<산출물 없음>}"
    echo "      $cmd"
    continue
  fi

  log "[$id] RUN env=$env gpu=$gpu"
  ( eval "$cmd" ) || { log "❌ [$id] 실행 실패"; FAIL=1; break; }
  # 산출물·계약 사후 검증
  if [ -n "$outfile" ]; then
    { [ -f "$outfile" ] && [ "$(wc -l <"$outfile")" -ge 2 ]; } || { log "❌ [$id] 산출물 미생성: $outfile"; FAIL=1; break; }
    if [ -n "$req" ] && ! verify_cols "$outfile" "$req"; then log "❌ [$id] required_cols 위반: $req"; FAIL=1; break; fi
    log "     ✅ $(basename "$outfile") 생성·계약 충족"
  fi
done < <(emit_stages)

if [ "$FAIL" = 0 ]; then log "DONE — 전 stage 해소(SKIP/RUN) + 계약 충족"; exit 0
else log "FAILED — 위 로그 참조"; exit 1; fi
