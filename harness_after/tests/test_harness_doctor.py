#!/usr/bin/env python3
"""test_harness_doctor.py — 정합성 게이트(harness_doctor.py)의 검증 테스트.

왜 필요한가: harness_doctor는 "하네스 구성이 맞는지" 판정하는 게이트다.
게이트가 틀리면 잘못된 PASS(놓침) 또는 잘못된 FAIL(오검)이 그대로 팀 판단이 된다.
그래서 게이트 자체를 검증한다 — 합성 리포를 만들어 **알려진 정답**과 대조한다.

의존성: 표준 라이브러리 + PyYAML(doctor가 사용). pytest 불필요.
실행:  python harness_after/tests/test_harness_doctor.py
종료코드: 0=전부 통과, 1=실패 있음
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
DOCTOR = os.path.join(HERE, "..", "scripts", "harness_doctor.py")


BASE_MANIFEST = """\
harness_version: 1
project_profile: test
roles:
  analyst:
    type: agent
    path: .claude/agents/analyst.md
    required: true
    implemented: true
  venue_reviewer:
    aka: [reviewer]
    type: agent
    path: .claude/agents/venue-reviewer.md
    required: false
    implemented: false
artifacts:
  findings: results/FINDINGS.md
execution:
  require_repo_root: true
doc_reference_scan:
  files:
%(scan_files)s
path_reference_scan:
  enabled: %(path_scan)s
  resolve_by_basename: true
  files:
%(scan_files)s
%(local_only)s  ignore:
    - "^https?://"
    - "^upstream/"
