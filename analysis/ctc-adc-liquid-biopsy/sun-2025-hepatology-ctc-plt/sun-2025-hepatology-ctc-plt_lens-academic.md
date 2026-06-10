# Lens — Academic — sun-2025-hepatology-ctc-plt
> PDF-based full analysis. 이전 abstract-only 분석을 overwrite. 2026-06-10.

---

## Limitations

### 저자가 명시한 한계

- **임상 코호트 편향**: 수술 절제 환자만 포함. 비수술(전신 치료, 경동맥 화학색전술) 시나리오에서 PLT+CTC의 임상적 의미가 다를 수 있음. 다양한 치료 반응 감시 세팅에서 별도 평가 필요.
- **인간화 마우스 재현 실패**: NK-cell의 성숙·기능·항상성이 기존 인간화 마우스 모델에서 충분히 재현되지 않아 동 실험을 humanized model로 검증하지 못함. 향후 NOG 기반 인간 NK-cell 재구성 strain 개발이 필요.
- **다른 혈액 면역세포와의 관계 미탐구**: CTC가 PLT 외에 macrophage, CTL(세포독성 T세포), neutrophil 등과도 상호작용할 가능성이 있으며, PLT 이외 혈구에 의한 면역 회피 기전은 별도 연구가 필요하다고 명시.
- **CD155+CTC의 다양한 임상 세팅 검증 필요**: CD155+CTC가 anti-TIGIT 면역치료 예후 예측 바이오마커로 기능할 가능성이 언급되었으나, 이를 뒷받침하는 독립 코호트 데이터 없음.

### 분석자가 판단한 한계

- **임상 코호트 규모**: PFS/OS 분석이 n = 20(PLT+CTC n = 14, PLT−CTC n = 6)에 기반. PLT−CTC군 n = 6은 Kaplan-Meier 검정력에 결정적으로 부족하며, 두 군 간 병기·AFP·치료 프로토콜 분포 균형이 본문에 명시되지 않음. 교란변수를 통제한 다변량 분석 없음.
- **다중 비교 보정 미적용**: 저자들이 figure 당 여러 군 비교를 수행했으나 BH/Bonferroni 등 다중 검정 보정 적용 여부가 명시되지 않음. 특히 Figure 5, 6의 다수 군 비교에서 false positive 리스크 존재.
- **간접 공배양 방법 불명확**: 직접 공배양 대비 간접 공배양이 contact-dependency를 증명하는 핵심 대조군인데, 간접 공배양의 물리적 분리 방법(transwell membrane? conditioned media?)이 본문에 명시되지 않음. 완전한 비접촉 보장 여부 불확실.
- **CD155 이외 checkpoint 기여 미탐구**: Figure 3B에서 CD276도 RNA-seq에서 유의하게 상향조절됨. PLT 부착이 CD155 단일 checkpoint만 올리는 것이 아닐 수 있으며, CD276의 기여가 별도 탐구되지 않음.
- **c-Jun binding site의 유일성 미검증**: JASPAR 예측 c-Jun 결합 사이트가 CD155 프로모터에서 유일한 것인지(다른 AP-1 결합 사이트 가능성) 검토되지 않음. MUT 프로모터 실험이 이 특정 사이트의 기여를 보여주지만 전체 AP-1 기여를 완전히 규명하지는 못함.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장 1**: CD155-TIGIT axis가 NK-cell 억제의 "주요" 경로임을 주장하나, CD155-CD96 비교에서 α-CD96가 효과 없음을 보인 것만으로 CD96가 완전히 배제되었다고 볼 수 있는가. TIGIT와 CD96는 동일 ligand(CD155)를 공유하는데, 두 수용체의 세포 표면 발현량 및 친화력 차이를 실험적으로 정량화하지 않음.
- **현재 논문에서 제시한 근거**: α-TIGIT + α-CD96 비교 실험(Figures 6A, B). DNAM1(CD226, activating receptor)과의 관계도 보임(Supplemental S9).
- **더 필요해 보이는 근거**: NK-cell 표면에서 TIGIT 대비 CD96의 발현량 정량(flow cytometry mean fluorescence intensity)과 CD155 결합 친화력 비교.

- **연결이 약한 주장 2**: PLT 부착에 의한 CD155 upregulation이 "FAK 활성화로만" 일어난다는 주장. iFAK 처리 후 CD155가 감소하는 것은 FAK가 필요조건임을 보여주지만, FAK 말고 다른 adhesion kinase(예: Src, ILK) 경유 경로의 기여가 배제되지 않음.

### 정리되지 않은 질문

- 질문: PLT 고갈(Emfret anti-PLT scavenger)이 PLT 이외 세포(예: megakaryocyte 유래 microparticle)에도 영향을 주는지 대조 실험이 있는가?
- 질문: CD155-TIGIT axis가 HCC 외 위암·유방암 CTC에서도 동일하게 작동하는가? 본 논문에서 NSCLC/PDAC CTC의 PLT 부착은 보였지만, CD155 기전과의 연결은 HCC 중심으로만 규명됨.
- 질문: HCC 환자의 수술 중 혈중 CTC 방출(surgical stress) 시 PLT-CTC complex 형성이 급격히 증가하는가? Discussion에서 언급된 시나리오지만 직접 데이터 없음.
- 질문: CD155+CTC 검출이 anti-TIGIT 치료(tiragolumab 병용) 반응 예측 바이오마커로 기능하는가? MORPHEUS-liver trial(NCT04524871) 데이터와 연결 가능성.

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: PLT-CTC adhesion이 면역 회피에서 "물리적 차폐"에서 "능동적 immune checkpoint 전사 유도"로 패러다임을 전환시킨 연구. FAK/JNK/c-Jun→CD155→TIGIT라는 contact-dependent 경로를 분자 수준에서 확립했고, α-TIGIT 차단이 이를 역전한다는 preclinical proof-of-concept 제공.

