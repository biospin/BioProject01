<!--
draft_v2.md의 한국어 검토본(번역·윤문). 정본은 영어 draft_v2.md. 2026-07-19.
수치·통계·주장·구조는 영문 draft_v2.md가 정본이며, 이 문서는 kkkim의 한국어 검토용이다.
헤드라인 = 측정 앵커 velocity 출력 신뢰도 결정 지도. 저자·소속·교신·IP·accession·repository는 <FILL> 유지.
-->

# 전사 속도는 multiome RNA velocity의 유일한 외부 anchoring 출력이다: single-cell kinetics를 위한 측정 기반 신뢰도 지도

**저자:** <FILL: author list>

**소속:** <FILL: affiliations>

**교신저자:** <FILL: name, email>

> *연구·교육용 초안.* 이 원고는 이미 검증된 결과를 동료 심사를 위해 재구성한 것이며, 임상·진단 자원이 아니다. 저자·소속·교신저자·IP 항목은 확정 전 자리표시자다.

---

## Abstract

**배경.** Chromatin 정보를 결합한("multiome") RNA velocity 방법들은 유전자별로 여러 값을 산출한다. 전사 속도(transcription rate), 분해 속도(degradation rate), 그리고 chromatin에서 transcription으로 이어지는 *시간차(lag)*, 곧 locus가 열리거나 닫히는 시점과 그 유전자의 transcription이 전환되는 시점 사이의 오프셋이 그것이다. 이 값들은 저마다 생물학적 판독값으로 제안되어 왔고, 특히 시간차(lag)는 epigenetic 약물 반응의 timing을 예측하는 데 쓸 수 있다고 여겨져 왔다. 그러나 파생된 값을 하류에서 쓰려면 그것이 먼저 *신뢰할 수 있어야* 한다. 곧 합리적인 알고리즘들에 걸쳐 재현되어야 하고, 가능하다면 독립적인 측정값과도 부합해야 한다. 우리는 인간 조혈모·전구세포(hematopoietic stem and progenitor cells, HSPC; 10x Multiome으로 프로파일링)에서 어떤 velocity 출력이 이 기준을 충족하는지를 물었다.

**접근.** 최대 다섯 개의 velocity arm(갈래)(RNA 전용 scVelo floor에 MultiVelo, MultiVeloVAE, MoFlow, CRAK-Velo를 더한 것)에 걸쳐 각 출력을 네 축에서 검정했다. 방법 간 재현성(순열 FDR), lineage 내 ATAC-shuffle 인과 대조군, 다섯 개 외부 multiome(그중 하나는 사전등록)에서의 cross-dataset 재현, 그리고 fitting된 속도가 측정된 합성(K562 TT-seq)·분해(mRNA 반감기) 속도에 외부 anchoring되는지가 그것이다.

**결과.** 출력들은 뚜렷이 갈라졌다. 전사 속도 α만이 두 축 모두에서 신뢰할 수 있었다. α는 방법 간에 재현되었고(Spearman ρ=0.88, 관측값), 세 방법 모두에서 측정된 K562 TT-seq 합성 속도를 복원했다(비-housekeeping ρ +0.24 ~ +0.29, 모든 CI가 0 배제). chromatin에서 transcription으로 이어지는 시간차(lag)는 크기에서 잘해야 약하게 재현되었고(가장 강한 쌍 ρ=+0.163, 대부분의 쌍 |ρ|≤0.08) 부호에서는 우연 수준에 그쳤으며(48%), ATAC를 뒤섞어도 통계적으로 변하지 않아 시간차(lag)가 chromatin에서 비롯된 것이 아니라 모델 구조에서 비롯됨을 드러냈다. 분해 속도 γ도 마찬가지로 방법에 취약했고(방법 간 ρ≈−0.1), ground truth가 있는 곳에서도 복원되지 않았다(K562 반감기 3/3 귀무; 교과서적 scVelo γ는 반대로 나와 −0.224, CI가 0 배제). α가 시간차(lag)보다 앞선다는 순서는 여섯 개 시스템 모두에서 유지되었고, 어떤 fitting보다 먼저 봉인한 사전등록 6-of-6 채점표(scorecard)를 통과했다. 프로파일 우도(profile-likelihood) 분석은 그 기제를 주었다. α는 stiff(식별 가능)한 반면 시간차(lag)는 sloppy하고 경계에 제약되며, 이 식별가능성은 외부 검증과 부분적으로 정렬하나 확증적으로 정렬하지는 않는다.

**결론.** 우리는 이 결과를 측정 앵커 velocity 출력 신뢰도 지도로 정리한다. α와 속도에서 파생된 신호는 신뢰한다(재현되고 외부에 anchoring되므로 직접 사용 가능). 시간차(lag), 그 부호, 절대 timing, 그리고 γ는 신뢰할 수 없는 것으로 다루며 직교(orthogonal) 검증을 요구한다. 하류의 어떤 timing 예측 모델이든 단일 방법의 시간차(lag)가 아니라 강건한 baseline-ATAC-to-α 경로를 거쳐야 한다.

**키워드:** RNA velocity, single-cell multiome, chromatin accessibility, transcriptional kinetics, parameter identifiability, external validation, benchmarking, hematopoiesis

---

## Background

RNA velocity는 unspliced와 spliced mRNA의 균형으로부터 transcription 변화의 방향과 속도를 추론하며, chromatin 정보를 결합한 확장 방법군은 이제 이를 single-cell ATAC와 결합해 chromatin 상태가 transcription에 어떻게 입력되는지를 모델링한다. 이 방법들은 하나의 숫자만 내놓지 않는다. 저마다 전사 속도 α, splicing 속도 β, 분해 속도 γ를 fitting하고, multiome 변형에서는 유전자별 *chromatin에서 transcription으로 이어지는 시간차(lag)*를 추가로 산출한다. MultiVelo는 chromatin과 RNA 전환 시각(switch time) 사이의 명시적 priming/decoupling 오프셋을 정의하고 유전자를 그에 따라 분류한다 [1]. MultiVeloVAE는 이를 세포별 연속 decoupling/coupling 인자로 일반화한다 [2]. MoFlow는 세포별 chromatin 개방·transcription·splicing·분해 속도를 추론하고 사전 지정된 latent time 없이 chromatin–spliced 시간차(lag)를 보고한다 [3]. CRAK-Velo는 chromatin 접근성 kinetics를 통합하고 궤적(trajectory)에서 유도된 시간차(lag)를 허용한다 [4]. 같은 계열의 대안들(archetypal ATAC+RNA 궤적 모델링 [5]; differential-accessibility prior에 기반한 regulatory velocity [6])과, 우리의 floor가 기반하는 RNA 전용 생성적 velocity(posterior velocity 불확실성을 더한 veloVI [7], 그리고 multiome MultiVeloVAE와 구별되는 RNA 전용 Bayesian veloVAE [8])가 이 지형을 이룬다. 생물학적 동기는 "chromatin potential"이다. 곧 lineage commitment 동안 핵심 locus의 접근성이 발현에 앞설 수 있다는 관찰, 즉 chromatin이 세포 운명을 *예비 개방(prime)*한다는 것이다 [14]. 발생 중인 대뇌 피질처럼 일시적 전사인자가 풍부한 시스템에서는 다단계 accessibility-이후-target 시간차(lag)가 기록되어 있는데 [15], 바로 그런 곳이 유전자별 시간차(lag)가 방법에 가장 민감할 지점이다.

이 출력들은 저마다 생물학적 판독값으로 제안되었고, 그중에서도 시간차(lag)는 기제적(mechanistic) 시계로서 매력적이다. 우리 연구의 동기가 된 목표는 baseline epigenomic feature로부터 epigenetic 약물 반응의 *timing*을 예측하는 것이며, 여기에는 유전자별 활성화/차단(activation/shutdown) 오프셋이 자연스러운 공변량(covariate)이 된다. 그러나 velocity에서 파생된 값은 *신뢰할 수 있을* 때에만 하류에서 쓸 수 있고, 신뢰도에는 보통 따로따로 검정되는 두 측면이 있다. 첫째는 내부적 측면이다. 어떤 합리적 알고리즘으로 산출했든 같은 값이 나오는가. velocity를 비판적으로 검토한 문헌들은 많은 velocity 판독값이 이 기준조차 통과하지 못함을 분명히 한다. 위배된 모델 가정과 복수의 kinetic regime은 잘못된 velocity를 낳고 [9], 파이프라인은 사용자가 지정하는 hyperparameter가 많으며 흔히 실무에 바로 쓰기 어렵고 [10], velocity의 *방향*조차 신뢰성 있게 정량하기가 간단치 않다 [11]. 2026년의 두 벤치마크는 velocity 방향이 방법에 의존하며 보편적 승자가 없음을 확립했지만 [12,13], 둘 다 velocity *벡터*를 채점할 뿐 유전자별 개별 출력을 채점하지 않으며, 순열 귀무 일치도 검정도 인과 음성 대조군도 외부 측정 anchor도 적용하지 않는다. 신뢰도의 둘째 측면은 외부적이며 velocity에서는 거의 검정된 적이 없다. fitting된 속도가 *독립적으로 측정된* kinetic 양을 복원하는가. metabolic labeling 실험(합성에는 TT-seq, 분해에는 SLAM-seq 반감기)은 이제 이 검정을 가능하게 하며, 이것이 더 강한 기준이다. 어떤 값은 방법 간에 재현되면서도 여전히 공유된 인공산물일 수 있지만, 다른 기술로 다른 세포에서 이뤄진 측정값과도 부합하는 값은 생물학에 anchoring된 것이다.

