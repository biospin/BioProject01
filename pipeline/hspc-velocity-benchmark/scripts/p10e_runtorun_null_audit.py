#!/usr/bin/env python
"""run-to-run null — 세포·ATAC 고정, 적합만 반복 (velocity_matrix_paired_shuffle.md 후속).

문제: 짝맞춘 ATAC-shuffle 대조의 Δ(=A−B, 중앙값 +0.063)는 세포 재표본은 통제했지만
     MultiVelo **적합 자체의 확률성(fit noise)** 은 통제하지 못했다. Δ = 크로마틴 효과 + fit 잡음.
해결: 같은 재표본 세포집합 S_b 에서 **ATAC 온전** 상태로 재적합한 arm(A2)을 legacy A 와 견줘
     같은 자(중심화 코사인·세포 부트스트랩 B=1000·seed 20260719)로 Δ_rr 을 잰다.

  A_b   = data/velocity/multivelo_bootstrap/refit_<b>.h5ad        (2026-07-01, n_jobs=16)
  A2_b  = data/velocity/multivelo_runtorun/refit_rr_b<b>_nj<N>.h5ad (신규, ATAC 온전, n_jobs=N)
  B_b   = data/velocity/multivelo_bootstrap_shuffled/refit_shuf_<b>.h5ad (ATAC 셔플, n_jobs=12)

  Δ_rr,b  = median_cell[ cen_cos(orig, A_b) − cen_cos(orig, A2_b) ]     ← run-to-run null
  Δ_pair,b= median_cell[ cen_cos(orig, A_b) − cen_cos(orig, B_b)  ]     ← 짝맞춘 크로마틴 효과 (재계산)

  주 null arm = nj12 (셔플 arm B 와 worker 수가 같아 짝 Δ 와 동일한 nj 대비를 갖는다).
  nj16 arm = legacy 와 worker 수까지 같아 **적합 결정론 여부**의 직접 측정.

판정 기준(결과 보기 전 봉인 — 과제 지시문):
  · 양성 진술 가능 = Δ_rr 가 짝 Δ 보다 뚜렷이 작다. 구현:
      (1) 측정한 모든 b 에서  upper CI(|Δ_rr,b|) < lower CI(Δ_pair,b)   (CI 비중첩·크기 조건)
      (2) 전역: max_b upper CI(|Δ_rr,b|) < 짝 Δ 3개 관측 최솟값(+0.0038, b=1)
    (1)·(2) 모두 통과 → POSITIVE-ENABLED. (1)만 통과 → MIXED(측정한 b 한정). 하나라도 CI 겹침 → RETRACTION-MAINTAINED.

실행: conda run -n scv-preprocess python scripts/p10e_runtorun_null_audit.py
출력: results/velocity_matrix_runtorun_null.md / .json  (신규 격리 — 기존 산출 덮어쓰지 않는다)
"""
import glob
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p10_velocity_matrix_audit import (ARMS, _names, cos_rows, load,
                                       sign_agreement, OUT, V, SEED, B_BOOT)
from p10d_paired_shuffle_audit import (BOOT_DIR, SHUF_DIR, CEILING_RANGE,
                                       audit_gene_set, boot_ci, boot_ci_paired,
                                       compare)

RR_DIR = os.path.join(V, "multivelo_runtorun")
PAIRED_JSON = os.path.join(OUT, "velocity_matrix_paired_shuffle.json")   # 읽기 전용
PRIMARY_NJ = 12          # 셔플 arm B 와 동일 worker 수 → 주 null
DETERMINISM_NJ = 16      # legacy 와 동일 worker 수 → 결정론 측정


