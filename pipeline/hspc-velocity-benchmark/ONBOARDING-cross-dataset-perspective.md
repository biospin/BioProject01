# BIOP01 velocity 벤치마크 — 온보딩 & 4개 데이터셋 적용 관점

> 작성: 김가경 · 대상: cross-dataset 담당자 및 이 벤치마크를 이어받거나 참고할 분
> 목적 ① HSPC(4개 데이터셋 중 1개)에서 진행한 작업을 5분 안에 파악하고, ② 같은 방법이
> 나머지 3개 데이터셋에서 **어떤 관점으로 쓰이는지** 잡는 것. 세부 수치와 해석은
> `results/FINDINGS.md`가 canonical 기준입니다.

---

## 1. 30초 요약

- **하는 일**: 단일세포 multiome에서 유전자별 **크로마틴→전사 lag**을 정량하고, 그것을 baseline
  후성유전 feature로 삼아 **약물 반응 timing 예측**으로 잇는 것이 최종 목표입니다.
- **먼저 검정한 것**: "그 lag이 애초에 method-robust한 양인가?"를 정면으로 물었고, 답은 **아니다**였습니다.
  method를 바꾸면 lag의 크기도 방향도 재현되지 않습니다(4-way 비교 + permutation FDR로 확증). 대신
  **robust한 것은 전사율 α(method 간 ρ=0.88)와 "day0 ATAC 접근성 → α" 경로(held-out 예측 ρ=+0.31)**였습니다.
- **완료한 범위**: **Human HSPC (GSE209878)**, 4개 데이터셋 중 1개. P0~P5 파이프라인 전체.
- **지금 필요한 것**: 이 결론을 **외부 데이터셋으로 재현**하는 것(P5 replication). 나머지 3개가 그 역할을 맡습니다.

---

## 2. 무엇을 했나 — HSPC 파이프라인 한눈에

같은 전처리에서 출발해 여러 velocity method로 각각 lag을 뽑고, 그 값들이 서로 얼마나 일치하는지(H1)를
검정하는 구조입니다.

| 단계 | 한 일 | 핵심 산출 |
|---|---|---|
| **P0** | GSE209878 다운로드·sha256 고정·라이선스·provenance | `P0_provenance.md` |
| **P1** | 통일 전처리(공통 세포/유전자/그래프) → 21,878 세포 MuData, 7 lineage | `P1_README.md` |
| **P2** | RNA-only floor(scVelo) + MultiVelo + MultiVeloVAE + MoFlow + CRAK-Velo + **scrambled 음성대조** | `results/*_genes.csv` |
| **P3** | cross-method lag 일치도(H1) + confound(cell-cycle/burst/doublet) | `concordance.md`, `confound.md` |
| **P4** | permutation FDR(N=10⁴) | `permutation_fdr.md` |
| **P5** | robustness 3각(accuracy sim / bootstrap / 예측) + per-lineage refit + **진짜 day0 ATAC feature** | `lineage_refit.md`, `atac_baseline_features.md`, `lag_model_atac.md` |

**핵심 결과 세 줄**

1. cross-method lag은 크기가 서로 무상관이고(ρ≈−0.04~+0.12) 방향은 ~50/50이라, **비robust**합니다.
   agreement-set은 0/598 유전자.
2. 음성대조에서 ATAC를 셔플해도 MultiVelo lag이 그대로였습니다 → lag은 크로마틴이 아니라 **모델 구조**에서
   나옵니다.
3. 반전은, **전사율 α는 robust**(ρ=0.88)하고 **day0 ATAC로 예측된다**(ρ=+0.31)는 점입니다. 반면 lag은
   ATAC로도 예측되지 않습니다(≈chance).

> 프레이밍 유의: 여기서 "비robust"는 **cross-method**를 뜻합니다 — method를 바꾸면 lag이 재현되지 않는다는
> 의미이며, 단일 파이프라인 *안*에서의 lag 예측(원 논문 방식)과는 서로 양립합니다.

---

## 3. 어디부터 보면 되나 (읽는 순서)

리더나 신규 담당자 기준의 권장 진입 순서입니다.

