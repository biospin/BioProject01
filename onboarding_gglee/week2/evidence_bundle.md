# evidence_bundle — Insight 입력 [BIOP01-15]

각 관찰의 근거 위치(`paper_analysis/epigenomic-lag/<id>/*`). Insight agent는 이 번들 + papers.jsonl만 읽는다.

## E1. 계보 (field flow)
- scVelo dynamical → cellDancer/DeepVelo(RNA-only, latent-time-free, cell-specific DNN) → MultiVelo(chromatin-aware, discrete, latent time) → **분기**: MoFlow(latent-time-free chromatin DNN) & MultiVeloVAE(연속 cVAE·multi-sample). 근거: hong-2026-moflow_methodology-brief("MultiVelo post-extension 두 갈래 중 하나"), li-2025-multivelovae_methodology-brief("MultiVelo를 continuous+multi-sample로 일반화"), li-2023-celldancer_methodology-brief("MoFlow의 direct predecessor").

## E2. chromatin 기여의 인과 분리 부재 (반복 한계)
- CRAK-Velo: chromatin term ablation(k=0)이 없어 chromatin 통합 효과가 인과적으로 분리 안 됨(el-kazwini brief '본인 재회고'). veloBench: **MultiVelo를 rna_only=True로 실행**해 multi-omic(ATAC-on) 이득을 평가하지 않음(luo brief). → "chromatin이 실제로 lag를 만드는가"를 논문들이 직접 시험하지 않음.

## E3. confound·척도 (반복 한계)
- cell-cycle 처리: MultiVelo/MultiVeloVAE/MoFlow 모두 '재회고'에서 cell-cycle confound 처리 미명시로 질문 남김. pseudotime≠wall-clock: lag가 latent 단위 → drug timing(시간)으로 직접 환산 불가(multivelo brief).

## E4. 차별점 (differentiation)
- MultiVelo=기계론·CPU·foundational; MultiVeloVAE=연속·multi-sample·GPU·BSD-3; MoFlow=latent-time-free·backflow 해소; CRAK-Velo=region-level·동일 GSE209878 head-to-head; DeepKinet=검증 프레임워크(scEU/scNT); veloBench=scenario 권장(complex topology→DeepVelo/veloVI/LatentVelo).

## E5. 재현·라이선스 (실무)
- 다수 repo가 license 명시 부재('검토필요:'): MoFlow·cellDancer·MultiVelo(MIT 추정). 명확 상업 허용은 MultiVeloVAE(BSD-3). GPU 필수: MultiVeloVAE·MoFlow·DeepVelo. CPU 가능: MultiVelo·cellDancer.
