# Lit Search — Human HSPC 10x Multiome (GSE209878)

- 수행일: 2026-06-12
- 입력: dataset accession `GSE209878` (담당: 김가경 / 류재면)
- 분석 목표 정합: gene별 chromatin–transcription **lag** 정량 → epigenetic drug response timing 예측 (`CLAUDE.md` 연구 핵심 개념)

## 데이터셋/주제 Identity

- **GSE209878** = MultiVelo 논문의 원본 HSPC 데이터셋. GEO title "Single-cell multi-omic velocity infers dynamic and decoupled gene regulation", PMID 36229609.
- 설계: Human HSPC, paired ATAC+RNA (10x Multiome), **day0/day7 2개 timepoint** — 본 프로젝트 dataset 중 wall-clock time이 있는 유일한 것 (pseudotime ↔ wall-clock 변환 anchor).
- repo 내 원 논문: `analysis/epigenomic-lag/li-2023-multivelo/` (이미 full analysis 완료).
- 검토필요: 아직 `analysis/_datasets/`에 이 dataset 전용 reference card(dataset-info.yaml + secondary-refs.md)는 미작성.

## repo에 이미 있어 직접 쓰는 문헌

| paper-id | 역할 | why |
|---|---|---|
| `li-2023-multivelo` | anchor + method | 이 dataset의 원 논문 + MultiVelo 방법. chromatin–RNA lag 정량 baseline. |
| `li-2025-multivelovae` | method | 직접 후속/대체 후보. HSPC 데이터 사용, continuous (δ, κ) + multi-sample 통합. |
| `hong-2026-moflow` | method | chromatin–RNA c-s lag 정량(Fig.7)이 프로젝트 outcome과 1:1. |
| `nomura-2024-mmvelo` | method | peak-level chromatin velocity (gene aggregation gap 보완). preprint-tier. |
| `li-2023-celldancer`, `cui-2024-deepvelo`, `mizukoshi-2024-deepkinet` | method(계보) | RNA-only velocity/kinetic 계보·검증 reference. |

## 새로 확보 권장 — Method (repo 부재)

| 제목 | 저자·연도·venue | DOI/URL | 역할 | why | repo 상태 |
|---|---|---|---|---|---|
| CRAK-Velo: Chromatin Accessibility Kinetics integration improves RNA Velocity estimation | bioRxiv 2024 | 10.1101/2024.09.12.612736 | method | MultiVelo 직접 경쟁/대체 chromatin-aware velocity. lag 분석 핵심 후보(최우선). | 새로 확보 |
| Benchmarking RNA velocity methods across 17 independent studies | Cell Reports Methods 2026 (bioRxiv 2025.08.02.668272) | S2667-2375(26)00067-6 | benchmark | MultiVelo 포함 벤치마크 → 우리 데이터에 어떤 method를 쓸지 근거. | 새로 확보 |
| Benchmarking algorithms for RNA velocity inference | bioRxiv 2026.01 | 10.64898/2026.01.03.697314 | benchmark | scKINETICS vs MultiVelo 비교 포함. 추정: scKINETICS가 더 일관된 신호 보고 → 후보 method 검토. | 새로 확보 |

## 새로 확보 권장 — Biology (lag 가설 검증, repo 부재)

핵심 가정("chromatin이 transcription보다 먼저 열린다 = activation lag")을 **같은 cell type(HSPC)에서** 뒷받침:

| 제목 | 출처 | why |
|---|---|---|
| Concurrent stem- and lineage-affiliated chromatin programs precede hematopoietic lineage restriction | Cell Reports 2022, PMID 35545037 | HSPC에서 chromatin priming이 commitment에 선행 — lag 개념 직접 근거. |
| Chromatin Accessibility Maps Provide Evidence of Multilineage Gene Priming in HSCs | bioRxiv 2020.11.24.394882 | multilineage priming 개념. |
| Dynamics of Chromatin Accessibility During HSC Differentiation | 리뷰, PMC10183972 | HSPC 분화 중 chromatin dynamics 개관. |

## 권장 다음 단계

1. **CRAK-Velo** → `source-grounding`으로 단일 full analysis 진행 (topic: `epigenomic-lag`, method 비교 baseline).
2. **velocity benchmark 2편** → `analysis/epigenomic-lag/_evidence/week2/scope.md` seed에 추가 후 `paper-scrapper`로 묶어 비교.
3. **HSPC biology 3편** → abstract-only 또는 metadata-only record로 등록 (lag 가설 검증 evidence).
4. **dataset reference card** → `analysis/_datasets/tenx-hspc-multiome-gse209878/`에 `dataset-info.yaml` + `secondary-refs.md` 작성, 위 repo 논문 4편을 secondary_refs로 cross-ref.

> 검증: 위 DOI·연도는 GEO 페이지 + 검색 결과 기준. repo commit 전 `skills/metadata-verify`로 교차 확인 권장.
