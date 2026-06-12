# Lens — Industry

근거: `ma-2020-shareseq_core.md`, `sources/abstract.txt`(Declaration of Interests 포함), `paper-info.yaml`. 원문 PDF·supplementary는 sources에 없으므로 core.md(이미 source-grounded)와 abstract를 1차 근거로 삼는다. 산업적 판단은 `해석:` / `추정:` / `질문:` / `검토필요:` / `미제공:`으로 분리했다. 학술적 한계·후속 논문 아이디어·citation 후보는 `ma-2020-shareseq_lens-academic.md` 담당.

## 1. Categorization

> paper-info.yaml의 categorization 블록과 동기화. 현재 yaml 값과 일치하므로 변경하지 않았다.

### Domain (자동 추출, 검토 표시)

- single-cell-genomics
- chromatin accessibility (ATAC)
- multi-omics (paired ATAC + RNA)
- experimental-methods (assay development)
- 해석: regulatory-genomics(cis peak-gene / DORC / super-enhancer)도 domain 후보지만, 본 paper의 1차 정체성은 assay + analytical method resource다.

### Use case (vocabulary 6개 중)

- `methodology-reference` — chromatin potential, DORC, cis peak-gene association은 본 프로젝트의 lag 정량화 frame에 직접 차용·변형 대상.
- `pipeline-applicable` — GSE140203 mouse skin paired ATAC/RNA가 본 프로젝트 Dataset 2이고, alignment 코드 3종(저자 V1/V2, Broad re-implementation)이 공개.
- `academic-citation` — lens-academic의 citation 후보가 풍부(인용 문장 4 + 수치 4 + Figure 2).
- 해당 없음: `BD-opportunity`는 약하게만 존재(아래 §3.1), `commercialization-candidate`·`regulatory-precedent`는 본 시점 해당 없음.

### Importance (1개 종합 등급)

- Level: **상**
- Perspective (1문장): 본 프로젝트 Dataset 2(GSE140203 mouse skin SHARE-seq)의 원 출처이자 chromatin potential 개념의 시초로, MultiVelo/MoFlow 등 epigenomic-lag 후속 work의 foundational reference.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- Sample / scale: adult mouse skin 34,774 high-quality paired profiles, 전체 84,426 cells across 4 cell lines + 3 tissues (core.md Dataset 2~3). single-cell scale은 충분하나, *생물학적 replicate 수*와 *동물 개체 수*는 core.md 근거 범위에 명시되지 않는다. 검토필요: STAR Methods에서 animal n, batch 구조 확인.
- Cohort 편향: 핵심 발견(chromatin priming)은 단일 tissue(mouse skin hair follicle) 단일 system에 집중. 해석: regulatory-grade 일반화 주장으로 쓰기엔 tissue 다양성이 부족하다. brain pairing accuracy 36.7% vs skin 74.9%(core.md Dataset 3)는 modality coupling이 tissue마다 다를 수 있다는 직접 신호.
- Replication: cell-line mixing QC는 replicate/추가 cell line에서 similar performance로 보고(core.md Dataset 1)되나, chromatin potential 결과 자체의 독립 lab/cohort 재현은 본문 근거 범위 밖. 해석: assay-level 재현성과 biological-claim 재현성을 분리해야 한다.
- Selection bias: "high-quality paired profiles 34,774"는 filtering 후 수치. QC threshold(예: fragments in peaks 65.5%, RNA UMI cutoff)가 결과를 유리하게 만들지 않았는지는 검토필요. core.md도 cell type annotation·clustering parameter sensitivity는 정밀 검증하지 못했다고 명시(core.md Figure 2 주의점).
- Multiple testing: peak-gene association에 FDR 제시(GM12878 FDR = 0.11)되나, residual 92%·DORC-super-enhancer overlap의 multiple testing 처리와 exact p-value는 crawl text에 없음(core.md Dataset 4~5). 해석: gene 단위 다중검정 통제가 불명확한 수치는 산업 보고에 그대로 쓰지 말 것.

### 2.2 임상·기술적 제약

- Tissue/sample 가용성: SHARE-seq는 fixed/permeabilized cell or nuclei에 적용(core.md Methods). 희귀 sample보다는 일반 single-cell input에 적용 가능해 진입 장벽은 낮은 편. 해석: 다만 fixation·split-pool 3-round barcoding은 wet-lab 숙련도에 민감.
- 장비·시약 가용성: 특정 상용 platform(10x 등) 비의존, in-house split-pool 방식이라 reagent cost는 낮지만 표준화·QC 일관성 확보에 hands-on 부담. core.md의 cost 수치(100,000 cells library prep 약 $433 vs sci-CAR >$30,000)는 *library prep 한정*이며 reagent price·sequencing·labor·failure rate 제외(core.md Dataset 2 주의점).
- 계산 자원: chromatin potential은 kNN matching($k=10$) + low-dimensional embedding 기반으로, GPU 필수 신호는 core.md에 없음. 추정: CPU + 충분한 RAM으로 재현 가능한 수준. (후속 MultiVeloVAE류 generative model과 달리 본 paper 자체는 deep model 아님.)
- Turnaround: assay + sequencing + 분석 파이프라인 합산 수일~수주 추정. 해석: discovery/research 용도이며 임상 의사결정 turnaround와는 무관한 카테고리.

