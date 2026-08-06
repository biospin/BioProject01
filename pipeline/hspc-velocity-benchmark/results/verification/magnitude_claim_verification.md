# 검증 기록 — lag magnitude 재현성 헤드라인 (AKM WEEK 03 과제1·과제2 적용)

> 대상 claim: draft_v2 Table 1 각주 †·L69 clean headline. **위험 Tier 3**(투고·공개). CANONICAL_WRITER 1명(kkkim 세션).
> 이 기록은 검증·보고만 한다. 원고(`draft_v2.md`/`draft_v2_ko.md`)는 이 검증으로 수정하지 않는다(NO_CHANGE).
> 규율: `manuscript/VERIFICATION_PROTOCOL.md`. 러너(과제2 자동화): `scripts/verify_manuscript.py`.

---

## 과제2 — Baseline 동결 (실제 도구, PHASE 0·1)

- 검증 대상(baseline artifact) = 원고 정본. 실제 `sha256sum` 결과:
  - `manuscript/draft_v2.md`     sha256 = `94a9f03d95c8058f3e4a648bb2a688245d513eecd3efadbc2aaaaa61bc4a58ef`
  - `manuscript/draft_v2_ko.md`  sha256 = `5f94d633317277fa702f4c52e02bc7addf0ff7ef2b5ba3d93a076804262e4732`
  - git HEAD = `cf93245`
- allowed source files (직접 read): `manuscript/draft_v2.md`(L69·L144), `results/identifiability_dissociation.md`, `results/concordance.md`.
- forbidden scope: 원고 수정(검증만), 외부 공개, 민감정보. required output = 이 기록 파일.
- canonical writer 1명 확인. source 전부 readable(HOLD 사유 없음).

---

## 과제1 — Prompt-only self-verification loop (PHASE 2~7)

### A. BASELINE_FROZEN
- baseline (draft_v2 L144 각주 †, 원문 그대로):
  > "The magnitude convention is the headline for the reproducibility claim, and by it the lag reproduces weakly at best (strongest pair +0.163, most pairs |ρ|≤0.08)."
- baseline_id: CHAT-COPY-1 (원고 SHA는 위 과제2 참조 — 채팅만으로 계산했다고 주장하지 않음)

### B. VERIFICATION_QUESTIONS (baseline 결론 복제 없이, verdict-changing)
- Q1: strongest magnitude pair가 어느 method 쌍이고 그 값·95% CI는? (근거 파일 명시)
- Q2: 같은 쌍의 signed convention 값은 얼마이며, 원고가 그 불일치를 인지·설명하는가?
- Q3: "most pairs |ρ|≤0.08"이 재계산 게이트의 쌍별 값과 일치하는가?
- Q4: 어떤 source가 "lag이 재현된다"(등가성)를 인증하는가, 아니면 dissociation만 지지하는가?

### C. INDEPENDENT_EVIDENCE_LEDGER (초안 아닌 SOURCE만 사용)
- Q1
  - source-only answer: magnitude convention의 strongest pair = MultiVelo × MultiVeloVAE, ρ=+0.163.
  - exact locator: `results/identifiability_dissociation.md` L15·L23 — "ρ_lag (magnitude) = +0.163  95%CI [+0.078, +0.244]".
  - evidence class: authoritative source direct-read (Lv1, 최상).
  - relation to baseline: **SUPPORT**.
  - independence limit: same-agent 추론이나 값은 실제 파일 인용(지어냄 아님).
- Q2
  - source-only answer: 같은 MV×MVVAE 쌍의 signed 값 = −0.010. 원고 각주 †가 "signed near-zero, sign-unstable lags let opposing signs cancel whereas the magnitude does not"로 그 차이를 명시·설명.
  - exact locator: signed = `results/concordance.md` L57 "multivelo×multivelovae … Spearman(rank) −0.010"; 화해 = `draft_v2.md` L144 각주 †; 범주혼동 경고 = `identifiability_dissociation.md` L24.
  - evidence class: source direct-read + 원고 자체 disclosure.
  - relation to baseline: **SUPPORT** (원고가 불일치를 숨기지 않고 문서화).
  - independence limit: 위와 동일.
