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
- **Voz**: `.specify/presets/writeonmars/references/voz/SKILL.md` (+ su carpeta
  `references/`). Aplica sus reglas y su checklist de edición. No dependas de
  ninguna skill externa del agente.

## Qué verificas

- Voz natural y sobria: sin frases comprimidas, sin eslóganes, sin moralina, sin
  metáforas mezcladas, plural inclusivo dominante (constitución § I).
- Transiciones explicadas, referentes claros, aperturas concretas, cierres bajos.
- Limpieza de patrones LLM (ver `references/voz`: prohibiciones y antipatrones).
- Test de lectura en voz alta: marca dónde se pierde el aire o se tropieza.

## Salida

Añade a `findings.md` un bloque `## Pasada 3 — Naturalidad` conforme a
`.specify/presets/writeonmars/contracts/pass-output-schema.md`, en modo autónomo con
incidencias `flagged`. La `signing_matrix` del manifiesto puede exigir firma humana
en esta pasada.
