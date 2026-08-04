# output_v02 — AI Scientist 설계 시각화 (HTML + mermaid)

`ai_scientist/`의 마크다운 6편(README, 01–05)을 하나의 인터랙티브 HTML 문서로 묶은 결과물이다. `output_v01`의 갱신판으로, 외부 하네스 두 편에서 참조한 게이트 강화 내용을 반영했다.

## 여는 법

`index.html`을 브라우저로 열면 된다.

```bash
xdg-open ai_scientist/output_v02/index.html   # Linux
open ai_scientist/output_v02/index.html       # macOS
```

## v01 대비 추가된 것

- **게이트 강화(§6.1)** 절과 다이어그램: 검증 게이트 스택, 다중 모델 적대적 검토
- **원칙 8**: 결정론적 코드와 LLM 판단 분리 + 전용 다이어그램
- **외부 참조** 절: `docs/hyperresearchdeck.html`, `docs/adversarial_multi_llm_council_harness.md`에서 가져온 것과 반영 위치 표
- 레이어 B 비용 절에 모델 티어링을 검증된 설정 객체로 두라는 보강

## 구성

- **단일 페이지**: 좌측 사이드바 목차 + 본문. 개요 → 레이어 A(게이트 강화 포함) → 레이어 B → 설계 원칙 8 → 결정론 vs LLM → 외부 참조 → 컴포넌트 맵.
- **mermaid 다이어그램 9종**: 전체 그림, 랩 조직도, 논문 생산 루프, 파이프라인 P0–P5, 검증 게이트 스택, 다중 모델 적대적 검토, 4계층 아키텍처, 인계 루프, 결정론 vs LLM 분리.
- **라이트/다크 테마 토글**(좌측 하단). 시스템 설정도 자동 반영.

## 알아둘 점

- mermaid 라이브러리를 CDN(jsdelivr)에서 불러온다. 다이어그램 렌더에는 인터넷 연결이 필요하고, 표·본문은 오프라인에서도 보인다.
- 게이트 강화(§6.1)의 세 항목은 아직 파이프라인에 구현되지 않은 **도입 대상**이다. 문서에도 그렇게 표기했다.
- 다이어그램 9종은 mermaid 파서로 문법 검증을 마쳤다.
