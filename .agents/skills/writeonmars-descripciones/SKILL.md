---
name: writeonmars-descripciones
description: Encadena las descripciones de cada capítulo (promesa, conexión anterior/siguiente, ejemplo recurrente aplicado, conceptos introducidos) envolviendo /technical-guide-design. Trigger cuando la persona diga "encadena las descripciones", "hilo conductor entre capítulos", "diseña las transiciones", "/speckit-plan descripciones".
allowed-tools: Bash, Read, Write, Edit, Skill
---

# writeonmars-descripciones

Skill que produce el hilo conductor entre capítulos. Por cada entrada del
temario emite una descripción encadenada que respeta el formato de
data-model.md §5: promesa específica, conexión anterior, conexión siguiente,
ejemplo recurrente aplicado, conceptos introducidos. Garantiza que `null`
solo aparezca en los bordes (capítulo 1 y último).

## Cuándo dispararse

- "encadena las descripciones"
- "hilo conductor entre capítulos"
- "diseña las transiciones"
- "/speckit-plan descripciones"
- Tras `writeonmars-temario`, cuando `plan.md` ya tiene `## Temario` pero
  todavía no `## Descripciones encadenadas`.

## Qué hace

1. Lee el temario aprobado y el brief.
2. Invoca `/technical-guide-design` con un prompt centrado en arquitectura
   de transiciones: cada capítulo abre desde donde cierra el anterior,
   cierra preparando el siguiente, aplica el ejemplo recurrente y
   declara explícitamente los conceptos que introduce.
3. Produce una descripción por capítulo con los seis campos de
   data-model.md §5.
4. Valida que `conexion_anterior = null` solo aparezca en el capítulo 1
   y `conexion_siguiente = null` solo en el último.
5. Verifica que el ejemplo recurrente se aplique en al menos 80% de los
   capítulos (SC-005); reporta como warning los capítulos donde no
   aplica naturalmente y exige nota de excepción.
6. Renderiza la sección `## Descripciones encadenadas` en
   `specs/[###-feature]/plan.md` entre marcadores
   `<!-- descripciones-start -->` y `<!-- descripciones-end -->`.

## Inputs

- `specs/[###-feature]/plan.md` — sección "Temario" (entrada).
- `specs/[###-feature]/spec.md` — brief, especialmente
  `ejemplo_recurrente`.
- `specs/[###-feature]/research.md` — para vincular conceptos
  introducidos con citas.
- Skill bundled: `/technical-guide-design`.

## Outputs

- Sección `## Descripciones encadenadas` en `plan.md` con bloque por
  capítulo.

## Procedimiento

1. Cargar el temario completo. Si tiene menos de un capítulo, abortar.
2. Para cada capítulo, redactar:
   - `promesa_especifica`: refina la promesa del temario sin contradecirla.
   - `conexion_anterior`: una o dos frases explicando desde dónde llega
     el lector. `null` solo en capítulo 1.
   - `conexion_siguiente`: una o dos frases preparando la próxima
     entrega. `null` solo en el último.
   - `ejemplo_recurrente_aplicado`: cómo se usa el ejemplo del brief en
     este capítulo. Si no aplica, declarar la nota de excepción.
   - `conceptos_introducidos`: lista de términos nuevos que entrarán al
     glosario consolidado vía `writeonmars-glossary`.
3. Validar el bloque entero contra el schema de data-model.md §5.
4. Persistir en `plan.md` y emitir resumen: total de capítulos, capítulos
   sin ejemplo recurrente aplicado, conceptos nuevos por capítulo.

## Errores comunes

- Conexiones rotas: la descripción siguiente del capítulo N no se
  corresponde con la descripción anterior del capítulo N+1. La skill lo
  detecta comparando ambos campos y bloquea hasta resolver.
- `null` en el medio de la guía: error crítico, no se persiste.
- Conceptos introducidos repetidos entre capítulos: warning;
  `writeonmars-glossary` arbitrará en una pasada posterior.
- Ejemplo recurrente forzado: la skill prefiere una nota de excepción
  honesta antes que un encaje artificial.

## FR cubierta

- FR-010 (descripciones encadenadas explícitas en el plan).
- SC-005 (ejemplo recurrente aplicado en ≥ 80% de los capítulos).

## Versión

v0.1.0-mvp — 2026-05-06
