# Lens — Academic — Li 2023 MultiVelo

> Citation: `@li2023multivelo`. 본 노트는 `li-2023-multivelo_core.md` 작성 후 *학계 시선*만 따로 정리. 산업·규제·BD 관점은 `li-2023-multivelo_lens-industry.md`로 분리.

---

## Limitations

### 저자가 명시한 한계

- **TF lag mechanism은 association**: §Results "MultiVelo relates TFs..." — "We cannot conclusively determine the mechanisms underlying these time lags without additional data. However, post-transcriptional and post-translational regulation, factors that affect the activity of chromatin remodeling complexes, and intercellular signaling could all contribute to this phenomenon." 즉 *TF expression이 motif accessibility를 선행*한다는 결과는 *시간 association*일 뿐, *causal regulation* 증거는 아님.
- **Bergen 2021의 RNA velocity challenge 3개 중 1개만 해결** (§S5): "transcriptional boost" (inflection point 후 transcription rate 급증), "simultaneous emergence of distinct cell types" 두 challenge는 *MultiVelo도 미해결*. 저자가 "Addressing the other two challenges will require rethinking the entire dynamical model framework, which is beyond the scope of this paper"로 명시.
- **Single c per gene 가정**: §S2 — promoter + 모든 linked enhancer peak를 합산. enhancer별 differential kinetics는 못 본다. 9개 aggregation strategy 비교 (Supplementary Fig. 6)에서 결과 robust하지만 *근본 한계는 명시되지 않음*.
- **Model 0 (transcription이 chromatin opening 전) 배제**: §Methods 후반 + §S2 — "biologically implausible." 일부 케이스 (pioneer TF가 nucleosome eviction 동시 진행하는 경우 등)에 대한 *gold-standard validation 부재*.

### 분석자가 판단한 한계

- **부족한 점 1 — Causal validation 없음**:
  - **왜 중요한가**: TF gene expression → motif accessibility lag, M1 vs M2 분류는 *전부 association 기반*. paper는 mechanism (regulation, cell cycle gene 분류) 어조로 해석하지만 perturbation (CRISPR KO, dCas9-recruited HDAC) 없이는 *regulatory direction*을 주장하기 어려움.
  - **어떤 증거가 부족한가**: ① TF perturb 후 motif accessibility + downstream gene 변화 시계열, ② chromatin remodeler (e.g., SWI/SNF) perturb 후 priming length 변화, ③ M1 vs M2 분류된 gene의 KO 후 cell cycle 영향.

- **부족한 점 2 — Spearman 0.51 vs 0.44 (mouse skin) 외에 정량 metric 부재**:
  - **왜 중요한가**: cell fate prediction 정확도 개선이 핵심 claim. 그러나 정량 metric은 mouse skin 1개 dataset의 Spearman correlation 1개뿐. 다른 dataset (mouse brain, human brain, HSPC)에서는 *backflow 정성 비교*만.
  - **어떤 증거가 부족한가**: ① cross-boundary consistency score, ② velocity vector field smoothness, ③ ground-truth lineage tracing (e.g., metabolic labeling, scNT-seq, sci-fate) dataset에서의 absolute time accuracy, ④ branch probability vs known lineage.

- **부족한 점 3 — Generalization to non-developmental systems 미검증**:
  - **왜 중요한가**: 4개 dataset 모두 *active differentiation*. steady-state tissue (성인 간, 신장 nephron), regeneration, perturbation response (e.g., LPS stimulation), cancer (tumor heterogeneity), disease (sclerosis) 등 *non-developmental dynamic system*에 대한 검증 없음.
  - **어떤 증거가 부족한가**: ① stimulation 직후 (acute response, hours) chromatin opening 속도 estimate, ② cancer multi-omic dataset에서 model 1 vs 2 비율, ③ aging system에서 priming length 변화.

