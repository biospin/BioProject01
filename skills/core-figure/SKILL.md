---
name: core-figure
description: Analyze figures for the objective <paper-id>_core.md section, and when useful extract one image per figure panel using the bundled scripts. Use when explaining why each figure was included, inferring which claim the figure supports, describing each panel (a, b, c, d...) using captions and main text, or cropping panels from the source PDF.
---

# Core Figure

## 목표
각 Figure를 단순히 "무엇을 보여준다"로 끝내지 않고, 먼저 "논문 저자가 왜 이 Figure를 넣었는가"를 분석한다. Figure가 논문 주장의 어떤 부분을 증명하거나 설득하기 위해 배치되었는지 추론한 뒤, 각 panel(a, b, c, d...)을 본문에서 비교한 내용 중심으로 설명한다.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 출력은 `analysis/<primary-topic>/<paper-id>/<paper-id>_core.md`의 Figure 섹션에 누적된다.
- panel image 추출은 `analysis/<primary-topic>/<paper-id>/figures/`에 저장한다.

## 언어 규칙
- 기본 출력은 한국어로 작성한다.
- `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `baseline`, `dataset`, `benchmark`, `Figure`, `panel`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 유지할 때는 처음 한 번 한국어 설명을 덧붙인다.
- 불필요하게 문장 전체를 영어로 쓰지 않는다.

## 작업 절차
1. Figure 번호, 제목, caption 전체를 확인한다.
2. 본문에서 해당 Figure를 언급하는 문단을 찾는다.
3. Figure가 뒷받침하는 논문 주장을 먼저 추론한다.
   - 예: 논문 주장이 “B가 C를 발생시킨다”이고 Figure가 B 유무에 따른 C 변화를 보여준다면, 이 Figure의 목적은 “B가 C를 유도한다는 주장을 시각적으로 입증하기 위해서”라고 해석한다.
4. 각 panel(a, b, c...)이 무엇을 비교하는지 정리한다.
5. caption보다 본문에서 저자가 강조한 비교, 차이, 방향성, baseline 대비 변화를 우선한다.
6. Figure 해석의 주의점을 쓴다. 인과 주장인지, 상관 또는 시각적 근거인지 구분한다.

## Panel Image Extraction
Figure panel을 이미지로 분리해야 하거나 slide 제작에 재사용할 가능성이 있으면 `scripts/extract_panels.py`를 사용한다.

### 사용 시점
- 사용자가 panel image extraction, figure crop, panel별 이미지 저장을 요청한 경우.
- Figure가 multi-panel이고 `full.md` 설명만으로 panel 위치 확인이 어려운 경우.
- Slide deck에서 큰 multi-panel Figure를 여러 장으로 나눠야 하는 경우.

### 출력 위치
- 기본 저장 위치는 해당 paper 분석 폴더 아래 `figures/`이다.
- 예: `analysis/<primary-topic>/<paper-id>/figures/figure_2_panel_01_a.png`
- script는 전체 Figure crop, panel image들, debug overlay, manifest JSON을 함께 저장한다.

### Script 사용법
먼저 dependency가 없으면 설치한다:

```bash
python3 -m pip install pymupdf pillow
```

PDF page와 Figure bbox를 알고 있으면 자동 분할을 시도한다:

```bash
python3 skills/core-figure/scripts/extract_panels.py papers/paper.pdf \
  --page 5 \
  --figure "Figure 2" \
  --figure-bbox 72,120,540,650 \
  --coords pdf \
  --out "analysis/<primary-topic>/<paper-id>/figures"
```

- `--page`는 1-based page number이다.
- `--figure-bbox`는 기본적으로 PDF point 좌표(`--coords pdf`)이며 `x0,y0,x1,y1` 형식이다.
- `--coords pixels` 또는 `--coords normalized`도 사용할 수 있다.
- 자동 분할 결과가 틀리면 generated `*_debug.png`를 보고 manual spec으로 다시 실행한다.

복잡한 layout은 JSON spec을 만든 뒤 panel별 bbox를 명시한다:

```json
{
  "figure": "Figure 2",
  "page": 5,
  "figure_bbox": [72, 120, 540, 650],
  "coords": "pdf",
  "panels": [
    { "label": "a", "bbox": [72, 120, 300, 360] },
    { "label": "b", "bbox": [300, 120, 540, 360] },
    { "label": "c", "bbox": [72, 360, 300, 650] },
    { "label": "d", "bbox": [300, 360, 540, 650] }
  ]
}
```

```bash
python3 skills/core-figure/scripts/extract_panels.py papers/paper.pdf \
  --spec figure2-panels.json \
  --out "analysis/<primary-topic>/<paper-id>/figures"
