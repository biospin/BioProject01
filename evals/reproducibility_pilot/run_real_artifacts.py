"""Real-artifact adapter — score the COMMITTED prereg scorecard, not a fixture.

    python3 run_real_artifacts.py

Fixtures prove the scorers are self-consistent. This proves they agree with the real
BIOP01 pipeline: it reads `results/prereg_gse205117_scorecard.csv`, applies the sealed
thresholds, and checks we reproduce the committed verdict (6 PASS / 0 FAIL).

READ-ONLY, stdlib-only, and deliberately NOT a recomputation:
  * it reads the scorecard's ρ/CI values — it does NOT refit velocity or recompute
    bootstrap concordance from results/*_genes.csv. Recomputation needs numpy/pandas/
    scipy + the velo-* pipeline envs, and "eval은 읽기만 한다"(작업 지시).
  * therefore this checks THRESHOLD APPLICATION, not the statistics themselves. If the
    committed ρ values were wrong, this would happily reproduce the wrong verdict.
    Recomputation belongs to the 채점기 itself (p3_prereg_gse205117.py), which is the
    layer that owns the bootstrap. See README §5.

CSV layout gotchas (verified against the committed file, 2026-07-17):
  * the `per_gene_disagree` row's `label` CONTAINS A COMMA inside quotes
    ("lag[MoFlow `cs_lag_median` (HSPC 원정의, 부호 유지)]|alpha") -> must use the csv
    module; `line.split(",")` shreds it.
  * that same row does NOT hold a ρ: it packs lag-disagree in `rho`, alpha-disagree in
    `lo`, and leaves `hi` EMPTY. Reading it as a correlation would be a category error.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

from scorers import SCORERS

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORECARD = REPO_ROOT / "pipeline/hspc-velocity-benchmark/results/prereg_gse205117_scorecard.csv"

# The committed verdict this adapter must reproduce — results/prereg_gse205117_scorecard.md
# ("종합: 6 PASS / 0 FAIL / 0 N/A", git 0367690/9eb0b76). Mapping of our scorer names to
# the sealed prediction numbers:
EXPECTED_COMMITTED = {
    "alpha_reproducibility": ("예측1 within cross-method α 재현", "pass"),
    "lag_fragility": ("예측2 within cross-method lag 재현", "pass"),
    "alpha_lag_dissociation": ("예측3 α > lag 순서 (Δρ)", "pass"),
    "cross_dataset_replication": ("예측4 cross HSPC↔gastrulation", "pass"),
    "prereg_adherence": ("예측5 per-gene 재현 격차", "pass"),
}


def _f(s: str) -> float | None:
    s = (s or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load_scorecard(path: Path) -> dict:
    """Translate the real scorecard CSV into the report shape scorers.py expects."""
    sections: dict[str, list[dict]] = {}
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):          # csv module: the label comma is quoted
            sec = row["section"]
            label = row["label"]
            n = int(row["n"]) if row["n"] else None

            if sec == "per_gene_disagree":
                # NOT a correlation row: rho=lag-disagree, lo=alpha-disagree, hi empty.
                m = re.match(r"lag\[(.*)\]\|alpha", label)
                sections.setdefault(sec, []).append({
                    "label": "lag|alpha",
                    "n": n,
                    "lag_disagree": _f(row["rho"]),
                    "alpha_disagree": _f(row["lo"]),
                    "lag_source": m.group(1) if m else label,
                })
                continue

            entry = {"label": label, "n": n, "rho": _f(row["rho"]),
                     "lo": _f(row["lo"]), "hi": _f(row["hi"])}
            if sec == "within_lag":
                # p3_prereg_gse205117.py L'예측2' computes LAG_MV/LAG_VAE with .abs() and
                # reports it as "lag 크기 rank"; the sign test is explicitly skipped.
                entry["test"] = "magnitude_rank"
            if sec == "delta_rho":
                entry["paired"] = True         # boot_dr — paired by construction
            sections.setdefault(sec, []).append(entry)

    return {
        "dataset": "gse205117",
        "scorecard": str(path.relative_to(REPO_ROOT)),
        "prereg_deviation": None,   # committed scorecard.md records no deviation
        "sections": sections,
    }


def main() -> int:
    if not SCORECARD.exists():
        print(f"[중단] 실물 scorecard 없음: {SCORECARD}", file=sys.stderr)
        return 2

    print(f"real artifact: {SCORECARD.relative_to(REPO_ROOT)}")
    print(f"committed verdict (scorecard.md): 6 PASS / 0 FAIL / 0 N/A\n")

    report = load_scorecard(SCORECARD)
    for sec, rows in report["sections"].items():
        print(f"  [{sec}] {len(rows)} row(s): "
              + ", ".join(f"{r['label']}(n={r['n']})" for r in rows))
    print()

    mismatches: list[str] = []
    for name, fn in SCORERS.items():
        pred_label, expected = EXPECTED_COMMITTED[name]
        v = fn(report)
        ok = v.status == expected
        if not ok:
            mismatches.append(f"{name}: committed={expected} eval={v.status}")
        print(f"[{'ok      ' if ok else 'MISMATCH'}] {pred_label:<34} "
              f"committed={expected:<6} eval={v.status}")
        for r in v.reasons:
            print(f"             - {r}")

    # 예측6 = #2 且 #3 (사전등록 표 6행) — derived, not an independent measurement.
    p2 = SCORERS["lag_fragility"](report).status
    p3 = SCORERS["alpha_lag_dissociation"](report).status
    p6 = "pass" if (p2 == "pass" and p3 == "pass") else "fail"
    ok6 = p6 == "pass"
    if not ok6:
        mismatches.append(f"예측6: committed=pass eval={p6}")
    print(f"[{'ok      ' if ok6 else 'MISMATCH'}] {'예측6 priming 극대에서도 fragile (#2 且 #3)':<34} "
          f"committed=pass   eval={p6}")

    print(f"\n{'='*78}")
    if mismatches:
        print("FAIL — eval이 커밋된 채점표를 재현하지 못했다:")
        for m in mismatches:
            print(f"  {m}")
        return 1
    print("6/6 — eval이 커밋된 채점표(6 PASS / 0 FAIL)를 정확히 재현했다.")
    print("범위: 임계 적용의 재현이지 통계(bootstrap ρ) 재계산이 아니다 — 모듈 docstring 참조.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
