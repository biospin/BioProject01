# 적대적 자체검토 #2 — Genome Biology 심사자 시뮬레이션 (draft_v2.md, **2026-07-19 변경분 한정**)

> 검토자: paper-critic (BIOP01 하네스). 역할 = 투고 전 적대적 자체검토.
> **검토 범위 = 오늘 바뀐 부분만**: Results 소절 "The cell×gene velocity matrix does not reproduce across methods either"(L113–117, 외부 재현 문단 포함) · Methods "Cell-level velocity-matrix audit"(L199–201) · Discussion scope 문장(L165 말미) · Positioning의 [12,13] 채점층 서술(L169) · Background의 [12,13] 문장 2곳(L55, L57) · Additional file 12(L271). 나머지는 배경으로만 읽었다.
> 직전 critic(`REVIEW-GB-2026-07-19.md`, 09:26)의 3건(abundance 교란 / γ 역방향 method 혼입 / lag magnitude +0.163)은 해소된 것으로 보고 **중복 지적하지 않는다**.
> 근거파일: `results/velocity_matrix_audit.md` · `results/velocity_matrix_audit.json` · `results/velocity_matrix_audit_pairs.csv` · `results/velocity_matrix_audit_external.md` · `..._external.json` · `..._external_pairs.csv` · `manuscript/PREREGISTRATION_velocity_matrix.md` · `manuscript/NOTE_benchmarks_12_13_scope_check.md` · `scripts/p10b_velocity_matrix_diagnostic.py`.
> 판정 날짜: 2026-07-19. advisor 게이트 통과. **인용한 수치는 전부 위 원천 파일에서 확인한 값이며, 이 문서는 draft를 수정하지 않는다.**

---

## 판정 — **MAJOR REVISION** (변경분 한정; accept 0% / minor 15% / **major 70%** / reject 15%)

1. **골격은 방어된다.** 봉인된 NEGATIVE 판정 자체는 사전등록이 지정한 **원척도** Δ(−0.206, `velocity_matrix_audit.json:contrastA`)로 계산됐고, 외부 4/4도 원척도·중심화 두 지표에서 같은 판정이며, 인과 결론을 MultiVelo로 제한한 것·multiome 쌍이 1개뿐인 시스템을 밝힌 것·모델형태 경합설명을 스스로 적은 것은 심사자의 값싼 공격을 선제 차단한다.
2. **그럼에도 major인 첫째 이유는 지표 서술이다.** HSPC 문단의 헤드라인 숫자(+0.872 · +0.838 · +0.583 · −0.500 · +0.260/−0.004/−0.292)는 **사전등록이 보조로 내려둔 중심화 코사인**이고, 바로 다음 문단의 외부 판정은 **사전등록이 주 지표로 못박은 원척도**다. 두 문단이 서로 다른 주 지표로 돌아가는데 본문에는 라벨이 대부분 없다 — 본문만 읽는 심사자는 어느 숫자가 어느 자인지 알 수 없고, 사전등록 준수 여부도 검증할 수 없다.
3. **둘째 이유는 대조군의 비대칭이다.** 재현성 천장(MultiVelo, 세포 재표본 재적합)은 MultiVelo 한 arm에만 있고, ATAC-shuffle 대조는 그 천장과 **다른 종류의 섭동**을 잰 값과 비교된다. 이 두 대조로부터 "cross-method 값은 측정 잡음이 아니라 실제 불일치"·"크로마틴 기여는 run-to-run 변동 안"이라는 **무조건 진술 두 개**가 나오는데, 근거는 조건부다. reject가 아닌 이유: 세 문제 전부 서술·라벨·한계 문장으로 교정 가능하며 supporting 등급 결론(NEGATIVE·REPLICATED)은 원척도 위에서 그대로 선다.

---

## CRITICAL — 주장/규율을 직접 위협하는 항목

### CRITICAL-1. 한 소절 안에서 주 지표가 바뀌는데 라벨이 없다 — 사전등록이 보조로 내린 지표가 HSPC 헤드라인을 차지했다

