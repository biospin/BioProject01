# Methodology Brief — hong-2026-moflow

## 한 줄 결론 (모든 독자)
- Citation: `@hong2026moflow`  |  Importance: `상` — `@li2023multivelo`(MultiVelo) post-extension의 *두 갈래 중 하나* (다른 하나 `@li2025multivelovae`). *latent-time-free + cell-specific kinetic + chromatin-aware DNN* 조합으로 backflow 해소 + epigenomic lag mechanism 정량.
- 한 문장 결론: MoFlow는 cellDancer (`@li2024celldancer`)의 *relay velocity cosine loss*에 chromatin scenario 양쪽 (open/close) 평가 + lower-loss 자동 선택 + 2-stage 학습을 추가한 multi-omic RNA velocity framework로, 우리 HSPC 10x Multiome pipeline의 *MultiVelo / MultiVeloVAE와 cross-validated baseline*으로 즉시 적용 가능.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` (4 dataset 모두 publicly available — Human Brain GSE162170, Mouse Skin GSE140203, 10x E18 Mouse Brain 10x dataset page, Human HSPC GSE209878). 신규 dataset 없음 — *MultiVelo (`@li2023multivelo`) preprocessed AnnData 그대로 재사용*.
- 코드 공개: https://github.com/AriHong/MoFlow — license `검토필요:` (paper Code availability 본문에 license 명시 없음). PyTorch Lightning, Demo notebooks 제공. Zenodo archive DOI 10.5281/zenodo.17666878.
- 자원 요구: **GPU 권장** — 본문 hardware 정보 `미제공:`. DNN architecture는 작은 편 (3-layer 64-48-32) — 소비자급 GPU (RTX 3060 12 GB 수준) 충분 추정. 100k+ cell scaling 정보 `미제공:`.
- 핵심 의존성: `pytorch` + `pytorch-lightning` + `scanpy` + `anndata` + `scvelo` + `velocyto` + `Seurat v4` (R, WNN smoothing) + `fastdtw` (Python DTW) + `DAVID` (web) + `GSEApy` (Python).
- 자세히 → [hong-2026-moflow_core.md](hong-2026-moflow_core.md) §Methods, [sources/hong-2026-moflow.pdf](sources/hong-2026-moflow.pdf) §Methods (p11–15, Eq. 1–33).

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: *완전 일치* — 우리 HSPC 10x Multiome이 본 paper의 HSPC dataset과 *동일 platform + 동일 modality* (RNA + ATAC). preprocessing은 Li 2023 (`@li2023multivelo`)과 동일하므로 *재사용 효율 최고*. 단 multi-sample 통합은 *지원 안 됨* — 별도 학습 후 post hoc 비교.
- 자원 가능성: GPU 환경 *권장* (필수 여부 본문 미명시). 우리 워크스테이션의 GPU 보유 여부 + VRAM 확인 필요. *MultiVeloVAE와 동일한 환경에서 운영* 가능 (둘 다 PyTorch 기반).
- 비용·시간 추정: 우리 HSPC dataset 적용 *2-3주 sprint* — install + GPU 환경 검증 (2일), preprocessing (2일, Li 2023과 동일 protocol), fit (수 시간 GPU), MultiVelo / MultiVeloVAE와 cross-validation 비교 (5일), 사내 review (3일).
- ROI 한 줄: 우리 epigenomic-lag 분석의 *cross-validated dual-method baseline*. MoFlow의 *latent-time-free + DAC + DTW lag*가 우리 outcome (gene별 chromatin–RNA lag 정량 + drug response timing 예측)과 1:1 mapping.
- 자세히 → [hong-2026-moflow_lens-industry.md](hong-2026-moflow_lens-industry.md) §3 (BD value & 상용화), §4 (전문가 코멘트)

## 본인 재회고 (본인)
- `질문: 우리 HSPC dataset에 적용 시 cell-cycle confound 처리? MoFlow 본문 미명시 — Li 2023 preprocessing 그대로 사용? 우리 cell-cycle regress out 결과 비교 필요?`
- `질문: 우리 워크스테이션의 GPU (RTX 3060 12 GB 이상?) 보유 여부 + VRAM 확인. paper 미명시.`
- `질문: MoFlow의 *cluster 10 polycomb/speckle 발견*이 우리 HSPC에서도 재현되는가? brain-specific 가설 vs general mechanism 가설 판별.`
- `질문: MoFlow의 m1/m2 score + MultiVelo discrete M1/M2 + MultiVeloVAE continuous (δ, κ) 셋의 *confusion matrix*? 세 method 동시 운영 가치 정량.`
- 다음 액션: **우리 HSPC dataset에 MoFlow + MultiVeloVAE 동시 실행 + MultiVelo와 head-to-head 비교 — 다음 sprint (2-3주)**. 결과로 ① 4-dataset CBDir matrix, ② cell-type-specific score (MoFlow 4 RNA state / MultiVeloVAE (δ, κ) / MultiVelo 4 state) confusion matrix, ③ cluster 10 재현 여부, ④ runtime / memory 비교를 산출해 R&D 리뷰에 발표.
- 자세히 → [hong-2026-moflow_lens-academic.md](hong-2026-moflow_lens-academic.md) Final Takeaways, [hong-2026-moflow_lens-industry.md](hong-2026-moflow_lens-industry.md) §4.4

---
마지막 갱신: 2026-05-25
