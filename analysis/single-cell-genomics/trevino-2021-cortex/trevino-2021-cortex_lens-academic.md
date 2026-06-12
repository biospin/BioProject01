# Lens — Academic

## Limitations

### 저자가 명시한 한계

- `검토필요:` Discussion/Limitation 원문을 확인하지 못했다. 현재 local source에는 PubMed abstract만 있어 저자 명시 한계를 확정할 수 없다.

### 분석자가 판단한 한계

- **부족한 점**: linked regulatory element와 gene expression의 strong correlation은 regulatory relationship의 근거지만, TF perturbation이나 enhancer perturbation 없이 causal regulation으로 단정하기 어렵다.
- **왜 중요한가**: ASD noncoding mutation interpretation은 cell-type-specific regulatory map에 의존한다. map의 peak-gene link가 틀리면 disrupted TF binding site와 target gene 해석이 바뀐다.
- **어떤 증거가 부족한가**: `미제공:` abstract에는 correlation metric, FDR, held-out validation, variant effect calibration, perturbation validation이 없다.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: active chromatin state transition이 early differentiating cells에서 먼저 관찰된다는 결과와 lineage commitment causality 사이.
- **현재 논문에서 제시한 근거**: abstract 기준으로는 chromatin accessibility와 gene expression의 trajectory-level association.
- **더 필요해 보이는 근거**: matched developmental timepoint replication, donor-level reproducibility, TF perturbation 또는 CRISPRi enhancer validation.

### 정리되지 않은 질문

- `질문:` `GSE162170`의 joint multiome cell subset과 independent scRNA/scATAC subset은 어떤 방식으로 통합됐는가?
- `질문:` ASD variant enrichment에서 control noncoding variant set은 GC content, mappability, mutational context, accessibility를 어떻게 matching했는가?
- `질문:` cell type별 disrupted TF binding site가 gene expression change 또는 disease-relevant phenotype과 연결되는 downstream validation이 있는가?

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- `sources/abstract.txt`: "single-cell atlas of gene expression and chromatin accessibility in the developing human cortex" 핵심 어구.
  - 사용 시나리오: human fetal cortex multiome reference dataset 소개.
  - BibTeX key: `@trevino2021cortex`
- `sources/abstract.txt`: "nearly continuous differentiation trajectory"와 TF-driven gene-regulation wave.
  - 사용 시나리오: developmental trajectory에서 chromatin-RNA coupling 또는 regulatory priming을 설명할 때.
  - BibTeX key: `@trevino2021cortex`
- `sources/abstract.txt`: ASD noncoding mutations의 cell-type-specific enrichment와 disrupted TF binding site 식별.
  - 사용 시나리오: disease variant interpretation에서 single-cell regulatory atlas가 필요한 이유를 쓸 때.
  - BibTeX key: `@trevino2021cortex`

### 인용 가능 수치

- `미제공:` abstract에는 cell 수, donor 수, ASD cohort size, p-value가 없다. 수치 인용은 PDF/STAR Methods 확인 전 보류.

### 인용 가능 Figure/Table

- `검토필요:` 원문 PDF 확보 후 atlas overview Figure, TF dynamics Figure, ASD variant scoring Figure를 선별.

## Final Takeaways

- 이 논문의 학술적 의미는 human cortex development를 transcriptome-only가 아니라 chromatin accessibility와 같이 해석하는 reference atlas를 제공했다는 점이다.
- 다음 논문 아이디어는 이 atlas의 peak-gene/TF-gene association을 perturb-seq, CRISPRi enhancer perturbation, 또는 orthogonal eQTL/caQTL evidence로 검증하는 방향이 가장 자연스럽다.
- 본 프로젝트에서는 Trevino 2021을 `GSE162170` benchmark의 original source로 인용하되, 후속 velocity paper가 전처리한 subset과 원 논문의 full atlas가 같은 대상인지 구분해서 써야 한다.
