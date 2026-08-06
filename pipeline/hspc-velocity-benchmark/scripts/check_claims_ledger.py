#!/usr/bin/env python3
"""check_claims_ledger.py — CLAIMS.yaml provenance ledger 무결성 게이트 (BIOP01-82, stdlib+PyYAML).

왜 있나
------
CLAIMS.yaml(BIOP01-69) 은 headline claim 을 근거·한계·강도와 함께 등록하지만, "게이트가
ledger 를 실제 참조하는 연동은 후속"으로 남아 있었다. 검수 하네스 mutation 실험이
그 gap 3종(claim_level 격상·limitations 삭제·key_number 무결성)을 NOT_TESTED 로 확정했다.
이 게이트가 그 3종을 결정론적으로 잡는다. LLM 판단 없음 — 등록된 값 대조뿐.

세 검사
-------
1. claim_level ↔ status : primary_* 등급(primary_positive/negative/generalization) 은
   status=supported 를 요구한다. provisional claim 을 primary 로 격상하면 CONTRADICTED.
2. limitations 보존       : 각 claim 의 limitations 문자열이 담은 수치가 원고에 실재해야
   한다. 한계 문단을 지우면 그 수치가 사라져 CONTRADICTED.
3. key_number ↔ evidence : 각 claim 의 key_numbers 가 담은 수치가 그 claim 의 evidence
   파일에 실재해야 한다. 근거 밖 값으로 바꾸면 CONTRADICTED.

판정(방법론 6종): SUPPORTED / CONTRADICTED / INSUFFICIENT(근거파일 부재).

사용:
    python3 scripts/check_claims_ledger.py                         # 정본
    python3 scripts/check_claims_ledger.py --claims X --draft Y    # 샌드박스 사본
    # 종료코드: CONTRADICTED 있으면 1
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]        # scripts/ → bench → pipeline → repo
PRIMARY = {"primary_positive", "primary_negative", "primary_generalization"}
NUM = re.compile(r"[-+]?\d+\.\d+|[-+]?\d+/\d+|[-+]?\d+%")   # 0.88, -0.04, 0/598, 48%


def norm(s: str) -> str:
    return str(s).replace("−", "-")


def nums(s: str) -> set[str]:
    """ledger 문자열이 담은 수치 토큰(검증 대상)."""
    return {n.lstrip("+") for n in NUM.findall(norm(s))}


def missing_in(tokens: set[str], text: str) -> list[str]:
    """check_manuscript_numbers 규약: 각 수치 토큰이 대상 텍스트에 substring 으로 실재하는지.
    (evidence 가 0.882 로 더 정밀하면 0.88 은 substring 매칭됨.)"""
    t = norm(text)
    return sorted(tok for tok in tokens if tok not in t)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", default=str(REPO / "CLAIMS.yaml"))
    ap.add_argument("--draft", default=str(REPO / "pipeline/hspc-velocity-benchmark/manuscript/draft_v2.md"))
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    ledger = yaml.safe_load(Path(a.claims).read_text())
    draft = Path(a.draft).read_text(errors="ignore")
    findings = []

    for c in ledger.get("claims", []):
        cid = c["id"]
        # 1. claim_level ↔ status
        if c.get("claim_level") in PRIMARY and c.get("status") != "supported":
            findings.append(dict(check="claim_level_vs_status", claim=cid, verdict="CONTRADICTED",
                                 detail=f"level={c['claim_level']} 은 status=supported 필요, 실제 status={c.get('status')}"))
        # 2. limitations 보존 (수치가 있는 한계만 대조)
        lim_nums = set().union(*(nums(x) for x in c.get("limitations", []))) if c.get("limitations") else set()
        if lim_nums and missing_in(lim_nums, draft) == sorted(lim_nums):   # 한계 수치가 draft 에서 통째로 사라짐
            findings.append(dict(check="limitations_preserved", claim=cid, verdict="CONTRADICTED",
                                 detail=f"limitations 수치 {sorted(lim_nums)} 가 원고에 없음(한계 삭제 의심)"))
        # 3. key_number ↔ evidence
        kn = set().union(*(nums(v) for v in c.get("key_numbers", {}).values())) if c.get("key_numbers") else set()
        if kn:
            ev_text = ""
            missing_files = []
            for e in c.get("evidence", []):
                p = REPO / e
                if p.exists():
                    ev_text += p.read_text(errors="ignore")
                else:
                    missing_files.append(e)
            if missing_files and not ev_text:
                findings.append(dict(check="key_number_vs_evidence", claim=cid, verdict="INSUFFICIENT",
                                     detail=f"근거 파일 부재: {missing_files}"))
            else:
                missing = missing_in(kn, ev_text)
                if missing:
                    findings.append(dict(check="key_number_vs_evidence", claim=cid, verdict="CONTRADICTED",
                                         detail=f"key_number 수치 {missing} 가 evidence 파일에 없음"))

    contra = [f for f in findings if f["verdict"] == "CONTRADICTED"]
    insuff = [f for f in findings if f["verdict"] == "INSUFFICIENT"]
    report = dict(claims=str(a.claims), draft=str(a.draft),
                  n_claims=len(ledger.get("claims", [])), findings=findings,
                  contradicted=len(contra), insufficient=len(insuff))
    if a.json:
        Path(a.json).write_text(json.dumps(report, ensure_ascii=False, indent=2))

    if not findings:
        print(f"check_claims_ledger: {report['n_claims']} claims, 0 문제 — SUPPORTED")
    else:
        for f in findings:
            print(f"  [{f['verdict']}] {f['claim']} {f['check']}: {f['detail']}")
        print(f"RESULT: {len(contra)} CONTRADICTED, {len(insuff)} INSUFFICIENT")
    return 1 if contra else 0


if __name__ == "__main__":
    sys.exit(main())
