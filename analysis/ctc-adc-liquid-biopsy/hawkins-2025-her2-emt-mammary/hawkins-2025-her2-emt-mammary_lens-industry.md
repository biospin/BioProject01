# Lens — Industry
# hawkins-2025-her2-emt-mammary

> 근거: 전문 PDF `sources/hawkins-2025-her2-emt-mammary.pdf` (12 pages). 본 분석은 PDF 원문에 기반하며 abstract 기반 이전 버전을 덮어씀.

---

## 1. Categorization

> 이 섹션은 paper-info.yaml의 categorization 블록과 동기화된다.

### Domain (자동 추출, 검토 표시)
- `breast-oncology`
- `EMT-biology`
- `HER2-ADC-resistance`
- `epigenomics` (mechanism은 미규명 — 제목 사용 용어 기준)

### Use case (vocabulary 6개 중 해당)
- `academic-citation` — HER2 ADC 내성 기전 맥락에서 EMT-driven HER2 silencing의 in vivo 최신(2025) 직접 증거로 인용 가치 높음.
- `BD-opportunity` — HER2 ADC(T-DM1·T-DXd) 치료 내성 메커니즘에 관심 있는 제약사(Daiichi-Sankyo 등)와의 BD 미팅 맥락에서 활용 가능. "CTC에서 HER2 발현 소실 실시간 모니터링" 서비스 필요성 근거로 직접 제시.

### Importance (1개 종합 등급)
- Level: **중상** (내부 기준 상/중/하에서 중에 가까운 상)
- Perspective (1문장): CTC·ADC 파이프라인에서 HER2 발현 동적 소실의 in vivo 근거로서 academic-citation 및 BD 미팅 활용 가치 높으나, 소표본(n=5 MC cases)·epigenetic 기전 미규명·특화 저널 게재로 직접 파이프라인 적용 ROI는 제한.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: HER2 증폭 MC 5 cases — 핵심 결과(Table 1)가 소표본. 100 cases MC 코호트에서 5–10%가 HER2 증폭이므로 5–10 cases는 구조적 상한. 전체 IDC·IBC·MC 300 cases는 대규모이나 핵심 결론은 5 cases에 집중.
- **p-value 미제공**: "All stated or calculated differences implied differences of statistical significance"라고 기술하지만 구체적 수치 없음. 독립 평가 불가. 해석: regulatory grade evidence로 사용하기 어려움. 탐색적·생물학적 근거로만 활용.
- **Cohort 편향**: MC는 희귀 아형 — 기관 집중 편향 가능. Meharry Medical College 및 Ohio State University 코호트 (미국 남부·중서부 기관). 인종 다양성 및 HER2 IHC/FISH 판정 기관간 변이 미제공.
- **Single cohort replication 부재**: 결과가 단일 코호트에서만 검증. 독립 기관 재현 없음. 해석: replication 부재, regulatory grade evidence로 부족.
- **Multiple testing**: 100 ROI × multiple genes × multiple groups에서 BH/Bonferroni correction 명시 없음.

### 2.2 임상·기술적 제약

- **조직 접근성**: LCM(Pixcell II Laser Capture Microdissection 788)은 전문 장비. MC 조직 확보 자체가 희귀 아형이라 제약. 신선 냉동 + 파라핀 절편 양쪽 필요.
- **FISH 장비**: Zeiss epifluorescence + HER2 FISH probe(Vysis Spectrum Orange). 표준 분자병리 장비이나 특수 프로브 비용 발생.
- **세포주 실험 재현성**: HTB20(BT-474) ATCC 구매 가능. TGFβ1 + serum starvation 조합 프로토콜은 공개. 단일 세포주 한계는 재현 시 추가 세포주 실험 필요.
- **임상 적용 turnaround**: 현재 연구는 기초 연구 수준 — 임상 진단에 직접 적용하려면 standard of care 수준의 validation 필요.

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**: 이 연구 자체는 기초 연구. HER2 발현 소실 기전 연구로 IVD/LDT/SaMD 직접 연관성 없음. 단, 이 발견이 CTC 기반 HER2 모니터링 LDT의 science 근거로 사용될 때 FDA LDT guidance 맥락.
- **Analytical validation**: 없음 — 기초 연구. IHC/FISH의 정밀도·정확도·LOD 데이터 없음.
- **IRB 승인**: 복수 기관 IRB 명시 (Ohio State 2006C0042, UCLA, Nevada IACUC, Meharry). 인체 조직은 retrospective + de-identified로 exempt from Human Subject review. 적절히 처리됨.
- **GMP/GLP**: 해당 없음 — 기초 연구.
- **Reproducibility for audit**: 표준 시판 시약·장비 사용. 코드/데이터 공개 없음 (No datasets generated or analysed 명시). 프로토콜은 방법 섹션에 충분히 기술되어 있어 재현 가능.

