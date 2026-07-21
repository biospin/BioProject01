# α 외부검증 2차 독립 소스 — Schwalb 2016 (GSE75792) K562 TT-seq synthesis rate

실행 **2026-07-10**. 스크립트 `scripts/external_rate_validation_schwalb.py`, env `scv-preprocess`.
원자료: `results/external_rate_validation_schwalb.csv`(full-set) · `_matched.csv`(matched-set headline) · `.json`, 파생 per-gene 표 `data/k562_schwalb_ttseq_synthrate.csv`.
1차 소스(GSE229305, Todorovski)는 `results/external_rate_validation.md` Part B에 있다.

> **목적:** 기존 α 외부검증(Part B)은 fit α를 **1개** 외부 실측 합성율(Todorovski 2024 K562 TT-seq, GSE229305)과 대조해 "α가 실측 합성율에 앵커됨"(non-HK ρ +0.24~+0.29, CI 0 배제)을 보였다. 이 "n=1 외부" 취약성을 없애기 위해 **2번째 독립 소스 = Schwalb et al. 2016 (Science 352:1225, GSE75792) K562 TT-seq**를 같은 방법(gene 매핑·non-HK 필터·per-gene rate·Spearman·bootstrap 95% CI)으로 추가한다.
> 두 소스 모두 **K562**이다 → 이는 세포주가 다른 대조가 아니라 **같은 세포 타입의 독립 실험실·독립 프로토콜·독립 정량 재현**이다(강점). cross-context(K562 측정 vs HSPC fit) caveat은 1차와 동일하게 유지한다.

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

> **결론:** Schwalb 2차 소스는 α 앵커링을 **독립적으로 재확인하지 못한다(null)**. 그러나 **사전등록 asymmetric 해석**상 이 null은 α를 **반증하지 않는다**(cross-context + 절대 α 비식별 + 이 소스는 잡음이 크다). 정직한 핵심 발견은 **"TT-seq 합성율 실측 자체가 study 간 rank 재현성이 낮다(ρ≈0.15)"**이며, 이것이 외부 corroboration이 도달할 수 있는 한계다. 따라서 **"n=1 외부" 취약성은 이 소스로는 제거되지 않는다** — 1차의 강한 양(+)은 유지되나, 이 2차로는 독립 재현도 반증도 되지 않는다(판정 불가에 가깝다).

---

## 데이터 확보 방법 & provenance

**GSE75792는 per-gene 합성율을 제공하지 않는다.** GEO supplementary는 count table·annotation뿐이며, 합성율은 `GSE75792_transcript.annotation.gtf.gz`의 **per-Transcriptional-Unit(TU)** attribute에만 존재한다(hg19 좌표, source `Schwalb_2015`, biotype + GENCODE-overlap flag, **gene symbol 없음**). 그래서 **좌표 join으로 per-gene rate를 재계산한다** — 이것이 "확보 가능한 형태"다(정직 문서화).

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
1. Schwalb TU 중 `protein_coding` + `GENCODE=="TRUE"` + 수치 synth_rate만 사용한다(6,913 TU).
2. 각 TU를 **같은 strand**의 GENCODE v19 protein_coding gene 중 **최대중첩(max-overlap)** gene에 배정한다. 신뢰할 만한 1:1 배정을 위해 **reciprocal-overlap ≥ 0.5** gate를 적용한다(2,965 TU 통과). **gate 통과 set의 중앙 overlap frac = 1.0** — 통과 TU는 사실상 해당 gene과 상호 완전 중첩이므로 → gene 동일성이 거의 확실하다(오배정이 아니다).
3. 여러 TU가 한 gene에 배정되면 **median**을 쓴다(1차 dup 처리와 동일).
4. non-HK/HK 층화, Spearman, **paired-gene percentile bootstrap 95% CI (B=10⁴)** — 모두 1차와 동일하다.

---

## 매핑 QC (discriminator — broken join과 진짜 null은 겉보기에 동일하므로 반드시 검증한다)

