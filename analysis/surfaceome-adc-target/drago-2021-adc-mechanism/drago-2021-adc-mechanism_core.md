# drago-2021-adc-mechanism_core.md

## Executive Summary

- **무엇**: ADC(antibody–drug conjugate) 설계 원리·작용 기전·임상 효능·독성·내성 메커니즘을 체계적으로 정리한 통합 리뷰. 기존 9종 FDA 승인 ADC의 구조적·기능적 차이를 분석하고 치료 잠재성을 극대화하기 위한 전략을 제시한다.
- **모델 / 방법**: 실험적 방법론이 아닌 리뷰 논문. 임상시험 데이터·전임상 연구·약동학(PK)/약력학(PD) 모델링 결과를 종합해 항체(antibody)·링커(linker)·payload의 3요소 프레임워크로 분류·해석한다.
- **핵심 결과**:
  - ① T-DXd — HER2+ 전이성 유방암 환자(5종 이상 선행치료 후)에서 ORR 60.9%
  - ② Enfortumab vedotin — 백금제·면역관문억제제 실패 후 전이성 요로상피암에서 ORR 44%
  - ③ Sacituzumab govitecan — 3차 이상 전이성 TNBC에서 ORR 33.3%
  - ④ T-DM1 — HER2+ 조기 유방암 잔존 병변 환자에서 재발·사망 위험 50% 감소
  - ⑤ 내성 기전 3종 카테고리 규명: 항원 발현 저하, 세포내 trafficking 변화, payload 내성·efflux
- **우리 적용**: ADC 타겟 선정 기준(표면 발현 수준·종양 특이성·내재화율·turnover)과 내성 패턴이 surfaceome-adc-target 분석의 타겟 우선순위 결정에 직접 활용 가능. `BD-opportunity` / `academic-citation` 이중 use_case.
- **심층**: 한계·재현 ROI는 `drago-2021-adc-mechanism_lens-academic.md` / `drago-2021-adc-mechanism_lens-industry.md` / `drago-2021-adc-mechanism_methodology-brief.md` 참고.

---

## Identity

| 항목 | 내용 |
|---|---|
| Title | Unlocking the potential of antibody–drug conjugates for cancer therapy |
| Authors | Joshua Z. Drago, Shanu Modi, Sarat Chandarlapaty |
| Year | 2021 |
| Venue | Nature Reviews Clinical Oncology |
| DOI | 10.1038/s41571-021-00470-8 |
| PMID | 33558752 |
| PMCID | PMC8287784 |
| Citation key | `@drago2021adcmechanism` |
| Document type | Review paper (peer-reviewed) |
| 저자 소속 | Memorial Sloan Kettering Cancer Center (MSKCC) + Weil Cornell Medicine |
| Published | 2021년 6월 (Epub 2021년 2월 8일) |

---

## Background

### 배경 스토리

