# hu-2021-cancer-surfaceome-atlas_lens-industry.md

## 1. Categorization

> 이 섹션은 paper-info.yaml의 categorization 블록과 동기화된다.

### Domain

- `surfaceome` — 인간 세포 표면 단백체 체계화
- `cancer-genomics` — 33개 암종 pan-cancer 통합 분석
- `oncology-drug-discovery` — ADC·CAR-T·항체 타깃 발굴
- `single-cell-genomics` — scRNA-seq 기반 미세환경 분석

### Use case

- `pipeline-applicable` — TCSA 포털과 caGESP 409개 목록을 현재 ADC/CAR-T 파이프라인 타깃 우선순위 결정에 직접 활용 가능.
- `BD-opportunity` — 저자 기관(UPenn)의 TCSA resource 및 Lin Zhang 그룹의 캔서 서페이스오믹스 포지션 탐색.
- `academic-citation` — ADC 타깃 발굴 배경 및 caGESP 규모 수치 인용 가치 높음.

### Importance

- **Level**: 상
- **Perspective**: 전체 surfaceome의 2.5%만 current drug target → 1,433개 신규 후보 목록과 caGESP 409개가 우리 ADC 파이프라인 타깃 선정의 1차 필터로 즉시 활용 가능; 공개 포털(TCSA)을 통한 데이터 접근까지 완비.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: TCGA n=9,807 (33개 암종) + GTEx n=7,429 (30개 정상 조직) — 충분한 규모. 단, 암종별 n이 수십~수백으로 차이가 크고, 희귀 암종(MESO, UVM 등)은 소수 샘플이다.
- **Cohort 편향**: TCGA가 주로 미국 기반이며 일부 인종 다양성 제한. Tumor purity 및 immune cell infiltration 비율이 암종·환자마다 다르며 bulk RNA-seq이 이를 모두 반영하지 못한다.
- **Replication**: 5-알고리즘 앙상블의 internal cross-validation + 임상 타깃 13.4% 재발굴로 방법론 precision을 확인했다. 그러나 독립 외부 코호트(비-TCGA)에서의 전면 재현 데이터는 없다. 해석: 알고리즘 precision은 높으나 완전한 replication 부재로 regulatory grade evidence로는 부족.
- **Multiple testing**: BH FDR 보정 적용 명시. 특이성 알고리즘 합산 방식 자체는 multiple testing 맥락에서 검증된 엄밀한 통계적 프레임워크가 아니고 semi-empirical 방식이다.
- **mRNA proxy**: 단백질 발현의 41% positive correlation (GESP 기준) — 59%는 mRNA-단백질 불일치 가능성. 개별 타깃 단백질 확인은 별도 assay 필요.

### 2.2 임상·기술적 제약

- **In vitro only**: 모든 기능 데이터(CRISPR essentiality, receptor-ligand coexpression)가 2D cell line 또는 bulk transcriptomics 기반. In vivo 종양 환경에서의 검증 미완.
- **Internalization 미평가**: ADC의 핵심 요건인 항체-약물 내재화 가능성 데이터 없음. Atlas가 제시하는 caGESP를 ADC 타깃으로 바로 적용하려면 별도 internalization assay 필수.
- **Post-translational modification 반영 불가**: Glycosylation, shedding, 단백질 분해에 의한 표면 접근성 변화는 발현 데이터만으로 포착 불가.
- **계산 자원**: 포털/데이터 다운로드는 웹 기반 접근. 내부 재분석 파이프라인 구성 시 TCGA/GTEx 규모 데이터 처리 자원 필요.

### 2.3 규제·QA·RA 관점

