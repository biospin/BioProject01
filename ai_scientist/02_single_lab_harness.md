# 02. 레이어 A — 단일 랩 자동화 (한 AI가 논문 한 편을 끝까지)

한 연구자의 연구 과정 전체를 여러 agent 멤버가 나눠 맡아 자동으로 돌리는 구조다. 이 하네스를 "하나의 연구 랩"으로 보는 지도가 `docs/HARNESS.md`이고, 라우팅과 산출물 계약 요약은 `CLAUDE.md`의 *Agent routing & artifact contract* 절에 있다.

핵심 발상은 이렇다. agent는 직원이 아니라 랩의 **멤버(연구원)**이고, 사람과 메인 루프가 랩을 이끄는 **PI**다. PI는 무엇을 할지 정하고 승인·공개를 책임지되, 실제 작업은 멤버가 파일로 주고받으며 이어서 한다.

## 1. 멤버 명부

`.claude/agents/`에 정의된 멤버는 다음과 같다. 하나(`hspc-velocity-analyst`)만 이 프로젝트 도메인 전용이고, 나머지는 다른 논문에도 재사용할 수 있게 만들었다.

| 멤버 | 벤치 | 역할 |
| --- | --- | --- |
| `hspc-velocity-analyst` | 분석실 | 도메인 슬롯. HSPC velocity-lag 파이프라인(P0–P5)·eval·통계·cross-dataset 실행/확장, 결과 파일 유지 |
| `literature-scout` | 문헌·기획 | 선행연구 탐색, 정직한 포지셔닝, related work |
| `novelty-strategist` | 문헌·기획 | 차별화 각도와 가장 값싼 입증 실험 제안 |
| `research-methodologist` | 문헌·기획 | 가설·기여문·실험설계, 누수·통계 감사 |
| `manuscript-writer` | 집필실 | 프리프린트·저널·블로그 본문 초안과 그림 연계 |
| `presenter` | 집필실 | 청중 맞춤 슬라이드·발제 |
| `paper-critic` | 심사·QA | 제출 전 적대적 자체검토와 그림 시각 QA |
| `reviewer` | 심사·QA | 정식 venue 스타일 공식 리뷰(선택) |
| `paper-orchestrator` | 코디네이션 | 멀티 agent 작업의 **계획**만 수립(실행은 PI) |
| `design` | 엔지니어링 | 로고·아이콘·브랜드·그림 미감 |
| 그림 생성 스크립트 | 엔지니어링 | `figures/figNN_*.py`. 결과 파일에서 그림 생성·번호 정합 |

그림 생성을 agent가 아니라 결정론적 스크립트로 둔 점이 설계상의 선택이다. `manuscript-writer`가 스크립트를 실행해 결과 파일로부터 그림을 만들고, 단순 재생성이면 메인 루프가 직접 돌린다. 숫자를 손으로 하드코딩하지 않고 결과 파일에서만 뽑게 해 재현성을 지킨다.

## 2. 자연어 라우팅 — 누가 시작할지 사람이 매번 안 정한다

요청에 agent 이름이 없어도 `CLAUDE.md`의 라우팅표가 자연어 요청을 멤버에 배정한다. 예를 들면 이렇게 나뉜다.

- "분석 돌려줘 / 재실행 / eval·통계 / cross-dataset 재현" → `hspc-velocity-analyst`
- "프리프린트·섹션 써줘 / 그림 만들어줘" → `manuscript-writer`
- "선행연구 / 스쿱 확인" → `literature-scout`
- "차별화 각도 / 뭘 새로 해야 하나" → `novelty-strategist`
- "가설·실험설계 점검·감사" → `research-methodologist`
- "제출 전 자체검토 / 그림 QA" → `paper-critic`
- "발표자료 / 슬라이드" → `presenter`

여러 단계를 엮는 요청("분석→집필→그림→검수까지", "critic 지적 반영해")은 단일 멤버가 아니라 오케스트레이터 Skill로 보낸다.

## 3. 오케스트레이터 — 여러 단계를 정해진 순서로

`paper-production-orchestrator` Skill(`.claude/skills/paper-production-orchestrator/SKILL.md`)이 논문 생산 루프의 입구다. 메인 루프(PI)가 이 Skill을 실행하며 멤버를 순서대로 부른다. subagent는 subagent를 못 부르므로, "계획만 짜는" `paper-orchestrator` agent와 달리 실제 실행은 이 Skill이 맡는다.

실행 흐름은 다음과 같다.

```
0. 단일 컨텍스트 로드 — manuscript/PAPER_DIRECTION.md 를 먼저 읽는다
   (현재 thesis · claim 등급표 · loop 규율 · 진행상태. 멤버 호출 전 이 문서를 넘긴다)
1. 모드 분기 — 풀 파이프라인 / 부분 재실행 / 하류만 다시
2. (선택) 기획·근거 — research-methodologist / literature-scout / novelty-strategist
2.5 claim-defensibility 게이트 — headline·novelty claim이 본문에 들어가기 전 필수
3. 분석·eval — hspc-velocity-analyst → results/FINDINGS.md
4. 집필 + 그림 — manuscript-writer → draft_v2.md + draft_v2_ko.md, figures/*.png
5. 검수 — paper-critic (적대적 + 그림 시각 QA)
6. 수정 — manuscript-writer 가 지적 반영
7. (선택) 정식 리뷰 — reviewer → REVIEW-<venue>-<date>.md
8. 검증 게이트 — 헤드라인 숫자 결정론적 재계산 (실패하면 멈추고 사람에게 보고)
9. (선택) 발표 — presenter
```

