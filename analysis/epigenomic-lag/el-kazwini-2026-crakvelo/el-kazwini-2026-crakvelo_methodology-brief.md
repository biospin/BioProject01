# Methodology Brief — el-kazwini-2026-crakvelo

## 한 줄 결론 (모든 독자)
- Citation: `@elkazwini2026crakvelo`  |  Importance: 상 (우리 GSE209878 HSPC에서 MultiVelo 대비 우위를 동일 셋업으로 입증한 chromatin-aware velocity, lag 파이프라인 1순위 baseline)
- 한 문장 결론: chromatin accessibility를 RNA velocity의 production rate로 직접 구성(UniTVelo 확장)하고 gene별 region weight를 산출하는 semi-mechanistic velocity — 우리 HSPC lag 분석에 직접 적용 가능, 단 lag는 후처리로 추출해야 함.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` — HSPC GEO GSE209878(preprocessed는 MultiVelo tutorial), E18 mouse brain 10x website, human cortex GEO GSE162170, TF ChIP-Atlas([22]).
- 코드 공개: Zenodo DOI 10.5281/(records/19247214) + GitHub StatBiomed/CRAK-Velo + cisTopic(github.com/Nour899/cisTopic). 재현 Jupyter notebook 포함. license는 코드 repo 확인 필요(검토필요:).
- 자원 요구: CRAK-Velo 본체 CPU(Intel Xeon Platinum), cisTopic Gibbs sampler GPU(A100 권장). HSPC ~15h + cisTopic ~3h. dataset당 10,000 epochs.
- 핵심 의존성: UniTVelo(base model, Eq. 4–7 계승), cisTopic(scATAC smoothing, Eq. 1–3), scVelo/scanpy(전처리), PAGA(transition graph).
- 자세히 → [el-kazwini-2026-crakvelo_core.md](el-kazwini-2026-crakvelo_core.md) §Methods, [sources/el-kazwini-2026-crakvelo.pdf](sources/el-kazwini-2026-crakvelo.pdf) §4

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: **일치** — 본 논문이 우리 GSE209878 HSPC 10x Multiome을 *동일 cell annotation*으로 사용. head-to-head 비교 진입 장벽 최소.
- 자원 가능성: 우리 환경(GPU 1장 + CPU)으로 재현 가능(추정). 기존 GSE209878 전처리물 재활용.
- 비용·시간 추정: 1일 compute(cisTopic 3h + CRAK-Velo 15h), 셋업 포함 ~1주.
- ROI 한 줄: MultiVelo 직접 대안을 *우리 데이터에서* 검증한 사례 → baseline 비교 + region-level lag raw material 확보. lag estimator 후처리 모듈은 별도 개발 필요.
- 자세히 → [el-kazwini-2026-crakvelo_lens-industry.md](el-kazwini-2026-crakvelo_lens-industry.md) §3

## 본인 재회고 (본인)
- 질문: region kinetic plot의 accessibility-peak ↔ unspliced-peak pseudotime gap을 우리 gene별 lag(시간 단위)로 환산하려면 pseudotime→wall-clock 매핑이 필요 — CRAK-Velo가 이를 제공하나?
- 질문: chromatin term ablation($k=0$)이 없어 chromatin 통합 효과가 인과적으로 분리 안 됨. 우리 비교에서 자체 ablation을 넣을 가치 있나?
- 다음 액션: CRAK-Velo vs MultiVelo head-to-head on GSE209878 — 이번 sprint(~1주), 산출물은 velocity field·terminal state·region 해석 정량 비교 리포트.
- 자세히 → [el-kazwini-2026-crakvelo_lens-academic.md](el-kazwini-2026-crakvelo_lens-academic.md), [el-kazwini-2026-crakvelo_lens-industry.md](el-kazwini-2026-crakvelo_lens-industry.md) §4

---
마지막 갱신: 2026-06-12
