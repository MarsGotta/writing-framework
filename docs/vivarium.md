# Vivarium · Qué es (documento maestro)

> **Documento de contexto** para el proyecto de Cowork. Explica Vivarium completo: visión,
> modelo, arquitectura, mecánicas, mercado y estado. Fuentes hermanas:
> `vivarium-retencion-enganche.md` (mecánicas y validación de mercado, con fuentes) y el
> doc de diseño del editor en Notion ("Write.OnMars · Editor (app local-first)").
> Última actualización: 2026-07-03.

## 1. Qué es Vivarium en una frase

Vivarium (apodo: **Viv**; latín, "lugar de vida") es una **aplicación de escritura
local-first** donde un equipo editorial de agentes de IA trabaja para el escritor: revisa
con rigor verificable lo que el humano escribe, o redacta no-ficción fundamentada en
fuentes bajo la dirección del humano. Por debajo: Markdown, git y Spec Kit, todos
invisibles. Por encima: un espacio zen donde el libro crece como un árbol.

Es la **cara B de Zeeds**: Zeeds es la red social de lectura y publicación (cara A, el
lado del lector); Vivarium es la herramienta de autoría (el lado del autor) y a la vez el
core del editor de Zeeds. La moneda común entre ambas es el Markdown. Publicar = empujar
tu obra desde el repo local a un Forest de Zeeds.

## 2. La tesis

- **De producto:** el competidor real no es otra app, es el **abandono del manuscrito**.
  Vivarium existe para que más gente termine sus libros, acompañada por un equipo que la
  conoce.
- **De mercado:** la línea aceptada socialmente e institucionalizada es "la IA te edita ≠
  la IA escribe por ti" (certificación Human Authored, reglas de Amazon KDP, US Copyright
  Office). Nadie ofrece hoy el bundle: local-first + git oculto + equipo editorial
  multi-agente + verificación de afirmaciones contra fuentes.
- **De experiencia:** la calma es la ventaja competitiva. Cero ansiedad de notificación,
  sin culpa por métricas, la herramienta desaparece (estrategia "fachada").

## 3. El modelo de entidades (lenguaje ubicuo botánico)

Cara A y cara B hablan el mismo idioma:

| Entidad | Qué es | En disco / sistema |
|---|---|---|
| **Zeed** | La idea germinal: el brief/spec del que nace el proyecto. Se planta. | `spec.md`, presentado como panel |
| **Root** | Fuente que nutre y fundamenta (grounding): fuentes fiables, citas, story bible, RAG. | `roots/` |
| **Tree** | El proyecto/obra que crece del Zeed. | el repo git |
| **Branch** | Unidad de contenido, recursiva, con su `tipo` (capítulo, parte, escena, poema, post...). | `content/`, ficheros `.md` |
| **Leaf** | Interacción anclada al texto: comentario/reacción/tag. Del autor (revisión con prioridad) o del lector (social). | CriticMarkup inline (autor) / Postgres (lector) |
| **Forest** | Espacio donde se publica, se descubre y se colabora. Público o privado. | la capa Zeeds (remoto git) |

El pipeline se lee como ciclo botánico: **plantas un Zeed → echa Roots (research) → toma
forma de Tree (plan/estructura de Branches) → crecen las Branches (escritura) → se
comprueba el enraizamiento (claims/consistencia contra Roots) → salen Leaves (revisión) →
se publica a un Forest**.

## 4. Los dos modos (dos puertas, un motor)

- **Modo estudio (el escritor escribe).** La IA guía, revisa y aprende contigo: pasadas
  editoriales, verificación de consistencia contra la story bible, Leaves con prioridad,
  espejo del escritor. Default para novela, relato, poesía, guion y académico.
- **Modo producción (la IA redacta).** Para guías técnicas, tutoriales y no-ficción
  fundamentada: la IA escribe anclada en Roots con la prosa de la casa; el humano dirige
  validando con Leaves CriticMarkup que se convierten en señal para los agentes. Default
  para guía/tutorial/documentación, con verificación obligatoria.

