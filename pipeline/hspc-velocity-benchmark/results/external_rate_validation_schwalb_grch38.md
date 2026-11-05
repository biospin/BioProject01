# GRCh38-corrected rerun: alpha vs Schwalb 2016 (GSE75792) K562 TT-seq synthesis rate

Run 2026-11-05. Script `scripts/external_rate_validation_schwalb_grch38.py` (new; the original `external_rate_validation_schwalb.py` and its outputs are untouched). Env `scv-preprocess`. Tables below are generated from `results/external_rate_validation_schwalb_grch38{.csv,_matched.csv,_abundance.csv,_inclNA.csv,.json}`.

## What was wrong

The GEO file `GSE75792_transcript.annotation.gtf.gz` is in GRCh38 coordinates, but the original script joined it to GENCODE v19 (hg19). Evidence checked in this run: the file's MYC TU is chr8:127,734,280-127,746,937 and GENCODE v24 (GRCh38) puts MYC at chr8:127,735,434-127,741,434, while GENCODE v19 (hg19) puts MYC at chr8:128,747,680-128,753,674. TP53: TU chr17:7,656,388-7,688,040 vs v24 7,661,779-7,687,550 vs v19 7,565,097-7,590,856. ACTB: v24 chr7:5,527,151-5,563,784 vs v19 5,566,782-5,603,415 (the co-author's ACTB-region TU ends at chr7:5,530,593, a PROMPT/conRNA TU on the minus strand at 5.52-5.53 Mb, which lies inside the v24 ACTB span and about 36 kb outside the v19 ACTB span; the sense ACTB TU itself was not separately checked). Under hg19, 2,965/6,913 TUs passed the reciprocal-overlap gate (2,746 genes); under GRCh38 6,907/6,913 pass (6,783 genes). The original conclusion ("2nd source is null") was an artifact of mis-joined genes.

## Provenance

| item | value |
|---|---|
| Annotation | GENCODE release 24 (GRCh38, Ensembl 83), `https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_24/gencode.v24.annotation.gtf.gz` |
| sha256 (full gtf.gz) | `147e62909c2cdd622433edae71796367b5774aa17f676174242801a79220093d` |
| sha256 (feature==gene subset, `data/gencode.v24.genes.gtf.gz`) | `438636113b82365276d697277d0ca5f404891ac3289f7cf6b3ab547b8d130d36` |
| Schwalb GTF sha256 | `2c7a31a83d81db465889973860b0a00dab5c081997432ada1fb396db9e6707b9` (matches the DATASETS manifest) |
| Per-gene table (`data/k562_schwalb_ttseq_synthrate_grch38.csv`) sha256 | `23758525fffac60e2dd0257ae59950d903f3a3156f43bc47dec8689c8e241b38` |
| Abundance | `results/coupling_per_gene.csv`, column `abundance` (HSPC mean Ms, as used in `scripts/p7b_abundance_valid.py`) |

Choice of v24: GENCODE v24 = Ensembl 83 (Dec 2015), the GRCh38 release contemporaneous with the Schwalb 2016 TU annotation, and the release the co-author used. Gene symbol mapping uses the gene_name attribute as in the original. No other input in the script implies a release (HSPC gene symbols are joined by name only).

## Method (identical to the original except where listed)

Same filters (TU biotype protein_coding, GENCODE flag TRUE, numeric synth), same reciprocal-overlap gate 0.5, median per gene, HK/non-HK strata, Spearman, paired-gene percentile bootstrap B=10,000, seed 20260710 with the same call order, so the alpha rows are exactly a v19-to-v24 swap. Additions (abundance, NA-biotype variant, QC) use a separate RNG stream (seed 20261105), so they do not perturb the alpha rows. Note each protein_coding TU is listed once but each NA-biotype TU twice (two biotype annotation systems), which doubles its weight in the per-gene median in the +NA variant (a dedup check changes rho by at most 0.01).

### A. alpha vs Schwalb synthesis, full gene set (non-HK headline stratum)

