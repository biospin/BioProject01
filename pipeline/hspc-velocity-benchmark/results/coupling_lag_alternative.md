# lag 대체 지표(모델-free 크로마틴-RNA 결합) + abundance-보정 α — make-or-break (BIOP01-54)

## 쉬운 요약 (초심자용)
- velocity 프로그램은 유전자마다 여러 속도를 계산한다: 전사속도 α, 분해속도 γ, 그리고 크로마틴↔전사 **시간차(lag)**.
- 우리 자랑은 "**α는 프로그램을 바꿔도 값이 같고(재현), 실제 실험 측정(합성율)과도 맞는다**"였다.
- **질문 1 — lag 대신 쓸 지표가 있나?** 크로마틴과 RNA가 세포들 사이에서 같이 움직이는 정도("결합")를 재 봤다. 이건 크로마틴을 뒤섞으면 무너진다(=진짜 크로마틴을 씀 — lag는 뒤섞어도 안 무너져 가짜였다). **좋은 성질이나, 데이터셋을 바꾸면 재현이 약해서**(가장 비슷한 조직에서만 됨) lag의 재현 가능한 대체는 못 된다.
- **질문 2 — α는 진짜 kinetic인가, 그냥 "발현량"인가?** 발현량(유전자가 얼마나 많이 켜져 있나)은 velocity 없이도 그냥 세면 된다. 확인해 보니 **α는 발현량과 많이 닮았다(순위 상관 0.80)**. 실제 합성율과도 **발현량(0.41)이 α(0.26)보다 더 잘 맞았다** — 합성율=발현량×분해율이라 당연한 것.
- **그럼 α는 그냥 발현량인가?** 완전히는 아니다. **두 독립 프로그램이 α에 동의하는 정도(0.88)가, α가 발현량을 닮은 정도(0.80)보다 조금 크다** → α엔 발현량 너머의 *재현되는* 신호가 조금 있다.
- **결론**: α는 "발현량을 다르게 부른 것"까지는 아니지만 **대부분 발현량과 겹친다**. 그래서 "α가 실측에 앵커된 *유일한* 값"이라는 자랑은 **과하다** → 헤드라인을 "α만 재현된다 + lag은 크로마틴 무관(가짜)"로 옮기고, 실측 일치는 **보강 증거**로 낮춘다. (상세 = 아래 기술 절.)

---


> 2026-07-19. `scripts/p7_coupling_lag_alternative.py`, env scv-preprocess. 사전선언 반증기준 하에 검정.
> coupling[g] = Spearman(C[:,g], S[:,g]) across 21,878 cells (C=ATAC 크로마틴층, S=Ms spliced). HSPC MultiVelo 538 유전자.

## 결과 A — 모델-free 크로마틴-RNA 결합이 lag를 대체하는가

| 축 | 결과 | 사전선언 반증기준 | 판정 |
|---|---|---|---|
| 실재 | real median **+0.126**(87.2% 양) | — | 신호 있음 |
| **(1) 인과(ATAC-shuffle)** | shuffle median +0.021, **MW p=5.6e-75**, per-gene Δ +0.098(75.3% 양) | shuffle 불변이면 실패 | ✅ **통과** — 결합은 크로마틴-특이적(shuffle하면 붕괴). **모델 lag은 shuffle 불변이었음(ρ=0.72 보존)** → 이 축에서 결합이 lag를 이긴다 |
| **(2) abundance 통제** | coupling~발현 ρ=+0.167; 삼분위 real−shuffle Δ = low +0.073·mid +0.109·high +0.194 | 통제 후 gap 0이면 실패 | ✅ **통과**(경계) — 전 삼분위서 real>shuffle, 단 고발현서 gap 큼 |
| **(3) 재현성(cross-dataset)** | HSPC↔human_brain 결합 rank Spearman **+0.173**(shared 102) | \|ρ\|≤0.2면 실패 | ❌ **실패** — 모델 lag cross-dataset(+0.185)과 사실상 동일. 대체 못 됨 |

**판정 A: 대체 실패(재현성 기준).** 결합은 **데이터 수준에서 진짜 크로마틴-의존**이고(모델 lag이 못 넘은 인과 대조를 통과), abundance만으로도 설명 안 됨. **그러나 cross-dataset 재현이 모델 lag과 똑같이 약하다(+0.173 vs +0.185).** → "lag가 비재현인 건 모델 differencing 탓만이 아니라, **유전자별 크로마틴-전사 관계 자체가 dataset-특이적**이기 때문"이라는 더 강한 음성 서사. 단 검정은 원거리 조직(혈액→태아피질, n=102) 1건 — 근접조직(BMMC·macrophage) 재검이 남음.