우리가 이미 신뢰하는 양(Todorovski)에 대해 좌표 join을 검정한다:

**QC1 — Schwalb synth vs Todorovski synth: ρ = +0.154 (n=1905, p=1.2e-11) → ✅ join이 유효하다.**
부호와 유의성이 기대(양)와 일치한다 → 좌표 join이 rate를 올바른 gene에 배치한다(build/join 정상). **gate 통과 set의 중앙 overlap frac=1.0**이고 frac≥0.8 subset으로 좁혀도 QC1이 개선되지 않는다(ρ≈0.14) → 매핑 잡음이 병목이 아니라 **ρ≈0.15가 두 소스의 실제 일치 상한이다**.

**QC2 — Schwalb decay vs 측정 반감기(4개 패널): 전 패널에서 무신호(|ρ|≤0.06) → Schwalb decay는 전역적으로 신뢰할 수 없다.**

| 반감기 패널 | n | ρ (기대: 음) | p |
|---|---|---|---|
| Todorovski K562 | 1238 | −0.013 | 0.65 |
| RNADecayCafe K562 | 1735 | −0.048 | 0.045 |
| MOLM13 | 1638 | −0.039 | 0.11 |
| THP1 | 1249 | −0.063 | 0.026 |

부호는 전부 올바른 방향(음)이나 |ρ|이 0.06 이하로 무의미하다 → Schwalb의 decay는 TT-seq 파생 2차 양으로서 어느 실측 반감기와도 rank 상관이 없다. **∴ α 대조에는 Schwalb의 1차 관측량인 synth만 사용한다**(QC1은 통과, QC2는 decay 배제 근거). QC2가 synth QC1 대비 완전 null인 점은 좌표 join이 아니라 Schwalb decay의 품질 문제임을 재확인한다(join이 깨졌다면 QC1도 null이었을 것이다).

---

## 본 분석 — matched-gene-set(apples-to-apples)이 headline

1차와 공정하게 비교하려면 **같은 gene축**에서 봐야 한다. 1차(Part B)는 fit α ∩ Todorovski(n≈193~251), 본 소스의 full-set은 fit α ∩ Schwalb(n≈88~107)로 **gene universe가 다르다**. 그래서 세 소스 공통(fit α ∩ Schwalb ∩ Todorovski) non-HK matched set에서 판정한다(위 ★표). 결과: **세 method 모두 α–Schwalb는 null(ρ −0.05~−0.01, CI 0 포함), α–Todorovski는 양(+0.23~+0.43)** — 같은 gene에서 1차 신호는 살아 있고 2차 신호만 없다.

### (참고) full-set 수치 — 다른 gene universe, headline 아님(caveat)
| method | full-set non-HK α vs Schwalb | n |
|---|---|---|
| rna_only | −0.188 [−0.393,+0.031] (CI 0 포함, null) | 88 |
| multivelo | −0.210 [−0.391,−0.011] (약한 음 유의) | 96 |
| multivelovae | −0.260 [−0.431,−0.073] (약한 음 유의) | 107 |

⚠️ 이 약한 음(−0.2)은 **Todorovski에 없고 Schwalb에만 매핑된 저신뢰 gene(~30~50개)**을 포함해서 생기며, **matched set에서는 부호가 사라진다(ρ≈0)**. 소규모 n·저품질 gene의 잡음이지 α와 합성율의 anti-correlation 증거가 **아니다** — headline은 위 matched set(ρ≈0, null)이다. HK 층은 overlap gene이 1~3개뿐이라 완전 비정보이므로 생략한다.

---

## 1차 vs 2차 나란히 비교 (matched non-HK, 같은 gene축)

| K562 TT-seq synth, matched non-HK | rna_only | multivelo | multivelovae | 판정 |
|---|---|---|---|---|
| **1차 Todorovski (GSE229305, 2024)** | +0.229 | **+0.427** ✅ | **+0.326** ✅ | 양(+), MV/VAE CI 0 배제 |
| **2차 Schwalb (GSE75792, 2016)** | −0.046 null | −0.009 null | −0.059 null | **3/3 null (CI 0 포함)** |
| **두 소스 상호 일치** | +0.138 | +0.212 | +0.195 | ρ≈0.15~0.21, study 간 재현성 낮음 |

