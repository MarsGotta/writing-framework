"""Tests de track.py (feature 006, US3 — escalar sin tirar trabajo).

track.py es el único camino para cambiar la pista de ceremonia de un proyecto.
Patrón dispose.py: identidad humana desde git config, legalidad, escritura
atómica del manifiesto. El escalado NO mueve ningún archivo (conservación
emergente, data-model § 6). Los tests construyen repos git reales en tmp (como
test_authorship.py / test_dispose.py) y validan el contrato de
contracts/track-cli.md § 1.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

FIXTURE_CORTA = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "006-corta"
SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "writeonmars" / "contracts" / "manifest-schema.json"
)


# --------------------------------------------------------------------------- #
# Utilidades: repos git reales en tmp con identidad humana o de agente.
# --------------------------------------------------------------------------- #
def git(project: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(project), *args], check=True, capture_output=True)


def make_repo(fixture: str, tmp_path: Path, *, email: str = "marcela@example.com",
              name: str = "Marcela", commit: bool = True) -> Path:
    """Copia un fixture 006-corta en un repo git con identidad configurada."""
    project = tmp_path / fixture
    shutil.copytree(FIXTURE_CORTA / fixture, project)
    git(project, "init")
    if name:
        git(project, "config", "user.name", name)
    git(project, "config", "user.email", email)
    if commit:
        git(project, "config", "commit.gpgsign", "false")
        git(project, "add", "-A")
        subprocess.run(
            ["git", "-C", str(project), "commit", "-m", "fixture"],
            check=True, capture_output=True,
        )
    return project


def run_track(scripts_dir: Path, project: Path, *args: str, env: dict | None = None):
    import os
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        [sys.executable, str(scripts_dir / "track.py"), *args, "--project-dir", str(project)],
        capture_output=True, text=True, env=merged,
    )


def set_track(project: Path, value: str) -> None:
    p = project / ".writeonmars-manifest.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["track"] = value
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_track_module(scripts_dir: Path):
    """Carga track.py como módulo para tests que monkeypatchean os.replace
    (imposible vía subprocess). No toca conftest.py."""
    path = scripts_dir / "track.py"
    spec = importlib.util.spec_from_file_location("wom_track", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wom_track"] = mod
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- #
# Escalado legal (corta → estandar): registro + schema + conservación.
# --------------------------------------------------------------------------- #
def test_escalar_registra_from_to_date_actor(scripts_dir, tmp_path):
    project = make_repo("produccion", tmp_path)
    res = run_track(scripts_dir, project, "--escalar", "--json")
    assert res.returncode == 0, res.stderr
    record = json.loads(res.stdout)
    assert record["from"] == "corta"
    assert record["to"] == "estandar"
    assert record["actor"] == "Marcela"
    assert record["email"] == "marcela@example.com"
    assert record["date"].endswith("Z")
    # ISO-8601 UTC sin microsegundos.
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", record["date"])

    data = json.loads((project / ".writeonmars-manifest.json").read_text(encoding="utf-8"))
    assert data["track"] == "estandar"
    assert data["track_history"][-1] == record


def test_escalar_produce_manifiesto_valido_contra_schema(scripts_dir, tmp_path):
    jsonschema = pytest.importorskip("jsonschema")
    project = make_repo("produccion", tmp_path)
    assert run_track(scripts_dir, project, "--escalar").returncode == 0
    manifest = json.loads((project / ".writeonmars-manifest.json").read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(manifest, schema)  # no lanza ⇒ válido v1.4.0


def test_escalar_solo_toca_el_manifiesto(scripts_dir, tmp_path):
    """Checkpoint US3: el escalado no mueve ningún archivo (SC-004). git status
    tras escalar muestra EXACTAMENTE el manifiesto modificado."""
    project = make_repo("produccion", tmp_path)
    assert run_track(scripts_dir, project, "--escalar").returncode == 0
    porcelain = subprocess.run(
        ["git", "-C", str(project), "status", "--porcelain"],
        capture_output=True, text=True, check=True,
    ).stdout
    # Formato porcelain: 'XY <path>'; el path empieza en la columna 3.
    changed = [line[3:] for line in porcelain.splitlines() if line.strip()]
    assert changed == [".writeonmars-manifest.json"]


def test_escalar_conserva_el_trabajo(scripts_dir, tmp_path):
    """SC-004: tras escalar y ampliar el temario a 4 filas, el capítulo 1
    conserva `approved` y la brújula pide 2, 3 y 4 sin migrar nada."""
    project = make_repo("produccion", tmp_path)
    assert run_track(scripts_dir, project, "--escalar").returncode == 0
    plan = project / "specs" / "001-mi-pieza" / "plan.md"
    plan.write_text(
        plan.read_text(encoding="utf-8")
        + "| 2 | Dos | Segunda promesa | didactica_v1 |\n"
        + "| 3 | Tres | Tercera promesa | didactica_v1 |\n"
        + "| 4 | Cuatro | Cuarta promesa | didactica_v1 |\n",
        encoding="utf-8",
    )
    res = subprocess.run(
        [sys.executable, str(scripts_dir / "status.py"), "--project-dir", str(project), "--json"],
        capture_output=True, text=True,
    )
    assert res.returncode == 0, res.stderr
    state = json.loads(res.stdout)
    assert state["by_chapter"]["1"]["approved"] is True
    assert state["pending_chapters"] == [2, 3, 4]


def test_escalar_dos_veces_rechaza(scripts_dir, tmp_path):
    project = make_repo("produccion", tmp_path)
    assert run_track(scripts_dir, project, "--escalar").returncode == 0
    again = run_track(scripts_dir, project, "--escalar")
    assert again.returncode == 1
    assert "ya está en pista estandar" in again.stderr


# --------------------------------------------------------------------------- #
# Des-escalado (estandar → corta): legal (legado) e ilegal (temario/capítulos).
# --------------------------------------------------------------------------- #
def test_desescalar_legado_sin_campo_track(scripts_dir, tmp_path):
    """Edge case 'proyecto legado que quiere volverse corta': el manifiesto no
    trae `track`; project_track lo resuelve a 'estandar' antes de escribir, así
    que el historial registra from='estandar'."""
    project = make_repo("legado", tmp_path)
    assert "track" not in json.loads(
        (project / ".writeonmars-manifest.json").read_text(encoding="utf-8")
    )
    res = run_track(scripts_dir, project, "--desescalar", "--json")
    assert res.returncode == 0, res.stderr
    record = json.loads(res.stdout)
    assert record["from"] == "estandar"
    assert record["to"] == "corta"
    data = json.loads((project / ".writeonmars-manifest.json").read_text(encoding="utf-8"))
    assert data["track"] == "corta"
    assert data["track_history"][0]["from"] == "estandar"


def test_desescalar_temario_multifila_rechaza(scripts_dir, tmp_path):
    project = make_repo("produccion", tmp_path)
    set_track(project, "estandar")
    plan = project / "specs" / "001-mi-pieza" / "plan.md"
    plan.write_text(
        plan.read_text(encoding="utf-8")
        + "| 2 | Dos | p | didactica_v1 |\n"
        + "| 3 | Tres | p | didactica_v1 |\n"
        + "| 4 | Cuatro | p | didactica_v1 |\n",
        encoding="utf-8",
    )
    res = run_track(scripts_dir, project, "--desescalar")
    assert res.returncode == 1
    assert "el temario tiene 4 filas; la pista corta exige pieza única" in res.stderr


def test_desescalar_con_capitulos_fuera_rechaza(scripts_dir, tmp_path):
    """Temario de una fila pero chapters/02 en disco: enumera los ordinales."""
    project = make_repo("produccion", tmp_path)
    set_track(project, "estandar")
    (project / "chapters" / "02-segunda.md").write_text("# Dos\n", encoding="utf-8")
    (project / "chapters" / "03-tercera.md").write_text("# Tres\n", encoding="utf-8")
    res = run_track(scripts_dir, project, "--desescalar")
    assert res.returncode == 1
    assert "existen capítulos fuera de pieza única: 2, 3" in res.stderr


# --------------------------------------------------------------------------- #
# Identidad humana (exit 3): agente y ausencia de user.name.
# --------------------------------------------------------------------------- #
def test_identidad_de_agente_rechaza(scripts_dir, tmp_path):
    project = make_repo("produccion", tmp_path, email="redactora@agents.writeonmars.invalid")
    res = run_track(scripts_dir, project, "--escalar")
    assert res.returncode == 3
    assert "pertenece a un agente" in res.stderr


def test_sin_user_name_rechaza(scripts_dir, tmp_path):
    """Sin user.name (ni local ni global) no hay identidad humana auditable."""
    project = tmp_path / "sin-nombre"
    shutil.copytree(FIXTURE_CORTA / "produccion", project)
    git(project, "init")
    # Aislar de la config global del entorno: sin user.name en ningún nivel.
    empty_home = tmp_path / "empty-home"
    empty_home.mkdir()
    env = {
        "HOME": str(empty_home),
        "GIT_CONFIG_GLOBAL": str(empty_home / ".gitconfig"),
        "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
    }
    res = run_track(scripts_dir, project, "--escalar", env=env)
    assert res.returncode == 3
    assert "user.name" in res.stderr


# --------------------------------------------------------------------------- #
# --check: read-only, no exige identidad; detecta incoherencia.
# --------------------------------------------------------------------------- #
def test_check_incoherente_falla(scripts_dir, tmp_path):
    """incoherente: track corta con temario de 3 filas ⇒ invariante roto."""
    project = make_repo("incoherente", tmp_path)
    res = run_track(scripts_dir, project, "--check")
    assert res.returncode == 1
    assert "track: corta con temario de 3 filas" in res.stderr


def test_check_no_exige_identidad_humana(scripts_dir, tmp_path):
    """--check es read-only: coherente aun con identidad de agente (exit 0)."""
    project = make_repo("produccion", tmp_path, email="redactora@agents.writeonmars.invalid")
    res = run_track(scripts_dir, project, "--check", "--json")
    assert res.returncode == 0, res.stderr
    diag = json.loads(res.stdout)
    assert diag == {"track": "corta", "temario_filas": 1, "capitulos_fuera": [], "coherente": True}


def test_check_estandar_sin_invariante(scripts_dir, tmp_path):
    project = make_repo("produccion", tmp_path)
    set_track(project, "estandar")
    res = run_track(scripts_dir, project, "--check")
    assert res.returncode == 0, res.stderr
    assert "sin invariante de pieza única" in res.stdout


# --------------------------------------------------------------------------- #
# Errores de uso y de estado.
# --------------------------------------------------------------------------- #
def test_grupo_obligatorio_es_uso_incorrecto(scripts_dir, tmp_path):
    project = make_repo("produccion", tmp_path)
    res = run_track(scripts_dir, project)  # sin --escalar/--desescalar/--check
    assert res.returncode == 2


def test_manifiesto_ausente_es_error_de_estado(scripts_dir, tmp_path):
    project = tmp_path / "vacio"
    project.mkdir()
    git(project, "init")
    git(project, "config", "user.name", "Marcela")
    git(project, "config", "user.email", "marcela@example.com")
    res = run_track(scripts_dir, project, "--escalar")
    assert res.returncode == 1
    assert "falta" in res.stderr and ".writeonmars-manifest.json" in res.stderr


# --------------------------------------------------------------------------- #
# Atomicidad: fallo en os.replace no corrompe el manifiesto ni deja .tmp.
# --------------------------------------------------------------------------- #
def test_atomicidad_sin_tmp_huerfano(scripts_dir, tmp_path, monkeypatch):
    track_mod = load_track_module(scripts_dir)
    project = make_repo("produccion", tmp_path)
    manifest = project / ".writeonmars-manifest.json"
    original = manifest.read_bytes()

    def boom(src, dst):
        raise OSError("fallo simulado en os.replace")

    monkeypatch.setattr(track_mod.os, "replace", boom)
    monkeypatch.setattr(sys, "argv", ["track.py", "--escalar", "--project-dir", str(project)])
    with pytest.raises(OSError):
        track_mod.main()

    assert manifest.read_bytes() == original  # bytes originales intactos
    assert not (project / ".{}.tmp".format(manifest.name)).exists()
    tmps = list(project.glob(".*.tmp"))
    assert tmps == []  # sin .tmp huérfano
