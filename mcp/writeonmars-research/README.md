# writeonmars-research (MCP de referencia)

Implementación de referencia Python 3.11+ del módulo MCP opcional
`writeonmars-research`. Materializa **FR-009b** del framework: un servidor
único que sustituye al modo BYOM (Bring Your Own MCP) cuando una persona
operadora prefiere no orquestar varios MCPs externos.

El módulo emite [CitationRecord](../../contracts/citation-contract.md) v1.0
validados contra
[`contracts/citation-record.schema.json`](../../contracts/citation-record.schema.json).

## Estado v1

Implementación de referencia. **No es la canónica**: el modo por defecto del
framework sigue siendo `byom` (cada proyecto declara qué MCPs usa). Este
módulo existe para:

- Demostrar que el contrato de citación se puede implementar fielmente desde
  cero.
- Servir de fallback para proyectos editoriales sin acceso a MCPs externos.
- Ser referencia ejecutable para futuros adapters (Codex, Cursor, etc.).

## Instalación

Requiere Python 3.11+.

```bash
cd mcp/writeonmars-research
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Dependencias mínimas (declaradas en `pyproject.toml`): `mcp`, `jsonschema`,
`httpx`, `pydantic`.

## Activación en el manifest del proyecto

Edita `.writeonmars-manifest.json` del proyecto editorial:

```json
{
  "research_mode": "bundled",
  "writeonmars_research_module": {
    "enabled": true,
    "version": "0.1.0"
  }
}
```

Tras editar, vuelve a validar el manifest contra
`contracts/manifest-schema.json` y reinicia el agente que esté usando el MCP.

## Herramientas expuestas

| Herramienta | Input | Output | Descripción |
|-------------|-------|--------|-------------|
| `research_web(query)` | `query: str` | `list[CitationRecord]` | Búsqueda web vía adaptador `httpx`. Cada resultado se normaliza a un CitationRecord `tipo=web_publica`. |
| `research_fetch(url)` | `url: str` | `CitationRecord` | Descarga del recurso indicado y emisión de un único CitationRecord `tipo=documentacion_oficial` (si el dominio está registrado como oficial) o `tipo=web_publica`. |
| `research_local(path)` | `path: str` | `CitationRecord` | Lee un archivo bajo `resources/` del proyecto editorial. CitationRecord `tipo=archivo_local`. |

Cada record valida contra el JSON Schema antes de emitirse. Si la
construcción del record viola el contrato (campos faltantes,
`versionado_aplicable=true` sin `version_aplicable`, `fecha_consulta` sin
formato ISO-8601, etc.), el servidor responde con error explícito y no emite
parcialmente.

## Uso desde Claude Code

Una vez activado y arrancado el servidor, Claude Code lo descubre como un
MCP más. Las skills `writeonmars-research` y `writeonmars-contraste` pasan
los resultados como CitationRecord directamente a `research.md` y
`findings.md` sin transformación adicional.

## Pruebas

Las pruebas viven en este repo bajo `mcp/writeonmars-research/tests/`
(opcional; añadir cuando el módulo deje de ser referencia).

Para una verificación manual rápida:

```bash
python -c "
from writeonmars_research.citation import CitationRecord, validate_against_schema
record = CitationRecord(
    citation_id='cit_001',
    tipo='archivo_local',
    referencia='resources/guia-IA-writing.md',
    fragmento='Diátaxis: cuatro tipos de documentación...',
    fecha_consulta='2026-05-06',
    motor='local:resources',
    contract_version='1.0'
)
print(validate_against_schema(record))
"
```

## Estructura

```
mcp/writeonmars-research/
├── README.md
├── pyproject.toml
├── server.py
└── src/
    └── writeonmars_research/
        ├── __init__.py
        ├── citation.py    # CitationRecord + validación contra schema
        ├── sources.py     # adapters por tipo (web, local, fetch)
        └── server.py      # MCP server entrypoint
```

## Referencias

- `contracts/citation-contract.md` — contrato v1.0 (fuente normativa).
- `contracts/citation-record.schema.json` — schema validado por este módulo.
- `docs/manifest-schema.md` § `writeonmars_research_module` — campo del
  manifest que activa el módulo.
- FR cubierta: FR-009b.
