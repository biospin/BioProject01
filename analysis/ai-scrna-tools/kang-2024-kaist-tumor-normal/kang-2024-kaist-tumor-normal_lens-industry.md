# Lens — Industry
# kang-2024-kaist-tumor-normal

## 1. Categorization

> 이 섹션은 paper-info.yaml의 categorization 블록과 동기화된다.

### Domain (자동 추출)

- `single-cell-genomics`
- `tumor-microenvironment`
- `cancer-immunology`
- `spatial-transcriptomics`
- `pan-cancer-atlas`

### Use case

- `pipeline-applicable` — Zenodo 공개 data + cellatlas.kaist.ac.kr web portal에서 우리 관심 cell type의 정상 조직 발현 즉시 조회 가능. ADC target의 tumor vs. normal selectivity 분석에 직접 참조.
- `academic-citation` — 30 암종 규모의 tumor-normal atlas는 단일 세포 cancer biology 논문의 background 또는 방법론 section 에서 reference로 빈번히 인용될 것. Citation 후보 풍부.
- `BD-opportunity` — KAIST + Samsung Medical Center 협력 연구. 저자 그룹(Choi JK, Park JE)은 pan-cancer informatics 역량 보유. 공동연구·데이터 접근 협의 가능성.

### Importance

- **Level**: 상
- **Perspective**: 30 암종에서 정상 조직 대비 종양 조직 cell state를 체계적으로 비교한 최대 규모 open atlas — ADC target selectivity 평가 및 정상 조직 발현 baseline 확보에 즉시 활용 가능.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size 불균형**: 104 datasets를 통합했으나 암종별 샘플 수 편차가 크다. BRCA, LC, HNSC, HCC 중심 — 희귀 암종(NET, synovial sarcoma 등)은 샘플 수가 상대적으로 적어 해당 암종의 cell state 정의 신뢰도가 낮다.
- **Cohort 편향**: 단일 기관(KAIST, SMC) 중심의 LC immunotherapy cohort ($n=497$). 동양인 환자 편중 가능성. 서양인 대형 코호트(TCGA는 포함되나 면역치료 cohort는 제한적)와의 ethnic diversity 불균형.
- **Replication 부족 (ADC 목적)**: AKR1C1⁺/WNT5A⁺ fibroblast의 발현 패턴이 단일 연구에서만 검증됨. ADC off-target toxicity 평가용으로 사용하려면 독립 코호트 검증 필요. `해석: ADC target 연구 인용 시 정상 기관에서의 발현 수준을 다른 데이터베이스(Human Protein Atlas 등)와 cross-check 권장.`
- **Multiple testing**: AND-gating에서 BH correction 적용 (adjusted $p < 0.05$). 면역치료 meta-analysis에서 cell state별로 multiple testing correction이 명시되어 있으나, forest plot에서 유의한 cell state만 표시되어 전체 correction 범위가 불명확.

### 2.2 임상·기술적 제약

- **10x Chromium 한정**: 포함 기준에서 10x Chromium 기반 scRNA-seq만 수집. Smart-seq2, Drop-seq 등 다른 플랫폼 제외. 기관별 chemistry 차이도 배제하여 실제 임상 적용 시 데이터 호환성 제한 가능.
- **Fresh/FFPE 혼합**: Methods에서 LC cohort는 FFPE도 포함 (AllPrep DNA/RNA Mini Kit 사용). FFPE 유래 scRNA-seq는 fresh 대비 RNA 품질 열등 — fresh/FFPE 혼합이 cell state 정의 품질에 미치는 영향이 본문에서 명시적으로 다뤄지지 않음.
- **계산 자원**: 4.9M 세포 처리는 고성능 컴퓨팅 필수. Geometric sketching으로 서브샘플링하여 처리 부담을 줄였으나, 원본 데이터 전체 재분석은 GPU 서버 또는 HPC 환경 필요.
- **EGA 통제 접근**: LC cohort scRNA-seq 데이터가 EGA EGAD00000000469에 controlled access. 데이터 활용 신청 및 승인 절차(4주 예상)가 필요하며, 분석 재현 또는 확장 시 지연 가능성.

### 2.3 규제·QA·RA 관점

