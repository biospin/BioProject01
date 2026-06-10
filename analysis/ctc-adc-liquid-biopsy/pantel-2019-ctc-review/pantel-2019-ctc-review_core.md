# pantel-2019-ctc-review_core.md

## Executive Summary

- **무엇**: 고감도 액체생검(CTC·ctDNA)을 MRD(최소잔류질환) 검출·모니터링에 적용하는 최신 기술·임상 근거를 체계적으로 정리한 리뷰. 수술 후 영상으로 잡히지 않는 micrometastasis를 혈액으로 추적해 재발을 조기 차단하는 것이 핵심 명제.
- **모델 / 방법**: 리뷰 paper (taxonomy). CTC enrichment(면역학적·물리적) → detection(면역세포화학·분자생물학·기능 assay) → characterization(genome/transcriptome/proteome/xenograft)와, ctDNA 검출(ddPCR·BEAMing·CAPP-Seq·NGS) 두 축의 기술 분류 + 암종별 임상 데이터 요약.
- **핵심 결과**:
  - ① 유방암(breast cancer) — Rack 2014(n=2,090): CTC 양성이 DFS HR 2.11(95% CI 1.49–2.99, p<0.0001), OS HR 2.18(95% CI 1.32–3.59, p=0.002) 독립 예후인자. CTC ≥5개/30 ml: DFS HR 4.51(95% CI 2.56–8.45).
  - ② 유방암 ctDNA — Garcia-Murillas 2015(n=37+43): ctDNA 검출이 전이성 재발을 임상 확인보다 평균 7.9개월 선행.
  - ③ 대장암(colorectal cancer) — NGS 기반 ctDNA, 수술 후 검출 시 재발 위험 HR 18.0(95% CI 7.9–40.0, p<0.001).
  - ④ 폐암(lung cancer) — CTC >5개/7.5 ml: PFS HR 5.15(95% CI 1.44–18.46, p=0.012), OS HR 8.3(95% CI 2.09–32.91, p=0.003).
  - ⑤ 치료 표적 — ESR1·PIK3CA·AR·EGFR·KRAS 변이가 CTC·ctDNA에서 실시간 검출 → 내성 기전 추적 가능.
- **우리 적용**: academic-citation + BD-opportunity — CTC 기반 ADC 표적(EPCAM·HER2·PSMA 등) 검출 근거 및 MRD 대리표지자 임상 설계에서 직접 인용 가능. CTC 표면 단백질 프로파일링은 ADC payload 선정 근거가 됨.
- **심층**: 한계·재현 ROI는 `pantel-2019-ctc-review_lens-academic.md` / `pantel-2019-ctc-review_lens-industry.md` / `pantel-2019-ctc-review_methodology-brief.md` 참고.

---

## Identity

- **Title**: Liquid biopsy and minimal residual disease — latest advances and implications for cure
- **Authors**: Klaus Pantel¹, Catherine Alix-Panabières²
  - ¹Department of Tumour Biology, University Medical Centre Hamburg-Eppendorf, Hamburg, Germany
  - ²Laboratory of Rare Human Circulating Cells (LCCRH), University Medical Centre and University of Montpellier, Montpellier, France
- **Year**: 2019 (published online 22 February 2019)
- **Venue**: Nature Reviews Clinical Oncology, Vol. 16, pp. 422–437
- **DOI**: 10.1038/s41571-019-0187-3
- **PMID**: 30796368
- **Document type**: Review paper (peer-reviewed)
- **Citation key**: pantel2019ctcreview

---

## Background

### 배경 스토리

- **문제의 출발점**: 조기 암 환자의 상당 비율이 1차 절제 후 수년에서 수십 년 후 전이성 재발을 경험한다. 호르몬 수용체 양성 유방암의 경우 stage T1 환자에서도 T1N0 20년 원격 재발 위험이 13%, T1N1–3 26%, T1N4–9 34%에 달한다(본문 §Introduction). 임상·영상 검사로는 검출되지 않는 micrometastasis 또는 잔류 종양세포(MRD)가 이 재발의 원천이다.

