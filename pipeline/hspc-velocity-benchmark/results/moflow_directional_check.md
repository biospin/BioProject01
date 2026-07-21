# MoFlow c-s lag directional check (P3 / BIOP01-26)

> 작성 2026-07-03. DESIGN §4B의 "진짜 directional sign check". 결론은 `FINDINGS.md §1`·
> `permutation_fdr.md`에 이미 통합돼 있으며, 이 문서는 그 directional 축을 한 곳에 정리한 것.

## 0. 질문
MultiVelo lag sign(`sw2 − sw1`, switch-time 차)이 **switch-time에 단조정렬**돼
전 gene에서 구조적으로 양수로 나온다(= chromatin이 항상 선행하는 것처럼 보임).
이게 **생물학적 방향**인가, 아니면 **모델 구조 아티팩트**인가? → 부호가 **가변인** 독립
method(MoFlow c-s lag)로 판정한다.

## 1. MultiVelo sign은 구조적·무정보 (tautology)
- MultiVelo lag = `sw2 − sw1`(chromatin/RNA switch-time 차). 모델이 switch를 단조 배열 →
  **485/485 gene, 전 12 refit에서 항상 양수**(`bootstrap_refit.md`).
- 즉 "어느 gene이 chromatin-leading인가"에 대해 MultiVelo sign은 **정보를 담지 않는다**
  (값이 항상 +이므로 gene 간 방향 구분 불가). directional 주장에 쓸 수 없다.

## 2. MoFlow c-s lag = 부호 가변 → directional 판정 가능
- MoFlow는 실제 relay-velocity **모델 fit** 후 `get_dtw()`로 chromatin→spliced DTW lag을 산출
  (`scripts/p2_moflow.py`). MultiVelo의 switch-time 정렬과 달리 **부호가 gene마다 가변**.
- **실행 검증(블로커 해소)**: 2026-06-30 **GPU 실행**(`runtime.csv`: `moflow … gpu=True`,
  636-gene full run 2,836s). 산출 `data/velocity/moflow.h5ad`는 완전한 velocity layer
  (`velo_s`, `velo_c`, `alpha_c`, `stateon/off` …) + `obs['velo_s_pseudotime']` 보유 = 진짜 fit.
  `results/moflow_genes.csv` = 636 gene, cs_lag 636/636 산출, 범위 −0.381 ~ +0.381.

## 3. 결과 — MultiVelo의 100% 양수는 아티팩트로 확증
| 지표 | 값 | 함의 |
|---|---|---|
| MoFlow chromatin-leads(cs_lag>0) 비율 | **44.8%** | 전역 ≈50/50 → "chromatin이 transcription을 항상 prime" **미지지** |
| MoFlow × MultiVeloVAE lag Spearman | **+0.083** (perm FDR q=0.051) | 크기 무상관 |
| MoFlow × CRAK-Velo lag Spearman(부호통일 후) | **−0.151** (q=0.017) | 4번째 method도 무상관/약한 음 |
| MoFlow × MultiVeloVAE gene 수준 sign-agreement | **48%** | 우연 수준 |
| per-gene cross-method sign-consistency agreement-set | **0/598** (FDR<0.10) | 공집합 |

→ 부호 가변 method(MoFlow)에서 방향이 **균형(44.8%)**이고 다른 method와 무상관이므로,
MultiVelo의 **485/485 항상 양수는 생물학이 아니라 switch-time 단조정렬(모델 구조) 아티팩트**로
확증된다. **강건한 것은 (a) 집단 수준 방향 균형(~50/50, method 수렴), (b) canonical priming
marker(CSF1R·S100A9 등 — MoFlow·CRAK-Velo 모두 chromatin-leading으로 일치)뿐.**

## 4. Caveat (accuracy arm과의 정합)
`sim_injected_lag.md`에서 DTW c-s lag construct는 **매끄러운 kinetic에서 per-gene 부호가
불안정**함을 보였다. 이는 "MoFlow per-gene sign을 개별 gene 방향 주장에 못 쓴다"는 것이지,
본 directional 결론을 약화시키지 않는다 — 오히려 **집단 수준 균형(44.8%)이 MultiVelo의 100%
양수와 대비**되어 "MultiVelo sign = 구조적" 결론을 **강화**한다. per-gene directional 주장은
어느 method로도 하지 않는다(cross-method 무상관·FDR 공집합이 근거).

## 5. 상태
- **BIOP01-26 deliverable 충족**: MoFlow c-s lag directional check 완료. GPU 블로커(BIOP01-22 의존)는
  6/30 GPU 실행으로 **해소**됨(티켓 생성 7/1 시점 서술이 산출물 시각보다 뒤처져 있었음).
- 결론은 `FINDINGS.md §1`, `permutation_fdr.md`(A)(B), `bootstrap_refit.md`(tautology)에 통합 반영됨.
