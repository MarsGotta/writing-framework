# Bookwright frente a Write.OnMars: contraste y qué tomar prestado

**Fecha**: 2026-07-03 · **Fuente analizada**: [jmorenobl/bookwright](https://github.com/jmorenobl/bookwright) v0.5.13 (repo clonado y leído en local, no solo el README) · **Contraparte**: preset `writeonmars/` v0.1.0 + `paperclip/`.

## 1. Qué es bookwright

Un CLI en Python instalable ([PyPI `bookwright-cli`](https://github.com/jmorenobl/bookwright#instalación), EUPL-1.2) más un juego de skills de agente para escribir novela, ensayo y memorias con el patrón spec-driven. La idea central: constitución, biblia, outline y manuscrito viven en texto plano bajo git; el CLI deriva de ellos un grafo de conocimiento (ontología [GOLEM](https://github.com/GOLEM-lab/golem-ontology) serializada en Turtle vía rdflib) y valida continuidad de forma **determinista** (presencia de personajes, cronología, focalización, estructura narrativa con vocabularios Propp/Greimas, anclas factuales). El juicio semántico con LLM (`/bookwright-continuity`, `/bookwright-verify`) existe pero queda **fuera del gate determinista** por diseño.

Datos de madurez verificados en el repo: 54 iteraciones Spec Kit completas en `specs/`, ~200 ficheros Python con mypy strict y cobertura ≥80% en CI, sitio de docs mkdocs con estructura Diátaxis, y dogfooding real: dos libros escritos con la herramienta y publicados en Amazon ([The Kola-Coca Company](https://www.amazon.es/dp/B0GXR59J3Q), [De la Pasión de Jesús a la Resurrección de Cristo](https://www.amazon.es/dp/B0GWMJNKQC)). La confianza en el autor está justificada: es un trabajo serio y muy disciplinado.

## 2. La diferencia de fondo: dónde vive el método

| | Write.OnMars | Bookwright |
|---|---|---|
| Papel de Spec Kit | **Es el runtime del método editorial**: el pipeline de escritura son comandos `speckit.*` | **Herramienta de construcción**: Spec Kit construye el CLI; el flujo de escritura es del producto (skills `bookwright-*` + CLI) |
| Núcleo determinista | Scripts (`status.py`, `close.py`, `export.py`) + convención markdown parseada con regex | Software empaquetado y testeado: grafo derivado, validadores tipados, contrato de resultados |
| Dominio | Guías técnicas de no-ficción en español | Ficción, ensayo y memorias |
| Modelo de agentes | Equipo multiagente con roles, firmas y cross-model | Un solo agente que invoca skills; sin modelo de actores |

Para Vivarium esto es una validación externa fuerte de nuestra tesis de arquitectura: otra persona, resolviendo el mismo problema, llegó a la misma separación (texto plano en git como fuente de verdad + estado derivado determinista + juicio LLM en capa aparte, fuera del gate). Bookwright es estructuralmente el tipo de motor que Vivarium presenta como fachada.

## 3. Qué tenemos mejor (no perderlo)

**Separación escribe uno, revisa otro.** Bookwright no tiene modelo de actores: el mismo agente puede redactar la escena y juzgar su continuidad. Nuestra regla dura (Redactora ≠ Editora de mesa ≠ Documentalista, cross-model, firmas autónoma/humana, estado `desviacion_justificada` con razón documentada) no existe allí en ninguna forma. Es nuestro diferencial principal y el que mapea directo a `decisions.jsonl` de Vivarium.

**Verificación factual por afirmación.** Nuestra pasada 4 emite `claims.md` con relación a la evidencia (`apoya/matiza/contradice/menciona`), veredicto por afirmación, verificación **en vivo** de URLs volátiles, índice de factualidad derivado y gate opcional `factuality_min`. Bookwright tiene procedencia de fuentes y anclas, pero `/bookwright-verify` es una skill LLM sin registro persistente por afirmación, sin verificación en vivo obligada y sin métrica.

**Loop de cierre completo.** `export.py` (PDF editorial), `feedback_intake.py` (PDF anotado → change-set quirúrgico → revise solo de capítulos afectados) y `close.py`. En bookwright el export está en horizonte demand-pulled: no existe.

**Capa de calidad de prosa.** `marcela-prose` y `technical-guide-design` son un método de calidad (voz, didáctica, carga cognitiva). Bookwright solo comprueba **consistencia** con la voz declarada en su constitución, no calidad de la prosa.

**Orquestación operativa.** Paperclip con 4 roles y flujo por capítulo funciona hoy; bookwright es deliberadamente mono-agente.

## 4. Qué tienen mejor y merece adoptarse

Ordenado por relación valor/coste:

### 4.1 Protocolo `[PENDING]` + `/clarify` + actualización in situ

Su mecanismo central de avance: cuando una skill no puede resolver un dato, escribe `[PENDING: ¿pregunta concreta?]` en el artefacto y **continúa**. Un pending sin resolver se trata como *indeciso*, no como respuesta: queda invisible para la validación (cero falsas alarmas). `/bookwright-clarify` lista las dudas abiertas del proyecto, y las skills generativas actualizan **in situ**: respetan la prosa humana y los pendientes ya resueltos, solo rellenan lo abierto ([docs/guides/pending.md](https://github.com/jmorenobl/bookwright/blob/main/docs/guides/pending.md)).

Nuestro `speckit.specify` bloquea hasta resolver los 8 campos del brief. Adoptar el patrón pending lo convierte en no bloqueante sin perder rigor. Y para Vivarium es un encaje perfecto con el principio de calma: huecos marcados, nada urge, nada bloquea.

### 4.2 Veredicto tri-valor con `kind` en las pasadas

Su contrato de validación (iteraciones 040/044/050, `bookwright-design.md §13`) distingue: evaluado sin hallazgos, evaluado con hallazgos, **no-evaluado(motivo, kind)** y evaluación parcial. El `kind` es un vocabulario cerrado: `missing_input` (faltó una entrada de este proyecto, accionable, deniega el verde) vs `pending_capability` (hueco de capacidad, visible pero no deniega). El predicado de verde vive en un único sitio.

Hoy nuestra pasada 4 sin acceso web declara `pendiente` por claim, pero la pasada puede pintarse `passed`. Adoptar el estado `no-evaluado` a nivel de pasada en `pass-output-schema` y `status.py` elimina el verde engañoso. Es además la formalización natural de detector ≠ corrector: un detector honesto declara lo que no pudo mirar.

### 4.3 Foco autoral separado del estado derivado

Su §21 separa tres capas: **foco autoral** (bloque `[focus]` del manifest, lo escribe el autor: `bookwright focus set/show/clear`), **estado derivado** (computado, función pura sobre el estado en disco, con `next_actions` por tabla de reglas estática) y **juicio** (LLM, en skills). Doctrina: *el estado se computa, nunca se inventa*.

Nuestro `status.py` ya deriva `next_step`, pero no tenemos puntero de intención ("qué trabajo ahora"). Un bloque `focus` en el manifest es barato y resuelve el síntoma que ellos documentan: skills que arrancan sesión sin contexto y preguntan en blanco. Para Vivarium, es el "¿por dónde iba?" del escritor al abrir la app.

### 4.4 El patrón grafo derivado como detector (no el stack)

GOLEM/RDF/SPARQL no lo adoptaría: es ontología de ficción y un coste alto. El **patrón** sí: derivar un índice estructurado del markdown y correr detectores deterministas fuera del LLM. En writeonmars habilitaría detectores baratos (terminología contra glosario, referencias cruzadas capítulo↔temario, huérfanos de research). En Vivarium es directamente la arquitectura del equipo editorial: findings deterministas donde se pueda, juicio LLM donde no, y el gate solo sobre lo determinista.

### 4.5 Dato para el Core de Vivarium (anclaje)

Su anclaje es `relpath:línea` con procedencia reificada en el grafo, y **funciona porque el grafo se rederiva entero en cada build**: ningún ancla sobrevive entre builds, así que las líneas nunca envejecen (spec [048-actionable-graph-locators](https://github.com/jmorenobl/bookwright/tree/main/specs/048-actionable-graph-locators)). Inferencia nuestra: esto sugiere dos regímenes de anclaje en Vivarium, findings de revisión **efímeros** (file:línea + rederivación, barato) frente a Leaves del autor **persistentes** (que sí deben sobrevivir ediciones y siguen necesitando el Core). No resuelve nuestra decisión pendiente, pero acota la mitad del problema.

### 4.6 Higiene de gobernanza del repo

Tres piezas baratas y directamente copiables: `DEBT.md` como registro de deuda con reglas explícitas de entrada y borrado (la deuda detectada fuera de scope se anexa, la resuelta se borra, git conserva el historial); la sección de **decisiones axiomáticas que no se reabren** (`bookwright-design.md §16`, equivalente endurecido de nuestra tabla de decisiones); y el roadmap **demand-pulled** con lista explícita de cancelados ("no lo pidas"), que evita plumbing especulativo.

### 4.7 Distribución y empaquetado

PyPI + materialización de skills por integración (`claude`/`generic` sobre el estándar [Agent Skills](https://agentskills.io), con `skills-lock.json`), README bilingüe y el dogfooding como marketing (los dos libros publicados en la portada del repo). Nuestro pendiente de distribución del preset tiene aquí un modelo completo que estudiar.

### 4.8 Ancla como hallazgo promovido a restricción

Su modelo de investigación distingue Fuente → Hallazgo → **Ancla** (hallazgo promovido explícitamente a restricción que el manuscrito no puede contradecir; el resto es color o contexto). La promoción explícita es más fina que nuestro CitationRecord plano y encaja con el modo producción de Vivarium: el escritor decide qué hechos obligan.

## 5. Qué no copiar

El stack RDF/Turtle/SPARQL (patrón sí, tecnología no). La doctrina "batch, no conversacional" como absoluto: vale para guías técnicas, pero el modo estudio de Vivarium es acompañamiento, no destilado por lotes. Y ojo con el vocabulario: bookwright redacta prosa de ficción sin complejos (`/bookwright-draft` es "el único comando que produce prosa de manuscrito"); nuestra decisión de vocabulario de supervivencia (Vivarium edita, guía y verifica, jamás "escribe por ti" hacia ficción) sigue vigente y nos diferencia de él.

## 6. Nota final

La distancia real entre ambos no está en el método editorial (el nuestro es más rico: roles, firmas, factualidad por afirmación, cierre a PDF) sino en el **núcleo determinista testeado**: ellos llevan 54 iteraciones endureciendo validadores con disciplina de software; nosotros parseamos markdown con regex en dos scripts. Si Vivarium va a apoyarse en el preset como motor, el camino que bookwright ya recorrió (contrato de validación tri-valor, estado derivado puro, locators accionables) es el mapa de lo que nos tocará endurecer.

Detalle menor observado: su `AGENTS.md` quedó desactualizado respecto a `CLAUDE.md` (declara v0.2.0 cuando el repo va por v0.5.13); mantener docs de contexto paralelos deriva. Nuestros symlinks multi-agente de `tools/new-guide.sh` evitan justo eso.
