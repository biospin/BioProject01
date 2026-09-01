# 재현 가능한 연구로: 분석을 하네스로 옮기기

> 한 줄 요약: 좋은 분석은 결과만으로는 부족하다. 다른 사람이, 또는 자동으로 실행하는 프로그램이 같은 절차를 그대로 다시 돌릴 수 있어야 한다. 그러려면 무엇을 할지 적은 지침과 그것을 돌리는 코드를 갈라 둔다. 이 틀은 박상준 님(@poqopo)이 만든 Harness_Baseline을 반입해 우리 파이프라인에 맞춘 것이고, 실행은 OpenClaw 기반으로 연습하는 중이다.

앞 세 글에서는 결과를 다뤘다. 전사 속도(α)는 계산 프로그램을 바꿔도 값이 일정했고, DNA가 열리고 나서 유전자가 켜지기까지의 시간차(lag)는 프로그램을 바꾸면 재현되지 않았으며, 이 순서가 다른 조직·다른 종에서도 되풀이됐다. 이번 글은 결과에서 한 걸음 물러나, 그 결과를 낸 절차를 다룬다. 반년 뒤의 나 또는 옆자리 동료가 같은 분석을 그대로 다시 돌리려면 무엇이 갖춰져 있어야 하는가. 이 물음에 답하려고 분석 절차를 하네스(harness)라는 틀에 옮겨 담았다.

## 핵심 개념: 지침과 코드의 분리

폴더를 열고 예전 명령을 똑같이 다시 입력했는데 아무것도 돌지 않는 상황을 떠올려 보자. 무엇을 어느 자리에 어떤 순서로 넣어야 하는지가 처음 짠 사람 머릿속에만 있으면 이렇게 된다. 그래서 좋은 분석은 결과만 좋아서는 오래가지 못한다. 다른 사람이 같은 절차를 되짚어 돌릴 수 있어야 쓸모가 남는다.

분석을 다시 돌게 만들려면 늘 붙어 다니던 두 가지, 곧 무엇을 할지 적은 지침과 그것을 실제로 돌리는 코드를 갈라 두면 된다. 둘이 붙어 있으면 처음 짠 사람만 분석을 다시 돌릴 수 있다. 갈라 두면 데이터와 작업 이름만 대도 같은 절차를 다시 돌릴 수 있다.

조리법에 빗대면 이렇다. 조리법이 한 장의 종이에 적혀 있고 재료와 도구가 정해진 자리에 있으면, 요리사가 바뀌어도 같은 음식이 나온다. 조리법이 한 사람 머릿속에만 있으면, 그가 자리를 비운 날엔 아무도 그 음식을 못 만든다. 종이에 적힌 조리법이 지침이고, 재료와 화구가 갖춰진 주방이 코드다. 이렇게 지침과 코드를 갈라 감싼 틀을 하네스라 부른다.

![재현 가능 하네스 개념도: 지침(무엇: SKILL.md·ROUTES·dataset→task)과 코드(어떻게: scripts/)를 갈라 두면, dataset과 task 이름만으로 같은 절차를 사람 또는 OpenClaw가 다시 돌릴 수 있다.](../pipeline/hspc-velocity-benchmark/figures/fig04_harness_concept.png)

## 배경: 남이 만든 틀을 반입

이 틀을 백지에서 짜지는 않았다. 박상준 님(@poqopo)이 만든 Harness_Baseline이라는 틀을 반입해 우리 파이프라인에 맞게 고쳤다. 잘 다듬어진 조리법 서식을 얻어다 우리 재료에 맞추는 방식이다. 원저작자는 박상준 님이고, 원 저장소에 라이선스 표기가 없어 공유·수정은 박상준 님의 동의를 전제로 한다. 이 출처와 조건은 반입한 문서 머리에 그대로 적어 두었다.

## 구조: 데이터 4종 × 작업 4단계

하네스는 격자로 짜여 있다. 데이터 네 종류를 저마다 같은 네 단계 작업으로 돌리는 얼개다.

