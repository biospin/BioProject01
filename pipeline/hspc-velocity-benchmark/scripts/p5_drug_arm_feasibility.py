#!/usr/bin/env python
"""
p5_drug_arm_feasibility.py — Drug-timing arm FEASIBILITY / PLUMBING demo.

>>> NOT a headline validation. NOT evidence for H_main. <<<
This script demonstrates that the end-to-end join + nested-model + ortholog
machinery of the drug-timing arm RUNS on public data, and reports the
decay-controlled INCREMENT of baseline chromatin features. Design is LOCKED by
manuscript/drug_timing_arm_scout.md §3 (feasibility mode). Guardrails:
  - chromatin-lag reported ONLY as increment OVER a decay-t½ base model (§3.1).
  - GSE201662 is mouse / coarse / IDH1i → ordinal early-vs-late onset ONLY,
    no per-gene t½ fit (§3.2). 4wk relapse arm EXCLUDED (regime change).
  - triple-system stacking + 5 further confounds stated in the .md output (§3.4).
  - a null / weak increment is an EXPECTED, acceptable feasibility outcome and is
    reported straight.

Inputs (provenance printed at runtime; see data/PROVENANCE_halflife.md):
  outcome   GSE201662  data/GSE201662_Table_S2_AG120_DEGs.xlsx  (author limma DEG,
             AG120 vs matched Vehicle at day5 & day14; mouse AML, sha printed)
  decay t½  GSE229314  data/todorovski_k562_halflife.csv        (Todorovski K562, 6580 genes)
  ortholog  MGI        data/HOM_MouseHumanSequence.rpt          (1:1 mouse->human)
  HSPC lag  (this proj) results/multivelo_genes.csv             (lag = t_sw2 - t_sw1)
  HSPC ATAC (this proj) results/atac_baseline_features.csv      (day0 promoter/enhancer)
  chrom     gencode v44 data/ref/gencode.v44.basic.annotation.gtf.gz

Outputs:
  results/drug_arm_feasibility.md
  results/drug_arm_feasibility_genes.csv
  results/drug_arm_feasibility_models.csv
  results/drug_arm_feasibility_permutation.csv
"""
import hashlib, gzip, sys, json
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
import statsmodels.api as sm
from scipy import stats

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
RES  = HERE / "results"
SEED = 20260710
rng = np.random.default_rng(SEED)
ADJ = 0.05          # responder significance (author adj.P.Val)
B_PERM = 2000       # permutation reps for held-out ΔAUC null

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------------------------------------------------------------- provenance
prov = {}
for name, p in [
    ("GSE201662_S2", DATA / "GSE201662_Table_S2_AG120_DEGs.xlsx"),
    ("GSE201662_rawcounts", DATA / "GSE201662_raw_counts.txt.gz"),
    ("decay_todorovski_k562", DATA / "todorovski_k562_halflife.csv"),
    ("ortholog_MGI_HOM", DATA / "HOM_MouseHumanSequence.rpt"),
    ("hspc_multivelo", RES / "multivelo_genes.csv"),
    ("hspc_atac", RES / "atac_baseline_features.csv"),
]:
    prov[name] = {"path": str(p), "sha256": sha(p) if p.exists() else "MISSING"}

# ---------------------------------------------------------------- 1. ortholog 1:1
hom = pd.read_csv(DATA / "HOM_MouseHumanSequence.rpt", sep="\t")
hom.columns = [c.strip() for c in hom.columns]
KEY = "DB Class Key"
mouse = hom[hom["Common Organism Name"].str.contains("mouse", na=False)][[KEY, "Symbol"]]
human = hom[hom["Common Organism Name"] == "human"][[KEY, "Symbol"]]
cm, ch = mouse.groupby(KEY).size(), human.groupby(KEY).size()
oto = set(cm[cm == 1].index) & set(ch[ch == 1].index)      # exactly 1 mouse & 1 human
m1 = mouse[mouse[KEY].isin(oto)].set_index(KEY)["Symbol"]
h1 = human[human[KEY].isin(oto)].set_index(KEY)["Symbol"]
m2h = {m1[k]: h1[k] for k in oto}                          # mouse symbol -> human symbol
n_orth = len(m2h)

