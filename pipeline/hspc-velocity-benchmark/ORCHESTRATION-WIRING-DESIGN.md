# BIOP01-45 설계 초안 — OpenClaw 계획→실행 배선 (P2–P5 runner 자동 실행)

> **상태: 설계 초안 (협의 대상).** 작성 지용기, 2026-07-22. 협의: braveji ↔ kkkim.
> 이 문서는 코드가 아니라 **호출 규약의 제안**이다. 합의 전 실행 배선을 만들지 않는다.
> 근거: BIOP01-45 본문 4개 할 일 + BIOP01-22 오케스트레이션 검토(계획 계층은 정합, 계획→실행 연결만 없음).

> ✅ **선결 ① 해소 (2026-07-27, BIOP01-71 A(복원) 확정·머지).**
> 이 초안 §3 route가 위임하는 `skills/ROUTES.md` 라우터가 `275def2`(7/20 PR #4 머지)에서 41파일 사고 유실됐던 건,
> kkkim A(복원) 확정 → **PR #5 머지(`cb886ee`)로 복원 완료**. 실측: `skills/ROUTES.md`(69줄) 등 41파일 복귀,
> `harness_doctor` **RESULT PASS(phantom-path 0)**. → 라우터 blocker 제거, 초안 §3의 dataset→task 2단 라우팅이 실체 위에 섬.
>
> ✅ **선결 ② 해소 (2026-08-04, 리더 결정) — 트리거 = codex, 형식 = YAML.**
> `openclaw` CLI가 팀 6대 중 실사용 불가(5대 바이너리 부재 + 6대 auth 부재, kkkim/이건규 실측)인 반면 **codex는 설치·인증 완료**.
> → **트리거는 codex**(같은 `agents/openai.yaml`을 codex로 실행, `skills/OPENCLAW-RUN.md` 3번 경로), **manifest 형식은 YAML**로 확정.
> 남은 서버측 선결 1건: "codex가 이 `openai.yaml`을 실제로 완주하는지" 1회 실증(codex 샌드박스 `bwrap` 이슈 포함) — kkkim 서버.
>
> **결정에 따라 실체화된 것 (2026-08-04):**
> - `cross_dataset/runner_manifest.yaml` — 워커 계층 계약(YAML). gse205117 실산출물로 멱등·계약 인라인 검증 PASS.
> - `cross_dataset/verify_manifest_resolution.py` — 정식 검증기(멱등·누락감지·계약 3검사). 실행 PASS(exit 0).
> - `cross_dataset/run_from_manifest.sh` — codex가 트리거하는 실행 래퍼. manifest를 읽어 stage별 `conda run`,
>   skip-if-output + required_cols 사후검증(BIOP01-41 게이트). `--dry-run`으로 gse205117 전 stage SKIP 확인.
>
> ✅ **§2 `runner_manifest.yaml`(워커 계층)은 트리거/형식 결정과 애초에 무관했다** — manifest는 "어느 runner를 어떤 env로"만
> 정의하고, "누가 트리거하나"(codex)는 상위 계층이다. (근거: 코멘트 11397·11439의 계층 분리 논지.)
> **남은 것**: codex→래퍼 실증(서버) + numpy env byte-identical scorecard 재생성(kkkim) → DoD "end-to-end 1회" 마감.

---

## 0. 한 줄 요약

하네스는 지금 "Model Plan" 문서까지만 만들고 **실제 `scripts/p2_*.py` 실행은 사람이 손으로** 한다.
필요한 인터페이스(env-var 계약·per-method env 매핑·산출물 규약·runtime 수집)는 **이미 전부 존재**한다.
BIOP01-45는 그 사이의 **호출 규약을 명문화(manifest)** 하고, OpenClaw route가 그 manifest를 읽어 runner를
자동 실행하도록 잇는 작업이다. **새 실행 로직을 발명하는 게 아니라, 흩어진 관례를 계약으로 고정**한다.

---

## 1. 지금 이미 있는 것 (실측 — 재발명 금지)

| 조각 | 실체 | 위치 |
|---|---|---|
| **env-var 계약** | `CROSS_DATASET_CONFIG`(dataset config 경로) + `CROSS_DATASET_SUFFIX`(산출물 접미사). 기본값 "" → HSPC byte-identical | `scripts/p2_config.py` L13 |
| **per-method env 매핑** | floor=`scv-preprocess` · MultiVelo=`velo-mv` · VAE/MoFlow/dl_prep=`velo-torch` · CRAK=`velo-tf` | 드라이버 실측 + `env/README.md` |
| **실행 규약** | `cd scripts && CROSS_DATASET_CONFIG=… CROSS_DATASET_SUFFIX=… [CUDA_VISIBLE_DEVICES=1] conda run -n <env> python -u p2_<method>.py` | `cross_dataset/run_gse205117_fits.sh` L38–64 |
| **산출물 규약** | `results/<method>_genes<SUFFIX>.csv` (첫 컬럼 `gene`), `results/runtime.csv` 누적 | `p2_config.py` L38,40 |
| **skip/게이트 관례** | 산출 CSV가 ≥2행이면 skip, 없으면 실행·검증·실패 시 die | fit 드라이버 공통 패턴 |
| **계획 계층** | AGENTS.md → ROUTES.md → SKILL.md → "Model Plan" markdown | 하네스(OpenClaw 포맷) |

→ **빠진 것은 단 하나**: "Model Plan"이 위 실행 규약을 **자동으로 호출**하는 연결. 그게 BIOP01-45.

---

## 2. 제안하는 계약 — `runner_manifest.yaml` (신규, 유일한 신규 파일)

runner의 실행 규약을 **한 곳에 선언**한다. 드라이버 스크립트마다 흩어진 지식을 한 파일로 모은다.
OpenClaw route도, 사람도, 미래의 다른 드라이버도 이 manifest 한 장만 읽으면 된다.

```yaml
# pipeline/hspc-velocity-benchmark/runner_manifest.yaml (제안)
version: 1
defaults:
  cwd: scripts                         # 모든 runner는 scripts/에서 실행
  suffix_env: CROSS_DATASET_SUFFIX
  config_env: CROSS_DATASET_CONFIG
  outputs_dir: results
  runtime_log: results/runtime.csv
stages:                                # P2 fit 산출 (순서 = 의존성)
  - id: floor
    runner: p2_rna_only.py
    env: scv-preprocess
    gpu: false
    output: rna_only_dynamical_genes{suffix}.csv
    required_cols: [gene, fit_alpha, fit_likelihood]
  - id: multivelo
    runner: p2_multivelo.py
    env: velo-mv
    gpu: false
    output: multivelo_genes{suffix}.csv
    required_cols: [gene, fit_alpha, fit_t_sw1, fit_t_sw2, fit_likelihood]
  - id: dl_prep
    runner: p2_dl_prep.py
    env: velo-torch
    gpu: true
    produces_input_for: [multivelovae, moflow]
  - id: multivelovae
    runner: p2_multivelovae.py
    env: velo-torch
    gpu: true
    output: multivelovae_genes{suffix}.csv
    required_cols: [gene, vae_alpha, vae_alpha_c]
  - id: moflow                         # 사전등록 예측5(원정의)에 필수 — BIOP01-41 교훈
    runner: p2_moflow.py
    env: velo-torch
    gpu: true
    output: moflow_genes{suffix}.csv
    required_cols: [gene, cs_lag_median]
score:                                 # P3 채점 (fit 위에서)
  - id: prereg
    runner: cross_dataset/p3_prereg_gse205117.py    # dataset별 채점기
    env: scv-preprocess
    gpu: false
    output: prereg{suffix}_scorecard.md
```

**설계 원칙**
- manifest는 **선언(what)** 만. 실행 순서·재시도·watchdog 같은 **방법(how)** 은 드라이버가 갖는다(관심사 분리).
- `required_cols`를 넣는 이유: BIOP01-41에서 **채점기가 잘못된 컬럼명(`cs_lag` vs `cs_lag_median`)으로 조용히 폴백**한 사고가 있었다. manifest가 컬럼 계약을 명시하면 runner 완료 직후 **계약 검증**이 가능해 같은 사고를 원천 차단한다.
- `moflow`를 stage에 **명시적으로** 넣는다: 같은 티켓(BIOP01-41)에서 fit 드라이버가 MoFlow를 빠뜨려 GPU를 두 번 돌릴 뻔했다. manifest에 있으면 누락이 구조적으로 드러난다.

---

## 3. OpenClaw route 배선 (BIOP01-45 할 일 2·4)

```
요청: "HSPC model 실행" (또는 "dataset=gse205117 model")
  │
  ├─ ROUTES.md: dataset=human-hspc, task=model → 이 route
  │
  ├─ [1] manifest 로드 → stages 순서 결정
  ├─ [2] 각 stage: output CSV 존재+≥2행+required_cols 충족? → skip
  │        아니면: cwd=scripts, env=stage.env, [gpu→CUDA_VISIBLE_DEVICES],
  │               CROSS_DATASET_CONFIG=config_<ds>.py CROSS_DATASET_SUFFIX=_<ds>
  │               conda run -n <env> python -u <runner>
  ├─ [3] 완료 후 required_cols 검증 → 실패 시 hard stop (조용한 통과 금지)
  ├─ [4] runtime.csv append 확인
  └─ [5] score stage 실행 → scorecard 경로 회신
```

**env 자동선택(할 일 4)**: manifest의 `stage.env`를 그대로 `conda run -n`에 넣으면 끝. 4-env(scv-preprocess/velo-mv/velo-torch/velo-tf) 매핑이 manifest에 선언돼 있으므로 route는 분기 로직이 필요 없다.

---

## 4. DoD 대응 (BIOP01-45 본문)

| DoD 항목 | 이 설계의 대응 |
|---|---|
| Model Plan ↔ runner 호출 규약 정의 | §2 manifest — 입력(config/suffix)·env·인자·출력·컬럼계약 |
| OpenClaw route로 P2–P5 트리거 | §3 route 의사코드 (skip·검증·회신) |
| 실행 결과 자동 수집·보고 | `runtime.csv` append + scorecard 경로 회신 (§2 score) |
| task별 올바른 env 자동선택 | manifest `stage.env` → `conda run -n` 직결 (§3) |
| end-to-end 1회 성공 | 검증 시나리오 §6 |

---

## 5. 열린 결정 — 처리 상태 (리더 결정 2026-08-04)

1. **manifest 형식** → ✅ **YAML 확정.** `cross_dataset/runner_manifest.yaml`. (PyYAML은 repo에 이미 있음 확인 6.0.1.)
2. **route 실행 주체** → ✅ **래퍼 확정.** `cross_dataset/run_from_manifest.sh`가 manifest를 읽어 실행; 트리거(codex)는 이 래퍼만 부른다. 기존 watchdog·flock 자산과 병행.
3. **GPU 스케줄링** → 래퍼는 manifest `gpu:true` stage에 `CUDA_VISIBLE_DEVICES=1` 고정(기존 규약). 여유 GPU 탐지는 후속 개선(비필수).
4. **dataset별 채점기 일반화** → **별건으로 분리 유지.** 지금은 `p3_prereg_<ds>.py`를 score stage에 직접 지정. parametric 통합은 후속 리팩터.
5. **적용 범위** → **P2(fit) + P3(prereg 채점)까지.** manifest `stages`(P2) + `score`(P3). P4/P5(bootstrap·FDR)는 후속.

> **트리거 = codex 확정(2026-08-04):** openclaw 팀 전체 실사용 불가, codex 설치·인증됨. codex가 `agents/openai.yaml`을 실행 → `run_from_manifest.sh` 호출.
> 서버측 선결 1건: codex가 openai.yaml을 실제 완주하는지 실증(bwrap 샌드박스 결정 포함) — kkkim.

---

## 6. 검증 시나리오 (DoD "end-to-end 1회 성공")

이미 완주한 **gse205117**로 회귀 검증하면 GPU 재실행 없이 배선만 검증 가능:
1. 산출물이 이미 다 있으므로 route 실행 시 **전 stage skip** 되어야 한다(멱등성 확인).
2. `moflow_genes_gse205117.csv`를 임시로 숨기면 → moflow stage가 **재실행 대상으로 감지**되는지(누락 감지 확인). ※ 실제 재실행은 GPU라 dry-run 플래그로 "실행할 명령"만 출력.
3. score stage가 manifest 경로로 채점기를 호출해 scorecard를 **byte-identical 재생성**하는지(결정론 확인 — 이미 kkkim이 확인한 성질).

→ 이 3개는 **CPU만으로 가능**하므로 제가(지용기) 배선 후 직접 돌려 검증할 수 있다. GPU 필요한 실제 fit 재실행은 kkkim 서버 몫.

---

## 7. 왜 이 순서인가 (설계 판단)

- **manifest 먼저, route 나중**: 계약이 확정돼야 route가 안정된다. manifest는 CPU로 검증 가능(§6)하니 저비용.
- **기존 관례를 계약으로 승격, 재작성 아님**: run_gse205117_fits.sh가 이미 하는 일을 manifest가 선언으로 옮길 뿐. 동작 변경 0 → 회귀 위험 최소.
- **BIOP01-41 교훈 반영**: `required_cols` 계약 + moflow 명시 stage로, "조용한 폴백"·"arm 누락" 두 사고를 구조로 막는다. 이게 이 설계가 단순 편의배선이 아니라 **재현성 강화**인 이유다.

---

## 부록 A — 미확인/리스크
- OpenClaw route가 `conda run`을 직접 부를 권한·환경이 되는지 **미확인**(braveji 확인 필요).
- `/opt/envs` 공유 마운트 여부 미확정(다른 계정 실행 시 env 접근) — BIOP01-22와 연동.
- P4/P5(permutation FDR·bootstrap)는 fit이 아니라 재분석이라 manifest 스키마가 그대로 맞는지 재검토 필요.
