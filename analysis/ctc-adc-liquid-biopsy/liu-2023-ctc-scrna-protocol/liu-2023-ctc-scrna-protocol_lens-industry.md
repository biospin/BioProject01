# Lens — Industry: liu-2023-ctc-scrna-protocol

> 분석 근거: `sources/liu-2023-ctc-scrna-protocol.pdf` 전문 (26 pp, 2026-06-10 재분석).

---

## 1. Categorization

> paper-info.yaml의 categorization 블록과 동기화됨.

### Domain

- CTC-biology
- single-cell-genomics
- liquid-biopsy
- pancreatic-cancer (PDAC)
- immune-checkpoint
- cell-cell-communication

### Use case

- `methodology-reference` — CTC wet-lab 분리 SOP + scRNA-seq QC pipeline을 직접 차용 가능.
- `pipeline-applicable` — Seurat + CopyKAT + CellPhoneDB interaction weight score 흐름이 우리 CTC ADC 파이프라인에 바로 적용 가능.
- `academic-citation` — CTC immune checkpoint 연구의 레퍼런스 프로토콜로 인용 가치 있음.

### Importance

- **Level**: 중
- **Perspective**: PDAC CTC scRNA-seq의 표준 wet-lab + 전산 프로토콜로 CTC ADC 파이프라인 SOP 설계 시 직접 참조 가능하나, 단일 기관 6명 코호트 + 단일 상업 chip 종속이 generaliz ability와 독립 재현성을 제한.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**: 환자 6명. PDAC 간전이 특정 서브그룹이며 단일 기관 환자. 전체 PDAC 환자군 일반화 불충분.
- **Cohort 편향**: 중국 단일 기관(West China Hospital, Sichuan University). 다인종·다지역 코호트 미포함. 면역 반응의 인종 차이를 반영하지 못할 수 있음.
- **Replication 부족**: 결과가 한 기관 데이터셋에서만 보고됨. 다른 기관에서의 wet-lab + 전산 재현 미확인. 해석: replication 부족, regulatory grade evidence로 부족.
- **CTC 수 정량 미제공**: capture efficiency (cells/mL, %) 수치가 없어 assay performance QA 평가 어려움.
- **Multiple testing**: CellPhoneDB permutation test (100 iterations, p < 0.05 필터) 사용. 면역관문 pair 수 기준 multiple testing correction(BH/Bonferroni) 적용 여부 미명시.

### 2.2 임상·기술적 제약

- **HPV 혈액 채취의 침습성**: hepatic portal vein 혈액은 간 수술(laparoscopic surgery) 중에만 채취 가능. 수술 기회 없는 환자나 간전이 미동반 환자에는 적용 불가. 외래 또는 routine blood draw로 대체 불가.
- **Microfluidic chip 종속**: MerryHealth(중국 항저우) 단일 공급사 제품에 종속. 유통망·공급 안정성·규제(ISO, CE) 인증 여부 확인 필요.
- **CTC 희귀성 및 수율 불안정**: 환자별 CTC 수 이질성이 크고, 100개 미만 CTC 시 scRNA-seq 적용 불확실. 임상 루틴 적용 시 실패율 예측 어려움.
- **Turnaround time**: CTC 분리 ~2 h + scRNA-seq ~2 days + 전산 분석 ~5 days 이상. 임상 의사결정 속도에 맞지 않음.
- **전산 자원**: CopyKAT (`n.cores = 20`), CellPhoneDB Python CLI 사용. 20코어 이상 서버 필요. 표준 임상 환경에서는 제약.

### 2.3 규제·QA·RA 관점

- **Analytical validation 미제공**: 포획 효율, 특이도(EpCAM⁺ CD45⁻ 세포 중 실제 CTC 비율), LOD, reproducibility (inter-assay, inter-operator) 데이터 없음.
- **Clinical validation 없음**: 이 프로토콜이 임상 결과(OS, 치료 반응)와 연관되는지 임상 데이터 없음.
- **IRB**: West China Hospital Ethics Committee 승인 명시됨. Informed consent 명시됨. 다른 기관 적용 시 별도 IRB 필요.
- **IVD/LDT pathway**: 현재 research-use-only (RUO) 수준. FDA IVD 또는 LDT 경로 진입을 위해서는 analytical + clinical validation 전체 수행 필요.
- **코드 공개 수준**: GitHub (Jinen22/scRNA-PDAC-CC) + Zenodo (DOI 명시). FDA audit 수준의 version control/locked pipeline은 아님.

