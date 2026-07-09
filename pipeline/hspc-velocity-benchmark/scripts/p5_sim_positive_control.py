#!/usr/bin/env python3
"""p5_sim_positive_control.py — synthetic multi-method positive control (ANALYSIS-EXTENSIONS §#2).

목표(한 문장): lag의 cross-method 비일치가 method 결함이 아니라 **regime-specific**임을 입증한다.
lag이 식별 가능한 영역(sharp switch·고SNR)에서는 독립 method(MoFlow fastdtw c-s lag +
MultiVelo switch-time lag)가 lag에 **일치**하고, smooth·저SNR(실제 HSPC 데이터가 사는 영역)에서만 갈린다.

설계(ANALYSIS-EXTENSIONS §#2 + advisor 리뷰):
  - 합성 생성기: 알려진 α,α_c(≈1/W),β,γ + 주입 lag τ 를 갖는 chromatin→RNA ODE로 c(t)/u(t)/s(t) 생성.
    (기존 p5_sim_injected_lag 의 causal sigmoid-switch 생성 로직을 확장; 노이즈는 **3채널 c/u/s 모두**에.)
  - **SNR × switch-sharpness 2D sweep**. 각 grid cell 마다 N_GENE 유전자.
  - 각 합성 데이터를 **두 method에 fit**: MoFlow(fastdtw c-s lag, torch env) + MultiVelo(switch-time
    lag=sw2−sw1, mv env). CRAK·VAE 는 readout 제외.
  - grid cell 마다: (a) cross-method lag concordance(Spearman, bootstrap 95% CI),
    (b) ground-truth injected-lag τ 회복도(Spearman + sign).
  - 부수: permutation-FDR test-A 검정력 보정(known-ρ 주입 → 검출 최소 effect size).

가드레일:
  - MultiVelo 는 구조적 상수-양수 sign 이므로 **magnitude/rank readout 만**. sign 검정은 MoFlow(만).
  - 모든 headline ρ 에 bootstrap CI, SEED 고정.
  - **true-t 를 통일 time-source 로 사용**(MoFlow velocity_pseudotime fallback 금지 — regime-confound).
    lag 은 c-vs-s *offset* 이라 true-t 를 줘도 답을 주는 게 아니다(scope caveat 로 명시).
  - 기존 main CSV(results/multivelo_genes.csv 등) 절대 미접촉 — sim_positive_control_* 만 기록,
    합성 h5ad 는 scratch dir 로.

단계(3-stage, 2-env):
  stage0 generate  : env-agnostic. per-grid-cell RNA+ATAC h5ad(Ms/Mu/spliced/unspliced, Mc, connectivities,
                     X_umap) + truth CSV 를 SIM_DIR 에 기록.  (torch env 에서 실행)
  stage1 probe     : **go/no-go gate**. pure-numpy fastdtw c-s estimator 를 W-sweep 에 걸어 식별 corner 존재/위치 확인.
  stage2a moflow   : conda run -n torch — MoFlow fit → results/sim_positive_control_moflow.csv
  stage2b multivelo: conda run -n mv    — MultiVelo fit → results/sim_positive_control_multivelo.csv
  stage3 aggregate : concordance + bootstrap CI + τ-recovery + FDR power → md + csv.

실행:
  python scripts/p5_sim_positive_control.py generate      # (torch env) 합성 h5ad 생성
  python scripts/p5_sim_positive_control.py probe         # gate (fastdtw만; torch)
  conda run -n torch python scripts/p5_sim_positive_control.py moflow --smoke 15   # 타이밍 스모크
  conda run -n torch python scripts/p5_sim_positive_control.py moflow
  conda run -n mv    python scripts/p5_sim_positive_control.py multivelo
  python scripts/p5_sim_positive_control.py aggregate
"""
from __future__ import annotations
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
FIG = HERE / "figures"
SIM_DIR = HERE / "data" / "velocity" / "sim_positive_control"   # gitignore(data/)

