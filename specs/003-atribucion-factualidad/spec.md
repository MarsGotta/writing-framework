# Feature Specification: Atribución por afirmación y gate de factualidad

**Feature Branch**: `003-atribucion-factualidad`
**Created**: 2026-06-21
**Status**: Draft
**Project type**: software (feature de framework: contratos, scripts y referencias; NO es una guía editorial)
**Input**: User description: "investigues métodos que estén usando en producción para cosas similares y contrastes" → "necesito que las aterrices más y me digas según la arquitectura y las tecnologías que usa el framework cómo podríamos implementarla" → "dejes todo bien especificado y redactado, al detalle junto la investigación".

---

## Resumen ejecutivo

Esta feature lleva la verificación de fuentes de Write.OnMars del grano **capítulo** al grano **afirmación**, alineándola con el patrón que se ha impuesto en producción para generación long-form con citas (research → grounding → write → **verify**). Se apoya en que la pasada 4 (`writeonmars-contraste`) **ya** extrae afirmaciones verificables, las mapea a `CitationRecord` y verifica en vivo lo volátil; hoy ese trabajo se descarta salvo cuando algo falla. La feature lo **persiste y lo cuenta**.

Tres mejoras, un solo modelo de datos (`ClaimRecord` en `claims.md`):

1. **Atribución por afirmación** — cada afirmación verificable de un capítulo queda anclada a ≥1 fuente en un artefacto durable (`claims.md`), análogo al `CitationRecord` actual.
2. **Veredicto de evidencia (smart citation)** — la pasada 4 clasifica la **relación** de cada cita con la afirmación (`apoya` / `matiza` / `contradice` / `menciona`), no solo si existe la cita; la relación gobierna la severidad.
3. **Gate de factualidad cuantificado** — `status.py` calcula de forma determinista un índice de factualidad (afirmaciones con evidencia / afirmaciones verificables) por capítulo y global, lo expone en `--json` y lo enchufa como gate de cierre configurable.

**Principio rector de la feature**: nada de esto rompe la topología de orquestación de Paperclip. El juicio (LLM) vive en la referencia agnóstica de la pasada 4; el conteo (determinista) vive en `status.py`. La frontera juicio↔conteo es la misma que ya existe entre `findings.md` y los gates. Ver `plan.md` § "Transparencia con Paperclip".

---

## Contexto y motivación

La investigación de métodos en producción (detalle y fuentes en `research.md`) arroja tres conclusiones que esta feature materializa:

- El estado del arte ancla la atribución a **nivel de frase/afirmación**, no de documento ni de sección, porque reduce alucinación y el coste de verificación humana (Anthropic Citations API; "Attribute First, then Generate"; STORM recoge las referencias *durante* la investigación, no post-hoc).
- La factualidad se mide con **descomposición en afirmaciones atómicas + verificación de soporte** (FActScore, VeriScore, RARR). Da una métrica reproducible que hoy Write.OnMars no cuantifica (solo cuenta críticos abiertos).
- El valor de una cita depende de si la fuente **apoya, matiza o contradice** la afirmación, no de su mera presencia (Scite "smart citations"). Es un juicio contextual por arista afirmación↔fuente.

Write.OnMars ya está alineado con el patrón ganador (research-gated → write-from-sources → verify-en-vivo). La deuda frente a producción es de **granularidad de atribución** y **verificación cuantificada**, que es exactamente el alcance de esta feature.

---

## User Stories *(operadores: agente que ejecuta el pipeline + mantenedor del framework)*

### User Story 1 — Atribución por afirmación persistida (Priority: P1)

Quien ejecuta la pasada 4 (la Documentalista, o cualquier agente en modo sin orquestación) produce, además del bloque de `findings.md`, un artefacto durable `claims.md` donde **cada** afirmación verificable del capítulo —no solo las que fallan— queda registrada con su(s) cita(s), su veredicto de soporte y la evidencia literal usada. La sección "Fuentes por capítulo" del capítulo deja de mantenerse a mano y pasa a derivarse/validarse contra `claims.md`.

