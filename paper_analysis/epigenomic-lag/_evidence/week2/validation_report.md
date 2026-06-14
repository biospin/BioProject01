# Validation Report

## 1. Overall Verdict

- 종합 판정: `revise`
- 가장 강한 insight: C1, C3, C4. 세 paper의 method evolution과 repeated limitations는 기존 분석 파일에서 직접 확인된다. celldancer/deepvelo full-analysis 추가로 *cell-specific kinetics 분기 lineage*가 PDF citation 수준에서 보강됨.
- 가장 약한 insight: C6. MoFlow lag group을 MultiVeloVAE differential test로 재검정하는 hybrid workflow는 논리적으로 자연스럽지만 아직 직접 evidence가 없다.
- 새로 보강된 insight: C7 (mmVelo PDF 정밀 패스로 `partially-supported` → `supported (preprint-tier)`); C8 (DeepKINET PDF 정밀 패스로 *concrete transferability map* 확보).
- 2026-06-12 승격 재평가: C9 (CRAK-Velo), C10 (Luo benchmark), C11 (Safi·Martin biology)의 4편이 **abstract-only → full-analysis로 승격**됨. evidence strength `weak → moderate~moderate-strong`, verdict `partially-supported → supported`(claim의 핵심 사실 부분). 단 셋 다 *한정 조건*이 명확해져, 그 한정을 넘는 확대는 여전히 overreach: C9는 lag 명시 출력 부재, C10은 MultiVelo `rna_only=True`(multi-omic 미측정), C11은 paired RNA 부재(정량 근거 아님). 이들은 핵심 방향(C1–C5)을 보강할 뿐 바꾸지 않는다.
- 다음 수정 우선순위:
  - C2와 C6은 "결론"이 아니라 `해석:` 또는 follow-up proposal로 유지해야 한다.
  - C5는 wet-lab "실험"이 아니라 computational benchmark로 표현해야 한다.
  - C7은 preprint maturity가 유일한 잔여 caveat — `검토필요: peer-review 출간 모니터링`만 남긴다.
  - C8은 "transfer 가능 / 부분 / 불가" 3-단계 transferability map으로 정리한다.
  - C9는 "CRAK-Velo가 lag를 명시 출력하지 않음 → region kinetic 후처리 필요"를 반드시 동반. C10은 "MultiVelo가 `rna_only=True`로 평가됨 → multi-omic 미측정"을 반드시 동반. C11은 "Safi scATAC 단독·Martin paired RNA 없음 → 정량 근거 아닌 배경"을 반드시 동반.
  - 남은 검토필요: CRAK-Velo Article-in-Press 표기 불일치($k$/$T$/Table 번호); Safi GEO accession 불일치(GSE173075/76 vs GSE148746) + 2023 erratum 미반영.
  - `handoff.md`에는 바로 실행할 수 있는 action item과 사용자 확인 필요 항목을 분리한다.

## 2. Claim-level Evidence Check

