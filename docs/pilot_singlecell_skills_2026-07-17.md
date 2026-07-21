# BIOP01 차용 후보 공개 Agent Skill 조사 (2026-07-17)

> **결론 먼저: 차용할 것 없음(No borrow).** 4개 후보 전부 실물을 클론해 코드를 읽었다.
> **BIOP01 실패셋(RC-01~RC-06) 중 어느 하나도 잡아주는 스킬이 없다.**
> 유일하게 값어치 있는 것은 스킬이 아니라 **패턴 1개**(`validate_adata.py`의 컬럼 하드실패)이고,
> 그마저 **BIOP01이 이미 `a34c10d`로 자체 구현했다.**
>
> 판정 근거 = `BioProject02/docs/HARNESS_REVIEW_2026-07-17.md` §4.5 (star·공식 여부 근거 금지,
> 합격 기준 = 우리가 실제로 당한 실패셋). 조사자: 서브에이전트. Leader(kkkim) 검토 대기.

---

## 1. 조사 범위 · 방법

`§5.6`이 BIOP01용으로 지목한 4건 + 상위 큐레이션 소스. **전부 `git clone` 후 실파일을 읽었다**
(README 요약·star·"공식" 표기를 근거로 쓰지 않음). 클론 위치 =
`/tmp/claude-10005/-home-kkkim/43ab9758-b432-48cf-afd5-3cb59e41929a/scratchpad/skills_eval/`.

**게이트 순서(§4.5):** LICENSE 실파일 → SKILL.md·스크립트 **내용**(실행코드가 있나, 산문뿐인가) → 위험호출 → **실패셋 적용**.

**철칙 준수:** `pip install`·`conda` 미실행. `velo-*` env **무접촉**. 클론·읽기만. BIOP01 파이프라인·데이터 수정 없음. git commit 없음.

### 1.1 판정을 좌우한 단 하나의 질문

실패셋은 성격상 둘로 갈린다 — **이 분할이 모든 판정을 결정한다.**

| 층 | 실패 | 차용 가능성 |
|---|---|---|
| **오케스트레이션·검증 게이트 층** | RC-01(MoFlow 미배선 치환) · RC-04(상수부호 MultiVelo 투입) · RC-05(헤드라인 CRAK 의존) | **차용 대상 아님** — §4.5가 "검증 게이트 설계·오케스트레이션은 자작 유지"로 봉인. 공개 스킬이 소유할 수도, 소유해서도 안 된다 |
| **표준 기계작업 층** (유일한 차용 후보) | **RC-02**(컬럼명 오타 → 조용한 VAE 폴백) = *스키마/컬럼 검증*<br>**RC-03**(`abs()` 버그 → 0.317→0.295 드리프트) = *정확값 회귀 대조*<br>**RC-06**(lock.yml 미커밋·stale env) = *env-lock/체크섬 계약* | 여기만 후보 |

→ **각 스킬에 던진 질문은 하나다: "결정론적 컬럼/스키마 검증기 · 정확값 회귀 대조 · env-lock/체크섬 메커니즘이 실제로 들어 있나?"**
없으면 아무리 잘 만들었어도 우리 실패에 닿지 않는다. **기본값 = "해당 없음"**, 구체적 스크립트가 반증해야 통과.

---

## 2. 후보별 표 (실존 · 라이선스 · 실행코드 · 실패셋 적용)

| # | 후보 | 실존 | 라이선스 (**실파일 확인**) | 실행코드 유무 | **BIOP01 실패셋 적용** | 판정 |
|---|---|---|---|---|---|---|
| 1 | **`anthropics/life-sciences`**<br>`scvi-tools` · `single-cell-rna-qc` · `nextflow-development` | ✅ `e96556b` (2026-05-08) | **Apache-2.0** — repo 루트엔 LICENSE 없음, **스킬별 `LICENSE.txt` 6개 전부 Apache-2.0**. 차용 자유 | ✅ **진짜 있음.** scvi-tools 2,566줄 / QC 700줄. numpy·scipy 실연산, exit code 0/1. **AIPOCH(실행코드 0줄)와 다르다** | ❌ **RC-02/03/06 전부 미해당**(§3 상세). 게다가 `train_velovi`가 **RC-02와 같은 계열의 조용한 폴백**을 스스로 저지름 | **차용 안 함**<br>(패턴 1개만 참고) |
| 2 | **`GPTomics/bioSkills`** | ✅ | **MIT** (실파일) | ⚠️ **명목상 824개, 실질은 예시.** 스크립트 전부 `examples/` — 하드코딩 경로(`'adata_clustered.h5ad'`), exit code·assert·검증 없음. **복붙용 참조 워크플로** | ❌ **0건.** `scvelo_velocity.py`는 교과서적 scVelo 워크플로 — BIOP01이 이미 갖고 있고 더 정교함 | **차용 안 함** |
| 3 | **`bioMate-AI/biomate-bioconductor-kb`** | ✅ (경로 재확인 필요했음 — §5-b) | **듀얼**: 스킬 콘텐츠 **CC-BY-4.0**(귀속 필요) / `extraction/*.py` **Apache-2.0**. 둘 다 허용적 | ❌ **산문 KB.** SKILL.md 200개 vs 스크립트 7개, 그 7개도 **KB 생성 도구 4 + 예시 워크플로 3**(우리가 돌릴 것 아님) | ❌ **0건 + 스코프 자체가 무관.** DESeq2/edgeR/limma 선택법인데 **BIOP01은 DE를 돌리지 않는다**(§4 실측) | **차용 안 함** |
| 4 | **`GoekeLab/awesome-genomic-skills`** (상위 큐레이션) | ✅ | **CC0-1.0** | — (큐레이션 목록) | — | **후보 탐색 소스로만 유용**(§5-c) |

