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

    def test_sin_specify_falla(self, scripts_dir, tmp_path, stub_sin_jsonschema):
        res = self._run(scripts_dir, tmp_path, stub_sin_jsonschema)
        assert res.returncode == 1
        assert "no es un proyecto spec-kit" in res.stderr

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
