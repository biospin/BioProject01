# gastrulation 일반화 검정 — 방향 일치가 우세 effector 프로그램에 몰리나 (BIOP01-58)

> 2026-07-19. HSPC에서 방향 만장일치 집단이 azurophil 과립 프로그램에 치우쳤다(배경보정 Reactome neutrophil degranulation adjP=9.44e-04). 이것이 **시스템 특이적 일화**인지 **일반 패턴**인지, 외부에서 유일하게 검정 가능한 시스템(gastrulation GSE205117, 부호 가변 arm 2개 = MoFlow·MultiVeloVAE)에서 검정.
> 방향 판정은 정정된 규약을 따른다: **lag이 정확히 0인 유전자는 방향 미정으로 제외**(`CORRECTION_sign_agreement_zero_handling.md`).

## 결과 (a) — per-gene 방향 일치: **정확히 우연**
- 공유 1,165 유전자, 방향 미정 104 제외 → **n=1,061**
- **sign-agreement = 50.6%** (이항검정 vs 50%: **p=0.713**)
- 대조: HSPC(MoFlow×MultiVeloVAE) **54.6%**(n=560, p=0.031) — 근소하게 우연 위였던 신호가 **외부에서 재현되지 않는다**.
- 각 method의 chromatin-leads 비율: MoFlow 66.4% · MultiVeloVAE 52.3%

## ★ 결정적 — "만장일치" 집단이 **독립 기대치와 일치**
| 조합 | 독립 가정 기대 | 관측 |
|---|---|---|
| both-chromatin | 0.664 × 0.523 = **0.347** | 368/1061 = **0.347** |
| both-RNA | 0.336 × 0.477 = **0.160** | 169/1061 = **0.159** |

두 method의 방향 판정이 **통계적으로 독립일 때 나오는 값과 소수점까지 같다.** 즉 gastrulation에서 "만장일치"는 **합의가 아니라 주변확률이 만든 부산물**이다. 방향에 대한 method 간 합의 구조가 **전혀 없다**.

## 결과 (b) — 만장일치 집단의 enrichment: 특정 프로그램 없음
배경 = 방향 판정 가능한 1,061 유전자(mouse symbol 대문자화), speedrichr custom background.
- Reactome: Integrin Cell Surface Interactions(adjP 1.2e-02) · Signal Transduction(2.1e-02) · Extracellular Matrix Organization(2.1e-02) 등 **일반적 발생·ECM 용어**만 경계 유의.
- GO BP: Positive Regulation Of Cell Migration/Motility · Cell Population Proliferation · Angiogenesis (전부 adjP 0.045~0.050, 경계).
- HSPC에서 본 것 같은 **특정 우세 effector 프로그램(과립 분비)에 해당하는 항목 없음.** (a)에서 집단 자체가 독립 부산물로 확인되므로, 이 약한 enrichment는 각 method가 어떤 유전자를 chromatin-leading으로 부르는 경향의 반영으로 읽는 것이 타당하다.

## 판정 — **일반화 실패 (사전 반증기준 (a)·(b) 모두 충족)**
- HSPC의 neutrophil-degranulation 치우침은 **HSPC 단일 시스템의 일화**이며 외부로 일반화되지 않는다.
- 나아가 gastrulation은 **더 강한 음성**을 준다: 방향 일치가 우연일 뿐 아니라 **합의 구조가 독립으로 완전히 설명된다.**

## 논문 반영 (절제, supporting)
- 한 문장: *"방향 일치 자체가 재현되는 현상인지 외부에서 검정할 수 있는 유일한 시스템(마우스 gastrulation, 부호 가변 arm 2개)에서 per-gene 방향 일치는 50.6%(n=1,061, 이항 p=0.71)로 우연이었고, 만장일치 집단의 크기는 두 method를 독립으로 가정한 기대치와 일치했다 — HSPC에서 관찰된 근소한 초과(54.6%)와 그 과립 프로그램 치우침은 외부에서 재현되지 않는다."*
- 효과: 방향에 대한 음성 결론이 **외부 재현으로 보강**된다. 헤드라인 승격은 하지 않는다(supporting).
