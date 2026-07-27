# Scope — epigenomic lag

- Owner: jmryu
- Issue: BIOP01-19 (2주차 과제 — Insight Agent)
- 작성일: 2026-07-27

## 주제

single-cell multi-omic velocity model이 chromatin accessibility와 transcription 사이의 **시간차(lag)** 를 어떻게 정의하고 추정하는가, 그리고 그 lag를 예측 대상으로 쓸 수 있는가.

## 키워드

`multi-omic velocity`, `RNA velocity`, `chromatin accessibility`, `ATAC-seq`, `priming`, `decoupling`, `latent time`, `pseudotime`, `c-s lag`, `relay velocity`, `single-cell multi-omics`

## 포함 기준

1. 같은 cell에서 RNA와 chromatin accessibility를 동시에 측정한 데이터(10x Multiome, SHARE-seq, SNARE-seq)를 다룰 것
2. chromatin과 RNA의 **시간 관계**를 model 내부에서 명시적으로 다룰 것 (단순 correlation 분석은 제외)
3. method를 제안하는 논문일 것 (application-only 논문 제외)
4. peer-reviewed journal 게재본일 것 (preprint 제외)

## 제외 기준

- RNA-only velocity method (scVelo, cellDancer, VeloVI 등) — 단, 비교 baseline으로는 인용함
- chromatin accessibility를 velocity의 보조 feature로만 쓰고 시간 관계를 모델링하지 않는 방법
- multi-omic integration만 다루고 dynamics를 추정하지 않는 방법 (Scanorama, scVI, MultiVI 등) — baseline으로만 인용

## 선정 논문 (3편)

| ID | 논문 | 연도 / Venue | 선정 이유 |
|---|---|---|---|
| `multivelo` | Multi-omic single-cell velocity models epigenome-transcriptome interactions and improves cell fate prediction | 2023, Nature Biotechnology | chromatin을 velocity ODE에 통합한 최초 계열. priming/decoupling 개념의 출처 |
| `multivelovae` | Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE | 2025, Nature Communications | MultiVelo의 discrete state를 continuous factor로 일반화. 같은 연구실 후속 |
| `moflow` | Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states | 2026, Nature Communications | latent time 자체를 제거하고 signed lag를 신호로 해석. 독립 그룹의 반론 |

세 편은 모두 `analysis/epigenomic-lag/<paper-title>/full.md`에 개별 분석이 완료되어 있다.

## 제외한 후보

- **cellDancer** — local relay velocity를 도입했으나 transcriptome-only. 포함 기준 1을 만족하지 않음. MoFlow의 직접 선행 연구이므로 Field Flow에서 맥락으로만 언급한다.
- **SHARE-seq 원 논문 (Ma et al.)** — chromatin potential 현상을 처음 보고했으나 velocity model을 제안하지 않음. 포함 기준 3 미충족. MultiVelo의 Wnt3 분석이 이 논문을 재현 대상으로 삼는다.

## 한계

논문 3편은 cross-paper insight를 만들기에 최소 규모다. 특히 Repeated Limitations는 3편 중 2편에서만 관찰돼도 "공통"으로 보일 위험이 있어, 각 항목마다 관찰된 편수와 예외를 명시한다.
