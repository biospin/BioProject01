#!/usr/bin/env python
"""MoFlow run-to-run null 감사 — 층② 세포x유전자 velocity 행렬 MAJOR-1 해소 (공격지점 (1)).

문제: `velocity_matrix_audit.md`의 근접-0 세 쌍(MV×MoFlow -0.012, MoFlow×CRAK-Velo +0.003,
     MoFlow×MultiVeloVAE +0.003, 전부 `cell_cos_excess` 필드)은 전부 MoFlow가 낀 쌍이고,
     MoFlow는 같은 설정 재실행 대조가 없어 이 값이 method 간 실제 불일치인지 MoFlow 한 arm의
     내부 불안정인지 구분되지 않는다(REVIEW-GB-2026-07-19b MAJOR-1 (1)). MoFlow 원본×ATAC-shuffle
     중심화 코사인(+0.113, `velocity_matrix_audit.md` §6)도 같은 이유로 해석 불가로 남아 있다.
해결: `p2_moflow_runtorun_refit.py`가 만든 독립 재실행(run1, run2 ...)을 원본 MoFlow(A)와 같은 자
     (세포 부트스트랩 B=1000, seed=20260719)로 비교해 **MoFlow 자신의 재현성 천장**을 잰다.
     MultiVelo의 재현성 천장(+0.826~+0.887, `velocity_matrix_audit.md` §4)과 구조적으로 동일한
     대조이나, 세포 bootstrap이 아니라 독립 재실행이 축이다(설계 근거는 `p2_moflow_runtorun_refit.py`
     docstring 참조).

판정 기준은 실행 전 봉인(중심화 코사인 기준 — 원 매트릭스 §4 재현성 천장과 동일 지표):
  · MOFLOW-REPRODUCIBLE (근접-0 쌍이 arm 불안정으로 설명되지 않음) =
      가장 보수적인 run의 lower CI(천장) > 근접-0 세 쌍의 중심화 코사인 |값| 최댓값
  · MOFLOW-NOT-SEPARABLE (근접-0 쌍이 여전히 arm 불안정과 분리 불가) =
      천장 CI가 그 임계 이하이거나 0을 포함

실행: conda run -n scv-preprocess python scripts/p10g_moflow_runtorun_null_audit.py
출력: results/moflow_runtorun_null.md / .json (신규 격리 — velocity_matrix_audit.* / FINDINGS.md /
      draft 는 읽기만 하고 건드리지 않는다)
"""
import glob
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p10_velocity_matrix_audit import (ARMS, SCRAMBLED, _names, cos_rows, load,
                                       sign_agreement, OUT, V, SEED, B_BOOT)
from p10d_paired_shuffle_audit import audit_gene_set, boot_ci

RR_DIR = os.path.join(V, "moflow_runtorun")
AUDIT_JSON = os.path.join(OUT, "velocity_matrix_audit.json")   # 읽기 전용 — 근접-0 세 쌍 원값
NEAR_ZERO_PAIRS = ["MultiVelo × MoFlow", "MoFlow × CRAK-Velo", "MoFlow × MultiVeloVAE"]


def moflow_audit_gene_set():
    """p10d.audit_gene_set() 과 동일 gene 축(5-arm 교집합 + 유한/분산>0),
    단 원본 행렬은 MultiVelo가 아니라 MoFlow 자신을 반환한다."""
    genes, _ = audit_gene_set()
    A_full = load(ARMS["MoFlow"][0], "velo_s", list(genes))
    return genes, A_full


def centered_cos(A, B):
    """세포 공통 평균 벡터를 뺀 뒤 세포별 코사인(velocity_matrix_audit.md §4 지표와 동일 정의)."""
    Ac = A - A.mean(axis=0, keepdims=True)
    Bc = B - B.mean(axis=0, keepdims=True)
    return cos_rows(Ac, Bc)


def raw_excess_vs_null(A, B, rng):
    """원척도 코사인의 세포-셔플 null 대비 초과분(velocity_matrix_audit.md §3 `cell_cos_excess`와 동일 정의)."""
    craw = cos_rows(A, B)
    med = float(np.nanmedian(craw))
    perm = rng.permutation(B.shape[0])
    null = float(np.nanmedian(cos_rows(A, B[perm])))
    return med, null, med - null


