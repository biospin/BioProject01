# Lens — Industry
# sun-2022-gastric-tme-scrna (@sun2022gastrictme)

---

## 1. Categorization

> paper-info.yaml의 categorization 블록과 동기화됨.

### Domain

- single-cell-genomics
- tumor-microenvironment
- gastric-cancer
- T-cell-biology
- cell-cell-communication

### Use case

- `academic-citation` — 위암 TME 대규모 atlas로 관련 분야 논문 introduction·background 인용 가치 높음. Tc17·TASC·Mφ_APOE 클러스터 정의와 수치가 인용 후보.
- `methodology-reference` — CellPhoneDB L-R 분석 파이프라인, Morisita-Horn similarity index 기반 clonotype 이동 정량, MuSiC deconvolution + TCGA-STAD 예후 연계 분석 워크플로우가 재사용 가능.
- `BD-opportunity` — Tc17 세포 타겟팅(IL-17/IL-22/IL-26 축, NECTIN2-TIGIT axis) 파이프라인 관찰; TASC 예후 마커로서 Fib_1/SMC_1 signature 활용 가능성.

### Importance

- **Level**: 중
- **Perspective**: 위암 TME의 가장 큰 paired scRNA-seq atlas로 조직-측(tissue-side) reference 가치가 있으나, 단일 기관 10명·중국 Beijing 코호트 한계로 임상 적용 ROI는 제한적. ADC 타겟 발굴 및 TME 상호작용 분석 워크플로우 차용에 집중.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: 10명 코호트 — 통계적으로 소규모. TCGA-STAD (n = 375) 연계로 예후 분석을 보강했으나, deconvolution 기반 간접 추정이므로 direct sequencing 결과보다 신뢰성 낮음.
- **Cohort 편향**: 단일 기관(Tsinghua-NCC, Beijing), 단일 인종(Chinese), 수술절제 가능 치료 미경험 위암 환자에 한정. 서양인 코호트, MSI-H 아형, 진행성·재발성 위암에서 같은 패턴이 재현될지 불확실.
- **Replication 부족**: TASC 예후 연관성을 독립 scRNA-seq 코호트에서 검증하지 않음. MuSiC deconvolution 기반 HR 추정값(1.8)은 단일 관찰 결과.
- **Selection bias**: 내시경생검이 아닌 수술절제 조직 위주. 생검 가능한 임상 샘플과 세포 구성이 다를 수 있음.
- **Multiple testing**: DEG에는 adjusted p-value 기준 적용, L-R permutation 1,000회 사용. 그러나 다중 세포 유형 쌍×L-R 쌍 조합에서 별도 FDR 보정 여부가 Methods에 명시되지 않음.
- **해석**: 개별 발견(특히 Tc17 trajectory, L-R interaction)은 탐색적 가설 생성 수준이며, 규제 grade 증거로 사용하기에는 replication 부족.

### 2.2 임상·기술적 제약

- **Tissue/sample 가용성**: 신선 수술절제 조직이 필요. 생검 또는 액체생검(CTC, ctDNA) 기반 접근으로 확장하기 어려움.
- **장비·시약 가용성**: 10x Chromium 5' scRNA-seq + V(D)J profiling — 일반 임상 병리 세팅에서 루틴 적용 어려움. 전문 core facility 필요.
- **계산 자원**: SCENIC(GENIE3) + RNA velocity + CellPhoneDB 통합 파이프라인은 고사양 서버(RAM 128GB+ 권장, 병렬화 필요) 환경 필요.
- **Turnaround time**: 전체 분석 파이프라인 1~2주 수준. 임상 실시간 의사결정에 부적합.

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**: 본 연구의 발견을 바탕으로 개발하려는 제품 유형에 따라 다름. 예:
  - TASC signature를 예후 바이오마커로 활용 → IVD/LDT pathway.
  - IL-17 중화 항체 + 위암 적응증 → IND/BLA pathway; IL-17 표적 항체는 이미 PsA/AS에서 승인된 사례 있음(외부 맥락).
  - NECTIN2-TIGIT 차단 병합요법 → IND 필요, TIGIT 억제제 임상 개발 진행 중인 타사 파이프라인 참조 필요.
