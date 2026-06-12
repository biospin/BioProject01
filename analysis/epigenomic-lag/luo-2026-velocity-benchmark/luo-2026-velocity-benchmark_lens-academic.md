# Lens — Academic

> 근거: `luo-2026-velocity-benchmark_core.md` + `sources/luo-2026-velocity-benchmark.pdf`. Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.

## Limitations

### 저자가 명시한 한계 (Discussion · Limitations of the study)

- **CBDir의 ground-truth 의존**: accuracy metric인 CBDir이 pre-defined ground truth(curated trajectory·biological knowledge)에 기반하므로 incomplete prior information·annotation bias에 취약. ground-truth 정의가 dataset마다 달라 benchmark 결과를 좌우.
- **high coherence ≠ fidelity**: ICCoh·velocity consistency가 높아도 이는 trajectory over-smoothing의 결과일 수 있고, biological continuity를 과장해 bifurcative/multifurcative trajectory에 bias를 준다.
- **method 간 inconsistency의 해석**: LatentVelo vs cell2fate 같은 불일치는 inference error가 아니라 distinct model architecture·가정의 반영일 수 있음 → "어느 쪽이 틀렸다"로 환원 불가.
- **신규 method 미포함**: 분야가 빠르게 발전해 일부 신규 method를 benchmark에 넣지 못함(15개로 한정).
- **downsampling은 sampling bias의 단순 모사**: 실제 데이터의 bias는 더 복잡. 다만 rare/intermediate cell undersampling이 erroneous trajectory를 만든다는 추세는 일관.

### 분석자가 판단한 한계

- **MultiVelo를 `rna_only=True`로 평가한 것**: 부족한 점 — 본 benchmark는 MultiVelo·Chromatin Velocity 등 epigenome-integrating method를 *RNA 채널만으로* 돌렸다(STAR Methods, MultiVelo `rna_only=True`). 왜 중요한가 — 이 method들의 존재 이유인 chromatin accessibility 통합이 평가에서 배제됐다. 우리(epigenomic-lag) 목표에서 정확히 필요한 multi-omic 모드 성능이 *측정되지 않았다*. 어떤 증거가 부족한가 — 10x Multiome(ATAC+RNA)에서 chromatin 채널을 켠 MultiVelo의 CBDir/ICCoh. Dataset16(embryonic mouse brain 10x multiome)이 multiome인데도 ATAC를 활용한 평가는 본문에 없음.
- **dataset별 method 순위의 부재**: 부족한 점 — Figure 2/S1은 17 dataset을 합친 분포 위주이고, "Dataset12(HSPC)에서 어느 method가 1등"인지 *수치 표*가 본문에 없다. 왜 중요한가 — 우리는 합산 순위가 아니라 *우리 데이터와 같은 hematopoietic branching*에서의 순위가 필요. 어떤 증거가 부족한가 — dataset-level metric breakdown(mmc1/mmc2에 부분 존재 가능, 본 core에서 미판독).
- **정확도 절대값이 낮음에도 "권고"로 전환**: 부족한 점 — 최고 CBDir이 0.23(veloVI)이고 전체 평균 ≈0.1로 낮다. 왜 중요한가 — "best-practice 권고"가 *상대 순위*일 뿐 *절대 신뢰도*를 보장하지 않는다. 어떤 증거가 부족한가 — CBDir 0.23이 downstream biological 결론을 신뢰할 수준인지에 대한 외부 검증(예: lineage tracing 정답과의 정량 비교).
- **A2(median 대비 정렬)의 순환 논리 위험**: 부족한 점 — A2는 모든 method의 median vector를 consensus로 삼는다. 왜 중요한가 — 다수 method가 같은 방향으로 틀리면 median도 틀린 방향이 되고, 그에 정렬되는 method가 "consistent"로 보상받는다. 어떤 증거가 부족한가 — median consensus가 ground truth와 얼마나 일치하는지의 직접 비교.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: "veloVI·Pyro-Velocity가 accuracy 최고" → "세 시나리오 모두에 veloVI 권장". 하지만 low-quality 시나리오 권고에는 UniTVelo·LatentVelo(accuracy가 아니라 stability 우위)가 함께 들어간다. accuracy 1위와 시나리오 권고의 논리 연결이 metric 간 가중치 없이 서술돼 있어 *왜 그 조합인지*가 Figure 6D 외에는 정량 근거가 약하다.
- **"unseen에서 더 높은 CBDir"**: 일부 method가 처음 보는 dataset에서 tested dataset보다 CBDir이 높았다는 관찰(Figure S1C)은 over-fitting 부재의 신호로 읽힐 수도, ground-truth 정의 편차로 읽힐 수도 있는데 본문은 해석을 길게 달지 않는다.

