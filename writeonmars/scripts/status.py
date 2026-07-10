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
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import findings_lib  # noqa: E402
from findings_lib import DISPOSITION_BY_STATE, parse_findings  # noqa: E402

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
    """Localiza specs/<###>/ vía la resolución canónica compartida (findings_lib).
    Con required=False devuelve None si todavía no hay specs/ (estado normal
    recién scaffoldeado: aún no se corrió `specify`)."""
    try:
        spec_dir = findings_lib.newest_spec_dir(project, override)
    except ValueError as e:
        fail(str(e))
    if spec_dir is None and required:
        fail(f"ningún specs/*/spec.md bajo {project / 'specs'}")
    return spec_dir


def load_manifest(project: Path) -> dict | None:
    try:
        return findings_lib.load_manifest(project)
    except ValueError as e:
        fail(str(e))


def project_mode(manifest: dict | None) -> str:
    try:
        return findings_lib.project_mode(manifest)
    except ValueError as e:
        fail(str(e))


def project_track(manifest: dict | None) -> str:
    try:
        return findings_lib.project_track(manifest)
    except ValueError as e:
        fail(str(e))


def bar(label: str, width: int = 18) -> str:
    return label.ljust(width)


# count_temario y drafted_ordinals viven ahora en findings_lib (R10, feature 006):
# track.py las comparte para validar el des-escalado. Los alias módulo-locales
# conservan los nombres previos (incluido el guion bajo histórico) para no romper
# importadores ni tests que llaman status.count_temario / status._drafted_ordinals.
count_temario = findings_lib.count_temario


INVALID_ACTORS = {"", "—", "pendiente", "tbd", "{id}", "actor"}


def _cap_sort_key(cap: str):
    """Ordena capítulos: numéricos primero (1, 2, …), etiquetas (global) al final."""
    return (0, int(cap)) if cap.isdigit() else (1, cap)


def _norm_cap(cap: str) -> str:
    """Normaliza la etiqueta de capítulo igual que el resto del módulo:
    quita corchetes y espacios. '1', '[1]', 'global' → '1', '1', 'global'."""
    return (cap or "").strip().strip("[]").strip()


_drafted_ordinals = findings_lib.drafted_ordinals


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


