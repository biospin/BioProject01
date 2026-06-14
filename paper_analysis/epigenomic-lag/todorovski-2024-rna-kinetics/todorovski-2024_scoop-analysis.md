# Todorovski et al. 2024 (NAR Cancer) — Scoop 경계 분석

> **출처(grounding)**
> - PMC 전문(HTML): https://pmc.ncbi.nlm.nih.gov/articles/PMC11447529/ — **전문 접근 성공** (본 분석의 1차 근거)
> - GEO SuperSeries: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE229314 (PMID 39372038 연결 확인)
> - preprint 백업(bioRxiv 2022.04.06.487057v2)은 이번에 직접 fetch하지 않음 — 필요 시 보강.
> - 접근일: **2026-06-14**
>
> **Grounding 한계 / 확인 메모**
> - 사용자 메시지의 "GSE229314" 표기는 **본 논문 PMC 본문에는 명시 안 됨**(본문은 재분석한 GSE138210/GSE111463만 인용). 단, GEO에서 GSE229314 = 동일 제목·동일 PMID(39372038)·동일 contact(Izabela Todorovski, Peter Mac)임을 **독립 확인**했으므로 이 연구의 primary SuperSeries로 신뢰함. (단, PMC excerpt 파서가 데이터 가용성 절을 완전히 안 잡았을 수 있어 [부분확인]으로 둠.)
> - 약물 처리 시점·assay 종류 등 수치는 PMC 본문에서 두 차례 교차 질의해 일치 확인.
> - PMID 39372038, NAR Cancer 6(4):zcae039, 2024-10-03 publish — [확인].

---

## 1. 그들이 실제로 한 것 (사실)

**핵심 한 줄**: leukemia cell line(bulk)에서 transcriptional inhibitor에 대한 mRNA **down-regulation의 selectivity(어느 gene이 떨어지나)를 결정하는 1차 인자는 baseline mRNA decay rate(짧은 half-life)** 이다. chromatin(super-enhancer)·synthesis rate가 아니다.

### baseline feature (정확히 무엇인가)
- **mRNA decay rate / half-life (t½)** — 주 predictor.
  - 측정: **4sU pulse-chase + SLAM-seq** (4sU 12h labeling → washout 후 12h window sampling). normalized transcript level에 **mono-exponential decay** 피팅 → **6,580개 gene t½** 추정. 예: c-MYC t½=1.3h.
  - 모델: M(t)=K+(M₀−K)e^(−k₂t), k₁=synthesis, k₂=decay, K=k₁/k₂.
- **production / synthesis rate** — 보조. **TT-seq**(짧은 4sU labeling 5–15min, decay artifact 회피). "TT-seq RPM ÷ length ÷ sampling time"로 산출.
- **결정적**: 두 feature 비교 시 **decay rate(t½)가 dominant predictor**. 본문: *"transcript half-life was the most predictive factor for total mRNA down-regulation."* synthesis는 보조("highest production rate AND shortest half-life"가 가장 강한 repression).

### outcome (무엇을 예측?)
- **고정 시점에서의 selective down-regulation의 *magnitude/방향(class)***. **timing/속도(반응이 얼마나 빨리 일어나는가)를 시간축으로 모델링한 것이 아님.**
- 검증: simulated total mRNA가 실험 baseline abundance 및 drug-treated sample과 유의 상관; **ROC AUC 0.86–0.94**(class I/II inhibitor).

### 약물 / 시점
- **A-485(p300/CBP), JQ1(BRD4), AZ-5576(CDK9i), Actinomycin-D(RNAPII)**; MAC-seq로 **73개 compound** 스크린(class I global / II selective / III minimal로 분류).
- 시점: **SLAM-seq+inhibitor = 2h**, **MAC-seq = 6h**, c-MYC 안정화·ELAVL1 KO 검증 = 6h. (= 2개 이산 시점, **time-course 약물반응 곡선 아님**.)

### chromatin readout
- **H3K27ac ChIP-seq**(외부 GSM1652918)로 super-enhancer(ROSE2) 정의. **ATAC-seq 없음. chromatin accessibility 측정·모델링 없음. chromatin→transcription lag 개념 없음.**
- SE-associated/CR-TF gene이 전반적으로 더 down되지만 **selectivity를 설명 못 함** — 본문: *"whether a gene will or will not respond is inherently driven by additional factors, independent of the chromatin state."*

