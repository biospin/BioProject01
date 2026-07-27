"""Inspect eval suite — BIOP01 재현성 회귀 (사전등록 예측 #1–#5).

Formalizes braveji's reproducibility regression as an Inspect eval, per 하네스 점검 §5.2
("지용기님의 재현성 회귀 테스트를 Inspect eval 스위트로 형식화 … scorer = 4종 교차 재현
일치도 ≥ 임계값") and 하네스 리뷰 §2. 2단계 — 1단계 BIOP02 파일럿(evals/critic_pilot)의
구조를 그대로 재사용하고 내용만 BIOP01(재현 일치도)로 바꿨다(리뷰 §3의 층 분할).

The checks are DETERMINISTIC — they read a reproducibility report and apply the sealed
pre-registration's own thresholds. No LLM is involved, so the eval runs with the built-in
mock model and needs no API key:

    /opt/envs/spatialpatho/bin/inspect eval reproducibility_pilot.py --model mockllm/model

⚠️ ENV NOTE: inspect_ai lives in the spatialpatho env because BIOP01's velo-* envs do not
   have it and must not be touched (CLAUDE.md: velo-* ↔ spatialpatho 통합·rename 금지).
   spatialpatho is used here ONLY as the eval TOOL runtime — this eval imports nothing from
   BIOP02 and reads only BIOP01 files. It is not a BIOP01 pipeline dependency: the same
   scorers run under bare `python3 run_pilot.py`, which is the durable proof.

This is deliberate rather than an LLM judge: 예측1–5 are numeric threshold comparisons with
exact answers, and CLAUDE.md's anti-self-reference rule forbids a checking layer from
setting its own thresholds — every number is quoted from p3_prereg_gse205117.py and
PREREGISTRATION_gse205117.md, not invented by a model.

Tasks:
    repro_alpha_reproducibility      -> 예측1 (α robust leg, pass = HIGH ρ)
    repro_lag_fragility              -> 예측2 (lag fragile leg, pass = LOW ρ)
    repro_alpha_lag_dissociation     -> 예측3/6 (Δρ, paired 가드레일)
    repro_cross_dataset_replication  -> 예측4
    repro_prereg_adherence           -> 예측5 + 봉인 준수
    repro_regression_corpus          -> 실제 재현성 실패 6건 coverage 측정
"""

from __future__ import annotations

import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.scorer import CORRECT, INCORRECT, Score, Target, accuracy, scorer, stderr
from inspect_ai.solver import Generate, TaskState, solver

from scorers import SCORERS, load_report

ROOT = Path(__file__).parent
SV_DIR = ROOT / "cases" / "scorer_validation"
RC_DIR = ROOT / "cases" / "regression_corpus"


def _build_dataset(dirs: list[Path], scorer_name: str) -> MemoryDataset:
    samples: list[Sample] = []
    for d in dirs:
        for p in sorted(d.glob("*.json")):
            with open(p, encoding="utf-8") as f:
                doc = json.load(f)
            meta = doc.get("_case_meta")
            if not meta or scorer_name not in (meta.get("expected") or {}):
                continue
            samples.append(
                Sample(
                    input=f"Apply 사전등록 예측 '{scorer_name}' to {p.name}",
                    target=meta["expected"][scorer_name],
                    id=p.stem,
                    metadata={
                        "case_path": str(p),
                        "scorer_name": scorer_name,
                        "kind": meta.get("kind", ""),
                        "intent": meta.get("intent", ""),
                        "expected_is_a_miss": meta.get("expected_is_a_miss", False),
                    },
                )
            )
    return MemoryDataset(samples)


@solver
def apply_prereg_prediction():
    """Runs the deterministic prereg scorer. Never calls the model."""

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        fn = SCORERS[state.metadata["scorer_name"]]
        report = load_report(state.metadata["case_path"])
        verdict = fn(report)
        state.output.completion = verdict.status
        state.metadata["reasons"] = verdict.reasons
        return state

    return solve


@scorer(metrics=[accuracy(), stderr()])
def prereg_verdict_match():
    """Correct iff the scorer's verdict equals the prereg-derived expectation."""

    async def score(state: TaskState, target: Target) -> Score:
        predicted = (state.output.completion or "").strip()
        expected = target.text.strip()
        reasons = "; ".join(state.metadata.get("reasons", [])) or "(no reasons)"
        return Score(
            value=CORRECT if predicted == expected else INCORRECT,
            answer=predicted,
            explanation=f"expected={expected} predicted={predicted} :: {reasons}",
            metadata={
                "kind": state.metadata.get("kind"),
                "expected_is_a_miss": state.metadata.get("expected_is_a_miss"),
            },
        )

    return score


def _item_task(scorer_name: str) -> Task:
    return Task(
        dataset=_build_dataset([SV_DIR, RC_DIR], scorer_name),
        solver=apply_prereg_prediction(),
        scorer=prereg_verdict_match(),
    )


@task
def repro_alpha_reproducibility() -> Task:
    """예측1 — within-dataset cross-method α 재현 (ρ ≥ 0.50). pass = HIGH ρ."""
    return _item_task("alpha_reproducibility")


@task
def repro_lag_fragility() -> Task:
    """예측2 — within-dataset cross-method lag 재현 (ρ ≤ 0.15). pass = LOW ρ (fragile leg)."""
    return _item_task("lag_fragility")


@task
def repro_alpha_lag_dissociation() -> Task:
    """예측3/6 — Δρ = ρ_α − ρ_lag ≥ 0.35, 동일 gene set paired (R3 가드레일)."""
    return _item_task("alpha_lag_dissociation")


@task
def repro_cross_dataset_replication() -> Task:
    """예측4 — cross α > +0.20 且 cross α > cross lag."""
    return _item_task("cross_dataset_replication")


@task
def repro_prereg_adherence() -> Task:
    """예측5 — per-gene 재현 격차 + 봉인된 MoFlow 원정의 준수(조용한 치환 차단)."""
    return _item_task("prereg_adherence")


@task
def repro_regression_corpus() -> Task:
    """Coverage over the 6 REAL BIOP01 reproducibility failures only.

    ⚠️ HOW TO READ THIS TASK'S SCORE: a high score does NOT mean the failures were caught.
    RC-02/03/05/06 carry expected='pass'/'not_applicable' precisely BECAUSE this pilot
    provably does not cover silent column-name fallback, lag-definition drift, buggy-arm
    dependence, or env locking. 'Correct' here means 'the scorer behaved as the gap
    analysis predicts'. The finding lives in cases/regression_corpus/*.json ->
    _case_meta.needs_scorer and in the coverage table printed by run_pilot.py.
    Real result: 6건 중 2건 적발 / 4건 미적발.
    """
    samples: list[Sample] = []
    for scorer_name in SCORERS:
        samples.extend(_build_dataset([RC_DIR], scorer_name).samples)
    for s in samples:
        s.id = f"{s.id}::{s.metadata['scorer_name']}"
    return Task(
        dataset=MemoryDataset(samples),
        solver=apply_prereg_prediction(),
        scorer=prereg_verdict_match(),
    )
