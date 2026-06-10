# hu-2021-cancer-surfaceome-atlas_lens-academic.md

## Limitations

### 저자가 명시한 한계

- 대부분의 현재 기능 연구가 in vitro 2D 세포 배양 기반이며, high-throughput in vivo 기능 스크리닝은 여전히 부재하다. 저자들은 Discussion에서 이를 명시하며 in vivo functional screening의 시급성을 강조했다.
- 단일 caGESP로 종양 세포를 '완전히 표적'하고 정상 세포를 '완전히 보호'하는 ideal target을 찾는 것은 여전히 어렵다 — 특히 MSLN처럼 폐, 나팔관, 침�샘에서도 저수준 발현이 관찰되는 경우.
- 수용체-리간드 상호작용의 대부분이 ligand-based CAR-T에 추가 통찰을 주지만, 세포간 통신 조절에서 mIAM의 역할을 in vitro/in vivo에서 검증하는 것이 여전히 필요하다.
- 발현 atlas가 mRNA 중심이어서 단백질 번역 후 수정(glycosylation, shedding, cleavage 등)에 의한 표면 접근성 변화를 포착하지 못한다.

### 분석자가 판단한 한계

- **부족한 점 1 — mRNA-단백질 상관의 불완전성**: GESP에서 positive mRNA-단백질 Spearman 상관 비율이 41%로 non-GESP(25%)보다 유의하게 높지만, 41%라는 수치 자체는 60%가 불일치함을 의미한다. 특히 타깃 우선순위 결정에서 발현 데이터만으로 선택된 caGESP가 실제 세포 표면에 단백질로 노출되는지 보장되지 않는다.
  - **왜 중요한가**: ADC나 항체가 결합해야 하는 것은 단백질 에피토프이지 mRNA가 아니다. Mismatch가 큰 유전자를 포함하면 false-positive 타깃이 생긴다.
  - **어떤 증거가 부족한가**: 33개 암종 전체에 대한 matched proteomics data. 현재 CPTAC는 5개 암종만 커버.

- **부족한 점 2 — in vitro CRISPR 필수성의 in vivo 이전 가능성**: 1,200개 cancer cell line에서 측정한 CRISPR 의존성은 3D 종양 구조, 종양 미세환경(immune, stromal), 혈관신생이 없는 2D 환경 산물이다.
  - **왜 중요한가**: 'common essential' 또는 'strongly selective' 분류에 따른 타깃 선택이 in vivo와 다른 우선순위를 줄 수 있다.
  - **어떤 증거가 부족한가**: Patient-derived organoid 또는 in vivo CRISPR 스크린 데이터.

- **부족한 점 3 — AND/iCAR-T 쌍 기능 검증 부재**: 179개 AND CAR-T 쌍과 443개 iCAR-T 쌍의 선택이 전적으로 발현 배타성 z-score 기반이며, 실제 T cell에서 AND/inhibitory gate가 의도한 대로 작동하는지는 확인되지 않았다.
  - **왜 중요한가**: Boolean logic gate CAR-T의 신호 효율이 목표 농도에서 실제로 작동하는지가 임상 개발의 핵심 불확실성이다.
  - **어떤 증거가 부족한가**: Co-culture assay에서 AND gate killing selectivity 측정, 최소 1개 쌍에 대한 마우스 in vivo 실험.

- **부족한 점 4 — 암종별 환자 이질성 무시**: TCGA 기반 집단 평균 발현을 caGESP 식별에 사용했으나, 암종 내 환자 간 발현 이질성이 크다. 집단 수준에서 'cancer-specific'인 caGESP가 개별 환자에서는 발현되지 않거나 정상조직에서도 발현될 수 있다.
  - **왜 중요한가**: 면역치료 타깃은 결국 개별 환자에 적용. Population-level atlas가 개인화 타깃 선택을 보장하지 않는다.
  - **어떤 증거가 부족한가**: Single-patient 수준의 caGESP 발현 분포 분석, 또는 clinical trial 샘플에서의 prospective 검증.

