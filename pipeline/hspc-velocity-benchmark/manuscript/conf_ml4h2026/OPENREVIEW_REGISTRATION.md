# OpenReview 프로필 등록 안내 (ML4H 2026 투고용)

ML4H 2026은 OpenReview로 투고함. **공저자는 각자 OpenReview 프로필이 있어야 함.**
2026-09-11에 kkkim이 직접 등록하며 막혔던 지점을 정리한 것이니, 처음 하는 사람은
이 문서 순서대로 하면 같은 데서 안 막힘.

등록 주소: https://openreview.net/
투고 그룹: https://openreview.net/group?id=ML4H/2026/Symposium

## 왜 미리 해야 하나

- 투고 자체가 OpenReview 계정으로 이루어짐.
- **신규 프로필은 사람이 검토함.** 바로 승인되지 않을 수 있으니 마감 직전에 시작하면 위험함.
- ML4H는 **상호 심사(reciprocal reviewing)** 를 요구함. 저자 중 최소 한 명이 심사자로
  등록돼야 하고, 등록이 없거나 배정된 심사를 제대로 하지 않으면 **desk rejection 사유**가 됨.

## ⛔ 가장 많이 막히는 곳 — 이메일 인증

**가입 후 확인 메일 링크를 누르지 않으면 로그인이 안 됨.** 비밀번호를 맞게 넣어도 실패함.
2026-09-11에 실제로 여기서 한참 막혔음.

증상이 "비밀번호가 맞는데 로그인이 안 됨"이면 아래를 볼 것.

1. 로그인 폼 아래 `Didn't receive email confirmation?`을 눌러 재발송할 것.
2. 스팸함을 볼 것.
3. `Forgot your password?`로 진단할 것. **계정이 없다고 나오면 아직 가입 전**이므로
   `Sign Up`부터 할 것.
4. 가입에 쓴 주소가 지금 넣는 주소와 같은지 볼 것.

## 등록 6단계

| 단계 | 내용 | 필수 여부 |
|---|---|---|
| 1 | Names | 필수 |
| 2 | Personal Info (Gender, Pronouns, DOB) | 선택 |
| 3 | Emails | 필수 |
| 4 | **Personal Links** | **최소 1개 필수** |
| 5 | Career & Education History | **현재 소속만 필수** |
| 6 | Expertise | 심사 배정에 쓰임 |

폼 안내 원문: *"Enter your current institution and at least one web URL to complete your
registration. All other fields are optional."*

## 4단계 Personal Links — 요건을 오해하기 쉬움

폼이 요구하는 조건이 까다로움.

> *At least one URL is required that displays your name and email.*

**이름과 이메일이 둘 다 보이는 페이지**여야 함. 여기서 걸리는 이유는 이러함.

- **ORCID**는 공개 이메일이 기본으로 비공개라, 그대로면 조건을 못 채움.
- **Google Scholar**는 검증 이메일이 없으면 이메일이 안 보임.
- **개인 홈페이지나 블로그에 이름과 이메일을 함께 올려 두면 그것 하나로 해결됨.**
  기관 홈페이지의 본인 소개 페이지도 같은 역할을 함.

채울 칸: Homepage, Google Scholar, DBLP, ORCID, Wikipedia, LinkedIn, Semantic Scholar,
ACL Anthology.

생명정보 분야면 **DBLP(전산학 색인)와 ACL Anthology(자연어처리 학회 색인)는 비워도 됨.**

### 동명이인 주의

Semantic Scholar와 Google Scholar는 같은 이름의 다른 연구자와 섞이기 쉬움. **논문 목록을
직접 보고 본인 것인지 확인한 뒤 URL을 넣을 것.** 공저자 구성을 보면 대개 갈림.

## 5단계 Career & Education History

**필수는 현재 소속 한 줄.** 나머지 줄은 오른쪽 빼기 버튼으로 지워도 등록됨.

다만 폼 설명이 밝히듯 **기관 도메인이 이해충돌(COI) 탐지와 저자 중복 제거에 쓰임.**
과거 소속이 없으면 옛 동료가 심사자로 배정되는 것을 시스템이 못 막음. 상호 심사로
심사자가 될 수 있으므로 **직전 소속과 최종 학력까지 세 줄 정도는 넣기를 권함.**

한 줄에 들어가는 칸: Position / Start / End / Institution(도메인) / Institution Name /
Country-Region / State-Province / City / Department.

- 재직 중이면 **End를 비울 것.**
- **Position은 소속이 있으면 `Researcher`, 소속이 없으면 `Independent Researcher`.**
  기관 도메인을 넣어야 COI 탐지가 작동하므로, 재직 중이면 `Independent Researcher`를
  고르지 말 것.
- 학위 과정은 `PhD student`, `MS student` 등으로 넣을 것.
- **도메인은 실제로 열리는지 확인하고 넣을 것.** 회사 대표 도메인과 연구소 도메인이
  다른 경우가 있음.
- 정확히 모르는 칸(City 등)은 비울 것. 지어내지 말 것.

### 논문 소속과 달라도 됨

원고의 소속과 OpenReview 프로필의 소속이 달라도 모순이 아님. 가리키는 것이 다르기 때문임.

- **원고의 소속** = 이 연구를 어느 기관 소속으로 수행했는가. 회사 업무가 아닌 개인 연구면
  무소속으로 적는 것이 정직함.
- **OpenReview 프로필** = 지금 어디 사람인가. 이해충돌 계산용이며 이중맹검 심사자에게
  노출되지 않음.

## 6단계 Expertise

**심사자 배정에 직접 쓰임.** 여기 적은 것과 비슷한 논문이 배정되므로 실제로 심사할 수 있는
주제만 넣을 것.

한 줄이 하나의 교집합임. 예시가 폼에 있음.

```
topic models, social network analysis, computational social science
deep learning, RNNs, dependency parsing
```

즉 한 줄에 관련 있는 키워드 3~5개를 쉼표로 묶고, 서로 다른 관심 영역은 줄을 나눔.
줄마다 Start와 End 연도를 넣되 **지금도 하는 분야면 End를 비울 것.**

- 줄이 많을수록 다양한 논문이 배정됨. 심사 부담을 줄이려면 세 줄 정도로 좁힐 것.
- **심사하고 싶지 않은 주제는 넣지 말 것.**
- 이번에 내는 논문의 주제는 반드시 한 줄에 포함할 것.

## 등록 전에 모아 둘 것

각자 아래를 미리 채워 두면 폼 작성이 빠름.

| 항목 | 내 값 |
|---|---|
| 가입 이메일 | |
| 이름과 이메일이 함께 보이는 URL | |
| ORCID | |
| Google Scholar | |
| LinkedIn | |
| Semantic Scholar | |
| 현재 소속 기관명(영문) | |
| 현재 소속 도메인 | |
| 부서명(영문) | |
| 현재 직위 시작 연도 | |
| Expertise 3~6줄 | |

**ORCID가 없으면 먼저 만들 것**(https://orcid.org). 논문 투고 시스템에서 계속 요구함.

## 참고

- ML4H 2026 Call for Participation: https://ml4h.ahli.cc/submit/call-for-papers/
- ML4H 2026 FAQ: https://ml4h.ahli.cc/resources/faqs/
- 관련 카드: BIOP01-89(BIOP01 ML4H 투고), BIOP02-115·BIOP02-137(BIOP02 ML4H 투고)
