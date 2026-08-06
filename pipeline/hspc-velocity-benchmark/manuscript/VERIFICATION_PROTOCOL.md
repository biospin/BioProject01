# 원고 검증 프로토콜 — AKM WEEK 03 운영화 (BIOP01 HSPC velocity)

> 출처 개념: AKM WEEK 03 — Verification(사실 검증)을 Refinement(표현 개선)와 분리한다. "더 자연스러운 문장 = 사실 확인"이라는 착각을 깬다. 이 문서는 그 프레임워크를 BIOP01 원고(`draft_v2.md`/`draft_v2_ko.md`)에 운영화한다.
>
> 실행기: `scripts/verify_manuscript.py` (과제2 = 에이전트·파일 기반, tool evidence). 산출: `results/verification/manuscript_verification_report.md`.
> **원칙: 이 하네스는 검증하고 보고할 뿐 고치지 않는다.** 수정은 사람이 correction gate(구체적 충돌이 있을 때만·cap 안에서) 아래 한다.

## 왜 필요한가

도구·판정 조각은 이미 다 있는데, AKM의 "하나의 검증 루프"로 묶은 게 없었다. 위험 Tier·correction cap·stop rules·per-claim verdict를 한 프로토콜/러너로 엮은 산출물이 부재했다. 2026-08 FINDINGS magnitude 라벨 사건이 그 부재의 증상이다. 도구(`check_manuscript_numbers.py` 등)는 있었지만 루프가 안 돌아 "비차단 잔여 1건"이 열흘 방치됐다.

## BIOP01에 이미 있는 조각 ↔ AKM 매핑

| AKM WEEK 03 요소 | BIOP01 기존 자산 |
|---|---|
| Baseline 동결 | git HEAD + `check_revision_preserved.py`(수정 전후 헤드라인 숫자·인용 대조) |
| Deterministic checks (과제2 tool evidence) | `check_manuscript_numbers.py`·`p3_*` 재계산·`p13_check_uncited_sources.py`·`verify_citations.py` |
| Claim ledger (Tier 3) | `CLAIMS.yaml`(BIOP01-69) + `check_claims_ledger.py` |
| No-degradation readback | EN/KO parity + 재계산 diff 0 |
| Verdict / HOLD | `PAPER_DIRECTION.md` claim-defensibility 게이트 |
| Evidence 독립성 사다리 | 실사용례(2026-08 FINDINGS): gate 재계산 → advisor 교차점검 → 종결 release |

핵심: 조각은 다 있으니 새로 만들 도구는 없다. AKM는 이것들을 **하나의 루프로 라우팅**하고, 언제 멈추고(stop rules) 몇 번까지 고치고(cap) 무엇을 보류할지(HOLD)를 규율한다.

## 위험 Tier 판정

이 원고는 **Tier 3 (투고·공개, 동료심사 대상)**로 다룬다. 근거 수준 = Claim ledger + 사람 권한, correction cap = 최대 2회.

## 8단계 검증 루프 (원고 적용)