데이터는 네 종류다. 생쥐 배아 뇌(10x-embryonic-mouse-brain), 생쥐 피부(share-seq-mouse-skin), 사람 뇌(human-brain-multiome), 그리고 우리가 주로 쓰는 사람 조혈세포(human-hspc-10x-multiome)다. 작업은 네 단계로, 내려받기(download) → 데이터 다듬기(preprocessing) → 값 계산(model) → 그림 그리기(visualization) 순서다. 지금 우리가 맡아 돌리는 칸은 사람 조혈세포다.

이 격자를 네 종류의 파일이 받친다.

- **AGENTS.md**: 프로젝트 전체 틀(project frame). 무슨 분석인지, lag을 어떻게 정의하는지, 어떤 baseline feature와 참고 방법을 쓰는지 적는다.
- **skills/ROUTES.md**: 데이터에서 작업으로 가는 안내도. 어떤 데이터의 어떤 작업을 부르면 그에 맞는 지침 파일로 이어 준다.
- **skills/&lt;데이터&gt;/&lt;작업&gt;/SKILL.md**: 작업 하나하나의 지침.
- **agents/openai.yaml**: 그 작업을 자동으로 실행할 때 필요한 설정.

```
AGENTS.md  (프로젝트 틀)
    │
ROUTES.md  (데이터 → 작업 라우팅)
    │
  데이터 4종                작업 4단계 (각 데이터마다)
  · 생쥐 배아 뇌            1. 내려받기   download
  · 생쥐 피부              2. 다듬기     preprocessing
  · 사람 뇌                3. 값 계산    model
  · 사람 조혈세포 ★         4. 그림      visualization
       (active)
    │
  칸마다: SKILL.md (지침) + openai.yaml (설정)
    │
  pipeline/hspc-velocity-benchmark/  (실제 코드)
```

이 형식은 OpenClaw와 Codex라는 실행 도구가 그대로 읽어 들이고, 우리가 평소 쓰는 Claude Code에서도 돈다. 지침이 가리키는 실제 코드는 파이프라인 폴더(`pipeline/hspc-velocity-benchmark/`)에 있다. 사람 조혈세포의 내려받기·다듬기 단계가 여기 스크립트로 구현돼 있고, 값 계산 단계는 앞 세 글에서 다룬 velocity 방법 벤치마크로 이어진다.

## 한계: 출처와 실행 연습

두 가지를 짚어 둔다. 하나는 출처다. 이 틀은 박상준 님의 Harness_Baseline에서 왔고, 원 저장소에 라이선스가 없어 공유·수정에는 원저작자의 동의가 필요하다. 코드의 최종 위치는 박상준 님과 협의할 몫으로 남겨 두었다.

**셋째는 게이트 자체다(2026-08 덧붙임).** 이 글은 "요리사가 바뀌어도 같은 음식이 나온다"는 비유로 하네스를 소개하는데, 게이트가 붙어 있다는 사실과 그 게이트가 실제로 결함을 잡는다는 사실은 다르다. 이 하네스를 다른 프로젝트로 옮겨 심으면서 일부러 결함을 심어 검사해 봤더니(mutation 검사), 구멍이 세 건 나왔다 — 검사할 행이 0개여도 "통과"로 찍히는 공허 통과, 증거가 하나도 없는 7개 항목이 그대로 pass로 넘어가던 경로 등. 전부 막았지만, 교훈은 그 세 건이 아니라 이것이다: **게이트를 붙였다는 것만으로는 아무것도 보장되지 않고, 그 게이트가 진짜 결함을 잡는지를 따로 검사해야 한다.** 조리법이 종이에 적혀 있어도, 그 조리법이 맞는지는 따로 확인해야 하는 것과 같다.

다른 하나는 실행이다. 우리는 이 하네스를 OpenClaw로 돌리는 것을 기본으로 삼고 연습하는 중이다. 형식과 구조가 OpenClaw가 읽을 수 있는 유효한 형태인지는 실제로 돌려서 확인했다. 다만 값을 끝까지 계산하는 단계는 아직 이 환경에서 완주하지 못했다. OpenClaw 같은 실행 도구가 AI 모델을 부르려면 인증 키가 필요한데, 이 환경엔 그 키가 아직 없다. 이는 실행 환경에서 비롯한 문제이고, 틀 자체의 문제는 아니다. 어디까지 되고 어디서 왜 막혔는지를 갈라 적어 두어야, 다음에 이 기록을 보는 사람이 온전한 틀을 처음부터 다시 손대지 않아도 된다.

