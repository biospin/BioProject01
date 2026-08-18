# Spark-to-Paper (Qian et al., 2026) — lens: academic

> 근거: `sources/fulltext_extract.md`(arXiv:2608.11924 HTML fulltext 자동추출, 2026-08-18). §번호는 자동추출이라 인용 시 `검토필요:`.
> 시선: 우리 팀이 만드는 **논문 생산·검증 하네스**(`kakyungkim/paper-production-harness` + verify-harness 3층: AKM 사실검증 / mutation 게이트검증 / 검사카탈로그·독립성 사다리) 관점에서, 같은 문제를 독립적으로 푼 선례로 읽는다.
> 표기: `해석:`=근거에서 우리가 끌어낸 판단, `미제공:`=논문이 다루지 않음, `검토필요:`=원문 대조 필요.

---

## 1. 저자가 명시한 한계 (fulltext §"저자 명시 한계" 6개)

1. **claim-level 증거 판정이 model-based다.** "determining whether a particular piece of evidence semantically supports a claim is currently performed by the model" — 저자 스스로 auditing이 필요한 약점으로 인정. 결정론 gate가 잡지 못하는 "증거가 주장을 의미적으로 뒷받침하나"는 결국 모델이 판단한다.
2. **실험 feasibility가 자동 해결되지 않는다.** 자원이 없으면 missing dependency를 기록하고 결과를 미기재. 자원 gap 자체는 시스템이 못 메운다.
3. **Self-Refutation 7-iteration bound가 명시적 정당화 없이 선택됐다.** 도메인에 따라 적정 횟수가 다를 수 있음을 저자가 인정.
4. **figure 재구성 신뢰성이 완전하지 않다.** 소수 correction round로 대개 복원하되, 불가 시 raster fallback으로 물러난다.
5. **model/tool 분리가 불완전하다.** adversarial review는 여전히 3분류(3-Way Validation) 수동 검증이 필요하다.
6. **평가 범위가 제한적이다.** 8 controlled topic, human preprint 8편으로, 체계적 audit이 아니다. cross-template robustness는 언급되나 main table에 수치가 없다.

> 투명성 조치(저자): 사전등록 + 외부 timestamp, "모든 결과를 Spark-to-Paper에 유리하든 아니든 보고", CI는 run이 아니라 paper 단위(n>3), 비용·token 불확실성 범위 공개, 이전 시스템과 pricing/model 가정이 다름을 인정.

---

## 2. 분석자 판단 — 우리 하네스 관점

우리와 Spark-to-Paper는 **같은 구조적 선택을 독립적으로 수렴**했다. 결정론 gate와 의미판단(모델 리뷰)의 분리, 사전등록으로 사후 프로토콜 적응을 막는 것, 실패를 억지 성공으로 덮지 않고 failure report로 남기는 것, 산출을 파일 아티팩트로 넘기는 것. 이 수렴 자체가 두 팀의 설계가 임의적이지 않다는 방증이다. 그 위에서 우열이 아니라 **어느 쪽이 더 깊은지**를 근거로 나눈다.

### 2-1. 그들이 우리보다 앞선 것 (근거 있음)

- **정량 ablation으로 게이트의 한계효용을 측정했다.** fabrication detection이 single-pass 14%(5/36) → +gate 69% → +self-review 81% → +adversarial 92%(33/36)로 단계별 증분이 CI와 함께 나온다(§검토필요:, 36 seeded probe / 10 failure family / 3 source). **우리는 mutation으로 "게이트가 결함을 잡나/못 잡나"를 이진으로 보이지만(2026-08-06 실행: M2/M5/A3가 NOT_TESTED→CONTRADICTED, `pipeline/hspc-velocity-benchmark/evals/validation_harness/EXECUTION-RECORD.md`), "각 층이 몇 %p 더 잡나"라는 정량 곡선은 아직 없다.** 이게 그들이 확실히 앞선 지점이다.
  - 해석: 우리 Layer 2 mutation은 "이 검사는 이 결함 부류에서 NOT_TESTED(공허)"를 판정하는 정성 게이트다. 그들은 같은 질문을 detection rate라는 연속 지표로 답했다.
