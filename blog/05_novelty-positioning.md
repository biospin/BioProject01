# 이 발견을 이미 누가 했다면 — 선행연구와 논문의 자리매김

> 한 줄 요약: "유전자별 시간차는 프로그램을 바꾸면 재현되지 않는다"는 우리 발견이 이미 나온 것은 아닌지 먼저 확인했다. 가장 가까운 선행연구인 MoFlow는 일부 유전자에서 프로그램끼리 시간차가 맞는다고 사후에 보고했지만, 우연을 거르는 장치도 인과를 확인하는 대조도 없었다. 우리에게는 그 둘이 있다. 그래서 이 연구는 부분적으로 앞서 나온 관찰 위에 있으면서도, 논문으로 낼 만한 새로움이 남는다.

세포 하나에서 유전자 발현과 크로마틴(chromatin, DNA가 감긴 실타래) 열림을 동시에 읽게 되면서, 우리는 크로마틴이 열리는 순서로 전사를 예측할 수 있는지를 묻는 연구를 해 왔다. 그 예측 재료로 삼으려던 "DNA가 열리고 나서 유전자가 켜지기까지의 시간차(lag)"를 앞 글들에서 검증했고, 그 값이 계산 프로그램을 바꾸면 재현되지 않는다는 결론에 이르렀다. 반대로 전사 속도(α, 유전자가 켜졌을 때 RNA를 만드는 빠르기)는 프로그램을 바꿔도 값이 일정했다. 그런데 결론을 아무리 여러 번 검증해도 남는 물음이 하나 있다. 이 발견을 이미 누군가 해 놓지는 않았는가. 그렇다면 우리 연구는 논문이 될 수 있는가.

이 글은 그 물음에 답한 기록이다. 무엇을 찾아봤고, 가장 비슷한 앞선 연구가 무엇을 어디까지 말했으며, 그에 견줘 우리에게 무엇이 남는지를 정리한다.

## 선행연구 확인이라는 관문

새 발견을 논문으로 내기 전에는, 같은 발견이 이미 나와 있는지 문헌을 뒤져 확인한다. 남이 먼저 발표한 결과를 모르고 다시 발표하는 일을 학계에서는 스쿱(scoop, 같은 발견을 남에게 선점당함)이라 부른다. 스쿱을 당하면 아무리 공들인 분석도 새 기여로 인정받기 어렵다. 그래서 이 확인은 분석만큼이나 중요한 관문이다.

확인은 두 갈래로 나눠서 한다. 하나는 "우리가 내린 바로 그 결론을 주제로 삼은 논문이 있는가"이고, 다른 하나는 "그 결론의 재료가 되는 관찰을 지나가듯 보고한 논문이 있는가"이다. 앞의 것이 있으면 스쿱이지만, 뒤의 것만 있으면 우리가 얹을 새로움이 남는지를 따져 봐야 한다.

```
발견: "유전자별 시간차는 프로그램마다 다르다"
   │  이미 누가 한 발견인가?
   ├─ 이걸 주제로 삼은 논문          → 없음
   ├─ 일반 velocity 벤치마크(2026)   → 방향은 채점, 시간차는 안 봄
   └─ 가장 가까운 선행 MoFlow        → "맞는 유전자 묶음" 사후 보고
                                         (우연 검정·인과 대조 없음)
   ↓
우리만의 근거 둘
   ① ATAC 뒤섞기 인과 대조 → 시간차 불변 = 크로마틴 아닌 모델 구조
   ② α 튼튼(ρ=0.88) / 시간차 약함(ρ≈0)의 해리
   → 판정: 논문거리(GO), 스쿱 위험 낮음~중간
```

## 찾아본 것과 찾지 못한 것

먼저 "프로그램끼리 시간차가 다르다"는 것을 주제로 내건 논문을 찾았다. 크로마틴을 함께 쓰는 velocity(세포 이동 방향 추정) 프로그램들이 유전자별 시간차에서 서로 엇갈린다는 사실을 연구의 중심 주제로 삼은 논문은 없었다. 시간차의 프로그램 간 일치도를 연구 대상으로 놓고 따진 사례가 없다는 뜻이다.

