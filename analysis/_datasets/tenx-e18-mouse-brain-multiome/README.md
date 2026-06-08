# Dataset 1 — 10x E18 Mouse Brain Multiome (vendor demo)

본 프로젝트 4개 dataset 중 1번. **동반 paper 없음** — 10x Genomics가 release한 demo dataset.

## TL;DR (agent briefing 용)

- **무엇**: 10x Genomics가 *Chromium Multiome (ATAC + GEX)* 제품 시연용으로 release한 E18 mouse brain ~5,000 cells. 실제 cell 기반 real data (BrainBits LLC commissioned).
- **왜 우리 4개 dataset에 들어가 있는가**:
  - 가장 단순 (mouse, 잘 알려진 cortex trajectory RG → IPC → ExN → upper/deeper layer).
  - chromatin-RNA velocity 후속 paper들이 *공통 benchmark*로 쓰는 dataset → 본 프로젝트 결과를 literature와 직접 대조 가능.
  - 가장 작음 (~3,365 cells QC 후) → pipeline 변경 시 빠른 smoke test.
- **anchor**: paper 대신 ① 10x dataset page (CC BY 4.0) + ② MultiVelo (Li 2023) Dataset 1 section (`analysis/epigenomic-lag/li-2023-multivelo/li-2023-multivelo_core.md`의 "Dataset 1 — 10x Multiome E18 mouse brain").

## "Demo dataset"이 의미하는 것

| 오해 | 사실 |
|---|---|
| Synthetic / toy data | ❌. Real cells from BrainBits LLC commissioned mouse, real Multiome library, real sequencing. |
| 품질이 낮음 | ❌. 10x 내부 QC 통과, gold-standard. |
| 사용 제한 | ❌. CC BY 4.0 (citation만 하면 자유). |
| Peer-reviewed paper 있음 | ❌. 10x는 biology paper를 쓰지 않음. technical document (protocol, user guide)만 존재. |

차이는 *오직* **publication anchor의 형태**: paper 대신 vendor dataset page + technical docs + 후속 paper들의 reuse 기록.

## Agent operation 가이드

이 dataset agent (담당: **이건규**, CLAUDE.md "팀 & 데이터셋 담당" 표) 가 작업 시작할 때 다음 순서로 anchor를 읽는다.

1. **`dataset-info.yaml`** (이 폴더) — single source of truth. provenance, license, cell counts, secondary refs.
2. **10x dataset page** (CG000366 protocol, CG000338 user guide 링크 포함, `sources/*.url`).
3. **MultiVelo (Li 2023) Dataset 1 section** — first refereed analysis. 본 프로젝트의 *재현 target* 수치 출처.
   - 위치: [analysis/epigenomic-lag/li-2023-multivelo/li-2023-multivelo_core.md](../../epigenomic-lag/li-2023-multivelo/li-2023-multivelo_core.md) ("#### Dataset 1 — 10x Multiome E18 mouse brain").
4. **MultiVelo의 preprocessed AnnData** — Dataset 1의 *de facto* canonical preprocessing은 MultiVelo 저자가 release. MultiVeloVAE (li-2025-multivelovae)가 이 AnnData를 그대로 사용. 본 프로젝트도 시작점으로 이걸 권장.

## 다른 dataset agent와의 anchor 구조 비교

| Agent | Anchor type | Anchor location |
|---|---|---|
| Dataset 1 (10x E18 brain) | **dataset-info + vendor docs + de facto paper** | `analysis/_datasets/tenx-e18-mouse-brain-multiome/` (이 폴더) |
| Dataset 2 (SHARE-seq skin) | paper analysis (`paper-info.yaml`) | `analysis/chromatin-rna-coupling/ma-2020-shareseq/` |
| Dataset 3 (Trevino cortex) | paper analysis | `analysis/single-cell-genomics/trevino-2021-cortex/` |
| Dataset 4 (HSPC) | paper analysis (Li 2023 MultiVelo) | `analysis/epigenomic-lag/li-2023-multivelo/` (Dataset 3 section in core.md) |

4개가 *parallel*한 anchor structure를 가진다 — Dataset 1만 schema가 살짝 다를 뿐 (paper-info.yaml → dataset-info.yaml).

## 우선 확인할 것 (agent 첫 sprint)

1. 어느 10x release version을 받을 것인지 확정 — `1.0.0` (MultiVelo 사용본) vs `2.0.0` (Cell Ranger ARC 2.0 재처리본) vs `3.1 standard 6.0.0` (cortex + hippocampus + SVZ). MultiVelo와 직접 비교하려면 `1.0.0` 권장.
2. preprocessed AnnData를 MultiVelo 저자 release에서 받을지, raw에서 직접 재처리할지 — pipeline 검증 목표에 따라 결정. 초기에는 저자 AnnData로 reproduce → 후에 raw에서 재처리하며 step별 sensitivity 검증.
3. `expected_outputs` 항목 (dataset-info.yaml `project_role.expected_outputs`)을 *quantitative target*으로 확정.

## 다른 dataset과 cross-validation 시점

본 프로젝트의 핵심 가설 — "chromatin → RNA lag (`activation lag` / `shutdown lag`)이 gene별로 정량 가능하고 후속 epigenetic drug response timing을 예측한다" — 의 *최소 cross-dataset 일관성 검증*은 다음 비교가 핵심:

- Dataset 1 ↔ Dataset 2: same species (mouse), different platform (10x vs SHARE-seq) → platform 잡음 분리.
- Dataset 1 ↔ Dataset 3: same tissue family (cortex developmental), different species (mouse vs human) → species-conserved lag program 식별.
- Dataset 4 (HSPC time-course): wall-clock time (day0/day7) 있는 유일한 dataset → pseudotime ↔ wall-clock conversion factor estimation의 anchor (CLAUDE.md "Pseudotime ≠ Wall-clock time" 주의사항 직접 다룸).
