# Cross-Dataset External Replication — 실행 상태 (LIVE)

---

## §0. 이 작업이 무엇이고 어디서 나왔나 (canonical, 2026-07-09) — 팀 공유용

> **한 줄:** cross-dataset 재현은 **원래 계획의 일부가 아니라, lag이 예상과 다르게 나와서 파생된 확장 분석(extension)**이다.
> 결과 근거의 canonical 원천은 `../results/FINDINGS.md`, 절차는 이 폴더 `RUNBOOK.md`.

### (1) 원래 분석 계획 (original plan)
gene별 **chromatin→transcription lag**(activation/shutdown 시점차)을 정량 → baseline epigenomic feature로
**epigenetic drug-response timing** 예측. 1차 데이터셋 = Human HSPC 10x Multiome(GSE209878).
전제 검정으로 velocity method head-to-head 벤치마크를 돌려 **"lag이 method-robust한 양인가"(H1)**를 먼저 본다.
→ **암묵적 기대: lag은 튼튼한(재현되는) 양이다**(priming이 실재하니 측정 가능한 안정된 시점차가 있으리라).

### (2) 예상과 다른 결과 (the pivot) — 확장의 방아쇠
**lag은 method-robust하지 않았다.** cross-method 크기 일치 |ρ|≤0.08, 부호 일치 48%≈우연, permutation-FDR
방향 일관 유전자 **0/598**. 반면 **전사율 α는 튼튼**(cross-method ρ=**0.88**) + day0 크로마틴으로 held-out 계통
예측 가능(ρ=**+0.31**). → "lag robust" 기대가 깨짐. **이 예상외 결과가 아래 확장 분석 전부를 촉발했다.**

### (3) 파생된 확장 분석 (extensions — 원래 계획에 없던 부분, 전부 이 pivot에서 나옴)
| 확장 | 왜 (예상외 결과에 대한 대응) | 산출 |
|---|---|---|
| **E1. 5중 자기검증** | "lag 비robust가 우리 실수/아티팩트 아닌가?" 배제 | `clean_concordance_gate.md`·`permutation_fdr.md`·`confound.md`·`crakvelo_sign_check.md`·(반감기 관문) |
| **E2. cross-dataset 재현** | "α>lag 순서가 HSPC 우연 아니라 조직·종 넘어 유지되나?" | `concordance_{human_brain,e18_mouse_brain,GSE194122_bmmc}.md` (+ 진행 중) |
| **E3. profile-likelihood 식별성** | "왜 lag이 fragile한가?" → 목적함수 성질로 승격 | `profile_likelihood_identifiability.md` (α stiffer 94.57%, κ비 median 3.53×) |
| **E4. drug-timing 타깃 전환** | 원래 목표를 lag이 아니라 **α**로(day0 ATAC→α) 재정렬 | `atac_baseline_features.md`·`lag_model_atac.md`, FINDINGS §6 |

→ **git 커밋도 이 흐름의 챕터다:** `P3 cross-dataset #N …`(E2) · `P3 profile-likelihood …`(E3) · `P3 외부 kinetic 검증 …`(E1/E4) 접두 커밋들이 각 확장에 대응. FINDINGS 발견별 §1~§8이 같은 순서.

### (4) 지금 cross-dataset(E2) 작업 분담 — **여기가 지용기(BIOP01-29) 혼동 지점**
heavy-run과 downstream을 나눈다. **핵심: heavy-run은 kkkim 몫, downstream이 모집(BIOP01-29) 몫.**

| 단계 | 무엇 | env/자원 | 담당 | 산출 |
|---|---|---|---|---|
| **heavy-run (fit 생산)** | build→floor→MultiVelo→VAE(→MoFlow)→P3 | kkkim 홈 conda env(scv-preprocess/mv/torch) + GPU — **kkkim 서버에서만 가능** | **kkkim이 이 서버에서 구동** | `results/{multivelo,rna_only,multivelovae}_genes_<dataset>.csv` |
| **downstream (BIOP01-29)** | concordance(α vs lag ρ)·bootstrap CI·해석 | **CPU만**, env 셋업·GPU·heavy-run **불필요** | **모집(지용기)** — kkkim fit CSV 위에서 | `results/concordance_<dataset>.md` |
| critic (BIOP01-39) | 결론·통계·hedge 점검 | — | 모집 | 리뷰 코멘트 |

