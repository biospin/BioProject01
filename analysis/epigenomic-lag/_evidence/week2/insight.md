# Insight

## 1. Executive Signal

- 가장 중요한 cross-paper insight: `epigenomic-lag` field는 MultiVelo의 **interpretable ODE/discrete state**에서 출발해, 두 방향으로 갈라졌다. 하나는 MultiVeloVAE의 **probabilistic multi-sample inference**, 다른 하나는 MoFlow의 **latent time-free local relay velocity**이다. 새로 추가한 cellDancer/DeepVelo/DeepKINET/mmVelo는 각각 relay velocity 계보, cell-specific kinetics 배경, kinetic validation, peak-resolved chromatin velocity gap을 보강한다.
- 왜 지금 중요한가: 두 후속 method가 같은 MultiVelo 한계를 겨냥하지만 철학이 다르다. 우리 목적이 "gene별 lag -> drug response timing"이면 MoFlow의 lag quantification과 MultiVeloVAE의 differential test를 둘 다 써서 cross-validation하는 전략이 가장 안전하다.
- 우리 topic과의 연결: MultiVelo는 baseline, MultiVeloVAE는 multi-sample/differential testing layer, MoFlow는 direct lag scoring layer로 역할을 나눌 수 있다.

## 2. Field Flow

- 선행 흐름:
  - `li-2023-multivelo`: RNA velocity의 constant transcription rate assumption을 깨고 $du/dt = \alpha c(t) - \beta u$ 형태로 chromatin accessibility를 transcription rate에 연결했다.
  - `li-2025-multivelovae`: MultiVelo의 discrete state와 single-sample 한계를 VAE, continuous $k_c/\rho$, $\delta/\kappa$, cVAE batch conditioning, Bayesian differential test로 확장했다.
  - `hong-2026-moflow`: MultiVelo의 gene-specific latent time과 fixed gene label 자체를 회피하고, local neighbor displacement 기반 relay velocity로 cell-specific kinetics를 학습했다.
- method / assay / dataset이 어떻게 바뀌는가:
  - MultiVelo: paired multiome에서 interpretable ODE state를 얻는 데 강함.
  - MultiVeloVAE: multi-sample, RNA-only mixed mode, perturbation simulation, statistical testing으로 분석 scope가 넓어짐.
  - MoFlow: reused benchmark 중심이지만 DTW c-s lag, DAC, m1/m2 같은 direct lag-oriented output이 우리 주제에 가장 직관적으로 맞음.
- 어떤 문제가 반복적으로 다음 paper를 유도했는가:
  - MultiVelo의 discrete/global assumptions -> MultiVeloVAE continuous cell-specific factors.
  - MultiVelo의 latent time over-correction 가능성 -> MoFlow latent time-free relay velocity.
  - single-sample method limitation -> MultiVeloVAE multi-sample cVAE.
  - association-heavy biological interpretation -> 세 paper 모두 perturbation/ground-truth validation 필요.

## 3. Differentiation Map

