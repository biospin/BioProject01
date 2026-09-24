# 크로마틴이 전사를 "미리 준비"시킬까 — 예측에 쓰려던 "시간차"부터 검증한 이유

> 한 줄 요약: 예측에 쓰려던 "시간차(lag)" 값이 계산 프로그램을 바꾸면 달라졌다. 반면 전사 속도(α)는 프로그램을 바꿔도 값이 일정했다. 그래서 예측 재료를 시간차에서 α로 바꿨다.

세포 하나에서 유전자 발현(RNA)과 크로마틴이 열린 정도를 동시에 읽는 기술이 나오면서, 오래 묻고 싶던 질문 하나를 실제로 시험할 수 있게 됐다. 유전자가 켜지기 전에 그 주변 DNA가 얼마나 앞서 열리는지, 곧 "크로마틴에서 전사까지의 시간차"를 유전자 하나하나에 대해 재려는 계산 방법이 최근 여럿 등장했다. 우리가 쓰려는 논문은 그 시간차가 믿고 쓸 수 있는 측정값인지를 따진다. 방법마다 답이 같은지 견주고, 크로마틴을 의도적으로 망가뜨리는 대조군으로 그 값이 정말 크로마틴에서 오는지 확인하는 것이 뼈대다. 이 글은 그 검증의 기록이고, 왜 이 질문이 중요한지는 아래의 약물 반응 예측에서 또렷해진다.

우리 최종 목표는 아무 처리도 하지 않은 상태(baseline)만 보고, 어떤 유전자가 후성유전(epigenetics) 약물에 얼마나 빨리 반응할지 미리 맞히는 것이다. 후성유전은 DNA 글자(서열) 자체가 아니라, 그 글자를 얼마나 읽을지, 곧 어떤 유전자를 켜고 끌지를 조절하는 층을 말한다. 후성유전 약물은 바로 이 켜고 끄는 상태를 바꾸는 약이다. DNA가 열려 있는지 닫혀 있는지, 또는 DNA에 붙은 화학 표지(메틸기)를 바꿔서 꺼져 있던 유전자를 다시 켠다. 대표적으로 HDAC 억제제(vorinostat, romidepsin 등)는 크로마틴(chromatin, DNA가 감겨 있는 실타래)을 열린 상태로 유지하고, DNMT 억제제(azacitidine, decitabine)는 DNA 메틸화를 지워 침묵하던 유전자를 되살린다. 이 약들은 주로 골수형성이상증후군(MDS), 급성골수성백혈병(AML), 일부 림프종 같은 혈액암 치료에 실제로 쓰인다. 그래서 우리가 다루는 조혈모·전구세포(HSPC)가 이 문제에 잘 맞는 모델이다.

이게 왜 중요한가. 이 약들은 효과가 있어도 유전자마다 반응이 제각각이라, 어떤 유전자는 빨리 켜지고 어떤 유전자는 반응이 느리거나 아예 반응하지 않는다. 어느 유전자가 빨리 반응할지를 약을 써 보기 전에 세포의 처리 전 상태만으로 미리 알 수 있다면, 약의 표적과 투여 시점을 훨씬 똑똑하게 고를 수 있다.

그 실마리로 오래전부터 지목돼 온 것이 크로마틴이다. 유전자 주변 DNA가 미리 열려 있으면 그 유전자는 켜질 준비가 된 상태라는 생각(chromatin priming)인데, 이게 맞다면 DNA가 열리고 나서 유전자가 켜지기까지의 시간차야말로 그 준비 정도를 재는 잣대가 된다. 이것이 우리가 시간차를 예측 재료 1순위로 삼은 이유다.

물론 "크로마틴이 먼저 열리고 전사가 뒤따른다"는 순서는 그럴듯하고, 여러 교과서도 그렇게 기술한다. 우리도 처음엔 그렇게 기대하며 시작했다. 다만 기대가 뚜렷할수록, 데이터에서 그 순서가 정말 보이는 것인지 아니면 우리가 보고 싶은 대로 읽는 것인지 가려내기가 어려워진다. 그래서 시간차를 검증하는 일은 예측 재료를 고르는 동시에, 그 익숙한 순서를 실제 데이터에 대고 확인하는 일이기도 했다.

그 값이 무엇인지 그림으로 먼저 보자.

```
  DNA 열림 ───── 시간차(lag) ─────► 유전자 켜짐
  (서랍 열기)                        (서류 꺼내 읽기, 속도 α)
```

유전자가 일하는 데는 두 단계가 있다. 먼저 유전자 주변 DNA가 열리고(서랍을 여는 일 = 크로마틴이 열림), 그다음 그 유전자가 켜져서 RNA를 만든다(서류를 꺼내 읽는 일). 이렇게 유전자를 읽어 RNA로 베껴 내는 일을 전사(transcription)라 한다. 이 두 단계 사이의 시간 간격이 시간차이고, 유전자가 일단 켜졌을 때 RNA를 얼마나 빨리 만드는지를 나타내는 값이 전사 속도(α)다. 이 글에서는 시간차와 전사 속도, 이 두 값이 계속 짝을 이뤄 나온다.

