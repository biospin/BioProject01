const state = {
  papers: [],
  runs: [],
  filter: "",
  token: localStorage.getItem("biop01_dashboard_token") || "",
  activeRunPath: "",
  activePrompt: "",
  jobPoller: null,
  engine: "codex",
};

const ENGINE_LABEL = { codex: "Codex", claude: "Claude" };

const $ = (id) => document.getElementById(id);

function log(message, payload) {
  const out = $("logOutput");
  const time = new Date().toLocaleTimeString();
  const detail = payload ? `\n${JSON.stringify(payload, null, 2)}` : "";
  out.textContent = `[${time}] ${message}${detail}\n\n${out.textContent}`;
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) {
    headers["X-Dashboard-Token"] = state.token;
  }
  const response = await fetch(path, {
    headers,
    ...options,
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || `Request failed: ${response.status}`);
  }
  return data;
}

async function uploadApi(path, formData) {
  const headers = {};
  if (state.token) {
    headers["X-Dashboard-Token"] = state.token;
  }
  const response = await fetch(path, {
    method: "POST",
    headers,
    body: formData,
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || `Request failed: ${response.status}`);
  }
  return data;
}

function statusBadge(label, done) {
  return `<span class="badge ${done ? "done" : "missing"}">${label}: ${done ? "done" : "missing"}</span>`;
}

function paperProgress(status) {
  const s = status || {};
  if (s.core && s.academic && s.industry && s.brief && s.html) {
    return { label: "완료", className: "done" };
  }
  if (s.core || s.academic || s.industry || s.brief || s.html) {
    return { label: "부분 완료", className: "partial" };
  }
  return { label: "분석 필요", className: "missing" };
}