2026년에 나온 큰 규모의 velocity 벤치마크가 셋 있는데, 우리 연구에 인접하지만 겹치지는 않는다. 첫째는 RNA만 쓰는 프로그램 15종을 17개 데이터에서 견주며 velocity 방향의 정확도와 안정성을 채점했고, 둘째는 29종을 176개 데이터에서 견주며 MultiVelo까지 포함했다. 셋째는 2026년에 추가로 나온 것으로 19개 도구·30개 방법을 34개 데이터에서 8개 과제로 채점한, 현재 최대 규모다. 셋 다 저차원 임베딩에서 velocity **벡터**를 채점했을 뿐, 유전자별 시간차의 일치도도 프로그램 간 velocity 행렬 비교도 다루지 않았다. 곧 이들은 "어느 방향으로 세포가 움직이는가"를 물었고, 우리는 "크로마틴과 RNA 사이의 시간차가 프로그램을 바꿔도 같은 값인가"를 묻는다. 던지는 물음 자체가 다르다.

## 가장 가까운 선행: MoFlow

문헌에서 우리 발견에 가장 가까이 다가온 것은 MoFlow(Hong et al. 2025)다. MoFlow는 크로마틴 신호와 RNA 신호를 나란히 맞대어 시간차를 재는, 계보가 다른 프로그램이다. 이 논문은 자기 방법을 소개하면서, 크로마틴이 먼저 열리는(음의 시간차) 유전자들의 묶음에서 MultiVelo와 자기 방법이 대체로 일치한다고 지나가듯 보고했다.

이 대목이 우리와 가장 겹친다. 크로마틴을 쓰는 두 프로그램의 유전자별 시간차를 실제로 맞대 본 결과가, 심사를 거친 논문에 이미 실려 있는 것이다. 그래서 이 부분은 정면으로 인용하고 우리 위치를 분명히 갈라 둬야 한다.

다만 MoFlow의 보고는 성격이 다르다. 그것은 자기 방법이 잘 맞는 유전자 묶음을 사후에 골라 "여기서는 두 방법이 일치한다"고 보인, 유리한 부분집합 위의 확인이다. 유전자 수천 개에서 우연히 맞아 보이는 것을 걸러 내는 통계도, 그 일치가 실제로 크로마틴에서 나온 것인지 확인하는 대조도 없었다. 우리가 던지는 물음은 그 일치가 재현되는지, 그리고 크로마틴이 만든 것인지인데, MoFlow는 그 둘을 시험하지 않았다.

![가장 가까운 선행연구 MoFlow와의 비교: 일부 유전자에서 프로그램 간 시간차 일치를 사후 보고한 점은 공통(✓)이지만, 우연을 거르는 permutation FDR과 크로마틴을 뒤섞는 음성대조는 MoFlow엔 없고(✗) 우리에겐 있다(✓).](../pipeline/hspc-velocity-benchmark/figures/fig03_novelty_comparison.png)

## 우리만의 근거 ①: ATAC 뒤섞기 인과 대조

우리가 MoFlow와 뚜렷이 갈리는 첫 지점은 인과를 시험하는 음성 대조군(negative control)이다. 시간차가 정말 크로마틴에서 나온 값인지 보려고, 같은 계통 안에서 크로마틴과 RNA의 짝을 의도적으로 어긋나게 섞었다. 어떤 세포의 RNA에 같은 계통의 엉뚱한 다른 세포 크로마틴을 붙이는 식인데, 이때 각 값의 전체 분포는 그대로 두고 세포 안에서의 연결만 끊는다. 시간차가 크로마틴에서 나온 값이라면, 이렇게 연결을 끊었을 때 시간차도 크게 달라져야 한다.

그런데 달라지지 않았다. MultiVelo가 낸 시간차 분포는 연결을 끊기 전과 통계적으로 거의 같았고(분포 차이 검정 p=0.20), 유전자별 시간차 상관도 ρ=0.72로 보존됐다. 크로마틴을 뒤섞어도 시간차가 그대로였다는 것은, 그 시간차가 크로마틴 신호가 아니라 프로그램 내부의 전환 시점 정렬 구조에서 나온 값이라는 뜻이다.

