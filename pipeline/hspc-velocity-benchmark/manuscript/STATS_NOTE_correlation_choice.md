# 상관계수 선택 근거 — 왜 Spearman인가 (Methods 보조 노트)

> BIOP01 벤치마크의 모든 per-gene 비교에 Spearman(순위)을 쓰는 이유. Methods "rank-based only" 문구의 상세 근거. (2026-07-19, kkkim 요청 기록.)

## Pearson vs Spearman
- **Pearson r**: 두 값의 **선형** 관계. 실제 값·스케일이 의미 있고, 대략 선형이며, 이상치가 적을 때. 값의 크기에 민감.
- **Spearman ρ**: **순위(rank)**에 대한 Pearson = **단조(monotonic)** 관계. 어떤 단조변환에도 불변, 이상치·왜곡에 강건, 선형·정규성 가정 없음. 순서만 본다.

## 우리 경우 — Spearman이 맞다 (강하게)
1. **절대율 비식별 + cross-context**: α는 HSPC에서 fit, 실측 합성율은 K562에서 측정. 절대값은 세포종·단위가 달라 비교 불가 — 유전자 순위만 의미 있음. Pearson(절대값)은 무의미. (논문도 "rank-based only, 절대율 non-identifiable(BayVel)"로 명시.)
2. **cross-method**: method마다 rate 파라미터화·스케일이 달라 값이 아니라 순위가 일치해야 함.
3. **cross-dataset**: 데이터셋마다 스케일 다름 → 순위.
4. **분포**: kinetic rate·발현·반감기는 heavy-tailed/로그성이라 Pearson은 소수 고값 유전자에 지배됨. Spearman은 강건.
5. **단조≠선형**: α↔합성율 같은 생물물리 관계가 포화 등 비선형 단조일 수 있음 → Spearman이 안전.

→ 우리의 per-gene cross-method·cross-dataset·외부검증·coupling 비교는 전부 Spearman이 정답이고 방어된다.

## 한 곳만 의도적으로 Pearson
partial correlation 계산에서 `stats.pearsonr(rank 잔차)`를 쓴다 — 이건 **partial Spearman의 정의**(rank(z)를 제거한 rank 잔차들의 Pearson = 부분 Spearman)라 맞다. 값이 아니라 이미 rank로 바꾼 잔차에 적용하는 것.

## 예외로 Pearson이 나을 때
단일 비교가능 스케일에서 선형 용량-반응을 볼 때 — 우리엔 해당 없음(cross-context). 그래서 전면 Spearman이 옳다.
