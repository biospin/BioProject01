# MoFlow Journal Meeting Speaker Notes

## 1. Title
- 논문은 MoFlow를 제안한다. 핵심은 RNA velocity를 chromatin accessibility와 결합하되, MultiVelo처럼 fixed gene class나 latent time에 강하게 의존하지 않는다는 점이다.

## 2. Problem
- 기존 RNA velocity는 RNA abundance만 사용한다.
- scVelo류 ODE model은 latent time과 gene-specific kinetics를 추정하지만 heterogeneous branching system에서 single path assumption이 약하다.
- MultiVelo는 chromatin을 넣었지만 fixed class와 gene-specific latent time이 non-canonical lag를 보정할 수 있다.

## 3. Core Idea
- MoFlow는 `(c, u, s)`에서 cell-specific kinetic parameter를 DNN으로 예측한다.
- local neighbor를 짧은 미래 상태로 보고 predicted velocity와 neighbor displacement의 cosine distance를 줄인다.
- chromatin opening/closing은 둘 다 평가한 뒤 lower loss scenario를 선택한다.

## 4. Method Output
- m1은 chromatin closing 중 RNA가 증가하는 delayed repression signal이다.
- m2는 chromatin opening 중 RNA가 감소하는 asynchronous repression signal이다.
- RNA-on/off는 unspliced/spliced RNA velocity 부호로 activation/repression state를 요약한다.

## 5. Figure 2
- developing human brain cortex에서 4693 cells, 842 genes를 분석했다.
- CBDir은 MoFlow 0.362, MultiVelo 0.211, scVelo 0.211, cellDancer -0.015.
- MoFlow는 known cortical development hierarchy와 가장 잘 맞고, 다른 model의 backflow를 줄인다.

## 6. Figure 2 Interpretation
- MoFlow m1/m2 score는 MultiVelo model 1/2 class와 맞는다.
- 중요한 점은 fixed switching time 없이 continuous score로 같은 regulatory logic을 읽는다는 것이다.

## 7. Figure 3
- OPC lineage에서 decoupling-sOff state가 보인다.
- PDGFRA와 MAP3K1은 unspliced RNA production이 유지되지만 spliced RNA가 감소한다.
- global time에서는 negative c-s lag가 남고, MultiVelo gene-specific time에서는 canonical order로 보정된다.

## 8. OPC Takeaway
- 이 Figure의 핵심은 gene-specific latent time이 biological expectation에 맞춰 data의 non-canonical order를 지울 수 있다는 점이다.
- decoupling-sOff region에서 OPC projection은 63%, complementary region은 20%였다.

## 9. Figures 4-5
- mouse skin SHARE-seq에서 MoFlow는 TAC에서 terminal hair follicle lineage로 가는 방향을 잡는다.
- Figure 4는 transcriptional boost, Figure 5는 alpha와 chromatin accessibility 분리를 보여준다.

## 10. Figure 5
- DAC score로 chromatin accessibility와 transcription rate variability를 분리한다.
- LCHA는 chromatin은 크게 바뀌지 않지만 transcription rate가 cell type마다 크게 달라지는 gene group이다.
- Padi3와 Myo10은 이런 관점에서 MoFlow가 잘 잡은 사례다.

## 11. Figure 6
- E18 mouse brain에서 MoFlow는 Cyc. Prog. -> RG -> IPC -> ExM/SP -> UL/DL 흐름을 잡는다.
- cluster 0의 alpha DAC는 DNA damage response와 DNA repair에 enriched된다.
- 저자 해석은 RG commitment 주변 stress-response transcriptional program이다.

## 12. Figure 7
- negative c-s lag를 RNA kinetics로 설명한다.
- clusters 0-3은 RNA decay/export가 chromatin closure보다 빠른 pattern.
- cluster 10은 spliced RNA accumulation이 chromatin opening보다 먼저 보이는 stimulus-responsive 또는 nuclear release 후보.
- half-life 자료가 NIH3T3 기반이라는 점은 limitation으로 말해야 한다.

## 13. Human HSPC
- HSPC에서도 MoFlow는 HSC/MPP에서 여러 blood lineage로 갈라지는 hierarchy를 대체로 복원했다.
- scVelo/cellDancer는 downstream progenitor에서 HSC로 돌아가는 backflow를 보였고, MultiVelo는 overly linear flow 경향이 있었다.

## 14. Limitations
- 저자 명시 한계: enhancer-promoter interaction, transcriptional memory, motif-level regulation을 명시적으로 모델링하지 않는다.
- 분석상 주의: velocity embedding distortion, external half-life dataset, lower angular error 기반 chromatin state 선택.

## 15. Final Takeaways
- MoFlow의 방법론적 의미는 local relay velocity와 chromatin-aware cell-specific kinetics의 결합이다.
- 생물학적 의미는 chromatin-dependent repression, chromatin-independent transcriptional boost, RNA export-linked lag를 나누어 볼 수 있다는 점이다.
- 후속 연구는 nascent RNA, nuclear/cytoplasmic RNA fraction, perturbation으로 predicted lag와 alpha burst를 검증하는 방향이 좋다.
