# 원고 간결화 계획 — draft_v2.md (2026-07-26)

`manuscript-condenser` 명세의 1단계(진단)를 실제 원고에 적용한 결과다. **아직 아무것도 고치지
않았다.** 이 문서는 어디를 얼마나 줄일지에 대한 계획이며, 승인 후 강등 → 병합 → 압축 순으로
실행한다.

> **출처.** 패턴 진단은 codex CLI(ChatGPT 계열)에 Results/Discussion/Conclusions 구간
> 7,654단어를 인라인으로 넘겨 받은 것이고, 각 지적은 원고에서 직접 대조해 확인했다(아래
> "확인" 열). §2.7은 이 대조 과정에서 추가로 나온 것이다. 다른 모델 계열을 쓴 이유는
> `.claude/agents/venue-reviewer.md`의 격리 규칙과 같다 — 같은 계열이 자기 글을 검수하면
> 모의 검수다.

## 1. 실측 기준선

전체 `draft_v2.md` 13,313단어.

| 섹션 | 단어 |
|---|---|
| Abstract | 422 |
| Background | 826 |
| **Results** | **5,857** |
| Discussion | 1,607 |
| Conclusions | 190 |
| Methods | 1,767 |

Results 소절별 (200단어 초과분, 괄호는 산문 속 ρ·p·CI·n 등장 횟수):

| 단어 | 수치 | 소절 |
|---|---|---|
| **2,147** | 17 | Table 2. Velocity-output reliability decision map |
| **1,632** | 1 | The cell×gene velocity matrix does not reproduce across methods either |
| 776 | 15 | Only the transcription rate α … reproduces across methods |
| 626 | 7 | The dissociation is a property of the objective function |
| 597 | 9 | The fitted transcription rate α, but not γ, recovers an external rate |
| 502 | 19 | The α-robust, lag-fragile ordering replicates across five external systems |
| 375 | 9 | Table 1. Cross-method reproducibility |
| 300 | 8 | Chromatin does not drive the lag |
| 238 | 2 | The reliability map |
| 232 | 3 | A synthetic positive control |
| 229 | 5 | The lag is unpredictable from baseline features |

재실측:

```bash
cd pipeline/hspc-velocity-benchmark/manuscript
python3 - <<'EOF'
import re, io
s = io.open("draft_v2.md", encoding="utf-8").read()
for p in re.split(r"\n(?=### )", s)[1:]:
    w = len(p.split())
    if w > 200:
        print("%5d w / %2d nums  %s" % (w, len(re.findall(r"[ρp]=|95% CI|n=", p)), p.split("\n")[0][4:70]))
EOF
```

## 2. 장황 패턴

감축량이 큰 순서다. "확인" 열은 원고에서 실제로 대조한 결과다.

### 2.1 수정 이력·감사 로그의 본문화 — 800~1,200단어
- 위치: `The cell×gene velocity matrix …` L117, L119
- 확인: **사실.** "Our first version of this second comparison was not like-for-like, and we correct
  it here …", "Against the archived fits the only departure is a single gene (*LRIG1*): a 4×10⁻¹⁶
  rounding difference …" 방법 수정 내역과 rerun null 상세가 Results 본문에 그대로 들어 있다.
- 왜: 신뢰성을 높이는 기록이지만 Results가 논증이 아니라 로그처럼 읽힌다.
- 처방: **강등**. 본문에는 결론을 바꾸는 문장만 남기고 상세는 Supplementary audit note로.
  단 "we therefore withdraw our earlier statement…"는 §3에 따라 본문 유지.

### 2.2 산문 속 수치 덤핑 — 700~1,000단어
- 위치: `The α-robust, lag-fragile ordering …`(502단어에 수치 19회), `Only the transcription
  rate α …`(776단어에 15회), `The fitted transcription rate α …`
- 확인: **사실이고 측정된다.** 502단어 소절에 ρ·p·CI·n이 19번 나온다. Table 1·2와 중복이다.
- 왜: 독자가 확인할 방향은 하나인데 모든 값을 산문에 푼다.
- 처방: **압축**. 본문은 범위·패턴·예외만. 개별 수치는 Table 1/2 또는 Supplementary Table로.

### 2.3 방어적 caveat 과적재 — 600~900단어
- 위치: `The α-robust …`의 "Caveats (Table 1 footnotes). (i) The…", Discussion "Three further
  limits are load-bearing…", `The cell×gene velocity matrix …`의 "Three limits keep the
  statement small…"
- 확인: **사실.** 번호식 한계 열거가 세 군데에서 반복된다.
- 처방: **강등**. 주장 해석을 바꾸는 caveat만 본문에, 나머지는 표 footnote·Supplementary·Methods로.

### 2.4 같은 판정의 3회 반복 — 500~800단어
- 위치: L127(Results 말미 reliability map), L169(Discussion 첫 문단), L183(Conclusions)
- 확인: **사실이고 수치까지 겹친다.** 세 곳 모두 ρ=0.88, +0.163, |ρ|≤0.08, +0.24~+0.29를
  다시 적는다. 판정문("α만 신뢰, lag·γ 불신뢰")이 거의 같은 문장으로 세 번 나온다.
- 처방: **병합**. Results 말미는 Table 2 참조 + 4~5문장, Discussion 첫 문단은 해석·한계 중심,
  Conclusions는 수치 최소화.

### 2.5 선행연구 positioning의 Results 침투 — 300~600단어
- 위치: `Chromatin does not drive the lag …`의 "We promote this negative control to a main…",
  `The dissociation is a property …`, Discussion의 "Positioning against prior work"
