# Methodology Brief — topa-2025-tnbc-ctc-emt

## 한 줄 결론 (모든 독자)
- Citation: `@mishra2025epitope`  |  Importance: `상` (CTC ADC on-treatment monitoring 개념 첫 전향적 검증; SEV_BRCA ADC pipeline 확장 직결)
- 한 문장 결론: TROP2/HER2-ADC 치료 중 단일 CTC에서 epitope는 내성 시 유지되며, Day 21 CTC 급감이 durable response의 조기 marker다. CTC-iChip + multispectral imaging 플랫폼의 ADC companion diagnostic 가능성을 처음 전향적으로 제시.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: request-based open (Open Science Framework, 요청 시 공개 예정). 환자 데이터 직접 다운로드 불가.
- 코드 공개: 없음. 이미지 분석은 상업 소프트웨어(HALO, Akoya InForm) 사용. 오픈소스 구현 없음.
- 자원 요구: PhenoImager HT (Akoya Biosciences) 또는 동급 40× multispectral imaging system 필수. CTC-iChip 하드웨어 (TellBio 상용 제품 또는 자체 제작). 계산 자원은 CPU 수준으로 GPU 불필요.
- 핵심 의존성: Akoya InForm (spectral unmixing), HALO image analysis platform (cell segmentation), CTC-iChip (하드웨어), Streck tubes (혈액 고정), Epredia EZ Megafunnels + Thermo Shandon Cytospin 4.
- 자세히 → [topa-2025-tnbc-ctc-emt_core.md](topa-2025-tnbc-ctc-emt_core.md) §Methods, [sources/topa-2025-tnbc-ctc-emt.pdf](sources/topa-2025-tnbc-ctc-emt.pdf) §Materials and Methods

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: SEV_BRCA 코호트 내 TROP2-ADC/HER2-ADC 치료 전이성 유방암 환자 식별 필요. 혈액 serial draw 프로토콜(D0, D21, 진행 시) IRB 포함 여부 확인 필요.
- 자원 가능성: CTC isolation 기술 보유 시 TROP2 (AF555) + HER2 (AF594) staining channel 추가로 기존 panel 확장 가능. PhenoImager 또는 동급 multispectral imaging 장비 미보유 시 도입 또는 CRO 위탁 필요.
- 비용·시간 추정: 항체 sourcing + SOP 설계 ~1개월; 세포주 calibrator 기반 cutoff 검증 ~1개월; 파일럿 환자 n=10 모집 및 분석 ~1분기. 총 ~2–3분기 소요.
- ROI 한 줄: ADC companion diagnostic 시장 선점 및 SEV_BRCA pipeline 임상 가치 증대를 위한 낮은 진입 비용의 staining panel 확장 — 기존 CTC platform 인프라 재활용 가능.
- 자세히 → [topa-2025-tnbc-ctc-emt_lens-industry.md](topa-2025-tnbc-ctc-emt_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)
- 질문: HR 신뢰구간이 1을 포함하는데 (TROP2: 0.65–26.35; HER2: 0.58–145.4), 대규모 validation 없이 Day 21 CTC monitoring을 임상 의사결정 기준으로 사용하는 것이 정당화될 수 있는가?
- 질문: TellBio ADC CDx 개발 진행 상황과 MGH 특허 범위가 우리 TROP2/HER2 staining panel 독자 개발에 법적 장벽이 되는가?
- 다음 액션: TellBio ClinicalTrials/Crunchbase 검색 (1주 내) + SEV_BRCA 코호트 내 ADC 치료 환자 수 및 IRB 적용 가능 범위 확인 (2주 내).
- 자세히 → [topa-2025-tnbc-ctc-emt_lens-academic.md](topa-2025-tnbc-ctc-emt_lens-academic.md), [topa-2025-tnbc-ctc-emt_lens-industry.md](topa-2025-tnbc-ctc-emt_lens-industry.md) §4

---
마지막 갱신: 2026-06-10

## 핵심 방법

