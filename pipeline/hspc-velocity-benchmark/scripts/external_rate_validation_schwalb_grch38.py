#!/usr/bin/env python
"""GRCh38-corrected rerun of external_rate_validation_schwalb.py (2nd TT-seq source, GSE75792).

WHY: the original script joins GSE75792 transcription-unit (TU) coordinates to GENCODE v19 (hg19).
The GEO file is in GRCh38 coordinates (verified: e.g. MYC TU chr8:127,734,280-127,746,937 is the
hg38 MYC locus; hg19 MYC is chr8:128.75 Mb). Under hg19 only 2,965/6,913 TUs passed the reciprocal-
overlap gate. This script is IDENTICAL in logic (filters, gate 0.5, median per gene, Spearman,
paired-gene percentile bootstrap B=10,000, seed 20260710, same call order for the alpha blocks) except:
  (1) the gene annotation is GENCODE v24 (GRCh38; Ensembl 83), not v19;
  (2) additions requested by the co-author review (all RNG draws for additions use a SEPARATE
      generator so the alpha numbers are exactly what a pure v19->v24 swap gives):
      - abundance (HSPC mean Ms, results/coupling_per_gene.csv::abundance, as used in
        scripts/p7b_abundance_valid.py) vs Schwalb synthesis, same gene sets / strata as alpha,
        plus paired-gene bootstrap of delta = rho(alpha, synth) - rho(abundance, synth);
      - variant: TU biotype protein_coding only (original filter) vs protein_coding + NA biotype.
Outputs: results/external_rate_validation_schwalb_grch38.{md,csv,json}, _matched.csv,
         _abundance.csv, data/k562_schwalb_ttseq_synthrate_grch38.csv (gitignored).
"""
import re, gzip, json, hashlib
import numpy as np, pandas as pd
from scipy import stats
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"; DATA = ROOT / "data"
RNG = np.random.default_rng(20260710); B = 10000          # same as original
RNG_X = np.random.default_rng(20261105)                   # separate stream for additions
FRAC_GATE = 0.5
TAG = "_grch38"

GENCODE_URL = "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_24/gencode.v24.annotation.gtf.gz"
GENCODE_FULL = DATA / "gencode.v24.annotation.gtf.gz"
GENCODE_GENES = DATA / "gencode.v24.genes.gtf.gz"          # feature=="gene" subset (same recipe as v19 subset)
SCHWALB_GTF = DATA / "GSE75792_transcript.annotation.gtf.gz"
PRIMARY_SYNTH = DATA / "k562_ttseq_synthrate.csv"
PRIMARY_HALFLIFE = DATA / "todorovski_k562_halflife.csv"
ABUND = RES / "coupling_per_gene.csv"

METHODS = {
    "rna_only":     (RES / "rna_only_dynamical_genes.csv", "fit_alpha"),
    "multivelo":    (RES / "multivelo_genes.csv",          "fit_alpha"),
    "multivelovae": (RES / "multivelovae_genes.csv",       "vae_alpha"),
}
HK = set(l.strip() for l in (DATA / "housekeeping.txt").read_text().splitlines() if l.strip())


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def ensure_gene_subset():
    if GENCODE_GENES.exists():
        return
    with gzip.open(GENCODE_FULL, "rt") as fi, gzip.open(GENCODE_GENES, "wt") as fo:
        for ln in fi:
            if ln.startswith("#"):
                continue
            if ln.split("\t", 3)[2] == "gene":
                fo.write(ln)


def parse_schwalb_tus(path, biotypes=("protein_coding",)):
    """TUs w/ GENCODE=TRUE and numeric synth; biotype in `biotypes`; keep decay for QC2."""
    rows = []
    with gzip.open(path, "rt") as fh:
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            if len(f) < 9 or f[2] not in biotypes:
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
    """GENCODE protein_coding gene-level intervals w/ symbol (v24: attribute gene_type)."""
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
            frac = ov[j] / min(float(r.end - r.start), glen[j])
            assign.append((gn[j], r.synth, r.decay, frac))
    mp = pd.DataFrame(assign, columns=["gene", "synth", "decay", "frac"])
    return mp[mp.frac >= frac_gate]


def boot_ci_rho(x, y, b=B, rng=None):
    rng = RNG if rng is None else rng
    n = len(x); rho0 = stats.spearmanr(x, y).statistic
    rhos = np.empty(b); idx = np.arange(n)
    for i in range(b):
        s = rng.choice(idx, n, replace=True)
        rhos[i] = stats.spearmanr(x[s], y[s]).statistic
    lo, hi = np.nanpercentile(rhos, [2.5, 97.5])
    return float(rho0), float(lo), float(hi)


