# scope — Insight Agent 대상 [BIOP01-15]

## 주제
single-cell RNA velocity로 **chromatin→transcription 타이밍(lag)과 kinetic rate**를 추정하는 method 계열. 우리 HSPC(GSE209878) 파이프라인 method 선택·해석의 근거.

## 키워드
RNA velocity, multiome (RNA+ATAC), chromatin accessibility, cell-specific kinetics, latent time, splicing/degradation rate, benchmark.

## 포함 (9편, `paper_analysis/epigenomic-lag/`)
multivelo(li-2023) · multivelovae(li-2025) · moflow(hong-2026) · crakvelo(el-kazwini-2026) · celldancer(li-2023) · deepvelo(cui-2024) · deepkinet(mizukoshi-2024) · mmvelo(nomura-2024) · velocity-benchmark(luo-2026).

## 제외
- 순수 trajectory/pseudotime(velocity 무관), spatial-only, 리뷰 논문.
- 기준: velocity ODE 또는 kinetic-rate 추정을 제시하지 않으면 제외.

## 산출
`papers.jsonl`(비교 records) → `comparison_table.md` → `evidence_bundle.md` → `insight.md`(4관점).
