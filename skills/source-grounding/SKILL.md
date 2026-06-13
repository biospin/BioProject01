---
name: source-grounding
description: Set up the per-document analysis folder, create paper-info.yaml, curate the source PDF/supplementary/non-paper materials in sources/, generate paper.bib, and define the hallucination-prevention rules that every other skill in this project inherits. Use at the beginning of every analysis.
---

# Source Grounding

## 역할

이 skill은 두 가지 일을 한다.

1. **모든 분석의 출발점**: document folder를 만들고, `paper-info.yaml`을 생성하고, 원문(PDF·웹페이지·리포트 등)과 supplementary, BibTeX를 `sources/` 아래에 정리한다.
2. **Hallucination 방지 원칙의 single source of truth**: 다른 skill (`core-*`, `lens-*`, `methodology-brief`, `abstract-analysis`, `question`)은 이 원칙을 *반복하지 않고* 단순히 "source grounding 원칙을 따른다"고 참조한다.

분석 대상은 paper만이 아니다. preprint, 학회 자료(proceeding·poster·talk), 기업 발행물(white paper·투자자료·기술 brief·press release), 정부·규제기관 리포트, 시장조사 리포트, 뉴스, 블로그, webinar 등 모두 지원한다. `document_type` 필드로 분기한다 (Part 7).

## 언어 규칙

- 기본 출력은 한국어로 작성한다.
- `DOI`, `BibTeX`, `accession`, `supplementary`, `paywall`, `preprint`, `white paper` 같은 분야 표준 영어 용어는 그대로 유지한다.

---

## Part 1. Hallucination 방지 원칙 (Master Definition)

이 섹션은 다른 skill에서 *링크로만 참조*하는 마스터 규칙이다. 다른 skill은 자신의 작성 규칙 안에서 이 원칙을 반복 기술하지 않는다.

### 1.1 차단해야 할 것

- 원문이나 supplementary에 없는 수치, 사실, 인용을 *원문의 내용처럼* 적는 것.
- "이 분야에서는 일반적으로..."로 시작하는 외부 통념을 *근거 없이 단정*하는 것.
- 검색·웹 정보·기억으로 알고 있는 다른 자료의 내용을 *현재 자료의 주장처럼* 적는 것.
- caption만 보고 본문이 강조하지 않은 비교·해석을 *저자 주장*으로 적는 것.

### 1.2 허용되는 것

- `sources/` 아래 파일에 명시적으로 나오는 수치, 문장, 그림, 표.
- 본문이 직접 인용한 선행자료를 *그 선행자료의 이름과 함께* 적는 것.
- 분석자(LLM)가 본문 근거 위에서 추론한 해석. 단 반드시 표시한다 (1.3 참고).

### 1.3 외부 맥락·해석·질문의 명시 분리 (Prefix 6종)

본문 밖의 지식, 분석자 추론, 또는 *분석자의 follow-up*을 적어야 할 때는 다음 prefix 중 하나를 반드시 붙인다.

| Prefix | 의미 | 예시 |
|---|---|---|
| `해석:` | 분석자가 본문 근거 위에서 추론한 해석 | `해석: 이 dataset 크기는 method paper 평균보다 크지만 batch effect 분리가 어렵다.` |
| `외부 맥락:` | 본문 밖의 분야 일반 지식. 출처가 있으면 함께 적는다. | `외부 맥락: organoid 12주차는 outer radial glia가 우세 (Pollen et al., 2019 — 본문은 인용하지 않음).` |
| `추정:` | 본문에 명시되지 않았으나 합리적으로 추측되는 값/관계. | `추정: chromatin opening rate prior는 MultiVelo default(0.5/hr)일 가능성이 높다.` |
| `미제공:` | 본문에 해당 정보가 없음을 적극적으로 표시. | `미제공: cell cycle phase별 lag estimate는 본문·supplementary에 없음.` |
| `질문:` | 분석자가 본인(사용자)에게 던지는 follow-up. 분석 노트를 다시 펴봤을 때 무엇을 더 알아봐야 할지 명시. | `질문: 이 알고리즘을 HSPC multiome에 그대로 돌리면 cell type imbalance가 lag estimate에 영향을 줄까? 별도 simulation 필요해 보임.` |
| `검토필요:` | 분석자가 *확신이 없거나* 본문 해석이 어려워 본인이 확인해야 할 곳. | `검토필요: Figure 4의 panel d에서 x축 단위가 pseudotime인지 wall-clock인지 본문에서 명확하지 않음. PDF 직접 확인 필요.` |

### 1.4 출처 표기 규칙

- 본문에서 인용할 때는 가능하면 *섹션 위치*를 함께 적는다 (예: `Methods §2.3`, `Figure 4d`, `Table S2`).
- supplementary 출처는 *파일명*도 함께 적는다 (예: `supp_2.pdf §S3`, `supp_tables.xlsx sheet "TableS5"`).
- 인용 부호("…")가 길어 부담스러우면 핵심 어구만 발췌한 뒤 `…`로 생략을 표시한다.
- non-paper 출처도 같은 원칙으로 표기 (예: `BCG 2024 cell therapy report §3.2`, `Gilead Q3 2024 earnings call transcript`).

### 1.5 다른 skill에서 이 원칙을 참조하는 방법

다른 skill의 작성 규칙 안에는 다음 한 줄만 둔다:

```markdown
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
```

이 한 줄로 1.1 ~ 1.4의 모든 규칙이 자동 적용된다.

---

## Part 2. paper-info.yaml — Single Source of Truth