Defaults opinados por tipo de proyecto, **no candados**: cambiar el modo pide
confirmación explícita y explica qué se pierde (el informe de autoría humana). El
incentivo hace de policía. La marca sí se segmenta duro: hacia ficción el marketing solo
habla del estudio; el modo producción se vende al segmento técnico con otro lenguaje.

## 5. Procedencia verificable por span (descartado el "% de IA")

Git + el anclaje + `decisions.jsonl` permiten saber por párrafo: escrito por el humano ·
redactado por IA y reescrito · sugerencia aceptada tal cual · redactado por IA validado.

- **Modo estudio → informe de autoría humana**: evidencia auditable (historial git)
  compatible con la certificación Human Authored. Nadie más puede generarla.
- **Modo producción → declaración honesta (KDP) + credibilidad**: cada afirmación con su
  CitationRecord y su procedencia.

Un porcentaje único de IA queda descartado: es crudo, gameable, y no compra la
certificación (Human Authored descalifica la obra entera si hay prosa generada; KDP exige
declarar lo generado aunque se edite después).

## 6. El motor editorial que hay debajo

Vivarium es la capa visual de un método que ya existe y funciona (repo
`writing-framework`):

- **Write.OnMars / preset writeonmars**: un preset de Spec Kit agente-agnóstico. La
  lógica vive en comandos (`speckit.constitution` · `specify` · `plan` · `research` ·
  `implement` · `revise` · pasadas 1-5) y las reglas en referencias (voz, didáctica,
  método). Scripts deterministas como sidecar: `status.py` (estado desde disco, la
  brújula), `export.py`, `feedback_intake.py`, `close.py`.
- **Equipo de 4 oficios** (agrupado por oficio, no por paso): **Editora jefa**
  (orquestadora, plan editorial, nunca escribe capítulos), **Documentalista** (research +
  pasada de precisión, verifica en vivo), **Redactora** (escribe y aplica revisiones),
  **Editora de mesa** (pasadas de estructura, utilidad, voz y formato; modelo distinto al
  de la Redactora).
- **Reglas duras del método:** escribe uno, revisa otro · detector ≠ corrector (quien
  revisa anota en `findings.md`, quien corrige es la Redactora) · voz y precisión
  separadas · severidad crítico/medio fuerza revisión, bajo solo avisa.
- **Dos ejecutores, un método:** a mano con un solo agente, u orquestado. Desde
  2026-07-07 el ejecutor orquestado es **Vivarium mismo** (constitución v1.6.0
  § Ejecutores del método): la capa Paperclip queda archivada como referencia y
  sus reglas (fan-out único por libro, ciclo peer-to-peer por capítulo,
  checkpoints humanos en brief y galeradas) se conservan en
  `paperclip/FLOW-CONTRACT.md`, que Vivarium implementa.

El flujo por unidad de contenido: la Redactora escribe → la Mesa pasa sus lentes y anota
findings → la Documentalista verifica y decide (accionables abiertos → revisión
quirúrgica; cero → aprobada) → ciclo hasta aprobar. Es un Ralph loop con gate de salida
verificable.

## 7. Estrategia "fachada": Spec Kit invisible

Regla fijada: **solo tocamos el proceso hasta donde Spec Kit nos deje**. `content/` es
nuestro y se mueve; `specs/` y `.specify/` quedan donde Spec Kit los quiere y se muestran
como paneles ("Zeed", "Outline del Tree", research/findings/claims/glossary). Verificado
contra el código real de Spec Kit: renombrar archivos core acopla a internals (evitar);
`.specify/` es el ancla, no se toca.

Lección de mercado que la respalda: Penflip ("GitHub for writers") murió por exponer git
a escritores. El escritor ve manuscrito, equipo y jardín; jamás un pipeline.

## 8. Experiencia: el jardín zen (resumen de mecánicas)

Detalle completo en `vivarium-retencion-enganche.md`. Las piezas:

1. **Memoria que se acumula:** constitución, adendas de voz, story bible y decisiones
   mejoran con cada sesión; "tu editora te conoce desde hace 47 sesiones". El switching
   cost honesto: despedir a un equipo entrenado, nunca lock-in de datos (todo es
   markdown en git).
