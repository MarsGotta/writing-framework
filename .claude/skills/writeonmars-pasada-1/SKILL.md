---
name: writeonmars-pasada-1
description: Pasada 1 (estructura) sobre un capítulo o sobre la guía completa. Envuelve /technical-guide-design y aplica la lente del Principio V.1. Trigger cuando la persona diga "pasada 1", "revisa la estructura", "valida la promesa de los capítulos", "review estructural".
allowed-tools: Bash, Read, Write, Edit, Skill, Agent
---

# writeonmars-pasada-1

Skill que materializa la pasada 1 (estructura) del Principio V de la
constitución. Envuelve `/technical-guide-design` con una lente
específica: promesa clara, audiencia explícita, función de cada
capítulo, progresión lógica, acción final. Emite el bloque "Pasada 1" en
`findings.md` y la checklist firmable
`checklists/[###-feature]/pasada-1.md`.

## Cuándo dispararse

- "pasada 1"
- "revisa la estructura"
- "valida la promesa de los capítulos"
- "review estructural"
- Tras redactar un capítulo, antes de pasada 2.

## Qué hace

1. Despacha un sub-agente fresco con el prompt
   `agents/claude/prompts/pasada-1.md`.
2. El sub-agente invoca `/technical-guide-design` con la lente de
   estructura del Principio V.1.
3. Recoge la salida en formato `pass-output-schema` v1.0:
   - Bloque markdown añadido al final de
     `specs/[###-feature]/findings.md`.
   - Checklist firmable en
     `checklists/[###-feature]/pasada-1.md` (extraída del template
     editorial).
4. Aplica la `signing_matrix` del manifiesto. Default v1: pasada 1 =
   `autonomous`. La firma se rellena automáticamente con el id del
   sub-agente y la fecha actual.
5. Reporta al operador: `estado_pasada` (`passed` |
   `passed-with-warnings` | `blocked`), número de hallazgos por
   severidad y rutas de ambos archivos producidos.

## Inputs

- `chapters/[###]-titulo.md` (capítulo objetivo) o todos los capítulos
  cuando se invoca con alcance global.
- `specs/[###-feature]/spec.md`, `plan.md`, `glossary.md`.
- `specs/[###-feature]/findings.md` (existente; se añaden bloques al
  final).
- `agents/claude/prompts/pasada-1.md`.
- `.specify/templates/checklist-template.md` § "Pasada 1 — Estructura".

## Outputs

- Bloque "Pasada 1 — Estructura" añadido a `findings.md`.
- `checklists/[###-feature]/pasada-1.md` con items marcados y firma.

## Procedimiento

1. Resolver la rama feature y el capítulo objetivo (o `global`).
2. Cargar el capítulo y los anexos relevantes (descripciones contiguas,
   glosario, brief).
3. Despachar el sub-agente. Adjuntar como system prompt el contenido
   completo de `agents/claude/prompts/pasada-1.md` y como mensaje
   inicial los archivos a revisar.
4. Validar la salida del sub-agente contra el schema:
   - Tabla de hallazgos con seis campos por fila.
   - `pasada: 1_estructura`.
   - `firma.tipo` coherente con la matriz.
5. Añadir el bloque al final de `findings.md` (sin sobreescribir
   bloques previos).
6. Materializar la checklist a partir de la plantilla editorial,
   marcando solo los items con evidencia.
7. Imprimir resumen.

## Lente específica (constitución § V.1)

- Promesa clara y reconocible al abrir el capítulo.
- Audiencia explícita; el capítulo no cambia de público.
- Función de cada capítulo dentro de la guía completa.
- Progresión lógica respecto a las descripciones encadenadas.
- Acción final: cada sección o capítulo cierra en una decisión, una
  advertencia o una acción concreta.

## Default signing

`autonomous` (signing_matrix v1).

## Errores comunes

- `findings.md` ausente: la skill lo crea con encabezado.
- Sub-agente que devuelve la tabla con menos de seis columnas: la skill
  rechaza y reintenta una vez.
- Items de la checklist marcados sin evidencia: la skill desmarca y
  reporta.

## FR cubierta

- FR-018, FR-019 (formato unificado de findings).
- Constitución § V.1.

## Versión

v0.1.0-mvp — 2026-05-06