이것은 "프로그램끼리 답이 다르다"는 관찰과는 성격이 다른 주장이다. 프로그램을 비교한 데서 한 걸음 더 들어가, 그 시간차가 어디서 오는지를 인과로 짚었기 때문이다. 이 시간차를 만든 것은 크로마틴이 아니라 모델 구조라는 점을, MoFlow를 포함해 어느 경쟁 논문도 대조로 확인하지 않았다. 이것이 우리 자리를 지켜 주는 첫 번째 근거다.

## 우리만의 근거 ②: α의 재현성과 시간차의 비재현성

두 번째 근거는 같은 파이프라인에서 나온 대비다. 시간차는 프로그램을 바꾸면 재현되지 않았지만(일치도 ρ이 0 근처), 전사 속도 α는 프로그램을 바꿔도 값이 잘 맞았다(ρ=0.88). 순위 일치도 ρ은 −1에서 +1 사이의 값으로, 보통 0.7을 넘으면 "잘 맞는다"고 본다. 그 잣대로 보면 0.88은 잘 맞는 값이고, 0 근처의 시간차는 상관 관계가 없다. 같은 데이터와 같은 전처리를 거쳤는데도 어떤 값은 재현되고 어떤 값은 사라진다는 이 갈림이 두 번째 근거다.

여기에 더해, 처리 전 day0 정보만으로 학습에 쓰지 않은 계통의 α를 어느 정도 맞힐 수 있었다(ρ=+0.31, 6개 계통 모두 양수). 같은 재료로 시간차는 맞히지 못했다. **다만 이 예측을 해내는 것은 크로마틴이 아니다.** 이 글을 처음 쓸 때는 크로마틴의 공으로 적었으나, 이후 검증에서 발현량 교란으로 판명됐다 — 발현량만으로 예측하면 +0.724가 나오고 크로마틴을 더하면 오히려 +0.708로 내려간다(증분 −0.016). 지금 원고는 이를 "크로마틴에서 α로"가 아니라 "기저 상태에서 α로"라고 적는다. 이 연구의 핵심은 어차피 α가 프로그램을 바꿔도 재현되는 값이라는 점이고, 예측 가능성은 부차적이다.

이 대비가 왜 중요한가. α가 잘 맞는다는 사실만 떼어 놓고 보면 "전사 속도는 원래 추정하기 쉬운 값"이라는 당연한 이야기로 들린다. 이 사실이 의미를 얻는 것은 시간차와 나란히 놓일 때다. 크로마틴과 무관하게 모델이 만들어 낸 시간차는 프로그램마다 값이 달라지는데, 바로 그 옆에서 α는 재현된다. 어떤 계산 결과는 믿을 수 있고 어떤 것은 그렇지 않은지, 이 대비가 핵심이다. 방법 논문들은 시간차를 생물학적 발견으로 앞세우면서 바로 이 대비를 빠뜨렸다.

## 반증 대상: 크로마틴 포텐셜 가설

우리 발견으로 오래된 생물학 가설 하나를 시험한다. Ma et al.(2020)의 크로마틴 포텐셜(chromatin potential) 가설이다. 세포가 운명을 정해 갈 때 유전자 주변 크로마틴이 발현보다 먼저 열린다는, 곧 크로마틴이 유전자를 미리 준비시킨다는 생각이다. 앞 글에서 다룬 chromatin priming과 같은 계열의 주장이고, 우리가 시간차를 예측 재료로 삼으려 한 출발점이기도 했다.

우리 데이터는 이 가설을 유전자 하나하나의 수준에서 시험한다. 집단 전체로 보면 크로마틴이 먼저인 유전자와 RNA가 먼저인 유전자가 대략 반반이라, "언제나 크로마틴이 먼저"라는 전역적 주장은 사람 조혈세포에서 유전자별로는 지지받지 못한다. 다만 교과서적 표지 유전자들은 프로그램을 바꿔도 크로마틴이 먼저 열리는 쪽으로 방향이 대체로 일치한다. 그래서 우리 결론은 크로마틴 포텐셜을 통째로 부정하는 데까지 가지 않는다. 이 방향 일치는 상관이다 — 뒤에 크로마틴 신호를 뒤섞는 인과 대조로 시험해 보니, 이름난 유전자에서도 크로마틴이 시간차를 더 흔들지는 못했다(후속 글에서 다룬다). 그러니 방향 일치는 실재하되, 크로마틴이 그 시간차를 만든다는 인과까지는 우리 데이터가 뒷받침하지 않는다. 유전자 전체에서 프로그램을 바꿔도 유지되는 보편 규칙도 아니다. 우리 주장은 이만큼으로 좁다. 이보다 강하게 "크로마틴 포텐셜은 틀렸다"고 말하면 Ma의 연구와 직접 충돌한다. 그래서 이 부분은 논문에서도 결론 한 문단짜리 함의로만 둔다.

