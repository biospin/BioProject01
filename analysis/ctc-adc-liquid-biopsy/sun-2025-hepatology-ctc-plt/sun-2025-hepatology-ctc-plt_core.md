# sun-2025-hepatology-ctc-plt — Core Analysis
> PDF-based full analysis. 이전 abstract-only 분석을 overwrite. 2026-06-10.

---

## Executive Summary

- **무엇**: HCC 환자 혈액의 CTC-혈소판(PLT) 복합체가 NK-cell 살상에서 면역 회피하는 분자 기전 규명. PLT 직접 부착이 FAK/JNK/c-Jun cascade를 활성화하여 CTC 표면의 immune checkpoint CD155(PVR)를 전사 수준으로 상향조절하고, CD155가 NK-cell의 TIGIT 수용체와 결합하여 세포독성을 억제.
- **모델 / 방법**: scRNA-seq으로 PLT 관련 유전자 농축 확인 → multiplex IF(ChimeraX-i120)로 환자 혈액 PLT+CTC 빈도 측정 → in vitro 직접/간접 PLT 공배양으로 contact-dependency 검증 → Western blot + luciferase reporter로 FAK→JNK→c-Jun→CD155 전사 경로 확인 → TIGIT blocking antibody(α-TIGIT) + in vivo H22-luc 마우스 모델로 전이 억제 효과 검증.
- **핵심 결과**:
  - ① HCC 환자 CTC 양성자의 70%(14/20)가 PLT+CTC; PLT+CTC군이 PLT−CTC군보다 PFS(p = 0.0257) 및 OS(p = 0.0459) 유의하게 단축.
  - ② scRNA-seq + qPCR + Western blot에서 PLT 직접 부착 시에만 CD155 상향조절(간접 공배양 무효과); 환자 PLT+CTC의 76.0%가 CD155+, PLT−CTC의 25.0%만 CD155+ (chi-square p = 0.011).
  - ③ FAK 억제제(iFAK)가 p-FAK, p-JNK, p-c-Jun, CD155를 동시 감소; CD155 promoter의 c-Jun binding site 돌연변이(MUT) 시 luciferase 활성 증가 불능 → c-Jun이 CD155 전사의 직접 활성인자.
  - ④ CD155 knockdown으로 PLT 처리 종양세포에 대한 NK-cell IFN-γ 및 CD107a 기능 회복; OE-CD155가 이를 역전 → CD155 의존성 확인.
  - ⑤ α-TIGIT가 PLT 처리 종양세포에 대한 NK-cell 기능을 in vitro·ex vivo·in vivo에서 완전 복원; α-CD96는 효과 없음 → CD155-TIGIT axis 특이성.
- **우리 적용**: CTC 분리 파이프라인(ChimeraX 기반)에서 CD41 co-staining으로 PLT+CTC 식별 후 CD155 발현을 교차 분석 가능. NCCHE 위암 CTC 샘플에서 `pipeline-applicable`. CD155+CTC 검출 가능성 → `academic-citation`.
- **심층**: 한계·재현 ROI는 `sun-2025-hepatology-ctc-plt_lens-academic.md` / `sun-2025-hepatology-ctc-plt_lens-industry.md` / `sun-2025-hepatology-ctc-plt_methodology-brief.md` 참고.

---

## Identity

- **Title**: Platelet-mediated circulating tumor cell evasion from natural killer cell killing through immune checkpoint CD155-TIGIT
- **Authors**: Yunfan Sun, Tong Li, Lin Ding, Jiyan Wang, Chen Chen, Te Liu, Yu Liu, Qian Li, Chuyu Wang, Ran Huo, Hao Wang, Tongtong Tian, Chunyan Zhang, Baishen Pan, Jian Zhou, Jia Fan, Xinrong Yang, Wenjing Yang, Beili Wang, Wei Guo
- **Corresponding authors**: Wei Guo, Yunfan Sun, Beili Wang, Wenjing Yang (Zhongshan Hospital, Fudan University, Shanghai)
- **Year**: 2025 (Received 2023-09-15, Accepted 2024-04-23)
- **Venue**: Hepatology (AASLD), Vol. 81, pp. 791–807
- **DOI**: 10.1097/HEP.0000000000000934
- **Citation key**: sun2025ctcplt
- **Funding**: National Natural Science Foundation of China (82172348, 82102483, 82073222, 81972000, 81902139), National Natural Science Foundation Excellent Young Scholars (82222057), Shanghai Municipal Health Commission, and others.
- **COI**: 저자들이 이해상충 없음 명시(no conflicts of interest).
- **Cancer type**: Hepatocellular carcinoma (HCC, primary). NSCLC, PDAC는 cross-cancer validation에 포함.

---

## Background

### 배경 스토리

- **문제의 출발점**: HCC는 전세계 원발 간암의 90%, 암 사망 원인 4위. 원발 부위를 벗어나 혈액에 진입한 CTC는 전이의 직접 전구체지만, 혈액 내에서 소수만 살아남아 원격 장기에 정착한다. 이 생존 선택의 면역학적 기반은 장기간 불명확했음.