---

## 3. Anthropic 공식 번들 — 실제로 쓸 만한가

**(c) 답: 코드는 진짜 결정론적이다. 그러나 우리 실패셋엔 닿지 않는다. → 차용 안 함.**
"공식이라 합격"을 명시적으로 거부한다(§4.5-b).

### 3.1 `single-cell-rna-qc` — 결정론적인가? **예. 산문 아니다.**

지목된 의혹("AIPOCH는 실행코드 0줄")은 **여기선 해당 없음.** `qc_core.py`(233줄)는
`scipy.stats.median_abs_deviation` 기반 MAD 이상치 탐지·하드 임계·유전자 필터를 **실제로 계산**한다.

**그런데 우리 실패셋 적용 = 0건.** 이건 **세포 수준 QC**(mito%·ribo%·MAD 이상치)다.
RC-02(concordance 채점기 컬럼 오타)·RC-03(`abs()` 정의 드리프트)·RC-06(env lock)은
**전부 QC 하류/바깥**에서 났다. BIOP01은 이미 `p1_build.py`로 통일 전처리를 갖고 있다.

> ⚠️ 부수 경고: `detect_outliers_mad`는 **데이터 의존 임계**(MAD)다. 사전등록 규율 관점에서
> 이런 걸 채점 경로에 들이면 "데이터를 보고 골대를 옮기는" 통로가 된다. QC 층에선 표준 관행이지만,
> **채점 층으로 새어들지 않게** 하는 건 우리 책임이다.

### 3.2 `scvi-tools` — 우리 velocity 파이프라인과 맞물리나? **아니다. 일반 scVI 워크플로다.**

**표면상 맞물리는 듯 보인다** — `veloVI`·`MULTIVI` 배선이 실제로 있다
(`train_model.py:133 train_velovi`, `scvi.external.VELOVI`, `MULTIVI.setup_mudata`).
"multiome RNA+ATAC" 문구까지 있어 우리(10x Multiome, chromatin→RNA lag)와 겹쳐 보인다.

**그러나 실측하면 안 맞물린다:**

1. **우리 스택에 없다.** BIOP01 tracked 파일에서 `scvi|velovi`는 **`manuscript/SCOOP-CHECK-2026-07.md`·`related_work.md` 2곳뿐** — 즉 **선행연구로 인용**할 뿐 파이프라인이 쓰지 않는다.
2. **veloVI는 RNA-only velocity다 — lag을 못 낸다.** 우리 헤드라인은 **chromatin→transcription lag**이고 그건 MultiVelo/CRAK 계열 담당이다. veloVI는 기껏해야 **arm 하나 추가**이지 실패셋 대응이 아니다.
3. **arm 추가는 우리 문제가 아니다.** RC-01이 보여주듯 우리 병은 "arm이 모자라서"가 아니라 **"arm이 조용히 치환돼서"** 났다.

#### ⚠️ 발견 — 같은 repo가 RC-02 계열 위반을 저지른다 (`train_model.py:133-150`)

```python
def train_velovi(adata, max_epochs=500):
    """Note: Requires scvelo preprocessing. If Ms/Mu layers don't exist,
    will run preprocessing automatically."""
    if "Ms" not in adata.layers or "Mu" not in adata.layers:
        print("Preprocessing data for veloVI (scvelo moments)...")      # print일 뿐, 실패 아님
        scv.pp.filter_and_normalize(adata, min_shared_counts=30, n_top_genes=2000)
        scv.pp.moments(adata, n_pcs=30, n_neighbors=30)                 # 하드코딩 파라미터
```

