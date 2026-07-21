# P3 — Cell-cycle confound (gene-level, refit 없이)

## 1. fit lag gene 중 cell-cycle gene
- fit lag gene n=538 중 cell-cycle gene **10개 (1.9%)**
- cell-cycle gene lag: n=10, median 6.80
- 나머지 gene lag: n=528, median 5.83
- Mann-Whitney(cell-cycle lag vs 나머지) p=0.862 → 유의차 없음 ✓

## 2. cell-cycle gene 제외 시 lag 분포 변화
- 전체:        median 5.87, IQR [3.03, 9.00]
- CC 제외:     median 5.83, IQR [3.00, 9.08]
- median 변화 0.037 pseudotime → 작음(결론 안정) ✓

## 3. cell-cycle score vs trajectory 구조 (진짜 confound 여부)
- pseudotime obs 없음 → trajectory 얽힘 검정 생략 (P3 pseudotime 산출 후)
- lineage별 cycling(S+G2M) 비율: MK 88%, Myeloid 79%, Erythroid 79%, Baso/Eo/Mast 44%, Lymphoid 16%, HSC/MPP 3%

## 결정
- regressed refit 필요? **아니오 — cell-cycle는 lag 결론에 비편향(sensitivity로만 보고)**
  - 근거: cell-cycle gene 비율 1.9%, lag 차이 검정 p=0.862, CC제외 median 변화 0.037.
- (full regressed refit = p2_multivelo.py --regress-cellcycle, ~수 h)