- **인용(draft L115)**: "per-cell cosine similarity between methods sat at or below a cell-shuffled null for every multiome pair (**excess −0.263 to +0.003**) … refitting MultiVelo on resampled cells reproduces its own matrix at **mean-centred cosine +0.872** … shuffling ATAC gene labels moved the MultiVelo matrix no further than refitting it did (**+0.838**, inside the refit range) … The strongest agreement anywhere in the comparison was between MultiVelo and the RNA-only scVelo floor (**+0.583**) … the corresponding values for CRAK-Velo, MoFlow and MultiVeloVAE were **+0.260, −0.004 and −0.292** … assigned systematically opposite directions to the same cells (**−0.500**)."
- **인용(draft L117)**: "paired per-cell Δ = **−0.159, −0.152, −0.289 and −0.184** … in gastrulation, MultiVelo and MultiVeloVAE do share cell-level signal above the shuffled null (**+0.200 versus +0.038**) … Across all five systems the strongest agreeing pair was MultiVelo with the RNA-only floor (**mean-centred** +0.583, +0.432, +0.578, +0.392, +0.283)."
- **인용(draft Methods L201)**: "Agreement was the per-cell cosine similarity across genes, reported against a cell-shuffled null … Because raw cosine is partly determined by a direction common to all cells …, **we also report the mean-centred cosine**."
- **왜 문제**:
  1. **사전등록과의 관계.** `PREREGISTRATION_velocity_matrix.md:41`(§2-4)는 "**주 분석은 원척도 코사인** … 민감도 분석으로 **유전자별 SD로 나눈(중심화 없음) 스케일 코사인**을 함께 보고"로 주 지표와 민감도 지표를 둘 다 못박았다. **평균 벡터 제거(mean-centring)는 이 목록에 없다** — 사전등록에 없는 사후 진단이고, 근거파일이 그렇게 부른다(`velocity_matrix_audit.md` §3 "사후 진단 … 판정을 바꾸지 않는다"). 외부편은 이 이탈을 자체 발견해 원척도로 되돌렸다(`velocity_matrix_audit_external.md:25` "규약 이탈 기록(자체 발견·정정)"). **그런데 본문 HSPC 문단은 정정 전 지표로 서술돼 있다.** (오해 방지: 같은 §2-4가 금지한 것은 **z-score**이고 그 이유는 "중심화하면 부호가 사라지므로"인데, draft의 mean-centring은 스케일 없이 평균 벡터만 빼서 부호를 보존한다(Methods L201). **z-score 금지 조항을 어긴 것은 아니다** — 문제는 주 지표 목록에 없는 지표가 헤드라인을 차지했고 그 사실이 어디에도 기재되지 않았다는 것이다.)
  2. **문단 간 불일치.** L115의 "excess −0.263 to +0.003"은 원척도, 같은 문장군의 +0.583/−0.500/−0.292는 중심화다. L117은 원척도 Δ와 원척도 +0.200/+0.038을 쓴 뒤 같은 문장 끝에서 중심화 +0.583으로 돌아온다. **동일한 +0.583이 L115에서는 무라벨, L117에서는 "mean-centred"로 등장**한다 — 심사자가 두 문단을 대조하면 곧바로 잡는다.
  3. **Methods가 주 지표를 지정하지 않는다.** "we also report the mean-centred cosine"은 원척도가 주 지표라는 함의만 줄 뿐, 사전등록 §2-4를 인용하지도, 외부편의 규약 이탈·정정을 기록하지도 않는다. 벤치마크 논문에서 "어느 자가 판정자인가"를 Methods가 안 정하면 재현 불가다.
- **어떻게 고칠지**: 어느 지표가 이기느냐는 저자의 선택이다 — **중심화가 더 나은 자일 수 있다**(draft 스스로 Methods L201에서 원척도가 평균 벡터에 12.9–37.4%까지 지배된다고 적었고, 그게 이 진단이 존재하는 이유다). 고쳐야 할 것은 **불일치와 미기재**다. (i) **주 지표를 하나로 정하고 HSPC와 외부 문단에 똑같이 적용**하라(현재는 문단마다 다르다). (ii) 변경 소절의 **모든 코사인 값에 raw / mean-centred 라벨을 예외 없이** 붙이고, 보조 지표는 괄호 병기(예: "raw +0.242, mean-centred +0.583")로 함께 보여라. (iii) Methods에 한 문장 추가 — 사전등록 §2-4의 주 지표는 원척도(민감도는 SD-스케일)였고 mean-centring은 사후 진단으로 도입됐으며, **두 지표가 HSPC와 외부 4/4에서 같은 판정을 준다**는 점, 그리고 외부 재현의 최초 실행이 중심화를 주 판정에 썼다가 **자체 발견해 원척도로 재판정**했다는 점. (iv) 판정 자체가 원척도로 계산됐다는 점(`contrastA` Δ=−0.206, 외부 `paired_delta_raw`)을 명시하면 이 지적은 "제시 방식+미기재" 문제로 축소되고 오히려 **규율 자산**이 된다 — 지금 서술은 그 자산을 스스로 버리고 있다.

---

## MAJOR — accept/minor를 막는 항목

### MAJOR-1. "실제 불일치이지 측정 잡음이 아니다"가 무조건문인데, **양쪽 끝에서 각각 다른 이유로** 방어되지 않는다 (공격지점 a)

