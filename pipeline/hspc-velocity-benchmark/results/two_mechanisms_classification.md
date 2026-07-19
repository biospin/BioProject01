# "두 기작"(chromatin-leading vs RNA-first) 유전자 분류가 재현·예측 가능한가 — make-or-break (BIOP01-55)

> 2026-07-19. 질문(kkkim): ~50/50 chromatin-leading/RNA-first split을 "두 개의 다른 기작"으로 승격해 유전자별로 분류·차등 예측 가능한가? naive(velocity lag 부호)는 이미 죽음(2-method sign-agreement 48%=우연). 부호 가변 3 method(MoFlow·CRAK·VAE)의 방향을 **생물학(canonical marker)으로 규약 정렬** 후 재현성 검정.

> ⚠️ **정정(2026-07-19)**: 아래 pairwise sign-agreement 수치는 **0(방향 미정) 처리를 명시하지 않은 값**이다. `cs_lag_median`에 정확히 0인 값이 다수 있어(MoFlow 76/636, CRAK 135/868) 계산 방식에 따라 값이 달라진다. **정정된 값(0 제외)** = MoFlow×CRAK **42.3%**(n=239) · MoFlow×VAE **54.6%**(n=560) · CRAK×VAE **46.6%**(n=277). 상세·근거 = `results/CORRECTION_sign_agreement_zero_handling.md`. **정성적 결론(per-gene 방향 비재현)은 불변.**

## 방법
- 부호 가변 방향 지표: MoFlow `cs_lag_median`, CRAK-Velo `cs_lag_median`, VAE rate-proxy(1/α_c−1/α).
- 규약 정렬: 각 method에서 myeloid priming marker(ELANE·AZU1·MPO·LYZ·CSF1R) mean − HSC marker(HLF·CRHBP·MEIS1) mean 이 양이면 규약이 생물학과 일치(chromatin-first=+). 셋 다 **flip 불필요**(이미 일치): myeloid−HSC = MoFlow +0.356 · CRAK +1.500 · VAE +0.071.

## 결과
**규약 정렬 후 pairwise per-gene sign-agreement (chance=50%):**
| 쌍 | sign-agree | rank ρ |
|---|---|---|
| MoFlow × CRAK | **32.4%** (n=330) | −0.151 |
| MoFlow × VAE | **48.1%** (n=636) | +0.083 |
| CRAK × VAE | **38.6%** (n=334) | −0.040 |

**고신뢰 부분집합(양쪽 |cs_lag| 상위, MoFlow×CRAK):** 전체 32.4% → 상위50% 42.1% → 상위33% **44.4%** (우연 수준 유지, 구제 안 됨).

## 판정 — per-gene 분류 재현 **실패** (사전 반증기준 (a),(b) 충족)
- 세 독립 부호 가변 method가 유전자를 두 기작으로 **우연(혹은 그 이하)으로 배정** — 규약 정렬·고신뢰 제한 후에도. **"gene X는 chromatin-leading"이 method 바꾸면 뒤집힘** → 신뢰할 per-gene 분류·차등 예측 **불가**. (advisor 5번째 양성 탐색, "실패 시 lock" 조건 충족.)

## 그러나 살릴 것 — **aggregate 계통 구조는 재현**(= (A) 프레이밍의 근거)
- **세 method 모두** myeloid priming 유전자(ELANE·AZU1·MPO)를 chromatin-first, HSC 유지 유전자(HLF·CRHBP)를 RNA-first 쪽으로(myeloid−HSC 전부 양). → **거친 계통 수준의 방향 구조는 method 간 일치**.
- 정직한 서술: "population은 ~50/50 chromatin-leading/RNA-first 두 regime으로 갈리고, 그 방향은 **계통 수준에서는** 세 method가 일치하며 생물학과 맞는다(myeloid vs HSC). **그러나 현재 방법들은 개별 유전자를 이 둘로 신뢰성 있게 분류하지 못한다(per-gene 방향 일치 32~48%=우연).**" → 음성을 풍부하게(두 regime 존재) 하되 per-gene 정량/예측 불가를 명시. 헤드라인 아님, supporting.
