---
name: results-scan
description: Rapidly extract datasets, experimental conditions, quantitative results, and figure evidence. Links each figure to the claim it supports. Translates experimental design into computational terms when wet lab content is unclear.
---

# Results Scan

## 언제 실행하나
`quality-gate` 판정이 "보통" 이상일 때 실행한다. Results 섹션과 Figure들을 함께 읽는다.

## 입력
논문 PDF (Results, Figure caption, Table, Supplementary).

## 실행 절차
0. `full.md`에 앞서 작성된 내용이 있으면 읽고 맥락을 파악한다.
1. 사용된 데이터셋 목록을 추출한다 (이름, species/tissue, 플랫폼, 규모).
2. 각 데이터셋이 무엇을 검증하려는 목적으로 사용됐는지 파악한다.
3. 비교 대상(baseline)을 정리한다.
4. 수치 결과를 그대로 추출한다. 없으면 "수치 미제공"으로 표시한다.
5. 각 주요 Figure가 어떤 결과 주장을 뒷받침하는지 연결한다.

## 실험 내용 계산적 번역
wet lab 실험 내용이 이해되지 않을 때 다음 기준으로 계산적 의미로 변환한다.

| 실험 내용 | 계산적 의미 |
|---|---|
| 세포 처리, 시약, 염색 | 입력 데이터의 생성 조건 (데이터 특성에 영향) |
| 시퀀싱 깊이, 커버리지 | 데이터 품질과 noise 수준 |
| 기술 반복(technical replicate) | 분산 추정 가능성 |
| 생물학적 반복(biological replicate) | 일반화 가능성 |
| 대조군(control) | Baseline 설정 방식 |
| perturbation (knockout, knockdown 등) | 인과 검증 실험 |

## Figure Panel 추출
Figure를 이미지로 분리해야 할 때 `skills/full-figure/scripts/extract_panels.py`를 사용한다.

```bash
python3 skills/full-figure/scripts/extract_panels.py papers/paper.pdf \
  --page [N] --figure "[Figure N]" --figure-bbox [x0,y0,x1,y1] \
  --out "analysis/<topic>/<paper-title>/figures"
```

복잡한 layout은 JSON spec으로 panel별 좌표를 명시한다. 먼저 auto mode로 실행해 `*_debug.png`를 확인하고, panel 경계가 맞지 않으면 manual JSON spec으로 전환한다.

## 출력 형식

```markdown
### Results Scan

#### 데이터셋
| 데이터셋 | Species / Tissue | 플랫폼 | 규모 | 검증 목적 |
|---|---|---|---|---|

#### 비교 대상 (Baseline)
-

#### 데이터셋별 결과

##### [데이터셋 이름]
- 평가 지표:
- 주요 수치:
- Baseline 대비:
- 뒷받침하는 Figure:

#### Figure-주장 연결
| Figure | 뒷받침하는 주장 | 근거 유형 (정량 / 시각) |
|---|---|---|

#### 주의할 결과
- 수치 없이 "개선됨"이라고만 표현한 부분:
- 시각적 근거에만 의존한 주장:
- 단일 데이터셋에서만 확인된 결과:
```

## 주의
- "성능이 좋다"고 쓰지 않는다. 어떤 metric에서 어떤 baseline 대비 얼마나 좋았는지 쓴다.
- Figure 설명은 "무엇을 보여주는가"가 아니라 "어떤 주장을 뒷받침하는가"로 쓴다.
- 본문에 없는 수치를 추측하지 않는다.
- 실험 내용이 이해되지 않으면 계산적 의미로 변환하고, 변환이 추정인 경우 "추정:"으로 표시한다.
