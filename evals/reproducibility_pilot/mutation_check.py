"""Mutation test — proves the case set actually constrains the scorers.

An eval that a stub scorer can ace is measuring nothing. A suite of only-FAIL cases
gives an always-fail stub a perfect score; a suite of only-PASS cases gives an
always-pass stub a perfect score. This replaces each real scorer with degenerate
ones and asserts the case set rejects every one of them.

Run after ANY change to cases/ or scorers.py.

    python3 mutation_check.py
"""

from __future__ import annotations

import sys

import scorers
from scorers import Verdict
from run_pilot import run_all

MUTANTS = {
    "always_pass": lambda r: Verdict("pass", ["stub"]),
    "always_fail": lambda r: Verdict("fail", ["stub"]),
    "always_caution": lambda r: Verdict("caution", ["stub"]),
    "always_na": lambda r: Verdict("not_applicable", ["stub"]),
    # Direction inversion: the specific bug this suite is most exposed to. α and lag
    # have OPPOSITE pass directions (α high = good, lag low = good), so a scorer that
    # silently applies α's direction to lag must not survive.
    "invert_threshold": None,   # installed per-target below
}


def _inverted(fn):
    """Flip pass<->fail while leaving caution/NA alone — a scorer with the comparison backwards."""
    def wrapped(report):
        v = fn(report)
        if v.status == "pass":
            return Verdict("fail", ["inverted stub"])
        if v.status == "fail":
            return Verdict("pass", ["inverted stub"])
        return v
    return wrapped


def main() -> int:
    real = dict(scorers.SCORERS)
    baseline, _ = run_all()
    base_ok = sum(1 for r in baseline if r["ok"])
    print(f"real scorers:      {base_ok}/{len(baseline)} correct\n")

    failed_to_kill: list[str] = []
    for mut_name in MUTANTS:
        for target in real:
            mut_fn = _inverted(real[target]) if mut_name == "invert_threshold" else MUTANTS[mut_name]
            scorers.SCORERS.clear()
            scorers.SCORERS.update(real)
            scorers.SCORERS[target] = mut_fn
            results, _ = run_all()
            rows = [r for r in results if r["scorer"] == target]
            ok = sum(1 for r in rows if r["ok"])
            killed = ok < len(rows)
            status = "killed" if killed else "SURVIVED <<<"
            print(f"  {target:<26} := {mut_name:<17} -> {ok}/{len(rows)} correct  [{status}]")
            if not killed:
                failed_to_kill.append(f"{target} := {mut_name}")
        print()

    scorers.SCORERS.clear()
    scorers.SCORERS.update(real)

    if failed_to_kill:
        print("FAIL — case set does not constrain these mutants:")
        for f in failed_to_kill:
            print(f"  {f}")
        return 1
    print("All mutants killed: every scorer is genuinely constrained by the cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