- **부족한 점 4 — Cell cycle confound 처리의 안전성**:
  - **왜 중요한가**: HSPC dataset에서 *cell cycle score regress-out* (S/G2M score를 RNA expression에서만 regress, unspliced/spliced count는 unchanged) 수행 (Methods §"Human HSPCs"). 그러나 cell cycle은 *chromatin opening/closing 자체*에 영향을 줄 가능성 (replication during S phase 시 chromatin 일시 변경 등).
  - **어떤 증거가 부족한가**: ① cell cycle phase별 c-u-s velocity 변화 ablation, ② non-cycling vs cycling cell separate fit 비교, ③ G1-arrested system (예: contact-inhibited cell) baseline.

- **부족한 점 5 — Identifiability of 8 parameters under noise**:
  - **왜 중요한가**: scVelo (4–5 parameter)보다 *2배 가까이* parameter 증가. Simulation (98.5% accuracy) 결과 있지만, *parameter identifiability* (예: profile likelihood, Fisher information) 별도 분석 부재.
  - **어떤 증거가 부족한가**: ① 각 parameter posterior 또는 confidence interval, ② noise scaling에 따른 parameter recovery curve, ③ partial trajectory gene (induction-only, repression-only)에서 추정 parameter의 *bias*.

- **부족한 점 6 — Data integration (separate RNA, ATAC) 시 정보 손실**:
  - **왜 중요한가**: Supplementary Fig. 1에서 *imputed pairing*으로 separate RNA/ATAC dataset 적용 시도. 결과: "lost/dampened priming and/or decoupling information." 즉 *paired multi-omic이 강제 조건*에 가까움.
  - **어떤 증거가 부족한가**: ① integration이 잘 작동하는 *조건* (cell type overlap %, dataset 크기) systematic 분석, ② alternative integration method (Harmony, scVI, GLUE, scMOMAT) 비교.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장 1**: "M2 genes are enriched for cell cycle GO" → "cells may use model 2 for rapid, transient activation of genes that do not need to maintain expression" (§Results 본문).
  - **현재 논문에서 제시한 근거**: M2 enriched GO terms (cell cycle), M2 expression timing earlier (P=9×10⁻⁷), HSPC dataset M2 marker UBE2C/GTSE1/KIF20B 시각화.
  - **더 필요해 보이는 근거**: cell cycle gene만 모은 ground-truth list (e.g., MSigDB Hallmark E2F target)에서 M1 vs M2 비율 확인. 그리고 *M2 ≠ cell cycle gene*인 fraction이 *어떤 functional category*인지 (예: immediate early gene, heat shock).

- **연결이 약한 주장 2**: SNP-gene lag 3 group → "groupings are relevant for understanding the functions of the SNPs" (§Results "MultiVelo relates TFs...").
  - **현재 논문에서 제시한 근거**: 3 group density plot (Fig. 6g), example SNP UMAP.
  - **더 필요해 보이는 근거**: ① group별 GWAS effect size correlation, ② disease별 (bipolar vs schizophrenia) group enrichment 차이, ③ eQTL data와의 cross-validation, ④ known functional SNPs (e.g., disease-causal variants from massively parallel reporter assays)와의 비교.

- **연결이 약한 주장 3**: Chromatin closing rate / opening rate ratio ≈ 1 (Fig. 3f) — "chromatin generally opens and closes at similar rates."
  - **현재 논문에서 제시한 근거**: Fig. 3f box plot (median ≈ 1).
  - **더 필요해 보이는 근거**: 이 ratio가 *external evidence* (e.g., MNase-seq dynamics, single-molecule tracking, FRAP)와 일치하는지 확인. 일반적으로 *closing이 opening보다 느린* 것으로 알려진 system들과 모순될 가능성.

