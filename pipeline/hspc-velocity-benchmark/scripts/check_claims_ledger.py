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
# Claim Admission taxonomy (BIOP01-88 도입2 — Spark-to-Paper Appendix C 재구현, @qian2026sparktopaper)
ADMIT = {"supported", "partially-supported", "unsupported", "contradicted", "needs-confirmation"}
LEGACY = {"provisional", "withdrawn", "hypothesis_only"}   # 점진 마이그레이션 — 통과시키되 신 라벨 권장
ALLOWED = ADMIT | LEGACY
NUM = re.compile(r"[-+]?\d+\.\d+|[-+]?\d+/\d+|[-+]?\d+%")   # 0.88, -0.04, 0/598, 48%

# 교정(fix) 등급·자리 — 방법론 §3. 이 도메인 결함은 정답이 하나로 안 정해져 auto 가 아니다
# (§12: 판단 필요 항목을 자동 PASS/FAIL 로 환원하지 않는다). detector 가 자리·제안을 명시하고
# 적용은 사람이 확인한다(assist). 루프는 교정 후 재실행으로 닫는다.
FIX = {
    "claim_level_vs_status": {"tier": "assist", "target": "source",
        "suggestion": "claim_level 을 status 에 맞게 하향(primary_→mechanism/supporting/downstream) 또는 evidence 확보 후 status 승격"},
    "limitations_preserved": {"tier": "assist", "target": "artifact",
        "suggestion": "삭제된 한계 문장을 원고에 복원(CLAIMS.limitations 참조)"},
    "key_number_vs_evidence": {"tier": "assist", "target": "source",
        "suggestion": "key_number 를 evidence 파일의 실측값으로 정정"},
    "admission_label": {"tier": "assist", "target": "source",
        "suggestion": "status 를 5라벨(supported/partially-supported/unsupported/contradicted/needs-confirmation) 중 하나로"},
    "admission_needs_confirmation": {"tier": "assist", "target": "source",
        "suggestion": "근거 확보 후 supported/partially 로 승격하거나 약화·삭제 — 제출 전 해소(미해결 blocker)"},
    "admission_partial_needs_limit": {"tier": "assist", "target": "source",
        "suggestion": "좁힌 범위를 limitations 에 명시"},
    "admission_contradicted_in_draft": {"tier": "assist", "target": "artifact",
        "suggestion": "contradicted claim 을 본문에서 삭제하거나 한계로만 서술"},
}


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
    ap.add_argument("--strict", action="store_true", help="needs-confirmation/contradicted 를 exit 1 로(제출 게이트)")
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
        # 4. Claim Admission taxonomy (BIOP01-88 도입2 — Spark-to-Paper Appendix C 재구현)
        st = c.get("status")
        if st not in ALLOWED:
            findings.append(dict(check="admission_label", claim=cid, verdict="CONTRADICTED",
                                 detail=f"status={st!r} 미정의 라벨 (허용 {sorted(ADMIT)} + legacy {sorted(LEGACY)})"))
        if st == "needs-confirmation":
            findings.append(dict(check="admission_needs_confirmation", claim=cid, verdict="NEEDS_HUMAN",
                                 detail="needs-confirmation 은 제출 전 해소 필요(미해결 blocker)"))
        if st == "partially-supported" and not c.get("limitations"):
            findings.append(dict(check="admission_partial_needs_limit", claim=cid, verdict="CONTRADICTED",
                                 detail="partially-supported 는 좁힘을 limitations 로 문서화해야 한다"))
        if st == "contradicted" and c.get("manuscript_locations"):
            findings.append(dict(check="admission_contradicted_in_draft", claim=cid, verdict="NEEDS_HUMAN",
                                 detail=f"contradicted claim 이 본문 {c.get('manuscript_locations')} 에 배치됨 — 삭제/한계화 확인"))

    for f in findings:                    # 방법론 §3·§5: 각 결함에 교정 자리·등급·제안(4요소 ④)
        f["fix"] = FIX.get(f["check"])
    contra = [f for f in findings if f["verdict"] == "CONTRADICTED"]
    insuff = [f for f in findings if f["verdict"] == "INSUFFICIENT"]
    needs  = [f for f in findings if f["verdict"] == "NEEDS_HUMAN"]
    report = dict(claims=str(a.claims), draft=str(a.draft),
                  n_claims=len(ledger.get("claims", [])), findings=findings,
                  contradicted=len(contra), insufficient=len(insuff), needs_human=len(needs))
    if a.json:
        Path(a.json).write_text(json.dumps(report, ensure_ascii=False, indent=2))

    if not findings:
        print(f"check_claims_ledger: {report['n_claims']} claims, 0 문제 — SUPPORTED")
    else:
        for f in findings:
            print(f"  [{f['verdict']}] {f['claim']} {f['check']}: {f['detail']}")
        print(f"RESULT: {len(contra)} CONTRADICTED, {len(insuff)} INSUFFICIENT, {len(needs)} NEEDS_HUMAN"
              + (" (--strict: NEEDS_HUMAN 도 실패)" if a.strict else ""))
    return 1 if contra or (a.strict and needs) else 0


if __name__ == "__main__":
    sys.exit(main())
