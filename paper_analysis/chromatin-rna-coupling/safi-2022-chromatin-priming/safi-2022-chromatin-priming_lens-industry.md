# Lens — Industry — Safi et al., 2022 (chromatin priming)

> 근거: `safi-2022-chromatin-priming_core.md` + `sources/safi-2022-chromatin-priming.pdf`.
> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.

## 1. Categorization

### Domain (자동 추출, 검토 표시)
- `hematopoiesis` (HSPC lineage commitment)
- `single-cell-genomics` (scATAC-seq, scRNA-seq, sc-qPCR)
- `epigenomics` (chromatin accessibility, TFBS motif, enhancer)
- `chromatin-rna-coupling` (chromatin priming이 transcription에 선행 — primary topic)

### Use case
- `academic-citation` — 우리 activation lag 가설의 *정성적 선행성*을 같은 HSPC system에서 뒷받침. lens-academic의 citation 후보 풍부. (1차)
- `methodology-reference` — pseudotime을 따라 motif accessibility change-point(`ruptures`)로 transition zone을 검출하는 절차가 우리 lag-detection 절차의 prototype 후보. (2차)

### Importance
- Level: 중
- Perspective (1문장): 우리 가설의 *방향성*을 같은 cell type에서 지지하는 강한 academic citation이지만, paired multiome이 아니고 transition 축이 pseudotime이라 gene-level lag 정량의 *직접* pipeline/제품화 근거는 아니다.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크
- **Sample size**: scATAC-seq 총 2,680 cells, 집단당 181–509 cells(LT-HSC 509, ST-HSC 230, MPP2 181, pre-MegE 495). scRNA-seq CD9high 523 cells. single-cell genomics 기준 small~moderate. 희귀 transition 집단(`CD9high`)은 더 적어 통계력 제한.
- **Cohort 편향**: mouse(C57BL/6) 단일 종, BM 단일 조직. human 일반화 미검증.
- **Replication**: 동일 결론을 scATAC-seq·scRNA-seq·sc-qPCR·in vitro·in vivo 다중 modality로 교차 지지 — 내부 replication은 양호. 단 *독립 lab/외부 cohort* replication은 본문에 없음.
- **Selection bias**: mitochondrial contamination·doublet filter, peak QC(top 5% invariant bin 제거 등) 적용. 합리적. `검토필요:` change-point 분석에 mean ratio ≥0.025 motif만 사용한 filtering이 transition zone 위치에 미치는 영향.
- **Multiple testing**: enhancer motif enrichment에 Benjamini-Hochberg(FDR 5%), scRNA cluster enrichment에 Poisson model(α=10⁻⁵), enhancer-gene pairing에 bootstrap 1,000 iteration(<0.01). multiple testing 통제 적절.

### 2.2 임상·기술적 제약
- **Tissue/sample 가용성**: mouse BM에서 다단계 FACS sort(8 집단, purity >94%). 희귀 transition 집단 분리에 고난도 sort panel 필요 — 외부 재현 진입장벽.
- **장비·시약**: 10x Chromium scATAC v1.1 / 3' GEX v2, NovaSeq, Fluidigm BioMark 96.96, FACS-Aria/Fortessa. 표준 core-facility 장비이나 small lab엔 부담.
- **계산 자원**: GPU 명시 없음. cellranger-atac, Seurat, Slingshot, FIMO, ruptures, SnapATAC — 일반 CPU server로 가능 수준. `추정:` GPU 불필요(method paper 아님).
- **Turnaround**: sort→sequencing→multi-step bioinformatics. 연구용 timeline, 임상 의사결정 부적합.

### 2.3 규제·QA·RA 관점
- **FDA/EMA pathway**: 해당 없음 — basic discovery science(mouse, mechanism). Dx/therapeutic claim 없음.
- **Analytical/Clinical validation**: 없음(기초 연구). 임상 grade evidence 아님.
- **IRB/consent**: mouse만 사용, Lund University 윤리위원회 승인 명시. human consent 무관.
- **Reproducibility for audit**: code·processed data가 OSF(`https://osf.io/y3faj/`) + GEO에 공개. 단 `검토필요:` accession 불일치(본문 GSE173075/173076 vs Resource Availability GSE148746) — audit·재현 전 GEO에서 유효 accession 확정 필요.

