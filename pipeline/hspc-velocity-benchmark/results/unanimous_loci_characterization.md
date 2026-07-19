# 방향이 method 만장일치인 loci는 어떤 유전자인가 (BIOP01-55 후속 특성화)

> 2026-07-19. `results/per_gene_direction_by_method.csv`(부호 가변 3 method 합의)에 coupling·abundance·곡률·rate를 결합해 특성화.
> 산출: `results/unanimous_chromatin_genes.csv`(만장일치 chromatin-leading 83개 + 특징).

## 어떤 loci인가 — 고발현 계통 effector 유전자
만장일치 chromatin-leading 83개 중 coupling 상위: **MPO · ELANE · AZU1 · PRTN3 · LYZ · CLC**(과립구 granule 단백질) · **HBD · ANK1 · SLC40A1**(적혈구) · **ITGA2B · MMRN1**(거핵구) · **GATA2 · CST3 · ALOX5 · TIMP3 · SLC18A2** 등 — 전형적인 **말단 분화 effector/과립 유전자**.
만장일치 RNA-first(164개)는 저발현·광범위 발현 유전자가 다수(S100Z·EIF2AK3·SLC4A4·TIAM1·WWOX·UTP6·GAB1 등).

## 특징 (median, 부호 가변 method ≥2 유전자 640개)
| 지표 | 만장일치 chromatin(83) | 만장일치 RNA(164) | split(393) | MW(chrom vs split) |
|---|---|---|---|---|
| **fit_alpha (전사속도)** | **2.853** | 0.215 | 1.147 | **p=8.8e-05** |
| **abundance (평균발현)** | **0.109** | 0.017 | 0.054 | **p=1.7e-03** |
| coupling (크로마틴-RNA 결합) | 0.086 | 0.117 | 0.139 | p=0.040 |
| kap_alpha (α 곡률) | 9.412 | 8.177 | 7.708 | n.s.(p=0.14) |
| lag 크기 · α_c | — | — | — | n.s. |

→ **방향이 method 만장일치로 잡히는 loci = 전사속도·발현량이 압도적으로 높은 유전자**(α 2.85 vs RNA-first 0.22).

## ⚠️ 양면 해석 — 현 데이터로 분리 불가 (정직)
1. **생물학적 읽기**: 고발현 말단 effector loci(과립 단백질 등)는 chromatin priming의 교과서적 대상 — 원 방법 논문들이 예시로 든 유전자와 같은 결.
2. **방법론적 읽기(경합 설명)**: 신호가 강한 유전자에서만 방향을 **해상**할 수 있어 method가 일치하는 것일 수 있음(**SNR 아티팩트**). FINDINGS §8(lag은 low-SNR + sloppy)과 부합.
- 두 설명은 현 데이터로 **분리되지 않는다**. 어느 쪽이든 실용 결론은 동일.

## 논문 반영 (supporting, 헤드라인 아님) — 신뢰 지도에 실행 규칙 추가
> "lag **방향**은 최상위 발현 effector loci(부호 가변 method 판정 가능 유전자의 ~13%)에서만 method 간 만장일치이고, 61%는 method가 갈린다. 이것이 그 loci의 진짜 chromatin priming 때문인지 단지 신호가 강해서인지는 현 데이터로 분리할 수 없다."
- 가치: **"어디서는 방향을 써도 되나"**를 알려주는 실행 규칙 → 결정지도(Table 2)에 조건부 행으로 얹을 수 있음.
- 금지: 이를 "chromatin priming이 effector loci에서 입증됐다"로 승격하지 말 것(SNR 경합 설명 미배제 + marker 인과 대조 NULL, MW p=0.58).
