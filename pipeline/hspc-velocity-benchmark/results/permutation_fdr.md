# P4 — Permutation FDR (DESIGN §5.5)

- N_perm=10000, seed=20260701, FDR q<0.1 (BH).
- 부호 가변 method: ['moflow', 'crakvelo', 'multivelovae']
> §85 권고대로 permutation을 기반으로 한다(공조절 gene은 서로 독립이 아니다). 범위와 null 정의는 스크립트 docstring을 참조한다.

## A. Cross-method lag concordance 유의성 (gene-label shuffle null)

| pair | n | Spearman ρ | p(param) | p(perm) | q(BH) | 유의(q<0.10) |
|---|---|---|---|---|---|---|
| moflow×crakvelo | 330 | -0.151 | 0.006 | 0.0057 | 0.017 | ✅ |
| moflow×multivelovae | 636 | +0.083 | 0.036 | 0.0338 | 0.051 | ✅ |
| crakvelo×multivelovae | 334 | -0.040 | 0.471 | 0.4713 | 0.471 | — |

→ 2/3 쌍이 gene-label shuffle null 대비 유의하다. **유의해도 |ρ|가 작으면 effect는 약하다**(통계적 유의 ≠ 강한 일치).

## B. Per-gene cross-method sign-consistency agreement-set (§4C 2차)

- 검정 gene(≥2 method 관측) = 598, **FDR<0.1 agreement-set = 0 gene**.
- consistency = |mean(sign)| (1=전 method 동부호, 0=반반). null = 부호 무작위 ±.

> ⚠️ **agreement-set가 비어 있다** — 어떤 gene도 method 간 부호가 무작위 이상으로 일관되지 않는다. 즉 lag 방향은 method에 민감하다(H1 강화). 대부분의 gene이 2개 method에서만 관측되어 검정력도 제한적이다.

---
### 해석 (DESIGN §4 reframe)
- 이 벤치마크는 *accuracy*가 아니라 *reproducibility/consistency*를 측정한다(ground truth가 없다).
- A·B가 유의하지 않거나 effect가 작으면 → **lag 방향과 순위는 method 선택에 민감하고**, 강건한 것은 construct-validity marker(§2)뿐이며 — H1 핵심 결론과 정합한다.
- ⚠️ 미수행(범위 밖): lineage 내 pseudotime-shuffle per-gene lag-크기 FDR(재-fit 필요), marker enrichment hypergeometric(§4C 2차, regulator 리스트 확정 후).

---

# P4 — Permutation FDR (DESIGN §5.5)

- N_perm=10000, seed=20260701, FDR q<0.1 (BH).
- sign-variable methods: ['moflow', 'crakvelo', 'multivelovae']
> As recommended in §85, this is permutation-based (co-regulated genes are not independent). See the script docstring for scope and null definition.

## A. Cross-method lag concordance significance (gene-label shuffle null)

| pair | n | Spearman ρ | p(param) | p(perm) | q(BH) | significant (q<0.10) |
|---|---|---|---|---|---|---|
| moflow×crakvelo | 330 | -0.151 | 0.006 | 0.0057 | 0.017 | ✅ |
| moflow×multivelovae | 636 | +0.083 | 0.036 | 0.0338 | 0.051 | ✅ |
| crakvelo×multivelovae | 334 | -0.040 | 0.471 | 0.4713 | 0.471 | — |

→ 2/3 pairs are significant against the gene-label shuffle null. **Even when significant, a small |ρ| means the effect is weak** (statistical significance ≠ strong agreement).

## B. Per-gene cross-method sign-consistency agreement-set (§4C secondary)

- Tested genes (observed in ≥2 methods) = 598, **FDR<0.1 agreement-set = 0 genes**.
- consistency = |mean(sign)| (1 = same sign across all methods, 0 = split). null = random sign ±.

> ⚠️ **the agreement-set is empty** — no gene has cross-method sign consistency above random. That is, lag direction is method-sensitive (reinforcing H1). Most genes are observed in only 2 methods, so power is also limited.

---
### Interpretation (DESIGN §4 reframe)
- This benchmark measures *reproducibility/consistency*, not *accuracy* (no ground truth).
- If A·B are non-significant or the effect is small → **lag direction and rank are sensitive to method choice**, and what is robust is only the construct-validity markers (§2) — consistent with the core H1 conclusion.
- ⚠️ Not done (out of scope): within-lineage pseudotime-shuffle per-gene lag-magnitude FDR (requires re-fit), marker-enrichment hypergeometric (§4C secondary, after the regulator list is finalized).
