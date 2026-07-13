# Week 7(박상준 원설계) 대비 설계 갭 심층검토 — 미커밋·팀 논의용

> 출처: Confluence [Week 7] 스터디내용(p.23953412, 작성 이건규, Day 3 = 박상준 BIOP01 velocity-lag 원설계).
> 목적: 박상준 원설계 중 **아직 안 했고 디자인에 참고할 만한 것** 심층검토. BIOP01은 박상준 최초 기획·팀 프로젝트 → 이 문서는 **권고**이지 PAPER-PLAN 재구조화가 아님(팀 합의 후 반영).
> 작성 근거: 이 폴더 `PAPER-PLAN.md`/`DESIGN.md`와 레포 grep 대조, GSE70677 GEO 메타 검증(2026-07-12).

## 0. 한 줄 결론
**박상준 원설계의 뼈대는 이미 PAPER-PLAN에 흡수됐다**(Step1 lag측정=Part1, Step3 lag→drug=Part2). 새로 크게 없다. 단, **우리 중심 발견(α 재현·lag 비재현)이 원설계보다 나중**이라, 원설계를 그 렌즈로 다시 읽으면 **실행 가능한 델타 1개(헤드라인)+조건부 1개**가 남는다.

## 1. 박상준 Week 7 원설계 요약
- **가설:** baseline 후성유전 상태(promoter/enhancer accessibility, H3K27ac/me3, H3K4me3, TF occupancy, regulatory architecture)가 gene별 **activation lag**(chromatin open→transcription onset)과 **shutdown lag**(transcription off→chromatin close)를 결정 → gene별 lag structure로 perturbation/epigenetic drug 반응 **timing** 예측 가능.
- **Step 1** gene별 activation/shutdown lag 정의·정량 (lag distribution이 gene마다 실재하나?)
- **Step 2** baseline epigenomic feature로 lag structure 예측(어떤 chromatin feature가 lag을 가장 잘 설명하나?)
- **Step 3** lag-informed model을 실제 약물 timecourse에 적용(short-lag=빠른 반응 검증). 약물패널=HDACi(Vorinostat/TSA/VPA/Panobinostat/Romidepsin/Entinostat/Dacinostat)·DNMTi(Azacitidine)·DOT1Li(Pinometostat)·IDH2i(Enasidenib)·PRMT5i, 포털=L1000/CMap(시그니처)+PRISM/DepMap(민감도).
- **데이터:** 10x embryonic mouse brain, SHARE-seq skin(GSE140203), human brain(GSE162170), HSPC(GSE209878), GSE284047, **CD34+ HSPC ChIP-seq(GSE70677)**. refs=MultiVelo(2023)·MultiVeloVAE(2025)·MoFlow(2025).

## 2. 이미 흡수/보유한 것 (과장 방지 — 새 갭 아님)
| 원설계 요소 | 현재 상태 |
|---|---|
| Step1 lag 측정 | **Part 1 benchmark**(GSE209878 P1 완료, cross-dataset 진행). = 원설계 계승 |
| Step3 lag→drug **timing** | **Part 2**가 정확히 이 비전("baseline chromatin→transcription coupling이 epigenetic drug response *timing* 예측"). 단 **데이터 없어 blocked**(§4) |
| 데이터셋 GSE140203·162170·284047·209878 | 이미 사용/인지(19·26·4·다수 파일) |
| shutdown lag, bivalency, CpG, peak-to-gene, kinetic spectrum | **설계 문서엔 언급**(md 다수) |
| L1000/CMap/PRISM | paper_analysis 노트·DATA-HUNT·drug_timing_arm_scout에 **언급**(미개발) |

## 3. ★ 척추 — α-vs-lag 충돌(원설계가 우리 발견보다 앞섬)
박상준 원설계는 **lag이 gene별로 신뢰성 있게 측정되는 양**임을 전제로 Step 1→2→3을 쌓는다. 그러나 **우리 Part 1 벤치마크의 중심 발견은 정반대**다:
- **α(전사율): 방법 바꿔도 재현 ρ≈0.88** (믿을 만한 kinetic 신호)
- **lag/timing: 방법 바꾸면 답 갈림 ρ≈0.04** (비재현)

→ 원설계의 예측 변수(lag)가 **Part 1이 신뢰성을 담보하지 못한 바로 그 양**이다. 그러므로 원설계의 모든 "미완 단계"는 이 렌즈로 재해석해야 한다: **"lag을 더 하자"가 아니라, 재현되는 신호(α)로 예측 변수를 옮기고, lag이 왜 취약한지를 설명하는 쪽**이 디자인적으로 옳다.

## 4. 실제 안 된/덜 된 델타 (우선순위)

