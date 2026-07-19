# 방향 신뢰의 사전 기준 탐색 — 임계·복합지표·pathway (BIOP01-57)

> 2026-07-19. 질문(kkkim): "방향은 ~13% loci에서만 method-robust"는 사후 집합이라 실행 규칙이 못 된다. **사전(a priori) 기준**(발현/α 임계, 복합지표, 유전자군)이 방향 일치를 예측하는가?
> 대상: `results/per_gene_direction_by_method.csv`의 방향 판정 가능 유전자(부호 가변 arm ≥2, n=640; 발현·rate 결합 후 n=506~538).

---

## 1. 발현·α 임계 — **성립하지 않음**

십분위별 합의 유형 (fit_alpha 기준, n=538):

| 분위 | median α | chromatin-만장일치 | RNA-만장일치 | **split** |
|---|---|---|---|---|
| D1 | 0.050 | 1.9% | 61.1% | 37.0% |
| D5 | 0.574 | 3.7% | 31.5% | 64.8% |
| D7 | 1.459 | 7.5% | 7.5% | **84.9%** |
| D9 | 4.940 | 16.7% | 0.0% | 83.3% |
| **D10** | **20.230** | **31.5%** | 0.0% | **68.5%** |

- Spearman(α, chromatin-만장일치) = **+0.250** (p=4.2e-09) / Spearman(α, RNA-만장일치) = **−0.472** (p=3.1e-31). abundance도 같은 방향(+0.201 / −0.347).
- **추세는 통계적으로 실재하나, 최상위 십분위에서도 방향 만장일치는 31.5%뿐이고 68.5%가 split.** 어떤 임계에서도 사용 가능한 신뢰 수준에 도달하지 못한다.
- ⚠️ **저α의 RNA-만장일치(D1 61%)는 축퇴(degenerate) 의심**: 전사가 거의 없는 유전자에서 모든 method가 기본값 근처로 수렴한 일치일 수 있어 진짜 신호가 아니다.
- 참고 수치 기준(HSPC MultiVelo fit): **fit_alpha** median 0.718 · 상위25% ≥2.482 · 상위20% ≥3.432 · 상위10% ≥7.747 · 상위5% ≥19.424. **abundance**(평균 Ms) median 0.036 · 상위25% ≥0.120 · 상위20% ≥0.155 · 상위10% ≥0.371 · 상위5% ≥0.740.
- 만장일치 chromatin 83개 중 전체 α 상위20%에 드는 비율은 **42.6%** — "고발현 유전자"로 정의되지도 않는다.

## 2. 복합 지표(가중 결합) — **성립하지 않음**
7 feature(fit_alpha·abundance·coupling·kap_alpha·kap_gamma·lag_mag·fit_alpha_c) 로지스틱, 5-fold CV로 chromatin-만장일치 예측:
- **CV AUC = 0.701** (사전기준 ≥0.70 간신히 통과)
- **점수 상위 10%에서도 만장일치 31.4% / split 68.6%** → 사전기준(≥70%) **실패**.
- 표준화 계수: **fit_alpha +0.885 단독 지배**(나머지 전부 |0.3| 미만) → 사실상 α 하나를 다시 쓴 것.
- **판정: 임계로도 복합지표로도 방향은 사용 가능한 신뢰도에 이르지 못한다.** 결정지도에 "발현 상위 X%에서는 방향 사용 가능" 같은 조건부 규칙을 **넣지 않는다**(초안에서 제안했다가 철회).

## 3. Pathway enrichment — 배경 보정 후 **한 갈래만 생존**
만장일치 chromatin 83개 (Enrichr):
- **기본 배경(전체 유전체)**: Neutrophil Degranulation adjP=3.3e-07(n=15) · Antimicrobial Humoral Response 1.6e-04 · Innate Immune 4.0e-05 · Platelet Degranulation 1.1e-03 · Hemostasis 4.6e-04 · Hallmark Coagulation 7.6e-04.
- ⚠️ 그러나 우리 유전자 집합은 이미 velocity-fit(고발현·동적) 유전자에서 뽑혔다 → **배경을 방향 판정 가능 유전자 640개로 교체**하고 재검정(Enrichr speedrichr custom background):
  - **Reactome: Neutrophil Degranulation adjP=9.44e-04 (n=15) · Innate Immune System 8.3e-03 — 생존**
  - **GO Biological Process: 유의 항목 전무** — 앞선 GO 항목들은 배경 편향으로 설명됨. Platelet/Hemostasis 계열도 탈락.
- 만장일치 **RNA-first(164)**: 어느 배경에서도 **유의 항목 없음**(일관된 생물학 없음 = 축퇴 의심과 부합).

