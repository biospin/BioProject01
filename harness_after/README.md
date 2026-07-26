# harness_after/ — 논문 생산 하네스 교체용 "after" 버전 (검토 대기)

- 작성 이건규 · 2026-07-26 · branch `gglee` · 관련 BIOP02-100 / BIOP01-64~70
- **이 폴더는 교체 후보다.** 라이브 하네스(`../docs/HARNESS.md`, `../CLAUDE.md`, `../.claude/*`, orchestrator SKILL)는 **수정하지 않았다.** 팀 검토·승인 후 아래 "스왑 방법"으로 교체한다.
- 목적: 언제든 교체 가능하도록 개선안을 실제 파일로 만들어 두고(git 보관), 상황에 따라 스왑.

## 무엇이 들어있나
| 파일 | 역할 | 스왑 대상(승인 시) |
| --- | --- | --- |
| `harness.yaml` | **SSOT manifest** — roles/gates/artifacts 기계판독 | 리포 루트에 신규 추가 |
| `scripts/harness_doctor.py` | **정합성 게이트** — manifest↔실제/문서 대조, 팬텀·경로 drift 검출 | 리포 루트 `scripts/`에 추가, PR CI 연결 |
| `docs/HARNESS.md` | 개선된 랩 지도(after) | `../docs/HARNESS.md` 교체 |
| `CLAUDE-routing.after.md` | 개선된 라우팅·산출물 계약 섹션(after) | `../CLAUDE.md`의 해당 섹션 교체 |

## 무엇이 바뀌었나 (before → after)
- 멤버 수 서술 → **구성요소 인벤토리 표**(논리역할/구현형태/경로/상태). `reviewer` 미구현 명시.
- 실행 환경 전제 **명문화**(repo 루트, 범용 폴백 금지) — 침묵 폴백 차단.
- 게이트 **3분류**(자동 무결성 / 과학적 판단 / 공개·거버넌스) + "사람 통과"는 후자에만.
- 검증 게이트 **이중화**(분석 직후 결과검증 + 공개 직전 패키지검증) & 외부리뷰보다 앞.
- `reviewer` → **`venue-reviewer`**(프로젝트 로컬 우선, 격리 규칙) — 전역 실체화 안 함.
- core/project profile/run instance **3계층** 관점 도입.
- 근거 없는 정량·수사("80%" 등) 제거.

## 스왑 방법 (승인 후에만)
```
# 리포 루트에서
cp harness_after/harness.yaml            ./harness.yaml
cp harness_after/scripts/harness_doctor.py ./scripts/harness_doctor.py
cp harness_after/docs/HARNESS.md         ./docs/HARNESS.md
# CLAUDE.md의 "Agent routing & artifact contract" 섹션을 CLAUDE-routing.after.md 내용으로 교체
# venue-reviewer / planner·runner 개명 등 에이전트 변경은 각 티켓(BIOP01-64/70)에서 별도 반영
python scripts/harness_doctor.py --repo . --manifest harness.yaml   # 통과 확인
```
되돌리려면 git revert 한 번. 라이브를 건드리지 않으므로 이 폴더 존재만으로는 하네스 동작에 영향 없음.

## 상태
검토 대기(BIOP02-100 → 검토 중). 반영은 이건규 노트 v2(`~/HARNESS_REVIEW_AND_PROPOSAL_2026-07-26.md`) 재검토 및 팀 승인 후.