- ⚠️ **BIOP01-29 본문의 "처리해야 할 2가지(config 파라미터화·LINEAGE_MARKERS 재정의)"는 이미 완료됨** — cross-dataset #1~4가 `CROSS_DATASET_CONFIG`/`CROSS_DATASET_SUFFIX` env 배선을 이미 쓴다(아래 §wiring). 모집자가 새로 할 필요 없음.
- 팀 공유 GPU env(다른 계정에서 heavy-run 하려면 필요)는 이건규 님께 별건 요청(비긴급). 현 분담대로면 **지용기 님은 env 없이 kkkim fit을 기다렸다 CPU 분석만** 하면 됨.

### (5) 데이터셋 상태 (2026-07-10 갱신)
| # | 데이터셋 | Accession | fit(heavy-run) | downstream(concordance) | cross α / lag |
|---|---|---|---|---|---|
| 1 | human fetal cortex | GSE162170 | ✅ | ✅ `concordance_human_brain.md` | +0.475 / +0.19 |
| 2 | E18 mouse brain | 10x embryonic | ✅ | ✅ `concordance_e18_mouse_brain.md` | +0.32 / +0.10 |
| 3 | human BMMC | GSE194122 | ✅ | ✅ `concordance_GSE194122_bmmc.md` | +0.55 / +0.05 |
| 4 | **macrophage 분화** | GSE284047 / figshare 30280333 | ✅ (kkkim, 2026-07-09) | ✅ `concordance_macrophage.md` (지용기, BIOP01-29) | **+0.643** / +0.148 |
| — | ~~mouse skin~~ | GSE140203 (SHARE-seq) | ❌ **NO-GO 확정** (velocity 신호 부족, 아래) | 해당 없음 | — |
| **5** | **mouse gastrulation** (대체 채택) | **GSE205117** (PRJNA843939) | 🔄 preflight **GO 확정** → full-B(4시점) 다운·GEX STARsolo 진행 중 (kkkim) | ⏳ 대기 (지용기, **BIOP01-41**) | — |

> **#5 skin NO-GO 확정 (2026-07-11) — 사유 정정에 주의.**
> ❌ **틀린 사유**: "SRA에 barcode read 부재". 이건 STARsolo-from-FASTQ 경로에서 나온 판정인데, 그 경로 자체가 잘못이었다(SHARE-seq 3×8bp 비연속 barcode에 `CB_UMI_Simple` 연속 파라미터 → **거짓 NO-GO**). `FEASIBILITY_shareseq_skin.md`가 경고한 함정에 실제로 빠진 사례.
> ✅ **맞는 사유**: 정본 경로(velocyto-on-BAM, 저자 BAM, barcode read-이름 선디코딩)를 **완주했고 barcode는 정상**(0 skip, 50,671 cells)·**GTF 정합도 정상**(mm10 chr-prefixed 일치). 그럼에도 **spliced nnz 0.02% / unspliced 0.03%**(chr1 희석 보정해도 ~0.56%), per-cell spliced ~14.5 → **velocity 신호 자체가 얕다.** 게다가 unspliced > spliced로 3′ 화학의 정상 패턴과 어긋난다. → **데이터 품질 사유의 NO-GO**(우리가 못 해서가 아님). Methods에 이 사유로 기재.
>
> **⚠️ 방법론 교훈 (다른 데이터셋에도 적용):** **nnz 절대 임계(macrophage 35.6%)는 depth-confounded** — 서브셋·부분 염색체엔 그대로 쓰면 안 된다(GSE205117 20M 서브셋에서 실제로 거짓 NO-GO를 유발할 뻔함). feasibility 판정 지표는 **unspliced/spliced 비율(건강 범위 ~0.3–0.4) + barcode 매칭률 + mapping률**로 본다. nnz는 **같은 depth끼리만** 비교.
>
> **#5 대체 = GSE205117 (mouse gastrulation E7.5–8.75, ~59k cells).** 10x Multiome이라 skin 실패요인이 전부 해소된다: R1 = 16bp CB + 12bp UMI(**연속**) + R2 90bp cDNA → STARsolo `CB_UMI_Simple`+`Velocyto` 직산출.
> preflight 실측: **barcode 유효 100% · genome mapping 95.1% · unspliced/spliced 0.388(건강)**, nnz는 20M→60M에서 2.2배 비례 상승 → 낮은 nnz가 depth 아티팩트임을 입증. **GO 확정.**
> mouse이므로 cross-dataset은 E18과 동일한 uppercase ortholog 매핑 재사용.
> **결과는 `manuscript/PREREGISTRATION_gse205117.md`의 봉인된 6개 예측에 그대로 대조한다(사후 구제 금지).** 채점기 = `p3_prereg_gse205117.py`.

