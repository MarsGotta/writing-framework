#!/usr/bin/env python3
"""writeonmars close — cierre determinista: evalúa los gates y, si pasa, exporta.

Encadena `status.py --gate` y, solo si el proyecto cierra (sin críticos abiertos
y con las firmas humanas requeridas), lanza `export.py` para generar el PDF.
Si está bloqueado, imprime los blockers (vía status) y sale con exit 1 sin
exportar. Apto para correr sin agente (Paperclip) o como paso final del ciclo.

Uso:
    python3 close.py                       # gate + export con defaults
    python3 close.py --no-export           # solo evaluar el gate
    python3 close.py -- --title "Mi guía"  # pasa flags a export.py tras '--'
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, extra: list[str]) -> int:
    return subprocess.run([sys.executable, str(HERE / script), *extra]).returncode


def main() -> None:
    ap = argparse.ArgumentParser(description="Cierre determinista: gate + export.")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--spec", default=None)
    ap.add_argument("--no-export", action="store_true", help="Solo evaluar el gate de cierre.")
    ap.add_argument("export_args", nargs="*", help="Flags para export.py (tras '--').")
    args = ap.parse_args()

    common = ["--project-dir", args.project_dir]
    if args.spec:
        common += ["--spec", args.spec]

    print("== Gate de cierre ==")
    gate = run("status.py", common + ["--gate"])
    if gate != 0:
        print("\n[close] BLOQUEADO: no se exporta. Resuelve los blockers de arriba.", file=sys.stderr)
        sys.exit(1)

    if args.no_export:
        print("\n[close] CERRABLE. (--no-export: no se genera PDF.)")
        return

    print("\n== Export ==")
    rc = run("export.py", common + args.export_args)
    if rc != 0:
        print("\n[close] el gate pasó pero el export falló.", file=sys.stderr)
        sys.exit(rc)
    print("\n[close] OK: proyecto cerrado y PDF generado.")


if __name__ == "__main__":
    main()
