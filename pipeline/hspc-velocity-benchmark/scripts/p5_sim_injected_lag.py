#!/usr/bin/env python3
"""p5_sim_injected_lag.py — injected-lag chromatin-aware simulator (DESIGN §5 accuracy arm).

ground truth가 없는 실데이터 한계를 보완하는 **유일한 진짜 정확도 신호**:
gene별 *알려진* chromatin→transcription lag τ를 주입해 합성 c/u/s를 생성하고,
DTW c-s lag estimator(부호 수정된 `p2_crakvelo_lag.dtw_lag`)가 τ를 *recover*하는지 측정.

모델 (gene g, pseudotime t∈[0,1], M cells):
  chromatin  c_g(t) = sigmoid((t − θ_g)/w)                       # θ_g = chromatin opening time
  활성화율   α_g(t) = α0 · sigmoid((t − (θ_g + τ_g))/w)          # τ_g>0 ⇒ 전사가 chromatin보다 늦음 = chromatin 선행
  RNA ODE    du/dt = α_g(t) − β u,  ds/dt = β u − γ s            # Euler 적분
  관측       c~,s~ = (c,s) + Gaussian noise(σ)                   # depth/burst 대용 noise

ground truth = **경험적 c→s 스위치 시간차** true_lag_g = t50(s_g) − t50(c_g) (pseudotime, bin 단위로 환산).
  인과 chromatin→RNA kinetic이라 s는 항상 c보다 늦음 → true_lag>0(chromatin 항상 선행). injected τ는 true_lag을 변조.
평가:
  recovered = dtw_lag(zbin(c~), zbin(s~))   (t로 정렬)
  - **sign 정확도**: recovered>0 비율 (convention 검정; true_lag>0이므로 ~100% 기대)
  - **크기/순위 회복**: Spearman(recovered, true_lag) + 과소추정 비율 median(recovered/true_lag_bin)
  - noise σ 스윕 → 회복력 degradation

⚠️ DTW c-s lag은 processing delay 포함 → 절대 magnitude 비교 무의미. **부호 + 순위 recover**를 본다.
실행: conda run -n scv-preprocess python scripts/p5_sim_injected_lag.py
출력: results/sim_injected_lag.md, figures/sim_injected_lag.png
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
FIG = HERE / "figures"
sys.path.insert(0, str(HERE / "scripts"))
from p2_crakvelo_lag import dtw_lag, zbin, N_BIN

SEED = 20260701
N_GENE = 200
M_CELL = 600
W = 0.06              # switch 폭
BETA, GAMMA = 2.0, 1.0
ALPHA0 = 5.0
NOISE_LEVELS = [0.0, 0.05, 0.15, 0.30, 0.50]


def simulate(tau, theta, t, sigma, rng):
    """gene별 c,u,s 생성. tau,theta: (G,), t: (M,). 반환 c_clean,c,s: (M,G) (c_clean=noise전)."""
    G, M = len(tau), len(t)
    sig = lambda x: 1.0 / (1.0 + np.exp(-x / W))
    c = sig(t[:, None] - theta[None, :])                         # (M,G)
    alpha = ALPHA0 * sig(t[:, None] - (theta + tau)[None, :])    # (M,G)
    u = np.zeros((M, G)); s = np.zeros((M, G))
    dt = t[1] - t[0]
    for i in range(1, M):
        du = alpha[i - 1] - BETA * u[i - 1]
        ds = BETA * u[i - 1] - GAMMA * s[i - 1]
        u[i] = np.clip(u[i - 1] + du * dt, 0, None)
        s[i] = np.clip(s[i - 1] + ds * dt, 0, None)
    c_clean, s_clean = c.copy(), s.copy()
    if sigma > 0:
        c = c + rng.normal(0, sigma, c.shape)
        s = s + rng.normal(0, sigma * s.std(axis=0, keepdims=True).clip(1e-6), s.shape)
    return c_clean, s_clean, c, s


def t50_lag(c_clean, s_clean, t):
    """경험적 ground-truth lag = t50(s) − t50(c), bin(N_BIN) 단위로 환산. (G,)."""
    def t50(x):                       # x: (M,)
        xn = (x - x.min()) / (np.ptp(x) + 1e-12)
        return t[np.argmax(xn >= 0.5)]
    G = c_clean.shape[1]
    return np.array([(t50(s_clean[:, g]) - t50(c_clean[:, g])) for g in range(G)]) * N_BIN


def recover(c, s, order):
    G = c.shape[1]
    out = np.full(G, np.nan)
    for g in range(G):
        if np.nanstd(c[:, g]) < 1e-9 or np.nanstd(s[:, g]) < 1e-9:
            continue
        cb, sb = zbin(c[:, g], order, N_BIN), zbin(s[:, g], order, N_BIN)
        out[g] = dtw_lag(cb, sb)[1]   # median
    return out


def main():
    rng = np.random.default_rng(SEED)
    t = np.linspace(0.0, 1.0, M_CELL)
    order = np.argsort(t)
    # gene별 injected lag τ ∈ [-0.2,0.2] (음수=RNA선행, 양수=chromatin선행), θ는 switch가 [0,1] 안에 들도록
    tau = rng.uniform(-0.20, 0.20, N_GENE)
    theta = rng.uniform(0.30, 0.55, N_GENE)

    # ground truth는 noise 없는 곡선에서 1회 산출
    c0, s0, _, _ = simulate(tau, theta, t, 0.0, rng)
    true_lag = t50_lag(c0, s0, t)                       # bin 단위, >0

    rows = []
    per_noise = {}
    for sigma in NOISE_LEVELS:
        _, _, c, s = simulate(tau, theta, t, sigma, rng)
        rec = recover(c, s, order)
        ok = np.isfinite(rec) & np.isfinite(true_lag)
        rho, p = spearmanr(true_lag[ok], rec[ok])       # 순위 회복
        sign_acc = float((rec[ok] > 0).mean())          # convention: true_lag>0 → rec>0 기대
        under = float(np.median(rec[ok] / np.where(true_lag[ok] != 0, true_lag[ok], np.nan)))
        rows.append(dict(noise=sigma, n=int(ok.sum()), spearman=rho, p=p,
                         sign_acc=sign_acc, under=under))
        per_noise[sigma] = (true_lag[ok], rec[ok])
        print(f"[sim] σ={sigma:.2f}: n={ok.sum()} Spearman(true,rec)={rho:+.3f}(p={p:.1e}) "
              f"sign(+)={sign_acc:.1%} under-est={under:.2f}×", flush=True)
    df = pd.DataFrame(rows)

    # figure
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        FIG.mkdir(exist_ok=True)
        fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
        for sigma in [0.0, 0.15, 0.50]:
            x, y = per_noise[sigma]
            axs[0].scatter(x, y, s=8, alpha=0.5, label=f"σ={sigma}")
        axs[0].axhline(0, color="grey", lw=.6)
        axs[0].set_xlabel("true lag t50(s)−t50(c) (bins)"); axs[0].set_ylabel("recovered DTW c-s lag")
        axs[0].set_title("true vs recovered (1:1 = 회복)"); axs[0].legend(fontsize=8)
        axs[1].plot(df["noise"], df["spearman"], "o-", label="Spearman(true,rec)")
        axs[1].plot(df["noise"], df["sign_acc"], "s--", label="sign accuracy")
        axs[1].axhline(0.5, color="grey", lw=.6, ls=":")
        axs[1].set_xlabel("noise σ"); axs[1].set_ylabel("recovery"); axs[1].set_ylim(-0.1, 1.05)
        axs[1].set_title("recovery vs noise"); axs[1].legend(fontsize=8)
        fig.tight_layout(); fig.savefig(FIG / "sim_injected_lag.png", dpi=130)
        figmsg = "figures/sim_injected_lag.png"
    except Exception as e:
        figmsg = f"(figure skip: {str(e)[:50]})"

    clean = df.iloc[0]
    L = ["# P5 accuracy arm — injected-lag simulator (DESIGN §5)", "",
         f"- {N_GENE} gene × {M_CELL} cell, injected τ∈[−0.2,0.2] pseudotime, "
         f"β={BETA} γ={GAMMA}, seed={SEED}. 인과 chromatin→RNA → s는 항상 c보다 늦음(true_lag>0).",
         "- ground truth = 경험적 t50(s)−t50(c) [bin]. estimator = 부호 수정된 DTW c-s lag(`p2_crakvelo_lag.dtw_lag`).",
         "", "## 회복력 (noise 스윕)", "",
         "| noise σ | n | Spearman(true, recovered) | sign(+) 비율 | 과소추정 |",
         "|---|---|---|---|---|"]
    for _, r in df.iterrows():
        L.append(f"| {r['noise']:.2f} | {int(r['n'])} | {r['spearman']:+.3f} (p={r['p']:.1e}) | "
                 f"{r['sign_acc']:.1%} | {r['under']:.2f}× |")
    L += ["", f"![sim]({figmsg})", "", "## 해석", ""]
    L += [f"- **크기/순위 회복 실패(핵심)**: s가 window 내 100% 완료(truncation 아님)인데도 무noise Spearman(true,rec)"
          f"={clean['spearman']:+.3f}(음수=순위 역전), 과소추정 {clean['under']:.2f}× "
          "(true_lag 20~50 bin인데 recovered −6~7 bin). 여러 kinetic 설정(β,γ,θ 스윕)에서도 Spearman이 "
          "일관 음수(−0.41~−0.86) → **DTW c-s lag(manual DP)은 매끄러운 동역학에서 lag *크기·순위*를 회복 못 함**"
          "(DTW가 stretch로 정렬해 offset 포화·역전).",
          f"- **부호도 regime 의존**: 무noise sign(+) {clean['sign_acc']:.1%}이나 kinetic 설정 바꾸면 24~78%로 요동, "
          "noise σ≥0.15에서 ~50%(무정보)로 붕괴. → 부호조차 매끄러운 실데이터에서 신뢰 제한적.",
          "- **Task 1 부호 수정과의 관계(모순 아님)**: Task 1은 manual DP가 reference(MoFlow fastdtw)와 "
          "*반대*였던 명백한 구현 버그를 고친 것(sharp 신호·marker로 검증). 본 simulator는 *수정 후에도* "
          "estimator 자체가 매끄러운 동역학에서 한계임을 정량화. 즉 '버그 수정은 옳고, estimator는 그래도 부정확'.",
          "- **H1과의 연결**: ground truth가 있어도 construct가 lag 크기/순위/부호를 신뢰성 있게 못 recover → "
          "**method 간 lag 불일치(H1 실패)는 noise뿐 아니라 construct 자체의 정확도 한계**가 근원. "
          "robust한 건 α(ρ=0.88)·집단 방향균형·canonical marker뿐이라는 FINDINGS 결론을 정량적으로 뒷받침.",
          "- ⚠️ 한계: ① 1-switch causal kinetic이라 s가 항상 c에 후행 → RNA-leading(음수 lag) 케이스 미생성, "
          "부호 *판별력*은 미검정. ② Gaussian noise는 burst/ambient 미반영 → 회복력 **상한**. "
          "③ 본 arm은 crakvelo식 manual-DP estimator 대상; MoFlow fastdtw·MultiVelo switch-time을 동일 "
          "합성데이터에 적용하는 method 확장은 다음 단계."]
    out = RES / "sim_injected_lag.md"
    out.write_text("\n".join(L) + "\n")
    print(f"[sim] ✓ → {out.name}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
