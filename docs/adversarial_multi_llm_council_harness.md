# Adversarial Multi-LLM Council Harness
## 3 Models × 4 Independent Sessions

## 0. 목적

첨부한 연구 아이디어 문서를 대상으로 다중 LLM 적대적 검토를 수행한다.

이 작업의 목적은 아이디어를 친절하게 개선하거나 옹호하는 것이 아니다.

목표는 다음과 같다.

1. 아이디어의 논리적·수학적·통계적·생물학적 약점을 최대한 공격한다.
2. 서로 다른 모델과 독립 세션이 동일한 결론에 도달하는지 확인한다.
3. 각 모델이 자기 비판과 타 모델 비판을 모두 수행하게 한다.
4. 비판 자체의 오류, 과장, 문헌 누락, 환각도 다시 검증한다.
5. 최종적으로 아이디어가 폐기되어야 하는지, 수정 가능한지, 연구 가치가 남는지를 판정한다.

각 세션은 가능한 한 독립적으로 실행한다.  
사용 가능한 모델 중 각 플랫폼의 가장 높은 성능 모델을 선택한다.

---

# 1. 전체 구조

사용할 모델은 다음 세 종류다.

- Claude
- GPT
- Gemini

각 모델은 서로 다른 네 개의 독립 세션을 사용한다.

따라서 총 심사 세션 수는 다음과 같다.

```text
Claude:  4 sessions
GPT:     4 sessions
Gemini:  4 sessions
--------------------
Total:  12 sessions
```

이후 별도의 오케스트레이터 세션이 12개 결과를 종합한다.

---

# 2. Stage 1 — 원본 독립 비판

먼저 세 모델이 원본 연구 아이디어만 받고 독립적으로 비판한다.

```text
Claude Session 1  → Original Critique by Claude
GPT Session 1     → Original Critique by GPT
Gemini Session 1  → Original Critique by Gemini
```

이 단계에서는 다른 모델의 평가를 공유하지 않는다.

각 모델은 원본 아이디어만 읽고 독립적인 적대적 리뷰를 작성한다.

## Stage 1 산출물

1. `01_claude_original_critique.md`
2. `02_gpt_original_critique.md`
3. `03_gemini_original_critique.md`

---

# 3. Stage 2 — 모델별 3방향 재비판

Stage 1의 세 원본 비판이 모두 완료되면 다음 자료를 하나의 검토 패키지로 구성한다.

- 원본 연구 아이디어
- Claude의 원본 비판
- GPT의 원본 비판
- Gemini의 원본 비판

이 동일한 패키지를 각 모델의 새로운 독립 세션 세 개에 제공한다.

각 모델은 다음 세 역할을 각각 별도의 세션에서 수행한다.

1. 자기 모델의 원본 비판을 비판하는 세션
2. 다른 모델 A의 원본 비판을 비판하는 세션
3. 다른 모델 B의 원본 비판을 비판하는 세션

같은 세션 안에서 세 리뷰를 한꺼번에 평가하지 않는다.

---

## 3.1 Claude의 세 개 재비판 세션

```text
Claude Session 2
→ Claude의 원본 비판을 재비판
→ Self-Critique

Claude Session 3
→ GPT의 원본 비판을 비판

Claude Session 4
→ Gemini의 원본 비판을 비판
```

산출물:

4. `04_claude_on_claude.md`
5. `05_claude_on_gpt.md`
6. `06_claude_on_gemini.md`

---

## 3.2 GPT의 세 개 재비판 세션

```text
GPT Session 2
→ GPT의 원본 비판을 재비판
→ Self-Critique

GPT Session 3
→ Claude의 원본 비판을 비판

GPT Session 4
→ Gemini의 원본 비판을 비판
```

산출물:

7. `07_gpt_on_gpt.md`
8. `08_gpt_on_claude.md`
9. `09_gpt_on_gemini.md`

---

## 3.3 Gemini의 세 개 재비판 세션

```text
Gemini Session 2
→ Gemini의 원본 비판을 재비판
→ Self-Critique

Gemini Session 3
→ Claude의 원본 비판을 비판

Gemini Session 4
→ GPT의 원본 비판을 비판
```

산출물:

10. `10_gemini_on_gemini.md`
11. `11_gemini_on_claude.md`
12. `12_gemini_on_gpt.md`

---

# 4. 세션 독립성 규칙

모든 재비판은 별도의 새 세션에서 수행한다.

각 세션은 자신에게 배정된 하나의 원본 비판만 직접 심사 대상으로 삼는다.

다만 사실관계 확인과 문맥 파악을 위해 다음 전체 패키지는 함께 제공한다.

- 원본 연구 아이디어
- Claude 원본 비판
- GPT 원본 비판
- Gemini 원본 비판

