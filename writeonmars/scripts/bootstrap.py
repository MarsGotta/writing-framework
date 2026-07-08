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
import os
import re
import shutil
import sys
from pathlib import Path

PRESET = Path(__file__).resolve().parent.parent  # .../presets/writeonmars
FRAMEWORK_VERSION = "0.1.0"
# Centinela que separa el núcleo de la capa por guía. Es una marca única que NO
# aparece en el núcleo (a diferencia del título "## Adendas del proyecto", que el
# núcleo menciona inline). `/speckit-constitution` escribe las adendas a partir de
# esta línea, tomándola de templates/adendas-template.md.
ADENDAS_MARKER = "<!-- WRITEONMARS:ADENDAS -->"


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[bootstrap] error: {msg}", file=sys.stderr)
    sys.exit(1)


def read_constitution_version() -> str:
    """Lee la versión desde memory/constitution.md (pie: `**Version**: X.Y.Z`).

    La versión se deriva del fichero, nunca de una constante: un hardcode aquí ya
    se desincronizó dos veces (1.3.0 y 1.4.0 quedaron fósiles tras sendos bumps).
    """
    src = PRESET / "memory" / "constitution.md"
    try:
        text = src.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"no puedo leer la constitución bundled en {src}: {exc}")
    m = re.search(r"^\*\*Version\*\*:\s*(\d+\.\d+\.\d+)", text, re.MULTILINE)
    if not m:
        fail(f"no encuentro la marca '**Version**: X.Y.Z' al pie de {src}")
    return m.group(1)


CONSTITUTION_VERSION = read_constitution_version()


def default_manifest(operator: str, email: str, mode: str = "produccion") -> dict:
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
        "mode": mode,
        # El sector lo fija `/speckit-constitution` (primer paso del ciclo) a partir
        # de las bases en references/sectores/. null = adendas aún sin configurar.
        "sector": None,
    }


def validate_manifest(manifest: dict) -> None:
    """Valida el manifest contra contracts/manifest-schema.json antes de escribirlo.

    Con `jsonschema` instalado la validación es completa; sin él se comprueban
    las claves requeridas del schema (suficiente para cazar un manifest roto).
    """
    schema_path = PRESET / "contracts" / "manifest-schema.json"
    if not schema_path.exists():
        print(f"[bootstrap] aviso: no encuentro {schema_path.name}; omito la validación del manifest")
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        import jsonschema  # type: ignore
    except ImportError:
        missing = [k for k in schema.get("required", []) if k not in manifest]
        if missing:
            fail(f"el manifest generado no tiene claves requeridas: {', '.join(missing)}")
        return
    try:
        jsonschema.validate(instance=manifest, schema=schema)
    except jsonschema.ValidationError as exc:
        fail(f"el manifest generado no valida contra el schema: {exc.message}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Bootstrap de un proyecto editorial Write.OnMars.")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--operator", default="marcela.gotta", help="ID del operador humano.")
    ap.add_argument("--email", default="", help="Email del operador (opcional).")
    ap.add_argument(
        "--mode",
        default=os.environ.get("WRITEONMARS_MODE", "produccion"),
        choices=["produccion", "estudio"],
        help="Modo del proyecto: produccion (default) o estudio.",
    )
    ap.add_argument("--force", action="store_true", help="Sobrescribe constitución y manifest existentes.")
    args = ap.parse_args()

    # argparse no valida `choices` sobre el default: un WRITEONMARS_MODE con
    # typo llegaría aquí intacto y acabaría escrito en el manifest.
    if args.mode not in ("produccion", "estudio"):
        fail(f"mode inválido: {args.mode!r} (esperado produccion|estudio; revisa WRITEONMARS_MODE)")

    proj = Path(args.project_dir).resolve()
    if not (proj / ".specify").is_dir():
        fail(f"{proj} no es un proyecto spec-kit (falta .specify/). Corre antes `specify init` y `specify preset add`.")

    # 1. Constitución
    src = PRESET / "memory" / "constitution.md"
    if not src.exists():
        fail(f"no encuentro la constitución bundled en {src}")
    dst = proj / ".specify" / "memory" / "constitution.md"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copyfile(src, dst)
        print(f"[bootstrap] núcleo copiado → .specify/memory/constitution.md (v{CONSTITUTION_VERSION})")
    elif not args.force:
        print(f"[bootstrap] constitución ya presente (v{CONSTITUTION_VERSION}); --force para re-sellar el núcleo")
    else:
        # --force: re-sella el núcleo desde el preset, PRESERVANDO las adendas de
        # la guía (todo lo que vive desde `## Adendas del proyecto` hacia abajo).
        current = dst.read_text(encoding="utf-8")
        idx = current.find(ADENDAS_MARKER)
        if idx != -1:
            adendas = current[idx:]
            dst.write_text(src.read_text(encoding="utf-8").rstrip() + "\n\n" + adendas, encoding="utf-8")
            print(f"[bootstrap] núcleo re-sellado (v{CONSTITUTION_VERSION}); adendas del proyecto preservadas")
        else:
            shutil.copyfile(src, dst)
            print(f"[bootstrap] núcleo sobrescrito (v{CONSTITUTION_VERSION}); no había adendas que preservar")

    # 2. Manifest
    man = proj / ".writeonmars-manifest.json"
    if man.exists() and not args.force:
        print("[bootstrap] .writeonmars-manifest.json ya existe; --force para regenerar")
    else:
        manifest = default_manifest(args.operator, args.email, args.mode)
        validate_manifest(manifest)
        man.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[bootstrap] manifest creado → .writeonmars-manifest.json (operador: {args.operator})")

    print("[bootstrap] listo. El proyecto ya tiene constitución y manifest.")


if __name__ == "__main__":
    main()