| claim_id | verdict | evidence found | missing evidence | overreach risk | action |
|---|---|---|---|---|---|
| C1 | supported | MultiVelo core는 ODE/discrete state; MultiVeloVAE core는 cVAE/continuous/multi-sample; MoFlow core는 latent time-free relay velocity. cellDancer (`@li2023celldancer` core p.61 §Introduction)는 *latent time-free local neighbor cosine loss*를 처음 제시해 MoFlow의 *direct predecessor*임을 PDF로 확인. DeepVelo (`@cui2024deepvelo` core p.41 §Background)는 *GCN + continuity loss*로 cell-specific kinetics를 self-supervised로 학습 — MultiVeloVAE의 cell-specific kinetics rationale에 대한 RNA-only predecessor. | 없음 | 낮음 | 그대로 사용. cell-specific kinetics 분기는 cellDancer/DeepVelo PDF로 lineage가 한 단계 더 깊게 확인됨. |
| C2 | partially-supported | MoFlow는 direct lag outputs, MultiVeloVAE는 multi-sample/differential test 기능 보유 | 실제 우리 dataset benchmark 없음 | 중간. "적합하다"가 확정처럼 들릴 수 있음 | `해석:`으로 표시하고 "우선 테스트 전략"으로 낮춰 표현 |
| C3 | supported | MultiVelo single c per gene; MultiVeloVAE individual CRE 직접 modeling 부재; MoFlow long-range enhancer-promoter/motif-level modeling 부재. mmVelo PDF (p.2 §1)가 MultiVelo 한계를 *직접 인용*: *"this aggregates the peak accessibility for each gene, making it difficult to determine the dynamics at the resolution of the single-peak level"* — gene-level aggregation 한계가 후속 paper에서 명시적으로 비판됨. | 우리 HSPC peak-level source data 비교는 여전히 없음 | 낮음 | 그대로 사용 |
| C4 | supported | MultiVelo TF lag association; MultiVeloVAE perturbation wet-lab 검증 부재; MoFlow mechanism external reference association. DeepKINET 저자도 Discussion p.12에서 SERGIO-style simulation 외에는 *strict* kinetic ground truth가 없음을 인정 — causal validation 부족이 RNA velocity field 전반의 공통 bottleneck임을 보강. | 각 paper의 모든 biological claim을 일괄 평가한 것은 아님 | 낮음-중간 | "핵심 mechanistic interpretation의 causal validation 부족"으로 표현 |
| C5 | partially-supported | 두 paper가 서로 직접 비교하지 않고 MultiVelo와 각각 비교. cellDancer는 MoFlow가 *외부 후속 paper*로서 CBDir로 재평가했을 때 HSPC $-0.056$, SHARE-seq $0.026$로 *MultiVelo·MoFlow보다 낮음* (`@li2023celldancer` core p.270, MoFlow Supp Table 1) — 즉 *MoFlow의 직접 ancestor benchmark* 만이 통일 metric으로 존재. | 직접 metric unification (MoFlow ↔ MultiVeloVAE)이 아직 설계되지 않음 | 중간 | "우선순위 높은 computational benchmark"로 수정 |
| C6 | needs-source-check | MoFlow lag outputs와 MultiVeloVAE differential test 기능은 각각 존재 | 같은 gene/cell에서 두 output이 compatible한지 미검증 | 높음 | follow-up idea로만 유지. 실행 전 input schema compatibility 확인 |
| C7 | supported (preprint-tier) | mmVelo PDF 정밀 패스 완료. (a) *peak-level resolution* 메커니즘은 *decoder output dimension*임을 PDF p.2 §1, p.3 §2.1, p.13–14 §5.4–5.5에서 확인 — peak가 *공통 latent transition* $d_n$을 *공유*하되 *peak-specific decoder branch* $f_p^a$를 통과한 차분 $\Delta \text{ATAC} = C^a \odot (f^a(z_n + \rho d_n) - f^a(z_n))$로 single-peak velocity를 정의 (per-peak ODE rate는 *없음*). (b) MultiVelo와 *직접 benchmark*함: SHARE-seq mouse skin hair shaft-cuticle/cortex lineage에서 spliced/unspliced/gene-aggregated/peak-level 네 가지 consistency score (Fig S3j-m, PDF p.4 §2.3, p.26). (c) Code: github.com/nomuhyooon/mmVelo (PDF p.23 §10.3), license CC-BY 4.0 (PDF footer). | PDF read로 supported; preprint 성숙도가 유일한 잔여 caveat | 낮음 | "후보"가 아니라 "supported with preprint-tier caveat"로 표현. `검토필요: peer-review 출간 모니터링 (bioRxiv 10.1101/2024.12.11.628059 v1 2024-12-17)`; GitHub repo license verification. |
| C9 | supported (full-analysis, single-paper) | `@elkazwini2026crakvelo` PDF 정밀 패스(core/lens). UniTVelo 확장 semi-mechanistic 정체성·수식(Eq.4–13) 확인. **동일 GSE209878 HSPC(11,605/2,000/3,939)에서 MultiVelo와 직접 head-to-head**: CBDir 최고, platelet terminal state 정확 식별(MultiVelo는 erythrocyte→granulocyte spurious flow), KNN 우위(HDC 0.259 vs 0.183), run-time 15h vs >24h(Table S1). 모두 본문 근거. | 공식 ablation(chromatin term on/off, $k=0$, weight permutation) 없음 → "순수 chromatin 효과" 분리 안 됨. CBDir·KNN에 통계 검정·CI 없음. **lag를 명시 parameter로 출력하지 않음** — region kinetic은 pseudotime 축 시각화. | 중간 — "MultiVelo 우위/대체"는 supported지만, "lag 정량에 적합"으로 확대하면 overreach(lag 후처리 미검증). | "동일 HSPC head-to-head에서 MultiVelo 대비 단순·빠르고 우위" supported. 단 "lag layer 대체"가 아니라 "region kinetic을 lag로 후처리해야 함" 동반. `검토필요:` Article-in-Press 표기 불일치($k$=0.5 vs Eq.15/16, $T$=20/30/50, Table S1/S2) — 최종본 교정 모니터링. |
| C10 | supported (full-analysis, single-paper) | `@luo2026velocitybenchmark` PDF 정밀 패스. "no single method exhibited superior performance in all the assessments"는 본문에 직접 존재, 17 real + 3 simulation·15 method로 정량 입증(veloVI CBDir 0.23 최고, 평균 ≈0.1). **우리 HSPC(GSE209878)가 Dataset12로 직접 사용**(transition HSC→MPP 등, core.md Tables S1). C2/C5의 데이터 기반 선택 원칙과 정합. | **MultiVelo가 STAR Methods에서 `rna_only=True`(ATAC 비활성)로 평가** — 우리에게 핵심인 multi-omic 모드 성능이 측정되지 않음(core.md Methods/분석 메모). Dataset12 단독 method 순위 수치 표가 본문에 없음(합산 분포). | 중간 — RNA-only 순위를 우리 multi-omic 도구 선택에 직접 적용하면 overreach. | "no single method superior + Dataset12 직접 포함" supported. **반드시 동반**: "MultiVelo가 `rna_only=True`로 평가되어 multi-omic 강점 미측정 → multi-omic velocity 선택은 자체 검증". Dataset12 순위는 mmc1/mmc2 추출 필요. |
| C11 | supported (full-analysis, biology, 정성적) | `@safi2022chromatinpriming` PDF: commitment에 앞서 stem/lineage program 동시 보유하는 CD9high cluster 3, lympho-myeloid 최초 transition point가 cluster 3에 mapping, distal homogeneity 0.434 vs 0.246, scRNA cluster 3 enrich p<10⁻⁵. `@martin2023hspcchromatin` PDF: HSC-primed CRE <25% 유지, HSC-unique 3,026 peak erythroid GO, CRISPRi CD115 enhancer p<.0001(CD11b enhancer ns). 둘 다 같은 HSPC 축에서 chromatin priming 선행을 정성적으로 supported. | **Safi는 paired multiome 아님**(scATAC↔scRNA 다른 batch projection), transition 축이 pseudotime. **Martin은 paired RNA 없음**(외부 GEXC) + bulk ATAC. 둘 다 시간 단위 gene별 lag 정량 안 함. 둘 다 mouse(human cross-species 미확정). Safi GEO accession 불일치·2023 erratum. | 높음 — "priming 선행"(정성)을 "gene별 lag 정량/인과 근거"로 확대하면 association→causality + modality 비약. | "lag 가설의 생물학적 plausibility/배경"으로 한정. **반드시 동반**: "Safi scATAC 단독·pseudotime, Martin paired RNA 없음 → lag 정량 직접 근거 아님". `검토필요:` Safi GEO accession(GSE173075/76 vs GSE148746)·2023 erratum; cross-species. |
| C8 | partially-supported (with concrete transferability map) | DeepKINET PDF 정밀 패스 완료. *Transfer 가능*: (i) 2-stage decoupling 학습 전략 (Stage 1 VAE freeze → Stage 2 cell-specific rate decoder, lens-academic §3 PDF p.13–14, core p.111). (ii) 100-repeat multi-method box-plot evaluation + *negative correlation = fail* rule (core p.13 Fig 3b). (iii) Cluster-level set-vs-estimated scatter benchmark template. *Partial*: SERGIO-style chromatin-aware simulator는 *재설계 필요* — DeepKINET은 rate (1/time) 단위 inject, lag는 time 단위 inject (lens-academic §3 PDF p.121). *Transfer 불가*: (i) scEU-seq/scNT-seq RNA labeling 자체는 *chromatin opening event를 label하지 않음* (lens-academic §3 PDF p.114) — single-cell chromatin labeling 표준 부재. (ii) Dynamo-derived rate를 *chromatin lag ground truth*로 차용 불가 — MultiVelo switch time을 차용하면 *circular validation*. | concrete 4-bullet transferability map으로 정리됨; 잔여 gap은 chromatin-aware simulator 설계와 chromatin labeling 표준 부재 | 낮음 (이전 중간 → 명시화로 risk 감소) | "validation design reference 제한" → "framework borrow 가능 / labeling ground truth 불가" 양면으로 표현. 후속: chromatin-aware simulator 설계 (BEELINE, MultiVelo authors simulation script 후보 검토) + DeepKINET-Multiome 형태의 chromatin-aware extension 모니터링. |