## 확장: 하네스에서 루프와 메모리로 (2026-07-12 덧붙임)

여기까지가 하네스였다. 분석을 다시 돌릴 수 있게 지침과 코드를 갈라 감싼 틀. 그 위에 한 층이 더 있다. 요즘 루프 엔지니어링(loop engineering)이라 부르는 것으로, 하네스가 "에이전트에 어떤 환경이 필요한가"를 묻는다면 루프는 "무엇이 그 에이전트를 목표를 향해 계속 돌게 하고, 언제 멈추는가"를 묻는다. 한 번의 지시가 요청이라면, 루프는 정책에 가깝다 — 새벽 세 시에도 돌고, 내가 자리를 비운 사이에도 돌며, 한 바퀴 돌 때마다 배운 것을 적어 다음 바퀴가 조금 나아지는.

우리 프로젝트에서 이 루프가 어느 날 밤 두 번, 스스로 자기 실수를 잡았다. 둘은 같은 얼굴이었다. 확인하지 않은 "완료".

첫째는 데이터를 내려받는 일에서 나왔다. 여덟 덩어리를 순서대로 받는 프로그램이었는데, 도중에 여섯 덩어리가 네트워크 문제로 조용히 실패했다. 그런데도 프로그램은 그걸 "완료"라 적고 다음 단계로 넘어가 버렸다. 돌지도 않은 시험을 통과했다고 스스로 보고한 셈이다. 이럴 때 필요한 건 그 보고를 믿지 않는 별도의 검증자다. 그래서 여덟 덩어리가 실제로 파일로 존재하고 받다 만 흔적이 없는지를 기계적으로 확인하는 관문을 세웠다. 하나라도 빠지면 완료 표시를 아예 만들지 않고 멈추고, 다시 돌리면 받다 만 것만 이어받는다.

둘째는 논문의 주장에서 나왔다. 앞 글들에서 우리는 시간차(lag)가 계산 프로그램을 바꾸면 재현되지 않는다는 결과를 얻었다. 논문의 차별점을 세우는 역할을 맡은 부분이 이 결과를 한 단계 끌어올리자고 제안했다 — "lag는 그냥 재현이 안 되는 게 아니라, 데이터로부터 애초에 결정되지 않는 양이다"라는 원리로 격상하자는 것이었다. 이름을 바꾸면 같은 결과가 더 높은 급으로 읽힌다. 매력적인 제안이었다. 그래서 더 위험했다. 매력적인 주장일수록 검증 없이 굳히면 논문 전체가 그 위에 얹히니까.

그래서 같은 종류의 관문을 통과하게 했다. 어떤 중심 주장도 본문에 들어가기 전에, 그 주장을 죽일 수 있는 가장 값싼 검정을 먼저 견뎌야 한다. 여기서 검정은 이랬다 — 그 "결정되지 않음"을 재는 지표가 재현성을 예측하긴 하는데, 더 단순한 설명인 "그냥 신호가 약해서"를 걷어내고도 여전히 예측하는가. 기존 데이터로 확인했더니, 그 지표의 예측력은 신호 세기를 통제하자 절반 아래로 무너졌고, 둘은 사실상 같은 것을 가리키고 있었다. 격상된 주장은 이미 아는 사실과 구별되지 않았다. 그래서 그 강한 주장은 버리고, 방어할 수 있는 선까지만 남긴 뒤, 그 판정을 방향 문서에 적어 다음에 같은 유혹이 와도 이미 접었음을 알게 했다.

두 사건의 교훈은 하나로 모인다. 만드는 눈과 검증하는 눈은 달라야 한다. 만든 쪽은 자기 과정을 보지만, 검증하는 쪽은 결과물과 기준만 본다. 같은 눈이 자기 것을 채점하면 "괜찮아 보인다"가 "괜찮다"를 이겨, 돌지도 않은 시험도 그럴듯한 과장도 통과한다. 눈을 갈라 두어야 걸린다.

