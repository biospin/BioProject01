# Proxy-join §2 GATE 결과 — gene-intrinsic t½ 보존성 (BIOP01-27)

실행 2026-07-03. 스크립트 `scripts/pj_gene_intrinsic_gate.py` (env `scv-preprocess`).
질문: **Todorovski K562(leukemia) mRNA 반감기 t½를 우리 HSPC lag 분석으로 차용(borrow)해도 되는가?**
판정법: reference(K562) vs 비교 세포주 t½의 gene-wise **Spearman ρ**(log t½ rank 보존). 임계 ρ≥0.50 PASS / 0.30–0.50 CONDITIONAL / <0.30 FAIL.
데이터 원천·정규화·다운로드 URL = `data/PROVENANCE_halflife.md`.

## 판정: **PASS** (median ρ = 0.74)

원자료: `proxy_join/out_gate/gate_report.json`, 플롯 `proxy_join/out_gate/gate_*.png`.
reference = Todorovski **K562_UT** 6,579 gene.

| 비교셋 | 성격 | n(overlap) | **전역 ρ** | HK ρ | **non-HK ρ** | top10% Jaccard |
|---|---|---:|---:|---:|---:|---:|
| THP-1 (Todorovski) | 조혈, **same-study(상한)** | 4,750 | 0.743 | 0.773 | 0.700 | 0.457 |
| **MOLM-13 (RNADecayCafe)** | 조혈 AML, **cross-study(★주지표)** | 6,061 | **0.695** | 0.727 | **0.659** | 0.287 |
| HEK293T (RNADecayCafe) | 비조혈, cross-study 하한 | 6,337 | 0.750 | 0.771 | 0.723 | 0.396 |
| — median (스크립트 verdict) | | | **0.74** | | | |

**앵커** (gate median 미포함, 해석용): K562(Todorovski) vs K562(RNADecayCafe = Ietswaart/Muhar/Schofield labs, **Todorovski 아님 — 확인**) = cross-lab **same-cell-type** ρ = **0.749** (n=6,404). → cross-study 기술적 상한. (MOLM-13도 Muhar 2018 유래로 Todorovski와 독립 — 확인.)

## 해석 (median 하나로 읽지 말 것 — 소스별 분리 보고)

- **주 gate 지표 = cross-study 조혈계(MOLM-13) ρ = 0.695**, non-HK ρ = 0.659. THP-1(same-study, 0.743)은 **낙관적 상한**(같은 lab·SLAM-seq·24h cap → 기술 covariance 공유)이므로 headline로 쓰지 않는다. cross-study 숫자가 답이다.
- **핵심**: cross-lab same-cell-type 상한(0.749)과 cross-study **다른** 조혈 세포주(MOLM-13 0.695) 차이가 ~0.05뿐. 즉 **cell-type을 바꿔도 rank 보존이 cross-lab 기술노이즈 수준 이상 거의 안 떨어진다** → t½는 강하게 **gene-intrinsic**. (Agarwal & Kelley 2022가 경고한 cross-dataset 기술노이즈가 상한을 눌러도, 그 상한 근처까지 보존.)
- **차용 위험이 실제 사는 곳 = non-HK gene**: HK는 어디서나 보존(0.72–0.77)되므로 자명. non-HK에서도 세 비교 모두 **0.659–0.723**로 임계 0.50을 여유 있게 상회 → cell-type-specific gene의 t½ 차용도 (보수적으로) 정당.
- 세 소스 전부(same-study·cross-study 조혈·cross-study 비조혈) PASS → 판정은 THP-1 같은 한 소스에 의존하지 않는다(robust PASS).

## 한계 / 후속 (PASS이되 무조건 아님)

1. **24h 우측 검열**: Todorovski K562의 8.1% gene이 24.0h에 상한(진짜 t½ 아님). Spearman은 견디나, 반감기 최상위 decile의 절대값·Jaccard(top10% 0.29–0.46로 중간)는 이 검열로 약화. → §4 모델에서 t½를 연속 예측변수로 쓸 때 상한 gene은 별도 처리 or censored 인지.
2. **여전히 HSPC 직접 t½는 아님**: 가장 가까운 게 AML 세포주(MOLM-13). CD34+ primary HSPC t½ 공개데이터 부재 → gene-intrinsic 가정으로 방어(본 gate) + §4에서 cell-type 차를 잔차/공변량으로 흡수(PROXY-JOIN-DESIGN §2.3, §4).
3. **결론 형태**: PASS = "t½ 차용 정당, 한계 명시"(스크립트 verdict). timing 예측 아님 — reframe(magnitude outcome, decay 통제 후 lag incremental) 준수.

## 재현
```
conda run -n scv-preprocess python scripts/pj_gene_intrinsic_gate.py
```
입력 CSV 5종 + housekeeping.txt = `data/` (provenance: `data/PROVENANCE_halflife.md`). data/ 는 .gitignore.