## 2b. Status Enum + Novelty (Week3 rubric 정렬)

Week3 과제 안내(박상준)의 Validation 기록 형식에 맞춰, §2의 내부 verdict를 과제 공통 **Status enum**(`Valid` / `Needs Evidence` / `Overstated` / `Unclear` / `Rejected`)으로 매핑하고, 6기준 중 누락돼 있던 **Novelty**(단순 요약이 아닌 새 insight인가, 상/중/하)를 claim별로 명시한다. Week4 Agent 구현 시 출력 형식 통일(토론질문 ⑤)을 위한 정렬 layer다. 내부 verdict(`supported` 등)는 §2에 그대로 유지.

| claim_id | 내부 verdict (§2) | **Status (과제 enum)** | **Novelty** | 조건/메모 |
|---|---|---|---|---|
| C1 | supported | **Valid** | 중 | field 재구조화 + cellDancer/DeepVelo predecessor lineage 확인 (신규 발견보다 구조화) |
| C2 | partially-supported | **Overstated** | 중 | "적합하다" 단정 → `해석:`/병렬 검증 전략으로 하향 |
| C3 | supported | **Valid** | 하~중 | gene-level c aggregation 한계 — field 공통, 잘 알려진 한계 |
| C4 | supported | **Valid** | 하 | causal validation 부족 — field 전반 bottleneck (널리 인정됨) |
| C5 | partially-supported | **Needs Evidence** | 상 | head-to-head 부재라는 구체 gap. 단 "실험"→"computational benchmark" 표현 + 우리 data benchmark 미수행 |
| C6 | needs-source-check | **Unclear** | 상 | hybrid workflow 신규 아이디어지만 output compatibility 미검증 → follow-up only |
| C7 | supported (preprint-tier) | **Valid** | 상 | decoder-level peak resolution(≠per-peak ODE rate) 구분 명확. 잔여: preprint 출간 모니터링 |
| C8 | partially-supported | **Needs Evidence** | 중~상 | validation framework는 transfer 가능(✅), chromatin-aware simulator 재설계·labeling ground truth는 미해결(⚠️/❌) |
| C9 | supported (full-analysis) | **Valid** | 상 | 동일 GSE209878 HSPC head-to-head 우위는 supported. **조건**: lag 명시 출력 부재 → region kinetic 후처리 필요(확대 시 Overstated) |
| C10 | supported (full-analysis) | **Valid** | 중 | "no single method superior" + 우리 HSPC=Dataset12 직접. **조건**: MultiVelo `rna_only=True` → multi-omic 미측정, RNA-only 순위만 차용 |
| C11 | supported (full-analysis, 정성적) | **Valid** | 하~중 | chromatin priming 선행의 생물학적 plausibility(배경). **조건**: Safi scATAC 단독·Martin paired RNA 없음 → gene별 lag 정량 근거 아님, mouse |