def read_near_zero_pairs():
    """velocity_matrix_audit.json 의 근접-0 세 쌍을 읽기만 한다(재계산 아님) — cell_cos_excess 필드."""
    if not os.path.exists(AUDIT_JSON):
        return {}
    with open(AUDIT_JSON) as f:
        d = json.load(f)
    return {r["pair"]: r["cell_cos_excess"] for r in d.get("pairs", []) if r.get("pair") in NEAR_ZERO_PAIRS}


def recompute_near_zero_centered(genes):
    """근접-0 세 쌍의 중심화 코사인을 5-arm 공유 gene 축 위에서 직접 재계산한다
    (velocity_matrix_audit.md §4 는 stdout 캡처본이라 tracked json이 없다 — p10b 정의 그대로 재현)."""
    mats = {k: load(p, l, list(genes)) for k, (p, l) in ARMS.items()}
    ok = np.ones(len(genes), bool)
    for M in mats.values():
        ok &= np.isfinite(M).all(axis=0) & (np.nanstd(M, axis=0) > 0)
    mats = {k: M[:, ok] for k, M in mats.items()}
    pairs = {"MultiVelo × MoFlow": ("MultiVelo", "MoFlow"),
             "MoFlow × CRAK-Velo": ("MoFlow", "CRAK-Velo"),
             "MoFlow × MultiVeloVAE": ("MoFlow", "MultiVeloVAE")}
    return {name: float(np.nanmedian(centered_cos(mats[a], mats[b]))) for name, (a, b) in pairs.items()}


def recompute_shuffle_delta(genes, A_full, ok_mask):
    """원본×MoFlow-scr 중심화 코사인 재계산 — 봉인값 +0.113(velocity_matrix_audit.md §6) 재현 확인."""
    p_scr, layer = SCRAMBLED["MoFlow-scr"]
    if not os.path.exists(p_scr):
        return None
    B = load(p_scr, layer, list(genes))
    good = ok_mask & np.isfinite(B).all(0) & (np.nanstd(B, 0) > 0)
    m, lo, hi = boot_ci(centered_cos(A_full[:, good], B[:, good]))
    return dict(centered_median=m, ci=[lo, hi], n_gene=int(good.sum()))


