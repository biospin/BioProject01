# 우리 결과를 스스로 공격한 세 가지 분석 — 리뷰어보다 먼저

> 한 줄 요약: 우리 결론을, 심사자가 던질 세 가지 반론으로 먼저 시험했다. 둘은 반론을 견뎌 냈고, 하나는 뜻대로 되지 않았다. 실패한 것도 나온 대로 적었다.

## 0. 핵심 개념

세포가 유전자를 쓰는 과정을, 이 시리즈에서는 서랍에서 서류를 꺼내 읽는 일에 빗대 왔다.

- **크로마틴 열림**(chromatin, DNA가 감긴 실타래): 서랍을 여는 일. ATAC로 측정한다.
- **전사 속도 α**(transcription rate): 꺼낸 서류를 읽는 속도. 유전자가 켜져 RNA를 만드는 빠르기다.
- **시간차 lag**: 서랍을 연 뒤 서류를 읽기까지 걸리는 시간. DNA가 열리고 유전자가 켜지기까지의 간격이다.

우리 논문의 결론은 아래 두 줄로 요약된다.

```
시간차(lag)  ── 프로그램 바꾸면 ──▶ 값이 달라짐  (재현 안 됨,  |ρ|≤0.08)
분해속도(γ)  ── 프로그램 바꾸면 ──▶ 값이 달라짐  (재현 안 됨,  ρ≈−0.1)
전사속도(α)  ── 프로그램 바꿔도 ──▶ 값이 그대로  (재현 됨,     ρ 0.88)
```

재현에 실패한 값이 시간차 하나가 아니라는 점을 처음 판에서 빠뜨렸다. 분해 속도 γ도 프로그램을 바꾸면 값이 달라지고(ρ≈−0.1), 외부 측정(K562 반감기)과 대조하면 세 프로그램 모두 맞지 않았다. 교과서격인 scVelo의 γ는 방향까지 뒤집혀 나왔다(−0.224, 신뢰구간이 0을 배제). 재현되는 것은 α 하나다.

여기서 ρ은 두 프로그램의 값이 얼마나 맞는지를 **−1에서 +1 사이**로 나타낸 수다. +0.7을 넘으면 "잘 맞음", 0 근처면 "관계 없음", 음수면 "반대 방향"으로 읽는다. 그러니 α(0.88)는 잘 맞고, 시간차(|ρ|≤0.08)는 사실상 안 맞는다.

한 가지만 분명히 해 둔다. "시간차가 프로그램을 바꾸면 안 맞는다"는 "크로마틴이 무의미하다"가 아니다. 크로마틴 신호 자체는 데이터에 실재한다 — 크로마틴 층과 RNA의 유전자별 상관은 +0.126인데 크로마틴을 뒤섞으면 +0.021로 무너진다. 잃어버리는 자리는 데이터가 아니라 **모델이 뽑아낸 시간차**다.

다만 처음 판에서 여기에 "한 프로그램 안에서는 시간차에 신호가 있다"고 적은 것은 거두어들인다. 우리 자신의 가장 센 자기비판이 정확히 그 반대를 가리키기 때문이다. **ATAC를 계통 안에서 뒤섞고 모델을 다시 적합해도 시간차 분포는 통계적으로 그대로였다**(Mann–Whitney p=0.20, 유전자별 순위 ρ=0.72). 크로마틴 신호를 없애도 시간차가 안 변한다면, 그 시간차는 크로마틴이 아니라 **모델 구조**(전환 시점을 한 방향으로 정렬하는 방식)가 만들어 낸 값이다. 부호 일치율이 54.6%로 우연에 붙어 있는 것도 같은 이야기다. 그러니 정확한 진술은 "한 프로그램 안에서는 신호가 있다"가 아니라, **한 프로그램 안에서 나오는 시간차조차 크로마틴을 근거로 읽어서는 안 된다**이다.

## 왜 스스로 공격하나