### 핵심 주장 1–3 (verbatim 근사)
1. *"It is not only the selective disruption of mRNA production, but rather mRNA decay rates that largely influence the selectivity associated with transcriptional inhibition."*
2. *"Genes down-regulated with transcriptional inhibitors are largely characterized by extremely rapid mRNA production and turnover."*
3. mRNA kinetics는 modulatable — 검증: c-MYC 3′UTR↔HPRT1 swap으로 안정화 시 mRNA 수준 저항(단 표현형 미구제); ELAVL1 KO/MS-444가 CDK9i와 synergy.

### 시스템 / 데이터
- **bulk only** (SLAM/TT/MAC-seq, total RNA-seq, 3′mRNA-seq). **single-cell·multiome 전혀 없음.**
- K562(CML), THP-1(AML) (+HEK293T, MV4;11). SuperSeries **GSE229314**.

---

## 2. 문장 단위 scoop 경계 테이블

| 축 | Todorovski 2024 | 우리(김가경) | 겹침 / 차별 |
|---|---|---|---|
| **baseline feature** | mRNA **decay rate / half-life** (RNA-side kinetics) | **chromatin→transcription lag** (chromatin accessibility가 transcription을 선행/지연시키는 정도) | **차별 핵심.** 우리는 RNA decay가 아니라 **chromatin-side 동역학**. 겹침은 "baseline kinetic feature가 drug response를 예측"이라는 *틀(frame)*뿐. |
| **측정 차원** | **bulk** (population SLAM/TT/MAC-seq) | **single-cell / 10x multiome** (RNA+ATAC 동일 세포) | 차별. multiome은 동일 세포에서 chromatin과 RNA를 동시 관측 → lag을 cell-level로 정의 가능. 그들은 bulk라 cell-state 분해 불가. |
| **outcome** | selective down-regulation **magnitude / inhibitor class** (2h·6h 이산) | drug response의 **timing / 속도(반응 kinetics)** | **차별 핵심.** 그들은 "얼마나/어느 gene이 떨어지나", 우리는 "얼마나 *빨리* 반응하나". outcome 정의 자체가 다름. (단 주의: 우리도 진짜 time-course outcome을 확보해야 함 — 3·5절 참조.) |
| **시스템** | leukemia **cell line** (K562/THP-1, transformed) | human **HSPC** (primary, normal-ish baseline) | 차별. primary HSPC baseline → drug timing 예측은 그들이 안 다룬 생물학적 맥락. |
| **chromatin** | H3K27ac SE만, accessibility 없음, "chromatin state independent"라 결론 | **chromatin accessibility(ATAC) + lag을 핵심 predictor로** | 차별 + **공격 지점**: 그들이 "chromatin state로 설명 안 됨"이라 명시 → 우리는 *그들이 안 측정한 chromatin dynamics(lag)* 가 잔여 분산을 잡는다고 주장 가능. |
| **시간 격자** | 약물반응 = 2h, 6h **이산 2점**; kinetics는 decay 쪽만 time-course | (계획) drug response time-course + pseudotime lag | 차별 가능하나, **우리 outcome이 실제 timing이 되려면 multi-timepoint 약물반응 데이터가 필수**. |

---

## 3. 핵심 판단 — 확장 가능성 (RNA-decay vs chromatin-lag)

**관계 진단: (b) 인과적 upstream/downstream + (c) 상보적 — "같은 것의 다른 측면"은 아님.**

- **upstream/downstream**: chromatin opening → transcription(production) → mRNA → decay 의 흐름에서, **chromatin-lag은 production rate의 *상류 결정자*에 가깝고, Todorovski의 t½는 mRNA의 *하류 동역학*** 이다. 즉 둘은 동일 축의 양 끝. 그들의 모델 M(t)=K+(M₀−K)e^(−k₂t)에서 transcriptional inhibitor는 k₁(synthesis)→0으로 두고 **k₂(decay)만으로 반응 magnitude를 설명** — 즉 그들의 outcome은 구조적으로 **decay-dominated인 매트릭(시점에서의 절대 감소량)**. **반면 chromatin-lag은 약물이 chromatin/PIC를 건드린 뒤 transcription이 *재설정되는 속도*에 영향** → decay 모델 바깥의 자유도.

