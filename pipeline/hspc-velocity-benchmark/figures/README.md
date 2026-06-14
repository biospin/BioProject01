# figures/ — 논문 그림 (생성 스크립트 tracked, 출력 이미지 ignored)

그림은 **재현 가능한 스크립트**로 만든다. 그림 파일(png/pdf)은 commit하지 않고, **스크립트만** commit해 `data/processed/` + `results/`로부터 언제든 재생성한다.

## 규칙
- 스크립트: `figNN_<slug>.py` (예: `fig01_umap_lineage.py`) — **tracked**.
- 출력: `figNN_<slug>.{png,pdf,svg}` — **ignored** (`.gitignore`).
- 각 스크립트는 입력(processed 객체/results csv)과 출력 경로를 파일 상단에 명시.

## 재생성
```bash
conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/figures/figNN_<slug>.py
```

## manuscript 연결
파일명 `figNN`을 `manuscript/`의 Figure 번호와 일치시킨다. legend는 `manuscript/figure-legends.md`.
