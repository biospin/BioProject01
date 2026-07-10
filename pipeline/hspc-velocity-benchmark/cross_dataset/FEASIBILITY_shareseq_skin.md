# Phase 0 Feasibility — BIOP01-41 SHARE-seq mouse skin (GSE140203, Ma et al. 2020 Cell)

> Literature-scout deliverable. cross-dataset 재현 5번째 후보 데이터셋의 착수 타당성 조사.
> 조사일 2026-07-10. 웹 조사 + 로컬 코드 읽기만 수행(데이터 다운로드·파이프라인 실행·commit 없음).
> 근거 URL은 각 절 말미와 문서 끝 Sources에. **검증 못 한 것은 "미확인"으로 표기**.
>
> **독립 확인 (지용기, 2026-07-10)**: GEO `filelist.txt`를 직접 조회해 블로커 1·3의 사실관계를 재확인함.
> supplementary에 **BAM·fastq는 0건**이고 skin RNA는 `GSM4156608_skin.late.anagen.rna.counts.txt.gz`(UMI count, 37MB)뿐이며,
> ATAC는 `GSM4156597_skin.late.anagen.atac.fragments.bed.gz`(5.0GB) 형태다. cell-type 라벨
> `GSM4156597_skin_celltype.txt.gz`(263KB)는 **실재**한다. → 아래 판정의 전제가 성립한다.

---

## 3줄 요약 + 종합 판정

1. **spliced/unspliced가 유일한 실질 블로커다.** GSE140203은 **processed UMI count matrix만** 배포하고 BAM·fastq·spliced/unspliced를 **일절 배포하지 않는다**. 공개된 velocity-ready SHARE-seq skin AnnData/loom도 **못 찾았다**(MultiVelo·MultiVeloVAE는 각각 E18 brain·HSPC/EB/macrophage만 배포). 따라서 reads로부터 재정렬(STARsolo Velocyto)이 필수인데, **SRA의 index read(=cell barcode)가 손상돼 있다는 커뮤니티 보고**가 있어 barcode 복원 자체에 리스크가 있다.
2. **블로커 2·3은 사실상 해결됨.** mouse→human ortholog는 E18에서 이미 쓴 **uppercase 매핑(`.index.str.upper()`)을 verbatim 재사용** 가능하고, skin lineage annotation은 GEO가 **cell-type 파일(`GSM4156597_skin_celltype.txt.gz`)을 직접 배포**하므로 E18처럼 provider annotation을 그대로 쓰면 된다(concordance는 전역 per-gene fit rank라 lineage 비-load-bearing).
3. 따라서 이 티켓의 GO/NO-GO는 **전적으로 블로커 1(spliced/unspliced 확보) 성패에 달렸다.**

### 종합 판정: **CONDITIONAL-GO**
- **조건**: 본 heavy-run에 착수하기 전에 **small preflight spike**(skin RNA fastq 1개 lane에 STARsolo `--soloFeatures Velocyto`를 돌려 barcode 매칭률·spliced/unspliced nnz가 정상인지 확인, 또는 MultiVelo/mmVelo 저자에게 처리된 skin loom 공유 요청)를 **먼저** 통과할 것.
- preflight가 **성공하면 GO**(macrophage 전례대로 kkkim heavy-run → 지용기 CPU downstream).
- preflight가 **실패하면**(SRA barcode 복원 불가 + 저자 자료 확보 실패) **NO-GO/DEFER 유지** → 아래 "대안" 절.
- ⚠️ **지금 상태로 full heavy-run 착수는 권하지 않는다** — spliced/unspliced 확보가 검증되지 않은 채 fastq 다운로드·정렬(수십~수백 GB, mouse STAR index ~30GB)에 자원을 쏟는 것은 도박이다.

---

## 블로커 1 — spliced/unspliced 확보 경로 · **판정: CONDITIONAL-GO (게이팅 블로커)**

### 조사한 것
GSE140203이 실제로 배포하는 것, SHARE-seq barcode 구조, velocyto/STARsolo/kallisto 적용 가능성, 그리고 **누군가 이미 velocity-ready 형태를 공개했는지**.

### 찾은 것

