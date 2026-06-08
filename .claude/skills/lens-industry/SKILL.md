---
name: lens-industry
description: Produce the industry lens — industrial/regulatory/clinical risks (QA, RA, FDA/EMA/IRB), BD value and commercialization candidacy (Dx/assay/SW/therapeutic), and an expert comment with single-grade importance. Also fills paper-info.yaml's categorization block (use_case, importance) and audience hints. Academic limitations and next-paper ideas belong to lens-academic, not here.
---

# Lens — Industry

## 목표

이 자료의 *산업 시선* 노트를 만든다. 시니어 바이오인포매티션 + R&D + BD 의사결정자가 다음 미팅에서 *이 paper를 어떻게 쓸 것인가*를 정리한다. 학술적 한계나 후속 논문 아이디어는 `lens-academic`으로 분리하고, 여기서는 **산업·규제·임상 리스크**, **BD value & 자체 제품화 가능성**, **전문가 코멘트(등급)** 만 다룬다.

핵심 산출물 두 가지:
1. `analysis/<primary-topic>/<paper-id>/<paper-id>_lens-industry.md` — 4개 섹션의 해석 노트.
2. `analysis/<primary-topic>/<paper-id>/paper-info.yaml`의 `categorization` 블록 (use_case, importance) 채우기.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- non-paper 자료에 대한 권위·신뢰 가중치(`1차 출처:` / `2차 출처:` / `의견·해설:`) 표기도 적극 활용. 자세한 정의는 `source-grounding` Part 7.4.

## 출력 형식

`<paper-id>_lens-industry.md`는 다음 4개 섹션을 순서대로 갖는다.

```markdown
# Lens — Industry

## 1. Categorization
> 이 섹션은 paper-info.yaml의 categorization 블록과 동기화된다. 본문에는 사람이 읽기 좋게 풀어쓰고, yaml에는 구조화 값으로 기록.

### Domain (자동 추출, 검토 표시)
- ...

### Use case (vocabulary 6개 중 1~3개)
- ...

### Importance (1개 종합 등급)
- Level: 상 / 중 / 하
- Perspective (1문장): ...

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크
- ...

### 2.2 임상·기술적 제약
- ...

### 2.3 규제·QA·RA 관점
- ...

### 2.4 권위·신뢰 가중치
- 1차 출처 / 2차 출처 / peer-review 여부 / 발행처의 이해상충 등

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)
- 라이선싱·공동연구·경쟁사 동향

### 3.2 Commercialization-candidate (자체 제품화)
- Dx / assay / SW / therapeutic 후보화 가능성

### 3.3 우리 파이프라인과의 fit
- ...

### 3.4 후속 BD·제품 액션 후보
- ...

## 4. 전문가 코멘트

### 4.1 종합 등급 (Importance에서 재인용 + 풀어쓰기)
- Level: 상 / 중 / 하
- Perspective (1문장): ...
- 등급을 내린 근거 (3~5 bullet)

### 4.2 활용 우선순위
- 지금 / 다음 분기 / 장기 중 어디에 속하는가

### 4.3 발표·미팅에서 들이밀 시점
- 본인 PPT 발표, BD 미팅, R&D 리뷰 중 어디서 인용·언급할 가치가 큰지

### 4.4 추가 탐색 필요 영역
- 본인이 직접 알아봐야 할 follow-up (`질문:` prefix 활용)
```

---

## Section 1: Categorization 작성 규칙

### 1.1 Domain (자동 추출)

LLM이 paper-info.yaml의 `title`, `abstract_text`, `keywords`, `venue`에서 자동 추출. 사용자 검토.

- Freeform vocabulary로 시작. 예: `single-cell-genomics`, `epigenomics`, `RNA velocity`, `hematopoiesis`, `oncology`, `regulatory-genomics`.
- 누적된 vocabulary는 자주 쓰면 별도 사전으로 승격 (현 시점에는 자유 추가).
- 한 paper에 1~4개 정도.

### 1.2 Use case (vocabulary 6개)

