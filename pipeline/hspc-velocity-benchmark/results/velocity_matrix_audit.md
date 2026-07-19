# 층② 세포×유전자 velocity 행렬 감사 (BIOP01-59)

> 2026-07-19. 사전등록 = `manuscript/PREREGISTRATION_velocity_matrix.md`(실행 전 봉인).
> 실행 = `scripts/p10_velocity_matrix_audit.py`(주 판정) + `scripts/p10b_velocity_matrix_diagnostic.py`(사후 진단).
> 데이터 = HSPC 10x Multiome **21,878 cells 전량**, 5개 arm 공유 505 gene → 사전등록 제외규칙 적용 후 **354 gene**
> (scVelo가 dynamics를 복원하지 못해 NaN으로 남긴 151개 제외. 다른 arm의 NaN·분산0 제외는 0개).
> 비교 layer는 spliced velocity로 통일(MultiVelo `velo_s`·MoFlow `velo_s`·CRAK-Velo `velocity`·MultiVeloVAE `vae_velocity`·scVelo `velocity`). chromatin velocity는 섞지 않았다.

---

## 0. 한 줄

**세포 수준 velocity 행렬은 method 사이에서 재현되지 않는다.** 같은 method를 재적합하면 잘 재현되는데(중심화 코사인 +0.87), 서로 다른 multiome method 사이에서는 0 또는 음수다. MultiVelo에서는 **크로마틴을 통째로 셔플해도 재적합 잡음만큼밖에 안 움직인다**(+0.838, 재적합 천장 95% 범위 안). 그나마 실질적인 method 간 일치는 크로마틴을 안 쓰는 **RNA-only 기준선과의 쌍**에서 나오지만, 이것도 **MultiVelo에서만 뚜렷하고**(+0.583) multiome 계열 전체의 성질은 아니다.

## 1. 판정 — **NEGATIVE** (사전등록 §5)

| 대조 | 사전 조건 | 실측 | 판정 |
|---|---|---|---|
| **A. 기준선** | multiome↔multiome 코사인 > multiome↔RNA-only (95% CI 비중첩) | **−0.139** [−0.140, −0.138] vs **+0.080** [+0.078, +0.081], paired Δ **−0.206** [−0.207, −0.205] | ❌ **반대 방향** |
| **B. 인과** | ATAC-shuffle이 행렬을 무너뜨린다 | MultiVelo 원본×셔플 **+0.732** ≫ 다른 어떤 method와의 일치(−0.41 ~ +0.05) | ❌ 안 무너진다 |

두 대조 모두 실패 → **층①의 결론이 층②로 확장된다.** 사후 구제 없음.

## 2. 쌍별 세포 수준 코사인 (세포마다 1개, 중앙값)

`null` = 세포 짝 셔플(method A의 세포 i vs method B의 무작위 세포 j). 모든 velocity가 전역적으로 비슷한 방향을 향하면 짝이 맞든 안 맞든 코사인이 높으므로, **null 대비 초과분만이 세포 수준 일치**다.

| 쌍 | 종류 | raw | null | **초과** | SD 스케일 | 부호 일치 |
|---|---|---|---|---|---|---|
| MultiVelo × MoFlow | MM | −0.000 | +0.012 | −0.012 | +0.024 | 49.7% |
| MultiVelo × CRAK-Velo | MM | +0.047 | +0.124 | −0.077 | −0.038 | 50.1% |
| MultiVelo × MultiVeloVAE | MM | −0.408 | −0.145 | −0.263 | +0.127 | 56.4% |
| MoFlow × CRAK-Velo | MM | −0.000 | −0.003 | +0.003 | −0.021 | 53.8% |
| MoFlow × MultiVeloVAE | MM | −0.015 | −0.018 | +0.003 | +0.005 | 51.5% |
| CRAK-Velo × MultiVeloVAE | MM | −0.411 | −0.410 | −0.001 | +0.020 | 58.3% |
| **MultiVelo × scVelo(RNA)** | M-RNA | +0.242 | −0.078 | **+0.320** | **+0.406** | 63.5% |
| MoFlow × scVelo(RNA) | M-RNA | −0.010 | −0.007 | −0.003 | −0.000 | 51.6% |
| CRAK-Velo × scVelo(RNA) | M-RNA | −0.169 | −0.190 | +0.020 | +0.043 | 62.1% |
| **MultiVeloVAE × scVelo(RNA)** | M-RNA | +0.271 | +0.217 | +0.055 | **+0.420** | 64.3% |

**multiome method 6쌍 중 어느 쌍도 null을 의미 있게 넘지 못한다.** 초과분이 가장 큰 두 쌍은 둘 다 **RNA-only 기준선과의 쌍**이다. (cell,gene) 부호 일치율도 multiome끼리는 49.7~58.3%로 동전 던지기 언저리이고, RNA-only와의 쌍(62~64%)이 더 높다.

