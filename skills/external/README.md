# skills/external — 외부 참고 스킬 (vendored / pointer)
BIOP02 벤치마킹 흐름에 따라 반입한 외부 Agent Skills. **활성 스킬 아님** — 우리 conda env 적응 + 검증 게이트 통과 후에만 실제 사용.

| 스킬 | 출처 | 라이선스 | 형태 | BIOP01 용도 |
|---|---|---|---|---|
| atac-seq/enhancer-gene-linking | GPTomics/bioSkills | MIT | 복사 | peak→gene 집계 직결 |
| atac-seq/atac-qc | GPTomics/bioSkills | MIT | 복사 | ATAC QC |
| scvi-tools | anthropics/life-sciences | 미지정 | 포인터 | MultiVI/veloVI(우리 VAE arm 인접) |

규율: 자동 PASS 신뢰 금지. 스킬 카탈로그의 "있다" 주장도 SKILL.md 실측 후 도입(K-Dense scVelo confab 전례).