## 판정: 논문거리, 그리고 낼 곳

정리하면 이렇다. 우리 발견은 새롭되 부분적으로 앞서 나온 관찰 위에 있다. 크로마틴을 쓰는 두 프로그램이 유전자별 시간차에서 부분적으로 어긋난다는 날것의 관찰은 MoFlow에 이미 있다. **그리고 시간차가 왜 흔들리는지의 기전 쪽에도 선행연구가 있다** — ConsensusVelo가 velocity 전환시점(switch time)의 우도가 평평하다는 것, 곧 그 값이 애초에 잘 식별되지 않는다는 것을 우리보다 먼저 보였다. 이 글을 처음 쓸 때 우리는 이 선례를 지도에 올리지 않았는데, 이후 원고는 이를 정면으로 인정하고 우리 목적함수 분석을 **확증(confirmatory)**으로 적는다. 그러니 남는 우리 몫은 "시간차가 왜 어긋나는가"의 최초 발견이 아니라, 그 흔들림을 여러 축으로 계통적으로 재어 **무엇이 대신 재현되는지(α)**까지 함께 낸 신뢰도 지도다. 일치도 숫자 하나만으로는 경쟁 관계지만, 우연을 거르는 검정과 인과 대조까지 갖춘 견고성 비판은 성격이 다르다.

그래서 판정은 진행(GO)이다. 스쿱 위험은 낮음에서 중간 정도로 본다. 위험이 아예 없다고는 하지 않는다. MoFlow가 지나가듯 남긴 비교를 앞세워 인용하고 우리 위치를 갈라 두는 조건에서, 이 연구는 논문이 된다. 잘못 짚기 쉬운 대목은 일치도 숫자를 앞세워 이야기를 시작하는 것이다. 그러면 MoFlow와 세 벤치마크에 얹힌 부수적 기여로 읽힌다. 인과 대조와 신뢰도 지도를 앞세우면 기여가 뚜렷해진다. ("선점당하지 않는다"고까지 적었던 처음 문장은 거두어들인다 — 식별성 쪽 선례인 ConsensusVelo를 그때 지도에 올리지 않은 상태에서 나온 말이었다.)

낼 곳으로는 방법을 감사하는 성격의 저널, 곧 Genome Biology나 Cell Reports Methods를 겨눈다. 견고성 비판과 벤치마크에 α라는 재현되는 값, 그리고 인과 대조를 함께 얹은 연구에 맞는 자리다. 다만 α를 "쓸 만한 불변량"이라고까지 적었던 것은 지금 기준으로 과하다 — α는 프로그램을 바꿔도 재현되지만 상당 부분 발현량이고, 외부 측정(TT-seq 합성률)과의 대조에서 발현량이 α만큼(오히려 더) 잘 맞는다(발현량 +0.410 대 α +0.262). α가 발현량을 넘어서는 정보를 준다는 근거는 아직 없다. 다만 데이터 한 벌만으로는 이런 저널에 얇게 읽히므로, 앞 글에서 다룬 다른 조직·다른 종에서의 재현이 이 자리매김을 뒷받침하는 근거가 된다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 스쿱 (scoop) | 같은 발견을 남에게 먼저 발표당해 새 기여로 인정받지 못하게 되는 일 |
| 선행연구 (related work / prior art) | 같은 주제나 재료를 앞서 다룬 연구. 논문 전에 스쿱 여부를 가리는 대상 |
| 시간차 (lag) | DNA가 열리고 나서 유전자가 켜지기까지의 간격(앞 글 참조) |
| 전사 속도 (α) | 유전자가 켜졌을 때 RNA를 만드는 빠르기(앞 글 참조) |
| 음성 대조군 (negative control) | 크로마틴–RNA 연결을 의도적으로 끊어 결과가 유지되는지 보는 시험 |
| 유리한 부분집합 (favorable subset) | 자기 방법이 잘 맞는 유전자만 사후에 골라 일치를 보이는 것 |
| 크로마틴 포텐셜 (chromatin potential) | 운명 결정 때 크로마틴이 발현보다 먼저 열려 유전자를 준비시킨다는 Ma et al.(2020)의 가설 |
| 일치도 ρ | 두 프로그램의 값이 얼마나 맞는지(−1~+1). 0.7 이상이면 "잘 맞음" |

