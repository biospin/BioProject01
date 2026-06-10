# Methodology Brief — xie-2024-her2-ctc-concordance

## 한 줄 결론 (모든 독자)
- Citation: `@xie2024her2ctcconcordance`  |  Importance: `중` (조직-CTC HER2 불일치율 32.6% 수치 제공; 소규모 단일 기관으로 재현성 미확보)
- 한 문장 결론: 유방암 조직 HER2⁻ 환자 1/3에서 혈중 HER2+CTC 검출 — TBCD 기반 CTC 재프로파일링이 ADC 처방 확장 및 CTC liquid biopsy 상용화 BD 근거로 활용 가능.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `restricted` — 원저 중국 국립암센터 임상 데이터. Supplementary Table 1 (n=43 개인별 CTC/HER2+CTC 수)은 논문 내 공개. 원시 flow cytometry FCS 파일 미공개.
- 코드 공개: `있음` — "All codes generated for analysis are available" 명시. 단 GitHub URL 미제공. R 4.3.2 사용. 요청 시 저자 contact 필요.
- 자원 요구: GPU 불필요. 표준 유세포 분석기 + flow cytometry 소프트웨어 (IDEAS 6.2 또는 FlowJo). Amnis ImageStream MK II(Luminex)는 imaging 분석용이나 standard flow cytometer로 대체 가능 여부 미확인.
- 핵심 의존성: oHSV1-hTERTp-eGFP 바이러스(저자 제공 또는 자체 제조), anti-CD45(APC-Cy7, Biosciences), anti-HER2(APC, BioLegend), R 4.3.2 (stats, ggplot2).
- **Protocol 병목**: 혈액 채취 → 결과까지 16–24 h 배양 필요. 바이러스 MOI=1 감염, 37°C/5% CO₂ 조건 유지.
- 자세히 → [xie-2024-her2-ctc-concordance_core.md](xie-2024-her2-ctc-concordance_core.md) §Methods, [sources/xie-2024-her2-ctc-concordance.pdf](sources/xie-2024-her2-ctc-concordance.pdf) §2

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: SEV_BRCA, NCCHE_Gastric 코호트 — 유방암·위암 환자 혈액 샘플 4 ml로 즉시 적용 가능. 혈액 채취 후 4°C 보관, 1 h 이내 처리 조건.
- 자원 가능성: 유세포 분석기 보유 필수. 바이러스 시약(oHSV1-hTERTp-eGFP) 자체 제조 또는 Zhang W. 그룹 공여. BSL-2 수준 바이러스 취급 인프라 필요.
- 비용·시간 추정: 파일럿 (n=50) 기준 — 바이러스 입수 + SOP 수립 1–2개월, 검체 처리 1개월, 분석 2주. 총 약 2–3개월.
- ROI 한 줄: CTC HER2 재프로파일링 서비스/CDx 개발 초기 타당성 확인용 파일럿으로 투자 대비 효용 있음. 단 대규모 재현 전 임상 결정 근거로는 부적합.
- 자세히 → [xie-2024-her2-ctc-concordance_lens-industry.md](xie-2024-her2-ctc-concordance_lens-industry.md) §3

## 본인 재회고 (본인)
- 질문: Zhang W. 그룹의 oHSV1-hTERTp-eGFP 특허 현황 및 시약 공여 또는 라이선싱 조건은?
- 질문: TBCD의 false positive rate (건강 공여자 대상 specificity)가 공개된 다른 논문(Zhang 2016, 2021, 2022)에서 얼마인가? 임상 적용 전 반드시 확인.
- 다음 액션: Zhang W. (zhangwen@cicams.ac.cn) 또는 Shulian Wang (wangsl@cicams.ac.cn)에게 협업 타진 이메일 — 다음 분기.

---
마지막 갱신: 2026-06-10