function renderPapers() {
  const root = $("papersList");
  const needle = state.filter.trim().toLowerCase();
  const papers = state.papers.filter((paper) => {
    const haystack = [paper.paper_id, paper.topic, paper.title, paper.doi, paper.venue]
      .join(" ")
      .toLowerCase();
    return !needle || haystack.includes(needle);
  });

  if (!papers.length) {
    root.innerHTML = '<div class="output empty">표시할 분석 자료가 없습니다.</div>';
    return;
  }

  root.innerHTML = papers
    .map((paper) => {
      const s = paper.status || {};
      const title = paper.title || paper.paper_id;
      const progress = paperProgress(s);
      return `
        <article class="paper-row">
          <div>
            <div class="paper-title-row">
              <p class="paper-title">${escapeHtml(title)}</p>
              <span class="progress-badge ${progress.className}">${progress.label}</span>
            </div>
            <div class="paper-meta">
              ${escapeHtml(paper.topic)} / ${escapeHtml(paper.paper_id)}
              ${paper.year ? ` · ${escapeHtml(String(paper.year))}` : ""}
              ${paper.venue ? ` · ${escapeHtml(paper.venue)}` : ""}
              ${paper.doi ? ` · DOI ${escapeHtml(paper.doi)}` : ""}
            </div>
            <div class="badges">
              ${statusBadge("PDF", s.pdf)}
              ${statusBadge("Core", s.core)}
              ${statusBadge("Academic", s.academic)}
              ${statusBadge("Industry", s.industry)}
              ${statusBadge("Brief", s.brief)}
              ${statusBadge("HTML", s.html)}
            </div>
          </div>
          <div class="paper-actions">
            <button type="button" data-action="analyze-paper" data-paper-id="${escapeAttr(paper.paper_id)}">Claude로 분석</button>
            <button type="button" data-action="render" data-path="${escapeAttr(paper.path)}">HTML 보기</button>
            <button type="button" data-action="open-core" data-path="${escapeAttr(`${paper.path}/${paper.paper_id}_core.md`)}">핵심 분석 보기</button>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderRuns() {
  const root = $("runsList");
  if (!state.runs.length) {
    root.innerHTML = "";
    return;
  }

  root.innerHTML = state.runs
    .slice(0, 8)
    .map((run) => {
      const request = run.request || {};
      return `
        <div class="run-row">
          <strong>${escapeHtml(run.run_id)}</strong>
          <div class="run-meta">
            ${escapeHtml(request.source || "source 없음")}
            ${request.topic ? ` · ${escapeHtml(request.topic)}` : ""}
            ${request.mode ? ` · ${escapeHtml(request.mode)}` : ""}
          </div>
          <div class="paper-actions">
            <button type="button" data-action="open-prompt" data-path="${escapeAttr(`${run.path}/prompt.md`)}">요청 불러오기</button>
          </div>
        </div>
      `;
    })
    .join("");
}

async function refreshAll() {
  const [papers, runs] = await Promise.all([api("/api/papers"), api("/api/runs")]);
  state.papers = papers.papers || [];
  state.runs = runs.runs || [];
  renderPapers();
  renderRuns();
  log("Refreshed dashboard", { papers: state.papers.length, runs: state.runs.length });
}

async function createRun(event) {
  event.preventDefault();
  const payload = {
    source: $("sourceInput").value,
    topic: $("topicInput").value,
    mode: $("modeInput").value,
    lens: $("lensInput").value,
    notes: $("notesInput").value,
  };
  const result = await api("/api/run/new", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  $("runOutput").classList.remove("empty");
  $("runOutput").textContent = result.prompt;
  setActivePrompt(result.prompt, result.run_path);
  log("Created run prompt", { run_id: result.run_id, run_path: result.run_path });
  await refreshAll();
}

async function uploadPdf() {
  const input = $("pdfInput");
  const status = $("uploadStatus");
  const file = input.files && input.files[0];
  if (!file) {
    status.textContent = "업로드할 PDF를 먼저 선택하세요.";
    return;
  }
  if (file.type && file.type !== "application/pdf") {
    status.textContent = "PDF 파일만 업로드할 수 있습니다.";
    return;
  }

  const button = $("uploadPdfBtn");
  button.disabled = true;
  status.textContent = "Uploading PDF...";
  try {
    const formData = new FormData();
    formData.append("pdf", file);
    const result = await uploadApi("/api/upload/pdf", formData);
    $("sourceInput").value = result.path;
    status.textContent = `Uploaded: ${result.path}`;
    log("Uploaded PDF", result);
  } finally {
    button.disabled = false;
  }
}

function paperSource(paper) {
  if (paper.doi) return paper.doi;
  return paper.path || paper.paper_id;
}

async function analyzePaper(paperId) {
  const paper = state.papers.find((item) => item.paper_id === paperId);
  if (!paper) {
    throw new Error(`Paper not found: ${paperId}`);
  }

  const payload = {
    source: paperSource(paper),
    topic: paper.topic,
    mode: "full",
    lens: "both",
    notes: [
      `Existing paper folder: ${paper.path}`,
      "Dashboard Analyze button에서 시작한 재분석 요청.",
      "기존 paper-info.yaml이 있으면 그것을 우선 확인하고, missing 산출물(core/lens/brief/html)을 완성한다.",
    ].join("\n"),
  };

  $("sourceInput").value = payload.source;
  $("topicInput").value = payload.topic;
  $("modeInput").value = payload.mode;
  $("lensInput").value = payload.lens;
  $("notesInput").value = payload.notes;

  const result = await api("/api/run/new", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  $("runOutput").classList.remove("empty");
  $("runOutput").textContent = result.prompt;
  setActivePrompt(result.prompt, result.run_path);
  log("Created analysis run from paper row", {
    paper_id: paper.paper_id,
    run_id: result.run_id,
    run_path: result.run_path,
  });

  state.engine = "claude";
  const job = await api("/api/run/start-claude", {
    method: "POST",
    body: JSON.stringify({ run_path: result.run_path }),
  });
  renderJobStatus(job);
  startJobPolling();
  await refreshAll();
  log("Started Claude analysis from paper row", {
    paper_id: paper.paper_id,
    run_id: result.run_id,
    status: job.status,
  });
}

async function buildIndex() {
  const button = $("buildIndexBtn");
  button.disabled = true;
  try {
    const result = await api("/api/run/build-index", { method: "POST", body: "{}" });
    log("Build index finished", result);
    await refreshAll();
  } finally {
    button.disabled = false;
  }
}

async function renderHtml(paperPath) {
  const result = await api("/api/run/render-html", {
    method: "POST",
    body: JSON.stringify({ paper_path: paperPath }),
  });
  log("HTML render finished", result);
  await refreshAll();
  if (result.returncode !== 0) {
    throw new Error(result.stderr || result.stdout || "HTML render failed");
  }
  return htmlViewUrl(paperPath);
}

async function openFile(path) {
  const result = await api(`/api/file?path=${encodeURIComponent(path)}`);
  $("runOutput").classList.remove("empty");
  $("runOutput").textContent = result.content;
  if (path.endsWith("/prompt.md")) {
    setActivePrompt(result.content, path.replace(/\/prompt\.md$/, ""));
    const details = document.querySelector(".prompt-details");
    if (details) details.open = true;
    $("prompt-title").scrollIntoView({ behavior: "smooth", block: "start" });
  }
  log("Loaded file", { path: result.path });
}

function coreViewUrl(path) {
  return `/view/core?path=${encodeURIComponent(path)}`;
}

function htmlViewUrl(paperPath) {
  return `/view/html?paper_path=${encodeURIComponent(paperPath)}`;
}

function openPreviewWindow(url) {
  const preview = window.open(url || "about:blank", "_blank", "noopener");
  if (!preview) {
    log("Preview blocked", { reason: "browser blocked popup window" });
  }
  return preview;
}

function navigatePreview(preview, url) {
  if (preview) {
    preview.location.href = url;
  } else {
    window.location.href = url;
  }
}

function setActivePrompt(prompt, runPath) {
  state.activePrompt = prompt;
  state.activeRunPath = runPath || "";
  stopJobPolling();
  $("promptOutput").value = prompt;
  $("jobStatus").className = "job-status ready";
  $("jobStatus").textContent = state.activeRunPath
    ? `Ready to run: ${state.activeRunPath}`
    : "Prompt loaded without a saved run path.";
  $("jobArtifacts").innerHTML = "";
  $("jobLog").textContent = "Run in Codex를 누르면 이 위치에 실행 로그와 생성 파일 상태가 표시됩니다.";
}

async function copyPrompt() {
  const prompt = $("promptOutput").value;
  if (!prompt || prompt.startsWith("Create Run Prompt")) {
    log("Copy skipped", { reason: "no prompt loaded" });
    return;
  }
  await navigator.clipboard.writeText(prompt);
  log("Copied prompt");
}

function downloadPrompt() {
  const prompt = $("promptOutput").value;
  if (!prompt || prompt.startsWith("Create Run Prompt")) {
    log("Download skipped", { reason: "no prompt loaded" });
    return;
  }
  const blob = new Blob([prompt], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "paper-analysis-request.md";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  log("Downloaded prompt");
}

async function runEngine(engine) {
  if (!state.activeRunPath) {
    log("Run skipped", { reason: "create or open a run prompt first" });
    return;
  }
  state.engine = engine;
  const button = engine === "claude" ? $("runClaudeBtn") : $("runCodexBtn");
  button.disabled = true;
  try {
    const result = await api(`/api/run/start-${engine}`, {
      method: "POST",
      body: JSON.stringify({ run_path: state.activeRunPath }),
    });
    renderJobStatus(result);
    startJobPolling();
    log(`Started ${ENGINE_LABEL[engine] || engine} job`, result);
  } finally {
    button.disabled = false;
  }
}

async function refreshJob() {
  if (!state.activeRunPath) {
    log("Status skipped", { reason: "create or open a run prompt first" });
    return;
  }
  const engine = state.engine || "codex";
  const result = await api(`/api/run/${engine}-status?run_path=${encodeURIComponent(state.activeRunPath)}`);
  renderJobStatus(result);
  if (result.status === "running") {
    startJobPolling();
  } else {
    stopJobPolling();
  }
  log(`Refreshed ${ENGINE_LABEL[engine] || engine} job`, {
    status: result.status,
    returncode: result.returncode,
    log_path: result.log_path,
  });
}

function renderJobStatus(job) {
  const status = job.status || "unknown";
  const engine = job.engine || state.engine || "codex";
  const name = ENGINE_LABEL[engine] || engine;
  const statusText = {
    running: `Running: ${name}가 분석을 진행 중입니다. 이 화면은 5초마다 자동 갱신됩니다.`,
    succeeded: `Succeeded: ${name} 실행이 정상 종료되었습니다.`,
    failed: `Failed: ${name} 실행이 실패했습니다. 아래 로그에서 원인을 확인하세요.`,
    "finished-unknown": "Finished: 대시보드 재시작으로 반환 코드는 알 수 없지만, 로그와 산출물은 확인할 수 있습니다.",
    "not-started": `Not started: 아직 ${name} 분석을 시작하지 않았습니다.`,
    "invalid-status": `Status file is invalid: ${engine}-job.json을 읽을 수 없습니다.`,
  }[status] || `Status: ${status}`;
  const details = [
    job.pid ? `PID ${job.pid}` : "",
    job.returncode !== undefined && job.returncode !== null ? `return ${job.returncode}` : "",
    job.log_path ? job.log_path : "",
  ].filter(Boolean).join(" | ");

  $("jobStatus").className = `job-status ${statusClass(status)}`;
  $("jobStatus").innerHTML = `
    <strong>${escapeHtml(statusText)}</strong>
    ${details ? `<span>${escapeHtml(details)}</span>` : ""}
    ${job.note ? `<small>${escapeHtml(job.note)}</small>` : ""}
  `;

  renderJobArtifacts(job.outputs);
  $("jobLog").textContent = job.log_tail
    ? job.log_tail
    : `아직 ${engine}.log 내용이 없습니다. 실행 직후라면 몇 초 뒤 상태 새로고침을 눌러보세요.`;
}

function statusClass(status) {
  if (status === "running") return "running";
  if (status === "succeeded") return "succeeded";
  if (status === "failed" || status === "invalid-status") return "failed";
  if (status === "finished-unknown") return "finished-unknown";
  if (status === "not-started") return "not-started";
  return "ready";
}

function renderJobArtifacts(outputs) {
  const root = $("jobArtifacts");
  if (!outputs || !outputs.paper_dir) {
    root.innerHTML = `
      <div class="artifact-summary">아직 분석 결과 폴더가 감지되지 않았습니다.</div>
    `;
    return;
  }

  const badges = Object.entries(outputs.files || {})
    .map(([label, done]) => {
      const mark = done ? "created" : "missing";
      return `<span class="artifact-badge ${done ? "done" : "missing"}">${escapeHtml(label)}: ${mark}</span>`;
    })
    .join("");

  root.innerHTML = `
    <div class="artifact-summary">
      <strong>생성 위치</strong>
      <code>${escapeHtml(outputs.paper_dir)}</code>
    </div>
    <div class="artifact-list">${badges}</div>
  `;
}

function startJobPolling() {
  if (state.jobPoller) return;
  state.jobPoller = window.setInterval(() => {
    refreshJob().catch((error) => {
      stopJobPolling();
      log("Auto status refresh failed", { error: error.message });
    });
  }, 5000);
}

function stopJobPolling() {
  if (!state.jobPoller) return;
  window.clearInterval(state.jobPoller);
  state.jobPoller = null;
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("'", "&#039;");
}

document.addEventListener("click", async (event) => {
  const target = event.target.closest("button");
  if (!target) return;
  const scrollTarget = target.dataset.scrollTarget;
  if (scrollTarget) {
    const element = $(scrollTarget);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    return;
  }
  const action = target.dataset.action;
  const path = target.dataset.path;
  try {
    if (action === "render") {
      const preview = openPreviewWindow();
      target.disabled = true;
      const url = await renderHtml(path);
      target.disabled = false;
      navigatePreview(preview, url);
    } else if (action === "analyze-paper") {
      target.disabled = true;
      await analyzePaper(target.dataset.paperId);
      target.disabled = false;
    } else if (action === "open-core" || action === "open-prompt") {
      if (action === "open-core") {
        openPreviewWindow(coreViewUrl(path));
      } else {
        await openFile(path);
      }
    }
  } catch (error) {
    target.disabled = false;
    log("Action failed", { error: error.message });
  }
});

$("newRunForm").addEventListener("submit", (event) => {
  createRun(event).catch((error) => log("Create run failed", { error: error.message }));
});

$("refreshBtn").addEventListener("click", () => {
  refreshAll().catch((error) => log("Refresh failed", { error: error.message }));
});

$("buildIndexBtn").addEventListener("click", () => {
  buildIndex().catch((error) => log("Build index failed", { error: error.message }));
});

$("uploadPdfBtn").addEventListener("click", () => {
  uploadPdf().catch((error) => {
    $("uploadStatus").textContent = `Upload failed: ${error.message}`;
    log("PDF upload failed", { error: error.message });
  });
});

$("runCodexBtn").addEventListener("click", () => {
  runEngine("codex").catch((error) => log("Run Codex failed", { error: error.message }));
});

$("runClaudeBtn").addEventListener("click", () => {
  runEngine("claude").catch((error) => log("Run Claude failed", { error: error.message }));
});

$("refreshJobBtn").addEventListener("click", () => {
  refreshJob().catch((error) => log("Refresh job failed", { error: error.message }));
});

$("copyPromptBtn").addEventListener("click", () => {
  copyPrompt().catch((error) => log("Copy failed", { error: error.message }));
});

$("downloadPromptBtn").addEventListener("click", () => {
  downloadPrompt();
});

$("filterInput").addEventListener("input", (event) => {
  state.filter = event.target.value;
  renderPapers();
});

$("tokenInput").value = state.token;
$("tokenInput").addEventListener("input", (event) => {
  state.token = event.target.value;
  localStorage.setItem("biop01_dashboard_token", state.token);
});

refreshAll().catch((error) => log("Initial load failed", { error: error.message }));

/* ---------- Interactive tutorial (2026-06-09, ported continuation) ---------- */
const TUTORIAL_STEPS = [
  {
    target: null,
    title: "BioProject01 대시보드 둘러보기",
    body: "이 화면은 논문 분석 하네스를 클릭으로 실행하는 조작판입니다. 자료 입력 → 분석 실행 → 결과 확인 순서로 진행합니다. ‘다음’으로 각 단계를 살펴보세요.",
  },
  {
    target: "new-run-title",
    title: "1. 자료 입력",
    body: "분석할 논문을 지정합니다. PDF를 업로드하거나 DOI·URL·로컬 PDF 경로를 Source에 입력합니다. PDF를 올리면 파일 경로가 Source에 자동으로 채워집니다.",
  },
  {
    target: "new-run-title",
    title: "옵션 선택 후 요청 만들기",
    body: "Topic, Mode(full·abstract·core·question), Lens(academic·industry)를 고르고 Notes에 강조할 점을 적은 뒤 ‘요청 만들기’를 누르면 실행 요청이 생성됩니다.",
  },
  {
    target: "prompt-title",
    title: "2. 분석 실행",
    body: "‘Claude로 분석’ 또는 ‘Codex로 분석’을 누르면 저장된 요청으로 분석이 실행됩니다. 상태 카드, 생성 파일 배지, 실행 로그가 이 영역에 표시되고 ‘상태 새로고침’으로 진행 상황을 갱신합니다.",
  },
  {
    target: "papers-title",
    title: "3. 결과 확인",
    body: "분석된 자료 목록입니다. 배지가 missing이면 아직 산출물이 없고 done이면 생성된 것입니다. 각 행에서 Render HTML·View Core로 결과를 새 탭에서 엽니다.",
  },
  {
    target: "tokenInput",
    title: "팀 공유와 인덱스",
    body: "상단 Team token으로 LAN 공유 접근을 인증하고, Build Index로 분석 인덱스를 갱신합니다. 이 튜토리얼은 우측 상단 ‘❓ 튜토리얼’ 버튼으로 언제든 다시 볼 수 있습니다.",
  },
];

let tutorialIndex = 0;

function tutorialClearSpot() {
  document.querySelectorAll(".tutorial-spot").forEach((el) => el.classList.remove("tutorial-spot"));
}

function tutorialTargetEl(step) {
  if (!step.target) return null;
  const el = $(step.target);
  if (!el) return null;
  return el.closest(".panel, .workflow-guide, .topbar") || el;
}

function renderTutorialStep() {
  const step = TUTORIAL_STEPS[tutorialIndex];
  $("tutorialCounter").textContent = `${tutorialIndex + 1} / ${TUTORIAL_STEPS.length}`;
  $("tutorialTitle").textContent = step.title;
  $("tutorialBody").textContent = step.body;
  $("tutorialDots").innerHTML = TUTORIAL_STEPS
    .map((_, i) => `<span class="${i === tutorialIndex ? "active" : ""}"></span>`)
    .join("");
  $("tutorialPrev").disabled = tutorialIndex === 0;
  $("tutorialNext").textContent = tutorialIndex === TUTORIAL_STEPS.length - 1 ? "완료" : "다음";
  tutorialClearSpot();
  const el = tutorialTargetEl(step);
  if (el) {
    el.classList.add("tutorial-spot");
    el.scrollIntoView({ behavior: "smooth", block: "center" });
  } else {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

function openTutorial(index = 0) {
  tutorialIndex = index;
  $("tutorialOverlay").hidden = false;
  renderTutorialStep();
}

function closeTutorial() {
  $("tutorialOverlay").hidden = true;
  tutorialClearSpot();
  localStorage.setItem("biop01_tutorial_seen", "1");
}

$("tutorialBtn").addEventListener("click", () => openTutorial(0));
$("tutorialClose").addEventListener("click", closeTutorial);
$("tutorialSkip").addEventListener("click", closeTutorial);
$("tutorialPrev").addEventListener("click", () => {
  if (tutorialIndex > 0) {
    tutorialIndex -= 1;
    renderTutorialStep();
  }
});
$("tutorialNext").addEventListener("click", () => {
  if (tutorialIndex < TUTORIAL_STEPS.length - 1) {
    tutorialIndex += 1;
    renderTutorialStep();
  } else {
    closeTutorial();
  }
});
document.addEventListener("keydown", (event) => {
  if ($("tutorialOverlay").hidden) return;
  if (event.key === "Escape") closeTutorial();
  else if (event.key === "ArrowRight") $("tutorialNext").click();
  else if (event.key === "ArrowLeft") $("tutorialPrev").click();
});

if (!localStorage.getItem("biop01_tutorial_seen")) {
  openTutorial(0);
}