- **인용(draft L115)**: "First, a reproducibility ceiling: refitting MultiVelo on resampled cells reproduces its own matrix at mean-centred cosine +0.872 (six refits, range +0.826 to +0.887; sign agreement 78.6%), so the measure detects agreement where agreement exists, and **the cross-method values are genuine disagreement rather than measurement noise.**"
- **왜 문제**: cross-method 값은 한 덩어리가 아니라 **0 근처 쌍**과 **뚜렷한 음수 쌍**으로 갈리는데, 인용 문장은 둘을 한 단정으로 묶는다. 두 끝이 각각 다른 이유로 새어 나간다.
  - **① 0 근처 쌍 — 잡음과 분리되지 않는다(진짜 공백).** 두 arm의 코사인은 **두 arm 각각의 자기 재현성에 위에서 눌린다.** 천장은 MultiVelo 한 arm에만 측정됐고(`velocity_matrix_audit.md` §4), MoFlow·CRAK-Velo·MultiVeloVAE에는 same-config 재실행 대조가 **없다.** 0 근처인 세 쌍(MV×MoFlow −0.012, MoFlow×CRAK +0.003, MoFlow×VAE +0.003)은 **전부 MoFlow가 걸린 쌍**이고, 이 값이 "method 간 실제 불일치"인지 "MoFlow 한 arm의 내부 불안정"인지 이 설계로는 구분되지 않는다. **MultiVelo에 천장이 있어도 소용없다** — 병목은 상대 arm이기 때문이다. draft가 가진 유일한 관련 수치(MoFlow 원본×셔플 +0.113)는 **draft 스스로 "run-to-run 변동과 분리 불가"라고 적은 값**이므로 이 공백을 메울 수 없다. 즉 MoFlow가 불안정하다는 것도, 안정하다는 것도 **미확립**이다.
  - **② 뚜렷한 음수 쌍 — 잡음은 아니지만 "실제 불일치"도 미확정.** MultiVelo×MultiVeloVAE −0.500, CRAK×VAE −0.530은 **잡음으로 설명될 수 없다**(잡음은 코사인을 0 쪽으로 끌지, 체계적 반대 정렬을 만들지 않는다) — 이 끝에서는 draft의 단정이 오히려 안전하다. 다만 근거파일 §6이 남긴 유보가 본문에서 사라졌다: "MultiVelo↔MultiVeloVAE의 체계적 반대 정렬이 **진짜 불일치인지 문서화되지 않은 부호·모수화 규약 차이인지는 이 감사로 구분되지 않는다**." 즉 이 끝의 대안 설명은 잡음이 아니라 **규약 아티팩트**이고, 그 유보가 carried-limitation으로 유실됐다.
  - draft는 천장의 제한을 **인과 읽기에만** 걸어 두었고("We confine the causal reading to MultiVelo"), **불일치 읽기에는 걸지 않았다.**
- **어떻게 고칠지**: 한 단정을 **값의 부호에 따라 둘로 쪼개라** — "the ceiling shows the measure detects agreement where it exists. **The systematically anti-aligned pairs (−0.500, −0.530) cannot be measurement noise**, though we cannot exclude an undocumented sign or parametrization convention difference; **the near-zero pairs, all of which involve MoFlow, are not separable from that arm's own run-to-run variability**, since no same-configuration rerun exists for any arm but MultiVelo." 그리고 (i) 한계에 "재현성 천장은 5개 arm 중 1개에만 측정됐다"를, (ii) 근거파일 §6의 **부호·모수화 규약 유보 문장을 본문으로 반입**하라. (가장 값싼 실질 보강: MoFlow·VAE의 same-seed 재실행 2회씩만 추가하면 ①이 통째로 사라진다.)

### MAJOR-2. 재현성 천장과 ATAC-shuffle 대조가 **서로 다른 섭동**을 잰 값인데 직접 비교된다 — 인과 결론이 느슨한 자에 기대고 있다

- **인용(draft L115)**: "Second, the same causal control we applied to the lag: shuffling ATAC gene labels **moved the MultiVelo matrix no further than refitting it did** (+0.838, inside the refit range), placing **chromatin's contribution to the matrix within run-to-run variation**."
- **왜 문제**: 두 값의 섭동이 다르다. `scripts/p10b_velocity_matrix_diagnostic.py` [E]는 천장을 **세포 재표본(bootstrap refit, 15,315 cells)** 대비로 재고, [D]의 ATAC-shuffle은 **전량 세포에서 ATAC만 파괴한** 적합과의 비교다. 세포 재표본은 코사인을 **오직 떨어뜨리는 방향**으로만 작용하므로 +0.872는 same-data 재현성의 **하한**이다. 하한을 "잡음 바닥"으로 삼아 +0.838을 "잡음 안"이라고 읽으면 **크로마틴 무력 결론 쪽으로 체계적으로 편향**된다. 게다가 draft는 "run-to-run variation"이라고 쓰는데, 측정된 것은 run-to-run(같은 데이터 재실행)이 아니라 **cell-resample-to-cell-resample** 변동이다 — 용어가 실제 대조를 잘못 지칭한다.
- **어떻게 고칠지**: (i) 최소 교정 — "run-to-run variation"을 "**cell-resampling variation**"으로 바꾸고, 재표본 천장이 same-data 재현성의 **하한**이라는 점을 한 절로 명시하라. (ii) 제대로 된 교정 — **짝맞춘 대조**를 하나 돌려라: 같은 재표본 세포에서 ATAC 온전/셔플 두 적합을 비교(또는 전량 세포에서 same-config 재적합). 그러면 +0.838이 정말 잡음 범위인지 답이 나온다. 이 대조 없이는 "chromatin's contribution … within run-to-run variation"은 **비교 불가능한 두 자의 비교**다. (iii) 최소한 이 비대칭을 §한계에 적어라 — 근거파일 §6에도 없다.