- **Analytical / Clinical validation**: 본 연구에 없음. Biomarker 개발 시 analytical validation(정밀도/LOD) 및 clinical validation(sensitivity/specificity/PPV/NPV) 별도 필요.
- **GMP / GLP**: 해당 없음(기초 연구).
- **IRB / consent**: 독립 윤리위원회(National Cancer Center/Cancer Hospital 및 Tsinghua) 승인, 모든 환자 서면 동의 획득 명시(Methods p14).
- **Reproducibility for audit**: 원시 데이터 BIG Data Center HRA000704, 처리 행렬 OMIX001073, 코드 github.com/Lan-lab/sc-GC 공개. FDA audit 수준의 version 관리·validation 절차는 없음.

### 2.4 권위·신뢰 가중치

- **1차 출처**: Nature Communications (peer-reviewed, CC BY 4.0).
- **Peer review**: Andrea Cossarizza, Kyung-Hee Chun 등 외부 리뷰어 검토 완료 (peer review report 공개).
- **이해상충 없음**: 저자들 "no competing interests" 선언.
- **Funding**: NSFC, National Thousand Young Talents Program, China Postdoctoral Science Foundation, Tsinghua-Peking Joint Center — 공공 재원, 사기업 sponsorship 없음.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자/기관의 자산화 가능성**: 교신저자 Xun Lan (Tsinghua University MOE Key Lab of Bioinformatics). 현재까지 알려진 startup 창업 여부 미확인 — 직접 LinkedIn/Crunchbase 확인 필요.
- **공동연구 후보**: Yantao Tian (CICAMS, National Cancer Center). 중국 최대 암 센터 기반으로 위암 임상 샘플 접근성 높음. 중국-한국 공동연구 프레임워크(NSFC-NRF) 활용 가능성.
- **경쟁사 관찰**: Genentech(Roche), AstraZeneca, MSD 등이 PD-1/CTLA-4 위암 병합 임상을 진행 중. IL-17 타겟(secukinumab, ixekizumab) 위암 적응증 확장 여부는 별도 모니터링 필요.
- **시장 영향**: 위암 scRNA-seq atlas 분야에서 reference 데이터셋으로 자리잡을 가능성 있음 — ADC 타겟 discovery 시 tissue-side TME reference로 인용 가치.

### 3.2 Commercialization-candidate (자체 제품화)

- **제품 카테고리 후보**:
  - **Diagnostic (Dx)**: TASC (Fib_1/SMC_1) gene signature → 위암 예후 예측 패널. TRL 2-3 (proof-of-concept 수준).
  - **Software (SW)**: CellPhoneDB + SCENIC + MuSiC 통합 TME 분석 파이프라인 → SaaS 형태 제공 가능성. TRL 3-4.
  - **Therapeutic target**: IL-17 axis (Tc17) + NECTIN2-TIGIT + IL34-CSF1R → 병합 면역요법 타겟 후보. TRL 1-2 (hypothesis 수준).
