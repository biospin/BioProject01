#!/usr/bin/env python3
"""p7_coupling_lag_alternative.py — make-or-break: lag 대체 지표 + abundance-보정 α (BIOP01-54).

문제: 모델 lag(switch-time 차이)은 비재현(cross-method |ρ|≤0.08)이고 ATAC-shuffle에 불변(model-structural).
대체 후보 = **모델-free 크로마틴-RNA 결합(coupling)**: 유전자별 corr(C[:,g], S[:,g]) across cells.
lag가 못 넘은 두 관문을 이 지표가 넘는지 검정.

3축 + 사전선언 반증기준:
 (1) 인과(ATAC-shuffle): 유전자 라벨을 섞어 coupling 재계산. 모델 lag은 shuffle에 불변이었음(ρ=0.72 보존).
     → 반증: coupling도 shuffle에 불변이면(real≈shuffle) 대체 실패(크로마틴 무관).
 (2) abundance 통제: coupling이 그냥 발현량 함수면 trivial. partial(coupling|abundance) 잔존?
     → 반증: abundance 통제 후 real-shuffle gap이 0이면 실패.
 (3) 재현성(cross-dataset): HSPC coupling rank vs human_brain coupling rank(공유유전자).
     → 반증: 모델 lag 수준(|ρ|≤0.2)이면 재현 실패.
추가) abundance-보정 α: partial Spearman(α, TT-seq synth | mean expression). 잔존하면 α=real kinetics(발현 너머).

실행: ~/miniconda3/envs/scv-preprocess/bin/python -u scripts/p7_coupling_lag_alternative.py
산출: results/coupling_lag_alternative.md 재료(stdout) + results/coupling_per_gene.csv
"""
import os, sys, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3_profile_likelihood as pl

RES = pl.RES
RNG = np.random.default_rng(20260719)


