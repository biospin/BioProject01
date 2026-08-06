#!/usr/bin/env python3
"""run_validation.py — 결과물 검수 하네스 mutation 러너 (BIOP01, stdlib+PyYAML).

방법론: RESULT_VALIDATION_METHOD_PORTABLE_v1. "새 게이트를 만들지 않는다 — 이미 있는
게이트가 의도한 결함을 정말 탐지하는지 mutation 으로 증명한다." 케이스는 cases.yaml 에
코드보다 먼저 선언됐다.

핵심 설계
- 정본 미수정: mutation 은 .sandbox/ 사본에서만. 실행 전후 정본 sha256 불변을 assert.
- control-vs-mutated 델타: 게이트를 mutation 전/후로 두 번 돌려 '새로 생긴 결함'만 센다.
  (check_manuscript_numbers 는 정상 draft 에도 miss 1 을 내므로 exit·총miss 로 판정 불가.)
- 실경로 로깅(§9): 동명 사본(harness_after/) 혼동 방지로 실제 실행한 스크립트 절대경로 기록.
- 6판정 어댑터: 게이트 출력 → SUPPORTED/CONTRADICTED/INSUFFICIENT/NOT_TESTED/REVIEW_REQUIRED.

완료 조건(방법론 §10): 코드 작성이 아니라, 이 실행의 보고서 파일을 열어 판정을 확인해야 완료.

    python3 evals/validation_harness/run_validation.py     # bench 루트에서
"""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
BENCH = HERE.parents[1]                      # pipeline/hspc-velocity-benchmark
SANDBOX = HERE / ".sandbox"
SCRIPTS = BENCH / "scripts"
RESULTS = BENCH / "results"
MANU = BENCH / "manuscript"
REPRO = BENCH.parents[1] / "evals" / "reproducibility_pilot"   # 분석 관점 재현성 eval(재사용)