각 세션에는 다음 역할을 명시한다.

> 당신의 주된 심사 대상은 지정된 하나의 리뷰다.  
> 다른 리뷰들은 비교 및 사실 검증을 위한 참고자료일 뿐이다.  
> 세 리뷰를 종합하거나 최종 결론을 작성하지 말라.

이 규칙을 통해 각 재비판의 초점이 흐려지는 것을 방지한다.

---

# 5. Stage 1 원본 비판 프롬프트

각 모델의 첫 번째 세션에 다음 지시를 제공한다.

```text
첨부된 연구 아이디어를 적대적 학술 심사자의 관점에서 검토하라.

당신의 목적은 아이디어를 개선하거나 옹호하는 것이 아니라,
현재 형태의 아이디어가 왜 틀렸거나 불완전할 수 있는지 최대한 엄격하게 밝히는 것이다.

ICML, NeurIPS, ICLR, Nature Machine Intelligence,
Bioinformatics 또는 유사 수준 학술지의 회의적인 리뷰어처럼 행동하라.

다음을 반드시 검토하라.

1. 핵심 주장과 실제로 검증 가능한 가설의 구분
2. 숨겨진 전제
3. 논리적 비약과 순환논증
4. 수학적 정의의 부재 또는 오류
5. uncertainty, noise, latent variable의 개념 혼동
6. 식별 가능성 문제
7. 통계적 confounding
8. 데이터 누수와 batch effect
9. 생물학적 타당성
10. 알려진 pathway와 새로운 biology의 구분 가능성
11. latent embedding을 biology로 오인할 위험
12. 기존 연구 대비 novelty
13. 반증 가능한 실험 설계
14. 실패할 가능성이 가장 높은 지점
15. 논문으로서의 채택 가능성

모든 주장을 다음 중 하나로 분류하라.

- Proven
- Plausible
- Speculative
- Unsupported
- Incorrect

가능하면 관련 문헌을 확인하고 정확한 출처를 제시하라.
확인하지 못한 문헌이나 사실을 만들어내지 말라.

친절한 표현보다 정확성을 우선하라.
비판의 강도를 낮추지 말라.
```

---

# 6. Stage 2 재비판 프롬프트

각 재비판 세션에는 원본 아이디어와 세 개의 Stage 1 리뷰를 제공하고, 심사할 리뷰 하나를 명시한다.

```text
첨부 자료에는 다음이 포함되어 있다.

1. 원본 연구 아이디어
2. Claude의 원본 비판
3. GPT의 원본 비판
4. Gemini의 원본 비판

당신의 주된 심사 대상은 다음 리뷰다.

[TARGET REVIEW]

당신은 원본 연구 아이디어를 다시 심사하는 것이 아니라,
지정된 리뷰의 타당성과 품질을 적대적으로 검증해야 한다.

다음을 확인하라.

1. 리뷰가 원본 아이디어를 정확히 이해했는가?
2. 존재하지 않는 주장을 공격한 부분이 있는가?
3. 비판이 논리적으로 유효한가?
4. 수학적 또는 통계적 오류가 있는가?
5. uncertainty와 hidden biology를 잘못 동일시했는가?
6. 식별 가능성 문제를 정확히 설명했는가?
7. 생물학적 검증 가능성을 과소평가하거나 과대평가했는가?
8. 관련 문헌을 누락했는가?
9. 인용한 연구가 실제 주장을 지지하는가?
10. 비판 중 단순한 수사와 실제 치명적 결함을 구분했는가?
11. 지나치게 낙관적이거나 지나치게 비관적인 판단이 있는가?
12. 어떤 비판은 유효하고 어떤 비판은 폐기되어야 하는가?

각 비판 항목을 다음 중 하나로 판정하라.

- Valid and Fatal
- Valid but Fixable
- Partially Valid
- Weak
- Incorrect
- Hallucinated or Unsupported

마지막에 반드시 다음을 작성하라.

- 이 리뷰에서 유지해야 할 핵심 비판
- 삭제해야 할 잘못된 비판
- 추가해야 할 누락된 비판
- 수정 후 리뷰의 최종 판정
- 원본 아이디어에 대한 직접적인 새 종합은 하지 말 것

다른 두 리뷰는 비교와 사실 검증에만 사용하라.
세 리뷰 전체를 종합하지 말라.
```

---

# 7. Stage 3 — 최종 종합

12개의 결과가 모두 나온 후, 별도의 오케스트레이터 세션이 다음 자료를 모두 받는다.

- 원본 연구 아이디어
- Stage 1 원본 비판 3개
- Stage 2 재비판 9개

총 13개 입력 문서를 기반으로 최종 종합을 수행한다.

오케스트레이터는 단순 다수결을 해서는 안 된다.

