"""Tests del contrato de status.py para mode=estudio."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


def evaluate(status_mod, proj: Path) -> dict:
    return status_mod.evaluate(proj, status_mod.newest_spec_dir(proj, None))


def test_estudio_sin_capitulos_pide_write(status_mod, estudio_project):
    shutil.rmtree(estudio_project / "chapters")
    (estudio_project / "specs" / "001-estudio" / "findings.md").unlink()
    state = evaluate(status_mod, estudio_project)
    assert state["mode"] == "estudio"
    assert state["next_step"] == "write"
    assert state["pending_chapters"] == [1, 2, 3]
    assert "Redactora" not in state["next_detail"]


def test_estudio_con_capitulo_sin_findings_pide_review(status_mod, estudio_project):
    (estudio_project / "specs" / "001-estudio" / "findings.md").unlink()
    state = evaluate(status_mod, estudio_project)
    assert state["next_step"] == "review"
    assert state["pending_chapters"] == [2, 3]


def test_estudio_con_hallazgos_accionables_pide_dispose(status_mod, estudio_project):
    state = evaluate(status_mod, estudio_project)
    assert state["next_step"] == "dispose"
    assert state["pending_dispositions"] == ["F-1.1", "F-1.2"]
    assert state["deferred_findings"] == []


def test_huella_obsoleta_reabre_capitulo(status_mod, estudio_project):
    chapter = estudio_project / "chapters" / "001-uno-humano.md"
    chapter.write_text(chapter.read_text(encoding="utf-8") + "\nCambio humano.\n", encoding="utf-8")
    # Cerramos los accionables para que la razón visible del next_step sea la huella.
    findings = estudio_project / "specs" / "001-estudio" / "findings.md"
    text = findings.read_text(encoding="utf-8")
    text = text.replace("| F-1.1 | 1 | critico | frase | problema crítico | sugerencia | abierto | [] |",
                        "| F-1.1 | 1 | critico | frase | problema crítico | sugerencia | aplazado | [] |")
    text = text.replace("| F-1.2 | 1 | medio | frase | problema medio | sugerencia | abierto | [] |",
                        "| F-1.2 | 1 | medio | frase | problema medio | sugerencia | aplazado | [] |")
    findings.write_text(text, encoding="utf-8")
    disposiciones = estudio_project / "specs" / "001-estudio" / "disposiciones.jsonl"
    disposiciones.write_text(
        "\n".join([
            '{"v":1,"ts":"2026-07-08T00:00:00Z","finding_id":"F-1.1","disposicion":"aplazado","actor":"Marcela"}',
            '{"v":1,"ts":"2026-07-08T00:00:01Z","finding_id":"F-1.2","disposicion":"aplazado","actor":"Marcela"}',
        ]) + "\n",
        encoding="utf-8",
    )
    state = evaluate(status_mod, estudio_project)
    assert state["next_step"] == "review"
    assert state["reopened_chapters"] == ["1"]
    assert state["by_chapter"]["1"]["passes_done"] == []


def test_estado_no_abierto_sin_disposicion_no_avanza(status_mod, estudio_project):
    findings = estudio_project / "specs" / "001-estudio" / "findings.md"
    findings.write_text(
        findings.read_text(encoding="utf-8").replace(
            "| F-1.1 | 1 | critico | frase | problema crítico | sugerencia | abierto | [] |",
            "| F-1.1 | 1 | critico | frase | problema crítico | sugerencia | resuelto | [] |",
        ),
        encoding="utf-8",
    )
    state = evaluate(status_mod, estudio_project)
    assert state["next_step"] == "dispose"
    assert "F-1.1" in state["pending_dispositions"]
    assert any("DispositionRecord" in warning for warning in state["warnings"])


def test_oraculo_json_estudio(status_mod, repo_root, estudio_project):
    state = evaluate(status_mod, estudio_project)
    oracle = json.loads((repo_root / "tests/fixtures/005-estudio/expected-status.json").read_text(encoding="utf-8"))
    assert json.loads(json.dumps(state, ensure_ascii=False, sort_keys=True)) == oracle


def _to_produccion(project: Path) -> None:
    manifest = project / ".writeonmars-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["mode"] = "produccion"
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def test_produccion_capitulo_sin_ordinal_cuenta_como_escrito(status_mod, estudio_project):
    """Regresión FR-011: en produccion la cuenta de pendientes es ficheros vs
    temario (histórica); un capítulo sin prefijo numérico no reabre implement."""
    _to_produccion(estudio_project)
    chapters = estudio_project / "chapters"
    (chapters / "intro.md").write_text("# Intro\n", encoding="utf-8")
    (chapters / "099-extra.md").write_text("# Extra\n", encoding="utf-8")
    # 3 ficheros para un temario de 3: pendientes=0 aunque los ordinales 2 y 3 falten.
    state = evaluate(status_mod, estudio_project)
    assert state["mode"] == "produccion"
    assert state["next_step"] != "implement"
    assert state["pending_chapters"] == [2, 3]  # aditivo: informa, no gobierna


def test_produccion_ignora_disposiciones_corruptas(status_mod, estudio_project):
    """Regresión FR-011: en produccion disposiciones.jsonl ni se lee."""
    _to_produccion(estudio_project)
    (estudio_project / "specs/001-estudio/disposiciones.jsonl").write_text(
        "{esto no es json\n", encoding="utf-8"
    )
    state = evaluate(status_mod, estudio_project)  # no crashea
    assert state["mode"] == "produccion"


def test_estudio_disposiciones_corruptas_fallan_con_linea(status_mod, estudio_project):
    import pytest
    (estudio_project / "specs/001-estudio/disposiciones.jsonl").write_text(
        "{esto no es json\n", encoding="utf-8"
    )
    with pytest.raises(SystemExit):
        evaluate(status_mod, estudio_project)


def test_estudio_dispose_va_antes_que_reopened(status_mod, estudio_project):
    """Capítulo reabierto por huella CON hallazgos accionables abiertos: primero
    dispone la humana (review sería un callejón sin salida para el ejecutor)."""
    chapter = estudio_project / "chapters" / "001-uno-humano.md"
    chapter.write_text(chapter.read_text(encoding="utf-8") + "\nEdición.\n", encoding="utf-8")
    state = evaluate(status_mod, estudio_project)
    assert state["reopened_chapters"] == ["1"]
    assert state["next_step"] == "dispose"


def test_huella_ausente_no_cuenta_en_estudio(status_mod, estudio_project):
    """No evaluado ≠ verde: un bloque sin comentario de huellas no ancla nada."""
    import re
    findings = estudio_project / "specs/001-estudio/findings.md"
    text = re.sub(r"<!--\s*huellas:.*?-->\n?", "", findings.read_text(encoding="utf-8"))
    findings.write_text(text, encoding="utf-8")
    state = evaluate(status_mod, estudio_project)
    assert 1 not in state["by_chapter"]["1"]["passes_done"]
    assert "1" in state["reopened_chapters"]


def test_estudio_closeable_se_ancla_a_la_huella(status_mod, estudio_project, tmp_path):
    """G4 de la revisión: editar un capítulo aprobado deja el proyecto no-cerrable
    en estudio aunque g1-g3 sigan en verde (close.py solo consulta closeable)."""
    import hashlib
    spec = estudio_project / "specs/001-estudio"
    # Temario de 1 capítulo para poder aprobarlo todo.
    plan = spec / "plan.md"
    text = plan.read_text(encoding="utf-8")
    lines = [l for l in text.splitlines() if not re.match(r"\|\s*[23]\s*\|", l)]
    plan.write_text("\n".join(lines) + "\n", encoding="utf-8")
    chapter = estudio_project / "chapters" / "001-uno-humano.md"
    sha = hashlib.sha256(chapter.read_bytes()).hexdigest()
    blocks = []
    for num, name in [(1, "Estructura"), (2, "Utilidad"), (3, "Naturalidad"), (4, "Precisión")]:
        blocks.append(
            f"## Pasada {num} - {name}\n\n<!-- pass-output-schema: v1.2 -->\n\n"
            f"**Estado pasada**: passed\n**Capítulos cubiertos**: [1]\n**Firma**:\n"
            f"  - tipo: autonomous\n  - actor: mesa\n\n### Hallazgos\n\n"
            f"| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |\n"
            f"|----|----------|-----------|-------|----------|-------------|--------|-------|\n"
            f'\n<!-- huellas: {{"1": "{sha}"}} -->\n'
        )
    (spec / "findings.md").write_text("# Findings\n\n" + "\n".join(blocks), encoding="utf-8")
    (spec / "disposiciones.jsonl").unlink(missing_ok=True)
    state = evaluate(status_mod, estudio_project)
    assert state["all_chapters_approved"] is True
    assert state["closeable"] is True
    # La humana edita el capítulo tras las pasadas: el cierre se desancla.
    chapter.write_text(chapter.read_text(encoding="utf-8") + "\nCoda.\n", encoding="utf-8")
    state = evaluate(status_mod, estudio_project)
    assert state["all_chapters_approved"] is False
    assert state["closeable"] is False


import re  # noqa: E402
