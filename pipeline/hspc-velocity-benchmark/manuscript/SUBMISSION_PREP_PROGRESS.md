# submission-prep 진행판 (재개용)

> **세션이 끊겨도 이 파일만 읽으면 이어서 할 수 있게 유지한다.** 상태가 바뀌면 그 자리에서 갱신한다.
> 시작 2026-07-19. 상위 맥락 = `~/.claude/HANDOFF.md`, 논문 단일 권위 = `PAPER_DIRECTION.md`.

## 0. 지금 어디까지 왔나 (한눈에)

**티켓은 BIOP01-61 하나로 통합했다**(kkkim: 소단계마다 쪼개지 말 것). 62·63은 흡수 후 **향후 과제로 재정의**해 남겨 뒀다.

| # | 작업 | 상태 | 산출물 |
|---|---|---|---|
| A | 적대적 critic 재검토(2026-07-19 변경분) | ⏳ 백그라운드 | `manuscript/REVIEW-GB-2026-07-19b.md` |
| B | Supplementary figure 렌더 + AF11 정합 | ⏳ 백그라운드 | `figures/FIGURE_INVENTORY.md` + png |
| C | refs 26 → 50~85 확장(실문헌·CrossRef 검증) | ✅ **완료(후보목록)** | `manuscript/REFS_EXPANSION_CANDIDATES.md` |
| D | csv → xlsx 변환 | ✅ **완료** | `results/supp_xlsx/` 11개 파일 |
| E | A·B·C 결과를 draft에 반영 | ⛔ A·B·C 완료 후 | draft_v2 + draft_v2_ko **동시** |
| F | GitHub PR로 팀 공유 | ⛔ E 후 | PR(병합은 사람 승인) |

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
