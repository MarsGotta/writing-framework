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
# Conversión y ensamblado
# --------------------------------------------------------------------------- #
def pandoc_fragment(md: Path, anchor_id: str) -> str:
    try:
        out = subprocess.run(
            ["pandoc", str(md)], capture_output=True, text=True, check=True
        ).stdout
    except FileNotFoundError:
        fail("pandoc no está instalado (brew install pandoc / apt install pandoc)")
    except subprocess.CalledProcessError as e:
        fail(f"pandoc falló en {md}: {e.stderr.strip()}")
    return f'<div class="chapter" id="{anchor_id}">\n{out}\n</div>\n'


def build_cover(eyebrow: str, title: str, subtitle: str, meta: str) -> str:
    tpl = (ASSETS / "cover.html.template").read_text(encoding="utf-8")
    return (
        tpl.replace("{{EYEBROW}}", html.escape(eyebrow))
        .replace("{{TITLE}}", html.escape(title))
        .replace("{{SUBTITLE}}", html.escape(subtitle))
        .replace("{{META}}", html.escape(meta))
    )


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
    fail("no encuentro Chrome ni Chromium; pásalo con --chrome")


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_-]+", "-", s) or "guia"


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
    args = ap.parse_args()

    project = Path(args.project_dir).resolve()
    if not project.is_dir():
        fail(f"no existe el directorio {project}")
    if not (ASSETS / "style.css").exists():
        fail(f"falta {ASSETS/'style.css'}; ¿copiaste los assets del preset?")

    spec_dir = newest_spec_dir(project, args.spec, required=False)
    title = args.title or (parse_title(spec_dir / "spec.md", project.name) if spec_dir else project.name)
    temario = parse_temario(spec_dir / "plan.md") if spec_dir else {}
    from datetime import date

    meta = args.meta if args.meta is not None else str(date.today().year)
    chapters_dir = Path(args.chapters_dir).resolve() if args.chapters_dir else project / "chapters"

    # --- Recolectar piezas ---
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
    for num, path in chapters:
        anchor = f"cap-{num:02d}"
        meta_t = temario.get(num, {})
        title_c = meta_t.get("title") or first_h1(path)
        desc_c = meta_t.get("promesa", "")
        body_parts.append(pandoc_fragment(path, anchor))
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
    cover = build_cover(args.eyebrow, title, args.subtitle, meta)
    toc = build_toc(args.eyebrow or "Una guía", intro_toc, chap_toc, ref_toc)
    style_href = (ASSETS / "style.css").resolve().as_uri()
    final_html = (
        f'<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        f"<title>{html.escape(title)}</title>\n"
        f'<link rel="stylesheet" href="{style_href}">\n</head>\n<body>\n'
        f"{cover}\n{toc}\n{''.join(body_parts)}\n</body>\n</html>\n"
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
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        fail(f"Chrome falló: {e.stderr.strip()[:400]}")

    if not args.keep_temp:
        shutil.rmtree(tmpdir, ignore_errors=True)
    else:
        print(f"[export] HTML intermedio: {html_path}")

    print(f"[export] OK → {output}")
    print(f"[export] título: {title} | capítulos: {len(chapters)} | spec: {spec_dir.name if spec_dir else '—'}")


if __name__ == "__main__":
    main()
