---
name: paper-network
description: Map relationships between multiple analyzed papers—author overlap, institutional clusters, corporate funding connections, and research lineage. Run when two or more papers exist in analysis/ to detect potential echo chambers, conflicts of interest, or coordinated research groups.
---

# Paper Network

## 언제 실행하나
`analysis/` 아래에 두 개 이상의 논문 분석 (`full.md`)이 존재할 때 실행한다. 단일 논문에는 실행하지 않는다.

사용자가 명시적으로 요청하거나, 여러 논문을 분석한 뒤 그 논문들이 독립적인 연구인지 확인하고 싶을 때 실행한다.

## 입력
분석된 논문들의 `full.md` 파일. 저자, 기관, 펀딩 정보가 포함되어 있어야 한다 (`quality-gate` 출력 참고).

## 실행 절차
1. `analysis/**/full.md` 목록을 수집한다.
2. 각 논문의 저자 목록, 교신저자 기관, 펀딩 출처를 추출한다.
3. 저자 겹침을 분석한다.
4. 기관 클러스터를 분석한다 (같은 기관 또는 협력 기관 그룹).
5. 기업 펀딩 겹침을 분석한다.
6. Research lineage를 분석한다 (상호 인용, 방법 계승 관계, 동일 그룹 후속 연구 여부).
7. 주의 플래그를 생성한다.

## 출력 형식

```markdown
### Paper Network

**분석 대상 논문:**
| 번호 | 제목 | 교신저자 | 기관 |
|---|---|---|---|

#### 저자 겹침
| 저자 | 등장 논문 | 역할 (제1저자 / 교신저자 / 공저자) |
|---|---|---|

#### 기관 클러스터
| 기관 | 관련 논문 | 비고 |
|---|---|---|

#### 기업 / 펀딩 연관
| 기업 / 펀딩 기관 | 관련 논문 | 잠재적 이해충돌 |
|---|---|---|

#### Research Lineage
- [논문 A]는 [논문 B]의 방법을 계승 / 인용 / 비교함:
- 동일 연구 그룹으로 보이는 논문 묶음:

#### 주의 플래그
- 같은 그룹의 자기 검증 논문 여부:
- 기업 이해충돌 집중 여부:
- 특정 기관 bubble 여부 (다양한 독립 연구인가):

#### 종합 판단
이 논문 묶음이 독립적인 연구들인가, 아니면 특정 그룹 / 기업의 산출물인가.
신뢰도 평가 시 이 관계를 어떻게 고려해야 하는가.
```

## 주의
- 저자 겹침이나 기관 연관 자체가 논문의 신빙성을 낮추지는 않는다. 사실을 보고하고 해석은 사용자에게 맡긴다.
- 정보는 `full.md`와 `quality-gate` 출력에서 확인된 내용만 사용한다. 추측하지 않는다.
- Research lineage는 논문 내에서 명시적으로 인용되거나 방법을 계승한 경우만 표시한다.