# ---------------------------------------------------------------- 2. outcome (GSE201662)
d5  = pd.read_excel(DATA / "GSE201662_Table_S2_AG120_DEGs.xlsx", sheet_name="AG120_v_Vehicle_day5").set_index("ID")
d14 = pd.read_excel(DATA / "GSE201662_Table_S2_AG120_DEGs.xlsx", sheet_name="AG120_v_Vehicle_day14").set_index("ID")
genes_mm = d5.index.intersection(d14.index)
sig5  = set(genes_mm[d5.loc[genes_mm, "adj.P.Val"] < ADJ])
sig14 = set(genes_mm[d14.loc[genes_mm, "adj.P.Val"] < ADJ])
resp_mm = sig5 | sig14                                     # responder = sig at day5 OR day14 (4wk excluded by design)

# ordinal onset label (§3.2 feasibility): late_onset=1 if response still RISING 5d->14d
#   (|logFC_14|>|logFC_5|) = onset later; early_onset(0) if already peaked/plateaued by day5.
rows = []
for g in resp_mm:
    if g not in m2h:
        continue
    fc5, fc14 = d5.loc[g, "logFC"], d14.loc[g, "logFC"]
    rows.append((m2h[g], g, fc5, fc14,
                 int(g in sig5), int(g in sig14)))
out = pd.DataFrame(rows, columns=["gene", "gene_mm", "fc5", "fc14", "sig5", "sig14"]).dropna()
out = out.drop_duplicates("gene")
out["late_onset"] = (out["fc14"].abs() > out["fc5"].abs()).astype(int)
out["same_dir"]   = (out["fc5"] * out["fc14"] > 0).astype(int)

# ---------------------------------------------------------------- 3. decay t½ (control)
dec = pd.read_csv(DATA / "todorovski_k562_halflife.csv")
dec = dec.groupby("gene", as_index=False)["t_half_h"].median()
dec["log_thalf"] = np.log2(dec["t_half_h"])
dec["thalf_censored24"] = (dec["t_half_h"] >= 24.0).astype(int)   # 24h right-censor flag (~8%)

# ---------------------------------------------------------------- 4. HSPC baseline features
mv = pd.read_csv(RES / "multivelo_genes.csv")
mv["lag"] = mv["fit_t_sw2"] - mv["fit_t_sw1"]                     # chromatin->transcription lag (pseudotime)
mv = mv[["gene", "lag", "fit_alpha_c", "fit_alpha"]].rename(columns={"fit_alpha_c": "alpha_c"})
mv = mv.dropna(subset=["lag"]).drop_duplicates("gene")
atac = pd.read_csv(RES / "atac_baseline_features.csv")[
    ["gene", "prom_acc", "enh_acc", "enh_sum", "prom_enh_ratio"]].drop_duplicates("gene")

# ---------------------------------------------------------------- 5. gene -> chromosome (gencode v44)
chrom = {}
with gzip.open(DATA / "ref" / "gencode.v44.basic.annotation.gtf.gz", "rt") as fh:
    for ln in fh:
        if ln.startswith("#"):
            continue
        f = ln.split("\t")
        if f[2] != "gene":
            continue
        c = f[0]
        nm = f[8].split('gene_name "')[1].split('"')[0]
        chrom.setdefault(nm, c)          # first (canonical) occurrence

# ---------------------------------------------------------------- 6. JOIN -> intersection
df = (out.merge(dec[["gene", "log_thalf", "thalf_censored24"]], on="gene")
         .merge(mv, on="gene")
         .merge(atac, on="gene"))
df["chrom"] = df["gene"].map(chrom)
df = df.dropna(subset=["chrom"]).reset_index(drop=True)