**(a) GEO GSE140203이 배포하는 것 — count matrix만, BAM/fastq/spliced-unspliced 없음.**
GEO supplement 디렉터리(`ftp.ncbi.nlm.nih.gov/geo/series/GSE140nnn/GSE140203/suppl/`)에는 **`GSE140203_RAW.tar`(7.4 GB) + `filelist.txt`** 딱 둘뿐. filelist 기준 skin 관련 파일:
- `GSM4156608_skin.late.anagen.rna.counts.txt.gz` — **RNA UMI count matrix (gene×cell). spliced/unspliced 아님.**
- `GSM4156597_skin.late.anagen.atac.fragments.bed.gz` — ATAC fragments
- `GSM4156597_skin.late.anagen.atac.counts.txt.gz` — ATAC peak counts
- `GSM4156597_skin.late.anagen.atac.peaks.bed.gz` — peak 좌표
- `GSM4156597_skin.late.anagen.barcodes.txt.gz` — barcode
- `GSM4156597_skin_celltype.txt.gz` — **cell-type annotation (블로커 3에서 재사용)**
→ **BAM 없음, fastq 없음, loom/spliced/unspliced 없음.** processed matrix만. (파일 형식: tar/bed/txt/gz만 존재)
※ STATUS.md는 RAW.tar를 7.9GB로 적었는데 GEO ftp 리스팅은 7.4G — 경미한 불일치, 실제 다운로드 시 sha256로 확정할 것.

**(b) SHARE-seq barcode 구조 — 알려져 있으나 10x 경로 무효, STARsolo 커스텀 필요.**
Teichlab `scg_lib_structs` 문서 기준(RNA modality):
- cell barcode = **3 × 8 bp ligation barcode(LB)** = 24 bp (각 라운드 동일한 96-barcode set → 96³ = 884,736 조합), i7 index read(99bp) 안에 linker와 함께 박혀 있음.
- UMI = **10 bp** (RNA read의 앞 10 bp).
- 즉 표준 처리는 **99bp i7에서 3×8bp LB를 추출→24bp CB로 재조립한 뒤** STARsolo `--soloType CB_UMI_Simple --soloCBstart 1 --soloCBlen 24 --soloUMIstart 25 --soloUMIlen 10`로 정렬. → **10x용 CellRanger-ARC/velocyto-on-ARC-BAM 경로는 그대로는 무효**(candidate_datasets.md §4 진술 확인).

**(c) spliced/unspliced 생성 경로는 존재한다 — STARsolo Velocyto mode.**
STARsolo는 `--soloFeatures Velocyto`로 spliced/unspliced/ambiguous mtx를 직접 생성(velocyto tool과 동등). 즉 **fastq만 확보되면** SHARE-seq에도 spliced/unspliced 산출은 기술적으로 가능. 실제로 velocity를 SHARE-seq skin에 돌린 선행연구가 복수 존재:
- **MultiVelo (Nat Methods 2023, PMC10246490)**: SHARE-seq mouse skin을 벤치마크에 사용, **velocyto로 spliced/unspliced 산출**했다고 명시. hair follicle trajectory 세포군 = **TAC(root/progenitor), IRS, medulla, hair shaft cuticle/cortex**.
- **TIVelo / mmVelo** 등 후속도 "Velocyto run으로 spliced/unspliced 정량, TAC·IRS·medulla·hair shaft-cuticle/cortex 추출"을 기술.
→ **선행 코드/논문 존재 = 방법 자체는 established.** 다만 이들은 **처리 결과물(loom/h5ad)을 공개 배포하지 않았다**(아래 d).

**(d) 가장 중요한 질문 — 공개된 velocity-ready SHARE-seq skin AnnData/loom: 못 찾음.**
- MultiVelo GitHub(welch-lab/MultiVelo): 튜토리얼·처리 데이터는 **E18 mouse brain(10x)만**. SHARE-seq skin 언급 없음.
- MultiVeloVAE figshare(10.6084/m9.figshare.30280333): **HSPC/EB/macrophage**만(config_macrophage.py 실측). skin 없음.
- dynamo에 MultiVelo 튜토리얼이 있으나 대상은 skin으로 확인 안 됨(**미확인**).
- figshare/zenodo/GitHub 광역 검색에서 **GSE140203 skin의 spliced/unspliced 또는 velocity-ready h5ad/loom 공개본을 특정하지 못함.**
→ **결론: "이미 누군가 공개했다"는 정황을 찾지 못함(미확인, 존재 배제는 아님).** 확보하려면 우리가 직접 reads에서 재생성해야 함.