**레이어가 없으면 하드 실패하지 않고 자기 파라미터로 조용히 재전처리한다.** 이건
- **RC-02와 정확히 같은 계열**(입력이 없으면 추측해서 진행 → 결과는 겉보기 정상),
- **CLAUDE.md 방법론 주의 #5**(*"method 차이 ≠ preprocessing 차이: 공통 전처리 후 method 분기(C2)"*)를 **정면으로 깬다.** 이 함수를 벤치마크에 물리면 veloVI arm만 **다른 전처리**(n_top_genes=2000/n_pcs=30)로 돌아, 우리가 재려는 "method 간 재현 일치도"가 **preprocessing 차이로 오염**된다.

`train_peakvi`도 같은 계열(`adata.X.max() > 1`이면 말없이 이진화, `train_model.py:113-115`).

> **교훈(§4.3의 `verify-refs` 사건 재연): 이름·출처를 믿지 마라.** 같은 저장소가
> **RC-02의 해약(`validate_adata.py`)과 RC-02의 병(`train_velovi`)을 동시에 담고 있다.**
> "Anthropic 공식"은 조용한 폴백 부재를 보장하지 않는다.

### 3.3 `nextflow-development` — 도입 비용 vs 이득 (정직하게)

**이득 ≈ 0. 비용 = 파이프라인 전면 재작성. → 도입 안 함.**

- **BIOP01은 Nextflow를 안 쓴다 — 실측: tracked 파일에 `nextflow|nf-core` 히트 0건.**
- 스킬 내용은 **nf-core 파이프라인 운용**(`check_environment.py`=Docker/Java/Nextflow 존재 확인, `sra_geo_fetch.py`, `manage_genomes.py`=AWS iGenomes). 우리 `download_data.sh`+`p1_build.py`가 이미 하는 일이고, **GSE209878 특화 sha256 manifest는 우리 게 더 낫다.**
- **RC-06을 잡아주지도 않는다.** `check_environment.py`는 **도구가 설치돼 있나**를 볼 뿐 **env를 잠그지 않는다**.

> **RC-06의 진짜 해약은 워크플로 엔진 도입이 아니다.** 파일럿 README §5-c가 이미 정확히 지목했다 —
> **ClawBio식 재현성 계약**(`commands.sh` + `environment.yml` + `checksums.sha256`), 즉 **가벼운 lock+체크섬**이다.
> Nextflow는 이 문제에 대한 **과잉 처방**이다.

### 3.4 RC-06 (env-lock/체크섬) — 번들 전체에 없다

전 스킬 `sha256|checksum|conda env export|environment.yml|pip freeze|lock` 전수 grep 결과:
**유일한 히트가 `instrument-data-to-allotrope/convert_to_asm.py`의 파일 해시**(실험장비 데이터 → Allotrope 변환, **완전 무관 도메인**). **conda env 고정 메커니즘은 어디에도 없다.**
→ **RC-06에 대해 이 번들이 제공하는 것: 없음.**

### 3.5 위험호출 게이트 — 통과 (경미)

`pip install`은 **에러 메시지 문자열일 뿐 실행 안 됨**. `subprocess`는 `nextflow-development` 3개 파일에만(도구 탐지·`aws s3`). `eval()`/`exec()`/`rmtree` 없음. **자동 설치 없음 → `velo-*` 오염 위험 없음.**
단 `scvi-tools`는 `adata`를 **in-place 변형**한다(`adata.X = ...`, `inplace=True`) — 읽기 전용이 아니다.

---

## 4. (d) BIOP01 실패셋에 걸리는 게 있나 — **없다**

