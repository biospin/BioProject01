# SKILL — 논문 분석 Agent (method paper 읽기, gglee) [BIOP01-1]

method(알고리즘) 논문을 읽을 때 **재현·적용 판단에 필요한 요소**를 강제로 뽑는 스킬. epigenomics 브랜치 AGENTS.md/SKILL.md를 참고해 내 관점으로 재작성.

## 언제
새 velocity/kinetics method 논문 1편을 우리 HSPC(GSE209878) 파이프라인 관점에서 평가할 때.

## 입력 / 출력
- 입력: 논문 PDF(또는 core 노트) 1편 + 우리 데이터/목표 컨텍스트.
- 출력: `analysis_<paper-id>.md` — 아래 6블록.

## 반드시 뽑는 6블록 (요약과 insight를 구분)
1. **주장 & 메커니즘(1문장)** — 무엇을 어떻게 계산하나. 핵심 수식/loss/state 정의. "무엇이 새로운가"를 한 줄로.
2. **New vs Borrowed** — 이 논문 고유 기여 vs 선행(scVelo/UniTVelo/cellDancer 등)에서 상속한 것. (계보 명시 — 과대평가 방지.)
3. **데이터 & 재현성** — dataset 접근(open/restricted, GEO/dbGaP), 코드·license·유지보수, 자원(GPU 필수 여부·시간·메모리), 핵심 의존성.
4. **우리 적용성(HSPC)** — modality 일치(RNA-only vs multiome), 우리 GSE209878 사용 여부, lag 산출이 내장인지 후처리인지, 예상 비용.
5. **한계 & confound** — 저자가 통제 안 한 것(cell-cycle, chromatin ablation 부재, pseudotime≠wall-clock, multi-sample 미지원 등). **반례가 될 조건.**
6. **후속 질문 2–3** — 검증/의사결정을 가르는 질문.

## 규율
- 숫자·주장은 논문 본문/그림 위치를 명시(`§Methods pXX`, `Fig N`). 메모리 재유도 금지.
- "SOTA/우월"은 저자 주장인지 독립 벤치마크(Luo 2026)인지 구분. weak ≠ zero.
- modality mismatch(RNA-only인데 우리는 multiome)는 즉시 flag → baseline 용도로만.