- **선행 접근 A — 물리적 차폐 모델**: PLT가 CTC를 둘러싸 microcloak를 형성하여 NK-cell의 물리적 접근을 차단한다는 모델(Brady et al. 2020, Stegner et al. 2014). 이 모델이 가능하게 한 것: PLT-CTC adhesion이 전이 촉진의 실험적으로 재현 가능한 요인임을 확립. 이 모델의 한계: 물리적 차폐만으로는 PLT 부착이 종양세포에 실제로 new immune checkpoint 프로그램을 유도한다는 현상을 설명하지 못함.

- **선행 접근 B — PLT 유래 가용성 사이토카인 모델**: PLT가 TGF-β, VEGF, EGF, PDGF 등을 분비해 암세포의 EMT와 면역억제 미세환경에 기여(Labelle et al. 2011, Haemmerle et al. 2018). 이 모델의 보완: 사이토카인 매개 면역억제 경로 개념 제시. 이 모델의 한계: 저자들이 EGF, VEGF, PDGF-DD, TGF-β1, IL-1β를 각각 중화해도 CD155 상향조절이 억제되지 않음을 직접 실험으로 보임 — 사이토카인 독립적 기전의 필요성 확인.

- **선행 접근 C — PLT 유래 MHC-I / NKG2D ligand 전달 모델**: PLT가 MHC-I 분자를 CTC에 전달하거나 NKG2D ligand shedding을 유도(Placke et al. 2012). 이 모델의 한계: 부분적 설명에 그치며, CTC 자체가 어떤 immune checkpoint를 능동적으로 발현해 NK-cell을 억제하는지 규명되지 않음.

- **이 논문으로 이어지는 gap**: 저자들의 이전 연구(Sun et al. 2021, Nat Commun, ref 14)가 HCC CTC의 scRNA-seq에서 PLT 관련 유전자 농축과 불량 예후 연관성을 보고. 그 후속으로 "PLT 직접 접촉이 CTC의 어떤 immune checkpoint 유전자를 전사 수준에서 유도하고, 그것이 NK-cell 살상을 특이적으로 억제하는가"라는 미해결 질문이 이 논문의 출발점이 됨.

### 기본 개념

- **CTC (Circulating Tumor Cell)**: 원발 종양에서 탈락해 혈액에 진입한 종양세포. 본 논문에서는 EpCAM/Pan-CK/CK19+, CD45− 세포로 식별. CD41+(혈소판 마커) 공동 양성이면 PLT+CTC(PLT 부착 CTC)로 분류.
- **CD155 (PVR, Poliovirus receptor cell adhesion molecule)**: 종양세포 표면에 발현하는 immune checkpoint ligand. NK-cell/T-cell의 수용체 TIGIT(억제), CD96(억제), DNAM1/CD226(활성화)와 결합. TIGIT 결합 시 NK-cell 세포내 ITIM 도메인 활성화 → IFN-γ 분비 억제, CD107a(탈과립) 감소.
- **TIGIT (T-cell immunoreceptor with Ig and ITIM domains)**: NK-cell 및 T-cell 표면의 inhibitory receptor. CD155와 결합 시 ITIM을 통해 세포독성 기능 하향 조절. DNAM1(CD226)과 경쟁적으로 CD155에 결합.
- **FAK/JNK/c-Jun cascade**: Focal Adhesion Kinase(FAK)가 세포-세포 직접 접촉 시 활성화 → MAPK 하류로 JNK(mitogen-activated protein kinase 8, MAPK8) 인산화 → c-Jun(AP-1 전사인자 구성 요소) 인산화 → CD155 프로모터 −920∼−908 위치의 c-Jun binding site(ATGATGTCAT) 결합 → CD155 전사 활성화.
- **NK-cell 기능 마커**: IFN-γ(사이토카인 분비)와 CD107a(탈과립 지표). 두 마커 모두 PLT 처리 후 감소, CD155 knockdown 또는 α-TIGIT 처리 시 회복됨.
- **ChimeraX-i120 플랫폼**: 저자 그룹이 개발한 CTC 분리 플랫폼. 밀도 구배 + 항체 cocktail(EpCAM, Pan-CK, CK19, CD45)로 CTC를 분리하고 CellInsight CX5 High-Inclusion Screening Platform으로 스캔.

### 이 논문의 필요성

