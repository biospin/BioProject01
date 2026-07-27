# 출처 (vendored, MIT)
- 저장소: GPTomics/bioSkills — https://github.com/GPTomics/bioSkills
- 라이선스: **MIT** (LICENSE 동봉)
- 반입 스킬: `atac-seq/enhancer-gene-linking`, `atac-seq/atac-qc` (원본 경로 그대로)
- 반입일: 2026-07-15 (raw.githubusercontent.com/GPTomics/bioSkills/main/...)
- 반입 이유: BIOP01 10x Multiome ATAC 처리 — 특히 **enhancer-gene-linking**은 우리 peak→gene 집계(gene body ±10kb)와 직결.

## ⚠️ 적응 필요 (활성 사용 전)
- 우리 conda env(`scv-preprocess`/`velo-mv`)에 맞게 도구·경로 확인. 원본 스킬의 도구 가정(macs2·ArchR 등)이 우리 스택에 있는지 검증.
- **우리 검증 게이트 뒤에 둔다**: 스킬 산출물은 결정론 재계산·permutation FDR·Critic 통과 후 채택(자동 PASS 신뢰 금지).
- 미적응 원본 = 참고용. 활성 skills/로 승격 전 smoke-test 필수.

## 상태: 참고 보류 (2026-07-18)
스킬 의존 도구가 cicero·signac(R)·deeptools·bedtools·macs로 우리 velo env 밖. 우리 peak→gene은 gencode gene-body ±10kb 집계(다른 접근)라, 이 스킬은 **참고용**(활성화하려면 R/CLI 도구 별도 설치·검증 필요).