## 결과 B — abundance-보정 α ~~partial~~ → **INVALID CONTROL (검정 무효, advisor 판정 2026-07-19)**
- (무효 실행) α vs synth (non-HK n=235): raw +0.262 → abundance 통제 partial −0.135.
- ❌ **이 partial은 무효다.** abundance = mean Ms ≈ steady-state s_ss = **α/γ** 라, 통제 변수가 **테스트 대상 α를 기계적으로 포함**한다. 자기 예측변수를 포함한 변수로 partial하면 α의 정당한 분산까지 제거되고 부호가 살짝 음으로 뒤집힌다 — −0.135는 그 수학적 산물이지 "α=abundance"의 증거가 아니다. **make-or-break가 발화하지 않았음(mis-specified).** abundance 교란은 critic MAJOR-1의 *명시된 한계*로 남으며, 이 실행으로 확증도 제거도 되지 않았다.
- **유효 재검정(아래 결과 B')로 대체.**

## 결과 B' — 유효한 abundance 검정 (head-to-head + γ 대칭) ⚠️ 헤드라인 불리
> `scripts/p7b_abundance_valid.py` (Spearman, non-HK).
- **B'-1 head-to-head (n=235)**: Spearman(α, synth)=**+0.262** vs Spearman(**abundance**, synth)=**+0.410**. → **발현량이 α보다 실측 합성율을 *더 잘* 예측한다.** velocity-fit α는 abundance baseline을 **못 이긴다**(kinetic 부가가치 없음, 오히려 더 noisy).
- **B'-2 γ 대칭 (n=222)**: Spearman(γ, k_deg)=−0.003(미회복) · Spearman(abundance, k_deg)=−0.074. → "합성은 회복·분해는 미회복"이라는 α/γ 비대칭이 사실 **abundance 수준 현상**(발현량이 합성과는 상관·분해와는 무관). velocity rate가 그 비대칭을 만드는 게 아님.
- **함의(심각)**: 논문의 유일한 양성 leg("α가 실측 합성율에 외부앵커")가 **trivial baseline(발현량)에 진다.** 심사자가 바로 이 head-to-head를 돌리면 무너짐. → advisor 재확인 후 헤드라인 재구성 여부 결정(reproducibility-only로 후퇴? 그마저 abundance 재현인지?).

## 결과 A' — 근접조직 coupling 재현성
- HSPC↔**macrophage**(HSPC-direct, shared 274): Spearman=**+0.281** → **재현(>0.2)** ✅
- HSPC↔**BMMC**(same tissue, shared 88): +0.175 → 미재현(≤0.2)
- HSPC↔human_brain(원거리): +0.173 · 모델 lag cross-dataset: +0.185
- **판정**: coupling은 **최근접 lineage(macrophage)에서만 재현**, 그 밖(BMMC·brain)은 미재현. "lineage-class 안에서 재현, 넘어서면 아님"이라는 정직한 nuance — 헤드라인 대체는 아니고 supporting texture. (BMMC 미재현은 n=88 소표본 caveat.)

## 결정 진단 (advisor 처방, 비-confounded) — α는 발현풀과 구별되나
> naive 상관은 전부 confounded(abundance=α/γ, synth=abundance×k_deg). 유일하게 안 얽힌 진단 = α가 발현량과 얼마나 같은지 vs 두 method가 α에 얼마나 동의하는지.

| 비교 | Spearman |
|---|---|
| MultiVelo α ↔ abundance (non-HK) | **+0.809** (all +0.795) |
| MultiVeloVAE α ↔ abundance | +0.747 |
| **MultiVelo α ↔ MultiVeloVAE α (cross-method)** | **+0.882** |

- **판정: cross-method(0.882) > α↔abundance(0.795~0.809)** → **α는 발현풀과 완전히 같지 않다**(두 독립 method가 α에 동의하는 정도가 α가 발현량을 닮은 정도보다 큼 = 발현 너머의 *재현되는* kinetic 신호 존재). **단 마진이 작다(0.88 vs 0.80)** — α는 대부분 발현량과 겹친다.

## ★ 최종 판정 & 논문 반영 (make-or-break 종료, advisor: "다음은 test 아니라 write")
1. **양성 헤드라인 생존하되 재구성 필수.** "α가 실측에 앵커된 *유일한* 출력"(현 제목/초록)은 **방어 불가** → 변경.
   - **리드 2 leg(비-confounded)**: ① 재현성 순서(α 재현 0.88, lag·γ 비재현) — α가 발현량 닮음(0.80)을 넘어서는 재현이라는 단서 포함 ② 인과 대조(lag=크로마틴-shuffle 불변).
   - **외부측정은 "corroboration"으로 강등**: "fitted α는 실측 합성율과 상관(+0.26, CI 0배제); 단 합성율의 곱인자인 steady-state abundance가 최소한 그만큼(+0.41) 상관하므로, 이를 α가 최정확 합성율 추정량이라는 주장이 아니라 *일관성 증거*로 다룬다."
2. **lag 대체(coupling)**: 재현 가능한 대체 아님(최근접 조직만) → 별도 헤드라인 금지. "인과 대조 통과하는 데이터-결합조차 lineage-class 넘으면 비재현"은 supporting texture(선택).
3. **abundance-보정 α(무효 partial −0.135)**: 기록만, claim 아님.
4. **메타**: 4연속 2번째 양성 탐색(곡률·lag대체·abundance-α×2)이 전부 음성/경계 → **신뢰 결정지도가 그 자체로 finding**. 2번째 헤드라인 억지 금지. 다음 = 본문 확정(write), drilling 중단.


## 종합 (PROVISIONAL — advisor 게이트 전)
- **lag 대체 후보(결합)**: 인과·abundance는 통과하나 **재현성 실패** → 재현 가능한 대체 지표는 아님. 다만 "인과 대조를 통과하는 데이터-결합조차 dataset-특이적"은 논문의 음성 결론을 **더 깨끗하게** 하는 부수 결과(근접조직 재검 후 판단).
- **abundance-보정 α**: partial이 붕괴 → α 외부앵커의 abundance 교란이 **심각하거나, 통제가 과제거**. 어느 쪽이든 헤드라인(α=외부앵커된 유일 rate)의 강도에 직결 → **advisor로 통제 타당성부터 확인 후** 본문 반영 여부 결정. 지금은 draft 미반영.