def _chapter_hashes(project: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    chapters_dir = project / "chapters"
    if not chapters_dir.is_dir():
        return hashes
    for path in sorted(chapters_dir.glob("*.md")):
        m = re.match(r"\s*(\d+)", path.name)
        if not m:
            continue
        hashes[str(int(m.group(1)))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def _passes_by_chapter_checked(
    blocks: list[dict], chapter_hashes: dict[str, str]
) -> tuple[dict[str, set[int]], set[str], list[str]]:
    out: dict[str, set[int]] = {}
    reopened: set[str] = set()
    warnings: list[str] = []
    for b in blocks:
        num = b["num"]
        if num not in (1, 2, 3, 4):
            continue
        huellas = b.get("huellas") or {}
        caps_raw = b.get("capitulos") or ""
        for token in re.findall(r"\d+|global", caps_raw, re.I):
            if token.lower() == "global":
                continue
            key = str(int(token))
            current = chapter_hashes.get(key)
            recorded = huellas.get(key)
            if current is None:
                continue
            if recorded != current:
                reopened.add(key)
                reason = "sin huella" if not recorded else "huella no coincide"
                warnings.append(
                    f"capítulo {key}: pasada {num} no cuenta en modo estudio ({reason})"
                )
                continue
            out.setdefault(key, set()).add(num)
    return out, reopened, warnings


def _load_dispositions(spec_dir: Path | None) -> dict[str, set[str]]:
    """Disposiciones humanas por finding_id. Solo se invoca en modo estudio:
    en produccion el archivo se ignora por completo (retrocompat FR-011)."""
    records: dict[str, set[str]] = {}
    if spec_dir is None:
        return records
    path = spec_dir / "disposiciones.jsonl"
    if not path.exists():
        return records
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{path}:{idx} no es DispositionRecord válido: {exc}")
        fid = data.get("finding_id")
        disp = data.get("disposicion")
        if isinstance(fid, str) and isinstance(disp, str):
            records.setdefault(fid, set()).add(disp)
    return records


def _disposition_matches(state: str, dispositions: set[str]) -> bool:
    expected = DISPOSITION_BY_STATE.get(state)
    return bool(expected and expected in dispositions)


# --- Factualidad (feature 003): atribución por afirmación + índice determinista ---
# El JUICIO (relación apoya/matiza/contradice/menciona y soporte) lo produce la
# pasada 4 y vive en claims.md; aquí solo se CUENTA (Principio VI). Determinista,
# sin LLM. claims.md vive junto a findings.md en specs/<feature>/.

# soporte que cuenta en el denominador del índice (excluye 'pendiente': no se midió).
SOPORTE_VERIFICABLE = {"soportado", "parcial", "sin_fuente", "contradicho"}


def parse_claims(claims_md: Path) -> tuple[dict[str, list[dict]], set[str]]:
    """Parsea claims.md (esquema claim-record v1.0). Gemelo conceptual de
    parse_findings, pero la fuente de verdad de máquina es el bloque ```json de
    cada sección de capítulo (data-model §2), no una tabla markdown.

    Devuelve (parsed, malformed):
      - parsed:    {capitulo_str: [ClaimRecord, ...]} por sección con json válido.
      - malformed: {capitulo_str} cuyo bloque ```json falta o no parsea.
    Tolerante: nunca lanza (claims ausente → ({}, set()))."""
    parsed: dict[str, list[dict]] = {}
    malformed: set[str] = set()
    if not claims_md.exists():
        return parsed, malformed
    text = claims_md.read_text(encoding="utf-8")
    headers = list(re.finditer(
        r"^##\s+Claims\s*[—–-]\s*(?:Cap(?:[íi]tulo|\.)?\s*)?(\d+|global)\b",
        text, re.M | re.I))
    if not headers:
        # Sin secciones por capítulo: agrupa todo ClaimRecord por su campo 'capitulo'.
        for blk in re.findall(r"```json\s*(.+?)```", text, re.S):
            try:
                data = json.loads(blk)
            except json.JSONDecodeError:
                continue
            for rec in (data if isinstance(data, list) else [data]):
                if isinstance(rec, dict):
                    key = _norm_cap(str(rec.get("capitulo", ""))) or "—"
                    parsed.setdefault(key, []).append(rec)
        return parsed, malformed
    for i, h in enumerate(headers):
        raw = h.group(1)
        key = _norm_cap("global" if raw.lower() == "global" else str(int(raw)))
        start, end = h.end(), (headers[i + 1].start() if i + 1 < len(headers) else len(text))
        body = text[start:end]
        m = re.search(r"```json\s*(.+?)```", body, re.S)
        if not m:
            malformed.add(key)
            continue
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            malformed.add(key)
            continue
        recs = data if isinstance(data, list) else [data]
        parsed.setdefault(key, []).extend(r for r in recs if isinstance(r, dict))
    return parsed, malformed


def compute_factuality(
    parsed: dict[str, list[dict]],
    malformed: set[str],
    expected: int,
    fill_absent: bool,
) -> dict:
    """Índice de factualidad determinista (data-model §3.1). Sin LLM.

    factuality(c) = soportadas(c) / verificables(c); None si verificables == 0.
    Global = micro-promedio (Σ soportadas / Σ verificables). 'parcial' NO cuenta
    como soportada; 'pendiente' se excluye del denominador y se reporta aparte.

    fill_absent: si True (claims.md existe), los capítulos del temario sin sección
    se marcan 'no medidos' (None + unmeasured); si False (feature inactiva), no se
    inventan capítulos → salida mínima e inerte (retrocompat, SC-003)."""
    by_chapter: dict[str, float | None] = {}
    pending: dict[str, int] = {}
    sum_sop = sum_ver = 0
    for key, recs in parsed.items():
        ver = sum(1 for r in recs if r.get("soporte") in SOPORTE_VERIFICABLE)
        sop = sum(1 for r in recs if r.get("soporte") == "soportado")
        pen = sum(1 for r in recs if r.get("soporte") == "pendiente")
        if pen:
            pending[key] = pen
        if ver > 0:
            by_chapter[key] = round(sop / ver, 4)
            sum_sop += sop
            sum_ver += ver
        else:
            by_chapter[key] = None  # tiene claims pero 0 verificables → no medido
    for key in malformed:
        by_chapter.setdefault(key, None)  # bloque no parseable → no medido (null)
    unmeasured = set(malformed)
    if fill_absent:
        for n in range(1, expected + 1):
            k = str(n)
            if k not in parsed and k not in malformed:
                unmeasured.add(k)
                by_chapter.setdefault(k, None)
    return {
        "factuality_global": (round(sum_sop / sum_ver, 4) if sum_ver > 0 else None),
        "factuality_by_chapter": dict(sorted(by_chapter.items(), key=lambda kv: _cap_sort_key(kv[0]))),
        "factuality_unmeasured": sorted(unmeasured, key=_cap_sort_key),
        "factuality_pending": dict(sorted(pending.items(), key=lambda kv: _cap_sort_key(kv[0]))),
    }


def _build_by_chapter(
    expected: int,
    chapters: list[str],
    blocks: list[dict],
    revise_by_chapter: dict[str, int],
    advisory_by_chapter: dict[str, int],
    passes_override: dict[str, set[int]] | None = None,
) -> tuple[dict[str, dict], bool]:
    """Construye el objeto `by_chapter` (contrato FLOW-CONTRACT §3.7) y la señal
    global `all_chapters_approved`.

    Keyado por ordinal del temario en string ('1'..'N') más 'global' si hay
    hallazgos o cobertura globales. approved = drafted AND {1,2,3,4} ⊆ passes_done
    AND revise_pending == 0."""
    drafted = _drafted_ordinals(chapters)
    passes = passes_override if passes_override is not None else _passes_by_chapter(blocks)

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
               advisory_open: int = 0, fact_block: bool = False,
               mode: str = "produccion",
               pending_chapters: list[int] | None = None,
               pending_dispositions: list[str] | None = None,
               reopened_chapters: list[str] | None = None) -> tuple[str, str]:
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
    pending_chapters = pending_chapters or []
    pending_dispositions = pending_dispositions or []
    reopened_chapters = reopened_chapters or []
    # En produccion, la cuenta de pendientes es la histórica (ficheros vs temario):
    # un capítulo sin prefijo numérico (intro.md) sigue contando como escrito
    # (FR-011). Los ordinales solo gobiernan en estudio, donde nombran qué falta.
    if mode == "estudio":
        pendientes = len(pending_chapters)
        write_step = (
            "write",
            "faltan capítulos por escribir (modo estudio): "
            + ", ".join(str(n) for n in pending_chapters),
        )
    else:
        pendientes = max(0, expected - len(chapters))
        write_step = None
    if pendientes > 0 and not (mode == "estudio" and chapters):
        if write_step:
            return write_step
        return "implement", f"faltan {pendientes} capítulo(s): delegar a Redactora (paralelo en worktrees)"
    if not blocks:
        if mode == "estudio" and pendientes > 0:
            return "review", (
                f"capítulos escritos sin findings.md: lanzar pasadas "
                f"(quedan {pendientes} por escribir después)"
            )
        return "review", "capítulos completos sin findings.md: lanzar pasadas (Mesa + Documentalista)"
    if revise_pending > 0:
        # Política: crítico + medio fuerzan revise (detector ≠ corrector); 'bajo' es
        # aviso y NO bloquea ni fuerza. Enumera los capítulos accionables para que el
        # orquestador haga un BARRIDO —una tarea revise por capítulo a la Redactora—,
        # no un one-off que deja el resto sin corregir.
        if mode == "estudio":
            ids = ", ".join(pending_dispositions) if pending_dispositions else "—"
            return "dispose", (
                f"{revise_pending} hallazgo(s) accionable(s) a la espera de "
                f"disposición humana: {ids}"
            )
        caps = sorted((revise_by_chapter or {}), key=_cap_sort_key)
        detalle_crit = f", {crit_open} crítico(s)" if crit_open else ""
        aviso = f"; {advisory_open} aviso(s) 'bajo' aparte (no bloquean)" if advisory_open else ""
        etiqueta = ", ".join(caps) if caps else "—"
        return "revise", (
            f"{revise_pending} hallazgo(s) accionable(s) (crítico+medio{detalle_crit}) en "
            f"{len(caps)} capítulo(s) [{etiqueta}]: una tarea revise POR CAPÍTULO a la "
            f"Redactora (barrido completo, no one-off){aviso}"
        )
    # Reabiertos por huella DESPUÉS de dispose: con hallazgos accionables abiertos
    # primero dispone la humana (el ejecutor no tiene pasada que despachar sobre un
    # capítulo con revise_pending > 0: sería un callejón sin salida).
    if mode == "estudio" and reopened_chapters:
        return "review", (
            "capítulos con pasadas invalidadas por huella: "
            + ", ".join(reopened_chapters)
        )
    if sign_violations:
        return "review", "faltan firmas humanas exigidas por el manifest"
    if fact_block:
        # g4 (blocking) en rojo: NO es un paso nuevo. El déficit debe estar como
        # hallazgos crítico/medio de la pasada 4 → revise. Si no lo está, es señal
        # de inconsistencia claims.md↔findings.md (ver warnings).
        return "review", (
            "déficit de factualidad bajo umbral (gate g4): debe expresarse como "
            "hallazgos crítico/medio en la pasada 4 y enrutarse por revise; revisa "
            "coherencia claims.md↔findings.md"
        )
    if pendientes > 0 and write_step:
        return write_step
    if closeable:
        return "close", "gates en verde: intro + export + close (PDF final, Editora jefa)"
    return "review", "revisión en curso: hallazgos abiertos sin resolver"


def evaluate(project: Path, spec_dir: Path) -> dict:
    """Calcula el estado completo del proyecto (read-only). Única fuente de verdad:
    de aquí salen tanto el dashboard humano como la salida `--json` del orquestador.
    """
    blocks = parse_findings(spec_dir / "findings.md") if spec_dir else []
    manifest = load_manifest(project)
    mode = project_mode(manifest)
    track = project_track(manifest)
    signing = (manifest or {}).get("signing_matrix", {})
    chapters = sorted(
        p.name for p in (project / "chapters").glob("*.md")
    ) if (project / "chapters").is_dir() else []
    expected = count_temario(spec_dir) if spec_dir else 0
    drafted_ordinals = _drafted_ordinals(chapters)
    pending_chapters = [
        n for n in range(1, expected + 1)
        if n not in drafted_ordinals
    ]
    # El registro de disposiciones es exclusivo del modo estudio; en produccion
    # ni se lee (un archivo corrupto no puede tumbar la brújula, FR-011).
    dispositions = _load_dispositions(spec_dir) if mode == "estudio" else {}

    passes: list[dict] = []
    crit_open = 0
    sign_violations: list[str] = []
    total_open = 0
    advisory_open = 0                         # 'bajo' abiertos: avisan, no fuerzan revise
    revise_by_chapter: dict[str, int] = {}    # crítico+medio abiertos por capítulo
    advisory_by_chapter: dict[str, int] = {}  # 'bajo' abiertos por capítulo (avisos)
    pending_dispositions: list[str] = []
    deferred_findings: list[str] = []
    deferred_details: list[dict] = []
    warnings: list[str] = []
    for b in blocks:
        sev = {"critico": 0, "medio": 0, "bajo": 0}
        open_here = 0
        for h in b["hallazgos"]:
            s = h["severidad"]
            sev[s] = sev.get(s, 0) + 1
            state = h["estado"]
            fid = h.get("id", "")
            cap = _norm_cap(h.get("capitulo") or "") or "—"
            if state == "aplazado":
                deferred_findings.append(fid)
                deferred_details.append({
                    "id": fid,
                    "capitulo": cap,
                    "severidad": s,
                })
            inconsistent_disposition = False
            if mode == "estudio" and state != "abierto":
                if not _disposition_matches(state, dispositions.get(fid, set())):
                    inconsistent_disposition = True
                    warnings.append(
                        f"{fid}: estado {state} sin DispositionRecord compatible; "
                        "cuenta como pendiente en modo estudio"
                    )
            if state != "abierto" and not inconsistent_disposition:
                continue
            open_here += 1
            if s == "critico":
                crit_open += 1
            if s == "bajo":
                advisory_open += 1            # aviso: no fuerza revise ni bloquea
                advisory_by_chapter[cap] = advisory_by_chapter.get(cap, 0) + 1
            else:
                # crítico, medio o etiqueta desconocida → accionable (nunca perder un hallazgo)
                revise_by_chapter[cap] = revise_by_chapter.get(cap, 0) + 1
                if fid:
                    pending_dispositions.append(fid)
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
    base_closeable = g1 and g2 and g3
    revise_pending = sum(revise_by_chapter.values())

    # --- Gate g4: factualidad (feature 003), aditivo y opcional ---
    # g4 solo se EVALÚA si el manifest declara quality_gates.factuality_min.
    # Sin umbral → gates.factuality = None y closeable = g1·g2·g3 (idéntico a v1.0).
    claims_exists = bool(spec_dir and (spec_dir / "claims.md").exists())
    qg = (manifest or {}).get("quality_gates") or {}
    parsed_claims, malformed_claims = (
        parse_claims(spec_dir / "claims.md") if spec_dir else ({}, set())
    )
    fact = compute_factuality(parsed_claims, malformed_claims, expected, fill_absent=claims_exists)
    fmin = qg.get("factuality_min")
    fmin_cap = qg.get("factuality_min_per_chapter")
    fmode = qg.get("factuality_mode", "blocking")
    if fmin is None:
        g4 = None
    else:
        fg = fact["factuality_global"]
        g4_global = fg is not None and fg >= fmin
        g4_caps = (fmin_cap is None) or all(
            v >= fmin_cap for v in fact["factuality_by_chapter"].values() if v is not None
        )
        g4 = bool(g4_global and g4_caps)
    # g4 informa siempre (bool) cuando hay umbral; solo BLOQUEA en modo blocking.
    fact_blocks = g4 is False and fmode == "blocking"
    closeable = base_closeable and (not fact_blocks)
    if fact_blocks and revise_pending == 0:
        warnings.append(
            "factualidad bajo umbral pero sin hallazgos accionables abiertos: posible "
            "inconsistencia claims.md↔findings.md (la pasada 4 debe emitir crítico/medio "
            "por cada déficit, FR-009)"
        )

    reopened_chapters: list[str] = []
    passes_override = None
    if mode == "estudio":
        checked, reopened, hash_warnings = _passes_by_chapter_checked(blocks, _chapter_hashes(project))
        passes_override = checked
        reopened_chapters = sorted(reopened, key=_cap_sort_key)
        warnings.extend(hash_warnings)

    # Avisos advisory de pista corta (R5, contrato §3.2): informan, no bloquean;
    # no tocan next_step, gates, closeable ni by_chapter. En estandar no se emiten.
    if track == "corta":
        if expected > 1:
            warnings.append(
                f"track: corta declara pieza única pero el temario tiene {expected} filas: "
                "corrige el temario o escala (scripts/track.py --escalar)"
            )
        fuera = sorted(n for n in drafted_ordinals if n >= 2)
        if fuera:
            warnings.append(
                "track: corta con capítulos fuera de pieza única ("
                + ", ".join(str(n) for n in fuera)
                + "): sugiere escalar (scripts/track.py --escalar)"
            )

    by_chapter, all_chapters_approved = _build_by_chapter(
        expected, chapters, blocks, revise_by_chapter, advisory_by_chapter,
        passes_override=passes_override,
    )
    if mode == "estudio" and expected > 0:
        # El cierre en estudio se ancla a lo revisado: pasadas invalidadas por
        # huella o hallazgos sin disponer dejan el proyecto no-cerrable aunque
        # g1-g3 estén en verde — la aprobación se refiere al texto actual, y
        # close.py solo consulta closeable (FR-008 hasta el final del pipeline).
        closeable = closeable and all_chapters_approved and not reopened_chapters
    next_step, next_detail = _next_step(
        project, spec_dir, manifest, blocks, chapters, expected,
        closeable, crit_open, sign_violations,
        revise_pending, revise_by_chapter, advisory_open, fact_blocks,
        mode=mode,
        pending_chapters=pending_chapters,
        pending_dispositions=pending_dispositions,
        reopened_chapters=reopened_chapters,
    )
    return {
        "spec": spec_dir.name if spec_dir else "(sin spec todavía)",
        "mode": mode,
        "track": track,
        "chapters": chapters,
        "chapters_written": len(chapters),
        "chapters_expected": expected,
        "pending_chapters": pending_chapters,
        "passes": passes,
        "criticals_open": crit_open,
        "open_findings_total": total_open,
        "revise_pending": revise_pending,
        "revise_by_chapter": revise_by_chapter,
        "pending_dispositions": pending_dispositions,
        "deferred_findings": deferred_findings,
        "deferred_details": deferred_details,
        "reopened_chapters": reopened_chapters,
        "advisory_open_bajo": advisory_open,
        "by_chapter": by_chapter,
        "all_chapters_approved": all_chapters_approved,
        "sign_violations": sign_violations,
        "factuality_global": fact["factuality_global"],
        "factuality_by_chapter": fact["factuality_by_chapter"],
        "factuality_unmeasured": fact["factuality_unmeasured"],
        "factuality_pending": fact["factuality_pending"],
        "factuality_mode": (fmode if fmin is not None else None),
        "warnings": warnings,
        "gates": {
            "no_open_criticals": g1,
            "human_signatures": g2,
            "guide_complete": g3,
            "factuality": g4,
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
    fg = state.get("factuality_global")
    gfact = state["gates"].get("factuality")
    # Bloque de factualidad: se muestra solo si la feature está activa (algo medido o
    # umbral declarado). Inactiva → no se imprime nada → dashboard idéntico a v1.0 (SC-003).
    if fg is not None or gfact is not None or state.get("factuality_unmeasured"):
        pct_g = f"{fg*100:.0f}%" if fg is not None else "no medida"
        print("-" * 64)
        print(f" Factualidad (afirmaciones con evidencia plena): {pct_g}")
        fbc = state.get("factuality_by_chapter") or {}
        for key in sorted(fbc, key=_cap_sort_key):
            v = fbc[key]
            vtxt = f"{v*100:.0f}%" if v is not None else "no medido"
            pen = (state.get("factuality_pending") or {}).get(key, 0)
            print(f"   cap {key:<6} {vtxt}{f' · pendientes {pen}' if pen else ''}")
        unm = state.get("factuality_unmeasured") or []
        if unm:
            print(f"   sin claims (no medidos): {', '.join(unm)}")
    for w in state.get("warnings") or []:
        print(f"   ⚠ {w}")
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
    if g.get("factuality") is not None:
        fgg = state.get("factuality_global")
        pctg = f"{fgg*100:.0f}%" if fgg is not None else "no medida"
        mode = state.get("factuality_mode") or "blocking"
        tag = "" if mode == "blocking" else "   (modo aviso: no bloquea)"
        print(f"   [{'OK' if g['factuality'] else 'X'}] Factualidad sobre umbral (g4)   (global: {pctg}){tag}")
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
