# Lens — Industry — Nomura 2024 mmVelo

> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 본 lens는 *산업·규제·임상* 관점만 다룬다 (학술 한계는 `nomura-2024-mmvelo_lens-academic.md`).
>
> 본 paper는 **bioRxiv preprint (peer-review 전, 2024-12-17 v1)** 이므로 본 lens는 *preprint를 산업적으로 다룰 때의 권위 가중치*를 별도 section (§2)에서 명시한다.

## 1. Categorization

- **Domain**: single-cell genomics, multi-omics (multiome scRNA + scATAC), chromatin velocity, deep generative model (VAE), transcription factor regulation inference.
- **Use case**: `methodology-reference`, `pipeline-applicable`, `academic-citation` (paper-info.yaml과 일치).
- **Importance**: **상** — 이유: epigenomic-lag 프로젝트의 *Week2 evidence_bundle*에서 *peak-level chromatin velocity*를 제공하는 *기술적으로 유일하게 직접적인* 후보. **단** preprint이므로 *evidence maturity*는 낮춰 다룬다 (§2 참조).
- **Authority weighting (Part 7.4 prefix)**:
  - `1차 출처:` paper 자체의 방법론·결과 진술 (PDF p.2 §1, p.13–14 §5.4–5.5).
  - `2차 출처:` 본 paper가 인용하는 선행 연구 (S. Ma 2020 SHARE-seq, Tedesco 2022 Chromatin Velocity 등).
  - 본 paper는 *peer-review를 거치지 않음* → 산업·BD 결정에 *단독 근거*로 사용 금지.

## 2. Preprint risk — 산업적 다룸 (별도 sub-section)

### 2.1 Preprint 일반 리스크

