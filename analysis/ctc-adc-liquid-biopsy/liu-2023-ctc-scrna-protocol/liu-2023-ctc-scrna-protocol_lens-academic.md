# Lens — Academic: liu-2023-ctc-scrna-protocol

> 분석 근거: `sources/liu-2023-ctc-scrna-protocol.pdf` 전문 (26 pp, 2026-06-10 재분석).

---

## Limitations

### 저자가 명시한 한계 (Limitations + Troubleshooting 섹션, pp. 20–24)

- **CTC 수 불안정**: 환자별 PDAC 이질성과 전이 진행 정도에 따라 혈중 CTC 수가 달라, 시험 전 필요 CTC 수를 예측하기 어렵다. 저자 권장: ≥10 mL HPV 혈액 채취 + ≥100 CTCs 확보.
- **Cell viability 감소 리스크**: CTC 분리 전 과정에서 4°C 유지 및 신속 처리(채취 후 1–2 h 내)가 필수. 조직 분리 후에는 1.5 h 내 10x Genomics 투입 권장.
- **EMT-CTC 발현 감소**: EMT를 겪은 CTC는 EpCAM 발현이 감소해 chip에서 포획되지 않을 수 있다. CA19-9 병용이 일부 보완하나 완전하지 않음.
- **Immune checkpoint 기능 미검증**: CellPhoneDB로 동정한 immune checkpoint pair는 전산적 추론이며, 실제로 CTC가 그 분자 쌍을 통해 면역 회피를 실현하는지 in vivo 기능 검증이 없다.
- **Platelet marker 문제(Problem 6)**: CTC marker에 포함된 PPBP, PF4는 혈소판 marker이기도 하다. EMT로 epithelial gene이 감소한 CTC가 혈소판 클러스터로 오분류될 수 있으며, 이를 극복하기 위해 sequencing depth 증가 또는 smart-seq 방법 사용을 제안. inferCNV를 추가 보완 수단으로 권고.
- **CellPhoneDB 기본 output 재현 불일치(Problem 7)**: CellPhoneDB 기본 interaction count 출력이 직접 실행 결과와 다를 수 있음. Interaction weight score 방식이 이를 보완하지만, 코드 재현성 주의 필요.

### 분석자가 판단한 한계

- **단일 기관, 소수 환자 코호트**: 환자 6명 전원 West China Hospital. 다기관/다인종 코호트에서의 재현 미검증. 프로토콜 논문이나 biological claim 일반화에는 불충분.
- **Capture efficiency 정량 부재**: Figure 1G에서 시각 확인만 있고 cells/mL 또는 capture rate(%) 수치가 없다. Protocol 재현 시 자체 calibration 필요.
- **CTC 세포 수 미제공**: t-SNE에서 CTC cluster가 확인되나 cluster 내 세포 수, 환자별 CTC 확보 수 등 정량값이 없어 scRNA-seq statistical power를 평가하기 어렵다.
- **Seurat 파라미터 고정 문제**: resolution = 1.0, PC = 40이 고정값으로 제시됨. 데이터셋 크기 또는 세포 구성이 다른 경우 재최적화 없이 적용하면 over/under-clustering 가능.
- **CopyKAT 정상 대조 설정**: 면역세포를 normal control로 설정하는 방식은 면역세포 자체가 somatic CNV를 보유할 수 있어 편향 가능. 이 한계가 결과에 미치는 영향은 quantify되지 않음.
- **단일 time point**: 채취는 수술 시 1회만 진행. 치료 전후 CTC 변화 또는 치료 중 immune checkpoint 동태는 알 수 없다.
- **Sequencing depth**: 80,000–100,000 reads/cell 요구는 고비용. dropout 많은 CTC의 transcriptome 커버리지가 solid tumor 세포와 같은 수준인지 검증 미제공.

### 설명이 매끄럽지 않은 지점

- **Interaction weight score의 근거**: CellPhoneDB 기본 count 대신 expression-weighted score를 사용하는 근거가 간략히 언급되나, 이 score가 실제 ligand-receptor 기능 활성화와 상관관계를 갖는지 검증 데이터가 없다.
- **CTC marker set의 PDAC 특이성**: Table 1에서 CTC marker로 PTPRC, CD9, TIMP1, PPBP, PF4를 제시하나, 이 중 PTPRC는 CD45(범백혈구 마커)의 gene이고, PPBP/PF4는 혈소판 marker다. PTPRC를 negative marker로, 나머지를 positive marker로 쓴다는 것이 본문 step 61에서 명시되어 있으나 Table 1 제목(CTC marker)과의 일관성이 낮다.
- **EpCAM + CA19-9 chip 효율 비교 데이터**: 이중 항체 chip이 단일 EpCAM chip 대비 얼마나 더 capture efficiency가 높은지 비교 실험이 없다. 논문(ref. 1)에 있을 수 있으나 이 프로토콜에서는 미제공.

### 정리되지 않은 질문

