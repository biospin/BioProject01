#!/usr/bin/env python3
"""Local click dashboard for the BioProject01 paper-analysis harness.

The dashboard intentionally keeps the existing harness as the source of truth.
It records new analysis requests, lists existing paper folders, and runs the
project's deterministic helper scripts such as index rebuild and HTML render.
"""

from __future__ import annotations

import argparse
import cgi
import datetime as dt
import html
import json
import mimetypes
import os
import re
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

try:
    import markdown as markdown_lib
except ImportError:
    markdown_lib = None


REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = REPO_ROOT / "web"
STATIC_ROOT = WEB_ROOT / "static"
ANALYSIS_ROOT = REPO_ROOT / "analysis"
RUN_ROOT = REPO_ROOT / "artifacts" / "web-runs"
UPLOAD_ROOT = REPO_ROOT / "artifacts" / "uploads"
JOBS: dict[str, subprocess.Popen] = {}


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def unauthorized(handler: BaseHTTPRequestHandler) -> None:
    json_response(handler, 401, {"error": "dashboard token required"})


def text_response(
    handler: BaseHTTPRequestHandler,
    status: int,
    body: str,
    content_type: str = "text/plain; charset=utf-8",
) -> None:
    data = body.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def file_response(handler: BaseHTTPRequestHandler, path: Path) -> None:
    data = path.read_bytes()
    content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    if path.suffix.lower() in {".css", ".js"}:
        content_type += "; charset=utf-8"
    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def validate_analysis_file(raw_path: str, suffix: str) -> Path:
    path = safe_relative_path(raw_path)
    if not path.exists() or not path.is_file():
        raise ValueError("file not found")
    if ANALYSIS_ROOT.resolve() not in path.resolve().parents:
        raise ValueError("file must be under analysis/")
    if path.suffix.lower() != suffix:
        raise ValueError(f"file must be a {suffix} file")
    return path


def paper_html_path(raw_paper_path: str) -> Path:
    paper_dir = safe_relative_path(raw_paper_path)
    if not paper_dir.exists() or not paper_dir.is_dir():
        raise ValueError("paper_path must be an existing directory")
    if ANALYSIS_ROOT.resolve() not in paper_dir.resolve().parents:
        raise ValueError("paper_path must be under analysis/")
    html_path = paper_dir / f"{paper_dir.name}_core.html"
    if not html_path.exists():
        raise ValueError("core HTML has not been rendered yet")
    return html_path


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w가-힣一-龥ぁ-んァ-ン]+", "-", text.lower(), flags=re.UNICODE)
    return slug.strip("-") or "section"


def render_inline_markdown(text: str) -> str:
    value = html.escape(text)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    return value


def simple_markdown_to_html(md_text: str) -> str:
    """Small fallback renderer for reading notes when python-markdown is absent."""
    lines = md_text.splitlines()
    parts = []
    in_ul = False
    in_ol = False
    in_code = False
    code_lines = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            parts.append("</ul>")
            in_ul = False
        if in_ol:
            parts.append("</ol>")
            in_ol = False

    for line in lines:
        if line.startswith("```"):
            if in_code:
                parts.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                close_lists()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            close_lists()
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            close_lists()
            level = len(heading.group(1))
            label = heading.group(2).strip()
            parts.append(
                f'<h{level} id="{html.escape(slugify(label))}">{render_inline_markdown(label)}</h{level}>'
            )
            continue

        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        if bullet:
            if not in_ul:
                close_lists()
                parts.append("<ul>")
                in_ul = True
            parts.append(f"<li>{render_inline_markdown(bullet.group(1).strip())}</li>")
            continue

        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if ordered:
            if not in_ol:
                close_lists()
                parts.append("<ol>")
                in_ol = True
            parts.append(f"<li>{render_inline_markdown(ordered.group(1).strip())}</li>")
            continue

        close_lists()
        parts.append(f"<p>{render_inline_markdown(line.strip())}</p>")

    close_lists()
    if in_code:
        parts.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(parts)


