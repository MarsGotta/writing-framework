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
from datetime import datetime, timezone
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


def default_manifest(
    operator: str, email: str, mode: str = "produccion", track: str = "estandar"
) -> dict:
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
        # La pista de ceremonia (constitución v1.7.0 § Pistas de ceremonia). Se
        # escribe SIEMPRE, también con "estandar": explícito es mejor que implícito
        # y el schema lo admite (ausencia = estandar).
        "track": track,
        # El sector lo fija `--sector` (o `/speckit-constitution`) a partir de las
        # bases en references/sectores/. null = adendas aún sin configurar.
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


def available_sectors() -> list[str]:
    """Slugs de sector disponibles: todos los `*.md` de references/sectores/ salvo
    el índice (`_index.md`). El comando de constitución usa el mismo criterio."""
    sectores = PRESET / "references" / "sectores"
    if not sectores.is_dir():
        return []
    return sorted(p.stem for p in sectores.glob("*.md") if p.stem != "_index")


def extract_sector_name(sector_file: Path, slug: str) -> str:
    """Nombre legible del sector: el `# Sector: <Nombre>` de la cabecera. Si no
    aparece, cae al slug (nunca deja el bloque de adendas sin sector)."""
    text = sector_file.read_text(encoding="utf-8")
    m = re.search(r"^#\s+Sector:\s*(.+?)\s*$", text, re.MULTILINE)
    return m.group(1).strip() if m else slug


def extract_registro(sector_file: Path) -> "str | None":
    """Slug del registro por defecto del sector: el primer texto entre backticks
    bajo el encabezado `## Registro por defecto`. Devuelve None si no aparece
    (registro es campo opcional; el bloque lo declara 'sin registro declarado')."""
    text = sector_file.read_text(encoding="utf-8")
    m = re.search(r"^##\s+Registro por defecto\s*$", text, re.MULTILINE)
    if not m:
        return None
    bt = re.search(r"`([^`]+)`", text[m.end():])
    return bt.group(1).strip() if bt else None


def build_adendas_block(
    sector_slug: str, sector_name: str, registro: "str | None", nucleo_version: str, fecha: str
) -> str:
    """Bloque de adendas POR REFERENCIA (research.md § R2). No destila prosa:
    declara sector, registro, base aplicada y núcleo, y remite a la base del
    sector. El encabezado `### Tono calibrado` es obligatorio (sin él,
    speckit.specify se atasca en pista corta)."""
    if registro:
        registro_line = (
            f"**Registro (capa 2)**: `{registro}` · Base aplicada:\n"
            f"`references/registros/{registro}/SKILL.md`"
        )
        registro_ref = f"el registro `{registro}`"
    else:
        registro_line = "**Registro (capa 2)**: sin registro declarado"
        registro_ref = "el registro por defecto del sector (sin registro declarado)"
    return (
        f"{ADENDAS_MARKER}\n"
        "\n"
        "## Adendas del proyecto\n"
        "\n"
        f"**Sector**: {sector_name} · **Base aplicada**: `references/sectores/{sector_slug}.md`\n"
        f"{registro_line}\n"
        f"**Núcleo vigente**: Write.OnMars Constitution v{nucleo_version}\n"
        f"**Última edición de adendas**: {fecha}\n"
        "\n"
        "**Adendas aplicadas POR REFERENCIA.** Este proyecto adopta íntegros los valores\n"
        "por defecto de la base del sector (tono calibrado, anglicismos admitidos,\n"
        "matices léxicos, relajaciones estructurales, contrato terminológico inicial).\n"
        f"Las pasadas de revisión cargan `references/sectores/{sector_slug}.md` directamente.\n"
        "\n"
        "### Tono calibrado\n"
        "\n"
        "**Por referencia**: el tono de esta guía es el de la sección\n"
        f"`## Tono por defecto` de `references/sectores/{sector_slug}.md`, matizado por la\n"
        "persona gramatical de su sección `## Persona gramatical y registro`. El marco\n"
        f"general lo pone {registro_ref} (capa 2 de la pirámide de prosa).\n"
        "\n"
        "Quien necesite el tono —el brief (`/speckit-specify`, campo 5, que lo refleja\n"
        "como eco) y la pasada de naturalidad— lo lee de ahí. Para fijarlo literalmente\n"
        "aquí, corre `/speckit-constitution`.\n"
        "\n"
        "---\n"
        "\n"
        "Para calibrar cualquiera de esos valores a mano, corre `/speckit-constitution`:\n"
        "reescribe este bloque con las respuestas del cuestionario, sin tocar el núcleo.\n"
    )


