# Lens — Industry: workman-2026-scbench

**소스**: `workman-2026-scbench_core.md` + `sources/workman-2026-scbench.pdf`

---

## 1. Categorization

> 이 섹션은 paper-info.yaml의 categorization 블록과 동기화된다.

### Domain

- single-cell genomics
- AI/LLM agents
- bioinformatics benchmarking

### Use case

- `academic-citation` — LLM agent를 scRNA-seq 분석에 적용할 때 현재 SOTA 성능 한계를 인용하는 표준 reference로 사용 가능
- `internal-tool-evaluation` — 우리 분석 파이프라인에서 AI agent/LLM 선택 기준을 수립할 때 직접 참조 가능 (어떤 task·platform에서 실패하는지 정량화)
- `technology-watch` — LLM-driven bioinformatics 분야 트렌드 모니터링: 현재 52.8% SOTA는 사실상 "아직 완전 자동화 불가" 신호

### Importance

- **Level**: 상
- **Perspective**: frontier LLM agent가 scRNA-seq 분석에서 어떤 task·platform에서 실패하는지 처음으로 정량화한 benchmark로, 우리 파이프라인에 AI agent를 도입하거나 평가할 때 직접 참조 가능한 유일한 정량적 yardstick.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Benchmark 비공개 비율**: 394개 evaluation 중 30개(7.6%)만 공개. 나머지 364개는 training contamination 방지 명목으로 비공개. 우리가 자체 모델을 동일 benchmark로 평가하는 것은 불가하며, 공개 30개 subset 결과가 full benchmark 결과와 얼마나 일치하는지 검증 불가.
  - 해석: benchmark 완전 재현·감사가 불가하여 결과를 그대로 수용해야 하는 구조. 신뢰도에 limitation 존재.

- **Tissue-platform confounding**: MissionBio(hematopoietic·CCUS)와 Illumina(DRG)처럼 tissue와 platform이 완전히 confounded. platform 효과와 tissue 특수성을 분리 불가. 특히 MissionBio의 낮은 성능(26.4%)이 platform 비표준성 때문인지 임상 샘플 희귀성 때문인지 판단 불가.

- **Replicate 수**: K=3은 최소 통계 충분성. per-evaluation mean이 {0, 1/3, 2/3, 1} 4개 값만 취해 micro-level 추정 정밀도 낮음. Task category 하위 분석(특히 Trajectory, n=7)은 CI가 너무 넓어 결론 도출 어려움.

- **Evaluation type 비율 미공개**: Scientific / Procedural / Observational 분포가 공개되지 않아 aggregate accuracy의 해석 편향 가능성 배제 불가.

### 2.2 임상·기술적 제약

- **본 자료의 성격**: scBench는 임상 진단/치료제 개발 도구가 아닌 AI agent 평가 benchmark. 직접적인 임상 적용 대상이 아님.
- **계산 자원**: mini-SWE-agent harness 실행 시 LLM API 비용 발생. 394 evaluations × K=3 replicates × 8 모델 = 9,456 실행. frontier model 비용은 상당함. 우리가 자체 평가 시 subset만 가능.
- **LatchBio 종속성**: 현재 benchmark 운영이 LatchBio에 종속. 서비스 중단·정책 변경 시 외부 연구자의 접근이 제한될 수 있음.

### 2.3 규제·QA·RA 관점

- **규제 pathway 해당 없음**: scBench는 AI 평가 benchmark이며, FDA IVD/SaMD/LDT 등 직접적 규제 pathway 해당 없음.
  - 해석: 단, 우리가 AI agent를 임상 진단 보조 목적으로 사용할 경우, scBench 성능 데이터(52.8% 최고 정확도)는 "AI가 아직 임상 의사결정에 단독 사용 불가"임을 지지하는 근거로 활용 가능.
- **IRB 해당 없음**: 공개 sequencing dataset 사용. 신규 인간 샘플 수집 없음.
- **Reproducibility for audit**: 코드(latchbio/scbench)와 30개 canonical evaluation은 GitHub에 공개(Creative Commons Attribution 4.0). 나머지 364개 evaluation은 재현·감사 불가.

