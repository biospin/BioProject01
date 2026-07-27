# comparison_table — velocity method 비교 [BIOP01-15]

| Method (연도, venue) | 유형 | Modality | 핵심 메커니즘 | 결과 주장 | 대표 한계 |
| --- | --- | --- | --- | --- | --- |
| MultiVelo (2023, Nat Biotech) | 기계론 ODE | multiome | α^(k)·c(t), 4-state, latent time | 최초 chromatin→RNA lag 정량 | discrete·single-sample, cell-cycle 미명시 |
| MultiVeloVAE (2025, Nat Comm) | cVAE+ODE | multiome | 연속 (k_c,ρ), multi-sample, Bayesian diff test | MultiVelo 한계 일반화 | GPU 필수, scaling 미검증 |
| MoFlow (2026, Nat Comm) | DNN, latent-time-free | multiome | relay cosine loss + open/close scenario 자동선택 | backflow 해소, lag 정량 | multi-sample 미지원 |
| CRAK-Velo (2026, Genome Biol) | semi-mech (UniTVelo) | multiome | accessibility=production rate + region weight | GSE209878서 MultiVelo 대비 우위 주장 | **chromatin ablation 없음** |
| cellDancer (2023, Nat Biotech) | DNN, latent-time-free | RNA-only | local cosine loss + gene DNN | 방향 정확도; MoFlow 전신 | chromatin 없음 |
| DeepVelo (2024, Genome Biol) | GCN | RNA-only | GCN + continuity loss | scVelo 대비 우위 | chromatin 없음, 30k cell 한계 |
| DeepKinet (2024, Genome Biol) | 2-stage VAE | RNA-only | splicing/degradation rate + scEU/scNT 검증 | kinetic-rate **검증 프레임워크** | chromatin 없음 |
| mmVelo (2024, bioRxiv) | multimodal VAE | multiome | multimodal latent dynamics | cross-modality velocity | preprint |
| veloBench (2026, Cell Rep Meth) | 벤치마크 | mixed | 15 method × 20 dataset | **단일 정답 없음**, scenario별 권장 | MultiVelo를 **ATAC off**로 실행 |

**한눈에**: chromatin-aware 4종(MultiVelo/VAE/MoFlow/CRAK-Velo)이 우리 HSPC 직접 적용 대상; RNA-only 4종은 baseline/계보/검증-프레임워크; 벤치마크는 method 선택의 3자 근거이나 multi-omic(ATAC-on) 성능은 **비워둠**.
