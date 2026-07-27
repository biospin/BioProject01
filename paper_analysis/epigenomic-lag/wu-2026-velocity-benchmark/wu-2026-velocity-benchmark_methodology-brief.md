# Wu et al., 2026 (GB velocity benchmark) — methodology-brief

> 우리 원고(BIOP01) 작업에 바로 쓰는 실행 지침. 근거 = `_core.md`.

## 즉시 반영 (draft — 영/한 동시, 다른 창과 조율 후)
1. **참고문헌 추가**: Wu Y, Kong C, Liao X, Lin Z, Sun X, Liu J. Comprehensive benchmarking of RNA velocity methods across single-cell datasets. Genome Biology 27:242 (2026). doi:10.1186/s13059-026-04182-z. → [12][13] 옆 세 번째 벤치마크로. (p12/p15 재번호 스크립트로 편입, 앵커는 Background·Positioning의 벤치마크 언급 지점.)
2. **Positioning 문단 보강**: "임베딩 벡터를 채점하는 세 벤치마크(Luo·Huang·Wu)와 달리, 우리는 (a) cell×gene 행렬의 method 간 재현성 (b) ATAC-shuffle 인과 대조 (c) 외부 측정 rate 앵커 (d) 사전등록을 적용한다"로 명시.
3. **데이터 각주**: GSE209878이 Wu의 Data 6로도 쓰였음을 명기(중복이 아니라 다른 질문이라는 근거).

## 저널 결정(BIOP01-75)에 넘길 판단 자료
- GB에 종합 velocity 벤치마크가 방금 게재됨 → **GB desk-reject 위험 상향**. CRM base-case의 상대 안전성 ↑. 회의 안건(저널 결정)에 반영.

## 하지 말 것
- draft_v2/draft_v2_ko를 지금 임의 수정하지 않는다(다른 창과 draft 동시 편집 금지 규칙). 위 1~3은 **조율 후** 반영.
- Wu의 임베딩 지표(CBDir/ICVCoh)를 우리 지표로 도입하지 않는다 — 우리 축은 행렬 재현성·인과다.