**Why this priority**: es el cimiento. Las otras dos mejoras (veredicto y factualidad) leen y escriben este mismo artefacto. Sin `claims.md` no hay grano de afirmación ni métrica.

**Independent Test**: correr la pasada 4 sobre un capítulo de fixture con N afirmaciones verificables y comprobar que `claims.md` contiene N `ClaimRecord` válidos contra `claim-record.schema.json`, cada uno con ≥1 entrada en `evidencia[]` o marcado `sin_fuente`, y que el conjunto de `citation_id` referenciados existe en `research.md`.

**Acceptance Scenarios**:

1. **Given** un capítulo redactado y un `research.md` con `CitationRecord`, **When** se ejecuta la pasada 4, **Then** se crea/actualiza `specs/<###-feature>/claims.md` con un `ClaimRecord` por afirmación verificable detectada, validado contra el esquema.
2. **Given** una afirmación verificable sin ninguna cita compatible, **When** se ejecuta la pasada 4, **Then** su `ClaimRecord` queda con `soporte: sin_fuente` y `evidencia: []`, y se emite el finding correspondiente en `findings.md` (severidad según § "Mapeo de severidad").
3. **Given** un `claims.md` ya existente de una ronda previa, **When** la Redactora aplica un `revise` y se re-ejecuta la pasada 4 sobre ese capítulo, **Then** los `ClaimRecord` del capítulo se regeneran (no se duplican) y los de otros capítulos quedan intactos.

---

### User Story 2 — Veredicto de evidencia tipo "smart citation" (Priority: P1)

La pasada 4 no se limita a comprobar que existe una cita: tras abrir la fuente, **clasifica la relación** de cada fuente con la afirmación (`apoya` / `matiza` / `contradice` / `menciona`) y registra el fragmento exacto de la fuente que la sostiene. Esa clasificación gobierna la severidad del finding, enchufándose a la maquinería de revise que ya existe.

**Why this priority**: es lo que convierte la atribución en *verificación de verdad*. Sin esto, "tiene cita" cuenta como soportado aunque la fuente solo mencione el tema o lo contradiga. Es también lo que da contenido al `cita_fragmento_soporte`, que alimenta el grano de frase de US1.

**Independent Test**: sobre fixtures controlados (una afirmación con fuente que la apoya, otra con fuente que solo la menciona, otra con fuente que la contradice), verificar que la pasada 4 asigna `relacion` correcta a cada arista y que la severidad resultante en `findings.md` cumple la tabla de § "Mapeo de severidad".

**Acceptance Scenarios**:

1. **Given** una afirmación de dato duro (versión/comando/precio/estándar/estadística) cuya única cita solo **menciona** el tema sin sostener el dato, **When** se ejecuta la pasada 4, **Then** el `ClaimRecord` queda `soporte: sin_fuente` (o `parcial`) y se emite finding `critico` (dato duro sin evidencia real).
2. **Given** una afirmación cuya fuente abierta en vivo la **contradice**, **When** se ejecuta la pasada 4, **Then** la arista queda `relacion: contradice`, el `ClaimRecord` `soporte: contradicho` y el finding es `critico` (bloquea cierre), con la URL verificada anotada.
3. **Given** una afirmación absoluta cuya fuente la sostiene **con matices**, **When** se ejecuta la pasada 4, **Then** la arista queda `relacion: matiza`, el `ClaimRecord` `soporte: parcial` y el finding es `medio` (accionable: matizar la afirmación).
4. **Given** una afirmación con una fuente que la **apoya** y aporta fragmento de soporte, **When** se ejecuta la pasada 4, **Then** la arista queda `relacion: apoya` con `cita_fragmento_soporte` no vacío y el `ClaimRecord` `soporte: soportado` (sin finding).

---

### User Story 3 — Gate de factualidad cuantificado (Priority: P2)

`status.py` parsea `claims.md` y calcula un índice de factualidad por capítulo y global de forma determinista (sin LLM). Lo expone en el dashboard humano y en `--json`. El manifest puede declarar un umbral (`quality_gates.factuality_min`); cuando se declara, `status.py` evalúa un cuarto gate de cierre (g4) y lo incorpora a `closeable` / `--gate`.

