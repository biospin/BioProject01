---
name: core-results
description: Analyze the Results section for the objective <paper-id>_core.md section, with explicit emphasis on statistical significance (p-values, CI, effect size) and reproducibility (cross-dataset consistency, ablation, replication). Use to summarize datasets used, baselines compared, and concrete numerical or qualitative results for each dataset.
---

# Core Results

## 목표
Results 섹션을 "어떤 dataset을 사용했고, 그 dataset에서 어떤 결과값을 얻었는가" 중심으로 정리한다. 핵심은 자료의 주장을 뒷받침하는 *실제 수치*, dataset 이름, sample size, gene/cell 수, baseline, metric, 비교 결과, 그리고 **통계적 유의성(p-value, CI, effect size, multiple testing correction)** 과 **재현성(여러 dataset에서의 일관성, ablation, replication)** 을 빠뜨리지 않는 것이다.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 출력은 `analysis/<primary-topic>/<paper-id>/<paper-id>_core.md`의 "주요 결과" 섹션에 누적된다.

## 통계 유의성·재현성 강조 (이전 full-results 대비 보강)

수치를 옮길 때 다음을 *반드시* 함께 기록한다 — 본문에 있으면 그대로, 없으면 `미제공:`.

- **p-value / q-value (FDR)**: 통계 검정의 유의 수준.
- **Confidence interval (CI)**: 95% CI 또는 표준편차/표준오차.
- **Effect size**: Cohen's d, odds ratio, hazard ratio, AUC 차이의 크기.
- **Multiple testing correction**: BH, Bonferroni, permutation FDR 적용 여부.
- **재현성 근거**: 같은 결과가 *다른 dataset / 다른 cohort / 다른 lab*에서 나왔는지. 또는 *ablation·sensitivity analysis*.
- **Sample size**: n = … (cell, sample, patient 단위 명확히).

수치를 옮긴 후 다음 한 줄을 분석자가 추가:
- `해석: 이 p-value는 효과 크기 대비 [강한/약한] 증거다. 단일 dataset만으로는 재현성이 확보되지 않음.`

## 언어 규칙
- 기본 출력은 한국어로 작성한다.
- `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `baseline`, `dataset`, `benchmark`, `metric`, `pseudotime`, `Spearman`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 유지할 때는 처음 한 번 한국어 설명을 덧붙인다.
- 불필요하게 문장 전체를 영어로 쓰지 않는다.

## 작업 절차
1. Results, Figure caption, Table, Supplementary 언급에서 dataset 이름과 실험 조건을 먼저 뽑는다.
2. 각 dataset별로 cell 수, gene 수, tissue/species, platform, baseline, metric을 정리한다.
3. 실제 수치 결과를 우선 보존한다.
4. 수치가 없는 정성 결과는 `정성 결과:`로 분리한다.
5. baseline 비교가 있으면 “무엇과 비교했고 어떤 차이가 났는지”를 명확히 쓴다.
6. 결과가 논문 주장과 어떻게 연결되는지 한 줄로 정리한다.
7. 수치가 본문에 없고 Figure만 시각적으로 제시되면 `정확한 수치 본문 미제공`이라고 표시한다.

## 출력 형식
사용자가 다른 형식을 요청하지 않으면 아래 구조를 따른다.

```markdown
### Results

#### Dataset별 결과
##### Dataset 1
- Dataset:
- 목적:
- 사용한 데이터 규모:
- Baseline / 비교 대상:
- Metric / 평가 기준:
- 주요 수치:
- 정성 결과:
- 논문 주장과의 연결:

##### Dataset 2
- Dataset:
- 목적:
- 사용한 데이터 규모:
- Baseline / 비교 대상:
- Metric / 평가 기준:
- 주요 수치:
- 정성 결과:
- 논문 주장과의 연결:

#### 전체 결과 요약
- 반복적으로 관찰된 패턴:
- 가장 중요한 수치:
- baseline 대비 차이:
- 결과 해석 시 주의점:
```

## 수치 정리 규칙
- cell 수, gene 수, percentage, p-value, correlation, accuracy, score, runtime, memory가 나오면 가능한 한 그대로 적는다.
- `n = ...` 표기는 보존한다.
- Figure caption에만 있는 수치도 Results에 포함한다.
- 수치가 여러 dataset에 걸쳐 나오면 dataset별로 분리한다.
- “성능이 좋다”라고 쓰지 말고 어떤 metric에서 어떤 baseline보다 어떤 값이 좋았는지 쓴다.
- 정확한 metric이 없으면 `metric 명시 없음`이라고 쓴다.

## Dataset 정리 규칙
- species, tissue, platform, modality를 가능하면 함께 적는다.
- 예: `embryonic mouse brain E18 10x Multiome`, `mouse dorsal skin SHARE-seq`, `human HSPC RNA+ATAC`, `fetal human brain 10x Multiome`.
- dataset이 논문 주장의 어떤 부분을 검증하는지 함께 쓴다.

## 주의할 점
- Results에서 새로운 limitation이나 speculation을 길게 쓰지 않는다.
- Discussion으로 넘겨야 할 해석은 짧게만 표시한다.
- 누락된 수치가 있으면 임의로 만들지 않는다.