## 참고

**근거·문서**(주장 출처): `manuscript/related_work.md`(선행연구 지도·스쿱 판정), `manuscript/novelty_strategy.md`(자리매김·차별화 전략), `results/FINDINGS.md`(수치 종합), `results/scrambled_null.md`(ATAC 뒤섞기 음성 대조), `results/concordance.md`(프로그램 간 일치도).

**관련 논문**
- MultiVelo — Li et al., *Nature Biotechnology* 41, 387–398 (2023). [doi:10.1038/s41587-022-01476-y](https://doi.org/10.1038/s41587-022-01476-y)
- MoFlow — Hong et al., *Nature Communications* 17, 566 (2025). [doi:10.1038/s41467-025-67259-6](https://doi.org/10.1038/s41467-025-67259-6)
- 크로마틴 포텐셜 가설 — Ma et al., *Cell* 183, 1103–1116 (2020). [doi:10.1016/j.cell.2020.09.056](https://doi.org/10.1016/j.cell.2020.09.056)

---
*이 글은 진행 중인 연구의 내부 정리이며, 수치·자리매김은 현재 분석 기준이라 후속 검증으로 갱신될 수 있다(연구·교육용).*

---

# What if someone already found this? Prior work and where our paper stands

> TL;DR: Before publishing our finding — "the gene-level lag does not reproduce when you change the program" — we first checked whether it was already out there. The closest prior work, MoFlow (Hong et al. 2025), reported after the fact that some genes' lags agree across programs, but with no test to strip out chance and no control to check causation. We have both. So this study sits partly on top of an earlier observation and still keeps enough novelty to publish.

Since single-cell technology let us read a cell's gene expression and its chromatin (the thread of protein-wound DNA) openness at once, we have been asking whether the order in which chromatin opens can predict transcription. In earlier posts we vetted the quantity we meant to use as the predictor — the "lag" between the DNA around a gene opening and the gene turning on — and concluded that it does not reproduce when the computing program is changed. The transcription rate (α, how fast a gene makes RNA once it is on), by contrast, stayed stable across programs. But however many times a conclusion is checked, one question remains: has someone already found this? And if so, can our work still be a paper?

This post is the record of answering that. It lays out what we searched for, how far the nearest prior study went, and what remains ours by comparison.

## The gate of checking prior work

Before a new finding becomes a paper, you comb the literature to see whether the same finding is already published. Publishing a result without knowing someone got there first is what the field calls being scooped (having your discovery claimed by someone else first). Once scooped, even a carefully built analysis is hard to credit as a new contribution. So this check is a gate as important as the analysis itself.

We split the check two ways. One is "is there a paper whose thesis is the very conclusion we reached?"; the other is "is there a paper that reports, in passing, the observation our conclusion is built on?" The first would be a scoop; if only the second exists, we have to weigh whether there is new work left to add on top.

```
Finding: "the gene-level lag differs by program"
   │  has someone already found this?
   ├─ a paper whose thesis this is       → none
   ├─ general velocity benchmarks (2026) → score direction, not the lag
   └─ closest prior work, MoFlow         → post-hoc "subset of agreeing genes"
                                             (no chance test, no causal control)
   ↓
Two assets that are ours
   1. ATAC-shuffle causal control → lag unchanged = model structure, not chromatin
   2. α robust (ρ=0.88) / lag fragile (ρ≈0) dissociation
   → Verdict: publishable (GO), scoop risk low-to-moderate
```

## What we searched for and did not find

First we looked for a paper whose stated subject is that programs disagree on the lag. No paper makes cross-program disagreement of the gene-level lag among chromatin-aware velocity programs its object of study. No one has treated the cross-program concordance of the lag as the thing to be investigated.

Three large 2026 velocity benchmarks exist, adjacent to us but not overlapping. One sets 15 RNA-only programs against each other across 17 datasets, scoring the accuracy and stability of velocity direction; the second compares 29 across 176 datasets and does include MultiVelo; the third, the largest to date, scores 19 tools and 30 methods across 34 datasets on 8 tasks. All three score the velocity **vector** in a low-dimensional embedding — neither the concordance of the gene-level lag nor the cross-method comparison of velocity matrices. They asked "which way does the cell move?"; we ask "is the lag between chromatin and RNA the same value when you change the program?" The questions differ.

## The closest prior work: MoFlow

The nearest thing in the literature to our finding is MoFlow (Hong et al. 2025). MoFlow is a program from a different lineage that reads the lag by lining the chromatin and RNA signals up against each other. In introducing its method, that paper reported in passing that, over a subset of genes where chromatin opens first (a negative lag), MultiVelo and its own method mostly agreed.

This is where we overlap most. An actual gene-level comparison of two chromatin-aware programs' lags is already in a peer-reviewed paper. So this is the part we must cite head-on and clearly separate our position from.

But MoFlow's report is of a different character. It picked, after the fact, the genes where its own method concurs and showed "here the two methods agree" — a check on a favorable subset. There was no statistic to strip out the genes that look concordant by chance among thousands, and no control to check whether that agreement actually comes from chromatin. The questions we press — is that agreement reproducible, and is it made by chromatin — are exactly the two MoFlow did not test.

![Comparison with the closest prior work, MoFlow: both report partial cross-method lag agreement post-hoc (✓), but chance control (permutation FDR) and a causal scrambled-chromatin negative control are absent in MoFlow (✗) and present in ours (✓).](../pipeline/hspc-velocity-benchmark/figures/fig03_novelty_comparison.png)

## Our own asset 1: the ATAC-shuffle causal control

The first place we clearly part from MoFlow is a negative control that tests causation. To see whether the lag really comes from chromatin, we deliberately mismatched the chromatin–RNA pairing within each lineage — giving one cell's RNA the chromatin measurement from a different cell in the same lineage, keeping each value's overall distribution intact and breaking only the within-cell link. If the lag came from chromatin, breaking that link should change the lag substantially.

It did not. MultiVelo's lag distribution was statistically almost identical to before the link was broken (distribution-difference test p=0.20), and the per-gene lag correlation held at ρ=0.72. That the lag stayed put even after scrambling chromatin means it comes from the program's internal switch-time ordering, not from the chromatin signal.

This is a different kind of claim from "the programs disagree." That one compares programs; this one pins, causally, where the lag comes from. This control — showing that model structure, not chromatin, makes the lag — is one no competing paper, MoFlow included, has run. It is the first asset that holds our ground.

## Our own asset 2: α robust, the lag fragile

The second asset is a contrast drawn from the same pipeline. The lag did not reproduce across programs (agreement ρ near zero), but the transcription rate α matched well across programs (ρ=0.88). Rank agreement ρ runs from −1 to +1, and above 0.7 is usually read as "strong." By that yardstick 0.88 is strong, and a lag near zero is no correlation. This split — from the same data and the same preprocessing, one quantity survives and another collapses — is the second asset.

On top of that, from untreated day0 baseline features we could, to a degree, predict α for held-out lineages (ρ=+0.31, positive in all six lineages), while the lag could not be predicted from the same input. **What does the predicting, though, is not chromatin.** This post originally credited chromatin; later work showed an abundance confound — abundance alone predicts α at +0.724, and adding chromatin lowers it to +0.708 (increment −0.016). The manuscript now writes this as a baseline-to-α path, not a chromatin-to-α one. The weight of this study is less that α is used for prediction than that α is a quantity that reproduces across programs.

Why does this contrast matter? Taken alone, α matching well sounds like the dull fact that "transcription rate is easy to estimate." The weight comes from the contrast: right next to a lag that model structure generates independently of chromatin and that shifts from program to program, α reproduces. Which velocity outputs can be trusted and which cannot — that contrast is what the method papers left out while presenting the lag as a headline biological finding.

## The falsification target: the chromatin-potential hypothesis

Our finding puts an old biological hypothesis on the stand: the chromatin potential of Ma et al. (2020) — the idea that as a cell commits to a fate, the chromatin around a gene opens before its expression, that is, chromatin primes the gene. It is the same family of claim as the chromatin priming from the earlier post, and it was our starting point for wanting to use the lag as a predictor.

Our data test this at the level of individual genes. Across the population, genes where chromatin leads and genes where RNA leads split roughly half and half, so the global claim that "chromatin always comes first" is not supported per gene in human hematopoietic cells. Yet at canonical marker genes the chromatin-leading direction is largely consistent across programs. So our conclusion stops short of rejecting chromatin potential wholesale. But this direction-agreement is a correlation — a later causal control that scrambles the chromatin signal found that even at named genes chromatin does not shake the lag any more than elsewhere (covered in a follow-up post). So the direction-agreement is real, but our data do not support the causal claim that chromatin makes that lag, nor is it a universal rule that holds gene-wide and survives a change of program. Push past that line to "chromatin potential is wrong" and you trip directly over Ma's work. So in the paper too this stays a single closing paragraph of implication.

## Verdict: publishable, and where to send it

To sum up: our finding is novel but sits partly on top of an earlier observation. The raw observation that two chromatin-aware programs partly disagree on the gene-level lag is already in MoFlow. But why that lag disagrees (the causation pinned by the ATAC shuffle) and what reproduces in its place (α) are in no prior work. A single concordance number is a competitive claim; a robustness critique equipped with a chance-stripping test and a causal control is a claim of a different kind.

So the verdict is GO. We put the scoop risk at low-to-moderate — not that there is none. On the condition that we cite MoFlow's in-passing comparison up front and separate our position from it, this work becomes a paper. The failure mode to watch is opening the story with the concordance number; do that and it reads as an incremental add-on to MoFlow and the three benchmarks. Lead with the causal control and the reliability map and the contribution is clear. (We withdraw the original wording, "a contribution no one can preempt" — it was written before we put ConsensusVelo on the map. ConsensusVelo showed the flatness of velocity switch-time likelihoods before us, and the manuscript now credits it head-on and treats our objective-function analysis as confirmatory.)

For a venue we aim at a method-auditing journal — Genome Biology or Cell Reports Methods. That is the right home for a study that carries a robustness critique and a benchmark plus a usable invariant (α) and a causal control. One dataset alone would read thin for such a journal, though, so the cross-tissue, cross-species replication from the earlier post is the pillar that holds this positioning up.

## Glossary

| Term | Meaning |
|---|---|
| scoop | Having your discovery published by someone else first, so it no longer counts as a new contribution |
| related work / prior art | Research that addressed the same subject or material earlier; what a scoop check is run against |
| lag | The gap between the DNA opening and the gene turning on (see previous post) |
| transcription rate (α) | How fast a gene makes RNA once it is on (see previous post) |
| negative control | Deliberately breaking the chromatin–RNA link to see whether the result holds |
| favorable subset | Showing agreement by selecting, after the fact, only the genes where one's own method concurs |
| chromatin potential | Ma et al.'s (2020) hypothesis that chromatin opens before expression during fate commitment, priming the gene |
| agreement ρ | How well two programs' values match (−1 to +1); ≥0.7 counts as "strong" |

## References

**Evidence and documents** (sources of the claims): `manuscript/related_work.md` (prior-work landscape and scoop verdict), `manuscript/novelty_strategy.md` (positioning and differentiation strategy), `results/FINDINGS.md` (numbers), `results/scrambled_null.md` (ATAC-shuffle negative control), `results/concordance.md` (cross-program agreement).

**Related work**
- MultiVelo — Li et al., *Nature Biotechnology* 41, 387–398 (2023). [doi:10.1038/s41587-022-01476-y](https://doi.org/10.1038/s41587-022-01476-y)
- MoFlow — Hong et al., *Nature Communications* 17, 566 (2025). [doi:10.1038/s41467-025-67259-6](https://doi.org/10.1038/s41467-025-67259-6)
- Chromatin-potential hypothesis — Ma et al., *Cell* 183, 1103–1116 (2020). [doi:10.1016/j.cell.2020.09.056](https://doi.org/10.1016/j.cell.2020.09.056)

---
*Internal working note from ongoing research; numbers and positioning reflect the current analysis and may be updated by further validation (research and educational use).*
