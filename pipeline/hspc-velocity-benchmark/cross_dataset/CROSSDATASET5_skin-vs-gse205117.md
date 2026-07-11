# Cross-dataset #5 재점검 + 대체 후보 (2026-07-11)

> BIOP01 velocity 벤치마크 5번째 cross-dataset. skin(#5) NO-GO 재점검 + 대체(GSE205117) feasibility·preflight 기록.
> **git 커밋은 내용 쌓인 뒤**(사용자 지시). 중단 대비 durable 기록.

## 1. skin (#5, GSE140203 SHARE-seq) — DEFER 확정, 단 사유 정정 필요

**결론: DEFER.** 단 **블로커는 "barcode 부재"가 아니라 "velocity 신호(nnz) 약함"**.

- ❌ 이번 세션 초반 오판: STARsolo-from-FASTQ 경로로 "SRR10428407 49bp·barcode 부재 → NO-GO" 판정 + BIOP01-41 게시 + 57GB fastq 삭제. **이 경로 자체가 FEASIBILITY 문서가 "거짓 NO-GO 유발"이라 경고한 경로**(SHARE-seq 3×8bp 비연속 barcode에 CB_UMI_Simple 연속 파라미터).
- ✅ 정본 경로(velocyto-on-BAM, 저자 BAM `skin.late.anagen.rna.norg.bam`, barcode read이름 선디코딩)는 **2026-07-10 이미 완료(DONE)**: `/home/kkkim/data/shareseq_gse140203_preflight/`.
  - barcode 매칭 **정상**(0 reads skipped, 50,671 cells) — barcode는 문제 아님.
  - **spliced nnz 0.02% / unspliced 0.03%** (macrophage GO 전례 35.6% 대비) → "약함".
- GTF-정합 재확인(2026-07-11): BAM=mm10 chr-prefixed(chr1 LN 195,471,971), vM23 GTF=동일 네이밍 → **좌표/처리 버그 아님**. 단 nnz.py가 전체 유전자(55,335) 분모인데 스모크는 chr1 read만 → ~20배 희석(실제 chr1-gene nnz ≈0.56%). 그래도 35.6%엔 못 미치고 per-cell spliced ~14.5/cell로 얕음 → SHARE-seq 3′ 얕은 신호가 근본 한계.

**→ TODO(JIRA):** BIOP01-41 사유 정정("barcode 부재"→"velocyto-on-BAM nnz 약함, barcode·GTF는 정상") + STATUS #5 CONDITIONAL-GO→DEFER 확정.

## 2. 대체 5번째 후보 탐색 (웹 검증)

**핵심 교훈:** velocity-ready 관건은 **SHARE-seq냐 10x Multiome이냐**. 10x Multiome(cellranger-arc possorted BAM 또는 fastq 재정렬)은 정상 nnz(BMMC 검증), SHARE-seq 저자 BAM은 실패. MultiVelo 논문의 multiome 데이터셋(E18 brain·skin·fetal brain=GSE162170·HSPC)은 이미 전부 사용/NO-GO → 5번째는 발생 아틀라스에서.

| 순위 | Accession | 조직/종 | velocity-ready | priming | 판정 |
|---|---|---|---|---|---|
| **1** | **GSE205117**(PRJNA843939) | 마우스 gastrulation E7.5–8.75, ~59k | ✅ GEX fastq 공개, **R1 16bp CB+12bp UMI(연속)+R2 90bp cDNA 확인** | **최강**(gastrulation) | **GO-feasible** |
| 2 | GSE246169 | 인간 발생 망막 | ⚠️ GEO RAW.tar만, BAM/loom 미확인 | 강 | 불확실 |
| 3 | GSE226108 | 인간 망막 성체+태아 | paired 서브셋 | 혼재 | 백업 |
| 4 | SEACells CD34(Zenodo 6383269) | 인간 골수 CD34+ | processed만, raw 미확인 | 강 | 후순위(조혈 중복) |
| 5 | fetal pancreas | 인간 태아 췌장 | RNA+별도ATAC(same-cell 아님) | 강 | 부적합 |

## 3. GSE205117 preflight (진행 중)

**GO-feasible 확인:** GEX run `SRR19450561` spot = R1 28bp(16 CB+12 UMI, **연속**) + R2 90bp cDNA + 2×10bp 인덱스. skin 실패요인(barcode 부재·비연속) **전부 해소**. → STARsolo `--soloType CB_UMI_Simple --soloFeatures Velocyto`로 spliced/unspliced 직산출 가능(cellranger-arc 불필요).

**실행:** `cross_dataset/run_gse205117_preflight.sh` (setsid detached). work `/home/kkkim/data/gse205117_preflight/`.
- 단계: A) fastq-dump 20M spot subset → B) STARsolo(mm10 index **재사용**, CB_UMI_Simple, whitelist None) → C) nnz(top-5000, macrophage 35.6% 대조).

