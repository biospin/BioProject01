# Lens — Industry — Mizukoshi 2024 DeepKINET

Citation key: `@mizukoshi2024deepkinet`. Core analysis: `mizukoshi-2024-deepkinet_core.md`. 학술적 한계·후속 연구 idea는 `mizukoshi-2024-deepkinet_lens-academic.md`. 본 lens는 *산업·규제·BD 시선*만 다룬다.

## 1. Categorization

### 1.1 Domain
- `single-cell-genomics`, `RNA velocity`, `splicing kinetics`, `metabolic labeling`, `deep generative model`.
- 부수 응용: `cancer kinetics`, `MDS/hematologic malignancy`, `splicing factor mutation`.

### 1.2 Use case
- `methodology-reference`: 2-stage VAE decoupling + cell-state-dependent kinetic rate decoder 패턴은 *우리 epigenomic-lag method 설계*에 직접 차용 가능.
- `academic-citation`: RNA-only kinetics에서 metabolic labeling benchmark의 *standard* reference. 우리 후속 paper의 validation framing 인용.
- (`pipeline-applicable` 후보 — 부분): scEU-seq/scNT-seq data가 우리 손에 들어오면 그대로 적용 가능. 단 우리 HSPC pipeline은 *Multiome*이라 직접 fit은 아님. 따라서 본 use case는 *secondary*로만 표시.

### 1.3 Importance
- **Level**: 중
- **Perspective**: epigenomic-lag *direct* method는 아니나 *kinetic-rate validation의 standard framework*로 우리 Week2 evidence bundle의 가장 약한 지점(causal/ground-truth validation gap)을 보강. 직접 pipeline 차용은 ROI 낮음, BD/제품화 직접 후보는 아님.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Cell-level ground truth 부재**: 본 method가 *cell-level* rate를 산출하지만 검증은 *cluster-level*에서 종료. *환자별 진단 결정*에 cell-level rate를 직접 쓰려면 *임상적으로 의미 있는* cell-level validation이 별도 필요.
- **Simulation self-favorable risk**: SERGIO를 *저자가 직접 수정*해 cluster별 rate를 inject. cellDancer/DeepVelo는 *다른 inductive bias*. 우리 환경에서 재현할 때는 *완전 외부 simulator*로 cross-check 필수.
- **Metabolic labeling proxy ground truth → Dynamo 의존**: scEU-seq raw labeled fraction이 ground truth가 아니라 *Dynamo가 후처리한 cluster rate*가 ground truth. Dynamo 가정이 잘못되면 모든 비교가 잘못됨 — *vendor lock-in risk* 유사.
- **Single-cell-level 수치 부재**: 본문 텍스트에 *Pearson r, RMSE, rank concordance*의 정확한 수치가 명시되지 않음 (box plot만). 재현 검증 보고서에 *수치 인용*이 필요하면 supplementary source data 별도 요청 필요.
- **다중 검정**: Fig. 4 RBP target enrichment, Fig. 5 RBM47 interaction term, Fig. 6 SF3B1 mutation 모두 *gene 단위*. BH correction 사용 (저자 명시). 단 gene set이 *highly variable genes 1000–2000*으로 미리 좁혀짐 → *full transcriptome*에 적용 시 FDR 재계산 필요.

### 2.2 임상·기술적 제약

- **Wet-lab 검증 부재**: cellular knockdown/overexpression으로 *추정된 cell-specific rate가 실제 functional rate와 일치*하는지 *직접* 확인 없음. 임상 결정 근거로 쓰기 전에 *최소 한 case*에 perturbation 실험 필요.
- **scEU-seq/scNT-seq의 임상 적용 한계**:
  - 5-EU(또는 4sU) labeling은 *살아있는 세포*에서 incubation 필요 → fresh living sample만 가능. *FFPE / frozen 환자 sample*에 적용 불가.
  - Labeling 화학물질(5-EU, 4sU)은 *세포 toxicity*가 있음. clinical-grade IRB approval 별도 필요.
  - 외부 맥락: scEU-seq protocol 자체는 *연구용*으로 published (Battich 2020, Science) — clinical CLIA assay로 승인된 사례는 없음 (추정).