따라서 우리는 velocity 출력을 발견이 아니라 신뢰도로 분류할 후보로 다룬다. 인간 HSPC 10x Multiome(GSE209878)에서 RNA 전용 floor와 네 개의 chromatin 정보 arm을 정면으로 벤치마크하며, 순열 FDR 일치 검정, 인과적 ATAC-shuffle 음성 대조군, 사전등록 검정을 포함한 다섯 개 외부 시스템에서의 cross-dataset 재현, 그리고 출력들을 가장 깨끗하게 갈라놓는 축인, fitting된 속도를 측정된 합성·분해에 외부 anchoring하는 분석을 함께 수행한다. 이 틀은 신뢰도 지도다. 어떤 velocity 출력을 하류 분석가가 직접 신뢰할 수 있고 어떤 것이 직교 검증을 요구하는지를 따지는 것이지, "우리가 방법 X를 이겼다"는 비교가 아니다. 우리의 목적 함수 분석이 모수 식별가능성(parameter identifiability)에 닿는 지점에서, velocity 전환 시각의 약한 식별가능성은 ConsensusVelo가 우도 평탄성과 Fisher 정보로 이미 보였음을 먼저 밝혀 둔다 [16]. 그 연구는 우리 기제를 확증하는 쪽이며, 우리의 새로운 기여는 측정 앵커 신뢰도 지도 그 자체, 곧 α-stiff/lag-sloppy *분리(dissociation)*, 그것의 외부 anchoring, 그리고 multiome 확장이다.

---

## Results

### 전사 속도 α만 방법 간 재현되며, chromatin에서 transcription으로 이어지는 시간차(lag)는 재현되지 않는다

방법 간에 유전자별 시간차(lag)는 일치하지 않았다. HSPC에서 원래의 부호 포함 정의로 계산한 시간차의 쌍별 Spearman 상관은 −0.04(MultiVelo 대 MoFlow, p=0.38), −0.01(MultiVelo 대 MultiVeloVAE, p=0.81), +0.08(MoFlow 대 MultiVeloVAE, p=0.04)이었다. 시간차 정의를 동일 기준으로 통일해도 가장 강한 쌍이 +0.12까지밖에 오르지 않았고, 크기 규약(magnitude convention)에서는 바로 그 가장 강한 쌍(MultiVelo 대 MultiVeloVAE)이 +0.163에 도달한다(95% CI [+0.078, +0.244], 0 배제). 따라서 시간차(lag)는 크기에서 잘해야 약하게 재현되며, 대부분의 쌍이 |ρ|≤0.08이다(Fig. 1, `figures/fig01_p2_concordance.png`). 방향도 더 낫지 않았다. 부호가 변할 수 있는(sign-variable) 방법들에서 chromatin 선행(chromatin-leading) 비율은 44.8%(MoFlow)와 49.3%(MultiVeloVAE)로, 50/50에 가까운 집단 균형이어서 유전체 전반의 "chromatin이 transcription을 예비 개방한다"는 순서를 뒷받침하지 않으며, MoFlow와 MultiVeloVAE 사이의 유전자별 부호 일치(sign-agreement)는 48%, 곧 우연 수준이었다. (MultiVelo가 겉보기에 100% chromatin 선행인 것은 그 전환 시각 단조 정렬 제약이 만든 인공산물(artifact)이므로, 크기 검정과 순위 검정에만 포함하고 부호 검정에는 결코 포함하지 않는다.) 네 번째 방법을 추가해도 일치도는 회복되지 않았다. CRAK-Velo의 시간차 부호 규약 버그를 확인·수정한 뒤 MoFlow 대 CRAK-Velo는 −0.151, CRAK-Velo 대 MultiVeloVAE는 −0.04였고, CRAK-Velo의 chromatin 선행 비율은 41.1%(균형)였다. 방법 간에 일치한 유일한 시간차(lag) 특성은 대표적 priming 마커(예: *CSF1R*, *S100A9*)의 방향으로, 이들은 부호 변동 방법 둘 다에서 chromatin 선행이었는데, 이 점은 아래에서 다시 다루며 엄격히 상관적(correlational) 사실로만 읽는다.

순열 FDR 분석(유전자 라벨 shuffle 귀무, N=10⁴)은 이 약함을 통계적으로 확인했다. cross-method ρ는 3쌍 중 2쌍에서 shuffle 귀무 대비 유의했으나, 효과는 극히 약했고(|ρ|≤0.15) 방향이 일관되지 않았다. 유전자별 cross-method 부호 일관성 검정은 빈 일치 집합을 냈다(FDR<0.10에서 0/598 유전자). 우리는 이를 헤드라인이 아니라 **CRAK 의존 민감도 결과(CRAK-dependent sensitivity result)**로 보고하는데, 그 빈 집합은 부호 변동 방법 세 개를 필요로 하고, 깨끗한 부호 변동 쌍({MoFlow, MultiVeloVAE})만으로는 두 방법 부호 검정이 검정력에 제약되기 때문이다(신호와 무관하게 min p_perm≈0.50). 따라서 CRAK와 무관한 깨끗한 헤드라인은, 시간차(lag)가 크기에서 잘해야 약하게 재현되고(가장 강한 쌍 +0.163, 대부분의 쌍 |ρ|≤0.08) 부호에서는 우연 수준(48%)에 그친다는 것이다.

이와 뚜렷이 대조적으로, 전사 속도 α는 방법 간에 강하게 재현되었다(Spearman ρ=0.88, *관측값*; MultiVelo 대 MultiVeloVAE 축에서 짝지은 부트스트랩(paired-bootstrap) ρ=+0.882, 95% CI [+0.855, +0.905]). 시간차(lag) 취약성의 뿌리는 진단적이다. 시간차를 정하는 chromatin 개방 속도 α_c가 그 자체로 방법에 민감하고(ρ=0.29; +0.291, 95% CI [+0.209, +0.369]), 그래서 시간차는 α_c의 방법 민감성을 물려받는 반면 α는 그렇지 않다. 어떤 유전자가 chromatin 선행인지는 방법을 바꾸면 달라지지만(비강건), α와 집단 수준의 방향 균형은 수렴한다(강건). 이것이 두 신뢰도 축 가운데 첫째이며, 전사 속도는 이를 통과하고 시간차(lag)와 γ는 통과하지 못한다.

### Chromatin은 시간차(lag)를 만들지 않는다: 인과 음성 대조군

lineage 내에서 ATAC를 뒤섞어 chromatin과 RNA의 결합을 끊고 MultiVelo를 다시 fitting해도 시간차(lag) 분포는 원본과 통계적으로 동일했고(Mann–Whitney p=0.20, Kolmogorov–Smirnov p=0.51), 유전자별 시간차 순위를 보존했으며(ρ=0.72), chromatin 우도를 움직이지 않았다(0.239에서 0.237). 짝지은 Wilcoxon 검정만이 미미한 이동을 검출했고(p=0.0003, 중앙값 5.87에서 5.48), 이는 많아야 미미한(marginal) chromatin 기여를 시사한다. 이 음성 대조군은 구조적으로 독립인 두 번째 방법에도 확장되었다. MoFlow 시간차(lag)도 shuffle을 견뎠다(유전자별 ρ=0.52로, cross-method 교체 시의 ρ=0.08보다 훨씬 높고, chromatin 채널 fitting 품질은 변화 없음). 시간차(lag)는 chromatin 신호가 아니라 모델 구조(전환 시각 정렬)와 유전자 고유의 RNA 동역학에서 비롯되며, 이는 MultiVelo의 100% chromatin 선행이 구조적임을 독립적으로 확인한다. 우리는 이 음성 대조군을 main figure로 승격한다(Fig. 2, `figures/fig_atac_shuffle_causal.png`). 선행 velocity 연구에 견주어 이 벤치마크에서 가장 특징적인 대조군이기 때문이다. 우리가 아는 한, 어떤 원저 방법 논문도 자신의 시간차(lag)에 chromatin 제거(ablation) 대조군을 적용하지 않았다.

여기서 파생되는 한 결과가 명명된 priming 마커에 닿는다. 이 마커들은 방법 간에 일치한 유일한 시간차(lag) 특성이었으므로(앞 소절), 우리는 그 일치가 그 특정 locus의 chromatin에 의해 *생기는지*를 검정했다. 만약 chromatin이 마커의 시간차를 만든다면, ATAC를 뒤섞을 때 명명된 마커의 시간차가 나머지보다 더 크게 흔들려야 한다. 그렇지 않았다. 편향 보정한 상대 변화 척도에서 명명된 마커는 나머지 유전자보다 더 움직이지 않았고(마커 중앙값 0.137 대 나머지 0.144; 마커>나머지 Mann–Whitney p=0.58), 일부 마커가 절댓값으로 더 크게 움직인 것은 chromatin이 아니라 그들의 더 큰 baseline 시간차를 따랐다(|Δlag|가 시간차 크기와 상관, ρ=+0.24). 따라서 우리는 마커 방향의 cross-method 일치를 일관된 priming 생물학에 관한 *상관적* 사실로 읽으며, 그 locus에서 chromatin이 시간차(lag)를 만든다는 인과 주장은 하지 않는다.

### α는 예측하는 baseline feature가 시간차(lag)는 예측하지 못한다

