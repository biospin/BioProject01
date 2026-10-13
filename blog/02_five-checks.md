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
