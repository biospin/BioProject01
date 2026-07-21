# marker-shuffle "teeth" 검정 — 셔플이 명명 priming marker lag을 bulk보다 더 흔드나?

> make-or-break #1 (2026-07-18). 목적: 인과 음성대조(ATAC shuffle)의 유일 novelty 주장을 방어 —
> "chromatin이 실제 기여하는 명명 marker loci에서는 셔플이 lag을 흔든다"를 검정. 양방향 판별.
> 스크립트: 인라인(results/multivelo_genes.csv 원본 vs results/scrambled_genes.csv 셔플, lag=sw2−sw1).

## 결과 (공유 538 gene)
- **bulk 보존 확인**: 원본 vs 셔플 lag Spearman **ρ=+0.721** (논문 0.72 재현) — 전역 lag은 셔플에 거의 안 변함(=lag은 model-structural)이라는 핵심 음성 결과는 견고.
- **명명 marker(6개, S100A9는 fit set 부재)**: 절대 |Δlag|로는 3개(CSF1R 79.7%ile·ELANE 89.6%·IRF8 82.2%)가 크게 움직이나, **|Δlag|는 lag 크기와 상관(ρ=+0.24)** — 고lag 유전자가 원래 더 흔들리는 편향.
- **편향 보정(상대 변화 |Δlag|/|lag_o|)**: 마커 median **0.137 ≈ bulk 0.144**, **Mann-Whitney(marker>bulk) p=0.58**(오히려 마커가 약간 작음). IRF8만 상대 93%ile로 견고, CSF1R은 60%ile로 하락.

| marker | 절대 |Δ|%ile | 상대Δ %ile |
|---|---|---|---|
| CSF1R | 79.7% | 59.9% |
| ELANE | 89.6% | 77.1% |
| IRF8 | 82.2% | **93.1%** |
| GATA2 | 44.1% | 35.9% |
| MPO | 8.0% | 5.0% |
| HLF | 11.7% | 14.9% |

## 판정 (정직)
**이빨 없음(no teeth).** 공정한 상대-변화 기준으로 셔플은 명명 priming marker의 lag을 **bulk보다 더 흔들지 않는다**(p=0.58). 절대값으로 커 보인 건 lag 크기 편향. → **"named marker는 chromatin이 인과적으로 lag을 만든다(Medium-High)"는 주장은 인과 대조로 지지되지 않는다.**

## 함의
- 핵심 음성 결론("lag은 chromatin이 아니라 모델 구조")은 **오히려 더 깨끗해짐** — 명명 marker에서도 chromatin이 lag을 인과적으로 안 만든다. marker의 method 간 *방향* 일치는 상관적 사실이지 인과가 아님.
- 그러나 draft의 "chromatin priming은 특정 loci에선 실재"(L127)·Table2 "marker Medium-High"의 **인과적 함의는 하향해야 정직**하다(방향 일치=상관으로 재서술).
- 적대적 심사자의 R-4("셔플이 underpowered 아니냐")를 이 테스트로는 **반박 못 함** — 인과 novelty의 방어 컨트롤은 여전히 비어 있음.
- 한계: n=6(S100A9 부재), 단일 셔플(per-marker null 분포 없음). 더 큰 canonical set + 다중 셔플이면 검정력↑이나, 현 신호는 "선택적 marker 교란 없음"으로 명확.