- **다음 논문으로 이어질 아이디어**:
  1. CD155+CTC를 anti-TIGIT 치료 반응 예측 바이오마커로 검증하는 prospective 코호트 연구. 대상: HCC 또는 다른 고형암에서 tiragolumab 또는 vibostolimab 병용 치료군. Endpoint: PLT+CTC 비율, CD155 발현과 ORR/PFS 상관.
  2. 다른 암종(위암, 췌장암, 유방암) PLT+CTC에서 CD155 기전이 동일하게 작동하는지 범암종 분석. 특히 NCCHE 위암 CTC 데이터셋에서 PVR 발현 확인.
  3. PLT 부착이 CD155 외에 CD276, TNFRSF14 등 다른 immune checkpoint를 얼마나 올리는지 포괄적 immune checkpoint proteome 분석.
  4. iFAK 또는 JNK 억제제가 in vivo CTC CD155 발현을 낮추고 전이를 억제하는지 확인 — FAK/JNK axis의 druggable target으로서 가능성.

- **설명을 더 매끄럽게 만들 방법**:
  - 간접 공배양 방법을 transwell 실험으로 명확히 기술 + conditioned media 실험 병행.
  - 임상 코호트를 200명 이상의 독립 검증 코호트로 확장하고, 다변량 Cox 회귀분석으로 교란변수 통제.
  - NK-cell 표면 TIGIT vs. CD96 발현량과 CD155 결합 경쟁 친화력을 정량 비교.

- **우선순위가 높은 후속 실험 / 분석**:
  - 위암 CTC(NCCHE 데이터)에서 PLT+CTC의 PVR 발현 확인 (분석 기간 1주 이내 가능).
  - HCC 또는 위암 환자에서 수술 전후 PLT+CTC 비율과 CD155 발현 변화 추적 (수술 중 CTC 방출 시나리오 검증).

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- **§Introduction**: "CTC that were adhered with platelets showed significantly boosted resistance against NK-cell killing through overexpression of CD155."
  - 사용 시나리오: 자체 CTC 분석 논문의 Introduction에서 PLT-CTC subtype의 면역학적 기능 차이를 설명할 때.
  - BibTeX key: `@sun2025ctcplt`

- **§Results**: "Among all patients who are CTC-positive, 70% of them exhibited platelet adhesion to CTC, and those patients exhibited a markedly worse prognosis."
  - 사용 시나리오: CTC-PLT complex의 임상적 빈도와 불량 예후를 선행 데이터로 인용할 때.
  - BibTeX key: `@sun2025ctcplt`

- **§Results/Discussion**: "CD155 molecules on CTCs might mediate NK dysfunction by interacting with the immunomodulatory receptors CD96 … or TIGIT on the surface of NK cells … The resistance could be sensitized by blocking TIGIT but not CD96."
  - 사용 시나리오: CD155-TIGIT axis 특이성을 자기 논문의 target 선정 근거로 인용할 때.
  - BibTeX key: `@sun2025ctcplt`

- **§Discussion**: "Our data demonstrated that targeting TIGIT elicits potent anti-metastasis immunity by sensitizing resistant CTCs to NK-cell attack."
  - 사용 시나리오: anti-TIGIT 면역치료의 CTC 제거 전략으로서의 rationale 기술 시.
  - BibTeX key: `@sun2025ctcplt`

### 인용 가능 수치

- HCC CTC 양성자 중 PLT 부착률 70% (§Results, Figure 1D).
  - 사용 시나리오: PLT-CTC complex 발생 빈도의 baseline 수치로 자기 논문에서 인용.
  - BibTeX key: `@sun2025ctcplt`

- PLT+CTC vs. PLT−CTC PFS log-rank p = 0.0257, OS p = 0.0459 (Figure 1E, F).
  - 사용 시나리오: PLT 부착 CTC의 임상적 불량 예후 정량 근거.
  - BibTeX key: `@sun2025ctcplt`

- CD155+ 비율: PLT+CTC 76.0% vs. PLT−CTC 25.0%, chi-square p = 0.011 (Figure 3L).
  - 사용 시나리오: PLT 부착-CD155 발현 연관성의 환자 데이터 수치.
  - BibTeX key: `@sun2025ctcplt`

### 인용 가능 Figure/Table

- **Figure 7 (Graphical Abstract)** — PLT→FAK/JNK→c-Jun→CD155→TIGIT→NK억제→전이의 전체 기전 도식.
  - 사용 시나리오: CTC 면역 회피 기전 overview 슬라이드에서 인용 또는 재도식.
  - BibTeX key: `@sun2025ctcplt`

- **Figure 1E, F (Kaplan-Meier)** — PLT+CTC vs. PLT−CTC 생존 곡선.
  - 사용 시나리오: 자기 논문 clinical relevance 섹션에서 PLT-CTC 불량 예후의 대표 근거 figure.
  - BibTeX key: `@sun2025ctcplt`

- **Figure 5H–J (JASPAR + luciferase)** — c-Jun binding site 예측 + functional validation.
  - 사용 시나리오: CD155 전사 조절 기전 설명 시 방법론적 참고.
  - BibTeX key: `@sun2025ctcplt`
