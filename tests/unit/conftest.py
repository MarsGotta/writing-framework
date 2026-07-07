"""Fixtures compartidas para la suite unitaria de writeonmars/scripts.

Los scripts del preset no forman un paquete: se cargan por ruta con importlib,
sin tocar sys.path ni mover ficheros. Cada módulo se registra con un alias
(wom_status, wom_export, ...) para no chocar con nada del entorno.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from itertools import count
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "writeonmars" / "scripts"
FIXTURES_003 = REPO_ROOT / "tests" / "fixtures" / "003-factualidad"

# Separador canónico de los encabezados de pasada en findings.md reales (la raya,
# escapada a propósito). El parser también acepta "-", que es lo que usan los
# builders de abajo.
SEP_RAYA = "\u2014"

PASS_NAMES = {
    1: "Estructura",
    2: "Utilidad",
    3: "Naturalidad",
    4: "Precisión",
    5: "Formato",
}

_seq = count()


def _load_script(name: str, alias: str):
    """Carga writeonmars/scripts/<name>.py como módulo con un alias propio."""
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(alias, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Módulos bajo test (scope session: se cargan una sola vez)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def status_mod():
    return _load_script("status", "wom_status")


@pytest.fixture(scope="session")
def export_mod():
    return _load_script("export", "wom_export")


@pytest.fixture(scope="session")
def index_mod():
    return _load_script("index", "wom_index")


@pytest.fixture(scope="session")
def bootstrap_mod():
    return _load_script("bootstrap", "wom_bootstrap")


@pytest.fixture(scope="session")
def close_mod():
    return _load_script("close", "wom_close")


@pytest.fixture(scope="session")
def scripts_dir() -> Path:
    return SCRIPTS_DIR


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


# ---------------------------------------------------------------------------
# Builders de findings.md (esquema pass-output v1.1)
# ---------------------------------------------------------------------------
def make_finding_row(
    fid: str = "F-1.1",
    cap: str = "1",
    sev: str = "critico",
    estado: str = "abierto",
) -> str:
    """Fila de la tabla de hallazgos (8 celdas, contrato pass-output-schema)."""
    return (
        f"| {fid} | {cap} | {sev} | frase con problema | problema descrito "
        f"| reescritura propuesta | {estado} | [src-1] |"
    )


def make_pass_block(
    num: int,
    nombre: str | None = None,
    caps: str = "[1, 2]",
    estado: str = "passed",
    tipo: str = "autonomous",
    actor: str = "bot",
    filas: tuple[str, ...] | list[str] = (),
    sep: str = "-",
) -> str:
    """Bloque de pasada de findings.md tal como lo emiten las pasadas."""
    nombre = nombre or PASS_NAMES.get(num, f"Pasada {num}")
    filas_txt = ("\n".join(filas) + "\n") if filas else ""
    return (
        f"## Pasada {num} {sep} {nombre}\n\n"
        "<!-- pass-output-schema: v1.1 -->\n\n"
        f"**Estado pasada**: {estado}\n"
        f"**Capítulos cubiertos**: {caps}\n"
        "**Firma**:\n"
        f"  - tipo: {tipo}\n"
        f"  - actor: {actor}\n\n"
        "### Hallazgos\n\n"
        "| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |\n"
        "|----|----------|-----------|-------|----------|-------------|--------|-------|\n"
        f"{filas_txt}"
    )


def green_findings(caps: str = "[1, 2]") -> str:
    """findings.md en verde: pasadas 1 a 4 sobre los capítulos y la 5 global."""
    blocks = [make_pass_block(n, caps=caps) for n in (1, 2, 3, 4)]
    blocks.append(make_pass_block(5, caps="global"))
    return "# findings\n\n" + "\n".join(blocks)


@pytest.fixture
def pass_block():
    """Expone el builder de bloques de pasada a los tests."""
    return make_pass_block


@pytest.fixture
def finding_row():
    """Expone el builder de filas de hallazgo a los tests."""
    return make_finding_row


# ---------------------------------------------------------------------------
# Proyectos editoriales de prueba
# ---------------------------------------------------------------------------
MINI_MANIFEST = {
    "framework_version": "0.1.0",
    "constitution_version": "1.5.0",
    "agent_target": "claude-code",
    "language_primary": "es",
    "skills": [{"name": "x", "version": "1.0.0", "source": "bundled"}],
    "research_mode": "byom",
    "signing_matrix": {
        "pasada_1_estructura": "autonomous",
        "pasada_2_utilidad": "autonomous",
        "pasada_3_naturalidad": "autonomous",
        "pasada_4_precision": "autonomous",
        "pasada_5_formato": "autonomous",
    },
    "human_operators": [{"id": "m", "role": "author"}],
    "citation_contract_version": "1.0",
    "project_type": "editorial",
    "sector": "tecnologia",
}

MINI_PLAN = """# Plan de la guía