- **문제의 출발점**: 항암 화학요법은 전신 독성 때문에 치료 지수(therapeutic index)가 좁다. 항체를 이용해 세포독성 약물을 종양에 선택적으로 전달하면 이 제약을 극복할 수 있다는 아이디어는 Paul Ehrlich의 "magic bullet" 개념(1900년대 초)까지 거슬러 올라간다.
- **선행 접근 A — 초기 ADC 시대**: 1950년대 하이브리도마 기술로 표적 항체 생산이 가능해졌고, CD33 표적 gemtuzumab ozogamicin이 2000년 FDA 최초 승인을 받았다. 그러나 임상 독성이 효능을 압도해 2010년 자발적 시장 철수가 이어졌다. 초기 ADC들은 독성 payload(methotrexate, doxorubicin)를 사용했으나 free drug 대비 우월성이 없었다(§ADC design and construction).
- **A의 한계**: ① payload의 세포독성이 충분하지 않거나 ② 링커 안정성이 낮아 혈장 내 premature release 발생 ③ 타겟 항원의 종양 특이성 부족. 실제 종양에 도달하는 ADC 용량은 투여량의 0.1% 수준에 불과하다(§How ADCs work in vivo).
- **선행 접근 B — 2세대 ADC**: 2011년 brentuximab vedotin(CD30 표적, MMAE payload) 승인으로 전환점을 맞았다. 이어 2013년 T-DM1(HER2 표적, maytansinoid DM1) 승인. 이 시기에 cleavable/non-cleavable linker 기술이 정교해졌고, sub-nanomolar 수준의 highly potent cytotoxic payload(auristatin, maytansinoid, calicheamicin) 도입이 이루어졌다.
- **B에도 남은 한계**: ① 같은 ADC가 cancer type에 따라 다른 독성 프로파일을 보임 ② HER2 발현량과 치료 반응의 상관관계가 단순하지 않음(T-DM1의 경우 HER2 음성 폐암에서도 ORR 44%) ③ 내성 기전이 규명되지 않음 ④ 병용 요법의 근거가 없음 ⑤ 종양 미세환경(TME)과 ADC 상호작용의 복잡성이 임상에서 예측 불가.
- **이 리뷰로 이어지는 gap**: 2019~2020년 단 2년간 5종 ADC가 추가 승인되면서(Table 1) 임상 현장에서 ADC 선택·순서·병용의 원칙적 지침이 부재해졌다. 작용 기전, 독성 패턴, 내성 메커니즘, 그리고 차세대 전략을 통합 정리하는 현장 가이드가 필요해졌다.

### 기본 개념

- **ADC 3요소**: ① antibody(항원 결합 특이성·Fc 기능) ② linker(혈장 안정성·세포내 방출 조건) ③ payload(세포독성 기전·막 투과성). 각 요소의 조합이 ADC의 약동학·독성·효능을 결정한다(§ADC design and construction, Fig. 1).
- **DAR(drug-to-antibody ratio)**: 항체 1개당 결합된 payload 분자 수. 현재 승인 ADC는 DAR 2~8. DAR이 높을수록 시험관 내 효능은 증가하지만, 간 clearance 가속·독성 증가·치료 지수 악화 가능성도 높아진다(§Payloads).
- **Bystander effect(방관자 효과)**: 막 투과성 payload가 항원 발현 세포에서 방출된 후 주변 항원 음성 세포로 확산되어 세포독성을 발휘하는 현상. 종양 내 항원 이질성 극복에 기여하지만, 정상 조직 독성 위험도 수반한다(§How ADCs work in vivo, Fig. 2 panel 6).
- **내재화(internalization)**: ADC가 항원에 결합한 후 세포 내부로 진입하는 과정. 주로 clathrin-mediated endocytosis를 통해 endosome → lysosome 경로를 거쳐 payload가 방출된다. 내재화율과 lysosomal trafficking이 ADC 활성의 핵심 결정 인자다(§How ADCs work in vivo, Fig. 2 panel 4).
- **ABC transporter(ATP-binding cassette transporter)**: MDR1, MRP1, BCRP 등이 payload를 세포 밖으로 능동 배출하는 efflux pump 역할. MMAE·DM1·ozogamicin이 ABC transporter substrate이며, 내성 메커니즘의 하나다(§Resistance to ADCs, Fig. 3c).

### 이 리뷰의 필요성

- **핵심 이유**: 2011~2020년 9종 FDA 승인 ADC가 축적되었으나, 이를 일관된 기전 프레임워크로 해석하고 임상 전략으로 연결하는 통합 리뷰가 부재했다.
- **기존 방법으로 부족했던 지점**: 개별 ADC 임상 리포트는 풍부하지만, antibody/linker/payload 3요소가 *어떻게 상호작용하여* 임상 결과를 만드는지에 대한 기전 수준의 종합 해석이 없었다.
- **이 리뷰가 해결하려는 방향**: ① 설계 원리부터 in vivo 작용까지 기전 통합 ② 독성과 내성 패턴의 분류 ③ 다음 세대 전략(ADC-intrinsic / ADC-extrinsic) 제시.

---

## Methods

