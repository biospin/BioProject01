# Methodology Brief — sun-2025-hepatology-ctc-plt
> PDF-based full analysis. 이전 abstract-only 분석을 overwrite. 2026-06-10.

## 한 줄 결론 (모든 독자)

- Citation: `@sun2025ctcplt` | Importance: **상** — PLT-CTC immune evasion 기전(FAK/JNK/c-Jun→CD155→TIGIT)을 분자 수준에서 처음 규명한 연구.
- 한 문장 결론: HCC 환자 CTC의 70%가 PLT 부착을 보이고, PLT 직접 접촉이 FAK/JNK/c-Jun cascade로 CD155 전사를 활성화하여 NK-cell TIGIT를 통한 면역 회피를 일으킴; α-TIGIT 처리로 전이 억제 가능.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: RNA-seq raw data — GSA-Human HRA007585 공개 (https://ngdc.cncb.ac.cn/gsa-human). 임상 코호트(환자 혈액) — 기관 윤리위원회 승인 필요. ChimeraX-i120 플랫폼은 자체 개발 장비로 일반 접근 제한.
- **코드 공개**: R 4.0(scRNA-seq/전사체 분석), FlowJo V10(유세포), GraphPad Prism 7(통계) 명시. 분석 코드 GitHub 등 외부 공개 없음(논문 내 미언급).
- **자원 요구**: 해석: 실험 재현을 위해 NK-cell coculture 시스템(xCELLigence Roche), Western blot, luciferase assay, in vivo 마우스 모델 모두 필요. Computational 파트(RNA-seq 분석)는 R/서버 환경으로 재현 가능.
- **핵심 의존성**: ChimeraX-i120(CTC 분리), CellInsight CX5(IF 스캔), xCELLigence RTCA(NK 살상 assay), IVIS(in vivo 이미징), JASPAR(c-Jun binding site 예측), FAK inhibitor(iFAK), anti-TIGIT antibody(R&D Systems #MAB7267-100), CD155 antibody(Abcam ab21851).
- 자세히 → [sun-2025-hepatology-ctc-plt_core.md](sun-2025-hepatology-ctc-plt_core.md) §Methods, [sources/sun-2025-hepatology-ctc-plt.pdf](sources/sun-2025-hepatology-ctc-plt.pdf) §Methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 우리 CTC 분리 프로토콜(EpCAM/Pan-CK/CD45 기반)에 CD41 co-staining 추가 시 PLT+CTC 식별 가능. NCCHE 위암 보관 혈액 검체에서 즉시 적용 가능. h5ad 데이터에서는 PVR(CD155), PTK2(FAK), MAPK8(JNK), JUN 발현 비교 분석으로 computational 확인 가능.
- **자원 가능성**: Computational 분석(h5ad 유전자 발현 비교): 즉시 실행 가능, 1–2시간. Wet lab 확인(CD41+CD155+ IF): CD41 항체(ab21851) 추가 구입 필요, ~1주. In vitro NK-cell coculture 재현: NK-cell 분리 + xCELLigence 필요 → 팀 wet lab 역량 확인 선행 필요.
- **비용·시간 추정**: Computational 확인 즉시. Wet lab 단계 시작 ~ 1주. 전체 재현 실험(NK 기능 assay 포함) ~ 1–2개월.
- **ROI 한 줄**: CTC subtype 분류의 기능적 정당성을 임상 데이터와 분자 기전으로 동시에 지지하는 논문. CD155+PLT+CTC 검출을 anti-TIGIT CDx로 연결하는 preclinical 기반 제공. `pipeline-applicable` + `academic-citation`.
- 자세히 → [sun-2025-hepatology-ctc-plt_lens-industry.md](sun-2025-hepatology-ctc-plt_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 핵심 follow-up 질문:
  - `질문: NCCHE 위암 CTC 보관 검체에서 CD41 공동 staining이 기존 panel에 추가 가능한가? 기존 multiplex panel에 channel 여유 확인 필요.`
  - `질문: MORPHEUS-liver 임상시험(NCT04524871) 결과 데이터에서 CTC CD155 상태가 tiragolumab 반응과 연관되는지 확인한 후속 분석이 공개된 것이 있는가?`
- 다음 액션: NCCHE 위암 h5ad에서 CTC_platelet_assoc vs. CTC_solo 간 PVR 발현 비교 분석 실행 → 지금 즉시 가능. 결과 있으면 발표 Background 슬라이드 갱신.
- 자세히 → [sun-2025-hepatology-ctc-plt_lens-academic.md](sun-2025-hepatology-ctc-plt_lens-academic.md), [sun-2025-hepatology-ctc-plt_lens-industry.md](sun-2025-hepatology-ctc-plt_lens-industry.md) §4

---

마지막 갱신: 2026-06-10