- **IRB**: SMC immunotherapy cohort는 SMC IRB 2018-03-130 승인, 환자 written consent 포함. 인간 샘플 사용 기준 충족.
- **Analytical validation**: 이 논문은 biomarker 분류 연구이지만, TLS signature가 IVD (in vitro diagnostic) 또는 CDx (companion diagnostic)로 개발되려면 analytical validation (정밀도, 정확도, LOD) + clinical validation (prospective cohort에서 sensitivity/specificity)이 필요하다. 본 연구는 그 단계의 전단계(discovery/hypothesis generation) 수준.
- **FDA/EMA pathway**: TLS signature를 predictive biomarker로 개발 시 FDA Pre-Sub 또는 Breakthrough Device Designation 고려 가능. 현 단계에서 regulatory grade evidence는 미충족.
- **GCP / GLP**: scRNA-seq 분석이 연구 목적이므로 GLP 적용 없음. 임상 진단으로 전환 시 재설계 필요.

### 2.4 권위·신뢰 가중치

- `1차 출처:` Nature Communications (peer-reviewed, open access). Impact factor 14+. KAIST + Samsung Medical Center 기관 신뢰도.
- **저자 이해상충**: "The authors declare no competing interests." Penta Medix Co., Ltd. (Choi JK 소속 기업)가 author affiliation에 포함 — 미래 상업화와의 연계 가능성 관찰 필요.
- **Funding**: NRF (한국 국가 연구비), Samsung Medical Center, 한국 보건복지부 — 상업적 스폰서 없음. Bias 위험 낮음.
- **Erratum**: 2025-03-21 정오표 발행 (Nat Commun 16:2806). 내용을 확인 필요. `검토필요:` 정오표 세부 내용 확인 — ADC 관련 fig/table에 영향을 주는 수정인지 여부.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **KAIST 오픈 web portal**: cellatlas.kaist.ac.kr/ecosystem/ — interactive visualization, cell state 조회, expression 검색. 외부 연구자가 직접 데이터를 탐색 가능. 별도 계약 없이 정상 조직 baseline 데이터 접근 가능.
- **저자 그룹 협력 가능성**: Park JE (KAIST, jp24@kaist.ac.kr), Choi JK (KAIST + Penta Medix, jungkyoon@kaist.ac.kr)가 corresponding authors. Penta Medix와 Choi JK의 연계는 상업화 관심을 시사. 공동연구 또는 dataset 접근 협의 가능성 있음.
- **경쟁사 관찰**: Barkley et al. (Broad Institute/Weizmann), Gavish et al. 등 동일 niche의 경쟁 atlas들. 본 논문은 정상 조직 포함과 규모(4.9M)에서 차별화. 경쟁 atlas들과의 차이점을 BD 피치에서 강조 가능.
- **시장 영향**: 면역치료 반응 예측 biomarker 시장에서 TLS 관련 marker가 주목받는 시점에 이 atlas가 자원으로 활용될 가능성 높음. Immuno-oncology CDx 개발사들이 이 데이터셋을 reference로 사용할 수 있음.

### 3.2 Commercialization-candidate (자체 제품화)

- **Diagnostic (Dx) 후보**:
  - TLS signature → immunotherapy response prediction test: 현재 TRL 3~4 (lab validation 단계). prospective 검증 필요. RCC에서 spatial TLS와의 일치도가 보여졌으나 다른 암종에서 추가 검증 필요.
  - AKR1C1⁺/WNT5A⁺ fibroblast ratio → TME subtyping: 현재 TRL 2~3 (proof-of-concept). 임상적 actionability 증명 필요.
- **Software (SW) 후보**:
  - Atlas 기반 cell state annotation pipeline: cellatlas web portal의 상업화 또는 API 제공. KAIST 그룹이 이미 web portal을 구축한 상태. TRL 4~5.
  - ADC off-target prediction tool: 정상 조직 cell state expression profile을 ADC target scoring에 통합하는 SW 모듈. 우리 팀이 자체 개발 가능 (데이터 오픈).
- **IP 자유도**: 분석 알고리즘(NMF + AND-gating + Ro/e)은 코드 공개 상태 (Zenodo). TLS signature gene list는 Supplementary Data 7에 공개. 오픈 implementation 개발 가능.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**: 이 논문의 데이터는 10x Chromium scRNA-seq + 공간 전사체. 우리 NCCHE CTC/tumor scRNA-seq과 직접 통합 가능 (같은 platform). 정상 조직 reference로 우리 tumor cell과의 비교에 즉시 활용.
- **자원 가능성**: Zenodo data 오픈 접근 가능, cellatlas web portal에서 interactive query 가능. 전체 데이터 재분석은 대형 서버 필요하나, cell state score를 우리 데이터에 projection하는 것은 GPU 없이 가능 (sc.tl.score_genes).
- **비용·시간 추정**: cellatlas portal 활용으로 정상 발현 baseline 조회 → 1~2일. 우리 scRNA-seq에 cell state projection (Zenodo reference component 활용) → 1~2주. 독립 재분석 → 1~2개월 + HPC 자원.
- **전략적 fit**: ADC target의 tumor/normal selectivity 평가에 직접 활용 가능. 특히 fibroblast marker (AKR1C1, WNT5A), immune checkpoint (LAG3, PDCD1) 관련 target이 정상 조직에서 어느 수준으로 발현되는지 확인하는 reference.