1. **`results/FINDINGS.md`** — 결과와 해석을 모은 canonical 종합본. **이 문서 하나로 전체 그림이 잡힙니다.**
2. **`DESIGN.md`** — 왜 이 method들을, 어떤 confound 통제 아래 골랐는지(설계 근거, v2).
3. **`results/concordance.md`** — H1(cross-method 일치도) 수치의 원본.
4. **이 문서 §4** — 그래서 다른 데이터셋에서 무엇을 하는지.
5. (실무 착수 시) **`cross_dataset/RUNBOOK.md`** — 새 데이터셋 실행 절차와, 아직 남은 gap의 정직한 목록.

근거 레이어가 더 필요하면 `paper_analysis/epigenomic-lag/`에 MultiVelo·MoFlow·CRAK-Velo·MultiVeloVAE
원논문의 dual-lens 분석이 정리되어 있습니다.

---

## 4. ★ 이 방법이 4개 데이터셋에서 쓰이는 "관점"

### 4.0 핵심 통찰 — 우리 4개 = MultiVelo 원논문의 4개

우연이 아닙니다. 하네스의 4개 데이터셋은 **MultiVelo 원논문이 검증에 사용한 바로 그 4개**입니다.

| 하네스 데이터셋 | accession | 원논문에서의 역할 |
|---|---|---|
| Human HSPC 10x Multiome | GSE209878 | 조혈 계층 복원 + histone mark 외부검증 |
| SHARE-seq mouse skin | GSE140203 | **"chromatin potential"(priming) 최초 정량** — priming의 best case |
| Human brain multiome (fetal cortex) | GSE162170 | TF→motif accessibility lag + disease SNP timing |
| 10x embryonic mouse brain | 10x 공개 | method 기본 동작 검증(backflow 제거), cell-cycle 많음 |

곧, **method 로직(통일 전처리 → 다중 method → cross-method 일치도 → confound/FDR → 예측)은 그대로 전이**됩니다.
데이터셋마다 바뀌는 것은 *biology*(세포종·marker·분화 축)뿐입니다. 그래서 **각 데이터셋은 같은 파이프라인을
다른 생물학 위에서 돌려, 우리 결론을 다른 각도에서 압박(stress-test)하는 역할**을 합니다.

### 4.1 공통 관점 — 모두 "H1 네거티브 결과의 외부 재현"

가장 중요한 공통 역할은, **"lag은 cross-method로 비robust하다"가 HSPC만의 특성인지 아니면 일반적 현상인지**를
가려 주는 것입니다.

- 다른 조직에서도 method를 바꿀 때 lag이 재현되지 않는다면 → **강한 일반 방법론 주장**이 되어, 단일
  데이터셋이라는 이유의 desk-reject를 방어할 수 있습니다.
- 반대로 어떤 데이터셋에서는 lag이 robust하다면 → 그 *이유*가 곧 새로운 발견입니다(예: 단방향 분화계에서는
  α_c가 안정적인가?).
- 성공기준(단일 replication): method 순위와 lag-sign 패턴이 HSPC와 재현되는가. `RUNBOOK §7`의 Spearman
  게이트(|r|>0.3)로 확인합니다.

### 4.2 데이터셋별 관점 (각자 다른 것을 압박)

**① SHARE-seq mouse skin — "priming best case + 플랫폼 일반화"**

- 원논문에서 priming("chromatin potential")이 **가장 뚜렷했던** 데이터셋입니다(M1 66.6% vs M2 1.0%,
  거의 단방향 분화 TAC→hair shaft). 크로마틴 선도 신호가 **가장 강하게 기대되는** 곳입니다.
- 관점: *이곳에서도* cross-method lag이 비robust하다면 → "priming이 뚜렷한 계에서조차 lag은 method-민감"이라는,
  우리 주장의 가장 강한 확증이 됩니다. 반대로 이곳에서 robust하다면 → **단방향·priming이 강한 계에서는 lag이
  살아남는다**는 경계조건의 발견입니다(이 역시 좋은 결과).
- 보너스: **SHARE-seq는 10x Multiome이 아니므로**, 전처리 파이프라인이 플랫폼을 넘어 일반화되는지도 함께
  검증됩니다.
- ⚠️ marker 재정의 필수: keratinocyte/hair-follicle 계열(HSPC 조혈 marker는 무의미).

**② Human brain multiome / fetal cortex — "cross-modality lag + 같은 species"**

- 원논문에서 **TF 발현 → motif accessibility → target gene**의 다단계 lag과 disease SNP timing을 낸
  데이터셋입니다. transient TF cascade가 많아 lag의 정의가 가장 풍부하면서도 까다로운 계입니다.
