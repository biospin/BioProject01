# BIOP01-81 항목3 — C1 카운슬 Stage 3 최종 종합 판정 (2026-08-21)

COUNCIL-MINIMAL(2모델 최소 운용본)의 마지막 단계. 5개 leg가 모두 채워졌고, 최고토큰
오케스트레이터(Claude Opus)가 근거의 질로 최종 판정한다. `council_synthesize.py`는 집계일 뿐
판정이 아니다(다수결 금지 — 종합기는 정확 텍스트로만 클러스터링해 교차모델 합의를 못 묶는다).

## 대상 주장 C1 (CLAIMS.yaml, primary_negative)
"chromatin→transcription lag은 gene 수준에서 method-robust한 양이 아니다 (크기·방향 모두
method 간 일치도가 낮다)."

## 5개 leg 요약

| leg | 모델 | 세션 | C1 판정 | 최고 강도 critique | Valid-and-Fatal |
|---|---|---|---|---|---|
| S1 (add-on) | Gemini 3.1 Pro | S1-gemini-C1 | **Unsupported**(시도) | Valid-and-Fatal ×2 | 2 (아래서 전부 기각) |
| S1 (minimal) | GPT (codex gpt-5.5) | S1-gpt-C1 | **Plausible** | Valid-but-Fixable | 0 |
| S1 (minimal) | Claude Opus 4.8 | S1-claude-C1 | **Plausible** | Valid-but-Fixable | 0 |
| S2 교차 | Claude→GPT | S2-claude-on-gpt-C1 | GPT에 동의 | Partially-Valid | 0 |
| S2 교차 | GPT→Claude | S2-gpt-on-claude-C1 | Claude에 동의 | Partially-Valid | 0 |

Stage 3 종합은 최고토큰 Claude Opus 오케스트레이터(본 문서).

## Fatal 후보 2건 — 둘 다 Gemini발, 전부 기각

종합기가 표면화한 살아남은 Valid-and-Fatal 2건은 **모두 Gemini leg** 것이고, jamie의 Gemini
오케스트레이터 판정(`BIOP01-81_C1_orchestrator_review.md`)에서 이미 기각됐다:
1. **0/598 CRAK 의존 = Fatal** → 실제로는 Valid-but-**Fixable**. C1은 CRAK-비의존 magnitude
   concordance로 생존하며 이미 `clean_concordance_gate §4` 강등 + CLAIMS limitation①이 커버.
   GPT·Claude 두 독립 leg도 같은 지적을 **Fixable**로 판정(Gemini만 Fatal로 과대).
2. **§1.5 전역 방향편향 부재 은폐 = Fatal** → 범주오류. §1.5의 전역 편향 부재는 C1(gene별
   per-gene 일치도)과 다른 층위라 은폐가 아니다. jamie 판정에서 기각.

**즉 살아남은 Fatal은 실질 0건.** GPT·Claude 두 minimal leg와 두 교차 재비판 중
Valid-and-Fatal은 하나도 없다.

## C1 판정: 4개 적대 leg를 모두 통과 (유지)

- **magnitude leg(결정적)**: clean 3-way 쌍별 Spearman 모두 |ρ|≤0.083, n=537~636로 검정력
  충분. GPT·Claude 독립 leg 모두 이를 load-bearing 근거로 C1을 Plausible 유지.
- **sign leg(약함·규약견고)**: clean 2-method 부호-FDR degenerate(min p_perm=0.499), 0/598은
  CRAK 의존이라 강등. sign-agreement 54.6%/48% 둘 다 chance 근방이라 결론은 규약에 견고하나
  magnitude만큼 강하게 못 민다.
- 크기 leg이 결정적이고 방향 leg이 power-bounded·규약의존이라 두 leg 모두 **Proven이 아닌
  Plausible**로 독립 수렴. Gemini의 Unsupported 시도(rate-proxy ρ=+0.124를 강건성으로 오독)는
  통계오류로 기각됐다.

