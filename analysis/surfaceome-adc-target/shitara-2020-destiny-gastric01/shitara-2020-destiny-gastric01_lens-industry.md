# Lens — Industry: shitara-2020-destiny-gastric01

---

## 1. Categorization

> paper-info.yaml의 categorization 블록과 동기화.

### Domain

- `oncology-gastric-cancer`
- `antibody-drug-conjugate`
- `HER2-targeted-therapy`
- `clinical-trial-RCT`

### Use case

- `BD-opportunity` — T-DXd(Daiichi Sankyo/AstraZeneca)가 HER2 ADC 시장의 核心 자산. 동반진단(HER2 IHC/ISH), ILD 모니터링 솔루션, 내성 biomarker 탐지를 중심으로 BD 포지션 기회.
- `regulatory-precedent` — DESTINY-Gastric01은 FDA/MHLW 가속승인 및 정식승인의 직접 pivotal 근거. regulatory pathway 벤치마크로 활용 가능.
- `commercialization-candidate` — HER2 ADC 동반진단(CDx) 개발, ILD 조기감지 SW, T-DXd 내성 biomarker 패널 — 세 방향의 상용화 후보.

### Importance

- **Level**: 상
- **Perspective**: HER2+ 위암 ADC 분야의 랜드마크 RCT. FDA 정식승인 및 NCCN 1차 권고의 regulatory evidence로, ADC platform/CDx/ILD 관리 솔루션 등 3개 방향 BD 기회를 직접 열어주는 자료.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: N=187 — Phase 2 규모. FDA는 Phase 2 결과 기반 가속승인을 허용했으나, 확증적 Phase 3 데이터 없이 단독으로 최종 승인의 충분한 근거가 되는지는 indication에 따라 다름. T-DXd는 이후 DESTINY-Gastric02(서양 코호트 단일군)로 확장.
- **Cohort 편향**: 일본·한국만의 환자군. 서양 환자(다른 식이, 유전적 다양성, 이전 치료 프로토콜 차이)에서의 재현성 불확실. 이후 DESTINY-Gastric02(서양 2차군)가 이를 부분 보완.
- **Replication 부족(이 시험 시점)**: 단일 Phase 2 RCT. OS 개선이 이 시험에서 처음 보인 것이므로, 확증적 재현이 없음. 해석: regulatory grade OS evidence로는 Phase 3 RCT가 필요한 수준이지만, FDA가 가속승인 후 정식승인으로 이어졌으므로 이후 규제 수용 가능.
- **후속 치료 불균형**: PC군(74%) vs. T-DXd군(48%)의 후속 치료 비율 차이가 OS 비교에 교란 요인. 이를 보정한 RPSFT(Rank Preserving Structural Failure Time) 분석 등이 이 논문에서 제시되지 않음.
- **Open-label**: Unblinded trial — objective efficacy(ORR via ICR)는 이를 부분 보완하나, PFS, QoL 측정은 bias 가능성 있음.

### 2.2 임상·기술적 제약

- **ILD 모니터링**: T-DXd 투약 시 ILD/pneumonitis 10% 발생. 실제 임상에서 CT 모니터링 주기, 폐 기능 검사, 호흡기내과 협진이 프로토콜 수준으로 관리되어야 함 — 병원 인프라에 따라 적용 가능성 격차.
- **HER2 동반진단(CDx)**: IHC/ISH 중앙 확인이 필요. 지역 검사와 중앙 검사 간 불일치율이 위암에서 알려져 있어(discordance ~20–30%) CDx 표준화 문제.
- **Dose (6.4 mg/kg)**: 유방암 승인 용량(5.4 mg/kg)보다 높아 골수억제(Grade 3 호중구감소증 51%) 부담이 크다. 위암 환자는 일반적으로 영양 상태·체력이 유방암 환자보다 떨어지므로 실제 임상에서의 dose intensity 유지가 도전.
- **장비·시약**: IHC/ISH 시행에 표준 pathology lab 수준이면 충분. T-DXd 자체는 cold chain 요구 IV infusion — 수준 높은 infusion center 필요.
- **Turnaround time**: CDx 결과는 1–2주 소요 일반적. 임상 의사결정 지연 최소화를 위한 신속 CDx 필요.

### 2.3 규제·QA·RA 관점

