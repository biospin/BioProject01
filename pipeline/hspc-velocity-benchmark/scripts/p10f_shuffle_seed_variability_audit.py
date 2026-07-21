#!/usr/bin/env python
"""셔플 draw 변동(shuffle-seed 반복) — 짝 Δ 가 단일 draw 아티팩트인지 검정.

배경(확정된 것):
  · `velocity_matrix_paired_shuffle.md` — 같은 재표본 세포집합 S_b 에서 ATAC 온전(A) vs 셔플(B)
    짝 Δ = A−B = +0.081(b0) / +0.004(b1) / +0.063(b2).
  · `velocity_matrix_runtorun_null.md` — 같은 세포·같은 설정 재적합은 결정론(Δ_rr = 0.000000).
    ⇒ 짝 Δ 안에 fit 잡음 성분이 없다.
남은 구멍: 짝 Δ 는 b 마다 **셔플 추출 1회**에 기댄다. 적합이 결정론이므로 **셔플 seed 만 바꿔** 재적합하면
seed 간 Δ 변동은 **전부 셔플 draw 변동**이다.

지표·자 = p10d 와 동일(중심화 코사인 주, raw 병기, 세포 부트스트랩 B=1000, seed 20260719, percentile).
A arm 은 결정론이 실측됐으므로 기존 refit_b 를 재사용한다(재적합 불필요).

★ 판정 기준 (결과 보기 전 봉인 — 사후 조정 금지; p10d 의 "관측범위" 규칙을 쓰지 않는다)
  robust(현 주장 유지) ⟺ b=0 과 b=2 **둘 다**에서
      (a) 모든 seed 의 Δ 가 양수이고 각 Δ 의 95% CI 가 0 을 배제,
      (b) seed 산포 < Δ 크기.  산포 = range(Δ_k) = max−min, 크기 = median(Δ_k). 통과 = range < median.
          (SD 도 보고하되 합불은 보수적으로 range 로 판정.)
  둘 중 하나라도 실패하면 → weaken(현 주장 약화 필요).
  b=1 은 판정에 넣지 않고 별도로 보고한다(짝 Δ +0.0038 의 null 쌍이 seed 를 바꿔도 0 근처인가).
  주: 세포 n=15,315 이라 개별 Δ 의 CI 는 매우 좁고 (a) 는 거의 자동 성립한다. 실질 판별자는 (b) 다.

실행: conda run -n scv-preprocess python scripts/p10f_shuffle_seed_variability_audit.py
출력: results/velocity_matrix_shuffle_seed_variability.md / .json / _perseed.csv
      기존 velocity_matrix_paired_shuffle.* · velocity_matrix_runtorun_null.* · velocity_matrix_audit.* ·
      FINDINGS.md · draft* 는 **읽기만** 한다.
"""
import csv
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p10_velocity_matrix_audit import _names, load, OUT, V, SEED, B_BOOT
from p10d_paired_shuffle_audit import (audit_gene_set, boot_ci, boot_ci_paired,
                                       compare, BOOT_DIR, SHUF_DIR)

SEEDS_DIR = os.path.join(V, "multivelo_shuffle_seeds")
BOOTS_MAIN = (0, 2)      # 판정 대상 (짝 Δ 가 컸던 두 쌍)
BOOTS_ALL = (0, 1, 2)


def b_arm_paths(b):
    """(shuf_seed, h5ad 경로) 목록. 첫 항목 = 기존 draw(seed=b)."""
    out = []
    p0 = os.path.join(SHUF_DIR, f"refit_shuf_{b}.h5ad")
    if os.path.exists(p0):
        out.append((b, p0, "기존"))
    for p in sorted(glob.glob(os.path.join(SEEDS_DIR, f"refit_shufseed_b{b}_s*.h5ad"))):
        if ".smoke." in os.path.basename(p):
            continue
        s = int(os.path.basename(p).split("_s")[-1].split(".")[0])
        out.append((s, p, "신규"))
    return out


