# Lens — Industry — sun-2025-hepatology-ctc-plt
> PDF-based full analysis. 이전 abstract-only 분석을 overwrite. 2026-06-10.

---

## 1. Categorization

> 이 섹션은 paper-info.yaml의 categorization 블록과 동기화됨.

### Domain

- `CTC-biology` — immune evasion, PLT-CTC adhesion
- `immune-checkpoint` — CD155(PVR)-TIGIT axis
- `liquid-biopsy` — CTC-PLT complex as prognostic marker
- `NK-cell-immunology` — platelet-mediated NK-cell dysfunction
- `HCC-oncology` — hepatocellular carcinoma translational

### Use case

- **`pipeline-applicable`**: ChimeraX-i120 기반 CTC 분리 플랫폼 + CD41 co-staining으로 PLT+CTC 식별 방법론이 우리 파이프라인에 직접 적용 가능. CD155 발현 교차 분석 가능.
- **`academic-citation`**: PLT-CTC complex가 CD155-TIGIT 경유 NK-cell 면역 회피를 획득한다는 핵심 주장 및 수치(70% PLT+CTC, p = 0.011 CD155 연관)가 자기 논문 Introduction·Background에서 직접 인용 가능.
- **`commercialization-candidate`**: CD155+PLT+CTC 검출을 anti-TIGIT 치료 반응 예측 동반진단(CDx) 바이오마커로 개발하는 경로 존재.

### Importance

- **Level**: 상
- **Perspective**: HCC CTC의 NK-cell 면역 회피 기전을 FAK/JNK/c-Jun→CD155→TIGIT 축으로 분자 수준에서 규명한 연구. 우리 CTC 분리 플랫폼에서 PLT+CTC 식별에 직접 적용 가능하고, 위암 CTC 분석에서 CD155 발현 확인 분석의 인용 근거로 활용 가능.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: 임상 생존 분석 n = 20(PLT+CTC n = 14, PLT−CTC n = 6). PLT−CTC군이 극소수. 생존 분석 통계적 검정력 낮음. 단변량 분석이며 다변량 Cox 회귀 없음 → regulatory grade evidence로 부족.
- **Cohort 편향**: 단일 기관(Zhongshan Hospital, Fudan University, 상하이), 수술 절제 환자만 포함. 인종·병기·선행 치료 편향 존재. 중국 HCC 코호트 데이터를 다른 지역 또는 다른 암종으로 직접 외삽 주의.
- **Replication 부족**: HCC 단일 기관 코호트에서만 임상 예후 검증. 독립적 외부 코호트 검증 없음. 해석: replication 부족, regulatory grade evidence로 사용 불가.
- **Selection bias**: CTC 양성 환자만 분석 대상. CTC 음성 환자 군에서의 PLT 효과 없음. CTC 양성 선택이 이미 고 위험군을 농축할 가능성.
- **Multiple testing**: 본문에 다중 비교 보정(BH/Bonferroni) 명시 없음. Figure 5, 6의 다수 군 비교 결과 해석 시 false positive 리스크 감안.

### 2.2 임상·기술적 제약

- **CTC 분리 플랫폼 전용성**: ChimeraX-i120(저자 자체 개발 플랫폼, ref 16) 기반. 표준화된 공개 플랫폼이 아님. 외부 기관 재현 시 동일 플랫폼 접근이 필요하거나 대안 플랫폼 검증이 선행되어야 함.
- **혈액 처리 조건**: 원심 분리(900g)가 PLT를 부분 활성화시킬 가능성이 Supplemental S10에서 확인됨. 저자들은 이 부분적 활성화가 결과에 영향을 주지 않았다고 추가 실험으로 보이나, 임상 검체 처리 표준화 시 주의 사항.
- **NK-cell 분리**: 환자 혈액에서 magnetic separation으로 NK-cell 분리. 분리 효율 및 pure population 여부가 in vitro 기능 assay 결과에 영향 가능.
- **인간화 마우스 재현 실패**: 저자들이 Discussion에서 명시. 현재 시점에서 인간 NK-cell 생물학을 충실히 재현하는 in vivo 모델 부재 → IND/임상 개발 시 추가 human ex vivo 검증 필요.

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**: CD155+PLT+CTC 검출을 CDx 바이오마커로 개발하려면 IVD(in vitro diagnostics) pathway 해당. 분석적 검증(analytical validation: 정밀도, 정확도, LOD)과 임상적 검증(clinical validation: sensitivity/specificity for anti-TIGIT response prediction)이 모두 필요.
- **Analytical validation**: ChimeraX-i120 플랫폼의 CTC 회수율, CD41 염색 특이성, CD155 발현 정량 정밀도에 대한 analytical validation 데이터가 본 논문에 없음.
- **Clinical validation**: CD155+CTC가 anti-TIGIT 치료 반응 예측에 얼마나 유용한지에 대한 임상 데이터 없음. MORPHEUS-liver(NCT04524871) 같은 임상시험 샘플에서 검증 필요.
- **IRB / consent**: 연구 윤리위원회(Zhongshan Hospital Research Ethics Committee) 승인 및 모든 참가자 사전 동의 취득 명시. 헬싱키 및 이스탄불 선언 준수 명시.
- **Reproducibility for audit**: 소스 코드(R 4.0, FlowJo V10, GraphPad Prism 7 사용 명시)와 RNA-seq raw data(GSA-Human HRA007585)는 공개. 그러나 ChimeraX-i120 분석 workflow의 상세 재현 코드는 공개되지 않음.
- **GLP**: 동물 실험은 Fudan University 기관 가이드라인 및 국제(NIH AAALAC, Animal Welfare Act) 기준 준수 명시.

