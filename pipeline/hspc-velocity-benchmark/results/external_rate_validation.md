# External construct-validation of fitted kinetic rates — γ vs measured t½, α vs measured TT-seq synthesis

실행 **2026-07-07**. 스크립트 `scripts/external_rate_validation.py`(Part A) + `scripts/external_rate_validation_partB.py`(Part B), env `scv-preprocess`.
원자료: `results/external_rate_validation_gamma.csv`/`.json`, `results/external_rate_validation_alpha.csv`/`.json`. Provenance = `data/PROVENANCE_halflife.md`.

> **질문:** 우리가 HSPC에서 *fit*한 kinetic rate가 실험으로 *측정된* 실제 kinetic 양을 회복하는가?
> α(전사율)는 method 간 robust(ρ=0.88, `FINDINGS.md` §1)로 확인됐는데, 이것이 "method 재현성"을 넘어 **실측 합성율**에도 앵커되는가(정확도 leg)? 그리고 method-fragile로 확인된 γ(분해율, cross-method ρ≈−0.1)는 **외부 ground truth가 있는데도** 실측 분해율을 회복하는가?
> **모든 검정은 rank(Spearman) 기반** — 절대율은 식별 불가(BayVel)이고 cross-context(leukemia line ≠ dynamic HSPC)라 절대값 비교 금지. 모든 ρ은 유전자 paired **bootstrap 95% CI (B=10⁴)** 동반. HK는 자명 보존이므로 **headline은 non-HK**.

---

## ★ 종합 판정
- **Part A (γ):** **어떤 method의 γ도 실측 mRNA 분해율을 일관되게 회복하지 못한다.** 세 cell-line × 세 method 9칸 중 **올바른 방향(γ↑↔decay↑)으로 CI가 0을 배제한 칸은 단 1개**(multivelovae × MOLM13, non-HK ρ(γ,k_deg)=**+0.164**, CI [+0.028,+0.291]) — 약함·단일 reference·CI 하한이 겨우 +0.03(경계). 정반대로, 교과서 scVelo dynamical γ(rna_only)는 가장 깨끗한 reference(MOLM13, 무검열)에서 **거꾸로**(γ↑↔decay↓) 유의하게 나오고(non-HK ρ(γ,k_deg)=**−0.224**, CI [−0.359,−0.085], CI 0 배제) THP1에서도 같은 역방향 경향(ρ=−0.167, CI [−0.324,+0.002] — **CI가 0에 걸침**, p=0.045). → γ는 **외부 ground truth가 존재함에도** 신뢰 회복이 안 됨. (이 유일한 회복 칸이 null로 뒤집혀도 서사는 오히려 더 깨끗해짐 — "어떤 method도 γ 미회복".)
- **Part B (α):** **fit한 α는 실측 K562 TT-seq 합성율을 세 method 모두에서 양(+)으로 유의하게 회복한다.** non-HK ρ = rna_only **+0.236** [+0.095,+0.368] · multivelo **+0.262** [+0.133,+0.385] · multivelovae **+0.285** [+0.165,+0.398] — 셋 다 CI가 0을 배제(p 9.6e-4~4.4e-6). cross-context(백혈병 세포주 vs dynamic HSPC)임에도 gene-intrinsic 합성율 순위가 보존.
> **결론:** α는 method 재현성(ρ=0.88)에 더해 **실측 합성율에 앵커된 유일한 식별 가능한 rate**다. **외부 ground truth를 가진 γ조차 회복이 약하고 심지어 거꾸로 나온다** — dissociation("α는 real·식별 가능, 나머지 rate는 fragile")이 순수 cross-method 재현성 밖의 **실험 앵커**로 확증된다.

---

## Part A — fitted γ vs 실측 mRNA 반감기 t½ [로컬 데이터, 확정]

관계식: t½ = ln2 / γ_true → γ가 실측 분해를 회복하면 **Spearman(γ, t½)는 음(−)** (γ 클수록 빠른 분해=짧은 t½). 회복 방향을 Part B의 양(+)과 맞추기 위해 **측정 분해율 k_deg = ln2/t½** 로도 병기(rank상 ρ(γ,k_deg)=−ρ(γ,t½) 정확 성립). **판정 규칙(method×cell-line): ρ(γ,k_deg)의 bootstrap 95% CI가 양(+)쪽에서 0을 배제하면 "회복".**

