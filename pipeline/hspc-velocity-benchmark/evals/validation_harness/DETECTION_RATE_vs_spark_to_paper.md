# 게이트 결함 탐지율 — 우리 validation_harness vs Spark-to-Paper 92%

> 티켓: BIOP01-88 도입1. 실행: `python3 evals/validation_harness/run_validation.py`(2026-08-19T03:22:09Z, RESULT: PASS, 정본 sha 불변).
> 목적: mutation 결과에서 **게이트 결함 탐지율**을 명시 정의로 산출하고, Spark-to-Paper(Qian 2026, arXiv:2608.11924)가 보고한 fabrication detection 92%와 **정확히 같은 것을 재는지**를 정직하게 대조.
> 규율: 수치는 `report.json` 실제 출력만. 92%는 `paper_analysis/research-automation/qian-2026-spark-to-paper/`에서 확인한 값만 인용. CI는 Wilson 95%(그들 논문 CI와 재현되는 방법 — 아래 검증).

---

## 1. 탐지율 정의 (분자·분모에 무엇을 넣고 뺐는지)

**탐지율 = 결함을 주입한 케이스 중 게이트가 CONTRADICTED(탐지)로 잡은 비율.**

분모에 넣는 것 = **게이트가 반드시 발화(fire)해야 하는 결함 주입 케이스**: `M1, M2, M3, M4, M5, A3` = **6**.
- 이들은 실무자가 저지를 수 있는 실제 결함을 산출물 임시 사본에 주입하고(지어낸 수치·claim_level 격상·근거 stale·가짜 인용·한계 삭제·key_number 위조), 게이트가 그 결함을 CONTRADICTED로 잡아야 통과한다.

분모에서 **뺀 것**(과 이유):
- `M0_baseline` — mutation 없음. 정상 draft에 게이트가 **발화하지 않아야** 하는 위양성(false-positive) 대조. 탐지 시행이 아니라 특이도 시행이라 분자·분모 둘 다 제외.
- `A1_analysis_eval_nonvacuous`, `A2_analysis_corpus_classification` — 기대 판정이 SUPPORTED. 이들은 "스코어러가 공허하지 않은가(모든 mutant가 케이스셋에 의해 killed되나)"·"봉인 corpus를 사전등록대로 분류하나"를 보는 **비공허성/재현성 검사**이지, 주입된 산출물 결함을 잡는 탐지 시행이 아니다. **극성이 반대**(탐지 numerator에 넣으면 안 됨). 넣어서 8/8을 만들면 데이터를 본 뒤 골대를 넓히는 것이라 제외.
- `N0_negative_control` — 게이트가 아니라 **러너 자체**를 검사(기대를 일부러 SUPPORTED로 틀리게 선언 → 관측 CONTRADICTED와 불일치를 러너가 잡아야 정상). 게이트 탐지 시행 아님 → 제외.

NOT_TESTED 처리: 이번 실행 NOT_TESTED = **0**(`report.json` `not_tested: []`). 과거(2026-08-06 최초 실행)에는 M2/M5/A3가 NOT_TESTED였고(ledger 게이트 부재), 아래 pre-remediation 수치는 그것을 **미탐지(0점)로 계수**한다(분모에서 빼지 않음 — 게이트가 없어 못 잡은 것도 탐지 실패이므로).

---

## 2. 수치 (이번 실행 실측)

| 축 | 분자/분모 | 탐지율 | Wilson 95% CI |
|---|---|---|---|
| **post-remediation** (현행 게이트, ledger 신설 후) | 6/6 | **100%** | [61.0%, 100%] |
| **pre-remediation** (2026-08-06 최초, ledger 게이트 전) | 3/6 | **50%** | [18.8%, 81.2%] |

- post: M1·M2·M3·M4·M5·A3 모두 CONTRADICTED (이번 `report.json`).
- pre: M1·M3·M4만 CONTRADICTED, M2·M5·A3는 NOT_TESTED(=미탐지) — `EXECUTION-RECORD.md` §4 수정 전/후 표.
- pre-remediation 3/6이 **그들 ablation과 정신적으로 더 가까운 정직한 하한**이다. 우리 하네스가 스스로 gap을 찾아 `check_claims_ledger.py`를 신설해 6/6으로 올린 것이므로, 6/6은 **사후 보정(post-remediation)** 값임을 명시한다.

---

## 3. Spark-to-Paper 92%와의 대조축 — 같은 것을 재는가

**92%의 출처와 정확한 정의**(`qian-2026-spark-to-paper_core.md` L93·L198, `sources/fulltext_extract.md` L65에서 확인):

fabrication detection ablation, 분모 = **36 seeded probe / 10 failure family / 3 source** 공통.
- single-pass 14% (5/36) → +gate 69% (25/36) → +self-review 81% (29/36) → **+adversarial 92% (33/36)** [78–97%], 동반 precision 74% (42/57 issue) [61–83%].

**결론: 같은 것을 재지 않는다.** 네 가지 축이 다르다.