## 3. 사후 진단 — 큰 음수 코사인은 어디서 오나

주 판정은 위에서 끝났다. 아래는 −0.41 같은 값의 **구조를 분해**한 것이지 판정을 바꾸지 않는다.

각 method의 velocity 행렬은 *세포 공통 평균 벡터* + *세포별 편차*로 나뉜다. 평균 벡터가 차지하는 비중(‖mean‖²/평균 ‖row‖²)은 MultiVelo 12.9% · MoFlow 37.4% · CRAK-Velo 36.4% · MultiVeloVAE 28.8% · scVelo 18.9%. 즉 원척도 코사인은 **"모든 세포에 공통인 방향"에 상당히 지배**되고, 두 method의 평균 벡터가 반대로 정렬돼 있으면(MultiVelo×VAE −0.680, CRAK×VAE −0.533) 세포별 정보와 무관하게 큰 음수가 나온다.

평균을 제거한 **중심화 코사인**(세포별 편차만의 일치):

| 쌍 | raw → centered |
|---|---|
| MultiVelo × MoFlow | −0.000 → **−0.012** |
| MultiVelo × CRAK-Velo | +0.047 → +0.131 |
| MultiVelo × MultiVeloVAE | −0.408 → **−0.500** |
| MoFlow × CRAK-Velo | −0.000 → **+0.002** |
| MoFlow × MultiVeloVAE | −0.015 → **+0.002** |
| CRAK-Velo × MultiVeloVAE | −0.411 → **−0.530** |
| **MultiVelo × scVelo(RNA)** | +0.242 → **+0.583** |
| MoFlow × scVelo(RNA) | −0.010 → −0.004 |
| CRAK-Velo × scVelo(RNA) | −0.169 → +0.260 |
| MultiVeloVAE × scVelo(RNA) | +0.271 → **−0.292** |

중심화해도 결론은 같고 오히려 선명해진다. **전체 행렬에서 가장 강한 일치는 MultiVelo와 RNA-only scVelo 사이(+0.583)이며, multiome method끼리는 0 또는 뚜렷한 음수다.** MultiVelo와 MultiVeloVAE는 같은 세포에 대해 **체계적으로 반대 방향**의 velocity를 준다(−0.500).

**단, RNA-only와의 일치도 계열 전체의 성질이 아니다.** 중심화 M-RNA 열을 그대로 읽으면 MultiVelo +0.583 · CRAK-Velo +0.260 · MoFlow −0.004 · MultiVeloVAE −0.292로, 4개 중 2개는 RNA 기준선과도 세포 수준에서 아무것도 공유하지 않는다. 특히 MultiVeloVAE×scVelo는 raw +0.271이 중심화하면 −0.292로 **부호가 뒤집힌다** — 원척도의 양수가 전적으로 평균 벡터 정렬이었다는 뜻이다. 같은 쌍의 부호 일치율 64.3%도 세포 수준 일치가 아니라 **유전자별 평균 부호의 공유**를 재고 있다. 두 지표가 갈라지는 곳에서는 교집합만 주장한다(§5).

## 4. ★ 측정이 무딘 게 아니다 — 재현성 천장

"cross-method 일치가 0"이 지표가 잡음이라서인지 진짜 불일치인지 구분하려면 천장이 필요하다. MultiVelo를 세포 재표본(15,315 cells)으로 **재적합한 bootstrap refit 6개**와 원본을 같은 자로 비교했다.

| 비교 | 중심화 코사인 | 부호 일치 |
|---|---|---|
| **같은 method, 재적합** (재현성 천장) | **+0.872** (범위 0.826~0.887) | 78.6% |
| **같은 method, ATAC 셔플**(크로마틴 파괴) | **+0.838** | 78.9% |
| 서로 다른 multiome method | −0.530 ~ +0.131 | 49.7~58.3% |
| multiome × RNA-only(최고) | +0.583 | 63.5% |

**크로마틴을 통째로 셔플해도 재적합 잡음만큼밖에 안 움직인다**(+0.838 vs 천장 +0.872). 지표는 일치를 잡아낼 수 있다 — 같은 method 안에서는 0.87을 준다. 그러니 method 간 0은 측정 한계가 아니라 **실제 불일치**다.

## 5. 이게 뜻하는 것 — 지표가 전부 동의하는 교집합만

세 지표(중심화 코사인·null 대비 초과·부호 일치율)가 **모두** 지지하는 진술만 남긴다. 하나만 깨끗한 읽기는 쓰지 않는다.

