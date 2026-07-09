# α 외부검증 2차 독립 소스 — Schwalb 2016 (GSE75792) K562 TT-seq synthesis rate

실행 **2026-07-10**. 스크립트 `scripts/external_rate_validation_schwalb.py`, env `scv-preprocess`.
원자료: `results/external_rate_validation_schwalb.csv`(full-set) · `_matched.csv`(matched-set headline) · `.json`, 파생 per-gene 표 `data/k562_schwalb_ttseq_synthrate.csv`.
1차 소스(GSE229305, Todorovski)는 `results/external_rate_validation.md` Part B.

> **목적:** 기존 α 외부검증(Part B)은 fit α를 **1개** 외부 실측 합성율(Todorovski 2024 K562 TT-seq, GSE229305)과 대조해 "α가 실측 합성율에 앵커됨"(non-HK ρ +0.24~+0.29, CI 0 배제)을 보였다. 이 "n=1 외부" 취약성을 없애기 위해 **2번째 독립 소스 = Schwalb et al. 2016 (Science 352:1225, GSE75792) K562 TT-seq**를 같은 방법(gene 매핑·non-HK 필터·per-gene rate·Spearman·bootstrap 95% CI)으로 추가한다.
> 두 소스 모두 **K562** → 이는 세포주가 다른 대조가 아니라 **같은 세포 타입의 독립 실험실·독립 프로토콜·독립 정량 재현**이다(강점). cross-context(K562 측정 vs HSPC fit) caveat은 1차와 동일하게 유지된다.

---

## ★ 종합 판정 — **2차 소스는 1차를 독립 재확인하지 못한다(null). 억지 없이 정직 보고.**

**apples-to-apples 판정(matched non-HK gene set = fit α ∩ Schwalb ∩ Todorovski, 같은 gene축):**

| matched non-HK (n≈50–56) | α vs **Schwalb**(2차) | α vs **Todorovski**(1차) | Schwalb vs Todorovski |
|---|---|---|---|
| rna_only | **−0.046** [−0.35,+0.25] null | +0.229 [−0.05,+0.49] | +0.138 |
| multivelo | **−0.009** [−0.28,+0.26] null | **+0.427** [+0.14,+0.66] ✅ | +0.212 |
| multivelovae | **−0.059** [−0.34,+0.22] null | **+0.326** [+0.05,+0.57] ✅ | +0.195 |

- **같은 gene에서, 세 method 모두 α는 1차(Todorovski)를 양(+)으로 회복(+0.23~+0.43)하지만 2차(Schwalb)에 대해서는 완전 null(ρ≈0, CI가 0을 넉넉히 포함)**이다. → **2차 소스는 corroboration을 주지 않는다.**
- **결정적 원인(진단으로 확인):** 두 실측 소스 자체가 서로 약하게만 일치한다. **Schwalb synth vs Todorovski synth = ρ +0.154 (n=1905, p=1e-11)** — 같은 K562 TT-seq인데도 study 간 rank 일치가 겨우 +0.15다(matched set에서도 +0.14~+0.21). 두 "ground truth"가 서로 0.15로만 겹치면 **어떤 fit도 둘 다와 강하게 상관할 수 없다** — 이것이 corroboration의 상한을 규정한다.

> **결론:** Schwalb 2차 소스는 α 앵커링을 **독립적으로 재확인하지 못한다(null)**. 그러나 **사전등록 asymmetric 해석**상 이 null은 α를 **반증하지 않는다**(cross-context + 절대 α 비식별 + 이 소스는 잡음이 큼). 정직한 핵심 발견은 **"TT-seq 합성율 실측 자체가 study 간 rank 재현성이 낮다(ρ≈0.15)"**이며, 이것이 외부 corroboration이 도달할 수 있는 한계다. 따라서 **"n=1 외부" 취약성은 이 소스로는 제거되지 않는다** — 1차의 강한 양(+)은 유지되나, 이 2차로는 독립 재현도 반증도 되지 않는다(판정 불가에 가까움).

---

## 데이터 확보 방법 & provenance

**GSE75792는 per-gene 합성율을 제공하지 않는다.** GEO supplementary는 count table·annotation뿐이며, 합성율은 `GSE75792_transcript.annotation.gtf.gz`의 **per-Transcriptional-Unit(TU)** attribute에만 존재한다(hg19 좌표, source `Schwalb_2015`, biotype + GENCODE-overlap flag, **gene symbol 없음**). 그래서 **좌표 join으로 per-gene rate를 재계산**한다 — 이것이 "확보 가능한 형태"다(정직 문서화).

