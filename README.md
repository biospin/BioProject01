# BioProject01 — chromatin→transcription lag 와 RNA velocity 출력의 신뢰도

**목표**: gene별 **chromatin→transcription lag**(activation/shutdown 시점차)을 정량해서, baseline
epigenomic feature로 **epigenetic drug response timing** 을 예측한다.
1차 데이터셋 = **Human HSPC 10x Multiome (GSE209878)**.

**현재까지의 결론** — 그 전제인 "lag이 method-robust한 양인가"(H1)를 먼저 검정했고, **아니었다.**
lag은 method 간 크기·방향 모두 재현되지 않고, ATAC 셔플 음성대조에서도 변하지 않아 chromatin 생물학이
아니라 **모델 구조에서 나온 양**으로 판명됐다. 대신 **전사율 α는 method-robust하고 baseline ATAC으로
예측 가능**하며, 이 순서는 외부 데이터셋 다섯 곳에서 보존된다(그중 하나는 fit 전 봉인한 사전등록 통과).

> ⚠️ **수치는 이 문서에서 인용하지 않는다.** 결과·해석의 정본은
> `pipeline/hspc-velocity-benchmark/results/FINDINGS.md`(★통합 결론)이고, 원고는 `manuscript/draft_v2.md`
> (한국어 `draft_v2_ko.md`)다. 합격 기준·임계는 봉인 문서(`PREREGISTRATION_gse205117.md` 등)에서
> `파일:줄`로 인용한다 — 발표자료·요약본의 숫자를 임계로 쓰지 않는다(`CLAUDE.md` 방법론 주의 6).

