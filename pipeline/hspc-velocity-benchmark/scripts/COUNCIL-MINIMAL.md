# 다중 모델 적대적 검토 — 최소 운용본 설계 (BIOP01-81 항목3 보완)

> kkkim 제안(2026-08-06). 이건규 님 `README_council.md`·`council_synthesize.py`·`council_schema.json`
> 위에 **팀 접근 현실에 맞춘 right-size 운용본**을 얹는다. 새 인프라를 짓지 않고 기존 계약을 재사용한다.
> 원 설계(3모델×4세션=12 + 종합)는 `docs/adversarial_multi_llm_council_harness.md`.

## 왜 최소본이 필요한가 (접근 현실)

| 모델 | 팀 접근 | 카운슬 leg |
|---|---|---|
| Claude | **전원 Claude Max** | Claude leg — 지금 실행 가능(다세션) |
| GPT | kkkim **Codex Pro**·일부 | GPT leg — **codex CLI 로 실행 가능**(설치·인증 확인, BIOP01-45). full openclaw 워커 불요 |
| Gemini | 이건규 님만(비싼 모델 전부) | Gemini leg — 선택. 있으면 추가, 없으면 생략 |

원 문서도 "토큰 과다·미최적화"라고 했다. 그래서 **12세션 풀버전을 강제하지 않고, 2모델(Claude+GPT)로 축소한 최소본을 기본**으로 두고, Gemini 가 있으면 leg 를 더한다.

## 최소 운용본 (2모델, 5세션)

원 12세션 → **5세션**으로 축소. 규율(세션 독립·자기/타모델 분리·다수결 금지·결과파일만 전달)은 원본 그대로.

```
Stage 1 (독립 원본 비판)   Claude s1 · GPT(codex) s1               → 2
Stage 2 (교차 재비판)      Claude-on-GPT · GPT(codex)-on-Claude    → 2   (자기비판은 최소본에서 생략)
Stage 3 (최종 종합)        ★ 최고 토큰 Claude(Opus) 1세션           → 1
```

- **오케스트레이터/최종 검수 = 가장 토큰 큰 모델(Claude Opus)** — 원 문서 §10·사용자 지침. 13개 입력을 다 읽어 근거 질로 판정하는 자리라 최고 성능이 필요.
- Gemini 가용 시: Stage1 에 gemini_s1, Stage2 에 상호 leg 추가 → 원 풀버전으로 자연 확장. **스키마·종합기는 그대로**라 leg 만 붙이면 됨.

## 기존 자산 재사용 (새로 안 만듦)

- 세션 출력 = `council_schema.json` 형식 JSON 그대로.
- 종합 = `council_synthesize.py --dir sessions`(집계·Fatal 후보, 판정 아님) 그대로. Valid-and-Fatal 생존 시 exit 1.
- 신규로 필요한 것은 **GPT 세션을 codex 로 돌리는 얇은 래퍼 1개**뿐(BIOP01-45 codex 실증이 선행). Claude 세션은 별도 Claude 창/`paper-critic` 로 수동 실행.

## 검수 하네스(1층)와의 관계

카운슬은 **2층**(페르소나 적대검토)이고, 방법론(RESULT_VALIDATION §8)이 "1층 재료가 갖춰진 뒤 붙인다"고 못 박았다. 순서:

```
결정론 게이트(1층: p3 재계산·check_manuscript_numbers·verify_citations·check_claims_ledger)  ← 방금 검수 하네스로 검증됨
        ↓ 통과분만
카운슬(2층: 2모델 5세션 적대검토)  → council_synthesize
        ↓
같은 승격 사다리(§7): CONTRADICTED/Reject → 차단, SUPPORTED/Go → 사람 승인
```

러너를 하나로 합치지 않는다. **리포트 계약만 공유**한다(1층 6판정, 2층 Reject~Strong Go 를 같은 승격 사다리로).

## 선결 (착수 조건)

1. **BIOP01-45 codex 실증** — codex 가 openai.yaml 을 완주하는지 확인(kkkim 서버). 되면 GPT leg 자동화 가능.
2. 그 전까지 운용: Claude 다세션(수동) + GPT 세션 수동(codex 대화) → `council_schema.json` 저장 → `council_synthesize.py` 종합.
3. 우선순위: 검수 하네스(1층) 완성·BIOP02 이식이 먼저. 카운슬은 1층이 선 뒤.
