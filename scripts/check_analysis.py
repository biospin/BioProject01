#!/usr/bin/env python3
"""#11 (경량): 분석 산출물 구조 검증 — 재분석 없이 breakage 탐지.

각 paper(analysis/*/*/paper-info.yaml)에 대해:
  - paper-info.yaml 파싱 가능?
  - 필수 산출물 4종(core/lens-academic/lens-industry/methodology-brief) 존재?
  - sources/ 디렉토리 존재?
그리고 _index/papers.csv 행 수 == paper dir 수 (build_index 정합).

사용: python3 scripts/check_analysis.py   (실패 시 exit 1 → CI에서 차단)
의존: PyYAML.
"""
import csv
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML 필요: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["_core.md", "_lens-academic.md", "_lens-industry.md", "_methodology-brief.md"]


def main():
    papers = sorted(ROOT.glob("analysis/*/*/paper-info.yaml"))
    fails = []
    for y in papers:
        d = y.parent
        pid = d.name
        errs = []
        try:
            yaml.safe_load(y.read_text(encoding="utf-8"))
        except Exception as e:
            errs.append(f"paper-info.yaml 파싱 실패: {e}")
        for suf in REQUIRED:
            if not (d / f"{pid}{suf}").exists():
                errs.append(f"누락: {pid}{suf}")
        if not (d / "sources").is_dir():
            errs.append("sources/ 없음")
        if errs:
            fails.append((pid, errs))

    idx = ROOT / "analysis/_index/papers.csv"
    n_idx = None
    if idx.exists():
        try:
            n_idx = len(list(csv.DictReader(idx.open(encoding="utf-8"))))
        except Exception as e:
            fails.append(("_index", [f"papers.csv 파싱 실패: {e}"]))
    if n_idx is not None and n_idx != len(papers):
        fails.append(("_index", [f"papers.csv 행 {n_idx} != paper dir {len(papers)} — build_index.py 재실행 필요"]))

    print(f"검증: paper dir {len(papers)}편 | index rows {n_idx}")
    for pid, errs in fails:
        for e in errs:
            print(f"  ✗ {pid}: {e}")
    if fails:
        print(f"FAIL — {len(fails)}개 항목")
        return 1
    print("✓ OK — 모든 paper 구조 정상")
    return 0


if __name__ == "__main__":
    sys.exit(main())
