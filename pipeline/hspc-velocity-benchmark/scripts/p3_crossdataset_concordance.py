#!/usr/bin/env python3
"""P3 cross-dataset concordance — BIOP01 벤치마크(HSPC) lag/timing이 외부 데이터셋에서 재현되나.

RUNBOOK §7의 개념("HSPC 상위 lag gene이 새 dataset에서도 일관적인가")을 실제 컬럼으로 구현한다.
RUNBOOK §7 스니펫은 `switch_time` 컬럼을 쓰지만 MultiVelo csv엔 그 컬럼이 없다(fit_t_sw1/2/3뿐) —
scaffold 의사코드였음. 여기서 실제 컬럼으로 교정한다.

비교 축 (shared gene에서 Spearman rank):
  - headline: MultiVelo **lag 크기** = fit_t_sw2 − fit_t_sw1  (pseudotime, chromatin→transcription)
  - sanity : MultiVelo switch timing fit_t_sw2 / RNA-only floor timing fit_t_
성공 기준(RUNBOOK §7): |Spearman| > 0.3 → 단일 replication 외부 재현 성공.

⚠️ caveat (p3_concordance.py와 동일 서사, 무인 산출이라 반드시 보존):
  - MultiVelo 4-state는 t_sw1<t_sw2<t_sw3 **단조 정렬** → sw2−sw1은 정의상 항상 양수.
    즉 **sign은 무정보(구조적 아티팩트), 여기 비교는 lag *크기*의 gene간 rank 재현성**이다.
  - 단일 외부 데이터셋 replication 1건 — 강한 일반화 주장 금지.
  - cross-dataset per-gene concordance는 두 데이터셋이 서로 다른 spliced/unspliced를 쓰므로
    noise만 추가 → 낮은 rho는 "lag fragile"에 보수적, 높은 rho는 강한 신호.

실행: conda run -n scv-preprocess python p3_crossdataset_concordance.py [--dataset human_brain]
      [--hspc-mv PATH --new-mv PATH ...]  (검증용 경로 override)
출력: results/concordance_<dataset>.md
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RESULTS = Path(__file__).resolve().parent.parent / "results"
MIN_SHARED = 10   # 이 미만이면 rho 비정보 처리


def load(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    d = pd.read_csv(path, index_col=0)
    return d[d["fit_likelihood"].notna()] if "fit_likelihood" in d.columns else d


def rank_line(a: pd.Series, b: pd.Series, label: str) -> tuple[str, float | None, int]:
    """shared index에서 Spearman. shared<MIN_SHARED면 비정보 표시."""
    sh = sorted(set(a.dropna().index) & set(b.dropna().index))
    n = len(sh)
    if n < MIN_SHARED:
        return (f"- **{label}**: shared {n} (<{MIN_SHARED}) → 비정보(생략)", None, n)
    rho, p = spearmanr(a.loc[sh].astype(float), b.loc[sh].astype(float))
    verdict = "재현✅(|r|>0.3)" if abs(rho) > 0.3 else "약함/미재현(|r|≤0.3)"
    return (f"- **{label}** (shared {n}): Spearman **{rho:+.3f}** (p={p:.2g}) → {verdict}", float(rho), n)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="human_brain")
    ap.add_argument("--hspc-mv", default=None)
    ap.add_argument("--new-mv", default=None)
    ap.add_argument("--hspc-floor", default=None)
    ap.add_argument("--new-floor", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    ds = a.dataset

    hspc_mv_p = Path(a.hspc_mv) if a.hspc_mv else RESULTS / "multivelo_genes.csv"
    new_mv_p = Path(a.new_mv) if a.new_mv else RESULTS / f"multivelo_genes_{ds}.csv"
    hspc_fl_p = Path(a.hspc_floor) if a.hspc_floor else RESULTS / "rna_only_dynamical_genes.csv"
    new_fl_p = Path(a.new_floor) if a.new_floor else RESULTS / f"rna_only_dynamical_genes_{ds}.csv"
    out_md = Path(a.out) if a.out else RESULTS / f"concordance_{ds}.md"

    hspc_mv, new_mv = load(hspc_mv_p), load(new_mv_p)
    hspc_fl, new_fl = load(hspc_fl_p), load(new_fl_p)

    L = [f"# P3 cross-dataset concordance — HSPC ↔ {ds}", "",
         "> BIOP01 HSPC 벤치마크의 MultiVelo lag/timing이 외부 multiome({ds})에서 rank 재현되나.".format(ds=ds),
         "> 성공 기준(RUNBOOK §7): |Spearman| > 0.3 (단일 replication).", "",
         "## 입력",
         f"- HSPC MultiVelo: `{hspc_mv_p.name}` — " + (f"{len(hspc_mv)} gene" if hspc_mv is not None else "**없음**"),
         f"- {ds} MultiVelo: `{new_mv_p.name}` — " + (f"{len(new_mv)} gene" if new_mv is not None else "**없음**"),
         f"- HSPC floor: `{hspc_fl_p.name}` — " + (f"{len(hspc_fl)} gene" if hspc_fl is not None else "없음"),
         f"- {ds} floor: `{new_fl_p.name}` — " + (f"{len(new_fl)} gene" if new_fl is not None else "없음"),
         ""]

    if hspc_mv is None or new_mv is None:
        L += ["", "⚠️ MultiVelo csv 한쪽 이상 없음 → concordance 계산 불가. 종료."]
        out_md.write_text("\n".join(L), encoding="utf-8")
        print("\n".join(L)); print("MultiVelo 입력 부족 — 종료"); return 1

    rhos = {}
    L += ["## MultiVelo 일치도 (headline = lag 크기)", ""]
    # headline: lag magnitude rank
    hl_lag = (hspc_mv["fit_t_sw2"] - hspc_mv["fit_t_sw1"])
    nl_lag = (new_mv["fit_t_sw2"] - new_mv["fit_t_sw1"])
    line, rho, n = rank_line(hl_lag, nl_lag, "lag(fit_t_sw2−fit_t_sw1) 크기 rank  ← headline")
    L.append(line); rhos["mv_lag"] = rho
    # sanity: switch timing
    line, rho, n = rank_line(hspc_mv["fit_t_sw2"], new_mv["fit_t_sw2"], "switch timing fit_t_sw2 rank")
    L.append(line); rhos["mv_t_sw2"] = rho
    # rate sanity
    for prm in ["fit_alpha", "fit_beta", "fit_gamma"]:
        if prm in hspc_mv.columns and prm in new_mv.columns:
            line, rho, n = rank_line(hspc_mv[prm], new_mv[prm], f"rate {prm} rank")
            L.append(line)
    L.append("")

    # floor sanity
    L += ["## RNA-only floor 일치도 (sanity, chromatin 무관)", ""]
    if hspc_fl is not None and new_fl is not None and "fit_t_" in hspc_fl.columns and "fit_t_" in new_fl.columns:
        line, rho, n = rank_line(hspc_fl["fit_t_"], new_fl["fit_t_"], "floor timing fit_t_ rank")
        L.append(line); rhos["floor_t"] = rho
    else:
        L.append("- floor csv 한쪽 없음 → skip")
    L.append("")

    # 판정 요약
    hl = rhos.get("mv_lag")
    L += ["## 판정", ""]
    if hl is None:
        L.append("- shared gene 부족 → **비정보**. 외부 재현 판정 불가.")
    else:
        L.append(f"- **headline lag-크기 rank Spearman = {hl:+.3f}** → "
                 + ("**외부 재현 성공** (|r|>0.3, 단일 replication 기준)" if abs(hl) > 0.3
                    else "**재현 약함/미확인** (|r|≤0.3)"))
    L += ["",
          "## caveat (필수)",
          "- MultiVelo 4-state는 t_sw 단조 정렬 → lag sign은 **구조적 양수(무정보)**. 이 비교는 lag *크기*의 gene간 **rank 재현성**만 본다(방향 아님).",
          "- 단일 외부 데이터셋 replication 1건 — 강한 일반화 주장 금지.",
          "- 두 데이터셋은 서로 다른 spliced/unspliced 원천 → cross-dataset noise가 rho를 보수적으로 낮춤. 낮은 rho=lag fragile에 보수적, 높은 rho=강한 신호.",
          "- within-lineage(진짜 timing)가 아닌 *전역* fit rank 비교 — brain lineage annotation 무관하게 계산됨.", ""]

    out_md.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n✓ → {out_md.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
