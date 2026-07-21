> ⚠️ **역사 문서.** 이 계획으로 만든 `draft.md`는 재프레이밍 후 폐기됐고 **정본은 `draft_v2.md`·`draft_v2_ko.md`**다. 아래 `draft.md` 언급은 당시 기록으로만 읽는다.

# WRITING_PLAN — HSPC velocity-lag benchmark 원고 골격 (집필 준비)

> **성격: 집필 *골격*(scaffold)이지 draft가 아니다.** 새 분석 0건 — 검증된 FINDINGS 수치를 Genome Biology IMRaD로 재조직하는 지도.
> **"go" 대기 중.** kkkim이 go를 주면 `paper-production-orchestrator`가 이 지도를 따라 `manuscript/draft.md`를 생성한다.
> 작성 2026-07-18. 근거 단일 컨텍스트 = `PAPER_DIRECTION.md`(claim 등급표·loop 규율). 결과 정본 = `../results/FINDINGS.md`(한글 절반이 canonical).

---

## 0. 타겟 저널 확정 — Genome Biology

kkkim 확정(2026-07-18). 전략 문서 4곳의 1지망(`novelty_strategy.md` L123, `NOVELTY-EXTENSIONS.md` L83, `HANDOFF.md` L67, `publication_hardening_log.md` L31)과 일치.

**GB 포맷 스펙(골격이 지켜야 함):**
- 구조: Title → Abstract(**structured: Background/Results/Conclusions**) → **Background**(Introduction 아님) → **Results** → **Discussion** → **Conclusions** → **Methods**(본문 뒤) → Declarations/References.
- 길이 제한 없음 → 근거 10절 + 6축 replication 전부 수용 가능(GB tier의 전제조건 = cross-dataset load-bearing, 이미 6/0 충족).
- Methods는 본문 뒤 별도. figure는 첫 언급 순 번호.
- 서사 프레임: **"어떤 velocity 출력이 실재하고 어떤 것이 모델의 그림자인가"를 가르는 robustness audit**(실패담 아님). identifiability framing이 이 tier를 벌어준다.

**Fallback(미확정, 필요 시):** Cell Reports Methods(co-primary) → Cell Systems/MSB/eLife → Bioinformatics(7p, 근거 축소 불가피). Nature Methods stretch는 §8 scoop 때문에 현재 근거로 미지지.

---

## 1. 지배 thesis + claim 등급표 (PAPER_DIRECTION §2 — 원고가 이 등급을 넘지 않는다)

**Thesis(한 문장):** 계산 method를 바꾸면 chromatin→transcription **lag**은 재현되지 않고(cross-method ρ≈0, 6축) 전사속도 **α**는 재현된다(ρ≈0.88) — 그리고 한 method *안*의 fit 자신감 ≠ method *간* 신뢰성. 이로부터 velocity 출력의 **신뢰 결정지도**를 제시한다.

| claim | 등급 | 원고 반영 |
|---|---|---|
| lag cross-method/dataset 비재현, α 재현 | **CONFIRMED** | headline (Results 전면) |
| within-method fit자신감 ≠ cross-method 신뢰성 (2층) | **STRONG** | Results (Table 2 근거) |
| velocity 신뢰 결정지도 | **STRONG** | Discussion 핵심 |
| lag는 저SNR+sloppy(식별성 얽힘) | **BOUNDED** | §8, "SNR과 분리 불가" 명시 |
| ❌ "식별성이 SNR 넘어 재현성 예측" | **REJECTED** | **본문 금지**(SNR 검정서 반증) |
| ❌ AI/파이프라인 기여 | **REJECTED** | 본문 금지 |

**융합 금지:** 표1(재현성)·표2(신뢰지도)를 하나 숫자로 합치지 않는다. within fit 품질을 cross 재현성으로 승격 금지.

---

## 2. ⚠️ 집필 전 반드시 처리할 플래그 (writer가 놓치기 쉬움)