결론이 서면 심사자가 반론을 던진다. 우리가 좋아하는 결과를 심사자는 곧이곧대로 받아 주지 않는다. 그래서 그들이 던질 반론 세 가지를 미리 적고, 우리 손으로 먼저 시험했다.

```
① 다른 값을 고정해서 억지로 만든 그림 아닌가?      → 시험 1
② 계산법이 원래 시간차를 못 맞히는 것 아닌가?      → 시험 2
③ α가 실제 측정과 맞는다는 근거가 하나뿐인데?      → 시험 3
```

## 시험 1: 손잡이를 다 풀어 본다 (freed-nuisance)

α와 시간차 중 무엇이 더 "뚜렷한" 값인지는, 값을 살짝 흔들었을 때 점수(데이터에 얼마나 맞는지)가 얼마나 급히 떨어지는지로 잰다. 급히 떨어지면 데이터가 그 값을 뚜렷하게 정해 준 것이고, 거의 안 변하면 흐릿한 값이다. 앞선 분석에서 α는 뚜렷했고 시간차는 흐릿했다.

심사자는 이렇게 묻는다. 계산할 때 다른 값들(분해 속도 β·γ, 크로마틴 여는 속도 α_c 같은)을 손잡이 고정하듯 붙박아 두었는데, 하필 그 고정 때문에 시간차가 흐릿해 보인 것 아니냐고.

그래서 손잡이를 다 풀고 다시 맞춘 뒤 같은 계산을 돌렸다. 계산이 가능한 유전자 전체(수백 개)를 봤다.

```
손잡이 고정 → α 뚜렷함이 시간차의 3.53배  (α가 더 뚜렷한 유전자 94.57%)
손잡이 다 풂 → α 뚜렷함이 시간차의 2.49배  (α가 더 뚜렷한 유전자 77.03%)
```

풀어줘도 "α가 시간차보다 뚜렷하다"는 순서는 뒤집히지 않았다. 다만 손잡이를 풀자 α의 뚜렷함 자체는 줄었다(고정했을 때의 0.19배). 그래서 3.53배는 위쪽 한계로, 2.49배는 보수적인 아래쪽 값으로 보고, 논문에는 보수적인 쪽을 적는다. 첫 번째 반론에는 이렇게 답했다.

## 시험 2: 정답을 아는 모의고사 (양성대조)

두 번째 반론은 더 근본적이다. 프로그램들이 시간차에서 서로 안 맞는 게, 데이터 탓이 아니라 계산법이 원래 시간차를 못 맞히는 탓이라면?

이걸 가르려면 정답을 아는 데이터가 필요하다. 그래서 시간차를 우리가 직접 심은 가짜 데이터를 만들었다. 정답이 적힌 모의고사인 셈이다. 그리고 조건을 두 가지로 바꿔 가며 풀렸다. 신호가 잡음보다 얼마나 큰지(SNR), 그리고 전환이 얼마나 날카로운지다. 각 조건에서 서로 다른 두 프로그램(MoFlow, MultiVelo)이 정답을 맞히는지 봤다.

```
신호 큼  (SNR 20) │ 평균 일치 +0.242, 가장 좋은 구석 +0.454  ◀ 잘 잡히는 구석
신호 중간(SNR 6)  │ 평균 -0.035
신호 작음(SNR 2)  │ 평균 -0.005                            ◀ 실제 데이터가 사는 곳
```

신호가 크고 전환이 적당히 날카로운 좁은 구석에서만, 두 프로그램이 서로도 맞고 정답도 맞혔다. 신호가 작아지면 일치가 0으로 무너졌다. 실제 HSPC 데이터는 바로 그 신호 작은 구석에 산다.

