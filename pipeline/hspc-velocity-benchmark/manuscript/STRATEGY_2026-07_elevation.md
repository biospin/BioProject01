# BIOP01 논문 격상 전략 (2026-07-12)

> BIOP02(SpatialPathoAgent)의 07-11~12 방법론 템플릿을 BIOP01에 이식해 논문 급을 올리는 전략. advisor 압박검증 + SNR 검정(`results/identifiability_vs_snr.md`)으로 방어 가능선까지 벼림.
> 이 문서는 "무엇을 왜 주장하는가"의 권위 요약. 확정 아님 — 사용자·GSE205117 결과로 갱신.

## 0. BIOP02에서 이식한 템플릿
BIOP02는 "H&E로 분자예측"(레드오션)을 **"H&E가 분자검사를 언제 대신하나"의 사전등록 법칙 + 결정지도**로 격상. 이식할 무기:
1. **사전등록 falsifiable 명제**(결과 전 commit 해시 봉인) — 사후서술→사전예측.
2. **2층 프레임워크 절대 융합 금지**.
3. **반증기준 명시 + 사후 구제 금지**.
4. **교차-시스템 복제가 최강 검정**.
5. **해석수준 방어**(주장 층위를 명확히 해 후속 고해상 기술에 반증 안 되게).
6. AI/파이프라인 = 인프라이지 기여 아님.

## 1. 한 문단 요지
RNA velocity로 chromatin→transcription **lag**(활성화 시간차)을 정량하는 시도가 늘지만, 우리는 **lag가 계산 method를 바꾸면 재현되지 않는(cross-method ρ≈0)** 반면 **전사속도 α는 튼튼함(ρ≈0.88)**을 5개 시스템에서 보인다. 핵심은 두 층위의 분리다: 한 method **안에서** lag가 잘 fit돼 확신 있어 보여도(within-method fit), method **간** 신뢰성(cross-method reproducibility)은 없다. 이로부터 velocity 출력의 **신뢰 결정지도**(무엇을 믿고 무엇을 직교검증해야 하나)를 제시한다.

## 2. 방어 가능선 — SNR 검정이 그은 경계 (중요)
격상 후보였던 **"식별가능성(profile-likelihood 곡률)이 SNR을 넘어 재현성을 예측한다"는 discovery급 법칙**은 **폐기**. 근거(SNR 검정, N=537):
- ρ(κ_lag, 재현불일치)=−0.14(약함), nkeep(depth) 통제 후 −0.07(붕괴), 곡률↔depth 공선성 0.58.
- → 여기서 "sloppy"는 사실상 "저SNR/저depth". "곡률=그냥 SNR" 리뷰 공격이 성립 → 법칙 격상은 방어 불가.
- **이 검정을 미리 한 게 핵심 이득**: 방어 불가한 재프레이밍에 논문을 걸지 않음.

## 3. 채택 — 방어 가능한 격상 (현행 벤치마크 > 이것 > 방어불가 법칙)
### 핵심 기여
1. **재현성 격차** — α robust / lag fragile. per-gene도 확인(lag 불일치 0.317 vs α 0.078). 탄탄한 경험적 코어.
2. **2층 구분(저평가된 진짜 포인트)** — within-method **fit 자신감** ≠ cross-method **신뢰성**. 데이터 있음. "한 파이프라인이 준 lag 확신을 재현성으로 착각 말라."
3. **velocity 신뢰 결정지도** — α·rate=신뢰 / lag·절대 timing=불신(직교검증 필요) / direction-sign=구조적 편향. 필드 실용 기여.
4. **정직한 메커니즘** — lag는 두 switch-time의 **차이**라 구조적 저SNR + sloppy(둘 얽혀 분리 불가). §8은 이 얽힘을 정직하게 서술(식별가능성 SNR 초월 주장 X). 상한 fixed 3.53×/94.57%·기준 freed 2.49×/77% 안에서.
5. **cost 프레이밍(경량)** — lag를 믿으면 downstream(epigenetic drug-timing, 원 목표)이 method-arbitrary해짐. 결과의 실질 대가.

### 버림
- ❌ 식별가능성 "법칙" 격상(위 §2). ❌ AI 결정레이어 이식(BIOP02엔 on-thesis, 우리엔 scope bloat).

## 4. GSE205117 (5번째 시스템) 역할
- **사전등록 복제**: priming 극대(gastrulation)에서도 α robust/lag fragile 순서가 유지되는지 **결과 전 봉인**해 검정. 사전등록 표=`manuscript/PREREGISTRATION_gse205117.md`.
- **정직 표기**: 이는 이미 4번 본 순서의 **5번째 확증(confirmatory)**이지 discovery 아님(advisor). "priming best-case에서도 fragile"이 헤드라인 강화점.
- 반증기준: 만약 gastrulation에서 lag가 재현(cross-method ρ≥0.5)되면 "priming best-case" 주장 실패 → 정직 보고, 사후 구제 X.

## 5. 두 층위 (융합 금지) — 표 골격
- **표1 재현성**: method 간 α ρ vs lag ρ (5 시스템).
- **표2 신뢰 결정지도**: velocity 출력별 신뢰등급(α/rate=high, lag/timing=low, sign=biased) + 권장 조치(직교검증 필요 여부).
- 두 값을 하나로 합치지 않음(fit 자신감을 신뢰로 승격 금지 = BIOP02의 층위오류 방지 대응).

## 6. 선택지 (비용 명시)
- **현행(4-vs-4 + §8)**: 즉시 출판 가능, 탄탄.
- **격상(§3)**: 천장 ↑, scope는 결정지도·2층 프레이밍만큼만 ↑(SNR 리스크는 §2로 제거됨).
- **권장**: §3 채택. 특히 저비용·고효과 = **2층 프레이밍 + 신뢰 결정지도 + GSE205117 사전등록 복제**.

## 7. 정직한 한계 (원고 명시)
- 식별가능성은 SNR과 얽혀 분리 불가(§2) — "곡률이 근본 원리"로 과주장 X.
- freed-nuisance: α 곡률도 β/γ 자유화 시 0.19× 붕괴(조건부). fixed는 상한.
- skin(#5)은 DEFER(velocity 신호 약함), GSE205117로 대체.
- hypothesis-level: drug-timing 응용은 wet-lab 검증 필요(feasibility만).