## 다음 논문 / 후속 분석 아이디어

- **multi-omic 모드를 켠 velocity benchmark**: 같은 17(또는 multiome subset) dataset에서 MultiVelo·Chromatin Velocity를 ATAC 채널을 켠 상태로 재평가. 우리 epigenomic-lag 목표에 직결되는 빈칸을 메움. `질문:` ATAC를 켜면 HSPC(Dataset12)·embryonic brain(Dataset16)에서 CBDir이 RNA-only 대비 얼마나 오르는가?
- **lineage-tracing ground truth와의 정량 검증**: CBDir의 pre-defined ground truth 대신 실측 lineage(예: scEU-seq, metabolic labeling Dataset13) 정답으로 method를 채점해 절대 정확도 한계를 검증.
- **HSPC 전용 mini-benchmark**: Dataset12(GSE209878) + Dataset17(GSE81682)만으로 hematopoietic branching에 특화된 method 순위 재산출. 우리 데이터 적용 직전 단계.

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장
- §Summary: "no single method exhibited superior performance in all the assessments, and unexpected underperformance was observed in certain cases"
  - 사용 시나리오: 본인 introduction/methods에서 "단일 velocity method를 default로 고정하지 않는다"는 선택을 정당화할 때.
  - BibTeX key: `@luo2026velocitybenchmark`
- §Discussion: "we recommend adopting a multi-method comparison strategy that emphasizes cross-method consistency in downstream biological interpretations"
  - 사용 시나리오: 우리 pipeline에서 여러 method 결과를 교차 비교하는 설계의 근거.
  - BibTeX key: `@luo2026velocitybenchmark`
- §Results: human bone marrow에서 평균 CBDir이 −0.193까지 하락, mature PBMC에서 대부분 method가 biology와 반대 방향
  - 사용 시나리오: complex/mature hematopoietic state에서 velocity 신뢰도가 낮다는 caveat.
  - BibTeX key: `@luo2026velocitybenchmark`

### 인용 가능 수치
- veloVI CBDir=0.23(전체 1위), Pyro-Velocity 0.17 (§Results, Figure 2A)
  - 사용 시나리오: velocity accuracy의 현실적 상한을 인용.
- LatentVelo ICCoh=0.99, UniTVelo·MultiVelo 0.96 (§Results, Figure 2B)
  - 사용 시나리오: high coherence가 over-smoothing 신호일 수 있음을 논할 때.
- Pyro-Velocity·cell2fate CBDir range −0.11~0.403 (downsampling 불안정) (§Results, Figure 4A)
  - 사용 시나리오: sampling robustness가 method 선택 기준임을 보일 때.

### 인용 가능 Figure/Table
- Figure 6D (scenario decision tree)
  - 무엇: large atlas / low-quality / complex topology 3 시나리오별 권장 method 분기.
  - 사용 시나리오: 본인 review·methods에서 method 선택 가이드 도식으로 인용.
  - BibTeX key: `@luo2026velocitybenchmark`
- Table S1 (17 dataset 목록 + accession)
  - 무엇: 분야에서 반복 사용되는 velocity benchmark dataset 카탈로그(Dataset12 = HSPC GSE209878 포함).
  - 사용 시나리오: 우리 dataset이 표준 benchmark에 포함됨을 근거로.

## Final Takeaways

- 이 paper의 학술적 가치는 *새 알고리즘*이 아니라 *분야 전체의 신뢰도 지도*다 — "절대 정확도는 낮고(최고 0.23), 단일 정답은 없으며, method 간 합의가 약하다"를 정량화한 것.
- 우리 입장에서 가장 매끄럽지 않은 지점은 *MultiVelo가 chromatin을 끈 채 평가됐다*는 것. 이 benchmark는 우리의 multi-omic 질문에 직접 답하지 않으므로, RNA-only 성능 순위만 차용하고 multi-omic 검증은 우리가 따로 해야 한다.
- 다음 액션으로 가장 ROI 높은 것: Dataset12·17 기반 HSPC-특화 mini-benchmark를 우리 데이터로 재현해, 합산 순위가 아닌 hematopoietic branching 순위를 직접 얻는 것.
