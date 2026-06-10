# Methodology Brief — hawkins-2025-her2-emt-mammary

> 근거: 전문 PDF `sources/hawkins-2025-her2-emt-mammary.pdf` (12 pages). 본 분석은 PDF 원문에 기반하며 abstract 기반 이전 버전을 덮어씀.

---

## 한 줄 결론 (모든 독자)

- Citation: `@hawkins2025her2emmammary` | Importance: `중상` (EMT-driven HER2 silencing in vivo 최신(2025) 직접 증거. 소표본·p-value 미제공·특화 저널이 한계)
- 한 문장 결론: HER2 증폭 metaplastic breast carcinoma에서 자연 발생 및 TGFβ1 유도 EMT 모두 FISH 증폭을 유지하면서 HER2 mRNA·단백질을 소실시킨다 — CTC HER2 발현 모니터링 및 ADC resistance 맥락에서 `academic-citation` + `BD-opportunity` 활용.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: 인체 조직 — 기관 소유(Meharry/Ohio State IRB). 공개 accession 없음. 세포주 실험 재현은 HTB20(ATCC BT-474), MCF7(ATCC) 구매로 가능.
- **코드 공개**: 없음. "No datasets were generated or analysed." 프로토콜만 Methods에 기술.
- **자원 요구**: GPU 불필요. LCM 장비(Pixcell II) + Zeiss epifluorescence + FISH probe(Vysis) 필요. ABI 7500 Real-Time PCR. 표준 분자병리 환경에서 재현 가능.
- **핵심 의존성**: TGFβ1 (1–10 ng/ml, 48–72 h + serum starvation), HTB20 세포주, HER2 FISH probe(Vysis Spectrum Orange), Streptavidin-Biotin Complex/DAB IHC system, ABI SYBR Green RT-PCR, ImageJ for signal quantification.
- 자세히 → [hawkins-2025-her2-emt-mammary_core.md](hawkins-2025-her2-emt-mammary_core.md) §Methods, [sources/hawkins-2025-her2-emt-mammary.pdf](sources/hawkins-2025-her2-emt-mammary.pdf) §Materials and methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: SEV BRCA CTC scRNA-seq에서 ERBB2 mRNA + EMT score 산출 가능 — 이 논문 분석의 in silico 버전 재현 가능. HER2 증폭 MC 조직은 직접 접근 불가.
- **자원 가능성**: scRNA-seq 분석 파이프라인으로 ERBB2 vs. EMT gene signature 상관 분석 — 현재 환경에서 즉시 가능. Wet lab(CTC IHC/FISH) 확인은 외부 CRO 필요.
- **비용·시간 추정**: In silico 분석(SEV BRCA CTC에서 EMT-ERBB2 상관) — 1–2일. Wet lab 재현(HTB20 + TGFβ1) — 2–4주 (세포 배양 포함). MC 조직 수집 — 구조적 불가(희귀 케이스).
- **ROI 한 줄**: 직접 파이프라인 적용보다 academic-citation + BD 메시지 보강 가치가 크다. "HER2 ADC 내성 = EMT-driven silencing" 논거의 in vivo 최신 근거로 즉시 사용 가능.
- 자세히 → [hawkins-2025-her2-emt-mammary_lens-industry.md](hawkins-2025-her2-emt-mammary_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: SEV BRCA 코호트 CTC scRNA-seq에서 ERBB2 mRNA vs. EMT score Spearman 상관이 실제로 음수인가? — 이것이 양성이면 Hawkins 2025 적용 범위를 넓힐 수 있고 음성이면 MC 특이적 현상임을 시사.
- 질문: Daiichi-Sankyo BD 미팅 슬라이드에 Jordan 2016 + Nami 2021 + Hawkins 2025 삼각 논거 슬라이드 1장을 언제 추가할 것인가?
- 다음 액션: SEV BRCA CTC scRNA-seq에서 ERBB2 발현 vs. VIM/FN1/TWIST1 EMT score 상관 분석 실행 — 이번 sprint 내.
- 자세히 → [hawkins-2025-her2-emt-mammary_lens-academic.md](hawkins-2025-her2-emt-mammary_lens-academic.md), [hawkins-2025-her2-emt-mammary_lens-industry.md](hawkins-2025-her2-emt-mammary_lens-industry.md) §4

---

마지막 갱신: 2026-06-10
