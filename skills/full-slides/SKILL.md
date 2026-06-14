---
name: full-slides
description: Create static journal-meeting slide decks from existing topic-organized paper analyses. Use only when the user explicitly asks to make slides, a slide deck, or a presentation from an analyzed paper. Requires an existing analysis/<primary-topic>/<paper-id>/<paper-id>_core.md, uses design.md as the required visual design reference, follows the installed openclaw-slides skill for browser presentation structure, and should include captured figure images from the source PDF when explaining figures.
---

# Full Slides

## 목표
이미 생성된 `analysis/<primary-topic>/<paper-id>/<paper-id>_core.md`를 기준으로 journal meeting용 static slide deck을 만든다. 이 스킬은 자료 분석 과정에서 매번 자동 실행하지 않는다. 사용자가 "슬라이드 만들어줘", "발표자료 만들어줘", "presentation 만들어줘"처럼 명시적으로 요청했을 때만 사용한다.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. PDF Figure 캡처 등은 반드시 `sources/` 안의 파일만 사용한다.
- slide 본문은 `<paper-id>_core.md`와 `lens-*.md` 내용에 근거한다. <paper-id>_core.md에 없는 새 주장을 slide에 만들지 않는다.

## 필수 전제
- `analysis/<primary-topic>/<paper-id>/<paper-id>_core.md`가 먼저 존재해야 한다.
- `<paper-id>_core.md`가 없으면 slide를 만들지 말고 먼저 full paper analysis가 필요하다고 말한다.
- source PDF가 `papers/` 또는 `<paper-id>_core.md`의 Source PDF 경로에 있어야 Figure 이미지를 캡처할 수 있다.
- 디자인은 반드시 프로젝트 루트의 `design.md`를 기준으로 한다.
- slide deck authoring은 설치된 `openclaw-slides` skill을 따른다.
- 기본 목표는 video나 preview server가 아니라, `index.html`을 파일로 직접 열어도 볼 수 있는 zero-dependency single HTML slide deck이다.

## 언어 규칙
- 기본 slide text는 한국어로 작성한다.
- `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `baseline`, `dataset`, `benchmark`, `Figure`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- slide 한 장에 너무 많은 문장을 넣지는 않되, `<paper-id>_core.md`에 정리된 배경, 비교, 수치, limitation을 충분히 반영한다.
- slide 제목은 가능한 한 명사형 어미를 사용한다. 예: `... 확장`, `... 비교`, `... 정량화`, `... 한계`, `... 해석`.
- 제목에서 `...한다`, `...된다`, `...본다`, `...보여준다`처럼 했다체 문장형 어미를 피한다.

## 서술 톤 (AGENTS.md "서술 톤 / 레지스터" 준수)
- 전체 톤 규칙은 `AGENTS.md`의 *서술 톤 / 레지스터* 를 따른다. slide·speaker-notes 모두 "AI가 쓴 티"를 피한다.
- slide 본문도 개조식(명사형 종결)을 기본으로 하고, 모든 줄을 같은 길이의 `~이다 / ~한다` 명제체로 끝내 단조로운 리듬을 만들지 않는다.
- 과장·상투 은유("폭발 / 게임 체인저 / 태피스트리"), "X가 아니라 Y" 반전, 3연속 병렬, 전환어구("또한 / 게다가") 남발을 피한다.
- em 대시(—)·앞머리 화살표(→)를 한 슬라이드에 몇 개씩 쓰지 않는다(단계·플로우의 →는 예외). 강조는 굵게 남발이 아니라 수치·근거로 한다.
- `<br>` 줄바꿈은 어구 중간에서 끊지 말고 의미 단위(구·절 경계)에서만 쓴다. 좁은 박스(stat label 등)는 줄바꿈에 기대지 말고 텍스트를 짧게 다듬는다.

## OpenClaw Slides 사용 규칙
- 먼저 `~/.openclaw/workspace/skills/openclaw-slides/SKILL.md`가 있는지 확인한다.
- OpenClaw Slides가 없으면 slide를 만들기 전에 `openclaw skills install openclaw-slides`로 다운로드해야 한다고 말하고, 가능하면 해당 명령을 실행해 설치한다.
- 설치 후에는 `~/.openclaw/workspace/skills/openclaw-slides/SKILL.md`를 필요한 만큼 읽고 그 구조를 따른다.
- OpenClaw Slides의 Mode A(New Presentation)로 간주한다. 기존 `.ppt/.pptx` conversion workflow는 사용자가 명시적으로 요청할 때만 적용한다.
- output은 zero-dependency single HTML presentation을 기본으로 한다.
- `index.html`은 server 없이 `file://.../index.html`로 열어도 slide navigation이 가능해야 한다.
- keyboard navigation, touch/swipe, mouse wheel navigation, progress bar, navigation dots를 포함한다.
- `section.slide` 기반 semantic HTML과 viewport-fitting CSS를 사용한다.
- 모든 slide는 viewport 안에 정확히 들어가야 하며 slide 내부 scrolling을 만들지 않는다.
- 사용자가 명시적으로 video export를 요청하지 않는 한 video render는 하지 않는다.

