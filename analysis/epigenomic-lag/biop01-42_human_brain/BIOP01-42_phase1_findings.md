# BIOP01-42 Phase-1 Findings — human_brain velocity → α (정정판 v2, 논문 정합 프레이밍)

> 작성 sjpark · 2026-07-27 (v1) · **정정 v2 2026-07-28** (self-review + 재검토 + PAPER_DIRECTION 정합 반영)
> target = **α** (lag 아님, 옵션 A) · 데이터셋 GSE162170 (발달 인간 대뇌피질 pcw21)
> 산출물 `/workspace/data/cache/biop01/human_brain_GSE162170/` · claim_level = **provisional**
> ⚠️ 이 문서는 self-review로 정정됨. v1의 "baseline 크로마틴이 α 예측" 양성 주장은 아래대로 한정됨.

## 0. 논문 정합 프레이밍 (먼저 읽기)

BIOP01-42는 **새 헤드라인이 아니라**, 논문(`manuscript/PAPER_DIRECTION.md`)의 **"α-robust / 발현-얽힘 / velocity 신뢰 결정지도"** 서사를 **method-robustness(VAE·scVelo) + 정직한 negative(발현 confound)**로 보강하는 **supporting 결과**다.

논문 stage가 민감(적대심사 ~75–85% reject 위험, 정직 base-case venue = Cell Reports Methods)하므로, 본 결과는 **supporting/categorical로만** 반영하고 **발현 confound를 명시**한다. 세 축의 반영 지침:

- **(a) cross-dataset α 재현** → **categorical supporting**("α는 lag과 달리 데이터셋 넘어도 rank 재현")으로만. PAPER_DIRECTION §6 "cross-dataset α gradient는 **n=3 confounded → headline 금지, categorical 대비만**"을 준수. 정량 헤드라인 금지.
- **(b) baseline ATAC→α** → **발현 confound negative**. "크로마틴 고유의 α 예측력"은 성립 안 함(발현과 분리 불가). PAPER_DIRECTION §2의 α↔abundance 강등과 정합.
- **(c) MultiVeloVAE** → **method-robustness 보강**(α가 특정 velocity method 아티팩트 아님). 단 same-preprocessing 재실행 시 확정.

## 1. 방법 (요약)

- 전처리: multiome spliced/unspliced RNA + ATAC gene activity + metadata → `brain_rna/atac.h5ad` (8981 cells × 13265 genes). counts는 Ensembl ID라 심볼공간 불일치로 제외, X=spliced.
- α 추정: scVelo dynamical `recover_dynamics` → `fit_alpha` (553 gene). MultiVeloVAE(velo-torch GPU) → `vae_alpha` (669 gene). ⚠️ VAE는 ATAC raw 스케일이 ELBO NaN을 유발해 per-cell normalize+log1p 후 smoothing(파이프라인 p2_dl_prep과 다른 ATAC prep — same-preprocessing 아님).
- baseline→α: per-gene ATAC 통계 → log α, held-out CV + **발현량 partial + shuffle-null**.
- cross-dataset: HSPC α(git `pipeline/hspc-velocity-benchmark/results/`)와 rank Spearman.

## 2. 결과 (정정 반영)

### (a) cross-dataset α 재현 — categorical supporting
| 비교 (method 쌍) | shared | Spearman |
|---|---|---|
| MultiVelo ↔ MultiVelo (git값 재현) | 102 | +0.475 |
| scVelo ↔ MultiVelo (내 독립) | 61 | +0.515 |
| VAE ↔ VAE (내 독립) | 142 | +0.406 |
| VAE ↔ MultiVelo | 129 | +0.300 |
| brain내 VAE ↔ scVelo | 553 | +0.662 |

→ α는 4 method 조합에서 rank 재현(모두 >0.3). **단 정량 헤드라인 아님** — n=3 코호트라 confounded(PAPER_DIRECTION §6), **"α는 lag과 달리 재현된다"는 categorical 진술로만** 사용. conserved-expression이 이 concordance를 부풀리는지 partial은 후속 확인 필요.

