# 재현성 회귀 eval 파일럿 (BIOP01)

> **상태:** 파일럿. 실행·검증 완료(2026-07-17), 커밋 전 kkkim 검토 대기.
> **대상:** braveji(지용기)님의 **재현성 회귀** — velocity method 간·데이터셋 간 **재현 일치도**.
> **근거:** `BioProject02/docs/HARNESS_REVIEW_2026-07-17.md` §2·§3 (Leader 승인) ·
> 원 제안 `~/collab_workspace/Presentation/docs/AutoBioX_하네스_에이전트_점검_2026-07-17.md` §5.2.
> **1단계(BIOP02 Critic 파일럿):** `BioProject02/evals/critic_pilot/` — 이 파일럿의 **구조 원본**.

---

## 1. 무엇을·왜

하네스 리뷰 §2가 BIOP01 적용 대상으로 지목한 것: *"지용기님 재현성 회귀(ref/compact/reset diff)를
eval 스위트로. scorer = **4종 교차 재현 일치도**."*

이 파일럿은 BIOP01의 **봉인된 사전등록 재현 검정**을 Inspect eval로 형식화한다. 채점 대상은 velocity
벤치마크가 산출하는 **재현성 보고서**(cross-method / cross-dataset concordance)이고, 임계는 전부
**이미 봉인된 사전등록에서 인용**한다 — 이 eval이 스스로 정하지 않는다.

핵심 내용 (BIOP01 고유):

| leg | 통과 방향 | 의미 |
|---|---|---|
| **α (전사속도)** | ρ가 **높아야** pass (≥ 0.50) | method를 바꿔도 재현된다 = **robust leg** |
| **lag (chromatin→transcription)** | ρ가 **낮아야** pass (≤ 0.15) | method를 바꾸면 재현되지 **않는다** = **fragile leg** |

> ⚠️ **두 leg의 통과 방향이 반대다.** 프로젝트의 헤드라인 발견이 *"lag은 재현되지 않는다"*이므로,
> **lag ρ가 높으면 주장이 깨진다**(FAIL). α의 방향을 lag에 그대로 적용하면 모든 판정이 뒤집힌다.
> `mutation_check.py`의 `invert_threshold` 뮤턴트가 이 실수를 겨냥한다.

## 2. ⚠️ 실물이 정본 — 문서와 다른 점 2가지

작업 지시가 "문서가 말하는 것과 실제가 다를 수 있다 — 실물이 정본"이라 했고, **실제로 두 군데 달랐다.**

**(a) "ref/compact/reset diff"라는 실물은 BIOP01에 없다.**
이 표현은 회의록(원 제안 p.33 지용기님 작업항목 ①, §5.2, §6)에만 존재하고 BIOP01 저장소 전체에
`compact`/`reset` diff 자동화의 코드·결과·커밋이 **없다**(git log 전 브랜치 + 전체 grep 확인). 문맥상
paper-agent skill의 **대화 컨텍스트 상태**(ref / compact / reset) 간 산출물 diff를 뜻하는 계획 항목으로
보이며, **착수되지 않았다.**
반면 **같은 §5.2가 scorer를 "4종 교차 재현 일치도 ≥ 임계값"으로 규정**하고, 하네스 리뷰 §2도 이를
그대로 채택했다. **그 실물은 존재한다** — 아래 §3. 그래서 **실재하는 쪽(교차 재현 일치도)** 을 대상으로 삼았다.

**(b) "α 0.88 기준선"은 임계가 아니라 관측값이다.**
원 제안 §5.2는 *"(예: 전사속도 α 0.88 기준선)"* 이라 쓰지만, **0.88은 HSPC에서 실제로 관측된 α
concordance**(`results/concordance.md` §3.6 `Spearman(alpha) = +0.882`; `FINDINGS.md` "α(method 간
ρ=0.88)")이지 게이트가 아니다. **봉인된 임계는 ρ ≥ 0.50**이다
(`cross_dataset/p3_prereg_gse205117.py`, "변경 금지 — 바꾸면 git에 남는다").
→ 이 eval은 **0.50을 쓴다.** 0.88을 임계로 박으면 사전등록을 사후에 조이는 것이고, 실제로 통과한
gastrulation(+0.927)·macrophage(+0.865)를 제외한 다른 축이 임의로 FAIL 난다.

## 3. 대상 실물 (BIOP01에서 찾은 것)