- **선행 접근 A — 조직생검(tissue biopsy)**: 원발 병소를 기반으로 치료 표적·내성 변이를 파악하는 gold standard였다. 그러나 (1) 반복 채취 불가, (2) 원발과 전이 병소 사이의 분자적 이질성이 심해 원발 조직이 MRD를 대표하지 못하며, (3) 뇌·폐 등 특정 부위는 생검 자체가 어렵다(본문 §Therapeutic targets and resistance).

- **선행 접근 B — 영상 기반 MRD 감시**: CT·MRI는 임상 진단 역치(~10⁹ 세포) 이상의 종양 부하만 검출한다. 그보다 낮은 MRD 수준에서는 검출 자체가 불가능하다(Figure 4 caption).

- **한계의 핵심 gap**: 두 방법 모두 혈중 종양세포(CTC)와 ctDNA 수준에 있는 "MRD 진단 역치" 단계를 다룰 수 없다. 고감도 액체생검이 이 공백을 채울 수 있다는 전제에서 이 리뷰가 출발한다.

- **이 논문으로 이어지는 gap**: 고감도 liquid biopsy 기술은 이미 개발되었지만, 고형암 환자에서 MRD 추적에 실제로 적용할 수 있는지를 보여주는 임상 근거가 최근 5년간 급증했다. 이 데이터를 체계적으로 정리하고, 어떤 기술·어떤 암종에서 임상 적용이 현실적인지를 평가하는 것이 이 리뷰의 목적이다.

### 기본 개념

- **MRD (Minimal Residual Disease, 최소잔류질환)**: 1차 치료(수술·방사선·화학요법) 후 영상·임상 검사로는 확인되지 않지만 혈액·조직에 남아 있는 잔류 종양세포 또는 종양 DNA. 이후 전이성 재발의 원천.

- **CTC (Circulating Tumour Cells, 순환종양세포)**: 원발 또는 전이 병소에서 혈류로 유리된 세포. 혈액 내 반감기 1.0–2.4시간(유방암 기준). 대부분 apoptosis되지만 일부가 원격 장기에 disseminated tumour cells(DTCs)로 착상 후 dormancy에 진입하거나 overt metastasis로 발전.

- **ctDNA (Circulating tumour-derived DNA, 순환종양 DNA)**: 종양세포에서 유리된 cell-free DNA. 혈중 cfDNA의 <0.01%가 ctDNA(비전이성 초기 암)로 극히 낮다. 타깃 시퀀싱(ddPCR·BEAMing)은 검출 한계 <0.01%, CAPP-Seq는 ~0.004%까지 가능.

- **Cancer dormancy (암 휴면)**: 원발 병소에서 혈류를 거쳐 원격 장기에 도달한 DTCs가 수년~수십 년간 증식 없이 생존하는 상태. 세포 자체의 dormancy(G0/G1 arrest) 또는 면역계에 의한 tumor mass dormancy로 구분. 이 상태에서 벗어나면 overt metastasis로 진행(Box 1).

- **EMT (Epithelial-Mesenchymal Transition, 상피-간엽 전환)**: CTC가 혈류에 진입하기 위해 거치는 표현형 전환. EMT된 CTC는 EpCAM이 낮아 CellSearch 기반 포획에서 누락될 수 있음.

### 이 논문의 필요성

- **핵심 이유**: 고형암 MRD 영역의 대규모 임상 데이터가 2014–2018년 집중적으로 발표되어 체계적 정리가 필요한 시점이었다.
- **기존 방법으로 부족했던 지점**: 조직생검·영상은 MRD 단계에서 작동하지 않고, 이전까지의 CTC/ctDNA 리뷰는 전이성 암 또는 특정 암종에 집중되어 있었다.
- **이 논문이 해결하려는 방향**: CTC 기술의 전체 스펙트럼(enrichment → detection → characterization)을 정리하고, 암종별 임상 데이터를 통합해 MRD 대리표지자로서의 근거 강도를 평가하며, 치료 표적·내성 정보 획득 가능성을 기술한다.

---

## Methods

