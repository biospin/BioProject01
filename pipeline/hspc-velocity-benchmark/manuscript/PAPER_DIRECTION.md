# 논문 방향 (Paper Direction) — 하네스 단일 권위 컨텍스트

> **모든 논문 하네스 멤버(novelty-strategist·literature-scout·research-methodologist·manuscript-writer·paper-critic·reviewer)가 작업 시작 전 반드시 읽는 단일 소스.** "무엇을 왜 주장하는가 + 어떤 규율로 검증하는가"를 한눈에. 매번 재브리핑 불필요 — 이 문서가 최신 상태를 담는다.
> 갱신: 2026-07-12. 세부=`STRATEGY_2026-07_elevation.md`, 사전등록=`PREREGISTRATION_gse205117.md`, 검정=`../results/identifiability_vs_snr.md`, 스쿱=`SCOOP-CHECK-2026-07.md`, novelty=`NOVELTY-EXTENSIONS.md`.

## 1. 현재 thesis (한 문장)
계산 method를 바꾸면 chromatin→transcription **lag**은 재현되지 않고(cross-method ρ≈0, 5 시스템) 전사속도 **α**는 재현된다(ρ≈0.88) — 그리고 한 method **안**의 fit 자신감 ≠ method **간** 신뢰성. 이로부터 velocity 출력의 **신뢰 결정지도**를 제시한다.

## 2. 방어 가능한 claim-set (등급 표기 — 하네스는 이 등급을 지킨다)
| claim | 등급 | 근거 | 반증기준 |
|---|---|---|---|
| lag cross-method/dataset 비재현, α 재현 | **CONFIRMED** | §7, 4-vs-4 + per-gene | lag ρ≥0.5면 실패 |
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

## 5. 진행 상태 (2026-07-12)
- ✅ 4-vs-4 확증 + §8(SNR-bounded) + 방어가능선 전략 봉인(커밋 d52416c).
- 🔄 5번째 GSE205117(gastrulation) 다운·GEX 처리 밤샘 자율. 사전등록 6예측 봉인 완료 → 결과를 대조.
- ⏳ 다음: ATAC 처리 → 다method concordance → 사전등록 대조 → (통과 시) 본문에 5번째 확증 반영.

## 6. 정직한 한계 (본문 명시)
식별가능성-SNR 분리 불가 / freed-nuisance 조건부(α 곡률도 0.19× 붕괴) / skin DEFER / drug-timing은 design principle(wet-lab 미검증) / cross-dataset α gradient는 n=3 confounded라 headline 금지(categorical 대비만).