측정 패널(hour): K562(Todorovski, same-study SLAM-seq, 24h cap) · THP1(Todorovski, same-study, 24h cap) · **MOLM13(RNADecayCafe/EZbakR, cross-study, 실질 무검열 — 가장 깨끗한 reference)**. 검열율(값이 상한에 몰린 비율): K562 8.1% · THP1 3.4% · MOLM13 0.01%.

### non-HK headline (ρ(γ, k_deg) = 회복이면 양수)
| method | K562 (censor 8.1%) | THP1 (3.4%) | **MOLM13 (0.01%, 주지표)** | 판정 |
|---|---|---|---|---|
| rna_only (fit_gamma) | −0.118 [−0.320,+0.091] null | **−0.167** [−0.324,+0.002] ★거꾸로(경계) | **−0.224** [−0.359,−0.085] ★★**거꾸로 유의** | 회복 실패(역방향) |
| multivelo (fit_gamma) | +0.053 [−0.147,+0.247] null | +0.028 [−0.127,+0.183] null | −0.003 [−0.136,+0.134] null | 무신호 |
| multivelovae (vae_gamma) | −0.011 [−0.198,+0.175] null | +0.120 [−0.033,+0.271] null | **+0.164** [+0.028,+0.291] ✅약한 회복 | MOLM13서만 약 회복 |

(all/HK/uncensored 층 + ρ(γ,t½) 원값 = `external_rate_validation_gamma.csv`. uncensored 층에서도 위 부호·유의 동일 — 24h 검열이 결과를 만들지 않음. HK는 n 9~22로 CI 매우 넓어 비정보.)

**해석:** (1) 가장 깨끗한 reference(MOLM13, 무검열)에서 canonical scVelo γ(rna_only)는 **CI가 0을 배제하며 역방향**(fit γ 큰 gene이 오히려 반감기 길다=분해 느리다) → scVelo dynamical γ가 HSPC에서 scaling·switch와 얽혀 실측 분해 순위를 못 잡음. THP1도 같은 역방향이나 CI가 0에 걸침(경계). (2) multivelovae γ만 약하게 올바른 방향(+0.16)이나 CI 하한 +0.03(경계)·MOLM13 단일 reference. (3) multivelo γ는 세 reference 모두 무신호. → **`FINDINGS.md`의 "γ는 method-fragile(cross-method ρ≈−0.1)"이 외부 ground truth 축에서도 확증**: γ는 외부 실측이 있어도 회복이 약하거나 거꾸로다. (Part A는 hematopoietic near-context 실측이므로 null/역방향이 **정보적** — "그 method의 γ는 신뢰 불가"로 읽는다. Part B의 asymmetric hedge와 다름.)

---

## Part B — fitted α vs 실측 TT-seq 합성/생산율 [다운로드 완료]

측정: **GSE229305**(Todorovski 2024 SuperSeries GSE229314의 subseries, *"TTseq K562 production rates"* — 반감기 S10 xlsx와 **같은 study**), `synth_rate`, treatment=UT baseline, 11,776 gene. GEO FTP 직접 취득(proof-of-work 없음). **THP1 TT-seq 생산율 subseries 부재 → K562 단독.**
biophysical 대응: scVelo/MultiVelo **α ≡ TT-seq 생산율**. 회복하면 **양(+)**. K562 ≈ erythroid/MK, HSPC output lineage에 대응.

**사전등록 asymmetric 해석:** 양(+) ρ = α가 실 합성율 proxy로 검증됨. **null은 α가 틀렸음을 증명하지 않음**(cross-context K562≠HSPC + 절대 α 비식별 — rank만 의미). → null이어도 강등만, 반증 아님. 여기선 세 method 모두 **양(+) 유의**.

### α vs K562 TT-seq 합성율 (ρ, bootstrap 95% CI)
| method | all | **non-HK (headline)** | HK | 판정 |
|---|---|---|---|---|
| rna_only (fit_alpha) | +0.259 [+0.124,+0.387] | **+0.236** [+0.095,+0.368] (p=9.6e-4, n=193) | +0.629 [−0.007,+0.942] | ✅ 검증 |
| multivelo (fit_alpha) | +0.285 [+0.160,+0.401] | **+0.262** [+0.133,+0.385] (p=4.9e-5, n=235) | +0.698 [+0.343,+0.885] | ✅ 검증 |
| multivelovae (vae_alpha) | +0.315 [+0.200,+0.424] | **+0.285** [+0.165,+0.398] (p=4.4e-6, n=251) | +0.817 [+0.586,+0.929] | ✅ 검증 |

