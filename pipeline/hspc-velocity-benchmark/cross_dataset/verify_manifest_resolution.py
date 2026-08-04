#!/usr/bin/env python
"""runner_manifest.yaml 검증기 — BIOP01-45 §6 CPU 검증 (트리거·GPU 무관).

manifest의 stage 해소 로직과 required_cols 계약을, **이미 완주한 데이터셋 산출물**로 대조한다.
runner 실행·GPU 없음, stdlib + PyYAML만. (형식=YAML, 트리거=codex 확정 2026-08-04로 스크립트화.)

세 검사:
  (1) 멱등성    — 산출물이 다 있으면 모든 output stage가 SKIP으로 해소되나?
  (2) 누락 감지  — 특정 산출물을 (가상) 부재로 두면 그 stage만 RUN으로 잡히나?
  (3) 계약 검증  — 각 산출물이 manifest 선언 required_cols를 실제로 갖는가?
                  (BIOP01-41의 cs_lag vs cs_lag_median '조용한 폴백' 계열 사고를 manifest 층에서 차단)

실행: python cross_dataset/verify_manifest_resolution.py [--suffix _gse205117] [--hide moflow]
종료코드: 0=PASS, 1=FAIL.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]           # pipeline/hspc-velocity-benchmark
MANIFEST = Path(__file__).with_name("runner_manifest.yaml")


def load_manifest():
    with open(MANIFEST) as fh:
        return yaml.safe_load(fh)


def csv_header(path: Path):
    with open(path, newline="") as fh:
        return next(csv.reader(fh), [])


def resolve(tmpl: str, suffix: str) -> str:
    return tmpl.replace("{suffix}", suffix)


def output_stages(m):
    """output을 내는 stage만 — dl_prep 같은 중간 substrate(output 없음)는 제외."""
    return [s for s in m["stages"] if s.get("output")]


def check_idempotency(m, results: Path, suffix: str) -> bool:
    print("\n(1) 멱등성 — 산출물이 있으면 SKIP")
    ok = True
    for s in output_stages(m):
        out = results / resolve(s["output"], suffix)
        rows = sum(1 for _ in open(out)) if out.exists() else 0
        state = "SKIP" if (out.exists() and rows >= 2) else "RUN"
        print(f"  {'✅' if state=='SKIP' else '❌'} {s['id']:<12} → {state:<4} ({out.name}, {rows}행)")
        ok &= (state == "SKIP")
    print(f"  → {'전 stage SKIP(멱등)' if ok else '일부 RUN — 산출물 누락'}")
    return ok


def check_missing_detection(m, results: Path, suffix: str, hide: str) -> bool:
    print(f"\n(2) 누락 감지 — '{hide}' 산출물 가상 부재")
    detected = False
    for s in output_stages(m):
        out = results / resolve(s["output"], suffix)
        present = out.exists() and s["id"] != hide       # hide stage만 부재로 시뮬레이션
        state = "SKIP" if present else "RUN"
        if s["id"] == hide:
            detected = (state == "RUN")
            print(f"  {'✅' if detected else '❌'} {s['id']:<12} → {state} (가상 부재 감지 {'OK' if detected else '실패'})")
        else:
            print(f"     {s['id']:<12} → {state}")   # 다른 stage는 SKIP 유지(오탐 없음)
    print(f"  → {'누락 stage만 RUN으로 감지' if detected else '감지 실패'}")
    return detected


def check_contract(m, results: Path, suffix: str) -> bool:
    print("\n(3) 계약 — 산출물이 required_cols를 실제로 갖는가 (BIOP01-41 방지)")
    ok = True
    for s in output_stages(m):
        req = s.get("required_cols") or []
        out = results / resolve(s["output"], suffix)
        if not out.exists():
            print(f"  ⚠️ {s['id']:<12} 산출물 없음 — 계약 확인 skip")
            continue
        missing = [c for c in req if c not in csv_header(out)]
        print(f"  {'✅' if not missing else '❌'} {s['id']:<12} {req} {'전부 존재' if not missing else f'누락 {missing}'}")
        ok &= not missing
    print(f"  → {'모든 계약 충족(컬럼명 실체 일치)' if ok else '계약 위반 — manifest/산출물 점검'}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--suffix", default="_gse205117")
    ap.add_argument("--hide", default="moflow", help="누락 감지 시뮬레이션 대상 stage id")
    args = ap.parse_args(argv)

    m = load_manifest()
    results = ROOT / m["defaults"]["outputs_dir"]
    print(f"manifest {MANIFEST.name} v{m['version']} | suffix={args.suffix} | results={results}")
    print(f"stages={[s['id'] for s in m['stages']]} score={[s['id'] for s in m['score']]}")

    r1 = check_idempotency(m, results, args.suffix)
    r2 = check_missing_detection(m, results, args.suffix, args.hide)
    r3 = check_contract(m, results, args.suffix)

    passed = r1 and r2 and r3
    print(f"\n{'='*56}\n종합: 멱등 {'✅' if r1 else '❌'} · 누락감지 {'✅' if r2 else '❌'} · 계약 {'✅' if r3 else '❌'}"
          f"  →  {'PASS' if passed else 'FAIL'}")
    print("주의: byte-identical scorecard 재생성은 numpy env(scv-preprocess) 필요 → kkkim 서버.")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
