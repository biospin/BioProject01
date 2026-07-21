# Ma 2020 — SHARE-seq (chromatin potential) — Abstract Analysis

- **Source**: PubMed abstract (`sources/abstract.txt`, PMID 33098772). 본 분석은 abstract만 근거. 본문/Figures/Methods 미참조 — full PDF drop 후 `<paper-id>_core.md` 별도 생성 예정.
- **분석 일자**: 2026-05-26.

## Abstract Summary

- **한 문장 요약**: SHARE-seq (single-cell paired ATAC + RNA) 방법을 개발해 mouse skin 34,774 cells의 joint chromatin-transcriptome 프로파일을 만들고, "chromatin potential"이라는 정량 metric으로 chromatin priming이 gene expression을 *시간적으로 선행*함을 입증.
- **연구 목적**: scalable한 single-cell multi-omics platform을 만들고, 이를 사용해 chromatin accessibility 변화가 lineage commitment를 *선행하는지* 실험적·계산적으로 검증.
- **문제 또는 gap**:
  - Differentiation은 asynchronous process → 기존 cross-sectional snapshot으로는 regulatory event의 *temporal order*를 직접 추론하기 어려움.
  - Unimodal scRNA-seq 또는 scATAC-seq를 별도로 측정하면 *같은 cell*의 chromatin–RNA 관계가 손실됨.
- **핵심 방법**:
  - SHARE-seq (simultaneous high-throughput ATAC and RNA expression with sequencing) — 한 cell에서 ATAC + RNA 동시 측정.
  - cis-regulatory interaction 정의를 위한 computational strategy 도입.
  - DORC (domains of regulatory chromatin) — peak 밀도가 높은 regulatory region 군집을 단위로 정의.
  - chromatin potential — chromatin lineage-priming을 정량화하는 metric (정의의 수학적 형태는 abstract에 없음 — 미제공).
- **주요 결과**:
  - 34,774 joint profiles from mouse skin (정확히는 hair follicle 포함된 skin tissue — abstract에 "mouse skin"이라고만 명시. 외부 맥락: 본 프로젝트 Dataset 2 = GSE140203, hair follicle lineage가 중심임).
  - DORC가 super-enhancer와 *유의하게 overlap* (구체적 p-value는 abstract에 없음).
  - Lineage commitment 동안 *DORC의 chromatin accessibility가 gene expression을 선행* → chromatin priming의 직접 증거.
  - chromatin potential이 cell fate outcome을 예측 (어느 정확도인지는 abstract에 없음).
- **저자가 주장하는 기여**:
  1. SHARE-seq platform — *extensible*, 다양한 tissue에 적용 가능.
  2. DORC 단위 정의 (super-enhancer overlap).
  3. chromatin potential 정량 metric.
  4. cell fate prediction 응용.

## 추출 규칙 적용

- **모호한 주장**: "significantly overlap" — 통계량 abstract에 없음; "applicable to different tissues" — abstract 단계에서는 입증되지 않은 일반화 주장 (mouse skin 1 종류만 보고된 것으로 보임 — 본문 확인 필요).
- **Abstract에 명시되지 않음**:
  - chromatin potential의 수학적 정의 / 입력/출력.
  - DORC 정의의 정량 기준 (peak density threshold 등).
  - cell fate prediction의 baseline 대비 정확도.
  - replicate 수, technical noise 수준.
  - 다른 tissue에서의 검증 여부.
- **Abstract 외부 맥락**:
  - 본 프로젝트 Dataset 2의 GEO accession은 GSE140203 (paper-info.yaml `data` 참조).
  - 이 paper의 "chromatin potential" 개념은 MultiVelo (Li 2023) 등 후속 multi-omic velocity work의 직접적 motivation. `analysis/epigenomic-lag/li-2023-multivelo/li-2023-multivelo_core.md`에서 "선행 접근 D — single-cell epigenome velocity (Ma 2020 SHARE-seq chromatin potential ...)"로 인용됨.
  - Cell paper paywall — full PDF 자동 fetch 실패 (`fetch_sources.py` log 참조). PMC7669735 NIHMS manuscript 또한 직접 URL이 HTML landing으로 redirect.

## 후속 작업 (PDF 입수 후)

- `ma-2020-shareseq_core.md` 작성: Background / Methods (SHARE-seq protocol, DORC 정의, chromatin potential 수식) / Results (mouse skin cell typing, lineage trajectory) / Figures / Tables.
- 본 프로젝트 관점에서 우선 확인할 것:
  1. chromatin potential의 수학적 정의와 *시간 단위*가 무엇인지 (pseudotime?  wall-clock?).
  2. lineage commitment 검증에 쓴 cell type / gene 수.
  3. epigenomic-lag (chromatin → RNA) 정량의 *최초* paper로서, MultiVelo와의 method 차이를 명시적으로 추출 (Ma 2020 = descriptive metric, MultiVelo = generative ODE).
  4. 후속 paper들이 GSE140203에서 *어떤 cell subset*을 reuse하는지 (full 34k vs subset).