### 3.4 후속 BD·제품 액션 후보

- **정상 조직 baseline 데이터 추출**
  - 누가: 분석 담당자 (분석팀)
  - 언제: 지금 (이번 sprint)
  - 자원: cellatlas.kaist.ac.kr web portal 접근, 인력 0.5 FTE × 1주
  - 성공 기준: 우리 ADC target 후보 gene list에 대해 30 암종 × 정상 조직 cell type별 발현 수준 표 완성

- **TLS signature를 우리 tumor scRNA-seq에 projection**
  - 누가: 분석팀
  - 언제: 다음 분기
  - 자원: Zenodo 공개 data + sc.tl.score_genes; GPU 없이 가능
  - 성공 기준: 우리 tumor sample에서 TLS-enriched vs non-enriched 구분 및 면역치료 반응 예측력 초기 검증

- **KAIST 저자 그룹 공동연구 협의**
  - 누가: BD lead + 분석 담당자
  - 언제: 다음 분기
  - 자원: 미팅 1회 (온라인), pre-meeting deck 준비
  - 성공 기준: 데이터 접근 범위 확인 및 공동연구 가능성 탐색

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective**: 30 암종 4.9M 세포 tumor-normal 대비 atlas — ADC target validation의 정상 조직 baseline 확보에 직접 활용 가능하며 data 완전 공개.
- **등급 근거**:
  - 정상 조직 포함 대규모 atlas로서 ADC off-target 평가 reference로 즉시 활용 가능하다. Human Protein Atlas의 단백질 발현 데이터를 단일 세포 cell state 수준으로 업그레이드한 형태.
  - 4.9M 세포, 30 암종이라는 규모는 단일 연구로서 현재까지 최대급이며, 이후 5년간 major reference가 될 것이다.
  - 데이터(Zenodo)와 코드 완전 공개, web portal 운영 중 — 팀 자체 분석 및 BD 발표 자료 작성에 즉시 활용 가능.
  - 단, smFISH $n=3$ 기반 주장들과 단일 기관 LC cohort의 meta-analysis 비중이 한계. ADC 개발에 바로 쓰기보다는 "hypothesis 생성 + baseline 참조" 수준으로 활용.

### 4.2 활용 우선순위

- **지금 (이번 sprint / 이번 달)**: cellatlas web portal에서 우리 ADC target 후보 gene의 정상 조직 cell state별 발현 조회. 1~2일 작업.
- **다음 분기**: Zenodo data를 우리 scRNA-seq에 projection하여 우리 샘플의 cell state 구성 파악 + TLS signature score 산출.
- **장기**: KAIST 그룹과 공동연구 협의 가능성 탐색. 특히 우리 CTC 또는 tumor scRNA-seq 데이터를 이 atlas에 annotation하는 파이프라인 개발.

### 4.3 발표·미팅에서 들이밀 시점

- **BD 미팅 / ADC pitch deck**: "30 암종에서 정상 조직 대비 종양의 cell state 비교 atlas — 우리 target의 정상 발현 근거 데이터" 슬라이드에 Fig. 1A 또는 Fig. 2A 인용. 파트너사에게 scientific rigor 보여주는 데 유용.
- **사내 R&D 리뷰**: ADC target selectivity 평가 시 이 atlas를 정상 조직 reference로 사용하는 방법론 제안 자리에서 소개.
- **논문 introduction / background**: cancer immunology 또는 ADC 논문의 TME baseline 설정에서 인용.

### 4.4 추가 탐색 필요 영역

- `질문:` Penta Medix (Choi JK 소속 기업)가 이 atlas를 상업적으로 활용하고 있는지 확인 필요 (웹사이트, 특허 검색).
- `질문:` 정오표(2025-03-21)의 세부 내용 확인 — Figure 또는 수치 오류 수정인지, 해석에 영향을 주는 내용인지.
- `질문:` TLS signature (Supplementary Data 7의 top 50 gene) gene list가 우리 tumor scRNA-seq의 기존 marker gene set과 얼마나 겹치는지 빠른 overlap 분석 필요.
- `질문:` Zenodo repository에서 어떤 형태의 파일(h5ad, csv, etc.)로 데이터가 제공되는지 확인 — 우리 scanpy 파이프라인과의 호환성.