2. **Ritual nocturno:** dejas la Branch en revisión por la noche; galeradas esperando por
   la mañana. El pipeline asíncrono como mecánica de cita. Digest editorial semanal en
   tono de carta.
3. **Momento mágico en minutos:** pega un texto y recibe una revisión de mesa con Leaves
   priorizadas sin configurar nada; la constitución se construye incremental a partir de
   lo que aceptas y rechazas.
4. **Aceptar/rechazar como interacción estrella** (nivel Cursor, por hunk, teclado), y la
   editora aprende visiblemente ("he dejado de marcarte las oraciones largas").
5. **El espejo del escritor:** autoconocimiento como feature; tus patrones, tu voz
   descrita, tu evolución. Refleja, nunca prescribe ni compara.
6. **Gamificación botánica:** el árbol crece de verdad al aprobar Branches; estaciones,
   no streaks; celebraciones sobrias; el fruto es publicar. Nada de badges ni wordcount.

Prioridad: ritual nocturno y accept/reject que aprende, después momento mágico, árbol
vivo, espejo, digest, Forest.

## 9. El flywheel (foso de largo plazo)

Cada decisión del autor sobre lo que hace la IA alimenta un dataset de entrenamiento:
pares de edición (borrador IA → versión final), accept/reject por hunk (DPO), corrección
dirigida por comentario (instruction-tuning), aceptado tal cual (señal positiva). Las
lentes etiquetan el dataset solas (@voz = oro de prosa; @precision = factualidad).

- `decisions.jsonl` (log de procedencia/decisiones) existe **desde el MVP**, etiquetando
  origen del span y disposición del humano.
- Consentimiento por fases: fase 1 solo tu data (local, privada, modelo de TU voz); fase
  2 opt-in compartido (consentimiento explícito, ToS, anonimización). Nunca por defecto.
- Techo: "tu prosa aprendida", un modelo fine-tuneado con tus correcciones que se vuelve
  el Vivarium Pro hosted. El foso lo construyen los usuarios corrigiendo.

## 10. Arquitectura técnica

- **Desktop-first, local-first.** Paquete de UI agnóstico de plataforma + adaptador de
  plataforma (fs, git, scripts, agentes) con implementación desktop y web.
- **Stack: Tauri** (backend Rust; webview reutilizable para la versión web). Electron
  descartado.
- **Editor:** WYSIWYG por bloques (TipTap/ProseMirror o CodeMirror 6, por decidir) que
  serializa a Markdown + capa CriticMarkup. MVP simplificado: títulos, párrafos, negrita,
  cursiva, subrayado, enlaces.
- **Git:** libgit2 / isomorphic-git. Scripts python del preset como sidecar local.
  **Agentes y RAG vía MCP.** Forest/sync = remoto git.
- **Comentarios (Leaves del autor):** CriticMarkup inline `{>> ... <<}`, dos ejes:
  intención (texto libre) y prioridad (crítico/medio/bajo, reutiliza la severidad del
  pipeline). Routing de quién revisa lo decide el agente (triaje transparente, override
  manual). Resolución = el comentario desaparece al commit (git es el historial).
- **Zeeds (cara A):** Next.js + Vercel Postgres. Los Leaves del lector se anclan en
  Postgres.
- **El anclaje (el Core, PENDIENTE):** el primitivo compartido de posición en el texto
  (autor: inline en markdown/git; lector: paragraph-id + offset en Postgres;
  probablemente algoritmo compartido con almacenamiento distinto). Es foundational:
  comentarios, procedencia, flywheel y Leaves sociales cuelgan de él. **Primera decisión
  técnica a resolver.** Apunte que acota el problema: los findings de revisión pueden
  quedar fuera del Core con un régimen efímero `fichero:línea` (ver roadmap en §13).

## 11. Producto y negocio

**Una plataforma integrada (marca Zeeds), construida "editor primero"** (patrón
GitHub/Copilot): Vivarium ≈ el add-on de IA freemium; Zeeds ≈ la plataforma y el dinero
de equipos. Sin autores que suban Trees no hay nada que colaborar: el orden es editor →
individuos → equipos.

### La escalera de la IA (Vivarium, individual)

