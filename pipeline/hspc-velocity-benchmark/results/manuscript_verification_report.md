# 원고 검증 리포트 — AKM WEEK 03 (verify_manuscript.py)

> 자동 PASS를 신뢰하지 않는다. HOLD는 사람이 correction gate(구체 충돌 시만·cap 2회) 아래 판정한다.
> 이 러너는 검증·보고만 하고 원고를 고치지 않는다. 규율=`manuscript/VERIFICATION_PROTOCOL.md`.

## Baseline 동결 (provenance)

- `manuscript/draft_v2.md` sha256[:16] = `94a9f03d95c8058f`
- `manuscript/draft_v2_ko.md` sha256[:16] = `5f94d633317277fa`
- git HEAD = `9d1c615` | 위험 Tier = **3 (투고·공개)** | correction cap = 2

## Per-check verdict (tool evidence 층, 사다리 Lv3~4)

| 검사 | verdict | rc | 근거 |
|---|---|---|---|
| 숫자 드리프트 EN (check_manuscript_numbers) | **HOLD** | 1 | 플래그 있음 → 사람 판정 |
| 숫자 드리프트 KO (check_manuscript_numbers) | **HOLD** | 1 | 플래그 있음 → 사람 판정 |
| 수정 보존 EN (check_revision_preserved) | **PASS** | 0 | 이상 없음 |
| 수정 보존 KO (check_revision_preserved) | **PASS** | 0 | 이상 없음 |
| 본문→목록 인용결함 (p13_check_uncited_sources) | **PASS** | 0 | 이상 없음 |
| 재계산 게이트 p3_concordance.py | **SKIP** | None | --with-recompute 미지정(scv-preprocess+data 필요) |
| 재계산 게이트 p3_crossdataset_concordance.py | **SKIP** | None | --with-recompute 미지정(scv-preprocess+data 필요) |
| 재계산 게이트 p3_scrambled_null.py | **SKIP** | None | --with-recompute 미지정(scv-preprocess+data 필요) |

## 종합: **HOLD**  (PASS 3 · HOLD 2 · FAIL 0 · SKIP 3)

### HOLD/FAIL 카드 (4필드: 부족증거 · 다음확인 1개 · 책임경계 · 재개조건)

- **숫자 드리프트 EN (check_manuscript_numbers)** [HOLD]
  - 부족 증거: 플래그 있음 → 사람 판정
  - 다음 확인 1개: 아래 출력 검토 → 진짜 결함인지 정당 오탐(반올림·CI경계·파생값)인지 사람 판정
    > 
    > ⚠️ 근거 문서에 없는 원고 수치 1건 — 리뷰 필요(오타/구버전/드리프트/미반영 결과 가능):
    > 
    >   L67   9.4       | Across methods, the per-gene lag did not concord. In HSPC, pairwise Spearman correlations of the lag
    > 
    > (주의: CI 경계·파생값 등 정당한 미검출도 있을 수 있음 — 사람이 판정. 자동 PASS 신뢰 금지.)
  - 책임 경계: 원고 owner(kkkim). 수정은 owner가, cap 2회 안에서.
  - 재개 조건: 결함이면 최소 수정 후 이 러너 재실행 diff 0; 오탐이면 PASS_WITH_NOTE로 기록.
- **숫자 드리프트 KO (check_manuscript_numbers)** [HOLD]
  - 부족 증거: 플래그 있음 → 사람 판정
  - 다음 확인 1개: 아래 출력 검토 → 진짜 결함인지 정당 오탐(반올림·CI경계·파생값)인지 사람 판정
    > 
    > ⚠️ 근거 문서에 없는 원고 수치 1건 — 리뷰 필요(오타/구버전/드리프트/미반영 결과 가능):
    > 
    >   L50   9.4       | 방법 간에 유전자별 시간차(lag)는 일치하지 않았다. HSPC에서 원래의 부호 포함 정의로 계산한 시간차의 쌍별 Spearman 상관은 −0.04(MultiVelo 대 MoFlo
    > 
    > (주의: CI 경계·파생값 등 정당한 미검출도 있을 수 있음 — 사람이 판정. 자동 PASS 신뢰 금지.)
  - 책임 경계: 원고 owner(kkkim). 수정은 owner가, cap 2회 안에서.
  - 재개 조건: 결함이면 최소 수정 후 이 러너 재실행 diff 0; 오탐이면 PASS_WITH_NOTE로 기록.

## SKIP 목록 (별도 실행 필요)
- 재계산 게이트 p3_concordance.py: --with-recompute 미지정(scv-preprocess+data 필요)
- 재계산 게이트 p3_crossdataset_concordance.py: --with-recompute 미지정(scv-preprocess+data 필요)
- 재계산 게이트 p3_scrambled_null.py: --with-recompute 미지정(scv-preprocess+data 필요)