- Q3
  - source-only answer: 재계산 게이트(concordance.md §3.5)의 signed |값| = mv×moflow 0.038, mv×mvvae 0.010, moflow×mvvae 0.083 — 전부 ≤~0.08. magnitude strongest(+0.163)만 그 위. "most pairs |ρ|≤0.08" 성립.
  - exact locator: `results/concordance.md` L55·L57·L59.
  - evidence class: actual tool output (재계산 게이트, Lv2).
  - relation to baseline: **SUPPORT**.
  - independence limit: 게이트는 결정적 재계산이라 초안과 독립.
- Q4
  - source-only answer: 어떤 source도 등가성을 인증하지 않는다. identifiability_dissociation.md는 "등가 아님 … 엄격한 한계에서 등가성이 인증되지 않는다"(L23), headline은 dissociation(Δρ, L88)이라 명시. 원고는 "reproduces weakly at best"(재현된다 아님)로 표현.
  - exact locator: `identifiability_dissociation.md` L23·L26·L88·L89.
  - evidence class: source direct-read.
  - relation to baseline: **SUPPORT** (원고가 over-claim 하지 않음 — "weakly at best"·"most pairs |ρ|≤0.08").
  - independence limit: 위와 동일.

### D. CORRECTION_GATE
- **NO_CHANGE.** 4개 질문 모두 SUPPORT. baseline과 구체적으로 충돌하는 source·기준 실패 없음. 표현·취향만으로 고치지 않는다(그건 Refinement, 별개).

### E. FINAL_AFTER_ONE_CYCLE
- baseline 그대로 보존(수정 0회).

### F. NO_DEGRADATION_READBACK
- 목적 적합성: 재현성 헤드라인 주장 — 유지.
- 맞던 정보 보존: +0.163·CI·"most |ρ|≤0.08"·convention 구분 전부 보존(수정 없음).
- 필수 항목 보존: strongest pair 귀속·signed/magnitude 화해 유지.
- 새 unsupported claim 없음: 추가 주장 0.
- 형식·안전 경계: 원고 무수정, 외부 공개 없음.

### G. VERDICT
- verdict: **PASS_WITH_NOTE**.
- reason: baseline claim이 직접 원문(identifiability_dissociation.md)과 재계산 게이트(concordance.md)로 지지됨. over-claim 없음.
- NOTE: +0.163(magnitude)와 −0.010(signed)은 같은 MV×MVVAE 쌍의 서로 다른 convention이며, 원고 각주 †가 이를 정확히 disclosure한다. (파생 문서 `FINDINGS.md`가 이 둘을 혼동해 signed를 "magnitude concordance"로 오라벨했던 건 커밋 `9d1c615`로 정정됨 — 정본 원고는 처음부터 정확.)
- stop condition reached: YES (correction cap 도달 아님 — 결정적 근거로 SUPPORT 확정되어 수정 불요).
- unresolved item: 없음.
- next single check if HOLD: 해당 없음.

### H. LEARN_BACK
- status: **CONDITIONAL_CANDIDATE** (한 사건 근거라 정본 규칙 미승격).
- candidate rule: "부호가 0 근처에서 불안정하거나 구조적인 metric의 concordance를 보고할 때, 값에 convention(signed vs magnitude) 라벨을 명시하고 signed 값을 magnitude 라벨로 나르지 않는다."
- appliesWhen: sign이 unstable/structural한 양(예: lag=switch-time 차)의 쌍별 일치도 보고.
- doesNotApplyWhen: sign이 안정·유의미해 signed와 magnitude가 일치하는 경우.
- evidence: FINDINGS 오라벨 사건(9d1c615) + 이 검증.
- falsifier: near-zero 상쇄가 없어 signed≈magnitude라 라벨이 무의미한 사례.
- promotion boundary: 다른 대상에서 반복·전이 확인 전에는 정본 규칙 승격 금지.

---

## 과제2 — REQUIRED COMPLETION REPORT

