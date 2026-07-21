# Lens — Industry — Li 2023 cellDancer

> 본 lens는 `li-2023-celldancer_core.md`의 *객관적 분석* + `li-2023-celldancer_lens-academic.md`의 *학계 시선*을 기반으로 산업·규제·BD value 해석을 작성한다. 학술 한계 / 후속 논문 아이디어 / citation 후보는 lens-academic 참조.

## 1. Categorization

> 이 섹션은 `paper-info.yaml`의 categorization 블록과 동기화된다. 본문에는 풀어쓰고, yaml에는 구조화 값으로 기록.

### Domain (자동 추출)

- `RNA velocity`
- `single-cell-genomics`
- `deep-learning velocity inference`
- (보조) `regulatory-genomics`, `developmental biology`

### Use case (vocabulary 6개 중 1~2개)

- **`methodology-reference`** — *우선*. cellDancer의 *local cosine loss + gene별 DNN + discretized ODE 외삽*이라는 architectural pattern을 MoFlow가 직접 확장. 우리 프로젝트에서 *MoFlow를 우리 dataset에 적용할 때*, 그 *기저 method를 이해·인용*하기 위한 reference.
- **`academic-citation`** — *우선*. 본인 paper / 제안서 / 학회 발표에서 *latent time-free local relay velocity 계보*와 *multi-lineage RNA velocity benchmark*에 cellDancer 인용 필수.
- (보조) `pipeline-applicable` — RNA-only dataset이 있을 때만 직접 적용 가능. 우리 핵심 dataset은 *chromatin 포함 multiome*이므로 *MoFlow / MultiVeloVAE가 primary*, cellDancer는 *baseline 비교*에 한정.

### Importance

- **Level**: **중**
- **Perspective**: MoFlow `@hong2026moflow`의 *direct methodological predecessor*로 계보 설명과 RNA-only baseline 비교에 *필수*. 단 chromatin/epigenomic modality를 *직접 다루지 않음* → 우리 핵심 task (epigenomic-lag 정량)에는 *간접적 가치*만. 자체 BD asset이나 제품화 후보가 아니라 *방법론 backbone 인용 자료*.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: dataset 4종 모두 *n < 20k cells per dataset* (erythroid 12,329, hippocampus 18,140, pancreas 3,696, human embryo 1,054, RPE1 cell cycle 3,058). 임상 cohort 규모 (예: 100+ patient × 100k cells)와는 거리가 큼. *cell line 또는 mouse embryo development*에 집중 — *human clinical sample 검증 부재*.
- **Cohort 편향**: 모든 dataset이 *publicly available demonstration dataset*. cross-lab replication 부재. *biological replicate*도 *단일 sample / 단일 time point* 단위.
- **Replication 부족**: dataset 6종이 모두 *서로 다른 biology* — 같은 biological process를 *다른 lab의 dataset으로 재현*한 결과 없음. *해석: replication 부족, regulatory grade evidence로 부족*.
- **Selection bias**: 모든 dataset이 *cellDancer 우위가 명확한 영역*에 선별됨 — multi-lineage branching (hippocampus), transcriptional boost (erythroid MURK gene). 외부 paper (MoFlow) 평가에서는 *chromatin-aware multiome dataset에서 cellDancer가 약함*이 드러남. *cherry-picked benchmark*.
- **Multiple testing**: simulation 4 regime × 5 method = 20 pairwise 비교에 *BH/Bonferroni 명시 없음*. GO enrichment에만 BH 적용 (Fig. 2f, Fig. 3d). `해석: simulation Wilcoxon $P < 0.001$이 *multiple testing 보정 후에도 유의한지* 본문에서 직접 확인 불가.`
- **Effect size**: simulation에서 *3.5–15× error rate 감소*가 명확. 그러나 *real-data에서 정량 effect size 없음* (UMAP flow는 시각적 평가).

### 2.2 임상·기술적 제약