### 2.4 권위·신뢰 가중치

- **출처**: arXiv preprint (2026-02-09). 동료 심사 미완료.
  - 1차 출처: arXiv 2602.09063v1 (저자 직접 제출)
  - 2차 출처: 없음 (인용·뉴스 보도 여부 미확인)
- **Peer review 여부**: 미완료. preprint 결과를 정책 결정에 인용 시 caveat 명시 필요.
- **저자 이해상충 (COI)**:
  - 전원 LatchBio 소속. LatchBio는 bioinformatics SaaS platform 기업.
  - scBench는 사실상 LatchBio의 AI agent 인프라(Latch Copilot 등)를 홍보하는 benchmark 역할을 할 수 있음.
  - 해석: Claude Opus가 최고 성능을 기록한 결과의 방향성은 LatchBio의 파트너십·제품 방향과 align될 수 있음. 모델 순위는 참고용으로만 사용하고, 자체 검증 권장.
- **Funding source**: 미제공. LatchBio 내부 자원으로 추정. 공공 NIH 지원 없음.
  - 해석: corporate-sponsored benchmark. 결과의 자체 검증 필요성이 높음.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **LatchBio**: 민간 bioinformatics SaaS 기업. scBench는 LatchBio Copilot(AI agent 제품)의 마케팅 자산 역할. 라이선싱 대상 기술이라기보다 경쟁사·파트너 관찰 목적에 가까움.
- **경쟁사 관찰**: Genentech, Broad Institute, 기타 genomics 소프트웨어 회사들이 유사 AI agent를 개발 중이며, scBench 결과를 자사 agent 검증 근거로 활용 시도 가능. 우리도 동일 관점에서 참고.
- **공동연구 후보**: 해당 없음. LatchBio는 독립 상업 기업이며 공동연구 신호 없음.
- **시장 영향**: AI-driven scRNA-seq 분석 소프트웨어 시장(Seurat/Scanpy 기반 SaaS, LLM agent 통합 플랫폼)에서 "현재 SOTA 정확도 ~50%"라는 수치가 시장 성숙도·투자 판단에 영향을 줄 수 있음.

### 3.2 Commercialization-candidate (자체 제품화)

- **직접 제품화 가능성**: 낮음. scBench 자체는 benchmark framework. 우리가 제품화할 기술 자산이 아님.
- **간접 활용**:
  - SW 카테고리: 우리가 자체 scRNA-seq AI agent를 개발·평가할 때 scBench의 공개 30개 evaluation을 내부 QA 테스트셋으로 활용 가능.
  - Service 카테고리: AI agent bioinformatics 서비스를 외부에 제공할 경우, scBench 공개 subset 기준 성능 인증은 차별화 포인트가 될 수 있음.
- **TRL**: 해당 없음 (benchmark → 자체 제품화 경로 없음).
- **IP 자유도**: Creative Commons Attribution 4.0. 자유롭게 활용 가능.

### 3.3 우리 파이프라인과의 fit

- **현재 dataset 호환**: HSPC 10x Multiome은 scBench 평가 플랫폼(Chromium이 가장 근접)과 부분 일치. 단, MissionBio(Tapestri)처럼 DNA+protein multiome은 아직 scBench 지원 부족.
- **자원 가능성**: 공개 30개 canonical evaluation은 현재 팀 자원으로 실행 가능. 전체 394개는 접근 불가(비공개).
- **팀 역량**: scBench 공개 subset을 활용해 우리 AI agent(또는 Claude API 기반 파이프라인)를 내부 평가할 수 있음.
- **전략적 fit**: AI-augmented scRNA-seq 파이프라인을 구축할 경우 → "어떤 task에서 LLM이 실패하는지 이미 알고 있다"는 것이 설계 우선순위를 결정하는 데 직접 사용 가능.
  - **Cell typing & DE가 가장 어렵다(34.9%, 27.0%)**: 이 두 단계에 인간 전문가 검토 레이어를 유지해야 함.
  - **Normalization은 비교적 쉽다(70.4%)**: 자동화 먼저 적용 가능한 단계.

