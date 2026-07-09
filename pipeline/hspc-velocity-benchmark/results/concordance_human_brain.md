# P3 cross-dataset concordance — HSPC ↔ human_brain

> BIOP01 HSPC 벤치마크의 MultiVelo lag/timing이 외부 multiome(human_brain)에서 rank 재현되는가.
> 성공 기준(RUNBOOK §7): |Spearman| > 0.3 (단일 replication).

## 입력
- HSPC MultiVelo: `multivelo_genes.csv` — 538 gene
- human_brain MultiVelo: `multivelo_genes_human_brain.csv` — 551 gene
- HSPC floor: `rna_only_dynamical_genes.csv` — 487 gene
- human_brain floor: `rna_only_dynamical_genes_human_brain.csv` — 711 gene

## MultiVelo 일치도 (headline = lag 크기)

- **lag(fit_t_sw2−fit_t_sw1) 크기 rank  ← headline** (shared 102): Spearman **+0.185** (p=0.063) → 약함/미재현(|r|≤0.3)
- **switch timing fit_t_sw2 rank** (shared 102): Spearman **+0.049** (p=0.63) → 약함/미재현(|r|≤0.3)
- **rate fit_alpha rank** (shared 102): Spearman **+0.475** (p=4.5e-07) → 재현✅(|r|>0.3)
- **rate fit_beta rank** (shared 102): Spearman **+0.128** (p=0.2) → 약함/미재현(|r|≤0.3)
- **rate fit_gamma rank** (shared 102): Spearman **+0.187** (p=0.06) → 약함/미재현(|r|≤0.3)

## RNA-only floor 일치도 (sanity, chromatin 무관)

- **floor timing fit_t_ rank** (shared 99): Spearman **+0.002** (p=0.98) → 약함/미재현(|r|≤0.3)

## 판정

- **headline lag 크기 rank Spearman = +0.185** → **재현 약함/미확인** (|r|≤0.3)

## caveat (필수)
- MultiVelo 4-state는 t_sw를 순서대로 정렬(단조) → lag 부호는 **구조적 양수(무정보)**다. 이 비교는 lag *크기*의 gene간 **rank 재현성**만 본다(방향 아님).
- 단일 외부 데이터셋 replication 1건 — 강한 일반화 주장은 하지 않는다.
- 두 데이터셋은 서로 다른 spliced/unspliced 원천 → cross-dataset noise가 rho를 보수적으로 낮춘다. 낮은 rho=lag fragile에 보수적, 높은 rho=강한 신호.
- within-lineage(진짜 timing)가 아닌 *전역* fit의 rank 비교다 — brain lineage annotation과 무관하게 계산되었다.

---

# P3 cross-dataset concordance — HSPC ↔ human_brain

> Does the MultiVelo lag/timing of the BIOP01 HSPC benchmark reproduce (rank) in an external multiome (human_brain)?
> Success criterion (RUNBOOK §7): |Spearman| > 0.3 (single replication).

## Inputs
- HSPC MultiVelo: `multivelo_genes.csv` — 538 genes
- human_brain MultiVelo: `multivelo_genes_human_brain.csv` — 551 genes
- HSPC floor: `rna_only_dynamical_genes.csv` — 487 genes
- human_brain floor: `rna_only_dynamical_genes_human_brain.csv` — 711 genes

## MultiVelo concordance (headline = lag magnitude)

- **lag(fit_t_sw2−fit_t_sw1) magnitude rank ← headline** (shared 102): Spearman **+0.185** (p=0.063) → weak/not reproduced (|r|≤0.3)
- **switch timing fit_t_sw2 rank** (shared 102): Spearman **+0.049** (p=0.63) → weak/not reproduced (|r|≤0.3)
- **rate fit_alpha rank** (shared 102): Spearman **+0.475** (p=4.5e-07) → reproduced ✅ (|r|>0.3)
- **rate fit_beta rank** (shared 102): Spearman **+0.128** (p=0.2) → weak/not reproduced (|r|≤0.3)
- **rate fit_gamma rank** (shared 102): Spearman **+0.187** (p=0.06) → weak/not reproduced (|r|≤0.3)

## RNA-only floor concordance (sanity, chromatin-independent)

- **floor timing fit_t_ rank** (shared 99): Spearman **+0.002** (p=0.98) → weak/not reproduced (|r|≤0.3)

## Verdict

- **headline lag-magnitude rank Spearman = +0.185** → **reproduction weak/unconfirmed** (|r|≤0.3)

## caveat (required)
- MultiVelo's 4-state model orders t_sw monotonically → the lag sign is **structurally positive (uninformative)**. This comparison examines only the gene-to-gene **rank reproducibility** of lag *magnitude* (not direction).
- A single external-dataset replication — no strong generalization claim is made.
- The two datasets have different spliced/unspliced sources → cross-dataset noise conservatively lowers rho. A low rho is conservative toward lag being fragile; a high rho is a strong signal.
- This is a *global* fit rank comparison, not within-lineage (true timing) — computed independently of brain lineage annotation.