- **Tissue/sample 가용성**: scRNA-seq 데이터는 *10x Chromium platform* 표준 protocol — 임상 sample 적용에 *특별한 제약 없음*. 단 *fresh dissociation 필요* (대부분 fixed tissue 부적합) — *retrospective FFPE archive*에는 부적합.
- **장비·시약 가용성**: 10x Chromium scRNA-seq + standard scVelo pre-processing pipeline. *광범위하게 가용*. cellDancer 자체는 *PyTorch 기반 Python package*로 Linux/macOS 표준 환경.
- **계산 자원**: §Methods + Extended Data Fig. 10 기준 *24-core Intel Xeon W*에서 18k cells × 2,159 genes / 15 jobs / 40 min. *GPU 필수 아님* — CPU multi-core 충분. small lab도 *재현 가능*. 단 full atlas (1M cells × 20k genes) 적용 시 *cluster 환경 필요 가능* (linear scaling 가정 시 ~10 hours 추정).
- **Turnaround time**: 일반 scRNA-seq dataset (수만 cells) 단위로 *수 시간 내* — 임상 의사결정 단위 (며칠~몇 주)와 호환.
- **사용 시 dependency**: dynamo (downstream perturbation, vector field analysis) + scvelo (pre-processing) + scanpy (data handling)와 *느슨한 결합*. cellDancer 자체는 *stand-alone*이지만 *실용적으로는 ecosystem 의존*.

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**: cellDancer는 *연구용 tool* (research-use-only, RUO) — *임상 진단 또는 치료 결정 도구가 아님*. 직접적 regulatory pathway 해당 없음.
- **Analytical / Clinical validation**: 본 paper는 *method paper* — analytical validation (LOD, precision, accuracy)이나 clinical validation (sensitivity, specificity) 데이터 없음. *RUO 분류*.
- **GMP / GLP**: 해당 없음 — wet lab 실험 component 부재.
- **IRB / consent**: 사용 dataset 모두 *기존 published open access*. 본 paper 자체는 IRB 절차 없음.
- **Label·indication**: 해당 없음 — *intended use* 없음.
- **Reproducibility for audit**: 코드 GitHub open (`GuangyuWangLab2021/cellDancer`), data 모두 public accession. *기본 재현성은 OK*. 단 license 명시 부재 — `검토필요: GitHub repo에서 license 직접 확인 필요. 만약 license 없으면 default copyright protected — 상업 사용 제한.`

### 2.4 권위·신뢰 가중치

- **출처**: *1차 출처* — *Nature Biotechnology* (IF ~70, top-tier methodology venue). peer-reviewed.
- **Peer review**: ✅ (peer-reviewed, Nature Biotechnology). reviewer 정보 명시 — *Xiaojie Qiu* + anonymous (p13 Peer review information). Qiu는 dynamo 저자 (ref. 22) — *본 paper의 dynamo integration에 대한 reviewer 선정이 적절성 측면에서 *전문성은 ✅* 이지만 *친화적 selection 가능성* 분석자 추정.
- **저자 이해상충 (COI)**: 저자 명시 "no competing interests" (p13). 추가 검증 어려움.
- **Funding source**: *Houston Methodist internal grant* only (p13 Acknowledgements). NIH/공공 grant 명시 없음 — *기관 internal 자금*만으로 진행. corporate sponsorship 아님 → *결과 자체 검증* 필요성은 *NIH-funded paper 수준과 동일*.
- **저자 소속**: Houston Methodist Research Institute + Weill Cornell Medicine. *학술기관 cardiology / RNA therapeutics center*. *spinoff company 또는 license 가능 자산*인지 lens-industry §3.1에서 점검.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자/기관의 자산화 가능성**:
  - corresponding author *Guangyu Wang* (Houston Methodist) — 분야 method paper로 active. `질문: Guangyu Wang lab이 startup 창업했는지 LinkedIn / Crunchbase 확인 필요. Houston Methodist Center for Bioinformatics and Computational Biology의 commercialization 활동 검토 필요.`
  - Houston Methodist Office of Technology Transfer (또는 Weill Cornell technology licensing) 통한 *commercial license 가능성*은 *별도 inquiry 필요*.
  - patent 검색: `검토필요: USPTO / Google Patents에서 "cellDancer" 또는 "relay velocity" + Wang G. 검색 필요.`
- **공동연구 후보**:
  - 저자가 *cardiology / RNA therapeutics center* 소속 — 우리 *epigenetic therapy* 방향과 *부분 align*. 단 *direct overlap은 약함* (cardiology vs HSPC + epigenetics).
  - cellDancer GitHub repo가 active maintenance → *open community* — 공동연구보다는 *open-source contribution 또는 fork 기반 확장*이 현실적.
- **경쟁사 관찰**:
  - 우리 영역 (epigenetic therapy R&D)의 경쟁사가 cellDancer를 *직접 활용*한 사례는 *공개 정보로 확인 어려움*. `질문: bioRxiv 후속 paper에서 cellDancer를 baseline으로 사용한 industry-funded paper 검색 필요.`
  - 같은 영역 method 저자 (MoFlow `@hong2026moflow`의 Hong/Lee/Kim, MultiVelo `@li2023multivelo`의 Wang/Welch lab, MultiVeloVAE `@li2025multivelovae`의 Welch lab)가 *cellDancer를 baseline으로 인용* — *방법론 ecosystem 내부에서 standard reference*.
- **시장 영향**: cellDancer는 *single-cell genomics 도구 시장* (예: 10x Genomics, Parse Biosciences, Cellenics SaaS)에 *직접 영향 없음* — *분석 후단 (downstream analytics) 도구*. 10x / Parse는 *hardware + cloud analytics*에 focus, cellDancer 같은 algorithm은 *open-source toolkit*으로 *간접적 통합* (예: scanpy ecosystem).