### 3.4 후속 BD·제품 액션 후보

- **[scBench 공개 subset 내부 평가 실행]**
  - 누가: 바이오인포매틱스 팀
  - 언제: 지금 (이번 스프린트 또는 다음 달)
  - 자원: GitHub(latchbio/scbench), Claude API, 로컬 컴퓨팅 환경
  - 성공 기준: 30개 canonical eval에서 우리 Claude 기반 agent의 accuracy 측정 완료, 내부 보고서 1개

- **[AI agent 적용 우선순위 결정]**
  - 누가: R&D 리드
  - 언제: 다음 분기 내 AI agent 도입 논의 시
  - 자원: 이 분석 문서 1개 + scBench 결과 참고
  - 성공 기준: "normalization·QC는 AI agent 자동화, cell typing·DE는 human-in-the-loop 유지" 팀 내 결정

- **[LatchBio 동향 모니터링]**
  - 누가: 기술 트렌드 담당자
  - 언제: 장기 (분기별 1회 체크)
  - 자원: arXiv alert, GitHub watch
  - 성공 기준: scBench full suite 공개 또는 Latch Copilot 기술 업데이트 캐치

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective**: AI agent를 scRNA-seq 파이프라인에 도입·평가하려는 모든 팀이 한 번은 읽어야 하는 정량적 baseline. 현재 SOTA가 52.8%라는 수치 자체가 "AI 완전 자동화는 아직 무리"임을 명확히 함.
- **등급 근거**:
  - scRNA-seq AI agent 성능을 처음으로 정량화한 benchmark. 경쟁 도구 없음.
  - 플랫폼 효과(32.7 pp)가 모델 효과(23.6 pp)보다 크다는 발견 → platform-aware agent 설계 필요성의 직접 근거.
  - Cell typing(34.9%)·DE(27.0%)의 낮은 성능 → 자동화 전략에서 어디에 인간 전문가를 유지해야 하는지 명확한 map 제공.
  - GitHub 공개(30 eval), CC BY 4.0 → 즉시 내부 활용 가능.
  - 단점: preprint·LatchBio COI·benchmark 비공개(93%) 구조. 인용 시 caveat 명시 필요.

### 4.2 활용 우선순위

- **지금**: 공개 30개 canonical evaluation 내려받아 내부 AI agent 평가에 활용. AI agent 도입 의사결정 자료로 이 분석 문서 공유.
- **다음 분기**: AI-augmented 파이프라인 설계 시 "cell typing·DE는 semi-automated" 아키텍처 결정에 직접 반영.
- **장기**: scBench full suite 공개 시 재평가. LatchBio 신규 benchmark (spatial·multi-omic 통합) 모니터링.

### 4.3 발표·미팅에서 들이밀 시점

- **사내 R&D 리뷰**: AI agent 도입 필요성 및 한계를 논의할 때 — "현재 최고 모델도 50% 정확도"를 수치로 제시
- **BD 미팅**: AI-driven genomics 서비스 제안 시 — "cell typing·DE에서 AI agent는 아직 신뢰 부족, 인간 전문가 필요"라는 포지셔닝 근거
- **사내 뉴스레터 / 동향 공유**: LLM-bioinformatics 트렌드 업데이트 시 이 benchmark 결과를 스냅샷으로 소개

### 4.4 추가 탐색 필요 영역

- 질문: LatchBio의 Latch Copilot이 실제 상업 제품으로 scBench에서 어떤 성능을 내는지 확인 필요. 자사 benchmark에서 자사 제품을 평가하지 않은 것은 의도적 회피인지 설계상 limitation인지?
- 질문: 30개 canonical evaluation을 우리 Claude API 기반 파이프라인으로 돌렸을 때 scBench 논문 결과와 얼마나 일치하는지 — 재현 가능성 자체 검증 필요.
- 질문: scBench가 peer review 통과 후 (Nature Methods / Bioinformatics 등) 게재되면 citation weight가 올라감. 현재 preprint 상태의 인용은 caveat 동반 필요.
