# 헤드라인이 될 뻔한 우리 발견을, 더 센 검정으로 스스로 되돌린 이야기

> 한 줄 요약: 우리 결과를 두 번 더 공격했다. 하나는 논문 헤드라인으로 밀어 봤지만 더 센 검정에서는 아직 아니라는 결과가 나왔고 하나는 우리가 세게 말하던 주장을 깎았다. 둘 다 나온 대로 적었다.

## 0. 핵심 개념

이 시리즈에서 세포가 유전자를 쓰는 일을 서랍에서 서류를 꺼내 읽는 데 빗대 왔다.

- **크로마틴 열림**(chromatin): 서랍을 여는 일. ATAC로 측정한다.
- **전사 속도 α**(transcription rate): 꺼낸 서류를 읽는 속도.
- **시간차 lag**: 서랍을 연 뒤 서류를 읽기까지의 간격.

이번 글엔 값이 네 개 나온다. 계산 프로그램은 유전자 하나를 맞출 때 이 네 속도를 동시에 정한다.

```
α    전사 속도       — 서류를 읽는 속도
α_c  크로마틴 여는 속도 — 서랍을 여는 속도
β    가공 속도        — 읽은 내용을 다듬는 속도
γ    분해 속도        — 다 쓴 서류를 치우는 속도
```

그리고 "뚜렷함"이라는 말을 지난 글에서 정의했다. 값을 살짝 흔들었을 때 점수(데이터에 얼마나 맞는지)가 급히 떨어지면 그 값은 **뚜렷하고**(데이터가 딱 정해 줌), 거의 안 변하면 **흐릿하다**(데이터가 느슨하게 둠). α는 뚜렷했고 시간차는 흐릿했다.

## 왜 또 공격하나

지난 글에서 세 가지 반론을 미리 시험했다. 이번엔 두 가지를 더 시험했는데 하나는 좋은 결과를 얻고 욕심을 냈다가 그 욕심을 스스로 꺾은 이야기다.

```
공격 A  뚜렷한 값일수록 실제 측정과 잘 맞나? 이걸 논문 헤드라인으로 쓸 수 있나?
공격 B  이름난 유전자에선 크로마틴이 시간차를 만드나? (우리 주장을 스스로 시험)
```

## 공격 A: 헤드라인으로 밀어 봤다가 스스로 물러선 곳

지금까지는 α(뚜렷함)와 시간차(흐릿함) 둘만 비교했다. 이번엔 네 값 전부의 뚜렷함을 쟀다. 유전자 506개에서 각 값을 흔들어 점수가 떨어지는 속도를 봤다.

```
뚜렷함 순위 (높을수록 뚜렷=데이터가 딱 정해 줌)
  α    전사 속도    +7.98   ◀ 가장 뚜렷
  α_c  여는 속도    +7.32
  β    가공 속도    +4.86
  γ    분해 속도    +1.72   ◀ 가장 흐릿
```

그리고 네 값 중 바깥 실험으로 진짜 답을 아는 양 끝 둘을 실제 측정과 맞춰 봤다. 가장 뚜렷한 α는 실측 합성 속도와 맞았고(+0.24~+0.29) 가장 흐릿한 γ는 거꾸로 갔다(−0.224). "뚜렷하면 맞고, 흐릿하면 안 맞는다"는 그림이었다. 우리는 이걸 논문의 첫 문장, **"모델의 뚜렷함이 어느 값을 믿어도 되는지 미리 알려준다"**는 헤드라인으로 밀고 싶었다.

그런데 이 그림을 헤드라인으로 쓰기 전에 스스로 물었다. 이게 정말 법칙일까, 아니면 점 두 개일까.

