# hawkins-2025-her2-emt-mammary — Core Analysis

> 본 분석은 전문 PDF `sources/hawkins-2025-her2-emt-mammary.pdf` (12 pages) 를 근거로 한다.

---

## Executive Summary

- **무엇**: HER2 과발현 metaplastic breast carcinoma(MC) 및 HER2 증폭 세포주(HTB20)에서 EMT(epithelial-mesenchymal transition)가 — 자연 발생 및 TGFβ1 유도 모두 — *HER2* 유전자 증폭을 유지하면서 HER2 mRNA·단백질 발현을 후성유전적으로 소실시킨다는 직접 증거 제시.
- **모델 / 방법**: 인체 조직 TMA(IDC·IBC·MC 각 100 cases) + PDX(Mary-X) + 세포주(HTB20·MCF7) 세 갈래 병렬 접근. IHC·RT-PCR·FISH·LCM(laser capture microdissection)으로 epithelial vs. mesenchymal 구역을 직접 비교. TGFβ1(1–10 ng/ml) + serum starvation으로 실험적 EMT 유도.
- **핵심 결과**:
  - ① 인체 MC TMA — Table 1: HER2 증폭 MC 5 cases 전부에서 epithelial 구역 HER2 IHC +1~+3, mesenchymal 구역 IHC 0 (FISH 증폭 양 구역 동등 유지).
  - ② Mary-X PDX — emboli·non-emboli 모두 CDH1 강하게 유지; HER2 mRNA 차이 없음 → 단상성 진행에서는 EMT·HER2 silencing 없음 (음성 대조).
  - ③ Biphasic MC RT-PCR — mesenchymal phase에서 TWIST1·VIM·FN1 ↑; HER2 mRNA 극적 감소 (Fig. 4B, log scale).
  - ④ HTB20 + TGFβ1 — HER2 FISH 증폭 지속 확인(Fig. 5S); HER2 단백질 완전 소실(Fig. 5T); RT-PCR에서 HER2 mRNA 유의한 감소(Fig. 6).
  - ⑤ MCF7 + TGFβ1 — HER2 미증폭 상태에서 EMT 유도; HER2 발현 변화 없음 (음성 대조, Fig. 5I·J).
- **우리 적용**: HER2 ADC(T-DM1·T-DXd) resistance 기전 이해에 직결 — EMT에 의한 HER2 표적 소실이 ADC escape의 경로. CTC/liquid biopsy에서 EMT-high CTC의 HER2 발현 모니터링 설계 근거. `academic-citation` + `BD-opportunity` 활용 가능.
- **심층**: 한계·재현 ROI는 `hawkins-2025-her2-emt-mammary_lens-academic.md` / `hawkins-2025-her2-emt-mammary_lens-industry.md` / `hawkins-2025-her2-emt-mammary_methodology-brief.md` 참고.

---

## Identity

- **Title**: Natural and induced epithelial-mesenchymal transition results in epigenetic silencing of HER2 overexpression
- **Authors**: Kiandra N. Hawkins, Jordan Dillard, Yin Ye, Justin Wang, Robert M. Hoffman, Krista Mcphail, Sanford H. Barsky (corresponding: sbarsky@mmc.edu)
- **Year**: 2025
- **Venue**: Journal of Mammary Gland Biology and Neoplasia, 30:15
- **DOI**: 10.1007/s10911-025-09588-2
- **Published online**: 30 September 2025
- **Affiliations**: Meharry Medical College (Nashville, TN); Scripps Mercy Hospital (San Diego, CA); AntiCancer, Inc. (San Diego, CA); UCSD; Star Diagnostics Laboratories (Las Vegas, NV)
- **Funding**: DoD Breast Cancer Research Program (BC990959, BC024258, BC053405); Carolyn S. Glaubensklee Endowment; Meharry Medical College; NIH U54CA163069
- **Competing interests**: None declared
- **Ethics**: Multiple IACUC approvals (UCLA, Ohio State, Nevada, Meharry); human tissue IRB Ohio State 2006C0042 + Meharry (retrospective, exempt from Human Subject review)
- **Open Access**: CC BY-NC-ND 4.0

---

## Background

#### 배경 스토리

- **문제의 출발점**: EMT는 배아 발생부터 암 침윤·전이까지 관여하는 잘 알려진 현상이다. 상피성 암이 침윤하고 전이할 때 EMT가 일어난다면 전이 병소에서 상피 클러스터가 다시 나타나기 위해 MET(mesenchymal-epithelial transition)도 뒤따라야 한다는 이론이 지배적이었다.