- 확인: **사실.** novelty·우선권 서술이 Results와 Discussion 양쪽에 있다.
- 처방: **강등**. Results는 "Fig. 2/5 shows…"만, 선행연구 대비는 Discussion 한 절로.

### 2.6 부정 주장 과잉 한정 — 300~500단어
- 위치: `Chromatin does not drive the lag …`, Discussion "It is a statement about the methods
  and…", "Read together, these results bound our negative…"
- 확인: **사실.** "크로마틴 생물학을 부정하는 게 아니다"라는 안전장치가 여러 절에서 다른 말로
  반복된다.
- 처방: **병합**. Discussion에 한 번만. Results에서는 "correlational, not causal" 정도의 짧은 태그.

### 2.7 소절 하나가 Results의 28%를 쓴다 (대조 중 추가 발견)
- `The cell×gene velocity matrix does not reproduce across methods either` 혼자 **1,632단어**로
  Results 5,857단어의 28%다. 그런데 산문 속 수치는 1회뿐이다 — 즉 **수치가 아니라 서술이
  분량을 쓰고 있다.** 2.1·2.3이 이 소절에 겹쳐 있다.
- 이 소절 하나를 처리하면 위 여섯 패턴의 감축량 상당 부분이 여기서 나온다. **1순위.**
- 참고로 `Table 2. Velocity-output reliability decision map`은 2,147단어인데 표 소절이
  이 분량이면 표 주변 산문이 표를 다시 설명하고 있다는 뜻이다. 2순위.

## 3. 절대 줄이면 안 되는 자리

분량이 많아 보이지만 근거·한정어·불리한 사실을 지고 있다. 여기를 건드리면 주장이 세진다.

| 위치 | 원문 실마리 | 이유 |
|---|---|---|
| Only the transcription rate α … | "MultiVelo's apparent 100% chromatin-leads is…" | 구조적 sign bias 설명. 빼면 lag sign 비판이 과도해진다 |
| The fitted transcription rate α … | "The measured synthesis rate carries steady-state transcript…" | α 외부검증의 abundance confound를 진다 |
| The dissociation is a property … | "This is a relative (practical) non-identifiability…" | likelihood 주장이 "완전 비식별성"으로 과장되는 걸 막는다 |
| The cell×gene velocity matrix … | "We therefore withdraw our earlier statement that chromatin…" | 자기에게 불리한 정정. 투명성의 핵심 (REVIEW-GB MINOR-5) |
| Discussion | "we did not audit the low-dimensional embedding…" | velocity 전체를 부정한다는 오독을 막는 scope 제한 |

## 4. 이 원고 전용 체크리스트

1. Results에서 이미 판정한 숫자를 Discussion·Conclusions에서 다시 열거하지 않는다. 방향과 해석만.
2. 산문에 ρ·CI·p·n이 세 개 이상 연속되면 표로 보내고 본문에는 패턴만 남긴다.
3. caveat가 주장을 바꾸지 않으면 footnote 또는 Supplementary Note로 강등한다.
4. "not causal", "not biology", "not trajectory inference" 방어문은 논점당 한 번만 둔다.
5. correction history와 rerun audit는 결론을 바꾸는 한 문장만 남기고 상세는 보조자료로.
6. 선행연구 대비 문장은 Results에서 빼고 `Positioning against prior work` 한 절로 모은다.
7. 소절 끝 "therefore" 문장이 다음 소절이나 Discussion에서 반복되면 하나만 남긴다.

## 5. 실행 순서

`manuscript-condenser` 규칙대로 강등 → 병합 → 압축 순이며, 삭제는 쓰지 않는다.

| 단계 | 대상 | 예상 |
|---|---|---|
| 0 | `CLAIM-EVIDENCE-MAP-<date>.md` 작성 (감축 전 필수) | — |
| 1 | 2.1 강등 — 감사 로그를 Supplementary audit note로 | −800~1,200 |
| 2 | 2.3 강등 — caveat를 footnote·Supplementary로 | −600~900 |
| 3 | 2.5 강등 — positioning을 Discussion 한 절로 | −300~600 |
| 4 | 2.4 병합 — 판정 3회를 1회 + 참조로 | −500~800 |
| 5 | 2.6 병합 — 방어문 논점당 1회 | −300~500 |
| 6 | 2.2 압축 — 산문 수치를 표로 | −700~1,000 |

합계 추정 −3,200~5,000단어. 7,654 → 2,700~4,500. **이 추정은 codex의 것이고 실측이 아니다.**
1단계를 실제로 해 본 뒤 나머지 추정을 다시 잡는다.

각 단계 끝에 반드시:
- 결정론 재계산 게이트 3종 (`p3_concordance`, `p3_crossdataset_concordance`, `p3_scrambled_null`) diff 0
- `CLAIM-EVIDENCE-MAP`의 한정어 보존 열 전부 O
- EN/KO 파리티 (heading 개수·수치 전항·참고문헌 개수)
- `CONDENSE-LEDGER-<date>.md` 갱신

## 6. 미결

- **Abstract(422단어)는 이 계획에 없다.** 본문을 줄인 뒤 마지막에, 사람 확인을 받고 따로 한다.
- **Methods(1,767단어)도 제외**했다. 투고 규정상 별도 취급인 경우가 많아 목표 분량이 정해진
  뒤에 판단한다.
- 목표 분량이 아직 없다. 투고처의 실제 제한을 확인한 뒤 위 추정과 맞춰야 한다.