| 구성요소 | 경로 | 성격 |
|---|---|---|
| **봉인된 사전등록** | `pipeline/hspc-velocity-benchmark/manuscript/PREREGISTRATION_gse205117.md` | 6개 예측 + 임계 + **반증 기준**. fit 산출 전 봉인(커밋 해시가 시점 봉인) |
| **채점기** | `.../cross_dataset/p3_prereg_gse205117.py` | 결정론적. 임계 T1–T4를 코드로 고정 |
| **채점 결과** | `.../results/prereg_gse205117_scorecard.{csv,md}` | **6 PASS / 0 FAIL** |
| **재현 축 5종** | `.../results/concordance{,_macrophage,_e18_mouse_brain,_human_brain,_GSE194122_bmmc}.md` | HSPC + 외부 4 + gastrulation |
| **정합성 게이트** | `.../results/clean_concordance_gate.md` | 헤드라인의 CRAK 의존·MultiVelo 부호 구조 판정 |

**임계 출처 (전부 인용, 이 eval이 정하지 않음):**

| # | 예측 | 사전 임계 | 반증 기준(주장이 깨지는 지점) | 이 파일럿의 scorer |
|---|---|---|---|---|
| 1 | within cross-method α 재현 | ρ ≥ **0.50** (T1) | ρ < **0.30** | `alpha_reproducibility` |
| 2 | within cross-method lag 재현 | ρ ≤ **0.15** (T2) | ρ ≥ **0.50** | `lag_fragility` |
| 3 | α > lag 순서 | Δρ ≥ **0.35** (T3) | 순서 역전(Δρ < 0) | `alpha_lag_dissociation` |
| 4 | cross-dataset 재현 | cross α > **0.20** (T4) 且 > cross lag | — | `cross_dataset_replication` |
| 5 | per-gene 재현 격차 | lag 불일치 > α 불일치 | — | `prereg_adherence` |
| 6 | priming 극대에서도 fragile | #2 且 #3 | — | (파생 — `run_real_artifacts.py`) |

`caution`은 이 eval이 만든 **band 이름이지 새 임계가 아니다**: 사전 임계와 사전등록 자신의 반증 기준
**사이**(예: α 0.30–0.50)를 뜻한다. 두 숫자 모두 사전등록에 적혀 있다. "예측은 FAIL이나 논지가
반증된 건 아니다"를 `fail`과 뭉개지 않기 위한 구분이다.

## 4. 실행

```bash
cd evals/reproducibility_pilot

# 1) 케이스 채점 (stdlib만 — velo-* env 불필요, 어떤 python3에서나)
python3 run_pilot.py

# 2) 뮤테이션 체크 — 스코어러가 케이스에 진짜 제약되는지 (필수)
python3 mutation_check.py

# 3) 실물 채점표 재현 — 커밋된 6 PASS / 0 FAIL 을 재현하는가
python3 run_real_artifacts.py

# 4) Inspect eval (CI 스토리용)
/opt/envs/spatialpatho/bin/inspect eval reproducibility_pilot.py --model mockllm/model --log-dir logs/inspect

# 케이스 재생성
python3 build_cases.py
```

**⚠️ env 주의.** `scorers.py`·러너·`mutation_check.py`는 **stdlib 전용**(numpy/pandas/scipy 없음)이라
맨 `python3`로 돈다. inspect_ai는 BIOP01의 `velo-*` env에 **없고, 넣지 않는다**(CLAUDE.md:
velo-* ↔ spatialpatho **통합·rename 금지**). 그래서 inspect는 `/opt/envs/spatialpatho/bin/inspect`로
실행하되 **eval 도구 런타임으로만** 쓴다 — 이 eval은 BIOP02에서 아무것도 import하지 않고 BIOP01
파일만 읽는다. **BIOP01 파이프라인 의존성이 아니다**(stdlib 러너가 그 증거).

**이 eval은 BIOP01 파이프라인·데이터를 읽기만 한다.** 재계산·재fit·수정 없음.

## 5. ⚠️ 범위 한계 (반드시 읽을 것)

**(a) 임계 적용을 검증하지, 통계를 재계산하지 않는다.**
`run_real_artifacts.py`는 커밋된 scorecard의 ρ/CI **값을 읽어** 임계를 적용한다. bootstrap ρ를
`results/*_genes.csv`에서 다시 계산하지 **않는다**(numpy/pandas/scipy + velo-* env 필요 = "eval은 읽기만"
위반). **따라서 커밋된 ρ 자체가 틀렸다면 이 eval은 틀린 판정을 그대로 재현한다.** 통계 재계산은
채점기(`p3_prereg_gse205117.py`)의 책임이고, 그쪽이 bootstrap을 owns한다. 이 eval은 그 위층이다.