### 2.4 권위·신뢰 가중치

- **1차 출처**: peer-reviewed STAR Protocols (CellPress, Open Access). STAR Protocols는 재현 가능한 프로토콜을 전문으로 하는 저널로 방법론적 신뢰도는 높은 편.
- **Peer review 여부**: 있음 (published 2023-09-15).
- **저자 이해상충**: 저자들이 MerryHealth chip의 이해관계자인지 미명시. 해당 chip을 독점적으로 사용하는 것은 편향 가능성 있음.
- **Funding**: National Key R&D Program of China (2022YFC2504700/2022YFC2504703), NSFC, Key Program Sichuan Province 등 공공 재원.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity

- **MerryHealth chip**: Hangzhou MerryHealth의 EpCAM + CA19-9 dual antibody chip이 CTC 포획의 핵심 소모품. 이 chip의 라이선싱·공급 협력이 pipeline 재현 및 상용화의 전제 조건. 현재 중국 기업으로 국내(한국) 유통망 및 규제 허가 여부 확인 필요.
- **저자 공동연구 가능성**: West China Hospital 그룹(Ma, Shi 랩)은 PDAC CTC 분야에서 활발히 연구 중 (ref. 1 = Cell 41:272–287). 공동연구·방문 연구 가능성 있음.
- **경쟁사 동향**: 해석: CTC scRNA-seq 분야에서 10x Genomics + Foundation Medicine + Guardant Health 등이 CTC liquid biopsy에 투자 중이나 PDAC 특화 immune checkpoint profile 제품화는 아직 초기 단계. 이 프로토콜의 immune checkpoint pair 데이터는 향후 ADC/immuno-oncology 타깃 선정에 활용 가능.

### 3.2 Commercialization-candidate

- **Assay/Service**: CTC 분리 + scRNA-seq + immune checkpoint panel 분석을 PDAC 또는 타 암종의 CRO/CDx 서비스로 구성 가능. TRL: 3–4 (proof-of-concept, 단일 기관 시연 수준).
- **SW/Pipeline**: Seurat + CopyKAT + CellPhoneDB interaction weight score 파이프라인을 SaaS 또는 내부 분석 SW로 패키징 가능. IP 자유도 높음 (모두 오픈소스).
- **ADC 타깃 후보**: CTC 면역관문 분자(LGALS9, CD47, HAVCR2 등)는 ADC payload 타깃 후보. 단 functional validation 없어 TRL 2 수준.
- **IP 자유도**: 알고리즘 및 코드 오픈소스(CC BY-NC-ND). wet-lab protocol 자체는 MerryHealth chip 이외 부분에서 구현 가능.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**: 우리 CTC ADC 파이프라인에 10x Genomics 3' scRNA-seq를 사용한다면 직접 적용 가능. scRNA-seq 후처리(Seurat/CopyKAT/CellPhoneDB) 단계가 동일 툴체인.
- **팀 역량**: bioinformatics R + Python 역량이 있으면 전산 파이프라인 재현 가능. wet-lab(microfluidic chip, FACS)은 기존 역량 확인 필요. MerryHealth chip 조달 필요.
- **전략 align**: CTC ADC 타깃 발굴 목적에 직결. CTC 특이적 surface molecule(immune checkpoint) 중 ADC 타깃으로 전환 가능한 후보 선별에 이 프로토콜의 marker set 및 immune checkpoint pair 데이터를 활용 가능.
- **빠진 capability**: HPV 혈액 채취를 위한 간 수술 access. MerryHealth chip 조달. 수술 환경 없으면 말초혈 + alternative capture method로 수정 필요.

### 3.4 후속 BD·제품 액션 후보