def write_md(out):
    L = []; A = L.append
    A("# MoFlow run-to-run null — 세포·ATAC 고정, 독립 재실행만 반복\n")
    A("> 생성 = `scripts/p10g_moflow_runtorun_null_audit.py` "
      "(fit = `scripts/p2_moflow_runtorun_refit.py`).")
    A("> 신규 격리 산출물이다. `velocity_matrix_audit.*` · `scrambled_null_moflow.md` · `FINDINGS.md` · "
      "draft 는 읽기만 하고 건드리지 않는다.\n")
    A("## 0. 무엇을 재는가\n")
    A("층② 세포x유전자 velocity 행렬 감사에서 MoFlow가 낀 근접-0 세 쌍은 method 간 실제 불일치인지 "
      "MoFlow 한 arm의 내부 불안정인지 구분되지 않았다(REVIEW-GB-2026-07-19b MAJOR-1). MultiVelo가 이미 "
      "가진 재현성 천장(재표본 재적합 대비 +0.826~+0.887)의 대응물을, MoFlow는 세포 bootstrap이 없으므로 "
      "**동일 입력 독립 재실행**으로 잰다.\n")
    A("## 1. 근접-0 세 쌍 원값 (재계산 아님, 대조용)\n")
    A("| pair | cell_cos_excess (원값, `velocity_matrix_audit.json`) | 중심화 코사인 (재계산) |")
    A("|---|---|---|")
    nz, nzc = out["near_zero_pairs_raw_excess"], out["near_zero_pairs_centered"]
    for pair in NEAR_ZERO_PAIRS:
        A(f"| {pair} | {nz.get(pair, float('nan')):+.4f} | {nzc.get(pair, float('nan')):+.4f} |")
    A("")
    A("## 2. MoFlow 재현성 천장 (원본 vs 독립 재실행)\n")
    A("| run | n_cell | n_gene | 중심화 코사인 [95% CI] | raw 중앙값 | 세포-셔플 null | raw 초과분 | 부호일치 |")
    A("|---|---|---|---|---|---|---|---|")
    for r in out["runs"]:
        m, lo, hi = r["centered_ci"]
        A(f"| {r['run']} | {r['n_cell']} | {r['n_gene']} | {m:+.4f} [{lo:+.4f}, {hi:+.4f}] | "
          f"{r['raw_median']:+.4f} | {r['raw_null']:+.4f} | {r['raw_excess']:+.4f} | {r['sign_agreement']:.1%} |")
    A("")
    if "run1_vs_run2" in out:
        r12 = out["run1_vs_run2"]
        m, lo, hi = r12["centered_ci"]
        A(f"run1 대 run2(원본을 거치지 않은 직접 비교, n_gene={r12['n_gene']}): "
          f"중심화 코사인 {m:+.4f} [{lo:+.4f}, {hi:+.4f}]\n")
    A("## 3. 셔플 Δ 재계산 (봉인 수치 재현)\n")
    sh = out.get("shuffle_recompute")
    if sh:
        A(f"원본×MoFlow-scr 중심화 코사인 재계산 {sh['centered_median']:+.4f} "
          f"[{sh['ci'][0]:+.4f}, {sh['ci'][1]:+.4f}] (n_gene={sh['n_gene']}) — "
          f"봉인 보고 +0.113(`velocity_matrix_audit.md` §6)과 대조.\n")
    else:
        A("moflow_scrambled.h5ad 없음 — 셔플 대조 skip.\n")
    A("## 4. 판정 대비 봉인 기준\n")
    A(f"**{out['verdict']}**\n")
    vc = out["verdict_checks"]
    A(f"- 가장 보수적인 run의 lower CI(천장) {vc['min_lower_ci_ceiling']:+.4f} vs "
      f"근접-0 세 쌍 중심화 코사인 |값| 최댓값 {vc['near_zero_threshold']:.4f} → {vc['passes']}\n")
    A("## 5. 한계\n")
    A("- 재실행 축만 쟀다. MultiVelo 처럼 세포 재표본까지 곱한 이중 축은 MoFlow에 없다(전체 세포 단일 fit "
      "구조이므로 bootstrap 축 자체가 성립하지 않는다).")
    A("- run 수는 2로 적다. 분산 추정의 정밀도는 MultiVelo의 6-refit 천장보다 낮다.")
    A("- 이 감사는 `velo_s`(cell x gene velocity 행렬) 축만 본다. DTW c-s lag(`cs_lag_median`) 축의 "
      "재현성 상한은 별도이며 `scrambled_null_moflow.md` §4의 유보가 그대로 유효하다.")
    A("- 판정은 중심화 코사인 기준으로 봉인했다. raw 초과분(§1~2 표)은 대조용으로만 병기한다.\n")
    A("## 산출물\n")
    A("`results/moflow_runtorun_null.json` · `scripts/p10g_moflow_runtorun_null_audit.py` · "
      "`scripts/p2_moflow_runtorun_refit.py`")
    with open(os.path.join(OUT, "moflow_runtorun_null.md"), "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    genes, A_full = moflow_audit_gene_set()
    print(f"MoFlow 원본 {A_full.shape[0]} cell x 감사 유전자 {len(genes)}\n")

    rr_paths = sorted(p for p in glob.glob(os.path.join(RR_DIR, "moflow_rr_run*.h5ad"))
                      if ".smoke." not in os.path.basename(p))
    if not rr_paths:
        print("<BLOCKED: moflow run-to-run h5ad 없음 — p2_moflow_runtorun_refit.py 먼저 실행>")
        return 1

    rng = np.random.default_rng(SEED)
    out = {"design": "MoFlow run-to-run null: identical full-cohort input, ATAC intact, "
                     "independent re-run only",
           "audit_genes": int(len(genes)), "orig_cells": int(A_full.shape[0]),
           "sealed_criteria": {
               "moflow_reproducible": "min-over-runs lower CI(centered ceiling) > "
                                      "max |near-zero pair centered cosine|",
               "moflow_not_separable": "ceiling CI touches or falls below that threshold, or includes 0"},
           "near_zero_pairs_raw_excess": read_near_zero_pairs(),
           "near_zero_pairs_centered": recompute_near_zero_centered(genes),
           "runs": []}

    obs_ref = None
    ceilings = []
    for p in rr_paths:
        m = re.search(r"moflow_rr_run(\d+)\.h5ad$", os.path.basename(p))
        run = int(m.group(1))
        rv = set(_names(p, "var"))
        g = [x for x in genes if x in rv]
        R = load(p, "velo_s", g)
        Asub = A_full[:, np.isin(genes, np.array(g))]
        good = (np.isfinite(Asub).all(0) & (np.nanstd(Asub, 0) > 0) &
                np.isfinite(R).all(0) & (np.nanstd(R, 0) > 0))
        Ag, Rg = Asub[:, good], R[:, good]
        m_, lo, hi = boot_ci(centered_cos(Ag, Rg))
        raw_med, raw_null, raw_excess = raw_excess_vs_null(Ag, Rg, rng)
        sa, n_used, n_excl = sign_agreement(Ag, Rg)
        obs_here = _names(p, "obs")
        same_cells = bool(np.array_equal(obs_here, obs_ref)) if obs_ref is not None else None
        obs_ref = obs_here if obs_ref is None else obs_ref
        rec = dict(run=run, n_gene=int(good.sum()), n_cell=int(R.shape[0]),
                   same_cells_as_first_run=same_cells,
                   centered_ci=[m_, lo, hi], raw_median=raw_med, raw_null=raw_null,
                   raw_excess=raw_excess, sign_agreement=sa)
        out["runs"].append(rec)
        ceilings.append((m_, lo, hi))
        print(f"  run={run}: 중심화 코사인 {m_:+.4f} [{lo:+.4f},{hi:+.4f}] (n_gene={rec['n_gene']}, "
              f"n_cell={rec['n_cell']}, 부호일치={sa:.1%}, raw 초과분={raw_excess:+.4f})")

    if len(rr_paths) >= 2:
        p1, p2 = rr_paths[0], rr_paths[1]
        v1, v2 = set(_names(p1, "var")), set(_names(p2, "var"))
        g12 = [x for x in genes if x in v1 and x in v2]
        R1, R2 = load(p1, "velo_s", g12), load(p2, "velo_s", g12)
        good = (np.isfinite(R1).all(0) & (np.nanstd(R1, 0) > 0) &
                np.isfinite(R2).all(0) & (np.nanstd(R2, 0) > 0))
        m12, lo12, hi12 = boot_ci(centered_cos(R1[:, good], R2[:, good]))
        out["run1_vs_run2"] = dict(n_gene=int(good.sum()), centered_ci=[m12, lo12, hi12])
        print(f"  run1 vs run2 (원본 미경유 직접 비교): 중심화 코사인 {m12:+.4f} [{lo12:+.4f},{hi12:+.4f}]")

    ok_mask = np.isfinite(A_full).all(0) & (np.nanstd(A_full, 0) > 0)
    out["shuffle_recompute"] = recompute_shuffle_delta(genes, A_full, ok_mask)

    lo_min = min(c[1] for c in ceilings)
    nzc_vals = [v for v in out["near_zero_pairs_centered"].values() if v is not None]
    threshold = max(abs(v) for v in nzc_vals) if nzc_vals else float("nan")
    passes = bool(lo_min > threshold)
    verdict = ("MOFLOW-REPRODUCIBLE (근접-0 쌍은 arm 불안정으로 설명 안 됨)" if passes
               else "MOFLOW-NOT-SEPARABLE (근접-0 쌍이 여전히 arm 불안정과 분리 불가)")
    out["verdict"] = verdict
    out["verdict_checks"] = dict(min_lower_ci_ceiling=lo_min, near_zero_threshold=threshold, passes=passes)
    print(f"\n[판정] {verdict}")
    print(f"    min lower CI(천장)={lo_min:+.4f} vs 근접-0 쌍 중심화 코사인 |값| 최댓값={threshold:.4f}")

    with open(os.path.join(OUT, "moflow_runtorun_null.json"), "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    write_md(out)
    print("\n✓ results/moflow_runtorun_null.json / .md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