이 논문은 리뷰 논문이므로 실험적/계산적 methods가 아니라 **method taxonomy**를 기술한다. 저자들이 ADC 관련 임상·전임상 증거를 통합하는 방식과 그 논리 구조를 정리한다.

### 리뷰 방법론 개요

- **자료 유형**: FDA 승인 ADC 9종에 대한 임상시험 결과(phase I/II/III), 전임상 연구, 약동학/약력학(PK/PD) 모델링 연구, 내성 기전 연구를 종합. 186개 참고문헌 포함.
- **분석 프레임워크**: 3요소(항체·링커·payload) 구조 분석 → in vivo 작용 기전 → 임상 발현 양상 → 독성 분류 → 내성 기전 → 미래 전략 순서의 연역적 구조.
- **비교 분류 방식**:
  - 링커: cleavable(hydrazone, disulfide, dipeptide/protease-cleavable) vs. non-cleavable(MC, MCC) 이분법(Fig. 1b)
  - Payload: 기전별 분류(microtubule inhibitor — auristatins/maytansinoids, DNA cleavage — calicheamicins, TOPO1 inhibitor — camptothecins)(Fig. 1b, Table 1)
  - 독성: on-target/off-tumour vs. off-target 이분법, 이후 payload class별·항원별 세분화
  - 내성: 3대 카테고리(항원 발현 저하 / 세포내 trafficking 변화 / payload 내성·efflux)(Fig. 3)

### 핵심 기전 분석 — ADC 3요소

**항체 선택 기준 (§Antibody and target selection)**
- IgG subclass: 대부분 IgG1 backbone. IgG1은 긴 반감기(21일), 강한 C1q 결합·FcγR avidity로 ADCC(antibody-dependent cellular cytotoxicity)·ADCP(antibody-dependent cellular phagocytosis) 가능.
- 타겟 선정 원칙: 종양 세포에서 고발현·정상 조직 저발현, 내재화 가능, 기능적으로 oncogenic한 수용체(HER2, TROP2, nectin 4, BCMA, CD30, CD22, CD79b, CD33).
- 내재화율·turnover 중요성: 내재화율이 높을수록 payload delivery 효율 증가. 기능적 oncogenic driver는 downregulation 압력이 낮다는 이론적 장점.

**링커 기술 (§Linker types and technologies)**
- Cleavable linker: 종양 내 산성(pH-sensitive hydrazone), 환원성(reducible disulfide), 효소(protease-cleavable dipeptide — cathepsin B) 환경에서 payload 방출. 세포외 방출 및 bystander effect 가능.
- Non-cleavable linker: 혈장에서 안정적, lysosomal degradation으로 payload 방출 시 linker 잔기가 payload에 붙어 있어 전하를 띔 → 막 투과성 낮아짐 → bystander effect 감소. T-DM1, belantamab mafodotin에 사용.
- 검토필요: 저자들은 "extracellular payload release가 ADC 활성의 중요한 구성요소일 수 있다"고 언급하지만, 이것이 어느 ADC에서 어느 비중인지 정량적 데이터는 미제공.

**Payload 클래스 (§Payloads)**
- Auristatins(MMAE, MMAF): Dolabella auricularia 유래. 미세소관 탈안정화. 7개 승인 ADC 중 해당.
- Maytansinoids(DM1, DM4): Maytenus 식물 유래. 미세소관 결합.
- Calicheamicins(ozogamicin): Actinomycetes 유래. DNA double-strand break.
- Camptothecins(DXd, SN-38): TOPO1 억제. T-DXd, sacituzumab govitecan.

**DAR 최적화**
- 고DAR ADC는 in vitro 효능 ↑, 간 clearance 가속 ↑.
- 마우스 모델에서 DAR 8 버전은 DAR 2 대비 5배 빠른 clearance, 더 나쁜 치료 지수(§Payloads).
- Sacituzumab govitecan처럼 DAR이 고정되지 않는 ADC는 DAR 무관 plasma clearance → 고DAR이 유리.
- 해석: DAR과 linker 안정성의 최적 조합은 payload class와 항원 종류에 따라 달라지므로 단일 최적값이 없다.

