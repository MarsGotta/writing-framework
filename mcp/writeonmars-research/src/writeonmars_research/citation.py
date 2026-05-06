"""CitationRecord dataclass + validación contra contracts/citation-record.schema.json.

Implementa la entidad publicada en `contracts/citation-contract.md` v1.0.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal, Optional

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "jsonschema es obligatorio. Ejecuta `pip install -e .` antes de usar este módulo."
    ) from exc


CitationType = Literal[
    "documentacion_oficial",
    "web_publica",
    "archivo_local",
    "cita_bibliografica",
]
ConfianzaType = Literal["oficial", "comunidad_alta", "comunidad_baja", "personal"]


@dataclass
class CitationRecord:
    """Representación canónica de una cita en Write.OnMars (FR-009)."""

    citation_id: str
    tipo: CitationType
    referencia: str
    fragmento: str
    fecha_consulta: str  # ISO-8601 (YYYY-MM-DD)
    motor: str
    contract_version: str = "1.0"

    versionado_aplicable: Optional[bool] = None
    version_aplicable: Optional[str] = None
    volatil: Optional[bool] = None
    confianza: Optional[ConfianzaType] = None
    notas: Optional[str] = None

    def to_dict(self) -> dict:
        """Serializa el record sin claves None (jsonschema no admite null)."""
        raw = asdict(self)
        return {k: v for k, v in raw.items() if v is not None}


_SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent.parent
    / "contracts"
    / "citation-record.schema.json"
)


def _load_schema() -> dict:
    """Lee `contracts/citation-record.schema.json` del repo canónico."""
    if not _SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el schema en {_SCHEMA_PATH}. "
            "Asegúrate de que el módulo se ejecute desde el repo canónico."
        )
    with _SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


_SCHEMA: Optional[dict] = None


def _schema() -> dict:
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = _load_schema()
    return _SCHEMA


def validate_against_schema(record: CitationRecord) -> dict:
    """Valida un CitationRecord contra el JSON Schema canónico.

    Devuelve el dict serializado si valida. Lanza `jsonschema.ValidationError`
    si no valida (no se hace fallback parcial: el contrato es estricto).
    """
    payload = record.to_dict()
    validator = Draft202012Validator(_schema())
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        messages = "; ".join(f"{list(e.absolute_path)}: {e.message}" for e in errors)
        raise ValueError(f"CitationRecord invalido: {messages}")
    return payload


def build_citation_id(prefix: str, ordinal: int) -> str:
    """Construye un citation_id estable y determinista.

    Convención v1: `<prefix>_<ordinal:03d>`. Ejemplo: `web_001`,
    `local_042`, `doc_007`.
    """
    return f"{prefix}_{ordinal:03d}"