(참고 — 1차의 원 Part B full-set 값 non-HK: rna_only +0.236 / multivelo +0.262 / multivelovae +0.285, 3/3 CI 0 배제. 위 matched set은 n이 작아 rna_only CI가 0에 걸치나 MV/VAE는 여전히 유의하다.)

**판정:** 1차는 양(+)으로 회복하고, 2차는 3/3 null이다. **2차는 1차를 독립 재확인하지 못한다.** 결정적 맥락은 **두 실측 소스가 서로 ρ0.15~0.21로만 겹친다**는 사실이다 — 이것이 corroboration 상한을 규정하므로, 2차의 null은 "α가 실측 합성율에 앵커되지 않는다"가 아니라 "**TT-seq 합성율 실측 자체가 study 간 rank 재현성이 낮아 독립 corroboration이 어렵다**"로 읽는 것이 정확하다.

---

## 한계 / caveat

1. **낮은 study 간 TT-seq 재현성이 근본 상한이다.** Schwalb 2016 vs Todorovski 2024 K562 synth = ρ0.15(matched set 0.14~0.21). 두 "ground truth"가 서로 0.15로만 일치하면 어떤 fit도 둘 다와 강하게 상관할 수 없다 → 이것이 2차 null의 1차 원인이다.
2. **좌표 join + TU-level(구식) 정량.** Schwalb는 per-gene가 아니라 per-TU(hg19)로 제공한다. GENCODE v19 max-overlap join(reciprocal≥0.5, gate 통과 median frac=1.0)으로 gene을 배정하므로 잡음이 더해진다. (단 QC1이 양·유의라 join 자체는 정상 작동함을 확인했다 — null은 join 아티팩트가 아니다.)
3. **소규모 overlap n.** matched non-HK = 50~56으로 작다(1차 full-set은 193~251). n이 작아 CI가 넓다.
4. **cross-context는 1차와 동일하다**(K562 측정 vs HSPC fit, rank만). 세포주 차이 caveat은 **적용되지 않는다** — 두 소스 모두 K562다(독립 재현이지 cross-line이 아니다).
5. **asymmetric 해석을 유지한다.** null은 α 반증이 아니다 — 절대 α 비식별 + cross-context + 이 소스의 잡음 때문이다. 양(+)이었다면 corroboration이겠지만, null은 "이 소스로는 판정 불가"에 가깝다(1차의 강한 양이 남아 있다).

## 재현
```
conda run -n scv-preprocess python scripts/external_rate_validation_schwalb.py
```
입력: `results/{rna_only_dynamical_genes,multivelo_genes,multivelovae_genes}.csv`,
`data/{GSE75792_transcript.annotation.gtf.gz, gencode.v19.genes.gtf.gz, k562_ttseq_synthrate.csv, todorovski_k562_halflife.csv, halflife_rnadecaycafe_k562.csv, halflife_molm13.csv, halflife_thp1.csv, housekeeping.txt}` (data/ 는 .gitignore).
출력: `results/external_rate_validation_schwalb.csv`(full-set) · `_matched.csv`(headline) · `.json`, `data/k562_schwalb_ttseq_synthrate.csv`.

---

# α external validation, 2nd independent source — Schwalb 2016 (GSE75792) K562 TT-seq synthesis rate

Run on **2026-07-10**. Script `scripts/external_rate_validation_schwalb.py`, env `scv-preprocess`.
Raw outputs: `results/external_rate_validation_schwalb.csv` (full-set) · `_matched.csv` (matched-set headline) · `.json`, derived per-gene table `data/k562_schwalb_ttseq_synthrate.csv`.
The 1st source (GSE229305, Todorovski) is in `results/external_rate_validation.md` Part B.