**Why this priority**: aporta el número reproducible y el guardarraíl, pero depende de que US1/US2 llenen `claims.md` con veredictos fiables. Va después.

**Independent Test**: correr `status.py --json` contra fixtures `findings.md` + `claims.md` con factualidad conocida (p. ej. 8 de 10 soportadas) y comprobar que `factuality_global == 0.8`, que `factuality_by_chapter` es correcto, y que con `factuality_min: 0.9` el gate g4 marca `false` y `closeable: false`; con `factuality_min` ausente, g4 no se evalúa y el comportamiento es idéntico al actual.

**Acceptance Scenarios**:

1. **Given** un `claims.md` con afirmaciones de soporte mixto, **When** se ejecuta `status.py --json`, **Then** la salida incluye `factuality_global` (float 0–1), `factuality_by_chapter` (por ordinal) y `gates.factuality` (bool o `null` si no hay umbral).
2. **Given** un manifest con `quality_gates.factuality_min`, **When** la factualidad global o la de algún capítulo cae por debajo del umbral, **Then** `gates.factuality == false` y `closeable == false`; `status.py --gate` sale con código 1.
3. **Given** un manifest **sin** `quality_gates`, **When** se ejecuta `status.py`, **Then** g4 no se evalúa (`gates.factuality == null`), `closeable` se calcula como hoy (g1·g2·g3) y ninguna salida ni gate previo cambia (retrocompatibilidad).
4. **Given** un umbral configurado en modo aviso (`quality_gates.factuality_mode: "advisory"`), **When** la factualidad cae por debajo, **Then** se reporta el déficit en el dashboard pero `closeable` NO se bloquea por g4.

---

### User Story 4 — Transparencia con la capa de orquestación (Priority: P2)

El cambio no introduce tipos de tarea, routines ni estados nuevos de Paperclip, ni altera el fan-out, el ciclo peer-to-peer, los wakes ni los checkpoints humanos. La Documentalista sigue siendo la dueña de la pasada 4 y la decisora del ciclo; solo cambia su "cómo". La Editora jefa sigue obedeciendo `closeable`/`--gate` sin reescribir su HEARTBEAT.

**Why this priority**: es un requisito transversal de no-regresión, no una capacidad nueva. Se verifica al final.

**Independent Test**: ejecutar el flujo Paperclip de extremo a extremo en el Project de prueba (`guide-nlp`) con la feature activa y comprobar que (a) la jefa hace el mismo fan-out único; (b) la Documentalista escribe `claims.md` + `findings.md` y decide APPROVED/NEEDS_REVISE igual que antes; (c) el gate de factualidad, si está configurado, bloquea el `close` por la vía de `status.py --gate` que la jefa ya consulta; (d) no se usan APIs de Paperclip fuera de las permitidas en `FLOW-CONTRACT.md` §4/§5.

**Acceptance Scenarios**:

1. **Given** la feature activa, **When** la jefa corre `status.py --json` en su heartbeat, **Then** los campos nuevos (`factuality_*`, `gates.factuality`) son **aditivos** y los campos existentes (`next_step`, `by_chapter`, `all_chapters_approved`, etc.) conservan nombre y semántica.
2. **Given** un déficit de factualidad expresado como findings `critico`/`medio` (vía US2), **When** la jefa evalúa el cierre, **Then** `revise_pending` ya captura los accionables y `by_chapter.approved` ya se bloquea, sin tocar la fórmula de `_build_by_chapter`.

---

### Edge Cases