이 논문은 Review paper이다. 원저 방법론이 아니라 기존 기술·임상 연구의 taxonomy와 비교 정리가 핵심이다. `core-methods` skill의 method taxonomy 모드로 작성한다.

### CTC 분석 기술 분류

#### Enrichment (농축)

**Marker-dependent (표지자 의존)**
- *Positive selection*: EPCAM 항체(CellSearch가 대표)가 가장 광범위하게 쓰인다. EGFR, mucin 1(LAPC patients), PSMA(전립선), HER2(유방) 항체도 활용. 한계: EPCAM 낮은 CTC(EMT 진행 세포)를 놓친다.
- *Negative selection*: 비악성 혈액세포(CD45 등 백혈구 마커, CD146 내피세포, CD34 조혈줄기세포)를 고갈. Positive selection보다 순도 낮지만 EMT CTC 포획에 유리.

**Marker-independent (표지자 독립)**
- 크기·밀도·전하·변형능 차이를 이용. Microfilter: 혈액을 기공 통과 → 크기로 포획. 단, 크기 다양성(6–>20 µm)으로 소형 CTC 손실 가능. DEP(dielectrophoresis)는 전기 특성, inertial focusing은 크기+변형능.
- 중요 관찰: Coumans et al. 기준 혈구 직경 ~10 µm, CTC 6–>20 µm로 상당한 overlap.

#### Detection (검출)

- **면역세포화학(immunocytochemical)**: CellSearch(FDA 승인, EpCAM 양성 + 사이토케라틴 양성 + CD45 음성). 표준이지만 플랫폼 의존, EMT CTC 누락.
- **분자생물학(RT-PCR/RNA sequencing/in situ hybridization)**: 조직·종양 특이 transcript(PSA, 사이토케라틴 등) 검출. 단일 CTC 감도 충분하나 오염 백혈구의 저수준 발현으로 false positive 주의 필요.
- **기능 assay**:
  - EPISPOT: 96-well nitrocellulose membrane에서 CTC가 분비·탈락시키는 단백질(사이토케라틴 19, PSA 등) 검출 → 생존 세포만 검출, 유방·대장·전립선 암 검증됨.
  - EPIDROP: EPISPOT의 단일 세포 microfluidic 버전. 단일 CTC 수준에서 기능 정보.

#### Characterization (특성 분석)

- **Genome**: FISH(CNAs), WGA 후 array CGH·NGS(점돌연변이·CNA 포괄). 단일 세포 분리 후 whole-genome 증폭 가능하나 오류율 주의.
- **Transcriptome**: RT-PCR, RNA sequencing — AR-V7 splice variant(전립선암 내성 마커)를 mRNA 수준으로 검출.
- **Proteome**: 면역형광(증식·apoptosis 마커). Microfluidic western blot(최대 8개 단백질). Proximity extension assay 기술로 확장 가능성.
- **기능 in vivo**: PDX(patient-derived xenograft) — CTC를 면역결핍 마우스에 이식. 항암제 반응 예측 가능성 있으나 성공률 낮고(유방암 >1,000 CTCs 필요) 수개월 소요.

### ctDNA 분석 기술 분류

**Targeted sequencing (타깃 시퀀싱)**
- 원발 종양의 기지 돌연변이 panel을 표적: ddPCR, BEAMing, biPAP PCR, CAPP-Seq, TAmSeq 등.
- 감도: <0.01%(ddPCR/BEAMing 수준), CAPP-Seq iDES 버전은 0.004%까지.
- 장점: 단일 변이 기반 매우 높은 감도. 단점: 사전에 돌연변이 스펙트럼 정보 필요.

**Non-targeted WGS/WES**
- 전장 유전체 수준 CNA·점돌연변이 탐색. 사전 개인화 정보 불필요.
- 감도 1–5%(Standard NGS 기준)로 비전이성 단계에서는 ctDNA 농도가 너무 낮아 한계. 미전이암 재발 감시에는 targeted 방법이 현실적.

---

## Results

이 논문은 원저가 아닌 리뷰로, "결과"는 저자들이 종합·평가한 임상 연구들의 핵심 데이터다. 암종별로 정리한다.

### 유방암(Breast Cancer) — CTC 기반

