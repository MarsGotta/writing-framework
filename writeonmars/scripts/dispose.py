#!/usr/bin/env python3
"""writeonmars dispose — registra disposiciones humanas en modo estudio."""

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

from findings_lib import iter_finding_rows  # noqa: E402

STATE_BY_DISPOSITION = {
    "aceptado": "resuelto",
    "rechazado": "desviacion_justificada",
    "aplazado": "aplazado",
}


def die(message: str, code: int) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[dispose] error: {message}", file=sys.stderr)
    sys.exit(code)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"falta {path}", 1)
    except json.JSONDecodeError as exc:
        die(f"{path} no es JSON válido: {exc}", 1)


def project_mode(manifest: dict) -> str:
    mode = manifest.get("mode", "produccion")
    if mode is None:
        return "produccion"
    if mode not in {"produccion", "estudio"}:
        die("manifest.mode debe ser 'produccion' o 'estudio'", 1)
    return mode


def first_spec_dir(project: Path) -> Path:
    specs = project / "specs"
    if not specs.is_dir():
        die(f"no existe {specs}", 1)
    dirs = sorted(d for d in specs.iterdir() if d.is_dir() and (d / "spec.md").exists())
    if not dirs:
        die(f"ningún specs/*/spec.md bajo {specs}", 1)
    return dirs[0]


def git_config(project: Path, key: str) -> str:
    for cmd in (
        ["git", "-C", str(project), "config", key],
        ["git", "config", "--global", key],
    ):
        result = subprocess.run(cmd, capture_output=True, text=True)
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


def validate_record(record: dict) -> None:
    required = {"v", "ts", "finding_id", "disposicion", "actor"}
    missing = required - set(record)
    if missing:
        die(f"DispositionRecord incompleto: faltan {', '.join(sorted(missing))}", 5)
    if record["v"] != 1:
        die("DispositionRecord.v debe ser 1", 5)
    if record["disposicion"] not in STATE_BY_DISPOSITION:
        die("DispositionRecord.disposicion inválida", 5)
    if record["disposicion"] == "rechazado" and not record.get("motivo"):
        die("rechazo sin motivo", 2)


def update_findings(text: str, finding_id: str, disposition: str, motivo: str | None) -> tuple[str, str]:
    lines = text.splitlines()
    target_line = None
    target_cells = None
    for idx, _, cells in iter_finding_rows(text):
        if cells[0] == finding_id:
            target_line = idx
            target_cells = cells
            break
    if target_line is None or target_cells is None:
        die(f"hallazgo inexistente: {finding_id}", 1)
    current_state = target_cells[6]
    if current_state not in {"abierto", "aplazado"}:
        die(f"{finding_id} no admite disposición desde estado {current_state}", 1)
    if current_state == "aplazado" and disposition == "aplazado":
        die(f"{finding_id} ya está aplazado", 1)
    next_state = STATE_BY_DISPOSITION[disposition]
    target_cells[6] = next_state
    if disposition == "rechazado" and motivo and len(target_cells) > 8:
        target_cells[8] = motivo
    lines[target_line] = "| " + " | ".join(target_cells) + " |"
    return "\n".join(lines) + ("\n" if text.endswith("\n") else ""), current_state


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def write_pair_atomic(findings: Path, findings_text: str, dispositions: Path, dispositions_text: str) -> None:
    original_findings = findings.read_text(encoding="utf-8")
    findings_tmp = findings.with_name(f".{findings.name}.tmp")
    dispositions_tmp = dispositions.with_name(f".{dispositions.name}.tmp")
    findings_tmp.write_text(findings_text, encoding="utf-8")
    dispositions_tmp.write_text(dispositions_text, encoding="utf-8")
    try:
        os.replace(findings_tmp, findings)
        os.replace(dispositions_tmp, dispositions)
    except Exception:
        findings.write_text(original_findings, encoding="utf-8")
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
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.rechazar and not args.motivo:
        die("--rechazar requiere --motivo", 2)

    project = Path(args.project_dir).resolve()
    manifest = load_json(project / ".writeonmars-manifest.json")
    if project_mode(manifest) != "estudio":
        die("el ciclo de disposición solo aplica en mode=estudio", 1)
    spec_dir = first_spec_dir(project)
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
    validate_record(record)

    original = findings.read_text(encoding="utf-8")
    updated, _ = update_findings(original, args.finding_id, disposition, args.motivo)
    disposiciones = spec_dir / "disposiciones.jsonl"
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
