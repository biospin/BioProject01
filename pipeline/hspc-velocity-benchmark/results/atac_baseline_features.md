# day0 ATAC baseline feature 어셈블 (진짜 ATAC peak)

> `crakvelo_atac_prepro.h5ad` 197,482 peak에서 **day0 HSC/MPP 8583 세포** baseline 접근성.
> gencode v44 TSS 기준 promoter(±2000bp)/enhancer(±100kb distal) peak 매핑.
> p5_lag_model.py 한계 ①(moflow Mc smoothed proxy) 해소용 실제 ATAC feature.

- 대상 gene: MultiVelo 538 → TSS 매칭 512 → peak 할당 **511** gene.
- feature 커버리지: prom_acc 93%, enh_acc 100%.
- promoter peak 중앙값 1개, enhancer peak 중앙값 22개/gene.

## feature 분포(중앙값)

| feature | median | 설명 |
|---|---|---|
| prom_acc | 0.161 | promoter 평균 접근성(CP10k) |
| enh_acc | 0.033 | distal enhancer 평균 접근성 |
| enh_sum | 0.678 | distal enhancer 누적 접근성 |
| prom_enh_ratio | 0.832 | promoter 접근성 분배 |

## 다음
- `p5_lag_model.py`에 feature set `real-atac` 추가 → moflow-Mc baseline 대비 held-out 일반화 비교.
- ⚠️ peak-count 기반(fragment 미보유), consensus union 좌표. day0만 사용→ATAC batch 무관.
