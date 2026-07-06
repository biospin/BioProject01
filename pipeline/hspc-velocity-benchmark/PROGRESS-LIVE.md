# PROGRESS-LIVE — 진행 중 작업 추적 보드

> **목적**: 이 세션에서 백그라운드로 도는 작업이 중단/다른 창 전환돼도 상태를 잃지 않도록, 단계마다 실시간 갱신. 새 세션은 이 파일 + `HANDOFF.md`만 읽으면 이어받을 수 있다.
> 최종 갱신: **2026-07-05** (논문 근거 보강 — 3트랙 병렬 실행 중)

## 🔵 진행 중 (2026-07-05) — 논문 근거 보강 3트랙 병렬 (publication hardening)
> 서사/블로그용 정리 = `manuscript/publication_hardening_log.md`. 전략 근거 = `manuscript/novelty_strategy.md`. 이 표는 **이어받기용 상태판**.

| 트랙 | 작업 | 종류 | 산출(완료 시) | 상태 |
|---|---|---|---|---|
| **A** | correctness gate: agreement-set 0/598을 clean 3-method(MultiVelo×MoFlow×MultiVeloVAE)로 재계산 + CRAK sensitivity 강등 | 재분석(CPU, ~시간) | `results/clean_concordance_gate.md`, FINDINGS §1 갱신 | ✅ 완료 (헤드라인 pivot) |
| **A** | #1 MoFlow-subset held-out 확증 (consistent subset이 MVVAE held-out+ATAC-shuffle에서 생존?) | 재분석(CPU) | `results/moflow_subset_confrontation.md` | ✅ 완료 (§3 예측 falsify) |
| **B** | 데이터셋 다운로드: E18 mouse brain 5k(cheap-first) + GSE194122 human BMMC(복구경로 진단) | 다운로드 | `cross_dataset/P0_provenance_crossdataset.md` | ✅ 완료 |

**트랙 B 결과:** ① **E18 mouse brain** (`data/e18_mouse_brain/`, 790MB) — spliced/unspliced **제공·검증**(loom 4881 cell, spliced 5.3%/unspliced 5.4% nnz), MultiVelo P1 입력 전부 staging → **즉시 GO**(전처리 거의 0). CellRanger-ARC 1.0.0(문서 2.0.0 정정). mouse symbol → within-dataset H1은 매핑 불필요, cross-dataset lag-rank는 ortholog 매핑 필요. ② **GSE194122 human BMMC** (`data/GSE194122/`, processed 2.79GB) — spliced/unspliced **없음**(layers=['counts']만). 복구=원본 10x GEX possorted BAM(SRR17693266, 28.66GB, public S3, dbGaP 불필요)에 velocyto → **DEFER**(donor당 ~29GB/수시간, 전용 run으로; same-tissue human 조혈이라 복구 시 최고 재현가치). Bonus: MultiVeloVAE figshare에 `3423-MV-2`(=GSE209878 day7) post-processed 객체 → 나중에 reference-lag cross-check 가능.
| **C** | #2 second-method 인과대조: ATAC-shuffle을 MoFlow에 적용→GPU 재fit→lag 비교 (한계 #4 해소) | **GPU 재fit(cuda:1, ~1h)** | `results/scrambled_null_moflow.md`, `moflow_scrambled_genes.csv` | ✅ **완료** — MoFlow lag도 셔플 생존(모델구조적 확증) |
| **D** | 두 번째 cross-dataset 재현: E18 mouse brain P1→P2→concordance (HSPC 패턴 lag-fragile/α-robust 재현되나?) | 재분석+선택적 GPU | `results/concordance_e18_mouse_brain.md` (+`*_e18_mouse_brain.csv`) | ✅ **완료 (2026-07-06)** — 재현 YES: within-E18 α 0.81 ≫ lag 0.06, cross-dataset α 0.32 > lag 0.10. FINDINGS §7 병합 완료 |
| **H** | humanize 윤문: 네 트랙 요약을 쉬운 말로 | 재분석 | `manuscript/four_track_summary.md` | ✅ 완료(등급 A, 변경 0.6%, 내용 보존) |
| **E(최종)** | **블로그 md 작성 + 구글드라이브 업로드** — 트랙 D 완료 후 four_track_summary + E18 결과 합쳐 산문 블로그로 | 집필+업로드 | `blog/` md + GDrive 프로젝트/blog 하위 | ✅ **완료 (2026-07-06)** — 개별글 #12 Drive 업로드, 로컬 통합본(13편) 재생성. ⚠️Drive 통합본 same-title 2개(1wtZxlc 부분본·1tK2chP 구본) 수동 휴지통 정리 필요 |