**요약**: Valid 7 (C1·C3·C4·C7·C9·C10·C11, 단 C9–C11은 조건부) / Needs Evidence 2 (C5·C8) / Overstated 1 (C2) / Unclear 1 (C6) / Rejected 0. Novelty 상: C5·C6·C7·C9, 중: C1·C2·C8·C10, 하~중: C3·C11, 하: C4. → 설득력↑(Valid)이면서 Novelty 상인 **C7·C9**가 가장 강한 insight, Novelty 상이지만 미검증인 **C5·C6**가 다음 분석 우선순위.

## 3. Missing Assumptions

- claim: C2
  - 빠진 전제: 우리 HSPC data가 MoFlow와 MultiVeloVAE 양쪽의 preprocessing/input requirement를 모두 만족한다는 전제.
  - 왜 중요한가: 두 method가 요구하는 normalization, smoothing, peak-to-gene aggregation이 다르면 output concordance가 method 차이가 아니라 preprocessing 차이일 수 있다.
  - 확인 방법: 동일 AnnData/MuData에서 공통 preprocessing branch와 method-specific preprocessing branch를 분리해 benchmark한다.

- claim: C5
  - 빠진 전제: CBDir과 GCBDir을 같은 dataset에서 모두 계산할 수 있다는 전제.
  - 왜 중요한가: MoFlow paper는 CBDir 중심, MultiVeloVAE는 GCBDir/다축 metric 중심이라 metric 차이 자체가 결론을 바꿀 수 있다.
  - 확인 방법: 최소 metric set을 CBDir, GCBDir, runtime, memory, lag-score concordance로 고정한다.

