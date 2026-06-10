# scassist-2025-bioinformatics_lens-academic.md

Citation: `@nagarajan2025scassist` — DOI: 10.1093/bioinformatics/btaf402

---

## Limitations

### 저자가 명시한 한계

- LLM의 파라미터 추천은 training data에서 학습된 generalized pattern에 기반하며, 특정 dataset의 실제 생물학적 이질성을 반드시 반영하지 않을 수 있음. 저자는 추천을 "starting point"로 취급하고 기존 방법으로 검증할 것을 권고.
- LLM 버전 변화로 인해 미래 응답 예측 불가. 저자는 3개월마다 모니터링·패키지 업데이트 공약.

### 분석자가 판단한 한계

- **파라미터 추천의 downstream 검증 부재**
  - 부족한 점: LLM이 추천한 QC 임계값, normalization 방법, clustering resolution이 실제로 더 나은 생물학적 결과(예: 더 정확한 cell type 구분, 더 낮은 doublet rate, 더 나은 trajectory)를 낳는지 검증하지 않는다.
  - 왜 중요한가: "추천이 합리적으로 들린다(human evaluator 만족)"와 "추천이 실제로 더 낫다(downstream biology 개선)"는 근본적으로 다른 주장이다. 본 논문은 전자만 평가했다.
  - 어떤 증거가 부족한가: 다른 파라미터 추천 방법(예: 고정 휴리스틱, 사용자 경험 기반 선택)과 비교한 downstream clustering quality metric(예: silhouette score, adjusted Rand index) 또는 biological marker enrichment 결과.

- **평가 설계의 이해상충 구조**
  - 부족한 점: 전문가 평가 8명 중 senior 2명이 평가 대상 워크플로우의 원저자. 독립 외부 평가자가 아닌 내부 평가.
  - 왜 중요한가: 저자가 작성한 표준 workflow report를 저자가 평가하는 구조는 결과 편향 가능성이 있다.
  - 더 필요해 보이는 근거: 해당 연구실과 무관한 외부 bioinformatician 평가단의 독립 평가.

- **GPTCelltype 비교의 정량 부재**
  - 부족한 점: SCassist_analyze_and_annotate()와 GPTCelltype의 비교가 "highly concordant"로만 기술.
  - 왜 중요한가: 어느 케이스에서 불일치했는지, 어느 쪽이 더 정확한지 알 수 없음.
  - 더 필요해 보이는 근거: gold standard cell type label이 있는 공개 benchmark dataset(예: Tabula Sapiens) 대비 정확도 비교.

- **Semantic similarity 기준 없음**
  - 부족한 점: BERT semantic similarity 74~76%가 적합한 수준인지 판단할 reference가 제공되지 않는다.
  - 왜 중요한가: 이 수치가 random baseline 대비 얼마나 높은지, 혹은 전문가가 작성한 report와 비교하면 어느 수준인지 모른다.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: 저자는 groundedness 98.7~99.9%를 "hallucination 억제"의 증거로 제시하나, 실제로 groundedness score는 LLM이 제공된 토큰을 기반으로 응답했는지를 측정할 뿐이다. LLM이 제공된 데이터를 *잘못 해석*해 틀린 추천을 했더라도 groundedness는 높게 나올 수 있다.
- **현재 논문에서 제시한 근거**: groundedness score ≥ 98.7%, semantic similarity ≥ 74%.
- **더 필요해 보이는 근거**: 추천 파라미터의 실제 정확도 검증 — 예를 들어 "SCassist가 추천한 resolution으로 얻은 cluster가, 전문가가 선택한 resolution 결과와 얼마나 일치하는가."

### 정리되지 않은 질문

