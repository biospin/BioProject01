# H1 lag 무상관 진단 — multivelo × multivelovae (2026-06-30)

> 발단: `concordance.md` §3.5에서 multivelo×multivelovae lag Spearman **−0.01**(무상관) 산출.
> 원인이 (a) 진짜 method 불일치인지 (b) lag 정의가 비교 불가한 다른 양인지(proxy 부적합) 진단.
> 입력: `multivelo_genes.csv`(fit_*, 538 fit gene) ∩ `multivelovae_genes.csv`(vae_*, 641 gene) = **shared 538**.

## 1. 원래 비교는 apples-to-oranges였다
- §3.5의 lag 정의가 method별로 **달랐음**:
  - multivelo: `fit_t_sw2 − fit_t_sw1` (switch-**timing** 차이, pseudotime)
  - multivelovae: `1/vae_alpha_c − 1/vae_alpha` (rate **timescale** 차이)
- timing 차이 ≠ timescale 차이 → 무상관이 부분적으로 정의 불일치 아티팩트.
- (multivelovae는 chromatin/RNA 개별 switch time을 노출 안 함 — `vae_ton` 1개뿐. 그래서 rate-proxy가 유일한 선택지였음.)

## 2. 같은 rate 파라미터 method간 일치 (convergent validity)
| param | 의미 | Spearman | 판정 |
|---|---|---|---|
| **alpha** | transcription rate | **+0.882** (p=1e-177) | 강건 ✓ |
| **alpha_c** | chromatin opening rate | **+0.291** (p=6e-12) | 약함 ⚠️ |
| beta | splicing | +0.080 (p=0.06) | 거의 무상관 |
| gamma | degradation | −0.109 (p=0.01) | 거의 무상관 |

→ **두 method는 전사율(α)은 강하게 합의하지만 chromatin opening rate(α_c)는 약하게만 합의.**
lag은 α_c에 의존 → lag이 α_c의 method-민감성을 그대로 상속.

## 3. Apples-to-apples (양쪽 모두 rate-proxy `1/α_c − 1/α`로 통일)
- Spearman(rank) **+0.124** (p=0.004) — 통일해도 약한 양의 상관에 그침.
- sign-agreement **49.8%** — 동전던지기, chromatin이 선행/후행인지 directional 합의 없음.

## 4. MultiVelo 내부 self-consistency
- 같은 method 안에서 `switch-lag(sw2−sw1)` vs `rate-proxy(1/α_c−1/α)` = Spearman **+0.467**.
- 한 method 안에서도 두 lag 정의가 중간 정도만 일치 → switch-timing과 rate-timescale은 관련은 있으나 별개 양.

## 결론
1. 원래 ρ=−0.01은 **일부** 정의 불일치 아티팩트. 정의 통일 시 ρ=+0.12로 개선되나 여전히 약함.
2. 근본 원인 = **chromatin opening rate(α_c) 추정의 method 의존성**(ρ=0.29). 전사율 α는 강건(0.88)하나 lag을 결정하는 α_c가 흔들림.
3. **H1(cross-method lag 일치도)은 현재 2-method로는 약함**이 정직한 결론. lag 크기·방향 모두 method-민감.
4. 함의: chromatin→transcription lag을 단일 method로 보고하면 안 되며, α_c 추정 안정화 또는 sign-가변 method(MoFlow DTW) 추가로 3-way 교차검증 필요. lag을 baseline feature로 쓰는 drug-timing 모델은 이 method-민감성을 uncertainty로 반영해야 함.

## 다음
- MoFlow(GPU) DTW c-s lag 추가 → 3-way. DTW는 timing 기반이라 multivelo switch-lag과 정의가 더 가까움.
- α_c 안정성: bootstrap/per-lineage fit으로 α_c 추정 분산 정량(H1 stability).
- (재현) 위 수치는 `scripts/p3_concordance.py` §3.5 + 본 진단 1회성 스크립트로 산출.