document folder의 메타데이터는 모두 `paper-info.yaml`에 모은다. citation, 다운로드 링크, 카테고리(domain / use_case / importance), 공유 대상, 우선순위, 연관 자료가 한 곳에 있어야 분석 결과(`<paper-id>_core.md`, `lens-*.md`)에서 일관되게 참조 가능하다.

> 파일명 주의: 분석 대상이 paper가 아닌 경우에도 파일명은 `paper-info.yaml`로 유지한다 (이미 다른 skill·문서가 이 이름을 참조). 내용은 `document_type`에 따라 자유롭게 분기.

### 2.1 전체 schema (예시)

```yaml
# Wang et al., 2024 — MultiVelo — Nature Methods
# DOI: 10.1038/s41592-024-xxxxx
# Topics: epigenomic-lag (primary), single-cell-genomics  |  Importance: 상

# ─── end of header (auto-managed by build_index.py; do not edit this block manually) ───

# Identity
document_type: "paper"              # Part 7 카탈로그 참조
title: "Multi-omic single-cell velocity models epigenome-transcriptome interactions..."
authors:
  - "Wang, X."
  - "Lee, J."
  - "Hu, L."
year: 2024
venue: "Nature Methods"             # 또는 학회명, 기업명, 발행처
doi: "10.1038/s41592-024-xxxxx"
keywords:
  - "RNA velocity"
  - "multi-omics"
  - "chromatin accessibility"

# ───────────────────────────────────────────
# Topics (Option E 다중 분류)
# ───────────────────────────────────────────
topics:                             # 첫 번째가 primary topic (= 폴더 경로의 <primary-topic>)
  - "epigenomic-lag"                # primary
  - "single-cell-genomics"          # secondary
  - "chromatin"                     # secondary

# ───────────────────────────────────────────
# Version (preprint vs published 등 구분)
# ───────────────────────────────────────────
version:
  type: "published"                 # preprint / published / both
  peer_reviewed: true
  preprint:                         # 있으면 함께 기록
    server: "bioRxiv"
    doi: "10.1101/2023.xx.xx.xxxxxx"
    version: "v3"
    date: "2023-08-15"
  published:
    date: "2024-03-21"

# ───────────────────────────────────────────
# Citation
# ───────────────────────────────────────────
citation:
  key: "wang2024multivelo"          # BibTeX citation key — 분석 결과에서 @key로 참조
  short_id: "multivelo"             # 본인이 부르기 편한 짧은 ID
  bibtex_file: "sources/wang-2024-multivelo.bib"  # BibTeX entry 위치
  bibtex_type: "article"            # article / misc / techreport / incollection / online ...
  share_filename: "Wang 2024 - Multi-omic Relay Velocity (MultiVelo).pdf"  # 공유용 파일명 (선택)

# ───────────────────────────────────────────
# Source files (Part 2.4 명명 규칙 참고)
# ───────────────────────────────────────────
sources:
  paper:
    url: "https://www.nature.com/articles/s41592-024-xxxxx.pdf"
    local: "sources/wang-2024-multivelo.pdf"   # <paper-id>.pdf
    status: "downloaded"            # Part 4의 status 카탈로그 참조
  supplementary:
    - url: "https://static-content.springer.com/.../supp1.pdf"
      local: "sources/wang-2024-multivelo-supp-1-methods.pdf"
      type: "pdf"
      status: "downloaded"
      note: "Extended methods"
    - url: "https://static-content.springer.com/.../supp_tables.xlsx"
      local: "sources/wang-2024-multivelo-supp-2-tables.xlsx"
      type: "xlsx"
      status: "downloaded"
      note: "Supplementary Tables S1-S12"
  data:
    - url: "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE209878"
      local: "sources/data_GSE209878.url"
      type: "geo-accession"
      status: "url-only"
      note: "Human HSPC 10x Multiome"
  code:
    - url: "https://github.com/welch-lab/MultiVelo"
      type: "github"
      status: "url-only"
  abstract_text:                    # abstract auto-fetch 결과 (사용 가능 시)
    source: "pubmed"
    pmid: "38xxxxxx"
    local: "sources/abstract.txt"
    status: "downloaded"

# ───────────────────────────────────────────
# Categorization (LLM이 분석 단계에서 채움, 본인 검토)
# ───────────────────────────────────────────
categorization:
  domain:                           # source-grounding 또는 abstract-analysis 단계에서 자동 추출
    - "single-cell-genomics"
    - "epigenomics"
    - "RNA velocity"
  use_case: []                      # lens-industry 단계에서 채움
                                    # academic-citation / methodology-reference /
                                    # pipeline-applicable / BD-opportunity /
                                    # commercialization-candidate / regulatory-precedent
  importance:                       # lens-industry 단계에서 채움
    level: null                     # "상" / "중" / "하"
    perspective: null               # 어떤 관점에서 그 등급인지 한두 문장

# ───────────────────────────────────────────
# Stakeholder & priority
# ───────────────────────────────────────────
audience:                           # 이 분석 노트를 누가 다시 볼 것인가
  primary: "self"                   # self / team / bd-meeting / external / regulator
  secondary: []                     # 추가 stakeholder
  note: null
priority:
  level: "normal"                   # urgent / high / normal / low
  deadline: null                    # ISO date (YYYY-MM-DD) 또는 null
  reason: null                      # 왜 이 우선순위인지

# ───────────────────────────────────────────
# Cross-reference (연관 자료)
# ───────────────────────────────────────────
related:                            # 연관된 다른 분석의 citation.key 리스트
  - key: "li2022multivelo"
    relation: "predecessor"         # predecessor / successor / extension / competitor / cited
    note: "원본 MultiVelo paper"
  - key: "gao2024multivelovae"
    relation: "extension"
    note: "decoupling factor 추가"

# ───────────────────────────────────────────
# Workflow metadata
# ───────────────────────────────────────────
workflow:
  created: "2026-05-19"
  last_updated: "2026-05-19"
  analysis_status:
    abstract: "done"                # done / pending / skipped / not-applicable
    core: "in-progress"
    lens_academic: "pending"
    lens_industry: "pending"
    methodology_brief: "pending"
    slides: "skipped"
```

