# Spark-to-Paper — 전문 추출 (분석 근거)

> 출처: arXiv:2608.11924 (HTML fulltext, WebFetch 추출 2026-08-18). 수치·구조는 본문 근거.
> 저자 자체 추출본이 아니라 fulltext HTML 자동추출이므로, 인용 시 §번호는 `검토필요:`로 둔다.

## 문제 정의
- 자율 연구 에이전트는 "standalone applications with their own orchestration layers"를 요구한다. 반면 modern coding assistant는 연구 자동화에 필요한 기본 능력을 이미 제공한다.
- 핵심 질문: end-to-end 논문 생성을 별도 자율 플랫폼이 아니라 "기존 coding assistant 안의 재사용 skill 묶음"으로 돌릴 수 있는가?

## 아키텍처 — 13 composable skills, 8 stage (각 stage에 결정론적 gate)
| Stage | 작업 | 결정론적 Gate |
|---|---|---|
| 0 Input Routing | 입력 분류; Proposal Mode(데이터 없음) vs Data-Aware Mode(측정 데이터 있음) 선택 | Template Gate: venue spec 검증 |
| 1 Planning | research question·contribution·section 구조·notation·실험설계 추출 | Blueprint Gate: venue 구조 정합 |
| 2 Citation | 문헌 검색; DOI/arXiv/metadata로 검증; BibTeX 구축 | Citation Gate: malformed/미해결 key/일관성 |
| 3 Writing | blueprint+bib에 맞춰 LaTeX section 생성; 일관성 유지 | Manuscript Gate: 미해결 placeholder, mode별 result-integrity |
| 4 Refinement | 반복 제거·용어 정합·논증 개선·길이 조정 | 이전 gate 전부 재실행 |
| 5 Review | 다중 isolated review pass(기술 타당성·실험설계·증거강도); issue 검증 | issue는 특정 구절에 묶임; 3분류 검증 |
| 6 Figure | method figure: raster→HTML 재구성→vector PDF; result figure: 데이터에서 직접 plot | Figure Gate: artifact 존재, 정량 figure는 측정결과 grounding |
| 7 Assembly | section·bib·figure·template 결합→LaTeX 컴파일 | Compilation Gate: 인용·교차참조 해결된 컴파일 |
| 8 Experiment(조건부) | 증거 gap 식별·실행·provenance 검증·claim 수정 | evidence integrity; 실행불가는 결과 미기재 |

- Gate 메커니즘: 각 stage는 결정론적 검사를 통과해야 다음으로. Fatal violation은 실행 중단, warning은 기록하되 진행 허용.
- 명시적 한계: "Deterministic checks cannot determine whether an argument is sufficiently supported, whether different sections remain conceptually consistent" → model-based review 필요.

## 검증 스택
### 결정론적 integrity gate
- Template/Blueprint/Citation/Manuscript/Figure/Compilation gate (위 표).
- Manuscript Gate result-integrity는 mode별: Proposal Mode는 미관측 실증결과 거부, Data-Aware Mode는 공급 데이터가 뒷받침 안 하는 정량 진술 플래그.

### Self-Review (model-based, local)
- 편집 후 실행; 수정 내용을 주변 원고와 대조; terminology drift·redundancy·local inconsistency 수리.

### Adversarial Review (model-based, manuscript-level)
- 다중 isolated pass가 상보적 측면(theoretical soundness, experimental design, systems validity) 검토.
- 3-Way Validation Protocol (§5.2): ① 문제가 원고에 실제 존재하나 ② 다른 곳에서 이미 다뤄졌나 ③ 명시 scope 안인가. 하나라도 실패하면 폐기, 생존 issue만 수정 회부.

### 사전등록 (experiment planning)
- 실행 전 planning stage가 dataset·baseline·metric·ablation·result table을 명시. "The table structure is fixed in advance, while numerical cells remain empty until the corresponding experiments are completed." lightweight preregistration.

### Claim Admission Protocol (Appendix C)
- 실험 후 claim에 5라벨: supported, partially-supported, unsupported, contradicted, needs-confirmation.
- 조치: supported/partially→근거 맞춰 유지·좁힘; unsupported→실험/약화/삭제; contradicted→삭제 or 한계로; needs-confirmation→저자 확인(미해결로 남길 수 없음). 수정은 abstract·intro·results·conclusion 전 occurrence로 전파.

### Self-Refutation Loop bounding
- 실패모드: 시스템이 자기 결과가 원 가설을 지지 안 한다고 반복 결론내면서 같은 방향으로 계속 수정.
- 처방: experiment–critique–revision cycle을 7회로 bound. 한계 후에도 미지지면 trajectory 종료 + "failure report"(원 아이디어·시도 방법·관측 결과·불충분 사유) 기록, 억지 성공 안 함. 이후 새 아이디어로 전체 파이프라인 재실행.

## 평가 수치 (전부 CI 포함)
### Citation validity (외부 서지 metadata 검증, in-pipeline과 독립)
- Spark-to-Paper(full): 99.5% [98.4–100%], 384 refs / 8 papers.
- Human preprint: 97.8% [94.6–99.4%], 320 refs.
- AI Scientist 93%(42/45), AI Scientist-v2 91%(58/64), Agent Laboratory 96%(27/28), single-pass LLM 81%[76–86%].

