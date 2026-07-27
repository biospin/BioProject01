---
name: slide-deck
description: Create a journal-meeting slide deck from an existing full.md analysis. Run only when the user explicitly requests slides or a presentation. Requires full.md to exist. Uses design.md for visual style and openclaw-slides for structure.
---

# Slide Deck

## 언제 실행하나
사용자가 "슬라이드", "발표자료", "presentation"을 명시적으로 요청했을 때만 실행한다. 논문 분석 과정에서 자동으로 실행하지 않는다.

## 전제 조건
- `analysis/<topic>/<paper-title>/full.md`가 먼저 존재해야 한다. 없으면 full.md를 먼저 만들어야 한다고 말한다.
- 프로젝트 루트의 `design.md`를 반드시 읽고 시각 디자인 기준으로 삼는다.
- `/Users/jamie/.openclaw/workspace/skills/openclaw-slides/SKILL.md` 설치 여부를 확인한다. 없으면 `openclaw skills install openclaw-slides`로 설치 후 진행한다.

## 입력
- `analysis/<topic>/<paper-title>/full.md`
- 논문 원본 PDF (Figure 이미지 캡처용)

## 실행 절차
1. `full.md` 존재 여부를 확인한다.
2. `design.md`를 읽는다.
3. openclaw-slides 설치 여부를 확인하고 필요하면 설치한다.
4. source PDF에서 각 Figure가 있는 page를 확인한다.
5. Figure 이미지를 캡처해 `slides/assets/figures/`에 저장한다.
6. `full.md`에서 slide topic을 뽑는다.
7. slide를 구성하고 `index.html`을 작성한다.
8. `speaker-notes.md`를 작성한다.

## Slide 구성 순서
1. Title — 논문 제목, 저자, venue, year
2. 논문이 다루는 문제 (fig1-decode 기반)
3. 핵심 접근법 + Figure 1 이미지
4. 데이터셋 및 실험 설계 (results-scan 기반)
5. 주요 결과 — Figure별, 데이터셋별로 나눔
6. Apply Map 요약 — 이 논문을 어떻게 쓸 수 있는가
7. 한계와 열린 질문 (takeaway 기반)

각 slide는 주장 1개 + 근거 1–3개로 제한한다. Figure 이미지가 있으면 반드시 포함한다.

## Figure 이미지 규칙
- slide 면적의 절반을 넘지 않도록 한다.
- panel label이나 축이 읽히지 않으면 Figure를 여러 slide로 나눈다.
- 이미지 옆에는 반드시 짧은 해석을 둔다 (이 Figure가 뒷받침하는 주장, 주요 비교).
- 파일명: `figure-1.png`, `figure-2a-c.png` 형태로 번호와 범위를 표시한다.

## PDF Figure 캡처
사용 가능한 도구 중 하나를 선택한다: `pdftoppm`, `mutool`, `magick`, Python pymupdf.

```bash
# 예시: mutool로 특정 page를 PNG로 변환
mutool draw -o figure-N.png -r 150 papers/paper.pdf [page번호]
```

crop이 어려우면 page 전체를 캡처한 뒤 Figure 영역만 crop한다.

## 출력
- `analysis/<topic>/<paper-title>/slides/index.html` — server 없이 파일로 직접 열어도 동작하는 single HTML
- `analysis/<topic>/<paper-title>/slides/speaker-notes.md`
- `analysis/<topic>/<paper-title>/slides/assets/figures/` — 캡처된 Figure 이미지

## Design 기준
`design.md`를 읽고 색상, typography, spacing을 따른다. 핵심 원칙:
- warm cream background, charcoal text
- border 중심, 과한 shadow 금지
- 카드 안에 카드를 중첩하지 않음
- Figure 이미지: border `#eceae4`, radius 12px

## 금지
- `full.md`가 없는 상태에서 slide 내용을 만들지 않는다.
- 사용자가 요청하지 않았는데 자동으로 생성하지 않는다.
- 사용자가 요청하지 않았는데 video를 render하지 않는다.
- preview server를 자동으로 실행하지 않는다.
