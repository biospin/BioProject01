> 출처: 이 분석 하네스(`AGENTS.md` + `skills/`)는 **박상준(@poqopo) `Harness_Baseline`** 에서 반입해 BioProject01 `kkkim-pipeline`(실제 파이프라인 실행)에 맞게 적용함. 원저작자 박상준 (원 repo LICENSE 미지정 — 공유·수정은 박상준 동의 전제). HSPC는 `pipeline/hspc-velocity-benchmark/` 실행 구현과 연결.

# AGENTS.md

이 저장소는 single-cell multi-omic 또는 time-resolved ATAC/RNA 데이터로 gene-specific epigenomic lag structure를 분석하는 작업 공간입니다. 핵심 목표는 chromatin accessibility 변화와 transcription 변화 사이의 시간차를 정량화하고, 이 lag structure가 perturbation 또는 epigenetic drug response timing을 예측하는지 검증하는 것입니다.

## Project Frame

- Chromatin accessibility와 transcription 사이의 lag은 gene마다 다르다.
- Promoter/enhancer accessibility, histone marks, TF occupancy, regulatory architecture는 activation lag과 shutdown lag의 크기를 설명할 수 있다.
- Gene-specific lag structure는 perturbation 또는 epigenetic drug에 대한 gene-level response timing 예측 변수로 검증한다.
- 기존 Model 1/Model 2 이분법은 gene-specific kinetic spectrum으로 확장해서 해석한다.

## Lag Definitions

- `activation lag` 또는 `priming time` = `transcription onset time - chromatin opening time`
- `shutdown lag` 또는 `closing lag` = `chromatin closing time - transcription shutdown time`
- `Model 1-like`: chromatin 변화가 먼저 일어나고 transcription 변화가 뒤따르는 패턴
- `Model 2-like`: transcription 변화가 먼저 일어나고 chromatin 변화가 뒤따르는 패턴

Lag은 기본적으로 연속형 값으로 다루고, 필요할 때만 short/long lag class로 이산화합니다. 시간축은 pseudotime, real time, inferred switch time, DTW alignment time 중 무엇인지 항상 명시합니다.

## Analysis Priorities

1. Gene별 chromatin opening, transcription onset, transcription shutdown, chromatin closing time을 추정하거나 입력으로 받는다.
2. Gene-specific activation lag과 shutdown lag을 계산하고 confidence, uncertainty, missingness를 함께 남긴다.
3. Baseline epigenomic features로 lag structure를 예측하는 모델을 만든다.
4. 예측된 lag structure와 실제 perturbation/drug response timing의 관계를 분리해서 검증한다.

Baseline gene-level feature는 promoter/enhancer accessibility, H3K27ac, H3K27me3, H3K4me3, TF occupancy 또는 motif score, peak-to-gene linkage, CpG density/promoter class를 우선 고려합니다.

## Required Metadata

Feature, label, 결과를 만들 때 다음 정보를 기록합니다.

- genome build와 gene annotation source
- promoter/enhancer 정의와 peak-to-gene 연결 기준
- 입력 데이터 형식, sample metadata, replicate 여부
- time/trajectory definition, lineage 또는 cell state annotation
- cutoff, sample/group 정의, missingness 처리 방식

## Reference Frame

- MultiVelo, Nature Biotechnology 2023: chromatin/RNA switch time, Model 1/Model 2, priming interval, decoupling interval
- MultiVeloVAE, Nature Communications 2025: continuous, lineage-specific chromatin/RNA dynamics
- MoFlow, Nature Communications 2025/2026 record: gene별 DTW 기반 chromatin-vs-spliced RNA lag와 asynchronous timing

참고 연구 재현에 머무르지 말고 activation lag과 shutdown lag이라는 통일된 kinetic variable로 재구성합니다. 외부 데이터셋, accession, portal URL, 사용 조건, 파일 형식은 분석 시점에 공식 출처로 확인합니다.

## Dataset Routing

Dataset-specific workflow는 `skills/ROUTES.md`에 위임합니다.

1. Dataset 작업 요청이면 먼저 `skills/ROUTES.md`를 읽습니다.
2. Dataset을 먼저 고르고, 그 다음 task type을 고릅니다.
3. `skills/<dataset>/<task>/SKILL.md`를 사용합니다.
4. Cross-dataset 작업에서는 dataset별 genome build, annotation, time axis, lineage/cell state, lag definition, uncertainty를 정렬한 뒤 비교합니다.

## Repository Conventions

- `data/`: 입력 데이터 또는 원본 데이터 위치 안내
- `metadata/`: sample sheet, cell annotations, comparison design, genome build 정보
- `scripts/`: 재사용 가능한 분석 스크립트
- `results/`: 최종 결과 테이블, 그림, 리포트
- `work/`: 중간 산출물

대용량 생물정보 파일은 원본을 덮어쓰지 않고 `results/`, `outputs/`, `work/` 같은 산출물 경로를 사용합니다.

## Tooling And Reporting

- 파일 탐색은 `rg`와 `rg --files`를 우선 사용합니다.
- 기존 스크립트나 설정이 있으면 새로 만들기 전에 먼저 읽고 같은 스타일로 수정합니다.
- FASTQ/BAM/BED/bigWig/MTX/H5AD/H5MU 파일은 가능한 경우 헤더, shape, obs/var metadata, 일부 레코드를 확인합니다.
- 모델 성능은 accuracy보다 ranking, calibration, held-out lineage/dataset generalization, early-vs-late response separation을 중점적으로 평가합니다.
- 결과 보고에는 변경 파일, 실행 명령, 검증 결과를 간단히 포함합니다.
- 생물학적 해석은 데이터와 모델이 지지하는 범위 안에서만 작성하고, 불확실한 부분은 명확히 표시합니다.