## 입력
- 특정 topic과 논문이 지정되면 해당 `analysis/<primary-topic>/<paper-id>/<paper-id>_core.md`를 사용한다.
- 자료만 지정되고 topic이 지정되지 않으면 `analysis/**/<paper-id>/<paper-id>_core.md`를 검색해 가장 일치하는 파일을 사용한다.
- topic만 지정되고 그 아래 paper folder가 하나뿐이면 그 `<paper-id>_core.md`를 사용한다.
- 여러 후보가 있으면 어떤 topic / 논문으로 slide를 만들지 사용자에게 물어본다.

## 출력 위치
- slide project는 `analysis/<primary-topic>/<paper-id>/slides/`에 만든다.
- 기본 파일:
  - `index.html`: OpenClaw Slides style의 self-contained browser presentation
  - `speaker-notes.md`: 발표자용 말하기 노트
  - `assets/figures/`: PDF에서 캡처한 Figure 이미지

## Slide 구성 원칙
- `<paper-id>_core.md`를 그대로 옮기지 말고 journal meeting에서 설명 가능한 주제별 slide로 나눈다.
- 슬라이드 수는 제한하지 않는다. 내용을 충분히 설명하기 위해 필요하면 Figure별, panel별로 여러 장을 만든다.
- 단순 요약 slide보다 `<paper-id>_core.md`의 설명 구조를 충실히 보이도록 한다.
  - 배경: 기존 방법 A/B/C가 무엇을 했고 무엇을 못했는지
  - 방법: 입력, ODE 관점, latent time/state output
  - Figure: 왜 필요한 Figure인지, 뒷받침하는 주장, 본문 비교
  - Results: dataset, baseline, metric, 실제 수치
  - Discussion: limitation과 다음 논문 아이디어
- 기본 slide 흐름:
  1. Title / paper identity
  2. Problem and background story
  3. Core concept
  4. Method overview
  5. Figure 1 / model intuition with captured figure image
  6. Main result figures, one claim per slide
  7. Dataset-by-dataset results with captured figure images
  8. Results summary with numbers
  9. Limitations
  10. Next-paper ideas / final takeaways
- 논문이 복잡하면 Figure별 slide를 적극적으로 늘린다.
- 각 slide는 “주장 1개 + 근거 1-3개 + 필요한 숫자”로 제한한다.
- 수치, dataset, baseline, metric은 `<paper-id>_core.md`에 있는 내용만 사용한다.

## Figure 이미지 사용 규칙
- Figure 설명 slide에는 가능한 한 PDF에서 해당 Figure 이미지를 캡처해 넣는다.
- Figure 이미지는 source PDF에서 직접 캡처하고 `analysis/<primary-topic>/<paper-id>/slides/assets/figures/`에 저장한다.
- 파일명은 `figure-1.png`, `figure-2a-d.png`, `figure-2e-i.png`처럼 Figure 번호와 범위를 알 수 있게 만든다.
- 한 slide에서 Figure 이미지가 차지하는 면적은 최대 slide 면적의 절반으로 제한한다.
- Figure 전체를 절반 크기 안에 넣었을 때 panel label이나 축/legend가 읽히지 않으면 Figure를 여러 slide로 나눈다.
- Figure가 여러 panel(a, b, c, d...)로 구성되어 있으면 다음 기준으로 분할한다.
  - overview panel과 result panel을 분리한다.
  - baseline comparison panel과 model interpretation panel을 분리한다.
  - dataset result가 다른 panel은 별도 slide로 분리한다.
- 이미지 옆에는 반드시 짧은 해석을 둔다.
  - 이 Figure가 필요한 이유
  - 이 Figure가 뒷받침하는 주장
  - 본문에서 강조한 비교
- 이미지가 없는 Figure 설명 slide는 예외 상황이다. PDF 캡처가 실패했을 때만 사용하고, 실패 이유를 notes에 적는다.

