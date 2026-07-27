# Wu et al., 2026 (GB velocity benchmark) — lens: academic

> 근거: `_core.md` + `sources/`. 학술 기여·한계·우리 원고 방어선 관점.

## 학술적 기여
- 규모: 19 도구/30 method × 34 데이터셋 × 8 task. RNA velocity 벤치마크 중 현재 최대 축(이전 Luo 14×17, Huang 29×176과 함께 3대 벤치마크).
- 개념 기여: **directional consistency ↔ negative control robustness trade-off**(ρ=−0.572, P=0.003)를 정량화. "방향 신호 최적화가 spurious velocity를 낳는다"를 순위 역전(LatentVelo 1위↔23위)으로 실증.
- 단일 랭킹을 거부하고 task-aware 선택 지침을 산출물로 삼음 — 사용성 측면 기여.

## 한계 (우리 원고의 대비축)
- **채점이 임베딩/전이벡터 수준에 머문다**(CBDir·ICVCoh). velocity의 세 층(① 유전자별 모수 ② cell×gene 행렬 ③ 임베딩 화살표) 중 ③만 본다. ②(행렬)의 method 간 재현성은 다루지 않는다 — 우리 원고의 핵심 공백.
- **인과 대조가 없다**. negative control은 출력 robustness(STS/EES)이지 입력 교란(ATAC-shuffle)이 아니다. "무엇이 velocity를 만드는가"는 검정하지 않는다.
- **multimodal이 얕다**: 9개 multimodal 도구 중 5종, 그것도 1 task(통합), 3개 데이터셋. chromatin이 velocity에 기여하는지의 인과·재현성은 범위 밖.
- **외부 ground truth 부재**: 측정된 합성/분해 rate(TT-seq·SLAM) 앵커가 없다. 방향 정확도는 pseudo-ground-truth transition에 의존.
- **사전등록·자기철회 없음**: 결과를 본 뒤 지표를 고르는 것을 막는 장치가 명시되지 않음.

## 우리 원고 방어선 (리뷰어 대응)
- "이미 벤치마크가 있는데?" → 세 벤치마크(Luo·Huang·Wu) 전부 **임베딩 순위**다. 우리는 행렬 재현성 + ATAC-shuffle 인과 + 외부 rate 앵커 + 사전등록. 축이 다르다.
- "Wu가 우리 데이터(GSE209878)를 썼는데?" → 그들은 Data 6을 임베딩 CBDir로 채점, 우리는 같은 데이터에서 cell×gene 행렬의 method 간 재현성과 chromatin-lag 신뢰성을 본다. 같은 데이터, 다른 질문.
- "GraphVelo(ATAC)가 MultiVelo보다 낫다던데?" → 새 multiome method가 계속 나온다는 사실 자체가 "출력이 신뢰 가능한지 먼저 감사하라"는 우리 논지를 강화한다.