- **`claims.md` ausente** (capítulo nunca pasó por pasada 4 con la feature activa): `status.py` trata su factualidad como "no medida" (no como 0). No bloquea por g4 un capítulo sin claims; el gate de completitud/críticos sigue rigiendo. Documentar el estado "no medido" en el dashboard.
- **Afirmación con múltiples fuentes de relación divergente** (una `apoya`, otra `contradice`): prevalece la peor relación para la severidad (`contradice` > `menciona`/`sin_fuente` > `matiza` > `apoya`); el `ClaimRecord` registra todas las aristas.
- **Sin acceso a web en la pasada 4**: para datos volátiles, `relacion` no puede confirmarse en vivo → `soporte: pendiente`, finding `medio` "no verificado en vivo" (comportamiento actual preservado); estas afirmaciones cuentan como **no soportadas** en el índice de factualidad y se reportan aparte para no penalizar de forma opaca.
- **Afirmación no verificable** (opinión editorial, transición, didáctica): NO genera `ClaimRecord` ni entra en el denominador de factualidad. La heurística de detección de afirmaciones verificables es la misma que ya usa `writeonmars-contraste`.
- **Conflicto Redactora↔export por la sección "Fuentes"**: ver decisión obligatoria en `plan.md` § "Decisión D1". Hasta que se resuelva, `claims.md` **valida** la sección existente; no la sobrescribe.

---

## Requirements *(mandatory)*

### Functional Requirements

**Contrato y modelo de datos**

- **FR-001**: El sistema MUST definir un contrato `ClaimRecord` v1.0 en `contracts/claim-record.schema.json`, espejado en `writeonmars/contracts/`, aditivo y sin romper el contrato de citación v1.0. Estructura canónica en `data-model.md` § 1.
- **FR-002**: Cada `ClaimRecord` MUST referenciar afirmaciones por **cita literal anclada** (`frase`) y enlazar a fuentes vía `evidencia[]`, donde cada entrada lleva `citation_id`, `relacion`, `cita_fragmento_soporte` y `confianza_match`. El `citation_id` MUST existir en el `research.md` del proyecto.
- **FR-003**: El sistema MUST definir el enum `relacion` cerrado: `apoya | matiza | contradice | menciona`. Una entrada `relacion: apoya` MUST tener `cita_fragmento_soporte` no vacío (la oración de la fuente que sostiene la afirmación).
- **FR-004**: El sistema MUST definir el enum `soporte` del `ClaimRecord`: `soportado | parcial | sin_fuente | contradicho | pendiente`. Reglas de derivación de `soporte` a partir de `evidencia[]` en `data-model.md` § 1.3.

**Pasada 4 (referencia agnóstica + bundle del rol)**

- **FR-005**: La pasada 4 MUST persistir un `ClaimRecord` por **cada** afirmación verificable evaluada (no solo las que fallan), en `specs/<###-feature>/claims.md`, agrupados por capítulo.
- **FR-006**: La pasada 4 MUST, tras abrir la fuente (en vivo para datos volátiles), clasificar la `relacion` de cada cita con la afirmación y registrar el fragmento de soporte. Sin acceso a web, los datos volátiles quedan `soporte: pendiente` y NO se finge la verificación.
- **FR-007**: La regeneración de `claims.md` MUST ser idempotente por capítulo: re-ejecutar la pasada 4 sobre un capítulo reemplaza sus `ClaimRecord` sin duplicarlos ni tocar los de otros capítulos.
- **FR-008**: La pasada 4 MUST seguir emitiendo el bloque "Pasada 4" en `findings.md` conforme a `pass-output-schema` (ahora v1.1), con la severidad derivada de la tabla de § "Mapeo de severidad". La feature NO elimina ningún campo existente del esquema de findings.

**Mapeo de severidad (findings ↔ relacion/soporte)**

- **FR-009**: El sistema MUST mapear el veredicto a severidad así, enchufándose a la lógica de revise existente (crítico+medio = accionable; bajo = aviso):
  - `contradicho` (cualquier afirmación) → `critico`.
  - `sin_fuente` o `menciona`-solo en un **dato duro** (versión, comando, precio, estándar, estadística, fecha) → `critico`.
  - `parcial` / `matiza`, o `sin_fuente` en una afirmación blanda verificable → `medio`.
  - dato volátil `pendiente` por falta de web → `medio` ("no verificado en vivo").
  - ambigüedad de mapeo afirmación↔cita → `bajo` (aviso).

**Núcleo determinista (`status.py`)**

