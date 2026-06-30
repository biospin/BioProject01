# PROGRESS-LIVE — 진행 중 작업 추적 보드

> **목적**: 이 세션에서 백그라운드로 도는 작업이 중단/다른 창 전환돼도 상태를 잃지 않도록, 단계마다 실시간 갱신. 새 세션은 이 파일 + `HANDOFF.md`만 읽으면 이어받을 수 있다.
> 최종 갱신: **2026-06-30 17:45** (cisTopic ✅완료; CRAK-Velo fit 59% 진행; scrambled ✅완료)

## 🔴 GPU 작업 (cuda:1 전용)
| 작업 | PID | 로그 | 상태 | ETA |
|---|---|---|---|---|
| ~~cisTopic full~~ | 249700 | `scratchpad/cistopic_full.log` | ✅ **16:21 DONE** | — |
| **CRAK-Velo fit** (UniTVelo+chromatin, 10000 epoch) | (main.py) | `scratchpad/crakvelo_fit.log` | 🔄 ~59% (5900/10000) | ~18:1x |

- **cisTopic 완료**: postpro `crakvelo_atac_postpro.h5ad` 12.9GB(16:20, full이 smoke 덮어씀), obsm['cisTopic'] (21878,113136) ✓.
- **CRAK-Velo fit 진행 중**: B matrix 22928 region×2000 gene, velocity gene 911. cuda:1, "GPU card 0"=물리1.
  - ⚠️ **env 수정**: CRAK-Velo가 `TF_USE_LEGACY_KERAS=1`을 강제(recover_paras.py:210) → `tf-keras==2.15.1` 설치로 해결(memory 기록).
- 완료 watcher(background Bash, id **bv1k534o0**): `adata_rna_fit.h5ad` 파일 생성/에러 감지 → 4-way 재개. (이전 cisTopic watcher는 grep 패턴 버그로 완료 미감지 → 파일기반으로 교체.)
- 다음(fit 완료 시): lag 추출(DTW c-s) → `crakvelo_genes.csv` → p3_concordance 4-way → FINDINGS.md.

## 🟢 CPU 작업 — ✅ 완료
- **scrambled-chromatin null 완료**(15:07, 1h52m, 538 gene): `results/scrambled_genes.csv`.
- **검정 완료** `scripts/p3_scrambled_null.py` → `results/scrambled_null.md`:
  - **verdict: chromatin은 MultiVelo lag을 구동하지 않음.** lag 분포 동일(MW p=0.20, KS p=0.51), per-gene ρ=0.72, chromatin likelihood 거의 불변(0.239→0.237).
  - 단 Wilcoxon paired p=0.0003 — 작은 체계적 이동(median 5.87→5.48) = chromatin의 **marginal 기여**는 있으나 지배적 아님.
  - → H1의 'MultiVelo 100% chromatin-leads = 아티팩트' 결론을 음성대조로 확증.

---

## CRAK-Velo arm (4-way H1) — 단계 체크리스트
- [x] tf env 빌드 (TF2.15.1 GPU×3 + unitvelo --no-deps + scvelo + pybedtools)
- [x] vendor clone (CRAK-Velo, cisTopic) + torch_scatter
- [x] 입력 substrate `p2_crakvelo_prep.py` → consensus 197,482 peak + gencode 좌표 (`crakvelo_{atac,rna}_prepro.h5ad`)
- [x] **cisTopic** `p2_crakvelo_cistopic.py` → `crakvelo_atac_postpro.h5ad`  ✅ 완료(~16:20)
- [🔄] CRAK-Velo fit `p2_crakvelo.sh` + `p2_crakvelo_config.json` → `crakvelo_fit/`  ← 실행 중(17:11, cuda:1)
- [ ] lag 추출 (MoFlow식 DTW c-s lag) → `results/crakvelo_genes.csv`
- [ ] p3_concordance METHODS에 `crakvelo` 등록 → 4-way H1 산출 + 문서
- ⚠️ caveat: ATAC batch(day0/day7) 미보정 + peak-count overlap합산(fragments 미보유). 4-way H1 문서에 명기.

## CPU 작업 — 단계 체크리스트
- [x] scrambled-chromatin 러너 `p2_multivelo_scrambled.py` (within-lineage ATAC 셔플) + smoke 검증
- [x] **scrambled full run** → `scrambled_genes.csv` (538 gene)
- [x] `results/scrambled_null.md` — 검정 완료 (verdict: chromatin lag 미구동, marginal 기여만)
- [ ] permutation FDR (P4) — 4-way 완료 후 (DESIGN §85, lineage 내 shuffle)

---
### 변경 로그 (append-only)
- 12:54 — cisTopic full launch(cuda:1).
- 13:15 — scrambled-chromatin null full launch(CPU, PID 253142). cisTopic 11%(333/3000). 둘 다 watcher 설정.
- 14:23 — 상태 스냅샷: cisTopic 36%(1080/3000, ETA~16:20), scrambled 55%(350/641, ETA~15:13). 둘 다 정상. (scrambled는 7h 예상보다 빨라 ~2h.)
- 15:07 — scrambled full 완료(1h52m, 538 gene). 15:10 검정 완료 → scrambled_null.md(verdict: chromatin lag 미구동). cisTopic 62%.
- ~16:20 — cisTopic full 완료. `crakvelo_fit/`(datasplit·checkpoints) 생성됨.
- 17:11 — **CRAK-Velo fit launch**(cuda:1, PID 296334, env tf, --w 100000). 실행 중. [BIOP01 창 입력불가 → BIOP02 창에서 관측·대리 기록 18:15]
- 17:0x — tf-keras 2.15.1 설치(CRAK-Velo가 TF_USE_LEGACY_KERAS 강제 → optimizer ImportError 해결). 15:16 FINDINGS.md 종합본 신설. 논문 하네스 수령→제안서(`collab_workspace/harness/PROPOSAL-*.md`), 설치는 팀 상의 후.
- 18:29 — **자율 finisher 가동**(`scratchpad/finish_crakvelo.sh`, setsid·PID 307943): fit 완료 대기 → lag 추출(`p2_crakvelo_lag.py`) → 4-way concordance(crakvelo가 METHODS 등록됨) → 결과 staging. **창 닫혀도 완주**. ⚠️ CRAK-Velo lag sign convention은 marker로 검증 후 FINDINGS 반영(자동 안 함). 실패 시 안전 로그만(가짜 결과 금지).