### 핵심 기전 분석 — In vivo 작용 경로 (Fig. 2)

1. ADC는 혈장에서 intact conjugate, naked antibody, free payload 세 성분으로 순환.
2. 종양 미세환경(TME) 도달 전 일부 payload가 혈관 밖으로 누출.
3. 항원 결합 전 항체 구성요소가 Fc-mediated 면역 효과기 기능 발휘(ADCC, ADCP), 신호전달 억제.
4. 항원 결합 후 대부분 clathrin-mediated endocytosis로 내재화.
5. Endosome/lysosome에서 산성·효소 조건에 의해 payload 방출, 세포질 확산, 세포사.
6. 막 투과성 payload는 주변 항원 음성 세포로 확산(bystander effect).

항원 결합~payload 방출까지 >24시간 소요 가능. Tumor penetration은 투여 후 1~2일에 peak.

### 내성 기전 (§Resistance to ADCs, Fig. 3)

3대 카테고리:
- **항원 발현 저하**: HER2, CD30, CD33 downregulation이 각 ADC 내성과 연관된 전임상 근거. 단 환자에서의 직접 확인은 제한적.
- **세포내 trafficking 변화**: Endosome recycling 증가, lysosomal acidification 감소, 단백질 분해 속도 저하. T-DM1 내성 유방암 세포에서 lysosomal acidification 감소 및 ABCB1 upregulation.
- **Payload 내성·efflux**: MDR1(ABCB1), MRP1(ABCC1), BCRP(ABCG2)가 MMAE·DM1·ozogamicin을 efflux. T-DXd는 ABCC2, ABCG2 고발현 세포에서도 활성 유지 — ABC transporter 기질이 아닌 T-DXd payload의 이점.
- PIK3CA 돌연변이가 trastuzumab 내성과 연관되나 T-DM1 내성과의 연관은 확인되지 않음.

미제공: 환자 조직에서 내성 기전을 직접 확인한 longitudinal 데이터 거의 없음. 대부분 cell line 근거.

---

## Results

이 리뷰는 개별 clinical trial 데이터를 기전 프레임워크로 재해석하는 방식으로 구성된다. 승인 ADC들의 핵심 임상 결과와 기전적 의미를 정리한다.

### 치료 내성 암에서의 활성 (§Activity in treatment-refractory cancers)

**T-DM1 (HER2, IgG1, non-cleavable, DM1, DAR 3.5)**
- 전이성 HER2+ 유방암(trastuzumab + taxane 전처치): ORR 43.6% (§Results)
- 조기 HER2+ 유방암(잔존 병변 후 보조요법): 재발/사망 위험 50% 감소 (§Results)
- HER2 음성 폐암에서도 ORR 44% — HER2 발현 역치가 ADC 활성 예측에 단순하지 않음을 시사.

**T-DXd (HER2, IgG1, cleavable, DXd/camptothecin, DAR 8)**
- 전이성 HER2+ 유방암(≥2종 HER2 기반 요법 후): ORR 60.9% (§Results)
- 위암(HER2+ 잔존 병변): ORR 51% (위암에서 irinotecan ORR ~14%와 비교) (§Results)
- 이전 irinotecan 투여 위암에서 ORR 41.7% — TOPO1 억제 ADC의 bystander 효과로 해석.

**Enfortumab vedotin (nectin 4, IgG1, cleavable, MMAE, DAR 4)**
- 전이성 요로상피암(백금 + ICI 실패): ORR 44% (중앙 3종 선행치료) (§Results)
- 단독 taxane 기반 화학요법 예상 ORR 10.5%와 비교.

**Sacituzumab govitecan (TROP2, IgG1, cleavable, SN-38, DAR 8)**
- 전이성 TNBC(3차 이상): ORR 33.3% (§Results)

**Inotuzumab ozogamicin (CD22, IgG4, cleavable, calicheamicin, DAR 5~7)**
- R/R B-ALL: 승인 (Table 1)

### 독성 패턴 (§The issue of toxicity)

