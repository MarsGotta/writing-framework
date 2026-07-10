"""Shared parser for Write.OnMars findings.md blocks.

The scripts in this directory are intentionally plain files, not a Python
package. This helper stays stdlib-only so status.py and dispose.py can share
the markdown table parser without adding runtime dependencies.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterator

# Mapa canónico disposición humana → estado del hallazgo (pass-output v1.2).
# dispose.py escribe con él y status.py valida con su inverso: una sola fuente.
STATE_BY_DISPOSITION = {
    "aceptado": "resuelto",
    "rechazado": "desviacion_justificada",
    "aplazado": "aplazado",
}
DISPOSITION_BY_STATE = {state: disp for disp, state in STATE_BY_DISPOSITION.items()}


def newest_spec_dir(project: Path, override: str | None = None) -> Path | None:
    """Resolución canónica del spec activo: el MÁS RECIENTE (orden lexicográfico)
    de specs/*/ con spec.md — la regla de status.py, compartida por todos los
    scripts. `override` inexistente es error (ValueError), no None silencioso."""
    specs = project / "specs"
    if override:
        cand = (specs / override) if not Path(override).is_absolute() else Path(override)
        if not cand.is_dir():
            raise ValueError(f"no existe el spec {cand}")
        return cand
    if not specs.is_dir():
        return None
    dirs = sorted(d for d in specs.iterdir() if d.is_dir() and (d / "spec.md").exists())
    return dirs[-1] if dirs else None


def load_manifest(project: Path) -> dict | None:
    """Manifiesto del proyecto o None si no existe. JSON inválido → ValueError."""
    p = project / ".writeonmars-manifest.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f".writeonmars-manifest.json no es JSON válido: {e}") from e


def project_mode(manifest: dict | None) -> str:
    """Modo del proyecto: ausencia/None = produccion; valor desconocido → ValueError."""
    if manifest is None:
        return "produccion"
    mode = manifest.get("mode", "produccion")
    if mode is None:
        return "produccion"
    if mode not in {"produccion", "estudio"}:
        raise ValueError("manifest.mode debe ser 'produccion' o 'estudio'")
    return mode


def project_track(manifest: dict | None) -> str:
    """Pista del proyecto: ausencia/None = estandar; valor desconocido → ValueError.

    Gemelo exacto de project_mode. Todo consumidor (status.py, export.py,
    track.py) usa este accesor; ningún script lee manifest['track'] directamente.
    """
    if manifest is None:
        return "estandar"
    track = manifest.get("track", "estandar")
    if track is None:
        return "estandar"
    if track not in {"estandar", "corta"}:
        raise ValueError("manifest.track debe ser 'estandar' o 'corta'")
    return track


def count_temario(spec_dir: Path) -> int:
    """Cuenta los capítulos declarados en la tabla Temario de plan.md."""
    plan = spec_dir / "plan.md"
    if not plan.exists():
        return 0
    n, in_temario = 0, False
    for line in plan.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("## ") and "Temario" in s:
            in_temario = True
            continue
        if in_temario and s.startswith("## ") and "Temario" not in s:
            break
        if in_temario and re.match(r"\|\s*\d+\s*\|", s):
            n += 1
    return n


def drafted_ordinals(chapters: list[str]) -> set[int]:
    """Ordinales con fichero chapters/NN-*.md presente. Mapea ordinal→fichero por
    el prefijo numérico del nombre (p. ej. '03-intro.md' → 3)."""
    out: set[int] = set()
    for name in chapters:
        m = re.match(r"\s*(\d+)", name)
        if m:
            out.add(int(m.group(1)))
    return out


def parse_findings(findings_md: Path) -> list[dict]:
    """Return pass blocks with signature metadata, covered chapters and findings."""
    if not findings_md.exists():
        return []
    text = findings_md.read_text(encoding="utf-8")
    blocks = []
    headers = list(re.finditer(r"^##\s+Pasada\s+(\d+)\s*[—–-]\s*(.+)$", text, re.M))
    for i, h in enumerate(headers):
        start = h.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[start:end]
        num = int(h.group(1))
        name = h.group(2).strip()
        estado = _field(body, r"Estado pasada")
        firma_tipo = _firma_tipo(body)
        firma_actor = _firma_actor(body)
        caps = _field(body, r"Capítulos cubiertos")
        hallazgos = _parse_findings_table(body)
        blocks.append(
            {
                "num": num,
                "name": name,
                "estado": (estado or "—").lower(),
                "firma": (firma_tipo or "—").lower(),
                "actor": (firma_actor or "").lower(),
                "capitulos": caps or "—",
                "hallazgos": hallazgos,
                "huellas": _parse_huellas(body),
            }
        )
    return blocks


def iter_finding_rows(text: str) -> Iterator[tuple[int, str, list[str]]]:
    """Yield (line_index, raw_line, cells) for machine-readable finding rows."""
    for idx, line in enumerate(text.splitlines()):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 8 or not cells[0].startswith("F-"):
            continue
        yield idx, line, cells


def _field(body: str, label: str) -> str | None:
    m = re.search(rf"\*\*{label}\*\*\s*:\s*(.+)", body)
    return m.group(1).strip() if m else None


def _firma_tipo(body: str) -> str | None:
    m = re.search(r"\*\*Firma\*\*.*?tipo\s*:\s*(\w+)", body, re.S)
    return m.group(1) if m else None


def _firma_actor(body: str) -> str | None:
    m = re.search(r"\*\*Firma\*\*.*?actor\s*:\s*([^\n]+)", body, re.S)
    return m.group(1).strip() if m else None


def _parse_huellas(body: str) -> dict[str, str]:
    m = re.search(r"<!--\s*huellas:\s*(\{.*?\})\s*-->", body, re.S)
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}


def _parse_findings_table(body: str) -> list[dict]:
    out = []
    for _, _, cells in iter_finding_rows(body):
        item = {
            "id": cells[0],
            "capitulo": cells[1],
            "severidad": cells[2].lower(),
            "estado": cells[6].lower(),
        }
        if len(cells) > 8:
            item["decision_humana"] = cells[8]
        out.append(item)
    return out
