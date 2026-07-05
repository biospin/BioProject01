# 크로마틴은 정말 전사(轉寫)를 "미리 준비"시키는가 — HSPC multiome으로 lag을 재검증한 이야기

단일세포 multiome 데이터에서 "크로마틴이 열리고 → 전사가 따라온다"는 시간차(lag)를 유전자별로 다시 재보려
했다. 결론부터 말하면, **그 lag은 우리가 기대한 만큼 견고한 양(量)이 아니었다.** 다만 그 실패 덕분에 정작
쓸모 있는 신호가 무엇인지가 오히려 또렷해졌다. 이 글은 원본 논문의 아이디어에서 시작해, 데이터셋에 숨은
함정, 그리고 단계별 분석에서 무엇을 발견하고 무엇을 접었는지를 정리한 기록이다.

---

## 0. 우리가 답하고 싶었던 질문

큰 그림부터 짚자. 최종 목표는 이렇다.

> **처리 전(untreated) 세포의 후성유전 상태만 보고, 그 유전자가 후성유전 약물(HDAC 억제제, DNMT 억제제,
> EZH2 억제제 같은 것)에 *얼마나 빨리* 반응할지를 예측할 수 있을까?**

직관은 단순하다. 크로마틴이 이미 열려 전사와 딱 붙어 움직이는("poised") 유전자는 약물 자극에 빠르게 반응할
것이고, 크로마틴과 전사 사이에 긴 시간차가 있거나 완충(buffered)된 유전자는 느리게 반응할 것이다. 그렇다면
**baseline에서 잰 "크로마틴→전사 lag"이 약물 반응 timing의 예측 변수가 될 수 있다.** 이것이 우리 논문의
novelty로 이어질 다리다.

그런데 이 다리를 놓으려면 먼저 확인할 것이 있다. **애초에 그 "lag"이라는 것이 믿을 만하게 잴 수 있는 양인가?**
method를 바꿀 때마다 값이 뒤집히는 변덕스러운 숫자라면, 그것을 예측 변수로 삼는 일은 모래 위에 집을 짓는
것과 같다. 그래서 우리는 예측 모델을 만들기 전에 **"lag은 method-robust한 양인가?"**부터 정면으로 검정했다.
이 글의 대부분은 그 검정의 이야기다.

---

## 1. 원본 논문 — MultiVelo, 크로마틴을 ODE 안에 넣다

출발점은 **MultiVelo**(Li et al., *Nature Biotechnology*, 2023)다. 우리 1차 데이터셋도 이 논문이 새로
생산한 것이다.

### 배경: RNA velocity의 한계

RNA velocity는 하나의 단일세포 스냅샷만으로 세포의 미래 방향을 추정하는 영리한 아이디어다. 아직 스플라이싱되지
않은 unspliced RNA(u)와 스플라이싱된 spliced RNA(s)의 비율을 보면, 그 유전자가 지금 켜지는 중인지 꺼지는
중인지 알 수 있다. scVelo의 dynamical 모델은 이것을 미분방정식으로 fit한다.

    du/dt = α − βu      (전사 → unspliced)
    ds/dt = βu − γs     (splicing → spliced → 분해)

문제는 **전사율 α를 induction 구간 내내 상수로 가정한다**는 데 있다. 그래서 크로마틴이 서서히 열리면서
전사율이 0에서 최대로 *올라가는* 과정을 볼 수 없다. RNA만 보기 때문에, 전사가 시작되기 *전에* 일어나는
크로마틴 priming 역시 놓친다.

### MultiVelo의 한 수: α를 크로마틴의 함수로

10x Multiome처럼 *같은 세포에서* RNA와 ATAC(크로마틴 접근성)를 동시에 재는 기술이 등장하면서, MultiVelo는
크로마틴 접근성 c(t)를 방정식 안에 직접 집어넣었다.

    dc/dt = k_c·α_c − α_c·c     (크로마틴 열림/닫힘)
    du/dt = α·c(t) − βu         (★ 전사율이 c(t)에 비례)
    ds/dt = βu − γs

