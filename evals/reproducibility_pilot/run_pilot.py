"""Fallback runner — scores every case with stdlib python only.

    python3 run_pilot.py

Exists because the velo-* envs (BIOP01's pipeline envs) have no inspect_ai, and
installing it there is forbidden (env 통합·오염 금지). This runner is the durable
proof that the scorers work; `reproducibility_pilot.py` is the same logic wired into
Inspect for the CI story. Both import `scorers.py`, so they cannot drift apart.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from scorers import SCORERS, load_report

ROOT = Path(__file__).parent
CASE_DIRS = [ROOT / "cases" / "scorer_validation", ROOT / "cases" / "regression_corpus"]


def case_files() -> list[Path]:
    out: list[Path] = []
    for d in CASE_DIRS:
        out.extend(sorted(d.glob("*.json")))
    return out


def run_all() -> tuple[list[dict], list[dict]]:
    """Return (results, cases). results = one row per (case, scorer) with an expectation."""
    results: list[dict] = []
    cases: list[dict] = []
    for p in case_files():
        with open(p, encoding="utf-8") as f:
            doc = json.load(f)
        meta = doc.get("_case_meta") or {}
        cases.append({"path": p, "meta": meta})
        report = load_report(p)
        for name, fn in SCORERS.items():
            expected = (meta.get("expected") or {}).get(name)
            if expected is None:
                continue
            verdict = fn(report)
            results.append({
                "case": p.stem,
                "dir": p.parent.name,
                "scorer": name,
                "expected": expected,
                "actual": verdict.status,
                "ok": verdict.status == expected,
                "reasons": verdict.reasons,
                "kind": meta.get("kind", ""),
                "expected_is_a_miss": meta.get("expected_is_a_miss", False),
            })
    return results, cases


def main() -> int:
    results, cases = run_all()

    width = max(len(r["case"]) for r in results)
    cur_dir = None
    for r in results:
        if r["dir"] != cur_dir:
            cur_dir = r["dir"]
            print(f"\n=== {cur_dir} ===")
        mark = "ok " if r["ok"] else "MISMATCH"
        miss = "  (expected miss)" if r["expected_is_a_miss"] and r["ok"] else ""
        print(f"[{mark:8}] {r['case']:<{width}}  {r['scorer']:<26} "
              f"expected={r['expected']:<15} actual={r['actual']}{miss}")
        if not r["ok"]:
            for reason in r["reasons"]:
                print(f"             ! {reason}")

    n_ok = sum(1 for r in results if r["ok"])
    print(f"\n{'='*78}")
    print(f"scorer agreement: {n_ok}/{len(results)} cases scored as the prereg predicts")

    # --- coverage over the real failure corpus --------------------------------
    print(f"\n=== regression corpus coverage (실제 BIOP01 재현성 실패) ===")
    print("⚠️  '통과'는 '결함을 잡았다'가 아니다. expected='pass'인 real_failure는 이 파일럿이")
    print("    구조적으로 놓치는 결함이다(_case_meta.needs_scorer 참조).")
    caught = missed = 0
    for c in cases:
        meta = c["meta"]
        if meta.get("kind") not in ("real_failure", "out_of_scope"):
            continue
        if meta.get("caught"):
            caught += 1
            flag = "CAUGHT "
        else:
            missed += 1
            flag = "MISSED "
        print(f"  [{flag}] {c['path'].stem}")
        if not meta.get("caught"):
            need = (meta.get("needs_scorer") or "").split("\n")[0]
            print(f"            -> {need.strip()[:110]}")
    print(f"\n  실제 실패 {caught + missed}건 중 {caught}건 적발 / {missed}건 미적발(정직 보고).")

    bad = [r for r in results if not r["ok"]]
    if bad:
        print(f"\nFAIL — {len(bad)} scorer/expectation mismatch(es)")
        return 1
    print("\nAll cases scored exactly as the sealed prereg predicts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
