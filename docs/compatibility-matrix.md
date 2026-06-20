# Matriz de compatibilidad

Registra qué MCPs de investigación y qué agentes son compatibles con Write.OnMars.
Es la referencia rápida para quien instala el preset y para mantenedores que evalúan
PRs nuevos.

Para los criterios de certificación de un MCP, ver `docs/citation-contract.md` §
"Cómo certificar un MCP como compatible". El método es **agente-agnóstico** por
diseño (lógica en comandos + referencias, no en skills de un proveedor): portar a
otro agente no requiere reescribir la lógica, solo apuntar al preset (ver
`writeonmars/AGENTS.md`).

## MCPs de investigación compatibles

| Nombre | Estado | Tipo | Notas |
|--------|--------|------|-------|
| `context7` | v1 | `documentacion_oficial` | Soporta versionado por biblioteca. Recomendado para docs de SDK/API/CLI. |
| `web-search:tavily` | v1 | `web_publica` | Marca `volatil=true` por defecto. Usar con `[VERIFICAR]` antes de publicar. |
| `fetch` | v1 | `web_publica` | Sin reranker; manual. El operador decide qué fragmento citar. |
| `local:resources` | v1 | `archivo_local` | Lee `resources/` del proyecto editorial. Fuente obligatoria si existe. |

## Agentes soportados

El pipeline lo lanza cualquier agente que sepa leer archivos y ejecutar los
comandos del preset (ver `writeonmars/AGENTS.md`). Probado cross-model: redacción
con un modelo, revisión con otro.

| Agente | Estado | Notas |
|--------|--------|-------|
| Claude Code | probado | Los comandos se registran como skills con guion (`/speckit-specify`). |
| Codex | probado (review) | Corrió la pasada de precisión leyendo el preset por ruta. Registro nativo de comandos pendiente. |
| Cursor / Gemini / otros | manual | Apuntar al archivo del comando por ruta hasta registrarlos nativamente. |

---

Para añadir un MCP: ver `docs/citation-contract.md` § Certificación. Para portar un
agente: el contrato operativo está en `writeonmars/AGENTS.md`.