### 3.2 Commercialization-candidate (자체 제품화)

- **제품 카테고리 후보**:
  - Diagnostic (Dx): 해당 없음 — *RNA velocity는 cell state dynamics 추정*, biomarker 또는 classifier 자체가 아님.
  - Assay: 해당 없음 — wet lab protocol 없음.
  - Software (SW): *제한적 가능* — cellDancer 기반 *managed pipeline service* (clinical genomics CRO offering). 단 *upstream 10x Chromium + scVelo pre-processing*과 연계되어야 가치 — *stand-alone 제품화 어려움*.
  - Therapeutic: 해당 없음.
  - Service: *내부 R&D 도구*로 활용 가능 — *clinical cohort scRNA-seq dataset의 cell fate analysis service offering*. 단 *cellDancer의 chromatin 부재* 한계로 *epigenetic therapy R&D에는 MoFlow / MultiVeloVAE가 우선*.
- **기술적 성숙도 (TRL)**: TRL 5–6 (*lab validation*, *publicly available implementation*, *multiple dataset에서 검증*). 단 *clinical-grade validation 없음*.
- **IP 자유도**: `검토필요: cellDancer GitHub repo license 직접 확인 필요. 만약 *no license* 명시면 default copyright protected — 상업 사용 시 *commercial license 별도 협상* 필요. 만약 MIT/BSD/Apache면 *상업 fork + 수정 자유*.`
- **MVP 시나리오**: 우리 HSPC 10x Multiome dataset에 cellDancer 직접 적용 → MoFlow와의 head-to-head 비교 → *RNA-only baseline*으로서의 정량 위치 확보. ~ 2주.

### 3.3 우리 파이프라인과의 fit

- **현재 dataset 호환**: 우리 4개 dataset 모두 *10x Multiome 또는 SHARE-seq* — *chromatin + RNA 모두 포함*. cellDancer는 *RNA only* 사용 → *chromatin information을 활용 안 함* → 우리 *epigenomic-lag* task에는 *본질적 fit 약함*. 단 *baseline 비교용*으로는 활용 가능.
- **자원 가능성**: 우리 환경 (CPU multi-core 충분, GPU 가능)에서 직접 적용 가능. PyTorch 환경, scvelo / scanpy 표준 ecosystem. *기술적 fit OK*.
- **전략적 align**:
  - 우리 핵심 task (chromatin-RNA lag → epigenetic drug response time)에는 *chromatin 정보가 핵심*. cellDancer만으로는 *Step 1 (lag 정량) 자체 수행 불가*.
  - MoFlow / MultiVeloVAE / MultiVelo가 *primary tool*, cellDancer는 *RNA-only baseline + 계보 설명* 위치.
- **빠진 capability**:
  - chromatin accessibility 통합 → MoFlow 또는 MultiVelo로 보완.
  - multi-sample / batch harmonization → MultiVeloVAE의 cVAE 또는 Harmony / scVI로 보완.
  - cell cycle confound 처리 → 별도 sub-pipeline (예: tricycle, ccRemover) 필요.

### 3.4 후속 BD·제품 액션 후보

- **액션 1: cellDancer GitHub license 확인 + commercial use 가능성 검증**
  - 누가: 본인 + (필요 시) Houston Methodist Technology Transfer Office contact
  - 언제: 다음 sprint (이번 달)
  - 자원: GitHub repo 30분 확인 + email 1통
  - 성공 기준: license 명시 확인 (MIT/BSD/GPL/no-license/proprietary), commercial use 가능성 yes/no 판정

- **액션 2: 우리 HSPC 10x Multiome dataset에 cellDancer 적용 (RNA-only baseline)**
  - 누가: 본인 / jmryu (kkkim + jamie team)
  - 언제: 다음 분기 (~ 2개월)
  - 자원: GPU 환경 (또는 24-core CPU), 1주 wall time, 1 person-week
  - 성공 기준: HSPC dataset에서 cellDancer CBDir / In-cluster coherence 정량 → MoFlow / MultiVelo / MultiVeloVAE와 *4-way 비교 table* 작성. cellDancer가 *어떤 영역 (만약 있다면)에서 우위*인지 확인.