#### 주요 임상 연구 요약 (Table 1 기반)

**Rack et al. (2014)** — 가장 큰 CTC 예후 코호트
- Dataset: Stage pT1–T4, pN0–N3, M0 유방암, n=2,090
- Detection: CellSearch system
- 주요 수치:
  - CTC 양성: DFS HR 2.11(95% CI 1.49–2.99, p<0.0001), OS HR 2.18(95% CI 1.32–3.59, p=0.002) — 다변량 독립 예후인자
  - CTC ≥5개/30 ml 혈액: DFS HR 4.51(95% CI 2.56–8.45), OS HR 3.60(95% CI 1.56–8.45)
  - 화학요법 후 지속 CTC: DFS HR 1.12(95% CI 1.02–1.25, p=0.02), OS HR 1.16(95% CI 0.99–1.37, p=0.06)

**Janni et al. (2016)** — 풀분석, n=3,173
- DFS HR 1.82(95% CI 1.47–2.26), DDFS HR 1.89(95% CI 1.49–2.40), BCSS HR 2.04(95% CI 1.52–2.75), OS HR 1.97(95% CI 1.51–2.59) — 진단 시점 CTC

**Sparano et al. (2018)** — 수술 후 4.5–7.5년 추적
- n=547 HER2⁻ 유방암(호르몬 수용체 양성 집단, n=353)
- CTC 양성군 재발률 21.4%(7건/32.7인-년), CTC 음성군 2.0%(16건/796.3인-년)
- CTC 양성: 재발 위험 13.1배(HR 13.1, 95% CI 4.7–36.3) 증가

**Trapp et al. (2018)** — CTC 2년 후 측정값
- n=1,087, 화학요법 2년 후 CTC 양성: OS HR 3.91(95% CI 2.04–7.52, p<0.0001), DFS HR 2.31(95% CI 1.50–3.55, p<0.0001)

**Bidard et al. (2018)** — NAT(neoadjuvant therapy) 맥락
- n=1,574, NAT 전 CTC 검출: OS·DFS·LRFS 모두 p<0.001로 악화. 단, 병리학적 완전 관해 달성에는 영향 없음.

**Goodman et al. (2018)** — 방사선 치료와의 연관
- NCDB 코호트 n=1,697, SUCCESS trial n=1,516
- CTC 양성 환자에서 방사선 치료 시 LRFS HR 2.73(95% CI 1.62–4.80, p<0.001), DFS HR 3.05(95% CI 2.22–4.13, p<0.001), OS HR 1.83(95% CI 1.23–2.72, p=0.003) 개선

**Riethdorf et al. (2017)** — n=213, 중앙 추적 67.1개월
- NAT 전 CTC ≥1개/7.5 ml: DFS p=0.031, OS p=0.0057; ≥22개/7.5 ml: DFS p=0.0001, OS p<0.0001

#### 유방암 — ctDNA

**Garcia-Murillas et al. (2015)**
- n=37(단일 시점), n=43(연속 모니터링)
- 개인화 ddPCR 방법으로 TP53 등 환자 특이 돌연변이 추적
- ctDNA 검출 → 전이성 재발을 임상 확인 평균 7.9개월 선행(HR 25.1, 95% CI 4.08–130.50 단일 시점; HR 12.0, 95% CI 3.36–43.07 연속 모니터링; p<0.0001)

**Olsson et al. (2015)**
- n=20, WGS + rearrangement-specific ddPCR
- ctDNA 수준 증가: 원격 재발 OR 2.1(p=0.02), 사망 OR 1.3(p=0.04)
- 전이 임상 확인 평균 11개월 선행(범위 0–37개월)
- 수술 후 장기 DFS 환자 전원 ctDNA 음성

### 대장암(Colorectal Cancer) — ctDNA

**Tie et al. (2016)** — n=1,046 혈장 샘플, 230명 stage II 대장암
- NGS 기반 ctDNA
- 보조치료 없이 수술 후 추적 178명 중 14명(7.9%) ctDNA 양성
- 중앙 추적 27개월: ctDNA 양성군 78.7% 재발 vs 음성군 9.8%; HR 18.0(95% CI 7.9–40.0, p<0.001)
- 보조치료 후 ctDNA 양성 → RFS HR 11.0(95% CI 1.8–68, p=0.001)