정리하면, 프로그램끼리 시간차가 안 맞는 데는 데이터가 놓인 조건이 크게 작용한다. ("계산법의 흠이 아니다"라고 전면 면책했던 처음 문장은 지나쳤다 — 우리는 같은 연구에서 CRAK-Velo의 시간차에 부호 역전과 크기가 0.06배로 무너지는 추정 형태 문제를 실제로 찾아냈다. 계산법 쪽 흠도 있었고, 다만 그것만으로는 불일치가 설명되지 않는다는 것이 이 모의고사의 결론이다.) 실제 데이터에서 시간차가 안 맞았던 앞의 결론이, 계산 실패가 아니라 "원래 잡을 수 없는 조건"이었음을 이 모의고사가 보여 준다.

한 가지는 오해하면 안 된다. 잘 잡히는 구석은 아주 좁다. 신호 크기 20에서만 성립하는데, 유전자 하나당 그 정도 신호는 실제 데이터에선 비현실적으로 높다. 그러니 이 결과는 "시간차를 잘 잡을 수 있다"가 아니라 "실제 데이터는 시간차를 못 잡는 영역에 있다"를 오히려 굳힌다.

여기에 검정력 시험을 하나 덧붙였다. 알려진 크기의 신호를 심어 두고, 우리 검정이 그걸 잡아내는지 봤다. 일치도가 0.15쯤이면 대부분 잡아냈고(검출력 0.8 이상), 실제 시간차 일치도(0.08 이하)는 그 문턱 아래다. 즉 **크기 일치도** 쪽에서는 "잡을 수 있는 크기 아래로는 신호가 없다"가 맞는 진술이다.

**하지만 여기 이어 붙였던 "유전자 598개 중 0개 일치가 나온 건 검정이 무능해서가 아니다"는 문장은 틀렸다. 정정한다.** 그 0/598은 크기가 아니라 **방향** 검정이고, 방향 검정 쪽은 실제로 검정력에 막혀 있다. 부호가 흔들리는 깨끗한 프로그램이 둘(MoFlow·MultiVeloVAE)뿐이라 유전자당 얻을 수 있는 최소 p값이 0.5 근처(실측 0.499)이고, 그러면 신호가 있든 없든 어떤 FDR 문턱도 통과할 수 없다. 게다가 그 598개 검정은 셋째 프로그램으로 CRAK-Velo를 끌어 쓴 값이라 그 자체가 CRAK에 기댄다. 그래서 원고는 0/598을 헤드라인에서 내리고 CRAK 포함 민감도 분석으로 강등했다. 자기비판 시리즈에서 이 대목을 방어 논리로 쓴 것이 이 글의 가장 큰 잘못이었다.

## 시험 3: 두 번째 잣대, 그리고 실패 (Schwalb)

세 번째 시험은 결과가 우리 뜻대로 나오지 않았다.

α가 실제 측정치와 맞는다는 근거로, 앞서 외부 측정 하나를 댔다(Todorovski, K562 세포 TT-seq). 유전자별 α와 순위가 +0.24~+0.29로 맞았다. 문제는 근거가 하나뿐이라는 점이다. 그래서 같은 세포의 두 번째 독립 측정(Schwalb 2016)을 같은 방법으로 붙였다.

붙여 보니 맞지 않았다.

```
우리 α ── 첫째 잣대(Todorovski) : +0.24~+0.29   맞음
우리 α ── 둘째 잣대(Schwalb)    : −0.05~−0.01   안 맞음
첫째 잣대 ── 둘째 잣대           : +0.154        서로도 잘 안 맞음
```

원인을 따져 보니, 두 측정 자체가 서로 안 맞았다. 같은 세포의 같은 실험인데도 두 잣대의 순위가 겨우 0.15로만 겹쳤다. 자 두 개가 서로 안 맞으면, 어떤 값도 둘 다에 맞출 수 없다. 이것이 외부 확인이 도달할 수 있는 한계를 정한다. 좌표를 잘못 이어 붙인 오류는 아닌지도 확인했지만 검사는 통과했으니, 이 불일치는 실제로 나타난 결과다.