- canonical writer: kkkim 세션(단일).
- files created or modified: `results/verification/magnitude_claim_verification.md`(이 파일, 신규). 원고 무수정.
- baseline artifact: `manuscript/draft_v2.md` + `draft_v2_ko.md`(검증 대상, 동결).
- baseline SHA-256: 위 "과제2 Baseline 동결" 참조(실제 sha256sum, git HEAD cf93245).
- independent questions and verifier identity: Q1~Q4(위 B), verifier = 같은 에이전트(INDEPENDENCE_NOTE: same-agent 추론이나 근거는 실제 파일 직접 인용).
- direct source/tool/deterministic evidence: identifiability_dissociation.md(직접 read), concordance.md(재계산 게이트 산출물), draft L144(원고 자체 disclosure), `check_manuscript_numbers.py`(수치 grounding — +0.163·signed 값 근거 실재 확인).
- correction cycle count: **0**.
- no-degradation result: 통과(수정 없음 → 비열화 없음).
- final SHA-256: 원고 무수정이므로 baseline과 동일(위 값).
- verdict: **PASS_WITH_NOTE**.
- HOLD fields: 해당 없음.
- Learn Back: CONDITIONAL_CANDIDATE(위 H).
- limitations: (1) verifier가 same-agent라 완전 독립 아님 — cross-model/human(Lv5·Lv8)은 미적용. (2) 한 개 headline claim만 대상(다른 헤드라인은 별도 pass 필요). (3) p3 재계산 게이트는 `--with-recompute`로 별도 실행해야 완전.

---

## 과제2 후속 — Cross-model 독립검증 (Lv5, 다른 모델)

> BIOP01-84 후속(3). 다른 모델(sonnet) 서브에이전트가 source 파일만 직접 읽고 적대적 독립 검증. same-agent(위 과제1, Lv1)와 독립. 도구 7회, 96k tokens.

**OVERALL: SUPPORT_WITH_NOTE.** 핵심 수치(+0.163·CI [+0.078,+0.244]·signed −0.010)는 identifiability_dissociation.md·concordance.md·clean_concordance_gate.md·FINDINGS.md 4곳에서 정확 재현. "weakly at best"는 TOST 비등가 결과(등가 미인증)와 정합 — 과대·과소 주장 아님.

- Sub-fact 1(strongest MV×VAE +0.163) SUPPORT. 단 "strongest"는 다른 5쌍의 *magnitude* 재계산이 source에 없어 apples-to-apples 교차확인은 안 됨(signed |ρ| 최대 0.151과만 대비).
- Sub-fact 2(signed −0.010) SUPPORT.
- Sub-fact 3("most pairs |ρ|≤0.08") **SUPPORT_WITH_NOTE(실질 note)**: §3.5 6쌍 중 5쌍의 ≤0.08은 **signed** lag Spearman에서 온 값이고 magnitude convention 재계산은 MV×VAE 1쌍만 존재. 그 1쌍에서 signed(−0.010)와 magnitude(+0.163)가 16× 차이·부호 뒤집힘. 원고가 "under the magnitude convention … most pairs |ρ|≤0.08"로 붙여 쓰면 **균일한 magnitude convention이 전 쌍에 적용된 듯 읽힐 위험**. identifiability_dissociation.md L24가 MV×VAE에 대해 같은 범주혼동 경고를 달았으나 "most pairs" 일반화엔 확장 안 함.
- Sub-fact 4("weakly at best" 과대 아님) SUPPORT (Table 2 "Unreliable", TOST 비등가).
- 정밀 note: 엄밀히는 6쌍 중 moflow×crakvelo(0.151) 초과·moflow×VAE(0.083) 경계라 "4 of 6 ≤0.08 + 경계1 + 초과1". "most"는 합리적 반올림.

**disposition**: 수치 오류 아님(드리프트 0). 이건 *framing 정밀도* note로, 원고 수정 여부는 저자·리뷰어 판단(AKM: note는 contradiction 아님 → 자동 수정 안 함). 후보 조치 = 원고에서 convention을 clause별로 명시("strongest pair는 magnitude convention +0.163; 나머지 쌍은 signed |ρ|≤0.08"). BIOP01-52 원고 리뷰 후보 항목.

★ 의의: cross-model(Lv5)이 same-model(Lv1)이 놓친 실질 뉘앙스를 잡음 — 증거 독립성 사다리를 올리는 값을 실증.