### 2.4 권위·신뢰 가중치
- `1차 출처:` peer-reviewed Cell Reports(Cell Press), open access. 권위 가중치 높음.
- Funding: Swedish Cancer Society, Wallenberg, Swedish Research Council 등 공공/재단. corporate sponsorship 없음.
- COI: 저자 declare no competing interests.
- `검토필요:` 2023 erratum 존재 — 정정된 figure/수치 확인 후 인용.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)
- 저자(Karlsson lab, Lund)는 CD9 marker(Karlsson 2013)·HSPC immunophenotype 전문. `미제공:` startup·라이선싱 신호는 본문에 없음.
- code/data open(OSF/GEO) → 외부 자산으로 라이선싱 협상보다는 *공개 reuse* 성격. BD 라이선싱 대상으로서의 가치 낮음.
- 경쟁사 관찰: `미제공:` 본문 범위 밖.

### 3.2 Commercialization-candidate (자체 제품화)
- **Dx/assay**: `LSKFlt3int CD9high` immunophenotype은 mouse marker 조합으로, 그대로는 진단 제품 아님. human ortholog marker panel이 확립되면 HSPC subset 분리 assay 후보가 될 수 있으나 본 논문 범위 밖.
- **SW**: change-point 기반 transition-zone 검출 워크플로는 self-contained 제품이 아니라 기존 도구(ruptures, Slingshot) 조합. 독립 SW 제품성 낮음.
- **TRL**: 1–3(proof-of-concept, mouse discovery).
- IP 자유도: 공개 도구 조합이라 open implementation 자유로움.

### 3.3 우리 파이프라인과의 fit
- **Dataset 호환**: *개념적 호환*(같은 HSPC lineage priming 주제). 단 mouse scATAC 단독 vs 우리 human 10x Multiome(GSE209878, paired) — modality·species 불일치.
- **자원 가능성**: 우리 팀 역량으로 분석 재현 가능(GPU 불필요, 표준 single-cell stack).
- **전략 align**: epigenetic-therapy response timing 예측의 *생물학적 전제*(chromatin이 먼저 열린다)와 align. 단 직접 feature/model을 가져오는 fit은 아님.
- 빠진 capability: paired multiome same-cell lag 정량은 이 paper에 없음 — 우리가 채워야 할 부분.

### 3.4 후속 BD·제품 액션 후보
- 해당 없음 — 현 시점 BD/제품화 직접 가치 낮음(기초 discovery). academic citation·methodology reference로 활용.

## 4. 전문가 코멘트

### 4.1 종합 등급
- Level: 중
- Perspective: 우리 가설의 방향성을 같은 cell type에서 지지하는 강한 academic citation. gene-level lag 정량의 직접 근거는 아님.
- 등급 근거:
  - `safi-2022-chromatin-priming_core.md` §Results의 핵심 발견(chromatin priming이 commitment·frank expression에 선행)이 우리 activation lag 가설과 *정성적으로 동형* — citation value 높음.
  - 그러나 scATAC 단독(non-paired)이라 *같은 cell* chromatin-RNA 시간차를 못 잡음 → pipeline·제품화 직접 적용 불가.
  - transition 축이 pseudotime(ordering) → wall-clock lag 정량 근거 아님(CLAUDE.md 방법론 주의 1).
  - 데이터·코드 open이나 GEO accession 불일치·erratum 미반영 → 재현 전 확인 필요.
  - mouse·BM 단일 → human HSPC 일반화 미검증.

### 4.2 활용 우선순위
- 다음 분기: 우리 논문/제안서 introduction·discussion의 citation으로. 즉시 pipeline에 넣을 자료는 아님.

### 4.3 발표·미팅에서 들이밀 시점
- 본인 논문 introduction(chromatin 선행성 prior evidence)·사내 R&D 리뷰(우리 paired multiome 작업의 필요성 정당화 — "기존 연구는 non-paired라 lag를 직접 못 쟀다").

### 4.4 추가 탐색 필요 영역
- 질문: GEO에서 GSE173075/173076 vs GSE148746 중 유효 accession 확인. processed scATAC fragment file 접근 가능한가?
- 질문: 2023 erratum이 어느 figure/수치를 정정했는가? 우리가 인용하려는 수치(distal homogeneity 0.434, multi-lineage 30%)가 정정 대상인지.
- 질문: 같은 lab 또는 타 group이 human HSPC paired multiome에서 CD9high 유사 transition state·SPI1/GATA1 crossover를 재현한 후속 paper가 있는가?
