# 01. 개요 — AI Scientist가 무엇을 자동화하는가

## 출발점

이 프로젝트가 풀려는 연구 문제는 gene별 chromatin→transcription **lag**(activation/shutdown)을 정량하고, baseline epigenomic feature로 epigenetic drug response timing을 예측하는 것이다. 1차 데이터셋은 Human HSPC 10x Multiome(GSE209878)이다. 이 도메인 문제 자체는 `pipeline/hspc-velocity-benchmark/`가 담당한다.

AI Scientist 설계의 목표는 이 연구 문제를 푸는 **과정 전체**를 자동화하는 데 있다. 사람이 도구를 하나씩 손으로 돌리는 대신, AI 멤버들이 연구의 각 단계를 나눠 맡아 이어서 돌아가게 한다.

## 연구 과정을 어떤 단계로 나눴나

전통적인 연구 흐름을 AI가 맡을 수 있는 단계로 나누면 다음과 같다. 괄호 안은 이 저장소에서 그 단계를 맡는 주체다.

1. **논문 탐색·정리**: 선행연구를 찾아 정리하고, 우리 기여를 정직하게 위치시킨다. (`literature-scout`, 그리고 별도 하네스로 돌려 `paper_analysis/`에 반입한 dual-lens 분석 14편)
2. **가설 설정·차별화**: 무엇이 새로운지, 어떤 실험이 가장 싸게 그것을 입증하는지 정한다. (`novelty-strategist`, `research-methodologist`)
3. **실험 설계·감사**: 가설을 검증 가능한 실험으로 바꾸고 누수·통계 위험을 미리 잡는다. (`research-methodologist`)
4. **실험 수행·분석**: 파이프라인을 돌려 eval·통계·cross-dataset 재현을 계산한다. (`hspc-velocity-analyst` + `scripts/` P0–P5)
5. **집필·그림**: 결과 파일에서 원고와 그림을 만든다. (`manuscript-writer` + `figures/figNN_*.py`)
6. **검수·리뷰**: 제출 전 적대적 자체검토와 정식 venue 리뷰를 돌린다. (`paper-critic`, `reviewer`)
7. **발표**: 청중에 맞춰 슬라이드와 발제를 만든다. (`presenter`)

이 일곱 단계를 사람이 매번 순서대로 부르지 않도록, 자연어 요청을 멤버에 배정하는 라우팅표(`CLAUDE.md`)와 여러 단계를 엮어 실행하는 오케스트레이터 Skill(`paper-production-orchestrator`)을 두었다. 자세한 구조는 [02_single_lab_harness.md](02_single_lab_harness.md)에서 다룬다.

## 왜 한 명의 AI로 끝내지 않았나

연구 팀은 한 사람이 아니다. 이 프로젝트도 데이터셋별로 담당자가 다르고(mouse brain, SHARE-seq, human brain, HSPC 등), 팀원마다 쓰는 AI도 Claude, Codex, Gemini로 갈린다. 한 AI가 논문 한 편을 끝까지 끌고 가는 구조(레이어 A)만으로는 이 협업을 담을 수 없다.

그래서 두 번째 레이어를 설계했다. 팀원 A의 AI가 끝낸 작업을 팀원 B의 AI가 자동으로 이어받는 인계 체계다. 신호를 JIRA 상태 전환 하나로 일원화하고, 인계 맥락을 정형화된 Handoff 코멘트로 강제하며, 모든 AI가 같은 MCP 설정으로 JIRA·GitHub를 읽고 쓰게 한다. 자세한 구조는 [03_multi_ai_collaboration.md](03_multi_ai_collaboration.md)에서 다룬다.

## 두 레이어가 공유하는 발상

레이어 A와 B는 다른 문제를 풀지만 같은 원리 위에 서 있다.

- **다음 주체가 하나만 읽어도 착수할 수 있게 한다.** A에서는 결과 파일(`results/FINDINGS.md`), B에서는 JIRA Handoff 코멘트가 그 역할을 한다.
- **자동화하되 사람 게이트를 남긴다.** A에서는 공개·main 병합, B에서는 초기 도입기의 Slack 승인이 사람 손을 거친다.
- **폭주와 비용을 구조로 막는다.** A에서는 검증 게이트가 근거 없는 주장을, B에서는 Hop Count 상한과 큐가 무한 인계와 토큰 낭비를 막는다.

이 공통 원리는 [04_design_principles.md](04_design_principles.md)에 모아 두었다.
