# 사전등록 — 층② 세포×유전자 velocity 행렬 감사 (BIOP01-59)

> 2026-07-19. **결과를 보기 전에 봉인한다.** 이 문서의 정의·임계·제외규칙은 실행 후 바꾸지 않는다.
> 사후에 유리한 쪽으로 정의를 고르는 것을 막기 위한 장치다(GSE205117 사전등록과 같은 방식).

## 0. 왜 하나

RNA velocity 산출은 세 층이다.

```
①  유전자별 kinetic 모수     α, β, γ, α_c, lag        ← 현 논문이 감사한 층
②  세포×유전자 velocity 행렬  v = βu − γs              ← 본 감사 대상
③  세포 수준 velocity 벡터    ②를 임베딩에 투영한 화살표  ← 사람들이 실제 쓰는 용도
```

현 draft는 Discussion의 scope 문장으로 ②·③을 명시적으로 범위 밖에 남겨두었다. 본 감사는 그 유보를 실제 측정으로 채운다. **①의 결론을 ②로 자동 확장하지 않는다** — ②는 별도 측정이며 결과는 정해져 있지 않다.

## 1. 데이터·layer (고정)

- HSPC 10x Multiome, **21,878 cells 전량**(5개 arm 세포 barcode 완전 일치 확인됨).
- **5개 arm 공유 505 gene**. 유전자·세포는 **이름으로 정렬**한다(위치 정렬 금지).
- 비교 layer는 **spliced velocity로 통일**:

| arm | 사용 layer | 크로마틴 사용 |
|---|---|---|
| MultiVelo | `velo_s` | ○ |
| MoFlow | `velo_s` | ○ |
| CRAK-Velo | `velocity` | ○ |
| MultiVeloVAE | `vae_velocity` | ○ |
| scVelo-dynamical (RNA-only) | `velocity` | **✗ (기준선)** |
| MultiVelo-scrambled | `velo_s` | ATAC 셔플 |
| MoFlow-scrambled | `velo_s` | ATAC 셔플 |

- **chromatin velocity(`velo_chrom`·`velo_c`·`vae_velocity_c`)는 섞지 않는다.** 층이 다르다.

## 2. 사전 확정한 처리 규칙 (과거에 물린 함정의 형제)

1. **NaN 열 제외**: scVelo는 dynamics 미복원 유전자를 NaN velocity로 남긴다. **어느 한 arm에서라도 NaN이 있는 유전자는 전 분석에서 제외**하고, 제외 개수를 결과에 명기한다.
2. **분산 0 열 제외**: 어느 arm에서든 세포 축 분산이 0인 유전자 제외(코사인 정의 불가).
3. **정확히 0인 항목**: 부호 일치율에서는 **어느 한쪽이라도 정확히 0이면 "방향 미정"으로 제외**한다(`CORRECTION_sign_agreement_zero_handling.md`와 동일 규약). 코사인에서는 0을 그대로 둔다(내적 0, norm 기여 0) — 이 비대칭을 결과에 명기한다.
4. **크기 비식별성**: 주 분석은 **원척도 코사인**(화살표 방향 그대로의 해석). 민감도 분석으로 **유전자별 SD로 나눈(중심화 없음) 스케일 코사인**을 함께 보고한다 — 중심화하면 부호가 사라지므로 z-score는 쓰지 않는다.

## 3. 측정 축

- **(1) 세포별 코사인**(유전자 축, 세포마다 1개): "화살표가 일치하는가"에 가장 가깝다.
- **(2) 유전자별 코사인**(세포 축, 유전자마다 1개): 어떤 유전자가 세포수준 방향을 재현시키는가.
- **(3) (cell,gene) 부호 일치율**: 가장 세밀한 판정.

### 필수 null — 이게 없으면 숫자가 부풀려 읽힌다
- **세포 짝 셔플**: method A의 세포 i 와 method B의 **무작위 세포 j** 코사인. 모든 velocity 벡터가 전역적으로 비슷한 방향을 향하면 짝이 맞든 안 맞든 코사인이 높다. 이 null 대비 초과분만이 진짜 세포 수준 일치다.
- **유전자 셔플**: (2)의 대응 null.

## 4. ★ 결론을 가르는 대조 2종

원 코사인 값 자체는 발견이 아니다(층①에서 α=0.88이 발현량 0.81 대비로만 의미를 가졌던 것과 같은 구조). 비교 대상이 전부다.

**(A) 기준선 대조 — RNA-only**
multiome arm 끼리의 일치(6쌍)가 각 multiome arm과 **RNA-only** 사이의 일치(4쌍)보다 **실제로 높은가**.
- 높지 않다면 → 크로마틴은 세포수준 방향에 재현 가능한 기여를 하지 않는다.

**(B) 인과 대조 — ATAC-shuffle**
같은 method에서 크로마틴만 파괴했을 때(`multivelo_scrambled`·`moflow_scrambled`) velocity 행렬이 얼마나 움직이는가.
- 기준자: 같은 method 원본↔셔플 코사인 vs 서로 다른 method 간 코사인.
- 거의 안 움직이면 → 화살표를 끄는 것은 크로마틴이 아니다(lag에 쓴 것과 같은 인과 논리, 단 더 깨끗하다 — method family 차이가 섞이지 않는다).

## 5. 봉인된 판정 규칙