def boot_delta(a, ab, s, b=B, rng=RNG_X):
    """paired-gene bootstrap of rho(a,s) - rho(ab,s) on the same genes."""
    n = len(s); idx = np.arange(n)
    d0 = stats.spearmanr(a, s).statistic - stats.spearmanr(ab, s).statistic
    ds = np.empty(b)
    for i in range(b):
        k = rng.choice(idx, n, replace=True)
        ds[i] = stats.spearmanr(a[k], s[k]).statistic - stats.spearmanr(ab[k], s[k]).statistic
    lo, hi = np.nanpercentile(ds, [2.5, 97.5])
    return float(d0), float(lo), float(hi)


def run(alpha, synth, subset=None, tag=""):
    common = alpha.index.intersection(synth.index)
    if subset is not None:
        common = common.intersection(subset)
    if len(common) < 5:
        return dict(tag=tag, n=int(len(common)), rho_alpha_synth=None, ci=[None, None], p=None, validates=False)
    a = alpha.loc[common].values.astype(float)
    s = synth.loc[common].values.astype(float)
    rho, lo, hi = boot_ci_rho(a, s)
    p = stats.spearmanr(a, s).pvalue
    return dict(tag=tag, n=int(len(common)), rho_alpha_synth=round(rho, 3),
                ci=[round(lo, 3), round(hi, 3)], p=float(p), validates=bool(lo > 0))


def build_gene_tables(biotypes, gc):
    tu = parse_schwalb_tus(SCHWALB_GTF, biotypes)
    mp = map_tus_to_genes(tu, gc, FRAC_GATE)
    return tu, mp, mp.groupby("gene")["synth"].median(), mp.groupby("gene")["decay"].median()


def load_alpha(mpath, mcol):
    a = pd.read_csv(mpath).set_index("gene")[mcol].dropna()
    a = a[a > 0]
    return a[~a.index.duplicated()]


def sp(x, y):
    return float(stats.spearmanr(x, y).statistic), float(stats.spearmanr(x, y).pvalue)


# =============================== main ===============================
ensure_gene_subset()
gc = parse_gencode_genes(GENCODE_GENES)
tu, mp, schw_synth, schw_decay = build_gene_tables(("protein_coding",), gc)       # ORIGINAL filter
tu_na, mp_na, schw_synth_na, schw_decay_na = build_gene_tables(("protein_coding", "NA"), gc)  # variant

schw_synth.rename("synth_rate").to_csv(DATA / "k562_schwalb_ttseq_synthrate_grch38.csv")
schw_synth_na.rename("synth_rate").to_csv(DATA / "k562_schwalb_ttseq_synthrate_grch38_inclNA.csv")


def mapstats(tu_, mp_, sy):
    return dict(TUs_numeric_GENCODEtrue=int(len(tu_)),
                TUs_unique_by_coord=int(tu_.drop_duplicates(["chr", "start", "end", "strand"]).shape[0]),
                TUs_assigned_frac_gate=int(len(mp_)), frac_gate=FRAC_GATE,
                median_overlap_frac=round(float(mp_.frac.median()), 3),
                unique_genes_mapped=int(sy.shape[0]))


mapping_stats = dict(gencode_protein_coding_genes=int(len(gc)),
                     protein_coding_only=mapstats(tu, mp, schw_synth),
                     incl_NA_biotype=mapstats(tu_na, mp_na, schw_synth_na))

tod_synth = pd.read_csv(PRIMARY_SYNTH).set_index("gene")["synth_rate"]
tod_synth = tod_synth[tod_synth > 0].groupby(level=0).median()
ab = pd.read_csv(ABUND).set_index("gene")["abundance"].dropna()
ab = ab[~ab.index.duplicated()]


# ---- QC1 / QC2 for both variants (no RNG) ----
def qc_block(sy, de):
    c1 = sy.index.intersection(tod_synth.index)
    r1 = stats.spearmanr(sy.loc[c1], tod_synth.loc[c1])
    out = dict(QC1=dict(n=int(len(c1)), rho=round(float(r1.statistic), 3), p=float(r1.pvalue)), QC2={})
    dvalid = de.dropna()
    for pname, ppath in {"todorovski_K562": PRIMARY_HALFLIFE,
                         "rnadecaycafe_K562": DATA / "halflife_rnadecaycafe_k562.csv",
                         "molm13": DATA / "halflife_molm13.csv",
                         "thp1": DATA / "halflife_thp1.csv"}.items():
        if not ppath.exists():
            continue
        hl = pd.read_csv(ppath).set_index("gene")["t_half_h"]
        hl = hl[hl > 0].groupby(level=0).median()
        cc = dvalid.index.intersection(hl.index)
        rr = stats.spearmanr(dvalid.loc[cc], hl.loc[cc])
        out["QC2"][pname] = dict(n=int(len(cc)), rho=round(float(rr.statistic), 3), p=float(rr.pvalue))
    return out


