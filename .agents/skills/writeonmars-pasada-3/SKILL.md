---
name: writeonmars-pasada-3
description: Pasada 3 (naturalidad) sobre un capítulo. Envuelve /marcela-prose y aplica los anti-patterns de constitución § I. Firma humana obligatoria por defecto. Trigger cuando la persona diga "pasada 3", "revisa la naturalidad", "limpia voz LLM", "review de prosa".
allowed-tools: Bash, Read, Write, Edit, Skill, Agent
---

# writeonmars-pasada-3

Skill que materializa la pasada 3 (naturalidad) del Principio V.3 y los
anti-patterns del Principio I. Envuelve `/marcela-prose`. Firma humana
obligatoria por defecto (`signing_matrix.pasada_3_naturalidad: human`),
fundamento de FR-020a.

## Cuándo dispararse

- "pasada 3"
- "revisa la naturalidad"
- "limpia voz LLM"
- "review de prosa"
- Tras pasada 2 limpia, antes de pasada 4.

## Qué hace

1. Despacha un sub-agente con
   `agents/claude/prompts/pasada-3.md`.
2. El sub-agente invoca `/marcela-prose` con la lente de § I y § V.3.
3. Emite bloque "Pasada 3 — Naturalidad" en `findings.md` con
   `pasada: 3_naturalidad` y checklist firmable en
   `checklists/[###-feature]/pasada-3.md`.
4. La firma queda en `firma_tipo: autonomous` cuando el sub-agente la
   ejecuta. La pasada queda **pendiente de firma humana** hasta que un
   operador listado en `human_operators[]` del manifiesto la firme. La
   skill NO falsifica firmas humanas (regla del prompt canónico).

## Inputs

- `chapters/[###]-titulo.md`.
- `specs/[###-feature]/spec.md` (especialmente `tono`).
- `specs/[###-feature]/glossary.md`, `plan.md`, `findings.md`.
- `agents/claude/prompts/pasada-3.md`.
- `.specify/templates/checklist-template.md` § "Pasada 3 — Naturalidad".

## Outputs

- Bloque "Pasada 3 — Naturalidad" añadido a `findings.md`.
- `checklists/[###-feature]/pasada-3.md` con firma humana pendiente o
  registrada.

## Procedimiento

1. Despachar sub-agente con prompt canónico.
2. Validar salida y persistir bloque.
3. Producir checklist con `firma_tipo: human` (default v1) y
   `firma_actor: pendiente` hasta que un operador la firme. La skill
   reporta al operador qué firma falta.

## Lente específica (constitución § I + § V.3)

- Frases comprimidas que obligan a reconstruir la intención.
- "No es X: es Y" más de una vez por capítulo.
- Pronombres vagos sin referente explícito en la frase anterior.
- Transiciones secas sin explicar por qué cambia el tema.
- Entusiasmo artificial, lenguaje promocional, metáforas mezcladas.
- Notas internas convertidas en prosa final.
- Texto que no se puede leer en voz alta sin sonar artificial.

## Default signing

`human` (firma obligatoria por defecto, FR-020a).

## Errores comunes

- Sub-agente que firma como humano sin serlo: regla violada por el
  prompt; la skill lo detecta y reporta.
- Anti-pattern citado en `frase_original` sin reescritura sugerida en
  severidad media o crítica: la skill rechaza y reintenta.
- Operador no listado en `human_operators[]` que intenta firmar: la
  skill lo bloquea.

## FR cubierta

- FR-018, FR-019, FR-020a.
- Constitución § I, § V.3.

## Versión

v0.1.0-mvp — 2026-05-06