## 🔵 진행 중 (2026-07-06) — 다음 단계 2갈래 병렬 (BMMC 복구 + 약물 arm)
> 블로그 결론의 "다음 걸음"(검증 폭 확대 + 원래 목표 약물 예측) 착수. 둘 다 background agent로 발행.

| 트랙 | 작업 | 성격 | 산출(완료 시) | 상태 |
|---|---|---|---|---|
| **F** | GSE194122 human BMMC 복구 — velocyto on possorted BAM(SRR17693266, donor09, 28.66GB S3 sra-pub-src-2) → build→P1→P2→P3, `_GSE194122_bmmc` suffix | 무거운 compute(밤샘 detached) | `results/concordance_GSE194122_bmmc.md` (+gene csv) | 🔄 **재기동 (2026-07-06 21:17~, PID 959013)** — 1차 시도(06:34)는 stage[1] ref추출서 실패(tar 경로에 버전 접미사 `-2.0.0`·`.gz` 누락). **버그 수정 완료** → genes.gtf(1.42GB, GENCODE v32) 추출 검증 후 재기동. 현재 **stage[3] velocyto run**(BAM/ref skip). PPID=1 로그아웃 생존 실측. **⛔ 수동 재실행 금지** — 아래 이어받기 블록 참조 |
| **G** | 약물 타이밍 arm — **데이터 블로커**(gate 충족 단일셋 無, 페어링만). 후보 게이트 검증 + nested-model 설계 확정 | 데이터 검증·설계(compute 아님) | `manuscript/drug_timing_arm_scout.md` | ✅ **완료 (2026-07-06)** — 판정: **공개데이터 4종 전부 headline 부적격**(전사체 시간축이 1점으로 붕괴). 공개데이터는 보조역할만(GSE229314 decay 통제+scoop ref, GSE201662 coarse 타당성demo). **headline timing 주장은 wet-lab 필요.** nested-model(timing~decay vs +chromatin_lag, ΔR²) 설계 locked |

**🤖 트랙 F 무인 드라이버 실행 중 (2026-07-06 21:17 재기동, PID 959013) — ⛔ 수동 재실행 금지(중복됨):**
- **1차 실패·수정 이력:** 06:34 1차 기동(PID 916306)은 stage[1] ref추출서 죽음 — `run_bmmc_recovery.sh`의 tar 경로가 `refdata-cellranger-arc-GRCh38-2020-A/genes/genes.gtf`였으나 실제 아카이브는 `...-2.0.0/genes/genes.gtf.gz`(버전 접미사 + gzip). 두 곳 수정(REF_GTF 경로 + tar 추출·gunzip). genes.gtf(1.42GB) 추출 검증 후 21:17 재기동. BAM 28.66GB는 유지·skip.
- **게이트 PASS** — `cross_dataset/BMMC_PREFLIGHT_GATE.md`(바코드 브리지 92.2%, 형식 `-1` 일치). 복구 GO 확정.
- **드라이버:** `cross_dataset/run_bmmc_recovery.sh` (setsid, **PPID=1 로그아웃 생존 실측**, PID 959013). 로그 `cross_dataset/bmmc_driver.log`.
- **생존 확인:** `pgrep -af run_bmmc_recovery`. **상태 한눈에:** `cat cross_dataset/BMMC_PROGRESS`(stage별 heartbeat). 완료=`cross_dataset/BMMC_DONE`, 실패=`cross_dataset/BMMC_FAILED`.
- **stage:** [0]BAM 다운로드(28.66GB, ~40min) → [1]ref GTF → [2]rmsk(opt) → [3]velocyto(밤샘) → [4]build → [5]floor → [6]MultiVelo → [7]VAE(CUDA:1) → [8]P3. **전 stage idempotent**(산출물 있으면 skip).
- **완료 시:** `results/concordance_GSE194122_bmmc.md` + gene csv 3종(전부 `_GSE194122_bmmc` suffix, 기존 덮어쓰기 없음). **커밋은 복귀 후 사람이**(무인 git 금지).
- **드라이버 죽었고 BMMC_DONE도 없을 때만** 재기동: `cd cross_dataset && setsid bash run_bmmc_recovery.sh </dev/null >bmmc_driver.log 2>&1 &` (idempotent — 있는 산출물부터 이어감).
- 트랙 G: `manuscript/drug_timing_arm_scout.md` 존재 확인. compute 아니므로 재dispatch 가벼움.
- 커밋은 사람이(무인 git 금지).