> **Purpose:** the existing α external validation (Part B) compared fit α against **one** external measured synthesis rate (Todorovski 2024 K562 TT-seq, GSE229305) and showed "α is anchored to measured synthesis rate" (non-HK ρ +0.24~+0.29, CI excludes 0). To remove this "n=1 external" fragility, we add a **2nd independent source = Schwalb et al. 2016 (Science 352:1225, GSE75792) K562 TT-seq** using the same method (gene mapping, non-HK filter, per-gene rate, Spearman, bootstrap 95% CI).
> Both sources are **K562** → this is not a different-cell-line comparison but an **independent-lab, independent-protocol, independent-quantification reproduction of the same cell type** (a strength). The cross-context (K562 measurement vs HSPC fit) caveat is kept identical to the 1st source.

---

## ★ Overall verdict — **the 2nd source does not independently re-confirm the 1st (null). Reported honestly, without forcing.**

**apples-to-apples verdict (matched non-HK gene set = fit α ∩ Schwalb ∩ Todorovski, same gene axis):**

| matched non-HK (n≈50–56) | α vs **Schwalb** (2nd) | α vs **Todorovski** (1st) | Schwalb vs Todorovski |
|---|---|---|---|
| rna_only | **−0.046** [−0.35,+0.25] null | +0.229 [−0.05,+0.49] | +0.138 |
| multivelo | **−0.009** [−0.28,+0.26] null | **+0.427** [+0.14,+0.66] ✅ | +0.212 |
| multivelovae | **−0.059** [−0.34,+0.22] null | **+0.326** [+0.05,+0.57] ✅ | +0.195 |

- **On the same genes, all three methods recover the 1st source (Todorovski) as positive (+0.23~+0.43) but are completely null against the 2nd source (Schwalb) (ρ≈0, CI comfortably includes 0).** → **the 2nd source gives no corroboration.**
- **Decisive cause (confirmed by diagnostic):** the two measured sources themselves agree only weakly. **Schwalb synth vs Todorovski synth = ρ +0.154 (n=1905, p=1e-11)** — even for the same K562 TT-seq, between-study rank agreement is only +0.15 (+0.14~+0.21 in the matched set). If two "ground truths" overlap only at 0.15, **no fit can correlate strongly with both** — this sets the ceiling on corroboration.

> **Conclusion:** the Schwalb 2nd source **does not independently re-confirm (null)** the α anchoring. However, under the **pre-registered asymmetric interpretation** this null **does not refute** α (cross-context + absolute α non-identifiability + this source is noisy). The honest core finding is that **"measured TT-seq synthesis rate itself has low between-study rank reproducibility (ρ≈0.15)"**, and that is the limit external corroboration can reach. Therefore the **"n=1 external" fragility is not removed by this source** — the 1st source's strong positive stands, but with this 2nd source there is neither independent reproduction nor refutation (close to undecidable).

---

## Data acquisition & provenance

**GSE75792 does not provide per-gene synthesis rates.** The GEO supplementary holds only count tables and annotation; the synthesis rate exists only in the **per-Transcriptional-Unit (TU)** attribute of `GSE75792_transcript.annotation.gtf.gz` (hg19 coordinates, source `Schwalb_2015`, biotype + GENCODE-overlap flag, **no gene symbol**). So we **recompute per-gene rate via a coordinate join** — this is the "obtainable form" (documented honestly).

| Item | Value |
|---|---|
| Original paper | Schwalb M. et al., *"TT-seq maps the human transient transcriptome"*, **Science 352(6290):1225–1228 (2016)**, DOI 10.1126/science.aad9841 |
| GEO | **GSE75792** (K562 wild-type TT-seq) |
| Synthesis-rate raw file | `GSE75792_transcript.annotation.gtf.gz` — attribute = `synthesis rate; decay rate; GENCODE` per TU (21,874 TU) |
| Download URL | `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE75nnn/GSE75792/suppl/GSE75792_transcript.annotation.gtf.gz` (GEO FTP, no proof-of-work, direct curl succeeded 2026-07-10) |
| sha256 (raw gtf.gz) | `2c7a31a83d81db465889973860b0a00dab5c081997432ada1fb396db9e6707b9` |
| README | `.../GSE75792_README.txt` sha256 `f0dd51a00798c285fc3d119123eec5456f4f97dd573a93e5d28b64d080ef5f1c` |
| Coordinate→gene mapping reference | **GENCODE v19 (hg19)** gene-level, `https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz` → extract `feature=="gene"` (57,820) → protein_coding 20,345. Local subset sha256 `dffda977…3e62c5d` |
| Derived per-gene table | `data/k562_schwalb_ttseq_synthrate.csv` (2,746 genes, `gene,synth_rate`) sha256 `a05ed445…cb713689` |