- GitHub `biospin/BioProject01` · JIRA `BIOP01` · Confluence space `VC` > 프로젝트#01 (→ `Project-Info.md`)
- 정본 브랜치 = **`main`**. 팀 작업 브랜치 = `kkkim-pipeline`. (아래 [브랜치 지도](#브랜치-지도))

---

## 리포 지도

| 경로 | 무엇 |
| --- | --- |
| `pipeline/hspc-velocity-benchmark/` | **연구 본체.** 실행 코드(`scripts/` P0–P5)·격리 env(`env/`)·결과(`results/`)·그림(`figures/`)·원고(`manuscript/`)·설계(`DESIGN.md`)·데이터 출처(`dataset/`, `download_manifest.tsv`, `P0_provenance.md`) |
| `manuscript` | 위 `manuscript/` 로 가는 심볼릭 링크(단축 경로) |
| `paper_analysis/` | 선행연구 **dual-lens 분석 14편**(+ 스쿱 점검 1편) + 색인 `_index/`. 파이프라인 method 선택의 근거 |
| `AGENTS.md` + `skills/` | **데이터셋 분석 하네스** — dataset 4종 × task 4단계. 라우터 = `skills/ROUTES.md` |
| `.claude/` | **논문 생산 하네스** — agent 10종 + 오케스트레이터 Skill(`.claude/skills/paper-production-orchestrator/SKILL.md`) + 글쓰기 규율(`.claude/rules/writing-style.md`) |
| `harness.yaml` | 위 두 하네스의 **구성 SSOT(manifest)**. 문서·코드는 이 파일을 따른다 |
| `scripts/harness_doctor.py` | manifest ↔ 실물 대조 **검진기**(팬텀 역할·팬텀 경로) |
| `harness_after/` | 검진기 자체 테스트 18종(`tests/test_harness_doctor.py`) + 교체용 after 버전 |
| `evals/reproducibility_pilot/` | 사전등록 채점을 재현하는 eval + 회귀 케이스 코퍼스 |
| `docs/` | 랩 지도 `HARNESS.md` · 인프라 정본 `SHARED-INFRA-GUIDE.md` · 로드맵/정합성 보고 |
| `guide/` | 과제·가이드 원문(주차별 과제, 프로젝트 기획서) |
| `onboarding_gglee/` | 온보딩 1~3주차 산출물·회고 |
| `ai_scientist/` | "AI scientist" 구성 개념 문서(하네스 설계 배경) |
| `artifacts/` | 파이프라인 run 로그·리포트 요약 보관 규칙 |
| `CLAUDE.md` | 에이전트 운영 규칙 — 라우팅표·산출물 계약·**완료의 정의(DoD)**·commit 규칙 |
| `BIOP02_LINK.md` | BIOP02(SpatialPathoAgent)와의 cross-reference. **요약본, 정본 아님** |

---

## 하네스와 그 정기검진

문서가 실재하지 않는 역할·경로를 가리키면 팀은 그 문서를 계속 믿는다. 2026-07 조사에서 실제로
그런 결함 4종이 나왔다(팬텀 역할, cwd 의존 침묵 폴백, 게이트 순서 역전, 머지로 인한 `skills/` 41파일
유실). 개별 수리 대신 **구성 자체를 검증하는 게이트**를 뒀다:

```
harness.yaml            ← 단일 기준표(어떤 역할·산출물·게이트가 있어야 하는가)
  └ scripts/harness_doctor.py       ← 기준표 ↔ 실물 대조. 팬텀 역할·팬텀 경로를 FAIL
      └ harness_after/tests/test_harness_doctor.py   ← 검진기 자체 테스트 18종
          └ .github/workflows/harness-doctor.yml     ← PR CI (blocking)
```

로컬에서 같은 검사를 돌린다:

```bash
pip install pyyaml
python harness_after/tests/test_harness_doctor.py                 # 18/18 이어야 한다
python scripts/harness_doctor.py --repo . --manifest harness.yaml # PASS 여야 한다
```

`README.md`·`AGENTS.md`·`CLAUDE.md`·`docs/HARNESS.md`·오케스트레이터 SKILL 이 스캔 대상이다.
**이 문서에 백틱으로 쓴 경로도 검사 대상이므로**, 없는 경로를 적으면 PR이 막힌다.

### 실행 도구 현황 (2026-07-27 실측)

`skills/` 의 skill·agent 정의는 **OpenClaw/Codex 네이티브 포맷**을 유지한다. 다만 **팀 컨테이너 6개 중
`openclaw` CLI가 설치된 곳은 0개**다. 현재 실제 실행은 Claude Code / codex 로 하며, OpenClaw 도입
여부는 미결(회의 상정)이다. **문서는 openclaw 설치를 전제로 쓰지 않는다** — 전제로 쓰면 그 문서는
아무도 실행할 수 없는 절차가 된다.

---

## 브랜치 지도

2026-07-27 기준. `main` 과의 차이는 `git rev-list --count origin/main..<branch>` 실측.

| 브랜치 | 상태 |
| --- | --- |
| main | **정본.** PR #5 → #7 머지로 하네스 게이트·`skills/` 복원 반영 완료 |
| kkkim-pipeline | 팀 작업 브랜치. main 으로 승격하는 경로 |
| gglee | 이건규 작업. PR #5 로 반영 완료 |
| feat/manuscript-condenser | 진행 중 (PR #6 열림) |
| jamie-paper-agent | 진행 중 (cross-paper insight 파이프라인) |
| kkkim-paper-agent · braveji-paper-agent · sezinie-paper-agent | **archive(보존만).** 새 작업은 하지 않는다 |
| epigenomics · braveji/team-owner-mousebrain · fix/BIOP01-22-braveji-env-repro | main 에 병합 완료 — 정리 가능 |
| team-table-update-20260709 | **미병합 1커밋**(팀 담당표 갱신). 당시 README 구조가 지금과 달라 그대로는 적용되지 않는다 |

> 브랜치 이름은 백틱으로 감싸지 않는다 — 슬래시가 든 백틱 토큰을 정합성 게이트가 **리포 경로**로
> 읽어 팬텀으로 잡기 때문이다. 게이트가 브랜치 이름과 경로를 구별하지 못하는 것은 알려진 한계다.

---

## 빠른 시작

```bash
# 1) 격리 conda env (framework 별로 분리 — CUDA 충돌 회피)
bash pipeline/hspc-velocity-benchmark/env/setup_envs.sh
# 2) 데이터 (GSE209878; 체크섬은 download_manifest.tsv)
bash pipeline/hspc-velocity-benchmark/scripts/download_data.sh
# 3) 공통 전처리 (P1)
conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p1_build.py
```

상세: `P0_provenance.md` · `P1_README.md` · `DESIGN.md` · `env/README.md`.
서버 접속·GPU 예절·env 위치는 `docs/SHARED-INFRA-GUIDE.md` 가 정본이다(`CLAUDE.md` 에 중복하지 않는다).

**헤드라인 숫자를 커밋·공개하기 전에** 결정론적으로 재계산해 `FINDINGS.md` 와 대조한다 —
`p3_concordance.py` + `p3_crossdataset_concordance.py` + `p3_scrambled_null.py`. 전체 체크리스트는
`CLAUDE.md` 의 **완료의 정의(DoD)**.

---

## 이 리포에 없는 것

- **`HANDOFF.md` · `TODO.md` · `SESSION-LOG.md`** — 개인 작업기록. `.gitignore` 등재된 **로컬 전용**이라
  새 clone 에는 없다. 문서가 이들을 필수 산출물로 부르지만 리포에서 찾지 말 것.
- **원본 데이터·대용량 binary**(`*.h5ad`/`*.h5mu`/`*.loom`/PDF) — tracked 는 `*.md`/`*.yaml`/요약 `*.tsv`/코드.
- **conda env 실체** — 팀 공유 서버에 있고 git 미추적. 위치는 `docs/SHARED-INFRA-GUIDE.md`.

## 팀·추적

담당 데이터셋과 소유자의 **정본은 Confluence 프로젝트#01 페이지와 JIRA** 다.
⚠️ 리포 안 `Project-Info.md` 의 팀 표는 그 정본보다 뒤처져 있다 — 인용하지 말고 위를 볼 것.

commit 메시지 규칙, 언어, 저자 표기는 `CLAUDE.md` 를 따른다.

---

## 출처·라이선스

- 데이터셋 분석 하네스(`AGENTS.md` + `skills/`)는 **박상준(@poqopo) `Harness_Baseline`** 에서 반입해
  이 프로젝트에 맞춘 것이다. 원저작자 박상준 — 원 repo LICENSE 미지정이므로 공유·수정은 동의 전제.
- 논문 생산 하네스(`.claude/` + `docs/HARNESS.md`)는 *Designed by Ka-Kyung Kim, 2026 — reusable
  paper-production harness scaffold (CC BY 4.0)* 의 설치본이다.
- 리포 라이선스는 `LICENSE`.
