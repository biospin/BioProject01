# 논문 방향 (Paper Direction) — 하네스 단일 권위 컨텍스트

> **모든 논문 하네스 멤버(novelty-strategist·literature-scout·research-methodologist·manuscript-writer·paper-critic·reviewer)가 작업 시작 전 반드시 읽는 단일 소스.** "무엇을 왜 주장하는가 + 어떤 규율로 검증하는가"를 한눈에. 매번 재브리핑 불필요 — 이 문서가 최신 상태를 담는다.
> 갱신: **2026-07-18** (novelty 적대적 판정 + make-or-break 결과 반영, 아래 §5 참조). 세부=`STRATEGY_2026-07_elevation.md`, 사전등록=`PREREGISTRATION_gse205117.md`, 검정=`../results/identifiability_vs_snr.md`, 스쿱=`SCOOP-CHECK-2026-07.md`, novelty=`NOVELTY-EXTENSIONS.md`.

## 1. 현재 thesis (한 문장) — 2026-07-18 재프레이밍 (곡률 헤드라인 시도→기각, 결정지도로 리포지셔닝)
계산 method를 바꾸면 chromatin-transcription **lag**은 재현되지 않고(cross-method ρ≈0, 5 시스템) 전사속도 **α**는 재현된다(ρ≈0.88). **α는 method 재현성에 더해 실측 TT-seq 합성율에도 앵커되는(외부 검증) 유일한 rate**이고, lag·γ는 method-fragile이며 외부 측정도 회복 못 한다(γ는 심지어 역방향). 이로부터 **측정-앵커된 velocity 신뢰 결정지도**(어느 출력을 믿고 어느 출력은 직교검증이 필요한지)를 제시한다 — 이것이 헤드라인.
> **곡률→측정검증 헤드라인은 시도했다가 기각**(2026-07-18): 파라미터 내·유전자 간 tertile 검정(`results/curvature_tertile_validation.md`)에서 α는 예측 방향 경향(최고강성 분위 ρ=+0.30, CI 0배제)이나 high−low 차이 미유의(검정력 부족), γ는 gradient 없음. → **곡률→검증은 supporting/suggestive로 강등**, 결정지도가 헤드라인. (advisor 게이트: n=2 일화를 법칙으로 relabel 금지.)

## 2. 방어 가능한 claim-set (등급 표기 — 하네스는 이 등급을 지킨다)
| claim | 등급 | 근거 | 반증기준 |
|---|---|---|---|
| lag cross-method/dataset 비재현, α 재현 | **CONFIRMED** | §7, 4-vs-4 + per-gene | lag ρ≥0.5면 실패 |
| ~~곡률(내부 식별성)이 외부 측정검증을 예측~~ | **DEMOTED → suggestive supporting** (헤드라인 기각 2026-07-18) | tertile 검정 `results/curvature_tertile_validation.md` | **파라미터 내·유전자 간(n=210/201) 검정 결과: α는 예측방향 단조 경향(최고강성 분위 ρ=+0.30 CI 0배제, low 미검증)이나 ρ_high−ρ_low 미유의(검정력부족); γ는 강성-검증 gradient 없음(flat null). 헤드라인의 γ역방향(−0.224)은 scVelo γ였고 곡률 측정 method(MultiVelo)와 불일치. → "곡률→검증"은 supporting 관찰로만, 헤드라인 아님.** |
| **α만 cross-method 재현(0.88); lag·γ는 fragile** → velocity 출력 신뢰 결정지도 | **STRONG (헤드라인)** — 단 leg는 ①재현성 순서 ②인과대조(lag=shuffle불변)로 한정 | §7 cross-method + `scrambled_null.md` | α 재현이 무너지거나 lag가 shuffle에 깨지면 약화 |
| ~~α가 외부 합성율에 앵커된 *유일* 출력~~ → **corroboration으로 강등** (2026-07-19, BIOP01-54) | **DEMOTED** | `results/coupling_lag_alternative.md` | **head-to-head: 발현량이 α보다 synth 더 잘 예측(abundance 0.41 > α 0.26); synth=abundance×k_deg라 당연. 결정진단: α↔abundance 0.80 < cross-method α 0.88 → α는 발현풀과 완전히 같진 않으나(재현 kinetic 소량) 대부분 겹침. ⚠️ 제목/초록 "the only externally anchored output" 방어불가 → 변경. 외부측정은 '일관성 증거'로만.** |
| lag 대체(모델-free 크로마틴-RNA 결합) | **REJECTED as headline** (supporting만) | `coupling_lag_alternative.md` | 인과대조 통과(shuffle하면 붕괴, lag과 대비)·최근접 lineage(macrophage +0.28)만 재현·BMMC/brain 미재현 → 재현 가능 대체 아님 |
| ~~named marker는 chromatin이 lag을 **인과** 결정(Medium-High)~~ → **상관만** | **DOWNGRADED (2026-07-18)** | make-or-break #1 marker-shuffle teeth **NULL** (marker |Δlag| ≈ bulk, MW p=0.58; `results/marker_shuffle_teeth_test.md`) | marker의 method 간 *방향* 일치는 유지, **인과 함의는 뺀다** |
| within-method fit자신감 ≠ cross-method 신뢰성 (2층) | **STRONG** | per-gene 불일치 데이터 | fit 좋은 유전자가 재현도 잘되면 약화 |
| velocity 신뢰 결정지도(α/rate 신뢰·lag/timing 불신) | **STRONG** | 위 두 개에서 도출 | — |
| lag는 저SNR+sloppy(식별가능성 얽힘) | **BOUNDED** | §8 곡률, 단 SNR과 분리 불가(검정) | — |
| ❌ "식별가능성이 SNR 넘어 재현성 예측"(법칙 격상) | **REJECTED** | SNR 검정 ρ=−0.14·depth통제 붕괴 | 폐기 — 사전등록·본문에 쓰지 않음 |
| ❌ AI/파이프라인이 기여 | **REJECTED** | 인프라이지 기여 아님(BIOP02 원칙) | — |