- **연결이 약한 주장 4**: HSPC histone mark p=0.016 (H3K4me3 in M2)이 *M1/M2 분류의 외부 validation*으로 제시.
  - **현재 논문에서 제시한 근거**: ChIP-seq box plot Wilcoxon p value.
  - **더 필요해 보이는 근거**: ① multiple testing correction (3 mark × 2 model = 6 tests), ② effect size (Cohen's d), ③ 다른 cohort에서 replication.

### 정리되지 않은 질문

- **질문 1**: 같은 paper의 mouse brain dataset에서 chromatin closing rate ≈ opening rate (Fig. 3f). 그러나 HSPC dataset에서도 이 ratio가 1인가? 본문에 *mouse brain 1개 dataset의 ratio*만 보고됨. dataset 간 비교가 빠짐.

- **질문 2**: Decoupling LRT p-value가 일부 gene에서 10⁻²⁷⁹ 수준 (Robo2). 이는 *너무 강한* signal — sample size 효과인지 (n cell이 클수록 LRT statistic 자동 inflated)? p-value vs effect size 분리 검증 필요.

- **질문 3**: Stochastic model (Supplementary Fig. 2)이 deterministic vs *실제로 어떤 advantage*를 제공하는지 명확하지 않음. 둘 다 결과 비슷. 왜 두 버전 모두 제공? 사용자가 어느 시점에 어느 버전 써야 하는지 가이드 부재.

- **질문 4**: TF–motif lag (Fig. 6f)에서 "median positive at most latent times" — *모든 TF에 대해* positive인가, 일부 TF는 *negative* (motif accessibility가 TF expression을 선행)인가? Quantile plot에서 lower quantile은 negative로 보임. *어떤 TF가 negative*인지, 그게 어떤 mechanism (TF가 chromatin opening의 *consequence*인 케이스)을 의미하는지 미정리.

- **질문 5**: 4개 dataset 모두 *vertebrate, mouse + human only*. *non-mammalian* (drosophila, zebrafish) 또는 *plant* (Arabidopsis)에서 동일 동작이 보장되는가? chromatin–RNA lag이 universal한가?

## Final Takeaways

- **이 논문의 가장 큰 의미**:
  - RNA velocity framework를 *time-varying transcription rate*로 확장하는 *clean mathematical formulation*. 핵심 변화 (`α^(k)` → `α^(k) c(t)`)가 단순하면서 강력.
  - chromatin–RNA lag를 *latent time 단위로 정량*할 수 있게 한 첫 paper급 contribution. priming, decoupling을 *분석 가능한 quantity*로 만듦.
  - 신규 HSPC 10x Multiome dataset (11k cells, day 0 + day 7) 공개 (GSE209878) — community asset.

- **다음 논문으로 이어질 아이디어**:
  - **(아이디어 1) Causal validation via perturbation**: MultiVelo predicted M1/M2 분류 + TF-motif lag pair를 CRISPRi 또는 Perturb-seq로 검증. M1 gene KO 시 *coupled-off interval 단축* 가설 검증. → "Perturbation-validated chromatin–transcription coupling at single-cell resolution"
  - **(아이디어 2) MultiVelo on non-developmental systems**: ① LPS stimulation hour-by-hour multi-omic (인기 immunology system) — acute response의 priming/decoupling이 발달 system과 다른 패턴인가? ② tumor multi-omic (예: melanoma scMultiome) — M2 (cell cycle) 비율이 정상 대비 증가하는지. → "Chromatin–transcription dynamics across non-developmental states"
  - **(아이디어 3) MultiVelo + lineage tracing ground truth**: scNT-seq, sci-fate, metabolic labeling (4sU pulse) data에서 *true RNA half-life* 비교. MultiVelo의 추정 γ (degradation rate)가 *measured half-life*와 얼마나 일치? → method validation pillar.
  - **(아이디어 4) Per-enhancer kinetics**: 단일 c 대신 enhancer별 c_e(t)를 분리해 *enhancer specificity*가 priming length를 결정하는지 보기. → "Enhancer-resolved multi-omic velocity"
  - **(아이디어 5) MultiVelo + 3D genome**: Hi-C 또는 micro-C와 결합. chromatin opening이 long-range loop formation과 어떻게 연결되는지. → "Multi-omic velocity informed by chromatin topology"
  - **(아이디어 6) Spatial multi-omic velocity**: Stereo-seq 등 spatial multi-omic에서 MultiVelo 적용. cell이 *공간적으로* 이웃하는 chromatin priming gradient 관찰. → "Spatial multi-omic velocity"

- **설명을 더 매끄럽게 만들 방법**:
  - Section 1 (Results "MultiVelo distinguishes two models...") 뒤에 *quantitative cell fate metric* 추가. backflow를 정성적으로 보여주지 말고 vector field divergence, cell type boundary consistency 같은 score를 4개 dataset 모두에 적용.
  - SNP 분석 (Fig. 6g) 결과를 *known disease eQTL*과 cross-validate한 표 추가.
  - "M2 genes = cell cycle" 주장의 *exception*을 명시 (M2이면서 cell cycle 아닌 fraction, M1이면서 cell cycle인 fraction).

- **우선순위가 높은 후속 실험 / 분석**:
  - **(1) 우리 데이터에서 ablation 재실행**: M1/M2 force fit 결과를 *우리 HSPC 또는 organoid dataset*에서 재현해 robustness 확인.
  - **(2) Cell cycle phase별 c-u-s velocity 측정**: G1, S, G2/M arrested system에서 별도 fit 후 *cell cycle confound 영향* 정량.
  - **(3) MultiVelo + 다른 integration tool 비교**: scMOMAT, GLUE, MIRA, MultiMAP 등 multi-omic integration tool과 *upstream pipeline* 비교 — chromatin smoothing 전략이 결과에 얼마나 영향?

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- **§Introduction (p2)**: "Existing RNA velocity models assume that the transcription rate of a gene is uniform throughout the induction phase of gene expression. However, epigenomic changes play a key role in regulating gene expression..."
  - 사용 시나리오: 본인 introduction에서 *RNA velocity의 본질적 한계*를 짚을 때.
  - BibTeX key: `@li2023multivelo`

- **§Introduction (p2)**: "Single-cell multi-omic measurements provide an opportunity to incorporate epigenomic data into mechanistic models of transcription."
  - 사용 시나리오: multi-omic single-cell의 motivation 인용. proposal에서 "왜 multi-omic이 필요한가" 문단.
  - BibTeX key: `@li2023multivelo`

- **§Results "MultiVelo: a differential equation model..." (p3)**: "two distinct types of discordance between chromatin accessibility and transcription can occur ... we refer to this phenomenon as priming ... and decoupling."
  - 사용 시나리오: priming/decoupling concept 정의 인용.
  - BibTeX key: `@li2023multivelo`

- **§Discussion (p10)**: "In summary, MultiVelo models temporal chromatin accessibility and gene expression levels and quantifies the length of priming and decoupling intervals in which chromatin accessibility and gene expression are temporally out of sync."
  - 사용 시나리오: MultiVelo의 *one-sentence summary* 인용. review 또는 본인 multi-omic method paper의 prior work 단락.
  - BibTeX key: `@li2023multivelo`

- **§S5 (supplementary)**: "Addressing the other two challenges [transcriptional boost, simultaneous emergence] will require rethinking the entire dynamical model framework, which is beyond the scope of this paper."
  - 사용 시나리오: *MultiVelo의 한계*를 인정하는 후속 method paper에서 motivation으로.
  - BibTeX key: `@li2023multivelo`

- **§Results "MultiVelo relates TFs..." (p10)**: "We cannot conclusively determine the mechanisms underlying these time lags without additional data."
  - 사용 시나리오: *TF lag = causal proof 아님* 강조할 때. 본인 perturbation experiment proposal motivation.
  - BibTeX key: `@li2023multivelo`

### 인용 가능 수치

- **Spearman 0.51 (MultiVelo) vs 0.44 (scVelo) vs Palantir pseudotime, mouse skin**, §Results "MultiVelo quantifies epigenomic priming in SHARE-seq...".
  - 사용 시나리오: MultiVelo의 *정량 win*을 인용할 때. baseline reference.
  - BibTeX key: `@li2023multivelo`

- **State proportion (mouse brain 865 genes): induction 29.5%, repression 2.4%, M1 41.4%, M2 26.7%** (Fig. 2h).
  - 사용 시나리오: chromatin-transcription coupling pattern 분포 인용. 우리 데이터 분석 시 *expected baseline*.
  - BibTeX key: `@li2023multivelo`

- **Median priming interval 21%, decoupling interval 19%** of total time (mouse brain), §Results.
  - 사용 시나리오: priming/decoupling duration의 *first quantitative reference*.
  - BibTeX key: `@li2023multivelo`

- **HSPC ChIP-seq H3K4me3: p=0.016 (M2 higher), H3K4me1: p=0.097 (M1 higher), H3K27ac: p=0.48** (§S5, Extended Data Fig. 2c).
  - 사용 시나리오: M1/M2 분류의 *외부 epigenomic validation* 인용.
  - BibTeX key: `@li2023multivelo`

- **Simulation accuracy: 98.5% (likelihood-based) / 95.8% (top-quantile)** model assignment (§S3, Extended Data Fig. 5).
  - 사용 시나리오: MultiVelo의 *parameter identifiability* 근거 인용.
  - BibTeX key: `@li2023multivelo`

- **Runtime: 40 / 69 / 124 / 40 min on Intel i7-9750H 12-thread CPU** (Supplementary Table S1).
  - 사용 시나리오: computational feasibility 인용. 우리 lab 적용 가능성 평가 baseline.
  - BibTeX key: `@li2023multivelo`

- **6,968 GWAS SNPs → 757 filtered SNPs → 3 disease group classification** (§Results "MultiVelo relates TFs...").
  - 사용 시나리오: disease SNP × multi-omic velocity 연결 prior work.
  - BibTeX key: `@li2023multivelo`

### 인용 가능 Figure/Table

- **Figure 1 (schematic)**:
  - 무엇을 보여주는지 한 줄: chromatin–RNA ODE coupling + 2 model + 4 state의 schematic.
  - 사용 시나리오: 본인 review 또는 lab seminar에서 *chromatin-transcription coupling* 그림으로 재현. *재현 시 license 확인 필요* (Nature/Springer rights).
  - BibTeX key: `@li2023multivelo`

- **Figure 2 (mouse brain MultiVelo vs scVelo)**:
  - 무엇을 보여주는지 한 줄: chromatin 추가로 backflow 해결 + M1/M2 gene 예시.
  - 사용 시나리오: 본인 grant application의 *preliminary data로 RNA-only velocity 한계* 보여줄 때.
  - BibTeX key: `@li2023multivelo`

- **Figure 6e, f (TF–motif accessibility DTW + median Δt)**:
  - 무엇을 보여주는지 한 줄: TF gene expression이 motif accessibility를 선행 (median Δt > 0).
  - 사용 시나리오: TF regulatory dynamics 관련 본인 분석 introduction의 *first quantitative observation*.
  - BibTeX key: `@li2023multivelo`

- **Supplementary Table S1 (runtime/memory)**:
  - 무엇을 보여주는지 한 줄: 4 dataset × runtime + memory benchmark.
  - 사용 시나리오: tool comparison table에서 *resource requirement* 셀.
  - BibTeX key: `@li2023multivelo`

- **Supplementary Fig. 5d (decoupling LRT p-values)**:
  - 무엇을 보여주는지 한 줄: gene별 decoupling interval significance.
  - 사용 시나리오: *decoupling이 통계적으로 유의*하다는 점을 본인 follow-up paper에서 인용.
  - BibTeX key: `@li2023multivelo`
