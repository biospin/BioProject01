# proszek-2025-adc-ctc-resistance — Lens: Industry

> 근거: `sources/proszek-2025-adc-ctc-resistance.pdf` (전문 PDF 기반 분석). Sledge GW et al. 2025, npj Breast Cancer.

---

## 1. Categorization

> 이 섹션은 paper-info.yaml의 categorization 블록과 동기화된다.

### Domain

- `ADC-resistance` — T-DXd(trastuzumab deruxtecan) 내성 기전 규명이 논문의 핵심
- `breast-oncology` — 전이성 유방암(HER2-positive, HER2-low, HER2-null) 코호트
- `multi-omic-profiling` — WTS + NGS + IHC/CISH 통합 분석
- `real-world-evidence` — 보험청구 데이터 + 다기관 종양 profiling 기반

### Use case

- `academic-citation` — T-DXd 내성 관련 논문 introduction, 내성 biomarker panel 설계 시 인용 가치 높음
- `BD-opportunity` — Caris Life Sciences의 다기관 real-world 데이터 자산; ABCC1 억제제 개발 pipeline 파악; AstraZeneca/Daiichi Sankyo의 T-DXd next-generation 전략 관찰

### Importance

- **Level**: 상
- **Perspective**: T-DXd 내성 biomarker(ABCC1 + ERBB2 조합)가 2,799명 실세계 코호트에서 검증됐으며, ADC 내성 기전 이해의 산업적 기준점이 됨. CytoGen의 ADC 파이프라인(SEV_BRCA, NCCHE_Gastric)에서 내성 예측 전략 수립의 직접 참조 자료.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: 전체 N=2,799. WTS 기반 분석은 n=1,714. 규모는 real-world T-DXd 데이터로는 최대 수준이나, post-T-DXd 샘플은 n=379로 pre-T-DXd에 비해 소규모.
- **Cohort 편향**: 미국 다기관이지만 Caris Life Sciences 플랫폼에 접근한 기관으로 한정 — 커뮤니티 병원보다 학술 의료센터 편향 가능성. 인종/민족 정보는 Supplementary Table S5에 일부 제시됐으나 representativeness 제한.
- **Replication 부족**: ABCC1 발현 biomarker가 독립 코호트에서 재현된 적 없음. TCGA 데이터에서 ABCC1 발현 분포 확인(Supplementary Fig. S3c)됐지만 T-DXd OS와의 연관성 독립 replication은 없음. 해석: replication 부족, regulatory grade evidence로는 부족.
- **Selection bias**: Post-T-DXd 샘플은 치료를 충분히 받은(생존 기간이 길었던) 환자에서 비율적으로 많이 채취됐을 가능성 — survivorship bias.
- **Multiple testing**: BH correction 적용됨(q<0.05). 96개 feature에 대한 체계적 correction. 유의.

### 2.2 임상·기술적 제약

- **Tissue/sample 가용성**: FFPE 종양 조직 필요 (WTS 최소 10% 종양 함량 요구). 전이성 유방암 환자에서 반복 생검 접근성이 제한됨.
- **장비·시약**: WTS: Illumina NovaSeq 6000 (60M reads); NGS: NextSeq 500 또는 NovaSeq 6000 (592 gene panel 또는 WES). 표준 NGS 인프라 보유 기관에서 재현 가능.
- **계산 자원**: WTS + NGS 분석은 STAR alignment, Salmon quantification 등 표준 bioinformatics pipeline. 특별한 GPU 자원 불필요.
- **Turnaround time**: 병원 검사 보고 기준 미제공. CAP/CLIA certified lab 기준으로 WTS 통상 2-3주. 임상 의사결정(real-time monitoring)보다 치료 전 선별에 더 적합.

### 2.3 규제·QA·RA 관점

- **Regulatory pathway**: ABCC1 RNA 발현을 T-DXd 처방 결정에 활용하려면 IVD(In Vitro Diagnostic) 또는 LDT(Laboratory Developed Test) pathway 통과 필요. 현재 FDA 규제 체계에서 WTS 기반 companion diagnostic 개발 경로 필요.
- **Analytical validation**: 이 논문에서 ABCC1 WTS assay의 analyticalvalidation(precision, accuracy, LOD) 데이터는 제공되지 않음. Biomarker로 임상 개발하려면 별도 analytical validation 수행 필요.
- **Clinical validation**: 이 연구는 retrospective, observational 설계. Prospective clinical trial(예: ABCC1 low/high 사전 선별 후 T-DXd 치료)이 regulatory grade clinical validation을 위해 필요.
- **IRB / consent**: 보험청구 데이터 + de-identified molecular data 사용. Declaration of Helsinki 준수, WCG IRB 면제(45 CFR 46.104(d)(4) — retrospective, de-identified). IRB 승인 상세 명시.
- **Reproducibility for audit**: Caris Life Sciences 독점 데이터로 외부 재현 어려움. 데이터 접근은 letter of intent 후 6개월 내 조건부 가능(저자 contact 필요). Code/pipeline은 RRID로 참조(STAR, Salmon 등 공개 툴 사용).

