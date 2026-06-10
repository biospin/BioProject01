# Lens — Industry
## nami-2021-her2-emt-silencing

---

## 1. Categorization

> 이 섹션은 paper-info.yaml의 categorization 블록과 동기화된다.

### Domain

- `HER2-targeted-therapy`
- `breast-cancer-epigenetics`
- `EMT-drug-resistance`
- `ADC-target-biology`

### Use case

- `academic-citation` — HER2 ADC 및 trastuzumab 내성의 chromatin-based epigenetic 기전을 기술할 때 background reference로 인용 가치 높음.
- `BD-opportunity` — EMT subpopulation의 HER2 소실을 epigenetic reversion으로 극복하는 병용 전략 또는 epigenetic biomarker 기반 patient stratification 관련 BD 논의에서 참조 자료.

### Importance

- **Level**: 중
- **Perspective**: HER2 ADC/CTC liquid biopsy 파이프라인에서 EMT-driven HER2 target loss의 생물학적 근거 문헌으로 인용 가치가 있으나, 공개 데이터 재분석 + 소규모 세포 실험 수준으로 mechanistic 완성도가 낮아 직접 파이프라인 적용보다는 background reference + hypothesis generation 용도.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size (세포주)**: ChIP-seq 비교 HER2-high n=5, HER2-low n=3 — 소규모. 통계 검정력 낮음.
- **Replication 부족**: BT474 EMT 실험(Dataset 7)의 replicate 수 미명시. 단일 실험 가능성.
- **Multiple testing**: METABRIC 24개 marker 동시 상관 분석에 FDR 보정 미적용. $R^2$ = 0.005–0.12로 효과 크기 작음.
- **Selection bias**: 비교에 사용된 cell line이 HER2 발현 스펙트럼의 양 극단(HER2-overexpressed vs. mesenchymal/HER2-negative)에 편중. 중간 HER2 발현 cell line 포함 분석 없음.
- **해석: ChIP-seq 비교에 정량 통계 없이 시각적 browser track 비교만 제시 — regulatory grade evidence로 부족. 세포주 기반 epigenomics 연구로 임상 적용 전 독립 validation 필수.**

### 2.2 임상·기술적 제약

- **Tissue/sample**: 공개 데이터 재분석 + 단일 cell line 실험(BT474). 환자 primary tumor 또는 CTC에서의 직접 검증 없음.
- **장비·시약**: ChIPbase, GEO, Cistrome, 4Dgenome, WashU Epigenome Browser — 모두 공개 무료 도구. 재현 장벽 낮음.
- **계산 자원**: ChIP-seq 재분석은 표준 bioinformatics 환경에서 가능. GPU 불필요.
- **EMT 유도 실험 재현**: BT474 + StemXVivo CCM017(R&D Systems) 15일 처리 프로토콜은 비교적 표준적이나, 세포 균질성(% EMT 전환 세포) 정량화 없음.

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**: 이 논문의 발견을 바탕으로 한 임상 적용이 있다면 Companion Diagnostics (CDx — HER2 chromatin status 기반 treatment stratification) 또는 IVD 형태. 현재는 기초 연구 수준으로 어떤 규제 pathway에도 진입하지 않았음.
- **Analytical / Clinical validation**: 없음. HER2 expression과 chromatin mark의 association은 세포주 수준. 임상 validation(sensitivity/specificity, PPV/NPV) 데이터 없음.
- **IRB / consent**: 인간 primary tissue 사용 없음. 공개 데이터(METABRIC) + 세포주. IRB not applicable.
- **GMP / GLP**: 해당 없음 (기초 연구).
- **Reproducibility for audit**: 사용 데이터 모두 공개 접근 가능(GEO accession, cBioPortal, Cistrome). 코드 미제공(분석 소프트웨어: cBioPortal web, TAC 3.0, Prism v.6, WashU Browser).

### 2.4 권위·신뢰 가중치