**(b) 보고서 층만 본다 → artifact 층 결함은 구조적으로 못 잡는다.**
실제 실패 6건 중 **2건 적발 / 4건 미적발**(`run_pilot.py` coverage 표, 정직 보고):

| # | 실제 실패 (git 근거) | 결과 | 이유 |
|---|---|---|---|
| RC-01 | `06008c1` MoFlow 미배선 → MV×VAE 치환, 잠정 "6 PASS" | ✅ **적발** | 이탈이 **기록**돼 있음 → `prereg_adherence` caution |
| RC-04 | `clean_concordance_gate.md` §3 MultiVelo(상수 부호)를 부호 검정에 투입 = INVALID | ✅ **적발** | 검정 종류(`sign_agreement`)를 봄 |
| RC-02 | `a34c10d` 컬럼명 `cs_lag` 오타 → **조용한 VAE 폴백**(봉인 위반) | ❌ **미적발** | 보고서가 원정의를 **주장**하고 이탈 기록도 없어 겉보기 정상. **artifact 층에서만** 잡힌다 — 채점기의 "컬럼 없으면 하드 실패(추측 금지)" 수정(a34c10d)이 그 층 |
| RC-03 | `a34c10d` `abs()` 버그 → HSPC per-gene 0.317 → **0.295 드리프트** | ❌ **미적발** | 임계 비교(lag > α)는 정의 드리프트에 둔감(0.295도 0.078보다 큼). **커밋된 기준값과의 정확 재현 대조**가 필요 |
| RC-05 | `clean_concordance_gate.md` §4 헤드라인의 **CRAK 의존** | ❌ **미적발** | method_set을 보는 scorer가 없음. arm별 신뢰 상태의 **기계가독 정본**이 BIOP01에 없다(산문뿐) |
| RC-06 | ~~env lock 미커밋~~ **[정정 2026-07-18]** stale `velo-*` 명명만 잔존 | ❌ **범위 밖** | 아래 (c) |