### 2.4 권위·신뢰 가중치

- **출처**: 1차 출처 — peer-reviewed original research article.
- **Peer review 여부**: Received 1 April 2025, Accepted 4 August 2025. 정식 peer review 완료.
- **저널 수준**: Journal of Mammary Gland Biology and Neoplasia — 유방암·유방 생물학 특화 저널. Nature/Cancer Research 급 IF는 아니나 해당 분야 전문지. 개방 접근(CC BY-NC-ND 4.0).
- **저자 이해상충 (COI)**: "The authors declare no competing interests." Hoffman RM은 AntiCancer, Inc.(San Diego) 소속 — 이 기관이 PDX 연구(Mary-X)를 수행하는 상업 기관. COI 명시 없지만 주의.
- **Funding source**: DoD Breast Cancer Research Program + NIH + Meharry Medical College 공공 지원. 상업 편향 낮음.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자/기관 자산화 가능성**: Barsky SH (Meharry Medical College) — metaplastic carcinoma 분야 선도 연구자. 관련 특허 보유 여부 확인 필요 (USPTO 검색 권장). 기관 기술이전실(TTO) 통해 라이선싱 협상 가능한지 미확인.
- **공동연구 후보**: Barsky SH 그룹은 MC 연구의 희귀 speciality. CTC 분석 플랫폼 제공 + Barsky 그룹의 in vivo 조직 접근성 결합 시 synergy 가능. Email: sbarsky@mmc.edu (논문 공개).
- **경쟁사 관찰**: Daiichi-Sankyo/AstraZeneca (T-DXd 개발사)가 EMT-driven HER2 silencing 기전에 주목하고 있는지 — 공개 pipeline/investor day 자료에서 확인 필요. CARIS, Foundation Medicine 등 CGP 기업이 HER2 expression vs. amplification discordance를 liquid biopsy에서 다루는지 확인.
- **시장 영향**: HER2 ADC 시장(T-DXd 매출 2023년 ~$2B 이상) — HER2 발현 모니터링 수요는 실질적. 이 논문이 "발현 모니터링 필요성"의 과학적 근거를 강화.

### 3.2 Commercialization-candidate (자체 제품화)

- **제품 카테고리 후보**:
  - **Diagnostic (Dx)**: "EMT-score + HER2 expression 동시 측정 CTC 분석 패널" — HER2 ADC 치료 중 HER2 발현 소실 조기 감지. CTC liquid biopsy 서비스 또는 kit.
  - **Software (SW)**: EMT-ERBB2 correlation scoring algorithm — scRNA-seq CTC data에서 HER2 silencing risk index 계산.
  - **Service (CRO)**: HER2 증폭 유방암/위암 환자 CTC 반복 채혈 + EMT·HER2 발현 종단 모니터링 서비스.
- **기술적 성숙도 (TRL)**: TRL 3–4 (proof-of-concept, laboratory validation). 임상 샘플(CTC)에서의 직접 적용은 별도 validation 필요.
- **IP 자유도**: "EMT → HER2 silencing" 개념 자체는 Nami 2021 + Hawkins 2025로 선점. CytoGen 독자 알고리즘 또는 CTC 분석 프로토콜은 특허 가능 영역.
- **MVP 시나리오**: SEV BRCA 코호트 CTC scRNA-seq에서 ERBB2 mRNA vs. EMT score 음의 상관 재확인 → 소규모 clinical dataset 발표 → HER2 ADC 치료 중 CTC EMT-ERBB2 모니터링 feasibility study.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**: SEV BRCA 코호트에 HER2 양성 환자 포함 여부 확인 필요. CTC scRNA-seq으로 ERBB2 mRNA 및 EMT score 산출 — 현재 파이프라인에서 가능.
- **팀 역량**: scRNA-seq 분석, EMT score 계산(epithelial/mesenchymal gene signature) — 현재 파이프라인에서 수행 가능. Wet lab 추가(CTC 분리 후 IHC/FISH 확인)는 외부 협력 필요.
- **전략적 alignment**: CTC-ADC liquid biopsy 분야의 핵심 문제("원발 종양 HER2+인데 CTC에서는 왜 발현이 다른가")에 직접 해답 제공. Surfaceome·ADC target 분석과 연결 가능.
- **빠진 capability**: HER2 IHC/FISH를 CTC 단위에서 수행하는 wet lab capability. 현재 scRNA-seq mRNA 수준 분석이 primary.

