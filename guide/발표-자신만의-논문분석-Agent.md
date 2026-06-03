# 자신만의 논문 분석 Agent — 중요 요소와 Skill 반영

> 발표자: 지용기 (하네스 담당) · 과제: BIOP01-7 *"자신만의 논문 분석 Agent 만들기"* 8번 — 공유용
> 대상 논문: **MultiVelo** (chromatin–RNA joint velocity) · 도구: `Skills/paper-analysis.md`
> 슬라이드 아웃라인 + 발표 노트 겸용. 각 `##` 가 슬라이드 1장 기준.

---

## 0. 한 줄 요약 (오프닝)

> "논문 분석 Agent는 **요약기**가 아니라 **재현 가능한 비판적 리뷰어**여야 한다.
> 그래서 나는 *주장과 근거를 분리*하고, *우리 프로젝트(activation/shutdown lag) 관점*을 강제하고,
> *세션을 초기화해도 같은 결론이 나오는지*를 설계 기준으로 삼았다."

발표에서 보여줄 것 3가지:
1. 논문 볼 때 내가 **중요하게 보는 5가지 요소**
2. 그 각각을 Skill의 **어떤 구체적 장치**로 박았는지
3. `/compact`·`/clear`·`/reset` 후에도 그 관점이 **재현되는지 실제로 검증한 결과**

---

## 1. 내가 논문 분석에서 중요하게 보는 5가지 요소 (the "why")

평소 논문을 읽을 때 "요약"보다 아래 5가지에서 판단이 갈린다고 봤다.

| # | 중요 요소 | 왜 중요한가 / 흔한 실패 |
|---|---|---|
| **A** | **주장 ≠ 근거 ≠ 내 판단** | LLM 요약은 저자 결론을 그대로 사실로 베껴 쓴다. 진짜 리뷰는 *"저자 주장 / 제시 근거 / 내 평가 / 근거 강도"* 를 분리해야 한다. |
| **B** | **재현 가능성 (논문의 재현성 + 분석의 재현성)** | ① 논문이 데이터·코드·seed·버전을 공개했나. ② **내 분석 자체가** 세션 초기화 후에도 같게 나오나. 두 번째를 보는 사람은 드물다. |
| **C** | **방법론적 함정 (도메인 특화)** | epigenomics/single-cell에선 *pseudotime을 실제 시간으로 과해석*, confound(batch·cell cycle·depth·donor) 미통제, multiple testing 누락이 결론을 통째로 뒤집는다. |
| **D** | **우리 프로젝트와의 연결** | "흥미롭다"로 끝내면 안 됨. *activation lag / shutdown lag* 정량화와 3-step framework(lag 정량화 → baseline feature 예측 → perturbation 검증)에 **매핑되는지**가 채택 기준. |
| **E** | **신규성의 정직한 크기** | "새롭다"의 대부분은 incremental. 무엇이 genuinely new이고 무엇이 기존(MultiVelo/MultiVeloVAE/MoFlow) 대비 trade-off인지 구분. |

발표 포인트: **A·B가 "분석 태도", C·D가 "우리 도메인 렌즈", E가 "균형"** — 이 5개를 Skill에 그대로 박았다.

---

## 2. 각 요소를 Skill에 어떻게 박았나 (the "how")

`Skills/paper-analysis.md`의 실제 장치와 1:1 매핑.

### A. 주장 ≠ 근거 ≠ 판단 → **Step 6 "Key Results"의 강제 4분할**
각 핵심 결과를 다음 4칸으로 쓰게 강제:
- **Authors' claim** / **Evidence presented**(metric·figure·table) / **My assessment** / **근거 강도 = Strong / Moderate / Weak / Unsupported**
- + Core principle 1–2: *"Ground every claim in the paper / Separate what the paper states from your interpretation."*
- 효과: 결론 복붙이 구조적으로 불가능해짐.

### B. 재현 가능성 → **Step 11 + 고정 출력 포맷**
- **Step 11 Reproducibility Assessment**: data·code·params·seed·software version·figure-method 일치 체크 → **High / Moderate / Low** 등급.
- **고정 13-섹션 출력 포맷**: 출력 구조를 못 박아 두면 세션이 바뀌어도 *같은 틀*이 재생성됨 → 분석 자체의 재현성 확보 장치.

### C. 방법론적 함정 → **"Domain-specific checks" 전용 체크리스트 내장**
Skill 하단에 epigenomics/bioinformatics 전용 질문을 박아 매 분석마다 강제 점검:
- pseudotime을 real time으로 과해석하나?
- confound(batch, cell cycle, sequencing depth, donor) 통제하나?
- chromatin↔transcription **순서를 직접** 보였나, 간접 추론인가?
- paired multiome인가, cross-modality 통합인가?
- gene/peak 단위 **multiple testing correction** 했나?
- uncertainty·variance 보고하나? baseline은 공정·경쟁력 있나?

