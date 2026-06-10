# Methodology Brief — schat-2024-biorxiv

## 한 줄 결론 (모든 독자)

- Citation: `@lu2024scchat` | Importance: `하` (정량 evaluation 없는 n=3 showcase, 우리 multiome 파이프라인과 직접 연결점 없음)
- 한 문장 결론: GPT-4o + Scanpy function calls + RAG + web search를 결합한 scRNA-seq AI co-pilot 아이디어 논문. architecture 패턴 참고용, 직접 재현 또는 pipeline 적용 대상 아님.

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: 검증 data 중 Bagley et al.(GBM)은 Nat Cancer 2024 — 원논문에서 data availability를 확인해야 함. scChat 자체는 사용자가 `.h5ad` 파일을 제공.
- **코드 공개**: 외부 맥락: GitHub `li-group/scChat` (오픈소스, CC-BY-NC-ND 4.0 — 상업 이용 제한). maintenance 상태 미확인.
- **자원 요구**: GPT-4o API 필수(비용 발생). Scanpy 기반 function calls는 CPU로 가능. GPU 불필요.
- **핵심 의존성**: GPT-4o API(OpenAI), Gemini API(web search), Scanpy, Python `.h5ad` 형식.
- 자세히 → [schat-2024-biorxiv_core.md](schat-2024-biorxiv_core.md) §Methods, [sources/schat-2024-biorxiv.pdf](sources/schat-2024-biorxiv.pdf) §Methods
- **주의**: hyperparameter(temperature, Top-p, Frequency Penalty) 구체 값 미공개 → 동일 결과 재현 보장 불가.

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: scRNA-seq(`.h5ad`) 전용. 우리 HSPC 10x Multiome(RNA+ATAC) 중 RNA 부분은 기술적으로 가능하나, ATAC 처리 기능 없음. scChat의 분석 범위가 RNA-only에 한정.
- **자원 가능성**: API 비용 + 환자 데이터 외부 전송 문제가 임상·규제 환경에서 장벽. 연구 목적 탐색은 가능.
- **비용·시간 추정**: 직접 적용 현실적이지 않음 — 우리 파이프라인(epigenomics, multiome)에 기능 미매칭.
- **ROI 한 줄**: architecture 설계 패턴 참고 가치만 있음. 직접 deploy ROI 없음.
- 자세히 → [schat-2024-biorxiv_lens-industry.md](schat-2024-biorxiv_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)

- 질문: PMC13061372 버전에는 F1-score 0.886, 111개 질문 benchmark 등이 있다고 이전 abstract 분석에서 기재됨 — 이 preprint(bioRxiv 2024-10-03)와 다른 개정 버전이 있는가? 있다면 해당 버전 PDF 확보 후 재분석 필요.
- 질문: `li-group/scChat` GitHub 코드의 현재 activity와 ATAC/multiome 지원 계획을 확인할 것.
- **다음 액션**: 업데이트된 peer-reviewed 버전이 출판되면 재확인. 현 시점은 동향 파악 레벨에서 마무리.

---
마지막 갱신: 2026-06-10