- 질문: augmented prompt에서 데이터 metrics 없이 prompt template만 사용했을 때 groundedness가 얼마나 떨어지는가? (ablation 없음)
- 질문: 서로 다른 LLM 서버(Gemini vs. GPT vs. Llama3)에서 파라미터 추천이 일치하는가? 서버 간 variability 분석 없음.
- 질문: 동일 dataset에 대해 SCassist를 반복 실행하면 파라미터 추천이 얼마나 일관적인가? (stochasticity 분석 없음)
- 질문: SCassist가 추천한 파라미터와 사용자가 직접 결정한 파라미터를 사용했을 때 최종 clustering 결과의 downstream biology(cell type resolution, DEG 유의성 등)가 어떻게 다른가?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: LLM을 scRNA-seq 파이프라인 전 단계에 통합하는 "workflow assistant" 패러다임을 처음으로 구체적 구현으로 제시. 특히 QC, normalization, PC selection처럼 기존 AI tool들이 다루지 않던 초기 단계를 포함한 점이 차별적.
- **다음 논문 아이디어**:
  - 여러 공개 scRNA-seq benchmark dataset(예: Tabula Sapiens, Allen Brain Cell Atlas)에서 SCassist 추천 파라미터 vs. 전문가 선택 vs. 자동 휴리스틱 세 가지를 비교해 downstream clustering quality 차이를 정량화하는 연구.
  - 서로 다른 LLM(Gemini, GPT-4o, Llama3)의 파라미터 추천 일관성과 생물학적 타당성을 체계적으로 비교하는 벤치마크.
  - 저자가 예고한 multi-modal / spatial transcriptomics 확장: SCassist를 Visium 또는 10x Xenium workflow에 적용하는 follow-up.
  - Python(scanpy/AnnData) 환경 지원 버전. R 전용이라는 생태계 제약을 극복하면 adoption이 크게 넓어질 것.
- **설명을 더 매끄럽게 만들 방법**: groundedness score를 hallucination 억제 지표로 쓰는 대신, 실제 파라미터 추천 정확도(benchmark dataset 대비 confusion matrix 또는 downstream metric 비교)를 주요 evaluation으로 재설계.
- **우선순위가 높은 후속 실험 / 분석**: benchmark dataset에서 LLM 추천 파라미터의 clustering accuracy 독립 검증 — 이것이 논문의 가장 큰 validation gap.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction: "SCassist uniquely distinguishes itself by aiming to provide comprehensive workflow guidance across the entire scRNA-seq analysis pipeline, a feature absent in these task-specific tools."
  - 사용 시나리오: 본인 논문/제안서에서 기존 AI scRNA-seq tool들의 한계(pipeline 전체 미커버)를 짚을 때
  - BibTeX key: `@nagarajan2025scassist`

- §Introduction: "hallucination is recognized as an inherent limitation of LLM's…new methods and tools to mitigate this and take advantage of the LLM's abilities, like retrieval augmentation, are also being established"
  - 사용 시나리오: LLM hallucination 억제 방법을 서술할 때 배경 인용
  - BibTeX key: `@nagarajan2025scassist`

- §Methods §2.5.1: 두 평가 데이터셋(LCMV — NK cell in Uveitis, BCRUV — CTCF binding in Th1)을 실제 발표 논문 데이터로 평가
  - 사용 시나리오: 실사용 데이터 기반 AI tool 평가 방법론 서술 시
  - BibTeX key: `@nagarajan2025scassist`

### 인용 가능 수치

- Groundedness score 98.7% (LCMV, §3.2.1, Supplementary Table 5)
  - 사용 시나리오: augmented prompt 기반 LLM이 제공된 데이터를 충실하게 활용하는 수준의 baseline으로 인용
  - BibTeX key: `@nagarajan2025scassist`

- API 비용 $2.07 / 1,978 calls (§3.3)
  - 사용 시나리오: LLM 기반 분석 도구의 비용 현실성을 논의할 때 구체적 수치로 인용
  - BibTeX key: `@nagarajan2025scassist`

- Wilcoxon Signed-Rank p = 0.0001122 (§3.2.3)
  - 사용 시나리오: human evaluation 결과의 통계적 유의성 인용
  - BibTeX key: `@nagarajan2025scassist`

### 인용 가능 Figure/Table

- Figure 1 (§2.1)
  - SCassist 전체 아키텍처 overview — Seurat workflow 각 단계와 SCassist 함수의 대응 관계
  - 사용 시나리오: 본인 review에서 LLM-assisted workflow 구조 도식으로 재현 또는 참고
  - BibTeX key: `@nagarajan2025scassist`

- Supplementary Table 1 (feature comparison)
  - SCassist vs. Geneformer, scGPT, GPTCelltype 등 기존 도구의 기능 비교표
  - 사용 시나리오: AI scRNA-seq tool 비교 섹션의 taxonomy 참고
  - BibTeX key: `@nagarajan2025scassist`
