# Epigenetic Therapy 기반 Response Time 예측

Nature Biotechnology 2023의 multi-omic velocity framework는 gene을 크게 두 패턴으로 해석할 수 있는 관점을 제시함.

- **Model 1-like**: chromatin 변화가 먼저 일어나고 그 뒤 transcription이 따라오는 경우
- **Model 2-like**: transcription 변화가 먼저 일어나고 chromatin 변화가 뒤따르는 경우

이 연구는 여기서 한 단계 더 나아가, 단순히 변화의 순서만이 아니라 **그 사이에 걸리는 시간 차이 자체가 gene마다 유의미하게 다른가**를 묻는다.

> **각 gene에 대해 chromatin opening 이후 transcription이 시작되기까지의 priming time, 그리고 transcription shutdown과 chromatin closing 사이의 시간 차이가 유의미하게 다른가?**

- `activation lag` (`priming time`): chromatin이 열린 뒤 transcription이 시작될 때까지의 시간
- `shutdown lag` (`closing lag`): transcription이 꺼진 뒤 chromatin이 닫힐 때까지의 시간, 또는 그 반대 방향의 시간차

## Hypothesis

1. chromatin accessibility와 transcription lag은 gene마다 다르다.
2. promoter/enhancer accessibility, histone marks, TF occupancy, regulatory architecture는 activation lag과 shutdown lag의 크기를 결정하는 주요 요인이다.
3. 따라서 gene별 lag structure를 추정하면, 이후 특정 perturbation이나 epigenetic drug에 대한 반응 시간도 예측할 수 있다.

---

## Step 1. Gene-specific activation lag and shutdown lag를 정의하고 정량화

단일세포 multi-omic 또는 time-resolved ATAC/RNA 데이터를 이용해 각 gene에 대해 다음 값을 추정한다.

- chromatin opening time
- transcription onset time
- transcription shutdown time
- chromatin closing time

이를 바탕으로:

```
activation lag = transcription onset time - chromatin opening time
shutdown lag   = chromatin closing time - transcription shutdown time
```

를 계산한다.

Step 1 목적은 gene마다 서로 다른 lag distribution이 실제로 존재하는지 확인하는 것이다.

---

## Step 2. Baseline epigenomic features로 gene-specific lag structure를 예측하는 모델을 구축한다

각 gene에 대해 baseline 상태에서 다음 feature를 구축한다.

- promoter accessibility
- enhancer accessibility
- H3K27ac
- H3K27me3
- H3K4me3
- TF occupancy or motif score
- peak-to-gene linkage
- CpG density and promoter class

이 feature들을 이용해 각 gene의:

- short vs long activation lag
- short vs long shutdown lag
- 혹은 연속형 lag score

를 예측하는 모델을 구축한다.

Step 2의 목적은 어떤 baseline chromatin feature가 lag structure를 가장 잘 설명하는지 밝히는 것이다.

---

## Step 3. Gene-specific lag structure가 perturbation response timing을 예측하는지 검증한다

Aim 2에서 얻은 lag-informed model을 실제 perturbation system에 적용한다.

예를 들어 epigenetic drug 또는 특정 regulatory perturbation을 처리한 뒤, time-course RNA 또는 ATAC/RNA 데이터를 생성한다. 이후 다음을 검증한다.

- predicted short-lag genes가 실제로 더 빠르게 반응하는가
- predicted long-lag genes가 실제로 더 늦게 반응하는가
- activation lag이 짧은 gene set이 약물 초기 반응을 주도하는가
- shutdown lag이 긴 gene이 일시적 memory-like persistence를 보이는가

이 Step 3은 gene-specific lag structure가 실제 반응 시간 예측에 활용 가능한지를 보여주는 단계이다.

---

## 기대효과

- gene regulation을 더 정밀한 동역학 관점에서 이해할 수 있다.
- Model 1 / Model 2를 이분법이 아니라 연속적인 kinetic spectrum으로 확장할 수 있다.
- 특정 perturbation에 대한 반응 시간을 예측하는 새로운 feature space를 제공할 수 있다.
- epigenetic drug response를 설명할 때도, 단순 표적 효과가 아니라 gene-specific lag architecture라는 개념을 도입할 수 있다. (PRMT5i)

---

## Reference

1. **MultiVelo** (Nature Biotechnology 2023).
   이 논문은 gene별로 chromatin과 RNA의 **switch time**을 추정하고, gene을 `Model 1` / `Model 2` 로 나눈다. priming interval과 **decoupling interval** 길이로 gene들을 랭크한다. 그러나 주로 `어느 순서로` 변화가 일어나는가, 어느 유전자가 `primed/decoupled`한가, 또는 어느 `cluster`가 `asynchronous`한가 를 보여주는 데 초점이 있다.