- claim: C6
  - 빠진 전제: MoFlow의 gene/cell-specific kinetic outputs와 MultiVeloVAE의 $\delta/\kappa$ outputs가 같은 cell/gene indexing으로 안정적으로 매핑된다는 전제.
  - 왜 중요한가: gene filtering 또는 cell filtering이 다르면 concordance 분석이 biased된다.
  - 확인 방법: shared gene/cell intersection을 먼저 만들고, dropped genes/cells의 bias를 보고한다.

- claim: C7
  - 빠진 전제: mmVelo의 *single-peak chromatin velocity*가 per-peak ODE rate 없이 *decoder branch level* 에서 정의된다는 사실이 우리 lag framework에 *acceptable*하다는 전제.
  - 왜 중요한가: per-peak kinetic rate가 없으므로 mmVelo의 peak-level output을 "lag"로 해석할 때 *peak 간 timing 차이*는 *decoder weight 차이*에서 오는 것이지 *peak-specific ODE rate*에서 오는 것이 아님 — 해석 prior를 명확히 해야 한다.
  - 확인 방법: mmVelo의 Fig 2c-e Neurod2 enhancer→promoter→mRNA pseudotime ordering을 우리 HSPC multiome에서도 ablation으로 재현해, decoder-level peak ordering이 *cluster-level temporal consistency*를 제공하는지 확인.

- claim: C8
  - 빠진 전제: DeepKINET-style cluster-level set-vs-estimated benchmark가 우리 *chromatin-aware simulator*에서도 작동할 수 있다는 전제.
  - 왜 중요한가: lag inject는 time 단위, DeepKINET inject는 rate (1/time) 단위 — 동일 simulator 골격을 재사용하려면 *chromatin opening event time과 transcription start time을 명시적으로 설정*해야 함. simulator 재설계 부재 시 benchmark 차용이 무효화.
  - 확인 방법: BEELINE 또는 MultiVelo authors의 simulation script를 첫 후보로 검토하고, 없으면 SERGIO를 *time-event annotation* 가능하게 수정한 fork를 만들어야 함을 사용자에게 보고.

- claim: C9 (PDF 확인 완료 — 잔여 전제)
  - 빠진 전제: CRAK-Velo의 region kinetic plot(accessibility-peak↔unspliced-peak pseudotime 차이)을 gene별 lag 수치로 후처리하면 우리 lag 정의와 매핑된다는 전제. PDF 확인 결과 **CRAK-Velo는 lag를 명시 parameter로 출력하지 않음**이 확정됨.
  - 왜 중요한가: head-to-head에서 CRAK-Velo가 MoFlow의 DTW c-s lag에 대응하는 출력을 직접 주지 않으므로, lag 비교 축을 맞추려면 region kinetic 후처리 파이프라인이 선행돼야 한다.
  - 확인 방법: region kinetic의 peak-pseudotime 차이를 lag proxy로 정의하는 후처리를 우리 GSE209878에서 시범 구현해 MultiVelo switch time / MoFlow DTW lag와 정합하는지 검증.

- claim: C10 (PDF 확인 완료 — 핵심 caveat 확정)
  - 빠진 전제: Luo benchmark가 우리 multi-omic 사용 맥락을 평가했다는 전제는 **기각됨** — PDF 확인 결과 MultiVelo는 `rna_only=True`(ATAC 비활성)로만 평가됐고, Dataset16(10x multiome)조차 ATAC를 켜고 평가하지 않았다. 우리 HSPC는 Dataset12로 포함됐으나 RNA-only 조건이다.
  - 왜 중요한가: "단일 best 없음"·scenario 권고는 RNA-only velocity 선택에는 적용되나, multi-omic velocity(MultiVelo/MultiVeloVAE/MoFlow/CRAK-Velo) 선택에는 그대로 적용되지 않는다.
  - 확인 방법: multi-omic 모드를 켠 자체 mini-benchmark(Dataset12 GSE209878 + Dataset17 GSE81682)로 ATAC를 켠 method들의 CBDir을 재측정.

