#!/usr/bin/env python3
"""p5_atac_baseline_features.py — 진짜 day0 ATAC baseline feature 어셈블.

연구 목표(CLAUDE.md): baseline epigenomic feature로 epigenetic drug response timing 예측.
기존 p5_lag_model.py의 한계 ①(chromatin feature가 moflow Mc smoothed proxy)을 해소 —
**실제 ATAC peak**(crakvelo_atac_prepro.h5ad, 197,482 peak + 좌표)에서 gene별 promoter/enhancer
접근성을 **day0 HSC/MPP(분화 시작 baseline) 세포**에서 직접 계산한다.

설계
  - baseline 세포 = timepoint==day0 ∩ lineage==HSC/MPP (progenitor 시작 상태).
  - per-cell total-count 정규화(depth 통제) → 세포 평균 = 상대 접근성.
  - peak→gene 매핑(gencode v44 TSS 기준):
      promoter peak = TSS ±2kb 와 겹침
      enhancer peak = TSS ±100kb 내 distal(promoter window 밖)
  - gene별 feature:
      prom_acc  : promoter peak 평균 접근성(baseline 세포)
      enh_acc   : distal enhancer peak 평균 접근성
      enh_sum   : distal enhancer 총합 접근성(누적 regulatory load)
      n_prom/n_enh : peak 개수(regulatory 복잡도)
      prom_enh_ratio : prom/(prom+enh) 접근성 분배
  - 대상 gene = MultiVelo fit gene(multivelo_genes.csv)에 한정 → 모델과 정합.
  ⚠️ caveat: ATAC batch(day0/day7) 미보정이나 본 feature는 day0만 사용 → batch 무관.
     fragment 미보유라 peak-count 기반. 좌표 = consensus union(prep 단계).

실행: conda run -n scv-preprocess python scripts/p5_atac_baseline_features.py
출력: results/atac_baseline_features.csv, results/atac_baseline_features.md
"""
import sys, gzip, re
from pathlib import Path
import numpy as np
import pandas as pd
import anndata as ad
import scipy.sparse as sp

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
ATAC = HERE / "data/velocity/crakvelo_atac_prepro.h5ad"
GTF = HERE / "data/ref/gencode.v44.basic.annotation.gtf.gz"
MV = RES / "multivelo_genes.csv"
PROM_WIN = 2000        # promoter half-window (bp)
ENH_WIN = 100000       # cis enhancer half-window (bp)