def markdown_to_html(md_text: str) -> str:
    if markdown_lib is not None:
        return markdown_lib.markdown(
            md_text,
            extensions=["extra", "tables", "fenced_code", "toc", "sane_lists"],
            output_format="html5",
        )
    return simple_markdown_to_html(md_text)


def markdown_view_response(handler: BaseHTTPRequestHandler, path: Path) -> None:
    body = path.read_text(encoding="utf-8", errors="replace")
    title = html.escape(path.stem)
    rel_path = html.escape(str(path.relative_to(REPO_ROOT)))
    rendered_body = markdown_to_html(body)
    page = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
      body {{
        margin: 0;
        background: #f7f7f4;
        color: #202124;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
        line-height: 1.65;
      }}
      header {{
        position: sticky;
        top: 0;
        background: rgba(255, 255, 255, 0.96);
        border-bottom: 1px solid #d8dbe0;
        padding: 14px 22px;
      }}
      h1 {{
        margin: 0;
        font-size: 18px;
      }}
      p {{
        margin: 4px 0 0;
        color: #62666d;
      }}
      main {{
        max-width: 980px;
        margin: 0 auto;
        padding: 22px;
      }}
      article {{
        background: #fff;
        border: 1px solid #d8dbe0;
        border-radius: 8px;
        padding: 28px 34px;
      }}
      article h1,
      article h2,
      article h3,
      article h4 {{
        line-height: 1.25;
        margin-top: 1.5em;
        margin-bottom: 0.55em;
      }}
      article h1 {{
        font-size: 28px;
      }}
      article h2 {{
        border-bottom: 1px solid #d8dbe0;
        font-size: 22px;
        padding-bottom: 5px;
      }}
      article h3 {{
        font-size: 18px;
      }}
      article p,
      article ul,
      article ol {{
        margin: 0.7em 0;
      }}
      article li {{
        margin: 0.25em 0;
      }}
      article code {{
        background: #f0f2f4;
        border-radius: 4px;
        padding: 2px 5px;
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size: 0.92em;
      }}
      article pre {{
        background: #151719;
        color: #f3f5f6;
        border-radius: 8px;
        overflow: auto;
        padding: 14px 16px;
      }}
      article pre code {{
        background: transparent;
        color: inherit;
        padding: 0;
      }}
      article blockquote {{
        border-left: 3px solid #aeb5bd;
        color: #62666d;
        margin: 1em 0;
        padding: 6px 14px;
        background: #f6f8f7;
      }}
      article table {{
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
        font-size: 0.92em;
      }}
      article th,
      article td {{
        border: 1px solid #d8dbe0;
        padding: 8px 10px;
        text-align: left;
        vertical-align: top;
      }}
      article th {{
        background: #f0f2f4;
      }}
      @media (max-width: 760px) {{
        main {{
          padding: 12px;
        }}
        article {{
          padding: 20px;
        }}
      }}
    </style>
  </head>
  <body>
    <header>
      <h1>{title}</h1>
      <p>{rel_path}</p>
    </header>
    <main>
      <article>{rendered_body}</article>
    </main>
  </body>