핵심은 α·c(t)다. 크로마틴이 닫혀 있으면(c≈0) 전사도 0이고, 열리면 그에 비례해 올라간다. 이 한 줄 덕분에
모델은 각 유전자를 네 가지 상태로 분류할 수 있게 된다.

- **primed** — 크로마틴은 열렸는데 전사는 아직(c>0, u≈s≈0)
- **coupled-on** — 크로마틴과 전사가 함께 켜짐
- **decoupled** — 크로마틴은 닫히는데 전사는 아직 진행(엇박자)
- **coupled-off** — 함께 꺼짐

그리고 유전자를 **M1**(크로마틴이 전사 억제보다 *먼저* 닫힘)과 **M2**(전사 억제가 먼저이고, cell-cycle
유전자가 여기 몰림)로 나눈다.

### 논문이 보여준 것

네 개 데이터셋(마우스 뇌, 마우스 모낭, 태아 인간 대뇌피질, 그리고 **인간 HSPC**)에서 MultiVelo는
RNA-only(scVelo)가 만들어내던 "역류(backflow)" 같은 아티팩트를 없애고, 조혈 계층구조(HSC→MPP→...)를 제대로
복원했다. 시뮬레이션에서는 M1/M2 분류 정확도 98.5%, decoupling의 통계적 유의성(LRT p값이 10⁻²⁷⁹까지),
그리고 태아 뇌에서 "TF 발현이 그 결합부위 접근성보다 먼저 올라간다"는 cross-modality lag까지 정량했다.

**한 가지 중요한 대목** — 저자들은 스스로 이렇게 못 박았다. *"추가 데이터 없이는 이 시간차의 메커니즘을
확정할 수 없다."* 곧 lag은 관찰된 연관이지 인과의 증명이 아니다. 이 겸손함이 우리 재검증의 출발선이 된다.

---

## 2. 데이터셋 — GSE209878, 그리고 그 안에 숨은 함정들

우리 1차 데이터셋은 MultiVelo 논문이 생산한 **Human HSPC 10x Multiome (GSE209878)**이다.

| 항목 | 내용 |
|---|---|
| 조직 | CD34+ 조혈모/전구세포(HSPC), 단일 공여자 |
| 배양 | Stemspan II 시험관 확장 배양 |
| 시점 | **day0, day7** (7일 분화·확장) |
| 플랫폼 | 10x Multiome — 같은 핵에서 ATAC + 유전자 발현 동시 측정 |
| 분화 축 | HSPC → 적혈구계 / 골수계 / 림프계 / 거핵구(혈소판) |

이 데이터셋에는 **세 개의 함정**이 있었고, 분석 내내 우리를 따라다녔다.

**함정 ① Pseudotime ≠ 벽시계 시간.** day0/day7이라는 실제 시점이 있어 "시간 anchor로 쓸 수 있겠다" 싶지만,
day0과 day7은 batch 효과를 제거하려고 Seurat으로 통합되어 있다. 곧 **day 라벨이 batch와 aliased**되어 있어,
day0→day7 변화의 상당 부분은 시간이 아니라 *세포 구성 변화*(분화로 세포 종류가 바뀜)다. 따라서 **lag은 벽시계
단위로 낼 수 없고 pseudotime 단위로만 보고**해야 한다. 원래 설계에서 기대했던 "wall-clock lag" 가설은 이
때문에 강등됐다.

**함정 ② 세포 수 불일치(정직하게 밝혀둔다).** 원 논문은 11,605 세포를 보고했는데, 우리가 공통 파이프라인으로
재전처리하니 **21,878 세포**(day0 9,639 + day7 12,239)가 나왔다. QC 임계값 차이로 보이며, 이는 여전히 **열린
검토 항목**이다. 덮지 않고 기록해 둔다.

**함정 ③ 크로마틴 정보의 sparsity.** ATAC 신호는 매우 희소해서, peak를 유전자 단위로 집계하고 smoothing해야
한다. 이 집계 방식 자체가 하류의 lag 추정에 영향을 줄 수 있다(뒤에서 이것이 실제로 문제가 된다).

---

## 3. 분석의 뼈대 — 왜 여러 method를 동시에 돌렸나

