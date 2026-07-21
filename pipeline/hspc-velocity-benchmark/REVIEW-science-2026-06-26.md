# BIOP01-23 과학·방법론 검토 + 약물 time-course 데이터 탐색
> ⚠️ **self-review 한계**: 본 검토는 owner 측이 임시 self-review로 수행(박상준 부재 — 다른 기기 clone 후 첫 작업이라 부득이). **Owner≠Reviewer 원칙 위반이므로 박상준 cross-review로 보강/대체 필수.**
> 검토자 관점: 과학·방법론 critic. 작성 2026-06-26.
> 자료: kkkim-pipeline 브랜치 DESIGN.md(v2), results/concordance.md, dataset/lit-search.md, todorovski-2024 scoop-analysis.

## A. 4개 검토 포인트 verdict

### 1. drug-timing 방향 — ⚠️ 방향 타당, claim reframe 필요
- GPU(DL arm)가 답하는 건 "어떤 method가 재현적 lag을 내나"(방법론)이지 "lag이 timing을 예측하나"(과학)가 **아님**. timing은 데이터 없이는 GPU로도 못 풂.
- 권고: 현 논문 scope = "lag 재현적 정량 + decay 독립 축 입증"까지. drug-timing은 future + 가설.

### 2. Todorovski scoop + decay 통제 — ✅ 방향 옳음, 2개 보강
- ΔR²/ΔAUC nested(`resp~decay` vs `+lag`)는 정답. 단:
  - (a) **다중공선성 처리**(lag↔decay 상관): 부분상관/상대중요도(LMG)/VIF/orthogonalization. DESIGN §5.6을 decay 모델에선 범위 안으로.
  - (b) **gene-intrinsic 가정 검정**(t½ K562 → HSPC 차용 confound): cell type 간 t½ 보존성 검정.

### 3. P3 발견(MultiVelo sign 구조적) — ✅ 정확, 단 절반만 완성
- MultiVelo 4-state 단조정렬 → sw2−sw1>0 항상 → sign 무정보, 크기만 정보. MoFlow c-s lag(sign 가변)로 이동 타당.
- 단 **MoFlow/MultiVeloVAE 미실행(GPU 필요)** → directional/H1은 GPU 후 완성. = GPU 투자 직접 정당화.

### 4. 벤치마크 지표 — ✅ 견고, 3개 명시
- 독립 tie-breaker 명시(현재 공란), bootstrap **층화**(희소 lineage), simulator arm **plan B**(BEELINE/SERGIO fork 실현가능성).

### GPU 투자 판단
정당함(MoFlow/VAE/CRAK 실행 → directional·H1·method선정 비로소 가능). 단 산출물=방법론 결론이지 drug-timing 결론 아님. 최대 리스크는 scoop이 아니라 **timing outcome 데이터 부재**.

---

## B. 공개 약물 time-course 데이터 탐색 결과 (2026-06-26)

검색: GEO DataSets(multiome/scATAC×drug×timecourse, scRNA×epigenetic×hematopoietic), sci-Plex(GSE139944), 83-compound new-RNA(PMC12274403), SLAM/TT-seq drug.

| 후보 | assay | timepoint | 약물 | timing outcome(≥3시점) |
|---|---|---|---|---|
| multiome+약물+timecourse | — | — | — | **❌ 존재 안 함**(GEO 2회 검색 0건) |
| sci-Plex GSE139944 | sci-RNA-seq | **24h dose-response 단일** | 188(HDAC/BET/CDK) | ❌ time축 아님 |
| 83-compound (E-MTAB-13091/14822/14924) | NASC-seq2(4sU new RNA) | **대부분 60min 단일**, SAHA만 30/60min 2점, 6/24h 대조군만 | 83 epigenetic | ❌ onset/half-time 추출 난 |
| SLAM/TT-seq 약물 (JQ1/NVP-2 등) | SLAM/TT-seq | **30–60min 단일 펄스** | CDK9/BET | ❌ synthesis/decay rate용, timing 아님 |
| Todorovski GSE229314 | bulk SLAM/TT/MAC | **2h·6h 2점** | 73 | ❌(2점) decay 차용용 |

### 결론
**drug response를 시간축으로 모델링할 수 있는(≥3 timepoint) 공개 epigenetic-drug 데이터는 사실상 없음.** 있는 건 전부 (a) dose-response 단일시점, (b) nascent RNA 짧은 펄스(synthesis/decay rate 산출용), (c) 2점. → 검토 §1·§2의 우려가 데이터로 확정됨.

### 함의 / 경로
1. **reframe(권장)** — timing은 future. 현 논문은 lag 재현성 + decay/synthesis 독립축.
2. **proxy join 가능하나 outcome 재정의 필요** — Todorovski t½(decay) + nascent(synthesis rate)를 gene-level kinetic feature로 차용 → 우리 HSPC lag과 join. **단 outcome은 timing이 아니라 magnitude/rate** → scoop-analysis "magnitude면 scoop↑" 경고 → **decay+synthesis 둘 다 통제**해야 차별 성립.
3. **wet-lab** — HSPC + epigenetic drug ≥3 timepoint (multiome 이상적). 유일하게 진짜 timing outcome 확보. 범위·비용 큼, 별도 트랙.

### 우선순위
1. timing 데이터 경로(reframe vs wet-lab) **합의** — GPU 투자보다 상위.
2. decay 통제 모델: 공선성 + gene-intrinsic 검정 추가.
3. GPU 투자 진행(method 선정/directional) — 산출물=방법론 명시.
4. 독립 tie-breaker / bootstrap 층화 / simulator plan B 명시.

**Sources:** sci-Plex(Science aax6234, GSE139944) · 83-compound(PMC12274403, E-MTAB-13091/14822/14924) · Todorovski(PMC11447529, GSE229314) · SLAM/TT-seq(PMC6858503).
