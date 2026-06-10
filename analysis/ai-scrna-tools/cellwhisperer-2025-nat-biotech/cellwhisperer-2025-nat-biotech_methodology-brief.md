# Methodology Brief — cellwhisperer-2025-nat-biotech

## 한 줄 결론 (모든 독자)
- Citation: `@schaefer2025cellwhisperer` | Importance: `중` (zero-shot annotation 탐색 가능, 단 accuracy 한계로 primary tool 채택은 이르다)
- 한 문장 결론: CLIP 기반 multimodal 임베딩 (Geneformer+BioBERT) + Mistral 7B fine-tuning으로 scRNA-seq chat 탐색 구현 — 탐색적 분석 보조 및 methodology 참조 가치.

## 재현 가능성 체크 (재현 담당자)
- **데이터 접근**: open — GEO, CELLxGENE Census (모두 공개). 학습 데이터 다운로드 자동화 스크립트 포함 (GitHub).
- **코드 공개**: https://github.com/epigen/cellwhisperer — Creative Commons Attribution 4.0. 2025년 11월 기준 활성 (논문 동시 공개). Model checkpoints + training data: https://cellwhisperer.bocklab.org.
- **자원 요구**: 임베딩 추론 — CPU 가능 (수 시간), A100 1개면 분 단위. Chat model — A100 80GB 1개 필요. 학습 재현 — A100 8개 < 24h (embedding), A100 4개 3h (chat).
- **핵심 의존성**: `geneformer`, `transformers`, `pytorch`, `pytorch-lightning`, `llama.cpp` (Mixtral annotation용). CELLxGENE Explorer 1.2.0+ (web integration).
- 자세히 → [cellwhisperer-2025-nat-biotech_core.md](cellwhisperer-2025-nat-biotech_core.md) §Methods, [sources/cellwhisperer-2025-nat-biotech.pdf](sources/cellwhisperer-2025-nat-biotech.pdf) §Methods

## 우리 적용 가능성 (의사결정자)
- **Dataset 호환**: HSPC 10x Multiome (GSE209878) — scRNA-seq count matrix h5ad 전처리 후 적용 가능. ATAC-seq 정보는 현재 미지원 (RNA-only 적용).
- **자원 가능성**: 임베딩 추론은 CPU 서버로 가능. Chat 사용 시 A100급 GPU 1대 필요. 우리 환경에서 feasible.
- **비용·시간 추정**: 설치 + HSPC dataset 적용 시도 — 1–2일. CELLxGENE Explorer 통합 — 0.5일 (Docker 기반).
- **ROI 한 줄**: 탐색적 cell annotation 및 cluster 설명 자동화로 분석 초기 단계 효율 향상. 단 최종 결과는 기존 pipeline으로 재확인 필수.
- 자세히 → [cellwhisperer-2025-nat-biotech_lens-industry.md](cellwhisperer-2025-nat-biotech_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)
- 질문: HSPC h5ad에서 RNA layer만 추출해 CellWhisperer에 입력했을 때 cell type annotation 품질이 기존 scanpy 결과와 얼마나 일치하는가?
- 질문: Chat hallucination이 HSPC biology에서 어떤 패턴으로 나타나는지 — established marker gene을 잘못 언급하는지 직접 확인 필요.
- **다음 액션**: CellWhisperer GitHub clone + HSPC 소규모 subset (1k cells) 적용 시도 — 이번 sprint 내 (~1주).
- 자세히 → [cellwhisperer-2025-nat-biotech_lens-academic.md](cellwhisperer-2025-nat-biotech_lens-academic.md), [cellwhisperer-2025-nat-biotech_lens-industry.md](cellwhisperer-2025-nat-biotech_lens-industry.md) §4

---
마지막 갱신: 2026-06-10

---

## 핵심 방법

### 아키텍처 개요

```
RNA-seq 프로파일 (전사체)
        ↓
[전사체 인코더]      [텍스트 인코더 (LLM 기반)]
        ↓                    ↓
        ← 대조 학습(Contrastive Learning) →
              멀티모달 공동 임베딩 공간
                      ↓
              [LLM 언어 모델]
                      ↓
          자연어 질의응답 (채팅 인터페이스)
```

외부 맥락: CLIP(Contrastive Language-Image Pretraining, Radford et al. 2021)의 scRNA-seq 도메인 적용으로 추정. 이미지-텍스트 쌍 대신 전사체-텍스트 쌍을 사용.

### 학습 방법: 대조 학습