- **IP 자유도**: 본 논문 자체는 open access CC BY 4.0. 해당 타겟(TIGIT, NECTIN2) 관련 IP는 Bristol-Myers Squibb, Genentech, Merck 등에 다수 특허 존재 — 독자적 IP 전략 필요.
- **MVP 시나리오**: TASC signature (Fib_1 + SMC_1 marker gene panel, n = 20~50 genes) → RT-qPCR 또는 NanoString 기반 예후 검사키트. TCGA-STAD + 독립 코호트 검증으로 LDT 수준 시제품 가능.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**: 본 논문은 위암 scRNA-seq (10x Chromium 5', n = 166,533세포). 우리 주력 데이터셋은 BRCA(SEV_BRCA)/위암(NCCHE_Gastric) — 위암 데이터셋에 직접 비교 reference로 활용 가능.
- **팀 역량**: CellPhoneDB·scVelo·SCENIC 파이프라인은 본 팀의 scRNA-seq 분석 역량으로 재현 가능. SCENIC의 계산 부담(RAM 128GB+)은 현재 서버 환경 확인 필요.
- **전략적 방향**: ADC 타겟 발굴 (tissue-side TME 특성 파악) 및 CTC-tissue 비교 분석에서 tissue reference atlas로 활용 가능. 직접적 epigenetic therapy lag 연구와의 관련성은 낮음.
- **빠진 capability**: 공간 transcriptomics 데이터 생산 (Visium/Xenium) — 본 논문의 한계이자 우리도 현재 없음. 협력 기관 물색 또는 공개 데이터 활용 필요.

### 3.4 후속 BD·제품 액션 후보

- **NCCHE_Gastric 데이터셋에 CellPhoneDB 분석 적용**
  - 누가: 담당 분석자(김가경) + NCCHE_Gastric 데이터 보유자
  - 언제: 다음 분기
  - 자원: NCCHE 위암 scRNA-seq 데이터, 이 논문 방법론 참조, 서버 RAM 128GB+
  - 성공 기준: TASC-TAM-LAMP3+ DC 상호작용 허브가 NCCHE 데이터에서도 재현되는지 확인

- **TASC gene signature → NCCHE_Gastric 예후 연관성 검증**
  - 누가: 담당 분석자
  - 언제: 다음 분기
  - 자원: NCCHE 임상 데이터(생존 정보), Fib_1+SMC_1 marker gene 패널(Supplementary Data 3 참조)
  - 성공 기준: 이 논문의 HR 1.8 결과가 NCCHE cohort에서 방향 일치 여부 확인

- **Xun Lan 연구실 공동연구 打診**
  - 누가: BD lead
  - 언제: 장기
  - 자원: 미팅 1회
  - 성공 기준: NCCHE 위암 데이터 비교 분석 협력 가능성 탐색

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 중
- **Perspective**: 위암 TME 최대 규모 matched scRNA-seq atlas이며, tissue-side ADC 타겟 reference 및 CellPhoneDB 기반 TME 상호작용 분석 methodology reference로 활용 가치 있다. 단일 기관 소규모 코호트 한계로 임상 개발 직결 증거로는 부족.
- **등급 근거**:
  - 166,533세포, 삼중 matched 설계는 현재까지 GC scRNA-seq 중 가장 큰 규모 (2022년 기준).
  - TASC 예후 연관성(HR 1.8)을 TCGA-STAD에서 deconvolution으로 확인했으나, 독립 scRNA-seq 코호트 검증 부재.
  - Tc17→exhaustion alternative trajectory는 흥미로운 가설이나 in vivo 검증 없어 mechanistic novelty가 제한적.
  - CellPhoneDB + SCENIC + MuSiC + Morisita-Horn 통합 분석 파이프라인은 우리 NCCHE_Gastric 분석에 직접 참조 가능.
  - Nature Communications 게재, peer review 리포트 공개, data fully accessible (HRA000704, OMIX001073).

### 4.2 활용 우선순위

- **지금**: CellPhoneDB 분석 워크플로우 참조 → NCCHE_Gastric 데이터 적용 계획 수립.
- **다음 분기**: TASC gene signature를 NCCHE_Gastric 데이터에 적용해 예후 연관성 재현 여부 확인.
- **장기**: 위암 외 고형암(BRCA) TME에서 TASC 유사 클러스터 비교 분석. Tc17 타겟 치료 파이프라인 모니터링.

### 4.3 발표·미팅에서 들이밀 시점

- **사내 R&D 리뷰 (ADC 타겟 발굴)**: TASC(CAF/SMC)와 Mφ_APOE가 GC TME 상호작용 허브라는 점 → ADC 타겟으로 기질세포·대식세포 아형 검토 시 reference.
- **학회 발표 (scRNA-seq TME 분야)**: Fig. 6m (cytolytic vs. Tc17-exhaustion trajectory 비교) — T세포 소진 경로 다양성 설명 시 슬라이드 인용.
- **사내 newsletter / 동향 공유**: 위암 scRNA-seq 분야 최신 동향으로 공유 가능.

### 4.4 추가 탐색 필요 영역

- 질문: 이 논문의 TASC gene signature (Fib_1: FAP, MMP3, IL11, IL24; SMC_1: ACTA2, MYH11, INHBA 등)가 NCCHE_Gastric 데이터에서도 동일한 클러스터를 형성하는가? Supplementary Data 3 기반으로 확인 필요.
- 질문: Xun Lan 연구실이 후속 위암 scRNA-seq 논문(공간 transcriptomics 포함)을 발표했는가? bioRxiv 모니터링 필요.
- 질문: NECTIN2-TIGIT axis 차단 임상 시험(tiragolumab + atezolizumab 등)에서 위암 subgroup 결과가 있는가? 임상 데이터 확인 후 L-R 분석 결과와 연결.
- 질문: 본 논문의 L-R interaction pairs(Supplementary Data 6)에서 우리가 관심 갖는 ADC target (예: HER2, CLDN18.2, FGFR2)과 연관된 L-R 쌍이 있는가? 직접 확인 필요.
