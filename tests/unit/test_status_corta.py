"""Tests del contrato de status.py para track=corta (feature 006).

La pista corta no toca la brújula (R1, R5, contrato §3.3): status.py solo gana la
clave aditiva `track` y hasta dos avisos advisory. Aquí se fija ese contrato
mínimo: la brújula nunca pide `plan` ni `constitution` en corta, los avisos no
alteran el estado, y un track desconocido falla como lo hace `mode`.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

FIXTURE_CORTA = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "006-corta"


def evaluate(status_mod, proj: Path) -> dict:
    return status_mod.evaluate(proj, status_mod.newest_spec_dir(proj, None))


def _set_track(proj: Path, value: str) -> None:
    man = proj / ".writeonmars-manifest.json"
    data = json.loads(man.read_text(encoding="utf-8"))
    data["track"] = value
    man.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@pytest.fixture
def corta_produccion(tmp_path: Path) -> Path:
    """Copia mutable del fixture corta en produccion (spec + research + temario de
    una fila + 5 pasadas + capítulo). Los tests podan ficheros para recorrer los
    estados intermedios del ciclo corto."""
    dst = tmp_path / "produccion"
    shutil.copytree(FIXTURE_CORTA / "produccion", dst)
    return dst


# ---------------------------------------------------------------------------
# US1 / AS-1: la brújula nunca pide `plan` ni `constitution` en pista corta
# ---------------------------------------------------------------------------
def test_brujula_nunca_pide_plan_ni_constitution(status_mod, corta_produccion):
    """Recorre los estados intermedios (con pasadas → con capítulo → con research
    → sin research) y comprueba que `next_step` jamás vale `plan` ni `constitution`
    y que `chapters_expected` sigue en 1 (temario degenerado)."""
    proj = corta_produccion
    spec = proj / "specs" / "001-mi-pieza"
    forbidden = {"plan", "constitution"}

    # con pasadas (estado completo del fixture): sin críticos, cerrable (R11: close).
    state = evaluate(status_mod, proj)
    assert state["track"] == "corta"
    assert state["chapters_expected"] == 1
    assert state["next_step"] == "close"
    assert state["next_step"] not in forbidden

    # con capítulo, sin findings.md → review (no plan/constitution).
    (spec / "findings.md").unlink()
    state = evaluate(status_mod, proj)
    assert state["chapters_expected"] == 1
    assert state["next_step"] == "review"
    assert state["next_step"] not in forbidden

    # con research, sin capítulo → implement (temario de 1 fila sin escribir).
    shutil.rmtree(proj / "chapters")
    state = evaluate(status_mod, proj)
    assert state["chapters_expected"] == 1
    assert state["next_step"] == "implement"
    assert state["next_step"] not in forbidden

    # sin research → research (nunca plan pese a temario materializado).
    (spec / "research.md").unlink()
    state = evaluate(status_mod, proj)
    assert state["chapters_expected"] == 1
    assert state["next_step"] == "research"
    assert state["next_step"] not in forbidden


# ---------------------------------------------------------------------------
# R5 / Edge cases: las incoherencias de pista se reportan como warnings, no estado
# ---------------------------------------------------------------------------
def test_incoherente_emite_dos_warnings_sin_alterar_la_brujula(status_mod, tmp_path):
    """Fixture `incoherente/` (corta con temario de 3 filas y un capítulo 2 en
    disco): emite las DOS entradas advisory de pista, pero `next_step`, `gates`,
    `closeable` y `by_chapter` son IDÉNTICOS a los del mismo proyecto declarado
    `estandar`. Los avisos informan; no bloquean ni mueven la máquina de estados."""
    src = FIXTURE_CORTA / "incoherente"
    corta = evaluate(status_mod, src)  # evaluate es read-only: no muta el fixture

    dst = tmp_path / "estandar"
    shutil.copytree(src, dst)
    _set_track(dst, "estandar")
    estandar = evaluate(status_mod, dst)

    # Las dos entradas advisory, solo en corta.
    ws = corta["warnings"]
    assert any("el temario tiene 3 filas" in w for w in ws), ws
    assert any("fuera de pieza única (2)" in w for w in ws), ws
    assert not any("track: corta" in w for w in estandar["warnings"])

    # Estado idéntico entre corta y estandar (R5: warnings ≠ brújula).
    assert corta["next_step"] == estandar["next_step"]
    assert corta["gates"] == estandar["gates"]
    assert corta["closeable"] == estandar["closeable"]
    assert corta["by_chapter"] == estandar["by_chapter"]
    assert corta["all_chapters_approved"] == estandar["all_chapters_approved"]


# ---------------------------------------------------------------------------
# AS-5: un track desconocido falla claro (espejo de mode)
# ---------------------------------------------------------------------------
def test_track_desconocido_falla_con_exit_2(status_mod, tmp_path, capsys):
    dst = tmp_path / "rapida"
    shutil.copytree(FIXTURE_CORTA / "produccion", dst)
    _set_track(dst, "rapida")
    with pytest.raises(SystemExit) as exc:
        evaluate(status_mod, dst)
    assert exc.value.code == 2
    assert "track" in capsys.readouterr().err


# ===========================================================================
# T016 · US2 — Cinco dimensiones, dos relevos (P2)
#
# La pasada combinada (bloques 1·2·3·5) más la precisión (bloque 4) llevan el
# capítulo único a `approved` y el proyecto a `closeable` **con el parser
# actual**: status.py solo ganó la clave `track` (T007) y ni una línea más de
# lógica de estado. Es SC-002 (cero garantías perdidas) + SC-003 (la brújula no
# cambió de opinión). Si alguna de estas aserciones exigiera tocar `_next_step`,
# `_build_by_chapter`, `gates` o `closeable`, algo se habría entendido mal.
# ===========================================================================

# Separador canónico de la tabla de hallazgos, idéntico en los cinco fixtures de
# 006-corta: tras él se inyecta la fila de hallazgo abierto del apartado (c).
_TABLA_SEP = "|----|----------|-----------|-------|----------|-------------|--------|-------|"


def _copy_fixture(tmp_path: Path, name: str) -> Path:
    """Copia mutable de un fixture de 006-corta a tmp_path (patrón habitual en
    tests/unit/): los fixtures produccion/ y estudio/ llegan limpios."""
    dst = tmp_path / name
    shutil.copytree(FIXTURE_CORTA / name, dst)
    return dst


def _add_open_finding(findings_md: Path, sev: str = "medio", cap: str = "1", fid: str = "F-1.1") -> None:
    """Inyecta una fila de hallazgo ABIERTO en el primer bloque de pasada de
    findings.md. El apartado (c) exige construir el caso accionable copiando el
    fixture y añadiendo la fila (los fixtures limpios no la traen): la fila cuelga
    del capítulo `cap`, con lo que `revise_by_chapter[cap]` deja de estar vacío."""
    row = (
        f"| {fid} | {cap} | {sev} | frase con problema | problema {sev} "
        f"| reescritura propuesta | abierto | [] |"
    )
    text = findings_md.read_text(encoding="utf-8")
    assert _TABLA_SEP in text, "el fixture no trae el separador de tabla esperado"
    idx = text.index(_TABLA_SEP) + len(_TABLA_SEP)
    findings_md.write_text(text[:idx] + "\n" + row + text[idx:], encoding="utf-8")


# ---------------------------------------------------------------------------
# T016 (a) · SC-002 + SC-003: la combinada + la precisión aprueban y cierran
# ---------------------------------------------------------------------------
def test_combinada_lleva_a_approved_y_closeable(status_mod):
    """Fixture `produccion` completo (combinada 1·2·3·5 + precisión 4 + claims):
    las cinco dimensiones constan, el capítulo único queda `approved` y el
    proyecto `closeable` con el parser ACTUAL —status.py sin cambios más allá de
    la clave `track` de T007—. evaluate es read-only: no se copia el fixture."""
    proj = FIXTURE_CORTA / "produccion"
    state = evaluate(status_mod, proj)

    assert state["track"] == "corta"
    assert sorted(p["num"] for p in state["passes"]) == [1, 2, 3, 4, 5]
    # La pasada 5 es formato global y no gobierna el approved por capítulo (1-4).
    assert state["by_chapter"]["1"]["passes_done"] == [1, 2, 3, 4]
    assert state["by_chapter"]["1"]["approved"] is True
    assert state["all_chapters_approved"] is True
    assert state["closeable"] is True
    assert (proj / "specs" / "001-mi-pieza" / "claims.md").exists()


# ---------------------------------------------------------------------------
# T016 (b) · degradación grácil: la combinada a medias no aprueba
# ---------------------------------------------------------------------------
def test_combinada_a_medias_no_aprueba(status_mod):
    """Fixture `medias/` (la combinada solo registró los bloques 1 y 2): el
    capítulo NO llega a `approved` y no todas las pasadas constan.

    **NO se comprueba `next_step`** (research R11): en produccion ya vale `close`
    en cuanto hay un bloque sin críticos, porque `closeable` no exige
    `all_chapters_approved`; el despacho de la pasada ausente llega por la rama de
    normalización del ejecutor, no por la rama `review` de la brújula."""
    state = evaluate(status_mod, FIXTURE_CORTA / "medias")
    assert state["all_chapters_approved"] is False
    assert state["by_chapter"]["1"]["passes_done"] == [1, 2]
    assert state["by_chapter"]["1"]["approved"] is False


# ---------------------------------------------------------------------------
# T016 (c) · hallazgo accionable abierto: revise (produccion) / dispose (estudio)
# ---------------------------------------------------------------------------
def test_hallazgo_abierto_pide_revise_en_produccion(status_mod, corta_produccion):
    """Con un hallazgo `medio` ABIERTO, produccion pide `revise`. Aquí SÍ se
    comprueba `next_step`: `revise_pending > 0` precede a `closeable` en
    `_next_step`. El fixture entra limpio; el caso accionable se construye en
    tmp_path añadiendo la fila (no lo trae el fixture)."""
    _add_open_finding(corta_produccion / "specs" / "001-mi-pieza" / "findings.md", sev="medio")
    state = evaluate(status_mod, corta_produccion)

    assert state["mode"] == "produccion"
    assert state["revise_pending"] == 1
    assert state["by_chapter"]["1"]["revise_pending"] == 1
    assert state["next_step"] == "revise"


def test_hallazgo_abierto_pide_dispose_en_estudio(status_mod, tmp_path):
    """El mismo hallazgo `medio` ABIERTO en corta+estudio: la disposición es
    humana (checkpoint exit 10), así que `next_step` vale `dispose`, no `revise`
    (matriz track × mode, FR-009). El fixture `estudio/` llega limpio; la fila se
    añade sobre la copia en tmp_path."""
    proj = _copy_fixture(tmp_path, "estudio")
    _add_open_finding(proj / "specs" / "001-mi-pieza" / "findings.md", sev="medio")
    state = evaluate(status_mod, proj)

    assert state["track"] == "corta"
    assert state["mode"] == "estudio"
    assert state["revise_pending"] == 1
    assert state["pending_dispositions"] == ["F-1.1"]
    assert state["next_step"] == "dispose"


# ---------------------------------------------------------------------------
# T016 (d) · matriz corta+estudio: las huellas de la 005 invalidan pasadas
# ---------------------------------------------------------------------------
def test_huella_invalida_pasadas_en_corta_estudio(status_mod, tmp_path):
    """corta + estudio: editar el capítulo tras las pasadas rompe su huella
    sha256 (la de la 005) y reabre el capítulo — `passes_done` se vacía, y
    `approved`/`closeable` caen. La misma edición en corta + produccion NO
    invalida nada (las huellas solo gobiernan en estudio, FR-011): control de la
    matriz track × mode."""
    # corta + estudio, limpio: aprobado y cerrable, sin capítulos reabiertos.
    est = _copy_fixture(tmp_path, "estudio")
    antes = evaluate(status_mod, est)
    assert antes["by_chapter"]["1"]["passes_done"] == [1, 2, 3, 4]
    assert antes["by_chapter"]["1"]["approved"] is True
    assert antes["closeable"] is True
    assert antes["reopened_chapters"] == []

    # La humana edita el capítulo aprobado: la huella deja de coincidir.
    cap = est / "chapters" / "01-la-pieza.md"
    cap.write_text(cap.read_text(encoding="utf-8") + "\nEdición humana posterior.\n", encoding="utf-8")
    despues = evaluate(status_mod, est)
    assert despues["by_chapter"]["1"]["passes_done"] == []
    assert despues["by_chapter"]["1"]["approved"] is False
    assert despues["all_chapters_approved"] is False
    assert despues["closeable"] is False
    assert despues["reopened_chapters"] == ["1"]
    assert any("huella no coincide" in w for w in despues["warnings"]), despues["warnings"]

    # Control corta + produccion: la misma edición no toca ni las pasadas ni el cierre.
    prod = _copy_fixture(tmp_path, "produccion")
    cap_p = prod / "chapters" / "01-la-pieza.md"
    cap_p.write_text(cap_p.read_text(encoding="utf-8") + "\nEdición humana posterior.\n", encoding="utf-8")
    control = evaluate(status_mod, prod)
    assert control["by_chapter"]["1"]["passes_done"] == [1, 2, 3, 4]
    assert control["by_chapter"]["1"]["approved"] is True
    assert control["closeable"] is True
    assert control["reopened_chapters"] == []