### 2.4 권위·신뢰 가중치

- **1차 출처**: npj Breast Cancer (Nature Portfolio), peer-reviewed. 신뢰도 높음.
- **Peer review**: 정식 peer-review 완료(Received Aug 1 → Accepted Nov 16 → Published Dec 20, 2025).
- **저자 이해상충(COI)**: 주저자 포함 7명이 Caris Life Sciences 직원 — Caris의 multi-omic profiling 플랫폼을 사용한 연구임을 감안하면 데이터 자체의 독립성 검토 필요. 다수 저자가 AstraZeneca, Daiichi Sankyo(T-DXd 제조사)와 consulting/advisory 관계.
- **Funding source**: Caris Life Sciences 후원 연구 — corporate-sponsored. 결과 방향(Caris 플랫폼의 가치 강조)에 대한 자체 검증 필요성 있음.

---

## 3. BD Value & 상용화 가능성

### 3.1 BD-Opportunity (외부 자산 정찰)

- **Caris Life Sciences 자산**: 이 논문은 Caris의 독점 데이터 자산과 multi-omic profiling 플랫폼을 기반으로 한다. Caris는 미국 최대 종양 molecular profiling 회사 중 하나로, T-DXd 내성 관련 데이터 확장 파트너십 또는 데이터 라이선싱 가능성 탐색 가치 있음.
- **ABCC1 억제제 파이프라인 파악 필요**: 저자들이 임상 가능한 ABCC1 inhibitor 개발의 필요성을 시사했으나, 현재 임상 단계 ABCC1 selective inhibitor는 없음. 이 공간에 진입하려는 신규 biotech이 있을 수 있음.
  - 질문: ABCC1 억제를 표방하는 임상 단계 화합물이 있는가? Tariquidar(P-gp inhibitor), Reversan 등 다른 ABC transporter inhibitor의 T-DXd 병용 가능성?
- **AstraZeneca / Daiichi Sankyo 전략 관찰**: T-DXd 원개발사 Daiichi Sankyo가 이 내성 기전을 어떻게 수용하는지 모니터링 필요. Next-generation T-DXd 또는 ABCC1 억제 병용 임상시험 추진 가능성.
- **경쟁사 관찰**: 다른 HER2 타겟 ADC 파이프라인(예: ZW49, MEDI4276 등)의 ABCC1 관련 내성 데이터 비교 필요.

### 3.2 Commercialization-Candidate (자체 제품화)

- **제품 카테고리 후보**:
  - *Diagnostic (Dx)*: ABCC1 RNA 발현 + ERBB2 RNA 발현 조합을 사전 선별 biomarker로 한 T-DXd companion diagnostic 패널. 현재 IHC 기반 HER2 검사에 RNA 발현 레이어 추가.
  - *Software (SW)*: 96개 pathway feature 기반 T-DXd 내성 위험 분류 알고리즘 — "ADC resistance score" 형태의 SaaS 모듈. Real-world 종양 profiling 데이터와 연계.
  - *Service*: CRO 서비스로 ADC 내성 기전 스크리닝 panel 제공 (유사 플랫폼을 CytoGen 자체적으로 구축 가능한지 검토).
- **기술적 성숙도 (TRL)**: TRL 3-4. ABCC1 biomarker의 proof-of-concept은 확인됐으나 analytical/clinical validation 미완. 상용화까지 최소 2-3년 개발 필요.
- **IP 자유도**: ABCC1 RNA 기반 T-DXd 내성 예측에 관한 patent가 Caris에 있을 가능성 있음 (확인 필요). WTS 방법론 자체는 공개 표준.
- **MVP 시나리오**: ABCC1 + ERBB2 RNA 발현을 기존 WTS 보고서에 추가 모듈로 통합 → 치료 전 "ADC efflux risk" flag 제공. Minimum investment는 threshold 설정 + 임상 파트너십.

### 3.3 우리 파이프라인과의 Fit

- **Dataset 호환**: CytoGen의 ADC target 분석(SEV_BRCA, NCCHE_Gastric)이 유방암 및 위암 환자를 포함한다면, WTS + NGS 기반 ABCC1/ERBB2 발현 분석이 기존 파이프라인과 직접 연결 가능. 단, 위암에서의 T-DXd(또는 유사 ADC) 내성 패턴이 유방암과 동일한지 검증 필요.
- **팀 역량**: WTS + Cox regression 분석은 현재 bioinformatics 팀으로 재현 가능. Caris 규모의 real-world 데이터 없음이 한계 — 사내 데이터 규모(수십~수백 케이스)로는 같은 분석이 underpowered.
- **전략적 방향과 align**: CytoGen의 ADC target validation 및 내성 기전 이해 방향과 align. 특히 TROP2/HER2 타겟 ADC 내성 모니터링에 직접 참조 가능.
- **빠진 capability**: Matched pre/post-ADC 조직 paired 샘플 확보가 없으면 논문 수준의 mutation enrichment 분석 불가. 전향적 샘플 수집 프로토콜 또는 기존 샘플 코호트 확보 필요.

