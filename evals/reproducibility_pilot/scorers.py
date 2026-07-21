"""Deterministic scorers for the BIOP01 reproducibility regression (사전등록 예측 #1–#6).

Pure python — stdlib only, no numpy/pandas/scipy and no inspect_ai import here, so that:
  1. the scoring logic is testable without an eval harness AND without a velo-* env,
  2. `run_pilot.py` (fallback runner), `run_real_artifacts.py` (real scorecard adapter)
     and `reproducibility_pilot.py` (Inspect eval) share exactly one implementation.

Each scorer takes a parsed *reproducibility report* dict (see README §"Report shape")
and returns a Verdict.

Status vocabulary: pass | caution | fail | not_applicable
  — `pass`/`fail`/`not_applicable` mirror the 채점기's ✅PASS / ❌FAIL / ⚠️N/A
    (`cross_dataset/p3_prereg_gse205117.py::verdict`).
  — `caution` is this eval's addition, and it is NOT an invented threshold: it names the
    band BETWEEN the prereg's pass threshold and the prereg's own 반증(falsification)
    criterion, both of which are stated numbers. See ALPHA_* / LAG_* below.

⚠️ THRESHOLD PROVENANCE — nothing here is invented by this eval.
   CLAUDE.md forbids a checking layer from setting its own thresholds, so every number is
   quoted from the sealed pre-registration and its scorer:

     T1/T2/T3/T4  <- pipeline/hspc-velocity-benchmark/cross_dataset/p3_prereg_gse205117.py
                     (봉인된 임계, "변경 금지 — 바꾸면 git에 남는다")
     반증 기준     <- pipeline/hspc-velocity-benchmark/manuscript/PREREGISTRATION_gse205117.md
                     §"반증 기준 (틀리면 틀렸다고 보고 — 사후 구제 금지)"

   NOTE (실물이 정본): the harness memo §5.2 illustrates the scorer with "예: 전사속도 α
   0.88 기준선". 0.88 is the HSPC *observed* α concordance, not a gate. The sealed
   threshold is ρ ≥ 0.50 (T1). This eval uses the sealed 0.50. See README §2.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Verdict:
    status: str
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"status": self.status, "reasons": self.reasons}


# ---------------------------------------------------------------------------
# 봉인된 임계 (p3_prereg_gse205117.py L#'봉인된 임계' 블록과 1:1)
# ---------------------------------------------------------------------------
T1_ALPHA_WITHIN = 0.50   # 예측1: within cross-method α ρ ≥ 0.50
T2_LAG_WITHIN = 0.15     # 예측2: within cross-method lag ρ ≤ 0.15 (≈0)
T3_DELTA_RHO = 0.35      # 예측3: Δρ = ρ_α − ρ_lag ≥ 0.35
T4_CROSS_ALPHA = 0.20    # 예측4: cross α > +0.20 且 cross α > cross lag

# 반증 기준 (PREREGISTRATION_gse205117.md §반증 기준) — 프로젝트 주장이 깨지는 지점.
#   "α cross-method ρ < 0.30 → α robustness 실패(전체 논지 약화) → 정직 보고."
#   "lag cross-method ρ ≥ 0.50 → 'priming best-case에서도 fragile' 실패."
ALPHA_FALSIFY = 0.30
LAG_FALSIFY = 0.50

# ⚠️ DIRECTIONALITY — the single easiest thing to get backwards in this suite.
#   α  : pass = HIGH ρ (≥0.50). 전사속도는 method 간 재현된다(robust leg).
#   lag: pass = LOW  ρ (≤0.15). chromatin→transcription lag은 재현되지 *않는다*(fragile leg).
#   The project's headline finding IS the non-reproducibility of lag, so a HIGH lag ρ
#   FALSIFIES the claim. Inverting either direction inverts every verdict in this file.


def load_report(path: str | Path) -> dict[str, Any]:
    """Load a reproducibility report, stripping harness-only keys.

    `_case_meta` is fixture scaffolding, not part of the report shape. It must never be
    scored — its prose describes the defect under test.
    """
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    doc.pop("_case_meta", None)
    return doc


def _rows(report: dict[str, Any], section: str) -> list[dict[str, Any]]:
    sec = (report.get("sections") or {}).get(section)
    return sec if isinstance(sec, list) else []


def _median(vals: list[float]) -> float:
    s = sorted(vals)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def _num(v: Any) -> float | None:
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


# ---------------------------------------------------------------------------
# 예측 1 — within-dataset cross-method α 재현 (robust leg)
#   사전 임계: Spearman ρ ≥ 0.50 ; 채점 규칙 R1: pair가 셋이라 **median**을 헤드라인으로.
# ---------------------------------------------------------------------------

def score_alpha_reproducibility(report: dict[str, Any]) -> Verdict:
    rows = _rows(report, "within_alpha")
    if not rows:
        return Verdict("not_applicable", ["section 'within_alpha' absent — α fit pair 없음"])

    rhos: list[float] = []
    for r in rows:
        v = _num(r.get("rho"))
        if v is None:
            return Verdict("fail", [f"within_alpha['{r.get('label')}'] rho 누락/비수치 — 수치 없이 통과 불가"])
        rhos.append(v)

    med = _median(rhos)
    detail = ", ".join(f"{r.get('label')} {_num(r.get('rho')):+.3f}" for r in rows)

    # R1: median of the (up to 3) α pairs is the headline — macrophage 보고 전례와 동일.
    if med < ALPHA_FALSIFY:
        return Verdict(
            "fail",
            [f"α median ρ={med:+.3f} < 반증 기준 {ALPHA_FALSIFY} → α robustness 실패"
             f"(전체 논지 약화, 정직 보고 대상) [{detail}]"],
        )
    if med < T1_ALPHA_WITHIN:
        return Verdict(
            "caution",
            [f"α median ρ={med:+.3f} < 사전 임계 {T1_ALPHA_WITHIN}(예측1 미달)이나 "
             f"반증 기준 {ALPHA_FALSIFY} 이상 — 예측1 FAIL, 논지 반증은 아님 [{detail}]"],
        )
    return Verdict(
        "pass",
        [f"α median ρ={med:+.3f} ≥ {T1_ALPHA_WITHIN} (예측1 PASS) [{detail}]"],
    )


# ---------------------------------------------------------------------------
# 예측 2 — within-dataset cross-method lag 재현 (fragile leg)
#   사전 임계: Spearman ρ ≤ 0.15 (≈0). 크기(rank)만 비교 — MV 부호는 구조적 양수(무정보).
# ---------------------------------------------------------------------------

# pair label 토큰 → canonical method. 'MV×VAE', 'floor×MV', 'moflow×mvvae' 등이 실제로 쓰인다.
_METHOD_ALIASES = {
    "mv": "multivelo", "multivelo": "multivelo",
    "vae": "multivelovae", "mvvae": "multivelovae", "multivelovae": "multivelovae",
    "moflow": "moflow", "mof": "moflow",
    "crak": "crakvelo", "crakvelo": "crakvelo",
    "floor": "floor", "scvelo_floor": "floor", "rna_only_floor": "floor",
}

# 부호가 **구조적 상수**인 method — 부호 검정에 들어가면 검정이 무효가 된다.
# MultiVelo만 해당: lag = fit_t_sw2 − fit_t_sw1 이고 4-state가 switch time을 단조 정렬하므로
# 부호가 정의상 항상 +다(concordance.md §1: lag>0 비율 100.0%, n=538).
CONSTANT_SIGN_METHODS = {"multivelo"}


def _pair_methods(label: str) -> list[str]:
    """'MV×VAE' -> ['multivelo', 'multivelovae']. 정확 토큰 매칭(부분문자열 아님)."""
    out: list[str] = []
    for tok in re.split(r"[×x*/,\s]+", label.strip()):
        canon = _METHOD_ALIASES.get(tok.strip().lower())
        if canon:
            out.append(canon)
    return out


def _pair_has_constant_sign_method(label: str) -> bool:
    return any(m in CONSTANT_SIGN_METHODS for m in _pair_methods(label))


def score_lag_fragility(report: dict[str, Any]) -> Verdict:
    rows = _rows(report, "within_lag")
    if not rows:
        return Verdict("not_applicable", ["section 'within_lag' absent — chromatin-aware pair 없음"])

    r = rows[0]  # R2: floor에 lag이 없으므로 MV×VAE 단일 pair. 모호성 없음.
    rho = _num(r.get("rho"))
    if rho is None:
        return Verdict("fail", [f"within_lag['{r.get('label')}'] rho 누락/비수치 — 수치 없이 통과 불가"])

    # Guardrail — sign 검정의 유효성. 규칙은 "부호 검정 금지"가 **아니다**:
    #   clean_concordance_gate.md §3은 {moflow, mvvae} 부호 검정을 "valid but power-bounded"로,
    #   {multivelo, moflow, mvvae}를 "INVALID"로 판정한다. 차이는 **상수-부호 method의 포함 여부**다.
    #   §0: MultiVelo lag(fit_t_sw2 − fit_t_sw1)은 4-state 단조정렬 탓에 100% 양수 = 구조적 상수 →
    #   부호 검정에 넣으면 null을 잘못 설정하고 통계량을 편향시킨다.
    # 따라서 상수-부호 method가 낀 부호 검정만 무효(fail)로 잡는다.
    if r.get("test") == "sign_agreement":
        pair = str(r.get("label") or "")
        # 어느 method가 검정에 들어갔나는 **pair**가 정한다(method_set 전체가 아니라).
        # 부분문자열 매칭 금지: 'mvvae'가 'MV'를 포함하므로 substring으로 보면 MultiVeloVAE를
        # MultiVelo로 오인한다. 토큰을 정확히 정규화한다.
        if _pair_has_constant_sign_method(pair):
            return Verdict(
                "fail",
                [f"within_lag['{pair}'] test='sign_agreement' 에 상수-부호 method(MultiVelo)가 포함 — "
                 f"MultiVelo lag 부호는 4-state 단조정렬로 구조적 양수(무정보)라 null을 잘못 설정하고 "
                 f"통계량을 편향시킨다. INVALID 검정(clean_concordance_gate.md §0/§3)"],
            )
        # 부호 가변 method만의 부호 검정은 유효하다. 다만 sign-agreement %는 T2가 규율하는 ρ가
        # 아니므로 임계로 채점하지 않는다(범주 오류 방지) — 사람이 볼 수 있게 caution으로 표면화.
        return Verdict(
            "caution",
            [f"within_lag['{pair}'] test='sign_agreement' (상수-부호 method 없음) — 유효하나 "
             f"2-method 부호 검정은 검정력 제한(power-bounded, min p≈0.50; clean_concordance_gate.md §3). "
             f"sign-agreement %는 T2(ρ ≤ {T2_LAG_WITHIN})가 규율하는 통계량이 아니라 임계 채점 불가"],
        )

    if rho >= LAG_FALSIFY:
        return Verdict(
            "fail",
            [f"lag 크기 rank ρ={rho:+.3f} ≥ 반증 기준 {LAG_FALSIFY} → lag이 재현된다 = "
             f"'priming best-case에서도 fragile' 실패. 핵심 주장이 이 시스템에서 깨짐(정직 보고, "
             f"사후 임계 하향 금지)"],
        )
    if rho > T2_LAG_WITHIN:
        return Verdict(
            "caution",
            [f"lag 크기 rank ρ={rho:+.3f} > 사전 임계 {T2_LAG_WITHIN}(예측2 미달)이나 "
             f"반증 기준 {LAG_FALSIFY} 미만 — 예측2 FAIL, 주장 반증은 아님"],
        )
    return Verdict("pass", [f"lag 크기 rank ρ={rho:+.3f} ≤ {T2_LAG_WITHIN} (예측2 PASS — fragile 유지)"])


# ---------------------------------------------------------------------------
# 예측 3 + 6 — α > lag 순서 (dissociation)
#   사전 임계: Δρ = ρ_α − ρ_lag ≥ 0.35, **동일 gene set에서 paired** (R3 가드레일).
#   예측 6(priming 극대에서도 fragile) = #2 且 #3 → 여기서 #3을 채점한다.
# ---------------------------------------------------------------------------

def score_alpha_lag_dissociation(report: dict[str, Any]) -> Verdict:
    rows = _rows(report, "delta_rho")
    if not rows:
        return Verdict("not_applicable", ["section 'delta_rho' absent — paired Δρ 미산출"])

    d = rows[0]
    dr = _num(d.get("rho"))
    if dr is None:
        return Verdict("fail", ["delta_rho rho 누락/비수치 — 수치 없이 통과 불가"])

    reasons: list[str] = []

    # R3 가드레일: "서로 다른 gene set의 두 ρ를 빼는 것은 금지".
    # paired Δρ는 ρ_α(MV×VAE)와 ρ_lag(MV×VAE)를 **공통 gene**에서 계산해야 한다
    # → delta_rho.n 은 within_lag.n 과 같아야 한다.
    n_dr = d.get("n")
    lag_rows = _rows(report, "within_lag")
    n_lag = lag_rows[0].get("n") if lag_rows else None
    if isinstance(n_dr, int) and isinstance(n_lag, int) and n_dr != n_lag:
        return Verdict(
            "fail",
            [f"paired 위반(R3): Δρ n={n_dr} ≠ within_lag n={n_lag} — 서로 다른 gene set의 두 ρ를 뺐다. "
             f"Δρ는 동일 gene set에서 paired 계산해야 한다(boot_dr)"],
        )

    # 반증 기준: "α > lag 순서 역전(lag ρ > α ρ) → 순서 가설 실패".
    # Δρ = ρ_α − ρ_lag 이므로 Δρ < 0 이 곧 역전이다.
    if dr < 0:
        return Verdict(
            "fail",
            [f"Δρ={dr:+.3f} < 0 → 순서 역전(lag ρ > α ρ) = 순서 가설 실패(반증 기준)"],
        )
    if dr < T3_DELTA_RHO:
        return Verdict(
            "caution",
            [f"Δρ={dr:+.3f} < 사전 임계 {T3_DELTA_RHO}(예측3 미달)이나 순서 역전은 아님(Δρ ≥ 0)"],
        )

    lo = _num(d.get("lo"))
    if lo is not None and lo <= 0:
        reasons.append(f"Δρ 95%CI 하한={lo:+.3f} ≤ 0 — CI가 0을 제외하지 못한다(dissociation 미확정)")
        return Verdict("caution", reasons)

    return Verdict(
        "pass",
        [f"Δρ={dr:+.3f} ≥ {T3_DELTA_RHO} (예측3 PASS){'; CI 하한 %+.3f > 0 — dissociation 성립' % lo if lo is not None else ''}"],
    )


# ---------------------------------------------------------------------------
# 예측 4 — cross-dataset 재현 (HSPC ↔ 대상 데이터셋)
#   사전 임계: cross α > +0.20 且 cross α > cross lag.
#   (braveji 최고위험 지목 항목 — 06008c1 커밋 메시지)
# ---------------------------------------------------------------------------

def score_cross_dataset_replication(report: dict[str, Any]) -> Verdict:
    a_rows = _rows(report, "cross_alpha")
    l_rows = _rows(report, "cross_lag")
    if not a_rows or not l_rows:
        return Verdict("not_applicable", ["cross_alpha/cross_lag 미산출 — cross-dataset 축 없음"])

    x_a = _num(a_rows[0].get("rho"))
    x_l = _num(l_rows[0].get("rho"))
    if x_a is None or x_l is None:
        return Verdict("fail", ["cross_alpha/cross_lag rho 누락/비수치 — 수치 없이 통과 불가"])

    reasons: list[str] = []
    if x_a <= T4_CROSS_ALPHA:
        reasons.append(f"cross α={x_a:+.3f} ≤ 사전 임계 {T4_CROSS_ALPHA:+.2f} — 예측4 FAIL")
    if x_a <= x_l:
        reasons.append(f"cross α={x_a:+.3f} ≤ cross lag={x_l:+.3f} — 순서 조건 위반, 예측4 FAIL")
    if reasons:
        return Verdict("fail", reasons)

    return Verdict(
        "pass",
        [f"cross α={x_a:+.3f} > {T4_CROSS_ALPHA:+.2f} 且 > cross lag={x_l:+.3f} (예측4 PASS)"],
    )


# ---------------------------------------------------------------------------
# 예측 5 — per-gene 재현 격차 + 봉인 준수(사후 구제·조용한 치환 차단)
#   사전 임계: lag 불일치 median > α 불일치 median.
#   봉인된 결정(2026-07-13, kkkim): 예측5는 **MoFlow 원정의**(MV vs `cs_lag_median`, 부호 유지)로 채점.
#   → MoFlow arm 부재 시 MV×VAE 치환은 **봉인된 결정과의 이탈**이며, 조용히 넘어가면 안 된다.
# ---------------------------------------------------------------------------

# The sealed decision names this exact column. 2026-07-14 (a34c10d): the 채점기 asked for
# `cs_lag` — a column that does not exist — and pandas' .get() returned None, so the scorer
# SILENTLY fell back to the MV×VAE substitute and scored 예측5 off the sealed definition.
# The fix made a present-but-wrong-column a hard failure ("추측 금지"). This scorer encodes
# the same discipline at the report level.
MOFLOW_LAG_COL = "cs_lag_median"


def score_prereg_adherence(report: dict[str, Any]) -> Verdict:
    rows = _rows(report, "per_gene_disagree")
    if not rows:
        return Verdict("not_applicable", ["section 'per_gene_disagree' absent — 예측5 미산출"])

    r = rows[0]
    lag_d = _num(r.get("lag_disagree"))
    alpha_d = _num(r.get("alpha_disagree"))
    if lag_d is None or alpha_d is None:
        return Verdict("fail", ["per_gene_disagree의 lag/alpha 불일치 median 누락 — 수치 없이 통과 불가"])

    # (a) 봉인 준수 먼저 — 수치가 좋아 보여도 사전등록대로 잰 수치가 아니면 통과시키지 않는다.
    #     이것이 06008c1(잠정 6 PASS)이 "이탈 명기"를 달고 나온 이유다.
    deviation = report.get("prereg_deviation")
    if deviation:
        return Verdict(
            "caution",
            [f"봉인된 사전등록과의 이탈이 기록됨 → 예측5 채점은 사전등록대로가 아니다: {deviation}"],
        )

    src = r.get("lag_source") or ""
    if MOFLOW_LAG_COL not in src:
        return Verdict(
            "caution",
            [f"예측5 lag_source='{src}' 가 봉인된 원정의(MoFlow `{MOFLOW_LAG_COL}`, 부호 유지)를 명시하지 "
             f"않는다 — 조용한 치환 가능성. 이탈이면 이탈로 기록할 것"],
        )

    # (b) 봉인된 정의로 잰 경우에만 격차를 채점한다.
    if lag_d <= alpha_d:
        return Verdict(
            "fail",
            [f"per-gene 불일치 lag={lag_d:.3f} ≤ α={alpha_d:.3f} — 재현 격차 역전, 예측5 FAIL"],
        )
    return Verdict(
        "pass",
        [f"per-gene 불일치 lag={lag_d:.3f} > α={alpha_d:.3f} (예측5 PASS, 봉인된 MoFlow 원정의로 채점)"],
    )


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

SCORERS = {
    "alpha_reproducibility": score_alpha_reproducibility,        # 예측1
    "lag_fragility": score_lag_fragility,                        # 예측2
    "alpha_lag_dissociation": score_alpha_lag_dissociation,      # 예측3(+6)
    "cross_dataset_replication": score_cross_dataset_replication,  # 예측4
    "prereg_adherence": score_prereg_adherence,                  # 예측5 + 봉인 준수
}