1. **FINDINGS 영문 절반이 stale — writer는 한글 절반(canonical)에서만 인용.**
   FINDINGS.md 한글 헤더(L7)=2026-07-14, §7-E(gastrulation, **사전등록 6/0**) 포함. 영문 헤더(L175)=2026-07-10, **외부 4개만**, 영문 verdict(L288)에 gastrulation 없음, 영문 status table(L200-202)이 α_c refit·profile-likelihood freed를 ⬜pending으로 잘못 표기(한글 L33은 ✅). **원고가 영어라도 근거는 한글 절반에서 끌어온다. 또는 go 전에 영문 절반을 sync.** ← 안 지키면 가장 강한 sealed-before-fit 결과가 조용히 누락된다.
2. **§8 scoop 정면 인용 필수.** ConsensusVelo(Zhang et al., **bioRxiv 2024.05.14.594102**; 정식 Biometrics 82(1) ujag018)가 switch-time 약식별을 선취. §8은 **standalone novelty 아님 = confirmatory.** un-pre-empted 기여 = (i) α-stiff/lag-sloppy **해리**, (ii) 곡률비 κ_α/κ_lag 프레이밍, (iii) multiome chromatin→transcription lag 확장. **fresh thesis는 §8이 아니라 cross-method lag 벤치마크.** (Gu 2025 btaf581·Wang 2025·BayVel도 method 선례 인용 — `related_work.md`.)
3. **sealed-threshold 규율.** α 0.88은 *관측값*, 사전등록 *기준*은 Spearman ρ≥0.50 (`PREREGISTRATION_gse205117.md` L15). 임계 인용 시 **봉인 파일:줄 명시**, 관측값을 합격선으로 쓰지 않는다.
4. **정직 caveat(본문 명시):** lag-fragile leg는 replication서 대체로 단일 method쌍(MV×VAE)에 근거(gastrulation만 MoFlow 배선); 5 replication 모두 1 donor/sample → 강한 일반화 금지, 6축 일관성으로만 서사. profile-likelihood는 relative(practical) 비식별이지 완전 flat valley 아님; freed-nuisance 2.49×(하한)로 서술. pseudotime≠wall-clock. lag sign 구조적 양수=무정보.

**kkkim 결정 대기 2건(본편 골격은 안 막힘 — go 시점에 확정):**
- **(a) 미병합 2건 병합 범위**(§5 참조): 본문 삽입 vs revision 보류. → **본문 삽입 권장**(둘 다 accuracy/dissociation leg 강화).
- **(b) 저자·소속·corresponding·IP** = manuscript-writer `<FILL>`. **공개 게이트**만 막고 drafting은 안 막음 — `<FILL>`로 두고 진행.

---

## 3. Genome Biology IMRaD 섹션 지도 (FINDINGS § → GB 섹션)

### Abstract (structured)
- Background: velocity가 chromatin→transcription lag을 준다는데, 그게 method-robust한 양인가? drug-timing 예측 동기.
- Results: lag 비재현(|ρ|≤0.08, 6축) / α 재현(ρ=0.88) / 목적함수 해리(3.53×) / 사전등록 6/0.
- Conclusions: velocity 신뢰 결정지도 — α/rate는 믿고 lag/절대timing은 직교검증 필요.

### Background
- drug response timing 예측 동기 → chromatin→transcription lag 정량 목표(FINDINGS 연구질문).
- velocity method 지형(MultiVelo/MoFlow/MultiVeloVAE/CRAK-Velo, RNA-only floor).
- 선행: MoFlow consistent-subset·MultiVeloVAE 벤치마크·velocity critique(Gorin/Pachter, Marot-Lassauzaie) + **§8 scoop(ConsensusVelo) 정면**(`related_work.md`).
- H1 질문 제기: "lag은 method-robust한 양인가"를 drug-timing 전제로 먼저 검정.