### MAJOR-3. 층③으로의 확장이 [12]에서 **빌려온 증거**인데, [12]는 크로마틴이 아예 없다 (Discussion scope 문장)

- **인용(draft L165)**: "We note only that **the disagreement we measure does not appear to be repaired further up the stack**: those benchmarks report low cross-method agreement of transition vectors as well (A1<0.3) [12], so **neighbourhood smoothing does not restore quantitative agreement**, even where coarse streamlines may still look qualitatively similar."
- **왜 문제**: `NOTE_benchmarks_12_13_scope_check.md`가 직접 확인한 바로 **[12]는 ATAC이 없고 MultiVelo를 `rna_only=True`로 돌렸다 — multiome velocity는 평가되지 않았다.** 그리고 [12]의 A1<0.3은 우리 4개 arm과 대부분 겹치지 않는 **12개 RNA-only method**에 대한 값이다. 따라서 [12]는 "**우리가 잰 multiome 행렬 불일치**가 임베딩에서 회복되지 않는다"를 보일 수 없다. 다른 modality·다른 method 집합의 결과를 우리 결과의 상위층 운명에 대한 증거로 전용한 것이다. 게다가 바로 앞 문장 "Nothing here shows that trajectory inference is unreliable"과 이 문장이 수사적으로 서로를 잡아먹는다.
- **어떻게 고칠지**: 귀속을 정확히 하라 — "in RNA-only settings, where a comparable benchmark exists, cross-method agreement is also low at the transition-vector level (A1<0.3 across twelve methods) [12]; **whether the multiome disagreement we measure survives projection has not been tested by us or by [12], which ran without paired chromatin (MultiVelo in RNA-only mode)**." 즉 "회복되지 않는다"는 **단정을 빼고**, 층③이 미검정임을 그대로 남겨라. `velocity_matrix_audit.md` §6도 이 확장을 "층③의 정량 감사는 여전히 별도 측정 대상"으로 닫아 두었다 — 본문이 근거파일보다 한 발 더 나갔다.

### MAJOR-4. Background L55와 Positioning L169가 [13]에 대해 서로 모순된다

- **인용(draft L55)**: "Two 2026 benchmarks establish that velocity direction is method-dependent with no universal winner [12,13] — but **both score the velocity *vector* in a low-dimensional embedding rather than the individual per-gene outputs or the cell×gene velocity matrix** that precedes the projection."
- **인용(draft L169)**: "Neither compares different methods' cell×gene velocity matrices to each other, and neither applies a causal chromatin control; **[13] uses the matrix only to quantify a single method's run-to-run stability across random seeds.**"
- **왜 문제**: L55는 [13]이 행렬을 안 쓴다고 읽히고, L169는 [13]이 행렬을 쓴다(단 method 내부에서만)고 적는다. `NOTE_..._scope_check.md`가 확인한 사실은 L169 쪽이다. 심사자는 두 페이지 사이의 자기모순을 반드시 지적하고, 그 순간 [12,13] 서술 전체의 신뢰도가 내려간다. L169의 표현이 더 정확하므로 L55를 고치는 것이 맞다.
- **어떻게 고칠지**: L55를 "— but both judge the velocity *vector* in a low-dimensional embedding, and **neither compares the cell×gene velocity matrix across methods** ([13] uses that matrix only for one method's seed-to-seed stability)"로 정정하라. 같은 문장의 "neither applies a permutation-null concordance test, a causal negative control, or an external measurement anchor"도 **"to our knowledge"** 또는 NOTE 인용으로 한정하라 — 두 편만 읽고 내린 전면 부정문이다(직전 리뷰가 지적한 문헌-부정-단정과 같은 종이지만, **이건 새로 추가된 문장이므로 별건이다**).

### MAJOR-5. 부호 일치율 49.7–58.3%에 **null이 없다** — 그리고 그 null이 50%가 아님을 근거파일은 알고 있다

