# Lens — Industry — Spark-to-Paper

> 근거: `sources/fulltext_extract.md`(arXiv:2608.11924, HTML fulltext 자동추출 2026-08-18). §번호는 자동추출본이라 `검토필요:`로 둔다.
> 관점 주의: 이 논문은 우리 **velocity 과학 논문(HSPC chromatin-RNA lag)과는 무관**하다. 여기서 말하는 "우리 파이프라인"은 HSPC 분석 파이프라인이 아니라 **논문 생산·검증 하네스**(paper-production-orchestrator, verify-harness)를 가리킨다.

## 1. Categorization
> paper-info.yaml의 categorization 블록과 동기화(yaml은 kkkim이 별도 작성 — 본문 값과 맞출 것).

### Domain (자동 추출, 검토 표시)
- research automation (자율 연구 에이전트)
- LLM agent / coding-assistant skills
- scientific writing / paper generation

### Use case (vocabulary)
- `methodology-reference` — 8-stage 파이프라인, stage별 결정론적 gate, Claim Admission Protocol(5라벨), Self-Refutation loop bounding(7회 상한), lightweight preregistration 같은 설계를 우리 논문 생산·검증 하네스의 *검증 layer* 참고로 직접 차용 가능.
- `competitive-landscape` (vocabulary 확장 항목) — 우리가 만드는 paper-production-harness·verify-harness와 **직접 경쟁·수렴하는 외부 선례**. 채택할 지표보다 설계 대조·차별화의 근거로 다룬다.

### Importance (1개 종합 등급)
- Level: 상
- Perspective (1문장): 우리 논문 생산·검증 하네스와 직접 수렴하는 최초의 통합 선례이며, AI Scientist류를 검증 게이트로 감싸야 한다는 우리 논지(BIOP01-81 검증게이트·BIOP01-84 검증하네스)의 직접 근거가 된다. 단 velocity 과학 논문 자체와는 무관하니 인용 맥락을 분리한다.

## 2. 산업·규제·임상 리스크 (QA / RA)
> 이 논문은 임상·진단 도구가 아니라 논문 생성 시스템이므로, 여기서 "리스크"는 **이 방법을 실제 논문 생산에 도입했을 때의 리스크**로 읽는다. FDA/IVD/IRB 같은 임상 pathway 항목은 `미제공:`으로 둔다.

### 2.1 데이터·통계적 리스크 (평가 설계의 한계)
- **claim-level 판정이 model-based(환각 잔존)**: 저자 스스로 명시한 1순위 caveat — "특정 증거가 어떤 claim을 의미적으로 뒷받침하는지는 현재 model이 판정"(검토필요: 저자 한계 §). 결정론적 gate가 malformed citation·미해결 placeholder는 잡아도, 증거-주장 정합의 *의미 판정*은 여전히 LLM이 한다 → 환각·과대해석 잔존. 우리 하네스에 옮길 때 이 판정은 사람 감사 대상으로 남겨야 한다.
- **preregistration이 non-binding**: planning stage가 dataset·baseline·metric·table 구조를 실행 전 고정하지만(수치 cell만 비워둠), 저자도 "lightweight·비강제"라 인정. 사후 protocol 적응 위험을 *줄이는* 장치이지 *봉인*이 아니다. → 우리의 사전등록 봉인 규율(PREREGISTRATION 파일:줄 인용) 대비 약하다.
- **fabrication detection의 커버리지 제한**: 14→92% 상승은 36 seeded probe / 10 failure family에서만 측정했다. 실제 실패 유형 분포를 대표한다는 보증이 없고(precision 74% [61–83%]), 이 92%를 "환각을 92% 잡는다"로 일반화하면 과대 인용이 된다.
- **평가 범위가 8 topic**: primary가 외부 선정 8 research topic(사전등록), single-pass paired 비교는 3 topic, human preprint audit 8편. n>3 paper 단위 CI라 통계는 정직하나, 표본이 작아 도메인 일반화는 미검증. cross-template robustness는 언급만 되고 main table에 수치 없음(검토필요: §).
- **이전 시스템 비교 비정규화**: AI Scientist / AI Scientist-v2 / Agent Laboratory를 재실행 없이 공개 artifact 값만으로 비교. model backbone·pricing을 정규화하지 않았다(저자 인정). 따라서 "우리가 citation validity·figure editability에서 이긴다"는 비교는 *같은 조건의 head-to-head가 아니다*. Spark-to-Paper 우위 수치는 방향성 근거로만.

