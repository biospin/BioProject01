# HSPC chromatin–transcription velocity head-to-head benchmark — 설계 (v2)

> branch: `kkkim-pipeline` · v1 2026-06-13 · **v2 2026-06-13 (methodologist 검토 반영)**
> 근거: `analysis/epigenomic-lag/_evidence/week2/insight.md` Direction 1 / claim C5, `validation_report.md` §3, `CLAUDE.md` "방법론적 주의사항".
> 검토 반영: `REVIEW-methodologist-2026-06-13.md` (BLOCKER 5 + MAJOR 다수). v1의 H1 순환·H2 wall-clock 가정·lag accuracy 오해를 수정.
> 성격: **설계 문서**(코드/실행 전). 실행은 데이터 확보 + 환경(128GB RAM; **GPU는 선택** — 이 데이터 규모(11,605 cells)면 CPU로 충분, GPU는 bootstrap 반복 속도 이득만) 준비 후 Phase별.

---

## 0. 목적, 그리고 이 벤치마크가 측정할 수 있는 것의 한계

프로젝트 최종 목표는 gene별 chromatin→transcription lag 정량 → epigenetic drug response timing 예측. 그 1단계로 lag 정량 primary method를 *우리 데이터(GSE209878)에서* 정한다.

**먼저 정직하게 — 이 데이터에는 lag의 ground truth가 없다.** metabolic labeling·time-resolved per-cell clock·perturbation·injected-lag simulator가 전무하다. 따라서 §4의 lag metric은 전부 *accuracy*가 아니라 **reproducibility / stability / lineage-consistency**를 측정한다. 이 벤치마크가 답할 수 있는 질문은 "어떤 method가 우리 데이터에서 가장 *재현적·일관적*인 lag estimate를 내는가"이지 "가장 *정확한가*"가 아니다. 정확도 신호는 §5의 **injected-lag simulator arm**(secondary)에서만 부분적으로 얻는다.

**가설 (수정판)**
- **H1 (agreement → reproducibility, accuracy 아님)**: 두 chromatin-aware method가 lag *sign*에 합의하는 gene은 *bootstrap에서 더 재현적*이다. agreement는 robustness의 *necessary-not-sufficient* 신호다(공유 계보 bias로 함께 틀릴 수 있음 — §2 method 비독립).
- **H2 (강등됨 — confounded directional sanity check)**: day0/day7은 batch 제거 목적으로 Seurat 통합돼 day label이 batch와 aliased이고, 2 timepoint는 1 interval(보정곡선 불가)이며, day0→day7 변화는 주로 *cell-type composition shift*(in vitro 분화)다. 따라서 **wall-clock 단위 lag는 이 데이터로 산출 불가.** day label은 population 수준 pseudotime 단조성의 *방향 sanity check*로만, 그리고 method 선정 결정에서 **배제**한다(permuted-day-label control 동반).

**산출(정직판)**: ① lag estimate의 *재현성·일관성*이 가장 좋은 method 권고(accuracy는 simulator arm으로 보강) ② bootstrap-stable robust lag gene set ③ 각 method 한계의 우리-데이터 실측.

---

## 1. 데이터 (repo 검증치)

- **GSE209878** — Human HSPC, paired 10x Multiome (CellRanger ARC, 동일 nuclei). MultiVelo 원논문 데이터.
- 규모(확정, `li-2023-multivelo_core.md` L194): **11,605 cells × 1,000 genes(joint filtered), 936 variable genes fit, 11 Leiden cluster.** (검토 과정의 "~2,000"은 오류.)
- **single donor, Stemspan II in vitro 배양, day0 + day7** → day7은 7일 분화·확장. day0/day7은 **Seurat 통합**(batch 제거). 원논문은 **cell cycle(S/G2M) regress-out** 수행(Fig).
- 분화 축: HSPC → erythroid / myeloid / lymphoid / MK(platelet). 희소 lineage(MK/platelet)는 n 적음(아래 confound).

---

## 2. 비교 대상 method