```

### 품질 확인
- `*_debug.png`에서 red box가 panel 경계를 잘 잡았는지 확인한다.
- `*_manifest.json`의 `bbox_pdf_points_on_page`를 보존하면 나중에 같은 Figure를 재추출하기 쉽다.
- 자동 분할은 whitespace gutter 기반 heuristic이다. panel label이 작거나 panel 사이 여백이 없는 composite figure는 manual spec을 우선한다.

### 검증된 사용 패턴
- 먼저 auto mode로 실행해 `*_debug.png`를 확인한다.
- red box가 실제 panel a, b, c...와 1:1로 맞지 않으면 manual JSON spec을 만든다.
- manual spec의 `figure_bbox`와 `panels[].bbox`는 같은 좌표계로 작성한다. 기본은 PDF page 좌표(`coords: "pdf"`)이며 page 전체 기준이다.
- 실제 검증: `papers/MultiVelo.pdf` page 3의 Figure 1은 auto mode가 schematic 내부 여백 때문에 panel b와 상단 panel을 잘못 나눴다. manual spec으로 a-g 7개 panel을 정상 추출했다.

검증된 command 형태:

```bash
python3 skills/core-figure/scripts/extract_panels.py papers/MultiVelo.pdf \
  --spec "analysis/epigenomic-lag/Multi-omic single-cell velocity models epigenome-transcriptome interactions and improves cell fate prediction/figures/figure_1_panels.json" \
  --out "analysis/epigenomic-lag/Multi-omic single-cell velocity models epigenome-transcriptome interactions and improves cell fate prediction/figures"
```

성공 기준:
- `figure_1_manifest.json`의 `panels` 개수가 caption/main text의 panel 개수와 일치한다.
- `figure_1_debug.png`에서 각 red box가 panel label 하나와 대응한다.
- `figure_1_panel_01_a.png`처럼 panel별 PNG가 읽을 수 있는 해상도로 저장된다.

## 출력 형식
사용자가 다른 형식을 요청하지 않으면 Figure마다 아래 구조를 따른다.

```markdown
#### Figure N
- 이 Figure가 필요한 이유:
- 이 Figure가 뒷받침하는 주장:

##### 패널별 설명
- a:
- b:
- c:
- d:

##### 본문에서 강조한 비교
- 비교 대상:
- 관찰된 차이:
- 이 차이가 의미하는 것:

##### 해석 시 주의점
- 주의점:
```

## Figure 목적 추론 규칙
- Figure 목적은 caption 번역이 아니라 논문 전체 주장과 연결해서 쓴다.
- “왜 하필 이 실험/시각화가 필요한가?”를 먼저 답한다.
- Figure가 method overview인지, baseline 비교인지, ablation인지, case study인지, biological validation인지 구분한다.
- Figure가 특정 claim을 직접 증명하지 못하고 보조 근거만 제공하면 그 한계를 표시한다.
- Figure 1이 Overview에서 이미 다뤄졌다면 중복 설명을 줄이고, Figure 섹션에서는 논문 주장과의 연결만 압축한다.

## 패널별 설명 규칙
- panel label이 있으면 `a`, `b`, `c` 순서대로 정리한다.
- panel label이 텍스트 추출에서 불완전하면 caption과 본문 언급을 기준으로 가능한 범위만 정리한다.
- 각 panel 설명은 “무엇을 보여주는가”보다 “무엇과 무엇을 비교해 어떤 차이를 보이는가”를 우선한다.
- 축, 색상, 조건, cell type, dataset, baseline, metric이 해석에 중요하면 포함한다.
- 본문에 없는 과한 해석은 피하고, 필요한 경우 `추론:`으로 표시한다.

## 좋은 해석의 형태
```markdown
- 이 Figure가 필요한 이유: 논문의 핵심 주장은 B가 C를 유도한다는 것이다. 이 Figure는 B가 있는 조건과 없는 조건을 나란히 보여주어 C의 발생 여부가 B와 연결된다는 점을 설득하기 위해 배치되었다.
- 본문에서 강조한 비교: B 조건에서는 C signal이 증가하지만, baseline 조건에서는 같은 변화가 나타나지 않는다. 따라서 저자는 B가 C의 단순한 동반 현상이 아니라 C를 설명하는 핵심 변수라고 주장한다.
```

## 주의할 점
- Figure 설명을 caption 요약으로 끝내지 않는다.
- 본문에서 비교하지 않은 내용을 Figure만 보고 과하게 일반화하지 않는다.
- 수치, 조건, dataset 이름은 가능한 한 보존한다.
