# DATASETS_DOWNLOAD_MANIFEST: HSPC velocity 벤치마크 전 데이터셋 재수신 매니페스트

> **목적: GPU 서버 반납(2026년 8월 말) 대비.** 원본 데이터를 나중에 다시 받을 수 있도록 데이터셋마다 "어디서, 무엇을, 어떻게 받는지"를 한 문서에 모은다.
> **데이터는 리포에 없다.** `pipeline/hspc-velocity-benchmark/data/`는 `.gitignore` 등재라 원본 binary와 중간 산물은 커밋되지 않는다. 이 문서(`*.md`)만 git으로 추적된다.
> 성격: 흩어진 기존 provenance/config/log에서 실제 URL과 파일명을 그대로 옮긴 것이다. 값이 없어 표준 패턴으로 구성한 항목은 `등급 C`로 표시하고 다운로드 전 검증을 요구한다. 작성 2026-08-19.

## 읽는 법: provenance 등급 3단계

| 등급 | 뜻 | 해당 데이터셋 |
|---|---|---|
| **A** | 소스 URL 기록됨 + sha256/크기 기록됨(재수신 후 무결성 대조 가능) | GSE209878, GSE205117 ATAC fragments, GSE75792 |
| **B** | 소스 URL 기록됨, 체크섬 없음(또는 앞 16자만) | GSE194122, E18 mouse brain, GSE229305, GSE229314, MOLM13(Zenodo 15785218) |
| **C** | 소스 URL 미기록 → 표준 패턴으로 구성, **다운로드 전 검증 요** | GSE162170, figshare `ndownloader` 호스트 |

- **GEO 표준 suppl URL 패턴**: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSEnnnNNN/GSE.../suppl/<파일>`. NNN 자리는 GSE 번호 앞 세 자리 + `nnn`(예: GSE162170 → `GSE162nnn`). GSM 파일은 `.../geo/samples/GSMnnnNNN/GSM.../suppl/<파일>`.
- **취득 방식 주의(단순 curl로 안 되는 것)**: GSE205117 GEX(SRA `.sra` → `fasterq-dump --include-technical` → STARsolo), GSE229314 half-life(PMC proof-of-work 챌린지), GSE284047 raw(dbGaP 제한접근 → figshare 우회), GSE194122 spliced/unspliced(29GB BAM + velocyto pass). 각 절에 명시한다.
- **원본 다운로드 대상**과 **파생 파일**을 구분한다. half-life/합성율 CSV 다수는 다운로드 대상이 아니라 스크립트가 만든 파생물이다(§5).

---

# 1. Primary: GSE209878 (Human HSPC 10x Multiome) · 등급 A

- **Accession**: GEO **GSE209878** (PMID 36229609). Human HSPC, paired 10x Multiome, single donor(mobilized CD34+). MultiVelo 원논문 데이터.
- **역할**: 주 데이터셋(primary). gene별 chromatin→transcription lag 정량 + velocity method head-to-head 벤치마크의 기준.
- **로컬 경로**: `data/GSE209878/MV-1/`, `data/GSE209878/MV-2/` (2 sample = 2 timepoint: MV-1=day0, MV-2=day7).
- **다운로드 방법**: `bash scripts/download_data.sh` (→ `data/GSE209878/MV-{1,2}`, 약 1.9GB). Optional fragments는 스크립트 맨 아래 주석 해제.
- **provenance 정본**: `download_manifest.tsv`(sha256 전량), `P0_provenance.md` §1.

## 받을 파일 (sample당)

series suppl(`GSE209nnn/GSE209878/suppl/`)에서 받는 것:

| sample | 파일 | 크기(bytes) | sha256 | 소스 URL |
|---|---|---|---|---|
| MV-1 | `GSE209878_3423-MV-1_matrix.mtx.gz` | 610277465 | `0a351160fc3204b4…` | series suppl |
| MV-1 | `GSE209878_3423-MV-1_features.tsv.gz` | 3551910 | `ba9d56e353de8fc1…` | series suppl |
| MV-1 | `GSE209878_3423-MV-1_barcodes.tsv.gz` | 48912 | `051fa682a8057134…` | series suppl |
| MV-1 | `GSE209878_3423-MV-1_feature_linkage.bedpe.gz` | 991079 | `8b93be778c2a52c1…` | series suppl |
| MV-2 | `GSE209878_3423-MV-2_matrix.mtx.gz` | 856665370 | `492d4c40b6fcc345…` | series suppl |
| MV-2 | `GSE209878_3423-MV-2_features.tsv.gz` | 4120256 | `ff377eaf6ea04e5c…` | series suppl |
| MV-2 | `GSE209878_3423-MV-2_barcodes.tsv.gz` | 72356 | `0a21f19e48707028…` | series suppl |
| MV-2 | `GSE209878_3423-MV-2_feature_linkage.bedpe.gz` | 8329211 | `6f8523f5856208da…` | series suppl |

series suppl base URL: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE209nnn/GSE209878/suppl/`