- **선행 관찰 A**: 유방암 대부분(monophasic)은 침윤·emboli 형성 중에도 상피 형태를 유지해 EMT가 실제로 일어나지 않는다는 관찰이 있었다. 단, metaplastic breast carcinoma(MC)는 상피·간엽 두 가지 형태를 동시에 보이는 이상성(biphasic) 종양으로, 자연 발생 EMT의 in vivo 모델로 거론되었다.

- **A의 한계**: MC에서 EMT가 자연 발생한다는 조직학적 관찰은 있었지만, HER2 발현에 대한 직접적 분자 효과 — 특히 유전자 증폭(copy number)은 그대로인데 전사·번역만 소실되는 후성유전적 현상 — 는 직접 조직 수준 증거 없이 bioinformatic 추론에만 근거했다.

- **선행 접근 B**: 최근 bioinformatic 연구들이 공개 genomic dataset 분석으로 HER2 expression이 epithelial marker와 양의 상관, mesenchymal marker와 음의 상관임을 간접 보고했다 [ref 13]. lapatinib 저항성 및 trastuzumab 저항성 세포주에서 EMT 마커 증가 + HER2 발현 감소가 관찰되었다 [refs 36–38].

- **B의 한계**: 이 연구들은 genomic data 분석 또는 in vitro 획득 저항성 모델에 한정. 자연 발생 EMT 조직에서 HER2 mRNA·단백질과 FISH 증폭을 동시에 측정한 직접 증거가 없었다.

- **이 논문으로 이어지는 gap**: 자연 발생 EMT(in vivo 조직의 epithelial vs. mesenchymal 구역 직접 비교)와 실험적 EMT 유도(TGFβ1)가 HER2 overexpression을 epigenetically silencing하는지 직접 증거를 제시해야 했다.

#### 기본 개념

- **EMT (epithelial-mesenchymal transition)**: 상피 세포가 간엽 세포 표현형으로 전환하는 현상. 핵심 특징은 CDH1(E-cadherin) ↓, VIM(vimentin) ↑, FN1(fibronectin) ↑, TWIST1·SNAI1·SNAI2 등 전사인자 활성화. microRNA에 의한 추가 조절.

- **Metaplastic carcinoma (MC)**: 유방암의 드문 subset(~1%). 상피 성분과 간엽(육종성) 성분이 공존하는 이상성(biphasic) 종양. 약 90–95%가 triple negative; 5–10%는 HER2 증폭·과발현.

- **HER2 overexpression / amplification**: HER2(ERBB2) 단백질 과발현은 통상 *HER2* 유전자 증폭(chromosome 17q12)에 의존. 임상에서 IHC(단백질)와 FISH(유전자 copy number) 두 가지로 독립 측정. 증폭이 있어도 mRNA/단백질이 발현되지 않는 epigenetic silencing 가능성이 이 논문의 핵심 질문.

- **TGFβ1 유도 EMT**: TGFβ1(transforming growth factor-beta 1)을 serum starvation과 조합하면 in vitro에서 EMT를 효과적으로 유도하는 확립된 방법. 본 연구에서는 1–10 ng/ml TGFβ1, 48–72 h 처리 프로토콜 사용.

- **Laser capture microdissection (LCM)**: 조직 절편에서 특정 세포 집단(epithelial 또는 mesenchymal 구역)을 물리적으로 분리해 분자 분석하는 기술. 혼합 조직에서 세포 타입별 유전자 발현을 직접 비교할 수 있게 함.

#### 이 논문의 필요성

- **핵심 이유**: HER2 ADC(T-DM1, T-DXd) 치료 저항의 중요 기전 중 하나가 HER2 발현 소실이지만, 이것이 자연 발생 EMT와 연결된다는 직접 조직 수준 증거가 없었다.
- **기존 방법으로 부족했던 지점**: Bioinformatic 간접 상관 분석은 인과 방향과 조직 공간적 해상도를 제공하지 못했다.
- **이 논문이 해결하려는 방향**: LCM으로 epithelial vs. mesenchymal 구역을 물리적으로 분리 + IHC/FISH/RT-PCR 동시 적용. 이후 TGFβ1 실험으로 인과 가능성 강화.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: 자연 발생 EMT(MC in vivo) 및 실험적 EMT(TGFβ1 유도) 조건에서 HER2 유전자 증폭이 유지되는 동안 HER2 mRNA·단백질이 소실되는지 직접 정량.
- **입력**: (1) 인체 조직 TMA — IDC 100 cases, IBC 100 cases, MC 100 cases; 파라핀 임베딩 + 신선 냉동 조직. (2) Mary-X PDX(IBC). (3) 세포주 — HTB20[BT-474](CDH1+/HER2 증폭), MCF7(CDH1+/HER2 비증폭), HDF(인간 진피 섬유아세포, 간엽 참조).
- **출력**: 각 구역(epithelial/mesenchymal/emboli/non-emboli)별 CDH1·VIM·HER2 IHC signal intensity, HER2 FISH copy ratio, CDH1/TWIST1/VIM/FN1/HER2 mRNA 상대 정량.
- **추정 대상**: HER2 FISH 증폭과 HER2 IHC/mRNA 발현의 dissociation (= epigenetic silencing 여부).
- **중요한 hidden assumption**: TGFβ1 + serum starvation이 유도하는 in vitro EMT가 자연 발생 MC의 EMT와 동일한 epigenetic 기전을 공유한다는 가정. 논문은 이를 기전적으로 검증하지 않고 두 실험의 일관성으로 지지.

