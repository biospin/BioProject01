# Lens — Industry

> 근거: `luo-2026-velocity-benchmark_core.md` + `sources/luo-2026-velocity-benchmark.pdf`. Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기 동일.

## 1. Categorization

> paper-info.yaml의 categorization 블록과 동기화.

### Domain (자동 추출, 검토 표시)
- RNA velocity
- single-cell-genomics
- benchmark / method-evaluation
- hematopoiesis (저자 소속 Department of Hematology + HSPC·bone marrow·hematopoiesis dataset 다수)

### Use case
- `pipeline-applicable` — 우리 Human HSPC 10x Multiome(GSE209878)이 이 benchmark의 Dataset12로 실제 사용됨. method 선택을 이 논문의 권고에 직접 매핑 가능.
- `methodology-reference` — CBDir/ICCoh/Vcs/A1·A2 metric과 downsampling·HVG·simulation stability 평가 설계를 우리 자체 method 검증 파이프라인에 차용 가능.

### Importance
- Level: 상
- Perspective (1문장): 우리 HSPC 데이터가 benchmark에 직접 포함됐고, "단일 default 금지 + scenario별 method 선택"이라는 운영 지침을 즉시 적용 가능 — 단 MultiVelo가 RNA-only로 평가된 한계는 우리가 보완해야 함.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크
- accuracy 절대값이 낮다: 전체 CBDir 평균 ≈0.1, 최고 0.23(veloVI). `해석:` velocity 방향 추정 자체의 신뢰도가 낮으므로, 이를 임상·의사결정 근거로 쓰기엔 evidence grade가 부족하다 — 탐색적(exploratory) 용도로 제한.
- method 간 불일치(A1 대부분 <0.4): 같은 데이터에서 method를 바꾸면 결론이 달라질 수 있어, 단일 method 결과를 보고서에 단정적으로 싣는 것은 reproducibility 리스크.
- ground-truth 의존: CBDir이 annotation에 묶여 있어 cell type annotation 품질이 결과를 좌우.

### 2.2 임상·기술적 제약
- 계산 자원: 15 method 중 10개가 GPU 경로로 평가됐고 LatentVelo·Pyro-Velocity·cell2fate는 GPU 필수. cell2fate·Pyro-Velocity는 메모리 多, cellDancer·MultiVelo는 실행시간 長. `해석:` 우리 환경(GPU 1대, 128GB RAM)에서 cell2fate/Pyro-Velocity 대형 run은 메모리 병목 가능.
- turnaround: velocity 분석은 연구용 탐색 단계이며 임상 turnaround 요건과는 무관(임상 진단 도구 아님).

### 2.3 규제·QA·RA 관점
- `미제공:` analytical/clinical validation(정밀도·LOD·sensitivity/specificity) 데이터 없음 — 이 논문은 research method benchmark이지 IVD/SaMD 후보가 아니다. FDA/EMA pathway 해당 없음.
- 재현성: 분석 스크립트 GitHub(`luo-cloud/veloBench`) + Zenodo(10.5281/zenodo.18699599) 공개, 모든 dataset accession 명시 → audit 가능 수준의 reproducibility 자료는 갖춤.

### 2.4 권위·신뢰 가중치
- `1차 출처:` peer-reviewed (Cell Reports Methods, open access CC BY-NC-ND).
- COI: 저자 "no competing interests" 선언. funding은 National Key R&D Program of China + NSFC(공공) → corporate sponsorship 편향 낮음.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)
- 직접적 라이선싱 자산은 아님(method가 아니라 비교 연구). `해석:` BD 가치는 "외부 자산"보다 "내부 의사결정 근거"에 있다 — 어떤 velocity method를 우리 product/pipeline에 넣을지의 third-party 근거.
- 경쟁사 관찰: velocity method를 쓰는 single-cell 분석 서비스/SW 제공자가 method 선택의 근거로 이 benchmark를 인용할 가능성 — 동향 모니터링용.