- **핵심 이유**: PLT-CTC adhesion이 CTC 자체의 immune checkpoint 발현 프로그램을 전사 수준에서 리모델링하는지가 미탐구 상태였음.
- **기존 방법으로 부족했던 지점**: 물리적 차폐 및 사이토카인 모델이 PLT 효과의 일부를 설명하나, 어떤 specific immune checkpoint 분자가 상향조절되고 어떤 NK-cell 수용체를 통해 기능을 억제하는지의 분자 특이성을 증명한 연구가 없었음.
- **이 논문이 해결하려는 방향**: PLT 직접 부착 → FAK/JNK/c-Jun → CD155 전사 활성화 → TIGIT를 통한 NK-cell 억제라는 선형 인과 축을 복수의 orthogonal 실험으로 확립. α-TIGIT 처리로 이 축을 차단하면 전이가 억제됨을 preclinical에서 증명.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: HCC 환자 혈액 CTC-PLT complex에서 NK-cell 면역 회피를 일으키는 immune checkpoint와 그 상류 신호전달 경로를 인과적으로 규명하고 차단 가능성을 보임.
- **입력**: 환자 전혈 10 mL(HCC n=37, NSCLC n=5, PDAC n=5, 건강 공여자 n=20); HCC cell lines(Hep-3B, MHCC-97L, MHCC-97H, PLC/PRF/5); patient-derived organoids(PDO-1, PDO-2, PDO-3); 건강 공여자 및 환자 분리 NK-cell; PLT(platelet-rich plasma로부터).
- **출력**: PLT+CTC 빈도, CD155 발현 변화, FAK/JNK/c-Jun 경로 활성, NK-cell 기능(IFN-γ, CD107a), 전이 부담(IVIS).
- **중요한 hidden assumption**: PLT 직접 접촉 효과를 사이토카인 효과와 분리하려면 "직접 공배양 = 접촉 있음", "간접 공배양 = 접촉 없음"이라는 가정이 완전해야 함. 간접 공배양 방법(transwell 사용 여부 등)이 본문에 구체적으로 기술되지 않음.

### 확률 / 통계학적 구조

이 논문은 실험생물학 연구로, 수학적 computational model은 없음.

- **통계 검정**:
  - Kolmogorov-Smirnov test: scRNA-seq/전사체 데이터 분산 동질성.
  - Unpaired t-test (동질 분산): 2군 비교.
  - Mann-Whitney test (비동질 분산): 비모수 2군 비교.
  - Log-rank test (Kaplan-Meier): PFS, OS 생존 분석.
  - Chi-square test: CD155 발현-PLT 부착 연관성(범주형 데이터).
- **유의 수준**: p < 0.05(*), p < 0.01(**), p < 0.001(***), p < 0.0001(****).
- **소프트웨어**: R 4.0(scRNA-seq), FlowJo V10(유세포), GraphPad Prism 7(통계), RTCA Software 1.2(xCELLigence), JASPAR(TF binding site 예측).
- **다중 비교 보정**: 본문에서 명시적 언급 없음. 미제공.

### 핵심 method insight

- **기존 방법의 한계**: 이전 연구들이 PLT-CTC 상호작용의 물리적 차폐나 사이토카인 경로에 집중했고, PLT 직접 접촉이 CTC의 immune checkpoint transcriptome을 재프로그래밍한다는 가설을 체계적으로 검증하지 않음.
- **이 논문이 바꾼 가정**: PLT의 CTC 면역 회피 기여는 사이토카인 비의존적이며, 직접 세포-세포 접촉에 의한 FAK 활성화가 필수적.
- **새로 추가한 변수 또는 구조**: JASPAR 소프트웨어로 CD155 프로모터의 c-Jun binding site를 예측 후, wild-type vs. mutant promoter luciferase assay로 기능적 결합 관계를 직접 증명.
- **이 변화가 중요한 이유**: CD155 upregulation과 NK-cell 억제 사이의 인과 관계를 knockdown, overexpression, 억제제, luciferase, in vivo 다섯 수준의 orthogonal 증거로 뒷받침.

### 이전 방법과의 차이

- **Baseline 비교 방법**: PLT-CTC 선행 연구들(Brady 2020, Stegner 2014 등).
- **공통점**: PLT 고갈(Emfret anti-PLT scavenger) 마우스 모델 활용.
- **차이점**: (1) 직접/간접 coculture를 명시적으로 분리해 contact-dependency 확인; (2) 5가지 PLT 유래 사이토카인을 각각 중화하여 사이토카인 기여 명시적 배제; (3) RNA-seq → qPCR → Western blot 3단계 + 환자 CTC IF 검증으로 단계적 증거 구성; (4) JASPAR 기반 전사인자 결합 예측 + luciferase reporter로 전사 수준 인과 관계 증명.
- **차이가 크게 나타나는 조건**: 간접 공배양에서는 CD155 단백질 증가가 없음 → PLT와의 직접 세포 접촉이 반드시 필요한 조건.

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: HCC cell lines(Hep-3B, MHCC-97L, MHCC-97H, PLC/PRF/5), PDO 3개, Balb/C + NPSG 마우스(n = 5–6/group), 환자 코호트(n = 17–37).
- **Metric**: % IFN-γ+ NK cell, % CD107a+ NK cell, Normalized Cell Index(xCELLigence), Average Radiance(IVIS bioluminescence), % apoptotic tumor cells, chi-square p-value.
- **개선된 결과**: α-TIGIT 처리로 PLT-처리 종양세포에 대한 NK-cell 기능 회복(Figures 6C–E). In vivo에서 OE-CD155 + α-TIGIT군이 OE-CD155 + PBS군보다 전이 부담 유의 감소(p < 0.01, Figure 6F).
- **Ablation 근거**: iFAK 처리 시 p-FAK, p-JNK, p-c-Jun, CD155 동시 감소(Figures 5F, G). CD155-MUT 프로모터 luciferase assay에서 c-Jun 처리 + PLT 처리 모두 유의한 활성 증가 없음(Figures 5I, J).
- **정성적 효과**: PLT 고갈 마우스 CTC에서 p-Jun 및 CD155 신호 감소(Figure 5K), in vivo H&E에서 폐 전이 병소 감소 확인.

