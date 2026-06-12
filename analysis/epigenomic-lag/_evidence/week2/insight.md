# Insight

## 1. Executive Signal

- 가장 중요한 cross-paper insight: `epigenomic-lag` field는 MultiVelo의 **interpretable ODE/discrete state**에서 출발해, 두 방향으로 갈라졌다. 하나는 MultiVeloVAE의 **probabilistic multi-sample inference**, 다른 하나는 MoFlow의 **latent time-free local relay velocity**이다. 새로 추가한 cellDancer/DeepVelo/DeepKINET/mmVelo는 각각 relay velocity 계보, cell-specific kinetics 배경, kinetic validation, peak-resolved chromatin velocity gap을 보강한다.
- 왜 지금 중요한가: 두 후속 method가 같은 MultiVelo 한계를 겨냥하지만 철학이 다르다. 우리 목적이 "gene별 lag -> drug response timing"이면 MoFlow의 lag quantification과 MultiVeloVAE의 differential test를 둘 다 써서 cross-validation하는 전략이 가장 안전하다.
- 우리 topic과의 연결: MultiVelo는 baseline, MultiVeloVAE는 multi-sample/differential testing layer, MoFlow는 direct lag scoring layer로 역할을 나눌 수 있다.
- `해석:` (2026-06-12 full-analysis 승격된 4편이 더하는 것) 세 가지 축에서 기존 그림을 *보강*하되 핵심 방향(C1–C5)은 *바꾸지 않는다*. 네 편 모두 PDF 확보·분석 완료로 정량 비교가 이제 가능하다. (a) CRAK-Velo(`@elkazwini2026crakvelo`)는 UniTVelo 확장 semi-mechanistic chromatin-aware velocity로, **동일 GSE209878 HSPC에서 MultiVelo와 직접 비교**(동일 데이터·annotation)해 MultiVelo 대비 단순·빠르고(run-time 15h vs >24h) terminal state·deconvolution 우위 — 우리 head-to-head의 가장 직접적인 진입점. 단 chromatin–transcription "lag"를 명시 parameter로 출력하지 않아 region kinetic을 lag로 후처리해야 함. (b) Luo benchmark(`@luo2026velocitybenchmark`)는 "전 항목 우월 method 없음"을 17 real + 3 simulation으로 정량 입증해 C2/C5 전략에 외부 근거를 더하되, **우리 HSPC가 Dataset12로 쓰였지만 MultiVelo는 `rna_only=True`(ATAC 비활성)로만 평가**되어 우리에게 핵심인 multi-omic 성능은 미측정. (c) Safi(`@safi2022chromatinpriming`)·Martin(`@martin2023hspcchromatin`, review→primary 정정)은 chromatin priming 선행을 같은 HSPC 축에서 생물학적으로 뒷받침하나, 둘 다 paired RNA/시간 단위 lag를 정량하지 않아 *배경·plausibility*에 머문다.

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
| `el-kazwini-2026-crakvelo` | UniTVelo 확장 — chromatin을 transcription rate production term으로 직접 구성 + gene별 region weight $w_r^g$ | **동일 GSE209878 HSPC에서 MultiVelo 직접 비교** 우위(terminal state·deconvolution), 단순·빠름(15h vs >24h), region–gene interaction 해석 layer | lag를 명시 parameter로 출력 안 함; 공식 ablation·통계 검정 없음; HCC region-level 불안정; Article in Press 표기 불일치 | `evidence_bundle.md` `el-kazwini-2026-crakvelo` (full-analysis) |
| `luo-2026-velocity-benchmark` | 15 method × (17 real + 3 simulation) 벤치마크 (accuracy·stability·usability) | 단일 best method 부재를 정량 입증(veloVI 0.23 최고, 평균 ≈0.1); 우리 HSPC = Dataset12 직접 포함 | **MultiVelo가 `rna_only=True`로 평가 → multi-omic 강점 미측정**; HSPC 단독 순위 수치 본문에 없음 | `evidence_bundle.md` `luo-2026-velocity-benchmark` (full-analysis) |
| `safi-2022-chromatin-priming` | mouse LSK scATAC-seq의 concurrent stem/lineage priming (CD9high transition 집단) | activation lag 가설을 *같은 HSPC*에서 chromatin-side로 지지 (commitment 선행), prospectively isolable marker | **paired multiome 아님**(scATAC↔scRNA projection) + transition 축 pseudotime → lag 정량 안 함; mouse(cross-species); GSE accession 불일치·2023 erratum | `evidence_bundle.md` `safi-2022-chromatin-priming` (full-analysis) |
| `martin-2023-hspc-chromatin` | mouse 13 cell type bulk ATAC-seq dynamics + CRISPRi CRE 인과 검증 (**primary article**, review 오기 정정) | priming CRE가 commitment 전부터 accessible(<25%만 유지) — 선행성 배경 + accessibility→expression CRISPRi 인과 | **paired RNA 없음**(외부 GEXC) + bulk → 시간 lag 정량 불가; CRISPRi 인과 3 locus 한정; mouse | `evidence_bundle.md` `martin-2023-hspc-chromatin` (full-analysis) |

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

