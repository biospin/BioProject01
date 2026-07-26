#!/usr/bin/env python3
"""harness_doctor.py — 하네스 구성 정합성 게이트.

harness.yaml(manifest)을 기준으로 실제 파일·문서 참조가 일치하는지 검사한다.
논문 '결과'가 아니라 하네스 '구성 자체'를 검증한다. PR CI에서 돌린다.

검사:
  1) implemented=true 역할의 path 존재
  2) artifacts 경로 존재
  3) 문서가 참조하는 agent 이름이 미구현이면 FAIL                    ← reviewer 팬텀
     - 강한 참조(백틱 인용 / 표 행)만 FAIL, 산문 언급은 WARN         ← kkkim 공동리뷰 2026-07-26 반영
  4) 문서가 백틱으로 인용한 **경로**가 실재하는지                     ← skills/ROUTES.md 팬텀
     - local_only 로 선언된 경로는 부재해도 통과(개인 작업기록). 대신 .gitignore 등재를 확인
  5) execution.require_repo_root: repo 루트에서 실행됐는지
사용:  python scripts/harness_doctor.py --repo . --manifest harness.yaml
종료코드: 0=PASS, 1=FAIL, 2=실행오류
"""
import argparse, os, re, subprocess, sys


def load_yaml(path):
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML 필요 (pip install pyyaml / conda install pyyaml)", file=sys.stderr)
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def repo_index(repo):
    """리포 내 모든 경로 세그먼트의 집합. 상대 인용(`p3_concordance.py`) 해석용."""
    names, tops = set(), set()
    try:
        out = subprocess.check_output(["git", "-C", repo, "ls-files"], text=True).splitlines()
    except Exception:
        out = []
        for root, dirs, files in os.walk(repo):
            if ".git" in root.split(os.sep):
                continue
            for f in files:
                out.append(os.path.relpath(os.path.join(root, f), repo))
    for rel in out:
        parts = rel.split("/")
        tops.add(parts[0])
        for seg in parts:
            names.add(seg)
    return names, tops


