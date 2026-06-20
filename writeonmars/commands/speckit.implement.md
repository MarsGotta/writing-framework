---
description: "Redacta cada capítulo aplicando la voz y la estructura editorial. SOLO escribe; la revisión la hace speckit.review, idealmente con OTRO modelo. Neutral de modelo (la voz viaja en .specify/presets/writeonmars/references/voz)."
---

# Redacción de un capítulo

Escribes UN capítulo con la voz de la autora. Solo redacta; la revisión es aparte
(`speckit.review`). Un capítulo por ejecución, para que en orquestación cada
capítulo lo pueda tomar un agente distinto.

## User Input

```text
$ARGUMENTS
```

Indica QUÉ capítulo escribir:

- **Número explícito** (p. ej. `2`): redacta ese capítulo del temario. Si el
  archivo ya existe en `chapters/`, lo **rehace** (sobrescribe) — así pides "rehaz
  el 1" con `1`.
- **Sin argumento**: redacta el **siguiente pendiente** — el primer capítulo del
  temario (`plan.md`) que aún no tiene archivo en `chapters/`. Si el 1 ya existe,
  escribe el 2.

Si hay ambigüedad, confirma con la persona qué capítulo vas a (re)escribir antes de
empezar.

## Inputs (por capítulo)

- Brief, sección Temario, la descripción encadenada del capítulo objetivo y de
  los contiguos, glosario vigente, ejemplo recurrente.
- **Voz**: `.specify/presets/writeonmars/references/voz/SKILL.md` (+ su `.specify/presets/writeonmars/references/`). Aplícala; no dependas de
  ninguna skill externa.
- **Didáctica**: `.specify/presets/writeonmars/references/didactica/SKILL.md`.
- Detalle del método: `.specify/presets/writeonmars/references/metodo/writeonmars-redaccion/SKILL.md`.

## Qué haces

1. Escribe `chapters/<NN>-titulo.md` con las nueve secciones de la plantilla de
   capítulo y la voz de `.specify/presets/writeonmars/references/voz`. Usa el ejemplo recurrente real, no
   inventado.
2. Añade el anexo de glosario del capítulo (términos nuevos).

**Este comando SOLO redacta. No revises aquí.** Las pasadas de revisión las corre
`speckit.review`, idealmente con **otro modelo** distinto al que escribió: quien
redacta es indulgente con su propio texto. Escribe un agente, revisa otro — así la
revisión es independiente. No escribas en `findings.md` desde este comando.

## Output

`chapters/<NN>-titulo.md` + el anexo de glosario del capítulo. La revisión
(`findings.md`) la produce `speckit.review` por separado, idealmente con otro
modelo. El glosario consolidado se actualiza (ver
`.specify/presets/writeonmars/references/metodo/writeonmars-glossary/SKILL.md`).