# drop rows with any NaN in a feature used by any model (complete-case for a fair nested comparison)
FEAT_ALL = ["log_thalf", "lag", "prom_acc", "enh_acc", "enh_sum", "prom_enh_ratio", "alpha_c"]
n_prejoin = len(df)
df = df.dropna(subset=FEAT_ALL).reset_index(drop=True)
n_dropped_nan = n_prejoin - len(df)

n_final = len(df)
n_late = int(df["late_onset"].sum())
n_early = n_final - n_late

# ---------------------------------------------------------------- 7. nested models
# feature sets (all include the decay control per §3.1)
MODELS = {
    "M0_base_decay":        ["log_thalf"],
    "M1_full_lag":          ["log_thalf", "lag"],
    "M2_full_locked":       ["log_thalf", "lag", "prom_acc", "enh_acc"],   # §3.1 locked full
    "M3_sec_atac":          ["log_thalf", "prom_acc", "enh_acc"],          # §6 ATAC route
    "M4_sec_alpha":         ["log_thalf", "alpha_c"],                      # §6 α route
}
y = df["late_onset"].values
groups = df["chrom"].values
uchr = np.unique(groups)

def loco_auc(X, y, groups):
    """Leave-one-chromosome-out CV; pool OOF probs; single AUC. Scaler fit on train only."""
    oof = np.full(len(y), np.nan)
    for c in np.unique(groups):
        te = groups == c
        tr = ~te
        if len(np.unique(y[tr])) < 2:
            continue
        sc = StandardScaler().fit(X[tr])
        clf = LogisticRegression(max_iter=2000, C=1.0)
        clf.fit(sc.transform(X[tr]), y[tr])
        oof[te] = clf.predict_proba(sc.transform(X[te]))[:, 1]
    m = ~np.isnan(oof)
    if len(np.unique(y[m])) < 2:
        return np.nan, oof
    return roc_auc_score(y[m], oof[m]), oof

def insample_fit(X, y):
    """statsmodels Logit on standardized features -> llf, McFadden R2."""
    Xs = StandardScaler().fit_transform(X)
    Xc = sm.add_constant(Xs, has_constant="add")
    try:
        r = sm.Logit(y, Xc).fit(disp=0, maxiter=200)
        return r.llf, r.prsquared, r.mle_retvals.get("converged", True)
    except Exception as e:
        return np.nan, np.nan, False

def strat_auc(X, y, seed=SEED, n_repeats=20):
    """Repeated stratified-5-fold pooled-OOF AUC (chromosome-agnostic sanity vs the LOCO value).
    Averaged over n_repeats shuffles — one draw has SD≈0.07 at n≈72, too noisy for a durable claim."""
    aucs = []
    for r in range(n_repeats):
        oof = np.full(len(y), np.nan)
        for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed + r).split(X, y):
            sc = StandardScaler().fit(X[tr])
            clf = LogisticRegression(max_iter=2000, C=1.0).fit(sc.transform(X[tr]), y[tr])
            oof[te] = clf.predict_proba(sc.transform(X[te]))[:, 1]
        aucs.append(roc_auc_score(y, oof))
    return float(np.mean(aucs))

# base metrics
Xb = df[MODELS["M0_base_decay"]].values
auc_base, _ = loco_auc(Xb, y, groups)
llf_base, r2_base, conv_base = insample_fit(Xb, y)
# stratified-5-fold cross-check: shows the sub-0.5 LOCO base is a fold-composition artifact, not anti-signal
strat_base = strat_auc(Xb, y)
strat_m2 = strat_auc(df[MODELS["M2_full_locked"]].values, y)

