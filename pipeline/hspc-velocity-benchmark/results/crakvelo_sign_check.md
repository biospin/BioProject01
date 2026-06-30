# CRAK-Velo lag sign convention 검증 (2026-07-01)

> 블로커: 자율 finisher가 산출한 `crakvelo_genes.csv`의 lag **부호 convention 미검증**
> (finisher 로그상 marker CSF1R = −12, "Myeloid=양수 기대"와 반대처럼 보임).
> → 검증 결과 **`p2_crakvelo_lag.dtw_lag`의 부호가 docstring과 반대로 구현돼 있었음**(버그). 수정·재산출 완료.

## 1. 검증 방법 — 합성 신호 + 참조 구현 (`scripts/p3_crakvelo_sign_check.py`)

chromatin이 spliced보다 **명백히 선행**하는 switch 신호를 만들어 각 구현이 돌려주는 부호를 직접 측정.

| 구현 | chromatin-leading 입력 → lag | docstring("양수=chromatin선행") |
|---|---|---|
| MoFlow `eval_dtw.get_dtw` (`fastdtw`, `time[j]−time[i]`) | **+30** (양수) | ✓ 일치 |
| CRAK-Velo `dtw_lag` (manual DP, `j−i`) — **수정 전** | **−72** (음수) | ✗ **반전** |
| CRAK-Velo `dtw_lag` (`i−j`) — **수정 후** | **+8** (양수) | ✓ 일치 |

- 두 구현은 **같은 공식**(spliced index − chromatin index)을 쓰지만, manual DP backtrack의 path 방향이 `fastdtw`와 반대라 부호가 뒤집혔다.
- tie-break 순서를 바꿔도 부호 불변(−72 고정) → tie-break 산물 아님, **구현 고유의 방향 차이**.
- 정수-지연 복사 등 monotone 신호에서는 DTW lag이 ~0 (ill-posed)이라, two-center switch 신호로 판정.

## 2. 수정

`scripts/p2_crakvelo_lag.py::dtw_lag` — `offs.append(j - i)` → **`offs.append(i - j)`** (MoFlow와 부호 통일).
단위검증 PASS: chromatin선행 → +8, spliced선행 → −8, 동시 → 0. csv 재산출(868 gene).

## 3. 생물학적 검증 — marker (Myeloid = chromatin priming = 양수 기대)

| gene | CRAK-Velo(수정후) | MoFlow | 해석 |
|---|---|---|---|
| CSF1R | **+12.0** | −0.0 | crak: chromatin선행 ✓ |
| S100A9 | **+23.5** | — | chromatin선행 ✓ |
| AZU1/ELANE/MPO/PRTN3/CTSG | — (velocity subset 밖) | +0.4/+0.2/+0.1/+0.4/+0.3 | moflow 전부 (약)양수 ✓ |

→ **두 method 모두 canonical myeloid priming marker를 chromatin-leading(양수) 쪽에 둔다.** 수정된 부호가 생물학적으로 옳음. finisher의 "CSF1R=−12 반대" 경보는 **부호 버그가 원인**이었고 해소됨.

## 4. 부호 수정이 cross-method 일치도에 미친 영향 (concordance.md §3.5)

부호를 뒤집으면 crakvelo의 signed lag이 부호 반전 → rank-corr·sign-agreement도 반전:

| pair | 수정 전 | 수정 후(올바름) |
|---|---|---|
| moflow×crakvelo | rho +0.151, sign-agree 43.6% | **rho −0.151 (p=0.006), sign-agree 32.4%** |
| crakvelo×multivelovae | rho +0.040 | **rho −0.040 (p=0.47)** |

⚠️ **해석 주의**: 부호가 올바르게 통일된 뒤 genome-wide rank-corr이 **약한 음(−0.15)**, sign-agreement는 chance 이하다. 즉 **canonical priming marker에서는 두 method가 방향 일치하지만, 전장 유전자 수준에서는 lag 방향이 서로 갈린다.**
- |rho|=0.15로 magnitude도 약함 + lag 단위 비가역(crak=bin-index N_BIN=100, moflow=pseudotime-scaled) → magnitude는 직접 비교 불가, **rank/sign만**.
- → H1 핵심("lag은 method-민감, 강건한 건 construct-validity marker뿐")을 **강화**. CRAK-Velo는 MultiVelo의 구조적 100% chromatin-leads와 달리 ~41/43 **균형**(전역 priming 데이터 미지지)을 보임.

## 5. FINDINGS 반영 가능 여부

✅ **블로커 해소.** 부호 검증·수정·marker 검증 완료. canonical 4-way 결론에 다음을 반영 가능:
1. CRAK-Velo lag 부호는 이제 MoFlow와 통일(양수=chromatin선행), 단위검증·marker 검증됨.
2. 4-way lag 방향 일치도는 약함(|rho|≤0.15, sign≈chance) — marker 외 genome-wide는 method-divergent.
3. 단정 금지: cross-method magnitude 비교(단위 상이), 약한 음의 rank-corr의 생물학적 실재성(artifact 가능성, 단위/binning 차이).