| paper | 무엇이 다른가 | 강점 | 약점 | evidence |
|---|---|---|---|---|
| `li-2023-multivelo` | chromatin $c(t)$를 ODE transcription rate에 직접 결합 | 가장 해석 가능한 foundational model, priming/decoupling 개념 정립 | discrete state, gene-level c, causal validation 부족, multi-lineage 한계 | `evidence_bundle.md` `li-2023-multivelo` |
| `li-2025-multivelovae` | cVAE + continuous $\delta/\kappa$ + Bayesian differential test | multi-sample/differential test/perturbation/mixed modality 지원 | hyperparameter/FDR/perturbation validation 부족, de novo training | `evidence_bundle.md` `li-2025-multivelovae` |
| `hong-2026-moflow` | latent time 없이 relay velocity와 cell-specific kinetic 학습 | direct lag analysis, CBDir 성능, MultiVelo over-correction 문제 제기 | multi-sample/differential test/uncertainty 없음, ablation 부족 | `evidence_bundle.md` `hong-2026-moflow` |
| `li-2023-celldancer` | RNA-only relay velocity, latent time-free local neighbor cosine loss | MoFlow의 *직접 predecessor*, gene별 DNN + cosine similarity max over local neighbor 철학 제공 | chromatin 없음, 정성 평가 위주 (CBDir 같은 metric 부재) | `evidence_bundle.md` `li-2023-celldancer` (full-analysis 승급) |
| `nomura-2024-mmvelo` | mixture-of-experts VAE + decoder-level peak resolution chromatin velocity | gene-level c aggregation 한계를 *decoder branch level*에서 부분 보완. SHARE-seq에서 MultiVelo 직접 benchmark (Fig S3j-m). | preprint, per-peak ODE rate 없음 (공통 latent transition $d_n$ 공유) | `evidence_bundle.md` `nomura-2024-mmvelo` (full-analysis 승급, preprint-tier) |
| `cui-2024-deepvelo` | RNA-only GCN + continuity loss + cell-specific kinetics | cell-specific kinetics rationale의 RNA-only predecessor (MultiVeloVAE 배경) | chromatin 없음, *continuity score는 confidence proxy*일 뿐 posterior uncertainty 없음 | `evidence_bundle.md` `cui-2024-deepvelo` (full-analysis 승급) |
| `mizukoshi-2024-deepkinet` | 2-stage VAE + cell-specific splicing/degradation rate decoders + metabolic labeling validation | *evaluation framework* (2-stage decoupling, 100-repeat box-plot, negative correlation fail rule, cluster-level simulation benchmark)가 transferable | chromatin 없음, labeling 자체는 transfer 불가 (single-cell chromatin labeling 표준 부재) | `evidence_bundle.md` `mizukoshi-2024-deepkinet` (full-analysis 승급) |

## 4. Repeated Limitations

- 반복 한계 1: gene-level chromatin aggregation
  - 해당 paper: `li-2023-multivelo`, `li-2025-multivelovae`, `hong-2026-moflow`
  - 근거: MultiVelo와 MultiVeloVAE는 single c per gene 또는 individual cis-regulatory element 직접 modeling 부재가 한계로 정리됨. MoFlow도 long-range enhancer-promoter interaction과 motif-level regulation 직접 modeling 부재를 저자가 명시.
  - 왜 중요한가: drug response timing 예측에서 실제 target locus가 promoter인지 enhancer인지 구분하지 못하면 perturbation/assay 설계로 연결하기 어렵다.

- 반복 한계 2: causal validation 부족
  - 해당 paper: `li-2023-multivelo`, `li-2025-multivelovae`, `hong-2026-moflow`
  - 근거: MultiVelo의 TF lag는 association으로 명시됨. MultiVeloVAE perturbation은 in silico와 known biology consistency 중심. MoFlow의 negative lag mechanism은 external half-life/nuclear localization reference와의 association 중심.
  - 왜 중요한가: lag estimate를 regulatory mechanism 또는 drug response timing predictor로 쓰려면 perturbation 또는 time-stamped ground truth가 필요하다.

- 반복 한계 3: benchmark metric 통일 부재
  - 해당 paper: `li-2023-multivelo`, `li-2025-multivelovae`, `hong-2026-moflow`
  - 근거: MultiVelo는 일부 dataset에서 Spearman/정성 backflow 중심, MultiVeloVAE는 GCBDir 등 다축 metric, MoFlow는 CBDir 중심.
  - 왜 중요한가: 우리 pipeline에서 어떤 method를 primary로 쓸지 결정하려면 같은 input과 같은 metric으로 head-to-head가 필요하다.

## 5. Unresolved Gaps

