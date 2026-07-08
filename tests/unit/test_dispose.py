"""Tests de dispose.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def init_git_identity(project: Path, email: str = "marcela@example.com") -> None:
    subprocess.run(["git", "-C", str(project), "init"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(project), "config", "user.name", "Marcela"], check=True)
    subprocess.run(["git", "-C", str(project), "config", "user.email", email], check=True)


def run_dispose(scripts_dir: Path, project: Path, *args: str):
    return subprocess.run(
        [sys.executable, str(scripts_dir / "dispose.py"), *args, "--project-dir", str(project)],
        capture_output=True,
        text=True,
    )


def test_aceptar_actualiza_estado_y_jsonl(scripts_dir, estudio_project):
    init_git_identity(estudio_project)
    res = run_dispose(scripts_dir, estudio_project, "F-1.1", "--aceptar", "--json")
    assert res.returncode == 0, res.stderr
    record = json.loads(res.stdout)
    assert record["finding_id"] == "F-1.1"
    assert record["disposicion"] == "aceptado"
    findings = (estudio_project / "specs/001-estudio/findings.md").read_text(encoding="utf-8")
    assert "| F-1.1 | 1 | critico | frase | problema crítico | sugerencia | resuelto | [] |" in findings
    lines = (estudio_project / "specs/001-estudio/disposiciones.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["actor"] == "Marcela"


def test_rechazar_requiere_motivo(scripts_dir, estudio_project):
    init_git_identity(estudio_project)
    res = run_dispose(scripts_dir, estudio_project, "F-1.2", "--rechazar")
    assert res.returncode == 2


def test_rechazar_y_aplazar(scripts_dir, estudio_project):
    init_git_identity(estudio_project)
    reject = run_dispose(
        scripts_dir,
        estudio_project,
        "F-1.2",
        "--rechazar",
        "--motivo",
        "decisión editorial",
    )
    defer = run_dispose(scripts_dir, estudio_project, "F-1.3", "--aplazar")
    assert reject.returncode == 0, reject.stderr
    assert defer.returncode == 0, defer.stderr
    findings = (estudio_project / "specs/001-estudio/findings.md").read_text(encoding="utf-8")
    assert "desviacion_justificada" in findings
    assert "aplazado" in findings


def test_no_funciona_en_produccion(scripts_dir, estudio_project, repo_root):
    init_git_identity(estudio_project)
    (estudio_project / ".writeonmars-manifest.json").write_text(
        (repo_root / "tests/fixtures/005-estudio/manifests/produccion.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    res = run_dispose(scripts_dir, estudio_project, "F-1.1", "--aceptar")
    assert res.returncode == 1


def test_rechaza_identidad_de_agente(scripts_dir, estudio_project):
    init_git_identity(estudio_project, email="redactora@agents.writeonmars.invalid")
    res = run_dispose(scripts_dir, estudio_project, "F-1.1", "--aceptar")
    assert res.returncode == 3


def test_estado_final_no_admite_nueva_disposicion(scripts_dir, estudio_project):
    init_git_identity(estudio_project)
    assert run_dispose(scripts_dir, estudio_project, "F-1.1", "--aceptar").returncode == 0
    again = run_dispose(scripts_dir, estudio_project, "F-1.1", "--aceptar")
    assert again.returncode == 1


def test_atomicidad_sin_linea_huerfana(dispose_mod, estudio_project, monkeypatch):
    init_git_identity(estudio_project)
    findings = estudio_project / "specs/001-estudio/findings.md"
    original = findings.read_text(encoding="utf-8")
    calls = {"replace": 0}

    def flaky_replace(src, dst):
        calls["replace"] += 1
        if calls["replace"] == 2:
            raise OSError("fallo simulado")
        return dispose_mod.os.rename(src, dst)

    monkeypatch.setattr(dispose_mod.os, "replace", flaky_replace)
    monkeypatch.setattr(
        sys,
        "argv",
        ["dispose.py", "F-1.1", "--aceptar", "--project-dir", str(estudio_project)],
    )
    with pytest.raises(OSError):
        dispose_mod.main()
    assert findings.read_text(encoding="utf-8") == original
    assert not (estudio_project / "specs/001-estudio/disposiciones.jsonl").exists()