이 실패를 어떻게 읽느냐가 중요하다. 이 무상관은 "α가 측정치와 안 맞는다"는 증거가 아니다. 측정한 세포와 우리가 계산한 세포가 다르고, 절대적인 α 값은 원래 딱 정해지지 않으며, 이 두 번째 측정 자체가 잡음이 크기 때문이다. 정확한 발견은 "TT-seq 합성 속도 측정 자체가 연구마다 순위가 잘 안 맞는다(0.15)"는 것이고, 이것이 외부 확인의 한계다. 그래서 "근거 하나뿐"이라는 약점은 이 소스로는 없애지 못했다. 첫째 잣대의 맞음은 그대로 남지만, 둘째로는 재현도 반증도 되지 않는다.

결과가 밋밋해도 그대로 적었다. 두 번째 근거를 대려다 실패했고, 그 실패의 원인이 우리 계산이 아니라 측정 자체의 재현성에 있었다는 것, 이번에 얻은 건 거기까지다.

## 배운 점

- **방어에도 한계를 같이 적는다.** 시험 1은 반론을 막았지만, 그 과정에서 α의 뚜렷함이 줄어드는 것도 드러났다. 위쪽 값과 아래쪽 값을 함께 보고하고 보수적인 쪽으로 쓴다.
- **안 맞는 것이 오히려 신호일 때가 있다.** 시험 2는 "시간차가 안 잡힌다"가 방법의 흠이 아니라 조건 탓임을 보였다. 오히려 안 맞는다는 사실이 우리 해석을 뒷받침했다.
- **실패한 검증에서도 발견은 나온다.** 시험 3의 무상관은 α에 대한 결론을 바꾸지 못했고, 대신 "측정 자체가 연구마다 잘 안 맞는다"는 별도의 사실을 남겼다.

## 결론

심사자가 던질 세 가지 반론을 우리 손으로 먼저 시험했다. 값을 다 풀어도 α와 시간차의 순서는 그대로였고(시험 1), 정답을 아는 데이터는 시간차 불일치가 조건 탓임을 보였다(시험 2). 두 번째 외부 근거는 얻지 못했지만, 실패의 원인까지 적어 남겼다(시험 3). 세 결과 모두 `results/FINDINGS.md` §8~§10에 들어갔다. 다음은 이 분석들을 논문 본문과 그림으로 옮기는 일이다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 시간차 (lag) | DNA가 열리고 나서 유전자가 켜지기까지의 간격 |
| 전사 속도 (α) | 유전자가 켜졌을 때 RNA를 만드는 빠르기 |
| 일치도 ρ | 두 프로그램의 값이 얼마나 맞는지(−1~+1). +0.7 이상이면 "잘 맞음", 음수면 반대 방향 |
| SNR (신호 대 잡음비) | 신호가 잡음보다 얼마나 큰지 |
| 양성대조 (positive control) | 정답을 아는 데이터로 방법이 정답을 맞히는지 확인하는 시험 |
| freed-nuisance | 고정해 두었던 다른 값들을 모두 풀어 다시 맞추는 재검증 |

## 참고

근거: `results/FINDINGS.md` §8~§10, `results/profile_likelihood_freed.csv`, `results/sim_positive_control_multimethod.md`, `results/external_rate_validation_schwalb.md`.

*진행 중 연구의 내부 정리이며, 수치는 현재 분석 기준이라 후속 검증으로 갱신될 수 있다(연구·교육용).*

---

# Attacking our own result — three hardening analyses, before the reviewers

> TL;DR: We pre-tested our conclusion with the three objections a reviewer would raise. Two held; one did not go our way. We wrote up the failure as it was.

## 0. Core concepts

This series pictures a cell using a gene as opening a drawer and reading the document inside.

- **Chromatin opening** (chromatin, the thread of wound DNA): opening the drawer. Measured by ATAC.
- **Transcription rate α**: the reading speed. How fast a gene, once on, makes RNA.
- **The lag**: the time from opening the drawer to reading it. The gap between DNA opening and the gene turning on.