## 신규·비차단 쟁점 3가지 (원고 강화용, claim 미변경)

두 minimal leg + 두 교차 재비판이 새로 표면화했으나 **C1을 뒤집지 못한** 것들. 전부 비차단.

1. **Scope — 전역(global) fit 근거** (GPT critique-3, Claude-on-GPT가 원자료로 검증·정당).
   현재 결과는 "gene-level 전역 fitting 조건의 cross-method 비robust"를 강하게 시사하나,
   "모든 lineage별 맥락에서 method-robust하지 않다"의 완전 일반성엔 per-lineage cross-method
   fit이 더 필요. concordance.md §4가 스스로 이 한계를 밝힌다. **권고**: 한계 서술에 한 줄
   caveat(전역 fit 기반·per-lineage cross-method는 향후 과제; within-method per-lineage refit
   median ρ=0.349도 약한 일치).

2. **Within-method 신뢰도 미확립 → attenuation 미분리** (Claude critique-1, GPT-on-Claude 확인).
   낮은 cross-method ρ가 '진짜 비robust'인지 '각 method 내부 추정잡음 희석'인지 구분 못 함.
   within-method test-retest(bootstrap lag-sign stability) 미확립. concordance.md §4가 자인.
   **가장 강한 fixable 지적.** 향후 bootstrap 안정성 검정이 정공법이나 C1을 뒤집진 않는다.

3. **MultiVelo 구조부호 confound** (Claude critique-5 → GPT-on-Claude가 Partially-Valid로 하향).
   clean 3쌍 중 multivelo 포함 2쌍은 MultiVelo lag 100% 양수라 '크기 ordering vs 부호-우선
   ordering' 비교. 단 GPT가 지적하듯 **§3.6이 이미 apples-to-apples 재비교**(multivelo×
   multivelovae를 통일 rate-proxy로: Spearman **+0.124, p=0.0039, sign-agr 49.8%**)를 제공해
   confound가 MultiVelo 근거를 전부 무효화하진 않는다. **권고**: 원고 방어 시 §3.6의 +0.124
   재비교를 명시 인용해 선제 대응(이 값이 clean |ρ|≤0.08보다 커서 CLAIMS 헤드라인 |ρ|≤0.08과
   가벼운 긴장 — Claude-on-GPT meta-c4도 지적).

## 종합 판정

**C1은 카운슬 최소본(5 leg)을 통과한다.**
- Fatal 실질 0건(Gemini발 2건은 오케스트레이터가 이미 기각).
- 두 독립 minimal leg(GPT·Claude) 모두 반박 없이 Plausible 수렴.
- 두 교차 재비판(Stage 2) 모두 상대 leg에 동의, 새 Fatal 없음. GPT-on-Claude가 Claude
  critique-5를 한 단계 하향(§3.6 존재)한 것이 유일한 실질 조정이고, 이는 오히려 C1을 강화한다.
- claim-defensibility 영향: **없음.** 원고 claim 문구·헤드라인 수치 불변.

## 남은 일 (원고 편집 — 8/27 회의 / manuscript-writer 몫, 비차단)
1. 한계 서술 1줄 caveat(scope: 전역 fit). — 신규 쟁점 1
2. (선택) 향후 과제에 within-method bootstrap 안정성 검정 명기. — 신규 쟁점 2
3. (선택) 방어용으로 §3.6 rate-proxy 재비교(+0.124)를 본문/한계에 명시 인용. — 신규 쟁점 3
4. (운용) `council_schema.json`의 `target` enum이 `{original,claude-critique,gpt-critique,
   gemini-critique}`라 교차 leg의 `S1-*-C1` target값과 불일치(종합기는 키 존재만 검사해 통과).
   차기 카운슬 전 schema enum에 교차대상 표기 규약을 추가하면 정합.

세 원고 편집은 전부 claim을 바꾸지 않는 강화용이고 GB 투고 blocker가 아니다.
