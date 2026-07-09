# 추가 분석 현황 — 복구·통합 트래커 (2026-07-09)

> **왜 이 파일:** story-강화 추가 분석 설계·결과가 **커밋 안 된 untracked 파일**로만 존재해 기록이 유실될 뻔했다(HANDOFF에 없었음). 여기 한 곳에 상태를 통합한다. 설계 근거 = `ANALYSIS-EXTENSIONS.md`(통계·식별성 5종), `NOVELTY-EXTENSIONS.md`(profile-likelihood 데모), `DATA-HUNT.md`(외부 α 검증 데이터).
>
> **통합 thesis(재프레이밍):** lag은 multiome 스냅샷 + 현 모델군에서 **비식별(non-identifiable)** — chromatin 미구속(ATAC shuffle 불변)·method 미재현·baseline 미예측. **α만이 식별 가능한 불변량**(RNA-pinned; ATAC 없는 floor도 회복). = MultiVelo 저격이 아니라 data+model-class 성질(desk-reject 방어).

## ⏱️ 2026-07-10 갱신 — 커밋 상태 정정 + 신규 3종 착수
- **정정(이 문서가 stale했음):** 아래 "완료 2건"·"profile-likelihood 데모"는 **이미 커밋됨** — external kinetic α 검증(`results/external_rate_validation.md`)·dissociation(`results/identifiability_dissociation.md`)·**profile-likelihood 식별성(§8, `results/profile_likelihood_identifiability.md`, κ_α/κ_lag median 3.53×·α stiffer 94.57%)** 전부 git tracked + FINDINGS §8 병합. 최고 leverage(profile-likelihood)는 done.
- **신규 착수(2026-07-10, JIRA 분석=BIOP01-43 / critic=BIOP01-44 박세진):**
  - ④ **freed-nuisance 전체 게이트**(interior 302, CPU) — 실행 중. nuisance(α_c,β,γ,rescale,scale_cc) 재최적화해도 lag sloppy 유지 확인 → §8 방탄. 산출 `results/profile_likelihood_freed.csv`.
  - ① **합성 다중-method 양성대조**(GPU, sub-agent) — 실행 중. sharp/고SNR method 일치·smooth/저SNR만 갈림(regime-specific) + FDR 검정력 보정. 산출 `results/sim_positive_control_multimethod.md`.
  - ③ **2번째 외부 α**(Schwalb GSE75792 K562 TT-seq, CPU, sub-agent) — 실행 중. α 앵커 2번째 독립 소스. 산출 `results/external_rate_validation_schwalb.md`.
- **cross-dataset #4 macrophage** fit 완료(커밋 `63fb5fa`, floor 881·MV 872·VAE 881), concordance는 지용기(BIOP01-29) downstream 대기.

## 완료 (CPU, 결과 파일 존재 — 아직 커밋·FINDINGS 병합·블로그화 안 됨)

| 분석 | 결과 파일 | 핵심 결과 | 블로그 소재? |
|---|---|---|---|
| **HUNT1 외부 kinetic 검증** (α vs 실측 TT-seq 합성율, γ vs 실측 t½) | `results/external_rate_validation.md` (+ `_alpha/_gamma.csv/.json`), `scripts/external_rate_validation.py`·`_partB.py` | **α: 3/3 method 실측 합성율 회복**(non-HK ρ +0.24~+0.29, CI 0 배제). **γ: 외부 ground truth 있어도 미회복**(K562 3/3 null, canonical scVelo γ는 MOLM13서 역방향). → dissociation이 실험 앵커로 확증. | ⭐ **강함** — "α는 재현될 뿐 아니라 실측에 앵커됨" 정확도 leg. 신규 편 감. |
| **#1 paired Δρ dissociation + CI + TOST / #3a 식별성 랭킹 / #3b γ/β sloppiness / #5 cross-dataset CI / diff-budget** | `results/identifiability_dissociation.md` (+ `.csv`), `scripts/p3_identifiability_dissociation.py` | **Δρ(α−lag)=+0.720 CI[+0.639,+0.802]** 0 배제(BMMC~0.9·E18~0.8 재현). 식별성 **α≫α_c>β>γ**. cross-dataset α CI 겹침→순서는 정성적. lag는 diff-budget으로 성분보다 붕괴. | ⭐ **강함** — 01·02 결론에 CI·등가검정·식별성 랭킹 붙임. 본편 보강 or 번외 methods 편. |

## 미완 — 사용자(kkkim) GPU 몫 ★ 기록 유실 핵심

| 분석 | tier | 상태 | 근거 |
|---|---|---|---|
| **#2 다중 method 양성대조(합성 injected lag)** — sharp/고SNR에서 독립 method 일치, smooth/저SNR에서만 갈림 = regime-specific 네거티브 | **REFIT, GPU** (합성 c/u/s를 MultiVelo·MoFlow 포맷에 fit; format plumbing이 진짜 비용) | **미착수** | `ANALYSIS-EXTENSIONS.md` #2. O1·O3 flagship, permutation-FDR 검출력 보정 부수효과 |
| **SHARE-seq mouse skin GSE140203** 재현 (RAW→velocyto→P1~P3) | **heavy/GPU** | **미착수**(HANDOFF서 사용자 직접 수행 확정) | 5번째 replication; NOVELTY-EXTENSIONS는 "profile-likelihood가 5th dataset보다 나음"이라 우선순위 낮음 |

## 미완 — CPU (팀/assistant 가능, GPU 아님)

| 분석 | tier | 비고 |
|---|---|---|
| **NOVELTY #1 profile-likelihood 식별성 *데모*** — MultiVelo objective를 lag축 vs α축으로 profile → lag 평탄(비식별)·α 뾰족 | **CPU, ~1주, 최고 leverage** | 해석("비식별")을 목적함수 성질로 *입증*. 기존 fit 재사용, 신규데이터/ GPU 불필요. **5th dataset보다 우선**(NOVELTY-EXTENSIONS §2·§6) |
| #4 priming marker salvage (canonical marker서 chromatin-lead 재현?) | CPU | sign 검정 {MoFlow,VAE}만; MultiVelo 구조적 sign 금지 |
| HUNT1 2차 소스 Schwalb GSE75792 (K562 TT-seq) α 검증 | CPU | per-gene rate 재계산 필요 |
| 약물-timing bridge (#3/HUNT2) | **집필만** | 신규 run 없음. Discussion에 "α가 채울 transferable-feature 슬롯" design principle로 |

## 팀 배정 (모집 — 둘 다 아직 "해야 할 일", 지원 응답 전)
- **BIOP01-29** 가벼운 cross-dataset 확장 분석 → **지용기 님**
- **BIOP01-39** 완료 분석 결과·결론 critic/cross-review → **박세진 님** (전례: 박상준 님 BIOP01-25 lag 해석 정정)

## 다음 액션 제안
1. **완료 2건을 FINDINGS.md에 병합** + 블로그화(신규 편: 외부검증 + 식별성/dissociation). ← assistant 가능
2. **profile-likelihood 데모(CPU)** = 논문 ceiling 최대 상승. GPU 아니니 assistant/팀 가능 — 착수 여부 결정 필요.
3. **사용자 GPU**: #2 합성 양성대조 + SHARE-seq — 착수 시점 사용자 결정.
4. 이 untracked 결과·설계 파일들 커밋 여부(사람 승인) — 지금 git에 안 잡혀 있어 유실 위험.

*근거 파일 전부 `pipeline/hspc-velocity-benchmark/` 아래. 갱신 2026-07-09.*
