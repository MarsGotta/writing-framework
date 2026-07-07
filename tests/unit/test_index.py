"""Tests unitarios de index.py: tokenización, chunking, scoring TF interno y
ciclo build/query sobre un proyecto en tmp_path.

El backend bm25 es opcional: para el test de query se fuerza la ruta interna
(TF cosine) mockeando _score_bm25, así el resultado no depende del entorno.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# tokenize
# ---------------------------------------------------------------------------
class TestTokenize:
    def test_minusculas_y_sin_puntuacion(self, index_mod):
        assert index_mod.tokenize("¡Hola, Mundo!") == ["hola", "mundo"]

    def test_conserva_acentos_enie_y_numeros(self, index_mod):
        assert index_mod.tokenize("El año 2024 tomé café") == [
            "el", "año", "2024", "tomé", "café",
        ]

    def test_separa_por_guiones(self, index_mod):
        assert index_mod.tokenize("context-window") == ["context", "window"]

    def test_vacio(self, index_mod):
        assert index_mod.tokenize("") == []


# ---------------------------------------------------------------------------
# chunk_markdown
# ---------------------------------------------------------------------------
class TestChunkMarkdown:
    def test_divide_por_encabezados(self, index_mod, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text(
            "# Título\n\nintro breve\n\n## Sección A\n\ntexto de a\n\n"
            "## Sección B\n\ntexto de b\n",
            encoding="utf-8",
        )
        chunks = index_mod.chunk_markdown(f, tmp_path)
        assert [(c["heading"], c["text"]) for c in chunks] == [
            ("Título", "intro breve"),
            ("Sección A", "texto de a"),
            ("Sección B", "texto de b"),
        ]
        assert all(c["file"] == "doc.md" for c in chunks)

    def test_seccion_larga_se_trocea_en_chunk_words(self, index_mod, tmp_path):
        f = tmp_path / "largo.md"
        palabras_por_linea = 10
        lineas = (index_mod.CHUNK_WORDS * 2) // palabras_por_linea + 2
        cuerpo = "\n".join("palabra " * palabras_por_linea for _ in range(lineas))
        f.write_text(f"## Única\n\n{cuerpo}\n", encoding="utf-8")
        chunks = index_mod.chunk_markdown(f, tmp_path)
        assert len(chunks) >= 2
        assert all(c["heading"] == "Única" for c in chunks)

    def test_fichero_solo_encabezados_no_produce_chunks(self, index_mod, tmp_path):
        f = tmp_path / "hueco.md"
        f.write_text("# Uno\n\n## Dos\n", encoding="utf-8")
        assert index_mod.chunk_markdown(f, tmp_path) == []


# ---------------------------------------------------------------------------
# iter_source_files
# ---------------------------------------------------------------------------
class TestIterSourceFiles:
    def test_patrones_del_proyecto(self, index_mod, mini_project):
        (mini_project / "glosario.md").write_text("# Glosario\n\ntérmino\n", encoding="utf-8")
        files = {p.name for p in index_mod.iter_source_files(mini_project)}
        assert "01-primeros-pasos.md" in files
        assert "02-profundizando.md" in files
        assert "research.md" in files
        assert "findings.md" in files
        assert "glosario.md" in files
        # spec.md y plan.md no son fuentes de contenido indexable.
        assert "spec.md" not in files
        assert "plan.md" not in files


# ---------------------------------------------------------------------------
# Scoring TF interno (backend sin dependencias)
# ---------------------------------------------------------------------------
class TestScoreTf:
    def _chunks(self, *token_lists):
        return [{"tokens": list(t)} for t in token_lists]

    def test_documento_relevante_puntua_mas(self, index_mod):
        chunks = self._chunks(
            ["kubernetes", "pod", "kubernetes"], ["gato", "siames", "pelo"],
        )
        scores, engine = index_mod._score_tf(chunks, ["kubernetes"])
        assert engine == "tf"
        assert scores[0] > scores[1]
        assert scores[1] == 0.0

    def test_coincidencia_exacta_da_uno(self, index_mod):
        chunks = self._chunks(["kubernetes"], ["gato"])
        scores, _ = index_mod._score_tf(chunks, ["kubernetes"])
        assert scores[0] == pytest.approx(1.0)

    def test_consulta_sin_solape_da_cero(self, index_mod):
        chunks = self._chunks(["uno", "dos"], ["tres"])
        scores, _ = index_mod._score_tf(chunks, ["ausente"])
        assert scores == [0.0, 0.0]


# ---------------------------------------------------------------------------
# build y query (ciclo completo en tmp_path)
# ---------------------------------------------------------------------------
class TestBuildQuery:
    def test_build_escribe_el_indice(self, index_mod, mini_project, capsys):
        index_mod.build(mini_project)
        out = mini_project / index_mod.INDEX_NAME
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["n"] == len(data["chunks"]) > 0
        assert all("tokens" in c and "file" in c for c in data["chunks"])
        assert "fragmentos" in capsys.readouterr().out

    def test_build_sin_markdown_falla(self, index_mod, tmp_path):
        with pytest.raises(SystemExit) as e:
            index_mod.build(tmp_path)
        assert e.value.code == 1

    def test_load_sin_indice_falla(self, index_mod, tmp_path):
        with pytest.raises(SystemExit) as e:
            index_mod._load(tmp_path)
        assert e.value.code == 1

    def test_query_con_backend_interno(self, index_mod, mini_project, monkeypatch, capsys):
        index_mod.build(mini_project)
        capsys.readouterr()  # descarta la salida del build

        def sin_bm25(chunks, q_tokens):
            raise ImportError("forzado por el test")

        monkeypatch.setattr(index_mod, "_score_bm25", sin_bm25)
        index_mod.query(mini_project, "capítulo dos", top=3)
        out = capsys.readouterr().out
        assert "motor: tf" in out
        assert "02-profundizando.md" in out

    def test_query_vacia_falla(self, index_mod, mini_project):
        index_mod.build(mini_project)
        with pytest.raises(SystemExit):
            index_mod.query(mini_project, "¡¡!!", top=3)
