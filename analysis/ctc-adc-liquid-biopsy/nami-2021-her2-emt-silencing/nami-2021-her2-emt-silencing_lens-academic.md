# Lens — Academic
## nami-2021-her2-emt-silencing

---

### Limitations

#### 저자가 명시한 한계

- 저자는 Discussion에서 EMT와 HER2 발현 사이의 negative feedback loop의 *구체적 분자 기전*—HER2 overexpression이 EMT를 어떻게 유도하는지, EMT가 ERBB2 chromatin을 어떻게 silencing하는지—이 아직 규명되지 않았다고 명시했다. "We recommend investigating the mechanism of the negative feedback loop to understand how HER2 overexpression induces EMT, and how EMT causes ERBB2 gene silencing, leading to the emergence of tumor cells resistant to HER2-targeted therapies."(p.10)
- 저자는 epigenetic silencing이 "authentic mechanism"이라고 주장하지만, 이 논문에서 chromatin 상태와 EMT 유도를 직접 연결하는 perturbation 실험(예: HDAC inhibitor 처리 후 ERBB2 발현 회복 확인)을 수행하지 않았다.

#### 분석자가 판단한 한계

- **부족한 점 1: 정량 데이터 부재 (핵심 실험)**: BT474 EMT 유도 실험에서 trastuzumab binding 감소를 immunofluorescence 이미지로만 제시했다. FACS 정량(MFI, % positive cells), Western blot HER2 단백질 정량, 또는 binding assay(Biacore, ELISA) 없이 Figure 3C의 결론은 정성적 근거에 그친다.
  - **왜 중요한가**: 논문의 핵심 functional claim(EMT → trastuzumab binding 감소)이 정량 데이터로 뒷받침되지 않아 reviewer 및 downstream 인용에서 약점이 된다.

- **부족한 점 2: ChIP-seq 비교의 배치 효과**: 히스톤 mark ChIP-seq 데이터가 서로 다른 연구실(주로 Franco et al. 2018 데이터셋)에서 생산되어 기술적 배치 효과(antibody lot, ChIP protocol, sequencing depth)가 미보정된 채 시각적 비교만 이루어졌다. 정량 통계(peak intensity, RPKM, ChIP/input ratio)를 세포주 간 직접 비교하는 방법론적 기술이 없다.
  - **왜 중요한가**: HER2-high vs. HER2-low 차이가 실제 chromatin 상태 차이인지 기술적 배치 편향인지 구별하기 어렵다.

- **부족한 점 3: Multiple testing 미보정**: METABRIC n=1,904에서 ERBB2 vs. 24개 marker(12 epithelial + 12 mesenchymal) 상관 분석에 FDR 보정이 적용되지 않았다. $p < 0.0001$이 대부분이지만, $R^2$ 값이 낮아(0.005–0.12) 효과 크기가 매우 작다.
  - **왜 중요한가**: 작은 $R^2$와 다중 비교는 임상적 의미 과장 우려 — 단순 "correlates with" 수준을 넘어 해석 시 주의.

- **부족한 점 4: 세포주 모델의 일반화 한계**: Dataset 6(TGF-β1 처리)은 A549 폐암 세포주로 수행. 유방암과 폐암에서 ERBB2 chromatin regulation이 동일하다는 가정이 논문에서 검증되지 않았다. 또한 BT474 EMT 유도 실험은 replicate 수가 명시되지 않았다.

- **부족한 점 5: Causal mechanism 증거 부재**: 이 논문의 모든 chromatin 데이터는 상관 분석이다. EMT TF들이 ERBB2 chromatin의 histone modifier를 recruit하는 직접 증거(co-immunoprecipitation, ChIP-reChIP)가 없다. 따라서 "chromatin silencing이 EMT의 결과"라는 방향성은 지지되지만 "EMT TF가 HDAC를 recruit해 ERBB2 chromatin을 닫는다"는 mechanistic causal claim을 뒷받침하지는 못한다.

#### 설명이 매끄럽지 않은 지점

- **연결 1 (약한 연결)**: Figure 2E에서 H3K9me, H3K27me3 둘 다 낮다는 결과를 "activator absence = silencing 기전"으로 해석하는데, 이는 H3K27me3가 없다는 것과 chromatin이 "accessible"하다는 것을 직접 연결하지 못한다. PRC2-independent chromatin compaction이나 CTCF insulators가 관여할 가능성을 배제하지 않았다.
  - 현재 논문에서 제시한 근거: H3K9me, H3K27me3 ChIP-seq이 양군 모두 낮음.
  - 더 필요해 보이는 근거: ATAC-seq 정량 비교(open chromatin fraction 수치), CTCF insulator binding 차이 분석.

- **연결 2 (약한 연결)**: ERBB2 promoter에 mesenchymal TF(E2F1)가 결합한다는 결과(Figure 1G)가 ERBB2 발현 억제와 어떻게 연결되는지 기전이 불명확하다. E2F1은 일반적으로 전사 활성화 TF로 알려져 있어, ERBB2 chromatin에서의 E2F1 enrichment가 억제 기전이 되려면 repressor complex와의 association을 보여야 한다.
  - 현재 논문에서 제시한 근거: 시각적 ChIP-seq track 비교.
  - 더 필요해 보이는 근거: E2F1 perturbation(knockdown, overexpression) 후 ERBB2 발현 변화.

#### 정리되지 않은 질문