| 항목 | 내용 |
|------|------|
| 연구 설계 | 전향적 종적(prospective longitudinal) 관찰 연구 |
| 환자 수 | 33명 (전이성 유방암, TROP2 또는 HER2 표적 ADC 치료) |
| CTC 분석 방법 | 정량적 이미징(quantitative imaging) — 단일 CTC 단백질 발현 정량 |
| 측정 마커 | TROP2, HER2 (단백질 수준, 형광 강도 기반 추정) |
| 채혈 시점 | 치료 전(베이스라인), 치료 시작 3주 후, 진행(progression) 시점 |
| 비교 기준 | 매칭 종양 생검(matched tumor biopsy) |
| 임상 엔드포인트 | TTP(Time to Progression), HR(Hazard Ratio) |
| 통계 | Cox 비례위험 모델 (방법 상세 `미제공:`) |
| CTC 분리법 | `미제공:` — 외부 맥락: MGH Toner 그룹 = 마이크로플루이딕스(CTC-iChip 등) 전문 |

---

## 입력 데이터

- **임상 샘플**: 전이성 유방암 환자 33명 말초 혈액, 다시점 채혈
- **대조군**: 치료 전 베이스라인 CTC (각 환자 자신이 대조)
- **외부 비교**: 매칭 종양 생검의 TROP2/HER2 발현
- **에피토프 전환군**: `미제공:` — TROP2→HER2 또는 반대로 전환한 환자 수

---

## 우리 파이프라인 변경 사항

### 직접 재현 가능한 분석 (scRNA-seq 버전)

1. **TROP2/HER2 발현 종적 비교 모듈**:
   - SEV BRCA 코호트에서 CTC 양성 세포의 TROP2/HER2 전사체(log1p) 분포 시각화.
   - 치료 전 vs 치료 후(가능한 경우) 발현 분포 비교 → Mishra 2025 단백질 결과의 전사체 수준 검증.
   - 파일: `scripts/XX_trop2_her2_ctc_monitoring.py`

2. **Payload 내성 유전자 패널 분석** (Mishra 2025가 제기한 "payload 내성" 가설 검증):
   ```python
   PAYLOAD_RESISTANCE_GENES = [
       'ABCB1',   # P-glycoprotein (MDR1) — DXd efflux
       'ABCG2',   # BCRP — SN-38 efflux
       'ABCC1',   # MRP1 — broad efflux
       'TOP1',    # Topoisomerase I — DXd/SN-38 표적
       'SLC46A3', # lysosomal transporter — ADC 내재화
   ]
   # CTC 서브타입별 발현 → payload 내성 위험도 스코어
   ```

3. **CTC 수 × 전사체 상관 분석**:
   - Mishra 2025의 "3주 CTC 수 감소 = 반응 예측"을 scRNA-seq에서 CTC 클러스터 비율 변화로 대리 측정.
   - `analysis/XX_ctc_count_response_correlation/`

### 파이프라인 표준화 추가 사항

- `src/adc_targets.py` 에 payload 내성 유전자 패널 추가:
  - `PAYLOAD_RESISTANCE_GENES` dict: `{'DXd': ['TOP1', 'ABCB1', 'SLC46A3'], 'SN-38': ['TOP1', 'ABCG2', 'ABCC1']}`
- `tier_v2` 분류 시 payload 내성 유전자 과발현 CTC = "내성 위험군" 플래그 추가.

### 적용 시 주의사항

- **단백질 vs 전사체**: Mishra 2025는 단백질 정량 — TROP2/HER2 mRNA-단백질 상관관계 낮을 수 있음(post-transcriptional regulation). 직접 비교 시 이 한계 명시.
- **EpCAM 의존성**: Mishra 2025의 CTC 분리법이 EpCAM 의존이면 EMT-CTC 누락 가능 → CytoGen의 EpCAM-independent 분석이 보완적.
- **n=33 소규모**: 통계적 검정력 한계 — CytoGen 자체 SEV/NCCHE 분석에서 재현 시 샘플 수 명시.
- **Preprint**: 최종 출판 후 방법론 변경 가능 — 수치 사용 전 재확인.
