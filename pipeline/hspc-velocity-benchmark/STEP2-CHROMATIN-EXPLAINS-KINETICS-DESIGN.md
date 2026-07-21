# STEP 2 설계 — "baseline 크로마틴 활성마크가 *재현되는 α*를 설명하고 lag은 왜 취약한가"

> 상태: **미커밋·설계(protocol)**. 박상준 Week 7 Step 2를 우리 중심 발견(α 재현/lag 비재현) 위에서 재정의. 실행 전 팀·박상준 검토.
> 상위 맥락: [WEEK7-PARK-DESIGN-GAP-REVIEW.md](WEEK7-PARK-DESIGN-GAP-REVIEW.md) (A). 엄밀성 규약 승계: `DESIGN.md`·`PAPER-PLAN.md §4·§5`·repo `CLAUDE.md`.

## 0. 한 줄 목표
GSE70677(Human CD34+ HSPC 히스톤 ChIP-seq + CAGE)에서 gene별 baseline **크로마틴 활성 feature**를 만들고, Part 1의 두 kinetic 타깃(**α=재현 ρ0.88 / lag=비재현 ρ0.04**)에 **각각** 회귀해서 "무엇이 α를 설명하나 / lag은 왜 설명 안 되나(=노이즈인가 조건부 신호인가)"를 정량으로 답한다. **약물 데이터 불필요, 인간 HSPC 동일 세포계에서 지금 실행 가능.**

## 1. 왜 이 형태인가 (척추)
박상준 원 Step 2는 "chromatin feature로 **lag**을 예측"이었다. 그러나 Part 1이 **lag은 방법 바꾸면 안 재현(ρ0.04)** 임을 보였으므로, lag을 예측 타깃으로 삼으면 "노이즈를 예측"하는 꼴이 된다. → 타깃을 **재현되는 α로 옮기고**, lag은 **"왜 취약한가"의 대상**으로 강등해 대조군으로 쓴다. 이 대조(같은 feature로 α는 설명되고 lag은 안 됨)가 **velocity-trust 결정지도의 후성유전적 근거**가 된다.

## 2. 입력

### 2a. 타깃 (Part 1 산출물 = GSE209878 HSPC)
- **α_gene**: gene별 전사율. **방법 간 robust 합의값**(교차방법 median 또는 rank-consensus). Part 1의 재현 신호(ρ0.88)를 대표하도록 정의. 소스=`results/`의 method별 α → consensus 산출.
- **lag_gene**: gene별 chromatin→transcription lag **합의값**(비재현). + method별 원값 유지.
- **lag_reprod_gene**: gene별 **교차방법 일치도**(예: method쌍 lag의 SD 또는 Kendall 국소일치) — A3의 타깃.
- 필터: 충분 세포·발현되는 gene만(Part 1 QC 승계). pseudotime 단위 lag 주의(≠wall-clock).

### 2b. Feature (GSE70677, gene-level, **HSPC 집단=baseline**)
| feature | 소스(GSM) | 정의 |
|---|---|---|
| promoter H3K4me3 | GSM1816326 | TSS±2kb island 신호/피크폭 |
| promoter/enhancer H3K27ac | GSM1816328 | TSS±2kb + gene-linked enhancer |
| enhancer H3K4me1 | GSM1816327 | ±50kb 또는 peak-to-gene 링크 enhancer |
| input(정규화) | GSM1816325 | 배경 |
| CAGE TSS 사용량·프로모터 shape | GSM1816314 | 개시 강도 + broad/sharp(TSS 분산) = onset 직교 프록시 |
| baseline 발현 | GSE70677 RNA(HSPC A/B/C) | **통제 공변량**(핵심) |
| CpG density·promoter class | genome annot(hg19) | CpG island 프로모터 여부 |
| peak-to-gene linkage 수 | 위 피크+annot | gene당 링크 enhancer 개수 |
- 데이터 형식: **SICER island peak BED(hg19), GSM별 supplementary** — 원시 재처리 불필요.
- (옵션) HSPC→MPP→EPP 분화축의 mark 변화량 = "동역학" feature(2차; 우선 HSPC baseline만).

