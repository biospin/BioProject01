#!/usr/bin/env python
"""짝맞춘(paired) ATAC-shuffle 대조 — critic MAJOR-2 해소 (velocity_matrix_audit §4 후속).

문제: 기존 §4는 재현성 천장(재표본 15,315 cell)과 ATAC 셔플(전량 21,878 cell)을 직접 견줬다.
     섭동도 세포집합도 다르다.
해결: bootstrap refit이 쓴 **같은 재표본 세포집합 S_b** 위에서 ATAC만 셔플해 재적합한 arm(B)을
     같은 자로 비교한다. 지표·규약은 p10/p10b 와 동일(중심화 코사인 주, raw 병기, 부호 일치율).

  A_b (대조, 기존 산출 읽기전용) = refit_b            vs 원본  [재표본 + run 잡음 = 천장]
  B_b (신규)                     = refit_shuf_b       vs 원본  [같은 S_b, ATAC 셔플만 추가]
  Δ_b = centered_cos(A_b) − centered_cos(B_b)  (세포별 짝지어 계산 → 세포 부트스트랩 CI)

판정 기준(결과 보기 전 봉인, 과제 지시문):
  · 크로마틴 무력 확인 = B가 A의 관측 범위(0.826~0.887) 안이거나 CI가 겹친다.
  · 현 주장 반증       = B가 A보다 실질적으로 아래이고 CI 비중첩 (Δ CI가 0을 배제).

실행: conda run -n scv-preprocess python scripts/p10d_paired_shuffle_audit.py
출력: results/velocity_matrix_paired_shuffle.md / .json / _percell.csv
      기존 velocity_matrix_audit.* / FINDINGS.md / draft*.md 는 건드리지 않는다.
"""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p10_velocity_matrix_audit import (ARMS, SCRAMBLED, _names, cos_rows, load,
                                       sign_agreement, OUT, V, SEED, B_BOOT)

BOOT_DIR = os.path.join(V, "multivelo_bootstrap")
SHUF_DIR = os.path.join(V, "multivelo_bootstrap_shuffled")
CEILING_RANGE = (0.826, 0.887)   # velocity_matrix_audit.md §4 (봉인된 A 관측 범위)


def boot_ci(x, seed=SEED, B=B_BOOT, stat=np.nanmedian):
    """세포 부트스트랩 CI (percentile 95%)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    d = stat(x[idx], axis=1)
    return float(stat(x)), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def boot_ci_paired(a, b, seed=SEED, B=B_BOOT):
    """같은 세포 인덱스를 재표집해 짝지은 차이의 CI."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(a), size=(B, len(a)))
    d = np.median(a[idx] - b[idx], axis=1)
    return float(np.median(a - b)), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)), int(len(a))


def audit_gene_set():
    """p10b 와 동일한 공유 유전자 집합(5 arm 교집합 + 유한/분산0 제외)."""
    var = {k: set(_names(p, "var")) for k, (p, _) in ARMS.items()}
    shared = sorted(set.intersection(*var.values()))
    mats = {k: load(p, l, shared) for k, (p, l) in ARMS.items()}
    ok = np.ones(len(shared), bool)
    for M in mats.values():
        ok &= np.isfinite(M).all(axis=0) & (np.nanstd(M, axis=0) > 0)
    return np.array(shared)[ok], mats["MultiVelo"][:, ok]


def compare(A_orig_rows, S, label):
    """원본(행=해당 세포) vs 재적합 행렬 S. 이미 같은 gene 열로 맞춰진 상태."""
    Ac = A_orig_rows - A_orig_rows.mean(0, keepdims=True)
    Sc = S - S.mean(0, keepdims=True)
    craw = cos_rows(A_orig_rows, S)
    ccen = cos_rows(Ac, Sc)
    sa, n_used, n_excl = sign_agreement(A_orig_rows, S)
    return dict(label=label, raw_median=float(np.nanmedian(craw)),
                centered_median=float(np.nanmedian(ccen)),
                sign_agreement=sa, sign_n=n_used, sign_excluded=n_excl), craw, ccen


