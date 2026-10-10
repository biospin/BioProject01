# Post-review robustness checks (machine output, do not edit)

> B=10,000, seed=20261010, percentile 95% CIs. Existing fits only.

## Contract: headline numbers reproduce

| analysis | metric | n | point | 95% CI |
|---|---|---|---|---|
| contract_MVxVAE | rho_alpha | 538 | +0.882 | [+0.856, +0.904] |
| contract_MVxVAE | rho_lag_native_mag | 538 | +0.163 | [+0.077, +0.246] |

## R1 Harmonized: MultiVelo × MultiVeloVAE, one gene set, every convention

> n=538 genes common to both methods. Δρ = ρ_α − ρ_output on the same bootstrap draw.

| analysis | metric | n | point | 95% CI |
|---|---|---|---|---|
| R1_alpha_c | rho | 538 | +0.291 | [+0.208, +0.369] |
| R1_alpha_c | delta_rho_alpha_minus | 538 | +0.591 | [+0.510, +0.676] |
| R1_lag_native_mag | rho | 538 | +0.163 | [+0.078, +0.247] |
| R1_lag_native_mag | delta_rho_alpha_minus | 538 | +0.720 | [+0.636, +0.802] |
| R1_lag_rateproxy_signed | rho | 538 | +0.124 | [+0.038, +0.208] |
| R1_lag_rateproxy_signed | delta_rho_alpha_minus | 538 | +0.758 | [+0.670, +0.847] |
| R1_lag_rateproxy_mag | rho | 538 | -0.009 | [-0.095, +0.080] |
| R1_lag_rateproxy_mag | delta_rho_alpha_minus | 538 | +0.891 | [+0.801, +0.978] |

### Three-method common gene set (n=537)

| analysis | metric | n | point | 95% CI |
|---|---|---|---|---|
| R1c_MVxVAE_mag | rho | 537 | +0.165 | [+0.080, +0.248] |
| R1c_MVxVAE_mag | delta_rho_alpha_minus | 537 | +0.717 | [+0.635, +0.799] |
| R1c_MVxMoFlow_mag | rho | 537 | -0.013 | [-0.097, +0.070] |
| R1c_MVxMoFlow_mag | delta_rho_alpha_minus | 537 | +0.896 | [+0.807, +0.984] |
| R1c_VAExMoFlow_mag | rho | 537 | -0.064 | [-0.148, +0.023] |
| R1c_VAExMoFlow_mag | delta_rho_alpha_minus | 537 | +0.946 | [+0.855, +1.031] |
| R1c_VAExMoFlow_signed | rho | 537 | +0.107 | [+0.022, +0.188] |
| R1c_VAExMoFlow_signed | delta_rho_alpha_minus | 537 | +0.776 | [+0.692, +0.861] |
| R1c_alpha_MVxVAE | rho | 537 | +0.882 | [+0.854, +0.905] |

## R2 Abundance-residualized cross-method concordance (MV × VAE)

> Partial Spearman given HSPC mean Ms expression, n=538.

| analysis | metric | n | point | 95% CI |
|---|---|---|---|---|
| R2_alpha | rho_raw | 538 | +0.882 | [+0.855, +0.904] |
| R2_alpha | rho_partial_abundance | 538 | +0.715 | [+0.659, +0.765] |
| R2_alpha_c | rho_raw | 538 | +0.291 | [+0.208, +0.372] |
| R2_alpha_c | rho_partial_abundance | 538 | +0.264 | [+0.184, +0.344] |
| R2_lag_native_mag | rho_raw | 538 | +0.163 | [+0.079, +0.244] |
| R2_lag_native_mag | rho_partial_abundance | 538 | +0.182 | [+0.098, +0.265] |
| R2_alpha_MV_vs_abundance | rho | 538 | +0.795 | [+0.755, +0.829] |
| R2_alpha_VAE_vs_abundance | rho | 538 | +0.747 | [+0.699, +0.787] |
| R2_partial | delta_rho_alpha_minus_lag | 538 | +0.533 | [+0.441, +0.623] |

## R3 Dependence-aware bootstrap of Δρ = ρ_α − ρ_lag (MV × VAE, native magnitude)

> Genes resampled as whole co-expression modules (average-linkage clusters of the Ms
> gene-gene correlation). K = number of modules; iid = independent genes.

| analysis | metric | n | point | 95% CI |
|---|---|---|---|---|
| R3_iid | delta_rho | 538 | +0.720 | [+0.635, +0.800] |
| R3_modules_K10(largest=212) | delta_rho | 538 | +0.720 | [+0.582, +0.794] |
| R3_modules_K10(largest=212) | rho_lag | 538 | +0.163 | [+0.112, +0.194] |
| R3_modules_K20(largest=198) | delta_rho | 538 | +0.720 | [+0.600, +0.801] |
| R3_modules_K20(largest=198) | rho_lag | 538 | +0.163 | [+0.091, +0.204] |
| R3_modules_K50(largest=187) | delta_rho | 538 | +0.720 | [+0.611, +0.792] |
| R3_modules_K50(largest=187) | rho_lag | 538 | +0.163 | [+0.108, +0.240] |
| R3_modules_K100(largest=156) | delta_rho | 538 | +0.720 | [+0.612, +0.794] |
| R3_modules_K100(largest=156) | rho_lag | 538 | +0.163 | [+0.106, +0.250] |

## R4 Curvature coordinates (fixed-nuisance profile, interior genes)

> n=258. Both curvatures are −d²LL/d(ln θ)² per cell, invariant to a change of units.
> Sensitivity: lag re-expressed as a fraction of the pseudotime horizon (lag/20).

| coordinates | median κ_α/κ_lag | IQR | α stiffer (%) |
|---|---|---|---|
| ln α vs ln lag (as submitted) | 3.53 | [1.92, 7.41] | 94.6 |
| ln α vs lag/horizon | 0.10 | [0.03, 0.22] | 1.9 |

lag0 among these genes: median 3.50, range [0.20, 11.22] pseudotime units
lag class counts: {'interior': 302, 'boundary_pinned': 205, 'degenerate': 31}