GSM sample suppl(velocyto loom + peak_annotation)에서 받는 것. URL은 `download_data.sh` L26-29(base) + L51-52,L58-59(파일명)에서 조합했다:

| sample | 파일 | 크기(bytes) | sha256 | 소스 URL |
|---|---|---|---|---|
| MV-1 | `GSM6403409_3423-MV-1_atac_peak_annotation.tsv.gz` | 2210266 | `a4e0f05a919f4361…` | `.../geo/samples/GSM6403nnn/GSM6403409/suppl/` |
| MV-1 | `GSM6403408_3423-MV-1_gex_possorted_bam_0E7KE.loom.gz` | 163697703 | `b028ce0c3e8fead3…` | `.../geo/samples/GSM6403nnn/GSM6403408/suppl/` |
| MV-2 | `GSM6403411_3423-MV-2_atac_peak_annotation.tsv.gz` | 2636311 | `7d83c282d1eeed6f…` | `.../geo/samples/GSM6403nnn/GSM6403411/suppl/` |
| MV-2 | `GSM6403410_3423-MV-2_gex_possorted_bam_ICXFB.loom.gz` | 274317235 | `a91fac100d07304d…` | `.../geo/samples/GSM6403nnn/GSM6403410/suppl/` |

- **받지 않는 것**: `GSE209878_RAW.tar`(9.8GB 전체), `*_atac_fragments.tsv.gz`(MV-1 4.3GB + MV-2 5.1GB, peak가 matrix에 이미 포함이라 불요).
- sha256 전체 값은 `download_manifest.tsv` 참조(위 표는 앞 16자).

---

# 2. Cross-dataset 재현: E18 mouse brain 5k (10x Multiome) · 등급 B

- **Accession**: GEO 없음. 10x Genomics 공개 데모 "Fresh Embryonic E18 Mouse Brain (5k)", CellRanger-ARC **1.0.0**(`e18_mouse_brain_fresh_5k`). velocity layer와 annotation은 `welch-lab/MultiVelo` GitHub에서.
- **역할**: MultiVelo tutorial 데이터셋. spliced/unspliced 직접 제공이라 전처리 거의 없이 두 번째 재현 + cell-cycle confound stress-test(cycling-RG 풍부).
- **로컬 경로**: `data/e18_mouse_brain/`
- **다운로드 방법**: `cross_dataset/build_e18_mouse_brain.py`(빌드). 원 URL은 아래.
- **provenance 정본**: `cross_dataset/P0_provenance_crossdataset.md` Dataset A. ⚠️ **sha256는 앞 16자만 기록됨**(전체 아님). `sha256sum` 재계산 시 값이 짧다고 오인하지 말 것.

## 받을 파일 (sha256 = 앞 16자만)

| 파일 | 크기 | sha256(앞16) | 소스 URL |
|---|---|---|---|
| `10X_multiome_mouse_brain.loom` | 90MB | `5620bccd41c275e8` | `https://raw.githubusercontent.com/welch-lab/MultiVelo/main/Examples/velocyto/10X_multiome_mouse_brain.loom` |
| `cell_annotations.tsv` | 136K | `e568dc50ff33ab0f` | `https://raw.githubusercontent.com/welch-lab/MultiVelo/main/Examples/cell_annotations.tsv` |
| `e18_filtered_feature_bc_matrix.tar.gz` | 195MB | `dad70202574ad0cd` | 10x base(아래) `..._filtered_feature_bc_matrix.tar.gz` |
| `e18_atac_peak_annotation.tsv` | 6.6MB | `603564fc7bd6bd61` | 10x base `..._atac_peak_annotation.tsv` |
| `e18_analysis.tar.gz` | 290MB | `6806c85fbcffc462` | 10x base `..._analysis.tar.gz` |
| `seurat_wnn.zip` | 1.6MB | (없음) | `https://.../welch-lab/MultiVelo/main/Examples/seurat_wnn/`(optional; pyWNN로 재계산 가능) |

