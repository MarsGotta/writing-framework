"""MCP server entrypoint para writeonmars-research.

Expone tres herramientas:
- research_web(query)
- research_fetch(url)
- research_local(path)

Cada herramienta valida el output contra contracts/citation-record.schema.json
antes de emitirlo. Si valida, devuelve el record; si no, devuelve error.
"""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

try:
    from mcp.server import Server
    from mcp.types import TextContent, Tool
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "mcp es obligatorio. Ejecuta `pip install -e .` antes de arrancar el servidor."
    ) from exc

from . import __version__
from .sources import research_fetch, research_local, research_web


server = Server("writeonmars-research")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="research_web",
            description=(
                "Busqueda web; emite list[CitationRecord] validados contra "
                "contracts/citation-record.schema.json."
            ),
            inputSchema={
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {"type": "string", "minLength": 1},
                    "max_results": {"type": "integer", "minimum": 1, "default": 5},
                },
            },
        ),
        Tool(
            name="research_fetch",
            description=(
                "Descarga un recurso por URL y emite un CitationRecord validado."
            ),
            inputSchema={
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {"type": "string", "format": "uri"},
                },
            },
        ),
        Tool(
            name="research_local",
            description=(
                "Lee un archivo bajo resources/ del proyecto editorial y emite "
                "un CitationRecord tipo=archivo_local."
            ),
            inputSchema={
                "type": "object",
                "required": ["path"],
                "properties": {
                    "path": {"type": "string", "minLength": 1},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "research_web":
        records = list(research_web(arguments["query"], max_results=arguments.get("max_results", 5)))
        return [TextContent(type="text", text=json.dumps(records, ensure_ascii=False))]
    if name == "research_fetch":
        record = research_fetch(arguments["url"])
        return [TextContent(type="text", text=json.dumps(record, ensure_ascii=False))]
    if name == "research_local":
        record = research_local(arguments["path"])
        return [TextContent(type="text", text=json.dumps(record, ensure_ascii=False))]
    raise ValueError(f"Tool desconocida: {name}")


async def _run() -> None:  # pragma: no cover
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:  # pragma: no cover
    print(f"writeonmars-research v{__version__} (contract 1.0) listening on stdio", file=sys.stderr)
    asyncio.run(_run())


if __name__ == "__main__":  # pragma: no cover
    main()