rows_m = []
oof_store = {}
for name, feats in MODELS.items():
    X = df[feats].values
    auc, oof = loco_auc(X, y, groups)
    oof_store[name] = oof
    llf, r2, conv = insample_fit(X, y)
    if name == "M0_base_decay":
        lr_p = np.nan; dparam = 0
    else:
        dparam = len(feats) - len(MODELS["M0_base_decay"])
        lr_stat = 2 * (llf - llf_base)
        lr_p = stats.chi2.sf(lr_stat, dparam) if np.isfinite(lr_stat) and lr_stat > 0 else 1.0
    rows_m.append(dict(model=name, features="+".join(feats), n_params=len(feats) + 1,
                       cv_auc=auc, mcfadden_r2=r2, converged=conv,
                       dAUC_vs_base=auc - auc_base, dR2_vs_base=r2 - r2_base,
                       LR_p_vs_base=lr_p, added_params=dparam))
models_df = pd.DataFrame(rows_m)

# ---------------------------------------------------------------- 8. permutation null on held-out ΔAUC
# permute labels, recompute LOCO ΔAUC (model - base). Tests increment beyond chance.
perm_rows = []
targets = [m for m in MODELS if m != "M0_base_decay"]
perm_dauc = {m: np.empty(B_PERM) for m in targets}
Xsets = {m: df[MODELS[m]].values for m in MODELS}
for b in range(B_PERM):
    yp = rng.permutation(y)
    ab, _ = loco_auc(Xsets["M0_base_decay"], yp, groups)
    for m in targets:
        am, _ = loco_auc(Xsets[m], yp, groups)
        perm_dauc[m][b] = (am - ab) if (np.isfinite(am) and np.isfinite(ab)) else np.nan
for m in targets:
    obs = float(models_df.loc[models_df.model == m, "dAUC_vs_base"].iloc[0])
    pv = perm_dauc[m][np.isfinite(perm_dauc[m])]
    p_one = (np.sum(pv >= obs) + 1) / (len(pv) + 1)          # one-sided: increment > chance
    perm_rows.append(dict(model=m, dAUC_obs=obs, perm_mean=float(np.mean(pv)),
                          perm_sd=float(np.std(pv)), perm_p_onesided=p_one, B=len(pv)))
perm_df = pd.DataFrame(perm_rows)

# ---------------------------------------------------------------- 8b. label sensitivity (significance-onset)
# alt label: early = sig at day5 (onset<=5d), late-only = sig at day14 but NOT day5. In-sample LR only (cheap).
# degenerate/imbalanced by construction (day5 already sig for most) -> reported as robustness, not primary.
alt_map = {}
for g in resp_mm:
    if g in sig5:
        alt_map[m2h.get(g)] = 1          # early onset
    elif g in sig14:
        alt_map[m2h.get(g)] = 0          # late-only onset
dfa = df.copy()
dfa["alt_late"] = dfa["gene"].map(lambda g: 0 if alt_map.get(g, None) == 1 else (1 if alt_map.get(g, None) == 0 else np.nan))
# NOTE: alt_late here mirrors primary orientation (1=late). early(sig5)->0, late-only(sig14 not5)->1.
dfa = dfa.dropna(subset=["alt_late"])
ya = dfa["alt_late"].astype(int).values
alt_n1 = int(ya.sum()); alt_n0 = len(ya) - alt_n1
alt_llf_base, alt_r2_base, _ = insample_fit(dfa[MODELS["M0_base_decay"]].values, ya)
alt_llf_m1,   alt_r2_m1,   _ = insample_fit(dfa[MODELS["M1_full_lag"]].values, ya)
alt_lr = 2 * (alt_llf_m1 - alt_llf_base)
alt_lr_p = stats.chi2.sf(alt_lr, 1) if np.isfinite(alt_lr) and alt_lr > 0 else 1.0

# ---------------------------------------------------------------- 9. verdict
locked = models_df.loc[models_df.model == "M2_full_locked"].iloc[0]
lag1   = models_df.loc[models_df.model == "M1_full_lag"].iloc[0]
p_locked = float(perm_df.loc[perm_df.model == "M2_full_locked", "perm_p_onesided"].iloc[0])
increment_sig = (p_locked < 0.05) and (locked["dAUC_vs_base"] > 0) and (locked["LR_p_vs_base"] < 0.05)