- 10x base URL: `https://cf.10xgenomics.com/samples/cell-arc/1.0.0/e18_mouse_brain_fresh_5k/e18_mouse_brain_fresh_5k_{filtered_feature_bc_matrix.tar.gz, atac_peak_annotation.tsv, analysis.tar.gz}`
- 10x dataset page: `https://www.10xgenomics.com/resources/datasets/fresh-embryonic-e-18-mouse-brain-5-k-1-standard-1-0-0`
- ⚠️ `candidate_datasets.md`가 `2-0-0` 버전을 인용한 것은 doc 오류다. MultiVelo Demo notebook과 배포 loom은 **1.0.0** 기준이니 1.0.0을 쓴다.

---

# 3. Cross-dataset 재현: GSE194122 (Human BMMC, 10x Multiome) · 등급 B

- **Accession**: GEO **GSE194122** → BioProject **PRJNA799242** → SRA study **SRP356158**. Submitter CELLARITY. Homo sapiens.
- **역할**: HSPC와 같은 조혈축(가장 가까운 재현). human이라 gene 축이 GSE209878과 직접 겹친다(ortholog 매핑 불요).
- **로컬 경로**: `data/GSE194122/`
- **provenance 정본**: `cross_dataset/P0_provenance_crossdataset.md` Dataset B.

## (a) processed h5ad: 등급 B (sha256 앞16만)

| 파일(재수신 시 긴 이름) | 로컬 파일명 | 크기 | sha256(앞16) | 소스 URL |
|---|---|---|---|---|
| `GSE194122_openproblems_neurips2021_multiome_BMMC_processed.h5ad.gz` | `GSE194122_multiome_BMMC_processed.h5ad.gz` | 2.79GB(2917117242) | `53b516e7a35518e7` | series suppl(아래) |

- 소스 URL: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194122/suppl/GSE194122_openproblems_neurips2021_multiome_BMMC_processed.h5ad.gz`
- ⚠️ 이 processed h5ad에는 **spliced/unspliced가 없다**(`layers=['counts']`). CITE-seq 동반 파일(`..._cite_BMMC_processed.h5ad.gz`)은 multiome이 아니라 미취득.

## (b) spliced/unspliced 복원: velocyto on BAM (moderate)

**상태: 복원 완료.** `data/GSE194122_bmmc_velocyto/GSE194122_s4d9.loom`(48216547 bytes, 2026-07-06 생성). site4_donor09 GEX possorted BAM에 velocyto pass를 돌린 결과다. 재수신 시 아래 경로로 재생성 가능:

- 원본 BAM(공개, dbGaP 제한 없음): RNA/GEX run **SRR17693266**(GSM5828480) → `site4_donor09_multiome_gex.possorted_genome_bam.bam`, **28.66GB**, md5 `a7fed3450edf61dbba4d102087cb282d`.
  - S3: `https://sra-pub-src-2.s3.amazonaws.com/SRR17693266/site4_donor09_multiome_gex.possorted_genome_bam.bam.1`
- 복원 방법: `velocyto run`/`run10x`를 GEX possorted BAM(CB/UB 태그 보유)에 + GRCh38 GTF + processed h5ad의 filtered-barcode 목록 → spliced/unspliced loom. CellRanger-ARC 재실행이 아니다.
- 취득: `prefetch --type all SRR17693266`(또는 위 S3 curl). 기본 `.sra`는 normalized reads라 velocyto에 부적합, 원본 BAM을 받아야 한다.
- 참고 메타: BioProject `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA799242`, ATAC run 예 `SRR17693253`(GSM5828493). 프로젝트 런 = RNA-Seq 25 + ATAC-seq 13.

---

# 4. Cross-dataset 재현: GSE162170 (Human fetal cortex, Trevino 2021) · **등급 C (URL 미기록 → 패턴 구성)**

