# Lens — Industry — Trevino 2021 (Developing Human Cortex Multi-ome)

> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 근거는 `trevino-2021-cortex_core.md` + 원문 PDF 본문. 권위 가중치: 1차 출처(Cell peer-reviewed Resource).

## 1. Categorization

### Domain (자동 추출, 검토 표시)
- `single-cell-genomics`
- `developmental-neuroscience`
- `chromatin accessibility` / `regulatory-genomics`
- `disease-variant-interpretation` (ASD noncoding *de novo* mutation)
- `deep-learning-genomics` (BPNet 기반 sequence model)

### Use case (vocabulary 6개 중 1~3개)
- `academic-citation` — fetal human cortex multiome reference + sequence-model variant prioritization 사례로 인용 가치 높음.
- `methodology-reference` — CCA peak-gene linking, pseudotime 위 motif-expression wave, fuzzy module, BPNet variant scoring을 우리 분석에 차용 가능.
- `pipeline-applicable` — GSE162170이 후속 multiome velocity benchmark로 재사용되며, 우리 single-cell multiome pipeline의 human cortex validation reference.

### Importance (1개 종합 등급)
- **Level**: 상
- **Perspective**: 본 프로젝트 human brain multiome reference(Dataset 3) 원 논문이며, chromatin-RNA coupling과 noncoding variant interpretation을 한 자료에서 연결해 methodology-reference·citation 가치가 모두 높음.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크
- **Sample size**: primary sample 4개(PCW16/20/21/24), filtering 후 scRNA 57,868 / scATAC 31,304 cell, multiome 8,981 cell. cell 수는 크지만 **donor(sample) 수가 4로 작아** donor-level generalization이 약함. `검토필요:` donor ancestry·sex 분포는 STAR Methods 확인 필요(`미제공:` 로컬에 없음).
- **Cohort 편향**: fetal cortex tissue 자체가 procurement·IRB 부담이 크고 donor 다양성 확보가 어렵다. ASD variant 분석은 단일 cohort(Simons Simplex Collection, 1,902 family) 기반 — 독립 cohort 재현 없음.
- **Replication**: 내부 교차검증은 강함(singleome↔multiome $r=0.62$; 독립 scRNA dataset Bhaduri 2020/Polioudakis 2019 projection 일치). 그러나 disease variant enrichment의 외부 cohort 재현은 없음.
- **Effect size / multiple testing**: ASD enrichment effect size가 작음(early RG OR=1.909, GluN cluster >1.2-fold). prioritized mutation 수도 작음(case 262/control 232). `검토필요:` permutation FDR·null model 세부는 STAR Methods 확인(CLAUDE.md §방법론 주의 5).
- **Selection bias**: BPNet은 cell type에 peak이 있는 variant만 평가 가능 → variant 평가 대상이 chromatin landscape에 의해 선택됨(저자도 명시).

### 2.2 임상·기술적 제약
- research-grade developmental atlas + disease variant interpretation framework. 임상 진단 assay 아님.
- fetal cortex tissue 의존 → 외부 재현이 어려운 sample. ASD variant scoring은 hypothesis generation 단계.
- 10x Multiome + cluster별 BPNet 재학습은 **GPU 필수**, 분석 역량 요구 높음 → small lab/clinical setting 즉시 적용 부적합.

### 2.3 규제·QA·RA 관점
- **Regulatory pathway**: 현재 discovery/research evidence. IVD/LDT/SaMD 근거 아님.
- **Analytical validation**: `미제공:` assay precision/LOD/inter-lab reproducibility는 본문 범위 밖.
- **Clinical validation**: ASD variant prioritization은 sensitivity/specificity/PPV/NPV 같은 clinical performance metric 없음 → regulatory-precedent로 쓰기 부족.
- **IRB/consent**: human fetal tissue + ASD genome cohort 사용. `검토필요:` ethics statement·consent는 STAR Methods "Human tissue and institutional approval" 확인 필요.

### 2.4 권위·신뢰 가중치
- 1차 출처: Cell peer-reviewed Resource(2021), GEO GSE162170, GitHub repo(brain_comp, Brain_ASD).
- Peer-review 가중치 높음. funding은 공공·재단(Rita Allen, CZ Biohub/Initiative, NSF 등) 중심.
- **COI(본문 Declaration of Interests)**: W.J.G.는 10x Genomics consultant 및 ATAC-seq 특허 inventor; H.Y.C.는 Accent Therapeutics·Boundless Bio 공동창업자, 10x Genomics 등 advisor; A.S.는 Insitro 직원; K.F.는 Illumina 직원. → 10x platform·ATAC method에 상업적 이해관계 존재. 결과 자체 검증 시 platform 편향 가능성 인지.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)
- Stanford(Greenleaf/Kundaje/Pașca) collaboration — regulatory genomics + neurodevelopment 양쪽 협업 가치. 직접 라이선싱 자산보다 atlas/code/data reuse·공동연구 reference로 보는 게 현실적.
- BPNet variant-effect framework는 이미 공개 method(Avsec 2020) — 독점 자산 아님. 본 논문의 자산은 *cortex cluster별 학습 model + atlas*.