### 2.4 권위·신뢰 가중치

- **1차 출처**: 원저논문, peer-reviewed (Hepatology, AASLD 공식 저널, IF ~17, 간담췌 분야 top-tier). 미국간학회(AASLD) 공식 저널.
- **COI**: 저자들이 이해상충 없음 명시. 단, 공동저자 Chen Chen이 상하이 Dunwill Medical Technology 소속 → 간접 상업 관계 모니터링 권고.
- **Funding**: 국립자연과학기금(NSFC) 및 상하이시 보건위원회 등 공공 펀딩. Corporate 단독 후원 없음 → 결과 편향 리스크 낮음.
- **저자 트랙레코드**: Wei Guo, Yunfan Sun, Beili Wang, Wenjing Yang — Zhongshan Hospital 검사의학 및 간외과팀. Sun et al. 2021 Nat Commun(scRNA-seq CTC 연구, ref 14)의 연속 연구. 저자 그룹의 CTC 기술 전문성 높음.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자 자산화 가능성**: ChimeraX-i120 플랫폼이 저자 그룹의 자체 개발 CTC 검출 시스템. 상하이 Dunwill Medical Technology(공동저자 Chen Chen 소속)가 이 플랫폼과 연관 가능성. 라이선싱 또는 공동연구 대화 가능 대상.
- **공동연구 후보**: Zhongshan Hospital, Fudan University 간외과/검사의학 팀. scRNA-seq 기반 CTC 분석 역량 보유. NCCHE 위암 데이터셋과의 교차 분석 공동연구 제안 가능.
- **경쟁사 관찰**: TIGIT 차단 항체 개발사(Genentech/Roche tiragolumab, BMS vibostolimab, iTeos Therapeutics, Compugen)가 CTC CD155를 예측 바이오마커로 활용하는 방향으로 파이프라인을 발전시킬 가능성. 특히 MORPHEUS-liver 결과와 본 논문 연결 시 CTC-based CDx 기회 포착.
- **시장 영향**: anti-TIGIT 시장(2030년 예상 규모 수십억 달러급)에서 companion diagnostic 포지셔닝이 가능하면 높은 BD 가치.

### 3.2 Commercialization-candidate (자체 제품화)

- **제품 카테고리 후보**:
  - **Diagnostic (Dx/CDx)**: CD155+PLT+CTC 검출 assay → anti-TIGIT 치료 반응 예측 동반진단. 기술적 성숙도(TRL): 2–3 (proof-of-concept 단계, 임상 검증 전).
  - **Assay/Protocol**: PLT-CTC complex 분리 + CD155 IF 염색 표준화 프로토콜 → CRO 서비스 제공 가능.
  - **Liquid biopsy panel**: PLT+CTC 비율 + CD155 발현 + CD41 co-staining을 HCC 예후 패널 구성요소로 포함.
- **IP 자유도**: 현재 CD155-TIGIT axis 및 PLT-CTC 기전에 대한 특허 보유 여부 확인 필요. ChimeraX-i120 플랫폼의 특허 상태 확인 권고.
- **MVP 시나리오**: 자체 HCC 또는 위암 코호트에서 CD41+/CD155+ CTC 동시 검출 assay를 개발 → 기존 CTC 분리 장비(CellSearch, EpCAM-based) 대비 PLT+CTC 특이적 검출 패널 추가.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**: 우리 CTC 분리 플랫폼(ChimeraX 기반 또는 유사 EpCAM/CK 기반)이 CD41 공동 staining을 지원하면 즉시 적용 가능. NCCHE 위암 코호트 혈액 샘플에서 PLT+CTC 식별 → CD155 발현 교차 분석.
- **팀 역량**: CTC 분리·IF 스테이닝·flow cytometry 역량 보유. CD155 antibody(본 논문 Abcam ab21851 사용) 추가 구입으로 바로 시도 가능.
- **전략적 방향 align**: 우리 프로젝트의 CTC subtype 분류 정교화 및 ADC/면역치료 동반진단 CDx 개발 방향과 일치.
- **빠진 capability**: 위암 CTC에서 HCC 기전의 동일 적용 여부 확인을 위한 in vitro NK-cell coculture 실험(wet lab capacity 확인 필요).

