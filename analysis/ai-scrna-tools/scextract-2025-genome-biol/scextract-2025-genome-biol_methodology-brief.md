# Methodology Brief — scextract-2025-genome-biol

## 한 줄 결론 (모든 독자)
- Citation: `@wu2025scextract`  |  Importance: `중` (LLM-annotation + prior-aware integration 구조 깔끔, 코드 완전 공개, 그러나 multiome 미지원으로 우리 현재 dataset 직접 적용에 제약)
- 한 문장 결론: 논문 PDF를 읽어 scRNA-seq pipeline을 자동 실행하고 annotation을 prior로 배치 보정하는 end-to-end framework — 공개 데이터셋 통합 또는 large-scale atlas 구축 시 즉시 차용 가능.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: open — 18개 cellxgene benchmark datasets는 Zenodo(doi:10.5281/zenodo.13827072) 공개. 피부 14개 dataset은 Additional file 4 Table S3 accession으로 GEO에서 직접 다운.
- 코드 공개: https://github.com/yxwucq/scExtract (BSD 2-Clause, active 2025). 재현 결과·figures: Zenodo doi:10.5281/zenodo.15555221.
- 자원 요구: GPU 불필요 (annotation 단계). Integration 대규모(>200k cells) 시 V100 GPU 권고 (use_gpu=True, CuPy). PC(i5-13600K)에서 단일 dataset 처리 ~20분, $1 미만.
- 핵심 의존성: Python, scanpy, harmonypy [ref 61], scib_metrics [ref 6], decoupleR v1.6.0 [ref 62], OpenAI text-embedding-3-large (Azure API — annotation similarity matrix 생성용), LLM API (Deepseek-v2.5 / GPT-4o-mini / Claude-3.5-Sonnet 중 선택).
- 자세히 → [scextract-2025-genome-biol_core.md](scextract-2025-genome-biol_core.md) §Methods, [sources/scextract-2025-genome-biol.pdf](sources/scextract-2025-genome-biol.pdf) §Methods (pp.21–26)

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: 부분 일치 — HSPC 10x Multiome의 RNA 컴포넌트(h5ad)는 처리 가능. ATAC 컴포넌트는 미지원. 처리하려면 RNA만 분리 후 적용.
- 자원 가능성: 가능 — Python + scanpy 기반, 기존 팀 환경 그대로 사용. LLM API key 설정만 추가 필요 (Claude API 또는 Deepseek).
- 비용·시간 추정: 단일 dataset 테스트 ~1시간 (setup + 첫 실행). 우리 HSPC 공개 dataset(GSE209878) 1건 처리 시 API 비용 $1 이하.
- ROI 한 줄: 우리가 다른 팀의 공개 scRNA-seq dataset을 재활용하거나 multi-dataset atlas를 구축할 때 manual annotation 작업을 제거하는 데 가치. 핵심 연구(chromatin-RNA lag)와 직접 연결성은 낮음.
- 자세히 → [scextract-2025-genome-biol_lens-industry.md](scextract-2025-genome-biol_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)
- 질문: HSPC multiome RNA 컴포넌트에 scExtract annotation을 돌려 기존 수동 annotation과 일치율을 측정해볼 것 — 즉시 실행 가능.
- 질문: Tang lab에서 multiome 지원 확장 계획 여부 GitHub issues에서 확인.
- 다음 액션: GitHub clone + Claude API key 설정 → GSE209878 RNA subset에 시범 적용 (~2주 내).
- 자세히 → [scextract-2025-genome-biol_lens-academic.md](scextract-2025-genome-biol_lens-academic.md), [scextract-2025-genome-biol_lens-industry.md](scextract-2025-genome-biol_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