### ✅ 결과(2026-07-11 19:45 DONE) — GO-feasible (자동 nnz "NO-GO"는 거짓 NO-GO)
STARsolo 요약:
- **Reads With Valid Barcodes 100%** (16bp CB 완벽 매칭) · **Genome mapping 95.1%**(unique 81%) · Gene 55.2%.
- **unspliced/spliced = 1,990,654/5,125,917 = 0.388 (39%)** → **건강한 velocity 신호**(intronic read 풍부). ← skin norg BAM엔 없던 바로 그 신호(skin은 nnz 0.02% + unspliced>spliced 비정상).
- nnz spliced 1.02%/unspliced 0.61%가 낮은 건 **깊이 아티팩트**: **Sequencing Saturation 9.9%**, Median UMI/Cell 1,105(cells 2,999) = full-depth의 ~1/10~1/20. 20M 서브셋(run 1개 881M의 2%, 전체 10run의 0.2%)이라 얕음. macrophage 35.6%는 full-depth 값이라 서브셋과 직접 비교 불가.
- **⚠️ 방법론 교훈:** nnz 절대값 임계(35.6%)는 depth-confounded — 서브셋/부분염색체엔 부적절(skin chr1 희석도 동일 함정). **feasibility 지표는 unspliced 비율 + barcode/mapping률**로 봐야 함.

### #2 깊이 bulletproof (60M 서브셋, 2026-07-11) — GO 확정
20M→60M(3배 깊이)에서 nnz가 비례 상승 → "낮은 nnz=depth 아티팩트" 입증:
| 지표 | 20M | 60M | 스케일 |
|---|---|---|---|
| Median UMI/Cell | 1,105 | 3,091 | 2.8배↑ |
| Saturation | 9.9% | 14.6% | ↑ |
| spliced nnz | 1.02% | 2.28% | 2.2배↑ |
| unspliced nnz | 0.61% | 1.46% | 2.4배↑ |
| unspliced/spliced | 0.388 | 0.312 | 안정(~0.3-0.4 건강) |
→ full-depth(881M=20M의 44배)면 nnz가 macrophage 35.6% 임계권 도달 예상.

### 판정: GSE205117 = **GO 확정** (5번째 cross-dataset 채택)
barcode 100%·mapping 95%·unspliced 비율 건강·nnz 깊이비례 → skin과 달리 velocity 재현 가능.

### full run 샘플 선별(논의 중)
WT 발생 timecourse에서 궤적 확보. multiome이라 GEX+ATAC 쌍 필요(다운·정렬 2배).
- **full B(4시점, 권장)**: E7.5 SRR19450575 · E8.0 SRR19450564 · E8.5 SRR19450560 · E8.75 SRR19450574 (+ATAC 4) ≈250-280GB. pseudotime 축 최강.
- B-lite(3시점): E8.0+E8.5+E8.75 ≈180GB. commitment 창.
- CRISPR KO 제외. 다운=aria2c 16연결 S3 병렬(memory sra-download-slow-aria2c-s3), 변환=fasterq-dump -e8.

