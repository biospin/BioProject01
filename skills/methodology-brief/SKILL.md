---
name: methodology-brief
description: Produce a 1-page multi-audience brief for reproducibility/applicability decisions. Used after <paper-id>_core.md and lens-*.md are written; condenses key facts and links to detailed files. Serves three readers in one page — the reproduction engineer, the BD/decision maker, and the analyst (oneself) on revisit.
---

# Methodology Brief

## 목표

`<paper-id>_core.md`와 `lens-*.md` 작성이 끝난 후, **1페이지 짜리 multi-audience 압축본**을 만든다. 본인이 다시 펴봤을 때 ROI를 빠르게 판단하고, 팀 내 다른 사람(재현 담당자, BD/의사결정자)도 같은 문서로 자신의 take를 빠르게 얻을 수 있어야 한다. 자세한 내용은 *링크로* 다른 파일에 위임.

원칙:
1. **1페이지** 안에 끝낸다 (300~500 단어, 화면 한 번에 보이는 정도).
2. **세 독자** (재현 담당자 / 의사결정자 / 본인)가 모두 자신의 *입구*를 찾을 수 있다.
3. **자세한 내용은 다른 파일로 명시적 링크**. 같은 정보를 반복하지 않는다.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 출력은 `analysis/<primary-topic>/<paper-id>/<paper-id>_methodology-brief.md`.

## 호출 시점

- **모든 자료에 항상 호출**. core-methods가 작성되는 모든 자료에 같이 작성된다.
- 단, *Full Paper Workflow의 마지막 단계*에 호출된다 (core-* 와 lens-* 모두 완료된 후). 그래야 압축본이 *전체 분석을 본 후*의 take를 반영한다.
- non-paper에서도 호출. 단 *해당 없는 섹션*은 짧게 "재현 적용 불가 — 자료 유형: <document_type>" 식으로 줄임.

## 출력 형식

```markdown
# Methodology Brief — <paper-id>

## 한 줄 결론 (모든 독자)
- Citation: `@<citation.key>`  |  Importance: `<상/중/하>` (1문장 사유)
- 한 문장 결론: [무엇 + 어디 쓸지]

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: <accession / availability / 제약>
- 코드 공개: <URL / license / maintenance 상태>
- 자원 요구: <GPU/CPU, RAM, runtime estimate>
- 핵심 의존성: <library / framework / specific version>
- 자세히 → [<paper-id>_core.md](<paper-id>_core.md) §방법론, [sources/paper.pdf](sources/paper.pdf) §Methods

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: <우리 dataset과의 일치 정도>
- 자원 가능성: <우리 환경에서 가능 여부, estimate>
- 비용·시간 추정: <지금 적용 시 얼마나 걸리는지>
- ROI 한 줄: <왜 가져올 가치가 있는지/없는지>
- 자세히 → [<paper-id>_lens-industry.md](<paper-id>_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)
- 핵심 follow-up 질문 1~2개: `질문: ...`
- 다음 액션: <구체적 next-step + 시점>
- 자세히 → [<paper-id>_lens-academic.md](<paper-id>_lens-academic.md), [<paper-id>_lens-industry.md](<paper-id>_lens-industry.md) §4

---
마지막 갱신: <YYYY-MM-DD>
```

---

## 섹션별 작성 규칙

### 한 줄 결론 (3줄 이내)

- `paper-info.yaml`의 `citation.key`와 `categorization.importance`를 그대로 인용.
- "한 문장 결론"은 본 자료의 *가장 결정적인 한 줄*. 본인이 다른 사람에게 *5초 안에 설명*할 때 쓸 한 줄.
- 예: `Multi-omic velocity로 chromatin-RNA lag를 정량화하는 알고리즘. HSPC 파이프라인에 직접 차용 가능.`

### 재현 가능성 체크 (5줄 이내)

각 줄은 *상태 + 한 줄 요약*. 자세한 설명 금지.

- **데이터 접근**:
  - `open` (GEO/SRA/Zenodo accession 명시)
  - `restricted` (dbGaP, EGA, 기관 IRB 필요)
  - `proprietary` (저자 보유, 비공개)
  - `미제공` (data availability statement 없음)