### 3.4 후속 BD·제품 액션 후보

- **PLT+CTC CD155 발현 확인 분석 (내부)**
  - 누가: CTC 분석 담당(김가경 수석) + wet lab
  - 언제: 지금 (이번 스프린트, ~2주)
  - 자원: NCCHE 위암 PBMC/CTC 보관 검체 + CD41 항체(Abcam ab21851) + CD155 항체 추가 구입
  - 성공 기준: PLT+CTC 중 CD155+ 비율이 PLT−CTC 대비 유의하게 높음 확인

- **저자 그룹 공동연구 타진**
  - 누가: BD lead + 본인
  - 언제: 다음 분기
  - 자원: 이메일 컨택 (guo.wei@zs-hospital.sh.cn / sun.yunfan@zs-hospital.sh.cn)
  - 성공 기준: 위암 또는 다른 암종에서의 PLT-CTC CD155 기전 검증 공동연구 MOU 또는 협력 의향서

- **anti-TIGIT CDx 포지셔닝 내부 검토**
  - 누가: BD + regulatory 팀
  - 언제: 다음 분기 R&D 리뷰 시
  - 자원: MORPHEUS-liver trial 환자 샘플 접근 가능성 확인; tiragolumab 개발사(Genentech) CDx 파트너십 landscape 조사
  - 성공 기준: CD155+PLT+CTC CDx 개발 feasibility 보고서

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective**: PLT-CTC 면역 회피 기전의 분자 축을 처음으로 체계적으로 규명한 연구. HCC 임상 데이터 및 preclinical 검증 모두 포함. 우리 CTC 파이프라인에 직접 적용 가능성 높음.
- **등급 근거**:
  - PDF 전문 확인 결과, 임상 코호트(n = 20 생존 분석) + 3개 in vitro 시스템(cell line, PDO, coculture) + 2개 in vivo 모델(Balb/C, NPSG) + 환자 CTC IF의 단계적 검증 구조를 갖춤.
  - CD155-TIGIT axis의 특이성이 α-TIGIT vs. α-CD96 비교로 직접 증명됨.
  - ChimeraX-i120 플랫폼이 저자 자체 개발이지만, 우리 CTC 분리 체계(EpCAM/Pan-CK/CD45 기반)와 원리적으로 호환.
  - α-TIGIT preclinical 효과가 in vivo 전이 모델에서 통계적으로 유의하게 보임 → anti-TIGIT CDx 연계 가능성 명확.
  - 한계: 임상 코호트 소규모, 인간화 마우스 재현 실패, 다중 비교 보정 미적용 → 단독으로 regulatory 근거로는 부족. 후속 검증 필요.

### 4.2 활용 우선순위

- **지금**: NCCHE 위암 CTC 보관 샘플에서 CD41+CD155+ co-staining 분석 시작. PLT-CTC 논문 인용 추가(NCCHE 발표 배경 슬라이드).
- **다음 분기**: anti-TIGIT CDx 포지셔닝 검토. 저자 그룹 공동연구 타진.
- **장기**: CD155+PLT+CTC → anti-TIGIT 치료 반응 예측 CDx 개발 검토. 독립 외부 코호트 검증 확인 후.

### 4.3 발표·미팅에서 들이밀 시점

- **NCCHE 위암 CTC 발표**: Background에서 "혈소판 연관 CTC의 기능적 의미" 설명 시. PLT+CTC의 불량 예후 데이터(PFS p = 0.0257, OS p = 0.0459) 인용.
- **BD 미팅 (anti-TIGIT 개발사 또는 TIGIT CDx 논의)**: CD155+CTC 검출이 anti-TIGIT 치료 반응 예측 가능성 논의의 기초 근거.
- **사내 R&D 리뷰**: CTC subtype 분류 정교화(PLT+CTC 기능적 마커 추가) 제안 시 직접 인용.
- **외부 학회 발표 (액체생검/CTC 세션)**: "면역 회피 기능을 가진 CTC subtype"의 선행 데이터로 인용.

### 4.4 추가 탐색 필요 영역

- 질문: ChimeraX-i120 플랫폼이 특허 등록 또는 상업화된 제품인가? Dunwill Medical Technology와의 관계를 명확히 해야 외부 협력 가능성 평가 가능.
- 질문: NCCHE 위암 코호트 혈액 샘플에서 CD41(PLT 마커) 공동 staining이 현재 프로토콜에 추가 가능한가? 기존 panel에 항체 1개 추가 문제인지, 새 panel 설계 필요인지.
- 질문: MORPHEUS-liver(NCT04524871)에서 tiragolumab 반응 환자의 CTC CD155 상태 데이터가 공개된 것이 있는가? PubMed/ClinicalTrials 확인 필요.
- 질문: 동일 저자 그룹이 위암 또는 다른 암종에서 동일 기전을 검증 중인 후속 논문이 있는가? (Sun YF et al. 또는 Guo W 그룹 최신 preprint 확인 권고)
