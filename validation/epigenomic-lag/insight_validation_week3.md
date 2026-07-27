# Insight Validation - Epigenomic Lag Week 3

Owner: jmryu  
Issue: BIOP01-12  
Input analyses: `analysis/epigenomic-lag/**/full.md`

## Summary

검증 대상은 기존 `full.md` 분석에서 도출된 epigenome-transcriptome timing insight다. Status는 논문 내부 근거 기준으로 판정했으며, causal perturbation이 필요한 주장은 `Needs Evidence`로 남겼다.

## Insight Validation

| ID | Paper | Insight | Status | Reason | Evidence | Risk / Next Check |
|---|---|---|---|---|---|---|
| I-01 | MultiVelo | chromatin accessibility를 RNA velocity ODE에 넣으면 RNA-only model이 놓치는 early regulatory change와 priming interval을 포착할 수 있다. | Valid | Figure와 Results가 mouse brain, skin, HSPC, fetal brain에서 반복 근거를 제시한다. 주장은 model capability와 association 범위에 머문다. | Figure 1-6; mouse skin Spearman 0.51 vs scVelo 0.44; median primed interval 21%, decoupled interval 19%. | causal claim으로 확장하지 말 것. Perturbation 없이 chromatin opening이 RNA 증가를 직접 유발했다고 쓰면 과장이다. |
| I-02 | MultiVelo | model 2 gene은 transient activation 또는 cell-cycle-linked regulation을 반영할 수 있다. | Needs Evidence | model 2 enrichment와 timing 차이는 강하지만, mechanism은 저자도 hypothesis 수준으로 제시한다. | Figure 2h model 2 26.7%; model 2 최고 spliced expression이 더 이른 latent time에 나타남, P = 9 x 10^-7; HSPC model 2 cell-cycle GO FDR < 0.002. | cell-cycle perturbation, time-resolved validation, protein/TF activity 확인 필요. |
| I-03 | MoFlow | fixed latent time/gene class 없이 local relay와 cell-specific kinetics를 쓰면 branching trajectory에서 backflow를 줄일 수 있다. | Valid | 여러 baseline과 같은 dataset에서 CBDir 및 qualitative stream 비교가 제시된다. | Human brain cortex CBDir: MoFlow 0.362, MultiVelo 0.211, scVelo 0.211, cellDancer -0.015; Figure 2, 4, 6. | UMAP projection distortion과 neighbor selection sensitivity를 별도 점검해야 한다. |
| I-04 | MoFlow | negative `c-s` lag는 artifact가 아니라 RNA half-life, nuclear export, OPC-related regulation 같은 biological signal일 수 있다. | Needs Evidence | OPC projection과 half-life signature는 설득력 있는 association이지만 직접 측정한 mechanism은 아니다. | Figure 3: decoupling-sOff region mGPC/OPC 중 63% OPC projection vs complementary 20%; Figure 7 NIH3T3 half-life comparison. | half-life 자료가 외부 cell line에서 온 점이 약하다. Brain development에서 matched RNA kinetics assay 필요. |
| I-05 | MultiVeloVAE | continuous cell-specific rate와 shared latent time은 MultiVelo의 discrete state/single parameter 한계를 줄이고 multi-lineage velocity를 개선한다. | Needs Evidence | full.md 기준으로 relative improvement는 명시되지만 exact Figure 3g/3h 수치가 Source Data에 의존한다. | Figure 3g/3h summary; 5개 multi-omic dataset에서 k-step CBDir 및 Mann-Whitney U 개선 보고. | exact benchmark values와 Source Data 재확인 전에는 강한 성능 우위 표현을 피한다. |
| I-06 | MultiVeloVAE | partial modality integration으로 RNA-only sample의 chromatin profile과 perturbation effect를 예측할 수 있다. | Overstated | 논문은 computational prediction capability를 보이지만, 실제 perturbation validation과 동일하게 취급하면 범위 초과다. | Figure 7: partial modality integration, missing ATAC profile generation, in silico perturbation. | “예측 가능”은 가능하나 “검증됨” 또는 “실험 대체 가능”으로 쓰면 안 된다. |

## 토론 준비

1. 가장 설득력 있던 Insight: I-03. 동일 dataset에서 baseline과 CBDir 비교가 있고, qualitative backflow 감소와 quantitative metric이 함께 제시된다.
2. 근거 부족/과장 Insight: I-06. 모델 기능으로는 흥미롭지만 perturbation output은 computational prediction이며 experimental validation이 필요하다.
3. Validation Agent 필수 기준: Evidence와 Scope를 먼저 통과시킨 뒤 Novelty/Actionability를 평가해야 한다. 근거가 약한 새로운 해석은 `Needs Evidence`로 남긴다.
4. 결과가 서로 다를 때 판단 방법: 같은 dataset/metric/source data의 직접 비교를 우선하고, UMAP stream 같은 qualitative evidence는 보조 근거로 둔다.
5. 출력 형식 통일안: `ID / Paper / Insight / Status / Reason / Evidence / Risk or Next Check` 7열 표를 기본으로 사용한다.

## Next Work

- Figure Source Data를 확인해 I-05의 exact benchmark value를 채운다.
- 각 paper별 insight를 3-5개로 늘리되, causal mechanism 후보는 perturbation 필요 여부를 별도 column으로 분리한다.
- Validation 결과를 4주차 Openclaw Agent 입력 schema로 넘길 수 있도록 JSON schema 후보를 만든다.
