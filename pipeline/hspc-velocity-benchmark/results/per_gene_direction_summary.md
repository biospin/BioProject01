# 유전자 × method 방향(chromatin-leading vs RNA-first) 일치도 — Supplementary 재료

> `scripts/p8_per_gene_direction_table.py`. 부호 가변 3 method(MoFlow·CRAK-Velo·MultiVeloVAE rate-proxy)의 유전자별 방향과 합의 여부.
> MultiVelo lag(sw2−sw1)은 switch-time 단조정렬로 **구조적 양수 = 방향 무정보**라 판정에서 제외(값만 병기).
> 전체 표: `results/per_gene_direction_by_method.csv` (n=1175 genes).

## 합의 분포 (부호 가변 method ≥2개 있는 유전자)

| 합의 | 유전자 수 | 비율 |
|---|---|---|
| unanimous_chromatin | 83 | 13.0% |
| unanimous_RNA | 164 | 25.6% |
| split | 393 | 61.4% |
| **계** | 640 | 100% |

**만장일치(방향 일치) = 247/640 (38.6%)**, 나머지는 method 간 방향이 갈린다.

## pairwise sign-agreement (chance=50%)

| 쌍 | 일치율 | n |
|---|---|---|
| moflow × crak | 44.2% | 330 |
| moflow × vae_proxy | 55.0% | 636 |
| crak × vae_proxy | 44.0% | 334 |

## canonical marker (계통 생물학 대조)

| gene | 계통 | MoFlow | CRAK | VAE-proxy | 합의 |
|---|---|---|---|---|---|
| ELANE | myeloid | chromatin | — | chromatin | unanimous_chromatin |
| AZU1 | myeloid | chromatin | — | chromatin | unanimous_chromatin |
| MPO | myeloid | chromatin | — | chromatin | unanimous_chromatin |
| LYZ | myeloid | chromatin | — | chromatin | unanimous_chromatin |
| CSF1R | myeloid | RNA | chromatin | chromatin | split |
| S100A9 | myeloid | — | chromatin | chromatin | unanimous_chromatin |
| HLF | HSC | RNA | RNA | chromatin | split |
| CRHBP | HSC | RNA | chromatin | RNA | split |
| MEIS1 | HSC | RNA | — | RNA | unanimous_RNA |
| IRF8 | pDC | RNA | RNA | chromatin | split |
| TCF4 | pDC | RNA | chromatin | chromatin | split |
| GATA2 | prog | chromatin | chromatin | chromatin | unanimous_chromatin |
| CPA3 | mast | RNA | chromatin | chromatin | split |
| ITGA2B | MK | chromatin | chromatin | chromatin | unanimous_chromatin |
| VWF | MK | chromatin | RNA | chromatin | split |
| TFRC | ery | chromatin | — | chromatin | unanimous_chromatin |

## 읽는 법 (정직)
- **만장일치 비율이 낮고 split이 많다 = per-gene 방향이 method에 따라 갈린다** → '이 유전자는 chromatin-leading'을 신뢰성 있게 말할 수 없다(BIOP01-55 결론).
- 다만 **계통 수준 aggregate**(myeloid priming vs HSC)에서는 세 method 모두 같은 방향 경향을 보인다 — 거친 구조는 재현되나 유전자 단위는 아니다.
- MultiVelo 값은 방향 판정에 쓰지 않는다(구조적 양수).
