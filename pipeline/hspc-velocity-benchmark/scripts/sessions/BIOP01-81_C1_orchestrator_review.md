# BIOP01-81 항목3 — C1 카운슬 오케스트레이터 판정 (2026-08-20)

`council_synthesize.py` 산출(`S1-gemini-C1.json` 1세션)에 대한 최종 판정. 종합기는 집계일 뿐 판정이 아니므로,
`COUNCIL-MINIMAL.md`/comment 11779가 지정한 대로 최고토큰 오케스트레이터(Claude)가 근거의 질로 직접 판정한다.

## 실행 정보

- 모델: **Gemini 3.1 Pro (Extended thinking)**
- 입력 형태: **텍스트 붙여넣기**(파일 업로드 아님) — `concordance.md` 전문 + `CLAIMS.yaml` C1 블록 원문을
  프롬프트 본문에 markdown 코드블록으로 그대로 inline 포함. `clean_concordance_gate.md` §0은 구조적 논증만
  발췌하고 스테일 수치(48.1%, 정정 전 값)는 제외해 전달.

## 진행 상태 — 정직 명시

**Claude+GPT leg는 실행되지 않았다.** `sessions/`에 있는 건 Gemini S1(원본 비판) 세션 1개뿐이다. 이건 jamie가
맡은 Gemini leg만 완료된 것이지, `COUNCIL-MINIMAL.md`가 정의한 5세션 최소 운용본(Claude+GPT 4세션 + 종합)
전체가 완료된 게 아니다. 아래는 **Gemini 단독 적대적 검토**에 대한 판정이며, "카운슬 통과"로 승격하려면
Claude/GPT leg가 별도로 필요하다.

## claim 판정 (gemini: Unsupported) — 기각

Gemini는 §3.6의 rate-proxy lag(1/α_c−1/α) 통일 비교(Spearman +0.124, p=0.0039)를 "|rho|<=0.08 기준을
초과하는 강건성"이라고 읽고 C1을 Unsupported로 판정했다. **이는 통계적 유의성과 효과 크기를 혼동한 것이다.**
p=0.0039는 표본이 크면(n=538) 약한 상관도 유의해진다는 뜻일 뿐, ρ=0.124 자체는 α의 ρ=0.882(같은 §3.6)와
비교하면 여전히 매우 약한 상관이다. "0.08보다 크다"는 산술적으로 맞지만, 이 정도 크기를 "강건성 도출"로
부르는 건 과대해석이다. §3.6의 결론 문장("α는 강건하나 lag을 결정하는 α_c가 method-민감 → lag 불일치의
근원")도 정확히 반대로 읽는다 — 원문은 이 결과를 C1을 반박하는 근거가 아니라 **lag 불일치의 원인 규명**으로
쓰고 있다. **판정: claim 반박 실패, C1 유지.**

## critique-1 (gemini: Valid-and-Fatal, 0/598 CRAK 의존성) — 하향: Valid-but-Fixable (이미 조치됨)

CRAK-Velo를 포함해야만 "0/598 agreement-set"이 성립한다는 지적 자체는 정확하고, 근거 문서
(`clean_concordance_gate.md` §0)가 이미 자체적으로 밝힌 내용과 같다. 그러나 이건 C1의 **부호-일치
agreement-set 통계 하나**에 대한 결함이지 C1 전체의 결함이 아니다. C1의 주 근거인 **크기(magnitude)
concordance(|rho|<=0.08, 깨끗한 3-way)는 CRAK와 무관**하며 이 비판의 영향을 받지 않는다. 게다가 팀은
이미 이 문제를 인지해 0/598을 헤드라인에서 빼고 CRAK 민감도 분석(보조)으로 강등해뒀다
(`clean_concordance_gate.md` §4). **살아있는 결함이 아니라 이미 반영된 caveat다.**
`CLAIMS.yaml`의 limitation ①이 정확히 이 내용을 담고 있으므로 원고는 이미 정직하게 서술 중이다.
**판정: C1을 무효화하지 않음. Fatal 강등, 기존 caveat 서술 유지로 충분.**

## critique-2 (gemini: Partially-Valid, lag=0 제외 규약) — 유지: Partially-Valid

`CLAIMS.yaml`의 limitation ②가 이미 명시한 내용과 같은 지점을 짚었다(제외 시 54.6%, 미제외 시 48%).
"48%는 우연조차 안 된다"는 수사는 과장이다 — 48%도 50% chance와 유의하게 다르지 않을 가능성이 높다(두
값 모두 chance 근방). 하지만 "결과가 제외 규약 선택에 민감하다"는 지적 자체는 타당하고, 이미 원고
limitation에 명시돼 있다. **판정: 신규 결함 아님, 기존 caveat로 충분히 커버됨.**

## critique-3 (gemini: Valid-and-Fatal, 전역 방향편향 부재 은폐) — 기각: Incorrect (범주 오류)

§1.5의 "전역적으로 chromatin이 transcription보다 먼저 움직이는 경향이 있는가"(중앙값≈0, ~50/50, 전역
편향 없음)와 C1의 실제 주장인 "유전자별로 방법론 간 lag 방향이 일치하는가"(sign-agreement 42~55%)는
**서로 다른 질문이다.** 전역 편향이 없다는 사실은 유전자별 불일치를 반박하지 않는다 — 오히려 각 유전자가
서로 다른(때로는 반대) 방향의 실제 신호를 가지면서 평균은 0 근방으로 상쇄될 수 있고, 이건 원자료의 낮은
sign-agreement(42.3~54.6%, 우연 근방)와 정확히 양립한다. "은폐"라는 표현은 근거가 없다 — 원본이 §1.5와
§3.5를 나란히 실어 두 질문을 이미 분리해서 보고하고 있다(concordance.md §1.5 "rank-corr와 sign-agreement는
분리 보고(병합 금지)"). **판정: 비판 자체가 원자료 오독, C1에 영향 없음.**

## 종합 판정

**C1은 이 Gemini 단독 검토를 통과한다.** 살아남은 실질적 caveat는 없음(둘 다 원고가 이미 명시한 기존
limitation과 중복). Gemini가 제기한 3건의 비판 중 논리적으로 새로 살아남는 것은 없다 — 하나는 이미 조치된
내용의 재확인, 하나는 원자료 오독. claim 반박 시도(rate-proxy 재해석)도 통계 오류로 기각.

**남은 일**: 이건 Gemini 1개 세션의 결과다. `COUNCIL-MINIMAL.md`가 정의한 최소 운용본(Claude+GPT 4세션)은
여전히 미실행 — 카운슬 "통과"로 원고에 반영하려면 최소한 GPT leg(codex, BIOP01-45 경로로 실행 가능,
kkkim/이건규 소관)가 더 필요하다. 이 문서는 jamie가 맡은 Gemini leg의 완결 보고이자 그 결과에 대한
오케스트레이터 판정이며, 전체 카운슬의 최종 승인이 아니다.