- **FR-010**: `status.py` MUST parsear `claims.md` (parser análogo a `parse_findings`) y calcular `factuality_by_chapter` y `factuality_global` = afirmaciones con `soporte == soportado` / afirmaciones verificables totales (excluyendo `pendiente` del numerador; ver `data-model.md` § 3 para el tratamiento exacto del denominador). El cálculo MUST ser determinista y sin invocar ningún modelo.
- **FR-011**: `status.py --json` MUST exponer los campos nuevos de forma **aditiva**: `factuality_global` (float|null), `factuality_by_chapter` (objeto por ordinal), `factuality_unmeasured` (lista de capítulos sin `claims.md`), y `gates.factuality` (bool|null). Ningún campo existente cambia de nombre ni semántica.
- **FR-012**: `status.py` MUST evaluar el gate g4 SOLO si el manifest declara `quality_gates.factuality_min`. g4 = `factuality_global >= min` Y ningún capítulo medido por debajo de su piso. Con `quality_gates` ausente, `gates.factuality == null` y `closeable` se calcula como hoy (g1·g2·g3).
- **FR-013**: `status.py` MUST soportar `quality_gates.factuality_mode: "advisory" | "blocking"` (default `blocking` cuando hay umbral). En `advisory`, el déficit se reporta pero NO bloquea `closeable`.

**Manifest y versionado**

- **FR-014**: `manifest-schema.json` MUST añadir un objeto opcional `quality_gates` (`factuality_min`: number 0–1; `factuality_min_per_chapter`: number 0–1 opcional; `factuality_mode`: enum). Como el manifest tiene `additionalProperties: false`, esto es un bump MINOR del schema del manifest, espejado en ambas copias del contrato.
- **FR-015**: El sistema MUST versionar los cambios de contrato: `claim-record.schema.json` v1.0 (nuevo); `pass-output-schema.md` → v1.1 (MINOR, añade la tabla de claims y el comentario de versión); `manifest-schema.json` → MINOR; constitución → bump MINOR (añade requisito de atribución por afirmación + gate de factualidad, conserva "Fuentes por capítulo" derivándola).

**Exportación y "Fuentes por capítulo"**

- **FR-016**: `export.py` MUST, como mínimo, **validar** la sección "Fuentes por capítulo" de cada capítulo contra `claims.md` (toda fuente citada en el cuerpo aparece en claims; ninguna afirmación `sin_fuente`/`contradicho` queda en el PDF sin marca). La decisión "validar vs generar" se resuelve en `plan.md` § "Decisión D1" antes de implementar.

**Neutralidad y transparencia (no-regresión)**

- **FR-017**: Todo juicio de relación/soporte MUST vivir en la referencia agnóstica `writeonmars-contraste/SKILL.md` (y reflejarse en el `bundle.md` de la Documentalista); ningún juicio puede vivir en `status.py`. Todo conteo MUST vivir en `status.py`; ningún conteo en la skill. (Principio VI: neutralidad de agente y modelo.)
- **FR-018**: La feature MUST NOT introducir tipos de tarea, routines ni estados de Paperclip nuevos, ni modificar el fan-out, el ciclo peer-to-peer, los wakes o los checkpoints humanos descritos en `FLOW-CONTRACT.md`. `claims.md` es un archivo más del workspace, aislado por worktree como `findings.md`.
- **FR-019**: La feature MUST preservar la funcionalidad sin Paperclip: el gate de factualidad MUST funcionar para el runner de un solo agente vía `status.py --gate`.

**Tests**

- **FR-020**: El sistema MUST proveer `tests/lib/validate-claim.sh` (gemelo de `validate-citation.sh`) que valide un `ClaimRecord` contra `claim-record.schema.json`.
- **FR-021**: El sistema MUST proveer un smoke test que corra `status.py --json` contra fixtures `findings.md` + `claims.md` y verifique el índice de factualidad, el comportamiento de g4 (presente/ausente, advisory/blocking) y la retrocompatibilidad de los campos existentes.

### Key Entities