### 2.1.1 Header 블록 (자동 관리)

paper-info.yaml 파일의 *맨 앞 5줄*은 `build_index.py`가 자동 관리하는 header이다.

```yaml
# {Authors_short}, {year} — {short_keyword 또는 venue} — {venue}
# DOI: {doi}
# Topics: {primary} (primary), {secondary}  |  Importance: {level}

# ─── end of header (auto-managed by build_index.py; do not edit this block manually) ───
```

- **위 3줄 (요약 라인)** 은 `build_index.py`가 yaml 본문의 필드에서 자동 생성. 사용자가 수동 편집해도 다음 build에서 덮어쓰여짐.
- **빈 줄 + marker** 가 header 블록의 끝을 표시. marker 라인을 *지우거나 변경하지 말 것*. 지우면 build_index가 fallback 모드(leading comment block sweep)로 동작.
- **marker 이후의 yaml 본문은 사용자가 자유롭게 수정 가능**. ruamel.yaml round-trip 덕분에 *yaml 본문 안의 주석도 보존*된다.

예를 들어 분석 진행 중 분석자가 *workflow.analysis_status 위에 메모*를 남기는 것은 OK:

```yaml
# ─── end of header (auto-managed by build_index.py; do not edit this block manually) ───

# Identity
document_type: "paper"
...

# 2026-05-20: cell cycle confound 처리는 별도 sub-pipeline으로 분리 필요
workflow:
  created: "2026-05-19"
  last_updated: "2026-05-20"
  ...
```

이런 본문 주석은 build_index.py가 보존한다.

### 2.2 필드 작성 규칙

- **document_type**은 Part 7 카탈로그에서 골라 쓴다. 자유 추가 가능.
- **citation.key**는 `{lastname}{year}{shortword}` 권장 (예: `wang2024multivelo`). 충돌하면 뒷글자 추가.
- **bibtex_type**은 document_type에 맞춰 분기 (paper → `article`, preprint → `misc`, industry-report → `techreport`, ...).
- **sources의 `status`**는 Part 4의 8개 값 중 하나.
- **categorization 블록**의 빈 필드는 분석이 진행되면서 누적된다. importance.perspective는 비워두지 않는다 — 추정이라도 `해석:` prefix와 함께 한 문장.
- **audience.primary**: 분석 노트의 톤·깊이가 여기에 맞춰진다. `bd-meeting`이면 lens-industry가 더 자세, `self`면 자유로움.
- **priority.deadline**은 ISO date. 본인 일정과 자동 cross-check 가능.
- **related 블록**은 cross-reference. 같은 topic 폴더 안의 다른 분석을 `citation.key`로 link.
- **workflow.analysis_status**는 자동 갱신. `not-applicable`은 non-paper에서 figure/table이 없는 경우 등.

### 2.3 paper-info.yaml의 무결성 규칙

- `citation.key`와 BibTeX entry key가 일치.
- `sources.*.local` 경로의 파일이 *실재*해야 `status: downloaded`.
- 수정 시 `workflow.last_updated` 갱신.
- `related[].key`가 존재하지 않는 paper면 `검토필요:` 노트.

### 2.4 sources/ 파일 명명 규칙

`sources/` 안의 모든 파일은 *paper-id 기반*으로 명명한다. 폴더 밖으로 빼냈을 때도 어떤 자료인지 즉시 식별되도록.

| 파일 종류 | 명명 규칙 | 예시 |
|---|---|---|
| Paper 원문 PDF | `<paper-id>.pdf` | `li-2023-multivelo.pdf` |
| BibTeX | `<paper-id>.bib` | `li-2023-multivelo.bib` |
| Supplementary | `<paper-id>-supp-<num>-<short>.{pdf,xlsx,...}` | `li-2023-multivelo-supp-1-methods.pdf`, `li-2023-multivelo-supp-2-tables.xlsx` |
| Abstract (text) | `abstract.txt` (폴더 안에서 unique이므로 generic OK) | `abstract.txt` |
| Data accession stub | `data_<accession>.url` | `data_GSE140203.url` |
| Code stub | `code_<repo>.url` | `code_MultiVelo.url` |
| 기타 stub | `<type>_<identifier>.url` | `slides_journal-meeting.url` |

**공유 시 별도 파일명** — `paper-info.yaml`의 `citation.share_filename` 필드 (선택):

```yaml
citation:
  key: "li2023multivelo"
  share_filename: "Li 2023 - Multi-omic single-cell velocity (MultiVelo).pdf"
```

이 필드가 있으면 `share_paper.py` 스크립트(별도)가 *공유 폴더에 복사할 때* 이 이름을 사용한다. 없으면 자동 생성. 폴더 안 파일명은 *항상* `<paper-id>.pdf`를 유지하고, 공유 시에만 rename된 사본이 외부로 나간다.

---

## Part 3. Folder 생성과 초기 작업

### 3.1 디렉토리 생성

```bash
mkdir -p analysis/<primary-topic>/<paper-id>/sources
```

