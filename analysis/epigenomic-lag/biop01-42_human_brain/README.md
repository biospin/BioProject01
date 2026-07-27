# BIOP01-42 human_brain velocity to alpha (sjpark)

GSE162170 발달 대뇌피질 alpha 분석. target=alpha(lag 아님). supporting 결과(새 헤드라인 아님).
정본 결론/정정/논문정합 = BIOP01-42_phase1_findings.md (v2, self-review 반영).

- scripts/ : 전처리 -> alpha(scVelo) -> baseline ATAC->alpha -> cross-dataset -> MultiVeloVAE -> self-review
- results/ : 결과 JSON. 대용량 h5ad/csv/임베딩은 /workspace/data/cache/biop01/human_brain_GSE162170/ (미커밋)
- 핵심: alpha cross-dataset 재현(+0.3~0.5, 4 method, categorical supporting/n=3 confounded); baseline->alpha는 발현 confound(기전주장 불가); lag 미검정
