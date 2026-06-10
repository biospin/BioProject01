# Methodology Brief — cytetype-2025-biorxiv
<!-- PDF 기반 전체 분석. abstract-only 버전 덮어씀. Source: sources/cytetype-2025-biorxiv.pdf -->

## 한 줄 결론 (모든 독자)

- Citation: `@ahuja2025cytetype` | Importance: `중` (pipeline-applicable annotation tool. preprint COI 있어 독립 검증 단계 권장)
- 한 문장 결론: scRNA-seq cell type annotation을 multi-agent framework로 자동화하고 confidence score를 제공하는 Python/R SDK 도구 — 우리 HSPC dataset에 바로 적용 가능하며, low-confidence cluster 우선 검증 전략에 활용.

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: open — 4 benchmark datasets 모두 공개 atlas (HypoMap, Immune Cell Atlas, GTEx v9, Mouse Pancreatic Cell Atlas). 저자 benchmark notebooks: https://github.com/dalloliogm/cytetype_benchmark/tree/main/notebooks/manual
- **코드 공개**: open — Python SDK: https://github.com/NygenAnalytics/CyteType; R SDK: https://github.com/NygenAnalytics/CyteTypeR; CyteOnto: https://github.com/NygenAnalytics/CyteOnto (license 미확인; `검토필요:`)
- **자원 요구**: GPU 불필요. Cluster당 5–10분, 400,000–600,000 tokens. Closed-weight LLM API 비용 발생. Open-weight (DeepSeek R1, Kimi K2) 로컬 실행 시 비용 최소화 — 우리 서버 (128GB RAM) 환경 feasibility 확인 필요.
- **핵심 의존성**: AnnData (anndata), Seurat (R); LLM API (OpenRouter, AWS Bedrock) 또는 로컬 Ollama; CyteOnto Python package
- 자세히 → [cytetype-2025-biorxiv_core.md](cytetype-2025-biorxiv_core.md) §Methods, [sources/cytetype-2025-biorxiv.pdf](sources/cytetype-2025-biorxiv.pdf) §Methods

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: AnnData .h5ad 직접 지원 — 우리 HSPC 10x Multiome (GSE209878)과 완전 호환. RNA layer만 사용 (ATAC 통합 annotation은 미지원).
- **자원 가능성**: 현재 팀 역량으로 가능. Python SDK 설치 후 API key (OpenRouter) 또는 로컬 open-weight model 설정. GPU 불필요. 128GB RAM 서버에서 로컬 실행 검토 필요.
- **비용·시간 추정**: 파일럿 (50 clusters) 기준 open-weight 로컬 실행 시 ~1–2일 엔지니어링 + 수 시간 실행. 클라우드 API 사용 시 추가 비용.
- **ROI 한 줄**: Cell type annotation 수작업 부담 경감 + rare cell state 발굴 + confidence score 기반 wet lab 검증 우선순위 결정. 우리 epigenetic lag 연구에서 cell type-specific lag 분석을 위한 annotation QC layer로 활용.
- 자세히 → [cytetype-2025-biorxiv_lens-industry.md](cytetype-2025-biorxiv_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)

- `질문: CyteType을 우리 HSPC dataset에 파일럿 실행 시 기존 manual annotation 대비 confidence score 분포가 어떻게 나오는가? Low-confidence cluster가 epigenetic lag 분석에서 노이즈 원인인지 확인.`
- `질문: open-weight model (DeepSeek R1) 로컬 실행 시 우리 서버 (128GB RAM)에서 실제 처리 가능한가? Ollama 셋업 비용 대 API 비용 비교.`
- **다음 액션**: HSPC AnnData 파일 50개 clusters subset으로 CyteType Python SDK 파일럿 실행 — 다음 분기 초 (~2–3주).
- 자세히 → [cytetype-2025-biorxiv_lens-academic.md](cytetype-2025-biorxiv_lens-academic.md), [cytetype-2025-biorxiv_lens-industry.md](cytetype-2025-biorxiv_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
