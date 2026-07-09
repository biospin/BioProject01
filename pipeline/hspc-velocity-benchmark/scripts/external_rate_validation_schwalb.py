#!/usr/bin/env python
"""External construct-validation of fitted alpha — SECOND independent TT-seq source.

Adds a second, independent external synthesis-rate reference to Part B of
`external_rate_validation_partB.py`, to remove the "n=1 external source" fragility.

PRIMARY source (existing, _partB): GSE229305 (Todorovski 2024, NAR Cancer) K562 TT-seq
  production rates, per-gene `synth_rate`, gene_symbol supplied directly.
SECOND source (this script): GSE75792 (Schwalb et al. 2016, Science 352:1225 "TT-seq maps
  the human transient transcriptome") K562 wild-type TT-seq. Independent lab / protocol /
  quantification. Both cell lines are K562 -> this is an independent-replication of the SAME
  cell type (a STRENGTH), not a cross-cell-line comparison.

DATA FORM (honest note): GSE75792 does NOT ship per-gene synthesis rates. Its supplementary
  `GSE75792_transcript.annotation.gtf.gz` gives per-Transcriptional-Unit (TU) synthesis + decay
  rates as genomic intervals (hg19, source "Schwalb_2015") with a biotype and a GENCODE-overlap
  flag, but NO gene symbols. Per-gene rates therefore require a coordinate join. We restrict to
  the 7810 protein_coding TUs with GENCODE=="TRUE" and numeric synth_rate, and assign each TU to
  its maximal-overlap GENCODE v19 (hg19) protein_coding gene on the same strand (reciprocal-
  overlap gate >=0.5). Multiple TUs -> one gene: median (matches _partB dup handling).

MAPPING QC (discriminator — a broken build/join and a true null look identical, so we test the
  join against a quantity we already trust):
  QC1  Schwalb synth  vs Todorovski (GSE229305) K562 synth  -> expect POSITIVE (both = synthesis)
  QC2  Schwalb decay  vs Todorovski K562 half-life           -> expect NEGATIVE (decay = ln2/t1/2)
  QC1 positive => the coordinate join places rates on the right genes. (QC2 is a secondary check;
  Schwalb decay is a derived/noisier TT-seq quantity.)

Rank-based (Spearman); paired-gene percentile bootstrap 95% CI (B=10000). HK vs non-HK stratified;
headline non-HK. Same pre-registered ASYMMETRIC interpretation as Part B: positive rho corroborates
alpha as a synthesis-rate proxy; a null does NOT refute alpha (cross-context K562!=HSPC + absolute
alpha non-identifiable + this source is noisy: older TU-level quant, coordinate join, small overlap n).
"""
import re, gzip, json
import numpy as np, pandas as pd
from scipy import stats
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"; DATA = ROOT / "data"
RNG = np.random.default_rng(20260710); B = 10000
FRAC_GATE = 0.5  # reciprocal-overlap gate for a confident TU<->gene 1:1 assignment

SCHWALB_GTF = DATA / "GSE75792_transcript.annotation.gtf.gz"   # GSE75792 suppl (Schwalb 2016)
GENCODE_V19 = DATA / "gencode.v19.genes.gtf.gz"                # hg19 gene-level (GENCODE v19)
PRIMARY_SYNTH = DATA / "k562_ttseq_synthrate.csv"             # GSE229305 (Todorovski) for QC1
PRIMARY_HALFLIFE = DATA / "todorovski_k562_halflife.csv"       # GSE229314 S10 K562_UT for QC2

METHODS = {
    "rna_only":     (RES / "rna_only_dynamical_genes.csv", "fit_alpha"),
    "multivelo":    (RES / "multivelo_genes.csv",          "fit_alpha"),
    "multivelovae": (RES / "multivelovae_genes.csv",       "vae_alpha"),
}
HK = set(l.strip() for l in (DATA / "housekeeping.txt").read_text().splitlines() if l.strip())


def parse_schwalb_tus(path):
    """protein_coding TUs w/ GENCODE=TRUE and numeric synth; keep decay for QC2."""
    rows = []
    with gzip.open(path, "rt") as fh:
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            if len(f) < 9 or f[2] != "protein_coding":
                continue
            m = re.search(r'synthesis rate "([^"]+)"', f[8])
            d = re.search(r'decay rate "([^"]+)"', f[8])
            g = re.search(r'GENCODE "([^"]+)"', f[8])
            if not m or m.group(1) == "NA":
                continue
            if not g or g.group(1) != "TRUE":
                continue
            decay = float(d.group(1)) if d and d.group(1) != "NA" else np.nan
            rows.append((f[0], int(f[3]), int(f[4]), f[6], float(m.group(1)), decay))
    return pd.DataFrame(rows, columns=["chr", "start", "end", "strand", "synth", "decay"])