**(e) 최대 리스크 — SRA의 index read(=barcode) 손상 보고.**
`scg_lib_structs` SHARE-seq 문서가 명시적으로 경고:
> "However, SRA messed up the index read and the `fastq` header. Therefore, we are going to use the `fastq` files from the species mixing experiment provided by the author in the GoogleDrive."
- SHARE-seq는 **cell barcode를 i7 index read(99bp)에 담는데, SRA가 이 index read와 fastq header를 망가뜨려 놓음** → SRA fastq에서 barcode 복원이 깨질 수 있음.
- 저자가 GoogleDrive로 보정 fastq를 제공했지만, 이는 **species-mixing 실험 샘플에 대해서만 문서화**돼 있고 **skin 샘플 fastq에 대한 것이 아님**(미확인 — skin용 보정 fastq가 GoogleDrive에 있는지 확인 못 함).
- 즉 "fastq→STARsolo→velocyto" 경로의 **입력 fastq(skin)에서 barcode가 정상 복원되는지가 검증되지 않았다.** 선행연구들이 어떤 fastq/BAM으로 velocyto를 돌렸는지(저자 직접 수령 BAM일 가능성)는 **미확인**.

### 판정: **CONDITIONAL-GO**
- 방법(STARsolo Velocyto)·barcode 구조·선행 사례는 모두 확인됨 → 기술적으로 불가능하지 않음.
- 그러나 (i) 공개 velocity-ready 배포본 없음 + (ii) SRA barcode 손상 보고 → **spliced/unspliced 확보가 "받으면 끝"이 아니라 실패 가능한 재정렬 작업**이다.
- **선행 게이트 필수**: skin fastq 1 lane preflight 또는 저자(MultiVelo/원저자 buenrostrolab) 처리 loom 요청. 통과 시 GO.

### 남은 리스크
- skin fastq의 SRA barcode 복원 실패 가능성(문서화된 위험). 저자 GoogleDrive에 skin fastq 보정본 유무 미확인.
- skin fastq 총량·SRA 다운로드 시간 **미확인**(34,774 cells 규모 → 수십~수백 GB 추정, 검증 안 됨).
- STARsolo mouse genome index(~25–30GB) + 고RAM 정렬 필요(GPU 아님, CPU+RAM).
- 우리 다른 4종은 "외부 제공 spliced/unspliced" 또는 "10x loom"이라 전처리 분기점이 통일됐는데, skin은 **우리가 직접 만든 spliced/unspliced** → 방법론 #5(preprocessing confound) 관점에서 오히려 더 통제됨(장점). 단 velocyto 파라미터를 HSPC와 정합시켜야 함.

---

## 블로커 2 — mouse→human ortholog 매핑 · **판정: GO**

### 조사한 것
E18 mouse brain에서 쓴 매핑 방식(`build_e18_mouse_brain.py`, `p3_concordance_e18_mouse_brain.py`)을 읽고 skin에 그대로 재사용 가능한지.

### 찾은 것
- `p3_concordance_e18_mouse_brain.py`가 cross-dataset 축(§B)에서 **`e_mv_u.index = e_mv_u.index.str.upper()`** 로 mouse Title-case를 human UPPER로 올린 뒤 `set(HSPC.index) & set(E18_upper.index)` 교집합을 취함. raw_shared(대소문자 불일치) → uppercase 후 shared를 리포트해 STATUS.md trap #1(대문자화 안 하면 near-zero)을 실측으로 방어.
- within-dataset 축(§A, α robust / lag fragile의 핵심 leg)은 **동일 gene축이라 매핑 자체가 불필요**. 즉 **primary 결과(H1)는 ortholog 매핑 없이도 산출**된다(E18 주석과 동일).
- skin도 mouse SYMBOL 축이므로 **E18 코드의 uppercase 블록을 그대로 복제**하면 됨(`p3_concordance_shareseq_skin.py`를 E18판에서 fork).

### 판정: **GO (E18 방식 verbatim 재사용)**