| RC | 실패 내용 | 잡는 스킬 | 근거 |
|---|---|---|---|
| RC-01 | MoFlow 미배선 → MV×VAE 치환 | **없음**(범위 밖) | 오케스트레이션 = 자작 유지(§4.5) |
| **RC-02** | 컬럼명 `cs_lag` 오타 → **조용한 VAE 폴백** | **없음** | 가장 근접한 `validate_adata.py`조차 **AnnData `obs` 컬럼**용 — 우리 실패는 **concordance CSV 컬럼**에서 났다. **패턴은 옳고 표면이 다르다**(§6). 게다가 같은 repo `train_velovi`는 오히려 이 병을 앓는다(§3.2) |
| **RC-03** | `abs()` 버그 → 0.317→0.295 정의 드리프트 | **없음** | 4개 후보 어디에도 **정확값 회귀 대조**(커밋된 기준값 ± 허용오차) 메커니즘이 없다. 파일럿 README §7-1이 자체 과제로 잡아둔 그대로 |
| RC-04 | 상수부호 MultiVelo를 부호검정에 투입 | **없음**(범위 밖) | 검증 게이트 = 자작 유지 |
| RC-05 | 헤드라인의 CRAK 의존 | **없음**(범위 밖) | *참고*: bioSkills `trajectory-inference/SKILL.md:116`이 개념적으로 유사한 조언(*"conclusions survive dropping the velocity kernel"*)을 하나 **산문 조언이지 scorer가 아니다.** 파일럿 README §7-2("arm 신뢰상태 기계가독 정본")를 대신해주지 못한다 |
| **RC-06** | lock.yml 미커밋 · stale `velo-*` | **없음** | §3.4. 번들에 env-lock 부재 |

### ⚠️ RC-06 상태 정정 (실물이 정본 — 파일럿 README와 다름)

파일럿 README §5-b는 RC-06을 *"env lock 미커밋"*으로 적었으나 **실측하니 lock 파일은 이미 커밋돼 있다**:

```
env/velo-mv.lock.yml · env/velo-tf.lock.yml · env/velo-torch.lock.yml   → 64a93f8 (2026-07-11)
env/scv-preprocess.lock.yml · env/seqtools.lock.yml · env/celldancer.lock.txt  → tracked
```

→ **RC-06의 "lock.yml 미커밋" 절반은 해소됐다.** 남은 건 **stale `velo-*` 명명** 쪽이다.
**이 문서의 판정을 바꾸지는 않는다**(어차피 잡아주는 스킬이 없음). 다만 **파일럿 README §5-b의 RC-06 서술이 현재 실물과 불일치**하므로 kkkim 확인 후 갱신 권장.

---

## 5. 특기 사항

**(a) BioMate는 BIOP01과 스코프가 겹치지 않는다 — 실측.**
BioMate의 가치 제안은 "DESeq2/edgeR/limma **선택법**"인데, **BIOP01은 셋 중 무엇도 돌리지 않는다.**
tracked 전수 검색 결과 히트는 `p5_drug_arm_feasibility.py:18`·`results/drug_arm_feasibility.md` 2곳뿐이고,
그마저 **남의 논문 결과를 소비**하는 것이다 — *"author limma DEG (GSE201662 Table S2)"*, 즉
**저자가 limma로 낸 DEG 표를 읽어 쓰는** 것이지 우리가 limma를 실행하는 게 아니다.
→ **DE 방법 선택 KB는 BIOP01에 적용 지점이 없다.** (bulk RNA-seq DE ≠ 우리의 single-cell velocity.)

**(b) `§5.6`의 "BioMate Bioconductor KB"는 경로가 명시돼 있지 않았다 — 실존은 확인.**
정확한 경로는 **`bioMate-AI/biomate-bioconductor-kb`**(GitHub API로 확정, `total_count: 1`).
⚠️ **`GoekeLab/awesome-genomic-skills`에 BioMate 항목이 없다** — §5.6이 이 큐레이션 밖에서 가져왔다는 뜻.
또한 **WebSearch 요약이 star 수를 533으로 답했으나 API 실측은 663**이었다 —
**검색 산문을 근거로 쓰지 않고 API/실파일로 확인해야 하는 이유**의 실례(어차피 §4.5-b가 star를 근거에서 배제).

**(c) `awesome-genomic-skills`(CC0)는 목록으로서 유용하다.** 미탐색 인접 후보를 담고 있다 —
`ClawBio/ClawBio`(**RC-06 해약의 원 출처: 재현성 계약**), `bioagent-bench`(**손상 입력·decoy 파일 교란 스위트** —
우리 mutation_check와 발상이 같다), `Genentech/compbiobench-runner`, `Future-House/BixBench`.
**이번 임무 범위 밖이라 코드를 읽지 않았다 — 미검증.** 후속 조사한다면 여기부터.

---

## 6. 차용 판단 (e)

### **차용: 없음. 억지 후보를 만들지 않는다.**

§4.5의 원칙을 그대로 적용한 결과다 — *"합격 기준 = 우리가 실제로 당한 실패셋"*. **4개 후보 × 6개 실패 = 24칸이 전부 미해당.**
Apache-2.0/MIT/CC-BY라 **법적으로는 전부 차용 가능**하지만, **라이선스가 허용한다는 것이 쓸모가 있다는 뜻이 아니다.**

### 유일한 잔여 가치 — 스킬이 아니라 **패턴 1개**, 그리고 **우리는 이미 갖고 있다**

