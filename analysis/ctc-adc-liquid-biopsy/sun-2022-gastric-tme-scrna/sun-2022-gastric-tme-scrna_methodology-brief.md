# Methodology Brief — sun-2022-gastric-tme-scrna

## 한 줄 결론 (모든 독자)
- Citation: `@sun2022gastrictme`  |  Importance: `중` (위암 TME 최대 규모 paired scRNA-seq atlas; tissue-side reference + CellPhoneDB 파이프라인 재사용 가치. 단일 기관 10명 한계.)
- 한 문장 결론: 위암 10명 환자에서 166,533세포의 matched scRNA-seq atlas를 구축해 TASC-TAM-LAMP3+ DC 상호작용 허브와 Tc17→exhaustion alternative trajectory를 규명한 TME 지도 논문. ADC 타겟 tissue-side reference 및 CellPhoneDB 워크플로우 참조용.

---

## 재현 가능성 체크 (재현 담당자)
- **데이터 접근**: open — BIG Data Center HRA000704 (raw reads); OMIX001073 (processed matrices + cell annotations). 중국 데이터 서버 접근 속도 확인 필요.
- **코드 공개**: https://github.com/Lan-lab/sc-GC — example scripts 제공, license 명시 없음(확인 필요). maintenance 상태 미확인.
- **자원 요구**: SCENIC(GENIE3)은 RAM 128GB+ 권장, 병렬화 필요. RNA velocity(scVelo), CellPhoneDB, MuSiC는 일반 서버(RAM 64GB)에서 가능. GPU 불필요.
- **핵심 의존성**: scanpy ≥ 1.4.5, Seurat 3.1.0, scVelo 0.1.25, SCENIC 1.0.1, CellPhoneDB 2.0, MuSiC (ver. 0.2.0), Cell Ranger 3.1 (10x), inferCNV 0.99.0, Salmon 1.3.
- 자세히 → [sun-2022-gastric-tme-scrna_core.md](sun-2022-gastric-tme-scrna_core.md) §Methods, [sources/sun-2022-gastric-tme-scrna.pdf](sources/sun-2022-gastric-tme-scrna.pdf) §Methods

---

## 우리 적용 가능성 (의사결정자)
- **Dataset 호환**: NCCHE_Gastric (위암 scRNA-seq) — 직접 비교 reference로 활용 가능. SEV_BRCA는 암종이 달라 TASC/Tc17 클러스터 정의는 별도 검증 필요.
- **자원 가능성**: CellPhoneDB + scVelo는 현재 팀 서버로 가능. SCENIC은 RAM 128GB+ 서버 필요 — 현재 환경 확인 후 판단.
- **비용·시간 추정**: CellPhoneDB 재분석 (NCCHE 데이터) 1~2주. SCENIC까지 포함하면 3~4주 추가.
- **ROI 한 줄**: NCCHE_Gastric TME 상호작용 네트워크 검증 + TASC 예후 마커 재현 — ADC 타겟 발굴 pipeline의 tissue-side validation으로 직결.
- 자세히 → [sun-2022-gastric-tme-scrna_lens-industry.md](sun-2022-gastric-tme-scrna_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)
- 질문: Supplementary Data 6 (L-R interaction pairs, MOESM11)에서 HER2/CLDN18.2/FGFR2 관련 L-R 쌍이 있는가? 직접 xlsx 파일 열어서 확인 필요.
- 질문: NCCHE_Gastric 데이터에 CellPhoneDB를 돌릴 때 본 논문과 같은 cell type annotation을 써야 L-R 결과가 비교 가능 — annotation 통일 전략 결정 필요.
- 다음 액션: NCCHE_Gastric 데이터 보유 담당자와 공유해서 TASC gene signature 적용 분석 계획 수립 — 다음 주 내.
- 자세히 → [sun-2022-gastric-tme-scrna_lens-academic.md](sun-2022-gastric-tme-scrna_lens-academic.md), [sun-2022-gastric-tme-scrna_lens-industry.md](sun-2022-gastric-tme-scrna_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
