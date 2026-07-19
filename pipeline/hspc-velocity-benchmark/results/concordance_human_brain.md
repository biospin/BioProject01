# P3 cross-dataset concordance — HSPC ↔ human_brain

> BIOP01 HSPC 벤치마크의 MultiVelo lag/timing이 외부 multiome(human_brain)에서 rank 재현되나.
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

- **headline lag-크기 rank Spearman = +0.185** → **재현 약함/미확인** (|r|≤0.3)

## caveat (필수)
- MultiVelo 4-state는 t_sw 단조 정렬 → lag sign은 **구조적 양수(무정보)**. 이 비교는 lag *크기*의 gene간 **rank 재현성**만 본다(방향 아님).
- 단일 외부 데이터셋 replication 1건 — 강한 일반화 주장 금지.
- 두 데이터셋은 서로 다른 spliced/unspliced 원천 → cross-dataset noise가 rho를 보수적으로 낮춤. 낮은 rho=lag fragile에 보수적, 높은 rho=강한 신호.
- within-lineage(진짜 timing)가 아닌 *전역* fit rank 비교 — brain lineage annotation 무관하게 계산됨.