### Method 관점의 한계

- **약한 assumption**: 간접 공배양의 물리적 분리 방법(transwell 등) 세부 기술이 본문에 없어, "간접 = 완전 비접촉"이라는 전제가 검증 불충분.
- **구현 또는 학습상의 부담**: CTC 분리가 ChimeraX-i120 전용 플랫폼 필요. PDO 배양 및 인증에 시간 소요. 실험 전반이 전문 임상 샘플 접근을 요구.
- **일반화가 불확실한 조건**: 인간화 마우스 모델에서 재현 실패(Discussion 명시). H22(murine HCC)/Balb/C 계의 in vivo 결과를 인간 NK-cell 동태로 외삽 시 주의.

---

## Results

### Dataset별 결과

#### Dataset 1 — HCC 환자 혈액 코호트 (CTC 빈도·예후)

- **Dataset**: HCC 환자 37명(CTC 검출 목적), 그 중 PFS/OS 추적 가능 20명(Dec 2021–Dec 2023, Zhongshan Hospital, Fudan University). NSCLC 5명, PDAC 5명은 cross-cancer 검증에 포함.
- **목적**: PLT-CTC adhesion의 임상적 빈도와 HCC 예후 연관성 확인.
- **사용한 데이터 규모**: PFS/OS 분석 n = 20. PLT+CTC군 n = 14, PLT−CTC군 n = 6.
- **Baseline / 비교 대상**: PLT+CTC vs. PLT−CTC 환자군.
- **Metric**: Kaplan-Meier PFS, OS; log-rank test.
- **주요 수치**:
  - CTC 양성 20명 중 PLT+CTC 비율: 70% (14/20) (Figure 1D).
  - PFS: PLT+CTC군 유의 단축, log-rank p = 0.0257 (Figure 1E).
  - OS: PLT+CTC군 유의 단축, log-rank p = 0.0459 (Figure 1F).
  - GSEA (CTC vs. primary tumor scRNA-seq): GO: Platelet Activation NES = 1.68, p = 5×10⁻³; GO: Platelet Aggregation NES = 1.86, p = 3×10⁻⁴ (Figure 1B).
- **정성 결과**: PLT+CTC군은 추적 기간 내 조기 재발/사망 비율 높음. Kaplan-Meier 곡선 초기 분리 패턴.
- **논문 주장과의 연결**: PLT-CTC adhesion이 임상적 불량 예후 지표임을 뒷받침.
- 해석: PLT−CTC군 n = 6으로 통계적 검정력 제한. 단일 기관 후향적 코호트. 교란변수(TNM 병기, AFP, 치료 프로토콜) 통제 여부 본문 미명시. 다중 비교 보정 적용 여부 미제공.

---

#### Dataset 2 — CD155 발현과 PLT 부착 상관 (환자 CTC, n = 17)

- **Dataset**: CTC 양성 17명, CTC 총 29개. 플랫폼: ChimeraX-i120 + multiplex IF.
- **목적**: PLT 부착 CTC와 비부착 CTC 간 CD155 발현율 차이 확인.
- **사용한 데이터 규모**: PLT+CTC 21개 중 CD155+ 16개(76.0%); PLT−CTC 8개 중 CD155+ 2개(25.0%).
- **Metric**: Chi-square test.
- **주요 수치**: p = 0.011 (Figure 3L). 2×2 contingency table (Figure 3L): PLT+CTC CD155+(16) vs. CD155−(5); PLT−CTC CD155+(2) vs. CD155−(6).
- **논문 주장과의 연결**: 환자 혈액 샘플에서 PLT 부착-CD155 발현 연관성 직접 확인.
- 해석: 횡단면 관찰로 인과성 증명은 아님. 소규모 검체. 선택 편향(CTC 양성인 환자 선택) 가능성 있음.

---

#### Dataset 3 — PLT 공배양에 의한 CD155 upregulation (in vitro/ex vivo)

- **Dataset**: HCC cell lines Hep-3B, MHCC-97L; PDO-1, PDO-2, PDO-3 (HCC 환자 유래). PLT 직접/간접 공배양.
- **목적**: PLT 직접 부착이 contact-dependent 방식으로만 CD155를 상향조절하는지 확인.
- **주요 수치 및 정성 결과**:
  - RNA-seq: PVR(CD155)가 면역 checkpoint 중 가장 큰 log2FoldChange (Figure 3B). 정확 fold-change는 본문 수치 미기재; Supplemental Table S3 참조.
  - qPCR: Hep-3B, MHCC-97L 직접 공배양 시 CD155 mRNA 유의하게 증가 (n = 3, Figure 3C).
  - qPCR: PDO-1, -2, -3 직접 공배양 시 CD155 mRNA 증가; 간접 공배양에서는 변화 없음 (Figure 3D).
  - Western blot: Hep-3B(Figure 3E), MHCC-97L(Figure 3F)에서 직접 공배양에서만 CD155 단백질 증가; 간접 공배양에서는 β-tubulin 대비 변화 없음.
  - Western blot: PDO-1, -2, -3 동일 패턴 (Figure 3G).