정리하면, 서랍이 이미 열려 있는 유전자, 곧 시간차가 짧은 유전자일수록 약에 빨리 반응한다고 보고 시간차를 예측 재료로 쓰려 했다. 그런데 이 예측 전체가 시간차라는 숫자 하나에 얹혀 있다. 그 숫자가 프로그램을 바꿀 때마다 달라지는 것이라면, 그 위에 세운 예측 모델도 소용이 없다. 그래서 예측 모델을 만들기 전에 이것부터 검증했다. 이 시간차, 애초에 믿을 만한 값인가?

## 전제: 실제 시간이 아니라 pseudotime으로서의 "시간" 정의

이 글에서 말하는 "시간차"는 며칠·몇 시간처럼 실제로 흐른 시간이 아니다. 세포마다 분화가 얼마나 진행됐는지를 순서로 재구성한 눈금인데, 이것을 pseudotime이라 부른다. 데이터가 day0과 day7 두 시점에서 왔지만, 이 둘은 배치 효과를 없애려고 하나로 합쳐져 있어서 실제로 흐른 시간의 기준점으로는 쓸 수 없다. 그래서 시간차는 이 pseudotime 눈금으로만 보고한다.

이 데이터(GSE209878, Human CD34+ 조혈세포를 7일 분화시킨 10x Multiome)에는 짚어 둘 것이 두 가지 더 있다. 하나는 세포 수다. 원 논문은 11,605 세포를 보고했는데, 우리가 공통 파이프라인으로 다시 전처리하니 21,878 세포(day0 9,639 + day7 12,239)가 나왔다. 품질 관리 기준의 차이로 보이지만 아직 열린 검토 항목이라 덮지 않고 적어 둔다. 다른 하나는 크로마틴 신호가 매우 성기다는 점이다. 열린 자리들을 유전자 단위로 모으고 다듬어야 쓸 수 있는데, 이 모으는 방식 자체가 뒤의 시간차 추정에 영향을 줄 수 있다.

## 배경: 크로마틴을 방정식에 넣은 MultiVelo

시간차를 재는 프로그램들이 어떻게 작동하는지 잠깐 보고 가자. 뿌리는 RNA velocity라는 아이디어다. 세포를 한 순간 찍은 사진 한 장으로 그 유전자가 지금 켜지는 중인지 꺼지는 중인지를 추정하는 방법이다. 비결은 RNA를 두 종류로 나눠 보는 데 있다. 갓 만들어져 아직 다듬어지지 않은 것(unspliced, u)과 다듬어진 것(spliced, s)의 비율이 방향을 알려 준다. scVelo의 dynamical 모델은 이 관계를 방정식으로 푼다.

```
du/dt = α − βu      (전사로 u가 생기고, splicing으로 빠져나감)
ds/dt = βu − γs     (splicing으로 s가 생기고, 분해로 빠져나감)
```

α는 전사 속도, β는 splicing 속도, γ는 분해 속도다. 이 모델의 한계는 α를 유전자가 켜져 있는 동안 상수로 둔다는 것이다. 그래서 크로마틴이 서서히 열리며 전사가 0에서 차오르는 과정도, 전사가 시작되기 전의 크로마틴 준비도 볼 수 없다. RNA만 보기 때문이다.

MultiVelo는 바로 이 한계를 풀었다. 같은 세포에서 RNA와 크로마틴 열림 정도를 동시에 재는 10x Multiome이 나오자, MultiVelo는 크로마틴 열림 정도 c(t)를 방정식에 직접 넣었다. 전사 속도를 상수가 아니라 크로마틴에 비례하게 만든 것이다.

```
du/dt = α·c(t) − βu    (전사 속도가 크로마틴 열림 c에 비례)
```

크로마틴이 닫혀 있으면(c≈0) 전사도 0이고, 열리면 그만큼 올라간다. 이 한 줄 덕분에 모델은 각 유전자를 네 상태로 나눈다. 크로마틴은 열렸는데 전사는 아직인 상태(primed), 둘이 함께 켜진 상태(coupled-on), 크로마틴은 닫히는데 전사는 진행 중인 엇박자(decoupled), 둘이 함께 꺼진 상태(coupled-off)다. 유전자는 크로마틴이 전사보다 먼저 닫히는 부류(M1)와 그 반대(M2, 세포 분열 주기 유전자가 여기 몰린다)로도 나뉜다. 시간차는 이 전환 시점들의 차이에서 나오고, 크로마틴이 열리는 속도 α_c가 그 값을 좌우한다.