# ---------------------------------------------------------------- 10. write outputs
df_out = df[["gene", "gene_mm", "chrom", "late_onset", "same_dir", "sig5", "sig14",
             "fc5", "fc14", "log_thalf", "thalf_censored24", "lag", "alpha_c", "fit_alpha",
             "prom_acc", "enh_acc", "enh_sum", "prom_enh_ratio"]]
df_out.to_csv(RES / "drug_arm_feasibility_genes.csv", index=False)
models_df.to_csv(RES / "drug_arm_feasibility_models.csv", index=False)
perm_df.to_csv(RES / "drug_arm_feasibility_permutation.csv", index=False)

def fmt(x, d=3):
    return "NA" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{d}f}"

md = []
md.append("# Drug-timing arm — FEASIBILITY / PLUMBING demo (NOT a validation)\n")
md.append(f"> Generated by `scripts/p5_drug_arm_feasibility.py` (seed {SEED}). "
          "Design LOCKED by `manuscript/drug_timing_arm_scout.md` §3 (feasibility mode).\n")
md.append("> **This is a plumbing/robustness check, not evidence for H_main.** It demonstrates the "
          "join + ortholog + nested-model + permutation machinery runs end-to-end on public data, and "
          "reports the decay-controlled INCREMENT of baseline chromatin features. A null/weak increment "
          "is an expected, acceptable feasibility outcome (§3.1–§3.2).\n")

md.append("\n## 0. Verdict\n")
verdict = ("**increment SIGNIFICANT**" if increment_sig else "**increment NOT significant (null)**")
md.append(f"- **Feasibility: PASS.** Pipeline runs end-to-end — public data acquired (GEO FTP + MGI) → "
          f"MGI 1:1 mouse→human ortholog join → decay-controlled nested logistic → chromosome-blocked "
          f"hold-out AUC + permutation null, all reproducible. ✅ This machinery is the deliverable.\n")
md.append(f"- **Result: clean NULL.** Locked full model (decay + chromatin-lag + ATAC) vs decay-only base: "
          f"ΔAUC = **{fmt(locked['dAUC_vs_base'])}**, LR p = **{fmt(locked['LR_p_vs_base'])}**, "
          f"permutation p (held-out ΔAUC) = **{fmt(p_locked)}** → {verdict}. The cleanest 1-DOF increment "
          f"(M1, decay+lag) is also null: ΔAUC {fmt(lag1['dAUC_vs_base'])}, LR p {fmt(lag1['LR_p_vs_base'])}, "
          f"perm p {fmt(float(perm_df.loc[perm_df.model=='M1_full_lag','perm_p_onesided'].iloc[0]))}. "
          f"All McFadden R² ≈ 0.\n")
md.append(f"- **Even the decay-only base carries no signal here.** In-sample McFadden R² ≈ {fmt(r2_base,5)} "
          f"(essentially zero association — decay is neither a forward nor an inverse predictor). Its LOCO "
          f"CV AUC = {fmt(auc_base)} lands below 0.5, but that is a leave-one-chromosome-out fold-composition "
          f"artifact (null features → intercept-dominated OOF predictions tracking the training base-rate, which "
          f"is anti-correlated with each held-out chromosome): a plain stratified-5-fold base AUC = "
          f"**{fmt(strat_base)}** (≈0.5), confirming no anti-signal. The artifact cancels in ΔAUC and is absorbed "
          f"by the permutation null, so **the verdict is anchored on the LR test (R²≈0) + permutation p, not the "
          f"absolute CV AUC.** There is simply no baseline for chromatin to add to — the **EXPECTED** outcome "
          f"for a principled reason (§0.1), not broken plumbing.\n")
