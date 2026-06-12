# Dataset 1 — Secondary References

이 dataset을 분석한 refereed paper / preprint 목록. *de facto* representative analyses (peer-reviewed paper 본체가 없으므로 이 목록이 그 역할).

각 항목은 (a) 이 dataset을 어떤 version으로 받았는지, (b) 어떤 preprocessing을 거쳤는지, (c) 어떤 metric / model로 분석했는지, (d) reported 핵심 수치를 기록. 본 프로젝트 Dataset 1 agent의 *재현 target* + *비교 baseline* 이 된다.

---

## 1. Li 2023 — MultiVelo (Nature Biotechnology)

- **이 paper의 정식 분석본**: [analysis/epigenomic-lag/li-2023-multivelo](../../epigenomic-lag/li-2023-multivelo/) (full core + lens + methodology-brief 모두 작성됨).
- **이 dataset에 대한 핵심 sub-section**: `li-2023-multivelo_core.md` → "#### Dataset 1 — 10x Multiome E18 mouse brain".
- **Status**: **첫 refereed analysis**. 본 프로젝트 Dataset 1의 *재현 target*.

### Reported preprocessing
- 출처: 10x Genomics website 공개 (version 명시 안 됨 — MultiVelo GitHub tutorial 기준 `1.0.0` 추정).
- ATAC peak calling 등의 detail은 MultiVelo Methods section 참조.
- Filtering 후 **3,365 cells × 936 highly variable genes**. ODE model에 들어간 high-likelihood gene **426개** (likelihood threshold scVelo 기본 0.05).

### Reported analyses & numbers
| 분석 | 결과 |
|---|---|
| Cell trajectory 복원 | RG → IPC → ExN (upper/deeper layer 분리) — scVelo의 backflow 해소 (Fig. 2a, 2c) |
| Gene state distribution (variable genes 865개 중) | induction-only 29.5%, repression-only 2.4%, **M1 41.4%, M2 26.7%** (Fig. 2h) |
| M1 vs M2 expression timing | M2 highest spliced expression *earlier* — Wilcoxon one-sided **P = 9×10⁻⁷** |
| M1 vs M2 expression / accessibility 총량 | Wilcoxon P = 0.38, 0.32 (no significant difference) |
| M2 GO enrichment | cell-cycle terms (positive regulation of cell cycle, mitotic cell cycle, regulation of cell cycle phase transition) — exact FDR 미제공 |
| State interval (median across genes) | primed 21%, decoupled 19%, coupled-on + coupled-off ≈ 60% (Fig. 3e) |
| Chromatin closing / opening rate ratio | median ≈ 1 (Fig. 3f) |

### Highlight Figures (이 dataset 한정)
- **Figure 2**: chromatin 추가가 cell fate prediction 정확도 개선 + M1/M2 gene 분류의 gene-level validity 동시 입증.
- **Figure 3**: priming + decoupling phenomenon이 artifact가 아니라 reproducible signature임을 보임. Robo2, Gria2, Grin2b — decoupled state에서 chromatin/RNA UMAP discrepancy 최대.

### 본 프로젝트와 직결되는 점
- Dataset 1 agent의 *재현 target* — 위 수치들을 ±α% 이내로 reproduce하면 pipeline이 MultiVelo와 정합.
- "선행 접근 D — single-cell epigenome velocity (Ma 2020 SHARE-seq chromatin potential)" 와의 차별점이 이 dataset에서 시각적으로 드러남 — chromatin potential이 *binary priming* 표현인 반면 MultiVelo는 *시간 단위 lag* 정량.

---

## 2. Li 2025 — MultiVeloVAE (Nature Communications)

- **이 paper의 정식 분석본**: [analysis/epigenomic-lag/li-2025-multivelovae](../../epigenomic-lag/li-2025-multivelovae/) (full core + lens + methodology-brief 작성됨).
- **이 dataset에 대한 핵심 언급**: `li-2025-multivelovae_core.md` Dataset section — "Mouse brain 10x Multiome (`@li2023multivelo` AnnData 재사용)".
- **Status**: **benchmark reuse**. preprocessing pipeline을 새로 돌리지 않고 MultiVelo 저자 release AnnData 직접 사용 → Dataset 1의 *canonical preprocessing*은 사실상 MultiVelo 저자 release.

### Reported preprocessing
- AnnData 그대로 사용 → cell/gene 수는 MultiVelo Dataset 1과 동일 (3,365 cells × 936 genes 가정).

### Reported analyses & numbers
- VAE 기반 latent time → MultiVelo와의 직접 비교 metric (Spearman, DTW lag 등).
- 구체 수치는 li-2025-multivelovae core.md Results 참조 (작성 완료, 폴더 내 file).

### 본 프로젝트와 직결되는 점
- Dataset 1을 통해 MultiVelo (ODE) vs MultiVeloVAE (VAE) 두 architecture를 같은 cells에서 직접 비교 가능 → 본 프로젝트도 둘 다 baseline으로 두기 적합.

---

## 3. (Pending check) 다른 chromatin-RNA velocity / multi-omic methods

다음 paper들이 Dataset 1 (또는 유사한 10x E18 mouse brain Multiome demo)을 사용했는지 각 paper 분석본에서 cross-check 필요. 사용했다고 확인되는 대로 이 section에 추가.

- [ ] **DeepVelo** ([cui-2024-deepvelo](../../epigenomic-lag/cui-2024-deepvelo/), Genome Biology 2024)
- [ ] **MoFlow** ([hong-2026-moflow](../../epigenomic-lag/hong-2026-moflow/), Nat Commun 2026)
- [ ] **mmVelo** ([nomura-2024-mmvelo](../../epigenomic-lag/nomura-2024-mmvelo/), bioRxiv 2024)
- [ ] **DeepKINET** ([mizukoshi-2024-deepkinet](../../epigenomic-lag/mizukoshi-2024-deepkinet/))
- [ ] **cellDancer** ([li-2023-celldancer](../../epigenomic-lag/li-2023-celldancer/), Nature Biotechnology 2023)

확인 방법: 각 paper의 `<paper-id>_core.md` "Results" → Dataset section에서 "10x", "E18", "mouse brain", "embryonic" 등 grep. 사용 확인 시 (1) 이 file에 항목 추가, (2) `dataset-info.yaml`의 `secondary_refs`에도 추가, (3) 해당 paper의 `paper-info.yaml`에 `related:` cross-ref 양방향.

---

## 갱신 이력

- 2026-05-26 — 초기 생성. MultiVelo (Li 2023), MultiVeloVAE (Li 2025) 두 항목 등록. 다른 paper들은 cross-check pending.