### (A) ★ 헤드라인 — GSE70677(HSPC ChIP-seq 히스톤)로 Step 2의 *날카로운* 버전
- **미사용 확인**(레포 grep 0건). **GEO 실측 구성 검증(2026-07-12):**
  - **종·세포계: Homo sapiens, Human CD34+ HSPC** (+ MPP, EPP 분화 progenitor) → **GSE209878(인간 HSPC multiome)과 같은 종·같은 세포계 = gene축 매핑 깨끗.**
  - **히스톤 ChIP-seq: H3K4me3(활성 프로모터) · H3K4me1(인핸서) · H3K27ac(활성 인핸서/프로모터)** — 각 HSPC/MPP/EPP 3집단(+input). GSM1816318~28.
  - 부가: RNA-seq(A/B/C rep) + **CAGE(5′ TSS = 전사개시 신호, transcription onset의 직교 프록시로 유용)**.
- multiome는 ATAC accessibility만 주고 **히스톤 마크는 못 준다** — 박상준이 GSE70677을 지목한 이유. 이제 **실측 활성마크(promoter/enhancer 활성)를 gene별 baseline feature로** 쓸 수 있음.
- **⚠️ 한계(정직):** GSE70677엔 **H3K27me3(억제/polycomb 마크)이 없음** → 박상준 목록의 **bivalency/poising은 이 데이터 단독으론 불가**. 필요 시 BLUEPRINT/Roadmap CD34+ H3K27me3를 별도 페어링. 또한 **bulk-population(HSPC/MPP/EPP) 해상도**(단일세포 아님) → gene별 baseline feature로만 사용(Step 2엔 적합).
- **재프레이밍(척추 반영):** Step 2를 "lag 예측"이 아니라 **"어떤 baseline chromatin 활성마크가 *재현되는 α*를 설명하고, lag은 왜 취약한가"**로. 약물 데이터 **불필요**, 지금 실행 가능, Part 1 발견과 직결. → **가장 강한 미사용 자원.** (H3K27ac/H3K4me1/me3 + CAGE로 promoter/enhancer 활성·TSS 사용을 gene별 feature화 → α·lag 각각과 회귀.)

### (B) 조건부 — PRISM/DepMap 민감도 경로 + 구체 약물패널(blocked Part 2의 available-data 대안)
- 현 PAPER-PLAN §3 결론: 요건(epigenetic drug + ≥3 timepoint + transcriptome + heme) 충족 **공개 timecourse 없음 → Part 2 blocked**.
- 박상준 원설계엔 **PRISM/DepMap(민감도, *지금 있음*) + 구체 약물패널**(Pinometostat/DOT1L·Enasidenib/IDH2·PRMT5i 등, 현 계획엔 generic "HDACi/DNMTi"만)이 있음. → **timing이 막혔으니 sensitivity/magnitude로 먼저 proof-of-concept**(Todorovski 2024와 논리 동형)라는 우회가 available-data로 가능.
- **⚠️ 그대로 clean solution 아님:** PAPER-PLAN §R2가 이미 경고한 **세포계 불일치 confound**를 정면으로 안음(정상 HSPC baseline ↔ leukemia cell-line PRISM sensitivity). → "proof-of-concept, 세포-컨텍스트 caveat 명시" 수준으로만. decay 통제(§R4, Todorovski)도 그대로 필수.

### (C) 강등 — shutdown lag(설계엔 있으나 파이프라인 미구현)
- grep: shutdown/closing lag이 md 16파일엔 있으나 **pipeline .py엔 0건**(미구현).
- **첫 lag(activation)이 이미 비재현인데 두 번째 lag(shutdown)을 추가하면 같은 취약성 상속.** → 지금 구현 권장 **안 함**. 쓰려면 activation lag과 동일한 **재현성 게이트를 먼저 통과**해야 함.

### (D) 참고 — 개념·feature 세트 구체화
- "Model 1/2 이분법 → 연속 kinetic spectrum" 프레이밍(내러티브 강화).
- Step 2 feature를 박상준 목록으로 구체화: promoter/enhancer accessibility·H3K27ac·**H3K27me3·H3K4me3(bivalency)**·TF occupancy/motif·**peak-to-gene linkage**·**CpG density·promoter class**. (현 PAPER-PLAN §4 feature 초안보다 상세 — GSE70677 있으면 실측 가능.)

## 5. 권고(팀 논의)
1. **지금 실행 가능한 유일한 새 작업 = (A) GSE70677 기반 Step 2 재프레이밍**: "재현되는 α를 설명하는 chromatin feature 지도 + lag 취약성의 후성유전적 원인." 약물 데이터 불필요, Part 1 발견을 확장, novelty 독립.
2. **(B) PRISM/DepMap sensitivity 우회**는 blocked Part 2의 임시 proof-of-concept로 **가치 있으나 confound(세포계·decay) caveat 필수** — 팀·박상준 의견 필요(그의 원 의도가 sensitivity였는지 timing이었는지 확인).
3. **(C) shutdown lag은 보류**(재현성 게이트 선통과 조건).
4. PAPER-PLAN 재구조화는 **박상준·팀 합의 후**(이건 그의 원기획).