**최종 단계(E) 이어받기 (세션 중단 시):**
1. 트랙 D 완료 판정: `results/concordance_e18_mouse_brain.md` 존재 확인. 없고 프로세스 없으면 → 트랙 D 재dispatch(체크리스트 5번).
2. D 완료 시: `manuscript/four_track_summary.md`(humanize 완성본) + `results/concordance_e18_mouse_brain.md`(E18 재현 결과) + `manuscript/publication_hardening_log.md`를 근거로 **블로그 산문 md** 작성 → `blog/` 하위 저장.
3. 구글드라이브 업로드: **`/blog` 스킬** 사용(프로젝트 폴더 blog 하위로 업로드) 또는 GDrive MCP(`mcp__claude_ai_Google_Drive__create_file`).
4. 스타일: 사용자 선호 = 쉬운 윤문체(memory `feedback_briefing_plain_style`). 업로드 후 링크 사용자에 보고.

**트랙 C 재시작 정보 (detached):** fit = python PID **881349**(wrapper 881326), `CUDA_VISIBLE_DEVICES=1`, 로그 `data/velocity/moflow_scrambled.log`. fit 완료 시 모니터가 `p3_scrambled_null_moflow.py` 자동 실행 → `data/velocity/moflow_scrambled_stats.txt` → `results/scrambled_null_moflow.md`. sanity: per-gene marginal corr=1.0000(marginal 보존, cell-level 결합만 파괴). real `moflow_genes.csv`/`moflow.h5ad` 미접촉. **재시작 시**: `pgrep -af moflow_scrambled` 로 fit 생존 확인 → 죽었고 `moflow_scrambled.h5ad` 없으면 fit 재실행, 있으면 `p3_scrambled_null_moflow.py`만.

**이어받기 체크리스트 (세션 중단 후):**
1. `results/clean_concordance_gate.md` 있나? 없고 프로세스 없으면 → 트랙 A 재dispatch(브리프 = HANDOFF 2026-07-05 + novelty_strategy §4.0/§4.1).
2. `results/moflow_subset_confrontation.md` 있나? 없으면 → 트랙 A 위와 함께.
3. `cross_dataset/candidate_datasets.md`에 "## Acquisition log 2026-07-05" 있나? 없으면 → 트랙 B 재dispatch. E18은 MultiVelo GitHub에 spliced/unspliced 기존 제공(최저비용) — 여기부터.
4. `results/scrambled_null_moflow.md` 있나? **트랙 C fit은 완료**(`moflow_scrambled.h5ad` 존재) — md만 없으면 분석 단계만 재실행: `python scripts/p3_scrambled_null_moflow.py`(GPU 불필요, 재분석). h5ad도 없고 `pgrep -af moflow_scrambled` 없으면 fit부터 재실행. `moflow_genes.csv`(real-run) 덮어쓰지 말 것.
5. **[트랙 D]** `results/concordance_e18_mouse_brain.md` 있나? 없고 프로세스 없으면 → E18 재현 재dispatch. 선례=`cross_dataset/build_human_brain.py`+`config_human_brain.py`+`p3_crossdataset_concordance.py` 미러, 데이터=`data/e18_mouse_brain/`, 출력은 전부 `_e18_mouse_brain` suffix(HSPC/human_brain 덮어쓰기 금지). mouse brain은 `cell_annotations.tsv` 사용(hematopoiesis marker 강제 금지).
6. 트랙 전부 완료 시 → FINDINGS.md에 트랙 C(2nd 인과대조)·D(2nd 재현) 결과 병합 + HANDOFF/SESSION-LOG 갱신 + (사람) git 커밋.
- git 커밋은 **사람이** 한다(무인 금지). agent들은 커밋 금지 지시받음.