**문제는 점이 두 개라는 데 있었다.** 진짜 답을 아는 값은 α와 γ 둘뿐인데(나머지 α_c·β는 맞춰 볼 바깥 측정이 없다), 이 둘은 하필 가장 뚜렷한 값과 가장 흐릿한 값이다. **점이 두 개면 그 둘은 언제나 한 직선 위에 놓인다.** "제일 뚜렷한 게 맞고 제일 흐릿한 게 틀렸다"는 것만으로 "뚜렷함이 신뢰를 예측한다"는 법칙을 세울 수는 없다. 심사자는 한 줄로 꿰뚫을 것이다. "값 두 개 중 하나는 맞고 하나는 틀렸다, 그걸 법칙이라 부른 것뿐이다."

그래서 진짜 검정을 돌렸다. 값 **네 개를 서로 비교**하는 대신, 값 **하나를 유전자 수백 개에 걸쳐** 봤다. α는 유전자마다 진짜 합성 속도를 알기에, 유전자를 α의 뚜렷함에 따라 상·중·하 세 무리로 나누고 각 무리에서 α가 실측과 맞는 정도를 쟀다.

```
α 유전자, 뚜렷함 세 무리 (진짜 합성 속도와 맞는 정도)
  흐릿한 무리 │ +0.116  (0과 구분 안 됨)
  중간 무리   │ +0.153  (0과 구분 안 됨)
  뚜렷한 무리 │ +0.302  (0과 확실히 다름)
```

방향은 바라던 대로였다. 뚜렷한 무리일수록 실측과 잘 맞았고 가장 뚜렷한 무리만 확실한 신호를 냈다. **그런데 "뚜렷한 무리와 흐릿한 무리의 차이"를 통계로 검정하자 그 차이가 우연과 구분되지 않았다**(차이 +0.186, 95% 구간이 0을 포함). 무리당 유전자가 70개뿐이라 검정력이 부족했다. 방향은 맞지만 통계로는 아직 증명 못 한다는 뜻이다.

γ는 더 분명했다. 뚜렷함 세 무리 어디서도 실측 분해 속도와 맞는 신호가 없었다(전부 0과 구분 안 됨). 게다가 앞서 "거꾸로 갔다"던 그 −0.224는 사실 **다른 계산 프로그램의 γ**에서 나온 값이었다. 우리가 뚜렷함을 잰 프로그램의 γ는 거꾸로도 아니었다. 그냥 무신호였다. 두 값을 은근슬쩍 섞어 썼다.

그래서 결론은 이렇다. **"뚜렷함이 신뢰를 예측한다"는 헤드라인은 아직 못 쓴다.** α에서 방향은 맞지만 확증하기엔 표본이 모자라고 γ는 신호가 없다. 이건 아직 법칙은 아니다. **더 파 볼 만한 관찰**이다. 논문의 진짜 헤드라인은 따로 있다(아래 배운 점).

하마터면 점 두 개로 그은 선을 법칙이라 부를 뻔했다. 심사자에게 맞기 전에 우리 손으로 먼저 걸러 낸 것이 이번 공격 A의 성과다.

## 공격 B: 이름난 유전자에선 크로마틴이 시간차를 만들까

두 번째는 우리가 그동안 조금 세게 말하던 주장을 겨눴다.

시간차가 프로그램을 바꾸면 안 맞는다는 건 앞서 보였다. 그런데도 우리는 "그래도 CSF1R·IRF8 같은 이름난 유전자에선 크로마틴이 시간차를 실제로 만든다"고 적어 왔다. 이걸 검증할 방법이 있다. 크로마틴 신호를 유전자끼리 무작위로 뒤섞어 놓고(가짜 짝), 그래도 시간차가 그대로면 크로마틴이 시간차를 만든 게 아니다. 이름난 유전자에서만 시간차가 크게 흔들린다면, 거기선 크로마틴이 실제로 시간차를 만든 것이다.

```
전체 유전자 │ 뒤섞어도 시간차 그대로 (ρ=0.72)  ── 크로마틴이 시간차를 만들지 않음
이름난 유전자│ 뒤섞을 때 더 흔들리나?  ── 아니오 (bulk와 같음, p=0.58)
```

