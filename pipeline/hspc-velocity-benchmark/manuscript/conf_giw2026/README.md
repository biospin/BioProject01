# GIW/ISCB-Asia 2026 long abstract — 2페이지 PDF 빌드

`../CONF_LONGABSTRACT_GIW2026_BIOP01.md`(정본)에서 제출용 2페이지 PDF를 만드는 경로.
PDF는 `.gitignore` 대상이라 커밋하지 않는다. 소스와 변환기만 추적한다.

## 빌드

```bash
python3 md2tex.py /path/to/build/main.tex          # 정본 md -> LaTeX
mkdir -p /path/to/build/figures
cp ../../figures/fig01_p2_concordance.png ../../figures/fig07_reliability_map.png /path/to/build/figures/
cd /path/to/build && tectonic -X compile main.tex --outdir .
```

엔진 = `~/bin/tectonic`(0.17.0 정적 바이너리). `/tmp`가 `noexec`라 바이너리를 `/tmp`에 두면
"Permission denied"가 난다. 빌드 디렉터리는 `/tmp` 밑이어도 무방하다(실행이 아니라 쓰기라서).

## 변환기가 보장하는 것

- **한국어 제출-전-제거 메모가 원천적으로 안 실린다.** 본문을 첫 `# ` 제목 줄부터 잘라 쓰므로
  파일 머리의 HTML 주석 블록(수치 출처·내부 판단)은 들어갈 수 없다.
- **수치를 사람이 옮겨 적지 않는다.** 마크다운을 기계 변환하므로 드리프트가 생길 수 없다.
- 그리스 문자·수학 기호는 LaTeX 매크로로 치환한다(`α` -> `$\alpha$` 등). 변환 후 남은
  non-ASCII가 있으면 스크립트가 출력한다(정상 = `none`).
- Figure legends 절은 그림 캡션으로 흡수한다(내용 동일, 중복 제거).

## 제출 전 검증 (2026-08-15 실측값)

```bash
python3 -c "
from pypdf import PdfReader; import re
r=PdfReader('main.pdf'); t=''.join((p.extract_text() or '') for p in r.pages)
print('pages',len(r.pages),'| KO',len(re.findall(r'[가-힣]',t)),'| FILL',t.count('FILL'))"
```

- `pages 2 | KO 0 | FILL 0`
- 수치 토큰 대조(md vs pdf): 104/104 일치, 누락은 그림 파일명의 `01`·`07`뿐, 추가 0건
- 그림 2장 실제 삽입 확인: p1 fig01 1935x563(단 컬럼 배치라 실효 ~645dpi), p2 fig07 4539x2812
- LaTeX 경고 = underfull(여백 느슨함)만, overfull 0건

## 제출 정보

- 포털: https://app.oxfordabstracts.com/stages/82012/submitter
- 마감: 2026-08-15 23:59 AoE (= 2026-08-16 20:59 KST), no extensions
- 신청: (ii) talk and poster / 트랙 General Computational Biology and Bioinformatics
- 200단어 초록은 `../CONF_ABSTRACT_GIW2026_BIOP01.md`(199단어) 본문을 폼에 붙여넣는다
- 블라인드: 저자·소속 미기재 유지