### 3.2 Commercialization-candidate (자체 제품화)
- **Dx**: ASD diagnostic 직접 제품화는 evidence gap 큼(effect size 작음, 단일 cohort, 분자 검증 없음). research-use-only 해석 지원 component 정도.
- **Software**: cell-type-specific noncoding variant interpretation pipeline의 module로 흡수 가능(우리 자체 구현 IP 자유도 있음 — BPNet open).
- **Assay/service**: 10x Multiome + cluster별 regulatory-effect scoring service 가능. 단 fetal brain reference 적용 범위를 organ/disease model별로 제한해야.
- **TRL**: 4~6(lab validation). production-ready 아님.

### 3.3 우리 파이프라인과의 fit
- human cortex multiome benchmark + CRE-gene linking use case가 우리 epigenomic-lag / single-cell multiome 분석과 직접 맞음.
- HSPC multiome으로 biological conclusion을 옮길 수는 없으나 **분석 패턴(CCA linking, pseudotime motif wave, BPNet scoring)은 차용 가능**.
- `해석:` GSE162170은 raw discovery source보다 benchmark/reference annotation source로 두는 게 ROI 높음.

### 3.4 후속 BD·제품 액션 후보
- **GSE162170 multiome subset 재현 가능성 점검**
  - 누가: bioinformatics 담당
  - 언제: 다음 sprint
  - 자원: GEO download, ArchR/Signac/scanpy pipeline
  - 성공 기준: 후속 velocity paper가 쓴 multiome(PCW21, 8,981 cell) subset과 원 논문 cell annotation mapping 확인
- **CRE-gene linking + BPNet scoring PoC(우리 lineage)**
  - 누가: computational genomics 담당
  - 언제: 다음 분기
  - 자원: cluster별 peak-gene map + GPU(BPNet 재학습)
  - 성공 기준: 관심 lineage에서 cell-type-specific variant prioritization report 1건
- **저자 method/atlas 협업 탐색**
  - 누가: BD lead + technical contact
  - 언제: 장기
  - 자원: 미팅 1회
  - 성공 기준: data/code reuse 또는 공동연구 의향 확인

## 4. 전문가 코멘트

### 4.1 종합 등급
- **Level**: 상
- **Perspective**: 본 프로젝트 human brain multiome reference 원 논문 + chromatin-RNA coupling·noncoding variant interpretation 결합으로 methodology-reference·citation 가치 모두 높음.
- 등급 근거:
  - GSE162170이 후속 multiome velocity 논문(MultiVelo, MultiVeloVAE)에서 fetal human cortex benchmark로 반복 재사용 — 우리 Dataset 3 원 출처.
  - CCA peak-gene linking·pseudotime motif wave·BPNet variant scoring 등 차용 가능한 분석 패턴이 명확하고 수치로 뒷받침됨(64,878 link, $r=0.62$, OR=1.909).
  - 코드(GreenleafLab)·GEO 공개로 재현 출발점 존재.
  - 단 donor 4명·단일 ASD cohort·effect size 작음 → disease 결론은 reference로만, 우리 결론에 직접 전이 금지.

### 4.2 활용 우선순위
- **지금**: original dataset citation + source provenance 정리(완료).
- **다음 분기**: GSE162170 subset 재현·annotation mapping, CRE-gene linking 패턴 차용.
- **장기**: cell-type-specific variant prioritization module 확장.

### 4.3 발표·미팅에서 들이밀 시점
- 본인 논문/발표 introduction에서 "chromatin accessibility와 expression을 결합한 fetal human cortex regulatory atlas + sequence-model variant interpretation" 사례로 인용.
- R&D 리뷰에서 human fetal cortex benchmark(GSE162170) 원 출처로 짧게 언급.

### 4.4 추가 탐색 필요 영역
- 질문: GSE162170에서 multiome subset과 singleome을 파일 단위로 어떻게 구분해 받는가? 후속 velocity 논문은 multiome을 쓴다.
- 질문: brain_comp repo가 Figure 전체를 재현하는가, 일부 processing/comparison만 포함하는가? Brain_ASD repo의 BPNet 학습 코드 재현 비용은?
- 질문: cluster별 BPNet 재학습에 필요한 GPU·runtime을 우리 환경(GPU 1대)에서 감당 가능한가?