이것이 MultiVelo가 부실한 모델이라는 뜻은 아니다. 합성 데이터에서 M1/M2 분류 정확도가 98.5%였고, RNA만 쓸 때 생기던 이상한 잔상도 없앴다. 다만 저자들 스스로 "추가 데이터 없이는 이 시간차의 메커니즘을 확정할 수 없다"고 못 박았다. 곧 이 시간차는 관찰된 연관이지 인과의 증명이 아니다. 이 신중함이 우리 재검증의 출발선이다.

## 검증 방법: 프로그램 간 재현성 확인

시간차에는 정답 데이터가 없다. 세포를 실제로 추적하거나 실시간으로 잰 기록이 없기 때문이다. 그래서 답할 질문을 바꿨다. "어느 프로그램이 맞나"가 아니라 "프로그램을 바꿔도 같은 값이 나오나"이다.

같은 데이터와 같은 전처리에서 시작해, 프로그램 다섯 개로 각각 시간차를 계산하고 서로 비교했다. 여기서 전처리를 똑같이 맞추는 게 중요하다. 나중에 프로그램끼리 답이 갈릴 때 그게 프로그램 차이인지 전처리 차이인지 헷갈리면 안 되기 때문이다.

각 프로그램이 무엇이고 어떻게 다른지 짚어 두자. 앞의 넷은 모두 크로마틴 정보를 함께 쓰지만 시간차를 재는 방식이 서로 다르고, 마지막 하나는 크로마틴을 아예 안 쓰는 비교 기준이다.

- **MultiVelo**(원본): 크로마틴 열림 정도를 전사 속도에 직접 넣은 첫 모델. 유전자가 켜지고 꺼지는 전환 시각의 차이로 시간차를 잰다.
- **MultiVeloVAE**: MultiVelo 계열의 딥러닝(확률) 버전. 값을 여러 번 표본추출해 추정한다.
- **MoFlow**: 계보가 다른 방식으로, 크로마틴 신호와 RNA 신호를 나란히 맞대어 밀린 정도로 시간차를 잰다.
- **CRAK-Velo**: 또 다른 모델(UniTVelo)에 크로마틴을 붙여 확장한 것.
- **RNA-only 기준선**(scVelo): 크로마틴을 안 쓰고 RNA만 보는 바닥선. 크로마틴을 쓰는 위 넷이 이 바닥선보다 얼마나 나아지는지를 재는 기준이다.

시간차가 진짜 생물학적 값이라면 프로그램이 달라도 값이 비슷해야 한다.

## 결과: 프로그램 간의 상이성

```
              시간차(lag)            전사 속도(α)
  프로그램 A ─┐  값이 제각각          ┐  값이 비슷
  프로그램 B ─┼─ ρ ≈ 0              ┼─ ρ = 0.88
  프로그램 C ─┘  방향도 50 대 50      ┘
                 → 예측에 못 씀        → 쓸 수 있음
```

각 프로그램은 저마다 시간차 값을 내놓았다. 이를테면 MultiVelo는 538개 유전자에서 중앙값 5.98(pseudotime)의 시간차를 냈다. 이 값들을 프로그램끼리 맞대 보며 세 가지를 차례로 봤다.

**첫째, 시간차가 프로그램끼리 맞지 않았다.** 어느 유전자의 시간차가 큰지를 순위로 매겨 비교했더니 거의 무관했다. 아래 세 값은 시간차를 **부호까지 살린 채**(DNA 선행은 +, RNA 선행은 −) 비교한 것이다.

| 비교 | 일치도 ρ |
|---|---|
| MultiVelo × MoFlow | −0.04 |
| MultiVelo × MultiVeloVAE | −0.01 |
| MoFlow × MultiVeloVAE | +0.08 |

세 값 모두 0 근처다. 순위 일치도 ρ는 −1에서 +1 사이의 값으로, 보통 0.5는 넘어야 "어느 정도 맞는다", 0.7을 넘으면 "잘 맞는다"고 본다. 그 잣대로 보면 0.04·0.01·0.08은 사실상 상관 관계가 없다. (부호를 떼고 **크기만** 비교하면 가장 잘 맞는 한 쌍인 MultiVelo × MultiVeloVAE가 +0.163까지 올라간다. 그래도 "어느 정도"의 문턱 0.5에는 한참 못 미치고, 나머지 쌍은 여전히 |ρ| 0.08 이하다. 부호를 살린 값과 크기만 본 값은 서로 다른 잣대이므로 섞어 읽지 않도록 둘 다 적어 둔다.) 한 프로그램에서 시간차가 큰 유전자가 다른 프로그램에서는 크지 않다는, 곧 프로그램 간 불일치라는 뜻이다. 정의를 최대한 같은 기준으로 맞춰 다시 계산해도 +0.12에 그쳐, "어느 정도 맞는다"고 볼 0.5에도 한참 못 미친다. (반대로 뒤에서 볼 전사 속도 α의 0.88은 "잘 맞는" 쪽이다.)

