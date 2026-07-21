# STEP2 결과 (EXPLORATORY) — baseline 크로마틴이 재현되는 α를 설명하는가, lag은 왜 취약한가

> 🧪 **EXPLORATORY — 팀·박상준 합의 게이트(설계 §9, WEEK7 §5) 전 재프레이밍이다.**
> 본문(draft)·헤드라인 `FINDINGS.md`·`PAPER-PLAN.md`에 **미반영이 원칙**. 이 폴더(`results/step2/`)에 격리.
> 정본 protocol: `../../STEP2-CHROMATIN-EXPLAINS-KINETICS-DESIGN.md`. 실행일 2026-07-13.
> 엄밀성 게이트 승계(repo CLAUDE.md): 염색체 hold-out CV · permutation null · 강상관 regularize(ElasticNet) ·
> pseudotime≠wall-clock · **상관≠인과(예측/설명만 주장, perturbation 없음)** · 결정론적(seed=20260713).

## 0. 한 줄 결론 (model-robust dissociation 우선, ΔR² 아님)
동일 baseline feature 집합으로 **선형(ElasticNet)·비선형(GBM) 두 모델 모두 α는 예측하나(R²=0.34/0.37, p<0.01),
lag은 둘 다 예측하지 못한다(R²=0.017/−0.04)**. 이 **효과크기 20× 격차**가 가장 강한 정직한 진술이며,
Part1의 'α-robust / lag-fragile'을 **후성유전 baseline feature 축에서 독립 재확인**한다.
단 **confound 통제(A4)에서 α의 예측력은 대부분 baseline 발현 + gene 길이에서 오고**(R²_base=0.320),
**히스톤 활성마크의 incremental 기여는 ΔR²=0.016에 그친다** → 주장은 "**α는 baseline-예측가능, lag은 아니다**"이지
"히스톤 활성마크가 α를 설명한다"가 **아니다**.

---

## 1. 데이터·feature (GSE70677 Human CD34+ HSPC, hg19)
feasibility gate(2026-07-13 GEO 실측)로 GSM→(세포·마크) 대응 확인 후 사용:

| feature 소스 | GSM | 상태 |
|---|---|---|
| H3K4me3 (promoter) | GSM1816326 | ✅ SICER island BED4(chrom,start,end,score), hg19, 48,022 island |
| H3K4me1 (enhancer) | GSM1816327 | ✅ 90,544 island |
| H3K27ac (active prom/enh) | GSM1816328 | ✅ 26,932 island |
| CpG island promoter class | UCSC hg19 cpgIslandExt | ✅ 30,344 island |
| **HSPC input BED** | GSM1816325 | ⛔ **BLOCKED** (supp=NONE). island은 이미 SICER FDR0.01로 input 대비 유의 → 별도 input 정규화 불가(한계로 명시) |
| **CAGE (TSS 개시강도·shape)** | GSM1816314 | ⛔ **BLOCKED** (supp=NONE, raw SRA만) → CAGE_init/CAGE_shape feature 미생성 |
| **독립 baseline_expr (RNA)** | GSM1582706~08 | ⛔ **BLOCKED**: Affymetrix HG-U133 CEL(microarray), cms-r에 affy/hgu133plus2.db 부재 → **GSE209878 day0 HSC/MPP 발현으로 대체**(same-dataset; §5 caveat) |

- gene 축 조인: gencode **v19(hg19)** gene-SYMBOL ↔ velocity fit gene(GSE209878). liftOver 회피.
- feature 행렬: **1,111 gene × 9 feature**(`features_hspc.csv`). promoter=TSS±2kb, enhancer=2kb<|d|≤50kb distal.
  `me3_prom, ac_prom, me3_breadth, ac_enh, me1_enh, n_links, cpg_prom, baseline_expr, gene_length_log10`.
  (H3K27me3 부재 → **bivalency/poising 축은 스코프 밖**, 설계 §8.)