- **primary-topic**은 AGENTS.md의 규칙으로 결정 (kebab-case). `paper-info.yaml`의 `topics` 배열 첫 번째 값과 일치해야 한다.
- **paper-id 형식**: `<lastname>-<year>-<short-keyword>/`
  - 예: `wang-2024-multivelo/`, `gao-2024-multivelovae/`, `wang-2024-chromatin-rna-lag/`
  - **lastname**: 제1저자 성을 소문자로. 한국식 저자는 "성"만 (예: kim, park, lee).
  - **year**: 4자리. preprint면 preprint 연도, published 버전이면 published 연도.
  - **short-keyword**: 다음 우선순위로 결정:
    1. 저자가 명명한 method/tool 이름 (MultiVelo, MoFlow, scVI, RELAY 등) — 가장 자주.
    2. 없으면 핵심 어구 1~2단어 (chromatin-rna-lag, hspc-multiome, decoupling-factor 등).
    3. 모두 어려우면 venue + 단어 1개 (예: `wang-2024-nm-velocity`).
  - **충돌 처리**: 같은 lastname-year-keyword가 이미 존재하면 `-a`, `-b` suffix를 부여 (예: `wang-2024-multivelo-a`, `wang-2024-multivelo-b`). 시간 순서로 a, b, c.
  - **길이 제한**: paper-id는 40자 이내 권장.
- paper-id는 BibTeX `citation.key`와 *대응하지만 동일하지 않다*. citation.key는 yaml에 별도 (예: 폴더 `wang-2024-multivelo`, citation.key `wang2024multivelo`).

### 3.2 paper-info.yaml 시드 생성

다음 정보를 사용자에게 묻거나 입력에서 추출:

| 정보 | 출처 |
|---|---|
| document_type | 사용자가 명시하거나 URL/파일 종류에서 추론 |
| DOI 또는 PDF 경로 | 사용자 입력 또는 PDF 메타데이터 |
| Title, authors, year, venue | DOI fetch (Crossref API), PDF 메타데이터, 또는 사용자 |
| Supplementary 링크 | publisher landing page, 사용자 |
| Dataset accession | 본문 *Data availability* 또는 사용자 |
| Code repository | 본문 *Code availability* 또는 사용자 |
| audience, priority | 사용자에게 짧게 묻기 (skip 시 default 사용) |

자동 fetch가 어렵거나 부분적이면 *missing* 필드를 명시하고 사용자에게 짧게 묻는다.

### 3.3 paper.bib 생성

1. **paper / preprint**: Crossref `https://api.crossref.org/works/<DOI>/transform/application/x-bibtex` 로 fetch.
2. **conference / industry-report / corporate-publication / 기타**: LLM이 paper-info.yaml 정보로 BibTeX entry를 작성. bibtex_type을 적절히 선택.
3. `sources/paper.bib`에 저장. `citation.key`와 entry key 일치.

---

## Part 4. 다운로드 워크플로우

### 4.0 Default policy: auto-fetch before asking

새 paper 분석 요청이 들어왔을 때 default 흐름은 **fetch_sources.py 자동 시도 → 실패 시 안내 → 사용자 manual provision** 순서다. 사용자에게 "PDF를 어떻게 받을지" 다지선다로 묻기 *전에* 일단 자동 fetch부터 시도한다.

**적용 조건**:

1. `analysis/<primary-topic>/<paper-id>/sources/` 폴더가 비어 있거나, 폴더는 있지만 `<paper-id>.pdf`(또는 document_type 해당 원문 파일)가 없음.
2. `paper-info.yaml`에서 `doi` 또는 publisher URL을 추출 가능.

**시퀀스**:

1. paper-info.yaml seed 생성 (DOI / URL / title 등 기본 정보. Part 3.2).
2. `fetch_sources.py` 자동 실행 (Part 4.1, fallback chain Part 4.3).
   `--allow-scihub`는 default off.
3. 결과 평가:
   - **모두 성공** → 분석 진행. 사용자에게 "fetch 성공: paper.pdf + supp N개 받음" 한 줄만 보고.
   - **일부/전부 실패** → Part 4.4의 형식으로 *시도한 경로 + 최종 download URL + 권장 다음 행동*을 안내하고 사용자의 manual provision을 기다린다.
4. 사용자가 PDF를 `sources/`에 두면 Part 4.3.1의 자동 rename + yaml 갱신 흐름으로 이어진다.

**이 정책을 건너뛰는 예외**:

- 사용자가 명시적으로 "PDF 직접 넣을게" / "fetch 건너뛰어" / "이미 받아둔 파일 쓸게"라고 말한 경우.
- `paper-info.yaml`이 없고 DOI/URL도 추출 불가 → seed 단계로 돌아가 사용자에게 최소 정보(title 또는 DOI) 요청.
- 사용자가 abstract-only 분석을 명시적으로 선택한 경우 (Part 5.3).

**이 정책의 효과**:

- 사용자가 매번 다지선다에 답하지 않아도 fetch flow를 *밟아본 후* manual 단계로 자연스럽게 연결.
- open access paper는 즉시 자동 진행, paywall paper는 한 단계만에 사용자 manual로 fallback.
- fetch_sources.py 동작이 *모든 분석에서 default로 검증*되므로 script 자체의 신뢰성 지속 관찰 가능.
- 사용자가 skill을 호출할 때 명시적 옵션 선택 없이도 합리적 default 동작을 기대 가능 (stateless reproducibility).

### 4.1 자동 다운로드 — fetch_sources.py

`skills/source-grounding/scripts/fetch_sources.py`가 `paper-info.yaml`을 읽어 `sources/` 아래 파일을 다운로드한다.

```bash
python3 skills/source-grounding/scripts/fetch_sources.py \
  analysis/<primary-topic>/<paper-id>/paper-info.yaml
```

