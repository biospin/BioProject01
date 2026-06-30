# P5 — 진짜 day0 ATAC feature → kinetic timing 모델 (held-out lineage CV)

- 472 gene(세 feature set 공통), Ridge, leave-one-lineage-out.
- p5_lag_model.py 한계 ①(moflow Mc smoothed) 해소: **day0 HSC/MPP ATAC peak**에서 promoter/enhancer 접근성 직접 사용.
- feature set: **mc-proxy**(moflow Mc) / **real-atac**(prom/enh ATAC) / **atac+mc**(합집합).

## held-out lineage 일반화 (Spearman pred vs actual)

| target | feature set | overall | Baso/Eo/Mast | Erythroid | HSC/MPP | Lymphoid | MK | Myeloid |
|---|---|---|---|---|---|---|---|---|
| lag (method-sensitive) | mc-proxy | **-0.199** | -0.07 | -0.43 | -0.10 | -0.29 | -0.23 | -0.08 |
| lag (method-sensitive) | real-atac | **+0.049** | -0.04 | +0.19 | +0.09 | +0.03 | +0.12 | +0.05 |
| lag (method-sensitive) | atac+mc | **-0.038** | -0.07 | -0.17 | -0.01 | -0.07 | +0.09 | -0.01 |
| α (robust) | mc-proxy | **-0.089** | +0.12 | -0.28 | +0.02 | +0.04 | +0.00 | -0.19 |
| α (robust) | real-atac | **+0.309** | +0.39 | +0.46 | +0.34 | +0.38 | +0.22 | +0.60 |
| α (robust) | atac+mc | **+0.285** | +0.43 | +0.29 | +0.24 | +0.41 | +0.20 | +0.58 |

## 해석

- **핵심 발견 — 진짜 day0 ATAC baseline이 robust kinetic rate α를 lineage 간 예측한다(ρ=+0.309)**, 6개 held-out lineage **전부 양수**(+0.22~+0.60). moflow Mc smoothed proxy는 같은 target에서 ρ=−0.089로 **실패** → smoothing proxy가 못 잡던 일반화 신호를 실제 promoter/enhancer 접근성이 잡음. **day0 ATAC 어셈블의 가치를 모델 수준에서 입증.**
- **비robust한 lag은 ATAC로도 예측 불가**: real-atac ρ=+0.049(proxy −0.199보다 낫지만 ~0, 본질적으로 chance). lineage별로도 −0.04~+0.19로 일관성 없음.
- **이중 대조 = 핵심 메시지 강화**: 같은 baseline feature·같은 모델인데 **robust target(α)은 예측되고 비robust target(lag)은 안 됨** → H1('lag은 method-민감·비robust')이 *예측가능성* 축에서도 재확인. **drug-timing 모델은 단일 lag이 아니라 α 같은 robust kinetic + baseline ATAC feature를 써야 한다**는 방향을 데이터로 지지.
- atac+mc(합집합)는 α ρ=+0.285로 real-atac 단독(+0.309)을 못 넘음 → Mc proxy는 추가 정보 없음(오히려 노이즈), 진짜 ATAC만으로 충분.
- ⚠️ peak-count 기반(fragment 미보유), gene→lineage dominant-expression 근사, Ridge α=1 고정. day0만 사용 → ATAC batch 무관.
- 다음: per-lineage refit target(lineage_refit) + bootstrap 안정 gene으로 target 한정, promoter/enhancer 개별 ablation, drug perturbation arm(데이터 대기).
