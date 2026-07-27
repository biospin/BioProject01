# Wu et al., 2026 (GB velocity benchmark) — lens: industry / 실무

> 근거: `_core.md`. method 선택·파이프라인 적용 관점.

## 실무 시사
- **task-aware 선택**: 단일 최고 method가 없으므로, 목적(방향 정확도 vs false-positive 억제)에 따라 다른 method를 택해야 한다. 방향이 중요하면 directional 상위(예: LatentVelo std), 오탐 억제가 중요하면 negative-control 상위 — 둘은 trade-off라 동시 최적이 없다.
- **우리 파이프라인 적용**: 우리는 이미 MultiVelo·MoFlow·CRAK-Velo·MultiVeloVAE·scVelo 5-arm을 돌린다. Wu는 이 중 MultiVelo만(그것도 GraphVelo(ATAC)에 뒤짐) 평가 → **GraphVelo(ATAC)를 추가 arm 후보로 검토 가능**(향후 티켓, 필수 아님).
- **데이터 재사용**: Wu의 Data 6 = 우리 GSE209878. 전처리·transition 정의를 교차 참조 가능(단 Wu는 RNA-only/임베딩 관점).

## 비용·재현
- 코드·데이터 공개(open access, `검토필요:` repo URL). 재현 ROI는 낮음(우리 원고에 직접 재현할 이유는 없고, 인용·차별화가 목적).
- 우리 원고 관점의 실무 결론: 이 논문은 **경쟁 벤치마크**로 다루고(competitive-landscape), 채택할 도구나 지표는 없다. GraphVelo(ATAC)만 향후 arm 후보로 메모.
