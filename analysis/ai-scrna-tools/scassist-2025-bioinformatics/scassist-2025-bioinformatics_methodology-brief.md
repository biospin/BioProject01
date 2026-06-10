# Methodology Brief — scassist-2025-bioinformatics

## 한 줄 결론 (모든 독자)

- Citation: `@nagarajan2025scassist`  |  Importance: `하` (R 전용·downstream 검증 없음·우리 파이프라인 언어 불일치 — methodology 참고 수준)
- 한 문장 결론: Seurat scRNA-seq 분석 전 단계에서 augmented prompt로 LLM 파라미터 추천을 제공하는 R 패키지. 우리 Python 파이프라인 직접 적용보다 methodology-reference와 academic-citation 가치.

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: 평가 dataset (LCMV — Nath 2024 *Nat Commun*, BCRUV — Liu 2024 *Immunity*)은 이미 발표 논문 데이터. GEO accession 등 본문 미제공. 예시 데이터(GSM6625298)는 GitHub에서 제공.
- **코드 공개**: https://github.com/NIH-NEI/SCassist — public domain(미국 정부 저작물), active. Zenodo snapshot: https://doi.org/10.5281/zenodo.15298665.
- **자원 요구**: GPU 불필요. API 호출 기반. 2개월 1,978회 API 호출 = $2.07(Gemini). Ollama 로컬 사용 시 LLM 모델 파일(수 GB) + CPU/RAM 필요.
- **핵심 의존성**: R ≥ 4.4.1, Seurat, rollama, httr, jsonlite, visNetwork, clusterProfiler, BiocManager. Google/OpenAI API key 또는 Ollama 설치 필요.
- 자세히 → [scassist-2025-bioinformatics_core.md](scassist-2025-bioinformatics_core.md) §Methods

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 부분 불일치. 우리 HSPC 10x Multiome은 Python/scanpy/AnnData 기반. SCassist는 R/Seurat 전용. rpy2 브릿지 없이는 직접 통합 불가.
- **자원 가능성**: R 환경이 있으면 standalone 실행 가능. 주 파이프라인에 통합하려면 추가 브릿지 작업 필요.
- **비용·시간 추정**: standalone 테스트(Seurat 데이터에서) — 1~2일. 주 파이프라인 통합 — 1주 이상, ROI 불명확.
- **ROI 한 줄**: 직접 채택 ROI 낮음. augmented prompt 설계 패턴을 우리 파이프라인의 LLM 통합 단계 설계 시 methodology-reference로 참고.
- 자세히 → [scassist-2025-bioinformatics_lens-industry.md](scassist-2025-bioinformatics_lens-industry.md) §3

## 본인 재회고 (본인)

- 질문: supplementary zip(btaf402_supplementary_data.zip) 내 File 3에 GPTCelltype 비교 정량 수치(confusion matrix, 일치율)가 있는지 확인 필요.
- 질문: 저자가 예고한 multi-modal/spatial 확장 및 LLM function-calling 자동화 계획의 진행 상황 — GitHub repository 모니터링.
- **다음 액션**: academic-citation 등록 및 paper-info.yaml 갱신 완료. 별도 실험적 적용 계획 없음. 향후 Python scRNA-seq 파이프라인에 LLM 보조 단계 도입 검토 시 augmented prompt 3-레이어 구조(데이터 metrics + prompt template + 실험 맥락) 참고.
- 자세히 → [scassist-2025-bioinformatics_lens-academic.md](scassist-2025-bioinformatics_lens-academic.md), [scassist-2025-bioinformatics_lens-industry.md](scassist-2025-bioinformatics_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