| method | stratum | hg19 (original) | GRCh38 (corrected) |
|---|---|---|---|
| rna_only | all | n=89, -0.186 [-0.388, +0.028] | n=130, +0.061 [-0.120, +0.240] |
| rna_only | non_HK | n=88, -0.188 [-0.393, +0.031] | n=124, +0.087 [-0.100, +0.271] |
| rna_only | HK | n=1, NA | n=6, -0.429 [-1.000, +0.800] |
| multivelo | all | n=99, -0.207 [-0.391, -0.009] | n=169, +0.237 [+0.077, +0.388] |
| multivelo | non_HK | n=96, -0.210 [-0.391, -0.011] | n=157, +0.270 [+0.108, +0.428] |
| multivelo | HK | n=3, NA | n=12, +0.049 [-0.588, +0.644] |
| multivelovae | all | n=110, -0.245 [-0.419, -0.063] | n=177, +0.211 [+0.057, +0.357] |
| multivelovae | non_HK | n=107, -0.260 [-0.431, -0.073] | n=164, +0.235 [+0.080, +0.381] |
| multivelovae | HK | n=3, NA | n=13, +0.033 [-0.621, +0.714] |

### B. Matched non-HK gene set (alpha ∩ Schwalb ∩ Todorovski)

| method | quantity | hg19 | GRCh38 |
|---|---|---|---|
| rna_only | alpha vs Schwalb | n=50, -0.046 [-0.345, +0.249] | n=108, +0.095 [-0.108, +0.295] |
| rna_only | alpha vs Todorovski | +0.229 [-0.052, +0.485] | +0.299 [+0.107, +0.475] |
| rna_only | Schwalb vs Todorovski | +0.138 | +0.483 |
| multivelo | alpha vs Schwalb | n=54, -0.009 [-0.284, +0.264] | n=138, +0.271 [+0.095, +0.435] |
| multivelo | alpha vs Todorovski | +0.427 [+0.142, +0.659] | +0.341 [+0.170, +0.495] |
| multivelo | Schwalb vs Todorovski | +0.212 | +0.510 |
| multivelovae | alpha vs Schwalb | n=56, -0.059 [-0.344, +0.220] | n=143, +0.249 [+0.088, +0.402] |
| multivelovae | alpha vs Todorovski | +0.326 [+0.050, +0.569] | +0.319 [+0.157, +0.467] |
| multivelovae | Schwalb vs Todorovski | +0.195 | +0.510 |

### C. Abundance (HSPC mean Ms) vs synthesis, identical genes as alpha (delta = rho(alpha,synth) - rho(abundance,synth), paired bootstrap)