핵심은 **부분 재실행**이다. 이미 만들어진 산출물이 있으면 요청한 단계만 다시 돌리고 나머지는 기존 파일을 재사용한다. "그림만 다시"면 4단계만, "최신 결과로 본문 갱신"이면 변경 지점의 하류 단계만 돌린다.

## 4. 산출물 계약 — 대화가 아니라 파일로 넘긴다

멤버는 중간 결과를 대화에만 남기지 않고 정해진 파일로 넘긴다. 다음 멤버는 그 파일을 읽고 이어서 일한다.

| 단계 | Writer | 산출물 | 다음이 읽음 |
| --- | --- | --- | --- |
| 분석·eval | hspc-velocity-analyst | `results/FINDINGS.md` + `results/*.csv` + `results/*.md` | 집필·검수 |
| 집필·그림 | manuscript-writer | `manuscript/draft_v2.md` + `draft_v2_ko.md`(영/한 동시), `figures/*.png` | 검수·리뷰·발표 |
| 검수 | paper-critic / reviewer | `manuscript/REVIEW-<venue>-<date>.md` | 집필(수정) |
| 발표 | presenter | 슬라이드·발제 | 사람 |
| 상태 핸드오프 | 전원 | `HANDOFF.md`, `TODO.md`, `SESSION-LOG.md` | 다음 세션 |

이 계약 덕분에 멤버가 교체되거나 세션이 끊겨도 작업이 이어진다. 다음 주체가 산출물 파일 하나만 읽으면 착수할 수 있다는 기준을 지킨다.

## 5. 실험 실행 엔진 — 파이프라인 P0–P5

분석 단계의 실제 계산은 `pipeline/hspc-velocity-benchmark/scripts/`가 담당한다. `hspc-velocity-analyst`가 이 스크립트들을 돌려 결과 파일을 만든다. 내부 단계 표기는 P0부터 P5까지다.

- **P0: 다운로드·provenance.** `download_data.sh`로 GSE209878를 받고 `download_manifest.tsv`(sha256)와 `P0_provenance.md`를 남긴다.
- **P1: 통일 전처리.** `p1_build.py`가 공통 branch를 만든다. 여기서 preprocessing 차이와 method 차이를 분리한다.
- **P2: velocity method 실행.** `p2_multivelo.py`, `p2_moflow.py`, `p2_crakvelo_*`, `p2_multivelovae.py` 등으로 여러 method를 같은 전처리 위에서 돌린다.
- **P3: 재현성 검증.** `p3_concordance.py`, `p3_crossdataset_concordance.py`, `p3_scrambled_null.py`로 method 간·dataset 간 일치도와 null을 계산한다.
- **P4: permutation FDR.** gene 단위 다중검정을 통제한다.
- **P5: bootstrap 안정성.** shuffle/seed 변이 audit(`p10*`)까지 포함해 결과의 흔들림을 잰다.

method 선택의 근거는 `DESIGN.md`와 `paper_analysis/`의 dual-lens 분석 14편에 있다. 프레임워크별로 conda env를 격리(`env/`)해 의존성 충돌을 막는다.

## 6. 게이트 — 자동화가 넘지 못하는 선

이 랩은 전부를 자동으로 밀지 않는다. 두 종류의 게이트가 있다.

**검증 게이트(커밋·공개 전).** 헤드라인 숫자를 결정론적으로 재계산해 결과 파일과 대조한다.

```bash
cd pipeline/hspc-velocity-benchmark/scripts
conda run --no-capture-output -n scv-preprocess python p3_concordance.py
conda run --no-capture-output -n scv-preprocess python p3_crossdataset_concordance.py --dataset human_brain
conda run --no-capture-output -n scv-preprocess python p3_scrambled_null.py
# 출력 숫자를 results/FINDINGS.md 와 대조. 불일치면 멈추고 사람에게 보고.
```

**사람 승인 게이트.** 프리프린트·블로그 외부 공개와 main 병합은 사람이 승인한다. 저자·소속·IP·corresponding email이 확정되기 전에는 공개를 보류한다(원고에 `<FILL>`로 표시). 작업 브랜치 `kkkim-pipeline`에 대한 커밋·push는 자동으로 수행하되, 이 검증·공개 게이트는 유지한다.

claim 자체에도 게이트가 있다. headline claim은 반증기준, 가장 값싼 make-or-break 검정, advisor 확인을 통과하기 전에는 PROVISIONAL로 두고 본문에 넣지 않는다. within-method 적합 품질을 cross-method 재현성으로 승격하지 않는다는 규율(2층 융합 금지)도 여기에 든다.