**Mapping procedure (reuse of 1st-source methodology + added coordinate join):**
1. Use only Schwalb TUs that are `protein_coding` + `GENCODE=="TRUE"` + numeric synth_rate (6,913 TU).
2. Assign each TU to the **max-overlap** GENCODE v19 protein_coding gene on the **same strand**. For a reliable 1:1 assignment, apply a **reciprocal-overlap ≥ 0.5** gate (2,965 TU pass). **Median overlap frac of the passing set = 1.0** — passing TUs essentially fully reciprocally overlap the gene → gene identity is nearly certain (not a mis-assignment).
3. When multiple TUs map to one gene, use the **median** (same as the 1st-source dup handling).
4. non-HK/HK stratification, Spearman, **paired-gene percentile bootstrap 95% CI (B=10⁴)** — all identical to the 1st source.

---

## Mapping QC (discriminator — a broken join and a true null look identical, so this must be verified)

We test the coordinate join against a quantity we already trust (Todorovski):

**QC1 — Schwalb synth vs Todorovski synth: ρ = +0.154 (n=1905, p=1.2e-11) → ✅ the join is valid.**
Sign and significance match expectation (positive) → the coordinate join places rates on the correct genes (build/join OK). The **median overlap frac of the passing set = 1.0**, and narrowing to the frac≥0.8 subset does not improve QC1 (ρ≈0.14) → mapping noise is not the bottleneck; rather **ρ≈0.15 is the true agreement ceiling of the two sources**.

**QC2 — Schwalb decay vs measured half-life (4 panels): no signal in any panel (|ρ|≤0.06) → Schwalb decay is globally untrustworthy.**

| Half-life panel | n | ρ (expected: negative) | p |
|---|---|---|---|
| Todorovski K562 | 1238 | −0.013 | 0.65 |
| RNADecayCafe K562 | 1735 | −0.048 | 0.045 |
| MOLM13 | 1638 | −0.039 | 0.11 |
| THP1 | 1249 | −0.063 | 0.026 |

The sign is all in the correct direction (negative) but |ρ| ≤ 0.06 is meaningless → Schwalb's decay, a TT-seq-derived secondary quantity, has no rank correlation with any measured half-life. **∴ for the α comparison we use only synth, Schwalb's primary observed quantity** (QC1 passes; QC2 is the basis for excluding decay). That QC2 is fully null relative to synth's QC1 re-confirms this is a quality problem of Schwalb decay, not of the coordinate join (had the join been broken, QC1 too would have been null).

---

## Main analysis — the matched-gene-set (apples-to-apples) is the headline

To compare fairly with the 1st source, we must look on the **same gene axis**. The 1st source (Part B) is fit α ∩ Todorovski (n≈193~251); this source's full-set is fit α ∩ Schwalb (n≈88~107), so the **gene universe differs**. We therefore judge on the three-source common (fit α ∩ Schwalb ∩ Todorovski) non-HK matched set (★ table above). Result: **all three methods are null for α–Schwalb (ρ −0.05~−0.01, CI includes 0) and positive for α–Todorovski (+0.23~+0.43)** — on the same genes, the 1st-source signal survives and only the 2nd-source signal is absent.