## 3. loop-engineering 규율 (하네스 표준 — 자동 적용)
> 오늘(2026-07-12) identifiability 격상이 SNR 검정으로 반증된 사례가 이 규율의 근거. framing을 lock하기 전 반드시 통과.

1. **claim-defensibility 게이트 (핵심 신설)**: 모든 headline/novelty claim은 lock 전 3종 세트를 갖춰야 한다 — ① **반증기준**(무엇이 관측되면 틀린가), ② **가장 값싼 make-or-break 검정**(기존 데이터 우선), ③ **advisor 확인**. 검정 통과 전엔 등급 **PROVISIONAL**, 본문·사전등록에 쓰지 않는다.
2. **피드백 루프**: 검정 결과가 claim을 반증/약화하면 → 등급을 내리고 이 문서 §2 표를 즉시 갱신(사후 구제 금지). 반증을 반증으로 보고.
3. **사전등록**: 확증용 신규 데이터(예: GSE205117)에 대한 예측은 **결과 산출 전 commit 해시로 봉인**. 임계값 사후 조정 금지.
4. **2층 융합 금지**: fit 품질(within)을 재현성(cross)으로 승격하지 않는다. 표1(재현성)·표2(신뢰지도)를 하나 숫자로 합치지 않는다.
5. **SOTA 대비**: 약한 내부 baseline 아닌 최강 공개 도구를 bar로(novelty-strategist 규율 유지).
6. **숫자 규율**: 결과파일·검증 base만, bootstrap CI+검정, pseudotime≠wall-clock, permutation FDR, lag sign 구조적 양수(무정보).

## 4. 표 골격 (융합 금지)
- **표1 재현성**: 5 시스템 cross-method α ρ vs lag ρ.
- **표2 velocity 신뢰 결정지도**: 출력별 신뢰등급(α/rate=high, lag/절대timing=low, sign=biased) + 권장 조치(직교검증 필요 여부).

## 5. 진행 상태

### 2026-07-18 결정 (novelty 적대적 판정 후)
- **적대적 심사(GB) 판정**: 현 draft는 **~75~85% reject 위험** — "음성/부분재현 감사 + 얇은 양성"으로 읽힘. 정직한 base-case venue = **Cell Reports Methods**, GB는 stretch. (kkkim 결정: **A 결과로 재프레이밍 후 GB 도전**, 재검토.)
- ✅ **make-or-break A 통과(양성 헤드라인 확보)**: profile-likelihood를 α_c·β·γ로 확장(`p5_stiffness_all_params.py`) → **곡률이 외부 측정검증을 예측**(α≫α_c>β>γ, p<1e-11; α 회복·γ 역방향). 커밋 69861b8. → §1 thesis·§2 표 갱신.
- ❌ **make-or-break #1 실패(marker-shuffle teeth NULL)**: 셔플이 named marker lag을 bulk보다 더 안 흔듦(MW p=0.58) → "marker 인과" 주장 **하향**(§2). 핵심 음성결론은 더 깨끗해짐.
- ❌ **"크로마틴-제어-α 유전자 지도"는 별도 논문 불가(현 데이터로)**: 유일 약물데이터(AG-120)가 타임스케일 불일치(5d/14d vs 시·분 기전)라 α/접근성/lag 전부 null(정보적 아님). Enrichr 응집성 약함(inflammatory/signaling). → **methods 논문의 응용 예시로만**, "올바른 타임스케일 perturbation이 다음 실험"으로 명시. (`stiffness_predicts_validation.md`, `marker_shuffle_teeth_test.md`)