- **Accession**: GEO **GSE162170** (Trevino et al. 2021, Cell). human fetal cerebral cortex multiome.
- **역할**: cross-dataset 재현 1번. human이라 HSPC와 gene 축 직접 겹침. 원논문(MultiVelo)이 TF→motif accessibility lag을 낸 데이터셋.
- **로컬 경로**: `data/human_brain/`
- **다운로드 방법**: 빌드 `cross_dataset/build_human_brain.py`(GEO suppl tsv → processed h5ad). RUNBOOK option B(processed 직접 공유 경로).
- ⚠️ **provenance 갭**: 기존 문서 어디에도 다운로드 URL이 기록돼 있지 않다(리포 grep 결과 논문 DOI만 존재: `https://doi.org/10.1016/j.cell.2021.07.039`). 아래 소스 URL은 **GEO 표준 suppl 패턴으로 구성한 것이며 다운로드 전 검증이 필요하다.**

## 받을 파일: 파일명은 실측(로컬 존재), sha256은 로컬 실측(2026-08-19, 원 다운로드 기록 아님), URL은 패턴 구성

`build_human_brain.py` L36-41이 소비하는 파일 + 로컬 실재 파일. 파일 날짜(2021-09-17)로 GEO 유래 확인.

| 파일 | 크기(bytes) | sha256(로컬 실측 2026-08-19) | 비고 |
|---|---|---|---|
| `GSE162170_multiome_spliced_rna_counts.tsv.gz` | 11115238 | `beca04dcef6ab467…` | RNA spliced(symbol 축, 사용) |
| `GSE162170_multiome_unspliced_rna_counts.tsv.gz` | 15622285 | `c28f1443101d02d1…` | RNA unspliced(symbol 축, 사용) |
| `GSE162170_multiome_atac_counts.tsv.gz` | 149865144 | `1c61e5c0b5103bdd…` | ATAC peaks×cells(headerless) |
| `GSE162170_multiome_atac_consensus_peaks.txt.gz` | 18315449 | `9504dd1759d0dc6d…` | consensus peak 좌표 |
| `GSE162170_multiome_cell_metadata.txt.gz` | 492098 | `0520b5f37f3d03bb…` | cell metadata |
| `GSE162170_multiome_cluster_names.txt.gz` | 278 | `25c2fee9cfc80b70…` | cluster 이름 매핑 |
| `GSE162170_multiome_rna_counts.tsv.gz` | 24845803 | `6a7f112b7bc4546…` | ⚠️ **다운로드했으나 미사용**(ENSG 축이라 HSPC symbol 축과 안 겹침, `build_human_brain.py` L13-14) |