이름난 유전자에서도 뒤섞기가 시간차를 더 흔들지 못했다. 절대값으로는 몇 개가 크게 움직이는 듯 보였지만 원래 시간차가 큰 유전자가 더 흔들리는 편향을 걷어 내자 이름난 유전자의 흔들림은 전체 평균과 같았다. 검정에서 오히려 살짝 작았다.

그래서 "이름난 유전자에선 크로마틴이 시간차를 인과적으로 만든다"는 주장을 **상관으로 낮췄다.** 이름난 유전자에서 프로그램 간 시간차 방향이 얼추 맞는 건 사실이다. 다만 그건 상관일 뿐이고 크로마틴이 원인이라는 증거는 여기서 나오지 않는다. 오히려 우리 핵심 음성 결론("시간차는 크로마틴이 아니라 모델 구조에서 온다")은 이름난 유전자에서마저 더 깨끗해졌다.

이 공격은 우리에게 불리했다. 그래도 나온 대로 적고 논문의 그 문장을 고쳤다. 이 시리즈 5편에서 "크로마틴 선행은 특정 유전자 자리에서는 실재한다"고 적었던 문장도 이 결과에 맞춰 "방향 일치는 상관이지 크로마틴이 시간차를 만든다는 인과는 아니다"로 갱신했다.

## 그리고 한 가지 더: 이걸로 다른 논문 하나가 될까

공격 A의 방향이 그럴듯하자 욕심이 생겼다. 기저 상태에서 전사 속도 α로 이어지는 경로를 유전자 지도로 그려서, 약물 반응 타이밍을 예측하는 별도 논문으로 키울 수 있을까. 원래 이 연구는 "시간차로 약물 반응을 예측한다"는 가설로 시작했으니 자연스러운 방향이었다.

우리 손에 있는 유일한 약물 데이터로 맞춰 봤다. 결과는 밋밋했다. 약물 반응과 α·크로마틴·시간차가 다 무관하게 나왔다.

원인은 시간 눈금이 안 맞아서였다. 그 약물 실험은 5일·14일 뒤를 쟀는데 우리가 다루는 크로마틴 기전은 몇 시간·몇 분 단위로 움직인다. 며칠이 지나면 그 빠른 신호는 벌써 여러 번 지워진 뒤다. 처음의 α 차이가 약물 반응에 남아 있을 리 없다. 눈금 단위가 다른 자로는 그 차이를 잴 수 없다.

원인이 하나 더 있다. 애초에 이 지도를 그릴 근거였던 "처리 전 크로마틴이 α를 예측한다"는 결과(학습에 쓰지 않은 계통에서 ρ=+0.309, 6개 계통 모두 양수) 자체가 나중에 무너졌다. 발현량만으로 맞춰 보니 ρ=+0.724가 나왔고, 거기에 크로마틴을 더해도 성능이 −0.016만큼 오히려 줄었다. 발현량을 통제하면 크로마틴 몫은 ρ=+0.112만 남는다. 사람 뇌 데이터에서는 +0.212에서 +0.013으로 아예 사라졌다. 그래서 우리는 "크로마틴이 α를 예측한다"는 표현을 원고에서 지우고 "기저 상태에서 α로"라고만 쓴다. 별도 논문을 막은 것은 시간 눈금만이 아니었다.

그래서 이건 지금 데이터로는 별도 논문이 못 된다. 대신 방법 논문 안의 응용 예시로 넣고 "제대로 검증하려면 몇 시간 단위로 재는 교란 실험이 다음 실험"이라고 그대로 적는다. 없는 결과를 있는 척 부풀리지 않는다.

## 배운 점

- **점 두 개만으로는 법칙을 세우지 못했다.** 뚜렷함과 신뢰의 관계는 진짜 답을 아는 값이 둘뿐이라 점 두 개였다. 값 하나를 유전자 수백 개에 걸쳐 다시 보니, 방향은 맞아도 통계로는 아직 못 증명했다. 그래서 헤드라인에서 뺐다.
- **우리 주장을 스스로 겨눈 공격이 가장 도움이 됐다.** 공격 B는 우리에게 불리했지만 그 덕에 과하게 말하던 문장을 상관으로 낮췄고 핵심 결론은 더 단단해졌다.
- **좋은 결과에 욕심이 났지만, 근거가 발현량 교란이었고 시간 눈금도 맞지 않았다.** 데이터가 답할 수 없는 질문은 답할 수 없다고 적는다.

