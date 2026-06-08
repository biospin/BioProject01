---
name: core-table
description: Analyze tables for the objective <paper-id>_core.md section. Use to explain what each table compares, which metrics or numbers it presents, and how those numbers support or weaken the central claim. Counterpart of core-figure for tabular data.
---

# Core Table

## 목표

각 Table을 단순히 "어떤 수치가 있다"로 끝내지 않고, *왜 이 Table이 본문에 들어갔는가*, *무엇과 무엇을 비교하는가*, *어떤 수치가 결정적인가*, *통계적/실험적으로 그 차이가 의미 있는가*를 정리한다. `core-figure`의 자매 skill로, *시각화 대신 수치 표*를 다룬다.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 출력은 `analysis/<primary-topic>/<paper-id>/<paper-id>_core.md`의 "Table 분석" 섹션에 누적된다.

## 언어 규칙

- 기본 출력은 한국어.
- `Table`, `metric`, `baseline`, `dataset`, `p-value`, `CI`, `effect size`, `AUC`, `F1`, `accuracy`, `precision`, `recall` 같은 분야 표준 영어 용어는 유지.

## 적용 범위

Table이 있는 모든 자료에 호출. 자료 유형별 차이:

- **paper / preprint / conference-paper**: 모든 Table 분석. Supplementary Table 포함 (특히 결과 수치가 본문엔 없고 Supp Table에만 있는 경우 많음).
- **industry-report / whitepaper / government-report**: 통계 표, 비교 표, 시장 데이터 표가 있으면 분석.
- **review paper**: 주로 method taxonomy 표. *method 간 비교*가 핵심.
- **news / blog / webinar**: 표가 있으면 간단히. 보통 없음.

## 작업 절차

1. **Table 목록 추출**: 본문, Supplementary, Extended Data에서 모든 Table을 찾는다. Table 번호와 caption.
2. **본문 언급 위치 찾기**: 본문에서 "Table N에서 보듯이..." 같은 부분을 모은다.
3. **Table 목적 추론**: 저자가 *왜 이 Table을 넣었는가*. 어떤 주장을 뒷받침하는가.
4. **열·행 구조 파악**: 비교 축이 무엇인지 (예: row = method, column = dataset → method × dataset 성능 표).
5. **핵심 수치 식별**: 가장 중요한 수치 3~5개. baseline 대비 차이.
6. **통계적 유의성·재현성 확인**: p-value, CI, effect size, 다중 비교 보정. *core-results*와 일관되게 표기.
7. **해석의 강점·한계**: 표의 *수치 자체*가 강한 증거인지, 보조 증거인지.

## 출력 형식

```markdown
### Table N (또는 Table SN — supplementary)

- 이 Table이 필요한 이유: ...
- 이 Table이 뒷받침하는 주장: ...

#### 표 구조
- Row (비교 축 1): ...
- Column (비교 축 2): ...
- 셀 값의 의미 (예: AUC, accuracy, p-value): ...

#### 핵심 수치
- [수치 + 단위] (row=…, column=…)
  - baseline 대비 차이: …
  - 통계적 유의성: p = …, CI = [..], effect size = …
- [수치 + 단위] …

#### 본문에서 강조한 비교
- 비교 대상: …
- 관찰된 차이: …
- 이 차이가 의미하는 것: …

#### 해석 시 주의점
- 주의점: …
- (수치가 cherry-picked이거나 effect size 작은데 강조됐으면 표시)
```

## 작성 규칙

- **모든 Table을 같은 깊이로 다루지 않는다.** 본문 핵심 Table은 자세히, supplementary Table은 *그 Table이 다루는 비교*만 짧게.
- **수치를 그대로 옮긴다.** 반올림은 본문이 한 단위 그대로 (예: 본문 "AUC = 0.872"면 그대로, 임의로 0.87로 줄이지 않음).
- **셀 값이 무엇인지 명확히.** "0.872"만 적지 않고 "AUC = 0.872 (95% CI 0.85-0.89)".
- **Supplementary Table의 출처 명시**: `supp_2_tables.xlsx sheet "TableS5"` 또는 `Extended Data Table 1` 같이.
- **baseline 대비 차이를 항상 본다.** Table은 보통 비교용. "method A보다 method B가 좋다"가 핵심 메시지.
- **다중 비교가 많은 표 (예: method × dataset × metric)** 는 *가장 결정적인 셀 3개*만 본문에 풀어쓰고 나머지는 `...등` 또는 *원문 Table 참조*로 짧게.

## Cross-reference

- `core-results`가 *전체 결과 흐름*을 정리하고, `core-table`은 *각 표 단위 정밀 분석*. 두 출력이 같은 수치를 다루면 *수치는 한 번만* (core-results에) 옮기고 core-table에서는 분석에 집중.
- `core-figure`와 자매 skill. Figure가 같은 비교를 시각화한 경우, core-figure 분석과 cross-link (예: "이 Table은 Figure 3의 정량 버전").

## 주의할 점

- **Table caption만으로 분석하지 않는다.** 본문에서 어떤 비교를 강조했는지가 더 중요.
- **수치 cherry-picking 의심**: 본문이 강조하는 셀이 *전체 표에서 예외적으로 좋은 셀*이라면 표시 (`해석: 본문은 best case만 강조, 평균 또는 worst case는 다름`).
- **Supplementary Table 누락 주의**: 본문 핵심 결과가 Supp Table에만 있으면서 본문 figure에 *시각화*만 있는 경우 흔함. 반드시 supp_*.xlsx를 확인.
- **표가 미제공·접근 불가**면 `미제공:`으로 표시하고 진행. 추측 금지.
