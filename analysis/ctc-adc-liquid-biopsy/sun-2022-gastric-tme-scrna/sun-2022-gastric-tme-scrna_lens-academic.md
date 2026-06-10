# Lens — Academic
# sun-2022-gastric-tme-scrna (@sun2022gastrictme)

---

## Limitations

### 저자가 명시한 한계

- **환자 수 부족**: 10명 코호트로 결과가 탐색적(exploratory)이며 대규모 scRNA-seq 코호트에서 검증 필요하다고 저자가 Discussion에서 명시(p14).
- **공간 정보 부재**: scRNA-seq은 세포의 공간적 위치 정보를 제공하지 못한다. 저자는 향후 spatial transcriptomics와 scATAC-seq으로 이를 보완할 계획을 밝혔다(p14).
- **TASC 기능 검증 미완**: TASCs의 종양 촉진 특성은 PDX·PDO·GEMM 등 모델 시스템에서 추가 검증이 필요하다고 명시(p14).
- **분자 메커니즘 부재**: GC TME 세포 표현형 재형성의 underlying molecular mechanism 및 조절 경로는 genetically engineered mouse models 등으로 추가 연구가 필요하다(p14).

### 분석자가 판단한 한계

**한계 1: MuSiC deconvolution의 self-reference 문제**
- **부족한 점**: TCGA-STAD 예후 분석에서 TASC 비율을 MuSiC로 추정할 때, 동일 연구의 scRNA-seq 데이터가 reference panel로 쓰였다. 같은 연구에서 정의된 세포 유형이 deconvolution reference가 되면 순환 편향(circular bias)이 생길 수 있다.
- **왜 중요한가**: Fib_1·SMC_1의 HR 추정값(1.8)이 편향된 deconvolution에 근거한다면, 예후 연관성의 신뢰도가 낮아진다.
- **어떤 증거가 부족한가**: 독립 scRNA-seq reference panel을 사용한 재분석, 또는 세포 유형별 단백질/IHC 마커로 bulk cohort에서 직접 정량한 검증.

**한계 2: CellPhoneDB L-R 분석의 causality 부재**
- **부족한 점**: L-R 쌍 분석은 동일 환자 내 공동발현 패턴 기반의 통계적 association이다. IL34-CSF1R, NECTIN2-TIGIT 등의 기능적 중요성이 in vivo 차단 실험(anti-NECTIN2·TIGIT 병용 등)으로 확인된 것은 아니다.
- **왜 중요한가**: TME 상호작용 허브라는 주장이 임상적 치료 타겟으로 연결되려면 차단 실험에서 실제 효과가 있어야 한다.
- **어떤 증거가 부족한가**: IL34-CSF1R axis를 CSF1R 억제제로 차단했을 때 Mφ_APOE 감소 및 T세포 기능 회복 여부.

**한계 3: Tc17→exhaustion trajectory의 인과적 증거 부재**
- **부족한 점**: Diffusion map pseudotime과 clonotype 공유는 Tc17 → Exhaustion 방향의 가능성을 보여주지만, 실제 세포 분화 경로를 증명하지 않는다. 두 증거 모두 관찰적(associative)이다.
- **왜 중요한가**: Alternative exhaustion trajectory라는 핵심 claim이 이 논문의 novelty인데, 실제 전환을 in vitro (혹은 mouse model) lineage tracing으로 확인하지 않았다.
- **어떤 증거가 부족한가**: Fate-mapping (CreERT2/Rosa26-YFP 등) 또는 in vitro culture에서 IL-17+ CD8+ T세포를 exhaustion 자극으로 처리했을 때 전환 여부.

**한계 4: Tc17의 IL22/IL26 분비 기능 미확인**
- **부족한 점**: IL22·IL26이 Tc17에서 분비된다는 주장의 근거가 scRNA-seq 발현 데이터에 머문다. 단백질 수준(ELISA, intracellular cytokine staining)에서 Tc17이 IL22/IL26을 실제로 생산한다는 증거가 없다. 저자 스스로 TCGA-STAD bulk에서 IL22·IL26 발현이 낮다고 인정했다(Discussion p14).
- **왜 중요한가**: IL17+ 세포를 치료 타겟으로 제시하는 논문의 핵심 기능적 주장.
- **어떤 증거가 부족한가**: 환자 종양 조직에서 분리한 Tc17 세포의 ex vivo 사이토카인 분비 측정.

