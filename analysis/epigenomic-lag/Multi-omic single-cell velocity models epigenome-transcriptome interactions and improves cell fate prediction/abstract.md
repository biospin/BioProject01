# Multi-omic single-cell velocity models epigenome-transcriptome interactions and improves cell fate prediction

- 저자: Chen Li, Maria C. Virgilio, Kathleen L. Collins, Joshua D. Welch
- 연도: 2023
- Venue: Nature Biotechnology
- 분야: single-cell multi-omics, RNA velocity, epigenome-transcriptome dynamics

## Abstract Summary
- 한 문장 요약: MultiVelo는 single-cell multi-omic 데이터에서 chromatin accessibility와 RNA dynamics를 함께 모델링해 cell fate prediction을 개선하고, epigenome과 transcriptome 사이의 시간차를 정량화하는 방법이다.
- 연구 목적: 같은 cell에서 측정된 RNA와 chromatin accessibility를 이용해 epigenome 변화와 transcriptome 변화의 시간적 관계를 추정하고, RNA-only velocity보다 더 정확하게 cell fate를 예측하는 것이다.
- 문제 또는 gap: 기존 RNA velocity는 spliced/unspliced RNA만 사용하므로 chromatin remodeling이 transcription보다 먼저 일어나거나 늦게 닫히는 상황을 직접 모델링하지 못한다. 또한 epigenome-only 접근은 gene expression을 통합하지 못해 transcription dynamics와의 연결이 약하다.
- 핵심 방법: MultiVelo는 RNA velocity framework를 확장해 chromatin accessibility, unspliced pre-mRNA, spliced mRNA를 세 개의 ODE로 연결한다. probabilistic latent variable model과 expectation-maximization 절차로 chromatin closing, transcriptional induction, transcriptional repression의 switch time과 rate parameter를 추정한다.
- 주요 결과: RNA-only velocity estimate보다 cell fate prediction 정확도가 개선되었다고 주장한다. brain, skin, blood single-cell multi-omic dataset에 적용해 chromatin이 transcription 종료 전 닫히는 gene class와 transcription 종료 후 닫히는 gene class를 구분했고, epigenome과 transcriptome이 coupled된 두 상태와 decoupled된 두 상태를 찾았다. 또한 TF expression과 binding site accessibility 사이, disease-associated SNP accessibility와 linked gene expression 사이의 time lag를 확인했다.
- 저자가 주장하는 기여: MultiVelo는 multi-omic single-cell dataset에서 epigenomic regulation of gene expression을 동역학적으로 해석하고, priming과 decoupling interval을 정량화하며, disease-associated variant와 gene expression 사이의 시간적 관계까지 분석할 수 있는 velocity model을 제공한다.
- 주의점 또는 빠진 정보: Abstract에는 구체적인 benchmark 수치, cell 수, gene 수, runtime, 실패 사례가 명시되지 않는다. “accuracy 개선”은 Abstract에서는 정량값 없이 주장으로 제시되며, 구체 근거는 Results와 Figure에서 확인해야 한다.