## 2. 타깃 (GSE209878 Part1 consensus, `targets_alpha_lag.csv`)
percentile-rank 평균 consensus(스케일 상이 → median 아님). clean-gate 규율: **MultiVelo lag은 크기(magnitude) rank만**, sign 미사용.
- `alpha_consensus`(≥2 method, n=604) — α percentile-rank 평균.
- `lag_consensus`(≥2 method, n=640) — lag **크기** percentile-rank 평균.
- `lag_reprod`(≥3 method, n=582) — lag 크기 rank의 method간 SD의 음수(높을수록 재현적).

**타깃 sanity(Part1 신호 승계 확인):** α cross-method Spearman **+0.882**(mv×vae)/+0.818/+0.889 = FINDINGS ρ0.88 재현.
lag 크기 cross-method **−0.05~+0.16**(near-zero) = lag-fragile 재현. → consensus 타깃이 Part1의 두 leg를 충실히 운반한다.
> ⚠️ `lag_consensus`는 서로 거의 무상관(ρ≈−0.05..0.16)인 method들을 평균한 **본질적으로 잡음 큰 타깃**이다 —
> 낮은 예측력은 부분적으로 타깃 자체의 비일관성을 반영한다(그 자체가 lag-fragile 서사이나 명시함).

## 3. A1~A4 결과 (`model_results.csv`, `deltaR2_A4.csv`)
GroupKFold(5, group=chrom, 24 그룹) OOF. permutation: A1~A3 = y 전역 shuffle N=1000(EN); A4 = chromatin block row-permute N=1000(base-y 보존).

| 분석 | 타깃 | n | R²(EN) | Spearman(EN) | p(EN) | R²(GBM) | Spearman(GBM) |
|---|---|---|---|---|---|---|---|
| **A1** α 설명 | alpha_consensus | 550 | **0.337** | 0.572 | **0.001** | **0.365** | 0.597 |
| **A2** lag 설명(대조) | lag_consensus | 574 | **0.017** | 0.143 | 0.002 | **−0.038** | 0.150 |
| **A3** lag 재현성 | lag_reprod | 533 | **−0.003** | −0.041 | 0.36 | −0.189 | −0.073 |

**A4 nested ΔR² (chromatin | baseline_expr + gene_length):**

| 타깃 | R²_base | R²_full | **ΔR²(chromatin)** | p |
|---|---|---|---|---|
| α (alpha_consensus) | **0.320** | 0.337 | **+0.016** | 0.001 |
| lag (lag_consensus) | −0.008 | 0.017 | +0.025 | 0.001 |

## 4. 해석 (정직)
- **A1 vs A2 = 핵심 dissociation (model-robust):** 선형·비선형 두 모델 모두 α는 예측(0.34/0.37)하고 lag은 못 한다(0.017/−0.04).
  이 **효과크기 격차**가 결정적 진술이다. ⚠️ A2 p=0.002는 "유의"이나 R²=0.017은 **자명(trivial)** — p가 아니라 효과크기로 읽어야 한다.
- **A4가 α 주장을 tempering한다:** α 예측력은 대부분 baseline 발현+gene 길이(R²_base=0.320)에서 오고, **히스톤 마크 incremental은 ΔR²=0.016**.
  → "히스톤 활성마크가 α를 설명한다"가 **아니라** "α는 baseline-예측가능(주로 발현/길이), lag은 아니다"가 맞는 진술.
- **어느 feature가 그 작은 증분을 만드나:** ElasticNet α 모델은 **promoter 활성마크(me3_prom, ac_prom)를 0으로 소거**했다(발현 공변량과 강상관 → 탈락).
  작은 chromatin 증분은 **enhancer 아키텍처**(n_links +0.020, me1_enh +0.006, cpg_prom −0.017)에서 온다 — canonical 'active promoter'가 아니다.