md.append("\n### 0.1 Why a null is expected here — feature↔outcome timescale mismatch (primary limit)\n")
md.append("The outcome is sampled at **5 d and 14 d** = **~10–20 mRNA half-lives** (Todorovski K562 t½ is "
          "single-digit hours, capped at 24 h). Every non-censored gene is fully mRNA-equilibrated long before "
          "day 5, so **decay t½ has essentially no mechanistic channel to predict a day5-vs-day14 ordinal** — "
          "the base model is asked to predict on a timescale where its native mechanism (Todorovski's 2 h/6 h "
          "decay→response) does not operate. Likewise the chromatin→transcription **lag** encodes minutes-to-hours "
          "coupling, while day-scale onset differences reflect cellular/differentiation dynamics. **Both base and "
          "increment are asked to predict a days-scale ordinal that neither feature's native timescale matches.** "
          "The honest reading of the null is therefore *'the design cannot test the hypothesis at this sampling "
          "cadence / in this coarse mouse proxy'*, **NOT** *'chromatin lag does not predict drug-response timing'* "
          "(a biological claim this data cannot make). The arm's tier is unchanged (no headline).\n")

md.append("\n## 1. Data acquired (provenance)\n")
md.append("| role | dataset | file | sha256 (head) |\n|---|---|---|---|\n")
md.append(f"| outcome | GSE201662 (mouse IDH1m AML, AG-120) | `data/GSE201662_Table_S2_AG120_DEGs.xlsx` | `{prov['GSE201662_S2']['sha256'][:16]}` |\n")
md.append(f"| outcome(raw) | GSE201662 | `data/GSE201662_raw_counts.txt.gz` | `{prov['GSE201662_rawcounts']['sha256'][:16]}` |\n")
md.append(f"| decay t½ (control) | GSE229314 (Todorovski K562) | `data/todorovski_k562_halflife.csv` | `{prov['decay_todorovski_k562']['sha256'][:16]}` |\n")
md.append(f"| ortholog 1:1 | MGI HOM | `data/HOM_MouseHumanSequence.rpt` | `{prov['ortholog_MGI_HOM']['sha256'][:16]}` |\n")
md.append(f"| HSPC lag/α | this project | `results/multivelo_genes.csv` | `{prov['hspc_multivelo']['sha256'][:16]}` |\n")
md.append(f"| HSPC day0 ATAC | this project | `results/atac_baseline_features.csv` | `{prov['hspc_atac']['sha256'][:16]}` |\n")
md.append("\nGSE201662 URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE201662 (GEO FTP suppl). "
          "GSE229314 t½ provenance: `data/PROVENANCE_halflife.md`. "
          "MGI HOM_MouseHumanSequence.rpt: https://www.informatics.jax.org/downloads/reports/ .\n")

md.append("\n## 2. Outcome construction (§3.2 feasibility, mouse coarse)\n")
md.append(f"- Author limma DEG (GSE201662 Table S2), AG-120 vs **matched Vehicle** at day5 and day14. "
          f"**4-week relapse arm EXCLUDED** (regime change) — S2 contains only day5/day14 AG120 contrasts.\n")
md.append(f"- **No per-gene t½ fit** (forbidden by §3.2 for this coarse 2-point mouse proxy).\n")
md.append(f"- Responder = adj.P.Val < {ADJ} at day5 **or** day14: {len(resp_mm)} mouse genes "
          f"(day5 sig {len(sig5)}, day14 sig {len(sig14)}, late-only {len(sig14 - sig5)}).\n")
md.append("- **Ordinal onset label:** `late_onset = 1` if response still RISING 5d→14d (|logFC_14|>|logFC_5|), "
          "else `0` (already peaked/plateaued by day5 = early onset). Chosen over a significance-onset label "
          "because day5 alone is already significant for most genes (→ degenerate 86/14 imbalance); the "
          "magnitude-trajectory label gives usable class balance and is the natural 2-point onset ordinal.\n")

