# Lens — Industry

## 1. Categorization

### Domain (자동 추출, 검토 표시)

- `single-cell-genomics`
- `developmental-neuroscience`
- `chromatin accessibility`
- `regulatory-genomics`
- `disease-variant-interpretation`

### Use case (vocabulary 6개 중 1~3개)

- `academic-citation` — developing human cortex multiome reference dataset로 인용 가치가 높다.
- `methodology-reference` — chromatin accessibility + expression + regulatory variant scoring을 연결하는 분석 프레임을 차용할 수 있다.
- `pipeline-applicable` — `GSE162170`은 후속 multiome velocity benchmark에서 이미 재사용되며, 우리 single-cell multiome pipeline의 human cortex validation reference로 쓸 수 있다.

### Importance (1개 종합 등급)

- **Level**: 상
- **Perspective**: 본 프로젝트의 human brain multiome reference dataset 원 논문이며, chromatin-RNA coupling과 noncoding variant interpretation을 한 자료 안에서 연결해 methodology-reference와 citation 가치가 모두 높다.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: `검토필요:` abstract에는 cell, donor, ASD cohort size가 없다. QA 관점에서는 GEO/STAR Methods의 sample table이 필수 확인 대상.
- **Cohort 편향**: fetal human cortex sample은 접근성이 낮고 donor composition에 민감하다. `미제공:` ancestry, sex, gestational week distribution, tissue source heterogeneity는 local source에 없음.
- **Replication 부족**: abstract 기준으로는 independent clinical cohort replication 여부 확인 불가.
- **Multiple testing**: TF binding site disruption과 enrichment 분석은 다중 비교가 큰 영역이다. `검토필요:` FDR correction과 null model 확인 필요.

### 2.2 임상·기술적 제약

- 이 자료는 임상 진단 assay가 아니라 research-grade developmental atlas와 disease variant interpretation framework다.
- fetal cortex tissue는 산업 제품화 관점에서 sample procurement와 consent/IRB 부담이 크다.
- 10x Multiome류 assay와 sequence-level model은 분석 역량 요구가 높다. routine clinical turnaround에 바로 들어갈 형태는 아니다.

### 2.3 규제·QA·RA 관점

- **Regulatory pathway**: 현재는 IVD/LDT/SaMD evidence가 아니라 discovery/research evidence.
- **Analytical validation**: `미제공:` assay precision, LOD, reproducibility, inter-lab validation.
- **Clinical validation**: ASD variant scoring은 disease relevance hypothesis generation에 가깝다. sensitivity/specificity, PPV/NPV 같은 clinical performance는 local source에 없음.
- **IRB/consent**: human fetal tissue와 ASD cohort를 다루므로 원문 Methods의 ethics statement 확인 필요.

### 2.4 권위·신뢰 가중치

- 1차 출처: Cell peer-reviewed article, PubMed record, GEO accession, associated GitHub URL stub.
- 신뢰 가중치: peer-reviewed Cell paper라 reference value는 높다.
- COI: author affiliation 중 Illumina AI Laboratory가 포함되어 있다 (`sources/abstract.txt`). `검토필요:` full COI statement 확인 필요.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- 저자 그룹은 Stanford/Greenleaf/Kundaje/Pașca collaboration으로, regulatory genomics와 neurodevelopment 모델 양쪽의 협업 가치가 높다.
- 직접 라이선싱 자산으로 보기보다는 human cortex regulatory atlas, code/data reuse, 공동연구 reference로 보는 편이 현실적이다.

### 3.2 Commercialization-candidate (자체 제품화)

- **Dx**: ASD diagnostic으로 직접 제품화하기에는 evidence gap이 크다. disease variant interpretation support tool의 research-use-only component 정도가 현실적.
- **Software**: cell-type-specific regulatory variant interpretation pipeline의 module로 흡수 가능.
- **Assay/service**: 10x Multiome + regulatory atlas comparison service는 가능하지만, fetal brain reference의 적용 범위를 disease/organ model별로 제한해야 한다.

### 3.3 우리 파이프라인과의 fit

- Human cortex multiome benchmark와 regulatory element-gene linking use case가 우리 epigenomic-lag/single-cell multiome 분석과 잘 맞는다.
- HSPC multiome에 직접 biological conclusion을 옮길 수는 없지만, analysis pattern은 차용 가능하다.
- `해석:` 우리 파이프라인에서는 `GSE162170`을 raw discovery source보다 benchmark/reference annotation source로 두는 것이 ROI가 높다.

### 3.4 후속 BD·제품 액션 후보

- **PDF/STAR Methods 확보 후 QA checklist 작성**
  - 누가: 분석 담당자
  - 언제: 지금
  - 자원: PDF manual download, supplementary 확인
  - 성공 기준: cell/donor/cohort/QC/statistical test가 methodology brief에 채워짐
- **GSE162170 재현 가능성 점검**
  - 누가: bioinformatics 담당
  - 언제: 다음 sprint
  - 자원: GEO download, 10x/ArchR/Scanpy pipeline
  - 성공 기준: 후속 velocity paper에서 사용한 subset과 원 논문 annotation mapping 확인
- **Regulatory variant module PoC**
  - 누가: computational genomics 담당
  - 언제: 다음 분기
  - 자원: accessible peak-gene map + variant scoring baseline
  - 성공 기준: 우리 관심 disease/lineage에서 cell-type-specific variant prioritization report 생성

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective**: 본 프로젝트의 human brain multiome reference dataset 원 논문이며, chromatin-RNA coupling과 noncoding variant interpretation을 한 자료 안에서 연결해 methodology-reference와 citation 가치가 모두 높다.
- 등급 근거:
  - 후속 multiome velocity analyses에서 `GSE162170`이 benchmark dataset으로 반복 재사용된다.
  - PubMed abstract만으로도 scRNA/scATAC/joint multiome + ASD noncoding mutation scoring이라는 사용 범위가 명확하다.
  - 코드와 GEO URL stub이 있어 재현 출발점은 있다.
  - 단 PDF/supplementary 미확보 상태에서는 QA-grade methods와 Figure 수치를 확정할 수 없다.

### 4.2 활용 우선순위

- **지금**: original dataset citation과 source provenance 정리.
- **다음 분기**: GSE162170 subset 재현과 annotation mapping.
- **장기**: regulatory variant prioritization module로 확장.

### 4.3 발표·미팅에서 들이밀 시점

- 본인 논문/발표 introduction에서 human cortex multiome reference dataset 또는 chromatin accessibility와 expression을 결합한 developmental regulatory atlas 사례로 인용.
- R&D 리뷰에서는 "human fetal cortex benchmark의 원 출처"로 짧게 언급.

### 4.4 추가 탐색 필요 영역

- `질문:` Cell supplementary에 ASD cohort와 variant scoring null model이 얼마나 상세히 공개되어 있는가?
- `질문:` `brain_comp` repo가 논문 Figure 전체를 재현하는가, 아니면 일부 comparison/processing만 포함하는가?