- **인용(draft L115)**: "…and **per-(cell,gene) sign agreement was 49.7–58.3%**."
- **왜 문제**: (i) 코사인에는 세포 짝 셔플 null을 붙였는데 **부호 일치율에는 어떤 null도 붙지 않았다.** (ii) draft 스스로 Methods L201에서 "the mean vector accounts for **12.9–37.4%** of squared row norm"이라 적었는데, 이는 유전자별 평균 부호가 method 간에 공유되기만 하면 부호 일치율이 **구조적으로 50%를 넘는다**는 뜻이다. 근거파일 `velocity_matrix_audit.md:66`이 정확히 그렇게 해석한다 — "부호 일치율 64.3%도 세포 수준 일치가 아니라 **유전자별 평균 부호의 공유**를 재고 있다." 본문은 이 해석을 옮기지 않은 채 49.7–58.3%를 우연 수준의 증거로 제시한다. (iii) n이 수백만이므로 58.3%는 50%와 **압도적으로 유의**하다 — "우연 수준"이라는 함의는 검정으로 방어되지 않는다. (iv) 배제된 항목이 대량이다: MultiVelo×MoFlow는 2,363,745 / 7,744,812 = **약 31%가 "방향 미정"으로 제외**됐고(`velocity_matrix_audit_pairs.csv`), gastrulation MultiVelo×MoFlow는 3,235,906 / 9,129,813 = **35%**다(`..._external_pairs.csv`). Methods는 배제 규약만 말하고 **배제 비율을 보고하지 않는다** — lag 절에서는 배제 개수를 매 비교마다 보고했던 것과 대비된다.
- **어떻게 고칠지**: (i) 부호 일치율에 셔플 null(또는 유전자 평균부호만 남긴 baseline)을 붙이거나, 붙일 수 없으면 **"이 지표의 무정보 기준선은 50%가 아니다"**를 본문에 명시하라. (ii) 제외 비율(최대 ~35%)을 Methods나 Additional file 12에 보고하라. (iii) 그게 부담이면 부호 일치율을 헤드라인에서 빼고 Additional file로 내려라 — 결론은 코사인과 천장만으로 선다.

### MAJOR-6. 사전등록된 **측정축 (2)와 그 필수 null(유전자 셔플)이 실행·보고에서 사라졌다** (공격지점 e의 실질)

- **인용(사전등록 §3)**: "**(2) 유전자별 코사인**(세포 축, 유전자마다 1개) … ### 필수 null — **이게 없으면 숫자가 부풀려 읽힌다** … **유전자 셔플**: (2)의 대응 null."
- **인용(draft L271, Additional file 12)**: "Cell-level velocity-matrix audit — **per-cell and per-gene cosine similarity for every method pair with its cell-shuffled null**, mean-centred values, per-(cell,gene) sign agreement … **plus the same pair table** and the paired baseline contrast for the four external systems."
- **왜 문제**: 확인 결과 — HSPC pairs 파일에는 `gene_cos_median`·`gene_cos_frac_pos`가 있으나 **`gene_cos_null`(유전자 셔플 null) 열이 없고**, 스크립트에도 유전자 셔플이 구현돼 있지 않다(`grep gene_shuffle|gene_cos_null` → 0 hit). 즉 사전등록이 "**없으면 숫자가 부풀려 읽힌다**"고 명시한 필수 null 하나가 실행되지 않았고, 결과파일·본문 어디에도 그 사실이 기록되지 않았다. 또한 **외부 pairs 파일에는 `gene_cos_*` 열도 SD-스케일 열(`cell_cos_median_sdscaled`, 사전등록 §2-4의 민감도 분석)도 아예 없다** — 그런데 캡션은 "the same pair table"이라고 말한다. 캡션이 산출물보다 넓다. (부수적으로 유전자별 코사인은 본문·결과 md 어디에서도 서술되지 않는다.)
- **어떻게 고칠지**: 셋 중 하나 — (i) 유전자 셔플 null을 실제로 돌려 채운다(가장 싸다), (ii) Methods에 "사전등록한 유전자 축과 그 null은 실행하지 않았으며 본 감사의 결론은 세포 축과 부호 축에만 근거한다"고 **이탈을 명시**한다, (iii) Additional file 12 캡션에서 per-gene cosine과 "the same pair table"을 **실제 산출물과 일치하도록** 축소한다(외부 표에는 유전자 축·SD-스케일 열이 없음을 명시). **어느 경우에도 캡션이 없는 데이터를 약속해서는 안 된다** — 심사자가 부록을 열면 즉시 드러난다.

---

## MINOR — 판정을 막지는 않으나 심사자가 지적할 항목