**한계 5: 단일 기관·치료 미경험 bias**
- **부족한 점**: 수술절제 가능한 치료 미경험 위암 환자에 한정. 면역요법 중·후 또는 진행성 위암의 TME는 반영되지 않는다.
- **왜 중요한가**: 면역요법 반응을 예측하는 바이오마커나 병합 치료 전략에 이 atlas를 적용하려면 treated cohort에서의 검증이 필요하다.

### 설명이 매끄럽지 않은 지점

**지점 1: Tc17 세포의 T세포 억제 vs. 종양 촉진 이중 역할**
- **연결이 약한 주장**: 논문은 Tc17이 MDSCs를 유도해 cytotoxic CD8+ T세포를 억제하고(외부 참고문헌 38-39 인용), 동시에 IL17/IL22/IL26으로 종양 세포를 직접 촉진한다고 주장한다.
- **현재 논문에서 제시한 근거**: 수용체 발현 데이터(TCGA-STAD), KEGG enrichment, 기존 문헌 인용. 본 데이터에서 직접 검증한 것은 아님.
- **더 필요해 보이는 근거**: Tc17-MDSC 축을 이 데이터셋에서 직접 보여주는 L-R 분석 결과 (Fig. 8에서 Tc17과 MDSCs 간 L-R 분석은 없음).

**지점 2: LAMP3+ DC 기원(cDC2)의 RNA velocity 신뢰성**
- **연결이 약한 주장**: RNA velocity (scVelo)로 LAMP3+ DC가 cDC2에서 유래한다고 추론했지만, scVelo는 spliced/unspliced 비율에서 추론하므로 데이터 스파스성이 높을 때 신뢰성이 낮다.
- **현재 논문에서 제시한 근거**: Fig. 4h-i velocity plot.
- **더 필요해 보이는 근거**: 단일세포 pseudo-bulk DEG 분석에서 cDC2와 DC_LAMP3 전환 마커 확인; 또는 DC 발달 lineage tracing.

### 정리되지 않은 질문

- 질문 1: Tc17 세포가 exhaustion 전 단계에서 임상적으로 유효한 타겟인가? 즉, 이 세포를 제거/차단하면 cytotoxic T세포 기능이 회복되는가, 아니면 오히려 exhaustion을 늦출 가능성도 있는가?
- 질문 2: Mφ_APOE 아형이 위암 외 다른 고형암(BRCA 포함)에서도 유사하게 존재하고 TASCs와 피드백을 형성하는가? Cross-cancer atlas 비교가 필요.
- 질문 3: TASC(Fib_1, SMC_1) 불량 예후 연관성이 HER2 양성·MSI-H 등 분자적 subtype과 독립적인가, 아니면 특정 subtype에서만 나타나는가?
- 질문 4: GC08처럼 Wnt 신호 이상 케이스(Supplementary Note 3)가 예후·치료 반응과 어떻게 연결되는가?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: 위암 TME의 전 구획을 가장 큰 matched 규모(166,533세포, 삼중 조직)로 단일세포 해상도에서 정량하고, Tc17→exhaustion alternative trajectory라는 새 T세포 소진 경로를 clonotype+velocity 이중 증거로 제안한 것. TASC가 예후 인자임을 scRNA-seq + TCGA-STAD 연계로 검증한 것도 실용적 기여.

- **다음 논문으로 이어질 아이디어**:
  1. Tc17 세포의 IL17/IL22/IL26 분비 기능을 단백질 수준에서 확인하고, PDX 또는 GEMM에서 Tc17 제거 효과를 검증하는 in vivo 연구.
  2. Spatial transcriptomics로 TASC-Mφ_APOE-DC_LAMP3의 공간적 조직화를 규명하고, IL34-CSF1R axis 차단 실험으로 기능적 의존성 입증.
  3. 면역요법(pembrolizumab) 투여 전·후 동일 환자 matched scRNA-seq으로 Tc17 비율·trajectory 변화가 반응 여부와 연관되는지 분석.
  4. 여러 암종(BRCA, 폐암, 대장암) cross-cancer scRNA-seq 비교로 TASC+Mφ_APOE 피드백 루프의 보편성 검증.

- **설명을 더 매끄럽게 만들 방법**:
  - Tc17 종양 촉진 주장에 Tc17와 MDSCs 간 L-R 분석 결과 추가.
  - MuSiC deconvolution 결과를 독립 IHC 정량(자동화 병리 이미지 분석)으로 교차 검증.
  - EOMES/RUNX2 knockdown in vitro 실험으로 trajectory-specific TF 주장 강화.