**순서 보존 요지:** 값 자체는 조직이 멀수록 α가 순서대로 낮아진다(macrophage +0.643 > BMMC +0.55 > brain +0.475 > E18 +0.32 — macrophage가 HSPC 직계 조혈축이라 최고). 반면 **lag은 어디서도 무신호(+0.05~+0.19)** → "α robust / lag fragile"가 데이터셋 넘어 보존.

> ⚠️ **정직 caveat (macrophage)**: cross lag +0.148의 bootstrap 95%CI는 [+0.027, +0.263]로 ±0.2를 벗어나 **TOST 등가는 아니다**("약한 양수"). 헤드라인 주장은 등가가 아니라 within-dataset **Δρ dissociation** (ρ_α−ρ_lag = **+0.843**, 95%CI [+0.773, +0.912], 0 제외)이므로 서사는 영향받지 않는다. `concordance_macrophage.md` §B·caveat 참조.

---

> ⚠️ **아래 배너/이하 절은 2026-07-05 human_brain 무인 드라이버 시절 실행 이력**이다(위 §0가 최신·정본). "커밋 안 함/무인 push 금지"는 이후 **작업 브랜치 자동 커밋 정책으로 대체**됨(CLAUDE.md). 절차·wiring 세부는 여전히 유효.

> ## ⏭️ 재로그인 시 (2026-07-05 13:35 갱신) — 🤖 무인 드라이버가 관장 중, 수동 개입 금지
> **⛔ 절대 MultiVelo/P3를 수동 재실행하지 말 것.** `run_crossdataset_autonomous.sh`가 detached(PPID=1, 로그아웃 생존)로 돌며
> MultiVelo 풀런 완료 대기 → 죽으면 자동 재실행(최대 3회) → 완료 시 P3 concordance까지 자동 수행한다. 수동 실행하면 **중복 실행**된다.
> - **상태 한눈에**: `cat cross_dataset/AUTOPIPE_PROGRESS` (poll마다 갱신 heartbeat). 완료=`cross_dataset/AUTOPIPE_DONE` 생성, 실패=`AUTOPIPE_FAILED`.
> - **드라이버 생존 확인**: `pgrep -af run_crossdataset_autonomous`. 로그=`cross_dataset/driver.log`.
> - 진행 이력:
>   - ✅ **RNA-only floor** — `results/rna_only_dynamical_genes_human_brain.csv` (824 gene, velocity_genes=388).
>   - ✅ **MultiVelo 스모크(--genes 20)** — 15/20 수렴, fit+SUFFIX 게이트 검증. `multivelo_genes_human_brain.smoke.csv`.
>   - 🔄 **MultiVelo 풀런** — 802 gene MV_CHUNK=50씩. → `results/multivelo_genes_human_brain.csv` (완료 시).
>   - ⏭️ **P3 cross-dataset concordance** (자동) — `scripts/p3_crossdataset_concordance.py`: HSPC↔human_brain lag크기 rank Spearman(headline)+timing.
>      HSPC-vs-HSPC self-test(rho=1.0)·smoke 교집합 실측 검증 완료. → `results/concordance_human_brain.md`. 성공기준 |r|>0.3.
> - **드라이버가 죽었고 AUTOPIPE_DONE도 없을 때만** 재기동: `cd cross_dataset && setsid bash run_crossdataset_autonomous.sh </dev/null >driver.log 2>&1 &` (idempotent — csv 있으면 P3로 바로 넘어감).
> **환경 주의**: floor·P3는 `scv-preprocess`(HSPC와 동일 env=공정 비교), MultiVelo만 `mv`.
> **커밋 안 함** — 사용자 복귀 후 수동. (무인 push 금지)

