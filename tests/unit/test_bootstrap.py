"""Tests unitarios de bootstrap.py: versión de la constitución, manifest por
defecto, validación contra el schema y flujo end-to-end en tmp_path.

El end-to-end corre bootstrap.py como subprocess con un stub que fuerza la ruta
sin jsonschema, para que el resultado no dependa de lo instalado en la máquina.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

try:
    import jsonschema  # noqa: F401

    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


# ---------------------------------------------------------------------------
# read_constitution_version
# ---------------------------------------------------------------------------
class TestReadConstitutionVersion:
    def test_lee_el_pie_de_la_constitucion_bundled(self, bootstrap_mod, repo_root):
        v = bootstrap_mod.read_constitution_version()
        assert re.fullmatch(r"\d+\.\d+\.\d+", v)
        # La versión sale del fichero, nunca de una constante: el pie del
        # constitution.md bundled debe contener exactamente esa marca.
        text = (repo_root / "writeonmars" / "memory" / "constitution.md").read_text(
            encoding="utf-8"
        )
        assert f"**Version**: {v}" in text

    def test_la_constante_del_modulo_coincide(self, bootstrap_mod):
        assert bootstrap_mod.CONSTITUTION_VERSION == bootstrap_mod.read_constitution_version()


# ---------------------------------------------------------------------------
# default_manifest
# ---------------------------------------------------------------------------
class TestDefaultManifest:
    def test_claves_requeridas_del_schema(self, bootstrap_mod, repo_root):
        schema = json.loads(
            (repo_root / "writeonmars" / "contracts" / "manifest-schema.json").read_text(
                encoding="utf-8"
            )
        )
        m = bootstrap_mod.default_manifest("op.test", "")
        faltan = [k for k in schema["required"] if k not in m]
        assert faltan == []

    def test_operador_y_email(self, bootstrap_mod):
        m = bootstrap_mod.default_manifest("marcela.gotta", "m@ejemplo.com")
        assert m["human_operators"] == [
            {"id": "marcela.gotta", "role": "author", "email": "m@ejemplo.com"}
        ]

    def test_email_vacio_no_se_incluye(self, bootstrap_mod):
        m = bootstrap_mod.default_manifest("op", "")
        assert "email" not in m["human_operators"][0]

    def test_todas_las_pasadas_arrancan_autonomas(self, bootstrap_mod):
        m = bootstrap_mod.default_manifest("op", "")
        assert set(m["signing_matrix"].values()) == {"autonomous"}
        assert len(m["signing_matrix"]) == 5

    def test_sector_arranca_en_null_y_tipo_editorial(self, bootstrap_mod):
        m = bootstrap_mod.default_manifest("op", "")
        assert m["sector"] is None
        assert m["project_type"] == "editorial"
        assert m["constitution_version"] == bootstrap_mod.CONSTITUTION_VERSION

    def test_mode_default_es_produccion(self, bootstrap_mod):
        m = bootstrap_mod.default_manifest("op", "")
        assert m["mode"] == "produccion"

    @pytest.mark.parametrize("mode", ["produccion", "estudio"])
    def test_mode_explicito(self, bootstrap_mod, mode):
        m = bootstrap_mod.default_manifest("op", "", mode=mode)
        assert m["mode"] == mode

    def test_track_default_es_estandar(self, bootstrap_mod):
        m = bootstrap_mod.default_manifest("op", "")
        assert m["track"] == "estandar"

    @pytest.mark.parametrize("track", ["estandar", "corta"])
    def test_track_se_escribe_siempre(self, bootstrap_mod, track):
        # default_manifest escribe `track` SIEMPRE, también con estandar.
        m = bootstrap_mod.default_manifest("op", "", track=track)
        assert m["track"] == track


# ---------------------------------------------------------------------------
# Helpers de sector (extracción de registro/nombre, listado, bloque de adendas)
# ---------------------------------------------------------------------------
class TestSectorHelpers:
    @pytest.fixture
    def tecnologia_md(self, repo_root) -> Path:
        return repo_root / "writeonmars" / "references" / "sectores" / "tecnologia.md"

    def test_available_sectors_incluye_tecnologia_y_excluye_index(self, bootstrap_mod):
        slugs = bootstrap_mod.available_sectors()
        assert "tecnologia" in slugs
        assert "_index" not in slugs

    def test_extract_registro_tecnologia(self, bootstrap_mod, tecnologia_md):
        assert bootstrap_mod.extract_registro(tecnologia_md) == "tecnico-divulgativo"

    def test_extract_sector_name_tecnologia(self, bootstrap_mod, tecnologia_md):
        assert bootstrap_mod.extract_sector_name(tecnologia_md, "tecnologia") == "Tecnología"

    def test_extract_sector_name_cae_al_slug_si_no_hay_cabecera(
        self, bootstrap_mod, tmp_path
    ):
        f = tmp_path / "raro.md"
        f.write_text("## Registro por defecto\n\n`x`\n", encoding="utf-8")
        assert bootstrap_mod.extract_sector_name(f, "raro") == "raro"

    def test_build_adendas_tiene_tono_calibrado_y_por_referencia(self, bootstrap_mod):
        block = bootstrap_mod.build_adendas_block(
            "tecnologia", "Tecnología", "tecnico-divulgativo", "1.7.0", "2026-07-10"
        )
        assert block.startswith(bootstrap_mod.ADENDAS_MARKER)
        # El encabezado `### Tono calibrado` es OBLIGATORIO (research R2): sin él
        # speckit.specify se atasca en pista corta.
        assert "### Tono calibrado" in block
        assert "POR REFERENCIA" in block
        assert "`tecnico-divulgativo`" in block
        assert "v1.7.0" in block

    def test_build_adendas_sin_registro_lo_declara(self, bootstrap_mod):
        block = bootstrap_mod.build_adendas_block("x", "X", None, "1.7.0", "2026-07-10")
        assert "sin registro declarado" in block
        assert "### Tono calibrado" in block


# ---------------------------------------------------------------------------
# validate_manifest
# ---------------------------------------------------------------------------
class TestValidateManifest:
    def test_default_pasa_sin_jsonschema(self, bootstrap_mod, monkeypatch):
        """Ruta fallback (solo claves requeridas): el manifest por defecto valida."""
        monkeypatch.setitem(sys.modules, "jsonschema", None)  # fuerza ImportError
        bootstrap_mod.validate_manifest(bootstrap_mod.default_manifest("op", ""))

    def test_falla_con_clave_requerida_ausente(self, bootstrap_mod, monkeypatch):
        monkeypatch.setitem(sys.modules, "jsonschema", None)
        m = bootstrap_mod.default_manifest("op", "")
        del m["signing_matrix"]
        with pytest.raises(SystemExit) as e:
            bootstrap_mod.validate_manifest(m)
        assert e.value.code == 1

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="requiere jsonschema instalado")
    def test_default_pasa_con_jsonschema(self, bootstrap_mod):
        """El manifest por defecto valida completo: el schema v1.2.1 admite
        sector null (bootstrap escribe null hasta que speckit.constitution lo fija)."""
        bootstrap_mod.validate_manifest(bootstrap_mod.default_manifest("op", ""))

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="requiere jsonschema instalado")
    def test_con_sector_string_valida_completo(self, bootstrap_mod):
        """Prueba que el fallo anterior es exactamente el sector=null: con un
        slug de sector el manifest valida contra el schema completo."""
        m = bootstrap_mod.default_manifest("op", "")
        m["sector"] = "tecnologia"
        bootstrap_mod.validate_manifest(m)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="requiere jsonschema instalado")
    @pytest.mark.parametrize("mode", ["produccion", "estudio"])
    def test_manifest_con_cada_mode_valida_completo(self, bootstrap_mod, mode):
        m = bootstrap_mod.default_manifest("op", "", mode=mode)
        bootstrap_mod.validate_manifest(m)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="requiere jsonschema instalado")
    def test_manifest_sin_mode_sigue_validando(self, bootstrap_mod):
        m = bootstrap_mod.default_manifest("op", "")
        del m["mode"]
        bootstrap_mod.validate_manifest(m)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="requiere jsonschema instalado")
    @pytest.mark.parametrize("track", ["estandar", "corta"])
    def test_manifest_con_cada_track_valida_completo(self, bootstrap_mod, track):
        # Contra el schema v1.4.0 (track + registro declarados).
        m = bootstrap_mod.default_manifest("op", "", track=track)
        m["sector"] = "tecnologia"
        m["registro"] = "tecnico-divulgativo"
        bootstrap_mod.validate_manifest(m)

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="requiere jsonschema instalado")
    def test_manifest_sin_track_sigue_validando(self, bootstrap_mod):
        m = bootstrap_mod.default_manifest("op", "")
        del m["track"]
        bootstrap_mod.validate_manifest(m)

    def test_sin_schema_solo_avisa(self, bootstrap_mod, monkeypatch, tmp_path, capsys):
        """Si falta contracts/manifest-schema.json se omite la validación."""
        monkeypatch.setattr(bootstrap_mod, "PRESET", tmp_path)
        bootstrap_mod.validate_manifest({})
        assert "omito la validación" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Flujo end-to-end (subprocess, determinista vía stub de jsonschema)
# ---------------------------------------------------------------------------
class TestMainEndToEnd:
    @pytest.fixture
    def stub_sin_jsonschema(self, tmp_path: Path) -> Path:
        """Directorio para PYTHONPATH con un jsonschema falso que fuerza la ruta
        fallback de validate_manifest (así el test no depende del entorno)."""
        stub = tmp_path / "stub"
        stub.mkdir()
        (stub / "jsonschema.py").write_text(
            'raise ImportError("stub de test: fuerza la ruta sin jsonschema")\n',
            encoding="utf-8",
        )
        return stub

    def _run(self, scripts_dir, proj: Path, stub: Path, *extra: str):
        env = dict(os.environ, PYTHONPATH=str(stub))
        return subprocess.run(
            [sys.executable, str(scripts_dir / "bootstrap.py"),
             "--project-dir", str(proj), *extra],
            capture_output=True, text=True, env=env,
        )

    @pytest.fixture
    def proyecto_speckit(self, tmp_path: Path) -> Path:
        proj = tmp_path / "proyecto"
        (proj / ".specify").mkdir(parents=True)
        return proj

    def test_crea_constitucion_y_manifest(
        self, scripts_dir, bootstrap_mod, proyecto_speckit, stub_sin_jsonschema
    ):
        res = self._run(scripts_dir, proyecto_speckit, stub_sin_jsonschema,
                        "--operator", "test.op")
        assert res.returncode == 0, res.stderr
        dst = proyecto_speckit / ".specify" / "memory" / "constitution.md"
        assert dst.exists()
        manifest = json.loads(
            (proyecto_speckit / ".writeonmars-manifest.json").read_text(encoding="utf-8")
        )
        assert manifest["constitution_version"] == bootstrap_mod.CONSTITUTION_VERSION
        assert manifest["human_operators"][0]["id"] == "test.op"
        assert manifest["mode"] == "produccion"

    def test_crea_manifest_en_modo_estudio(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        res = self._run(
            scripts_dir,
            proyecto_speckit,
            stub_sin_jsonschema,
            "--operator",
            "test.op",
            "--mode",
            "estudio",
        )
        assert res.returncode == 0, res.stderr
        manifest = json.loads(
            (proyecto_speckit / ".writeonmars-manifest.json").read_text(encoding="utf-8")
        )
        assert manifest["mode"] == "estudio"

    def test_sin_specify_falla(self, scripts_dir, tmp_path, stub_sin_jsonschema):
        res = self._run(scripts_dir, tmp_path, stub_sin_jsonschema)
        assert res.returncode == 1
        assert "no es un proyecto spec-kit" in res.stderr

    def test_mode_invalido_por_entorno_falla(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        """argparse no valida `choices` sobre el default: un WRITEONMARS_MODE
        con typo debe cazarlo el guard explícito antes de escribir el manifest
        (sin jsonschema el fallback solo comprueba claves required)."""
        env = dict(
            os.environ,
            PYTHONPATH=str(stub_sin_jsonschema),
            WRITEONMARS_MODE="Estudio",
        )
        res = subprocess.run(
            [sys.executable, str(scripts_dir / "bootstrap.py"),
             "--project-dir", str(proyecto_speckit)],
            capture_output=True, text=True, env=env,
        )
        assert res.returncode == 1
        assert "mode inválido" in res.stderr
        assert not (proyecto_speckit / ".writeonmars-manifest.json").exists()

    def test_track_corta_escribe_la_clave(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        res = self._run(scripts_dir, proyecto_speckit, stub_sin_jsonschema, "--track", "corta")
        assert res.returncode == 0, res.stderr
        m = json.loads(
            (proyecto_speckit / ".writeonmars-manifest.json").read_text(encoding="utf-8")
        )
        assert m["track"] == "corta"
        # Sin --sector: comportamiento actual intacto.
        assert m["sector"] is None
        assert "registro" not in m
        const = (proyecto_speckit / ".specify" / "memory" / "constitution.md").read_text(
            encoding="utf-8"
        )
        assert "<!-- WRITEONMARS:ADENDAS -->" not in const

    def test_track_corta_por_entorno_escribe_la_clave(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        env = dict(
            os.environ, PYTHONPATH=str(stub_sin_jsonschema), WRITEONMARS_TRACK="corta"
        )
        res = subprocess.run(
            [sys.executable, str(scripts_dir / "bootstrap.py"),
             "--project-dir", str(proyecto_speckit)],
            capture_output=True, text=True, env=env,
        )
        assert res.returncode == 0, res.stderr
        m = json.loads(
            (proyecto_speckit / ".writeonmars-manifest.json").read_text(encoding="utf-8")
        )
        assert m["track"] == "corta"

    def test_track_invalido_por_entorno_falla(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        """argparse no valida `choices` sobre el default: un WRITEONMARS_TRACK con
        typo debe cazarlo el guard explícito antes de escribir el manifest."""
        env = dict(
            os.environ, PYTHONPATH=str(stub_sin_jsonschema), WRITEONMARS_TRACK="rapida"
        )
        res = subprocess.run(
            [sys.executable, str(scripts_dir / "bootstrap.py"),
             "--project-dir", str(proyecto_speckit)],
            capture_output=True, text=True, env=env,
        )
        assert res.returncode == 1
        assert "track inválido" in res.stderr
        assert not (proyecto_speckit / ".writeonmars-manifest.json").exists()

    def test_sector_escribe_sector_registro_y_adendas(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        res = self._run(
            scripts_dir, proyecto_speckit, stub_sin_jsonschema, "--sector", "tecnologia"
        )
        assert res.returncode == 0, res.stderr
        m = json.loads(
            (proyecto_speckit / ".writeonmars-manifest.json").read_text(encoding="utf-8")
        )
        assert m["sector"] == "tecnologia"
        assert m["registro"] == "tecnico-divulgativo"
        const = (proyecto_speckit / ".specify" / "memory" / "constitution.md").read_text(
            encoding="utf-8"
        )
        assert "<!-- WRITEONMARS:ADENDAS -->" in const
        assert "POR REFERENCIA" in const
        assert "### Tono calibrado" in const

    def test_sector_por_entorno_tambien_aplica(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        env = dict(
            os.environ,
            PYTHONPATH=str(stub_sin_jsonschema),
            WRITEONMARS_TRACK="corta",
            WRITEONMARS_SECTOR="tecnologia",
        )
        res = subprocess.run(
            [sys.executable, str(scripts_dir / "bootstrap.py"),
             "--project-dir", str(proyecto_speckit)],
            capture_output=True, text=True, env=env,
        )
        assert res.returncode == 0, res.stderr
        m = json.loads(
            (proyecto_speckit / ".writeonmars-manifest.json").read_text(encoding="utf-8")
        )
        assert m["track"] == "corta"
        assert m["sector"] == "tecnologia"
        assert m["registro"] == "tecnico-divulgativo"

    def test_sector_inexistente_falla_listando_disponibles(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        res = self._run(
            scripts_dir, proyecto_speckit, stub_sin_jsonschema, "--sector", "inventado"
        )
        assert res.returncode == 1
        assert "sector inválido" in res.stderr
        assert "Sectores disponibles" in res.stderr
        assert "tecnologia" in res.stderr
        # Falla antes de tocar el disco: ni manifest ni constitución.
        assert not (proyecto_speckit / ".writeonmars-manifest.json").exists()
        assert not (proyecto_speckit / ".specify" / "memory" / "constitution.md").exists()

    def test_sector_no_reescribe_centinela_preexistente(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        """Adendas calibradas a mano (centinela ya presente) se respetan: el
        bloque por referencia no se materializa y solo se avisa."""
        memory = proyecto_speckit / ".specify" / "memory"
        memory.mkdir(parents=True)
        const = memory / "constitution.md"
        const.write_text(
            "# Núcleo\n\n**Version**: 1.7.0\n\n"
            "<!-- WRITEONMARS:ADENDAS -->\n\n## Adendas del proyecto\n\n"
            "TONO CALIBRADO A MANO por la operadora.\n",
            encoding="utf-8",
        )
        res = self._run(
            scripts_dir, proyecto_speckit, stub_sin_jsonschema, "--sector", "tecnologia"
        )
        assert res.returncode == 0, res.stderr
        final = const.read_text(encoding="utf-8")
        assert "TONO CALIBRADO A MANO" in final          # adendas a mano preservadas
        assert "POR REFERENCIA" not in final             # no se re-materializó
        assert final.count("<!-- WRITEONMARS:ADENDAS -->") == 1
        assert "aviso" in res.stdout

    @pytest.mark.skipif(not HAS_JSONSCHEMA, reason="requiere jsonschema instalado")
    def test_manifest_corta_sector_generado_valida_contra_schema(
        self, scripts_dir, repo_root, proyecto_speckit
    ):
        """El manifest generado por un run corta+sector valida contra el schema
        v1.4.0 (sin el stub: entorno real con jsonschema)."""
        import jsonschema

        res = subprocess.run(
            [sys.executable, str(scripts_dir / "bootstrap.py"),
             "--project-dir", str(proyecto_speckit),
             "--track", "corta", "--sector", "tecnologia"],
            capture_output=True, text=True,
        )
        assert res.returncode == 0, res.stderr
        manifest = json.loads(
            (proyecto_speckit / ".writeonmars-manifest.json").read_text(encoding="utf-8")
        )
        schema = json.loads(
            (repo_root / "writeonmars" / "contracts" / "manifest-schema.json").read_text(
                encoding="utf-8"
            )
        )
        jsonschema.validate(instance=manifest, schema=schema)
        assert manifest["track"] == "corta"
        assert manifest["sector"] == "tecnologia"
        assert manifest["registro"] == "tecnico-divulgativo"

    def test_sin_force_no_sobrescribe(
        self, scripts_dir, proyecto_speckit, stub_sin_jsonschema
    ):
        self._run(scripts_dir, proyecto_speckit, stub_sin_jsonschema)
        man = proyecto_speckit / ".writeonmars-manifest.json"
        man.write_text('{"marca": "editado a mano"}', encoding="utf-8")
        res = self._run(scripts_dir, proyecto_speckit, stub_sin_jsonschema)
        assert res.returncode == 0
        assert "ya existe" in res.stdout
        assert json.loads(man.read_text(encoding="utf-8")) == {"marca": "editado a mano"}

    def test_force_resella_el_nucleo_preservando_adendas(
        self, scripts_dir, bootstrap_mod, proyecto_speckit, stub_sin_jsonschema
    ):
        self._run(scripts_dir, proyecto_speckit, stub_sin_jsonschema)
        dst = proyecto_speckit / ".specify" / "memory" / "constitution.md"
        adendas = (
            f"{bootstrap_mod.ADENDAS_MARKER}\n## Adendas del proyecto\n\n"
            "Sector: tecnologia. Tono: cercano.\n"
        )
        # Simula una guía configurada: núcleo tocado + adendas propias.
        dst.write_text("# núcleo desactualizado\n\n" + adendas, encoding="utf-8")
        res = self._run(scripts_dir, proyecto_speckit, stub_sin_jsonschema, "--force")
        assert res.returncode == 0, res.stderr
        final = dst.read_text(encoding="utf-8")
        assert "Sector: tecnologia. Tono: cercano." in final  # adendas preservadas
        assert "núcleo desactualizado" not in final           # núcleo re-sellado
        assert f"**Version**: {bootstrap_mod.CONSTITUTION_VERSION}" in final
