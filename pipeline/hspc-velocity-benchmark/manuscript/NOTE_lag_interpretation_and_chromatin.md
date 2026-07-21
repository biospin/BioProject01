# lag 해석 · 왜 모델이 못 뽑나 · 예시 유전자 · chromatin 구제 (Discussion 근거 노트)

> 2026-07-19 (kkkim 요청 "따로 잘 명기"). manuscript Discussion·Results 편입 근거. 근거파일 인용 포함.

## 1. 원 논문은 lag를 어떻게 "의미 있다"고 했나
- MultiVelo(Li et al. 2023 등)는 유전자별 전환시각 t_sw1(chromatin 열림)·t_sw2(transcription 켜짐)·t_sw3(닫힘)을 fit하는 다상태 ODE. **lag = t_sw2 − t_sw1** = chromatin이 열리고 transcription이 켜지기까지의 priming 간격으로 해석, 유전자를 priming/decoupling으로 분류.
- 검증 방식 = **개념(chromatin potential, Ma 2020) + 예시 유전자**(chromatin이 눈에 띄게 먼저 열리는 canonical marker). **per-gene lag가 method 간 재현되는지·chromatin을 실제로 쓰는지는 검정하지 않음.** ← 우리 기여의 공백.

## 2. 왜 velocity 모델이 chromatin 신호를 신뢰성 있게 못 뽑나
- lag는 **두 fit 값의 *차이*(t_sw2 − t_sw1)**. 두 전환시각은 개별적으로 sloppy(우도 평탄, profile-likelihood §8 + ConsensusVelo[16] 확인). **흐릿한 값의 차이 → 잡음 증폭, 신호 소실.**
- **구조적 부호**: MultiVelo 4-state는 t_sw 단조 정렬(t_sw1<t_sw2<t_sw3) → `sw2−sw1` **정의상 양수**(chromatin 100% 먼저) = 모델 제약, 데이터 아님(`concordance.md:12`). 진짜 방향 검정은 부호 가변 method(MoFlow DTW)에서만.
- **인과 shuffle 불변**: ATAC 유전자 라벨을 뒤섞어도 lag 분포 불변(per-gene ρ=0.72, MW p=0.20, `scrambled_null.md`) → lag는 RNA 동역학+모델 구조로 정해지고 **chromatin 신호를 거의 안 씀**.
- cross-method: |ρ|≤0.08(sign 48%=우연). cross-dataset: 다섯 시스템 어디서도 무신호(+0.03~+0.19).

## 3. 예시(canonical marker) 유전자에서는 — **의미 있으나 select loci·일화 수준**(2026-07-19 MoFlow 부호검증으로 정밀화)
⚠️ **부호 정당한 method로 재검정.** MultiVelo 부호는 구조적(485/485 양수, `moflow_directional_check.md`)이라 방향 근거 불가. **부호 가변 method = MoFlow**(`moflow_genes.csv`, cs_lag)로 봐야 함.

**검증 결과 (MoFlow cs_lag):**
- **전역 chromatin-leads = 51.3%**(n=636) = 50/50 → genome-wide "chromatin 먼저"는 **미지지**.
- **canonical marker 15개 전체도 53.3%** = 배경과 같음 → marker가 특별히 chromatin-first인 것은 **아님**.
- **그러나 계통-구조 방향은 생물학과 일치**: 골수/과립구 priming marker **ELANE +0.148·AZU1 +0.368·MPO +0.078·LYZ +0.123 = chromatin-first(4/5, median +0.123)** / HSC 유지 marker **HLF −0.289·CRHBP −0.303·MEIS1 −0.060 = RNA-first**. (혼재: CSF1R −0.045 약RNA, TFRC/MK 양, IRF8/TCF4 음.)

**정직한 서술(논문)**: "원 방법들이 예시로 보인 chromatin-potential은 우리 데이터의 **특정 계통 loci**에서 부호-가변 method(MoFlow)로도 재현된다 — 과립구 priming 유전자(ELANE·AZU1·MPO)는 chromatin-first, HSC 유지 유전자는 RNA-first로 알려진 생물학과 맞는다. **다만 genome-wide 방향은 ~50/50이고 canonical marker 패널 전체도 배경 대비 enrich되지 않아(53%≈51%), 이는 *select loci의 일화적 성립*이지 재현 가능한 genome-wide 정량 지표가 아니다.** MultiVelo의 균일 chromatin-first는 switch-time 단조정렬의 구조적 산물이다." → **원 논문을 부정하지 않으면서**(예시는 재현) 정량·genome-wide 지표로서의 한계를 구분. 인과도 아님(marker shuffle MW p=0.58).
- ⚠️ **cherry-pick 주의**: marker는 사후 선택이라 엄밀 enrichment 검정 아님(사전정의 marker set+정식 null 필요). 그림/표로 넣을 땐 "illustrative, 생물학과 일치, 단 genome-wide 미재현"으로 한정.

## 4. coupling — chromatin 신호는 실재, 모델이 못 뽑음 (진단으로 편입)
- 데이터 수준 chromatin-RNA 결합 coupling[g]=Spearman(C[:,g],S[:,g]): real median +0.126 → **ATAC shuffle하면 +0.021로 붕괴**(MW p=5.6e-75). **모델 lag은 shuffle 불변이었음** → 극명한 대비.
- **의미**: chromatin 신호는 데이터에 실재하고 유전자-특이적(shuffle에 민감). lag의 실패는 *chromatin이 없어서가 아니라 velocity 모델이 그 신호를 버려서*다. ATAC-shuffle 인과대조(lag=chromatin 안 씀)와 **짝**을 이루는 정합 기제.
- **한계(정직한 천장)**: cross-dataset 재현은 최근접 lineage(macrophage +0.281)만, BMMC +0.175·brain +0.173 미재현 → 신호는 실재하되 lineage-특이적. **재현 가능 lag 대체 헤드라인 아님**(supporting/diagnostic만).

## 5. chromatin 구제 — scope 명시 (over-reach 방지)
- 우리 음성은 **"RNA velocity라는 특정 과제에서 현재 multiome 방법이 chromatin으로 신뢰할 새 kinetic 출력(lag)을 못 만든다"**에 한정.
- **"chromatin/epigenomics가 무의미"가 아니다**: (a) 우리 coupling이 chromatin 신호 실재를 보임, (b) chromatin의 세포상태 식별·enhancer-gene 연결·regulatory 추론 가치는 **우리 범위 밖**이고 부정하지 않는다.
- 논문 메시지 = "chromatin 신호는 실재하나 현재 velocity 모델이 신뢰성 있게 못 뽑는다 → 신뢰 지도: α는 믿고(재현), lag은 직교검증, 데이터-결합은 계통 안에서 참고."