**El editor local nunca se gatea** (anzuelo, gratis para siempre). Lo que se escala es la
IA, en tres peldaños:

1. **Free = BYOM total.** Tus claves de API externas o **modelos locales vía Ollama**:
   montas tu propio agente y el pipeline corre entero en tu máquina. El peldaño local es
   además la historia de privacidad más fuerte del mercado ("tu editora completa, sin
   que una sola palabra salga de tu ordenador"): nadie ofrece hoy un pipeline editorial
   100% local. Caveat a gestionar: los modelos locales rinden menos; comunicar qué
   lentes funcionan bien en local y cuáles piden modelo grande, sin prometer paridad.
2. **Pro = modelos gestionados** (hosted, cero configuración) + pipeline completo, más
   agentes/lentes, informes de procedencia. Diseñado para uso episódico: informes por
   manuscrito / precio por proyecto además de mensualidad.
3. **Futuro: modelos propios destilados para el oficio.** Modelos pequeños,
   especializados en revisión editorial (no en generar prosa genérica), entrenados con
   el flywheel (pares de edición, findings, accept/reject etiquetados por lente).
   Precedente validado: Sudowrite construyó Muse (modelo propio de ficción) siendo un
   equipo de ~16 personas, y es su foso real. Doble efecto económico: un modelo
   destilado propio es barato de servir, así que **rompe el techo de margen del hosted**
   (revender API frontier soporta +10-20% antes de la revuelta, como mostraron
   Cursor/Zed; un modelo propio da margen real), y no es copiable porque el dataset lo
   generan nuestros usuarios corrigiendo. Condición de secuencia: es apuesta de fase 3;
   requiere volumen de flywheel primero y competencia seria de training/evals. No
   construir antes de tener los datos.

### Zeeds Enterprise (equipos, el dinero B2B)

Zeeds se separa en **dos negocios con economías opuestas**:

- **Zeeds Enterprise: Forests privados para equipos** (agencias, editoriales, servicios
  editoriales, equipos de contenido). Es la mitad fuerte: B2B SaaS puro que sigue el
  patrón GitHub (el dinero está en los repos privados de organizaciones, no en el feed
  público) y la lección Obsidian (monetizar colaboración/sync, no el editor). **No
  necesita efecto red**: un Forest privado es útil con un solo equipo dentro, sin
  cold-start. El bundle enterprise: Forests privados + Vivarium Pro por asiento +
  admin/SSO.
  - **Feature enterprise de primera clase: compliance de procedencia.** Editoriales y
    agencias van a necesitar demostrar qué es humano y qué es IA (KDP, cláusulas
    contractuales de IA, certificación Human Authored). Un Forest donde cada manuscrito
    llega con su informe de procedencia verificable es feature de compra, no
    nice-to-have, y nadie más puede ofrecerla.
  - **Comprador realista de la primera ola:** equipos de contenido técnico, editoriales
    indie de no-ficción, servicios editoriales y ghostwriting (el segmento donde el modo
    producción es aceptable). Las agencias literarias de ficción llegan después: son
    negocios pequeños, de margen fino y hoy hostiles a la IA.
  - **Competidor real:** Word con track changes y Google Docs (gratis, estándar del
    sector). El switching se justifica solo por lo que Docs no hace: manuscritos largos
    versionados, pipeline de revisión con agentes, procedencia verificable.
- **Zeeds red (lectura social, descubrimiento, monetización de creadores):** la mitad
  débil. Cold-start clásico, la atención ya la poseen Wattpad/Royal Road, y las
  economías para escritores son las peores del sector. Se trata como capa de marketing y
  moat a largo plazo (el bucle "tu Tree se vuelve Root de otro" como mecánica de
  estatus), nunca como línea de ingresos principal. No anclar la viabilidad del
  ecosistema a ella.

### Colaboración local-first

Git ya la resolvió; el Forest es el remoto compartido (async, ramas/PRs). Tiempo real
(CRDT) es capa posterior. Bucle del ecosistema: un Tree publicado puede volverse Root
del Tree de otra persona (fuente citable = estatus).

## 12. Posición de mercado (resumen; detalle con fuentes en el doc hermano)

- **A favor:** la línea edita≠escribe institucionalizada y Vivarium del lado seguro; 42-45%
  de autores ya usa IA (mayoritariamente para revisar, solo 11% genera texto publicable);
  la categoría "IA como editor" crece (ProWritingAid, AutoCrit, Marlowe); BYOM validado;
  local-first+privacidad ataca los miedos #1 (consentimiento, 96%) y #2 (imitación de
  voz, 86%); el bundle exacto desocupado.
