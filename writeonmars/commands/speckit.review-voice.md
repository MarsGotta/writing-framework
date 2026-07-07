---
description: "Pasada local de revisión: naturalidad (voz) de un capítulo. Aplica la voz de Marcela. Comando separado, asignable a su propio modelo. No verifica datos. Neutral de modelo."
---

# Pasada: naturalidad (voz)

Una de las pasadas locales. Revisa que el capítulo suene a la autora y limpia
patrones de IA. No verifica datos (eso es `speckit.review-precision`). Pensada para
correr aislada, idealmente con un modelo distinto al que redactó: quien escribe no
oye sus propios tropiezos.

## User Input

```text
$ARGUMENTS
```

Capítulo(s) a revisar. Sin argumento: todos.

## Inputs

- El/los capítulo(s) en `chapters/`.
- **Prosa-base (capa 1)**: `.specify/presets/writeonmars/references/prosa/SKILL.md`.
  Aplica su playbook de cosido y su checklist.
- **Registro (capa 2)**:
  `.specify/presets/writeonmars/references/registros/<registro>/SKILL.md`
  (`registro` del manifiesto; si falta, el default del sector). Aplica su
  checklist de registro y sus síntomas de deriva.
- **Voz (capa 3)**: `.specify/presets/writeonmars/references/voz/SKILL.md` (+ su carpeta
  `references/`). Aplica sus reglas y su checklist de edición. No dependas de
  ninguna skill externa del agente.

## Qué verificas

- Hilo y cohesión (`references/prosa`): sin fragmentos sin verbo no deliberados
  ni enumeraciones huérfanas tras punto; cada frase recoge algo de la anterior
  y cada párrafo abre con eco del previo (test del barajado); transiciones con
  porqué; sin staccato de tres frases cortas seguidas.
- Registro del género (`references/registros/<registro>`): sin deriva académica
  (nominalizaciones, impersonal sostenido, abstracción sin artefacto), casual
  (hipérbole, colegueo, afirmación sin alcance) ni de folleto (adjetivos de
  producto). Cita el dial violado en el hallazgo.
- Voz natural: sin frases comprimidas, sin eslóganes, sin moralina, sin
  metáforas mezcladas, plural inclusivo dominante (constitución § I).
- Transiciones explicadas, referentes claros, aperturas concretas, cierres bajos.
- Limpieza de patrones LLM (ver `references/voz`: prohibiciones y antipatrones).
- Test de lectura en voz alta: marca dónde se pierde el aire o se tropieza.

## Salida

Añade a `findings.md` un bloque `## Pasada 3 — Naturalidad` conforme a
`.specify/presets/writeonmars/contracts/pass-output-schema.md`, en modo autónomo con
incidencias `flagged`. La `signing_matrix` del manifiesto puede exigir firma humana
en esta pasada.