SEED = 20260709
N_GENE = 60            # grid cell 당 유전자 수 (Spearman CI 안정성 ↑)
M_CELL = 600           # 세포 수
BETA, GAMMA = 2.0, 1.0
ALPHA0 = 5.0
FLOOR = 0.02           # baseline 발현(정확한 0 제거) — MultiVelo quantile/max op crash·alpha_c NaN 방지
N_BIN = 20             # MoFlow get_dtw 기본 n_bins

# 2D sweep 축 (probe + MultiVelo 진단으로 결정).
#   MoFlow(DTW): sharp 일수록 회복↑. MultiVelo(ODE): 너무 sharp(W→0)면 alpha_c 포화·비식별 →
#   식별 sweet spot 은 **moderate W(≈0.10) + 고SNR**. 두 method 공통 식별 corner 를 잡도록 moderate 범위.
SHARPNESS_W = [0.06, 0.10, 0.16]     # sharp-ish → moderate → smooth
SNR_LEVELS = [20.0, 6.0, 2.0]         # signal-range/σ. 고SNR → 저SNR(실 HSPC 대응)

# probe 는 더 촘촘한 W grid 로 corner 위치 탐색
PROBE_W = [0.03, 0.045, 0.06, 0.08, 0.10, 0.12, 0.16, 0.20]
PROBE_SNR = [20.0, 6.0, 2.0]


# ────────────────────────────────────────────────────────────────────────────
# 생성기
# ────────────────────────────────────────────────────────────────────────────
def simulate(tau, theta, dc, t, W, snr, rng):
    """gene별 c,u,s 생성 — **activation→deactivation pulse** chromatin→RNA ODE.

    chromatin pulse: c(t)=σ((t−θ)/W)·(1−σ((t−(θ+dc))/W))  # θ에 열리고 θ+dc에 닫힘
    전사창(τ 만큼 지연):  gate(t)=σ((t−(θ+τ))/W)·(1−σ((t−(θ+dc+τ))/W))
    α(t)=ALPHA0·gate(t);  du/dt=α−βu;  ds/dt=βu−γs  (Euler).
    → c·u·s 모두 rise-and-fall(4-state 완결) = MultiVelo switch-time 식별 가능 형태.
       τ>0 = chromatin 이 전사보다 onset·offset 모두 선행(chromatin-lead).
    노이즈: SNR=signal_range/σ 로 c,u,s **세 채널 모두** 동일 규약으로 Gaussian 추가(advisor).
    반환: dict(c_clean,u_clean,s_clean, c,u,s)  각 (M,G).
    """
    G, M = len(tau), len(t)
    sig = lambda x: 1.0 / (1.0 + np.exp(-x / W))
    def pulse(shift):        # (M,G) rise@(θ+shift), fall@(θ+dc+shift)
        on = sig(t[:, None] - (theta + shift)[None, :])
        off = 1.0 - sig(t[:, None] - (theta + dc + shift)[None, :])
        return on * off
    c = pulse(0.0)                                   # chromatin pulse
    alpha = ALPHA0 * pulse(tau)                      # 전사 게이트(τ 지연)
    u = np.zeros((M, G)); s = np.zeros((M, G))
    dt = t[1] - t[0]
    for i in range(1, M):
        du = alpha[i - 1] - BETA * u[i - 1]
        ds = BETA * u[i - 1] - GAMMA * s[i - 1]
        u[i] = np.clip(u[i - 1] + du * dt, 0, None)
        s[i] = np.clip(s[i - 1] + ds * dt, 0, None)
    c = c + FLOOR; u = u + FLOOR; s = s + FLOOR    # baseline floor (정확한 0 제거)
    c_clean, u_clean, s_clean = c.copy(), u.copy(), s.copy()
    if np.isfinite(snr):
        for arr in (c, u, s):
            rng_range = np.ptp(arr, axis=0, keepdims=True).clip(1e-6)  # gene별 signal range
            arr += rng.normal(0, (rng_range / snr), arr.shape)
        np.clip(c, 0, None, out=c); np.clip(u, 0, None, out=u); np.clip(s, 0, None, out=s)
    return dict(c_clean=c_clean, u_clean=u_clean, s_clean=s_clean, c=c, u=u, s=s)