## Temario

| # | Título | Promesa |
|---|--------|---------|
| 1 | Primeros pasos | Arranca sin miedo |
| 2 | Profundizando | Domina el flujo |

## Otra sección

| 9 | Fila fuera del temario | no debe contarse |
"""


@pytest.fixture
def mini_project(tmp_path: Path) -> Path:
    """Proyecto editorial mínimo y CERRABLE: manifest con sector, constitución,
    spec + research + temario de 2 capítulos, 2 capítulos escritos y findings
    en verde. Los tests mutan ficheros para provocar cada estado."""
    proj = tmp_path / "guia"
    (proj / "chapters").mkdir(parents=True)
    (proj / ".specify" / "memory").mkdir(parents=True)
    (proj / ".specify" / "memory" / "constitution.md").write_text(
        "# Constitución editorial (test)\n\n**Version**: 1.5.0\n", encoding="utf-8"
    )
    (proj / ".writeonmars-manifest.json").write_text(
        json.dumps(MINI_MANIFEST, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    spec = proj / "specs" / "001-guia"
    spec.mkdir(parents=True)
    (spec / "spec.md").write_text(
        "# Feature Specification: Guía de prueba\n\nBrief mínimo.\n", encoding="utf-8"
    )
    (spec / "research.md").write_text("# Research\n\nNotas de fuentes.\n", encoding="utf-8")
    (spec / "plan.md").write_text(MINI_PLAN, encoding="utf-8")
    (spec / "findings.md").write_text(green_findings(), encoding="utf-8")
    (proj / "chapters" / "01-primeros-pasos.md").write_text(
        "# Primeros pasos\n\nTexto del capítulo uno.\n\n## Fuentes\n- Fuente A\n",
        encoding="utf-8",
    )
    (proj / "chapters" / "02-profundizando.md").write_text(
        "# Profundizando\n\nTexto del capítulo dos.\n\n## Fuentes\n- Fuente B\n",
        encoding="utf-8",
    )
    return proj


@pytest.fixture
def mini_spec_dir(mini_project: Path) -> Path:
    return mini_project / "specs" / "001-guia"


@pytest.fixture
def claims_md_003() -> Path:
    """claims.md del fixture 003 (solo lectura): caps 1 y 2 medidos a 0.8,
    cap 3 sin sección."""
    return FIXTURES_003 / "project" / "specs" / "001-fact" / "claims.md"


@pytest.fixture
def fact_project(tmp_path: Path):
    """Factoría: copia del proyecto de fixtures 003 en tmp_path.

    manifest: None (baseline sin quality_gates) o 'blocking' | 'advisory' | 'pass'
    (variantes de tests/fixtures/003-factualidad/manifests/).
    sector: se inyecta en el manifest para que next_step avance más allá de
    'constitution' (el fixture original no lo trae).
    """

    def _make(manifest: str | None = None, sector: str | None = "tecnologia") -> Path:
        dst = tmp_path / f"proyecto-{manifest or 'base'}-{next(_seq)}"
        shutil.copytree(FIXTURES_003 / "project", dst)
        if manifest:
            shutil.copyfile(
                FIXTURES_003 / "manifests" / f"{manifest}.json",
                dst / ".writeonmars-manifest.json",
            )
        (dst / ".specify" / "memory").mkdir(parents=True)
        (dst / ".specify" / "memory" / "constitution.md").write_text(
            "# Constitución editorial (test)\n\n**Version**: 1.5.0\n", encoding="utf-8"
        )
        if sector:
            man_p = dst / ".writeonmars-manifest.json"
            data = json.loads(man_p.read_text(encoding="utf-8"))
            data["sector"] = sector
            man_p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return dst

    return _make
