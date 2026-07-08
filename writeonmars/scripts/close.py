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
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from findings_lib import parse_findings  # noqa: E402


def run(script: str, extra: list[str]) -> int:
    return subprocess.run([sys.executable, str(HERE / script), *extra]).returncode


def _spec_dir(project: Path, override: str | None) -> Path | None:
    specs = project / "specs"
    if override:
        cand = specs / override if not Path(override).is_absolute() else Path(override)
        return cand if cand.is_dir() else None
    if not specs.is_dir():
        return None
    dirs = sorted(d for d in specs.iterdir() if d.is_dir() and (d / "spec.md").exists())
    return dirs[-1] if dirs else None


def deferred_debt(project: Path, spec: str | None) -> list[dict]:
    spec_dir = _spec_dir(project, spec)
    if spec_dir is None:
        return []
    out = []
    for block in parse_findings(spec_dir / "findings.md"):
        for finding in block["hallazgos"]:
            if finding.get("estado") == "aplazado":
                out.append({
                    "id": finding.get("id", ""),
                    "severidad": finding.get("severidad", ""),
                    "capitulo": finding.get("capitulo", ""),
                })
    return out


def print_deferred_debt(project: Path, spec: str | None) -> None:
    debt = deferred_debt(project, spec)
    if not debt:
        return
    print("\n== Deuda declarada ==")
    for item in debt:
        print(f"- {item['id']} · {item['severidad']} · capítulo {item['capitulo']}")


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
    print_deferred_debt(Path(args.project_dir).resolve(), args.spec)

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
