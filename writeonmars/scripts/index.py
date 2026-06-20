#!/usr/bin/env python3
"""writeonmars index — memoria de búsqueda del proyecto editorial.

Indexa el markdown del proyecto (capítulos, research, glosario, findings) en
fragmentos con metadatos, para que el agente pueda buscar contenido previo y no
contradecir ni redefinir lo ya escrito. Caché, nunca fuente de verdad: se
reconstruye desde el repo (constitución § Arquitectura del framework).

Backends de búsqueda, autodetectados (de mejor a peor):
  1. rank-bm25  → ranking BM25 (recomendado; `pip install rank-bm25`).
  2. interno    → cosine sobre TF, sin dependencias.
(El backend semántico con embeddings —chromadb + sentence-transformers— se puede
añadir después; la estructura del índice ya lo admite.)

Uso:
    python3 index.py build                 # construye .writeonmars-index.json
    python3 index.py query "context window"  # busca
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

INDEX_NAME = ".writeonmars-index.json"
CHUNK_WORDS = 180


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[index] error: {msg}", file=sys.stderr)
    sys.exit(1)


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-záéíóúñü0-9]+", text.lower())


def iter_source_files(project: Path):
    seen = set()
    patterns = [
        "chapters/*.md",
        "specs/*/research.md",
        "specs/*/findings.md",
        "glossary.md",
        "glosario.md",
        "anexos.md",
        "common-errors.md",
    ]
    for pat in patterns:
        for p in sorted(project.glob(pat)):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p


def chunk_markdown(path: Path, project: Path) -> list[dict]:
    """Divide por encabezados y agrupa ~CHUNK_WORDS palabras por fragmento."""
    text = path.read_text(encoding="utf-8")
    rel = str(path.relative_to(project))
    chunks: list[dict] = []
    heading = ""
    buf: list[str] = []

    def flush():
        if not buf:
            return
        body = " ".join(buf).strip()
        if body:
            chunks.append({"file": rel, "heading": heading, "text": body})
        buf.clear()

    for line in text.splitlines():
        h = re.match(r"#{1,6}\s+(.+)", line.strip())
        if h:
            flush()
            heading = h.group(1).strip()
            continue
        if line.strip():
            buf.append(line.strip())
            if sum(len(b.split()) for b in buf) >= CHUNK_WORDS:
                flush()
    flush()
    return chunks


def build(project: Path) -> None:
    chunks = []
    for p in iter_source_files(project):
        chunks.extend(chunk_markdown(p, project))
    if not chunks:
        fail("no encontré markdown para indexar (chapters/, research.md, glosario…)")
    for i, c in enumerate(chunks):
        c["id"] = i
        c["tokens"] = tokenize(c["text"])
    index = {"chunk_words": CHUNK_WORDS, "n": len(chunks), "chunks": chunks}
    out = project / INDEX_NAME
    out.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    files = sorted({c["file"] for c in chunks})
    print(f"[index] {len(chunks)} fragmentos de {len(files)} archivos → {out.name}")


def _load(project: Path) -> dict:
    p = project / INDEX_NAME
    if not p.exists():
        fail(f"no existe {INDEX_NAME}; corre primero: index.py build")
    return json.loads(p.read_text(encoding="utf-8"))


def _score_bm25(chunks, q_tokens):
    from rank_bm25 import BM25Okapi  # type: ignore

    corpus = [c["tokens"] for c in chunks]
    bm25 = BM25Okapi(corpus)
    return bm25.get_scores(q_tokens), "bm25"


def _score_tf(chunks, q_tokens):
    # IDF + TF cosine, sin dependencias.
    n = len(chunks)
    df = Counter()
    for c in chunks:
        for t in set(c["tokens"]):
            df[t] += 1
    idf = {t: math.log(1 + n / (1 + df[t])) for t in df}
    q = Counter(q_tokens)
    qvec = {t: q[t] * idf.get(t, 0.0) for t in q}
    qnorm = math.sqrt(sum(v * v for v in qvec.values())) or 1.0
    scores = []
    for c in chunks:
        tf = Counter(c["tokens"])
        dot = sum(qvec.get(t, 0.0) * tf[t] * idf.get(t, 0.0) for t in qvec)
        dnorm = math.sqrt(sum((tf[t] * idf.get(t, 0.0)) ** 2 for t in tf)) or 1.0
        scores.append(dot / (qnorm * dnorm))
    return scores, "tf"


def query(project: Path, q: str, top: int) -> None:
    index = _load(project)
    chunks = index["chunks"]
    q_tokens = tokenize(q)
    if not q_tokens:
        fail("consulta vacía")
    try:
        scores, engine = _score_bm25(chunks, q_tokens)
    except ImportError:
        scores, engine = _score_tf(chunks, q_tokens)
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)[:top]
    print(f"[index] motor: {engine} · {len(chunks)} fragmentos\n")
    for score, c in ranked:
        if score <= 0:
            continue
        snippet = c["text"][:160].replace("\n", " ")
        head = f" › {c['heading']}" if c["heading"] else ""
        print(f"  [{score:.3f}] {c['file']}{head}")
        print(f"          {snippet}…\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Memoria de búsqueda del proyecto editorial.")
    ap.add_argument("action", choices=["build", "query"])
    ap.add_argument("text", nargs="?", default="", help="Consulta (para 'query').")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()
    project = Path(args.project_dir).resolve()
    if args.action == "build":
        build(project)
    else:
        if not args.text:
            fail("uso: index.py query \"tu consulta\"")
        query(project, args.text, args.top)


if __name__ == "__main__":
    main()
