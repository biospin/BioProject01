# FIGURE_INVENTORY — Additional file 11 약속 대 실물 (2026-07-19, BIOP01-62)

> 목적: `manuscript/SUPPLEMENTARY.md`의 **Additional file 11**이 약속한 다섯 패널이 실제로 존재하는지 판정하고,
> 만들 수 있는 것은 실제로 렌더한 기록. **`manuscript/`·`results/`는 건드리지 않았다** — 새 파일은 전부 `figures/` 아래.
> 실행 환경: `~/miniconda3/envs/scv-preprocess/bin/python` (velocity env `velo-mv`는 이 서버에 **없음** — 아래 §1 참고).

---

## 0. 요약 판정

| 약속된 패널 | 판정 | 실물 |
|---|---|---|
| (1) per-dataset cross-method concordance scatter | **새로 만듦** | `figS01_per_dataset_concordance.{py,png}` |
| (2) 대표 stiff/sloppy 모수의 profile-likelihood 곡선 | **이미 있음**(재실행 검증 완료) | `fig05_profile_likelihood.{py,png}` |
| (3) ATAC-shuffle 대 관측 lag | **새로 만듦** | `figS03_atac_shuffle_lag.{py,png}` |
| (4) coupling shuffle 분포 | **새로 만듦** | `figS04_coupling_shuffle.{py,png}` |
| (5) α·γ stiffness-tertile ladder | **새로 만듦** | `figS05_stiffness_tertile_ladder.{py,png}` |

**"만들 수 없는 패널"은 없었다.** 다섯 종 전부 `results/`의 실제 산출물로 렌더된다.
다만 **약속 문구 두 곳이 실물보다 강하다** — (3)·(4)는 "귀무 *분포*"가 아니라 **셔플 1회 realization 겹쳐 그리기**다(§4 제안 문장에서 교정).

---

## 1. figures/ 조사 결과 — 기존 스크립트 3개 전부 실행됨

기존 png를 덮어쓰지 않도록 **스크래치패드에 심볼릭 링크 샌드박스**(`results/`·`scripts/`·`data/`만 링크)를 만들어 거기서 실행했다.

| 스크립트 | 실행 | 출력(재현된 수치) |
|---|---|---|
| `fig01_p2_concordance.py` | ✅ OK | `lag median 5.87, α-Spearman 0.82, timing-Spearman 0.04` |
| `fig05_profile_likelihood.py` | ✅ OK (패널 A–D **전부** 그려짐) | `ratio med 3.53x, alpha stiffer 95%` |
| `fig_blog_supplements.py` | ✅ OK | fig02·fig03·fig04 3장 재생성 |

- **fig05 주의사항 해소**: 스크립트 헤더는 "패널 D 재계산에 `velo-mv` env 필요"라고 적혀 있으나, 이 서버엔 `velo-mv`가 **없다**(`~/miniconda3/envs` = cms-r, scv-preprocess, spatialpatho). 실제로 돌려 보니 **scv-preprocess에서 패널 D까지 완주**한다(대표 유전자 TLE1, lag0=1.8pt). 헤더의 env 요구는 과한 기술이며, 저장소의 png는 유효하다. (안전을 위해 기존 png는 사전 백업 후 실행했고, **저장소 파일은 덮어쓰지 않았다**.)
- `figures/README.md` 규칙대로 png는 `.gitignore` 대상(`.gitignore:39 pipeline/**/figures/**/*.png`). 즉 **커밋되는 것은 스크립트뿐**이고, 투고 번들은 렌더해서 만든다.

### 이미 렌더돼 있던 png 8개의 정체