- claim: C11 (PDF 확인 완료 — 한정 확정)
  - 빠진 전제: chromatin priming의 *정성적 선행성*이 우리가 정량하려는 *gene별 time-lag*와 동일 현상이라는 전제는 **성립하지 않음** — PDF 확인 결과 Safi는 paired multiome이 아니라 scATAC 단독 + pseudotime이고(scRNA는 다른 batch projection), Martin은 paired RNA 없이 외부 GEXC + bulk ATAC다.
  - 왜 중요한가: priming(특정 단계에서 chromatin이 미리 열림)과 lag(같은 cell에서 chromatin open → transcription onset 시간차)는 관련은 있으나 동일하지 않다. paired RNA·시간 축이 없으면 lag로 환산되지 않는다.
  - 확인 방법: 우리 GSE209878(human, paired multiome)에서 같은 cell의 promoter ATAC change point와 transcription onset의 pseudotime 차이를 직접 측정 — Safi/Martin은 그 직전 단계(accessibility-side, 다른 species)의 배경 문헌으로만 유지.

## 4. Overreach / Weak Claims

- claim: C2
  - 현재 표현: "우리 use case에는 MoFlow primary, MultiVeloVAE secondary 전략이 적합하다."
  - 문제: 기존 paper evidence 기반의 분석자 판단이며, 우리 data benchmark 결과는 없음.
  - 더 안전한 표현: `해석: 현재 evidence 기준으로는 MoFlow를 direct lag quantification 후보, MultiVeloVAE를 multi-sample/differential test 후보로 나누어 병렬 검증하는 전략이 합리적이다.`

- claim: C5
  - 현재 표현: "direct head-to-head가 다음 우선순위 높은 실험/분석이다."
  - 문제: wet-lab experiment로 오해 가능.
  - 더 안전한 표현: "direct head-to-head computational benchmark가 다음 우선순위 높은 분석이다."

- claim: C6
  - 현재 표현: "hybrid workflow가 유망하다."
  - 문제: 실제 output compatibility, statistical validity 미검증.
  - 더 안전한 표현: "`질문:` MoFlow lag group을 MultiVeloVAE differential test의 hypothesis set으로 넣을 수 있는가? 먼저 compatibility pilot 필요."

- claim: C7
  - 현재 표현: "mmVelo는 gene-level c aggregation gap을 메우는 후보이다."
  - 문제: 이전엔 preprint metadata만으로 표현했지만, PDF 정밀 패스로 mechanism이 명확해진 만큼 *gap-filling의 의미*도 정밀화 필요. mmVelo는 *per-peak ODE rate*가 아니라 *decoder branch resolution*으로 peak-level를 정의함.
  - 더 안전한 표현: "mmVelo는 *decoder-level peak resolution*으로 single-peak chromatin velocity를 정의해 gene-level aggregation을 *부분적으로* 메우는 후보. `검토필요: preprint 출간 모니터링 + per-peak ODE rate가 아닌 decoder-level resolution임을 인용 시 명확히 구분`."

- claim: C9 (CRAK-Velo)
  - 현재 표현: "동일 GSE209878 HSPC에서 MultiVelo 직접 비교 우위, 단순·빠름."
  - 문제: 성능 우위(terminal state·deconvolution·run-time)는 PDF로 supported지만, "lag 정량에 적합"이나 "순수 chromatin 효과"로 확대하면 overreach(공식 ablation 부재, lag 명시 출력 부재).
  - 더 안전한 표현: "`해석: CRAK-Velo는 동일 HSPC에서 MultiVelo 대비 단순·빠르고 terminal state·deconvolution 우위. 단 chromatin–transcription lag를 명시 parameter로 출력하지 않으므로 region kinetic의 peak-pseudotime 차이를 lag로 후처리해야 하며, chromatin 통합의 인과 기여는 ablation 부재로 미분리(검토필요: Article-in-Press 표기 불일치).`"

- claim: C10 (Luo benchmark)
  - 현재 표현: "데이터 기반 method 선택을 보강한다."
  - 문제: 우리 HSPC가 Dataset12로 쓰였으나 MultiVelo가 `rna_only=True`로 평가됐다 — RNA-only 결론을 우리 multi-omic 도구 선택에 직접 적용하면 overreach.
  - 더 안전한 표현: "`해석: 'no single method superior' + 우리 HSPC(GSE209878)=Dataset12 직접 포함은 단일 default를 피하라는 원칙을 보강한다. 단 MultiVelo가 rna_only=True(ATAC 비활성)로만 평가되어 multi-omic 성능은 미측정이므로, RNA-only 순위·scenario 권고만 차용하고 multi-omic velocity 선택은 자체 검증한다.`"