2. **MultiVeloVAE** (Nature Communications 2025)는 그걸 더 연속적이고 lineage-specific하게 확장합니다.
   **cell-specific / gene-specific dynamics**로 다루고, chromatin opening rate와 transcription rate 차이를 이용한 **decoupling factor**까지 정의했다.

3. **MoFlow** (Nature Communications 2025/2026 record)는 gene별 DTW(dynamic time warping)로 gene별 chromatin-vs-spliced RNA lag를 계산해서 **gene regulation timing과 비동기성을 더 잘 해석하는 모델을 만들었다**.

→ 기존의 개념들을 `activation lag` / `shutdown lag` 라는 두 개의 통일된 kinetic variable으로 합친 뒤 gene별 lag structure가 **실제 perturbation이나 drug response timing prediction**에 쓸 수 있는지를 검증하는 것을 목표로 한다.

---

## Dataset

| Dataset | Accession / Source | Data type | Main biology | Used in paper(s) |
|---|---|---|---|---|
| 10x embryonic mouse brain | 10x Genomics dataset page | 10x multiome | embryonic brain differentiation | MultiVelo, Nat Biotech 2023; MoFlow, Nat Commun 2025 |
| SHARE-seq mouse skin | GSE140203 | paired chromatin + RNA | skin differentiation | MultiVelo, Nat Biotech 2023; MoFlow, Nat Commun 2025 |
| Human brain multi-ome | GSE162170 | human multiome | fetal / developing brain | MultiVelo, Nat Biotech 2023; MoFlow, Nat Commun 2025 |
| Human HSPC 10x Multiome | GSE209878 | human multiome | hematopoietic stem/progenitor state | MultiVelo, Nat Biotech 2023; MoFlow, Nat Commun 2025 |

---

## Drug

| Drug | Role | Portal / link | Data type |
|---|---|---|---|
| `Vorinostat (SAHA)` | HDAC inhibitor | L1000 / CMap: CLUE positive controls | L1000 : bulk-like perturbation transcriptomic signature |
| `Trichostatin A` | HDAC inhibitor | L1000 / CMap: CLUE positive controls | L1000 : bulk-like perturbation transcriptomic signature |
| `Valproic acid` | HDAC-related epigenetic modulator | L1000 / CMap: CLUE positive controls | L1000 : bulk-like perturbation transcriptomic signature |
| `Vorinostat (SAHA)` | HDAC inhibitor | PRISM / DepMap: DepMap compound page | PRISM : pooled cell-line drug sensitivity / viability screen |
| `Panobinostat (LBH589)` | HDAC inhibitor | PRISM / DepMap: DepMap compound page | PRISM : pooled cell-line drug sensitivity / viability screen |
| `Romidepsin` | HDAC inhibitor | PRISM / DepMap: DepMap compound page | PRISM : pooled cell-line drug sensitivity / viability screen |
| `Entinostat (MS-275)` | HDAC inhibitor | PRISM / DepMap: DepMap compound page | PRISM : pooled cell-line drug sensitivity / viability screen |
| `Azacitidine` | DNMT inhibitor | PRISM / DepMap: DepMap compound page | PRISM : pooled cell-line drug sensitivity / viability screen |
| `Pinometostat (EPZ-5676)` | DOT1L inhibitor | PRISM / DepMap: DepMap compound page | PRISM : pooled cell-line drug sensitivity / viability screen |
| `Enasidenib` | IDH2 inhibitor | PRISM / DepMap: DepMap compound page | PRISM : pooled cell-line drug sensitivity / viability screen |
| `Dacinostat (LAQ824)` | HDAC inhibitor | PRISM / DepMap: DepMap compound page | PRISM : pooled cell-line drug sensitivity / viability screen |

---

## 12주 동안의 Milestone (Step 1~2)

| 기간 | 목표 | Person 1 | Person 2 | Person 3 | Person 4 |
|---|---|---|---|---|---|
| 1-2주 | 질문/데이터셋별 전처리 | 10x embryonic mouse brain | SHARE-seq mouse skin | Human brain multi-ome | Human HSPC 10x Multiome |
| 3-4주 | dataset별 전처리 + Gene별 모델 분리(M1, M2) → M1 Gene 추출 | | | | |
| 5-6주 | M1 gene dataset lag 계산 및 dataset / gene / cell 별로 특징이 있는지 확인. | | | | |
| 7-8주 | Gene transition lag 예측 모델 구축 | | | | |
| 9-10주 | 예측 모델을 다른 데이터셋을 활용하여 상호 검증 | 10x embryonic mouse brain, SHARE-seq mouse skin, Human brain multi-ome, Human HSPC 10x Multiome | | | |
| 11-12주 | 예측 모델 결과 통합 | | | | |

