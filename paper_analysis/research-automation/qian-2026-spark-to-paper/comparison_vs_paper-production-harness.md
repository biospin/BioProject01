# Spark-to-Paper vs paper-production-harness (최신본) — 대조

> 작성 2026-08-18(백그라운드). 근거: `sources/fulltext_extract.md` + 상류 harness 최신 main(PR#4·#5 병합, verify-depth 포함).
> 목적: kkkim 지시 — Spark-to-Paper 상세분석 후 우리 하네스 최신본과 재비교, 티켓에 명시.

## 0. 한 줄
Spark-to-Paper(arXiv:2608.11924)는 우리 하네스와 **독립적으로 같은 설계에 수렴**했다. 최신 verify-depth 반영 후, **우리가 더 깊은 축**(게이트 자체 검증·독립성 사다리)은 유지되고, **그들이 앞선 축**(정량화·claim taxonomy·비용 벤치)이 우리 도입 후보로 남는다.

## 1. 수렴 (둘 다 도달한 설계 — 이미 공통)
| 설계 원칙 | Spark-to-Paper | 우리 harness |
|---|---|---|
| 파일 아티팩트로 stage 소통 | blueprint.json·refs.bib·results.facts.json·sections/*.tex | 산출물 계약(FINDINGS.md·draft_v2·CLAIMS.yaml) |
| 결정론 gate vs 의미판단(model review) 분리 | deterministic gate + model review 명시 분리 | DESIGN_NOTES "검수 2단계" + verify-harness Layer1/3 |
| 실험 preregistration(표 먼저·셀 공백) | planning stage가 표 구조 고정 | DESIGN_NOTES 사전등록 절 + PREREGISTRATION 봉인 |
| self-refutation cap → 실패 리포트 | 7-iteration cap, 억지 성공 금지 | DESIGN_NOTES "실패는 실패 리포트로" + claim-defensibility |

→ 이 4가지는 이미 양쪽 공통. DESIGN_NOTES의 Spark-to-Paper 선례 절이 이 수렴을 기록함.

## 2. 우리가 더 깊은 축 (Spark-to-Paper에 없음)
| 우리 자산 | 무엇 | 그들의 상태 |
|---|---|---|
| **mutation(게이트 자체 검증)** | 알려진 결함 주입해 게이트가 잡나 확인(watchmen). 못 잡으면 NOT_TESTED | **없음** — gate가 공허한지(실데이터서 아무것도 안 봐도 통과) 검사 안 함 |
| **fail-closed(VACUOUS≠pass)** | CAUGHT/SURVIVED/VACUOUS 판정 분리, 빈 evidence·조회실패는 pass 불가 | 없음(gate 통과=OK로 봄) |
| **circular-evidence 격리** | 검증 리포트를 검사 코퍼스 밖에 | 명시 없음(파일 아티팩트라 노출 가능) |
| **cross-model + 사람 독립성 사다리** | Lv1 same-model→Lv3 결정론→Lv5 cross-model→Lv8 사람/advisor | adversarial review가 **same-model isolated pass** → **precision 74%(오탐 26%)**. 다른 모델·사람 계단 없음 |
| **재계산 diff-0(byte-identical)** | 게이트 산출물이 커밋값과 diff 0인지 | 결과 grounding은 하나 diff-0 명시 없음 |

★ 특히 그들의 adversarial review precision 74%(오탐 26%)는 same-model 한계의 실측 증거 — 우리 Lv5·Lv8 사다리가 그 위에 필요한 이유를 그들 데이터가 뒷받침한다.

## 3. 그들이 앞선 축 (우리 도입 후보 = 이 대조의 핵심 산출)
| 그들 자산 | 수치/내용 | 우리 갭 · 도입안 |
|---|---|---|
| **정량 fabrication-detection ablation** | single-pass 14% → +gate 69% → +self-review 81% → +adversarial 92% (36 probe) | 우리는 mutation **도구는 있으나 헤드라인 탐지율 미산출**. → **도입1: verify-harness Layer2 mutation 스위트를 돌려 "우리 게이트 결함 탐지율 N%"를 내고 "그들 92% vs 우리 N%" 비교축 확보**(BIOP01-84·§6.1 정량 근거) |
| **Claim Admission 5라벨** | supported/partially/unsupported/contradicted/needs-confirmation + 라벨별 조치 + 전 occurrence 전파 | 우리 claim-defensibility는 PROVISIONAL 이진에 가까움. → **도입2: 5라벨 taxonomy를 CLAIMS.yaml claim ledger에 접목**(needs-confirmation=사람 확인 강제가 특히 유용) |
| **비용/토큰/시간 벤치** | $8.1·11.9M tok·3.2h/편, 증분(gate +$5.3 등) | 우리 파이프라인 실행비용 미기록. → **도입3(선택): 실행비용 기록으로 효율·재현성 주장** |
| **citation validity 정량 대비** | 99.5% vs human 97.8% vs prior 81–96%, 외부 metadata 검증 | 우리 verify_citations는 있으나 정량 벤치 미보고. → **도입4(선택): 인용정합률을 human/prior 대비로 보고** |
| **figure editability 지표** | raster→HTML→vector PDF, 96.4% editable | 우리 그림은 결과파일 생성이나 editability 지표 없음. → 참고(우리 그림 스크립트에 vector 유지 규율 추가 검토) |

## 4. 도입 우선순위 (권고)
1. **도입1 (정량 mutation ablation)** — 값 가장 큼. 우리 verify-harness Layer2가 이미 그 도구. "그들 92% vs 우리 N%"는 §6.1(BIOP01-81)·검증하네스(BIOP01-84) 논지를 정량화하고, Spark-to-Paper를 직접 인용해 방어.
2. **도입2 (Claim Admission 5라벨)** — claim ledger 정련. needs-confirmation 강제가 우리 "note≠contradiction, 사람 이관"과 정합.
3. 도입3·4 (비용·citation 벤치) — 선택, 하네스를 글로 쓸 때.

## 5. 인용 전략
Spark-to-Paper는 우리가 하네스를 글로 쓸 때(BIOP01 §6.1 AI Scientist 검증게이트, 또는 방법 노트) **직접 prior art**. 
- 우리 차별점(mutation·독립성 사다리)을 그들 한계(게이트 공허성 미검·precision 74%)와 대비해 서술.
- 그들 92% ablation을 "검증 스택이 fabrication을 잡는다"의 외부 근거로, 우리 mutation 수치를 그 위에 배치.
- BibTeX: `@qian2026sparktopaper` (arXiv:2608.11924).

## 6. cytogenbi·claude 재출현 진단 (별건, kkkim 지시)
- **main·live Contributors: 이미 깨끗**(kakyungkim·Geongyu만, cytogenai·claude 0).
- 잔재는 **GitHub 불변 PR ref `refs/pull/1/head`=3c54903**(옛 초기 커밋, cytogenai@gmail.com + Claude Fable 트레일러)에만. **force-push로 제거 불가**(GitHub 관리 immutable, PR 삭제 불가).
- contributor 그래프는 default branch(main) 기준이라 이미 깨끗 — 재출현은 **그래프 캐시**. 완전 purge는 GitHub Support 또는 repo 재생성(파괴적)뿐. → 상세·옵션은 티켓.