- **같은 측면 아님 근거**: 그들 본문이 synthesis rate를 측정했음에도 **decay를 dominant로 결론**했고, **chromatin은 selectivity 설명에서 명시적으로 배제**("independent of the chromatin state"). 즉 그들의 데이터·결론 안에서 chromatin dynamics는 **미설명 잔차로 남아 있다.** 이건 우리에게 유리한 white space.

- **"chromatin-lag이 RNA-decay 너머 timing 분산을 설명한다"는 주장의 본문 근거?**
  - **유리한 근거(있음)**: (i) chromatin state가 selectivity를 설명 못 한다고 *그들 스스로* 명시 → 잔여 분산 존재 인정. (ii) 그들의 outcome은 magnitude이지 **timing이 아님** → timing 분산은 그들이 *전혀 모델링하지 않은 차원*. (iii) ATAC/accessibility를 측정조차 안 함.
  - **불리한/주의(없거나 위험)**: 그들은 timing을 outcome으로 안 봤기 때문에 **"chromatin-lag이 timing을 더 잘 예측한다"를 그들 데이터로 직접 반박/지지할 비교가 본문엔 없음.** → 우리가 그 비교를 **새로** 만들어야 하며, 만들지 않으면 "다른 outcome을 봤을 뿐"이라는 약한 차별에 그침. **이게 scoop 위험의 본질이 아니라, *차별을 입증할 책임이 우리에게 있다*는 의미.**

---

## 4. 차별화 전략 (구체적·실행가능, 값싼 순)

**전제**: 우리의 강점은 (1) chromatin-side feature(lag), (2) single-cell/multiome, (3) primary HSPC, (4) timing outcome. 그들의 약점은 (1') chromatin dynamics 무측정, (2') bulk, (3') cell line, (4') magnitude-only. → 4축 모두에서 비겹침이 있어 **포지셔닝은 명확.** 남은 건 "chromatin-lag이 *추가* 예측력"을 정량 입증하는 것.

### 값싼 win 1 — GSE229314 재분석으로 "decay-only는 timing 분산을 못 잡는다" 직접 대조 (가장 high-leverage)
- 그들의 **t½(6,580 gene)** 와 우리 multiome chromatin-lag를 **gene 단위로 join** → 두 feature의 상관·상보성 정량.
- 핵심 실험: drug response를 (a) magnitude(그들 재현) (b) timing 두 outcome으로 두고, **nested model**: `response ~ decay(t½)` vs `response ~ decay + chromatin_lag`. ΔR²(또는 ΔAUC) + likelihood ratio test로 **chromatin-lag의 incremental 예측력**을 보고.
- **제약/리스크**: GSE229314는 **bulk K562/THP-1, ATAC 없음** → *그들 데이터에는 chromatin-lag가 없음.* 따라서 직접 join은 **gene-level t½ ↔ (우리 HSPC multiome에서 얻은 gene-level lag)** 형태의 *cross-dataset gene 매핑*이 됨(세포 종 다름 → 보수적으로 "gene-intrinsic kinetic property" 가정 필요, ortholog 아닌 cell-type 차이가 confound). → **결론: "그들의 GSE229314를 재분석해 직접 head-to-head"는 부분적으로만 가능.** decay는 그들 값을 차용 가능하나, lag·timing outcome은 우리 데이터에서 새로 생성해야 함. 이 한계를 논문에 명시하고, gene-intrinsic 가정 robustness check(예: K562 자체 ATAC public으로 lag proxy 재현)를 붙이는 게 정공법.

