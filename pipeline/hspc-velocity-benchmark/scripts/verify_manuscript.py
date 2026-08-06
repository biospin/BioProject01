#!/usr/bin/env python3
"""verify_manuscript.py — 원고 검증 하네스 (AKM WEEK 03 운영화, 과제2 파일 기반).

기존 결정적 검사(check_manuscript_numbers·check_revision_preserved·p13·…)를 *하나의 루프*로
체인하고, baseline SHA 동결 → per-check verdict(PASS/HOLD/FAIL) → HOLD 카드 → 종합 verdict를
낸다. 규율은 `manuscript/VERIFICATION_PROTOCOL.md`.

★ 원칙: 이 러너는 **검증·보고만 하고 원고를 고치지 않는다**(correction gate는 사람이).
   verdict는 tool evidence(사다리 Lv3~4)일 뿐 최종이 아니다 — HOLD는 사람이 판정한다.

exit 매핑: 검사 exit 0 → PASS, 1/2 → HOLD(자동 FAIL 아님), 크래시 → FAIL, 입력부재 → SKIP.
종합: 하나라도 HOLD/FAIL이면 종합 HOLD(자동 PASS 신뢰 금지).

사용:
  python3 scripts/verify_manuscript.py                  # 결정적 검사 체인
  python3 scripts/verify_manuscript.py --with-recompute # p3 재계산 게이트까지(scv-preprocess 필요)
  python3 scripts/verify_manuscript.py --conda /path/to/conda
산출: results/manuscript_verification_report.md
종료코드: 0 = 전부 PASS, 1 = HOLD 있음(사람 판정 필요), 2 = FAIL 있음.
"""
from __future__ import annotations
import argparse
import datetime as _dt  # noqa: F401  (사용 안 함 — 시각은 git/외부에서)
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
SCRIPTS = BENCH / "scripts"
DRAFT_EN = "manuscript/draft_v2.md"
DRAFT_KO = "manuscript/draft_v2_ko.md"


def sha256(rel):
    p = BENCH / rel
    if not p.exists():
        return "(없음)"
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def git_head():
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=BENCH,
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or "(git 없음)"
    except Exception:
        return "(git 없음)"


