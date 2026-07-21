#!/usr/bin/env bash
# BIOP01-41 SHARE-seq mouse skin(GSE140203) Phase0 preflight — 지용기 경로2 spec.
# 목표 2숫자로 GO/NO-GO: (1) SHARE-seq barcode 매칭률, (2) spliced/unspliced nnz(macrophage 35.6% 전례).
# ⚠️ 발견: GSE140203_RAW.tar = 처리 매트릭스뿐, fastq 없음 → raw fastq는 SRA에서(1 lane만).
# ⚠️ 이 드라이버는 deterministic 선행(STAR설치·mouse index·SRA fetch)을 무인 수행. barcode 재조립/STARsolo는
#    SHARE-seq 정확 offset 검증 필요 → best-effort로 시도하고 실패 시 로그에 명기(다음 세션 확인).
# 실행(detach): setsid bash run_skin_preflight.sh </dev/null >skin_preflight.log 2>&1 &
set -u
ROOT="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
CROSS="$ROOT/cross_dataset"; DATA="$ROOT/data"; RES="$ROOT/results"
CONDA="/home/kkkim/miniconda3/bin/conda"
REF="$DATA/ref/mm10"; IDX="$DATA/ref/mm10_star"; SKIN="$DATA/skin"; SRADIR="$SKIN/sra"
DONE="$CROSS/SKIN_PREFLIGHT_DONE"; FAILED="$CROSS/SKIN_PREFLIGHT_FAILED"; PROG="$CROSS/SKIN_PREFLIGHT_PROGRESS"
export TMPDIR="/home/kkkim/.tmp_skin"; mkdir -p "$TMPDIR" "$REF" "$IDX" "$SRADIR"
log(){ echo "[$(date '+%F %T')] $*"; }
hb(){ echo "stage: $1 ($(date '+%F %T'))" > "$PROG"; }
die(){ log "FAILED at $1: $2"; { echo "FAILED at $1"; echo "$2"; date; } > "$FAILED"; exit 1; }
rm -f "$DONE" "$FAILED"
log "=== skin preflight 시작 (PID $$, PPID $PPID) ==="

# ── A) STAR + sra-tools env (star 전용 env, idempotent) ──
hb "A STAR/sra-tools 설치"
if ! "$CONDA" run -n seqtools which STAR >/dev/null 2>&1; then
  log "[A] star env 생성(STAR + sra-tools, bioconda)"
  "$CONDA" create -y -n seqtools -c bioconda -c conda-forge star=2.7.11b sra-tools pigz >/dev/null 2>&1 \
    || die "A-env" "conda star env 생성 실패"
fi
STAR_BIN="$CONDA run -n seqtools STAR"; log "[A] STAR $("$CONDA" run -n seqtools STAR --version 2>/dev/null)"

# ── B) mouse mm10 genome + GTF 다운로드 + STAR index 빌드 (idempotent) ──
hb "B mouse genome+GTF+index"
FA="$REF/GRCm38.primary_assembly.genome.fa"; GTF="$REF/gencode.vM25.annotation.gtf"
if [ ! -f "$IDX/SAindex" ]; then
  [ -f "$FA" ] || { log "[B] genome fasta 다운로드(GENCODE GRCm38 vM25)"; \
    curl -fL --retry 3 -o "$FA.gz" "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M25/GRCm38.primary_assembly.genome.fa.gz" || die "B-fa" "genome fasta 다운로드 실패"; \
    pigz -d "$FA.gz" 2>/dev/null || gunzip "$FA.gz"; }
  [ -f "$GTF" ] || { log "[B] GTF 다운로드(GENCODE vM25)"; \
    curl -fL --retry 3 -o "$GTF.gz" "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M25/gencode.vM25.annotation.gtf.gz" || die "B-gtf" "GTF 다운로드 실패"; \
    pigz -d "$GTF.gz" 2>/dev/null || gunzip "$GTF.gz"; }
  log "[B] STAR genomeGenerate (mm10, ~1h·~30GB RAM)"
  $STAR_BIN --runMode genomeGenerate --genomeDir "$IDX" --genomeFastaFiles "$FA" \
    --sjdbGTFfile "$GTF" --sjdbOverhang 100 --runThreadN 12 --genomeSAsparseD 1 \
    --outTmpDir "$TMPDIR/star_gg" >/dev/null 2>&1 || die "B-idx" "STAR index 빌드 실패"
  log "[B] index 완료"
