# Methodology Brief — luo-2026-velocity-benchmark

## 한 줄 결론 (모든 독자)
- Citation: `@luo2026velocitybenchmark`  |  Importance: 상 (우리 HSPC 데이터 GSE209878이 benchmark Dataset12로 직접 포함, scenario별 method 선택 지침 즉시 적용 가능)
- 한 문장 결론: 15개 RNA velocity method를 17 real + 3 simulation dataset에서 accuracy·stability·usability로 비교해 "단일 정답 없음 + scenario별 권장 method"를 제시한 benchmark. 우리 HSPC velocity method 선택의 1차 근거.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` — 17 dataset 모두 공개. 우리 관심: Dataset12 HSPC = GEO GSE209878, Dataset17 mouse hematopoiesis = GSE81682, Dataset16 embryonic mouse brain 10x multiome = 10x Genomics.
- 코드 공개: `https://github.com/luo-cloud/veloBench` + Zenodo `10.5281/zenodo.18699599` (분석 스크립트). 각 method는 원저자 repo 사용(velocyto, scVelo, MultiVelo welch-lab, veloVI YosefLab 등).
- 자원 요구: 15 method 중 10개 GPU 경로(NVIDIA A800 80GB, 1TB RAM 환경에서 측정). LatentVelo·Pyro-Velocity·cell2fate는 GPU 필수. CPU 5종(velocyto, scVelo-sto/dyn, Dynamo-sto, CellRank)은 40-core/125GB로 실행. cell2fate·Pyro-Velocity 메모리 多, cellDancer·MultiVelo 실행시간 長.
- 핵심 의존성: scVelo, scanpy/anndata, dyngen(simulation), 각 method별 repo. MultiVelo는 `rna_only=True`(ATAC 없이)로 실행됨.
- 자세히 → [luo-2026-velocity-benchmark_core.md](luo-2026-velocity-benchmark_core.md) §Methods, §Tables(Table S1 dataset 목록)

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: **직접 호환** — 우리 HSPC 10x Multiome(GSE209878)이 Dataset12로 사용됨(transition: HSC→MPP, MPP→LMPP, MEP→Erythrocyte, GMP→Granulocyte).
- 자원 가능성: 우리 GPU 1대 + 128GB RAM으로 권장 method 다수 재현 가능. 단 cell2fate/Pyro-Velocity 대형 run은 메모리 주의.
- 비용·시간 추정: HSPC에 veloVI/DeepVelo/scVelo-sto 3종 비교 PoC = 약 1~2주.
- ROI 한 줄: 우리 데이터에 어떤 method를 쓸지의 third-party 근거 + cross-method consistency QC 설계를 그대로 차용. 단 MultiVelo multi-omic(ATAC-on) 성능은 본 논문이 비워둠 → 자체 검증 필요.
- 자세히 → [luo-2026-velocity-benchmark_lens-industry.md](luo-2026-velocity-benchmark_lens-industry.md) §3

## 우리 HSPC 데이터 method 선택 지침 (이 benchmark 직접 적용)
- 우리 HSPC는 hematopoietic branching = **complex topology** + UMI 깊이에 따라 부분적 **sparsity** 특성.
  - complex topology 권장(Figure 6D): **DeepVelo, veloVI, LatentVelo** (real accuracy + simulation 안정성).
  - low-quality/sparse 권장: **UniTVelo, LatentVelo, veloVI, Pyro-Velocity** (downsampling robust).
  - 교집합으로 **veloVI · LatentVelo**가 우리 HSPC의 1차 후보, **DeepVelo**가 정확도·usability 보강.
- 운영 원칙: 단일 default 금지. 위 후보 2~3개를 같은 HSPC anndata에 돌려 CBDir(HSC→MPP 등 알려진 transition 기준) + cross-method A1 consistency를 함께 보고 결론.
- 주의: rare progenitor·intermediate transitional cell의 undersampling이 erroneous trajectory를 만든다(Figure 4) → HSPC의 rare HSC/MPP subset 보존 필요. mature state(PBMC Dataset11 사례)에서 방향 신뢰도 낮음 — terminal cell 결론은 보수적으로.

## 본인 재회고 (본인)
- 질문: Dataset12(HSPC)에서 method별 개별 CBDir 순위는 합산 분포가 아니라 dataset-level로 어떻게 나오나? mmc1.pdf Figure S1/Table S1 추가 판독.
- 질문: ATAC 채널을 켠 MultiVelo가 우리 HSPC에서 RNA-only 대비 정확도가 오르는가? (본 논문 미평가 영역, epigenomic-lag 목표 직결)
- 다음 액션: HSPC subset에 veloVI + LatentVelo + DeepVelo 비교 PoC + cross-method consistency 리포트 — 다음 sprint(~2주).
- 자세히 → [luo-2026-velocity-benchmark_lens-academic.md](luo-2026-velocity-benchmark_lens-academic.md), [luo-2026-velocity-benchmark_lens-industry.md](luo-2026-velocity-benchmark_lens-industry.md) §4

---
마지막 갱신: 2026-06-12