- claim: C11 (Safi·Martin)
  - 현재 표현: "activation lag 가설을 생물학적으로 뒷받침한다."
  - 문제: "priming 선행"(정성)을 "gene별 lag의 정량/인과 근거"로 확대하면 association→causality 및 modality 비약. Safi scATAC 단독, Martin paired RNA 없음이 PDF로 확정됨.
  - 더 안전한 표현: "`해석: Safi(scATAC 단독 + pseudotime)·Martin(paired RNA 없음, bulk + CRISPRi 인과)은 같은 HSPC 축에서 chromatin priming 선행의 정성적 방향을 보여 lag 가설의 plausibility를 더한다. paired multiome·시간 단위 lag 정량이 없고 둘 다 mouse이므로 gene별 lag의 직접 근거가 아니라 배경으로 한정한다.`"

## 5. Source Coverage

| paper | status | evidence quality | validation note |
|---|---|---|---|
| `li-2023-multivelo` | full-analysis | high | core/lens/methodology 모두 존재. 주요 수치와 한계 확인됨. |
| `li-2025-multivelovae` | full-analysis | high | core/lens/methodology + supplementary/source-data 언급 존재. Exact numeric matrix는 추가 추출 가능. |
| `hong-2026-moflow` | full-analysis | high | core/lens/methodology 모두 존재. CBDir 수치와 MoFlow vs MultiVeloVAE 비교 노트 확인됨. |
| `li-2023-celldancer` | full-analysis | high | core 494L + lens 331L. PDF 정밀 패스 완료. MoFlow의 *직접 predecessor*임이 핵심 — *latent time-free cosine loss*가 본 paper §Introduction p2에서 처음 제시되어 MoFlow가 이를 chromatin-aware로 확장한 lineage가 PDF로 확인됨. |
| `nomura-2024-mmvelo` | full-analysis | high (preprint-tier) | core 361L + lens 302L. PDF 정밀 패스 완료. *single-peak chromatin velocity*가 decoder-level resolution임을 PDF p.2/p.3/p.13–14에서 확인. SHARE-seq에서 MultiVelo와 *직접 benchmark* (Fig S3j-m). License CC-BY 4.0, code public. `검토필요: peer-review 출간 모니터링`. |
| `cui-2024-deepvelo` | full-analysis | high | core 552L + lens 370L. PDF 정밀 패스 완료. *GCN + continuity loss* 기반 cell-specific kinetics — MultiVeloVAE의 cell-specific kinetics rationale에 대한 RNA-only predecessor. chromatin은 없음. |
| `mizukoshi-2024-deepkinet` | full-analysis | high | core 383L + lens 337L. PDF 정밀 패스 완료. *2-stage decoupling 학습 + 100-repeat box-plot + negative correlation fail rule + cluster-level simulation benchmark* 의 *evaluation framework*는 transferable; *scEU-seq/scNT-seq labeling 자체*는 non-transferable (단일-cell chromatin labeling 표준 부재). C8 transferability map의 1차 source. |
| `el-kazwini-2026-crakvelo` | full-analysis | high | core(26KB) + lens + methodology-brief + Additional file 1/2. PDF 정밀 패스 완료. UniTVelo 확장 semi-mechanistic, **동일 GSE209878 HSPC에서 MultiVelo 직접 비교** 우위 + run-time 15h vs >24h 확인. lag 명시 출력 부재·ablation 부재는 한계. `검토필요:` Article-in-Press 표기 불일치($k$/$T$/Table) — 최종본 모니터링. C9 근거. |
| `luo-2026-velocity-benchmark` | full-analysis | high | core(33KB) + lens + methodology-brief + STAR Methods + mmc1/mmc2. PDF 정밀 패스 완료. 15 method·17 real + 3 simulation, "no single method superior"·우리 HSPC = Dataset12 확인. **MultiVelo `rna_only=True` 확정** — multi-omic 미측정. Dataset12 단독 순위는 mmc 추출 필요. C10 근거. |
| `safi-2022-chromatin-priming` | full-analysis | high (biology, 정성적) | core(31KB) + lens + methodology-brief + mmc1–7. PDF 정밀 패스 완료. CD9high concurrent priming·SPI1/GATA1 crossover·기능 검증 확인. **paired multiome 아님(scATAC↔scRNA projection) + pseudotime 축** → lag 정량 직접 근거 아님. mouse. `검토필요:` GEO accession 불일치(GSE173075/76 vs GSE148746)·2023 erratum. C11 근거의 절반. |
| `martin-2023-hspc-chromatin` | full-analysis | high (biology) | core(24KB) + lens + methodology-brief + supplementary. PDF 정밀 패스 완료. **review→primary research article 정정**(ATAC-seq + CRISPRi). HSC-primed CRE <25% 유지·HSC-unique 3,026 peak·CRISPRi 인과(CD11b enhancer ns) 확인. **paired RNA 없음(외부 GEXC) + bulk** → 시간 lag 정량 불가. mouse. C11 근거의 절반. |