`scvi-tools/scripts/validate_adata.py`(397줄, Apache-2.0)의 계약:

```python
if batch_key not in adata.obs.columns:
    result.add_error(f"batch_key '{batch_key}' not found in obs. "
                     f"Available columns: {list(adata.obs.columns)}")   # → is_valid=False → exit(1)
```

**"호출자가 기대 컬럼을 선언하고, 없으면 추측하지 말고 하드 실패(+가용 컬럼 나열)"** — 이건 **RC-02의 정확한 해약**이다.
**그러나 BIOP01은 이미 `a34c10d`에서 같은 수정을 했다**(채점기의 *"컬럼 없으면 하드 실패(추측 금지)"*, 파일럿 README §5-b RC-02 행).
→ **차용할 게 아니라 우리 판단이 옳았다는 독립 방증.** 코드를 가져올 이유가 없다(표면도 다르다 — AnnData `obs` vs concordance CSV).

**한 가지 개선 힌트는 있다:** `validate_adata.py`는 **가용 컬럼 목록을 에러에 함께 출력**한다. RC-02류 오타 디버깅에 실질적으로 유용하니, 우리 채점기 에러 메시지에 **같은 한 줄을 더하는 것**은 저비용·유의미하다. **이건 차용이 아니라 우리 코드 개선 제안이며, Leader 승인 사항이다.**

### 자작 유지 확인 (§4.5)

검증 게이트·오케스트레이션(RC-01/04/05)은 **자작 유지**가 이번에도 실증됐다. 공개 스킬 중
`_case_meta.expected` 계약 · mutation_check · 사전등록 인용 규율에 **상응하는 것이 하나도 없었다.**
오히려 §3.2가 보여주듯 **공식 번들이 우리가 이미 고친 병(조용한 폴백)을 앓고 있다.**

---

## 7. 한계 (f) — 미검증 항목

1. **정적 읽기만 했다. 실행하지 않았다.** 철칙(env 오염 금지)에 따라 `pip install`·`conda` 미실행 →
   **스크립트가 실제로 도는지 미검증.** 판정 근거는 **소스 독해**뿐이다. 단, 이번 판정("실패셋 미해당")은
   **기능의 부재**에 근거하므로 실행해도 뒤집히지 않는다 — 없는 기능은 돌려도 안 나온다.
2. **`train_velovi`의 조용한 폴백은 코드 독해로 확정했고 실행 재현은 안 했다.**
   다만 분기(`if "Ms" not in adata.layers`)와 `print`(=실패 아님)는 **소스에 명시적**이라 해석 여지가 좁다.
3. **§5.6 4건 + 큐레이션 1건만 봤다.** `awesome-genomic-skills`의 **ClawBio·bioagent-bench 등은 미탐색**(§5-c).
   **RC-06의 진짜 해약은 ClawBio 계약 쪽**이라 파일럿 README §5-c가 이미 지목했다 — **별도 조사 권장.**
4. **`anthropics/life-sciences`는 `e96556b`(2026-05-08) 시점 스냅샷.** 이후 변경 미추적.
5. **MCP 서버는 안 봤다.** 이 번들의 다수 항목(10x·ChEMBL·Open Targets 등)은 스킬이 아니라 **MCP 서버**이고
   **BIOP01 실패셋과 무관**해 게이트 밖으로 뒀다.
6. **BioMate 200개 SKILL.md를 전수 정독하지 않았다.** 스코프 판정(§5-a: BIOP01이 DE를 안 돌림)이
   **BIOP01 쪽 실측**으로 났기 때문에 개별 스킬 품질과 무관하게 적용 지점이 없다.
7. **RC-06 상태 정정(§4)은 이 조사의 부수 발견**이다 — 파일럿 README 갱신은 **kkkim 판단 영역**이라 손대지 않았다.

---

## 8. kkkim 확인 요청

1. **RC-06 서술 정정** — 파일럿 README §5-b가 *"lock.yml 미커밋"*이라 하나 **실물은 커밋돼 있다**(`64a93f8`, 2026-07-11). 갱신할까요? (RC-06을 "부분 해소, stale 명명만 잔존"으로)
2. **`validate_adata.py` 힌트 반영 여부** — 채점기 컬럼 에러에 **가용 컬럼 목록 출력** 한 줄 추가(§6). 차용이 아니라 자체 개선.
3. **후속 조사 범위** — **ClawBio 재현성 계약**(RC-06 해약 후보) · **bioagent-bench 교란 스위트**(mutation_check와 동류)를 별도 임무로 열까요?
