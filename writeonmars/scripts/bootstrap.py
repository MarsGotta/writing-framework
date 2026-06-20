#!/usr/bin/env python3
"""writeonmars bootstrap — instala lo que el preset no puede.

Un preset de Spec Kit registra plantillas y comandos, pero NO puede escribir la
constitución (`.specify/memory/`) ni el manifest del proyecto. Este script cubre
ese hueco en un solo paso. Córrelo UNA vez tras `specify preset add`.

Hace dos cosas:
  1. Copia la constitución editorial canónica a `.specify/memory/constitution.md`.
  2. Crea un `.writeonmars-manifest.json` inicial (matriz de firmas por defecto:
     TODAS las pasadas autónomas; el control humano es el PDF anotado al final).

Uso (desde la raíz del proyecto editorial):
    python3 .specify/presets/writeonmars/scripts/bootstrap.py
    python3 .../bootstrap.py --operator marcela.gotta --email tu@correo --force
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PRESET = Path(__file__).resolve().parent.parent  # .../presets/writeonmars
CONSTITUTION_VERSION = "1.2.0"
FRAMEWORK_VERSION = "0.1.0"


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[bootstrap] error: {msg}", file=sys.stderr)
    sys.exit(1)


def default_manifest(operator: str, email: str) -> dict:
    op = {"id": operator, "role": "author"}
    if email:
        op["email"] = email
    return {
        "framework_version": FRAMEWORK_VERSION,
        "constitution_version": CONSTITUTION_VERSION,
        "agent_target": "claude-code",
        "language_primary": "es",
        "skills": [
            {"name": "marcela-prose", "version": "2.0.0", "source": "bundled"},
            {"name": "technical-guide-design", "version": "1.0.0", "source": "bundled"},
        ],
        "research_mode": "byom",
        "signing_matrix": {
            "pasada_1_estructura": "autonomous",
            "pasada_2_utilidad": "autonomous",
            "pasada_3_naturalidad": "autonomous",
            "pasada_4_precision": "autonomous",
            "pasada_5_formato": "autonomous",
        },
        "human_operators": [op],
        "citation_contract_version": "1.0",
        "project_type": "editorial",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Bootstrap de un proyecto editorial Write.OnMars.")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--operator", default="marcela.gotta", help="ID del operador humano.")
    ap.add_argument("--email", default="", help="Email del operador (opcional).")
    ap.add_argument("--force", action="store_true", help="Sobrescribe constitución y manifest existentes.")
    args = ap.parse_args()

    proj = Path(args.project_dir).resolve()
    if not (proj / ".specify").is_dir():
        fail(f"{proj} no es un proyecto spec-kit (falta .specify/). Corre antes `specify init` y `specify preset add`.")

    # 1. Constitución
    src = PRESET / "memory" / "constitution.md"
    if not src.exists():
        fail(f"no encuentro la constitución bundled en {src}")
    dst = proj / ".specify" / "memory" / "constitution.md"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not args.force and "Write.OnMars Constitution" in dst.read_text(encoding="utf-8"):
        print(f"[bootstrap] constitución ya presente (v{CONSTITUTION_VERSION}); --force para sobrescribir")
    else:
        shutil.copyfile(src, dst)
        print(f"[bootstrap] constitución copiada → .specify/memory/constitution.md (v{CONSTITUTION_VERSION})")

    # 2. Manifest
    man = proj / ".writeonmars-manifest.json"
    if man.exists() and not args.force:
        print("[bootstrap] .writeonmars-manifest.json ya existe; --force para regenerar")
    else:
        man.write_text(json.dumps(default_manifest(args.operator, args.email), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[bootstrap] manifest creado → .writeonmars-manifest.json (operador: {args.operator})")

    print("[bootstrap] listo. El proyecto ya tiene constitución y manifest.")


if __name__ == "__main__":
    main()