## 6. Cross Validation Notes

- 다른 Validation Agent와 일치: 아직 없음. 현재는 single validation run.
- 다른 Validation Agent와 불일치: 해당 없음.
- 토론으로 남길 항목:
  - MoFlow와 MultiVeloVAE 중 어떤 method를 primary로 볼지.
  - metric을 CBDir/GCBDir 중 무엇으로 통일할지.
  - 우리 HSPC benchmark를 먼저 할지, source data 수치 추출을 먼저 할지.

## 7. Required Revisions to insight.md

- C2, C6은 final claim이 아니라 `해석:` 또는 follow-up proposal로 표시.
- C5의 "실험/분석"을 "computational benchmark"로 구체화.
- "적합" 같은 확정 표현은 "현재 evidence 기준의 테스트 전략"으로 낮춘다.
- C7: "preprint이며 PDF/code 확인 전이므로 강한 결론 금지" 문구를 *제거*하고 "PDF 정밀 패스로 mechanism은 supported; preprint 성숙도가 잔여 caveat"로 교체. "후보" → "supported (preprint-tier)". *Decoder-level resolution*과 *per-peak ODE rate 없음*을 정확히 표현.
- C8: "RNA-only splicing/degradation validation을 chromatin lag validation으로 직접 확대하지 않기"를 *유지*하되, 그 뒤에 *4-bullet transferability map* (✅ 2-stage decoupling + 100-repeat benchmark / ⚠️ chromatin-aware simulator 재설계 / ❌ scEU-seq labeling 자체 / ❌ Dynamo proxy ground truth) 명시.
- C9/C10/C11(full-analysis 승격): 세 claim 모두 evidence strength `weak → moderate~moderate-strong`, verdict `partially-supported → supported`(핵심 사실 부분)로 갱신. 단 한정 조건을 반드시 동반: C9는 "lag 명시 출력 부재 → region kinetic 후처리 필요 + ablation 부재", C10은 "MultiVelo `rna_only=True` → multi-omic 미측정, RNA-only 순위만 차용", C11은 "Safi scATAC 단독·Martin paired RNA 없음 → 정량 근거 아닌 배경, mouse cross-species". 남은 `검토필요:`: CRAK-Velo Article-in-Press 표기 불일치, Safi GEO accession 불일치·2023 erratum.

## 8. Handoff Decision

- Jira / Confluence로 넘겨도 되는 항목:
  - Week2 workflow demo 산출물 생성 완료.
  - HSPC head-to-head benchmark 설계.
  - MoFlow license 확인.
  - mmVelo PDF/code/license 확인.
  - source data에서 exact benchmark matrix/gene list 추출.
- 보류할 항목:
  - hybrid MoFlow lag group + MultiVeloVAE differential test는 compatibility pilot 전까지 보류.
  - enhancer-resolved lag model은 장기 아이디어로 보류.
- 추가 paper analysis가 필요한 항목:
  - **11편 모두 full-analysis로 승급 완료** (2026-06-12 CRAK-Velo/Luo benchmark/Safi 2022/Martin 2023 승격). evidence set 전체가 PDF-기반.
  - 잔여 source 확인(분석 승급은 불필요, 사실 검증만): (1) CRAK-Velo Article-in-Press 최종본 교정($k$/$T$/Table 번호) 모니터링. (2) Luo Dataset12(HSPC) 단독 method 순위를 mmc1/mmc2/원자료에서 추출 — C10을 우리 데이터에 직접 적용할 때 필요. (3) Safi GEO accession(GSE173075/76 vs GSE148746) GEO 직접 확인 + 2023 erratum 대조.
  - DeepKINET이 *in-house validation design reference*로 들어왔으므로 *perturbation/time-stamped ground truth* paper는 Week3에서 *chromatin-aware* 방향(perturb-seq + multiome, time-resolved multiome, 또는 BEELINE-style chromatin-aware simulator 논문)으로 좁혀 추가하면 C4(causal validation)와 C8(validation design transfer) 두 gap을 동시에 메울 수 있다.