| png | 생성 스크립트 | 내용 | 용도 판정 |
|---|---|---|---|
| `fig01_p2_concordance.png` | `figures/fig01_p2_concordance.py` | HSPC 3패널: MultiVelo lag 분포 / floor×MV α scatter(ρ=0.82) / absolute timing scatter(ρ=0.04) | 본문·블로그용. **패널(1)의 HSPC 한 조각**이지만 5개 데이터셋 대조가 아니라 supp 패널(1)을 대신하지 못함 |
| `fig02_crossdataset_concordance.png` | `fig_blog_supplements.py` | dataset별 **cross-dataset**(HSPC↔외부) α vs lag 막대 3종 | 블로그 삽화. **cross-method가 아니라 cross-dataset** — 패널(1)과 다른 축 |
| `fig03_novelty_comparison.png` | `fig_blog_supplements.py` | MoFlow 대비 체크표(개념도, 데이터 아님) | 블로그 전용 |
| `fig04_harness_concept.png` | `fig_blog_supplements.py` | 하네스 개념도(데이터 아님) | 블로그 전용 |
| `fig05_profile_likelihood.png` | `figures/fig05_profile_likelihood.py` | A 곡률 violin(α vs lag) · B per-gene 강성비 · C lag 삼분류 · D 대표 유전자 profile 곡선 | **supp 패널(2) 그 자체** |
| `fig_sim_positive_control.png` | `scripts/p5_sim_positive_control_agg.py` | 합성 양성대조 heatmap 3종(SNR×W 격자) | supp 후보(약속엔 없음) |
| `lag_model.png` | `scripts/p5_lag_model.py` | baseline-only 예측 vs 실제(lag ρ=−0.21 / α ρ=−0.09) | supp 후보(약속엔 없음) |
| `sim_injected_lag.png` | `scripts/p5_sim_injected_lag.py` | 주입 lag 회수 시뮬(true vs recovered, 노이즈별 회수율) | supp 후보(약속엔 없음) |

> 즉 기존 8장 중 **약속된 다섯 패널에 해당하는 것은 fig05 하나뿐**이었다. Additional file 11의 현 서술은 실물보다 앞서 있었다.

---

## 2. 새로 만든 그림 (전부 `results/` 산출물에서 나옴, 숫자 조작 없음)

각 스크립트는 **결과 md에 이미 적힌 값과 재계산 값을 대조해 어긋나면 `SystemExit`으로 죽는 하드 게이트**를 갖고 있다.

### figS01 — per-dataset cross-method concordance scatter (패널 1)
- 파일: `figS01_per_dataset_concordance.py` → `figS01_per_dataset_concordance.png` (2455×947)
- 내용: 두 chromatin-aware arm(MultiVelo × MultiVeloVAE)의 **rank–rank scatter**, 데이터셋 5종 × 2행(위=α, 아래=lag 크기).
- 정의는 `cross_dataset/p3_concordance_macrophage.py`(A1/A2)와 동일: α=`fit_alpha` vs `vae_alpha`, lag=`|fit_t_sw2−fit_t_sw1|` vs `|1/vae_alpha_c − 1/vae_alpha|`, gene=`fit_likelihood` 유효 교집합.
- 재계산 대조 로그:

| dataset | n | α ρ (재계산 / md) | lag 크기 ρ (재계산 / md) |
|---|---|---|---|
| HSPC (GSE209878) | 538 | +0.882 / +0.882 ✅ | **+0.163 / (md에 값 없음 — 신규 계산)** |
| Macrophage | 871 | +0.917 / +0.917 ✅ | +0.074 / +0.074 ✅ |
| E18 mouse brain | 1027 | +0.898 / +0.898 ✅ | +0.057 / +0.057 ✅ |
| Human BMMC (GSE194122) | 272 | +0.906 / +0.906 ✅ | −0.088 / −0.088 ✅ |
| Mouse gastrulation (GSE205117) | 969 | +0.953 / +0.953 ✅ | −0.026 / −0.026 ✅ |

  - ⚠️ **HSPC lag 값 주의**: `results/concordance.md` §3.5는 같은 쌍에 대해 **부호 유지** 정의로 ρ=**−0.010**을 보고한다(재계산으로 −0.010 확인). 외부 4종과 축을 맞추려고 그림은 **크기(|lag|) 정의**를 썼고 그 값이 +0.163이다. 두 값은 서로 다른 정의이며 모순이 아니다. 본문에서 HSPC lag concordance를 인용할 땐 **어느 정의인지 명시**해야 한다(신규 계산치를 인용하려면 `results/`에 먼저 기록하는 편이 안전).