- **코드 공개**:
  - URL + license (MIT / Apache / GPL / 상업 등)
  - maintenance 상태 (active / archived / abandoned)
  - `없음` (코드 비공개)
- **자원 요구**:
  - GPU 필수 여부, 메모리, runtime estimate
  - 본문에 명시 없으면 `해석: <자료 유형 기준 추정>` 또는 `미제공:`
- **핵심 의존성**:
  - 가장 중요한 library/framework 3~5개
  - 특정 version에 묶여 있으면 표시 (예: `scanpy >= 1.9.0`)

### 우리 적용 가능성 (5줄 이내)

- **Dataset 호환**: 우리 현재 dataset(예: HSPC 10x Multiome)과의 일치 정도. 일치/부분일치/불일치.
- **자원 가능성**: 우리 환경(현재 GPU, headcount, wet lab)으로 가능한가. 부족하면 *무엇이 부족한지*.
- **비용·시간 추정**: 본인이 즉시 적용 시작했을 때 얼마나 걸리는지 (1주/1개월/1분기).
- **ROI 한 줄**: 왜 가져올 가치가 있는지 (또는 없는지). lens-industry §3을 압축.
- 항목이 *해당 없으면* "해당 없음 — <이유>" 식으로 줄여서 표시. 빈 칸 만들지 않는다.

### 본인 재회고 (3~5줄)

- **follow-up 질문 1~2개**: `질문:` prefix. 본인이 분석 다시 펴봤을 때 *직접 알아봐야 할 것*.
- **다음 액션 1개**: 구체적 next-step + 시점. 예: `HSPC subset에 MultiVelo 적용 시도 — 다음 sprint (~2주)`.
- 자세한 학계·산업 시선은 *링크로 위임*.

---

## 작성 규칙 (전체)

- **1페이지 제한 엄수.** 화면 한 번에 보여야 함. 페이지 넘기면 multi-audience brief의 의미 손실.
- **같은 정보를 두 절에서 반복하지 않는다.** ROI 한 줄이 "Importance"와 겹치면 한쪽만.
- **모든 자세한 분석은 *링크로 위임*.** "이것에 대한 자세한 분석은…" 같은 문장 금지. 그냥 `→ [파일.md](파일.md)`.
- **non-paper 자료**:
  - 재현 가능성 섹션이 적용 불가능하면 짧게 "재현 적용 불가 — 자료 유형: <document_type>" + 자세히 링크.
  - 우리 적용 가능성은 *정보 활용 가능성*으로 재해석 (예: "BD 미팅에서 시장 동향 자료로 활용").
- **`paper-info.yaml`의 importance가 비어 있으면** brief 작성을 *대기*하거나 `검토필요:`로 표시. lens-industry가 먼저 채워야 한다.
- **링크는 *상대 경로*로**. 같은 폴더 안의 파일이므로 `[<paper-id>_core.md](<paper-id>_core.md)` 형태.

## 호출 순서 안에서의 위치

AGENTS.md의 Full Paper Workflow에서:

1. source-grounding (sources, paper-info.yaml)
2. core-problem, core-methods, core-results, core-figure, core-table → `<paper-id>_core.md`
3. lens-academic → `<paper-id>_lens-academic.md`
4. lens-industry → `<paper-id>_lens-industry.md` (categorization 갱신)
5. **methodology-brief → `<paper-id>_methodology-brief.md`** ← 여기
6. Executive Summary 한 단락 추가 (`<paper-id>_core.md` 맨 앞)

즉 methodology-brief는 *모든 분석의 마지막에서 두 번째*. Executive Summary 직전에. lens-* 결과를 보고 압축.

## 주의할 점

- **본 skill은 새로운 분석을 만들지 않는다.** 이미 만들어진 core-* / lens-* 의 *압축 + 링크*.
- **1페이지 제한을 깨면 *목적 상실*.** 본인이 *5초 안에 그림 잡기*가 목표. 길어지면 그냥 다른 파일 보면 됨.
- **링크가 가리키는 파일이 비어있으면** 표시 (`자세히 → <paper-id>_lens-industry.md (미작성)`). 거짓 링크 금지.
- **외부 자료 (사내 wiki, Confluence, JIRA)는 본 brief에 직접 link하지 않는다.** 필요하면 `paper-info.yaml`의 별도 필드에 기록.