### 3.4 후속 BD·제품 액션 후보

- **SEV BRCA EMT-ERBB2 상관 분석 (internal)**
  - 누가: 김가경 (본인) + 분석팀
  - 언제: 지금 (이번 sprint)
  - 자원: SEV BRCA scRNA-seq CTC data + EMT gene signature + ERBB2 mRNA 비교
  - 성공 기준: EMT score 상위 CTC에서 ERBB2 mRNA 유의한 감소 확인

- **Daiichi-Sankyo BD 미팅 자료 보강**
  - 누가: BD lead + 김가경 (technical slide 준비)
  - 언제: 다음 BD 미팅 전
  - 자원: Hawkins 2025 + Nami 2021 + 자체 CTC 결과 삼각 슬라이드 1장
  - 성공 기준: "CTC HER2 발현 소실 모니터링 필요성" 메시지 수용

- **Barsky SH 그룹 contact (공동연구 타진)**
  - 누가: 본인 or PI
  - 언제: 다음 분기
  - 자원: Email 1통 (sbarsky@mmc.edu)
  - 성공 기준: 공동연구 관심 여부 확인

---

## 4. 전문가 코멘트

### 4.1 종합 등급 (Importance 재인용 + 풀어쓰기)

- **Level**: 중상
- **Perspective**: CTC·ADC liquid biopsy 파이프라인에서 HER2 발현 동적 소실의 in vivo 2025년 직접 증거.
- **등급 근거**:
  - 핵심 결과(Table 1)가 FISH 증폭 보존 + IHC 소실을 동일 조직 내에서 동시 확인 — 개념 증명으로서 compelling.
  - TGFβ1 세포주 실험이 인과성 방향을 지지 (HTB20 vs. MCF7 음성 대조 포함).
  - 단, n=5 HER2 증폭 MC cases, p-value 미제공, epigenetic 기전 미규명이 결론 강도를 제한.
  - 특화 저널(J Mammary Gland Biol Neoplasia) — high-impact 저널 대비 인용 파급력 낮음.
  - 2025년 최신 — Nami 2021(세포주)을 in vivo로 보강하는 역할. 두 논문 함께 인용 시 스토리 완결성 높음.

### 4.2 활용 우선순위

- **지금 (이번 sprint)**: SEV BRCA CTC scRNA-seq에서 ERBB2 vs. EMT score 상관 분석. BD 미팅 데크에 Hawkins 2025 citation 추가.
- **다음 분기**: Daiichi-Sankyo BD 미팅 슬라이드에서 3-논문 삼각 인용 (Jordan 2016 + Nami 2021 + Hawkins 2025) 구성. Barsky SH 그룹 contact.
- **장기**: MC specific이라는 한계로 인해 일반 유방암·위암 CTC에서 같은 패턴 확인되어야 파이프라인 확장. 현재는 academic-citation + BD 논거로만 활용.

### 4.3 발표·미팅에서 들이밀 시점

- **BD 미팅 (Daiichi-Sankyo 등 HER2 ADC 개발사)**: "원발 종양 HER2 FISH 양성이어도 EMT-high CTC에서 HER2 단백질이 소실된다는 2025년 in vivo 직접 증거" 로 CTC 모니터링 서비스 필요성 강조.
- **사내 R&D 리뷰**: CTC-ADC 파이프라인에서 HER2 발현 소실 tracking의 과학적 근거 제시. Surfaceome 분석 전략의 배경 설명.
- **외부 컨퍼런스 / 키노트**: CTC heterogeneity + ADC target dynamics 맥락에서 인용.

### 4.4 추가 탐색 필요 영역

- 질문: USPTO에서 Barsky SH / Meharry Medical College의 HER2-EMT silencing 관련 특허 검색 필요.
- 질문: Daiichi-Sankyo의 최신 T-DXd investor day/pipeline 문서에서 EMT-driven resistance mechanism 언급 여부 확인.
- 질문: TCGA BRCA 데이터에서 MC subtype + HER2 amplified 샘플의 HER2 mRNA 수준이 실제로 낮은지 — 공개 bioinformatic validation 가능.
- 질문: CTC 분석 플랫폼 중 HER2 IHC/FISH를 CTC 단위에서 수행하는 업체(Veracyte, Epic Sciences 등) 현황 파악 필요.