- **논문 주장과의 연결**: PLT 직접 접촉이 CD155 전사 및 단백질 수준에서 contact-dependent 방식으로 상향조절됨을 RNA·단백질·PDO 3단계에서 확인.

---

#### Dataset 4 — NK-cell 기능 assay (PLT 처리 종양세포 공배양)

- **Dataset**: Hep-3B, MHCC-97L 공배양. NK-cell 분리 출처: 건강 공여자 및 HCC 환자 혈액. xCELLigence(Roche) + flow cytometry.
- **목적**: PLT 부착이 NK-cell 살상을 억제하는지 기능적으로 확인.
- **주요 수치**:
  - Hep-3B + NK + PLT: IFN-γ+ NK cell 비율 및 CD107a+ NK cell 비율 유의 감소 vs. NK 단독군 (Figure 2F, p < 0.05–0.01).
  - MHCC-97L + NK + PLT: 동일 패턴 (Figure 2G).
  - Tumor cell apoptosis: NK + PLT + Hep-3B vs. NK + Hep-3B에서 유의 감소 (Figure 2H, p < 0.01); MHCC-97L에서도 동일(p < 0.0001).
  - CD155 knockdown(MHCC-97H, PLC/PRF/5): PLT 처리에도 불구 IFN-γ+, CD107a+ NK cell 비율 회복 (Figures 4A, B).
  - α-TIGIT: PLT 처리 종양세포에 대한 NK-cell 기능 완전 복원 (Figures 6A–D). α-CD96: 유의한 회복 없음(ns).

---

#### Dataset 5 — in vivo 전이 모델 (Balb/C, NPSG, C57BL/6J 마우스)

- **Dataset**: H22-luc(Balb/C, NPSG), Hepa1-6(C57BL/6J). n = 5–6/group.
- **목적**: PLT의 전이 촉진 효과가 NK-cell 의존적이고 CD155 의존적임을 in vivo로 검증.
- **주요 수치**:
  - NPSG(면역결핍) 마우스: PLT 고갈군과 대조군 간 IVIS 신호 차이 없음(ns, Figure 2B).
  - Balb/C: PLT 고갈군 폐 전이 Avg Radiance 유의 감소(p < 0.05, Figure 2C). NK inhibitor(anti-asailo GM1) 동시 처리 시 전이 감소 효과 역전(p < 0.001) → NK-cell 의존적.
  - PLT 고갈 + sh-CD155: 전이 감소. OE-CD155 + PLT 고갈: 전이 부담 rescue (Figure 4C).
  - OE-CD155 + α-TIGIT vs. OE-CD155 + PBS: IVIS Avg Radiance 유의 감소(p < 0.01–0.001, Figure 6F).
  - CD107a+ NK cell in lungs: PLT 고갈군에서 비율 증가(Figure 2D); OE-CD155 + α-TIGIT군에서 회복(Figure 6G).
- **정성 결과**: 폐 H&E에서 전이 병소 감소 확인(Supplemental Figures S2C, D, S6F, G).

---

#### Dataset 6 — FAK/JNK/c-Jun 경로 확인 (Western blot + luciferase)

- **Dataset**: MHCC-97L, Hep-3B, MHCC-97H. iFAK(FAK inhibitor), wild-type vs. mutant CD155 promoter luciferase reporter.
- **목적**: PLT 직접 부착이 FAK→JNK→c-Jun 경로를 활성화하고, c-Jun이 CD155 프로모터를 직접 전사 활성화하는지 인과적으로 검증.
- **주요 수치**:
  - MHCC-97L PLT 직접 공배양: p-FAK fold 3.50, p-JNK fold 3.60, CD155 fold 4.40. p-p38 및 p-ERK1/2: 변화 없음(Figure 5C).
  - iFAK 처리(MHCC-97L): p-FAK(fold 3.29→감소), p-JNK(fold 1.54→감소), CD155(fold 4.40→감소) (Figure 5D).
  - Hep-3B 동일: p-FAK fold 4.20, p-JNK fold 1.52, CD155 fold 3.56 (Figure 5E).
  - iFAK + MHCC-97L: p-FAK, p-JNK, p-c-Jun, CD155 동시 감소(Figure 5F). Hep-3B 동일(Figure 5G).
  - Luciferase: c-Jun cotransfection + CD155-WT promoter → fold change ~1.5, p < 0.0001 (Figure 5I). CD155-MUT + c-Jun: ns.
  - PLT 처리 + CD155-WT promoter: luciferase ~1.5배 증가, p < 0.01(Figure 5J). CD155-MUT: ns.
  - In vivo IF: PLT 고갈 마우스 CTC에서 p-Jun 및 CD155 신호 감소(Figure 5K).

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: PLT 직접 부착 → CD155 상향조절 → NK-cell 기능 억제 → 전이 증가 패턴이 cell line, PDO, 마우스 in vivo, 환자 CTC 4개 시스템에서 일관되게 재현됨.
- **가장 중요한 수치**: HCC CTC 양성자 70%에서 PLT 부착; 환자 PLT+CTC의 76.0% vs. PLT−CTC의 25.0%가 CD155+ (p = 0.011).
- **baseline 대비 차이**: α-TIGIT 처리가 PLT 처리 종양세포에 대한 NK-cell 기능을 PBS 대비 완전히 복원하는 반면, α-CD96는 동일 조건에서 효과 없음 → TIGIT 특이성 확인.
- **결과 해석 시 주의점**: 임상 코호트 n이 소규모(14 vs. 6 생존 분석). 수술 절제 환자 기반으로 비수술 시나리오 일반화 제한됨. 인간화 마우스 재현 실패(Discussion). 다중 비교 보정 명시 없음.