qc = dict(protein_coding_only=qc_block(schw_synth, schw_decay), incl_NA_biotype=qc_block(schw_synth_na, schw_decay_na))

# ---- main alpha vs Schwalb (same order of RNG use as the original) ----
results = {"mapping": mapping_stats, "qc": qc, "methods": {}}
rows = []
for mname, (mpath, mcol) in METHODS.items():
    alpha = load_alpha(mpath, mcol)
    r_all = run(alpha, schw_synth, tag="all")
    r_nonhk = run(alpha, schw_synth, subset=alpha.index.difference(HK), tag="non_HK")
    r_hk = run(alpha, schw_synth, subset=set(HK), tag="HK")
    results["methods"][mname] = dict(all=r_all, non_HK=r_nonhk, HK=r_hk)
    for r in (r_all, r_nonhk, r_hk):
        rows.append(dict(method=mname, source="Schwalb2016_GSE75792_K562_GRCh38", stratum=r["tag"],
                         n=r["n"], rho_alpha_synth=r["rho_alpha_synth"],
                         ci_lo=r["ci"][0], ci_hi=r["ci"][1], p=r["p"], validates=r["validates"]))

matched = {}; matched_rows = []
for mname, (mpath, mcol) in METHODS.items():
    a = load_alpha(mpath, mcol)
    tri = a.index.intersection(schw_synth.index).intersection(tod_synth.index).difference(HK)
    if len(tri) < 5:
        matched[mname] = dict(n=int(len(tri))); continue
    av = a.loc[tri].values.astype(float)
    sv = schw_synth.loc[tri].values.astype(float)
    tv = tod_synth.loc[tri].values.astype(float)
    r_as, lo_as, hi_as = boot_ci_rho(av, sv)
    r_at, lo_at, hi_at = boot_ci_rho(av, tv)
    r_st = float(stats.spearmanr(sv, tv).statistic)
    matched[mname] = dict(
        n_nonHK=int(len(tri)),
        alpha_vs_schwalb=dict(rho=round(r_as, 3), ci=[round(lo_as, 3), round(hi_as, 3)], p=float(stats.spearmanr(av, sv).pvalue)),
        alpha_vs_todorovski=dict(rho=round(r_at, 3), ci=[round(lo_at, 3), round(hi_at, 3)], p=float(stats.spearmanr(av, tv).pvalue)),
        schwalb_vs_todorovski_rho=round(r_st, 3))
    matched_rows.append(dict(method=mname, stratum="non_HK_matched", n=int(len(tri)),
                             rho_alpha_schwalb=round(r_as, 3), ci_lo_as=round(lo_as, 3), ci_hi_as=round(hi_as, 3),
                             rho_alpha_todorovski=round(r_at, 3), ci_lo_at=round(lo_at, 3), ci_hi_at=round(hi_at, 3),
                             rho_schwalb_todorovski=round(r_st, 3)))
results["matched_gene_set_nonHK"] = matched

out = pd.DataFrame(rows)
out.to_csv(RES / f"external_rate_validation_schwalb{TAG}.csv", index=False)
pd.DataFrame(matched_rows).to_csv(RES / f"external_rate_validation_schwalb{TAG}_matched.csv", index=False)

# =================== additions (separate RNG stream) ===================
abund_rows = []