- **FDA pathway**: 2021년 1월 FDA 가속승인(HER2+ GC 2차 이상 치료). 이후 2023년 정식승인(5.4 mg/kg으로 용량 조정 포함). Pivotal evidence = DESTINY-Gastric01.
- **일본 MHLW**: 2021년 승인. 한국 MFDS도 이후 승인.
- **Analytical validation**: CDx로 Ventana PATHWAY anti-HER2/neu (4B5) IHC 키트가 companion diagnostic으로 FDA 승인. 임상시험에서 중앙 검토 기반으로 설계되어 실제 병원 검사 수행 가이드는 별도 CDx labeling 참조.
- **GLP/GCP**: 제약사(Daiichi Sankyo) 스폰서 + IRB 승인 + 환자 동의서 명시. 표준 임상시험 프로세스.
- **Safety reporting**: ILD adjudication committee 별도 운영 — 독립적 grading. CTCAE v5.0 기준.
- **Label·indication**: HER2 IHC 3+ 또는 IHC 2+/ISH+; 위·GEJ 선암; 이전 trastuzumab 포함 2가지 이상 치료. Label이 CDx 결과와 연동되어 있어 CDx 준수 없으면 off-label 사용.
- **Reproducibility for audit**: 프로토콜이 NEJM 부록으로 공개됨. 임상 데이터는 data sharing statement 있으나 원시 데이터 요청 형태 — FDA CDER audit 수준으로의 완전 공개는 제한적.
- **1차 출처**: NEJM peer-reviewed article + FDA prescribing information (Enhertu label) + ICH E9 통계 원칙.

### 2.4 권위·신뢰 가중치

- **Peer review**: New England Journal of Medicine — 최고 tier.
- **이해상충**: Daiichi Sankyo 스폰서; AstraZeneca가 데이터 해석 및 원고 검토 참여(2019년 협업 계약 이후). 전문 의학 writer 사용(sponsor 자금). 결과의 자체 검증 필요성 존재하나, 독립 중앙 검토(ICR)와 독립 통계 분석으로 부분 완화.
- **Funding source**: Corporate sponsored — 결과 방향이 스폰서에 유리. 외부 확증(DESTINY-Gastric02, real-world data)으로 보완 필요.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **T-DXd 자체(Daiichi Sankyo / AstraZeneca)**: 이미 Daiichi Sankyo와 AstraZeneca의 공동 개발·상업화. 라이선싱 창구는 사실상 닫혀 있으나, 특정 indication 확장(HER2 low GC, neoadjuvant 등) 또는 지역 파트너 기회는 존재 가능.
- **동반진단 시장**: HER2 IHC/ISH CDx. Roche Ventana(4B5), Dako HER2 FISH 등이 이미 시장에 있으나, 위암 특화 빠른 CDx(액체생검 기반 ctDNA HER2 CN)는 미개척 영역.
- **ILD 조기감지**: T-DXd 처방 환자에서 ILD를 조기에 탐지하는 AI 영상 분석(chest CT) 또는 혈청 biomarker(KL-6, SP-D 등) 솔루션 — 해당 marker가 위암 세팅에서 검증되지 않아 BD 기회 존재.
- **경쟁사 관찰**: Zymeworks(zanidatamab), BioNTech(BNT323, pan-HER2), MacroGenics(MCLA-128), Celldex(CDX-0159 없이 HER2로)가 위암 HER2 ADC 영역에 진입 중. DESTINY-Gastric01이 benchmark를 설정하여 후발주자가 이를 초과해야 함.

### 3.2 Commercialization-candidate (자체 제품화)

**후보 1: HER2 동반진단 (Dx)**
- 제품 카테고리: Dx / IVD
- TRL: 4–6 (IHC/ISH는 성숙, ctDNA HER2는 3–4)
- IP 자유도: 기존 IHC/ISH 키트와 차별화된 새 platform(cfDNA 기반, digital pathology AI) 필요
- MVP 시나리오: 기존 NGS panel에 HER2 CN/mutation 추가 + 조직 IHC와 correlation 분석 cohort study

**후보 2: ILD 모니터링 SW (SaMD)**
- 제품 카테고리: Software as a Medical Device (SaMD)
- TRL: 2–3 (AI CT 분석 연구 단계, T-DXd 세팅에서 검증 없음)
- IP 자유도: 기존 chest CT AI 회사(Imbio, Optellum 등)와의 경쟁 고려
- MVP 시나리오: T-DXd 처방 환자의 baseline + follow-up CT 데이터 수집 → ILD grade 예측 모델 학습 → 임상 utility 연구

**후보 3: T-DXd 내성 biomarker 패널**
- 제품 카테고리: Companion Dx / RUO panel
- TRL: 1–2 (내성 기전 불명확, 이 논문에 biomarker 데이터 없음)
- 자세한 분석은 향후 내성 시험 데이터 확보 후 가능

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**: CTC (Circulating Tumor Cell) 연구를 진행한다면, T-DXd 치료 환자의 HER2 발현 변화를 CTC로 추적하는 액체생검 응용 가능. 위암 환자 NCCHE_Gastric 데이터 활용 가능성.
- **팀 역량**: ADC 임상 해석, HER2 표적 분야 expertise가 있다면 DESTINY 시리즈 데이터를 기반으로 CDx 또는 ILD 솔루션 기획 가능. Wet lab 필요 없음(SW/Dx 방향이면).
- **전략적 방향**: surfaceome-adc-target 토픽과 직접 align. T-DXd가 어떤 HER2 발현 수준에서 최적 효과를 내는지를 surfaceome 관점에서 재해석할 수 있음.
- **빠진 capability**: 위암 환자 실제 임상 데이터(real-world), T-DXd 내성 기전 데이터.