### 2.3 규제·QA·RA 관점

- FDA/EMA pathway: 해당 없음 — 본 자료는 academic discovery resource다. IVD/LDT/SaMD/drug 어느 pathway에도 직접 매핑되지 않는다.
- Analytical / Clinical validation: 미제공 — assay validation은 internal QC(species mixing collision 0.04%, library size estimate; core.md Dataset 1) 수준이고, LOD·정밀도·sensitivity/specificity 같은 regulatory analytical validation은 대상 아님.
- GMP / GLP: 해당 없음 — research-grade protocol.
- IRB / consent: 인간 primary sample 사용 아님(GM12878 cell line + mouse tissue). 해석: 인간 cell line 사용이라 IRB 이슈는 낮으나, 본 method를 human primary sample로 확장 시 별도 consent/IRB 필요.
- Reproducibility for audit: 코드 3종 + GEO accession 공개로 academic 재현성은 양호하나, FDA audit 수준(version-locked, validated pipeline)은 아님.

### 2.4 권위·신뢰 가중치

- 1차 출처: peer-reviewed Cell 2020 (183(4):1103-1116.e20), PMID 33098772, PMCID PMC7669735. 권위 가중치 높음.
- 저자/기관: Broad Institute + Harvard (Buenrostro, Regev 그룹). single-cell chromatin 분야 핵심 그룹.
- COI (이해상충, abstract.txt Declaration of Interests 근거):
  - A.R.은 Celsius Therapeutics 창업자·equity holder, Immunitas Therapeutics equity holder, 2020-08-31까지 Syros/Neogene/Asimov/ThermoFisher SAB, 2020-08-01부터 Genentech 직원.
  - J.D.B.는 ATAC-seq 관련 특허 보유, Camp4·seqWell SAB.
  - **J.D.B., A.R., S.M.이 본 연구 기반 provisional patent application 제출.**
  - 해석: assay·method에 IP가 걸려 있다는 신호. 자체 제품화·라이선싱 검토 시 freedom-to-operate를 먼저 확인해야 한다(아래 §3).
- Funding: 미제공 — core.md/abstract 근거 범위에 funding source 명시 없음. 검토필요.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- 자산화 신호: SHARE-seq assay와 chromatin potential method에 provisional patent(J.D.B./A.R./S.M.)가 걸려 있음(§2.4). 해석: assay IP는 라이선싱 대상이 될 수 있으나, 이후 상용 paired multiome 시장은 10x Genomics Multiome 등으로 빠르게 표준화되어 SHARE-seq 자체의 라이선싱 매력은 제한적. 추정: 본 프로젝트 입장에서 가져올 *자산*은 assay IP가 아니라 *공개된 분석 method + 데이터*다.
- 공동연구 후보: open code(저자 V1/V2 + Broad epi-SHARE-seq-pipeline) + GEO 공개로 협업 진입 장벽은 낮음. 해석: 라이선싱보다 method 차용·재현이 현실적 경로.
- 경쟁사/생태계 관찰: core.md가 sci-CAR, SNARE-seq, Paired-seq를 비교 대상으로 명시(core.md Figure 1). 이후 본 프로젝트가 쓰는 후속 도구(MultiVelo, MultiVeloVAE, MoFlow)가 모두 GSE140203을 benchmark로 재사용(paper-info.yaml related). 해석: 이 데이터셋은 사실상 epigenomic-lag 분야의 공통 평가 자산이 되었다.
- 시장 영향: paired single-cell multiome 개념을 대중화한 landmark. 직접적 BD 거래 대상이라기보다, 분야 표준 reference로서의 영향.

### 3.2 Commercialization-candidate (자체 제품화)

- 제품 카테고리: 해당 없음 — 본 시점 직접 제품화(Dx/assay/SW/therapeutic) 후보 아님.
  - Assay: SHARE-seq 자체는 IP·후속 상용 platform 경쟁으로 자체 제품화 매력 낮음.
  - SW: chromatin potential/DORC 분석을 SW로 패키징할 여지는 있으나, MultiVelo 등 후속 open-source가 이미 더 발전된 형태로 존재.
- TRL: assay는 lab-validated(4~6), 분석 method는 proof-of-concept~lab-validation. production-grade 제품과는 거리.
- IP 자유도: 검토필요 — provisional patent 범위 확인 전에는 SHARE-seq assay 재현·상용화 freedom-to-operate 단정 불가. 단 *분석 method*(DORC, chromatin potential)를 open 데이터에 적용하는 연구 용도는 통상 제약이 낮다.