옵션:
- `--allow-scihub` — Sci-Hub fallback 허용 (기본 off, 본인 환경에서만 사용).
- `--fetch-abstract` — abstract 자동 가져오기 (PubMed/Crossref).
- `--discover-supp` — Nature/Springer DOI(`10.1038/...`)인 paper에 한해, `sources.supplementary[]`가 비어 있을 때만 Springer CDN(`static-content.springer.com/.../MOESM<N>_ESM.{pdf,xlsx}`)을 N=1..6까지 자동 probe. 첫 페이지 텍스트를 보고 `figures` / `reporting-summary` / `peer-review` / `source-data` 등으로 best-guess label을 붙여 `sources/<paper-id>-supp-<N>-<label>.{pdf,xlsx}` 로 저장하고 yaml에 추가. 기본 off — 이미 yaml을 수동 편집한 사용자가 의도치 않게 mutated 되지 않도록 opt-in.

`.url` stub은 cross-platform shortcut으로 작성됨:
- `<name>.url` — Windows `[InternetShortcut]` INI (Explorer에서 더블 클릭).
- `<name>.webloc` — macOS plist 형식이 같은 폴더에 함께 생성 (Finder에서 더블 클릭).
두 파일 모두 git commit 대상 — `.gitignore`는 `.url`도 `.webloc`도 제외하지 않음.

### 4.2 status 카탈로그 (8종)

| status | 의미 |
|---|---|
| `downloaded` | 파일이 local에 존재 |
| `manual-needed` | 자동 실패, 사용자가 수동 다운로드 필요 |
| `paywall` | 접근 불가, 사용자가 권한 확보 필요 |
| `failed` | 시도 후 실패. 사유를 `note`에 기록 |
| `url-only` | 의도적으로 다운로드하지 않고 URL만 (GEO accession, GitHub repo 등) |
| `preprint-only` | publisher 버전 없고 preprint만 받음. 추후 publisher 버전 나오면 추가 |
| `author-contact-needed` | 다운로드 fallback 모두 실패, 공동저자/지인 contact 필요 |
| `not-applicable` | 해당 자료 타입에는 의미 없음 (예: blog post의 supplementary) |

### 4.3 다운로드 fallback chain (5단계)

자동 다운로드 실패 시 다음 순서로 시도:

```
[1] paper-info.yaml의 primary URL — 자동
[2] Publisher landing page 재시도 — alternative URL 추출
[3] PubMed open access (PMC, NIH manuscript) — DOI → PMID lookup → PMC ID 확인
[4] Sci-Hub — opt-in (--allow-scihub flag)
[5] 공동저자/지인 contact — corresponding author 정보와 메일 템플릿 출력
```

각 단계 실패 시 status를 적절히 업데이트하고 다음 단계로. 5단계까지 가면 `author-contact-needed`로 설정.

### 4.3.1 사용자가 받은 파일의 자동 rename

사용자가 publisher 또는 PubMed에서 PDF/supplementary를 직접 다운로드한 경우, 받은 *원본 파일명*을 그대로 `analysis/<primary-topic>/<paper-id>/sources/` 폴더에 옮긴 뒤 분석 세션에게 알린다. LLM이 다음을 수행:

1. `sources/` 안의 새 파일들을 `ls`로 확인.
2. 각 파일명(`NIHMS*`, `s41587-*`, `*-supp-*`, `*MOESM*` 등) + 크기 + 필요시 첫 페이지 내용을 보고 *paper 본문 vs supplementary*를 판단.
3. paper-info.yaml의 명명 규칙 (Part 2.4)에 맞춰 `mv` 명령으로 rename.
4. paper-info.yaml의 `sources` 블록을 갱신 (`local` 경로, `status`, `supplementary` 항목 추가).

이 흐름으로 사용자는 *받은 그대로 폴더에 넣기만* 하면 되고, 명명 규칙·yaml 갱신은 LLM이 처리한다.

### 4.4 수동 다운로드 가이드 출력

자동 fallback 모두 실패한 항목은 사용자에게 다음 형식으로 안내:

```
다음 파일은 자동 다운로드 실패. 수동 확보 필요:

[1] paper "paper.pdf"
    Primary URL:    https://www.nature.com/articles/s41592-024-xxxxx.pdf  (HTTP 403)
    PubMed alt:     없음
    Sci-Hub:        (--allow-scihub 옵션 사용 시 시도 가능)
    Corresponding:  Joshua D. Welch <welchjd@umich.edu>
    Local 저장 위치: analysis/epigenomic-lag/multi-omic-relay/sources/paper.pdf

권장 순서: PubMed → publisher 직접 → Sci-Hub → 저자 contact
```

### 4.5 분석 진행 가능 여부

- **paper.pdf가 없으면 full paper 분석 진행 안 함.** abstract만 있으면 `abstract-analysis`로 대체.
- supplementary 없으면 분석 진행하되 *해당 supplementary가 다루는 부분*은 `미제공:`으로 표시.
- code/dataset이 url-only면 재현성 평가 시에만 참조.

---

## Part 5. 사용 시점별 분기

### 5.1 PDF가 주어진 경우

1. PDF 메타데이터 (title, DOI, authors) 추출.
2. paper-info.yaml 시드 생성. supplementary 링크는 사용자에게 물음.
3. `sources/paper.pdf`로 복사.
4. fetch_sources.py로 supplementary 자동 다운로드.

### 5.1.1 PDF 완전 읽기 검증 (필수 — 절단 오판 방지)

분석 전에 PDF를 **끝까지** 읽었는지 반드시 확인한다. 일부만 읽고 "PDF가 절단됐다 / 뒷 섹션이 없다"고 잘못 결론 내리는 오류를 막는 규칙:

1. **page count는 `file`이 아니라 pymupdf로 확정한다.** `file paper.pdf`의 "N pages"는 linearized·incremental PDF(arXiv 등)에서 *틀린 값*을 보고할 수 있다. 항상:
   ```bash
   python3 -c "import fitz; print(len(fitz.open('<path>')))"
   ```
   로 실제 페이지 수를 구한다.
2. **전 페이지를 읽는다.** Read의 `pages`로 1..N 전체를 ≤20p 배치로 나눠 읽는다 (>10p PDF는 `pages` 지정 필수). 일부 페이지만 보고 분석을 시작하지 않는다.
3. **절단/누락 red-flag 규칙**: 추출 텍스트가 *문장 중간에서 끊기거나*, 본문이 참조하는 `§X`·`Appendix`·`Figure/Table N`이 "안 보인다"고 느껴지면 → 이는 *PDF 결함이 아니라 읽기 누락* 신호로 먼저 간주한다. ① pymupdf page count 재확인, ② 안 읽은 페이지 읽기. **pymupdf page count로 확인하기 전에는 "PDF 절단/미제공"이라고 단정하지 않는다.** 실제로 PDF가 손상/불완전한 경우에만(다운로드 크기 0, 페이지 열기 실패 등) `검토필요:`로 표시한다.
4. (권장) 확정한 page count를 분석 메모나 provenance에 기록해 재현 시 대조 가능하게 한다.

> 사례(2026-06-13): `workman-2026-scbench`에서 `file`이 "8 pages"로 오보 → 분석이 §4.4에서 멈춰 "§4.5 grader 5종 누락(미제공)"으로 잘못 표기. 실제는 17쪽 완전본. pymupdf page count 확인으로 즉시 드러남.

### 5.2 DOI나 URL만 주어진 경우

1. DOI/URL에서 메타데이터 fetch (Crossref + publisher landing page).
2. paper-info.yaml 시드 생성.
3. fetch_sources.py로 paper와 supplementary 다운로드 시도.
4. Part 4.3 fallback chain 자동 진행.

### 5.3 Abstract만 주어진 경우 (Abstract Auto-fetch)

1. paper-info.yaml 시드 생성.
2. abstract auto-fetch 시도:
   - **PubMed E-utilities**: DOI → PMID lookup → efetch (rettype=abstract)
     ```
     https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&rettype=abstract&retmode=text
     ```
   - 실패 시 **Crossref**: `works/<DOI>` JSON의 `abstract` 필드.
   - 실패 시 **publisher landing page 크롤링** (selectors per publisher).
3. `sources/abstract.txt`에 저장, `abstract_text.status: downloaded`.
4. `abstract-analysis` skill 호출.
5. 나중에 full paper로 확장 시 PDF만 추가하면 됨. `abstract.txt`는 보존, `<paper-id>_core.md`를 새로 생성.

### 5.4 Non-paper reference (학회/기업/리포트/뉴스/블로그)

→ Part 7 참조.

### 5.5 이미 paper-info.yaml이 있는 경우

1. 기존 yaml을 로드.
2. **sources 무결성 점검**: `sources/<paper-id>.pdf` (또는 해당 document_type의 원문 파일)가 실재하는지 확인. 없으면 **Part 4.0 정책에 따라 fetch_sources.py를 자동 실행**한 뒤 실패 시 사용자에게 manual provision 안내.
3. 사용자가 추가/수정 요청한 부분만 갱신.
4. `workflow.analysis_status`에 따라 어디서부터 이어갈지 결정.

---

## Part 6. 출력 체크리스트

source-grounding 단계가 끝났을 때 다음이 충족되어야 한다.

- [ ] `analysis/<primary-topic>/<paper-id>/` 디렉토리 존재 (paper-id 형식 = `<lastname>-<year>-<short-keyword>`).
- [ ] `paper-info.yaml` 존재, Identity·version·citation·sources·topics 블록 채워짐.
- [ ] `paper-info.yaml` 첫 줄에 human-readable header (3줄) 존재.
- [ ] `topics` 배열의 첫 번째 값이 폴더 경로의 `<primary-topic>`과 일치.
- [ ] document_type에 맞게 sources 필드 분기.
- [ ] `sources/paper.pdf` 또는 `sources/abstract.txt` 또는 *non-paper local file* 존재.
- [ ] `sources/paper.bib` 존재, citation.key와 entry key 일치.
- [ ] supplementary 항목이 다운로드되거나 fallback chain까지 시도됨.
- [ ] 외부 지식 차단 규칙이 분석 세션 전체에 적용됨을 사용자와 다른 skill이 인지.
- [ ] audience, priority가 짧게라도 채워짐 (skip 시 default).
- [ ] `workflow.analysis_status` 초기화.
- [ ] `build_index.py` 실행되어 `analysis/_index/papers.csv`와 `_index/<topic>.md`가 갱신됨.

---

## Part 7. Non-paper References

`document_type`에 따라 paper-info.yaml의 일부 필드는 *없거나 의미가 달라진다*. 분석 skill도 일부는 호출하지 않는다.

### 7.1 document_type 카탈로그

