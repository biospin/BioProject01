# cellwhisperer-2025-nat-biotech_core.md

## Executive Summary

- **무엇**: scRNA-seq 데이터를 자연어 채팅으로 탐색하기 위한 multimodal AI 시스템 CellWhisperer. 100만 개 이상의 RNA profile과 LLM 생성 텍스트 주석을 contrastive learning으로 결합, 사용자 제공 단일 세포 데이터에 대해 자연어 질의 및 chat 기반 생물학적 해석을 가능하게 한다.
- **모델 / 방법**: (1) Geneformer(전사체) + BioBERT(텍스트)를 CLIP 방식으로 공동 임베딩 훈련 → 2,048차원 joint embedding space; (2) Mistral 7B LLM을 transcriptome 임베딩을 추가 입력으로 받도록 fine-tuning. 학습 데이터: GEO + CELLxGENE Census에서 수집한 1,082,413쌍의 transcriptome-텍스트 annotation.
- **핵심 결과**:
  - ① Tabula Sapiens (20 common cell types, n=184,450 cells) zero-shot cell type AUROC = 0.94, Accuracy = 0.61 — fine-tuned scFM 3종과 동등 수준.
  - ② ImmGen bulk RNA (42 types) 및 Asian Immune Diversity Atlas (9 types, n=7,842) zero-shot AUROC > 0.99.
  - ③ Human Diseases dataset (229 disease subtypes) zero-shot AUROC = 0.82.
  - ④ Human Development meta-analysis: 6개 독립 embryo dataset (95,092 scRNA-seq profiles)에서 4단계 temporal dynamics 및 10개 장기 발달 진행 포착; heart marker gene overlap odds ratio = 10.2 (p = 1.4×10⁻⁵²).
  - ⑤ Chat model perplexity 평가: Evaluation Conversations (n=200)에서 matched transcriptome 임베딩에 대해 90% preference.