### 3.4 후속 BD·제품 액션 후보

- **ABCC1 inhibitor 파이프라인 landscape 파악**
  - 누가: BD lead + 전임상 팀
  - 언제: 다음 분기
  - 자원: Cortellis/PharmaProjects database access, 미팅 2-3회
  - 성공 기준: 임상 단계 ABCC1 inhibitor 또는 병용 전략 보유 biotech 목록 확보

- **내부 ADC 코호트 ABCC1 발현 분석**
  - 누가: 본인 (bioinformatics) + 임상 데이터 담당자
  - 언제: 이번 분기 내
  - 자원: SEV_BRCA 또는 NCCHE_Gastric WTS 데이터 보유 여부 확인, Salmon TPM 재계산
  - 성공 기준: ABCC1 발현 분포 확인 + 치료 반응 데이터와 preliminary 연관성 분석

- **Caris 데이터 접근 문의**
  - 누가: BD lead
  - 언제: 장기
  - 자원: Letter of intent 작성, 저자(Joanne Xiu, jxiu@carisls.com) contact
  - 성공 기준: 데이터 공유 계약 또는 공동연구 agreement

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective**: T-DXd 내성의 실세계 large-scale 증거로서, ABCC1이 HER2와 독립적인 임상적으로 유의미한 내성 biomarker임을 처음 확립. ADC 내성 메커니즘 이해의 분기점이 되는 논문.
- **등급 근거**:
  - 2,799명 real-world 코호트 — T-DXd 내성 연구로는 최대 규모. Real-world OS와 molecular data 통합은 임상 decision-making에 직접적.
  - ABCC1이 HER2 IHC 카테고리와 독립적으로 예측력을 가진다는 발견 — 현재 HER2 IHC 기반 처방 기준을 보완할 biomarker로 개발 가능성.
  - ERBB2 + ABCC1 조합 분석에서 27.9개월 vs 11.2개월의 OS 차이 — 임상적으로 의미 있는 층화.
  - In vitro 결과(MK-571 + T-DXd 병용)가 치료 전략적 hypothesis를 제공.
  - 단, Caris Life Sciences 이해상충, unmatched comparison, HER2+ 세포주만 in vitro 검증이라는 한계로 "완전한" 근거보다는 강력한 hypothesis generation 단계.

### 4.2 활용 우선순위

- **지금 (이번 sprint)**:
  - 내부 ADC 코호트에서 ABCC1 발현 분포 확인 (WTS 보유 여부 전제).
  - BD 미팅에서 T-DXd 내성 biomarker 논의 시 이 논문의 데이터를 baseline으로 활용.
- **다음 분기**:
  - ABCC1 inhibitor 파이프라인 landscape 파악.
  - T-DXd 이후 ADC next-line 전략 문헌 review에 이 논문의 mutation data(ERBB2, NFE2L2/KEAP1, TOP1) 포함.
- **장기**:
  - ABCC1 RNA 기반 companion diagnostic 개발 가능성 탐색 — analytical validation 계획 수립.
  - Caris 또는 AstraZeneza/Daiichi Sankyo와의 공동연구 가능성 타진.

### 4.3 발표·미팅에서 들이밀 시점

- **사내 R&D 리뷰**: ADC target selection 및 내성 기전 presentation에서 ABCC1과 ERBB2 발현의 조합 예측력(Fig. 4d) 인용.
- **BD 미팅**: T-DXd 내성 모니터링 필요성을 강조할 때 "2,799명 코호트에서 ABCC1이 HER2-independent 내성 biomarker"로 brief 논거.
- **학회 발표**: ADC resistance mechanism overview slide에 Fig. 1(9단계 경로도)과 Fig. 2(bubble chart + KM curves) 활용.
- **사내 newsletter**: ADC 파이프라인 관련 monthly update에 "T-DXd 내성 기전 landscape" 항목으로 포함 가치 있음.

### 4.4 추가 탐색 필요 영역

- 질문: Caris Life Sciences 플랫폼 외 다른 cohort(예: TCGA BRCA, METABRIC)에서 ABCC1 발현과 ADC 치료 결과 연관성이 재현된 데이터가 있는가?
- 질문: ABCC1-selective clinical inhibitor 개발 현황 — Tariquidar, Reversan 등 기존 ABC transporter inhibitor의 T-DXd 병용 임상시험이 진행 중인가?
- 질문: 이 논문의 SMAD4 mutation 농축(q<0.0005)이 T-DXd 내성에서 어떤 역할인가? Discussion에 설명 없음 — follow-up literature search 필요.
- 질문: 위암(NCCHE_Gastric) 또는 다른 HER2-positive 고형암에서도 ABCC1이 T-DXd 내성 biomarker로 작동하는가? 현 논문은 유방암 한정.
- 질문: Daiichi Sankyo의 T-DXd next-generation ADC 또는 ABCC1 관련 내성 극복 전략 patent 또는 pipeline이 있는가?
