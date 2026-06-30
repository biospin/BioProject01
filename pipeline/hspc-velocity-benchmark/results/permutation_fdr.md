# P4 — Permutation FDR (DESIGN §5.5)

- N_perm=10000, seed=20260701, FDR q<0.1 (BH).
- sign-가변 method: ['moflow', 'crakvelo', 'multivelovae']
> §85 권고대로 permutation 기반(공조절 gene 비독립). 범위·null 정의는 스크립트 docstring 참조.

## A. Cross-method lag concordance 유의성 (gene-label shuffle null)

| pair | n | Spearman ρ | p(param) | p(perm) | q(BH) | 유의(q<0.10) |
|---|---|---|---|---|---|---|
| moflow×crakvelo | 330 | -0.151 | 0.006 | 0.0057 | 0.017 | ✅ |
| moflow×multivelovae | 636 | +0.083 | 0.036 | 0.0338 | 0.051 | ✅ |
| crakvelo×multivelovae | 334 | -0.040 | 0.471 | 0.4713 | 0.471 | — |

→ 2/3 쌍이 gene-label shuffle null 대비 유의. **유의해도 |ρ|가 작으면 effect는 약함**(통계적 유의 ≠ 강한 일치).

## B. Per-gene cross-method sign-consistency agreement-set (§4C 2차)

- 검정 gene(≥2 method 관측) = 598, **FDR<0.1 agreement-set = 0 gene**.
- consistency = |mean(sign)| (1=전 method 동부호, 0=반반). null = 부호 무작위 ±.

> ⚠️ **agreement-set 비어 있음** — 어떤 gene도 method 간 부호가 무작위 이상으로 일관되지 않음. = lag 방향은 method-민감(H1 강화). 대부분 gene이 2 method에만 관측되어 검정력도 제한적.

---
### 해석 (DESIGN §4 reframe)
- 이 벤치마크는 *accuracy*가 아니라 *reproducibility/consistency*를 측정(ground truth 없음).
- A·B가 유의하지 않거나 effect가 작으면 → **lag 방향/순위는 method 선택에 민감**, 강건한 건 construct-validity marker(§2)뿐 — H1 핵심 결론과 정합.
- ⚠️ 미수행(범위 밖): lineage 내 pseudotime-shuffle per-gene lag-크기 FDR(재-fit 필요), marker enrichment hypergeometric(§4C 2차, regulator 리스트 확정 후).