### figS03 — ATAC-shuffle 대 관측 lag (패널 3)
- 파일: `figS03_atac_shuffle_lag.py` → `figS03_atac_shuffle_lag.png`
- 입력: `results/multivelo_genes.csv`(관측) vs `results/scrambled_genes.csv`(ATAC within-lineage 셔플 후 재fit) — `scripts/p3_scrambled_null.py` 산출.
- A: 두 lag 분포 겹쳐 그림 + 중앙값. B: per-gene paired scatter.
- `results/scrambled_null.md`와 **9개 값 전부 일치**: n=538, median 5.868/5.475, MW p=0.1957, KS D=0.050 p=0.5074, paired Wilcoxon p=2.9e-04, per-gene Spearman 0.721, 상대변화 median 14.7%.
- ⚠️ **셔플 1회 realization**(seed `p2_config.RANDOM_SEED`). "귀무 분포"가 아니라 **셔플 분포 겹쳐 그리기**이고, 그 사실을 그림 부제에 박아 뒀다.

### figS04 — coupling shuffle (패널 4)
- 파일: `figS04_coupling_shuffle.py` → `figS04_coupling_shuffle.png`
- 입력: `results/coupling_per_gene.csv`(`coupling`, `coupling_shuffle0`) — `scripts/p7_coupling_lag_alternative.py` 산출.
- A: 관측 vs 셔플 coupling 분포. B: paired scatter. C: per-gene Δ 히스토그램.
- `results/coupling_lag_alternative.md`와 대조: real median **+0.126** ✅, 양수 비율 **87.2%** ✅, per-gene Δ median **+0.098** ✅, Δ>0 **75.3%** ✅.
- ⚠️ **p-value 출처 주의(중요)**: md의 `MW p=5.6e-75`는 스크립트가 **셔플 20회를 pool해서** 계산한 값이다(`p7_coupling_lag_alternative.py` L85-89, 로그 `[shuffle coupling] median(over 20)`). CSV엔 realization 0만 저장돼 있어 그것만으로 재계산하면 p=2.0e-40이 나온다. 그림은 **재계산하지 않고 md 값을 "20회 pooled, 인용"이라고 명시**해 표시한다. shuffle0 median은 +0.022(md의 pooled +0.021과 반올림 차이).
- 서사 정직성: 이 패널은 **coupling이 lag의 대체가 된다는 근거가 아니다.** md의 판정은 "인과 대조는 통과하나 **cross-dataset 재현 실패(ρ=+0.173, 사전선언 기준 |ρ|>0.2)**"이며, 그 문장을 그림 부제에 넣었다.

### figS05 — stiffness-tertile ladder (패널 5)
- 파일: `figS05_stiffness_tertile_ladder.py` → `figS05_stiffness_tertile_ladder.png`
- 입력: `results/curvature_tertile_validation.csv` — **재계산 없이 그대로 플롯**(모든 값이 csv 원문).
- A(α): +0.116 → +0.153 → +0.302 (high 분위만 CI 0 배제), overall +0.185 [+0.047, +0.316], **high−low +0.186 [−0.149, +0.504], P=0.863 → UNSUPPORTED**.
- B(γ): −0.015 / −0.101 / +0.077 전부 CI 0 포함, overall −0.017, **high−low +0.092 [−0.279, +0.440], P=0.694 → UNSUPPORTED**.
- 부제에 scVelo γ 참조값(−0.224 [−0.360, −0.082], n=188)이 **다른 method**라 ladder 불가라는 사실을 명시(csv의 `GAMMA_scVelo_ref` 행).
- csv의 한글 판정어 `미지지`는 그림에 **쓰지 않고** `UNSUPPORTED`로 표기(§3 참조).

### 그림 언어
새 그림 4장 모두 **영어 라벨만** 사용했다. 한글은 한 글자도 렌더되지 않는다(csv/leg 문자열의 α·γ는 조회 키로만 쓰고 축·제목엔 `alpha`/`gamma`로 표기, 판정어는 `UNSUPPORTED`).

---

## 3. 남은 리스크 / 사람이 판단할 것