그리고 이 검증이 성립하려면 앞에 반드시 하나가 있어야 한다. 목표다. 됐는지 안 됐는지를 기계가 판정할 수 있는 목표. "테스트를 통과시켜라"는 판정되고, "코드를 개선해라"는 판정되지 않는다. 판정할 수 없는 목표는 결국 자기보고로 되돌아간다. 그래서 우리 목표는 셀 수 있게 적었다 — 여덟 덩어리 완결, 그리고 어떤 주장이든 자기를 죽일 검정을 견딜 것.

루프에는 기억도 붙는다. 한 바퀴에서 배운 것을 적어 두어야 다음 바퀴가 같은 실수를 되풀이하지 않는다. 그런데 기억이 쌓이기만 하면 아무도 손대지 않는 잡동사니가 된다. 그래서 기억은 자리를 얻어야 오른다 — 검증된 결과만 상태 파일을 고치고, 되풀이 확인된 것만 규칙으로 굳는다. 앞서 접은 그 과장된 주장도 그냥 지우지 않고 방향 문서에 "검정으로 접음"이라 적어 두었다. 다음에 같은 유혹이 와도 시스템이 이미 안다. "완료"라는 표시조차 코드를 다 짰을 때가 아니라 끝까지 돌려 확인했을 때만 찍는다 — 데이터의 여덟 덩어리 완결 관문과 주장의 검정 관문은 같은 규칙의 두 적용이다.

이렇게 관찰하고, 검증하고, 복구하고, 기억하는 사이클을 설계하는 일을 요즘 루프 엔지니어링(loop engineering)이라 부른다. 새로 생긴 발상은 아니다. 되먹임 고리는 제어공학만큼 오래됐고, 근래 자율 에이전트가 강해지며 이름을 얻고 다시 뜨거워졌을 뿐이다. 우리가 한 건 그 개념을 남의 방식 그대로 옮겨 온 게 아니라 다른 길로 구현한 것이다. 이 사이클을 알아서 잘 도는 최신 모델이 있지만, 생명과학 데이터는 그 모델이 자동으로 한 급 다른 모델로 넘겨 버린다. 그래서 우리는 모델이 대신해 주기를 기다리는 대신, 보고를 믿지 않는 별도의 검증자와 작은 작업 단위, 자리를 얻어야 오르는 기억, 그리고 됐는지 기계가 판정할 수 있는 목표를 하네스에 손으로 심었다. 모델에 얹힌 능력이 아니라 틀에 박힌 규율이라, 모델이 바뀌어도 남는다. 게다가 이 규율은 책에서 베껴 온 게 아니라 그날 밤 두 번의 실수가 강제한 것이다. 필요가 만든 규율이 마침 이름 붙은 개념과 만난 셈이다.

여기서 하네스가 한 일은 앞 절들의 재현성과 결이 같다. 재현성은 절차가 처음 짠 사람의 기억에 기대지 않게 했고, 검증 관문은 결과가 만든 이나 프로그램의 보고에 기대지 않게 하며, 기억은 배움이 한 사람의 머릿속에만 갇히지 않게 한다. 셋 다 엄밀함을 사람에서 시스템으로 옮기는 한 일의 세 얼굴이다.

> ※ 초안(2026-07-12 작업 기록) — 게시 전 윤문과 사람 승인을 거친다. 루프·메모리 엔지니어링은 되먹임 고리라는 오래된 발상을 근래 공개 논의(LangChain "The Art of Loop Engineering", Ken Huang의 "Claude Fable 5" 시리즈 2·3부 등)가 다시 정리·명명한 것이다. 여기서 적은 것은 그 개념을 최신 모델에 의존하지 않고 하네스에 손으로 구현한 방식과, 그것이 우리 프로젝트의 실제 두 사례(내려받기 완료 오보, 주장 과장)로 어떻게 나타났는지다 — 개념을 우리가 처음 세웠다는 뜻은 아니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| 하네스 (harness) | 지침과 코드를 갈라 감싸, 같은 절차를 다시 돌릴 수 있게 한 틀 |
| 지침 (skill) | 어느 데이터에 어떤 작업을 어떤 순서로 돌릴지 적어 둔 문서 |
| AGENTS.md | 프로젝트 전체 틀을 적은 문서(무슨 분석·lag 정의·참고 방법) |
| ROUTES.md | 데이터에서 작업으로 이어 주는 안내도 |
| openai.yaml | 작업을 자동으로 실행할 때 필요한 설정 파일 |
| OpenClaw · Codex | 이 형식을 그대로 읽어 실행하는 자동 실행 도구 |
| 재현 (reproducibility) | 다른 사람·다른 환경에서 같은 절차를 그대로 다시 돌릴 수 있는 정도 |

