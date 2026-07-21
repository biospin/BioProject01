#!/usr/bin/env bash
# make_repro_bundle.sh — ClawBio식 재현성 번들 생성.
# "에이전트 없이도 헤드라인 수치를 결정론적으로 재현": 헤드라인 산출물의 SHA-256 +
# 재생성 명령 + env lock 을 results/REPRODUCE.md 한 장으로 묶는다.
# BIOP01 결정론적 재계산 게이트(CLAUDE.md DoD)를 사람이 읽는 형태로 고정.
set -u
cd "$(dirname "$0")/.." || exit 2   # → pipeline/hspc-velocity-benchmark
OUT=results/REPRODUCE.md
sha(){ [ -f "$1" ] && sha256sum "$1" | awk '{print $1}' || echo "MISSING"; }

# 헤드라인 산출물(논문 핵심 수치의 출처)
HEAD_MD=(results/FINDINGS.md results/concordance.md results/scrambled_null.md
         results/prereg_gse205117_scorecard.md results/sim_positive_control_multimethod.md
         results/external_rate_validation_schwalb.md results/profile_likelihood_identifiability.md)
HEAD_CSV=(results/profile_likelihood_freed.csv
          results/multivelo_genes.csv results/rna_only_dynamical_genes.csv results/multivelovae_genes.csv
          results/moflow_genes_gse205117.csv results/multivelo_genes_gse205117.csv)
# 결정론 재계산 게이트 명령(env → command)
declare -A GATE=(
 ["scv-preprocess"]="python p3_concordance.py ; python p3_crossdataset_concordance.py ; python p3_scrambled_null.py ; python cross_dataset/p3_prereg_gse205117.py"
)

{
  echo "# REPRODUCE — HSPC velocity 벤치마크 헤드라인 수치 재현 번들"
  echo
  echo "> 자동 생성: \`scripts/make_repro_bundle.sh\`. **에이전트 없이도** 아래 env·명령으로 헤드라인 산출물을 재생성하고 SHA-256로 대조한다."
  echo "> 규율: 재생성값이 아래 checksum과 다르면 드리프트 — 사람이 원인 확인(자동 PASS 신뢰 금지). 수치-원고 정합은 \`scripts/check_manuscript_numbers.py\`."
  echo
  echo "## 1. 환경(conda env lock — 결정론 고정)"
  for l in env/scv-preprocess.lock.yml env/velo-mv.lock.yml env/velo-torch.lock.yml env/velo-tf.lock.yml; do
    [ -f "$l" ] && echo "- \`$l\` — sha256 \`$(sha "$l")\`"
  done
  echo
  echo "## 2. 재생성 명령(결정론적 재계산 게이트)"
  echo '```bash'
  echo "cd pipeline/hspc-velocity-benchmark"
  for env in "${!GATE[@]}"; do
    echo "# env: $env"
    echo "conda run --no-capture-output -n $env bash -lc '${GATE[$env]}'"
  done
  echo "# 재현성 대조:"
  echo "bash scripts/make_repro_bundle.sh   # 이 표를 다시 생성해 checksum 비교"
  echo '```'
  echo
  echo "## 3. 헤드라인 산출물 checksum (SHA-256)"
  echo "| 산출물 | SHA-256 | 비고 |"
  echo "|---|---|---|"
  for f in "${HEAD_MD[@]}" "${HEAD_CSV[@]}"; do
    h=$(sha "$f"); note=""; [ "$h" = "MISSING" ] && note="⚠️ 없음"
    echo "| \`${f#results/}\` | \`${h:0:16}…\` | $note |"
  done
  echo
  echo "_생성 시각은 git 커밋으로 대신(결정론 위해 스크립트에 timestamp 미기록). 산출물이 갱신되면 이 스크립트를 다시 돌려 REPRODUCE.md를 재생성·커밋._"
} > "$OUT"
echo "생성: $OUT ($(wc -l <"$OUT")줄)"
grep -c MISSING "$OUT" | xargs echo "MISSING 산출물 수:"