def add_block(variant, synth_s, sname):
    """alpha vs synth and abundance vs synth on IDENTICAL genes (alpha ∩ synth ∩ abundance)."""
    for mname, (mpath, mcol) in METHODS.items():
        a = load_alpha(mpath, mcol)
        base = a.index.intersection(synth_s.index).intersection(ab.index)
        sets = {"all": base, "non_HK": base.difference(HK), "HK": base.intersection(HK)}
        if sname == "schwalb":   # matched triple set (alpha ∩ Schwalb ∩ Todorovski ∩ abundance), non-HK
            sets["non_HK_matched"] = base.intersection(tod_synth.index).difference(HK)
        for st, g in sets.items():
            if len(g) < 5:
                abund_rows.append(dict(variant=variant, source=sname, method=mname, stratum=st, n=int(len(g)))); continue
            av = a.loc[g].values.astype(float); bv = ab.loc[g].values.astype(float)
            sv = synth_s.loc[g].values.astype(float)
            ra, la, ha = boot_ci_rho(av, sv, rng=RNG_X)
            rb, lb, hb = boot_ci_rho(bv, sv, rng=RNG_X)
            d, ld, hd = boot_delta(av, bv, sv)
            abund_rows.append(dict(variant=variant, source=sname, method=mname, stratum=st, n=int(len(g)),
                                   rho_alpha_synth=round(ra, 3), a_lo=round(la, 3), a_hi=round(ha, 3),
                                   rho_abund_synth=round(rb, 3), b_lo=round(lb, 3), b_hi=round(hb, 3),
                                   delta_alpha_minus_abund=round(d, 3), d_lo=round(ld, 3), d_hi=round(hd, 3),
                                   rho_alpha_abund=round(sp(av, bv)[0], 3)))


add_block("protein_coding_only", schw_synth, "schwalb")
add_block("incl_NA_biotype", schw_synth_na, "schwalb")
add_block("primary", tod_synth, "todorovski")   # 1st source on the same machinery (reference)

# alpha-vs-Schwalb with the NA-biotype variant (unrestricted gene sets, same function as main)
na_rows = []
for mname, (mpath, mcol) in METHODS.items():
    alpha = load_alpha(mpath, mcol)
    for st, sub in (("all", None), ("non_HK", alpha.index.difference(HK))):
        g = alpha.index.intersection(schw_synth_na.index)
        if sub is not None:
            g = g.intersection(sub)
        av = alpha.loc[g].values.astype(float); sv = schw_synth_na.loc[g].values.astype(float)
        r, lo, hi = boot_ci_rho(av, sv, rng=RNG_X)
        na_rows.append(dict(method=mname, stratum=st, n=int(len(g)), rho_alpha_synth=round(r, 3),
                            ci_lo=round(lo, 3), ci_hi=round(hi, 3), variant="incl_NA_biotype"))
    tri = alpha.index.intersection(schw_synth_na.index).intersection(tod_synth.index).difference(HK)
    av = alpha.loc[tri].values.astype(float)
    sv = schw_synth_na.loc[tri].values.astype(float); tv = tod_synth.loc[tri].values.astype(float)
    r, lo, hi = boot_ci_rho(av, sv, rng=RNG_X)
    na_rows.append(dict(method=mname, stratum="non_HK_matched", n=int(len(tri)), rho_alpha_synth=round(r, 3),
                        ci_lo=round(lo, 3), ci_hi=round(hi, 3), variant="incl_NA_biotype",
                        rho_schwalb_todorovski=round(float(stats.spearmanr(sv, tv).statistic), 3)))

pd.DataFrame(abund_rows).to_csv(RES / f"external_rate_validation_schwalb{TAG}_abundance.csv", index=False)
pd.DataFrame(na_rows).to_csv(RES / f"external_rate_validation_schwalb{TAG}_inclNA.csv", index=False)

provenance = dict(
    gencode_url=GENCODE_URL, gencode_full_sha256=sha256(GENCODE_FULL), gencode_genes_subset_sha256=sha256(GENCODE_GENES),
    schwalb_gtf_sha256=sha256(SCHWALB_GTF), abundance_file="results/coupling_per_gene.csv (column abundance = HSPC mean Ms)",
    schwalb_per_gene_table_sha256=sha256(DATA / "k562_schwalb_ttseq_synthrate_grch38.csv"))
results["provenance"] = provenance
results["inclNA"] = na_rows
results["abundance"] = abund_rows
(RES / f"external_rate_validation_schwalb{TAG}.json").write_text(json.dumps(results, indent=2, default=str))

print("=== provenance ==="); print(json.dumps(provenance, indent=2))
print("=== mapping ==="); print(json.dumps(mapping_stats, indent=2))
print("=== QC ==="); print(json.dumps(qc, indent=2))
print("=== MATCHED non-HK ==="); print(json.dumps(matched, indent=2))
print("=== full-set alpha vs Schwalb ==="); print(out.to_string(index=False))
print("=== incl NA variant alpha vs Schwalb ==="); print(pd.DataFrame(na_rows).to_string(index=False))
print("=== abundance vs synth ==="); print(pd.DataFrame(abund_rows).to_string(index=False))
