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
- **Prosa-base (capa 1, SIEMPRE, antes que la voz)**:
  `.specify/presets/writeonmars/references/prosa/SKILL.md`. Fluidez y cohesión:
  frases completas, progresión conocido → nuevo, eco entre párrafos,
  transiciones con porqué, ritmo de crucero. Redacta con su checklist de
  generación activo; sus dos innegociables no los deroga ninguna otra capa.
- **Registro (capa 2)**:
  `.specify/presets/writeonmars/references/registros/<registro>/SKILL.md`, con
  `<registro>` del manifiesto (`registro`); si falta, el default del sector
  (sección "Registro por defecto" de su base). Fija formalidad, densidad,
  figuras, humor y aserción del género.
- **Voz (capa 3)**: `.specify/presets/writeonmars/references/voz/SKILL.md` (+ su `.specify/presets/writeonmars/references/`). Aplícala; no dependas de
  ninguna skill externa. En conflicto de sabor gana la voz; en formalidad y
  densidad globales, el registro; los innegociables de prosa-base, nadie.
- **Didáctica**: `.specify/presets/writeonmars/references/didactica/SKILL.md`.
- Detalle del método: `.specify/presets/writeonmars/references/metodo/writeonmars-redaccion/SKILL.md`.

## Qué haces

1. Escribe `chapters/<NN>-titulo.md` con la estructura de capítulo que fije la
   **base del sector** (`.specify/presets/writeonmars/references/sectores/<sector>.md`,
   sector en el manifiesto), el hilo de `.specify/presets/writeonmars/references/prosa`,
   el registro de `.specify/presets/writeonmars/references/registros/<registro>`
   y la voz de `.specify/presets/writeonmars/references/voz`.
   Usa el ejemplo recurrente real, no inventado.
2. **Cierra el capítulo con una sección `## Fuentes`** (obligatoria, Estándares
   editoriales): nombre, enlace y fecha de cada fuente citada en ESE capítulo. No
   basta con el research consolidado; la trazabilidad es por capítulo.
3. Añade el anexo de glosario del capítulo (términos nuevos).

**Este comando SOLO redacta. No revises aquí.** Las pasadas de revisión las corre
`speckit.review`, idealmente con **otro modelo** distinto al que escribió: quien
redacta es indulgente con su propio texto. Escribe un agente, revisa otro — así la
revisión es independiente. No escribas en `findings.md` desde este comando.

## Output

`chapters/<NN>-titulo.md` + el anexo de glosario del capítulo. La revisión
(`findings.md`) la produce `speckit.review` por separado, idealmente con otro
modelo. El glosario consolidado se actualiza (ver
`.specify/presets/writeonmars/references/metodo/writeonmars-glossary/SKILL.md`).
