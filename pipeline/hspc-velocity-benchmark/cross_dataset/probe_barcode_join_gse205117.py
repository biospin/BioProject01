#!/usr/bin/env python3
"""GSE205117 GEX(STARsolo, whitelist=None) ↔ ATAC(fragments) 바코드 조인 de-risk (E7.5).

MultiVelo는 RNA·ATAC 세포를 짝지어야 성립 → 바코드 매핑이 전체 build의 관문.
STARsolo는 whitelist=None(관측 16bp 그대로), ATAC fragments는 cellranger-arc 산출 바코드.
세 후보 매핑을 GEX *called* 세포(Gene/filtered/barcodes.tsv, E7.5 ~8595)에 대해 실측 교집합으로 판정:

  (1) direct        : fragment 바코드에서 '-1' suffix 제거 후 그대로
  (2) revcomp       : fragment 바코드의 역상보
  (3) ARC translate : gex↔atac 737K-arc-v1 화이트리스트 위치대응(디스크에 없으면 skip, 보고)

가장 큰 교집합(~8.5k 기대)을 내는 매핑이 정답. 전부 실패면 GSE metadata 바코드파일 존재 확인 후 BLOCKED.

실행: conda run -n scv-preprocess python cross_dataset/probe_barcode_join_gse205117.py
"""
from __future__ import annotations
import gzip
import subprocess
from pathlib import Path
from collections import Counter

GEX_FILT = Path("/home/kkkim/data/gse205117_fullB/gex_solo/SRR19450575/"
                "SRR19450575_Solo.out/Gene/filtered/barcodes.tsv")
FRAG = Path("/home/kkkim/data/gse205117_fullB/atac_frag/"
            "GSM6205427_E7.5_rep1_ATAC_fragments.tsv.gz")

_COMP = str.maketrans("ACGTN", "TGCAN")
def revcomp(s: str) -> str:
    return s.translate(_COMP)[::-1]


def sample_frag_barcodes(path: Path, n: int = 2_000_000) -> Counter:
    """fragments 앞부분 n 줄에서 바코드(col4) 빈도 표본."""
    c = Counter()
    seen = 0
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            c[parts[3]] += 1
            seen += 1
            if seen >= n:
                break
    return c


def main():
    gex = set(l.strip() for l in open(GEX_FILT) if l.strip())
    print(f"GEX called cells (E7.5): {len(gex)}  예: {list(gex)[:3]}")
    if not FRAG.exists():
        print(f"[대기] fragments 아직 없음: {FRAG}"); return 1
    fc = sample_frag_barcodes(FRAG)
    frag_bcs = set(fc)
    print(f"fragments 표본 고유 바코드: {len(frag_bcs)}  예(빈도상위): "
          f"{[b for b, _ in fc.most_common(3)]}")
    # suffix 관찰
    ex = next(iter(frag_bcs))
    print(f"fragment 바코드 예시='{ex}' (len={len(ex)}, '-1' suffix? {ex.endswith('-1')})")

    def strip1(b: str) -> str:
        return b[:-2] if b.endswith("-1") else b

    frag_direct = set(strip1(b) for b in frag_bcs)
    frag_rc = set(revcomp(strip1(b)) for b in frag_bcs)

    ov_direct = len(gex & frag_direct)
    ov_rc = len(gex & frag_rc)
    print("\n=== 매핑 후보 교집합 (GEX called ∩ fragment 표본) ===")
    print(f"(1) direct  : {ov_direct} / {len(gex)}  ({100*ov_direct/len(gex):.1f}%)")
    print(f"(2) revcomp : {ov_rc} / {len(gex)}  ({100*ov_rc/len(gex):.1f}%)")

    # (3) ARC translate — 화이트리스트 있으면
    wl = None
    for cand in ["737K-arc-v1", "arc-v1"]:
        r = subprocess.run(["bash", "-c", f"find /home/kkkim /opt -iname '*{cand}*' 2>/dev/null | head"],
                           capture_output=True, text=True)
        if r.stdout.strip():
            wl = r.stdout.strip().splitlines()
            break
    if wl:
        print(f"(3) ARC whitelist 발견: {wl}")
    else:
        print("(3) ARC translate: gex↔atac 737K-arc-v1 화이트리스트 디스크에 없음 → skip. "
              "direct/revcomp가 실패할 때만 필요(그때 다운로드).")

    best = max([("direct", ov_direct), ("revcomp", ov_rc)], key=lambda x: x[1])
    print(f"\n>>> 최적 매핑 = {best[0]} (교집합 {best[1]}). "
          f"{'GO — build에 이 매핑 사용' if best[1] > 0.5*len(gex) else 'WEAK — ARC translate 또는 metadata 확인 필요'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
