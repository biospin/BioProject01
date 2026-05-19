---
name: core-to-html
description: Render core.md (and optionally lens-*.md, methodology-brief.md) into a standalone HTML report with Figure/Table images embedded inline. Supports page-level PDF crop (fast, automatic) and panel-level crop (precise, requires bbox spec). Used after core.md is written to produce a browser-viewable journal-meeting handout.
---

# Core to HTML

## 목표

분석 노트(`core.md` 등 markdown)를 *Figure·Table 이미지가 임베드된 HTML report*로 변환한다. 본인이 *브라우저로 더블클릭만으로 열기*, *팀과 공유*, *PDF로 export* 등에 활용.

핵심 산출물:
1. `analysis/<primary-topic>/<paper-id>/figures/` — PDF에서 추출한 Figure/Table PNG.
2. `analysis/<primary-topic>/<paper-id>/core.html` — standalone HTML (CSS inline, image relative path).
3. (선택) `core-with-figures.md` — markdown image 임베드 버전. VS Code preview에서도 보임.

## Source grounding

- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
- 본 skill은 *새로운 분석*을 만들지 않는다. *기존 분석을 시각화*만.
- 원문 PDF (`sources/<paper-id>.pdf`)에서 image를 *추출*한다. 외부 image 사용 금지.

## 언어 규칙

- HTML report의 *본문 내용*은 markdown 그대로 변환 (한국어).
- HTML metadata (title, meta tag)는 본인 검색 편의 위해 영어·한국어 혼용 OK.

---

## Part 1. 두 가지 추출 모드

### 1.1 Page-level mode (default)

- PDF의 *Figure가 있는 페이지를 통째로 PNG로 추출*.
- 장점: 빠름. caption까지 같이 들어가서 self-contained.
- 단점: 페이지 단위라 *한 페이지에 여러 Figure*면 분리 안 됨.

### 1.2 Panel-level mode (정밀)

- 각 Figure의 *panel별 bbox spec JSON*을 입력 받아 정확히 crop.
- `skills/core-figure/scripts/extract_panels.py` 활용.
- 장점: 정확. *한 페이지에 여러 Figure*나 *한 Figure 안 panel 분리*도 가능.
- 단점: bbox spec 작성 부담. 사용자가 PDF 보고 좌표 결정해야 함.

### 1.3 Hybrid 사용

- 기본은 page-level로 자동 추출.
- 정밀이 필요한 Figure만 *spec JSON*으로 panel-level 추가.
- spec 파일 위치: `analysis/<primary-topic>/<paper-id>/figures/panels.json` (선택, 있으면 사용).

---

## Part 2. 페이지·Figure 매핑

PDF의 어느 페이지에 어느 Figure가 있는지 자동 탐지.

### 2.1 자동 탐지 휴리스틱

1. PDF의 모든 페이지를 text + image 비율로 분석.
2. 다음 패턴이 보이는 페이지를 *Figure 페이지 후보*로:
   - "Fig. N" 또는 "Figure N" 캡션이 페이지 상단·하단에 위치.
   - text 면적이 *전체 면적의 30% 이하*.
   - embedded image area가 *전체 면적의 50% 이상*.
3. Caption text의 *Figure 번호*로 매핑 (예: page 33 → Fig 1).

### 2.2 사용자 확인 / Override

자동 매핑이 틀릴 수 있다. `build_html.py`는 매핑 결과를 *먼저 출력*하고 사용자가 확인. 잘못된 경우:
- `--figure-map <Fig1=33,Fig2=34,...>` 옵션으로 수동 지정.
- 또는 `analysis/<primary-topic>/<paper-id>/figures/figure-map.json`에 저장.

---

## Part 3. 출력 파일 구조

```
analysis/<primary-topic>/<paper-id>/
├── core.md                          # 원본 분석 노트 (변경 없음)
├── core-with-figures.md             # image 임베드 markdown (자동 생성)
├── core.html                        # standalone HTML report (자동 생성)
└── figures/
    ├── figure-1.png                 # Fig 1 (page-level 또는 panel composite)
    ├── figure-2.png
    ├── ...
    ├── extended-data-fig-1.png      # Extended Data Fig 1
    ├── ...
    ├── figure-map.json              # 페이지 매핑 (수정 가능)
    └── panels.json                  # (선택) panel-level bbox spec
```

---

## Part 4. build_html.py

`skills/core-to-html/scripts/build_html.py`가 메인 entry.

### 4.1 사용법

```bash
# Default: page-level, 자동 매핑
python3 build_html.py analysis/<primary-topic>/<paper-id>

# 특정 Figure 매핑 수동 지정
python3 build_html.py analysis/<topic>/<paper-id> --figure-map "Fig1=33,Fig2=34"

# Panel-level 정밀 추출 (figures/panels.json 필요)
python3 build_html.py analysis/<topic>/<paper-id> --use-panels

# 추출만 (HTML 안 만듦)
python3 build_html.py analysis/<topic>/<paper-id> --extract-only

# 변환만 (이미지 추출 skip, 이미 figures/ 있다고 가정)
python3 build_html.py analysis/<topic>/<paper-id> --render-only

# 다른 markdown 파일도 포함
python3 build_html.py analysis/<topic>/<paper-id> --include "lens-academic,lens-industry,methodology-brief"
```

### 4.2 옵션

