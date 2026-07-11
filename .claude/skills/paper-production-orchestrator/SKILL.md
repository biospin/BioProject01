---
name: paper-production-orchestrator
description: 논문 생산 루프의 입구(진행표/팀장). "논문 풀 파이프라인 돌려줘", "프리프린트 업데이트해서 제출 준비", "분석→집필→그림→검수까지 한 번에", "그림만 다시", "리뷰만 다시", "critic 지적 반영해", "최신 결과로 본문 갱신" 같이 분석·집필·그림·검수·검증·발표를 엮는 요청에서 사용한다. 기존 멤버(hspc-velocity-analyst, manuscript-writer, 그림 스크립트, paper-critic, reviewer, presenter)를 정해진 순서로 호출하고 부분 재실행을 처리한다. 새 agent는 만들지 않는다.
---

# paper-production-orchestrator (논문 생산 루프 진행표 / 팀장) — HSPC velocity-lag benchmark

이 Skill은 **메인 루프(PI)가 실행**한다. 메인 루프는 Agent 도구로 멤버를 직접 부를 수 있으므로, "계획만" 하는 `paper-orchestrator`(agent)와 달리 실제로 루프를 돌린다. 멤버는 전부 기존 정의를 재사용한다 — 신규 agent 0개.

전체 랩 구조·멤버 JD는 `docs/HARNESS.md`, 라우팅·산출물 계약 요약은 `CLAUDE.md`의 *Agent routing & artifact contract* 참조.

## 언제 이 스킬을 쓰나
- 초기/전체: "논문 풀 파이프라인", "프리프린트 업데이트해 제출 준비", "분석부터 발표까지".
- 부분 재실행: "그림만 다시", "리뷰만", "분석만 다시", "발표만".
- 보완/이어서: "critic 지적 반영", "최신 결과로 본문 갱신".

## 실행 모드 분기 (먼저 확인)
1. 산출물 존재·최신 여부 확인:
   - result files: `pipeline/hspc-velocity-benchmark/results/FINDINGS.md` + `results/*.csv` + `results/*.md`
   - manuscript files: `pipeline/hspc-velocity-benchmark/manuscript/draft.md` (+ `refs.bib`, `supplementary.md`), figures: `pipeline/hspc-velocity-benchmark/figures/`
2. 분기:
   - **없음 / "풀 파이프라인" / "제출 준비"** → 초기·전체(전 단계).
   - **있음 + 특정 부분 요청** → 부분 재실행(해당 단계만, 나머지 기존 파일 재사용).
   - **"지적 반영" / "최신 결과로 갱신"** → 변경 지점의 **하류 단계만** 다시.
3. `hspc-velocity-analyst`가 LLM 기반 sub-분석을 쓰는 경우, **offline mock 경로**(API 키 미설정 등)로 돌았는지 확인한다. mock이면 "실 결과 아님 / 데모"를 보고에 명시한다.

## 멤버 구성 (전원 기존 재사용)
`hspc-velocity-analyst`(도메인 분석 슬롯), manuscript-writer(그림 포함 — `figures/figNN_*.py` 스크립트 실행), paper-critic, reviewer, presenter. (기획 단계 선택: research-methodologist, literature-scout, novelty-strategist.)

> 참고: 그림 생성은 **agent가 아니라 스크립트**로 둔다. `manuscript-writer`가 `pipeline/hspc-velocity-benchmark/figures/figNN_*.py`(예: `fig01_p2_concordance.py`)를 실행해 결과 파일에서 그림을 만든다. 단순 재생성이면 메인 루프가 직접 그 스크립트를 돌려도 된다(결정론적).

## 품질 기준선
- **Headline = "velocity 기반 chromatin→transcription lag은 cross-method/cross-dataset로 robust하게 재현되지 않는다(method에 대한 주장); transcription rate α는 재현된다."** 통계가 뒷받침하지 않는 우월/재현 주장 금지. weak ≠ zero.
- 숫자는 결과 파일·검증된 base에서만(메모리 재유도 금지). bootstrap CI + 적절한 유의성 검정 동반.
- pseudotime≠wall-clock, within-lineage, permutation FDR, lag sign 구조적 양수(무정보) 규율 유지.
- 그림은 결과 파일에서 생성(하드코딩 금지), 번호는 첫 언급 순, 95% CI + paired test 표시.

