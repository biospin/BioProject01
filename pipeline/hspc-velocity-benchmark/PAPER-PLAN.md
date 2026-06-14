# PAPER-PLAN — Baseline chromatin→transcription coupling이 epigenetic drug response *timing*을 예측한다

> 우리 논문의 상위 설계(protocol). `DESIGN.md`는 이 중 **Part 1(lag 측정 도구 검증)**의 하위 프로토콜이다.
> 1차 타깃 = **drug-timing 예측**(최종 비전). 상태: Part 1 데이터(GSE209878) 확보, Part 2 약물 timecourse 데이터 **탐색 중**.

## 0. 한 줄 기여 (contribution)
처리 전(untreated) 단일세포 multiome에서 측정한 **gene별 chromatin→transcription 결합/lag**이, 같은(혹은 매칭되는) 세포계의 **epigenetic drug 반응 *timing*(반응 속도)**을 예측한다는 것을 정량적으로 보인다. → "어떤 유전자가 약물에 *빨리* 반응할지"를 baseline 후성유전 상태만으로 예측하는 첫 frameworks.

## 1. 중심 가설 (두 반쪽을 잇는 다리)
- **H_main**: baseline에서 chromatin이 이미 transcription과 강하게 결합된(짧은 lag, "poised") 유전자는 epigenetic drug에 **빠르게** 반응하고, lag이 길거나 buffered된 유전자는 **느리게/약하게** 반응한다.
- 따라서 baseline epigenomic feature(lag, promoter/enhancer ATAC, bivalency, burst kinetics 등)로 drug-response **timing**(예: 절반 반응 도달 시간 t½, 반응 onset)을 회귀/분류로 예측할 수 있다.

## 2. 논문 구조 (2-part)
| Part | 질문 | 데이터 | 산출물 |
|---|---|---|---|
| **Part 1 — lag 측정 + 도구 검증** | HSPC에서 gene별 chromatin→transcription lag을 *신뢰성 있게* 어떻게 재나? | GSE209878 (확보✓, P1 완료) | benchmark(`DESIGN.md`) → method 선정 + robust lag map (per-gene/per-lineage) |
| **Part 2 — 예측** | baseline lag/epigenome이 drug response timing을 예측하나? | **약물 timecourse (탐색 중)** + Part1 feature | 예측 모델 + 검증 + 생물학적 해석 |

> Part 1만으로도 독립 결과(HSPC lag landscape)지만, **우리 논문의 novelty는 Part 2의 예측 다리**에 있다. Part 1은 그 예측에 쓸 feature의 신뢰성을 담보한다.

## 3. 데이터 요건 (Part 2)
- 약물 = epigenetic modulator (HDACi/DNMTi/EZH2i/BETi/LSD1i 등).
- **timecourse 필수**(≥3 시점) — "timing"을 정의하려면.
- readout = transcriptome (+chromatin이면 가점), human hematopoietic/leukemia 우선.
- 시나리오 A: 단일 데이터셋이 baseline+timecourse 모두 제공. 시나리오 B: **GSE209878(baseline) + 별도 drug timecourse 페어링**(세포계 정합성·gene 축 매핑이 핵심 가정 → 검증 필요).
- → `lit-search` 에이전트 결과로 후보 확정 후 이 절 채움. (없으면 wet-lab 옵션 §7.)

## 4. 예측 모델 설계 (초안)
- **target(반응 timing)**: 유전자별 t½(half-response time) 또는 onset time / 반응 속도 상수. timecourse를 유전자별 sigmoid/exponential fit으로 추출.
- **features(baseline)**: ① chromatin→transcription lag(Part 1), ② promoter/enhancer ATAC accessibility, ③ bivalency/poising proxy, ④ burst kinetics, ⑤ baseline 발현·spliced/unspliced 비율. (강상관 → regularized; CLAUDE.md #3)
- **model**: regularized regression(Elastic Net) baseline → 비선형(GBM) 비교. feature importance로 해석.
- **평가**: gene-level cross-validation, **chromosome/lineage 단위 hold-out으로 leakage 방지**. permutation null로 예측력 유의성(CLAUDE.md #4).

## 5. 방법론 엄밀성 (DESIGN에서 승계)
within-lineage 계산 · rare lineage uncertainty 별도(MK/Baso/pDC/Lymphoid) · cell-cycle/burst/ambient/doublet 통제 · permutation FDR · pseudotime≠wall-clock(lag은 pseudotime 단위) · method≠preprocessing(공통 전처리, P1 완료).

## 6. novelty / scoop 점검 (진행 중)
- RNA velocity·multiome lag 측정은 선행 다수(우리 `paper_analysis/` 14편). **차별점 = 그 lag을 "drug response timing의 예측 변수"로 쓰는 것** — 측정에서 예측·인과로 한 걸음.
- `lit-search` 에이전트가 "baseline epigenome → drug timing 예측" 선행 출판 여부 점검 중. 겹치면 angle 재조정.

## 7. 리스크 / 결정 포인트
- **R1 (최대)**: 적합한 공개 drug-timecourse가 없을 수 있음 → (a) cell-line timecourse로 proof-of-concept, (b) 페어링 가정 약화, (c) wet-lab timecourse(팀/협업) 검토.
- **R2 페어링 타당성**: baseline(HSPC)과 drug(다른 세포계) 페어링 시 세포계 차이가 교란 → 같은 세포계 우선, 아니면 gene-intrinsic feature로 한정.
- **R3 인과 vs 상관**: "예측"은 상관. 인과 주장하려면 perturbation 일관성/방향성 별도.

## 8. 마일스톤
1. (지금) drug-timecourse 데이터 후보 확정 → §3 채움, 시나리오 A/B 결정.
2. Part 1 완주: P2 benchmark 실행 → method 선정 → robust lag map (`results/`).
3. Part 2: timing target 추출 → 예측 모델 → 검증 → 해석.
4. manuscript: Part1+Part2 통합, `paper_analysis/` 인용, figures.

## 9. 열린 결정
- [ ] 폴더명 `hspc-velocity-benchmark`는 Part 1 중심 명칭 — 논문이 drug-timing이면 상위 폴더명/프레이밍 재고(추후, churn 회피 위해 지금은 유지).
- [ ] 시나리오 A(단일) vs B(페어링) — 데이터 탐색 결과로 확정.
- [ ] target 정의(t½ vs onset vs rate) — timecourse 시간격자 보고 확정.
