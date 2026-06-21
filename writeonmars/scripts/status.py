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


def newest_spec_dir(project: Path, override: str | None, required: bool = True):
    """Localiza specs/<###>/. Con required=False devuelve None si todavía no hay
    specs/ (estado normal recién scaffoldeado: aún no se corrió `specify`)."""
    specs = project / "specs"
    if override:
        cand = (specs / override) if not Path(override).is_absolute() else Path(override)
        if not cand.is_dir():
            fail(f"no existe el spec {cand}")
        return cand
    if not specs.is_dir():
        return None if not required else fail(f"no existe {specs}")
    dirs = sorted(d for d in specs.iterdir() if d.is_dir() and (d / "spec.md").exists())
    if not dirs:
        return None if not required else fail(f"ningún specs/*/spec.md bajo {specs}")
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


INVALID_ACTORS = {"", "—", "pendiente", "tbd", "{id}", "actor"}


def _cap_sort_key(cap: str):
    """Ordena capítulos: numéricos primero (1, 2, …), etiquetas (global) al final."""
    return (0, int(cap)) if cap.isdigit() else (1, cap)


def _norm_cap(cap: str) -> str:
    """Normaliza la etiqueta de capítulo igual que el resto del módulo:
    quita corchetes y espacios. '1', '[1]', 'global' → '1', '1', 'global'."""
    return (cap or "").strip().strip("[]").strip()


def _drafted_ordinals(chapters: list[str]) -> set[int]:
    """Ordinales con fichero chapters/NN-*.md presente. Mapea ordinal→fichero por
    el prefijo numérico del nombre (p. ej. '03-intro.md' → 3)."""
    out: set[int] = set()
    for name in chapters:
        m = re.match(r"\s*(\d+)", name)
        if m:
            out.add(int(m.group(1)))
    return out


def _passes_by_chapter(blocks: list[dict]) -> dict[str, set[int]]:
    """Pasadas (1·2·3·4) que cubren cada capítulo, leídas del campo
    'Capítulos cubiertos' de cada bloque de pasada en findings.md.

    El campo es texto libre ('1, 2 y 3', 'global', 'caps. 1-3', etc.): se extraen
    los enteros y, si aparece 'global', se atribuye a la clave 'global'. La pasada 5
    es formato global y no participa del approved por capítulo (solo 1-4)."""
    out: dict[str, set[int]] = {}
    for b in blocks:
        num = b["num"]
        if num not in (1, 2, 3, 4):
            continue
        caps_raw = b.get("capitulos") or ""
        for token in re.findall(r"\d+|global", caps_raw, re.I):
            key = "global" if token.lower() == "global" else str(int(token))
            out.setdefault(key, set()).add(num)
    return out


def _build_by_chapter(
    expected: int,
    chapters: list[str],
    blocks: list[dict],
    revise_by_chapter: dict[str, int],
    advisory_by_chapter: dict[str, int],
) -> tuple[dict[str, dict], bool]:
    """Construye el objeto `by_chapter` (contrato FLOW-CONTRACT §3.7) y la señal
    global `all_chapters_approved`.

    Keyado por ordinal del temario en string ('1'..'N') más 'global' si hay
    hallazgos o cobertura globales. approved = drafted AND {1,2,3,4} ⊆ passes_done
    AND revise_pending == 0."""
    drafted = _drafted_ordinals(chapters)
    passes = _passes_by_chapter(blocks)

    # Claves: 1..expected (temario) + cualquier ordinal con fichero/hallazgo/pasada
    # fuera de rango + 'global' si aparece en hallazgos o cobertura.
    keys: set[str] = {str(n) for n in range(1, expected + 1)}
    keys |= {str(n) for n in drafted}
    keys |= set(revise_by_chapter) | set(advisory_by_chapter) | set(passes)

    by_chapter: dict[str, dict] = {}
    for key in keys:
        is_num = key.isdigit()
        is_drafted = bool(is_num and int(key) in drafted)
        passes_done = sorted(passes.get(key, set()))
        revise_pending = revise_by_chapter.get(key, 0)
        approved = (
            is_drafted
            and {1, 2, 3, 4}.issubset(set(passes_done))
            and revise_pending == 0
        )
        by_chapter[key] = {
            "drafted": is_drafted,
            "passes_done": passes_done,
            "revise_pending": revise_pending,
            "advisory": advisory_by_chapter.get(key, 0),
            "approved": approved,
        }

    # all_chapters_approved: todos los capítulos del temario (1..expected) aprobados.
    # Sin temario (expected == 0) no hay condición global que cumplir → False.
    all_approved = expected > 0 and all(
        by_chapter.get(str(n), {}).get("approved", False)
        for n in range(1, expected + 1)
    )
    return by_chapter, all_approved