- **GPU 의존성**: 본 paper는 TSUBAME3.0, AI Bridging Cloud Infrastructure(ABCI), Tokyo대 SHIROKANE supercomputer 사용 (Acknowledgements, p.18). 일반 lab GPU(예: V100 1대)로 *얼마나 시간 걸리는지* 본문 명시 없음 — 미제공.
- **AnnData/scVelo 생태계 의존**: scvelo.pp.filter_and_normalize(), Velocyto count matrix 전처리 필수. 우리 기존 pipeline과 호환 가능하나 *parameter*가 우리 default와 다를 수 있음 (min_shared_counts = 20/100, n_top_genes = 1000/2000 등 dataset별로 저자가 변경).

### 2.3 규제·QA·RA 관점

- **MIT license + Zenodo deposit (10.5281/zenodo.13054695)**: 상업적 활용 *허용*. license 충돌 없음.
- **FDA/EMA 직접 precedent 없음**: 본 paper는 *순수 method paper*. clinical decision support tool로 승인된 적 없음 (추정 — 본문 명시 없음). regulatory pathway 참조용으로는 직접 사용 불가.
- **재현 자료 충분도**: GitHub + Zenodo + 모든 dataset GEO accession (GSE132188, GSE128365, SRP129388, GSE167036) 공개. *재현은 가능*. 단 우리 *진단 product 검증 보고서*에 인용하려면 별도 IND-supporting documentation 필요.
- **데이터 출처의 환자 동의 범위**: 본 paper의 MDS-RS data (Adema 2022)는 기존 published cohort. 우리가 *동일 method를 자체 cohort에 적용*하려면 별도 IRB의 *secondary use* 검토 필요.

### 2.4 권위·신뢰 가중치

- **1차 출처**: peer-reviewed *Genome Biology* (BMC), Q1, IF 12 가량 (외부 맥락 — 본문 명시 없음). 충분한 peer-review 권위.
- **저자 소속**: Nagoya University Medical Graduate School + National Cancer Center Research Institute (NCC) + Tokyo Medical and Dental University. 일본 ML + 임상 RNA biology 교집합. *clinical context*가 강함 (특히 NCC).
- **이해상충**: "The authors declare no competing interests" 명시 (p.18). DeepKINET 자체가 상업 제품이 아니라 open-source academic tool.
- **Funding**: JSPS, AMED, JST Moonshot R&D 등 일본 정부 funding. 산업 후원 없음.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자 lab과의 contact 후보**: Yasuhiro Kojima (NCC, yakojim@ncc.go.jp) 또는 Teppei Shimamura (TMDU, shimamura.csb@tmd.ac.jp). Kojima lab은 VICDYF 등 *deep generative single-cell* 계열 활발. *공동연구* (특히 MDS/AML 같은 hematologic malignancy)에서 우리 HSPC pipeline과 *겹치는 cohort* 협업 가능성.
- **경쟁사 동향**: cellDancer (Li lab, MIT/Texas A&M, `@li2023celldancer`), DeepVelo (Wang lab, Toronto, `@cui2024deepvelo`) 등 *cell-specific rate* method가 빠르게 늘어남. *kinetic rate-based clinical biomarker* 시장은 *아직 형성 전 단계*. early-mover advantage 있을 수 있음.
- **Splicing factor mutation × therapeutic response** 응용 (본 paper Fig. 6 SF3B1 사례): *임상적으로 중요한 angle*. SF3B1 inhibitor (예: H3B-8800, Otzuka) precision therapy 후보 stratification 도구로 발전 여지.

### 3.2 Commercialization-candidate (자체 제품화)

- **본 method 자체의 제품화 후보 등급**: *낮음*. RNA-only kinetic rate method는 *연구용*. clinical Dx로 만들기 위해서는 (a) scEU-seq나 metabolic labeling 자체의 clinical assay화, (b) 추정 rate가 임상 결정에 직접 사용된 *evidence*가 필요. 둘 다 현재 없음.
- **간접 응용**:
  - SF3B1/SRSF2/U2AF1 mutation patient stratification — MDS/AML 진단보조 SW로 발전 가능.
  - Splicing kinetics 기반 *RBP-targeted therapy* response predictor — exploratory phase.
- 결론: 본 method *자체*를 제품화하기보다 *우리 epigenomic-lag method가 동등한 validation framework로 무장*해 더 상위 단계 product (예: chromatin-RNA lag-based drug response timing predictor)의 *validation gold standard*로 인용하는 indirect leverage가 더 현실적.

### 3.3 우리 파이프라인과의 fit

