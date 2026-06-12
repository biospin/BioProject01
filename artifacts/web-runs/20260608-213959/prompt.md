# Paper Analysis Request

BioProject01 논문 분석 하네스를 사용해 아래 자료를 분석해줘.

- Source: 10.1016/j.cell.2021.07.039
- Topic: single-cell-genomics
- Mode: full
- Lens: both

## Required workflow
1. AGENTS.md Quick Start와 Full Paper Workflow를 따른다.
2. source-grounding으로 `analysis/<topic>/<paper-id>/`와 `paper-info.yaml`을 만든다.
3. mode/lens 선택에 맞춰 core, lens, methodology-brief를 작성한다.
4. 마지막에 `skills/source-grounding/scripts/build_index.py`를 실행한다.
5. full/core 분석이면 `skills/core-to-html/scripts/build_html.py <paper-dir>`를 실행한다.

추측은 `해석:` / `추정:` / `검토필요:`로 분리하고, PDF 또는 supplementary에 없는 사실을 단정하지 않는다.
