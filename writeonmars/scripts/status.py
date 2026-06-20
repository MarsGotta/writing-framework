#!/usr/bin/env python3
"""writeonmars status — dashboard determinista de un proyecto editorial.

Lee `specs/<###-feature>/findings.md` (esquema pass-output v1.0) y el
`.writeonmars-manifest.json`, y muestra en una pantalla: estado de cada pasada,
firmas, hallazgos por severidad y los tres gates de cierre (críticos abiertos +
firmas humanas faltantes + completitud del temario). Sustituye `wom status` y
`wom close`. Read-only.

Uso:
    python3 status.py                 # desde la raíz del proyecto
    python3 status.py --gate          # además, exit 1 si el proyecto NO cierra
    python3 status.py --project-dir /ruta --spec 001-mi-guia
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PASS_KEY = {
    1: "pasada_1_estructura",
    2: "pasada_2_utilidad",
    3: "pasada_3_naturalidad",
    4: "pasada_4_precision",
    5: "pasada_5_formato",
}


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[status] error: {msg}", file=sys.stderr)
    sys.exit(2)


def newest_spec_dir(project: Path, override: str | None) -> Path:
    specs = project / "specs"
    if override:
        cand = (specs / override) if not Path(override).is_absolute() else Path(override)
        if not cand.is_dir():
            fail(f"no existe el spec {cand}")
        return cand
    if not specs.is_dir():
        fail(f"no existe {specs}")
    dirs = sorted(d for d in specs.iterdir() if d.is_dir() and (d / "spec.md").exists())
    if not dirs:
        fail(f"ningún specs/*/spec.md bajo {specs}")
    return dirs[-1]


def parse_findings(findings_md: Path) -> list[dict]:
    """Lista de bloques de pasada con su estado, firma y hallazgos."""
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
            }
        )
    return blocks


def _field(body: str, label: str) -> str | None:
    m = re.search(rf"\*\*{label}\*\*\s*:\s*(.+)", body)
    return m.group(1).strip() if m else None


def _firma_tipo(body: str) -> str | None:
    # Formato: **Firma**:\n  - tipo: autonomous|human
    m = re.search(r"\*\*Firma\*\*.*?tipo\s*:\s*(\w+)", body, re.S)
    return m.group(1) if m else None


def _firma_actor(body: str) -> str | None:
    m = re.search(r"\*\*Firma\*\*.*?actor\s*:\s*([^\n]+)", body, re.S)
    return m.group(1).strip() if m else None


def _parse_findings_table(body: str) -> list[dict]:
    out = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 8 or not cells[0].startswith("F-"):
            continue
        out.append(
            {
                "id": cells[0],
                "capitulo": cells[1],
                "severidad": cells[2].lower(),
                "estado": cells[6].lower(),
            }
        )
    return out


def load_manifest(project: Path) -> dict | None:
    p = project / ".writeonmars-manifest.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f".writeonmars-manifest.json no es JSON válido: {e}")


def bar(label: str, width: int = 18) -> str:
    return label.ljust(width)


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


def main() -> None:
    ap = argparse.ArgumentParser(description="Dashboard de estado de una guía Write.OnMars.")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--spec", default=None)
    ap.add_argument("--gate", action="store_true", help="Exit 1 si el proyecto NO cierra.")
    args = ap.parse_args()

    project = Path(args.project_dir).resolve()
    spec_dir = newest_spec_dir(project, args.spec)
    blocks = parse_findings(spec_dir / "findings.md")
    manifest = load_manifest(project)
    signing = (manifest or {}).get("signing_matrix", {})

    chapters = sorted(
        p.name for p in (project / "chapters").glob("*.md")
    ) if (project / "chapters").is_dir() else []
    expected = count_temario(spec_dir)

    print("=" * 64)
    print(f" Write.OnMars · {spec_dir.name}")
    print("=" * 64)
    if expected:
        print(f" Capítulos: {len(chapters)}/{expected} del temario")
    else:
        print(f" Capítulos redactados: {len(chapters)}")
    if chapters:
        print("   " + ", ".join(chapters))
    print("-" * 64)
    print(f" {bar('Pasada')}{bar('Estado',22)}{bar('Firma',12)}Hallazgos")
    print("-" * 64)

    crit_open = 0
    sign_violations: list[str] = []
    total_open = 0

    if not blocks:
        print("   (sin findings.md todavía: ninguna pasada ejecutada)")
    for b in blocks:
        sev = {"critico": 0, "medio": 0, "bajo": 0}
        open_here = 0
        for h in b["hallazgos"]:
            sev[h["severidad"]] = sev.get(h["severidad"], 0) + 1
            if h["estado"] == "abierto":
                open_here += 1
                if h["severidad"] == "critico":
                    crit_open += 1
        total_open += open_here
        # Gate de firma: una pasada que el manifest exige `human` solo cuenta como
        # firmada si tiene tipo human Y un actor real (no vacío ni "pendiente").
        key = PASS_KEY.get(b["num"])
        required = signing.get(key) if key else None
        invalid_actors = {"", "—", "pendiente", "tbd", "{id}", "actor"}
        firma_disp = b["firma"]
        if required == "human":
            actor = b.get("actor", "")
            signed = b["firma"] == "human" and actor not in invalid_actors
            if not signed:
                motivo = "firma autónoma" if b["firma"] == "autonomous" else f"sin firmar (actor: {actor or '—'})"
                sign_violations.append(f"pasada {b['num']} {b['name']} — {motivo}")
                firma_disp = f"{b['firma']}!"  # marca pendiente
            else:
                firma_disp = f"human:{actor}"
        hl = f"crit {sev['critico']} · med {sev['medio']} · baj {sev['bajo']} · abiertos {open_here}"
        label = f"{b['num']} {b['name']}"
        print(f" {bar(label)}{bar(b['estado'],22)}{bar(firma_disp,14)}{hl}")

    print("-" * 64)
    print(" Gates de cierre")
    g1 = crit_open == 0
    g2 = not sign_violations
    g3 = (expected == 0) or (len(chapters) >= expected)
    print(f"   [{'OK' if g1 else 'X'}] Sin hallazgos críticos abiertos   (críticos abiertos: {crit_open})")
    if g2:
        print("   [OK] Firmas humanas completas")
    else:
        print(f"   [X] Firma humana faltante en: {', '.join(sign_violations)}")
    if g3:
        print(f"   [OK] Guía completa   ({len(chapters)}/{expected or len(chapters)} capítulos)")
    else:
        print(f"   [X] Guía incompleta   ({len(chapters)}/{expected} capítulos del temario)")
    closeable = g1 and g2 and g3
    print("-" * 64)
    print(f" CIERRE: {'PROYECTO CERRABLE' if closeable else 'BLOQUEADO'}"
          f"  (hallazgos abiertos totales: {total_open})")
    if not g3:
        print(" Nota: faltan capítulos. `export` genera un PDF parcial; `close` los exige todos.")
    if manifest is None:
        print(" Nota: sin .writeonmars-manifest.json; el gate de firma no se evalúa.")
    print("=" * 64)

    if args.gate and not closeable:
        sys.exit(1)


if __name__ == "__main__":
    main()
