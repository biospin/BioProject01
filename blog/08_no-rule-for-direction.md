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