| 항목 | 값 |
|---|---|
| 원 논문 | Schwalb M. et al., *"TT-seq maps the human transient transcriptome"*, **Science 352(6290):1225–1228 (2016)**, DOI 10.1126/science.aad9841 |
| GEO | **GSE75792** (K562 wild-type TT-seq) |
| 합성율 원파일 | `GSE75792_transcript.annotation.gtf.gz` — attribute = `synthesis rate; decay rate; GENCODE` per TU (21,874 TU) |
| 다운로드 URL | `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE75nnn/GSE75792/suppl/GSE75792_transcript.annotation.gtf.gz` (GEO FTP, proof-of-work 없음, 직접 curl 성공 2026-07-10) |
| sha256 (raw gtf.gz) | `2c7a31a83d81db465889973860b0a00dab5c081997432ada1fb396db9e6707b9` |
| README | `.../GSE75792_README.txt` sha256 `f0dd51a00798c285fc3d119123eec5456f4f97dd573a93e5d28b64d080ef5f1c` |
| 좌표→gene 매핑 참조 | **GENCODE v19 (hg19)** gene-level, `https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz` → `feature=="gene"` 추출(57,820) → protein_coding 20,345. 로컬 subset sha256 `dffda977…3e62c5d` |
| 파생 per-gene 표 | `data/k562_schwalb_ttseq_synthrate.csv` (2,746 gene, `gene,synth_rate`) sha256 `a05ed445…cb713689` |

**매핑 절차(1차 방법론 재사용 + 좌표 join 추가):**
1. Schwalb TU 중 `protein_coding` + `GENCODE=="TRUE"` + 수치 synth_rate만 사용(6,913 TU).
2. 각 TU를 **같은 strand**의 GENCODE v19 protein_coding gene 중 **최대중첩(max-overlap)** gene에 배정. 신뢰 1:1 배정을 위해 **reciprocal-overlap ≥ 0.5** gate(2,965 TU 통과). **gate 통과 set의 중앙 overlap frac = 1.0** — 통과 TU는 사실상 해당 gene과 상호 완전 중첩 → gene 동일성 거의 확실(오배정 아님).
3. 여러 TU→한 gene은 **median**(1차 dup 처리와 동일).
4. non-HK/HK 층화, Spearman, **paired-gene percentile bootstrap 95% CI (B=10⁴)** — 모두 1차와 동일.

---

## 매핑 QC (discriminator — broken join과 진짜 null은 겉보기 동일하므로 반드시 검증)

우리가 이미 신뢰하는 양(Todorovski)에 대해 좌표 join을 검정한다:

**QC1 — Schwalb synth vs Todorovski synth: ρ = +0.154 (n=1905, p=1.2e-11) → ✅ join 유효.**
부호·유의가 기대(양)와 일치 → 좌표 join이 rate를 올바른 gene에 배치한다(build/join 정상). **gate 통과 set의 중앙 overlap frac=1.0**이고 frac≥0.8 subset으로 좁혀도 QC1이 개선되지 않음(ρ≈0.14) → 매핑 잡음이 병목이 아니라 **ρ≈0.15가 두 소스의 실제 일치 상한**.

**QC2 — Schwalb decay vs 측정 반감기(4개 패널): 전 패널에서 무신호(|ρ|≤0.06) → Schwalb decay는 전역적으로 신뢰 불가.**

| 반감기 패널 | n | ρ (기대: 음) | p |
|---|---|---|---|
| Todorovski K562 | 1238 | −0.013 | 0.65 |
| RNADecayCafe K562 | 1735 | −0.048 | 0.045 |
| MOLM13 | 1638 | −0.039 | 0.11 |
| THP1 | 1249 | −0.063 | 0.026 |

부호는 전부 올바른 방향(음)이나 |ρ|이 0.06 이하로 무의미 → Schwalb의 decay는 TT-seq 파생 2차 양으로 어느 실측 반감기와도 rank 상관이 없다. **∴ α 대조에는 Schwalb의 1차 관측량인 synth만 사용**(QC1은 통과, QC2는 decay 배제 근거). QC2가 synth QC1 대비 완전 null인 점은 좌표 join이 아니라 Schwalb decay의 품질 문제임을 재확인한다(join이 깨졌다면 QC1도 null이었을 것).

---

## 본 분석 — matched-gene-set(apples-to-apples)이 headline

1차와 공정 비교하려면 **같은 gene축**에서 봐야 한다. 1차(Part B)는 fit α ∩ Todorovski(n≈193~251), 본 소스의 full-set은 fit α ∩ Schwalb(n≈88~107)로 **gene universe가 다르다**. 그래서 세 소스 공통(fit α ∩ Schwalb ∩ Todorovski) non-HK matched set에서 판정한다(위 ★표). 결과: **세 method 모두 α–Schwalb는 null(ρ −0.05~−0.01, CI 0 포함), α–Todorovski는 양(+0.23~+0.43)** — 같은 gene에서 1차 신호는 살아 있고 2차 신호만 없다.

