# 저자 연락처 정본 (투고 시스템 입력용)

투고 시스템(OpenReview, 저널 제출 폼)의 저자 이메일 칸에 넣는 값. 원고 본문에는 교신저자
이메일만 실린다. **출처는 JIRA BIOP01-79**이고, 각 값은 본인이 직접 지정했거나 kkkim이
전달받아 표로 확인받은 것이다.

| 순번 | 이름(영문) | 이메일 | 근거 |
|---|---|---|---|
| 1 · 교신 | Ka-Kyung Kim | `kakyung.kim@gmail.com` | 본인 |
| 2 | Jaemyun Lyu | `jaemyunlyu@gmail.com` | 본인 지정, BIOP01-79 #11908 |
| 3 | Geongyu Lee | `rjsrb365@gmail.com` | 본인 지정, #11909 |
| 4 | Sejin Park | `sezinie@gmail.com` | kkkim 전달분, #11890 · #11905 표 |
| 5 · 시니어 | Yong Gi Ji | `ygji49@gmail.com` | #11890 · #11905 표 |

류재면 ORCID = `0000-0001-5439-7160` (#11981).

## ⚠️ git 커밋 이메일과 혼동하지 말 것

`HANDOFF.md`의 `.mailmap` identity 표는 **커밋 작성자 주소**를 정리한 것이고 투고 연락처가 아니다.
BIOP01-79 #11905가 그 구분을 명시한다. "git 커밋 이메일이 있긴 하지만, 커밋 이메일과 투고
연락처는 다를 수 있다."

혼동하기 쉬운 짝은 이렇다.

| 사람 | 커밋 이메일 (투고용 아님) | 투고용 정본 |
|---|---|---|
| 류재면 | `siegfried.lyu@gmail.com`, `jmlyu@genolution1.com` | `jaemyunlyu@gmail.com` |
| 박세진 | `sezinie000@gmail.com` | `sezinie@gmail.com` |
| 지용기 | `braveji18@gmail.com` | `ygji49@gmail.com` |
| 이건규 | `rjsrb365@gmail.com` | 같음 |

2026-09-11 ML4H 제출 때 이 구분을 놓쳐 세 건을 커밋 이메일로 넣었고, 제출 후 수정했다.
**투고 폼을 채울 때는 이 파일을 본다. HANDOFF의 identity 표를 보지 않는다.**

## 영문명 표기 주의

**이건규 = `Geongyu Lee` (붙여쓰기).** 2026-09-11 본인 정정으로 확정됐다(BIOP02-114 #12213).
기존 출판물 7편과 통일되며 ORCID, Google Scholar, PubMed에서 같은 저자로 묶인다.

폐기된 표기가 둘 있으니 되살리지 말 것.

| 표기 | 출처 | 상태 |
|---|---|---|
| `Geongyu Lee` | 본인 정정 2026-09-11 (#12213) | **정본** |
| `Geon gyu Lee` | 본인 제출값 #11712·#11784 | 폐기 |
| `Geon-Gyu LEE` | git 커밋 identity | 투고용 아님 |

한동안 "소문자 `gyu`는 오기가 아니니 고치지 말 것"이라는 메모가 돌았는데, 그건 2026-08-15
기준 판단이었고 본인 정정으로 대체됐다. ML4H 제출본은 `Geon gyu Lee`로 나갔다가 제출 후
`Geongyu Lee`로 수정했다.

**지용기 = `Yong Gi Ji`.** 본인 카톡 확정값은 `YONG GI JI`(전대문자)이고, kkkim이 논문 관례에
따라 title case로 적었다(#12057). 소속은 본인 확정값 `Qaumtum c&s`를 그대로 쓴다.
홈페이지 철자(Quantum C&S)와 다르지만 본인 결정이므로 되돌리지 않는다.

## 2026-09-11 ML4H 제출 결과

제출 폼에서 박세진, 지용기, 이건규 세 분은 **이름 검색으로 OpenReview 프로필에 직접 연결**했다.
프로필로 연결되면 그 계정이 신원이므로 어느 이메일로 등록했는지는 문제가 되지 않고,
이해충돌 정보도 그분들 프로필에서 읽힌다. 류재면 님은 이메일 자리표시로 들어갔다.

**따라서 이메일 표는 프로필이 없는 공저자에게만 필요하다.** 프로필이 있으면 검색으로 연결한다.
