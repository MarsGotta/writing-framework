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
