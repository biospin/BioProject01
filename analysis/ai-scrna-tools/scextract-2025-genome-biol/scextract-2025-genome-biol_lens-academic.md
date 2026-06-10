# scExtract — Lens: Academic

> Wu Y. and Tang F., 2025. Genome Biology 26:174. DOI: 10.1186/s13059-025-03639-x
> Citation key: `@wu2025scextract`
>
> **근거 자료**: `scextract-2025-genome-biol_core.md` + 원문 PDF. 외부 지식 사용 시 `외부 맥락:` 표기.

---

## Limitations

### 저자가 명시한 한계

- **LLM 출력 variability**: annotation은 LLM 특성상 run마다 달라질 수 있다. 저자는 confidence scoring과 re-annotation round로 완화하지만, biologically ambiguous datasets에서 variability가 집중된다고 명시(Discussion).
- **Text-to-embedding 모델의 domain specificity 부족**: 현재 사용 중인 일반 목적 embedding 모델(OpenAI text-embedding-3-large)은 cell type 생물학적 유사도보다 언어적 유사도를 반영할 수 있다. 저자는 domain-specific 또는 cell-type fine-tuned embedding 모델의 필요성을 인정(Discussion).
- **Biased incorrect labeling에 대한 scanorama-prior 취약성**: annotation이 기존 cell type 쪽으로 편향되어 잘못 지정된 경우, scanorama-prior는 두 cell type 사이의 outlier로 위치시키는 결과를 낸다. Cellhint-prior는 이 시나리오에서 더 robust (Fig. S12C).
- **LLM annotation 결과 manual 검토 권고**: 저자는 특히 single-dataset 사용 시 생성된 log file을 직접 검토할 것을 권고.

### 분석자가 판단한 한계

- **부족한 점 1 — ground truth의 품질**: benchmark에 사용된 cellxgene curator 레이블은 curated되었으나, 이 레이블 자체가 논문 저자의 annotation을 기준으로 하므로 inter-annotator agreement나 외부 기관의 independent validation이 없다. scExtract가 비교 기준보다 더 정확한 생물학적 annotation을 했어도 metric이 이를 반영하지 못할 수 있다.
- **왜 중요한가**: annotation accuracy 주장의 강도가 ground truth 품질에 직결된다. 특히 "scExtract가 original article의 세분성에 더 가깝다"는 주장은 Fig. 2B의 cell type 수 상관관계로만 뒷받침되며, 개별 세포 수준의 정확도는 별개 문제다.
- **어떤 증거가 부족한가**: 동일 dataset에 대해 두 명 이상의 전문가가 독립적으로 annotation한 결과와 scExtract 결과의 비교. 또는 perturb-seq나 FACS-sorted population처럼 experimental ground truth가 있는 dataset에서의 validation.

- **부족한 점 2 — integration 성능의 규모 의존성 이론화 부재**: 저자는 "dataset 수 > 4 또는 평균 cell 수/dataset < 50k → scanorama-prior, 그 외 → cellhint-prior"를 실용 guideline으로 제시하지만, 이 분기점의 이론적 근거가 없다. 경험적 관찰에 불과하며, 다른 tissue type이나 protocol에서 다를 수 있다.
- **왜 중요한가**: 새 데이터셋에서 어떤 방법을 선택해야 하는지 불확실성이 남는다.
- **어떤 증거가 부족한가**: 규모 조건을 체계적으로 변화시킨 ablation (예: 동일 데이터를 다른 dataset 수/cell 수 조합으로 subsampling해 분기점 탐색).

- **부족한 점 3 — 계산 비용의 dataset 수 의존성**: 본문에 단일 dataset당 비용($1, 20min)만 제시. 14개 dataset을 통합할 때 총 비용과 시간이 선형으로 증가하는지, bottleneck이 어디인지 명시되지 않음.
- **왜 중요한가**: 100개 이상 dataset 통합을 고려하는 팀에서 비용 예측이 불가능.
- **어떤 증거가 부족한가**: 데이터셋 수 × 비용/시간 scaling curve.