- **HSPC 10x Multiome (kkkim/jamie 담당) 직접 fit**: ❌. 본 method는 RNA only, chromatin 없음. Multiome data에 그대로 적용해도 *chromatin part 무시*.
- **HSPC 10x Multiome → DeepKINET RNA part만 적용**: ⚠️ 부분. 우리 HSPC는 *labeling 없는* multiome. DeepKINET을 *labeling-free* mode로 돌리면 cellDancer/DeepVelo와 같은 *cell-specific rate*가 나오지만 *validation 자체가 우리 환경에서 불가* (scEU-seq 없음). 단순 *exploratory*로만 가능.
- **Validation framework 차용**: ✅. 본 paper의 *evaluation pattern* (simulation 20×10 + labeling 100회 반복 + box plot + negative-correlation fail rule)을 우리 lag method evaluation에 *그대로* 적용 가능 (자세히는 `mizukoshi-2024-deepkinet_lens-academic.md` §3 참고).

### 3.4 scEU-seq / scNT-seq 자체 시도 feasibility — 우리 institution에서 가능한가?

> 본 sub-section은 *우리가 직접 scEU-seq/scNT-seq를 수행*해 chromatin-transcription lag validation을 할 수 있는지 평가.

#### 3.4.1 Instrument & reagent

- **scEU-seq (5-ethynyl uridine, click chemistry-based labeled RNA selection + scRNA-seq)**:
  - 핵심 reagent: 5-EU (Click-iT chemistry kit, Invitrogen/Thermo), biotin-azide, streptavidin pull-down 시약.
  - Sequencing platform: 10x Chromium + Illumina (우리 기존 platform과 호환). 단 *Click-iT module*은 표준 10x workflow 안에 *없음* — wet-lab side에서 *custom modification* 필요.
  - 외부 맥락: scEU-seq 원본 protocol (Battich 2020, Science)은 RPE1-FUCCI 같은 *cell line*에 적용. 일반 *primary cell* (특히 HSPC)에 직접 적용한 사례는 매우 제한적 — 추정.
- **scNT-seq (4-thiouridine, T-to-C conversion + scRNA-seq)**:
  - 핵심 reagent: 4-thiouridine (4sU), iodoacetamide for alkylation, custom UMI design.
  - Platform: Drop-seq 기반 (원본 Qiu 2020). 10x Chromium 호환 *변형*은 별도 protocol 필요 — 추정 검토필요.

#### 3.4.2 Cost 추정 (해석)

- 해석: 본 논문에는 *cost 정보 전혀 없음*. 분석자 추정 (외부 맥락 기반).
- 5-EU 5g 가량 vendor 기준 ~$200, click chemistry kit per sample 수십~수백 달러. *Reagent cost* 자체는 sample당 10x experiment 기본 비용 대비 +20~50% 정도로 *manageable*.
- *Wet-lab labor*가 더 큰 cost. labeling time-course 설계, pulse/chase 단계 timing 정밀 통제 → *전담 wet-lab 시간 ≥ 2주/condition*.
- *Sequencing depth*: labeled RNA가 *전체 RNA의 소수*이므로 deeper sequencing 필요. 평균 +50~100% sequencing cost — 추정.

#### 3.4.3 Regulatory / IRB

- **5-EU와 4sU의 cellular toxicity**: *living cell incubation* 필수. *임상 환자 sample에 직접* incubation은 IRB *별도 승인* 필요 (외부 맥락 — clinical-grade assay 승인 사례 없음, 추정).
- **임상 sample이 아닌 *in vitro cell culture* 단계 적용**: 우리가 HSPC를 *in vitro 배양*해 labeling → 그 후 scRNA-seq 하는 design은 *기본 연구 IRB로 가능* (추정). 단 환자 sample을 in vitro로 배양하는 단계의 별도 승인 필요.
- **Chromatin-aware extension** (우리가 진짜 원하는 것): 5-EU/4sU와 *chromatin labeling*을 동시에? 현재 표준 protocol *없음*. 검토필요.

#### 3.4.4 종합 평가

