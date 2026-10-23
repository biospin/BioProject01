# priming 정의(t_sw1) 재계산: ATAC 셔플·MultiVelo 재적합 (machine output, do not edit)

> scripts/p18_priming_recompute.py. B=10,000, seed=20261023. 기존 입력 파일만 사용, 재적합 없음.

## S. ATAC within-lineage 셔플: 원본 vs 셔플 재적합

> 입력: results/multivelo_genes.csv, results/scrambled_genes.csv (공통 유전자 n=538). ρ의 95% CI는 유전자 bootstrap 10,000회.

| 정의 | n | per-gene Spearman ρ [95% CI] | MW p | KS p | Wilcoxon p | median 원본 → 셔플 | 상대변화 median | 0인 유전자(원본/셔플) |
|---|---|---|---|---|---|---|---|---|
| coupled_on | 538 | +0.721 [+0.656, +0.780] | 0.196 | 0.507 | 0.00029 | 5.868 → 5.475 | 14.7% | 0/0 |
| priming | 538 | +0.753 [+0.695, +0.806] | 0.651 | 0.460 | 0.00068 | 4.606 → 4.999 | 17.4% | 0/0 |

계약 검사 통과: coupled-on 정의 값이 scrambled_null.md(ρ 0.721, MW p 0.196, KS p 0.507)와 같다.

## B. MultiVelo 재적합 안정성 (12 × 70% 부분표본)

재적합 표가 없어 건너뛰었다(찾은 위치: `/Users/kkkim/projects/autobiox/BioProject01-pipeline/pipeline/hspc-velocity-benchmark/results/bootstrap_refit`). 이 표는 `.gitignore` 대상이라 HPC의 `results/bootstrap_refit/`에만 있다. 그곳에서 `--refit-dir`를 주고 다시 실행한다.

