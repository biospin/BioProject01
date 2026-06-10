# hawkins-2025-her2-emt-mammary — Academic Lens

> 근거: 전문 PDF `sources/hawkins-2025-her2-emt-mammary.pdf` (12 pages). 본 분석은 PDF 원문에 기반하며 abstract 기반 이전 버전을 덮어씀.

---

## Limitations

### 저자가 명시한 한계

- **자연 발생 EMT 기전 조사 범위 외**: 저자들은 EMT의 분자 기전을 조사하는 것이 목적이 아니라 EMT가 HER2 발현에 미치는 효과를 자본화하는 것이 목적이라고 Discussion에서 명시. "Our studies were also not designed to investigate the mechanism of EMT induction."
- **TGFβ1 대 serum starvation 단독 비교 없음**: 실험의 대조군은 serum starvation을 받지 않았다. "Our controls were not subject to serum starvation since our study was not designed to compare EMT induction by TGFβ1 v serum starvation."
- **HER2 silencing이 resistance의 일부 기전**: "The silencing of HER2 expression may be one of many possible mechanisms accounting for resistance to HER2-targeting therapies." HER2 shedding, altered HER2 signaling, HER2 neutralizing miRNAs [refs 39–43] 등 다른 기전 공존 가능성 인정.
- **Epigenetic silencing 기전 미규명**: Discussion에서 possible mechanisms (miRNA, DPAGT1 등)을 언급하지만 본 연구에서 직접 측정하지 않음.

### 분석자가 판단한 한계

- **부족한 점 1 — "Epigenetic silencing" 제목의 과장**: 논문 제목에 "epigenetic silencing"이 명시되어 있지만 DNA methylation(bisulfite sequencing, methylation array), histone modification(ChIP-seq), chromatin accessibility(ATAC-seq) 등 epigenetic layer를 직접 측정한 결과가 전혀 없다.
  - 왜 중요한가: epigenetic silencing과 transcriptional repression은 동일하지 않다. mRNA·단백질 소실이 chromatin remodeling에 의한 것인지, miRNA에 의한 post-transcriptional regulation인지, transcription factor 결합 감소인지 구분되어야 기전적으로 의미 있다.
  - 어떤 증거가 부족한가: HER2 promoter의 CpG methylation 또는 H3K27me3 ChIP-qPCR 최소 수준의 epigenetic 측정.

- **부족한 점 2 — 소표본 (n=5 HER2 증폭 MC cases)**: Table 1의 핵심 결과가 5 cases에서만 확인. MC 자체가 희귀(유방암의 ~1%)하고 HER2 증폭은 그 5–10%이므로 100 cases MC 코호트에서 5 cases는 구조적으로 작은 숫자다.
  - 왜 중요한가: p-value 미제공 상태에서 5 cases의 일관성만으로 "direct evidence"를 주장하는 것은 표본 크기가 결론 강도를 제한.
  - 어떤 증거가 부족한가: 다기관 검증 코호트 또는 TCGA/GEO의 MC RNA-seq data에서 동일 패턴 확인.

- **부족한 점 3 — 단일 세포주**: HTB20 한 가지 세포주로 실험적 EMT 효과 검증. BT-474, SK-BR-3, JIMT-1 등 다른 HER2 증폭 세포주에서 재현 여부 미확인.

- **부족한 점 4 — p-value 미제공**: "All stated or calculated differences implied differences of statistical significance, assessed by two-tailed Student's t test as well as ANOVA"라고 기술하지만 구체적 수치 일절 미제공. Table 1 자체도 비통계적 수치 표. 독자가 통계 검증력을 독립적으로 평가할 수 없음.

- **부족한 점 5 — HER2 silencing 가역성 미제공**: EMT가 HER2를 silencing한다면, MET(mesenchymal-to-epithelial transition) 시 HER2가 재발현되는지가 치료 내성 이해에 결정적이지만 이 논문에서는 다루지 않음.

### 설명이 매끄럽지 않은 지점

- **"자연 발생 EMT → HER2 silencing" 인과 방향**: 관찰 연구는 MC 조직의 epithelial vs. mesenchymal 구역을 한 시점에서 비교한 것으로, EMT가 HER2 sosilencing을 *일으킨다*는 인과 방향은 추론이다. HER2가 낮은 세포가 더 쉽게 mesenchymal 분화를 거쳤을 가능성(역인과)을 배제하는 실험이 없다.
  - 현재 논문이 제시한 근거: TGFβ1 처리 실험(Dataset 4)이 인과 방향을 지지하는 가장 강한 근거. HTB20에서 TGFβ1이 HER2 발현이 이미 높은 상태에서 처리 후 소실되므로 "EMT가 HER2를 끈다"는 방향 지지.
  - 더 필요해 보이는 근거: EMT 유도 전·후 time-course (6h, 12h, 24h, 48h)에서 HER2 mRNA 변화 추적. EMT reprogramming을 epigenetic inhibitor(EZH2 inhibitor, DNMT inhibitor)로 차단했을 때 HER2 silencing이 방지되는지.

- **Mary-X 데이터 일부 재사용**: Fig. 2 caption이 "Reproduced in part from Figs. 1 and 3 [ref 16] with explicit permission from MDPI"로 명시. 이전 연구에서 이미 발표된 데이터를 재확인 목적으로 포함했으나, 새 실험 데이터와 구분이 명확하지 않음.

### 정리되지 않은 질문