1. **Baseline 동결** — 현재 `draft_v2.md`/`draft_v2_ko.md`의 SHA-256 + git HEAD를 기록(변경 없이 보존). 러너가 자동 스탬프.
2. **고영향 범위 선택** — headline claim 3~5개만 대상화(전체 문장 아님). 현 headline: (a) α만 방법 간 재현 ρ=0.88, (b) lag magnitude 잘해야 약함(strongest +0.163, 대부분 |ρ|≤0.08), (c) ATAC-shuffle 불변(lag=모델 구조), (d) α는 대체로 발현(abundance 보강), (e) 사전등록 6/6.
3. **독립 질문 설계** — 초안 문구를 복제하지 않는 원자적 질문. 예: "strongest magnitude pair가 정말 MV×MVVAE +0.163인가, 근거 파일은?"
4. **초안과 분리해 답하기** — 초안이 아니라 source(results/*.md·csv) 또는 도구(재계산 게이트)만으로 답한다.
5. **Evidence priority 적용** — 직접 원문 > 도구 출력 > 결정적 검사 > 권한자. 러너의 deterministic checks는 Lv3~4(도구·결정적 검사)이며, **단독으로 최종 verdict가 아니다**(사람=Lv8 필요).
6. **Correction gate** — 구체적 충돌이 있을 때만 최소 수정. 표현이 어색하다고 고치지 않는다(그건 Refinement, 별개).
7. **No-degradation readback** — 수정 후 맞던 헤드라인 숫자·인용이 손상되지 않았는지 `check_revision_preserved.py`로 확인.
8. **Verdict + 조건부 Learn-back** — PASS / PASS_WITH_NOTE / HOLD / FAIL. 조건 없는 HOLD는 규칙으로 승격하지 않고 후보로만 보존.

## 러너가 체인하는 결정적 검사 (tool evidence 층)

| 검사 | 잡는 것 | exit 규약 |
|---|---|---|
| `check_manuscript_numbers.py`(EN·KO) | 원고에만 있고 결과문서엔 없는 수치(드리프트·오타·지어냄) | 0=PASS, 1=HOLD |
| `check_revision_preserved.py`(EN·KO) | 수정 중 헤드라인 숫자·인용이 조용히 바뀜/삭제 | 0=PASS, 1=HOLD, 2=baseline없음 |
| `p13_check_uncited_sources.py` | 본문→목록 인용 결함 | 0=PASS, 1=HOLD |
| `verify_citations.py` | 인용 서지 정합(CrossRef) | 0=PASS, 1=HOLD |
| `check_claims_ledger.py` | CLAIMS.yaml claim↔draft 모순 | 0=PASS, 1=HOLD (CLAIMS.yaml 없으면 SKIP) |
| `check_quote_integrity.py` | 인용문 훼손 | 0=PASS, 1=HOLD |
| `p3_concordance.py` 외 재계산 게이트 | 헤드라인 수치 결정론적 재현(diff 0) | env(scv-preprocess)+data 필요 → 별도 실행, 러너는 SKIP 표기 |

**verdict 매핑**: exit 0 → PASS. exit 1/2 → **HOLD**(자동 FAIL 아님 — 예: 반올림 오탐은 사람이 정당 판정). 스크립트 크래시 → FAIL. 러너는 자동 PASS를 신뢰하지 않는다(각 도구의 자기 경고와 같은 결).

## 과잉 검증 방지 (AKM 8실패 대응)

- **Correction cap = 2회**(Tier 3). 초과 시 stop.
- **False correction 주의**: 약한 반대(오탐)로 맞는 것을 틀리게 바꾸지 않는다. 반올림·CI 경계·파생값 오탐이 대표 사례.
- 6 stop rules 중 하나면 즉시 멈춘다: (1) correction cap 도달 (2) 필요한 근거 부재 (3) no-degradation 실패 (4) judge 불일치 미해소 (5) readback 후 새 중대 모순 (6) 검증 비용 > 작업 위험.

## HOLD 카드 4필드 (마땅한 종결이 아님)

각 HOLD는 다음을 채운다: (1) 부족한 증거 구체화 (2) 다음 확인 1개 (3) 책임자/권한 경계 (4) 재개 조건.

## 최종 문장 템플릿

> 이 원고 검증은 **Tier 3**이고, **직접 원문·결정적 재계산**이 없으면 **고치지 않고 HOLD로 사람에게 이관**한다.

## 사용

```bash
python3 scripts/verify_manuscript.py                 # 전체 결정적 검사 체인 + verdict 리포트
python3 scripts/verify_manuscript.py --with-recompute # p3 재계산 게이트까지(scv-preprocess env 필요)
```
산출: `results/verification/manuscript_verification_report.md`(baseline SHA·per-check verdict·HOLD 카드). 커밋·투고 전, 그리고 리뷰 지적 반영 후 실행한다.

## ★ 함정 기록 — circular evidence (2026-08-07 실제 발생·수정)

`--with-recompute` 재실행에서 숫자 드리프트 verdict가 HOLD→PASS로 뒤집혔다. 원인: 러너 리포트를 `results/`에 쓰는데, `check_manuscript_numbers.py`의 source 코퍼스가 `results/*.md`라 **자기 이전 리포트(플래그된 수치를 인용)를 근거로 읽어** 그 수치가 "근거에 실재"한다고 통과시켰다. AKM가 경고한 **weak-judge propagation / circular evidence** 그 자체다. 하네스가 자기 산출물을 검증 근거로 삼으면 안 된다.

수정: 러너 리포트를 `results/verification/`(코퍼스 glob `results/*.md`가 매치 안 함)에 쓴다. 검증 산출물은 검증 대상의 source 코퍼스에서 반드시 격리한다. 재실행 결과 숫자 드리프트가 정직하게 HOLD(9.44→9.4 정당 반올림 오탐)로 복귀했다.

교훈: 검증 verdict가 재실행에서 이유 없이 좋아지면 오염을 의심한다(정상이면 결정적 검사는 재현적이어야 한다).
