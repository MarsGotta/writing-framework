---
description: "Pasada local de revisión: estructura + utilidad de un capítulo. Comando separado, asignable a su propio modelo. No toca la voz ni verifica datos. Neutral de modelo."
---

# Pasada: estructura + utilidad

Una de las pasadas locales. Revisa que el capítulo enseñe bien, sin tocar la voz
(eso es `speckit.review-voice`) ni verificar datos (eso es
`speckit.review-precision`). Pensada para correr aislada, idealmente con un modelo
distinto al que redactó.

## User Input

```text
$ARGUMENTS
```

Capítulo(s) a revisar (p. ej. `1` o `1,2`). Sin argumento: todos.

## Inputs

- El/los capítulo(s) en `chapters/`, el brief y la descripción encadenada.
- Diseño didáctico: `.specify/presets/writeonmars/references/didactica/SKILL.md`.

## Qué verificas

- **Estructura**: promesa clara, función del capítulo, progresión lógica, y que
  cada sección cierre en una decisión, advertencia o acción (Principio II).
- **Utilidad**: un ejemplo por concepto, acción práctica al final, checklist,
  errores comunes, criterios de éxito.

## Salida

Añade a `specs/<###-feature>/findings.md` **dos bloques** —`## Pasada 1 —
Estructura` y `## Pasada 2 — Utilidad`— conforme a
`.specify/presets/writeonmars/contracts/pass-output-schema.md` (cubre las dos
dimensiones en una sola ejecución, según el `signing_matrix`: `pasada_1_estructura`
y `pasada_2_utilidad`). Modo autónomo, incidencias `flagged` por severidad. No
reescribes voz; si una frase falla de voz, lo dejas para la pasada de naturalidad.
## Modo estudio

Si el manifiesto declara `mode: estudio`, esta pasada opera sobre texto humano.
PROHIBIDO editar `chapters/` o `README.md`; la única salida es el bloque de
hallazgos en `findings.md`. PROHIBIDO cambiar `estado` de hallazgos existentes:
las transiciones son exclusivas de `scripts/dispose.py`.

Todo bloque emitido MUST incluir `<!-- pass-output-schema: v1.2 -->` y terminar
con `<!-- huellas: {"<capitulo>": "<sha256-hex>"} -->` calculado sobre los bytes
actuales del capítulo.
