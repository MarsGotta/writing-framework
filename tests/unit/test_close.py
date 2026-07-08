"""Tests unitarios de close.py: orquestación gate + export.

close.py solo encadena subprocesos (status.py --gate y export.py), así que se
prueba (a) la construcción del comando con subprocess mockeado, (b) el flujo de
main() con run() mockeado y (c) el gate real vía CLI con --no-export, que nunca
llega a pandoc ni a Chrome.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


class TestRun:
    def test_construye_el_comando_con_el_interprete_actual(self, close_mod, monkeypatch):
        capturado = {}

        def fake_sub_run(cmd):
            capturado["cmd"] = cmd

            class R:
                returncode = 7

            return R()

        monkeypatch.setattr(close_mod.subprocess, "run", fake_sub_run)
        rc = close_mod.run("status.py", ["--gate", "--project-dir", "/p"])
        assert rc == 7
        cmd = capturado["cmd"]
        assert cmd[0] == sys.executable
        assert cmd[1].endswith("status.py")
        assert Path(cmd[1]).parent == close_mod.HERE  # hermano en scripts/
        assert cmd[2:] == ["--gate", "--project-dir", "/p"]


class TestMain:
    @pytest.fixture
    def calls(self, close_mod, monkeypatch):
        """Mockea close.run registrando llamadas; devuelve la lista y un dict
        mutable de returncodes por script."""
        registro: list[tuple[str, list[str]]] = []
        rcs = {"status.py": 0, "export.py": 0}

        def fake_run(script, extra):
            registro.append((script, list(extra)))
            return rcs[script]

        monkeypatch.setattr(close_mod, "run", fake_run)
        return registro, rcs

    def _main(self, close_mod, monkeypatch, *argv: str):
        monkeypatch.setattr(sys, "argv", ["close.py", *argv])
        return close_mod.main()

    def test_gate_bloqueado_no_exporta(self, close_mod, monkeypatch, calls, capsys):
        registro, rcs = calls
        rcs["status.py"] = 1
        with pytest.raises(SystemExit) as e:
            self._main(close_mod, monkeypatch, "--project-dir", "/p")
        assert e.value.code == 1
        assert [s for s, _ in registro] == ["status.py"]  # export nunca se llamó
        assert "BLOQUEADO" in capsys.readouterr().err

    def test_gate_ok_encadena_export_con_flags_comunes(
        self, close_mod, monkeypatch, calls, capsys
    ):
        registro, _ = calls
        self._main(close_mod, monkeypatch, "--project-dir", "/p", "--spec", "001-guia")
        assert registro[0] == ("status.py", ["--project-dir", "/p", "--spec", "001-guia", "--gate"])
        assert registro[1] == ("export.py", ["--project-dir", "/p", "--spec", "001-guia"])
        assert "PDF generado" in capsys.readouterr().out

    def test_flags_de_export_pasan_tras_el_separador(self, close_mod, monkeypatch, calls):
        registro, _ = calls
        self._main(close_mod, monkeypatch, "--", "--title", "Mi guía")
        script, extra = registro[1]
        assert script == "export.py"
        assert extra == ["--project-dir", ".", "--title", "Mi guía"]

    def test_no_export_solo_evalua(self, close_mod, monkeypatch, calls, capsys):
        registro, _ = calls
        self._main(close_mod, monkeypatch, "--no-export")
        assert [s for s, _ in registro] == ["status.py"]
        assert "CERRABLE" in capsys.readouterr().out

    def test_no_export_enumera_deuda_declarada(
        self, close_mod, monkeypatch, calls, capsys, estudio_project
    ):
        registro, _ = calls
        findings = estudio_project / "specs/001-estudio/findings.md"
        findings.write_text(
            findings.read_text(encoding="utf-8").replace(
                "| F-1.3 | 1 | bajo | frase | aviso bajo | sugerencia | abierto | [] |",
                "| F-1.3 | 1 | bajo | frase | aviso bajo | sugerencia | aplazado | [] |",
            ),
            encoding="utf-8",
        )
        self._main(close_mod, monkeypatch, "--project-dir", str(estudio_project), "--no-export")
        assert [s for s, _ in registro] == ["status.py"]
        out = capsys.readouterr().out
        assert "Deuda declarada" in out
        assert "F-1.3" in out

    def test_export_fallido_propaga_el_codigo(self, close_mod, monkeypatch, calls, capsys):
        _, rcs = calls
        rcs["export.py"] = 3
        with pytest.raises(SystemExit) as e:
            self._main(close_mod, monkeypatch)
        assert e.value.code == 3
        assert "el gate pasó pero el export falló" in capsys.readouterr().err


class TestCliGateReal:
    """Gate real contra el fixture 003 vía CLI. Con --no-export jamás se
    invoca export.py, así que no hacen falta pandoc ni Chrome."""

    def _run(self, scripts_dir, proj: Path):
        return subprocess.run(
            [sys.executable, str(scripts_dir / "close.py"),
             "--project-dir", str(proj), "--no-export"],
            capture_output=True, text=True,
        )

    def test_proyecto_cerrable_sale_0(self, scripts_dir, fact_project):
        res = self._run(scripts_dir, fact_project())
        assert res.returncode == 0, res.stderr
        assert "CERRABLE" in res.stdout

    def test_gate_g4_bloqueado_sale_1(self, scripts_dir, fact_project):
        res = self._run(scripts_dir, fact_project(manifest="blocking"))
        assert res.returncode == 1
        assert "BLOQUEADO" in res.stderr