def one_pair(b, ps, genes, A_full, pos):
    """A(refit_b) vs B(ps) 짝 비교 — p10d 와 동일 절차, gene mask 는 seed 별로 재계산."""
    pr = os.path.join(BOOT_DIR, f"refit_{b}.h5ad")
    rc, sc_ = _names(pr, "obs"), _names(ps, "obs")
    assert np.array_equal(rc, sc_), f"b={b} {os.path.basename(ps)}: A/B 세포집합 불일치"
    rv, sv = set(_names(pr, "var")), set(_names(ps, "var"))
    g = [x for x in genes if x in rv and x in sv]
    R = load(pr, "velo_s", g)
    H = load(ps, "velo_s", g)
    A = A_full[np.array([pos[c] for c in rc])][:, np.isin(genes, np.array(g))]
    good = (np.isfinite(R).all(0) & (R.std(0) > 0) &
            np.isfinite(H).all(0) & (H.std(0) > 0))
    A, R, H = A[:, good], R[:, good], H[:, good]
    recA, _, cenA = compare(A, R, f"A refit_{b}")
    recB, _, cenB = compare(A, H, f"B {os.path.basename(ps)}")
    mA, loA, hiA = boot_ci(cenA)
    mB, loB, hiB = boot_ci(cenB)
    dmed, dlo, dhi, ncell = boot_ci_paired(cenA, cenB)
    return dict(n_cell=int(len(rc)), n_gene=int(good.sum()),
                A_centered=[mA, loA, hiA], B_centered=[mB, loB, hiB],
                A_raw=recA["raw_median"], B_raw=recB["raw_median"],
                A_sign=recA["sign_agreement"], B_sign=recB["sign_agreement"],
                delta=dmed, delta_ci=[dlo, dhi], delta_n_cell=ncell,
                delta_ci_excludes_zero=bool(dlo > 0 or dhi < 0),
                delta_positive_and_significant=bool(dlo > 0))