본문 분석 결과(<paper-id>_core.md, <paper-id>_lens-academic.md)와 paper-info.yaml의 메타데이터를 종합해 다음 6개 중 1~3개 선택:

| Tag | 적용 시점 |
|---|---|
| `academic-citation` | 본인 논문·제안서·학회 발표에서 인용 가치 있을 때. `<paper-id>_lens-academic.md`의 Citation 후보 섹션이 풍부하면 자동 부여. |
| `methodology-reference` | core-methods가 자세하고, 방법을 차용·변형해서 쓸 만할 때. |
| `pipeline-applicable` | 우리 dataset (HSPC multiome 등)에 바로 적용 가능. 코드·docker·workflow가 제공되면 가중. |
| `BD-opportunity` | 저자 소속 기관·기업이 외부 자산으로 흥미. 라이선싱·공동연구·경쟁사 관찰 가치. |
| `commercialization-candidate` | 자료의 기술·발견을 자체 제품(Dx, assay, SW, therapeutic)으로 만들 가능성. |
| `regulatory-precedent` | FDA / EMA / IRB 승인 사례, guidance, label, regulatory pathway 참조. |

태그가 *없으면 비워둠*. 억지로 채우지 않는다.

### 1.3 Importance (1개 종합 등급 + 1문장)

- **Level**: `상` / `중` / `하` 중 하나.
- **Perspective**: 1문장. 어떤 관점에서 그 등급인지.
  - 예: `상 — HSPC multiome 파이프라인에 바로 차용 가능 + chromatin-RNA lag 알고리즘이 우리 핵심 문제 직결`
  - 예: `중 — methodology는 흥미롭지만 우리 dataset 규모에선 ROI 낮음. BD-opportunity로만 활용`
  - 예: `하 — 결과가 단일 cohort로 제한, 재현성 불확실. 모니터링만`

### 1.4 paper-info.yaml 갱신

위 1.1~1.3을 paper-info.yaml의 categorization 블록에 동기화:

```yaml
categorization:
  domain:
    - "single-cell-genomics"
    - "epigenomics"
  use_case:
    - "methodology-reference"
    - "pipeline-applicable"
  importance:
    level: "상"
    perspective: "HSPC multiome 파이프라인에 바로 차용 가능 + chromatin-RNA lag 알고리즘이 우리 핵심 문제 직결"
```

`build_index.py`가 이 값들을 papers.csv와 _index/<topic>.md에 자동 반영.

---

## Section 2: 산업·규제·임상 리스크 작성 규칙

### 2.1 데이터·통계적 리스크

다음 항목을 본문에서 추출해 평가:

- **Sample size**: cell, sample, patient 단위. 작으면 *일반화 우려*.
- **Cohort 편향**: 단일 기관·단일 인종·단일 dataset인지. 다양성 부족하면 표시.
- **Replication 부족**: 결과가 *한 dataset에서만* 검증되었는지. 다른 cohort/lab에서 재현 안 됐으면 `해석: replication 부족, regulatory grade evidence로 부족`.
- **Selection bias**: cell filtering, QC threshold가 결과를 유리하게 만들지 않았는지.
- **Multiple testing**: BH/Bonferroni 적용 여부. 누락이면 false positive 우려.

### 2.2 임상·기술적 제약

- **Tissue/sample 가용성**: 실험 protocol이 *희귀 sample*에 의존하면 외부 재현 어려움.
- **장비·시약 가용성**: 특정 platform (예: 10x Chromium, NovaSeq)에 의존하면 small lab 적용 어려움.
- **계산 자원**: GPU 필수면 small lab/clinical setting 적용 어려움.
- **Turnaround time**: 결과 산출에 며칠~몇 주 걸리면 임상 의사결정에 부적합.

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**: 자료의 기술이 어떤 규제 pathway (IVD, LDT, SaMD, drug, biologic)에 해당하는지.
- **Analytical / Clinical validation**: 자료에 *analytical validation* (정밀도, 정확도, LOD)이나 *clinical validation* (sensitivity, specificity, PPV/NPV) 데이터가 있는지.
- **GMP / GLP**: 제조·실험 표준 준수 여부.
- **IRB / consent**: 인간 sample 사용 시 IRB 승인, consent form 명시 여부.
- **Label·indication**: 어떤 환자군·indication을 타깃하는지 명확한가.
- **Reproducibility for audit**: code·data·protocol이 *FDA audit 수준*으로 공개되어 있는가.

