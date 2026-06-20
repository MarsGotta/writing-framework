---
name: writeonmars-pasada-2
description: Pasada 2 (utilidad) sobre un capítulo o sobre la guía completa. Envuelve /technical-guide-design y aplica la lente del Principio V.2. Trigger cuando la persona diga "pasada 2", "revisa la utilidad", "valida los ejemplos por concepto", "review de checklists y errores comunes".
allowed-tools: Bash, Read, Write, Edit, Skill, Agent
---

# writeonmars-pasada-2

Skill que materializa la pasada 2 (utilidad) del Principio V.2. Envuelve
`/technical-guide-design` con la lente de operatividad: ejemplos por
concepto, acción práctica por capítulo, checklists, errores comunes,
síntomas reales, criterios de éxito. Emite "Pasada 2" en `findings.md` y
checklist en `checklists/[###-feature]/pasada-2.md`.

## Cuándo dispararse

- "pasada 2"
- "revisa la utilidad"
- "valida los ejemplos por concepto"
- "review de checklists y errores comunes"
- Tras pasar la pasada 1 sin críticos abiertos.

## Qué hace

1. Despacha un sub-agente con `agents/claude/prompts/pasada-2.md`.
2. El sub-agente revisa el capítulo aplicando la lente de Principio V.2.
3. Emite bloque "Pasada 2 — Utilidad" en `findings.md` y checklist
   firmable en `checklists/[###-feature]/pasada-2.md`.
4. Aplica `signing_matrix.pasada_2_utilidad`. Default v1: `autonomous`.

## Inputs

- `chapters/[###]-titulo.md`.
- `specs/[###-feature]/spec.md`, `plan.md`, `glossary.md`,
  `findings.md`.
- `agents/claude/prompts/pasada-2.md`.
- `.specify/templates/checklist-template.md` § "Pasada 2 — Utilidad".

## Outputs

- Bloque "Pasada 2 — Utilidad" añadido a `findings.md`.
- `checklists/[###-feature]/pasada-2.md` con firma.

## Procedimiento

Idéntico al de pasada 1, sustituyendo prompt y plantilla.

## Lente específica (constitución § V.2)

- Cada concepto técnico tiene al menos un ejemplo concreto en el
  capítulo.
- Acción práctica y checklist **según lo declaren las adendas del proyecto**: por
  capítulo, o centralizados en el cierre y los anexos (p. ej. tecnología los
  centraliza). No exijas checklist por capítulo si el sector lo relaja.
- Cajas visuales ("Quédate con esto", "Qué hacer mañana", "Síntoma → causa
  probable") **solo si las adendas las declaran obligatorias** para el sector. No
  son obligatorias por defecto (constitución § Estándares editoriales, v1.3.0).
- Errores frecuentes con síntoma y causa probable, no abstracciones.
- Criterios de éxito explícitos cuando aplica.

## Default signing

`autonomous` (signing_matrix v1).

## Errores comunes

- Capítulo sin caja visual: finding `severidad: medio`, fix sugerido en
  pasada 5.
- Acción práctica genérica ("aplicá lo aprendido"): finding crítico.
- Conceptos técnicos sin ejemplo: finding crítico, bloquea cierre.

## FR cubierta

- FR-018, FR-019.
- Constitución § V.2.

## Versión

v0.1.0-mvp — 2026-05-06