### 남은 리스크
- uppercase 매핑은 **1:1 ortholog에서 symbol이 보존된 경우(Gata1→GATA1)만 포착**. mouse-specific 유전자, symbol이 다른 ortholog(예: 일부 Krtap/후각수용체/gene family), 다대다 ortholog는 놓친다 → 교집합이 실제 ortholog보다 작아짐.
- 그러나 cross-dataset rank concordance에서 이 누락은 **noise만 추가 → "lag fragile" 결론에 보수적**(높은 ρ가 나오면 진짜 신호, 낮으면 fragile). E18에서 이미 이 논리로 수용됨.
- 더 정밀히 하려면 Ensembl/HomoloGene ortholog 테이블을 붙일 수 있으나 **불필요**(비용 대비 이득 낮고, primary는 within-dataset). 정밀 매핑은 optional.

---

## 블로커 3 — skin lineage annotation · **판정: GO**

### 조사한 것
TAC→hair shaft 궤적의 표준 marker set을 우리 `LINEAGE_MARKERS` 포맷으로 확보 가능한지.

### 찾은 것
1. **GEO가 provider annotation을 직접 배포**: `GSM4156597_skin_celltype.txt.gz`. E18이 제공 `cell_annotations.tsv`를 `rna.obs["celltype"]`로 그대로 쓴 것과 동일하게, **이 파일을 primary annotation으로 사용**하면 marker score를 강제할 필요조차 없다(concordance는 전역 per-gene fit rank → lineage 비-load-bearing).
2. **원논문/MultiVelo가 쓴 hair follicle 세포군**(확인됨): **TAC(root/progenitor) → IRS, medulla, hair shaft cuticle/cortex.** (+ 일반 skin에는 ORS, dermal papilla, dermal fibroblast, 면역세포 등 공존.)
3. 원논문의 대표 DORC/priming 예시 유전자: **Wnt3**(chromatin이 expression을 선행하는 대표 예), **Lef1**(precortex/hair shaft 분화 Wnt 표적).

### 제안 marker set (mouse Title-case — 데이터가 mouse이므로 symbol도 mouse 표기)
> ⚠️ 아래는 hair-follicle 생물학 문헌 + MultiVelo/원논문 기술에서 **컴파일한 제안치**이며, 원논문 supplementary의 verbatim 목록이 아니다(원논문 본문 fetch가 403으로 차단됨 → 아래 caveat). build 시 `var_names`에 존재하는 marker만 사용(macrophage config 규약).

```python
LINEAGE_MARKERS = {
    # 궤적 root — 증식성 progenitor (matrix/TAC)
    "TAC":        ["Shh", "Lef1", "Krt17", "Mki67", "Top2a", "Ccnb1", "Cdk1"],
    # inner root sheath
    "IRS":        ["Gata3", "Krt71", "Krt25", "Krt27", "Krt28"],
    # hair shaft — cortex/cuticle (분화 종착)
    "HairShaft":  ["Krt31", "Krt35", "Krt85", "Krt81", "Krt83",
                   "Lef1", "Msx2", "Hoxc13", "Dsg4"],
    # medulla (hair shaft 내층) — marker 불확실성 높음(caveat)
    "Medulla":    ["Foxn1", "Krt75"],
    # outer root sheath (분지)
    "ORS":        ["Krt5", "Krt14", "Krt15", "Sox9"],
    # 비-HF 상피/간질 (skin 전체 스냅샷에 공존) — 궤적 밖
    "DermalPapilla": ["Sox2", "Corin", "Bmp4"],
}
RARE_LINEAGES = {"Medulla", "DermalPapilla"}
```
- 궤적 서사: **TAC(root) → IRS / medulla / hair shaft cuticle·cortex**. concordance 자체는 lineage 비의존이므로, 이 marker set은 QC·시각화·within-lineage 진단용 보조. **1차 annotation은 provider `GSM4156597_skin_celltype.txt.gz`.**

### 판정: **GO (provider annotation + 보조 marker set)**

