# Wu et al., 2026 — RNA Velocity Benchmark (GB) — Abstract 분석

> 근거 자료: publisher metadata의 abstract 원문(`sources/abstract.txt`) + 본문 도입부(`sources/fulltext_extracted.txt`). abstract에 명시된 것만 근거로 한다.

## Abstract Summary

- **한 문장 요약**: RNA velocity method가 급증했으나 종합·표준 벤치마크가 없는 상황에서, 19개 도구(30 method)를 34개 데이터셋(26 real + 8 simulated)에서 8개 task로 평가하고, 단일 랭킹 대신 **task별·맥락별 선택 가이드**를 제시한 종합 벤치마크.
- **연구 목적**: diverse biological·technical scenario에서 맥락 특이적 metric으로 method를 평가하는 표준 벤치마크 수립.
- **문제/gap**: 기존 비교가 "limited scope or incomplete task design"이라 사용자에게 명확한 가이드가 없음.
- **핵심 방법**: 25개 RNA-only method를 8 task로 평가(핵심 4: directional consistency, temporal precision, negative control robustness, sequencing depth stability), multimodal-enhanced 5종은 multimodal integration task에서만 평가.
- **주요 결과**: directional consistency ↔ negative control robustness 사이 **명확한 trade-off**, temporal modeling 전략별 그룹 거동, sequencing depth·quantification 선택에 따른 변동. 개선 필요 gap 3종(gene dependence 모델링, temporal inference 정확도, multimodal 설계).
- **저자 주장 기여**: 단일 overall 랭킹이 아니라 생물·기술 맥락별 **task-aware 선택 지침**.

## 우리 원고(BIOP01)와의 관계 — abstract 수준

- 같은 장르(velocity 벤치마크)이나 **RNA-only 중심 + 임베딩/전이벡터 지표**다. 우리는 multiome 행렬 재현성 + ATAC-shuffle 인과 + chromatin-lag 감사라 축이 다르다.
- abstract에는 우리 차별점 키워드(cell×gene 행렬 method 간 재현성, ATAC-shuffle, chromatin-lag 신뢰성, 외부 측정 rate 앵커, 사전등록)가 **없다**. 전문 검증은 `_core.md` §스쿱.
- **타깃 저널(Genome Biology) 게재**이므로 abstract만으로도 인용·차별화 필요가 확정된다.