## ✅ 완료 (2026-07-01) — per-lineage MultiVelo refit (진짜 within-lineage H1)

## ✅ 완료 (2026-07-01) — per-lineage MultiVelo refit (진짜 within-lineage H1)
| 작업 | 로그 | 상태 | 결과 |
|---|---|---|---|
| **per-lineage refit** (5 lineage: root∪L 따로 fit) | `scratchpad/perlineage_refit.log` | ✅ 5/5 fit 완료(02:04~04:51) | `results/lineage_refit/*.csv` |
| **자율 finisher** (PID 357446) | `scratchpad/finish_perlineage.log` | ✅ p3 자동 실행 완료 | `results/lineage_refit.md` |

- **결과**: cross-lineage lag magnitude ρ median=**0.349**(범위 0.234~0.513, 양수 10/10) → lag 일치도 **약함/경계**. 대조군 α_c ρ median=**0.483**(lag보다 robust) → 기존 H1 패턴 재현. per-lineage vs 전역 fit ρ 0.23~0.46(전역 fit이 lineage 신호 뭉갬 → refit 정당). **cross-lineage 축에서도 H1(lag 비robust) 확증.**

## 🔵 진행 중 (2026-07-01) — α_c 전체 re-fit bootstrap stability
| 작업 | PID | 로그 | 상태 | ETA |
|---|---|---|---|---|
| **bootstrap 전체 re-fit** (B=12, frac 0.70 비복원 subsample, 530 canonical gene) | py **377590** | `scratchpad/bootstrap_refit.log` | 🔄 refit 0/12 fit 중 | ~6.5h (refit당 ~30min) |
| **자율 finisher** (PID 377569) | — | `scratchpad/finish_bootstrap_refit.log` | 🔄 12개 채워지면 p3 자동 실행 | — |

- **목적**: `p5_bootstrap_stability.py`(fit 고정→stability 하한)가 명시적으로 남긴 미완 — **전체 re-fit 반복** — 수행. cell subsample마다 MultiVelo를 처음부터 재fit해 **α_c·α·lag의 진짜 재fit 안정성**(rank 일치도·CV·부호flip) 측정.
- **가설(H1 정합)**: α 계열(α/α_c) rank 일치도 ≫ lag → 'α는 재fit-robust, lag은 비robust'를 재fit 축에서 직접 확증.
- **스크립트**: `p2_multivelo_bootstrap_refit.py`(mv env, resumable·incremental CSV) + `p3_bootstrap_refit.py`(scv-preprocess). 스모크(B2×12gene) 통과.
- ⚠️ MultiVelo는 **CPU** fit(n_jobs=16, 32코어 idle) — TODO의 "GPU 반복 fit"은 부정확. subsample 비복원(복원추출은 kNN graph 붕괴).
- **산출(완료 시)**: `results/bootstrap_refit/refit_<b>.csv`(12) → `results/bootstrap_refit.md` + `bootstrap_refit_pergene.csv`.