else log "[B] STAR index 존재 → skip"; fi

# ── C) skin RNA SRA run 해소 + 1 lane fetch ──
hb "C SRA skin RNA fetch"
# GSM4156608 = skin.late.anagen.rna. SRA run 해소(sra-tools prefetch는 SRR 필요) → NCBI eutils로 SRR 조회.
if ! ls "$SRADIR"/*.fastq* >/dev/null 2>&1; then
  log "[C] GSM4156608(skin RNA) → SRR 조회(NCBI eutils)"
  SRRINFO=$(curl -fsL "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term=GSM4156608&retmax=20" 2>/dev/null)
  UIDS=$(echo "$SRRINFO" | grep -oE '<Id>[0-9]+</Id>' | grep -oE '[0-9]+' | head -20)
  [ -n "$UIDS" ] || die "C-esearch" "GSM4156608 SRA UID 조회 실패(eutils)"
  RUNINFO=$(curl -fsL "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id=$(echo $UIDS|tr ' ' ',')&rettype=runinfo&retmode=text" 2>/dev/null)
  SRR=$(echo "$RUNINFO" | grep -oE 'SRR[0-9]+' | head -1)
  [ -n "$SRR" ] || die "C-runinfo" "SRR accession 해소 실패. runinfo=$(echo "$RUNINFO"|head -c 200)"
  log "[C] skin RNA run = $SRR → fasterq-dump --include-technical(SHARE-seq barcode=index read 필수; 1 lane 전량, GSE 전체 아님). fastq-dump는 --include-technical 미지원이라 fasterq-dump 사용."
  ( "$CONDA" run -n seqtools fasterq-dump "$SRR" --split-files --include-technical -e 8 -t "$TMPDIR" -O "$SRADIR" ) \
    || die "C-fetch" "fasterq-dump 실패($SRR) — sratools env·네트워크·디스크 확인"
  echo "$SRR" > "$SKIN/skin_rna_srr.txt"
  log "[C] fastq: $(ls "$SRADIR"/*.fastq* 2>/dev/null | tr '\n' ' ')"
else log "[C] fastq 존재 → skip"; fi

# ── D) SHARE-seq barcode 재조립(3×8bp→24bp)+UMI 10bp: best-effort, offset 검증 필요 ──
hb "D barcode 재조립"
log "[D] ⚠️ SHARE-seq barcode 재조립은 정확한 ligation-barcode offset(99bp index read 내 3×8bp 위치) 확정이 필요."
log "[D]    fastq read 길이/개수 진단만 수행하고, 재조립 스크립트는 다음 세션 검증으로 남긴다(무인 오조립 방지)."
for f in "$SRADIR"/*.fastq; do [ -f "$f" ] && log "[D]   $(basename $f): read len $(awk 'NR==2{print length($0); exit}' "$f") / reads $(($(wc -l < "$f")/4))"; done
{ echo "=== SKIN PREFLIGHT: 선행 완료, barcode/STARsolo 대기 ==="; date;
  echo "STAR env·mm10 index·SRA fastq 확보 완료. 다음: SHARE-seq barcode 재조립(offset 확정)→STARsolo(--soloCBlen 24 --soloUMIlen 10 --soloFeatures Velocyto)→nnz.";
  echo "fastq: $(ls "$SRADIR"/*.fastq 2>/dev/null|tr '\n' ' ')"; } > "$DONE"
log "=== 선행 단계 완료(STAR·index·SRA). barcode/STARsolo는 다음 세션. ==="
exit 0