- `--figure-map <spec>`: Figure 번호 ↔ PDF 페이지 매핑 override.
- `--use-panels`: `figures/panels.json` 사용 (panel-level).
- `--extract-only` / `--render-only`: 단계 분리 실행.
- `--include <skills>`: core.md 외 추가 markdown 파일도 HTML에 포함 (쉼표 구분).
- `--dpi <n>`: PNG export DPI (default 150). 인쇄용은 300, 빠른 미리보기는 100.
- `--no-toc`: TOC 생성 안 함.

### 4.3 동작 단계

1. `paper-info.yaml`에서 `sources.paper.local` 경로 확인.
2. PDF 열고 page count, embedded image count.
3. (--use-panels가 아니면) 자동 매핑으로 Figure 페이지 식별.
4. Figure 페이지를 `figures/figure-N.png`로 export.
5. `core.md`를 복사하고 각 *Figure N* 섹션에 `![Figure N](figures/figure-N.png)` 추가 → `core-with-figures.md`.
6. markdown → HTML 변환 (Python `markdown` library, extensions: `extra`, `tables`, `toc`, `fenced_code`).
7. CSS 인라인 (reading-friendly, monospace 본문, 자료 인용 style).
8. `core.html` 저장.

---

## Part 5. CSS 디자인 원칙

HTML report는 *journal-meeting handout* 또는 *내부 R&D 노트*. 따라서 단순·읽기 좋게:

- **Width**: 본문 최대 880px (한 줄이 너무 길지 않게).
- **Font**: 본문은 시스템 sans-serif (한국어·영어 혼용). 코드/식은 monospace.
- **색**: charcoal text (#222) on warm-off-white (#fafaf7). `design.md`의 톤과 비슷.
- **Figure**: 가운데 정렬, 너비 100% (단 최대 800px), `1px solid #ddd` border + 12px radius.
- **Caption**: Figure 바로 아래 italic. caption text는 figure 옆에 자동으로 같이 들어감 (page-level mode에서 PNG 안에 포함).
- **Table**: zebra row + border, 가독성 우선.
- **Prefix 표시**: `해석:`, `외부 맥락:`, `추정:`, `미제공:`, `질문:`, `검토필요:`를 *색상으로 시각 구분* — 본인이 보고 즉시 인식.

### 5.1 Prefix 색상 (제안)

| Prefix | 색상 | 용도 |
|---|---|---|
| `해석:` | blue-gray | 분석자 해석 |
| `외부 맥락:` | warm gray | 외부 지식 |
| `추정:` | amber | 추측 |
| `미제공:` | red-gray | 본문에 없음 |
| `질문:` | green | 자기 follow-up |
| `검토필요:` | red | 본인 확인 필요 |

JavaScript 또는 CSS regex로 *분석 노트의 prefix line*을 자동 highlight.

---

## Part 6. 호출 시점

- **core.md 작성 직후** — page-level로 빠르게 HTML 미리보기.
- **lens-*.md, methodology-brief.md 추가된 후** — `--include`로 전체 통합 report.
- **공유 직전** — panel-level로 정밀 추출 후 최종 HTML.
- **반복 실행 OK** — figures/는 *덮어쓰기*, HTML도 덮어쓰기. 매번 최신 상태 유지.

---

## Part 7. 의존성

- `pymupdf` (PDF 페이지 PNG export)
- `markdown` (markdown → HTML 변환, `extra`, `tables`, `toc` extensions)
- `ruamel.yaml` (paper-info.yaml 읽기)

`skills/source-grounding/scripts/requirements.txt`에 추가 (또는 별도 requirements 분리).

---

## Part 8. Panel-level spec JSON 형식

`figures/panels.json`은 다음 schema:

```json
{
  "figures": [
    {
      "label": "Figure 1",
      "page": 33,
      "figure_bbox": [72, 120, 540, 720],
      "coords": "pdf",
      "panels": [
        { "label": "a", "bbox": [72, 120, 280, 320] },
        { "label": "b", "bbox": [280, 120, 540, 320] }
      ]
    }
  ]
}
```

자세한 bbox 좌표 결정은 `skills/core-figure/SKILL.md`의 Panel Image Extraction 섹션 참고.

---

## Part 9. 출력 체크리스트

- [ ] `core.html`이 standalone — 외부 link 의존 없음 (CSS 인라인, image 상대 경로).
- [ ] `figures/` 안의 PNG 파일이 *Figure N에 정확히 대응*.
- [ ] `core-with-figures.md`는 *원본 core.md*와 별개로 유지 (원본 보존).
- [ ] 모든 Prefix (`해석:` 등)가 HTML에서 *시각적으로 구분*.
- [ ] Table이 HTML `<table>`로 변환됨 (markdown extension `tables`).
- [ ] TOC (목차)가 자동 생성됨 (긴 분석 노트에 유용).
- [ ] HTML을 *브라우저로 더블클릭*만으로 열림.

---

## 주의할 점

- **page-level과 panel-level은 *덮어쓰기*.** 둘 다 같은 `figures/figure-N.png` 파일에 저장. 마지막 실행 모드가 남음.
- **figure-map.json은 *수정 후 보존*** — 다음 실행 시 자동 매핑 대신 이 파일을 우선 사용.
- **본 skill은 분석을 *읽기 좋게 표현*만 한다.** 분석 *내용*은 core-* / lens-* 가 만든다.
- **lens-industry.md의 *민감 정보*는 HTML에 그대로 노출됨.** 외부 공유 전 본인이 검토.
