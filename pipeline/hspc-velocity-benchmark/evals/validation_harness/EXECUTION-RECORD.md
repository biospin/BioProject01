# 결과물 검수 하네스 실행 기록 — BIOP01, 2026-08-06

> 성격: 실제로 무엇을 돌렸고, 무엇이 나왔고, 무엇을 고쳤는지의 이력.
> 짝 문서: 케이스·판정 계약은 `cases.yaml`, 결과 요약은 `README.md`, 기계 판정은 `report.json`.
> 방법론 원본: Google Drive `RESULT_VALIDATION_METHOD_PORTABLE_v1.md`.
> 형식 벤치마킹: 임상 리포트 도메인의 `결과물 검수 실행 기록`(그대로 복사 아님 — 우리 도메인=velocity 원고+분석에 맞춰 번역).
> 범위: **BIOP01 한정.** BIOP02 이식은 §7.

---

## 0. 한 줄 요약

검수 하네스를 **자동화로 만들어 정상+mutation 케이스를 세션에서 실행**하고, 그 하네스가 스스로
찾아낸 **탐지 gap 3종을 detector 신설로 닫은 뒤 재검증**했다.

가장 중요한 발견은, 원고 수치·인용은 기존 게이트가 실제로 잡지만 **CLAIMS.yaml ledger 를 읽는 게이트가
없어 claim_level 격상·limitations 삭제·key_number 위조가 통째로 미검출**이었다는 것이다(NOT_TESTED 3).
`check_claims_ledger.py` 를 만들어 셋 다 CONTRADICTED 로 잡히게 하고 하네스로 재확인했다.

---

## 1. 진행 과정

방법론(§13)대로 **기존 검사기를 먼저 검색해 중복을 피하고**, 케이스 판정을 코드보다 먼저 선언한 뒤 돌렸다.

