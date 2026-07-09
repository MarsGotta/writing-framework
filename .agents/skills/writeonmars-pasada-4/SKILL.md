---
name: writeonmars-pasada-4
description: Pasada 4 (precisión) sobre un capítulo. Envuelve writeonmars-contraste para verificar afirmaciones contra CitationRecord. Firma humana obligatoria por defecto. Trigger cuando la persona diga "pasada 4", "revisa la precisión", "valida fuentes y datos verificables", "contraste final".
allowed-tools: Bash, Read, Write, Edit, Skill, Agent
---

# writeonmars-pasada-4

Skill que materializa la pasada 4 (precisión) del Principio V.4. Envuelve
`writeonmars-contraste` (T040) para emitir el bloque "Pasada 4" en
`findings.md` y la checklist firmable. Firma humana obligatoria por
defecto (FR-020a).

## Cuándo dispararse

- "pasada 4"
- "revisa la precisión"
- "valida fuentes y datos verificables"
- "contraste final"
- Tras pasada 3 con firma humana registrada.

## Qué hace

1. Invoca `writeonmars-contraste` con el capítulo objetivo. Esa skill
   produce el bloque base de la pasada 4.
2. Despacha un sub-agente con
   `agents/claude/prompts/pasada-4.md` para revisar adicionalmente:
   versiones declaradas, comandos y precios verificados, afirmaciones
   absolutas matizadas, principios estables distinguidos de datos
   temporales.
3. Consolida los hallazgos del sub-agente con el output de
   `writeonmars-contraste` en un único bloque "Pasada 4 — Precisión" en
   `findings.md`.
4. Materializa la checklist en
   `checklists/[###-feature]/pasada-4.md` con firma humana pendiente.

## Inputs

- `chapters/[###]-titulo.md`.
- `specs/[###-feature]/research.md`,
  `specs/[###-feature]/findings.md`.
- `agents/claude/prompts/pasada-4.md`.
- Skill propia: `writeonmars-contraste`.
- `.specify/templates/checklist-template.md` § "Pasada 4 — Precisión".

## Outputs

- Bloque "Pasada 4 — Precisión" en `findings.md` con
  `referencias_cita` por finding (campo obligatorio en pasada 4).
- `checklists/[###-feature]/pasada-4.md`.

## Procedimiento

1. Llamar a `writeonmars-contraste`. Capturar findings.
2. Despachar sub-agente con prompt de pasada 4.
3. Consolidar hallazgos: deduplicar por `frase_original`, fusionar
   `referencias_cita`, asignar IDs `F-4.M`.
4. Persistir bloque y checklist.
5. Reportar firma pendiente (humana por defecto).

## Lente específica (constitución § V.4)

- Sin datos inventados; cada afirmación verificable tiene cita.
- Versiones, comandos y precios verificados con fecha de consulta
  reciente.
- Afirmaciones absolutas matizadas cuando el dominio admite excepción.
- Principios estables distinguidos de datos temporales (volátiles).
- Cuando el capítulo cita estándares (ISO, RAE, Fundéu, AENOR), la
  referencia exacta queda registrada en `research.md`.

## Default signing

`human` (firma obligatoria por defecto, FR-020a).

## Errores comunes

- Afirmación verificable sin `referencias_cita`: finding crítico.
- Cita con `volatil: true` y `fecha_consulta` > 90 días: warning,
  exigir refresco antes de firma humana.
- Sub-agente que firma como humano: bloqueado por el prompt canónico.

## FR cubierta

- FR-016, FR-017, FR-018, FR-019, FR-020a.
- Constitución § V.4.

## Versión

v0.1.0-mvp — 2026-05-06