- **En contra:** 58-67% de novelistas no usa ninguna IA y parte es impersuadible; el
  posicionamiento puede matar la marca (NaNoWriMo cerró en 2025); uso episódico → churn
  estructural sin datos públicos de referencia; economía BYOM = lifestyle salvo que la
  red despegue; Sudowrite ya lanza features agénticas (la ventana de feature-moat dura
  trimestres); la capa social tiene las peores economías del sector.
- **Foso real:** confianza local-first + flywheel consentido + profundidad del método.
  No el número de agentes.

## 13. Estado y orden de construcción

- **Estado:** pre-MVP, backend primero. El motor editorial (preset writeonmars)
  montado y validado en el repo `writing-framework`. La app vive **por ahora como
  monorepo** en `vivarium/` de ese repo (frontera dura documentada en su README;
  extraíble a repo propio después). Paperclip queda archivado como referencia.
- **Cambio de secuencia (2026-07-07):** se construye primero el núcleo headless
  (spec 004: contrato del ejecutor + bootstrap de proyecto + runner por estados +
  campo `mode` del manifiesto), validable por CLI sin interfaz. El editor visual
  (antes "MVP v1") pasa a construirse sobre ese núcleo.
- **MVP v1 (editor, sin orquestación):** abrir un Tree, árbol de Branches, editor Notion-lite,
  Leaves CriticMarkup con prioridad, modo foco, export PDF manual, historial git visible.
- **Etapa 2 (inyectar el proceso):** nuevo proyecto desde la app (sin terminal), captura
  guiada del Zeed + constitución, RAG externo (Roots vía MCP), revisión de consistencia
  contra Roots (generaliza la maquinaria de claims: ficción = "va contra el arco del
  personaje"; académico = "contradice la fuente") apoyada en el grafo de Roots (ver
  apunte de roadmap abajo; si el grafo visual entra en MVP o etapa 2 se decide tras el
  experimento con graphify sobre un manuscrito real).
- **Después:** orquestación completa, flywheel/informes de procedencia, espejo, Zeeds.

**Decisiones abiertas:** el anclaje (la primera); TipTap vs CodeMirror y serialización
del subrayado; RAG externo a integrar; forma del free tier de Zeeds; forma de la bandeja
de galeradas; alcance del espejo; umbral de "reescrito por humano" en procedencia.

### Roadmap futuro: dos regímenes de anclaje (apunte del 2026-07-03)

**Qué es.** Separar el anclaje en dos regímenes con costes y garantías distintos, en vez
de resolver el Core como un problema único:

1. **Findings de revisión: efímeros, `fichero:línea`.** Los hallazgos del equipo
   editorial no necesitan sobrevivir a las ediciones del texto: cada pasada de revisión
   se rederiva entera desde el estado en disco, así que un locator plano
   `manuscript/cap-04.md:42` nunca envejece (si el texto cambió, la siguiente pasada
   emite locators frescos). No requieren el Core.
2. **Leaves del autor y lector: persistentes, el Core.** Los comentarios, la procedencia
   por span y la capa social sí deben sobrevivir a ediciones, merges y reordenaciones.
   Este es el problema duro que sigue pendiente y que el régimen 1 no toca.

**Por qué.** Desacopla el MVP del problema duro: los findings del pipeline (la mayoría
del volumen de anotaciones) pueden construirse ya con el régimen barato, sin esperar a
resolver el Core ni contaminar su diseño con un caso que no necesita persistencia.
Además fija una garantía de honestidad: un finding nunca apunta a una posición
desactualizada, porque no se migra, se regenera.