### full B 다운로드 (진행 중, 2026-07-11 23:00~)
**확정 = full B (4시점 rep1, GEX+ATAC 각 4):**
| 시점 | GEX | ATAC |
|---|---|---|
| E7.5 | SRR19450575 | SRR19450572 |
| E8.0 | SRR19450564 | SRR19450569 |
| E8.5 | SRR19450560 | SRR19450557 |
| E8.75 | SRR19450574 | SRR19450555 |

- **드라이버:** `cross_dataset/dl_gse205117_fullB.sh` (setsid detached, PID 140283). work `/home/kkkim/data/gse205117_fullB/`(sra/·fastq/).
- **속도 현실:** aria2c 16연결 병렬도 ~7 MB/s(총 국제대역폭 한계, 병렬 무효). ~180GB → **~7시간(밤샘)**. resumable(aria2c --continue).
- **재개 확인:** `tail -20 dl_fullB.log; cat DL_PROGRESS; ls DL_DONE`. 중단 시 스크립트 재실행(idempotent, 완료분 skip).
- Phase1 aria2c 다운 → Phase2 fasterq-dump --split-files -e8 변환.

### 🌙 밤샘 자율 실행 상태 + 재개 (2026-07-12 05:xx, 3 프로세스 detached)
```
[147269] DL 8/8 완료 → fasterq 변환(dltools) 진행
[147295] GEX STARsolo Velocyto+QC ← DL_DONE 대기 → GEX_SOLO_DONE에서 멈춤(ATAC는 수동)
[159402] 결과 watcher → 각 단계 완료 시 RESULTS_SUMMARY.md에 결과+해석 자동 append
```
**재개 확인(다음 세션 최우선):**
```
cat /home/kkkim/data/gse205117_fullB/RESULTS_SUMMARY.md      # 자동 요약된 결과·해석
ls  /home/kkkim/data/gse205117_fullB/{DL_DONE,GEX_SOLO_DONE,DL_PARTIAL}
cat /home/kkkim/data/gse205117_fullB/gex_solo/QC_REPORT.txt  # 4 GEX 런 세포수·nnz
```
- 중단 시: `setsid bash cross_dataset/dl_gse205117_fullB.sh …`(완결분 skip) / `run_gse205117_gex_solo.sh`(DL_DONE 대기) / `watch_gse205117_results.sh` 각각 재실행.
- **핵심 다음 작업 = ATAC 처리(cellranger-arc) → GEX+ATAC 통합 → 다method fit → concordance를 `manuscript/PREREGISTRATION_gse205117.md` 6개 예측에 대조**(통과/실패 그대로, 사후구제 금지). GEX Velocyto는 RNA 측만이라 lag/α cross-method 검정엔 ATAC 필수.
- 논문 전략(방어 가능선)·사전등록·SNR 검정 = 커밋 `d52416c` 봉인. 전략 상세 `manuscript/STRATEGY_2026-07_elevation.md`.

### 후속 자동화 (무인 연쇄, 2026-07-12 기동)
**`cross_dataset/run_gse205117_gex_solo.sh`** (setsid detached, PID 142581) — **DL_DONE 대기 → GEX 4런 STARsolo Velocyto(full, CB_UMI_Simple, CellRanger2.2 세포필터) → filtered 세포 nnz QC → GEX_SOLO_DONE**.
- 확인: `cat /home/kkkim/data/gse205117_fullB/GEX_SOLO_PROGRESS; ls GEX_SOLO_DONE; cat gex_solo/QC_REPORT.txt`.
- ⚠️ **ATAC 처리·세포통합·P1~P3는 자동화 안 함**(설계·검증 필요, 미검증 heavy 무인실행 방지) → GEX_SOLO_DONE 리포트에서 멈춤. 다음 세션에 ATAC(cellranger-arc/chromap) 설계부터.
- nnz는 scv-preprocess python(scipy 정상) 사용.