- **부족한 점 4 — single-cell annotation의 cluster 경계 의존성**: scExtract의 annotation이 clustering granularity에 의존한다. 클러스터 수를 잘못 추론하거나 논문에 명시되지 않은 경우, annotation 결과 자체가 달라진다. 이 "clustering → annotation" 전파 오류에 대한 체계적 분석이 없다.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: "article-derived prior knowledge가 annotation 정확도를 향상시킨다"는 주장을 Fig. 2F(with/without context 비교)로 지지하는데, 이 비교는 context 추가 vs. 제거만 보여줄 뿐 "어떤 정보가 결정적이었는지" (파라미터 추출 vs. marker gene background vs. clustering granularity 추론)를 분리하지 않는다.
- **현재 논문에서 제시한 근거**: Fig. 2F에서 context 추가 시 유의한 정확도 향상 (p < 0.02).
- **더 필요해 보이는 근거**: 논문 텍스트의 어느 부분(Methods section, Results section, title/abstract)이 성능 향상에 가장 기여하는지 ablation. 예: Methods만 제공 vs. background만 제공 vs. 전체.

- **연결이 약한 주장 2**: Fig. 6의 CXCL14⁺ psoriatic keratinocyte 발굴을 scExtract의 생물학적 발견 능력의 근거로 제시하지만, 이 subpopulation이 scExtract 없이는 발견되지 않았다는 직접 비교가 명확하지 않다. Fig. 6D vs. 6E에서 scanorama-prior가 subpopulation을 분리하고 scanorama가 분리하지 못한다는 것은 보이지만, 분석자가 원본 scanorama 결과로도 post-hoc으로 같은 subpopulation을 찾을 수 있었는지 확인되지 않았다.

### 정리되지 않은 질문

- 질문 1: scExtract가 annotation한 cell type과 independent wet lab validation (FACS, immunostaining)이 있는 데이터셋에서 annotation 정확도는 어떤가?
- 질문 2: LLM이 논문에서 추출한 전처리 파라미터와 실제 저자의 파라미터 사이의 agreement rate는 얼마인가? (systematic extraction accuracy 측정)
- 질문 3: 동일한 pipeline을 multi-omic 데이터(ATAC+RNA)에 적용할 수 있는가? 현재는 scRNA-seq 전용.
- 질문 4: annotation 오류가 downstream biological analysis (differential expression, trajectory, cell-cell communication)에 얼마나 전파되는가?
- 질문 5: 논문이 English가 아닌 경우 LLM extraction 성능은 어떻게 되는가?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: LLM을 단순한 cell type annotation 도구가 아니라 "논문을 읽고 pipeline 전체를 재현하는" 에이전트로 쓴 첫 번째 실용 사례. text-to-embedding기반 annotation similarity를 배치 보정 알고리즘의 prior로 연결하는 integration 구조는 개념적으로 깔끔하고 후속 확장 가능성이 높다.

- **다음 논문으로 이어질 아이디어**:
  - 1. **multiome (ATAC+RNA) 지원**: scExtract의 LLM agent가 ATAC peak annotation 또는 chromatin accessibility를 함께 추출해 multi-omic prior를 구성하면, 우리 프로젝트의 chromatin-transcription lag 정량화에 직접 연결 가능.
  - 2. **domain-specific embedding**: cell type name → biological embedding으로 Cell Ontology 기반 fine-tuned 모델을 사용하면 $M_{IJ}$ matrix의 biological specificity 향상 가능. Cell Ontology hierarchy를 거리 함수로 사용하는 방법과 비교.
  - 3. **LLM annotation uncertainty를 downstream analysis에 전파**: confidence level을 soft label로 weighted 사용. annotation이 불확실한 세포에서 DE analysis, trajectory의 robustness 평가.
  - 4. **ablation: 논문 어느 부분이 annotation에 기여하는가**: Methods 섹션만, abstract만, background만 제공 시 성능 비교.