| 대조축 | Spark-to-Paper | 우리 validation_harness |
|---|---|---|
| **분모 크기·설계** | 36 probe / 10 failure family / 3 source. failure family는 어느 게이트가 있느냐와 독립으로 설계 | 6 결함주입 케이스. 게이트와 **함께** 저술(케이스가 게이트를 정당화하지 못하게 코드 전에 사전선언했으나, family 독립 설계는 아님) |
| **탐지 주체** | 4층 스택(single-pass→gate→self-review→adversarial), **LLM-in-the-loop**. 게이트 단독은 69% 층 | **결정론적 게이트 단독**(LLM 판단 없음, substring/CrossRef 대조). self-review·adversarial 층 없음 |
| **정량 곡선** | 층별 한계효용 곡선(각 층이 +몇 %p) | 없음 — 우리는 층별 곡선이 아니라 게이트 단독의 이진 탐지만 |
| **precision** | 74% (별도 issue corpus 57건) | 산출 불가 — 위양성 대조가 M0 1건뿐, issue corpus 없음. M0 하나로 precision 100%를 함의하지 않는다(부재로 남김) |

**비교 시 반드시 붙일 두 문장:**

1. **그들의 92%(=+adversarial, LLM 4층)와 직접 견줄 우리 셀은 없다.** 우리 결정론 게이트 단독에 가장 가까운 그들의 셀은 **+gate 69% (25/36)** [53.1%, 82.0%]다 — 92%가 아니다. 우리 pre-remediation 3/6=50% [18.8%, 81.2%]와 그들 gate-only 69% [53.1%, 82.0%]는 CI가 크게 겹쳐 **구분되지 않는다**.
2. **n=6이라 우리 CI가 매우 넓다.** post 6/6=100%의 Wilson 하한은 61.0%로, 그들 33/36 [78.2%, 97.1%]를 거의 감싼다. 두 비율은 **통계적으로 구분되지 않는다** — "우리가 맞먹거나 앞선다"가 아니라 **"현재 표본으로는 우열을 가릴 수 없다"**가 옳은 결론이다.

(CI 방법 검증: Wilson 95%로 그들 33/36을 계산하면 [78.2%, 97.1%]로 논문 보고 [78–97%]와 재현된다 → Wilson이 그들과 같은 방법. 우리도 Wilson으로 통일.)

---

## 4. 우리 하네스가 더 깊은 축 (근거만, 과장 없이)

그들의 층별 정량 곡선은 우리에게 없다(위 §3에서 인정). 반대로 우리가 가진, 그들 fulltext 추출본에 근거가 안 보이는 축:

| 우리 축 | 근거(artifact) |
|---|---|
| **게이트 자체를 mutation으로 검증**(watchmen) | `report.json` `cases` — 정상 산출물이 아니라 게이트가 결함을 잡는지 직접 시행. mutation은 산출물이지 프롬프트가 아님 |
| **fail-closed(공허≠pass)** | `check_manuscript_numbers`는 정상 draft에도 exit=1(miss "9.4") → 러너가 exit이 아니라 **control-vs-mutated miss 델타** + 사전등록 expected-miss로 판정. exit→PASS 매핑을 거부(EXECUTION-RECORD §1.1) |
| **음성 대조로 러너 자체 검사** | `N0_negative_control` — 기대를 일부러 틀리게 선언 → 러너가 불일치를 잡음(관측 CONTRADICTED ≠ 기대 SUPPORTED). 하네스가 공허하지 않음을 증명 |
| **정본 불변 sha256 assert** | `report.json` `canonical_intact: true`, before==after(5개 정본 파일). mutation이 정본을 오염시키지 않음 |
| **교정 루프 실증(assist 등급)** | `remediation_demo.loop_closed: true` — A3 탐지→정정(정본값 복원)→재검증 clean. auto(무인) 등급은 의도적 부재(판단 필요를 자동 PASS/FAIL로 환원 금지) |

주의: 이 축들은 "우리가 그들보다 낫다"의 근거가 아니라 **서로 다른 것을 측정한다**는 근거다. 그들=탐지율의 정량 곡선(넓은 결함 커버리지), 우리=게이트 단독의 이진 탐지 + 게이트/러너 자체의 무결성.

---

## 5. 실행 무결성 (이번 run)

- RESULT: **PASS** — 10/10 케이스가 사전선언 판정과 일치.
- 정본 sha 불변: `canonical_intact: true`. (참고: `draft_v2.md`/`draft_v2_ko.md` sha는 2026-08-06 대비 바뀌었는데, 이는 그 사이 원고가 정상 편집된 것이지 이번 실행이 훼손한 게 아니다 — before==after로 확인. CLAIMS.yaml·refs.bib·evidence는 8/6과 동일.)
- M3 전제 유지: `precondition_single_source: true`, `0.724`는 `atac_alpha_expression_confound.md` 단독 → M3가 stale을 실제로 검사함(원고 편집 후에도 유효).
- M4 네트워크: CrossRef 조회 성공(FAB=NOT_FOUND, CTL=VERIFIED) → CONTRADICTED. (네트워크 불통이었으면 INSUFFICIENT로 떨어져 탐지 실패가 아닌 별개 상태로 분리됐을 것 — 이번엔 해당 없음.)

---

## 6. 한 줄 결론

우리 결정론 게이트의 결함 탐지율은 **post-remediation 6/6 = 100%** [61.0%, 100%], **pre-remediation 3/6 = 50%** [18.8%, 81.2%]. Spark-to-Paper의 92%는 **LLM 4층 스택**의 값이라 우리 결정론 게이트 단독과 직접 비교 대상이 아니며, 우리에 가장 가까운 그들 셀은 **+gate 69% (25/36)**다. n=6로 CI가 넓어 두 하네스의 탐지율은 현재 표본으로 **통계적으로 구분되지 않는다**. 우리 하네스는 층별 정량 곡선이 없는 대신 게이트/러너 자체를 mutation으로 검증하는 축을 가진다.