### 설명이 매끄럽지 않은 지점

- **주장**: mIAM의 IFN 신호와의 연관이 종양 면역 조절에서 중요하다.
  - **현재 논문에서 제시한 근거**: ISG 양성 상관 mIAM 비율이 게놈 전체보다 유의하게 높음 (OR=1.5, P=1.9×10⁻⁴). Co-stimulatory/co-inhibitory 분자 농축.
  - **더 필요해 보이는 근거**: IFN 처리 실험 후 mIAM 발현 변화 측정 (perturbation), 또는 mIAM knock-down/overexpression 후 IFN 신호 변화 — 현재 association만 있고 causal direction이 불명확.

- **주장**: 수용체-리간드 발현 공동발현 패턴이 종양형성 중 세포간 통신이 극적으로 변화한다는 증거다.
  - **현재 근거**: Pearson's test 기반 공동발현 99.1%/99.2%. Unsupervised clustering에서 종양과 정상조직의 분리.
  - **더 필요해 보이는 근거**: 실제 리간드 분비/결합 기능 실험, 또는 CellPhoneDB를 넘어서는 scRNA-seq 기반 물리적 세포 접촉 증거.

### 정리되지 않은 질문

- **질문 1**: caGESP 발현이 종양 미세환경 내 비종양 세포(종양 침윤 면역세포, CAF 등)에서의 발현에 의해 얼마나 오염되어 있는가? scRNA-seq 분석이 13개 암종에 한정되어 이 질문이 나머지 20개 암종에서 열려 있다.

- **질문 2**: ADC에 사용되는 타깃 단백질은 세포 표면에서 내재화(internalization)되어야 약물이 세포 내로 전달될 수 있다. Atlas가 내재화 가능성을 평가하지 않는데, 409개 caGESP 중 몇 개가 ADC에 실제로 적합한가?

- **질문 3**: 재발성 게놈 변이(특히 ERBB2 증폭, CTNNB1 돌연변이)와 caGESP 특이 발현이 동일 유전자에서 겹치는 경우, 이 유전자들이 타깃으로서 가장 강력한 근거를 가지는가? 체계적 cross-analysis가 본문에서 명시적으로 제시되지 않았다.

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: 9개 자원 통합 GESP list + 5-알고리즘 caGESP 식별 + 발현·게놈·기능·약물 반응 통합이라는 multi-modal evidence framework를 처음 pan-cancer 규모로 구현했다. TCSA 포털 공개로 연구 커뮤니티가 직접 탐색 가능한 공공재를 만들었다.

- **다음 논문으로 이어질 아이디어**:
  - **아이디어 1 — Proteomics-guided caGESP 정제**: CPTAC 데이터를 5개 암종 이상으로 확장하거나 proximity ligation proteomics를 활용해 409개 caGESP의 단백질 수준 검증 → false-positive 제거 + 내재화 가능성 동시 평가.
  - **아이디어 2 — Patient-level caGESP heterogeneity**: TCGA bulk RNA-seq을 single-patient 수준 deconvolution (또는 단일 세포 수준)으로 분석해 환자 내 caGESP 발현 이질성을 정량화. Responder vs. non-responder 예측 모델과 연결.
  - **아이디어 3 — AND CAR-T 기능 검증 파이프라인**: Atlas 상위 priority 쌍 10~20개를 대상으로 co-culture killing assay → 최소 2~3쌍 mouse tumor model에서 AND gate 특이성 검증 → 임상 우선순위 정제.
  - **아이디어 4 — mIAM IFN 인과 관계 규명**: IFN-γ 처리 또는 STING agonist 처리 후 mIAM 발현 변화를 scRNA-seq으로 측정; mIAM knockdown 후 IFN 신호 변화 → co-stimulatory/co-inhibitory axis와의 인과 연결.
  - **아이디어 5 — ADC internalization atlas**: Atlas의 caGESP에 antibody-drug internalization assay 데이터를 overlay해 ADC에 실제 적합한 타깃 서브셋 정의 (이미 알려진 ADC 타깃 CD30, HER2, TROP2 등을 positive control로).