- **비용·토큰·wall-clock을 벤치마크로 보고했다.** $8.1 [6.9–9.6] / 11.9M token [10.2–13.7M] / 3.2h, 8 topic. 층별 증분도 분해했다(gate +8.1M tok/+$5.3, self-review +1.1M/+$0.6, adversarial +2.6M/+$1.6). **우리 하네스엔 검증 1회의 비용 회계가 없다.** 검증의 한계효용을 비용 대비로 논할 근거가 그들에겐 있고 우리에겐 없다.
- **Claim Admission Protocol이 5라벨로 정형화돼 있다.** supported / partially-supported / unsupported / contradicted / needs-confirmation, 각 라벨에 조치가 붙고(unsupported→실험·약화·삭제, needs-confirmation→저자 확인, 미해결 금지) 수정을 abstract·intro·results·conclusion 전 occurrence로 전파한다. **우리 claim ledger는 claim_level↔status(primary는 supported 요구) 무결성은 검사하지만, "부분지지/반증됨/확인필요"까지 나눈 5라벨 상태기계와 전파 규칙은 없다.**
- **문헌 대비 citation validity를 벤치마크로 세웠다.** 99.5% [98.4–100%](384 refs)를 human preprint 97.8%, AI Scientist 93%, v2 91%, Agent Laboratory 96%, single-pass 81%와 나란히 놓았다. **우리 검사 카탈로그의 "서지 정합(CrossRef 대조)"은 pass/fail 게이트일 뿐, 경쟁 시스템과의 비교 수치가 없다.**

### 2-2. 우리가 더 깊은 것 (근거 있음 — 실행 아티팩트 명시)

> 아래 세 항목은 설계문(verify-harness SKILL)만이 아니라 **실행된 결과물**로 뒷받침된다: 2026-08-06 mutation 실행 기록 `pipeline/hspc-velocity-benchmark/evals/validation_harness/`(EXECUTION-RECORD.md·cases.yaml·run_validation.py·report.json)와 gap을 닫은 detector `pipeline/hspc-velocity-benchmark/scripts/check_claims_ledger.py`. "그들에게 없다"는 진술은 fulltext 추출본 기준이며 원문 Appendix 대조가 필요하다.

- **우리는 게이트 자체를 mutation으로 검증하고 실제로 공허한 게이트를 찾아 닫았다.** 2026-08-06 실행에서 원고 수치·인용 게이트는 결함을 잡았으나 **CLAIMS.yaml ledger를 읽는 게이트가 없어 claim_level 격상·limitations 삭제·key_number 위조가 통째로 미검출(NOT_TESTED 3)**임을 발견하고, `check_claims_ledger.py`를 신설해 셋 다 CONTRADICTED로 잡히게 한 뒤 재검증했다(NOT_TESTED=0, 정본 sha256 불변 assert). 우리 Layer 2 명제 — "deterministic check를 Lv3 증거로 신뢰하려면 그 검사가 공허하지 않음을 먼저 보여야 한다" — 에 해당하는 절차가 **fulltext 추출본에 없다(원문 Appendix 대조 필요)**.
  - 미제공: fulltext 추출본에 게이트의 false-negative(정상처럼 통과시키는 결함 부류)를 체계적으로 뒤진 흔적이 없다(원문 Appendix 대조 필요). detection 92%는 곧 **8%(3/36)를 못 잡는다**는 뜻인데, 어떤 결함 부류가 새는지의 분류가 보이지 않는다.
- **circular-evidence(자기 리포트를 근거로 삼기) 격리가 우리 설계와 실행에 명시돼 있다.** 우리 함정 (1): 검증 리포트를 검사 대상의 source 코퍼스에 넣지 말 것(weak-judge propagation). 실제 실행도 mutation을 bench 하위 `.sandbox/`(gitignore) 사본에서만 돌리고 report.json을 코퍼스 밖에 썼다. 그들의 Self-Review는 "수정 내용을 주변 원고와 대조"하는데, **리뷰 산출이 다음 판정의 입력으로 새는지에 대한 격리 규율이 fulltext 추출본에 없다(원문 대조 필요).**
- **cross-model + 사람으로 이어지는 독립성 사다리를 우리는 명시한다. 그들의 review는 same-model isolated pass다.** 그들의 adversarial review는 "다중 isolated pass"지만 **같은 모델 backbone**이고, 그 결과 precision이 74%(42/57 issue) [61–83%]에 그친다 — **제기된 issue의 약 26%가 오탐**이다. 우리 사다리는 Lv5 cross-model(다른 모델이 source만 읽고 적대 검증) → Lv8 사람/advisor를 높은 영향 수정의 필수 관문으로 둔다. same-model 자기비평은 우리 사다리에서 **Lv1(질문 후보일 뿐 사실 증명 아님)**로 강등된다.
  - 해석: 그들의 precision 74%는 우리가 "same-model 자기검증만 믿지 마라"(함정 3)로 경계한 바로 그 실패를 정량으로 보여준다. 그들이 만든 26% 오탐이 우리 사다리의 존재 이유를 외부 데이터로 뒷받침한다.