### MINOR-1. 소절 제목 "does not reproduce across methods **either**"가 본문 숫자보다 세다
draft 자신이 같은 소절에서 MultiVelo×scVelo +0.583(=+0.320 raw excess)와 gastrulation MultiVelo×MultiVeloVAE "above the shuffled null (+0.200 versus +0.038)"를 보고한다. "does not reproduce"는 전칭이고 데이터는 "multiome 쌍 사이에서는 재현되지 않는다(그리고 gastrulation은 부분 예외)"다. → 제목을 "**Multiome methods' cell×gene velocity matrices do not agree above an RNA-only baseline**" 정도로 정확히 하라. 층①의 서사 대구("either")를 위해 층② 문장을 강하게 쓰는 것은 값싼 실점이다.

### MINOR-2. "both preregistered contrasts failed … **so** the per-gene conclusion extends to the matrix" — 봉인 규칙이 결론을 정의로 부여한다
- **인용(L115)**: "…and both preregistered contrasts failed (Additional file 12), **so the per-gene conclusion extends to the matrix.**"
- 사전등록 §5는 NEGATIVE를 "층①의 결론이 층②로 확장된다"로 **정의**했다. 따라서 "두 대조가 실패했으므로 확장된다"는 추론이 아니라 **동어반복**이다. 실제로 확장을 지지하는 증거는 대조 실패가 아니라 **천장 대비 cross-method 값과 부호 일치율**이다. 심사자는 "부재의 증거를 봉인 규칙으로 존재의 결론으로 바꿨다"고 읽을 수 있다. → "the two sealed contrasts failed, and the ceiling-referenced cross-method values (…) are what carries the extension"처럼 **증거와 판정 라벨을 분리**하라.

### MINOR-3. "다섯 시스템"의 최상위 쌍 진술은 시스템마다 **후보 수가 다르다** (공격지점 c)
- **인용(L117)**: "**Across all five systems** the strongest agreeing pair was MultiVelo with the RNA-only floor (mean-centred +0.583, +0.432, +0.578, +0.392, +0.283)."
- draft는 이미 "three of the four external systems have a single multiome pair"를 밝혀 두었다(정직). 남는 빈틈은 **이 진술의 기저율**이다: HSPC는 10쌍 중 1위, gastrulation은 6쌍 중 1위지만 macrophage·BMMC·E18은 **3쌍 중 1위**다(무정보 기준선 1/3). "5/5로 반복"이 주는 인상은 실제 통계적 무게보다 크다. → 기존 공개 문장에 한 절만 덧붙여라 — "in the three systems with two multiome arms this is the strongest of only three possible pairs." 과대표현이라기보다 **기저율 미공개**이므로 MINOR.

### MINOR-4. MultiVelo×scVelo 관찰을 실을 자격은 있으나, **보여주는 숫자가 선택적**이다 (공격지점 b·d의 교차점)
- **인용(L115)**: "…though this is not a family property, since the corresponding values for CRAK-Velo, MoFlow and MultiVeloVAE were **+0.260, −0.004 and −0.292**…"
- "family property가 아니다"라는 결론 자체는 **두 지표 모두에서 산다**(원척도 excess: MultiVelo +0.320 vs CRAK +0.020 / MoFlow −0.003 / VAE +0.055 — MultiVelo가 여전히 압도). 문제는 draft가 **가장 극적인 중심화 −0.292만 보여주고 같은 쌍의 원척도 +0.055는 감춘다**는 점이다. MultiVeloVAE×scVelo는 원척도 +0.271 → 중심화 −0.292로 **부호가 뒤집히는 쌍**이고, 근거파일 §3이 그 이유(평균 벡터 정렬)를 설명해 두었다. 본문만 읽는 독자는 이 쌍이 지표에 따라 뒤집힌다는 걸 알 수 없다. → 두 값을 병기하고(§CRITICAL-1의 라벨 규칙에 흡수), 부호 반전 쌍은 각주 한 줄로 밝혀라.
- **경합 설명(모델 형태 공유)에 대한 판단**: draft가 스스로 인정하고 승격하지 않으므로 **싣는 것은 정당하다.** 다만 "해석할 수 없다"고 말하는 관찰을 두 문단에서 다섯 숫자로 강조하는 것은 분량 배분이 어긋난다 — **한 문장으로 압축**하고 5-시스템 표는 Additional file 12로 내리는 편이 심사자에게 낫다. (덧붙여, 미언급 제3의 설명이 있다: MultiVelo·CRAK-Velo는 scVelo의 전처리·moment 계산 위에 구축된 파생 구현이라 **공유 소프트웨어 계보**도 후보다. "RNA 정보 vs 모델 형태" 이분법에 이 세 번째를 한 절로 추가하면 오히려 방어가 단단해진다.)

