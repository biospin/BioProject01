# Lens — Industry: drago-2021-adc-mechanism

## 1. Categorization

> paper-info.yaml의 categorization 블록과 동기화됨.

### Domain

- `ADC-oncology` — ADC 설계·기전·임상 전반
- `cancer-immunology` — Fc 효과기 기능, 면역요법 병용
- `oncology-clinical` — 임상시험 결과 및 환자 선택
- `drug-delivery` — 링커 기술, payload PK/PD, 종양 침투

### Use case

- `academic-citation` — ADC 설계 원리, 기전, 임상 수치의 표준 참고문헌. 어떤 ADC 관련 발표·논문에서도 인용 가능.
- `BD-opportunity` — 저자(Modi, Chandarlapaty)가 AstraZeneca/Daiichi Sankyo/Genentech 등과 consulting 관계 명시. 해당 파이프라인(T-DXd 등)의 BD 가치 평가에 직접 활용 가능한 레퍼런스.
- `regulatory-precedent` — FDA 승인 9종 ADC의 적응증·바이오마커 기준이 정리되어 있어 규제 전략 수립 시 reference 역할.

### Importance

- **Level**: 상
- **Perspective**: ADC 타겟 선정·링커-payload 설계·내성 기전·환자 선택 전략이 단일 문서에 통합된 현장 표준 리뷰. surfaceome-adc-target 타겟 우선순위 평가와 BD 발표 배경 자료로 직접 활용.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Cross-trial 비교 한계**: 리뷰가 제시하는 ORR 수치(T-DXd 60.9%, enfortumab 44% 등)는 다른 patient population, 선행치료 수, 측정 기준(IRC vs investigator)의 trial에서 나온 것이다. 숫자를 직접 비교하면 ADC 간 우열을 과도하게 단순화할 수 있다. BD 발표에서 수치 인용 시 trial heterogeneity를 반드시 병기.
- **내성 데이터의 대부분이 cell line**: §Resistance 섹션의 ABC transporter efflux, lysosomal dysfunction, antigen loss 근거는 "in vitro evidence largely unconfirmed in patients." 환자 조직에서의 전향적 내성 코호트 연구가 없어, 내성 예측 바이오마커의 임상 등급 근거로는 부족.
- **바이오마커 cut-off 미확립**: TROP2 IHC 기준, HER2 low 정의, gpNMB ≥5% vs ≥25% 등 여러 biomarker 분류의 cut-off 근거가 이 리뷰에서 정리되었으나 FDA-validated 정식 기준이 아님. 진단 검사 개발 시 별도 analytical validation 필요.
- **단일 기관 저자**: 3인 모두 MSKCC 소속. 임상 경험이 풍부하지만 single-center perspective의 선택 편향 가능성.

### 2.2 임상·기술적 제약

- **ADC 제조 복잡성**: DAR homogeneity 관리(stochastic vs. site-specific conjugation), linker-payload 합성 품질 관리가 GMP 환경에서 어렵다. 리뷰는 이를 다루지 않아 CDMO 의존도 평가 시 추가 문헌 필요.
- **독성 모니터링 부담**: Belantamab mafodotin(안과 검진 주기 관리), T-DXd(간질성 폐질환 모니터링), enfortumab vedotin(dysgeusia + 피부독성) 등 ADC 특이적 독성 모니터링이 표준 화학요법보다 복잡. 임상 운영 인프라 추가 필요.
- **Bystander effect의 투날 독성**: 막 투과성 payload는 정상 조직 세포로도 확산 가능. 임상 환경에서 이를 통제할 방법이 현재 없음.
- **Turnaround 이슈**: 리뷰 논문 특성상 실험 프로토콜 turnaround 해당 없음.

### 2.3 규제·QA·RA 관점

- **FDA pathway**: ADC는 biologic drug(BLA 경로)로 분류. 소분자 chemotherapy와 달리 세포주 확보·항체 제조·conjugation 공정 전 과정이 GMP 대상. 리뷰는 이를 다루지 않음.
- **바이오마커 co-development**: T-DM1, T-DXd는 HER2 IHC/FISH companion diagnostics(CDx) 요구. ASCO-CAP 가이드라인 기반. 리뷰가 CDx 개발 경로는 논의하지 않으나, "biomarker selection 개선 필요성"을 반복 강조 — 향후 ADC 승인 전략에서 CDx 동반 개발이 핵심 요소임을 시사.
- **IRB/consent**: 리뷰 논문이므로 해당 없음(primary data 미포함).
- **Reproducibility for audit**: 리뷰 논문이므로 code/data 공개 해당 없음. 참고한 임상시험 개별 등록 및 데이터 공개는 각 원논문 확인 필요.
- **1차 출처**: Nature Reviews Clinical Oncology 게재, peer-reviewed. MSKCC 저자. 임상 추천 근거로 사용하기에 권위 충분.