#### 확률 / 통계학적 구조

- **Model family**: 실험 biology paper (finding 중심). Computational model 없음.
- **통계**: Two-tailed Student's t-test + ANOVA. 각 case당 100 ROI 분석.
- **반복 설계**: RT-PCR 실험 5회 반복, 각 실험 5 replicates. 결과는 mean ± SD.
- **Multiple testing correction**: 미제공 — 본문에 BH/Bonferroni correction 명시 없음.
- **이미지 분석**: ERA(epithelial recognition algorithm) + SRA(specific recognition algorithm). Gaussian kernel 기반 tumor cluster/clump 인식, lymphovascular emboli(circumferential CD31/PDPN)·CDH1·VIM·HER2 signal intensity 정량. ImageJ 소프트웨어 사용. 장비: iSCAN System (BioImagine, Inc.).

#### 핵심 method insight

- **기존 방법의 한계**: 전체 조직(bulk) 추출 분석은 epithelial·mesenchymal 세포 혼합으로 구역별 HER2 발현 소실 측정 불가. Bioinformatic 분석은 세포 타입 해상도 없이 상관 계수만 제공.
- **이 논문이 바꾼 가정**: 조직 내 공간 구조를 보존하면서 epithelial과 mesenchymal 구역을 물리적으로 분리(Pixcell II Laser Capture Microdissection 788 Laboratory System)한 뒤 독립 분석.
- **새로 추가한 변수**: HER2 FISH(증폭)와 HER2 IHC(단백질)를 동일 사례·동일 구역에서 동시 측정 → copy number와 expression의 dissociation 직접 확인.
- **이 변화가 중요한 이유**: 유전자 증폭이 있어도 발현이 0이 될 수 있다는 epigenetic silencing의 조직 수준 직접 증거.

#### 이전 방법과의 차이

- **Baseline**: Bioinformatic correlation study [ref 13]; in vitro 획득 저항성 세포주 모델 [refs 36–38].
- **공통점**: HER2 expression 감소와 EMT marker 증가의 연관성 관찰.
- **차이점**: 본 연구는 in vivo 조직의 공간적 분리(LCM) + FISH 동시 측정으로 유전자 copy 수가 보존된 상태의 expression loss를 구역별로 직접 확인. 자연 발생(observational) + 실험적(interventional) 두 가지 설계 병행.
- **차이가 크게 나타나는 조건**: HER2 증폭 MC의 biphasic 구역 (epithelial ↔ mesenchymal 경계가 명확한 경우).

#### 세부 프로토콜

- **TMA 구성**: 각 파라핀 블록에서 평균 10 cores/block (2 mm 조직 코어). ERA/SRA로 epithelial/emboli 구역 자동 정렬·인식.
- **FISH**: *HER2* probe (140 kb chromosomal region 직접 표지, fluorophore Spectrum Orange, Vysis). 대조: chromosome 17 centromeric α-satellite probe (D17Z1, biotin-FITC). Zeiss epifluorescence, single band pass 조합. Red/green signal ratio.
- **IHC antibodies**: anti-PDPN (clone D2-40, Agilent Dako), anti-PECAM1 (rabbit polyclonal, Spring Bioscience), anti-HER2 (DAKO), CDH1-3195, VIM (Cell Signaling Technology). 1차 항체 1:100 희석, 30 min RT. Streptavidin-Biotin Complex/DAB 발색.
- **RT-PCR primer sets** (forward/reverse): CDH1-5/3, TWIST1-5/3, VIM-5/3, FN1-5/3, HER2-5/3. ABI 7500 Real-Time PCR System; Power SYBR Green; 7500 System SDS software. 실험 5회, 5 replicates. HDF를 reference cell line으로 사용.
- **Western blot**: 4–12% precast gradient gel (Invitrogen); CDH1 rabbit mAb (24E10 + H108, Santa Cruz). ACTB(13E5)를 housekeeping 대조. Chemiluminescent detection (West Femto, Pierce).
- **통계**: 각 그룹에서 mean ± SD (100 ROI). Two-tailed Student's t-test + ANOVA. "All experiments performed in quadruplicate" — RT-PCR 5 experiments × 5 replicates.

