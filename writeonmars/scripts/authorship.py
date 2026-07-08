#!/usr/bin/env python3
"""writeonmars authorship — informe determinista de autoría humana."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

AGENT_DOMAIN = "@agents.writeonmars.invalid"
MANUSCRIPT_STEPS = {"implement", "revise", "intro"}


def die(message: str, code: int) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[authorship] error: {message}", file=sys.stderr)
    sys.exit(code)


def run_git(project: Path, *args: str) -> str:
    if shutil.which("git") is None:
        die("git no está disponible", 3)
    result = subprocess.run(
        ["git", "-C", str(project), *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        die(result.stderr.strip() or f"git {' '.join(args)} falló", 1)
    return result.stdout


def latest_spec_dir(project: Path) -> Path:
    specs = project / "specs"
    dirs = sorted(d for d in specs.iterdir() if d.is_dir() and (d / "spec.md").exists()) if specs.is_dir() else []
    if not dirs:
        die("sin specs/<feature>/spec.md; no hay destino para el informe", 1)
    return dirs[-1]


def parse_ts(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def chapter_from_path(path: str) -> str:
    m = re.match(r"chapters/(\d+)", path)
    if not m:
        return "sin_ordinal"
    return str(int(m.group(1)))


def read_decisions(project: Path) -> list[dict]:
    path = project / "decisions.jsonl"
    if not path.exists():
        return []
    out = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            die(f"{path}:{idx} no es DecisionRecord válido: {exc}", 1)
    return out


def dispatch_windows(project: Path) -> list[dict]:
    windows: list[dict] = []
    open_dispatches: list[dict] = []
    for record in read_decisions(project):
        event = record.get("event")
        step = record.get("step")
        if step not in MANUSCRIPT_STEPS:
            continue
        if event == "dispatch":
            open_dispatches.append(record)
            continue
        if event != "disposition":
            continue
        pos = next(
            (
                idx for idx, item in enumerate(open_dispatches)
                if item.get("step") == step and item.get("chapter") == record.get("chapter")
            ),
            None,
        )
        if pos is None:
            continue
        start_record = open_dispatches.pop(pos)
        start = parse_ts(start_record.get("ts", ""))
        end = parse_ts(record.get("ts", ""))
        if start and end:
            windows.append({
                "step": step,
                "chapter": str(record.get("chapter") or "global"),
                "start": start,
                "end": end,
            })
    return windows


def in_agent_window(chapter: str, commit_ts: datetime | None, windows: list[dict]) -> bool:
    if commit_ts is None:
        return False
    for window in windows:
        w_chapter = window["chapter"]
        if w_chapter not in {chapter, "global"}:
            continue
        if window["start"] <= commit_ts <= window["end"]:
            return True
    return False


def git_chapter_commits(project: Path) -> tuple[str, dict[str, dict]]:
    run_git(project, "rev-parse", "--is-inside-work-tree")
    head = run_git(project, "rev-parse", "HEAD").strip()
    raw = run_git(
        project,
        "log",
        "--format=@@@%H%x1f%an%x1f%ae%x1f%cI",
        "--numstat",
        "--",
        "chapters",
    )
    if not raw.strip():
        die("sin commits que toquen chapters/; no hay evidencia que informar", 1)
    chapters: dict[str, dict] = {}
    current: dict | None = None
    windows = dispatch_windows(project)
    for line in raw.splitlines():
        if line.startswith("@@@"):
            sha, author, email, ts = line[3:].split("\x1f")
            current = {"sha": sha, "author": author, "email": email, "ts": ts}
            continue
        if not line.strip() or current is None:
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        path = parts[2]
        if not path.startswith("chapters/"):
            continue
        chapter = chapter_from_path(path)
        commit_ts = parse_ts(current["ts"])
        by_identity = current["email"].endswith(AGENT_DOMAIN)
        by_window = in_agent_window(chapter, commit_ts, windows)
        clase = "agente" if by_identity or by_window else "humano"
        razon = "identidad" if by_identity else ("ventana_dispatch" if by_window else "git")
        bucket = chapters.setdefault(chapter, {"file": path, "commits": []})
        bucket["file"] = path
        bucket["commits"].append({
            "sha": current["sha"],
            "author": current["author"],
            "email": current["email"],
            "clase": clase,
            "razon": razon,
        })
    if not chapters:
        die("sin commits que toquen chapters/; no hay evidencia que informar", 1)
    return head, chapters


def verdict(commits: list[dict]) -> str:
    humans = any(c["clase"] == "humano" for c in commits)
    agents = any(c["clase"] == "agente" for c in commits)
    if humans and agents:
        return "mixta"
    if agents:
        return "ia"
    return "humana"


def build_report(project: Path) -> dict:
    head, chapters = git_chapter_commits(project)
    ordered: dict[str, dict] = {}
    for chapter in sorted(chapters, key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x)):
        info = chapters[chapter]
        info["commits"] = sorted(info["commits"], key=lambda c: c["sha"])
        info["veredicto"] = verdict(info["commits"])
        ordered[chapter] = info
    global_verdict = (
        "autoria_humana_demostrada"
        if ordered and all(info["veredicto"] == "humana" for info in ordered.values())
        else ("ia" if ordered and all(info["veredicto"] == "ia" for info in ordered.values()) else "mixta")
    )
    return {
        "head": head,
        "chapters": ordered,
        "veredicto_global": global_verdict,
    }


def markdown(report: dict) -> str:
    lines = [
        "# Informe de autoría humana",
        "",
        f"HEAD: `{report['head']}`",
        f"Veredicto global: `{report['veredicto_global']}`",
        "",
    ]
    for chapter, info in report["chapters"].items():
        lines.extend([
            f"## Capítulo {chapter}",
            "",
            f"Archivo: `{info['file']}`",
            f"Veredicto: `{info['veredicto']}`",
            "",
            "| Commit | Autor | Email | Clase | Razón |",
            "|--------|-------|-------|-------|-------|",
        ])
        for commit in info["commits"]:
            lines.append(
                f"| `{commit['sha'][:12]}` | {commit['author']} | {commit['email']} | "
                f"{commit['clase']} | {commit['razon']} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Genera el informe de autoría humana.")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()

    project = Path(args.project_dir).resolve()
    report = build_report(project)
    out = Path(args.out) if args.out else latest_spec_dir(project) / "authorship-report.md"
    out.write_text(markdown(report), encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