모델 수가 아니라 근거의 질, 논리적 유효성, 문헌 근거, 반증 가능성을 기준으로 판단한다.

---

# 8. 최종 종합 프롬프트

```text
당신은 적대적 다중 LLM 학술심사 카운슬의 최종 메타 리뷰어다.

입력에는 다음이 포함되어 있다.

- 원본 연구 아이디어 1개
- 독립 원본 비판 3개
- 원본 비판에 대한 재비판 9개

총 12개의 심사 결과를 모두 검토하라.

단순 요약이나 다수결을 하지 말라.

각 주장과 비판을 증거의 질에 따라 재평가하라.

다음을 수행하라.

1. 모든 주요 비판 항목을 정규화하고 중복을 제거한다.
2. 세 모델이 합의한 비판을 식별한다.
3. 모델 간 의견이 갈린 비판을 식별한다.
4. 재비판 과정에서 폐기된 비판을 식별한다.
5. 자기비판에서만 발견된 오류를 식별한다.
6. 타 모델 비판에서만 발견된 오류를 식별한다.
7. 문헌으로 확인된 사실과 추측을 분리한다.
8. 아이디어의 치명적 결함과 수정 가능한 결함을 분리한다.
9. 현재 데이터로 검증 가능한 부분과 불가능한 부분을 분리한다.
10. 최소한의 반증 실험을 제안한다.
11. 연구를 계속할 가치가 있는지 냉정하게 판정한다.

최종 판정은 다음 중 하나여야 한다.

- Reject: Fundamentally Invalid
- Reject: Not Identifiable with Available Data
- Major Revision: Plausible but Severely Underspecified
- Conditional Go: Worth Testing under Strict Conditions
- Strong Go: Clear and Defensible Research Direction

최종 문서에는 반드시 다음 섹션을 포함하라.

- Executive Verdict
- Reconstructed Core Hypothesis
- Claims That Survived
- Claims That Failed
- Fatal Problems
- Fixable Problems
- Reviewer Disagreements
- Literature Gaps
- Minimum Falsification Experiments
- Required Mathematical Formalization
- Required Biological Validation
- Publication Potential
- Final Recommendation
```

---

# 9. 전체 산출물

## 원본 비판 3개

1. `01_claude_original_critique.md`
2. `02_gpt_original_critique.md`
3. `03_gemini_original_critique.md`

## 재비판 9개

4. `04_claude_on_claude.md`
5. `05_claude_on_gpt.md`
6. `06_claude_on_gemini.md`
7. `07_gpt_on_gpt.md`
8. `08_gpt_on_claude.md`
9. `09_gpt_on_gemini.md`
10. `10_gemini_on_gemini.md`
11. `11_gemini_on_claude.md`
12. `12_gemini_on_gpt.md`

## 최종 종합

13. `13_final_meta_review.md`

## 선택 산출물

14. `14_revised_hypothesis.md`
15. `15_experiment_blueprint.md`
16. `16_claim_evidence_matrix.md`

선택 산출물은 최종 메타 리뷰가 완료된 후에만 작성한다.  
비판 단계에서 원본 아이디어를 임의로 개선하거나 다시 쓰지 않는다.

---

# 10. 실행 원칙

- 각 세션에는 가능한 최고 성능 모델을 사용한다.
- 서로 다른 세션의 숨은 추론을 공유하지 않는다.
- 결과 문서만 다음 단계의 입력으로 전달한다.
- 모든 세션은 원본 아이디어를 직접 확인할 수 있어야 한다.
- 인용은 실제로 확인 가능한 문헌만 사용한다.
- 불확실한 내용은 불확실하다고 표시한다.
- 동일 모델의 자기비판과 타 모델 비판을 분리한다.
- 오케스트레이터는 모델 이름을 권위의 근거로 사용하지 않는다.
- 합의가 곧 진실이라는 가정을 금지한다.
- 비판의 강도보다 비판의 유효성을 우선한다.

---

# 11. 구조 요약

```text
Original Research Idea
        │
        ├── Claude Session 1 ── Claude Original Critique
        ├── GPT Session 1 ───── GPT Original Critique
        └── Gemini Session 1 ── Gemini Original Critique
                         │
                         ▼
       Original + Three Original Critiques
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
 Claude Sessions 2–4  GPT Sessions 2–4  Gemini Sessions 2–4
       │                 │                 │
       ├─ on Claude      ├─ on GPT         ├─ on Gemini
       ├─ on GPT         ├─ on Claude      ├─ on Claude
       └─ on Gemini      └─ on Gemini      └─ on GPT
                         │
                         ▼
               12 Review Documents
                         │
                         ▼
                Final Meta Reviewer
                         │
                         ▼
             13_final_meta_review.md
```