### Figure editability
- Spark-to-Paper 96.4% [92.7–98.6%] of ~1,900 ground-truth figure elements editable.
- Human preprint 58% [44–71%]. 이전 자율 시스템 0–3%(raster 임베드).

### Fabrication detection — ablation (36 seeded probe, 10 failure family, 3 source)
| 구성 | detection | precision |
|---|---|---|
| single-pass draft(gate 없음) | 14% (5/36) [6–29%] | N/A |
| +gate | 69% (25/36) [53–82%] | N/A |
| +gate+self-review | 81% (29/36) [65–90%] | N/A |
| +gate+self-review+adversarial | 92% (33/36) [78–97%] | 74% (42/57 issue) [61–83%] |
- adversarial precision: blinded 60 sampled issue, "cannot tell" 3 제외 → 57 denominator.

### 생성 효율
- 비용 $8.1 [6.9–9.6]; token 11.9M [10.2–13.7M]; wall-clock 3.2h [2.6–3.9h], 8 topic.
- 증분(3-topic subset): gate +8.1M±0.9M tok/+$5.3±0.5; self-review +1.1M±0.2M/+$0.6±0.1; adversarial +2.6M±0.4M/+$1.6±0.2.
- single-pass baseline: 0.11M tok($0.66, 16 min). 이전 시스템 $10–25/run 또는 $2.33–$20–25/attempt.

### 평가 범위
- primary: 외부 선정 8 research topic(사전등록). single-pass와 paired 비교는 3 topic. human preprint audit 8편. 이전 시스템 audit는 공개 artifact(재실행 없음).
- cross-template robustness: 언급되나 main table에 수치 없음.

## Baseline·비교 방법
- AI Scientist(Lu 2024)·AI Scientist-v2(Yamada 2025), Agent Laboratory(Schmidgall 2025): 공개 논문 audit. single-pass LLM(같은 Claude backbone, gate/review 없음, in-house). human preprint.
- 이전 시스템은 재실행 없이 "publicly released papers and artifacts"의 값만 사용, model backbone·pricing 정규화 안 함. "mark unavailable measurements as not reported rather than estimating them."

## 저자 명시 한계·caveat
1. claim-level 증거 판정이 현재 model-based ("determining whether a particular piece of evidence semantically supports a claim is currently performed by the model") → auditing 필요한 약점으로 인정.
2. 실험 feasibility: 자원 없으면 missing dependency 기록 + 결과 미기재. 자원 gap 자동해결 아님.
3. Self-Refutation 7-iteration bound는 명시적 정당화 없이 선택; 도메인별로 다를 수 있음.
4. figure 재구성 신뢰성: 소수 correction round로 대개 복원, 불가 시 raster fallback.
5. model/tool 분리 불완전: adversarial review는 여전히 3분류 수동 검증 필요.
6. 평가 범위 제한: 8 controlled topic, human preprint 8편(체계적 audit 아님).

### 투명성 조치
- 사전등록 프로토콜 + 외부 timestamp. "Report all outcomes regardless of whether they favor Spark-to-Paper." CI는 개별 run이 아니라 paper 단위(n>3). 비용·token 불확실성 범위 공개. 이전 시스템과 pricing/model 가정 다름 인정.

## 핵심 claim + 저자 caveat
1. end-to-end 통합(13 skill, 별도 platform 불요). caveat: Claude Code backend 필요, 타 구현 없음.
2. 증거-grounded 생성(planning↔reporting 분리로 사후 프로토콜 적응 위험 감소). caveat: preregistration은 lightweight·non-binding, model이 여전히 사후 claim 판정.
3. citation validity 99.5%. caveat: 외부 metadata 검증이라 인용의 의미적 정확성·맥락 적절성은 보증 안 함.
4. fabrication detection 14→92%. caveat: 36 probe/10 family만, failure coverage 제한.
5. Self-Refutation bounding이 억지 성공 방지. caveat: "some trajectories may fail in the same way", coherent claim 산출분만 최종 원고 → 모든 거부 trajectory가 진짜 불가능인지 보증 안 함.
6. figure editability 96.4%. caveat: 의도적 raster 제외, human 58%라 생성 explanatory figure가 오히려 editable 하기 쉬운 셈.

## 산출물(Table 6, Appendix D)
- blueprint.json, template.json, refs.bib, claims_map.json, sections/*.tex, figures/, results.facts.json, main.tex/pdf, logs/*.io.md.

## 재현성
- GitHub: https://github.com/Spark-To-Paper-Skills/spark-to-paper-skills
- corresponding: wangwenhao@vastilab.com
- Claude Code + Claude model family 사용. 소스 릴리스 명시 없음(위 GitHub 예고). Appendix D: venue별 동작을 hard-code 아니라 JSON spec으로.
- case study 도메인: clinical risk screening, PM2.5 forecasting. Figure count는 self-reported(존재 증거이지 benchmark 아님).
- fabrication probe corpus 36개, review precision 60 issue(57 usable), citation audit 384 ref(human 320).