def true_lag_t50(sim, t):
    """경험적 ground-truth onset lag = t50↑(s) − t50↑(c) [pseudotime], noise 없는 곡선의 rising limb.
    (pulse 의 첫 상향교차 = onset). injected τ 의 kinetic 변조판(둘 다 chromatin-leading, >0)."""
    def t50up(x):
        pk = np.argmax(x)                          # peak(상승→하강 경계)
        xr = x[:pk + 1]
        if len(xr) < 2 or np.ptp(xr) < 1e-9:
            return t[pk]
        xn = (xr - xr.min()) / (np.ptp(xr) + 1e-12)
        return t[np.argmax(xn >= 0.5)]
    c0, s0 = sim["c_clean"], sim["s_clean"]
    return np.array([t50up(s0[:, g]) - t50up(c0[:, g]) for g in range(c0.shape[1])])


def make_genes(rng):
    """grid cell 전체가 공유하는 gene별 (tau, theta, dc). 모든 grid cell 동일 축 → cross-cell 비교 정합."""
    tau = rng.uniform(0.02, 0.20, N_GENE)      # 주입 onset lag(양수=chromatin 선행), 크기 변이 → rank 회복
    theta = rng.uniform(0.20, 0.35, N_GENE)    # chromatin opening 시점
    dc = rng.uniform(0.35, 0.50, N_GENE)       # chromatin open 지속(닫힘=θ+dc ≤ ~0.85, [0,1] 안 완결)
    names = [f"G{g:03d}" for g in range(N_GENE)]
    return tau, theta, dc, names


# ────────────────────────────────────────────────────────────────────────────
# fastdtw c-s lag estimator (MoFlow eval_dtw.get_dtw 수학 복제) — probe 및 참조용
# ────────────────────────────────────────────────────────────────────────────
def _norm(x):
    r = np.ptp(x)
    return (x - np.min(x)) / (r if r > 1e-12 else 1.0)


def _smooth(x, size=3):
    from scipy.ndimage import uniform_filter1d
    return uniform_filter1d(x, size=size)


def _bin_avg(x, time, n_bins):
    bins = np.linspace(np.min(time), np.max(time), n_bins + 1)
    binned = np.digitize(time, bins) - 1
    return np.array([np.mean(x[binned == i]) if np.any(binned == i) else np.nan
                     for i in range(n_bins)])


def fastdtw_cs_lag(c, s, time, n_bins=N_BIN):
    """MoFlow get_dtw 와 동일 math 의 c-s lag(median). 양수=chromatin 선행. (true-t 정렬 사용)."""
    from fastdtw import fastdtw
    tt = np.clip(time, 0, np.quantile(time, 0.95))
    cb = _bin_avg(c, tt, n_bins); sb = _bin_avg(s, tt, n_bins)
    cb = pd.Series(cb).interpolate(limit_direction="both").to_numpy()
    sb = pd.Series(sb).interpolate(limit_direction="both").to_numpy()
    c_pad = np.concatenate([[0], _smooth(_norm(cb)), [0]])
    s_pad = np.concatenate([[0], _smooth(_norm(sb)), [0]])
    tpad = np.linspace(0, 1, len(c_pad))
    _, path = fastdtw(c_pad, s_pad)
    lags = [tpad[j] - tpad[i] for i, j in path]   # +: chromatin(i) 가 spliced(j) 보다 앞선 index
    return float(np.median(lags))


