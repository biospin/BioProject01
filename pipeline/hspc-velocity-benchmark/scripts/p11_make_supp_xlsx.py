#!/usr/bin/env python
"""
Additional file용 csv -> xlsx 변환 (BIOP01-61 포함4).

`manuscript/SUPPLEMENTARY.md`의 매니페스트에 등재된 csv를 투고용 xlsx로 만든다.
여러 csv를 묶는 Additional file은 **한 파일 안 여러 시트**로 넣는다(BMC 관례).
원본 csv는 건드리지 않는다. 존재하지 않는 원천은 만들어내지 않고 MISSING으로 보고한다.
"""
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "results")
OUT = os.path.join(R, "supp_xlsx")

# Additional file 번호 -> (파일명 stem, [(시트명, csv 상대경로), ...])
SPEC = {
    1:  ("AdditionalFile1_TableS1_datasets",        [("S1_datasets", "supp_dataset_inventory.csv")]),
    2:  ("AdditionalFile2_TableS2_velocity_arms",   [("S2_arms", "supp_velocity_arms_inventory.csv")]),
    3:  ("AdditionalFile3_TableS3_direction",       [("S3_direction", "per_gene_direction_by_method.csv")]),
    4:  ("AdditionalFile4_TableS4_unanimous",       [("S4_unanimous", "unanimous_chromatin_genes.csv")]),
    5:  ("AdditionalFile5_TableS5_stiffness",       [("S5_stiffness", "stiffness_all_params.csv")]),
    6:  ("AdditionalFile6_TableS6_concordance",     [("S6_concordance", "concordance_shared.csv")]),
    7:  ("AdditionalFile7_TableS7_external_rates",  [("alpha_TTseq", "external_rate_validation_alpha.csv"),
                                                     ("gamma_halflife", "external_rate_validation_gamma.csv"),
                                                     ("alpha_Schwalb", "external_rate_validation_schwalb.csv")]),
    8:  ("AdditionalFile8_TableS8_tertile",         [("S8_tertile", "curvature_tertile_validation.csv")]),
    9:  ("AdditionalFile9_TableS9_coupling",        [("S9_coupling", "coupling_per_gene.csv")]),
    10: ("AdditionalFile10_DataS1_prereg_scorecard", [("scorecard", "prereg_gse205117_scorecard.csv")]),
    12: ("AdditionalFile12_TableS10_velocity_matrix", [("HSPC_pairs", "velocity_matrix_audit_pairs.csv"),
                                                       ("external_pairs", "velocity_matrix_audit_external_pairs.csv")]),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    made, missing = [], []
    for n, (stem, sheets) in sorted(SPEC.items()):
        present = [(s, p) for s, p in sheets if os.path.exists(os.path.join(R, p))]
        for s, p in sheets:
            if not os.path.exists(os.path.join(R, p)):
                missing.append(f"AF{n}: {p}")
        if not present:
            continue
        dest = os.path.join(OUT, stem + ".xlsx")
        with pd.ExcelWriter(dest, engine="openpyxl") as xw:
            for s, p in present:
                df = pd.read_csv(os.path.join(R, p))
                # 엑셀 시트명은 31자 제한
                df.to_excel(xw, sheet_name=s[:31], index=False)
        made.append((n, os.path.basename(dest),
                     [(s, len(pd.read_csv(os.path.join(R, p)))) for s, p in present]))
        print(f"AF{n:<2} -> {os.path.basename(dest)}  "
              + " | ".join(f"{s}({len(pd.read_csv(os.path.join(R,p)))} rows)" for s, p in present),
              flush=True)

    print(f"\n생성 {len(made)}개 파일 -> {OUT}")
    if missing:
        print("!! 원천 없음(만들어내지 않음):")
        for m in missing:
            print("   ", m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
