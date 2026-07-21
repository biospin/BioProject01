"""Regenerate cases/ — reproducibility-report fixtures for the BIOP01 pilot.

    python3 build_cases.py

Design: every scorer_validation fixture is the REAL gse205117 report (a verbatim
transcription of results/prereg_gse205117_scorecard.csv) with **one defect injected**.
That keeps each case's expectation derivable from the sealed prereg rather than
reverse-engineered from scorer output, and it means an injected defect is the only
difference between a PASS case and its FAIL twin.

Every number in the control cases is copied from a committed BIOP01 artifact — no
value here is invented. Provenance is recorded per-case in `_case_meta.source`.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).parent
SV = ROOT / "cases" / "scorer_validation"
RC = ROOT / "cases" / "regression_corpus"

BENCH = "pipeline/hspc-velocity-benchmark"

ALL = ["alpha_reproducibility", "lag_fragility", "alpha_lag_dissociation",
       "cross_dataset_replication", "prereg_adherence"]

# ---------------------------------------------------------------------------
# BASE — real GSE205117, transcribed from results/prereg_gse205117_scorecard.csv
# (committed 2026-07-14, 6 PASS / 0 FAIL). Values are verbatim, not rounded.
# ---------------------------------------------------------------------------
GSE205117 = {
    "dataset": "gse205117",
    "description": "mouse gastrulation — 5번째 cross-dataset 사전등록 재현 검정",
    "prereg_source": f"{BENCH}/manuscript/PREREGISTRATION_gse205117.md",
    "scored_by": f"{BENCH}/cross_dataset/p3_prereg_gse205117.py",
    "scorecard": f"{BENCH}/results/prereg_gse205117_scorecard.csv",
    "bootstrap": {"B": 10000, "seed": 20260707},
    "prereg_deviation": None,
    "method_set": ["rna_only_floor", "multivelo", "multivelovae", "moflow"],
    "sections": {
        "within_alpha": [
            {"label": "floor×MV", "n": 846, "rho": 0.9112311980039997,
             "lo": 0.8973243136757327, "hi": 0.9227869301643904},
            {"label": "floor×VAE", "n": 1001, "rho": 0.9270205483139615,
             "lo": 0.9153552237335473, "hi": 0.9365625094354536},
            {"label": "MV×VAE", "n": 969, "rho": 0.9529479951601811,
             "lo": 0.9455666734553594, "hi": 0.9589169557117171},
        ],
        "within_lag": [
            {"label": "MV×VAE", "n": 969, "rho": -0.025870583117979684,
             "lo": -0.08867092320457663, "hi": 0.03821619065064866,
             "test": "magnitude_rank"},
        ],
        "delta_rho": [
            {"label": "MV×VAE", "n": 969, "rho": 0.9788185782781609,
             "lo": 0.9156511165189795, "hi": 1.0414830125754637, "paired": True},
        ],
        "cross_alpha": [
            {"label": "HSPC×gastr", "n": 111, "rho": 0.4149701649701649,
             "lo": 0.24379871724657895, "hi": 0.5606713948575612},
        ],
        "cross_lag": [
            {"label": "HSPC×gastr", "n": 111, "rho": 0.02842225342225342,
             "lo": -0.16526369067500402, "hi": 0.22371266445819063},
        ],
        "per_gene_disagree": [
            {"label": "lag|alpha", "n": 968,
             "lag_disagree": 0.29390495867768596,
             "alpha_disagree": 0.05159958720330238,
             "lag_source": "MoFlow `cs_lag_median` (HSPC 원정의, 부호 유지)"},
        ],
    },
}


def write(d: Path, name: str, doc: dict, meta: dict) -> None:
    out = copy.deepcopy(doc)
    out = {"_case_meta": meta, **out}
    (d / f"{name}.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def base() -> dict:
    return copy.deepcopy(GSE205117)


def main() -> None:
    for d in (SV, RC):
        d.mkdir(parents=True, exist_ok=True)
        for p in d.glob("*.json"):
            p.unlink()

    # ======================= scorer_validation =============================
    # --- negative controls (real artifacts that SHOULD pass) ---------------
    write(SV, "control_real_01_gse205117", base(), {
        "kind": "negative_control",
        "source": f"{BENCH}/results/prereg_gse205117_scorecard.csv (committed 2026-07-14)",
        "intent": "실제 6 PASS / 0 FAIL 산출물. 전 항목 통과해야 한다 — 무조건 FAIL 스코어러를 죽이는 대조군.",
        "expected": {
            "alpha_reproducibility": "pass",       # median +0.927 ≥ 0.50
            "lag_fragility": "pass",               # -0.026 ≤ 0.15
            "alpha_lag_dissociation": "pass",      # Δρ +0.979 ≥ 0.35, CI lo +0.916 > 0, paired n=969=969
            "cross_dataset_replication": "pass",   # α +0.415 > 0.20 且 > lag +0.028
            "prereg_adherence": "pass",            # lag 0.294 > α 0.052, MoFlow 원정의
        },
    })

    # macrophage — real, from results/concordance_macrophage.md (canonical, 2026-07-10)
    mac = {
        "dataset": "macrophage",
        "description": "human macrophage — 4번째 cross-dataset (HSPC 직계 조혈축)",
        "prereg_source": None,
        "scored_by": f"{BENCH}/cross_dataset/p3_concordance_macrophage.py",
        "scorecard": f"{BENCH}/results/concordance_macrophage.md",
        "bootstrap": {"B": 10000, "seed": 20260707},
        "prereg_deviation": None,
        "method_set": ["rna_only_floor", "multivelo", "multivelovae"],
        "sections": {
            "within_alpha": [
                {"label": "floor×MV", "n": 702, "rho": 0.826, "lo": 0.796, "hi": 0.854},
                {"label": "floor×VAE", "n": 709, "rho": 0.865, "lo": 0.839, "hi": 0.887},
                {"label": "MV×VAE", "n": 871, "rho": 0.917, "lo": 0.902, "hi": 0.929},
            ],
            "within_lag": [
                {"label": "MV×VAE", "n": 871, "rho": 0.074, "lo": 0.006, "hi": 0.143,
                 "test": "magnitude_rank"},
            ],
            "delta_rho": [
                {"label": "MV×VAE", "n": 871, "rho": 0.843, "lo": 0.773, "hi": 0.912,
                 "paired": True},
            ],
            "cross_alpha": [
                {"label": "HSPC×macrophage", "n": 274, "rho": 0.643, "lo": 0.554, "hi": 0.719},
            ],
            "cross_lag": [
                {"label": "HSPC×macrophage", "n": 274, "rho": 0.148, "lo": 0.027, "hi": 0.263},
            ],
            # scorecard note: "macrophage(치환 정의): 0.280 vs 0.061" — measured MV×VAE,
            # NOT the HSPC 원정의(MoFlow cs_lag_median). The report says so itself.
            "per_gene_disagree": [
                {"label": "lag|alpha", "n": 871, "lag_disagree": 0.280, "alpha_disagree": 0.061,
                 "lag_source": "MultiVeloVAE 치환 정의"},
            ],
        },
    }
    write(SV, "control_real_02_macrophage", mac, {
        "kind": "negative_control",
        "source": f"{BENCH}/results/concordance_macrophage.md + FINDINGS.md §7-D",
        "intent": (
            "실제 macrophage 재현(4번째 축) — α/lag/Δρ/cross 전부 통과. "
            "단 per-gene 격차는 scorecard가 스스로 '치환 정의'라 명기한 자로 쟀다 → "
            "prereg_adherence가 caution으로 표면화하는 것이 정답(수치 0.280>0.061은 좋아 보여도 "
            "HSPC 원정의로 잰 값이 아니다)."
        ),
        "expected": {
            "alpha_reproducibility": "pass",       # median +0.865
            "lag_fragility": "pass",               # +0.074 ≤ 0.15
            "alpha_lag_dissociation": "pass",      # Δρ +0.843, lo +0.773 > 0, paired 871=871
            "cross_dataset_replication": "pass",   # α +0.643 > 0.20 且 > lag +0.148
            "prereg_adherence": "caution",         # lag_source = 치환 정의
        },
    })

    # HSPC — the reference axis itself (no cross-dataset leg, no paired Δρ published)
    hspc = {
        "dataset": "hspc",
        "description": "human HSPC (GSE209878) — 원 벤치마크 축. 다른 데이터셋의 cross-dataset 기준선.",
        "prereg_source": None,
        "scored_by": f"{BENCH}/scripts/p3_concordance.py + scripts/p3_identifiability_vs_snr.py",
        "scorecard": f"{BENCH}/results/concordance.md",
        "prereg_deviation": None,
        "method_set": ["rna_only_floor", "multivelo", "multivelovae", "moflow", "crakvelo"],
        "sections": {
            "within_alpha": [
                # concordance.md §3 (floor∩MultiVelo shared 368) and §3.6 (MV×VAE shared 538)
                {"label": "floor×MV", "n": 368, "rho": 0.818},
                {"label": "MV×VAE", "n": 538, "rho": 0.882},
            ],
            "within_lag": [
                # concordance.md §3.5 multivelo×multivelovae (shared 538)
                {"label": "MV×VAE", "n": 538, "rho": -0.010, "test": "magnitude_rank"},
            ],
            # per-gene 원정의 — identifiability_vs_snr.md, N=537 4-method 공통
            "per_gene_disagree": [
                {"label": "lag|alpha", "n": 537, "lag_disagree": 0.317, "alpha_disagree": 0.078,
                 "lag_source": "MoFlow `cs_lag_median` (HSPC 원정의, 부호 유지)"},
            ],
        },
    }
    write(SV, "control_real_03_hspc", hspc, {
        "kind": "negative_control",
        "source": f"{BENCH}/results/concordance.md §3/§3.5/§3.6 + results/identifiability_vs_snr.md",
        "intent": (
            "원 벤치마크 축. paired Δρ·cross-dataset leg는 HSPC 자신에 대해 산출되지 않는다 "
            "(HSPC가 cross의 기준축) → 해당 스코어러는 not_applicable이어야 한다. "
            "N/A를 pass로 뭉개지 않는지 확인하는 대조군."
        ),
        "expected": {
            "alpha_reproducibility": "pass",              # median(0.818, 0.882) = 0.850
            "lag_fragility": "pass",                      # -0.010 ≤ 0.15
            "alpha_lag_dissociation": "not_applicable",   # delta_rho 섹션 없음
            "cross_dataset_replication": "not_applicable",  # HSPC = 기준축
            "prereg_adherence": "pass",                   # 0.317 > 0.078, 원정의
        },
    })

    # --- 예측1 (α) FAIL/CAUTION — robust leg ------------------------------
    c = base()
    for r, v in zip(c["sections"]["within_alpha"], [0.19, 0.22, 0.26]):
        r["rho"] = v
    write(SV, "alpha_fail_01_below_falsification", c, {
        "kind": "fail_case",
        "source": "synthetic — 반증 기준 주입",
        "intent": "α median +0.22 < 반증 기준 0.30 → α robustness 실패(전체 논지 약화). 정직 보고 대상.",
        "expected": {"alpha_reproducibility": "fail", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},
    })

    c = base()
    for r, v in zip(c["sections"]["within_alpha"], [0.38, 0.42, 0.46]):
        r["rho"] = v
    write(SV, "alpha_caution_01_band", c, {
        "kind": "caution_case",
        "source": "synthetic — 사전 임계와 반증 기준 사이 band",
        "intent": "α median +0.42 — 예측1(≥0.50) FAIL이나 반증 기준(<0.30)에는 안 걸림 → caution.",
        "expected": {"alpha_reproducibility": "caution", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},
    })

    c = base()
    c["sections"]["within_alpha"][1]["rho"] = None
    write(SV, "alpha_fail_02_rho_missing", c, {
        "kind": "fail_case",
        "source": "synthetic — 수치 누락",
        "intent": "α pair의 ρ가 누락 → 수치 없이 통과시키지 않는다(BIOP02 #2 '수치 누락 → reject'와 같은 규율).",
        "expected": {"alpha_reproducibility": "fail", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},
    })

    # --- 예측2 (lag) FAIL/CAUTION — fragile leg ---------------------------
    # ⚠️ 방향 반대: lag은 HIGH ρ가 실패다.
    c = base()
    c["sections"]["within_lag"][0]["rho"] = 0.62
    c["sections"]["within_lag"][0]["lo"] = 0.55
    c["sections"]["within_lag"][0]["hi"] = 0.69
    c["sections"]["delta_rho"][0]["rho"] = 0.33   # ρ_α(0.953) − ρ_lag(0.62) ≈ 0.33
    c["sections"]["delta_rho"][0]["lo"] = 0.26
    c["sections"]["delta_rho"][0]["hi"] = 0.40
    write(SV, "lag_fail_01_reproducible", c, {
        "kind": "fail_case",
        "source": "synthetic — 반증 기준 주입 (PREREGISTRATION §반증 기준 1행)",
        "intent": (
            "lag ρ +0.62 ≥ 0.50 → lag이 재현된다 = 'priming best-case에서도 fragile' 실패. "
            "핵심 주장이 깨지는 케이스. Δρ도 0.33으로 임계(0.35) 아래 → dissociation caution. "
            "임계를 사후에 낮춰 구제하는 것이 금지된 바로 그 상황."
        ),
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "fail",
                     "alpha_lag_dissociation": "caution", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},
    })

    c = base()
    c["sections"]["within_lag"][0]["rho"] = 0.30
    c["sections"]["within_lag"][0]["lo"] = 0.24
    c["sections"]["within_lag"][0]["hi"] = 0.36
    write(SV, "lag_caution_01_band", c, {
        "kind": "caution_case",
        "source": "synthetic — 사전 임계(0.15)와 반증 기준(0.50) 사이 band",
        "intent": "lag ρ +0.30 — 예측2 FAIL이나 주장 반증은 아님 → caution.",
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "caution",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},
    })

    # 부호 검정의 유효성은 '상수-부호 method 포함 여부'로 갈린다(clean_concordance_gate.md §3).
    # RC-04(MultiVelo 포함 = INVALID)의 대응쌍: 부호 가변 method만의 검정 = valid but power-bounded.
    c = base()
    c["method_set"] = ["moflow", "multivelovae"]
    c["sections"]["within_lag"] = [
        {"label": "moflow×mvvae", "n": 560, "rho": 0.481, "test": "sign_agreement"},
    ]
    del c["sections"]["delta_rho"]
    write(SV, "lag_caution_02_sign_test_power_bounded", c, {
        "kind": "caution_case",
        "source": f"{BENCH}/results/clean_concordance_gate.md §3 표 1행"
                  "('{moflow, mvvae} (clean sign-informative) … 유효하나 검정력 제한(2-method degenerate)')"
                  " + §2('깨끗한 2-method 부호-일치 = 48.1% = 우연 수준')",
        "intent": (
            "부호 **가변** method만의 부호 검정은 INVALID가 아니다 — 유효하되 검정력 제한이다. "
            "RC-04(MultiVelo 포함 → fail)와 갈리는 지점. 또 sign-agreement %(0.481)는 T2가 규율하는 "
            "ρ가 아니므로 임계로 채점하면 범주 오류 → caution으로 표면화한다. "
            "'부호 검정이면 무조건 fail'로 짠 스코어러를 잡는 케이스."
        ),
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "caution",
                     "alpha_lag_dissociation": "not_applicable",
                     "cross_dataset_replication": "pass", "prereg_adherence": "pass"},
    })

    # --- 예측3 (Δρ) FAIL — dissociation + paired 가드레일 -----------------
    c = base()
    c["sections"]["within_alpha"] = [
        {"label": "floor×MV", "n": 846, "rho": 0.55, "lo": 0.49, "hi": 0.61},
        {"label": "floor×VAE", "n": 1001, "rho": 0.57, "lo": 0.51, "hi": 0.63},
        {"label": "MV×VAE", "n": 969, "rho": 0.58, "lo": 0.52, "hi": 0.64},
    ]
    c["sections"]["within_lag"][0]["rho"] = 0.44
    c["sections"]["within_lag"][0]["lo"] = 0.37
    c["sections"]["within_lag"][0]["hi"] = 0.51
    c["sections"]["delta_rho"][0]["rho"] = -0.12   # ρ_lag > ρ_α → 순서 역전
    c["sections"]["delta_rho"][0]["lo"] = -0.21
    c["sections"]["delta_rho"][0]["hi"] = -0.03
    write(SV, "dissoc_fail_01_order_inverted", c, {
        "kind": "fail_case",
        "source": "synthetic — 반증 기준 3행('α > lag 순서 역전 → 순서 가설 실패')",
        "intent": "Δρ −0.12 < 0 → lag이 α보다 재현된다 = 순서 가설 실패. lag +0.44는 caution band.",
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "caution",
                     "alpha_lag_dissociation": "fail", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},
    })

    c = base()
    c["sections"]["delta_rho"][0]["n"] = 604   # within_lag n=969 와 불일치
    write(SV, "dissoc_fail_02_unpaired_gene_set", c, {
        "kind": "fail_case",
        "source": "synthetic — 채점 규칙 R3 가드레일('서로 다른 gene set의 두 ρ를 빼는 것은 금지')",
        "intent": (
            "Δρ n=604 ≠ within_lag n=969 → 서로 다른 gene set의 ρ를 뺐다. "
            "수치(+0.979)는 멀쩡해 보이지만 paired 계산이 아니므로 통과시키면 안 된다."
        ),
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "fail", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},
    })

    c = base()
    c["sections"]["delta_rho"][0]["rho"] = 0.40
    c["sections"]["delta_rho"][0]["lo"] = -0.02   # CI가 0을 제외하지 못함
    c["sections"]["delta_rho"][0]["hi"] = 0.81
    write(SV, "dissoc_caution_01_ci_includes_zero", c, {
        "kind": "caution_case",
        "source": "synthetic — concordance_macrophage.md §A3('헤드라인은 Δρ CI가 0 제외')",
        "intent": "Δρ +0.40 ≥ 0.35이나 95%CI 하한 −0.02 ≤ 0 → dissociation 미확정 → caution.",
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "caution", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},
    })

    # --- 예측4 (cross-dataset) FAIL ---------------------------------------
    c = base()
    c["sections"]["cross_alpha"][0]["rho"] = 0.12
    write(SV, "cross_fail_01_alpha_below_threshold", c, {
        "kind": "fail_case",
        "source": "synthetic — 사전 임계 T4 주입",
        "intent": "cross α +0.12 ≤ +0.20 → 예측4 FAIL(braveji 최고위험 지목 항목).",
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "fail",
                     "prereg_adherence": "pass"},
    })

    c = base()
    c["sections"]["cross_alpha"][0]["rho"] = 0.25
    c["sections"]["cross_lag"][0]["rho"] = 0.31   # cross lag > cross α → 순서 조건 위반
    write(SV, "cross_fail_02_alpha_not_above_lag", c, {
        "kind": "fail_case",
        "source": "synthetic — T4의 두 번째 조건('且 cross α > cross lag')",
        "intent": (
            "cross α +0.25 > +0.20 은 만족하나 cross lag +0.31 이 더 크다 → 순서 조건 위반. "
            "첫 조건만 보는 스코어러를 잡는 케이스."
        ),
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "fail",
                     "prereg_adherence": "pass"},
    })

    # --- 예측5 (per-gene 격차) FAIL ---------------------------------------
    c = base()
    c["sections"]["per_gene_disagree"][0]["lag_disagree"] = 0.048
    c["sections"]["per_gene_disagree"][0]["alpha_disagree"] = 0.091
    write(SV, "prereg_fail_01_gap_inverted", c, {
        "kind": "fail_case",
        "source": "synthetic — 예측5 임계('lag 불일치 > α 불일치') 역전",
        "intent": "per-gene lag 불일치 0.048 ≤ α 0.091 → 재현 격차 역전, 예측5 FAIL.",
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "pass",
                     "prereg_adherence": "fail"},
    })

    # ======================= regression_corpus =============================
    # 실제 BIOP01 재현성 실패 이력(git log). '우리가 실제로 당한 것'만 넣는다.

    # RC-01 — 06008c1 (2026-07-13): MoFlow arm 미배선 → MV×VAE 치환, 잠정 6 PASS
    c = base()
    c["prereg_deviation"] = (
        "봉인된 사전등록(2026-07-13)은 예측5를 MoFlow 원정의로 채점하도록 확정했으나, "
        "results/moflow_genes_gse205117.csv가 없어 MV×VAE로 치환했다. 이 채점은 사전등록대로가 아니다."
    )
    c["sections"]["per_gene_disagree"][0].update({
        "lag_disagree": 0.307, "alpha_disagree": 0.052,
        "lag_source": "MultiVeloVAE 치환 (⚠️ 봉인된 결정과의 이탈)",
    })
    c["method_set"] = ["rna_only_floor", "multivelo", "multivelovae"]
    write(RC, "rc_01_moflow_unwired_vae_substitution", c, {
        "kind": "real_failure",
        "source": "git 06008c1 — 'P3 GSE205117 사전등록 채점(잠정) — 6 PASS / 0 FAIL, 단 예측5는 "
                  "MoFlow 미배선으로 MV×VAE 치환(사전등록 이탈 명기)'",
        "intent": (
            "실제 사건: 채점표는 '6 PASS'로 나왔지만 예측5는 봉인된 정의로 잰 게 아니었다. "
            "이탈이 **기록돼 있으므로** 스코어러가 caution으로 잡아야 한다 — 'PASS 6개'를 그대로 믿으면 안 된다."
        ),
        "caught": True,
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "pass",
                     "prereg_adherence": "caution"},
    })

    # RC-02 — a34c10d (2026-07-14): 컬럼명 cs_lag → 조용한 VAE 폴백. 이탈이 기록되지 '않은' 상태.
    c = base()
    c["prereg_deviation"] = None            # 버그라서 아무도 이탈로 기록하지 못했다 — 그게 핵심
    c["sections"]["per_gene_disagree"][0].update({
        "lag_disagree": 0.307, "alpha_disagree": 0.052,
        "lag_source": "MoFlow `cs_lag_median` (HSPC 원정의, 부호 유지)",   # 보고서의 주장
    })
    write(RC, "rc_02_moflow_colname_silent_fallback", c, {
        "kind": "real_failure",
        "source": "git a34c10d — 'MoFlow 컬럼명 cs_lag→cs_lag_median 오류로 조용한 VAE 폴백(봉인 위반) 차단'",
        "intent": (
            "실제 사건: 채점기가 존재하지 않는 컬럼 `cs_lag`를 찾자 조용히 VAE로 폴백해 봉인을 위반했다. "
            "보고서는 원정의로 쟀다고 **주장**하는데 실제 수치는 치환값이다."
        ),
        "caught": False,
        "expected_is_a_miss": True,
        "needs_scorer": (
            "report-level 스코어러로는 잡을 수 없다 — 보고서가 원정의를 주장하고 이탈도 기록되지 않아 "
            "겉보기에 정상이다. 이 결함은 **artifact 층**에서만 잡힌다: p3_prereg_gse205117.py가 "
            "'파일은 있는데 컬럼이 없으면 하드 실패(추측 금지)'로 고쳐졌다(a34c10d). "
            "→ eval의 한계이자, 왜 채점기의 hard-fail이 필요한지의 근거."
        ),
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},   # ← MISS. 통과시켜버린다.
    })

    # RC-03 — a34c10d: abs() 버그. HSPC 원정의는 부호 유지인데 abs를 씌워 0.317 → 0.295 드리프트.
    c = copy.deepcopy(hspc)
    c["sections"]["per_gene_disagree"][0].update({
        "lag_disagree": 0.295,   # abs 버전. 커밋된 정본은 0.317.
        "lag_source": "MoFlow `cs_lag_median` (abs 적용 — 원정의는 부호 유지)",
    })
    write(RC, "rc_03_abs_lag_definition_drift", c, {
        "kind": "real_failure",
        "source": "git a34c10d — 'abs() 제거(HSPC 원정의는 부호 유지) … HSPC 커밋값 0.317/0.078 정확 "
                  "재현 검증(abs 버전은 0.295로 어긋남)'",
        "intent": (
            "실제 사건: lag 정의에 abs()를 씌우자 HSPC per-gene 불일치가 0.317 → 0.295로 드리프트했다. "
            "정의가 조용히 바뀌었는데 lag > α 순서는 그대로라 예측5는 여전히 PASS다."
        ),
        "caught": False,
        "expected_is_a_miss": True,
        "needs_scorer": (
            "임계 비교(lag > α)는 정의 드리프트에 둔감하다 — 0.295도 0.078보다 크므로 PASS. "
            "필요한 것은 **커밋된 기준값과의 정확 재현 대조**(0.317 ± 허용오차)이며, 이는 "
            "lag_source 문자열이 아니라 정본 수치를 아는 회귀 baseline이 있어야 한다. "
            "→ 다음 단계(README §6-2): 데이터셋별 canonical 수치 baseline 도입."
        ),
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "not_applicable",
                     "cross_dataset_replication": "not_applicable",
                     "prereg_adherence": "pass"},   # ← MISS.
    })

    # RC-04 — clean_concordance_gate.md §0/§3: 상수-부호 method(MultiVelo)를 부호 검정에 투입 = INVALID
    c = base()
    c["sections"]["within_lag"] = [
        {"label": "MV×VAE", "n": 628, "rho": 0.31, "test": "sign_agreement"},
    ]
    del c["sections"]["delta_rho"]
    write(RC, "rc_04_multivelo_in_sign_test", c, {
        "kind": "real_failure",
        "source": f"{BENCH}/results/clean_concordance_gate.md §0 + §3 표 2행"
                  "('{multivelo, moflow, mvvae} … INVALID (MultiVelo 상수 부호가 검정을 편향)')",
        "intent": (
            "실제 사건: MultiVelo lag 부호는 4-state 단조정렬로 **구조적 양수**라 무정보인데 "
            "부호-일관성 검정에 넣으면 null을 잘못 설정하고 통계량을 편향시킨다. "
            "clean_concordance_gate가 이를 INVALID로 판정했다. 스코어러가 검정 종류를 보고 잡아야 한다."
        ),
        "caught": True,
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "fail",
                     "alpha_lag_dissociation": "not_applicable",
                     "cross_dataset_replication": "pass", "prereg_adherence": "pass"},
    })

    # RC-05 — clean_concordance_gate.md §4: 헤드라인의 CRAK 의존
    c = base()
    c["method_set"] = ["moflow", "crakvelo", "multivelovae"]
    c["headline_claim"] = "0/598 agreement-set (FDR<0.10)"
    write(RC, "rc_05_crak_dependent_headline", c, {
        "kind": "real_failure",
        "source": f"{BENCH}/results/clean_concordance_gate.md §4"
                  "('0/598 agreement-set은 단지 CRAK에 오염된 것이 아니라 본질적으로 CRAK에 의존한다')",
        "intent": (
            "실제 사건: 헤드라인 통계량이 우리가 버그로 지적한 arm(CRAK-Velo)에 본질적으로 의존했다 → "
            "민감도 분석으로 강등 필요."
        ),
        "caught": False,
        "expected_is_a_miss": True,
        "needs_scorer": (
            "이 파일럿 5개 스코어러 중 method_set을 보는 것이 없다 → 놓친다. "
            "필요한 것은 'headline 통계량이 buggy arm에 의존하는가' 스코어러이며, 그러려면 "
            "arm별 신뢰 상태(어느 arm이 buggy인가)가 기계가 읽을 수 있는 정본으로 있어야 한다 "
            "— 현재 BIOP01엔 그런 파일이 없다(crakvelo_sign_check.md는 산문). "
            "→ 범위 밖(README §5), 다음 단계 후보."
        ),
        "expected": {"alpha_reproducibility": "pass", "lag_fragility": "pass",
                     "alpha_lag_dissociation": "pass", "cross_dataset_replication": "pass",
                     "prereg_adherence": "pass"},   # ← MISS.
    })

    # RC-06 — env 재현성 갭. 이 eval의 대상이 아님(파이프라인/인프라 스모크).
    write(RC, "rc_06_env_lock_uncommitted", {
        "dataset": "hspc",
        "description": "env 재현성 갭 — scv-preprocess.lock.yml 미커밋 + Dockerfile stale env명(velo-*)",
        "prereg_source": None,
        "prereg_deviation": None,
        "method_set": ["multivelo", "multivelovae", "moflow"],
        "sections": {},
    }, {
        "kind": "out_of_scope",
        "source": "git 48c1728('BIOP01-22 재현성 갭 2건 해소 — scv-preprocess.lock.yml 커밋 + "
                  "Dockerfile velo-* 개명 반영') + 7f38b23('stale env 파일명(velo-*) 정정 + "
                  "MoFlow/MultiVeloVAE 커밋 핀')",
        "intent": (
            "실제 재현성 실패지만 **concordance 지표 실패가 아니다** — 환경이 고정되지 않아 재현이 "
            "사람 기억에 의존한 사건이다. 이 eval은 산출된 지표 보고서를 채점하므로 섹션이 비어 있고 "
            "전 스코어러가 not_applicable이어야 한다."
        ),
        "caught": False,
        "expected_is_a_miss": True,
        "needs_scorer": (
            "eval이 아니라 **파이프라인/인프라 스모크**의 대상이다(하네스 리뷰 §1.2가 긋는 바로 그 선: "
            "'1~3은 eval이 아니라 파이프라인 스모크 회귀로 잡아야 한다'). "
            "ClawBio 재현성 계약(commands.sh + environment.yml + checksums.sha256, 리뷰 §4.1.2)이 "
            "이 층의 후보다. → 범위 밖(README §5)."
        ),
        "expected": {k: "not_applicable" for k in ALL},
    })

    n_sv = len(list(SV.glob("*.json")))
    n_rc = len(list(RC.glob("*.json")))
    print(f"wrote {n_sv} scorer_validation + {n_rc} regression_corpus cases")


if __name__ == "__main__":
    main()