### Results (첫 언급 순 = figure 번호)
| R# | 내용 | FINDINGS § | Figure/Table |
|---|---|---|---|
| **R1** | cross-method lag 비재현(clean headline |ρ|≤0.08, sign 48%≈chance) + α 재현 ρ=0.88 + 근원 α_c method-민감(0.29) | §1 | **Fig01** (fig01_p2_concordance) · **Table 1** |
| **R2** | 음성대조 — chromatin이 lag 미구동(ATAC-shuffle 분포 동일, 2 method: MV+MoFlow) | §2, §한계4 | (supp fig 가능) |
| **R3** | robustness 3각 + 예측가능성 — accuracy(crakvelo construct shape-왜곡)·stability(83% 표집-하한)·per-lineage refit(0.349<α_c 0.483)·**day0 ATAC→α 예측 ρ=+0.31 vs lag 비예측** | §5, §6 | lag_model.png, sim_injected_lag.png (supp) |
| **R4** ★ | cross-dataset replication 5 외부 + **사전등록 gastrulation 6/0**(load-bearing) | §7, §7-E | **Fig02** (fig02_crossdataset) · **Table 1** |
| **R5** | 목적함수 해리 — profile-likelihood α stiff/lag sloppy(κ비 3.53×, 94.57%), freed 2.49× 하한 + **정량 dissociation Δρ**(병합) | §8, +merge | **Fig05** (fig05_profile_likelihood) |
| **R6** | 합성 다중-method 양성대조 — lag 비재현은 regime-specific(식별 corner서 두 method 일치 ρ=0.454) | §9 | fig_sim_positive_control |
| **R7** | α 외부 앵커 — 실측 TT-seq 합성율 회복(non-HK ρ+0.24~+0.29), γ는 외부 GT 있어도 미회복(정직 null 2차 Schwalb 병기) | merge + §10 | fig03_novelty_comparison? |
| — | velocity 신뢰 결정지도 종합 | — | **Table 2** |

> confound(§3)·within-lineage 분포(§4)는 Methods/Supplementary로.

### Discussion
- 무엇이 robust(α/rate, 방향균형, canonical marker) vs 그림자(lag/절대timing/sign).
- drug-timing 함의: 단일 method lag 금지 → **day0 ATAC→α 경로** 사용(FINDINGS "drug-timing 연결").
- scoop 위치잡기(§8=확증), 한계(§Key limitations 6항).

### Conclusions
- velocity 출력의 신뢰 결정지도 = 이 논문의 기여. lag 생물학 부재 주장 아님 — "현재 method로 무엇을 믿을 수 있나"의 경계.

### Methods (본문 뒤)
- 데이터셋(GSE209878 primary + 5 외부), 공통 전처리→method 분기, velocity 4 method + RNA-only floor, concordance 통계(Spearman rank, paired bootstrap B=10⁴ CI, permutation FDR N=10⁴), profile-likelihood(fixed/freed nuisance), **사전등록 프로토콜**(봉인 해시), confound 통제(cell-cycle/burst/ambient, within-lineage).

---

## 4. Figure · Table 인벤토리 (전부 디스크에 존재 — 재생성은 figures/figNN_*.py 결정론적)

| 산출 | 파일 | 섹션 | 상태 |
|---|---|---|---|
| Fig01 concordance | `figures/fig01_p2_concordance.png` (+.py) | R1 | ✅ 존재 |
| Fig02 cross-dataset | `figures/fig02_crossdataset_concordance.png` | R4 | ✅ 존재(gastrulation 반영 여부 go 시 확인) |
| Fig03 novelty 비교 | `figures/fig03_novelty_comparison.png` | R7/Discussion | ✅ 존재 |
| Fig04 harness concept | `figures/fig04_harness_concept.png` | (제외 검토 — AI/pipeline 기여 REJECTED) | ⚠️ 본문 미사용 권장 |
| Fig05 profile-likelihood | `figures/fig05_profile_likelihood.png` (+.py) | R5 | ✅ 존재 |
| supp: lag_model, sim_injected, sim_positive | `figures/*.png` | R3/R6 supp | ✅ 존재 |
| **Table 1** 재현성(6축 α ρ vs lag ρ) | (생성 필요) | R1/R4 | 🔲 go 시 FINDINGS §7-E 표에서 |
| **Table 2** velocity 신뢰 결정지도 | (생성 필요) | Discussion | 🔲 go 시 PAPER_DIRECTION §4에서 |

