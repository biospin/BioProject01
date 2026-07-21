# Proxy-join 설계 — chromatin-lag의 decay/synthesis 독립성 입증 (BIOP01-23, reframe 후)
> 작성 2026-06-26. 검토자 관점(과학·방법론). DESIGN.md(v2) 스타일 준수.
> 전제: **timing outcome reframe 확정** — ≥3 timepoint 약물 데이터 부재(BIOP01-23_review §B). drug-timing 예측은 future work + 가설로 강등.

## 0. Reframe된 주장 (이 분석이 입증하는 것)

- ~~"chromatin-lag → drug response timing 예측"~~ (데이터 없음 → future)
- **→ "chromatin–transcription lag은 mRNA decay/synthesis kinetics로 환원되지 않는, 독립적인 chromatin-side kinetic 축이다. drug response *magnitude*에 대해 decay·synthesis를 통제한 뒤에도 incremental 예측력을 가진다."**
- timing은 이 **독립성을 근거로 한 가설**로만 서술(예측 주장 X).
- Todorovski 대비 포지션: 그들이 "chromatin state independent"라 결론하고 안 측정한 **chromatin dynamics(lag)** 가 잔여 분산을 잡는지 정면 검정.

## 1. 데이터 & join key

| 출처 | 제공 feature | 비고 |
|---|---|---|
| **우리 HSPC multiome (GSE209878)** | gene별 **chromatin-lag** (MoFlow c-s lag 1차 / MultiVeloVAE δ·κ) | BIOP01-22 벤치마크 산출물. **within-lineage** 집계. lag ground truth 없음(재현성만). |
| **Todorovski (GSE229314)** | gene별 **t½(decay, 6,580 gene)**, **synthesis(TT-seq)**, **drug response magnitude**(MAC-seq class I/II, ROC) | bulk K562/THP-1(leukemia). |
| **83-compound NASC-seq2 (E-MTAB-13091/14822/14924)** | **synthesis rate**(nascent, 보조/교차검증) | bulk·single-cell, epigenetic 83종. |
| (선택) 공개 HSPC/CD34 half-life DB | t½ 보존성 검정용 | gene-intrinsic 가정 gate. |

- **join key = gene symbol**(HGNC 정규화; ortholog 아님, 동일 인간 gene). intersection + drop 보고.

## 2. ⚠️ Gate: gene-intrinsic 가정 검정 (통과 못 하면 join 무효)

proxy join의 최대 약점 = t½/synthesis를 **leukemia(K562) → HSPC**로 차용. 분석 전 **gate**로 검정:
1. 공개 HSPC/CD34 t½(또는 다른 cell type t½)와 Todorovski K562 t½의 **gene-wise 상관**(Spearman). 전역 + housekeeping/cell-type-specific 층화.
2. 보존성이 낮으면(예: ρ<0.3) → t½ 차용 무효 → **K562 자체 ATAC public으로 lag proxy 재현**(win1 대안) 또는 join 포기.
3. 통과 시: gene-intrinsic 가정 + 잔차 confound로 cell-type 차이 흡수, 한계 명시.

## 3. Feature 구성

- **outcome Y** = drug response **magnitude** (Todorovski down-regulation; 연속 logFC 또는 class ROC). ⚠️ magnitude이지 timing 아님(reframe).
- **baseline predictors** (Todorovski 재현): `decay(t½)` + `synthesis_rate`.
- **test predictor**: `chromatin_lag`(우리; MoFlow 1차).
- **confound 공변량**: baseline expression level, gene length, GC, (가능 시) within-lineage 평균화로 lineage kinetics, cell-cycle stratify.

## 4. 모델 & incremental 검정 (공선성 처리 포함)

```
M0 (baseline):  Y ~ decay + synthesis + confounds          # Todorovski SOTA 재현(AUC 0.86–0.94 목표 바)
M1 (test):      Y ~ decay + synthesis + confounds + lag
```
- **incremental**: ΔR²(연속) / ΔAUC(class) + **likelihood-ratio test**, **nested CV**(gene-level, leakage 방지)로 과적합 통제.
- **다중공선성(필수)**: lag↔decay 상관 가능 →
  - VIF 보고(>5 경고),
  - **orthogonalization**: lag을 (decay+synthesis)에 회귀시킨 **잔차 lag⊥**로 incremental 재검(순수 lag 기여),
  - **상대중요도(LMG/Shapley R²)**로 lag의 분산 분해 기여 보고.
- **effect-size 사전 점검**: ΔR²가 너무 작으면(예: <0.01) 논문 약함 → power/표본 gene 수 사전 고려.

## 5. Null / robustness

- **gene-label permutation**(lag↔outcome shuffle) → ΔR² null 분포. permutation-FDR(공조절 비독립).
- **scrambled-chromatin lag**(ATAC permutation으로 만든 가짜 lag) → incremental 사라져야 함(lag이 chromatin 신호임을 입증).
- **lag method 교체**(MoFlow ↔ MultiVeloVAE)로 incremental 부호·크기 재현 → lag 정의 의존성 점검(P3 교훈).
- **cross-dataset sensitivity**: t½ 출처 바꿔(다른 cell type DB) incremental 안정성.

## 6. 의존 순서 (중요)

proxy join 입력 `chromatin_lag`의 신뢰성 = **BIOP01-22/23 벤치마크 결과에 의존**.
→ **순서: ① 벤치마크(method 선정 + lag stability, GPU 필요) → ② proxy join.** lag이 재현적이지 않으면 join 입력이 noise. (= GPU 투자가 join의 선행조건이기도 함)

## 7. 한계 (논문에 명시)

1. **cross-dataset**(leukemia t½ ↔ HSPC lag) — gene-intrinsic 가정(§2 gate로 부분 방어).
2. **outcome = magnitude, not timing** — timing 주장은 future. (현 데이터로 timing 모델 불가)
3. **lag·t½ 모두 추정치**(ground truth 없음) — lag은 재현성만, t½는 차용.
4. 결론 형태: "decay/synthesis 통제 후 lag incremental 유의" → **독립 축 주장**까지. timing 예측은 가설.

## 8. 산출물

- `proxy_join/gene_intrinsic_gate.md` (§2 통과/실패)
- `proxy_join/nested_models.csv` (M0/M1, ΔR²/ΔAUC, VIF, LMG)
- `proxy_join/null_robustness.md`
- `RESULTS.md` 절: "chromatin-lag은 decay/synthesis 독립 축 (incremental 예측력)"

## 한 줄
reframe 후 핵심 = **"timing 예측"이 아니라 "lag의 kinetic 독립성"**. proxy join은 *magnitude* outcome으로 decay+synthesis를 통제하고 ΔR²/ΔAUC로 lag incremental을 보임 — gene-intrinsic gate(§2)와 공선성 처리(§4)가 성패를 가른다. 입력 lag 신뢰성은 GPU 벤치마크 선행에 의존(§6).