## 3. Feature 추출 파이프라인 (concrete)
1. **획득**: HSPC 마크 4개(H3K4me3/me1/H3K27ac/input)+CAGE_HSPC+RNA를 GSM supplementary에서 다운(§7).
2. **유전자 좌표(hg19)**: GENCODE hg19(v19 등)에서 TSS·gene body. **BED 전부 hg19라 liftOver 불필요**(피크→gene 배정은 hg19 내에서).
3. **피크→gene 배정**: promoter=TSS±2kb 겹침; enhancer=gene body±50kb 또는 활성 피크의 nearest-gene/링크. 마크별 신호=island score 합 또는 피크폭(정규화는 input 대비 + 총 island 길이).
4. **CAGE**: TSS clustering → gene별 초기화 강도, 프로모터 shape(IQR of TSS).
5. **feature 행렬**: gene × {H3K4me3, H3K27ac_prom, H3K27ac_enh, H3K4me1, CAGE_init, CAGE_shape, CpG_class, n_links, baseline_expr}. log/quantile 정규화, 강상관→그대로 두되 모델은 regularized.
6. **gene축 조인**: GSE70677(gene symbol/Ensembl hg19) ↔ 타깃(GSE209878 gene symbol) **심볼/Ensembl 기준 조인**(좌표 liftOver 회피). 교집합 gene만.
7. 산출: `results/step2/features_hspc.parquet`, `targets_alpha_lag.parquet`.

## 4. 모델·분석
- **A1 — α 설명**: `α ~ features`. Elastic Net(선형) + GBM(비선형). **염색체 단위 hold-out CV**(누출차단). permutation null로 유의성. 산출=R²·feature importance.
- **A2 — lag 설명(대조)**: `lag ~ 같은 features`. **예상 R²≪A1.** 같은 feature로 α는 설명되고 lag은 안 됨 → "α가 실질 신호"의 후성유전 근거.
- **A3 — lag이 노이즈인가 조건부신호인가**: `lag_reprod ~ features`. 크로마틴이 **어디서 lag이 재현되는지**(예: sharp H3K4me3 프로모터=안정 lag) 예측하면 lag=조건부 실신호; 못 하면 lag≈노이즈. 어느 쪽이든 결론.
- **A4 — confound 통제(필수)**: baseline 발현·gene 길이·세포수·(가능시 mRNA decay 프록시)를 base로, **크로마틴의 incremental ΔR²**(nested: base vs base+chromatin) 보고(PAPER-PLAN §4 승계). "크로마틴이 발현을 다시 잰 것"으로 환원 방지.

## 5. 엄밀성 게이트 (승계)
염색체/계통 hold-out · permutation FDR · 강상관 regularize · pseudotime≠wall-clock · **상관≠인과**(예측만 주장) · 결정론적 재계산 + Critic pass(repo CLAUDE.md).

## 6. 산출물·결론 형태
- feature 행렬·모델 결과·**feature importance 그림**.
- **결정 문장(velocity-trust 결정지도 확장)**: "동일 baseline 크로마틴 활성마크가 **α는 ΔR²=__로 설명**하나 **lag은 설명 못 함(R²≈0)** → α는 후성유전에 각인된 실질 kinetic, lag의 방법의존성은 측정 취약성. (bivalency 축은 H3K27me3 부재로 유보.)"

## 7. 데이터 획득 (명령 스케치)
```bash
# HSPC 히스톤·CAGE·input (GSM supplementary BED/CAGE), hg19
for g in 1816325 1816326 1816327 1816328 1816314; do
  base="ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM${g%???}nnn/GSM${g}/suppl/"
  wget -q -r -np -nd -A "*.gz" "$base" -P data/gse70677/GSM${g}/
done
# GENCODE hg19 gene annotation (TSS/gene body)
# → features_hspc.parquet 생성 (peak→gene 배정 스크립트)
```
(RNA-seq HSPC A/B/C = GSM1582706~08.)

## 8. 한계·리스크 (정직)
- **bivalency 불가**: H3K27me3 없음 → poising/bivalent 축은 별도 소스(BLUEPRINT/Roadmap CD34+ H3K27me3) 페어링 시에만. 미페어링이면 "활성마크만"으로 스코프 명시.
- **bulk-population 해상도**: 단일세포 아님 → gene별 baseline feature로만(세포상태 해상도 없음). 타깃(단일세포 α/lag)과 해상도 불일치 = feature는 population-baseline, 타깃은 gene-level 요약이라 **gene 축에서 조인은 타당**하나 세포아형별 분해는 불가.
- **hg19 vs (타깃 게놈)**: gene-symbol 조인으로 회피하되 심볼 불일치/멀티매핑 gene 손실 보고.
- **α consensus 정의 의존**: A1 결과가 α 대표값 선택에 민감 → 여러 정의로 민감도 분석.
- **상관≠인과**: perturbation 없음 → "설명/예측"만. 인과는 Part 2(약물) 영역.

## 9. 다음 결정 (팀)
- [ ] 박상준 원의도 확인: Step 2 타깃을 α로 옮기는 재프레이밍 동의?
- [ ] bivalency 위해 H3K27me3 소스(BLUEPRINT CD34+) 추가 여부.
- [ ] 실행 주체=`hspc-velocity-analyst` 에이전트에 위임 여부(feature 추출→A1~A4).