- gap: MultiVeloVAE와 MoFlow의 head-to-head가 없다.
  - 현재 evidence: 두 paper 모두 MultiVelo와 비교하지만 서로 직접 비교하지 않는다.
  - 부족한 evidence: 같은 HSPC/mouse brain/mouse skin input에서 CBDir, GCBDir, runtime, memory, lag score concordance.
  - 검증 가능한 질문: MoFlow의 high CBDir gene/cell이 MultiVeloVAE의 high $|\delta|$ 또는 high $\kappa$ region과 일치하는가?

- gap: direct lag score와 statistical differential test가 분리되어 있다.
  - 현재 evidence: MoFlow는 DTW c-s lag, m1/m2, DAC가 강하지만 differential test가 약함. MultiVeloVAE는 Bayesian test가 강하지만 lag-specific biological score는 MoFlow만큼 직접적이지 않음.
  - 부족한 evidence: MoFlow-derived lag groups를 MultiVeloVAE differential test로 재검정하는 hybrid workflow.
  - 검증 가능한 질문: MoFlow negative c-s lag genes가 MultiVeloVAE의 cell-type/time differential $\delta$ gene으로도 잡히는가?

- gap: enhancer-resolved lag modeling이 없다.
  - 현재 evidence: 세 paper 모두 gene-level c aggregation 한계가 반복됨.
  - 부족한 evidence: promoter/enhancer peak별 lag, peak-gene linkage confidence, perturbation targetability.
  - 검증 가능한 질문: gene-level lag가 같은 gene에서도 promoter peak와 distal enhancer peak에 따라 다른 sign/duration을 보이는가?

## 6. Follow-up Research Directions

- 방향 1: HSPC method head-to-head benchmark
  - 가설: MultiVeloVAE와 MoFlow가 모두 high-confidence로 잡는 gene은 robust epigenomic-lag candidate이고, disagree gene은 method-assumption-sensitive candidate이다.
  - 필요한 dataset / assay: Human HSPC 10x Multiome GSE209878 또는 우리 내부 HSPC multiome.
  - 분석 방법: MultiVelo, MultiVeloVAE, MoFlow를 같은 preprocessed input에 실행. CBDir/GCBDir/runtime/memory/score concordance 측정.
  - 성공 기준: method agreement gene set과 disagreement gene set이 구분되고, agreement set에서 known lineage marker 또는 epigenetic regulator enrichment가 높음.
  - 관련 paper: `li-2023-multivelo`, `li-2025-multivelovae`, `hong-2026-moflow`

- 방향 2: MoFlow lag group + MultiVeloVAE differential test hybrid
  - 가설: MoFlow의 negative c-s lag 또는 high DAC group은 MultiVeloVAE Bayesian differential dynamics에서도 유의한 driver로 검출된다.
  - 필요한 dataset / assay: multi-lineage HSPC 또는 brain multiome.
  - 분석 방법: MoFlow로 c-s lag group 분류 -> MultiVeloVAE로 해당 gene의 $\delta/\kappa$ differential test -> concordance table.
  - 성공 기준: MoFlow group별 MultiVeloVAE Bayes factor/FDR 분포가 유의하게 다름.
  - 관련 paper: `li-2025-multivelovae`, `hong-2026-moflow`

- 방향 3: enhancer-resolved epigenomic lag pilot
  - 가설: gene-level c aggregation은 enhancer-specific lag sign을 평균내어 숨긴다.
  - 필요한 dataset / assay: peak-level ATAC + gene expression paired multiome, peak-gene linkage.
  - 분석 방법: 기존 gene-level c 대신 promoter/distal enhancer peak group별 c(t) 또는 c-score를 만들고 lag sign/duration을 비교.
  - 성공 기준: gene-level lag와 peak-level lag가 불일치하는 high-value genes를 식별.
  - 관련 paper: 세 paper 모두의 repeated limitation.

## 7. Practical Actions

- 지금 할 일:
  - `papers.jsonl`, `evidence_bundle.md`, `insight.md`, `validation_report.md`를 OpenClaw Week2 demo input/output으로 사용.
  - MoFlow GitHub license 확인.
  - mmVelo PDF/code/license 확인.
  - 같은 HSPC input에서 MoFlow vs MultiVeloVAE 비교를 위한 실행 환경 요구사항 정리.
