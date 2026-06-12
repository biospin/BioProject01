# Methodology Brief — trevino-2021-cortex

## 한 줄 결론 (모든 독자)

- Citation: `@trevino2021cortex`  |  Importance: `상` — human cortex multiome benchmark의 original paper이며 chromatin accessibility, gene expression, ASD noncoding mutation interpretation을 연결한다.
- 한 문장 결론: `GSE162170`과 Trevino 2021은 우리 single-cell multiome 분석에서 human cortex reference dataset과 regulatory interpretation 사례로 우선 확보해야 할 자료다.

## 재현 가능성 체크 (재현 담당자)

- 데이터 접근: GEO `GSE162170` URL stub 존재. `검토필요:` raw/processed files, donor metadata, modality별 sample mapping 확인.
- 코드 공개: `sources/code_brain_comp.url`에 GitHub stub 존재. `검토필요:` license, commit 상태, figure 재현 범위.
- 자원 요구: `미제공:` abstract에는 CPU/GPU/RAM/runtime 없음. 10x Multiome + sequence model 분석이므로 local 재현에는 고메모리 single-cell workflow가 필요할 가능성.
- 핵심 의존성: `미제공:` STAR Methods와 repo environment 확인 전까지 확정 불가.
- 자세히 -> [trevino-2021-cortex_core.md](trevino-2021-cortex_core.md) §Methods, [sources/data_GSE162170.url](sources/data_GSE162170.url)

## 우리 적용 가능성 (의사결정자)

- Dataset 호환: single-cell multiome 및 chromatin-RNA coupling benchmark로 부분 일치. HSPC biology와 직접 일치하지는 않음.
- 자원 가능성: GEO download + single-cell pipeline 재처리는 가능하나, PDF/supplementary 확보 후 정확한 preprocessing contract를 먼저 고정해야 한다.
- 비용·시간 추정: source 확보와 metadata audit 0.5-1일, GSE 재처리와 annotation mapping은 1-2주.
- ROI 한 줄: original source를 정확히 잡아두면 후속 MultiVelo/MoFlow/mmVelo 계열 결과 해석에서 dataset provenance 혼선을 줄인다.
- 자세히 -> [trevino-2021-cortex_lens-industry.md](trevino-2021-cortex_lens-industry.md) §3

## 본인 재회고 (본인)

- `질문:` 후속 velocity paper들이 사용한 Trevino subset은 원 논문의 어떤 sample/cell type/QC slice인가?
- `질문:` ASD noncoding mutation scoring의 null model과 multiple testing correction은 regulatory-grade로 충분히 투명한가?
- 다음 액션: `sources/trevino-2021-cortex.pdf` manual drop 후 Figure/Table/STAR Methods를 보강하고, `GSE162170` file manifest를 별도 dataset note에 연결. Publisher summary와 data/code availability는 `sources/publisher_fulltext_excerpt.txt`에 보존.
- 자세히 -> [trevino-2021-cortex_lens-academic.md](trevino-2021-cortex_lens-academic.md), [trevino-2021-cortex_lens-industry.md](trevino-2021-cortex_lens-industry.md) §4

---
마지막 갱신: 2026-06-08