> ⚠️ **정정 (kkkim 실물 확인 2026-07-18):** RC-06의 "env lock 미커밋"은 **틀렸다.** lock.yml은
> **커밋돼 있다** — `64a93f8`(2026-07-11, kkkim 본인: "P0 env 동결: velo-mv/velo-tf/velo-torch/
> seqtools lock.yml 생성(재현성)"), 4개 env 전부 `env/*.lock.yml` 실재. 남은 실제 갭은
> **명명 stale(`velo-*`)뿐.** 이 stale 서술은 단일세포 스킬 조사 서브에이전트가 잡았고 kkkim이
> git show로 확인했다. → RC-06의 "미커밋" 근거는 소멸. 범위-밖 분류 자체는 유지(명명 문제는
> concordance 지표가 아니라 인프라 스모크 층).

**(c) 범위 밖으로 분류한 것 — 파이프라인/인프라 스모크.**
env 재현성 갭(RC-06)은 **진짜 재현성 실패지만 concordance 지표 실패가 아니다**. 하네스 리뷰 §1.2가
긋는 선을 그대로 따랐다: *"1~3은 eval이 아니라 **파이프라인 스모크 회귀**로 잡아야 한다. 이 둘을 한
바구니에 넣으면 scorer가 못 잡는 걸 잡는 척하게 된다."* → 이 층의 후보는 ClawBio 재현성 계약
(`commands.sh` + `environment.yml` + `checksums.sha256`, 리뷰 §4.1.2)이지 이 eval이 아니다.
**"ref/compact/reset diff"**(§2-a)도 착수되지 않아 범위 밖이다 — 실물이 생기면 별도 파일럿.

**(d) 파일럿 규모.** scorer 5개(사전등록 6예측 중 #6은 #2·#3의 파생) · 재현 축은 gse205117·macrophage·
HSPC 3개만 fixture화(외부 5축 전부 아님) · CI 훅 미구현(§5.5 GitHub Actions는 3단계).

## 6. 검증 실적 (2026-07-17 실제 실행 — `logs/` 에 원본)

> ⚠️ **아래 초록불의 의미를 오해하지 말 것.** `105/105`·`1.000`·`뮤턴트 전멸`은 **스코어러가
> 케이스에 제약되고 선언한 대로 동작하는가**를 잰 것이지 **결함 적발률이 아니다.**
> 실제 재현성 실패에 대한 적발은 **6건 중 2건**이고, 4건은 구조적 미적발이다(§5-b).
> 이 파일럿은 "재현성 회귀를 잡는다"가 아니라 **"두 종류를 잡고, 보고된 ρ 값은 신뢰한다"**(§5-a)이다.

| 검증 | 결과 | 무엇을 재는가 |
|---|---|---|
| `run_pilot.py` | **105/105** — 21 케이스 × 5 scorer | 스코어러 ↔ 사전등록 일치 |
| `mutation_check.py` | **25/25 뮤턴트 전멸** (always_pass / always_fail / always_caution / always_na / **invert_threshold**) × scorer 5 | 케이스가 스코어러를 진짜 제약하는가 |
| `run_real_artifacts.py` | **6/6** — 커밋된 `prereg_gse205117_scorecard`(6 PASS / 0 FAIL)를 정확히 재현 | 실물과의 일치 (**임계 적용만** — §5-a) |
| `inspect eval` | 6 task 전부 **accuracy 1.000** (135 samples) | 하네스 배선 |
| **coverage** | 실제 실패 6건 중 **2건 적발 / 4건 미적발** | ← **실제 결함 적발력. 이게 진짜 성적표.** |

**음성 대조군**(전부 FAIL만 있으면 무조건-FAIL 스코어러도 만점이므로 필수): 실물 3건 —
`control_real_01_gse205117`(실제 6 PASS) · `control_real_02_macrophage` · `control_real_03_hspc`.
`control_real_03_hspc`는 **N/A를 pass로 뭉개지 않는지**도 본다(HSPC는 cross-dataset의 기준축이라
cross leg·paired Δρ가 자기 자신에 대해선 산출되지 않는다).

### ❓ kkkim 확인 요청 — macrophage가 caution인 것이 맞나 (이건 내 판단이지 사전등록에서 유도된 게 아니다)

`control_real_02_macrophage`의 `prereg_adherence`는 **caution**이 나온다. scorecard가 스스로
*"macrophage(치환 정의): 0.280 vs 0.061"* 이라 밝히듯 HSPC 원정의(MoFlow `cs_lag_median`)가 아니라
**치환 자**로 쟀기 때문이다.

- **caution이 맞다는 근거:** 수치가 좋아 보여도 봉인된 정의로 잰 게 아니면 통과시키지 않는 것이 이
  스코어러의 존재 이유다 — RC-01이 실제로 그 사건("6 PASS"인데 이탈).
- **아닐 수도 있는 근거:** 봉인은 **GSE205117 사전등록**의 것이다. macrophage는 그 사전등록의 대상이
  아니고, 치환 정의를 쓴 것도 스스로 밝힌 **적법한 선택**이었을 수 있다. 그렇다면 "다른 데이터셋의
  적법한 치환 정의"에까지 GSE205117 봉인을 들이대는 셈이다.

→ **어느 쪽인지는 재현성 회귀의 owner(braveji)·Leader(kkkim)가 정할 정책 문제**다. CLAUDE.md가
채점 층의 자체 임계 설정을 금하므로 여기서 확정하지 않고 표면화만 했다. **caution을 유지할지, 데이터셋별
원정의를 따로 인정할지 확인 부탁드립니다.**

## 7. 다음 단계

1. **RC-03 대응 — canonical 수치 baseline.** 데이터셋별 정본 수치(HSPC per-gene lag **0.317** / α
   **0.078** 등)를 회귀 baseline으로 두고 **정확 재현 대조**(± 허용오차). 정의 드리프트를 잡는 유일한 길.
2. **RC-05 대응 — arm 신뢰 상태의 기계가독 정본.** "어느 arm이 buggy인가"(CRAK-Velo)가 현재 산문
   (`crakvelo_sign_check.md`)뿐이라 scorer가 읽을 수 없다. 정본이 생기면 method_set scorer 가능.
3. **CI 게이팅**(§5.5, 3단계) — PR마다 `run_pilot.py` + `mutation_check.py` + `run_real_artifacts.py`.
   전부 stdlib이라 GitHub Actions에서 env 없이 돈다.
4. **재현 축 확대** — 외부 5축(human_brain·E18·BMMC) fixture화.
5. **범용층 추출**(리뷰 §3) — BIOP02 `critic_pilot`과 이 파일럿이 공유하는 구조(`_case_meta.expected`
   계약 · mutation_check 패턴 · coverage 표)를 공통 하네스로. **scorer 내용은 프로젝트별 유지.**

## 8. 파일

| 파일 | 역할 |
|---|---|
| `scorers.py` | 결정론적 scorer 5종. **stdlib 전용.** 임계 출처를 주석으로 못박음 |
| `build_cases.py` | `cases/` 재생성. 실물 기반 + 결함 1개씩 주입 |
| `run_pilot.py` | 폴백 러너(stdlib) + coverage 표 |
| `mutation_check.py` | **뮤테이션 체크** — 5종 뮤턴트 × scorer 5. 없으면 이 파일럿은 미완성 |
| `run_real_artifacts.py` | 실물 scorecard CSV 채점 → 커밋된 6 PASS/0 FAIL 재현 |
| `reproducibility_pilot.py` | Inspect eval (6 task) |
| `cases/scorer_validation/` | 15건 — 실물 대조군 3 + 주입 결함/band 12 |
| `cases/regression_corpus/` | 6건 — **실제 BIOP01 재현성 실패**(git 근거). 지어낸 사례 없음 |
| `logs/` | 실행 로그 원본 |

## 9. BIOP02 파일럿과의 관계 (리뷰 §3의 층 분할)

| 층 | 처리 |
|---|---|
| eval 하네스 구조(Inspect) · 실패 코퍼스 스키마 | ✅ **재사용** — `critic_pilot`과 같은 구조: `_case_meta.expected` 계약, scorer registry, 폴백 러너, mutation_check, coverage 표, 실물 대조군 |
| scorer의 **항목·임계값** | ❌ **프로젝트별** — BIOP02 = Critic 7-point(DRP 프레이밍·baseline margin·claim level) / **BIOP01 = 재현 일치도**(α ρ·lag ρ·Δρ·cross·per-gene 격차). **BIOP02 scorer를 복사하지 않았다** — 공유 코드 0줄, 도메인 임계는 전부 BIOP01 사전등록 인용 |

**공통 규율(양쪽 CLAUDE.md):** 채점 층은 **자기 임계를 스스로 정하지 않는다**. BIOP02가
`checklist_v1.md`를 인용하듯, 이 파일럿은 `PREREGISTRATION_gse205117.md` + `p3_prereg_gse205117.py`를
인용한다. 사후 임계 조정은 git에 남는다.

---

## kkkim 판정 — `control_real_02_macrophage`의 `prereg_adherence: caution` (2026-07-17)

**판정: caution 유지. 단 프레이밍을 정정한다.**

파일럿 저자가 *"제 판단이지 사전등록에서 유도된 게 아니다"* 라며 확정을 보류하고 표면화만 한 것은
**옳은 처신**이다(CLAUDE.md: 채점 층의 자체 임계 설정 금지 = anti-self-reference).

그러나 근거를 다시 보면 **이건 자체 임계 설정이 아니다.** caution의 실제 근거는
*"GSE205117 봉인을 macrophage에 들이댄 것"* 이 아니라 **원 scorecard 스스로가
`per_gene_disagree`를 "치환 정의"로 쟀다고 명기한 것**이다(`concordance_macrophage.md` +
`FINDINGS.md` §7-D). 즉 채점기는 **임계를 발명한 게 아니라 문서화된 정의 이탈을 보고**하고 있다.
그건 Critic 층이 마땅히 할 일이다. → **caution 유지.**

**다만 이름·메시지가 오해를 만든다.** `prereg_adherence`라는 이름은 "GSE205117 사전등록이
macrophage를 규율한다"고 읽히는데, **그건 사실이 아니다**(그 봉인은 GSE205117 전용).
정확한 주장은 다음이며, evidence 문구를 이렇게 좁힌다:

> per-gene 격차가 **HSPC 봉인 원정의(`cs_lag_median`)가 아니라 치환 정의**로 측정됨
> → **예측5와 직접 비교 불가**(수치 0.280 > 0.061이 좋아 보여도 같은 자로 잰 값이 아니다).
> 이는 **비교가능성 caution**이지 **사전등록 위반이 아니다.**

**데이터셋별 원정의를 따로 인정할 것인가** — 인정하려면 **그 데이터셋의 사전등록을 따로 봉인**해야 한다.
사후에 "이것도 적법한 정의"라고 추가하는 건 사전등록의 의미를 없앤다. 지금은 **caution으로 남기고
macrophage를 헤드라인 근거로 쓰지 않는다.**
