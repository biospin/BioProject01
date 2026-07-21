"""P2 공통 유틸 — runtime/peak-memory 로깅 (DESIGN §4D 자원/안정성)."""
from __future__ import annotations
import csv, time, resource, sys, subprocess
from datetime import datetime, timezone
from pathlib import Path


def _git_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL,
            cwd=str(Path(__file__).resolve().parent)).decode().strip()
    except Exception:
        return "unknown"


def peak_mem_mb():
    """현재 프로세스 peak RSS(MB). macOS는 byte, linux는 KB 단위라 보정."""
    ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(ru / (1024**2 if sys.platform == "darwin" else 1024), 1)


class timer:
    """with timer() as t: ...  → t.sec."""
    def __enter__(self):
        self._t0 = time.perf_counter(); return self
    def __exit__(self, *a):
        self.sec = round(time.perf_counter() - self._t0, 1)


def log_runtime(csv_path, *, method, arm, n_cells, n_genes, wall_sec, peak_mb, note=""):
    """results/runtime.csv 에 한 행 append (tracked 요약)."""
    csv_path = Path(csv_path); csv_path.parent.mkdir(parents=True, exist_ok=True)
    new = not csv_path.exists()
    with open(csv_path, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["timestamp_utc", "method", "arm", "n_cells", "n_genes",
                        "wall_sec", "peak_mem_mb", "commit", "note"])
        w.writerow([datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    method, arm, n_cells, n_genes, wall_sec, peak_mb, _git_commit(), note])
    print(f"  [runtime] {method}/{arm}: {wall_sec}s, peak {peak_mb}MB → {csv_path.name}")