**둘째, 방향도 반반으로 나뉘었다.** DNA가 먼저 열리는지 유전자가 먼저 켜지는지의 방향을 봤더니, MultiVelo만 "DNA가 100% 먼저"라고 나왔다. 하지만 이건 실제 신호가 아니다. MultiVelo는 켜짐·꺼짐 전환 시점을 한 방향으로만 정렬하는 구조라, 방향이 처음부터 한쪽으로 고정되어 나온다. 방향이 자유로운 프로그램에서는 DNA가 먼저인 비율이 41~49%로, 모두 절반 근처였다. 즉 "크로마틴이 전사를 미리 준비시킨다"는 전역적 주장을 데이터가 지지하지 않는다. 다만 계통별로 보면 방향이 무작위가 아니라 결이 있다. 초기 세포(HSC/MPP)에서는 RNA가 먼저 움직이는 표지 유전자(HLF, CRHBP: −0.31)가, 골수계에서는 크로마틴이 먼저 열리는 표지 유전자(AZU1 +0.38, ELANE +0.19)가 나온다. 그리고 이런 교과서적 표지 유전자의 방향은 프로그램을 바꿔도 대체로 일치했다. 흔들리는 것은 "어느 유전자가" 크로마틴 선행인지의 세부지, 잘 알려진 표지 유전자의 방향이나 집단 수준의 균형은 아니다. **다만 이 일치는 상관일 뿐 인과가 아니다.** 우리는 나중에 이 표지 유전자들에 직접 인과 대조를 걸어 봤다 — ATAC를 뒤섞었을 때 표지 유전자의 시간차가 나머지 유전자보다 더 흔들리는지 본 것인데, 결과는 무신호였다(표지 0.137 대 전체 0.144, p=0.58). 여러 프로그램이 같은 방향을 가리킨다는 사실은 남지만, 그 방향이 **그 자리의 크로마틴 때문**이라는 근거는 우리 데이터에 없다.

**셋째, 크로마틴 신호를 망가뜨려도 시간차가 그대로였다.** 이게 시간차가 크로마틴에서 나온 값이 아니라는 가장 분명한 근거다. 원래 세포 하나에는 그 세포의 크로마틴(서랍이 열린 정도)과 그 세포의 RNA(유전자가 켜진 정도)가 짝으로 붙어 있다. 이 짝을 의도적으로 어긋나게 섞었다. 어떤 세포의 RNA에 엉뚱한 다른 세포의 크로마틴을 갖다 붙인 것이다(각 값의 전체 분포는 그대로 두고, 세포 안에서의 연결만 끊는다). 시간차가 정말 크로마틴에서 나온 값이라면, 이렇게 연결을 끊었을 때 시간차도 크게 달라져야 한다. 그런데 시간차 분포가 통계적으로 거의 같았고(분포 차이 검정 p=0.20), 유전자별 시간차 상관도 ρ=0.72로 보존됐다. 그래서 MultiVelo가 낸 시간차는 크로마틴 신호가 아니라 프로그램 내부 구조에서 나온 값이다.

## 시간차 민감성의 원인

앞의 방정식에서 봤듯, 시간차를 좌우하는 것은 크로마틴이 열리는 속도 α_c다. 여기에 시간차가 프로그램마다 달라지는 원인이 있다. α_c를 추정하는 것 자체가 프로그램마다 크게 달랐고(ρ=0.29), 그 위에서 계산되는 시간차도 따라서 달라졌다. 반면 전사 속도 α는 프로그램 간에 매우 일정했다(ρ=0.88). 프로그램들이 "읽는 속도(α)"에는 쉽게 합의하면서 "서랍-서류 시간차"에는 합의하지 못하는 이유가 여기 있다.

## 일정한 전사 속도 지표, α

이 여러 속도 지표 가운데 의미 있게 살아남은 것이 전사 속도 α다. 앞서 봤듯 α는 프로그램을 바꿔도 값이 일정했고(ρ=0.88), 게다가 예측에도 쓸 수 있었다. 처리 전 day0 정보만으로 학습에 쓰지 않은 계통의 α를 맞힐 수 있었던 반면(ρ=+0.31, 6개 계통 모두 양수), 시간차는 같은 정보로도 맞히지 못했다(ρ≈+0.05, 절반 수준). 같은 재료로 α는 맞히고 시간차는 못 맞힌 것이다.