| method | 분기/역할 | lag 출력 | 축 배정 | 비고 |
|---|---|---|---|---|
| **MultiVelo** | baseline (ODE/discrete) | switch time(scalar) | A + B/C | 단 home-field(§3.3) — annotation은 method-agnostic으로 재정의 |
| **MultiVeloVAE** | probabilistic multi-sample (δ/κ + Bayesian test) | δ/κ(rate) | A + B/C | CPU 실행 가능(GPU는 속도 선택). H1 한 축 |
| **MoFlow** | latent time-free relay | DTW c-s lag | A + B/C | license 확인. H1 한 축 |
| **CRAK-Velo** | UniTVelo 확장 semi-mechanistic | **명시 없음** | **A only**(기본) | lag axis는 proxy 독립검증 통과 후만(§4.2), proxy-derived 플래그 |
| **RNA-only floor (scVelo dynamical, cellDancer)** | chromatin 기여 대조 | rate/lag | **REQUIRED** baseline | chromatin-aware가 RNA-only 대비 *얼마나* 개선하는지의 floor |
| (선택) mmVelo | decoder-level peak resolution | peak-level | A 보조 | per-peak ODE rate 없음 — 해석 prior 주의 |
| (음성대조) scrambled-chromatin | ATAC permutation | — | ablation | chromatin 채널이 장식인지 검정 |
| (정확도) injected-lag simulator | 합성 ground truth | known lag | **secondary accuracy arm** | BEELINE/SERGIO fork (C8) |

H1 핵심 쌍 = MultiVeloVAE ↔ MoFlow. 단 계보 비독립(MoFlow⊃cellDancer, MultiVeloVAE⊃MultiVelo)이라 독립 계열 1개를 tie-breaker로 둔다.

---

## 3. 통일 전처리 + 공정성 (C2 + 검토 MAJOR)

- **공통 branch**: 동일 cell/gene/peak QC → 동일 normalization → 동일 HVG → 동일 peak-to-gene 입력. 단일 `MuData`에서 출발. **joint peak calling**(timepoint별 따로 X) 확인.
- **ambient/doublet 제거** (검토 추가): SoupX/CellBender + Scrublet — unspliced ratio가 ambient에 민감, 미제거 시 artifact가 모든 RNA-coupled method에 동일 전파돼 *가짜 agreement*로 위장.
- **method-specific branch**는 권장값 사용하되 명시 기록 + **공통 neighbor-graph ablation**(native graph vs 공통 graph) — graph 선택이 model보다 결과 좌우 가능.
- **method-agnostic annotation** (3.3): cluster/lineage label을 공통 graph Leiden 또는 marker 기반으로 정의·**freeze 후** velocity 실행. MultiVelo-native annotation 대비 sensitivity 보고(MultiVelo home-field 제거).
- shared gene/cell intersection + drop bias 보고(C6). lineage별 **expression/coverage floor** 사전 설정(low-expression gene CI 폭주 방지).

---

## 4. 평가 지표 (전부 lineage 내에서 계산 후 집계)

> **모든 concordance/lag 비교는 lineage 내에서.** pooling은 method 차이와 composition 차이를 혼동.

**A. trajectory sanity (tie-breaker, lag 품질 아님)** — CBDir, GCBDir 둘 다 동일 input에서. annotation bias 상속·굵은 방향만 보상하므로 **1차 결정 근거 아님**.

**B. lag-specific (consistency, accuracy 아님)** — MoFlow DTW lag / MultiVeloVAE δ·κ / MultiVelo switch time / (검증 시) CRAK-Velo proxy. 정의가 비교 불가한 이질적 양이므로:
- **sign-agreement와 rank-correlation(Spearman)을 분리 보고** (병합 금지).
- monotonicity 가정은 명시하거나, 안 되면 **sign-only**로 강등.
- known-gene **construct-validity sign check**(교과서적 erythroid TF 등에서 네 정의가 최소 sign 일치하는지) 선행 — 실패 시 global rank-corr 무의미.

**C. agreement set (H1, stability 기반)** — 1차 기준 = **bootstrap lag-sign stability**(agreement gene이 disagreement gene보다 sign-flip rate 낮음, gene 단위 paired test). 2차 = dynamic-gene background 대비 marker/regulator enrichment(hypergeometric + permutation-FDR). whole-genome background 금지(순환).

**D. 자원/안정성** — runtime, peak memory. subsample/bootstrap 반복(횟수는 GPU 실측 후 결정) → lag 분포. "negative correlation across repeats"는 *self-consistency(stability)*로 명명(validity 아님).

**음성대조/null**: scrambled-chromatin(lag 거의 안 변하면 chromatin 장식), no-lag null(모든 metric이 이 null을 이겨야 함), permuted-day-label(H2가 살아남으면 batch 포착).

