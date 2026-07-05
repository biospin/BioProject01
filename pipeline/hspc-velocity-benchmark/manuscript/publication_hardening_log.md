# 논문 근거 보강 로그 — chromatin→transcription lag은 정말 "실재하는 양"인가

> **성격**: 이 문서는 진행 중 작업의 *서사형 로그*다. 나중에 블로그 글로 옮길 수 있을 정도로 정리하되, 아직 돌고 있는 실험은 "진행 중"으로 정직하게 표기한다. 숫자·판정의 canonical 근거는 `results/FINDINGS.md`, 전략 근거는 `novelty_strategy.md`, 선행연구는 `related_work.md`, 실시간 상태판은 `../PROGRESS-LIVE.md`.
> 시작: **2026-07-05**.

## 0. 왜 이 작업을 시작했나

우리는 HSPC 10x Multiome(GSE209878)에서 gene별 **chromatin→transcription lag** — 염색질이 열리는 시점과 전사가 켜지는 시점의 시간차 — 을 정량하고, 이 lag을 baseline 후성유전 feature로 예측해 후성유전 약물의 반응 *타이밍*을 예측하려 했다.

그런데 파이프라인을 5개 velocity method 팔(scVelo 동역학 floor, MultiVelo, MultiVeloVAE, MoFlow, CRAK-Velo)로 돌려 "lag이 method를 바꿔도 재현되는 양인가"(H1)를 검정한 결과는 **부정적**이었다: gene별 lag은 method 간 거의 무상관이고(pairwise Spearman ρ ≈ −0.04 ~ +0.12), 유일하게 robust한 것은 전사율 α(method 간 ρ=0.88)·집단 수준 방향 균형·canonical marker 방향뿐이었다.

문제는 **"근거가 논문 쓸 만큼 강한가"**였다. negative result는 정직하지만, 그 자체로는 "우리가 method를 잘못 썼다"는 반론에 약하다. 그래서 두 가지를 하네스로 확인했다: (1) 이게 이미 알려진 결과인가(**scoop 체크**), (2) 뭘 더 하면 출판 가능한 근거가 되는가.

## 1. 선행연구 정찰 — 우리 결과는 이미 나와 있나? (scoop)

`literature-scout`로 세 갈래를 훑었다: chromatin-informed velocity method들, velocity 벤치마크·비판 논문들, "염색질이 전사를 prime한다"는 chromatin-potential biology.

**판정 = novel하되 부분 선점.** 두 편의 2026 RNA-velocity 벤치마크는 velocity의 *방향*을 채점할 뿐 lag은 다루지 않았다. 하지만 **MoFlow(Hong et al. 2025)** 가 이미 MultiVelo와 per-gene lag을 우발적으로 비교하며 "일치하는 gene subset(consistent subset)이 있다"고 보고했다. 이게 가장 날카로운 위협이다 — 우리가 앞세워 인용하고 차별화해야 한다.

우리에게 고유하게 남는 것:
- 4개 팔 전체의 체계적 concordance를 **agreement-set = 공집합**까지 정량 (MoFlow는 두 method 사이 favorable subset만, null·held-out·인과대조 없이 본 것)
- **ATAC-shuffle 인과 음성대조** — 염색질↔RNA 결합을 세포 수준에서 깨뜨려도 lag이 불변 → lag은 chromatin 신호가 아니라 **모델 구조**에서 나온다
- **α-robust / lag-fragile 해리** — 같은 데이터에서 α는 method 간 ρ=0.88로 안정, lag은 ρ≈0

## 2. 프레이밍 전환 — negative를 mechanism으로

`novelty-strategist`의 결론: "concordance가 낮다"만으론 MoFlow 대비 incremental이다. 논문이 실재하는 이유는 **메커니즘**이다. 그래서 단일 주장을 이렇게 못박았다:

> **per-gene chromatin→transcription lag은 model-structural artifact다** — method 간 재현되지 않고 ATAC를 셔플해도 변하지 않는다. 반면 전사율 α는 cross-method invariant(ρ=0.88)다. 따라서 timing 모델은 lag이 아니라 α를 입력으로 써야 한다.

이건 "실패한 실험" 서사가 아니라 "**어떤 양이 실재하고 어떤 양이 모델의 그림자인가**"를 가르는 robustness audit이다. 겨냥 venue class = Genome Biology / Cell Reports Methods.

## 3. 지금 돌리고 있는 실험 (2026-07-05, 3트랙 병렬)

전략에서 뽑은 최저비용 실험 3개를 병렬로 걸었다. 목표는 위 단일 주장의 각 다리를 리뷰어 공격에 견디게 만드는 것.

### 트랙 A — correctness gate + MoFlow-subset 대치 *(재분석, ✅ 완료 2026-07-05)*
- **correctness gate → 헤드라인 pivot(결론은 생존)**: 예상보다 미묘했다. MultiVelo lag은 100% 양수(switch-time 단조정렬의 구조적 상수)라 그 *부호*는 정보가 없다 → **sign-consistency 검정에 못 들어간다**. 그 결과 sign-정보를 가진 clean method는 {MoFlow, MultiVeloVAE} 2개뿐이고, 2-method sign FDR은 degenerate(min p_perm=0.499)라 신호와 무관하게 agreement-set이 0이 된다. 즉 **"0/598 공집합"은 단순히 CRAK로 오염된 게 아니라 CRAK 없이는 3번째 sign-정보 method 자체가 없어 성립 불가** — 그래서 CRAK sensitivity arm으로 강등하고, **CRAK-independent 헤드라인은 magnitude concordance(|ρ|≤0.083)와 clean 2-method sign 48.1%(=우연)로 옮겼다.** verify-gate가 기존 p4 숫자(0/598)를 정확히 재현 → self-check 통과. FINDINGS §1 반영.
- **#1 MoFlow-subset → 부분 falsify, 더 정직한 주장으로 좁힘**: MoFlow "consistent subset" S(60 gene)을 held-out MVVAE로 검정하니 **+12.4pp chromatin-leading enrichment(61.7% vs 49.3%, one-sided binom p=0.037, n=60, uncorrected)** — 즉 순수 2-method 우연이 아니라 **약한 방향성 concordance는 실재**했다(mirror subset도 대칭). 이는 novelty_strategy §3의 "held-out에 일반화 안 됨" 예측을 **falsify**한다. 그러나 chromatin-priming 해석은 무너진다: magnitude rank ρ≈0.10–0.15, S 내 agreement-set 0/60, 그리고 **ATAC-shuffle 인과대조에서 S의 lag *순서*가 chromatin-독립(rank ρ=0.70 ≈ 전유전체 0.72), magnitude만 marginal 감소(−1.5%)**. → 정직한 최종 주장: **"약한 방향 일치는 있으나 재현되는 per-gene 크기 없음 + chromatin 인과 없음(switch-time 구조적)."** 이 좁힌 판정을 manuscript-writer가 써야 하고, §3의 낡은 한 줄은 쓰면 안 된다.

