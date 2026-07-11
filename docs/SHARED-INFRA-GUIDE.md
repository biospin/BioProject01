# 공용 서버·GPU·환경 사용 가이드 (BIOP01 · BIOP02 공용)

> **목적** — 다인 협업 서버(A6000×3)의 접속·GPU·conda 환경 사용법을 한 곳에 모은 canonical 문서.
> **추적** — 이 파일(git) ↔ Confluence VC "다인 AI 협업 JupyterLab 서버 사용법" 하위 페이지를 동기화.
> **발표자료** — PseudoCon 2026 인프라/협업 슬라이드의 원천(§6 요약표 그대로 사용 가능).
> 최초 정리 2026-07-11 (kkkim). 접속 장애 진단·복구(§2) 반영.

---

## 0. 공용 작업 문서 인덱스 (리스트업)

| 문서 | 위치 | 내용 |
|---|---|---|
| **이 가이드** (canonical) | git `docs/SHARED-INFRA-GUIDE.md` + Confluence 하위 | 접속·GPU·env 통합 |
| 다인 AI 협업 JupyterLab 서버 사용법 | Confluence VC / 44859462 | 접속 정본(본 가이드로 현행화) |
| GPU 자원 운용 방안 — A6000 vs RunPod | Confluence VC / 40566786 | 자원 계획·스케줄링 |
| 서버 변경 + 임베딩 완료 (2026-06-30) | Confluence VC / 46333954 | 서버 이관 기록 |
| [인프라] 협업 JupyterLab 구축·운영 | Jira SCRUM-5 | 인프라 일감 |
| env 구축(velocity benchmark) | git `pipeline/hspc-velocity-benchmark/env/README.md` | BIOP01 conda env 5종 |

---

## 1. 서버 개요

- **본서버**: `121.126.38.195` (내부망 `192.168.0.85`) — Threadripper PRO, **RTX A6000 48GB × 3**, RAM 503GB
- **Bastion(점프 호스트)**: `61.109.239.220` (구 A100 서버 주소)
- **팀원별 컨테이너**: 각자 **개별 docker 컨테이너**(bridge 네트워크 `172.18.0.x`)로 격리. SSH 포트가 컨테이너별로 매핑됨.

| 계정 | SSH 포트 | | 계정 | SSH 포트 |
|---|---|---|---|---|
| braveji(지용기) | 2201 | | jhans(서정한) | 2204 |
| gglee(이건규) | 2202 | | **kkkim(김가경)** | **2205** |
| jamie(류재면) | 2203 | | sjpark(박세진) | 2206 |

---

## 2. JupyterLab 협업 접속

실시간 동시편집 + 채팅. jupyter는 **kkkim 컨테이너**에서 1개 기동, 팀 전원이 터널로 공유.

### 2.1 기동 (kkkim만)
```bash
bash ~/start_collab_jupyter.sh     # 8899 포트, --ip=0.0.0.0, notebook-dir=~/collab_workspace
```
스크립트가 **kkkim 컨테이너 IP**(`hostname -i`)를 출력함 → 팀원 터널 목적지로 사용.

### 2.2 접속 (팀원 각자 로컬 PC) — ⚠️ 핵심
```bash
# 목적지는 localhost가 아니라 kkkim 컨테이너 IP(예시 172.18.0.5). 본인 SSH 포트 사용.
ssh -L 8899:172.18.0.5:8899 -J bastion@61.109.239.220 -p <본인포트> <계정>@192.168.0.85
# 브라우저 → http://localhost:8899   (웹 비밀번호: abio26)
```
- **kkkim 본인만** `-L 8899:localhost:8899` 가능(jupyter가 자기 컨테이너에 있으므로).
- kkkim 컨테이너 IP는 재시작 시 바뀔 수 있음 → 기동 로그의 "★ kkkim 컨테이너 IP" 값을 확인.
- SSH 세션 종료 시 터널도 끊김 → 사용 중 터미널 유지.

### 2.3 접속 장애 진단·복구 이력 (2026-07-10~11)
- **증상**: kkkim 외 전원 접속 불가(`127.0.0.1:8899 Connection refused`).
- **원인**(jamie·sjpark 진단): ① jupyter가 localhost 바인딩, ② 팀원 터널 목적지 `-L …:localhost:…`가 각자 자기 컨테이너로 해석돼 kkkim 컨테이너에 안 닿음.
- **해결**: ① 시작 스크립트 `--ip=0.0.0.0`(반영됨), ② 터널 목적지를 kkkim 컨테이너 IP로(스크립트가 `hostname -i`로 자동 안내). 컨테이너 bridge TCP는 열려 있어 ①+②로 전원 접속.

