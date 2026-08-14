#!/usr/bin/env python3
"""Confluence 페이지 상단에 정정 배너를 prepend — REST PUT (MCP 1000자 cap 우회).

사용: scripts/confluence_prepend_banner.py <pageId> <bannerHtmlFile> [--dry]
      (먼저 `source ~/.atlassian_env`)

배경: Atlassian MCP의 create/update_confluence_page는 content 1000자 하드 검증이라
      전문(1만~3만자) 페이지를 못 고친다. 그러나 **REST API에는 그 제한이 없다**
      (2026-08-14 실측). JIRA에서 MCP 대신 REST를 쓰는 것과 같은 구조.

설계: 기존 본문은 건드리지 않고 앞에만 붙인다(서식 손상 위험 최소화).
      마커 텍스트가 이미 있으면 중복 삽입을 거부한다(멱등).

BIOP01-83(원고 8/4 정정이 게시본에 미전파) 대응으로 작성. 인덱스=49545229,
자식 6편 = 49414154 / 49545246 / 49217541 / 49086484 / 49414177 / 50954242.
"""
import json, os, sys, urllib.request, ssl, socket

# ⚠️ Confluence는 ac: 매크로의 비표준 속성(data-*)을 저장 시 제거한다 → 속성 마커 못 씀.
#    반드시 본문에 남는 '텍스트'를 마커로 쓴다 (2026-08-14 실측 확인).
MARKER = '정정 안내 (2026-08-14 게시본 갱신)'
HOST = "biospin-ai.atlassian.net"
IP = "13.227.180.4"

def req(method, path, body=None):
    url = f"https://{HOST}{path}"
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(url, data=data, method=method)
    import base64
    tok = base64.b64encode(f"{os.environ['ATLASSIAN_EMAIL']}:{os.environ['ATLASSIAN_API_TOKEN']}".encode()).decode()
    r.add_header("Authorization", "Basic " + tok)
    r.add_header("Content-Type", "application/json")
    r.add_header("User-Agent", "kkkim-cli")
    # DNS 우회
    orig = socket.getaddrinfo
    socket.getaddrinfo = lambda h, p, *a, **k: orig(IP, p, *a, **k) if h == HOST else orig(h, p, *a, **k)
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read().decode())
    finally:
        socket.getaddrinfo = orig

pid = sys.argv[1]
banner = open(sys.argv[2], encoding="utf-8").read().strip()
dry = "--dry" in sys.argv

cur = req("GET", f"/wiki/rest/api/content/{pid}?expand=body.storage,version,space")
body = cur["body"]["storage"]["value"]
ver = cur["version"]["number"]
print(f"[{pid}] {cur['title'][:50]}")
print(f"  현재 v{ver}, body {len(body)}자")

if MARKER in body:
    print("  → 이미 배너 있음. 중복 삽입 거부.")
    sys.exit(0)

new_body = banner + "\n" + body
print(f"  새 body {len(new_body)}자 (+{len(new_body)-len(body)})")

if dry:
    print("  [dry-run] PUT 안 함")
    sys.exit(0)

out = req("PUT", f"/wiki/rest/api/content/{pid}", {
    "id": pid,
    "type": "page",
    "title": cur["title"],
    "space": {"key": cur["space"]["key"]},
    "body": {"storage": {"value": new_body, "representation": "storage"}},
    "version": {"number": ver + 1, "message": "BIOP01-83 정정 배너 삽입 (원고 8/4 정정 반영, 본문 무변경)"},
})
print(f"  ✅ PUT OK → v{out['version']['number']}")