### D. 프로젝트 연결 → **Step 3·10에 "Project connection" + Step 13 "Project Utility Assessment"**
- Step 3·10에 *Project connection* 블록을 박아 매번 activation/shutdown lag·3-step framework와의 관계를 서술하게 함.
- **Step 13 = 최종 채택 등급**: **Directly usable / Adaptable with modification / Conceptually informative only / Not useful** 중 택1 + "무엇이 쓸모 있고, 3-step의 어디에 매핑되고, 무엇을 더 보태야 하는지".

### E. 신규성 균형 → **Step 10 "Comparison to Prior Work"**
- *genuinely new vs incremental vs trade-off* 를 분리하고, MultiVelo/MultiVeloVAE/MoFlow 간 차이를 명시하도록 요구.

### (공통) 정직성 → **Behavior rules**
paywall 시 WebFetch/WebSearch fallback, 부분 접근이면 *어느 섹션을 못 봤는지* 명시, abstract만 봤으면 full review인 척 금지.

---

## 3. "재현 가능한 분석"이 핵심 설계 철학 (한 슬라이드 강조)

과제 6·7번(파일 삭제 → `/compact` → 재분석, → `/clear`·`/reset` → 재분석)이 곧 Skill의 설계 목표였다.

- **요약기**: 매번 다른 문장, 결론도 흔들림 → 신뢰 불가
- **이 Skill**: 고정 13-섹션 + 강제 분할 + 등급 라벨 → *세션 초기화에 강건한* 분석 프레임

> "Skill의 목적은 멋진 요약이 아니라, **누가 언제 돌려도 같은 비판 지점이 나오는 disciplined analysis**."

---

## 4. 검증 결과 — `/compact`·`/clear`·`/reset` 재현성 (과제 6·7)

### 실험 설계
같은 MultiVelo 논문을 3조건에서 분석하고 5개 기준점을 비교.
- `multivelo-analysis.ref.md` (기준)
- `multivelo-analysis-compact.md` (`/compact` 후)
- `multivelo-analysis-reset.md` (`/clear`·`/reset` 후)

### 결과 표

| 기준점 | ref | compact | reset | 재현 판정 |
|---|---|---|---|:--:|
| Gene-specific lag 정량화 | 신중 | 신중 | 더 낙관적(단 caveat 유지) | **O** |
| chromatin → transcription 순서 | 명시 | 명시 | 명시 | **O** |
| pseudotime 과해석 경고 | 강함 | 강함 | 존재하나 약함 | **O** |
| **Project Utility Assessment** | Adaptable | Adaptable | **Directly usable** | **△** |
| Reproducibility Assessment | Moderate | Moderate | Moderate | **O** |

### 핵심 발견
- ✅ **재현된 것**: 핵심 분석 프레임 전부 — chromatin-RNA joint dynamics 규정, Model 1/Model 2 중심성, chromatin→transcription 순서, pseudotime 한계 인식, 재현성 등급(Moderate).
- ⚠️ **흔들린 것 하나**: 최종 **Project Utility 라벨**이 reset 후 `Adaptable with modification` → `Directly usable` 로 더 낙관적으로 이동.
- 즉, **사실·구조·방법 판단은 안정**적이었고, **주관적 최종 "실용성 등급"의 엄격도만 드리프트**.

---

## 5. 교훈 & 다음 단계 (클로징)

**교훈**
1. 구조를 못 박으면(고정 포맷·강제 분할) LLM 분석도 세션 초기화에 **상당히 강건**하다.
2. 그러나 **단일 라벨로 압축되는 주관적 최종 판단**은 컨텍스트가 사라지면 톤이 흔들린다.

**개선안 (Skill v2)**
- Step 13 등급에 **명시적 rubric** 부여: 각 라벨의 진입 조건을 정의(예: *"continuous lag 변수 직접 출력 + real-time 검증 존재 → Directly usable"*) → 엄격도 드리프트 차단.
- 등급과 함께 **"왜 그 등급인지 1줄 + 근거 강도"** 를 항상 동반시켜 낙관/비관 톤을 근거에 고정.
- (하네스 역할 연계) ref/compact/reset 3종 자동 생성 + diff 비교를 **재현성 회귀 테스트**로 하네스에 넣는 것을 검토.

**한 줄 마무리**
> "Skill만으로 프로젝트 맞춤 비판적 분석 프레임이 안정적으로 재현됨을 확인했다.
> 남은 과제는 *최종 판단의 엄격도*까지 rubric으로 고정하는 것."

---

### 부록 — 근거 파일
- Skill: `Skills/paper-analysis.md` (13-step, domain-specific checks)
- 분석 3종: `analysis/multivelo-analysis.{ref,compact,reset}.md`
- 비교 메모: `analysis/reproducibility-check.md`
- (branch: `braveji-paper-agent`)