- **1차 출처**: Peer-reviewed journal (MDPI *Life*, impact factor 중하). Open access CC BY 4.0.
- **2차 출처**: ChIP-seq 데이터는 Franco et al. 2018(*Genome Research*) 등 고품질 공개 데이터셋 재사용 — 데이터 자체의 신뢰도는 높음.
- **Peer review**: 공식 peer review 거쳤으나 *Life*는 IF 낮은 MDPI 저널. 고영향력 학술지 검증은 미완.
- **COI**: 저자 선언 "no conflict of interest." CIHR 공공 펀딩.
- **저자 배경**: Nami는 이 그룹의 HER2 시리즈 논문(Cancers 2017, 2018, 2019 등) 제1저자로 HER2 signaling 전문성 있음. Wang(senior) = University of Alberta 시그널 전달 그룹.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자/기관 자산화 가능성**: 저자들이 startup 창업 또는 특허 출원 정보는 이 논문에서 미제공. 추정: 기초 연구 수준으로 바로 라이선싱 가능한 자산은 현재 없을 가능성 높음. 확인 필요.
- **공동연구 후보**: Wang 그룹은 HER2 biology 전문. Open access 공개 + Canadian CIHR 펀딩 — 공동연구 접근 가능성 있음. 다만 직접 연락 ROI가 높지 않음(기초 연구 수준).
- **경쟁사 관찰**: HER2 ADC(trastuzumab deruxtecan, T-DXd; DS-8201)를 개발하는 Daiichi-Sankyo/AZ, Genentech, Seagen/Pfizer 등이 EMT-driven HER2 loss를 주요 내성 기전으로 이미 인식하고 있음.
- **해석: 이 논문의 BD 가치는 직접적인 라이선싱보다 내부 R&D 및 BD 미팅에서 HER2 ADC 내성 기전 reference로 인용하는 것.**

### 3.2 Commercialization-candidate (자체 제품화)

- **Diagnostic (Dx) 가능성**: ERBB2 chromatin accessibility 또는 active histone mark(H3K27ac)를 HER2+ 유방암의 EMT 상태 + trastuzumab 반응 예측 바이오마커로 사용하는 아이디어. 그러나 현재 기술 성숙도 TRL 1–2(concept). 임상 검체에서 측정 가능성이 선행되어야 함.
- **Liquid biopsy (CTC/cfDNA)**: CTC에서 ERBB2 chromatin state를 측정하는 assay 개발 — 현재 기술적으로 도전적. CTC-ATAC-seq 기술(외부 맥락: Corces et al. 2016 등)이 존재하나, 임상 검체에서 CTC 수가 적어 sensitivity 문제.
- **Service / CRO**: EMT 상태와 HER2 chromatin의 bioinformatics 분석 서비스. 기술적으로 가능하나 시장 규모 불명확.
- **Therapeutic**: Epigenetic reversion으로 ERBB2 chromatin을 reopening → HER2 발현 회복 → trastuzumab re-sensitization. HDAC inhibitor + trastuzumab 병용이 직접적 치료 전략 후보. 그러나 이 논문은 이것을 직접 검증하지 않았다.
- **TRL**: 1–2 (proof-of-concept, in silico + cell line).

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**: 우리 파이프라인의 직접 데이터(HSPC 10x Multiome 등)와는 적용 영역이 다름(유방암 HER2 vs. HSPC epigenomics). 단, CTC/ADC liquid biopsy 파이프라인에서 EMT marker + HER2 expression 분석이 있다면 직접 관련.
- **자원 가능성**: 공개 데이터 재분석 위주이므로 우리 환경에서 재현 용이. ChIP-seq 데이터 재분석은 표준 bioinformatics 툴(deepTools, DiffBind 등)로 가능.
- **비용·시간**: 공개 데이터 재분석만이라면 1–2주. BT474 EMT 실험 재현은 세포 배양 + immunofluorescence 가능한 wet lab 필요(약 1개월, 세포주 확보 후).
- **ROI**: CTC liquid biopsy 파이프라인에서 EMT 상태와 HER2 발현의 연관을 background reference로 사용하는 것이 주요 ROI. 직접 알고리즘 차용보다 개념 framework reference.

