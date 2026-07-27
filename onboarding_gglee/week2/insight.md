# insight — cross-paper Insight (4관점) [BIOP01-15]

요약이 아니라 논문 *간* 관계·패턴·gap. 근거는 `evidence_bundle.md`(E1–E5), `papers.jsonl`.

## Field Flow (흐름)
**I1.** velocity 계열은 "정확도 향상"이 아니라 **자유도 이동**으로 진화했다: scVelo(gene-global kinetics) → cellDancer/DeepVelo(**cell-specific**, latent-time 제거) → MultiVelo(**chromatin 축 추가**, 단 discrete·latent-time 복귀) → 두 분기가 MultiVelo의 서로 다른 제약을 각각 푼다 — MoFlow(latent-time 다시 제거) vs MultiVeloVAE(discrete→연속, single→multi-sample). 즉 최신 두 방법은 **경쟁이 아니라 상보적**(각기 다른 축을 완화). [E1]

## Differentiation Map (차별점·강약)
**I2.** chromatin-aware 4종은 겹치지 않는 강점을 판다: MultiVelo=재현 쉬움(CPU·foundational) / MultiVeloVAE=multi-sample·differential test(연구 확장성) / MoFlow=backflow 해소·latent-time-free(방향 안정) / CRAK-Velo=region-level 해석·동일 데이터 head-to-head. **약점의 공통 축**은 "chromatin의 인과 기여 미검증"과 "cell-cycle/척도". → 단일 default 대신 **2–3종 교차 실행 + 합의**가 방법론적으로 정당(veloBench의 'no single answer'와 일치). [E4, E1]

## Repeated Limitations (반복 한계)
**I3.** 세 한계가 방법을 가로질러 반복된다: (a) **chromatin 인과 분리 부재** — CRAK-Velo에 k=0 ablation 없음, veloBench가 MultiVelo를 ATAC-off로 실행 → "chromatin이 lag를 만든다"를 아무도 직접 시험 안 함. (b) **cell-cycle confound 미명시**(MultiVelo/VAE/MoFlow 공통). (c) **pseudotime≠wall-clock** → lag가 시간 단위가 아니라 drug-timing 예측에 직접 못 씀. [E2, E3]

## Unresolved Gaps (미해결·후속)
**I4.** 분야가 답하지 않은 질문: ① **ATAC-on이 RNA-only 대비 실제로 정확도/lag를 개선하는가?**(veloBench 공백) → 우리 HSPC에서 자체 ablation로 채울 자리. ② **chromatin→transcription lag가 method 간 재현되는가?**(cross-method consistency를 어느 논문도 보고 안 함) → 우리 파이프라인의 차별화 지점. ③ latent-time lag → wall-clock 매핑 anchor. ④ cell-cycle regress-out vs separate-fit의 lag 민감도. [E2, E3, E4]

> 종합: 이 분야의 진짜 공백은 "더 정확한 method"가 아니라 **chromatin의 인과성·method 간 재현성·시간 척도의 검증**이며, 이는 우리 HSPC multiome + 자체 ablation/cross-method 설계로 메울 수 있다.