### 2.4 권위·신뢰 가중치

- `1차 출처`: Nature Reviews Clinical Oncology (peer-reviewed) — 임상 oncology 분야 최고 권위 리뷰 저널.
- Peer review 여부: Yes.
- **COI(이해상충)**: Modi — AstraZeneca, Daiichi Sankyo, Genentech, Novartis 컨설팅 및 advisory board; Chandarlapaty — Eli Lilly, Novartis, Sanofi 컨설팅 + research support. T-DXd(AstraZeneca/Daiichi Sankyo), T-DM1(Genentech/Roche) 긍정적 묘사와 연결 가능성 유의.
- **Funding**: NCI Cancer Center Support Grant, Conquer Cancer Foundation 등 공공 지원. 일부 institutional research support from industry. 전체 결론에 대한 기업 압력은 명확하지 않으나 COI 명시적 표시 필요.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **T-DXd (AstraZeneca + Daiichi Sankyo 공동)**: 이 리뷰에서 가장 두드러진 next-gen ADC. HER2 low에서의 활성 가능성이 언급되며, 이후 DESTINY-Breast04(2022)로 확인된다. AstraZeneca/Daiichi Sankyo의 ADC platform 전략은 HER2, HER3, TROP2, B7-H3를 타겟으로 한 pipeline 확장 중 — BD 관점에서 주시 대상.
- **Seagen(현 Pfizer)**: brentuximab vedotin, enfortumab vedotin 원개발사. CD30·nectin 4 이외 타겟으로의 MMAE linker-payload 기술 확장 방향 파악 필요.
- **Immunomedics(현 Gilead)**: sacituzumab govitecan. TROP2 타겟 ADC에서 SN-38 payload의 독보적 입지. TNBC 이후 폐암·방광암·부인암 확장 중 — 경쟁사 동향 모니터링.
- **내성 바이오마커 기술**: ABC transporter expression, lysosomal function assay를 ADC 치료 전 평가하는 진단 플랫폼은 아직 없음 — CDx-biomarker co-development 기회.

### 3.2 Commercialization-candidate (자체 제품화)

- **ADC targetability scoring 플랫폼 (SW/Dx)**:
  - 이 리뷰가 정의하는 타겟 선정 기준(발현 수준·내재화율·turnover·oncogenic relevance·표면 밀도)을 알고리즘화한 surfaceome scoring tool 개발 가능.
  - 입력: bulk RNAseq / proteomics / scRNAseq + surfaceome annotation.
  - 출력: ADC targetability 점수, 내재화 kinetics 예측, 독성 위험 예측.
  - TRL: 1~2 (concept 단계). surfaceome-adc-target 분석이 선행 데이터 역할.
  - IP 자유도: 높음 — 공개 문헌 기반 알고리즘.
- **내성 예측 다중진단 (Dx)**:
  - ADC 치료 전 ABC transporter 발현(ABCB1, ABCC1, ABCG2), HER2/TROP2/CD30 surface density, lysosomal acidification capacity를 동시 측정하는 멀티플렉스 패널.
  - 규제 경로: IVD/CDx (FDA 510(k) 또는 PMA depending on clinical claim).
  - TRL: 1~2. 전임상 근거는 있으나 환자 검증 없음.

### 3.3 우리 파이프라인과의 fit

- **SEV_BRCA, NCCHE_Gastric 적용 직결**: paper-info.yaml의 `applicable_to`에 명시된 적응증. HER2+ 위암(T-DXd ORR 51%)과 BRCA 관련 유방암 ADC 전략 수립에 직접 활용 가능.
- **surfaceome-adc-target 분석 방향성 제공**: 이 리뷰의 타겟 선정 기준(§Antibody and target selection)이 우리 surfaceome dataset에서 ADC 타겟을 우선순위화하는 scoring 기준으로 직접 활용 가능.
- **BD 발표 레퍼런스**: 파트너 또는 규제기관에게 ADC 설계 근거를 설명하는 표준 인용 문헌.
- **부족한 역량**: wet lab ADC 제조·conjugation·독성 평가. 외부 CRO 또는 파트너십 필요 시 참고.

### 3.4 후속 BD·제품 액션 후보

