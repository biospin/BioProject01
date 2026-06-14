# Lens — Industry

> 근거: `el-kazwini-2026-crakvelo_core.md` + sources PDF. paper-info.yaml의 categorization 블록과 동기화.
> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 본문 밖 정보·추론은 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` prefix로 분리한다.

## 1. Categorization

### Domain (자동 추출, 검토 표시)
- single-cell-genomics
- RNA velocity
- epigenomics / chromatin accessibility
- regulatory genomics (gene–region interaction, TF enrichment)

### Use case (vocabulary 6개 중 1~3개)
- `pipeline-applicable` — 우리 HSPC 10x Multiome(GSE209878)에 *동일 데이터·동일 cell annotation*으로 바로 적용 가능. 코드(GitHub StatBiomed/CRAK-Velo, Zenodo) 공개.
- `methodology-reference` — UniTVelo 확장형 chromatin-aware velocity. lag 정량은 직접 제공하지 않으나 region weight·region kinetic을 우리 lag 정의로 재가공할 reference.
- `academic-citation` — MultiVelo의 spurious flow 비판, simpler/faster 비교 등 인용 가치 있음(lens-academic Citation 후보 참고).

### Importance (1개 종합 등급)
- Level: 상
- Perspective (1문장): 우리 핵심 dataset(GSE209878 HSPC)에서 MultiVelo 대비 우위를 *동일 셋업*으로 직접 입증한 chromatin-aware velocity로, lag 분석 파이프라인의 1순위 비교 baseline.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크
- **Sample size / 규모**: cell 단위 충분(HSPC 11,605, mouse brain 3,365, HCC 4,693)하나 모두 *공개 reference dataset*. 새 환자 cohort·임상 sample 검증 없음.
- **Replication 부족**: 세 public dataset에서만 검증. 독립 lab·독립 생물학적 replicate 없음. `해석: regulatory-grade evidence로는 부족 — 연구용 분석 도구 수준.`
- **통계 검정 누락**: CBDir·KNN accuracy에 p-value·CI·multiple-testing 보정 없음(core.md Results). enrichment만 log-enrichment/p로 제시. false-positive 통제 불충분.
- **Selection bias**: region을 ≥800(HSPC)/≥400(brain) cells 검출 + TSS ±10kb로 필터 → long-range enhancer 배제, low-coverage gene 손실(HCC 민감성의 원인).

### 2.2 임상·기술적 제약
- **Platform 의존**: paired 10x Multiome(scRNA + scATAC) 전제. unpaired multi-omics 적용 가능성은 본문에 없음(미제공:).
- **계산 자원**: cisTopic Gibbs sampler 선행 단계가 GPU(NVIDIA A100) 권장. CRAK-Velo 본체는 CPU(Intel Xeon Platinum). HSPC end-to-end ~15h(+ cisTopic 3h) — 임상 turnaround에 부적합, 연구용.
- **Turnaround**: 수 시간~하루 단위. 임상 의사결정용 아님.

### 2.3 규제·QA·RA 관점
- **규제 pathway**: 해당 없음 — 연구용 분석 SW. IVD/LDT/SaMD 아님. analytical/clinical validation 데이터 없음(미제공:, 본 자료 목적상 정상).
- **IRB / consent**: Ethical Approval "Not applicable"(공개 데이터 재분석). 인간 sample 직접 사용 없음.
- **Reproducibility for audit**: code(Zenodo DOI + GitHub) + Jupyter notebook 재현 workflow 공개 → 학술 재현성은 양호. 단 FDA-audit 수준 검증(version-locked env, validation report)은 아님.

### 2.4 권위·신뢰 가중치
- `1차 출처:` peer-reviewed Genome Biology(단 "Article in Press — unedited manuscript", 최종 교정 전).
- COI: 저자 "no competing interests". Yuanhua Huang은 Genome Biology Editorial Board Member이나 본 원고 편집에 미관여(명시).
- Funding: AIRC(이탈리아 암연구협회) IG 27631, Next Generation EU(공공). corporate sponsor 없음 → 결과 편향 위험 낮음.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)
- 학술 그룹(SISSA + HKU) 산출 open-source 도구. 라이선싱 대상이라기보다 *자유 활용 자산*(BY-NC-ND 4.0 — 논문; 코드 license는 GitHub 확인 필요, 검토필요:).
- 경쟁사 관찰: chromatin-aware velocity 분야(MultiVelo, MultiVeloVAE, MoFlow 등 repo 내 분석 존재)의 최신 진입자. 우리 epigenomic-lag topic의 method 지형 파악에 유효.

### 3.2 Commercialization-candidate (자체 제품화)
- SW 관점: 자체 제품화 후보로는 약함 — 이미 open 구현 존재, 차별화 어려움. 단 *우리 lag 정량 파이프라인*의 내부 component로 통합하는 것은 가능(제품화가 아닌 R&D 도구화).
- TRL: 4~6(공개 데이터 lab validation 수준). production-ready 아님.

### 3.3 우리 파이프라인과의 fit
- **Dataset 호환: 일치** — 본 논문이 *바로 우리의 GSE209878 HSPC*를 동일 cell annotation으로 사용. head-to-head 비교의 진입 장벽이 거의 없음.
- **자원 가능성**: CPU 기반 본체 + GPU 1장(cisTopic)이면 우리 환경에서 재현 가능 추정(추정: A100급 1장으로 충분, 본문 셋업과 동일).
- **전략 align**: gene별 chromatin–transcription lag → drug response timing이라는 우리 목표에, CRAK-Velo의 region weight·region kinetic은 *lag의 raw material*. 단 lag를 직접 출력하지 않아 후처리 필요(빠진 capability: gene-level lag estimator).

### 3.4 후속 BD·제품 액션 후보
- CRAK-Velo vs MultiVelo head-to-head on GSE209878
  - 누가: 본인(technical) + 분석 팀
  - 언제: 지금 / 이번 sprint
  - 자원: GPU 1장, ~1일 compute(cisTopic 3h + CRAK-Velo 15h), 기존 GSE209878 전처리물
  - 성공 기준: 동일 cell에서 두 method의 velocity field·terminal state·region 해석을 정량 비교한 내부 리포트 1건
- region kinetic → gene-level lag estimator 후처리 모듈 시작
  - 누가: 본인
  - 언제: 다음 분기
  - 자원: CRAK-Velo 출력($w_r^g$, $c_r^g(t)$, pseudotime) 파싱 스크립트
  - 성공 기준: KLF1 등 known gene에서 accessibility-peak ↔ unspliced-peak pseudotime gap을 lag로 산출, 생물학적 타당성 sanity check 통과

## 4. 전문가 코멘트

### 4.1 종합 등급
- Level: 상
- Perspective: 우리 GSE209878 HSPC에서 MultiVelo 대비 우위를 동일 셋업으로 입증한 chromatin-aware velocity — lag 파이프라인의 1순위 비교 baseline.
- 등급 근거:
  - core.md Results §Dataset 1 — 우리와 *동일한 GSE209878 HSPC 10x Multiome*, MultiVelo annotation 그대로 사용 → 비교 진입 장벽 최소.
  - MultiVelo 대비 빠름(HSPC 15h vs >24h, Table S1) + 단순한 모델 + region-level 해석 제공.
  - 코드·재현 notebook 공개(Zenodo + GitHub) → 재현 ROI 높음.
  - 단 chromatin–transcription lag를 명시 parameter로 출력하지 않음 → 우리가 후처리 모듈 추가 필요(빠진 capability).
  - "Article in Press"라 일부 표기 불일치($k$, topic 수, Table 번호) 존재 — 최종본 재확인 권장.

### 4.2 활용 우선순위
- 지금(이번 sprint): GSE209878 head-to-head 비교 착수.

### 4.3 발표·미팅에서 들이밀 시점
- 사내 R&D 리뷰: epigenomic-lag 방법론 비교(MultiVelo vs CRAK-Velo) 결정 자리.
- 본인 논문/제안서 introduction: RNA-only velocity의 한계 + chromatin-aware 대안 비교.

### 4.4 추가 탐색 필요 영역
- 질문: CRAK-Velo GitHub(StatBiomed/CRAK-Velo) license가 무엇인지(상업/내부 활용 자유도 확인). BY-NC-ND는 논문 텍스트 license일 뿐 코드와 별개.
- 질문: 우리 GSE209878에 cell cycle confound 처리가 필요한지 — 본 논문은 다루지 않음. 별도 sub-pipeline 필요 여부 판단.
- 질문: unpaired scRNA + scATAC에도 적용 가능한지(우리가 가진 데이터가 항상 paired인지 점검).
