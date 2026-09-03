# BIOP01 개발 블로그 — 전체 합본

> 생성 2026-09-02. 개별 편 `01`~`08`을 순서대로 결합한 파일이다.
> 정본은 각 개별 편이며, 이 합본은 파생물이다. 개별 편을 고치면 이 파일을 다시 만든다.

---

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

---

# 재현되지 않는 결과를 스스로 검증하기

> 한 줄 요약: 앞 글에서 "크로마틴에서 전사까지의 시간차는 프로그램을 바꾸면 재현되지 않는다"는 비재현성 결론에 이르렀다. 이런 결론은 우리 실수 때문에 나왔을 수도 있어서, 논문으로 발간하기 전에 실수가 개입할 만한 다섯 방법(벤치마크 설계, 우연, 교란변수, 우리 코드, 빌려 온 숫자)을 차례로 의심하고 하나씩 검증했다. 다섯 곳을 다 통과한 뒤에야 그 결론을 측정값으로 받아들였다.

이 글은 앞 글 「크로마틴이 전사를 "미리 준비"시킬까」의 후속편이다. 앞 글에서 우리는, 유전자 주변 DNA가 열리고 나서 그 유전자가 켜지기까지의 시간차(lag)가 계산 프로그램을 바꾸면 값이 달라져 재현되지 않는다는 결론에 이르렀다.

그런데 비재현성 결론은 조심해서 다뤄야 한다. "재현이 안 된다"는 결과는 진짜로 신호가 없어서일 수도 있지만, 우리가 어딘가에서 실수를 했기 때문일 수도 있다. 논문으로 이 주장을 발표하려면 그 결론이 우리 실수가 아님을 먼저 보여야 한다. 그래서 결론을 내기 전에, 실수가 개입할 만한 다섯 방법을 차례로 의심했다.

```
결론: "시간차는 프로그램을 바꾸면 재현 안 됨"
   │  이게 우리 실수가 아니라고 어떻게 아나?
   ├─ ① 설계   "프로그램끼리 일치도 = 정답"인가?  → 아니오(재현성만 물음)
   ├─ ② 우연   유전자 수천 개의 거짓 패턴 걷어내기 → 방향 일치 54.6%(우연 50%)
   ├─ ③ 교란   세포 분열 주기가 원인 아닌가?        → 유전자엔 1.9%, 안 뽑음
   ├─ ④ 코드   우리 부호 계산은 맞나?             → 버그 한 줄 + 숫자 오독 정정
   └─ ⑤ 차용   다른 세포의 반감기를 써도 되나?      → 관문 통과(ρ=0.695)
```

## ① 설계: 일치와 정답의 구분

정답지 없는 시험을 채점한다고 해 보자. 학생마다 답이 다른데 누가 맞았는지 알 길이 없다. 우리 데이터(GSE209878)가 바로 그런 상황이었다. 유전자가 언제 켜졌는지 직접 표시해 주는 장치가 없어, 시간차의 정답을 알 수 없다.

그래서 질문을 바꿨다. 어느 프로그램이 정확한지는 정답지가 없으니 물을 수 없다. 대신 프로그램을 바꿔도 같은 값이 나오는지를 물었다. 정답지가 없어도 여러 채점자의 점수가 서로 얼마나 겹치는지는 확인할 수 있다.

여기엔 조심할 대목이 하나 있다. 채점자 둘이 같은 학교에서 같은 기준을 배웠다면, 둘의 점수가 겹치더라도 답이 옳다고는 볼 수 없다. 같은 편향을 함께 물려받아 나온 일치일 수도 있기 때문이다. 프로그램도 마찬가지다. MoFlow는 cellDancer라는 앞선 프로그램의 계보를 잇고, MultiVeloVAE는 MultiVelo의 계보를 잇는다. 그래서 재현을 판정하는 핵심 비교 쌍으로는 계보가 서로 다른 MultiVeloVAE와 MoFlow를 두었다. 여기에 크로마틴을 아예 안 쓰는 RNA-only 바닥선을 반드시 넣어, 크로마틴이 실제로 일을 하는지도 함께 봤다. 출발 조건도 공정하게 맞췄다. 모든 프로그램이 같은 세포·유전자·이웃 관계도에서 출발하게 하고, 떠도는 오염 RNA와 이중세포를 먼저 걸러 냈다. 걸러 내지 않으면 모든 프로그램이 같은 오염을 똑같이 반영해 겉으로만 답이 맞는 가짜 일치가 생긴다. 이웃 관계도는 결과를 크게 좌우할 수 있어, 프로그램마다 원래 쓰던 관계도와 공통 관계도를 둘 다 돌려 비교했다. 설계 첫머리에서부터 일치는 재현성의 필요조건일 뿐이라는 점을 분명히 해 두었다. 프로그램끼리 답이 같다고 해서 그 답이 옳다는 증거가 되지는 않는다.

## ② 우연: 유전자 수천 개가 만드는 거짓 패턴

유전자를 한꺼번에 수천 개 검정하면, 진짜 신호가 하나도 없어도 몇 개는 우연히 "맞는 것처럼" 보인다. 동전 수천 개를 던지면 그중 몇 개는 "연달아 앞면" 같은 패턴을 저절로 만드는 것과 같다. 이 우연을 걸러내려고 다중검정 보정을 하는데, 흔히 거짓 발견 비율(FDR, false discovery rate)을 잣대로 쓴다.

교과서적 FDR 보정은 검정들이 서로 독립이라고 가정하는데, 유전자는 독립이 아니다. 같은 조절을 함께 받는 유전자들은 발현이 같이 움직인다. 그래서 진짜 신호가 전혀 없는 상태를 데이터로 직접 만들어 보기로 했다. 유전자 라벨을 무작위로 1만 번 섞어(순열 검정, permutation) 진짜 연결은 끊되 유전자끼리 묶인 구조는 남긴 가짜 데이터를 만들고, 실제 관측값이 그 가짜들 사이에서 얼마나 튀는지를 봤다.

첫 번째 검정에서는 프로그램 쌍끼리 시간차가 서로 얼마나 일치하는지를 따졌다.

| 프로그램 쌍 | 일치도 ρ | q(FDR) |
|---|---|---|
| MoFlow × CRAK-Velo | −0.151 | 0.017 (유의) |
| MoFlow × MultiVeloVAE | +0.083 | 0.051 (유의) |
| CRAK-Velo × MultiVeloVAE | −0.040 | 0.471 |

세 쌍 중 둘이 가짜 대비 유의하게 나왔다. 다만 통계적으로 유의한 것과 두 값이 강하게 맞는 것은 서로 다른 얘기다. 유의한 두 쌍조차 크기가 0.15와 0.08에 그쳤고(0.5는 넘어야 "어느 정도 맞는다"고 본다), 그중 하나는 음수라 방향이 반대였다. 표본이 크면 이처럼 약한 값도 통계적으로는 유의하게 나오기 때문에, 유의성만으로 실제 크기를 판단할 수는 없다.

두 번째 검정은 유전자 하나하나마다 프로그램들의 시간차 방향(DNA가 먼저인지 유전자가 먼저인지)이 얼마나 일치하는지, 그 일치가 우연을 넘어서는지 세는 것이었다. 검정한 598개 유전자 가운데 엄격한 기준(FDR 0.10)을 넘긴 것은 0개였다.

**이 "0개"는 이후 헤드라인에서 내려왔다.** 이 글을 처음 쓸 때 우리는 이 숫자를 가장 분명한 증거로 앞세웠는데, 나중에 스스로 감사해 보니 그렇게 쓸 수 없는 값이었다. 이유는 두 가지다. 첫째, 이 598개 검정은 부호가 흔들리는 프로그램 세 개가 필요해서 MultiVelo를 빼고 **CRAK-Velo를 넣어** 돌린 것인데, CRAK-Velo의 시간차는 바로 이 글 뒷부분에서 우리가 부호 버그를 지적한 그 값이다. 둘째, CRAK-Velo를 빼고 깨끗한 두 프로그램(MoFlow·MultiVeloVAE)만으로 같은 검정을 돌리면 **신호가 있든 없든 0이 나온다** — 프로그램이 둘뿐이면 유전자당 얻을 수 있는 최소 p값이 0.5 근처(실측 0.499)라 어떤 FDR 문턱에서도 통과하는 유전자가 원리적으로 나올 수 없다. 즉 이건 "방향이 일관된 유전자가 없다"가 아니라 **검정이 애초에 그걸 잡을 힘이 없다**는 뜻이다(검정력 제한, power-bounded).

그래서 지금 원고는 0/598을 대표 결과에서 빼고 CRAK 포함 **보조 민감도 분석**으로 다룬다. 헤드라인은 크기 일치도로 갈아탔다(가장 잘 맞는 한 쌍 +0.163, 나머지 |ρ| 0.08 이하). 방향 쪽 깨끗한 숫자는 따로 있다 — MoFlow × MultiVeloVAE 부호 일치율 **54.6%**(방향이 미정인 유전자를 뺀 560개, 이항 p=0.031). 우연인 50%에서 겨우 4.6%p 떨어진 값이라 쓸 수 있는 수준과는 거리가 멀지만, "0개"와는 성격이 다른 정직한 숫자다. 결론(시간차의 방향은 프로그램 간에 재현되지 않는다)은 그대로 서지만, 그 결론을 떠받치는 숫자는 이렇게 바뀌었다.

## ③ 교란: 상관을 봤다고 뽑지 않은 이유

진짜 원인이 아니면서 결과에 끼어드는 딴 요인을 교란변수(confound)라 한다. 단일세포 분석에서는 세포 분열 주기를 특히 조심해야 한다. 세포가 분열 주기의 어디쯤 있느냐에 따라 수많은 유전자 발현이 함께 움직이기 때문이다. 실제로 세포 하나하나를 보니 분열 주기 점수와 우리가 재는 값이 같이 움직였다(상관 0.33~0.36). 이 상관이 0.3을 넘으면 분열 주기의 영향을 회귀로 제거하는 편을 검토하라는 것이 관행이다.

여기서 성급히 뺐다면 진짜 신호까지 함께 지울 뻔했다. 질문을 유전자 단위로 바꾸자 양상이 달라졌다. 값을 얻은 유전자 538개 가운데 분열 주기 유전자는 10개, 1.9%뿐이었다. 이 유전자들과 나머지 유전자의 시간차는 유의하게 다르지 않았고(Mann–Whitney 검정 p=0.862), 분열 주기 유전자를 다 빼도 중앙값은 5.87에서 5.83으로 0.037밖에 움직이지 않았다.

세포 단위에서 나온 이 상관에는 다른 원인이 있었다. 세포 분열 정도가 계통마다 크게 달랐기 때문이다. 활발히 분열하는 세포의 비율이 거핵구는 88%, 골수계·적혈구계는 79%, Baso/Eo/Mast 계열은 44%, 림프계는 16%, HSC/MPP는 3%였다. 그러니 세포를 계통 구분 없이 한데 모아 보면 "분열 주기와 시간차의 상관"처럼 보인다. 그러나 그 상관은 실제로는 계통 구조에서 비롯된다. 계통 안에서(within-lineage) 계산하면 이 연관은 이미 통제된다. 그래서 전역 통제는 의도적으로 하지 않았다. 무리하게 통제했다면 분열과 함께 움직이는 분화 신호까지 뽑았을 것이다. 이 경우엔 뽑지 않는 편이 더 조심스러운 선택이었다. 결국 분열 주기는 통제 대상으로 삼지 않고 민감도 점검 항목으로만 보고했다.

교란 후보는 분열 주기 말고도 더 있었다. 유전자가 한꺼번에 켜지는 발현 폭발(burst)과 전사 속도 α의 공선성은 순위 상관 ρ=−0.242로 중간 정도였다. 지금 결론을 흔들 만큼은 아니지만, 나중에 예측 모델에서 통제할 항목으로 적어 두었다. 세포 밖을 떠도는 오염 RNA와 두 세포가 한 방울에 잡힌 이중세포(doublet)도 점검했다. scrublet으로 걸러 낸 뒤 남은 이중세포 점수는 상위 1%가 0.268로 정상 범위였고, 죽어 가는 세포의 흔적인 미토콘드리아 RNA 비율도 중앙값 10.4%로 QC 상한 20% 안쪽이었다.

## ④ 코드: 우리 부호부터 의심

시간차에는 크기("얼마나")와 방향("어느 쪽이 먼저")이 함께 들어 있다. 방향은 부호(sign)로 적는데, 두 사건의 순서를 뺄셈으로 구할 때 `j−i`를 `i−j`로 잘못 쓰면 부호가 통째로 뒤집힌다. 그런데 크기는 그대로라, 크기만 확인하는 검사는 아무 문제 없이 통과한다.

처음 이상을 알아챈 곳은 표지 유전자였다. 골수계 표지 유전자 CSF1R은 선행 문헌상 DNA가 미리 열리는 쪽으로 알려져 있어 양수를 예상했는데, −12로 나왔다. (여기서 "양수가 나와야 한다"는 것은 문헌 기반 기대이지 우리가 확인한 정답이 아니다. 우리가 나중에 표지 유전자에 ATAC 뒤섞기 대조를 걸었을 때는 무신호였다 — p=0.58. 이 대목은 버그를 찾게 해 준 단서로는 유효하지만, 표지 유전자의 방향을 정답처럼 쓰면 안 된다.) DNA가 먼저 열리는 가짜 전환 신호를 직접 만들어 넣고 확인해 보니, MoFlow는 예상대로 +30인데 CRAK-Velo는 −72로 부호가 정반대였다. 그래서 뺄셈 순서를 바로잡도록 수식을 고쳤고(`j−i`→`i−j`), 고친 뒤에는 CRAK-Velo도 +8로 방향이 일치했다. 실제 표지 유전자에서도 방향이 예상과 맞았다. 고친 값으로 CSF1R은 +12, 또 다른 골수 표지 유전자 S100A9는 +23.5로 나와, 둘 다 크로마틴이 먼저 열리는 쪽에 놓였다.

실수는 한 번 더 있었는데, 이번엔 결과를 해석하는 과정에서였다. 부호를 고친 뒤 시뮬레이터로 정확도를 재니 순위 일치도가 −0.89로 나왔다. 처음엔 "순위조차 되찾지 못한 실패"로 읽었지만, 다시 보니 오히려 그 반대였다. 크기로 따진 0.89는 추정기가 순위를 오히려 강하게 따라간다는 뜻이고, 정작 문제는 부호가 뒤집히고 크기가 크게 줄어든다는 데 있었다(참값 20~50 눈금이 되찾으면 −6~7로, 0.06배로 축소). 설정을 여러 가지로 바꿔 돌려도 순위 일치도는 한결같이 음수였다(−0.41~−0.86). 같은 숫자를 정반대로 읽을 뻔했다. 그래서 방향을 다루는 코드라면 크기보다 방향을 먼저 확인해야 한다는 교훈이 남았다.

![injected-lag 시뮬레이터: 정답 시간차(가로축)와 추정기가 되찾은 값(세로축). 순위는 강하게 따라가지만 부호가 뒤집히고 크기가 크게 줄어든다.](../pipeline/hspc-velocity-benchmark/figures/sim_injected_lag.png)

다만 이 문제가 미치는 범위는 좁다. 이런 왜곡은 CRAK-Velo의 추정 방식에서만 나타나므로, CRAK-Velo가 낸 시간차는 프로그램 간 비교에서 신뢰하지 않는다. 앞 글의 핵심 결론(MoFlow·MultiVelo·MultiVeloVAE 세 축)은 이 방식을 쓰지 않으니 그대로 유효하다. 오히려 부호를 바르게 통일하고 나자 MoFlow×CRAK-Velo 일치도는 +0.151에서 −0.151로 바뀌어, "시간차의 방향은 프로그램마다 갈린다"는 결론을 한 번 더 뒷받침했다. (여기 처음 적었던 방향 일치 비율 43.6%→32.4%는 이후 정정됐다. 시간차가 정확히 0이라 방향이 미정인 유전자를 세는 방식이 명시되지 않아 값이 흔들렸다. 그 91개를 빼고 다시 세면 **42.3%**(239개, 이항 p=0.020)로, 여전히 우연인 50%보다 유의하게 낮다. 결론은 그대로고 숫자만 바뀐다.)