### 3.4 후속 BD·제품 액션 후보

- **[HER2 liquid biopsy CDx 개발 파트너십 탐색]**
  - 누가: BD lead + 분자진단 파트너 (academic hospital pathology 또는 liquid biopsy startup)
  - 언제: 다음 분기
  - 자원: 파트너 미팅 2–3회, 기술 평가 1개월
  - 성공 기준: Co-development LOI 또는 데이터 공유 agreement

- **[ILD 조기감지 AI 시장 조사]**
  - 누가: 본인 + AI/imaging 파트너
  - 언제: 지금 (백그라운드 리서치 1–2주)
  - 자원: 공개 데이터 + 문헌 조사
  - 성공 기준: 기존 솔루션 gap 분석 + MVP 기술 스펙 초안

- **[NCCHE_Gastric 코호트에서 HER2 re-biopsy/ctDNA 연구 연계]**
  - 누가: 본인 + NCCHE 임상 파트너
  - 언제: 장기 (IRB 필요)
  - 자원: 임상 샘플 수집 프로토콜, ctDNA panel sequencing 비용
  - 성공 기준: 파일럿 환자 20명 이상 등록, HER2 ctDNA 데이터 확보

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective**: HER2+ 위암 ADC 치료의 landmark RCT — FDA 승인의 직접 pivotal evidence이며 ADC 분야 전체의 benchmark.
- **등급 근거**:
  - ORR 51% vs. 14%, OS HR 0.59 — 이전 HER2 표적제 모두 실패한 설정에서 두 primary/key endpoint 모두 통계적 달성.
  - T-DM1(ORR 20%, OS 실패) 대비 명확한 구조적 개선(DAR, payload, linker)을 임상 결과로 뒷받침.
  - NEJM 발표 + FDA 승인 + NCCN 1차 권고 — regulatory + clinical community 수용 최고 수준.
  - 가장 빠른 BD 경로는 동반진단 및 ILD 모니터링 솔루션. 이 두 분야에서 미충족 수요 명확.

### 4.2 활용 우선순위

- **지금**: ADC target 선정 근거 자료 및 BD pitch 슬라이드에 즉시 활용. DESTINATION-Gastric01 수치(ORR, OS HR, safety)를 ADC 플랫폼 presentation에 benchmark로 삽입.
- **다음 분기**: HER2 liquid biopsy CDx 파트너십 및 ILD 모니터링 솔루션 시장 조사.
- **장기**: NCCHE_Gastric 코호트 연계 및 T-DXd 내성 biomarker 연구 기획.

### 4.3 발표·미팅에서 들이밀 시점

- **BD 미팅 (ADC target 논의)**: "T-DXd가 HER2+ 위암 3차에서 ORR 51%, OS HR 0.59를 달성했고 이 뒤에는 IHC/ISH CDx와 ILD 모니터링이 unmet need로 남아있다" — 시장 진입점 논의에 직접 활용.
- **내부 R&D 리뷰 (surfaceome-adc-target 토픽)**: HER2가 surfaceome 표적으로 임상 검증된 gold standard임을 보여주는 근거.
- **학회 발표 / 논문 introduction**: ADC efficacy benchmark로 인용. "위암에서 trastuzumab deruxtecan이 이전 전략 대비 superior ORR을 보인 첫 RCT"라는 context에서.

### 4.4 추가 탐색 필요 영역

- 질문: T-DXd 승인 이후 real-world 데이터(ORR, OS, ILD 발생률)는 임상시험과 얼마나 다른가? 일본 NDB 또는 SPD(J-RWD) 데이터 확인 필요.
- 질문: ILD 예측 biomarker로 현재 어떤 후보가 개발 중인가? KL-6(Krebs von den Lungen 6), SP-D, 혈청 cytokine panel 중 T-DXd 세팅에서 검증된 것 확인.
- 질문: Daiichi Sankyo의 CDx 파트너(Roche Ventana 외)와 새로운 HER2 detection 협력 가능성 있는가? 최신 partnership 발표 확인.
- 질문: DESTINY-Gastric03 (1차 치료, T-DXd + ramucirumab + paclitaxel) 결과가 나왔는가? 확인 필요.
