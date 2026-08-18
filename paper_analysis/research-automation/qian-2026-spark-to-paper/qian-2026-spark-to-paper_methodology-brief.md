# Methodology Brief — qian-2026-spark-to-paper

## 한 줄 결론 (모든 독자)
- Citation: `@qian2026sparktopaper` (arXiv:2608.11924) | Importance: **상(하네스 관점)** — 우리 논문 생산·검증 하네스와 독립 수렴한 외부 선례. 단 우리 velocity 과학과는 무관한 메타 자료.
- 한 문장 결론: end-to-end 논문 생성을 coding assistant 내장 13 skill로 구현하고 검증 스택으로 fabrication을 14%→92%까지 잡은 시스템 논문. 우리 verify-harness·§6.1의 **직접 prior art이자 도입 후보 공급원**.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: 평가는 외부 선정 8 research topic(사전등록). 원 데이터셋 목록은 본문 `미제공:`(case study만 clinical risk·PM2.5 언급).
- 코드 공개: `github.com/Spark-To-Paper-Skills/spark-to-paper-skills` (url-only, 소스 릴리스 명시 없음·예고). **Claude Code + Claude model family 종속**(타 구현 없음).
- 자원 요구: 편당 **$8.1 · 11.9M token · 3.2h**(8 topic). 증분 gate +$5.3, self-review +$0.6, adversarial +$1.6.
- 핵심 의존성: Claude Code 실행환경, 결정론 gate(python 추정 `검토필요:`), LaTeX 컴파일, 외부 서지 metadata API(citation 검증).
- 자세히 → [qian-2026-spark-to-paper_core.md](qian-2026-spark-to-paper_core.md) §Methods, [sources/fulltext_extract.md](sources/fulltext_extract.md)

## 우리 적용 가능성 (의사결정자)
- 하네스 호환: **높음** — 우리 paper-production-harness가 이미 같은 구조(파일 아티팩트·결정론 gate vs model review·preregistration·self-refutation cap). 도입은 통째 이식이 아니라 **부분 접목**.
- 도입 후보(우선순위): **① 정량 fabrication ablation**(verify-harness Layer2 mutation으로 "우리 게이트 탐지율 N%" 산출 → 그들 92%와 비교축) → **② Claim Admission 5라벨**(supported/partially/unsupported/contradicted/needs-confirmation)을 CLAIMS.yaml에 접목. ③④ 비용·citation 벤치(선택).
- 비용·시간 추정: 도입1 = 우리 mutation 스위트 실행 + 리포트(수 시간). 도입2 = claim ledger 스키마 확장(중간).
- ROI 한 줄: §6.1(BIOP01-81)·검증하네스(BIOP01-84) 논지를 **정량화 + 외부 선례로 방어** — 값 큼.
- 자세히 → [comparison_vs_paper-production-harness.md](comparison_vs_paper-production-harness.md), [qian-2026-spark-to-paper_lens-industry.md](qian-2026-spark-to-paper_lens-industry.md) §3

## 본인 재회고 (본인)
- 핵심 follow-up 질문:
  - `질문: 우리 verify-harness Layer2 mutation을 우리 게이트에 돌리면 탐지율이 그들 92% 대비 어디인가? (같은 36-probe식 seeded-defect 셋을 우리 게이트 클래스에 맞춰 설계)`
  - `질문: 그들 adversarial precision 74%(오탐 26%)를 우리 cross-model(Lv5)+사람(Lv8) 사다리로 얼마나 줄이나 — 정량 대비 가능한가?`
- 다음 액션: BIOP01-88에 도입1·2를 실행 항목으로. 우리 하네스를 글로 쓸 때 `@qian2026sparktopaper`를 §6.1 prior art로 인용(우리 차별점=mutation·독립성 사다리를 그들 한계와 대비).
- 자세히 → [qian-2026-spark-to-paper_lens-academic.md](qian-2026-spark-to-paper_lens-academic.md) (Citation 후보·후속 아이디어)
