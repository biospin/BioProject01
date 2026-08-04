# 파일럿: 외부 Agent Skill 재조사 — hyperresearch · K-Dense (2026-07-27)

> **목적:** `jordan-gibbs/hyperresearch` 와 `K-Dense-AI/scientific-agent-skills` 두 저장소에 우리가 쓸 것이 있는지 판정한다.
> **판정 기준:** 새로 만들지 않았다. 팀이 2026-07-17~18에 정한 것을 그대로 쓴다 — `blog/2026-07-18_BIOP02_09_skill-benchmark-no-borrow.md`, `docs/HARNESS_REVIEW_2026-07-17.md` §4.5.
> **결론 선요약:** **기존 "차용 없음" 유지.** 지금 설치할 것은 없다. 다만 미조사 스코프 하나와, 어느 저장소도 안 잡는 새 실패 범주 하나가 드러났다.
> **작성:** 이건규. Claude·GPT·Gemini 3모델 교차검증(같은 사실 카드, 다른 질문). 합의·불일치를 §6에 그대로 적었다.

---

## 0. 판정 기준 (인용, 새로 만들지 않음)

> "별점도, 공식이라는 표시도, 도구가 스스로 매긴 점수도 아니다. **그 도구가 우리가 실제로 겪은 실패를 잡아내는지, 그리고 다시 돌려도 같은 답을 내는지. 이 두 가지뿐이다.**"
>
> "표준적인 기계 작업은 빌려 올 수 있지만, **'이게 진짜 맞는가'를 가리는 관문만큼은 우리 손으로** 지어야 한다."

이 문서는 위 기준을 뒤집지 않는다. 적용할 뿐이다.

---

## 1. 실패셋 (합격선) — 7건 → **11건으로 갱신**

`docs/HARNESS_REVIEW_2026-07-17.md` §1.2 의 7건에, 2026-07-27 에 드러난 4건을 더했다.

| # | 실패 | 성질 |
|---|---|---|
| 1 | csv `\r` 파일명 → openslide "missing" | 파이프라인·조용한 실패 |
| 2 | bash 자기참조 → `set -u` unbound → 다운로드 성공 후 임베딩 침묵 사망 | 파이프라인·조용한 실패 |
| 3 | detached shell 에 conda 없음 → 임베딩 실패 | 파이프라인 |
| 4 | n=187 vs n=85 혼동 | 문서·주장 |
| 5 | 인용 오류 5건 — 존재하지 않는 "Williams 2022" | 문서·주장 |
| 6 | "523 slides" vs "523 cases" 단위 혼동 | 문서·주장 |
| 7 | Virchow2 HF 캐시가 `.incomplete` 인데 `du` 크기만 보고 "완료" 보고 | 파이프라인 |
| **8** | **원고 R2 가 "공개 코호트는 원리적으로 검정력 부족"이라 주장하나, 코호트 전체 양성이 평가가 본 것의 3~5배**(위 MSI 82 vs 24). 단일 70/15/15 분할의 결과지 코호트 한계가 아님 | **상태 불일치** |
| **9** | **정본 스코어보드는 "위암 endpoint 전체 저신뢰", 원고 R4 는 "Lauren 만."** 정본이 요청한 진단이 나왔는데 정본 미갱신 | **상태 불일치** |
| **10** | **논문이 몇 편인지 리더 결정·`CLAUDE.md`·Jira 스프린트가 각각 다르게 말함**(2주째) | **상태 불일치** |
| **11** | **원고가 인용한 커밋(`a693984`)이 브랜치 HEAD 가 아니어서 stale 내용 기준으로 검토가 진행됨** | **상태 불일치** |

---

## 2. 조사 범위

| 대상 | 규모 | 방법 | 기존 조사 여부 |
|---|---|---|---|
| `jordan-gibbs/hyperresearch` | 196 파일, `src/hyperresearch/` 12모듈 | 로컬 클론 + 소스 정독 | **신규** (2026-07-17 목록에 없음) |
| `K-Dense-AI/scientific-agent-skills` | **154** SKILL.md (당시 149) | 로컬 클론 + 스킬 목록 census | **기조사·기각** (병리 스코프) |

클론만 했다. **설치·`pip install` 은 하지 않았다** — `/opt/envs/spatialpatho` 격리 규율 때문.

---

## 3. K-Dense — 이미 기각됐다. 단 스코프가 한정적이었다

`docs/pilot_pathology_skills_2026-07-17.md` 판정을 재확인했고 **유효하다**:

> "본진(병리)에 차용할 스킬은 없다. 후보 5종 전부 **실행코드 0줄**이고, 우리 실패 6건 중 **0건**을 잡는다."

`skills/histolab`·`skills/pathml` 은 기존 pip 라이브러리 사용설명서다. 이 판정은 그대로 둔다.

### 3.1 그런데 조사 스코프가 세 영역뿐이었다

기존 조사는 **(a) 병리·이미지 본진 (b) 논문 집필 (c) 단일세포** 만 봤다. BIOP02 의 실제 작업 층은 더 넓다.