## 실행 흐름
0. **단일 컨텍스트 로드 (매 실행 필수)** — `manuscript/PAPER_DIRECTION.md`를 먼저 읽는다. 현재 thesis·claim 등급표·loop 규율·진행상태가 여기 있다. 멤버 호출 전 이 문서를 컨텍스트로 전달(매번 재브리핑 불필요 = 하나의 시스템).
1. **모드 분기** → 실행할 단계 집합 결정.
2. **(선택) 기획·근거** — 새 방향일 때만: research-methodologist / literature-scout / novelty-strategist. 산출된 새 claim은 등급 **PROVISIONAL**로 표기.
2.5. **claim-defensibility 게이트 (신설 — headline/novelty claim이 본문에 들어가기 전 필수)**:
   - 새 framing/claim마다 3종 세트 확인: ① **반증기준**(무엇이 관측되면 틀린가) ② **가장 값싼 make-or-break 검정**(기존 데이터 우선, 예: `results/identifiability_vs_snr.md`가 템플릿 — 곡률이 SNR 넘는지 partial corr로 반증 시도) ③ **advisor 확인**.
   - 검정 실패/약화 → claim 등급을 내리고 `PAPER_DIRECTION.md §2` 표를 즉시 갱신(**사후 구제 금지**). 통과 전 claim은 draft·사전등록에 쓰지 않는다.
   - 확증용 신규 데이터 예측은 **결과 전 commit 봉인**(`PREREGISTRATION_*.md`), 임계값 사후조정 금지.
   - **2층 융합 금지**: within-method fit 품질을 cross-method 재현성으로 승격 금지.
3. **분석·eval** — `hspc-velocity-analyst` → `results/FINDINGS.md` + result 파일 갱신. mock 경고 확인.
4. **집필 + 그림** — `manuscript-writer` → `manuscript/draft.md`. 그림은 `figures/figNN_*.py` 실행 → `figures/`. 그림만 재실행이면 이 단계만(결정론적, 결과 파일에서 생성).
5. **검수** — `paper-critic`(적대적 + 그림 시각 QA) → 지적 노트. 블로킹이면 6으로, 경미하면 메모만.
6. **수정** — `manuscript-writer`가 critic 지적 반영 → 본문 갱신.
7. **(선택) 정식 리뷰** — 요청 시 `reviewer` → `manuscript/REVIEW-<venue>-<date>.md`.
8. **검증 게이트** — 아래 verify-gate 실행. **실패하면 멈추고 사람에게 보고**, 커밋·발행하지 않는다.
9. **(선택) 발표** — 요청 시 `presenter` → 덱·발제.

각 단계 산출물은 **파일로 남긴다**. 다음 단계는 그 파일을 읽는다.

## 검증 게이트 (헤드라인 숫자 결정론적 재계산)
```bash
cd pipeline/hspc-velocity-benchmark/scripts
conda run --no-capture-output -n scv-preprocess python p3_concordance.py
conda run --no-capture-output -n scv-preprocess python p3_crossdataset_concordance.py --dataset human_brain
conda run --no-capture-output -n scv-preprocess python p3_scrambled_null.py
# 출력된 숫자를 results/FINDINGS.md + concordance*.md 와 대조. 불일치 → 멈춤·보고.
```

## 산출물 계약
| 단계 | 멤버 | 산출 파일 | 다음이 읽음 |
| --- | --- | --- | --- |
| 분석·eval | hspc-velocity-analyst | `results/FINDINGS.md`, `results/*.csv`, `results/*.md` | 집필·검수 |
| 집필 | manuscript-writer | `manuscript/draft.md`, `refs.bib`, `supplementary.md` | 검수·리뷰·발표 |
| 그림 | manuscript-writer (`figures/figNN_*.py`) | `figures/*.png` | 집필·검수 |
| 검수 | paper-critic | 적대 노트 + 그림 QA | 집필(수정) |
| 리뷰 | reviewer | `manuscript/REVIEW-<venue>-<date>.md` | 집필(수정) |
| 발표 | presenter | 슬라이드/발제 | 사람 |
| 상태 핸드오프 | (전원) | `HANDOFF.md`, `TODO.md`, `SESSION-LOG.md` | 다음 세션 |

## 실패 처리 / 멈춤 조건
- verify 게이트 실패 → **멈춤**, 무엇이 왜 실패했는지 보고.
- `hspc-velocity-analyst` sub-분석이 mock 경로 → 결과는 데모, "실 결과 아님" 명시.
- 단계 산출 파일이 안 생김 → 재시도 1회, 그래도 실패면 사람에게 보고.

## 사람 승인 게이트 (자동화하지 않음)
- **공개**(프리프린트/blog 게시)는 **저자·소속·IP·corresponding email 확정** 전까지 **보류**. 이 Skill은 절대 게시하지 않는다.
- 외부 발송(메일·메신저·제출)은 사람 승인 뒤에만.
- 커밋/푸시는 사람이 한다(무인 git 금지).

## 마무리
- 최종 보고에 **무엇을 어떤 순서로 돌렸고, 어떤 파일이 갱신됐고, verify 통과 여부, 남은 일**을 done/in-progress/blocked로 구분해 명시. 부분 재실행이면 "건드리지 않은 단계"도 명시한다.
