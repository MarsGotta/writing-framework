"""Tests unitarios de export.py: helpers puros (slugify, parseo de spec/plan,
ensamblado de HTML) y validación de factualidad contra claims.md.

Nada de aquí lanza pandoc ni Chrome: las rutas que los invocan se prueban con
subprocess.run mockeado.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_CORTA = REPO_ROOT / "tests" / "fixtures" / "006-corta" / "produccion"


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------
class TestSlugify:
    def test_minusculas_y_guiones(self, export_mod):
        assert export_mod.slugify("Mi Guia De Prueba") == "mi-guia-de-prueba"

    def test_conserva_acentos(self, export_mod):
        # \w en Python es unicode: los acentos sobreviven al slug (comportamiento
        # actual documentado, no aspiracional).
        assert export_mod.slugify("Guía de Kubernetes") == "guía-de-kubernetes"

    def test_quita_simbolos_y_colapsa_separadores(self, export_mod):
        assert export_mod.slugify("t: (v2), ¡ya!  _final") == "t-v2-ya-final"

    def test_separador_al_final_sobrevive(self, export_mod):
        # Quirk documentado: el strip() ocurre antes de colapsar separadores,
        # así que un "_" o "-" final deja un guion colgante en el slug (y por
        # tanto en el nombre del PDF). Inofensivo con títulos reales.
        assert export_mod.slugify("título_") == "título-"

    def test_vacio_cae_a_guia(self, export_mod):
        assert export_mod.slugify("") == "guia"
        assert export_mod.slugify("!!!") == "guia"


# ---------------------------------------------------------------------------
# newest_spec_dir (variante de export: exige plan.md)
# ---------------------------------------------------------------------------
class TestNewestSpecDir:
    def _mk_spec(self, root: Path, name: str, con_plan: bool = True) -> Path:
        d = root / "specs" / name
        d.mkdir(parents=True)
        if con_plan:
            (d / "plan.md").write_text("## Temario\n", encoding="utf-8")
        return d

    def test_prefiere_numero_mas_alto_con_plan(self, export_mod, tmp_path):
        self._mk_spec(tmp_path, "001-a")
        esperado = self._mk_spec(tmp_path, "002-b")
        self._mk_spec(tmp_path, "003-sin-plan", con_plan=False)
        assert export_mod.newest_spec_dir(tmp_path, None) == esperado

    def test_sin_specs_required_false_devuelve_none(self, export_mod, tmp_path):
        # Guía legacy de layout plano: export sigue funcionando sin specs/.
        assert export_mod.newest_spec_dir(tmp_path, None, required=False) is None

    def test_override_sin_plan_ni_spec_falla(self, export_mod, tmp_path):
        (tmp_path / "specs" / "001-hueca").mkdir(parents=True)
        with pytest.raises(SystemExit) as e:
            export_mod.newest_spec_dir(tmp_path, "001-hueca")
        assert e.value.code == 1

    def test_override_valido(self, export_mod, tmp_path):
        d = self._mk_spec(tmp_path, "001-real")
        assert export_mod.newest_spec_dir(tmp_path, "001-real") == d


# ---------------------------------------------------------------------------
# Parseo de spec.md y plan.md
# ---------------------------------------------------------------------------
class TestParseTitle:
    def test_formato_feature_specification(self, export_mod, tmp_path):
        f = tmp_path / "spec.md"
        f.write_text("# Feature Specification: Guía de podado\n", encoding="utf-8")
        assert export_mod.parse_title(f, "fallback") == "Guía de podado"

    def test_h1_plano(self, export_mod, tmp_path):
        f = tmp_path / "spec.md"
        f.write_text("# Mi título\n", encoding="utf-8")
        assert export_mod.parse_title(f, "fallback") == "Mi título"

    def test_h1_con_placeholder_se_salta(self, export_mod, tmp_path):
        f = tmp_path / "spec.md"
        f.write_text("# [FEATURE NAME]\n", encoding="utf-8")
        assert export_mod.parse_title(f, "fallback") == "fallback"

    def test_fichero_ausente_usa_fallback(self, export_mod, tmp_path):
        assert export_mod.parse_title(tmp_path / "no.md", "fallback") == "fallback"


class TestParseTemario:
    def test_filas_validas_y_ruido(self, export_mod, tmp_path):
        f = tmp_path / "plan.md"
        f.write_text(
            "## Temario\n\n"
            "| # | Título | Promesa |\n"
            "|---|--------|---------|\n"
            "| 1 | Uno | p1 |\n"
            "| 2 | [Título placeholder] | p2 |\n"
            "| ... | ... | ... |\n"
            "| 3 | Tres | p3 |\n\n"
            "## Otra sección\n\n"
            "| 9 | Fuera | del temario |\n",
            encoding="utf-8",
        )
        temario = export_mod.parse_temario(f)
        assert set(temario) == {1, 3}
        assert temario[1] == {"title": "Uno", "promesa": "p1"}

    def test_plan_ausente(self, export_mod, tmp_path):
        assert export_mod.parse_temario(tmp_path / "no.md") == {}

    def test_temario_del_mini_proyecto(self, export_mod, mini_spec_dir):
        temario = export_mod.parse_temario(mini_spec_dir / "plan.md")
        assert set(temario) == {1, 2}
        assert temario[2]["title"] == "Profundizando"


class TestChapters:
    def test_first_h1(self, export_mod, tmp_path):
        f = tmp_path / "01-cap.md"
        f.write_text("intro\n\n# El título real\n## Sub\n", encoding="utf-8")
        assert export_mod.first_h1(f) == "El título real"

    def test_first_h1_sin_h1_usa_el_stem(self, export_mod, tmp_path):
        f = tmp_path / "01-cap.md"
        f.write_text("sin encabezados\n", encoding="utf-8")
        assert export_mod.first_h1(f) == "01-cap"

    def test_leading_num(self, export_mod):
        assert export_mod.leading_num("03-intro.md") == 3
        assert export_mod.leading_num("apendice.md") is None

    def test_collect_chapters_solo_numerados_y_ordenados(self, export_mod, tmp_path):
        cdir = tmp_path / "chapters"
        cdir.mkdir()
        for name in ["02-b.md", "01-a.md", "notas.md"]:
            (cdir / name).write_text("# x\n", encoding="utf-8")
        got = export_mod.collect_chapters(cdir)
        assert [(n, p.name) for n, p in got] == [(1, "01-a.md"), (2, "02-b.md")]

    def test_collect_chapters_dir_ausente(self, export_mod, tmp_path):
        assert export_mod.collect_chapters(tmp_path / "nada") == []


# ---------------------------------------------------------------------------
# Validación de factualidad (D1-A: export valida, no genera)
# ---------------------------------------------------------------------------
class TestValidateClaims:
    def test_sin_claims_no_valida_nada(self, export_mod, tmp_path):
        assert export_mod.validate_claims(None, [(1, tmp_path)]) == []

    def test_load_claims_del_fixture_003(self, export_mod, fact_project):
        proj = fact_project()
        by_chap = export_mod.load_claims_by_chapter(proj / "specs" / "001-fact")
        assert set(by_chap) == {"1", "2"}
        assert len(by_chap["1"]) == 5

    def test_avisa_soporte_sin_fuente_y_capitulo_sin_cobertura(
        self, export_mod, fact_project
    ):
        proj = fact_project()
        spec_dir = proj / "specs" / "001-fact"
        chapters = export_mod.collect_chapters(proj / "chapters")
        warnings = export_mod.validate_claims(spec_dir, chapters)
        # El fixture trae un sin_fuente en cap 1 y otro en cap 2, y el cap 3
        # no tiene sección en claims.md.
        assert sum("sin_fuente" in w for w in warnings) == 2
        assert any("cap 03: sin cobertura" in w for w in warnings)

    def test_todo_soportado_no_avisa(self, export_mod, tmp_path):
        spec = tmp_path / "specs" / "001-x"
        spec.mkdir(parents=True)
        (spec / "claims.md").write_text(
            "## Claims - Capítulo 1\n\n```json\n"
            + json.dumps([{"claim_id": "c1", "capitulo": 1, "soporte": "soportado"}])
            + "\n```\n",
            encoding="utf-8",
        )
        cap = tmp_path / "01-uno.md"
        cap.write_text("# Uno\n", encoding="utf-8")
        assert export_mod.validate_claims(spec, [(1, cap)]) == []


# ---------------------------------------------------------------------------
# Ensamblado de HTML (sin pandoc real ni Chrome real)
# ---------------------------------------------------------------------------
class TestHtml:
    def test_wrap_chapter_sources_envuelve_fuentes(self, export_mod):
        html_in = '<h1>Cap</h1>\n<p>texto</p>\n<h2 id="fuentes">Fuentes</h2>\n<ul></ul>'
        out = export_mod.wrap_chapter_sources(html_in)
        assert '<div class="chapter-sources">' in out
        assert out.index("chapter-sources") < out.index("Fuentes")

    def test_wrap_chapter_sources_sin_fuentes_no_toca(self, export_mod):
        html_in = "<h1>Cap</h1><p>texto</p>"
        assert export_mod.wrap_chapter_sources(html_in) == html_in

    def test_pandoc_fragment_mockeado(self, export_mod, tmp_path, monkeypatch):
        def fake_run(cmd, **kwargs):
            assert cmd[0] == "pandoc"

            class R:
                stdout = "<h1>Cap</h1>\n<h2>Fuentes</h2>\n<p>f</p>"

            return R()

        monkeypatch.setattr(export_mod.subprocess, "run", fake_run)
        md = tmp_path / "01-cap.md"
        md.write_text("# Cap\n", encoding="utf-8")
        frag = export_mod.pandoc_fragment(md, "cap-01", is_chapter=True)
        assert '<div class="chapter" id="cap-01">' in frag
        assert '<div class="chapter-sources">' in frag

    def test_pandoc_ausente_falla_con_mensaje(self, export_mod, tmp_path, monkeypatch):
        def fake_run(cmd, **kwargs):
            raise FileNotFoundError("pandoc")

        monkeypatch.setattr(export_mod.subprocess, "run", fake_run)
        md = tmp_path / "x.md"
        md.write_text("# x\n", encoding="utf-8")
        with pytest.raises(SystemExit) as e:
            export_mod.pandoc_fragment(md, "x")
        assert e.value.code == 1

    def test_build_cover_escapa_html(self, export_mod):
        out = export_mod.build_cover("", "<Guía> & co", "sub", "2026")
        assert "&lt;Guía&gt; &amp; co" in out
        assert "<Guía>" not in out

    def test_build_toc_incluye_secciones_y_anclas(self, export_mod):
        toc = export_mod.build_toc(
            "Una guía",
            intro=[("Acerca de", "desc", "intro-readme")],
            chapters=[("01", "Uno", "p1", "cap-01")],
            refs=[("Glosario", "términos", "ref-glosario")],
        )
        for esperado in ['href="#intro-readme"', 'href="#cap-01"', 'href="#ref-glosario"',
                         "Material introductorio", "Capítulos", "Material de referencia"]:
            assert esperado in toc


# ---------------------------------------------------------------------------
# find_chrome (nunca se lanza Chrome: solo localización)
# ---------------------------------------------------------------------------
class TestFindChrome:
    def test_override_existente_gana(self, export_mod, tmp_path):
        binario = tmp_path / "mi-chrome"
        binario.write_text("#!/bin/sh\n", encoding="utf-8")
        assert export_mod.find_chrome(str(binario)) == str(binario)

    def test_override_inexistente_falla(self, export_mod, monkeypatch):
        monkeypatch.setattr(export_mod.shutil, "which", lambda _: None)
        with pytest.raises(SystemExit):
            export_mod.find_chrome("/no/existe/chrome")

    def test_candidato_resuelto_por_which(self, export_mod, monkeypatch):
        monkeypatch.setattr(export_mod, "CHROME_CANDIDATES", ["chromium-fake"])
        monkeypatch.setattr(
            export_mod.shutil, "which",
            lambda c: "/usr/bin/chromium-fake" if c == "chromium-fake" else None,
        )
        assert export_mod.find_chrome(None) == "chromium-fake"

    def test_sin_candidatos_falla_con_pista(self, export_mod, monkeypatch, capsys):
        monkeypatch.setattr(export_mod, "CHROME_CANDIDATES", [])
        monkeypatch.setattr(export_mod.shutil, "which", lambda _: None)
        with pytest.raises(SystemExit):
            export_mod.find_chrome(None)
        assert "WOM_CHROME" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Pista corta (feature 006): portada compacta y bifurcación del ensamblado.
# Todo se verifica sin Chrome: funciones puras + HTML intermedio (pandoc mockeado).
# ---------------------------------------------------------------------------
def _fake_pandoc(export_mod, monkeypatch, stdout: str) -> None:
    def fake_run(cmd, **kwargs):
        class R:
            pass

        R.stdout = stdout
        return R()

    monkeypatch.setattr(export_mod.subprocess, "run", fake_run)


class TestPistaCorta:
    def test_build_cover_compact_marcado_y_sin_eyebrow_ni_subtitle(self, export_mod):
        out = export_mod.build_cover_compact("T", "A", "2026")
        assert "cover-compact" in out
        assert "T" in out and "A" in out and "2026" in out
        assert "cover-eyebrow" not in out
        assert "cover-subtitle" not in out

    def test_cover_author_prefiere_email_luego_id_y_vacios(self, export_mod):
        assert export_mod.cover_author(
            {"human_operators": [{"id": "m", "email": "m@x.com"}]}
        ) == "m@x.com"
        assert export_mod.cover_author(
            {"human_operators": [{"id": "m", "role": "author"}]}
        ) == "m"
        assert export_mod.cover_author({"human_operators": []}) == ""
        assert export_mod.cover_author(None) == ""

    def test_html_corta_no_contiene_toc_page(self, export_mod, monkeypatch):
        _fake_pandoc(export_mod, monkeypatch, "<h1>Cap</h1>\n<p>x</p>")
        project = FIXTURE_CORTA
        manifest = export_mod.findings_lib.load_manifest(project)
        track = export_mod.findings_lib.project_track(manifest)
        assert track == "corta"
        html_out, chapters = export_mod.assemble_html(
            project,
            project / "specs" / "001-mi-pieza",
            project / "chapters",
            title="La pieza",
            meta="2026",
            track=track,
            author=export_mod.cover_author(manifest),
        )
        assert "toc-page" not in html_out
        assert "cover-compact" in html_out
        # human_operators[0].email materializa la línea de autor.
        assert "marcela@example.com" in html_out
        assert len(chapters) == 1

    def test_html_estandar_conserva_toc_y_eyebrow(
        self, export_mod, fact_project, monkeypatch
    ):
        # Regresión: proyecto sin track (⇒ estandar) mantiene índice y portada larga.
        _fake_pandoc(export_mod, monkeypatch, "<h1>Cap</h1>\n<h2>Fuentes</h2>\n<p>x</p>")
        project = fact_project()
        manifest = export_mod.findings_lib.load_manifest(project)
        track = export_mod.findings_lib.project_track(manifest)
        assert track == "estandar"
        html_out, _chapters = export_mod.assemble_html(
            project,
            project / "specs" / "001-fact",
            project / "chapters",
            title="Guía de factualidad",
            eyebrow="Una guía",
            meta="2026",
            track=track,
        )
        assert "toc-page" in html_out
        assert "cover-eyebrow" in html_out
        assert "cover-compact" not in html_out