우리는 시간차(lag)를 세 축(정확도, 안정성, 예측 가능성)에서 더 삼각 측량했으며, 하류 사용에 중요한 예측 가능성 축을 여기서 요약한다(전체 삼각 측량은 Supplementary Note S1). 순수 baseline chromatin feature만으로는 held-out(학습에서 제외한) lineage에 걸쳐 시간차(lag)를 예측하지 못했고(ρ=−0.21), fitting된 kinetic feature를 더하면 +0.59까지 올랐지만 이는 순환적이다(fitting된 α_c가 MultiVelo 시간차를 기계적으로 결정하기 때문). 실제 day0 ATAC promoter/enhancer 접근성(8,583개 day0 HSC/MPP 세포에 걸친 511개 유전자)을 모으자 대비가 선명해졌다. *강건한* 표적 α는 held-out lineage에서 예측되었으나(ρ=+0.309, 여섯 lineage 모두에서 양수), *비강건한* 시간차(lag)는 실제 ATAC로도 예측 불가능한 채였다(ρ=+0.05, 우연)(Supplementary Fig. S2, `figures/lag_model.png`). 동일 방법 내에서 lineage를 가로지른 재-fitting도 같은 이야기를 했다. 시간차 크기는 따로 fitting한 lineage들 사이에서 약하게만 일치했고(중앙값 ρ=0.349, 범위 0.234–0.513), 그 α_c 대조는 더 강건했다(중앙값 ρ=0.483). 강건한 α를 예측하는 바로 그 baseline feature들이 비강건한 시간차(lag)는 예측하지 못하며, 그렇기 때문에 하류 timing 모델은 단일 시간차 값이 아니라 baseline feature와 α 위에 세워야 한다. (완결성을 위해, 시간차를 주입한(injected-lag) 정확도 시뮬레이션과 부트스트랩 부호 안정성 점검은 Supplementary Note S1에 보고한다. 정확도 시뮬레이션은 매끄러운 동역학에서 CRAK-Velo DTW 구성이 만드는 형태(shape) 인공산물로, 핵심 MoFlow/MultiVelo/MultiVeloVAE arm에는 닿지 않는다.)

### α-강건, lag-취약 순서는 사전등록 검정을 포함한 다섯 개 외부 시스템에서 재현된다

이 순서가 한 HSPC 데이터셋의 특이성인지를, 조직 거리(tissue distance)를 아우르는 다섯 개 외부 multiome에서 재현하며 물었다(Fig. 3, `figures/fig02_crossdataset_concordance.png`; Table 1). 핵심 주장은 어떤 절댓값이 아니라 *α가 시간차(lag)보다 앞선다는 순서의 보존*이다.

각 외부 데이터셋 내부에서 cross-method α(floor, MultiVelo, MultiVeloVAE, 세 쌍의 중앙값)는 강하게 재현된 반면 dataset 내부 시간차(MultiVelo 대 MultiVeloVAE)는 0 근처에 머물렀다. E18 마우스 뇌 α 중앙값 +0.81 대 시간차 +0.057; 인간 BMMC +0.851 대 −0.088(p=0.15); 대식세포 +0.865 대 +0.074(TOST로 0과 동등); 마우스 gastrulation +0.927 대 −0.026([−0.089, +0.038]), dataset 내부 분리 Δρ=+0.979(95% CI [+0.916, +1.041]). 데이터셋을 가로질러서도 HSPC-대-외부 α 순위는 모든 시스템에서 그 시간차(lag) 대응값보다 높게 재현되었다. 인간 태아 피질 α +0.475(p=4.5e-7) 대 시간차 +0.185(p=0.06); E18 +0.32(p=2e-4) 대 +0.10(p=0.23); BMMC +0.550(p=2.9e-8) 대 +0.052(p=0.63); 대식세포 +0.643(95% CI [+0.554, +0.719], p=2.5e-33) 대 +0.148(95% CI [+0.027, +0.263], p=0.014); gastrulation +0.415(95% CI [+0.244, +0.561]) 대 +0.028(95% CI [−0.165, +0.224]). 대식세포 축은 명시적 cross-dataset 분리 Δρ=+0.843(95% CI [+0.773, +0.912])을 준다.

다섯 번째 외부 시스템인 마우스 gastrulation(GSE205117, E7.5–E8.75 10x Multiome, 10,779 세포)은 lineage priming이 최대이고 시간차(lag)가 방법에 *가장* 민감할 것으로 예상되는 발생 atlas인데, **사전등록(preregistration)**으로 검정했다. 사전 선언한 임계를 가진 여섯 개 예측을 어떤 velocity fitting이나 일치도가 존재하기 전에 commit 해시로 봉인했고(`PREREGISTRATION_gse205117.md`), 사후(post-hoc) 구제는 허용하지 않았다. 여섯 개 모두 통과했다(6 PASS / 0 FAIL). dataset 내부 cross-method α ρ≥0.50(봉인된 합격선, `PREREGISTRATION_gse205117.md:15`; 이것은 임계일 뿐이며 HSPC α=0.88은 합격선이 아니라 *관측값*임에 유의), dataset 내부 시간차 ρ≤0.15, α에서 시간차를 뺀 순서 간격 ≥0.35, cross-dataset α>+0.2 및 α>lag, α 불일치보다 큰 유전자별 시간차 불일치(봉인된 원 정의 MultiVelo 대 MoFlow 기준 유전자별 불일치 시간차 0.294, n=968, 대 α 0.052), 그리고 최대 priming 하에서도 지속되는 취약성. 이 예측들이 fitting 이전에 봉인되었기 때문에, 이 재현은 사후 패턴이 아니라 확증적이다.

**숨김없이 밝히는 유의점(Table 1 각주).** (i) cross-dataset α 값은 조직 거리가 멀어질수록 감소하지만(대식세포 +0.643 > BMMC +0.55 > 뇌 +0.475 > gastrulation +0.415 > E18 +0.32), 이들의 95% CI는 겹친다(공통 구간 [0.368, 0.472]). 따라서 우리는 이를 *정성적(qualitative)* 순서로만 제시하고 점들에 어떤 추세도 fitting하지 않는다. (ii) dataset 내부 lag-취약 근거는, HSPC가 아닌 네 시스템에서 대체로 단일 방법 쌍(MultiVelo 대 MultiVeloVAE)에 의존한다. gastrulation만 추가로 MoFlow arm을 가지며, 그 봉인된 유전자별 시간차 예측에 쓰였다. (iii) 다섯 재현은 각각 공여자/시료 하나씩이다. 서사는 어느 한 시스템의 강한 일반화가 아니라 여섯 축에 걸친 일관성에 기댄다. (iv) 인간 태아 피질(GSE162170)은 dataset 내부 MultiVeloVAE fitting이 없어 dataset 내부 cross-method 시간차를 계산할 수 없다. 그 α 대 시간차 증거는 cross-dataset 축이다(Table 1, N/A).

### Fitting된 전사 속도 α는 (γ와 달리) 외부에서 측정된 속도를 복원한다

출력들을 가장 깨끗하게 갈라놓는 축은 fitting된 속도가 *독립적으로 측정된* kinetic 양을 복원하는지다. velocity 출력 가운데 측정된 외부 대응물을 가진 것은 둘뿐이다. 전사 속도 α(TT-seq 합성 대비)와 분해 속도 γ(SLAM-seq 반감기 대비)다. 시간차(lag), α_c, β는 측정된 ground truth가 없으므로, 이 외부 축은, 그리고 제목·초록의 "외부 anchoring" 틀은, 바로 이 두 속도에 대한 검정이다. 우리는 순위 기반 검정만 썼다(절대 속도는 비식별이고 설정은 cross-context다; 모든 ρ는 짝지은 부트스트랩 95% CI를 동반, B=10⁴; 헤드라인은 비-housekeeping 층이다). Fitting된 α는 세 방법 모두에서 측정된 K562 TT-seq 합성 속도(GSE229305, 반감기 패널과 같은 연구)를 복원했다. 비-housekeeping ρ = +0.236 [+0.095, +0.368](RNA 전용 floor, p=9.6e-4, n=193), +0.262 [+0.133, +0.385](MultiVelo, p=4.9e-5, n=235), +0.285 [+0.165, +0.398](MultiVeloVAE, p=4.4e-6, n=251)로, cross-context 설정(K562에서 측정, HSPC에서 fitting)에도 불구하고 모두 CI가 0을 배제했다(Fig. 4, `figures/fig_external_rate_anchor.png`).

이와 대조적으로 분해 속도 γ는 외부 ground truth가 있는 곳에서도 복원되지 *않았다*. 가장 깨끗한 동일 기준 비교(같은 K562 세포)에서 세 방법 모두 측정된 분해 속도에 대해 γ는 귀무였으나(rna-only −0.118, MultiVelo +0.053, MultiVeloVAE −0.011; 3/3 귀무) α는 셋 다 양수였다. 세 세포주 반감기 패널로 확장하면 9개 방법×세포주 칸 중 1개만 γ를 약하게 복원했고(MultiVeloVAE 대 MOLM13, +0.164 [+0.028, +0.291], CI 하한이 0을 겨우 넘음), 교과서적 scVelo dynamical γ(RNA 전용 floor)는 가장 깨끗하고 검열되지 않은 참조(MOLM13, −0.224 [−0.359, −0.085], CI가 0 배제)에서 *반대로* 나왔다. 곧 fitting된 γ가 더 큰 유전자일수록 측정된 반감기가 *더 길었다*. 이는 외부 실험 축에서 신뢰도 분화를 확인한다. α는 방법 재현성과 측정 anchoring을 모두 갖춘 유일한 속도인 반면, γ는 ground truth가 있는 곳에서도 외부적으로 실패하고 심지어 거꾸로 간다. (−0.224 반전은 MultiVelo의 γ가 아니라 scVelo/RNA 전용 γ의 성질이다. 우리는 이를 전반적으로 그 방법에 귀속시키며, 다른 어떤 방법의 fitting에 대한 증거로 쓰지 않는다.)

