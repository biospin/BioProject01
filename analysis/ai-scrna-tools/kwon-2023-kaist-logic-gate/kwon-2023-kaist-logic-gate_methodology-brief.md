# Methodology Brief — kwon-2023-kaist-logic-gate

## 한 줄 결론 (모든 독자)

- Citation: `@kwon2023logicgate`  |  Importance: `상` (ADC/CAR 타겟 combinatorial 선발 프레임워크로 우리 BD 파이프라인에 직접 적용 가능)
- 한 문장 결론: 단일세포 atlas 기반 RF-CNN 두 단계로 AND/OR/NOT logic gate별 surfaceome 유전자 쌍을 자동 순위화 — ECF 개념과 PCASA 코드·공개 atlas로 즉시 재현 가능.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: open — meta-atlas https://cellatlas.kaist.ac.kr/cart; OV scRNA-seq GEO GSE192898; 전처리 데이터 Zenodo DOI:10.5281/zenodo.7416669.
- **코드 공개**: https://github.com/kaistomics/PCASA (PCASA v1, 라이선스 미명시 — 상업 활용 전 확인 필요). Python 3.8, Keras 2.6.0, TensorFlow 2.4.1.
- **자원 요구**: CPU 클러스터 (HPC 권장). GPU 필수 아님; CNN 12.9M param, batch 500, 10 epochs. RAM 64GB+ 권장 (1.4M 세포). Runtime 미제공.
- **핵심 의존성**: R — randomForest v4.6.14, ROCR v1.0.11, Seurat v3.2.3, scanpy v1.7.2, SingleR v1.4.0, CopyKAT v0.1.2, geosketch v1.2, BBKNN v1.5.1; Python — Keras v2.6.0, TensorFlow v2.4.1, tf-keras-vis v0.8.0, numpy v1.20.0, pandas v1.4.3, ggplot2 v3.3.5.
- 자세히 → [kwon-2023-kaist-logic-gate_core.md](kwon-2023-kaist-logic-gate_core.md) §Methods, [sources/kwon-2023-kaist-logic-gate.pdf](sources/kwon-2023-kaist-logic-gate.pdf) §Methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 부분 일치 — scRNA-seq tumor + normal matched 데이터 있으면 직접 입력 가능. 위암(GC n=40) cellatlas 포함 확인됨. 우리 CTC RNA-seq이 scRNA-seq 포맷이면 호환 가능.
- **자원 가능성**: CPU 클러스터 있으면 가능. GPU 불필요. PCASA GitHub + Zenodo 데이터로 2주 내 pipeline 재현 가능 수준.
- **비용·시간 추정**: 공개 데이터 재현 1주, 우리 타겟 목록 적용 1–2주 추가 (데이터 포맷 맞추기 포함). 총 2–4주.
- **ROI 한 줄**: 기존 단일 ADC 타겟 목록에 ECF 기준 재평가 + NOT gate inhibitor 후보 발굴로 BD pitch 강화. 개발 비용 낮고 공개 코드·데이터 활용.
- 자세히 → [kwon-2023-kaist-logic-gate_lens-industry.md](kwon-2023-kaist-logic-gate_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: PCASA GitHub 라이선스 미명시 — 상업 활용 전 Penta Medix/Choi JK 연락 필요.
- 질문: cellatlas.kaist.ac.kr에서 위암(GC) 데이터 접근 가능 여부, 우리 NCCHE_Gastric 후보 유전자 ECF 즉시 계산 가능한지 확인.
- 다음 액션: PCASA 코드 설치 + Zenodo 데이터 다운로드 후 OV ECF 재현 — 다음 sprint (~2주). 재현 성공 시 우리 관심 암종 적용.
- 자세히 → [kwon-2023-kaist-logic-gate_lens-academic.md](kwon-2023-kaist-logic-gate_lens-academic.md), [kwon-2023-kaist-logic-gate_lens-industry.md](kwon-2023-kaist-logic-gate_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
