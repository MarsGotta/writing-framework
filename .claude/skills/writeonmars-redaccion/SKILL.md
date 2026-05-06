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

Modo serial por defecto. El modo `--parallel N` se añadirá en T062 (US3):
NO está implementado en esta versión.

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

## Modo paralelo (no implementado en esta versión)

`--parallel N` se entrega en T062 (US3). Hasta entonces, los capítulos
se redactan en serie para preservar coherencia del hilo conductor con el
glosario evolucionando.

## FR cubierta

- FR-014 (sub-agente fresco por capítulo).
- FR-015 (anexo de glosario para consolidación).

## Versión

v0.1.0-mvp — 2026-05-06