- **설명을 더 매끄럽게 만들 방법**: AND CAR-T 쌍 섹션에서 priority score 상위 10개 쌍에 대해 기존 임상/전임상 데이터를 직접 교차 참조하면 atlas의 예측 정확도를 더 직접적으로 보여줄 수 있었을 것.

- **우선순위가 높은 후속 실험 / 분석**:
  1. Pan-cancer proteomics (확장된 CPTAC 또는 HPA antibody-based) → mRNA-단백질 불일치 GESP 제거
  2. 상위 5개 AND CAR-T 쌍 co-culture killing assay (종양 세포 + 정상 세포 혼합 조건)
  3. Patient-level caGESP 이질성 분석 (TCGA 기반 혹은 meta-analysis)

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Abstract: "By systematically integrating single-cell and bulk genomics, functional studies and target actionability… we comprehensively identify and annotate genes encoding SPs (GESPs) pan-cancer."
  - 사용 시나리오: 본인 introduction에서 pan-cancer surfaceome 자원의 존재를 인용할 때 (ADC/CAR-T 타깃 발굴 배경).
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

- §Results p.1406: "SPs serve as targets for >60% of approved drugs for human diseases."
  - 사용 시나리오: 세포 표면 단백질의 drug target 중요성을 정량화할 때.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

- §Results p.1408: "only 22.1% of GESPs were ubiquitously expressed across all cancer types; in contrast, 48.4% of non-GESPs… were detectable."
  - 사용 시나리오: GESP의 암 특이 발현 특성을 baseline fact로 제시할 때.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

- §Discussion p.1417: "the currently drugged GESPs in oncology represent only 2.5% of the surfaceome, and preclinical anticancer drug discovery efforts are also focused on a relatively small fraction of the surfaceome."
  - 사용 시나리오: 신규 타깃 탐색의 필요성을 강조할 때.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

- §Results p.1410 (caGESP): "13.4% (55/409) of the caGESPs identified by our systematic approaches have been previously reported as being in advanced clinical development for cancer immune therapy."
  - 사용 시나리오: atlas 방법론의 precision을 clinical validation으로 뒷받침할 때.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

### 인용 가능 수치

- **97.0%** — CAR-T/ADC/항체 임상 타깃이 core GESP score ≥ 4 충족 (§Results, Fig. 1c)
  - 사용 시나리오: GESP 정의의 high precision 근거로.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

- **409개 caGESP, 33개 암종** — cancer-specific GESP 수 (§Results, Fig. 3)
  - 사용 시나리오: surfaceome 타깃 후보 규모 제시.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

- **1,433개 치료 타깃 후보, 평균 86개/암종** (§Results, Fig. 8e)
  - 사용 시나리오: pan-cancer 타깃 발굴 결과의 규모를 인용.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

- **66.8%의 GESPs가 understudied** (Pubtator score < 150; §Results, Fig. 8a)
  - 사용 시나리오: surfaceome 탐색의 미충족 과제를 강조할 때.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

### 인용 가능 Figure/Table

- **Figure 3f** — 33개 암종별 caGESP 목록 및 임상 개발 현황
  - 무엇을 보여주는지: 어떤 암종에 어떤 caGESP가 식별되었고, 임상 개발 tier를 한눈에 확인.
  - 사용 시나리오: 본인 리뷰 또는 연구 배경에서 암종별 타깃 현황 overview로 재현.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

- **Figure 8b** — CAR-T/ADC/antibody/small molecule별 GESP 타깃 비율
  - 무엇을 보여주는지: 치료 모달리티별 GESP 직접 타깃 비율 (CAR-T·ADC 100%).
  - 사용 시나리오: ADC/CAR-T 치료제의 GESP 의존성을 강조할 때.
  - BibTeX key: `@hu2021cancersurfaceomeatlas`

## 1. 학술적 위치

### 연구 계보 (외부 맥락)

