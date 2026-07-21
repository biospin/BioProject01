# Methodology Brief — mizukoshi-2024-deepkinet

## 한 줄 결론 (모든 독자)
- Citation: `@mizukoshi2024deepkinet`  |  Importance: 중 — epigenomic-lag *direct* method 아님, *RNA-only kinetic-rate validation의 standard reference*.
- 한 문장 결론: scRNA-seq의 unspliced/spliced만으로 cell-specific splicing/degradation rate를 2-stage VAE로 추정 + simulation+scEU-seq+scNT-seq로 validation한 paper. 우리 epigenomic-lag stack에는 *validation framework reference*로 인용 가치 큼.

## 재현 가능성 체크 (재현 담당자)
- **데이터 접근**: `open` — pancreas (GSE132188), cell cycle scEU-seq (GSE128365), forebrain (SRP129388), breast cancer (GSE167036), MDS-RS는 Adema 2022 published cohort. scNT-seq hematopoiesis는 Dynamo paper data 재사용.
- **코드 공개**: https://github.com/3254c/DeepKINET, Zenodo 10.5281/zenodo.13054695, MIT license. maintenance 상태는 미제공 — 검토필요.
- **자원 요구**: GPU 필수 (저자: TSUBAME3.0, ABCI, SHIROKANE supercomputer 사용; Acknowledgements p.18). 일반 lab GPU(V100 1대) runtime 추정치 본문 *미제공*. 해석: scVAE 계열 일반 runtime 기준 시간~수십 시간 추정.
- **핵심 의존성**: PyTorch + functorch (Jacobian 계산), Scanpy, scVelo, Velocyto, Dynamo (validation 비교용), SERGIO v1.0.0 (simulation), Cell Ranger (raw → count matrix). VICDYF 코드 계승.
- 자세히 → [`mizukoshi-2024-deepkinet_core.md`](mizukoshi-2024-deepkinet_core.md) §Methods, [`sources/mizukoshi-2024-deepkinet.pdf`](sources/mizukoshi-2024-deepkinet.pdf) §Methods p.13–17

## 우리 적용 가능성 (의사결정자)
- **Dataset 호환**: ⚠️ 부분. 우리 HSPC 10x Multiome → DeepKINET RNA part만 적용 가능, chromatin part는 무시. *labeling 없음*이라 우리 환경에서 validation 자체 불가.
- **자원 가능성**: GPU 있음. 단 scEU-seq/scNT-seq 자체 생산은 단기 불가 (wet-lab capability 부족 — `mizukoshi-2024-deepkinet_lens-industry.md` §3.4 참고).
- **비용·시간 추정**: published data에 *시험 적용*은 *1~2주*. 자체 데이터 generation은 *외부 wet-lab 협업 6~12개월*.
- **ROI 한 줄**: *direct pipeline 차용 ROI 낮음*. *validation framework 차용 ROI 큼* — 우리 method paper의 evaluation 설계 template로 그대로 활용.
- 자세히 → [`mizukoshi-2024-deepkinet_lens-industry.md`](mizukoshi-2024-deepkinet_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)
- 핵심 follow-up 질문:
  - 질문: DeepKINET-Multiome (chromatin-aware extension)이 이미 누군가 시도했나? bioRxiv 모니터링 필요.
  - 질문: 본 paper의 *evaluation pattern* (simulation 20×10 + labeling 100회 + box plot + negative-correlation fail rule)을 우리 lag method 평가에 그대로 옮길 때 *어떤 metric*이 lag에 자연스러운가?
- 다음 액션: Week2 validation_report C8 wording을 lens-academic §3 분해표 기준으로 update (*"framework 차용 가능, labeling ground truth ≠ chromatin labeling ground truth"* 양면 표현). 다음 sprint 안에 처리.
- 자세히 → [`mizukoshi-2024-deepkinet_lens-academic.md`](mizukoshi-2024-deepkinet_lens-academic.md) §3 (validation design transferability), [`mizukoshi-2024-deepkinet_lens-industry.md`](mizukoshi-2024-deepkinet_lens-industry.md) §4

---
마지막 갱신: 2026-05-26
