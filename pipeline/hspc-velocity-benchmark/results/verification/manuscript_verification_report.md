# 원고 검증 리포트 — AKM WEEK 03 (verify_manuscript.py)

> 자동 PASS를 신뢰하지 않는다. HOLD는 사람이 correction gate(구체 충돌 시만·cap 2회) 아래 판정한다.
> 이 러너는 검증·보고만 하고 원고를 고치지 않는다. 규율=`manuscript/VERIFICATION_PROTOCOL.md`.

## Baseline 동결 (provenance)

- `manuscript/draft_v2.md` sha256[:16] = `5a2d6e2179e00af6`
- `manuscript/draft_v2_ko.md` sha256[:16] = `8f60b7e18c64c6f6`
- git HEAD = `27ff58f` | 위험 Tier = **3 (투고·공개)** | correction cap = 2

## Per-check verdict (tool evidence 층, 사다리 Lv3~4)

| 검사 | verdict | rc | 근거 |
|---|---|---|---|
| 숫자 드리프트 EN (check_manuscript_numbers) | **PASS** | 0 | 이상 없음 |
| 숫자 드리프트 KO (check_manuscript_numbers) | **PASS** | 0 | 이상 없음 |
| 수정 보존 EN (check_revision_preserved) | **PASS** | 0 | 이상 없음 |
| 수정 보존 KO (check_revision_preserved) | **PASS** | 0 | 이상 없음 |
| 본문→목록 인용결함 (p13_check_uncited_sources) | **PASS** | 0 | 이상 없음 |
| 정본 수치 파리티 (check_canonical_parity) | **PASS** | 0 | 이상 없음 |
| 재계산 게이트 p3_concordance.py | **SKIP** | None | --with-recompute 미지정(scv-preprocess+data 필요) |
| 재계산 게이트 p3_crossdataset_concordance.py | **SKIP** | None | --with-recompute 미지정(scv-preprocess+data 필요) |
| 재계산 게이트 p3_scrambled_null.py | **SKIP** | None | --with-recompute 미지정(scv-preprocess+data 필요) |

## 종합: **PASS**  (PASS 6 · PASS_WITH_NOTE 0 · HOLD 0 · FAIL 0 · SKIP 3)

HOLD/FAIL 없음 — 전 결정적 검사 통과. 단 최종 verdict는 사람(Lv8)이 확정한다.

## SKIP 목록 (별도 실행 필요)
- 재계산 게이트 p3_concordance.py: --with-recompute 미지정(scv-preprocess+data 필요)
- 재계산 게이트 p3_crossdataset_concordance.py: --with-recompute 미지정(scv-preprocess+data 필요)
- 재계산 게이트 p3_scrambled_null.py: --with-recompute 미지정(scv-preprocess+data 필요)