def load_tss(gtf, want_genes):
    """gencode GTF → gene_name별 TSS(strand 반영) + chrom. 첫 등장(canonical) 기준."""
    want = set(want_genes)
    tss = {}
    op = gzip.open if str(gtf).endswith(".gz") else open
    with op(gtf, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.split("\t")
            if f[2] != "gene":
                continue
            m = re.search(r'gene_name "([^"]+)"', f[8])
            if not m:
                continue
            name = m.group(1)
            if name not in want or name in tss:
                continue
            chrom, start, end, strand = f[0], int(f[3]), int(f[4]), f[6]
            t = start if strand == "+" else end
            tss[name] = (chrom, t)
    return tss


def assign_peaks(tss, peak_df):
    """gene→(promoter peak idx, enhancer peak idx). peak_df: chrom/start/end/mid, 정렬됨."""
    out = {}
    by_chrom = {c: g for c, g in peak_df.groupby("chrom")}
    for gene, (chrom, t) in tss.items():
        sub = by_chrom.get(chrom)
        if sub is None:
            continue
        mid = sub["mid"].values
        lo = np.searchsorted(mid, t - ENH_WIN, "left")
        hi = np.searchsorted(mid, t + ENH_WIN, "right")
        if hi <= lo:
            continue
        idx = sub["idx"].values[lo:hi]
        dist = np.abs(mid[lo:hi] - t)
        prom = idx[dist <= PROM_WIN]
        enh = idx[dist > PROM_WIN]
        if len(prom) or len(enh):
            out[gene] = (prom, enh)
    return out


def main():
    mv = pd.read_csv(MV, index_col=0)
    genes = list(mv.index)
    print(f"[atac] MultiVelo gene {len(genes)}", flush=True)

    tss = load_tss(GTF, genes)
    print(f"[atac] gencode TSS 매칭 {len(tss)}/{len(genes)} gene", flush=True)

    a = ad.read_h5ad(ATAC)
    print(f"[atac] peaks {a.shape}", flush=True)
    # baseline 세포 = day0 ∩ HSC/MPP
    base_mask = (a.obs["timepoint"].astype(str) == "day0") & \
                (a.obs["lineage"].astype(str) == "HSC/MPP")
    n_base = int(base_mask.sum())
    print(f"[atac] baseline(day0∩HSC/MPP) 세포 {n_base}", flush=True)
    if n_base < 50:
        print("[atac] ⚠️ baseline 세포 부족 → day0 전체로 폴백", flush=True)
        base_mask = (a.obs["timepoint"].astype(str) == "day0")
        n_base = int(base_mask.sum())
        print(f"[atac] day0 전체 {n_base}", flush=True)

    peak_df = pd.DataFrame({
        "chrom": a.var["chrom"].astype(str).values,
        "start": a.var["chromStart"].astype(int).values,
        "end": a.var["chromEnd"].astype(int).values,
        "idx": np.arange(a.n_vars),
    })
    peak_df["mid"] = (peak_df["start"] + peak_df["end"]) // 2
    peak_df = peak_df.sort_values(["chrom", "mid"]).reset_index(drop=True)

    assign = assign_peaks(tss, peak_df)
    print(f"[atac] peak 할당된 gene {len(assign)}", flush=True)

    # baseline 세포 × (관련 peak) 부분행렬 → depth 정규화
    used = sorted({i for p, e in assign.values() for i in np.concatenate([p, e])})
    used = np.array(used)
    Xb = a[base_mask.values][:, used].X
    Xb = Xb.tocsc() if sp.issparse(Xb) else sp.csc_matrix(Xb)
    # per-cell total(전체 peak 기준) 으로 정규화해야 depth 통제 — 전체 행 합 사용
    Xfull = a[base_mask.values].X
    depth = np.asarray(Xfull.sum(axis=1)).ravel() if sp.issparse(Xfull) else Xfull.sum(axis=1)
    depth[depth == 0] = 1.0
    scale = (1e4 / depth)            # CP10k 유사
    col_pos = {peak: j for j, peak in enumerate(used)}

    def acc(peaks):
        """peak 집합의 baseline 세포 평균 접근성(정규화). 반환 (mean_per_peak, sum)."""
        if len(peaks) == 0:
            return np.nan, np.nan
        cols = [col_pos[p] for p in peaks]
        sub = Xb[:, cols]                                   # cell × peak
        norm = sub.multiply(scale[:, None])                # depth 정규화
        per_cell_sum = np.asarray(norm.sum(axis=1)).ravel()  # 세포별 총합
        m_sum = float(per_cell_sum.mean())
        m_mean = m_sum / len(peaks)
        return m_mean, m_sum

    rows = []
    for gene, (prom, enh) in assign.items():
        pm, _ = acc(prom)
        em, es = acc(enh)
        rows.append(dict(gene=gene,
                         prom_acc=pm, enh_acc=em, enh_sum=es,
                         n_prom=len(prom), n_enh=len(enh)))
    feat = pd.DataFrame(rows).set_index("gene")
    feat["prom_enh_ratio"] = feat["prom_acc"] / (feat["prom_acc"].fillna(0) + feat["enh_acc"].fillna(0) + 1e-9)
    feat = feat.sort_index()
    feat.to_csv(RES / "atac_baseline_features.csv")
    print(f"[atac] ✓ feature {feat.shape} → atac_baseline_features.csv", flush=True)

    # 요약 md
    cov = feat[["prom_acc", "enh_acc"]].notna().mean()
    L = ["# day0 ATAC baseline feature 어셈블 (진짜 ATAC peak)", "",
         f"> `crakvelo_atac_prepro.h5ad` 197,482 peak에서 **day0 HSC/MPP {n_base} 세포** baseline 접근성.",
         f"> gencode v44 TSS 기준 promoter(±{PROM_WIN}bp)/enhancer(±{ENH_WIN//1000}kb distal) peak 매핑.",
         f"> p5_lag_model.py 한계 ①(moflow Mc smoothed proxy) 해소용 실제 ATAC feature.", "",
         f"- 대상 gene: MultiVelo {len(genes)} → TSS 매칭 {len(tss)} → peak 할당 **{len(feat)}** gene.",
         f"- feature 커버리지: prom_acc {cov['prom_acc']*100:.0f}%, enh_acc {cov['enh_acc']*100:.0f}%.",
         f"- promoter peak 중앙값 {int(feat['n_prom'].median())}개, enhancer peak 중앙값 {int(feat['n_enh'].median())}개/gene.", "",
         "## feature 분포(중앙값)", "",
         "| feature | median | 설명 |", "|---|---|---|",
         f"| prom_acc | {feat['prom_acc'].median():.3f} | promoter 평균 접근성(CP10k) |",
         f"| enh_acc | {feat['enh_acc'].median():.3f} | distal enhancer 평균 접근성 |",
         f"| enh_sum | {feat['enh_sum'].median():.3f} | distal enhancer 누적 접근성 |",
         f"| prom_enh_ratio | {feat['prom_enh_ratio'].median():.3f} | promoter 접근성 분배 |", "",
         "## 다음", "- `p5_lag_model.py`에 feature set `real-atac` 추가 → moflow-Mc baseline 대비 held-out 일반화 비교.",
         "- ⚠️ peak-count 기반(fragment 미보유), consensus union 좌표. day0만 사용→ATAC batch 무관."]
    (RES / "atac_baseline_features.md").write_text("\n".join(L) + "\n")
    print("[atac] ✓ atac_baseline_features.md", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