| document_type | 설명 | BibTeX type | 주로 호출되는 skill |
|---|---|---|---|
| `paper` | 정식 학술지 논문 (peer-reviewed) | `article` | core-* 전부 + lens-* + methodology-brief |
| `preprint` | bioRxiv, arXiv, medRxiv | `misc` 또는 `unpublished` | core-* 전부 + lens-* + methodology-brief |
| `conference-paper` | 학회 proceeding 논문 | `inproceedings` | core-* + lens-* |
| `conference-poster` | 학회 포스터 | `misc` | core-figure (포스터 자체가 figure 역할) + lens-* |
| `conference-talk` | 학회 구두 발표 (슬라이드·녹화) | `misc` | core-figure (선택) + lens-* |
| `industry-report` | 시장조사·컨설팅 리포트 (BCG/McKinsey/Evaluate 등) | `techreport` | lens-industry 중심 + core-table (수치 있을 시) |
| `corporate-publication` | 기업 발행물 (white paper / 투자자 자료 / 기술 brief / press release / IR 자료) | `techreport` 또는 `misc` | lens-industry 중심 |
| `government-report` | 정부·규제기관 보고서 (FDA / EMA / NIH) | `techreport` | lens-industry 중심 + regulatory-precedent 태깅 |
| `regulatory-document` | 승인 letter, guidance document, label | `misc` | lens-industry 전용 |
| `news` | 언론 기사, 동향 분석 | `misc` 또는 `article` | 경량 요약 + lens-industry (의미) |
| `whitepaper` | 학술/기술 백서 (corporate-publication과 겹칠 수 있음) | `techreport` | lens-industry 중심 + 선택적 core-methods |
| `book-chapter` | 책의 챕터 | `incollection` | core-problem + core-methods (선택) |
| `blog` | 블로그 글, online article | `online` | 경량 요약 + lens-* (선택) |
| `webinar` | 온라인 세미나 | `misc` | 경량 요약 + lens-* (선택) |

위에 없으면 자유 추가 가능. 단 자주 쓰는 새 type은 vocabulary에 반영 요청.

### 7.2 Non-paper의 paper-info.yaml 작성 가이드

- `doi`가 없을 수 있다 → `url`로 대체.
- `venue` 대신 *발행 기관*(기업·정부·미디어). 예: `venue: "BCG"`, `venue: "FDA"`, `venue: "Nature News"`.
- `authors`는 unknown이면 빈 list. 기업 리포트는 기관명을 author로 두는 것도 OK.
- `version`: corporate-publication은 *발행 차수*·*revision*을 기록. 예:
  ```yaml
  version:
    type: "released"
    edition: "Q3 2024 update"
    date: "2024-10-15"
  ```
- `supplementary` 대신 *appendix*, *exhibit*, *related deck* 등을 자유롭게 기록.
- `peer_reviewed: false`가 명확해야 lens-industry가 *권위 가중치*를 조정할 수 있다.

### 7.3 Non-paper의 분석 흐름 (경량)

paper/preprint와 달리, non-paper는 모든 core-* skill을 호출하지 않는다. AGENTS.md에서 다음 규칙을 따른다:

1. **항상**: source-grounding으로 폴더·yaml·sources 정리.
2. **항상**: core-problem 대체 — *왜 이 자료가 발행되었나*, *주장의 핵심* 한 섹션. (core-problem skill의 톤을 살짝 변형해 사용)
3. **document_type에 따라**:
   - **methods 호출**: peer-reviewed paper, preprint, conference-paper, whitepaper, government-report (방법론이 자세히 적힌 경우).
   - **figure/table 호출**: 시각자료가 있는 모든 type. 단 conference-poster는 *포스터 자체*를 한 figure로 다룸.
   - **lens-industry 항상 호출**: non-paper는 거의 항상 *사업·규제·산업적 시사*가 핵심.
   - **lens-academic 선택**: 인용 가능성·후속 연구 시사가 있을 때만.
   - **methodology-brief 선택**: 재현·검토가 의미있는 경우만.

### 7.4 권위·신뢰 가중치 표시

non-paper는 peer review가 없거나 출처 신뢰도가 다양하다. 분석 노트에서 다음 prefix로 *권위 수준*을 명시할 수 있다.

- `1차 출처:` — 원 출처가 권위 있음 (FDA letter, 기업 IR 자료, Nature paper).
- `2차 출처:` — 1차 출처를 요약·해석 (시장조사 리포트, 뉴스 기사).
- `의견·해설:` — 검증된 사실이 아닌 의견·예측 (블로그, opinion piece).

`lens-industry`에서 이 가중치를 importance.perspective에 반영한다.

---

## Part 8. Index 자동 생성 (`analysis/_index/`)

Option E의 다중 topic 지원을 위해, paper-info.yaml들을 순회해 통합 인덱스를 *자동 생성*한다. 사용자가 직접 편집하지 않는다.

### 8.1 생성되는 파일

```
analysis/_index/
├── papers.csv          # 모든 paper의 통합 표 (RFC 4180 quoted CSV, Excel/Numbers/Sheets 호환)
├── <topic>.md          # topic별 markdown 목록 (primary + secondary로 속한 paper 모두 포함)
└── README.md           # 인덱스 사용 가이드
```

### 8.2 papers.csv schema

다음 열을 기본으로 한다. `csv.writer`가 자동으로 표준 quoting (콤마·따옴표·줄바꿈을 안전 처리).

| 열 | 출처 (paper-info.yaml) | 비고 |
|---|---|---|
| `folder` | 계산값 | primary topic + paper-id (예: `epigenomic-lag/wang-2024-multivelo`) |
| `paper_id` | folder 끝 segment | `wang-2024-multivelo` |
| `title` | `title` | 원문 그대로 (콤마 포함 시 quoting됨) |
| `authors_short` | `authors[0]` + " et al." | 표시용 |
| `year` | `year` | |
| `venue` | `venue` | |
| `doi` | `doi` | |
| `document_type` | `document_type` | |
| `topics` | `topics` | semicolon 구분 (예: `epigenomic-lag;single-cell-genomics`) |
| `use_case` | `categorization.use_case` | semicolon 구분 |
| `importance_level` | `categorization.importance.level` | 상/중/하 |
| `importance_perspective` | `categorization.importance.perspective` | |
| `audience_primary` | `audience.primary` | |
| `priority_level` | `priority.level` | |
| `priority_deadline` | `priority.deadline` | ISO date |
| `analysis_status_short` | `workflow.analysis_status` | 압축 표현 (예: `abs:done,core:ip,la:pn,li:pn,mb:pn,sl:sk`) |
| `last_updated` | `workflow.last_updated` | |
| `citation_key` | `citation.key` | BibTeX cross-ref용 |

