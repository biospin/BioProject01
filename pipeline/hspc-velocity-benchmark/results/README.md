# results/ — 논문 표·수치가 되는 추적(tracked) 산출물

method를 돌린 **요약 결과**만 둔다. 대용량 중간산출(.h5ad/.npz 등)은 `../data/`(gitignore)에 두고, 여기엔 **논문 Table/본문 수치로 직행하는 요약**(`*.csv`, `*.md`)만 commit한다.

> 📌 **결과·해석 종합본 = [`FINDINGS.md`](FINDINGS.md)** — 개별 분석 md를 연구 질문에 맞춰 묶은 canonical 문서. 결과를 볼 땐 여기부터. 개별 md(`concordance.md`/`h1_lag_diagnostic.md`/`scrambled_null.md`/`confound.md`/`cellcycle_genelevel.md`/`lineage_lag.md`)는 상세 근거.

## 무엇이 tracked / ignored 인가
- **tracked**: `*.csv`(요약 metric), `*.md`(리포트), `*.json`(작은 설정/요약).
- **ignored**: `*.h5ad`, `*.npz`, `*.parquet`, per-cell 대용량 등 (`.gitignore` 참고).

## 정본·기계 산출 분리 (모델2 — 한국어 정본)
일부 결과는 **한 base 이름에 3파일**로 나뉜다. BIOP02처럼 **한국어를 정본**으로 하고 검토 후 영문으로 옮기되, 재계산 게이트(byte 재현)는 **기계 산출**만 검사해 사람 윤문이 덮이지 않게 한다.

| 파일 | 역할 | 누가 쓰나 | 게이트 |
|---|---|---|---|
| `<base>.gen.md` | **기계 산출**(스크립트 출력, byte 재현) | `p3_*.py` (자동) | 재계산 diff-0 대상 |
| `<base>.md` | **한국어 정본**(윤문) | 사람 | `check_canonical_parity.py`(수치 파리티) |
| `<base>.en.md` | 영문(정본에서 파생) | 사람 | 〃 |
| `<base>.csv` | 데이터 | `p3_*.py` (자동) | 재계산 diff-0 대상 |

- 현재 대상: `identifiability_dissociation`, `concordance_{macrophage,e18_mouse_brain,GSE194122_bmmc}`.
- **스크립트는 `.gen.md`만 쓴다** — 정본 `.md`·`.en.md`는 절대 덮지 않는다(모델2 이전의 "게이트 재실행 시 한 언어 소실" 함정 제거).
- **수치·표기 형식 불변**: 윤문·번역 시 정본/영문의 모든 수치 토큰은 `.gen.md`에 그대로 있어야 한다(`0.193`→`0.19` 금지). `python3 scripts/check_canonical_parity.py`로 검증(정본 .md 지어낸 수치 0 확인).

## DESIGN §7 단계별 기대 산출물
| Phase | 파일 | 논문 매핑 |
|---|---|---|
| P2 method 실행 | `runtime.csv` (method×runtime/memory) | Methods/Table: 실행 비용 |
| P3 지표·일치도 | `metrics/*.csv`, `concordance.md` | Results: method 일치도 |
| P4 confound·null | `confound_report.md`, `simulator/*.csv` | Results: robustness |
| P5 종합 | `RESULTS.md`, `robust_lag_genes.csv` | 주요 결론 표·gene set |

## provenance 규칙
각 결과 파일 상단(또는 동명 `.prov`)에 **생성 스크립트 + git commit + 입력 객체(예: `hspc_multiome_common.h5mu`) 요약**을 남긴다 — 재현성/리뷰 대응.