#### Method 관점의 한계

- **약한 assumption**: TGFβ1 + serum starvation은 생리적 조건과 다른 강제 EMT 유도. 종양 microenvironment에서의 자연 발생 EMT와 기전적 동일성 미검증.
- **Epigenetic 기전 미규명**: 논문 제목에 "epigenetic silencing"이 명시되어 있지만 DNA methylation·histone modification·miRNA 등 구체적 기전은 본문에서 검증되지 않음. Discussion에서 가능성만 언급 (refs 39–43: miRNA, DPAGT1, CMTM6 등).
- **소표본**: Table 1 핵심 결과가 HER2 증폭 MC 5 cases에 기반. 희귀 종양이라 대규모 검증 어려움.
- **Multiple testing correction 미제공**: 100 ROI per case, 다수 gene 비교에서 BH/Bonferroni correction 명시 없음.

---

## Results

#### Dataset별 결과

##### Dataset 1 — 인체 유방암 조직 TMA (retrospective, n=300 cases)

- **Dataset**: Human breast cancer TMA. IDC 100 cases, IBC 100 cases, MC 100 cases. 파라핀 임베딩 + 신선 냉동 조직. Natural Language Informational Warehouse Database 검색. IRB: Ohio State University (2006C0042), Meharry Medical College.
- **목적**: 자연 발생 EMT 유무 + HER2 발현·증폭 패턴 확인.
- **사용한 데이터 규모**: 각 case당 100 ROI. 총 300 cases.
- **Baseline / 비교 대상**: IDC·IBC(단상성) vs. MC(이상성).
- **Metric**: CDH1/VIM IHC signal intensity (mean ± SD, ERA/SRA); HER2 IHC (0/+1/+2/+3 반정량); HER2 FISH (red/green ratio).
- **주요 수치**:
  - IDC 및 IBC: emboli + non-emboli 모두 강한 CDH1 발현; VIM 낮음; HER2 발현 양 구역 동등 (Fig. 4A).
  - MC epithelial phase: CDH1 높음(~++++ ), VIM 낮음. MC mesenchymal phase: CDH1 낮음, VIM 높음 (Fig. 4A — 정확한 수치 본문 미제공, 시각적 bar graph).
  - **Table 1** (핵심): HER2 증폭 MC 12 cases 중 5 cases에서 HER2 FISH 증폭 확인(ratio: 1.1–60X). 이 5 cases 전부에서 epithelial(carcinoma) 구역 HER2 IHC +1~+3, mesenchymal(sarcoma) 구역 HER2 IHC 0 또는 +1 (Case 3·5는 +1 잔여). FISH ratio는 epithelial·mesenchymal 동등.
  - 나머지 7 cases: HER2 FISH ≤2X (비증폭), 대부분 sarcoma 구역 HER2 IHC 0.
- **정성 결과**: CDH1 IHC — 모든 12 cases에서 carcinoma 구역 ++++/+++, sarcoma 구역 −−−− 또는 + (Table 1). EMT 발생 구역에서 CDH1 소실 확인.
- **통계**: "All stated or calculated differences implied differences of statistical significance, assessed by two-tailed Student's t test as well as ANOVA." 구체적 p-value 미제공.
- 해석: 5 cases 소표본이나 FISH 보존 + IHC 소실의 조합이 모든 증폭 case에서 일관 → 우연 가능성 낮음. 단, 독립적 통계 평가 위한 p-value 수치 부재.

##### Dataset 2 — Mary-X PDX (IBC, monophasic, 음성 대조)

- **Dataset**: Mary-X, PDX of inflammatory breast carcinoma. 다수 선행 연구에서 검증된 well-characterized PDX. Emboli vs. non-emboli 구역 분리 (D2-40 immunofluorescence로 lymphatics vs. blood vessels 구분).
- **목적**: 단상성 암에서 EMT 부재 확인.
- **주요 수치**:
  - Western blot (Fig. 2C): Mary-X emboli·non-emboli — full-length CDH1(120 kDa) 강하게 발현. Emboli 구역에서 E-cad/NTF1(calpain-mediated proteolytic fragment, 90–95 kDa) 비율 증가하지만 전체 CDH1 발현 감소 없음. Mary-X spheroids도 CDH1 strong 유지.
  - IBC emboli·non-emboli: 양 구역 strong CDH1 발현 (Fig. 2C).
  - HDF (음성 대조, 완전 간엽): CDH1 음성 (Fig. 2C).
- **정성 결과**: 단상성 진행(emboli 형성)에서 CDH1 발현 유지 → EMT 없음. 전이성 emboli 형성이 EMT 없이 일어남.
- **논문 주장과의 연결**: 이전 연구 [refs 4, 16] 재확인. 단상성 암과 이상성 MC의 대조 배경 역할.