def _next_step(project: Path, spec_dir: Path, manifest: dict | None,
               blocks: list, chapters: list, expected: int,
               closeable: bool, crit_open: int, sign_violations: list,
               revise_pending: int = 0, revise_by_chapter: dict | None = None,
               advisory_open: int = 0) -> tuple[str, str]:
    """Deriva el siguiente paso del ciclo para el orquestador (Editora jefa).

    Es el corazón del heartbeat: con esto el orquestador decide a qué rol
    delegar sin leer prosa ni acumular ruido. Solo mira estado en disco.
    """
    constitution = project / ".specify" / "memory" / "constitution.md"
    if manifest is None or not constitution.exists():
        return "setup", "base ref sin preparar: el humano corre tools/new-guide.sh (scaffold del Project)"
    if not manifest.get("sector"):
        return "constitution", "adendas sin configurar (sector=null): fija sector + tono (speckit-constitution)"
    if spec_dir is None or not (spec_dir / "spec.md").exists():
        return "specify", "no hay brief: capturar spec.md (Editora jefa · checkpoint humano 1)"
    if not (spec_dir / "research.md").exists():
        return "research", "no hay research.md: delegar a Documentalista (resources/ + web rigurosa)"
    if expected == 0:
        return "plan", "no hay temario en plan.md: diseñar el temario (Editora jefa)"
    pendientes = expected - len(chapters)
    if pendientes > 0:
        return "implement", f"faltan {pendientes} capítulo(s): delegar a Redactora (paralelo en worktrees)"
    if not blocks:
        return "review", "capítulos completos sin findings.md: lanzar pasadas (Mesa + Documentalista)"
    if revise_pending > 0:
        # Política: crítico + medio fuerzan revise (detector ≠ corrector); 'bajo' es
        # aviso y NO bloquea ni fuerza. Enumera los capítulos accionables para que el
        # orquestador haga un BARRIDO —una tarea revise por capítulo a la Redactora—,
        # no un one-off que deja el resto sin corregir.
        caps = sorted((revise_by_chapter or {}), key=_cap_sort_key)
        detalle_crit = f", {crit_open} crítico(s)" if crit_open else ""
        aviso = f"; {advisory_open} aviso(s) 'bajo' aparte (no bloquean)" if advisory_open else ""
        etiqueta = ", ".join(caps) if caps else "—"
        return "revise", (
            f"{revise_pending} hallazgo(s) accionable(s) (crítico+medio{detalle_crit}) en "
            f"{len(caps)} capítulo(s) [{etiqueta}]: una tarea revise POR CAPÍTULO a la "
            f"Redactora (barrido completo, no one-off){aviso}"
        )
    if sign_violations:
        return "review", "faltan firmas humanas exigidas por el manifest"
    if closeable:
        return "close", "gates en verde: intro + export + close (PDF final, Editora jefa)"
    return "review", "revisión en curso: hallazgos abiertos sin resolver"


