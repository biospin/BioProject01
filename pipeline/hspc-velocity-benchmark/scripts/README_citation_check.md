# 참고문헌 검증 도구 사용법

논문 참고문헌이 실제로 존재하는지, 저자와 연도가 맞는지 확인하는 도구다. BioProject02에서 만들어 이곳으로 옮겨왔다(2026-07-18). 두 프로젝트가 같은 도구를 쓴다.

## 왜 쓰나

존재하지 않는 논문을 인용하거나 저자·연도를 잘못 적는 사고를 논문 내기 전에 막으려는 것이다. 실제로 최근 다른 문서에서 존재하지 않는 논문("Williams 2022")을 인용한 적이 있었고, 그럴듯한 서지 정보만 보고 진짜인 줄 알았던 것이 원인이었다. 이 도구는 CrossRef와 PubMed에 실제로 조회해 대조한다.

## 쓰는 법

참고문헌 파일(`manuscript/refs.bib`)을 두 단계로 검증한다. 먼저 `.bib`를 도구가 읽는 형식으로 바꾸고, 그다음 검증한다.

```bash
python3 scripts/bib_to_cites.py manuscript/refs.bib > /tmp/cites.json
python3 scripts/verify_citations.py /tmp/cites.json --json /tmp/verdict.json
```

## 판정이 뜻하는 것

각 인용에 다음 중 하나가 붙는다.

- **VERIFIED** — 저자·연도가 확인됐다. 통과.
- **AUTHOR_MISMATCH** / **YEAR_MISMATCH** — 논문은 있는데 적어둔 저자나 연도가 다르다.
- **NOT_FOUND** — 조회로 찾지 못했다. 존재하지 않는 논문일 수 있으니 사람이 직접 확인해야 한다.
- **CLAIM_UNSUPPORTED** — 인용에 딸린 수치·주장이 초록에서 뒷받침되지 않는다.
- **NEEDS_HUMAN** — 정보가 모자라 도구가 판단하지 못했다.

**중요한 것 하나.** VERIFIED가 아닌 것이 곧 "가짜 인용"은 아니다. DOI가 없거나 저자 필드가 비어 있으면 도구가 조회를 못 해 NOT_FOUND나 NEEDS_HUMAN을 낸다. 그래서 통과 여부는 사람이 판단한다. 도구가 자동으로 "이상 없음" 도장을 찍게 두지 않는다.

## 2026-07-18 첫 검증에서 나온 것

`manuscript/refs.bib` 19편을 돌린 결과, 10편은 확인됐고 나머지에서 손볼 것이 나왔다. 특히 네 편은 원본 `.bib`에 저자 필드가 아예 없었다. `ArchVelo`, RNA velocity 벤치마크 두 편, `BayVel`이며, 모두 저자 확인이 아직 안 된 항목으로 note가 붙어 있다. 논문에 넣기 전 저자를 채워야 한다. 그 밖에 DOI가 없거나 연도 대조가 필요한 것이 다섯 편 있었다.