- **소스 URL(패턴 구성, 검증 요)**: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE162nnn/GSE162170/suppl/<위 파일명>`
- sha256는 이번 반납 대비 로컬에서 계산한 값이라 provider가 게시한 digest가 아니다. 재수신 후 파일이 동일한지 대조하는 용도로만 쓴다.

---

# 5-cross. Cross-dataset 재현: GSE205117 (Mouse gastrulation E7.5–E8.75, 10x Multiome)

> ⚠️ **task 브리핑은 이 데이터셋을 "provenance 없음(갭)"이라 했으나 사실이 아니다.** ATAC fragments는 실 URL + sha256 + 정확한 크기까지 기록돼 있고(등급 A), GEX는 실 SRA S3 URL과 8개 SRR이 열거돼 있다. 진짜 갭은 좁다: `.sra`/fastq의 sha256과 STARsolo index/annotation 빌드 기록이 없다.

- **Accession**: GEO **GSE205117** (mouse gastrulation). 사전등록 = `manuscript/PREREGISTRATION_gse205117.md`.
- **역할**: 5번째 cross-dataset 재현. priming 극대(gastrulation)에서도 'α robust / lag fragile'가 유지되는지 확증. skin(NO-GO) 대체 채택.
- **로컬 경로**: ⚠️ **repo `data/` 밖이다.** raw는 `/home/kkkim/data/gse205117_fullB/`(sra/, fastq/, atac_frag/, gex_solo/). processed는 `data/processed_gse205117/`. 4 rep1 시점(E7.5 / E8.0 / E8.5 / E8.75).
- **provenance 정본**: `cross_dataset/config_gse205117.py`, `cross_dataset/dl_gse205117_fullB.sh`, `cross_dataset/dl_gse205117_atac_frag.sh`, ATAC sha = `/home/kkkim/data/gse205117_fullB/atac_frag/atac_frag_provenance.tsv`.

## (a) GEX: raw SRA → STARsolo Velocyto · 등급 B(체크섬 없음)

`.sra`를 SRA ODP S3에서 받아 `fasterq-dump`로 fastq 변환 후 STARsolo Velocyto로 spliced/unspliced를 만든다.

- **소스 URL 패턴**: `https://sra-pub-run-odp.s3.amazonaws.com/sra/<SRR>/<SRR>` (`dl_gse205117_fullB.sh` L16)
- 4 시점 GEX SRR: **E7.5=SRR19450575 · E8.0=SRR19450564 · E8.5=SRR19450560 · E8.75=SRR19450574**
- 다운로드 스크립트: `cross_dataset/dl_gse205117_fullB.sh`(aria2c 16연결 → `fasterq-dump`).
- ⚠️ **취득 방식 주의**: `fasterq-dump --include-technical --split-files` 필수. 이 플래그가 없으면 10x barcode read(R1)가 드롭돼 STARsolo가 불가하다(2026-07-12 버그수정 기록, 스크립트 L57).
- ⚠️ **도구 경로**: aria2c·fasterq-dump는 `/opt/envs/dltools/bin/`. `<FILL: GPU 서버 반납 후 이 공유 env 경로 재확인 요>`.
- 현재 로컬 상태: `.sra` 7개(~185GB, `sra/`), fastq(`fastq/`, `_1`~`_4`, 총 ~2.9TB) 모두 존재(2026-08-19 확인, 아직 reclaim 안 됨). `reclaim_gse205117_raw.sh`가 게이트 통과 시 삭제하는 캐시라 반납 전 삭제될 수 있다. sha256/size는 `<FILL: .sra/fastq 무결성 기록 없음>`.

## (b) ATAC: GEO 제공 processed fragments · 등급 A

raw 정렬·cellranger-arc 불요. sample별 fragments.tsv.gz를 GEO에서 직접 받는다.

- **소스 URL base**: `https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM6205nnn/<GSM>/suppl/<파일>` (`dl_gse205117_atac_frag.sh` L9-16)
- 다운로드 스크립트: `cross_dataset/dl_gse205117_atac_frag.sh`

| 시점 | 파일(GSM/suppl/) | 크기(bytes) | sha256 |
|---|---|---|---|
| E7.5 | `GSM6205427/suppl/GSM6205427_E7.5_rep1_ATAC_fragments.tsv.gz` | 2920922447 | `acde220774e5d8a7d14fc38444613f2127a080d6d6316f7fb49cbb881740b2d1` |
| E8.0 | `GSM6205430/suppl/GSM6205430_E8.0_rep1_ATAC_fragments.tsv.gz` | 2391892970 | `bb4f23a6b25ac82e4ee0befbbaf1e3f017abda86f6910288749927a0398154e8` |
| E8.5 | `GSM6205434/suppl/GSM6205434_E8.5_rep1_ATAC_fragments.tsv.gz` | 3337999783 | `070bfcb07c4786707499b0376724b1fc8622cbd9651872ff0bde9d0100336bf2` |
| E8.75 | `GSM6205436/suppl/GSM6205436_E8.75_rep1_ATAC_fragments.tsv.gz` | 2512208940 | `7c6f2c0f34e5471c2d83278d0bad2b5e6e36a71f82a9539580730dfb224b6659` |

- peak→gene 집계는 우리 자체(gencode vM25 gene body ±10kb). provider gene-activity 미사용.
- 참고: `config_gse205117.py`의 ATAC GSM(GSM6205427/30/34/36)은 위 fragments 파일용이다. `dl_gse205117_fullB.sh`의 `ATAC` SRR(SRR19450572/569/557/555)은 별도 SRA raw로, fragments를 쓰는 현재 경로에서는 필수가 아니다.

---

# 6. Cross-dataset 재현: GSE284047 / figshare 30280333 (Macrophage) · 등급 C(호스트) + B(파일)