### 트랙 B — 벤치마크 확장 데이터셋 확보 *(다운로드, ✅ 완료 2026-07-05)*
cross-dataset 재현을 n=1 → n≥2로 늘리기 위한 데이터 확보(필터: paired RNA+ATAC + spliced/unspliced 복구 가능 + 분화 trajectory).
- **E18 mouse brain 5k → 즉시 GO**: loom을 열어 spliced/unspliced가 실제로 있음을 검증(4881 cell, spliced 5.3%·unspliced 5.4% nnz, 둘 다 정상). MultiVelo P1 입력(loom + filtered matrix + peak annotation + feature linkage)이 전부 갖춰져 `mv.aggregate_peaks_10x` 경로가 그대로 적용 → **전처리 거의 0의 두 번째 재현 + cell-cycle 스트레스 테스트.** (mouse symbol이라 within-dataset H1은 매핑 불필요, 인간 HSPC와의 lag-rank 비교는 ortholog 매핑이 선행 필요.)
- **GSE194122 human BMMC → staged, DEFER**: processed h5ad(2.79GB)엔 `counts`만 있고 spliced/unspliced 없음. 복구 경로를 *가정이 아니라 확인*: 원본 10x GEX possorted BAM(SRR17693266, 28.66GB, 공개 S3, dbGaP 불필요)에 velocyto를 돌리면 됨 — moderate(FASTQ 재run 아님). 무거우니 전용 run으로 미룸. HSPC와 같은 조혈 축이라 복구 시 가장 tight한 재현.
- **Bonus**: MultiVeloVAE figshare에 `3423-MV-2`(=우리 GSE209878 day7) post-processed 객체가 있음 → 나중에 저자 파이프라인의 reference-lag과 직접 cross-check 가능(트랙 B 범위 밖, 메모).

### 트랙 C — 두 번째 method 인과대조 *(GPU 재fit, ✅ 완료 2026-07-06)*
현재 ATAC-shuffle 음성대조는 MultiVelo 단일 method뿐이었다(FINDINGS 한계 #4). 이걸 **MoFlow**(DTW/딥러닝 relay-velocity — MultiVelo의 switch-time과 구조가 완전히 다름)로 확장했다: 같은 within-lineage ATAC 셔플을 MoFlow 입력에 적용하고 GPU(cuda:1)에서 재fit(636→633 gene, 6473s).
- **판정: MoFlow lag도 셔플에서 살아남는다 → "model-structural, not chromatin-driven"이 두 번째·구조 독립 method로 일반화.** 세 축이 수렴: ① lag 분포 원본=셔플(MW p=0.38, KS p=0.18) ② **per-gene signed ρ=+0.52**(셔플로 DNA 결합을 깨도 lag이 크게 안 변함) — 이걸 method-swap ρ=0.08과 나란히 놓으면 결정적이다: **DNA를 끊는 것보다 method를 바꾸는 게 lag을 훨씬 크게 흔든다**(chromatin-driven이면 정반대여야 함) ③ chromatin-채널 fit-quality 불변(|α_c| p=0.52, |velo_c| p=0.12, loss 비악화).
- 정직한 hedge: 약함≠0(loss에 미소 유의 shift p=1.6e-10이나 비악화 방향, chromatin-leading 비율 ~6pt drift) — marginal chromatin 기여는 있으나 지배적이지 않음(MultiVelo와 같은 패턴). caveat: ATAC batch·DTW 부호규약·single seed·same-ATAC refit 신뢰상한 미측정.
- **효과: FINDINGS 한계 #4("음성대조가 MultiVelo 하나뿐") 해소.** 중심 주장(lag은 모델 구조의 산물)의 최대 방어력 업그레이드.

## 4. 아직 열려 있는 것 / 다음

- 세 트랙 완료 시 `FINDINGS.md` §1을 clean 3-method 헤드라인으로 병합, HANDOFF/SESSION-LOG 갱신, 사람이 git 커밋.
- 그 다음 후보: GSE162170 cortex cross-dataset 재현 완주(별도 진행 중) → transient-TF가 풍부해 lag이 *더* method-민감할 것으로 예상되는 시스템에서의 공정한 외부 검정.
- 약물 perturbation arm(timing ground truth)으로 "day0 ATAC → α" 경로 검증 — 이게 원래 목표(약물 반응 타이밍 예측)로 돌아가는 다리.

---
*작성 규칙: 실험이 끝날 때마다 해당 트랙 문단을 결과 한 줄+판정으로 갱신하고, 진행 중 표기를 제거한다. 블로그 이관 시 §0~§2는 거의 그대로, §3은 완료형으로 다시 쓴다.*