##### Dataset 3 — Biphasic MC RT-PCR (LCM 기반, observational)

- **Dataset**: Biphasic MC cases에서 LCM(Pixcell II, Arcturus)으로 epithelial(MC-epith) 및 mesenchymal(MC-mesen) 구역 분리. 신선 냉동 + 파라핀 절편(8 μm), 70% ethanol 고정, hematoxylin 염색.
- **목적**: 자연 발생 EMT에서 HER2 mRNA 변화 직접 정량.
- **사용한 데이터 규모**: 100 ROI 이상/group. RT-PCR 5회 반복, 5 replicates.
- **Metric**: Relative mRNA levels (log scale) — CDH1, TWIST1, VIM, FN1, HER2. HDF 참조 세포.
- **주요 수치**: MC mesenchymal phase에서 TWIST1·VIM·FN1 ↑ (IDC 대비, Fig. 4B log scale). HER2 mRNA: MC mesenchymal phase에서 MC epithelial phase 대비 극적 감소(Fig. 4B — 정확한 fold-change 미제공, 시각적으로 log scale 1–2 단위 감소 = 10–100배 수준).
- **통계**: Mean ± SD, 5 separate experiments × 5 replicates. 개별 p-value 미제공.
- 해석: HDF(완전 간엽)에서 CDH1 낮고 TWIST1·VIM·FN1 높은 패턴이 MC-mesen과 유사 → MC-mesen이 genuine mesenchymal phenotype임을 지지.

##### Dataset 4 — HTB20 + TGFβ1 실험적 EMT 유도

- **Dataset**: HTB20[BT-474] (CDH1+/HER2 amplified; ATCC, Manassas, VA). TGFβ1 1–10 ng/ml + serum starvation (High Glucose RPMI 1640 + 10 μg/ml insulin, 0% FBS, 24 h → TGFβ1 48–72 h).
- **목적**: 실험적 EMT에서 HER2 발현 소실 인과 검증.
- **대조군**: MCF7(CDH1+/HER2 비증폭) + 동일 TGFβ1 처리.
- **Metric**: Phase contrast morphology, CDH1/VIM IHC, HER2 FISH ratio, HER2 IHC, RT-PCR mRNA.
- **주요 수치**:
  - HTB20 baseline: HER2 FISH red/green >4 (증폭, Fig. 5N); HER2 IHC strong+(Fig. 5O); HER2 mRNA ~100 (relative, Fig. 6, log scale).
  - HTB20 + TGFβ1: FISH ratio >4 유지(증폭 지속, Fig. 5S); HER2 IHC 완전 소실(Fig. 5T); CDH1 IHC 소실(Fig. 5Q); VIM IHC 증가(Fig. 5R); HER2 mRNA 극적 감소 (~0.5 relative level, Fig. 6).
  - MCF7 baseline: HER2 FISH ratio <4 (비증폭, Fig. 5D); HER2 IHC 음성(Fig. 5E).
  - MCF7 + TGFβ1: EMT 유도(spindle morphology, Fig. 5F); CDH1 감소(Fig. 5G); VIM 증가(Fig. 5H); HER2 FISH 비증폭 유지(Fig. 5I); HER2 IHC 음성 유지(Fig. 5J) → **증폭 없으면 silencing 효과 없음**.
  - RT-PCR (Fig. 6): HTB20+TGFβ — CDH1 mRNA 유의한 감소 + TWIST1·VIM·FN1 유의한 증가 + HER2 mRNA 유의한 감소. MCF7+TGFβ — CDH1 감소 + EMT markers 증가; HER2 변화 없음.
- **통계**: Mean ± SD, 5 experiments × 5 replicates. "Significant increases and decreases" — 구체적 p-value 미제공.
- 해석: HER2 증폭 세포주(HTB20)에서만 EMT 후 HER2 silencing이 일어나고, 비증폭 세포주(MCF7)에서는 일어나지 않음 → 증폭된 HER2가 EMT에 의한 후성유전적 침묵화의 표적이 됨을 시사. 단일 세포주 단일 조건의 한계.

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: HER2 FISH 증폭이 보존된 상태에서 EMT 발생 시 HER2 mRNA·단백질 발현 소실. 자연 발생(MC 조직) + 실험적 유도(TGFβ1) 모두에서 일관. MCF7 음성 대조로 증폭 의존성 확인.
- **가장 중요한 수치**: Table 1 — HER2 증폭 MC 5 cases에서 mesenchymal 구역 HER2 IHC ≤+1 (epithelial 구역 +1~+3 대비). FISH ratio 양 구역 동등.
- **baseline 대비 차이**: 단상성 IDC/IBC에서는 emboli·non-emboli 모두 HER2 발현 유지. MC에서만 mesenchymal 구역에서 소실.
- **결과 해석 시 주의점**: (1) 핵심 Table 1 결과는 5 cases — 소표본. (2) Epigenetic silencing의 분자 기전 미규명. (3) 구체적 p-value 미제공으로 통계적 엄밀성 평가 제한.