### 3.4 후속 BD·제품 액션 후보

- **[1] CTC epigenomics assay 탐색]**
  - 누가: liquid biopsy 팀 + bioinformatics
  - 언제: 다음 분기
  - 자원: CTC-ATAC-seq 선행 논문 스크리닝 (1–2주)
  - 성공 기준: CTC에서 ERBB2 chromatin status 측정 가능성 검토 보고서

- **[2] HDAC inhibitor + trastuzumab 병용 내성 극복 문헌 정리]**
  - 누가: R&D 팀
  - 언제: 이번 달 내
  - 자원: PubMed 검색 + paper analysis (이 하네스 활용)
  - 성공 기준: EMT + epigenetic inhibitor 병용 전략의 임상 전/임상 데이터 summary 1페이지

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 중
- **Perspective**: HER2 ADC·liquid biopsy 파이프라인의 EMT-driven HER2 target loss 기전 reference로 인용 가치가 있으나, 기초 공개 데이터 재분석 + 소규모 세포 실험으로 mechanistic 완성도가 낮아 직접 적용보다 background reference 용도.
- **등급 근거**:
  - METABRIC n=1,904 임상 데이터에서 ERBB2-EMT 연관을 보인 것은 규모 면에서 강점이나 $R^2$ 0.005–0.12로 효과 크기 작음.
  - ChIP-seq 비교는 공개 데이터 시각적 비교 위주 — 정량 통계 없어 regulatory evidence 부족.
  - BT474 EMT + trastuzumab binding 실험이 핵심 functional claim이나 정량 데이터 미제공.
  - 발표 venue(*Life*, MDPI)가 고영향력 저널이 아님.
  - 그러나 HER2 내성 기전의 "chromatin architecture" 프레임을 공개 데이터로 종합한 개념 논문으로서 citation 가치는 있음.

### 4.2 활용 우선순위

- **지금**: CTC liquid biopsy R&D 보고서 또는 HER2 ADC 내성 기전 background 정리에서 citation 사용.
- **다음 분기**: HDAC inhibitor 병용 전략 관련 BD 미팅 자료 준비 시 참조.
- **장기**: EMT 상태 CTC의 ERBB2 chromatin status를 직접 측정하는 assay 개발 탐색이 가시화되면 다시 검토.

### 4.3 발표·미팅에서 들이밀 시점

- **HER2 ADC 내성 기전 R&D 리뷰**: EMT subpopulation에서 HER2 target loss의 chromatin 기전을 설명할 때 Figure 3D(schematic) 인용.
- **BD 미팅 (HER2 ADC 또는 epigenetic combination 파트너와)**: "60–70% trastuzumab de novo resistance"(p.2) 수치와 EMT → ERBB2 silencing 기전을 background data로 제시.
- **사내 newsletter / 동향 공유**: CTC liquid biopsy + HER2 epigenetics 동향 공유 시 참조.

### 4.4 추가 탐색 필요 영역

- 질문: Nami 그룹(Wang lab, Univ. Alberta)이 이 논문 이후 HER2 chromatin + HDAC inhibitor 병용 연구를 발표했는가? PubMed follow-up 확인 필요.
- 질문: T-DXd(trastuzumab deruxtecan) 내성 기전으로 EMT + HER2 loss가 실제 임상에서 보고된 사례가 있는가? Daiichi-Sankyo/AZ의 DESTINY 시리즈 clinical data 확인.
- 질문: CTC에서 ERBB2 promoter chromatin accessibility를 non-invasively 측정하는 기술(CTC-ATAC, EPIC-seq 등)의 현재 성숙도 확인 필요.
- 질문: ZEB1과 ERBB2 chromatin 사이의 direct regulatory link ($R^2 = 0.1260$이 가장 높음)를 mechanistic study로 확인한 후속 논문이 있는가?