| 미조사 층 | 우리가 실제로 하는 일 | K-Dense 대응 후보 |
|---|---|---|
| **데이터 조달** | `guide/runbooks/download_cptac_from_idc.md`, TCGA/CPTAC WSI 다운로드 | `imaging-data-commons` |
| **치료증거 연결** | jhans Therapeutic Evidence Agent, DepMap/GDSC | `depmap` |
| 라벨·유전체 메타데이터 정합 | 라벨 추출·QC (jamie) | `genomic-coordinates`, `anndata` |

**이 층들은 기각된 적이 없다. 조사된 적이 없다.** 154개로 5개 늘어난 것 때문이 아니라, 이 스코프 구멍 때문에 좁은 재조사가 정당하다.

> ⚠️ 단, "미조사"는 "유망"이 아니다. 병리 스코프에서 나온 패턴(설명서만 있고 실행코드 0줄)이 여기서도 반복될 가능성이 높다. 실패셋 대조를 거치기 전에는 후보로도 세지 않는다.

---

## 4. hyperresearch — 실행코드는 실재한다. 그러나 우리 원고엔 못 쓴다

MIT. Python 3.11–3.13. `src/hyperresearch/` 아래 12모듈(cli·core·graph·search·web·mcp·export 등). **실행코드가 실재한다** — 이 점에서 K-Dense 병리 스킬과 다르다.

### 4.1 cite-check 를 코드로 확인했다

광고 문구가 아니라 구현을 읽었다. `src/hyperresearch/core/citecheck.py` (214줄):

```python
# parse_sources_section: Map `[N]` -> note_id by matching Sources-section URLs/titles to the vault
row = conn.execute("SELECT note_id FROM sources WHERE url = ?", (url,)).fetchone()

# triage_pairs 의 판정 범주
#   dangling — citation resolves to no vault note (finding)

def sample_needs_llm(pairs, sample_rate: float = 0.6): ...
```

읽어낸 것:

1. **대조 대상이 자기 vault SQLite 다.** 그 run 에서 hyperresearch 가 직접 받아온 소스하고만 맞춘다. Crossref·PubMed·DOI 해석이 아니다.
2. 그래서 **vault 가 없는 문서는 검사 자체가 불가능하다.** 우리 원고(`manuscript/sections/*.md`)는 우리 에이전트가 썼고 hyperresearch vault 가 없다. **실패 #5(존재하지 않는 Williams 2022)를 우리 원고에서 잡을 수 없다.**
3. LLM 스팟체크는 **60% 표본**(`sample_rate=0.6`)이다. 전수가 아니다.

즉 이 기능이 유효한 범위는 "hyperresearch 가 처음부터 끝까지 생산한 리포트"뿐이다. 우리 워크플로 전체를 이 도구로 옮기지 않는 한 쓸 수 없다.

### 4.2 벤치마크 주장은 근거로 쓰지 않는다

README 가 "DeepResearch-Bench RACE 리더보드 1위"라며 그래프를 싣는다. 그 그림의 캡션 원문:

> "**Forward-looking projection** from a stratified pilot against the leaderboard snapshot. **Third party validation is pending.**"

측정치가 아니라 투영이고 3자 검증 전이다. 본문도 "benchmarked internally"라고 쓴다. §0 기준에 따라 **판단 근거로 쓰지 않는다.**

### 4.3 우리에게 없는 기능만 추리면

`.claude/agents/` 9종, `paper-production-orchestrator`, `auto_review_gate.py`, `verify_citations.py`, `evals/` 2종과 대조해 **중복을 뺀 신규**:

| 기능 | 우리에게 없나 | 도입 판단 |
|---|---|---|
| **independence audit** — 파생 사본 클러스터링(재출판 5건이 합의 5표로 세어지지 않게) | 없음 | 발상은 참고할 만함. 우리 문헌 규모에서 실익은 미확인 |
| **run resume (manifest)** — 죽은 단계에서 재개 | 없음 | ⚠️ 우리 실패 #2·#3(침묵 사망)과 **인접**하나 겨냥이 다름. 재개는 사후 복구지 침묵 방지가 아님 |
| **persistent vault** (markdown+SQLite) | 없음 | 우리 `research/REFERENCE_LIST.md`(77편) 로 부분 대체 중 |
| 4 adversarial critics · tool-locked patcher | **있음** — `paper-critic`, `auto_review_gate` | 중복. 그리고 §5 참조 |
| cite-check | **있음** — `verify_citations.py` + `CITATION_AUDIT_2026-07-17.md` | §4.1 이유로 대체 불가 |

---

## 5. 가져오면 안 되는 것 — 검증 관문

hyperresearch 의 4 critics + tool-locked patcher + cite-check 는 **검증·비평 층**이다. 이 층을 외부에 맡기는 것은 §0 기준의 후단("관문만큼은 우리 손으로")에 정면으로 걸린다.