def spearman(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 20: return np.nan
    return stats.spearmanr(x[m], y[m]).statistic


def partial_spearman(x, y, z):
    """Spearman(x,y | z) = corr of residuals of rank(x)~rank(z), rank(y)~rank(z)."""
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    if m.sum() < 20: return np.nan
    rx, ry, rz = stats.rankdata(x[m]), stats.rankdata(y[m]), stats.rankdata(z[m])
    Z = np.c_[np.ones_like(rz), rz]
    def resid(r):
        beta, *_ = np.linalg.lstsq(Z, r, rcond=None); return r - Z @ beta
    ex, ey = resid(rx), resid(ry)
    return stats.pearsonr(ex, ey).statistic


def gene_coupling(C, S, cols=None):
    """per-gene Spearman(C[:,g], S[:,g]) across cells. cols=permutation for shuffle."""
    n = C.shape[1]
    idx = np.arange(n) if cols is None else cols
    out = np.full(n, np.nan)
    for g in range(n):
        out[g] = spearman(C[:, idx[g]], S[:, g])
    return out


def load_h5(path):
    import scanpy as sc
    a = sc.read_h5ad(path)
    def raw(l):
        x = a.layers[l]; return (x.A if hasattr(x, "A") else np.asarray(x)).astype(np.float64)
    return a, raw("ATAC"), raw("Ms")


def main():
    print("=== HSPC 로드 ===", flush=True)
    a, C, U, S, conn = pl.load()
    genes = np.array(a.var_names)
    n = len(genes)
    print(f"cells={C.shape[0]} genes={n}", flush=True)

    # 실제 coupling
    cp = gene_coupling(C, S)
    abund = np.nanmean(S, axis=0)  # 유전자별 평균 발현
    print(f"\n[real coupling] median={np.nanmedian(cp):+.3f}  frac>0={(cp>0).mean():.1%}  n valid={np.isfinite(cp).sum()}", flush=True)

    # (1) 인과: ATAC 유전자 라벨 shuffle × K
    K = 20
    sh_med = []
    sh_all = []
    for k in range(K):
        perm = RNG.permutation(n)
        cps = gene_coupling(C, S, cols=perm)
        sh_med.append(np.nanmedian(cps)); sh_all.append(cps)
        if k == 0: cp_shuffle0 = cps
    sh_all = np.concatenate([s[np.isfinite(s)] for s in sh_all])
    print(f"[shuffle coupling] median(over {K})={np.median(sh_med):+.3f}  pooled median={np.nanmedian(sh_all):+.3f}", flush=True)
    mw = stats.mannwhitneyu(cp[np.isfinite(cp)], sh_all, alternative='greater')
    print(f"[인과 검정] real > shuffle? MW p={mw.pvalue:.2e}  (real median {np.nanmedian(cp):+.3f} vs shuffle {np.nanmedian(sh_all):+.3f})", flush=True)
    # per-gene: real - own-shuffle0
    dgap = cp - cp_shuffle0
    print(f"   per-gene(real - shuffle0): median Δ={np.nanmedian(dgap):+.3f}, frac>0={(dgap>0).mean():.1%}", flush=True)

    # (2) abundance 통제
    rho_cp_abund = spearman(cp, abund)
    print(f"\n[abundance] coupling vs 평균발현 Spearman={rho_cp_abund:+.3f} (높으면 발현 종속 의심)", flush=True)
    # abundance 삼분위 내에서 real>shuffle 유지되나
    fin = np.isfinite(cp) & np.isfinite(abund)
    q = pd.qcut(pd.Series(abund[fin]).rank(method='first'), 3, labels=['low','mid','high'])
    gi = np.where(fin)[0]
    for lab in ['low','mid','high']:
        sub = gi[(q == lab).values]
        rr = np.nanmedian(cp[sub]); ss = np.nanmedian(cp_shuffle0[sub])
        print(f"   [{lab}] real median={rr:+.3f} vs shuffle0 {ss:+.3f}  Δ={rr-ss:+.3f}", flush=True)

    # per-gene csv
    pd.DataFrame(dict(gene=genes, coupling=cp, coupling_shuffle0=cp_shuffle0, abundance=abund)).to_csv(
        os.path.join(RES, "coupling_per_gene.csv"), index=False)

    # (3) 재현성 cross-dataset (human_brain)
    print("\n=== (3) 재현성: human_brain ===", flush=True)
    try:
        hb_path = os.path.join(pl.ROOT, "data", "velocity", "multivelo_human_brain.h5ad")
        ah, Ch, Sh = load_h5(hb_path)
        cph = gene_coupling(Ch, Sh)
        gh = pd.Series(cph, index=np.array(ah.var_names))
        gk = pd.Series(cp, index=genes)
        common = gk.index.intersection(gh.index)
        r = spearman(gk.loc[common].values, gh.loc[common].values)
        print(f"HSPC↔human_brain coupling rank Spearman={r:+.3f} (shared {len(common)})  [모델 lag cross-dataset은 +0.185]", flush=True)
    except Exception as e:
        print(f"human_brain 재현성 스킵: {e}", flush=True)

    # 추가) abundance-보정 α
    print("\n=== abundance-보정 α (partial Spearman) ===", flush=True)
    try:
        DATA = pl.DATA if hasattr(pl, 'DATA') else os.path.join(pl.ROOT, "data")
        HK = set(l.strip() for l in open(os.path.join(DATA, "housekeeping.txt")).read().splitlines() if l.strip())
        mv = pd.read_csv(os.path.join(RES, "multivelo_genes.csv")).set_index("gene")
        alpha = mv["fit_alpha"]; alpha = alpha[alpha > 0]
        synth = pd.read_csv(os.path.join(DATA, "k562_ttseq_synthrate.csv")).set_index("gene")["synth_rate"]
        synth = synth[synth > 0].groupby(level=0).median()
        abund_s = pd.Series(abund, index=genes)
        common = alpha.index.intersection(synth.index).intersection(abund_s.index).difference(HK)
        al = alpha.loc[common].values; sy = synth.loc[common].values; ab = abund_s.loc[common].values
        raw = spearman(al, sy); par = partial_spearman(al, sy, ab)
        print(f"α vs synth (non-HK n={len(common)}): raw Spearman={raw:+.3f} | abundance 통제 partial={par:+.3f}", flush=True)
        print(f"  → partial이 0으로 붕괴하면 'α=대부분 abundance', 살아남으면 'α=real kinetics(발현 너머)'", flush=True)
    except Exception as e:
        print(f"abundance-보정 α 스킵: {e}", flush=True)

    print("\n=== 판정 요약 ===", flush=True)
    print("반증기준: coupling이 (a)shuffle 불변 (b)abundance 통제 후 gap 0 (c)cross-dataset |ρ|≤0.2 → 대체 실패", flush=True)


if __name__ == "__main__":
    main()