---

## Figures

### Figure 1 — PLT-CTC adhesion의 임상적 빈도 및 예후 연관성

- **이 Figure가 필요한 이유**: 논문의 임상적 출발 주장 — "HCC 환자 혈액에서 PLT-CTC adhesion이 흔하고 불량 예후와 연관된다" — 를 환자 scRNA-seq, GSEA, multiplex IF, Kaplan-Meier 4개 데이터 타입으로 뒷받침하기 위해 배치됨.
- **이 Figure가 뒷받침하는 주장**: PLT-CTC adhesion이 HCC에서 70%의 빈도로 발생하며, 임상 예후 불량과 직접 연관됨.

##### 패널별 설명
- **A**: Heat map. HCC 환자 scRNA-seq. CTC vs. primary tumor 상위 발현 유전자. ITGA2B, GP9, GSN, CD36, ITGB3, GP1BA 등 혈소판 관련 유전자가 CTC에서 선택적으로 농축.
- **B**: GSEA. GO: Platelet Activation(NES = 1.68, p = 5×10⁻³), GO: Platelet Aggregation(NES = 1.86, p = 3×10⁻⁴)이 CTC에서 유의하게 풍부.
- **C**: Multiplex IF 이미지. PLT+CTC(CD41+/EpCAM·CK·Pan-CK+/CD45−/DAPI) vs. PLT−CTC 채널 분리. Scale bar 5 μm.
- **D**: Bar plot. 20명 환자 각각의 CTC 수 및 PLT+CTC(적색, 70%) vs. PLT−CTC(청색, 30%) 비율.
- **E**: Kaplan-Meier PFS. PLT+CTC(n = 14) vs. PLT−CTC(n = 6). Log-rank p = 0.0257.
- **F**: Kaplan-Meier OS. 동일군. Log-rank p = 0.0459.

##### 본문에서 강조한 비교
- PLT+CTC군이 PLT−CTC군 대비 PFS와 OS 모두 단축 → 단순 물리적 마커가 아닌 기능적 불량 예후 인자로서의 임상적 근거.

##### 해석 시 주의점
- PLT−CTC군 n = 6으로 통계적 검정력 부족. 후향적, 단일 기관 데이터.

---

### Figure 2 — PLT 부착이 NK-cell 살상을 억제하여 전이 촉진

- **이 Figure가 필요한 이유**: PLT가 NK-cell을 경유한 면역감시 억제로 전이를 촉진한다는 기전 주장을 NPSG/Balb/C in vivo + in vitro coculture 두 시스템에서 동시에 뒷받침.

##### 패널별 설명
- **A**: In vivo 실험 설계 모식도. H22-luc 꼬리정맥 주사 → PLT scavenger 처리 → IVIS 4–6주 추적.
- **B**: NPSG(면역결핍) 마우스. PLT 고갈 vs. control IVIS + 정량. ns → NK-cell 의존적 효과.
- **C**: Balb/C(면역능력) 마우스. PLT 고갈군 폐 전이 유의 감소(p < 0.05). iNK + iPLT 동시 처리 시 역전(p < 0.001) → NK-cell 의존성 직접 증명.
- **D**: Flow cytometry. Balb/C 폐 NK-cell CD107a+ 비율. PLT 고갈군에서 CD107a+ NK 증가.
- **E**: In vitro coculture 모식도.
- **F, G**: Bar graphs. Hep-3B(F), MHCC-97L(G)에서 PLT 처리 후 IFN-γ+ 및 CD107a+ NK 비율 유의 감소.
- **H**: Apoptosis. PLT 추가 시 NK-cell 유도 종양세포 apoptosis 유의 감소(MHCC-97L, Hep-3B).

##### 본문에서 강조한 비교
- NPSG(NK-cell 없음)에서 PLT 고갈 효과 없음 vs. Balb/C에서 효과 있음 → PLT 효과가 NK-cell 경유임을 대조실험으로 확인.

##### 해석 시 주의점
- H22 세포는 murine HCC. 인간 NK-cell biology와 종별 차이 존재. n = 5–6/group으로 in vivo 소규모.

---

### Figure 3 — PLT 부착이 CTC에서 CD155를 상향조절

- **이 Figure가 필요한 이유**: PLT 부착이 어떤 immune checkpoint를 올리는지를 전사체 → mRNA → 단백질 → in vivo CTC → 환자 CTC 순서로 단계적으로 규명.

