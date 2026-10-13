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