- **Accession**: GEO **GSE284047**(MultiVeloVAE 신규; Li & Gu et al., Nat Commun 16, 11505, 2025). ⚠️ **raw = dbGaP phs002915.v2.p1 제한접근**(환자 프라이버시) → 사용 불가.
- **공개 경로**: **figshare DOI `10.6084/m9.figshare.30280333` (CC BY 4.0)**, MultiVeloVAE post-processed AnnData.
- **역할**: cross-dataset 재현. HSPC와 같은 human 조혈축의 하류(단핵구→대식세포 분화). drug-timing endpoint에 가장 근접.
- **로컬 경로**: `data/macrophage/`
- **다운로드 방법**: `cross_dataset/build_macrophage.py`(빌드), 다운로드 로그 `data/macrophage/download_macrophage.log`.
- **provenance 정본**: `cross_dataset/config_macrophage.py`, `cross_dataset/P0_provenance_crossdataset.md`(Bonus note).

## 받을 파일

| 파일 | 크기(bytes) | figshare file ID | 진입점 |
|---|---|---|---|
| `8489-MV-1-9060-MV-3_adata_postpro_concat.h5ad`(RNA) | 189862633 | 58495783 | figshare DOI(아래) |
| `8489-MV-1-9060-MV-3_adata_atac_postpro_concat.h5ad`(ATAC, gene-level) | 64946348 | 58495777 | figshare DOI(아래) |

- **검증된 진입점(등급 A 수준)**: `https://doi.org/10.6084/m9.figshare.30280333`. DOI와 file ID(58495783/58495777)는 config와 다운로드 로그에 실재하고, 크기(`got==exp`)도 로그로 검증됐다.
- **직접 다운로드 URL(등급 C, 검증 요)**: figshare 표준 패턴 `https://ndownloader.figshare.com/files/<file_id>`(예 `.../files/58495783`). 로그가 "corrected host"로만 적고 실제 호스트 문자열을 남기지 않아 호스트는 패턴 구성이다. 재수신 시 DOI 페이지에서 파일 링크를 확인하는 편이 안전하다.
- ⚠️ 취득 형태 주의: RNA postpro는 HVG 필터 + scVelo moments 완료 상태(layers `Ms`/`Mu`)로, raw spliced/unspliced count layer는 없다. concat은 HSPC(8489-MV-1) + macrophage(9060-MV-3) 2 batch라 macrophage batch만 subset해야 primary leakage를 막는다(`build_macrophage.py`).

---

# 7. External rate validation (α/γ 외부검증) 원본 데이터

γ vs 실측 mRNA 반감기, α vs 실측 TT-seq 합성율 검정에 쓰는 외부 실측 소스. 결과 = `results/external_rate_validation.md`, `results/external_rate_validation_schwalb.md`. provenance 정본 = `data/PROVENANCE_halflife.md`.

## 7-1. GSE229314: Todorovski 2024 half-life SuperSeries · 등급 B

- **Accession**: GEO SuperSeries **GSE229314**. Todorovski I. et al., NAR Cancer 6(4):zcae039 (2024), DOI 10.1093/narcan/zcae039.
- **역할**: 주 반감기 reference(K562) + 조혈계 비교셋(THP1). γ 외부검증.
- **원파일**: `zcae039_supplemental_files.zip` → `Manuscript_NAR_Cancer_Supp_Table_10_230322.xlsx`, 시트 `K562_UT`(6,580 gene) / `THP1_UT`(7,001 gene).
- **소스 URL**: `https://pmc.ncbi.nlm.nih.gov/articles/instance/11447529/bin/zcae039_supplemental_files.zip`
- ⚠️ **취득 방식 주의**: PMC proof-of-work 챌린지 통과 후 취득. OUP silverchair CDN 링크는 signed-cookie 필요라 직접 curl 불가. 단순 curl로 안 됨.
- 파생물(§5): `data/todorovski_k562_halflife.csv`, `data/halflife_thp1.csv`.

## 7-2. GSE229305: Todorovski 2024 K562 TT-seq 합성율 · 등급 A(sha 있음은 파생물)

