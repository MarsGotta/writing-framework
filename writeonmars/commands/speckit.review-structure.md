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
## Huellas (ambos modos)

Todo bloque emitido MUST incluir `<!-- pass-output-schema: v1.2 -->` y terminar
con `<!-- huellas: {"<capitulo>": "<sha256-hex>"} -->` calculado sobre los bytes
actuales del capítulo.

## Modo estudio

Si el manifiesto declara `mode: estudio`, esta pasada opera sobre texto humano.
PROHIBIDO editar `chapters/` o `README.md`; la única salida es el bloque de
hallazgos en `findings.md`. PROHIBIDO cambiar `estado` de hallazgos existentes:
las transiciones son exclusivas de `scripts/dispose.py`.

## Pista corta

Si el manifiesto declara `track: corta` (`.writeonmars-manifest.json`), este
comando **vehicula la pasada combinada**: un único run verifica y registra
**cuatro bloques** de pasada en `specs/<###-feature>/findings.md`, en lugar de
dos. Ese run viaja por el despacho de la pasada 1 de siempre; el ejecutor no
cambia, porque ve el bloque 1 registrado y pasa a la pasada 4.

Los cuatro bloques, cada uno con su `<!-- pass-output-schema: v1.2 -->` y su
huella, son:

- `## Pasada 1 — Estructura`, `## Pasada 2 — Utilidad` y `## Pasada 3 —
  Naturalidad`, los tres con `**Capítulos cubiertos**: 1` y huella
  `<!-- huellas: {"1": "<sha256>"} -->` sobre los bytes actuales de
  `chapters/01-*.md`.
- `## Pasada 5 — Formato`, con `**Capítulos cubiertos**: global` y huella
  `<!-- huellas: {"global": "<sha256>"} -->`, cuyo valor es
  `sha256(concat(sha256(cap_i)))` en orden ordinal —con un solo capítulo,
  `sha256(sha256(cap_1))`—.

Cada dimensión se verifica con el criterio de su pasada suelta: la naturalidad
con la pirámide de prosa de `speckit.review-voice` y el formato con
`speckit.review-global`. La coherencia entre capítulos de la dimensión 5 es vacua
en pieza única, porque no hay dos capítulos entre los que contradecirse, así que
el bloque 5 verifica solo formato. Respeta la `signing_matrix`: una pasada que
exige firma `human` no se cierra como `autonomous`.

La **dimensión 4 (precisión) no va en la combinada**. Corre en relevo aparte, con
otro rol y otro modelo (`documentalista`): es la regla dura **voz ≠ precisión**
del Principio V, que separa reescribir prosa de contrastar datos. El esquema
pass-output no se toca; este comando ya emitía dos bloques en un run y la
combinada extiende ese precedente a cuatro dimensiones.