새 열 추가가 필요하면 build_index.py에 반영하고 schema도 업데이트.

### 8.3 `_index/<topic>.md` 형식

각 topic에 *primary 또는 secondary*로 속한 모든 paper를 한 markdown 표로.

```markdown
# Topic: epigenomic-lag

마지막 갱신: 2026-05-19

## Papers (primary topic으로 등록된 것)

| Paper | Year | Venue | Importance | Use case | Status |
|---|---|---|---|---|---|
| [wang-2024-multivelo](../epigenomic-lag/wang-2024-multivelo/) | 2024 | Nat Methods | 상 | methodology-reference; pipeline-applicable | core: done |
| [gao-2024-multivelovae](../epigenomic-lag/gao-2024-multivelovae/) | 2024 | Nat Methods | 중 | methodology-reference | core: in-progress |

## Related (secondary topic으로만 등록된 것)

| Paper | Primary topic | Year | Venue | Importance |
|---|---|---|---|---|
| [li-2022-chromatin-coupling](../chromatin-dynamics/li-2022-chromatin-coupling/) | chromatin-dynamics | 2022 | Genome Res | 중 |
```

### 8.4 build_index.py 동작

```bash
python3 skills/source-grounding/scripts/build_index.py
```

옵션:
- `--topic <name>` — 특정 topic의 markdown만 다시 빌드.
- `--csv-only` — papers.csv만.
- `--verbose` — 처리 중인 yaml 경로 출력.

동작:

1. `analysis/**/paper-info.yaml`을 모두 찾기 (`_index/` 제외).
2. 각 yaml을 파싱. 필수 필드(`topics`, `title`, `year` 등)가 없으면 경고 출력하고 skip.
3. `papers.csv` 생성: 8.2 schema대로 한 줄씩 작성. `csv.writer`로 자동 quoting.
4. 각 topic별로:
   - 그 topic을 `topics`에 포함하는 yaml을 모음.
   - `topics[0] == topic`인 paper는 *primary* 섹션에.
   - 그 외 (`topic in topics[1:]`)는 *Related* 섹션에.
   - `_index/<topic>.md` 작성.
5. paper-info.yaml의 *첫 줄 human-readable header*도 동시에 갱신:
   - `# {Authors_short}, {year} — {short_keyword 또는 venue} — {venue}`
   - `# DOI: {doi}` (있으면)
   - `# Topics: {primary} (primary), {secondary} | Importance: {level}`
6. `_index/README.md` 자동 작성 (간단한 사용 가이드).

### 8.5 언제 실행하는가

다음 시점에 자동 또는 수동 실행:

- **source-grounding이 새 paper-info.yaml을 생성한 직후** — 자동.
- **`lens-industry`가 importance/use_case를 채운 직후** — 자동.
- **사용자가 `topics` 배열을 수정한 직후** — 수동 또는 자동.
- **분석 진행 상태 갱신 직후** — workflow.analysis_status가 변하면 자동.
- **사용자가 명시적으로 갱신 요청** — 수동.

자동 실행 시점은 각 호출 skill이 *완료 직후* `build_index.py`를 호출. 실패해도 분석을 막지 않는다 (인덱스는 *부수 효과*, 분석 자체는 paper-info.yaml에 누적됨).

### 8.6 인덱스 무결성

- `_index/` 디렉토리는 git에 commit한다 (협업자와 공유).
- 단 build_index.py가 멱등(idempotent)하므로 *재생성 가능한 캐시*로 취급해도 OK.
- 충돌이 잦으면 `.gitignore`에 추가하고 *각자 로컬에서 빌드*하는 방식도 가능.

---

## 주의할 점

- **Topic을 모호한 채로 진행하지 않는다.** AGENTS.md의 규칙대로 topic을 먼저 확정.
- **paper-id가 너무 길면 줄인다.** 40자 이내 권장. 단축 시 paper-info.yaml의 `title`은 원문 보존.
- **paper-info.yaml 첫 줄 header는 직접 편집하지 않는다.** build_index.py가 갱신한다.
- **자동 다운로드를 강제하지 않는다.** 사용자가 이미 PDF를 가지고 있다고 말하면 수동 경로를 따른다.
- **Sci-Hub는 기본 off.** `--allow-scihub` flag로 명시적 opt-in해야 시도. 본인 환경의 합법성은 사용자가 책임.
- **categorization 필드는 비어둘 수 있다.** 나중 skill이 채운다. 단 키는 둔다 (스키마 일관성).
- **본 skill은 분석을 시작하지 않는다.** 폴더와 메타데이터 준비까지만. 실제 분석은 호출하는 라우터(AGENTS.md)나 후속 skill이 담당.
- **non-paper에서 paper-info.yaml의 paper-* 필드명**: 이름은 그대로 유지(예: `sources.paper`). 내용만 분기. 일관성이 변경 비용보다 가치 있음.
- **`_index/`는 자동 생성이다.** 사용자가 markdown을 직접 손대면 다음 build에서 덮어쓰여짐.