### MINOR-5. 외부 재현의 **규약 이탈 자체발견·정정이 본문에 없다** (공격지점 e의 잔여)
`velocity_matrix_audit_external.md:25`는 최초 실행이 중심화를 주 판정에 썼다가 봉인 규약대로 원척도로 되돌린 사실과 "바뀌었더라도 원척도를 따랐을 것"을 기록했다. **이것은 자산인데 본문에 없다.** 자기에게 유리한 정정을 결과파일에만 남기면, 심사자가 부록에서 발견했을 때 "숨겼다"로 읽힐 수 있다. → Methods 한 문장으로 반입하라. (사전등록 순서 자체 — 외부 부록을 HSPC 결과를 본 뒤 봉인한 것 — 는 **부록이 그 사실을 스스로 명시했고**(`PREREGISTRATION_velocity_matrix.md:90`) 외부 데이터를 열기 전에 봉인했으므로 치명적이지 않다. 남는 실질 약점은 **재현 검정할 종점을 HSPC를 본 뒤 골랐다**는 점이다: 더 강한 HSPC 소견("모든 multiome 쌍이 null 이하")이 아니라 더 약한 순서 소견(Δ)을 종점으로 삼았고, draft의 "Third" 한계가 실제로 강한 쪽은 재현되지 않았음을 인정한다. 이미 공개돼 있으므로 MINOR이나, "the external endpoint was the ordering, chosen as the transferable form of the HSPC result"처럼 **종점 선택이 사후였음**을 한 절로 밝히면 완전해진다.)

### MINOR-6. Methods 소절이 **외부 재현 절차를 담지 않는다**
"Cell-level velocity-matrix audit"(L199–201)은 HSPC 절차만 기술한다. 외부 4개 시스템의 Δ 정의, paired 부트스트랩(B=1,000, seed 20260719), **3-of-4 사전등록 임계**, 시스템별 사용 유전자 수(847/702/232/973, `..._external.json`)가 Methods에 없고 Results 괄호에만 흩어져 있다. 벤치마크 논문의 Methods로는 재현 불가 수준이다. → 외부 재현을 Methods에 2–3문장으로 분리 기술하라.

### MINOR-7. 천장·셔플 대조의 **유전자·세포 집합이 본 비교와 다르다**는 점이 미기재
`p10b` [E]는 refit에 존재하는 세포(≈15,315)·유전자로만 천장을 계산하고, [D]의 셔플 비교도 셔플 arm에 있는 유전자로 제한한다(MoFlow n=353). 본 cross-method 비교는 21,878 cells × 354 genes다. 결론을 바꿀 크기는 아니지만, 세 숫자(+0.872 / +0.838 / cross-method)가 **같은 자 위에서 잰 값이 아니라는 점**은 Methods에 한 절로 적어야 한다(MAJOR-2와 함께 고치면 한 문장으로 끝난다).

### MINOR-8. 신규성 부정문이 **두 편만 읽고** 내려졌다
- **인용(L169)**: "**To our knowledge** the matrix-level cross-method comparison, the ATAC-shuffle control applied to it, and **the use of a refit reproducibility ceiling as the interpretive baseline are absent from prior velocity benchmarks.**"
- "to our knowledge"가 있어 방어는 되지만, 근거는 [12,13] 두 편 정독뿐이다. 특히 세 번째 항목("재적합 천장을 해석 기준자로 사용")은 [13]의 seed 안정성과 **계산량이 사실상 같고 용도만 다르다** — 심사자는 "용도 차이를 신규성으로 파는가"로 읽을 수 있다. → 세 번째 항목은 신규성 목록에서 빼고 **"we use it as the interpretive baseline rather than as a quality score, following [13]'s stability measure"**처럼 선행연구에 붙여 쓰는 편이 강하다. 앞의 두 항목(행렬 수준 cross-method 비교 · ATAC-shuffle 인과 대조)은 NOTE의 확인으로 충분히 방어된다.

---

## 방어되는 것 — 공격했으나 근거가 버틴 지점

심사 신뢰도의 자산이므로 그대로 유지할 것.

