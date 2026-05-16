# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

**Epigenetic Therapy 기반 Response Time 예측** — gene별 chromatin-transcription lag structure를 정량화하고, 이를 이용해 epigenetic drug에 대한 반응 시간을 예측하는 연구 프로젝트.

핵심 개념:
- `activation lag`: chromatin이 열린 뒤 transcription이 시작될 때까지의 시간
- `shutdown lag`: transcription이 꺼진 뒤 chromatin이 닫힐 때까지의 시간
- 목표: baseline epigenomic feature로 gene별 lag를 예측 → drug response timing 예측

연구 3단계 구조는 [guide/Epigenetic Therapy 기반 Response Time 예측.md](guide/Epigenetic Therapy%20기반%20Response%20Time%20예측.md)에 상세 기술되어 있음.

## 외부 협업 도구

- **Confluence**: Space key `VC`, 경로: 프로젝트 진행-AI전용 > 프로젝트#01
- **JIRA**: Space key `BIOP01`
- **Slack**: 각 멤버별 openclaw bot 사용

## 팀 & 데이터셋 담당

| 담당 데이터셋 | 담당자 | GitHub ID |
|---|---|---|
| 10x embryonic mouse brain | gglee (gklee) | Geongyu |
| SHARE-seq mouse skin | 박상준 | — |
| Human brain multi-ome | 전연수 / sjpark | sezinie000 |
| Human HSPC 10x Multiome | kkkim / jamie (jmryu) | kakyungkim / JamieLyu |
| 하네스 | braveji (ykji) | braveji18 |

## 주요 데이터셋

| Dataset | Accession | Data type |
|---|---|---|
| 10x embryonic mouse brain | 10x Genomics dataset page | 10x multiome |
| SHARE-seq mouse skin | GSE140203 | paired chromatin + RNA |
| Human brain multi-ome | GSE162170 | human multiome |
| Human HSPC 10x Multiome | GSE209878 | human multiome |

## 기술 스택 (예정)

Python 기반 bioinformatics 파이프라인. `.gitignore`는 Python 환경 기준으로 설정되어 있음.

핵심 라이브러리 (예상):
- **MultiVelo** — chromatin/RNA switch time 추정, Model 1/2 분류
- **MultiVeloVAE** — cell/gene-specific dynamics, decoupling factor
- **MoFlow** — DTW 기반 gene-specific chromatin-RNA lag 계산
- scRNA-seq 표준 스택: `scanpy`, `anndata`, `muon` (multiome)
- ATAC-seq: `snapatac2` 또는 `ArchR`

GPU가 MultiVeloVAE 재현에 필요함 (선택사항이 아님).

## 주요 방법론적 주의사항

1. **Pseudotime ≠ Wall-clock time**: Step 1–2의 lag는 pseudotime 단위, Step 3 검증은 실제 시간 단위. 변환 가능성을 별도 입증해야 함.
2. **Confound 통제 필수**: burst kinetics (mean expression + variance scaling), cell cycle phase를 covariate로 통제하지 않으면 lag estimate가 artifact일 수 있음.
3. **Multicollinearity**: promoter ATAC, enhancer ATAC, H3K27ac, H3K4me3, TF motif score는 강한 상관 → group lasso 등 regularized model 필요.
4. **ChIP-seq mismatch**: bulk ChIP (예: GSE70677)을 baseline feature로 쓸 때 cell type 해상도 손실 주의. multiome ATAC peak을 primary로 사용.
5. **Multiple testing**: gene 단위 가설 (수만 개) → BH correction 또는 permutation 기반 FDR.

## 리소스 요구사항

- RAM: 128GB
- 저장: 1–2TB (dataset당 raw + intermediate 200–500GB 예상)
- GPU: 1대 이상 권장
