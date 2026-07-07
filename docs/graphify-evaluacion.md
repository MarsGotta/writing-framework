# Grafo de Roots en Vivarium: evaluación de graphify frente a construir propio

**Fecha**: 2026-07-03 · **Fuente analizada**: [safishamsi/graphify](https://github.com/safishamsi/graphify) v0.9.5 (repo clonado y leído en local: `extract.py`, `dedup.py`, `serve.py`, `export.py`, spec de extracción LLM, 124 ficheros de test) · **Caso de uso evaluado**: conectar Roots (personajes, fuentes, ciudades), analizar consistencia de personaje contra su arco, verificar citas, contar usos ("cuántas veces y dónde") y grafo visual estilo Obsidian.

## 1. Qué es graphify realmente

Una herramienta para **asistentes de código**: `/graphify .` mapea un proyecto de software (código, docs, PDFs, imágenes) a un grafo de conocimiento que el agente consulta en vez de grepear. MIT, PyPI `graphifyy`, empresa YC S26 (Graphify Labs, según su README), desarrollo muy activo (último commit el mismo día de este análisis, changelog de 227 KB, CI, 124 ficheros de test).

Cómo extrae, y esto es lo que decide todo:

| Capa | Método | Determinista |
|---|---|---|
| Código (~20 lenguajes) | AST vía tree-sitter: imports, llamadas, símbolos | Sí |
| Markdown/docs (estructura) | Regex: headings, enlaces `[texto](...)` y `[[wikilinks]]` entre documentos | Sí |
| **Conceptos y entidades de prosa** | **Subagentes LLM** con un prompt de extracción genérico (conceptos, entidades, citas) que emite JSON con confianza `EXTRACTED/INFERRED/AMBIGUOUS` | **No** |

Piezas de ingeniería reales y bien hechas: pipeline de deduplicación de entidades (normalización → MinHash/LSH → Jaro-Winkler → union-find), servidor **MCP** de consulta (`query_graph` BFS/DFS con presupuesto de tokens, `get_node`, `get_neighbors`, `shortest_path`, `god_nodes`, `graph_stats`), exports a `graph.html` interactivo, **vault de Obsidian**, JSON y Cypher (Neo4j/FalkorDB opcionales), actualización incremental con cache semántica, watch y hooks de git.

## 2. El desajuste de fondo

Graphify está construido para responder "¿cómo se conecta este codebase?" a un agente de código. Todo lo que Vivarium necesita del grafo (personajes, lugares, citas, arcos) cae en su capa **LLM**, la única no determinista, con un esquema pensado para software: los `file_type` válidos son `code|document|paper|image|rationale|concept`. No hay personaje, lugar, evento, cita ni arco; no hay ontología narrativa ninguna. La capa determinista que sí trae (AST de 20 lenguajes de programación, triaje de PRs de GitHub) es peso muerto para un manuscrito.

Tres consecuencias concretas contra los requisitos:

**Los conteos no serían de fiar.** "Este personaje aparece 14 veces, aquí" exige extracción exacta. En graphify, las entidades de prosa las extrae un LLM por chunks de ficheros y luego un dedup difuso decide si `manuscript_cap_01_juan` y `manuscript_cap_03_juan` son el mismo nodo. Con alias narrativos ("Juan", "el detective", "Herrera") el merge difuso falla en ambas direcciones: separa lo que es uno y junta lo que son dos. Un contador que a veces miente es peor que no tenerlo: rompe el principio detector honesto y la confianza en la UI. La alternativa determinista es trivial cuando los Roots están **declarados** (ficha de personaje con sus alias en la biblia): matching exacto de alias sobre la prosa, con `fichero:línea` por aparición. Es exactamente lo que hace el `character_presence` de bookwright.

**La consistencia de personaje no la da ningún grafo.** "Juan no haría esto según su arco" es juicio semántico: lo hace un LLM leyendo la ficha del personaje, su arco declarado y la escena, con el grafo como contexto de recuperación. Graphify no aporta nada aquí que no aporte pasarle los ficheros correctos al agente; bookwright resolvió esto mismo con `/bookwright-continuity` (juicio LLM fuera del gate) sobre un índice determinista. El grafo ayuda a **encontrar** qué leer (todas las escenas donde aparece Juan), no a juzgar.

**La verificación de citas ya la tenemos mejor.** Graphify tiene aristas `cites` pero cero maquinaria de verificación (no compara la cita con la fuente, no corrige nada). Nuestra pasada 4 + `claims.md` (relación `apoya/matiza/contradice`, verificación en vivo, veredicto por afirmación) es más de lo que graphify ofrecerá nunca en este frente: su roadmap es memoria para agentes de código. Lo que falta no es capacidad de verificar sino **representar** cita y fuente como nodos del grafo para contarlas y navegarlas, y eso es formato, no motor.

A esto se suma el riesgo de dependencia: startup en v0.9.x moviéndose rápido (la rama principal es `v8`), un solo autor dominante, roadmap orientado a coding assistants (sus últimas features son triaje de PRs de GitHub, introspección de Postgres y Cargo). Acoplar una feature nuclear de Vivarium a esa trayectoria es apostar a que sus prioridades coincidan con las nuestras; no hay razón para que lo hagan. MIT mitiga (se puede forkear), pero forkear 15.000+ líneas de `extract.py` del que usaríamos el 10% no es mitigación, es adopción de deuda.

## 3. Lo que sí vale la pena robarle

No adoptar la herramienta no significa ignorarla. Cuatro piezas son directamente aprovechables:

1. **El formato `graph.json`** (nodos/aristas con `source_file`, `source_location`, `relation`, `confidence`, hyperedges). Adoptar un esquema compatible es gratis y deja abierta la puerta a usar su visor o su servidor tal cual.
2. **El patrón del servidor MCP de consulta.** `query_graph` con BFS/DFS, presupuesto de tokens y `get_neighbors` es exactamente cómo los agentes de Vivarium deberían consumir el grafo ("agentes y RAG vía MCP" ya es invariante nuestra). Al ser MIT y un módulo razonablemente aislado (`serve.py`), se puede reutilizar sobre un `graph.json` propio o reimplementar el contrato en unas pocas horas.
3. **Las etiquetas de confianza.** `EXTRACTED` (determinista) vs `INFERRED/AMBIGUOUS` (LLM) es la traducción a grafo de detector ≠ corrector: el índice propio emite `EXTRACTED`; los enriquecimientos del equipo editorial (relaciones inferidas entre personajes, temas) emiten `INFERRED` y jamás alimentan conteos ni gates.
4. **`graph.html` y el export a Obsidian como banco de pruebas hoy.** Antes de diseñar nada: correr graphify sobre un manuscrito real con biblia y mirar qué sale. Coste: una tarde. Sirve para validar si el grafo visual aporta al escritor (la mecánica se evalúa contra la tesis: ¿ayuda a avanzar el manuscrito?) sin escribir una línea.

## 4. Recomendación

**Ni graphify como motor, ni "de cero" en el sentido de reinventar todo: índice propio delgado + convenciones que ya existen.** El grafo de Vivarium no es un problema de extracción (que es donde graphify pone su ingeniería) porque en nuestro modelo **las entidades están declaradas**: los Roots son ficheros con frontmatter (nombre, tipo, alias). La convención de fichas no hay ni que inventarla: [OKF, Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) (spec abierta de Google, 2026-06) formaliza exactamente este patrón (un concepto por fichero markdown, ruta = identidad, frontmatter con `type` obligatorio, enlaces = grafo), y basta definir sobre ella los tipos editoriales (personaje, lugar, fuente, cita, evento). Con eso, el grafo se **deriva** determinista y barato:

- **Nodos**: fichas de Roots (personajes, lugares, fuentes) + capítulos/Branches + citas de `claims.md`/CitationRecord.
- **Aristas de aparición**: matching exacto de nombre+alias sobre el manuscrito → `aparece_en(cap, línea)`. De ahí salen los conteos y el "dónde" con exactitud, gratis.
- **Aristas declaradas**: `[[wikilinks]]` entre fichas (Juan `[[Madrid]]`, cita X `[[fuente Y]]`), que el escritor ya crea al escribir.
- **Aristas inferidas** (opcionales, etiquetadas `INFERRED`): las propone el equipo editorial, nunca cuentan como hechos.
- **Régimen efímero**: el grafo se rederiva en cada build, como los findings (ver `vivarium.md` §13, dos regímenes de anclaje). No se persiste verdad en el grafo: es una proyección del markdown, coherente con "markdown en git es la única fuente de verdad".
- **Consumo**: servidor MCP con el contrato de graphify (o su `serve.py` directamente); las lentes de consistencia de personaje y verificación de citas son skills LLM que consultan ese grafo, fuera del gate.
- **Visual**: para el MVP del experimento, el `graph.html` que sea; para Vivarium, render propio sobre el `graph.json` (el jardín es identidad de producto, no un vis.js genérico).

El tamaño del índice propio así acotado es de días, no meses: parsear frontmatter, matching de alias, emitir JSON. Es la misma conclusión que dejó el análisis de bookwright (`docs/bookwright-contraste.md` §4.4): adoptar el **patrón** grafo-derivado-determinista, no el stack de nadie. Graphify aporta el contrato MCP, el formato y un prototipo gratis; el motor no es suyo porque su motor resuelve otro problema.

**Primer paso sugerido** (barato y reversible): correr `graphify` sobre un manuscrito de prueba con biblia, mirar `graph.html` y el vault de Obsidian, y decidir con eso delante si la visualización merece sitio en el MVP o en etapa 2.