| source / TU filter | method | stratum | n | alpha vs synth | abundance vs synth | delta | rho(alpha,abund) |
|---|---|---|---|---|---|---|---|
| schwalb / protein_coding_only | rna_only | all | 122 | +0.071 [-0.123, +0.254] | +0.248 [+0.060, +0.421] | -0.177 [-0.306, -0.057] | +0.768 |
| schwalb / protein_coding_only | rna_only | non_HK | 116 | +0.102 [-0.092, +0.289] | +0.262 [+0.070, +0.438] | -0.159 [-0.289, -0.034] | +0.771 |
| schwalb / protein_coding_only | rna_only | HK | 6 | -0.429 [-1.000, +0.742] | -0.143 [-1.000, +1.000] | -0.286 [-1.000, +0.000] | +0.771 |
| schwalb / protein_coding_only | rna_only | non_HK_matched | 101 | +0.116 [-0.095, +0.323] | +0.234 [+0.033, +0.425] | -0.119 [-0.252, +0.013] | +0.789 |
| schwalb / protein_coding_only | multivelo | all | 169 | +0.237 [+0.081, +0.389] | +0.274 [+0.116, +0.422] | -0.037 [-0.138, +0.062] | +0.792 |
| schwalb / protein_coding_only | multivelo | non_HK | 157 | +0.270 [+0.105, +0.421] | +0.309 [+0.150, +0.460] | -0.039 [-0.132, +0.050] | +0.825 |
| schwalb / protein_coding_only | multivelo | HK | 12 | +0.049 [-0.599, +0.648] | -0.196 [-0.730, +0.498] | +0.245 [-0.509, +0.942] | +0.420 |
| schwalb / protein_coding_only | multivelo | non_HK_matched | 138 | +0.271 [+0.098, +0.435] | +0.299 [+0.126, +0.461] | -0.028 [-0.129, +0.069] | +0.822 |
| schwalb / protein_coding_only | multivelovae | all | 169 | +0.227 [+0.072, +0.376] | +0.274 [+0.119, +0.422] | -0.048 [-0.151, +0.058] | +0.773 |
| schwalb / protein_coding_only | multivelovae | non_HK | 157 | +0.250 [+0.092, +0.398] | +0.309 [+0.151, +0.462] | -0.058 [-0.161, +0.043] | +0.795 |
| schwalb / protein_coding_only | multivelovae | HK | 12 | +0.021 [-0.662, +0.707] | -0.196 [-0.736, +0.502] | +0.217 [-0.500, +0.946] | +0.517 |
| schwalb / protein_coding_only | multivelovae | non_HK_matched | 138 | +0.275 [+0.104, +0.434] | +0.299 [+0.125, +0.457] | -0.024 [-0.131, +0.080] | +0.808 |
| schwalb / incl_NA_biotype | rna_only | all | 137 | +0.068 [-0.110, +0.243] | +0.260 [+0.087, +0.423] | -0.192 [-0.311, -0.075] | +0.763 |
| schwalb / incl_NA_biotype | rna_only | non_HK | 129 | +0.107 [-0.078, +0.283] | +0.290 [+0.114, +0.453] | -0.183 [-0.305, -0.066] | +0.763 |
| schwalb / incl_NA_biotype | rna_only | HK | 8 | -0.429 [-1.000, +0.538] | -0.190 [-0.852, +0.675] | -0.238 [-0.720, +0.000] | +0.857 |
| schwalb / incl_NA_biotype | rna_only | non_HK_matched | 112 | +0.123 [-0.078, +0.311] | +0.256 [+0.064, +0.429] | -0.133 [-0.257, -0.009] | +0.789 |
| schwalb / incl_NA_biotype | multivelo | all | 193 | +0.245 [+0.099, +0.386] | +0.275 [+0.128, +0.414] | -0.030 [-0.123, +0.064] | +0.802 |
| schwalb / incl_NA_biotype | multivelo | non_HK | 179 | +0.275 [+0.124, +0.413] | +0.317 [+0.169, +0.454] | -0.042 [-0.128, +0.042] | +0.835 |
| schwalb / incl_NA_biotype | multivelo | HK | 14 | -0.029 [-0.595, +0.555] | -0.314 [-0.795, +0.298] | +0.286 [-0.371, +0.867] | +0.451 |
| schwalb / incl_NA_biotype | multivelo | non_HK_matched | 155 | +0.283 [+0.119, +0.436] | +0.304 [+0.143, +0.455] | -0.022 [-0.114, +0.069] | +0.832 |
| schwalb / incl_NA_biotype | multivelovae | all | 193 | +0.224 [+0.081, +0.363] | +0.275 [+0.132, +0.409] | -0.050 [-0.148, +0.046] | +0.779 |
| schwalb / incl_NA_biotype | multivelovae | non_HK | 179 | +0.255 [+0.110, +0.393] | +0.317 [+0.170, +0.452] | -0.062 [-0.159, +0.033] | +0.794 |
| schwalb / incl_NA_biotype | multivelovae | HK | 14 | -0.121 [-0.678, +0.578] | -0.314 [-0.792, +0.306] | +0.193 [-0.307, +0.797] | +0.613 |
| schwalb / incl_NA_biotype | multivelovae | non_HK_matched | 155 | +0.283 [+0.124, +0.433] | +0.304 [+0.139, +0.454] | -0.022 [-0.123, +0.081] | +0.812 |
| todorovski / primary | rna_only | all | 179 | +0.268 [+0.121, +0.402] | +0.415 [+0.277, +0.538] | -0.147 [-0.243, -0.052] | +0.765 |
| todorovski / primary | rna_only | non_HK | 167 | +0.242 [+0.088, +0.387] | +0.370 [+0.219, +0.504] | -0.128 [-0.227, -0.029] | +0.762 |
| todorovski / primary | rna_only | HK | 12 | +0.629 [+0.011, +0.936] | +0.615 [-0.065, +0.943] | +0.014 [-0.229, +0.277] | +0.916 |
| todorovski / primary | multivelo | all | 254 | +0.285 [+0.163, +0.401] | +0.446 [+0.330, +0.551] | -0.162 [-0.236, -0.091] | +0.794 |
| todorovski / primary | multivelo | non_HK | 235 | +0.262 [+0.133, +0.386] | +0.410 [+0.284, +0.524] | -0.148 [-0.222, -0.077] | +0.814 |
| todorovski / primary | multivelo | HK | 19 | +0.698 [+0.336, +0.885] | +0.749 [+0.408, +0.925] | -0.051 [-0.379, +0.268] | +0.647 |
| todorovski / primary | multivelovae | all | 254 | +0.318 [+0.197, +0.427] | +0.446 [+0.330, +0.550] | -0.128 [-0.202, -0.055] | +0.769 |
| todorovski / primary | multivelovae | non_HK | 235 | +0.286 [+0.162, +0.407] | +0.410 [+0.285, +0.524] | -0.124 [-0.201, -0.046] | +0.774 |
| todorovski / primary | multivelovae | HK | 19 | +0.814 [+0.581, +0.930] | +0.749 [+0.406, +0.928] | +0.065 [-0.148, +0.317] | +0.754 |