- 질문 1: EMT 과정에서 어떤 epigenetic enzyme(HDAC, EZH2, LSD1 등)이 ERBB2 chromatin에 recruited되는가? 특정 억제제 처리 시 ERBB2 발현이 회복되는가?
- 질문 2: ERBB2 chromatin silencing이 가역적인가? MET(mesenchymal-to-epithelial transition) 유도 시 HER2 발현과 trastuzumab 감수성이 회복되는가?
- 질문 3: CD44+/CD24− BCSC population에서 ERBB2 chromatin 상태가 어떠한가? CTC에서의 ERBB2 chromatin 상태를 측정할 수 있는 방법이 있는가?
- 질문 4: 이 논문에서 제시된 31개 mesenchymal TF 중 ERBB2 chromatin silencing에 필수적인 TF는 무엇인가?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: HER2 내성 발생을 DNA methylation이 아닌 histone modification + chromatin accessibility 변화로 설명하는 개념 틀을 공개 데이터 기반으로 제시했다. "Activator mark 부재가 silencing 기전"이라는 관찰은 HER2 chromatin biology 이해에 기여.

- **다음 논문으로 이어질 아이디어**:
  - BT474 또는 SKBR3에서 EMT 유도 후 H3K27ac ChIP-seq + ATAC-seq을 자체 생성하여 ERBB2 cis-regulatory element의 activity dynamics를 정량화.
  - HDAC inhibitor(예: vorinostat) 또는 EZH2 inhibitor(예: tazemetostat) + trastuzumab 병용 처리 시 EMT-induced BT474에서 HER2 발현 및 trastuzumab binding 회복 확인.
  - scRNA-seq + scATAC-seq을 HER2+ 유방암 환자 종양에 적용해 ERBB2 chromatin state가 single cell 수준에서 EMT score와 어떻게 연관되는지 확인.
  - CTC에서 ERBB2 promoter chromatin accessibility를 cfDNA open chromatin (cell-free ATAC 또는 APOBEC-based assay)으로 측정하는 liquid biopsy 접근.

- **설명을 더 매끄럽게 만들 방법**:
  - BT474 EMT 실험에 FACS 정량 + Western blot 추가.
  - ChIP-seq 비교에 정량 통계(DESeq2 또는 DiffBind peak analysis) 추가.
  - E2F1 knockdown 후 ERBB2 발현 변화 확인으로 인과 연결.

- **우선순위가 높은 후속 실험 / 분석**:
  1. BT474/SKBR3 EMT 전후 자체 H3K27ac ChIP-seq + ATAC-seq (우선순위 최상: 논문 핵심 주장의 직접 데이터).
  2. Epigenetic inhibitor + trastuzumab 병용 실험 (translational 가치 최상).
  3. scATAC-seq on HER2+ primary tumors (임상 relevance).

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction (p.2): "Approximately 60–70% of HER2-positive breast cancer patients develop de novo resistance to trastuzumab; this is partially due to the loss of HER2 expression in their tumor cells during treatment."
  - 사용 시나리오: HER2 ADC 내성 발생 빈도를 introduction에서 제시할 때. Background에서 치료 한계 강조.
  - BibTeX key: `@nami2021her2emt`

- §Discussion (p.9): "Our results suggest that EMT of HER2-positive breast cancer cells results in abrogation of HER2 expression by chromatin-based epigenetic silencing of the ERBB2 gene that leads to trastuzumab resistance."
  - 사용 시나리오: EMT-driven HER2 target loss를 epigenetic 기전으로 기술할 때. ADC resistance 맥락.
  - BibTeX key: `@nami2021her2emt`

- §Discussion (p.10): "The significant depletion of HER2 in the mesenchymal-like cells inside the tumor can take place by chromatin-based epigenetic silencing of the ERBB2 gene during EMT."
  - 사용 시나리오: HER2 ADC의 tumor heterogeneity 문제(EMT subpopulation의 HER2 소실)를 기술할 때.
  - BibTeX key: `@nami2021her2emt`

- §Discussion (p.10): "EMT and mesenchymal-like cells, particularly cancer stem cells, can serve as bona fide targets to overcome drug resistance in breast cancers."
  - 사용 시나리오: Cancer stem cell을 치료 타깃으로 제안하는 연구 또는 제안서에서 선행 근거.
  - BibTeX key: `@nami2021her2emt`

### 인용 가능 수치

- METABRIC n=1,904에서 ERBB2 vs. ZEB1 $R^2 = 0.1260$, $p < 0.0001$ (Figure 1B)
  - 사용 시나리오: ZEB1과 ERBB2 발현의 역상관 관계를 대규모 임상 데이터로 인용.
  - BibTeX key: `@nami2021her2emt`

- "60–70% of HER2-positive breast cancer patients develop de novo resistance to trastuzumab" (p.2)
  - 사용 시나리오: 치료 저항성 규모를 수치로 제시.
  - BibTeX key: `@nami2021her2emt`

- HCC-1954: 240 promoter-enhancer loops; MCF7: 11 loops (Figure 2F)
  - 사용 시나리오: HER2-high 세포에서 ERBB2 chromatin topology의 방대함을 illustrate할 때.
  - BibTeX key: `@nami2021her2emt`

### 인용 가능 Figure/Table

- **Figure 3D** (Summary schematic)
  - EMT 진행에 따른 epithelial phenotype ↓, ERBB2 chromatin activity ↓, HER2 발현 ↓, anti-HER2 drug resistance ↑의 연쇄를 한 도식으로 요약.
  - 사용 시나리오: HER2 내성 기전을 설명하는 slide 또는 review figure로 재사용 가능. 개념 도식으로 인용.
  - BibTeX key: `@nami2021her2emt`

- **Figure 2E** (H3K9me, H3K27me3 양군 모두 낮음)
  - ERBB2 silencing이 "activator absence"에 의한 것임을 보이는 비교. 반직관적 결과로 주목.
  - 사용 시나리오: Epigenetic silencing 기전을 논의할 때 repressor 관여 없음을 보이는 근거로.
  - BibTeX key: `@nami2021her2emt`