- **surfaceome ADC targetability scoring 알고리즘 개발**
  - 누가: 바이오인포매틱스 팀 (김가경 수석 + 분석팀)
  - 언제: 이번 분기 내 concept design. 다음 분기 prototype.
  - 자원: surfaceome dataset(보유 중), 공개 단백질 발현 DB (CCLE, TCGA HPA), 분석 인력 1인 2주.
  - 성공 기준: 알려진 ADC 타겟(HER2, TROP2, nectin 4, BCMA, CD30)이 상위 10% 이내 ranking.

- **내성 바이오마커 CDx 개념 기획**
  - 누가: BD 리드 + RA 담당 (현재 담당자 확인 필요)
  - 언제: 장기 (1년+)
  - 자원: 환자 코호트(ADC 치료 전·후 paired biopsy) + 멀티플렉스 어세이 플랫폼
  - 성공 기준: pilot cohort(n ≥ 20)에서 내성 예측 AUC > 0.75

- **파트너 동향 모니터링 (AstraZeneca ADC pipeline)**
  - 누가: BD 리드
  - 언제: 분기별 업데이트
  - 자원: 공개 파이프라인 DB + ASCO/ESMO 초록 모니터링
  - 성공 기준: HER3·TROP2·B7-H3 타겟 ADC 임상 단계 최신화

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective**: ADC 설계·기전·임상·내성·차세대 전략을 단일 문서로 통합한 2021년 현재 가장 권위 있는 리뷰. surfaceome-adc-target 파이프라인과 BD 발표 모두에서 핵심 배경 문헌.
- **등급 근거**:
  - 9종 FDA 승인 ADC 전체를 3요소 프레임워크로 통합 분류 — 타겟 선정 scoring 알고리즘 개발의 직접 기준.
  - 내성 3카테고리 정의가 향후 CDx 바이오마커 target 목록으로 그대로 사용 가능.
  - T-DXd·enfortumab vedotin 등 핵심 ADC의 임상 수치가 BD 발표 인용 가능한 권위 있는 수치.
  - Nature Reviews Clinical Oncology 게재, MSKCC 저자 → 파트너·규제기관 발표에서 인용 신뢰도 높음.
  - 논문 출판 후 T-DXd 관련 결과(DESTINY-Breast06 등)로 예측력 검증됨 — 기전 해석의 정확성 확인.

### 4.2 활용 우선순위

- **지금 (이번 달)**: surfaceome scoring 알고리즘 설계 시 타겟 선정 기준(§Antibody and target selection) 직접 적용. BD 발표 배경 슬라이드에 Table 1·Figure 2 인용.
- **다음 분기**: NCCHE_Gastric 관련 HER2+ 위암 ADC 전략 수립 시 T-DXd 임상 데이터(ORR 51%) 및 비교 근거 제시.
- **장기**: 내성 바이오마커 CDx 기획이 구체화될 때 Fig. 3(내성 기전)을 기술 motivation으로 활용.

### 4.3 발표·미팅에서 들이밀 시점

- **BD 미팅 (파트너와 ADC 전략 논의)**: Table 1 기반 ADC landscape 제시. "ADC 설계에서 타겟 특이성·링커·payload 조합이 왜 중요한지" 설명하는 표준 레퍼런스.
- **R&D 리뷰 (surfaceome-adc-target 분석 결과 보고)**: 분석에서 발굴된 타겟 후보를 Table 1의 기준과 비교 평가하는 근거.
- **사내 newsletter / 동향 공유**: ADC 분야 신입 팀원 온보딩 자료로 적합.

### 4.4 추가 탐색 필요 영역

- 질문: T-DXd의 HER2 low(IHC 1+ / 2+ FISH음성) 활성이 DESTINY-Breast04(2022) 이후 얼마나 빠르게 임상 적용되었는가? 우리 HER2 low 분류가 이 기준과 호환되는가?
- 질문: surfaceome dataset에서 nectin 4(PVRL4), TROP2(TACSTD2) 발현 분포가 우리 타겟 암종(BRCA, Gastric)에서 어떠한가? ADC targetability scoring의 첫 번째 검증 타겟으로 적합한가?
- 질문: belantamab mafodotin이 2022년 시장 철수 후 현재 재임상 진행 중인지 확인 필요 — BCMA 표적 ADC 전략 평가에 영향.
- 검토필요: 저자들의 COI(AstraZeneca, Daiichi Sankyo 관계)가 T-DXd 관련 긍정적 서술에 영향을 미쳤는지 독립적으로 확인 필요. 특히 T-DXd의 폐 독성(ILD 리스크)이 이 리뷰에서 상대적으로 경미하게 기술된 부분.