---

## Figures

#### Figure 1
- **이 Figure가 필요한 이유**: 단상성 vs. 이상성 유방암 형태학적 차이를 조직학적으로 확립. EMT가 왜 MC에서만 일어날 수 있는지 시각적 전제.
- **이 Figure가 뒷받침하는 주장**: MC의 biphasic 형태학이 자연 발생 EMT를 시사.

##### 패널별 설명
- **A**: 단상성 IDC H&E. ductal carcinoma in situ(E1), invasive areas(E2), lymphovascular emboli(E3) 모두 상피 형태 유지. Scale bar 250 μm.
- **B**: Biphasic MC H&E. 상피(E)와 방추형 간엽(M) 두 가지 형태 공존. Scale bar 50 μm.

##### 본문에서 강조한 비교
- IDC는 모든 단계에서 상피 형태만. MC는 상피·간엽 공존 → 자연 발생 EMT 가능성.

##### 해석 시 주의점
- 형태학적 관찰이며 분자적 EMT 증거가 아님. 배경 정보 제공 역할.

---

#### Figure 2
- **이 Figure가 필요한 이유**: 단상성 암(Mary-X IBC)에서 emboli·non-emboli 모두 CDH1 발현 유지됨을 보여줌으로써 monophasic progression에서 EMT가 일어나지 않는다는 주장 지지.
- **이 Figure가 뒷받침하는 주장**: Emboli 형성(lymphovascular invasion)이 EMT 없이 가능하다.

##### 패널별 설명
- **A**: Mary-X PDX 조직. non-emboli(NE)와 emboli(E) 구역 구분. Scale bar 250 μm.
- **B**: D2-40(red)/CDH1(green) 이중 면역형광. NE·E 모두 강한 CDH1(green). NE에서 D2-40 circumferential 음성, E에서 양성. Scale bar 50 μm.
- **C**: Western blot. 레인: Mary-X Emboli, Mary-X Non-emboli, Mary-X Spheroids, Mary-X Aggregates, IBC Emboli, IBC Non-emboli, HDF. 120 kDa full-length CDH1 + 90–95 kDa proteolytic fragment. Emboli 구역에서 E-cad/NTF1(90–95 kDa) 비율 증가, 전체 CDH1 감소 없음. HDF는 CDH1 음성 대조. 이전 연구 [ref 16]에서 재현(MDPI permission 명시).

##### 본문에서 강조한 비교
- Emboli와 non-emboli: CDH1 발현량 차이 없음. Emboli에서 E-cad/NTF1 비율만 증가 — calpain-mediated processing 변화이지 발현 소실 아님.

##### 해석 시 주의점
- CDH1 발현 유지가 EMT 완전 부재의 충분 조건인지 논란 가능 (partial EMT 개념). 주요 기능: 음성 대조로서의 역할.

---

#### Figure 3
- **이 Figure가 필요한 이유**: Biphasic MC에서 HER2 FISH 증폭은 epithelial·mesenchymal 구역에 동등하게 존재하지만 HER2 단백질은 mesenchymal에서만 소실된다는 핵심 결과를 직접 이미지로 제시.
- **이 Figure가 뒷받침하는 주장**: EMT에 의한 HER2 epigenetic silencing의 in vivo 직접 시각 증거.

##### 패널별 설명
- **A**: H&E. 상피(E)와 간엽(M) 구역 공존. Scale bar 250 μm.
- **B**: CDH1 IHC. 상피(E)에서 강한 막 발현, 간엽(M)에서 소실. Scale bar 250 μm.
- **C**: HER2 FISH. Red(HER2)/green(Chr17) signal ratio >10X. 상피·간엽 구역 모두 동등한 증폭 신호. Scale bar 25 μm.
- **D**: HER2 IHC. 상피(E)에서 강한 발현(3+), 간엽(M)에서 완전 소실(0). Scale bar 250 μm.

##### 본문에서 강조한 비교
- Panel C vs. D: FISH 동등 증폭(copy number 불변) + IHC 단백질 완전 소실 → epigenetic silencing.

##### 해석 시 주의점
- 단일 대표 케이스 이미지. 전체 5 cases 정량은 Table 1로 제시.

---

#### Figure 4
- **이 Figure가 필요한 이유**: TMA 기반 정량 IHC(A)와 RT-PCR mRNA 정량(B)으로 IDC·MC 비교를 수치화. 단순 시각 이미지 외 통계 비교 근거.
- **이 Figure가 뒷받침하는 주장**: MC mesenchymal phase에서 EMT 발생 + HER2 발현 감소의 통계적 정량 확인.