def parse_gencode_genes(path):
    """hg19 GENCODE v19 protein_coding gene-level intervals w/ symbol."""
    rows = []
    with gzip.open(path, "rt") as fh:
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            gt = re.search(r'gene_type "([^"]+)"', f[8])
            gn = re.search(r'gene_name "([^"]+)"', f[8])
            if gt and gt.group(1) == "protein_coding" and gn:
                rows.append((f[0], int(f[3]), int(f[4]), f[6], gn.group(1)))
    return pd.DataFrame(rows, columns=["chr", "start", "end", "strand", "gene"])


def map_tus_to_genes(tu, gc, frac_gate):
    """Assign each TU to its max-overlap same-strand protein_coding gene; reciprocal-overlap gate."""
    assign = []
    for (c, st), tug in tu.groupby(["chr", "strand"]):
        gcs = gc[(gc.chr == c) & (gc.strand == st)]
        if gcs.empty:
            continue
        gs = gcs.start.values; ge = gcs.end.values; gn = gcs.gene.values
        glen = (ge - gs).astype(float)
        for _, r in tug.iterrows():
            ov = np.maximum(np.minimum(r.end, ge) - np.maximum(r.start, gs), 0)
            if ov.max() <= 0:
                continue
            j = int(np.argmax(ov))
            frac = ov[j] / min(float(r.end - r.start), glen[j])  # reciprocal overlap fraction
            assign.append((gn[j], r.synth, r.decay, frac))
    mp = pd.DataFrame(assign, columns=["gene", "synth", "decay", "frac"])
    mp = mp[mp.frac >= frac_gate]
    return mp


def boot_ci_rho(x, y, b=B):
    n = len(x); rho0 = stats.spearmanr(x, y).statistic
    rhos = np.empty(b); idx = np.arange(n)
    for i in range(b):
        s = RNG.choice(idx, n, replace=True)
        rhos[i] = stats.spearmanr(x[s], y[s]).statistic
    lo, hi = np.nanpercentile(rhos, [2.5, 97.5])
    return float(rho0), float(lo), float(hi)


def run(alpha, synth, subset=None, tag=""):
    common = alpha.index.intersection(synth.index)
    if subset is not None:
        common = common.intersection(subset)
    if len(common) < 5:
        return dict(tag=tag, n=int(len(common)), rho_alpha_synth=None,
                    ci=[None, None], p=None, validates=False)
    a = alpha.loc[common].values.astype(float)
    s = synth.loc[common].values.astype(float)
    rho, lo, hi = boot_ci_rho(a, s)
    p = stats.spearmanr(a, s).pvalue
    return dict(tag=tag, n=int(len(common)), rho_alpha_synth=round(rho, 3),
                ci=[round(lo, 3), round(hi, 3)], p=float(p), validates=bool(lo > 0))


# ---------------- build per-gene Schwalb K562 synthesis rate ----------------
tu = parse_schwalb_tus(SCHWALB_GTF)
gc = parse_gencode_genes(GENCODE_V19)
mp = map_tus_to_genes(tu, gc, FRAC_GATE)
schw_synth = mp.groupby("gene")["synth"].median()
schw_decay = mp.groupby("gene")["decay"].median()

# persist the per-gene synth table (provenance/reuse)
schw_synth.rename("synth_rate").to_csv(DATA / "k562_schwalb_ttseq_synthrate.csv")

mapping_stats = dict(
    schwalb_protein_coding_TUs_numeric_GENCODEtrue=int(len(tu)),
    gencode_v19_protein_coding_genes=int(len(gc)),
    TUs_assigned_frac_gate=int(len(mp)),
    frac_gate=FRAC_GATE,
    median_overlap_frac=round(float(mp.frac.median()), 3),
    unique_genes_mapped=int(schw_synth.shape[0]),
)

# ---------------- mapping QC (discriminator) ----------------
tod_synth = pd.read_csv(PRIMARY_SYNTH).set_index("gene")["synth_rate"]
tod_synth = tod_synth[tod_synth > 0].groupby(level=0).median()
c1 = schw_synth.index.intersection(tod_synth.index)
qc1 = stats.spearmanr(schw_synth.loc[c1], tod_synth.loc[c1])

# QC2: Schwalb decay vs measured half-life across ALL available panels (expect NEGATIVE).
# If null against every panel -> Schwalb decay is globally unreliable (only synth is usable).
dvalid = schw_decay.dropna()
HL_PANELS = {
    "todorovski_K562": PRIMARY_HALFLIFE,
    "rnadecaycafe_K562": DATA / "halflife_rnadecaycafe_k562.csv",
    "molm13": DATA / "halflife_molm13.csv",
    "thp1": DATA / "halflife_thp1.csv",
}
qc2 = {}
for pname, ppath in HL_PANELS.items():
    if not ppath.exists():
        continue
    hl = pd.read_csv(ppath).set_index("gene")["t_half_h"]
    hl = hl[hl > 0].groupby(level=0).median()
    cc = dvalid.index.intersection(hl.index)
    rr = stats.spearmanr(dvalid.loc[cc], hl.loc[cc])
    qc2[pname] = dict(n=int(len(cc)), rho=round(float(rr.statistic), 3), p=float(rr.pvalue))

