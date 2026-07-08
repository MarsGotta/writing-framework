"""Tests de authorship.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def git(project: Path, *args: str, env: dict | None = None) -> str:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    result = subprocess.run(
        ["git", "-C", str(project), *args],
        capture_output=True,
        text=True,
        env=merged,
        check=True,
    )
    return result.stdout


def commit_file(project: Path, path: str, text: str, author: str, email: str, date: str) -> None:
    target = project / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    git(project, "add", path)
    env = {
        "GIT_AUTHOR_NAME": author,
        "GIT_AUTHOR_EMAIL": email,
        "GIT_AUTHOR_DATE": date,
        "GIT_COMMITTER_NAME": author,
        "GIT_COMMITTER_EMAIL": email,
        "GIT_COMMITTER_DATE": date,
    }
    git(project, "commit", "-m", f"add {path}", env=env)


def make_repo(tmp_path: Path) -> Path:
    project = tmp_path / "repo"
    project.mkdir()
    git(project, "init")
    (project / "specs/001-estudio").mkdir(parents=True)
    (project / "specs/001-estudio/spec.md").write_text("# Spec\n", encoding="utf-8")
    commit_file(
        project,
        "chapters/001-uno.md",
        "# Uno\n\nTexto humano.\n",
        "Marcela",
        "marcela@example.com",
        "2026-01-01T00:00:00+00:00",
    )
    commit_file(
        project,
        "chapters/001-uno.md",
        "# Uno\n\nTexto agente.\n",
        "Redactora",
        "redactora@agents.writeonmars.invalid",
        "2026-01-02T00:00:00+00:00",
    )
    commit_file(
        project,
        "chapters/002-dos.md",
        "# Dos\n\nTexto humano.\n",
        "Marcela",
        "marcela@example.com",
        "2026-01-03T00:00:00+00:00",
    )
    commit_file(
        project,
        "chapters/003-tres.md",
        "# Tres\n\nTexto en ventana.\n",
        "Marcela",
        "marcela@example.com",
        "2026-01-04T00:30:00+00:00",
    )
    (project / "decisions.jsonl").write_text(
        "\n".join([
            '{"v":1,"ts":"2026-01-04T00:00:00Z","event":"dispatch","step":"implement","chapter":"3","role":"redactora"}',
            '{"v":1,"ts":"2026-01-04T01:00:00Z","event":"disposition","step":"implement","chapter":"3","role":"redactora","outcome":"ok"}',
        ]) + "\n",
        encoding="utf-8",
    )
    return project


def run_authorship(scripts_dir: Path, project: Path):
    return subprocess.run(
        [sys.executable, str(scripts_dir / "authorship.py"), "--project-dir", str(project), "--json"],
        capture_output=True,
        text=True,
    )


def test_authorship_clasifica_y_es_determinista(scripts_dir, tmp_path):
    project = make_repo(tmp_path)
    first = run_authorship(scripts_dir, project)
    second = run_authorship(scripts_dir, project)
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert first.stdout == second.stdout
    report = json.loads(first.stdout)
    assert report["chapters"]["1"]["veredicto"] == "mixta"
    assert report["chapters"]["2"]["veredicto"] == "humana"
    assert report["chapters"]["3"]["veredicto"] == "ia"
    assert report["chapters"]["3"]["commits"][0]["razon"] == "ventana_dispatch"
    assert report["veredicto_global"] == "mixta"
    assert (project / "specs/001-estudio/authorship-report.md").is_file()


def test_authorship_sin_repo_falla(scripts_dir, tmp_path):
    project = tmp_path / "no-repo"
    project.mkdir()
    res = run_authorship(scripts_dir, project)
    assert res.returncode == 1
