# Week2 Handoff

## Status

- Paper Scrapper dry run: done
- Insight Agent dry run: done
- Validation Agent dry run: done
- Evidence set: `li-2023-multivelo`, `li-2025-multivelovae`, `hong-2026-moflow`, `li-2023-celldancer`, `nomura-2024-mmvelo`, `cui-2024-deepvelo`, `mizukoshi-2024-deepkinet`

## Jira / Confluence Ready Summary

### 핵심 결론

`epigenomic-lag` method 흐름은 MultiVelo를 baseline으로 두고 두 갈래로 확장된다.

- MultiVeloVAE: multi-sample, continuous factor, Bayesian differential test에 강함.
- MoFlow: latent time-free direct lag quantification과 cell-specific kinetic에 강함.
- cellDancer (full-analysis 승급): MoFlow의 *직접 predecessor*. *latent time-free cosine loss* lineage의 origin. chromatin 없음.
- DeepVelo (full-analysis 승급): GCN + continuity loss 기반 cell-specific kinetics. MultiVeloVAE의 cell-specific kinetics rationale의 RNA-only predecessor.
- mmVelo (full-analysis 승급, preprint-tier): *decoder-level peak resolution* chromatin velocity로 gene-level c aggregation gap을 *부분적으로* 메움. SHARE-seq에서 MultiVelo와 *직접 benchmark* (Fig S3j-m). per-peak ODE rate는 없음 — 공통 latent transition $d_n$ + peak-specific decoder branch.
- DeepKINET (full-analysis 승급): *in-house validation framework reference*. 2-stage decoupling + 100-repeat box-plot + negative correlation fail rule + cluster-level simulation benchmark가 transferable. labeling data 자체는 transfer 불가.
- 우리 프로젝트에서는 두 method (MultiVeloVAE / MoFlow)를 경쟁자로만 보지 말고 cross-validation pair로 쓰는 것이 합리적이며, DeepKINET-style framework로 validation design을 따로 설계해야 한다.

### 바로 실행할 액션

- [ ] MoFlow GitHub license 확인.
- [ ] mmVelo: PDF read 완료 (CC-BY 4.0 footer 확인). GitHub `nomuhyooon/mmVelo` repository의 explicit license 별도 확인.
- [ ] mmVelo Fig S3 box plot 정확 수치 (median, IQR, p-value)는 본문 textual report에 없음 → bioRxiv source data 또는 peer-review 출간본 모니터링.
- [ ] HSPC common input benchmark 설계:
  - MultiVelo
  - MultiVeloVAE
  - MoFlow
  - (선택) mmVelo — *peak-level* output을 lag framework로 어떻게 mapping할지 ablation 필요.
- [ ] metric set 고정:
  - CBDir
  - GCBDir
  - runtime
  - memory
  - shared gene/cell concordance
  - MoFlow lag score vs MultiVeloVAE $\delta/\kappa$
- [ ] MultiVeloVAE source data xlsx에서 exact benchmark matrix 추출.
- [ ] MoFlow supplementary/source data에서 129 reversal genes와 cluster 10 gene list 추출 가능 여부 확인.
- [ ] **DeepKINET-style validation framework 차용 설계 초안**:
  - 2-stage decoupling (lag-aware joint VAE → freeze → lag decoder)
  - 100-repeat box-plot evaluation (lag score correlation)
  - negative correlation = fail rule
  - cluster-level set-vs-estimated lag benchmark (chromatin-aware simulator 필요)

### 보류 / 검토 항목

- MoFlow lag group을 MultiVeloVAE differential test hypothesis set으로 넣는 hybrid workflow는 compatibility pilot 후 진행.
- enhancer-resolved lag modeling은 장기 아이디어로 유지. mmVelo의 *decoder-level peak resolution*은 *kinetic interpretation*이 아닌 *temporal ordering*만 제공한다는 caveat 명시 필요.
- 추가 paper analysis: DeepKINET이 *in-house validation framework reference*로 들어왔으므로 Week3 후보는 *chromatin-aware* 방향 — (a) perturb-seq + multiome paper, (b) time-resolved multiome / labeled chromatin assay paper, (c) BEELINE-style *chromatin-aware simulator* paper. C4 (causal validation)와 C8 (validation design transfer) 두 gap을 동시에 메울 수 있는 후보 선정 필요.
- `검토필요:` mmVelo peer-review 출간 모니터링 (bioRxiv 10.1101/2024.12.11.628059 v1 2024-12-17).
- `검토필요:` DeepKINET-Multiome 형태의 chromatin-aware extension 후속 publication 모니터링 (Welch lab 또는 Shimamura lab).

## 내가 해야 할 일

현재 repo 안에서 Week2 dry run은 완료됐다. 사용자가 직접 해야 할 것은 아래 결정뿐이다.

1. OpenClaw에서 이 산출물을 그대로 demo할지, 아니면 agent별로 다시 실행해서 생성 과정을 보여줄지 결정.
2. HSPC benchmark를 실제 다음 작업으로 진행할지 결정.
3. MoFlow license 확인을 내가 웹/GitHub 확인으로 진행해도 되는지 승인.

## OpenClaw Auto Mode 실행 프롬프트

아래 프롬프트를 OpenClaw Orchestrator에 넣으면 된다.

```text
AGENTS.md의 Evidence-to-Insight Workflow (Week2)와 openclaw/week2-agent-setup.md를 따라 실행해줘.

작업 topic은 epigenomic-lag이고 scope는 analysis/epigenomic-lag/_evidence/week2/scope.md를 사용해.

1. Paper Scrapper Agent는 skills/paper-scrapper/SKILL.md를 따라
   analysis/epigenomic-lag/_evidence/week2/papers.jsonl,
   comparison_table.md,
   evidence_bundle.md를 생성 또는 갱신해.

2. Insight Agent는 skills/insight-agent/SKILL.md를 따라
   evidence_bundle.md와 papers.jsonl을 읽고 insight.md를 생성 또는 갱신해.

3. Validation Agent는 skills/validation-agent/SKILL.md를 따라
   evidence_bundle.md, papers.jsonl, insight.md를 검증하고
   validation_report.md를 생성 또는 갱신해.

4. Integrator는 validation_report.md를 반영해서 handoff.md를 Jira/Confluence ready action item으로 정리해.

주의:
- 기존 analysis/<topic>/<paper-id>/ 개별 paper 분석 폴더는 수정하지 마.
- evidence에 없는 내용을 사실처럼 쓰지 마.
- full analysis가 있는 paper만 strong evidence로 사용해.
- insight의 claim은 validation_report.md에서 claim별 verdict가 가능하도록 작성해.
```
