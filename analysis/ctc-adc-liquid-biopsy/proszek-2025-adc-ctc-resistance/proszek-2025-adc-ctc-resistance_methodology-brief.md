# Methodology Brief — proszek-2025-adc-ctc-resistance

## 한 줄 결론 (모든 독자)

- Citation: `@sledge2025tdxdresistance`  |  Importance: `상` (T-DXd 내성의 real-world large-scale 증거로 ABCC1이 HER2 독립적 내성 biomarker임을 확립)
- 한 문장 결론: Real-world 2,799명 코호트에서 ABCC1(drug efflux pump)과 ERBB2(HER2 target) 발현의 조합이 T-DXd 치료 결과를 최대 2.5배 층화하며, ADC 내성 biomarker 패널 및 ABCC1 억제 병용 전략의 근거를 제공.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: `proprietary` — Caris Life Sciences 독점 데이터. 접근 시 저자(jxiu@carisls.com) letter of intent 필요, 통상 6개월 내 조건부 가능. 공개 재현 불가.
- **코드 공개**: 분석 코드 미공개. WTS pipeline은 공개 툴 사용(STAR v2.7, RRID:SCR_004463; Salmon, RRID:SCR_017036; QuanTISeq, RRID:SCR_022993). Cox regression은 표준 R/Python 구현으로 재현 가능.
- **자원 요구**: WTS: Illumina NovaSeq 6000 (60M reads/sample, min 10% tumor content). NGS: NextSeq 500 또는 NovaSeq 6000 (592 gene panel 또는 WES). 특별한 GPU 불필요. 표준 HPC 환경에서 재현 가능.
- **핵심 의존성**: STAR (alignment), Salmon (TPM quantification), QuanTISeq (TME deconvolution), R (survival package for Cox regression), GraphPad Prism v10.0 (cell viability IC50), Azure 500 (Western blot imaging).
- 자세히 → [proszek-2025-adc-ctc-resistance_core.md](proszek-2025-adc-ctc-resistance_core.md) §Methods, [sources/proszek-2025-adc-ctc-resistance.pdf](sources/proszek-2025-adc-ctc-resistance.pdf) §Methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 부분 일치. CytoGen의 ADC 파이프라인(SEV_BRCA, NCCHE_Gastric)이 WTS 데이터를 보유한다면 ABCC1/ERBB2 TPM 발현 분석 직접 적용 가능. 단 이 논문은 유방암 한정 — 위암·기타 고형암에서의 ABCC1 내성 패턴 외삽 불확실.
- **자원 가능성**: Cox regression + KM 분석은 현재 bioinformatics 팀 역량으로 재현 가능. 문제는 데이터 규모 — 내부 코호트가 수십~수백 케이스 수준이면 같은 분석이 underpowered. Caris 규모(N=2,799)는 현실적으로 달성 불가.
- **비용·시간 추정**: ABCC1/ERBB2 발현 분석 적용(기존 WTS 데이터 활용): 1-2주. In vitro ABCC1 억제 검증 재현: 1-2개월(세포주 확보 + MK-571 구매 포함). 전체 파이프라인 재현: 데이터 접근 기간(6개월) + 분석(2-3개월) = 9개월 이상.
- **ROI 한 줄**: T-DXd 내성 위험 환자 사전 선별(ABCC1 high + ERBB2 low)로 ADC 치료 결정 지원 — 내성 monitoring 서비스 또는 companion diagnostic 개발의 foundation.
- 자세히 → [proszek-2025-adc-ctc-resistance_lens-industry.md](proszek-2025-adc-ctc-resistance_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: 내부 ADC 코호트(SEV_BRCA 또는 NCCHE_Gastric)에서 WTS 데이터가 있는가? ABCC1 발현 분포를 먼저 확인해볼 수 있는지.
- 질문: SMAD4 mutation이 가장 강한 post-T-DXd 농축 신호(q<0.0005)인데 Discussion에서 설명이 없음 — T-DXd-SMAD4 연결에 관한 follow-up literature search가 필요.
- 다음 액션: 내부 ADC 치료 코호트 WTS 보유 여부 확인 + ABCC1/ERBB2 TPM 발현 분포 preliminary 분석 — 이번 분기 내.
- 자세히 → [proszek-2025-adc-ctc-resistance_lens-academic.md](proszek-2025-adc-ctc-resistance_lens-academic.md), [proszek-2025-adc-ctc-resistance_lens-industry.md](proszek-2025-adc-ctc-resistance_lens-industry.md) §4

---

마지막 갱신: 2026-06-10
