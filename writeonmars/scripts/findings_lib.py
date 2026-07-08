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
