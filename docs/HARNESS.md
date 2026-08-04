# HARNESS.md — 랩 구조 (Agent 하네스 지도) — SpatialPathoAgent (BioProject02)

*Designed by Ka-Kyung Kim, 2026 — a reusable paper-production harness, contributed as a scaffold (CC BY 4.0).*

이 문서는 이 프로젝트의 `.claude` **논문 생산 하네스**를 하나의 연구 랩으로 본 지도다. 운영 규칙·라우팅·산출물 계약 요약은 `CLAUDE.md`의 *Agent routing & artifact contract*. 이 파일은 그 확장판(멤버 명부 + 관계도 + JD)이다.

> ⚠️ 이건 **논문 *생산* 하네스**(결과→논문·발표)다. BioProject02의 기존 **분석 파이프라인**(`agents/<role>/` 워크스페이스: data/embedding/modeling/therapeutic_evidence/critic)을 대체하지 않는다 — 그 위에 얹혀 결과를 논문으로 쓰는 레이어이고, 분석 레이어는 도메인 슬롯 `spatialpatho-analyst`가 대표한다.

## 1. 멤버 명부 (Roster)

| # | 멤버 | 벤치 | 한 줄 역할 | 상태 |
| --- | --- | --- | --- | --- |
| D | `spatialpatho-analyst` | 분석실 | **(도메인 슬롯)** WSI→embedding→phenotype→therapeutic 파이프라인 대표·eval·통계, result 파일 유지 | ✅ 채움(경로 배선) |
| 1 | `literature-scout` | 문헌·기획 | 선행연구·포지셔닝·related work | 재사용 |
| 2 | `novelty-strategist` | 문헌·기획 | 차별화 각도 + 가장 싼 입증 실험 | 재사용 |
| 3 | `research-methodologist` | 문헌·기획 | 가설·기여문·설계, 누수/통계 감사 | 재사용 |
| 4 | `manuscript-writer` | 집필실 | 프리프린트/저널/블로그 본문·초안 + 그림 연계 | ✅ 채움(집필-단계 FILL 대기) |
| 5 | `presenter` | 집필실 | 슬라이드·발표(청중 맞춤) | ✅ 채움(경로 FILL 대기) |
| 6 | `paper-critic` | 심사·QA | 제출 전 적대적 자체검토 + 그림 QA (기존 `agents/critic/` 체크리스트와 병행) | 재사용 |
| 7 | `paper-orchestrator` | 코디네이션 | 멀티-agent 작업 **계획**(실행은 PI) | 재사용 |
| 8 | `design` | 엔지니어링 | 로고·아이콘·브랜드·그림 미감 | 재사용 |
| 9 | `venue-reviewer` (**프로젝트 로컬**, 선택) | 심사·QA | 정식 venue 스타일 리뷰 문서. 검증 게이트 ① 통과 후에만 호출 | ✅ 채움 (BIOP02-103) |
| S | 그림 생성 (스크립트) | 엔지니어링 | 결과 파일에서 그림 생성·번호 정합 | FILL(스크립트 지정) |

## 2. 관계도 (일이 흐르는 표준 경로)
```
research-methodologist / literature-scout / novelty-strategist            (기획·근거)
   └─▶ spatialpatho-analyst ──▶ <FILL: result files + consolidated summary>  (분석·검증)
   └─▶ manuscript-writer ──▶ <FILL: manuscript>                              (집필)
            ║  <FILL: figure script> ──▶ <FILL: figures dir>                 (그림)
   └─▶ paper-critic (+ agents/critic/ 체크리스트) ──▶ reviewer               (심사)
            └─▶ (수정) manuscript-writer
   └─▶ <FILL: verify-gate = headline AUC/AUPRC 재계산> ──▶ presenter         (검증→발표)
```
실행 입구 = `paper-production-orchestrator` Skill(메인 루프가 실행). `paper-orchestrator`(agent)는 계획만.
- **검증 게이트**(헤드라인 숫자 재계산)와 **공개 게이트**(저자·소속·저자순서·IP·GPU 제공처)는 PI가 통과시킨다.

## 3. 멤버별 JD
권위 있는 전체 정의는 각 `.claude/agents/<name>.md` 본문. 분석=spatialpatho-analyst(기존 파이프라인 대표), 나머지는 재사용 연결조직.

## 4. 현재 하네스 상태 (성숙도)

| 항목 | 상태 |
| --- | --- |
| 멤버(agent) 정의 | ✅ 재사용 7 + 도메인 슬롯(spatialpatho-analyst) |
| 자연어 라우팅 | ✅ CLAUDE.md 라우팅표 적용 |
| 산출물 계약 | ⚠️ 경로 일부 FILL — 집필-단계 산출물(FINDINGS/manuscript/figures) 미존재(분석 진행 중) |
| 입구(Orchestrator Skill) | ✅ 설치 |
| 검증 게이트 | ⚠️ FILL — 헤드라인 AUC/AUPRC 재계산 스크립트 팀 확정 필요 |
| 미결(팀·사람 확정) | 결과요약 파일·verify-gate·headline 주장·manuscript 경로·저자순서·소속·corresponding email·GPU 제공처 |

> **이유**: BioProject02는 분석 진행 단계(sprint 0/1). 연결 조직은 지금 설치했고, 집필-단계 FILL은 **첫 write-up-ready 결과가 나오면** 팀이 채운다. 과학적 주장·숫자는 지어내지 않는다(가정 금지).
