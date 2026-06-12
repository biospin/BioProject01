# `_datasets/` — Dataset reference cards

이 디렉토리는 *paper attachment 없이 공개된 dataset* (예: vendor demo, repository public release) 의 reference card를 모은다. `analysis/<topic>/<paper-id>/`의 paper analysis 폴더와 **목적이 다르고 schema도 다르다**.

## 왜 필요한가

본 프로젝트는 4개 dataset (CLAUDE.md "주요 데이터셋" 표 참조) 위에서 chromatin–RNA lag 분석 agent를 운영한다. dataset 중 3개는 동반 paper가 있어 `analysis/<topic>/<paper-id>/` 구조에 자연스럽게 들어가지만 **1개 (10x E18 mouse brain Multiome)는 10x Genomics가 demo 형태로 release한 dataset이라 동반 publication이 없다**. 그래도 agent에게 *anchor document*를 줘야 하고, "데이터를 어떻게 받았고 어디서 왔는지" 등을 추적 가능한 단일 location이 필요해서 별도 카테고리로 만든다.

## paper analysis 폴더와 다른 점

| 항목 | paper analysis (`<topic>/<paper-id>/`) | dataset reference (`_datasets/<dataset-id>/`) |
|---|---|---|
| 단일 source of truth | `paper-info.yaml` | `dataset-info.yaml` |
| 핵심 결과물 | `<paper-id>_core.md`, `_lens-academic.md`, `_lens-industry.md`, `_methodology-brief.md` | `README.md`, `secondary-refs.md` |
| `build_index.py`가 색인 | ✅ `analysis/_index/`에 자동 추가 | ❌ skip (`paper-info.yaml`만 검색하므로) |
| 출력 lens | academic + industry | 없음 (객관적 사실만) |
| `core-to-html` 적용 | ✅ | ❌ |

## 디렉토리 컨벤션

```text
_datasets/
├── README.md                                    # 이 파일
└── <dataset-id>/                                # 예: tenx-e18-mouse-brain-multiome
    ├── dataset-info.yaml                        # single source of truth (자체 schema, 아래 참고)
    ├── README.md                                # human-readable summary (agent briefing용)
    ├── secondary-refs.md                        # 이 dataset을 분석한 paper들 (de facto representative refs)
    └── sources/                                 # 외부 자료 link (PDF는 .gitignore되므로 .url 위주)
        ├── *.url                                # link to vendor page, protocol, user guide
        └── (optional) *.pdf                     # protocol document local copy
```

## `dataset-info.yaml` schema (간이판)

```yaml
# Identity
dataset_id: "<kebab-case-id>"
provider: "<vendor / consortium / repository name>"
version: "<e.g. 1.0.0>"
release_date: "YYYY-MM-DD or 미제공"

# Biological identity
species: "<e.g. Mus musculus>"
tissue: "<e.g. Embryonic E18 cerebral cortex + hippocampus + SVZ nuclei>"
sample_provenance: "<who collected, how, supplier>"
modality: ["<e.g. scRNA-seq>", "<e.g. scATAC-seq>", "<paired Multiome 등>"]
platform: "<e.g. 10x Genomics Chromium Multiome ATAC + Gene Expression>"

# Scale
cell_count_advertised: <int>
cell_count_after_qc: <int or 미제공>
gene_count_advertised: <int or 미제공>

# Access
access:
  primary_url: "<vendor or repository URL>"
  geo_accession: "<GSE... or null>"
  license: "<e.g. CC BY 4.0>"
  citation_form: "<how the vendor asks you to cite>"

# Documents (paper가 아닌 technical docs)
documents:
  - title: "<e.g. CG000366 Demonstrated Protocol>"
    url: "<link>"
    local: "sources/<filename>.url"
    type: "protocol | user-guide | application-note | white-paper"
    note: "<왜 이게 anchor에 들어가는지>"

# Secondary references (이 dataset을 분석한 paper들)
secondary_refs:
  - paper_id: "<paper-id 또는 외부>"
    relation: "first-refereed-analysis | benchmark-reuse | downstream-reanalysis"
    note: "<어떤 부분에 쓰이고 어떤 모델이 어떤 metric으로 평가했는지>"

# Role in this project
project_role:
  dataset_number: <1, 2, 3, or 4>
  agent_owner: "<담당자 — CLAUDE.md 표 참조>"
  primary_use: "<e.g. smoke test + 문헌 비교 anchor>"
  expected_outputs: ["<e.g. MultiVelo M1/M2 분포 재현>", "<...>"]

# Workflow metadata
workflow:
  created: "YYYY-MM-DD"
  last_updated: "YYYY-MM-DD"
  status: "active | deprecated | candidate"
```

## 갱신 규칙

- `dataset-info.yaml`이 single source of truth. `README.md`, `secondary-refs.md`는 이걸 보조하는 사람이 읽는 view.
- 새 paper가 이 dataset을 reuse하면 `secondary_refs`에 항목 추가 + paper analysis 폴더(`analysis/<topic>/<paper-id>/`)에 `related:` cross-ref를 양방향으로 단다.
- `build_index.py`는 이 dir를 무시하므로 `_index/`에는 안 보인다. 사람이 이 README를 직접 참조.