### 남은 리스크
- 제안 marker는 문헌 컴파일 — 원논문 verbatim이 아님(403 차단). build 후 provider celltype과 marker-score argmax의 **일치도를 sanity-check**할 것.
- medulla marker(Foxn1/Krt75)는 문헌상 특이도가 낮음 → rare로 분류, uncertainty 별도 보고(방법론 #2).
- provider celltype 라벨 체계(정확한 문자열: "TAC-1/TAC-2", "Hair Shaft-cuticle.cortex" 등)는 실제 파일 열어봐야 확정(**미확인** — 다운로드 금지라 헤더 미확인).

---

## 만약 GO라면 — 실행 계획 (macrophage 전례 준용)

heavy-run(kkkim, GPU/고RAM 서버) vs downstream(지용기, CPU) 분담. STATUS.md §0-(4) 표와 동일 구조.

| 단계 | 무엇 | env/자원 | 담당 | 산출 |
|---|---|---|---|---|
| **P0. preflight spike (게이트)** | skin RNA fastq 1 lane STARsolo `--soloFeatures Velocyto` → barcode 매칭률·spliced/unspliced nnz 확인. **또는** MultiVelo/buenrostrolab 저자에 처리 loom 요청 | CPU+고RAM(STAR index ~30GB) | **kkkim** | preflight 판정 메모(GO/NO-GO 확정) |
| **P1a. reads→spliced/unspliced** | skin fastq 전량 SRA/저자수령 → STARsolo 정렬(24bp CB + 10bp UMI) → spliced/unspliced mtx | CPU 다코어 + RAM≥40GB, mouse STAR index | **kkkim** | `data/shareseq_skin/velocyto/{spliced,unspliced}.mtx` |
| **P1b. build h5ad** | mtx + `GSM4156597_skin_celltype` + ATAC fragments→peak→gene 집계 → `rna_spliced_unspliced.h5ad` + `atac_gene.h5ad`. E18 `build_e18_mouse_brain.py`를 fork | scv-preprocess env | **kkkim** | `data/processed_shareseq_skin/*.h5ad` |
| **P2. fit 생산 (heavy-run)** | RNA-only floor → MultiVelo → MultiVeloVAE(GPU) → MoFlow(GPU) | scv-preprocess/mv + torch(GPU) | **kkkim (이 서버)** | `results/{rna_only,multivelo,multivelovae,moflow}_genes_shareseq_skin.csv` |
| **P3. downstream (concordance)** | within-skin cross-method(α robust/lag fragile) + cross-dataset HSPC↔skin(uppercase 매핑) ρ + bootstrap CI | **CPU만**, env·GPU 불필요 | **지용기 (BIOP01-41/-29 라인)** | `results/concordance_shareseq_skin.md` |
| **critic** | 결론·통계·hedge·priming best-case 서사 점검 | — | 모집/critic | 리뷰 코멘트 |

- **배선**: `config_shareseq_skin.py`(macrophage config fork) + `CROSS_DATASET_CONFIG`/`CROSS_DATASET_SUFFIX=_shareseq_skin` env 방식(STATUS.md §wiring). PYTHONPATH shim 금지.
- **p3 스크립트**: `p3_concordance_e18_mouse_brain.py`를 fork(uppercase 매핑 블록 포함) → `p3_concordance_shareseq_skin.py`.
- **예상 소요(추정, 미확정)**: preflight 반나절 / fastq 다운로드+정렬 수 시간~1일(fastq 총량 미확인) / P2 fit macrophage와 유사(수 시간, GPU) / P3 CPU 수십 분.
- **예상 디스크(추정)**: RAW.tar 7.4GB + skin fastq 수십~수백 GB(**미확인**) + mouse STAR index ~30GB + 중간 BAM/mtx. **여유 ≥200GB 권장**(RUNBOOK §0의 50GB로는 부족할 수 있음).
- **헤드라인 가치**: skin은 chromatin-potential/priming 정본 best case → "priming이 가장 강한 곳에서도 lag이 fragile한가"에 대한 가장 강한 반증 무대. macrophage(α +0.643)에 이어 α 순서 보존 + lag 무신호를 확인하면 서사 완결.

---

## 만약 NO-GO라면 — 대안

preflight 실패(barcode 복원 불가 + 저자 자료 확보 실패) 시:

1. **티켓 재정의 — "priming best-case"를 다른 데이터로 대체**: 이미 5개 축(HSPC/cortex/E18/BMMC/macrophage)에서 α-robust/lag-fragile이 보존됨. skin의 고유 가치는 **priming best-case**라는 서사뿐이므로, 이를 **원논문의 chromatin-potential 결과를 인용**해 서술로 대신하고 skin 자체 재현은 생략(정직하게 "재정렬 리스크로 skin은 정량 재현 대신 문헌 대조" 명시).
2. **대체 priming 데이터셋**: 다른 SHARE-seq/10x-Multiome 분화 데이터 중 spliced/unspliced가 이미 배포된 것을 탐색(예: MultiVeloVAE 10-dataset 중 미사용분 — embryoid body는 figshare에 velocity-ready로 존재). skin만큼 강한 priming 서사는 아니지만 재정렬 리스크 없음.
3. **저자 협업 경로**: MultiVelo(welch-lab) 또는 원저자(buenrostrolab)에 **처리된 skin velocity loom/h5ad 공유 요청**. 이들은 이미 velocyto 산출물을 보유 → 성사 시 블로커 1이 즉시 해소되고 GO로 전환(가장 저비용 해법).
4. **DEFER 유지**: 위가 모두 막히면 현행 DEFER를 유지하고 BIOP01-41을 "문헌 대조 only"로 축소.

---

## 정직 caveat — 확인 못 한 것 (추측을 사실로 쓰지 않음)

- **skin fastq의 SRA barcode 복원 가능 여부: 미확인.** SRA index-read 손상 보고는 `scg_lib_structs`에서 확인했으나, 그 보정 GoogleDrive fastq가 **skin 샘플에도 있는지, skin barcode가 실제로 복원되는지는 검증 못 함.** preflight로만 확정 가능.
- **선행연구(MultiVelo/TIVelo/mmVelo)가 정확히 어떤 입력으로 velocyto를 돌렸는지(저자 수령 BAM인지 SRA fastq인지): 미확인.**
- **공개 velocity-ready SHARE-seq skin 배포본 부재는 "못 찾음"이지 "존재하지 않음"이 아님.** figshare/zenodo 전수조사는 불가능 — 존재 배제 못 함.
- **skin fastq 총 용량·SRA 다운로드 시간: 미확인**(34,774 cells로부터 추정만).
- **`GSM4156597_skin_celltype.txt.gz`의 정확한 라벨 문자열·클러스터 수: 미확인**(다운로드 금지로 헤더 미열람). "TAC/IRS/medulla/hair shaft cuticle·cortex"는 MultiVelo 논문 기술에 근거.
- **제안 `LINEAGE_MARKERS`는 문헌 컴파일**이며 원논문 supplementary verbatim 아님(Cell/bioRxiv 본문 fetch가 403). build 후 provider celltype과 sanity-check 필요.
- **RAW.tar 크기 불일치**(GEO 7.4G vs STATUS.md 7.9GB) 미해소 — 실제 sha256로 확정할 것.
- GEO acc.cgi 페이지는 fetch 중 socket hang up 반복 → **파일 목록은 GEO ftp `filelist.txt` 파싱 결과에 근거**(1차 출처). GSM 번호(4156597 skin ATAC / 4156608 skin RNA)는 그 파싱에서 나옴.

---

## Sources
- GEO GSE140203 supplement 리스팅: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE140nnn/GSE140203/suppl/
- GEO GSE140203 filelist: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE140nnn/GSE140203/suppl/filelist.txt
- Ma et al. 2020 Cell (SHARE-seq, chromatin potential): https://www.cell.com/cell/fulltext/S0092-8674(20)31253-8 · bioRxiv: https://www.biorxiv.org/content/10.1101/2020.06.17.156943v1.full · PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC7669735/
- SHARE-seq barcode 구조 + SRA index-read 손상 보고: https://scg-lib-structs.readthedocs.io/en/latest/multi/SHARE-seq.html · https://github.com/Teichlab/scg_lib_structs/blob/master/docs/source/multi/SHARE-seq.md
- MultiVelo (SHARE-seq skin velocyto 사용, hair follicle 세포군): https://pmc.ncbi.nlm.nih.gov/articles/PMC10246490/ · GitHub(E18만 배포): https://github.com/welch-lab/MultiVelo
- STARsolo Velocyto mode(spliced/unspliced 산출): https://github.com/alexdobin/STAR/blob/2.7.3a/docs/STARsolo.md
- hair follicle lineage marker(Lef1/Wnt3 등): https://genesdev.cshlp.org/content/15/13/1688.long
- MultiVeloVAE datasets(HSPC/EB/macrophage, skin 없음): https://www.nature.com/articles/s41467-025-66287-6
- (로컬) E18 ortholog 매핑 코드: `cross_dataset/p3_concordance_e18_mouse_brain.py` (`.index.str.upper()`), `cross_dataset/build_e18_mouse_brain.py`; 분담 전례: `cross_dataset/config_macrophage.py`, STATUS.md §0-(4)
