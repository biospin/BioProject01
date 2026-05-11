# MultiVelo Journal Meeting Speaker Notes

## 1. Title
- 이 논문은 MultiVelo라는 multi-omic velocity model을 제안한다.
- 핵심은 chromatin accessibility를 RNA velocity의 보조 feature가 아니라 transcription dynamics의 시간 변수로 넣는 것이다.

## 2. Problem
- trajectory inference는 cell ordering을 제공하지만 direction과 relative rate 해석이 약하다.
- RNA velocity는 unspliced/spliced RNA로 미래 state를 예측하지만 chromatin remodeling을 explicit하게 넣지 않는다.
- Multiome 데이터가 나오면서 같은 cell의 RNA와 chromatin accessibility를 동시에 쓸 수 있게 됐다.

## 3. Core Model
- MultiVelo는 `c(t)`, `u(t)`, `s(t)`를 하나의 ODE system으로 묶는다.
- transcription rate가 chromatin accessibility `c(t)`에 비례한다고 둔다.
- output은 velocity vector, latent time, switch time, state assignment, priming/decoupling interval이다.

## 4. Model 1 vs Model 2
- model 1은 chromatin closing이 transcriptional repression보다 먼저 시작된다.
- model 2는 transcriptional repression이 먼저 시작되고 chromatin closing이 뒤따른다.
- priming은 chromatin이 먼저 열렸지만 RNA production이 아직 없는 구간이다.
- decoupling은 chromatin과 RNA가 서로 다른 방향으로 움직이는 구간이다.

## 5. Embryonic Mouse Brain
- MultiVelo는 RG에서 neuron, astrocyte, oligodendrocyte 방향으로 알려진 cortical trajectory를 복원했다.
- scVelo는 upper layer neuron에서 backflow를 보였다.
- fit gene `n = 865`에서 model 1 41.4%, model 2 26.7%, induction-only 29.5%였다.

## 6. Cell-Gene States
- Figure 3은 gene별 kinetics를 넘어 cell-gene pair state를 assignment할 수 있음을 보여준다.
- median primed interval은 전체 time의 21%, median decoupled interval은 19%였다.
- 이 수치는 chromatin과 RNA가 상당한 시간 동안 lagged relationship을 가진다는 근거다.

## 7. Mouse Skin SHARE-seq
- MultiVelo latent time과 Palantir pseudotime의 Spearman correlation은 0.51이고, scVelo는 0.44였다.
- Wnt3에서 chromatin-spliced RNA delay가 길게 나타났다.
- chromatin potential을 velocity framework 안에서 priming interval로 정량화한 사례다.

## 8. Human HSPC
- 11,605 high-quality cell에서 MultiVelo가 hematopoietic hierarchy와 더 맞는 velocity를 보였다.
- model 2 gene은 cell-cycle GO term에 enriched되었고 FDR < 0.002였다.
- terminal marker gene은 chromatin accessibility 증가 뒤 RNA expression이 증가하는 pattern을 보였다.

## 9. Fetal Human Brain
- MultiVelo는 human brain development pattern과 맞는 velocity를 보였고 scVelo는 일부 neuron lineage에서 backflow를 보였다.
- TF expression peak가 downstream motif accessibility peak보다 앞서는 경향이 있었다.
- GWAS SNP 6,968개 중 757개를 accessibility-expression timing으로 분석했다.

## 10. Cross-Dataset Pattern
- 반복되는 메시지는 chromatin timing이 RNA-only ambiguity를 줄인다는 것이다.
- 다만 dataset마다 같은 metric으로 benchmark한 것은 아니므로 성능 claim은 조심해서 읽어야 한다.

## 11. Limitations
- benchmark metric이 통일되지 않았다.
- ODE model은 복잡한 molecular regulatory mechanism을 rate constant와 switch time으로 추상화한다.
- TF/SNP timing은 temporal association이지 causal proof는 아니다.

## 12. Final Takeaways
- MultiVelo의 기여는 epigenome-transcriptome timing concept을 gene별, cell별로 정량화한 것이다.
- 좋은 후속 연구는 predicted priming/decoupling을 perturb-seq, CRISPRi/a, allele-specific assay 등으로 검증해야 한다.
