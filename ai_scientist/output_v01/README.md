# output_v01 — AI Scientist 설계 시각화 (HTML + mermaid)

`ai_scientist/`의 마크다운 6편(README, 01–05)을 하나의 인터랙티브 HTML 문서로 묶은 결과물이다.

## 여는 법

`index.html`을 브라우저로 열면 된다.

```bash
# 예: 로컬에서 바로 열기
xdg-open ai_scientist/output_v01/index.html   # Linux
open ai_scientist/output_v01/index.html       # macOS
```

## 구성

- **단일 페이지**: 좌측 사이드바 목차 + 본문. 개요 → 레이어 A → 레이어 B → 설계 원칙 → 컴포넌트 맵.
- **mermaid 다이어그램 6종**: 전체 그림, 랩 조직도, 논문 생산 루프, 파이프라인 P0–P5, 4계층 아키텍처, 인계 루프.
- **라이트/다크 테마 토글**(좌측 하단 버튼). 시스템 설정도 자동 반영.

## 알아둘 점

- mermaid 라이브러리를 CDN(jsdelivr)에서 불러온다. 따라서 **다이어그램 렌더에는 인터넷 연결이 필요**하다. 표·본문은 오프라인에서도 보인다.
- 완전 오프라인(자체 완결형)이 필요하면 mermaid를 파일에 인라인하는 버전으로 다시 만들 수 있다.
- 다이어그램 6종은 mermaid 파서로 문법 검증을 마쳤다.
