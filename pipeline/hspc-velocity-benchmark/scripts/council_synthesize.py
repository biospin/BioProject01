#!/usr/bin/env python3
"""council_synthesize.py — 다중 모델 적대적 검토 결정론적 종합 (BIOP01-81 항목3, stdlib only).

여러 모델·세션의 구조적 검토 출력(council_schema.json 형식)을 읽어 **메타리뷰 골격**을 만든다.
이 스크립트는 판정을 대신하지 않는다. 중복 제거·모델 간 집계·이견 표면화만 하고, 최종 판정은
메타리뷰어(사람 또는 전용 종합 세션)가 한다. 원 하네스 원칙: "다수결은 진실이 아니다,
모델 이름은 권위가 아니다"(docs/adversarial_multi_llm_council_harness.md, ai_scientist §6.1).

무엇을 하나
- 세션 파일들을 로드·검증(필수 키·enum). 형식 오류는 조용히 통과시키지 않고 표면화.
- claim을 정규화 텍스트로 클러스터링 → 모델별 판정 집계, 합의/이견 표시.
- 비판을 클러스터링 → 유효(valid-ish)/약함(weak-ish) 집계로 살아남음/폐기/이견 분류.
- Valid-and-Fatal이 살아남은 클러스터는 blocking 후보로 별도 표시.

사용:
  python3 scripts/council_synthesize.py session1.json session2.json ...
  python3 scripts/council_synthesize.py --dir /path/to/sessions [--out /tmp/meta_scaffold.md]
종료코드: 0 = 살아남은 Fatal 비판 없음, 1 = 살아남은 Valid-and-Fatal 있음(blocking), 2 = 입력/형식 오류.
"""
from __future__ import annotations
import argparse, json, re, sys
from collections import defaultdict
from pathlib import Path

CLAIM_VERDICTS = {"Proven", "Plausible", "Speculative", "Unsupported", "Incorrect"}
CRIT_VERDICTS = {"Valid-and-Fatal", "Valid-but-Fixable", "Partially-Valid", "Weak", "Incorrect", "Hallucinated"}
VALID_ISH = {"Valid-and-Fatal", "Valid-but-Fixable", "Partially-Valid"}
WEAK_ISH = {"Weak", "Incorrect", "Hallucinated"}

def norm(s: str) -> str:
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s.strip(' .,:;"\'')

def load_sessions(paths: list[Path]) -> tuple[list[dict], list[str]]:
    sessions, errors = [], []
    for p in paths:
        try:
            d = json.loads(p.read_text())
        except Exception as e:  # noqa: BLE001
            errors.append(f"{p.name}: JSON 파싱 실패 ({type(e).__name__})"); continue
        for k in ("model", "session", "target"):
            if k not in d:
                errors.append(f"{p.name}: 필수 키 '{k}' 없음")
        for c in d.get("claims", []):
            if c.get("verdict") not in CLAIM_VERDICTS:
                errors.append(f"{p.name}: claim verdict 오류 '{c.get('verdict')}'")
        for c in d.get("critiques", []):
            if c.get("verdict") not in CRIT_VERDICTS:
                errors.append(f"{p.name}: critique verdict 오류 '{c.get('verdict')}'")
        d["_file"] = p.name
        sessions.append(d)
    return sessions, errors

def cluster_claims(sessions):
    clusters = defaultdict(lambda: {"text": "", "by_model": defaultdict(list)})
    for s in sessions:
        for c in s.get("claims", []):
            key = norm(c["text"])
            clusters[key]["text"] = c["text"]
            clusters[key]["by_model"][s["model"]].append(c["verdict"])
    return clusters

def cluster_critiques(sessions):
    clusters = defaultdict(lambda: {"text": "", "by_model": defaultdict(list), "verdicts": []})
    for s in sessions:
        for c in s.get("critiques", []):
            key = norm(c["text"])
            clusters[key]["text"] = c["text"]
            clusters[key]["by_model"][s["model"]].append(c["verdict"])
            clusters[key]["verdicts"].append(c["verdict"])
    return clusters