## 4. 기제 서사 — "α가 지배하고 나머지는 발라내지 못한다"
위 결과들은 하나로 꿰인다:
- profile-likelihood: **α만 stiff**(κ +7.98) · α_c +7.32 · β +4.86 · **γ 가장 sloppy**(+1.72) → 우도가 α 방향으로만 뾰족.
- α_c는 method-fragile(cross-method ρ=0.29)인데 **lag은 그 흐릿한 switch-time의 *차이*** → 못 발라낸 성분의 차이라 잡음 증폭.
- 재현되는 건 α(0.88)뿐이고, 복합지표의 계수도 α 단독 지배(+0.885).
- **그리고 α 자체가 발현량과 ρ=0.809로 겹친다** → 현재 multiome velocity가 견고하게 회복하는 것은 사실상 "얼마나 발현되는가"에 가깝고, 그 너머의 kinetic 분해(chromatin 시차·분해속도)는 **분리되지 않는다**.
- ⚠️ 이는 구현 실수가 아니라 **정보 한계**(데이터가 그 방향으로 평평)다. 원 방법을 탓하는 서술이 아니라 "이 데이터·모델 조합에서 분리 불가"로 쓴다.

## 5. Neutrophil Degranulation의 생물학적 의미 — 어디까지 말할 수 있나
- **그럴듯한 근거**: 생존 유전자는 azurophil(1차) 과립 프로그램(MPO·ELANE·AZU1·PRTN3·CTSG·LYZ·S100A9·RNASE2 등). 이들은 promyelocyte 단계에서 좁고 강한 버스트로 켜졌다 꺼지며, C/EBPα·PU.1 등 계통결정 TF의 강한 통제와 enhancer priming이 잘 문서화된 **chromatin-potential의 교과서적 loci**다. 방향이 chromatin-first로 나오는 것은 알려진 골수 분화 생물학과 부합한다.
- **말할 수 없는 것(3중 제약)**:
  1. **일치 ≠ 정답**. 방향에는 외부 ground truth가 없다. method들이 동의한다고 그 방향이 옳다는 보장은 없다(공통 편향 가능).
  2. **인과 아님**. 명명 marker에서 ATAC-shuffle이 lag을 bulk보다 더 흔들지 못했다(MW p=0.58). 이 loci에서도 chromatin이 lag을 *만든다*는 증거는 없다.
  3. **SNR 경합 설명**. 이 유전자들은 on-off 동역학이 가장 날카롭고 발현이 높아, 방향이 *해상*되기 때문에 일치하는 것일 수 있다. 현 데이터로 생물학과 SNR을 분리 못 한다.

## 6. 데이터셋이 바뀌면 재현될까 — **대부분 검정 불가, 그리고 pathway 자체는 계통 특이적**
- 방향 합의에는 **부호 가변 arm이 2개 이상** 필요하다. 실제 보유: **HSPC 3개(MoFlow·CRAK·VAE), gastrulation 2개(MoFlow·VAE)**. macrophage·BMMC·E18은 1개(VAE), human fetal cortex는 0개 → **외부 대부분에서 방향 합의 재현을 검정할 수 없다**(MultiVelo는 구조적 양수라 제외).
- 게다가 **neutrophil degranulation은 HSPC계 우세 분화 프로그램**이다. gastrulation(마우스 배아)에는 호중구가 없으므로 **같은 pathway가 재현될 수 없다** — pathway 자체는 시스템 특이적.
- 일반화 가능한 형태가 있다면 "방향 일치는 그 시스템의 **우세한 말단 effector 프로그램**에 몰린다" 정도이고, 이는 **미검정**(gastrulation 2-arm으로 부분 검정 가능하나 현재 미실행).
- **결론: 이 enrichment는 HSPC 단일 시스템·단일 method 조합의 관찰로만 보고해야 하며, 일반 규칙으로 승격하지 않는다.**

---

## 논문 반영 지침 (절제)
- 본문에는 **한두 문장**으로: 방향 일치는 α와 함께 증가하나 최상위에서도 2/3가 불일치하여 **어떤 임계·복합지표도 방향을 사용 가능하게 만들지 못한다**. 일치가 관찰되는 소수 loci는 azurophil 과립 프로그램에 치우치나(배경 보정 후 Reactome Neutrophil Degranulation), **일치는 정답이 아니고 인과 대조는 음성이며 SNR과 분리되지 않아** 생물학적 주장으로 올리지 않는다.
- Supplementary에 상세(십분위표·복합지표 계수·enrichment 양 배경)를 둔다.
- 결정지도에 조건부 행을 **추가하지 않는다**(초안 제안 철회).