실행 전에 못박는다. **양성 결과가 가능하며, 그게 이 검정을 돌릴 이유다.**

| 판정 | 조건 |
|---|---|
| **POSITIVE** (층①에서 못 얻은 새 소견) | multiome↔multiome 코사인 중앙값이 multiome↔RNA-only보다 **유의하게 높고**(부트스트랩 95% CI 비중첩) **동시에** ATAC-shuffle에서 유의하게 무너진다(원본↔셔플 코사인 < 원본↔다른 method 코사인) |
| **NEGATIVE** | 위 둘 중 하나라도 성립하지 않는다 → 층①의 결론이 층②로 확장된다 |
| **INCONCLUSIVE** | 사용 가능 유전자 < 100 또는 null 대비 초과분이 전 쌍에서 0에 가까움(측정 자체가 정보 없음) |

- 부트스트랩: 세포 재표본 B=1,000, seed=20260719.
- **결과가 나쁘면 나쁜 대로 적는다. 사후 구제·정의 변경 금지.**

## 6. 논문 편입 정책 (선결)

- 현 draft의 **동결된 주장 5개는 이 결과로 자동 수정하지 않는다.**
- 결과가 NEGATIVE면 → Discussion scope 문장을 유지하되 한 문장으로 보강할지 **별도 판단**.
- 결과가 POSITIVE면 → 새 축이므로 **후속 논문/별도 티켓**이 기본. 현 draft에 넣으려면 scope 문장(주장 #4)과의 정합을 먼저 정리해야 한다.
- 어느 쪽이든 2026 벤치마크 [12,13]이 ②(행렬)를 봤는지 ③(임베딩)을 봤는지 확인한 뒤에 서술한다(중복·모순 방지).

---

# 부록 — 외부 재현 사전등록 (BIOP01-60), 2026-07-19 추가 봉인

> 본편(HSPC)의 결과를 **본 뒤에** 쓰는 확장이므로, 무엇을 재현 검정하는지와 판정 기준을 **외부 데이터를 열기 전에** 다시 못박는다.
> 지표·제외규칙은 위 §1~§3을 **그대로** 쓴다(정의를 외부에 맞춰 바꾸지 않는다).

## A. 왜
현 draft의 다른 결론은 전부 6개 시스템 일관성으로 방어하는데 층② 결과만 **HSPC 단일 시스템**이다. 이것이 일화인지 패턴인지 검정한다.

## B. 대상 (이미 fitting된 것만, 추가 fit 없음)
| 시스템 | arm | 공유 세포 | 공유 유전자 |
|---|---|---|---|
| gastrulation GSE205117 (mouse) | MultiVelo·MoFlow·MultiVeloVAE·scVelo(4) | 10,779 | 968 |
| macrophage | MultiVelo·MultiVeloVAE·scVelo(3) | 3,572 | 871 |
| BMMC GSE194122 | MultiVelo·MultiVeloVAE·scVelo(3) | 2,850 | 272 |
| E18 mouse brain | MultiVelo·MultiVeloVAE·scVelo(3) | 4,423 | 1,027 |

## C. 무엇을 재현 검정하는가
HSPC에서 본 **순서** — *multiome 방법끼리의 일치가 multiome↔RNA-only 기준선을 넘지 못한다*. 세포 단위 paired 부트스트랩(B=1,000, seed 20260719)으로 Δ = (multiome×multiome 평균) − (multiome×RNA-only 평균)와 95% CI.

## D. ★ 무엇을 재현할 수 **없는지** (미리 명시)
1. **인과 대조(ATAC-shuffle)는 재현 불가** — 외부에 scrambled arm이 없다. 인과 결론은 **HSPC·MultiVelo 한정**으로 남는다.
2. **재현성 천장을 시스템별로 잴 수 없다** — 외부에 bootstrap refit이 없다. HSPC 천장(중심화 +0.872)을 참조로 쓰되, **시스템마다 천장이 다를 수 있다**는 한계를 결과와 논문 양쪽에 적는다.
3. macrophage·BMMC·E18은 multiome arm이 2개뿐이라 multiome×multiome 쌍이 **1개**다. gastrulation만 3쌍.

## E. 봉인된 판정 규칙
| 판정 | 조건 |
|---|---|
| **REPLICATED** | 4개 시스템 중 **3개 이상**에서 Δ ≤ 0 이고 그 95% CI가 양수 영역을 배제 |
| **NOT GENERALIZED** | **2개 이상**에서 Δ가 유의하게 양수(multiome끼리가 기준선보다 실제로 더 잘 맞음) → draft의 해당 문단을 **HSPC 한정으로 축소** |
| **MIXED** | 그 사이. 사후 구제 없이 MIXED로 적는다 |

- 부수 관측(판정에 쓰지 않음): 시스템별 cross-method 부호 일치율, 세포 셔플 귀무 대비 초과분.
- **결과가 나쁘면 나쁜 대로 적는다.**

## F. 산출물
`scripts/p10c_velocity_matrix_external.py` · `results/velocity_matrix_audit_external.md` · `results/velocity_matrix_audit_external_pairs.csv`

---

## 7. 산출물

`scripts/p10_velocity_matrix_audit.py` · `results/velocity_matrix_audit.md` · `results/velocity_matrix_audit_pairs.csv`
