# Paper Research Agent Router

이 프로젝트는 scientific paper를 분석하고 구조화된 노트를 `analysis/<topic>/` 아래에 저장한다.
라우팅 규칙은 이 파일에, 분석 규칙은 각 `skills/` 아래 SKILL.md에 있다.

## 언어
- 기본 출력은 한국어로 작성한다.
- 아래 목록의 scientific term은 영어로 유지한다. 각 skill의 언어 규칙은 이 목록을 공통 기준으로 삼는다.
  - 생물학 / genomics: `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `pseudotime`, `perturbation`, `causal evidence`
  - 데이터 / 실험: `baseline`, `dataset`, `benchmark`, `metric`, `Figure`, `panel`, `Spearman`, `ablation`, `replicate`, `control`
  - 통계 / 기계학습: `likelihood`, `prior`, `posterior`, `latent variable`, `ODE`, `loss function`, `regularization`, `optimization`, `variational inference`, `Bayesian`
- 영어 용어를 처음 사용할 때 필요한 경우 짧게 한국어 설명을 덧붙인다.
- 문장 전체를 영어로 쓰지 않는다.

## 출력 경로
- 입력 PDF는 `papers/`에 둔다.
- 분석 결과는 `analysis/<topic>/<paper-title>/full.md`에 저장한다.
- topic folder name은 사용자가 준 주제를 kebab-case로 정규화한다.
- paper title을 folder name으로 사용한다. title을 신뢰도 있게 추출할 수 없으면 PDF filename을 사용한다.
- topic이 명시되지 않으면 대화 맥락에서 추론하거나, 추론이 불가능하면 짧게 물어본다.

## Agent 목록

| Agent | Skill | 실행 시점 |
|---|---|---|
| Figure 1 Decode | `skills/fig1-decode/SKILL.md` | 논문 분석 시작 시 항상 첫 번째 |
| Claim Extract | `skills/claim-extract/SKILL.md` | fig1-decode 이후 |
| Quality Gate | `skills/quality-gate/SKILL.md` | claim-extract 이후, 깊은 분석 전 |
| Results Scan | `skills/results-scan/SKILL.md` | quality-gate 판정 "보통" 이상일 때 |
| Method Reference | `skills/method-ref/SKILL.md` | 필요할 때만 (on-demand) |
| Apply Map | `skills/apply-map/SKILL.md` | results-scan 이후 |
| Takeaway | `skills/takeaway/SKILL.md` | results-scan 이후 |
| Paper Scrapper | `skills/paper-scrapper/SKILL.md` | 논문 2개 이상, cross-paper 비교 자료가 필요할 때 |
| Insight Agent | `skills/insight-agent/SKILL.md` | paper-scrapper 이후 |
| Paper Network | `skills/paper-network/SKILL.md` | 논문 2개 이상일 때 |
| Paper QA | `skills/paper-qa/SKILL.md` | 분석된 논문에 대한 질문 시 |
| Slide Deck | `skills/slide-deck/SKILL.md` | 슬라이드 명시적 요청 시 |
| Claim Verify | `skills/claim-verify/SKILL.md` | insight 검증 요청 시 |
| Paper Digest | `skills/paper-digest/SKILL.md` | 논문 단락 순서 따른 1페이지 압축 요청 시 |

## 단일 논문 분석 워크플로우
PDF 한 편을 분석할 때 다음 순서를 따른다.

1. topic을 정하고 `analysis/<topic>/` folder를 준비한다.
2. **fig1-decode** — Figure 1로 논문의 핵심 접근법을 파악한다. Figure 1이 unhelpful하면 대체 전략을 사용한다.
3. **claim-extract** — Abstract / Introduction 발췌독으로 핵심 주장과 gap을 뽑는다.
4. **quality-gate** — 저널 수준, 저자 기관, 근거 품질, paper mill 위험을 평가한다.
   - 판정이 "읽지 않음 권고"이면 분석을 여기서 멈추고 사용자에게 알린다.
   - 판정이 "낮음"이면 사용자에게 알리고 계속 여부를 확인한다.
5. **results-scan** — 데이터셋, 수치 결과, Figure 증거를 정리한다.
6. **apply-map** — 이 논문을 내 연구에 어떻게 쓸 수 있는지 평가한다.
7. **takeaway** — 논문이 열어놓은 질문과 다음 연구 방향을 정리한다.
8. **method-ref** — results-scan 또는 apply-map에서 방법 이해가 필요하면 그 시점에 실행한다.
9. `analysis/<topic>/<paper-title>/full.md`에 저장한다.

## 복수 논문 분석 워크플로우
여러 논문을 같은 topic으로 분석한 뒤:

1. 각 논문에 대해 단일 논문 워크플로우를 실행한다.
2. **paper-scrapper** — 각 `full.md`를 `scope.md` / `papers.jsonl` / `comparison_table.md` / `evidence_bundle.md`로 구조화한다.
3. **insight-agent** — Field Flow, Differentiation Map, Repeated Limitations, Unresolved Gaps 4관점의 cross-paper insight를 만든다.
4. **paper-network** — 저자 겹침, 기관 클러스터, 기업 연관, research lineage를 분석한다.

cross-paper 산출물은 `analysis/<topic>/_evidence/week2/`에 저장한다. 이 경로는 `.gitignore`에서 예외 처리되어 추적된다.

## Slide Workflow
사용자가 "슬라이드", "발표자료", "presentation"을 명시적으로 요청했을 때만 실행한다.

1. 해당 `full.md`가 존재하는지 확인한다.
2. **slide-deck** — `design.md`를 기준으로 저널 미팅용 HTML 슬라이드를 만든다.

## QA / 검증 워크플로우
- 분석된 논문에 대한 질문 → **paper-qa**
- 특정 insight나 해석의 근거 검증 → **claim-verify**
