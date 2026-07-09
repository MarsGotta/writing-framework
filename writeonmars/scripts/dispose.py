#!/usr/bin/env python3
"""writeonmars dispose — registra disposiciones humanas en modo estudio."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import findings_lib  # noqa: E402
from findings_lib import (  # noqa: E402
    DISPOSITION_BY_STATE,
    STATE_BY_DISPOSITION,
    iter_finding_rows,
)

FINDING_ID_RE = re.compile(r"^F-[0-9]+\.[0-9]+$")


def die(message: str, code: int) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[dispose] error: {message}", file=sys.stderr)
    sys.exit(code)


def git_config(project: Path, key: str) -> str:
    for cmd in (
        ["git", "-C", str(project), "config", key],
        ["git", "config", "--global", key],
    ):
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    return ""


def human_identity(project: Path) -> tuple[str, str]:
    actor = git_config(project, "user.name")
    email = git_config(project, "user.email")
    if not actor:
        die("sin git config user.name; no hay identidad humana auditable", 3)
    if actor.endswith("@agents.writeonmars.invalid") or email.endswith("@agents.writeonmars.invalid"):
        die("la identidad git pertenece a un agente; la disposición debe ser humana", 3)
    return actor, email


def prior_dispositions(path: Path) -> dict[str, set[str]]:
    """Disposiciones ya registradas, por finding_id. Línea malformada = error
    duro: este script está a punto de anexar al mismo archivo."""
    records: dict[str, set[str]] = {}
    if not path.exists():
        return records
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            die(f"{path}:{idx} no es DispositionRecord válido: {exc}", 1)
        fid = data.get("finding_id")
        disp = data.get("disposicion")
        if isinstance(fid, str) and isinstance(disp, str):
            records.setdefault(fid, set()).add(disp)
    return records


def update_findings(
    text: str,
    finding_id: str,
    disposition: str,
    motivo: str | None,
    recorded: dict[str, set[str]],
) -> tuple[str, str]:
    """Edición quirúrgica: solo la celda `estado` (y `decision_humana` en
    rechazo) de la fila del hallazgo. El resto del archivo — CRLF, padding de
    otras celdas, líneas vecinas — conserva sus bytes."""
    lines = text.splitlines(keepends=True)
    target_idx = target_cells = None
    for idx, _, cells in iter_finding_rows(text):
        if cells[0] == finding_id:
            target_idx, target_cells = idx, cells
            break
    if target_idx is None or target_cells is None:
        die(f"hallazgo inexistente: {finding_id}", 1)
    current_state = target_cells[6]
    if current_state not in {"abierto", "aplazado"}:
        # Estado no-disponible CON registro humano compatible = ya dispuesto.
        # SIN registro compatible = inconsistencia (p. ej. un agente editó la
        # tabla): status.py lo cuenta como pendiente, así que la humana debe
        # poder regularizarlo aquí — sin esta vía habría livelock.
        expected = DISPOSITION_BY_STATE.get(current_state)
        if expected and expected in recorded.get(finding_id, set()):
            die(f"{finding_id} no admite disposición desde estado {current_state}", 1)
        print(
            f"[dispose] aviso: {finding_id} está '{current_state}' sin disposición "
            "humana registrada; se trata como abierto y se regulariza",
            file=sys.stderr,
        )
    if current_state == "aplazado" and disposition == "aplazado":
        die(f"{finding_id} ya está aplazado", 1)
    next_state = STATE_BY_DISPOSITION[disposition]

    # El raw sale de la lista con keepends (iter_finding_rows itera sin saltos):
    # así el salto de línea original — \n o \r\n — se conserva al reconstruir.
    target_raw = lines[target_idx]
    body = target_raw.rstrip("\r\n")
    ending = target_raw[len(body):]
    parts = body.split("|")
    # parts[0] = prefijo antes del primer pipe; la celda k es parts[k+1].
    parts[7] = f" {next_state} "
    if disposition == "rechazado" and motivo:
        safe = motivo.replace("|", "/")
        if len(target_cells) > 8:
            parts[9] = f" {safe} "
        else:
            parts.insert(len(parts) - 1, f" {safe} ")
    lines[target_idx] = "|".join(parts) + ending
    return "".join(lines), current_state


def read_preserving(path: Path) -> str:
    """Lee sin traducción de saltos de línea (read_text convierte CRLF→LF): el
    contrato exige preservar los bytes del archivo fuera de la celda tocada."""
    return path.read_bytes().decode("utf-8")


def write_pair_atomic(findings: Path, findings_text: str, dispositions: Path, dispositions_text: str) -> None:
    original_findings = read_preserving(findings)
    findings_tmp = findings.with_name(f".{findings.name}.tmp")
    dispositions_tmp = dispositions.with_name(f".{dispositions.name}.tmp")
    findings_tmp.write_text(findings_text, encoding="utf-8", newline="")
    dispositions_tmp.write_text(dispositions_text, encoding="utf-8")
    try:
        os.replace(findings_tmp, findings)
        os.replace(dispositions_tmp, dispositions)
    except Exception:
        findings.write_text(original_findings, encoding="utf-8", newline="")
        for tmp in (findings_tmp, dispositions_tmp):
            try:
                tmp.unlink()
            except FileNotFoundError:
                pass
        raise


def main() -> None:
    ap = argparse.ArgumentParser(description="Registra una disposición humana sobre un hallazgo.")
    ap.add_argument("finding_id")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--aceptar", action="store_true")
    group.add_argument("--rechazar", action="store_true")
    group.add_argument("--aplazar", action="store_true")
    ap.add_argument("--motivo")
    ap.add_argument("--nota")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--spec", help="specs/<dir> concreto (default: el más reciente)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not FINDING_ID_RE.match(args.finding_id):
        die(f"finding_id inválido: {args.finding_id} (formato F-N.M)", 2)
    if args.rechazar and not args.motivo:
        die("--rechazar requiere --motivo", 2)
    if args.rechazar and len(args.motivo.strip()) < 3:
        die("--motivo demasiado corto (mínimo 3 caracteres)", 2)

    project = Path(args.project_dir).resolve()
    try:
        manifest = findings_lib.load_manifest(project)
        mode = findings_lib.project_mode(manifest)
    except ValueError as exc:
        die(str(exc), 1)
    if manifest is None:
        die(f"falta {project / '.writeonmars-manifest.json'}", 1)
    if mode != "estudio":
        die("el ciclo de disposición solo aplica en mode=estudio", 1)
    try:
        spec_dir = findings_lib.newest_spec_dir(project, args.spec)
    except ValueError as exc:
        die(str(exc), 1)
    if spec_dir is None:
        die(f"ningún specs/*/spec.md bajo {project / 'specs'}", 1)
    findings = spec_dir / "findings.md"
    if not findings.exists():
        die(f"falta {findings}", 1)

    disposition = "aceptado" if args.aceptar else ("rechazado" if args.rechazar else "aplazado")
    actor, email = human_identity(project)
    record = {
        "v": 1,
        "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "finding_id": args.finding_id,
        "disposicion": disposition,
        "actor": actor,
    }
    if email:
        record["email"] = email
    if args.motivo:
        record["motivo"] = args.motivo
    if args.nota:
        record["nota"] = args.nota

    disposiciones = spec_dir / "disposiciones.jsonl"
    recorded = prior_dispositions(disposiciones)
    original = read_preserving(findings)
    updated, _ = update_findings(original, args.finding_id, disposition, args.motivo, recorded)
    existing = disposiciones.read_text(encoding="utf-8") if disposiciones.exists() else ""
    next_line = json.dumps(record, ensure_ascii=False, sort_keys=True)

    next_dispositions = existing + ("" if existing.endswith("\n") or not existing else "\n") + next_line + "\n"
    write_pair_atomic(findings, updated, disposiciones, next_dispositions)

    if args.json:
        print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    else:
        print(f"[dispose] {args.finding_id} → {STATE_BY_DISPOSITION[disposition]}")


if __name__ == "__main__":
    main()