### (참고) full-set 수치 — 다른 gene universe, headline 아님(caveat)
| method | full-set non-HK α vs Schwalb | n |
|---|---|---|
| rna_only | −0.188 [−0.393,+0.031] (CI 0 포함, null) | 88 |
| multivelo | −0.210 [−0.391,−0.011] (약한 음 유의) | 96 |
| multivelovae | −0.260 [−0.431,−0.073] (약한 음 유의) | 107 |

⚠️ 이 약한 음(−0.2)은 **Todorovski에 없고 Schwalb에만 매핑된 저신뢰 gene(~30~50개)**을 포함해서 생기는 것으로, **matched set에서 부호가 사라진다(ρ≈0)**. 소규모 n·저품질 gene의 잡음이지 α와 합성율의 anti-correlation 증거가 **아니다** — headline은 위 matched set(ρ≈0, null)이다. HK 층은 overlap gene 1~3개로 완전 비정보(생략).

---

## 1차 vs 2차 나란히 비교 (matched non-HK, 같은 gene축)

| K562 TT-seq synth, matched non-HK | rna_only | multivelo | multivelovae | 판정 |
|---|---|---|---|---|
| **1차 Todorovski (GSE229305, 2024)** | +0.229 | **+0.427** ✅ | **+0.326** ✅ | 양(+), MV/VAE CI 0 배제 |
| **2차 Schwalb (GSE75792, 2016)** | −0.046 null | −0.009 null | −0.059 null | **3/3 null (CI 0 포함)** |
| **두 소스 상호 일치** | +0.138 | +0.212 | +0.195 | ρ≈0.15~0.21, study 간 재현성 낮음 |

(참고 — 1차의 원 Part B full-set 값 non-HK: rna_only +0.236 / multivelo +0.262 / multivelovae +0.285, 3/3 CI 0 배제. 위 matched set은 n이 작아 rna_only CI가 0에 걸치나 MV/VAE는 여전히 유의.)

**판정:** 1차는 양(+)으로 회복, 2차는 3/3 null. **2차는 1차를 독립 재확인하지 못한다.** 결정적 맥락은 **두 실측 소스가 서로 ρ0.15~0.21로만 겹친다**는 사실 — 이것이 corroboration 상한을 규정하므로, 2차의 null은 "α가 실측 합성율에 앵커되지 않는다"가 아니라 "**TT-seq 합성율 실측 자체가 study 간 rank 재현성이 낮아 독립 corroboration이 어렵다**"로 읽는 것이 정확하다.

---

## 한계 / caveat

1. **낮은 study 간 TT-seq 재현성이 근본 상한.** Schwalb 2016 vs Todorovski 2024 K562 synth = ρ0.15(matched set 0.14~0.21). 두 "ground truth"가 서로 0.15로만 일치하면 어떤 fit도 둘 다와 강하게 상관할 수 없다 → 2차 null의 1차 원인.
2. **좌표 join + TU-level(구식) 정량.** Schwalb는 per-gene가 아니라 per-TU(hg19). GENCODE v19 max-overlap join(reciprocal≥0.5, gate 통과 median frac=1.0)으로 gene 배정 → 추가 잡음. (단 QC1 양·유의로 join 자체는 정상 작동 확인 — null은 join 아티팩트 아님.)
3. **소규모 overlap n.** matched non-HK = 50~56(1차 full-set은 193~251). n이 작아 CI가 넓다.
4. **cross-context는 1차와 동일**(K562 측정 vs HSPC fit, rank만). 세포주 차이 caveat은 **적용 안 됨** — 두 소스 모두 K562(독립 재현이지 cross-line 아님).
5. **asymmetric 해석 유지.** null은 α 반증이 아니다 — 절대 α 비식별 + cross-context + 이 소스의 잡음. 양(+)이었다면 corroboration, null은 "이 소스로는 판정 불가"에 가깝다(1차의 강한 양이 남아 있음).

## 재현
```
conda run -n scv-preprocess python scripts/external_rate_validation_schwalb.py
```
입력: `results/{rna_only_dynamical_genes,multivelo_genes,multivelovae_genes}.csv`,
`data/{GSE75792_transcript.annotation.gtf.gz, gencode.v19.genes.gtf.gz, k562_ttseq_synthrate.csv, todorovski_k562_halflife.csv, halflife_rnadecaycafe_k562.csv, halflife_molm13.csv, halflife_thp1.csv, housekeeping.txt}` (data/ 는 .gitignore).
출력: `results/external_rate_validation_schwalb.csv`(full-set) · `_matched.csv`(headline) · `.json`, `data/k562_schwalb_ttseq_synthrate.csv`.