- **선행 surfaceome 연구**: 외부 맥락: Bausch-Fluck et al. (2015, MCP) — 세포 표면 단백체 정의를 체계화한 Cell Surface Capture 방법론. Almen et al. (2009) — transmembrane protein 분류 데이터베이스. 이들 방법론 기반 위에 Hu 2021이 암종별 통합 atlas를 구축.
- **TCGA 이후 통합 분석**: 외부 맥락: TCGA 게놈 데이터에 CPTAC 단백체와 HPA 이미징을 통합한 접근은 RNA-protein 상관성의 한계(특히 표면 단백질에서 낮은 상관성)를 극복하는 방법론적 발전.
- **Cancer Cell 위상**: 외부 맥락: Cancer Cell은 종양 생물학 top-tier 저널(IF ~38). 2021년 게재 — ADC 타겟 발굴 연구의 방법론 정립 시점.
- **Fang 2024와의 관계**: 외부 맥락: Hu 2021이 범-암종 surfaceome atlas의 선행 연구이고, Fang 2024는 이를 ADC 타겟 발굴에 특화한 후속 또는 독립 연구로 추정. 두 논문 모두 CytoGen ADC 타겟 참조 자료로 함께 활용.

### 방법론적 기여 (외부 맥락 추정)

- **Multi-modal 통합**: 게놈(TCGA) + 단백체(CPTAC) + 이미징(HPA) 통합은 단일 모달리티 한계 극복.
- **Surfaceome 특화 분류**: 범용 유전체 분석이 아닌 ADC/항체 접근 가능한 표면 단백질에 특화된 분석 틀.
- **면역 연관성**: 표면 단백질과 종양 면역 환경(TME) 연관성 분석 — ADC 단독 또는 면역 병용 전략 설계에 유용.

### 한계 (외부 맥락 추정)

- **RNA-protein gap**: CPTAC 단백체 데이터는 일부 암종에만 존재 — 위암, 담도암 등 NCCHE 주요 암종의 CPTAC 커버리지 확인 필요.
- **CTC 특이성**: 고형암 조직 기반 atlas — 혈행 중 CTC의 실제 표면 단백질 발현이 조직과 얼마나 다른지 직접 주소하지 않음.
- **공간 해상도**: 조직 수준 평균 — 세포 아형(subpopulation) 수준 발현은 scRNA-seq/scProteomics 없이 한계.

### 후속 연구 아이디어 (CytoGen 맥락)

- `질문: NCCHE STAD(위암) CTC에서 발현되는 표면 단백질이 Hu 2021 atlas의 위암 선택성 상위 후보와 얼마나 겹치는가?`
- `질문: 담도암(CHOL), 췌장암(PAAD) 등 희귀 암종의 surfaceome 커버리지는 atlas에서 충분한가?`
- `제안: Atlas supplementary table 확보 후, NCCHE 4개 암종별 CTC 발현 표면 단백질을 atlas 점수와 교차 → ADC 타겟 우선순위 matrix 생성.`

---

## 2. 논문 신뢰도 평가

- **저널 위상**: *Cancer Cell* (IF ~38, top-tier). 2021년 peer-reviewed.
- **저자**: Hu, Z. et al. — 소속 기관 미제공 (전문 확인 필요).
- **검증 체계**: 게놈 + 단백체 + 이미징 3-modal — 다중 검증 설계.
- **공개 데이터 활용**: TCGA / CPTAC / HPA 모두 공개 데이터 — 재현 가능성 높음.
- **권고**: 전문 입수 후 사용 암종 목록 및 NCCHE 해당 암종 커버리지 확인.

---

## 3. 인용 전략

- **인용 맥락**: "외부 범-암종 surfaceome atlas에서 검증된 타겟" 맥락에서 Fang 2024와 함께 인용.
- **인용 키**: `@hu2021cancersurfaceomeatlas`
- **동반 인용 권고**: Fang 2024 (ADC 특화 후속), TCGA 원본 논문.
- **주의**: 전문 입수 전 구체 수치 인용 금지.
