# Paper Researcher Agent Router

이 프로젝트는 scientific paper를 분석하고 구조화된 노트를 `analysis/<topic>/` 아래에 저장한다. `AGENTS.md`는 라우터 역할만 담당한다. 자세한 작성 규칙은 `skills/` 아래의 local skill에 있다.

## 언어
- 기본 출력 언어는 한국어로 작성한다.
- 분야에서 자연스러운 표준 scientific term은 English로 유지한다. 예: `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `baseline`, `dataset`, `benchmark`.

## 출력 경로
- 입력 paper는 `papers/`에 둔다.
- paper analysis를 시작하기 전에 먼저 topic을 정한다.
  - 사용자가 topic을 명시하면 그대로 사용한다.
  - 사용자가 topic을 명시하지 않았지만 대화나 기존 묶음에서 명확히 추론 가능하면 그 topic을 사용한다.
  - topic을 안전하게 추론할 수 없으면 분석 전에 짧게 물어본다.
- 완료된 paper analysis는 각각 `analysis/<topic>/<paper-title>/`에 저장한다.
- 각 paper folder에는 반드시 다음 파일이 있어야 한다:
  - `full.md`
- topic folder name은 사용자가 준 주제를 kebab-case로 정규화한다. 예: `epigenomic lag` → `epigenomic-lag`.
- paper title을 folder name으로 사용한다. title을 신뢰도 있게 추출할 수 없으면 PDF filename을 사용하고, output file에 그 불확실성을 명시한다.

## Skill Routing
paper analysis에는 다음 local skill을 사용한다:

| Task | Skill |
| --- | --- |
| `full.md` Background | `skills/full-background/SKILL.md` |
| `full.md` Overview | `skills/full-overview/SKILL.md` |
| `full.md` Methods - computational methods 중심 실험논문에서만 선택적으로 사용 | `skills/full-methods/SKILL.md` |
| `full.md` Figure / Table Analysis | `skills/full-figure/SKILL.md` |
| `full.md` Results | `skills/full-results/SKILL.md` |
| `full.md` Limitations and Final Takeaways | `skills/full-discussion/SKILL.md` |
| Cell type annotation 전략 및 품질 평가 - annotation 방법이 결론에 영향을 주는 single-cell / multi-ome 논문에서 사용 | `skills/celltype-annotation/SKILL.md` |
| Multi-ome modality 통합 품질 평가 - scRNA-seq + scATAC-seq joint 분석 논문에서 통합 신뢰도가 downstream 분석에 영향을 줄 때 사용 | `skills/multiome-integration/SKILL.md` |
| 기존 `full.md` 기반의 명시적 static slide deck 요청 | `skills/full-slides/SKILL.md` |
| 분석된 paper에 대한 질문 | `skills/question/SKILL.md` |

## Full Paper Workflow
PDF를 분석할 때는 다음 순서를 따른다:

1. topic을 먼저 정하고 `analysis/<topic>/` folder를 준비한다.
2. title, authors, year, venue, field를 추출한다.
3. 아래 section별 skill routing을 통해 `full.md`를 작성한다:
   - Background: `skills/full-background/SKILL.md`
   - Overview: `skills/full-overview/SKILL.md`
   - Methods: `skills/full-methods/SKILL.md`
     - 단, 매번 작성하지 않는다.
     - 논문이 새로운 computational model, statistical model, inference algorithm, optimization objective, benchmark framework를 제안하거나 기존 method를 실험적으로 확장/비교하는 경우에만 사용한다.
     - Methods에서는 사용한 확률/통계학적 방법, 핵심 method insight, 이전 방법과 다른 점, 그 차이가 Results에서 어떤 효과로 나타났는지를 자세히 다룬다.
     - review paper처럼 여러 computational method를 소개만 하는 경우에는 `full-methods`를 호출하지 않고 `Figure / Table Analysis`와 `Results`에서 method taxonomy로 정리한다.
   - Figures / Tables: `skills/full-figure/SKILL.md`
   - Results: `skills/full-results/SKILL.md`
   - Limitations / Final Takeaways: `skills/full-discussion/SKILL.md`
4. `analysis/<topic>/<paper-title>/full.md`에 저장한다.

## Slide Workflow
사용자가 slides, slide deck, presentation 생성을 명시적으로 요청했을 때만 다음 순서를 따른다:

1. `skills/full-slides/SKILL.md`를 사용한다.
2. 먼저 `analysis/<topic>/<paper-title>/full.md`가 존재해야 한다.
3. `design.md`를 필수 visual design reference로 사용한다.
4. source PDF에서 관련 Figure image를 캡처해 Figure explanation slide에 포함한다.
5. 각 Figure image는 slide의 절반 이하 크기로 유지한다. 크거나 multi-panel인 Figure는 여러 slide로 나눈다.
6. `analysis/<topic>/<paper-title>/slides/` 아래에 OpenClaw Slides 기반의 browser-previewable journal-meeting slide deck을 만든다.
7. 사용자가 video export를 명시적으로 요청하지 않는 한 video는 render하지 않는다.
8. 일반 paper analysis 중에는 slides를 자동 생성하지 않는다.

## Question Workflow
사용자가 이미 분석된 paper에 대해 질문하면 다음 순서를 따른다:

1. `skills/question/SKILL.md`를 사용한다.
2. 먼저 `analysis/**/full.md`를 검색한다.
3. 관련 paper의 `full.md`에 답이 있으면 그 파일만 근거로 답한다.
4. 다른 분석된 paper에 답이 있으면 `According to <paper title>...` 형식으로 출처를 명시한다.
5. 어떤 분석된 `full.md`에도 답이 없으면, 분석된 파일에는 해당 정보가 없다고 말한다.