위험은 기술적인 것이 아니라 **규율 차원**이다. `cite-check`·`critic` 같은 이름이 붙어 있으면, 우리 내부 게이트가 잡아야 할 실패를 외부 도구가 잡아 줄 것처럼 착각하게 된다. 실제로 §4.1 에서 확인했듯 그 도구는 **우리 원고를 검사하지도 못한다.**

---

## 6. 가장 중요한 발견 — 새 실패 범주를 아무도 안 잡는다

실패셋 11건을 성질별로 재분류하면 이렇다.

| 성질 | 해당 | 잡는 수단 | 두 저장소가 잡나 |
|---|---|---|---|
| 파이프라인 조용한 실패 | #1 #2 #3 #7 | 스모크 회귀 | ❌ |
| 문서·주장 오류 | #4 #5 #6 | Critic eval | ❌ (§4.1) |
| **다중 소스 상태 불일치** | **#8 #9 #10 #11** | **현재 없음** | ❌ |

#8~11 은 2026-07-27 하루에 나왔고, 앞의 두 범주와 성질이 다르다. 런타임 오류도 아니고 한 문서 안의 오기도 아니다. **git 커밋·정본 스코어보드·Jira·원고가 서로 다른 상태를 말하는 것**이다.

`docs/HARNESS_REVIEW_2026-07-17.md` §1.2 의 경고를 여기에도 적용해야 한다:

> "이 둘을 한 바구니에 넣으면 **scorer 가 못 잡는 걸 잡는 척하게 된다.**"

세 번째 바구니가 생겼고, 그것을 겨냥한 도구는 조사한 두 저장소 어디에도 없다. **밖에서 사 올 자리가 아니라 우리가 만들 자리다** — BIOP02-107(원고↔결과문서 드리프트 체커)이 그 자리를 겨냥한다.

---

## 7. 3모델 교차검증 기록

같은 사실 카드를 주고 질문을 갈랐다. Claude(오케스트레이션·실측) / GPT(적대적 심사) / Gemini(스코프 대조).

**합의된 것**

- 기존 no-borrow 결정을 뒤집을 근거는 없다 (GPT #1)
- README 벤치마크는 자기평가 점수로 취급, 근거로 쓰지 않는다 (GPT #4)
- 검증 관문 층은 외부에 맡기지 않는다 (GPT #2, Gemini #6)
- K-Dense 재조사는 **데이터 조달·치료증거 스코프에 한해** 정당하다 (Gemini #5)
- #8~11 은 기존과 다른 범주다 (Gemini #3 — "다중 소스 형상/상태 불일치")

**갈린 것 — 기록해 둔다**

hyperresearch cite-check 를 시범 도입할지에서 갈렸다.

- **Gemini**: 도입 자체가 선을 넘는다. 우리에게 이미 `verify_citations.py`·eval 코퍼스가 있다.
- **GPT**: 도입하되 **독립 프로세스가 아니라 `evals/citation_verifier/` mutation fixture 에 붙인 비교군으로만**. 금지 조건 3개(PR 게이트 대체 금지 · 원고 자동수정 금지 · 실패셋 미통과 시 "도입" 표현 금지).

작성자 판단은 GPT 쪽이다. 근거는 §4.1 을 코드로 확인하기 전까지 "우리보다 나은가"에 답할 수 없었다는 것이고, 그 확인 비용이 낮다는 점이다(`CITATION_AUDIT_2026-07-17.md` 77편 baseline 이 이미 있어 diff 파일럿이 싸다). **다만 §4.1 확인 결과 vault 결합이 드러났으므로, 이 비교군조차 실익이 크지 않을 수 있다.** 리뷰에서 판단을 구한다.

---

## 8. 권고 (전부 조건부, 결정은 팀)

1. **차용 없음 유지.** 두 저장소에서 지금 설치할 것은 없다.
2. **미조사 층만 좁게 재조사.** K-Dense `imaging-data-commons`·`depmap` 을 실패셋 11건 대조로. 클론만, 설치 없음.
3. **hyperresearch cite-check 비교군** (선택, §7 에서 갈린 항목). 채택 시 금지 조건 3개를 함께 명문화.

---

## 9. 확인 못 한 것 (정직 기록)

- **K-Dense `imaging-data-commons`·`depmap` 의 실행코드 유무를 아직 세지 않았다.** 권고 2가 그 작업이다. 이 문서는 "미조사"라고만 말하고 "유망"이라고 말하지 않는다.
- **hyperresearch 를 실제로 돌려 보지 않았다.** 설치가 env 격리 규율에 걸려 소스 정독으로만 판단했다. `sample_rate=0.6` 이 런타임에 어떻게 바뀌는지 등은 미확인.
- **independence audit·run resume 의 실효는 미측정이다.** 우리 문헌 규모(77편)에서 파생 사본 클러스터링이 실익이 있는지 재보지 않았다.
- K-Dense 154개 중 **스킬 이름만 census 했고 전수 정독은 하지 않았다.** 병리·집필·단일세포는 기조사분을 재확인했고, 나머지는 §3.1 표의 후보만 지목했다.