**해석:** 세 method 모두 non-HK에서 **CI가 0을 배제하는 양의 상관**(+0.24~+0.29) → fit α는 method를 바꿔도 **실측 hematopoietic 합성율의 gene-intrinsic 순위를 회복**한다. HK는 더 강함(+0.63~+0.82, 자명 보존 확인). 이는 cross-context(K562 leukemia에서 측정, α는 dynamic HSPC에서 fit)임에도 성립 → "α는 method 재현성뿐 아니라 **실험에 앵커된** 양"이라는 정확도 leg를 확립.

---

## 대조가 핵심 (Part A vs Part B)
**가장 깨끗한 apples-to-apples = 같은 cell-line(K562) 내 α vs γ** — 같은 세포·같은 gene축, cross-line 손짓 없음:
| K562 (non-HK) | rna_only | multivelo | multivelovae | 판정 |
|---|---|---|---|---|
| **α vs TT-seq 합성율** | +0.236 ✅ | +0.262 ✅ | +0.285 ✅ | **3/3 CI 0 배제** |
| **γ vs t½ 분해(k_deg)** | −0.118 null | +0.053 null | −0.011 null | **3/3 null** |

→ **같은 K562 세포에서, 같은 method들이 α는 실측 합성율을 회복하고 γ는 아무도 실측 분해를 회복하지 못한다.** (MOLM13/THP1은 multi-reference 확장 — γ는 거기서 약 회복 또는 역방향으로, 여전히 미회복.)

| | 외부 ground truth | 회복(비-HK) | 의미 |
|---|---|---|---|
| **α (전사율)** | TT-seq 합성율(K562) | **3/3 method 양의 유의**(+0.24~+0.29) | robust **AND** 실측 앵커 → 식별 가능·real |
| **γ (분해율)** | mRNA t½(K562·THP1·MOLM13) | K562 3/3 null, 9칸 중 1칸만 약 회복, canonical scVelo γ는 MOLM13서 역방향 | fragile, 외부 ground truth 있어도 미회복 |

→ dissociation이 method 내부 재현성을 넘어 **외부 실험 축**에서 재현됨. 이는 "α만이 식별 가능한 불변량"(ANALYSIS-EXTENSIONS thesis)의 가장 강한 외부 증거이며, MultiVelo 저격이 아니라 rate별 식별성 차이(data+model-class 성질)임을 보인다. **왜 α만 살아남나(식별성 프레이밍):** scVelo rate는 gene별 time-scale까지만 식별 가능해 cross-gene 절대 γ는 noisy한 반면, α는 cross-gene dynamic range가 훨씬 넓다 → 그 순위가 γ가 무너지는 곳에서 살아남는 이유. 이는 약점이 아니라 "α가 식별 가능한 rate"라는 주장을 뒷받침.

## 한계
1. **cross-context**: 실측은 leukemia line(K562/THP1/MOLM13), α/γ는 HSPC fit. gene-intrinsic 순위 보존 가정(proxy_join_gate PASS median ρ=0.74로 t½ 차용은 방어됨). 절대율 비교 금지 — rank만.
2. **Part B는 K562 단독**(THP1 TT-seq 생산율 subseries 부재). 독립 2차 소스(Schwalb 2016 GSE75792, K562 TT-seq)는 per-gene rate 재계산 필요 — 후속.
3. **Part A γ 역방향**은 "실측이 틀렸다"가 아니라 "그 fit γ가 분해 순위를 못 잡는다"로 읽음(γ fragile과 정합). MOLM13(무검열)이 K562/THP1(24h cap)보다 신뢰 reference.
4. n이 작음(비-HK overlap 87~251) — CI 폭 반영. HK 층은 n<25로 비정보(참고만).
5. **abundance 교란(Part B)**: α와 TT-seq 합성율이 둘 다 발현량(abundance)을 따라가서 +0.26이 나올 수 있음(s_ss = α/γ). non-HK 한정(자명 보존 gene 제외)이 부분 완화하고 biophysics(α↔합성율)가 상관을 **예측**하지만, "α가 abundance가 아니라 합성 kinetics를 특정 포착"까지 이 검정만으로 단정하지 않음 — rank 방향 검증에 한정.

## 재현
```
conda run -n scv-preprocess python scripts/external_rate_validation.py        # Part A (γ vs t½)
conda run -n scv-preprocess python scripts/external_rate_validation_partB.py   # Part B (α vs TT-seq)
```
입력: `results/{rna_only_dynamical_genes,multivelo_genes,multivelovae_genes}.csv`, `data/{todorovski_k562_halflife,halflife_thp1,halflife_molm13,k562_ttseq_synthrate,housekeeping.txt}` (data/ 는 .gitignore).
