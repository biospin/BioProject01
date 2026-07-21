# Luo et al., 2026 — RNA Velocity Benchmark — Abstract 분석

> 근거 자료: `sources/abstract.txt` (PubMed abstract, PMID 41916302). 원문 PDF·supplementary 미확보 상태이므로 abstract 본문에 명시된 내용만 근거로 한다. 벤치마크의 method별 점수·순위·dataset 목록은 abstract에 없어 추측하지 않는다.

## Abstract Summary

- **한 문장 요약**: RNA velocity inference에 대한 근거 기반 best-practice 가이드라인이 없는 상황에서, 15개 기존 RNA velocity method를 17개 독립 dataset에 대해 accuracy·stability·usability 세 축으로 벤치마크하여 시나리오별 method 선택 권고안을 제시한 연구.
- **연구 목적**: RNA velocity inference에서 어떤 method를 언제 써야 하는지에 대한 evidence-based best-practice를 수립하는 것.
- **문제 또는 gap**: "diverse computational methods have been developed, there are no evidence-based guidelines for best-practice in RNA velocity inference" — 다양한 method가 나왔지만 best-practice에 대한 근거 기반 지침이 부재.
- **핵심 방법**: 15개 기존 RNA velocity method를 17개 독립 dataset에서 벤치마크. multiple validation strategy를 결합하고, accuracy·stability·usability 세 dimension으로 성능 평가.
- **주요 결과**: 모든 평가에서 우월한 단일 method는 없었고(no single method exhibited superior performance in all the assessments), 일부 경우 예상치 못한 underperformance가 관찰됨.
- **저자가 주장하는 기여**: 위 결과를 바탕으로 한 scenario-based best-practice 권고안. 사용자가 자신의 data와 분석 목적에 가장 적합한 method를 고를 수 있도록 지원.

## 연구 목적

RNA velocity는 다양한 biological context에서 cell state transition trajectory를 밝힐 잠재력이 크다(저자 표현: "great potential for unveiling trajectories of cell state transitions"). 저자는 method가 많아진 현 시점에서 "무엇을 쓸지"를 근거로 정할 수 있는 best-practice를 만드는 것을 목적으로 한다.

## 문제 / Gap

- 다수의 computational method가 개발되었으나, RNA velocity inference의 best-practice에 대한 evidence-based guideline이 없음.
- 즉, method 선택이 근거가 아니라 관행·접근성에 의존하는 상황. 이 gap을 비교 벤치마크로 메우려는 것이 동기.

## 방법 (벤치마크 설계)

- **비교 대상**: 기존 RNA velocity method 15개.
- **데이터 폭**: 17개 independent dataset.
- **검증**: multiple validation strategy를 통합(incorporating multiple validation strategies). 구체적인 validation 종류는 abstract에 명시되지 않음.
- **평가 축 3종**:
  - accuracy (정확도)
  - stability (안정성)
  - usability (사용성)
- `미제공:` 15개 method의 이름, 17개 dataset의 종류·accession, 각 validation strategy의 정의, dimension별 정량 지표는 abstract에 없음. method별 점수·순위 표도 abstract에 없음.

## 주요 결과

- 모든 평가 항목에서 일관되게 우월한 단일 method는 없음. → method 선택이 context-dependent임을 시사.
- 특정 경우에 "예상치 못한 underperformance"가 관찰됨(unexpected underperformance in certain cases). 어떤 method·어떤 dataset·어떤 dimension에서였는지는 abstract에 명시되지 않음.
- `미제공:` 어느 method가 어느 시나리오에서 우세/열세였는지의 구체 결과는 abstract에 없음 (full paper 확인 필요).

## 기여

- accuracy·stability·usability 세 축의 비교 결과를 근거로 한 scenario-based best-practice 권고안 제시.
- 사용자가 자신의 data 특성과 analytical need에 맞춰 method를 고르도록 돕는 의사결정 지침. → 이 논문의 실질 산출물은 새 method가 아니라 *선택 가이드*다.

## 주의점

- `해석:` abstract만으로는 "어떤 시나리오에 어떤 method"라는 권고안의 실제 내용을 알 수 없다. 권고안 본문(아마 main figure/table 또는 supplementary)이 핵심이므로 full paper 확보 전까지 method 선택 결정에 직접 인용하면 안 된다.
- `해석:` "no single method superior" + "unexpected underperformance"는 method 선택 시 *단일 default에 고정하지 말고 data별로 검증*하라는 신호로 읽힌다. 다만 어떤 검증을 권하는지는 본문 확인 필요.
- `미제공:` 15개 method에 우리 관심 도구(MultiVelo, MultiVeloVAE, MoFlow 등 multi-omic velocity)가 포함되는지 abstract에 없음. 본 벤치마크가 scRNA-only velocity 위주인지 multi-omic까지 포함인지 확인 필요 — 우리 chromatin–transcription lag 목표와의 직접 관련성은 이 확인에 달려 있다.
- `검토필요:` 17개 dataset에 hematopoiesis/HSPC 계열이 포함되는지. 저자 소속이 Department of Hematology(Xiamen University)이므로 hematopoietic dataset 비중이 있을 가능성 — 다만 abstract에 명시되지 않아 본문 확인 필요.

### 우리 HSPC 데이터 적용 시사점 (한 줄)

`해석:` "전 항목 우월 method 없음"이라는 결론상, Human HSPC 10x Multiome(GSE209878)에 velocity method를 고를 때 단일 default를 가정하지 말고, 이 논문의 scenario-based 권고에서 우리 data 성격(multiome, hematopoietic trajectory)에 맞는 항목을 full paper에서 확인한 뒤 accuracy·stability를 자체 재검증해야 한다 — 단, 본 벤치마크에 multi-omic velocity method가 포함되는지 먼저 확인이 전제다.
