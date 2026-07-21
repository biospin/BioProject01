# Methodology Brief — li-2025-multivelovae

## 한 줄 결론 (모든 독자)
- Citation: `@li2025multivelovae`  |  Importance: `상` — MultiVelo의 *discrete state + single sample* 한계를 *continuous + multi-sample + Bayesian differential test*로 일반화한 framework. 우리 HSPC 10x Multiome pipeline의 직접 후속 / 대체 후보.
- 한 문장 결론: MultiVelo (`@li2023multivelo`)의 4 state ODE를 cVAE + cell-specific continuous (k_c, ρ) + shared latent time + 부분-overlap modality로 확장하고, Bayesian differential dynamics test + in silico TF perturbation을 추가한 multi-omic RNA velocity framework. 우리 HSPC + 추가 sample 통합 분석에 즉시 적용 가능.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` (신규 EB + HSPC + macrophage processed → GEO **GSE284047**, post-processed AnnData → figshare DOI 10.6084/m9.figshare.30280333) + `restricted` (raw FASTQ → dbGaP **phs002915.v2.p1**). MultiVelo의 mouse brain/skin/HSPC/human brain AnnData는 `@li2023multivelo`와 동일하게 재사용.
- 코드 공개: https://github.com/welch-lab/MultiVeloVAE — license **BSD-3-Clause** (commercial 사용 허용, copyright notice 유지), PyPI 설치 가능, Zenodo archive DOI 10.5281/zenodo.17268254, maintenance `active` (Welch lab flagship).
- 자원 요구: **GPU 필수** (개발 환경: Intel i3-12100F + NVIDIA RTX 3060 12 GB VRAM + 64 GB RAM, Arch Linux). Fig. 3h에서 MultiVelo 대비 *significantly faster* (정확 minute 미보고). 100k+ cell scaling 시 추가 batch training 필요 예상.
- 핵심 의존성: `pytorch` + CUDA (GPU 가속), `scanpy`, `anndata`, `scVelo` (preprocessing), `STARsolo` (alignment, ref. 70), `scIB` (integration benchmark), `Scenic+` (GRN 분석, ref. 42), `CellRank` (fate probability, ref. 32), `chromVAR` / `ChromHMM` (peak annotation).
- 자세히 → [li-2025-multivelovae_core.md](li-2025-multivelovae_core.md) §Methods, [sources/li-2025-multivelovae.pdf](sources/li-2025-multivelovae.pdf) §Methods (p14-21, Eq. 4-28)

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: *완전 일치* — 우리 HSPC 10x Multiome이 본 paper의 HSPC dataset과 *동일 platform + 동일 modality* (RNA + ATAC). cVAE multi-sample inference로 우리가 추가 donor / 추가 condition 확보 시 *바로 통합 분석* 가능.
- 자원 가능성: GPU 환경 *필수* — 우리 워크스테이션 GPU 보유 여부 확인 필요 (`질문:` 표시). 미보유 시 cloud GPU 또는 hardware upgrade 필요. 팀 역량 (scanpy / PyTorch / scVI 경험)으로 운영 가능.
- 비용·시간 추정: 우리 HSPC dataset 적용 *2-3주 sprint* — install + GPU 환경 검증 (2일), preprocessing (3일), fit (수 시간 GPU), 결과 해석 + MultiVelo 비교 (5일), 사내 review (3일).
- ROI 한 줄: 우리 epigenomic-lag 분석의 *직접 upgrade*. MultiVelo의 cell-type-specific 한계 해소 + 향후 multi-sample 통합 / differential dynamics test / in silico perturbation 같은 *MultiVelo로 불가능했던 분석* 가능.
- 자세히 → [li-2025-multivelovae_lens-industry.md](li-2025-multivelovae_lens-industry.md) §3 (BD value & 상용화), §4 (전문가 코멘트)

## 본인 재회고 (본인)
- `질문: 우리 HSPC dataset에 적용 시 cell cycle confound 어떻게 처리? MultiVelo와 동일하게 RNA에서만 regress out? cell cycle phase별 separate fit ablation 필요?`
- `질문: 우리 워크스테이션의 GPU (RTX 3060 12 GB 이상?) 보유 여부 + VRAM 확인. 100k+ cell scaling 시 batch training 전략?`
- `질문: MultiVeloVAE의 continuous (δ, κ)가 MultiVelo discrete 4 state와 어떤 confusion matrix? 두 method 동시 운영 가치?`
- 다음 액션: **우리 HSPC dataset에 MultiVeloVAE 실행 + MultiVelo와 head-to-head 비교 — 다음 sprint (2-3주)**. 결과로 cell-type-specific (δ, κ) gradient + MultiVelo 4 state assignment confusion matrix + runtime 비교 + lineage hierarchy 정확성을 산출해 R&D 리뷰에 발표.
- 자세히 → [li-2025-multivelovae_lens-academic.md](li-2025-multivelovae_lens-academic.md) Final Takeaways, [li-2025-multivelovae_lens-industry.md](li-2025-multivelovae_lens-industry.md) §4.4

---
마지막 갱신: 2026-05-25
