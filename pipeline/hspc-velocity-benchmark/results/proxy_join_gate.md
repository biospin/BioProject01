# Proxy-join §2 GATE 결과 — gene-intrinsic t½ 보존성 (BIOP01-27)

실행일은 2026-07-03이다. 스크립트는 `scripts/pj_gene_intrinsic_gate.py`(env `scv-preprocess`)이다.
질문: **Todorovski K562(leukemia) mRNA 반감기 t½를 우리 HSPC lag 분석으로 차용(borrow)해도 되는가?**
판정법: reference(K562)와 비교 세포주 t½의 gene-wise **Spearman ρ**(log t½ rank 보존)를 본다. 임계 ρ≥0.50 PASS / 0.30–0.50 CONDITIONAL / <0.30 FAIL.
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
- **핵심**: cross-lab same-cell-type 상한(0.749)과 cross-study **다른** 조혈 세포주(MOLM-13 0.695)의 차이가 ~0.05에 불과하다. 즉 **cell-type을 바꿔도 rank 보존이 cross-lab 기술 잡음 수준 이상으로는 거의 떨어지지 않는다** → t½는 강하게 **gene-intrinsic**하다. (Agarwal & Kelley 2022가 경고한 cross-dataset 기술 잡음이 상한을 눌러도, 그 상한 근처까지 보존된다.)
- **차용 위험이 실제로 존재하는 곳 = non-HK gene**: HK는 어디서나 보존(0.72–0.77)되므로 자명하다. non-HK에서도 세 비교 모두 **0.659–0.723**로 임계 0.50을 여유 있게 상회하므로 → cell-type-specific gene의 t½ 차용도 (보수적으로) 정당하다.
- 세 소스 전부(same-study·cross-study 조혈·cross-study 비조혈) PASS → 판정은 THP-1 같은 한 소스에 의존하지 않는다(robust PASS).

## 한계 / 후속 (PASS이되 무조건 아님)

1. **24h 우측 검열**: Todorovski K562의 8.1% gene이 24.0h에서 상한에 걸린다(진짜 t½가 아니다). Spearman은 견디나, 반감기 최상위 decile의 절대값과 Jaccard(top10% 0.29–0.46로 중간)는 이 검열로 약화된다. → §4 모델에서 t½를 연속 예측변수로 쓸 때 상한 gene은 별도로 처리하거나 censored로 인지해야 한다.
2. **여전히 HSPC 직접 t½는 아님**: 가장 가까운 것이 AML 세포주(MOLM-13)이다. CD34+ primary HSPC t½ 공개데이터가 없으므로 → gene-intrinsic 가정으로 방어하고(본 gate), §4에서 cell-type 차를 잔차/공변량으로 흡수한다(PROXY-JOIN-DESIGN §2.3, §4).
3. **결론 형태**: PASS = "t½ 차용 정당, 한계 명시"(스크립트 verdict). timing 예측이 아니며 — reframe(magnitude outcome, decay 통제 후 lag incremental)을 준수한다.

## 재현
```
conda run -n scv-preprocess python scripts/pj_gene_intrinsic_gate.py
```
입력 CSV 5종 + housekeeping.txt = `data/`(provenance: `data/PROVENANCE_halflife.md`). data/는 .gitignore에 있다.

---

# Proxy-join §2 GATE result — gene-intrinsic t½ conservation (BIOP01-27)

Run on 2026-07-03. Script `scripts/pj_gene_intrinsic_gate.py` (env `scv-preprocess`).
Question: **May we borrow Todorovski K562 (leukemia) mRNA half-life t½ into our HSPC lag analysis?**
Decision rule: gene-wise **Spearman ρ** of reference (K562) vs. comparison cell-line t½ (log t½ rank conservation). Threshold ρ≥0.50 PASS / 0.30–0.50 CONDITIONAL / <0.30 FAIL.
Data source · normalization · download URL = `data/PROVENANCE_halflife.md`.

