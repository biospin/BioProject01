# Lens — Academic — Martin et al., 2023 (HSPC Chromatin Dynamics)

> 근거: `martin-2023-hspc-chromatin_core.md` 및 원문 PDF. Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.

## activation lag 가설에 주는 배경 (우리 프로젝트 핵심)

`해석:` 우리 `activation lag` 가설은 *chromatin이 열린 뒤 transcription이 시작될 때까지의 시간 지연*을 정량하려는 것이다. 이 논문은 그 가설의 **방향성(접근성이 발현에 선행)을 HSPC 분화 축에서 직접 보여주는 primary 근거**다. 본문 근거를 모으면:

1. **Priming = accessibility가 expression에 선행한다는 명시적 정의** (Background, p.522). 저자는 priming을 "target gene이 발현되지 않았는데도 putative target CRE가 열려 있는 상태"로 정의한다 — 이것이 곧 *opening이 transcription을 앞서는 lead time*의 생물학적 실체다. 우리 가설의 mechanistic framing을 그대로 인용할 수 있다.
2. **HSC의 global하게 가장 열린 chromatin** (Fig 1B,C; Table 1, HSC IDR peak 70,731 / cumulative signal 최고). multipotent 상태일수록 미래 lineage CRE를 미리 열어둔다 → lineage가 확정되기 *전부터* accessibility가 존재한다는 lag의 출발 조건.
3. **lineage-primed CRE의 선택적 유지** (Fig 6C). HSC-primed peak의 25% 미만(17% MkP, 11% EP, 13% GM, 12% B, 26% T)만 분화 끝까지 accessibility 유지. `해석:` 이것은 lag 가설에 두 가지 함의가 있다 — (a) 대부분의 primed CRE는 transcription으로 *이어지지 않고 닫힌다* → "열렸으나 미발현"이 흔한 background state라는 점, (b) 발현으로 이어지는 소수 CRE는 분화 전 과정에서 *지속적으로* 열려 있다 → 이들이 lag 측정의 진짜 대상.
4. **CRISPRi로 accessibility → expression 인과 확립** (Fig 7K). CD115 enhancer를 silencing하면 발현이 떨어진다 → 열린 CRE가 (지연 후) 발현을 *유발*한다는 directional causality. 단 CD11b enhancer는 무효(Fig 7L) → 열린 CRE가 모두 기능적이지 않음 = lag 측정 시 "열림"을 무조건 "곧 발현"으로 보면 안 된다는 caveat의 근거.

`미제공:` 단, 이 논문은 paired RNA / multiome / 시간 단위 측정이 없다. accessibility와 expression이 *같은 세포에서 동시 측정*되지 않았고(expression은 외부 GEXC database), pseudotime이나 wall-clock 단위 lag을 정량하지 않는다. 따라서 **lag의 직접 정량 근거가 아니라 priming의 방향성·persistence 배경 문헌**으로 위치시키는 것이 정확하다.

### Limitations

#### 저자가 명시한 한계
- bulk ATAC-seq 기반 — population-level. single-cell intermediate state를 분해하지 못함(본문은 functionally defined population 분리로 보완 시도).
- CLP의 priming 분포가 HSC/MPP와 유의하게 다르지 않은 점(Fig 6B)을 저자 스스로 "in vivo로 구현되지 않는 inherited priming일 수 있다"고 단서를 단다(Discussion, ref 69; in vitro reignite 가능 ref 70).
- HSC priming의 대부분이 분화 중 유지되지 않음(<25%)을 "unexpected"로 인정 — priming의 기능적 의미가 보편적이지 않을 수 있음.

#### 분석자가 판단한 한계
- **부족한 점**: accessibility-expression 상관이 *같은 세포의 동시 측정*이 아니다. expression은 별도 microarray 기반 GEXC(ref 31)에서 가져왔다.
  - **왜 중요한가**: priming(열림이 발현에 선행)을 주장하려면 두 modality의 시간 정렬이 필요한데, 두 데이터셋의 cell type 정의·batch가 완전히 일치한다는 보장이 없다.
  - **어떤 증거가 부족한가**: 동일 세포의 paired RNA(multiome 또는 SHARE-seq) 또는 시간 추적(pseudotime 위 accessibility-expression 정렬).
- **부족한 점**: peak count·cumulative signal이 HSC에서 최고라는 핵심 결과가 input cell 수·library depth에 민감한 지표인데, 정규화 절차의 본문 수치 제시가 약하다(`검토필요:` "careful quality control"만 언급).
  - **왜 중요한가**: "HSC가 가장 열려 있다"는 본 논문의 중심 메시지이자 우리가 인용할 핵심. technical confound 가능성이 남으면 인용 강도를 조절해야 한다.
  - **어떤 증거가 부족한가**: cell number-matched downsampling, depth-normalized peak count, spike-in 등.
- **부족한 점**: replicate $n=2$, HSC 2 sample은 hierarchical clustering에서 유일하게 비인접(p.535).
  - **왜 중요한가**: HSC accessibility variability가 결론(가장 열림, erythroid 편향)의 robustness를 약화시킬 수 있음.