**함께 보고하는 음성 결과(honest null).** 독립적인 두 번째 α 출처(Schwalb 2016 K562 TT-seq, GSE75792)는 *귀무*였다. α 대 Schwalb는 3/3 귀무(ρ −0.05 ~ −0.01)였던 반면 α 대 Todorovski는 3/3 양수였다. 결정적 원인은 측정된 두 TT-seq 출처 자체가 약하게만 일치한다는 것이다(ρ≈0.15, n=1905). 측정된 합성 속도의 연구 간 재현성이 어떤 확증에도 천장(ceiling)이 된다. 우리는 이를 비대칭적으로, 그리고 사전등록한 대로 해석한다. 이 귀무는 α를 반증하지 않는다(cross-context, 절대-α 비식별성, 출처 잡음이 모두 작용한다). 다만 이는 "단일 외부 출처" 취약성이 이 두 번째 출처로 제거되지 않았음을 뜻한다. 일차 anchor는 유효하며, 있는 그대로 읽으면 두 번째 출처는 재현도 반증도 아니다.

### 이 분리는 목적 함수의 성질이다: α는 stiff, 시간차(lag)는 sloppy

이 관찰이 *왜* 반복되는지 묻기 위해, MultiVelo 자체 우도를 α 방향과 시간차 방향(lag = t_sw2 − t_sw1)을 따라 프로파일링하며 latent time을 재최적화했다(n=538 유전자; fitting/우도 재현 r≈1.0)(Fig. 5, `figures/fig05_profile_likelihood.png`). 세포당 곡률(curvature)은 시간차보다 α에서 훨씬 컸다(세포당 중앙값 8.20 대 2.24). 우리는 유전자별 강성비(stiffness ratio) κ_α/κ_lag를 보수적인 **nuisance 모수 해방(freed-nuisance)** 기준에서 보고한다. 곧 β, γ, α_c, rescale, scale_cc를 재최적화하는 경우인데, 여기서 분리는 중앙값 비 **2.49×**, 유전자의 **77.03%**에서 α가 시간차보다 더 stiff한 채로 유지된다(n=148). 더 엄격한 nuisance 고정(fixed-nuisance) 프로파일은 더 큰 3.53×(IQR [1.92, 7.41])를 주고 유전자의 94.57%에서 α가 더 stiff한데, 우리는 이를 상한(upper bound)으로 다루며, β와 γ를 해방하면 α 곡률이 고정 시 값의 중앙값 0.19×로 붕괴함을 숨김없이 밝힌다. 시간차 삼분류가 이 점을 뒷받침했다. 538개 유전자 중 302개(56%)는 내부(interior), 205개(38%)는 경계 고정(boundary-pinned), 31개(6%)는 퇴화(degenerate)였고, 44%에서는 데이터가 시간차의 상한조차 설정하지 못한다. 이는 시간차 방향의 *상대적(실질적)* 비식별성이지, 완전히 평평한 골짜기가 아니다. velocity 전환 시각 자체의 약한 식별가능성은 ConsensusVelo가 우도 평탄성과 Fisher 정보로 확립했다 [16]. 우리의 목적 함수 분석은 그것을 확증하며, 선점되지 않은 것은 α-stiff/lag-sloppy *분리*, 곡률비(curvature-ratio) 틀, 그리고 multiome chromatin-대-시간차 확장이다 [17,18,19].

fitting된 모수를 cross-method 재현성으로 순위 매기면 경험적 식별가능성 순서 **α ≫ α_c > β > γ**가 나온다(α +0.882; α_c +0.291 [+0.209, +0.369]; β +0.080 [−0.009, +0.168]; γ −0.109 [−0.192, −0.023]). 시사적으로, ATAC 채널이 전혀 없는 RNA 전용 floor도 chromatin 방법 수준의 강도로 α를 복원한다(floor 대 MultiVelo +0.818 [+0.773, +0.855]; floor 대 MultiVeloVAE +0.889 [+0.862, +0.910]). 차분 예산(diff-budget) 분석은 시간차가 왜 가장 나쁜지를 보인다. 시간차는 두 속도-시간척도(rate-timescale)의 차이이며, 1/α는 +0.882로, 1/α_c는 +0.291로 일치하지만 그 차이는 더 약한 성분보다도 낮게 떨어진다(+0.124 [+0.036, +0.210]). 차분이 잡음을 증폭하기 때문이다.

우리는 이 내부 식별가능성이 어떤 출력이 외부적으로 검증되는지를 *예측하는지*를 물었다. 목적 함수 기하와 측정 anchor를 잇는 자연스러운 다리다. 부분적으로 정렬하지만, 현재 데이터로는 법칙을 확증할 수 없다. 네 속도를 목적 함수 강성으로 순위 매기면(α ≫ α_c > β > γ) 외부 ground truth가 있는 두 속도가 양 끝에 놓이고, 그 둘은 예상한 순서로 검증된다. 가장 stiff한 α는 측정된 합성 속도를 복원하는 반면, 가장 sloppy한 γ는 어떤 multiome 방법으로도 복원되지 않으며(MultiVelo/MultiVeloVAE 귀무), RNA 전용 scVelo γ는 여기에 더해 *반대로* 간다(−0.224). 그러나 이 모수 간(between-parameter) 배치는 본질적으로 두 점뿐이며(외부 anchoring된 속도는 α와 γ뿐이고, 두 점은 언제나 단조다), 그것만으로는 추세를 확립할 수 없다. 공정한 검정은 오히려 모수 *내부(within)*의, 유전자 *간(between-gene)* 검정이다. "더 stiff한 유전자가 더 잘 검증되는가"이며, 이는 시사적일 뿐이다. α 유전자를 강성 삼분위로 나누면 방향은 예측대로 단조이고(Spearman(α, 측정된 합성)이 저·중·고 삼분위에 걸쳐 0.116, 0.153, 0.302로 상승) 최상위 삼분위만 0을 넘지만(ρ=+0.302, 95% CI [+0.068, +0.511]), 결정적인 상위-하위 대비는 유의하지 않고(Δρ=+0.186, 95% CI [−0.149, +0.504], 삼분위당 n=70), γ 축은 강성 경사가 전혀 없다(평평한 귀무). 따라서 우리는 식별가능성과 외부 검증의 연결을 헤드라인 법칙이 아니라 *시사적 보조 관찰(suggestive supporting observation)*로 보고한다. 내부 식별가능성은 외부 검증과 부분적으로 정렬하나 현재의 검정력으로는 확증할 수 없으며, 외부 anchoring된 유전자 집합을 넓히는 것이 다음 단계다. 아래 신뢰도 지도의 어떤 것도 이 연결에 기대지 않는다.

### 합성 양성 대조군: 시간차(lag) 비재현성은 방법 결함이 아니라 regime 특유의 현상이다

이 실패가 버그가 아니라 데이터 regime의 성질임을 보이기 위해, 알려진 주입 onset 시간차 τ를 가진 chromatin-대-RNA pulse ODE를 switch-sharpness × SNR 격자에서 시뮬레이션하고, 구조적으로 독립인 두 방법(MoFlow DTW chromatin–spliced 시간차, MultiVelo 전환 시각 시간차)을 공유 유전자 축에서 fitting했다(짝지은 부트스트랩 95% CI, B=10⁴)(Fig. 6, `figures/fig_sim_positive_control.png`). 식별가능성 코너(높은 SNR, 중간 sharpness; W=0.1, SNR=20)에서 두 방법은 서로(일치도 ρ=+0.454 [+0.20, +0.67], CI가 0 배제), 그리고 주입된 τ와도(MoFlow +0.506, MultiVelo +0.672) 일치했다. SNR이 떨어지자 일치도는 0을 향해 붕괴했다(SNR 주변 평균 20이 +0.242, 6이 −0.035, 2가 −0.005). 검정력 보정은 실제 HSPC의 시간차 일치도가 검정력 인공산물이 아니라 진짜로 약함을 보인다. n=598, N_perm=10⁴에서 이 장치는 |ρ|≳0.15의 일치하는 시간차를 검정력 ≥0.8로 검출하며, 실제 HSPC는 바로 그 하한에 있다. 대부분의 쌍(|ρ|≤0.08)은 그 아래여서 검출되지 않고, 오직 가장 강한 크기 쌍(+0.163)만이 겨우 검출 가능한데, 이는 보정이 예측한 그대로다. 따라서 cross-method 시간차 불일치는 어떤 방법의 결함이 아니라 실제 HSPC가 속한 (저-SNR, 매끄러운) regime의 성질이다. 식별가능성 코너는 좁고(유전자당 SNR=20은 비현실적으로 높다), 이는 실제 데이터가 비식별 regime에 산다는 주장을 강화할 뿐이다.

### 신뢰도 지도: 어떤 velocity 출력을 신뢰하고 어떤 것을 검증할 것인가