- **ClaimRecord**: representa una afirmación verificable de un capítulo y su evidencia. Atributos clave: `claim_id`, `capitulo`, `frase` (cita literal anclada), `tipo_afirmacion`, `evidencia[]` (aristas a fuentes con `relacion` y fragmento de soporte), `soporte` (veredicto derivado), `verificado_en_vivo` + `url_verificada` + `fecha_verificacion`. Vive en `specs/<###-feature>/claims.md`. Relación 1:N con `CitationRecord` vía `evidencia[].citation_id`.
- **Arista de evidencia** (`evidencia[]` dentro de `ClaimRecord`): el vínculo contextual afirmación↔fuente. La `relacion` es propiedad de la **arista**, no de la fuente (la misma fuente puede apoyar una afirmación y solo mencionar otra). Esta es la diferencia de modelado clave frente a meter el veredicto en `CitationRecord`.
- **Índice de factualidad**: métrica derivada (no almacenada como fuente de verdad; recomputable por `status.py` desde `claims.md`). Por capítulo y global.
- **quality_gates** (en el manifest): configuración opcional del gate g4. Cache de política, no de datos.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Tras la pasada 4 sobre un capítulo, el 100% de las afirmaciones verificables detectadas tiene un `ClaimRecord` válido contra el esquema (no solo las que fallan).
- **SC-002**: `status.py --json` emite `factuality_global` y `factuality_by_chapter` con error 0 respecto al cálculo manual sobre los mismos `claims.md` de fixture (determinismo verificable).
- **SC-003**: Con la feature desactivada (sin `quality_gates`, sin `claims.md`), la salida de `status.py` y los gates g1·g2·g3 son **idénticos byte-a-byte** a los de la versión previa para los mismos inputs (retrocompatibilidad demostrada).
- **SC-004**: En el flujo Paperclip de extremo a extremo, el número de tipos de tarea, estados y routines usados es el mismo que antes de la feature (0 nuevos); verificable contra `FLOW-CONTRACT.md` §4/§5.
- **SC-005**: Sobre un set de fixtures con relación conocida, la severidad emitida por la pasada 4 coincide con la tabla de FR-009 en el 100% de los casos.
- **SC-006**: Una afirmación cuya fuente solo `menciona` un dato duro deja de contar como soportada (cambio medible frente al baseline, donde "tiene cita" bastaba): el índice de factualidad del fixture correspondiente baja respecto al cálculo ingenuo "tiene_cita / total".

---

## Assumptions

- La heurística de detección de "afirmaciones verificables" existente en `writeonmars-contraste` es suficiente como denominador v1; la descomposición en afirmaciones **atómicas** estilo FActScore puro (una sub-frase por hecho) se considera refinamiento v2 (ver `research.md` § "Qué queda fuera").
- La clasificación de `relacion` la produce el modelo de la pasada 4, que el método ya manda correr en un modelo distinto al de redacción y con acceso a web. La calidad del veredicto es dependiente del modelo; el contrato fija el formato, no la exactitud del juicio.
- "Attribute First, then Generate" real (la Redactora selecciona la fuente antes de escribir y ancla inline) queda **fuera de v1** por su impacto en la voz/didáctica (diferencial del producto). v1 hace "atribuir-y-persistir tras escribir". Las anclas inline en prosa son opcionales y se especifican como extensión.
- `claims.md` se ubica junto a `findings.md` en `specs/<###-feature>/` y se versiona en git como el resto del estado; no requiere almacenamiento externo.
- La calibración del umbral `factuality_min` se hará contra una guía de referencia (p. ej. `guide-ai-developers-basic` / `guide-nlp`) y arrancará en modo `advisory` antes de promoverse a `blocking`, replicando cómo la constitución relajó estándares calibrando contra una guía real.

## Out of scope (v1)

- Reescritura del flujo de redacción hacia "Attribute First" con selección de fuente previa.
- Anclas de cita inline en la prosa renderizadas como notas (extensión opcional, descrita pero no exigida).
- Descomposición atómica sub-oracional estilo FActScore/VeriScore puro.
- Verificación NLI automatizada por modelo clasificador dedicado (la relación la juzga el modelo de la pasada 4, no un clasificador NLI separado).
- Cualquier cambio en pasadas 1·2·3·5 o en los roles Redactora/Editora de mesa más allá de la decisión D1 sobre la sección "Fuentes".