## ⑤ 차용: 빌린 숫자도 통과해야 할 관문

마지막으로는 분석에 넣는 데이터 자체를 의심했다. 우리 분석에는 mRNA 반감기(전사가 멈춘 뒤 mRNA가 절반으로 줄어드는 시간)라는 통제 변수가 꼭 필요하다. 반감기가 긴 유전자는 전사가 멈춰도 mRNA가 천천히 사라져, 실제로는 꺼졌는데도 "느리게 반응하는 중"처럼 보이기 때문이다. 그런데 우리가 다루는 조혈세포(HSPC)에는 이 값을 잰 공개 데이터가 없고, 가장 가까운 것이 백혈병 세포다.

다른 세포에서 잰 숫자를 그냥 빌려 써도 될까? 자를 빌리는 일에 빗대 보자. 눈금 위치가 조금 달라도 "A가 B보다 길다"는 순서만 맞으면 물건을 재는 데는 지장이 없다. 우리도 반감기의 절대값까지는 필요하지 않고, 유전자들 사이의 순위만 있으면 된다. 그래서 기준 세포주(K562) 대비 다른 세포주 반감기의 순위상관을 관문으로 삼고, 통과선을 0.50으로 미리 정해 두었다.

검정에 쓸 비교셋은 성격이 서로 다른 셋으로 골랐다. 조혈세포와 비조혈세포를 함께 넣고, 같은 연구에서 잰 것과 다른 연구에서 잰 것을 섞었다. 쉬운 조건만 모아 통과시키는 일은 피했다.

| 비교셋 | 성격 | 전역 ρ | non-HK ρ |
|---|---|---|---|
| THP-1 | 조혈, 같은 연구(상한) | 0.743 | 0.700 |
| MOLM-13 | 조혈 AML, 다른 연구(주지표) | 0.695 | 0.659 |
| HEK293T | 비조혈, 다른 연구(하한) | 0.750 | 0.723 |

셋 다 통과선 0.50을 여유 있게 넘겼다(중앙값 0.74). 다만 값이 비슷해 보여도 무게는 다르다. 같은 연구에서 잰 THP-1의 0.743은 실험 조건이 겹쳐 부풀려진 상한이라, 대표 숫자로 앞세우면 안 된다. 우리 상황과 가장 비슷한 조건은 다른 연구에서 잰 조혈 백혈병 세포주 MOLM-13이고, 여기서 ρ=0.695가 나와 관문을 통과했다. 이 값이 좋은 편인지는 견줄 상한이 있어야 판단할 수 있다. 세포 종류가 아예 같은 경우(실험실만 다른 K562)의 순위 보존이 0.749였는데, 세포 종류까지 다른 MOLM-13이 0.695였으니 그 차이는 0.05에 그쳤다. 세포 종류를 바꿔도 순위는 실험실 간 기술 잡음 수준 이상으로는 거의 떨어지지 않았다. 반감기가 세포 환경보다 유전자 자체의 성질에 더 강하게 매여 있다는(gene-intrinsic) 근거다. 어느 세포에서나 늘 켜져 있는 housekeeping 유전자를 빼고 봐도 0.659~0.723으로 기준을 넘겼다.

![반감기 차용 관문: 기준 세포주 K562 대비 조혈 백혈병 세포주 MOLM-13의 유전자별 반감기 순위상관(ρ=0.695). 통과선 0.50을 넘겼다.](../pipeline/hspc-velocity-benchmark/proxy_join/out_gate/gate_molm13_rnadecaycafe.png)

단, 이 통과에는 두 가지 한계가 따른다. 우선 기준 세포주 유전자의 8.1%가 24시간 상한에 걸려 값이 잘려 있다. 또한 이 값은 조혈세포를 직접 잰 것이 아니라, 가장 가까운 백혈병 세포주에서 잰 값이다. 그래서 이번 검증으로는, 한계를 분명히 적어 두는 조건에서라면 반감기를 빌려 써도 된다는 데까지만 말할 수 있다. 약물 반응 타이밍을 예측하는 일은 그다음 문제이고, 따로 검증해야 한다.

## 다섯 가지 검증을 통과하고 남은 것

다섯 가지를 하나씩 확인해 보니 결과는 모두 같은 쪽을 가리켰다.

- **설계**: 프로그램끼리 답이 같다고 해서 그것을 정답으로 인정하지 않도록 벤치마크를 설계했다.
- **우연**: 우연을 엄격히 걸러내도 방향이 일관된 유전자는 0개였다.
- **교란**: 세포 분열 주기는 결론을 바꾸지 않았다.
- **코드**: 부호 버그를 찾아 고쳤다.
- **차용**: 빌려 온 반감기는 관문을 통과했다.

그래서 우리는 "시간차는 프로그램을 바꾸면 재현되지 않는다"는 결론을 냈다. 다섯 가지 검증을 모두 통과했으니 이 결과는 믿고 쓸 수 있다. 비재현성 결과일수록 이렇게 여러 단계의 검증을 거쳐 두면, 그 결과를 다음 연구에 활용할 수 있다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 시간차 (lag) | DNA가 열리고 나서 유전자가 켜지기까지의 간격(앞 글 참조) |
| 재현성 (reproducibility) | 프로그램·조건을 바꿔도 같은 값이 나오는 정도 |
| 다중검정·FDR | 유전자 수천 개를 한꺼번에 검정할 때 섞이는 우연을 걷어내는 통계(거짓 발견 비율) |
| 순열 검정 (permutation) | 라벨을 무작위로 섞은 가짜 데이터와 견줘 우연의 몫을 재는 방법 |
| 교란변수 (confound) | 진짜 원인이 아닌데 결과에 끼어드는 딴 요인(예: 세포 분열 주기) |
| within-lineage | 세포 계통을 섞지 않고 계통 안에서 따로 계산하는 것 |
| 음성 대조군 | 크로마틴–RNA 연결을 의도적으로 끊어 결과가 유지되는지 보는 시험 |
| gene-intrinsic | 세포 환경보다 유전자 자체의 성질에 강하게 매인 |
| housekeeping 유전자 | 어느 세포에서나 늘 비슷하게 켜져 있는 유전자 |

## 참고

**근거·코드**(수치 출처): `DESIGN.md`·`REVIEW-methodologist-2026-06-13.md`(벤치마크 설계), `results/permutation_fdr.md`(다중검정), `results/confound.md`·`results/cellcycle_genelevel.md`(교란 통제), `results/crakvelo_sign_check.md`·`results/sim_injected_lag.md`(부호 검증·시뮬레이터, 그림 `figures/sim_injected_lag.png`), `results/proxy_join_gate.md`·`PROXY-JOIN-DESIGN.md`(반감기 관문, 그림 `proxy_join/out_gate/gate_*.png`).

