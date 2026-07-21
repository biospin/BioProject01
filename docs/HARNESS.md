# HARNESS.md — 랩 구조 (Agent 하네스 지도) — HSPC velocity-lag benchmark

*Designed by Ka-Kyung Kim, 2026 — a reusable paper-production harness, contributed as a scaffold (CC BY 4.0).*

이 문서는 이 프로젝트의 `.claude` 하네스를 **하나의 연구 랩**으로 본 지도다.
각 agent는 직원이 아니라 **랩의 멤버(연구원)** 이고, 사람(+메인 루프)이 랩을 이끄는 **PI**다.
운영 규칙·라우팅·산출물 계약 요약은 `CLAUDE.md`의 *Agent routing & artifact contract* 에 둔다. 이 파일은 그 확장판(멤버 명부 + 관계도 + JD)이다.

- 멤버는 **누가 일을 시작할지** 사람이 매번 지정하지 않아도, CLAUDE.md 라우팅표로 자연어 요청에서 배정된다.
- 멤버는 결과를 **대화에만 남기지 않고** 산출물 계약(아래)에 따라 파일로 넘긴다.
- `paper-orchestrator`는 *계획만* 짠다. 실제 멤버 호출(실행)은 PI/메인 루프가 `paper-production-orchestrator` **Skill**로 한다 — subagent는 subagent를 못 부르기 때문.

---

## 1. 멤버 명부 (Roster)

| # | 멤버 | 소속 벤치 | 한 줄 역할 | 상태 |
| --- | --- | --- | --- | --- |
| D | `hspc-velocity-analyst` | 분석실 | **(도메인 슬롯)** HSPC velocity-lag 파이프라인(P0–P5)·eval·통계·cross-dataset 실행/확장, result 파일 유지 | ✅ 채움 |
| 1 | `literature-scout` | 문헌·기획 | 선행연구 탐색·정직한 포지셔닝·related work | 재사용 |
| 2 | `novelty-strategist` | 문헌·기획 | 차별화 각도 + 가장 싼 입증 실험 제안 | 재사용 |
| 3 | `research-methodologist` | 문헌·기획 | 가설·기여문·실험설계, 누수/통계 감사 | 재사용 |
| 4 | `manuscript-writer` | 집필실 | 프리프린트/저널/블로그 본문·초안 + 그림 연계 | ✅ 채움(저자/소속 FILL 잔여) |
| 5 | `presenter` | 집필실 | 슬라이드·발표·발제(청중 맞춤) | ✅ 채움(경로) |
| 6 | `paper-critic` | 심사·QA | 제출 전 적대적 자체검토 + 그림 시각 QA | 재사용 |
| 7 | `paper-orchestrator` | 코디네이션 | 멀티-agent 작업 **계획** 수립(실행은 PI) | 재사용 |
| 8 | `design` | 엔지니어링 | 로고·아이콘·브랜드·그림 미감(SVG/PNG) | 재사용 |
| 9 | `reviewer` (전역, 선택) | 심사·QA | 정식 venue 스타일 공식 리뷰 문서 | 선택 |
| S | 그림 생성 (스크립트) | 엔지니어링 | `figures/figNN_*.py` — 결과 파일에서 그림 생성·번호 정합 | ✅ (스크립트) |

> ⚠️ 그림 생성은 스크립트로 둔다. `manuscript-writer`가 `pipeline/hspc-velocity-benchmark/figures/figNN_*.py`(예: `fig01_p2_concordance.py`)를 실행해 만든다. 단순 재생성은 메인 루프가 직접 돌려도 된다(결정론적).

---

## 2. 관계도 (Org / collaboration chart)

```
                         PI = 사람 + 메인 루프
                    (호출·승인·공개 게이트 책임)
                              │  실행 입구 = paper-production-orchestrator (Skill)
                    ┌─────────┴─────────┐
                    │  paper-orchestrator│  ← 계획만(실행 X)
                    └─────────┬─────────┘
   ┌──────────────┬──────────┼───────────────┬──────────────┐
   ▼              ▼          ▼                ▼              ▼
 문헌·기획      분석실      집필실          심사·QA       엔지니어링
 ────────      ──────      ──────          ───────       ──────────
 literature-   hspc-       manuscript-     paper-critic  design
   scout        velocity-   writer         reviewer(선택) [그림 생성=
 novelty-       analyst     presenter       (그림 QA는     figNN_*.py,
   strategist                               paper-critic)   run by writer]
 research-
   methodologist
```

### 일이 흐르는 표준 경로 (논문 생산 루프)
```
research-methodologist / literature-scout / novelty-strategist   (기획·근거: paper_analysis/ 14편)
        └─▶ hspc-velocity-analyst ──▶ results/FINDINGS.md + results/*             (분석·검증)
        └─▶ manuscript-writer ──▶ manuscript/draft.md                            (집필)
                 ║  figures/figNN_*.py ──▶ figures/*.png                          (그림)
        └─▶ paper-critic ──▶ reviewer ──▶ manuscript/REVIEW-*.md                 (심사)
                 └─▶ (수정 반영) manuscript-writer
        └─▶ verify-gate(p3_concordance + p3_crossdataset_concordance + p3_scrambled_null) ──▶ presenter
```
- **검증 게이트**(헤드라인 숫자 결정론적 재계산)와 **공개 게이트**(저자·소속·IP 검토)는 PI가 통과시킨다.

---

## 3. 멤버별 JD 요약
권위 있는 전체 정의는 각 `.claude/agents/<name>.md` 본문. (분석=hspc-velocity-analyst; 집필=manuscript-writer; 발표=presenter; 검수=paper-critic; 기획=literature-scout/novelty-strategist/research-methodologist; 계획=paper-orchestrator; 디자인=design.)

---

## 4. 현재 하네스 상태 (성숙도)

| 항목 | 상태 |
| --- | --- |
| 멤버(agent) 정의 | ✅ 재사용 7 + 도메인 슬롯(hspc-velocity-analyst) 채움 |
| 자연어 라우팅 | ✅ CLAUDE.md 라우팅표 적용 |
| 산출물 계약 | ✅ 경로 검증(results/, manuscript/, figures/) |
| 입구(Orchestrator **Skill**) | ✅ `.claude/skills/paper-production-orchestrator/SKILL.md` |
| 검증 게이트 | ✅ `p3_concordance.py` + `p3_crossdataset_concordance.py` + `p3_scrambled_null.py` 재계산 |
| 개선 루프 | `SESSION-LOG.md`(세션별 회고 누적) |
| 미결(사람 확정) | 저자·소속·corresponding email·공개 정책 — manuscript-writer의 `<FILL>` |