### 2.4 권위·신뢰 가중치

- **출처 1차/2차**: `1차 출처:` (FDA letter, Nature paper, 기업 IR) / `2차 출처:` (시장조사 리포트, 뉴스).
- **Peer review 여부**: peer-reviewed면 가중치 ↑, preprint·blog·corporate publication은 가중치 ↓.
- **저자 이해상충 (COI)**: 저자가 *상업적 이익을 가진 기업*과 연결되어 있으면 표시.
- **Funding source**: NIH/공공 vs. corporate sponsored. 후자는 *결과의 자체 검증* 필요성 더 높음.

---

## Section 3: BD value & 상용화 가능성 작성 규칙

### 3.1 BD-opportunity (외부 자산 정찰)

이 자료의 *외부 자산*을 우리가 *가져올 가치*가 있는가?

- **저자/기관의 자산화 가능성**: 저자가 startup 창업했는가? 기관에서 라이선싱 가능한가? Method가 patent된 적 있는가?
- **공동연구 후보**: 저자가 공동연구·visiting 협업에 열려 있는 신호 (consortium 참여, open code, 공개 강연 등).
- **경쟁사 관찰**: 우리 영역 경쟁사가 이 자료를 *이미 활용*하거나 *언급*했는가?
- **시장 영향**: 이 자료가 시장 (특히 BD pipeline 또는 신약개발 의사결정)에 영향을 줄 정도인가?

### 3.2 Commercialization-candidate (자체 제품화)

이 자료의 기술·발견을 *우리가 직접 제품화*할 수 있는가?

- **제품 카테고리 후보**:
  - Diagnostic (Dx): biomarker, signature, classifier
  - Assay: experimental protocol, reagent kit
  - Software (SW): pipeline, SaaS platform, AI model
  - Therapeutic: target, modality, MOA hypothesis
  - Service: CRO·CDMO·consulting offering
- **기술적 성숙도 (TRL)**: Technology Readiness Level. 1~3 (proof-of-concept) / 4~6 (lab validation) / 7~9 (production ready).
- **IP 자유도**: patent 회피 가능한가? 우리가 *open implementation*을 만들 수 있는가?
- **MVP 시나리오**: 가장 빠른 minimum viable product로 어떻게 구성?

### 3.3 우리 파이프라인과의 fit

- 우리 *현재 dataset* (HSPC 10x Multiome 등)과 호환되는가?
- 우리 *팀 역량*으로 재현·확장 가능한가? (R&D headcount, GPU, wet lab capacity)
- 우리 *전략적 방향* (epigenetic therapy 등)과 align되는가?
- 빠진 capability가 있으면 명시 (예: "wet lab 검증 필요, 외부 CRO 필요").

### 3.4 후속 BD·제품 액션 후보

구체적인 next-step 액션 2~5개. 각각 다음 형식:

```markdown
- [액션 이름]
  - 누가: [담당 또는 협업 대상]
  - 언제: [지금 / 다음 분기 / 장기]
  - 자원: [필요한 데이터·인력·예산 수준]
  - 성공 기준: [어떻게 되면 성공인가]
```

예시:
```markdown
- 저자 contact 후 라이선싱 사전 협상
  - 누가: BD lead + 본인 (technical contact)
  - 언제: 다음 분기 안
  - 자원: 미팅 1회, slide deck 1개
  - 성공 기준: term sheet 발행 또는 명시적 거절
```

---

## Section 4: 전문가 코멘트 작성 규칙

### 4.1 종합 등급 (Importance 재인용 + 풀어쓰기)