> **마지막 갱신:** 2026-07-05
> **배경:** 담당 조율 결과 — 박상준 님이 "kkkim 직접 데이터 분석 진행해도 된다" 허락, 전연수 님 무응답.
> → **kkkim이 자율적으로 공개 데이터 다운로드·전처리 진행**하기로 결정 (블로커 없음).
> 이 결정과 진행이 이전 세션에서 기록 없이 중단됨 → 본 문서가 canonical 진행판.

---

## 타깃 데이터셋 (우선순위)

| # | 데이터셋 | Accession | 종류 | 공개 형식 | 상태 |
|---|---|---|---|---|---|
| 1 | **human fetal cortex** | GSE162170 (Trevino 2021, Cell) | human multiome | ✅ processed matrix (**spliced/unspliced 제공**) | **다운로드 완료** |
| 2 | mouse skin | GSE140203 (SHARE-seq, Ma 2020) | SHARE-seq | ⚠️ `GSE140203_RAW.tar`만 (spliced/unspliced 없음 → raw 처리 필요) | 후순위(heavy) |
| 3 | mouse brain | 10x embryonic (미확정 accession) | 10x multiome | 미확인 | 후순위 |

**우선순위 근거:** GSE162170만이 (a) human이라 HSPC와 gene ID 축 직접 겹침(ortholog 불필요),
(b) 공개 supplement에 spliced/unspliced counts 직접 제공 → velocyto/BAM 재처리 불필요.
→ **human brain을 depth-first로 end-to-end(변환→P2→concordance) 완주**해 wiring을 검증하면 나머지 2개가 재사용.

## GSE162170 다운로드 완료 파일 (`data/human_brain/`)
- `GSE162170_multiome_rna_counts.tsv.gz` (24M)
- `GSE162170_multiome_spliced_rna_counts.tsv.gz` (11M) ← spliced
- `GSE162170_multiome_unspliced_rna_counts.tsv.gz` (15M) ← unspliced
- `GSE162170_multiome_atac_counts.tsv.gz` (150M) ← peak counts (sparse 로드 필수)
- `GSE162170_multiome_atac_consensus_peaks.txt.gz`
- `GSE162170_multiome_cell_metadata.txt.gz`
- `GSE162170_multiome_cluster_names.txt.gz`
- (미다운로드/선택) `..._atac_gene_activities.tsv.gz` (832M) — **사용 안 함**: provider gene-activity를 쓰면
  method와 preprocessing이 confound. HSPC와 동일한 peak→gene 집계를 우리가 수행.

---

## 파이프라인 인터페이스 (코드 실측 — RUNBOOK보다 우선)

- `p1_build.py` → `import p1_config`, `p2_multivelo.py` → `import p2_config`, `p3_concordance.py` → `import p1_config, p2_config`.
- **RUNBOOK의 `--config`/`--dataset` argparse는 실재하지 않음.** config는 모듈명 `p1_config`로 하드코딩 import.
- `p2_config`의 입력/출력 경로는 전부 `p1_config`에서 파생(IN_RNA=p1.OUT_RNA, ...). → **주입 지점 = p1_config**.
- human brain은 processed spliced/unspliced 보유 → **P1(CellRanger ARC + velocyto loom) 건너뜀(RUNBOOK option B)**,
  대신 tsv → `data/processed_human_brain/{rna_spliced_unspliced,atac_peaks}.h5ad` 직접 생성.