lag의 ground truth는 이 데이터에 **없다.** metabolic labeling도, 세포별 실시간 시계도, perturbation도 없다.
그래서 우리가 답할 수 있는 질문은 "어떤 method가 가장 *정확한가*"가 아니라 **"어떤 lag 추정이 가장
*재현적·일관적*인가"**로 재정의됐다.

핵심 전략은 이렇다. **같은 전처리(P1)에서 출발해, 크로마틴을 다루는 서로 다른 velocity method 여러 개로 각각
lag을 뽑고, 그 값들이 서로 얼마나 일치하는지를 본다.** 만약 lag이 진짜 생물학적 양이라면 method가 달라도 비슷한
값이 나와야 한다. 이것이 **H1 가설**이다.

돌린 method들:

- **RNA-only floor (scVelo dynamical)** — 크로마틴 없이 얼마나 나오는지의 바닥선
- **MultiVelo** — 원본, switch-time 기반 lag
- **MultiVeloVAE** — 확률적 VAE 버전, rate-timescale 기반
- **MoFlow** — latent-time-free, DTW로 크로마틴↔spliced lag
- **CRAK-Velo** — UniTVelo 확장, 같은 GSE209878 사용
- **scrambled-chromatin** — 음성 대조군(뒤에서 설명)

lag의 정의가 method마다 다르기 때문에(switch-timing vs rate-timescale vs DTW), 비교할 때는 **크기(rank
correlation)와 방향(sign)을 반드시 분리**해서 봤다.

---

## 4. 단계별 분석 기록 (P0 → P5)

### P0 — 데이터 확보와 출처 고정

GSE209878을 다운로드(day0/day7)하고, sha256 매니페스트로 무결성을 고정하고, 라이선스 게이트를 확인하고,
provenance를 문서화했다. "어떤 파일이 어디서 왔고 해시가 무엇인지"를 못 박아 두는, 재현성의 기초 공사다.

### P1 — 통일 전처리

모든 method가 **완전히 동일한 세포/유전자/그래프**에서 출발하도록 단일 파이프라인으로 전처리했다. 이것이
중요한 이유는, 나중에 method 간 결과가 갈릴 때 그것이 *method 차이*인지 *전처리 차이*인지 헷갈려서는 안 되기
때문이다. 결과물은 21,878 세포 × [RNA 36,601 유전자(spliced/unspliced) + ATAC 유전자 단위 집계] MuData이며,
7개 lineage 라벨을 부여하고 day별 라벨을 세포 단위로 보존했다.

### P2 — method 실행 + 음성 대조군

각 method를 같은 substrate에서 fit했다. MultiVelo는 538개 유전자에서 switch-time 기반 lag(sw2−sw1)의 중앙값이
pseudotime 단위 **5.98**로 나왔다. 여기까지는 순조로웠다.

문제는 **음성 대조군**에서 드러났다. scrambled-chromatin은 원본 파이프라인과 딱 한 군데만 다르다 — ATAC를
**lineage 안에서 세포끼리 뒤섞어** 크로마틴↔RNA의 세포 단위 결합만 파괴한다(유전자별 주변 분포와 lineage
구성은 보존). 만약 MultiVelo의 lag이 진짜 크로마틴 신호에서 나온다면, 이렇게 뒤섞은 뒤에는 lag이 무너져야
한다.

**결과: 거의 바뀌지 않았다.** lag 분포는 통계적으로 동일했고(Mann–Whitney p=0.20, KS p=0.51), 유전자별 lag
상관은 ρ=0.72로 보존됐으며, 크로마틴 likelihood는 0.239→0.237로 사실상 불변이었다(Wilcoxon paired만
p=0.0003으로 아주 작은 marginal 기여를 잡아냈다).

**해석:** MultiVelo의 lag은 크로마틴 신호가 아니라 **모델 구조(switch-time 순서)와 유전자 고유의 RNA
동역학**에서 나온다. 첫 번째 경고등이 켜졌다.

### P3 — 일치도 검정 (H1의 핵심)

이제 method들끼리 lag을 맞대 봤다.

**lag 크기(rank)는 서로 거의 무상관이었다.**