## 참고

**근거 문서**: `AGENTS.md`(project frame), `skills/ROUTES.md`(데이터→작업 라우팅), `skills/human-hspc-10x-multiome/`(사람 조혈세포 4단계 지침), `pipeline/hspc-velocity-benchmark/BASELINE-ALIGNMENT.md`(Harness_Baseline 정합 기록), `skills/OPENCLAW-RUN.md`(OpenClaw 실행 점검).

**개념도**: 지침과 코드를 갈라 두는 개념도(범용 재사용 자산)는 `/workspace/skills/harness-concept/`에 독립적으로 두었다.

**원 틀**: Harness_Baseline — 박상준 님(@poqopo). 원 저장소 LICENSE 미지정(공유·수정은 원저작자 동의 전제).

---
*이 글은 진행 중인 연구의 내부 정리이며, 하네스 구조와 실행 절차는 후속 작업으로 갱신될 수 있다(연구·교육용).*

---

# From results to reproducibility: moving our analysis into a harness

> TL;DR: A good analysis needs more than good results. Someone else — or a program that runs on its own — has to be able to rerun the same procedure. That means keeping the instructions (what to do) apart from the code (that runs it). This frame was brought in from Harness_Baseline, made by 박상준 (@poqopo), and fitted to our pipeline; running it on OpenClaw is still something we are practicing.

The previous three posts were about results. The transcription rate (α) stayed stable when we changed the program, the lag between the DNA opening and the gene turning on did not reproduce across programs, and that ordering recurred in other tissues and species. This post steps back from the results to the procedure that produced them. If a colleague — or myself half a year from now — wants to rerun the same analysis, what has to be in place? To answer that, we moved the analysis procedure into a frame called a harness.

## The core idea: keeping instructions apart from code

Picture opening a folder, typing the old commands again, and nothing runs. That happens when what goes where, and in what order, lived only in the head of whoever first wrote it. So a good analysis does not last on good results alone. It lasts when someone else can retrace the same procedure.

The trick for making an analysis rerunnable is simple: keep apart two things that usually travel together. One is the instructions — what to do: a document stating which task runs on which data, in what order. The other is the code that actually runs it. Kept together, only the person who wrote it can rerun the analysis. Kept apart, naming the data and the task is enough to rerun the same procedure.

A recipe makes the point. If the recipe is on a sheet of paper and the ingredients and tools sit in their places, the same dish comes out even when the cook changes. If the recipe lives only in one person's head, no one makes that dish on the day they are away. The recipe on paper is the instructions; the kitchen stocked with ingredients and burners is the code. This split, wrapped into one frame, is what we call a harness.

![Reproducible harness: splitting instructions (WHAT: SKILL.md · ROUTES · dataset→task) from code (HOW: scripts/) lets the same procedure be re-run by name — by a person or by OpenClaw.](../pipeline/hspc-velocity-benchmark/figures/fig04_harness_concept.png)

## Background: bringing in someone else's frame

We did not build this frame from a blank page. We brought in a frame called Harness_Baseline, made by 박상준 (@poqopo), and adapted it to our pipeline — taking a well-shaped recipe template and fitting it to our own ingredients. The original author is 박상준, and since the original repository carries no license, sharing and modifying it are on the premise of his consent. That source and condition are written at the top of the imported documents.

## Structure: four datasets × four tasks

The harness is laid out as a grid: four kinds of data, each run through the same four tasks.

