# 하네스 개선 (성능 + 구조 정리) + 교차 크리틱 요청서

> 작성: 2026-06-13 (kkkim-paper-agent branch).
> 배경: Week 13 스터디(2026-06-12) 상준님과의 하네스 논의 (폴더 구조 정리 + 교차 크리틱 요청).
> 목적: ① 상세 분석 30분+ 소요의 주 병목인 **그림 크롭**을 근거 기반으로 진단, ② 즉효 개선(numpy 벡터화)을 실제 구현, ③ **하네스 폴더 이중화 정리**(skills/ vs .claude/skills) 결정·구현, ④ 박상준 교차 크리틱에 **성능·구조 양쪽 + 다른 관점까지** 요청하기 위한 context.

---

## 1. 진단 — 그림 크롭이 느린 이유 (영향 큰 순)

대상 코드: `skills/core-figure/scripts/extract_panels.py`, 플로우: `skills/core-figure/SKILL.md`.

### B. 에이전트 왕복 루프 = 30분의 주범 (구조적)
`SKILL.md`의 검증된 패턴이 Figure **한 장씩** 다음을 반복한다:
> auto 실행 → `*_debug.png` 눈으로 확인 → red box 틀리면 manual JSON spec을 손으로 작성 → 재실행 → 재확인

LLM이 debug 이미지를 보고 panel bbox를 눈대중으로 정해 JSON을 쓰고 재실행하는 왕복이 "한 땀 한 땀"의 정체다. auto가 틀리는 figure(예: MultiVelo Figure 1, schematic 내부 여백)는 교정 사이클이 1~2회 더 붙는다. **연산이 아니라 사람/LLM-in-the-loop가 wall-clock의 대부분.**

### A. 파이썬 픽셀 루프 = 호출당 수~수십 초 (연산) — ✅ 해결함
스크립트에 순수 파이썬 픽셀 이중 루프가 있었다:
- `ink_bbox`: 전체 픽셀 순회 `for y: for x: pix[x,y]`.
- `projection`: 픽셀 이중 루프 + 매 호출 `convert("L")` 재실행. `best_split`→`split_panels`가 박스마다 반복 호출 → 멀티패널 1장에 수십 회.
- `--dpi 300`으로 기하 분석까지 고해상도 수행(gutter 위치 찾는 데 8MP 불필요).
- `render_page`가 호출마다 `fitz.open`+렌더 → 같은 페이지 figure 여러 개면 재렌더 반복.

### C. 전 파이프라인에 fast path 부재 (구조적)
상세 모드는 core-problem/methods/results/figure/table + lens 2종 + brief를 8단계 순차 실행하고, `AGENTS.md` Quick Start가 **HTML 생성 default on**이라 빠른 스크리닝에도 figure 크롭이 강제로 끌려 들어온다. 모든 paper가 풀비용을 낸다.

---

## 2. 구현한 것 — A 병목(픽셀 루프) numpy 벡터화 ✅

`ink_bbox`/`projection`을 PIL 픽셀 루프에서 numpy 불리언 마스크 연산으로 교체. grayscale 배열을 figure당 1회만 만들어 `split_panels`까지 재사용.

- `ink_bbox(gray)`: `mask = gray < threshold` 후 `mask.any(axis=0/1)` + `np.flatnonzero`로 경계 산출.
- `projection(gray, box, axis)`: `sub.sum(axis=0|1)`.
- `best_split`/`split_panels`/`main`이 PIL 이미지 대신 사전계산된 gray 배열을 전달.
- 의존성에 `numpy` 추가(lazy import 패턴 유지).

### 측정 (파리티 + 속도)
파리티: 무작위 이미지 6종 + blank edge case에서 old(픽셀루프) vs new(numpy) 출력 **완전 동일**.

| 함수 | old | new | 배속 |
|---|---|---|---|
| `ink_bbox` (1500²) | 2458.9 ms | 1.04 ms | **2368×** |
| `projection` (1500²) | 458.9 ms | 3.19 ms | **144×** |

`split_panels`가 `projection`을 figure당 수십 회 호출하므로 실제 이득은 더 누적. 실제 PDF(`nomura-2024-mmvelo` p.3) 전체 페이지 auto-mode end-to-end: **6.9s** (이제 PDF 렌더 + PNG 저장 I/O가 지배, 분석 연산은 ms). 동일 작업이 구버전에선 ink_bbox만 페이지 크기(8MP)에서 ~13s + projection 반복 → 30~60s+ 규모였다.

> 검증 스크립트: `/tmp/bench_panels.py` (비커밋). old 로직을 그대로 복사해 new와 대조 + 타이밍.

---

## 3. 아직 안 한 것 — 제안 (우선순위)

**즉효·구조적 (가장 큰 wall-clock 절감):**
- **B-2 크롭/분석 분리**: core-figure의 *텍스트 분석*(왜 필요/패널 비교)은 PNG 크롭이 불필요. 크롭은 HTML·slide용. → 크롭을 default 경로에서 빼고 on-demand로.
- **C fast/상세 프로필 공식화**: fast = abstract + core 텍스트 + lens(크롭·HTML 없음, 수 분) / detailed = 풀 + 크롭 + HTML(30분은 의도된 깊은 경로).
- **C 타이밍 계측**: skill/스크립트를 timestamp로 감싸 `artifacts/`에 작업별 소요 로그 → 무엇을 자를지 데이터로 결정.