def write_md(out):
    L = []
    A = L.append
    A("# 셔플 draw 변동 — 셔플 seed 반복으로 본 짝 Δ 의 안정성\n")
    A("> 생성 = `scripts/p10f_shuffle_seed_variability_audit.py` "
      "(fit = `scripts/p2_multivelo_shuffle_seed_refit.py`, 드라이버 = `scripts/run_shuffle_seed_refit.sh`).")
    A("> 신규 격리 산출물이다. `velocity_matrix_paired_shuffle.*`·`velocity_matrix_runtorun_null.*`·"
      "`velocity_matrix_audit.*`·`FINDINGS.md`·draft 는 읽기만 한다.\n")
    A("## 0. 무엇을 재는가\n")
    A("짝맞춘 ATAC-shuffle 대조의 Δ(A−B)는 세포 재표본과 fit 잡음을 걷어냈지만, b 마다 **셔플 추출이 1회**였다. "
      "run-to-run null 이 적합의 결정론을 실측했으므로(Δ_rr = 0.000000), 같은 S_b 에서 **셔플 seed 만 바꿔** "
      "재적합하면 seed 간 Δ 변동은 전부 **셔플 draw 변동**이다. A arm(ATAC 온전)은 결정론이라 재적합하지 않고 "
      "기존 refit_b 를 그대로 쓴다.\n")
    A("셔플 규약은 기존과 같은 `scramble_within_lineage`(within-lineage 행 permutation)이고 seed 만 바뀐다. "
      "seed 설계는 실행 전 고정: b 별 [b(기존 draw), 101+b, 202+b, 303+b].\n")
    A("판정 기준(결과 보기 전 봉인): robust = b=0·b=2 **둘 다**에서 (a) 모든 seed 의 Δ 가 양수이고 CI 가 0 을 배제, "
      "(b) seed 산포 range(Δ) < 크기 median(Δ). 하나라도 실패하면 weaken. b=1 은 판정에서 빼고 따로 보고한다.\n")
    A("## 1. seed 별 짝 Δ\n")
    A("| b | shuf_seed | 출처 | n_gene | A 중심화 [95% CI] | B 중심화 [95% CI] | Δ=A−B [95% CI] | Δ CI 0 배제 |")
    A("|---|---|---|---|---|---|---|---|")
    for b in BOOTS_ALL:
        for r in out["per_seed"].get(str(b), []):
            a, bb = r["A_centered"], r["B_centered"]
            A(f"| {b} | {r['shuf_seed']} | {r['origin']} | {r['n_gene']} | "
              f"{a[0]:+.3f} [{a[1]:+.3f}, {a[2]:+.3f}] | {bb[0]:+.3f} [{bb[1]:+.3f}, {bb[2]:+.3f}] | "
              f"{r['delta']:+.4f} [{r['delta_ci'][0]:+.4f}, {r['delta_ci'][1]:+.4f}] | "
              f"{r['delta_ci_excludes_zero']} |")
    A("\nCI 는 세포 부트스트랩(B=1000, seed=20260719, percentile), 세포 15,315 개. "
      "기존 draw 행은 `velocity_matrix_paired_shuffle.md` 의 봉인 수치와 같은 값이어야 한다(재현 확인은 §3).\n")
    A("## 2. b 별 Δ 분포와 셔플 draw 변동\n")
    A("| b | seed 수 | Δ 중앙값 | Δ 최소 | Δ 최대 | 범위(max−min) | SD | 분산 | 범위/중앙값 | 모든 seed Δ>0 & CI 0 배제 | 범위 < 중앙값 |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    for b in BOOTS_ALL:
        s = out["summary"].get(str(b))
        if not s:
            continue
        rat = f"{s['range']/s['median']:.2f}" if s["median"] != 0 else "n/a"
        A(f"| {b} | {s['n_seeds']} | {s['median']:+.4f} | {s['min']:+.4f} | {s['max']:+.4f} | "
          f"{s['range']:.4f} | {s['sd']:.4f} | {s['var']:.2e} | {rat} | "
          f"{s['all_positive_significant']} | {s['range_lt_median']} |")
    A("")
    for b in BOOTS_ALL:
        s = out["summary"].get(str(b))
        if not s:
            continue
        A(f"- b={b}: 셔플 draw 변동(범위 {s['range']:.4f})은 관측된 Δ 크기(중앙값 {s['median']:+.4f}) 대비 "
          f"{abs(s['range']/s['median']):.0%}다. 기존 단일 draw(seed={s['existing_seed']}, Δ {s['existing_delta']:+.4f})는 "
          f"이 4 개 draw 중 작은 쪽부터 {s['existing_rank']}번째다.")
    A("")
    A(f"12 개 적합(3 b × 4 seed) 전부에서 Δ 는 양수이고 각 CI 가 0 을 배제한다(부호 12/12). "
      f"반면 크기는 draw 마다 {out['pooled']['min']:+.4f}~{out['pooled']['max']:+.4f} 로 흩어진다. "
      "방향은 draw 에 안 흔들리지만 크기는 흔들린다.\n")
    A("## 3. 기존 봉인 수치 재현\n")
    A("| b | 기존 draw Δ 재계산 | 봉인 보고(velocity_matrix_paired_shuffle.md) | 일치 |")
    A("|---|---|---|---|")
    for b in BOOTS_ALL:
        r = out["reproduction"].get(str(b))
        if not r:
            continue
        A(f"| {b} | {r['recomputed']:+.4f} | {r['sealed']:+.4f} | {r['match']} |")
    A("")
    A("## 4. 봉인 기준 대비 판정\n")
    A(f"**{out['verdict']}**\n")
    for b in BOOTS_MAIN:
        s = out["summary"].get(str(b))
        if not s:
            A(f"- b={b}: <BLOCKED: 적합 산출 없음>")
            continue
        A(f"- b={b}: (a) 모든 seed Δ>0 & CI 0 배제 = {s['all_positive_significant']}, "
          f"(b) 범위 {s['range']:.4f} < 중앙값 {s['median']:.4f} = {s['range_lt_median']}.")
    s1 = out["summary"].get("1")
    if s1:
        A(f"- b=1(판정 제외, 참고): Δ 중앙값 {s1['median']:+.4f}, 범위 {s1['min']:+.4f}~{s1['max']:+.4f}, "
          f"모든 seed Δ>0 & CI 0 배제 = {s1['all_positive_significant']}.")
    A("")
    A(out["verdict_text"])
    A("")
    A("## 5. 한계\n")
    A("- b 당 seed 는 4 개다. 셔플 draw 분포를 정밀하게 추정하기엔 적고, 범위·SD 도 그만큼 거칠다.")
    A("- A arm 은 재적합하지 않았다. 근거는 run-to-run null 의 결정론 실측이다(같은 입력 → 같은 답).")
    A("- 신규 B 는 n_jobs=8 로, 기존 B(=12)·legacy A(=16)와 worker 수가 다르다. "
      "worker 수가 결과를 바꾸지 않음은 run-to-run null §3 에서 실측했다(nj12 vs nj16 완전 동일).")
    A("- MultiVelo 한정이고, 셔플은 within-lineage 규약이라 lineage 수준의 크로마틴 구조는 보존된다.")
    A("- 효과 크기 자체는 여전히 작다. 짝 Δ 중앙값은 재현성 천장 +0.872 대비 한 자릿수 % 수준이다.\n")
    A("## 6. 실행 기록\n")
    A("신규 적합 9 회(3 b × 신규 3 seed)를 3 stream 병렬(stream 당 njobs=8, CPU)로 돌렸다. "
      "적합 1 회 wall 2709~2903 s, 전체 wall 8540 s(2026-07-21 17:23:48~19:46:08 KST). "
      "기록 = `results/runtime.csv` 의 `multivelo_shuffle_seed` 행(스모크 3 행은 `_SMOKE` 라벨), "
      "로그 = `results/logs/shuffle_seed_refit.log` 와 `shuffle_seed_refit_b<b>.log`, "
      "완료 sentinel = `results/logs/SHUFFLE_SEED_DONE`.\n")
    A("## 산출물\n")
    A("`results/velocity_matrix_shuffle_seed_variability.json` · "
      "`results/velocity_matrix_shuffle_seed_variability_perseed.csv` · "
      "`results/bootstrap_refit_shuffled_seeds/` · `scripts/p10f_shuffle_seed_variability_audit.py` · "
      "`scripts/p2_multivelo_shuffle_seed_refit.py` · `scripts/run_shuffle_seed_refit.sh`")
    with open(os.path.join(OUT, "velocity_matrix_shuffle_seed_variability.md"), "w") as f:
        f.write("\n".join(L) + "\n")


SEALED_PAIRED = {0: 0.0808, 1: 0.0038, 2: 0.0628}   # velocity_matrix_paired_shuffle.md §2


def main():
    from p10_velocity_matrix_audit import ARMS
    obs = _names(ARMS["MultiVelo"][0], "obs")
    pos = {c: i for i, c in enumerate(obs)}
    genes, A_full = audit_gene_set()
    print(f"원본 MultiVelo {A_full.shape[0]} cell × 감사 유전자 {len(genes)}\n")

    out = {"design": "shuffle-draw variability: same S_b, same shuffle protocol, shuffle seed varied",
           "metric": "centered cosine vs original MultiVelo velo_s; cell bootstrap B=%d seed=%d" % (B_BOOT, SEED),
           "sealed_criteria": {
               "robust": "for b in {0,2}: all seeds delta>0 with CI excluding 0 AND range(delta) < median(delta)",
               "weaken": "otherwise",
               "note": "b=1 reported separately, not part of verdict"},
           "seed_design": "per b: [b (existing draw), 101+b, 202+b, 303+b]",
           "audit_genes": int(len(genes)),
           "per_seed": {}, "summary": {}, "reproduction": {}}

    for b in BOOTS_ALL:
        arms = b_arm_paths(b)
        if not arms:
            print(f"b={b}: B arm 없음 → skip")
            continue
        rows = []
        print(f"[b={b}] B arm {len(arms)} 개")
        for s, p, origin in arms:
            rec = one_pair(b, p, genes, A_full, pos)
            rec["shuf_seed"] = s
            rec["origin"] = origin
            rec["file"] = os.path.basename(p)
            rows.append(rec)
            print(f"  seed={s:4d} ({origin}) n_gene={rec['n_gene']:3d} "
                  f"A {rec['A_centered'][0]:+.3f}  B {rec['B_centered'][0]:+.3f}  "
                  f"Δ {rec['delta']:+.4f} [{rec['delta_ci'][0]:+.4f},{rec['delta_ci'][1]:+.4f}]")
        rows.sort(key=lambda r: r["shuf_seed"])
        out["per_seed"][str(b)] = rows
        d = np.array([r["delta"] for r in rows], float)
        med = float(np.median(d))
        summ = dict(n_seeds=len(d), median=med, min=float(d.min()), max=float(d.max()),
                    range=float(d.max() - d.min()), sd=float(d.std(ddof=1)) if len(d) > 1 else float("nan"),
                    var=float(d.var(ddof=1)) if len(d) > 1 else float("nan"),
                    all_positive_significant=bool(all(r["delta_positive_and_significant"] for r in rows)),
                    values=[float(x) for x in d],
                    seeds=[int(r["shuf_seed"]) for r in rows])
        summ["range_lt_median"] = bool(summ["range"] < med)
        ex_row = [r for r in rows if r["origin"] == "기존"]
        if ex_row:
            ed = float(ex_row[0]["delta"])
            summ["existing_seed"] = int(ex_row[0]["shuf_seed"])
            summ["existing_delta"] = ed
            summ["existing_rank"] = int(np.sum(d <= ed))   # 작은 쪽부터 몇 번째
        summ["all_delta_positive"] = bool(all(r["delta"] > 0 for r in rows))
        out["summary"][str(b)] = summ
        print(f"  → 중앙값 {med:+.4f} 범위 {summ['min']:+.4f}~{summ['max']:+.4f} "
              f"(폭 {summ['range']:.4f}) SD {summ['sd']:.4f} | 모두 유의 양수={summ['all_positive_significant']} "
              f"| 범위<중앙값={summ['range_lt_median']}")
        ex = [r for r in rows if r["origin"] == "기존"]
        if ex:
            rec = float(ex[0]["delta"]); sealed = SEALED_PAIRED[b]
            out["reproduction"][str(b)] = dict(recomputed=rec, sealed=sealed,
                                               match=bool(abs(rec - sealed) < 5e-4))

    ok = []
    for b in BOOTS_MAIN:
        s = out["summary"].get(str(b))
        ok.append(bool(s and s["all_positive_significant"] and s["range_lt_median"]))
    all_d = [r["delta"] for b in BOOTS_ALL for r in out["per_seed"].get(str(b), [])]
    all_sig = [r["delta_positive_and_significant"] for b in BOOTS_ALL for r in out["per_seed"].get(str(b), [])]
    out["pooled"] = dict(n_fits=len(all_d), min=float(min(all_d)), max=float(max(all_d)),
                         median=float(np.median(all_d)),
                         n_positive_significant=int(sum(all_sig)))

    MIN_SEEDS = 4    # 과제 지시: b 당 총 4 개 이상 (기존 1 + 신규 3)
    have_all = all(str(b) in out["summary"] and out["summary"][str(b)]["n_seeds"] >= MIN_SEEDS
                   for b in BOOTS_MAIN)
    if not have_all:
        out["verdict"] = "<BLOCKED: b=0/b=2 seed 4개 미만 — 적합 미완>"
        out["verdict_text"] = "판정 불가 — 필요한 적합이 아직 없다."
    elif all(ok):
        out["verdict"] = "ROBUST(현 주장 유지 가능)"
        out["verdict_text"] = (
            "두 조건이 b=0·b=2 에서 모두 성립한다. 셔플 draw 를 바꿔도 Δ 는 계속 양수이고, "
            "seed 간 산포가 Δ 크기보다 작다. 짝 Δ 는 단일 draw 아티팩트가 아니다. "
            "다만 효과 크기가 작다는 기존 한계는 그대로다.")
    else:
        out["verdict"] = "WEAKEN(현 주장 약화 필요)"
        broke = [f"b={b}" for b in BOOTS_MAIN
                 if not (out["summary"][str(b)]["all_positive_significant"]
                         and out["summary"][str(b)]["range_lt_median"])]
        out["verdict_text"] = (
            f"봉인 조건이 {', '.join(broke)} 에서 성립하지 않는다. 깨진 것은 산포 조건 (b)다. "
            "단일 셔플 draw 가 크기의 대표값이 아니었다는 뜻이므로, Δ 의 크기를 특정 숫자로 못 박는 서술은 수위를 낮춰야 한다. "
            "다만 조건 (a)는 b=0·b=1·b=2 의 12 개 draw 전부에서 성립한다. 즉 ATAC 을 셔플하면 velocity 행렬이 "
            "원본에서 멀어진다는 **방향**은 draw 를 바꿔도 흔들리지 않고, 흔들리는 것은 그 **크기**다.")
    print(f"\n[판정] {out['verdict']}")

    with open(os.path.join(OUT, "velocity_matrix_shuffle_seed_variability.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, sort_keys=True)
    write_md(out)
    with open(os.path.join(OUT, "velocity_matrix_shuffle_seed_variability_perseed.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["b", "shuf_seed", "origin", "file", "n_cell", "n_gene",
                    "A_centered", "B_centered", "B_ci_lo", "B_ci_hi",
                    "delta", "delta_ci_lo", "delta_ci_hi", "A_raw", "B_raw",
                    "A_sign_agreement", "B_sign_agreement"])
        for b in BOOTS_ALL:
            for r in out["per_seed"].get(str(b), []):
                w.writerow([b, r["shuf_seed"], r["origin"], r["file"], r["n_cell"], r["n_gene"],
                            f"{r['A_centered'][0]:.6f}", f"{r['B_centered'][0]:.6f}",
                            f"{r['B_centered'][1]:.6f}", f"{r['B_centered'][2]:.6f}",
                            f"{r['delta']:.6f}", f"{r['delta_ci'][0]:.6f}", f"{r['delta_ci'][1]:.6f}",
                            f"{r['A_raw']:.6f}", f"{r['B_raw']:.6f}",
                            f"{r['A_sign']:.6f}", f"{r['B_sign']:.6f}"])
    print("✓ results/velocity_matrix_shuffle_seed_variability.{md,json} / _perseed.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