그럼 논문의 진짜 헤드라인은 무엇인가. **전사 속도 α는 프로그램을 바꿔도 값이 그대로일 뿐 아니라(재현), 실제 측정한 합성 속도와도 맞는(외부 검증) 유일한 값**이다. 시간차와 분해 속도는 둘 다 못 한다. 그러니 우리가 내놓을 것은 "곡률이 신뢰를 예측한다"는 법칙이 아니다. 바로 **어느 velocity 값을 믿고 어느 값은 따로 검증해야 하는지를 표시한 신뢰 지도**다. 이건 이번 두 공격과 무관하게 이미 단단히 서 있다.

다만 여기에는 단서가 붙는다. α가 실측 합성 속도와 맞는 정도(ρ=+0.262)는 그냥 발현량으로 맞춘 것(ρ=+0.410)보다 오히려 낮다. 그래서 우리 결론은 "α를 믿어라"가 아니라 "발현량 기준선과 견주어 α를 믿어라"다. 지금까지의 근거로는 α가 발현량 이상의 정보를 준다고 말할 수 없다.

이 외부 검증은 아직 측정 소스 하나(Todorovski TT-seq)에 걸려 있다. 두 번째 소스(Schwalb)에서는 세 방법 모두 무신호였고, 두 실측 소스끼리도 ρ≈0.15 정도로만 맞는다. 잣대 자체의 재현성이 상한인 셈이다.

## 결론

우리 결과를 두 번 더 공격했다. 하나(공격 A)는 논문 헤드라인으로 밀어 봤지만 더 센 검정에서 α는 방향만 맞았고 아직 증명은 안 됐으며 γ는 신호도 없었다. 하나(공격 B)는 우리가 세게 말하던 주장을 상관으로 낮추게 했다. 곁가지로 "별도 논문이 될까"도 물었지만 지금 데이터로는 아니었다. 세 결과 모두 `results/`에 그대로 들어갔다. 논문의 헤드라인은 법칙이 아니다. 신뢰 지도로 간다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 전사 속도 (α) | 유전자가 켜졌을 때 RNA를 만드는 빠르기 |
| 분해 속도 (γ) | 다 쓴 RNA를 치우는 빠르기 |
| 시간차 (lag) | DNA가 열리고 나서 유전자가 켜지기까지의 간격 |
| 뚜렷함 (곡률/식별성) | 값을 흔들 때 점수가 급히 떨어지는 정도. 클수록 데이터가 그 값을 딱 정해 줌 |
| 실측 합성/분해 속도 | 바깥 실험(TT-seq 등)으로 직접 잰 진짜 속도, 우리 계산값을 맞춰 보는 잣대 |
| 검정력 | 진짜 차이가 있을 때 그걸 통계로 잡아낼 수 있는 힘. 표본이 적으면 부족해진다 |

## 참고

근거: `results/curvature_tertile_validation.md`(공격 A 판별 검정), `results/marker_shuffle_teeth_test.md`(공격 B), `results/external_rate_validation.md`, `results/stiffness_predicts_validation.md`.

*진행 중 연구의 내부 정리다. 수치는 현재 분석 기준이라 후속 검증으로 갱신될 수 있다(연구·교육용).*

---

# How we walked back our own would-be headline with a harder test

> TL;DR: We attacked our result twice more. One we tried to push as the paper's headline, but a harder test said "not yet"; the other made us walk back a claim we had stated too strongly. We wrote up both as they landed.

## 0. Core concepts

This series pictures a cell using a gene as opening a drawer and reading the document inside.

- **Chromatin opening** (chromatin): opening the drawer. Measured by ATAC.
- **Transcription rate α**: the reading speed.
- **The lag**: the gap from opening the drawer to reading it.