def classify_critique(verdicts):
    v = sum(1 for x in verdicts if x in VALID_ISH)
    w = sum(1 for x in verdicts if x in WEAK_ISH)
    if v > w:
        return "survived"
    if w > v:
        return "failed"
    return "disagreement"

def fmt_by(by: dict) -> str:
    """{'claude': ['Weak'], ...} → 'claude:Weak; gpt:Valid-and-Fatal'."""
    parts = []
    for m, vs in by.items():
        parts.append(m + ":" + "/".join(vs))
    return "; ".join(parts)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--dir", help="세션 JSON 디렉토리(*.json 전부)")
    ap.add_argument("--out", help="메타리뷰 골격 markdown 출력 경로")
    args = ap.parse_args()

    paths = [Path(f) for f in args.files]
    if args.dir:
        paths += sorted(Path(args.dir).glob("*.json"))
    paths = [p for p in paths if p.exists()]
    if not paths:
        print("세션 파일 없음.", file=sys.stderr); return 2

    sessions, errors = load_sessions(paths)
    if errors:
        print("⚠ 입력 형식 오류(자동 통과 아님):", file=sys.stderr)
        for e in errors:
            print("   -", e, file=sys.stderr)
        return 2

    models = sorted({s["model"] for s in sessions})
    claims = cluster_claims(sessions)
    crits = cluster_critiques(sessions)

    survived, failed, disagreement, fatal = [], [], [], []
    for _, c in crits.items():
        cls = classify_critique(c["verdicts"])
        entry = (c["text"], dict(c["by_model"]))
        if cls == "survived":
            survived.append(entry)
            if any(v == "Valid-and-Fatal" for v in c["verdicts"]):
                fatal.append(entry)
        elif cls == "failed":
            failed.append(entry)
        else:
            disagreement.append(entry)

    L = []
    L.append("# 메타리뷰 골격 (council_synthesize.py — 집계이지 판정이 아님)")
    L.append("")
    L.append(f"- 입력 세션 {len(sessions)}개, 모델 {', '.join(models)}")
    L.append(f"- claim 클러스터 {len(claims)}, 비판 클러스터 {len(crits)}")
    L.append("- 최종 판정(Reject/Major Revision/Conditional Go 등)은 메타리뷰어가 근거의 질로 정한다. 다수결 아님.")
    L.append("")
    L.append("## Claim 판정 집계")
    for _, c in claims.items():
        allv = {v for vs in c["by_model"].values() for v in vs}
        tag = "합의" if len(allv) == 1 and len(c["by_model"]) > 1 else ("단일" if len(c["by_model"]) == 1 else "이견")
        L.append(f"- [{tag}] {c['text']}  ({fmt_by(c['by_model'])})")
    L.append("")
    L.append(f"## 살아남은 비판 (valid-ish 우세) — {len(survived)}")
    for t, by in survived:
        L.append(f"- {t}  ({fmt_by(by)})")
    L.append("")
    L.append(f"## ⛔ Fatal 후보 (살아남음 + Valid-and-Fatal 포함) — {len(fatal)}")
    for t, by in fatal:
        L.append(f"- {t}")
    L.append("")
    L.append(f"## 폐기된 비판 (weak-ish 우세) — {len(failed)}")
    for t, by in failed:
        L.append(f"- {t}")
    L.append("")
    L.append(f"## 이견 있는 비판 (valid=weak) — {len(disagreement)}")
    for t, by in disagreement:
        L.append(f"- {t}  ({fmt_by(by)})")
    scaffold = "\n".join(L) + "\n"

    if args.out:
        Path(args.out).write_text(scaffold)
    print(scaffold)
    return 1 if fatal else 0

if __name__ == "__main__":
    raise SystemExit(main())
