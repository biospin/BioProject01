# Index

`build_index.py`가 자동 생성하는 디렉토리입니다. **직접 편집하지 마세요.**

## 파일

- `papers.csv` — 모든 분석된 자료의 통합 표. Excel/Numbers/Google Sheets에서 정렬·필터.
- `<topic>.md` — topic별 markdown 목록. *primary topic*과 *secondary topic*으로 등록된 자료를 분리.

## 갱신

paper-info.yaml이 변경되었거나 새 자료가 추가되었으면 다음을 실행:

```bash
python3 skills/source-grounding/scripts/build_index.py
```

옵션:
- `--topic <name>` — 특정 topic만 다시 빌드
- `--csv-only` — papers.csv만 갱신
- `--verbose` — 처리 중인 yaml 경로 출력
