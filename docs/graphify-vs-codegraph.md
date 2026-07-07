# Graphify vs CodeGraph como tooling de navegación del repo

**Fecha**: 2026-07-07 · **Ámbito**: qué herramienta de grafo debe usar el agente para **entender y editar este repositorio** (flujo de trabajo de desarrollo), no como feature de producto. Para la pregunta "¿graphify como motor del grafo de Roots de Vivarium?" ver [`graphify-evaluacion.md`](graphify-evaluacion.md), que es otra decisión y concluye distinto (índice propio + OKF).

## TL;DR

**Usar las dos, cada una en su mitad.** No compiten: resuelven problemas distintos sobre un repo que es 90 % prosa.

- **CodeGraph** → navegación de código en vivo (barata, precisa, sub-ms, ya cableada en MCP). Pero aquí solo ve 23 archivos.
- **Graphify** → mapa periódico del corpus de prosa (el 90 % que CodeGraph no ve). Cuesta tokens; se rehace, no se consulta en caliente.

## 1. El dato que decide: composición del repo

| Tipo | Archivos | Líneas |
|---|---|---|
| Markdown (prosa, referencias, contratos, skills) | 229 | 33.591 |
| Python | 17 | 3.717 |
| Shell | 27 | 5.219 |

El 90 % del repo es prosa. Qué ve cada herramienta importa más que sus features.

## 2. Cara a cara (con datos de una corrida real)

`codegraph status` y `/graphify .` sobre el mismo repo, 2026-07-07:

| | CodeGraph (v1.0.1) | Graphify (`graphifyy`, CLI 0.9.5 / pkg 0.9.9) |
|---|---|---|
| Naturaleza | Grafo SQLite de símbolos (AST) | Grafo de conocimiento LLM-asistido |
| Archivos indexados | **23** (17 py + 6 yaml) | **308** (código + 237 docs + 2 PDF) |
| Nodos / aristas | 422 / 781 | **1.682 / 2.378** (955 AST + 727 semánticos) |
| Comunidades | — | 154 |
| Ve la prosa (90 % del repo) | No | Sí |
| Puentes entre-documento | No | Sí, y relevantes a la tesis del proyecto |
| Coste por build | ~0 (sin LLM) | ~1,6 M tokens (11 subagentes) |
| Latencia de consulta | sub-ms | rebuild / traversal |
| Frescura | daemon en vivo (~1 s de lag) | snapshot; hay que rehacer |
| Integración | MCP + CLAUDE.md global | ninguna (herramienta puntual) |
| Salvedad | — | ~212 aristas colgantes (~8 %): IDs no compartidos entre chunks; grafo usable pero incompleto en enlaces entre-documento |

## 3. Qué reveló Graphify que CodeGraph no puede

Las **conexiones sorprendentes** del reporte no son ruido; caen sobre la arquitectura conceptual del proyecto:

- `prosa-base (capa 1)` ↔ `marcela-prose (capa 3)` — las capas de la pirámide de prosa
- `claims.md / ClaimRecord v1.0` ↔ `CitationRecord v1.0` — el modelo de atribución
- `Gate g4 (factualidad)` ↔ `Firmas desviación_justificada (proxy humano)`
- `Modelo cognitivo (Hayes y Flower)` ↔ `Principio III: brief obligatorio`

**Traza de la pirámide de prosa** (`graphify query`): las tres capas canónicas (`prosa-base`, `registro técnico-divulgativo`, `marcela-prose voz`) agrupan en la misma comunidad junto con las skills de método que las aplican (`writeonmars-redaccion`, `writeonmars-pasada-3`, `writeonmars-descripciones`, `technical-guide-design`). Y el grafo redescubrió por su cuenta un gotcha conocido: la capa de voz está **duplicada en dos árboles y dos comunidades** — `writeonmars/references/voz/…` (preset empaquetado) y `.claude/skills/marcela-prose/…` (skill instalada / dogfooding), con los mismos ficheros (`arquitectura-capitulo.md`, `registros-por-modalidad.md`) espejados. Es una superficie de sincronización real, del tipo que CodeGraph no puede producir.

## 4. Recomendación

Mantener ambas:

- **CodeGraph** como capa por defecto para editar código (`writeonmars/scripts/`, el gate de tests). Ya está indexado, es gratis y preciso, y está cableado en el flujo del agente.
- **Graphify** como mapa periódico del corpus de prosa: un build por mes o tras cambios grandes en `references/`. Se consulta con `graphify query` sobre `graph.json`, se mira `graph.html`, y su audit trail de procedencia (`EXTRACTED/INFERRED/AMBIGUOUS`) encaja con la tesis de atribución del proyecto.

## 5. Política de versionado de `graphify-out/`

Criterio: **versionar solo lo que necesitó destilación desde un modelo.** La extracción semántica (`cache/semantic/`, 239 entradas, ~1,2 M) costó ~1,6 M tokens y es lo único no reconstruible gratis. Todo lo demás es determinista y se regenera sin LLM:

| Se versiona | Se ignora (regenerable sin modelo) |
|---|---|
| `graphify-out/cache/semantic/` | `graph.json`, `graph.html`, `GRAPH_REPORT.md` |
| `graphify-out/.gitignore` | `cache/ast/`, `cache/stat-index.json`, `manifest.json`, `cost.json`, `.graphify_*` |

Implementado como allowlist en [`../graphify-out/.gitignore`](../graphify-out/.gitignore). Un rebuild futuro reutiliza la caché → ~0 tokens en los archivos sin cambios.
