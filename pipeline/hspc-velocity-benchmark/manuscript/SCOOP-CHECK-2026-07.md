# Scoop check — profile-likelihood identifiability (§8) + multiome lag-benchmark (2026-07-10)

> 방법: deep-research 하네스(6 각도 → 16 1차출처 fetch → 70 claim 추출 → 25 claim 3표 적대적 검증, 23 확증/2 반증). 근거 전부 1차 출처 verbatim 인용. `related_work.md §0`(lag-benchmark 스쿱) 보강판.
> §8 실체 = `results/profile_likelihood_identifiability.md`: MultiVelo 목적함수를 α축 vs lag축(=t_sw2−t_sw1)으로 profile, per-cell 곡률 κ 측정 → α stiff(8.20/cell)·lag sloppy(2.24/cell), 곡률비 **3.53×**, α stiffer **94.57%**. 정직 framing = **상대(practical) 비식별**, 완전 평탄 valley 아님.

## 판정 요약

| 각도 | verdict | 한 줄 |
|---|---|---|
| **§8 profile-likelihood 식별성** (lag/switch-time sloppy WHILE α stiff, 우도 기하) | **PARTIALLY ANTICIPATED (not scooped)** | 세 논문이 각각 *구성요소*를 선취 — head-on cite-and-differentiate 필수 |
| **multiome cross-method lag benchmark** (lag method-fragile / α robust) | **FRESH** (medium conf; absence finding) | 이걸 thesis로 한 논문 없음. 본 논문 핵심 novelty는 여기 |

## §8 각도 — 반드시 정면 인용·차별화할 3+1편

1. **Zhang et al. "Quantifying uncertainty in RNA velocity" (ConsensusVelo)** — bioRxiv 2024.05.14.594102 / Biometrics 2026. **최근접 선행(최우선).**
   - 겹침: switch-time/latent-time 방향의 **weak(near-non-)identifiability를 우도 평탄성+Fisher information으로** 확립. verbatim: *"large τc can only be weakly identified from the likelihood … The likelihood then remains almost constant for any sufficiently large τc (Fisher information of tc)"*; *"t0(2) tends to have large posterior uncertainty with right-skewed distribution … result from their weak identifiability"* (Kif11 long right tail). → **"flat switch-time valley" 절반을 직접 선취.**
   - 차별화(우리 우위): (a) RNA-only, **chromatin→transcription lag 없음**; (b) 단일-파라미터 Fisher weak-identifiability이지 **Hessian sloppy-vs-stiff 스펙트럼 아님**; (c) **stiff α vs sloppy switch 해리(dissociation) 안 함**(그들의 λ도 weakly identifiable로 표시); (d) Bayesian posterior-uncertainty framing이지 profile-likelihood/곡률비 아님.
2. **Gu et al. (Bioinformatics 2025, btaf581)** — **최우선 likelihood-geometry 방법 선례.**
   - 겹침: **profile-likelihood**로 single-cell telegraph/bursting kinetic rate(kon/koff/ksyn)의 **practical(구조적 아님) non-identifiability** 입증. verbatim: *"the profile likelihood (PL) function for each parameter is obtained … the majority of the parameter space is not practically identifiable from single-cell RNA sequencing data, and low capture rates worsen the identifiability."*
   - 차별화: **bursting 파라미터**이지 velocity switch-time/lag 아님 — 방법 선례는 되나 velocity-specific 결과는 아님.
3. **Wang "Are Single Cells Sloppy?" (bioRxiv 2025.12.31.697145)** — **sloppy/stiff Fisher 방법 직접 아날로그.**
   - 겹침: single cell에 **sloppy-vs-stiff Fisher eigenvalue** 프레임 적용, *"pronounced sloppiness in single cells."*
   - 차별화: 파라미터가 **cell-STATE Gaussian 좌표(μ,σ)**이지 velocity kinetic(α/β/γ/switch/lag) 아님. velocity는 transition kernel로만 사용. (⚠ 전문 PDF 403/429 — abstract+methods 기반, 최종 문구 전 재확인 권장.)
