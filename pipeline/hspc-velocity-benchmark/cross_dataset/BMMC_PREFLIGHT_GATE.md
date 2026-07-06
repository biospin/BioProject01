# BMMC 복구 pre-flight 게이트 — 판정: **PASS** (2026-07-06)

> 트랙 F(GSE194122 human BMMC 복구, donor09/SRR17693266)에서 **28.66GB BAM 다운로드 + velocyto(밤샘)** 를
> 착수하기 전, "복구가 애초에 가능한가"를 검증하는 게이트. h5ad ↔ BAM 바코드(CB) 매핑이 안 되면 복구 불가 →
> 다운로드하지 않고 중단하는 것이 설계 의도. 게이트 통과 시에만 `run_bmmc_recovery.sh` 드라이버 기동.

## 검증: 바코드 브리지 (h5ad cells ⊆ BAM CB tags?)
velocyto는 `-b <barcodes>` 로 준 세포만 spliced/unspliced 카운트한다. 따라서 processed h5ad의 세포
바코드가 BAM의 CB 태그와 **같은 형식·같은 문자열**로 존재해야 loom이 h5ad 세포에 정합된다.

| 항목 | 값 |
|---|---|
| h5ad 세포 바코드 (`s4d9_cb_sorted.txt`) | 4,325 |
| BAM CB 태그 고유 (부분 스트림 샘플 `cb_sample_uniq.txt`) | 26,635 |
| 교집합 (h5ad ∩ BAM-sample) | **3,988** |
| h5ad 바코드 중 **부분 샘플**에서 이미 발견 | **92.2%** |
| 바코드 형식 (h5ad / BAM) | 둘 다 `<16bp>-1` (suffix `-1` 일치) |

**해석:** BAM CB 샘플은 전체가 아닌 **부분 스트림**(cb_sample 5.2MB)인데도 h5ad 세포의 92.2%가 이미
잡혔다. 나머지 337개(7.8%)는 부분 샘플 밖일 뿐 전체 BAM엔 존재할 것으로 추정(방향성·형식 일치 확인).
BAM이 h5ad보다 훨씬 많은 바코드(26,635 ≫ 4,325)를 가진 건 정상 — cellranger가 valid cell 4,325로
필터한 결과이고, 우리가 검증할 방향은 **h5ad cells ⊆ BAM CBs** 이다. 이 방향이 확증됨.

→ **velocyto run `-b s4d9_barcodes_CB_dash1.txt` 는 h5ad 세포에 정합되는 loom을 만든다. 복구 GO.**

## 게이트 재료 (이전 세션 07-06 05:53~05:55 생성)
- h5ad 파생: `s4d9_barcodes_CB_dash1.txt`(4325, velocyto `-b` 입력) / `s4d9_cb_sorted.txt` / `s4d9_core16_sorted.txt`
- BAM 파생(부분 스트림): `cb_sample.txt`(원본) → `cb_sample_uniq.txt`(26635 고유) / `cb_sample_core16.txt`

## 다음 (게이트 PASS 후)
`run_bmmc_recovery.sh` detached 드라이버 기동 → [0]BAM 다운로드(28.66GB) → [1]ref GTF → [2]rmsk(optional)
→ [3]velocyto → [4]build → [5]floor → [6]MultiVelo → [7]VAE → [8]P3 concordance. 전 stage idempotent.
상태판 = `BMMC_PROGRESS`(heartbeat), 완료 = `BMMC_DONE`, 실패 = `BMMC_FAILED`.
