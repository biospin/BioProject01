# Trevino 2021 — Developing Human Cortex Multi-ome — Abstract Analysis

- **Source**: PubMed abstract (`sources/abstract.txt`, PMID 34390642). 본 분석은 abstract만 근거. 본문/Figures/Methods 미참조 — full PDF drop 후 `<paper-id>_core.md` 별도 생성 예정.
- **분석 일자**: 2026-05-26.

## Abstract Summary

- **한 문장 요약**: 발생 중 human cerebral cortex에서 scRNA-seq, scATAC-seq, 그리고 joint multi-omic 측정을 결합해 cell type/lineage별 gene-regulatory element activity map을 만들고, base-pair-resolution NN 모델로 ASD-관련 noncoding mutation의 cell-type-specific disruption을 정량.
- **연구 목적**: corticogenesis (human cortex development) 과정에서 어떤 regulatory element가 어떤 cell type에서 결정적인지 dynamic하게 추적 → neurodevelopmental disease (특히 ASD) 의 cell-type-specific 발병 메커니즘 단서 제공.
- **문제 또는 gap**:
  - Cortex 발생의 *genetic perturbation*이 ASD 등 neurodev disease를 유발한다는 사실은 알려져 있으나, *어떤 cell type의 어떤 regulatory element*가 결정적인지 정량적 map이 없음.
  - Bulk 측정은 cell type 해상도 손실, unimodal scRNA/scATAC는 동일 세포의 chromatin–RNA coupling 손실.
- **핵심 방법**:
  - scRNA-seq + scATAC-seq를 *독립적으로* 측정 + *joint multi-omic* (10x Multiome) 측정 병행.
  - cis-regulatory element ↔ linked gene expression 상관 분석으로 lineage-determining TF 식별.
  - Base-pair-resolution neural network model — noncoding mutation의 *cell-type-specific* disruption 예측 (model 이름/구조 abstract에 없음, ChromBPNet 류 추정 — 외부 맥락 / 확인 필요).
  - ASD individuals cohort의 noncoding mutation을 model로 scoring.
- **주요 결과**:
  - 거의 *continuous한 differentiation trajectory*를 따라 key TF에 의한 gene-regulation의 *wave* 패턴 식별.
  - Glial lineage의 distinct expression program 분리.
  - Lineage-determining TF — linked regulatory element와 expression 간 상관이 강함; early differentiating cell에서 active chromatin state로 *선행* 전환 (lineage commitment와 일관).
  - ASD cohort의 noncoding mutation이 *특정 cell type*에서 강하게 enrichment + *frequently disrupted TF binding site* 식별.
- **저자가 주장하는 기여**:
  1. Human cortex의 cell-type-specific gene-regulatory atlas (정확한 cell 수는 abstract에 없음).
  2. Continuous differentiation trajectory를 따른 TF regulation wave model.
  3. Lineage-determining TF의 chromatin priming 입증 (cortex 맥락).
  4. ASD noncoding mutation의 cell-type-specific impact 정량 framework.

## 추출 규칙 적용

- **모호한 주장**: "nearly continuous differentiation trajectory" — 통계량/trajectory inference method abstract에 없음; "strong correlation between linked regulatory elements and expression levels" — 어떤 correlation metric / threshold인지 미명시.
- **Abstract에 명시되지 않음**:
  - 정확한 cell 수, donor 수, gestational week 범위, replicate 수.
  - NN 모델 구조 / 학습 데이터 / output type.
  - ASD cohort의 sample size, mutation 수.
  - 다른 비교군 paper / dataset 대비 성능.
- **Abstract 외부 맥락**:
  - 본 프로젝트 Dataset 3의 GEO accession은 GSE162170 (paper-info.yaml `data` 참조).
  - 이 paper는 MultiVelo (Li 2023, "Dataset 4 — Fetal human cerebral cortex 10x Multiome (Trevino 2021)") + MultiVeloVAE 등의 *evaluation dataset*으로 표준화돼 있음.
  - Greenleaf lab (ATAC-seq 개척, ArchR 개발) + Pașca lab (cortical organoid) + Kundaje lab (Base-pair NN, ChromBPNet 등) collaboration — abstract 외 정보.

## 후속 작업 (PDF 입수 후)

- `trevino-2021-cortex_core.md` 작성: Background (corticogenesis + ASD 배경) / Methods (sample collection, scRNA/scATAC/multiome protocol, NN model, ASD analysis) / Results (cell typing, TF wave, glial lineage, ASD scoring) / Figures.
- 본 프로젝트 관점에서 우선 확인할 것:
  1. *GSE162170에 실제로 deposit된 modality*: scRNA만? scATAC만? Multiome만? 몇 sample? — MultiVelo가 "fetal human cortex 10x Multiome"으로 인용하므로 Multiome가 핵심.
  2. cell type annotation 기준 (marker genes, ArchR cluster id 등) — 후속 paper들이 이 annotation을 그대로 차용.
  3. lineage-determining TF의 *list* + 각 TF의 chromatin-priming lag (lag을 *정량*했는지 확인. abstract는 "active chromatin state 전환"이라는 binary 표현만 사용).
  4. NN model이 ChromBPNet인지 BPNet인지 자체 model인지 확인 (Kundaje lab → 가능성 높음).