## 5b. Full-analysis 승격 4편이 기존 insight에 더하거나 바꾸는 것

`해석:` 아래 4편은 2026-06-12에 **full-analysis로 승격**(PDF + core/lens/methodology-brief 완료)됐다. 정량 비교가 이제 가능하나, 핵심 방향(C1–C5)은 *바꾸지 않고 보강*한다.

- (a) **CRAK-Velo — 같은 GSE209878 HSPC에서 MultiVelo 직접 대체 후보** (`@elkazwini2026crakvelo`)
  - 확정: UniTVelo를 chromatin-aware로 확장한 semi-mechanistic model. **우리 데이터(GSE209878)에서 MultiVelo와 동일 셋업으로 직접 head-to-head**해 platelet terminal state·deconvolution 우위, run-time 15h vs MultiVelo >24h로 단순·빠름. 우리 head-to-head 후보 목록(Field Flow / Direction 1)에 즉시 들어오며, MultiVelo 1순위 대체 baseline 후보다.
  - 바꾸지 않는 것: **chromatin–transcription lag를 명시 parameter로 출력하지 않는다**(region kinetic plot의 지연은 pseudotime 축 시각화). 따라서 MoFlow의 direct lag layer 역할을 대체하지 않고, region kinetic의 accessibility-peak↔unspliced-peak pseudotime 차이를 lag로 *후처리*해야 한다. 공식 ablation 부재라 chromatin 통합의 인과 기여는 미분리.

- (b) **Luo benchmark → 우리 HSPC가 Dataset12, 단 MultiVelo는 RNA-only로 평가** (`@luo2026velocitybenchmark`)
  - 확정: 15 method × (17 real + 3 simulation)에서 "no single method superior"를 정량 입증(veloVI 0.23 최고, 평균 ≈0.1). **우리 HSPC(GSE209878)가 Dataset12로 직접 사용**됐으므로 C2/C5(데이터 기반 method 선택)에 직접 적용 가능한 근거.
  - 바꾸는 것(중요 caveat): 이 benchmark에서 **MultiVelo는 `rna_only=True`(ATAC 비활성)로만 평가**됐다. 즉 우리에게 정작 필요한 multi-omic(chromatin) 모드의 정확도·안정성은 측정되지 않았다. RNA-only 순위·scenario 권고는 차용하되, multi-omic velocity 선택(MultiVelo/MultiVeloVAE/MoFlow/CRAK-Velo)은 우리 자체 검증으로 정해야 한다(권고안 직접 인용 금지).