- 관점: "α는 robust, lag는 fragile"이라는 분리가 **neuron/glia 분화**에서도 유지되는가. TF cascade가 많으면
  lag이 더 흔들릴 것으로 예상되므로, 우리 결론과 정합할 가능성이 큽니다.
- 보너스: **human**이라 HSPC와 유전자 축(gene ID)이 직접 겹칩니다 → cross-dataset lag rank 비교가 mouse보다
  깔끔합니다(ortholog 매핑 불필요).
- ⚠️ marker 재정의: RG/IPC/ExN/interneuron/OPC 등.

**③ 10x embryonic mouse brain — "cell-cycle stress-test + method 기본검증"**

- 원논문의 "일단 작동하는가"를 확인한 기본 데이터셋입니다. **cycling RG가 많아 cell-cycle confound가 가장
  강한** 계입니다.
- 관점: HSPC에서 내린 **"cell-cycle은 gene 수준에서 비편향이고 within-lineage로 통제된다"**는 판단이,
  cell-cycle이 더 심한 계에서도 성립하는지 직접 검증합니다. M1/M2 균형도 재확인합니다.
- ⚠️ marker 재정의 + cross-species(mouse) 유전자 축 매핑.

### 4.3 drug-timing(Part 2)과의 관계 — 정직하게

- **나머지 3개 데이터셋은 주로 Part 1(방법 일반화·외부재현)에 기여**합니다. 약물 예측(Part 2)의
  ground truth(약물 timecourse)는 이 데이터셋들에 없습니다.
- Part 2로 직접 이어지는 것은 **HSPC 계열(조혈/백혈병) 페어링**뿐입니다(mRNA 반감기 차용 gate는
  `proxy_join_gate.md`에서 PASS). 뇌·피부는 대응되는 후성유전 약물 timecourse가 확보될 때에 한해 Part 2로
  확장합니다.
- 결국 3개 데이터셋의 가치는, **"우리 방법(ATAC→α는 robust, lag는 fragile)이 조직을 넘어 일반적이다"**를
  세워 Part 2의 일반화 주장을 뒷받침하는 데 있습니다.

---

## 5. 새 데이터셋 착수 시 — 실무 3-gap (RUNBOOK 요약)

"데이터만 받으면 바로 실행"은 **아직 아닙니다.** 스캐폴드(`cross_dataset/`)에 먼저 처리해야 할 gap이 남아
있습니다(안전장치로, `run_all.sh`는 gap이 해결되지 않으면 실행을 거부해 HSPC 결과 덮어쓰기를 막습니다).

1. **배선 gap**: `p1/p2/p3`가 `config`를 하드코딩하고 있습니다 → `CROSS_DATASET_CONFIG` env로
   `config_<dataset>.py`를 주입하고, 산출물에 dataset suffix를 붙입니다(`multivelo_genes_<dataset>.csv`).
2. **domain annotation gap (근본)**: `LINEAGE_MARKERS`/`QC`/`RARE_LINEAGES`가 **HSPC 조혈 전용**입니다.
   모든 지표가 within-lineage라 **marker가 틀리면 replication 자체가 무의미**해집니다 → 조직·species에 맞게
   재정의가 필수입니다.
3. **데이터 형식 확정**: raw CellRanger ARC vs 처리된 h5ad(옵션 A/B).

착수 순서: `RUNBOOK.md §0 체크리스트` → `§1 데이터` → `§2 config` → `§3~5 P1/P2/P3` → `§7 해석 게이트`.

---

## 6. 정직한 현재 상태 / 열린 것

- **완료**: HSPC P0~P5 본체 + 4-way H1 + permutation FDR + day0 ATAC 예측 경로.
- **열린 QC 항목**: 세포 수가 재전처리 21,878 vs 원논문 11,605으로 차이가 있습니다 — 임계값 검토가 필요하며,
  덮지 않고 기록해 둡니다.
- **cross-dataset 코드**: 아직 설계 스캐폴드 상태입니다(위 3-gap). 데이터가 도착하면 gap을 처리한 뒤
  실행합니다.
- **Part 2(약물)**: HSPC 페어링 경로만 열려 있고(반감기 차용 gate PASS), timecourse 데이터 확보가 다음
  관문입니다.

문의처: 세부 수치는 `results/FINDINGS.md`, 실행 절차는 `cross_dataset/RUNBOOK.md`, 설계 근거는 `DESIGN.md`.