---

## 5. 미병합 2건 — 병합 권장(수치 파일 확인 완료)

### ⭐ (1) `results/identifiability_dissociation.md` → **R5에 병합 권장**
정량 dissociation headline. HSPC within: ρ_α **+0.882** [+0.855,+0.904], ρ_lag(mag) **+0.163** [+0.078,+0.244], **Δρ = +0.720** 95%CI **[+0.639,+0.802]**(0 배제). lag 관례 robustness: magnitude +0.720 / signed +0.893 / rate-proxy +0.891(전부 0 배제). cross-dataset Δρ: BMMC +0.994, E18 +0.841. **경험적 식별성 순위 α > α_c > β > γ**(§3a 표). → §8 목적함수 해리(3.53×)에 **데이터 축 정량 짝**을 붙임.

### ⭐ (2) `results/external_rate_validation.md` → **R7에 병합 권장(§10 Schwalb null 병기 필수)**
accuracy leg 외부 앵커. **Part B(α):** fit α가 실측 K562 TT-seq 합성율 회복 — non-HK ρ rna_only **+0.236**[+0.095,+0.368]·multivelo **+0.262**[+0.133,+0.385]·multivelovae **+0.285**[+0.165,+0.398](셋 다 0 배제). cross-context(K562≠HSPC)임에도 rank 보존. **Part A(γ):** 외부 GT 있어도 γ 미회복(scVelo는 오히려 역방향 CI 0배제) → "γ method-fragile"을 실험 축서 확증. **정직: §10 Schwalb 2차 소스는 null(study 간 재현성 ρ≈0.15가 상한) — asymmetric hedge로 반드시 병기.**

> 두 건 모두 "α는 실재·식별 가능, lag/나머지 rate는 그림자"라는 headline을 **cross-method 재현성 밖(목적함수·실험 앵커)**에서 보강. 권장 = 본문 삽입. 최종은 kkkim §2(a) 결정.

---

## 6. Writer 제약 체크리스트 (go 시 manuscript-writer에 전달)

- [ ] 수치는 **결과 파일·검증 base만**, 메모리 재유도 금지. bootstrap CI + 적절 유의검정 동반.
- [ ] FINDINGS **한글 절반**에서 인용(영문 stale). §7-E gastrulation 6/0 누락 금지.
- [ ] claim이 §1 등급표를 안 넘음. REJECTED 2건(SNR 격상, AI 기여) 본문 금지.
- [ ] §8 ConsensusVelo 정면 인용 + "confirmatory" 표기. fresh thesis=lag 벤치마크.
- [ ] 임계 인용 시 봉인 파일:줄. α 0.88=관측값 ≠ 합격선(ρ≥0.50).
- [ ] 표1(재현성)·표2(신뢰지도) 융합 금지.
- [ ] pseudotime≠wall-clock, within-lineage, permutation FDR, lag sign 구조적 양수=무정보.
- [ ] 저자/소속/corresponding/IP = `<FILL>`(공개 게이트, drafting 안 막음).
- [ ] Fig04(harness) 본문 미사용(AI 기여 REJECTED 원칙).

---

## 7. "go" 런북 (kkkim go 시 메인 루프 실행)

1. `paper-production-orchestrator` §0 — `PAPER_DIRECTION.md` 로드(이 골격과 함께 컨텍스트).
2. 모드 = **초기·전체**(draft.md 부재). 새 분석 없음 → 3(집필)로 직행.
3. §2 플래그 처리: FINDINGS 영문 sync 여부 결정 → manuscript-writer가 GB IMRaD로 `draft.md` 생성(§3 지도) + Table1/2 생성 + figure 첫언급 순 재번호.
4. paper-critic 적대 검수 → 수정.
5. **검증 게이트**(커밋 전): `p3_concordance.py` + `p3_crossdataset_concordance.py` + `p3_scrambled_null.py` 재계산 → FINDINGS 대조. 불일치 시 멈춤·보고.
6. 공개(프리프린트/blog)·main 병합은 사람 승인. 작업 브랜치 push는 자동.
