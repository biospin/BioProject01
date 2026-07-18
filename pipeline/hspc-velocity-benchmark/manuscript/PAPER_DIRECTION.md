# 논문 방향 (Paper Direction) — 하네스 단일 권위 컨텍스트

> **모든 논문 하네스 멤버(novelty-strategist·literature-scout·research-methodologist·manuscript-writer·paper-critic·reviewer)가 작업 시작 전 반드시 읽는 단일 소스.** "무엇을 왜 주장하는가 + 어떤 규율로 검증하는가"를 한눈에. 매번 재브리핑 불필요 — 이 문서가 최신 상태를 담는다.
> 갱신: **2026-07-18** (novelty 적대적 판정 + make-or-break 결과 반영, 아래 §5 참조). 세부=`STRATEGY_2026-07_elevation.md`, 사전등록=`PREREGISTRATION_gse205117.md`, 검정=`../results/identifiability_vs_snr.md`, 스쿱=`SCOOP-CHECK-2026-07.md`, novelty=`NOVELTY-EXTENSIONS.md`.

## 1. 현재 thesis (한 문장) — 2026-07-18 재프레이밍(음성→양성 헤드라인)
계산 method를 바꾸면 chromatin-transcription **lag**은 재현되지 않고(cross-method ρ≈0, 5 시스템) 전사속도 **α**는 재현된다(ρ≈0.88). **나아가 목적함수 곡률(내부 식별성)이 어느 velocity 출력이 외부 측정으로 검증되는지를 예측한다** — 강성 랭킹 **α ≫ α_c > β > γ**(전 pairwise p<1e-11)에서 최고 stiff **α는 실측 TT-seq 합성율을 회복**하고 최저 sloppy **γ는 실측 분해율에 역방향**. 이로부터 **측정-앵커된 velocity 신뢰 지도**를 제시한다.
> 리드 전환: 심사자에겐 "lag 재현 실패"(음성)가 아니라 **"곡률이 측정검증을 예측한다"(양성·제1원리)**를 앞세운다(적대적 판정 R-1/R-2 대응).

## 2. 방어 가능한 claim-set (등급 표기 — 하네스는 이 등급을 지킨다)
| claim | 등급 | 근거 | 반증기준 |
|---|---|---|---|
| lag cross-method/dataset 비재현, α 재현 | **CONFIRMED** | §7, 4-vs-4 + per-gene | lag ρ≥0.5면 실패 |
| **곡률(내부 식별성)이 외부 측정검증을 예측**(α stiff→합성율 회복, γ sloppy→분해율 역방향) | **STRONG** (make-or-break A 통과, 강성랭킹 α≫α_c>β>γ 전 pairwise p<1e-11; advisor 대기) | `results/stiffness_predicts_validation.md` + `external_rate_validation.md` | α/γ 외부측정 순서가 강성 순서와 어긋나면 약화. ⚠️ 직접 외부측정은 α·γ뿐(α_c·β는 내부순위만) |
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

### 이전 (2026-07-12~15)
- ✅ 4-vs-4 확증 + §8(SNR-bounded) + 방어가능선 전략 봉인(커밋 d52416c).
- ✅ 5번째 GSE205117(gastrulation) 완주 — 사전등록 6/0 PASS(MoFlow arm 원정의 재채점, 커밋 9eb0b76). 본문·Table1 반영.

## 6. 정직한 한계 (본문 명시)
식별가능성-SNR 분리 불가 / freed-nuisance 조건부(α 곡률도 0.19× 붕괴) / skin DEFER / drug-timing은 design principle(wet-lab 미검증) / cross-dataset α gradient는 n=3 confounded라 headline 금지(categorical 대비만).
