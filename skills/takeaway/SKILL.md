---
name: takeaway
description: Extract actionable research directions and critical assessment from Discussion. Identifies what the paper leaves unresolved, where evidence is thin, and what follow-up experiments would make the story stronger.
---

# Takeaway

## 언제 실행하나
`results-scan` 이후 실행한다. Discussion / Conclusion / Limitations를 읽고 논문이 열어놓은 다음 방향을 정리한다.

## 입력
논문 PDF (Discussion, Conclusion, Limitations 섹션).

## 실행 절차
0. `full.md`에 앞서 작성된 내용 전체를 읽는다. fig1-decode, claim-extract, results-scan에서 정리된 주장과 수치를 파악한 뒤 Discussion을 읽는다.
1. 저자가 명시한 한계를 추출한다.
2. 저자가 제안한 다음 연구 방향을 추출한다.
3. Results와 Discussion 사이에서 설명이 매끄럽지 않거나 주장에 비해 근거가 부족한 부분을 찾는다.
4. 이 논문이 답하지 못하고 열어놓은 질문들을 정리한다.
5. 다음 연구 아이디어를 실행 가능한 수준으로 구체화한다.

## 설명 gap 판단 기준
다음 패턴이 보이면 gap으로 표시한다:
- Causal claim인데 association evidence만 제시된 경우
- 단일 데이터셋 결과를 일반적 결론으로 제시한 경우
- 시각적 근거(heatmap, UMAP)에 의존하고 수치 검증이 없는 경우
- 저자가 인정하지 않았지만 ablation이나 baseline이 빠진 경우

## 출력 형식

```markdown
### Takeaway

#### 저자가 인정한 한계
-

#### 분석자 판단: 설명 gap
| 주장 | 제시된 근거 | 부족한 근거 |
|---|---|---|

#### 이 논문이 열어놓은 질문
-

#### 다음 연구 아이디어
| 아이디어 | 필요한 실험 / 분석 | 내 연구와의 연결 |
|---|---|---|

#### 한 줄 평
- 가장 중요한 기여:
- 가장 큰 한계:
```

## 주의
- 저자가 인정한 한계와 분석자가 판단한 gap을 구분한다.
- "다음 연구 아이디어"는 현실적으로 수행 가능한 수준으로 쓴다.
- 비판은 "약하다"가 아니라 구체적으로 어떤 근거가 없기 때문에 약한지를 쓴다.
- 논문에 없는 추측을 사실처럼 쓰지 않는다.