### 값싼 win 2 — 우리 HSPC multiome으로 timing outcome을 *진짜* 만들고 decay를 통제 변수로 포함
- 우리 약물반응(time-course) 데이터에서 gene별 **response half-time / onset speed**를 outcome으로 정의.
- predictor: chromatin_lag(우리) + decay(SLAM-seq 차용 or 공개 half-life DB로 proxy) + production proxy + cell-cycle/burst confound(CLAUDE.md 방법론 주의 준수).
- **주장 형태**: "decay rate를 통제해도 chromatin-lag가 response timing의 잔여 분산을 유의하게 설명한다" → 이게 Todorovski 대비 **정면 novelty claim**.
- 리스크: **우리에게 실제 multi-timepoint 약물반응 데이터가 있어야 timing이 outcome이 된다.** 없으면 timing 주장 전체가 공허 → 이게 우리 최대 내부 리스크(scoop보다 큼). [확인필요: 우리 GSE209878은 day0/day7 *발생* 데이터지 *약물 time-course*가 아님 → outcome용 약물반응 데이터 출처를 DESIGN에서 못박아야 함.]

### 값싼 win 3 — "chromatin state independent"라는 그들 주장을 single-cell 해상도로 재검
- 그들은 bulk·SE 수준에서 chromatin이 selectivity와 무관하다 결론. 우리는 **동일 세포 내 accessibility-RNA 동시관측 + within-lineage**로, bulk에서 평균되어 사라진 chromatin-response 연관을 복원할 수 있는지 검정.
- 값싸고(우리 데이터 내부), 차별 메시지가 선명("bulk에서 안 보인 게 single-cell에서 보인다"). 리스크: 안 보이면 chromatin-lag 가설 자체에 타격 → 사실 이건 우리 가설의 핵심 sanity check이므로 어차피 해야 함.

---

## 5. scoop 위험 최종 평가

**위험도: 중(中) — 단, 조건부 하향 가능.**

- **중인 이유**: 동일 *프레임*("baseline kinetic feature → transcriptional drug response 예측")과 동일 질환축(leukemia)을 선점했고, 같은 약물군(JQ1/CDK9i)·동일 시점대(2–6h)를 사용. 표면 유사도가 높아 reviewer가 "이미 있다"고 볼 1차 위험 존재.
- **하향 근거(우리가 입증하면 하→중하)**: 4축(chromatin-lag vs decay / single-cell vs bulk / timing vs magnitude / HSPC vs cell line) **모두에서 비겹침**이고, 무엇보다 **그들이 chromatin dynamics를 측정하지 않았고 "chromatin state independent"라 명시**해 잔여 분산을 스스로 인정. → 우리 주장은 그들 결론의 *반박이 아니라 미탐색 차원의 보완*으로 깔끔히 포지셔닝됨.
- **상으로 올라가는 트리거(피해야 함)**: 우리가 outcome을 magnitude로 두거나, decay를 통제하지 않은 채 chromatin-lag 단독 예측력만 보고하면 "decay의 proxy를 chromatin으로 다시 잰 것"으로 환원돼 **scoop 위험 상**. → **반드시 decay를 통제 변수로 넣고 incremental 예측력(ΔR²/ΔAUC)으로 차별을 정량화**할 것.

### 반드시 인용·대조해야 할 그들의 결과
- **Figure 2** — t½가 most/least-responsive gene을 가르고(약 3–4배 차이), ROC AUC 0.86–0.94. → 우리 nested model 비교의 **baseline 바(SOTA)**. 우리는 "decay-only AUC = 그들 수준" 위에 chromatin-lag로 ΔAUC를 보여야 함.
- **Figure 1** — nascent(광범위) vs total(선택적) 괴리 + "SE/CR-TF가 down되나 selectivity 설명 못 함". → "chromatin으로 설명 안 됨"의 직접 근거. 우리 white space 정당화에 인용.
- **Figure 3** — 73-compound MAC-seq, decay가 다약물 across 예측. → 우리가 약물 일반화 주장할 때 비교 대상.
- **본문 명제** *"...independent of the chromatin state"* — 우리 도입부에서 가장 먼저 인용해 white space를 명시할 문장.

---

### 한 줄 verdict
프레임은 가까우나 **chromatin dynamics·single-cell·timing outcome 3축이 동시에 비어 있어 defensible novelty는 충분히 확보 가능**. 단 그 novelty는 *데이터로 입증해야* 성립하며, **(i) 약물 time-course outcome 확보, (ii) decay를 통제한 incremental-prediction 설계**가 scoop을 면하는 두 개의 결정적 조건이다.