- **On-target, off-tumour 독성**: 정상 조직의 항원 발현이 독성의 주요 원인.
  - Enfortumab vedotin: dysgeusia 40% — nectin 4 발현(침샘)
  - T-DXd + trastuzumab duocarmazine: 폐 독성 — HER2 발현 관련 추정
  - Belantamab mafodotin: 안구 독성 — MMAF + non-cleavable linker, 각막 상피 축적
  - CD44v6-targeted: 독성 표피 괴사 ~80%
- **Off-target 독성**: MMAE → 말초 신경병증·중성구감소증, DM1 → 혈소판감소증·간독성, MMAF/DM4 → 안구독성
  - 동일 payload class 내에서도 linker 차이로 독성 프로파일 다름: MMAF(non-cleavable) → 각막 축적, MMAE(cleavable) → 각막 세포 diffusion → 독성 더 낮음(§The issue of toxicity)
- **Target-independent uptake**: FcγR-mediated pinocytosis, macropinocytosis로 비표적 세포에도 ADC 흡수 가능.
- **HER2 표적 ADC에서 심장독성이 trastuzumab 단독보다 낮은 역설**: ERBB-neuregulin 신호축 차단이 아닌 별개의 기전일 가능성, 단 명확하지 않음(§The issue of toxicity).

### 바이오마커 및 환자 선택 (§De novo resistance and patient selection)

- 대부분 고형암 ADC는 tumor type 기반으로만 승인(TROP2 IHC 없이 sacituzumab govitecan 사용 가능).
- T-DM1, T-DXd만 HER2 발현 확인 요구(각각 IHC + FISH 기반 ASCO-CAP 가이드라인).
- 혈액암은 항원 발현이 cell lineage 정의적이어 biomarker 선택 필요성 낮음(CD30, BCMA).
- TROP2: 전이성 TNBC 환자의 ~90%가 중등도~고발현. 개별 발현 수준과 반응 상관관계 초기 신호 있음 — 정식 cut-off 미확립.
- gpNMB 발현 ≥25%: glembatumumab vedotin에서 ORR ~30% (전체 ORR 6%와 비교) — biomarker 선택의 중요성 예시.

### 치료 내성 암에서 ADC 효능의 기전 해석

- "Chemo-refractory" 암에서 ADC 효능: 기존 화학요법 내성이 ADC 타겟·payload 조합에 대한 내성과 다를 수 있음. ADC의 우월한 치료 지수가 기존 화학요법이 충분한 농도를 달성하지 못한 상황을 극복.
- Bystander effect: 항원 이질성 종양에서 cleavable linker + 막 투과성 payload의 bystander 살상이 중요. T-DXd(DXd, bystander capable)가 T-DM1(DM1, bystander 제한적)보다 우월한 이유 중 하나로 해석.
- 해석: ADC의 임상적 우월성은 단일 design parameter가 아니라 항체·링커·payload·TME·환자 선택의 복합 작용임을 저자들은 강조.

---

## Figures

### Figure 1 — ADC의 모듈 구성요소

#### 패널별 설명
- **패널 a**: 단일 ADC 모식도. 항체(녹색 Y자), 링커(파란색), payload(노란색 별). DAR = 4 예시.
- **패널 b**: 항체(IgG1~4 subclass, 반감기·C1q 결합·FcγR avidity 비교표), 링커(hydrazone/disulfide/dipeptide cleavable vs. MC/MCC non-cleavable 화학구조), payload(auristatins/maytansinoids/calicheamicins/camptothecins 4계열, 기전 요약) 통합 도식.

#### 본문에서 강조한 비교
- IgG1 vs IgG4: IgG4는 C1q 결합 없음, FcγR avidity 낮음 → ADCC/ADCP 기여 낮음. IgG4 기반 ADC(gemtuzumab, inotuzumab)는 IgG1 기반과 다른 면역 효과기 프로파일.
- Non-cleavable MC/MCC linker: MCC는 일부 payload에서 cleavable하게 작동 가능(*주석 표시).
- Payload class별 mechanism: auristatins·maytansinoids = anti-microtubule, calicheamicins = DNA cleavage, camptothecins = TOPO1 inhibition.

