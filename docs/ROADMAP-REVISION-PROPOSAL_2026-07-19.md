# BIOP01 로드맵·역할 재정비 제안 (2026-07-19)

> 작성: 김가경(kkkim). 대상 문서: Confluence VC "프로젝트 로드맵 & 구성원별 할 일 (2026-05-29)" (page 35684354, v4, 2026-07-09 최종수정, 소유: biospin-leader/지용기).
> 목적: 2026-05-29 로드맵 이후 실제 진도가 크게 나가 역할·범위·과학 방향을 재정비할 필요가 있어, 오케스트레이터(지용기)와 팀 논의용 제안을 정리한다.
> **주의(거버넌스):** 지용기는 **오케스트레이터·로드맵 페이지 소유자**이지 BIOP01 프로젝트 리더가 아니다. **BIOP01 프로젝트 리더는 아직 미정.** 아래 리더/주저자 관련 항목은 결정 사항이 아니라 팀 논의 안건이다.

## 1. 로드맵 대비 실제 진도 (2026-05-29 → 2026-07-19)

로드맵은 3-step(Step1 lag 정량 → Step2 baseline feature 예측 → Step3 perturbation timing 검증)을 Phase 1/2로 나누고 데이터셋을 4명에 배분한 상태다. 그 사이 HSPC 라인(kkkim)이 Phase 1을 넘어 **완결된 벤치마크·논문 단계**까지 진행됐다.

**kkkim(HSPC, GSE209878) 실제 산출:**
- 풀 파이프라인 P0~P5: 다운로드·통일 전처리·velocity 5종(scVelo floor / MultiVelo / MultiVeloVAE / MoFlow / CRAK-Velo) + lag 정량(Step1) + baseline feature 예측 검토(Step2)
- **5-method head-to-head 벤치마크** + **5개 외부 시스템 cross-dataset 재현**(HSPC·macrophage·BMMC·gastrulation·brain)
- **외부 실측 construct-validation**: α vs TT-seq 합성율(회복), γ vs 실측 분해율(미회복/역방향)
- **사전등록(GSE205117) 6/0 통과** (fit 산출 전 commit 해시 봉인)
- **Genome Biology 타겟 manuscript**(draft_v2): 결정론적 재계산 게이트 통과 + 적대적 critic MAJOR 3건 해소
- 블로그 7편(자기반증 시리즈) + 재현성 번들 + 인용검증 + 방법론/QC reviewer 역할 수행

## 2. 재정비가 필요한 4가지

### (1) kkkim 역할 재정의 + 프로젝트 리더 논의
- 페이지: "HSPC 데이터셋 담당 + 방법론/QC reviewer 겸임".
- 실제: **벤치마크·manuscript를 단독 리드**해 GB 투고 단계까지 끌어옴. reviewer 역할도 수행.
- 제안: kkkim을 **벤치마크·논문 리드(주저자 후보)**로 재정의. **BIOP01 프로젝트 리더가 미정**이므로, 실제 진도를 고려해 리더/주저자 역할을 팀에서 확정하는 안건으로 올린다.

### (2) 과학 방향 변경 반영 (로드맵의 3-step 전제 수정)
- 원 목표: "lag → 약물반응 타이밍 예측".
- 검정 결과: **lag은 method-robust하지 않고**(cross-method |ρ|≤0.08, sign near-chance), **약물-타이밍 테스트는 null**(약물데이터 5·14일 vs 크로마틴 기전 시·분 = 타임스케일 불일치).
- 재프레이밍: 산출물은 **"velocity 출력 신뢰 결정지도"(방법론 벤치마크 논문)**. α만 재현+외부검증 양축 앵커, lag·γ는 불신·직교검증 대상.
- Phase 2(perturbation timing 검증): "분리"가 아니라 **"올바른 타임스케일(시간 단위) perturbation 데이터가 다음 실험"**으로 재서술.

### (3) 데이터셋 담당 중복 조율
- BIOP01-24(mouse embryonic brain / 서정한): **해야 할 일**(미착수). 그러나 kkkim 벤치마크가 **E18 mouse brain을 cross-replication에 이미 사용**.
- BIOP01-42(human brain / 박세진): **해야 할 일**(미착수). kkkim 벤치마크가 **human brain도 이미 사용**.
- 조율안: (a) 벤치마크 replication으로 흡수해 해당 티켓 close, 또는 (b) 담당의 심층 per-dataset 분석을 벤치마크 위 별도 기여로 재정의. 어느 쪽이든 **중복·선점 리스크 제거**를 위해 오케스트레이터가 조율.

### (4) JIRA 추적 공백 메움 — **발행 완료 (2026-07-19)**
- 로드맵 자신이 지적한 갭("Phase 1 작업이 task로 안 올라가 추적 불가"). HSPC 벤치마크·논문은 그동안 **JIRA 미등록**이었음(로드맵 표에서 HSPC 행에 티켓번호 없음).
- 조치 완료 — 에픽 + 완료작업 5 + 리뷰요청 1 신규 발행:
  - **BIOP01-46 (에픽, 진행 중, kkkim)**: HSPC velocity 신뢰 벤치마크 & GB manuscript
  - **BIOP01-47~51 (완료, kkkim)**: 파이프라인 P0~P5+Step1/2 · 5-method 벤치마크+5-dataset 재현 · 외부 실측검증 · 사전등록6/0+음성대조 · GB manuscript+번들+블로그
  - **BIOP01-52 (미배정, 리뷰요청)**: manuscript 독립 critic/리뷰 — **다른 팀원에게 배정 요청**(kkkim 단독 리드였으므로 독립 시각 필요). 오케스트레이터 라우팅 요망.

## 3. 리더 결정 4건 상태 갱신 (페이지 §4, 현재 전부 미체크)
| # | 페이지 결정사항 | 실제 상태(2026-07-19) |
|---|---|---|
| 1 | 데이터셋 축소(4개 vs 2~3개) | 사실상 발생 — HSPC 집중 + 재현용 5시스템 확장 |
| 2 | GPU/스토리지 확정 | GPU 실사용(A6000) — 사실상 해소, 문서화만 필요 |
| 3 | JIRA Phase 1 task 등록 | 부분 — 24/41/42 존재, HSPC 벤치마크·논문은 미등록 → 본 제안 §2(4)로 메움 |
| 4 | Phase 2 분리 공식화 | **재정의 필요** — 분리가 아니라 "올바른 타임스케일 perturbation" 후속으로 |

## 4. 요청
오케스트레이터(지용기)와 팀에 위 4가지 재정비를 요청한다. 특히 (1) 리더/주저자 역할 확정과 (3) 데이터셋 중복 조율은 팀 결정이 필요하다. 본 제안본과 함께 Confluence 페이지에 진도 갱신 댓글을 게시하고, HSPC 벤치마크·논문 추적 에픽을 신규 등록한다.