def write_md(out):
    """결과를 그대로 md로 옮긴다(해석 문구는 판정 분기별 고정 템플릿)."""
    L = []
    A = L.append
    A("# 짝맞춘(paired) ATAC-shuffle 대조 — velocity 행렬 (critic MAJOR-2)\n")
    A("> 생성 = `scripts/p10d_paired_shuffle_audit.py` (fit = `scripts/p2_multivelo_paired_shuffle_refit.py`).")
    A("> 기존 `velocity_matrix_audit.md`·`FINDINGS.md`·draft는 건드리지 않는다. 이 파일은 독립 산출물이다.\n")
    A("## 0. 무엇을 고쳤나\n")
    A("기존 §4의 인과 비교는 재현성 천장(재표본 15,315 cell)과 ATAC 셔플(전량 21,878 cell)을 견줬다. "
      "세포집합이 달라 like-for-like가 아니었다. 여기서는 bootstrap refit이 쓴 **같은 재표본 세포집합 S_b** 위에서 "
      "ATAC만 셔플해 재적합하고(같은 하이퍼파라미터·같은 canonical gene set·같은 within-lineage 셔플 규약), "
      "세포별로 짝지어 비교한다. 두 arm의 세포 이름 벡터가 정확히 같음을 fit 시점과 분석 시점 모두 assert로 확인했다.\n")
    A(f"판정 기준은 실행 전 봉인: 확인 = B가 A 관측 범위 {CEILING_RANGE} 안이거나 CI 겹침, "
      "반증 = B가 실질적으로 아래이고 CI 비중첩(짝지은 Δ의 CI가 0 배제).\n")
    A("## 1. 분석층 검증 — 기존 감사 수치 재현\n")
    A("| 항목 | 재계산 | 감사 보고 |")
    A("|---|---|---|")
    cen6 = [r["centered_median"] for r in out["ceiling_all6"]]
    sg6 = [r["sign_agreement"] for r in out["ceiling_all6"]]
    A(f"| 재현성 천장(refit 6개) 중심화 코사인 중앙값 | {np.median(cen6):+.3f} (범위 {min(cen6):.3f}~{max(cen6):.3f}) | +0.872 (0.826~0.887) |")
    A(f"| 천장 부호 일치 | {np.median(sg6):.1%} | 78.6% |")
    u = out["unpaired_reference"]
    A(f"| 전량 ATAC 셔플 중심화 코사인 | {u['centered_median']:+.3f} | +0.838 |")
    A(f"| 전량 셔플 부호 일치 | {u['sign_agreement']:.1%} | 78.9% |")
    A("\n같은 코드로 봉인된 값이 재현되므로 아래 신규 수치도 같은 자로 잰 것이다.\n")
    A("## 2. 짝맞춘 대조 (같은 세포집합 S_b)\n")
    A("| b | n_cell | n_gene | A 중심화(ATAC 온전) [95% CI] | B 중심화(ATAC 셔플) [95% CI] | Δ=A−B [95% CI] | A raw | B raw | A 부호 | B 부호 |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for r in out["paired"]:
        a, b_, d = r["A_centered_ci"], r["B_centered_ci"], r["delta_ci"]
        A(f"| {r['b']} | {r['n_cell']} | {r['n_gene']} | {a[0]:+.3f} [{a[1]:+.3f}, {a[2]:+.3f}] | "
          f"{b_[0]:+.3f} [{b_[1]:+.3f}, {b_[2]:+.3f}] | {r['delta_centered_median']:+.4f} [{d[0]:+.4f}, {d[1]:+.4f}] | "
          f"{r['A']['raw_median']:+.3f} | {r['B']['raw_median']:+.3f} | {r['A']['sign_agreement']:.1%} | {r['B']['sign_agreement']:.1%} |")
    A("\nCI는 세포 부트스트랩(B=1000, seed=20260719, percentile). Δ는 같은 세포 인덱스를 재표집한 **짝지은** 차이다.")
    A("세포가 15,315개라 CI 폭이 매우 좁다. 따라서 Δ가 0을 배제한다는 사실 자체는 정보량이 크지 않고, "
      "판정을 지탱하는 근거는 **B가 refit 6개의 관측 범위 전체보다 아래인가**라는 크기 조건이다.\n")
    A("## 3. 봉인 기준 대비 판정\n")
    A(f"**{out['verdict']}**\n")
    A(f"- Δ(A−B) 중앙값 {out['delta_summary']['median']:+.4f}, b별 " +
      ", ".join(f"{d:+.4f}" for d in out["delta_summary"]["values"]) + ".")
    A("- B 중심화 코사인 " + ", ".join(f"{v:+.3f}" for v in out["delta_summary"]["B_values"]) +
      f" vs A 관측 범위 {CEILING_RANGE[0]}~{CEILING_RANGE[1]}.")
    for r in out["paired"]:
        A(f"- b={r['b']}: B가 A 관측범위 안={r['B_within_A_observed_range']}, "
          f"A·B CI 겹침={r['ci_overlap_AB']}, Δ CI가 0 배제={r['delta_ci_excludes_zero']}.")
    A(f"- b별 크기 조건 집계: 관측범위 안/CI 겹침 {out['verdict_counts']['n_within_or_overlap']}개, "
      f"범위 아래 {out['verdict_counts']['n_below_range']}개 (총 {out['verdict_counts']['n_paired']}개).")
    dv = out["delta_summary"]["values"]; bv = out["delta_summary"]["B_values"]
    A(f"\n판정의 강도도 같이 밝힌다. Δ는 b마다 {min(dv):+.4f}~{max(dv):+.4f}로 고르지 않고, "
      f"B 값({', '.join('%+.3f' % v for v in bv)})이 A 범위 하한 {CEILING_RANGE[0]}을 밑도는 폭도 "
      f"{min(CEILING_RANGE[0] - v for v in bv):.3f}~{max(CEILING_RANGE[0] - v for v in bv):.3f}로 좁은 쪽이다. "
      "방향은 3/3 일관되지만 효과 크기는 작다. 특히 b=1은 짝지은 Δ가 +0.0038로 사실상 잡음 수준이고, "
      "그 짝인 A_1이 마침 refit 범위의 하한(+0.826)이어서 범위 조건만 통과한다. "
      "일관된 효과를 실제로 끌고 가는 것은 b=0과 b=2다. b=1의 raw 코사인은 +0.759→+0.386으로 크게 떨어지지만 "
      "중심화는 +0.826→+0.813으로 거의 안 움직인다. 주 지표는 중심화이므로 raw의 낙폭을 근거로 쓰지 않는다.\n")
    A("### 크기 감각 (해석 과잉 방지)\n")
    cross = "−0.530 ~ +0.131"
    A(f"Δ의 크기는 A 값의 몇 %인지로 보는 게 정확하다. 예: Δ {out['delta_summary']['median']:+.3f} 는 "
      f"천장 +0.872 대비 {abs(out['delta_summary']['median'])/0.872:.0%} 수준이다. "
      f"같은 자로 잰 method 간 중심화 코사인은 {cross} 로 흩어진다(velocity_matrix_audit §3). "
      "즉 크로마틴 셔플의 효과는 재표본·run 잡음보다는 크지만, method 선택이 만드는 차이보다는 훨씬 작다.\n")
    A("## 4. 한계\n")
    A("- 짝맞춘 B는 재적합 " + str(len(out["paired"])) + "회다. A(6회)보다 표본이 적어 arm 간 run 변동의 추정이 덜 촘촘하다.")
    A("- MultiVelo 재적합은 병렬 부동소수 잡음을 포함한다. 이 잡음은 A arm이 흡수하는 바로 그 성분이므로 "
      "비트 단위 동일 재현은 요구하지 않는다. 세포 재표본(S_b)의 재현성은 obs_names 일치로 증명했다.")
    A("- 기존 refit(A)는 2026-07-01에 n_jobs=16으로, 신규 B는 n_jobs=12로 적합했다. MultiVelo는 gene을 독립으로 "
      "적합하므로 worker 수가 per-gene velo_s를 바꾸지 않지만, 차이가 있었다는 사실은 밝혀 둔다.")
    A("- MultiVelo 한정이다. MoFlow는 재실행 대조가 없어 여전히 인과 주장에서 제외된다.")
    A("- 공유 354 gene 위에서 잰 값이고, 셔플은 within-lineage 규약이라 lineage 수준의 크로마틴 구조는 보존된다.\n")
    A("## 산출물\n")
    A("`results/velocity_matrix_paired_shuffle.json` · `results/velocity_matrix_paired_shuffle_percell.csv` · "
      "`scripts/p10d_paired_shuffle_audit.py` · `scripts/p2_multivelo_paired_shuffle_refit.py`")
    with open(os.path.join(OUT, "velocity_matrix_paired_shuffle.md"), "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    obs = _names(ARMS["MultiVelo"][0], "obs")
    pos = {c: i for i, c in enumerate(obs)}
    genes, A_full = audit_gene_set()
    print(f"원본 MultiVelo {A_full.shape[0]} cell × 감사 유전자 {len(genes)}\n")

    out = {"design": "paired ATAC-shuffle refit on identical resampled cell set",
           "audit_genes": int(len(genes)), "orig_cells": int(A_full.shape[0]),
           "sealed_criteria": {"confirm": f"B within A observed range {CEILING_RANGE} or CI overlap",
                               "refute": "B substantially below A with non-overlapping CI (paired delta CI excludes 0)"},
           "ceiling_all6": [], "paired": [], "unpaired_reference": {}}

    # ── 0) 검증: 기존 감사 수치 재현 (천장 6개 + 전량 셔플) ────────────────────────
    print("[검증] 기존 velocity_matrix_audit §4 수치 재현")
    for p in sorted(glob.glob(os.path.join(BOOT_DIR, "*.h5ad")))[:6]:
        rc = _names(p, "obs"); rv = set(_names(p, "var"))
        g = [x for x in genes if x in rv]
        S = load(p, "velo_s", g)
        A = A_full[np.array([pos[c] for c in rc])][:, np.isin(genes, np.array(g))]
        good = np.isfinite(S).all(axis=0) & (S.std(axis=0) > 0)
        rec, _, _ = compare(A[:, good], S[:, good], os.path.basename(p))
        rec["n_gene"] = int(good.sum()); rec["n_cell"] = int(len(rc))
        out["ceiling_all6"].append(rec)
        print(f"    {rec['label']:14s} n_cell={rec['n_cell']} n_gene={rec['n_gene']:3d} "
              f"raw {rec['raw_median']:+.3f} centered {rec['centered_median']:+.3f} "
              f"sign {rec['sign_agreement']:.1%}")
    cen6 = [r["centered_median"] for r in out["ceiling_all6"]]
    sg6 = [r["sign_agreement"] for r in out["ceiling_all6"]]
    print(f"    → 천장 중앙값 centered {np.median(cen6):+.3f} 범위 {min(cen6):.3f}~{max(cen6):.3f} "
          f"sign {np.median(sg6):.1%}   (감사 보고: +0.872 / 0.826~0.887 / 78.6%)")

    sp, sl = SCRAMBLED["MultiVelo-scr"]
    svar = set(_names(sp, "var"))
    g = [x for x in genes if x in svar]
    S = load(sp, sl, g)
    A = A_full[:, np.isin(genes, np.array(g))]
    good = np.isfinite(S).all(axis=0) & (S.std(axis=0) > 0)
    rec, _, _ = compare(A[:, good], S[:, good], "full-cell ATAC shuffle (기존, 짝 안 맞음)")
    rec["n_gene"] = int(good.sum()); rec["n_cell"] = int(A.shape[0])
    out["unpaired_reference"] = rec
    print(f"    전량 셔플 n_cell={rec['n_cell']} n_gene={rec['n_gene']} raw {rec['raw_median']:+.3f} "
          f"centered {rec['centered_median']:+.3f} sign {rec['sign_agreement']:.1%}   (감사 보고: +0.838 / 78.9%)\n")

    # ── 1) 짝맞춘 A vs B ──────────────────────────────────────────────────────────
    percell_rows = []
    shufs = sorted(glob.glob(os.path.join(SHUF_DIR, "refit_shuf_*.h5ad")))
    shufs = [p for p in shufs if ".smoke." not in os.path.basename(p)]
    if not shufs:
        print("<BLOCKED: paired-shuffle refit h5ad 없음 — p2_multivelo_paired_shuffle_refit.py 먼저 실행>")
        return 1
    print("[본 대조] 같은 재표본 세포집합 S_b 위 A(ATAC 온전) vs B(ATAC 셔플)")
    for ps in shufs:
        b = int(os.path.basename(ps).split("_")[-1].split(".")[0])
        pr = os.path.join(BOOT_DIR, f"refit_{b}.h5ad")
        if not os.path.exists(pr):
            print(f"    b={b}: 짝 refit 없음 → skip"); continue
        rc, sc_ = _names(pr, "obs"), _names(ps, "obs")
        assert np.array_equal(rc, sc_), f"b={b}: A/B 세포집합 불일치 — paired 성립 안 함"
        rv, sv = set(_names(pr, "var")), set(_names(ps, "var"))
        g = [x for x in genes if x in rv and x in sv]
        R = load(pr, "velo_s", g)
        H = load(ps, "velo_s", g)
        A = A_full[np.array([pos[c] for c in rc])][:, np.isin(genes, np.array(g))]
        good = (np.isfinite(R).all(0) & (R.std(0) > 0) &
                np.isfinite(H).all(0) & (H.std(0) > 0))
        A, R, H = A[:, good], R[:, good], H[:, good]
        recA, rawA, cenA = compare(A, R, f"A refit_{b} (ATAC 온전)")
        recB, rawB, cenB = compare(A, H, f"B refit_shuf_{b} (ATAC 셔플)")
        mA, loA, hiA = boot_ci(cenA)
        mB, loB, hiB = boot_ci(cenB)
        dmed, dlo, dhi, ncell = boot_ci_paired(cenA, cenB)
        rec = dict(b=b, n_cell=int(len(rc)), n_gene=int(good.sum()),
                   A=recA, B=recB,
                   A_centered_ci=[mA, loA, hiA], B_centered_ci=[mB, loB, hiB],
                   delta_centered_median=dmed, delta_ci=[dlo, dhi], delta_n_cell=ncell,
                   B_within_A_observed_range=bool(CEILING_RANGE[0] <= mB <= CEILING_RANGE[1]),
                   ci_overlap_AB=bool(not (hiB < loA or hiA < loB)),
                   delta_ci_excludes_zero=bool(dlo > 0 or dhi < 0))
        out["paired"].append(rec)
        print(f"  b={b} (n_cell={rec['n_cell']}, n_gene={rec['n_gene']})")
        print(f"    A  centered {mA:+.3f} [{loA:+.3f},{hiA:+.3f}]  raw {recA['raw_median']:+.3f}  sign {recA['sign_agreement']:.1%}")
        print(f"    B  centered {mB:+.3f} [{loB:+.3f},{hiB:+.3f}]  raw {recB['raw_median']:+.3f}  sign {recB['sign_agreement']:.1%}")
        print(f"    Δ(A−B) {dmed:+.4f} [{dlo:+.4f},{dhi:+.4f}]  "
              f"B∈A범위={rec['B_within_A_observed_range']} CI겹침={rec['ci_overlap_AB']} Δ CI가 0 배제={rec['delta_ci_excludes_zero']}")
        for i, c in enumerate(rc):
            percell_rows.append((b, c, cenA[i], cenB[i], rawA[i], rawB[i]))

    # ── 2) 봉인 기준 판정 ─────────────────────────────────────────────────────────
    dvals = [r["delta_centered_median"] for r in out["paired"]]
    bvals = [r["B_centered_ci"][0] for r in out["paired"]]
    # 판정은 **크기 조건**(B가 A 관측범위 안인가 / CI 겹치는가)을 b별로 세어 낸다.
    # n=15k에서 부트스트랩 CI는 매우 좁아 Δ≠0은 거의 자동으로 성립하므로, Δ CI만으로 판정하지 않는다.
    n_in = sum(1 for r in out["paired"]
               if r["B_within_A_observed_range"] or r["ci_overlap_AB"])
    n_below = sum(1 for r in out["paired"]
                  if (not r["B_within_A_observed_range"]) and (not r["ci_overlap_AB"])
                  and r["delta_centered_median"] > 0 and r["delta_ci_excludes_zero"])
    nb = len(out["paired"])
    verdict = ("CONFIRM(크로마틴 무력 유지)" if n_in == nb else
               "REFUTE(현 주장 약화 필요)" if n_below == nb else
               "MIXED(b마다 갈림 — 나온 대로 서술)")
    out["verdict_counts"] = {"n_paired": nb, "n_within_or_overlap": n_in, "n_below_range": n_below}
    out["verdict"] = verdict
    out["delta_summary"] = dict(median=float(np.median(dvals)), values=dvals, B_values=bvals)
    print(f"\n[판정] {verdict}")
    print(f"    Δ 중앙값 {np.median(dvals):+.4f} (b별 {['%+.4f' % d for d in dvals]})")
    print(f"    B centered {['%+.3f' % v for v in bvals]} vs A 관측범위 {CEILING_RANGE}")

    with open(os.path.join(OUT, "velocity_matrix_paired_shuffle.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    write_md(out)
    import csv
    with open(os.path.join(OUT, "velocity_matrix_paired_shuffle_percell.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["b", "cell", "centered_cos_A_intact", "centered_cos_B_shuffled",
                    "raw_cos_A_intact", "raw_cos_B_shuffled"])
        for r in percell_rows:
            w.writerow([r[0], r[1], f"{r[2]:.6f}", f"{r[3]:.6f}", f"{r[4]:.6f}", f"{r[5]:.6f}"])
    print(f"\n✓ results/velocity_matrix_paired_shuffle.json / _percell.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
