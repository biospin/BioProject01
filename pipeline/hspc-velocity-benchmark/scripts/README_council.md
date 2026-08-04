# 다중 모델 적대적 검토 절차 (BIOP01-81 항목 3)

headline claim을 여러 모델로 교차검증하는 절차다. `docs/adversarial_multi_llm_council_harness.md`(수동 절차)를 이 저장소에서 돌릴 수 있게 파일 계약과 종합 스크립트로 옮긴 것이다. 설계 근거는 `ai_scientist/02_single_lab_harness.md` §6.1.

## 언제 쓰나

결과 검증 게이트(`p3_*` 재계산)와 인용 무결성 게이트를 통과한 뒤, headline claim이 정말 방어 가능한지 여러 모델로 교차검증할 때. `paper-critic`(단일 검수자)를 보완한다.

## 규율 (원 하네스와 동일)

- 세션은 독립으로 둔다. 다른 세션의 숨은 추론을 공유하지 않고 결과 파일만 넘긴다.
- 자기모델 비판과 타모델 비판을 분리한다.
- 종합은 다수결이 아니다. 근거의 질로 판정한다. 합의를 진실로, 모델 이름을 권위로 삼지 않는다.
- `council_synthesize.py`는 집계·구조화만 한다. 최종 판정은 메타리뷰어(사람 또는 전용 종합 세션)가 한다.

## 파일 계약

각 모델·세션은 검토 결과를 `council_schema.json` 형식의 JSON으로 남긴다(claim은 Proven/Plausible/Speculative/Unsupported/Incorrect, 비판은 Valid-and-Fatal/Valid-but-Fixable/Partially-Valid/Weak/Incorrect/Hallucinated).

```
sessions/
  claude_s1.json    gpt_s1.json    gemini_s1.json      # Stage 1 독립 비판
  claude_on_gpt.json  ...                              # Stage 2 교차 재비판
```

## 실행

```bash
cd pipeline/hspc-velocity-benchmark
# 세션 JSON들을 종합해 메타리뷰 골격 생성 (Valid-and-Fatal 살아남으면 exit 1)
python3 scripts/council_synthesize.py --dir sessions --out /tmp/meta_scaffold.md
```

종합 골격은 claim 판정 집계, 살아남은/폐기된/이견 비판, Fatal 후보를 나눠 보여준다. 메타리뷰어가 이를 근거로 최종 판정(Reject / Major Revision / Conditional Go / Strong Go)을 적는다.

## 현재 실행 가능 범위 (정직한 표기)

- **Claude leg**: 지금 실행 가능. `paper-critic` 또는 별도 Claude 세션으로 Stage 1·2를 돌려 스키마 형식으로 저장한다.
- **GPT · Gemini leg**: **Layer B 멀티모델 워커 인프라에 의존한다(현재 미구축).** `guide/ai-handoff-architecture-guide.md`·`guide/openclaw-claude-guide.md`의 AI 워커(claude/codex/gemini) 경로가 붙으면 자동화된다.
- 그때까지의 운용: (1) Claude 단독 다세션으로 부분 운용하거나, (2) 사람이 GPT·Gemini 세션을 수동 실행해 `council_schema.json` 형식으로 저장한 뒤 `council_synthesize.py`로 종합한다.

## 관련 파일

- `scripts/council_schema.json` — 세션 출력 스키마
- `scripts/council_synthesize.py` — 결정론적 종합(집계, 판정 아님)
- `docs/adversarial_multi_llm_council_harness.md` — 원 수동 절차
