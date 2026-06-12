# Luo et al., 2026 — Benchmarking RNA velocity methods across 17 independent studies — core 분석

> 근거 자료: `sources/luo-2026-velocity-benchmark.pdf` (본문 1–8p + STAR Methods e1–e5). supplementary(`sources/mmc1.pdf`, `sources/mmc2.pdf`)는 본 core에서 직접 인용한 부분만 표시한다. 본문·STAR Methods에 명시된 method 이름·dataset accession·metric 정의·scenario 권고만 근거로 한다. Figure의 정확한 수치는 본문이 텍스트로 밝힌 값만 단정하고, 그래프에서 읽어야 하는 값은 `검토필요:`로 표시한다.
>
> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 본 문서에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.

## Executive Summary

- **무엇**: RNA velocity inference에 best-practice 가이드가 없는 상황에서, 15개 RNA velocity method를 17개 독립 dataset(real 17 + simulation 3)에서 accuracy·stability·usability 세 축·4개 metric으로 벤치마크하고, dataset 성격별 method 선택 권고(scenario-based suggestion)를 제시한 resource paper. 새 method가 아니라 *선택 지침*이 산출물.
- **모델 / 방법**: method가 추정한 cell-level velocity $v_c$를 4개 metric으로 평가. 핵심은 cross-boundary direction correctness $\mathrm{CBDir}(c)=\frac{1}{|\{c'\in C_B\cap N(c)\}|}\sum_{c'} \frac{v_c\cdot(x_{c'}-x_c)}{|v_c|\,|x_{c'}-x_c|}$ (방향 정확도, ground-truth transition 기반), in-cluster coherence ICCoh(cluster 내 cosine 일관성), velocity consistency Vcs(이웃 30개와의 cosine), method agreement A1/A2(method 간 일치도). 단일 정답 method는 없음.
- **핵심 결과**:
  - ① Accuracy(CBDir, 17 real dataset 평균 약 0.1) — veloVI가 최고(CBDir=0.23), 다음 Pyro-Velocity(0.17). 전반적으로 낮아 "개선 여지 큼". veloVAE는 다수 dataset에서 방향이 역전(negative CBDir).
  - ② Human bone marrow(Dataset4, multi-trajectory)에서 평균 CBDir이 −0.193까지 하락; mature PBMC(Dataset11)에서 대부분 method가 CD8+→naive 등 biology와 반대 방향 산출.
  - ③ ICCoh/Vcs — LatentVelo ICCoh=0.99, UniTVelo 0.96, MultiVelo 0.96; 대부분 ICCoh≥0.7, Vcs≥0.6으로 높으나 이는 over-smoothing 가능성. veloVAE는 두 metric 모두 underperform.
  - ④ Method agreement — A1 대부분 <0.4(method 간 불일치 큼). latentvelo·cell2fate가 가장 불일치. Pyro-Velocity·cell2fate는 CBDir이 sampling에 가장 불안정(range −0.11~0.403).
  - ⑤ Stability/Usability — UniTVelo·LatentVelo가 downsampling/HVG 변화에 안정, veloVAE는 급락. GPU method 중 DeepVelo·veloVI가 실행시간·메모리 우수; cell2fate·Pyro-Velocity는 메모리 多, cellDancer·MultiVelo는 실행시간 長.
- **우리 적용**: Human HSPC 10x Multiome(GSE209878)는 본 benchmark의 **Dataset12**로 실제 사용됨(transition: HSC→MPP, MPP→LMPP, MEP→Erythrocyte, GMP→Granulocyte). 단 MultiVelo는 `rna_only=True`로 ATAC 없이 돌렸으므로 multi-omic 성능은 평가되지 않음. use_case=pipeline-applicable + methodology-reference. 상세 적용 지침은 `luo-2026-velocity-benchmark_methodology-brief.md`.
- **심층**: 한계·재현 ROI·산업 시선은 `luo-2026-velocity-benchmark_lens-academic.md` / `luo-2026-velocity-benchmark_lens-industry.md` / `luo-2026-velocity-benchmark_methodology-brief.md` 참고.

## Identity

- **Title**: Benchmarking RNA velocity methods across 17 independent studies
- **Authors**: Ya Luo, Jun Ren, Qian Yang (공동 1저자), Zhiyu You, Ying Zhou, Qingqing Qin, Qiyuan Li (corresponding, lead contact)
- **소속**: Department of Hematology, The First Affiliated Hospital of Xiamen University and Institute of Hematology / National Institute for Data Science in Health and Medicine, School of Medicine, Xiamen University
- **Year**: 2026 (published 2026-03-30, issue 2026-04-20)
- **Venue**: Cell Reports Methods 6(4):101367 — Resource article, open access (CC BY-NC-ND)
- **DOI**: 10.1016/j.crmeth.2026.101367 (preprint bioRxiv 10.1101/2025.08.02.668272)
- **Citation key**: `luo2026velocitybenchmark`
- **Code/data**: 분석 스크립트 `https://github.com/luo-cloud/veloBench`, Zenodo 10.5281/zenodo.18699599. 모든 dataset publicly available (accession은 Key Resources Table).

## Background

### RNA velocity와 3단계 파이프라인

RNA velocity는 spliced/unspliced mRNA의 상대 abundance로부터 cell이 어느 방향으로 state transition 중인지를 single-cell 수준에서 추정한다 (La Manno 2018, ref 4). 본문은 RNA velocity inference를 세 stage로 정리한다 (Figure 1A):

1. **Preprocessing** — spliced/unspliced matrix를 HVG filtering → normalization → 저차원 projection(PCA) → kNN smoothing(default k=30).
2. **Velocity estimation** — method별로 가장 크게 갈리는 단계. steady-state 가정(velocyto: 모든 gene에서 transcription·degradation·splicing rate가 상수이고 일부 cell이 steady-state) vs. dynamical model(scVelo: cell-specific latent time을 도입해 maximum likelihood로 kinetic parameter $\alpha,\beta,\gamma$를 공동 추정).
3. **Postprocessing** — gene-wise velocity vector를 UMAP/t-SNE/PCA 저차원 공간에 projection, cell transition probability $\pi_{ij}\propto \frac{\langle \delta_{ij}, v_i\rangle}{|\delta_{ij}||v_i|}$ 로 transition matrix 구성 후 streamline/grid plot로 시각화.

### 문제 정의 — best-practice 부재

2018년 velocyto 이후 method가 20개 이상으로 폭증했고(Figure 1B의 timeline: velocyto 2018 → scVelo, protaccel 2020 → MultiVelo, Chromatin Velocity, CellRank, veloVI 등 2021 → Dynamo, UniTVelo, Pyro-Velocity, LatentVelo, Region-velocity 등 2022 → cell2fate, cellDancer, GraphVelo 2023 → DeepVelo 2024), 방법론이 세 갈래로 분화했다:

1. **추가 biological information 통합형** — protaccel(protein translation), **Chromatin Velocity·MultiVelo(chromatin accessibility 등 epigenomic feature)**, PhyloVelo(genealogical info), Dynamo(metabolic labeling).
2. **noise 제어·dynamics 충실 재현형** — velvet(neighborhood constraint), VeloVAE·veloVI·Pyro-Velocity(Bayesian inference로 uncertainty), veloAE(autoencoder smoothing), DeepVelo(variational autoencoder), UniTVelo(uniform regularization), DeepVelo(graph convolution으로 gene-/cell-specific kinetic parameter), LatentVelo(multi-branching용 neural ODE), cellDancer(deep NN로 cell-specific kinetic), cell2fate(biological module 분해).

> `외부 맥락:` 본문은 method를 위 두 갈래(+steady-state)로 서술하나, MultiVelo/Chromatin Velocity가 우리 epigenomic-lag 목표와 직결되는 "epigenome–transcriptome interaction" 계열임을 명시한다(ref 9, 10). 이 benchmark에서 MultiVelo는 chromatin 정보를 끈 채 평가됐다는 점이 우리에게 핵심(Methods 참조).

선행 benchmark는 단일 성능 dimension·특정 application에 국한돼 평가 기준이 제한적이었다(refs 24–26). 저자는 inference accuracy + algorithmic stability + computational usability를 full-scale로 평가하고, "대부분 method가 처음으로 17개 dataset에서 함께 시험"된다는 점을 차별점으로 든다.

## Methods

### Formal task

각 method는 cell $c$에 대해 velocity vector $v_c$를 산출한다. 평가의 출발점은 *ground-truth development direction* $A\to B$ (curated cell trajectory 또는 기존 biological knowledge로 정의)이고, 모든 metric은 추정된 $v_c$를 이 ground truth 혹은 method 간 합의에 비춰 점수화한다. Table S2에 dataset별 known differentiation order가 정리되고 CBDir에 적용된다.

### 평가 대상 method 15종 (3 카테고리)

| 카테고리 | Method | 비고 / 실행 설정 (STAR Methods) |
|---|---|---|
| ODE-based (5) | **velocyto** | steady-state, `scVelo.tl.velocity mode='deterministic'` default |
| | **scVelo-stochastic (scVelo-sto)** | `mode='stochastic'` |
| | **scVelo-dynamical (scVelo-dyn)** | `mode='dynamical'` |
| | **MultiVelo** | `rna_only=True` — 우리 데이터처럼 scATAC 없는 conventional scRNA로 실행 (chromatin 채널 비활성) |
| | **CellRank** | default |
| ML-based (4) | **UniTVelo** | `velo.FIT_OPTION='1'` (unified mode) |
| | **Dynamo-stochastic (Dynamo-sto)** | stochastic mode, `dyn.tl.cell_velocities` cosine kernel |
| | **Pyro-Velocity** | default (GPU only) |
| | **cell2fate** | >10000 cell이면 `compute_and_plot_total_velocity_scVelo()` (GPU only) |
| Deep learning (6) | **veloAE** | default |
| | **veloVI** | default |
| | **veloVAE** | continuous veloVAE |
| | **LatentVelo** | default (GPU only) |
| | **cellDancer** | cosine kernel + `dyn.tl.cell_velocities` |
| | **DeepVelo** | default |

> `해석:` MultiVelo·cellDancer·Dynamo는 원래 multi-omic 또는 metabolic labeling 같은 추가 모달리티를 쓸 수 있는 method지만, 본 benchmark는 *conventional scRNA-only* 조건으로 통일했다. 즉 "MultiVelo가 benchmark에 포함됐다"는 사실은 맞으나, 그 multi-omic(epigenome) 채널은 평가되지 않았다. 우리 chromatin–transcription lag 목표에 직결되는 MultiVelo의 강점은 이 논문이 측정하지 않은 영역이다 (`질문:` 아래 분석 메모 참조).

### 평가 metric 4종 (확률/통계 구조)

본문은 STAR Methods e4–e5에서 4개 metric을 식으로 정의한다.

1. **Cross-boundary direction correctness (CBDir)** — *accuracy* 핵심. ground-truth $A\to B$에서, source cluster $A$에 속하면서 target cluster $B$에 이웃을 가진 boundary cell 집합 $C_{A\to B}=\{c\in C_A \mid \exists c'\in C_B\cap N(c)\}$ 를 잡고,
   $$\mathrm{CBDir}(c)=\frac{1}{|\{c'\in C_B\cap N(c)\}|}\sum_{c'\in C_B\cap N(c)} \frac{v_c\cdot(x_{c'}-x_c)}{|v_c|\,|x_{c'}-x_c|}$$
   velocity $v_c$가 displacement $x_{c'}-x_c$(저차원 공간에서 짧은 시간의 cell 이동)와 얼마나 같은 방향인지의 cosine. ground-truth가 필요하다.
2. **In-cluster coherence (ICCoh)** — 같은 cluster 내 이웃 cell들 velocity의 cosine 평균. 방향의 *정답 여부와 무관*하게 cluster 내부에서 velocity가 얼마나 매끄러운지(smoothing)를 본다.
   $$\mathrm{ICCoh}(c)=\frac{1}{|\{c'\in C_A\cap N(c)\}|}\sum_{c'\in C_A\cap N(c)} \frac{v_c\cdot v_{c'}}{|v_c|\,|v_{c'}|}$$
3. **Velocity consistency (Vcs)** — cell $i$의 velocity와 30개 nearest neighbor velocity의 cosine 평균 $C_i=\frac{1}{|N_i|}\sum_{j\in N_i} S_{\cos}(v_i,v_j)$ (ref 5, scVelo). ICCoh와 유사하나 cluster가 아닌 kNN 기준.
4. **Method agreement A1 / A2** (ref 25) — method 간 일치도.
   - $A_1=S_{\cos}(v_{i,M_1}, v_{i,M_2})$ — cell $i$에서 method $M_1$과 $M_2$ transition vector의 cosine (pairwise).
   - $A_2=S_{\cos}(v_{i,M_1}, v_{i,\mathrm{Med}})$ — method $M_1$ vector와 모든 method의 median vector의 cosine (consensus 대비 정렬도).

> `해석:` CBDir만 ground-truth에 의존하는 "정확도" metric이고, ICCoh·Vcs는 ground-truth 없이 "내부 일관성/smoothness", A1/A2는 method 간 합의를 본다. 저자도 본문(Discussion·Limitations)에서 ICCoh·Vcs의 높은 값이 over-smoothing의 부작용일 수 있고, CBDir이 pre-defined ground truth(annotation bias 가능)에 의존함을 인정한다. 따라서 "ICCoh 0.99 = 좋음"이라고 단순 해석하면 안 된다.

### 평가 데이터 (real 17 + simulation 3)

- **real 17 dataset**: 최소 3개 RNA velocity method 논문에서 쓰인 dataset 위주로 선정. accession은 Key Resources Table·Results 참조 (아래 Tables 섹션에 정리).
- **stability — downsampling**: 4개 benchmark dataset(Dataset1 pancreas, Dataset2 dentate gyrus, Dataset3 erythroid, Dataset4 human bone marrow)에서 spliced matrix를 cell cluster별 stratified로 sample rate 0.4/0.5/0.6/0.7/0.8로 다운샘플, 각 5회 반복.
- **stability — HVG**: 같은 4개 dataset에서 HVG 개수를 바꿔(예: 1,000 HVG) metric 변화 관찰.
- **simulation 3 dataset**: dyngen(ref 29)으로 1,000 cell씩 bifurcation(185 gene)·cycle(171 gene)·linear(171 gene) backbone 생성. CBDir의 cell transition은 dyngen milestone으로 정의.
- **usability**: 실제 dataset에서 average execution time + average memory increment 측정.

### Computer platform (재현 환경)

- CPU test(velocyto, scVelo-sto, scVelo-dyn, Dynamo-sto, CellRank 5종): Intel Xeon Silver 4210 2.2GHz, 40 core, 125GB RAM.
- GPU test(10종 = MultiVelo, UniTVelo, Pyro-Velocity, cell2fate, veloAE, veloVI, veloVAE, LatentVelo, cellDancer, DeepVelo): Intel Xeon Gold 6230 2.1GHz, 80 core, 1TB RAM, NVIDIA A800 80GB. 이 중 LatentVelo·Pyro-Velocity·cell2fate는 GPU만 지원, 나머지 7종은 GPU/CPU 모두 지원.

### 이전 방법(선행 benchmark)과의 차이

선행 RNA velocity benchmark(refs 24–26)는 단일 성능 dimension 또는 특정 application에 집중. 본 연구는 (1) accuracy(CBDir, ICCoh, Vcs, A2) + stability(downsampling·HVG·simulation) + usability(time·memory)를 한 파이프라인으로 통합, (2) 17 real + 3 simulation으로 대부분 method를 처음으로 동일 조건 비교, (3) 단일 ground-truth·dataset에 의존하지 않고 multi-dataset 일관 추세로 권고를 도출한 점이 차별점.

### Method 한계 (저자가 명시한 trade-off)

- CBDir은 pre-defined ground truth에 의존 → incomplete prior info·annotation bias에 취약. ground-truth 정의가 dataset마다 달라 결과에 영향.
- ICCoh 등 high coherence는 biological fidelity가 아니라 trajectory over-smoothing의 결과일 수 있음.
- method 간 inconsistency(예: LatentVelo vs cell2fate)는 inference error가 아니라 서로 다른 model architecture·가정의 반영일 수 있음.
- 빠른 분야 발전으로 일부 신규 method 미포함.

## Results

### 전체 결과 요약 — "전 항목 우월 method 없음"

저자의 1차 결론: 어떤 metric에서도 모든 평가를 압도하는 단일 method는 없었고, 일부 method는 특정 조건에서 예상치 못하게 underperform했다. 따라서 단일 method 의존 대신 *multiple method 결과의 cross-method consistency를 비교*할 것을 권고한다.

### Accuracy (Figure 2, Figure 6A)

- **CBDir (Figure 2A)**: 17 real dataset 전체에서 대부분 method의 평균이 약 0.1로 낮아 "개선 여지가 크다". 최고는 **veloVI (CBDir=0.23)**, 다음 **Pyro-Velocity (0.17)**. veloVAE는 다수 dataset에서 inferred velocity 방향이 *역전*(negative CBDir, Figure 2A·S2A).
- **complexity↑ → accuracy↓**: 전사 dynamics가 복잡할수록 방향 추정 정확도가 하락.
  - **Human bone marrow(Dataset4)**: multiple transcriptionally enhanced cell trajectory 때문에 평균 CBDir이 **−0.193**까지 하락(Figure S1B).
  - **Mature PBMC(Dataset11)**: 대부분 method가 erroneous direction 산출. 예 CD8+ cytotoxic T → CD4+/CD45RA+/CD25- naive T 같은 biology와 반대 방향(Figure S1B, S2B).
  - 일부 method는 처음 시험된("unseen") dataset에서 "tested on" dataset보다 높은 CBDir을 보임(Figure S1C).
- **ICCoh (Figure 2B)**: 대부분 method가 ICCoh≥0.7로 높음(이웃 cell 간 velocity field가 매끄러움). 특히 **LatentVelo ICCoh=0.99, UniTVelo 0.96, MultiVelo 0.96**. **veloVAE는 ICCoh도 낮음**.
- **Velocity consistency (Figure 2C)**: 대부분 Vcs≥0.6. 단 velocity consistency는 original dataset("tested on")에서 더 높고 unseen에서 낮음(Figure S1C). veloVAE는 Vcs도 underperform.

> `해석:` veloVI가 정확도(CBDir) 단독 1위이지만 0.23은 절대값으로 낮다. ICCoh/Vcs 상위(LatentVelo, UniTVelo, MultiVelo)는 "매끄럽다"는 뜻이지 "방향이 맞다"는 뜻이 아니다. 저자도 high ICCoh가 over-smoothing일 수 있다고 경고하므로, 정확도와 일관성을 같은 축으로 합산하면 오독 위험이 있다.

### Method 간 불일치 (Figure 3, Figure 4D)

- **A1 (pairwise, Figure 3A)**: 15 method의 A1이 대체로 낮아(대부분 <0.4) velocity 추정 간 substantial discrepancy. **latentvelo·cell2fate가 다른 모든 method와, 또 서로 간에도 특히 낮은 A1**.
- **cell type별 method agreement (Figure S4A–S4D, dataset1–4)**: pancreas(Dataset1)에서 velocyto·scVelo-dyn·veloVAE·DeepVelo·CellRank는 early cell type에서 robust했으나 terminally differentiated cell에서 A1이 ~56% 하락. human bone marrow(Dataset4)에서는 veloVI·DeepVelo만 모든 cell type에서 stability 유지. 나머지 2개 dataset은 consensus가 전반적으로 낮음.
- **A2 (consensus 정렬, Figure 3B)**: **Pyro-Velocity·scVelo-sto·Dynamo-sto가 A2>0.5로 상대적으로 우수**, **latentvelo가 A2<0.3으로 최저 일관성**.

### Stability — downsampling (Figure 4)

- 대부분 method에서 sampling rate가 stability를 좌우. **Pyro-Velocity·cell2fate의 CBDir이 가장 불안정**(CBDir range **−0.11 ~ 0.403**). 반면 ICCoh는 대부분 downsample rate에서 0.7 이상으로 비교적 안정(velocyto·cellDancer는 outlier).
- velocity consistency는 downsampling 시 양극화. **UniTVelo·LatentVelo는 sampling rate가 달라도 안정·우수**, 다른 method는 불안정·underperform(Figure 4C, S5E).
- inter-method agreement A1은 downsampling에도 대체로 불변(Figure 4D). DeepVelo·scVelo-sto·veloVI·velocyto는 highly stable agreement. A2는 대부분 안정, scVelo-sto·Pyro-Velocity·Dynamo-sto는 full data에서 높고 downsample에서도 A2>0.5 유지(Figure 4E, S5F).

### Stability — HVG 수 (Figure S6)

- **CBDir은 HVG 선택에 매우 민감**. latentvelo·UniTVelo는 **1,000 HVG**에서 최적(Figure S6A).
- ICCoh·velocity consistency는 feature 선택에 robust(veloVAE만 예외, Figure S6B, S6C). A1은 HVG 수 변화에도 전체 일관성 거의 불변. **scVelo-sto·Dynamo-sto·Pyro-Velocity의 A2는 HVG 수가 늘수록 증가**(Figure S6E).

### Stability — simulation 3 trajectory (Figure 5)

- dyngen 3 dataset(bifurcation 185 gene, cycle 171 gene, linear 171 gene), 각 1,000 cell.
- **bifurcating·cycling trajectory 해결: veloVI·DeepVelo·Dynamo-sto가 높은 CBDir** (Figure 5A). **latentvelo·cell2fate는 ICCoh·Vcs는 높지만(국소적으로 smooth·stable한 velocity field) — Figure 5B, 5C — 정작 CBDir(방향)은 낮음**.
- A1은 method 쌍별로 갈리고(velocyto–scVelo-sto, CellRank–cellDancer, DeepVelo–veloVI 등만 높은 일치), DeepVelo·velocyto·veloVI·Dynamo-sto가 높은 A2 → 일부 transcription dynamics 공통 feature를 잡았을 가능성(Figure 5E).

### Usability (Figure 6C)

- GPU method 중 **DeepVelo·veloVI는 실행시간·메모리 모두 우수**. 반대로 **cell2fate·Pyro-Velocity는 메모리 多, cellDancer·MultiVelo는 실행시간 長**.
- CPU method는 메모리 요구가 낮음. **velocyto·scVelo-sto·Dynamo-sto는 실행시간 짧음**.

> `검토필요:` Figure 6C의 정확한 시간/메모리 수치(예: 각 method의 분/GB)는 본문 텍스트에 숫자로 나오지 않고 Figure 6 메모리/시간 bubble·bar로만 제시된다. Figure 6 패널의 우측 "Memory cost / Time" 컬럼에 method별 값(예 veloVI 0.8G/6m, DeepVelo 5.3G/19s 등으로 보이는 숫자)이 있으나 해상도상 정밀 판독 필요. 정량 인용 전 PDF 확대 확인.

### Overall + scenario별 best-practice (Figure 6A–6D, Discussion)

저자는 세 core 축(accuracy / stability / usability)을 종합해 Figure 6A(real 17 dataset 4 metric, red), 6B(downsample·HVG·simulation 4 metric, blue), 6C(time·memory, green)로 요약하고, Figure 6D에 decision tree 형태의 시나리오별 권고를 제시한다.

| 시나리오 | 데이터 특성 | 우선시 축 | **권장 method** |
|---|---|---|---|
| (i) Extra-large dataset | million-cell scale cell atlas | scalability + accuracy + computational efficiency | **veloVI, DeepVelo, Dynamo-sto, scVelo-sto** (high accuracy·낮은 memory·CPU 호환) |
| (ii) Low-quality data | sparse / noisy / low-depth | accuracy + downsampling·HVG stability | **UniTVelo, LatentVelo, veloVI, Pyro-Velocity** (downsampling robust·undersampling 저항) |
| (iii) Complex dynamics | non-linear / multi-branching lineage | accuracy + simulated-perturbation stability | **DeepVelo, veloVI, LatentVelo** (real에서 high accuracy·simulation에서 resilience) |

> `해석:` 세 시나리오 모두에 **veloVI**가 들어가고(전 시나리오 권장), DeepVelo는 large·complex 두 곳, LatentVelo는 low-quality·complex 두 곳에 등장한다. 전 항목 1등은 없다는 결론과 모순되지 않는다 — veloVI는 정확도 우위(CBDir 0.23)이고 usability도 좋아 default 후보로 가장 안전하지만, low-quality·complex에서는 UniTVelo/LatentVelo의 stability가 보완한다.

### Discussion에서의 일반 권고

biology context마다 ground truth가 다르므로 결론은 단일 dataset이 아닌 multi-dataset 추세에 기반. 핵심 운영 권고는 **단일 method 의존을 피하고 multiple method 결과의 cross-method consistency(특히 downstream biological interpretation 수준)를 비교**하라는 것. 향후 개선 방향으로 (1) lineage tracing·metabolic labeling 결합한 large multi-center balanced dataset, (2) parallel benchmarking, (3) cell population imbalance 통제, (4) multi-method consistency 강조를 든다.

## Figures

### Figure 1 — An overview of RNA velocity methods

#### 패널별 설명
- **A**: RNA velocity 3단계(preprocessing → modeling inference → postprocessing) 도식. preprocessing은 spliced/unspliced matrix → filtering/gene selection/normalization/PCA → kNN smoothing(k=30). modeling은 steady-state model($\frac{du}{dt}=\alpha-\beta u$, $\frac{ds}{dt}=\beta u-\gamma s$, steady-state ratio $\gamma$로 velocity)과 dynamical model-scVelo(EM step으로 $\alpha,\beta,\gamma$·latent time 추정). postprocessing은 cell transition probability $\pi_{ij}\propto\langle\delta_{ij},v_i\rangle/(|\delta_{ij}||v_i|)$ → transition matrix → embedding → streamline plot.
- **B**: 2018–2024 method timeline. 색으로 differential equation model / deep learning model / machine learning model 구분. velocyto(2018) → scVelo·protaccel → MultiVelo·Chromatin Velocity·CellRank·veloAE → Dynamo·UniTVelo·veloVI·veloVAE·Pyro-Velocity·Region-velocity·LatentVelo → PhyloVelo·GraphVelo·cell2fate·cellDancer → DeepVelo(2024).
- **C**: 본 benchmark workflow 도식 — 15 method(3 카테고리) × {5 human + 12 mouse real dataset, 3 simulation(bifurcation/linear/cycle)} → Accuracy(CBDir·ICCoh·Vcs·A1/A2) / Stability(downsampling·HVG·simulation) / Usability(time·memory).

#### 본문에서 강조한 비교
method가 3계열(ODE / ML / deep learning)로 분화했고, 그중 MultiVelo·Chromatin Velocity가 epigenomic feature 통합 계열임을 timeline으로 보여 분야 지형을 정리.

#### 해석 시 주의점
`해석:` Figure 1B의 timeline에는 20개+ method가 있으나 실제 benchmark는 15개만(예: protaccel, PhyloVelo, Region-velocity, velvet, GraphVelo, Chromatin Velocity는 평가 대상에서 제외). 포함/제외 기준은 "최소 3개 velocity paper에서 쓰인 dataset에 적용 가능 + publicly available"이다.

### Figure 2 — 15 method의 real 17 dataset 성능

#### 패널별 설명
- **A** CBDir score (point=cluster transition A→B 방향 정확도). veloVI가 분포 상단, veloVAE가 하단(역전).
- **B** ICCoh score. LatentVelo·UniTVelo·MultiVelo가 상단(≈0.96–0.99), veloVAE 하단.
- **C** velocity consistency. method별 violin, 노란 심볼 = 전 dataset grand mean.

#### 본문에서 강조한 비교
veloVI(CBDir 0.23)·Pyro-Velocity(0.17)의 정확도 우위 vs. veloVAE의 방향 역전. ICCoh/Vcs는 대부분 높으나 over-smoothing 주의.

#### 해석 시 주의점
`검토필요:` Figure 2A에서 veloVI=0.23, Pyro=0.17은 본문이 텍스트로 명시한 값이다. 다른 method의 개별 CBDir 값은 violin에서 읽어야 하므로 정량 인용 전 확인.

### Figure 3 — method 간 velocity field 일치도

#### 패널별 설명
- **A** pairwise mean-A1 heatmap(15×15). 대부분 셀이 <0.4. latentvelo·cell2fate 행/열이 특히 낮음.
- **B** method별 mean-A2 violin(전 dataset). Pyro-Velocity·scVelo-sto·Dynamo-sto 상단, latentvelo 하단.

#### 본문에서 강조한 비교
A1 전반 저조 → 동일 데이터라도 method가 만드는 velocity field가 크게 다름. A2로 보면 consensus에 잘 정렬되는 것은 Pyro-Velocity·scVelo-sto·Dynamo-sto.

#### 해석 시 주의점
`해석:` 저자는 method 불일치가 inference error가 아니라 model architecture 차이일 수 있다고 본다(특히 LatentVelo·cell2fate). 따라서 A1이 낮은 method를 "틀렸다"고 단정하면 안 된다.

### Figure 4 — downsampling 안정성

#### 패널별 설명
- **A** sample rate(0.4–1.0)별 CBDir 궤적(4 dataset, 15 method). Pyro-Velocity·cell2fate가 가장 요동(−0.11~0.403).
- **B** ICCoh — 대부분 0.7 이상 평탄(velocyto·cellDancer outlier).
- **C** velocity consistency — UniTVelo·LatentVelo 평탄·우수.
- **D** mean-A1 (downsample rate별), **E** mean-A2. "1.0"이 original ground truth.

#### 본문에서 강조한 비교
sampling rate가 안정성의 주 변수. UniTVelo·LatentVelo가 sampling에 강건. A1/A2는 downsampling에 대체로 불변(DeepVelo·scVelo-sto·veloVI·velocyto가 특히 안정).

#### 해석 시 주의점
`해석:` rare cell·intermediate transitional cell의 undersampling이 erroneous/incomplete trajectory를 유발한다는 것이 저자 결론. 우리 HSPC처럼 rare progenitor가 중요한 데이터에서 직접적 경고.

### Figure 5 — simulation(dyngen) 성능

#### 패널별 설명
- **A** CBDir, **B** ICCoh, **C** velocity consistency (각 bifurcation/cycle/linear stacked).
- **D** mean-A1 heatmap, **E** A2 violin(3 simulation).

#### 본문에서 강조한 비교
bifurcating·cycling 해결력: veloVI·DeepVelo·Dynamo-sto의 CBDir 높음. latentvelo·cell2fate는 ICCoh·Vcs 높지만 CBDir 낮음(smooth하나 방향 부정확).

#### 해석 시 주의점
`해석:` complex topology 시나리오 권고(DeepVelo·veloVI·LatentVelo)에서 LatentVelo가 들어가는 건 real-data accuracy + simulation stability의 합. simulation 단독 CBDir만 보면 LatentVelo는 강자가 아니므로 권고 근거를 분리해 읽어야 한다.

### Figure 6 — 전 method 종합 + 시나리오 권고

#### 패널별 설명
- **A** 15 method × 4 metric(CBDir·ICCoh·Vcs·A2), 17 real dataset, red 농도=점수.
- **B** 같은 4 metric을 downsample·HVG·simulation에서, blue.
- **C** method별 average execution time + memory(green). 막대 길수록·진할수록 높은 점수, bubble 클수록·진할수록 높은 점수. 우측에 method별 Memory/Time 수치.
- **D** decision tree: start → data 특성 분석 → {Large cell atlas → veloVI/DeepVelo/Dynamo-sto/scVelo-sto (accuracy+usability) | Data quality·sparsity → UniTVelo/LatentVelo/veloVI/Pyro-Velocity (accuracy+stability) | Complex topology → DeepVelo/veloVI/LatentVelo (accuracy+stability)}.

#### 본문에서 강조한 비교
"overall" metric은 CBDir·ICCoh·Vcs·A2 4개의 geometric mean. 이 종합으로도 단일 절대 우위 method는 없으며, 시나리오별 권고로 분기.

#### 해석 시 주의점
`검토필요:` Figure 6C의 Memory/Time 수치는 PDF에서 직접 판독해야 한다(본문 텍스트에 표로 없음). `해석:` Figure 6D가 이 논문의 실질 산출물(decision tree)이며, 우리 method 선택의 1차 근거다.

## Tables

### 본문 정식 Table

본문(main text)에는 정식 number Table이 없다. method·dataset·metric 정리는 Figure 1·6과 STAR Methods 서술, 그리고 supplementary Table S1/S2에 있다.

### Table S1 (Supplementary) — 17 real dataset 목록

STAR Methods·Key Resources Table에서 dataset 번호·출처·accession·평가 transition을 서술. 본 core에 직접 인용한 항목:

| Dataset | 내용 | Accession | 평가 transition (CBDir, 발췌) |
|---|---|---|---|
| Dataset1 | Pancreatic endocrinogenesis | GEO GSE132188 | Ngn3 high EP→Pre-endocrine, Pre-endocrine→Alpha/Beta/Delta/Epsilon |
| Dataset2 | Dentate gyrus neurogenesis (2930 cell, 13913 gene) | GEO GSE95753 | OPC→OL, nIPC→Neuroblast, Neuroblast→Granule, Radial Glia-like→Astrocytes |
| Dataset3 | Erythroid maturation | GEO GSE87038 | Blood progenitor1→2→Erythroid1→2→3 |
| Dataset4 | Human bone marrow | INSDC ERP120467 | HSC_1→Ery_1, HSC_1→Ery_2, Ery_1→Ery_2 (multi-trajectory, CBDir 최저) |
| Dataset5 | Intestinal organoid | GEO GSE128365 | Stem→TA, Stem→Goblet |
| Dataset6 | Mouse retina development | GEO GSE122466 | Neuroblast→PR/AC,HC/RGC |
| Dataset7 | Mouse hindbrain (GABA, Glial) | GEO GSE118068 | 6 cell type 발생 순서 (DeepVelo 정의) |
| Dataset8 | Mouse organogenesis | GEO GSE119945 | Early mesenchyme→Chondrocyte/Osteoblast/Myocyte 등 (DeepVelo 정의) |
| Dataset9 | Developing human cerebral cortex | GEO GSE162170 | RG/Astro→Cyc.→nIPC/ExN→ExUp |
| Dataset10 | Human first post-conception forebrain | SRA SRP129388 | Radial Glia→Neuroblast→Immature Neuron→Neuron |
| Dataset11 | Human PBMC-68k (mature) | SRA SRP073767 | CD4+/CD45RA+/CD25- naive T→CD4+/CD45RO+memory 등 (대부분 method 오방향) |
| **Dataset12** | **Human HSPC** | **GEO GSE209878** | **HSC→MPP, MPP→LMPP, MEP→Erythrocyte, GMP→Granulocyte** |
| Dataset13 | Mouse cortical neuron (scNT-seq) | GEO GSE141851 | time points 0→15, 15→30, 30→60, 60→120 (metabolic labeling 시간) |
| Dataset14 | Mouse oligodendrocyte differentiation | SRA SRP135960 | COPs→NFOLs→MFOLs |
| Dataset15 | Mouse bone marrow (low UMI) | GEO GSE109989 | neutrophil maturation (dividing→progenitors→activating) |
| Dataset16 | Embryonic mouse brain (5k, 10x multiome) | 10x Genomics / loom | RG,Astro,OPC→IPC; Deeper layer→Upper Layer |
| Dataset17 | Mouse hematopoiesis | GEO GSE81682 | LTHSC→MPP, MPP→LMPP, MPP→CMP, CMP→GMP, CMP→MEP |

> `해석:` Dataset12(Human HSPC, GSE209878)는 정확히 우리 김가경 담당 데이터의 accession이며, Li et al. 2023 MultiVelo paper(ref 10)의 데이터다. Dataset16(embryonic mouse brain 10x multiome)·Dataset17(mouse hematopoiesis GSE81682)도 우리 팀 관심과 인접. 즉 본 benchmark의 권고를 우리 HSPC에 적용할 직접 근거가 있다 — 단 MultiVelo가 `rna_only=True`로 평가된 한계 동반.

> `미제공:` Dataset12에서 각 method의 *개별 CBDir/ICCoh 수치*는 Figure 2/S1의 dataset별 point에 묻혀 있어 본문이 숫자로 명시하지 않는다. HSPC 단독 method 순위는 supplementary/원자료에서 별도 추출 필요.

### Table S2 (Supplementary) — dataset별 known differentiation order

CBDir에 적용된 ground-truth transition order 모음. 위 표의 transition 열이 이에 해당.

## Supplementary Information

- `sources/mmc1.pdf` — Supplementary figures/tables(추정: Figure S1–S6, Table S1–S2 포함). 본문이 인용한 S1(dataset별 CBDir, unseen vs tested), S2(오방향 예시), S4(cell type별 A1), S5(downsample 상세), S6(HVG 상세)가 여기 있을 것으로 보임.
- `sources/mmc2.pdf` — 대용량(약 15MB) supplementary. `추정:` 고해상도 figure 또는 dataset별 상세 plot.

> `미제공:` 본 core 작성 시 mmc1/mmc2의 개별 패널 정밀 수치는 직접 판독하지 않았다(본문 인용 범위로 한정). Dataset12(HSPC) method별 정량 비교가 필요하면 mmc1.pdf의 Figure S1·S2와 Table S1을 추가 확인.

## 분석 자체에 대한 메모

- `질문:` 본 benchmark는 MultiVelo를 `rna_only=True`(ATAC 비활성)로 평가했다. 우리 목표(chromatin–transcription lag, MultiVelo의 multi-omic 모드 활용)에서 *정작 평가받지 못한 채널*이 핵심이다. 그렇다면 이 논문은 "MultiVelo의 RNA-only 성능"만 알려줄 뿐, 우리가 쓸 multi-omic 모드의 정확도/안정성은 별도 검증이 필요하다. → lens-academic/methodology-brief에서 다룸.
- `질문:` 시나리오 권고에 MultiVelo·Chromatin Velocity 같은 epigenome-integrating method가 어느 시나리오에도 top으로 들어가지 않는다(RNA-only 조건에서 MultiVelo는 ICCoh만 높음, 0.96). 우리 데이터는 10x Multiome이므로 "Dataset16(embryonic mouse brain 10x multiome)"처럼 multi-omic 모드를 켜면 결과가 달라질 가능성 — 이 논문 범위 밖.
- `검토필요:` Figure 6C usability의 method별 정확한 time/memory 수치는 PDF 확대 판독 필요(본문 텍스트에 표 없음). methodology-brief에서 우리 리소스(GPU 1대, 128GB RAM) 대비 실행가능성 판단 시 필요.
- `해석:` HSPC(Dataset12)와 mouse hematopoiesis(Dataset17)가 모두 포함됐고, 둘 다 HSC→MPP→LMPP/CMP/MEP→terminal의 branching trajectory다. Figure 4의 "rare/transitional cell undersampling → erroneous trajectory" 경고가 우리 hematopoietic branching에 직접 적용된다.