- **Accession**: GEO **GSE229305**(GSE229314 SuperSeries의 subseries, "TTseq K562 production rates").
- **역할**: α 외부검증 Part B 주 소스(fit α ≡ TT-seq 생산율).
- **원파일**: `GSE229305_K562_TTseq_synthesis_measurements_rates.txt.gz`(로컬 `data/GSE229305_K562_TTseq_rates.txt.gz`, 145375 bytes).
- **소스 URL**: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE229nnn/GSE229305/suppl/GSE229305_K562_TTseq_synthesis_measurements_rates.txt.gz`(GEO FTP, proof-of-work 없음, 직접 curl 성공 2026-07-07).
- ⚠️ THP1 TT-seq 생산율 subseries는 부재 → Part B는 K562 단독.
- 파생물(§5): `data/k562_ttseq_synthrate.csv`.

## 7-3. GSE75792: Schwalb 2016 K562 TT-seq (α 2차 소스) · 등급 A

- **Accession**: GEO **GSE75792**. Schwalb B. et al., Science 352(6290):1225-1228, 2016, DOI 10.1126/science.aad9841. K562 wild-type TT-seq.
- **역할**: α 외부검증 2차 독립 소스(1차 GSE229305의 "n=1 외부" 취약성 완화 시도. 결과는 null, 정직 보고).
- **원파일**: `GSE75792_transcript.annotation.gtf.gz`(로컬 `data/GSE75792_transcript.annotation.gtf.gz`), sha256 `2c7a31a83d81db465889973860b0a00dab5c081997432ada1fb396db9e6707b9`.
- **소스 URL**: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE75nnn/GSE75792/suppl/GSE75792_transcript.annotation.gtf.gz`(GEO FTP, proof-of-work 없음, 직접 curl 성공 2026-07-10).
- ⚠️ per-gene 합성율 없음(per-TU만, hg19 좌표). per-gene는 GENCODE v19 좌표 join으로 재계산(§8 gencode 참조).
- 파생물(§5): `data/k562_schwalb_ttseq_synthrate.csv`.

## 7-4. MOLM13 half-life: RNADecayCafe / Muhar 2018 (Zenodo) · 등급 B

- **Accession**: Zenodo record **15785218**(RNADecayCafe, bioRxiv 2025.08.19.671151 / PMC12393342). 원 study = Muhar et al. 2018, Science(Zuber lab SLAM-seq), RNADecayCafe `dataset` 라벨 `Muhar_etal_2018_many`.
- **역할**: γ 외부검증 주 gate 지표(독립 lab·독립 파이프라인, cross-study 대표치). 실질 무검열(가장 깨끗한 reference).
- **원파일**: `AvgKdegs_genes_v1.csv`(`cell_line=='MOLM13'` 필터).
- **소스 URL**: `https://zenodo.org/api/records/15785218/files/AvgKdegs_genes_v1.csv/content`
- 파생물(§5): `data/halflife_molm13.csv`. 같은 Zenodo에서 `cell_line=='HEK293T'` → `data/halflife_hek293t.csv`, `cell_line=='K562'` → `data/halflife_rnadecaycafe_k562.csv`(비조혈 하한 + cross-lab K562 앵커).

---

# 5(파일). 파생 파일: 다운로드 대상 아님(스크립트 산출물)

아래 CSV는 소스 URL이 없다. 위 §7 원본에서 스크립트가 gene 매핑·정규화·필터로 만든 파생물이다. 재수신 시 원본을 받아 스크립트를 다시 돌려 재생성한다.

| 파생 파일 | 원본(§7) | 생성 |
|---|---|---|
| `data/todorovski_k562_halflife.csv` (6,580) | GSE229314 S10 `K562_UT` | rename만 |
| `data/halflife_thp1.csv` (7,001) | GSE229314 S10 `THP1_UT` | rename만 |
| `data/halflife_molm13.csv` (10,624) | Zenodo 15785218 (MOLM13) | filter+rename |
| `data/halflife_hek293t.csv` (15,231) | Zenodo 15785218 (HEK293T) | filter+rename |
| `data/halflife_rnadecaycafe_k562.csv` (10,802) | Zenodo 15785218 (K562) | filter+rename |
| `data/k562_ttseq_synthrate.csv` (11,776) | GSE229305 | treatment=UT, rename |
| `data/k562_schwalb_ttseq_synthrate.csv` (2,746) | GSE75792 + GENCODE v19 | 좌표 join 재계산 |