##### 패널별 설명
- **A**: In vitro/ex vivo 공배양 실험 설계 모식도.
- **B**: RNA-seq bar plot. PVR(CD155), CD276, TNFRSF14가 PLT 공배양 후 가장 크게 상향조절.
- **C**: qPCR heat map. Hep-3B, MHCC-97L 직접 공배양에서 CD155 mRNA 상승 (n = 3).
- **D**: PDO qPCR heat map. PDO-1, -2, -3 직접 공배양에서만 CD155 mRNA 상승.
- **E, F**: Western blot. Hep-3B(E), MHCC-97L(F). 직접 PLT 부착에서만 CD155 단백질 상승.
- **G**: PDO Western blot. PDO-1, -2, -3 직접 PLT 부착 시에만 CD155 상승.
- **H**: In vivo 실험 모식도. PLT scavenger vs. PBS, H22-EGFP 주입 후 CTC 분리.
- **I**: In vivo IF. PLT 고갈 마우스 CTC에서 CD155 낮음; 대조군에서 높음.
- **J**: 환자 CTC IF. PLT 부착 CTC에서 CD155 높음; 비부착 CTC에서 낮음.
- **K**: Bar graph. PLT+CTC CD155+ 76%, CD155+CTC 24% / PLT−CTC CD155+ 25%, CD155− 75%.
- **L**: Chi-square contingency table. PLT+CTC: CD155+(16), CD155−(5). PLT−CTC: CD155+(2), CD155−(6). p = 0.011.

##### 본문에서 강조한 비교
- 직접 vs. 간접 공배양에서 CD155 단백질 차이 → contact-dependent 효과. 환자 76% vs. 25% 차이 → 임상 관련성.

##### 해석 시 주의점
- Western blot 반정량적. PDO 3개는 환자 다양성의 일부만 대표.

---

### Figure 4 — CD155가 PLT 의존적 NK-cell 저항성의 직접 매개체

- **이 Figure가 필요한 이유**: CD155가 단순 상관이 아닌, NK-cell 억제의 인과적으로 필요한 분자임을 knockdown/overexpression + in vivo로 입증.

##### 패널별 설명
- **A**: MHCC-97H(CD155 high) sh-CD155 knockdown. IFN-γ+ 및 CD107a+ NK 비율 PLT 처리군에서도 회복(p < 0.05–0.0001).
- **B**: PLC/PRF/5 동일 패턴.
- **C**: In vivo IVIS. sh-CD155에서 전이 감소. OE-CD155 + PLT 고갈에서 전이 부담 rescue(n = 5).
- **D**: Flow cytometry. 폐 NK-cell CD107a+. PLT 고갈에서 증가, OE-CD155에서 감소.

##### 본문에서 강조한 비교
- CD155 knockdown이 PLT 부착에 의한 NK 기능 억제를 역전 → CD155가 필요충분 조건. OE-CD155가 PLT 고갈의 전이 억제 효과를 rescue → executor 역할 확인.

##### 해석 시 주의점
- knockdown 효율(%) 본문 미제공, Supplemental 참조 필요. In vivo n = 5, 군별 분산 큼.

---

### Figure 5 — FAK/JNK/c-Jun cascade가 CD155 전사를 조절

- **이 Figure가 필요한 이유**: CD155 upregulation의 상류 신호전달 경로를 분자 수준에서 규명. FAK→JNK→c-Jun의 인과 관계를 GO, GSEA, Western blot, JASPAR 예측, luciferase assay, in vivo IF 6개 수준으로 입증.

##### 패널별 설명
- **A**: GO-CC bar chart. PLT 공배양 MHCC-97L에서 Focal adhesion이 가장 유의하게 농축(−log₁₀p > 8).
- **B**: GSEA. MAPK signaling pathway NES = 1.89, p = 0.0014.
- **C**: MHCC-97L Western blot. PLT 직접 공배양: p-FAK fold 3.50, p-JNK fold 3.60, CD155 fold 4.40. p-p38, p-ERK1/2: 변화 없음 → JNK 특이적 활성화.
- **D, E**: MHCC-97L(D), Hep-3B(E) iFAK 처리. p-FAK, p-JNK, CD155 감소.
- **F, G**: iFAK + MHCC-97L(F), Hep-3B(G). p-FAK, p-JNK, p-c-Jun, CD155 동시 감소.
- **H**: JASPAR 예측. CD155 프로모터 −920∼−908 위치에 c-Jun binding motif(ATGATGTCAT).
- **I**: Luciferase assay. c-Jun + CD155-WT: ~1.5배 증가(p < 0.0001). c-Jun + CD155-MUT: ns.
- **J**: PLT 처리 luciferase. CD155-WT + PLT: ~1.5배 증가(p < 0.01). CD155-MUT + PLT: ns.
- **K**: In vivo IF. PLT 고갈 마우스 CTC에서 p-Jun 및 CD155 감소.

##### 본문에서 강조한 비교
- p-p38, p-ERK에 변화 없고 p-JNK만 특이적으로 증가 → PLT 부착이 MAPK 중 JNK axis만 활성화. WT vs. MUT 프로모터 luciferase assay가 c-Jun binding site 필요성을 직접 증명.

##### 해석 시 주의점
- Luciferase assay n = 3, SEM 에러바. CD155 프로모터에 다른 AP-1 결합 사이트가 존재할 가능성 미배제.

---