## PDF Figure 캡처 절차
- 먼저 source PDF 경로를 확인한다. `<paper-id>_core.md`에 `Source PDF`가 있으면 그 경로를 우선한다.
- PDF에서 Figure가 있는 page를 찾는다.
- 가능한 도구를 사용해 page 또는 Figure region을 PNG로 캡처한다.
  - `pdftoppm`, `mutool`, `magick`, `python` PDF/image library, macOS preview/screenshot 등 사용 가능한 도구 중 정확한 방법을 선택한다.
- Figure region crop이 어렵다면 page 전체를 먼저 캡처한 뒤 Figure 중심으로 crop한다.
- crop 후 slide에서 읽히는지 snapshot 또는 preview로 확인한다.
- 캡처 이미지는 논문 설명 목적의 부분 인용으로만 사용하고, 원문 Figure 전체를 불필요하게 크게 재배포하지 않는다.

## Design 적용
- `design.md`를 먼저 읽고 색상, typography, radius, spacing, depth 원칙을 따른다.
- 기본 방향:
  - warm cream background
  - charcoal text
  - border 중심의 shallow depth
  - 과한 shadow와 saturated accent color 금지
  - 큰 제목은 editorial하게, 본문은 짧고 읽기 쉽게
- slide deck은 논문 발표용이므로 landing page처럼 만들지 않는다.
- 카드 안에 카드를 중첩하지 않는다.
- Figure나 dataset slide는 숫자와 비교가 빠르게 보이도록 구성한다.
- Figure 이미지는 border `#eceae4`, radius 12px 안에 배치하고, 텍스트보다 시각 자료가 과도하게 커지지 않게 한다.

## 작업 절차
1. `analysis/<primary-topic>/<paper-id>/<paper-id>_core.md` 존재 여부를 확인한다.
2. `design.md`를 읽는다.
3. `openclaw-slides` skill 설치 여부를 확인한다. 없으면 `openclaw skills install openclaw-slides`로 설치한 뒤 필요한 규칙을 확인한다.
4. source PDF에서 Figure page와 Figure region을 확인한다.
5. 필요한 Figure 이미지를 캡처해 `slides/assets/figures/`에 저장한다.
6. `<paper-id>_core.md`에서 slide topics를 뽑는다.
7. 각 topic을 slide로 매핑하되 Figure 설명은 필요하면 여러 slide로 나눈다.
8. `analysis/<primary-topic>/<paper-id>/slides/`에 OpenClaw Slides 방식의 static HTML deck을 만든다.
9. `index.html`에 slide composition, CSS, navigation JS를 구현한다.
10. `index.html`은 local file open fallback을 포함한다. 서버 없이 `file://.../index.html`로 열어도 slide navigation이 가능해야 한다.
11. `speaker-notes.md`를 작성한다.
12. 가능한 정적 검증을 수행한다. 최소한 HTML asset path, duplicate IDs, basic syntax를 확인한다.
13. 가능하면 snapshot으로 Figure 이미지 크기와 텍스트 overflow를 확인한다. 서버 preview는 기본적으로 실행하지 않는다.
14. 사용자가 명시적으로 video export를 요청하지 않는 한 MP4 render는 하지 않는다.

## 품질 체크
- 모든 slide가 `<paper-id>_core.md` 근거를 갖는가?
- 한 slide에 주장이 하나만 있는가?
- 숫자, dataset, baseline이 틀리지 않았는가?
- PDF에서 캡처한 Figure 이미지가 들어갔는가?
- Figure 이미지가 slide 면적의 절반을 넘지 않는가?
- 큰 Figure는 여러 slide로 분할됐는가?
- `design.md`의 warm neutral design을 따르는가?
- 깨진 asset/path가 없는가?
- `index.html`을 직접 열었을 때 slide가 보이는가?

## 금지 사항
- `<paper-id>_core.md`가 없는 상태에서 slide 내용을 만들어내지 않는다.
- PDF 원문이나 외부 지식을 근거로 slide 내용을 확장하지 않는다. 필요한 경우 먼저 `<paper-id>_core.md`를 업데이트한다.
- design.md와 다른 임의의 화려한 색상/효과를 넣지 않는다.
- 사용자가 요청하지 않았는데 자동으로 slide를 만들지 않는다.
- 사용자가 video를 요청하지 않았는데 MP4 render를 만들지 않는다.
- 사용자가 server preview를 요청하지 않았는데 preview server를 실행하지 않는다.
- Figure 이미지를 너무 크게 넣어 설명 텍스트를 밀어내지 않는다.