**Scholer et al. (2017)** — n=45 CRC
- 수술 후 ctDNA 검출 → MRD 및 재발 위험 증가

**Tie et al. (2019)** — n=230 CRC: 수술 후 재발 민감도 93%, 특이도 100%

**Hanahan & Weinberg 방식의 진화 관찰** — Soler et al.: 대장암 CTC line의 치료 저항성 클론 선택 확인

### 폐암(Lung Cancer) — CTC

**비소세포폐암(NSCLC)** — stage III–IV, n=70
- CTC >5개/7.5 ml: PFS HR 5.15(95% CI 1.44–18.46, p=0.012), OS HR 8.3(95% CI 2.09–32.91, p=0.003)
- CTC 수치가 치료 개입으로 조절 가능하며 PFS·OS와 상관(p<0.001 및 p=0.009)

**소세포폐암(SCLC)** — 같은 assay로 CTC 검출률 77/97명(85%)
- SCLC: CTC 범위 0–44,896개/7.5 ml; 평균 1,589±5,565
- 화학요법 1주기 후 CTC ≥50 vs <50: OS HR 2.45(95% CI 1.39–4.30, p=0.002), PFS HR 5.49(95% CI 1.78–16.91, p=0.003)

### 전립선암(Prostate Cancer) — CTC

- 근치적 전립선 절제술 3개월 후: CTC 검출률 66%→34%(p=0.031), 원발이 EPCAM+ CTC의 주요 원천임을 시사
- 반감기 혈중 1.0–2.4시간(유방암 기준) — 수술 3개월 후 CTC는 주로 clinically occult lesion 유래

### 치료 표적 및 내성 정보

**EGFR (NSCLC)**: EGFR^L858R 또는 exon 19 deletion → TKI 감수성; EGFR^T790M → 내성. CTC와 ctDNA 모두에서 검출 가능. Cobas EGFR Mutation Test v2: 민감도 99.8%, 특이도 65.7% (FDA·EMA 승인).

**ESR1 (유방암)**: ER+ 전이성 유방암 ~20%에서 내분비 내성 ESR1 변이 발생. PALOMA-3 trial(n=195) ctDNA 분석에서 ESR1^Y537S 변이 포함, palbociclib + fulvestrant 치료 후 clonal evolution 확인.

**PIK3CA (유방암)**: MBC 44명 중 7.9%(n=7/44)에서 PIK3CA 변이 CTC 검출. HER2+ 환자가 lapatinib 사용 시 내성 기전.

**AR·AR-V7 (전립선암)**: CRPC에서 AR 변이 다수. AR-V7 splice variant — 세포질 AR 결합 도메인 소실, constitutively active → enzalutamide·abiraterone 내성 예측. RNA 수준: 36% AR-V7, 25% AR-V12, 10% AR-V1/V3/V4.

**TMPRSS2-ERG fusion (전립선암)**: CTC에서 검출, abiraterone acetate 민감도 예측 바이오마커 후보.

**KRAS·BRAF (대장암)**: CTC·ctDNA에서 검출, KRAS 이질성(intra-patient) 현저함. CDK8 CTC 증폭 → CDK inhibitor 후보 표적.

**PD-L1**: CTC에서 원발 조직보다 높게 발현(MBC >60% vs <20%). NSCLC stage IV: 치료 후 PD-L1⁻ CTC는 nivolumab 반응 예측; 두경부암 PD-L1⁺ CTC는 OS HR 16.00(95% CI 2.76–92.72, p=0.002), PFS HR 6.22(OR 16.00 등, p<0.001) 와 완전 관해 반비례(negative correlation).

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: CTC 양성이 DFS·OS의 독립 예후인자임은 유방암(n>10,000 누적), 대장암, 폐암에서 일관. ctDNA는 유방암·CRC에서 재발을 영상보다 수개월 선행 검출.
- **가장 중요한 수치**: 유방암 CRC-ctDNA HR 18.0; 유방암 ctDNA 선행 검출 7.9개월.
- **baseline 대비 차이**: CTC/ctDNA vs. 영상: 재발 선행 검출 수개월 차이.
- **결과 해석 시 주의점**: ctDNA 코호트는 대부분 n<50으로 소규모. CTC 연구는 CellSearch 중심으로 EMT CTC 제외 편향. 전립선암은 데이터 이질성 큼(Supplementary Table 1 — 모든 조기 전립선암 연구에서 CTC-예후 통계적 유의성 없음).

