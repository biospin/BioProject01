#!/usr/bin/env python3
"""P0 data pre-check for the HSPC velocity benchmark (GSE209878).

Answers the data-dependent open checks in DESIGN.md §8 from a processed
AnnData (.h5ad) or MuData (.h5mu) object — WITHOUT running any method:

  - cell / gene / peak counts (vs expected 11,605 cells)
  - per-cell day0/day7 timepoint label preserved?  (gates H2)
  - cluster / lineage annotation present?
  - spliced/unspliced layers present?              (velocity prerequisite)
  - ATAC modality / peaks present?                 (multiome prerequisite)

Usage:
  python3 check_data.py <path-to-.h5ad-or-.h5mu>

Deps: anndata (required); mudata (only if a .h5mu is passed). numpy.
"""
from __future__ import annotations

import sys
from pathlib import Path

TIME_KEYS = ["day", "timepoint", "time_point", "time", "stage", "condition", "batch", "sample", "orig.ident"]
ANNOT_KEYS = ["lineage", "cell_type", "celltype", "cell.type", "annotation", "anno",
              "leiden", "cluster", "clusters", "louvain", "seurat_clusters"]
SPLICE_LAYERS = ["spliced", "unspliced", "Ms", "Mu", "ambiguous", "matrix"]


def _hit(cols, keys):
    low = {c.lower(): c for c in cols}
    return [low[k] for k in keys if k in low] + \
           [orig for lc, orig in low.items() if any(k in lc for k in keys) and low.get(lc) not in
            [low[k] for k in keys if k in low]]


def report_adata(name, ad, np):
    print(f"\n── modality/object: {name} ──")
    print(f"  shape: {ad.n_obs:,} obs (cells) × {ad.n_vars:,} vars")
    if ad.n_obs:
        exp = 11605
        flag = "✓ matches expected" if ad.n_obs == exp else f"(expected ~{exp:,} for GSE209878)"
        print(f"  cell count: {ad.n_obs:,} {flag}")
    # timepoint
    tcols = _hit(list(ad.obs.columns), TIME_KEYS)
    if tcols:
        print(f"  [timepoint] candidate obs columns: {tcols}")
        for c in tcols[:4]:
            try:
                vals = ad.obs[c].astype(str).unique()
                print(f"     - {c}: {len(vals)} unique → {list(vals)[:8]}")
            except Exception as e:
                print(f"     - {c}: (could not summarize: {e})")
        print("     → H2 gate: if a column cleanly splits day0/day7 per cell, H2 (weak directional) is possible.")
    else:
        print("  [timepoint] ✗ NO day0/day7-like obs column found → H2 (wall-clock anchor) NOT usable from this object.")
    # annotation
    acols = _hit(list(ad.obs.columns), ANNOT_KEYS)
    print(f"  [annotation] cluster/lineage columns: {acols if acols else '✗ none found (need method-agnostic annotation in P1)'}")
    # spliced/unspliced layers
    layers = list(ad.layers.keys())
    sp = [l for l in layers if l in SPLICE_LAYERS or 'splice' in l.lower()]
    print(f"  [velocity layers] {sp if sp else '✗ no spliced/unspliced layers'}  (all layers: {layers})")
    # ATAC hint
    vnames = list(map(str, ad.var_names[:50]))
    atac_like = sum(1 for v in vnames if (":" in v and "-" in v) or v.lower().startswith("chr"))
    if atac_like > len(vnames) * 0.3:
        print(f"  [ATAC] var_names look peak-like (e.g. {vnames[:3]}) → likely an ATAC matrix")
    else:
        print(f"  [ATAC] var_names look gene-like (e.g. {vnames[:3]})")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"✗ not found: {p}", file=sys.stderr)
        return 2
    try:
        import numpy as np
        import anndata as ad_mod
    except ImportError as e:
        print(f"✗ missing dep: {e}. Install: pip install anndata numpy", file=sys.stderr)
        return 2

    print(f"=== P0 data pre-check: {p.name} ===")
    if p.suffix == ".h5mu":
        try:
            import mudata as md
        except ImportError:
            print("✗ .h5mu needs mudata. Install: pip install mudata", file=sys.stderr)
            return 2
        mdata = md.read(str(p))
        print(f"MuData: {mdata.n_obs:,} cells × modalities {list(mdata.mod.keys())}")
        for name, a in mdata.mod.items():
            report_adata(name, a, np)
    else:
        report_adata(p.stem, ad_mod.read_h5ad(str(p)), np)

    print("\n=== 요약 → DESIGN.md §8 체크 갱신에 사용 ===")
    print("  - timepoint 라벨 유무 = H2 가능 여부")
    print("  - spliced/unspliced layer 유무 = velocity 실행 전제")
    print("  - ATAC modality/peak 유무 = multiome 전제")
    print("  - cluster/lineage = P1 method-agnostic annotation 필요 여부")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
