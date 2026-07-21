# Methodology Brief — li-2023-multivelo

## 한 줄 결론 (모든 독자)
- Citation: `@li2023multivelo`  |  Importance: `상` — HSPC 10x Multiome pipeline에 *바로 차용 가능* + epigenomic-lag topic의 foundational reference.
- 한 문장 결론: scVelo dynamical 모델의 transcription rate를 `α^(k) · c(t)`로 확장해 chromatin–RNA *priming/decoupling lag*를 latent time scale에서 정량하는 첫 multi-omic velocity 알고리즘. 우리 HSPC multiome에 즉시 적용 가능.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` (mouse skin GSE140203, human brain GSE162170, ChIP-seq GSE70677, HSPC processed GSE209878) + `restricted` (HSPC raw FASTQ dbGaP phs002915.v1.p1). 10x mouse brain은 10x Genomics 공식 dataset.
- 코드 공개: https://github.com/welch-lab/MultiVelo (PyPI, Bioconda) — license `검토필요: GitHub LICENSE 확인 (MIT 추정)`, maintenance `active` (Welch lab flagship).
- 자원 요구: CPU only, Intel i7-9750H 12-thread + 32 GB RAM 기준. Mouse brain 40 min / Mouse skin 69 min / HSPC 124 min / Human brain 40 min. Peak memory 0.9-2.9 GB (dataset에 따라). GPU 불필요.
- 핵심 의존성: `scanpy`, `scVelo` (post-fitting reuse), `Seurat V4` (WNN smoothing, R), `Signac` (peak processing), `chromVAR` (motif), `numba` (JIT 가속), `scipy.optimize` (Nelder–Mead).
- 자세히 → [li-2023-multivelo_core.md](li-2023-multivelo_core.md) §Methods, [sources/li-2023-multivelo.pdf](sources/li-2023-multivelo.pdf) §Methods (p11–26), [sources/li-2023-multivelo-supp-1-info.pdf](sources/li-2023-multivelo-supp-1-info.pdf) §S2

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: *완전 일치* — 우리 HSPC 10x Multiome이 본 paper의 HSPC dataset과 동일 platform, 동일 modality (RNA + ATAC).
- 자원 가능성: 우리 워크스테이션 (32 GB RAM, GPU optional)으로 *바로 실행*. 팀 역량 (scanpy/scVelo 경험) 충분.
- 비용·시간 추정: 우리 HSPC dataset 적용 *2주 sprint* — install (1일), preprocessing (3일), fit (2시간), 결과 해석/시각화 (3일), 사내 review (3일).
- ROI 한 줄: 우리 epigenomic-lag 분석의 *baseline + foundational tool*. 후속 비교 (MultiVeloVAE, chromatin velocity)의 starting point 확보.
- 자세히 → [li-2023-multivelo_lens-industry.md](li-2023-multivelo_lens-industry.md) §3 (BD value & 상용화), §4 (전문가 코멘트)

## 본인 재회고 (본인)
- `질문: 우리 HSPC dataset에 적용 시 cell cycle confound 어떻게 처리? regress-out으로 충분? non-cycling subset separate fit ablation 필요?`
- `질문: MultiVeloVAE (Gao 2024) 등 후속 multi-omic velocity tool과 비교 시 어느 것이 우리 use case에 최적?`
- 다음 액션: **우리 HSPC dataset에 MultiVelo 실행 — 다음 sprint (2주)**. 결과로 M1/M2 gene list + priming/decoupling 시간 분포 + velocity stream을 산출해 R&D 리뷰에 발표.
- 자세히 → [li-2023-multivelo_lens-academic.md](li-2023-multivelo_lens-academic.md) Final Takeaways, [li-2023-multivelo_lens-industry.md](li-2023-multivelo_lens-industry.md) §4.4

---
마지막 갱신: 2026-05-22