This post has four values. When the program fits one gene, it sets all four speeds at once.

```
α    transcription rate  — the reading speed
α_c  chromatin-open rate — the drawer-opening speed
β    processing rate      — the speed of trimming what was read
γ    degradation rate     — the speed of clearing a used-up document
```

And "sharpness," defined last time: nudge a value, and if the score (how well the fit matches the data) drops steeply, the value is **sharp** (the data pins it down); if it barely moves, it is **blurry** (the data leaves it loose). α was sharp; the lag was blurry.

## Why attack again

Last time we pre-tested three objections. This time we ran two more — and one is the story of getting a good result, getting ambitious, and reining that ambition in ourselves.

```
Attack A  Do sharper values match real measurement better? Can we headline that?
Attack B  At named genes, does chromatin make the lag? (testing our own claim)
```

## Attack A: where we pushed for a headline and then backed off

So far we had compared only α (sharp) and the lag (blurry). This time we measured the sharpness of all four values, across 506 genes, by how fast the score falls when each is nudged.

```
Sharpness ranking (higher = sharper = pinned down by data)
  α    transcription rate  +7.98   ◀ sharpest
  α_c  opening rate        +7.32
  β    processing rate     +4.86
  γ    degradation rate    +1.72   ◀ blurriest
```

Then we matched the two extremes — the only two with real external answers — against measurement. The sharpest, α, matched measured synthesis rate (+0.24~+0.29); the blurriest, γ, ran backwards (−0.224). "Sharp matches, blurry doesn't." We wanted to make this the paper's opening line: **the model's sharpness tells you in advance which value to trust.**

But before headlining it we asked ourselves: is this a law, or is it two dots?

**It was two dots.** Only α and γ have known answers (α_c and β have no external measurement to check), and those two happen to be the sharpest and the blurriest. **Two dots always fall on a straight line.** "The sharpest matched and the blurriest missed" cannot, by itself, establish that sharpness predicts trust. A reviewer would puncture it in one line: "two values, one matched, one didn't — you just relabeled that a law."

So we ran the real test. Instead of comparing four values (only two anchored), we took one value across hundreds of genes. Since α has a real synthesis rate per gene, we split genes into sharp/mid/blurry thirds by α-sharpness and measured how well α matched measurement in each third.

```
α genes, three sharpness thirds (match to real synthesis rate)
  blurry third │ +0.116  (not distinct from 0)
  mid third    │ +0.153  (not distinct from 0)
  sharp third  │ +0.302  (clearly above 0)
```

The direction was what we hoped: sharper thirds matched better, and only the sharpest third gave a clear signal. **But when we tested the difference between the sharp and blurry thirds, it was not distinguishable from chance** (difference +0.186, 95% interval includes 0). With only 70 genes per third, the test lacked power. The direction is right, but the statistics do not yet prove it.

γ was clearer still. None of the three sharpness thirds matched measured decay (all indistinguishable from 0). And that "−0.224 backwards" from before was actually from **a different program's γ**. The γ of the program whose sharpness we measured was not backwards, just null. We had quietly mixed two values.

So the conclusion: **"sharpness predicts trust" is not a headline we can write yet.** For α the direction holds but the sample is too small to confirm; for γ there is no signal. This is not a law but an observation worth digging into further. The paper's real headline lies elsewhere (see below).

We nearly called a line through two dots a law. Catching it ourselves, before a reviewer did, is what Attack A actually bought us.

## Attack B: at named genes, does chromatin make the lag?

The second attack aimed at a claim we had stated a bit too strongly.

We had shown the lag does not match across programs. Yet we kept writing that "still, at named genes like CSF1R and IRF8, chromatin really does make the lag." There is a way to test this. Scramble the chromatin signal randomly across genes (fake pairings); if the lag stays put, chromatin did not make it. If the lag shakes hard only at named genes, chromatin was doing real work there.

```
all genes   │ lag unchanged under scrambling (ρ=0.72)  ── chromatin does not make the lag
named genes │ shaken more under scrambling?  ── no (same as bulk, p=0.58)
```

