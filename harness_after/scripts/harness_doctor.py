#!/usr/bin/env python3
"""harness_doctor.py — 하네스 구성 정합성 게이트.

harness.yaml(manifest)을 기준으로 실제 파일·문서 참조가 일치하는지 검사한다.
논문 '결과'가 아니라 하네스 '구성 자체'를 검증한다. PR CI에서 돌린다.

검사:
  1) implemented=true 역할의 path 존재
  2) artifacts 경로 존재
  3) 문서(doc_reference_scan)가 참조하는 agent 이름이 미구현(implemented=false)인데 쓰이면 FAIL  ← reviewer 팬텀 검출
  4) execution.require_repo_root: repo 루트(.git 또는 CLAUDE.md)에서 실행됐는지
사용:  python scripts/harness_doctor.py --repo . --manifest harness.yaml
종료코드: 0=PASS, 1=FAIL, 2=실행오류
"""
import argparse, os, re, sys

def load_yaml(path):
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML 필요 (pip install pyyaml / conda install pyyaml)", file=sys.stderr)
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--manifest", default="harness.yaml")
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    man_path = a.manifest if os.path.isabs(a.manifest) else os.path.join(repo, a.manifest)
    if not os.path.exists(man_path):
        print(f"ERROR: manifest 없음: {man_path}", file=sys.stderr); sys.exit(2)
    m = load_yaml(man_path)

    fails, warns = [], []
    def p(path): return os.path.join(repo, path)

    roles = m.get("roles", {})
    # 1) implemented 역할 path 존재
    for name, r in roles.items():
        if not isinstance(r, dict):
            continue
        if r.get("implemented") and r.get("path") and not os.path.exists(p(r["path"])):
            fails.append(f"[role] {name}: implemented=true 인데 경로 없음 → {r['path']}")

    # 2) artifacts 존재
    for k, v in (m.get("artifacts") or {}).items():
        if not os.path.exists(p(v)):
            warns.append(f"[artifact] {k}: 경로 없음 → {v}")

    # 3) 문서 참조 vs 미구현 (팬텀 검출)
    scan = (m.get("doc_reference_scan") or {}).get("files", [])
    # 미구현 역할의 모든 별칭(aka) 토큰 수집
    phantom_tokens = {}
    for name, r in roles.items():
        if isinstance(r, dict) and r.get("implemented") is False:
            akas = r.get("aka", [])
            if isinstance(akas, str): akas = [akas]
            for tok in set([name] + akas):
                phantom_tokens.setdefault(tok, name)
    for f in scan:
        fp = p(f)
        if not os.path.exists(fp):
            warns.append(f"[scan] 문서 없음 → {f}"); continue
        text = open(fp, encoding="utf-8", errors="replace").read()
        for tok, role in phantom_tokens.items():
            if re.search(r"(?<![\w-])" + re.escape(tok) + r"(?![\w-])", text):
                fails.append(f"[phantom] '{tok}'(역할 {role}, 미구현)가 {f}에서 참조됨 → 구현하거나 참조 제거")

    # 4) repo 루트 실행 전제
    if (m.get("execution") or {}).get("require_repo_root"):
        if not (os.path.exists(p(".git")) or os.path.exists(p("CLAUDE.md"))):
            fails.append("[execution] require_repo_root=true 이나 repo 루트(.git/CLAUDE.md) 아님")

    # 리포트
    print(f"harness_doctor: repo={repo}")
    print(f"  roles={len(roles)}  artifacts={len(m.get('artifacts') or {})}  scan_files={len(scan)}")
    for w in warns: print(f"  WARN {w}")
    for e in fails: print(f"  FAIL {e}")
    if fails:
        print(f"\nRESULT: FAIL ({len(fails)} 문제, {len(warns)} 경고)")
        sys.exit(1)
    print(f"\nRESULT: PASS ({len(warns)} 경고)")
    sys.exit(0)

if __name__ == "__main__":
    main()