There are four datasets: embryonic mouse brain (10x-embryonic-mouse-brain), mouse skin (share-seq-mouse-skin), human brain (human-brain-multiome), and the human hematopoietic cells we mainly use (human-hspc-10x-multiome). The tasks are four steps: download → preprocessing → model → visualization. The cell we run right now is the human hematopoietic one.

Four kinds of file support this grid.

- **AGENTS.md**: the project frame — what the analysis is, how lag is defined, which baseline features and reference methods to use.
- **skills/ROUTES.md**: the map from data to task; naming a task on a dataset routes to the matching instruction file.
- **skills/&lt;dataset&gt;/&lt;task&gt;/SKILL.md**: the instructions for each single task.
- **agents/openai.yaml**: the settings needed to run that task automatically.

```
AGENTS.md  (project frame)
    │
ROUTES.md  (data → task routing)
    │
  4 datasets                 4 tasks (for each dataset)
  · embryonic mouse brain    1. download
  · mouse skin               2. preprocessing
  · human brain              3. model
  · human HSPC ★             4. visualization
       (active)
    │
  per cell: SKILL.md (instructions) + openai.yaml (settings)
    │
  pipeline/hspc-velocity-benchmark/  (the actual code)
```

This format is read directly by the OpenClaw and Codex runners, and it also runs in the Claude Code we use day to day. The actual code the instructions point to sits in the pipeline folder (`pipeline/hspc-velocity-benchmark/`). The download and preprocessing steps for the human hematopoietic cells are implemented there as scripts, and the model step continues into the velocity-method benchmark covered in the previous three posts.

## Limits: source, and a run still in practice

Two things to state plainly. One is the source. This frame came from 박상준's Harness_Baseline, and with no license on the original repository, sharing and modifying it need the original author's consent. Where the code finally lives is left to settle with 박상준.

**Third, the gates themselves (added 2026-08).** This post introduces the harness with the image of "the same dish comes out even when the cook changes" — but having gates and having gates that catch real defects are two different things. Porting this harness to another project, we planted defects deliberately to test it (mutation testing) and found three holes: a gate reporting "pass" with zero rows to check, a path where seven items with no evidence at all still came through as passing, and one more of the same kind. All are closed now, but the lesson is not those three. It is this: **attaching a gate guarantees nothing on its own; whether the gate catches real defects has to be tested separately.** The recipe being written down does not make the recipe correct.

The other is running it. We take running this harness on OpenClaw as the default and are practicing it. That the format and structure are valid in a form OpenClaw can read, we confirmed by actually running it. But the step that computes values to the end has not yet finished in this environment, because the authentication key for the AI model the runner calls is not set up here. This is a matter of the run environment, not a flaw in the frame. Writing down separately how far it got and where and why it stopped is what spares the next person who reads this from rebuilding a sound frame from scratch.

## Glossary

| Term | Meaning |
|---|---|
| harness | A frame that keeps instructions and code apart, wrapping them so the same procedure can be rerun |
| skill (instructions) | A document stating which task runs on which data, in what order |
| AGENTS.md | The document that states the project frame (what analysis, lag definition, reference methods) |
| ROUTES.md | The map that routes from data to task |
| openai.yaml | The settings file needed to run a task automatically |
| OpenClaw · Codex | Runners that read this format directly and execute it |
| reproducibility | The degree to which the same procedure can be rerun by another person or in another environment |

## References

**Source documents**: `AGENTS.md` (project frame), `skills/ROUTES.md` (data→task routing), `skills/human-hspc-10x-multiome/` (four-step instructions for the human hematopoietic cells), `pipeline/hspc-velocity-benchmark/BASELINE-ALIGNMENT.md` (Harness_Baseline alignment record), `skills/OPENCLAW-RUN.md` (OpenClaw run check).

**Concept diagram**: the instructions-vs-code diagram (a cross-project reusable asset) is kept separately at `/workspace/skills/harness-concept/`.

**Original frame**: Harness_Baseline — 박상준 (@poqopo). No LICENSE on the original repository (sharing and modifying on the premise of the original author's consent).

---
*Internal working note from ongoing research; the harness structure and run procedure may be updated by later work (research and educational use).*
