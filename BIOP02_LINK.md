# BIOP01 ↔ BIOP02 연결 노트 (positioning cross-ref)

> 작성: 2026-07-10, BIOP02 세션에서 생성한 cross-reference 노트. **정본 아님** — BIOP01 결론의 canonical 원천은
> `pipeline/hspc-velocity-benchmark/results/FINDINGS.md`(★통합 결론) + `manuscript/novelty_strategy.md`.
> 이 파일은 그 결론을 (a) talk-ready 프레이밍으로 요약하고 (b) BIOP02와의 연결을 BIOP01 쪽에도 남기기 위함.
> ⚠️ **요약본이며 정본이 아니다.** 수치가 갱신되면 여기가 먼저 낡는다 — 인용은 반드시 위 정본에서 한다.
> (2026-07-22 커밋. 이때 방향 일치율을 48%에서 정정값 54.6%로 고쳤다.)

## 1. BIOP01 결론 — "벤치마크"가 아니라 반증형 결론 (talk-ready)
> **chromatin→transcription lag은 식별 불가·비재현이고, 전사율 α가 신뢰 가능한 예측 신호다.**

- ① **lag은 method-robust하지 않다** — 4방법 크기 |ρ|≤0.08, 방향 54.6%(정정값, 2026-07-19 — 방향 미정 lag=0 제외 전에는 48%로 읽혔다), permutation-FDR 공집합(CRAK 의존이라 민감도 arm으로 강등). "chromatin이 transcription을 prime한다"는 **분야 가정을 반증**.
- ② **음성대조**: ATAC 셔플(chromatin↔RNA 결합 파괴)해도 lag 불변 → lag은 chromatin 생물학이 아니라 **모델 구조 아티팩트**.
- ③ **건설적 대안**: 전사율 **α는 robust(ρ=0.88)·예측 가능(+0.31)**.
- ④ **메커니즘**: profile-likelihood — 목적함수가 lag을 데이터로 식별 못 함(α가 3.53× 민감, 94.57% 유전자). **관찰을 메커니즘으로 설명.**
- ⑤ **4개 외부 데이터셋 보존**(human_brain·E18 mouse·BMMC·macrophage).
- → **cautionary + 건설적 독립 논문감.** 발표·논문에서 "벤치마크 돌렸다"가 아니라 **"믿던 lag을 반증하고 α를 세웠다"**로 서술.
- 근거: `results/FINDINGS.md` §★통합결론·§1·§2·§8, `results/profile_likelihood_identifiability.md`.

## 2. BIOP02와의 연결 (치료효과 예측 서사)
- **BIOP02** = 정적 병리(H&E→분자아형→치료축 cost-of-substitution 지도). 가장 **불확실한 칸 = ER+/내분비**(H&E 정적으론 안 보이고 세포주 치료증거도 내분비 못 잡음, positive control 1/8).
- **내분비 저항 = 본질적으로 동역학**(상태 전이). 정적으론 원리적 한계 → **동역학 신호로 넘겨야 함.**
- **연결점:** BIOP01이 "**α는 robust·예측 가능·cross-dataset**"임을 증명 → ER+ 저항을 넘길 신뢰 신호가 막연한 velocity가 아니라 **구체적으로 α**. 두 프로젝트가 **ER+ 저항에서 만남.**

## 3. 연결의 위상 — **발표 서사만, 단독 논문/그랜트 아님**
- ⛔ 한 논문으로 묶으면 억지(데이터·생물학·방법 상이) → 심사자 "스테이플".
- ⛔ 그랜트 근거 아님(예비+발표+오픈repo는 그랜트 패키지 아님).
- ❌ **생물학 파이프라인(Paper C) 공개 데이터로 실행 불가**(2026-07-10 스쿱): 최적 데이터 **GSE240112(Genome Medicine 2024)가 이미 tamoxifen-저항 종양에 scVelo 적용** + 저항 환자 **n=3**(예측 태부족), 저항 라벨 있는 paired multiome 없음. → **새 paired-multiome(내분비요법하) 데이터 생성이 전제.**
- ✅ **용도 = 발표 vision 슬라이드**("정적 02가 못 푸는 ER+ 칸을 동역학 α로 넘긴다") + BIOP02 Paper A Discussion future-work 한 줄.

## 4. Target journal (참고, 잠정)
- **BIOP01**(critique+건설 tier): 현실 IF ~8–11 — Cell Systems / Molecular Systems Biology / eLife. Stretch = Genome Biology(~11)/Nature Methods Analysis. drug perturbation arm 붙으면 상승. (velocity 비판 선행 Bergen 2021 등 있으니 multiome chromatin-lag + 식별성 각의 fresh함이 관건.)
- (BIOP02 Paper A: 현실 IF ~6–9, npj Precision Oncology 등.)

## 5. 상호 포인터
- BIOP02 연결 문서(정본): `~/project/BioProject02/research/program-narrative/2026-07-10_biop01-02-static-dynamic.md`
- BIOP02 subtype 치료지도: `~/project/BioProject02/research/paperA-positioning/2026-07-10_subtype-decision-map.md`
- BIOP01 정본 결론: `pipeline/hspc-velocity-benchmark/results/FINDINGS.md`, `manuscript/novelty_strategy.md`