**다만 그 예측을 해내는 것이 크로마틴은 아니다.** 이 글을 처음 쓸 때 우리는 이 +0.31을 "day0 크로마틴에서 α로 이어지는 경로"라고 적었는데, 이후 검증에서 틀린 귀속으로 판명됐다. 발현량(전사체 존재량)만으로 α를 예측하면 ρ=+0.724가 나오고, 여기에 크로마틴을 더해도 +0.708로 오히려 내려간다(증분 −0.016). 발현량을 통제하면 크로마틴의 몫은 +0.112까지 줄어든다. 인간 뇌 데이터에서는 같은 경로가 +0.212에서 +0.013으로 아예 사라졌다. 즉 크로마틴이 α를 예측한 것이 아니라, 크로마틴과 α가 둘 다 발현량을 따라간 것이다. 지금 원고는 이 대목을 "크로마틴에서 α로"가 아니라 **"기저 상태에서 α로"**라고 적는다. 예측 경로가 있다는 결론은 남지만, 그 공은 크로마틴이 아니라 발현량에 있다.

## 결론

크로마틴에서 전사까지의 시간차는 유전자 수준에서 프로그램을 바꾸면 재현되지 않는다.

단, "시간차가 무의미하다"거나 "MultiVelo가 틀렸다"는 의미가 아님을 주의해야 한다. 한 프로그램 안에서만 보면 시간차에도 신호가 있다. 예를 들어 같은 데이터에서 세포를 다시 뽑아 계산해도 방향이 83% 유지된다. 우리가 말하는 것은 "프로그램을 바꿔도 값이 유지되는가"라는 더 엄격한 기준을 통과하지 못했다는 것뿐이며, 이 구분을 흐리면 결론이 실제보다 과장된다.

그래서 약물 타이밍 모델의 예측 재료는 시간차 대신 α를 쓴다. 시간차를 꼭 쓰려면, 프로그램에 따라 값이 달라지는 불확실성을 모델에 그대로 반영해야 한다.

돌아보면 이 검증이 준 것은 시간차에 대한 판정만이 아니었다. 한 도구가 "언제나 크로마틴이 먼저"라고 말할 때 그게 생물학인지 도구의 설계 탓인지를 먼저 의심하게 됐고, 정작 예측하려던 값이 믿을 수 없다는 걸 확인하고 나서야 무엇을 써야 하는지(α)가 또렷해졌다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 후성유전 (epigenetics) | DNA 글자는 그대로 두고, 어떤 유전자를 켜고 끌지 조절하는 층 |
| 크로마틴 (chromatin) | DNA가 단백질에 감긴 실타래. 열리면 그 안의 유전자를 읽을 수 있음 |
| 전사 (transcription) | 유전자를 읽어 RNA로 베껴 내는 일(유전자가 "켜짐") |
| 시간차 (lag) | DNA가 열리고 나서 유전자가 켜지기까지의 간격 |
| 전사 속도 (α) | 유전자가 켜졌을 때 RNA를 만드는 빠르기 |
| α_c | 크로마틴이 열리는 속도. 시간차를 좌우함 |
| unspliced / spliced RNA | 갓 만들어 아직 안 다듬어진 RNA(u) / 다듬어진 RNA(s). 둘의 비율이 유전자 방향을 알려 줌 |
| splicing 속도 β · 분해 속도 γ | u가 s로 바뀌는 속도 · s가 분해되는 속도 |
| pseudotime | 분화가 얼마나 진행됐는지의 순서(실제로 흐른 시간 아님) |
| 일치도 ρ | 두 프로그램의 값이 얼마나 맞는지(−1~+1). 0.7 이상이면 "잘 맞음" |
| 음성 대조군 | 크로마틴–RNA 연결을 의도적으로 끊어 결과가 유지되는지 보는 시험 |
| HSPC | 조혈모·전구세포. 여러 혈액세포로 분화하는 출발 세포 |

## 참고

**근거·코드**(수치 출처): `results/FINDINGS.md`(종합), `p3_concordance.py`(프로그램 간 일치도·방향), `p2_multivelo_scrambled.py`·`p3_scrambled_null.py`(음성 대조군), `h1_lag_diagnostic.md`(α_c 민감성 진단), baseline→α 예측·bootstrap 안정성 결과.

