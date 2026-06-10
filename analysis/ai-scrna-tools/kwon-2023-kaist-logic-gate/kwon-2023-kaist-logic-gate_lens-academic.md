# Lens — Academic: kwon-2023-kaist-logic-gate

## Limitations

### 저자가 명시한 한계

- **binarized 발현의 dropout 민감성**: "The residual expression of some of the candidate genes in normal cells may be masked by the dropout effect. Thus, final candidates should be pruned by careful inspection of individual cells." 실제 미발현인지 기술 dropout인지 구별 불가.
- **mRNA ≠ protein**: "not all mRNAs are translated into proteins, the findings derived from our meta-atlas should be validated at the protein level." 실제로 CLDN3/4는 CITE-seq 항체가 작동하지 않아 IHC로 대체.
- **epitope–paratope interaction**: "protein expression has been validated, the epitope–paratope interaction between the corresponding antibody and target protein should be determined for CAR engineering." 단순히 단백질이 발현되는 것 이상의 CAR 설계 요건.
- **sample heterogeneity**: "our sample-wise analysis shows that the combinatorial targets identified by our approach might be ideal for most tumors but are not applicable in certain patient cases." BRCA 등에서 individual sample 수준 변동성 큼. Patient subtyping 필요성 언급.

### 분석자가 판단한 한계

- **부족한 점 1 — tumor cell 분리 신뢰도**: CopyKAT을 이용한 aneuploidy 기반 tumor cell 분리는 폴리플로이드 정상세포(예: 간세포)와 diploid 종양세포를 오분류할 위험이 있다. Tumor ECF 계산의 분모 자체가 오염될 경우 false-high ECF가 생성된다.
  - 왜 중요한가: ECF criteria(>70%)가 파이프라인의 핵심 기준이므로, tumor cell labeling 오류가 선발 후보 신뢰도에 직접 영향.
  - 어떤 증거가 부족한가: CopyKAT 정확도를 독립 방법(예: inferCNV, CONICS)과 cross-validate한 결과가 본문에 없음.

- **부족한 점 2 — 정상 atlas의 완전성**: 12개 정상 장기, 111 cell type 포함이지만 일부 조직(예: 생식기, 내분비선)은 누락. 특정 희귀 정상 cell type에서의 off-tumor 발현이 탐지되지 않을 수 있음.
  - 왜 중요한가: NOT gate 설계에서 정상세포 ECF를 낮게 추정하면 clinical safety를 과대평가.
  - 어떤 증거가 부족한가: 논문은 정상 atlas 범위의 제한을 명시하지 않고, "12 normal organs"로만 기술.

- **부족한 점 3 — in vivo 기능 검증 없음**: 선발된 CAR switch 후보가 실제로 tumor killing efficacy와 off-tumor toxicity 개선을 달성하는지 동물 실험이나 in vitro cytotoxicity assay 결과가 없다.
  - 왜 중요한가: CITE-seq + IHC는 발현 지도 검증이지 기능 검증이 아님. CAR 효능은 epitope accessibility, steric hindrance, CAR construct design 등에 의존.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: Fig. 4a에서 "기존 임상 타겟 95개 중 7개만 tumor ECF > 50%"를 PCASA 우월성 근거로 제시하지만, 95개 타겟 선발 기준이 논문에서 충분히 설명되지 않음. "clinically tested or identified by bulk expression profiling"이라는 기술만 있음.
  - 현재 논문에서 제시한 근거: Fig. 4a에서 직접 시각 비교.
  - 더 필요해 보이는 근거: 95개 타겟 ECF 계산의 원본 reference 목록과 선발 기준 명시 (Supplementary Table에도 부분적으로만 제공).

- **연결이 약한 주장 2**: CNN Grad-CAM weight를 "gene pair의 combinatorial 기여도"로 해석하지만, Grad-CAM은 last convolution layer의 gradient를 기반으로 하므로 non-linear interaction effect만을 포착. 두 유전자의 독립적 기여가 아닌 조합 기여임을 명확히 구분하는 설명이 부족.

### 정리되지 않은 질문

- 질문 1: PCASA가 scATAC-seq 또는 multiome 데이터를 통합하면 chromatin accessibility 기반 항원 발현 예측이 가능한가? CAR 타겟 선발에 epigenetic layer를 추가할 수 있는가?
- 질문 2: AND gate 후보에서 두 항원의 protein isoform이나 glycosylation 상태가 항체 결합에 영향을 줄 수 있는가? 현재 분석은 mRNA만 고려.
- 질문 3: 10개 미만 샘플 암종(예: ATC n=5, PC n=2)의 ECF 추정 신뢰도는? 소수 샘플에서의 ECF variance 추정치 없음.
- 질문 4: FOLR1-not-CD52 NOT gate의 경우 CD52가 종양-침윤 림프구에서 발현될 때, CAR T cell 자체의 CD52 발현에 의한 fratricide가 발생할 수 있는가?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: 단일세포 발현 atlas + ECF 개념 + RF-CNN 두 단계 파이프라인으로 AND/OR/NOT CAR switch 후보를 체계적으로 순위화하는 최초의 범암종 계산 프레임워크. PCASA 코드와 meta-atlas를 공개하여 재현성 기반 마련.