- **입력 쌍**: RNA-seq 프로파일 ↔ AI 큐레이션 텍스트 설명
- **학습 목표**: 같은 쌍(positive pair)의 임베딩은 가깝게, 다른 쌍(negative pair)은 멀게 정렬
- **학습 데이터 규모**: 100만 개 RNA-seq 프로파일 + 대응 텍스트 주석
- **AI 큐레이션 주석**: 기존 메타데이터(CZ CellxGene 등)를 AI로 텍스트화한 것으로 추정. 외부 맥락: 수동 큐레이션의 확장성 한계를 극복하기 위한 접근.

### 추론 방법: Zero-shot 예측

- 새로운 세포의 RNA-seq 프로파일 → 전사체 인코더 → 임베딩 추출
- 임베딩을 텍스트 공간의 세포 유형 설명과 유사도 비교
- 가장 가까운 텍스트 설명의 세포 유형을 예측 — 추가 학습(fine-tuning) 없이 동작

### 자연어 질의응답 파이프라인

- 사용자 질문 → LLM 파싱 → 멀티모달 임베딩에서 관련 세포/유전자 검색 → LLM으로 자연어 답변 생성
- CELLxGENE 브라우저 통합: 시각화(UMAP 등) + 채팅 답변 동시 표시

---

## 재현 가능성

### 재현성 강점

- 100만 개 공개 데이터(CZ CellxGene 등) 기반 — 학습 데이터 접근성 양호
- CELLxGENE 통합으로 공개 배포 및 웹 접근 가능성 높음
- 외부 맥락: CeMM 그룹의 이전 연구들(Bock 교수 그룹)이 오픈소스 중심임을 고려하면 코드 공개 가능성 높음

### 재현성 제약

- AI 큐레이션 텍스트 주석의 생성 방법 및 버전 관리: abstract 범위 외, 미제공
- LLM 응답의 비결정론적(non-deterministic) 특성 — 동일 쿼리에 대해 답변이 다를 수 있음
- 벤치마크 데이터셋 및 구체적 평가 지표: abstract 범위 외, 전문 확인 필요
- 100만 프로파일 학습에 필요한 컴퓨팅 자원: 대규모 GPU 필요 (재현 시 비용 높음)

---

## OncoRader 내부 적용 가능한 기법

### 1. 대조 학습 기반 멀티모달 임베딩

**적용 가능 시나리오**: OncoRader에서 CTC 마커 패널과 문헌 텍스트(ADC 타겟 논문)를 연결하는 임베딩 구축에 응용 가능. 예를 들어, 특정 CTC 유전자 발현 프로파일과 "HER2-positive breast cancer CTC marker" 같은 텍스트를 연결하면 ADC 타겟 발굴에 맥락 정보를 추가할 수 있음.

**주의점**: 공개 CTC 데이터가 100만 개 규모에 비해 극히 적으므로, CTC 특화 대조 학습은 데이터 부족 문제가 있음. 공개 조직 scRNA-seq 데이터로 pre-train 후 CTC 데이터로 fine-tune하는 방식 필요.

### 2. Zero-shot 세포 유형 주석

**적용 가능 시나리오**: OncoRader 파이프라인에서 비-CTC 배경 세포(혈소판, 면역세포, 내피세포 등) 클러스터 자동 주석에 활용. CellWhisperer의 일반 세포 유형 지식으로 배경 세포를 빠르게 분류하면 CTC 분리 정확도 향상에 보조적으로 기여 가능.

**실용성**: API 또는 오픈소스로 배포될 경우 OncoRader 전처리 단계에 통합 가능. 단, CTC 자체 주석은 CellWhisperer 학습 데이터 부족으로 직접 활용 어려움.

### 3. 자연어 인터페이스 설계 참고

**적용 가능 시나리오**: OncoRader 사용자 인터페이스 개발 시 채팅 기반 탐색 UX 설계 참고. 제약사 담당자가 "이 환자 코호트에서 HER2 발현 CTC 비율이 얼마인가?"를 자연어로 질의하는 방식으로 확장 가능.

**기술 스택 참고**: 외부 맥락: LangChain/LangGraph + 벡터 데이터베이스(FAISS, ChromaDB 등) + OpenAI API 조합이 이 분야 표준으로 자리잡고 있음. OncoRader 채팅 기능 추가 시 참고 아키텍처로 활용 가능.

### 요약: 단기 적용 우선순위

| 기법 | 단기 적용 가능성 | 예상 효과 |
|------|:---:|---------|
| 대조 학습 멀티모달 임베딩 | 중간 | ADC 타겟-문헌 맥락 연결 |
| Zero-shot 세포 주석 | 높음 | 배경 세포 자동 분류 보조 |
| 자연어 인터페이스 | 높음 | 사용성 향상, BD 데모 강화 |