#### 설명이 매끄럽지 않은 지점
- **연결이 약한 주장**: "HSC-unique peak이 self-renewal/multipotency의 regulator"라는 framing(Fig 7 제목·Abstract).
  - **현재 근거**: HSC-unique peak이 ELF3/NF-E2/RUNX motif + "definitive erythrocyte differentiation" GO에 enrich(Fig 7C,D).
  - **더 필요한 근거**: GO·motif는 *erythropoiesis*에 치우치는데(저자도 인정), self-renewal/multipotency로의 도약은 약하다. self-renewal marker(예: HSC reconstitution assay)와의 직접 연결이 없다. `해석:` 결과는 "HSC-unique peak = erythroid-primed"에 가깝고 self-renewal 주장은 약하게 받쳐진다.
- **causal claim vs association**: Fig 1~6은 모두 association. 인과는 Fig 7 CRISPRi 3개 locus(CD81/CD115/CD11b)에만 있다. genome-wide priming 주장의 인과 검증은 3개 sample에 불과 — generalization은 제한적.

#### 정리되지 않은 질문
- `질문:` primed되었으나 닫히는 75%+ CRE와 유지되는 <25% CRE를 구분하는 sequence/TF 결정 요인은 무엇인가? (본 논문은 분포만 보고 결정 요인을 모델링하지 않음)
- `질문:` CD11b enhancer가 무효였던 이유(Fig 7L)는 잘못된 CRE annotation인가, redundancy인가, 아니면 분화 stage 의존성인가? CRE annotation의 false-positive rate를 어떻게 추정하나?

### Citation 후보 (본인 논문·제안서·학회 발표용)

#### 인용 가능 문장
- §Background(p.522): "open cis-regulatory elements exclusively shared between HSCs and unipotent lineage cells were enriched for DNA binding motifs of known lineage-specific transcription factors" (priming의 motif 근거)
  - 사용 시나리오: 우리 introduction에서 *chromatin priming이 lineage TF 활동에 선행한다*는 선행 근거로 인용.
  - BibTeX key: `@martin2023hspcchromatin`
- §Background(p.522): priming = "chromatin accessibility of a putative CRE despite lack of expression of its presumed target gene"
  - 사용 시나리오: activation lag의 mechanistic 정의 문장으로 직접 차용.
  - BibTeX key: `@martin2023hspcchromatin`
- §Results/Discussion: HSC-primed peak의 "no lineage had more than 25% of the HSC-primed peaks maintain openness throughout differentiation"
  - 사용 시나리오: "열린 CRE 대부분은 발현으로 이어지지 않는다"는 우리 lag 모델의 background 통계로 인용.
  - BibTeX key: `@martin2023hspcchromatin`

#### 인용 가능 수치
- HSC ATAC IDR peak 70,731 (master peak-list 92,842) — Table 1
  - 사용 시나리오: HSC의 global open chromatin baseline 수치.
  - BibTeX key: `@martin2023hspcchromatin`
- HSC-unique peak 3,026개 중 92.7%(2,805)가 non-promoter — Fig 7B
  - 사용 시나리오: stem cell priming이 distal CRE 중심이라는 근거.
  - BibTeX key: `@martin2023hspcchromatin`
- lineage별 priming 유지율 17%(MkP)/11%(EP)/13%(GM)/12%(B)/26%(T) — Fig 6C
  - 사용 시나리오: priming persistence가 lineage마다 다르다는 정량 근거.
  - BibTeX key: `@martin2023hspcchromatin`

#### 인용 가능 Figure/Table
- Figure 1A — hematopoiesis 계통도(13 cell type)
  - HSC→progenitor→mature의 분화 trajectory + 측정 cell type
  - 사용 시나리오: 우리 발표에서 HSPC 분화 축 도식의 reference.
  - BibTeX key: `@martin2023hspcchromatin`
- Figure 6C — HSC-primed peak의 trajectory별 유지 heatmap
  - priming이 대부분 닫히고 소수만 유지됨을 시각화
  - 사용 시나리오: "열렸으나 미발현 → 닫힘" background state를 보여줄 때.
  - BibTeX key: `@martin2023hspcchromatin`

## Final Takeaways
- **이 논문의 가장 큰 의미**: HSPC 분화에서 chromatin priming(접근성이 발현·계통확정에 선행)을 13 cell type ATAC-seq로 trajectory 전체에서 정량하고, CRISPRi로 distal CRE의 functional necessity까지 연결한 primary 근거. 우리 activation lag 가설의 *방향성 배경*으로 직접 인용 가능.
- **다음 논문으로 이어질 아이디어**: 같은 HSPC 분화 축에서 *paired RNA + ATAC(10x Multiome 또는 SHARE-seq)*로 동일 세포의 accessibility-expression을 동시 측정해, primed CRE가 발현으로 전환되기까지의 lag을 pseudotime 단위로 정량. 본 논문은 그 직전 단계(accessibility-only)에 멈춰 있다.
- **설명을 더 매끄럽게 만들 방법**: cell number-matched downsampling으로 "HSC가 가장 열림"의 technical robustness를 보강하고, primed-but-not-maintained CRE와 maintained CRE를 가르는 sequence/TF feature를 모델링.
- **우선순위가 높은 후속 실험 / 분석**:
  1. (우리) 이 논문 mouse HSC-unique/primed CRE 좌표를 우리 Human HSPC 10x Multiome(GSE209878)로 liftover해 ortholog 수준 overlap 확인 → baseline primed-CRE feature 정의.
  2. (우리) 우리 multiome에서 "열렸으나 미발현" CRE의 비율을 lineage별로 추정해, 본 논문의 <25% 유지 통계와 비교.