## 실행 계획 (human brain)
- [x] domain gap 처리: `config_human_brain.py` (cortical marker/QC 재정의 완료)
- [x] GSE162170 multiome 다운로드
- [x] **변환** (`build_human_brain.py`): tsv → `rna_spliced_unspliced.h5ad`(8981×32581, X=spliced+unspliced, layers spliced/unspliced, symbol축) + `atac_peaks.h5ad`(8981×467315 peak-level sparse). RNA var_names unique 처리(중복 19).
- [x] **검증**: RNA↔ATAC obs_names 동일, 전부 finite, spliced nnz 2.5%/unspliced 3.8%.
- [x] **wiring gap 처리 (①③)**: `scripts/p1_config.py`에 `CROSS_DATASET_CONFIG` env override 블록 추가(env 미설정 시 HSPC byte-identical) + `p2_config.SUFFIX`(=`CROSS_DATASET_SUFFIX`) → p2_multivelo/p2_rna_only 출력명 suffix. **⚠️ PYTHONPATH shim은 실패**(`python script.py`가 script 디렉터리를 sys.path[0]로 먼저 잡아 무력화) → env 방식으로 확정. `run_all.sh` 대신 `CROSS_DATASET_CONFIG=... CROSS_DATASET_SUFFIX=_human_brain` 직접 지정.
- [x] **P1-equivalent finalize** (`finalize_human_brain.py`, **완료** 2026-07-05): QC(mito≤15/genes/Singlet) → counts layer → normalize_total(1e4)+log1p → HVG(2000) → PCA(30)+neighbors(30) → leiden → cortical lineage annotation. + **ATAC peak→gene 집계**(gencode v44 gene body ±10kb, GSE162170이 10x peak_annotation 미제공 → mv.aggregate_peaks_10x 불가 대체) → `atac_gene.h5ad`. config OUT_ATAC를 atac_gene.h5ad로 변경.
  - **산출 실측**: `rna_spliced_unspliced.h5ad` 8414×32581 (QC 8981→8414), layers=counts/spliced/unspliced, leiden+lineage 존재 — lineage: ExN 5014 / InN 1693 / RG 1172 / OPC 275 / Cycling 209 / Microglia 51. `atac_gene.h5ad` 8414×22432 (cell 정합).
- [ ] **P2 full**: RNA-only floor(`rna_only_dynamical_genes_human_brain.csv`) + MultiVelo(`multivelo_genes_human_brain.csv`, ~2h CPU)
- [ ] **P3 concordance**: HSPC vs human_brain switch_time rank (Spearman, RUNBOOK §7 style) → `results/concordance_human_brain.md`

## wiring 실행 명령 (확정)
```bash
cd pipeline/hspc-velocity-benchmark/scripts
CROSS_DATASET_CONFIG=../cross_dataset/config_human_brain.py CROSS_DATASET_SUFFIX=_human_brain \
  HDF5_USE_FILE_LOCKING=FALSE conda run --no-capture-output -n velo-mv python -u p2_rna_only.py    # floor
#   ...p2_multivelo.py 도 동일 env로. 출력은 자동으로 *_human_brain.csv (HSPC 결과 보호).
```

## 알려진 함정 (advisor)
1. **mouse concordance**: `hspc.index ∩ new.index`가 mouse는 case 불일치(`Gata1`≠`GATA1`)로 ~0 → ortholog/case 매핑 선행 필수. human brain은 무관.
2. **ATAC**: provider gene_activities 쓰지 말고 HSPC와 동일 peak→gene 집계. 150M ATAC counts는 sparse 로드.
3. **foreign spliced/unspliced 주입**: dataset 내부 method 비교는 동일 입력 공유라 무편향. cross-dataset per-gene concordance엔 noise만 추가 → "lag fragile" 결론에 보수적. OK.
