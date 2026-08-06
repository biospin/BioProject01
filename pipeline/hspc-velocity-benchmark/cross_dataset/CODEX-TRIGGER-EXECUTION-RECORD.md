# codex 트리거 실증 기록 — BIOP01-45, 2026-08-06

> 성격: 워커 계층(run_from_manifest.sh + runner_manifest.yaml)을 실제로 무엇으로 돌렸고, 무엇이
> 나왔고, 무엇이 막혔는지의 이력. 설계·계획은 `ORCHESTRATION-WIRING-DESIGN.md`.
> 결론: **워커층·재현성·codex 트리거 모두 통과.** codex 는 샌드박스 바이패스(`--dangerously-bypass-approvals-and-sandbox`)로 래퍼를 완주(exit 0). 트리거 결정 A(codex) 실증 완료.

---

## 0. 한 줄 요약

트리거 결정 A(codex)를 서버에서 실증했다. **워커 래퍼 dry-run 과 byte-identical scorecard 는 통과**했고,
**codex 자체도 정상**(authed·connected·gpt-5.6-sol)이었으나, **codex 의 실행 샌드박스(bwrap)가 이
환경에서 namespace 를 못 만들어** 모든 exec 가 exit 1 이었다. 우리 래퍼는 신뢰 코드이므로
**`--dangerously-bypass-approvals-and-sandbox` 로 샌드박스를 끄면 성립**한다.

---

## 1. 실행한 것 (kkkim 서버, 2026-08-06)

| # | 명령 | 목적 |
|---|---|---|
| 1 | `bash cross_dataset/run_from_manifest.sh --dataset gse205117 --dry-run` | 워커층 단독(codex 없이, GPU 불요) |
| 2 | `codex doctor` | codex 인증·런타임 health |
| 3 | `codex exec "…run_from_manifest.sh … --dry-run…"` | codex 가 워커를 구동하는가(핵심 실증) |
| 4 | `codex exec "…--dry-run 빼고…"` | 실제 실행(전 SKIP 이라 GPU 불요) |
| 5 | `conda run -n scv-preprocess python -u cross_dataset/p3_prereg_gse205117.py` | byte-identical scorecard 재생성 |

---

## 2. 결과

### ✅ 워커 래퍼 (dry-run) — 통과

전 stage SKIP + required_cols OK + `DONE` + exit 0. gse205117 산출물이 이미 있어 GPU·데이터 불요.

```
[floor]        SKIP  required_cols OK: gene,fit_alpha,fit_likelihood
[multivelo]    SKIP  required_cols OK: gene,fit_alpha,fit_t_sw1,fit_t_sw2,fit_likelihood
[dl_prep]      SKIP  (하위 산출물 존재 → GPU substrate 재생성 불요)
[multivelovae] SKIP  required_cols OK: gene,vae_alpha,vae_alpha_c
[moflow]       SKIP  required_cols OK: gene,cs_lag_median
[prereg]       SKIP
DONE — 전 stage 해소(SKIP/RUN) + 계약 충족   (exit 0)
```

### ✅ byte-identical scorecard — 통과

`p3_prereg_gse205117.py` 재생성 → 6 PASS / 0 FAIL. 커밋본과 **`git diff` 0**(완전 동일).
paired bootstrap B=10,000·seed=20260707 고정 → 결정론적 재현 확인. 남아 있던 서버 항목 하나 닫힘.

### ⚠️ codex 트리거 — 샌드박스 벽

`codex doctor`: 16 ok. codex 0.146.1, auth=chatgpt(tokens), websocket connected(HTTP 101),
model=gpt-5.6-sol, sandbox=restricted+bwrap. **codex 자체는 정상.**

그러나 `codex exec` 가 명령을 돌리려 하자 매 exec 마다:

```
bwrap: No permissions to create a new namespace, likely because the kernel does not
allow non-privileged user namespaces.
→ exit 1 (dry-run·실제 실행 모두, 스크립트 시작조차 못 함)
```

---

## 3. 진단

- **`kernel.unprivileged_userns_clone = 1` 인데도 실패한다.** userns 자체는 허용돼 있으나, codex 를
  띄운 **VS Code-SSH 중첩 환경**에서 codex 번들 bubblewrap 이 nested user namespace 를 못 만드는 것으로 보인다.
- `apt install bubblewrap`(시스템 bwrap)로는 안 풀린다 — bwrap 부재가 아니라 커널/중첩 문제다.
- `openai.yaml` 은 현재 `default_prompt`(모델 플랜 작성)만 있고 래퍼를 참조하지 않는다. 그래서 이번 실증은
  openai.yaml 자동 트리거가 아니라 **`codex exec` 로 래퍼를 직접 구동**하는 형태였다.

---

## 4. 해결 · 재시도

우리 래퍼는 신뢰 코드이므로 샌드박스를 끄고 돌린다(남의 코드엔 쓰지 말 것):

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  "cd ~/project/BioProject01/pipeline/hspc-velocity-benchmark && \
   bash cross_dataset/run_from_manifest.sh --dataset gse205117 --dry-run"
# 또는:  -c sandbox_mode=danger-full-access
```

**성공 판정 → 확인됨(2026-08-06)**: 위 바이패스 명령으로 codex 가 래퍼를 실제 실행 —
`succeeded in 4ms`, 전 stage SKIP, `DONE`, exit 0. **트리거 결정 A(codex) 실증 완료.**

---

## 5. 남은 것 · 함의

- ~~codex 바이패스 재시도~~ — **완료.** 바이패스로 codex 가 워커를 완주(exit 0). 트리거 A 확정.
- **openai.yaml → 래퍼 자동 배선** — 완전 자동(사람이 `codex exec` 안 치고 openai.yaml 로 트리거)하려면
  skill/openai.yaml 프롬프트에 "run_from_manifest.sh 실행" 지시를 넣어야 한다(이건규 님 skill / 지용기 님 워커층 소관). 실증 후 결정.
- **카운슬(BIOP01-81) GPT leg** — 같은 방식(`codex exec` 바이패스)으로 개통 가능. 이 실증이 그 선결.

## 6. 변경 이력

- 2026-08-06 최초 작성 + 당일 갱신. 워커 dry-run·byte-identical 통과, codex 샌드박스 차단 진단 → **바이패스로 codex 완주(exit 0) 확인**. 트리거 A(codex) 실증 완료.