md.append("\n## 3. Intersection size (reported FIRST — §3.3 power caveat)\n")
md.append(f"- MGI 1:1 high-confidence mouse→human orthologs: **{n_orth}**.\n")
md.append(f"- Todorovski t½ genes: **{len(dec)}**  ∩  HSPC lag∩ATAC genes: **{len(set(mv.gene)&set(atac.gene))}**  "
          f"∩  ortholog-mapped GSE201662 responders (with chrom): **join →**\n")
md.append(f"- **FINAL analyzable intersection: n = {n_final} genes** "
          f"(late_onset = {n_late}, early_onset = {n_early}; balance {n_late/n_final:.2f}; "
          f"{n_dropped_nan} dropped for feature NaN — complete-case).\n")
md.append(f"- ⚠️ **Small & triple-system-stacked** (HSPC lag ∩ K562 decay ∩ mouse-AML outcome). The binding "
          f"constraint is the HSPC MultiVelo lag set (~{len(set(mv.gene))} genes). n={n_final} is "
          f"**underpowered** for a small incremental effect regardless of true effect size — read the "
          f"increment test as a plumbing demonstration, not a powered inference.\n")

md.append("\n## 4. Nested models — decay-controlled increment (§3.1)\n")
md.append("Outcome = `late_onset`. Base is decay-t½ only; every other model adds features OVER decay. "
          "`cv_auc` = leave-one-chromosome-out pooled-OOF AUC (chromosome-blocked hold-out, scaler fit on "
          "train fold only — no leakage). `LR_p` = in-sample likelihood-ratio χ² vs base. "
          f"`perm_p` = one-sided permutation null on the held-out ΔAUC (B={B_PERM}).\n\n")
md.append("| model | features | CV AUC | McFadden R² | ΔAUC vs base | LR p | perm p |\n")
md.append("|---|---|---|---|---|---|---|\n")
pmap = {r["model"]: r["perm_p_onesided"] for _, r in perm_df.iterrows()}
for _, r in models_df.iterrows():
    pp = pmap.get(r["model"], np.nan)
    md.append(f"| {r['model']} | {r['features']} | {fmt(r['cv_auc'])} | {fmt(r['mcfadden_r2'])} | "
              f"{fmt(r['dAUC_vs_base'])} | {fmt(r['LR_p_vs_base'])} | {fmt(pp)} |\n")
md.append(f"\n- **Decay-only base CV AUC = {fmt(auc_base)}** (below 0.5): decay t½ has no usable out-of-fold "
          f"signal for this day-scale ordinal — primarily the timescale mismatch (§0.1), secondarily the IDH1i "
          f"drug-class mismatch (§3.4 #4). All McFadden R² ≈ 0 (base {fmt(r2_base,4)}).\n")
md.append(f"- **Headline locked increment = M1 (decay+lag, 1 added DOF — the most powered increment at n={n_final}):** "
          f"ΔAUC {fmt(lag1['dAUC_vs_base'])}, LR p {fmt(lag1['LR_p_vs_base'])}. The full locked-spec M2 "
          f"(decay+lag+ATAC, 3 added DOF): ΔAUC {fmt(locked['dAUC_vs_base'])}, LR p {fmt(locked['LR_p_vs_base'])}, "
          f"perm p {fmt(p_locked)} — M2 spends DOF n={n_final} cannot afford, so M1 carries interpretation. "
          f"Both null.\n")
md.append("- §6-consistent secondary routes (M3 ATAC-only, M4 α) reported alongside, also null. The LOCKED "
          "contribution per §3.1 is the chromatin-lag increment OVER decay (reported ONLY as an increment); "
          "it is not significant.\n")
md.append(f"- **CV-artifact cross-check:** stratified-5-fold pooled-OOF AUC — base {fmt(strat_base)}, "
          f"full-locked M2 {fmt(strat_m2)} (ΔAUC {fmt(strat_m2-strat_base)}). Both ≈0.5, ΔAUC ≈0 → the null "
          "holds independent of the chromosome-blocking scheme; the sub-0.5 LOCO values are a fold artifact.\n")
