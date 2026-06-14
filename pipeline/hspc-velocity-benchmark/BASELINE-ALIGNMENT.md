# Harness_Baseline 정합 — 팀 baseline 분석 하네스 파악 + 우리 HSPC pipeline 매핑

> 2026-06-14 · branch `kkkim-pipeline`
> 대상: **박상준(@poqopo) `Harness_Baseline`** (개인 repo, 팀 baseline 분석 하네스 초안)
> 결정(2026-06-14, user): **규약만 정합 — 실행 코드는 BioProject01 유지.** 코드 최종 위치는 박상준님과 추후 협의.

## 1. Harness_Baseline이 무엇인가
- 팀 프로젝트(epigenomic lag → drug response timing)의 **"데이터 분석" 레이어 baseline 하네스**. Codex 포맷(`AGENTS.md` + `skills/<dataset>/<task>/SKILL.md` + `agents/openai.yaml`).
- **markdown SKILL = 지침(plan)만, 실행 코드·LICENSE 없음** (초안, 3 commits). 즉 *무엇을 할지*를 규정; *어떻게 실행할지*는 우리가 채움.
- 팀 깃헙(`biospin/BioProject01`)엔 지금 **paper-agent 레이어만** 올라가 있음. 이 baseline 분석 레이어는 박상준님 개인 repo에 있음 → CLAUDE.md가 말한 "연구 프로젝트 컨텍스트(계획)" 레이어에 해당.

## 2. 구조
- `AGENTS.md`: project frame(activation/shutdown lag 정의, baseline epigenomic features, required metadata, reference frame=MultiVelo/MultiVeloVAE/MoFlow).
- `skills/ROUTES.md`: **dataset 먼저 → task 다음** 라우팅.
- **dataset 4종**: `10x-embryonic-mouse-brain`, `share-seq-mouse-skin`, `human-brain-multiome`, **`human-hspc-10x-multiome`(우리 것, GSE209878)**.
- **task 4단계**: `download → preprocessing → model → visualization`.

## 3. HSPC SKILL 핵심 (우리가 따라야 할 규약)
- **download**: 공식 출처·accession·access date 기록, raw/processed/metadata 분리, **donor/sample/batch + lineage/HSPC subpopulation metadata 보존**, **checksum + download_manifest**. 경로 규약 `data/human-hspc-10x-multiome/{raw,processed}/`, `metadata/human-hspc-10x-multiome/`.
- **preprocessing**: RNA/ATAC pairing+QC, HSPC subpopulation·lineage annotation, promoter/enhancer accessibility + peak-to-gene feature, **lineage commitment pseudotime root/direction 명시**. 산출 `work/` 또는 `results/human-hspc-10x-multiome/`.
- **model**: gene별 chromatin open/close + transcription onset/shutdown timing 추정 → activation/shutdown lag → **lineage별 lag 분포 비교** → baseline feature로 lag 예측 → **held-out lineage/subpopulation generalization 평가**.
- **공통 주의(= 우리 methodologist 검토와 일치)**: branch별 timing을 **global pseudotime으로 강제 합치지 말 것**, **rare lineage uncertainty 별도 표시**, time-axis(pseudotime/real/switch/DTW) **항상 명시**.

## 4. 우리 BioProject01 작업 ↔ Harness_Baseline 매핑
| Harness_Baseline (지침) | 우리 (실행, `pipeline/hspc-velocity-benchmark/`) | 상태 |
|---|---|---|
| HSPC `download` | `scripts/download_data.sh` (GSE209878, ~1.8GB 확보·검증) | ✅ |
| HSPC `preprocessing` | `scripts/p1_build.py` (통일 전처리, DESIGN §3) | 🚧 P1 실행 중 |
| HSPC `model` (lag 추정 method 선택) | `DESIGN.md` 벤치마크 = model 1단계 **method-selection** | 📐 설계+검토 완료 |
| HSPC `model` (feature→lag 예측, held-out) | 미착수 (P2 이후) | ⬜ |
| HSPC `visualization` | 미착수 | ⬜ |

> 우리 벤치마크는 baseline의 `model` 단계 중 **"어떤 velocity method로 lag를 추정할지"** 를 엄밀히 정하는 부분. 그 결과가 feature→lag 예측/평가로 이어진다.

## 5. 채택할 규약 체크리스트 (정합)
- [x] **download_manifest** 생성 — `download_manifest.tsv` (sample/file/size/sha256/source, 12파일). genome build/access date는 헤더 주석.
- [ ] **required metadata** 기록: genome build(hg38?), gene annotation source, **lineage label + pseudotime root/direction**, time-axis 명시 → P1 산출(`p1_build.py`/`dataset-info.yaml`)에 반영.
- [ ] **경로 매핑** 명시: 우리 `pipeline/hspc-velocity-benchmark/data/GSE209878/` ↔ baseline `data/human-hspc-10x-multiome/`. (재배치 대신 매핑 표로 정합; 코드 위치는 BioProject01 유지.)
- [x] **within-lineage + rare-pop + time-axis 규율** — DESIGN.md/REVIEW에 이미 반영(일치).

## 6. 결정·후속
- **규약 정합, 코드 BioProject01 유지** (user 2026-06-14). 코드 최종 위치(기여 vs 유지)는 박상준님과 협의.
- 후속: 박상준님께 "Harness_Baseline 규약에 맞춰 BioProject01에서 HSPC 구현 중 — model 단계는 method 벤치마크부터" 공유 + 경로/manifest 규약 합의.
- 참고: Harness_Baseline은 LICENSE 없음 → 내용 복사·기여 시 박상준님 동의 필요.
