# Comparison Table — epigenomic lag (3편)

입력: `papers.jsonl` · 근거: 각 논문 `full.md`
수치는 `full.md`에 명시된 값만 기재하며, 본문에 없는 값은 "미제시"로 둔다.

## 1. Method 축

| | MultiVelo (2023) | MultiVeloVAE (2025) | MoFlow (2026) |
|---|---|---|---|
| Method class | ODE + EM fitting | VAE + variational inference | DNN + local relay |
| 시간축 | gene-specific latent time | shared latent time (모든 gene 공통) | **latent time 없음** — local neighbor relay |
| Parameter 범위 | population 전체에 단일 parameter set | cell-specific `kc`, `rho` (continuous) | cell-specific `alpha_c`, `alpha`, `beta`, `gamma` |
| 상태 표현 | discrete 4-state (primed / coupled-on / decoupled / coupled-off) + model 1/2 | continuous coupling `kappa`, decoupling `delta = kc - rho` | continuous m1/m2 score, RNA-on/off score |
| chromatin 처리 | gene 주변 peak aggregation | gene-linked peak의 **summed** accessibility | gene-level `c`, opening/closing 시나리오를 angular error로 선택 |
| Uncertainty | 없음 | posterior, credible interval, cell-state uncertainty | 없음 |
| Multi-sample | 미지원 | conditional VAE로 batch 통합 | 미지원 |
| 통계 검정 | Wilcoxon rank-sum (기술 통계 수준) | Bayes factor 기반 differential dynamics test | KS / Fisher / Mann-Whitney (사후 분석) |

## 2. Assay 축

| | MultiVelo | MultiVeloVAE | MoFlow |
|---|---|---|---|
| 필수 modality | ATAC + RNA (unspliced/spliced) | 동일, 단 **RNA-only도 가능** | ATAC + RNA |
| Partial modality | 미지원 | 지원 (missing ATAC 생성) | 미지원 |
| 사용 platform | 10x Multiome, SHARE-seq | 10x Multiome, SHARE-seq, scRNA-seq | 10x Multiome, SHARE-seq |
| 외부 데이터 의존 | GWAS SNP, chromVar motif | Scenic+ GRN, ENCODE/ChromHMM | **NIH3T3 RNA half-life** (외부 cell line), polycomb/speckle gene set |
| 최대 분석 규모 | HSPC 11,605 cells | partial integration 27,841 cells / 1,044 genes | human cortex 4,693 cells / 842 genes |

## 3. Result 축

| | MultiVelo | MultiVeloVAE | MoFlow |
|---|---|---|---|
| 주 metric | Palantir pseudotime과 Spearman | GCBDir, k-step CBDir, held-out MSE/MAE | CBDir |
| 대표 수치 | mouse skin **0.51** vs scVelo 0.44 | exact value **본문 미제시** (Source Data 의존) | human cortex **0.362** vs MultiVelo 0.211, scVelo 0.211, cellDancer −0.015 |
| baseline 우위 근거 | scVelo 대비 backflow 감소 (정성) + Spearman 1건 | 10개 scRNA + 5개 multi-omic dataset에서 상대 우위 서술 | CBDir 1건 정량 + 나머지는 Supplementary 의존 |
| lag 관련 핵심 결과 | median primed interval 21%, decoupled 19% (mouse brain) | `delta = kc - rho` continuous priming (mouse skin Wnt3) | lag sign reversal >400 gene (≥25% bin), 129 gene (>75% bin) |
| lag 부호 해석 | 양수 전제 (`c → u → s`) | 부호 언급 없음, 연속값으로 처리 | **음수 lag를 biological signal로 해석** (OPC 63% vs 20%) |
| 고유 산출물 | model 1/2 분류, disease SNP timing (757 SNP) | differential dynamics test, in silico KO, missing ATAC | DAC gene group, RNA half-life 연결 |

## 4. Limitation 축

| | MultiVelo | MultiVeloVAE | MoFlow |
|---|---|---|---|
| 저자 명시 | TF lag mechanism 결론 불가, TF binding·looping 미포함 | mature cell type 어려움, de novo training 의존, pre-trained set 필요 | long-range enhancer-promoter 미모델링, gene-wise라 pathway-level 제한, UMAP distortion |
| benchmark 일관성 | dataset마다 metric 불일치 | exact value가 Source Data 의존 | dataset마다 exact value 불일치 |
| causal 검증 | 없음 (CRISPR 필요) | in silico KO만, 실제 perturbation 없음 | 없음 |
| chromatin 해상도 | gene-level aggregation | **summed** accessibility (저자 명시) | gene-level, enhancer 미포함 |
| 외부 데이터 위험 | — | — | half-life가 NIH3T3 유래, tissue 불일치 |

## 5. 같은 dataset 사용 현황

cross-paper 비교의 가장 강한 근거이므로 별도로 정리한다.

| Dataset | MultiVelo | MultiVeloVAE | MoFlow |
|---|---|---|---|
| SHARE-seq mouse skin | ✅ Figure 4 (Wnt3) | ✅ Figure 3f (Wnt3) | ✅ Figure 4·5 (Wnt3 포함) |
| E18 / embryonic mouse brain | ✅ Figure 2·3 | ✅ (MultiVelo dataset 재사용) | ✅ Figure 6·7 |
| Human HSPC | ✅ Figure 5 | ✅ Figure 3·4·5 | ✅ (규모 미제시) |
| 발달기 human brain cortex | ✅ fetal, Figure 6 | ✅ human embryonic brain | ✅ Trevino et al., Figure 2·3 |

**세 논문 모두 SHARE-seq mouse skin의 `Wnt3`를 분석했다.** 동일 gene·동일 dataset에 대한 3자 해석 비교가 가능하다 (insight.md §2 참조).
