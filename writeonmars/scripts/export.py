#!/usr/bin/env python3
"""writeonmars export — genera un PDF editorial de una guía Write.OnMars.

Determinista: corre sin agente (apto para Paperclip). Reutiliza el estilo de la
skill `markdown-to-pdf` (writeonmars/assets/style.css), arma la portada desde el
brief y el índice desde el temario de `plan.md`, convierte cada capítulo con
pandoc y genera el PDF con Chrome/Chromium headless.

Uso típico:
    python3 export.py                      # desde la raíz del proyecto editorial
    python3 export.py --title "Mi guía" --subtitle "Para principiantes"
    python3 export.py --project-dir /ruta/al/proyecto --output salida.pdf

El proyecto editorial se espera con esta forma (constitución v1.1):
    specs/<###-feature>/spec.md      (brief; de aquí sale el título)
    specs/<###-feature>/plan.md      (temario; de aquí sale el índice)
    chapters/<NN>-titulo.md          (capítulos; el cuerpo)
    README.md  glossary.md|glosario.md  anexos.md   (intro y referencia, opcional)
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import findings_lib  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[export] error: {msg}", file=sys.stderr)
    sys.exit(1)


# --------------------------------------------------------------------------- #
# Localización de artefactos del proyecto
# --------------------------------------------------------------------------- #
def newest_spec_dir(project: Path, override: str | None, required: bool = True):
    """Localiza specs/<###>/. Con required=False devuelve None si no hay (guía
    legacy de layout plano, sin specs/)."""
    specs = project / "specs"
    if override:
        cand = (specs / override) if not Path(override).is_absolute() else Path(override)
        if not (cand / "plan.md").exists() and not (cand / "spec.md").exists():
            if not required:
                return None
            fail(f"el spec '{override}' no tiene plan.md ni spec.md")
        return cand
    if not specs.is_dir():
        if not required:
            return None
        fail(f"no existe {specs}; ¿es la raíz de un proyecto editorial?")
    dirs = [d for d in specs.iterdir() if d.is_dir() and (d / "plan.md").exists()]
    if not dirs:
        if not required:
            return None
        fail(f"ningún specs/*/plan.md bajo {specs}")
    # Prefiere el de número más alto (001, 002, ...); si no, el más reciente.
    dirs.sort(key=lambda d: d.name)
    return dirs[-1]


def parse_title(spec_md: Path, fallback: str) -> str:
    if spec_md.exists():
        for line in spec_md.read_text(encoding="utf-8").splitlines():
            m = re.match(r"#\s*Feature Specification:\s*(.+)$", line.strip())
            if m:
                return m.group(1).strip()
            m = re.match(r"#\s+(.+)$", line.strip())
            if m and "[" not in m.group(1):
                return m.group(1).strip()
    return fallback


def parse_temario(plan_md: Path) -> dict[int, dict[str, str]]:
    """Devuelve {numero: {'title':..., 'promesa':...}} desde la tabla de Temario."""
    out: dict[int, dict[str, str]] = {}
    if not plan_md.exists():
        return out
    text = plan_md.read_text(encoding="utf-8")
    m = re.search(r"##\s*Temario.*?$(.*?)(?:^##\s|\Z)", text, re.S | re.M)
    block = m.group(1) if m else text
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        num_raw = cells[0]
        if not re.fullmatch(r"\d+", num_raw):
            continue  # salta cabecera, separadora y filas placeholder ("...")
        title = cells[1]
        promesa = cells[2]
        if title.startswith("[") or not title:
            continue
        out[int(num_raw)] = {"title": title, "promesa": promesa}
    return out


def first_h1(md: Path) -> str:
    for line in md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"#\s+(.+)$", line.strip())
        if m:
            return m.group(1).strip()
    return md.stem


def leading_num(name: str) -> int | None:
    m = re.match(r"(\d+)", name)
    return int(m.group(1)) if m else None


def collect_chapters(chapters_dir: Path) -> list[tuple[int, Path]]:
    if not chapters_dir.is_dir():
        return []
    items = []
    for p in sorted(chapters_dir.glob("*.md")):
        n = leading_num(p.name)
        if n is not None:
            items.append((n, p))
    return items


# --------------------------------------------------------------------------- #
# Validación de factualidad contra claims.md (feature 003, decisión D1-A:
# export VALIDA, no genera; la Redactora sigue escribiendo "## Fuentes").
# --------------------------------------------------------------------------- #
import json as _json  # noqa: E402  (uso local, evita tocar el bloque de imports)


def load_claims_by_chapter(spec_dir: Path | None) -> dict[str, list[dict]]:
    """Lee claims.md (bloques ```json por capítulo). Tolerante: {} si no existe o
    no parsea. Gemelo ligero de status.parse_claims (export es standalone)."""
    if not spec_dir:
        return {}
    claims_md = spec_dir / "claims.md"
    if not claims_md.exists():
        return {}
    text = claims_md.read_text(encoding="utf-8")
    out: dict[str, list[dict]] = {}
    for blk in re.findall(r"```json\s*(.+?)```", text, re.S):
        try:
            data = _json.loads(blk)
        except _json.JSONDecodeError:
            continue
        for rec in (data if isinstance(data, list) else [data]):
            if isinstance(rec, dict):
                key = str(rec.get("capitulo", "")).strip().strip("[]").strip() or "—"
                out.setdefault(key, []).append(rec)
    return out


def validate_claims(spec_dir: Path | None, chapters: list[tuple[int, Path]]) -> list[str]:
    """D1-A: comprueba coherencia capítulo↔claims.md SIN reescribir nada. Devuelve la
    lista de avisos (vacía si claims.md no existe → feature inactiva, no se valida).

    Avisa cuando: (a) una afirmación llega al PDF con soporte 'sin_fuente'/'contradicho'
    (no debería sin marca); (b) un capítulo exportado no tiene cobertura en claims.md."""
    by_chap = load_claims_by_chapter(spec_dir)
    if not by_chap:
        return []  # sin claims.md: no se valida (export sigue funcionando)
    warnings: list[str] = []
    UNSUPPORTED = {"sin_fuente", "contradicho"}
    for num, _path in chapters:
        recs = by_chap.get(str(num))
        if recs is None:
            warnings.append(f"cap {num:02d}: sin cobertura en claims.md (pasada 4 no lo registró)")
            continue
        for r in recs:
            sop = r.get("soporte")
            if sop in UNSUPPORTED:
                frase = (r.get("frase") or "")[:60]
                warnings.append(
                    f"cap {num:02d}: afirmación con soporte '{sop}' llega al PDF — "
                    f"\"{frase}…\" ({r.get('claim_id', '?')})"
                )
    return warnings


# --------------------------------------------------------------------------- #
# Conversión y ensamblado
# --------------------------------------------------------------------------- #
# Localiza el "## Fuentes" de cierre de capítulo en el HTML de pandoc para
# envolverlo como aparato (clase .chapter-sources): en PDF queda inline pero
# atenuado, sin tocar el markdown (que conserva la sección por capítulo).
SOURCES_H2 = re.compile(r"<h2\b[^>]*>\s*Fuentes\b", re.I)


def wrap_chapter_sources(html_out: str) -> str:
    m = SOURCES_H2.search(html_out)
    if not m:
        return html_out  # capítulo sin "## Fuentes": lo señala la pasada de revisión
    head, tail = html_out[: m.start()], html_out[m.start():]
    return f'{head}<div class="chapter-sources">\n{tail}\n</div>\n'


def pandoc_fragment(md: Path, anchor_id: str, is_chapter: bool = False) -> str:
    try:
        out = subprocess.run(
            ["pandoc", str(md)], capture_output=True, text=True, check=True
        ).stdout
    except FileNotFoundError:
        fail("pandoc no está instalado (brew install pandoc / apt install pandoc)")
    except subprocess.CalledProcessError as e:
        fail(f"pandoc falló en {md}: {e.stderr.strip()}")
    if is_chapter:
        out = wrap_chapter_sources(out)
    return f'<div class="chapter" id="{anchor_id}">\n{out}\n</div>\n'


def build_cover(eyebrow: str, title: str, subtitle: str, meta: str) -> str:
    tpl = (ASSETS / "cover.html.template").read_text(encoding="utf-8")
    return (
        tpl.replace("{{EYEBROW}}", html.escape(eyebrow))
        .replace("{{TITLE}}", html.escape(title))
        .replace("{{SUBTITLE}}", html.escape(subtitle))
        .replace("{{META}}", html.escape(meta))
    )


def build_cover_compact(title: str, author: str, meta: str) -> str:
    """Portada compacta de pieza única (pista corta): sin eyebrow ni subtitle.
    Gemela pura de build_cover; conserva la clase .cover para heredar la @page."""
    tpl = (ASSETS / "cover-compact.html.template").read_text(encoding="utf-8")
    return (
        tpl.replace("{{TITLE}}", html.escape(title))
        .replace("{{AUTHOR}}", html.escape(author))
        .replace("{{META}}", html.escape(meta))
    )


def cover_author(manifest: dict | None) -> str:
    """Autor para la portada compacta desde manifest['human_operators'][0]:
    su 'email' o, si no lo hay, su 'id'. Cadena vacía si falta el manifiesto o la
    lista de operadores (la portada compacta muestra entonces la línea vacía)."""
    if not manifest:
        return ""
    ops = manifest.get("human_operators") or []
    if not ops:
        return ""
    first = ops[0] or {}
    return str(first.get("email") or first.get("id") or "")


def toc_entry(num: str, title: str, desc: str, anchor: str) -> str:
    return (
        f'    <a class="toc-entry" href="#{anchor}">\n'
        f'      <div class="toc-entry-num">{html.escape(num)}</div>\n'
        f'      <div class="toc-entry-text">\n'
        f'        <div class="toc-entry-title">{html.escape(title)}</div>\n'
        f'        <div class="toc-entry-desc">{html.escape(desc)}</div>\n'
        f"      </div>\n"
        f"    </a>\n"
    )


def build_toc(eyebrow: str, intro, chapters, refs) -> str:
    parts = ['<div class="toc-page">']
    parts.append(f'  <div class="toc-eyebrow">{html.escape(eyebrow)}</div>')
    parts.append('  <h1 class="toc-title">Índice</h1>')
    if intro:
        parts.append('  <div class="toc-section">')
        parts.append('    <div class="toc-section-label">Material introductorio</div>')
        for title, desc, anchor in intro:
            parts.append(toc_entry("·", title, desc, anchor))
        parts.append("  </div>")
    if chapters:
        parts.append('  <div class="toc-section">')
        parts.append('    <div class="toc-section-label">Capítulos</div>')
        for num, title, desc, anchor in chapters:
            parts.append(toc_entry(num, title, desc, anchor))
        parts.append("  </div>")
    if refs:
        parts.append('  <div class="toc-section">')
        parts.append('    <div class="toc-section-label">Material de referencia</div>')
        for title, desc, anchor in refs:
            parts.append(toc_entry("·", title, desc, anchor))
        parts.append("  </div>")
    parts.append("</div>")
    return "\n".join(parts) + "\n"


def find_chrome(override: str | None) -> str:
    if override:
        if Path(override).exists() or shutil.which(override):
            return override
        fail(f"no encuentro Chrome en '{override}'")
    for cand in CHROME_CANDIDATES:
        if Path(cand).exists() or shutil.which(cand):
            return cand
    fail("no encuentro Chrome ni Chromium; pásalo con --chrome /ruta/al/binario o exporta WOM_CHROME=/ruta/al/binario")


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_-]+", "-", s) or "guia"


# --------------------------------------------------------------------------- #
# Ensamblado del documento (pura salvo por pandoc: NO lanza Chrome). Extraída de
# main() para poder verificar el HTML intermedio sin generar un PDF real.
# --------------------------------------------------------------------------- #
def assemble_html(
    project: Path,
    spec_dir: Path | None,
    chapters_dir: Path,
    *,
    title: str,
    subtitle: str = "",
    eyebrow: str = "",
    meta: str,
    track: str = "estandar",
    author: str = "",
    strict_claims: bool = False,
) -> tuple[str, list[tuple[int, Path]]]:
    """Recolecta las piezas y ensambla el HTML final. Devuelve (html, capítulos).

    En pista corta usa la portada compacta y NO genera índice (build_toc); en
    estándar el comportamiento es byte-idéntico al anterior."""
    temario = parse_temario(spec_dir / "plan.md") if spec_dir else {}

    body_parts: list[str] = []
    intro_toc: list[tuple[str, str, str]] = []
    chap_toc: list[tuple[str, str, str, str]] = []
    ref_toc: list[tuple[str, str, str]] = []

    readme = project / "README.md"
    if readme.exists():
        body_parts.append(pandoc_fragment(readme, "intro-readme"))
        intro_toc.append(("Acerca de esta guía", "Promesa, alcance y cómo leerla", "intro-readme"))

    chapters = collect_chapters(chapters_dir)
    if not chapters:
        fail(f"no hay capítulos en {chapters_dir} (esperaba <NN>-titulo.md)")

    # D1-A: validar coherencia con claims.md (no reescribe "## Fuentes"; la Redactora
    # sigue siendo su autora). Sin claims.md no hay avisos (feature inactiva).
    claim_warnings = validate_claims(spec_dir, chapters)
    for w in claim_warnings:
        print(f"[export] aviso factualidad: {w}", file=sys.stderr)
    if claim_warnings and strict_claims:
        fail(f"--strict-claims: {len(claim_warnings)} aviso(s) de factualidad; abortando antes del PDF")

    for num, path in chapters:
        anchor = f"cap-{num:02d}"
        meta_t = temario.get(num, {})
        title_c = meta_t.get("title") or first_h1(path)
        desc_c = meta_t.get("promesa", "")
        body_parts.append(pandoc_fragment(path, anchor, is_chapter=True))
        chap_toc.append((f"{num:02d}", title_c, desc_c, anchor))

    for fname, label, anchor, desc in [
        ("glossary.md", "Glosario", "ref-glosario", "Definiciones de los términos clave"),
        ("glosario.md", "Glosario", "ref-glosario", "Definiciones de los términos clave"),
        ("anexos.md", "Anexos", "ref-anexos", "Plantillas reutilizables"),
        ("common-errors.md", "Errores comunes", "ref-errores", "Síntoma → causa probable"),
    ]:
        f = project / fname
        if f.exists() and anchor not in {a for _, _, a in ref_toc}:
            body_parts.append(pandoc_fragment(f, anchor))
            ref_toc.append((label, desc, anchor))

    # --- Ensamblar HTML ---
    if track == "corta":
        # Pieza única: portada compacta y sin índice (R9). El primer capítulo abre
        # página por el page-break-after de .cover; no hace falta .toc-page.
        middle = build_cover_compact(title, author, meta)
    else:
        cover = build_cover(eyebrow, title, subtitle, meta)
        toc = build_toc(eyebrow or "Una guía", intro_toc, chap_toc, ref_toc)
        middle = f"{cover}\n{toc}"

    style_href = (ASSETS / "style.css").resolve().as_uri()
    final_html = (
        f'<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        f"<title>{html.escape(title)}</title>\n"
        f'<link rel="stylesheet" href="{style_href}">\n</head>\n<body>\n'
        f"{middle}\n{''.join(body_parts)}\n</body>\n</html>\n"
    )
    return final_html, chapters


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="Genera el PDF editorial de una guía Write.OnMars.")
    ap.add_argument("--project-dir", default=".", help="Raíz del proyecto editorial (default: cwd).")
    ap.add_argument("--spec", default=None, help="Nombre/ruta del spec; default: el de número más alto.")
    ap.add_argument("--chapters-dir", default=None, help="Carpeta de capítulos (default: <proyecto>/chapters).")
    ap.add_argument("--title", default=None, help="Título de portada (default: del spec).")
    ap.add_argument("--subtitle", default="", help="Subtítulo de portada.")
    ap.add_argument("--eyebrow", default="", help="Texto pequeño superior (eyebrow) en portada e índice.")
    ap.add_argument("--meta", default=None, help="Meta de portada (default: año actual).")
    ap.add_argument("--output", default=None, help="Ruta del PDF (default: <proyecto>/<slug-titulo>.pdf).")
    ap.add_argument("--chrome", default=os.environ.get("WOM_CHROME"), help="Ruta a Chrome/Chromium.")
    ap.add_argument("--keep-temp", action="store_true", help="No borrar el HTML intermedio.")
    ap.add_argument("--strict-claims", action="store_true",
                    help="Falla (exit 1) si la validación de factualidad contra claims.md emite avisos.")
    args = ap.parse_args()

    project = Path(args.project_dir).resolve()
    if not project.is_dir():
        fail(f"no existe el directorio {project}")
    if not (ASSETS / "style.css").exists():
        fail(f"falta {ASSETS/'style.css'}; ¿copiaste los assets del preset?")

    # Detección de pista (R9, contrato § 4.1). Tolerante: manifiesto ausente ⇒
    # estandar (guía legacy de layout plano). Un manifiesto roto sí es error, pero
    # se reporta como los demás errores de export, no como un traceback: hasta ahora
    # export.py ni leía el manifiesto, así que el fallo sería nuevo y feo.
    try:
        manifest = findings_lib.load_manifest(project)
        track = findings_lib.project_track(manifest)
    except ValueError as exc:
        fail(str(exc))
    author = cover_author(manifest)

    spec_dir = newest_spec_dir(project, args.spec, required=False)
    title = args.title or (parse_title(spec_dir / "spec.md", project.name) if spec_dir else project.name)
    from datetime import date

    meta = args.meta if args.meta is not None else str(date.today().year)
    chapters_dir = Path(args.chapters_dir).resolve() if args.chapters_dir else project / "chapters"

    final_html, chapters = assemble_html(
        project,
        spec_dir,
        chapters_dir,
        title=title,
        subtitle=args.subtitle,
        eyebrow=args.eyebrow,
        meta=meta,
        track=track,
        author=author,
        strict_claims=args.strict_claims,
    )

    tmpdir = Path(tempfile.mkdtemp(prefix="wom-export-"))
    html_path = tmpdir / "final.html"
    html_path.write_text(final_html, encoding="utf-8")

    output = Path(args.output).resolve() if args.output else project / f"{slugify(title)}.pdf"
    chrome = find_chrome(args.chrome)
    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", f"--print-to-pdf={output}", html_path.as_uri(),
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=180)
    except subprocess.CalledProcessError as e:
        fail(f"Chrome falló: {e.stderr.strip()[:400]}")
    except subprocess.TimeoutExpired:
        fail("Chrome superó los 180 s generando el PDF (¿proceso colgado?); reintenta o prueba otro binario con --chrome / WOM_CHROME")

    if not args.keep_temp:
        shutil.rmtree(tmpdir, ignore_errors=True)
    else:
        print(f"[export] HTML intermedio: {html_path}")

    print(f"[export] OK → {output}")
    print(f"[export] título: {title} | capítulos: {len(chapters)} | spec: {spec_dir.name if spec_dir else '—'}")


if __name__ == "__main__":
    main()