def evaluate(project: Path, spec_dir: Path) -> dict:
    """Calcula el estado completo del proyecto (read-only). Única fuente de verdad:
    de aquí salen tanto el dashboard humano como la salida `--json` del orquestador.
    """
    blocks = parse_findings(spec_dir / "findings.md") if spec_dir else []
    manifest = load_manifest(project)
    signing = (manifest or {}).get("signing_matrix", {})
    chapters = sorted(
        p.name for p in (project / "chapters").glob("*.md")
    ) if (project / "chapters").is_dir() else []
    expected = count_temario(spec_dir) if spec_dir else 0

    passes: list[dict] = []
    crit_open = 0
    sign_violations: list[str] = []
    total_open = 0
    advisory_open = 0                         # 'bajo' abiertos: avisan, no fuerzan revise
    revise_by_chapter: dict[str, int] = {}    # crítico+medio abiertos por capítulo
    advisory_by_chapter: dict[str, int] = {}  # 'bajo' abiertos por capítulo (avisos)
    for b in blocks:
        sev = {"critico": 0, "medio": 0, "bajo": 0}
        open_here = 0
        for h in b["hallazgos"]:
            s = h["severidad"]
            sev[s] = sev.get(s, 0) + 1
            if h["estado"] != "abierto":
                continue
            open_here += 1
            if s == "critico":
                crit_open += 1
            cap = _norm_cap(h.get("capitulo") or "") or "—"
            if s == "bajo":
                advisory_open += 1            # aviso: no fuerza revise ni bloquea
                advisory_by_chapter[cap] = advisory_by_chapter.get(cap, 0) + 1
            else:
                # crítico, medio o etiqueta desconocida → accionable (nunca perder un hallazgo)
                revise_by_chapter[cap] = revise_by_chapter.get(cap, 0) + 1
        total_open += open_here
        # Gate de firma: una pasada que el manifest exige `human` solo cuenta como
        # firmada si tiene tipo human Y un actor real (no vacío ni "pendiente").
        key = PASS_KEY.get(b["num"])
        required = signing.get(key) if key else None
        firma_disp = b["firma"]
        signed = None
        if required == "human":
            actor = b.get("actor", "")
            signed = b["firma"] == "human" and actor not in INVALID_ACTORS
            if not signed:
                motivo = "firma autónoma" if b["firma"] == "autonomous" else f"sin firmar (actor: {actor or '—'})"
                sign_violations.append(f"pasada {b['num']} {b['name']} — {motivo}")
                firma_disp = f"{b['firma']}!"  # marca pendiente
            else:
                firma_disp = f"human:{actor}"
        passes.append({
            "num": b["num"], "name": b["name"], "estado": b["estado"],
            "firma": b["firma"], "actor": b["actor"], "firma_disp": firma_disp,
            "required": required, "signed": signed,
            "severidades": sev, "abiertos": open_here,
        })

    g1 = crit_open == 0
    g2 = not sign_violations
    g3 = (expected == 0) or (len(chapters) >= expected)
    closeable = g1 and g2 and g3
    revise_pending = sum(revise_by_chapter.values())
    by_chapter, all_chapters_approved = _build_by_chapter(
        expected, chapters, blocks, revise_by_chapter, advisory_by_chapter,
    )
    next_step, next_detail = _next_step(
        project, spec_dir, manifest, blocks, chapters, expected,
        closeable, crit_open, sign_violations,
        revise_pending, revise_by_chapter, advisory_open,
    )
    return {
        "spec": spec_dir.name if spec_dir else "(sin spec todavía)",
        "chapters": chapters,
        "chapters_written": len(chapters),
        "chapters_expected": expected,
        "passes": passes,
        "criticals_open": crit_open,
        "open_findings_total": total_open,
        "revise_pending": revise_pending,
        "revise_by_chapter": revise_by_chapter,
        "advisory_open_bajo": advisory_open,
        "by_chapter": by_chapter,
        "all_chapters_approved": all_chapters_approved,
        "sign_violations": sign_violations,
        "gates": {
            "no_open_criticals": g1,
            "human_signatures": g2,
            "guide_complete": g3,
        },
        "closeable": closeable,
        "has_manifest": manifest is not None,
        "next_step": next_step,
        "next_detail": next_detail,
    }


