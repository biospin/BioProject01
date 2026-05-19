---
name: question
description: Answer user questions using existing analyses. Use when receiving a question about analyzed materials, content, methods, figures, results, limitations, comparisons, or takeaways. Answer from analysis/**/core.md (and lens-*.md, methodology-brief.md, paper-info.yaml) rather than re-analyzing source PDFs or inventing unsupported claims.
---

# Question

## 목표
사용자가 자료 내용에 대해 질문했을 때, 새로 추측하거나 원문을 다시 해석하기보다 먼저 `analysis/**/core.md`에 정리된 내용을 근거로 답한다. 이 스킬은 분석 파일을 생성할 때는 사용하지 않고, 이미 정리된 분석 결과를 바탕으로 질의응답할 때만 사용한다.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  답변에서 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 답변의 *근거는 분석 결과물* (core.md / lens-*.md / methodology-brief.md / paper-info.yaml). 원문 PDF나 외부 지식을 우선 근거로 삼지 않는다.

## 언어 규칙
- 기본 답변은 한국어로 작성한다.
- `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `baseline`, `dataset`, `benchmark`, `metric`, `Figure`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 유지할 때는 처음 한 번 한국어 설명을 덧붙인다.
- 불필요하게 문장 전체를 영어로 쓰지 않는다.

## 답변 우선순위
1. 질문이 특정 topic과 자료를 가리키면 해당 자료의 `analysis/<primary-topic>/<paper-id>/core.md`를 먼저 확인한다.
2. 질문이 특정 자료만 가리키면 `analysis/**/<paper-id>/core.md`를 검색해 가장 일치하는 파일을 먼저 확인한다.
3. 해당 `core.md`에 답이 있으면 그 내용만 근거로 답한다.
4. core.md에 부족하면 같은 폴더의 `lens-academic.md`, `lens-industry.md`, `methodology-brief.md`, `paper-info.yaml`을 참고한다.
5. 다른 자료에 관련 내용이 있으면 `<paper-id>에 따르면...` 또는 `@<citation.key>` 형식으로 출처를 명시한다.
6. 어떤 분석 파일에도 관련 내용이 없으면 `분석된 파일에서는 해당 내용을 찾지 못했습니다.`라고 답한다. 추측하지 않는다.

## 금지 사항
- 분석 파일에 없는 내용을 사실처럼 말하지 않는다.
- PDF 원문, 외부 논문, 웹 검색, 일반 배경지식을 우선 근거로 삼지 않는다.
- 다른 논문의 내용을 특정 논문의 내용처럼 말하지 않는다.
- 근거가 약한 추론을 단정적으로 말하지 않는다.

## 작업 절차
1. 사용자의 질문이 어떤 논문, Figure, method, dataset, result, limitation을 묻는지 파악한다.
2. `analysis/**/core.md` 목록을 확인한다.
3. 질문이 특정 논문을 지칭하면 해당 `core.md`를 우선 읽는다.
4. 필요한 경우 `rg`로 관련 키워드를 찾고, 관련 section을 읽는다.
5. 답변할 수 있으면 `core.md`의 내용에 맞춰 간결하게 답한다.
6. 관련 내용이 다른 논문에만 있으면 논문 제목을 밝히고 답한다.
7. 관련 내용이 없으면 없다고 말하고, 어떤 추가 자료가 있으면 답할 수 있는지 짧게 말한다.

## 출력 형식
일반 질문에는 간결하게 답한다. 근거를 명확히 해야 할 때는 아래 구조를 쓴다.

```markdown
답변:

근거:
- 참고한 분석 파일:
- 관련 섹션:

주의:
```

## 답변 예시
```markdown
답변:
이 질문은 현재 분석된 MultiVelo core.md 기준으로는 Figure 6의 TF expression과 motif accessibility time lag 분석에 해당합니다. 정리된 내용에 따르면 TF expression은 대체로 motif accessibility보다 먼저 나타나는 경향이 있고, 저자는 이를 regulatory timing 분석에 활용할 수 있다고 봅니다.

근거:
- 참고한 분석 파일: analysis/epigenomic-lag/wang-2024-multivelo/core.md
- 관련 섹션: Figure 6, Final Takeaways

주의:
이 분석은 time lag 기반 association이며 causal proof는 아니라고 정리되어 있습니다.
```

## 찾지 못했을 때
```markdown
분석된 core.md들에서는 해당 내용을 찾지 못했습니다.
현재 답하려면 해당 논문의 core.md에 그 내용이 추가되어 있거나, 원문 PDF를 다시 분석해야 합니다.
```