Our conclusion is short.

```
lag  ── change the program ──▶ value shifts   (not reproduced, |ρ|≤0.08)
γ    ── change the program ──▶ value shifts   (not reproduced, ρ≈−0.1)
α    ── change the program ──▶ value holds     (reproduced,     ρ 0.88)
```

The first version of this post left out that more than the lag failed to reproduce. The degradation rate γ also shifts when the program changes (ρ≈−0.1), and against external measurement (K562 half-lives) all three programs missed. Textbook scVelo's γ came out reversed in direction (−0.224, CI excluding zero). α is the one that reproduces.

ρ is how well two programs' values match, from **−1 to +1**. Above +0.7 is "a good match," near 0 is "no relation," and negative means opposite directions. So α (0.88) matches well; the lag (|ρ|≤0.08) essentially does not.

One clarification. "The lag does not reproduce across programs" is not "chromatin is meaningless." The chromatin signal itself is real in the data — the per-gene correlation between the chromatin layer and spliced RNA is +0.126, and it collapses to +0.021 when ATAC is shuffled. What is lost is not the data but **the lag the model extracts from it**.

We do, however, withdraw the original sentence here — "within one program the lag carries signal" — because our own sharpest self-criticism points the other way. **Shuffling ATAC within lineage and re-fitting the model left the lag distribution statistically unchanged** (Mann–Whitney p=0.20, per-gene rank ρ=0.72). If destroying the chromatin signal does not move the lag, then the lag is produced by **model structure** (the monotone ordering of switch times), not by chromatin. Sign agreement sitting at 54.6%, right against chance, says the same thing. The accurate statement is not "within one program there is signal" but rather: **even the lag a single program emits should not be read as evidence about chromatin.**

## Why attack ourselves

Once a conclusion stands, reviewers push back, and they do not take a result we like at face value. So we wrote down their objections and tested them ourselves first. Three of them.

```
① Isn't it a picture you forced by fixing other quantities?   → Test 1
② Can the methods even recover a lag at all?                   → Test 2
③ The claim that α matches real data rests on one source?      → Test 3
```

## Test 1: free every knob (freed-nuisance)

Which is "sharper," α or the lag, is measured by how steeply the score (how well the fit matches the data) drops when you nudge the value. A steep drop means the data pin it down; barely any change means it is blurry. In the earlier analysis α was sharp and the lag was blurry.

The reviewer asks: the computation held other quantities fixed (decay rates β·γ, the chromatin-opening rate α_c) like locked knobs — maybe that locking is what made the lag look blurry.

So we unlocked every knob, re-fit, and reran the same computation over hundreds of genes.

```
knobs fixed → α is 3.53× sharper than the lag  (α sharper in 94.57% of genes)
knobs freed → α is 2.49× sharper than the lag  (α sharper in 77.03% of genes)
```

Freeing them did not flip the order: α stays sharper than the lag. One caveat — freeing the knobs shrank α's own sharpness (to 0.19× of the fixed case). So we treat 3.53× as an upper bound and 2.49× as the conservative lower value, and write the conservative side in the paper. That answers the first objection.

## Test 2: a mock exam with a known answer key (positive control)

The second objection cuts deeper. What if the programs disagree on the lag not because of the data but because the methods cannot recover a lag at all?

To tell these apart you need data whose answer you know. So we built synthetic data with a lag we planted ourselves — a mock exam with the answer key. We varied two conditions: how large the signal is versus noise (SNR), and how sharp the transition is. In each, we checked whether two different programs (MoFlow, MultiVelo) hit the answer.

```
strong signal (SNR 20) │ mean +0.242, best corner +0.454  ◀ the recoverable corner
mid signal    (SNR 6)  │ mean -0.035
weak signal   (SNR 2)  │ mean -0.005                       ◀ where real data live
```