**Implementación propuesta.** Los findings del preset llevan `path:línea` + hash del
contenido de la línea como cheque de frescura; `status.py` (o su sucesor en Vivarium)
descarta como obsoleto cualquier finding cuyo hash no case y lo marca para re-pasada,
nunca lo reancla. Los Leaves usan el primitivo Core (por decidir: probablemente
paragraph-id estable + offset con algoritmo compartido autor/lector, ver §10). Regla de
frontera: si una anotación necesita sobrevivir a un commit, es Leaf y paga el coste del
Core; si no, es finding y usa el régimen barato.

**Fuente.** Patrón observado en [bookwright](https://github.com/jmorenobl/bookwright)
(spec [048-actionable-graph-locators](https://github.com/jmorenobl/bookwright/tree/main/specs/048-actionable-graph-locators)):
sus validadores anclan todo a `relpath:línea` con procedencia reificada, y funciona
precisamente porque el grafo se rederiva entero en cada build y ningún ancla persiste
entre builds. Análisis completo en `docs/bookwright-contraste.md` (§4.5). La partición
en dos regímenes es inferencia nuestra a partir de ese patrón, no algo que bookwright
implemente (no tiene anotaciones persistentes).

### Roadmap futuro: grafo de Roots (apunte del 2026-07-03)

**Qué es.** Un grafo de conocimiento derivado del manuscrito y sus Roots (personajes,
lugares, fuentes, citas) que conecta cualquier entidad con cualquier otra y con los
puntos del texto donde aparece. Habilita cuatro cosas: navegación entre entidades
(patrón wikilinks + OKF + graphify, el mismo del mars-vault de Marcela pero con
estructura editorial); conteos exactos de uso ("este personaje/esta cita aparece N
veces, aquí"); lentes de revisión con contexto (consistencia de personaje contra su
arco, verificación de citas contra su fuente); y un grafo visual como mecánica del
jardín.

**Por qué.** La revisión de consistencia contra Roots ya está en etapa 2; el grafo es
su columna vertebral: da al equipo editorial el contexto de recuperación (qué escenas
leer para juzgar a un personaje) y al escritor una vista de su mundo que ningún
procesador de texto ofrece. Evaluado contra la tesis: ver el mundo propio crecer y
detectar inconsistencias antes que el lector ayuda a que el manuscrito avance y a
volver mañana.

**Implementación.** Índice propio delgado, no motor de terceros (evaluación crítica en
`docs/graphify-evaluacion.md`): las entidades están **declaradas**, así que no hay
problema de extracción. Reglas:

- **Fichas OKF-compatibles, no OKF-dependientes.** Un concepto por fichero markdown,
  ruta como identidad, frontmatter con `type` (tipos editoriales nuestros: personaje,
  lugar, fuente, cita, evento) más campos propios (alias). Eso es compatible con
  [OKF v0.1](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
  (spec abierta de Google, 2026-06, que formaliza el patrón LLM-wiki) y cuesta cero,
  pero la spec tiene semanas, viene del mundo data-catalog y no condiciona nuestro
  modelo editorial: si muere no perdemos nada, si despega estamos a un rename. El
  escritor jamás ve "OKF" (fachada).
- **Wikilinks solo entre fichas, jamás en la prosa.** El manuscrito no lleva sintaxis
  de herramienta: el escritor no marca entidades a mano (la herramienta desaparece) y
  el markdown exportable queda limpio. Las apariciones en prosa las detecta el índice
  por matching exacto de nombre+alias (conteos y `fichero:línea` exactos); el editor
  puede renderizar menciones como enlaces sutiles, pero eso es derivado, no almacenado.
  El hueco de recall (epítetos, "el detective", pro-drop) no se cierra con matching
  difuso: el equipo editorial **propone alias nuevos para la ficha** y el humano
  confirma; el conteo sigue determinista y la ficha mejora. Honestidad del dato: se
  presenta como "menciones por alias declarado", no como verdad absoluta.
- **Aristas inferidas** por el equipo editorial etiquetadas `INFERRED`: nunca alimentan
  conteos ni gates (detector ≠ corrector en el grafo).
- **Régimen efímero.** El grafo se rederiva en cada build, proyección del markdown,
  nunca fuente de verdad (ver apunte de dos regímenes de anclaje arriba). Para el
  volumen real (una novela larga ~150k palabras, cientos de Roots) basta `graph.json`
  regenerado al guardar y cargado en memoria: el matching es cuestión de milisegundos
  en Rust. **SQLite solo como caché regenerable** (jamás commiteada, borrable sin
  pérdida, patrón `.codegraph/` de bookwright) y solo ante disparador concreto,
  demand-pulled: conteos en vivo por pulsación con índice incremental, búsqueda
  full-text del corpus, o consultas cruzadas multi-proyecto. Antes de eso es plumbing
  especulativo. La evolución de conteos en el tiempo la da git gratis (grafo por
  commit).
- **Consumo por agentes** vía MCP con el contrato de consulta de graphify
  (`query_graph` BFS/DFS, `get_neighbors`, `shortest_path`); las lentes de consistencia
  de personaje y de citas son juicio LLM sobre ese contexto, fuera del gate.
- **Visual:** render propio sobre `graph.json` (el jardín es identidad de producto);
  el `graph.html` de graphify o el visualizador OKF de referencia sirven solo como
  prototipos desechables para validar la mecánica sobre un manuscrito real.

**Secuencia.** Todo esto es etapa 2: queda como apunte, no como construcción, hasta que
el MVP v1 (editor + Leaves) exista. Única excepción por barata: el experimento de una
tarde con graphify/OKF sobre un manuscrito real, que decide si el grafo visual merece
sitio y en qué etapa.

**Fuente.** Patrón validado por partida triple: [bookwright](https://github.com/jmorenobl/bookwright)
(grafo derivado determinista + juicio LLM fuera del gate, `docs/bookwright-contraste.md`
§4.4), [graphify](https://github.com/safishamsi/graphify) (formato `graph.json`,
contrato MCP de consulta y etiquetas `EXTRACTED/INFERRED`, MIT; descartado como motor
por desajuste de dominio, `docs/graphify-evaluacion.md`) y
[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
(spec abierta del formato de fichas; el contenido editorial de los tipos es nuestro,
la spec solo fija la superficie de interoperabilidad). Prior art propio: el mars-vault
(wikilinks + OKF + graphify) demuestra el flujo; aquí cambia la estructura, orientada
al oficio editorial.

## 14. Registro de decisiones tomadas

| Decisión | Resultado |
|---|---|
| Nombre | Vivarium (Viv); Zeeds = plataforma y Forests |
| Proceso vs Spec Kit | Fachada: solo `content/` se mueve; `specs/` y `.specify/` intactos, mostrados como paneles |
| Modelo de entidades | Botánico: Zeed / Root / Tree / Branch (recursivo) / Leaf / Forest |
| Estructura de producto | Una plataforma (marca Zeeds), editor primero |
| Monetización | Editor gratis siempre; Free=BYOM, Pro=hosted; plataforma en Zeeds |
| Stack | Tauri; WYSIWYG bloques → Markdown + CriticMarkup; git; agentes vía MCP |
| Comentarios | Intención + prioridad (crítico/medio/bajo); routing por triaje del agente; se resuelven al commit |
| Export | Manual, desacoplado del cierre |
| Modos | Estudio y producción; defaults por tipo de proyecto, sin candados |
| Transparencia | Procedencia por span (descartado % de IA); informes por modo |
| Flywheel | `decisions.jsonl` desde el MVP; consentimiento por fases; nunca cross-user por defecto |
| Escalera de IA | Free = BYOM total (claves externas u Ollama local) → Pro = hosted → fase 3: modelos propios destilados para revisión (post-flywheel) |
| Zeeds, dos negocios | **Zeeds Enterprise** (Forests privados B2B + Vivarium Pro por asiento + compliance de procedencia) = el dinero; Zeeds red (social/descubrimiento) = marketing y moat, nunca ingresos principales |
| Experiencia | Principios zen; gamificación botánica; sin métricas de wordcount |
| Anclaje | PENDIENTE (el Core, foundational) |
| Ejecutor orquestado | Vivarium (monorepo `vivarium/`, backend primero); Paperclip archivado como referencia (2026-07-07); constitución v1.6.0 codifica modos y ejecutores |
