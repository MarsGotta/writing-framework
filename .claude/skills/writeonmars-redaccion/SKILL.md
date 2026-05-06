---
name: writeonmars-redaccion
description: Redacta un capítulo de la guía despachando un sub-agente con el prompt canónico de redacción. El sub-agente invoca /technical-guide-design para arquitectura y /marcela-prose para voz. Trigger cuando la persona diga "redacta el capítulo N", "produce el capítulo objetivo", "escribe la guía", "redacta capítulo".
allowed-tools: Bash, Read, Write, Edit, Agent
---

# writeonmars-redaccion

Skill orquestadora que despacha un sub-agente fresco por capítulo.
Materializa FR-014 y FR-015 (en su parte de generación). El sub-agente
recibe el prompt canónico de `agents/claude/prompts/redaccion.md` y el
contexto mínimo necesario; invoca `/technical-guide-design` para la
arquitectura del capítulo y `/marcela-prose` para la voz. Devuelve
`chapters/[###]-titulo.md` con front-matter YAML y anexo de términos
nuevos para alimentar a `writeonmars-glossary`.

Modo serial por defecto. El modo `--parallel N` (US3 / T062) habilita
despacho concurrente de sub-agentes; ver § "Modo paralelo (`--parallel N`)".

## Cuándo dispararse

- "redacta el capítulo N"
- "produce el capítulo objetivo"
- "escribe la guía"
- "redacta capítulo"
- Tras `writeonmars-descripciones`, cuando un capítulo del temario
  todavía no tiene su archivo en `chapters/`.

## Qué hace

1. Identifica el capítulo objetivo desde el argumento del operador o
   desde el primer capítulo del temario sin redactar.
2. Carga el contexto mínimo:
   - Brief (`specs/[###-feature]/spec.md`).
   - Temario y descripción objetivo (`plan.md`).
   - Descripciones contiguas (capítulo anterior y siguiente, si
     existen).
   - Ejemplo recurrente del brief.
   - Glosario consolidado (`specs/[###-feature]/glossary.md` y/o
     `glossary.md` raíz).
   - Constitución (los cinco principios y los Estándares editoriales).
3. Despacha un sub-agente con la herramienta Agent (Claude Code,
   `subagent_type: general-purpose`). El system prompt del sub-agente es
   el contenido completo de `agents/claude/prompts/redaccion.md`.
4. El sub-agente produce `chapters/[###]-titulo.md` con front-matter YAML
   (data-model.md §7) y anexo de glosario en bloque
   `<!-- glossary-annex START -->` … `<!-- glossary-annex END -->`.
5. Tras recibir el archivo, esta skill verifica:
   - Front-matter YAML sintácticamente válido.
   - Las nueve secciones obligatorias en orden.
   - Anexo de glosario presente.
   - `terminos_introducidos` del front-matter coincide con el anexo.
6. Si la verificación falla, NO persiste; reporta el bloqueo y deja el
   archivo en `chapters/[###]-titulo.draft.md` para inspección.

## Inputs

- `specs/[###-feature]/spec.md` — brief.
- `specs/[###-feature]/plan.md` — temario y descripciones encadenadas.
- `specs/[###-feature]/glossary.md` o `glossary.md` raíz.
- `agents/claude/prompts/redaccion.md` — prompt canónico (vía T047).
- `.specify/memory/constitution.md`.

## Outputs

- `chapters/[###]-titulo.md` con front-matter, nueve secciones y anexo
  de glosario.

## Procedimiento

1. Determinar `capitulo_numero` y `titulo` desde el temario.
2. Calcular el slug del título (kebab-case sin acentos, sin emoji) para
   formar el nombre de archivo `chapters/[###]-<slug>.md`.
3. Componer el contexto mínimo en un payload markdown que se pase al
   sub-agente como mensaje inicial. Adjuntar también el prompt canónico
   como system prompt del sub-agente.
4. Despachar el sub-agente serialmente (un capítulo a la vez en esta
   versión).
5. Recibir la salida del sub-agente y validar.
6. Persistir el capítulo en `chapters/[###]-<slug>.md`.
7. Tras persistir, sugerir al operador correr `writeonmars-glossary`
   para consolidar los términos nuevos.

## Errores comunes

- Sub-agente devuelve un capítulo sin alguna de las nueve secciones: se
  guarda como `.draft.md` y se reporta.
- Front-matter YAML inválido: se reporta línea por línea.
- Términos del anexo que no figuran en `terminos_introducidos`: se
  rechaza el archivo y se solicita reintento.
- Capítulo que no usa el ejemplo recurrente sin nota de excepción:
  warning de SC-005.

## Modo paralelo (`--parallel N`)