---

## 검토 의견 (김가경 조사 — 회의록 기반)

### 핵심 컨셉 평가

먼저 강점부터. MultiVelo의 priming interval / decoupling interval을 **activation lag / shutdown lag** 라는 통일된 kinetic variable로 묶고, baseline epigenomic feature로 lag를 예측한 뒤 perturbation timing 예측에 활용하겠다는 3-step 구조는 깔끔하고 falsifiable함. MoFlow가 이미 DTW 기반 gene-specific lag를 산출했고 MultiVeloVAE도 decoupling factor를 정의했지만, "lag → drug response timing 예측"으로 외삽하는 angle은 실제 신규성이 있음.

다만 이 angle이 살아남으려면 아래 구조적 문제들을 proposal 안에서 명시적으로 해결해야 함.

### 가장 큰 구조적 문제: Pseudotime ≠ Wall-clock time

제안의 가장 큰 약점. Step 1–2에서 측정하는 lag는 pseudotime (또는 latent time) 단위. Step 3에서 검증하려는 drug response timing은 hours/days 단위의 실제 시간. 두 시간 축은 monotonic하긴 하지만 **일대일 맵이 아님** — splicing rate, transcriptional bursting frequency, cell cycle phase가 trajectory를 따라 비균질하게 변하면서 pseudotime↔wall-clock 변환을 gene별로 다르게 만듦.

즉 "predicted short-lag genes가 실제로 더 빠르게 반응한다"는 질문이 의미를 가지려면 pseudotime lag → wall-clock lag 변환 가능성을 별도로 입증해야 함. 단순 가정으로 넘기면 reviewer critique에서 무너짐.

**해결 옵션:**

- Step 3 데이터셋 중 적어도 하나는 4sU labeling / TT-seq 류의 **wall-clock 단위 nascent transcription 데이터**를 포함시켜 conversion factor를 검증
- 또는 Step 1을 developmental trajectory에서 **time-course multiome with drug perturbation** 시스템으로 옮김 (단 공개 데이터 거의 없음 — 아래 참고)

### Step 3 데이터 갭 — 가장 risky한 부분

LINCS L1000 + PRISM/DepMap만으로는 가설을 직접 검증할 수 없음:

- **L1000**: time-resolved지만 bulk + 978 landmark + inferred. Single-cell도 chromatin도 없음. lag 가설은 single-cell multiome에서 정의됐는데 bulk transcriptome으로 검증하면 추정 단계가 두 번 들어감
- **PRISM**: single-timepoint viability. 시간 정보 없음. lag 가설과 결이 다름
- 진짜 검증에 필요한 건 **drug perturbation 후 time-course single-cell multiome**인데 이게 공개 데이터로 거의 없음

**현실적 후퇴 옵션:**

1. Replogle/Norman 류 Perturb-seq + ATAC (CRISPRi가 epigenetic drug 대용은 아니지만 transcriptional kinetics 검증엔 활용 가능)
2. sci-Plex류 (chromatin 없음 — 부분 검증)
3. 가설을 약화: "lag ranking이 L1000 6h → 24h fold-change ratio와 상관되는가"로 축소

**권고: 12주에 Step 3 full validation은 비현실적.** Phase 1 (Step 1+2)과 Phase 2 (Step 3)로 분리하고 Phase 1 정량 결과를 보고 Phase 2 진입 여부 결정.

### 류재면 님 코멘트 재해석 필요

> "M1은 핵 진입 가능 분자량 제약이 커 약물 범위가 좁음 → M2 우선"

이 framing은 한 번 다시 봐야 함. M1/M2는 **gene regulatory phenotype** (chromatin이 먼저 변하는가 vs transcription이 먼저 변하는가)이지 **drug 작용 메커니즘이 아님**.

- Vorinostat ~264 Da, Panobinostat ~349 Da, Azacitidine ~244 Da — 모두 핵 진입에 문제 없는 small molecule
- 어떤 약물이 nuclear protein을 타깃하는지와, 그 약물이 affect하는 gene이 M1인지 M2인지는 별개 차원

오히려 **HDAC inhibitor 메커니즘은 M1-like response를 유도하는 것이 자연스러움** — 약물이 acetylation을 증가시켜 chromatin opening이 먼저, transcription이 뒤따름. 즉 HDACi에서는 **M1 gene이 더 빠르고 크게 반응**한다는 예측이 자연스럽고, 이것이 falsifiable한 가설로 더 깔끔함.