여러 축을 모으면 하나의 사용 진술이 나오며, 우리는 이를 Discussion에 묻힌 조언이 아니라 결과로서 여기 보고한다(Table 2; 시각 요약 Fig. 7, `figures/fig_reliability_heatmap.png`). 내부(cross-method) 축과 외부(측정 속도) 축 모두에서 신뢰할 수 있는 출력은 정확히 하나, 전사 속도 α다. α는 방법 간에 재현되고(ρ=0.88), RNA 전용 floor로도 복원되며, 측정된 합성 속도에 anchoring되고(비-housekeeping ρ +0.24 ~ +0.29), 실제 baseline ATAC에서 예측된다. 두 출력은 내부 축에서만 신뢰할 수 있어 집단 진술로 쓸 수 있다. 약 50/50의 방향 균형(두 방법이 수렴)과 대표 priming 마커의 cross-method *방향* 일치(인과가 아니라 상관적 사실이다. ATAC shuffle이 마커의 시간차를 나머지보다 더 흔들지 않았다)다. 나머지는 모두 신뢰할 수 없다. chromatin 개방 속도 α_c(cross-method ρ=0.29), 분해 속도 γ(cross-method ρ≈−0.1이고 외부적으로 복원되지 않음), 유전자별 시간차 크기(대부분의 쌍 |ρ|≤0.08, 가장 강한 쌍 +0.163, baseline에서 예측 불가), 그리고 시간차 부호와 절대 timing(48% 일치, 구조적으로 편향되어 정보 없음)이다. 이 지도의 실질적 내용은 라우팅 규칙이다. 하류 분석가는 α와 속도에서 파생된 신호는 직접 소비하되, 단일 방법의 시간차·부호·γ는 직교 측정 없이 소비해서는 안 된다.

---

### Table 1. 여섯 개 시스템에 걸친 α 대 시간차(lag)의 방법 간 재현성

dataset 내부 항목은 cross-method Spearman ρ이다(α는 RNA 전용 floor, MultiVelo, MultiVeloVAE, 세 쌍의 중앙값; 시간차는 MultiVelo 대 MultiVeloVAE, 부호 포함 규약 — 각주 † 참조). cross-dataset 항목은 HSPC-대-외부 순위 ρ이다. 이 표는 *cross-method 재현성만* 보고하며, 방법 내부(within-method) fitting 품질로 읽어서는 안 된다(Table 2는 설계상 분리 유지).

| 시스템 | 조직 관계 | dataset 내부 α(중앙값) | dataset 내부 lag(MV 대 VAE) | cross-dataset α(HSPC 대 외부) | cross-dataset lag |
|---|---|---|---|---|---|
| HSPC (GSE209878) | 일차 | 0.88 | −0.01 (p=0.81)† | — | — |
| 대식세포 분화 (GSE284047) | HSPC 직접 | +0.865 | +0.074 (≈0, TOST) | +0.643 [+0.554,+0.719] | +0.148 [+0.027,+0.263] |
| 인간 BMMC (GSE194122) | 같은 조직 | +0.851 | −0.088 (p=0.15) | +0.550 (p=2.9e-8) | +0.052 (p=0.63) |
| 인간 태아 피질 (GSE162170) | 원거리 | N/A‡ | N/A‡ | +0.475 (p=4.5e-7) | +0.185 (p=0.06) |
| 마우스 gastrulation (GSE205117) | 발생, priming 최대 | +0.927 | −0.026 [−0.089,+0.038] | +0.415 [+0.244,+0.561] | +0.028 [−0.165,+0.224] |
| E18 마우스 뇌 (10x 데모, GSE 없음) | 종간(cross-species) | +0.81 | +0.057 | +0.32 (p=2e-4) | +0.10 (p=0.23) |

† HSPC dataset 내부 시간차 값 −0.01은 부호 포함 규약에서의 MultiVelo 대 MultiVeloVAE 수치다(이 cross-dataset 열 전반에서 쓰는 규약). 같은 축을 크기 규약(기제 분석에 쓰인 규약)으로 계산하면 +0.163(95% CI [+0.078, +0.244])이다. 둘이 다른 이유는, 0에 가깝고 부호가 불안정한 시간차에 부호를 매기면 반대 부호가 상쇄되는 반면 크기는 상쇄되지 않기 때문이다. 재현성 주장의 헤드라인은 크기 규약이며, 그에 따르면 시간차는 잘해야 약하게 재현된다(가장 강한 쌍 +0.163, 대부분의 쌍 |ρ|≤0.08).
‡ 인간 태아 피질(GSE162170, Trevino 2021 발생기 피질)은 dataset 내부 MultiVeloVAE fitting이 없어(MultiVelo와 floor만) dataset 내부 cross-method 시간차와 α를 계산할 수 없다. 그 증거는 cross-dataset 축이다.
cross-dataset α의 CI가 겹치므로 조직 거리 순서는 정성적이며 단조 주장이 아니다. 다섯 외부 재현은 각각 공여자/시료 하나씩이다. 마우스 gastrulation은 fitting 전에 봉인된 사전등록 6/0 채점표를 통과했다(α 합격선 ρ≥0.50, `PREREGISTRATION_gse205117.md:15`; HSPC 0.88은 합격선이 아니라 관측값).

### Table 2. 측정 앵커 velocity 출력 신뢰도 결정 지도

Table 1과 의도적으로 분리한다. 이것은 velocity 출력의 *사용(usage)* 지도이지, 방법 내부 fitting 품질을 cross-method 재현성에 섞은 것이 아니다. "신뢰 가능"은 해당 축을 통과했다는 뜻이며, 외부 anchor가 더 강한 기준이다.

| Velocity 출력 | cross-method 재현성(내부) | 외부 측정 anchor | 신뢰도 | 권장 조치 |
|---|---|---|---|---|
| 전사 속도 α | 높음 (ρ=0.88; floor가 복원) | 있음 (측정된 TT-seq 합성, 비-HK ρ +0.24 ~ +0.29, CI가 0 배제) | **신뢰 가능** | 직접 사용; 하류 feature로 선호 |
| 집단 방향 균형 (~50/50) | 높음 (두 방법 수렴) | — | **신뢰 가능(집단 진술)** | 집단 수준 진술로만 사용 |
| 대표 priming 마커 방향 | 높음 (방법 간 일치) | 상관적일 뿐 (ATAC-shuffle 귀무, MW p=0.58; 인과 근거 없음) | **상관으로서 신뢰 가능** | 명명된 locus에 상관적 방향으로 사용, 유전체 전반 불가, 인과 불가 |
| chromatin 개방 속도 α_c | 낮음 (ρ=0.29) | — | **신뢰 불가** | 사용 전 안정화(부트스트랩 또는 lineage별) |
| 분해 속도 γ | 낮음 (ρ≈−0.1) | 없음 (K562 3/3 귀무; scVelo γ 반전, −0.224, CI가 0 배제) | **신뢰 불가** | 있는 그대로 사용 금지 |
| 유전자별 시간차 크기 | 낮음 (대부분의 쌍 |ρ|≤0.08; 가장 강한 쌍 +0.163) | baseline에서 예측 불가 (≈우연) | **신뢰 불가** | 직교 검증 필요; 단일 방법 값 사용 금지 |
| 유전자별 시간차 부호 / 절대 timing | 우연 (48% 일치); 구조적으로 편향 | — | **신뢰 불가(정보 없음)** | 사용 금지; 부호는 구조적으로 양수여서 정보가 없음 |

*재고 표(velocity arm; 외부 데이터셋)는 GB 표준 형식의 Supplementary Table S1–S2로 제공한다.*

---

## Discussion

드러나는 그림은 velocity 출력을 신뢰도로 깔끔하게 분류하는 것이며, 그 두 축은 보통 따로 검정된다. 전사 속도 α만이 둘 다 통과한다. 방법 간에 ρ=0.88로 재현되고, chromatin 채널 없이도 복원되며, 측정된 TT-seq 합성 속도에 anchoring되고, 실제 day0 ATAC에서 예측된다. chromatin에서 transcription으로 이어지는 시간차(lag)는 어느 축도 통과하지 못한다. cross-method(크기가 약하고 대부분의 쌍 |ρ|≤0.08, 가장 강한 쌍 +0.163, 부호는 우연), 인과(chromatin-shuffle에 불변), 예측(baseline에서 우연) 모두에서 그렇다. 분해 속도 γ는 두 축 모두에서 취약해, 방법 간에 재현되지 못하고 ground truth가 있는 곳에서도 측정된 반감기를 복원하지 못하며, 교과서적 scVelo γ는 실제로 거꾸로 간다. 시간차를 정하는 α_c가 그 자체로 취약하고(ρ=0.29), 시간차는 두 속도-시간척도의 *차이*이므로 차분이 그 일치도를 더 약한 성분보다도 아래로 끌어내린다. 이 순서가, 시간차가 방법에 가장 민감할 것으로 예상된 priming 최대의 gastrulation 시스템에서 사전등록 검정을 견뎌낸다는 것은 확증이 취할 수 있는 가장 강한 형태다. 이 연구의 새로움은 시간차에 대한 음성 결과 하나도, 식별가능성 기제 하나도 아니고, *측정 앵커* 신뢰도 지도, 곧 출력을 내부 일치뿐 아니라 외부 실험 축으로 분류한 데 있다.

