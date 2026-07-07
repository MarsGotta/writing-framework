"""Tests unitarios de status.py: parsers, factualidad, gates g1-g4 y next_step.

status.py es la brújula del método: evaluate() es la única fuente de verdad del
dashboard y de la salida --json del orquestador. Aquí se fija su contrato.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import SEP_RAYA, green_findings, make_finding_row, make_pass_block


def write_findings(proj: Path, text: str) -> None:
    (proj / "specs" / "001-guia" / "findings.md").write_text(text, encoding="utf-8")


def evaluate(status_mod, proj: Path) -> dict:
    """Atajo: evalúa el proyecto con su spec más reciente."""
    spec_dir = status_mod.newest_spec_dir(proj, None)
    return status_mod.evaluate(proj, spec_dir)


# ---------------------------------------------------------------------------
# parse_findings y helpers de parseo
# ---------------------------------------------------------------------------
class TestParseFindings:
    def test_fichero_ausente_devuelve_lista_vacia(self, status_mod, tmp_path):
        assert status_mod.parse_findings(tmp_path / "no-existe.md") == []

    def test_bloque_basico(self, status_mod, tmp_path):
        f = tmp_path / "findings.md"
        f.write_text(make_pass_block(1, caps="[1]"), encoding="utf-8")
        blocks = status_mod.parse_findings(f)
        assert len(blocks) == 1
        b = blocks[0]
        assert b["num"] == 1
        assert b["name"] == "Estructura"
        assert b["estado"] == "passed"
        assert b["firma"] == "autonomous"
        assert b["actor"] == "bot"
        assert b["capitulos"] == "[1]"
        assert b["hallazgos"] == []

    def test_acepta_separador_canonico_raya(self, status_mod, tmp_path):
        """Los findings reales separan con raya (escapada aquí a propósito)."""
        f = tmp_path / "findings.md"
        f.write_text(make_pass_block(2, sep=SEP_RAYA), encoding="utf-8")
        blocks = status_mod.parse_findings(f)
        assert blocks and blocks[0]["num"] == 2
        assert blocks[0]["name"] == "Utilidad"

    def test_tabla_de_hallazgos(self, status_mod, tmp_path):
        filas = [
            make_finding_row("F-1.1", cap="1", sev="critico", estado="abierto"),
            make_finding_row("F-1.2", cap="2", sev="medio", estado="resuelto"),
            # Ruido que el parser debe ignorar: fila corta y fila sin prefijo F-.
            "| F-9.9 | 1 | bajo |",
            "| X-1 | 1 | bajo | f | p | r | abierto | [] |",
        ]
        f = tmp_path / "findings.md"
        f.write_text(make_pass_block(4, filas=filas), encoding="utf-8")
        hallazgos = status_mod.parse_findings(f)[0]["hallazgos"]
        assert [h["id"] for h in hallazgos] == ["F-1.1", "F-1.2"]
        assert hallazgos[0] == {
            "id": "F-1.1", "capitulo": "1", "severidad": "critico", "estado": "abierto",
        }
        assert hallazgos[1]["estado"] == "resuelto"

    def test_firma_humana_con_actor(self, status_mod, tmp_path):
        f = tmp_path / "findings.md"
        f.write_text(make_pass_block(3, tipo="human", actor="marcela"), encoding="utf-8")
        b = status_mod.parse_findings(f)[0]
        assert b["firma"] == "human"
        assert b["actor"] == "marcela"

    def test_campos_ausentes_usan_placeholder(self, status_mod, tmp_path):
        f = tmp_path / "findings.md"
        f.write_text("## Pasada 1 - Estructura\n\ncuerpo sin campos\n", encoding="utf-8")
        b = status_mod.parse_findings(f)[0]
        assert b["estado"] == SEP_RAYA.lower()  # placeholder textual
        assert b["firma"] == SEP_RAYA
        assert b["actor"] == ""

    def test_findings_del_fixture_003(self, status_mod, fact_project):
        """El findings real del fixture 003: 12 bloques (pasadas 1-4 x 3 caps)."""
        proj = fact_project()
        blocks = status_mod.parse_findings(proj / "specs" / "001-fact" / "findings.md")
        assert len(blocks) == 12
        assert all(b["estado"] == "passed" for b in blocks)
        assert all(b["hallazgos"] == [] for b in blocks)


# ---------------------------------------------------------------------------
# newest_spec_dir y count_temario
# ---------------------------------------------------------------------------
class TestNewestSpecDir:
    def _mk_spec(self, root: Path, name: str, con_spec_md: bool = True) -> Path:
        d = root / "specs" / name
        d.mkdir(parents=True)
        if con_spec_md:
            (d / "spec.md").write_text("# x\n", encoding="utf-8")
        return d

    def test_elige_el_de_numero_mas_alto(self, status_mod, tmp_path):
        self._mk_spec(tmp_path, "001-vieja")
        esperado = self._mk_spec(tmp_path, "002-nueva")
        assert status_mod.newest_spec_dir(tmp_path, None) == esperado

    def test_ignora_dirs_sin_spec_md(self, status_mod, tmp_path):
        esperado = self._mk_spec(tmp_path, "001-real")
        self._mk_spec(tmp_path, "002-hueca", con_spec_md=False)
        assert status_mod.newest_spec_dir(tmp_path, None) == esperado

    def test_override_relativo(self, status_mod, tmp_path):
        self._mk_spec(tmp_path, "001-a")
        b = self._mk_spec(tmp_path, "002-b")
        assert status_mod.newest_spec_dir(tmp_path, "002-b") == b

    def test_sin_specs_con_required_false_devuelve_none(self, status_mod, tmp_path):
        assert status_mod.newest_spec_dir(tmp_path, None, required=False) is None

    def test_sin_specs_con_required_true_sale_con_codigo_2(self, status_mod, tmp_path):
        with pytest.raises(SystemExit) as e:
            status_mod.newest_spec_dir(tmp_path, None)
        assert e.value.code == 2


class TestCountTemario:
    def test_cuenta_solo_filas_del_temario(self, status_mod, mini_spec_dir):
        # El plan del mini proyecto tiene 2 filas en Temario y una fila numérica
        # en otra sección que NO debe contarse.
        assert status_mod.count_temario(mini_spec_dir) == 2

    def test_plan_ausente_devuelve_cero(self, status_mod, tmp_path):
        assert status_mod.count_temario(tmp_path) == 0

    def test_temario_del_fixture_003(self, status_mod, fact_project):
        proj = fact_project()
        assert status_mod.count_temario(proj / "specs" / "001-fact") == 3


# ---------------------------------------------------------------------------
# Helpers puros
# ---------------------------------------------------------------------------
class TestHelpers:
    def test_norm_cap(self, status_mod):
        assert status_mod._norm_cap("[1]") == "1"
        assert status_mod._norm_cap(" global ") == "global"
        assert status_mod._norm_cap("") == ""
        assert status_mod._norm_cap(None) == ""

    def test_cap_sort_key_numericos_antes_que_etiquetas(self, status_mod):
        caps = ["10", "global", "2", "1"]
        assert sorted(caps, key=status_mod._cap_sort_key) == ["1", "2", "10", "global"]

    def test_drafted_ordinals(self, status_mod):
        nombres = ["01-uno.md", "2-dos.md", "10-diez.md", "sin-numero.md"]
        assert status_mod._drafted_ordinals(nombres) == {1, 2, 10}

    def test_passes_by_chapter_texto_libre_y_global(self, status_mod):
        blocks = [
            {"num": 1, "capitulos": "1, 2 y 3"},
            {"num": 4, "capitulos": "caps. 1-2"},
            {"num": 2, "capitulos": "global"},
            {"num": 5, "capitulos": "[1]"},  # la pasada 5 no participa
        ]
        out = status_mod._passes_by_chapter(blocks)
        assert out["1"] == {1, 4}
        assert out["2"] == {1, 4}
        assert out["3"] == {1}
        assert out["global"] == {2}
        # Ninguna clave registra la pasada 5.
        assert all(5 not in v for v in out.values())


# ---------------------------------------------------------------------------
# parse_claims (esquema claim-record v1.0)
# ---------------------------------------------------------------------------
class TestParseClaims:
    def test_fixture_003_caps_1_y_2(self, status_mod, claims_md_003):
        parsed, malformed = status_mod.parse_claims(claims_md_003)
        assert set(parsed) == {"1", "2"}
        assert len(parsed["1"]) == 5
        assert len(parsed["2"]) == 5
        assert malformed == set()

    def test_fichero_ausente_es_tolerante(self, status_mod, tmp_path):
        assert status_mod.parse_claims(tmp_path / "claims.md") == ({}, set())

    def test_bloque_json_malformado_marca_el_capitulo(self, status_mod, tmp_path):
        f = tmp_path / "claims.md"
        f.write_text(
            "## Claims - Capítulo 1\n\n```json\n{esto no es json}\n```\n\n"
            "## Claims - Capítulo 2\n\n```json\n"
            '[{"claim_id": "c2-1", "capitulo": 2, "soporte": "soportado"}]\n```\n',
            encoding="utf-8",
        )
        parsed, malformed = status_mod.parse_claims(f)
        assert malformed == {"1"}
        assert set(parsed) == {"2"}

    def test_seccion_sin_bloque_json_es_malformada(self, status_mod, tmp_path):
        f = tmp_path / "claims.md"
        f.write_text("## Claims - Capítulo 3\n\n(prosa sin bloque json)\n", encoding="utf-8")
        parsed, malformed = status_mod.parse_claims(f)
        assert parsed == {}
        assert malformed == {"3"}

    def test_sin_secciones_agrupa_por_campo_capitulo(self, status_mod, tmp_path):
        f = tmp_path / "claims.md"
        f.write_text(
            "```json\n"
            '[{"claim_id": "a", "capitulo": 1, "soporte": "soportado"},\n'
            ' {"claim_id": "b", "capitulo": "[2]", "soporte": "parcial"}]\n'
            "```\n",
            encoding="utf-8",
        )
        parsed, malformed = status_mod.parse_claims(f)
        assert set(parsed) == {"1", "2"}
        assert malformed == set()


# ---------------------------------------------------------------------------
# compute_factuality (data-model §3.1)
# ---------------------------------------------------------------------------
class TestComputeFactuality:
    def test_indice_del_fixture_003(self, status_mod, claims_md_003):
        """Caps 1 y 2: 4 soportado + 1 sin_fuente cada uno. Índice 0.8; el cap 3
        del temario no tiene sección y queda como no medido."""
        parsed, malformed = status_mod.parse_claims(claims_md_003)
        fact = status_mod.compute_factuality(parsed, malformed, expected=3, fill_absent=True)
        assert fact["factuality_global"] == 0.8
        assert fact["factuality_by_chapter"] == {"1": 0.8, "2": 0.8, "3": None}
        assert fact["factuality_unmeasured"] == ["3"]
        assert fact["factuality_pending"] == {}

    def test_parcial_es_verificable_pero_no_soportada(self, status_mod):
        parsed = {"1": [{"soporte": "soportado"}, {"soporte": "parcial"}]}
        fact = status_mod.compute_factuality(parsed, set(), expected=1, fill_absent=True)
        assert fact["factuality_by_chapter"]["1"] == 0.5

    def test_pendiente_sale_del_denominador_y_se_reporta(self, status_mod):
        parsed = {"1": [{"soporte": "soportado"}, {"soporte": "pendiente"}]}
        fact = status_mod.compute_factuality(parsed, set(), expected=1, fill_absent=True)
        assert fact["factuality_by_chapter"]["1"] == 1.0
        assert fact["factuality_pending"] == {"1": 1}

    def test_capitulo_sin_verificables_no_se_mide(self, status_mod):
        parsed = {"1": [{"soporte": "pendiente"}]}
        fact = status_mod.compute_factuality(parsed, set(), expected=1, fill_absent=True)
        assert fact["factuality_by_chapter"]["1"] is None
        assert fact["factuality_global"] is None

    def test_fill_absent_false_no_inventa_capitulos(self, status_mod):
        """Feature inactiva (sin claims.md): salida mínima e inerte, SC-003."""
        fact = status_mod.compute_factuality({}, set(), expected=3, fill_absent=False)
        assert fact["factuality_global"] is None
        assert fact["factuality_by_chapter"] == {}
        assert fact["factuality_unmeasured"] == []

    def test_global_es_micro_promedio(self, status_mod):
        parsed = {
            "1": [{"soporte": "soportado"}] * 9 + [{"soporte": "sin_fuente"}],  # 0.9
            "2": [{"soporte": "contradicho"}, {"soporte": "soportado"}],        # 0.5
        }
        fact = status_mod.compute_factuality(parsed, set(), expected=2, fill_absent=True)
        # Micro-promedio 10/12, no la media de índices (0.7).
        assert fact["factuality_global"] == round(10 / 12, 4)


# ---------------------------------------------------------------------------
# Gates g1-g3 y ciclo por capítulo (evaluate sobre el mini proyecto)
# ---------------------------------------------------------------------------
class TestGates:
    def test_proyecto_verde_es_cerrable(self, status_mod, mini_project):
        state = evaluate(status_mod, mini_project)
        assert state["gates"] == {
            "no_open_criticals": True,
            "human_signatures": True,
            "guide_complete": True,
            "factuality": None,  # sin quality_gates el g4 no se evalúa
        }
        assert state["closeable"] is True
        assert state["criticals_open"] == 0
        assert state["next_step"] == "close"
        assert state["all_chapters_approved"] is True
        assert state["by_chapter"]["1"]["approved"] is True
        assert state["by_chapter"]["1"]["passes_done"] == [1, 2, 3, 4]

    def test_critico_abierto_bloquea(self, status_mod, mini_project):
        filas = [make_finding_row("F-4.1", cap="1", sev="critico", estado="abierto")]
        findings = green_findings().replace(
            make_pass_block(4), make_pass_block(4, filas=filas)
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["gates"]["no_open_criticals"] is False
        assert state["closeable"] is False
        assert state["criticals_open"] == 1
        assert state["revise_by_chapter"] == {"1": 1}
        assert state["next_step"] == "revise"
        assert state["by_chapter"]["1"]["approved"] is False
        assert state["by_chapter"]["2"]["approved"] is True

    def test_critico_resuelto_no_bloquea(self, status_mod, mini_project):
        filas = [make_finding_row("F-4.1", cap="1", sev="critico", estado="resuelto")]
        findings = green_findings().replace(
            make_pass_block(4), make_pass_block(4, filas=filas)
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["gates"]["no_open_criticals"] is True
        assert state["closeable"] is True
        assert state["open_findings_total"] == 0

    def test_medio_abierto_fuerza_revise_pero_no_bloquea_el_cierre(
        self, status_mod, mini_project
    ):
        """Contrato: solo 'critico' bloquea. Un medio abierto deja closeable en
        True pero el heartbeat lo enruta a revise (detector distinto de corrector)."""
        filas = [make_finding_row("F-2.1", cap="2", sev="medio", estado="abierto")]
        findings = green_findings().replace(
            make_pass_block(2), make_pass_block(2, filas=filas)
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["gates"]["no_open_criticals"] is True
        assert state["closeable"] is True
        assert state["revise_pending"] == 1
        assert state["next_step"] == "revise"
        assert state["by_chapter"]["2"]["approved"] is False

    def test_bajo_abierto_es_aviso_y_no_fuerza_revise(self, status_mod, mini_project):
        filas = [make_finding_row("F-3.1", cap="1", sev="bajo", estado="abierto")]
        findings = green_findings().replace(
            make_pass_block(3), make_pass_block(3, filas=filas)
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["closeable"] is True
        assert state["revise_pending"] == 0
        assert state["advisory_open_bajo"] == 1
        assert state["next_step"] == "close"
        assert state["by_chapter"]["1"]["approved"] is True
        assert state["by_chapter"]["1"]["advisory"] == 1

    def test_severidad_no_canonica_es_accionable_pero_no_critica(
        self, status_mod, mini_project
    ):
        """El contrato fija 'critico' sin acento. Una etiqueta desconocida (aquí
        con acento) no cuenta como crítico para g1, pero por diseño va a revise:
        nunca se pierde un hallazgo."""
        filas = [make_finding_row("F-4.1", cap="1", sev="crítico", estado="abierto")]
        findings = green_findings().replace(
            make_pass_block(4), make_pass_block(4, filas=filas)
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["criticals_open"] == 0
        assert state["gates"]["no_open_criticals"] is True
        assert state["revise_pending"] == 1
        assert state["next_step"] == "revise"

    def _exigir_firma_humana(self, proj: Path, pasada: str = "pasada_3_naturalidad"):
        man = proj / ".writeonmars-manifest.json"
        data = json.loads(man.read_text(encoding="utf-8"))
        data["signing_matrix"][pasada] = "human"
        man.write_text(json.dumps(data), encoding="utf-8")

    def test_firma_autonoma_donde_se_exige_humana_bloquea(self, status_mod, mini_project):
        self._exigir_firma_humana(mini_project)
        state = evaluate(status_mod, mini_project)
        assert state["gates"]["human_signatures"] is False
        assert state["closeable"] is False
        assert len(state["sign_violations"]) == 1
        assert "pasada 3" in state["sign_violations"][0]
        assert state["next_step"] == "review"
        assert "firmas" in state["next_detail"]
        p3 = next(p for p in state["passes"] if p["num"] == 3)
        assert p3["signed"] is False
        assert p3["firma_disp"] == "autonomous!"

    def test_firma_humana_con_actor_placeholder_no_cuenta(self, status_mod, mini_project):
        self._exigir_firma_humana(mini_project)
        findings = green_findings().replace(
            make_pass_block(3), make_pass_block(3, tipo="human", actor="pendiente")
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["gates"]["human_signatures"] is False
        assert "sin firmar" in state["sign_violations"][0]

    def test_firma_humana_valida_pasa_el_gate(self, status_mod, mini_project):
        self._exigir_firma_humana(mini_project)
        findings = green_findings().replace(
            make_pass_block(3), make_pass_block(3, tipo="human", actor="marcela")
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["gates"]["human_signatures"] is True
        assert state["closeable"] is True
        p3 = next(p for p in state["passes"] if p["num"] == 3)
        assert p3["signed"] is True
        assert p3["firma_disp"] == "human:marcela"

    def test_guia_incompleta_bloquea_y_pide_implement(self, status_mod, mini_project):
        (mini_project / "chapters" / "02-profundizando.md").unlink()
        state = evaluate(status_mod, mini_project)
        assert state["gates"]["guide_complete"] is False
        assert state["closeable"] is False
        assert state["chapters_written"] == 1
        assert state["chapters_expected"] == 2
        assert state["next_step"] == "implement"
        assert state["by_chapter"]["2"]["drafted"] is False
        assert state["by_chapter"]["2"]["approved"] is False

    def test_capitulo_sin_pasada_4_no_esta_aprobado(self, status_mod, mini_project):
        # La pasada 4 solo cubre el capítulo 1: el 2 queda sin aprobar.
        findings = green_findings().replace(
            make_pass_block(4), make_pass_block(4, caps="[1]")
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["by_chapter"]["1"]["approved"] is True
        assert state["by_chapter"]["2"]["approved"] is False
        assert state["by_chapter"]["2"]["passes_done"] == [1, 2, 3]
        assert state["all_chapters_approved"] is False


# ---------------------------------------------------------------------------
# Gate g4: factualidad (feature 003) sobre el fixture real
# ---------------------------------------------------------------------------
class TestGateFactualidad:
    def test_baseline_sin_umbral_no_evalua_g4(self, status_mod, fact_project):
        proj = fact_project()  # manifest sin quality_gates
        state = evaluate(status_mod, proj)
        assert state["gates"]["factuality"] is None
        assert state["factuality_mode"] is None
        assert state["factuality_global"] == 0.8  # se mide igual: claims.md existe
        assert state["closeable"] is True

    def test_blocking_bajo_umbral_bloquea_y_avisa_inconsistencia(
        self, status_mod, fact_project
    ):
        proj = fact_project(manifest="blocking")  # umbral 0.9, global 0.8
        state = evaluate(status_mod, proj)
        assert state["gates"]["factuality"] is False
        assert state["closeable"] is False
        assert state["factuality_mode"] == "blocking"
        # g4 en rojo sin hallazgos accionables: warning de inconsistencia FR-009.
        assert any("inconsistencia" in w for w in state["warnings"])
        assert state["next_step"] == "review"
        assert "factualidad" in state["next_detail"]

    def test_advisory_informa_pero_no_bloquea(self, status_mod, fact_project):
        proj = fact_project(manifest="advisory")  # umbral 0.9, modo aviso
        state = evaluate(status_mod, proj)
        assert state["gates"]["factuality"] is False
        assert state["closeable"] is True
        assert state["factuality_mode"] == "advisory"
        assert state["next_step"] == "close"

    def test_umbral_alcanzado_pasa(self, status_mod, fact_project):
        proj = fact_project(manifest="pass")  # umbral 0.7, global 0.8
        state = evaluate(status_mod, proj)
        assert state["gates"]["factuality"] is True
        assert state["closeable"] is True

    def test_piso_por_capitulo_puede_tumbar_g4(self, status_mod, fact_project):
        proj = fact_project(manifest="pass")
        man = proj / ".writeonmars-manifest.json"
        data = json.loads(man.read_text(encoding="utf-8"))
        data["quality_gates"]["factuality_min_per_chapter"] = 0.9  # caps a 0.8
        man.write_text(json.dumps(data), encoding="utf-8")
        state = evaluate(status_mod, proj)
        assert state["gates"]["factuality"] is False
        assert state["closeable"] is False

    def test_capitulo_sin_medir_queda_en_unmeasured(self, status_mod, fact_project):
        proj = fact_project()
        state = evaluate(status_mod, proj)
        assert state["factuality_unmeasured"] == ["3"]
        assert state["factuality_by_chapter"]["3"] is None


# ---------------------------------------------------------------------------
# next_step: la escalera del heartbeat
# ---------------------------------------------------------------------------
class TestNextStep:
    def test_sin_manifest_pide_setup(self, status_mod, mini_project):
        (mini_project / ".writeonmars-manifest.json").unlink()
        state = evaluate(status_mod, mini_project)
        assert state["next_step"] == "setup"
        assert state["has_manifest"] is False

    def test_sin_constitucion_pide_setup(self, status_mod, mini_project):
        (mini_project / ".specify" / "memory" / "constitution.md").unlink()
        state = evaluate(status_mod, mini_project)
        assert state["next_step"] == "setup"

    def test_sector_null_pide_constitution(self, status_mod, mini_project):
        man = mini_project / ".writeonmars-manifest.json"
        data = json.loads(man.read_text(encoding="utf-8"))
        data["sector"] = None
        man.write_text(json.dumps(data), encoding="utf-8")
        state = evaluate(status_mod, mini_project)
        assert state["next_step"] == "constitution"

    def test_sin_spec_pide_specify(self, status_mod, mini_project):
        # Fase temprana del orquestador: evaluate tolera spec_dir None.
        state = status_mod.evaluate(mini_project, None)
        assert state["next_step"] == "specify"
        assert state["spec"] == "(sin spec todavía)"

    def test_sin_research_pide_research(self, status_mod, mini_project):
        (mini_project / "specs" / "001-guia" / "research.md").unlink()
        state = evaluate(status_mod, mini_project)
        assert state["next_step"] == "research"

    def test_sin_temario_pide_plan(self, status_mod, mini_project):
        (mini_project / "specs" / "001-guia" / "plan.md").write_text(
            "# Plan vacío\n", encoding="utf-8"
        )
        state = evaluate(status_mod, mini_project)
        assert state["next_step"] == "plan"

    def test_sin_findings_pide_review(self, status_mod, mini_project):
        (mini_project / "specs" / "001-guia" / "findings.md").unlink()
        state = evaluate(status_mod, mini_project)
        assert state["next_step"] == "review"
        assert "findings" in state["next_detail"]

    def test_revise_enumera_los_capitulos_afectados(self, status_mod, mini_project):
        filas = [
            make_finding_row("F-4.1", cap="1", sev="critico", estado="abierto"),
            make_finding_row("F-4.2", cap="2", sev="medio", estado="abierto"),
        ]
        findings = green_findings().replace(
            make_pass_block(4), make_pass_block(4, filas=filas)
        )
        write_findings(mini_project, findings)
        state = evaluate(status_mod, mini_project)
        assert state["next_step"] == "revise"
        assert "[1, 2]" in state["next_detail"]
        assert "1 crítico(s)" in state["next_detail"]


# ---------------------------------------------------------------------------
# CLI (subprocess): --json y --gate, sin agente
# ---------------------------------------------------------------------------
class TestCli:
    def _run(self, scripts_dir, proj: Path, *flags: str):
        return subprocess.run(
            [sys.executable, str(scripts_dir / "status.py"),
             "--project-dir", str(proj), *flags],
            capture_output=True, text=True,
        )

    def test_json_emite_el_estado_completo(self, scripts_dir, fact_project):
        proj = fact_project()
        res = self._run(scripts_dir, proj, "--json")
        assert res.returncode == 0, res.stderr
        state = json.loads(res.stdout)
        assert state["factuality_global"] == 0.8
        assert state["closeable"] is True
        assert state["chapters_expected"] == 3

    def test_gate_sale_0_si_cierra_y_1_si_no(self, scripts_dir, fact_project):
        cerrable = fact_project()
        bloqueado = fact_project(manifest="blocking")
        assert self._run(scripts_dir, cerrable, "--gate").returncode == 0
        assert self._run(scripts_dir, bloqueado, "--gate").returncode == 1

    def test_dashboard_imprime_gates(self, scripts_dir, fact_project):
        proj = fact_project()
        res = self._run(scripts_dir, proj)
        assert res.returncode == 0
        assert "Gates de cierre" in res.stdout
        assert "PROYECTO CERRABLE" in res.stdout