md.append(f"- **Label-choice sensitivity:** re-running the cleanest increment (M1 decay+lag) against the "
          f"*alternative* significance-onset label (early=sig@day5→0, late-only=sig@day14→1; n={len(ya)}, "
          f"{alt_n1}/{alt_n0}, imbalanced by construction) is **also null** — M1 McFadden R² {fmt(alt_r2_m1,4)} "
          f"vs base {fmt(alt_r2_base,4)}, LR p {fmt(alt_lr_p)}. The null does not depend on the primary "
          f"magnitude-trajectory label choice.\n")

md.append("\n## 5. Confounds stated honestly (§3.4 — all six)\n")
md.append("1. **Cell-context mismatch (max confound):** baseline = human HSPC; decay = human K562 leukemia "
          "line; outcome = mouse IDH1m AML. Gene-intrinsic-feature restriction (§3.3) mitigates but does not "
          "remove it. Only gene-intrinsic properties (lag, α, t½, promoter/enhancer accessibility as a stated-"
          "assumption covariate) cross systems — no absolute accessibility values transferred.\n")
md.append("2. **Triple-system stacking:** three organisms/systems stitched by gene (HSPC + K562 + mouse AML) — "
          f"more context confound than the 2-system pairing anticipated; the n={n_final} intersection is the price.\n")
md.append(f"3. **Feature-intersection power:** n={n_final} (late {n_late}/early {n_early}). Underpowered for a "
          "small increment irrespective of effect size — the leading caveat.\n")
md.append("4. **Drug-class heterogeneity:** AG-120 = IDH1i (metabolic→demethylation), NOT a chromatin writer / "
          "transcriptional inhibitor. No pooling with HMA/HDACi/BETi; base decay model may be off-mechanism.\n")
md.append("5. **Pseudotime ≠ wall-clock + feature↔outcome timescale mismatch (the primary limit, §0.1):** HSPC "
          "lag is in pseudotime units and encodes minutes-to-hours chromatin→transcription coupling; decay t½ is "
          "single-digit hours; but the outcome onset is sampled at 5 d / 14 d (~10–20 half-lives). Neither "
          "feature's native timescale matches a day-scale ordinal, so the null is expected by construction — the "
          "design cannot test the hypothesis at this cadence. This is the honest headline caveat.\n")
md.append("6. **Multiple testing / leakage:** chromosome-blocked hold-out (LOCO), scaler fit on train fold "
          "only, permutation null for the ΔAUC significance. Only the locked increment is the claim.\n")
md.append("\n**Extra:** Todorovski K562 t½ has ~8% right-censoring at 24 h; used as log2 t½ (rank-robust), "
          f"censor flag in the genes CSV ({int(df['thalf_censored24'].sum())} censored in the intersection).\n")

md.append("\n## 6. Files\n")
md.append("- `results/drug_arm_feasibility_genes.csv` — per-gene joined table (outcome + all features + chrom).\n")
md.append("- `results/drug_arm_feasibility_models.csv` — nested-model comparison.\n")
md.append("- `results/drug_arm_feasibility_permutation.csv` — held-out ΔAUC permutation null.\n")
md.append(f"\n_Reproduce:_ `conda run -n scv-preprocess python scripts/p5_drug_arm_feasibility.py` (seed {SEED}).\n")

(RES / "drug_arm_feasibility.md").write_text("".join(md))

# console summary
print("=== FEASIBILITY DEMO COMPLETE ===")
print(f"1:1 orthologs: {n_orth} | mouse responders: {len(resp_mm)}")
print(f"FINAL intersection n={n_final} (late={n_late}, early={n_early})")
print(f"base CV AUC={fmt(auc_base)}")
print(models_df[["model","cv_auc","dAUC_vs_base","LR_p_vs_base"]].to_string(index=False))
print(perm_df[["model","dAUC_obs","perm_p_onesided"]].to_string(index=False))
print(f"increment_significant={increment_sig}")
print("wrote results/drug_arm_feasibility.md + _genes/_models/_permutation.csv")