### 다음: 처리 파이프라인 설계 (다운 완료 후)
- **GEX**(검증됨): fasterq-dump R1(barcode)+R2(cDNA) → STARsolo CB_UMI_Simple + Velocyto → spliced/unspliced.
- **ATAC**(설계 필요): 10x Multiome ATAC → 정렬(chromap/cellranger-arc)→fragments→peak/gene-activity + GEX 세포와 barcode 매칭. **cellranger-arc**(GEX+ATAC 조인트, gex_possorted_bam·peak·joint 세포호출 산출)가 표준이나 설치+mm10-arc ref(~10GB)+heavy. vs 수동(STARsolo+chromap+barcode 매칭). → MultiVelo 등이 요구하는 chromatin 입력 형태에 맞춰 결정.
- 통합 후 P1~P3 concordance(`run_macrophage` 패턴)로 'α-robust/lag-fragile' 재현.

### ⚠️ 도구 경로 (2026-07-12 정정)
- **aria2c + fasterq-dump/prefetch = `/opt/envs/dltools`** (다운로드 전용 env). STAR·velocyto·samtools = `/opt/envs/seqtools`. nnz = scv-preprocess python.
- **주의**: aspera-cli를 seqtools에 설치했다 remove했더니 **sra-tools까지 연쇄 삭제**됨(fasterq-dump 사라짐) → dltools에 재설치. seqtools의 scipy는 복구, velocyto.py는 llvmlite 이슈 잔존(full run엔 불필요).

### 밤샘 1차 실패·복구 (2026-07-12 02:37)
1차 밤샘(23:00~)이 2/8에서 깨짐: ①다운 3~8번 00:44경 transient 네트워크 blip으로 실패 ②fasterq-dump 부재(위 sra-tools 삭제) ③드라이버가 실패해도 DL_DONE 조기 생성 → GEX 오케스트레이터 빈 결과. → 드라이버 수정(완결성 게이트: 전부 complete여야 DL_DONE, 파일당 5회 재시도, 미완결시 DL_PARTIAL)·sra-tools 복구·sentinel 정리 후 재기동. 재기동 속도 ~25MB/s(경쟁 없어 빠름).

**다음(heavy, 사용자 승인):** full run = 전 GEX run(~400GB) STARsolo Velocyto(또는 cellranger-arc) → 세포 화이트리스트 교집합 → P1~P3 concordance(`run_macrophage` 패턴)로 'α-robust/lag-fragile' 재현 검정. 5번째는 선택(4-vs-4+profile-likelihood로 이미 충분), priming 극대(gastrulation) 헤드라인 강화용.

## 4. 세션 상태(2026-07-11, 중단 대비) — infra/env 요약

- **협업 JupyterLab 복구**: `~/start_collab_jupyter.sh`(--ip=0.0.0.0, -L 목적지=kkkim 컨테이너IP, setsid+중복가드). 접속 정본=직접접속 @121.126.38.195. Confluence 44859462 v7 + SCRUM-5 댓글.
- **conda env 대청소**: bmmc-recover+중복 삭제(~23GB), star+sratools+velocyto→seqtools, mv/tf/torch→velo-*(GPU·훅 보존), velocity 5종 전부 /opt/envs. lock.yml 4개. git `8333474`까지 push. (spatialpatho=BIOP02, 이후 BIOP02가 /opt 이동)
- **미확인**: /opt 컨테이너 간 공유 마운트 여부(팀원 `ls /opt/envs` 확인 대기).
- **문서**: git `docs/SHARED-INFRA-GUIDE.md`(canonical). memory: collab-jupyter-container-ip-access, tf-env-celldancer-conflict, confluence-mcp-1000char-limit.
