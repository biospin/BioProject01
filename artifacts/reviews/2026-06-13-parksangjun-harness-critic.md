## 핵심 판단

원격 저장소는 기능적으로 많이 확장되어 있지만, 현재 상태의 가장 큰 약점은 **자동화 범위가 넓어진 만큼 deterministic boundary가 흐려진 것**이다. 분석 규칙, metadata, source, web dashboard, Codex/Claude bridge, HTML render가 모두 연결되어 있는데, 일부 중요한 단계가 여전히 "LLM이 prompt를 잘 따를 것"에 의존한다.

Critic의 방향은 "기능을 더 넣자"가 아니라, 이미 커진 하네스에서 **상태를 줄이고, 책임 경계를 고정하고, 실패가 조용히 지나가지 않게 만드는 것**이어야 한다.

## 주요 단점

### 1. 하네스가 과하게 넓어져 cognitive load가 큼

`AGENTS.md`가 paper, preprint, industry report, government report, blog, news, webinar까지 한 workflow로 받는다. 여기에 `core`, `lens-academic`, `lens-industry`, `methodology-brief`, HTML, dashboard까지 붙어 있다.

문제:

- 처음 사용자 입장에서는 "논문 한 편 분석"보다 "문서 처리 플랫폼"처럼 보인다.
- 각 자료 유형마다 실제로 필요한 깊이가 다른데, router가 너무 많은 것을 한 번에 약속한다.
- `source-grounding`이 master rule이 되면서 중요도는 올라갔지만, 동시에 모든 skill이 이 파일의 schema와 prefix 규칙에 의존한다.

수정 제안:

- `AGENTS.md`는 기본 paper workflow와 non-paper workflow를 더 강하게 분리한다.
- Quick Start에는 paper/preprint만 남기고, industry/government/blog/webinar는 "advanced document workflow"로 내려도 된다.
- non-paper는 default full workflow가 아니라 `source-grounding + lens-industry + brief` 정도로 제한하는 것이 안전하다.

### 2. 산출물이 너무 많이 쪼개져 paper 하나의 상태를 파악하기 어렵다

paper 하나가 다음 파일들로 흩어진다.

```text
paper-info.yaml
<paper-id>_core.md
<paper-id>_lens-academic.md
<paper-id>_lens-industry.md
<paper-id>_methodology-brief.md
<paper-id>_core.html
<paper-id>_core-with-figures.md
figures/
sources/
```

문제:

- "최종적으로 무엇을 보면 되는가"가 약하다.
- `paper-info.yaml`이 single source of truth라고 하지만, 실제 중요 판단은 `lens-industry.md`, `methodology-brief.md`, `core.md Executive Summary`에도 중복된다.
- lens-industry가 `paper-info.yaml`의 `categorization`을 갱신하므로, markdown과 yaml 사이 drift가 생길 수 있다.
- HTML과 `_core-with-figures.md`는 generated artifact인데, 분석 상태 판단에서는 종종 실제 산출물처럼 취급된다.

수정 제안:

- `paper-info.yaml`에는 사람이 판단한 prose를 최소화하고, 상태와 identifier만 둔다.
- `methodology-brief.md`를 "사람이 먼저 읽는 최종 entrypoint"로 명시한다.
- generated artifact는 `_generated/` 또는 `figures/` 아래로 묶고, source 분석 파일과 시각화 산출물을 분리한다.
- `build_index.py`가 yaml/markdown 간 drift를 검사하도록 한다. 예: yaml importance와 lens-industry importance 불일치 경고.

### 3. HTML report default-on은 fast path와 충돌

`AGENTS.md`는 Full Paper Workflow에서 HTML report를 default-on으로 둔다. 그런데 최신 critic artifact는 figure crop과 HTML/figure pipeline이 30분 wall-clock의 주요 병목이라고 진단한다.

문제:

- "빠르게 paper를 훑기"와 "HTML figure-embedded report 생성"이 같은 default path에 있다.
- `core-to-html`은 figure/table extraction까지 포함하므로, 분석 자체와 presentation artifact 생성이 섞인다.
- crop이 틀릴 때 LLM/manual correction loop가 붙으면 분석 시간이 급증한다.

수정 제안:

- default는 markdown-only로 바꾸고, HTML은 명시 요청 또는 dashboard button으로만 실행한다.
- workflow profile을 명시한다.

```text
fast: source-grounding + abstract/core 핵심, no crop, no html
full: core + lens + brief, no html by default
publish: html + figure/table extraction
slides: slide용 crop만 별도 수행
```

### 4. `skills/`와 `.claude/skills/` mirror는 drift 위험이 구조적으로 남아 있음

원격은 root `skills/`를 source로 두고 `.claude/skills/`를 mirror로 둔다. `scripts/sync-skills.sh`와 pre-commit hook도 있다.

문제:

- 실제 clone에서 `core.hooksPath`가 설정되어 있지 않으면 `scripts/hooks/pre-commit`은 동작하지 않는다. hook은 문서상 존재할 뿐 per-machine 설치가 필요하다.
- `.claude/skills`는 `skills`와 파일 수가 같아도, 사용자가 hook을 설치하지 않으면 drift를 막지 못한다.
- `.claude/agents/*.md`는 sync 대상이 아니다. 즉 skill mirror는 검사하지만 agent prompt drift는 별도 위험으로 남는다.
- `rsync --delete`는 mirror 내부에 실수로 둔 파일을 지운다. 파생 mirror라면 맞는 동작이지만, 팀원이 `.claude/skills`를 직접 수정했을 때 손실이 발생한다.

수정 제안:

- repo-level로 `git config core.hooksPath scripts/hooks`를 강제할 수 없으므로 CI 또는 dashboard startup check가 필요하다.
- `scripts/sync-skills.sh --check`뿐 아니라 `.claude/agents`가 root agent spec과 맞는지도 검사한다.
- `.claude/skills/README.md`에 "직접 수정 금지, root skills만 수정"을 넣는다.
- 가능하면 mirror를 없애고 Claude web에서 symlink/discovery가 되는지 별도 실험 후 결정한다.

### 5. `.claude/agents`에 사용자 절대경로가 박혀 있음

여러 `.claude/agents/*.md`가 다음 절대경로를 읽으라고 지시한다.

```text
/Users/kkkim/projects/autobiox/BioProject01
```

문제:

- GitHub checkout, 다른 팀원 PC, CI, web runner에서는 경로가 다르다.
- Claude subagent가 repo root를 현재 작업 디렉토리로 이미 알고 있어도, prompt가 특정 사용자 path를 강제한다.
- "팀 공유 가능한 Claude harness"라는 목표와 충돌한다.

수정 제안:

- `.claude/agents`의 절대경로를 모두 repo-relative 표현으로 바꾼다.

```text
현재 repo root의 `AGENTS.md`와 `CLAUDE.md`를 읽는다.
```

- agent prompt lint를 추가한다. 금지 패턴: `/Users/`, 개인 GitHub ID, local machine path.

### 6. Dashboard가 LLM에게 파일 복사를 맡김

web dashboard에서 PDF를 업로드하면 파일은 `artifacts/uploads/`에 저장된다. 이후 prompt에 "분석 폴더를 만든 직후 이 PDF를 `sources/`로 복사하라"고 적는다.

문제:

- source-grounding의 핵심인 PDF 보존을 deterministic backend가 아니라 LLM prompt에 맡긴다.
- LLM이 복사를 누락해도 분석은 진행될 수 있고, 그 결과 PDF-grounded analysis가 아닌 상태가 된다.
- TODO에도 "uploaded-PDF → `sources/` copy를 dashboard-side deterministic으로 만들자"가 남아 있다.

수정 제안:

- dashboard가 run prompt 생성 시점에 target folder를 아직 모른다면, 최소한 `artifacts/web-runs/<run-id>/source.pdf`로 복사하고 checksum을 기록한다.
- analysis folder 생성 후에는 helper script가 source PDF를 이동/복사하도록 한다. LLM은 그 script를 호출만 하게 한다.
- `paper-info.yaml`에 source file checksum을 기록한다.

### 7. Dashboard 실행 권한 경계가 위험하다

`web/app.py`는 Claude 실행에 다음 command를 사용한다.

```text
claude -p --dangerously-skip-permissions
```

문제:

- dashboard token이 있더라도 LAN 공유 상태에서 임의 prompt 실행 표면이 생긴다.
- token이 optional이고, default host는 localhost지만 share script는 `0.0.0.0`으로 연다.
- "논문 분석 도구"가 사실상 repo cwd에서 agent command execution launcher가 된다.

수정 제안:

- dashboard는 기본적으로 prompt 생성과 deterministic scripts까지만 담당하고, LLM 실행은 manual copy/paste를 기본값으로 둔다.
- LLM 실행 버튼은 `--dangerously-skip-permissions` 없이 가능한 모드가 있는지 먼저 확인한다.
- 최소한 allowlist prompt template만 실행하고, 사용자가 raw prompt를 임의 수정한 경우 경고 또는 실행 차단한다.
- LAN mode에서는 token 필수, localhost mode에서도 실행 endpoint는 token을 요구하도록 분리한다.

### 8. Web UI/문서에 engine 상태가 섞여 있음

최근 변경으로 paper-row Analyze button은 Claude를 기본으로 바꾸었지만, UI 문구와 TODO에는 여전히 Codex 중심 표현이 남아 있다.

예:

- `TODO.md`: "Click Run in Codex"
- `web/index.html`: "요청 만들기 후 Run in Codex 실행"
- `web/index.html`: "No active Codex job."
- `web/static/app.js`: 일부 default log가 "Run in Codex"로 남음

문제:

- 사용자는 현재 기본 engine이 Claude인지 Codex인지 헷갈린다.
- engine-aware backend를 만들었지만 UX copy는 완전히 engine-neutral하지 않다.

수정 제안:

- 모든 문구를 `Run analysis`, `No active job`, `선택한 engine` 기준으로 바꾼다.
- paper-row button도 engine selector를 사용하게 한다.
- job status schema에 `engine`을 필수로 넣고 UI에서 항상 표시한다.

### 9. 자동 metadata 생성이 과신될 수 있음

`AGENTS.md`는 Crossref API, PDF metadata, URL, 사용자 한 줄 응답 기반으로 `paper-info.yaml`을 만든다고 설명한다. 하지만 paper title, authors, venue, year, DOI는 실제로 오류가 잦은 영역이다.

문제:

- PDF metadata는 publisher template title이 들어가거나 비어 있는 경우가 많다.
- preprint와 published version이 동시에 있을 때 DOI/year/venue가 섞일 수 있다.
- `paper-id`가 metadata 오류 위에서 생성되면 나중에 folder rename 비용이 크다.

수정 제안:

- `metadata-verify`를 "commit 전 권장"이 아니라 `source-grounding`의 필수 단계로 올린다.
- `paper-info.yaml`에 `metadata_confidence`와 `verified_by`를 둔다.
- DOI/arXiv/PubMed/Crossref 중 무엇으로 확정했는지 `identity_source`를 기록한다.

### 10. `paper-info.yaml` schema가 너무 큼

원격의 schema는 identity, topics, version, citation, sources, categorization, audience, priority, related, workflow까지 포함한다.

문제:

- 한 파일이 metadata, workflow status, user priority, business categorization, cross-reference를 모두 가진다.
- LLM이 yaml을 수정할 때 indentation이나 list ordering 실수가 나기 쉽다.
- schema migration이 필요해지면 기존 paper 14개 이상을 모두 갱신해야 한다.

수정 제안:

- `paper-info.yaml`은 identity/source/status 중심으로 줄인다.
- BD/use_case/importance는 `paper-tags.yaml` 또는 generated index layer로 분리할 수 있다.
- schema version을 넣는다.

```yaml
schema_version: 1
```

### 11. 검증이 "한 paper 재실행"에 치우쳐 있음

Claude 포팅 검증은 Trevino 2021 한 건을 재실행해 Codex 출력과 비교한 것으로 보인다.

문제:

- 한 paper는 smoke test일 뿐, method paper, review paper, non-paper, supplementary-heavy paper, figure-heavy paper를 대표하지 못한다.
- "섹션 구조 동일"과 "핵심 사실 일치"는 충분하지만, 숫자 누락, figure/table drift, source coverage까지 검증한 것은 아니다.

수정 제안:

- 최소 regression set을 둔다.

```text
1. method-heavy paper
2. biology finding paper
3. review paper
4. supplementary table-heavy paper
5. uploaded local PDF case
6. paywalled / PDF missing case
```

- 각 run에서 검사할 항목: required files, yaml validity, source file exists, citations, figure count, table extraction result, index rebuild.

### 12. `artifacts/` 정책이 아직 정리되지 않음

TODO에 `artifacts/web-runs/*`를 commit할지, ignore할지, archive할지 결정 필요가 남아 있다.

문제:

- `prompt.md`, `request.json`, job metadata는 reproducibility에는 좋지만, 사용자 입력이나 local path가 들어갈 수 있다.
- logs는 ignore하지만 job json과 prompt는 commit될 수 있다.
- artifacts가 운영 기록, 발표 자료, web run record, critic 요청서를 모두 담아 역할이 넓다.

수정 제안:

- `artifacts/records/`, `artifacts/reports/`, `artifacts/web-runs/`처럼 하위 정책을 분리한다.
- web-runs는 기본 ignore하고, 공유할 run만 export script로 정리해 commit한다.
- prompt/request에 local path, token, private note가 들어가지 않는지 scrub step을 둔다.

## 수정 우선순위

| 우선순위 | 항목 | 이유 |
|---|---|---|
| P0 | `.claude/agents` 절대경로 제거 | 팀원/웹 checkout에서 바로 깨질 수 있음 |
| P0 | uploaded PDF 복사를 backend/helper script로 이동 | source-grounding 핵심을 LLM prompt에 맡기면 안 됨 |
| P0 | `--dangerously-skip-permissions` 실행 경계 재설계 | dashboard가 command launcher가 되는 위험 |
| P1 | HTML default-on 해제 및 profile 분리 | 30분 병목을 줄이는 가장 직접적 조치 |
| P1 | hook/CI로 `.claude/skills` drift 검사 강제 | mirror 구조를 유지하려면 자동 검사가 필요 |
| P1 | engine-neutral UI 문구 정리 | Claude/Codex 혼선 제거 |
| P2 | `paper-info.yaml` schema 축소 또는 versioning | 장기 유지보수 비용 절감 |
| P2 | regression set 구축 | Claude/Codex 포팅 품질 검증 강화 |
| P2 | artifacts 정책 분리 | private/local 운영 기록이 repo에 섞이는 것 방지 |

## 짧은 총평

원격 저장소의 방향은 좋지만, 현재는 "자동화된 research harness"와 "팀용 local execution dashboard"가 한 repo 안에서 너무 밀접하게 결합되어 있다. 특히 source 보존, engine 실행, skill mirror 동기화처럼 실패하면 분석 신뢰도를 바로 떨어뜨리는 단계는 LLM prompt나 per-machine hook에 맡기면 안 된다.

가장 먼저 할 일은 기능 추가가 아니라 boundary 정리다. `source-grounding`은 deterministic script가 책임지고, LLM은 분석문 작성에 집중한다. HTML/figure/dashboard는 default workflow에서 분리한다. `.claude` mirror는 유지하더라도 절대경로와 drift 검사를 먼저 고쳐야 한다.