류재면 님이 의도한 바를 직접 재확인할 것. 만약 "M1 메커니즘으로 작용하는 drug 후보가 좁다"는 의미였다면 BET inhibitor, EZH2i, KDM inhibitor 등을 panel에 추가해야 함.

### 통계적 / 방법론적 우려

1. **Lag estimate의 uncertainty 정량화 미비.** MultiVelo switch time은 ML point estimate일 뿐 CI가 큼. "gene별 lag distribution이 존재한다"고 주장하기 전에 bootstrap CI, low-expression gene에서의 systematic bias를 명시해야 함. 안 그러면 "단순 coverage artifact" critique로 일축됨.

2. **Bursting kinetics confound.** High-burst-frequency gene은 systematically 짧은 lag를 보임. Burst kinetics (mean expression + variance scaling)를 covariate로 통제하지 않으면 lag prediction이 사실상 burst frequency prediction일 수 있음 — Larsson et al. 2019 류 분석과 cross-check 필요.

3. **Cell cycle confound.** 특히 proliferative system (HSPC, embryonic brain)에서 cell cycle phase는 chromatin/transcription 양쪽에 영향. cell cycle phase regress-out 하지 않으면 cluster-specific artifact가 lag로 잡힘.

4. **Multicollinearity in baseline features.** Promoter ATAC, enhancer ATAC, H3K27ac, H3K4me3, TF motif score는 강한 상관. 단순 feature importance score로는 mechanism 해석 불가. Regularized model (group lasso 등) + 명시적 feature decomposition (PCA 또는 partial correlation 기반) 필수.

5. **ChIP-seq 데이터 mismatch.** GSE70677은 bulk CD34+ HSPC. multiome은 cell-specific인데 bulk peak을 baseline feature로 쓰면 cell type 해상도를 잃음. multiome ATAC peak을 primary로, ChIP은 secondary annotation으로만 사용 권장.

6. **Multiple testing.** Gene 단위 가설 (수만 개) — BH correction, 더 보수적으로는 burst kinetics를 null로 한 permutation 기반 FDR 권장.

### MoFlow / MultiVeloVAE와의 차별화

현재 differentiation은 "기존 framework를 unify했다" 수준. 약함. 더 강한 angle 후보:

- "lag → drug timing prediction"을 Phase 1 데이터에서 명시적으로 demonstration하면 그 자체가 contribution
- Lag structure를 modulating하는 specific TF / chromatin feature identification (prediction에서 mechanism으로 한 단계 더)
- Lag가 cell-type-specific한지 vs gene-intrinsic한지의 분리 (MoFlow는 이걸 깔끔히 안 다룸)

### 실행 측면

- **12주는 빠듯**: multiome QC + MultiVelo retraining만으로 4–6주 가능. 7 dataset + 2 drug screen은 12주에 다 못 함. **Phase 1 데이터셋을 2–3개로 축소** (예: SHARE-seq mouse skin + GSE162170 human brain) 권장
- **GPU "선택사항"은 위험**: MultiVeloVAE 재현은 사실상 GPU 필요. baseline GPU 1대로 충분
- Person 4 (drug integration / writing)에 **검증/QC 책임 병행 필요** — 4명 중 실질 reviewer가 없는 구조
- Resource는 RAM 128GB, 저장 1–2TB는 적절. 단 multiome raw + intermediate가 dataset당 200–500GB 나올 수 있음

### 우선순위 추천

위 검토를 정리하면, 시급한 보강 순서:

1. **Pseudotime↔wall-clock 갭 명시 처리** (1주): proposal 내 별도 섹션으로 conversion 가정과 검증 방법을 적시
2. **Step 1–2 단단히** (4–6주): 2–3개 dataset, lag uncertainty 정량화, burst/cell-cycle covariate 통제, regularized baseline model
3. **Step 3 가설 축소** (4주): "L1000 6h vs 24h fold-change ratio가 lag와 상관"으로 좁힘 — 이건 12주 내 가능
4. **M1/M2 framing 재정립** (1주): 류재면 님 코멘트 재확인 + drug-gene phenotype mapping 명시화. HDACi → M1 gene response 예측이 자연스러움을 hypothesis로 lock
5. **Phase 2 (full drug timing validation)는 별도 proposal로 분리** — collaborator 확보 또는 자체 time-course multiome generation 필요

---

전체적으로 컨셉은 valid하고 angle도 incremental하나마 의미 있음. 그러나 **pseudotime↔wall-clock 갭과 Step 3 데이터 갭**, 이 두 holes가 proposal 안에서 명시적으로 다뤄지지 않으면 reviewer 입장에서 즉시 발목 잡힘. 이 두 가지를 어떻게 처리할지가 가장 시급한 보강 포인트.
