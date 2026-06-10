# Methodology Brief — chen-2024-trop2-ctc-emt

## 한 줄 결론 (모든 독자)

- Citation: `@liao2024trop2ctc`  |  Importance: `중` — TNBC CTC에서 TROP2 EMT-CTC marker 개념 검증, ADC 표적 동일 분자로 BD 관심 높으나 임상 cohort 소규모·EMT-CTC 추가 회수율 미제공.
- 한 문장 결론: TROP2가 TNBC CTC에서 EMT 정도와 비례하여 발현되고 migration/invasion을 촉진함을 세포주 + 임상 혈액 39례로 검증한 개념 검증 논문 — sacituzumab govitecan companion Dx 가능성의 초기 근거.

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: `restricted` — TCGA/GTEx/CPTAC는 공개 접근 가능. 임상 혈액 샘플(n=39)은 "Please contact the corresponding author" 조건부 공개.
- **코드 공개**: `없음` — bioinformatics 분석은 R 4.0.3 + GraphPad Prism 9 사용. 스크립트 미공개. 통계 방법 기술만 있음.
- **자원 요구**: GPU 불필요. 형광 현미경 (자동화 scanning), RNA-ISH 시약, EasySep CTC enrichment kit 필요. qRT-PCR, western blot, transwell 표준 wet lab 장비.
- **핵심 의존성**: CanPatrol CTC assay (Surexam, 상용 플랫폼), RNA-ISH probe 서열 (Table S2 공개), primer 서열 (Table S1 공개), TROP2/EpCAM 항체 (BioLegend 1:100), EasySep Direct Human CTC Enrichment Kit (Stemcell Technology).
- 자세히 → [chen-2024-trop2-ctc-emt_core.md](chen-2024-trop2-ctc-emt_core.md) §Methods, [sources/chen-2024-trop2-ctc-emt.pdf](sources/chen-2024-trop2-ctc-emt.pdf) §Materials and Methods

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 우리 HSPC 10x Multiome dataset과 직접 연결 없음. SEV_BRCA (TNBC CTC 프로젝트)와 높은 관련성.
- **자원 가능성**: 우리 팀 wet lab capacity가 있다면 사전 실험 (spiking assay, qRT-PCR) 가능. CanPatrol 플랫폼 없이는 임상 RNA-ISH 부분 재현 어려움.
- **비용·시간 추정**: in vitro 사전 재현 (spiking + qRT-PCR): 1~2개월. 임상 cohort 확장 연구: 6개월~1년.
- **ROI 한 줄**: TROP2 CTC assay가 sacituzumab govitecan companion Dx로 이어질 경우 BD/규제 가치 높음. 현재는 개념 검증 단계로 추가 투자 결정에 대규모 validation 데이터 필요.
- 자세히 → [chen-2024-trop2-ctc-emt_lens-industry.md](chen-2024-trop2-ctc-emt_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)

- 질문: CK-음성 TROP2-양성 spiking recovery (진짜 EMT-CTC 추가 포착률)를 직접 측정해야 이 논문의 핵심 주장을 검증할 수 있다. 우리가 in-house 설계할 수 있는가?
- 질문: TROPiCS-02 또는 ASCENT 임상 시험에서 TROP2 liquid biopsy biomarker 분석 데이터가 이미 발표된 것이 있는가? 확인 필요.
- **다음 액션**: SEV_BRCA 프로젝트 미팅에서 TROP2 CTC marker 추가 검토를 안건으로 올리고, CanPatrol assay 대안(자체 RNA-ISH 프로토콜 구축 가능 여부) 파악 — 이번 달 안.
- 자세히 → [chen-2024-trop2-ctc-emt_lens-academic.md](chen-2024-trop2-ctc-emt_lens-academic.md), [chen-2024-trop2-ctc-emt_lens-industry.md](chen-2024-trop2-ctc-emt_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
