# BIOP01 연구 블로그 — 정본

HSPC velocity-lag 벤치마크 연구(크로마틴에서 전사로 가는 시간차와 전사 속도)를 비전공자도 읽을 수 있게 산문으로 정리한 글이다. 영문과 국문을 한 파일에 함께 둔다.

## 이 폴더가 정본이다 (2026-09-02 이전)

원래 정본은 협업 서버 `/workspace/blog/BIOP01/`이었고 이 저장소는 `blog/` 전체를 `.gitignore`로 제외했다. GPU 서버를 반납하면서 그 경로가 사라졌고, 정정본이 개인 백업 한 곳에만 남는 상태가 됐다. 그래서 이 저장소로 정본을 옮겼다. 경위는 JIRA BIOP01-83에 있다.

블로그는 이미 Confluence로 공개된 글이므로 저장소에 두어도 새로 노출되는 것이 없다. 오히려 이력과 검수 게이트가 함께 붙는다.

## 파일

| 파일 | 내용 |
|---|---|
| `01_lag-vs-alpha.md` | 크로마틴이 전사를 미리 준비시킬까 |
| `02_five-checks.md` | 재현되지 않는 결과를 스스로 검증하기 |
| `03_cross-dataset-replication.md` | 조직과 종을 바꿔 본 재현 |
| `04_reproducible-harness.md` | 분석을 하네스로 옮기기 |
| `05_novelty-positioning.md` | 선행연구와 논문의 자리매김 |
| `06_self-adversarial-hardening.md` | 우리 결과를 스스로 공격한 세 가지 분석 |
| `07_curvature-predicts-trust.md` | 헤드라인이 될 뻔한 발견을 스스로 되돌린 이야기 |
| `08_no-rule-for-direction.md` | 크로마틴 방향 규칙을 찾다가 세 번 실패한 이야기 |
| `00_all.md` | 위 여덟 편을 순서대로 결합한 합본. **파생물이므로 개별 편을 고친 뒤 다시 만든다** |
| `glossary.md` | 용어집 |

## 게시 경로

Confluence VC 스페이스가 공개본이다. 인덱스는 page 49545229이고 여덟 편이 그 자식 페이지로 붙어 있다.

정정이 생기면 본문 전체를 갈아 끼우지 않고 **상단에 정정 배너를 붙인다**. 서식 손상 위험이 적고 오독 위험은 즉시 닫힌다. 배너 원문은 `docs/confluence_banners/blog0N_banner.html`에 두고, 적용은 아래로 한다.

```
source ~/.atlassian_env
python3 scripts/confluence_prepend_banner.py <pageId> docs/confluence_banners/blog0N_banner.html \
    --marker "정정 안내 (YYYY-MM-DD 게시본 갱신)" --dry
```

마커 텍스트가 이미 본문에 있으면 중복 삽입을 거부한다. 날짜가 다른 배너를 새로 붙일 때는 `--marker`로 그 배너의 문구를 넘긴다.

## 규율

- **수치와 주장은 연구 결과 원본에서만 가져온다.** 정본은 `pipeline/hspc-velocity-benchmark/results/FINDINGS.md`와 `manuscript/draft_v2.md`이며, 블로그는 그 산문 판이다.
- **원고에서 철회하거나 강등한 주장은 블로그에도 반영한다.** 2026년 8월에 이 동기화가 한 번 누락돼 철회된 주장이 공개본에 남아 있었다(BIOP01-83). 원고를 고치면 블로그도 같은 세션에서 본다.
- **영문과 국문을 함께 고친다.** 한쪽만 고치면 같은 페이지 안에서 서술이 어긋난다. 실제로 8편에서 한국어 표의 두 행이 빠져 기전 설명이 영문과 반대로 적힌 적이 있다.
- `00_all.md`를 직접 고치지 않는다. 개별 편을 고치고 다시 만든다.

## 아직 남은 것

- `site/` 브라우저판이 서버와 함께 사라졌다. 필요하면 md에서 다시 만든다.
- 04편 본문이 개념도 위치를 `/workspace/skills/harness-concept/`로 가리키는데, 그 경로도 서버와 함께 없어졌다. 대체 위치를 정한 뒤 문구를 고쳐야 한다.