Activación con la bandera `--parallel N`, donde N ∈ [2, 8]. Sin la
bandera, la skill mantiene el modo serial (default histórico). El modo
paralelo despacha hasta N sub-agentes concurrentemente vía la herramienta
Agent de Claude Code en una sola llamada con múltiples invocaciones.

### Mecanismo

1. Identifica todos los capítulos pendientes (sin archivo en `chapters/`
   o marcados como `.draft.md`). Solo capítulos NO redactados se
   distribuyen.
2. Decide el reparto:
   - Si `pendientes ≤ N`: cada sub-agente toma 1 capítulo.
   - Si `pendientes > N`: round-robin en lotes secuenciales hasta
     agotar la cola. Cada lote dispara N sub-agentes en paralelo y
     espera la última respuesta antes de iniciar el siguiente lote.
3. Compone el contexto compartido (idéntico para todos los sub-agentes
   del mismo lote): brief, temario completo, glosario consolidado al
   inicio del lote, descripciones encadenadas (anterior y siguiente
   por capítulo objetivo), constitución, ejemplo recurrente del brief.
4. En una única llamada del orquestador, despacha N invocaciones de la
   herramienta Agent (`subagent_type: general-purpose`). Cada invocación
   recibe:
   - System prompt: contenido completo de
     `agents/claude/prompts/redaccion.md` (idéntico al modo serial).
   - Mensaje inicial: payload markdown con el capítulo objetivo
     específico de ese sub-agente más el contexto compartido.
5. Cada sub-agente escribe SOLO a su archivo de capítulo
   (`chapters/[###]-<slug>.md`). No hay shared writes ni mutación
   concurrente del glosario.
6. Tras la última tanda, el orquestador recibe los N archivos, los
   valida individualmente (front-matter, secciones, anexo) y persiste
   los que pasan; los que fallan quedan como `.draft.md`.
7. Una vez cerrados todos los lotes, recomienda invocar
   `writeonmars-glossary` para consolidar los anexos y detectar
   colisiones (ver T064 y FR-015).

### Mapeo capítulo → sub-agente

```
pendientes = [cap_a, cap_b, cap_c, cap_d]
N = 2
lote_1: sub-agente A → cap_a, sub-agente B → cap_b   (paralelo)
lote_2: sub-agente A → cap_c, sub-agente B → cap_d   (paralelo)
```

Round-robin para que cada sub-agente vea capítulos contiguos del
temario y aproveche el contexto reciente de su lote anterior. El
glosario consolidado se refresca entre lotes (no en mitad de un lote).

### Reglas

- Cada sub-agente recibe el mismo prompt canónico
  (`agents/claude/prompts/redaccion.md`) sin alteraciones.
- El glosario que recibe cada sub-agente es la versión consolidada al
  inicio del lote: dos capítulos del mismo lote pueden introducir
  términos colisionantes; eso lo detecta `writeonmars-glossary` después
  (FR-015). El paralelismo no degrada la detección, solo la difiere
  hasta el cierre del lote.
- Si un sub-agente falla (timeout, validación, error de la herramienta
  Agent), el orquestador reintenta ese capítulo en serie tras cerrar
  el lote para no demorar el resto.
- Si la validación post-redacción de un capítulo falla, queda como
  `.draft.md` igual que en modo serial.

### Cuándo usar paralelo

- Guías con ≥ 4 capítulos donde cada capítulo tarda ≥ 10 minutos en el
  modelo objetivo.
- Capítulos cuya dependencia secuencial sea suave (descripciones
  encadenadas bien diseñadas, ejemplo recurrente compartido).
- Recursos disponibles: cuotas, latencia y costo del modelo objetivo
  permiten N invocaciones concurrentes.

### Cuándo evitarlo

- Guías cortas (≤ 3 capítulos): el overhead de dispatch suele superar
  la ganancia.
- Capítulos con dependencia fuerte secuencial (un capítulo construye
  artefactos que el siguiente referencia explícitamente). Suele
  indicar que las descripciones encadenadas necesitan más diseño antes
  que paralelismo.
- Operador que quiere control fino capítulo a capítulo (revisión
  intermedia entre capítulos).
- Cuotas de modelo limitadas o latencia tan alta que el dispatch
  paralelo introduce contención más que aceleración.

Documentación operativa completa en `docs/parallel-execution.md`.

## FR cubierta

- FR-014 (sub-agente fresco por capítulo, serial o paralelo).
- FR-015 (anexo de glosario para consolidación; colisiones detectadas
  por `writeonmars-glossary` tras el cierre del lote paralelo).

## Versión

v0.2.0-mvp-2026-05-06 — añade modo `--parallel N` (T062).
v0.1.0-mvp — 2026-05-06.