| 쌍 | Spearman ρ | p |
|---|---|---|
| MultiVelo × MoFlow | −0.04 | 0.38 |
| MultiVelo × MultiVeloVAE | −0.01 | 0.81 |
| MoFlow × MultiVeloVAE | +0.08 | 0.04 |

정의를 최대한 apples-to-apples로 통일해도 +0.12에 그쳤다. **네 번째 method(CRAK-Velo)를 추가해도** 그림은
같았다 — moflow×crakvelo −0.15, crakvelo×mvvae −0.04.

**방향(sign)도 우연 수준이었다.** MultiVelo는 lag이 100% 양수("크로마틴이 항상 전사를 선도")로 나오는데,
이것은 **switch-time을 단조 정렬하는 모델 제약에서 비롯된 아티팩트**다(sign이 구조적으로 고정된다). sign이
자유로운 method들을 보면 크로마틴-선도 비율이 MoFlow 44.8%, MultiVeloVAE 49.3%, CRAK-Velo 41.1%로 전부
**~50/50**이다. 곧 데이터는 "크로마틴이 전사를 미리 준비시킨다"는 *전역적* 주장을 지지하지 않는다. 유전자
수준의 방향 일치도(moflow×mvvae)는 48%로, 동전 던지기다.

**근원 진단.** 왜 lag이 이토록 method에 민감할까? lag을 결정하는 것은 **크로마틴 열림 속도 α_c**인데, 이
α_c 추정 자체가 method-민감하다(ρ=0.29). 반면 전사율 **α는 method 간 매우 강건하다(ρ=0.88)**. 곧 lag은 α_c의
불안정성을 그대로 상속한다.

**여기서 프레이밍을 정확히 못 박아야 한다.** "lag이 비robust하다"는 것은 **cross-method** — method를 바꾸면
재현되지 않는다는 뜻이지, "lag이 무의미하다"거나 "MultiVelo가 틀렸다"는 뜻이 아니다. 단일 파이프라인
*안에서는* lag에 신호가 있다(뒤의 bootstrap 83%, α ρ=0.88). MultiVelo의 100% 크로마틴-선도는 "그 모델의
switch-time 정렬 아티팩트"라는, 구체적이고 공정한 지적이다.

### P3 곁가지 — Confound 통제

lag 결론이 혹시 교란변수 때문에 생긴 것은 아닌지 점검했다.

- **Cell cycle:** 세포 수준에서는 상관이 있지만(ρ≈0.33–0.36), **유전자 수준에서는 비편향**이다. fit된 lag
  유전자 중 cell-cycle 유전자는 1.9%뿐이고, 그것을 빼도 중앙값은 0.037밖에 변하지 않는다. 세포 수준 상관의
  정체는 "cycling이 lineage와 강하게 얽혀 있어서"다(거핵구 88% ↔ HSC 3%). lineage 안에서 분석하면 이미
  통제된다. 그래서 **전역 regress-out은 일부러 하지 않았다** — 그렇게 하면 분화 신호까지 지워버릴 위험이 있기
  때문이다.
- **Burst / ambient / doublet:** 모두 허용 범위였다. scrublet로 doublet을 점검했고 정상이었다.

### P4 — Permutation FDR로 통계 확증

유전자가 수천 개이니 다중검정을 엄격히 처리해야 한다. gene-label을 셔플한 null(N=10⁴)과 비교했다.

- cross-method 상관은 3쌍 중 2쌍이 null 대비 유의하긴 했으나, **효과가 극도로 약하고(|ρ|≤0.15) 방향도
  불일치**했다.
- 유전자별 cross-method sign 일관성으로 보면, FDR<0.10에서 **agreement-set = 0/598 유전자**, 곧 **공집합**이었다.
  어떤 유전자도 method 간에 lag 방향이 무작위 이상으로 일관되지 않았다.

### P5 — 세 방향의 robustness 검정 + 진짜 예측 경로

lag의 robustness를 세 축으로 마지막까지 몰아붙였다.