- **우선순위가 높은 후속 실험 / 분석**:
  1. **즉시**: Tc17 세포의 ex vivo 사이토카인 분비 측정 (IL17, IL22, IL26 protein) — 환자 종양 조직 신선 분리.
  2. **단기**: Spatial transcriptomics (Visium/Xenium) 적용으로 TASC-TAM 공간 조직화 확인.
  3. **장기**: anti-NECTIN2·anti-TIGIT 병용 + CAR-T 또는 IL-17 중화 병합 전략의 preclinical 효과 검증.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction: "the intertumoral variation and individual variation of cellular composition were associated with survival, highlighting an unmet need to dissect the complex and dynamic biological characteristics of the tumor microenvironment (TME) to exploit advanced interventions to combat it."
  - 사용 시나리오: 위암 또는 고형암 ADC 연구의 introduction에서 TME 이질성이 치료 개발의 장벽임을 justification할 때.
  - BibTeX key: `@sun2022gastrictme`

- §Results (stromal compartment): "The cell type proportions in TCGA-STAD were estimated by MuSiC… we found that both of Fib_1 and SMC_1 was associated with a worse prognosis"
  - 사용 시나리오: CAF/기질세포 예후 영향을 다루는 논문의 Background 또는 validation 섹션에서.
  - BibTeX key: `@sun2022gastrictme`

- §Results (Tc17): "Tc17 cells constitute more than 1% of the total tumor infiltrated T cell population in 8 out of the 10 patients"
  - 사용 시나리오: IL-17 신호나 Tc17 관련 연구에서 위암에서 Tc17의 실제 빈도를 인용할 때.
  - BibTeX key: `@sun2022gastrictme`

- §Discussion: "Our results indicate that IL17+ cells may promote tumor progression through IL17, IL22, and IL26 signaling, highlighting the possibility of targeting IL17+ cells and associated signaling pathways as a therapeutic strategy to treat GC."
  - 사용 시나리오: IL-17 axis 타겟 치료전략 논문의 rationale에서.
  - BibTeX key: `@sun2022gastrictme`

- §Discussion (limitation): "scRNA-seq lacks the crucial information of spatial distribution and chromatin accessibility of the various types of cells. In the future, we plan to apply spatial transcriptomics and scATAC-seq to dissect the positional relationship…"
  - 사용 시나리오: scRNA-seq 한계를 multi-omic approach로 보완하는 논문의 motivation에서.
  - BibTeX key: `@sun2022gastrictme`

### 인용 가능 수치

- 166,533세포, 10 GC 환자, 삼중 매칭 (§Results, Fig. 1b)
  - 사용 시나리오: GC scRNA-seq atlas 규모 비교 표에서 baseline으로 인용.
  - BibTeX key: `@sun2022gastrictme`

- Fib_1 HR = 1.8, p = 0.0019; SMC_1 HR = 1.8, p = 0.009 (TCGA-STAD, Fig. 3l)
  - 사용 시나리오: CAF/기질세포 예후 영향 논문에서 위암 specific baseline으로 인용.
  - BibTeX key: `@sun2022gastrictme`

- IL17RA p = 1.5e-9, IL17RB p = 3.2e-17 (종양 vs. 정상, TCGA-STAD, Fig. 5h)
  - 사용 시나리오: IL-17 수용체 발현 상향을 설명할 때 수치 인용.
  - BibTeX key: `@sun2022gastrictme`

### 인용 가능 Figure/Table

- Figure 8a (L-R interaction dot plot, §세포 간 상호작용)
  - TASC-TAM-DC_LAMP3 상호작용 허브를 시각화한 가장 포괄적인 Figure.
  - 사용 시나리오: TME 상호작용 네트워크를 설명하는 리뷰·학회 발표 슬라이드에서.
  - BibTeX key: `@sun2022gastrictme`

- Figure 6j-m (trajectory + pseudotime, §Tc17 exhaustion)
  - cytolytic vs. Tc17-exhaustion 두 경로를 나란히 비교한 직관적 Figure.
  - 사용 시나리오: T세포 exhaustion 다양성을 논의하는 논문 또는 발표에서.
  - BibTeX key: `@sun2022gastrictme`