- CTC 세포 수가 100개 미만인 환자의 데이터를 어떻게 처리했는가? 6명 중 일부 환자는 제외된 건지, 아니면 100개 미만으로 진행한 건지 불명확.
- EMT 완료 EpCAM⁻ CA19-9⁻ CTC가 있다면 이 프로토콜이 완전히 놓치는가? 보완 전략이 있는가?
- CellPhoneDB immune checkpoint gene list는 2021년 기준 (파일명 `_20211213.csv`). 이후 새로 발견된 면역관문 분자는 포함되지 않았다고 저자가 명시. 최신 리스트로 업데이트하면 결과가 어떻게 달라지는가?

---

## Final Takeaways

- **이 프로토콜의 가장 큰 의미**: PDAC CTC를 대상으로 한 최초의 wet-lab + 전산 통합 scRNA-seq 프로토콜. 특히 HPV 혈액 + microfluidic chip + CopyKAT + CellPhoneDB를 하나의 흐름으로 묶은 것이 재현 가능한 형태로 문서화된 최초 사례.
- **다음 논문으로 이어질 아이디어**:
  - EpCAM/CA19-9 chip vs. EpCAM-only chip vs. 음성 선별(CD45 depletion) 방식의 capture efficiency + CTC 전사체 비교 연구.
  - PDAC 이외 암종(위암, 유방암 등)에 동일 pipeline 적용 후 CTC immune checkpoint profile의 암종 간 공통점/차이 분석.
  - CTC 분리 → immune checkpoint 분자 발현 CTC를 표적으로 하는 ADC payload 설계에 대한 feasibility 연구 (marker set 직결).
  - CTC에서 동정된 LGALS9:CD47 쌍의 항체 차단 후 NK-mediated CTC killing 기능 회복 실험 (in vitro co-culture).
- **설명을 더 매끄럽게 만들 방법**: capture efficiency 정량 실험 추가; CTC 세포 수 환자별 보고; marker-CNV discordant 세포에 대한 처리 방침 명시.
- **우선순위 높은 후속 실험/분석**: (1) PDAC 이외 암종으로의 marker 교체 후 pipeline 검증, (2) CTC immune checkpoint 분자에 대한 ADC 타깃 가능성 검토 (특히 LGALS9, CD47 blocking scenario).

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Summary: "Circulating tumor cells (CTCs) are regarded as the 'seeds' of tumor metastasis. Identifying immune checkpoints on CTCs is essential for establishing efficient immunotherapies to prevent tumor metastasis."
  - 사용 시나리오: 본인 introduction에서 CTC-immune checkpoint 연구 필요성 근거 인용.
  - BibTeX key: `@liu2023ctcscrnaprotocol`

- §Expected Outcomes: "several unique immune checkpoints between CTCs and immunocytes in the blood circulation, such as CD94-NKG2A: HLA-E, CD94-NKG2C: HLA-E, SIPRA_CD47, LGALS9_CD47, etc."
  - 사용 시나리오: CTC 면역관문 landscape의 구체 분자 목록 인용.
  - BibTeX key: `@liu2023ctcscrnaprotocol`

- §Limitations: "it cannot confirm whether these pairs enable CTCs to evade immune surveillance. Validating the biological function of these immune checkpoints in vivo is necessary."
  - 사용 시나리오: computational interaction 분석의 한계 인용 후 기능 검증 연구 필요성 강조.
  - BibTeX key: `@liu2023ctcscrnaprotocol`

### 인용 가능 수치

- Solid tumor FACS yield: 300,000–500,000 cells/sample (§Expected Outcomes, p. 20)
  - 사용 시나리오: PDAC solid tumor 단일세포 분리 기대 수율로 인용.
  - BibTeX key: `@liu2023ctcscrnaprotocol`
- scRNA-seq 투입 전 ≥100 CTCs 확보 권장 (§step 19 CRITICAL, p. 7)
  - 사용 시나리오: CTC 기반 scRNA-seq의 최소 세포 수 기준으로 인용.
  - BibTeX key: `@liu2023ctcscrnaprotocol`

### 인용 가능 Figure/Table

- **Table 1** (p. 20) — Major cell type marker gene set (8 types)
  - CTC marker 포함 cell type annotation 기준으로 인용. 본인 PDAC 또는 타 암종 분석의 cell type marker 참조 출처.
  - BibTeX key: `@liu2023ctcscrnaprotocol`
- **Table 2** (p. 22) — Immune cell sub-type marker gene set (14 types)
  - 면역 sub-type annotation 근거로 인용. 본인 분석의 immune cell typing 출처.
  - BibTeX key: `@liu2023ctcscrnaprotocol`
- **Figure 5** (p. 23) — CTC–immunocyte immune checkpoint interaction dotplot (Primary/Blood/Metastasis)
  - CTC 면역관문 landscape 시각화 출처. 본인 review/발표에서 CTC-immune crosstalk 도식으로 활용.
  - BibTeX key: `@liu2023ctcscrnaprotocol`