qc = dict(
    QC1_schwalb_vs_todorovski_synth=dict(n=int(len(c1)), rho=round(float(qc1.statistic), 3),
                                         p=float(qc1.pvalue), expect="POSITIVE", note="validates coordinate join"),
    QC2_schwalb_decay_vs_measured_thalf=dict(expect="NEGATIVE",
                                             note="Schwalb decay = derived/noisier TT-seq quantity; only synth used",
                                             panels=qc2),
)

# ---------------- main: fitted alpha vs Schwalb synth ----------------
results = {"mapping": mapping_stats, "qc": qc, "methods": {}}
rows = []
for mname, (mpath, mcol) in METHODS.items():
    df = pd.read_csv(mpath)
    alpha = df.set_index("gene")[mcol].dropna()
    alpha = alpha[alpha > 0]
    alpha = alpha[~alpha.index.duplicated()]
    r_all = run(alpha, schw_synth, tag="all")
    r_nonhk = run(alpha, schw_synth, subset=alpha.index.difference(HK), tag="non_HK")
    r_hk = run(alpha, schw_synth, subset=set(HK), tag="HK")
    results["methods"][mname] = dict(all=r_all, non_HK=r_nonhk, HK=r_hk)
    for r in (r_all, r_nonhk, r_hk):
        rows.append(dict(method=mname, source="Schwalb2016_GSE75792_K562", stratum=r["tag"],
                         n=r["n"], rho_alpha_synth=r["rho_alpha_synth"],
                         ci_lo=r["ci"][0], ci_hi=r["ci"][1], p=r["p"], validates=r["validates"]))

# MATCHED-GENE-SET (apples-to-apples) headline: for each method, on the SAME genes
# (fit_alpha ∩ Schwalb ∩ Todorovski), compare alpha-vs-Schwalb, alpha-vs-Todorovski, and the
# two sources against each other. This removes the different-gene-universe confound of the main
# table above (fit_alpha∩Schwalb has ~30 genes absent from Todorovski that drift the full-set rho).
matched = {}
matched_rows = []
for mname, (mpath, mcol) in METHODS.items():
    a = pd.read_csv(mpath).set_index("gene")[mcol].dropna()
    a = a[a > 0]; a = a[~a.index.duplicated()]
    tri = a.index.intersection(schw_synth.index).intersection(tod_synth.index)
    tri = tri.difference(HK)  # non-HK matched set (headline stratum)
    if len(tri) < 5:
        matched[mname] = dict(n=int(len(tri)))
        continue
    av = a.loc[tri].values.astype(float)
    sv = schw_synth.loc[tri].values.astype(float)
    tv = tod_synth.loc[tri].values.astype(float)
    r_as, lo_as, hi_as = boot_ci_rho(av, sv)          # alpha vs Schwalb (2nd source)
    r_at, lo_at, hi_at = boot_ci_rho(av, tv)          # alpha vs Todorovski (1st source)
    r_st = float(stats.spearmanr(sv, tv).statistic)   # Schwalb vs Todorovski (source concordance)
    matched[mname] = dict(
        n_nonHK=int(len(tri)),
        alpha_vs_schwalb=dict(rho=round(r_as, 3), ci=[round(lo_as, 3), round(hi_as, 3)],
                              p=float(stats.spearmanr(av, sv).pvalue)),
        alpha_vs_todorovski=dict(rho=round(r_at, 3), ci=[round(lo_at, 3), round(hi_at, 3)],
                                 p=float(stats.spearmanr(av, tv).pvalue)),
        schwalb_vs_todorovski_rho=round(r_st, 3),
    )
    matched_rows.append(dict(method=mname, stratum="non_HK_matched", n=int(len(tri)),
                             rho_alpha_schwalb=round(r_as, 3), ci_lo_as=round(lo_as, 3), ci_hi_as=round(hi_as, 3),
                             rho_alpha_todorovski=round(r_at, 3), ci_lo_at=round(lo_at, 3), ci_hi_at=round(hi_at, 3),
                             rho_schwalb_todorovski=round(r_st, 3)))
results["matched_gene_set_nonHK"] = matched

out = pd.DataFrame(rows)
out.to_csv(RES / "external_rate_validation_schwalb.csv", index=False)
pd.DataFrame(matched_rows).to_csv(RES / "external_rate_validation_schwalb_matched.csv", index=False)
(RES / "external_rate_validation_schwalb.json").write_text(json.dumps(results, indent=2))

print("=== mapping ==="); print(json.dumps(mapping_stats, indent=2))
print("=== QC (mapping discriminator) ==="); print(json.dumps(qc, indent=2))
print("=== MATCHED non-HK gene set (apples-to-apples headline) ==="); print(json.dumps(matched, indent=2))
print("=== full-set: fitted alpha vs Schwalb K562 synth (different gene universe, caveat) ==="); print(out.to_string(index=False))
print("\nWrote:", RES / "external_rate_validation_schwalb.csv")
print("Wrote:", RES / "external_rate_validation_schwalb_matched.csv")
print("Wrote:", DATA / "k562_schwalb_ttseq_synthrate.csv")