### 3.3 우리 파이프라인과의 fit

- Dataset 호환: 높음. GSE140203 mouse skin SHARE-seq가 본 프로젝트 Dataset 2이며, 본인 담당 Human HSPC 10x Multiome(GSE209878)과 같은 "paired ATAC+RNA" modality 구조. 해석: cross-species지만 분석 frame(peak-gene association → DORC → lag)은 그대로 이식 가능.
- 자원 가능성: 분석 재현은 본 팀 역량으로 가능(GPU 불요 추정). assay 자체 재현은 wet-lab split-pool 숙련 필요하나, 본 프로젝트는 *공개 데이터 분석*이 목적이라 무관.
- 전략 align: 본 프로젝트 목표(chromatin-transcription lag → epigenetic drug response timing 예측)의 개념적 출발점. 단 chromatin potential은 activation 방향(열림→발현)만 다루고 shutdown lag는 미포함(lens-academic §정리되지 않은 질문). 빠진 capability: wall-clock 시간 환산, burst kinetics·cell cycle confound 통제 — 본 프로젝트가 추가해야 할 작업.

### 3.4 후속 BD·제품 액션 후보

- 데이터셋 표준 reference로 내부 등록
  - 누가: 본인(데이터 담당)
  - 언제: 지금
  - 자원: build_index 갱신 + Confluence 링크
  - 성공 기준: GSE140203가 epigenomic-lag benchmark로 팀 내 단일 참조점으로 정리됨.
- SHARE-seq IP / freedom-to-operate 사전 확인
  - 누가: 본인(technical) + 법무/IP 담당
  - 언제: 자체 assay·SW 제품화를 *실제로 검토할 때만* (현재는 보류)
  - 자원: provisional patent 조회 1회
  - 성공 기준: assay 재현·상용화 시 IP 충돌 여부 명확화. (현 시점 우선순위 낮음.)

## 4. 전문가 코멘트

### 4.1 종합 등급

- Level: **상**
- Perspective: 본 프로젝트 Dataset 2의 원 출처이자 chromatin potential의 시초로, 후속 epigenomic-lag 도구들이 공통으로 재사용하는 foundational reference.
- 등급 근거:
  - GSE140203 mouse skin SHARE-seq가 본 프로젝트 Dataset 2이고, MultiVelo(li-2023-multivelo)·MultiVeloVAE(li-2025-multivelovae)가 같은 데이터를 재사용(paper-info.yaml related). 분야 공통 benchmark의 원점.
  - chromatin potential/DORC/cis peak-gene association이 본 프로젝트 lag 정량화 frame의 직접 차용 대상(methodology-reference).
  - 코드 3종 + GEO 공개로 재현·이식 가능(pipeline-applicable).
  - lens-academic citation 후보가 풍부 — 본인 introduction/methods의 foundational citation(academic-citation).
  - 단 상업적 BD/제품화 가치는 낮음(§3). 등급 "상"은 *연구·파이프라인 가치* 기준이지 BD 기준이 아니다.

### 4.2 활용 우선순위

- 지금: GSE140203 분석 frame 차용 검토, 데이터셋 내부 표준 등록.
- 다음 분기: confound-통제 lag 추출 파이프라인을 본 데이터에 시범 적용(lens-academic §우선순위 1~2와 연계).
- 장기: SHARE-seq IP 확인은 자체 제품화 논의가 실제로 떠오를 때만.

### 4.3 발표·미팅에서 들이밀 시점

- 본인 논문/제안서 introduction: chromatin priming / chromatin-transcription lag의 foundational citation.
- 사내 R&D 리뷰: 본 프로젝트 Dataset 2의 출처·신뢰도 설명, 후속 도구 benchmark 계보 정리.
- BD 미팅: 해당 약함 — 직접 라이선싱 대상이 아니므로 우선순위 낮음.

### 4.4 추가 탐색 필요 영역

- 질문: SHARE-seq provisional patent의 청구 범위는? 자체 assay·SW 제품화를 검토하게 되면 freedom-to-operate를 먼저 확인해야 한다.
- 질문: GSE140203 raw/intermediate를 본 프로젝트 저장소 기준으로 어디까지 보관할지(200~500GB/dataset 기준)? 데이터 관리 정책과 연결.
- 질문: 본 데이터에서 cell cycle·burst kinetics를 covariate로 통제한 뒤에도 chromatin-leads-RNA가 남는 gene set은 무엇인가? — 본 프로젝트 feature 후보 정의의 입력(lens-academic과 공유 질문).
- 검토필요: funding source가 core.md/abstract 근거 범위에 없음. 필요 시 원문 STAR Methods/Acknowledgments 확인.