### D. alpha vs Schwalb, TU biotype protein_coding + NA

| method | stratum | n | rho [95% CI] |
|---|---|---|---|
| rna_only | all | 151 | +0.036 [-0.126, +0.204] |
| rna_only | non_HK | 143 | +0.069 [-0.106, +0.236] |
| rna_only | non_HK_matched | 123 | +0.088 [-0.104, +0.274] |
| multivelo | all | 193 | +0.245 [+0.099, +0.382] |
| multivelo | non_HK | 179 | +0.275 [+0.129, +0.415] |
| multivelo | non_HK_matched | 155 | +0.283 [+0.119, +0.436] |
| multivelovae | all | 205 | +0.190 [+0.051, +0.323] |
| multivelovae | non_HK | 190 | +0.219 [+0.073, +0.352] |
| multivelovae | non_HK_matched | 163 | +0.234 [+0.079, +0.385] |

### E. QC

| quantity | hg19 | GRCh38 protein_coding | GRCh38 +NA |
|---|---|---|---|
| QC1 Schwalb vs Todorovski synth | n=1905, +0.154 | n=6051, +0.415 | n=6900, +0.390 |
| QC2 decay vs half-life, todorovski_K562 (expect negative) | n=1238, -0.013 | n=4179, +0.021 | n=4710, +0.012 |
| QC2 decay vs half-life, rnadecaycafe_K562 (expect negative) | n=1735, -0.048 | n=5738, -0.028 | n=6512, -0.030 |
| QC2 decay vs half-life, molm13 (expect negative) | n=1638, -0.039 | n=5413, +0.005 | n=6156, -0.002 |
| QC2 decay vs half-life, thp1 (expect negative) | n=1249, -0.063 | n=4210, -0.047 | n=4738, -0.054 |
## Notes

- The matched sets are non-HK genes with alpha, Schwalb and Todorovski values. They grow from n=54-56 (hg19) to n=108-143 (GRCh38).
- Abundance rows C use genes present in alpha, the synthesis source and the abundance table, so n can be smaller than in A. The `primary` rows apply the same machinery to the Todorovski (GSE229305) source for reference.
- QC2 (Schwalb decay vs half-life) uses the half-life files in the backup copy of `data/`; decay stays uninformative (|rho| <= 0.06) after the fix, so only synthesis is used.
- HK strata have n <= 14; ignore them.