- **CTC 분리 프로토콜 SOP화**
  - 누가: 본인 + wet-lab 담당자
  - 언제: 다음 분기
  - 자원: MerryHealth chip 구매 문의, FACS 장비 확인, 1–2 PDAC 또는 위암 환자 샘플 확보
  - 성공 기준: 내부 SOP 문서화 + 1회 pilot run 완료

- **CTC scRNA-seq 전산 파이프라인 내재화**
  - 누가: bioinformatics 담당 (본인 또는 류재면)
  - 언제: 이번 sprint (~2주)
  - 자원: GitHub 코드 clone + OMIX002487 데이터 다운로드 + 서버 20 cores
  - 성공 기준: OMIX002487 데이터로 Figure 3 재현

- **Immune checkpoint pair → ADC 타깃 shortlist 작성**
  - 누가: 본인 (분석) + BD lead (타당성 검토)
  - 언제: 다음 분기
  - 자원: Figure 5 데이터 + CTC ADC 선행 문헌 5편
  - 성공 기준: LGALS9, CD47, HAVCR2, TIGIT 4개 후보에 대한 ADC 타깃 feasibility 1-pager

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 중
- **Perspective**: PDAC CTC scRNA-seq 표준 프로토콜로 CTC ADC 파이프라인 SOP 및 bioinformatics baseline 설계에 직접 참조 가능. 단 소규모 코호트 + 상업 chip 종속 + analytical validation 미제공으로 독립 재현성에 한계.
- **등급 근거**:
  - 전과정 step-by-step 프로토콜 공개 + GitHub + Zenodo 코드·데이터 접근 가능 → 재현 시도 가능.
  - CTC immune checkpoint pair (LGALS9:CD47, CD94-NKG2A:HLA-E 등)가 우리 ADC 타깃 선정에 직접 연결.
  - MerryHealth chip 의존성 + 6명 cohort + analytical validation 없음 → 즉시 임상/BD 활용 어려움.
  - HPV 혈액 채취는 수술 접근 필요 — routine liquid biopsy로 확장 불가.

### 4.2 활용 우선순위

- **지금 (이번 sprint)**: 전산 파이프라인(GitHub 코드 + OMIX002487 data) 재현 시도. Seurat + CopyKAT + CellPhoneDB interaction weight score 흐름을 내재화.
- **다음 분기**: CTC wet-lab SOP화 검토. MerryHealth chip 대안(in-house EpCAM/CA19-9 chip 또는 타 상업 제품) 조사. Immune checkpoint pair → ADC 타깃 shortlist 작성.
- **장기**: CTC scRNA-seq 기반 ADC 타깃 검증 (in vitro 기능 실험). PDAC 이외 암종(위암, 유방암)으로 확장 시 marker set 업데이트.

### 4.3 발표·미팅에서 들이밀 시점

- **CTC ADC pitch/BD 미팅**: CTC 분리 → scRNA-seq → immune checkpoint 동정 흐름의 기술 근거로 인용. Figure 5 circle plot이 시각적으로 설득력 있음.
- **사내 R&D 리뷰 (pipeline SOP 결정)**: CTC wet-lab 표준 SOP 제안 근거 문서로 활용.
- **학회 발표 (introduction/background)**: PDAC CTC immune checkpoint landscape 선행 데이터 인용.

### 4.4 추가 탐색 필요 영역

- 질문: MerryHealth CTC chip의 한국 유통 및 규제 허가 상태. 대안 공급사(예: Veridex/J&J CellSearch, Miltenyi CTC isolation kit) 비교 필요한가?
- 질문: 6명 외 추가 PDAC 환자에서 동일 immune checkpoint pair(LGALS9:CD47, CD94-NKG2A:HLA-E)가 재현되는가 — Liu et al. 2023 Cell 논문(ref. 1) 원문에서 확인 필요.
- 질문: CTC 분리 없이 말초혈 PBMC에서 scRNA-seq 후 CTC를 in silico 동정하는 방법(예: EpCAM⁺ cluster)과 이 프로토콜의 결과가 얼마나 일치하는가?