---

## 5. Confound 통제 (operationalize — naming 아님)

1. **Pseudotime ≠ wall-clock (#1)**: lag는 **pseudotime 단위로만** 보고. H2는 §0대로 강등.
2. **Cell cycle + burst (#2)**: lag에 사후 covariate 불가 → cell-cycle score로 **stratify** 또는 quiescent cell 한정, cycling 포함/제외 양쪽 보고(원논문도 regress-out).
3. **ATAC depth/peak batch**: timepoint별 ATAC QC(depth/FRiP) 보고, joint peak set 확인.
4. **Lineage-specific kinetics + composition imbalance**: 모든 비교 lineage 내. 희소 lineage(MK/platelet)는 n 적어 불안정→"disagreement"가 sampling artifact일 수 있음 → set 멤버십 vs lineage abundance 보고.
5. **Multiple testing (#5)**: **permutation FDR**(lineage 내 cell/pseudotime shuffle) — 공조절 gene 비독립이라 parametric FDR anti-conservative. test family 경계 명시.
6. **Multicollinearity (#3)**: downstream feature model용 — 본 단계 범위 밖(메모).

**accuracy arm (검토 BLOCKER 3)**: injected-lag chromatin-aware simulator(BEELINE/SERGIO fork)를 secondary로 — known lag를 *recover*하는 method를 측정(유일한 진짜 정확도 신호).

---

## 6. 성공 기준 (reproducibility 중심으로 reframe)

- **H1**: agreement gene이 bootstrap lag-sign stability에서 disagreement보다 유의하게 높음(gene 단위 paired, pre-registered 임계). enrichment는 dynamic-gene background 대비 2차 확인.
- **method 선정**: 1차 = lag-specific consistency(B) + stability(D) + simulator recovery(§5). A(trajectory)는 tie-breaker만. 단일 우월 없으면 "MoFlow primary(lag) + MultiVeloVAE secondary(differential test)" cross-validation 전략(`해석:`).
- **accuracy 미주장**: 모든 결론에 "lag accuracy는 이 데이터로 미검증(simulator arm 제외)" 명시.
- **external replication**: ranking을 팀의 다른 multiome(mouse brain/skin)로 1회 외부 재현(단일 데이터 desk-reject 방지).

---

## 7. 단계(Phase)

| Phase | 내용 | 산출물 |
|---|---|---|
| **P0 환경·데이터·사전체크** | GSE209878 download; **per-cell timepoint label이 통합 객체에 보존됐는지 확인**; license(MoFlow·mmVelo); CPU 1-fit 시간/메모리 실측(GPU 불필요, 길면만 GPU 검토); dataset-info.yaml | `P0_provenance.md`, `dataset-info.yaml` |
| **P1 통일 전처리** | 공통 branch + ambient/doublet 제거 + joint peak 확인 + method-agnostic annotation freeze + shared intersection | `preprocess/`, `qc_report.md` |
| **P2 method 실행** | baseline(RNA-only) + chromatin-aware + scrambled-chromatin ablation; native vs 공통 graph; runtime/memory 로깅 | per-method outputs, `runtime.csv` |
| **P3 지표·일치도** | A(tie-break)/B(sign·rank 분리)/C(stability) lineage 내; construct-validity sign check | `metrics/`, `concordance.md` |
| **P4 confound·null·simulator** | cycle stratify, permutation FDR, no-lag/scrambled/permuted-day null, simulator accuracy arm | `confound_report.md`, `simulator/` |
| **P5 종합·권고·외부재현** | method 선정 + robust gene set + enrichment + 타 dataset ranking 재현 | `RESULTS.md`, `robust_lag_genes.csv` |

> 대용량 중간산출(.h5ad 등)·원문 binary는 `.gitignore`. tracked = `*.md`, 요약 `*.csv`, config, 코드.

---

## 7b. Compute 자원 (CPU vs GPU — GPU 1대 가용 가정)

전제: 데이터 규모 11,605 cells × ~1,000 genes(+ ~3,939 peaks)는 single-cell 기준 **중소 규모**. GPU 1대 빌릴 수 있으면 충분하며, 이 규모에선 **VRAM이 아니라 system RAM이 실제 병목**이다. 아래 runtime은 *추정* — P0의 1-fit 실측으로 확정한다.

| method | 엔진 | CPU 단일 fit (추정) | GPU 이득 | VRAM 필요 | 비고 |
|---|---|---|---|---|---|
| **MultiVelo** | CPU 전용 | ~2h (원논문 124분/12-thread, 동일 데이터) | **없음**(GPU 미지원) | — | 4개 중 RAM·runtime 최대 |
| **MultiVeloVAE** | PyTorch VAE | ~30분–2h | ~5–10× | 2–6 GB | bootstrap 반복에 GPU 유리 |
| **MoFlow** | PyTorch Lightning | ~30분–1h | ~5–10× | 2–6 GB | |
| **CRAK-Velo** | TensorFlow (UniTVelo 확장) | **~15h** (원논문, HSPC) | **큼**(TF GPU 가속) | 4–8 GB | **GPU 최대 수혜** |
| RNA-only floor (scVelo dyn. / cellDancer) | CPU / DL | scVelo ~10–30분(CPU) | cellDancer만 GPU 선택 | 2–4 GB | |
| simulator arm | CPU | 경량 | — | — | |

**핵심**
- **GPU 1대로 충분.** DL 3종(MultiVeloVAE·MoFlow·CRAK-Velo)을 GPU에서 *순차* 실행. 모델·데이터가 작아 8 GB VRAM이면 여유, 24 GB면 넉넉. VRAM은 이 규모에서 병목 아님.
- **MultiVelo는 GPU 이득 0** → CPU(12+ thread)로 병행, GPU는 DL 메소드에 양보.
- **GPU의 진짜 가치 = ① CRAK-Velo(15h→대폭 단축) ② bootstrap 반복**(§4D, 모든 metric을 N배) 현실화. GPU 없으면 bootstrap 횟수 축소 또는 posterior sample로 stability 대체.
- **System RAM이 실제 제약**: 11k cells는 작지만 ATAC peak matrix + 다중 method 중간산출(.h5ad) 동시 적재 → **32–64 GB 권장(128 GB면 여유)**. CLAUDE.md의 128 GB 목표는 이 단계엔 충분.

**권장 환경(1 GPU)**: GPU 8–24 GB VRAM 1대 + CPU 12+ thread + RAM 64 GB↑ + 디스크 ~200–500 GB(raw + intermediate). 이전 설계의 "GPU 필수"는 철회 — *CPU만으로도 실행 가능하되, 1 GPU가 있으면 CRAK-Velo와 bootstrap이 실용적*이 된다.

## 8. 열린 결정 / 사전체크 (P0에서 확정)

- [ ] **per-cell `timepoint` 라벨**이 *통합 후* 객체에 남아있는지 — 없으면 H2의 약한 형태도 불가.
- [ ] **license**: MoFlow(=H1 한 축, 없으면 H1 쌍 재구성), mmVelo(CC-BY 4.0 추정, repo 확인).
- [ ] **CPU runtime**: MultiVeloVAE/MoFlow 1-fit 시간/메모리 실측(11k cells면 CPU 충분 예상) → bootstrap 반복 횟수 결정(너무 길면 posterior sample로 stability 대체). GPU는 반복이 비현실적으로 길 때만 도입.
- [ ] **CBDir+GCBDir** 단일 구현으로 동시 계산 가능 여부.
- [ ] **CRAK-Velo proxy** 5–10 gene pilot(switch time 대비) — 통과 못 하면 axis A only 유지.
- [ ] **simulator**: BEELINE/MultiVelo-authors sim script 우선 검토, 없으면 SERGIO를 time-event annotation 가능하게 fork.
- ~~cell-count 모호~~ → **11,605 확정**(repo 검증).

---

## 9. 다음 행동

1. **P0 착수** (현재): GSE209878 + license 확인 + 환경 spec + dataset-info.yaml + 사전체크 6항목.
2. (선택) 박상준 교차 크리틱으로 2차 검토.
3. P1 통일 전처리 코드 스캐폴딩.

> 변경 이력: v1→v2는 methodologist 검토(BLOCKER 5)를 반영 — H1 순환 제거(stability 1차), H2 wall-clock 강등, lag=consistency reframe + simulator accuracy arm, RNA-only/scrambled REQUIRED, CRAK-Velo axis A 격리, within-lineage·ambient/doublet·permutation-FDR 추가.