| # | 단계 | 목적 | 실측 결과 |
|---|---|---|---|
| 1 | 방법론 2편 정독 + 기존 하네스 전수 조사 | 무엇이 이미 있나 | 게이트 9종·evals·`mutation_check.py`(스코어러 검사=게이트 검사 아님, gap) |
| 2 | CLAIMS.yaml 실체 확인 | mutation 기준본 유무 | **정본 없음**(PR#12 gglee만) → kkkim-pipeline 반입(ab08715) |
| 3 | 게이트 계약 실측 | exit·JSON 실패신호 확정 | ★ `check_manuscript_numbers` 는 **정상 draft 도 exit=1**(miss "9.4") → exit→판정 불가 |
| 4 | 케이스 사전선언 | 코드가 케이스를 정당화 못 하게 | 10 케이스, 논문+분석 2관점 (cases.yaml) |
| 5 | 하네스 실행 (before) | 게이트가 정말 잡나 | M1/M3/M4 CONTRADICTED ✅, **M2/M5/A3 NOT_TESTED(gap 3)** |
| 6 | gap detector 신설 | 탐지에서 끝내지 않음 | `check_claims_ledger.py`(3검사) |
| 7 | 케이스 재선언 + 재실행 (after) | 고쳐졌나 | M2/M5/A3 **NOT_TESTED→CONTRADICTED**, NOT_TESTED=0 |
| 8 | 정본 불변·무회귀 확인 | 검수가 정본을 안 건드렸나 | 실행 전후 sha256 동일(draft·CLAIMS·refs·evidence) |

정본은 손대지 않았다. mutation 은 bench 하위 `.sandbox/`(gitignore) 사본에서만, 실행 전후 checksum 으로 불변을 assert 했다.

### 1.1 게이트 계약 실측 (단계 3) — 가장 중요한 함정

`check_manuscript_numbers --json` 를 정상 draft 에 돌리니 **exit=1, misses=1**(값 "9.4", L67 lag 문맥의 파생·서술 수치)이었다.
exit 코드로 판정을 매핑하면 **모든 mutation 이 SUPPORTED 로 읽힌다**(baseline 도 이미 1). 그래서 러너는
**control(정본) 대 mutated(사본) miss 델타**로 판정한다 — 새로 생긴 miss 가 있으면 CONTRADICTED.

### 1.2 mutation 대상 실측 (단계 3) — 단일소스 전제

M3(근거 바꾸고 원고 stale)은 바꾼 수치가 **근거 파일 하나에만** 있어야 union 이 stale 을 잡는다.
헤드라인 수치는 다중소스였다(`0.88` = 18파일). `results/*.md` 를 훑어 **단일소스 `0.724`**
(`atac_alpha_expression_confound.md` 단독, draft 에도 존재)를 골라 전제로 기록했다.

---

## 2. 찾아낸 방법 — 무엇이 결함/gap 을 드러냈나

계획보다 아래가 실제로 gap 을 잡았다. 다른 프로젝트(BIOP02)에도 옮길 수 있다.

1. **게이트 출력 계약을 케이스 전에 실측한다.** exit=1 이 정상인 게이트를 모르면 러너가 공허해진다. 실패신호(JSON `misses` 델타)를 먼저 확정.
2. **control-vs-mutated 델타로 판정한다.** 정상도 miss 를 내는 게이트에서 baseline 을 자동 상쇄.
3. **mutation 은 실무자가 저지를 실수로.** 근거없는 수치 삽입·evidence 갱신 후 원고 stale·claim_level 무심코 격상 — 전부 게이트 통과하되 결과가 심각.
4. **특정 finding 표적 대조.** ledger 게이트가 정본 C4 에 baseline 발견을 내도, mutation 이 만든 **특정 check+claim** 이 새로 뜨는지로 판정 → baseline 과 무관.
5. **음성 대조로 러너 자체를 검사.** 기대를 일부러 틀리게 선언한 N0 에서 러너가 불일치를 잡아야 한다(관측 CONTRADICTED ≠ 기대 SUPPORTED).

---

## 3. 고친 것 — gap detector 신설

하네스가 확정한 NOT_TESTED gap 3종을 `scripts/check_claims_ledger.py`(결정론, LLM 판단 없음, substring 대조)로 닫았다.
등급으로 보면 detector 는 `assist`(제안·확신도), 교정 자리는 `source`(CLAIMS.yaml)·`artifact`(원고).

| 검사 | 규칙 | 잡는 mutation |
|---|---|---|
| claim_level ↔ status | primary_* 등급은 status=supported 필요 | M2: provisional claim 을 primary 로 격상 |
| limitations 보존 | claim limitations 의 수치가 원고에 실재(substring) | M5: 한계 수치(0/598·48%) 삭제 |
| key_number ↔ evidence | claim key_number 의 수치가 그 evidence 파일에 실재 | A3: key_number 를 근거 밖 값(0.987654)으로 |

**매칭 함정도 실측으로 고쳤다.** 첫 실행에서 정본 C1/C2/C4 가 CONTRADICTED 로 떴다 —
evidence 는 `0.882`·`-0.042` 로 더 정밀한데 ledger 는 `0.88`·`-0.04` 로 반올림했기 때문.
exact-token 대조 → **substring 대조**(`check_manuscript_numbers` 규약)로 바꿔 정본이 통과하게 했다.

---

## 4. 수정 전 / 후 (하네스 재실행)

같은 10 케이스를 detector 신설 전후로 돌렸다.

| case | 관점 | 수정 전(c3ae53c) | 수정 후(3a99707) |
|---|---|---|---|
| M0_baseline | 논문 | SUPPORTED | SUPPORTED (무회귀) |
| M1_fabricated_number | 논문 | CONTRADICTED ✅ | CONTRADICTED ✅ |
| M3_stale_manuscript | 논문 | CONTRADICTED ✅ | CONTRADICTED ✅ |
| M4_fabricated_citation | 논문 | CONTRADICTED ✅ | CONTRADICTED ✅ |
| **M2_claim_level_escalation** | 논문 | **NOT_TESTED** ⚠️ | **CONTRADICTED** ✅ |
| **M5_limitations_deleted** | 논문 | **NOT_TESTED** ⚠️ | **CONTRADICTED** ✅ |
| **A3_claims_evidence_integrity** | 분석 | **NOT_TESTED** ⚠️ | **CONTRADICTED** ✅ |
| A1_analysis_eval_nonvacuous | 분석 | SUPPORTED | SUPPORTED |
| A2_analysis_corpus_classification | 분석 | SUPPORTED | SUPPORTED |
| N0_negative_control | 하네스 | 러너가 잡음 ✅ | 러너가 잡음 ✅ |
| **NOT_TESTED 합계** | | **3** | **0** |
| 정본 sha256 | | 불변 | 불변 |

10/10 케이스가 사전선언 판정과 일치. **탐지 gap 을 닫았다.**

---

## 5. 아직 안 고친 것 (정직하게)

| 항목 | 왜 안 고쳤나 |
|---|---|
| **교정(fix) 루프 자동화** | detection gap 은 닫았으나, 게이트가 fix 3등급(auto/assist/manual)을 **산출·자동적용하지 않는다.** cases.yaml 에 등급만 선언. 관측→교정→재검증 자동화는 후속 |
| **정본 CLAIMS C4 `0.19`** | lag_signal 범위 상단(`+0.03~+0.19`)이 evidence 리터럴 부재(파생·범위값). `check_manuscript_numbers` 허용 baseline 과 같은 성격. 이건규 님 보고, 정본은 미수정 |
| **게이트↔CI 배선** | `check_claims_ledger` 를 harness_doctor/package_validation 에 hard gate 로 붙이는 것은 후속(현재는 하네스가 호출) |
| **BIOP02 이식** | §7. 복사 아닌 벤치마킹이라 도메인 게이트 조사 선행 |

**이번 작업으로 완결된 것은 "탐지"까지다.** 교정 자동화는 `NOT_TESTED` 로 남긴다.

---

## 6. 재현 방법

```bash
cd pipeline/hspc-velocity-benchmark
python3 evals/validation_harness/run_validation.py     # 10 케이스, report.json 생성
cat evals/validation_harness/report.json               # 판정 확인(완료조건: 보고서를 연다)

# gap detector 단독
python3 scripts/check_claims_ledger.py                 # 정본
python3 scripts/check_claims_ledger.py --claims <사본> --draft <사본>
```

완료조건(방법론 §10): 코드 작성이 아니라 **report.json 을 열어 판정을 확인**해야 완료.

---

## 7. BIOP02 로 옮길 때 (복사 아닌 벤치마킹)

일반화할 수 있는 것은 §2 다섯 가지다. BIOP02(SpatialPathoAgent)는 도메인이 다르므로 **게이트를 그대로 옮기지 않는다.**

- 먼저 BIOP02 게이트(critic 7항목·operating-point·LOSO 등)와 CLAIMS.yaml 유무를 조사한다(현재 BIOP02 CLAIMS 없음 확인).
- BIOP02 의 "실무자가 저지를 실수"로 mutation 을 다시 정의한다(예: 라벨 오분류·split 누수·operating-point 조작). velocity 의 claim_level 격상을 그대로 베끼지 않는다.
- 러너 골격·6판정·control-vs-mutated 델타·정본 checksum 규율은 재사용하되, detector 는 BIOP02 게이트를 부른다.

---

## 8. 변경 이력

- 2026-08-06 최초 작성. 검수 하네스 신설·실행 이력. 하네스 2회 실행(before c3ae53c / after 3a99707),
  10 케이스, gap 3종 발견(NOT_TESTED) → `check_claims_ledger.py` 신설 → 3종 CONTRADICTED 로 폐쇄(NOT_TESTED 3→0).
  정본 CLAIMS 반입 ab08715, ledger detector 3a99707. 티켓 BIOP01-82.