## Verdict: **PASS** (median ρ = 0.74)

Raw outputs: `proxy_join/out_gate/gate_report.json`, plots `proxy_join/out_gate/gate_*.png`.
reference = Todorovski **K562_UT** 6,579 genes.

| comparison set | nature | n(overlap) | **global ρ** | HK ρ | **non-HK ρ** | top10% Jaccard |
|---|---|---:|---:|---:|---:|---:|
| THP-1 (Todorovski) | hematopoietic, **same-study (upper bound)** | 4,750 | 0.743 | 0.773 | 0.700 | 0.457 |
| **MOLM-13 (RNADecayCafe)** | hematopoietic AML, **cross-study (★primary metric)** | 6,061 | **0.695** | 0.727 | **0.659** | 0.287 |
| HEK293T (RNADecayCafe) | non-hematopoietic, cross-study lower bound | 6,337 | 0.750 | 0.771 | 0.723 | 0.396 |
| — median (script verdict) | | | **0.74** | | | |

**Anchor** (not included in gate median, for interpretation): K562(Todorovski) vs K562(RNADecayCafe = Ietswaart/Muhar/Schofield labs, **not Todorovski — confirmed**) = cross-lab **same-cell-type** ρ = **0.749** (n=6,404). → cross-study technical upper bound. (MOLM-13 also derives from Muhar 2018 and is independent of Todorovski — confirmed.)

## Interpretation (do not read from the median alone — report separately by source)

- **Primary gate metric = cross-study hematopoietic (MOLM-13) ρ = 0.695**, non-HK ρ = 0.659. THP-1 (same-study, 0.743) is an **optimistic upper bound** (same lab · SLAM-seq · 24h cap → shared technical covariance), so it is not used as the headline. The cross-study number is the answer.
- **Key point**: the difference between the cross-lab same-cell-type upper bound (0.749) and the cross-study **different** hematopoietic cell line (MOLM-13 0.695) is only ~0.05. That is, **even changing the cell-type barely reduces rank conservation by more than the cross-lab technical-noise level** → t½ is strongly **gene-intrinsic**. (Even when the cross-dataset technical noise warned of by Agarwal & Kelley 2022 pushes the upper bound down, conservation holds near that bound.)
- **Where borrowing risk actually lives = non-HK genes**: HK is conserved everywhere (0.72–0.77), so it is trivial. In non-HK too, all three comparisons are **0.659–0.723**, comfortably above the 0.50 threshold → borrowing t½ for cell-type-specific genes is (conservatively) also justified.
- All three sources (same-study · cross-study hematopoietic · cross-study non-hematopoietic) PASS → the verdict does not depend on a single source like THP-1 (robust PASS).

## Limitations / follow-up (PASS but not unconditional)

1. **24h right-censoring**: 8.1% of Todorovski K562 genes are capped at 24.0h (not a true t½). Spearman tolerates it, but the absolute values of the top decile of half-lives and the Jaccard (top10% 0.29–0.46, moderate) are weakened by this censoring. → When using t½ as a continuous predictor in the §4 model, capped genes must be handled separately or recognized as censored.
2. **Still not a direct HSPC t½**: the closest is an AML cell line (MOLM-13). No public CD34+ primary HSPC t½ data exists → defended by the gene-intrinsic assumption (this gate), with cell-type differences absorbed as residual/covariate in §4 (PROXY-JOIN-DESIGN §2.3, §4).
3. **Form of conclusion**: PASS = "t½ borrowing justified, limitations stated" (script verdict). Not a timing prediction — it follows the reframe (magnitude outcome, incremental lag after decay control).

## Reproduction
```
conda run -n scv-preprocess python scripts/pj_gene_intrinsic_gate.py
```
5 input CSVs + housekeeping.txt = `data/` (provenance: `data/PROVENANCE_halflife.md`). data/ is in .gitignore.