## ✅ 완료 (2026-07-01) — 진짜 day0 ATAC baseline feature 어셈블 + 모델
| 작업 | 스크립트 | 산출 |
|---|---|---|
| **day0 ATAC feature 어셈블** | `p5_atac_baseline_features.py` | `atac_baseline_features.{csv,md}` |
| **ATAC feature → timing 모델** | `p5_lag_model_atac.py` | `lag_model_atac.{csv,md}` |

- crakvelo 197,482 peak에서 **day0 HSC/MPP 8,583 세포** 기준 gene별 promoter(±2kb)/enhancer(±100kb distal) 접근성 → 511 gene. p5_lag_model.py 한계 ①(moflow Mc smoothed proxy) **해소**.
- **핵심 발견**: held-out lineage CV에서 **robust α는 진짜 ATAC로 예측됨(ρ=+0.309, 6 lineage 전부 양수)**, Mc proxy(−0.089)는 실패. **비robust lag은 ATAC로도 비예측(ρ=+0.05)**. → 같은 feature가 robust target만 예측 = H1 예측가능성 축 재확인 + day0 ATAC 어셈블 가치 입증. drug-timing 모델 입력 경로 = **day0 ATAC → α**(lag 아님). FINDINGS §6 신설.
- 남은 블로커: **drug perturbation arm**(timing ground truth 데이터 부재) + α_c 전체-refit bootstrap(GPU).

- **목적**: 전역 fit lag을 dominant-expression으로 lineage 귀속한 `lineage_lag.md`를 **진짜 per-lineage fit**으로 대체. lag이 gene-intrinsic robust 속성인지(cross-lineage 일치도) = within-method H1 축 추가.
- **스크립트**: `scripts/p2_multivelo_perlineage.py`(fit, mv env) + `scripts/p3_lineage_refit.py`(분석, scv-preprocess env). 스모크(Lymphoid 12 gene) 통과 후 full launch.
- **설계**: 각 terminal lineage L = HSC/MPP(root)∪L 세포로 부분집합 → P1 동일 substrate(filter_and_normalize→HVG→moments) → knn_smooth_chrom → recover_dynamics_chrom. root 포함 이유=분화 trajectory 필요.
- **산출**: `results/lineage_refit/<lin>_genes.csv`(5종) → `results/lineage_refit.md`(A.분포 B.cross-lineage lag ρ C.vs전역 D.α_c 대조군).
- ⚠️ MultiVelo lag sign 구조적(sw2>sw1 항상 양수) → magnitude rank Spearman만 평가.

## 🔴 GPU 작업 (cuda:1 전용)
| 작업 | PID | 로그 | 상태 | ETA |
|---|---|---|---|---|
| ~~cisTopic full~~ | 249700 | `scratchpad/cistopic_full.log` | ✅ **16:21 DONE** | — |
| **CRAK-Velo fit** (UniTVelo+chromatin, 10000 epoch) | (main.py) | `scratchpad/crakvelo_fit.log` | 🔄 ~59% (5900/10000) | ~18:1x |

- **cisTopic 완료**: postpro `crakvelo_atac_postpro.h5ad` 12.9GB(16:20, full이 smoke 덮어씀), obsm['cisTopic'] (21878,113136) ✓.
- **CRAK-Velo fit 진행 중**: B matrix 22928 region×2000 gene, velocity gene 911. cuda:1, "GPU card 0"=물리1.
  - ⚠️ **env 수정**: CRAK-Velo가 `TF_USE_LEGACY_KERAS=1`을 강제(recover_paras.py:210) → `tf-keras==2.15.1` 설치로 해결(memory 기록).
- 완료 watcher(background Bash, id **bv1k534o0**): `adata_rna_fit.h5ad` 파일 생성/에러 감지 → 4-way 재개. (이전 cisTopic watcher는 grep 패턴 버그로 완료 미감지 → 파일기반으로 교체.)
- 다음(fit 완료 시): lag 추출(DTW c-s) → `crakvelo_genes.csv` → p3_concordance 4-way → FINDINGS.md.