- **lag ΔR²=0.025 > α ΔR²=0.016 wrinkle (설명 없이 그대로 보고):** 위협 아님 — (a) base R² 0.320 vs −0.008이라 ΔR² 비교 불가(lag은 빈 방이 컸을 뿐),
  (b) GBM lag은 음수라 미corroborate, (c) 절대 lag 예측력은 여전히 자명(0.017). **weak≠zero 정직 원칙**: lag의 유일한 baseline 신호는
  GBM이 뒷받침 못 하는 약한 선형 chromatin-architecture 연관뿐이다.
- **A3 — lag 비재현은 노이즈-유사:** baseline 크로마틴은 "어디서 lag이 재현되는지"를 예측 못 한다(R²<0, p=0.36; GBM −0.19).
  → lag 비재현은 baseline 크로마틴에 각인된 **조건부 실신호가 아니라 노이즈에 가깝다**. ⚠️ 단 lag_reprod는 3~4 method-rank의 SD인 **잡음 큰 타깃** →
  이 null은 잘 측정된 타깃의 null보다 **약한 증거**다 → "노이즈-유사와 consistent"이지 "증명"이 아니다.

## 5. 한계 (정직)
1. **baseline_expr가 α와 same-dataset**: 독립 microarray 경로 BLOCKED → GSE209878 day0 발현 사용. 발현은 dynamical α 추정에 **정의상 부분 결합** →
   R²_base=0.320은 그 결합으로 **부풀려짐** → chromatin ΔR²=0.016은 **보수적 하한(floor)**. 독립 발현 공변량이면 base/chromatin 분할이 달라질 수 있다.
2. **input·CAGE·독립 RNA BLOCKED**(§1) → 설계 §2b feature 중 CAGE onset·input 정규화 미구현.
3. **bulk-population(HSPC/MPP/EPP) 해상도**: 단일세포 아님 → gene별 baseline feature로만(세포아형 분해 불가).
4. **bivalency 불가**: H3K27me3 없음 → poising/bivalent 축 유보(BLUEPRINT/Roadmap 페어링 시에만).
5. **상관≠인과**: perturbation 없음 → 설명/예측만 주장. 인과는 Part2(약물) 영역.
6. **parquet 엔진 부재**(어느 env에도 pyarrow/fastparquet 없음) → 산출은 CSV(`features_hspc.csv`, `targets_alpha_lag.csv`; 내용 동일).
7. gencode v19 SYMBOL 조인: velocity 1,228 gene 중 TSS 매칭 1,111 → 심볼 불일치/멀티매핑 gene 손실.

## 6. 결정 문장 (velocity-trust 결정지도 확장, EXPLORATORY)
> "동일 baseline feature로 **α는 선형·비선형 모두 예측(R²=0.34/0.37)** 하나 **lag은 둘 다 못 함(R²=0.017/−0.04)** →
> α는 baseline에 예측가능한 실질 kinetic, lag의 방법의존성은 측정 취약성(baseline 크로마틴에 각인된 조건부 신호도 아님, A3).
> 단 α 예측력은 주로 baseline 발현·gene 길이이며 히스톤 활성마크의 incremental 기여는 작다(ΔR²=0.016, enhancer 아키텍처 중심).
> (bivalency 축은 H3K27me3 부재로 유보; ΔR²는 발현-α same-dataset 결합으로 보수적 하한.)"

## 7. 재현 (결정론적)
```
conda run -n scv-preprocess python scripts/step2_features.py   # → features_hspc.csv (1111×9)
conda run -n scv-preprocess python scripts/step2_targets.py    # → targets_alpha_lag.csv (+ Part1 sanity ρ)
conda run -n scv-preprocess python scripts/step2_models.py     # → model_results.csv, deltaR2_A4.csv, feature_importance.csv
```
seed=20260713, NPERM=1000(EN)/200(GBM). ⚠️ GBM permutation p는 음수 R²에서 아티팩트(순열 모델이 더 음수일 뿐) → 예측력 근거로 **미사용**, R²만 보고.
