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
| M2_claim_level_escalation | 논문 | claim_level 을 근거보다 격상 | (없음) | **NOT_TESTED** ⚠️ gap |
| M5_limitations_deleted | 논문 | 한계 문단 삭제 | (없음) | **NOT_TESTED** ⚠️ gap |
| A1_analysis_eval_nonvacuous | 분석 | 스코어러 degenerate/invert 치환 | reproducibility_pilot/mutation_check | SUPPORTED ✅ 스코어러 제약됨 |
| A2_analysis_corpus_classification | 분석 | 결함주입 fixture 분류 | reproducibility_pilot/run_pilot | SUPPORTED ✅ 봉인 corpus 정확 |
| A3_claims_evidence_integrity | 분석 | CLAIMS key_number 를 근거 밖 값으로 | (없음) | **NOT_TESTED** ⚠️ gap |
| N0_negative_control | 하네스 | M1 과 동일하나 기대를 SUPPORTED 로 오선언 | check_manuscript_numbers | 관측 CONTRADICTED≠기대 → 러너가 잡음 ✅ |

## 사용자 3질문에 대한 실측 답

**(a) 판정 6종이 현행 게이트 결과에 매핑되는가 — 부분적.**
`verify_citations` 만 near-native(VERIFIED→SUPPORTED, NOT_FOUND/MISMATCH→CONTRADICTED, NEEDS_HUMAN→REVIEW_REQUIRED, 조회불가→INSUFFICIENT). 나머지는 PASS-ish 산문·exit 코드뿐이라 어댑터가 필요했다. 특히 `check_manuscript_numbers` 는 **정상 draft 에도 exit=1(miss 1)** 이라 exit→판정 매핑이 불가 → control-vs-mutated **miss 델타**로 판정. INSUFFICIENT(대조본 없음)와 CONTRADICTED(대조했더니 틀림)를 반드시 분리(§1).

**(b) mutation 케이스가 있었는가 — 없었다(이제 있다).**
기존 `reproducibility_pilot/mutation_check.py` 는 **스코어러**를 mutate 해 eval 케이스셋을 검사하는 것이지, **게이트가 훼손된 산출물을 잡는지**는 아니었다. 이 gap 을 §4 형식(기대 판정 사전선언)으로 5+ 케이스 신설해 메웠다.

**(c) 탐지 후 교정(§3 Fix 3등급)이 루프로 닫혀 있는가 — 아니다(detection-only).**
현행 게이트 어느 것도 `fix` 필드(auto/assist/manual + target)를 내지 않는다. 관측→판정에서 멈추고 교정·재검증 배선이 없다. 각 case 에 부여할 fix 등급은 `cases.yaml` 에 선언했으나 **게이트가 이를 산출하지 않는다** → 루프 미완결이 확정 발견.

## ⚠️ 확정 gap 3종 (NOT_TESTED) — 이 실험의 최대 발견

셋 다 **CLAIMS.yaml ledger 를 읽는 게이트가 없어서**다(BIOP01-69: ledger 는 있으나 "게이트가 실제 참조하는 연동은 후속"으로 명시). 원고 수치·인용은 잡지만:
- **claim_level 격상**(근거보다 센 주장) — 탐지 게이트 없음.
- **limitations 삭제** — 한계 보존 검사 없음(`check_revision_preserved` 는 수치·인용마커만, git baseline 필요).
- **CLAIMS key_number ↔ evidence 무결성** — 대조 게이트 없음.

→ 코드 작성만으로 "완료" 처리하지 않는다. 위 3종은 미검출로 정직 기록하고, ledger 연동 detector 를 후속 작업으로 남긴다.