# ────────────────────────────────────────────────────────────────────────────
# stage0 generate — per-grid-cell h5ad
# ────────────────────────────────────────────────────────────────────────────
def _build_anndata(sim, names, t, rng):
    import anndata as ad
    import scanpy as sc
    import scipy.sparse as sp
    M = len(t)
    Ms = sim["s"]; Mu = sim["u"]; Mc = sim["c"]
    rna = ad.AnnData(X=sp.csr_matrix(Ms.astype(np.float32)),
                     obs=pd.DataFrame(index=[f"c{i:04d}" for i in range(M)]),
                     var=pd.DataFrame(index=names))
    rna.layers["Ms"] = Ms.astype(np.float32)
    rna.layers["Mu"] = Mu.astype(np.float32)
    rna.layers["spliced"] = sp.csr_matrix(Ms.astype(np.float32))
    rna.layers["unspliced"] = sp.csr_matrix(Mu.astype(np.float32))
    rna.layers["counts"] = sp.csr_matrix(np.round(Ms).astype(np.float32))
    rna.obs["true_t"] = t.astype(float)
    # 결정론적 embedding: [t, jitter] (advisor: stochastic UMAP 회피, 재현성)
    emb = np.column_stack([t, 0.01 * rng.standard_normal(M)]).astype(np.float32)
    rna.obsm["X_umap"] = emb
    rna.obsm["X_pca"] = emb
    # connectivities: clean 1D → sc.pp.neighbors (near-identity smoothing)
    sc.pp.neighbors(rna, n_neighbors=30, use_rep="X_pca", random_state=SEED)
    atac = ad.AnnData(X=sp.csr_matrix(Mc.astype(np.float32)),
                      obs=rna.obs.copy(), var=pd.DataFrame(index=names))
    atac.layers["Mc"] = Mc.astype(np.float32)
    atac.obsm["X_umap"] = emb
    for a in (rna, atac):
        a.uns.pop("log1p", None)
        for k in list(a.uns):
            if a.uns[k] is None:
                del a.uns[k]
    return rna, atac


def cmd_generate():
    import scanpy as sc  # noqa
    SIM_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    t = np.linspace(0.0, 1.0, M_CELL)
    tau, theta, dc, names = make_genes(rng)
    manifest = []
    for wi, W in enumerate(SHARPNESS_W):
        for si, snr in enumerate(SNR_LEVELS):
            cell_id = f"w{wi}_s{si}"
            # 각 grid cell 독립 rng stream(재현·격리)
            crng = np.random.default_rng(SEED + 1000 * wi + si)
            sim = simulate(tau, theta, dc, t, W, snr, crng)
            tl = true_lag_t50(sim, t)
            rna, atac = _build_anndata(sim, names, t, crng)
            rna.write_h5ad(SIM_DIR / f"rna_{cell_id}.h5ad")
            atac.write_h5ad(SIM_DIR / f"atac_{cell_id}.h5ad")
            truth = pd.DataFrame(dict(gene=names, tau_injected=tau, theta=theta, dc=dc,
                                      true_lag_t50=tl))
            truth.to_csv(SIM_DIR / f"truth_{cell_id}.csv", index=False)
            manifest.append(dict(cell_id=cell_id, W=W, snr=snr, wi=wi, si=si,
                                 n_gene=N_GENE, n_cell=M_CELL))
            print(f"[gen] {cell_id}: W={W} SNR={snr} true_lag median={np.median(tl):+.3f}", flush=True)
    pd.DataFrame(manifest).to_csv(SIM_DIR / "manifest.csv", index=False)
    (SIM_DIR / "params.json").write_text(json.dumps(dict(
        SEED=SEED, N_GENE=N_GENE, M_CELL=M_CELL, BETA=BETA, GAMMA=GAMMA, ALPHA0=ALPHA0,
        FLOOR=FLOOR, SHARPNESS_W=SHARPNESS_W, SNR_LEVELS=SNR_LEVELS, N_BIN=N_BIN), indent=2))
    print(f"[gen] ✓ {len(manifest)} grid cells → {SIM_DIR}", flush=True)
    return 0