1. **패널 3·4는 단일 셔플 realization**이다. 심사자가 "null distribution"을 기대하면 다중 permutation envelope(예: 20회 셔플의 per-bin 분위)로 다시 그려야 한다. 현재 `results/`엔 셔플 20회의 per-gene 산출이 저장돼 있지 않아(coupling은 CSV에 realization 0만, scrambled refit은 1회) **지금은 만들 수 없다** — 만들려면 재실행이 필요하고, 그건 `results/` 재생성이므로 이번 작업 범위 밖.
2. **HSPC |lag| = +0.163은 신규 계산치**다. 본문에 실으려면 `results/`에 기록하는 절차를 밟는 편이 안전하다(§2 figS01 주의).
3. png는 gitignore 대상 → **투고 번들은 스크립트 4+1개를 돌려 재생성**한다. 재생성 명령:
   ```bash
   PY=~/miniconda3/envs/scv-preprocess/bin/python
   cd pipeline/hspc-velocity-benchmark
   $PY figures/figS01_per_dataset_concordance.py
   $PY figures/fig05_profile_likelihood.py            # = Figure S2
   $PY figures/figS03_atac_shuffle_lag.py
   $PY figures/figS04_coupling_shuffle.py
   $PY figures/figS05_stiffness_tertile_ladder.py
   ```
4. **번호 정합**: 약속 순서를 그대로 S1…S5로 매핑했고, 패널(2)만 파일명이 `fig05_profile_likelihood.py`다(기존 파일명 유지, 이름 변경은 다른 문서의 참조를 깨므로 하지 않음). 번들 시 **fig05 → Figure S2**로 배치해야 한다.
5. `fig_sim_positive_control.png` · `sim_injected_lag.png` · `lag_model.png` 3장은 Additional file 11의 약속에 없다. 넣을지 뺄지는 집필자 판단(넣는다면 S6~S8).

---

## 4. `SUPPLEMENTARY.md` Additional file 11 — 제안 문장 (직접 고치지 않음)

> 아래는 **교체 제안**이다. 현재 서술의 "Planned panels … Not yet rendered"를 실물 기준으로 바꾼다.
> `Cited in.`은 본문 인용 위치를 확인하지 않았으므로 `<FILL>`로 남긴다 — 지어내지 않는다.

