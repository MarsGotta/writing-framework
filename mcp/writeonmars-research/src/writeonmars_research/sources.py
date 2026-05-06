"""Adapters por tipo de fuente (web, fetch, local).

Cada adapter normaliza la salida del motor concreto a CitationRecord,
respetando el contrato de citación.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urlparse

try:
    import httpx
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "httpx es obligatorio. Ejecuta `pip install -e .` antes de usar este módulo."
    ) from exc

from .citation import CitationRecord, build_citation_id, validate_against_schema


# ---------------------------------------------------------------------------
# Catálogo mínimo de dominios oficiales conocidos. La lista es deliberadamente
# corta en v1; ampliable vía PR.
# ---------------------------------------------------------------------------

_OFFICIAL_DOMAINS = {
    "docs.python.org",
    "developer.mozilla.org",
    "kubernetes.io",
    "docs.djangoproject.com",
    "react.dev",
    "nodejs.org",
    "anthropic.com",
    "docs.anthropic.com",
}


def _today_iso() -> str:
    return _dt.date.today().isoformat()


def _classify_url(url: str) -> tuple[str, str]:
    """Determina (tipo, confianza) a partir del dominio."""
    host = urlparse(url).netloc.lower()
    if any(host == d or host.endswith(f".{d}") for d in _OFFICIAL_DOMAINS):
        return "documentacion_oficial", "oficial"
    return "web_publica", "comunidad_alta"


# ---------------------------------------------------------------------------
# research_local
# ---------------------------------------------------------------------------


def research_local(
    path: str,
    *,
    project_root: Optional[Path] = None,
    fragment_lines: int = 8,
    ordinal: int = 1,
) -> dict:
    """Lee un archivo bajo `resources/` y emite un CitationRecord."""
    project_root = project_root or Path.cwd()
    abs_path = (project_root / path).resolve()
    if not abs_path.exists() or not abs_path.is_file():
        raise FileNotFoundError(f"resources path no existe: {abs_path}")

    text = abs_path.read_text(encoding="utf-8", errors="replace")
    fragment = "\n".join(text.splitlines()[:fragment_lines]).strip() or text[:400]

    record = CitationRecord(
        citation_id=build_citation_id("local", ordinal),
        tipo="archivo_local",
        referencia=str(abs_path.relative_to(project_root)),
        fragmento=fragment,
        fecha_consulta=_today_iso(),
        motor="local:resources",
        contract_version="1.0",
        confianza="personal",
    )
    return validate_against_schema(record)


# ---------------------------------------------------------------------------
# research_fetch
# ---------------------------------------------------------------------------


def research_fetch(
    url: str,
    *,
    fragment_chars: int = 600,
    ordinal: int = 1,
    timeout: float = 10.0,
) -> dict:
    """Descarga el recurso indicado y emite un CitationRecord."""
    tipo, confianza = _classify_url(url)
    response = httpx.get(url, timeout=timeout, follow_redirects=True)
    response.raise_for_status()
    text = response.text
    fragment = text[:fragment_chars].strip()

    record = CitationRecord(
        citation_id=build_citation_id("fetch", ordinal),
        tipo=tipo,
        referencia=url,
        fragmento=fragment,
        fecha_consulta=_today_iso(),
        motor=f"fetch:httpx:{httpx.__version__}",
        contract_version="1.0",
        confianza=confianza,
    )
    return validate_against_schema(record)


# ---------------------------------------------------------------------------
# research_web
# ---------------------------------------------------------------------------


def research_web(query: str, *, max_results: int = 5) -> Iterable[dict]:
    """Búsqueda web. v1 entrega un esqueleto.

    La implementación productiva debería integrarse con un motor concreto
    (Tavily, Brave, etc.). Aquí emitimos un único CitationRecord nulo cuando
    no hay motor configurado, marcando explícitamente la indisponibilidad
    para que el caller no asuma resultados silenciosamente.
    """
    if not query.strip():
        raise ValueError("query vacía")

    # Fallback explícito: emitir un record que marca el motor como ausente.
    record = CitationRecord(
        citation_id=build_citation_id("web", 1),
        tipo="web_publica",
        referencia=f"search-stub://?q={query}",
        fragmento=(
            "research_web esta en modo stub: configura un motor real (Tavily, "
            "Brave, etc.) y reemplaza esta funcion. Hasta entonces, prefiere "
            "research_fetch o research_local."
        ),
        fecha_consulta=_today_iso(),
        motor="web:stub",
        contract_version="1.0",
        confianza="personal",
        notas="motor de busqueda no configurado",
    )
    yield validate_against_schema(record)
    _ = max_results  # silenciar linter; v1 stub no pagina