4. **(추가 플래그) BayVel (arXiv 2505.03083, 2025)** — scVelo dynamical 파라미터의 **구조적** non-identifiability를 **time-shift invariance** [s(t+a, t0on+a,…)=s(t,…)]로 증명. 우리 §8은 **practical(상대) 비식별**이라 상보적(전역 time-shift는 기지 scale degeneracy 계열) — 인용해 두되 우리 주장은 lag vs α **상대 곡률 해리**임을 구분.

**§8 방어 가능 novelty** = (i) **해리 자체**(lag/switch sloppy WHILE α stiff), (ii) **Hessian 곡률비(κ_α/κ_lag) sloppy/stiff 프레이밍**, (iii) **chromatin→transcription lag(multiome)로의 확장**. Zhang·Gu·Wang·BayVel 중 이 셋을 **결합한** 논문은 없음. 단, Zhang을 **정면으로** 인용·차별화하지 않으면 리뷰어가 "flat switch-time은 이미 알려짐"으로 감점 → §8은 "관찰의 우도-기하 **확증**"으로 프레이밍(단독 headline 금지).

## multiome lag-benchmark 각도 — FRESH
- MultiVelo/MoFlow/MultiVeloVAE/CRAK-Velo에 걸친 **per-gene lag의 cross-method 재현성 벤치마크(lag fragile / α robust)**를 thesis로 한 논문 없음(2023–2025).
- 최근접 = **MoFlow의 "consistent subset" 부수적 cross-method 비교**(이미 related_work에서 cite-and-differentiate 중). MultiVeloVAE 벤치마크는 scVelo/UniTVelo/DeepVelo/VeloVI/PyroVelocity/cellDancer 대상이라 우리 각도 미선취(반증 vote 1-2). HALO는 Granger-causality lag(다른 formalism)라 별개.

## 함의 (venue)
- **핵심 novelty는 lag-benchmark(fresh)에 있음** — 논문 축 그대로 유효(Primary tier: Cell Systems/MSB/eLife 현실적).
- **§8은 wholly-novel headline이 아님** — Zhang이 switch-time flatness 선취. "우도 기하로의 확증 + α/lag 해리 + multiome 확장"으로 정직 프레이밍하면 방어 가능하나, 이것만으로 Stretch(Nature Methods) tier를 끌어올리진 못함.

## 후속(열린 항목)
- Zhang 전문에서 **α를 stiff로 대조한 대목이 있는지** 확인(없으면 우리 해리 novelty 경계 선명).
- Wang 전문(접근 제한) 재독 — velocity ODE 파라미터에 sloppy 분석 적용 supplement 유무.
- Gorin/Pachter CME(Monod) 계열의 chromatin/switch-time 구조적 식별성 결과 타깃 재검색(telegraph=Gu만 표면화).
- 실행: **related_work.md에 Zhang·Gu·Wang·BayVel 4편 추가** + §8 서술을 "확증+해리+multiome" 프레이밍으로 조정(manuscript-writer).

## 출처(1차, 검증)
- Zhang ConsensusVelo — https://www.biorxiv.org/content/10.1101/2024.05.14.594102v1.full.pdf
- Gu profile-likelihood — https://academic.oup.com/bioinformatics/article/41/11/btaf581/8300553
- Wang Are Single Cells Sloppy — https://www.biorxiv.org/content/10.64898/2025.12.31.697145v1
- BayVel — https://arxiv.org/html/2505.03083v1
- Bergen 2021 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8388041/ · MoFlow — https://www.nature.com/articles/s41467-025-67259-6 · CRAK-Velo — https://link.springer.com/article/10.1186/s13059-026-04086-y · HALO — https://www.nature.com/articles/s41467-025-63921-1 · MultiVeloVAE — https://www.nature.com/articles/s41467-025-66287-6
