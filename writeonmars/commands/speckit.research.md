---
description: "Investiga las fuentes y produce research.md con una cita por concepto obligatorio del brief. Bloquea si algún concepto queda sin respaldo. Neutral de modelo."
---

# Investigación con fuentes

Produces el respaldo documental de la guía. Cada concepto obligatorio del brief
debe quedar citado, para que la pasada de precisión pueda contrastar después.

## Inputs

- El brief aprobado (`specs/<###-feature>/spec.md`), en especial los conceptos
  obligatorios.
- Fuentes locales en `resources/` (obligatorias si existen).
- Búsqueda web o MCPs que cumplan el contrato de citación
  (`.specify/presets/writeonmars/contracts/citation-contract.md`).
- Detalle del método: `.specify/presets/writeonmars/references/metodo/writeonmars-research/SKILL.md`.

## Qué haces

1. Para cada concepto obligatorio, busca respaldo en `resources/` y, si hace
   falta, en la web / MCPs.
2. Escribe `specs/<###-feature>/research.md` con un `CitationRecord` por concepto,
   conforme a `.specify/presets/writeonmars/contracts/citation-record.schema.json` (nombre, fecha, URL,
   cita). Nunca afirmes un dato sin fuente; si no la encuentras, márcalo y
   pregunta.

## Bloqueo

No avances a `speckit.plan` mientras quede un concepto obligatorio sin al menos
una cita válida, o si los `CitationRecord` no validan contra el esquema.

## Output

`specs/<###-feature>/research.md` con cobertura completa de los conceptos
obligatorios.
