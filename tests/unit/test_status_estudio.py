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
