# 다인 AI 협업 JupyterLab 서버 셋팅 기록

> 셋팅일: 2026-06-30. 서버: 121.126.38.195 (AMD Threadripper PRO, A6000×3, 503GB RAM)

## 설치된 패키지 (scv-preprocess conda env)

```bash
pip install jupyterlab==4.6.1
pip install jupyter-collaboration==4.4.1
pip install jupyterlab-chat==0.22.1
```

## 서버 시작

```bash
bash ~/start_collab_jupyter.sh
# 로그 확인: tail -f /tmp/collab_jupyter.log
```

스크립트 위치: `~/start_collab_jupyter.sh`  
작업 디렉토리: `/home/kkkim/collab_workspace`  
바인딩: `127.0.0.1:8899` (외부 직접 접근 차단, SSH 터널 필수)

## 팀원별 접속 (로컬 PC에서 실행)

```bash
# braveji
ssh -L 8899:localhost:8899 -J bastion@61.109.239.220 -p 2201 braveji@192.168.0.85

# 이건규 (gglee)
ssh -L 8899:localhost:8899 -J bastion@61.109.239.220 -p 2202 gglee@192.168.0.85

# jamie
ssh -L 8899:localhost:8899 -J bastion@61.109.239.220 -p 2203 jamie@192.168.0.85

# jhans
ssh -L 8899:localhost:8899 -J bastion@61.109.239.220 -p 2204 jhans@192.168.0.85

# 김가경 (kkkim)
ssh -L 8899:localhost:8899 -J bastion@61.109.239.220 -p 2205 kkkim@192.168.0.85

# 박세진 (sjpark)
ssh -L 8899:localhost:8899 -J bastion@61.109.239.220 -p 2206 sjpark@192.168.0.85
```

터널 연결 후 → 브라우저에서 `http://localhost:8899`  
비밀번호: `abio26`  
SSH 세션 끊으면 터널도 끊김 — 사용 중 터미널 유지할 것.

## 기능

- **실시간 동시 편집**: 같은 노트북 파일을 여러 명이 동시에 편집, 각자 커서 색상으로 구분
- **JupyterLab Chat**: 왼쪽 사이드바 채팅 패널 (jupyterlab-chat)
- **각자 계정으로 접속 가능**: `kkkim` 공유 불필요 — 본인 계정으로 SSH 터널

## 비밀번호 변경 방법

```bash
# 새 해시 생성
conda run -n scv-preprocess python -c "from jupyter_server.auth import passwd; print(passwd('새비밀번호'))"

# ~/start_collab_jupyter.sh 에서 --ServerApp.password 값 교체 후 서버 재시작
pkill -f "jupyter.*8899" && bash ~/start_collab_jupyter.sh
```

## 참고

- SSH 포트 정보 원본: https://biospin-ai.atlassian.net/wiki/spaces/VC/pages/27787268/02+-+SpatialPathoAgent
- Confluence 사용법 페이지: https://biospin-ai.atlassian.net/wiki/spaces/VC/pages/44859462/AI+JupyterLab
