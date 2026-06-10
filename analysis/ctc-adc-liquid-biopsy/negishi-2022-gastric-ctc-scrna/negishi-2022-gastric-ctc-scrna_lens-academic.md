# Lens — Academic
# negishi-2022-gastric-ctc-scrna

## Limitations

### 저자가 명시한 한계

- **소규모 코호트**: 분석에 사용된 CTC 수(n = 47)와 환자 수(n = 27)가 작아 large-scale clinical study가 필요하다고 저자 스스로 명시 (Discussion 후반).
- **marker gene validation 필요**: subgroup 식별에 사용된 유전자들은 본 논문에서 검증을 위한 large-scale clinical study가 수행되지 않았으며 추가 검증 예정.
- **혈소판-CTC 상호작용 메커니즘**: 혈소판 부착 CTC (Subgroup B)에서 관찰된 TGF-β/SMAD + NF-κB 경로 연결은 in vitro, mouse model 선행연구(ref. 51, 52)에 근거한 추론이며, 본 논문에서 직접 기능 실험으로 검증되지 않았다.
- **EMT 획득 정확한 메커니즘 미규명**: CTC에서 EMT 유도 메커니즘에 혈소판이 관여한다고 제안하나 결론적 증거는 제시되지 않았다.

### 분석자가 판단한 한계

- **부족한 점 1 — 인과 추론 부재**: Subgroup A의 전사 활성화 패턴과 화학내성의 연관은 치료 교체 횟수 overlay(Supplementary Fig. 7B)와 간단한 관찰 수준. Kaplan–Meier, log-rank test, Cox proportional hazard 같은 통계적 분석이 없다. OS 비교 역시 Supplementary Table 1에 수치만 있고 통계 검정 미수행.
- **왜 중요한가**: 화학내성 CTC subgroup 주장이 논문의 가장 중요한 임상적 의미인데, 이를 뒷받침하는 통계적 근거가 매우 약하다. 소수 환자에서의 관찰을 생물학적 결론으로 제시하는 것은 독자가 받아들이기 어렵다.
- **어떤 증거가 부족한가**: 서브그룹 레이블과 OS/PFS의 log-rank 분석; 다변량 분석에서 CTC subgroup이 독립 예후 인자인지 여부; 치료 전후 같은 환자의 longitudinal CTC 비교.

- **부족한 점 2 — Subgroup B의 기술적 혼입 가능성**: Subgroup B의 PF4, PPBP, ITGA2B 등 혈소판 마커 고발현이 CTC에 혈소판이 실제로 결합된 생물학적 현상인지, 혈액 처리 과정에서 혈소판 RNA가 CTC에 혼입된 기술적 artifact인지 구별이 어렵다. nFeature가 낮은 것도 이 가능성을 배제하기 어렵게 한다.
- **왜 중요한가**: 혈소판-CTC 상호작용은 논문의 핵심 biological claim 중 하나이며, 이것이 artifact라면 Subgroup B 전체 해석이 흔들린다.
- **어떤 증거가 부족한가**: 공초점 현미경 등 이미징으로 CTC에 혈소판이 물리적으로 부착된 것 확인; 혈소판 제거 후 재sequencing; 혈소판 spike-in 실험으로 RNA 혼입 정도 정량화.

- **부족한 점 3 — Single-cell WTA의 gene body 3' 편향**: CTC에서 SNU-1보다 강한 3' 편향 관찰. 저자는 apoptosis에 의한 mRNA 분해로 해석하나, poly-A tailing WTA 자체의 3' 편향과 구별이 어렵다. 낮은 평균 transcript 수(4064 ± 1967 vs. 4376–12,084/세포주)는 분석 감도 제한을 시사한다.

- **부족한 점 4 — RPM 1.0 threshold의 arbitrary 설정**: 미발현 기준 RPM < 1.0의 생물학적·통계적 근거가 제시되지 않았다. 이 threshold를 다르게 설정하면 검출 유전자 수·서브그룹 분류가 달라질 수 있다.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: "혈소판이 EMT를 유도한다" — 본 논문에서 Subgroup B의 TGF-β/SMAD 및 NFKB1A 발현이 관찰된 것을 근거로 하지만, Subgroup B와 Subgroup A가 UMAP에서 분리된 별개 클러스터라는 점이 역설적이다. 혈소판 부착이 EMT 유도 intermediate 단계라면, EMT 완료된 Subgroup A와 혈소판 부착 단계의 Subgroup B가 서로 연속체여야 한다. 두 클러스터의 명확한 분리는 대신 두 가지 독립적 CTC 상태를 시사할 수 있다.
- **현재 논문에서 제시한 근거**: 4C의 violin plot에서 TGFB1, SPARC, ITGA2가 Subgroup A에서도 일부 발현.
- **더 필요해 보이는 근거**: Pseudotime 분석(Monocle 등)으로 Subgroup B → Subgroup A의 전이 trajectory 존재 여부 검증.

- **연결이 약한 주장 2**: "Subgroup C CTC = 불량 예후" — n = 2에 근거. Supplementary Table 1에서 G12 (OS 27일), G23 (OS 10일)만 Subgroup C 포함. 통계 검정 없이 이를 결론으로 제시하는 것은 과도하다.

### 정리되지 않은 질문