- 질문 1: HER2 silencing의 구체적 epigenetic 기전은 무엇인가 — DNA methylation인지, PRC2-mediated H3K27me3인지, miR-221/222 같은 특정 miRNA인지?
- 질문 2: TGFβ1 처리를 중단하거나 EMT 억제제(예: TGFβR inhibitor)를 투여하면 HER2 발현이 회복되는가 (reversibility)?
- 질문 3: HER2 증폭 MC에서 HER2 ADC 치료를 받은 환자에서 mesenchymal 구역의 biopsied material은 HER2 IHC가 0인 상태로 측정될 경우, ADC 효과가 epithelial 구역에 한정되는가?
- 질문 4: TCGA BRCA 데이터에서 HER2 amplified + mesenchymal signature high 샘플에서 HER2 expression이 실제로 낮은지 re-analysis 가능?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: HER2 증폭 MC에서 in vivo 조직을 LCM으로 직접 분리해 "FISH 증폭 보존 + IHC/mRNA 소실"을 확인한 것이 이 논문의 핵심 기여. Bioinformatic 추론에서 in vivo 직접 증거로의 이행. TGFβ1 실험으로 인과성 보강.

- **다음 논문으로 이어질 아이디어**:
  - HER2 promoter의 epigenetic 변화(CpG methylation, H3K27me3) 측정으로 "epigenetic silencing" 기전 직접 규명.
  - EZH2 inhibitor (tazemetostat) 처리 시 EMT-induced HER2 silencing이 방지되는지 — PRC2 의존성 확인.
  - 다양한 HER2 증폭 세포주(BT-474, SK-BR-3, JIMT-1) + 다양한 EMT 유도 방법(EGF, Wnt3a, hypoxia)에서 일반화 검증.
  - HER2 silencing의 가역성: TGFβR inhibitor 처리 후 HER2 회복 time-course.
  - TCGA BRCA MC subset이나 GEO의 MC bulk RNA-seq/WES로 HER2 amplification vs. HER2 expression dissociation 재분석 (in silico validation).

- **설명을 더 매끄럽게 만들 방법**: 
  - 역인과 배제를 위해 isogenic 세포주(HER2 과발현을 ectopic으로 유도한 세포)에서 EMT 처리 실험.
  - Time-series EMT induction에서 EMT marker 증가와 HER2 감소 순서 확인(어느 것이 먼저?).

- **우선순위가 높은 후속 실험 / 분석**:
  1. HER2 promoter bisulfite sequencing (HTB20 EMT 처리 전후) — 2주 내 수행 가능.
  2. SK-BR-3 + TGFβ1 처리에서 동일 패턴 재현 — 단일 세포주 한계 극복.
  3. TGFβ1 처리 시간별 HER2 mRNA 변화 + CDH1/TWIST1 동시 추적 (time-course).

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- **§Abstract/Conclusion**: "These studies provide direct evidence that both naturally occurring and induced EMT results in epigenetically silencing of HER2 overexpression."
  - 사용 시나리오: 본인 introduction에서 *EMT가 HER2 발현을 소실시킨다는 in vivo 직접 증거*를 한 문장으로 인용할 때.
  - BibTeX key: `@hawkins2025her2emmammary`

- **§Conclusion**: "In essence EMT converts a HER2 positive MC to triple negative."
  - 사용 시나리오: HER2 ADC resistance 맥락에서 EMT에 의한 표적 소실을 극적으로 표현할 때. CTC heterogeneity 논의에서 HER2 IHC 불일치 설명에 활용.
  - BibTeX key: `@hawkins2025her2emmammary`

- **§Discussion**: "The silencing of HER2 expression may be one of many possible mechanisms accounting for resistance to HER2-targeting therapies."
  - 사용 시나리오: HER2 ADC 내성 기전 diversity를 다루는 섹션에서 epigenetic silencing을 복수 기전 중 하나로 위치시킬 때.
  - BibTeX key: `@hawkins2025her2emmammary`

### 인용 가능 수치

- **Table 1**: HER2 증폭 MC 5 cases — carcinoma area HER2 IHC +1~+3 vs. sarcoma area IHC 0 (FISH ratio 동등). 수치는 case별로 표에 있음.
  - 사용 시나리오: 본인 paper의 "HER2 expression-amplification dissociation" baseline 수치 인용. "5 of 100 MC cases showed HER2 amplification with complete loss of protein expression in mesenchymal areas (Table 1, Hawkins 2025)"
  - BibTeX key: `@hawkins2025her2emmammary`

- **Fig. 6**: HTB20 + TGFβ1 — HER2 mRNA level ~100→~0.5 (log scale, Fig. 6). 정확한 fold-change 미제공이나 "dramatically reduced" 기술.
  - 사용 시나리오: in vitro EMT가 HER2 mRNA를 실질적으로 소실시킨다는 실험 결과 인용.
  - BibTeX key: `@hawkins2025her2emmammary`

### 인용 가능 Figure/Table

- **Fig. 3C·D**: HER2 FISH(증폭 동등) + HER2 IHC(mesenchymal 소실)를 같은 시야에서 보여주는 대표 이미지.
  - 사용 시나리오: 본인 review paper나 slide에서 "epigenetic silencing" 개념 시각화.
  - BibTeX key: `@hawkins2025her2emmammary`

- **Table 1**: 12 cases의 epithelial vs. mesenchymal HER2 FISH/IHC 대조 수치.
  - 사용 시나리오: 본인 방법론·임상 배경 섹션에서 "HER2 expression heterogeneity within a single tumor" 사례 제시.
  - BibTeX key: `@hawkins2025her2emmammary`