def boot_ci_paired_abs(a, b, seed=SEED, B=B_BOOT):
    """|짝지은 차이 중앙값| 의 CI (부호와 무관한 크기 비교용)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(a), size=(B, len(a)))
    d = np.abs(np.median(a[idx] - b[idx], axis=1))
    return (float(abs(np.median(a - b))),
            float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)))


def velo_identity(pA, pB, genes):
    """두 fit 의 velo_s 를 공유 gene 위에서 bit 수준 비교."""
    va, vb = set(_names(pA, "var")), set(_names(pB, "var"))
    g = [x for x in genes if x in va and x in vb]
    A, B = load(pA, "velo_s", g), load(pB, "velo_s", g)
    fin = np.isfinite(A) & np.isfinite(B)
    eq = (A == B) | (~np.isfinite(A) & ~np.isfinite(B))
    diff = np.abs(A[fin] - B[fin])
    return dict(n_gene=len(g),
                frac_exact_equal=float(eq.mean()),
                max_abs_diff=float(diff.max()) if diff.size else float("nan"),
                median_abs_diff=float(np.median(diff)) if diff.size else float("nan"),
                bitwise_identical=bool(eq.all()))


def param_identity(b, nj):
    """gene 단위 fit 모수(float64 CSV)의 legacy vs 신규 차이 — velo_s(float32) 비교의 보완."""
    import pandas as pd
    pa = os.path.join(OUT, "bootstrap_refit", f"refit_{b}.csv")
    pb = os.path.join(OUT, "runtorun_refit", f"refit_rr_b{b}_nj{nj}.csv")
    if not (os.path.exists(pa) and os.path.exists(pb)):
        return None
    A = pd.read_csv(pa, index_col=0); B = pd.read_csv(pb, index_col=0)
    if not (len(A) == len(B) and (A.index == B.index).all()):
        return dict(comparable=False)
    num = [c for c in A.columns if c in B.columns and A[c].dtype.kind in "fi"]
    D = (A[num] - B[num]).abs().to_numpy()
    nz = np.isfinite(D) & (D > 0)
    return dict(comparable=True, n_gene=int(len(A)), n_param_col=len(num),
                n_cells_differing=int(nz.sum()),
                frac_entries_differing=float(nz.mean()),
                max_abs_diff=float(np.nanmax(D)) if D.size else float("nan"),
                n_genes_differing=int((nz.any(axis=1)).sum()),
                genes_differing=[str(x) for x in A.index[nz.any(axis=1)]])


def newnew_identity(b, genes):
    """같은 날 돌린 두 신규 적합(nj12 vs nj16) 사이의 동일성 — worker 수 효과 측정."""
    import pandas as pd
    p12 = os.path.join(RR_DIR, f"refit_rr_b{b}_nj12.h5ad")
    p16 = os.path.join(RR_DIR, f"refit_rr_b{b}_nj16.h5ad")
    if not (os.path.exists(p12) and os.path.exists(p16)):
        return None
    rec = dict(b=b, velo=velo_identity(p12, p16, genes))
    c12 = os.path.join(OUT, "runtorun_refit", f"refit_rr_b{b}_nj12.csv")
    c16 = os.path.join(OUT, "runtorun_refit", f"refit_rr_b{b}_nj16.csv")
    if os.path.exists(c12) and os.path.exists(c16):
        A = pd.read_csv(c12, index_col=0); B = pd.read_csv(c16, index_col=0)
        num = [c for c in A.columns if c in B.columns and A[c].dtype.kind in "fi"]
        D = (A[num] - B[num]).abs().to_numpy()
        nz = np.isfinite(D) & (D > 0)
        rec["param"] = dict(n_gene=int(len(A)), n_entries_differing=int(nz.sum()),
                            max_abs_diff=float(np.nanmax(D)) if D.size else float("nan"))
    return rec


def write_md(out):
    L = []; A = L.append
    A("# run-to-run null — 세포·ATAC 고정, 적합만 반복\n")
    A("> 생성 = `scripts/p10e_runtorun_null_audit.py` (fit = `scripts/p2_multivelo_runtorun_refit.py`).")
    A("> 신규 격리 산출물이다. `velocity_matrix_paired_shuffle.*`·`velocity_matrix_audit.*`·`FINDINGS.md`·"
      "draft 는 읽기만 하고 건드리지 않는다.\n")
    A("## 0. 무엇을 재는가\n")
    A("짝맞춘 ATAC-shuffle 대조의 Δ(A−B)는 세포 재표본은 걷어냈지만 MultiVelo 적합 자체의 확률성은 "
      "걷어내지 못했다. 그래서 Δ 안에 크로마틴 효과와 fit 잡음이 섞여 있었고, 크로마틴에 대해 양성 진술을 "
      "할 수 없었다. 여기서는 **세포집합 S_b 와 ATAC 을 모두 고정한 채 적합만 반복**해 fit 잡음의 바닥"
      "(run-to-run null)을 같은 자로 잰다.\n")
    A("| arm | 입력 | worker |")
    A("|---|---|---|")
    A("| A (legacy) | S_b, ATAC 온전 | n_jobs=16 (2026-07-01) |")
    A(f"| A2 (신규) | S_b, ATAC 온전 | n_jobs={PRIMARY_NJ} (주 null), n_jobs={DETERMINISM_NJ} (결정론 측정) |")
    A("| B (셔플) | S_b, ATAC within-lineage 셔플 | n_jobs=12 |\n")
    A("Δ_rr,b = median_cell[cen_cos(원본, A_b) − cen_cos(원본, A2_b)], 세포 부트스트랩 B=1000, seed 20260719. "
      "짝 Δ 와 동일한 자다.\n")
    A("판정 기준은 실행 전 봉인: 양성 진술 가능 = 측정한 모든 b 에서 upper CI(|Δ_rr|) < lower CI(Δ_paired) "
      "이고 전역으로 max upper CI(|Δ_rr|) < 짝 Δ 관측 최솟값(+0.0038). 하나라도 CI 가 겹치면 철회 유지.\n")
    A("## 1. 짝 Δ 재계산 (봉인 수치 재현)\n")
    A("| b | Δ_paired 재계산 [95% CI] | 봉인 보고 |")
    A("|---|---|---|")
    for r in out["paired_recompute"]:
        A(f"| {r['b']} | {r['delta']:+.4f} [{r['ci'][0]:+.4f}, {r['ci'][1]:+.4f}] | {r['sealed_delta']:+.4f} |")
    A("")
    A("## 2. run-to-run null\n")
    A("| b | n_jobs | n_cell | n_gene | A 중심화 | A2 중심화 | Δ_rr [95% CI] | \\|Δ_rr\\| [95% CI] | A·A2 직접 중심화 코사인 | velo_s bit 동일 |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(out["runs"], key=lambda x: (x["b"], x["njobs"])):
        d, dc = r["delta_rr"], r["delta_rr_ci"]
        a, ac = r["abs_delta_rr"], r["abs_delta_rr_ci"]
        A(f"| {r['b']} | {r['njobs']} | {r['n_cell']} | {r['n_gene']} | {r['A_centered_ci'][0]:+.4f} | "
          f"{r['A2_centered_ci'][0]:+.4f} | {d:+.6f} [{dc[0]:+.6f}, {dc[1]:+.6f}] | "
          f"{a:.6f} [{ac[0]:.6f}, {ac[1]:.6f}] | {r['direct_centered_cos_A_A2']:+.6f} | "
          f"{r['velo_identity']['bitwise_identical']} |")
    A("")
    A("## 3. 적합 결정론 실측\n")
    A("| b | n_jobs | 공유 gene | velo_s 정확일치 비율 | max\\|diff\\| | bit 동일 |")
    A("|---|---|---|---|---|---|")
    for r in sorted(out["runs"], key=lambda x: (x["b"], x["njobs"])):
        i = r["velo_identity"]
        A(f"| {r['b']} | {r['njobs']} | {i['n_gene']} | {i['frac_exact_equal']:.6%} | "
          f"{i['max_abs_diff']:.3e} | {i['bitwise_identical']} |")
    A("")
    A("지표(세포별 중심화 코사인) 수준에서 두 적합이 얼마나 다른지도 직접 본다.\n")
    A("| b | n_jobs | 값이 다른 세포 | 세포별 \\|차이\\| 최대 | 평균 |")
    A("|---|---|---|---|---|")
    for r in sorted(out["runs"], key=lambda x: (x["b"], x["njobs"])):
        pcd = r.get("percell_absdiff")
        if not pcd:
            continue
        A(f"| {r['b']} | {r['njobs']} | {pcd['n_cells_differing']}/{pcd['n_cells']} | "
          f"{pcd['max']:.3e} | {pcd['mean']:.3e} |")
    A("\ngene 단위 fit 모수(float64 CSV)로도 같이 본다. velo_s 는 float32 로 읽어 비교하므로 "
      "더 미세한 차이는 모수 쪽에서 드러난다.\n")
    A("| b | n_jobs | gene | 모수 항목 중 다른 비율 | 다른 gene 수 | max\\|diff\\| |")
    A("|---|---|---|---|---|---|")
    for r in sorted(out["runs"], key=lambda x: (x["b"], x["njobs"])):
        pi = r.get("param_identity")
        if not pi or not pi.get("comparable"):
            A(f"| {r['b']} | {r['njobs']} | - | 비교 불가 | - | - |"); continue
        A(f"| {r['b']} | {r['njobs']} | {pi['n_gene']} | {pi['frac_entries_differing']:.4%} | "
          f"{pi['n_genes_differing']} | {pi['max_abs_diff']:.3e} |")
    A("")
    A("같은 날 돌린 두 신규 적합(nj12 vs nj16)끼리도 견준다. worker 수만 다르고 나머지는 같다.\n")
    A("| b | velo_s bit 동일 | velo_s 정확일치 | 모수 중 다른 항목 | 모수 max\\|diff\\| |")
    A("|---|---|---|---|---|")
    for x in out.get("newnew_identity", []):
        v = x["velo"]; pp = x.get("param", {})
        A(f"| {x['b']} | {v['bitwise_identical']} | {v['frac_exact_equal']:.6%} | "
          f"{pp.get('n_entries_differing')} | {pp.get('max_abs_diff'):.3e} |")
    A("")
    gd = out.get("genes_differing_vs_legacy", [])
    A(f"\n같은 날 돌린 두 신규 적합은 worker 수(12 vs 16)에 상관없이 서로 완전히 같다: "
      f"**{out.get('fit_deterministic_same_day')}**. 즉 적합은 같은 입력에 대해 같은 답을 낸다.\n")
    A(f"legacy A(2026-07-01)와 견주면 velo_s 가 bit 단위로 전부 같지는 않다"
      f"(전 run 동일 = **{out['fit_deterministic_all']}**). 차이는 gene "
      f"{len(gd)}개({', '.join(gd) if gd else '없음'})에 국한된다. "
      "b 마다 성격이 다르다. b=0 은 모수 차이가 4.4e-16 로 부동소수 반올림 수준이고, "
      "b=2 는 loss 가 거의 같은 대안 해(t_sw2 65.0 대 66.9)에 정착한 실제 차이다. "
      "지표 수준에서는 세포별 중심화 코사인 차이가 "
      f"최대 {max((r.get('percell_absdiff') or {}).get('max', 0.0) for r in out['runs']):.1e} 라 "
      "Δ_rr 중앙값은 0 그대로다.\n")
    A("## 4. 봉인 기준 대비 판정\n")
    A(f"**{out['verdict']}**\n")
    for c in out["verdict_checks"]["per_b"]:
        A(f"- b={c['b']}: upper CI(|Δ_rr|) {c['abs_delta_rr_upper']:.6f} < lower CI(Δ_paired) "
          f"{c['paired_delta_lower']:.6f} → {c['passes']}")
    A(f"- 전역: max upper CI(|Δ_rr|) {out['verdict_checks']['max_abs_delta_rr_upper']:.6f} vs "
      f"짝 Δ 관측 최솟값 {out['verdict_checks']['paired_min_observed']:+.4f} → "
      f"{out['verdict_checks']['cond2_below_min_paired']}\n")
    A("## 5. 한계\n")
    A("- 측정한 b 는 " + ", ".join(str(b) for b in sorted({r["b"] for r in out["runs"]})) +
      " 로, 짝 Δ 가 컸던 두 쌍이다. b=1(짝 Δ +0.0038)에는 대응 null 을 재지 않았다.")
    A("- MultiVelo 한정이다. MoFlow 는 여전히 인과 주장에서 제외된다.")
    A("- velo_s 는 감사 지표가 쓰는 것과 같은 float32 로 읽어 비교했다. 이보다 미세한 차이는 "
      "gene 단위 모수(float64) 표에서 확인한다.")
    A("- run-to-run 이 결정론으로 나오면 CI 는 퇴화([0,0])한다. 그때 양성 진술을 지탱하는 근거는 "
      "확률적 재적합 분포가 아니라 **결정론 실측**이다. 짝 Δ 에서 빼야 할 fit 잡음 성분이 없다는 뜻이다.")
    A("- 결정론이더라도 짝 Δ 에는 셔플 추출 1회분의 변동이 남는다. b 마다 셔플 seed 가 하나뿐이고, "
      "셔플 seed 반복은 이 분석 범위 밖이다.")
    A("- 효과 크기는 여전히 작다. 짝 Δ 중앙값 +0.063 은 재현성 천장 +0.872 대비 7% 수준이고, "
      "같은 자로 잰 method 간 중심화 코사인 산포(−0.530 ~ +0.131)보다 훨씬 작다.\n")
    A("## 산출물\n")
    A("`results/velocity_matrix_runtorun_null.json` · `scripts/p10e_runtorun_null_audit.py` · "
      "`scripts/p2_multivelo_runtorun_refit.py` · `scripts/run_runtorun_refit.sh`")
    with open(os.path.join(OUT, "velocity_matrix_runtorun_null.md"), "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    obs = _names(ARMS["MultiVelo"][0], "obs")
    pos = {c: i for i, c in enumerate(obs)}
    genes, A_full = audit_gene_set()
    print(f"원본 MultiVelo {A_full.shape[0]} cell × 감사 유전자 {len(genes)}\n")

    rr_paths = sorted(p for p in glob.glob(os.path.join(RR_DIR, "refit_rr_b*_nj*.h5ad"))
                      if ".smoke." not in os.path.basename(p))
    if not rr_paths:
        print("<BLOCKED: run-to-run refit h5ad 없음 — p2_multivelo_runtorun_refit.py 먼저 실행>")
        return 1

    out = {"design": "run-to-run null: identical cells S_b, ATAC intact, re-fit only",
           "audit_genes": int(len(genes)), "orig_cells": int(A_full.shape[0]),
           "sealed_criteria": {
               "positive_enabled": "for all measured b: upper CI(|delta_rr|) < lower CI(delta_paired) "
                                   "AND max upper CI(|delta_rr|) < min observed paired delta (+0.0038)",
               "retraction_maintained": "any |delta_rr| CI overlaps its paired delta CI"},
           "primary_njobs": PRIMARY_NJ, "determinism_njobs": DETERMINISM_NJ,
           "runs": [], "paired_recompute": [], "verdict": None}

    with open(PAIRED_JSON) as f:
        paired_json = json.load(f)
    out["paired_sealed"] = {str(r["b"]): dict(delta=r["delta_centered_median"], ci=r["delta_ci"])
                            for r in paired_json["paired"]}
    paired_min_observed = float(min(paired_json["delta_summary"]["values"]))
    out["paired_min_observed"] = paired_min_observed

    # ── 1) 짝 Δ 재계산 (같은 코드로 봉인 수치가 재현되는지 확인) ─────────────────
    print("[검증] 짝맞춘 Δ 재계산 (velocity_matrix_paired_shuffle.md 대조)")
    bs_rr = sorted({int(re.search(r"_b(\d+)_nj", os.path.basename(p)).group(1)) for p in rr_paths})
    paired_recomp = {}
    for b in bs_rr:
        pr = os.path.join(BOOT_DIR, f"refit_{b}.h5ad")
        ps = os.path.join(SHUF_DIR, f"refit_shuf_{b}.h5ad")
        if not (os.path.exists(pr) and os.path.exists(ps)):
            print(f"    b={b}: 짝 arm 없음 → skip"); continue
        rc = _names(pr, "obs")
        assert np.array_equal(rc, _names(ps, "obs")), f"b={b}: A/B 세포집합 불일치"
        rv, sv = set(_names(pr, "var")), set(_names(ps, "var"))
        g = [x for x in genes if x in rv and x in sv]
        R, H = load(pr, "velo_s", g), load(ps, "velo_s", g)
        A = A_full[np.array([pos[c] for c in rc])][:, np.isin(genes, np.array(g))]
        good = (np.isfinite(R).all(0) & (R.std(0) > 0) & np.isfinite(H).all(0) & (H.std(0) > 0))
        _, _, cenA = compare(A[:, good], R[:, good], "A")
        _, _, cenB = compare(A[:, good], H[:, good], "B")
        d, lo, hi, n = boot_ci_paired(cenA, cenB)
        paired_recomp[b] = dict(delta=d, ci=[lo, hi], n_cell=int(n), n_gene=int(good.sum()))
        sealed = out["paired_sealed"].get(str(b))
        print(f"    b={b} Δ_paired {d:+.4f} [{lo:+.4f},{hi:+.4f}]  (봉인 {sealed['delta']:+.4f})")
        out["paired_recompute"].append(dict(b=b, **paired_recomp[b],
                                            sealed_delta=sealed["delta"] if sealed else None))

    # ── 2) run-to-run null ────────────────────────────────────────────────────
    print("\n[본 측정] run-to-run null (ATAC 온전, 같은 S_b, 적합만 반복)")
    for p in rr_paths:
        m = re.search(r"_b(\d+)_nj(\d+)\.h5ad$", os.path.basename(p))
        b, nj = int(m.group(1)), int(m.group(2))
        pr = os.path.join(BOOT_DIR, f"refit_{b}.h5ad")
        if not os.path.exists(pr):
            print(f"    b={b}: legacy refit 없음 → skip"); continue
        rc, rc2 = _names(pr, "obs"), _names(p, "obs")
        same_cells = bool(np.array_equal(rc, rc2))
        assert same_cells, f"b={b} nj={nj}: 세포집합 불일치 — run-to-run null 성립 안 함"
        rv, sv = set(_names(pr, "var")), set(_names(p, "var"))
        g = [x for x in genes if x in rv and x in sv]
        R, R2 = load(pr, "velo_s", g), load(p, "velo_s", g)
        A = A_full[np.array([pos[c] for c in rc])][:, np.isin(genes, np.array(g))]
        good = (np.isfinite(R).all(0) & (R.std(0) > 0) & np.isfinite(R2).all(0) & (R2.std(0) > 0))
        recA, rawA, cenA = compare(A[:, good], R[:, good], f"A refit_{b}")
        recA2, rawA2, cenA2 = compare(A[:, good], R2[:, good], f"A2 refit_rr_b{b}_nj{nj}")
        mA, loA, hiA = boot_ci(cenA)
        m2, lo2, hi2 = boot_ci(cenA2)
        d, dlo, dhi, ncell = boot_ci_paired(cenA, cenA2)
        ad_, alo, ahi = boot_ci_paired_abs(cenA, cenA2)
        pc = np.abs(cenA - cenA2)
        percell = dict(max=float(np.nanmax(pc)), mean=float(np.nanmean(pc)),
                       n_cells_differing=int(np.nansum(pc > 0)), n_cells=int(len(pc)))
        recD, rawD, cenD = compare(R[:, good], R2[:, good], f"A vs A2 (b={b}, nj={nj})")
        ident = velo_identity(pr, p, genes)
        rec = dict(b=b, njobs=nj, n_cell=int(len(rc)), n_gene=int(good.sum()),
                   same_cells=same_cells,
                   A_centered_ci=[mA, loA, hiA], A2_centered_ci=[m2, lo2, hi2],
                   delta_rr=d, delta_rr_ci=[dlo, dhi],
                   abs_delta_rr=ad_, abs_delta_rr_ci=[alo, ahi],
                   direct_centered_cos_A_A2=float(np.nanmedian(cenD)),
                   direct_raw_cos_A_A2=float(np.nanmedian(rawD)),
                   sign_agreement_A_A2=recD["sign_agreement"],
                   percell_absdiff=percell,
                   velo_identity=ident, param_identity=param_identity(b, nj),
                   is_primary=bool(nj == PRIMARY_NJ))
        out["runs"].append(rec)
        print(f"  b={b} nj={nj} (n_cell={rec['n_cell']}, n_gene={rec['n_gene']})")
        print(f"    A  centered {mA:+.3f}  A2 centered {m2:+.3f}")
        print(f"    Δ_rr {d:+.6f} [{dlo:+.6f},{dhi:+.6f}]   |Δ_rr| {ad_:.6f} [{alo:.6f},{ahi:.6f}]")
        print(f"    A vs A2 직접 중심화 코사인 {np.nanmedian(cenD):+.6f} | "
              f"velo_s bit 동일={ident['bitwise_identical']} "
              f"(정확일치 {ident['frac_exact_equal']:.6%}, max|diff| {ident['max_abs_diff']:.3e})")

    out["newnew_identity"] = [x for x in (newnew_identity(b, genes) for b in bs_rr) if x]
    for x in out["newnew_identity"]:
        v = x["velo"]; pp = x.get("param", {})
        print(f"  [신규 nj12 vs nj16] b={x['b']}: velo_s bit 동일={v['bitwise_identical']} "
              f"(정확일치 {v['frac_exact_equal']:.6%}), 모수 다른 항목="
              f"{pp.get('n_entries_differing')} max={pp.get('max_abs_diff')}")

    # ── 3) 봉인 기준 판정 ─────────────────────────────────────────────────────
    prim = [r for r in out["runs"] if r["is_primary"] and r["b"] in paired_recomp]
    checks = []
    for r in prim:
        pl = paired_recomp[r["b"]]["ci"][0]
        checks.append(dict(b=r["b"], abs_delta_rr_upper=r["abs_delta_rr_ci"][1],
                           paired_delta_lower=pl,
                           passes=bool(r["abs_delta_rr_ci"][1] < pl)))
    cond1 = bool(checks) and all(c["passes"] for c in checks)
    max_up = max([c["abs_delta_rr_upper"] for c in checks], default=float("nan"))
    cond2 = bool(checks) and (max_up < paired_min_observed)
    verdict = ("양성 진술 가능(POSITIVE-ENABLED)" if cond1 and cond2 else
               "부분 양성(MIXED — 측정한 b 한정)" if cond1 else
               "양성 진술 불가(RETRACTION-MAINTAINED)")
    out["verdict_checks"] = dict(per_b=checks, cond1_all_b_nonoverlap=cond1,
                                 cond2_below_min_paired=cond2,
                                 max_abs_delta_rr_upper=max_up,
                                 paired_min_observed=paired_min_observed)
    out["verdict"] = verdict
    out["determinism"] = {f"b{r['b']}_nj{r['njobs']}": r["velo_identity"] for r in out["runs"]}
    all_det = [r["velo_identity"]["bitwise_identical"] for r in out["runs"]]
    out["fit_deterministic_all"] = bool(all(all_det)) if all_det else None
    nn = out.get("newnew_identity", [])
    out["fit_deterministic_same_day"] = (bool(all(x["velo"]["bitwise_identical"] and
                                                 x.get("param", {}).get("n_entries_differing", 1) == 0
                                                 for x in nn)) if nn else None)
    out["genes_differing_vs_legacy"] = sorted({g for r in out["runs"]
                                               for g in (r.get("param_identity") or {}).get("genes_differing", [])})
    print(f"\n[판정] {verdict}")
    for c in checks:
        print(f"    b={c['b']}: upper|Δ_rr|={c['abs_delta_rr_upper']:.6f} < "
              f"lower Δ_paired={c['paired_delta_lower']:.6f} → {c['passes']}")
    print(f"    전역: max upper|Δ_rr|={max_up:.6f} vs 짝 Δ 관측 최솟값 {paired_min_observed:+.4f} → {cond2}")
    print(f"    MultiVelo 적합 bit 단위 결정론(전 run): {out['fit_deterministic_all']}")

    with open(os.path.join(OUT, "velocity_matrix_runtorun_null.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    write_md(out)
    print("\n✓ results/velocity_matrix_runtorun_null.json / .md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
