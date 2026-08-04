# Wu et al., 2026 — Comprehensive benchmarking of RNA velocity methods across single-cell datasets — core 분석

> 근거 자료: `sources/wu-2026-velocity-benchmark.pdf`(본문 36p, Genome Biology 27:242) + `sources/fulltext_extracted.txt`(pypdf 추출, grep 근거). 본문에 텍스트로 명시된 method 이름·task 정의·metric·수치·dataset accession만 단정한다. Figure에서 읽어야 하는 값은 `검토필요:`로 표시한다.
>
> 표기: `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `검토필요:`.

## Executive Summary

- **무엇**: RNA velocity method가 급증(La Manno 2018 이후 RNA-only 17종 + multimodal-enhanced 9종)했으나 종합·표준 벤치마크가 없다는 문제의식에서, **19 도구 / 30 method를 34 데이터셋(26 real + 8 simulated)에서 8 task로 평가**하고 단일 랭킹 대신 **task-aware 선택 지침**을 제시한 resource/benchmark 논문. 새 method가 아니다.
- **평가 설계**: RNA-only 25종은 8 task 전부에서, multimodal-enhanced 5종은 **multimodal integration task 하나에서만** 평가. 핵심 4 task와 지표:
  - (I) **directional consistency** — CBDir(cross-boundary direction correctness) · ICVCoh(in-cluster coherence)
  - (II) **temporal precision** — CTO(cluster temporal ordering) · TSC(temporal Spearman correlation)
  - (III) **negative control robustness** — STS(self-transition score) · EES(effective entropy score)
  - (IV) **sequencing depth stability** — SCBDir · STSC
  - (추가 4 task: quantification stability 등)
- **핵심 결과**:
  - ① **directional consistency ↔ negative control robustness 사이 유일하게 유의한 음의 상관**(Spearman ρ = −0.572, P = 0.003). 방향 신호를 강하게 최적화한 method가 false positive 억제를 희생. **LatentVelo(std)가 directional 1위인데 negative control 23위**로 그 trade-off를 전형적으로 보여줌 — "dynamic inference 강조가 spurious velocity를 낳을 수 있다".
  - ② method 간 방향 불일치가 top method에서도 큼. UniTVelo(ind)·veloVI·VeloAE가 Data 1에서 HSC↔erythroid 방향을 역전 추정(Fig 3b). 같은 method가 Data 3에서는 옳게 추정 → **dataset 의존**.
  - ③ **multimodal integration task**: paired scRNA-seq+scATAC 3개(Data 22–24)에서 chromatin-enhanced 3종(MultiVelo, LatentVelo(ATAC), GraphVelo(ATAC))을 **CBDir·ICVCoh로 순위**. **GraphVelo(ATAC)가 CBDir에서 MultiVelo·LatentVelo를 크게 앞섬.**
  - ④ 개선 필요 gap 3종: gene dependence 모델링, temporal inference 정확도, multimodal architecture 설계.
- **우리 적용 / 스쿱**: 아래 §스쿱. 요지 = **스쿱 아님**(축이 다름), **반드시 인용**(타깃 저널 게재 + 우리 데이터 Data 6 사용), **차별화 문단 사활**, **GB desk-reject 위험 상향**.

## Identity

- **Title**: Comprehensive benchmarking of RNA velocity methods across single-cell datasets
- **Authors**: Yida Wu, Chuihan Kong, Xu Liao, Zhixiang Lin, Xiaobo Sun, Jin Liu (corresponding — `검토필요:` 정확한 소속·교신 이메일은 전문 헤더에서 확정)
- **Venue**: Genome Biology **27:242** (2026-07-27 게재), open access
- **DOI**: 10.1186/s13059-026-04182-z (preprint Research Square 10.21203/rs.3.rs-8708834/v1, 2026-02)
- **Citation key**: `wu2026velocitybenchmark`

## Background

RNA velocity는 spliced/unspliced mRNA 비율로 cell state transition 방향을 추정한다(La Manno 2018). 본문은 파이프라인을 preprocessing → velocity estimation → postprocessing 3단계로 정리하고, postprocessing에서 velocity matrix로부터 cosine-kernel 전이행렬을 만들어 저차원 임베딩에 투영한다고 명시한다. method 계보를 DL 11종(veloVI·scTour·SvelvetVAE·LatentVelo·VeloVAE 등 VAE 계열 + VeloAE·DeepVelo·cellDancer 비생성형) vs non-DL 14종으로 나눈다. multimodal-enhanced 9종은 chromatin accessibility(MultiVelo 등) 또는 metabolic labeling(Dynamo·VelvetVAE) 등 auxiliary 정보를 입력으로 쓴다.

- **해석**: 이 논문의 채점 지점은 [12] Luo·[13] Huang과 동일 계열이다 — velocity를 **임베딩/전이벡터 수준**(CBDir·ICVCoh)에서 평가하고 method를 순위 매긴다. multimodal은 8 task 중 1개(통합 task)에서만, 그것도 같은 CBDir·ICVCoh로 본다.

## 핵심 방법·결과 (근거 표시)

- **directional consistency**: CBDir(ground-truth transition으로 방향 정확도) + ICVCoh(cluster 내 cosine 일관성). — 본문 명시.
- **negative control robustness**: STS(self-transition score) + EES(effective entropy score). — 본문 명시. **해석: 이는 "정적/무-동역학 상황에서 velocity가 spurious하지 않은가"(출력 robustness)를 재는 것이다. 크로마틴을 파괴하는 우리 ATAC-shuffle 인과 대조와 목적이 다르다.**
- **trade-off 수치**: Spearman ρ = −0.572, P = 0.003 (directional vs negative control). LatentVelo(std) 1위 ↔ 23위. — 본문 텍스트 값.
- **multimodal**: Data 22–24(paired RNA+ATAC)에서 GraphVelo(ATAC) > MultiVelo·LatentVelo(ATAC) in CBDir. — 본문 명시. `검토필요:` 정확한 점수·ICVCoh 순위는 Fig 7 / Additional file 1 Table S9.
- **데이터셋**: 34개(26 real + 8 sim). **Data 6 = GSE209878 + GSE284047** — 본문 accession 명시. **외부 맥락: GSE209878은 우리 BIOP01 HSPC 1차 데이터. Luo 2026이 Dataset12로 쓴 것과 동일.**

## ★ 스쿱 점검 — 우리 원고(BIOP01) 대비 (전문 근거)

**판정: 스쿱 아님. [12][13]과 같은 계열의 세 번째 종합 벤치마크이며, 우리 6개 차별점이 전문 grep으로도 전부 유효.**

| 우리 차별점 | Wu 2026 본문 (grep 실측) |
|---|---|
| cell×gene velocity **행렬의 method 간 재현성**(층②) | 없음 — 임베딩 CBDir/ICVCoh만 |
| **ATAC-shuffle 인과 대조** | 없음 — negative control은 STS/EES(출력 robustness). `shuffle` 0회·`permutation` 0회 |
| **chromatin→lag 신뢰성·부호 편향** | 주제 아님 — `lag` 1회(무관 맥락) |
| **외부 측정 rate 앵커**(TT-seq·half-life) | 없음 — metabolic labeling은 method **입력**으로만(Dynamo·VelvetVAE) |
| **사전등록·permutation null·자기철회** | 없음 (`preregist` 0·`permutation` 0) |
| **MoFlow·CRAK-Velo 포함** | `MoFlow` 0회·`CRAK` 0회 (우리 4 arm 중 둘 미포함) |
| HSPC 10x multiome 특이 | 일반 scRNA-seq 34종. multiome은 3개 데이터·1 task |

- **negative control robustness 해소**: STS·EES 정의 확인 → "정적 상황 velocity가 spurious한가"이지 "크로마틴을 파괴하면 행렬이 움직이나"(우리 인과)가 아니다. 겹치지 않는다.
- **multimodal task 해소**: CBDir·ICVCoh로 MultiVelo 등을 **순위**한 것이지, 우리 **행렬의 method 간 재현성**도 chromatin-lag 신뢰성도 아니다.

## 우리 적용 (BIOP01)

1. **인용 필수** — 타깃 저널(GB) 게재 + 우리 데이터(GSE209878=Data 6) 사용. 미인용 시 리뷰어 첫 지적. refs에 [12][13] 옆 세 번째 벤치마크로.
2. **'무엇이 다른가' 문단 사활** — 같은 GB에 방금 종합 벤치마크. "우리는 임베딩이 아니라 **행렬**을, 순위가 아니라 **재현성·인과**를, RNA-only가 아니라 **multiome 4-arm**을, 그리고 **외부 측정 rate·사전등록**을 본다"를 앞세운다.
3. **저널 결정 영향(BIOP01-75)** — GB desk-reject 위험 상향("velocity 벤치마크를 방금 실었는데 또?"). CRM base-case 상대 안전성 ↑. 단 축이 갈려 '중복 아님' 방어 가능.
4. **부수 활용** — Wu의 GraphVelo(ATAC) > MultiVelo는 "새 multiome method가 계속 나온다 → 출력 신뢰성 감사가 필요"라는 우리 논지를 뒷받침. Discussion 한 줄.

## 심층

한계·재현 ROI·산업 시선은 `..._lens-academic.md` / `..._lens-industry.md` / `..._methodology-brief.md` 참고.