At named genes too, scrambling failed to shake the lag any more than elsewhere. A few looked large in absolute terms, but once we removed the bias that high-lag genes shake more, the named genes' movement equaled the overall average — slightly smaller, by the test.

So we **downgraded to correlation** the claim that "at named genes chromatin causally makes the lag." That the cross-program lag direction roughly agrees at named genes is real, but the "roughly" runs only 54.6% (560 genes, p=0.031) against a coin flip, and in magnitude most of it sits at |ρ|≤0.08 — statistically detectable, practically negligible. And that is correlation, not evidence chromatin is the cause. If anything, our core negative conclusion — the lag comes from model structure, not chromatin — got cleaner, holding even at named genes. Post 5 of this series, which had said "chromatin-leading is real at specific loci," was likewise updated to "the direction-agreement is a correlation, not evidence that chromatin makes the lag."

## And one more: could this be its own paper

When Attack A's direction looked promising, we got ambitious. Could we draw a gene-level map of the baseline-to-α path and grow it into a separate paper predicting drug-response timing? This study began from the hypothesis that the lag predicts drug response, so it was a natural direction.

We matched it against the only drug data we have. The result was flat: drug response was unrelated to α, chromatin, and the lag alike.

The cause was a scale mismatch. That drug experiment measured 5 and 14 days out, while the chromatin mechanism we study moves over hours and minutes. After days, the fast signal has been overwritten many times over, so any initial α difference cannot survive in the drug response. A ruler with the wrong graduations measures nothing.

There was a second reason. The result that motivated the map in the first place — that baseline chromatin predicts α (held-out lineages, ρ=+0.309) — did not survive. Abundance alone reached ρ=+0.724, adding ATAC changed it by −0.016, and controlling for abundance left ATAC at ρ=+0.112. In human brain the same signal fell from +0.212 to +0.013. We therefore removed "chromatin predicts α" from the manuscript and now write only "baseline-to-α". It was not the time-scale alone that stopped the separate paper.

So the conclusion: with current data this is not a separate paper. Instead it goes in as an application example inside the methods paper, with an honest note that "validating it properly needs a perturbation experiment measured on the scale of hours — the next experiment." We do not inflate an absent result into a present one.

## What we learned

- **Don't write two dots up as a law.** The link between sharpness and trust rested on only two values with known answers — two dots. Taking one value across hundreds of genes, the direction held but the statistics did not yet prove it. So we cut it from the headline.
- **The attack on your own claim is the most valuable.** Attack B went against us, but it let us downgrade an overstated sentence to correlation, and the core conclusion got firmer.
- **The more tempting the result, the harder you check the ruler.** The dream of a separate paper rested on an abundance confound, and the time scale did not match either. A question the data cannot answer, we write up as unanswerable.

Then what is the paper's real headline? **Transcription rate α is the only value that both holds when you change the program (reproduces) and matches the measured synthesis rate (external validation).** The lag and the degradation rate do neither. So what we offer is not a law that "curvature predicts trust," but a **reliability map showing which velocity values to trust and which to validate separately.** That stands firm regardless of these two attacks.

One caveat belongs here. α matches the measured synthesis rate at ρ=+0.262, but plain abundance matches it better, at ρ=+0.410. So our conclusion is not "trust α" but "trust α against an abundance baseline"; on present evidence α adds no demonstrable information beyond expression.

This external check still rests on a single measured source (Todorovski TT-seq). A second source (Schwalb) was null in all three methods, and the two measured sources agree only at ρ≈0.15 — the reproducibility of the ruler itself is the ceiling.

## Conclusion

We attacked our result twice more. One (Attack A) we pushed toward a headline, but a harder test turned it back — "α has the right direction but no proof yet, γ has no signal at all." One (Attack B) made us downgrade an overstated claim to correlation. On the side we asked whether it could be a separate paper; with current data, not yet. All three went into `results/`. The paper's headline goes to a reliability map, not a law.