우리는 이것이 무엇을 주장하고 무엇을 주장하지 않는지에 신중하다. 이는 생물학이 아니라 *방법과 그 신뢰도*에 대한 진술이다. chromatin priming은 특정 locus에서는 실재하며(대표 마커들은 방법 간에 방향이 일치하는 상관적 사실이나, ATAC shuffle이 명명된 마커의 시간차를 나머지보다 더 흔들지 않았으므로 이를 인과로 승격하지 않는다, Mann–Whitney p=0.58), 더 깊은 sequencing, 더 세밀한 시간 해상도, 또는 metabolic labeling이 시간차(lag)를 식별 가능하게 만들 여지도 아직 있다. 우리의 주장은 *현재의* 방법들이 뒷받침하는 것에 대한 경계다. 세 가지 추가 한계가 핵심적이다. 첫째, pseudotime은 실제 흐른 시간(wall-clock)이 아니다. day0과 day7 batch가 통합되어 있어서 시간차(lag)는 pseudotime 단위이고 실제 시간에 anchoring할 수 없다. 둘째, 프로파일 우도 결과는 *상대적(실질적)* 비식별성이지 완전히 평평한 골짜기가 아니다. 우리는 이를 보수적인 nuisance 해방 기준(2.49×, 유전자의 77%에서 α가 더 stiff)에서 보고하는데, nuisance 모수를 해방하면 α 곡률이 부분적으로 붕괴하고 더 엄격한 nuisance 고정의 3.53×는 상한일 뿐이기 때문이다. 셋째, 우리는 목적 함수 곡률이 외부 검증을 예측한다고 주장하지 *않는다*. 모수 내부의 유전자 간 검정은 검정력이 부족하다(최상위 삼분위 α ρ=+0.30은 0을 넘지만 상위-하위 대비 Δρ=+0.186은 넘지 못하며, 삼분위당 n=70이고 γ 축은 경사가 없다). 따라서 식별가능성은 외부 검증과 *시사적으로만* 정렬하며, 신뢰도 지도는 이 연결이 아니라 두 신뢰도 축에서 직접 구성한다. lag-취약 근거는 HSPC 밖에서는 대체로 단일 방법 쌍(MultiVelo 대 MultiVeloVAE)에 의존하며, MoFlow arm이 연결된 gastrulation만 예외다. 다섯 외부 재현은 모두 단일 시료이고, 외부 α anchor는 주로 하나의 TT-seq 출처에 기댄다. 독립적인 Schwalb 출처가 귀무였고 두 측정 출처가 ρ≈0.15로만 일치하기 때문이다. α anchor에 대한 추가 유의점은 abundance 교란이다. α와 측정된 TT-seq 합성 속도 둘 다 transcript abundance를 따라갈 수 있으므로(s_ss = α/γ), +0.24 ~ +0.29 상관은 일부가 abundance 공변량일 수 있다. 비-housekeeping 층으로 제한하면 이를 부분적으로 완화하고 생물물리(α와 합성 속도의 대응)가 그 상관을 *예측*하지만, 이 순위-방향 검정만으로는 α가 abundance가 아니라 합성 kinetics를 특정해 포착하는지를 확정하지 못한다. 끝으로, 이 연구의 모든 데이터는 10x Multiome이다. 또 다른 multiome assay(SHARE-seq skin, GSE140203)에 대해 저자 제공 정렬에서 velocity layer(spliced/unspliced)를 복원하려 했으나 사용 가능한 count를 얻지 못했다. 따라서 신뢰도 지도는 10x Multiome에 대해 확립된 것이며, 다른 multiome assay로의 일반화는 검정하지 않았다. 범위는 의도적으로 "multiome velocity 출력", 곧 chromatin 정보를 담은 시간차와 이 방법들의 속도 출력이며, 10x Multiome은 그것들을 평가한 기질(substrate)이다.

**선행 연구 대비 자리매김.** 유전자 수준 chromatin에서 transcription으로 이어지는 시간차(lag)는 MultiVelo가 생물학적 판독값으로 *도입*했고 [1] MultiVeloVAE와 MoFlow가 재정식화했다 [2,3]. 이들 중 어느 것도 시간차가 방법 간에 *같은 값*인지를 감사하지 않았으며, MoFlow의 한 번의 cross-method 비교는 유리한 부분집합에서의 일치를 보고했다 [3]. 2026년의 일반 벤치마크들은 velocity *방향*이 방법 의존적임을 확립하지만 [12,13] 개별 출력을 외부 측정에 견주어 채점하지 않는다. 우리의 기여는 측정 앵커 보완이다. 순열 귀무, 인과 음성 대조군, 그리고 선행 velocity 벤치마크에 없던 조각인 측정된 합성·분해 속도에 대한 외부 anchor를 갖춘 체계적 다중 arm 신뢰도 지도로, 어떤 파생 값(α)이 두 검정을 모두 견디고 어떤 것(시간차, γ)이 어느 것도 견디지 못하는지를 보인다. 식별가능성 측면에서, velocity 전환 시각 평탄성을 처음 보인 공은 ConsensusVelo에 정면으로 돌린다 [16]. single-cell kinetic 속도에 대한 프로파일 우도 [17], single cell에서의 sloppy/stiff Fisher 기하 [18], 구조적 시간 이동 축퇴(time-shift degeneracy) [19]가 추가적인 방법 선례다. 우리의 목적 함수 분석은 경험적 지도에 대한 *확증적 기제*이지 이 논문의 새로움이 아니다(Fig. 8, `figures/fig03_novelty_comparison.png`).

**하류 timing 예측에 대한 함의.** 신뢰도 지도(Table 2)의 실질적 성과는 설계 원칙이다. epigenetic 약물 반응 timing을 예측하는 모델은 단일 방법 시간차나 단일 방법 γ를 소비해서는 *안 된다*. 대신 우리가 검증한 강건한 경로, 곧 day0 ATAC promoter/enhancer 접근성에서 α로 이어지는 경로를 거쳐야 하며, 여기서는 시간차를 예측하지 못하는 바로 그 baseline feature들이 held-out lineage에서 α는 예측한다(ρ=+0.31). 이것은 벤치마크에서 유도한 설계 원칙이지 wet-lab으로 검증된 timing 예측기가 아니다. ATAC에서 α로, 다시 timing으로 이어지는 경로를 perturbation ground truth에 대해 검증하는 것이 자연스러운 다음 단계이며, 식별가능성이 외부 검증을 확증적으로 예측하는지를 검정하기 위해 외부 anchoring된 유전자 집합을 넓히는 것도 마찬가지다.

---

## Conclusions

multiome velocity 방법들이 산출하는 여러 유전자별 값 가운데, 전사 속도 α만이 하류 사용에 중요한 두 축 모두에서 신뢰할 수 있다. 방법 간에 재현되고(cross-method ρ=0.88, 관측값), RNA 전용 floor로 복원되며, 외부에서 측정된 합성 속도에 anchoring된다(비-housekeeping ρ +0.24 ~ +0.29). chromatin에서 transcription으로 이어지는 시간차(lag)는 크기에서 잘해야 약하게 재현되고(가장 강한 쌍 +0.163, 대부분의 쌍 |ρ|≤0.08) 부호에서는 우연 수준에 그치며, chromatin에서 비롯되지 않고, 우도에서 sloppy하다. 분해 속도 γ는 취약하고 외부 ground truth가 있는 곳에서도 복원되지 않으며, RNA 전용 scVelo γ는 심지어 거꾸로 간다. 이것은 현재 방법의 신뢰도에 대한 주장이지 timing 생물학의 부재에 대한 주장이 아니다. 이 연구의 기여는 그 결과로 얻은 측정 앵커 신뢰도 지도(α와 속도 파생 신호는 신뢰하고, 시간차·부호·절대 timing·γ는 직교 검증이 필요한 것으로 다룸)와, 어떤 timing 예측 모델이든 단일 방법 시간차가 아니라 강건한 day0-ATAC에서 α로 이어지는 경로 위에 세워야 한다는 구체적 하류 함의다.

---

## Methods

### 데이터셋

일차 데이터셋은 인간 HSPC 10x Multiome(GEO GSE209878)으로, day0와 day7 통합, 21,878 세포다. cross-dataset 재현에는 다섯 개 외부 multiome 시스템을 썼다. 인간 태아 피질(GSE162170, Trevino 2021), 태아 E18 마우스 뇌(10x Genomics "Fresh Embryonic E18 Mouse Brain 5k" 데모, CellRanger-ARC 1.0.0; MultiVelo 튜토리얼 데이터, GEO accession 없음), 인간 골수 단핵세포(bone-marrow mononuclear cells, BMMC; GSE194122, donor09/site4, spliced/unspliced는 velocyto로 GEX BAM에서 복원), 대식세포 분화(GSE284047 / figshare 30280333, Day14 HSPC 직접 분화), 그리고 마우스 gastrulation(GSE205117, E7.5/E8.0/E8.5/E8.75 rep1, 10x Multiome, 10,779 세포; GEX는 STARsolo Velocyto raw, ATAC는 gencode vM25로 gene body ±10 kb에 걸쳐 GEO fragment에서 집계). 모든 재현은 단일 공여자 또는 단일 시료다. pseudotime은 실제 흐른 시간(wall-clock)이 아님에 유의한다. 일차 데이터에서 day0과 day7이 batch 통합되어 있어 시간차(lag)는 pseudotime 단위로 표현되고 wall-clock anchor를 쓸 수 없다.

### 공통 전처리와 방법 분기