#### 해석 시 주의점
- Fig. 1b의 링커 구조도는 대표 예시. 실제 각 ADC의 합성 조건·결합 방식에 따라 링커 안정성이 크게 달라진다.

---

### Figure 2 — ADC 작용 기전

#### 패널별 설명
- **패널 1**: ADC가 혈액에서 세 성분(intact conjugate, naked antibody, free payload)으로 순환.
- **패널 2**: 종양으로 확산 중 일부 payload가 TME로 방출.
- **패널 3**: 항원 결합 전 Fc-mediated 면역 효과기 기능(NK cell 등), receptor dimerization 방해, downstream signaling 억제.
- **패널 4**: 항원 결합 후 clathrin-mediated endocytosis → endosome → lysosome에서 산성/단백질분해 조건으로 payload 방출.
- **패널 5**: Payload가 lysosome에서 방출 → 세포질 → microtubule(또는 DNA) 타겟 → 세포사.
- **패널 6**: 막 투과성 payload가 주변 항원 음성 세포로 확산(bystander effect).

#### 본문에서 강조한 비교
- ADC는 단순 "Trojan horse"가 아님: 세포외 payload release, Fc 효과기 기능, 직접 신호 억제가 payload-independent 기여.
- Clathrin-mediated endocytosis가 주 경로이나 pinocytosis 등 항원 독립적 경로도 존재.

#### 해석 시 주의점
- Fig. 2 caption에서 "TME에서 pay load release의 항암 기여 정도는 대부분 ADC에서 poor characterization"이라고 명시.

---

### Figure 3 — ADC 내성 메커니즘

#### 패널별 설명
- **패널 a**: 항원 downregulation/loss → ADC-항원 결합 불가 → lysosomal payload 방출 불가.
- **패널 b**: Endosome recycling 증가(ADC가 세포 밖으로 재배출), lysosomal 환경 변화(산성화 감소) → payload 방출 불충분.
- **패널 c**: ABC transporter(MDR1, MRP1 등) upregulation → payload efflux → 세포 생존.

#### 본문에서 강조한 비교
- 세 메커니즘은 전임상(in vitro)에서 각각 입증. 환자에서 동시·독립적 발생 가능하나 임상 확인 부재.
- T-DXd는 ABC transporter 내성이 상대적으로 낮음 — DXd payload가 poor ABC substrate.

#### 해석 시 주의점
- Caption: "supported largely by in vitro evidence but have not yet been confirmed in patients with cancer." — 임상 연관성 해석 시 주의.

---

### Figure 4 — ADC 활성 강화를 위한 합리적 병용 전략

#### 패널별 설명
- **패널 a**: 혈관 생물학을 변화시켜(항혈관신생제) ADC 종양 침투·delivery 개선.
- **패널 b**: 항원 발현/처리 조절 약물로 항원-ADC 결합 증대, ADC internalization 가속.
- **패널 c**: Payload 세포독성을 synergistic 또는 synthetic lethality로 강화하는 병용.
- **패널 d**: 면역요법으로 ADC 매개 면역 반응(ADCC, T세포 동원) 강화.

#### 본문에서 강조한 비교
- KATE2 trial: T-DM1 + atezolizumab(anti-PD-L1)에서 병용 효과 미확인(§Conclusions에서 언급).
- Enfortumab vedotin + pembrolizumab: 요로상피암에서 early signs of activity → phase III 진행(NCT04223856).

#### 해석 시 주의점
- 병용 임상의 대부분은 early phase 또는 진행 중. 병용 효능의 근거는 아직 preclinical 중심.

---

## Tables

### Table 1 — FDA 현재 승인 ADC (미국, 출판 당시 9종)