- **단기 (3개월 이내)**: 자체 scEU-seq 수행 ❌. 기존 published scEU-seq data (GSE128365)에 *우리 method를 시험 적용*하는 단계만 가능.
- **중기 (6~12개월)**: in vitro HSPC + scEU-seq feasibility study 가능 *if* wet-lab 협업 partner (예: NCC Kojima lab 또는 국내 wet-lab) 확보. 우리 단독으로는 wet-lab capability 부족.
- **장기 (1년+)**: chromatin labeling + RNA labeling 동시 single-cell assay 개발은 *novel method development* 영역. 자체 R&D pipeline에서 *연구 과제 별도 정의* 필요.
- **결론**: 본 method의 *validation framework는 즉시 차용 가능*. *labeling data 자체*는 우리 환경에서 *단기* 자체 생산 불가. *Validation 보강이 우리 method paper의 핵심 contribution*이 될 수 있는 BD 포인트 있음 (외부 협업으로 풀어야 함).

### 3.5 후속 BD·제품 액션 후보

1. **NCC Kojima lab과 academic-industry contact 시도** — HSPC multiome + labeling 협업 가능성 탐색.
2. **자체 method paper에서 DeepKINET을 "RNA-only validation의 standard"로 명시 인용** — 우리 chromatin-aware contribution의 *delta*를 부각.
3. **국내 wet-lab partner (HSPC + labeling capability) 매핑** — 별도 surveying 필요.
4. **MDS/AML cohort에 SF3B1 mutation × DeepKINET 적용** — 우리 HSPC 환자 cohort가 있으면 *clinical exploratory analysis* 후보.

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 중
- **Perspective**: epigenomic-lag *direct* method가 아니라 *RNA-only kinetic-rate validation의 standard reference*. 우리 후속 paper의 validation framing 강화 + 후속 method idea (chromatin-aware DeepKINET) 명시적 motivation 제공. 단 직접 pipeline 차용 ROI는 낮고, 자체 제품화 후보는 아님.
- **등급 근거**:
  - ➕ Week2 validation_report C8의 *유일한 metabolic-labeling reference* — 다른 candidate 없음.
  - ➕ 저자 본인이 *MultiVelo로 chromatin extension*을 직접 신호 → 우리 stack과 자연 연결.
  - ➕ Validation framework (simulation + labeling + 100회 반복 + box plot) 즉시 차용 가능.
  - ➖ chromatin 직접 다루지 않음 — *우리 핵심 문제*는 아님.
  - ➖ Single-cell-level ground truth 부재 — *clinical decision-level evidence*로는 약함.
  - ➖ scEU-seq 자체 생산은 우리 환경에서 단기 불가.

### 4.2 활용 우선순위

- **지금**: Week2 validation_report C8 update 근거로 즉시 사용. 본인 method paper draft의 "validation framework" 섹션 인용 후보로 표시.
- **다음 분기**: 우리 chromatin-aware method paper draft 작성 시 *baseline framing reference*로 활용. *DeepKINET-Multiome* 후속 idea를 white-paper 또는 internal proposal로 정리.
- **장기**: NCC Kojima lab BD contact, 국내 wet-lab partner mapping (scEU-seq capability).

### 4.3 발표·미팅에서 들이밀 시점

- **본인 PPT 발표 (학회/사내 review)**: "RNA-only에서는 DeepKINET이 metabolic-labeling validation standard를 세웠다. 우리는 chromatin-RNA lag에서 동등한 framework를 세운다"는 *대조 framing*에서 인용.
- **BD 미팅**: NCC contact 가능성 brief에서 *우리가 활용하고 싶은 외부 자산*으로 언급. 직접 라이선싱 대상은 아님 (open-source MIT).
- **R&D 리뷰**: validation 설계 sub-section에서 *evaluation pattern* (multi-method 100회 반복 + negative-correlation rule)을 우리 evaluation plan의 기본 template로 제안.

### 4.4 추가 탐색 필요 영역

- 질문: scEU-seq를 *primary HSPC*에 적용한 사례가 publishing되어 있는가? — 별도 PubMed search.
- 질문: NCC Kojima lab의 *후속 paper* (DeepKINET-Multiome 시도)가 preprint로 나왔는가? — bioRxiv 모니터링.
- 질문: 국내 wet-lab 중 *5-EU labeling + 10x Multiome combined capability* 있는 곳이 있는가? — 내부 매핑 필요.
- 질문: SF3B1 mutation × DeepKINET rate analysis 결과를 우리 HSPC cohort에 적용했을 때 *임상 결정*에 의미 있는 stratification이 나오는가? — exploratory analysis 후보.

마지막 갱신: 2026-05-26
