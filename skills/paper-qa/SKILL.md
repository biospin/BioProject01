---
name: paper-qa
description: Answer questions about analyzed papers using only the content in existing full.md files. Never re-analyze PDFs or invent information not present in the analysis files.
---

# Paper QA

## 언제 실행하나
이미 분석된 논문에 대해 사용자가 질문할 때 실행한다. 새로운 논문 분석에는 사용하지 않는다.

## 답변 우선순위
1. 특정 논문을 가리키면 해당 `analysis/<topic>/<paper-title>/full.md`를 먼저 읽는다.
2. 그 `full.md`에 답이 있으면 해당 내용만 근거로 답한다.
3. 없으면 `analysis/` 아래 다른 논문 `full.md`를 검색한다.
4. 다른 논문에 관련 내용이 있으면 "OO 논문 분석에 따르면..."으로 출처를 밝힌다.
5. 어디에도 없으면 없다고 말하고, 어떤 추가 분석이 있으면 답할 수 있는지 제안한다.

## 출력 형식
간단한 질문은 직접 답한다. 근거를 명시해야 할 때:

```markdown
**답변:**

**근거:**
- 파일: analysis/[topic]/[paper]/full.md
- 섹션:

**주의:** (확인된 내용과 해석의 경계가 있으면 표시)
```

## 금지
- `full.md`에 없는 내용을 사실처럼 답하지 않는다.
- PDF 원문이나 외부 지식을 우선 근거로 삼지 않는다.
- 다른 논문의 내용을 특정 논문의 내용처럼 말하지 않는다.