- (c) **Safi·Martin이 activation lag 가설을 같은 HSPC 시스템에서 생물학적으로 뒷받침** (`@safi2022chromatinpriming`, `@martin2023hspcchromatin`)
  - 확정: Safi는 commitment에 앞서 stem/lineage chromatin program을 동시 보유하는 CD9high transition 집단을, Martin(review→**primary article 정정**)은 HSC-primed CRE가 commitment 전부터 accessible(<25%만 유지) + CRISPRi로 accessibility→expression 인과를 보여, "chromatin priming이 transcription/commitment에 선행"한다는 *정성적 선행성*을 HSPC 축에서 지지한다.
  - 바꾸지 않는 것: **Safi는 paired multiome이 아니라 scATAC 단독 + pseudotime**(scRNA는 다른 batch projection), Martin은 paired RNA 없이 외부 GEXC + bulk다. 따라서 gene별 lag *정량의 직접 근거가 아니라 배경·plausibility*로 위치한다. 둘 다 mouse라 human HSPC cross-species 일반화는 선결 과제. `검토필요:` Safi GSE accession 불일치(GSE173075/76 vs GSE148746)·2023 erratum.

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
  - (완료 2026-06-12) CRAK-Velo·Luo benchmark·Safi 2022·Martin 2023 full-analysis 승격 완료. 후속: CRAK-Velo Article-in-Press 최종본 교정 모니터링, Luo Dataset12(HSPC) 단독 method 순위를 mmc1/mmc2에서 추출, Safi GEO accession(GSE173075/76 vs GSE148746) GEO에서 확정.
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
| C9 | CRAK-Velo(UniTVelo 확장 semi-mechanistic)는 **동일 GSE209878 HSPC에서 MultiVelo와 직접 비교**해 단순·빠르고(15h vs >24h) terminal state·deconvolution 우위 — 우리 HSPC head-to-head의 MultiVelo 1순위 대체 baseline. 단 chromatin–transcription lag를 명시 parameter로 출력하지 않아 region kinetic을 lag로 후처리해야 함. | `el-kazwini-2026-crakvelo` | moderate-strong (full-analysis, single-paper) | PDF 정밀 패스 완료. terminal state·deconvolution·run-time 우위는 supported. 단 공식 ablation·통계 검정 부재라 "순수 chromatin 효과"로 단정 금지. "lag 정량 적합"은 후처리 검증 전까지 유보(`검토필요:` Article in Press 표기 불일치 $k$/$T$/Table). |
| C10 | Luo benchmark의 "단일 best method 없음"(veloVI 0.23 최고, 평균 ≈0.1)은 우리 HSPC에 method를 데이터 기반으로 골라야 한다는 C2/C5를 보강한다. **우리 HSPC(GSE209878)가 Dataset12로 직접 사용됐으나 MultiVelo는 `rna_only=True`(ATAC 비활성)로만 평가** → multi-omic 강점은 미측정. | `luo-2026-velocity-benchmark` | moderate (full-analysis, single-paper) | "no single method superior" 문구·Dataset12 포함·MultiVelo `rna_only=True`는 PDF로 supported. RNA-only 순위·scenario 권고는 차용 가능하나, **multi-omic velocity 선택에 직접 인용 금지**(우리 핵심 모드 미측정). Dataset12 단독 method 순위는 mmc1/mmc2 추출 필요. |
| C11 | Safi 2022·Martin 2023은 같은 HSPC 시스템에서 chromatin priming이 commitment/transcription에 선행함을 보여 activation lag 가설의 *생물학적 plausibility*를 뒷받침한다 (정성적 선행성). Martin은 CRISPRi로 accessibility→expression 인과까지 보임(단 CD11b enhancer ns). | `safi-2022-chromatin-priming`, `martin-2023-hspc-chromatin` | moderate (full-analysis, biology, 정성적) | PDF로 priming 선행 방향은 supported. 단 **Safi는 paired multiome 아님(scATAC 단독 + pseudotime), Martin은 paired RNA 없음(외부 GEXC) + bulk** → gene별 lag *정량의 직접 근거 아님*, 배경·plausibility로 한정. 둘 다 mouse(human cross-species 미확정). association을 lag 인과로 확대 금지. `검토필요:` Safi GEO accession 불일치·2023 erratum. |
