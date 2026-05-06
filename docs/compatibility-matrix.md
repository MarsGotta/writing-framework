# Matriz de compatibilidad

Este documento registra qué MCPs de investigación y qué agentes son compatibles con Write.OnMars en cada versión. Es la referencia rápida para operadores que instalan el framework y para mantenedores que evalúan PRs nuevos.

Para los criterios de certificación de un MCP, ver `docs/citation-contract.md` § "Cómo certificar un MCP como compatible". Para portar un agente, ver `docs/portability-validation.md` (T075, pendiente).

## MCPs investigación compatibles

| Nombre | Estado | Tipo | Notas |
|--------|--------|------|-------|
| `context7` | v1 | `documentacion_oficial` | Soporta versionado por libreria. Recomendado para docs de SDK/API/CLI. |
| `web-search:tavily` | v1 | `web_publica` | Marca `volatil=true` por defecto. Usar con `[VERIFICAR]` antes de publicar. |
| `fetch` | v1 | `web_publica` | Sin reranker; manual. El operador decide qué fragmento citar. |
| `local:resources` | v1 | `archivo_local` | Lee `resources/` del proyecto editorial. Fuente obligatoria si existe (FR-008). |

## Agentes soportados

| Agente | Estado v1 | Adaptador | Notas |
|--------|-----------|-----------|-------|
| claude-code | v1 (prioritario) | `agents/claude/prompts/` | Implementacion canonica. Cubre todas las skills `writeonmars-*`. |
| codex | planned | `agents/codex/prompts/` | Scaffolding en T074 (Polish). Sin paridad funcional en v1. |
| cursor | planned | TBD | Sin scaffolding aun. Requiere PR completo para entrar al roadmap. |
| other | manual | TBD | Requiere portar adapter. El operador asume el coste de mantenimiento. |

---

Para añadir un MCP: ver `docs/citation-contract.md` § Certificación. Para portar un agente: ver `docs/portability-validation.md` (T075).