def materialize_adendas(dst: Path, slug: str, sector_file: Path, registro: "str | None") -> None:
    """Añade el bloque de adendas por referencia al final de la constitución del
    proyecto. Si el centinela ya existe, NO reescribe (respeta adendas calibradas
    a mano) y solo avisa."""
    current = dst.read_text(encoding="utf-8")
    if ADENDAS_MARKER in current:
        print(
            f"[bootstrap] aviso: la constitución del proyecto ya trae el centinela "
            f"{ADENDAS_MARKER}; conservo las adendas existentes (usa /speckit-constitution "
            "para recalibrar a mano)"
        )
        return
    sector_name = extract_sector_name(sector_file, slug)
    fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    block = build_adendas_block(slug, sector_name, registro, CONSTITUTION_VERSION, fecha)
    dst.write_text(current.rstrip() + "\n\n" + block, encoding="utf-8")
    detalle = f"registro: {registro}" if registro else "sin registro declarado"
    print(
        f"[bootstrap] adendas del sector '{slug}' aplicadas POR REFERENCIA "
        f"({detalle}) → .specify/memory/constitution.md"
    )


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
    ap.add_argument(
        "--track",
        default=os.environ.get("WRITEONMARS_TRACK", "estandar"),
        choices=["estandar", "corta"],
        help="Pista de ceremonia: estandar (default) o corta.",
    )
    ap.add_argument(
        "--sector",
        default=os.environ.get("WRITEONMARS_SECTOR"),
        help="Slug del sector (references/sectores/<slug>.md). Fija adendas por referencia.",
    )
    ap.add_argument("--force", action="store_true", help="Sobrescribe constitución y manifest existentes.")
    args = ap.parse_args()

    # argparse no valida `choices` sobre el default: un WRITEONMARS_MODE con
    # typo llegaría aquí intacto y acabaría escrito en el manifest.
    if args.mode not in ("produccion", "estudio"):
        fail(f"mode inválido: {args.mode!r} (esperado produccion|estudio; revisa WRITEONMARS_MODE)")

    # Mismo bug para --track: un WRITEONMARS_TRACK con typo no lo caza argparse
    # (no valida el default). Sin este guard acabaría escrito en el manifest.
    if args.track not in ("estandar", "corta"):
        fail(f"track inválido: {args.track!r} (esperado estandar|corta; revisa WRITEONMARS_TRACK)")

    proj = Path(args.project_dir).resolve()
    if not (proj / ".specify").is_dir():
        fail(f"{proj} no es un proyecto spec-kit (falta .specify/). Corre antes `specify init` y `specify preset add`.")

    # Validación temprana del sector: si el slug no existe, fallar ANTES de tocar
    # el disco (mismo criterio que los guards de --mode/--track). Registro se
    # extrae aquí para usarlo tanto en el manifest como en las adendas.
    sector_file = None
    registro = None
    if args.sector:
        sector_file = PRESET / "references" / "sectores" / f"{args.sector}.md"
        if not sector_file.is_file():
            disponibles = available_sectors()
            fail(
                f"sector inválido: {args.sector!r}. "
                f"Sectores disponibles: {', '.join(disponibles) or '(ninguno)'}"
            )
        registro = extract_registro(sector_file)

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

    # 1b. Adendas por referencia (solo con --sector): se materializan tras el
    # núcleo, empezando por el centinela. El centinela preexistente se respeta.
    if args.sector:
        materialize_adendas(dst, args.sector, sector_file, registro)

    # 2. Manifest
    man = proj / ".writeonmars-manifest.json"
    if man.exists() and not args.force:
        print("[bootstrap] .writeonmars-manifest.json ya existe; --force para regenerar")
    else:
        manifest = default_manifest(args.operator, args.email, args.mode, args.track)
        if args.sector:
            manifest["sector"] = args.sector
            if registro:
                manifest["registro"] = registro
        validate_manifest(manifest)
        man.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[bootstrap] manifest creado → .writeonmars-manifest.json (operador: {args.operator})")

    print("[bootstrap] listo. El proyecto ya tiene constitución y manifest.")


if __name__ == "__main__":
    main()
