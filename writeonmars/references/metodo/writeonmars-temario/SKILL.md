---
name: writeonmars-temario
description: Diseña la lista de capítulos de la guía envolviendo /technical-guide-design y emite la sección "Temario" en plan.md. Trigger cuando la persona diga "diseña el temario", "estructura los capítulos", "arma el índice", "/speckit-plan temario".
allowed-tools: Bash, Read, Write, Edit, Skill
---

# writeonmars-temario

Skill que materializa el Principio II (estructura situación → explicación →
consecuencia) y FR-010. Envuelve `/technical-guide-design` para producir un
temario que respeta la promesa del brief y la audiencia declarada. Emite la
sección "Temario" dentro de `specs/[###-feature]/plan.md`.

## Cuándo dispararse

- "diseña el temario"
- "estructura los capítulos"
- "arma el índice"
- "/speckit-plan temario"
- Tras `writeonmars-research` cuando `plan.md` aún no tiene la sección
  "Temario".

## Qué hace

1. Lee el brief y la investigación para entender promesa, audiencia,
   conceptos obligatorios y ejemplo recurrente.
2. Invoca `/technical-guide-design` con un prompt enfocado al diseño de
   lista de capítulos: estructura ordenada según Diátaxis y andragogía,
   carga cognitiva por capítulo, función explícita de cada uno.
3. Mapea el resultado al esquema de data-model.md §4: cada capítulo tiene
   `numero`, `titulo`, `promesa`, `estructura_aplicada` (default
   `didactica_v1`).
4. Renderiza la sección "Temario" en `specs/[###-feature]/plan.md` con un
   bloque markdown encabezado `## Temario` y una tabla o lista numerada.
5. Verifica que el número total de capítulos sea coherente con la promesa
   del brief y advierte cuando el temario excede 12 capítulos sin
   justificación (riesgo de carga cognitiva).

## Inputs

- `specs/[###-feature]/spec.md` — brief.
- `specs/[###-feature]/research.md` — fuentes y conceptos cubiertos.
- `.specify/memory/constitution.md` — Principio II.
- Skill bundled: `/technical-guide-design`.

## Outputs

- Sección `## Temario` en `specs/[###-feature]/plan.md`.

## Procedimiento

1. Verificar prerrequisitos: `spec.md` con brief completo y `research.md`
   con citas. Si falta cualquiera, detener y reportar.
2. Construir el prompt para `/technical-guide-design` incluyendo:
   audiencia, promesa de la guía, conceptos obligatorios, ejemplo
   recurrente, riesgos.
3. Recibir la propuesta de capítulos. Validar que cada capítulo declare
   título claro, promesa específica y función operativa.
4. Renderizar el bloque "Temario" en `plan.md` entre marcadores
   `<!-- temario-start -->` y `<!-- temario-end -->` para que
   `writeonmars-descripciones` y posteriores ediciones puedan reescribirlo
   sin colisionar con el resto del plan.
5. Si `plan.md` no existe, crearlo desde la plantilla
   `.specify/templates/plan-template.md`.

## Errores comunes

- Capítulos con títulos vacíos o promesas vagas: la skill bloquea y exige
  reintento.
- Promesas que se solapan entre capítulos: warning y propuesta de
  consolidación.
- Faltan conceptos obligatorios del brief en el temario: error crítico,
  no se persiste hasta cubrirlos.

## FR cubierta

- FR-010 (temario explícito en el plan).
- Constitución § II (estructura didáctica).

## Versión

v0.1.0-mvp — 2026-05-06