def print_dashboard(state: dict) -> None:
    print("=" * 64)
    print(f" Write.OnMars · {state['spec']}")
    print("=" * 64)
    if state["chapters_expected"]:
        print(f" Capítulos: {state['chapters_written']}/{state['chapters_expected']} del temario")
    else:
        print(f" Capítulos redactados: {state['chapters_written']}")
    if state["chapters"]:
        print("   " + ", ".join(state["chapters"]))
    print("-" * 64)
    print(f" {bar('Pasada')}{bar('Estado',22)}{bar('Firma',12)}Hallazgos")
    print("-" * 64)
    if not state["passes"]:
        print("   (sin findings.md todavía: ninguna pasada ejecutada)")
    for p in state["passes"]:
        sev = p["severidades"]
        hl = f"crit {sev['critico']} · med {sev['medio']} · baj {sev['bajo']} · abiertos {p['abiertos']}"
        label = f"{p['num']} {p['name']}"
        print(f" {bar(label)}{bar(p['estado'],22)}{bar(p['firma_disp'],14)}{hl}")
    bc = state.get("by_chapter") or {}
    if bc:
        print("-" * 64)
        print(" Capítulos (ciclo por capítulo)")
        for key in sorted(bc, key=_cap_sort_key):
            c = bc[key]
            estado = "APPROVED" if c["approved"] else ("draft" if c["drafted"] else "pendiente")
            pasadas = "·".join(str(n) for n in c["passes_done"]) or "—"
            print(f"   cap {key:<6} {bar(estado,12)} pasadas {bar(pasadas,10)}"
                  f" revise {c['revise_pending']} · avisos {c['advisory']}")
        print(f"   Todos los capítulos aprobados: {'sí' if state.get('all_chapters_approved') else 'no'}")
    print("-" * 64)
    print(" Gates de cierre")
    g = state["gates"]
    print(f"   [{'OK' if g['no_open_criticals'] else 'X'}] Sin hallazgos críticos abiertos   (críticos abiertos: {state['criticals_open']})")
    if g["human_signatures"]:
        print("   [OK] Firmas humanas completas")
    else:
        print(f"   [X] Firma humana faltante en: {', '.join(state['sign_violations'])}")
    if g["guide_complete"]:
        print(f"   [OK] Guía completa   ({state['chapters_written']}/{state['chapters_expected'] or state['chapters_written']} capítulos)")
    else:
        print(f"   [X] Guía incompleta   ({state['chapters_written']}/{state['chapters_expected']} capítulos del temario)")
    print("-" * 64)
    print(f" CIERRE: {'PROYECTO CERRABLE' if state['closeable'] else 'BLOQUEADO'}"
          f"  (hallazgos abiertos totales: {state['open_findings_total']})")
    print(f" Siguiente paso: {state['next_step']} — {state['next_detail']}")
    if not g["guide_complete"]:
        print(" Nota: faltan capítulos. `export` genera un PDF parcial; `close` los exige todos.")
    if not state["has_manifest"]:
        print(" Nota: sin .writeonmars-manifest.json; el gate de firma no se evalúa.")
    print("=" * 64)


def main() -> None:
    ap = argparse.ArgumentParser(description="Dashboard de estado de una guía Write.OnMars.")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--spec", default=None)
    ap.add_argument("--gate", action="store_true", help="Exit 1 si el proyecto NO cierra.")
    ap.add_argument("--json", action="store_true",
                    help="Emite el estado en JSON (para el orquestador/heartbeat de Paperclip).")
    args = ap.parse_args()

    project = Path(args.project_dir).resolve()
    # El orquestador (--json) tolera la fase temprana sin specs/ (devuelve next_step);
    # el dashboard y el gate de cierre (close.py) siguen exigiendo un spec real.
    spec_dir = newest_spec_dir(project, args.spec, required=not args.json)
    state = evaluate(project, spec_dir)

    if args.json:
        print(json.dumps(state, ensure_ascii=False, indent=2))
    else:
        print_dashboard(state)

    if args.gate and not state["closeable"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
