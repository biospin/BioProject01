# manuscript/ — 논문 원고 레이어

이 연구의 **원고**가 모이는 곳. 분석 근거(literature)는 repo 루트 `paper_analysis/`(14편 dual-lens 분석)에서 인용한다 — 근거 레이어와 원고 레이어를 분리한다.

## 파일 (생기는 대로)
| 파일 | 내용 |
|---|---|
| `draft_v2.md` | **본문 정본**(영어). 한국어 검토본 = `draft_v2_ko.md`. 내용 수정은 항상 두 파일 동시 |
| `refs.bib` | 인용 — `paper_analysis/*/<paper-id>/*.bib`에서 모음 |
| `supplementary.md` | 보충 (추가 표·방법 상세) |
| `figure-legends.md` | `../figures/figNN`과 1:1 대응하는 legend |

## 섹션 ↔ repo 매핑 (재현성)
- **Methods** ← `DESIGN.md`(protocol) + `dataset/` + `env/` + `scripts/`(P0–P5)
- **Results** ← `results/`(표·수치) + `figures/`(그림)
- **Intro/Related Work/Method 정당화** ← `paper_analysis/`(근거)

## 빌드 (선택)
```bash
pandoc manuscript/draft_v2.md --citeproc --bibliography=manuscript/refs.bib -o /tmp/draft.pdf
```
컴파일 산출물(pdf/docx)은 commit하지 않는다 (`.gitignore`).
