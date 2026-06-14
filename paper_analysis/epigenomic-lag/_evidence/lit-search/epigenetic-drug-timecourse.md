# Lit-search — epigenetic drug 반응 *timing* 검증용 공개 데이터셋 (2026-06-14)

가설: "baseline(untreated) epigenome — gene별 chromatin→transcription lag — 이 epigenetic drug에 대한 transcriptional 반응의 *timing*을 예측한다." (`pipeline/hspc-velocity-benchmark/PAPER-PLAN.md` Part 2)

> 방법: NCBI E-utilities(esearch/esummary/elink) + GEO `acc.cgi` 1차 확인. 시점 수는 GEO overall-design 텍스트 기반, 불확실값은 `추정:` 표기. repo 중복 제거: `paper_analysis/` 14편 중 drug-timecourse 데이터셋 0편(신규).

## 핵심 결론
**요건(epigenetic drug + ≥3 timepoint + transcriptome + heme + multiome 가점)을 모두 충족하는 단일 공개 데이터셋은 없음.** 후보들은 timecourse↔chromatin↔single-cell 중 하나씩 빠진다.

## A. 후보 랭킹

| accession | 시스템 | 약물 | modality | 시점 | 규모 | sc? | multiome? | 적합 | caveat |
|---|---|---|---|---|---|---|---|---|---|
| **GSE229314** (SuperSeries GSE229306-13) | K562, THP-1 | JQ1, A-485, CDK9i, ActD | bulk SLAM-seq+MAC-seq | 2h,6h | ~60-70 samp | no | no | 상 | 시점 얕음·chromatin 없음·scoop-인접 |
| **GSE256354** | human primary AML | DAC, AZA | scRNA+bulk+methyl | 추정: endpoint/colony | n=2765 | yes(일부) | no | 중 | "timepoint"가 실험 날짜였음; timing 격자 불명 |
| **GSE201662** | mouse IDH1m AML | ivosidenib±AZA | bulk RNA | 5d,14d,4wk | 14 | no | no | 중 | mouse·IDH1i(대사)·격자 거침 |
| **GSE190785** | MOLM13+primary AML | quizartinib+LSD1i | bulkRNA+scATAC+ChIP | 2/6/24h(조건) | n=289 | scATAC | no | 중 | RNA는 condition 비교; scATAC는 처리 timecourse 아님 |
| **GSE138696** | primary AML(14명) | decitabine in-vivo | array | day0/day8 | 80 arr | no | no | 하 | 시점 2개 |
| GSE120715 | (BETi sensitivity) | I-BET | baseline chromatin(BET occ.) | — | — | no | no | 하 | baseline-chromatin→*sensitivity* 개념 reference(timing 아님) |
| bioRxiv 2024.07.17.603961 | A549(lung) | SAHA | RNA+ATAC+HiC+ChIP | 24/48h | 추정 | no | no | 하 | 비-heme·2시점·개념 reference |

## B. 페어링 전략 권고
- **단일 데이터셋 불가** → 권고 = **GSE209878(baseline multiome) + 별도 drug-timecourse 페어링**. baseline lag을 feature 행렬로 고정, 별도 timecourse의 gene-level timing(t½/onset)을 outcome으로.
- 페어링 키 = gene-level feature 정렬(genome build/annotation 통일). **최대 confound = 세포 컨텍스트 불일치**(baseline=정상 HSPC vs outcome=주로 leukemia line). 같은 시스템이면 이상적.
- 차선: outcome=GSE201662(≥3 timepoint), baseline=GSE209878 + mouse↔human ortholog 매핑(limitation 명시).

## C. Scoop 점검
1. **Todorovski 2024, NAR Cancer (PMID 39372038, GSE229314)** — leukemia에서 **baseline mRNA production/decay rate가 transcriptional/epigenetic inhibitor에 대한 gene별 반응 선택성 결정**. 우리와 논리 동형. **차이**: baseline이 RNA-decay지 chromatin-lag 아님; single-cell/multiome 아님; 2/6h 얕음 → **chromatin-lag + single-cell + timing 조합은 미점유 niche. scoop 위험 '중'.** 필수 인용.
2. **Decitabine response signature 계열(GSE138696/61162)** — response 여부(magnitude)만, timing·baseline epigenome 결합 없음.
3. **Bhagwat, I-BET sensitivity (GSE120715)** — baseline chromatin(BET occupancy)→BETi 민감도 예측. baseline-chromatin→response 논리 유사하나 outcome=sensitivity(크기), timecourse 아님.
4. (개념) bioRxiv 603961(A549,SAHA) — baseline chromatin↔expression 변화 locus별 관계. 비-heme·2시점·timing framing 아님.

→ **"baseline chromatin→transcription lag이 drug response *timing/속도*를 예측"한 정확한 framing의 출판 논문은 없음.** Todorovski(RNA-kinetics 각도)가 가장 가까움.

## D. 솔직한 갭 + wet-lab 권고
- "epigenetic drug × ≥3 timepoint × paired chromatin × human heme" 동시 충족 공개셋 없음.
- 세포 컨텍스트 불일치(정상 HSPC baseline ↔ leukemia outcome)가 페어링의 약점.
- 초기 빠른 kinetics(2-24h) 깊은 격자 부재.
- **결론: 공개 데이터만으로 직접 검증 어려움.** 권고 minimal wet-lab = **K562 또는 MOLM13/CD34+에서 (i) untreated 10x Multiome baseline 1회 + (ii) HDACi(panobinostat/SAHA)/HMA(decitabine)/BETi(JQ1) 처리 후 0/2/6/12/24/48h scRNA-seq(또는 multiome) timecourse.** 같은 시스템 페어링으로 컨텍스트 confound·scoop 동시 해소. 공개 데이터는 Todorovski(RNA-side 비교군)·GSE201662(coarse 예비검증) 보조 역할.

## 출처
- Todorovski 2024 NAR Cancer: PMID 39372038 / PMC11447529 / bioRxiv 2022.04.06.487057
- GSE229314, GSE256354, GSE201662, GSE190785, GSE138696, GSE120715 (GEO acc.cgi)
- bioRxiv 2024.07.17.603961 (A549/SAHA)