### 2.2 기술적 제약 (도입 관점)
- **Claude Code + Claude model family 하드 종속**: 별도 orchestration 없이 coding assistant "안"에서 도는 것이 핵심 셀링포인트이자 제약. 타 백엔드 구현이 없어 이식성은 저자도 caveat로 명시.
- **figure 재구성 신뢰성**: method figure는 raster→HTML 재구성→vector PDF. 편집가능 96.4%는 *의도적으로 raster를 제외한* 뒤의 수치이고, 복원 불가 시 raster fallback. human preprint 58%보다 높은 건 생성 explanatory figure가 애초에 재구성하기 쉬운 성격이라는 점을 감안(저자 caveat).
- **turnaround·자원**: 논문 1편당 3.2h wall-clock, 11.9M token, $8.1. 실험 단계는 자원 gap을 자동 해결하지 못하고 missing dependency로 기록 후 결과 미기재.

### 2.3 규제·QA·RA 관점
- **FDA/IVD/IRB pathway**: `미제공:` — 임상 검증 자료가 아니라 논문 생성 시스템. analytical/clinical validation(정밀도·sensitivity 등)은 해당 없음.
- **audit 관점의 진짜 가치**: 오히려 이 논문의 gate 스택(Template/Blueprint/Citation/Manuscript/Figure/Compilation) + Claim Admission Protocol + 사전등록+외부 timestamp + "모든 결과를 유불리와 무관하게 보고"라는 투명성 조치가, 우리 verify-harness의 audit-ready 검증 layer 설계 참고가 된다. 특히 Self-Refutation 7회 상한 후 "failure report"를 남기고 억지 성공을 안 하는 규율은 우리 claim-defensibility 게이트와 같은 정신.
- **human oversight 필요**: 저자 결론이 claim-level 판정을 auditing 필요한 약점으로 인정 → 우리가 이 방식을 쓴다면 SOP에 사람 검증 게이트를 명문화할 근거(우리 CLAUDE.md 검증 게이트와 정합).

### 2.4 권위·신뢰 가중치
- `1차 출처:` VastiLab(corresponding wangwenhao@vastilab.com) 원저자의 1차 시스템 보고.
- **Peer review 여부**: **arXiv preprint, 미peer-review**. 가중치 하향. 1차 출처지만 figure count 등 일부는 self-reported("존재 증거이지 benchmark 아님"이라 저자도 명시). fabrication·citation·editability 수치는 CI 포함 자체측정이라 상대적으로 신뢰도가 높으나, 외부 재현은 아직 없다.
- **저자 이해상충(COI)**: `해석:` corresponding author 소속(VastiLab)이 자율 연구·논문생성 시스템을 자산으로 포지셔닝할 수 있는 조직으로 추정(전체 저자 소속은 추출본에 없음). framing(coding assistant만으로 end-to-end 논문생성 가능) 자체가 사업 방향과 align할 소지. 평가는 공개 이전 시스템 대상이나 비정규화 비교라 자사 우위가 과대평가될 여지를 감안.
- **소스 미공개**: GitHub(`Spark-To-Paper-Skills/spark-to-paper-skills`) 예고만 있고 릴리스 명시 없음(검토필요: 현재 repo 상태). 재현·차용 판단은 소스 공개 확인 후.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)
- **경쟁·수렴 관찰 대상**: 우리 paper-production-orchestrator(BioProject01/02)와 verify-harness가 하려는 것을 거의 같은 구조(stage gate + model review + 사전등록 + claim 판정)로 먼저 구현. 라이선싱보다 **설계 벤치마크**로서의 가치가 크다. 소스가 공개되면 gate/review 구현 세부를 대조해 우리 하네스의 빈틈을 점검할 수 있다.
- **차용 자유도**: 개념(gate 스택·Claim Admission·loop bounding)은 공개 논문에 서술 → 개념 차용은 자유. 소스 license는 아직 확인되지 않아 별도 질문으로 남긴다.