Section 1.3의 Level과 Perspective를 *3~5 bullet으로 풀어 설명*. paper-info.yaml에는 1문장만 있고, <paper-id>_lens-industry.md에서는 자세한 근거.

```markdown
- Level: 상
- Perspective: HSPC multiome 파이프라인에 바로 차용 가능 + chromatin-RNA lag 알고리즘이 우리 핵심 문제 직결.
- 등급 근거:
  - <paper-id>_core.md §3.2의 dataset (HSPC 10x Multiome, n=24k cells)이 우리 현재 dataset과 동일 platform.
  - core-methods의 chromatin opening rate 모델이 우리 Step 1~2 lag 정량화에 직접 적용 가능.
  - code (welch-lab/MultiVelo)가 GitHub open, MIT license.
  - 단 cell cycle confound 처리는 본 자료가 비워둠 — 우리가 추가 작업 필요.
```

### 4.2 활용 우선순위

- **지금 (이번 sprint / 이번 달)**: 즉시 검토하거나 실험적용 시작할 가치.
- **다음 분기**: 관련 BD 미팅·R&D 리뷰 일정에 맞춰.
- **장기**: 백로그. 큰 새 프로젝트 들어갈 때 다시 본다.

### 4.3 발표·미팅에서 들이밀 시점

본인 어떤 자리에서 이 paper를 *명시적으로 언급*할 가치가 있는가:

- 본인 학회 발표 / 논문 introduction
- BD 미팅 (특정 후보와의 라이선싱·공동연구 협상)
- 사내 R&D 리뷰 (현재 프로젝트 결정)
- 외부 컨퍼런스 / 키노트
- 사내 newsletter / 동향 공유

해당 없으면 비워둔다.

### 4.4 추가 탐색 필요 영역

`질문:` prefix로 시작하는 follow-up. 본인이 다시 펴봤을 때 즉시 액션 가능하게.

```markdown
- 질문: 이 알고리즘을 우리 HSPC dataset에 돌리면 cell cycle confound는 어떻게 처리? 별도 sub-pipeline 필요?
- 질문: 저자가 startup 창업했는지 LinkedIn / Crunchbase 확인 필요.
- 질문: 같은 method를 fetal liver dataset에 적용한 follow-up paper 있는지 확인.
```

---

## 작성 규칙 (전체)

- **본 skill은 lens-academic의 영역을 침범하지 않는다.** 학술적 한계, 다음 논문 아이디어, citation 후보는 `lens-academic`이 담당.
- **억지로 채우지 않는다.** Section 3 (BD value)이 해당 자료에 거의 의미 없으면 짧게 "해당 없음 — 현 시점 BD/제품화 가치 낮음"으로 끝내도 OK. 비어 있는 게 *과장된 평가*보다 낫다.
- **권위 가중치를 끝까지 유지한다.** corporate-publication·blog·news 같은 자료는 *1차 출처가 무엇인지*를 추적하고, 결론에 반영.
- **paper-info.yaml의 categorization 블록과 본문은 동기화되어야 한다.** 본문에서 importance를 상으로 평가하면 yaml에도 상.
- **민감 정보·NDA·내부 자산 정보는 본 skill 출력에 직접 적지 않는다.** 필요하면 `검토필요:`로 추상화하고 사용자에게 전달.

## 주의할 점

- **lens-industry는 *분석 결과*에 대한 *해석*이다.** 사실 추가 발견을 위한 핵심 분석은 core-* 와 source 원문에서.
- **importance.level은 시간에 따라 변한다.** 처음엔 *중*이었다가 우리 파이프라인 변화로 *상*이 될 수 있음. paper-info.yaml의 `workflow.last_updated`로 추적.
- **`audience.primary`가 `bd-meeting`이면 본 skill의 출력을 좀 더 자세히 + executive summary 추가.**
- **Document_type이 non-paper면 Section 2의 "Analytical validation" 같은 paper 특화 항목은 `미제공:`으로 표시.** 억지 분석 금지.
