# 사전등록 — GSE205117(마우스 gastrulation) 5번째 cross-dataset 재현 검정

> **봉인 시점: 2026-07-12.** GSE205117의 어떤 velocity fit·cross-method concordance도 산출 전(현재 GEX fastq 처리 중, ATAC 미처리, 어떤 α/lag도 없음). 이 예측은 진짜 held-out이다. **커밋 해시가 시점을 봉인한다.**
> 성격: 이미 4개 시스템(HSPC·human_brain·E18·BMMC·macrophage)에서 본 'α robust / lag fragile' 순서의 **5번째 사전등록 확증(confirmatory replication)**. discovery 아님(정직 표기, advisor). 강화점 = **priming 극대(gastrulation)에서도 fragile인가**.
> ⚠️ 폐기된 강한 예측: "profile-likelihood 곡률이 SNR 넘어 재현성 예측" — SNR 검정(`results/identifiability_vs_snr.md`)에서 방어 불가 판정 → 사전등록하지 않음.

## 검정 설계
- 데이터: GSE205117 full B (E7.5/E8.0/E8.5/E8.75 각 rep1, GEX+ATAC 10x Multiome). WT 발생 궤적.
- Method: 기존 벤치마크와 동일 — RNA-only floor(scVelo dynamical) + chromatin-aware(MultiVelo·MultiVeloVAE·MoFlow). ATAC로 chromatin 입력.
- 산출: within-dataset cross-method Spearman ρ (α, lag 각각) + cross-dataset(HSPC↔gastrulation) α·lag 재현. 기존 `p3_concordance.py`/`p3_crossdataset_concordance.py` 패턴.

## 봉인된 예측 (결과 보기 전 확정, falsifiable)
| # | 예측 | 사전 임계 | 근거(기존 4시스템) |
|---|---|---|---|
| 1 | **within-dataset cross-method α 재현** | Spearman ρ **≥ 0.50** | HSPC 0.88, 다른 시스템도 높음 |
| 2 | **within-dataset cross-method lag 재현** | Spearman ρ **≤ 0.15**(≈0) | 기존 −0.04~+0.08 |
| 3 | **α > lag 순서** | α ρ − lag ρ **≥ 0.35** | 전 시스템 성립 |
| 4 | **cross-dataset HSPC↔gastrulation** | cross α **> +0.2** 且 cross α > cross lag | E18 +0.32/+0.10, BMMC +0.55/+0.05 |
| 5 | **per-gene 재현 격차** | lag 불일치 median > α 불일치 median | HSPC 0.317 vs 0.078 |
| 6 | **priming 극대에서도 fragile** | gastrulation(강한 lineage priming)에서 #2·#3 성립 | 헤드라인 강화 |

> **결정 로그 — MoFlow arm 포함 확정 (2026-07-13, kkkim, 어떤 fit도 산출 전).**
> 예측5의 per-gene lag 불일치는 **HSPC 원정의(MultiVelo vs MoFlow)** 로 채점한다 — MV vs MultiVeloVAE 치환이 아니다(α는 원정의대로 MV vs VAE). `p2_moflow.py`로 `results/moflow_genes_gse205117.csv`를 산출하며, 채점기(`cross_dataset/p3_prereg_gse205117.py`)가 이 파일을 감지하면 자동으로 원정의로 채점한다(코드 분기 이미 존재). 이 결정은 GEX/ATAC fit이 하나도 없는 시점에 기록되어 held-out 무결성을 유지한다.

## 반증 기준 (틀리면 틀렸다고 보고 — 사후 구제 금지)
- **lag cross-method ρ ≥ 0.50** → "priming best-case에서도 fragile" **실패**. lag가 재현되면 우리 핵심 주장이 이 시스템에서 깨짐 → 정직 보고, 조건 좁혀 재서술(사후 α<0.5로 임계 낮추기 금지).
- **α cross-method ρ < 0.30** → α robustness 실패(전체 논지 약화) → 정직 보고.
- **α > lag 순서 역전**(lag ρ > α ρ) → 순서 가설 실패.
- 이 경우 skin(#5) DEFER처럼 **실패를 실패로** 처리한다.

## 해석 수준 명확화 (예측 불변)
- 이 검정은 "현행 velocity method로 lag가 재현되는가"이지 "lag 생물학이 부재"가 아니다. 더 깊은 seq·시간해상·대사표지가 나중에 lag를 식별가능케 할 수 있음 — 우리 주장은 **현재 method로 무엇을 믿을 수 있나**의 경계다.
- 메커니즘(§8)은 lag가 두 switch-time의 **차이라 저SNR + sloppy**임을 정직히 서술(식별가능성이 SNR 초월한다는 과주장 X — `identifiability_vs_snr.md`).

## 상태
- GSE205117 다운로드·GEX 처리 진행 중(밤샘). ATAC 처리·다method fit·concordance는 이후(며칠). **결과 산출 시 이 표의 각 예측에 대해 통과/실패를 그대로 기록.**