---

## Figures

### Figure 1 — Technologies for CTC and ctDNA enrichment, detection, and characterization

- **이 Figure가 필요한 이유**: 논문 첫 번째 major section이 CTC 기술을 다루므로, 전체 기술 스펙트럼을 한눈에 조망하는 schematic이 필요했다.
- **이 Figure가 뒷받침하는 주장**: 다양한 생물학적·물리적·면역학적·분자생물학적 접근이 통합되어야 CTC의 enrichment, detection, characterization이 가능하다는 주장을 시각화.

##### 패널별 설명
- **CTC enrichment 구역 (좌하)**: Biology(positive/negative selection, 항체 기반) + Physics(크기·밀도·전하·DEP) 두 축으로 분류. 항체는 epithelial(EpCAM, CK) 또는 mesenchymal(vimentin, N-cadherin) marker를 표적.
- **CTC detection 구역 (중앙)**: 면역세포화학(epithelial·mesenchymal·tissue-specific·tumour-associated 마커) + 기능 assay(EPISPOT·EPIDROP — 단백질 분비 기반).
- **CTC characterization 구역 (우측)**: Genome(FISH·WGA·NGS), Transcriptome(qRT-PCR·RNA sequencing·in situ), Proteome(immunostaining·proteomics), Xenograft(종양 성장).
- **ctDNA 경로 (상단)**: 혈장에서 DNA 추출 → translocation·deletion/insertion·point mutation·amplification·epigenetic marks·chromosomal aberrations 탐색.

##### 본문에서 강조한 비교
- 비교 대상: CTC biology 기반(항체) vs. physics 기반(크기·전하) 농축
- 관찰된 차이: 항체 기반은 표지자 발현에 의존하므로 EMT CTC 누락 위험; 물리적 방법은 표지자 독립적이나 혈구와의 크기 중복으로 소형 CTC 손실 가능

##### 해석 시 주의점
- Figure 1은 개별 플랫폼의 성능 비교가 아닌 기술 분류 개요. 실제 sensitivity·specificity 수치는 본문 각 섹션 참조 필요.

---

### Figure 2 — Methods of ctDNA detection

- **이 Figure가 필요한 이유**: ctDNA 농도는 병기와 검출 방법에 따라 100만 배 이상 차이가 나며, 이 범위를 시각화하지 않으면 MRD 단계 적용 가능성을 오판하기 쉽다.
- **이 Figure가 뒷받침하는 주장**: 비전이성 암의 MRD 단계에서 ctDNA 검출에는 targeted 고감도 assay(ddPCR·BEAMing·CAPP-Seq 수준)가 필수임을 정량적으로 보여줌.

##### 패널별 설명
- x축: assay sensitivity (100% → 0.00025%), y축: 암 병기(전이성 → 비전이성 → 비악성).
- Sanger sequencing: sensitivity 100% → 전이성 고부하에서만 작동.
- Real-time PCR·standard NGS: 10–1% → 중간 병기.
- ddPCR·BEAMing·BEAMing·modified NGS: 0.1–0.01%.
- CAPP-Seq: 0.01–0.00025% → 비전이성 비악성 조건에서도 검출 가능 수준.

##### 해석 시 주의점
- ctDNA 농도 범위는 암종·환자마다 넓은 변이. 비전이성 암 일부 환자는 ctDNA가 아예 검출 불가능할 수 있음.
- 고감도 assay(CAPP-Seq)는 clonal haematopoiesis(노화·양성 종양에서도 낮은 수준 변이 검출) 문제로 false positive 위험.

---