- **우리 적용**: HSPC multiome dataset에 CellWhisperer 임베딩을 적용하여 cell type 주석 및 cluster label 자동 생성 시도 가능 (pipeline-applicable). 코드 및 모델 가중치 공개 (GitHub: https://github.com/epigen/cellwhisperer).
- **심층**: 한계·재현 ROI는 `cellwhisperer-2025-nat-biotech_lens-academic.md` / `cellwhisperer-2025-nat-biotech_lens-industry.md` / `cellwhisperer-2025-nat-biotech_methodology-brief.md` 참고.

---

## Identity

- **Title**: Multimodal learning enables chat-based exploration of single-cell data
- **Authors**: Moritz Schaefer, Peter Peneder (공동 제1저자), Daniel Malzl, Salvo Danilo Lombardo, Mihaela Peycheva, Jake Burton, Anna Hakobyan, Varun Sharma, Thomas Krausgruber, Celine Sin, Jörg Menche, Eleni M. Tomazou, Christoph Bock (corresponding author: cbock@cemm.oeaw.ac.at)
- **Year**: 2025
- **Venue**: Nature Biotechnology (Published online: 11 November 2025; Received: 15 October 2024; Accepted: 11 September 2025)
- **DOI**: 10.1038/s41587-025-02857-9
- **Citation key**: schaefer2025cellwhisperer
- **Affiliations**: Medical University of Vienna (CEDAS/CAIM), CeMM Research Center for Molecular Medicine (Austrian Academy of Sciences), St. Anna Children's Cancer Research Institute, Max Perutz Labs Vienna, University of Vienna (여러 학과), Ludwig Boltzmann Institute for Network Medicine, Medical University of Vienna Center for Cancer Research 외.
- **Competing interests**: Christoph Bock는 Myllia Biotechnology 및 Neurolentech의 공동창업자 및 scientific advisor. 나머지 저자는 competing interests 없음.
- **Funding**: Medical University of Vienna (open access funding). European Research Council (ERC) Consolidator Grant (101001971), Austrian Science Fund (P34958), Vienna Science and Technology Fund (LS18-049, LS20-045). Human Cell Atlas 프로젝트 일부.
- **Open access**: Creative Commons Attribution 4.0.

---

## Background

#### 배경 스토리

- **문제의 출발점**: scRNA-seq는 세포 수준에서 유전자 발현 프로파일을 제공하지만, 데이터 해석은 bioinformatics 전문지식과 분야별 생물학적 지식을 동시에 요구한다. 수만 개 유전자 × 수백만 개 세포의 count matrix를 분석하는 작업은 복잡한 코드와 여러 도구를 필요로 한다.
- **선행 접근 A — scRNA-seq 분석 소프트웨어**: `scanpy` 등의 도구가 시각화·클러스터링·differential expression·gene set analysis를 지원하지만, 사용자가 분야별 workflow를 직접 설계하고 구현해야 한다.
- **A의 한계**: 분석 진입장벽이 높아 프로그래밍 경험이 없는 생물학자에게 사용이 어렵다. 탐색적 가설 생성에 비효율적이다.
- **선행 접근 B — Single-cell foundation models (scFMs)**: Geneformer, scGPT, UCE 등이 대규모 scRNA-seq 데이터로 사전훈련되어 cell type annotation, trajectory analysis 등 다양한 downstream task에 적용 가능해졌다.
- **B의 한계**: scFM들은 특정 분석 task에 fine-tuning이 필요하고, 사용자가 자연어로 자유롭게 질문하거나 대화를 통해 생물학적 맥락을 탐색하는 기능이 없다.
- **선행 접근 C — 멀티모달 LLM 접근 (LangCell, Cell2Sentence 등)**: LangCell은 transcriptome-text contrastive 임베딩을 학습하지만 개별 세포 수준 대화를 지원하지 않는다. Cell2Sentence(C2S)는 세포 하나마다 비싼 LLM 실행이 필요하다.
- **C의 한계**: 커뮤니티 규모의 대규모 데이터를 활용한 multimodal training 및 실제 배포 가능한 웹 인터페이스 통합이 없다.
- **이 논문으로 이어지는 gap**: GEO + CELLxGENE Census의 100만 규모 transcriptome-텍스트 쌍을 LLM 보조 큐레이션으로 생성하고, CLIP 기반 multimodal 임베딩 모델과 LLM chat 모델을 결합해 CELLxGENE Explorer에 직접 통합된 자연어 chat 기반 scRNA-seq 탐색 도구를 제시한다.

#### 기본 개념

- **CLIP (Contrastive Language-Image Pretraining)**: 이미지와 텍스트 pair를 같은 embedding space에 놓도록 학습하는 방식. CellWhisperer는 이를 transcriptome과 텍스트에 적용한다.
- **Geneformer**: ~30M개 scRNA-seq 프로파일로 사전훈련된 transformer 모델. 유전자 발현 rank order를 입력으로 받아 세포의 transcriptome 임베딩을 생성한다 (12 layers, 40M parameters).
- **BioBERT**: 생물의학 텍스트로 사전훈련된 BERT 계열 언어모델. 텍스트 annotation을 임베딩하는 데 사용 (12 layers, 110M parameters).
- **Mistral 7B**: 70억 파라미터 open-weights LLM (Instruct v0.2). CellWhisperer에서 fine-tuning을 통해 transcriptome 임베딩을 추가 입력으로 받아 chat 응답을 생성한다.
- **CellWhisperer score**: 텍스트 쿼리 임베딩과 각 transcriptome 임베딩 사이의 cosine similarity를 softmax-변환한 확률 기반 매칭 점수. 높을수록 텍스트 쿼리와 해당 transcriptome이 잘 매칭됨을 의미한다.
- **Pseudo-bulk transcriptome**: scRNA-seq 데이터에서 동일 metadata group(예: cell type + sample)에 속하는 세포들의 count를 평균 내어 만든 bulk 수준의 profile. CellWhisperer 학습 데이터 구성의 기본 단위.
- **Perplexity (LLM 평가)**: 주어진 context에서 정답 응답 토큰의 예측 확률을 수치화한 것 (지수화된 평균 negative log-likelihood). 낮을수록 모델이 정답을 더 잘 예측한다.

#### 이 논문의 필요성

- **핵심 이유**: scRNA-seq 데이터 해석을 자연어로 민주화하여, 프로그래밍 경험 없이도 생물학적 탐색이 가능한 직관적 채널을 제공.
- **기존 방법으로 부족했던 지점**: scFM + 코드 기반 접근법은 탐색적 가설 생성에 비효율적이고, 기존 LLM 접근은 커뮤니티 규모 데이터 활용 및 대화형 웹 통합이 부재.
- **이 논문이 해결하려는 방향**: GEO + CELLxGENE Census의 대규모 데이터를 LLM 보조 큐레이션으로 통합 → multimodal 임베딩 + LLM chat 모델 결합 → CELLxGENE Explorer web integration.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: scRNA-seq transcriptome 프로파일과 자연어 텍스트를 동일한 embedding space에 매핑하고, 이 임베딩 기반으로 (a) 텍스트 쿼리에 의한 세포 검색/주석 및 (b) 자연어 chat 응답 생성.
- **입력**: (임베딩 모델) transcriptome count vector (상위 2,048 발현 유전자) + 텍스트 annotation. (Chat 모델) transcriptome 임베딩 + 사용자 질문 텍스트.
- **출력**: (임베딩 모델) 2,048차원 joint multimodal embedding vector. (Chat 모델) 자연어 응답 텍스트.
- **추정 대상**: transcriptome과 텍스트 annotation의 의미적 유사도 (cross-modal alignment).
- **중요한 hidden assumption**: 충분히 큰 규모의 transcriptome-텍스트 pair를 curate하면, 임베딩 모델이 cell type·조직·질환·발달 단계 등 생물학적 개념을 transcriptome에서 implicit하게 학습할 수 있다는 가정.

#### 확률 / 통계학적 구조

- **Model family**: Multimodal contrastive learning (CLIP 기반). 두 modality-specific encoder + adapter layer 구조.
  - Transcriptome encoder: Geneformer (frozen). 상위 2,048 발현 유전자 tokenization → 512차원 출력 → adapter (512→2048, BatchNorm+ReLU) → 2,048차원 normalized 벡터.
  - Text encoder: BioBERT (unfrozen). WordPiece tokenization, 최대 128 tokens → 768차원 → adapter (768→2048→2048, BatchNorm+ReLU) → 2,048차원 normalized 벡터.
- **Objective (Embedding model)**: InfoNCE loss. Batch 내 matched (transcriptome, text) pair의 cosine similarity를 최대화하고 unmatched pair를 최소화. Batch size 512, 최대 learning rate 0.00001. 16 epochs 훈련, A100 GPU 8개 사용, 훈련 시간 < 24시간.
- **Training data**: GEO (722,425개 ARCHS4 human transcriptome → 7,049개 제거 후 705,430개) + CELLxGENE Census (257개 study, 19,663,838 scRNA-seq profiles → pseudo-bulk 376,983개). 최종 학습 쌍 1,082,413개.
- **LLM-assisted curation**: 각 transcriptome에 Mixtral 8x7b (Q5_K_M quantized, llama.cpp)를 사용하여 GEO metadata → 생물학적으로 informative한 자연어 설명 생성. Sampling temperature 0.2, nucleus sampling top_p 0.9, top_k 50.
- **Chat model architecture**: LLaVA 방식. 2-layer adapter (2048→8×4096, GELU) → 8개 token → concatenate with text tokens → Mistral 7B LLM 입력. 1st epoch: LLM frozen, adapter만 학습 (1,082,413개 simple QA). 2nd epoch: LLM + adapter 동시 fine-tuning (106,610개 conversation). 4×A100 80GB GPU, 총 3시간.
- **Chat model 학습 데이터**: 4종 — Simple (10,000개, GPT-4 zero-shot), Detailed (10,000개, GPT-4 few-shot), Complex (5,000개, GPT-4 pre-action reasoning), Conversational (81,610개, Mixtral 8x7b few-shot). 총 106,610개.

#### 핵심 method insight

- **기존 방법의 한계**: 기존 scFM들은 transcriptome 단독 처리. LLM chat 접근은 transcriptome을 직접 입력으로 처리하지 않거나 세포마다 LLM을 실행하는 계산 비용 문제.
- **이 논문이 바꾼 가정**: transcriptome과 텍스트를 분리된 modality로 독립 처리하는 대신, CLIP 방식으로 joint embedding space를 구성하여 cross-modal retrieval 및 semantic similarity 산출이 가능하게 한다.
- **새로 추가한 변수 또는 구조**: (1) LLM-assisted 자동 큐레이션으로 GEO+CELLxGENE Census의 raw metadata를 생물학적으로 informative한 자연어 설명으로 변환. (2) Pseudo-bulk aggregation으로 scRNA-seq sample 내 세포를 metadata group별로 평균 → 텍스트와 1:1 pair 구성. (3) Chat 모델에서 transcriptome 임베딩을 8개 token으로 변환해 Mistral 7B에 주입 (LLaVA 방식).
- **이 변화가 중요한 이유**: transcriptome 임베딩이 chat context에 포함됨으로써 텍스트 only LLM 대비 transcriptome-aware 응답 생성이 가능해진다 (perplexity 실험으로 검증).

#### 이전 방법과의 차이

- **Baseline**: Geneformer fine-tuned (3 configurations), scGPT fine-tuned (3 configurations), UCE fine-tuned (3 configurations), CellAssign (marker-based).
- **공통점**: Geneformer를 transcriptome encoder backbone으로 사용.
- **차이점**: CellWhisperer는 fine-tuning 없이 zero-shot으로 동작. 기존 scFM들은 cell type prediction을 위해 task-specific fine-tuning 필요. CellAssign은 marker gene 목록 참조 필요.
- **차이가 크게 나타나는 조건**: training data에 없는 cell type/dataset에 대한 zero-shot 상황. ImmGen, Asian Immune Diversity Atlas에서 AUROC > 0.99 달성.

#### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: Tabula Sapiens (20 types, 184,450 cells), Pancreas (16,382 cells), ImmGen (42 types), Asian Immune Diversity Atlas (9 types, 7,842 cells), Human Diseases (229 subtypes), Human Development (95,092 profiles).
- **Metric**: AUROC, Accuracy (macro-averaged), F1 score, Perplexity, Recall@5.
- **개선된 결과**: zero-shot 조건에서 Tabula Sapiens AUROC 0.94 — fine-tuned scFM 최고 (0.99)에는 못 미치나 CellAssign (0.52) 대비 크게 상회.
- **Ablation 근거 (Extended Data Fig. 1c)**: InfoNCE loss + batch size 512 + density 기반 sample weighting + annotation augmentation 조합이 최적. JSD loss, GEO only data, scGPT backbone 변형은 성능 저하.
- **Chat model 근거**: Evaluation Conversations 90% preference (matched vs. 30종 mismatched transcriptome 배경 대비). Cell Type Conversations에서 177개 cell type 대다수가 matched transcriptome 선호.

#### Method 관점의 한계

- **약한 assumption**: LLM이 생성한 텍스트 주석의 품질에 의존. metadata가 빈약한 GEO sample은 생물학적 정보량이 낮을 수 있다.
- **구현 또는 학습상의 부담**: Chat model fine-tuning에 4×A100 80GB 필요. 임베딩 학습에 5,000 A100 GPU hours 추정. 임베딩 추론은 GPU 없이도 가능하나 속도 저하.
- **일반화가 불확실한 조건**: 공개 데이터베이스에 잘 표현되지 않은 cell type/조직은 성능 보장 불가. CLIP 기반 모델 특성상 prompt 표현 방식에 민감 (Extended Data Fig. 2f).

---

## Results

#### Dataset별 결과

##### Dataset 1 — Tabula Sapiens (20 common cell types)
- **Dataset**: 인간 다장기 scRNA-seq, 24개 조직, 177개 annotated cell type. 평가에는 liver/lung/blood의 20개 common cell type (n=184,450 cells) 사용. CellWhisperer training data에 미포함.
- **목적**: Zero-shot cell type prediction benchmark.
- **Baseline / 비교 대상**: Geneformer fine-tuned (frozen/unfrozen, ±pseudo-bulking, 총 3종), scGPT (동일 3종), UCE (동일 3종), CellAssign.
- **Metric**: Accuracy (macro-averaged), F1 score (macro-averaged), AUROC.
- **주요 수치**: CellWhisperer zero-shot — AUROC = 0.94, Accuracy = 0.61, F1 = 0.61. Fine-tuned Geneformer (with pseudo-bulking, best): Accuracy = 0.79, AUROC = 0.99. CellAssign: Accuracy = 0.37, AUROC = 0.52 (Fig. 2c).
- **정성 결과**: 혼동 오류는 주로 'monocytes' vs 'classical monocytes', CD8+ T cell subtype 등 closely related cell type 간 발생 (Fig. 2b).
- **통계적 유의성**: 미제공 (bar plot with values, CI 미표시).
- **논문 주장과의 연결**: zero-shot으로 fine-tuned scFM들과 comparable한 수준 → cell type prediction 특화 training 없이도 유효한 transcriptome-text alignment를 학습.

##### Dataset 2 — ImmGen + Asian Immune Diversity Atlas
- **Dataset**: ImmGen: bulk RNA-seq, 42 immune cell types, GSE227743. Asian Immune Diversity Atlas: scRNA-seq, 619명, 7개 population, 9 cell types, n=7,842 cells (최대 1,000/type 랜덤 선택).
- **주요 수치**: ImmGen AUROC > 0.99. Asian Immune Diversity Atlas AUROC > 0.99 (Fig. 2c).
- **논문 주장과의 연결**: 면역 세포 데이터에서 강건한 zero-shot 성능 → 모델 일반화 능력 지지.

##### Dataset 3 — Pancreas (scRNA-seq meta-analysis)
- **Dataset**: 16,382 scRNA-seq profiles, 여러 기술 플랫폼 혼합, batch effect 심한 meta-analysis benchmark.
- **주요 수치**: CellWhisperer zero-shot AUROC = 0.89 (Fig. 2c).
- **해석**: closely related cell type과 pronounced batch effect 조건에서도 0.89 달성 → robustness 근거.

##### Dataset 4 — Human Diseases (14,112 bulk RNA-seq samples)
- **Dataset**: GEO에서 수집한 14,112개 disease-annotated transcriptome, 229개 disease subtype. CellWhisperer training data에서 제외. 별도 pipeline(fetchngs + rnaseq) 및 GPT-4 zero-shot prompting으로 annotation 생성.
- **주요 수치**: disease subtype AUROC = 0.82; tissue-of-origin AUROC: Tabula Sapiens 0.75, Human Diseases 0.87 (Fig. 2d).
- **해석**: disease prediction은 cell type prediction보다 어렵지만 random baseline 대비 substantially 높음.

##### Dataset 5 — Gene set prediction (8,812 gene sets)
- **Dataset**: GO Biological Process/Molecular Function/Cellular Component 2023, KEGG 2021 Human + cell type/disease gene sets. Human Diseases dataset에 GSVA enrichment 점수와 CellWhisperer score 상관 분석.
- **주요 수치**: Diseases (OMIM_Expanded): 164/178개 gene set에서 significant positive association (p<0.05). Azimuth 2023: 1,279/1,425 (Extended Data Fig. 2b,c, Supplementary Table 2).
- **해석**: 모델이 gene set 수준의 생물학적 개념을 implicit하게 학습.

##### Dataset 6 — Human Development (embryo scRNA-seq meta-analysis)
- **Dataset**: 6개 독립 dataset (PRJEB30442, E-MTAB-3929, E-MTAB-8060, PRJEB40781, GSE232861, GSE155121). 수정 후 3~38일 human embryo (Carnegie stage 1–23). scANVI로 batch effect 보정 후 통합 → 95,092 scRNA-seq profiles. CellWhisperer training data 미포함.
- **목적**: Temporal dynamics 포착 및 organ marker gene discovery 검증.
- **주요 수치**: 4 developmental stage 쿼리(zygote/blastula/gastrula/organogenesis)에서 CellWhisperer score가 예상 시간 순서와 일치 (Fig. 3a). Heart marker gene overlap: CellWhisperer-identified 136개 공유 / fetal atlas 340개 (odds ratio = 10.2, two-sided Fisher's exact test p = 1.4×10⁻⁵², Fig. 3c). PubMed co-mention: CellWhisperer-identified 유전자가 random 대비 'heart'와 유의하게 더 자주 co-mention (two-sided Mann-Whitney U test p = 4.7×10⁻²⁶, Fig. 3c right). 10개 장기 모두에서 각 장기당 최소 10개 이상 신규 marker 발굴 (Supplementary Table 3).
- **재현성**: 10개 장기 모두에서 일관된 결과 (Extended Data Fig. 3).

##### Dataset 7 — Colonic Epithelium (사용자 제공 데이터 탐색)
- **Dataset**: GSE116222. 6명(3 healthy, 3 inflammatory bowel disease) colonic biopsy. n=11,175 cells.
- **목적**: 사용자 제공 데이터 대상 탐색적 분석 + 기존 bioinformatics workflow 비교.
- **주요 수치**: CellWhisperer 분석 소요 수 분. 기존 workflow: ~400줄 Python + 5개 도구 + ~3시간. stemness score 차이 — 기존 접근 adjusted p = 0.0024 (one-sided t-test, Fig. 5l).
- **정성 결과**: LGR5+ epithelial stem cell 서브클러스터 동정, inflamed에서 stemness 감소 — 두 접근 모두 동일한 결론.

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: CellWhisperer zero-shot AUROC가 여러 dataset에서 일관되게 높음 (0.89–0.99 범위). 특히 면역 세포 dataset에서 최고 성능.
- **가장 중요한 수치**: Tabula Sapiens zero-shot AUROC 0.94; ImmGen/Asian AUROC > 0.99; Human Diseases AUROC 0.82; chat model 90% preference; heart marker odds ratio 10.2 (p = 1.4×10⁻⁵²).
- **baseline 대비 차이**: CellAssign (marker-based) 대비 zero-shot accuracy 0.61 vs 0.37. Fine-tuned scFM 최고 성능(~0.79)에는 미치지 못하지만 zero-shot 조건임.
- **결과 해석 시 주의점**: zero-shot AUROC가 높아도 accuracy가 낮은 경우 (closely related cell type 구분의 어려움). Cell type prediction을 위한 특화 훈련 모델이 아님을 저자 명시.

---

## Figures

#### Figure 1
- **이 Figure가 필요한 이유**: CellWhisperer의 전체 학습 pipeline, 추론 흐름, 실제 응용을 한 번에 조망. 독자가 논문의 핵심 기여를 개념적으로 파악하도록 설계.
- **이 Figure가 뒷받침하는 주장**: CellWhisperer는 대규모 커뮤니티 데이터에서 학습하여 transcriptome과 text를 연결하는 multimodal AI이며, 실제 탐색 도구로 활용 가능하다.

##### 패널별 설명
- **a**: 학습 데이터 생성(GEO/CELLxGENE metadata → LLM 텍스트 주석 + 대화 생성), multimodal embedding 훈련(Geneformer + BioBERT, InfoNCE loss), 추론 응용(free-text cell labeling, chat about cell samples)을 하나의 다이어그램으로 요약.
- **b**: UMAP visualization — 705,430개 GEO-derived 인간 transcriptome의 CellWhisperer embedding. Leiden cluster 생성, CellWhisperer chat로 cluster label 자동 생성. 세포 유형·발달 단계·조직·질환이 embedding space에서 분리됨.
- **c**: GEO transcriptome UMAP 위에 'infection' 검색 쿼리의 CellWhisperer score(색상) 투영 — 면역 반응 관련 세포 클러스터 강조.
- **d**: CellWhisperer가 선택한 transcriptome의 GEO submission 날짜 히스토그램 — sample metadata(CD34+ HSPCs, K562 세포, 활성 면역 리모델링 등)별 시간적 제출 패턴.

##### 본문에서 강조한 비교
- 비교 대상: 'infection' 텍스트 쿼리 vs. 전체 transcriptome embedding.
- 관찰된 차이: CellWhisperer score가 높은 transcriptome이 UMAP 상 면역/감염 반응 관련 클러스터에 집중.
- 이 차이가 의미하는 것: 임베딩 모델이 자연어 개념과 transcriptome feature를 연결함을 시각적으로 입증.

##### 해석 시 주의점
- UMAP은 dimensionality reduction 결과물이므로 클러스터 경계가 절대적이지 않음. CellWhisperer score 투영은 정성적 시각화.

---

#### Figure 2
- **이 Figure가 필요한 이유**: CellWhisperer의 zero-shot cell type/disease/tissue prediction 성능을 정량적으로 benchmark. 핵심 주장인 "fine-tuning 없이도 유용한 cell annotation"을 수치로 뒷받침.
- **이 Figure가 뒷받침하는 주장**: CellWhisperer embedding model이 cell type, tissue, disease 등 다양한 생물학적 특성을 zero-shot으로 인식한다.

##### 패널별 설명
- **a**: Zero-shot evaluation 개요 — expert-annotated 데이터(training 미포함)에 CellWhisperer score 적용 → 정답 label과의 일치 여부 평가 흐름.
- **b**: Tabula Sapiens 20 common cell types의 CellWhisperer 예측 vs. expert annotation UMAP + confusion matrix (heatmap). 혼동은 주로 유사 cell type 간.
- **c**: 5개 dataset에서 Accuracy, F1 score, AUROC를 model별 bar plot. Zero-shot CellWhisperer를 fine-tuned Geneformer/scGPT/UCE 및 CellAssign과 비교.
- **d**: 다른 cell characteristics (organ/tissue/disease subtype)에 대한 zero-shot 예측 성능 — AUROC 및 Accuracy bar plot. Tabula Sapiens, Human Diseases dataset 포함.

##### 본문에서 강조한 비교
- Zero-shot CellWhisperer Accuracy = 0.61 vs. fine-tuned Geneformer best = 0.79 vs. CellAssign = 0.37 (Tabula Sapiens 20 types).
- CellWhisperer가 fine-tuned model에는 못 미치지만 marker-based method를 명확히 상회.

##### 해석 시 주의점
- AUROC가 높아도 Accuracy/F1이 낮은 경우 있음 — closely related cell type이 많은 조건에서 해석 주의. CellWhisperer는 cell type prediction 특화 모델이 아님을 저자 명시.

---

#### Figure 3
- **이 Figure가 필요한 이유**: Human embryo development라는 복잡한 biological application에서 CellWhisperer의 temporal dynamics 포착 및 novel marker gene discovery 능력을 검증. 단순 annotation을 넘어 발견적 사용 가능성 제시.
- **이 Figure가 뒷받침하는 주장**: CellWhisperer embedding이 생물학적으로 해석 가능하며, 텍스트 쿼리만으로 organ development marker gene을 기존 방법 수준으로 발굴할 수 있다.

##### 패널별 설명
- **a**: 6개 embryo dataset × 4개 developmental stage 쿼리 heatmap. CellWhisperer score의 시간적 패턴이 예상 발달 순서(zygote→blastula→gastrula→organogenesis)와 일치.
- **b**: 'Heart' 쿼리 CellWhisperer z-score의 일별 변화 — 발달 초기부터 심장 특이적 score 상승.
- **c**: Heart marker gene overlap Venn diagram + PubMed co-mention violin plot. CellWhisperer identified (n=499) vs. fetal atlas marker (n=499) vs. random (n=499). Fisher's exact test odds ratio = 10.2, p = 1.4×10⁻⁵².
- **d**: Expression enrichment (log₂FC) vs. PubMed co-mention frequency scatter plot. CellWhisperer-identified 유전자 중 높은 enrichment + 낮은 literature support를 보이는 26개 신규 marker gene 후보 (오른쪽 box, Mann-Whitney p = 1.3×10⁻²⁷).
- **e**: Carnegie stage 8 embryo 공간 유전자 발현. CellWhisperer-identified 신규 marker (IOCOS3, LRTM3), established marker (ISL1), 비관련 유전자 (GAPDH, NOTO) 비교.

##### 본문에서 강조한 비교
- CellWhisperer-identified heart marker genes → 기존 fetal atlas marker와 높은 overlap (odds ratio 10.2). PubMed co-mention에서 random gene set 대비 유의하게 'heart'와 co-mention 빈도 높음.
- 10개 장기 모두에서 이 패턴 반복 (Extended Data Fig. 3).

##### 해석 시 주의점
- Co-mention 분석은 gene-organ functional link의 간접 증거. 직접 perturbation 또는 experimental validation은 없음. 신규 marker 후보들의 기능적 역할은 추가 검증 필요.

---

#### Figure 4
- **이 Figure가 필요한 이유**: CELLxGENE Explorer 통합 및 chat 기반 탐색의 실용적 워크플로우를 실제 예시로 보여줌.
- **이 Figure가 뒷받침하는 주장**: CellWhisperer chat가 사용자 선택 세포 집단에 대해 biologically coherent한 자연어 설명을 생성하고 후속 질문에도 일관성 있게 응답한다.

##### 패널별 설명
- **a**: CellWhisperer 웹 도구 screenshot. 'structural cells with immune functions' 쿼리 → UMAP 상 고득점 세포 집단 시각화.
- **b**: 고득점 cluster (fibroblasts) UMAP zoom-in + CellWhisperer-generated cluster label.
- **c**: 선택된 세포에 대한 chat 대화 스크린샷 — decidua fibroblasts 설명, immune function 질문, mechanistic 질문 3회 교환.
- **d**: Chat 응답에서 언급된 유전자 (IFITM3, ISG15, JUN, COL1A1, COL3A1, FOSB)의 UMAP 상 평균 발현.

##### 본문에서 강조한 비교
- Chat 응답이 언급한 유전자의 발현 패턴이 해당 세포 cluster에서 실제로 높음 (Fig. 4d) — plausibility check.
- CellWhisperer가 찾은 fibroblasts는 structural cell + immune function 쿼리에 부합 — endothelial·epithelial·fibroblast·pericyte 등 비혈구 면역 조절 세포.

##### 해석 시 주의점
- Chat 응답은 모델이 학습 데이터 분포에서 계속 추론하는 것. 저자 자신도 "exploratory tool for hypothesis generation"으로 한정, 독립 검증 필요.

---

#### Figure 5
- **이 Figure가 필요한 이유**: 사용자 제공 scRNA-seq 데이터(Colonic Epithelium)에 대한 CellWhisperer 분석과 기존 bioinformatics workflow를 나란히 비교. 두 접근의 실용적 trade-off를 보여줌.
- **이 Figure가 뒷받침하는 주장**: CellWhisperer는 탐색적 초기 분석을 수 분 안에 제공하며, 기존 bioinformatics 접근을 보완하는 역할을 할 수 있다.

##### 패널별 설명
- **a**: CellWhisperer 분석 workflow 다이어그램 — count matrix → 자동 처리 파이프라인 → h5ad → CellWhisperer 웹 도구. 기존 workflow: scVI → scanpy → CellTypist → differential expression → matplotlib.
- **b**: CellWhisperer-generated cluster label UMAP.
- **c**: 'stem cells' 쿼리 CellWhisperer score overlay UMAP.
- **d**: 상위 100개 stem cells에 대한 chat 응답 — LGR5, OLFM4 언급.
- **e**: LGR5 유전자 발현 UMAP.
- **f**: 'stem cells' CellWhisperer score — inflamed vs. noninflamed 히스토그램.
- **g–l**: 기존 bioinformatics workflow 단계별 결과 — scVI 통합 UMAP (h), CellTypist cluster-level annotation (i), cell-level annotation (j), differential expression of stem cells (k), stemness score violin plot (l).

##### 본문에서 강조한 비교
- CellWhisperer 분석 시간: 수 분. 기존 workflow: ~3시간 + 400줄 Python.
- 결론 일치: LGR5+ stem cell 서브클러스터 동정, inflamed에서 stemness 감소. Stemness score (Fig. 5l) adjusted p = 0.0024.
- 기존 workflow가 batch effect 보정·재현성·추적 가능성에서 우수; CellWhisperer가 초기 탐색 속도에서 우수.

##### 해석 시 주의점
- 정량적 일치도 검증 없음. 기존 workflow의 세밀한 제어가 최종 결과에서는 더 reliable.

---

## Tables

본문에 정식 Table 없음.

### Supplementary Table 1
- Cell type prediction 상세 평가 결과 — dataset × method × metric. Extended Data Fig. 2a와 연결.

### Supplementary Table 2
- GSVA enrichment 분석에서 CellWhisperer score와 유의한 상관을 보인 gene set 목록 (p<0.05). Extended Data Fig. 2b,c와 연결.

### Supplementary Table 3
- CellWhisperer가 발굴한 10개 장기의 신규 organ marker gene 목록. Fig. 3d, Extended Data Fig. 3c와 연결. 각 장기당 최소 10개 이상의 기존 atlas에 없던 신규 후보 포함.

---

## Supplementary Information

### Supplementary Note 1 (MOESM1) — CellWhisperer usage examples
- 4개 CellWhisperer 웹 도구 기능: (1) 자연어 쿼리로 세포 검색/주석, (2) 세포 선택 후 chat, (3) cluster label 자동 생성, (4) 유전자 발현 시각화.
- Dataset별 사용 예시 — Tabula Sapiens (structural cells with immune functions, kidney cortex 확인), Colonic Epithelium (stem cell niche, S phase cells), GEO, Human Development.

### Supplementary Note 2 — LLM-assisted curation + chat model 학습 데이터 상세
- GEO/CELLxGENE Census metadata → Mixtral 8x7b 기반 텍스트 주석 생성 prompt 및 예시.
- Chat 학습 데이터 4종(simple/detailed/complex/conversational) 생성 방법 상세.

### Supplementary Note 3 (MOESM2) — Ablation study
- CellWhisperer embedding model 변형 15가지 비교 (Extended Data Fig. 1c 기반). InfoNCE + batch 512 + density weighting + augmentation이 최적.

### Extended Data Figures
- Extended Data Fig. 1: 모델 아키텍처 + training/ablation 상세 (cross-modal retrieval performance, ablation bar plot).
- Extended Data Fig. 2: scFM variant 비교 + gene set GSVA 평가 + prompt robustness 분석.
- Extended Data Fig. 3: 10개 장기 organ marker gene validation (상관 분석, PubMed co-mention, spatial expression).
- Extended Data Figs. 4–9: Chat model perplexity 평가, Colonic Epithelium 추가 분석 (webp 형식, MOESM3 미제공 PDF).

---

## 분석 자체에 대한 메모

- 본 분석은 main PDF (cellwhisperer-2025-nat-biotech.pdf) + Supplementary Note 1 (MOESM1, pages 1-10)를 1차 근거로 사용.
- Extended Data Fig. 4–9는 webp 파일(MOESM)로 제공되어 캡션과 본문 설명으로만 파악; 상세 수치 확인은 원본 webp image 참조 필요.
- Supplementary Table 수치는 xlsx(MOESM3–5)로 제공되나 본 분석에서는 본문 인용 수치만 사용.
- COI: Christoph Bock (대응 저자)이 Myllia Biotechnology·Neurolentech의 공동창업자 — 결과 해석 시 이해상충 고려 필요.
- 학습 데이터 생성에 GPT-4 (OpenAI API) 및 Mixtral 8x7b 사용 — annotation 품질이 OpenAI API 응답에 부분적으로 의존.

---

## Executive Summary

- **무엇**: CellWhisperer는 scRNA-seq 데이터를 자연어 채팅으로 탐색할 수 있는 AI 모델 및 소프트웨어 도구. 100만 개 RNA-seq 프로파일과 AI 큐레이션 텍스트 주석을 대조 학습(contrastive learning)으로 학습해 멀티모달 임베딩을 구축하고, 이를 LLM에 연결해 세포 및 유전자에 대한 자연어 질의응답을 가능하게 함.
- **핵심 발견**: 세포 유형 및 생물학적 주석 예측을 위한 zero-shot 성능을 벤치마킹했으며, 인간 배아 발생 메타분석에서 생물학적 발견에 활용 가능함을 시연. CELLxGENE 브라우저와 채팅 인터페이스 통합.
- **OncoRader 비교**: CellWhisperer는 공개 조직 scRNA-seq 데이터(CZ CellxGene 등 커뮤니티 리포지토리) 기반의 범용 세포 주석 도구. CTC 액체생검 맥락이 없고 ADC 타겟 발굴 기능 부재. OncoRader는 CTC × 액체생검 × ADC 타겟 발굴에 특화된 임상 의사결정 지원 도구로 목적과 입력 데이터가 근본적으로 다름.

---

## Identity

- **Title**: Multimodal learning enables chat-based exploration of single-cell data
- **Authors**: Moritz Schaefer#, Peter Peneder#, Daniel Malzl, Sergi Dabad Lombardo, Mihaela Peycheva, Jonathan Burton, Ani Hakobyan, Vivek Sharma, Thomas Krausgruber, Christoph Sin, Jörg Menche, Eva Maria Tomazou, Christoph Bock (corresponding, cbock@cemm.oeaw.ac.at). (#equal contribution: M.S., P.P. co-first authors)
- **Affiliation**: Medical University of Vienna (Institute of Artificial Intelligence / Comprehensive Center for AI in Medicine), CeMM Research Center for Molecular Medicine (Austrian Academy of Sciences), St. Anna Children's Cancer Research Institute (CCRI), Max Perutz Labs, University of Vienna, Ludwig Boltzmann Institute for Network Medicine. (모두 Vienna, Austria)
- **Venue / Year**: *Nature Biotechnology* (2025, online 2025-11-11). PMID: 41219484.
- **Funding**: 미제공 (abstract 범위 외)
- **COI**: C.B. — Myllia Biotechnology 및 Neurolentech 공동창업자 겸 과학 자문. 나머지 저자 이해충돌 없음.
- **License**: © 2025 The Author(s) — 외부 맥락: Nature Biotechnology 논문은 일반적으로 CC BY 4.0 Open Access 게재 가능.
- **Citation key**: `schaefer2025cellwhisperer`

---

## Background (배경: 왜 AI가 scRNA-seq에 필요한가)

### 문제의 출발점

scRNA-seq는 단일세포 수준의 유전자 발현을 전례 없는 규모와 해상도로 측정하지만, 데이터 해석은 여전히 전문적인 생물정보학 지식을 요구한다. 수백만 개의 세포 프로파일이 공개 리포지토리(CZ CellxGene 등)에 누적되어 있지만, 비전문가 연구자가 이 데이터를 탐색하고 의미 있는 생물학적 질문에 답하기 어렵다.

### 기존 접근의 한계

기존 scRNA-seq 분석 파이프라인은 세포 유형 주석, 클러스터링, 경로 분석 등의 개별 작업에 특화되어 있어 연구 맥락을 통합한 해석이나 가설 생성이 제한적이다. 특히 전사체와 텍스트(문헌 지식) 사이의 다리가 없어, 분석 결과와 기존 생물학적 지식을 자동으로 연결하기 어렵다.

### 이 논문이 해결하려는 방향

100만 개 규모의 RNA-seq 프로파일과 AI 큐레이션 텍스트 주석을 대조 학습으로 연결하는 멀티모달 임베딩을 구축. 이 임베딩을 LLM에 결합해 사용자가 자연어로 세포와 유전자에 대해 질의하고 해석하는 인터랙티브 채팅 기반 탐색을 가능하게 함.

---

## Methods (abstract 범위)

- **핵심 방법론**: 대조 학습(contrastive learning) 기반 멀티모달 임베딩 — RNA-seq 프로파일(전사체)과 텍스트 주석을 동일 임베딩 공간에 정렬.
- **학습 데이터**: 100만 개 RNA-seq 프로파일 + AI 큐레이션 텍스트 설명.
- **하위 아키텍처**: 전사체 인코더 + 텍스트 인코더 → 공동 임베딩 공간 → LLM 연결. 외부 맥락: CLIP 스타일의 대조 학습을 scRNA-seq 도메인에 적용한 구조로 추정.
- **평가**: zero-shot 세포 유형 예측 및 기타 생물학적 주석 예측 벤치마킹.
- **응용 시연**: 인간 배아 발생 메타분석에서 생물학적 발견.
- **통합**: CELLxGENE 브라우저에 채팅 박스 통합 — 그래픽 인터페이스 + 채팅 인터페이스 결합.

---

## Results (abstract 범위)

- **Zero-shot 성능**: 세포 유형 예측 및 기타 생물학적 주석에서 zero-shot 예측 성능 벤치마킹 완료. 구체적 정확도 수치는 abstract 범위 외.
- **생물학적 발견**: 인간 배아 발생 메타분석에서 CellWhisperer 활용 생물학적 발견 시연.
- **CELLxGENE 통합**: 그래픽 + 채팅 통합 인터페이스로 유전자 발현 인터랙티브 탐색 가능.
- 외부 맥락: 대규모 커뮤니티 scRNA-seq 리포지토리(CZ CellxGene 포함)의 데이터를 활용해 전사체-텍스트 연결을 학습.

---

## Analysis Notes (CytoGen/OncoRader 경쟁 분석 맥락)

### 기술 포지셔닝

CellWhisperer는 **전사체-텍스트 대조 학습** 기반의 채팅형 탐색 도구다. 대규모 공개 데이터(100만 개 프로파일)를 통해 일반화된 세포 생물학 지식을 구축하고 LLM에 연결하는 접근법은 기술적으로 정교하다.

### OncoRader와의 차별점

| 항목 | CellWhisperer | OncoRader |
|------|--------------|-----------|
| 입력 데이터 | 조직 scRNA-seq (공개 리포지토리) | CTC × 액체생검 scRNA-seq |
| 임상 맥락 | 없음 (범용 탐색 도구) | ADC 타겟 발굴 + 치료 반응 예측 |
| CTC 특화 | 없음 | CTC subtype 분류 + CTC-specific 마커 |
| ADC tier 분류 | 없음 | Tier1~Tier3 + FDA status 2-axis |
| 출력 형태 | 자연어 답변 + 시각화 | ADC 타겟 후보 리스트 + 임상 해석 |

### 경쟁 위험도 평가

낮음. CellWhisperer는 연구자 탐색 및 주석 보조 도구로, OncoRader의 제약사 대상 ADC 타겟 발굴 서비스와 직접 경쟁하지 않음. 내부 보조 도구로의 활용 가능성(세포 유형 주석 보조)은 있으나, CTC/ADC 도메인 지식이 없어 OncoRader 핵심 기능을 대체할 수 없음.

### BD 활용

"CellWhisperer는 일반 조직 scRNA-seq 탐색 도구로, CTC 액체생검 데이터나 ADC 타겟 발굴 맥락이 전혀 없습니다. OncoRader는 이 공백을 정확히 채우는, CTC × ADC 타겟 발굴에 특화된 유일한 도구입니다."