- **Peer review 부재**: PDF 각 페이지 footer *"this preprint (which was not certified by peer review)"*. 산업 결정 (예: 자체 pipeline 채택, BD 평가, IP 분석)에 *primary evidence*로 사용하면 안 된다.
- **Publication 시 변경 가능성**: bioRxiv v1 (2024-12-17 posted). publication accepted 시 reviewer 요청에 따라 (1) ablation 추가, (2) benchmark 수치 변경, (3) limitation 명시 강화, (4) code Zenodo deposit (현재 GitHub만, PDF p.23 §10.3에 "publicly available *for publication*"이라 명시) 등이 발생 → 본 분석에서 인용한 모든 수치는 *v1 기준*이며 publication 시 재검증 필요.
- **Reproducibility 보장 부재**: GitHub repository (https://github.com/nomuhyooon/mmVelo) 존재하나 *DOI-cited* code (Zenodo deposit)는 publication 시점이라고 명시 → 현재는 *moving target* 일 수 있음.

### 2.2 Publication 시점 추정과 모니터링 권장사항

미제공: 본 PDF에는 *submitted to* venue 정보 없음. bioRxiv preprint이라는 사실만 확인됨.

해석: 저자 그룹(Nagoya Univ. + National Cancer Center + Institute of Science Tokyo)이 *Nature Methods*, *Cell Reports Methods*, *Genome Biology*, *Bioinformatics* 같은 venue를 자주 이용 (관련 paper: Minoura 2021 scMM → Cell Reports Methods; Mizukoshi 2024 DeepKINET → Genome Biology). mmVelo가 *Nature Methods* 또는 *Cell Reports Methods* level을 노릴 가능성이 높음. *peer-review 기간 6–12개월* 추정. 

**모니터링 권장**:
- bioRxiv preprint page (https://www.biorxiv.org/content/10.1101/2024.12.11.628059v1)의 *new version* (v2, v3) 출시 알림.
- *published version* DOI가 부여되면 본 paper-info.yaml의 `version.published` 블록을 채우고 *수치 변경 여부*를 재검토.
- GitHub repository의 *Zenodo DOI release*가 등록되면 `sources.code[].zenodo_doi` 필드 추가.

### 2.3 권위 가중치의 *산업 결정에서의* 적용

| 결정 종류 | preprint 단독 근거로 가능? | 보강 필요 evidence |
|---|---|---|
| 내부 R&D scouting (method screen) | **Yes** | — |
| Pilot 적용 (우리 HSPC dataset에 실험적 적용) | **Yes**, 단 결과 해석은 보수적으로 | peer-reviewed alternative (MultiVelo) 와 동시 적용 |
| 정식 production pipeline 채택 | **No** | publication + 외부 cohort validation + code review |
| BD evaluation (라이선싱·collaboration) | **No** | publication + author group의 IP 상태 확인 |
| 제품화 (Dx/assay/SW) 의사결정 | **No** | publication + clinical validation + regulatory precedent |
| 규제 제출 자료 (FDA/EMA/PMDA) | **절대 No** | published peer-reviewed paper + GLP-validated data |
| 학회 발표 / 본인 논문 인용 | **Yes**, 단 "*as bioRxiv preprint, not yet peer-reviewed*"로 명시 | — |

### 2.4 Preprint 정정·철회 (correction/withdrawal) 리스크

미제공: bioRxiv preprint의 정정·철회 시 *논문 ID 자체*는 유지되지만 *version flag*가 바뀐다. 본 paper는 현재 v1이고 *withdrawn* 상태 아님 (2026-05-26 분석 시점 기준 확인 필요 — 본 PDF의 footer가 "version posted December 17, 2024"라 명시).

검토필요: 분석 진행 중 bioRxiv 페이지 상태 (withdrawn/superseded) 확인.

## 3. 산업·규제·임상 리스크 (preprint 리스크 외)

### 3.1 데이터 라이선스 / 사용 가능성

- **Code**: MIT/Apache 등 *명시적 라이선스*가 본 PDF에 적혀있지 않음. GitHub repository (https://github.com/nomuhyooon/mmVelo) 의 LICENSE 파일을 직접 확인해야 함 (검토필요).
- **Paper itself**: CC-BY 4.0 (PDF footer 명시). 본문·figure는 *attribution하면* 상업적 사용 가능.
- **Datasets**: 
  - 10x E18 mouse brain: 10x Genomics public dataset — *상업적 use* 가능 (10x EULA 확인).
  - SHARE-seq mouse skin GSE140203: GEO public, 데이터 자체는 *no usage restriction* (NIH GEO policy).
  - Human cortex GSE162170 (Trevino 2021): GEO public, 단 *인간 데이터*이므로 IRB·dbGaP 등 추가 access 정책 *해당 시* 확인.

### 3.2 Causal claim의 *RA/QA 리스크*

- TF-peak regulation 추론 (101,644 pair, FDR 0.001)이 *간접 prior signal* (CRM motif score, genomic distance)로만 validation됨 → *"이 TF가 이 enhancer를 조절한다"*는 *causal language*를 임상 또는 진단 context에서 직접 사용 시 over-claim 위험. *RA 측면*에서는 *predicted* / *putative* 같은 hedge word를 의무화.
- Cross-modal generation의 *batch / cohort generalization* 미보고 → 만약 *임상 cohort*에서 *missing modality velocity*를 *진단 feature*로 사용하려면 *별도 multi-cohort validation* 필수.

### 3.3 Reproducibility / pipeline 안정성

- 단일 GPU + AdamW + 500 epoch + early stop 30 epoch + minibatch 128 — PDF p.14 §5.6에 명시. *training time*은 미보고 (검토필요 — code repository에서 example notebook 시간 확인).
- *Hyperparameter sensitivity 실험 부재* (`nomura-2024-mmvelo_lens-academic.md` §1.2 (f)). 사내 pipeline에서 *robustness test*는 자체 책임.

### 3.4 데이터 모달리티 / 측정 기술 의존성

- 10x Multiome / SHARE-seq 같은 *paired chromatin + RNA* 측정을 *훈련 시 anchor*로 필요. *별도 anchor multiome cohort* 없이 *singleome only* 환경에 적용 시 cross-modal generation 신뢰도 미보장.
- Splicing kinetics anchor 의존 → *mature 조직, FFPE sample, low-quality unspliced* 환경에서 RNA velocity 자체가 불안정 → mmVelo도 동반 실패.

### 3.5 GPU / 컴퓨팅 자원 요구

해석: PyTorch + AdamW + ZINB decoder + MoE-VAE → *GPU 1대 이상* 필요. CLAUDE.md에 *GPU 1대 이상 권장*이 적혀있으므로 사내 환경에서는 만족 가능.

## 4. BD value & 상용화 가능성

### 4.1 BD opportunity 단계 평가

| 차원 | 평가 | 사유 |
|---|---|---|
| Method novelty | 중상 | peak-level chromatin velocity는 *기술적 novelty*가 있으나, *kinetic rate*가 아닌 *decoder projection*이라 MultiVelo와 *직교적 보완* |
| IP 상태 | 미확인 | 검토필요 — Nagoya Univ. / Institute of Science Tokyo / National Cancer Center 중 *patent filing* 여부 |
| Code license | 미확인 | 검토필요 — GitHub LICENSE 파일 |
| 협업 가능성 | 중 | 일본 academic group, *language/timezone* 협업 가능. *방법 차용 후 자체 변형 + 협업 paper* 시나리오 현실적 |
| 제품화 가능성 (직접) | 하 | research tool (Python library) 수준이지 *Dx/assay* 직접 제품화 어려움 |
| 제품화 가능성 (간접) | 중 | epigenomic-lag → drug response timing prediction의 *upstream feature engineering*으로 활용 → 우리 제품의 *내장 기술* 가능 |

### 4.2 상업적 시나리오

- **Scenario A — 자체 pipeline 채택**: mmVelo를 *우리 HSPC dataset*에 적용해 *peak-level lag*을 산출, 다른 method (MultiVelo, MultiVeloVAE, MoFlow) 와 head-to-head 비교 → *우리 자체 method 개발*의 baseline.
- **Scenario B — 협업/공저자 paper**: SHARE-seq mouse skin 외 *다른 lineage*에서 mmVelo benchmark 재현 + 우리 데이터셋 적용 결과로 *공저자 paper* (joint preprint).
- **Scenario C — 라이선싱**: 본 paper 자체가 *CC-BY 4.0*이므로 *attribution 만으로 상업적 활용 가능*. 코드 라이선스 확인 후 *내장 가능*. 단 *paper IP*는 작성 권리이며, 저자 그룹의 *patent filing* 여부 별도 확인 필요.

### 4.3 경쟁사·다른 method와의 BD 차별점

- MultiVelo는 *Welch lab (UMich)* — 미국 academic, 이미 Nature Biotechnology peer-reviewed.
- MultiVeloVAE는 *Gao 2024* — 후속 vae 확장.
- mmVelo는 *Shimamura lab (Tokyo) + Kojima (NCC)* — 일본 academic, **peer-review 전이지만 단독으로 peak-level이라는 unique angle**.
- BD 관점: mmVelo는 *peer-review 후* MultiVelo 와의 head-to-head publication이 등장하면 *positioning이 더 명확*해질 것. 현재는 *기술적 우월성*은 확인되었지만 *시장적 채택*은 아직.

## 5. 전문가 코멘트

### 5.1 활용 우선순위 (자체 R&D 관점)

| 우선순위 | Action | Owner | 기한 |
|---|---|---|---|
| 즉시 | Week2 evidence_bundle에 *preprint-tier* evidence로 추가, validation_report C7 supported로 격상 | 분석자 | 본 분석으로 완료 |
| 1주 내 | GitHub repository clone, README/dependency/example notebook 동작 확인 | 데이터팀 | — |
| 1개월 내 | 우리 HSPC 10x Multiome (GSE209878)에 mmVelo 적용 pilot | kkkim/jamie | — |
| 3개월 내 | mmVelo vs MultiVelo vs MultiVeloVAE vs MoFlow head-to-head benchmark on 동일 dataset | epigenomic-lag 팀 | — |
| 6개월 내 | bioRxiv preprint version flag 모니터링 + publication 출시 시 paper-info.yaml 업데이트 | 분석자 | — |

### 5.2 산업 환경에서의 *적용 안내*

- *Hedge language* 의무: TF-peak regulation 추론을 사용할 때 *"putative"*, *"predicted"*, *"computationally inferred"* 같은 hedge word 필수.
- *외부 validation* 의무: 임상/진단 맥락에서는 *cross-cohort validation*과 *experimental perturbation*이 없으면 *결정 근거*로 사용 불가.
- *Citation 형식* 의무: 본 paper를 인용할 때는 *"bioRxiv preprint, not yet peer-reviewed"*를 함께 표기.
- *Code dependency 추적*: PyTorch + scvi-tools 계열 dependency가 *minor version 변경*에 민감할 수 있으므로 *pinned environment*로 운영.

### 5.3 등급 판정 사유

- **상**: peak-level chromatin velocity output을 *유일하게* 제공하는 method (Fig S3m). 우리 Week2 evidence_bundle의 가장 큰 *technical gap*을 직접 메움.
- **단 preprint-tier**: 산업·규제 결정에 *단독 근거*로 사용 불가. publication 모니터링 필수.
- **종합 권장**: "**promote to evidence**" 하되 *preprint-tier flag*를 명시 유지. validation_report C7을 *partially-supported* → ***supported (preprint-tier)*** 로 격상 권장.

## 6. 질문 (분석자가 본인에게 던지는 follow-up)

- 질문: GitHub repository LICENSE 파일은 어떤 라이선스인가? (MIT / Apache / GPL / custom?)
- 질문: 본 저자 그룹 (Shimamura lab)의 *후속 preprint*가 더 있는가? — 특히 *variable kinetic rate + multimodal*을 통합한 방향.
- 질문: mmVelo와 MoFlow / MultiVeloVAE가 *동일 dataset 동일 metric*으로 비교된 적이 있는가? — 우리가 직접 만들어야 할 수도.
- 질문: 우리 HSPC dataset (GSE209878)에 적용 시 *cell count, peak count, GPU memory* 예상치는?
- 질문: publication 출시 시 *peer-review 후 변경*된 부분이 우리 차용 부분 (peak-level velocity 정의)에 영향을 주는가?

## 7. paper-info.yaml 갱신 권장 (본 lens 완료 시 적용)

```yaml
categorization:
  use_case:
  - "methodology-reference"
  - "pipeline-applicable"
  - "academic-citation"
  importance:
    level: "상"
    perspective: "epigenomic-lag Week2 evidence의 핵심 gap (gene-level chromatin aggregation)을 *peak-level decoder projection*으로 직접 보완. 단 peer-review 전 preprint이므로 *preprint-tier evidence*로 다루고 publication 모니터링 필수."
sources:
  code:
  - url: "https://github.com/nomuhyooon/mmVelo"
    type: "github"
    status: "url-only"
    note: "PyTorch implementation. Zenodo deposit은 publication 시점 (PDF p.23 §10.3 명시). LICENSE 파일 직접 확인 필요."
workflow:
  analysis_status:
    abstract: "done"
    core: "done"
    lens_academic: "done"
    lens_industry: "done"
    methodology_brief: "done"
    slides: "skipped"
```