*방법* 차이를 *전처리(preprocessing)* 차이와 분리하기 위해, 모든 arm은 공통 전처리 분기를 공유했고 그 뒤 velocity 방법이 분기했다(공통 graph ablation 적용). cross-dataset arm은 위에 적은 대로 데이터셋별 spliced/unspliced 복원을 썼다. ATAC 집계는 데이터셋 출처에 따라 달랐고(HSPC는 `mv.aggregate_peaks_10x`; BMMC는 처리된 peak matrix의 gencode 근접 집계; gastrulation은 gene body ±10 kb에 걸친 GEO fragment), 이는 cross-dataset 순위 비교에 보수적 잡음을 더한다.

### Velocity 방법과 RNA 전용 floor

다섯 arm을 fitting했다. RNA 전용 floor(scVelo dynamical 모델, chromatin 채널 없음)와 네 개의 chromatin 정보 방법, 곧 MultiVelo [1](chromatin 전환 시각 ODE; lag = t_sw2 − t_sw1), MultiVeloVAE [2](VAE, 세포별 연속 decoupling/coupling), MoFlow [3](relay velocity; chromatin–spliced DTW 시간차), CRAK-Velo [4](준-기제적; DTW 유도 시간차)다. CRAK-Velo 시간차 부호 규약 버그(MoFlow의 `fastdtw`와 부호 반대)를 발견해 수정했다. CRAK-Velo의 시간차는 매끄러운 동역학에서의 형태 인공산물 때문에 민감도 arm으로만 보고한다. velocity arm 재고(모델 계열, chromatin 채널, 시간차 정의, 부호 규약)는 Supplementary Table S1로 제공한다.

### 일치도 통계

모든 cross-method·cross-dataset 일치도는 Spearman 순위 상관이었다. 출처 분석이 제공한 경우 상관에는 짝지은 유전자 부트스트랩 95% CI를 붙인다(B=10⁴ 재표집, seed 20260707, percentile 방법). 쌍별 헤드라인 상관은 출처가 제공하는 경우 그 p값과 n과 함께 보고한다. 시간차는 검정마다 단일 규약으로 보고했다. cross-dataset 재현성 표(Table 1)에서는 부호 포함 규약을, 기제(곡률) 분석과 헤드라인 재현성 지표에서는 크기 규약을 썼으며, HSPC MultiVelo 대 MultiVeloVAE 축에서 각각 −0.01과 +0.163을 준다(Table 1 각주 †에서 화해). MultiVelo의 구조적으로 양인 부호는 부호 검정에 결코 동원하지 않았다. cross-method 부호 일관성은 순열 FDR로 검정했다(유전자 라벨 shuffle 귀무, N=10⁴, FDR<0.10). 빈 일치 집합은, 깨끗한 부호 변동 쌍이 검정력에 제약되므로 CRAK 의존 민감도 결과로 보고한다. 0과의 동등성은 사전 선언한 |ρ|<0.2 경계에 대한 TOST로 평가했다. cross-dataset α의 조직 거리 순서는 CI가 겹치므로 정성적으로만 보고하며 점들에 추세를 fitting하지 않는다.

### 인과 음성 대조군과 마커-shuffle 검정

ATAC를 lineage 내에서 뒤섞어 chromatin과 RNA의 결합을 끊고 모델을 다시 fitting했다. 시간차(lag) 분포를 원본과 Mann–Whitney, Kolmogorov–Smirnov, 짝지은 Wilcoxon 검정과 유전자별 Spearman ρ로 비교했으며, MultiVelo와 MoFlow에 대해 독립적으로 수행했다. 명명된 priming 마커의 cross-method 일치가 그 locus의 chromatin에 의해 생기는지를 검정하기 위해, shuffle이 유발한 명명된 마커 시간차의 변화를 나머지와 편향 보정 상대 변화 척도에서 비교했다(|Δlag|/|lag_original|, |Δlag|가 시간차 크기와 상관하므로, ρ=+0.24), Mann–Whitney(마커 > 나머지)로. 이 검정은 귀무였고(마커 중앙값 0.137 대 나머지 0.144, p=0.58), 따라서 마커 방향 일치는 인과가 아니라 상관으로 보고한다.

### 외부 속도 검증

fitting된 α와 γ를 측정된 속도와 비교했다(순위 기반, cross-context, 유전자별 부트스트랩 95% CI, B=10⁴). α는 측정된 K562 TT-seq 합성 속도(GSE229305, Todorovski 2024; 그리고 두 번째 출처 Schwalb 2016 K562 TT-seq, GSE75792)와, γ는 측정된 mRNA 반감기(K562/THP1 동일 연구 SLAM-seq, MOLM13 교차 연구)와 비교했다. housekeeping 층은 자명하게 보존되므로 헤드라인은 비-housekeeping 층이다. 분해 복원 방향은 ρ(γ, k_deg)로 채점했다(k_deg = ln2/t½; 복원 = 양수). α 귀무의 해석은 비대칭적이고 사전등록되어 있다. cross-context 측정과 절대-α 비식별성을 감안하면 귀무는 격하할 뿐 반증하지 않는다. 근접 맥락의 조혈 참조에서 나온 γ 귀무 또는 반전은 정보가 있는 비복원으로 읽는다. α anchor에는 abundance 교란이 적용된다. α와 측정된 TT-seq 합성 속도 둘 다 transcript abundance를 따라갈 수 있으므로(s_ss = α/γ) 양의 순위 상관은 일부가 abundance 공변량일 수 있다. 비-housekeeping 층으로 제한하면 이를 부분적으로 완화하고 생물물리가 그 상관을 예측하지만, 순위-방향 검정만으로는 α가 abundance가 아니라 합성 kinetics를 포착하는지를 확정하지 못한다.

### 프로파일 우도 식별가능성과 외부 검증과의 정렬

MultiVelo의 목적(우도)을 α 축과 시간차 축(lag = t_sw2 − t_sw1)을 따라 프로파일링했고, 각 스캔 점에서 latent time을 재최적화했다(n=538 유전자; fitting/우도 재현 r≈1.0). 두 nuisance regime을 돌렸다. **nuisance 고정(fixed-nuisance)**(β, γ, α_c, rescale, scale_cc 고정)은 상한 곡률비를 주고, **nuisance 해방(freed-nuisance)**(이들을 재최적화)은 본문에 보고한 보수적 하한을 준다(2.49×). 유전자별 강성은 곡률비 κ_α/κ_lag로 요약했다. 내부/경계 고정/퇴화 분류는 데이터가 시간차를 경계 지을 수 있는지를 기술한다. 내부 강성이 (모수 순위만이 아니라) *외부* 검증을 예측하는지를 검정하기 위해, 프로파일 강성을 모든 속도로 확장하고(`stiffness_all_params`) α 유전자를 강성 삼분위로 나눠 측정된 합성 속도에 대한 모수 내부·유전자 간 검정을 수행했다. 이 검정은 검정력이 부족했고(최상위 삼분위 ρ=+0.302 [+0.068, +0.511]은 0을 넘지만 상위-하위 Δρ=+0.186 [−0.149, +0.504]은 넘지 못하며, 삼분위당 n=70) γ 축은 경사가 없었으므로, 식별가능성과 외부 검증의 연결은 헤드라인 결과가 아니라 시사적 보조 증거로만 보고한다.

### 사전등록 프로토콜

다섯 번째 외부 재현(마우스 gastrulation, GSE205117)에 대해, 사전 선언한 임계를 가진 여섯 개의 반증 가능한 예측을 어떤 velocity fitting이나 일치도가 존재하기 전에 commit 해시로 봉인했다(`PREREGISTRATION_gse205117.md`; dataset 내부 α ρ≥0.50은 15번째 줄, 시간차 ρ≤0.15, α에서 시간차를 뺀 간격 ≥0.35, cross-dataset α>+0.2 및 >cross-lag, 유전자별 시간차 불일치 > α 불일치, 최대 priming 하 취약성). 임계 ρ≥0.50이 봉인된 합격선이며, 관측된 HSPC α=0.88은 합격선이 아니라 관측값이다. 채점은 봉인된 원 유전자별 정의(시간차 예측에는 MultiVelo 대 MoFlow)를 사후 구제 없이 적용했고, 채점표는 결정론적 재계산에서 바이트 단위로 동일하게 재현되었다.

### 교란 통제

cell-cycle, 전사 버스트(transcriptional burst), ambient/doublet 교란(confound)을 통제했다. cell-cycle은 유전자 수준에서 편향이 없었다(cell-cycle 유전자는 fit-lag 유전자의 1.9%; CC 대 나머지 Mann–Whitney p=0.86; 제외 시 중앙값 변화 0.037). 세포 수준 상관은 세포주기가 lineage에 결합되어 있어서 생기며(MK 88% 대 HSC 3%), 이는 within-lineage 분석이 이미 통제하므로, (분화 신호를 제거하지 않기 위해) 전역 regress-out은 하지 않았다. 버스트: 시간차 대 α Spearman −0.24(중간 정도, regularized 회귀에 반영). Ambient/doublet: scrublet 적용, doublet 중앙값 0.045, pct_mito 중앙값 10.4%(QC 최대 20%). 분석은 within-lineage였고, 희귀 lineage(MK/Baso·Eo·Mast/pDC)는 별도 불확실성으로 다뤘다. promoter/enhancer ATAC feature의 다중공선성(multicollinearity)은 regularized 회귀로 처리했고, 유전자에 걸친 다중 검정에는 순열 FDR을 썼다.

