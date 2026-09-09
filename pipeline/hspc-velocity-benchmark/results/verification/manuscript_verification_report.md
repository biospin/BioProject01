# 원고 검증 리포트 — AKM WEEK 03 (verify_manuscript.py)

> 자동 PASS를 신뢰하지 않는다. HOLD는 사람이 correction gate(구체 충돌 시만·cap 2회) 아래 판정한다.
> 이 러너는 검증·보고만 하고 원고를 고치지 않는다. 규율=`manuscript/VERIFICATION_PROTOCOL.md`.

## Baseline 동결 (provenance)

- `manuscript/draft_v2.md` sha256[:16] = `a351642682a3cae0`
- `manuscript/draft_v2_ko.md` sha256[:16] = `7fde2a93f27faea6`
- git HEAD = `d2039d9` | 위험 Tier = **3 (투고·공개)** | correction cap = 2

## Per-check verdict (tool evidence 층, 사다리 Lv3~4)

| 검사 | verdict | rc | 근거 |
|---|---|---|---|
| 숫자 드리프트 EN (check_manuscript_numbers) | **PASS** | 0 | 이상 없음 |
| 숫자 드리프트 KO (check_manuscript_numbers) | **PASS** | 0 | 이상 없음 |
| 수정 보존 EN (check_revision_preserved) | **PASS** | 0 | 이상 없음 |
| 수정 보존 KO (check_revision_preserved) | **PASS** | 0 | 이상 없음 |
| 본문→목록 인용결함 (p13_check_uncited_sources) | **PASS** | 0 | 이상 없음 |
| 정본 수치 파리티 (check_canonical_parity) | **PASS** | 0 | 이상 없음 |
| 재계산 게이트 p3_concordance.py | **HOLD** | 1 | rc=1 — 실행 실패, 확인 필요 |
| 재계산 게이트 p3_crossdataset_concordance.py | **HOLD** | 1 | rc=1 — 실행 실패, 확인 필요 |
| 재계산 게이트 p3_scrambled_null.py | **HOLD** | 1 | rc=1 — 실행 실패, 확인 필요 |

## 종합: **HOLD**  (PASS 6 · PASS_WITH_NOTE 0 · HOLD 3 · FAIL 0 · SKIP 0)

### HOLD/FAIL 카드 (4필드: 부족증거 · 다음확인 1개 · 책임경계 · 재개조건)

- **재계산 게이트 p3_concordance.py** [HOLD]
  - 부족 증거: rc=1 — 실행 실패, 확인 필요
  - 다음 확인 1개: 아래 출력 검토 → 진짜 결함인지 정당 오탐(반올림·CI경계·파생값)인지 사람 판정
    > EnvironmentLocationNotFound: Not a conda environment: /opt/anaconda3/envs/scv-preprocess
  - 책임 경계: 원고 owner(kkkim). 수정은 owner가, cap 2회 안에서.
  - 재개 조건: 결함이면 최소 수정 후 이 러너 재실행 diff 0; 오탐이면 PASS_WITH_NOTE로 기록.
- **재계산 게이트 p3_crossdataset_concordance.py** [HOLD]
  - 부족 증거: rc=1 — 실행 실패, 확인 필요
  - 다음 확인 1개: 아래 출력 검토 → 진짜 결함인지 정당 오탐(반올림·CI경계·파생값)인지 사람 판정
    > EnvironmentLocationNotFound: Not a conda environment: /opt/anaconda3/envs/scv-preprocess
  - 책임 경계: 원고 owner(kkkim). 수정은 owner가, cap 2회 안에서.
  - 재개 조건: 결함이면 최소 수정 후 이 러너 재실행 diff 0; 오탐이면 PASS_WITH_NOTE로 기록.
- **재계산 게이트 p3_scrambled_null.py** [HOLD]
  - 부족 증거: rc=1 — 실행 실패, 확인 필요
  - 다음 확인 1개: 아래 출력 검토 → 진짜 결함인지 정당 오탐(반올림·CI경계·파생값)인지 사람 판정
    > EnvironmentLocationNotFound: Not a conda environment: /opt/anaconda3/envs/scv-preprocess
  - 책임 경계: 원고 owner(kkkim). 수정은 owner가, cap 2회 안에서.
  - 재개 조건: 결함이면 최소 수정 후 이 러너 재실행 diff 0; 오탐이면 PASS_WITH_NOTE로 기록.

## SKIP 목록 (별도 실행 필요)
