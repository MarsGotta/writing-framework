#!/usr/bin/env python3
"""writeonmars track — cambia la pista de ceremonia de un proyecto.

Único camino para mover un proyecto entre `corta` y `estandar` (escalar /
des-escalar) o auditar el invariante de pieza única (`--check`). Patrón
`dispose.py`: identidad humana desde git config, validación de legalidad y
escritura atómica del manifiesto. Ningún agente puede cambiar la pista: se
rechazan las identidades `*@agents.writeonmars.invalid`.

El escalado NO toca ningún archivo salvo el manifiesto. La conservación del
trabajo (brief, pieza como capítulo 1, findings, claims, pasadas) es emergente,
no una migración (data-model § 6): el temario degenerado ya era un temario y la
pieza ya era el capítulo 1.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import findings_lib  # noqa: E402


def die(message: str, code: int) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[track] error: {message}", file=sys.stderr)
    sys.exit(code)


def git_config(project: Path, key: str) -> str:
    """Idéntico a dispose.py: preferencia por el config del repo, con fallback
    al global. Vacío si no hay valor."""
    for cmd in (
        ["git", "-C", str(project), "config", key],
        ["git", "config", "--global", key],
    ):
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return ""


def human_identity(project: Path) -> tuple[str, str]:
    """Identidad humana auditable (idéntica a dispose.py:45). Sin git config
    user.name o con identidad de agente ⇒ exit 3: el cambio de pista es humano."""
    actor = git_config(project, "user.name")
    email = git_config(project, "user.email")
    if not actor:
        die("sin git config user.name; no hay identidad humana auditable", 3)
    if actor.endswith("@agents.writeonmars.invalid") or email.endswith("@agents.writeonmars.invalid"):
        die("la identidad git pertenece a un agente; el cambio de pista debe ser humano", 3)
    return actor, email


def out_of_piece_ordinals(project: Path) -> list[int]:
    """Ordinales >= 2 con chapters/NN-*.md en disco (rompen la pieza única).

    Reutiliza findings_lib.drafted_ordinals (misma resolución ordinal→fichero
    que status.py); no reimplementa el parser."""
    chapters_dir = project / "chapters"
    if not chapters_dir.is_dir():
        return []
    names = [p.name for p in sorted(chapters_dir.glob("*.md"))]
    return sorted(n for n in findings_lib.drafted_ordinals(names) if n >= 2)


def temario_rows(project: Path, spec_override: str | None) -> int:
    """Filas del temario del spec activo. Sin spec ⇒ 0 (nada que romper)."""
    try:
        spec_dir = findings_lib.newest_spec_dir(project, spec_override)
    except ValueError as exc:
        die(str(exc), 1)
    if spec_dir is None:
        return 0
    return findings_lib.count_temario(spec_dir)


def write_manifest_atomic(path: Path, manifest: dict) -> None:
    """Escritura atómica del manifiesto (tmp + os.replace, rollback ante
    excepción; patrón dispose.py:135). Preserva el orden de claves existente y
    el indent=2 con ensure_ascii=False (como bootstrap.py:319)."""
    original = path.read_bytes()
    tmp = path.with_name(f".{path.name}.tmp")
    text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    tmp.write_text(text, encoding="utf-8")
    try:
        os.replace(tmp, path)
    except Exception:
        path.write_bytes(original)
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
        raise


def load_manifest_or_die(project: Path) -> tuple[Path, dict]:
    manifest_path = project / ".writeonmars-manifest.json"
    try:
        manifest = findings_lib.load_manifest(project)
    except ValueError as exc:
        die(str(exc), 1)
    if manifest is None:
        die(f"falta {manifest_path}", 1)
    return manifest_path, manifest


def current_track_or_die(manifest: dict) -> str:
    try:
        return findings_lib.project_track(manifest)
    except ValueError as exc:
        die(str(exc), 1)


def do_change(project: Path, manifest_path: Path, manifest: dict, args, destino: str) -> None:
    """Escribe track + entrada en track_history de forma atómica y reporta."""
    origen = current_track_or_die(manifest)
    actor, email = human_identity(project)
    record = {
        "from": origen,
        "to": destino,
        "date": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "actor": actor,
    }
    if email:
        record["email"] = email

    manifest["track"] = destino
    manifest.setdefault("track_history", []).append(record)
    write_manifest_atomic(manifest_path, manifest)

    if args.json:
        print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    else:
        print(f"[track] {origen} → {destino} (actor: {actor})")


def do_escalar(project: Path, args) -> None:
    manifest_path, manifest = load_manifest_or_die(project)
    if current_track_or_die(manifest) != "corta":
        die("el proyecto ya está en pista estandar", 1)
    # --escalar es SIEMPRE legal desde corta: no comprueba nada del disco.
    do_change(project, manifest_path, manifest, args, "estandar")


def do_desescalar(project: Path, args) -> None:
    manifest_path, manifest = load_manifest_or_die(project)
    if current_track_or_die(manifest) != "estandar":
        die("el proyecto ya está en pista corta", 1)
    filas = temario_rows(project, args.spec)
    if filas > 1:
        die(f"el temario tiene {filas} filas; la pista corta exige pieza única", 1)
    fuera = out_of_piece_ordinals(project)
    if fuera:
        die("existen capítulos fuera de pieza única: " + ", ".join(str(n) for n in fuera), 1)
    do_change(project, manifest_path, manifest, args, "corta")


def do_check(project: Path, args) -> None:
    """Read-only: valida el invariante corta ⟺ (temario ≤ 1 fila ∧ sin
    capítulos con ordinal ≥ 2). No exige identidad humana."""
    _, manifest = load_manifest_or_die(project)
    track = current_track_or_die(manifest)
    filas = temario_rows(project, args.spec)
    fuera = out_of_piece_ordinals(project)

    if track == "corta":
        coherente = filas <= 1 and not fuera
    else:
        coherente = True  # estandar no tiene invariante de pieza única

    if args.json:
        print(json.dumps(
            {"track": track, "temario_filas": filas, "capitulos_fuera": fuera, "coherente": coherente},
            ensure_ascii=False, sort_keys=True,
        ))
        sys.exit(0 if coherente else 1)

    if track != "corta":
        print("[track] estandar: sin invariante de pieza única que verificar")
        sys.exit(0)
    if filas > 1:
        die(f"track: corta con temario de {filas} filas; corrige el temario o escala", 1)
    if fuera:
        die("track: corta con capítulos fuera de pieza única: " + ", ".join(str(n) for n in fuera), 1)
    n_caps = len(list((project / "chapters").glob("*.md"))) if (project / "chapters").is_dir() else 0
    print(
        f"[track] corta: coherente (temario {filas} fila{'s' if filas != 1 else ''}, "
        f"{n_caps} capítulo{'s' if n_caps != 1 else ''})"
    )
    sys.exit(0)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Cambia la pista de ceremonia del proyecto (escalar/des-escalar) o audita el invariante."
    )
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--escalar", action="store_true", help="corta → estandar (siempre legal desde corta)")
    group.add_argument("--desescalar", action="store_true", help="estandar → corta (solo con pieza única)")
    group.add_argument("--check", action="store_true", help="valida el invariante de pieza única (read-only)")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--spec", help="specs/<dir> concreto (default: el más reciente)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    project = Path(args.project_dir).resolve()
    if args.check:
        do_check(project, args)
    elif args.escalar:
        do_escalar(project, args)
    else:
        do_desescalar(project, args)


if __name__ == "__main__":
    main()