**(1) 정확도 — injected-lag 시뮬레이터.** 여기서 우리 스스로 함정에 한 번 빠졌다가 나왔다. 합성 데이터에
*알려진* lag을 심고 CRAK-Velo의 DTW 추정기가 그것을 회복하는지 봤더니 Spearman(true, recovered) = **−0.89**가
나왔다. 처음엔 이것을 "순위 회복 실패"로 오독했는데, 다시 보니 정반대였다 — **|ρ|=0.89는 추정기가 true-lag
순위를 *강하게 추적*한다는 뜻**이다. 진짜 문제는 **부호가 뒤집히고 크기가 붕괴**한다는 데 있었다.

**곁가지 — 우리 코드에서 잡은 부호 관례 버그.** 이 과정에서 CRAK-Velo용으로 짠 manual-DP DTW가 MoFlow의
fastdtw와 **부호가 반대**임을 발견해 고쳤다(j−i를 i−j로). 합성 switch 신호로 검증했다. 교훈은, **새 lag
코드는 부호를 반드시 단위 검증**해야 한다는 것이다. 매끄러운 동역학에서는 이 construct가 부호와 크기를 왜곡하는
shape-아티팩트가 있어, **CRAK-Velo lag은 cross-method 비교에서 신뢰하지 말라**는 것이 이 arm의 정확한
결론이다(핵심 H1인 moflow×multivelo×mvvae는 이 construct를 쓰지 않으므로 독립적으로 살아남는다).

**(2) 안정성 — bootstrap.** fit을 고정하고 세포를 복원추출하면 lag 부호가 **83% 안정**적이다. 다만 이것은
표집 노이즈만 본 *가장 약한* 안정성이라, cross-method 비robust와 모순되지 않는다. 진짜 re-fit 안정성은 이보다
낮을 것이다.

**(3) 예측 가능성 — baseline→timing 모델.** 순수 baseline 크로마틴 feature만으로 held-out lineage의 lag을
예측하려 하면 **실패**한다(ρ=−0.21). fit된 kinetic feature를 넣으면 ρ=+0.59로 오르지만, 이것은 **순환**이다
(α_c가 lag을 기계적으로 결정하기 때문이다).

**per-lineage refit.** 전역 fit을 lineage로 쪼개지 않고, 5개 terminal lineage를 각각 따로 fit했다.
cross-lineage lag 일치도는 ρ 중앙값 **0.349**(약함/경계)였고, 반면 대조군 α_c는 **0.483**(더 견고)이었다.
H1의 패턴("α가 lag보다 robust")이 lineage 축에서도 재현된 것이다.

**★ 진짜 day0 ATAC feature — 여기서 반전이 온다.** 지금까지는 크로마틴 feature로 smoothed proxy를 썼는데,
consensus peak(197,482개)에서 **day0의 HSC/MPP 8,583 세포**만 골라 유전자별 promoter(±2kb)/enhancer(±100kb)
접근성을 실제로 어셈블했다(511 유전자). 그리고 같은 baseline feature와 모델로 held-out lineage를 예측했더니
결과는 이랬다.

- **robust한 α는 진짜 day0 ATAC로 예측된다 — ρ=+0.31(6개 lineage 전부 양수).**
- 비robust한 lag은 ATAC로도 예측되지 않는다 — ρ≈+0.05(동전 던지기).

**이것이 이야기의 반전이다.** *같은 feature*가 robust target(α)은 예측하고 비robust target(lag)은 예측하지
못한다. 실패한 것(lag)만 남은 게 아니라, **성공하는 경로(day0 ATAC → α)가 데이터로 드러난** 것이다.

---

## 5. 곁다리 — 약물 반감기를 빌려와도 되나 (proxy-join gate)

Part 2(약물 예측)로 가려면 문제가 하나 있다. HSPC 자체의 약물 timecourse 공개 데이터가 없다. 그래서 mRNA
반감기(t½) 같은 필수 통제 변수를 다른 세포주에서 **빌려와야** 한다(Todorovski 2024가 baseline decay rate가
약물 반응 선택성을 결정한다고 보였기에, decay 통제는 필수다).