CANONICAL = [                                # 실행 전후 불변이어야 하는 정본
    MANU / "draft_v2.md", MANU / "draft_v2_ko.md", MANU / "refs.bib",
    BENCH.parent.parent / "CLAIMS.yaml",
    RESULTS / "atac_alpha_expression_confound.md",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "ABSENT"


def run(cmd, cwd=BENCH):
    """게이트 실행. (exit, stdout, resolved_script_path) 반환."""
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


# ---- 어댑터: 게이트 출력 → 6판정 -------------------------------------------

def cmn_misses(doc_rel: str, src_globs: list[str]) -> set[str]:
    """check_manuscript_numbers 를 돌려 miss 값 집합 반환."""
    out_json = SANDBOX / "cmn_out.json"
    cmd = [sys.executable, str(SCRIPTS / "check_manuscript_numbers.py"),
           "--doc", doc_rel, "--src", *src_globs, "--json", str(out_json)]
    run(cmd)
    d = json.loads(out_json.read_text())
    return {m["value"] for m in d.get("misses", [])}


def verdict_from_delta(new_misses: set[str]) -> str:
    return "CONTRADICTED" if new_misses else "SUPPORTED"


def verify_cites(cites_path: Path) -> tuple[str, dict]:
    """verify_citations 어댑터. (fabricated 항목 판정, 상세) 반환."""
    out_json = SANDBOX / "vc_out.json"
    cmd = [sys.executable, str(SCRIPTS / "verify_citations.py"),
           str(cites_path), "--json", str(out_json)]
    ec, log = run(cmd)
    try:
        rows = json.loads(out_json.read_text())
    except Exception:
        return "INSUFFICIENT", {"reason": "verify_citations 출력 파싱 실패(네트워크?)", "log": log[-300:]}
    m = {"VERIFIED": "SUPPORTED", "NOT_FOUND": "CONTRADICTED",
         "AUTHOR_MISMATCH": "CONTRADICTED", "YEAR_MISMATCH": "CONTRADICTED",
         "CLAIM_UNSUPPORTED": "CONTRADICTED", "NEEDS_HUMAN": "REVIEW_REQUIRED"}
    by_id = {r.get("id"): r.get("verdict") for r in rows}
    fab = by_id.get("FAB")
    ctl = by_id.get("CTL")
    # 네트워크 불통 신호: 둘 다 NEEDS_HUMAN 이면 대조 자체가 불가 → INSUFFICIENT
    if fab == "NEEDS_HUMAN" and ctl == "NEEDS_HUMAN":
        return "INSUFFICIENT", {"reason": "CrossRef 조회 불가로 대조 불가", "by_id": by_id}
    return m.get(fab, "REVIEW_REQUIRED"), {"by_id": by_id, "control_ok": m.get(ctl) == "SUPPORTED"}


# ---- 케이스별 실행 ----------------------------------------------------------

def prepare_sandbox():
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    SANDBOX.mkdir(parents=True)


def sb_rel(p: Path) -> str:
    return str(p.relative_to(BENCH))


def case_cmn_number(mutate: str) -> tuple[str, dict]:
    """M1/N0: 본문에 지어낸 숫자 삽입. control(정본 draft) vs mutated(사본) 델타."""
    base = cmn_misses("manuscript/draft_v2.md", ["results/FINDINGS.md", "results/*.md"])
    mut_doc = SANDBOX / "draft_mut.md"
    txt = (MANU / "draft_v2.md").read_text()
    # Results 첫 문단에 지어낸 수치 문장 삽입(입력 게이트 통과·심각한 결함)
    txt = txt.replace("## Results", "## Results\n\nAcross methods the correlation was Spearman rho=0.999 (fabricated).", 1)
    mut_doc.write_text(txt)
    mut = cmn_misses(sb_rel(mut_doc), ["results/FINDINGS.md", "results/*.md"])
    new = mut - base
    return verdict_from_delta(new), {"new_misses": sorted(new), "base_miss_n": len(base)}


def case_cmn_stale() -> tuple[str, dict]:
    """M3: 근거 파일 수치 변경 + 원고 그대로. 소스만 사본으로 두고 변이."""
    # 단일소스 precondition 실측
    hits = [p.name for p in sorted(RESULTS.glob("*.md")) if "0.724" in p.read_text(errors="ignore")]
    single_source = hits == ["atac_alpha_expression_confound.md"]
    sb_res = SANDBOX / "results"
    sb_res.mkdir()
    for p in RESULTS.glob("*.md"):
        shutil.copy2(p, sb_res / p.name)
    src_glob = [f"{sb_rel(sb_res)}/*.md"]
    base = cmn_misses("manuscript/draft_v2.md", src_glob)          # 사본(미변이) 기준
    tgt = sb_res / "atac_alpha_expression_confound.md"
    tgt.write_text(tgt.read_text().replace("0.724", "0.111"))
    mut = cmn_misses("manuscript/draft_v2.md", src_glob)
    new = mut - base
    return verdict_from_delta(new), {"precondition_single_source": single_source,
                                     "0.724_in": hits, "new_misses": sorted(new)}


def case_fabricated_citation() -> tuple[str, dict]:
    """M4: 가짜 DOI 인용 + 실제 control 을 verify_citations 로."""
    cites = [
        {"id": "FAB", "title": "A nonexistent benchmark of fabricated velocity",
         "first_author": "Nemo", "year": "2099", "doi": "10.9999/fake.2099.000000"},
        {"id": "CTL", "title": "RNA velocity of single cells",
         "first_author": "La Manno", "year": "2018", "doi": "10.1038/s41586-018-0414-6"},
    ]
    cp = SANDBOX / "cites.json"
    cp.write_text(json.dumps(cites))
    return verify_cites(cp)


def main() -> int:
    cases = yaml.safe_load((HERE / "cases.yaml").read_text())["cases"]
    pre = {p.name: sha(p) for p in CANONICAL}
    prepare_sandbox()
    resolved = {
        "check_manuscript_numbers": str((SCRIPTS / "check_manuscript_numbers.py").resolve()),
        "verify_citations": str((SCRIPTS / "verify_citations.py").resolve()),
    }

    findings = []
    for c in cases:
        cid = c["id"]
        exp = c["expect"]
        if cid in ("M1_fabricated_number", "N0_negative_control"):
            obs, detail = case_cmn_number(c["mutation"])
            key = "check_manuscript_numbers"
        elif cid == "M0_baseline":
            base = cmn_misses("manuscript/draft_v2.md", ["results/FINDINGS.md", "results/*.md"])
            # registered EXPECTED_MISS 제거 후 남는 새 miss 없으면 SUPPORTED
            reg = {"9.4"}
            residual = base - reg
            obs, detail = ("SUPPORTED" if not residual else "CONTRADICTED"), {"residual_misses": sorted(residual), "registered": sorted(reg)}
            key = "check_manuscript_numbers"
        elif cid == "M3_stale_manuscript":
            obs, detail = case_cmn_stale()
            key = "check_manuscript_numbers"
        elif cid == "M4_fabricated_citation":
            obs, detail = case_fabricated_citation()
            key = "verify_citations"
        elif cid == "A1_analysis_eval_nonvacuous":
            ec, log = run([sys.executable, "mutation_check.py"], cwd=REPRO)
            obs, detail = ("SUPPORTED" if ec == 0 else "CONTRADICTED"), {"exit": ec, "tail": log.strip().splitlines()[-1:]}
            key = "analysis_eval_nonvacuous"
        elif cid == "A2_analysis_corpus_classification":
            ec, log = run([sys.executable, "run_pilot.py"], cwd=REPRO)
            obs, detail = ("SUPPORTED" if ec == 0 else "CONTRADICTED"), {"exit": ec, "tail": log.strip().splitlines()[-1:]}
            key = "analysis_corpus_matches_sealed"
        elif cid in ("M2_claim_level_escalation", "M5_limitations_deleted", "A3_claims_evidence_integrity"):
            obs, detail = "NOT_TESTED", {"reason": "이 결함을 검사하는 게이트가 없음(detector: none)"}
            key = list(exp.keys())[0]
        else:
            obs, detail = "NOT_TESTED", {"reason": "unhandled case"}
            key = list(exp.keys())[0]

        expected = exp.get(key)
        # 음성 대조: 관측≠기대 여야 정상. 그 외: 관측==기대 여야 정상.
        if c["kind"] == "negative_control":
            harness_ok = (obs != expected)
        else:
            harness_ok = (obs == expected)
        findings.append(dict(id=cid, kind=c["kind"], detector=key, expected=expected,
                             observed=obs, harness_ok=harness_ok, detail=detail,
                             fix=c.get("fix"), overall=c.get("overall")))

    post = {p.name: sha(p) for p in CANONICAL}
    canonical_intact = pre == post
    shutil.rmtree(SANDBOX, ignore_errors=True)

    report = dict(
        run_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        runner=str(Path(__file__).resolve()),
        resolved_gate_paths=resolved,
        canonical_sha256_before=pre, canonical_sha256_after=post,
        canonical_intact=canonical_intact,
        not_tested=[f["id"] for f in findings if f["observed"] == "NOT_TESTED"],
        cases=findings,
    )
    (HERE / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))

    # 사람용 요약
    print(f"검수 하네스 실행 — {report['run_at']}")
    print(f"정본 불변: {'OK' if canonical_intact else '★훼손★'}")
    print(f"{'case':<26}{'kind':<17}{'expected':<14}{'observed':<14}harness")
    all_ok = True
    for f in findings:
        mark = "ok" if f["harness_ok"] else "★MISMATCH★"
        if not f["harness_ok"]:
            all_ok = False
        print(f"  {f['id']:<24}{f['kind']:<17}{str(f['expected']):<14}{f['observed']:<14}{mark}")
    print(f"\nNOT_TESTED(게이트 없음): {report['not_tested']}")
    print(f"보고서: {HERE / 'report.json'}")
    ok = all_ok and canonical_intact
    print(f"\nRESULT: {'PASS (모든 케이스가 사전선언 판정과 일치, 정본 불변)' if ok else 'FAIL (불일치/훼손 — 보고서 확인)'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