- **질문 1**: Subgroup A CTC가 화학내성과 연관된다면, 치료 시작 전 → 1차 치료 실패 후 같은 환자에서 longitudinal CTC 서브그룹 변화가 있는가? 이를 추적했다면 인과 방향성에 더 강한 근거가 된다.
- **질문 2**: Subgroup B가 혈소판 부착 artifact가 아닌 진짜 생물학적 CTC state라면, 혈소판 제거 전후 동일 CTC의 재sequencing으로 발현 변화를 확인할 수 있는가?
- **질문 3**: WTA에서 CTC의 낮은 transcript 수는 RNA quality 문제인가, 아니면 EMT 진행 세포의 실제 낮은 전사 활성인가?
- **질문 4**: MCA 포어 크기(8 µm)가 모든 위암 CTC를 포착하는가? CTC 크기 분포에 따라 소형 CTC의 누락 가능성 존재.

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: 위암에서 최초로 단일 CTC 전사체 분석을 수행하여 EMT 기반 3개 서브그룹 구조를 제시했다. EpCAM-independent size-based 분리가 mesenchymal CTC 포함 다양한 표현형 포착에 유효함을 보였다. Subgroup A–화학내성, Subgroup C–불량 예후 association hypothesis는 후속 연구의 출발점이 된다.
- **다음 논문으로 이어질 아이디어**:
  - 100+ CTC 분석 가능한 확장 코호트로 서브그룹 분류의 재현성 및 OS/PFS와의 통계적 연관성 (log-rank, multivariate Cox) 검증.
  - Longitudinal 설계: 1차 치료 전 → 1차 치료 실패 후 같은 환자에서 CTC 서브그룹 dynamics 추적.
  - Subgroup B 혈소판 부착 artifact 여부: FACS 정렬 후 platelet-attached vs. platelet-free CTC 비교sequencing.
  - Pseudotime 분석(Monocle 또는 Scanpy trajectory)으로 B → A 전이 경로 존재 여부 탐색.
  - in vitro: 혈소판 co-culture 후 위암세포주의 EMT marker 변화 → TGFB1/NF-κB 경로 의존성 검증 (TGF-β inhibitor, IκB kinase inhibitor).
- **설명을 더 매끄럽게 만들 방법**: Subgroup A = 화학내성 claim에 통계 검정 추가. Subgroup B = 혈소판 artifact 배제 실험 추가. Pseudotime으로 B → A 연속성 또는 독립성 명확히.
- **우선순위가 높은 후속 실험 / 분석**:
  1. 확장 코호트 (n > 100 환자) CTC 서브그룹 분류 + 임상 outcome 연관 통계 분석.
  2. 혈소판 부착 artifact 배제를 위한 FACS 정렬 + re-sequencing.
  3. in vitro 혈소판-위암세포 co-culture → TGF-β/SMAD + NF-κB 기능 검증.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction: "transcriptome analysis of single CTCs has only been reported for a limited number of cancer types, such as multiple myeloma, breast, hepatocellular, and prostate cancer"
  - 사용 시나리오: CTC scRNA-seq 연구의 미개척 암종을 서술할 때 위암 포함 적용 범위 제한을 근거로 인용.
  - BibTeX key: `@negishi2022gastricctcscrna`

- §Results (Discussion): "The detection rate of CTC in gastric cancer was remarkably high compared to previous reports (11–85%)"
  - 사용 시나리오: EpCAM-independent size-based CTC 분리의 우수성을 주장하는 방법론 paper에서 비교 baseline으로 인용.
  - BibTeX key: `@negishi2022gastricctcscrna`

- §Discussion: "CTCs exhibit cell cycle arrest and are associated with resistance to chemotherapy"
  - 사용 시나리오: CTC의 화학내성·dormancy 가설을 소개하는 background section에서 인용.
  - BibTeX key: `@negishi2022gastricctcscrna`

- §Discussion: "platelet adhesion initiates a signal transduction, which leads to the induction of EMT"
  - 사용 시나리오: 혈소판-CTC 상호작용 메커니즘 section에서 위암 evidence로 인용. 단, 이 주장이 논문 내에서 기능 실험으로 검증되지 않았음을 함께 명시할 것.
  - BibTeX key: `@negishi2022gastricctcscrna`

### 인용 가능 수치

- QC pass rate 43.8% (49/112 CTC), 환자 검출률 96% (26/27) — §Results Fig. 2B.
  - 사용 시나리오: size-based CTC 분리의 sensitivity를 EpCAM 기반 방법과 비교하는 분석에서.
  - BibTeX key: `@negishi2022gastricctcscrna`

- GCM cDNA yield 80.6 ± 33.6 ng vs. micromanipulation 40.3 ± 29.4 ng (p = 0.003) — Supplementary Fig. 3A.
  - 사용 시나리오: 하이드로겔 기반 단일세포 분리의 WTA 수율 우수성을 방법론 paper에서 baseline으로 인용.
  - BibTeX key: `@negishi2022gastricctcscrna`

- Subgroup B GO: platelet degranulation p = 1.64E-07 — §Results Fig. 5B.
  - 사용 시나리오: 혈소판-CTC 상호작용의 전사체 evidence를 제시할 때.
  - BibTeX key: `@negishi2022gastricctcscrna`

### 인용 가능 Figure/Table

- Figure 3B (§Results)
  - EMT score scatter plot: CTC 대부분이 세포주보다 더 mesenchymal 방향에 분포.
  - 사용 시나리오: 위암 CTC EMT 상태를 시각적으로 요약하는 review 또는 소개 slide에서 재현.
  - BibTeX key: `@negishi2022gastricctcscrna`

- Figure 4A (§Results) UMAP 서브그룹 시각화
  - CTC와 세포주가 UMAP에서 분리되는 것 + 3 서브그룹 구조.
  - 사용 시나리오: 단일세포 전사체 기반 CTC 분류 접근법을 소개하는 논문 도입부에서.
  - BibTeX key: `@negishi2022gastricctcscrna`