### 데이터셋 및 코드 가용성

외부 데이터셋 재고(accession, 종/조직, 세포 수, 플랫폼, 역할)는 Supplementary Table S2로 제공한다. 분석 코드와 결정론적 재계산 스크립트(`p3_concordance.py`, `p3_crossdataset_concordance.py`, `p3_scrambled_null.py`, `external_rate_validation.py`, `p5_stiffness_all_params.py`, `p6_curvature_tertile_validation.py`)는 `<FILL: repository/DOI + license>`에 보관한다.

---

## Declarations

**연구윤리 승인 및 참여 동의.** 해당 없음. 이 연구는 이미 출판된 비식별 공개 데이터셋을 사용한다.

**출판 동의.** 해당 없음.

**데이터 및 자료 가용성.** 모든 일차·외부 데이터셋은 공개다(GSE209878, GSE194122, GSE284047, GSE205117, GSE229305, GSE75792, GSE162170; E18 마우스 뇌는 10x Genomics "Fresh Embryonic E18 Mouse Brain 5k" 데모 데이터셋으로 GEO accession이 없다). 분석 코드와 결정론적 재계산 스크립트: `<FILL: repository/DOI + license>`.

**이해 상충.** `<FILL>`.

**연구비.** `<FILL>`.

**저자 기여.** `<FILL>`.

**감사의 글.** `<FILL>`.

**면책.** 연구·교육용 초안이며 임상·진단 자원이 아니다.

---

## Figures (캡션과 배치 계획; 이 초안에서 그림은 렌더링하지 않음)

**Fig. 1.** HSPC에서 유전자별 시간차(lag)와 전사 속도 α의 cross-method 일치도. 시간차 크기 쌍별 산점/순위 행렬(대부분의 쌍 |ρ|≤0.08, 가장 강한 쌍 +0.163)과 부호 일치(48%)를 α 재현성 산점(ρ=0.88)과 대비. `figures/fig01_p2_concordance.png`. *배치: Results 서두.*

**Fig. 2 (main; supplementary에서 승격).** 인과 음성 대조군. lineage 내 ATAC shuffle이 MultiVelo 시간차 분포를 통계적으로 바꾸지 않음(Mann–Whitney p=0.20; 유전자별 ρ=0.72), MoFlow에서 재현(ρ=0.52); 삽입도: 명명된 마커 shuffle 검정 귀무(마커 대 나머지 상대 변화, p=0.58). `figures/fig_atac_shuffle_causal.png`. *배치: 인과 대조군 소절.*

**Fig. 3.** 여섯 개 시스템에 걸친 cross-dataset 재현. 시스템별 짝지은 α(cross-method 중앙값) 대 시간차 막대와 HSPC-대-외부 순위 ρ, 사전등록 gastrulation 6/0 채점표. `figures/fig02_crossdataset_concordance.png`. *배치: 재현 소절.*

**Fig. 4.** 외부 측정 anchor. fitting된 α 대 측정된 K562 TT-seq 합성 속도(세 방법, 비-HK ρ +0.24 ~ +0.29, CI가 0 배제)와 fitting된 γ 대 측정된 반감기(K562 3/3 귀무; scVelo γ 반전, −0.224). `figures/fig_external_rate_anchor.png`. *배치: 외부 anchor 소절.*

**Fig. 5.** 프로파일 우도 분리. α 축 대 시간차 축의 MultiVelo 우도 곡률(freed-nuisance κ_α/κ_lag=2.49×, 유전자의 77%에서 α가 더 stiff)과 시간차 삼분류(56% 내부 / 38% 경계 고정 / 6% 퇴화). `figures/fig05_profile_likelihood.png`. *배치: 기제 소절.*

**Fig. 6.** 합성 양성 대조군. switch-sharpness × SNR 격자에 걸친 두 방법 시간차 일치도; 식별가능성 코너에서의 일치(ρ=+0.454)가 SNR이 떨어지며 붕괴, HSPC 검정력 보정 하한 표시. `figures/fig_sim_positive_control.png`. *배치: 양성 대조군 소절.*

**Fig. 7 (main; 신규).** 측정 앵커 신뢰도 heatmap. velocity 출력(행) 대 축(열: cross-method 재현 / chromatin-인과 / baseline-예측 / 측정-anchoring), Table 2 결정 지도의 시각 형태. `figures/fig_reliability_heatmap.png`. *배치: 종합 소절(Results 마무리).*

**Fig. 8.** 선행 velocity 벤치마크·방법 논문 대비 새로움 비교(순열 귀무, 인과 대조군, 외부 측정 anchor를 선점되지 않은 축으로). `figures/fig03_novelty_comparison.png`. *배치: Discussion.*

---

## References

[1] Li C, Virgilio MC, Collins KL, Welch JD. Multi-omic single-cell velocity models epigenome–transcriptome interactions and improves cell fate prediction. *Nature Biotechnology* 41, 387–398 (2023). doi:10.1038/s41587-022-01476-y.

[2] Li C, Gu Y, Virgilio MC, Lee KH, Collins KL, Welch JD. Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE. *Nature Communications* 16, 11505 (2025). doi:10.1038/s41467-025-66287-6.

[3] Hong A, Lee S, Kim K. Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states. *Nature Communications* 17, 566 (2025). doi:10.1038/s41467-025-67259-6.

[4] El Kazwini N, Gao M, Kouadri Boudjelthia I, Cai F, Huang Y, Sanguinetti G. CRAK-Velo: chromatin accessibility kinetics integration improves RNA velocity estimation. *Genome Biology* 27(1) (2026). doi:10.1186/s13059-026-04086-y.

[5] ArchVelo: archetypal velocity modeling for single-cell multi-omic trajectories. *Nature Communications* (2026). doi:10.1038/s41467-026-74000-4. [Author list to verify before submission.]

[6] Su M, et al. scKINETICS: inference of regulatory velocity with single-cell transcriptomics data. *Bioinformatics* 39(Suppl 1), i394–i403 (2023).

[7] Gayoso A, Weiler P, Lotfollahi M, et al. Deep generative modeling of transcriptional dynamics for RNA velocity analysis in single cells. *Nature Methods* 21, 50–59 (2024). doi:10.1038/s41592-023-01994-w.

[8] Gu Y, et al. Bayesian inference of RNA velocity incorporating timepoints, lineage bifurcations, and count data (veloVAE). *PLOS Computational Biology* 22(3), e1014060 (2026). doi:10.1371/journal.pcbi.1014060. [Distinct from MultiVeloVAE [2].]

[9] Bergen V, Soldatov RA, Kharchenko PV, Theis FJ. RNA velocity — current challenges and future perspectives. *Molecular Systems Biology* 17(8), e10282 (2021). doi:10.15252/msb.202110282.

[10] Gorin G, Fang M, Chari T, Pachter L. RNA velocity unraveled. *PLOS Computational Biology* 18(9), e1010492 (2022). doi:10.1371/journal.pcbi.1010492.

[11] Marot-Lassauzaie V, Bouman BJ, Donaghy FD, Demerdash Y, Essers MAG, Haghverdi L. Towards reliable quantification of cell state velocities. *PLOS Computational Biology* 18(9), e1010031 (2022). doi:10.1371/journal.pcbi.1010031.

[12] Benchmarking RNA velocity methods across 17 independent studies. *Cell Reports Methods* (2026), S2667-2375(26)00067-6. bioRxiv 2025.08.02.668272. [Author list/DOI to confirm at proof.]

[13] Benchmarking algorithms for RNA velocity inference. bioRxiv 2026.01.03.697314 (2026). [Preprint; author list/venue to confirm.]

[14] Ma S, Zhang B, LaFave LM, et al. Chromatin Potential Identified by Shared Single-Cell Profiling of RNA and Chromatin. *Cell* 183(4), 1103–1116.e20 (2020). doi:10.1016/j.cell.2020.09.056.

[15] Trevino AE, Müller F, Andersen J, et al. Chromatin and gene-regulatory dynamics of the developing human cerebral cortex at single-cell resolution. *Cell* 184(19), 5053–5069.e23 (2021). doi:10.1016/j.cell.2021.07.039. (GSE162170.)

[16] Zhang et al. Quantifying uncertainty in RNA velocity (ConsensusVelo). bioRxiv 2024.05.14.594102 (2024); *Biometrics* 82(1) ujag018 (in press). doi:10.1101/2024.05.14.594102. [Closest prior art to the profile-likelihood section; cited head-on. Full author list/final venue to confirm.]

[17] Gu et al. Profile-likelihood identifiability analysis of single-cell transcription (telegraph) kinetics. *Bioinformatics* 41(11), btaf581 (2025). doi:10.1093/bioinformatics/btaf581. [Distinct from [8].]

[18] Wang. Sloppiness and Action Constraint in Cell State Transitions: Are Single Cells Sloppy? bioRxiv 2025.12.31.697145 (v2, 2025). [Methodological analog on cell-state Gaussian coordinates.]

[19] BayVel: A Bayesian Framework for RNA Velocity Estimation in Single-Cell Transcriptomics. arXiv:2505.03083 (2025). [Preprint; author list to confirm.]

---

*Bibliography exported to `manuscript/refs.bib`. Reference count (19) is below the Genome Biology benchmark norm (≈50–85); expanding it is a submission-prep task tracked separately in `GB_BENCHMARK.md` (G3) and is not undertaken here to avoid fabricating citations. Items with "to confirm/verify" notes carry over the flags from `related_work.md`.*
