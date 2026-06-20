#!/usr/bin/env python3
"""writeonmars feedback-intake — convierte un PDF anotado en un change-set.

Cierra el loop de revisión sin retrabajo. Lee las anotaciones de un PDF (las que
deja Marcela: resaltados, tachados, notas, comentarios), mapea cada una a su
capítulo de origen buscando el texto anclado en `chapters/*.md`, las clasifica y
produce:

  - specs/<###-feature>/feedback.md            (log legible, categorizado)
  - specs/<###-feature>/feedback-changeset.json (para re-despacho quirúrgico)

Es determinista: la reescritura la hace el agente (comando `speckit.feedback`)
solo sobre los capítulos afectados, no sobre la guía entera.

Dependencias: `pymupdf` (recomendado, extrae el texto bajo cada resaltado) o
`pypdf` (fallback, solo comentarios). Instala con:
    pip install pymupdf        # o: pip install pypdf

Convención de etiquetas en el comentario (opcional, para clasificar):
    #dato #voz #estructura #claridad #cobertura   (tipo)
    #recortar #ampliar                            (acción)
    #critico #medio #bajo                         (severidad)
Sin etiqueta: el tipo se infiere del subtipo de anotación y la severidad es 'medio'.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

TIPOS = {
    "dato": "Dato/precisión",
    "voz": "Voz",
    "estructura": "Estructura",
    "claridad": "Claridad",
    "cobertura": "Cobertura",
    "recortar": "Recortar",
    "ampliar": "Ampliar",
}
SEVERIDADES = {"critico", "medio", "bajo"}
# Subtipo de anotación → tipo por defecto cuando no hay etiqueta.
SUBTYPE_DEFAULT = {
    "StrikeOut": ("Recortar", "medio"),
    "Highlight": ("Voz", "medio"),
    "Underline": ("Claridad", "bajo"),
    "Squiggly": ("Claridad", "bajo"),
    "Text": ("Nota", "bajo"),
    "FreeText": ("Nota", "bajo"),
    "Caret": ("Ampliar", "medio"),
}


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[feedback] error: {msg}", file=sys.stderr)
    sys.exit(1)


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


# --------------------------------------------------------------------------- #
# Extracción de anotaciones (pymupdf preferido, pypdf fallback)
# --------------------------------------------------------------------------- #
def extract_with_pymupdf(pdf: Path) -> list[dict]:
    import fitz  # type: ignore

    annots = []
    doc = fitz.open(pdf)
    for pageno, page in enumerate(doc, start=1):
        for a in page.annots() or []:
            info = a.info
            subtype = a.type[1] if a.type else ""
            if subtype in {"Link", "Popup"}:
                continue
            anchored = ""
            try:
                anchored = page.get_textbox(a.rect).strip()
            except Exception:
                pass
            annots.append(
                {
                    "page": pageno,
                    "subtype": subtype,
                    "comment": (info.get("content") or "").strip(),
                    "author": (info.get("title") or "").strip(),
                    "anchor_text": anchored,
                }
            )
    doc.close()
    return annots


def extract_with_pypdf(pdf: Path) -> list[dict]:
    from pypdf import PdfReader  # type: ignore

    annots = []
    reader = PdfReader(str(pdf))
    for pageno, page in enumerate(reader.pages, start=1):
        for ref in page.get("/Annots") or []:
            try:
                obj = ref.get_object()
            except Exception:
                continue
            subtype = str(obj.get("/Subtype", "")).lstrip("/")
            if subtype in {"Link", "Popup"}:
                continue
            annots.append(
                {
                    "page": pageno,
                    "subtype": subtype,
                    "comment": str(obj.get("/Contents", "")).strip(),
                    "author": str(obj.get("/T", "")).strip(),
                    "anchor_text": "",  # pypdf no resuelve el texto bajo el resaltado
                }
            )
    return annots


def extract_annotations(pdf: Path) -> tuple[list[dict], str]:
    try:
        return extract_with_pymupdf(pdf), "pymupdf"
    except ImportError:
        pass
    try:
        return extract_with_pypdf(pdf), "pypdf"
    except ImportError:
        fail("instala pymupdf (recomendado) o pypdf: pip install pymupdf")


# --------------------------------------------------------------------------- #
# Clasificación y mapeo a capítulo
# --------------------------------------------------------------------------- #
def classify(annot: dict) -> tuple[str, str, str]:
    """Devuelve (tipo, severidad, comentario_limpio)."""
    comment = annot["comment"]
    tags = {t.lower() for t in re.findall(r"#(\w+)", comment)}
    tipo = next((TIPOS[t] for t in tags if t in TIPOS), None)
    sev = next((t for t in tags if t in SEVERIDADES), None)
    if tipo is None:
        tipo, sub_sev = SUBTYPE_DEFAULT.get(annot["subtype"], ("Nota", "bajo"))
        sev = sev or sub_sev
    sev = sev or "medio"
    clean = re.sub(r"#\w+", "", comment).strip()
    return tipo, sev, clean


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def locate_chapter(anchor: str, chapters: list[tuple[str, Path, str]]) -> tuple[str | None, int | None]:
    """Busca el texto anclado en los capítulos. Devuelve (nombre_archivo, linea)."""
    if not anchor or len(anchor) < 6:
        return None, None
    needle = norm(anchor)[:60]
    for _id, path, content in chapters:
        if needle and needle in norm(content):
            # línea aproximada
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if needle[:30] in norm(line):
                    return path.name, i
            return path.name, None
    return None, None


def load_chapters(project: Path) -> list[tuple[str, Path, str]]:
    cdir = project / "chapters"
    out = []
    if cdir.is_dir():
        for p in sorted(cdir.glob("*.md")):
            out.append((p.stem, p, p.read_text(encoding="utf-8")))
    return out


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="Convierte un PDF anotado en un change-set editorial.")
    ap.add_argument("--pdf", required=True, help="PDF anotado por la revisora.")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--spec", default=None)
    args = ap.parse_args()

    project = Path(args.project_dir).resolve()
    pdf = Path(args.pdf).resolve()
    if not pdf.exists():
        fail(f"no existe el PDF {pdf}")
    spec_dir = newest_spec_dir(project, args.spec)
    chapters = load_chapters(project)

    raw, engine = extract_annotations(pdf)
    if not raw:
        print(f"[feedback] no se encontraron anotaciones en {pdf.name} (motor: {engine})")
        return

    items = []
    for i, a in enumerate(raw, 1):
        tipo, sev, comment = classify(a)
        chap, line = locate_chapter(a["anchor_text"], chapters)
        items.append(
            {
                "id": f"FB-{i}",
                "chapter_file": chap,
                "line": line,
                "page": a["page"],
                "tipo": tipo,
                "severidad": sev,
                "anchor_text": a["anchor_text"][:200],
                "comentario": comment,
                "subtype": a["subtype"],
                "estado": "abierto",
            }
        )

    affected = sorted({it["chapter_file"] for it in items if it["chapter_file"]})

    # --- feedback.md ---
    lines = [
        f"# Feedback del PDF anotado — {spec_dir.name}",
        "",
        f"**Fuente**: `{pdf.name}` · **Fecha**: {date.today().isoformat()} · "
        f"**Motor**: {engine} · **Anotaciones**: {len(items)}",
        "",
        f"**Capítulos afectados**: {', '.join(affected) if affected else '(sin mapear — revisar a mano)'}",
        "",
        "| ID | Capítulo | Pág | Tipo | Severidad | Texto anclado | Comentario | Estado |",
        "|----|----------|-----|------|-----------|---------------|------------|--------|",
    ]
    for it in items:
        chap = it["chapter_file"] or "?"
        anchor = (it["anchor_text"] or "").replace("|", "\\|").replace("\n", " ")[:60]
        com = (it["comentario"] or "").replace("|", "\\|").replace("\n", " ")[:80]
        lines.append(
            f"| {it['id']} | {chap} | {it['page']} | {it['tipo']} | {it['severidad']} "
            f"| {anchor} | {com} | {it['estado']} |"
        )
    lines += [
        "",
        "## Tareas de revisión (re-despacho quirúrgico)",
        "",
        "Re-despachar SOLO estos capítulos y re-correr sus pasadas locales:",
        "",
    ]
    for chap in affected or ["(ninguno mapeado automáticamente)"]:
        n = sum(1 for it in items if it["chapter_file"] == chap)
        lines.append(f"- `{chap}` — {n} cambio(s)")
    feedback_md = spec_dir / "feedback.md"
    feedback_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # --- feedback-changeset.json ---
    changeset = {
        "generated": date.today().isoformat(),
        "pdf": pdf.name,
        "spec": spec_dir.name,
        "engine": engine,
        "affected_chapters": affected,
        "items": items,
    }
    cs_path = spec_dir / "feedback-changeset.json"
    cs_path.write_text(json.dumps(changeset, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- resumen ---
    by_sev: dict[str, int] = {}
    unmapped = 0
    for it in items:
        by_sev[it["severidad"]] = by_sev.get(it["severidad"], 0) + 1
        if not it["chapter_file"]:
            unmapped += 1
    print(f"[feedback] {len(items)} anotaciones (motor: {engine})")
    print(f"[feedback] severidad: " + " · ".join(f"{k} {v}" for k, v in by_sev.items()))
    print(f"[feedback] capítulos afectados: {', '.join(affected) or '—'}")
    if unmapped:
        print(f"[feedback] sin mapear a capítulo: {unmapped} (revisar a mano; pág en feedback.md)")
    print(f"[feedback] → {feedback_md}")
    print(f"[feedback] → {cs_path}")


if __name__ == "__main__":
    main()