### Figure 3 — Therapeutic targets and resistance mechanisms

- **이 Figure가 필요한 이유**: 액체생검의 두 번째 핵심 가치는 MRD 탐지뿐 아니라 치료 표적·내성 정보의 실시간 획득. 이 Figure는 CTC·ctDNA가 어떤 genomic 및 transcriptional 정보를 제공하는지 표시한다.
- **이 Figure가 뒷받침하는 주장**: CTC와 ctDNA는 상호 보완적 — ctDNA는 genomic/epigenomic 변이에, CTC는 transcriptional·단백질 수준 변화(AR-V7 등)에 강점.

##### 패널별 설명
- 좌측 구체(sphere): genomic aberrations — EGFR, ROS1, ALK(NSCLC), KRAS(CRC), ESR1, PIK3CA(유방암), AR, BRAF, TMPRSS2-ERG 등.
- 우측 구체: transcriptional changes — AR, AR-V7, PSMA, PD-L1, HER2, ER 등.
- 화살표: ctDNA·CTC 모두 두 구체에 연결되지만 emphasis가 다름.

##### 해석 시 주의점
- 이 Figure는 "가능성이 있는" 표적 목록이지 임상 검증 수준을 표시하지 않는다. EGFR(FDA 승인 Cobas test)과 AR-V7(임상 연구 단계)의 근거 수준이 동일한 도식에 표시됨.

---

### Figure 4 — Therapeutic strategies depending on dynamic changes in tumour burden

- **이 Figure가 필요한 이유**: MRD 개입의 clinical rationale을 타임라인으로 보여주는 conceptual figure. 왜 MRD 단계에서의 개입이 cure로 이어질 수 있는지 설득.
- **이 Figure가 뒷받침하는 주장**: 종양 부하가 MRD 진단 역치 이하일 때 post-adjuvant therapy를 투입하면 잔류 종양 세포를 eradication할 기회가 있음.

##### 패널별 설명
- y축: tumour load(세포 수, log scale 10¹–10¹²). x축: 시간(년).
- 선 A: 수술 후 MRD가 cure 역치 아래로 유지 → 치료 성공.
- 선 B: MRD가 잔류 → MRD 진단 역치를 일시 통과 후 관해 → 장기 관해.
- 선 C: 치료 실패 → MRD에서 임상 진단 역치까지 재성장 → 재발.
- 회색 "MRD diagnostic threshold"와 "Clinical diagnostic threshold" 구분선: 현재 영상 및 임상 검사는 clinical threshold 이하를 못 잡음. 액체생검은 MRD threshold까지 감지.

##### 해석 시 주의점
- 이 그래프는 개념 도식으로 실제 데이터 기반이 아님(Figure caption "hypothetical patient" 명시). 임상 검증이 필요한 intervention window의 존재를 정당화하는 conceptual argument.

---

## Tables

### Table 1 — Key studies of prognostic liquid biopsy analyses in patients with breast cancer

- **이 Table이 필요한 이유**: 유방암이 CTC·ctDNA MRD 연구에서 가장 근거가 두터운 암종으로, 주요 연구 7개(CTC 6 + ctDNA 3)를 한눈에 비교 가능하게 정리.
- **이 Table이 뒷받침하는 주장**: CTC 수와 임상 결과(DFS·OS·DDFS·BCSS·LRFS) 사이의 일관된 연관성; ctDNA가 영상보다 먼저 재발을 예측한다는 주장.

#### 표 구조
- Row: 각 연구(저자·연도)
- Column: Inclusion criteria / n / Detection method / Prognostic relevance / Refs
- 셀 값: HR·OR·p-value·CI

#### 핵심 수치 (CTC 연구)
- Rack et al. 2014: DFS HR 2.11(95% CI 1.49–2.99, p<0.0001); OS HR 2.18(p=0.002) — n=2,090, 가장 대규모
- Sparano et al. 2018: HR 13.1(95% CI 4.7–36.3) — 수술 후 4.5–7.5년, 장기 잠복 재발
- Janni et al. 2016: OS HR 1.97(95% CI 1.51–2.59), n=3,173

