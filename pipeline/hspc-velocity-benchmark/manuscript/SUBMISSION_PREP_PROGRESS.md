# submission-prep 진행판 (재개용)

> **세션이 끊겨도 이 파일만 읽으면 이어서 할 수 있게 유지한다.** 상태가 바뀌면 그 자리에서 갱신한다.
> 시작 2026-07-19. 상위 맥락 = `~/.claude/HANDOFF.md`, 논문 단일 권위 = `PAPER_DIRECTION.md`.

## 0. 지금 어디까지 왔나 (한눈에)

**티켓은 BIOP01-61 하나로 통합했다**(kkkim: 소단계마다 쪼개지 말 것). 62·63은 흡수 후 **향후 과제로 재정의**해 남겨 뒀다.

| # | 작업 | 상태 | 산출물 |
|---|---|---|---|
| A | 적대적 critic 재검토(2026-07-19 변경분) | ✅ **완료·반영** | `manuscript/REVIEW-GB-2026-07-19b.md` |
| B | Supplementary figure 렌더 + AF11 정합 | ✅ **완료** | `figures/FIGURE_INVENTORY.md` + figS01/03/04/05 |
| C | refs 26 → 50~85 확장(실문헌·CrossRef 검증) | ✅ **완료(후보목록)** | `manuscript/REFS_EXPANSION_CANDIDATES.md` |
| D | csv → xlsx 변환 | ✅ **완료** | `results/supp_xlsx/` 11개 파일 |
| E | A·B·C 전부 반영 완료 | ✅ **완료** | draft_v2 + draft_v2_ko **동시** |
| F | GitHub PR로 팀 공유 | ✅ **완료** | [PR #4](https://github.com/biospin/BioProject01/pull/4) (병합은 사람 승인) |

### 관련 티켓
- **BIOP01-61** — 이 진행판의 A·B·C·D 전부. 통합 티켓.
- BIOP01-62 (향후) 층③ 임베딩 화살표 감사 — 착수 전 차별점 설계 필요([12,13]이 이미 채점한 축)
- BIOP01-63 (향후) MoFlow 동일설정 재실행 대조 확보 — 인과 판정을 MultiVelo 밖으로 확장

## 1. 재개 절차 (세션이 끊겼다면 이것부터)

1. 위 표에서 ⏳인 항목의 **산출물 파일이 실제로 존재하는지** 확인한다. 있으면 그 작업은 끝난 것으로 보고 내용을 검토한다. 없으면 다시 띄운다.
2. `git log --oneline -10`으로 어디까지 커밋됐는지 확인한다.
3. `git status`로 미커밋 산출물이 있는지 본다.
4. E(draft 반영)는 **A·B·C가 모두 끝난 뒤** 한 번에 한다. 부분 반영하면 영/한 동기화가 어긋난다.

## 2. 반영할 때 반드시 지킬 규칙 (어기면 되돌려야 함)

- **draft_v2.md와 draft_v2_ko.md는 항상 같은 턴에 함께 수정.**
- **Abstract는 손대지 않는다.** 오늘 추가분은 전부 supporting 등급이며 헤드라인 승격이 없다.
- **날조 금지.** refs는 CrossRef 실조회로 확인된 것만. 그림은 실제로 렌더된 것만 Additional file에 등재.
- 금지어(정직/맞닿/가름/가려낸/갈렸다), 본문 화살표 `→`, 한국어 em대시 금지.
- 커밋 메시지에 **Claude attribution 금지**(리포 CLAUDE.md). 접두는 P0~P5 또는 실제 JIRA 키.
- 커밋 전 **결정론 재계산 게이트**: `p3_concordance` · `p3_crossdataset_concordance` · `p3_scrambled_null` 재실행 후 산출물 diff 0 확인.

## 3. 오늘(2026-07-19) 확정돼 있어 건드리면 안 되는 것

- 층② 감사 NEGATIVE(BIOP01-59), 외부 재현 REPLICATED 4/4(BIOP01-60). 커밋 `62dc643` · `743978d` · `01fa80a`.
- **5-시스템 주장은 "기준선 순서(Δ<0)"만.** HSPC의 "모든 multiome 쌍이 귀무 이하"는 외부에서 깨진다(gastrulation MultiVelo×VAE 원척도 +0.200 > 귀무 +0.038).
- **인과 결론(크로마틴 무력)은 HSPC·MultiVelo 한정.** 외부엔 ATAC-shuffle arm도 refit도 없다.
- `MultiVelo×scVelo`가 5/5 최상위지만 **모델 형태 공유** 경합 설명이 있어 "RNA가 살아남는다"로 승격하지 않는다.
- 쓰면 안 되는 문장: "평활되면 겉보기 궤적은 비슷해 보일 것"([12] A1<0.3이 반박).

## 4. 사람만 할 수 있는 것 (에이전트가 못 채움)

`<FILL>` 저자 목록 · 소속 · corresponding(이름·이메일) · repository DOI와 라이선스 · scVelo 1차 인용 확정
프로젝트 리더/주저자 확정 · BIOP01-52 리뷰어 배정 · 블로그 7·8편 게시 승인 · main 병합 승인

## 5. 로그 (완료 시각과 결과를 여기 append)

- 2026-07-19: A·B·C 백그라운드 착수, 이 진행판 생성.
- 2026-07-19: 티켓을 BIOP01-61 하나로 통합(62·63은 향후 과제로 재정의해 존치). 상시규칙 memory 갱신 — 티켓은 "한 번에 보고할 결과가 나오는 덩어리" 단위.
- 2026-07-19: **D 완료** — `scripts/p11_make_supp_xlsx.py`로 Additional file 1~10·12를 xlsx 11개 생성. AF7은 3시트(alpha_TTseq·gamma_halflife·alpha_Schwalb), AF12는 2시트(HSPC_pairs·external_pairs). 원천 누락 0건. AF11(그림)은 B 완료 후.
- 2026-07-19: **C 완료** — `REFS_EXPANSION_CANDIDATES.md`. 후보 **59편 전부 CrossRef 실물 확인**(서지는 조회 JSON 그대로, 미확인은 제외). 착지 제안: 현재 26 + Tier A 24 = **50편**(GB 하한), A+선별B ≈ **66편**(권장).
  - ★ **본문에서 이름으로 부르는데 참고문헌 항목이 없는 인용 결함 12건 발견**(직접 재확인함): Schwalb 본문 4회·refs 0 / Todorovski 2회·0 / GSE229305 3회·0 / TOST 3회·0 / sloppy 6회·0 / scrublet·STARsolo·velocyto 각 1회·0. scVelo도 [9]는 2021 perspective이지 method 논문이 아님.
  - DOI 독립 재검증 2건 통과: Schwalb *Science* 352:1225-1228 (2016) doi:10.1126/science.aad9841 · Todorovski *NAR Cancer* 6 zcae039 (2024) doi:10.1093/narcan/zcae039.
  - 함정 기록: DeepVelo 동명이인 2종(Chen/Gerstein *Sci Adv* 2022 vs Cui/Wang *Genome Biol* 2024) — 둘 다 인용하거나 둘 다 뺀다. Transtrum 2015는 양날(인용하면 dissociation이 일반현상 사례가 돼 신규성 희석) — 인용하되 무엇이 새로운지 함께 쓸 것.
  - 후속 필요: STARsolo는 preprint만 확인(STAR Dobin 2013은 **미검증**) · Reactome release 버전 확인 후 DB 논문 인용 여부 결정 · 저자 목록이 6인+et al.로 절단돼 최종 조립 시 전체 저자 재조회 · GSE194122·10x E18 demo 출처 논문은 확정 불가라 accession-only 유지.
- 2026-07-19: **B 완료** — 약속된 다섯 패널 **전부 실물화**. (1) `figS01_per_dataset_concordance` (2) 기존 `fig05_profile_likelihood`(재실행 검증 통과) (3) `figS03_atac_shuffle_lag` (4) `figS04_coupling_shuffle` (5) `figS05_stiffness_tertile_ladder`. 조작 없음. 신규 스크립트 4개 모두 **재계산값이 `results/*.md` 기존 수치와 어긋나면 SystemExit으로 죽는 게이트** 내장, 전부 통과. 라벨 전부 영어(tofu 0).
  - 정직성 표기 2건: 패널 3·4는 "귀무 분포"가 아니라 **셔플 1회 realization 겹쳐 그리기** → AF11 문구를 "overlaid on the observed"로 교정 필요. coupling MW p=5.6e-75는 **셔플 20회 pooled** 값이고 csv엔 realization 0만 있음(그것만이면 2.0e-40) → 재계산하지 않고 "20회 pooled, 인용"으로 표기.
  - `fig05_profile_likelihood.py` 헤더가 `velo-mv` env를 요구한다고 적혀 있으나 그 env는 이 서버에 없고 **scv-preprocess에서 패널 A~D 전부 완주** — 헤더 기술이 과함(수정 후보).
  - 기존 png 8장 중 약속 패널에 해당하는 건 fig05 하나뿐. fig02는 cross-**dataset**(cross-method 아님), fig03·04는 블로그용 개념도.
  - ⚠️ **에이전트가 제기한 "HSPC lag ρ=+0.163 추적 불가"는 오경보** — 확인 결과 `results/identifiability_dissociation.md`에 ρ_lag(magnitude) **+0.163, 95% CI [+0.078, +0.244]** 로 CI까지 draft와 일치한다. 같은 파일이 "FINDINGS §3.5의 signed −0.010은 MV-magnitude와 VAE-signed를 섞은 범주 불일치"라는 경고도 이미 달아 뒀고, 그것이 draft Table 1 각주 †가 화해시키는 바로 그 지점이다. **draft 수정 불필요.**
  - png는 `.gitignore` 대상 → 스크립트와 인벤토리만 커밋. 투고 번들은 `FIGURE_INVENTORY.md` §3의 재생성 명령으로 만든다.
- 2026-07-19: **A 완료·반영** — 자체 critic **MAJOR REVISION**(CRITICAL 1·MAJOR 6·MINOR 8). 전부 영/한 동시 반영, 커밋 `3fee5a1`.
  - CRITICAL-1: HSPC 문단 헤드라인 수치가 **중심화**인데 봉인 규약의 주 지표는 **원척도**이고 centring은 목록에 없었다 → 모든 수치에 라벨을 붙이고, centring이 사후 진단임과 사전등록 판정은 원척도로 계산됐음을 본문에 명시.
  - MAJOR: "genuine disagreement" 주장을 MultiVelo 한정으로 축소(0 근처 세 쌍이 전부 MoFlow 쌍) · 천장(15,315 세포 재적합)과 셔플(전량)이 서로 다른 섭동이라 **천장이 하한**임을 자백 · −0.500의 부호규약 유보 복원 · [12]가 rna_only였음을 층③ 문장에 명시 · Background↔Positioning 자기모순 해소 · 부호 일치율에 제외율(0~30.5%)과 기준선 해석 추가 · 신규성 3항목 중 refit 천장이 [13] seed 안정성과 겹침을 인정.
  - **MAJOR-6은 텍스트가 아니라 실행으로 해결**: 봉인해 놓고 빠뜨렸던 **유전자 셔플 null**을 p10·p10c에 추가해 재실행. multiome 쌍 중 귀무를 넘은 건 MultiVelo×VAE 하나(+0.328), 최대 초과분 둘은 다시 RNA-only 쌍(+0.380·+0.278). **판정 불변**(NEGATIVE / REPLICATED 4/4).
  - 오경보 1건 기각: "lag ρ=+0.163 추적 불가"는 사실이 아님(`identifiability_dissociation.md`에 CI까지 일치).
  - 게이트 통과(재계산 diff 0), EN/KO 파리티 28/28, 금지어 0, 화살표 0, Abstract 무수정.
- 2026-07-19: **F 완료** — PR #4 생성(팀 공유·리뷰용, 병합은 사람 승인). 리뷰 요청 3항: 주장 범위 제한 충분성 / MultiVelo×scVelo 처리 / refs 후보 채택 범위.

### ⏭ 다음 세션이 이어서 할 일
1. **C(참고문헌) 본문 반영이 유일한 미완**입니다. `REFS_EXPANSION_CANDIDATES.md`의 검증된 후보를 draft에 넣되 **영/한 동시**, 번호는 기존 [1]~[26] 뒤에 append하면 재번호 없이 끝납니다. 우선순위는 **인용 결함 12건**(Schwalb·Todorovski/GSE229305·scVelo 원본·velocyto·sloppy/stiff·profile likelihood·BH·TOST·scrublet·STARsolo·Reactome·과립 마커) — 이건 심사에서 바로 걸릴 구멍입니다.
2. 후보 파일의 미검증 항목 주의: STARsolo는 preprint만 확인됨(STAR Dobin 2013 **미검증**), Reactome은 실제 사용 release 확인 필요, 저자 목록이 6인+et al.로 절단돼 최종 조립 시 재조회 필요.
3. DeepVelo 동명이인 2종은 **둘 다 인용하거나 둘 다 제외**.
- 2026-07-20: **C(참고문헌) 본문 반영 완료 — 26 → 66편.** kkkim 지적 두 건 처리.
  - **왜 인용 결함 12건이 났나**: 기존 `verify_citations.py`는 *목록 → CrossRef* 방향(내가 적은 문헌이 실존하나)만 본다. 목록에 아예 없는 것은 원리적으로 못 잡는다. 누락분은 대부분 초안 이후 본문이 자라며 생겼다(외부검증·통계규약·전처리·기제 서술). → **`scripts/p13_check_uncited_sources.py` 신설**(*본문 → 목록* 방향). 초록·Additional file 캡션은 규약상 제외. 현재 영/한 **0건 통과**.
  - **넘버링**: 등장순이 아니었다(9번째 등장이 [14], [16]~[19]는 맨 뒤에서 첫 등장 = 주제별 배정 흔적). → **`scripts/p12_refs_integrate_renumber.py`**로 토큰화 → 앵커 삽입 → **첫 등장 순 1..N 재배정** → 목록 재작성 → 영/한 매핑 대조.
  - 채택: Tier A 24 + Tier B 16 = 40편 추가. B는 도구 인용 결함(scrublet·STARsolo)과 논지 직결 문헌 우선. **DeepVelo 동명이인 2종은 둘 다 제외.**
  - **표기 통일**(kkkim "목차가 이상하다"): 신규분이 CrossRef 원문 그대로라 `La Manno Gioele, …` 전체이름+따옴표 제목이었고 기존은 Vancouver 약자여서 두 양식이 섞여 있었다. → **`scripts/p14_normalize_refs.py`**로 DOI 재조회해 family/given을 제대로 받아 약자로 변환(6명 이하 전원, 7명 이상 앞 3명+et al.), 따옴표 제거, 쪽 범위 en dash, preprint 라벨 통일. 40건 변환. `[39]`는 in press라 preprint 오라벨을 되돌림.
  - 검증: 영/한 각각 본문 66종 == 목록 66편, 첫 등장 순 == 1..66, 1:1 대응, **영/한 목록 텍스트 66/66 동일**, 초록 인용 0.
  - 작업 중 사고 2건과 처리: ① 같은 문구가 초록과 본문에 있어 **초록에 인용이 샜다** → 스크립트에서 Background 이전 구간을 구조적으로 배제 ② 스크립트를 처리된 파일에 재실행해 103편이 됐다 → 백업 복구 후 클린 상태에서 1회만 실행.
  - 남은 것(사람): `<FILL>` 저자·소속·corresponding·repository DOI/라이선스. 그 외 자동 처리 가능한 항목은 없음.
  - 참고: Enrichr(speedrichr custom background)는 본문에서 도구명을 부르지 않아 인용 대상이 아니다. 재현성을 위해 Methods에 도구명을 넣을지는 **내용 판단**이라 남겨 둔다.
- 2026-07-20: **Enrichment 절차를 Methods에 명기 — 재현성 구멍 하나 메움.** Results에 `adjusted p=9.4e-04`가 실려 있는데 그 값을 낸 도구·절차가 Methods에 없었다(Reactome은 라이브러리 이름일 뿐, 계산은 Enrichr speedrichr). 리뷰어가 재현하려면 도구·라이브러리·배경·보정 방식이 필요하다.
  - 새 소절 「Enrichment analysis」(영/한): Enrichr[66,67,68] + Reactome[42], **speedrichr custom background**, 배경을 **부호 가변 판정 2개 이상인 640개 유전자**로 교체하면 GO 항목이 전부 사라지고 Reactome neutrophil degranulation(n=15)만 남는다는 점, BH 보정, 만장일치 RNA-first 164개는 어느 배경에서도 무유의.
  - Enrichr 3편 CrossRef 실검증(Chen 2013 · Kuleshov 2016 · Xie 2021). 참고문헌 **66 → 69편**.
  - **인용결함 검사기가 새 문장의 누락을 즉시 잡았다** — "Benjamini-Hochberg"에 인용이 없었다. BH[65] 부착 후 재통과. 검사축을 만든 값을 바로 회수.
  - `scripts/p15_renumber_inplace.py` 신설: p12는 번호 없던 상태에 한 번 쓰는 도구라 처리된 파일에 재실행하면 중복된다(실제로 66→103 사고). p15는 **현재 상태에서** 기존 `[n]`을 토큰으로 되돌려 재번호한다. 앞으로 참고문헌을 더 넣을 때는 **p12가 아니라 p15**를 쓴다.
  - 검증: 영/한 각각 본문 69종 == 목록 69편, 첫 등장 순 1..69, 1:1, 목록 텍스트 69/69 동일, 초록 무인용, 토큰 잔여 0, 재계산 게이트 diff 0.
- 2026-07-20: **"크로마틴은 velocity 행렬에 무력하다" 철회 반영**(근거 = `results/velocity_matrix_paired_shuffle.md`, 커밋 `8b995ed`). 기존 비교가 천장은 재표집 15,315 cell, 셔플은 전량 21,878 cell이라 세포집합이 어긋나 있었다. 같은 S_b에서 짝맞추면 셔플이 온전한 범위 아래로 3/3(+0.784·+0.813·+0.810 대 +0.826~+0.887, CI 3/3 비중첩).
  - **반대 방향의 양성 단정은 하지 않는다.** 같은 세포·같은 설정 run-to-run 귀무가 없어 짝지은 Δ(+0.081·+0.004·+0.063, b=1은 사실상 null)는 크로마틴 기여와 재적합 잡음의 합이다. 이 한계를 본문에 명시했다.
  - 수정 파일: `draft_v2.md`(Results 문단 1개를 2개로, Methods 층② 소절) · `draft_v2_ko.md`(대응 문단 동시) · `results/velocity_matrix_audit.md`(§0 정정 박스, §1 B행 포인터, §4, §5-2, §6 한계 갱신) · `PAPER_DIRECTION.md` 2026-07-19 블록에 정정 항목 추가(governing doc에 철회된 결론이 남지 않도록).
  - **Abstract 무수정.** 이 건은 층② 행렬 한정 supporting sub-claim이며, Abstract의 인과 문장은 층① per-gene lag 대상이라 무관하다.
  - Additional file 번호는 새로 만들지 않고 `results/velocity_matrix_paired_shuffle.md` 경로로만 인용했다. 이 대조에 AF를 새로 부여할지는 사람 판단으로 남긴다.
  - 사실오류 정정: `scramble_within_lineage`(p2)는 **lineage 내부 ATAC 행(세포) permute**라 draft의 "shuffling ATAC gene labels"를 고쳤다. AF9(p7 coupling)는 실제로 유전자 열 permute(`RNG.permutation(n_genes)`)라 캡션이 맞아 **손대지 않았고**, permutation-FDR의 gene-label shuffle null도 정상이라 그대로 뒀다.
  - 검증: 재계산 게이트 3종 재실행 diff 0, 금지어 0, 본문 화살표 0, 신규 한국어 문단 em대시 0, 인용결함 검사 0건, heading 파리티 34/34.
- 2026-07-20 심야: **run-to-run null 결과를 draft에 반영 — 철회가 "잡음 아님"으로 정정됐다.** 다른 창이 `p10e_runtorun_null_audit.py`로 잰 결과(커밋 c70efa7)를 영/한 본문에 옮겼다.
  - 결과: MultiVelo 적합은 **결정론적**이다. 같은 세포집합·같은 입력에서 worker 수만 바꾼 두 적합이 **bit 단위 동일**, 감사 지표로 잰 Δ_rr = **0.000000**(부트스트랩 구간 퇴화), 측정한 두 세포집합 모두. 보관 적합과의 유일한 차이는 유전자 하나(LRIG1)로 4e-16 반올림 또는 loss가 거의 같은 대안 해이며 세포별 중심화 코사인을 최대 2e-06 움직인다.
  - 따라서 **짝지은 Δ에는 빼낼 재적합 잡음 성분이 없다.** 사전등록 조건(upper CI(|Δ_rr|) < lower CI(Δ_paired))이 0.000000 대 0.0792·0.0608로 통과 → **POSITIVE-ENABLED**.
  - draft 문장 교체: "재실행 귀무가 없어 Δ에 크로마틴과 재적합 잡음이 섞여 있다"(옛말) → "크로마틴 채널을 파괴하면 출력이 실제로 움직이며 그 움직임은 재적합의 인공물이 아니다"(MultiVelo·이 행렬 한정).
  - 한계 3개를 같은 문단에 유지: (1) 세 쌍 중 둘만 짝맞춘 귀무를 가지며 짝 Δ가 가장 작은 쌍(+0.004)은 빠져 있다 (2) 짝 Δ는 세포집합당 셔플 추출 한 번에 기대므로 셔플 표집 분산이 정량되지 않았다 (3) 효과는 method 선택이 만드는 불일치보다 **한 자릿수 아래**라 "여기서 크로마틴이 기여한다"가 "크로마틴이 이 행렬을 신뢰할 만하게 만든다"는 뜻은 아니다.
  - 이 주장은 하루에 **두 번 뒤집혔다**: 인과 있음 → (짝맞춤 대조) 철회 → (결정론 실측) 잡음 아님. 논문 주 결론(방법 간 불일치)은 세 번 모두 영향 없음.
  - 검증: 영/한 수치 파리티 전항 일치, 옛 문장 잔여 0, 참고문헌 69/69 동일, 인용결함 검사 통과, 재계산 게이트 diff 0.