</html>
"""
    text_response(handler, 200, page, "text/html; charset=utf-8")


def read_body(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length") or "0")
    raw = handler.rfile.read(length).decode("utf-8") if length else "{}"
    if not raw.strip():
        return {}
    return json.loads(raw)


def safe_upload_name(filename: str) -> str:
    stem = Path(filename or "paper.pdf").name
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip(".-")
    if not stem.lower().endswith(".pdf"):
        stem += ".pdf"
    return stem or "paper.pdf"


def upload_pdf(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length") or "0")
    max_size = 150 * 1024 * 1024
    if length <= 0:
        raise ValueError("empty upload")
    if length > max_size:
        raise ValueError("PDF upload is too large; limit is 150 MB")

    form = cgi.FieldStorage(
        fp=handler.rfile,
        headers=handler.headers,
        environ={
            "REQUEST_METHOD": "POST",
            "CONTENT_TYPE": handler.headers.get("Content-Type", ""),
        },
    )
    field = form["pdf"] if "pdf" in form else None
    if field is None or not field.filename:
        raise ValueError("multipart field 'pdf' is required")

    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    target = UPLOAD_ROOT / f"{timestamp}-{safe_upload_name(field.filename)}"
    with target.open("wb") as out:
        while True:
            chunk = field.file.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)

    return {
        "path": str(target.relative_to(REPO_ROOT)),
        "filename": target.name,
        "size": target.stat().st_size,
    }


def safe_relative_path(raw_path: str, base: Path = REPO_ROOT) -> Path:
    path = (base / raw_path).resolve()
    if base.resolve() not in path.parents and path != base.resolve():
        raise ValueError("path must stay inside the repository")
    return path


def first_yaml_scalar(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip()
    if value.startswith(("'", '"')) and value.endswith(("'", '"')):
        value = value[1:-1]
    return value


def yaml_list(text: str, key: str) -> list[str]:
    inline = re.search(rf"^{re.escape(key)}:\s*\[(.*?)\]\s*$", text, re.MULTILINE)
    if inline:
        return [part.strip().strip("'\"") for part in inline.group(1).split(",") if part.strip()]

    block = re.search(rf"^{re.escape(key)}:\s*\n((?:\s+- .+\n?)+)", text, re.MULTILINE)
    if not block:
        return []
    values = []
    for line in block.group(1).splitlines():
        item = line.strip()
        if item.startswith("- "):
            values.append(item[2:].strip().strip("'\""))
    return values


def file_status(paper_dir: Path, paper_id: str) -> dict[str, bool]:
    return {
        "core": (paper_dir / f"{paper_id}_core.md").exists(),
        "academic": (paper_dir / f"{paper_id}_lens-academic.md").exists(),
        "industry": (paper_dir / f"{paper_id}_lens-industry.md").exists(),
        "brief": (paper_dir / f"{paper_id}_methodology-brief.md").exists(),
        "html": (paper_dir / f"{paper_id}_core.html").exists(),
        "pdf": (paper_dir / "sources" / "paper.pdf").exists(),
    }


def list_papers() -> list[dict]:
    papers = []
    for yaml_path in sorted(ANALYSIS_ROOT.glob("*/*/paper-info.yaml")):
        paper_dir = yaml_path.parent
        paper_id = paper_dir.name
        text = yaml_path.read_text(encoding="utf-8")
        rel_dir = paper_dir.relative_to(REPO_ROOT)
        papers.append(
            {
                "paper_id": paper_id,
                "topic": paper_dir.parent.name,
                "path": str(rel_dir),
                "title": first_yaml_scalar(text, "title"),
                "year": first_yaml_scalar(text, "year"),
                "venue": first_yaml_scalar(text, "venue"),
                "doi": first_yaml_scalar(text, "doi"),
                "document_type": first_yaml_scalar(text, "document_type"),
                "topics": yaml_list(text, "topics"),
                "status": file_status(paper_dir, paper_id),
            }
        )
    return papers


def run_command(args: list[str], timeout: int = 180) -> dict:
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    proc = subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "command": args,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-8000:],
        "stderr": proc.stderr[-8000:],
        "started_at": started,
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def write_job_status(run_dir: Path, status: dict) -> None:
    (run_dir / "codex-job.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_job_status(run_dir: Path) -> dict:
    status_path = run_dir / "codex-job.json"
    if not status_path.exists():
        return {"status": "not-started"}
    try:
        return json.loads(status_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"status": "invalid-status"}


def read_run_request(run_dir: Path) -> dict:
    request_path = run_dir / "request.json"
    if not request_path.exists():
        return {}
    try:
        return json.loads(request_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def find_output_dir(run_dir: Path, log_tail: str):
    request = read_run_request(run_dir)
    topic = request.get("topic", "").strip()

    matches = re.findall(r"analysis/([^/\s]+)/([^/\s]+)/", log_tail)
    for found_topic, paper_id in reversed(matches):
        if topic and found_topic != topic:
            continue
        paper_dir = ANALYSIS_ROOT / found_topic / paper_id
        if paper_dir.exists():
            return paper_dir

    if topic:
        topic_dir = ANALYSIS_ROOT / topic
        if topic_dir.exists():
            candidates = [path for path in topic_dir.iterdir() if path.is_dir()]
            if candidates:
                return max(candidates, key=lambda path: path.stat().st_mtime)
    return None


def summarize_run_outputs(run_dir: Path, log_tail: str) -> dict:
    paper_dir = find_output_dir(run_dir, log_tail)
    if not paper_dir:
        return {
            "paper_dir": "",
            "message": "No analysis folder detected yet.",
            "files": {},
        }

    paper_id = paper_dir.name
    files = {
        "paper-info.yaml": (paper_dir / "paper-info.yaml").exists(),
        "core.md": (paper_dir / f"{paper_id}_core.md").exists(),
        "academic lens": (paper_dir / f"{paper_id}_lens-academic.md").exists(),
        "industry lens": (paper_dir / f"{paper_id}_lens-industry.md").exists(),
        "methodology brief": (paper_dir / f"{paper_id}_methodology-brief.md").exists(),
        "core.html": (paper_dir / f"{paper_id}_core.html").exists(),
    }
    return {
        "paper_dir": str(paper_dir.relative_to(REPO_ROOT)),
        "message": f"Detected outputs in {paper_dir.relative_to(REPO_ROOT)}",
        "files": files,
    }


def process_is_running(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        stat = subprocess.run(
            ["ps", "-p", str(pid), "-o", "stat="],
            text=True,
            capture_output=True,
            timeout=2,
            check=False,
        )
        if stat.returncode != 0:
            return False
        if stat.stdout.strip().startswith("Z"):
            return False
    except Exception:
        pass
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def watch_codex_job(run_dir: Path, proc: subprocess.Popen) -> None:
    returncode = proc.wait()
    status = read_job_status(run_dir)
    if status.get("status") == "running":
        status["status"] = "succeeded" if returncode == 0 else "failed"
        status["returncode"] = returncode
        status["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        write_job_status(run_dir, status)


def resolve_run_dir(raw_path: str) -> Path:
    run_dir = safe_relative_path(raw_path)
    if not run_dir.exists() or not run_dir.is_dir():
        raise ValueError("run_path must be an existing run directory")
    if RUN_ROOT.resolve() not in run_dir.resolve().parents:
        raise ValueError("run_path must be under artifacts/web-runs/")
    return run_dir


def start_codex_job(raw_path: str) -> dict:
    run_dir = resolve_run_dir(raw_path)
    run_id = run_dir.name
    prompt_path = run_dir / "prompt.md"
    if not prompt_path.exists():
        raise ValueError("prompt.md not found for this run")

    existing = JOBS.get(run_id)
    if existing and existing.poll() is None:
        return get_codex_job(raw_path)

    log_path = run_dir / "codex.log"
    command = ["codex", "exec", "--cd", str(REPO_ROOT), "-"]
    prompt_file = prompt_path.open("r", encoding="utf-8")
    log_file = log_path.open("a", encoding="utf-8")
    proc = subprocess.Popen(
        command,
        cwd=REPO_ROOT,
        stdin=prompt_file,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    prompt_file.close()
    log_file.close()

    JOBS[run_id] = proc
    status = {
        "status": "running",
        "run_id": run_id,
        "pid": proc.pid,
        "command": command,
        "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "finished_at": "",
        "returncode": None,
        "log_path": str(log_path.relative_to(REPO_ROOT)),
    }
    write_job_status(run_dir, status)
    threading.Thread(target=watch_codex_job, args=(run_dir, proc), daemon=True).start()
    result = status.copy()
    result["log_tail"] = ""
    result["outputs"] = summarize_run_outputs(run_dir, "")
    return result


def get_codex_job(raw_path: str) -> dict:
    run_dir = resolve_run_dir(raw_path)
    run_id = run_dir.name
    status = read_job_status(run_dir)
    proc = JOBS.get(run_id)
    if proc:
        returncode = proc.poll()
        if returncode is not None and status.get("status") == "running":
            status["status"] = "succeeded" if returncode == 0 else "failed"
            status["returncode"] = returncode
            status["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            write_job_status(run_dir, status)
    elif status.get("status") == "running" and not process_is_running(status.get("pid")):
        status["status"] = "finished-unknown"
        status["finished_at"] = status.get("finished_at") or dt.datetime.now(dt.timezone.utc).isoformat()
        status["note"] = "Dashboard restarted after this job began, so the exact return code is unavailable. Check codex.log for the final result."
        write_job_status(run_dir, status)

    log_path = run_dir / "codex.log"
    log_tail = ""
    if log_path.exists():
        log_tail = log_path.read_text(encoding="utf-8", errors="replace")[-12000:]
    result = status.copy()
    result["log_tail"] = log_tail
    result["outputs"] = summarize_run_outputs(run_dir, log_tail)
    return result


def make_run_id() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def create_prompt(payload: dict) -> str:
    source = payload.get("source", "").strip()
    topic = payload.get("topic", "").strip()
    mode = payload.get("mode", "full").strip()
    lens = payload.get("lens", "both").strip()
    notes = payload.get("notes", "").strip()

    lines = [
        "# Paper Analysis Request",
        "",
        "BioProject01 논문 분석 하네스를 사용해 아래 자료를 분석해줘.",
        "",
        f"- Source: {source or '확인 필요'}",
        f"- Topic: {topic or '자동 추천 후 사용자 확인'}",
        f"- Mode: {mode}",
        f"- Lens: {lens}",
    ]
    if notes:
        lines.extend(["", "## Notes", notes])
    lines.extend(
        [
            "",
            "## Required workflow",
            "1. AGENTS.md Quick Start와 Full Paper Workflow를 따른다.",
            "2. source-grounding으로 `analysis/<topic>/<paper-id>/`와 `paper-info.yaml`을 만든다.",
            "3. mode/lens 선택에 맞춰 core, lens, methodology-brief를 작성한다.",
            "4. 마지막에 `skills/source-grounding/scripts/build_index.py`를 실행한다.",
            "5. full/core 분석이면 `skills/core-to-html/scripts/build_html.py <paper-dir>`를 실행한다.",
            "",
            "추측은 `해석:` / `추정:` / `검토필요:`로 분리하고, PDF 또는 supplementary에 없는 사실을 단정하지 않는다.",
        ]
    )
    return "\n".join(lines) + "\n"


def create_run(payload: dict) -> dict:
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    run_dir = RUN_ROOT / make_run_id()
    suffix = 1
    while run_dir.exists():
        run_dir = RUN_ROOT / f"{make_run_id()}-{suffix}"
        suffix += 1
    run_dir.mkdir(parents=True)

    request = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": payload.get("source", "").strip(),
        "topic": payload.get("topic", "").strip(),
        "mode": payload.get("mode", "full").strip(),
        "lens": payload.get("lens", "both").strip(),
        "notes": payload.get("notes", "").strip(),
        "status": "prompt-created",
    }
    prompt = create_prompt(request)
    (run_dir / "request.json").write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    return {
        "run_id": run_dir.name,
        "run_path": str(run_dir.relative_to(REPO_ROOT)),
        "prompt": prompt,
        "request": request,
    }


def list_runs() -> list[dict]:
    if not RUN_ROOT.exists():
        return []
    runs = []
    for run_dir in sorted(RUN_ROOT.iterdir(), reverse=True):
        if not run_dir.is_dir():
            continue
        request_path = run_dir / "request.json"
        data = {}
        if request_path.exists():
            try:
                data = json.loads(request_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                data = {"status": "invalid-json"}
        runs.append(
            {
                "run_id": run_dir.name,
                "path": str(run_dir.relative_to(REPO_ROOT)),
                "request": data,
                "has_prompt": (run_dir / "prompt.md").exists(),
            }
        )
    return runs[:50]


class AppHandler(BaseHTTPRequestHandler):
    server_version = "BioProject01PaperWeb/0.1"

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def token_required(self) -> bool:
        token = getattr(self.server, "dashboard_token", "")
        if not token:
            return False
        if not self.path.startswith("/api/"):
            return False
        provided = self.headers.get("X-Dashboard-Token", "")
        return provided != token

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            if self.token_required():
                unauthorized(self)
                return
            if parsed.path == "/":
                index = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
                text_response(self, 200, index, "text/html; charset=utf-8")
            elif parsed.path == "/view/core":
                query = parse_qs(parsed.query)
                raw_path = unquote(query.get("path", [""])[0])
                path = validate_analysis_file(raw_path, ".md")
                markdown_view_response(self, path)
            elif parsed.path == "/view/html":
                query = parse_qs(parsed.query)
                raw_paper_path = unquote(query.get("paper_path", [""])[0])
                file_response(self, paper_html_path(raw_paper_path))
            elif parsed.path == "/api/papers":
                json_response(self, 200, {"papers": list_papers()})
            elif parsed.path == "/api/runs":
                json_response(self, 200, {"runs": list_runs()})
            elif parsed.path == "/api/run/codex-status":
                query = parse_qs(parsed.query)
                raw_path = unquote(query.get("run_path", [""])[0])
                json_response(self, 200, get_codex_job(raw_path))
            elif parsed.path == "/api/file":
                query = parse_qs(parsed.query)
                raw_path = unquote(query.get("path", [""])[0])
                path = safe_relative_path(raw_path)
                if not path.exists() or not path.is_file():
                    json_response(self, 404, {"error": "file not found"})
                    return
                body = path.read_text(encoding="utf-8", errors="replace")
                json_response(
                    self,
                    200,
                    {"path": str(path.relative_to(REPO_ROOT)), "content": body},
                )
            elif parsed.path.startswith("/static/"):
                rel = parsed.path[len("/static/") :]
                path = safe_relative_path(rel, STATIC_ROOT)
                if not path.exists() or not path.is_file():
                    text_response(self, 404, "not found")
                    return
                file_response(self, path)
            else:
                text_response(self, 404, "not found")
        except Exception as exc:  # pragma: no cover - local diagnostic route
            json_response(self, 500, {"error": str(exc)})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            if self.token_required():
                unauthorized(self)
                return
            if parsed.path == "/api/upload/pdf":
                result = upload_pdf(self)
                json_response(self, 201, result)
            elif parsed.path == "/api/run/new":
                payload = read_body(self)
                result = create_run(payload)
                json_response(self, 201, result)
            elif parsed.path == "/api/run/build-index":
                result = run_command(
                    [sys.executable, "skills/source-grounding/scripts/build_index.py"],
                    timeout=180,
                )
                json_response(self, 200, result)
            elif parsed.path == "/api/run/render-html":
                payload = read_body(self)
                paper_path = payload.get("paper_path", "")
                paper_dir = safe_relative_path(paper_path)
                if not paper_dir.exists() or not paper_dir.is_dir():
                    json_response(self, 400, {"error": "paper_path must be an existing directory"})
                    return
                if ANALYSIS_ROOT.resolve() not in paper_dir.resolve().parents:
                    json_response(self, 400, {"error": "paper_path must be under analysis/"})
                    return
                result = run_command(
                    [sys.executable, "skills/core-to-html/scripts/build_html.py", str(paper_dir)],
                    timeout=300,
                )
                json_response(self, 200, result)
            elif parsed.path == "/api/run/start-codex":
                payload = read_body(self)
                result = start_codex_job(payload.get("run_path", ""))
                json_response(self, 202, result)
            else:
                text_response(self, 404, "not found")
        except json.JSONDecodeError:
            json_response(self, 400, {"error": "invalid json"})
        except subprocess.TimeoutExpired as exc:
            json_response(self, 504, {"error": "command timed out", "command": exc.cmd})
        except Exception as exc:  # pragma: no cover - local diagnostic route
            json_response(self, 500, {"error": str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the BioProject01 paper web dashboard.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=int(os.environ.get("PORT", "8765")), type=int)
    parser.add_argument(
        "--token",
        default=os.environ.get("BIOP01_DASHBOARD_TOKEN", ""),
        help="Optional API token for team/LAN sharing. Also read from BIOP01_DASHBOARD_TOKEN.",
    )
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), AppHandler)
    server.dashboard_token = args.token
    print(f"BioProject01 paper dashboard: http://{args.host}:{args.port}", flush=True)
    if args.token:
        print("API token authentication: enabled", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