**중기:**
- **B-1 PDF 네이티브 bbox**: `page.get_images`/`get_image_bbox`(임베드 raster 정확한 bbox), `get_drawings`(벡터 패널 경계), `get_text("dict")` 블록으로 눈대중 bbox 대체 → 교정 사이클 ↓.
- **B-3 배치**: figure별 interactive 재실행 대신 spec 한 번에 모아 1패스.
- **A-2/A-3 (이제 낮은 우선순위)**: 벡터화로 연산은 ms가 됐으나 6.9s의 잔여는 300 DPI 렌더 + PNG I/O. 기하 분석만 저해상도(~100 DPI)에서, 최종 크롭만 고해상도 + 페이지 pixmap 캐시로 더 줄일 수 있음.

---

## 4. 하네스 폴더 구조 정리 (skills/ 이중화) ✅

**배경**: 코덱스(루트 `skills/`) ↔ 클로드(`.claude/skills`)를 오가며 skill 폴더가 이중화됨. 상준님과의 논의에서 정리 필요성이 제기되어 방향을 검토.

**진단 (git + 파일 실태):**
- **root `skills/` = 실제 활성 source**(편집 커밋 다수). `.claude/skills` = 포팅 때 **1회 복사된 사본**.
- `.claude/skills`는 **불완전 사본** — `scripts/`(extract_panels / build_html / build_index / fetch_sources / share_paper)가 통째 누락. → 루트 삭제 시 하네스 붕괴(web Render HTML·인덱스·크롭·fetch 전부).
- **Codex 실가동**: `web/app.py` 기본 엔진=codex. Codex는 루트 `AGENTS.md`+`skills/`만 읽고 `.claude/`는 못 봄. 비용 백업(Claude Max 중단 시 Codex 메인 승격) + 교차 크리틱용으로 **유지 결정**.

**결정·구현 (B안):** root `skills/` = 유일 source 유지, `.claude/skills` = 파생 mirror. `scripts/sync-skills.sh`(rsync 기반, `--check`로 drift 검사) 추가 + 누락 스크립트 6개 동기화 완료. 심볼릭(A안)은 claude.ai/code 웹이 symlink로 skill을 discover하는지 미검증이라 보류 — 검증되면 중복 완전 제거 위해 전환.

> 논의에서 거론된 "통합" 방향과는 결론이 다르다(통합 X, 루트가 source). 목표(이중화 해소)는 동일. 이 판단이 맞는지도 크리틱 대상(§5).

## 5. 교차 크리틱 요청 — 박상준 (성능·구조 + 다른 관점 환영)

개선본(이 문서 + 벡터화 + 구조 정리 커밋)을 대상으로 본인 에이전트로 크리틱을 돌려주세요. **내가 짚은 진단/결정에 동의하는지뿐 아니라, 내가 놓친 다른 관점도 같이** 봐주면 좋겠습니다.

### 성능 / 그림 크롭
1. **벡터화 정합성**: numpy 치환이 정말 출력 불변인가? 파리티 테스트(무작위 6 + blank)가 충분한가, 놓친 edge case(임계값 경계, 빈 projection, 단일 픽셀 ink)는?
2. **병목 진단의 타당성**: 30분의 주범이 정말 B(왕복)인가, 아니면 다른 단계(core-methods 등 LLM 생성, PDF 텍스트 추출, HTML 빌드)가 더 큰가? 측정 없이 단정한 부분 지적.
3. **대안 아키텍처**: 그림 크롭 자체를 다르게 풀 길(출판사 figure 원본 다운로드, vector 추출, VLM 기반 panel 검출)이 픽셀 heuristic + 수동 spec보다 나은가?
4. **fast/상세 분리의 경계**: 어디까지 fast에 넣어야 "쓸모 있는 빠른 버전"인가? 크롭을 빼면 품질 손실은 어디서 나는가?

### 구조 / 폴더 정리
5. **방향 자체**: "root=source, `.claude`=mirror(B)"가 맞나, 아니면 `.claude`로 통합하는 편이 더 나은가? Codex를 정말 유지할 가치가 있나(백업+교차크리틱 효용 vs 이중 컨벤션 유지비)?
6. **mirror 방식**: copy+sync 훅(B) vs symlink(A) — claude.ai/code 웹이 symlink로 skill을 discover하는지 검증할 방법이 있나? pre-commit 훅으로 drift 막는 게 충분한가?
7. **sync 스크립트 위험**: `scripts/sync-skills.sh`의 `rsync --delete` + checksum `--check` 설계에 위험은 없나(의도치 않은 삭제, `.claude` 안 openai.yaml 중복 포함 등)?

### 공통
8. **평가 기준**: 아웃풋 품질 외에 **소요 시간·비용**을 에이전트 평가에 어떻게 반영할지(박상준 본인 고민 주제). 작업별 timing 계측을 어떤 schema로 남기면 비교가 쉬운가?
9. **그 외**: 내가 전혀 안 본 각도 — 정확성/재현성/유지보수성/source-grounding 위반 가능성 등 무엇이든.

피드백 방식 자유(브랜치 코멘트, 별도 문서, 이슈 등). 이 문서 자체에 대한 반박도 환영.