### 3.2 Commercialization-candidate (자체 제품화)
- 직접 팔 Dx/assay/therapeutic 후보 아님. 우리에게는 **내부 SW 자산(논문 생산·검증 하네스)의 기능 후보**로서의 가치.
- 도입 후보 기능(우리 하네스에 이식 검토):
  - Claim Admission Protocol 5라벨(supported/partially/unsupported/contradicted/needs-confirmation) → 우리 claim 등급표를 실험 후 자동 재판정하는 규격으로.
  - Self-Refutation loop bounding(7회 상한 + failure report) → 우리 loop가 같은 방향으로 무한 수정하는 실패모드를 막는 가드.
  - lightweight preregistration(table 구조 선고정, 수치 cell 후채움) → 우리 봉인 사전등록과 병행할 실행 규격.
  - stage별 결정론적 gate → 우리 검증 게이트(p3 재계산 대조)의 상류 게이트 확장 참고.
- 도입 비용: 논문 1편당 **$8.1 [6.9–9.6] · 11.9M token [10.2–13.7M] · 3.2h [2.6–3.9h]**, **Claude Code + Claude model family 종속**. gate가 증분 token의 대부분(3-topic subset 측정 +8.1M±0.9M, +$5.3±0.5)이라 검증 강화는 비용과 정비례.

### 3.3 우리 파이프라인과의 fit (= 논문 생산·검증 하네스)
- **직접 fit(하네스)**: 높음. 우리 paper-production-orchestrator·verify-harness와 목적·구조가 수렴 → 설계 대조로 즉시 유용.
- **velocity 과학 파이프라인과의 fit**: 낮음(무관). HSPC chromatin-RNA lag 분석과는 연결점 없음 — 인용 맥락을 반드시 분리한다.
- **팀 역량**: gate/claim-protocol 개념을 우리 하네스에 이식할 역량 충분(코드·하네스 중심 workstream, 지용기 Critic 총괄).
- **빠진 capability**: 우리 하네스는 이미 결정론적 재계산 대조(p3)·claim-defensibility 게이트·봉인 사전등록을 갖췄다. 이 논문이 더 가진 것은 *stage 전 구간을 하나의 skill 묶음으로 통합*한 점과 *fabrication probe로 gate 유효성을 정량 측정*한 점 → 후자는 우리 verify-harness의 mutation 검사와 사상이 같아 대조 가치가 크다.

### 3.4 후속 BD·제품 액션 후보
- 소스 릴리스·license 확인
  - 누가: 본인(하네스 담당)
  - 언제: 지금 (repo 공개 여부만 점검)
  - 자원: web 확인 1회
  - 성공 기준: `Spark-To-Paper-Skills/spark-to-paper-skills` 공개/license 확정 → 공개 시 gate·review 구현 세부 대조 착수 판단.
- Claim Admission Protocol 이식 PoC
  - 누가: 본인 + Critic 총괄(지용기)
  - 언제: 다음 분기
  - 자원: 우리 draft 1편에 5라벨 재판정 규격 적용
  - 성공 기준: 실험 후 claim 등급표가 supported/…/needs-confirmation로 재현적으로 재판정되고 abstract·intro·results 전 occurrence로 전파되는 PoC 동작.