##### 패널별 설명
- **A**: TMA image analysis. X축: IDC non-emboli, IDC emboli, MC epithelial, MC mesenchymal. Y축: relative signal intensity (mean ± SD). CDH1(black), VIM(gray), HER2(hatched). MC-mesen에서 CDH1 ↓, VIM ↑, HER2 ↓. IDC emboli·non-emboli: CDH1 high, VIM low. 정확한 수치 본문 미제공(그래프에서 시각 판독).
- **B**: RT-PCR comparisons. X축: IDC, IDC-Emboli, MC-epith, MC-mesen, HDF. Y축: relative mRNA (log scale). CDH1/TWIST1/VIM/FN1/HER2 5개 markers. MC-mesen: TWIST1·VIM·FN1 ↑; HER2 ↓. HDF: CDH1 low, EMT genes high.

##### 본문에서 강조한 비교
- IDC emboli: HER2 overexpression 지속. MC mesenchymal: HER2 극적 감소. TWIST1·VIM·FN1 증가 = EMT 확인.

##### 해석 시 주의점
- Log scale Y축 — 시각적 차이를 linear로 변환해야 실제 배수 평가 가능. 정확한 수치·p-value 미제공.

---

#### Figure 5
- **이 Figure가 필요한 이유**: TGFβ1 유도 EMT가 HER2 발현을 silencing하는지 세포주에서 실험 검증. HTB20(HER2 증폭)과 MCF7(비증폭) 나란히 비교.
- **이 Figure가 뒷받침하는 주장**: TGFβ1이 HER2 증폭 세포에서만 HER2를 silencing. 유전자 증폭과 발현 독립성 in vitro 확인.

##### 패널별 설명
- **A–E**: MCF7 baseline — epithelial cluster(A), CDH1+(B), VIM−(C), HER2 FISH 비증폭(D), HER2 IHC 음성(E).
- **F–J**: MCF7 + TGFβ1 — spindle morphology(F), CDH1↓(G), VIM↑(H), HER2 FISH 비증폭 유지(I), HER2 IHC 음성 유지(J). **음성 대조**.
- **K–O**: HTB20 baseline — epithelial cluster(K), CDH1+(L), VIM−(M), HER2 FISH 증폭 >4X(N), HER2 IHC strong+(O).
- **P–T**: HTB20 + TGFβ1 — spindle morphology(P), CDH1−(Q), VIM+(R), HER2 FISH 증폭 지속(S), HER2 IHC 완전 소실(T). **핵심 결과**.

##### 본문에서 강조한 비교
- HTB20 Panel N vs. S: FISH 증폭 유지(copy number 불변). Panel O vs. T: 단백질 완전 소실 → in vitro epigenetic silencing.

##### 해석 시 주의점
- 대표 이미지. 정량 수치는 Fig. 6(RT-PCR). 단일 세포주·단일 처리 조건. TGFβ1 dose-response 및 silencing 가역성 미제공.

---

#### Figure 6
- **이 Figure가 필요한 이유**: 세포주 EMT 유도의 RT-PCR 정량 결과. Fig. 5 이미지를 mRNA 수치로 뒷받침. HER2 mRNA 감소를 통계적으로 확인.
- **이 Figure가 뒷받침하는 주장**: TGFβ1이 HTB20에서 CDH1 ↓ + TWIST1·VIM·FN1 ↑ + HER2 ↓ 를 mRNA 수준에서 유의하게 유도.

##### 패널별 설명
- **단일 패널**: 5 conditions (MCF7, MCF7+TGFβ, HTB20, HTB20+TGFβ, HDF). Log scale Y축. CDH1(black), TWIST1(red), VIM(blue hatched), FN1(green), HER2(brown). Mean ± SD, n=5 experiments × 5 replicates.
- MCF7 + TGFβ: CDH1 ↓, TWIST1·VIM·FN1 ↑; HER2 변화 없음 (비증폭 음성 대조).
- HTB20: HER2 brown bar ~100 relative level. HTB20+TGFβ: HER2 ~0.5 (log scale 기준 ~100배 이상 감소).

##### 본문에서 강조한 비교
- HTB20+TGFβ에서 HER2 mRNA "dramatically reduced" — 5 experiments × 5 replicates에서 일관. 정확한 fold-change·p-value 미제공.

##### 해석 시 주의점
- Log scale 시각 차이 → linear 변환 필요. p-value 및 CI 미제공.

---

## Tables

### Table 1 — HER2 in biphasic metaplastic carcinomas

