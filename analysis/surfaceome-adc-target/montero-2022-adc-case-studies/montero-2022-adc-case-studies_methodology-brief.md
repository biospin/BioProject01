# Methodology Brief — montero-2022-adc-case-studies

Liu et al. 2023 Cancer Cell — HLA-E:CD94-NKG2A immune checkpoint in CTC NK evasion (DOI: 10.1016/j.ccell.2023.01.001)

---

## 한 줄 결론 (모든 독자)

- Citation: `Liu et al. 2023 Cancer Cell` | Importance: **상**
- 한 문장 결론: PDAC 간전이 환자 HPV 혈액에서 523개 CTC를 단일세포 프로파일링하여 HLA-E:CD94-NKG2A를 혈행 CTC의 지배적 NK cell 면역 회피 checkpoint로 규명하고, anti-NKG2A 투여(day −1)로 in vivo 폐전이를 63배 감소시켰다.

---

## 재현 가능성 체크 (재현 담당자)

### 데이터 접근

- **Raw scRNA-seq**: NGDC GSA-human HRA003672
- **Processed scRNA-seq**: NGDC OMIX002487
- **Exome WGS**: NGDC GSA-human HRA003687
- **공개 비교 dataset**: GSE117623 (HCC), GSE144561 (PDAC), GSE67939 (BRCA), GSE86978 (BRCA), GSE74369 (COAD), GSE38495 (SKCM), GSE51372 (mouse PDAC), GSE155698, CNP0000095
- **코드**: https://github.com/Jinen22/scRNA-PDAC-CC

### 핵심 소프트웨어 의존성

| Tool | Version | 역할 |
|---|---|---|
| Seurat | v4.0.1 | scRNA-seq normalization, clustering, t-SNE |
| CellPhoneDB | v2.0 | Ligand-receptor interaction analysis |
| CopyKAT | v1.0.5 | CNV-based malignancy inference |
| scBet | v1.0 | Cell type annotation |
| SingleCellSignatureExplorer | v3.6 | Gene set enrichment |
| limma | v3.42.0 | Differential expression |

### 재현 요구 자원

- **계산**: Linux HPC. 74,206 cells scRNA-seq 처리 → RAM 128GB 이상 권장. GPU 불필요 (이 논문 주요 분석은 CPU-based).
- **실험**: C57BL/6 또는 Balb/c nude mice, KPC-Luc cells (구입 또는 in-house), anti-NKG2A antibody (BioXcell #BE0321), IVIS Spectrum imager.
- **CTC 분리**: Microfluidic chip 제작 (PDMS two-layer) — 전문 장비 없이는 FACS (EpCAM/CD45 staining) 대체 가능하나 세포 생존율 하락.

### 재현 난이도 평가

- **scRNA-seq 분석**: 중간 — 코드 공개, 표준 파이프라인. 데이터는 중국 NGDC (해외 접근 제한 가능, VPN/기관 계정 필요 여부 확인).
- **In vivo 전이 모델**: 높음 — IVIS imager 필수, 동물 실험 IACUC 필요. KPC-Luc cells 구입/제작 선행.
- **CTC microfluidic chip**: 높음 — 제작 전문성 필요. FACS 대체 시 재현성 저하 가능.

---

## 우리 적용 가능성 (의사결정자)

### 단기 (0–3개월) — citation / BD reference

- PDAC CTC 면역 회피 기전 literature review에 즉시 인용 가능.
- NK cell immunotherapy + PDAC perioperative 임상 설계 BD 논의 시 근거 논문으로 활용.
- HLA-E surface expression on CTCs → liquid biopsy biomarker 후보 pipeline에 추가.

### 중기 (3–12개월) — 부분 재현 / validation

- **재현 우선 실험**: Figure 3 anti-NKG2A timing (day −1 window) — C57BL/6 + KPC-Luc + anti-NKG2A antibody. 비용 추정: ~$5,000–8,000 (mice, cells, antibody, IVIS 이용료). 기간: 6–8주. ROI: PDAC perioperative immunotherapy 전임상 패키지 기초.
- **PDAC 외 확장 검증**: 한국 PDAC 코호트 (서울아산, 삼성병원 협력 가능 여부 확인) CTC에서 HLA-E/RGS18 발현 validation → 국내 임상 적용 가능성 데이터.

### 장기 (12개월 이상) — 임상 설계

- 외부 맥락: Anti-NKG2A (monalizumab) PDAC 1/2상: perioperative 투여 protocol + CTC HLA-E 발현 level을 바이오마커로 하는 biomarker-selected trial 설계 feasibility 검토.
- CTC HLA-E → ADC payload delivery 실험: HLA-E internalization kinetics + cytotoxic payload efficacy in vitro.

### 비용·시간 요약

| 액션 | 비용 | 기간 |
|---|---|---|
| Citation 작성 (BD pitch) | 0 | 즉시 |
| Figure 3 부분 재현 | ~$5,000–8,000 | 6–8주 |
| 한국 코호트 HLA-E validation | TBD (협력 기관) | 6–12개월 |
| In vitro HLA-E ADC feasibility | ~$3,000–5,000 | 3–4개월 |

---

## 본인 재회고 (분석 담당자)

### 핵심 follow-up 질문

- `질문: HPV 혈액 수집이 임상 표준이 아닌 상황에서, 말초 혈액 CTC에서도 동일한 HLA-E:NKG2A dominant pattern이 관찰되는가?`
- `질문: RGS18-AKT-GSK3β-CREB1 axis에서 임상 단계 억제제(AKTi: ipatasertib, capivasertib; GSK3βi: LY2090314)와 anti-NKG2A의 병용 synergy 데이터 존재하는가?`
- `질문: 한국 PDAC 환자 CTC에서 HLA-E 발현 패턴이 중국 코호트와 동일한가? (KRAS/TP53 mutation spectrum 유사하나 인종별 면역 프로파일 차이 가능)`
- `질문: CTC RGS18 발현을 혈소판 활성화 억제(예: aspirin) 또는 anticoagulant로 억제할 수 있는가? → Low-cost intervention 가능성.`

### 다음 액션 (우선순위 순)

1. BD 피치 자료에 "HLA-E:NKG2A CTC immune checkpoint" figure 추가 (Figure 7 schema 활용)
2. monalizumab 현재 임상 단계 및 PDAC 적응증 공백 확인 (ClinicalTrials.gov 검색)
3. NGDC HRA003672 데이터 접근 가능성 확인 (기관 계정 신청 필요 여부)
4. Figure 3 timing 실험 재현 feasibility — 동물 실험 가능 기관 및 IACUC 현황 확인

---

마지막 갱신: 2026-06-10