1. **봉인된 판정이 사전등록 지표 위에서 선다.** 주 판정 Δ는 원척도로 계산됐고(`velocity_matrix_audit.json:contrastA` Δ=−0.206 [−0.207, −0.205]), 외부 4/4도 `paired_delta_raw` 기준이며 중심화에서도 4/4다(`..._external.json`의 `replicated_raw`·`replicated_centered` 모두 true). **CRITICAL-1은 서술·라벨 문제이지 판정 문제가 아니다** — 결론은 지표 선택에 의존하지 않는다.
2. **인과 결론의 범위 제한이 정확하다.** "We confine the causal reading to MultiVelo, the only arm with a refit control; MoFlow is a stochastic deep model whose original-versus-shuffled value (+0.113) cannot be separated from run-to-run variation" — 근거파일 §6과 정확히 일치하고, 외부에 scrambled arm이 없다는 제약도 본문에 그대로 옮겨졌다("the causal statement remains specific to HSPC and to MultiVelo"). 사전등록 §D가 **미리** 못박은 그대로다.
3. **재현되지 않은 것을 재현됐다고 쓰지 않았다.** "Third, what replicates is the ordering and not the stronger HSPC observation that every multiome pair sits at or below its null — in gastrulation, MultiVelo and MultiVeloVAE do share cell-level signal above the shuffled null (+0.200 versus +0.038)". 실제 CSV 값(raw 0.1998 / null 0.0378)과 일치하고, **자기 서사에 불리한 예외를 본문 한가운데에 적었다.** 감점이 아니라 가점 지점이다.
4. **경합 설명을 숨기지 않았다.** 모델 형태 공유("both are classical βu − γs residuals on the same smoothed counts")를 본문에서 스스로 제기하고 "this design cannot separate"로 닫으며, "RNA 성분이 재현된다"는 해석을 **승격하지 않는다.** 공격지점 (b)의 핵심 — 싣는 것 자체가 부당한가 — 에 대한 답은 **아니오**다. 분량만 줄이면 된다(MINOR-4).
5. **RNA-only 최상위가 계열 성질이 아님을 스스로 적었다.** "though this is not a family property, since the corresponding values … were +0.260, −0.004 and −0.292" — 원척도로 봐도 같은 결론이며(§MINOR-4), 근거파일 §5-3의 등급("MultiVelo 사례까지만")을 본문이 낮추지 않고 지켰다.
6. **헤드라인 승격이 없다.** 소절은 supporting으로 남고 Abstract·Table 2·동결 주장 5개를 건드리지 않았다 — `PAPER_DIRECTION.md` §5(2026-07-19) 편입 정책과 Prereg §6을 지켰다. **층② 결과로 결정지도를 재작성하지 않은 것**이 이 변경분에서 가장 규율 있는 선택이다.
7. **[12,13] 선결 게이트를 실제로 통과시켰다.** `NOTE_benchmarks_12_13_scope_check.md`는 두 편의 전문을 읽고 채점 층·multiome 범위·인과 대조 유무를 표로 확정했으며, Positioning L169의 서술([12]는 rna_only로 MultiVelo 실행, [13]은 multiome 1개 데이터셋·2개 method)은 그 확인과 정확히 일치한다. **draft를 고치기 전에 문헌을 확인한다는 순서 규율이 실제로 작동했다.** (MAJOR-4는 L169가 틀렸다는 뜻이 아니라 L55가 L169를 못 따라갔다는 뜻이다.)
8. **Methods가 지표의 구조적 함정을 자백한다.** "the mean vector accounts for 12.9–37.4% of squared row norm" · "centring is applied without scaling so that sign is preserved" · 세포 짝 셔플 null을 쓰는 이유("a globally shared velocity direction inflates the raw value") — 원 코사인 값을 그대로 발견으로 팔지 않겠다는 사전등록 §4의 정신이 Methods에 남아 있다.
9. **인용 수치는 전부 원천과 대조해 일치한다.** 21,878 cells / 505→354 genes / scVelo NaN 151 / excess −0.263~+0.003 / sign 49.7–58.3% / 천장 +0.872 (0.826–0.887) · 78.6% / 셔플 +0.838 · MoFlow +0.113 / 중심화 +0.583·+0.260·−0.004·−0.292·−0.500 / 외부 Δ −0.159·−0.152·−0.289·−0.184 및 4/4 / 5-시스템 최상위 +0.583·+0.432·+0.578·+0.392·+0.283 / gastrulation +0.200 vs +0.038 — **불일치 0건.** 날조 없음.

---

## 최종 판정 (한 줄)

**MAJOR REVISION (변경분 한정)** — 층②의 NEGATIVE·REPLICATED 결론은 사전등록 지표 위에서 방어되고 범위 제한·경합 설명·불리한 예외까지 정직하게 적혀 있으나, (i) HSPC 문단이 사전등록이 보조로 내린 중심화 지표를 무라벨로 헤드라인화해 이웃 문단과 주 지표가 어긋나고(CRITICAL-1), (ii) 재현성 천장이 5개 arm 중 1개에만 있는데 "실제 불일치" 단정이 무조건문이며(MAJOR-1), (iii) 그 천장과 ATAC-shuffle이 서로 다른 섭동을 잰 값끼리 비교되고(MAJOR-2), (iv) 층③ 확장이 크로마틴 없는 [12]에서 빌려온 증거에 기대며(MAJOR-3), (v) Background와 Positioning이 [13]에 대해 서로 모순되고(MAJOR-4), (vi) 부호 일치율에 null이 없고 사전등록된 유전자 축 null이 실행·기재 없이 사라졌다(MAJOR-5·6) — 여섯 건 모두 본문 서술·라벨·한계 문장과 소규모 추가 계산으로 교정 가능하므로 reject는 아니다.