```markdown
### Additional file 11: Supplementary figures (Figures S1–S5)
**Title.** Supplementary figures supporting the main display items.
**Description.**
*Figure S1 — Cross-method concordance within each dataset.* Rank–rank scatter of the two
chromatin-aware arms (MultiVelo × MultiVeloVAE) for the transcription rate α (top row) and for the
chromatin→transcription lag magnitude (bottom row), in each of the five multiome systems that carry
two chromatin-aware arms. α reproduces everywhere (Spearman +0.882 HSPC, +0.917 macrophage,
+0.898 E18 mouse brain, +0.906 human BMMC, +0.953 mouse gastrulation) while the lag magnitude does
not (+0.163*, +0.074, +0.057, −0.088, −0.026). Only lag magnitude is compared: MultiVelo's lag sign is
structurally positive under the 4-state monotone switch ordering and therefore uninformative.
*(\*) The HSPC lag-magnitude value +0.163 was computed for this panel and is not yet recorded in any
`results/` file; it uses the magnitude convention shared with the four external systems, and is distinct
from the signed-convention value −0.010 reported for the same method pair in `results/concordance.md` §3.5.
Record it in `results/` before this text is finalized.*
*Figure S2 — Profile-likelihood identifiability.* On MultiVelo's own objective: per-cell log-curvature
for α versus the lag (A), the per-gene stiffness ratio (B, α stiffer in 95% of genes, median 3.5×), the
lag population trichotomy (C, 56% interior / 38% boundary-pinned / 6% degenerate), and overlaid
profile-likelihood curves for a representative gene (D). This is relative, practical non-identifiability,
not a flat likelihood valley.
*Figure S3 — ATAC-shuffle negative control.* The lag distribution from a within-lineage chromatin
permutation refit end to end, overlaid on the observed lag distribution (single realization, not a
multi-permutation null envelope), together with the per-gene paired comparison. The distributions are
statistically indistinguishable (Mann–Whitney p = 0.196; KS D = 0.050, p = 0.507) and the per-gene lag is
largely preserved (Spearman 0.721; median relative change 14.7%), although a paired test detects a small
systematic shift (Wilcoxon p = 2.9 × 10⁻⁴, median 5.87 → 5.47).
*Figure S4 — Chromatin–RNA coupling under the same shuffle.* Observed versus ATAC-shuffled coupling
distributions, the per-gene paired scatter, and the per-gene difference. Unlike the fitted lag, the
model-free coupling collapses under the shuffle (observed median +0.126, 87.2% of genes positive;
per-gene excess +0.098, positive in 75.3% of genes; pooled Mann–Whitney p = 5.6 × 10⁻⁷⁵ over 20 shuffle
realizations). Coupling is nevertheless not a reproducible replacement for the lag: it fails the
prespecified cross-dataset criterion (ρ = +0.173 HSPC vs human brain, bound |ρ| > 0.2) and replicates only
in the nearest tissue (macrophage +0.281).
*Figure S5 — Stiffness-tertile ladder for α and γ.* Within-tertile Spearman correlation between the
fitted rate and an external measured rate, with bootstrap 95% CIs, for genes binned by per-gene
profile-likelihood curvature. The α ladder is monotone in the predicted direction (+0.116 → +0.153 →
+0.302) and only its top tertile excludes zero, but the decisive high-minus-low contrast is not separable
(+0.186, 95% CI [−0.149, +0.504], P(diff > 0) = 0.863); the γ ladder is flat (high-minus-low +0.092, 95% CI
[−0.279, +0.440]). Both legs are therefore reported as unsupported, and the reversed γ correlation quoted
elsewhere (−0.224, 95% CI [−0.360, −0.082], n = 188) comes from scVelo — a different method whose per-gene
curvature was never measured and which therefore cannot be laddered.
**Format.** .pdf (single bundled file, Figures S1–S5)
**Source.** `figures/figS01_per_dataset_concordance.py` · `figures/fig05_profile_likelihood.py` (= Figure S2) ·
`figures/figS03_atac_shuffle_lag.py` · `figures/figS04_coupling_shuffle.py` ·
`figures/figS05_stiffness_tertile_ladder.py`; underlying results in `results/concordance*.md`,
`results/prereg_gse205117_scorecard.csv`, `results/profile_likelihood_identifiability.csv`,
`results/scrambled_null.md`, `results/coupling_lag_alternative.md`,
`results/curvature_tertile_validation.csv`. Rendered images are gitignored and are regenerated by running
the five scripts (see `figures/FIGURE_INVENTORY.md`).
**Status.** Rendered. Figures S3 and S4 show a single shuffle realization overlaid on the observed data,
not a multi-permutation null envelope; the pooled p value in Figure S4 is quoted from the 20-realization
test in `results/coupling_lag_alternative.md`. The starred HSPC value in Figure S1 should be written into
`results/` (deterministic recomputation from the committed per-gene CSVs) before this entry is finalized.
**Cited in.** <FILL — confirm main-text citation points before submission>
```

### 부수 수정 제안
- 같은 파일 **L100** "supplementary figures are numbered S1 onward inside Additional file 11" → 그대로 유효(S1–S5).
- 현 L84의 `**Status.** **Not yet rendered.** … Do not cite as existing until rendered.` 문장은 **삭제**한다(이제 사실이 아니다).
- Additional file 11 제목의 `(Figures S1–Sn) — TO BE RENDERED` → `(Figures S1–S5)`.

---

## 5. 이번 작업이 만진 파일 (전부 `figures/` 아래, 신규 생성)
- `figures/figS01_per_dataset_concordance.py` + `.png`
- `figures/figS03_atac_shuffle_lag.py` + `.png`
- `figures/figS04_coupling_shuffle.py` + `.png`
- `figures/figS05_stiffness_tertile_ladder.py` + `.png`
- `figures/FIGURE_INVENTORY.md` (이 문서)

`manuscript/`·`results/`·기존 `figures/*.py`·기존 `figures/*.png`은 **읽기만 했고 수정하지 않았다.**