### 3.2 Commercialization-candidate (자체 제품화)
- SW: 이 논문의 평가 파이프라인(다중 method를 같은 데이터에 돌려 CBDir/ICCoh/Vcs/A1·A2 + cross-method consistency를 산출)을 우리 내부 "velocity QC/consistency 리포트" 모듈로 재구현 가능. TRL 4~6(코드·metric 정의 공개로 재현 용이).
- IP 자유도: metric은 선행 문헌(refs 5,17,25) 기반이라 특정 patent에 묶이지 않음. open implementation 가능.

### 3.3 우리 파이프라인과의 fit
- Dataset 호환: **직접 호환** — GSE209878(HSPC)이 Dataset12로 포함, GSE81682(mouse hematopoiesis)가 Dataset17, embryonic mouse brain 10x multiome가 Dataset16. 우리 팀 데이터셋과 다수 겹침.
- 팀 역량: GPU 1대 + 128GB RAM으로 veloVI·DeepVelo·scVelo-sto 등 권장 method는 재현 가능(usability 상위). cell2fate/Pyro-Velocity는 메모리 주의.
- 전략 fit: epigenomic-lag 목표와 align되나, *chromatin 채널을 켠 multi-omic velocity*는 이 논문이 비워둠 → 우리가 채워야 할 영역.

### 3.4 후속 BD·제품 액션 후보
- velocity consistency QC 모듈 사내 PoC
  - 누가: 본인(김가경) + 류재면
  - 언제: 다음 분기
  - 자원: GPU 1대, 기존 HSPC anndata, veloBench 스크립트 참조
  - 성공 기준: HSPC에 3개 이상 method(veloVI/DeepVelo/scVelo-sto) 돌려 CBDir + cross-method A1 리포트 자동 생성
- multi-omic(ATAC-on) velocity 빈칸 검증
  - 누가: 본인
  - 언제: 장기
  - 자원: 10x Multiome ATAC peak matrix, MultiVelo full mode
  - 성공 기준: RNA-only vs ATAC-on MultiVelo의 HSPC CBDir 차이 정량화

## 4. 전문가 코멘트

### 4.1 종합 등급
- Level: 상
- Perspective: 우리 HSPC 데이터가 benchmark에 직접 포함됐고 운영 지침(scenario별 method 선택 + multi-method consistency)을 즉시 적용 가능.
- 등급 근거:
  - Dataset12 = GSE209878 = 우리 김가경 담당 HSPC 데이터의 정확한 accession.
  - Figure 6D decision tree가 우리 method 선택의 즉시 적용 가능한 근거.
  - 코드·dataset이 모두 공개(GitHub + Zenodo)로 재현 진입장벽 낮음.
  - 단 MultiVelo가 `rna_only=True`로 평가돼 우리 multi-omic 목표의 핵심 질문에는 직접 답하지 못함 — 우리가 추가 검증 필요.

### 4.2 활용 우선순위
- 지금: HSPC method 선택 근거로 본 benchmark의 시나리오 권고 채택(우리는 hematopoietic branching = complex topology + 부분적 sparsity → veloVI/DeepVelo/LatentVelo/UniTVelo 후보군).
- 다음 분기: velocity consistency QC 모듈 PoC.

### 4.3 발표·미팅에서 들이밀 시점
- 사내 R&D 리뷰: "왜 우리가 단일 velocity method에 고정하지 않는가"의 근거.
- 본인 논문 introduction/methods: method 선택 정당화 인용.

### 4.4 추가 탐색 필요 영역
- 질문: Dataset12(HSPC)에서 method별 개별 CBDir 순위는? mmc1.pdf Figure S1/Table S1에서 추출 필요.
- 질문: 우리 HSPC에 ATAC 채널을 켠 MultiVelo의 정확도가 RNA-only 대비 유의하게 오르는가? 이 논문은 답하지 않음 — 자체 실험 필요.
- 질문: veloVI를 우리 HSPC에 돌릴 때 GPU 메모리/실행시간이 우리 1-GPU 환경에서 수용 가능한가? Figure 6C 수치 정밀 판독 후 추정.