def run_check(label, argv, timeout=180, needs=None):
    """needs: 실행 전 존재해야 하는 파일들(상대경로). 하나라도 없으면 SKIP."""
    for n in (needs or []):
        if not (BENCH / n).exists():
            return dict(label=label, verdict="SKIP", rc=None, note=f"입력 부재: {n}", tail="")
    script = SCRIPTS / argv[0]
    if not script.exists():
        return dict(label=label, verdict="SKIP", rc=None, note=f"스크립트 부재: {argv[0]}", tail="")
    cmd = [sys.executable, str(script)] + argv[1:]
    try:
        r = subprocess.run(cmd, cwd=BENCH, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return dict(label=label, verdict="HOLD", rc=None, note=f"타임아웃 {timeout}s", tail="")
    except Exception as e:
        return dict(label=label, verdict="FAIL", rc=None, note=f"실행 오류 {type(e).__name__}: {e}", tail="")
    out = (r.stdout + r.stderr).strip().splitlines()
    tail = "\n".join(out[-6:])
    rc = r.returncode
    verdict = {0: "PASS", 1: "HOLD", 2: "HOLD"}.get(rc, "FAIL")
    note = {0: "이상 없음", 1: "플래그 있음 → 사람 판정",
            2: "baseline/입력 없음"}.get(rc, f"비정상 종료 rc={rc}")
    return dict(label=label, verdict=verdict, rc=rc, note=note, tail=tail)


def find_claims():
    for c in (BENCH.glob("**/CLAIMS.yaml")):
        return str(c.relative_to(BENCH))
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-recompute", action="store_true", help="p3 재계산 게이트까지(env 필요)")
    ap.add_argument("--conda", default=shutil.which("conda") or "/home/kkkim/miniconda3/bin/conda")
    a = ap.parse_args(argv)

    checks = [
        ("숫자 드리프트 EN (check_manuscript_numbers)",
         ["check_manuscript_numbers.py", "--doc", DRAFT_EN], [DRAFT_EN]),
        ("숫자 드리프트 KO (check_manuscript_numbers)",
         ["check_manuscript_numbers.py", "--doc", DRAFT_KO], [DRAFT_KO]),
        ("수정 보존 EN (check_revision_preserved)",
         ["check_revision_preserved.py", "--doc", DRAFT_EN], [DRAFT_EN]),
        ("수정 보존 KO (check_revision_preserved)",
         ["check_revision_preserved.py", "--doc", DRAFT_KO], [DRAFT_KO]),
        ("본문→목록 인용결함 (p13_check_uncited_sources)",
         ["p13_check_uncited_sources.py"], []),
    ]
    claims = find_claims()
    if claims:
        checks.append(("CLAIMS ledger 모순 (check_claims_ledger)",
                       ["check_claims_ledger.py", "--claims", claims, "--draft", DRAFT_EN], [claims]))

    results = [run_check(lbl, argv, needs=needs) for (lbl, argv, needs) in checks]

    # p3 재계산 게이트 (옵션, env 필요)
    for g in ("p3_concordance.py", "p3_crossdataset_concordance.py", "p3_scrambled_null.py"):
        if not a.with_recompute:
            results.append(dict(label=f"재계산 게이트 {g}", verdict="SKIP", rc=None,
                                note="--with-recompute 미지정(scv-preprocess+data 필요)", tail=""))
            continue
        cmd = [a.conda, "run", "--no-capture-output", "-n", "scv-preprocess",
               "python", f"scripts/{g}"]
        try:
            r = subprocess.run(cmd, cwd=BENCH, capture_output=True, text=True, timeout=1200)
            rc = r.returncode
            results.append(dict(label=f"재계산 게이트 {g}",
                                verdict="PASS" if rc == 0 else "HOLD", rc=rc,
                                note="재계산 완료" if rc == 0 else f"rc={rc} 확인 필요",
                                tail="\n".join((r.stdout + r.stderr).strip().splitlines()[-4:])))
        except Exception as e:
            results.append(dict(label=f"재계산 게이트 {g}", verdict="SKIP", rc=None,
                                note=f"실행 불가: {type(e).__name__} (env 확인)", tail=""))

    # ── 리포트 ──
    npass = sum(r["verdict"] == "PASS" for r in results)
    nhold = sum(r["verdict"] == "HOLD" for r in results)
    nfail = sum(r["verdict"] == "FAIL" for r in results)
    nskip = sum(r["verdict"] == "SKIP" for r in results)
    overall = "FAIL" if nfail else ("HOLD" if nhold else "PASS")

    L = []
    A = L.append
    A("# 원고 검증 리포트 — AKM WEEK 03 (verify_manuscript.py)")
    A("")
    A("> 자동 PASS를 신뢰하지 않는다. HOLD는 사람이 correction gate(구체 충돌 시만·cap 2회) 아래 판정한다.")
    A("> 이 러너는 검증·보고만 하고 원고를 고치지 않는다. 규율=`manuscript/VERIFICATION_PROTOCOL.md`.")
    A("")
    A("## Baseline 동결 (provenance)")
    A("")
    A(f"- `{DRAFT_EN}` sha256[:16] = `{sha256(DRAFT_EN)}`")
    A(f"- `{DRAFT_KO}` sha256[:16] = `{sha256(DRAFT_KO)}`")
    A(f"- git HEAD = `{git_head()}` | 위험 Tier = **3 (투고·공개)** | correction cap = 2")
    A("")
    A("## Per-check verdict (tool evidence 층, 사다리 Lv3~4)")
    A("")
    A("| 검사 | verdict | rc | 근거 |")
    A("|---|---|---|---|")
    for r in results:
        A(f"| {r['label']} | **{r['verdict']}** | {r['rc']} | {r['note']} |")
    A("")
    A(f"## 종합: **{overall}**  (PASS {npass} · HOLD {nhold} · FAIL {nfail} · SKIP {nskip})")
    A("")
    holds = [r for r in results if r["verdict"] in ("HOLD", "FAIL")]
    if holds:
        A("### HOLD/FAIL 카드 (4필드: 부족증거 · 다음확인 1개 · 책임경계 · 재개조건)")
        A("")
        for r in holds:
            A(f"- **{r['label']}** [{r['verdict']}]")
            A(f"  - 부족 증거: {r['note']}")
            if r["tail"]:
                A(f"  - 다음 확인 1개: 아래 출력 검토 → 진짜 결함인지 정당 오탐(반올림·CI경계·파생값)인지 사람 판정")
                for ln in r["tail"].splitlines():
                    A(f"    > {ln}")
            A("  - 책임 경계: 원고 owner(kkkim). 수정은 owner가, cap 2회 안에서.")
            A("  - 재개 조건: 결함이면 최소 수정 후 이 러너 재실행 diff 0; 오탐이면 PASS_WITH_NOTE로 기록.")
        A("")
    else:
        A("HOLD/FAIL 없음 — 전 결정적 검사 통과. 단 최종 verdict는 사람(Lv8)이 확정한다.")
        A("")
    A("## SKIP 목록 (별도 실행 필요)")
    for r in results:
        if r["verdict"] == "SKIP":
            A(f"- {r['label']}: {r['note']}")

    out = BENCH / "results/manuscript_verification_report.md"
    out.write_text("\n".join(L) + "\n")

    # 콘솔 요약
    print(f"[verify_manuscript] Tier 3 | baseline EN={sha256(DRAFT_EN)} git={git_head()}")
    for r in results:
        mark = {"PASS": "✅", "HOLD": "⚠️", "FAIL": "❌", "SKIP": "⏭"}[r["verdict"]]
        print(f"  {mark} {r['verdict']:<4} {r['label']} — {r['note']}")
    print(f"\n종합: {overall} (PASS {npass}·HOLD {nhold}·FAIL {nfail}·SKIP {nskip})")
    print(f"리포트: {out.relative_to(BENCH)}")
    return 2 if nfail else (1 if nhold else 0)


if __name__ == "__main__":
    sys.exit(main())
