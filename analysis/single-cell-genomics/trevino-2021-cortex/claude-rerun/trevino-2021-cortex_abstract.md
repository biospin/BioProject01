# Trevino 2021 — Developing Human Cortex Multi-ome — Abstract Analysis (Claude 재현)

- **재현 메타**: Codex에서 돌린 BioProject01 논문 분석 하네스를 Claude Code로 포팅한 뒤(`.claude/skills/abstract-analysis` + `.claude/agents/abstract-analysis.md`), 동일 하네스를 Claude에서 재실행한 산출물. 비교를 위해 Codex 원본(`../trevino-2021-cortex_abstract.md`)을 덮어쓰지 않고 별도 폴더에 저장.
- **Source**: `../sources/abstract.txt` (PubMed, PMID 34390642) + `../sources/publisher_fulltext_excerpt.txt` (ScienceDirect landing — Highlights + data/code availability). 본 분석은 abstract와 open-access highlights만 근거. 본문/Figures/STAR Methods 미참조 (full PDF 미확보 — Codex run의 `검토필요:`와 동일 경계).
- **분석 일자**: 2026-06-09.

## Abstract Summary

- **한 문장 요약**: 발생 중 human cerebral cortex(인간 대뇌 피질)에서 scRNA-seq와 scATAC-seq를 독립·joint로 측정해 single-cell 수준의 gene expression + chromatin accessibility atlas를 만들고, base-pair-resolution neural network로 ASD 관련 noncoding mutation의 cell-type-specific disruption을 예측한 연구.
- **연구 목적**: corticogenesis(피질 발생)에서 어떤 gene-regulatory element가 어느 cell type에서 결정적인지 dynamic하게 mapping → ASD 등 neurodevelopmental disease의 cell-type-specific 발병 단서 제공.
- **문제 또는 gap**:
  - cortical development의 genetic perturbation이 ASD 등 neurodev disease로 이어진다는 것은 알려졌으나, corticogenesis에 결정적인 genomic region(어느 cell type의 어느 regulatory element인지)이 정량적으로 mapping돼 있지 않음.
  - (해석:) bulk 측정은 cell type 해상도를 잃고, 단일 modality(scRNA 또는 scATAC만)는 동일 세포의 chromatin–RNA 연결을 잃음 → 독립 + joint 병행 측정의 동기. abstract는 "independently and jointly"만 명시.
- **핵심 방법**:
  - scRNA-seq + scATAC-seq를 독립적으로, 그리고 jointly(같은 세포에서 동시) 측정해 gene-regulatory element activity map 생성.
  - cis-regulatory element ↔ linked gene expression 상관으로 lineage-determining TF 식별.
  - base-pair-resolution neural network model로 noncoding mutation의 disruptive 여부를 cell-type-specific하게 예측, ASD cohort에 적용.
  - (외부 맥락:) Highlights는 NN을 "neural networks prioritize noncoding de novo mutations"로만 기술. 구체 model 이름은 abstract/excerpt에 없음 — code는 `GreenleafLab/Brain_ASD`(BPNet 계열로 추정, 확인필요).
- **주요 결과**:
  - key TF에 의한 gene regulation의 wave가 거의 continuous한 differentiation trajectory를 따라 나타남.
  - glial lineage의 distinct expression program 분리(neurogenesis vs gliogenesis 별개 regulatory program — Highlights).
  - lineage-determining TF는 linked regulatory element와 expression 간 상관이 강하고, early differentiating cell에서 active chromatin state로 선행 전환 → lineage commitment와 일관.
  - ASD cohort의 noncoding mutation이 특정 cell type에서 강하게 enrichment, frequently disrupted TF binding site 식별.
- **저자가 주장하는 기여**:
  1. human cortex의 cell-type-specific gene-regulatory atlas (정확한 cell/donor 수 abstract에 없음).
  2. continuous differentiation trajectory를 따른 TF regulation wave 기술.
  3. lineage-determining TF의 chromatin priming(조기 active state) 입증.
  4. cell-type-specific하게 ASD noncoding mutation 영향을 정량하는 NN framework.

## 추출 규칙 적용

- **모호한 주장**: "nearly continuous differentiation trajectory" — trajectory inference method/통계량 미명시. "strong correlation between linked gene-regulatory elements and expression levels" — correlation metric/threshold 미명시.
- **Abstract에 명시되지 않음**: 정확한 cell 수·donor 수·gestational week 범위·replicate 수; NN model 구조/학습 데이터/output; ASD cohort sample size·mutation 수; 비교 baseline 대비 성능 수치.
- **Abstract 외부 맥락**:
  - Data: GEO **GSE162170** + supplementary website `https://scbrainregulation.su.domains/` (excerpt).
  - Code: `https://github.com/GreenleafLab/Brain_ASD` (excerpt).
  - 저자 구성: Greenleaf lab(ATAC-seq), Pașca lab(cortical organoid), Kundaje lab(base-pair NN), Illumina AI(K. Farh) collaboration — abstract author affiliation 기반.
- **검토필요:** full PDF 미확보로 Figure/Table/STAR Methods는 PDF drop 후 `<paper-id>_core.md`에서 확장.

## 후속 작업 (PDF 입수 후)

- `trevino-2021-cortex_core.md`로 확장: Background(corticogenesis + ASD) / Methods(sample, scRNA·scATAC·multiome protocol, NN model, ASD analysis) / Results(cell typing, TF wave, glial lineage, ASD scoring) / Figures.
- 본 프로젝트 관점 우선 확인:
  1. GSE162170에 실제 deposit된 modality와 sample 수 (후속 velocity paper들이 "fetal human cortex 10x Multiome"으로 인용).
  2. cell type annotation 기준(marker, cluster id) — 후속 paper가 그대로 차용.
  3. lineage-determining TF list와 chromatin-priming lag을 정량했는지(abstract는 binary 표현만).
  4. NN model이 BPNet/ChromBPNet/자체 model 중 무엇인지.