# ────────────────────────────────────────────────────────────────────────────
# stage1 probe — go/no-go gate (fastdtw only, pure numpy, true-t)
# ────────────────────────────────────────────────────────────────────────────
def cmd_probe():
    from scipy.stats import spearmanr
    RES.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    t = np.linspace(0.0, 1.0, M_CELL)
    tau, theta, dc, names = make_genes(rng)
    rows = []
    for W in PROBE_W:
        for snr in PROBE_SNR:
            crng = np.random.default_rng(SEED + hash((W, snr)) % 10_000)
            sim = simulate(tau, theta, dc, t, W, snr, crng)
            tl = true_lag_t50(sim, t)
            rec = np.array([fastdtw_cs_lag(sim["c"][:, g], sim["s"][:, g], t)
                            for g in range(N_GENE)])
            ok = np.isfinite(rec) & np.isfinite(tl)
            rho_tau, p_tau = spearmanr(tau[ok], rec[ok])       # 주입 τ rank 회복
            rho_t50, _ = spearmanr(tl[ok], rec[ok])            # 경험 t50 lag rank 회복
            sign_pos = float((rec[ok] > 0).mean())             # sign(+) = chromatin-leading
            rows.append(dict(W=W, snr=snr, n=int(ok.sum()),
                             rho_recover_tau=rho_tau, p_tau=p_tau,
                             rho_recover_t50=rho_t50, sign_pos=sign_pos,
                             med_rec=float(np.median(rec[ok]))))
            print(f"[probe] W={W:.3f} SNR={snr}: ρ(τ,rec)={rho_tau:+.3f} "
                  f"ρ(t50,rec)={rho_t50:+.3f} sign(+)={sign_pos:.0%} med_rec={np.median(rec[ok]):+.3f}",
                  flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(RES / "sim_positive_control_probe.csv", index=False)
    # gate 판정: 노이즈 없는(inf SNR) 축에서 sharp corner 가 τ rank 를 +로 회복하고 sign flip 소멸하는가
    clean = df[~np.isfinite(df["snr"]) | (df["snr"] == np.inf)]
    best = clean.loc[clean["rho_recover_tau"].idxmax()] if len(clean) else None
    print("\n[probe] === GATE 판정 ===", flush=True)
    if best is not None:
        print(f"[probe] clean 최고 τ-회복: W={best['W']:.3f} ρ={best['rho_recover_tau']:+.3f} "
              f"sign(+)={best['sign_pos']:.0%}", flush=True)
    print(f"[probe] ✓ → sim_positive_control_probe.csv", flush=True)
    return 0


# ────────────────────────────────────────────────────────────────────────────
# stage2a moflow — conda run -n torch
# ────────────────────────────────────────────────────────────────────────────
def cmd_moflow(smoke=0):
    import scanpy as sc
    sys.path.insert(0, str(HERE / "vendor" / "MoFlow" / "src"))
    from MoFlow.moflow import MOFlow
    man = pd.read_csv(SIM_DIR / "manifest.csv")
    out_csv = RES / ("sim_positive_control_moflow.smoke.csv" if smoke else "sim_positive_control_moflow.csv")
    done = {}
    if out_csv.exists():
        prev = pd.read_csv(out_csv)
        done = {cid: sub for cid, sub in prev.groupby("cell_id")}
    allrows = [] if not done else [prev]
    import time as _time
    for _, m in man.iterrows():
        cid = m["cell_id"]
        if cid in done:
            print(f"[moflow] {cid} 이미 완료 → skip", flush=True); continue
        rna = sc.read_h5ad(SIM_DIR / f"rna_{cid}.h5ad")
        atac = sc.read_h5ad(SIM_DIR / f"atac_{cid}.h5ad")
        if smoke:
            g = list(rna.var_names[:smoke]); rna = rna[:, g].copy(); atac = atac[:, g].copy()
        t0 = _time.perf_counter()
        mf = MOFlow(rna, atac, embed="X_umap", device=None)
        result = mf.velocity(rna, n_jobs=4, save_path=str(SIM_DIR / f"moflow_{cid}_out"))
        # advisor: true-t 통일 time-source (velocity_graph/pseudotime 미사용)
        result.obs["velo_s_pseudotime"] = np.asarray(result.obs["true_t"], float)
        from MoFlow.eval_dtw import get_dtw
        rows = []
        for gene in result.var_names:
            try:
                *_, lag_cs, _ = get_dtw(result, gene, timekey="velo_s_pseudotime", n_bins=N_BIN)
                arr = np.asarray(lag_cs, float)
                rows.append(dict(cell_id=cid, gene=gene,
                                 cs_lag_mean=float(np.nanmean(arr)),
                                 cs_lag_median=float(np.nanmedian(arr))))
            except Exception as e:
                rows.append(dict(cell_id=cid, gene=gene, cs_lag_mean=np.nan,
                                 cs_lag_median=np.nan, err=str(e)[:40]))
        el = _time.perf_counter() - t0
        sub = pd.DataFrame(rows)
        allrows.append(sub)
        pd.concat(allrows, ignore_index=True).to_csv(out_csv, index=False)   # checkpoint
        n_ok = int(sub["cs_lag_median"].notna().sum())
        print(f"[moflow] {cid}: {n_ok}/{len(sub)} gene lag | {el:.0f}s "
              f"({el/max(1,len(sub)):.1f}s/gene) → {out_csv.name}", flush=True)
        if smoke:
            break
    print(f"[moflow] ✓ → {out_csv.name}", flush=True)
    return 0


# ────────────────────────────────────────────────────────────────────────────
# stage2b multivelo — conda run -n mv
# ────────────────────────────────────────────────────────────────────────────
def cmd_multivelo(smoke=0):
    import scanpy as sc
    import anndata as ad
    import multivelo as mv
    try:
        import torch; torch.set_num_threads(1)
    except Exception:
        pass
    man = pd.read_csv(SIM_DIR / "manifest.csv")
    out_csv = RES / ("sim_positive_control_multivelo.smoke.csv" if smoke else "sim_positive_control_multivelo.csv")
    done = set()
    allrows = []
    if out_csv.exists():
        prev = pd.read_csv(out_csv); done = set(prev["cell_id"].unique()); allrows = [prev]
    import time as _time
    for _, m in man.iterrows():
        cid = m["cell_id"]
        if cid in done:
            print(f"[mv] {cid} 이미 완료 → skip", flush=True); continue
        rna = sc.read_h5ad(SIM_DIR / f"rna_{cid}.h5ad")
        atac = sc.read_h5ad(SIM_DIR / f"atac_{cid}.h5ad")
        if smoke:
            g = list(rna.var_names[:smoke]); rna = rna[:, g].copy(); atac = atac[:, g].copy()
        t0 = _time.perf_counter()
        try:
            res = mv.recover_dynamics_chrom(
                rna.copy(), atac.copy(), max_iter=5, device="cpu",
                parallel=True, n_jobs=6, embedding="X_umap")
        except ValueError as e:
            print(f"[mv] {cid} fit 실패(low-quality?): {e}", flush=True)
            res = None
        el = _time.perf_counter() - t0
        keep = [c for c in (res.var.columns if res is not None else []) if c.startswith("fit_")]
        if res is not None and keep:
            g = res.var[keep].copy(); g.insert(0, "cell_id", cid); g.index.name = "gene"
            g = g.reset_index()
            n_fit = len(g)
        else:
            g = pd.DataFrame(columns=["cell_id", "gene"]); n_fit = 0
        allrows.append(g)
        pd.concat(allrows, ignore_index=True).to_csv(out_csv, index=False)   # checkpoint
        print(f"[mv] {cid}: fit {n_fit} gene | {el:.0f}s → {out_csv.name}", flush=True)
        if smoke:
            break
    print(f"[mv] ✓ → {out_csv.name}", flush=True)
    return 0


# ────────────────────────────────────────────────────────────────────────────
# main dispatch
# ────────────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(__doc__); return 1
    cmd = sys.argv[1]
    smoke = int(sys.argv[sys.argv.index("--smoke") + 1]) if "--smoke" in sys.argv else 0
    if cmd == "generate":
        return cmd_generate()
    if cmd == "probe":
        return cmd_probe()
    if cmd == "moflow":
        return cmd_moflow(smoke=smoke)
    if cmd == "multivelo":
        return cmd_multivelo(smoke=smoke)
    if cmd == "aggregate":
        from p5_sim_positive_control_agg import cmd_aggregate
        return cmd_aggregate()
    if cmd == "report":     # 캐시된 grid/fdr CSV 로 md+fig 만 재생성(재계산 없음)
        from p5_sim_positive_control_agg import cmd_report
        return cmd_report()
    print(f"unknown cmd: {cmd}"); return 1


if __name__ == "__main__":
    sys.exit(main())