**관련 논문·데이터**
- MultiVelo — Li et al., *Nature Biotechnology* 41, 387–398 (2023). [doi:10.1038/s41587-022-01476-y](https://doi.org/10.1038/s41587-022-01476-y)
- MoFlow — Hong et al., *Nature Communications* 17, 566 (2025). [doi:10.1038/s41467-025-67259-6](https://doi.org/10.1038/s41467-025-67259-6)
- mRNA decay가 약물 반응 선택성을 좌우함 — Todorovski et al. (2024).

---
*이 글은 진행 중인 연구의 내부 정리이며, 세부 수치는 각 절에 링크한 결과 문서가 기준이다(연구·교육용).*

---

# Self-checking a result that does not reproduce

> TL;DR: In the previous post we reached a negative conclusion — the chromatin-to-transcription lag does not reproduce when you change the program. A negative result can also come from our own mistakes, so before publishing it we suspected five things in turn and checked each: the benchmark design, chance, confounders, our own code, and a borrowed number. Only after all five passed did we accept the conclusion as a measurement.

This post is the companion to "Does chromatin really 'prime' transcription?" Its conclusion was that the lag between the DNA around a gene opening and the gene turning on changes when you change the program — it does not reproduce.

Negative results carry a trap. "It does not reproduce" can mean the signal truly is not there, but it can also mean we slipped somewhere: a badly designed benchmark, chance mistaken for signal, a confounder, a bug in the code, or a borrowed dataset that should not have been used. To publish this claim, we first had to show the conclusion was not our own mistake. So before stating it, we suspected five things in turn.

```
Conclusion: "the lag does not reproduce across programs"
   │  how do we know this isn't our own mistake?
   ├─ 1. Design    is "programs agree" the same as "correct"?  → no (we ask only about reproducibility)
   ├─ 2. Chance    scrub the false patterns from thousands of genes  → 54.6% direction agreement (chance = 50%)
   ├─ 3. Confound  is it the cell cycle?  → only 1.9% of genes; not regressed out
   ├─ 4. Code      is our own sign right?  → one-line bug + a misread number, both fixed
   └─ 5. Borrowing may we borrow half-lives?  → passes the gate (ρ=0.695)
```

## 1. Design: agreement is not correctness

Imagine grading an exam with no answer key. Every student answers differently and there is no way to know who is right. Our data (GSE209878) is exactly like that: nothing in it marks when a gene actually switched on, so there is no ground truth for the lag.

So we changed the question: not "which program is accurate?" but "which lag survives a change of program?" Even without an answer key, we can ask how much different graders' scores overlap.

There is a trap here. If two graders trained at the same school with the same rubric, their agreement is not evidence of correctness — only of a shared bias. The same is true of programs: MoFlow descends from an earlier method (cellDancer), and MultiVeloVAE descends from MultiVelo. So the key comparison for reproducibility is between programs of different lineage (MultiVeloVAE vs MoFlow), and we always include an RNA-only floor that ignores chromatin, to see whether chromatin does any real work. Agreement is a necessary condition for reproducibility, not proof of truth — a line we drew from the first paragraph of the design.

## 2. Chance: the false patterns thousands of genes create

Test thousands of genes at once and a few will look "significant" purely by luck, even if there is no real signal — just as tossing thousands of coins yields a few "heads in a row" on their own. The statistics that strip out this luck are multiple-testing corrections, and the common yardstick is the false discovery rate (FDR).

Textbook FDR assumes the tests are independent, but genes are not: co-regulated genes move together. So we built a state with no real signal directly from the data. Shuffling gene labels 10,000 times (a permutation test) breaks the real links while keeping the correlation structure among genes, and we asked how far the real observation stands out from those fakes.

The first test measured how parallel each program pair's lags were:

| program pair | agreement ρ | q (FDR) |
|---|---|---|
| MoFlow × CRAK-Velo | −0.151 | 0.017 (sig.) |
| MoFlow × MultiVeloVAE | +0.083 | 0.051 (sig.) |
| CRAK-Velo × MultiVeloVAE | −0.040 | 0.471 |

Two of three pairs were significant against the fakes. But significant is not the same as strongly matching. Even the two significant pairs reached only 0.15 and 0.08 (0.5 is the bar for "moderate"), and one was negative — opposite direction. A large sample lets statistics catch even weak effects, but being caught does not make an effect large enough to use.

The second test took each gene one at a time and counted how consistently the programs agreed on the direction of its lag (DNA first, or gene first), and whether that consistency beat chance. Of 598 genes tested, 0 passed the strict bar (FDR 0.10).

**That "zero" has since been demoted from a headline.** We originally led with it; our own later audit showed it could not carry that weight, for two reasons. First, the 598-gene test needs three sign-variable programs, so it drops MultiVelo and **includes CRAK-Velo** — the very lag whose sign bug we flag later in this same post. Second, rerun on the clean pair alone (MoFlow and MultiVeloVAE), the test returns zero **whether or not there is signal**: with only two programs the smallest achievable per-gene p is about 0.5 (measured: 0.499), so no gene can clear any usable FDR threshold in principle. The result is not "no gene keeps a consistent direction" but "the test has no power to find one" — power-bounded.

The manuscript therefore moves 0/598 out of the headline and into a CRAK-inclusive **sensitivity analysis**, and leads on magnitude concordance instead (strongest pair +0.163, the rest at |ρ| ≤ 0.08). The clean number on the direction axis is a different one: MoFlow × MultiVeloVAE sign agreement of **54.6%** (560 genes, after excluding genes whose direction is undetermined; binomial p=0.031). Four and a half points off the 50% coin flip is nowhere near usable — but it is an honest number, and it is not "zero". The conclusion (lag direction does not reproduce across programs) stands; the number holding it up has changed.

## 3. Confound: why we saw a correlation and still did not regress it out

A factor that is not the real cause but slips into the result is a confounder. The most notorious one in single-cell analysis is the cell cycle: where a cell sits in its division cycle drags many genes' expression along. And indeed, cell by cell, the cell-cycle score moved together with the values we measure (correlation 0.33–0.36) — past the textbook 0.3 where one is told to consider regressing it out.

Reflexively removing it would have been a mistake. At the gene level the picture changed. Of the 538 genes with a value, only 10 (1.9%) were cell-cycle genes; their lags were not significantly different from the rest (Mann–Whitney p=0.862), and dropping them moved the median only from 5.87 to 5.83 (0.037).

The cell-level correlation had another source: cycling was strongly entangled with lineage. The fraction of actively dividing cells was 88% in megakaryocytes and 79% in the myeloid and erythroid lineages, but only 3% in HSC/MPP. Pour the cells into one pot and it looks like a "cell-cycle vs lag" correlation, but its true face is lineage structure. Computing within lineage already removes that entanglement, so we deliberately did not regress it out globally — doing so would have pulled the differentiation signal, tangled with cycling, out along with it. Here, not removing it was the more careful choice, and the cell cycle was reported as a sensitivity check, not a controlled variable.

## 4. Code: suspecting our own sign first

A lag carries both a magnitude ("how much") and a direction ("which came first"). The direction is written as a sign, and if the subtraction that computes the order writes `i−j` where it should write `j−i`, the sign flips wholesale — while the magnitude stays the same, so a test that checks only magnitude passes cleanly.

The alarm came from a marker gene. CSF1R, a myeloid marker, is reported in prior work to have pre-opened chromatin, so we expected a positive value; it came out at −12. (That "should be positive" is a literature-based expectation, not a ground truth we established. When we later ran the ATAC-shuffle control on the marker genes it came back null — p=0.58. The expectation was a useful clue for finding the bug, but marker direction should not be treated as an answer key.) Feeding in a synthetic switch signal where the DNA clearly opens first, MoFlow returned +30 (as promised) but CRAK-Velo returned −72 — the opposite sign. The fix was one line that reversed the subtraction order (`j−i`→`i−j`); afterward CRAK-Velo read +8, the right direction.

The second slip came in interpreting the result. After fixing the sign, a simulator put the rank agreement at −0.89. We first read it as "did not even recover the ranking," but the opposite was true: a magnitude of 0.89 means the estimator tracks the ranking strongly, and the real problem was that the sign flipped and the magnitude shrank sharply (a true range of 20–50 came back as −6 to 7, about 0.06×). The same number nearly read two opposite ways, which left one rule: code that handles direction must be checked for direction, not just magnitude.

![Injected-lag simulator: true lag (x-axis) versus the value the estimator recovers (y-axis). The ranking is tracked strongly, but the sign flips and the magnitude collapses.](../pipeline/hspc-velocity-benchmark/figures/sim_injected_lag.png)

We keep the scope narrow. This quirk belongs to CRAK-Velo's estimation alone, so we do not trust CRAK-Velo's lag in cross-program comparison. The previous post's core conclusion (the three axes MoFlow, MultiVelo, MultiVeloVAE) does not use this method and survives independently. If anything, unifying the sign correctly moved MoFlow × CRAK-Velo from +0.151 to −0.151, reinforcing that the lag's direction splits by program. (The direction-agreement figures first published here, 43.6% → 32.4%, were later corrected: the handling of genes whose lag is exactly zero — direction undetermined — was not specified, which moved the value. Excluding those 91 genes gives **42.3%** (n=239, binomial p=0.020), still significantly *below* the 50% coin flip. The conclusion is unchanged; the number is not.)

## 5. Borrowing: putting a borrowed number through a gate too

Finally, we questioned the input data itself. Our analysis needs a control variable: mRNA half-life (how long after transcription stops the mRNA falls to half). A gene with a long half-life keeps its mRNA long after transcription has stopped, so it looks like it is "still responding slowly" when it is already off. But there is no public half-life dataset for the hematopoietic cells (HSPCs) we study; the nearest is leukemia cells.

May we simply borrow another cell type's numbers? Think of borrowing a ruler. Its zero and spacing may differ a little, but as long as the order "A is longer than B" holds, it measures fine. What we use is not the absolute half-life but the ranking among genes. So we made the rank correlation of another cell line's half-lives against a reference line (K562) the gate, and fixed the pass mark at 0.50 in advance.

It passed. In the condition closest to ours — a hematopoietic leukemia line measured in a different study (MOLM-13) — ρ was 0.695. Whether that is good is judged against an upper bound: the same cell type across labs (K562) preserved rank at 0.749, and MOLM-13, a different cell type, reached 0.695 — a gap of only 0.05. Changing the cell type barely lowered the ranking beyond cross-lab technical noise, evidence that half-life is strongly gene-intrinsic (tied to the gene more than to the cell environment). Even excluding housekeeping genes (always-on in every cell), the values held at 0.659–0.723, above the bar.

![Half-life borrowing gate: per-gene rank correlation of half-lives between the reference line K562 and the hematopoietic leukemia line MOLM-13 (ρ=0.695), clearing the 0.50 pass mark.](../pipeline/hspc-velocity-benchmark/proxy_join/out_gate/gate_molm13_rnadecaycafe.png)

This pass comes with two limits, though. First, 8.1% of the reference line's genes are censored at a 24-hour ceiling. Second, these values were not measured in hematopoietic cells directly, but in the nearest leukemia line. So what we have shown is only that borrowing the half-life is justified, provided the limits are stated. Predicting drug-response timing is a separate question, still to be tested.

## What is left after all five

All five checks pointed the same way.

- **Design**: the benchmark was built so that programs agreeing is not treated as being correct.
- **Chance**: even after strictly removing chance, no gene kept a consistent direction.
- **Confound**: the cell cycle did not change the conclusion.
- **Code**: the sign bug was found and fixed.
- **Borrowing**: the borrowed half-life passed its gate.

So we concluded that the lag does not reproduce across programs. Having passed all five checks, the result is trustworthy. The more negative a result, the more rounds of verification it takes before it can be used in later research.

## Glossary

| Term | Meaning |
|---|---|
| lag | The gap between the DNA opening and the gene turning on (see previous post) |
| reproducibility | The degree to which the same value appears when program or setting changes |
| multiple testing / FDR | Statistics that remove the luck mixed in when thousands of genes are tested at once (false discovery rate) |
| permutation test | Measuring the share due to chance by comparing against label-shuffled fake data |
| confounder | A factor that is not the real cause but slips into the result (e.g. the cell cycle) |
| within-lineage | Computing inside each cell lineage rather than mixing lineages |
| negative control | Deliberately breaking the chromatin–RNA link to see whether the result holds |
| gene-intrinsic | Tied to the gene itself more than to the cell environment |
| housekeeping gene | A gene kept similarly on in every cell type |

## References

**Evidence and code** (sources of the numbers): `DESIGN.md` · `REVIEW-methodologist-2026-06-13.md` (benchmark design), `results/permutation_fdr.md` (multiple testing), `results/confound.md` · `results/cellcycle_genelevel.md` (confound control), `results/crakvelo_sign_check.md` · `results/sim_injected_lag.md` (sign check and simulator; figure `figures/sim_injected_lag.png`), `results/proxy_join_gate.md` · `PROXY-JOIN-DESIGN.md` (half-life gate; figure `proxy_join/out_gate/gate_*.png`).

**Related work and data**
- MultiVelo — Li et al., *Nature Biotechnology* 41, 387–398 (2023). [doi:10.1038/s41587-022-01476-y](https://doi.org/10.1038/s41587-022-01476-y)
- MoFlow — Hong et al., *Nature Communications* 17, 566 (2025). [doi:10.1038/s41467-025-67259-6](https://doi.org/10.1038/s41467-025-67259-6)
- mRNA decay governs drug-response selectivity — Todorovski et al. (2024).

---
*Internal working note from ongoing research; detailed numbers follow the results documents linked in each section (research and educational use).*

---

# 한 데이터의 결론을 어떻게 믿을까 — 조직·종을 바꿔 본 재현

> 한 줄 요약: 앞 두 글의 결론(전사 속도 α는 프로그램을 바꿔도 튼튼하고, 시간차는 약하다)은 사람 조혈세포 한 데이터에서 나왔다. 그래서 같은 분석을 다른 데이터에 그대로 걸었다. 종도 조직도 다른 생쥐 배아 뇌(먼 재현), 그리고 같은 조혈 조직인 사람 골수(가까운 재현)에서 α가 시간차보다 잘 맞는 순서가 되풀이됐다.

이 글은 앞 두 글의 후속편이다. 첫 글에서 우리는 DNA가 열리고 나서 유전자가 켜지기까지의 시간차(lag)가 계산 프로그램을 바꾸면 값이 달라져 재현되지 않는다는 결론에 이르렀고, 전사 속도(α)는 프로그램을 바꿔도 값이 일정하다는 것을 함께 확인했다. 둘째 글에서는 그 비재현성 결론이 우리 실수가 아님을 다섯 가지 자기 검증으로 확인했다. 이 연구가 다루는 큰 질문은 크로마틴(chromatin, DNA가 감긴 실타래)이 열리는 순서로 전사를 예측할 수 있느냐이고, 우리는 그 예측 재료로 삼으려던 시간차부터 검증했다. 그런데 지금까지의 결론은 모두 한 데이터에서만 나왔다.

한 데이터에서 아무리 깔끔한 결론이 나와도, 그것만으로는 그 데이터에만 있는 특성인지 어디서나 통하는 현상인지 가를 수 없다. 심사자가 "그건 그 조혈 데이터가 특이해서 그런 것 아니냐"고 물으면, 데이터가 하나뿐인 우리는 내놓을 답이 마땅치 않다. 그래서 같은 분석 방법을 다른 데이터에 그대로 적용해, 결론이 조직과 종을 넘어 살아남는지 본다. 이렇게 다른 데이터에서도 같은 결과가 나오는지 확인하는 일을 재현(replication)이라 한다. 이 글은 그 재현의 기록이다.

재현에는 거리가 있다. 원래 데이터와 같은 조직에서 다시 보는 것은 가까운 재현이고, 종과 조직이 모두 다른 데서 다시 보는 것은 먼 재현이다. 거리가 멀수록 값이 그대로 보존되기는 어렵지만, 그래도 같은 결론이 나온다면 그만큼 일반적이라는 뜻이 된다.

```
        사람 조혈세포(HSPC) 한 데이터에서 얻은 결론
              α는 튼튼하다 / 시간차는 약하다
                          │
          같은 결론이 다른 데이터에서도 나오나?
     ┌────────────────────┴────────────────────┐
  가까운 재현                                 먼 재현
  사람 골수(BMMC)                          생쥐 배아 뇌(E18)
  같은 조혈 조직                            다른 종·다른 조직
```

## 두 가지 비교: 프로그램을 바꿀 때와 데이터를 바꿀 때

재현을 이야기하기 전에 두 종류의 비교를 갈라 둬야 한다. 뒤에 나오는 숫자가 어느 쪽 비교인지 헷갈리면 결론이 과장되기 때문이다.

하나는 한 데이터 안에서 프로그램만 바꿔 견주는 비교다(within-dataset). 같은 세포, 같은 전처리에서 시작해 프로그램 여러 개로 값을 뽑고 서로 맞대 본다. 첫 글에서 "α는 프로그램을 바꿔도 ρ=0.88로 일정하다"고 한 것이 이 비교다.

다른 하나는 프로그램은 같은 것을 쓰되 데이터를 통째로 바꿔 견주는 비교다(cross-dataset). 사람 조혈세포에서 어느 유전자의 α가 큰지의 순위를, 생쥐 뇌에서 잰 순위와 맞대 본다. 이 비교는 데이터가 다르니 값이 더 약하게 나올 수밖에 없다.

두 비교 모두에서 물음은 같다. α가 시간차보다 더 잘 재현되는가. 앞으로 나오는 재현도 값은 순위 일치도(Spearman ρ)로, −1에서 +1 사이다. 경험칙으로 0.5는 넘어야 "어느 정도 맞는다", 0.7을 넘으면 "잘 맞는다"고 본다. 0 근처는 상관 관계가 없다는 뜻이다.

## 먼 재현: 생쥐 배아 뇌

첫 재현은 원래 데이터에서 가장 멀리 떨어진 데이터를 골랐다. 생쥐 배아 뇌(10x Multiome E18)는 종도 조직도 사람 조혈세포와 전혀 다르다. 여기서 같은 결론이 나온다면, 우리 결론이 조혈세포에 매인 특성이 아니라는 강한 근거가 된다.

한 데이터 안에서 프로그램을 바꿔 본 결과부터 보자. 전사 속도 α는 프로그램이 달라도 잘 맞았다. RNA만 쓰는 기준선과 MultiVelo가 ρ=+0.78, 기준선과 MultiVeloVAE가 +0.81, 크로마틴을 쓰는 두 프로그램(MultiVelo×MultiVeloVAE)이 +0.90으로, 중앙값이 +0.81이었다. 세 값 모두 "잘 맞는다"고 볼 0.7을 넘거나 그에 가깝다. 반면 시간차는 크로마틴을 쓰는 두 프로그램에서만 잴 수 있는데, 그 일치도가 +0.06에 그쳤다. α는 튼튼하고 시간차는 약하다는, 사람 조혈세포에서 봤던 그 대비가 종이 다른 데이터 안에서도 그대로 나왔다.

데이터를 건너 견준 결과도 같은 쪽을 가리켰다. 생쥐와 사람은 유전자 이름 표기가 달라(생쥐 Gata1, 사람 GATA1) 대문자로 맞춰 겹치는 유전자 132개를 찾아 비교했다. α의 순위 일치도가 +0.32로, 데이터를 건너뛰었는데도 양수로 남았다. 같은 재료로 시간차를 견주면 +0.10에 머물렀다. 데이터를 바꿨을 때도 α가 시간차보다 잘 맞는 순서가 지켜졌다.

짚어 둘 한계가 있다. 여기서 시간차 비교는 크로마틴을 쓰는 프로그램 한 쌍(MultiVelo×MultiVeloVAE)으로만 봤다. 사람 조혈세포에서는 세 쌍으로 봤으니 그보다 얇은 근거다. 또 이 비교는 시간차의 크기 순위만 본 것이고 방향(DNA가 먼저인지 유전자가 먼저인지)은 보지 않았다. MultiVelo의 시간차 부호는 내부 구조상 늘 양수로 고정되어 나와, 방향 비교로는 뜻이 없기 때문이다. 그리고 외부 데이터 재현은 아직 한 건이다.

## 가까운 재현: 사람 골수

두 번째 재현은 반대로, 원래 데이터에 가장 가까운 데이터를 골랐다. 사람 골수(BMMC, GSE194122)는 원래 데이터인 사람 조혈세포와 같은 조혈 축에 있다. 종도 같고 조직도 같으니, 지금까지 시도한 것 중 가장 가까운 재현이다.

가까운 만큼 이 데이터는 준비 과정이 더 까다로웠다. 시간차와 전사 속도를 재려면 갓 만들어져 아직 다듬어지지 않은 RNA(unspliced)와 다듬어진 RNA(spliced)를 나눠 세어야 하는데, 공개된 골수 데이터에는 이 구분이 없었다. 대신 원본을 만들 때 쓴 대용량 유전체 파일(28기가바이트)이 공개돼 있어, 거기서부터 우리가 직접 계산해 되살렸다. 무거운 다운로드와 밤샘 계산에 들어가기 전에, 되살리기가 애초에 가능한지부터 값싸게 확인하는 관문을 뒀다. 우리가 가진 세포 목록(바코드 4,325개)과 대용량 파일 앞부분에서 뽑은 세포 표식(26,635개)의 형식이 양쪽 모두 `<16염기>-1`로 같았고, 우리 세포의 92.2%가 그 앞부분만으로도 이미 잡혔다. 관문을 통과한 뒤에야 전체 계산을 돌렸다.

같은 골수 데이터 안에서 프로그램을 바꿔 보니, 전사 속도 α의 일치도가 세 쌍에서 +0.82, +0.85, +0.91로 나와 중앙값이 +0.85였다. 이는 원래의 사람 조혈세포에서 본 +0.88과 거의 같다. 튼튼하다던 α가 같은 조직에서 가장 강하게 되풀이된 것이다. 시간차는 크로마틴을 쓰는 두 프로그램에서 −0.09로, 여기서도 상관 관계가 없었다.

데이터를 건너 견준 결과도 같은 방향이었다. 둘 다 사람 조혈세포라 유전자 이름이 직접 겹쳐, 겹치는 88개 유전자로 비교했다. α의 순위 일치도가 +0.55로, 앞의 먼 재현(+0.32)보다 높았다. 조직이 가까울수록 잘 맞는다는 상식과 들어맞는다. 시간차는 같은 비교에서 +0.05에 머물렀다.

여기에도 분명히 적어 둘 한계가 있다. 우리가 RNA를 되살린 방식(BAM 파일에서 velocyto로 unspliced/spliced 복구)과 크로마틴 신호를 유전자 단위로 모은 방식이 원래 조혈세포 파이프라인과 구현이 다르다. 이 차이는 데이터를 건너 견줄 때 잡음을 더할 뿐이라, 오히려 일치도를 실제보다 낮게 나오게 한다. 이 데이터도 공여자 한 명, 샘플 하나에서 나온 재현 한 건이고, 시간차가 약하다는 대목은 프로그램 한 쌍으로만 확인했다.

## 통합: 조직 거리 순 재현도

세 번째 데이터인 사람 뇌까지 더해, 데이터를 건너 견준 재현도를 조직 거리 순으로 늘어놓으면 이렇다. 사람 뇌는 종은 같고 조직은 다른, 가까운 재현과 먼 재현의 중간이다.

| 재현 데이터 | 조직 거리 | 건너서 잰 α 일치도 | 건너서 잰 시간차 일치도 |
|---|---|---|---|
| 사람 골수(BMMC) | 같은 조직(가장 가까움) | +0.55 | +0.05 |
| 사람 뇌 | 같은 종, 다른 조직 | +0.475 | +0.19 |
| 생쥐 배아 뇌(E18) | 다른 종, 다른 조직 | +0.32 | +0.10 |

전사 속도 α는 조직이 가까워질수록 일치도가 꾸준히 올라간다(+0.32 → +0.475 → +0.55). 시간차는 어디서 재도 +0.05에서 +0.19 사이에 머물러, "어느 정도 맞는다"고 볼 0.5에 한참 못 미친다. DNA가 열리고 유전자가 켜지기까지의 그 시간차는, 프로그램을 바꾸면 가장 가까운 조직에서조차 다시 나타나지 않았다.

![데이터셋별 재현 일치도(순위상관 ρ): E18 생쥐 뇌·사람 뇌·사람 골수 모두에서 전사 속도 α(초록)가 크로마틴→전사 시간차(빨강)보다 높다. 참고로 같은 조혈세포 안에서 프로그램만 바꾸면 α ρ=0.88, 시간차 ρ≈0.](../pipeline/hspc-velocity-benchmark/figures/fig02_crossdataset_concordance.png)

여기서 주장의 크기를 정확히 맞춰 둔다. 우리 주장은 순서에 관한 것이다. 어느 데이터에서 재든, 그리고 프로그램을 바꾸든 데이터를 바꾸든, α가 시간차보다 늘 더 잘 맞았다. 이 순서가 사람 조혈세포·사람 뇌·생쥐 배아 뇌·사람 골수 네 데이터에서 지켜졌다. 다만 α의 값 자체가 종을 넘어 그대로 보존된다는 데까지는 나아가지 않는다. 종이 다르면 α도 약해져, 한 데이터 안에서 +0.8이던 일치도가 데이터를 건너뛰면 +0.32까지 내려가기 때문이다.

## 결론

α는 튼튼하고 시간차는 약하다는 결론이 데이터 한 벌을 넘어 유지됐다. 한 데이터 안에서 프로그램을 바꿀 때도, 데이터를 통째로 바꿀 때도 α가 시간차보다 잘 맞았다. 종도 조직도 다른 생쥐 뇌에서, 같은 조혈 조직인 사람 골수에서도 마찬가지였다. 그래서 굳이 둘 중 하나를 발판으로 삼는다면 시간차가 아니라 α다. 프로그램을 바꾸면 값이 달라지는 시간차는 발판으로 쓰기 어렵다.

**다만 여기서 한 걸음 더 나가면 안 된다.** 이 글이 처음에 "약물 반응 타이밍을 예측할 때도 이 α를 발판으로 삼는 편이 옳다"고 적은 것은 "α가 시간차보다 재현된다"(순서)에서 "α를 예측에 쓰는 게 옳다"(효용)로 건너뛴 것이다. 재현된다는 것과 쓸모가 있다는 것은 다른 이야기이고, 우리 데이터는 후자를 뒷받침하지 않는다. 결정적인 것은 **비교 기준선**이다 — α를 외부 측정(K562 TT-seq 합성률)에 대보면 순위가 +0.24~+0.29로 맞는데, 아무 모델도 거치지 않은 **발현량**을 같은 측정에 대보면 +0.410으로 오히려 더 잘 맞는다. 즉 α가 발현량을 넘어서는 정보를 준다는 근거가 아직 없다. 정확한 권고는 "α를 발판으로 삼으라"가 아니라, **먼저 발현량만으로 답이 나오는지 확인하고, 그래도 부족할 때 α를 보되 발현량 기준선과 나란히 놓고 보라**이다.

일반화의 크기는 좁게 잡아 둔다. 세 재현은 저마다 공여자 한 명, 샘플 하나에서 나왔으니 아직 강한 일반화는 이르다. 시간차가 약하다는 대목도 사람 골수와 생쥐 뇌에서는 프로그램 한 쌍으로만 확인했고, 사람 조혈세포에서 세 쌍으로 본 것보다 얇은 근거다. 그럼에도 네 데이터가 같은 순서를 가리키므로 결론 자체는 일관된다. 이로써 결론이 단일 데이터에서만 나온 것이라는 반론은 약해진다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 재현 (replication) | 다른 데이터에서도 같은 결과가 나오는지 확인하는 일. 조직·종이 가까우면 가까운 재현, 멀면 먼 재현 |
| 시간차 (lag) | DNA가 열리고 나서 유전자가 켜지기까지의 간격(앞 글 참조) |
| 전사 속도 (α) | 유전자가 켜졌을 때 RNA를 만드는 빠르기(앞 글 참조) |
| within-dataset | 한 데이터 안에서 프로그램만 바꿔 값을 견주는 비교 |
| cross-dataset | 프로그램은 같게 두고 데이터를 통째로 바꿔 값을 견주는 비교 |
| 순위 일치도 ρ | 두 값이 얼마나 맞는지(−1~+1). 0.5는 넘어야 "어느 정도", 0.7 이상이면 "잘 맞음" |
| unspliced / spliced RNA | 갓 만들어 아직 안 다듬어진 RNA / 다듬어진 RNA. 시간차·전사 속도 계산에 둘의 구분이 필요 |
| 관문 (preflight gate) | 무거운 작업 전에 될지 안 될지를 값싸게 먼저 가르는 확인 |
| BMMC | 사람 골수 단핵세포(bone marrow mononuclear cell). 여러 혈액세포로 분화하는 조혈 조직 |
| HSPC | 조혈모·전구세포. 원래 데이터(GSE209878)의 세포 |

## 참고

**근거·코드**(수치 출처): `results/concordance_e18_mouse_brain.md`(생쥐 배아 뇌 재현), `results/concordance_GSE194122_bmmc.md`(사람 골수 재현), `results/concordance_human_brain.md`(사람 뇌 재현), `cross_dataset/BMMC_PREFLIGHT_GATE.md`(복구 가능성 관문), `cross_dataset/p3_concordance_*.py`(재현도 계산), `results/FINDINGS.md`(종합).

**관련 논문·데이터**
- MultiVelo — Li et al., *Nature Biotechnology* 41, 387–398 (2023). [doi:10.1038/s41587-022-01476-y](https://doi.org/10.1038/s41587-022-01476-y)
- MoFlow — Hong et al., *Nature Communications* 17, 566 (2025). [doi:10.1038/s41467-025-67259-6](https://doi.org/10.1038/s41467-025-67259-6)
- 사람 골수 재현 데이터(BMMC) — GSE194122 (NeurIPS 2021 Multimodal Single-Cell).

---
*이 글은 진행 중인 연구의 내부 정리이며, 수치는 현재 분석 기준이라 후속 검증으로 갱신될 수 있다(연구·교육용).*

---

# How do you trust a conclusion from one dataset? Replicating it across tissues and species

> TL;DR: The conclusion from the first two posts — the transcription rate α is stable across programs while the lag is not — came from a single dataset of human hematopoietic cells. So we applied the same analysis to other data. In mouse embryonic brain (a far replication, different species and tissue) and in human bone marrow (a near replication, the same hematopoietic tissue), the ordering held: α matched better than the lag.

This post follows the previous two. In the first, we concluded that the lag between the DNA around a gene opening and the gene turning on changes when you swap programs — it does not reproduce — while the transcription rate (α) stays stable across programs. In the second, we confirmed through five self-checks that this negative result was not our own mistake. The larger question this research asks is whether the order in which chromatin (the thread of protein-wound DNA) opens can predict transcription, and we started by vetting the lag we meant to use as a predictor. But every conclusion so far came from one dataset.

However clean a conclusion from a single dataset, it alone cannot tell whether it reflects a quirk of that data or something that holds everywhere. If a reviewer asks, "Isn't that just because your hematopoietic data are unusual?", a lab with only one dataset has no ready answer. So we apply the same analysis to other data and see whether the conclusion survives across tissue and species. Checking whether the same result appears in other data is what replication means, and this post is that record.

Replication comes in distances. Rerunning in the same tissue as the original is a near replication; rerunning where both species and tissue differ is a far replication. The greater the distance, the harder it is for values to be preserved intact — but if the same conclusion still appears, that speaks to how general it is.

```
        Conclusion from one human HSPC dataset
             α is robust / the lag is fragile
                          │
        Does the same conclusion appear in other data?
     ┌────────────────────┴────────────────────┐
  near replication                          far replication
  human bone marrow (BMMC)              mouse embryonic brain (E18)
  same hematopoietic tissue             different species & tissue
```

## Two comparisons: swapping the program vs. swapping the data

Before talking about replication, two kinds of comparison have to be kept apart. If it is unclear which comparison a number belongs to, the conclusion gets overstated.

One is comparing programs within a single dataset (within-dataset). Starting from the same cells and the same preprocessing, we compute values with several programs and set them against each other. When the first post said "α is stable across programs at ρ=0.88," that was this comparison.

The other keeps the program the same but swaps the whole dataset (cross-dataset). We take the ranking of which gene has a large α in human hematopoietic cells and set it against the ranking measured in mouse brain. Because the data differ, values here are necessarily blurrier.

In both comparisons the question is the same: does α reproduce better than the lag? The replication figures below are rank agreements (Spearman ρ), between −1 and +1. As a rule of thumb, a value needs to clear 0.5 to count as "moderate" and 0.7 to count as "strong"; near zero means no correlation.

## Far replication: mouse embryonic brain

The first replication moves the stage as far as it goes. Mouse embryonic brain (10x Multiome, E18) differs from human hematopoietic cells in both species and tissue. If the same conclusion appears here, that is strong evidence it is not tied to hematopoietic cells.

Start with swapping programs within the one dataset. The transcription rate α matched well across programs: the RNA-only baseline vs. MultiVelo at ρ=+0.78, the baseline vs. MultiVeloVAE at +0.81, and the two chromatin-aware programs (MultiVelo × MultiVeloVAE) at +0.90 — a median of +0.81. All three clear or approach the 0.7 bar for "strong." The lag, which can only be measured in the two chromatin-aware programs, reached only +0.06. The contrast seen in human hematopoietic cells — α robust, lag fragile — appeared intact inside data from a different species.

The cross-dataset comparison pointed the same way. Because mouse and human write gene names differently (mouse Gata1, human GATA1), we matched them in uppercase and found 132 shared genes. The rank agreement of α was +0.32 — positive even across a jump between datasets. The lag over the same material reached only +0.10. Even when the data changed, α matched better than the lag.

A limit worth stating: the lag comparison here rests on a single program pair (MultiVelo × MultiVeloVAE). In human hematopoietic cells it rested on three pairs, so this is thinner evidence. This comparison also looks only at the rank of the lag's magnitude, not its direction (DNA first or gene first), because MultiVelo's lag sign comes out fixed positive by its internal structure and carries no directional information. And this external replication is still a single case.

## Near replication: human bone marrow

The second replication instead pulls the stage as close as it comes. Human bone marrow (BMMC, GSE194122) sits on the same hematopoietic axis as the original human hematopoietic data. Same species, same tissue — the closest replication we have attempted.

Being close, this dataset took more work. Measuring the lag and α requires counting freshly made, not-yet-spliced RNA (unspliced) separately from spliced RNA, but the public bone marrow data lacked this split. The large genomic file (28 GB) used to build the original was available, so we recomputed the split from it ourselves. Before committing to the heavy download and overnight computation, we set a cheap gate to check whether recovery was even possible. Our cell list (4,325 barcodes) and the cell tags sampled from the head of the large file (26,635) shared the same format on both sides (`<16 bases>-1`), and 92.2% of our cells were already found in that head-sample alone. Only after the gate passed did we run the full computation.

Swapping programs within the one bone marrow dataset, the α agreement came out at +0.82, +0.85, and +0.91 across the three pairs, a median of +0.85. That is nearly the same as the +0.88 seen in the original human hematopoietic cells. The α called robust reproduced most strongly in the same tissue. The lag, in the two chromatin-aware programs, was −0.09 — again no correlation.

The cross-dataset comparison pointed the same way. Both being human hematopoietic cells, the gene names overlap directly, so we compared over 88 shared genes. The rank agreement of α was +0.55 — higher than the far replication (+0.32). This matches the intuition that closer tissues match better. The lag over the same comparison stayed at +0.05.

Here too there is a limit to state plainly. The way we recovered the RNA (unspliced/spliced from a BAM file via velocyto) and aggregated the chromatin signal to the gene level differs in implementation from the original hematopoietic pipeline. This difference only adds noise to the cross-dataset comparison, which if anything pushes the agreement lower than it really is. This dataset too is a single replication from one donor and one sample, and the weakness of the lag was confirmed with only one program pair.

## Putting it together: replication by tissue distance

Adding a third dataset, human brain, and laying out the cross-dataset replication by tissue distance gives the following. Human brain, same species but different tissue, sits between the near and far replications.

| replication data | tissue distance | cross-measured α agreement | cross-measured lag agreement |
|---|---|---|---|
| human bone marrow (BMMC) | same tissue (closest) | +0.55 | +0.05 |
| human brain | same species, different tissue | +0.475 | +0.19 |
| mouse embryonic brain (E18) | different species, different tissue | +0.32 | +0.10 |

The transcription rate α climbs steadily as the tissue gets closer (+0.32 → +0.475 → +0.55). The lag stays between +0.05 and +0.19 wherever it is measured, far short of the 0.5 bar for "moderate." That gap between the DNA opening and the gene turning on did not revive under a change of program even in the closest tissue.

![Cross-dataset replication (rank Spearman ρ): in every dataset (E18 mouse brain, human brain GSE162170, human BMMC), transcription rate α (green) exceeds the chromatin→transcription lag (red). Within-HSPC reference: α cross-method ρ=0.88, lag ρ≈0.](../pipeline/hspc-velocity-benchmark/figures/fig02_crossdataset_concordance.png)

Let me size the claim precisely. We are not saying α is preserved intact across species. When the species differs, α blurs too: an agreement of +0.8 within a single dataset falls to +0.32 once you jump between datasets. Our claim is about ordering. Wherever it is measured, and whether you swap the program or swap the data, α matched better than the lag. That ordering held across four datasets — human hematopoietic cells, human brain, mouse embryonic brain, and human bone marrow.

## Conclusion

The conclusion that α is robust and the lag is fragile held beyond a single dataset. Swapping programs within one dataset, swapping the dataset whole, in mouse brain of a different species and tissue, and in human bone marrow of the same hematopoietic tissue — in all of them α matched better than the lag. So if either of the two is to serve as a foothold, it is α rather than a lag that shifts when the program changes.

**But we should not take the next step.** This post originally said α is the sounder footing "for predicting drug-response timing too" — a jump from "α reproduces better than the lag" (an ordering) to "α should be used for prediction" (a utility). Reproducing and being useful are different claims, and our data do not support the second. The decisive point is the **baseline**: α ranks with external measurement (K562 TT-seq synthesis) at +0.24 to +0.29, but plain transcript **abundance** — no model involved — ranks with the same measurement at +0.410, more strongly. There is as yet no evidence that α adds information beyond abundance. The accurate recommendation is not "use α as your foothold" but: **check first whether abundance alone answers the question, and if you do reach for α, read it alongside the abundance baseline.**

We keep the size of the generalization honest. Each of the three replications came from one donor and one sample, so a strong generalization is still premature. The weakness of the lag was confirmed with only one program pair in human bone marrow and mouse brain — thinner evidence than the three pairs in human hematopoietic cells. Even so, all four datasets point to the same ordering, so the conclusion itself is consistent. The "you only have one dataset" objection is weakened by this.

## Glossary

| Term | Meaning |
|---|---|
| replication | Checking whether the same result appears in other data; a near replication if the tissue/species is close, a far replication if distant |
| lag | The gap between the DNA opening and the gene turning on (see previous post) |
| transcription rate (α) | How fast a gene makes RNA once it is on (see previous post) |
| within-dataset | Comparing values by swapping only the program within one dataset |
| cross-dataset | Comparing values by swapping the whole dataset while keeping the program the same |
| rank agreement ρ | How well two values match (−1 to +1); needs 0.5 to be "moderate," ≥0.7 to be "strong" |
| unspliced / spliced RNA | Freshly made, not-yet-spliced RNA / spliced RNA; the split is needed to compute the lag and α |
| preflight gate | A cheap check before heavy work to sort out whether it will work at all |
| BMMC | Bone marrow mononuclear cells — hematopoietic tissue that gives rise to many blood cells |
| HSPC | Hematopoietic stem/progenitor cells — the cells of the original dataset (GSE209878) |

## References

**Evidence and code** (sources of the numbers): `results/concordance_e18_mouse_brain.md` (mouse embryonic brain replication), `results/concordance_GSE194122_bmmc.md` (human bone marrow replication), `results/concordance_human_brain.md` (human brain replication), `cross_dataset/BMMC_PREFLIGHT_GATE.md` (recovery-feasibility gate), `cross_dataset/p3_concordance_*.py` (replication computation), `results/FINDINGS.md` (synthesis).

**Related work and data**
- MultiVelo — Li et al., *Nature Biotechnology* 41, 387–398 (2023). [doi:10.1038/s41587-022-01476-y](https://doi.org/10.1038/s41587-022-01476-y)
- MoFlow — Hong et al., *Nature Communications* 17, 566 (2025). [doi:10.1038/s41467-025-67259-6](https://doi.org/10.1038/s41467-025-67259-6)
- Human bone marrow replication data (BMMC) — GSE194122 (NeurIPS 2021 Multimodal Single-Cell).

---
*Internal working note from ongoing research; numbers reflect the current analysis and may be updated by further validation (research and educational use).*

---

# 재현 가능한 연구로: 분석을 하네스로 옮기기

> 한 줄 요약: 좋은 분석은 결과만으로는 부족하다. 다른 사람이, 또는 자동으로 실행하는 프로그램이 같은 절차를 그대로 다시 돌릴 수 있어야 한다. 그러려면 무엇을 할지 적은 지침과 그것을 돌리는 코드를 갈라 둔다. 이 틀은 박상준 님(@poqopo)이 만든 Harness_Baseline을 반입해 우리 파이프라인에 맞춘 것이고, 실행은 OpenClaw 기반으로 연습하는 중이다.

앞 세 글에서는 결과를 다뤘다. 전사 속도(α)는 계산 프로그램을 바꿔도 값이 일정했고, DNA가 열리고 나서 유전자가 켜지기까지의 시간차(lag)는 프로그램을 바꾸면 재현되지 않았으며, 이 순서가 다른 조직·다른 종에서도 되풀이됐다. 이번 글은 결과에서 한 걸음 물러나, 그 결과를 낸 절차를 다룬다. 반년 뒤의 나 또는 옆자리 동료가 같은 분석을 그대로 다시 돌리려면 무엇이 갖춰져 있어야 하는가. 이 물음에 답하려고 분석 절차를 하네스(harness)라는 틀에 옮겨 담았다.

## 핵심 개념: 지침과 코드의 분리

폴더를 열고 예전 명령을 똑같이 다시 입력했는데 아무것도 돌지 않는 상황을 떠올려 보자. 무엇을 어느 자리에 어떤 순서로 넣어야 하는지가 처음 짠 사람 머릿속에만 있으면 이렇게 된다. 그래서 좋은 분석은 결과만 좋아서는 오래가지 못한다. 다른 사람이 같은 절차를 되짚어 돌릴 수 있어야 쓸모가 남는다.

분석을 다시 돌게 만들려면 늘 붙어 다니던 두 가지, 곧 무엇을 할지 적은 지침과 그것을 실제로 돌리는 코드를 갈라 두면 된다. 둘이 붙어 있으면 처음 짠 사람만 분석을 다시 돌릴 수 있다. 갈라 두면 데이터와 작업 이름만 대도 같은 절차를 다시 돌릴 수 있다.

조리법에 빗대면 이렇다. 조리법이 한 장의 종이에 적혀 있고 재료와 도구가 정해진 자리에 있으면, 요리사가 바뀌어도 같은 음식이 나온다. 조리법이 한 사람 머릿속에만 있으면, 그가 자리를 비운 날엔 아무도 그 음식을 못 만든다. 종이에 적힌 조리법이 지침이고, 재료와 화구가 갖춰진 주방이 코드다. 이렇게 지침과 코드를 갈라 감싼 틀을 하네스라 부른다.

![재현 가능 하네스 개념도: 지침(무엇: SKILL.md·ROUTES·dataset→task)과 코드(어떻게: scripts/)를 갈라 두면, dataset과 task 이름만으로 같은 절차를 사람 또는 OpenClaw가 다시 돌릴 수 있다.](../pipeline/hspc-velocity-benchmark/figures/fig04_harness_concept.png)

## 배경: 남이 만든 틀을 반입

이 틀을 백지에서 짜지는 않았다. 박상준 님(@poqopo)이 만든 Harness_Baseline이라는 틀을 반입해 우리 파이프라인에 맞게 고쳤다. 잘 다듬어진 조리법 서식을 얻어다 우리 재료에 맞추는 방식이다. 원저작자는 박상준 님이고, 원 저장소에 라이선스 표기가 없어 공유·수정은 박상준 님의 동의를 전제로 한다. 이 출처와 조건은 반입한 문서 머리에 그대로 적어 두었다.

## 구조: 데이터 4종 × 작업 4단계

하네스는 격자로 짜여 있다. 데이터 네 종류를 저마다 같은 네 단계 작업으로 돌리는 얼개다.

데이터는 네 종류다. 생쥐 배아 뇌(10x-embryonic-mouse-brain), 생쥐 피부(share-seq-mouse-skin), 사람 뇌(human-brain-multiome), 그리고 우리가 주로 쓰는 사람 조혈세포(human-hspc-10x-multiome)다. 작업은 네 단계로, 내려받기(download) → 데이터 다듬기(preprocessing) → 값 계산(model) → 그림 그리기(visualization) 순서다. 지금 우리가 맡아 돌리는 칸은 사람 조혈세포다.

이 격자를 네 종류의 파일이 받친다.

- **AGENTS.md**: 프로젝트 전체 틀(project frame). 무슨 분석인지, lag을 어떻게 정의하는지, 어떤 baseline feature와 참고 방법을 쓰는지 적는다.
- **skills/ROUTES.md**: 데이터에서 작업으로 가는 안내도. 어떤 데이터의 어떤 작업을 부르면 그에 맞는 지침 파일로 이어 준다.
- **skills/&lt;데이터&gt;/&lt;작업&gt;/SKILL.md**: 작업 하나하나의 지침.
- **agents/openai.yaml**: 그 작업을 자동으로 실행할 때 필요한 설정.

```
AGENTS.md  (프로젝트 틀)
    │
ROUTES.md  (데이터 → 작업 라우팅)
    │
  데이터 4종                작업 4단계 (각 데이터마다)
  · 생쥐 배아 뇌            1. 내려받기   download
  · 생쥐 피부              2. 다듬기     preprocessing
  · 사람 뇌                3. 값 계산    model
  · 사람 조혈세포 ★         4. 그림      visualization
       (active)
    │
  칸마다: SKILL.md (지침) + openai.yaml (설정)
    │
  pipeline/hspc-velocity-benchmark/  (실제 코드)
```

이 형식은 OpenClaw와 Codex라는 실행 도구가 그대로 읽어 들이고, 우리가 평소 쓰는 Claude Code에서도 돈다. 지침이 가리키는 실제 코드는 파이프라인 폴더(`pipeline/hspc-velocity-benchmark/`)에 있다. 사람 조혈세포의 내려받기·다듬기 단계가 여기 스크립트로 구현돼 있고, 값 계산 단계는 앞 세 글에서 다룬 velocity 방법 벤치마크로 이어진다.

## 한계: 출처와 실행 연습

두 가지를 짚어 둔다. 하나는 출처다. 이 틀은 박상준 님의 Harness_Baseline에서 왔고, 원 저장소에 라이선스가 없어 공유·수정에는 원저작자의 동의가 필요하다. 코드의 최종 위치는 박상준 님과 협의할 몫으로 남겨 두었다.

**셋째는 게이트 자체다(2026-08 덧붙임).** 이 글은 "요리사가 바뀌어도 같은 음식이 나온다"는 비유로 하네스를 소개하는데, 게이트가 붙어 있다는 사실과 그 게이트가 실제로 결함을 잡는다는 사실은 다르다. 이 하네스를 다른 프로젝트로 옮겨 심으면서 일부러 결함을 심어 검사해 봤더니(mutation 검사), 구멍이 세 건 나왔다 — 검사할 행이 0개여도 "통과"로 찍히는 공허 통과, 증거가 하나도 없는 7개 항목이 그대로 pass로 넘어가던 경로 등. 전부 막았지만, 교훈은 그 세 건이 아니라 이것이다: **게이트를 붙였다는 것만으로는 아무것도 보장되지 않고, 그 게이트가 진짜 결함을 잡는지를 따로 검사해야 한다.** 조리법이 종이에 적혀 있어도, 그 조리법이 맞는지는 따로 확인해야 하는 것과 같다.

다른 하나는 실행이다. 우리는 이 하네스를 OpenClaw로 돌리는 것을 기본으로 삼고 연습하는 중이다. 형식과 구조가 OpenClaw가 읽을 수 있는 유효한 형태인지는 실제로 돌려서 확인했다. 다만 값을 끝까지 계산하는 단계는 아직 이 환경에서 완주하지 못했다. OpenClaw 같은 실행 도구가 AI 모델을 부르려면 인증 키가 필요한데, 이 환경엔 그 키가 아직 없다. 이는 실행 환경에서 비롯한 문제이고, 틀 자체의 문제는 아니다. 어디까지 되고 어디서 왜 막혔는지를 갈라 적어 두어야, 다음에 이 기록을 보는 사람이 온전한 틀을 처음부터 다시 손대지 않아도 된다.

## 확장: 하네스에서 루프와 메모리로 (2026-07-12 덧붙임)

여기까지가 하네스였다. 분석을 다시 돌릴 수 있게 지침과 코드를 갈라 감싼 틀. 그 위에 한 층이 더 있다. 요즘 루프 엔지니어링(loop engineering)이라 부르는 것으로, 하네스가 "에이전트에 어떤 환경이 필요한가"를 묻는다면 루프는 "무엇이 그 에이전트를 목표를 향해 계속 돌게 하고, 언제 멈추는가"를 묻는다. 한 번의 지시가 요청이라면, 루프는 정책에 가깝다 — 새벽 세 시에도 돌고, 내가 자리를 비운 사이에도 돌며, 한 바퀴 돌 때마다 배운 것을 적어 다음 바퀴가 조금 나아지는.

우리 프로젝트에서 이 루프가 어느 날 밤 두 번, 스스로 자기 실수를 잡았다. 둘은 같은 얼굴이었다. 확인하지 않은 "완료".

첫째는 데이터를 내려받는 일에서 나왔다. 여덟 덩어리를 순서대로 받는 프로그램이었는데, 도중에 여섯 덩어리가 네트워크 문제로 조용히 실패했다. 그런데도 프로그램은 그걸 "완료"라 적고 다음 단계로 넘어가 버렸다. 돌지도 않은 시험을 통과했다고 스스로 보고한 셈이다. 이럴 때 필요한 건 그 보고를 믿지 않는 별도의 검증자다. 그래서 여덟 덩어리가 실제로 파일로 존재하고 받다 만 흔적이 없는지를 기계적으로 확인하는 관문을 세웠다. 하나라도 빠지면 완료 표시를 아예 만들지 않고 멈추고, 다시 돌리면 받다 만 것만 이어받는다.

둘째는 논문의 주장에서 나왔다. 앞 글들에서 우리는 시간차(lag)가 계산 프로그램을 바꾸면 재현되지 않는다는 결과를 얻었다. 논문의 차별점을 세우는 역할을 맡은 부분이 이 결과를 한 단계 끌어올리자고 제안했다 — "lag는 그냥 재현이 안 되는 게 아니라, 데이터로부터 애초에 결정되지 않는 양이다"라는 원리로 격상하자는 것이었다. 이름을 바꾸면 같은 결과가 더 높은 급으로 읽힌다. 매력적인 제안이었다. 그래서 더 위험했다. 매력적인 주장일수록 검증 없이 굳히면 논문 전체가 그 위에 얹히니까.

그래서 같은 종류의 관문을 통과하게 했다. 어떤 중심 주장도 본문에 들어가기 전에, 그 주장을 죽일 수 있는 가장 값싼 검정을 먼저 견뎌야 한다. 여기서 검정은 이랬다 — 그 "결정되지 않음"을 재는 지표가 재현성을 예측하긴 하는데, 더 단순한 설명인 "그냥 신호가 약해서"를 걷어내고도 여전히 예측하는가. 기존 데이터로 확인했더니, 그 지표의 예측력은 신호 세기를 통제하자 절반 아래로 무너졌고, 둘은 사실상 같은 것을 가리키고 있었다. 격상된 주장은 이미 아는 사실과 구별되지 않았다. 그래서 그 강한 주장은 버리고, 방어할 수 있는 선까지만 남긴 뒤, 그 판정을 방향 문서에 적어 다음에 같은 유혹이 와도 이미 접었음을 알게 했다.

두 사건의 교훈은 하나로 모인다. 만드는 눈과 검증하는 눈은 달라야 한다. 만든 쪽은 자기 과정을 보지만, 검증하는 쪽은 결과물과 기준만 본다. 같은 눈이 자기 것을 채점하면 "괜찮아 보인다"가 "괜찮다"를 이겨, 돌지도 않은 시험도 그럴듯한 과장도 통과한다. 눈을 갈라 두어야 걸린다.

그리고 이 검증이 성립하려면 앞에 반드시 하나가 있어야 한다. 목표다. 됐는지 안 됐는지를 기계가 판정할 수 있는 목표. "테스트를 통과시켜라"는 판정되고, "코드를 개선해라"는 판정되지 않는다. 판정할 수 없는 목표는 결국 자기보고로 되돌아간다. 그래서 우리 목표는 셀 수 있게 적었다 — 여덟 덩어리 완결, 그리고 어떤 주장이든 자기를 죽일 검정을 견딜 것.

루프에는 기억도 붙는다. 한 바퀴에서 배운 것을 적어 두어야 다음 바퀴가 같은 실수를 되풀이하지 않는다. 그런데 기억이 쌓이기만 하면 아무도 손대지 않는 잡동사니가 된다. 그래서 기억은 자리를 얻어야 오른다 — 검증된 결과만 상태 파일을 고치고, 되풀이 확인된 것만 규칙으로 굳는다. 앞서 접은 그 과장된 주장도 그냥 지우지 않고 방향 문서에 "검정으로 접음"이라 적어 두었다. 다음에 같은 유혹이 와도 시스템이 이미 안다. "완료"라는 표시조차 코드를 다 짰을 때가 아니라 끝까지 돌려 확인했을 때만 찍는다 — 데이터의 여덟 덩어리 완결 관문과 주장의 검정 관문은 같은 규칙의 두 적용이다.

이렇게 관찰하고, 검증하고, 복구하고, 기억하는 사이클을 설계하는 일을 요즘 루프 엔지니어링(loop engineering)이라 부른다. 새로 생긴 발상은 아니다. 되먹임 고리는 제어공학만큼 오래됐고, 근래 자율 에이전트가 강해지며 이름을 얻고 다시 뜨거워졌을 뿐이다. 우리가 한 건 그 개념을 남의 방식 그대로 옮겨 온 게 아니라 다른 길로 구현한 것이다. 이 사이클을 알아서 잘 도는 최신 모델이 있지만, 생명과학 데이터는 그 모델이 자동으로 한 급 다른 모델로 넘겨 버린다. 그래서 우리는 모델이 대신해 주기를 기다리는 대신, 보고를 믿지 않는 별도의 검증자와 작은 작업 단위, 자리를 얻어야 오르는 기억, 그리고 됐는지 기계가 판정할 수 있는 목표를 하네스에 손으로 심었다. 모델에 얹힌 능력이 아니라 틀에 박힌 규율이라, 모델이 바뀌어도 남는다. 게다가 이 규율은 책에서 베껴 온 게 아니라 그날 밤 두 번의 실수가 강제한 것이다. 필요가 만든 규율이 마침 이름 붙은 개념과 만난 셈이다.

여기서 하네스가 한 일은 앞 절들의 재현성과 결이 같다. 재현성은 절차가 처음 짠 사람의 기억에 기대지 않게 했고, 검증 관문은 결과가 만든 이나 프로그램의 보고에 기대지 않게 하며, 기억은 배움이 한 사람의 머릿속에만 갇히지 않게 한다. 셋 다 엄밀함을 사람에서 시스템으로 옮기는 한 일의 세 얼굴이다.

> ※ 초안(2026-07-12 작업 기록) — 게시 전 윤문과 사람 승인을 거친다. 루프·메모리 엔지니어링은 되먹임 고리라는 오래된 발상을 근래 공개 논의(LangChain "The Art of Loop Engineering", Ken Huang의 "Claude Fable 5" 시리즈 2·3부 등)가 다시 정리·명명한 것이다. 여기서 적은 것은 그 개념을 최신 모델에 의존하지 않고 하네스에 손으로 구현한 방식과, 그것이 우리 프로젝트의 실제 두 사례(내려받기 완료 오보, 주장 과장)로 어떻게 나타났는지다 — 개념을 우리가 처음 세웠다는 뜻은 아니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 하네스 (harness) | 지침과 코드를 갈라 감싸, 같은 절차를 다시 돌릴 수 있게 한 틀 |
| 지침 (skill) | 어느 데이터에 어떤 작업을 어떤 순서로 돌릴지 적어 둔 문서 |
| AGENTS.md | 프로젝트 전체 틀을 적은 문서(무슨 분석·lag 정의·참고 방법) |
| ROUTES.md | 데이터에서 작업으로 이어 주는 안내도 |
| openai.yaml | 작업을 자동으로 실행할 때 필요한 설정 파일 |
| OpenClaw · Codex | 이 형식을 그대로 읽어 실행하는 자동 실행 도구 |
| 재현 (reproducibility) | 다른 사람·다른 환경에서 같은 절차를 그대로 다시 돌릴 수 있는 정도 |

## 참고

**근거 문서**: `AGENTS.md`(project frame), `skills/ROUTES.md`(데이터→작업 라우팅), `skills/human-hspc-10x-multiome/`(사람 조혈세포 4단계 지침), `pipeline/hspc-velocity-benchmark/BASELINE-ALIGNMENT.md`(Harness_Baseline 정합 기록), `skills/OPENCLAW-RUN.md`(OpenClaw 실행 점검).

**개념도**: 지침과 코드를 갈라 두는 개념도(범용 재사용 자산)는 `/workspace/skills/harness-concept/`에 독립적으로 두었다.

**원 틀**: Harness_Baseline — 박상준 님(@poqopo). 원 저장소 LICENSE 미지정(공유·수정은 원저작자 동의 전제).

---
*이 글은 진행 중인 연구의 내부 정리이며, 하네스 구조와 실행 절차는 후속 작업으로 갱신될 수 있다(연구·교육용).*

---

# From results to reproducibility: moving our analysis into a harness

> TL;DR: A good analysis needs more than good results. Someone else — or a program that runs on its own — has to be able to rerun the same procedure. That means keeping the instructions (what to do) apart from the code (that runs it). This frame was brought in from Harness_Baseline, made by 박상준 (@poqopo), and fitted to our pipeline; running it on OpenClaw is still something we are practicing.

The previous three posts were about results. The transcription rate (α) stayed stable when we changed the program, the lag between the DNA opening and the gene turning on did not reproduce across programs, and that ordering recurred in other tissues and species. This post steps back from the results to the procedure that produced them. If a colleague — or myself half a year from now — wants to rerun the same analysis, what has to be in place? To answer that, we moved the analysis procedure into a frame called a harness.

## The core idea: keeping instructions apart from code

Picture opening a folder, typing the old commands again, and nothing runs. That happens when what goes where, and in what order, lived only in the head of whoever first wrote it. So a good analysis does not last on good results alone. It lasts when someone else can retrace the same procedure.

The trick for making an analysis rerunnable is simple: keep apart two things that usually travel together. One is the instructions — what to do: a document stating which task runs on which data, in what order. The other is the code that actually runs it. Kept together, only the person who wrote it can rerun the analysis. Kept apart, naming the data and the task is enough to rerun the same procedure.

A recipe makes the point. If the recipe is on a sheet of paper and the ingredients and tools sit in their places, the same dish comes out even when the cook changes. If the recipe lives only in one person's head, no one makes that dish on the day they are away. The recipe on paper is the instructions; the kitchen stocked with ingredients and burners is the code. This split, wrapped into one frame, is what we call a harness.

![Reproducible harness: splitting instructions (WHAT: SKILL.md · ROUTES · dataset→task) from code (HOW: scripts/) lets the same procedure be re-run by name — by a person or by OpenClaw.](../pipeline/hspc-velocity-benchmark/figures/fig04_harness_concept.png)

## Background: bringing in someone else's frame

We did not build this frame from a blank page. We brought in a frame called Harness_Baseline, made by 박상준 (@poqopo), and adapted it to our pipeline — taking a well-shaped recipe template and fitting it to our own ingredients. The original author is 박상준, and since the original repository carries no license, sharing and modifying it are on the premise of his consent. That source and condition are written at the top of the imported documents.

## Structure: four datasets × four tasks

The harness is laid out as a grid: four kinds of data, each run through the same four tasks.

There are four datasets: embryonic mouse brain (10x-embryonic-mouse-brain), mouse skin (share-seq-mouse-skin), human brain (human-brain-multiome), and the human hematopoietic cells we mainly use (human-hspc-10x-multiome). The tasks are four steps: download → preprocessing → model → visualization. The cell we run right now is the human hematopoietic one.

Four kinds of file support this grid.

- **AGENTS.md**: the project frame — what the analysis is, how lag is defined, which baseline features and reference methods to use.
- **skills/ROUTES.md**: the map from data to task; naming a task on a dataset routes to the matching instruction file.
- **skills/&lt;dataset&gt;/&lt;task&gt;/SKILL.md**: the instructions for each single task.
- **agents/openai.yaml**: the settings needed to run that task automatically.

```
AGENTS.md  (project frame)
    │
ROUTES.md  (data → task routing)
    │
  4 datasets                 4 tasks (for each dataset)
  · embryonic mouse brain    1. download
  · mouse skin               2. preprocessing
  · human brain              3. model
  · human HSPC ★             4. visualization
       (active)
    │
  per cell: SKILL.md (instructions) + openai.yaml (settings)
    │
  pipeline/hspc-velocity-benchmark/  (the actual code)
```

This format is read directly by the OpenClaw and Codex runners, and it also runs in the Claude Code we use day to day. The actual code the instructions point to sits in the pipeline folder (`pipeline/hspc-velocity-benchmark/`). The download and preprocessing steps for the human hematopoietic cells are implemented there as scripts, and the model step continues into the velocity-method benchmark covered in the previous three posts.

## Limits: source, and a run still in practice

Two things to state plainly. One is the source. This frame came from 박상준's Harness_Baseline, and with no license on the original repository, sharing and modifying it need the original author's consent. Where the code finally lives is left to settle with 박상준.

**Third, the gates themselves (added 2026-08).** This post introduces the harness with the image of "the same dish comes out even when the cook changes" — but having gates and having gates that catch real defects are two different things. Porting this harness to another project, we planted defects deliberately to test it (mutation testing) and found three holes: a gate reporting "pass" with zero rows to check, a path where seven items with no evidence at all still came through as passing, and one more of the same kind. All are closed now, but the lesson is not those three. It is this: **attaching a gate guarantees nothing on its own; whether the gate catches real defects has to be tested separately.** The recipe being written down does not make the recipe correct.

The other is running it. We take running this harness on OpenClaw as the default and are practicing it. That the format and structure are valid in a form OpenClaw can read, we confirmed by actually running it. But the step that computes values to the end has not yet finished in this environment, because the authentication key for the AI model the runner calls is not set up here. This is a matter of the run environment, not a flaw in the frame. Writing down separately how far it got and where and why it stopped is what spares the next person who reads this from rebuilding a sound frame from scratch.

## Glossary

| Term | Meaning |
|---|---|
| harness | A frame that keeps instructions and code apart, wrapping them so the same procedure can be rerun |
| skill (instructions) | A document stating which task runs on which data, in what order |
| AGENTS.md | The document that states the project frame (what analysis, lag definition, reference methods) |
| ROUTES.md | The map that routes from data to task |
| openai.yaml | The settings file needed to run a task automatically |
| OpenClaw · Codex | Runners that read this format directly and execute it |
| reproducibility | The degree to which the same procedure can be rerun by another person or in another environment |

## References

**Source documents**: `AGENTS.md` (project frame), `skills/ROUTES.md` (data→task routing), `skills/human-hspc-10x-multiome/` (four-step instructions for the human hematopoietic cells), `pipeline/hspc-velocity-benchmark/BASELINE-ALIGNMENT.md` (Harness_Baseline alignment record), `skills/OPENCLAW-RUN.md` (OpenClaw run check).

**Concept diagram**: the instructions-vs-code diagram (a cross-project reusable asset) is kept separately at `/workspace/skills/harness-concept/`.

**Original frame**: Harness_Baseline — 박상준 (@poqopo). No LICENSE on the original repository (sharing and modifying on the premise of the original author's consent).

---
*Internal working note from ongoing research; the harness structure and run procedure may be updated by later work (research and educational use).*

---

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

---

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

---

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

---

# 크로마틴 방향을 믿어도 되는 규칙을 찾다가 세 번 실패한 이야기

> 한 줄 요약: "어떤 유전자에서는 크로마틴 방향을 써도 되나"에 답할 규칙을 세 가지 방식으로 찾아봤고 세 번 다 기준에 못 미쳤다. 대신 왜 안 되는지가 드러났다. 지금의 계산 프로그램들이 튼튼하게 되찾는 값은 사실상 발현량에 가깝고 그 너머의 시간 정보까지는 나뉘지 않는다.

## 0. 핵심 개념

이 시리즈는 세포가 유전자를 쓰는 일을 서랍에서 서류를 꺼내 읽는 데 빗대 왔다.

- **크로마틴 열림**(chromatin, DNA가 감긴 실타래가 풀리는 것): 서랍을 여는 일. ATAC로 측정한다.
- **전사 속도 α**(transcription rate): 꺼낸 서류를 읽는 속도.
- **시간차 lag**: 서랍을 연 뒤 서류를 읽기까지의 간격.
- **발현량**(abundance): 그 유전자의 서류가 세포 안에 얼마나 쌓여 있는가.

이번 글의 주인공은 시간차의 **부호**, 다시 말해 방향이다.

```
방향이 + (크로마틴 먼저)  서랍을 먼저 열고 나중에 읽는다
방향이 − (RNA 먼저)      읽기가 먼저 움직이고 서랍이 뒤따른다
```

방향을 스스로 정하는 계산 프로그램은 우리 손에 셋이 있다. 셋 다 같은 데이터를 받지만 계보와 셈법이 다르다.

- **MoFlow**: 크로마틴 신호와 RNA 신호를 나란히 맞대어 밀린 정도로 시간차를 잰다.
- **CRAK-Velo**: 다른 모델(UniTVelo)에 크로마틴을 붙여 확장한 것.
- **MultiVeloVAE**: MultiVelo 계열의 딥러닝(확률) 버전으로, 값을 여러 번 표본추출해 추정한다.

원조 MultiVelo는 여기 넣지 않았다. 그 프로그램은 전환 시점을 한 방향으로만 정렬하는 구조라 방향이 처음부터 한쪽으로 고정돼 나온다. 방향을 비교하려면 방향이 자유로운 프로그램만 써야 한다.

## 방향에 규칙이 필요한 이유

앞선 글에서 우리는 시간차가 프로그램을 바꾸면 유지되지 않는다고 보고했다. 그다음에 나오는 질문은 실용적이다. 다른 연구자가 이 지표를 쓰려 할 때, "전부 못 믿는다"보다 "이런 유전자에서는 써도 된다"가 훨씬 쓸모 있다. 그래서 우리는 **사전에 정할 수 있는 기준**을 찾기로 했다.

여기서 사전이라는 말이 중요하다. 결과를 다 보고 나서 "일치한 유전자 247개가 신뢰 집합이다"라고 말하는 것은 실행 규칙이 못 된다. 그건 답을 보고 나서 답을 적은 것이다. 쓸 수 있는 규칙은 데이터를 받자마자 적용할 수 있어야 한다. 발현량이 얼마 이상이면, 전사 속도가 얼마 이상이면 하는 식으로.

세 가지 방식을 차례로 시험했다.

```
시도 1  유전자 하나하나에 방향을 붙일 수 있나
시도 2  발현량·전사 속도로 선을 그을 수 있나
시도 3  여러 지표를 섞은 새 점수를 만들면 되나
```

## 시도 1: 유전자별 방향의 프로그램 간 일치도

먼저 확인할 것이 있었다. 그 방향이 프로그램을 바꿔도 유지되는가.

한 가지 손질을 먼저 했다. 세 프로그램은 부호를 자기 나름의 규약으로 붙이므로 어느 쪽이 +인지 자체가 다를 수 있다. 그래서 골수계 표지 유전자(ELANE·AZU1·MPO·LYZ·CSF1R)와 조혈모세포 표지 유전자(HLF·CRHBP·MEIS1)의 값 차이로 각 프로그램의 규약을 생물학에 맞췄다. 셋 다 이미 같은 쪽을 가리키고 있어 뒤집을 필요가 없었다(골수계에서 크로마틴이 먼저인 쪽: MoFlow +0.356, CRAK +1.500, VAE +0.071). 계통 수준의 거친 방향 구조는 세 프로그램이 함께 재현했다. 이건 알려진 골수 분화 생물학과 어긋나지는 않는다.

그 위에서 유전자 하나하나의 방향을 맞대 봤다. 동전 던지기라면 50%가 나온다.

```
프로그램 쌍별 방향 일치율 (동전 던지기 = 50%)
  MoFlow × CRAK  │ 42.3%  (유전자 239개)
  MoFlow × VAE   │ 54.6%  (유전자 560개, 이항 p=0.031)
  CRAK  × VAE    │ 46.6%  (유전자 277개)
```

여기서 한 가지를 먼저 걸러야 했다. 시간차 값이 **정확히 0**인 유전자가 적지 않다. 방향을 정하지 못했다는 뜻이라 어느 쪽으로도 세면 안 된다. 이런 유전자를 빼고 센 값이 위 표다.

세 쌍 모두 동전 던지기에서 크게 벗어나지 않았고, 한 쌍은 오히려 그보다 낮았다. 그러면 시간차 크기가 큰 유전자만 골라 보면 어떨까. 프로그램이 자신 있게 방향을 말한 유전자들이다. MoFlow와 CRAK 양쪽에서 시간차 크기가 큰 유전자로 좁혀 갔다. 전체 42.3%에서 상위 절반 44.4%, 상위 3분의 1에서 **47.8%**. 올라가긴 했지만 끝까지 동전 던지기를 넘지 못했다.

계통 수준에서 세 프로그램이 함께 가리키는 방향은 있다. 다만 그 구조를 유전자 하나에 붙이는 일은 지금 방법들로 되지 않는다. 이 유전자는 크로마틴이 먼저라고 이름표를 다는 일 말이다.

## 시도 2: 발현량과 전사 속도의 임계

방향이 유전자마다 흔들린다면, 흔들리지 않는 구역이 따로 있을지 모른다. 유전자를 전사 속도 α 순으로 열 무리(십분위)로 나누고 무리마다 세 프로그램이 방향을 만장일치로 잡는 비율을 봤다.

```
전사 속도 α 십분위별 방향 합의 (유전자 538개)
  분위  median α   크로마틴 만장일치   RNA 만장일치   프로그램 간 엇갈림
  D1     0.050          1.9%            61.1%           37.0%
  D5     0.574          3.7%            31.5%           64.8%
  D7     1.459          7.5%             7.5%           84.9%
  D9     4.940         16.7%             0.0%           83.3%
  D10   20.230         31.5%             0.0%           68.5%
```

추세는 진짜였다. 전사 속도가 높을수록 크로마틴 만장일치가 늘어나고(Spearman +0.250, p=4.2e-09) RNA 만장일치는 줄어든다(−0.472, p=3.1e-31). 발현량으로 나눠도 같은 방향이 나온다. 통계적으로 확실한 추세다.

문제는 크기다. **가장 높은 십분위에서도 만장일치는 31.5%뿐이고 68.5%는 여전히 프로그램마다 방향이 엇갈린다.** 세 명 중 두 명이 다른 답을 내는 지표를 실행 규칙으로 내놓을 수는 없다. 선을 어디에 그어도 마찬가지였다. 만장일치 크로마틴 유전자 83개 중 전사 속도 상위 20%에 드는 것도 42.6%라, 고발현 유전자라는 말로 그 집합을 정의하는 것조차 안 된다.

가장 낮은 분위의 RNA 만장일치 61.1%도 신호로 읽지 않는다. 전사가 거의 없는 유전자에서는 프로그램들이 다 같이 기본값 근처로 수렴해 버려서, 일치가 생겨도 그건 축퇴(degenerate, 값이 정해지지 못하고 한 점에 몰리는 것)일 가능성이 크다.

## 시도 3: 여러 지표를 가중 결합한 점수

지표 하나로 안 되면 여러 개를 섞으면 된다는 게 다음 생각이었다. 전사 속도, 발현량, 크로마틴-RNA 결합도, 곡률 두 종류, 시간차 크기, 크로마틴 여는 속도까지 일곱 가지를 넣고 로지스틱 회귀로 "이 유전자에서 세 프로그램이 크로마틴 방향으로 만장일치할까"를 예측하게 했다. 5겹 교차검증으로 점수를 매겼다.

교차검증 AUC는 **0.701**이었다. 우리가 미리 정해 둔 통과선(0.70)을 간신히 넘긴 값이다. 여기까지는 됐다.

그런데 그 점수로 유전자를 줄 세워 상위 10%만 봤더니 만장일치는 **31.4%**였고 68.6%는 프로그램마다 답이 달랐다. 미리 정한 두 번째 통과선은 70%였다. 시도 2와 사실상 같은 자리다.

계수를 열어 보니 이유가 보였다. 표준화한 계수에서 **전사 속도 α가 +0.885로 혼자 지배**했고 나머지 여섯은 전부 절댓값 0.3 아래였다. 일곱 개를 섞은 점수라고 만들었지만 실제로는 α 하나를 다시 쓴 것이다. 도착한 자리도 시도 2와 같았다.

여기서 판정을 내렸다. 결정 지도에 "발현 상위 몇 퍼센트에서는 방향을 써도 된다" 같은 조건부 규칙을 **넣지 않는다.** 초안에 넣자고 제안했다가 이 결과를 보고 거뒀다.

## 곁가지: 방향이 일치하는 소수 유전자의 정체

규칙을 못 만들었으니 반대로 물어봤다. 그래도 일치하는 그 소수는 어떤 유전자인가.

만장일치로 크로마틴 방향이 나온 83개를 pathway(생물학적 기능 묶음) 데이터베이스에 넣었더니 호중구 과립 유전자가 뚜렷하게 몰렸다. MPO·ELANE·AZU1·PRTN3·CTSG처럼 골수 분화 초기에 좁고 강하게 켜졌다 꺼지는 과립 단백질들이다.

여기엔 함정이 하나 있다. 우리 유전자 집합은 애초에 계산이 잘 되는 고발현·역동적 유전자에서 뽑혔다. 그런 집합을 전체 유전체와 비교하면 원래도 이런 프로그램이 튀어나온다. 그래서 배경을 유전체 전체가 아니라 **방향 판정이 가능했던 유전자 640개**로 바꾸고 다시 검정했다. GO 항목은 전부 유의성을 잃었고 혈소판·지혈 계열도 떨어져 나갔다. 살아남은 것은 **Reactome의 Neutrophil Degranulation(adjP=9.44e-04, 유전자 15개)** 한 갈래였다. 반대로 만장일치 RNA 방향 164개는 어느 배경에서도 유의한 항목이 없었다.

배경을 공정하게 바꿔도 살아남은 신호라 눈길이 간다. 그래도 이걸 생물학적 주장으로 올리지는 않는다. 막는 것이 셋이다.

1. **일치는 정답이 아니다.** 방향에는 바깥에서 답을 알려 줄 실험이 없다. 프로그램끼리 같은 답을 냈다고 그 답이 맞다는 보장은 없고 셋이 같은 편향을 공유했을 수도 있다.
2. **인과 대조는 음성이었다.** 크로마틴 신호를 유전자끼리 무작위로 뒤섞어도 이 표지 유전자들의 시간차는 다른 유전자보다 더 움직이지 않았다(p=0.58). 여기서도 크로마틴이 시간차를 만든다는 증거는 나오지 않았다.
3. **신호 세기라는 경합 설명이 있다.** 이 유전자들은 켜지고 꺼지는 동역학이 가장 날카롭고 발현도 가장 높다. 방향이 잘 보이니까 프로그램들이 같은 답을 낸 것일 수 있다. 생물학과 신호 세기를 현 데이터로 나눌 방법이 없다.

데이터셋을 바꿔 확인하는 길도 막혀 있다. 방향 합의를 검정하려면 부호가 자유로운 프로그램이 두 개 이상 필요한데, 실제로 갖춘 것은 HSPC 3개와 마우스 배아 gastrulation 2개뿐이다. 게다가 호중구 과립 프로그램은 조혈 계통의 우세한 분화 프로그램이라, 호중구가 없는 마우스 배아에서는 같은 pathway가 애초에 나올 수 없다. 이 관찰은 HSPC 한 시스템, 한 프로그램 조합의 관찰로만 보고한다.

## 안 되는 이유

세 번의 실패가 같은 곳을 가리켰다.

프로그램은 유전자 하나를 맞출 때 네 속도를 동시에 정한다. 값을 살짝 흔들었을 때 데이터에 맞는 정도가 급히 떨어지면 그 값은 뚜렷하고(데이터가 딱 정해 줌), 거의 안 변하면 흐릿하다(데이터가 느슨하게 둠).

```
뚜렷함 (높을수록 데이터가 딱 정해 줌)
  α    전사 속도          +7.98   ◀ 가장 뚜렷
  α_c  크로마틴 여는 속도   +7.32
  β    처리 속도          +4.86
  γ    분해 속도          +1.72   ◀ 가장 흐릿
```

데이터에 맞는 정도는 α 방향으로 가장 뾰족하고, 분해 속도 γ 쪽으로는 평평하다. 크로마틴 여는 속도 α_c는 경우가 다르다. 한 번의 맞춤 안에서는 뚜렷하게 정해지지만(+7.32), 프로그램을 바꾸면 순위 상관이 ρ=0.29밖에 안 된다. 프로그램마다 또렷하지만 서로 다른 값에 안착하는 것이다. 시간차는 이렇게 정해진 전환 시점들의 차이다. 한쪽은 데이터가 느슨하게 두고 다른 쪽은 프로그램에 따라 흔들리니, 그 차이에는 잡음만 남는다.

여기에 하나가 더 붙는다. 튼튼하게 재현되는 유일한 값인 α 자체가 **발현량과 ρ=0.809로 겹친다.** 두 값이 이만큼 겹치면 서로 다른 정보를 준다고 보기 어렵다.

지금의 multiome velocity 프로그램들이 프로그램을 바꿔도 튼튼하게 되찾는 것은 사실상 "그 유전자가 얼마나 많이 켜져 있는가"에 가깝다. 크로마틴이 얼마나 앞서는지, RNA가 얼마나 빨리 치워지는지 같은 그 너머의 시간 정보는 나뉘지 않는다. 그래서 세 시도가 모두 α로 되돌아왔다.

한 가지는 분명히 해 둔다. 이건 프로그램을 잘못 짜서 생긴 일이 아니다. 이 데이터와 이 모델의 조합에서 데이터가 그 방향으로 평평하다는 정보의 한계다.

## 사람들이 velocity를 쓰는 방식은 이게 아니지 않나

여기까지는 유전자 하나하나에 붙는 값 이야기였다. 당연한 반문이 따라온다. velocity를 실제로 쓸 때 보는 건 그 값이 아니라 그림 위의 화살표 아닌가.

맞는 말이라 한 층 위를 실제로 재 봤다. velocity 산출물은 세 층이다.

```
① 유전자별 값        전사 속도·분해 속도·시간차        ◀ 여기까지가 위 이야기
② 세포×유전자 행렬   세포마다 유전자마다의 변화량       ◀ 이번에 잰 곳
③ 그림 위의 화살표   ②를 2차원 그림에 투영한 것        ◀ 사람들이 보는 것
```

②는 이미 계산돼 파일 안에 들어 있었다. 감사만 안 했을 뿐이다. 그래서 세포 21,878개와 유전자 354개(다섯 프로그램이 공통으로 다루고 다섯 곳 모두에서 값이 나온 것)에서 두 프로그램이 **같은 세포에 같은 방향**의 변화를 주는지 쟀다.

숫자 하나만 보면 안 되는 건 여기서도 같다. 대조군을 두 개 놓았다. 둘 다 잴 수 있는 프로그램이 MultiVelo뿐이라 두 대조군은 MultiVelo 기준이다. 다시 맞춘 결과가 저장된 프로그램이 여기뿐이다.

**대조군 1, 천장.** MultiVelo를 세포만 다시 뽑아 다시 맞추면 얼마나 같은 답이 나오나. **0.87**이었다(1이면 완전 일치, 0이면 무관). 자를 대면 일치가 보인다.

**대조군 2, 크로마틴 지우기.** 같은 MultiVelo에서 크로마틴 정보를 통째로 뒤섞고 다시 돌렸다. **0.84**. 다시 맞춘 것과 사실상 같다. 크로마틴을 지워도 화살표가 거의 안 움직인다.

정작 **서로 다른 프로그램끼리는 0 근처이거나 음수**였다(−0.53~+0.13). 세포·유전자 하나하나의 부호가 맞는 비율도 49.7~58.3%로 동전 던지기였다. 두 프로그램(MultiVelo와 MultiVeloVAE)은 같은 세포에 **서로 반대 방향**을 줬다(−0.50).

```
같은 프로그램, 다시 맞춤        0.87   ◀ 자는 일치를 잡아낸다
같은 프로그램, 크로마틴 지움    0.84   ◀ 크로마틴은 거의 기여 안 함
서로 다른 프로그램끼리          ~0     ◀ 진짜로 안 맞는다
크로마틴 안 쓰는 프로그램과     0.58   ◀ 가장 잘 맞는 상대가 이쪽
```

가장 잘 맞는 짝은 **크로마틴을 아예 안 쓰는 RNA 전용 프로그램**이었다. 다만 이건 네 프로그램 중 MultiVelo에서만 뚜렷했다(나머지는 +0.26, −0.00, −0.29). "multiome에서 살아남는 건 RNA 쪽"이라고 일반화하지는 않는다. 크로마틴이 무력하다는 인과 판정도 다시 맞춘 대조군이 있는 MultiVelo에만 붙인다.

이 검정도 결과를 보기 전에 판정 기준을 봉인해 두고 돌렸고 통과 조건 두 개가 다 실패했다. 유전자별 값에서 내린 결론이 한 층 위에서도 그대로였다.

③(그림 위 화살표)은 아직 안 쟀다. "행렬이 안 맞아도 그림에서는 이웃끼리 뭉개지며 비슷해 보일 것'이라고 변명할 수 있다. 그 변명은 쓸 수 없다. 2026년에 나온 벤치마크 두 편을 확인해 보니 그중 하나가 이웃 평활을 거친 단계에서도 프로그램 간 일치가 낮다고 이미 보고했다(비교한 12개 전부). 정량적인 일치는 위층에서 회복되지 않는다. 남는 여지는 거친 흐름선이 눈으로 보기에 비슷해 보일 수 있다는 정도까지다.

## 예시로 보인 값과 지표로 쓰는 값

다시 해 보면 달라지는 결과는 드물지 않다. 전임상 생물학에서 대표 연구들을 다시 돌린 시도는 일부만 되찾았고, 심리학에서 대규모로 이뤄진 복제도 사정이 비슷했다. 연구자 설문에서는 남의 실험을 재현하지 못한 경험이 다수였고 자기 실험에서도 그런 일이 적지 않았다. 암 생물학의 체계적 복제 시도는 더 앞쪽에서 막혔다. 논문만 읽고 실험을 그대로 반복할 만큼 방법이 적힌 경우가 드물어 원저자에게 물어야 했다. 유전체학에서도 발표된 발현 분석이 논문만으로 반복되지 않는 일이 잦았다.

우리가 마주한 것은 그와 결이 조금 다르다. 원 방법들이 예시로 보인 그림은 우리 데이터에서도 상관 수준에서는 재현된다. MPO나 ELANE 같은 유전자에서 세 프로그램이 크로마틴 먼저 쪽을 함께 가리킨다. 다만 이 표지 유전자 집합은 무작위로 고른 집합과 구별되지 않았다(marker-shuffle 음성, MW p=0.58). 그래서 이 일치를 방향의 정답으로 쓸 수는 없다. 다음 단계에서 갈린다. 예시로 보인 값이 이후 유전자 하나하나의 정량 지표로 쓰이는데, 그 수준의 식별성 문제는 ConsensusVelo가 먼저 제기했고 우리 결과는 그 지적을 multiome 세팅에서 확인하는 쪽이다. 다만 원 방법들이 나오던 당시에는 견줘 볼 독립 프로그램이 없었다.

이 글이 잰 것은 그 사이의 구간이다. 예시로 보인 것과 지표로 쓰는 것 사이에는 검정되지 않은 자리가 있고, 우리는 거기에 자를 대 봤다.

## 배운 점

- **규칙은 못 만들었지만 왜 못 만드는지는 알게 됐다.** 세 시도가 다 α로 수렴한 덕에 막힌 자리가 임계값 고르기가 아님이 드러났다. 데이터가 담고 있는 정보의 양이 문제였다.
- **p값이 확실한 추세도 실행 규칙으로는 못 썼다.** 전사 속도와 방향 일치의 관계는 p값으로 보면 의심할 여지가 없다(4.2e-09). 그래도 최상위 구간의 31.5%는 실행 규칙으로 쓸 수 없는 수준이다. 어느 쪽 문턱을 보고 있는지 헷갈리면 결론이 뒤집힌다.
- **계수를 열어 보기 전까지는 새 지표를 만든 줄 알았다.** AUC 0.701만 보면 새 지표를 만든 것 같지만 계수를 보면 α 하나가 +0.885로 지배하고 있었다. 성능 숫자 하나로는 점수가 무엇을 재고 있는지 알 수 없다.
- **살아남은 pathway 하나도 그대로 두지 않았다.** 배경을 바꿔도 남은 호중구 과립 신호는 눈에 띄지만, 정답 없음·인과 음성·신호 세기라는 세 제약이 걸려 있고 다른 조직에서는 재현될 수 없어 관찰로만 적는다.
- **"그건 실제 용법이 아니잖아"라는 반문에 말 대신 자로 답했다.** 유전자별 값만 봤다는 지적에 말로 답하는 대신 한 층 위를 실제로 쟀고 결론이 같았다. 여기서 결정적이었던 건 천장 대조군이다. 같은 프로그램을 다시 맞추면 0.87이 나온다는 걸 확인하지 않았다면, 프로그램 간 0은 "자가 무딘 것"과 구분되지 않았다.

## 결론

방향을 언제 믿어도 되는지 판정할 사전 기준을 세 가지 방식으로 찾았고 세 번 다 쓸 수 있는 수준에 못 미쳤다. 유전자별 방향 일치는 42~55%로 동전 던지기 근처였고 시간차가 큰 유전자로 좁혀도 47.8%에서 멈췄다. 전사 속도 임계는 최상위 십분위에서도 31.5%, 일곱 지표를 섞은 점수는 상위 10%에서 31.4%였다. 그래서 결정 지도에 "여기서는 방향을 써도 된다"는 조건부 행을 넣지 않는다.

대신 왜 안 되는지가 남았다. 지금의 프로그램들이 되찾는 값은 발현량 근처까지이고 그 너머의 시간 정보는 이 데이터에서 나뉘지 않는다. 이 결론은 유전자별 값에만 걸리지 않았다. 한 층 위인 세포×유전자 행렬에서도 프로그램 간 일치는 0 근처였고 MultiVelo에서는 크로마틴을 지워도 행렬이 다시 맞춘 만큼밖에 안 움직였다. 다음 실험이 무엇이어야 하는지도 여기서 나온다. 시간차를 쓰려면 시간차를 흐릿하게 만드는 그 평평함을 걷어 낼 측정이 필요하다. 시간을 직접 재는 실험이다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 방향 (부호) | 크로마틴이 먼저 열렸는지 RNA가 먼저 움직였는지 |
| 전사 속도 (α) | 유전자가 켜졌을 때 RNA를 만드는 빠르기 |
| 발현량 (abundance) | 그 유전자의 RNA가 세포 안에 쌓여 있는 양 |
| 만장일치 | 방향이 자유로운 세 프로그램이 한 유전자에서 같은 방향을 낸 경우 |
| 십분위 | 유전자를 어떤 값 순으로 줄 세워 열 무리로 나눈 것 |
| 교차검증 AUC | 예측이 얼마나 잘 맞는지의 지표. 0.5는 동전 던지기, 1.0은 완벽 |
| 축퇴 (degenerate) | 데이터가 값을 정해 주지 못해 여러 프로그램이 다 같이 기본값 근처로 몰리는 것 |
| 뚜렷함 (곡률) | 값을 흔들 때 데이터에 맞는 정도가 급히 떨어지는 정도. 클수록 데이터가 그 값을 딱 정해 줌 |
| pathway enrichment | 유전자 목록이 특정 기능 묶음에 치우쳐 있는지 검정하는 것. 무엇을 배경으로 두느냐에 따라 결과가 달라진다 |
| 세포×유전자 행렬 | 세포마다 유전자마다 "지금 늘고 있나 줄고 있나"를 담은 표. 그림 위 화살표는 이 표를 2차원에 투영한 것 |
| 천장 (재현성 상한) | 같은 프로그램을 세포만 다시 뽑아 다시 맞췄을 때의 일치도. 자가 잡아낼 수 있는 최대치라, 프로그램 간 일치를 여기에 견줘야 뜻이 생긴다 |

## 참고

근거: `results/direction_reliability_threshold_and_enrichment.md`(임계·복합지표·enrichment, BIOP01-57), `results/two_mechanisms_classification.md`(유전자별 방향 재현 검정, BIOP01-55), `results/unanimous_loci_characterization.md`(만장일치 유전자 특성화), `results/marker_shuffle_teeth_test.md`(인과 대조), `results/velocity_matrix_audit.md`(세포×유전자 행렬 감사, BIOP01-59), `manuscript/NOTE_benchmarks_12_13_scope_check.md`(2026 벤치마크 두 편이 어느 층을 쟀는지 확인).

*진행 중 연구의 내부 정리다. 수치는 현재 분석 기준이라 후속 검증으로 갱신될 수 있다(연구·교육용).*

---

# Three failed attempts to find a rule for when to trust direction

> TL;DR: We looked for a rule answering "in which genes can we use the chromatin-first direction?", tried three ways, and all three fell short of usable. What we got instead was the reason. What today's programs robustly recover is close to abundance, and the timing information beyond it does not separate out.

## 0. Core concepts

This series pictures a cell using a gene as opening a drawer and reading the document inside.

- **Chromatin opening** (chromatin, the unwinding of DNA's spool): opening the drawer. Measured by ATAC.
- **Transcription rate α**: the reading speed.
- **The lag**: the gap from opening the drawer to reading the document.
- **Abundance**: how much of that gene's document has piled up inside the cell.

This post is about the lag's **sign** — its direction.

```
direction +  (chromatin first)  the drawer opens, reading follows
direction −  (RNA first)        reading moves first, the drawer follows
```

Three programs in our hands set that direction themselves. All three take the same data but come from different lineages and do different arithmetic.

- **MoFlow**: lines up the chromatin and RNA signals and reads the lag from how far one is shifted against the other.
- **CRAK-Velo**: another model (UniTVelo) extended with chromatin.
- **MultiVeloVAE**: a deep-learning (probabilistic) version in the MultiVelo lineage that estimates values by sampling.

The original MultiVelo is not in this set. It aligns switch times in one direction only, so the direction comes out fixed to one side from the start. To compare directions, only programs whose sign is free will do.

## Why direction needs a rule

Earlier posts reported that the lag does not survive a change of program. The next question is a practical one. For someone who wants to use this measure, "in genes like these you can use it" is far more useful than "trust none of it." So we went looking for a criterion that can be **set in advance**.

That "in advance" is the crux. Looking at all the results and then declaring "the 247 genes that agreed are the trustworthy set" is not an operating rule; it writes the answer after seeing it. A usable rule must apply the moment the data arrives — abundance above such-and-such, transcription rate above such-and-such.

We tried three routes in turn.

```
Attempt 1  Can we label direction gene by gene?
Attempt 2  Can abundance or transcription rate draw the line?
Attempt 3  Does a new composite score do it?
```

## Attempt 1: cross-program agreement of per-gene direction

First we had to check whether the direction survives a change of program at all.

One preparation came first. Each program assigns signs by its own convention, so which side counts as + can differ. We aligned each program's convention to biology using the gap between myeloid priming markers (ELANE, AZU1, MPO, LYZ, CSF1R) and HSC markers (HLF, CRHBP, MEIS1). All three already pointed the same way, so no flip was needed (chromatin-first on the myeloid side: MoFlow +0.356, CRAK +1.500, VAE +0.071). The coarse, lineage-level directional structure does reproduce across all three programs, and it fits known myeloid differentiation biology.

On top of that we compared direction gene by gene. A coin flip would give 50%.

```
Sign agreement by program pair (coin flip = 50%)
  MoFlow × CRAK  │ 42.3%  (239 genes)
  MoFlow × VAE   │ 54.6%  (560 genes, binomial p=0.031)
  CRAK  × VAE    │ 46.6%  (277 genes)
```

One thing had to be filtered out first. For a fair number of genes the lag value is **exactly zero**, which means no direction was determined, so such a gene must not be counted on either side. The table above excludes them.

All three pairs sat close to a coin flip, and one fell below it. What if we keep only genes with a large lag, the ones a program called confidently? We narrowed to genes with large lag magnitude in both MoFlow and CRAK: 42.3% overall, 44.4% in the top half, **47.8%** in the top third. It rose, but never got past a coin flip.

There is a direction all three programs point to at the lineage level. Pinning that structure onto a single gene, that is, tagging one gene as "chromatin leads here," is what today's methods cannot do.

## Attempt 2: a threshold on abundance and transcription rate

If direction wavers gene by gene, maybe there is a zone where it does not. We split genes into ten groups (deciles) by transcription rate α and looked at the fraction where all three programs agreed on direction.

```
Direction consensus by α decile (538 genes)
  decile  median α   chromatin unanimous   RNA unanimous   programs split
  D1       0.050            1.9%              61.1%            37.0%
  D5       0.574            3.7%              31.5%            64.8%
  D7       1.459            7.5%               7.5%            84.9%
  D9       4.940           16.7%               0.0%            83.3%
  D10     20.230           31.5%               0.0%            68.5%
```

The trend is real. As transcription rate rises, chromatin-unanimous genes increase (Spearman +0.250, p=4.2e-09) and RNA-unanimous genes decrease (−0.472, p=3.1e-31). Splitting by abundance gives the same direction. Statistically the trend is not in doubt.

The problem is its size. **Even in the highest decile, unanimity reaches only 31.5%, and for 68.5% the programs still disagree on direction.** A measure where two of three give a different answer cannot ship as an operating rule, and no placement of the line changed that. Of the 83 chromatin-unanimous genes, only 42.6% fall in the top 20% by transcription rate, so the set cannot even be described as "the highly expressed genes."

We also decline to read the 61.1% RNA-unanimous figure in the lowest decile as signal. Where transcription is nearly absent, the programs all converge near their default values, so agreement there is likely degenerate — values collapsing onto one point rather than being pinned down.

## Attempt 3: a weighted composite score

If one measure will not do, combine several. That was the next idea. We fed seven features — transcription rate, abundance, chromatin-RNA coupling, two curvature terms, lag magnitude, and chromatin opening rate — into a logistic regression predicting whether the three programs would be chromatin-unanimous at a gene, scored by 5-fold cross-validation.

Cross-validated AUC came out at **0.701**, just past the 0.70 bar we had set in advance. So far so good.

Then we ranked genes by that score and looked at the top 10%: unanimity **31.4%**, split 68.6%. The second bar we had set in advance was 70%. That is essentially where Attempt 2 landed.

Opening up the coefficients showed why. In standardized terms, **transcription rate α dominated alone at +0.885**, with the other six all below 0.3 in absolute value. We had built a seven-feature score that in practice used α again — which is why it arrived at the same place as Attempt 2.

So we made the call. No conditional rule such as "direction is usable above the top X% of expression" goes into the decision map. We had proposed one in a draft and withdrew it on seeing this.

## A side branch: what the few agreeing genes are

Having failed to build the rule, we asked the reverse question: what kind of genes are the few that do agree?

Putting the 83 chromatin-unanimous genes into pathway databases, neutrophil granule genes came up strongly — MPO, ELANE, AZU1, PRTN3, CTSG, the granule proteins that switch on and off in a narrow, intense burst early in myeloid differentiation.

There is a trap here. Our gene set was drawn from highly expressed, dynamic genes that fit well in the first place, and comparing such a set against the whole genome brings out these programs anyway. So we replaced the background with the **640 genes where direction could be judged** and retested. All GO terms lost significance, and the platelet and hemostasis families dropped out. One branch survived: **Reactome Neutrophil Degranulation (adjP=9.44e-04, 15 genes)**. The 164 RNA-unanimous genes, by contrast, gave no significant term under either background.

A signal that survives a fair background swap is worth noting, but we do not promote it to a biological claim. Three things stand in the way.

1. **Agreement is not correctness.** There is no external experiment that reveals the true direction. Programs giving the same answer does not make that answer right, and all three could share the same bias.
2. **The causal control was negative.** Scrambling the chromatin signal randomly across genes moved these markers' lags no more than other genes' (p=0.58). Here too, no evidence that chromatin makes the lag.
3. **Signal strength is a competing explanation.** These genes have the sharpest on-off dynamics and the highest expression. The programs may agree simply because the direction is resolvable there. With current data, biology and signal strength cannot be told apart.

Checking in another dataset is blocked as well. Testing direction consensus needs at least two sign-free programs, and we have three only for HSPC and two for mouse gastrulation. Besides, the neutrophil granule program is a dominant differentiation program of the blood lineage; in a mouse embryo with no neutrophils, the same pathway cannot appear at all. So this is reported as an observation from one system and one combination of programs.

## Why it does not work

The three failures all pointed to the same place.

When the program fits one gene, it sets four speeds at once. Nudge a value: if the fit to the data drops steeply, the value is sharp (the data pins it down); if it barely moves, it is blurry (the data leaves it loose).

```
Sharpness (higher = pinned down by the data)
  α    transcription rate  +7.98   ◀ sharpest
  α_c  chromatin-open rate +7.32
  β    processing rate     +4.86
  γ    degradation rate    +1.72   ◀ blurriest
```

The fit is steepest along α and nearly flat along the degradation rate γ. The chromatin opening rate α_c is a different case: within a single fit it is pinned down sharply (+7.32), yet across programs it holds only at ρ=0.29. Each program lands on a crisp value, and those values disagree with each other. The lag is a **difference** between switch times set that way. One side is left loose by the data, the other shifts with the program, so taking their difference leaves mostly noise.

One more thing sits on top. α, the one value that reproduces robustly, **overlaps abundance at ρ=0.809.** With that much overlap, the two can hardly be carrying different information.

Put together: what today's multiome velocity programs robustly recover across a change of program is close to "how much this gene is switched on." The timing information beyond it — how far chromatin runs ahead, how fast RNA is cleared — does not separate out. Which is why all three attempts came back to α.

One point to be clear about: this is not a matter of programs being written badly. It is an information limit of this data and model combination, which does not carry enough information along the lag direction.

## But that is not how people actually use velocity

Everything above concerns values attached to individual genes. The obvious objection follows: **what people look at is not those values but the arrows on the plot.**

Fair enough, so we measured one layer up. Velocity output comes in three layers.

```
① per-gene values      transcription rate, degradation rate, lag   ← the story above
② cell × gene matrix   how much each gene moves in each cell       ← measured here
③ arrows on the plot   ② projected into two dimensions             ← what people look at
```

Layer ② was already computed and sitting in the files; it had simply never been audited. So on the 21,878 cells, and on the 354 of the genes shared by all five programs that return a value in every one of them, we asked whether two programs move **the same cell in the same direction**.

A single number would mislead here as much as anywhere, so we set two controls. Only one program, MultiVelo, can carry them — it is the only one whose refits were stored — so both controls are MultiVelo's.

**Control 1, the ceiling.** Refit MultiVelo on a resampled set of cells: how much does it agree with itself? **0.87** (1 is identical, 0 is unrelated). The ruler can see agreement when agreement exists.

**Control 2, erase chromatin.** In the same MultiVelo, shuffle the chromatin information wholesale and refit. **0.84** — effectively the same as a plain refit. Erasing chromatin barely moves the arrows.

Meanwhile **different programs sat at or below zero** (−0.53 to +0.13). Per-cell, per-gene sign agreement was 49.7–58.3%, a coin flip. Two programs, MultiVelo and MultiVeloVAE, gave the same cells **opposite directions** (−0.50).

```
same program, refit            0.87   ◀ the ruler does detect agreement
same program, chromatin gone   0.84   ◀ chromatin contributes almost nothing
two different programs         ~0     ◀ they genuinely disagree
vs the program with no chromatin  0.58   ◀ the best match is over here
```

The point of that table is that the best-matching partner was the **RNA-only program that uses no chromatin at all**. That held clearly for only one of the four programs, MultiVelo (the rest were +0.26, −0.00, −0.29), so we do not generalise it into "what survives in multiome is the RNA part". The causal verdict on chromatin is likewise confined to MultiVelo, the only program with a refit control.

This test too was run with its pass criteria sealed before the results were read, and both conditions failed. The conclusion drawn on per-gene values held one layer up.

Layer ③, the arrows on the plot, we have not measured. One escape is available — "even if the matrix disagrees, neighbouring cells get smoothed together and the plot may still look similar" — but that escape is closed. Checking the two 2026 benchmarks, one of them already reports **low cross-program agreement at the neighbour-smoothed stage as well**, across all twelve programs it compared. Quantitative agreement is not repaired further up. What remains open is only that coarse streamlines may still look similar to the eye.

## A value shown as an example, a value used as a metric

Results that shift when you redo them are not rare. Attempts to rerun landmark preclinical studies recovered only a portion of them, and a large replication effort in psychology found much the same. In surveys, most researchers report having failed to reproduce someone else's experiment, and many report the same about their own. A systematic replication effort in cancer biology hit an earlier wall: published reports rarely carried enough method detail to repeat an experiment without asking the original authors. In genomics, published expression analyses were often not repeatable from the paper alone.

What we ran into has a slightly different grain. The picture the originating methods showed by example holds in our data too: at genes such as MPO and ELANE, all three programs point the same way about chromatin opening first. The parting comes at the next step. A value demonstrated on examples is later used as a per-gene quantitative metric, and at that level its reliability had never been tested. At the time there was not even an independent program to compare against.

What this post measured is the stretch in between. Between a value shown as an example and a value used as a metric there is an untested gap, and we put a ruler to it.

## What we learned

- **The rule we could not build told us why it could not be built.** All three attempts converging on α showed that the problem lies in how much information the data carries, not in the choice of threshold.
- **A statistically solid trend and a usable rule sit at different bars.** By p-value the link between transcription rate and direction agreement is beyond doubt (4.2e-09). Yet 31.5% in the top bin is unusable as an operating rule. Confusing which bar you are looking at flips the conclusion.
- **Open the coefficients before trusting a combination of measures.** AUC 0.701 looks like a new measure was built; the coefficients show α dominating alone at +0.885. A single performance number cannot tell you what the score is measuring.
- **We did not leave the one surviving pathway alone either.** The neutrophil granule signal stands out after the background swap, but with no ground truth, a negative causal control, and signal strength as a competing explanation — and no chance of replicating in another tissue — it is written up as an observation.
- **"That is not the real use case" is answered by measuring, not by arguing.** Instead of replying in words to the objection that we only looked at per-gene values, we measured one layer up and got the same conclusion. The ceiling control was what made it decisive: without knowing that a refit of the same program returns 0.87, a cross-program zero could not be told apart from a blunt ruler.

## Conclusion

We looked three ways for an a priori criterion telling us when direction can be trusted, and all three fell short of usable. Per-gene direction agreement sat at 42–55%, near a coin flip, and stopped at 47.8% even among large-lag genes. A transcription-rate threshold gave 31.5% in the top decile; a seven-feature composite gave 31.4% in its top 10%. So no conditional row saying "direction is usable here" goes into the decision map.

What remains is the reason. What today's programs recover reaches about as far as abundance, and the timing information beyond it does not separate in this data. That conclusion was not confined to per-gene values either: one layer up, in the cell × gene matrix, cross-program agreement was also near zero, and in MultiVelo erasing chromatin moved the matrix no more than a refit did. That also says what the next experiment has to be: to use the lag, we need a measurement that removes the uncertainty now blurring it — an experiment that times the process directly.
