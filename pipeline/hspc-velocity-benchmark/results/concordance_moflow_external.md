# P3 within-dataset cross-method concordance — MoFlow arm (외부 4종)

> 목적: lag-fragile leg에 **두 번째 method 쌍 MV×MoFlow** 추가(기존 MV×VAE 단독 한계 대응).
> paired bootstrap 95% CI: B=10000, seed=20260707. MV lag=fit_t_sw2−fit_t_sw1(구조적 양수),
> MoFlow lag=cs_lag_median, VAE lag=1/α_c−1/α. magnitude=|lag| rank(headline), signed=원값 rank.

## human_brain
| comparison | convention | Spearman ρ | 95% CI | n_shared | note |
|---|---|---|---|---|---|
| MV×MoFlow lag | magnitude | -0.052 | [-0.135, +0.029] | 551 |  |
| MV×MoFlow lag | signed | -0.028 | [-0.113, +0.056] | 551 |  |
| MV×VAE lag | magnitude | — | — | 0 | method(s) 없음 |
| MV×VAE lag | signed | — | — | 0 | method(s) 없음 |
| floor×MV alpha | alpha | +0.767 | [+0.719, +0.808] | 485 |  |
| MV×VAE alpha | alpha | — | — | 0 | method(s) 없음 |
| floor×VAE alpha | alpha | — | — | 0 | method(s) 없음 |

## e18_mouse_brain
| comparison | convention | Spearman ρ | 95% CI | n_shared | note |
|---|---|---|---|---|---|
| MV×MoFlow lag | magnitude | — | — | 0 | shared<10 |
| MV×MoFlow lag | signed | — | — | 0 | shared<10 |
| MV×VAE lag | magnitude | +0.057 | [-0.005, +0.118] | 1027 |  |
| MV×VAE lag | signed | +0.073 | [+0.014, +0.131] | 1027 |  |
| floor×MV alpha | alpha | +0.777 | [+0.748, +0.803] | 973 |  |
| MV×VAE alpha | alpha | +0.898 | [+0.882, +0.910] | 1027 |  |
| floor×VAE alpha | alpha | +0.810 | [+0.783, +0.834] | 1112 |  |

## GSE194122_bmmc
| comparison | convention | Spearman ρ | 95% CI | n_shared | note |
|---|---|---|---|---|---|
| MV×MoFlow lag | magnitude | -0.116 | [-0.228, -0.003] | 272 |  |
| MV×MoFlow lag | signed | +0.033 | [-0.084, +0.149] | 272 |  |
| MV×VAE lag | magnitude | -0.088 | [-0.205, +0.030] | 272 |  |
| MV×VAE lag | signed | +0.027 | [-0.089, +0.143] | 272 |  |
| floor×MV alpha | alpha | +0.820 | [+0.767, +0.860] | 232 |  |
| MV×VAE alpha | alpha | +0.906 | [+0.879, +0.925] | 272 |  |
| floor×VAE alpha | alpha | +0.851 | [+0.808, +0.883] | 244 |  |

## macrophage
| comparison | convention | Spearman ρ | 95% CI | n_shared | note |
|---|---|---|---|---|---|
| MV×MoFlow lag | magnitude | -0.025 | [-0.089, +0.041] | 871 |  |
| MV×MoFlow lag | signed | +0.014 | [-0.054, +0.083] | 871 |  |
| MV×VAE lag | magnitude | +0.074 | [+0.006, +0.141] | 871 |  |
| MV×VAE lag | signed | +0.211 | [+0.145, +0.280] | 871 |  |
| floor×MV alpha | alpha | +0.826 | [+0.795, +0.853] | 702 |  |
| MV×VAE alpha | alpha | +0.917 | [+0.902, +0.930] | 871 |  |
| floor×VAE alpha | alpha | +0.865 | [+0.840, +0.887] | 709 |  |

## caveat (필수)
- MV 4-state는 switch-time 단조정렬 → MV lag은 구조적 양수, sign 무정보 → **magnitude rank**가 headline.
- MoFlow velo 행렬은 재현성 높으나(run-to-run +0.9999) **cs_lag_median(DTW) 축 재현성 밴드는 별도로 느슨**
  (`moflow_runtorun_null.md` §5) → 단일-fit ρ 점추정을 신호로 과대해석 금지, CI로 판단.
- α leg(floor×MV×VAE)는 MoFlow가 α를 내지 않아 **불변** — 여기선 문맥용 재계산일 뿐 MoFlow가 강화하지 않음.
- human_brain은 VAE 미실행 → MoFlow가 이 데이터셋의 **첫** within-dataset lag 파트너(두 번째 아님).
- 각 replication 1 donor/샘플 — 강한 일반화 금지. BMMC는 shared gene 적어 CI 넓음.