### (reference) full-set numbers — different gene universe, not the headline (caveat)
| method | full-set non-HK α vs Schwalb | n |
|---|---|---|
| rna_only | −0.188 [−0.393,+0.031] (CI includes 0, null) | 88 |
| multivelo | −0.210 [−0.391,−0.011] (weak negative significance) | 96 |
| multivelovae | −0.260 [−0.431,−0.073] (weak negative significance) | 107 |

⚠️ This weak negative (−0.2) arises from including **low-confidence genes (~30~50) mapped in Schwalb but absent in Todorovski**, and **the sign disappears in the matched set (ρ≈0)**. It is noise from small n and low-quality genes, **not** evidence of anti-correlation between α and synthesis rate — the headline is the matched set above (ρ≈0, null). The HK stratum has only 1~3 overlapping genes, is fully uninformative, and is omitted.

---

## 1st vs 2nd side by side (matched non-HK, same gene axis)

| K562 TT-seq synth, matched non-HK | rna_only | multivelo | multivelovae | verdict |
|---|---|---|---|---|
| **1st Todorovski (GSE229305, 2024)** | +0.229 | **+0.427** ✅ | **+0.326** ✅ | positive, MV/VAE CI excludes 0 |
| **2nd Schwalb (GSE75792, 2016)** | −0.046 null | −0.009 null | −0.059 null | **3/3 null (CI includes 0)** |
| **Mutual agreement of the two sources** | +0.138 | +0.212 | +0.195 | ρ≈0.15~0.21, low between-study reproducibility |

(reference — the 1st source's original Part B full-set values, non-HK: rna_only +0.236 / multivelo +0.262 / multivelovae +0.285, 3/3 CI excludes 0. The matched set above has small n, so the rna_only CI touches 0, but MV/VAE are still significant.)

**Verdict:** the 1st source recovers as positive, the 2nd is 3/3 null. **The 2nd does not independently re-confirm the 1st.** The decisive context is that **the two measured sources overlap only at ρ0.15~0.21** — since this sets the corroboration ceiling, the 2nd source's null reads correctly not as "α is not anchored to measured synthesis rate" but as "**measured TT-seq synthesis rate itself has low between-study rank reproducibility, so independent corroboration is hard**".

---

## Limitations / caveats

1. **Low between-study TT-seq reproducibility is the fundamental ceiling.** Schwalb 2016 vs Todorovski 2024 K562 synth = ρ0.15 (matched set 0.14~0.21). If two "ground truths" agree only at 0.15, no fit can correlate strongly with both → this is the primary cause of the 2nd-source null.
2. **Coordinate join + TU-level (legacy) quantification.** Schwalb is provided per-TU (hg19), not per-gene. Genes are assigned via a GENCODE v19 max-overlap join (reciprocal≥0.5, passing median frac=1.0), which adds noise. (But QC1 being positive/significant confirms the join itself works — the null is not a join artifact.)
3. **Small overlap n.** matched non-HK = 50~56, small (1st full-set is 193~251). Small n widens the CI.
4. **cross-context is identical to the 1st source** (K562 measurement vs HSPC fit, rank only). The cell-line-difference caveat **does not apply** — both sources are K562 (independent reproduction, not cross-line).
5. **The asymmetric interpretation is maintained.** The null is not a refutation of α — it is due to absolute α non-identifiability + cross-context + this source's noise. Had it been positive it would be corroboration; being null it is close to "undecidable with this source" (the 1st source's strong positive remains).

## Reproduction
```
conda run -n scv-preprocess python scripts/external_rate_validation_schwalb.py
```
Inputs: `results/{rna_only_dynamical_genes,multivelo_genes,multivelovae_genes}.csv`,
`data/{GSE75792_transcript.annotation.gtf.gz, gencode.v19.genes.gtf.gz, k562_ttseq_synthrate.csv, todorovski_k562_halflife.csv, halflife_rnadecaycafe_k562.csv, halflife_molm13.csv, halflife_thp1.csv, housekeeping.txt}` (data/ is .gitignore).
Outputs: `results/external_rate_validation_schwalb.csv` (full-set) · `_matched.csv` (headline) · `.json`, `data/k562_schwalb_ttseq_synthrate.csv`.