**관련 논문**
- MultiVelo — Li et al., *Nature Biotechnology* 41, 387–398 (2023). [doi:10.1038/s41587-022-01476-y](https://doi.org/10.1038/s41587-022-01476-y)
- MoFlow — Hong et al., *Nature Communications* 17, 566 (2025). [doi:10.1038/s41467-025-67259-6](https://doi.org/10.1038/s41467-025-67259-6)
- Chromatin potential 가설 — Ma et al., *Cell* 183, 1103–1116 (2020). [doi:10.1016/j.cell.2020.09.056](https://doi.org/10.1016/j.cell.2020.09.056)

---
*이 글은 진행 중인 연구의 내부 정리이며, 수치는 현재 분석 기준이라 후속 검증으로 갱신될 수 있다(연구·교육용).*

---

# Does chromatin really "prime" transcription? Why we vetted the "lag" before trusting it as a predictor

> TL;DR: The "lag" we wanted to use as a predictor changed depending on which program computed it. The transcription rate (α), by contrast, stayed stable across programs. So we switched our predictor from lag to α.

Single-cell technology can now read a cell's gene expression (RNA) and how open its chromatin is at the same time, which lets us finally test a long-standing question: before a gene turns on, how much earlier does the DNA around it open (the "chromatin-to-transcription lag")? Several computational methods now try to measure this lag gene by gene. The paper this post draws on asks whether that lag is a measurement we can trust: it compares whether different methods give the same answer and uses a control that deliberately breaks the chromatin signal to confirm the lag really comes from chromatin. This post is that verification story; why the question matters is clearest in the drug-response prediction below.

Our end goal is to predict, from a cell's baseline (untreated) state alone, how quickly a given gene will respond to an epigenetic drug. Epigenetics refers not to the DNA letters (the sequence) themselves but to the layer that controls how much they are read — which genes get switched on or off. Epigenetic drugs change exactly that on/off state: they alter whether the DNA is open or closed, or the chemical tags (methyl groups) attached to it, to switch silenced genes back on. HDAC inhibitors (vorinostat, romidepsin) keep chromatin (the thread of protein-wound DNA) in an open state, and DNMT inhibitors (azacitidine, decitabine) erase DNA methylation to reactivate silenced genes. Such drugs are used clinically mostly in blood cancers — myelodysplastic syndrome (MDS), acute myeloid leukemia (AML), and some lymphomas — which is why the hematopoietic stem/progenitor cells (HSPCs) we study are a fitting model for this question.

Why does this matter? These drugs work, but unevenly: some genes switch on fast, others respond slowly or not at all. If we could tell, from a cell's untreated baseline alone, which genes will respond quickly, we could choose drug targets and timing far more intelligently, without testing every drug on every patient.

The clue people have long pointed to is chromatin. The idea (chromatin priming) is that if the DNA around a gene is already open, the gene is poised to fire; if that holds, then the lag between the DNA opening and the gene turning on is exactly a ruler for how poised a gene is. That is why the lag was our first-choice predictor.

The picture of chromatin opening first and transcription following is a plausible one, and it is how many textbooks describe it; we started out expecting it too. But that very plausibility is the catch: the clearer the expectation, the harder it is to tell whether the order is really in the data or something we are reading into it. So testing the lag became, at the same time, a way to hold that familiar order up against the data.

Here is what it means:

```
  DNA opens ───── lag ─────► gene turns on
  (unlock drawer)             (take out the file & read; rate α)
```

A gene works in two steps. First the DNA around it opens (unlocking a drawer — this thread of wound-up DNA is called chromatin), then the gene turns on and copies itself into RNA (taking the file out and reading it); this copying is transcription. The time gap between the two steps is the lag, and a second value, the transcription rate (α), is how fast the gene makes RNA once it is on. These two values appear side by side throughout this post.

So a gene whose drawer is already open (a short lag) should respond quickly to a drug; that was the plan. But the whole prediction rests on this one number. If the lag changes every time we swap programs, any model built on top of it is worthless. So before building any model, we tested exactly that: is the lag even a trustworthy number?

## First, a caveat: "time" here is not clock time

The "lag" here is not measured in clock time. It is a reconstructed ordering of how far each cell has progressed through differentiation — called pseudotime. The data come from two timepoints (day0, day7), but they were merged to remove batch effects, so they cannot anchor real clock time. Lag is reported in pseudotime only.

Two more things about this data (GSE209878 — human CD34+ hematopoietic cells differentiated for seven days on 10x Multiome) are worth stating plainly. One is the cell count: the original paper reported 11,605 cells, while our common pipeline re-preprocessed to 21,878 (day0 9,639 + day7 12,239). This looks like a difference in quality-control thresholds, but it is still an open item, so we record it rather than hide it. The other is that the chromatin signal is very sparse: open sites have to be aggregated to the gene level and smoothed, and that aggregation can itself affect the lag estimates downstream.

## Background: MultiVelo, putting chromatin into the equation

A quick look at how these programs work. The root idea is RNA velocity: estimating, from a single snapshot of a cell, whether a gene is currently switching on or off. The trick is to split RNA into two kinds — freshly made, not-yet-spliced (unspliced, u) and spliced (s); their ratio reveals the direction. scVelo's dynamical model fits this with equations:

```
du/dt = α − βu      (transcription makes u; splicing turns it into s)
ds/dt = βu − γs     (u becomes s; s is degraded)
```

Here α is the transcription rate, β the splicing rate, γ the degradation rate. The limitation is that α is held constant while the gene is on, so the model cannot see chromatin gradually opening and transcription ramping from zero, nor the chromatin preparation before transcription starts — it sees only RNA.

MultiVelo's key move addresses this. Once 10x Multiome could measure RNA and chromatin openness in the same cell, MultiVelo put chromatin openness c(t) directly into the equation, making the transcription rate proportional to chromatin rather than constant:

```
du/dt = α·c(t) − βu    (transcription rate scales with chromatin openness c)
```

When chromatin is closed (c≈0) transcription is zero; as it opens, transcription rises with it. This one line lets the model sort each gene into four states: chromatin open but transcription not yet (primed), both on (coupled-on), chromatin closing while transcription continues (decoupled), both off (coupled-off). Genes also split into those whose chromatin closes before transcription is repressed (M1) and the reverse (M2, where cell-cycle genes cluster). The lag comes from the differences between these switch times, and the chromatin-opening rate α_c governs it.

This is not to say MultiVelo is a poor model. On synthetic data its M1/M2 classification was 98.5% accurate, and it removed odd artifacts that appear with RNA alone. But the authors themselves noted that the mechanism of this lag cannot be established without additional data — the lag is an observed association, not proven causation. That caution is where our re-check begins.

## How we tested it: does the value survive a change of program?

There is no ground truth for the lag — no cell was tracked or timed directly. So we changed the question: not "which program is right?" but "does the value stay the same when we swap programs?"

Starting from the same data and the same preprocessing, we computed the lag with five programs and compared them. Keeping preprocessing identical matters: when the answers diverge, we must know it is the program, not the preprocessing.

Here is what each program is and how they differ. The first four all use chromatin but measure the lag differently; the last ignores chromatin and serves as a baseline.

- **MultiVelo** (the original): the first model to feed chromatin openness directly into the transcription rate. It reads the lag from the difference between a gene's on and off switch times.
- **MultiVeloVAE**: a deep-learning (probabilistic) version in the MultiVelo lineage that estimates values by sampling.
- **MoFlow**: from a different lineage; it lines up the chromatin and RNA signals and reads the lag from how far one is shifted against the other.
- **CRAK-Velo**: another model (UniTVelo) extended with chromatin.
- **RNA-only baseline** (scVelo): uses no chromatin at all — the floor against which we measure how much the four chromatin-aware programs add.

If the lag were a real biological quantity, the programs should agree.

## Result: the value differed by program

```
              lag                    transcription rate (α)
  program A ─┐  all over the place   ┐  similar
  program B ─┼─ ρ ≈ 0                ┼─ ρ = 0.88
  program C ─┘  direction 50/50      ┘
                → not usable           → usable
```

Each program produced its own lags. MultiVelo, for instance, gave a median lag of 5.98 (pseudotime) over 538 genes. Setting these values against one another, we ran three checks:

**1. The lag did not match across programs.** Ranking genes by lag, the programs were essentially uncorrelated. The three values below keep the **sign** (chromatin-first positive, RNA-first negative):

| comparison | agreement ρ |
|---|---|
| MultiVelo × MoFlow | −0.04 |
| MultiVelo × MultiVeloVAE | −0.01 |
| MoFlow × MultiVeloVAE | +0.08 |

All near zero. As a rough rule of thumb, a rank agreement ρ needs to clear about 0.5 to count as "moderate" and 0.7 to count as "strong"; by that yardstick 0.04, 0.01, and 0.08 are essentially no correlation. (Dropping the sign and comparing **magnitude only**, the strongest pair — MultiVelo × MultiVeloVAE — rises to +0.163. That is still far short of the 0.5 bar, and the remaining pairs stay at |ρ| ≤ 0.08. Signed and magnitude values are different yardsticks, so we give both rather than let them be read as one.) Even after aligning the definitions as closely as possible, it only reached +0.12 — far short of that bar. (By contrast, the α agreement of 0.88 we will see later sits firmly in the "strong" range.)

**2. The direction was a coin flip.** Only MultiVelo said "DNA is first 100% of the time" — but that is not a real signal. MultiVelo aligns on/off switch times in one direction only, so the direction is fixed from the start. In programs where direction is free, DNA-first ranged 41–49% — right around half. So the data do not support a global claim that chromatin primes transcription. Per lineage, though, the direction is not random but patterned. In early cells (HSC/MPP), markers where RNA moves first show up (HLF, CRHBP: −0.31), while in the myeloid lineage, markers where chromatin opens first show up (AZU1 +0.38, ELANE +0.19). And the direction of these textbook markers was largely consistent across programs. What wavers is the detail of which gene leads with chromatin, not the direction of well-known markers or the population-level balance. **That agreement is correlational, not causal.** We later ran the causal control on these very markers — asking whether shuffling ATAC perturbs the markers' lags more than it perturbs the rest — and it came back null (markers 0.137 versus bulk 0.144, p=0.58). The fact that several programs point the same way survives; evidence that they do so *because of the chromatin at those loci* does not exist in our data.

**3. Scrambling the chromatin signal left the lag unchanged.** This is the clearest evidence that the lag is not driven by chromatin. Normally each cell carries its own chromatin (how far its drawer is open) paired with its own RNA (how far its gene is on). We deliberately mismatched that pairing — giving one cell's RNA the chromatin measurement from a different cell, keeping each value's overall distribution intact and breaking only the within-cell link. If the lag really came from chromatin, breaking that link should change the lag substantially. Instead the lag distribution was statistically almost identical (p=0.20) and the per-gene correlation held at ρ=0.72. So MultiVelo's lag comes from the program's internal structure, not from chromatin.

## Why only the lag is program-sensitive

As the equations above show, what governs the lag is the chromatin-opening rate α_c. That is where the program-sensitivity comes from. Estimating α_c was itself highly program-dependent (ρ=0.29), so the lag built on top of it varied too. The transcription rate α from the same equations, by contrast, was very consistent across programs (ρ=0.88). That is why programs readily agree on "reading speed (α)" but not on the drawer-to-file lag.

## What did stay stable across programs

Among those rates, the one that meaningfully survived was the transcription rate α. As noted, α stayed stable across programs (ρ=0.88), and it was also predictable: from day0 baseline features alone we could predict α for held-out lineages (ρ=+0.31, positive in all 6 lineages), while the lag could not be predicted from the same input (ρ≈+0.05, near chance). The same input predicted α but not the lag.

**What does the predicting, however, is not chromatin.** When this post first went up we described that +0.31 as "a usable path: day0 chromatin → α". Later work showed the attribution was wrong. Baseline transcript abundance alone predicts α at ρ=+0.724; adding chromatin lowers it to +0.708 (an increment of −0.016), and controlling for abundance shrinks chromatin's own share to +0.112. In human brain the same path collapsed from +0.212 to +0.013. Chromatin was not predicting α — chromatin and α were both tracking abundance. The manuscript now writes this as a **baseline-to-α** path rather than a chromatin-to-α one. The predictive path survives; the credit moves from chromatin to abundance.

## Conclusion

At the gene level, the chromatin-to-transcription lag does not reproduce when you change the program.

But note that this does not mean "the lag is meaningless" or "MultiVelo is wrong." Within a single program there is signal in the lag — for example, resampling cells from the same data keeps the direction 83% of the time. What we are saying is only that it fails the stricter test of whether the value survives a change of program — and blurring that distinction would overstate the result.

So the drug-timing model uses α, not lag, as its input. If the lag must be used, the program-dependent uncertainty has to be carried into the model explicitly.

Looking back, this check gave us more than a verdict on the lag. When a tool now says "chromatin always comes first," we ask first whether that is biology or the tool's own design; and it was only after finding that the quantity we meant to predict was untrustworthy that it became clear what to use instead (α).

---
## Glossary

| Term | Meaning |
|---|---|
| epigenetics | The layer that controls which genes are on or off, without changing the DNA sequence |
| chromatin | DNA wound around protein; when it opens, the gene inside can be read |
| transcription | Copying a gene into RNA (the gene "turning on") |
| lag | The gap between the DNA opening and the gene turning on |
| transcription rate (α) | How fast a gene makes RNA once it is on |
| α_c | The rate at which chromatin opens; it sets the lag |
| unspliced / spliced RNA | Freshly made, not-yet-spliced RNA (u) / spliced RNA (s); their ratio reveals a gene's direction |
| splicing rate β · degradation rate γ | Rate at which u becomes s · rate at which s is degraded |
| pseudotime | An ordering of how far a cell has differentiated (not real elapsed time) |
| agreement ρ | How well two programs' values match (−1 to +1); ≥0.7 counts as "strong" |
| negative control | Deliberately breaking the chromatin–RNA link to see whether the result holds |
| HSPC | Hematopoietic stem/progenitor cells — the starting cells that become blood cells |

## References

**Evidence and code** (sources of the numbers): `results/FINDINGS.md` (synthesis), `p3_concordance.py` (cross-program agreement and direction), `p2_multivelo_scrambled.py` · `p3_scrambled_null.py` (negative control), `h1_lag_diagnostic.md` (α_c sensitivity), baseline→α prediction and bootstrap-stability results.

**Related work**
- MultiVelo — Li et al., *Nature Biotechnology* 41, 387–398 (2023). [doi:10.1038/s41587-022-01476-y](https://doi.org/10.1038/s41587-022-01476-y)
- MoFlow — Hong et al., *Nature Communications* 17, 566 (2025). [doi:10.1038/s41467-025-67259-6](https://doi.org/10.1038/s41467-025-67259-6)
- Chromatin-potential hypothesis — Ma et al., *Cell* 183, 1103–1116 (2020). [doi:10.1016/j.cell.2020.09.056](https://doi.org/10.1016/j.cell.2020.09.056)

---
*Internal working note from ongoing research; numbers reflect the current analysis and may be updated by further validation (research and educational use).*