- **이 Table이 필요한 이유**: HER2 증폭 MC의 epithelial(carcinoma-area)과 mesenchymal(sarcoma-area)에서 CDH1 IHC, HER2 FISH, HER2 IHC를 12 cases 직접 수치 비교. 논문의 핵심 정량적 증거.
- **이 Table이 뒷받침하는 주장**: HER2 FISH 증폭이 양 구역에서 동등할 때 HER2 단백질은 mesenchymal에서 소실.

#### 표 구조
- **Row**: Case 1–12
- **Column**: Carcinoma-area (CDH1, HER2 FISH, HER2 IHC) vs. Sarcoma-area (CDH1, HER2 FISH, HER2 IHC)
- **셀 값**: CDH1 IHC (+/++/+++/++++), HER2 FISH (X배수), HER2 IHC (0/+1/+2/+3)

#### 핵심 수치

| Case | Carcin. CDH1 | Carcin. FISH | Carcin. IHC | Sarc. CDH1 | Sarc. FISH | Sarc. IHC |
|------|------|------|------|------|------|------|
| 1 | ++++ | 60X | +3 | −−−− | 60X | **0** |
| 2 | +++ | 20X | +3 | −−−− | 20X | **0** |
| 3 | ++++ | 4X | +3 | −−−− | 4X | **+1** |
| 4 | ++++ | 2X | +2 | −−−− | 2X | **0** |
| 5 | ++++ | 10X | +3 | + | 10X | **+1** |
| 6 | ++++ | 5X | +3 | + | 5X | **0** |
| 7 | +++ | 1.1X | +2 | −−−− | 1.1X | **0** |
| 8 | ++++ | 2.0X | +1 | −−−− | 2.0X | 0 |
| 9 | +++ | 1X | 0 | −−−− | 1X | 0 |
| 10 | ++++ | 1X | 0 | −−−− | 1X | 0 |
| 11 | +++ | 1.5X | +1 | −−−− | 1.5X | 0 |
| 12 | +++ | 1.5X | +1 | −−−− | 1.5X | 0 |

- Table footnote: 100 cases MC 중 HER2 amplification이 있는 5 cases(Table 1 기준으로는 Cases 1·2·3·5·6이 명확한 증폭) 특정. HER2 overexpression은 epithelial에서 유지, mesenchymal에서 완전 소실.
- 통계: 개별 p-value 미제공.

#### 본문에서 강조한 비교
- FISH 증폭 확인 cases에서: carcinoma area HER2 IHC +1~+3 vs. sarcoma area 0 (또는 +1). FISH ratio 동등.
- CDH1: carcinoma area 전부 +++/++++, sarcoma area 전부 −−−− 또는 + → EMT 구역 특이적.

#### 해석 시 주의점
- Case 3·5: sarcoma 구역 HER2 IHC +1 잔여 → 완전 소실이 아닌 partial silencing. Case 6·7: FISH 5X·1.1X — 경계선 증폭. 5 cases 소표본. 다중 비교 보정 미제공.

---

## Supplementary Information

- **No datasets were generated or analysed during the current study** (Data availability statement 명시).
- 별도 Supplementary PDF·데이터 파일 없음.
- Figure 2 일부 패널: 이전 연구 [ref 16 — Wang 2024]에서 MDPI permission으로 재사용 (Fig. 2 caption 명시).
- 참고문헌 43개 (References, pages 10–12).

---

## 분석 자체에 대한 메모

1. **p-value 미제공**: "All stated or calculated differences implied differences of statistical significance"라고 기술하지만 구체적 p-value를 본문에 일절 제시하지 않음. 독립적 통계 평가 제한.
2. **"Epigenetic silencing" 제목과 기전 증거 불일치**: 논문 제목에 명시되어 있으나 DNA methylation·histone modification·miRNA 등 구체적 기전은 측정되지 않음. Discussion에서 가능성만 언급. 제목이 mechanistic evidence를 넘어선 해석.
3. **소표본 HER2 증폭 MC**: Table 1 핵심 결과가 5 cases에 기반. MC 자체 희귀(유방암 ~1%)이므로 구조적으로 소표본이나 결론 강도 제한은 인식해야 함.
4. **TGFβ1 모델의 생리적 한계**: Serum starvation + TGFβ1은 표준 in vitro EMT 프로토콜이나 종양 microenvironment의 자연 EMT와 기전적 동일성 미검증.
5. **후속 분석 권고**: DNA methylation array(HER2 promoter 영역), ChIP-seq(H3K27me3·H3K4me3), small RNA-seq(miRNA 패널)으로 epigenetic 기전 직접 규명 필요.
6. **Mary-X 그림 재사용**: Fig. 2 일부가 이전 논문 [ref 16]의 재사용 — 이전 데이터 재확인인지 새 실험인지 주의 필요.