- verify-harness mutation vs. fabrication-probe 대조 메모
  - 누가: 본인
  - 언제: 다음 분기
  - 자원: 두 접근(우리 mutation 감시 / 이 논문 seeded probe) 비교 1페이지
  - 성공 기준: 우리 게이트가 놓치는 failure family가 이 논문 10 family 대비 무엇인지 gap 목록화.

## 4. 전문가 코멘트

### 4.1 종합 등급
- Level: 상
- Perspective: 우리 논문 생산·검증 하네스와 직접 수렴하는 최초의 통합 선례. AI Scientist류를 검증 게이트로 감싸야 한다는 우리 논지(BIOP01-81·BIOP01-84)의 1차 근거.

시니어 관점: 이 논문은 "coding assistant 안의 재사용 skill 묶음만으로 end-to-end 논문을 뽑는다"는, 우리가 사내에서 조용히 하던 것과 같은 도박을 공개 수치와 함께 내놓았다. gate만으로 fabrication 탐지가 14→69%로 오르고 self-review·adversarial을 얹어 92%까지 가되 precision은 74%에 그치는 것, preregistration이 비강제라고 스스로 못박은 것, 이전 시스템 비교가 backbone·pricing 비정규화라 head-to-head가 아니라고 인정한 것까지, 저자가 직접 밝힌 이런 한계가 오히려 이 논문을 우리 설계 대조 자료로 쓸 만하게 만든다. 결정론적 gate가 citation·placeholder·compile 같은 형식은 잡지만 증거-주장 정합의 의미 판정은 끝내 LLM 몫으로 남고, 그 한계선이 바로 우리가 사람 감사 게이트를 어디에 둘지의 지도가 된다. 다만 preprint·미peer-review·소스 미공개·8 topic이라는 근거의 얇음과 velocity 과학 논문과 무관하다는 점은 인용 때마다 분리해 둔다.

- 등급 근거:
  - Claim Admission Protocol·Self-Refutation bounding·lightweight preregistration이 우리 하네스에 바로 이식 검토할 구체 규격.
  - fabrication seeded probe로 gate 유효성을 정량화한 접근이 우리 verify-harness mutation 검사와 사상이 같아 대조 가치.
  - 단 claim-level 판정이 model-based(환각 잔존)이고 비교가 비정규화이며 소스가 미공개라, 수치는 방향성 근거로만 쓰고 임계·성능 주장으로 인용하지 않는다.

### 4.2 활용 우선순위
- 지금: 소스 릴리스·license 확인(3.4). 우리 하네스 설계 대조 메모 착수.
- 다음 분기: Claim Admission Protocol 이식 PoC, verify-harness vs. fabrication-probe gap 메모.
- 장기: 우리 논문 생산·검증 하네스 문서(BIOP01-81/84)의 외부 선례 reference로 상시 인용.

### 4.3 발표·미팅에서 들이밀 시점
- 사내 R&D/하네스 리뷰: "AI Scientist류를 검증 게이트로 감싸는 것이 맞는가"를 논의할 때 1차 외부 근거(BIOP01-81/84).
- 우리 하네스 설계 문서: gate 스택·claim 판정·loop bounding의 선례 인용.
- velocity 과학 논문 introduction에는 인용하지 않는다(무관).

### 4.4 추가 탐색 필요 영역
- 질문: `Spark-To-Paper-Skills/spark-to-paper-skills` repo가 실제 공개되었는가? license는? 공개면 gate·adversarial review 구현 세부를 우리 것과 대조.
- 질문: 이들의 10 failure family가 우리 verify-harness mutation set과 얼마나 겹치는가? 우리가 놓치는 family가 있는가?
- 질문: cross-template robustness(main table에 수치 없음)는 어디까지 검증됐는가 — venue별 JSON spec이 실제로 hard-code 없이 도는지 소스로 확인.
- 질문: preregistration 외부 timestamp를 어떤 장치로 걸었는가(우리 봉인 규율에 이식 가능한 형태인지).