### (b) baseline ATAC → α — 발현 confound negative
| 지표 | 값 |
|---|---|
| 단순 Spearman(ATAC, log α) | +0.212 (p=4.7e-7) |
| Spearman(ATAC, 발현) / Spearman(발현, α) | +0.418 / +0.504 |
| **partial Spearman(ATAC, α | 발현)** | **+0.013 (p=0.75)** |
| shuffle-null(1000) thr(+2sd) | +0.087 (real +0.212 > thr) |

→ 원 연관(+0.212)은 shuffle-null 위지만 **발현량 통제 시 소멸(+0.013)**. **크로마틴 고유의 α 예측력은 성립 안 함.**
⚠️ **재검토(review the review)**: 발현이 confounder인지 mediator(크로마틴→α→발현)인지 단일 timepoint로 판별 불가. mediator면 발현 통제는 over-control이라 +0.013이 과소추정. → **"철회"가 아니라 "한정": ATAC-α 연관은 발현과 분리 불가, 크로마틴 고유 예측력은 확증도 반증도 아님(예측 연관은 성립, 기전 주장 불가).** PAPER_DIRECTION §2 α↔abundance 강등과 같은 테마.

### (c) lag — 미검정
본 run은 α만 계산. lag-fragile 헤드라인은 기존 파이프라인 몫이며 **내 fresh 결과 아님**. "lag-fragile 재확인" 표현 금지.

## 3. self-review 결함 목록 (사후구제 없이 기록)

- ① baseline→α 발현 confound (위 2b).
- ② "lag-fragile 재확인" 과대 → 미검정으로 한정.
- ③ VAE ATAC 정규화 deviation → VAE↔VAE(+0.406) same-preprocessing 아님(apples-to-oranges).
- ④ gene-selection bias(553/2000 fit) + cross-dataset 표본 작음(shared 61~142).
- ⑤ multi-seed 부재(프로젝트는 5-seed shuffle-null 규율).

## 4. 논문 정합성 — 종합판정

| 축 | 논문 claim-set 관계 |
|---|---|
| α cross-dataset 재현 | 정합(supporting). §6 n=3 confounded → categorical만, headline 금지 |
| baseline→α 발현 confound | 정합·강화. §2 α↔abundance 강등 재확인 |
| self-review 규율(shuffle-null·partial) | 논문 claim-defensibility 게이트와 동일 정신 |
| lag | 내 run 무관(기존 결과) |
| chromatin-coupling as lag-alt | 논문 이미 REJECTED(brain 미재현) — 같은 방향 |

**종합**: supporting 결과. ✅ 원 주장("크로마틴이 α 예측 +0.21")을 그대로 뒀다면 논문의 강등 입장과 **정면충돌**할 뻔했고, self-review가 이를 막았다.

## 5. 방어 가능한 최종 서술 (본문/블로그 반영 기준)

1. α는 cross-dataset·cross-method로 rank 재현된다(**categorical supporting, n=3 confounded 명시, headline 아님**).
2. baseline 크로마틴의 α 예측력은 발현량과 분리되지 않는다(**기전 주장 불가**) — 논문 α↔abundance 강등과 정합.
3. lag는 본 run 미검정. VAE 정합(+0.406)은 same-preprocessing 재실행 시 확정.

## 6. 산출물

`/workspace/data/cache/biop01/human_brain_GSE162170/`: brain_rna/atac.h5ad, brain_rna_dynamical.h5ad, brain_gene_alpha.csv, brain_multivelovae_genes.csv, brain_multivelovae.h5ad, brain_crossdataset_alpha_concordance.json, brain_vae_concordance.json, brain_baseline_atac_to_alpha.json, brain_selfreview_atac_alpha.json.