---

# 8. 보조 참조 파일 (reference; download 대상)

| 파일 | 로컬 | 소스 URL | 등급 |
|---|---|---|---|
| GENCODE v19 gene-level (hg19) | `data/gencode.v19.genes.gtf.gz`(sha256 `dffda97722d19f56…`) | `https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz` → `feature=="gene"` subset | A(URL 실재, sha256 앞16) |
| Housekeeping gene list (Eisenberg & Levanon) | `data/housekeeping.txt`(3,804) | `https://www.tau.ac.il/~elieis/HKG/HK_genes.txt`(첫 컬럼 symbol) | B(URL 실재, 체크섬 없음) |
| MGI mouse→human ortholog | `data/HOM_MouseHumanSequence.rpt` | `https://www.informatics.jax.org/downloads/reports/HOM_MouseHumanSequence.rpt`(디렉터리 실재, `p5_drug_arm_feasibility.py` L336) | B(URL 실재, 체크섬 없음) |
| MGI marker→Ensembl | `data/MRK_ENSEMBL.rpt` | `https://www.informatics.jax.org/downloads/reports/MRK_ENSEMBL.rpt`(같은 MGI reports 디렉터리) | C(디렉터리만 기록, 파일 URL 패턴 구성) |

- GENCODE v19는 §7-3 Schwalb per-gene 재계산용. housekeeping은 α/γ 검정 non-HK 층화용(스크립트 input). MGI 파일은 drug-arm feasibility(`scripts/p5_drug_arm_feasibility.py`)의 mouse→human ortholog join용.

---

# 9. 미사용 데이터셋 (기록만)

- **GSE140203** (Mouse skin hair follicle, SHARE-seq; Ma et al. 2020, Cell, DOI 10.1016/j.cell.2020.09.056): 복원 시도했으나 SHARE-seq가 10x가 아니고 raw only(spliced/unspliced 없음)라 재처리 부담이 커 **DEFER/미사용**. GSE205117로 대체. 상세 = `cross_dataset/FEASIBILITY_shareseq_skin.md`, `cross_dataset/candidate_datasets.md`.

---

# 부록: 등급/취득방식 요약

| 데이터셋 | 역할 | 로컬 경로 | provenance 등급 | 단순 curl 가능? |
|---|---|---|---|---|
| GSE209878 | primary HSPC | `data/GSE209878/` | **A** | O(GEO FTP) |
| E18 mouse brain | 재현(cell-cycle) | `data/e18_mouse_brain/` | **B**(sha 앞16) | O(github/10x) |
| GSE194122 | 재현(조혈, 최근접) | `data/GSE194122/` (+`_bmmc_velocyto/`) | **B** | processed=O; spliced/unspliced=X(29GB BAM+velocyto) |
| GSE162170 | 재현(fetal cortex) | `data/human_brain/` | **C**(URL 미기록→패턴) | O 예상(GEO FTP, 검증 요) |
| GSE205117 | 재현(gastrulation) | `/home/kkkim/data/gse205117_fullB/`(repo 밖) | ATAC=**A**, GEX=**B** | ATAC=O; GEX=X(SRA→fasterq-dump `--include-technical`→STARsolo) |
| GSE284047/figshare | 재현(macrophage) | `data/macrophage/` | 진입점 A, 호스트 **C** | raw=X(dbGaP); figshare=O(DOI 경유) |
| GSE229314 | γ 검증(half-life) | 파생 `data/*.csv` | **B** | X(PMC proof-of-work) |
| GSE229305 | α 검증(TT-seq) | `data/GSE229305_*.gz` | **A** | O(GEO FTP) |
| GSE75792 | α 검증 2차 | `data/GSE75792_*.gz` | **A** | O(GEO FTP) |
| Zenodo 15785218 | γ 검증(MOLM13 등) | 파생 `data/halflife_*.csv` | **B** | O(Zenodo API) |

> `<FILL>` 항목(재수신 전 확인 요): GSE205117 `.sra`/fastq sha256·크기, GSE205117 STARsolo index/annotation 빌드 기록, `/opt/envs/dltools` 도구 경로(반납 후), MRK_ENSEMBL.rpt 정확한 파일 URL.
