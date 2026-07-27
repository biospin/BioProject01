# validation — week2 Insight 검증 [BIOP01-8]

week2 `insight.md`의 I1–I4를 6기준(Evidence/Logic/Scope/Novelty/Actionability/Risk)으로 검증. Status ∈ {Valid, Needs Evidence, Overstated, Unclear, Rejected}.

---

## I1 — 계열은 정확도가 아니라 자유도 이동으로 진화, 최신 둘은 상보적
- **Status: Valid**
- Evidence: 계보는 3개 브리프에서 직접 확인(moflow='두 갈래 중 하나', multivelovae='일반화', celldancer='predecessor'). [E1]
- Logic: cell-specific·latent-time·chromatin·multi-sample을 축으로 두면 각 method의 완화 축이 다름 → 상보 주장 성립.
- Scope: '상보적'은 *설계 축* 기준. 실측 성능 우열 주장 아님(그건 I2/벤치마크). 과확장 아님.
- Novelty: 개별 논문 요약을 넘은 계보-축 재구성 = 새 관찰.
- Risk: MoFlow와 MultiVeloVAE를 실제 우리 데이터에서 함께 돌려 정말 상보적(다른 gene에서 강함)인지는 미검증 → I4-②와 연결.

## I2 — chromatin-aware 4종은 강점이 겹치지 않음 → 2–3종 교차+합의가 정당
- **Status: Valid** (운영 권고로서)
- Evidence: 차별점은 브리프에서 각각 확인[E4]; 'no single answer'는 veloBench 결론[luo brief].
- Logic: 강점 분산 + 공통 약점(인과·척도) → 교차 실행 합의가 단일 default보다 robust. 타당.
- Scope: veloBench의 권장은 RNA-only method(DeepVelo/veloVI/LatentVelo) 중심 → chromatin-aware 4종에 그대로 확장하는 건 **부분적 비약**. 'no single answer' 원칙은 이식되나 구체 후보 목록은 아님.
- Actionability: 높음 — 우리 파이프라인이 실제로 MultiVelo/MoFlow/MultiVeloVAE 3종 교차로 감(프로젝트 방향과 일치).
- Risk: 교차 후 '합의'를 어떻게 정의(방향 부호? 크기?)하는지 미정 → 척도 필요.

## I3 — 세 한계(chromatin 인과·cell-cycle·척도)가 반복
- **Status: Valid**
- Evidence: (a) CRAK-Velo k=0 ablation 부재 + veloBench ATAC-off = 2개 독립 근거[E2]. (b) cell-cycle 미명시는 3개 브리프 '재회고'[E3]. (c) pseudotime≠wall-clock은 multivelo brief 명시.
- Logic·Scope: 세 항목 모두 다수 논문에서 관찰 → '반복' 성립. 단 (b)는 "논문에 명시 안 됨"이지 "처리 안 함"이 아닐 수 있음 → 문구를 '미보고'로 한정해야 정확.
- Novelty: 개별 한계를 교차로 묶어 '분야 공통 맹점'으로 승격 = insight.
- Risk: (a)가 가장 강함(우리 자체 결과로 검증됨 — scrambled-chromatin 대조에서 lag가 chromatin 없이도 생존). → I4-①/②의 근거.

## I4 — 미해결 공백(ATAC-on 이득, cross-method 재현, wall-clock, cell-cycle)
- **Status: Valid (핵심), 단 ①②는 우리 내부 결과로 이미 부분 답이 나옴 → '공백'→'우리 기여'로 재프레이밍 권장**
- Evidence: 공백 자체는 문헌 근거 확실(veloBench 공백, cross-method consistency 미보고)[E2,E4].
- Logic: "분야가 안 한 것 = 우리가 할 것" 연결 타당.
- Scope: ①(ATAC-on 이득)·②(cross-method 재현)는 **우리 파이프라인이 이미 착수**(scrambled-null 대조, 3-method concordance) → 순수 '미해결'로 두면 우리 진척을 누락. 문헌 공백 + 우리 예비결과를 함께 기재해야 정직.
- Actionability: 매우 높음 — 프로젝트 핵심 가설(lag cross-method 재현성)과 직결.
- Risk: 우리 내부 결과(예: lag |ρ|≤0.08)는 아직 논문화 전 → insight 문서에 인용 시 '내부·잠정' 표기 필수.

---

## 토론 준비(5문항) 답
1. **가장 설득력**: I3(반복 한계) — 독립 근거 2개 이상 + 우리 실험과도 합치.
2. **근거 부족/과장**: I2의 'veloBench 권장을 chromatin-aware로 확장' 부분(부분 비약), I4를 순수 공백으로 둔 점(우리 진척 누락).
3. **Validation 필수 기준**: Evidence(근거 위치) + Scope(과확장 여부)가 이 도메인에서 가장 자주 걸림.
4. **결과 상충 시**: 근거 개수·독립성 우선, 우리 내부 예비결과는 '잠정'으로 하위 가중.
5. **출력 형식 통일안**: Insight마다 {Status, 6기준 한 줄, Evidence 경로, Risk} — 4주차 OpenClaw agent가 파싱 가능하도록 고정. (→ CLAIMS.yaml 스키마와 정합, BIOP01-69.)