## 🟢 CPU 작업 — ✅ 완료
- **scrambled-chromatin null 완료**(15:07, 1h52m, 538 gene): `results/scrambled_genes.csv`.
- **검정 완료** `scripts/p3_scrambled_null.py` → `results/scrambled_null.md`:
  - **verdict: chromatin은 MultiVelo lag을 구동하지 않음.** lag 분포 동일(MW p=0.20, KS p=0.51), per-gene ρ=0.72, chromatin likelihood 거의 불변(0.239→0.237).
  - 단 Wilcoxon paired p=0.0003 — 작은 체계적 이동(median 5.87→5.48) = chromatin의 **marginal 기여**는 있으나 지배적 아님.
  - → H1의 'MultiVelo 100% chromatin-leads = 아티팩트' 결론을 음성대조로 확증.

---

## CRAK-Velo arm (4-way H1) — 단계 체크리스트
- [x] tf env 빌드 (TF2.15.1 GPU×3 + unitvelo --no-deps + scvelo + pybedtools)
- [x] vendor clone (CRAK-Velo, cisTopic) + torch_scatter
- [x] 입력 substrate `p2_crakvelo_prep.py` → consensus 197,482 peak + gencode 좌표 (`crakvelo_{atac,rna}_prepro.h5ad`)
- [x] **cisTopic** `p2_crakvelo_cistopic.py` → `crakvelo_atac_postpro.h5ad`  ✅ 완료(~16:20)
- [x] CRAK-Velo fit `p2_crakvelo.sh` + `p2_crakvelo_config.json` → `crakvelo_fit/`  ✅ (06-30 ~19:14)
- [x] lag 추출 (MoFlow식 DTW c-s lag) → `results/crakvelo_genes.csv`
- [x] p3_concordance METHODS에 `crakvelo` 등록 → 4-way H1 산출 + 문서
- [x] **lag 부호 convention 검증·수정**(2026-07-01) → `results/crakvelo_sign_check.md`. `dtw_lag`이 MoFlow와 반대 부호(버그)였음 → `i−j`로 통일(양수=chromatin선행), 단위·marker 검증. csv·concordance 재산출. **블로커 해소.**
- ⚠️ caveat: ATAC batch(day0/day7) 미보정 + peak-count overlap합산(fragments 미보유). 4-way H1 문서에 명기.

## CPU 작업 — 단계 체크리스트
- [x] scrambled-chromatin 러너 `p2_multivelo_scrambled.py` (within-lineage ATAC 셔플) + smoke 검증
- [x] **scrambled full run** → `scrambled_genes.csv` (538 gene)
- [x] `results/scrambled_null.md` — 검정 완료 (verdict: chromatin lag 미구동, marginal 기여만)
- [x] **permutation FDR (P4)** `scripts/p4_permutation_fdr.py` → `results/permutation_fdr.md` (2026-07-01):
  - (A) cross-method concordance permutation FDR: moflow×crakvelo ρ=−0.151(q=0.017✅), moflow×mvvae ρ=+0.083(q=0.051✅), crak×mvvae ρ=−0.040(q=0.47). **유의해도 effect 극약·방향 불일치.**
  - (B) per-gene sign-consistency agreement-set = **0/598 gene**(FDR<0.10) → 공집합. **H1(lag method-민감) 통계 확증.**
  - ⚠️ 범위 밖(추후): lineage 내 pseudotime-shuffle per-gene lag-크기 FDR(재-fit 필요), marker enrichment hypergeometric(§4C 2차).