1. **같은 method는 재현되지만, 서로 다른 multiome method는 세포 수준에서 우연 수준으로 일치한다.** 천장 +0.872 대 method 간 중심화 코사인 −0.530~+0.131, 부호 일치 49.7~58.3%. 층①(모수)의 결론이 층②(행렬)로 그대로 확장된다.
2. **크로마틴은 velocity 행렬에 인과적으로 무력하다 — 단 MultiVelo에 한정.** ATAC를 셔플해도 재적합 잡음 범위 안에서만 움직인다(+0.838 vs 천장 +0.872). MoFlow는 재실행 대조가 없어 인과 주장에서 제외한다(§6).
3. **method를 넘어 남는 일치는 RNA-only 기준선과의 것이지만, 계열 전체의 성질이 아니라 MultiVelo에서 가장 뚜렷하다**(+0.583; CRAK +0.260, MoFlow −0.004, VAE −0.292). "multiome velocity의 재현되는 부분은 RNA 쪽"이라는 일반 명제는 이 데이터로는 **MultiVelo 사례까지만** 지지된다.
4. **실행 규칙**: 세포 수준 velocity 화살표를 결론의 근거로 쓸 거라면 **method를 하나 더 돌려 같은 화살표가 나오는지 먼저 확인**해야 한다. 특히 MultiVelo와 MultiVeloVAE를 바꿔 끼우면 같은 세포에서 반대 방향이 나올 수 있다.

## 6. 한계 (정직하게)

- **MoFlow의 ATAC-shuffle 대조는 해석 불가.** MoFlow 원본×셔플 중심화 코사인은 +0.113으로 낮지만, MoFlow는 확률적 심층모형이고 **같은 설정 재실행 대조가 없다**. 이 값이 크로마틴 효과인지 학습 run-to-run 변동인지 분리할 수 없다. 인과 결론은 재적합 천장을 가진 **MultiVelo에서만** 주장한다.
- **공유 354 gene 위에서 잰 값**이다. 실제 논문들이 그리는 화살표는 각 method가 자기 유전자 집합 전체로 그린다. 유전자 집합이 다르면 화살표도 달라질 수 있고, 그 차이는 여기서 측정되지 않았다.
- **층③(임베딩 화살표)은 아직 안 봤다.** 행렬이 불일치해도 임베딩 투영이 이웃 그래프로 평활되면서 겉보기 궤적은 비슷해질 수 있다. 층③은 별도 측정이 필요하다(2026 벤치마크 [12,13]의 소관과 겹치는지 먼저 확인할 것).
- **HSPC 단일 시스템.** 외부 재현 없음.
- 코사인에서는 정확히 0인 항목을 그대로 두었고(내적 0·norm 기여 0), 부호 일치율에서만 "방향 미정"으로 제외했다(사전등록 2-3, `CORRECTION_sign_agreement_zero_handling.md`와 같은 규약). 이 비대칭은 의도된 것이다.
- MultiVelo↔MultiVeloVAE의 체계적 반대 정렬이 **진짜 불일치인지 문서화되지 않은 부호·모수화 규약 차이인지**는 이 감사로 구분되지 않는다. 어느 쪽이든 두 출력을 확인 없이 섞어 쓰는 사용자는 반대 궤적을 얻는다.

## 7. 논문 편입 (사전등록 §6대로 별도 판단)

- 현 draft의 **동결된 주장 5개는 이 결과로 자동 수정하지 않는다.**
- 결과가 NEGATIVE이므로 Discussion의 scope 문장(주장 #4)은 **그대로 유지**된다. 다만 "우리는 세포 수준 벡터를 감사하지 않았다"에서 **"행렬(층②)은 감사했고 같은 결론이었다 / 임베딩(층③)은 여전히 범위 밖"**으로 정밀해질 수 있다.
- **⛔ 선결 게이트: 2026 벤치마크 [12,13]이 층②(행렬)를 채점했는지 층③(임베딩)을 채점했는지 확인하기 전에는 draft_v2를 건드리지 않는다.** ③를 봤고 일치를 보고했다면 우리의 ② 불일치는 모순이 아니라 이웃 그래프 평활로 설명되는 관계이고(§6 한계 3), ②를 봤고 같은 결론이었다면 우리는 corroboration이다. 어느 쪽인지 모르고는 Discussion 문장을 옳게 쓸 수 없다.
- 편입한다면 **supporting 한 문단 + Additional file**, 헤드라인 승격은 하지 않는다. 이 결과는 동결된 헤드라인을 **확장**할 뿐 새 헤드라인을 열지 않는다.

## 산출물
`results/velocity_matrix_audit.json` · `results/velocity_matrix_audit_pairs.csv` · `scripts/p10_velocity_matrix_audit.py` · `scripts/p10b_velocity_matrix_diagnostic.py`