- **Peer-review**: Nature Cancer (IF > 20) 게재, peer-review 완료.
- **IRB / consent**: TCGA/GTEx는 기존 공개 데이터베이스 사용. 신규 환자 샘플 없음. 개인정보 및 IRB 이슈 없음.
- **Regulatory pathway**: 이 논문 자체는 IVD·SaMD·drug 규제 자료가 아닌 발견/탐색 단계 자원. Atlas 기반 타깃으로 ADC·CAR-T 개발 시 IND 신청은 별도 전임상 단계 필요.
- **Reproducibility for audit**: 코드 (https://github.com/fcgportal/TCSA), 데이터 공개 포털 (TCSA at http://fcgportal.org/TCSA), 주요 소프트웨어 버전 명시(Reporting Summary). Audit 수준 재현성 높음.
- **Analytical validation**: 임상 타깃 97% 재발굴 및 caGESP 13.4% 임상 중 타깃 재발굴로 방법론 analytical precision 확인. Clinical validation (환자 예후, 치료 반응) 데이터는 없음.

### 2.4 권위·신뢰 가중치

- **1차 출처**: Nature Cancer 게재 peer-reviewed research paper (DOI: 10.1038/s43018-021-00282-w). 신뢰도 높음.
- **저자 이해상충 (COI)**: L.Z.와 X.H.는 AstraZeneca로부터 연구비 수령 보고 (Bristol-Myers Squibb, Squibb/Celgene, Prelude Therapeutics 포함). R.H.V.는 Children's Hospital Boston 대상 특허 보유 및 라이선싱. O.T.와 H.M.C.는 AstraZeneca 직원. → 표적 치료제 개발 이해관계 있는 저자 포함. 결과 자체는 계산 분석으로 직접 상업적 영향 낮으나 주의.
- **Funding**: NCI/NHGRI 지원 TCGA 기반. Lin Zhang은 NIH R01 grants (R01CA127776, R01CA190415, R01CA225929, R01CA262070, P50CA083638, P50CA174523) 지원. 공공 자금 기반으로 신뢰도 높음.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자/기관 자산화 가능성**: TCSA 포털은 UPenn + Functional Cancer Genome 데이터 포털(http://fcgportal.org/TCSA)을 통해 공개 제공. 현재까지 commercial startup 공개 정보 없음. Lin Zhang 그룹은 종양학 전산 분석 전문 학술 그룹으로, 직접 자산화보다는 공동연구·학술 라이선싱 경로에 가깝다. 해석: 직접 IP 확보보다 데이터 활용 + 저자 그룹과 공동연구 접근이 현실적.
- **경쟁사 관찰**: ADC 분야 주요 플레이어(AstraZeneca, Daiichi Sankyo, Genentech, Seagen)가 HER2·TROP2·Nectin4·FRα 등 표면 단백질 타깃으로 ADC를 이미 승인/개발 중. Atlas는 이 타깃들이 caGESP로 식별됨을 재확인. AstraZeneca 직원이 저자에 포함되어 있어 이미 내부 활용 가능성 있음.
- **시장 영향**: ADC 글로벌 시장 급성장 (외부 맥락: 2030년 수십조 원 규모 예상). 신규 타깃 1,433개라는 발굴 결과는 초기 R&D 방향 설정에 직접 영향.

### 3.2 Commercialization-candidate (자체 제품화)

- **Software (SW) / Platform**: TCSA 포털은 공개 플랫폼. 이를 내부 proprietary platform으로 확장해 자체 파이프라인에 통합하는 것이 가능 — UPenn 측 IP 관계 확인 필요. MVP: TCSA API + 내부 ADC 타깃 우선순위 scoring algorithm 결합.
- **Therapeutic (target identification)**: caGESP 409개 목록과 AND/iCAR-T 쌍 179/443개를 내부 타깃 선정 워크플로우에 직접 연결 가능. 특히 소화기암(STAD, ESCA, COAD, READ — CEACAM5, EPCAM, MUC1 등이 강조됨)이 우리 NCCHE_Gastric 라인과 overlap.
- **기술적 성숙도 (TRL)**: TRL 2~3 (개념 증명, 계산 기반). 단백질 수준 검증(TRL 4~5)이 다음 단계.
- **IP 자유도**: 코드 GitHub 공개 (MIT-style 예상, 직접 확인 필요). 방법론 특허 여부 명시 없음. 오픈소스 기반 재구현 가능성 높음.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**: TCGA 기반 — 우리 데이터셋과 직접 overlap 없음. 그러나 우리 타깃 암종(BRCA, gastric, 기타)에 대한 caGESP 목록은 TCSA에서 직접 조회 가능.
- **팀 역량**: TCSA 포털의 단순 조회는 즉시 가능. 내부 재분석(5-알고리즘 파이프라인 재구성)은 bioinformatics 1인 + Python/R 역량 필요. GPU 불필요.
- **전략적 방향 alignment**: ADC 타깃 우선순위 결정, liquid biopsy 바이오마커 탐색에 직접 align. 특히 SEV_BRCA, NCCHE_Gastric 대상 타깃 서브셋이 즉시 활용 가능.
- **빠진 capability**: 내재화 assay(wet lab), 단백체 수준 확인 장비/샘플 접근성.

### 3.4 후속 BD·제품 액션 후보

- **TCSA 포털 활용 및 내부 caGESP 목록 구축**
  - 누가: 본인 (bioinformatics)
  - 언제: 지금 (1주 내)
  - 자원: TCSA 포털 접근 + Supplementary Table 9 다운로드
  - 성공 기준: 우리 관심 암종(BRCA, gastric) 대상 caGESP tier 1 목록 확보 + 기존 파이프라인 타깃과 overlap 분석 완료

- **Internalization 데이터 overlay**
  - 누가: 본인 + wet lab 파트너 (또는 외부 CRO)
  - 언제: 다음 분기
  - 자원: TCSA caGESP 목록 + antibody panel + flow cytometry 또는 imaging assay
  - 성공 기준: 관심 caGESP 10~20개에 대한 internalization rate 측정

- **AstraZeneca / 경쟁사 동향 모니터링**
  - 누가: BD lead
  - 언제: 지금 (분기 리뷰)
  - 자원: ClinicalTrials.gov + ASCO/ESMO 발표 모니터링
  - 성공 기준: TCSA 상위 caGESP 중 경쟁사가 임상 진입한 타깃 파악

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective**: 전체 surfaceome의 2.5%만 current drug target → 1,433개 신규 후보 목록과 caGESP 409개가 우리 ADC 파이프라인 타깃 선정의 1차 필터로 즉시 활용 가능; 공개 포털(TCSA)을 통한 데이터 접근까지 완비.
- **등급 근거**:
  - 공개된 caGESP 409개 목록(Supp. Table 9)을 우리 ADC 관심 암종 필터링에 즉시 사용 가능 — zero additional cost.
  - 임상 타깃 97% 재발굴 + 13.4% 임상 개발 재확인 → 방법론 신뢰도가 있는 자원.
  - 수용체-리간드 쌍 1,278개는 ADC의 타깃-리간드 관계 탐색에 추가 인사이트 제공.
  - 단점: mRNA-단백질 불일치 + internalization 데이터 없음 → 고우선순위 타깃에는 추가 wet lab 검증 필수.
  - ERBB2 증폭 데이터(11개 암종 재발성 증폭)는 HER2 ADC 전략 우선순위 재확인 근거로 유용.

### 4.2 활용 우선순위

- **지금**: TCSA 포털 조회 + Supp. Table 9 (caGESP 409개) 내 우리 관심 암종 타깃 목록 추출. 기존 파이프라인 타깃과 overlap 확인.
- **다음 분기**: 상위 caGESP에 대한 단백체 수준 확인 계획 수립 (HPA 또는 CPTAC로 일부 보완 가능). AND CAR-T 쌍 목록(Supp. Table 10) 중 우리 관심 암종 해당 쌍 추출.
- **장기**: TCSA 방법론을 내부 새 데이터(신규 proteomics, scRNA-seq)에 적용해 자체 surfaceome atlas 구축.

### 4.3 발표·미팅에서 들이밀 시점

- **사내 R&D 리뷰**: ADC 타깃 선정 근거 제시 시 — "전체 surfaceome 2.5%만 current target, 신규 1,433개 후보" 수치가 탐색 필요성을 정당화하는 강력한 프레임.
- **BD 미팅**: 외부 파트너와 ADC 타깃 공동개발 논의 시, atlas 기반 타깃 후보 목록의 존재를 언급해 체계적 접근 강조.
- **사내 newsletter / 동향 공유**: Surfaceome atlas가 ADC 타깃 발굴 패러다임에 어떤 영향을 주는지 소개 자료로 적합.

### 4.4 추가 탐색 필요 영역

- 질문: TCSA 포털(http://fcgportal.org/TCSA)에서 BRCA 및 gastric cancer(STAD) 대상 tier 1 caGESP를 직접 조회하면 우리 현재 ADC 타깃 리스트와 얼마나 overlap되는가?
- 질문: caGESP 중 ADC-relevant internalization이 이미 문헌에서 보고된 타깃이 몇 개인가 (CEACAM5, EPCAM, MUC1 등 자주 언급되는 것 외)?
- 질문: Lin Zhang 그룹 또는 TCSA와 데이터 공유·공동연구 채널이 있는가? (학회 발표, 기존 collaboration 확인)
- 질문: Atlas의 AND CAR-T 쌍 중 HNSC 대상 쌍이 있는지 확인 — 우리 HNSC 라인과의 연결 가능성.

## 1. Categorization

### Domain

- `surfaceome-adc-target` — 범-암종 표면 단백체 atlas
- `pan-cancer genomics/proteomics`
- (보조) `immunotherapy target`, `precision oncology`

### Use case

- **`adc_target_reference`** — 우선. CytoGen이 CTC에서 발굴한 표면 단백질 후보를 외부 공개 atlas로 검증하는 1차 기준 자료.
- **`bd_pitch_reference`** — 보조. 제약사 발표에서 "우리 타겟이 Cancer Cell급 외부 atlas에서도 해당 암종 고선택성 타겟으로 확인된다"는 third-party 권위 참조.

### Importance

- **Level**: **고** (Cancer Cell 게재, 범-암종 커버리지, 전문 입수 시 즉시 활용 가능)

---

## 2. CytoGen Tier 체계와 연동

### ADC Tier 분류 — Atlas 교차 검증 프레임워크

| CytoGen Tier | 의미 | Atlas 교차 항목 |
|---|---|---|
| Tier1 ADC-Ready | FDA 승인 ADC 타겟 | 해당 암종 atlas 최상위 선택성 여부 |
| Tier2 Promising | 임상 3상+ 진행 중 | atlas 중상위 선택성 — 타겟 정당성 |
| Tier3 Biology | 생물학적 흥미 | atlas 하위 또는 미포함 — 신규 발굴 후보 |
| ICI-CDx | 면역 관문 마커 | atlas 면역 관련 표면 단백질 섹션 |

### NCCHE Gastric(STAD) 맥락

- **CLDN18.2**: 외부 맥락: 위암에서 CLDN18.2는 HPA 이미징에서 위 특이적 발현이 잘 알려져 있음. Atlas에서 STAD 최상위 선택성 타겟으로 포함될 가능성 높음 → Tier1 분류 근거 보강.
- **HER2**: 외부 맥락: HER2 amplification이 위암 15~20%에서 발생. CPTAC 단백체에서 HER2 과발현과 유전자 증폭 일치도 확인 가능.
- **TROP2(TACSTD2)**: 외부 맥락: 위암 포함 여러 암종에서 고발현. Atlas에서 선택성 점수 확인 권고.

### SEV BRCA 맥락

- 외부 맥락: 유방암 주요 표면 타겟: HER2, TROP2, HER3(ERBB3), FOLR1, NECTIN4. Atlas에서 BRCA 선택성 확인 → CTC HER2+ 발견(mCTC HER2+)의 외부 근거.

### NCCHE 범-암종 맥락 (Pancreatic/Colon/Biliary)

- 외부 맥락: PAAD(췌장암) — MSLN(메소텔린), EGFR, HER2; COAD(대장암) — CEACAM5, HER2, EGFR; CHOL(담도암) — FGFR2/3(fusion 타겟이나 표면 발현 연관). Atlas에서 각 암종별 상위 선택성 타겟 확인.

---

## 3. 정상 조직 안전성 (Therapeutic Window)

- 외부 맥락: Atlas의 핵심 가치 중 하나 — 정상 조직 발현 정량화. ADC는 정상 조직 발현이 높으면 독성(off-target toxicity) 위험.
- CytoGen 적용: NCCHE CTC에서 발굴한 신규 후보 단백질의 정상 조직 발현을 atlas에서 확인 → Tier 분류 시 안전성 가중 고려.

---

## 4. 리스크 및 제한

- **DOI 오기재**: 현재 paper-info.yaml DOI가 Strand 2022 DCIS 논문으로 오기재. 실제 Hu 2021 Cancer Surfaceome Atlas 논문 특정 후 재분석 필요.
- **CPTAC 커버리지**: NCCHE 주요 암종(특히 CHOL 담도암, PAAD 췌장암)의 CPTAC 단백체 데이터 커버리지가 제한적일 수 있음.
- **CTC 적용 간접성**: 조직 atlas → CTC 발현 외삽은 간접적.

---

## 5. 즉시 액션

1. 실제 Hu 2021 Cancer Surfaceome Atlas 논문 탐색 (PubMed: "cancer surfaceome atlas 2021 Hu Cancer Cell").
2. 전문 입수 후 supplementary table에서 STAD/BRCA/PAAD/COAD/CHOL 타겟 목록 추출.
3. NCCHE CTC 발현 표면 단백질과 교차 비교 → ADC Tier 분류 외부 검증.
4. paper-info.yaml DOI 및 sources/abstract.txt 수정.