- 다음 분기:
  - HSPC head-to-head benchmark 수행.
  - MoFlow lag group과 MultiVeloVAE $\delta/\kappa$ concordance 계산.
  - source data xlsx에서 MultiVeloVAE exact benchmark matrix와 MoFlow supplementary gene lists 추출.
- 장기:
  - enhancer-resolved lag model 설계.
  - perturbation 또는 time-stamped multiome validation dataset 확보.

## 8. Claims for Validation

| claim_id | insight claim | evidence papers | evidence strength | validation focus |
|---|---|---|---|---|
| C1 | Field는 MultiVelo baseline에서 MultiVeloVAE probabilistic multi-sample branch와 MoFlow latent time-free relay branch로 갈라졌다. | `li-2023-multivelo`, `li-2025-multivelovae`, `hong-2026-moflow` | strong | 세 method의 stated limitations/claimed extensions가 이 구조를 지지하는지 |
| C2 | 우리 use case에는 MoFlow를 lag quantification primary, MultiVeloVAE를 multi-sample/differential test secondary로 쓰는 cross-validation 전략이 적합하다. | `li-2025-multivelovae`, `hong-2026-moflow` | moderate | "적합"은 분석자 판단이므로 과장되지 않았는지 |
| C3 | 세 paper 모두 enhancer/promoter-specific kinetics를 직접 모델링하지 못하는 gene-level c aggregation 한계가 있다. | all three | strong | 각 paper에서 실제로 해당 한계가 명시/도출되는지 |
| C4 | causal validation 부족은 세 paper 공통의 bottleneck이다. | all three | strong | association과 causality 구분이 충분한지 |
| C5 | MultiVeloVAE와 MoFlow의 direct head-to-head가 다음 우선순위 높은 실험/분석이다. | `li-2025-multivelovae`, `hong-2026-moflow` | moderate | 실험이 아니라 computational benchmark임을 명확히 해야 함 |
| C6 | MoFlow lag group을 MultiVeloVAE differential test로 재검정하는 hybrid workflow가 유망하다. | `li-2025-multivelovae`, `hong-2026-moflow` | weak | 실제 compatibility는 아직 미검증이므로 follow-up idea로 제한 |
| C7 | mmVelo는 *decoder-level peak resolution*으로 single-peak chromatin velocity를 정의해 gene-level c aggregation gap을 *부분적으로* 메우는 후보이다. PDF로 mechanism과 MultiVelo 직접 benchmark가 supported; per-peak ODE rate는 *없음* (공통 latent transition $d_n$ + peak-specific decoder branch $f_p^a$). | `nomura-2024-mmvelo` | moderate-strong (preprint-tier) | PDF 정밀 패스 통과. `검토필요:` preprint 출간 모니터링 (bioRxiv v1 2024-12-17), GitHub repo `nomuhyooon/mmVelo` license 확인. |
| C8 | DeepKINET은 *kinetic-rate validation framework* (2-stage decoupling + 100-repeat box-plot + negative correlation fail rule + cluster-level simulation benchmark)를 제공해 epigenomic-lag validation 설계에 *framework 수준에서* 참고할 수 있다. *Labeling data 자체* (scEU-seq/scNT-seq RNA labeling, Dynamo proxy)는 chromatin lag validation으로 *직접 전이 불가* — single-cell chromatin labeling 표준 부재 + Dynamo 차용 시 circular validation 위험. | `mizukoshi-2024-deepkinet` | moderate (framework borrow), low (labeling) | concrete 4-bullet transferability map (✅ 2-stage decoupling + 100-repeat / ⚠️ chromatin-aware simulator 재설계 / ❌ scEU-seq labeling / ❌ Dynamo proxy) 기반으로 사용. |