---
### 변경 로그 (append-only)
- 12:54 — cisTopic full launch(cuda:1).
- 13:15 — scrambled-chromatin null full launch(CPU, PID 253142). cisTopic 11%(333/3000). 둘 다 watcher 설정.
- 14:23 — 상태 스냅샷: cisTopic 36%(1080/3000, ETA~16:20), scrambled 55%(350/641, ETA~15:13). 둘 다 정상. (scrambled는 7h 예상보다 빨라 ~2h.)
- 15:07 — scrambled full 완료(1h52m, 538 gene). 15:10 검정 완료 → scrambled_null.md(verdict: chromatin lag 미구동). cisTopic 62%.
- ~16:20 — cisTopic full 완료. `crakvelo_fit/`(datasplit·checkpoints) 생성됨.
- 17:11 — **CRAK-Velo fit launch**(cuda:1, PID 296334, env tf, --w 100000). 실행 중. [BIOP01 창 입력불가 → BIOP02 창에서 관측·대리 기록 18:15]
- 17:0x — tf-keras 2.15.1 설치(CRAK-Velo가 TF_USE_LEGACY_KERAS 강제 → optimizer ImportError 해결). 15:16 FINDINGS.md 종합본 신설. 논문 하네스 수령→제안서(`collab_workspace/harness/PROPOSAL-*.md`), 설치는 팀 상의 후.
- 18:29 — **자율 finisher 가동**(`scratchpad/finish_crakvelo.sh`, setsid·PID 307943): fit 완료 대기 → lag 추출(`p2_crakvelo_lag.py`) → 4-way concordance(crakvelo가 METHODS 등록됨) → 결과 staging. **창 닫혀도 완주**. ⚠️ CRAK-Velo lag sign convention은 marker로 검증 후 FINDINGS 반영(자동 안 함). 실패 시 안전 로그만(가짜 결과 금지).

- 19:15 ✅ **CRAK-Velo fit→lag→4-way 자율 완주**(창 닫힌 상태에서).
  - 산출: results/crakvelo_genes.csv, concordance.md(4-way 갱신, §3.5 자동).
  - ⚠️ **CRAK-Velo lag sign convention 미검증** — marker(AZU1/ELANE/MPO Myeloid=양수 기대) sanity는 finish_crakvelo.log 참조.
    sign OK 확인 후에만 FINDINGS.md canonical 4-way 결론 반영할 것(자동 안 함).

- 2026-07-01 ✅ **블로커 해소 + P4 완료** (Task 1·2):
  - **(1) CRAK-Velo lag 부호 검증·수정** → `results/crakvelo_sign_check.md`. 합성 신호 검증으로 `dtw_lag`(manual DP)이 MoFlow `fastdtw`와 **반대 부호**(버그)임 확인 → `i−j`로 통일(양수=chromatin선행). 단위검증 PASS, marker(CSF1R/S100A9 양수=chromatin선행, MoFlow myeloid markers도 양수) 생물학 검증. csv·concordance §3.5/§18 **재산출**. 부호 통일 후 moflow×crakvelo는 ρ +0.151→**−0.151**(genome-wide 약한 음의 일치, marker는 동의). **FINDINGS canonical 반영 가능.**
  - **(2) permutation FDR(P4)** `scripts/p4_permutation_fdr.py` → `results/permutation_fdr.md`. (A) 2/3 쌍 유의하나 effect 극약·방향 불일치. (B) agreement-set 0/598(FDR<0.1) = 공집합. **H1(lag method-민감) 통계 확증.**

- 2026-07-01 ✅ **P5 트랙 3종 완료**(accuracy·stability·predictability):
  - **simulator(accuracy)** `p5_sim_injected_lag.py` → `sim_injected_lag.md`+png. DTW c-s lag은 ground truth 있어도 lag 크기/순위 회복 실패(Spearman 일관 음수)·부호 regime 의존. H1 근원=construct 정확도 한계.
  - **bootstrap(stability)** `p5_bootstrap_stability.py` → `bootstrap_stability.{md,csv}`. fit 고정·표집서 부호 83% 안정(가장 약한 stability, H1 모순 아님).
  - **P5 모델(predictability)** `p5_lag_model.py` → `lag_model.{md,csv}`+png. held-out lineage: 순수 baseline chromatin으로 lag 비예측(ρ=−0.21), +fit feature 순환(ρ=+0.59). → baseline feature·α 중심 모델 방향.
  - FINDINGS §5(3각 검정) 신설·통합결론 갱신. 다음: 실제 day0 ATAC feature + per-lineage refit + drug perturbation arm(데이터/GPU 대기).