def classify_hit(line, tok):
    """강한 참조 = 백틱 인용 또는 표 행(라우팅/계약). 그 외 산문은 약한 참조."""
    if re.search(r"`[^`\n]*(?<![\w-])" + re.escape(tok) + r"(?![\w-])[^`\n]*`", line):
        return "strong"
    if line.lstrip().startswith("|"):
        return "strong"
    return "weak"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--manifest", default="harness.yaml")
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    man_path = a.manifest if os.path.isabs(a.manifest) else os.path.join(repo, a.manifest)
    if not os.path.exists(man_path):
        print(f"ERROR: manifest 없음: {man_path}", file=sys.stderr)
        sys.exit(2)
    m = load_yaml(man_path)

    fails, warns = [], []
    def p(path): return os.path.join(repo, path)

    roles = m.get("roles", {})

    # 1) implemented 역할 path 존재
    for name, r in roles.items():
        if not isinstance(r, dict):
            continue
        if r.get("implemented") and r.get("path") and not os.path.exists(p(r["path"])):
            fails.append("[role] %s: implemented=true 인데 경로 없음 → %s" % (name, r["path"]))

    # 2) artifacts 존재
    for k, v in (m.get("artifacts") or {}).items():
        if not os.path.exists(p(v)):
            warns.append("[artifact] %s: 경로 없음 → %s" % (k, v))

    # 3) 문서 참조 vs 미구현 역할 (팬텀 에이전트)
    scan = (m.get("doc_reference_scan") or {}).get("files", [])
    phantom_tokens = {}
    for name, r in roles.items():
        if isinstance(r, dict) and r.get("implemented") is False:
            akas = r.get("aka", [])
            if isinstance(akas, str):
                akas = [akas]
            for tok in set([name] + akas):
                phantom_tokens.setdefault(tok, name)

    doc_text = {}
    for f in scan:
        fp = p(f)
        if not os.path.exists(fp):
            warns.append("[scan] 문서 없음 → %s" % f)
            continue
        doc_text[f] = open(fp, encoding="utf-8", errors="replace").read()
        for tok, role in phantom_tokens.items():
            strong, weak = [], []
            rx = re.compile(r"(?<![\w-])" + re.escape(tok) + r"(?![\w-])")
            for ln, line in enumerate(doc_text[f].splitlines(), 1):
                if rx.search(line):
                    (strong if classify_hit(line, tok) == "strong" else weak).append(str(ln))
            if strong:
                fails.append("[phantom-agent] '%s'(역할 %s, 미구현)가 %s:%s 에서 참조됨 → 구현하거나 참조 제거"
                             % (tok, role, f, ",".join(strong[:6])))
            if weak:
                warns.append("[phantom-agent?] '%s'가 %s:%s 에 산문으로 언급됨 (라우팅 참조 아닐 수 있음 — 사람 확인)"
                             % (tok, f, ",".join(weak[:6])))

    # 4) 문서가 인용한 경로 실재 검사 (팬텀 경로)
    prs = m.get("path_reference_scan") or {}
    n_paths = 0
    if prs.get("enabled"):
        ign = [re.compile(x) for x in (prs.get("ignore") or [])]
        local_only = set(prs.get("local_only") or [])
        names, tops = repo_index(repo)

        # local_only: 리포에 커밋하지 않는 개인 작업기록. 부재는 정상이지만,
        # .gitignore 에 없으면 계약("필수 산출물")과 어긋나 실수로 커밋된다 → 그건 FAIL.
        for lo in sorted(local_only):
            try:
                rc = subprocess.run(["git", "-C", repo, "check-ignore", "-q", lo]).returncode
            except Exception:
                rc = 1
            if rc != 0:
                fails.append("[local-only] %s는 로컬 전용으로 선언됐으나 .gitignore에 없음 "
                             "→ 실수로 커밋될 수 있음" % lo)
            elif not os.path.exists(p(lo)):
                warns.append("[local-only] %s 없음 — 개인 작업기록이라 정상이나, "
                             "계약상 세션 종료 시 갱신 대상" % lo)
        pat = re.compile(r"`([^`\n]+)`")
        hits = {}
        for f in (prs.get("files") or scan):
            text = doc_text.get(f)
            if text is None:
                fp = p(f)
                if not os.path.exists(fp):
                    warns.append("[scan] 문서 없음 → %s" % f)
                    continue
                text = open(fp, encoding="utf-8", errors="replace").read()
            for ln, line in enumerate(text.splitlines(), 1):
                for tok in pat.findall(line):
                    t = tok.strip().rstrip(",.)")
                    if " " in t or "<" in t:
                        continue
                    if not re.match(r"^[\w./\-]+$", t):
                        continue
                    if "/" not in t and "." not in t:
                        continue
                    if any(rx.search(t) for rx in ign):
                        continue
                    if t in local_only:
                        continue
                    if os.path.exists(p(t)):
                        continue
                    base = os.path.basename(t.rstrip("/"))
                    if prs.get("resolve_by_basename", True) and base in names:
                        continue
                    if "/" in t and t.split("/")[0] in tops:
                        continue
                    hits.setdefault(t, []).append("%s:%d" % (f, ln))
        n_paths = len(hits)
        for t in sorted(hits):
            fails.append("[phantom-path] '%s'가 실재하지 않는데 문서가 참조 → %s"
                         % (t, ", ".join(hits[t][:4])))

    # 5) repo 루트 실행 전제
    if (m.get("execution") or {}).get("require_repo_root"):
        if not (os.path.exists(p(".git")) or os.path.exists(p("CLAUDE.md"))):
            fails.append("[execution] require_repo_root=true 이나 repo 루트(.git/CLAUDE.md) 아님")

    print("harness_doctor: repo=%s" % repo)
    print("  roles=%d  artifacts=%d  scan_files=%d  phantom_paths=%d"
          % (len(roles), len(m.get("artifacts") or {}), len(scan), n_paths))
    for w in warns:
        print("  WARN %s" % w)
    for e in fails:
        print("  FAIL %s" % e)
    if fails:
        print("\nRESULT: FAIL (%d 문제, %d 경고)" % (len(fails), len(warns)))
        sys.exit(1)
    print("\nRESULT: PASS (%d 경고)" % len(warns))
    sys.exit(0)


if __name__ == "__main__":
    main()
