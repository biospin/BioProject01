# Lens — Industry — Martin et al., 2023 (HSPC Chromatin Dynamics)

> 근거: `martin-2023-hspc-chromatin_core.md` 및 원문 PDF. Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.

## 1. Categorization
> paper-info.yaml의 categorization 블록과 동기화.

### Domain (자동 추출)
- hematopoiesis, epigenomics, chromatin accessibility, ATAC-seq, cis-regulatory element (CRE)

### Use case (vocabulary 6개 중)
- **academic-citation** — chromatin priming(접근성이 발현·계통확정에 선행)의 primary 근거. activation lag 가설 introduction·background에서 인용.
- **methodology-reference** — 13 cell type을 master peak-list로 통합 → primed CRE의 trajectory별 유지를 정량하는 분석 설계, CRISPRi mouse(dCas9-KRAB)로 CRE→유전자 functional link 검증하는 프로토콜을 우리 파이프라인에 차용·변형 가능.
- (제외) pipeline-applicable은 아님 — mouse bulk ATAC + 외부 expression 조합으로, 우리 Human 10x Multiome에 *그대로* 돌아가지 않음.

### Importance (1개 종합 등급)
- Level: **중**
- Perspective(1문장): `해석:` HSPC 분화 축의 chromatin priming을 primary로 보이고 CRISPRi로 functional 검증까지 연결해 우리 lag 가설의 방향성 배경·방법 참조 가치가 높으나, paired RNA·시간 단위 lag 정량과 human·임상 직접 자산은 없어 '상'은 아니다.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크
- ATAC peak count·cumulative signal이 input cell 수·library depth에 민감한 지표인데 본문의 정규화 절차 수치 제시가 약함(`검토필요:`). "HSC가 가장 열림"을 내부 자료/제안서에 인용 시 이 confound를 함께 표기.
- replicate $n=2$, HSC 2 sample이 hierarchical clustering에서 비인접(p.535) → 통계적 검정력·재현성이 제한적. 정량 수치를 단정적 baseline으로 쓰기 전 caveat 필요.
- genome-wide priming claim의 functional 인과는 CRISPRi 3개 locus(CD81/CD115/CD11b)에만 근거 — generalization 제한.

### 2.2 임상·기술적 제약
- mouse(C57BL/6) 모델. human hematopoiesis로의 직접 외삽은 ortholog/CRE 보존 검증이 선행되어야 함(`미제공:` human 데이터 없음).
- bulk ATAC-seq — population 평균. 임상 sample의 rare population·heterogeneity 분해에는 single-cell 전환 필요.
- CRISPRi readout이 cell-surface protein(CD81/CD115/CD11b)의 flow cytometry — endogenous transcription/RNA를 직접 측정한 것이 아님.

### 2.3 규제·QA·RA 관점
- 기초연구 논문으로 직접적 regulatory precedent는 없음. CRISPRi mouse는 연구 도구이며 therapeutic 후보가 아님.
- `해석:` 활용 시 regulatory 의미는 *간접적* — primed CRE/HSC marker는 향후 cell therapy의 quality attribute나 potency assay 후보로 검토될 *기초 근거* 정도.

### 2.4 권위·신뢰 가중치
- `1차 출처:` peer-reviewed primary research, Stem Cells(OUP), data open(GEO GSE184851/GSE162949), code는 모두 public tool(ENCODE pipeline, chromVAR, HOMER, GREAT, CRISPOR).
- 이해상충: S.C.가 NextRNA Therapeutics 컨설턴트(noncoding RNA 회사) — 본 연구의 ATAC/CRISPRi 결론과 직접 충돌 소지는 낮음.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)
- Forsberg lab(UCSC)의 CRISPRi mouse(dCas9-KRAB@H11, resistance gene 없는 clean line)는 HSPC native chromatin context에서 CRE를 스크리닝하는 도구 자산. 공동연구·material transfer로 접근 가능성 검토 가치.
- HSC-unique/lineage-primed CRE 좌표 + Supplementary peak list(S1-S6)는 erythroid/lymphoid fate marker 후보 라이브러리로 재활용 가능한 resource.

### 3.2 Commercialization-candidate (자체 제품화)
- 직접적 제품화 후보 약함. `해석:` 가능성 있는 간접 경로: (a) HSC potency/identity assay의 epigenomic biomarker 후보(HSC-unique peak), (b) erythroid/lymphoid lineage bias 예측용 CRE 패널 — 둘 다 human 검증·재현이 선행되어야 하는 초기 단계.

### 3.3 우리 파이프라인과의 fit
- **분석 설계 차용**: master peak-list 통합 → primed peak의 trajectory별 유지 정량(`bedtools intersect` 기반)은 우리 Human HSPC multiome에 변형 적용 가능.
- **CRE 좌표 활용**: mouse primed CRE를 hg38 liftover해 우리 ATAC peak과 overlap 검증 시 baseline epigenomic feature 정의에 직접 기여.
- **불일치**: mouse·bulk·외부 expression 조합이라 *그대로* 재현은 부적합. our setting은 human·single-cell·paired RNA.

### 3.4 후속 BD·제품 액션 후보
- Forsberg lab CRISPRi mouse 자산의 라이선싱/공동연구 조건 정찰(우선순위 낮음, 탐색만).
- HSC-unique peak/primed CRE list를 우리 human multiome feature engineering의 prior로 평가(우선순위 중).

## 4. 전문가 코멘트

### 4.1 종합 등급
- Level: **중**
- Perspective(1문장): activation lag 가설의 방향성·persistence 배경 + 분석/검증 방법 참조로 가치가 높은 primary 근거지만, human·paired RNA·lag 정량·임상 자산이 없어 상위 등급은 아님.
- 등급 근거:
  - chromatin priming의 명시적 정의 + trajectory 정량 + CRISPRi functional link 결합 — 배경·방법 인용 가치 높음.
  - data·tool 모두 open → 재현·재활용 용이.
  - mouse·bulk·외부 expression 조합 → 우리 human single-cell 파이프라인에 직접 이식 불가.
  - functional 인과가 3 locus에 한정, lag 정량 자체는 없음.

### 4.2 활용 우선순위
- **다음 분기** — lag 가설 문서/제안서 작성 시 background citation으로 즉시 활용. CRE liftover 검증은 multiome 분석 sprint와 묶어 진행.

### 4.3 발표·미팅에서 들이밀 시점
- 본인 PPT/제안서의 *chromatin priming이 transcription에 선행한다*는 motivation slide. R&D 리뷰에서 우리 multiome feature(primed CRE)의 생물학적 정당화 근거.

### 4.4 추가 탐색 필요 영역
- `질문:` mouse primed/HSC-unique CRE 좌표의 hg38 liftover 성공률과, 우리 human HSPC ATAC peak과의 overlap율은? baseline feature로 쓸 만한 수준인가?
- `질문:` Forsberg lab CRISPRi mouse가 academic MTA로 접근 가능한가, 아니면 상업 라이선스가 필요한가?