- **다음 논문으로 이어질 아이디어**:
  1. **CAR T functional validation**: PCASA 상위 후보(예: CLDN3-and-CLDN4 AND gate CAR, FOLR1-not-CD52 NOT gate CAR)를 실제로 construct해 tumor organoid 또는 PDX 마우스에서 efficacy + toxicity 평가. Dataset: OV patient-derived organoid.
  2. **Spatial transcriptomics 통합**: 종양 내 공간적 항원 발현 이질성을 AND gate 설계에 반영 — 특정 영역의 항원 co-expression 패턴이 overall ECF와 다를 수 있음. Xenium or Visium 사용.
  3. **scATAC 기반 예측**: 항원 유전자의 promoter/enhancer accessibility로 항원 발현 on/off를 미리 예측 → ECF 안정성 분석. 특히 epigenetic silencing으로 인해 tumor subclone에서 항원이 down-regulation되는 immune escape 시나리오 평가.
  4. **Non-OV 암종 임상 검증**: CRC CEACAM5-not-CA4, LIHC 조합 후보에 대한 단백질 수준 CITE-seq + IHC 검증. 현재는 OV + CRC만 검증.
  5. **Inter-patient ECF variance 모델**: BRCA처럼 intertumoral heterogeneity가 큰 암종에서 sample-wise ECF distribution (mean ± SD)을 제시하고, 어느 subgroup에서 타겟이 적합한지 patient stratification criterion 개발.

- **설명을 더 매끄럽게 만들 방법**: CopyKAT tumor cell labeling 정확도를 독립 벤치마크로 검증한 결과를 supplementary에 추가하면 ECF 계산 신뢰도가 크게 향상됨. 또한 95개 기존 타겟 목록과 선발 기준을 Supplementary에 명시적으로 기재 필요.

- **우선순위가 높은 후속 실험 / 분석**: CLDN3/4 AND gate CAR construct + OV organoid cytotoxicity assay (다음 논문의 핵심). 또는 scATAC + PCASA 통합을 통한 epigenetic 안정성 평가.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction p.1594: "average expression levels, even when retrieved from separated tumor and normal cells, can be misleading in identifying and evaluating therapeutic targets."
  - 사용 시나리오: 본인 ADC/CAR 타겟 선발 방법론 section에서 bulk 기반 접근의 한계를 지적할 때.
  - BibTeX key: `@kwon2023logicgate`

- §Results p.1594: "We named this index ECF (expressing cell fraction) and used it to evaluate therapeutic target candidates in terms of the proportion of target and off-target cells that express the gene."
  - 사용 시나리오: ECF 개념을 단독 지표로 사용하거나 확장할 때 최초 정의 인용.
  - BibTeX key: `@kwon2023logicgate`

- §Discussion p.1602: "expression logic must be determined not only for tumor cells but also for normal cells. For example, NOT-gated CARs require the AND expression of the activating and repressing antigen in normal cells for their protection from off-tumor cytotoxicity."
  - 사용 시나리오: NOT gate CAR 설계 원리를 소개할 때.
  - BibTeX key: `@kwon2023logicgate`

### 인용 가능 수치

- AUC > 0.99 for all cancer types in RF model (Supplementary Table 4)
  - 사용 시나리오: 단일세포 기반 세포 분류기 성능 벤치마크로 인용.
  - BibTeX key: `@kwon2023logicgate`

- FOLR1-not-CD52: tumor ECF 100%, normal ECF 3.9% (Fig. 4b, OV NOT gate)
  - 사용 시나리오: NOT gate 전략의 효과를 수치로 보여줄 때.
  - BibTeX key: `@kwon2023logicgate`

- CLDN4: CRC 19/20 (95%) IHC 양성 (Discussion p.1602)
  - 사용 시나리오: CRC CAR 타겟으로서 CLDN4 근거.
  - BibTeX key: `@kwon2023logicgate`

### 인용 가능 Figure/Table

- Figure 1b (워크플로우 개요도)
  - 두 단계 RF→CNN 파이프라인의 overall flow를 보여주는 schematic.
  - 사용 시나리오: 본인 ADC/CAR 타겟 선발 방법론 소개 슬라이드.
  - BibTeX key: `@kwon2023logicgate`

- Figure 3a (population vs. single-cell level AND/OR 구별 개념도)
  - 왜 단일세포 수준 logic이 필요한지를 직관적으로 설명.
  - 사용 시나리오: CAR therapy 설계 배경 설명, BD 미팅용 pitch 슬라이드.
  - BibTeX key: `@kwon2023logicgate`