### 2026-07-18 (추가) — advisor 게이트가 A 헤드라인 기각, 결정지도로 리포지셔닝
- **make-or-break A 재검정 실패**: advisor가 "곡률→검증 make-or-break가 잘못된 축(파라미터 간 랭킹, 외부앵커 n=2)을 쟀다"고 지적 → 파라미터 내·유전자 간 tertile 검정(`p6_curvature_tertile_validation.py`, `results/curvature_tertile_validation.md`). 결과: **α 예측방향 경향이나 미유의(검정력부족), γ flat null, 헤드라인 γ역방향은 scVelo(method 불일치)**. → 곡률→검증 **헤드라인 기각·supporting 강등**.
- **헤드라인 = 측정앵커 velocity 신뢰 결정지도**로 되돌림(§1). manuscript 재작성은 이 기준. **A 기반 프리프린트/블로그7 헤드라인 보류** — 블로그7 초안은 게시 전 하향 필요.
- 규율 확인: claim-defensibility 게이트가 실제로 작동(make-or-break 통과처럼 보였으나 advisor가 축 오류 포착 → 본문 미반영으로 방어).

### 2026-07-19 — 층② 세포×유전자 velocity 행렬 감사(BIOP01-59) → NEGATIVE, supporting 편입
- **범위 확장의 근거**: "감사 대상이 per-gene 모수라 velocity의 실제 용도가 아니다"는 반론이 리뷰어 1번 공격 지점 → 한 층 위(세포×유전자 행렬)를 실제로 쟀다. 사전등록 봉인(`PREREGISTRATION_velocity_matrix.md`) 후 실행.
- **결과 NEGATIVE — 사전 대조 2종 모두 실패**: (A) multiome끼리 −0.139 < RNA-only 기준선 +0.080(paired Δ −0.206, 예상과 반대) (B) MultiVelo 원본×ATAC셔플 +0.732(중심화 +0.838) = 안 무너짐. **재적합 천장 +0.872**가 "지표가 무딘 게 아니라 실제 불일치"를 확정.
- **주장 등급**: supporting. **헤드라인 승격 없음** — 동결 헤드라인(신뢰 결정지도)을 한 층 넓힐 뿐. 인과 관련 진술은 재적합 대조군을 가진 **MultiVelo 한정**(MoFlow는 seed 재실행 대조 부재).
- ⚠️ **2026-07-20 정정(BIOP01-59 계열 supporting sub-claim)**: 위 (B)에서 끌어냈던 **"크로마틴은 velocity 행렬에 인과적으로 무력하다"를 철회한다.** 천장(재표집 15,315 cell)과 셔플(전량 21,878 cell)의 세포집합이 어긋난 비교였고, 같은 세포집합 S_b에서 짝맞춰 재적합하면 셔플 값이 온전한 범위 아래로 3/3 내려간다(+0.784·+0.813·+0.810 대 +0.826~+0.887, CI 3/3 비중첩; `results/velocity_matrix_paired_shuffle.md`). **양성 단정도 금지** — 같은 세포·같은 설정 run-to-run 귀무가 없어 짝지은 Δ(+0.081·+0.004·+0.063, 하나는 사실상 null)는 크로마틴 기여와 재적합 잡음의 합이다. 허용 서술은 "무력하다고 더는 단정할 수 없다 / 나타나는 곳에서도 작다 / method 선택이 만드는 불일치(−0.530~+0.131)보다 훨씬 작다"까지. **Abstract 무수정**(층① per-gene lag 대상의 인과 문장과는 별개 사안이라 혼동 금지). 반영 = draft_v2/ko Results·Methods, `velocity_matrix_audit.md` §0·§1·§4·§5-2·§6.
- **선결 게이트 통과**: [12,13] 전문 확인(`NOTE_benchmarks_12_13_scope_check.md`) — 둘 다 임베딩·전이 벡터 수준 채점이며 **행렬의 method 간 비교도, 인과 chromatin 대조군도 없다**. [12]는 ATAC 없이 MultiVelo를 rna_only로 실행. [13]은 행렬을 seed 안정성에만 사용. 우리 결과는 중복도 모순도 아니며, [12]의 A1<0.3(전이 벡터 수준 저일치)과 같은 방향이다.
- **draft 반영(영/한 동시)**: Results 새 소절 1개 + Methods 소절 1개 + Discussion scope 문장 정밀화(주장 #4: "세포 수준 벡터 미감사" → "행렬은 감사, 임베딩 화살표는 범위 밖") + Positioning 보강 + refs [12,13] 서지 확정 + Additional file 12. **Abstract는 손대지 않는다**(승격 방지).
- ⚠️ **금지**: "평활되면 겉보기 궤적은 비슷할 것"이라는 도피구 — [12]가 전이 벡터 수준에서도 저일치를 보고하므로 자기 인용에 반박당한다. 남는 여지는 정성적 흐름선까지.

### 이전 (2026-07-12~15)
- ✅ 4-vs-4 확증 + §8(SNR-bounded) + 방어가능선 전략 봉인(커밋 d52416c).
- ✅ 5번째 GSE205117(gastrulation) 완주 — 사전등록 6/0 PASS(MoFlow arm 원정의 재채점, 커밋 9eb0b76). 본문·Table1 반영.

## 6. 정직한 한계 (본문 명시)
식별가능성-SNR 분리 불가 / freed-nuisance 조건부(α 곡률도 0.19× 붕괴) / skin DEFER / drug-timing은 design principle(wet-lab 미검증) / cross-dataset α gradient는 n=3 confounded라 headline 금지(categorical 대비만).
