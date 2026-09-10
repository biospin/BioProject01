# ML4H 2026 Findings — 4페이지 PDF 빌드

`CONF_ML4H2026_BIOP01.md`(정본)에서 제출용 PDF를 만드는 경로. GIW 선례(`../conf_giw2026/`)와 같은 구조다.
**PDF는 `.gitignore` 대상이라 커밋하지 않는다. 소스와 변환기만 추적한다.**

## 트랙과 규정 (2026-09-10 CFP 실측)

| 항목 | 값 |
|---|---|
| 트랙 | **Findings (non-archival)** |
| 마감 | 2026-09-10 23:59 AoE = **KST 2026-09-11(화) 20:59** |
| 본문 | **4페이지.** 참고문헌과 부록은 페이지 수에 **포함되지 않는다** |
| 심사 | 이중맹검. 저자·소속·저장소·자기 인용 귀속이 드러나면 desk rejection |
| 제출 | OpenReview `https://openreview.net/group?id=ML4H/2026/Symposium` |
| 비용 | APC 0원, 등록비만 |

**왜 Findings인가.** BIOP01은 Genome Biology 투고를 유지한다. archival(Proceedings)로 실리면
prior publication이 되어 GB가 막힌다. BIOP02-137이 BIOP02에 대해 세운 것과 같은 논리다.

## 템플릿

공식 템플릿은 `jmlr` 클래스에 `[pmlr,twocolumn,10pt]` 옵션을 쓴다. Overleaf 원본은 직접 내려받을 수
없어서 ML4H 템플릿 논문의 arXiv e-print에서 클래스 파일을 얻었다.

```bash
curl -sL -o src.tar.gz https://arxiv.org/e-print/2508.16839
tar xzf src.tar.gz           # jmlr.cls, jmlrutils.sty, jmlrbook.cls
```

> ⚠️ 이 파일들은 **ML4H 2025 템플릿 논문**에서 온 것이다. CFP FAQ는 "올해 템플릿을 받아 쓰라"고
> 명시하므로, 제출 직전에 [2026 Overleaf 템플릿](https://www.overleaf.com/latex/templates/machine-learning-for-health-ml4h-2026-template/sqgwhtyswgcy)을
> 사람이 내려받아 클래스 파일을 교체하고 다시 빌드하는 편이 안전하다. 연도 표기는
> `md2tex_ml4h.py`의 `\jmlryear{2026}`·`\jmlrworkshop{...(ML4H) 2026}`에서 이미 2026으로 넣는다.

## 빌드

```bash
BUILD=/tmp/ml4h && mkdir -p "$BUILD/figures"
cp <arxiv에서 푼>/jmlr.cls <...>/jmlrutils.sty <...>/jmlrbook.cls "$BUILD/"
cp ../../figures/fig01_p2_concordance.png "$BUILD/figures/"
python3 md2tex_ml4h.py "$BUILD/main.tex"
cd "$BUILD" && ~/bin/tectonic -X compile main.tex --outdir .
```

엔진 = `~/bin/tectonic`(0.17.0 정적 바이너리). brew 설치는 Command Line Tools가 낡으면 실패하니
[GitHub 릴리스](https://github.com/tectonic-typesetting/tectonic/releases)의 정적 바이너리를 받는다.

그림은 `.gitignore` 대상이라 저장소에 없다. 새 머신에서는 먼저 렌더한다.

```bash
cd ../..   # pipeline/hspc-velocity-benchmark
export OMP_NUM_THREADS=1 MPLBACKEND=Agg
python figures/fig01_p2_concordance.py
```

## 변환기가 보장하는 것

- **한국어 제출-전-제거 메모가 원천적으로 안 실린다.** 본문을 첫 `# ` 제목 줄부터 잘라 쓰므로
  파일 머리의 HTML 주석 블록은 들어갈 수 없다.
- **수치를 사람이 옮겨 적지 않는다.** 마크다운을 기계 변환하므로 드리프트가 생길 수 없다.
- 그리스 문자와 수학 기호를 LaTeX 매크로로 치환한다. 변환 후 남은 non-ASCII를 출력한다(정상 = `none`).
- 저자 블록은 `Anonymous Author(s)` 고정이다. **이 블록을 제출 전에 바꾸지 않는다.**

## 제출 전 검증 (2026-09-10 실측값)

**본문 4페이지 판정** = References 헤딩이 어디서 시작하는가. p5 안에서 시작하면 실패다.

```bash
python3 - <<'PY'
import fitz
d = fitz.open("main.pdf")
for i, pg in enumerate(d, 1):
    h = pg.search_for("References")
    if h:
        print(f"본문 끝: p{i} y={h[0].y0:.0f}/{pg.rect.height:.0f}")
        break
print("총", d.page_count, "쪽")
for kw in ["Table 1", "Figure 1"]:
    print(kw, [i for i, p in enumerate(d, 1) if p.search_for(kw)])
PY
```

실측 결과: `본문 끝: p5 y=91/792` (p5 최상단이 References이고 p5에 본문은 한 줄도 없다), 총 11쪽,
Table 1 = p4, Figure 1 = p2. Overfull \hbox 0건, 비-ASCII 잔여 none.

**익명화와 수치 보존**

```bash
python3 -c "
from pypdf import PdfReader; import re
r=PdfReader('main.pdf'); t=''.join((p.extract_text() or '') for p in r.pages)
print('pages',len(r.pages),'| KO',len(re.findall(r'[가-힣]',t)),'| FILL',t.count('FILL'))"
```

- `KO 0 | FILL 0`
- 축약 전후 수치 토큰 431종 -> 431종, **완전 소실 0건**
- 저자명·소속·저장소·서버 경로 히트 0건, em-dash 0, 화살표 글리프 0

## 이 문서가 지키는 claim 규약

줄이는 과정에서 아래가 본문에 남아 있는지 매번 확인한다. 하나라도 빠지면 축약이 잘못된 것이다.

- 사전등록 통과선은 Spearman `ρ ≥ 0.50`이고 HSPC `α = 0.88`은 **관측값**이지 기준이 아니다.
  이 구분을 Methods와 Results 두 곳에 남긴다.
- 곡률과 외부검증의 연결은 `suggestive supporting evidence only`이며 지도의 어느 부분도 여기 기대지 않는다.
- ATAC-shuffle 인과 진술은 HSPC 한정, 행렬 층은 MultiVelo 한정.
- 명명된 마커 방향은 서술적(descriptive)이며 인과가 아니다.
- 연구·교육용 고지를 유지한다.