- **액션 3: cellDancer를 *baseline-only reference*로 internal benchmark suite에 등재**
  - 누가: 본인 (Week2 evidence integration)
  - 언제: 지금 (Week2 _evidence/papers.jsonl 갱신 시점)
  - 자원: paper-info.yaml + papers.csv 갱신, build_index.py 재실행
  - 성공 기준: `analysis/_index/epigenomic-lag.md`에 cellDancer가 *methodology-reference + academic-citation*으로 등재, importance 중.

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: **중**
- **Perspective**: MoFlow `@hong2026moflow`의 *direct methodological predecessor*로 계보 설명과 RNA-only baseline 비교에 *필수*. chromatin/epigenomic modality 부재로 우리 핵심 task에는 *간접 가치*.
- **등급 근거**:
  - `li-2023-celldancer_core.md` §Methods의 *latent time-free local cosine loss*가 MoFlow의 *직접적 architectural ancestor* — MoFlow의 *chromatin opening/closing 양쪽 가설 lower-loss 선택* 메커니즘은 cellDancer cosine loss의 *chromatin domain 확장*.
  - simulation에서 *cellDancer multi-forward branching error rate 2.63% vs DeepVelo 82.16%* (15×)는 *flagship number*로서 RNA velocity 방법론 review에 인용 가치.
  - 코드 (`GuangyuWangLab2021/cellDancer`) GitHub open + data 모두 public — *기본 재현성 OK*. 단 license 명시 부재로 *상업 사용 제한 가능성*.
  - chromatin/multi-omic 부재 — 우리 *epigenomic-lag* task에서 *primary tool 후보 아님*. MoFlow / MultiVeloVAE / MultiVelo가 우선.
  - real-data 정량 metric (CBDir 등) 본문 부재 — *외부 후속 paper (MoFlow) 평가에서 cellDancer가 chromatin-aware dataset에 약함*이 드러남 — 본 paper만으로는 *cellDancer의 약한 영역 인식 어려움*.

### 4.2 활용 우선순위

- **지금 (이번 sprint / 이번 달)**: Week2 `papers.jsonl` evidence record에 cellDancer를 *MoFlow predecessor*로 등재 + license 확인. `analysis/_index/epigenomic-lag.md`에서 *방법론 계보 narrative* 구축.
- **다음 분기**: HSPC dataset에 RNA-only cellDancer baseline 적용 → MoFlow와 head-to-head 비교. *cellDancer가 RNA-only modality에서 어느 정도 우위*인지 우리 dataset에서 정량.
- **장기**: cellDancer의 *kinetic rate cell identity marker* use case (Figure 4, Extended Data Fig. 6)를 *cohort-scale clinical scRNA-seq* (예: AML patient cohort)에 적용 시 *batch-invariant cell type classification feature*로서 가치 검증. (epigenetic therapy 본 line과는 별도 spin-off 가설.)

### 4.3 발표·미팅에서 들이밀 시점

- **본인 학회 발표 / 논문 introduction**: *MoFlow → 우리 프로젝트* 계보 narrative에서 *원조 (cellDancer) → 확장 (MoFlow)*의 method evolution 그림 그릴 때. Figure 1 schematic 재인용.
- **사내 R&D 리뷰**: 우리 HSPC dataset 분석 결과 발표 시 *RNA velocity baseline 4종 (scVelo, cellDancer, MultiVelo, MoFlow)* table에 cellDancer 등재.
- **BD 미팅**: *별도 BD 가치 약함*. *MoFlow 또는 MultiVeloVAE BD case*가 우선이고 cellDancer는 *방법론 ecosystem 설명*에 한정.
- **사내 newsletter / 동향 공유**: *Welch / Wang / Hong 3 lab의 RNA velocity 계보*를 정리하는 *방법론 evolution 시리즈* 첫 글에 cellDancer.

### 4.4 추가 탐색 필요 영역

- **질문**: cellDancer GitHub repo (`GuangyuWangLab2021/cellDancer`) license 명시 여부 — 상업 사용 가능 여부 결정.
- **질문**: Guangyu Wang lab의 *후속 paper* 또는 *cellDancer-update version*이 2024–2026 사이에 나왔는가? metabolic labeling 통합 (§Discussion p9 future work)이 실제 구현되었는가?
- **질문**: USPTO / Google Patents에서 "cellDancer" 또는 "relay velocity" + Wang G. 검색 — patent 등록 여부.
- **질문**: 우리 HSPC 10x Multiome dataset (GSE209878)에 cellDancer 적용 시 *cell cycle confound* 처리 방법 — cell cycle gene을 *pre-filter*할지 *post-hoc covariate regression*할지. cellDancer 본문은 *통제 없음*.
- **질문**: cellDancer 적용 시 *neighbor graph (UMAP / PHATE / diffusion map) 선택*의 sensitivity — 본 paper는 spliced-only vs spliced+unspliced 비교만 (Extended Data Fig. 7a). 우리 HSPC의 trajectory가 *neighbor graph 선택*에 얼마나 sensitive할까?
- **질문**: cellDancer의 *outlier neighbor*에 대한 sensitivity — SHARE-seq 같은 *technical noise 많은 multiome*에서 doublet/contamination이 cellDancer max-over-neighbor cosine loss를 *artifact direction*으로 끌고 가는지 — 우리 SHARE-seq 데이터에서 미니 실험 필요.
