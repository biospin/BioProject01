# 결과물 검수 하네스 — mutation 검증 (BIOP01)

> 방법론: `RESULT_VALIDATION_METHOD_PORTABLE_v1`(이건규/지용기 공유). 목적은 **새 검수 체계 도입이
> 아니라, 이미 있는 게이트가 의도한 결함을 정말 탐지하는지 mutation 으로 증명**하는 것.
> 실행: `cd pipeline/hspc-velocity-benchmark && python3 evals/validation_harness/run_validation.py`
> 완료조건(방법론 §10): 코드 작성이 아니라 **보고서(`report.json`)를 열어 판정을 확인**해야 완료.
> 범위: **BIOP01 한정.** 검증되면 BIOP02 에 벤치마킹 적용(별도 라운드).

## 무엇을 증명했나 (2026-08-06 실행, 10/10 PASS, 정본 sha 불변)

논문-작성 관점(원고가 결과를 충실히 반영하나) + 분석 관점(분석이 올바른 수를 재현하나) 둘 다.

| case | 관점 | mutation | 게이트 | 기대=관측 |
|---|---|---|---|---|
| M0_baseline | 논문 | 없음(정상) | check_manuscript_numbers | SUPPORTED (게이트가 늘-실패 아님) |
| M1_fabricated_number | 논문 | 근거에 없는 `rho=0.999` 본문 삽입 | check_manuscript_numbers | **CONTRADICTED** ✅ 탐지 |
| M3_stale_manuscript | 논문 | 근거 파일 `0.724`→`0.111`, 원고 그대로 | check_manuscript_numbers | **CONTRADICTED** ✅ 탐지 |
| M4_fabricated_citation | 논문 | 가짜 DOI 인용 삽입 | verify_citations(CrossRef 실조회) | **CONTRADICTED** ✅ 탐지 |
| M2_claim_level_escalation | 논문 | claim_level 을 근거보다 격상 | **check_claims_ledger** | **CONTRADICTED** ✅ 탐지(gap 폐쇄) |
| M5_limitations_deleted | 논문 | 한계 수치(0/598·48%) 삭제 | **check_claims_ledger** | **CONTRADICTED** ✅ 탐지(gap 폐쇄) |
| A1_analysis_eval_nonvacuous | 분석 | 스코어러 degenerate/invert 치환 | reproducibility_pilot/mutation_check | SUPPORTED ✅ 스코어러 제약됨 |
| A2_analysis_corpus_classification | 분석 | 결함주입 fixture 분류 | reproducibility_pilot/run_pilot | SUPPORTED ✅ 봉인 corpus 정확 |
| A3_claims_evidence_integrity | 분석 | CLAIMS key_number 를 근거 밖 값으로 | **check_claims_ledger** | **CONTRADICTED** ✅ 탐지(gap 폐쇄) |
| N0_negative_control | 하네스 | M1 과 동일하나 기대를 SUPPORTED 로 오선언 | check_manuscript_numbers | 관측 CONTRADICTED≠기대 → 러너가 잡음 ✅ |

## 사용자 3질문에 대한 실측 답

**(a) 판정 6종이 현행 게이트 결과에 매핑되는가 — 부분적.**
`verify_citations` 만 near-native(VERIFIED→SUPPORTED, NOT_FOUND/MISMATCH→CONTRADICTED, NEEDS_HUMAN→REVIEW_REQUIRED, 조회불가→INSUFFICIENT). 나머지는 PASS-ish 산문·exit 코드뿐이라 어댑터가 필요했다. 특히 `check_manuscript_numbers` 는 **정상 draft 에도 exit=1(miss 1)** 이라 exit→판정 매핑이 불가 → control-vs-mutated **miss 델타**로 판정. INSUFFICIENT(대조본 없음)와 CONTRADICTED(대조했더니 틀림)를 반드시 분리(§1).

**(b) mutation 케이스가 있었는가 — 없었다(이제 있다).**
기존 `reproducibility_pilot/mutation_check.py` 는 **스코어러**를 mutate 해 eval 케이스셋을 검사하는 것이지, **게이트가 훼손된 산출물을 잡는지**는 아니었다. 이 gap 을 §4 형식(기대 판정 사전선언)으로 5+ 케이스 신설해 메웠다.

**(c) 탐지 후 교정(§3 Fix 3등급)이 루프로 닫혀 있는가 — 아니다(detection-only).**
현행 게이트 어느 것도 `fix` 필드(auto/assist/manual + target)를 내지 않는다. 관측→판정에서 멈추고 교정·재검증 배선이 없다. 각 case 에 부여할 fix 등급은 `cases.yaml` 에 선언했으나 **게이트가 이를 산출하지 않는다** → 루프 미완결이 확정 발견.

## gap 3종 → detector 로 폐쇄 (BIOP01-82, 루프 닫음)

최초 실행에서 3종이 **NOT_TESTED**(CLAIMS.yaml ledger 를 읽는 게이트 부재, BIOP01-69 "연동 후속")로 나왔다.
이 하네스가 gap 을 확정 → `scripts/check_claims_ledger.py` 신설(결정론적 3검사) → 하네스가 재검증(CONTRADICTED).
관측→판정→(detector 구축)→재검증으로 **탐지 gap 을 닫았다.** 이제 NOT_TESTED = 0.

`check_claims_ledger.py` 3검사(LLM 판단 없음, 등록값 substring 대조):
1. **claim_level ↔ status** — primary_* 등급은 status=supported 필요.
2. **limitations 보존** — 각 claim limitations 의 수치가 원고에 실재.
3. **key_number ↔ evidence** — 각 claim key_number 의 수치가 그 evidence 파일에 실재.

**남은 것(정직):**
- **교정 루프 미완결** — detection gap 은 닫았으나 fix 3등급(auto/assist/manual) 을 게이트가 아직 **산출/자동적용하지 않는다.** cases.yaml 에 fix 등급은 선언했으나 관측→교정→재검증 자동화는 후속.
- **정본 ledger 소소 발견** — 정본 CLAIMS.yaml C4 key_number lag_signal 범위 상단 `0.19`(요약 `+0.03~+0.19`)가 evidence 파일에 리터럴로 없다(파생·범위값). `check_manuscript_numbers` 의 허용 baseline miss 와 같은 성격 — 이건규 님께 보고, 정본은 미수정.