---

## 3. GPU 공용 사용 예절 (A6000×3, 6명 공유) — 꼭 지킬 것

```bash
nvidia-smi                             # ① 먼저 빈 카드/메모리 확인 (0/1/2)
export CUDA_VISIBLE_DEVICES=0          # ② 자기 카드 1장만 지정
export TF_FORCE_GPU_ALLOW_GROWTH=true  # ③ (TensorFlow) 카드 메모리 전량 선점 방지
```
- **미지정 시 위험**: TensorFlow는 기본적으로 **보이는 GPU 전부 + 메모리 48GB 통째**를 잡음 → 한 명이 3장 독점. 반드시 `CUDA_VISIBLE_DEVICES`로 카드 지정.
- PyTorch도 명시 device 아니면 `cuda:0`만 사용 → 겹치지 않게 카드 번호 분담.
- **무거운 학습(다일 연속)**은 슬롯 사전 예약(GPU 자원 운용 페이지 규칙). 가벼운 추론/CPU 작업은 자유 병행.

---

## 4. conda 환경

### 4.1 BIOP01 — velocity benchmark (상세: `env/README.md`)
| env | method | GPU | 활성화 |
|---|---|---|---|
| `tf` | CRAK-Velo/UniTVelo (TF 2.13) | ✅ A6000×3 (설정 완료) | `conda activate /opt/envs/tf` |
| `torch` | MultiVeloVAE/MoFlow | ✅ cu121 (자체 번들) | `conda activate /opt/envs/torch` |
| `celldancer` | cellDancer(참고) | CPU (격리 env) | `conda activate /opt/envs/celldancer` |
| `mv` | MultiVelo/scVelo | CPU | `conda activate mv` |
| `scv-preprocess` | 공통 전처리 + JupyterLab 구동 | CPU | `conda activate scv-preprocess` |

- `tf` GPU: `conda activate`만으로 인식(activate.d 훅이 `LD_LIBRARY_PATH` 자동 설정). `tensorflow[and-cuda]` 금지 — 상세 `env/README.md`.
- `torch` GPU: cu121 wheel이 CUDA 자체 번들 → 바로 인식.
- `celldancer`: numpy 1.20.3 등 옛 버전 하드핀 → 전용 격리 env(legacy resolver). 상세 `env/celldancer.yml`.

### 4.2 BIOP02 — SpatialPathoAgent (GPU 사용 중)
- UNI/CONCH 임베딩 등 GPU 작업(§ 서버변경 페이지 기준 `~/data/embeddings/biop02/`).
- **[TODO — BIOP02 오너(braveji/sjpark) 확인]**: BIOP02 전용 conda env 이름·경로·GPU wheel 버전을 이 표에 추가.
  GPU 공용 예절(§3)은 BIOP02에도 그대로 적용.

---

## 5. 문제 시 연락 / 체크리스트

- JupyterLab 접속 안 됨 → (1) kkkim에게 서버 기동 요청(`bash ~/start_collab_jupyter.sh`), (2) `-L` 목적지가 kkkim 컨테이너 IP인지 확인, (3) 본인 SSH 포트 확인(§1 표).
- GPU 안 잡힘 → env 활성화 확인 + `nvidia-smi`로 드라이버 정상 확인.
- 공유 머신이므로 **체크포인팅 필수**(재부팅·대형 작업으로 중단 가능).

---

## 6. 발표자료용 한 줄 요약 (슬라이드)

> **인프라**: 자체 A6000×3(48GB) Threadripper 서버 + bastion. 6인 개별 컨테이너 위에 **실시간 협업 JupyterLab**(단일 인스턴스 공유) 운영. GPU는 `CUDA_VISIBLE_DEVICES` 분담 + 무거운 작업 슬롯 예약으로 조율. 프레임워크별 격리 conda env(velocity 5종: TF/PyTorch/celldancer 등)로 의존성 충돌 차단.

| 자원 | 스펙 | 용도 |
|---|---|---|
| GPU | RTX A6000 48GB × 3 | 임베딩·GNN·velocity DL arm |
| CPU/RAM | Threadripper PRO / 503GB | 전처리·타일링·부트스트랩 |
| 협업 | JupyterLab 실시간 동시편집 + Chat | 6인 공용 `~/collab_workspace` |
