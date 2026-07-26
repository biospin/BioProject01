<!-- CLAUDE.md의 "Agent routing & artifact contract (논문 생산 하네스)" 섹션 교체본 (after). 승인 시 라이브 CLAUDE.md의 해당 섹션을 이 내용으로 교체. -->

## Agent routing & artifact contract (논문 생산 하네스)  【after / 검토용】

> 재사용 스캐폴드(Designed by Ka-Kyung Kim, CC BY 4.0) 설치본. 정본 명세 = 리포 루트 **`harness.yaml`**(SSOT). 전체 랩 지도 = `docs/HARNESS.md`. 도메인 슬롯 = `hspc-velocity-analyst`(project profile).

### 실행 전제 (먼저)
- **repo 루트에서 실행.** 상위 디렉터리 실행 시 프로젝트 agent 미로드 → 범용 폴백. **범용 agent로 대체 금지, 필수 누락 시 중단.** (BIOP01-65)
- 단일 컨텍스트 = `pipeline/hspc-velocity-benchmark/manuscript/PAPER_DIRECTION.md` — 논문 멤버는 작업 전 로드.

### 자연어 라우팅
| 요청 (자연어) | 첫 agent |
| --- | --- |
| "분석 돌려줘 / 재실행 / eval·통계 / cross-dataset 재현" | `hspc-velocity-analyst` |
| "프리프린트/저널/블로그 초안·섹션" | `manuscript-writer` |
| "그림 만들어줘 / 그림 번호 정리" | `manuscript-writer` (runs `figures/figNN_*.py`) |
| "선행연구 / related work / 스쿱 확인" | `literature-scout` |
| "차별화 각도 / 뭘 새로 해야 하나" | `novelty-strategist` |
| "가설·실험설계·분석계획 점검·감사" | `research-methodologist` |
| "제출 전 적대적 자체검토 / 그림 QA" | `paper-critic` |
| "정식 venue 리뷰 시뮬레이션" | `venue-reviewer` *(프로젝트 로컬, 미구현 시 이 요청은 건너뛰고 안내)* |
| "발표자료/슬라이드/발제" | `presenter` |
| "로고·아이콘·브랜드·그림 미감" | `design` |
| "여러 단계 순서 계획만" | `paper-planner` (계획만; 실행은 메인 루프 `paper-runner`) |

**여러 단계를 엮는 요청 → orchestrator Skill `paper-production-orchestrator`(→`paper-runner`).** RUN_STATE 기준으로 다음 단계만 실행, 필수 누락 시 중단, 미승인 게이트 건너뛰기 금지.

### 산출물 계약
| 단계 | Writer | 산출물 | 다음이 읽음 |
| --- | --- | --- | --- |
| 분석·eval | `hspc-velocity-analyst` | `results/FINDINGS.md` + `results/*.csv/*.md` | 결과검증·집필 |
| 결과 검증(자동) | (스크립트) | `p3_concordance` + `p3_crossdataset_concordance` + `p3_scrambled_null` 재계산 → FINDINGS 대조 | 집필 |
| 집필+그림 | `manuscript-writer` | `manuscript/draft_v2.md` + `draft_v2_ko.md`, `figures/*.png` | 검수·리뷰 |
| 검수 | `paper-critic` | 적대 노트 + 그림 QA | 집필(수정) |
| (선택) 리뷰 | `venue-reviewer` | `manuscript/REVIEW-<venue>-<date>.md` | 집필(수정) |
| 패키지 검증(자동) | (스크립트) | 원고 숫자=결과 파일, 그림 재생성, commit/데이터 고정 | 사람 |
| 발표 | `presenter` | 슬라이드/발제 | 사람 |
| 상태 | (전원) | `RUN_STATE.yaml`, `CLAIMS.yaml`, `HANDOFF.md`, `SESSION-LOG.md` | 다음 세션 |

**게이트 3분류**: 자동 무결성(결과·패키지 검증, `harness_doctor`) / 과학적 판단(claim-defensibility — advisor 사람 포함) / 공개·거버넌스(저자·소속·IP — 사람). 커밋·push는 자동, **프리프린트/blog 공개와 main 병합만 사람 승인**.