Only in the narrow corner of strong signal and moderately sharp transition did the two programs agree with each other and hit the answer. As the signal weakened, the agreement collapsed to 0. Real HSPC data live in that weak-signal corner.

So the regime the data sit in accounts for much of why the programs disagree on the lag. (The original blanket exoneration — "not a flaw of the methods" — went too far: in the same study we did find method-side flaws, a sign reversal and a 0.06× magnitude collapse in CRAK-Velo's lag estimator. There were flaws; they just do not on their own explain the disagreement.) The mock exam shows that the earlier lag non-agreement in the real data was not a computation failure but a regime where the lag simply cannot be pinned down.

One thing not to misread: the recoverable corner is very narrow. It holds only at signal level 20, and per gene that is unrealistically high for real data. So the result strengthens, not softens, the claim that real data live where the lag cannot be recovered.

We added a power check. Planting signals of known size, we saw whether our test catches them. An agreement around 0.15 was caught most of the time (power ≥0.8), and the real lag agreement (≤0.08) is below that floor. On the **magnitude** axis, then, "no signal above what the test can catch" is the right statement.

**But the sentence we appended here — that "0 of 598 genes agreeing" is not an impotent test — was wrong, and we correct it.** That 0/598 is a test of **direction**, not magnitude, and the direction test genuinely is power-bounded: with only two clean sign-variable programs (MoFlow, MultiVeloVAE) the smallest achievable per-gene p is about 0.5 (measured: 0.499), so no gene can clear any FDR threshold whether or not signal exists. The 598-gene version also borrows CRAK-Velo as its third program, so it rests on CRAK. The manuscript has since moved 0/598 out of the headline and into a CRAK-inclusive sensitivity analysis. Using this point as a defence in a self-adversarial post was this post's worst error.

## Test 3: a second ruler, and a failure (Schwalb)

The third test did not go our way.

As evidence that α matches real measurements, we had cited one external measurement (Todorovski, K562 TT-seq). Per-gene α ranked with it at +0.24~+0.29. The problem is that there was only one. So we attached a second independent measurement of the same cell (Schwalb 2016) by the same method.

It did not match.

```
our α ── ruler 1 (Todorovski) : +0.24~+0.29   matches
our α ── ruler 2 (Schwalb)    : −0.05~−0.01   no match
ruler 1 ── ruler 2            : +0.154        the two rulers barely agree
```

The cause: the two measurements themselves disagreed. For the same cell and same experiment, the two rulers overlapped at only 0.15. If two rulers disagree, no value can match both. That sets the ceiling on external confirmation. We checked it was not a coordinate-join error — the check passed. The mismatch is real.

How to read this matters. This non-match is not evidence that α fails to match measurements. The measured cells differ from the cells we computed, absolute α is not sharply set, and this second measurement is itself noisy. The precise finding is that "TT-seq synthesis-rate measurement itself reproduces poorly between studies (0.15)," and that is the limit of external confirmation. So the "one source only" weakness was not removed by this source. Ruler 1's match stands; ruler 2 gives neither reproduction nor refutation.

We wrote it up plainly even though it landed flat. Trying for a second source and failing — and pinning the failure on the measurement's own reproducibility, not our computation — is what this round yielded.

## What we learned

- **Report a defense's limits alongside it.** Test 1 met the objection but also exposed that α's sharpness shrinks. We report both values and write the conservative side.
- **A mismatch can be the signal.** Test 2 showed "the lag can't be recovered" is a matter of regime, not a flaw. The very mismatch supported our reading.
- **A failed validation is also a finding.** Test 3's non-match did not shake α; it left a separate fact — that the measurement itself reproduces poorly between studies.

## Conclusion

We tested the three reviewer objections ourselves first. Freeing every knob kept the order intact (Test 1); data with a known answer showed the lag disagreement to be a matter of regime (Test 2). The second external source did not come through, but we recorded why (Test 3). All three went into `results/FINDINGS.md` §8~§10. Next is moving them into the paper's main text and figures.