#### 핵심 수치 (ctDNA 연구)
- Garcia-Murillas 2015: HR 25.1(95% CI 4.08–130.50) — n=37, 넓은 CI로 소규모 코호트
- Olsson 2015: n=20, ctDNA-MFS OR 2.1(p=0.02), 사전 ctDNA 검출 평균 11개월

#### 본문에서 강조한 비교
- CTC 연구는 대부분 n>500–3,000으로 큰 반면, ctDNA 연구는 n=20–43으로 소규모
- CTC 연구는 CellSearch 중심으로 기술 균일성 높음; ctDNA 연구는 assay 방법이 연구마다 다름

#### 해석 시 주의점
- Table 1은 유방암 이외 암종을 포함하지 않음 — 유방암 특화 결론으로 일반화 주의
- 다수 연구가 retrospective 또는 observational로, 전향적 RCT를 통한 개입 이익 검증은 아직 미완
- 해석: ctDNA HR(25.1)은 CI가 매우 넓어 소규모 코호트에서의 과추정 가능성 있음

---

### Supplementary Table 1 — Clinical studies on the prognostic value of CTCs in early stage prostate cancer

9개 연구(2008–2016), stage LPC 또는 LAPC, n=15–152.
- 모든 연구에서 CTC 검출률 5–58.7%이나, CTC 검출과 확립된 예후인자(PSA, Gleason score, DFS) 사이에 통계적 유의성 없음.
- 유일한 예외: Kuske et al.(2016) EPISPOT assay — PSA 상관 p<0.0001, 임상 병기 p=0.04(단 CellSearch에서는 같은 결론 없음).
- 해석: CellSearch 기반 조기 전립선암 CTC 검출은 현재 임상적 예후 가치가 확립되지 않았다. 기술적 한계(CTC수 절대적으로 적음, 높은 이질성)가 주요 원인으로 추정.

### Supplementary Table 2 — Summary of ongoing clinical trials combining MRD and liquid biopsy (2019년 기준)

4개 임상시험 등재(ClinicalTrials.gov):
- NCT03614689: 난소암 ctDNA MRD → 재발 예측 (n=100, 2017 시작)
- NCT03145961: c-TRAK TN — TNBC ctDNA MRD → pembrolizumab 트리거 (n=200, phase II)
- NCT03020342: HBV 관련 간세포암 cfDNA MRD (n=50)
- NCT02314871: 대장암 수술 후 마취 방법별 CTC 수 비교 (n=60)

---

## Supplementary Information

### Supplementary Table 1
조기 전립선암 CTC 예후 연구 9편 종합(2008–2016). 세부 내용은 Tables 섹션 참조.

### Supplementary Table 2
2019년 기준 진행 중인 MRD + 액체생검 임상시험 목록. 본문 §Leveraging MRD for cures에서 NCT03145561과 함께 인용.

---

## 분석 자체에 대한 메모

- 이 논문의 본제목 vs. DOI 메타데이터 불일치: DOI `10.1038/s41571-019-0187-3`의 PubMed 기록은 "Liquid biopsy and minimal residual disease — latest advances and implications for cure"이나, 초기 `paper-info.yaml`의 title 필드가 "Liquid biopsy and minimal residual disease - latest advances and implications for cure"(대시 표기 차이)로 저장됨. 내용 동일.
- 검토필요: Figure 3의 PD-L1 OR 수치(OR 16.00, 95% CI 2.76–92.72)는 두경부암 소규모 연구 기반(Strati et al.)으로 신뢰구간이 매우 넓음. 독립적 대규모 검증 전까지 주의 필요.
- 질문: 2019년 이후 c-TRAK TN (NCT03145961) 등 언급된 임상시험의 결과가 발표되었는가? 후속 논문으로 MRD 개입 이익이 실제 검증됐는지 확인 필요.
- 검토필요: 저자들이 EPCAM 기반 CellSearch와 EPCAM 독립 EPISPOT을 직접 비교한 수치를 제시하지 않아, 두 플랫폼 간 CTC 검출률 차이의 임상적 의미를 이 논문만으로는 정량 평가하기 어렵다.
