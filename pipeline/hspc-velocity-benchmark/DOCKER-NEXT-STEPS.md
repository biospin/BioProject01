# Docker / env 재현성 — 다음 할 일 (BIOP01-22)
> branch: kkkim-pipeline. 위치: pipeline/hspc-velocity-benchmark/

## 산출물 (이 디렉토리)
- `Dockerfile` — 4-env(scv-preprocess/mv/torch/tf) 통합. env/*.yml 그대로 COPY + torch arm에 MoFlow clone+패치 3건.
- `.dockerignore` — 화이트리스트(env yml 4개만 컨텍스트 포함).
- `env/` — 원본 env 자산(setup_torch_gpu.sh, setup_envs.sh, *.yml, README, GPU-SETUP). **정본**.
- repo 확정: MoFlow=`github.com/AriHong/MoFlow`(clone+패치), CRAK-Velo=`github.com/StatBiomed/CRAK-Velo`(url-only·미검증).

## BIOP01-22 점검 결과
- ✅ setup_torch_gpu.sh 커밋됨 — 단 2026-06-15 Mac(CPU) 검증만, GPU cuda=True 실검증 미완.
- ❌ **env/*.lock.yml 미커밋** ← 재현성 최우선 갭.
- ⚠️ tf arm(CRAK-Velo/cellDancer) 미검증·가장 취약(UniTVelo/TF 버전, cisTopic).

## 다음 할 일 (순서)
1. **docker 가용 확인 + CPU 빌드**: `cd pipeline/hspc-velocity-benchmark && docker build -t autobiox-bio01:cpu .`
2. **MoFlow import 검증**: `conda run -n torch python -c "import torch, multivelovae; from MoFlow.moflow import MOFlow; print('ok')"`.
3. **tf arm 단단히**: tf.yml 깨지면 UniTVelo 권장 TF 버전 핀 + (필요시) pycisTopic.
4. **GPU 검증**: GPU 머신에서 `--build-arg GPU=1` → `conda run -n torch python -c "import torch; print(torch.cuda.is_available())"`=True. (현재 GPU 서버 Xid79 다운 → 복구/A16/RunPod 필요)
5. **★ lock 박제(재현성 갭)**: 빌드 성공 후
   ```bash
   for e in scv-preprocess mv torch tf; do
     docker run --rm autobiox-bio01:gpu conda env export -n $e > env/$e.lock.yml
   done
   ```
   → 4개 `env/*.lock.yml` 커밋.

## 자원/런타임 (BIOP01-22 ③)
- MultiVelo: GPU 미지원, CPU 7.4h. 다코어 Linux 필요.
- DL arm: 11k cells면 CPU도 가능, bootstrap 대량 반복 시 GPU.
- GPU 1대를 torch→tf 순차 점유 → 1대로 충분.
- ❓ BioProject01 compute 머신 확정 필요(로컬 vs A16 vs RunPod).