- **재계산 게이트를 "실행됨"이 아니라 "diff-0"으로 대조하는 규율이 우리에겐 명시적이다.** 우리 함정 (2)·카탈로그의 "재계산 diff-0": 게이트 실행 후 산출물 git diff가 비어야 PASS(BIOP01 DoD의 `p3_concordance.py` 등 결정론 재계산 대조와 동일). 그들의 Compilation Gate는 "인용·교차참조 해결된 컴파일"인데, **컴파일 성공(rc=0)과 수치 재현(값 일치)을 구분하는 규율이 fulltext 추출본에 드러나지 않는다(원문 대조 필요).**

### 2-3. 겹치는 것 (독립 수렴)

- **사전등록으로 사후 적응을 막는다.** 그들: planning stage가 dataset·baseline·metric·ablation·result table 구조를 실험 전 고정, "numerical cells remain empty until experiments complete"(lightweight preregistration). 우리: PREREGISTRATION 문서에 기준(예 Spearman ρ≥0.50)을 봉인하고 "데이터를 본 뒤 골대 올리기 금지". **둘 다 planning↔reporting 분리로 같은 위험을 겨눈다.** 단 그들도 인정하듯 preregistration은 non-binding이고 사후 claim 판정은 모델이 한다.
- **self-refutation을 cap으로 묶고 실패를 실패로 남긴다.** 그들: experiment–critique–revision을 7회 bound, 초과 시 trajectory 종료 + failure report(원 아이디어·시도·관측·불충분 사유), 억지 성공 안 함. 우리: correction cap(Tier별) 초과·근거 부재 시 stop, HOLD 4필드로 사람 이관. **둘 다 "무한 자기수정으로 성공을 지어내는 것"을 유한 루프 + 실패 보고로 막는다.**
- **결정론 gate와 의미판단(모델 리뷰)을 분리한다.** 그들: "Deterministic checks cannot determine whether an argument is sufficiently supported" → model-based review로 보완. 우리: Lv3 결정적 검사(재현적) ↔ Lv5 cross-model 의미판단을 사다리에서 층으로 분리. **경계선을 같은 자리에 그었다.**
- **산출을 파일 아티팩트로 넘긴다.** 그들: blueprint.json, refs.bib, claims_map.json, results.facts.json, logs/*.io.md 등(Table 6). 우리: FINDINGS.md·claim ledger·VERIFICATION_PROTOCOL.md·cases.yaml·report.json. **중간 결과를 대화에 남기지 않고 파일 계약으로 넘기는 설계가 같다.**

---

## 3. 다음 연구 / 후속 아이디어 (우리 verify-harness에 도입할 것)

- **Claim Admission 5라벨을 우리 claim ledger에 접목한다.** 현재 우리 ledger의 status(supported/HOLD 중심)를 supported·partially-supported·unsupported·contradicted·needs-confirmation 5상태로 확장하고, 각 라벨에 조치(unsupported→약화·삭제, needs-confirmation→사람 이관, 미해결 금지)와 전 occurrence 전파 규칙을 붙인다. 이건 우리 Layer 3 카탈로그의 "claim ledger 무결성" 검사를 상태기계로 승격하는 일이고, 그 상태 전이 검사가 공허하지 않은지는 Layer 2 mutation(무단 격상·라벨 강등 주입)으로 먼저 증명한다.
- **정량 fabrication-detection ablation을 우리 mutation 스위트로 측정한다.** 그들의 방법(seeded probe × failure family)을 우리 도메인(velocity 벤치마크 원고·FINDINGS)에 맞춰 재해석해, single-pass → +결정론 게이트 → +cross-model(Lv5) → +사람(Lv8) 단계별 detection rate 곡선을 낸다. 그러면 **"그들 92% vs 우리 N%"라는 직접 비교 기준**이 생긴다. 우리 가설은 cross-model 층이 same-model adversarial(그들 92%, precision 74%)보다 오탐을 낮추면서 detection을 유지하는지다 — 검증하면 우리 사다리의 우위를 정량 근거로 못박을 수 있다.
- **검증 비용 회계를 붙인다.** 그들처럼 검증 1회의 token·비용·wall-clock을 층별로 기록해, "cross-model 한 층 추가의 한계효용 대비 비용"을 우리도 논할 수 있게 한다. 지금 우리 하네스엔 이 회계가 없다(2-1 지적).
- **게이트 false-negative 분류를 만든다.** 그들이 못 잡는 8%(3/36)의 결함 부류가 무엇인지 fulltext에 없는데(2-2 미제공), 우리 mutation 스위트에 failure family 분류(근거없는 수치·stale 원고·claim 무단격상·한계 삭제 등)를 갖춰 "우리 게이트가 새는 부류"를 명시적으로 좁힌다. 이게 우리가 그들보다 나은 지점을 실증하는 자리다.
- **preregistration binding 강화.** 그들도 우리도 preregistration이 non-binding이고 사후 claim 판정은 모델이 한다는 공통 약점이 있다. 봉인 문서의 `파일:줄` locator를 검증 게이트가 강제 대조하게 해(우리 CLAUDE.md의 "슬라이드 관측값을 임계로 쓰지 마라" 사고 방지) binding에 가깝게 만든다.

---

## 4. Citation 후보 (우리 논문·§6.1 AI Scientist·하네스 방법노트용)

> `paper-info.yaml` 미생성. BibTeX key는 과제 지정값 `@qian2026sparktopaper` 사용. 저자 표기는 검토필요:(fulltext는 corresponding=wangwenhao@vastilab.com만 제공, 폴더명 기준 first author Qian).

### 인용 가능 문장

- §검토필요:(Discussion/Limitation): "determining whether a particular piece of evidence semantically supports a claim is currently performed by the model"
  - 사용 시나리오: 우리 하네스 방법노트에서 "결정론 gate가 못 넘는 의미판단은 결국 모델이 하는 일이라 독립성 사다리(cross-model·사람)가 필요하다"를 논할 때, 선례도 같은 한계를 인정했다는 근거.
  - BibTeX key: `@qian2026sparktopaper`
- §검토필요:(Architecture): "Deterministic checks cannot determine whether an argument is sufficiently supported, whether different sections remain conceptually consistent"
  - 사용 시나리오: 우리 논문에서 결정론 검사와 의미판단 리뷰의 경계선을 그을 때, 독립 팀이 같은 경계를 그었다는 인용.
  - BibTeX key: `@qian2026sparktopaper`
- §검토필요:(Preregistration): "The table structure is fixed in advance, while numerical cells remain empty until the corresponding experiments are completed"
  - 사용 시나리오: 우리 사전등록(planning↔reporting 분리)의 선행 사례로 인용, "사후 프로토콜 적응 위험을 줄인다"는 주장의 근거.
  - BibTeX key: `@qian2026sparktopaper`
- §검토필요:(Self-Refutation): experiment–critique–revision cycle을 7회로 bound, 초과 시 "failure report"(원 아이디어·시도·관측·불충분 사유) 기록 + 억지 성공 안 함
  - 사용 시나리오: 우리 correction cap·HOLD 이관 규율의 선례로, "무한 자기수정으로 성공을 지어내는 실패모드"를 문헌으로 뒷받침.
  - BibTeX key: `@qian2026sparktopaper`
- §검토필요:(Transparency): "Report all outcomes regardless of whether they favor Spark-to-Paper"
  - 사용 시나리오: 우리 논문 생산 하네스의 정직 보고 규율(정직 게이트)이 자동 논문생성 분야의 규범과 정렬됨을 보일 때.
  - BibTeX key: `@qian2026sparktopaper`
- §검토필요:(Ablation caveat): fabrication detection 92%는 "36 probe / 10 family" 범위이며 failure coverage가 제한적임을 저자가 인정
  - 사용 시나리오: 우리가 정량 ablation을 도입할 때 "detection rate는 probe 코퍼스에 의존한다"는 방법론 주의로 자기 인용 겸 상대화.
  - BibTeX key: `@qian2026sparktopaper`

### 인용 가능 수치

- citation validity **99.5%** [98.4–100%] (384 refs, §검토필요: 평가). 대비: human 97.8%, AI Scientist 93%, v2 91%, Agent Laboratory 96%, single-pass 81%.
  - 사용 시나리오: 우리 서지 정합 게이트의 목표선·경쟁 시스템 벤치 인용. §6.1 AI Scientist 계열 비교표의 정량 근거.
  - BibTeX key: `@qian2026sparktopaper`
- fabrication detection **14%→69%→81%→92%** (single-pass→+gate→+self-review→+adversarial; 33/36, §검토필요: ablation)
  - 사용 시나리오: 검증 층을 쌓을수록 결함 검출이 오른다는 정량 곡선. 우리 mutation 곡선의 비교 baseline("그들 92% vs 우리 N%").
  - BibTeX key: `@qian2026sparktopaper`
- adversarial review **precision 74%** (42/57 issue) [61–83%] — 제기 issue의 약 26% 오탐
  - 사용 시나리오: "same-model isolated review는 오탐이 남는다"는 우리 주장(cross-model 필요성)의 외부 근거. 우리 독립성 사다리의 존재 이유.
  - BibTeX key: `@qian2026sparktopaper`
- 생성 비용 **$8.1** [6.9–9.6] / **11.9M token** / **3.2h**, 8 topic (single-pass baseline $0.66·0.11M·16min)
  - 사용 시나리오: 자동 논문생성의 비용 규모 인용. 우리 검증 비용 회계 도입 시 비교 기준.
  - BibTeX key: `@qian2026sparktopaper`
- figure editability **96.4%** [92.7–98.6%] (~1,900 element) vs human preprint 58%, 이전 자율시스템 0–3%
  - 사용 시나리오: 생성 figure의 벡터/편집가능성을 논할 때. 단 저자가 의도적 raster를 제외했음을 함께 명시(caveat).
  - BibTeX key: `@qian2026sparktopaper`

### 인용 가능 Figure/Table

- Table(§검토필요: fabrication ablation): 구성별 detection/precision (single-pass 14% → +gate+self-review+adversarial 92%/74%)
  - 무엇을 보여주나: 검증 층 누적에 따른 결함 검출 증분과 그 정밀도 상한.
  - 사용 시나리오: 우리 방법노트에서 "층별 한계효용 측정" 도식의 선례로 재현·인용.
  - BibTeX key: `@qian2026sparktopaper`
- Table 6 / Appendix D(산출물 목록): blueprint.json·refs.bib·claims_map.json·results.facts.json·logs/*.io.md
  - 무엇을 보여주나: 파이프라인이 남기는 파일 아티팩트 계약.
  - 사용 시나리오: 우리 산출물 계약(FINDINGS.md·claim ledger·report.json)과 대응시키는 비교표.
  - BibTeX key: `@qian2026sparktopaper`

---

## Final Takeaways

- **이 논문의 가장 큰 의미:** end-to-end 논문 생성+검증을 별도 자율 플랫폼이 아니라 기존 coding assistant 안의 재사용 skill 묶음으로 돌릴 수 있음을 정량 벤치(detection 14→92%, citation 99.5%, 비용 $8.1)로 보인 독립 선례. 우리와 같은 구조적 선택(사전등록·failure report·결정론/의미판단 분리·파일 아티팩트)에 독립 수렴했다.
- **우리 하네스로 이어질 아이디어:** (1) Claim Admission 5라벨을 우리 claim ledger 상태기계로 승격, (2) fabrication-detection ablation을 우리 mutation 스위트로 측정해 "그들 92% vs 우리 N%" 비교 기준 확보, (3) 검증 비용 회계 신설.
- **우리가 지켜야 할 우위:** 그들의 review는 same-model isolated(precision 74%, 오탐 26%)이고 게이트 공허성 검사가 없다. 우리 mutation(게이트가 결함을 잡나)·circular-evidence 격리·cross-model+사람 독립성 사다리가 바로 그 26% 오탐과 게이트 false-negative를 겨눈 층이다. 이 우위를 정량으로 실증하는 것이 우선순위 높은 후속 작업.
- **주의(미검증):** §번호는 fulltext 자동추출이라 전부 `검토필요:`. 저자 표기는 corresponding email(vastilab)만 제공됨. 위 비교의 "우리가 한 것"은 verify-harness SKILL 설계문 기준이며, 각 정량 비교("우리 N%")는 아직 측정 전이다(도입 아이디어이지 완료된 결과가 아님).
