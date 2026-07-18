# scvi-tools — BIOP01 활성화 가이드 (우리 작성, 원본 SKILL.md 복사 아님)

**활성화됨(2026-07-18)**: `velo-torch` env에 `scvi-tools 1.3.3` 설치·검증 완료.
smoke-test: MULTIVI·PEAKVI·SCVI·VELOVI 전부 import 성공.

## BIOP01에서 왜 유용한가 (우리 스택 직결)
- **MULTIVI** — 10x Multiome RNA+ATAC 공동 잠재공간. 우리 벤치마크의 multiome 입력에 직접.
- **VELOVI** (`scvi.external`) — 확률적 RNA velocity. 우리 velocity arm(MultiVeloVAE)과 계보 인접 → cross-method 벤치마크에 arm 추가 후보.
- **PEAKVI** — ATAC 전용 잠재공간(peak). day0 ATAC feature 인코딩 대안.
- **SCVI/scANVI** — 배치보정·라벨전이(day0/day7 통합에 참고).

## 실행 (velo-torch)
```bash
conda run --no-capture-output -n velo-torch python -c "from scvi.model import MULTIVI; ..."
```

## 규율 (중요)
- 산출물은 **우리 검증 게이트 뒤**: 결정론 재계산·permutation FDR·bootstrap·Critic 통과 후 채택.
- 새 velocity arm으로 VELOVI를 넣으면 **cross-method 정의 정합**(lag/α 자 통일) 필수 — p3_concordance 계약 준수.
- 원본 SKILL.md(anthropics/life-sciences)는 **라이선스 미지정**이라 복사 안 함. 이 문서는 우리가 작성. 업스트림은 SOURCE.md URL 참조.
