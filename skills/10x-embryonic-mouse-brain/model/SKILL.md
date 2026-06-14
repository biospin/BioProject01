---
name: 10x-embryonic-mouse-brain-model
description: Model gene-specific activation lag and shutdown lag in the 10x embryonic mouse brain multiome dataset. Use when Codex needs to estimate timing, fit MultiVelo-like dynamics, construct lag labels, or evaluate baseline feature predictors for this dataset.
---

# 10x Embryonic Mouse Brain Model

## 목표
10x embryonic mouse brain dataset에서 gene-specific `activation lag`과 `shutdown lag`을 추정하고, baseline epigenomic features가 lag structure를 설명하는지 모델링한다.

## 입력
- 전처리된 RNA/ATAC multiome object.
- gene-level 또는 peak-level accessibility features.
- pseudotime, lineage, developmental stage, cell state annotation.
- chromatin opening/closing time, transcription onset/shutdown time 또는 이를 추정할 수 있는 동역학 model output.

## 작업 절차
1. preprocessing output의 genome build, annotation, time axis를 확인한다.
2. gene별 chromatin/RNA timing 값을 추정하거나 기존 결과를 로드한다.
3. `activation lag = transcription onset time - chromatin opening time`을 계산한다.
4. `shutdown lag = chromatin closing time - transcription shutdown time`을 계산한다.
5. confidence, uncertainty, missingness를 gene별로 함께 저장한다.
6. promoter/enhancer accessibility, motif score, peak-to-gene linkage 같은 baseline feature로 lag을 예측한다.
7. 성능은 ranking, calibration, lineage-held-out generalization, early-vs-late separation 위주로 평가한다.

## 출력 형식
```markdown
## Model Plan
- Dataset:
- Time axis:
- Lag definition:
- Features:
- Model:
- Evaluation:
- Outputs:
- Limitations:
```

## 주의할 점
- Model 1/Model 2 이분법으로 끝내지 말고 continuous lag spectrum으로 해석한다.
- lineage-specific timing 차이가 있으면 global model과 lineage-specific model을 구분한다.

