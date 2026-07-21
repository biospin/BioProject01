# REPRODUCE — HSPC velocity 벤치마크 헤드라인 수치 재현 번들

> 자동 생성: `scripts/make_repro_bundle.sh`. **에이전트 없이도** 아래 env·명령으로 헤드라인 산출물을 재생성하고 SHA-256로 대조한다.
> 규율: 재생성값이 아래 checksum과 다르면 드리프트 — 사람이 원인 확인(자동 PASS 신뢰 금지). 수치-원고 정합은 `scripts/check_manuscript_numbers.py`.

## 1. 환경(conda env lock — 결정론 고정)
- `env/scv-preprocess.lock.yml` — sha256 `9087623c4b07be34e25a65bf66db17c3307e363aa75546da72933a22472244d8`
- `env/velo-mv.lock.yml` — sha256 `e5d332f8b49b8ac45d0dd05bc844803031e606341db455c0d0dd03c1f0ca4733`
- `env/velo-torch.lock.yml` — sha256 `f86fd5703cd0fa00740ec903f043d6ea1dd7400d1dfc178ff47985c96a701742`
- `env/velo-tf.lock.yml` — sha256 `0e467b91f19f96803bd04650d81c29c3e4cc72fa40a6774a4149799d6da799dc`

## 2. 재생성 명령(결정론적 재계산 게이트)
```bash
cd pipeline/hspc-velocity-benchmark
# env: scv-preprocess
conda run --no-capture-output -n scv-preprocess bash -lc 'python p3_concordance.py ; python p3_crossdataset_concordance.py ; python p3_scrambled_null.py ; python cross_dataset/p3_prereg_gse205117.py'
# 재현성 대조:
bash scripts/make_repro_bundle.sh   # 이 표를 다시 생성해 checksum 비교
```

## 3. 헤드라인 산출물 checksum (SHA-256)
| 산출물 | SHA-256 | 비고 |
|---|---|---|
| `FINDINGS.md` | `90fa04dfc426e797…` |  |
| `concordance.md` | `32b34533529d2ff6…` |  |
| `scrambled_null.md` | `22383ceaf12ee896…` |  |
| `prereg_gse205117_scorecard.md` | `ad9c7d7fe4c0c38d…` |  |
| `sim_positive_control_multimethod.md` | `843ce5db6112a25d…` |  |
| `external_rate_validation_schwalb.md` | `09b32044f2e4cdbd…` |  |
| `profile_likelihood_identifiability.md` | `f2c732d3466b7047…` |  |
| `profile_likelihood_freed.csv` | `88e63be6c2c84a57…` |  |
| `multivelo_genes.csv` | `7564d500200e485e…` |  |
| `rna_only_dynamical_genes.csv` | `51066912ff41d015…` |  |
| `multivelovae_genes.csv` | `7c1e43cd4ec302a8…` |  |
| `moflow_genes_gse205117.csv` | `42e19ec78a61fe48…` |  |
| `multivelo_genes_gse205117.csv` | `0c25be28a6799525…` |  |

_생성 시각은 git 커밋으로 대신(결정론 위해 스크립트에 timestamp 미기록). 산출물이 갱신되면 이 스크립트를 다시 돌려 REPRODUCE.md를 재생성·커밋._
