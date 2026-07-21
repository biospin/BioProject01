# Docker 운용 검토 — BIOP01 HSPC velocity benchmark

> 최초 작성: 2026-06-15 (BIOP01-22). **2026-06-30 서버 확인 후 전면 업데이트.**

---

## 현재 서버 스펙 확인 결과 (2026-06-30)

| 항목 | 현재 | BIOP01 요구사항 |
|---|---|---|
| CPU | AMD Threadripper PRO 3955WX 32코어 | MultiVelo 6-job 병렬 ✅ |
| RAM | **503GB** | 권장 128GB → 4배 여유 ✅ |
| GPU | **RTX A6000 ×3 (VRAM 48GB 각)** | DL arm 8-24GB 권장 → 6배 여유 ✅ |
| 디스크 | 6.4TB 여유 | 중간산출물 ~200-500GB ✅ |

**→ 모든 BIOP01 작업을 현재 서버에서 수행 가능. 외부 서버 불필요.**

---

## 현재 서버 Docker 설치 가능 여부

- Docker: **미설치**
- `sudo` 권한: **차단됨** (`no new privileges` 플래그 — 격리 환경)
- Podman / Singularity: 미설치
- **→ 관리자 없이 설치 불가**

관리자에게 요청할 명령 (필요 시):
```bash
apt install -y docker.io nvidia-container-toolkit
usermod -aG docker kkkim
systemctl restart docker
```

---

## Docker 이점 평가 — 이 프로젝트 맥락

| Docker 이점 | 이 프로젝트 실제 필요? | 판단 |
|---|---|---|
| 환경 이식성 (다른 서버 이동) | 현재 서버로 충분, 이동 불필요 | ❌ 지금 불필요 |
| 팀원 동일 환경 공유 | cross-dataset 시 유용하나 conda로 가능 | △ 선택 사항 |
| 컨테이너 병렬 격리 실행 | conda env 4종 격리로 이미 해결 | △ 선택 사항 |
| 클린 삭제/재설치 | 계속 쓸 환경 — 불필요 | ❌ 지금 불필요 |
| CI/CD 파이프라인 | 연구 프로젝트, 해당 없음 | ❌ 해당 없음 |
| **논문 재현성 (reviewer 요청 대응)** | **투고 시점에 환경 박제 필요** | ✅ 논문 투고 전 권장 |

**→ 지금 당장 Docker 셋팅 불필요. 논문 투고 직전 환경 박제 용도로 활용.**

---

## 류재면님 임시 서버 Docker 셋팅 필요성

- 현재 서버(503GB RAM, A6000 ×3)가 모든 작업에 충분
- 류재면님 서버가 "임시"라면 굳이 Docker 셋팅 불필요
- 재현성 외 추가 이점이 이 프로젝트에서 크지 않음
- **→ 류재면님 서버는 현재 계획에서 제외해도 됨**

---

## Docker 활용 권장 시점: 논문 투고 직전

```bash
cd pipeline/hspc-velocity-benchmark

# CPU 이미지 빌드
docker build -t autobiox-bio01:cpu .

# GPU 이미지 빌드
docker build -t autobiox-bio01:gpu --build-arg GPU=1 .

# 환경 lock 파일 생성 (재현성 고정) ← 재현성 최우선 갭 해소
for e in scv-preprocess mv torch tf; do
  docker run --rm autobiox-bio01:gpu conda env export -n $e > env/$e.lock.yml
done
# → git commit env/*.lock.yml

# Docker Hub 또는 Zenodo 업로드 → Methods에 image hash 기재
docker push kakyungkim/autobiox-bio01:gpu
```

---

## 현재 준비된 파일

| 파일 | 내용 |
|---|---|
| `Dockerfile` | 4개 conda env 통합. CPU/GPU ARG 분기. MultiVeloVAE 패치 포함. |
| `docker-compose.yml` | CPU/GPU 서비스 분리. cross-dataset 병렬 실행 예시 포함. |

### Dockerfile 주요 특징
- `condaforge/miniforge3` 베이스
- `--build-arg GPU=1` 시 CUDA 12.1 torch wheel 자동 교체
- MultiVeloVAE `pyproject.toml` license 포맷 버그 자동 패치 (setuptools >= 61 호환)
- MoFlow repo 클론 + `simulation` import 버그 패치 포함
- `PYTHONPATH=/opt/bench/vendor/MoFlow/src` 자동 설정

---

## 오늘 세션(2026-06-30) conda로 해결한 의존성 문제 — Docker 빌드 시 참고

실서버에서 발생한 이슈들. Docker 컨테이너 내에서는 대부분 자동 해결됨.

| 문제 | 원인 | Docker에서 |
|---|---|---|
| torch CUDA/NCCL 버전 불일치 | 시스템 NCCL ≠ pip torch CUDA | GPU ARG로 정확한 wheel → 자동 해결 |
| libstdc++ CXXABI 버전 부족 | 시스템 libstdc++ 구버전 | conda-forge 컴파일 버전 → 자동 해결 |
| `/tmp` noexec 마운트 | 서버 보안 설정 | 컨테이너 내 /tmp 기본 실행 가능 → 자동 해결 |
| MultiVeloVAE pyproject.toml | `license = "BSD-3-Clause"` 구포맷 | Dockerfile에 sed 패치 추가 완료 |
| pkg_resources 누락 | setuptools 82.x 변경 | `setuptools<80` 미리 설치 → 해결 |

---

## 미완료 항목 (기존 BIOP01-22 잔여)

- ❌ `env/*.lock.yml` 미커밋 ← 논문 투고 전 필수
- ⚠️ tf arm (CRAK-Velo/cellDancer) 미검증 — GPU 실행 후 확인 필요
- ❓ GPU 검증: `torch.cuda.is_available()` = True 실측 필요 (BIOP02 완료 후 GPU 확보 시)
