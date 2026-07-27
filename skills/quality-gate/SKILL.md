---
name: quality-gate
description: Evaluate paper credibility across five dimensions: journal standing, author and institutional profile, evidence quality, reproducibility, and bias risk including paper mill indicators. Outputs a reading priority judgment before deep analysis begins.
---

# Quality Gate

## 언제 실행하나
`fig1-decode`와 `claim-extract` 이후 실행한다. 논문을 깊이 읽기 전에 시간 투자 대비 가치를 판정하는 관문이다. 판정이 "낮음" 이하이면 `results-scan` 이후 단계를 건너뛸 수 있다.

## 입력
논문 PDF (표지, 저자 정보, Acknowledgements, 저널명).

## 평가 항목

### 1. 저널 수준
- 저널명 확인
- SCI / SCIE / SSCI 등재 여부
- Impact Factor (IF) — PDF에서 확인 가능한 범위만, 불확실하면 "미확인"
- Quartile: Q1 / Q2 / Q3 / Q4 / 미확인
- 알려진 predatory journal 여부

### 2. 저자 및 기관
- 제1저자와 교신저자(corresponding author)의 소속 기관을 확인한다.
- 기관 분류:
  - Top-tier 연구기관 (Broad Institute, EMBL, Sanger 등)
  - 주요 대학 연구실
  - 기업 연구소
  - 미확인 / 소규모 기관
- 해당 분야에서 교신저자가 알려진 연구자인지 가능한 범위에서 확인한다.

### 3. 기업 / 펀딩 연관성
- Acknowledgements와 논문 말미에서 funding 출처를 확인한다.
- 저자 소속에 기업이 포함되어 있는지 확인한다.
- 기업 이해관계가 결과 방향에 영향을 줄 수 있는 구조인지 판단한다.
  - 예: 특정 제품·시약 제조사가 펀딩하고 해당 제품이 유리한 결과를 보임
  - 예: 제약사 또는 바이오텍 소속 저자가 자사 플랫폼을 평가

### 4. 근거 품질
- 사용 데이터셋 수: 단일 / 복수 / 독립 검증 포함
- Baseline 경쟁력: 최신 방법과 비교했는가, 약한 baseline만 선택했는가
- 주요 주장이 정량적 수치로 뒷받침되는가, 시각적 근거에만 의존하는가
- Causal claim이 있는데 association evidence만 제시하는가

### 5. 재현 가능성 및 Paper Mill 위험

**재현 가능성:**
- 코드 / 데이터 공개 여부
- Methods에 재현에 충분한 상세 기술이 있는가

**Paper Mill 위험 지표** (해당하는 항목 수를 기록한다):
1. 저명도 낮은 저널 또는 predatory journal 게재
2. 결과가 지나치게 완벽하거나 오차 범위가 비정상적으로 좁음
3. 이해충돌(conflict of interest) 미신고
4. 코드·데이터 미공개이면서 방법 기술도 불충분
5. 동일 저자의 단기간 대량 출판 패턴
6. Figure 재사용 또는 이미지 이상 의심

## 출력 형식

```markdown
### Quality Gate

**저널:** [저널명] | [SCI/SCIE/미확인] | IF [값 또는 미확인] | [Q1/Q2/Q3/Q4/미확인]

**저자 / 기관:**
- 제1저자: [소속] ([기관 분류])
- 교신저자: [소속] ([기관 분류])

**펀딩 / 이해충돌:**
- Funding:
- 기업 소속 저자:
- 이해충돌 가능성:

**근거 품질:**
- 데이터셋 수:
- Baseline 경쟁력:
- 주장-근거 일치:
- Causal 주장 여부:

**재현 가능성:** [코드 공개 여부] | [방법 기술 수준]

**Paper Mill 위험:** [해당 지표 수] / 6
- 해당 항목:

**판정:**
- 읽기 우선순위: [높음 / 보통 / 낮음 / 읽지 않음 권고]
- 이유:
- 주의하며 읽을 부분:
```

## 판정 기준

| 판정 | 조건 |
|---|---|
| **높음** | Q1–Q2 저널, 상위 기관, 복수 데이터셋, 코드 공개, paper mill 지표 0–1개 |
| **보통** | Q3 이하 또는 기관 미확인, 단일 데이터셋, 부분 코드 공개, paper mill 지표 1–2개 |
| **낮음** | predatory journal 의심, 기업 이해충돌, 약한 baseline, paper mill 지표 3개 이상 |
| **읽지 않음 권고** | predatory journal 확인됨, paper mill 지표 4개 이상, 이해충돌 명백 |

## 주의
- IF, quartile은 PDF에서 확인되지 않으면 반드시 "미확인"으로 표시한다. 추측하지 않는다.
- Paper mill 지표는 개별 항목 하나만으로 낮은 판정을 내리지 않는다. 복합 패턴으로 판단한다.
- 기관, 저자, 국가에 대한 판단은 확인된 사실에 근거하며 선입견으로 일반화하지 않는다.
- "읽지 않음 권고"는 근거가 명확할 때만 사용한다.