### Figure 6 — α-TIGIT 처리가 NK-cell 기능을 회복하고 전이를 억제

- **이 Figure가 필요한 이유**: CD155-TIGIT가 CD155-CD96보다 NK-cell 억제의 특이적 축임을 증명하고, α-TIGIT의 잠재적 치료 가치를 preclinical로 뒷받침.

##### 패널별 설명
- **A**: xCELLigence assay. MHCC-97L + NK. PLT군 Normalized Cell Index 증가(NK 살상 억제). α-TIGIT 처리로 회복(p < 0.05–0.01). α-CD96: 효과 없음(ns).
- **B**: PLC/PRF/5 동일. α-TIGIT 회복(p < 0.01), α-CD96 ns.
- **C, D**: MHCC-97L(C), Hep-3B(D). Flow cytometry. α-TIGIT로 IFN-γ+, CD107a+ NK 비율 회복.
- **E**: PDO. α-TIGIT로 IFN-γ+, CD107a+ NK 비율 회복(p < 0.001–0.0001).
- **F**: In vivo IVIS (n = 5). OE-CD155 + α-TIGIT: Avg Radiance 유의 감소 vs. OE-CD155 + PBS(p < 0.01–0.001).
- **G**: Flow cytometry. OE-CD155 + α-TIGIT군에서 폐 CD107a+ NK 비율 회복.

##### 본문에서 강조한 비교
- α-TIGIT vs. α-CD96: TIGIT만이 CD155의 NK 억제 효과를 역전 → TIGIT가 CD155의 주요 inhibitory 결합 파트너. OE-CD155 + α-TIGIT in vivo에서 PLT 고갈 수준으로 전이 감소.

##### 해석 시 주의점
- DNAM1(CD226, activating receptor for CD155)에 대한 영향도 미미함을 Supplemental에서 확인. α-TIGIT는 R&D Systems 실험용 항체로, 임상 tiragolumab과 동일하지 않음.

---

### Figure 7 — Graphical Abstract

- **이 Figure가 필요한 이유**: PLT→FAK/JNK/c-Jun→CD155→TIGIT→NK-cell 억제→전이의 전체 기전 흐름을 독자가 한 번에 파악하도록.
- **내용**: (좌) PLT 없는 조건 — NK-cell이 CTC를 살상. (중) PLT 부착 → FAK/JNK/p-Jun 활성화 → CD155 upregulation → TIGIT 결합 → NK-cell 억제 → 전이 성공. (우) α-TIGIT 처리 → CD155-TIGIT 차단 → NK-cell 재활성화 → 전이 억제.

---

## Tables

본문에 정식 Table이 없음. 환자 임상 정보 상세: Supplemental Table S1. CTC 분류 데이터: Supplemental Table S2. 전사체 raw 데이터: Supplemental Table S3(GSA-Human HRA007585, https://ngdc.cncb.ac.cn/gsa-human). CD155 knockdown/overexpression 세부: Supplemental Table S4.

---

## Supplementary Information

- **Supplemental Tables**: S1(37명 HCC 환자 임상 정보), S2(CTC 분류 상세), S3(RNA-seq raw data, GSA-Human HRA007585), S4(CD155 knockdown/overexpression 세부). 접근 링크: http://links.lww.com/HEP/I470–I475.
- **Supplemental Figures S1–S11**: NSCLC/PDAC CTC PLT 부착(S1), NPSG/Balb/C 면역 분석(S2), cytokine neutralization(S3–S4), CD155 knockdown/overexpression(S5–S6), ex vivo NK-cell 결과(S7), FAK/JNK inhibitor in vivo(S8), DNAM1 관련 실험(S9), PLT 원심 부분 활성화 검증(S10), PLT 활성화 상태 독립성(S11).
- **Data availability**: Supplemental Table S3 raw sequence data GSA-Human(HRA007585) 공개. https://ngdc.cncb.ac.cn/gsa-human

---

## 분석 자체에 대한 메모

- HCC 코호트 생존 분석에서 PLT−CTC군 n = 6으로 통계적 검정력이 낮음. 현재 p = 0.04–0.03 수준이며, 교란변수 보정이 없는 단변량 비교임에 주의.
- CD155 외에 CD276도 RNA-seq에서 상향조절됨(Figure 3B). PLT 부착이 CD155 단일 checkpoint만 올리는 것은 아닐 가능성 — 저자들이 이를 CD155에 집중해서 탐구했지만, CD276 등 다른 경로의 기여는 미탐구.
- 인간화 마우스 재현 실패(Discussion, ref 35): Balb/C in vivo 결과의 인간 NK-cell 생물학으로의 직접 외삽 한계. 인간 NK-cell 기반 전임상 모델 부재가 regulatory 관점에서 약점.
- α-TIGIT 실험에 사용된 항체(R&D Systems #MAB7267-100)는 임상 개발 중인 tiragolumab과 별도 시약. 본 논문 결과가 임상 tiragolumab 유효성 예측의 근거로 직접 활용될 때 주의 필요.
- MORPHEUS-liver trial(NCT04524871)과의 연결이 Discussion에 언급되나, CTC CD155 상태와 tiragolumab 반응을 직접 연결하는 임상 데이터는 아직 없음.
