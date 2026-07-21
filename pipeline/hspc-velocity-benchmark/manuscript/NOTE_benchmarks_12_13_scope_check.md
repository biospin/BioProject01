# 선결 게이트 해소 — 벤치마크 [12,13]은 어느 층을 채점했나

> 2026-07-19. `results/velocity_matrix_audit.md` §7이 건 게이트: **[12,13]이 층②(세포×유전자 행렬)를 봤는지 층③(임베딩 화살표)을 봤는지 확인 전에는 draft를 못 고친다.**
> 두 논문 전문 PDF를 받아 metric 정의·결과를 직접 읽고 확인했다(추정 아님). 원문 = bioRxiv `2025.08.02.668272`, `10.64898/2026.01.03.697314`.

## 확정된 서지 (draft의 `<FILL>` 해소)

- **[12]** Luo Y, Ren J, Yang Q, You Z, Zhou Y, Qin Q, Li Q. *Benchmarking RNA velocity methods across 17 independent studies.* **Cell Reports Methods 6(4), 101367 (2026)**. doi:**10.1016/j.crmeth.2026.101367** (PII S2667-2375(26)00067-6 — draft에 있던 PII와 일치). 프리프린트 bioRxiv 2025.08.02.668272. CrossRef 실조회.
- **[13]** Huang K, Zhou Y, Wang T, Li X, Zhao X, Liu X, Huang L, Zhou X, Liu J. *Benchmarking algorithms for RNA velocity inference.* **bioRxiv 2026.01.03.697314 (2026)**, doi:10.64898/2026.01.03.697314. (Kexin Huang·Yu Zhou·Tiangang Wang 공동 1저자; 교신 Jiajia Liu·Xiaobo Zhou, UTHealth Houston / Xidian Univ.) 미심사 프리프린트.

## [12] — 14 method × 17 dataset, **전부 RNA-only**

| 항목 | 내용 |
|---|---|
| 채점 층 | **③ 임베딩/이웃그래프**. CBDir는 정의식이 명시적으로 *low-dimensional space*의 위치·변위를 쓴다. ICCoh·velocity consistency도 이웃 세포 간 코사인. |
| method 간 비교 | **있다** — method agreement **A1**(두 method의 *cell transition vector* 코사인)·**A2**(각 method vs 전 method의 median transition vector). |
| 비교 대상 | **transition vector**(전이 벡터)이지 원 세포×유전자 velocity 행렬이 아니다. |
| 결과 | **A1 < 0.3 (12개 method 전부)** — "substantial discrepancies in RNA velocity estimations among these methods". A2 > 0.5는 4개뿐. 초기 분화 세포에서 높고 성숙 세포형에서 평균 **64% 하락**. 결론 권고 = "여러 method 결과를 통합하라". |
| 크로마틴 | **없다.** 이들 데이터셋에 ATAC이 없어 **MultiVelo를 `rna_only=True`로 실행**했다. 즉 multiome velocity는 평가되지 않았다. |

## [13] — 29 method × 176 dataset(114 시뮬 + 62 실측), 4축(정확도·확장성·안정성·사용성)

| 항목 | 내용 |
|---|---|
| 채점 층 | **③ 임베딩/벡터**. ground-truth correlation(시뮬만)·velocity angle consistency·CBDir·ICCoh·consistency score + 군집 기하 지표. |
| 층② 사용처 | **있다 — 단 method *내부* 재실행 안정성에만.** 딥러닝 method를 seed 5개로 재실행해 `V(cells × genes)` 행렬의 세포별 코사인 평균으로 run-to-run 일치를 쟀다. **method 간 행렬 비교는 없다.** |
| multiome | **1개 데이터셋(mouse embryonic multi-omics)에서 MultiVelo vs scKINETICS 2종만.** 임베딩 지표(CBDir·ICCoh·consistency·군집거리)로 비교. MultiVelo가 CBDir 분포가 더 아래로 퍼져 "국소적으로 기대 전이 방향과 어긋나는 경우가 더 잦다"고 보고. |
| 크로마틴 인과 | **없다**(ATAC 셔플 등 음성대조 없음). |

## 판정 — 게이트 통과, **중복 아님 · 모순 아님 · 오히려 보강**

1. **우리가 한 층② cross-method 행렬 비교는 두 벤치마크 어디에도 없다.** [12]는 method 간 비교를 하지만 대상이 임베딩 transition vector이고, [13]은 행렬을 쓰지만 같은 method의 seed 재실행에만 쓴다.
2. **모순 걱정은 해소됐다.** 우려했던 시나리오(그들이 임베딩에서 "잘 맞는다"고 했는데 우리는 행렬에서 "안 맞는다"고 하면 평활로 설명해야 함)는 발생하지 않았다. [12]는 임베딩 수준에서도 **A1<0.3으로 일치가 낮다**고 보고한다. **두 층에서 같은 방향**이다 → 우리 결과는 독립 corroboration.
3. **우리만 가진 것 3가지**: (a) **원 세포×유전자 행렬 수준의 method 간 비교**, (b) **ATAC-shuffle 인과 음성대조**(둘 다 없음), (c) **재적합 재현성 천장을 대조 기준자로 사용**([13]은 seed 안정성을 method 품질 지표로 쓸 뿐, cross-method 일치의 해석 기준으로 쓰지 않는다).
4. **크로마틴 velocity의 공백이 확인됐다.** [12]는 ATAC이 아예 없었고(MultiVelo를 rna_only로 실행), [13]은 multiome을 1개 데이터셋·2개 method·임베딩 지표로만 봤다. **paired multiome velocity를 다중 method·인과대조로 감사한 것은 우리가 처음**이라고 말할 근거가 있다.
5. **[13]의 MultiVelo CBDir 관찰과 우리 결과는 같은 쪽을 가리킨다** — 그들은 임베딩에서 MultiVelo의 국소 방향 불일치가 잦다고 봤고, 우리는 행렬 수준에서 method 간 방향이 우연 수준임을 봤다.

## draft 반영 (영/한 동시)

- Background/Positioning의 "both score the velocity *vector*, not the individual per-gene outputs" → **여전히 맞다**. 다만 "우리는 세포 수준을 안 봤다"는 유보는 이제 **"행렬(②)은 감사했고 같은 결론이었다, 임베딩 화살표(③)는 범위 밖"**으로 정밀해진다.
- 서지 `<FILL>` 2건 해소(위 확정 서지로 교체).
- 편입 분량: Results supporting 한 문단 + Additional file. **헤드라인 승격 없음.**