그런데 **백혈병 세포주 t½를 HSPC 분석에 차용해도 되나?** 이것을 정면으로 게이트 검정했다. 판정법은,
reference(K562) 대비 다른 세포주 t½의 유전자별 rank 보존(Spearman ρ)이며, 임계값은 0.50이다.

**판정: PASS(중앙값 ρ=0.74).** 주 지표인 cross-study 조혈계(MOLM-13)가 ρ=0.695, non-HK 유전자에서도
0.659였다. 핵심은, cross-lab의 같은 세포타입 상한(0.749)과 다른 조혈 세포주(0.695)의 차이가 ~0.05뿐이라는
점이다 — **세포타입을 바꿔도 rank 보존이 기술 노이즈 수준 이상으로는 거의 떨어지지 않는다** → t½는 강하게
gene-intrinsic이다. 한계는, 24h에서 우측 검열된 유전자가 있고, 여전히 primary HSPC의 직접 t½는 아니라는 점이다
(가장 가까운 것이 AML 세포주다).

---

## 6. 통합 결론

**크로마틴→전사 lag은 유전자 수준에서 method-robust한 양이 아니다.** 크기도 방향도 method 간에 일치하지
않으며(4-way + permutation FDR로 확증, agreement-set 0/598), 음성 대조군은 한 method(MultiVelo)의 lag이
크로마틴이 아니라 모델 구조에서 나온다는 것을 보였다.

**하지만 robust한 것들은 분명히 있다.**

1. **전사율 α** — method 간 ρ=0.88
2. **집단 수준의 방향 균형** — 두 독립 method가 ~50/50으로 수렴
3. **교과서적 priming marker의 방향** — method 간 일치
4. **day0 ATAC promoter/enhancer 접근성 → α** — held-out lineage 예측 ρ=+0.31

그래서 drug-timing 모델의 입력 경로는 **"lag을 단일 값으로 쓴다"가 아니라 "day0 ATAC 접근성 → α"**로
가는 것이 데이터로 지지된다. lag을 굳이 쓰려면 method 불확실성을 모델에 명시적으로 반영해야 한다.

---

## 7. 이 프로젝트가 준 방법론 교훈

- **재현하려다 발견한다.** 원 논문을 "재현"하려던 시도가, 오히려 그 논문의 핵심 양(lag)이 지닌 method
  민감성을 드러냈다. 네거티브 결과가 다음 단계(feature 선택)를 더 또렷하게 만들었다.
- **음성 대조군은 협상 불가.** "ATAC를 셔플했더니 lag이 그대로였다"는 한 줄이, "이 lag은 크로마틴에서
  나온다"는 순진한 가정을 깼다.
- **부호는 반드시 단위 검증.** 우리 DTW 코드의 부호 관례 버그는 합성 신호로 잡혔다. 방향을 다루는 코드는
  방향부터 검증한다.
- **정직한 스코프.** −0.89를 "회복 실패"로 오독했다가 "부호 반전 + 크기 붕괴"로 바로잡은 과정 자체가, 숫자
  하나가 무엇을 의미하는지 끝까지 따져야 한다는 교훈이다.
- **robust ≠ 유용, 유용 ≠ robust를 분리해서 보고한다.** α는 robust하면서 예측에도 쓰이지만, lag은
  흥미롭되 cross-method로는 쓸 수 없다. 이 둘을 한 문장에 섞지 않는다.

---

## 8. 다음 단계

1. **약물 perturbation arm** — timing ground truth가 있는 약물 timecourse 데이터로 "day0 ATAC → α → 약물
   반응 timing" 경로를 실제로 검증한다(필수 통제: mRNA decay를 통제한 뒤 lag의 *incremental* 기여를 nested
   ΔR²로 보는 설계).
2. **cross-dataset 재현** — 다른 조직의 multiome 데이터셋에서 이 ranking 패턴이 재현되는지 확인해, 단일
   데이터셋 결론의 견고성을 확보한다.
3. **α_c 추정 안정화** — lag을 굳이 쓰려면 bootstrap-stable 유전자로 한정한다.

---

*이 글은 진행 중인 연구의 내부 정리 기록이다. 수치는 현재까지의 분석 기준이며, 후속 검증으로 갱신될 수 있다.*
