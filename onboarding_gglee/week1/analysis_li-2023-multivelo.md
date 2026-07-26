# 분석: Li 2023 — MultiVelo (SKILL 적용 샘플) [BIOP01-1]

*근거: `paper_analysis/epigenomic-lag/li-2023-multivelo/*` (methodology-brief, core §Methods p11–26).*

1. **주장 & 메커니즘**: scVelo dynamical 모델의 transcription rate를 `α^(k)·c(t)`(k=chromatin state, c=accessibility)로 확장해 **chromatin→RNA priming/decoupling lag**를 latent time 축에서 정량하는 첫 multi-omic velocity. 4-state ODE + Nelder–Mead 적합.
2. **New vs Borrowed**: (New) chromatin accessibility를 velocity ODE에 결합한 4-state 스위치 + priming/decoupling 시간. (Borrowed) scVelo dynamical의 spliced/unspliced ODE·latent time, Seurat WNN smoothing, Signac peak 처리.
3. **데이터 & 재현성**: dataset `open`(HSPC GSE209878 processed, mouse skin GSE140203, human brain GSE162170) + raw `restricted`(dbGaP phs002915.v1.p1). 코드 welch-lab/MultiVelo(PyPI/Bioconda, MIT 추정, active). **CPU only**, HSPC 124분/32GB, GPU 불필요. 의존성 scanpy·scVelo·Seurat v4(R)·Signac·numba.
4. **우리 적용성(HSPC)**: **완전 일치** — 본 논문 HSPC dataset = 우리 GSE209878, 동일 platform/modality. 워크스테이션에서 바로 실행. lag는 latent-time 축 산출(내장). → 우리 파이프라인의 **foundational baseline**.
5. **한계 & confound**: (a) **cell-cycle confound 처리 미명시** — regress-out 충분한지 불명. (b) **pseudotime≠wall-clock** — lag가 latent 단위라 drug timing(시간)으로 직접 못 씀. (c) **discrete 4-state + single-sample** — cell-type-specific 연속 kinetics·multi-donor 통합 불가(→ MultiVeloVAE가 해소). (d) chromatin 기여를 분리하는 ATAC-off ablation 없음.
6. **후속 질문**: ① cell-cycle regress-out vs non-cycling subset separate fit의 lag 차이? ② latent-time lag를 wall-clock으로 매핑할 anchor가 있나? ③ 후속(MultiVeloVAE/MoFlow)과 lag 방향이 gene 단위로 일치하나(cross-method consistency)?