- **설명을 더 매끄럽게 만들 방법**:
  - Fig. 3B의 정량 수치를 본문 텍스트에 명시 (현재 figure에만).
  - scanorama-prior vs. cellhint-prior 선택 guideline의 theoretical derivation 추가 또는 broader dataset 실험으로 경험적 robustness 강화.
  - CXCL14⁺ subpopulation 발굴에서 scExtract 기여가 "prior-aware integration" 때문인지 단순히 "더 좋은 clustering"인지 분리.

- **우선순위가 높은 후속 실험 / 분석**:
  - 우리 HSPC multiome dataset에 scExtract(annotation-only pipeline)를 적용 → LLM annotation vs. 우리의 manual annotation 비교.
  - cellxgene benchmark 외 FACS-sorted ground truth dataset (예: bone marrow CD34⁺ sorted populations)에서 external validation.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Background (p.2): "Current data sharing protocols only mandate submission of raw sequencing data, without requiring processed expression matrices."
  - 사용 시나리오: 공개 scRNA-seq 데이터의 annotation 부재 문제를 소개하는 introduction 절에서 현황 기술용.
  - BibTeX key: `@wu2025scextract`

- §Background (p.4): "scExtract requires only raw expression matrices and article content as input, automatically performing preprocessing, clustering, and annotation operations aligned with the original methods described in the articles."
  - 사용 시나리오: LLM-based automated analysis pipeline을 소개하는 methods section에서 관련 도구 설명용.
  - BibTeX key: `@wu2025scextract`

- §Results (p.10): "scExtract can complete all process procedure of a dataset in less than 20 min … at a cost of less than one dollar, with no additional computational resources required if using web API."
  - 사용 시나리오: computational efficiency 또는 scalability 주장의 benchmark 수치 인용.
  - BibTeX key: `@wu2025scextract`

- §Discussion (p.19): "We propose that annotation and integration processes in constructing integrated datasets are mutually reinforcing."
  - 사용 시나리오: annotation-integration co-design 개념을 도입할 때 conceptual framing.
  - BibTeX key: `@wu2025scextract`

- §Conclusions (p.20): "By eliminating labor-intensive manual preprocessing and enabling cost-effective integration of published datasets, scExtract democratizes large-scale single-cell analysis."
  - 사용 시나리오: LLM 기반 자동화가 single-cell 분석을 민주화한다는 narrative에서 supporting reference.
  - BibTeX key: `@wu2025scextract`

### 인용 가능 수치

- dataset당 처리 시간 < 20분, 비용 < $1 (§Results, Fig. S3E)
  - 사용 시나리오: 본인 pipeline의 cost/time efficiency benchmark 비교 기준.
  - BibTeX key: `@wu2025scextract`

- text-to-embedding 정확도에서 scExtract > GPTCelltype, p < 5×10⁻⁵ (§Results, Fig. 2H)
  - 사용 시나리오: LLM annotation의 article context 효과를 주장할 때.
  - BibTeX key: `@wu2025scextract`

- 피부 atlas 440,000 cells / 14 datasets 통합 (§Results)
  - 사용 시나리오: large-scale scRNA-seq integration의 규모 기준점.
  - BibTeX key: `@wu2025scextract`

### 인용 가능 Figure/Table

- Fig. 1B (workflow overview)
  - 무엇을 보여주는지: LLM agent 기반 전자동 scRNA-seq annotation + prior-informed integration pipeline의 구조.
  - 사용 시나리오: 본인 review 또는 grant proposal에서 LLM-for-single-cell 분야 현황 도식으로 참조.
  - BibTeX key: `@wu2025scextract`

- Fig. 2H/I (annotation accuracy comparison)
  - 무엇을 보여주는지: scExtract vs. GPTCelltype vs. reference transfer 방식의 annotation 정확도 정량 비교.
  - 사용 시나리오: LLM annotation 성능 비교 표/그림이 필요한 경우.
  - BibTeX key: `@wu2025scextract`