| ADC | 표적 항원 | mAb 종류 | 링커 | Payload | Payload class | DAR | 적응증 (승인 연도) |
|---|---|---|---|---|---|---|---|
| Gemtuzumab ozogamicin | CD33 | IgG4 | Cleavable | Ozogamicin | DNA cleavage (calicheamicin) | 2~3 | CD33+ R/R AML (2000년, 재승인 2017) |
| Brentuximab vedotin | CD30 | IgG1 | Cleavable | MMAE | Microtubule inhibitor | 4 | R/R sALCL, cHL, PTCL (2011~2018) |
| Ado-trastuzumab emtansine (T-DM1) | HER2 | IgG1 | Non-cleavable | DM1 | Microtubule inhibitor | 3.5 (mean) | Advanced HER2+ breast cancer (2013); residual disease early HER2+ (2019) |
| Inotuzumab ozogamicin | CD22 | IgG4 | Cleavable | Ozogamicin | DNA cleavage (calicheamicin) | 5~7 | R/R B-ALL (2017) |
| Fam-trastuzumab deruxtecan-nxki (T-DXd) | HER2 | IgG1 | Cleavable | DXd | TOPO1 inhibitor | 8 | Advanced HER2+ breast (≥2 HER2 regimens, 2019) |
| Polatuzumab vedotin-piiq | CD79b | IgG1 | Cleavable | MMAE | Microtubule inhibitor | 3.5 (mean) | R/R DLBCL (2019) |
| Sacituzumab govitecan-hziy | TROP2 | IgG1 | Cleavable | SN-38 | TOPO1 inhibitor | 8 | Advanced TNBC, 3rd line (2020) |
| Enfortumab vedotin-ejfv | Nectin 4 | IgG1 | Cleavable | MMAE | Microtubule inhibitor | 4 | Advanced urothelial carcinoma (2020) |
| Belantamab mafodotin-blmf | BCMA | IgG1 | Non-cleavable | MMAF | Microtubule inhibitor | Unknown | R/R multiple myeloma, 5th line (2020) |

**약어**: AML, acute myeloid leukaemia; B-ALL, B cell acute lymphoblastic leukaemia; BCMA, B cell maturation antigen; cHL, classical Hodgkin lymphoma; DAR, drug-to-antibody ratio; DLBCL, diffuse large B cell lymphoma; MMAE, monomethyl auristatin E; MMAF, monomethyl auristatin F; TOPO1, topoisomerase I; TROP2, tumour-associated calcium signal transducer 2; R/R, relapsed and/or refractory; sALCL, systemic anaplastic large cell lymphoma; PTCL, peripheral T cell lymphoma.

---

## Supplementary Information

- **Supplementary Table 1**: ADC와 면역요법 병용 임상시험 목록(≥20개). 승인 또는 실험적 면역요법제와의 병용 중인 ADC 대상 early phase 연구 포함. 본문 §Maximizing the potential of ADCs → ADC-extrinsic strategies에서 언급.
- 그 외 supplementary data: 미제공 (논문에 명시 없음; 리뷰 논문 특성상 원자료 supplementary는 제한적).

---

## 분석 자체에 대한 메모

- 이 리뷰는 2021년 초 출판 기준으로 9종 FDA 승인 ADC를 다룬다. 이후 승인된 ADC(mirvetuximab soravtansine, trastuzumab duocarmazine 상황 변화, disitamab vedotin 등)는 포함되지 않았다.
- 저자 3인 모두 MSKCC 소속. Modi, Chandarlapaty는 AstraZeneca, Daiichi Sankyo, Genentech, Novartis 등과의 이해관계(consulting, speaker fee) 명시(§Competing interests). 리뷰의 임상 사례 선택과 해석에 선택 편향 가능성 상존.
- 내성 메커니즘 섹션(§Resistance to ADCs)은 대부분 cell line 데이터 기반이며 저자들이 직접 caveat을 붙임("have not yet been confirmed in patients with cancer") — 임상 번역 시 주의.
- 검토필요: T-DXd의 뛰어난 임상 성적이 DAR 8 + cleavable linker + bystander effect 중 어느 요소에서 주로 기인하는지 분해 데이터가 논문 내에 없음. 개별 기여도 추정은 별도 연구 필요.