"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class DoctorCase(unittest.TestCase):
    """합성 리포를 만들고 doctor를 서브프로세스로 돌려 결과를 대조한다."""

    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="harness_doctor_test_")
        # repo 루트 표식 + 실재하는 역할/산출물
        write(os.path.join(self.repo, "CLAUDE.md"), "# test repo\n")
        write(os.path.join(self.repo, ".claude/agents/analyst.md"), "agent\n")
        write(os.path.join(self.repo, "results/FINDINGS.md"), "findings\n")

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def manifest(self, scan_files=("CLAUDE.md",), path_scan="true", local_only=()):
        lo = ""
        if local_only:
            lo = "  local_only:\n" + "".join("    - %s\n" % f for f in local_only)
        body = BASE_MANIFEST % {
            "scan_files": "".join("    - %s\n" % f for f in scan_files),
            "path_scan": path_scan,
            "local_only": lo,
        }
        write(os.path.join(self.repo, "harness.yaml"), body)

    def run_doctor(self, repo=None):
        r = subprocess.run(
            [sys.executable, DOCTOR, "--repo", repo or self.repo,
             "--manifest", "harness.yaml"],
            capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    # ---- 1. 정상 구성이면 통과해야 한다 (잘못된 FAIL이 없는지) ----
    def test_clean_repo_passes(self):
        write(os.path.join(self.repo, "CLAUDE.md"), "# test\n`results/FINDINGS.md` 를 읽는다.\n")
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 0, "정상 구성인데 FAIL — 오검\n" + out)
        self.assertIn("RESULT: PASS", out)

    # ---- 2. 구현했다고 선언한 역할 파일이 없으면 FAIL ----
    def test_missing_implemented_role_fails(self):
        os.remove(os.path.join(self.repo, ".claude/agents/analyst.md"))
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 1, out)
        self.assertIn("[role]", out)

    # ---- 3. 팬텀 에이전트: 백틱 인용(강한 참조)은 FAIL ----
    def test_phantom_agent_backtick_fails(self):
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n| 정식 리뷰 | `reviewer` (선택) |\n")
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 1, out)
        self.assertIn("[phantom-agent]", out)

    # ---- 4. 팬텀 에이전트: 표 행(강한 참조)도 FAIL ----
    def test_phantom_agent_table_row_fails(self):
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n| 리뷰 | paper-critic / reviewer | 노트 |\n")
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 1, out)
        self.assertIn("[phantom-agent]", out)

    # ---- 5. 팬텀 에이전트: 산문 언급은 WARN, FAIL 아님 (kkkim 오검 지적) ----
    def test_phantom_agent_prose_only_warns(self):
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n심사자(a real reviewer)가 지적하기 전에 잡는다.\n")
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 0, "산문 언급을 FAIL 처리 — 오검\n" + out)
        self.assertIn("[phantom-agent?]", out)
        self.assertIn("RESULT: PASS", out)

    # ---- 6. 팬텀 경로: 실재하지 않는 인용 경로는 FAIL ----
    def test_phantom_path_fails(self):
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n라우팅은 `skills/ROUTES.md` 에 위임한다.\n")
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 1, out)
        self.assertIn("[phantom-path]", out)
        self.assertIn("skills/ROUTES.md", out)

    # ---- 7. 상대 인용은 basename으로 해석되어 FAIL 아님 ----
    def test_relative_reference_resolves(self):
        write(os.path.join(self.repo, "pipeline/scripts/p3_concordance.py"), "#\n")
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n검증 게이트는 `p3_concordance.py` 재계산.\n")
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 0, "상대 인용을 팬텀으로 오검\n" + out)

    # ---- 8. ignore 규칙에 걸리는 외부 참조는 FAIL 아님 ----
    def test_ignored_external_reference(self):
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n상류는 `upstream/paper-production-harness` 다.\n")
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 0, "ignore 규칙이 동작하지 않음\n" + out)

    # ---- 9. 산출물 부재는 WARN (아직 안 만든 단계일 수 있음) ----
    def test_missing_artifact_warns_not_fails(self):
        os.remove(os.path.join(self.repo, "results/FINDINGS.md"))
        self.manifest()
        code, out = self.run_doctor()
        self.assertEqual(code, 0, "산출물 부재를 FAIL 처리 — 과잉\n" + out)
        self.assertIn("[artifact]", out)

    # ---- 10. repo 루트가 아니면 FAIL (BIOP01-65 실행 전제) ----
    def test_require_repo_root(self):
        self.manifest()
        sub = os.path.join(self.repo, "sub")
        os.makedirs(sub, exist_ok=True)
        shutil.copy(os.path.join(self.repo, "harness.yaml"), os.path.join(sub, "harness.yaml"))
        code, out = self.run_doctor(repo=sub)
        self.assertEqual(code, 1, out)
        self.assertIn("[execution]", out)

    # ---- 11. 스캔 대상에서 빠진 문서의 팬텀은 검출되지 않는다 ----
    #      (= "스코프가 곧 성능" — 2026-07-26 2차 조사에서 실제로 겪은 실패 모드)
    def test_scope_gap_is_real(self):
        write(os.path.join(self.repo, "AGENTS.md"),
              "# router\n라우팅은 `skills/ROUTES.md` 에 위임한다.\n")
        self.manifest(scan_files=("CLAUDE.md",))          # AGENTS.md 미포함
        code_before, out_before = self.run_doctor()
        self.manifest(scan_files=("CLAUDE.md", "AGENTS.md"))  # 포함
        code_after, out_after = self.run_doctor()
        self.assertEqual(code_before, 0, "스코프 밖인데 검출됨 — 테스트 전제 오류\n" + out_before)
        self.assertEqual(code_after, 1, "스코프에 넣었는데 미검출 — 회귀\n" + out_after)
        self.assertIn("skills/ROUTES.md", out_after)

    # ---- 12. path_reference_scan을 끄면 경로 검사가 돌지 않는다 ----
    def test_path_scan_toggle(self):
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n`skills/ROUTES.md` 참조.\n")
        self.manifest(path_scan="false")
        code, out = self.run_doctor()
        self.assertEqual(code, 0, out)
        self.assertNotIn("[phantom-path]", out)

    # ---- 13. local_only: gitignore 돼 있으면 부재해도 통과 ----
    #      개인 작업기록(HANDOFF/TODO/SESSION-LOG)은 78a5a92(2026-07-01)에서 의도적으로 untrack.
    #      계약이 이들을 "필수 산출물"로 지시하지만 리포에는 없는 게 정상이다.
    def test_local_only_absent_but_gitignored_passes(self):
        subprocess.run(["git", "init", "-q", self.repo], check=True)
        write(os.path.join(self.repo, ".gitignore"), "HANDOFF.md\n")
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n세션 종료 시 `HANDOFF.md` 를 갱신한다(로컬 전용).\n")
        self.manifest(local_only=("HANDOFF.md",))
        code, out = self.run_doctor()
        self.assertEqual(code, 0, "gitignore된 로컬 전용 파일을 팬텀으로 오검\n" + out)
        self.assertIn("[local-only]", out)

    # ---- 14. local_only인데 .gitignore에 없으면 FAIL (실수로 커밋될 위험) ----
    def test_local_only_not_gitignored_fails(self):
        subprocess.run(["git", "init", "-q", self.repo], check=True)
        write(os.path.join(self.repo, ".gitignore"), "nothing\n")
        write(os.path.join(self.repo, "CLAUDE.md"),
              "# test\n세션 종료 시 `HANDOFF.md` 를 갱신한다.\n")
        self.manifest(local_only=("HANDOFF.md",))
        code, out = self.run_doctor()
        self.assertEqual(code, 1, out)
        self.assertIn("[local-only]", out)


class LiveRepoCase(unittest.TestCase):
    """실제 BIOP01 리포에 대한 회귀 확인 — 알려진 결함이 계속 잡히는가."""

    REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

    def test_known_defects_detected(self):
        manifest = os.path.join(self.REPO, "harness.yaml")
        tmp_placed = False
        if not os.path.exists(manifest):
            shutil.copy(os.path.join(HERE, "..", "harness.yaml"), manifest)
            tmp_placed = True
        try:
            r = subprocess.run(
                [sys.executable, DOCTOR, "--repo", self.REPO, "--manifest", "harness.yaml"],
                capture_output=True, text=True)
            out = r.stdout + r.stderr
            if "CLAUDE.md" not in out and r.returncode == 2:
                self.skipTest("BIOP01 리포 컨텍스트 아님")
            # 2026-07-26 2차 조사에서 확인된 결함들이 계속 잡혀야 한다
            for expected in ("skills/ROUTES.md",):
                self.assertIn(expected, out, "알려진 결함 미검출: %s\n%s" % (expected, out))
        finally:
            if tmp_placed:
                os.remove(manifest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
