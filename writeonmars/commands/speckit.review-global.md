---
description: "Pasada global de revisión: formato + coherencia entre capítulos. Se corre una vez sobre el libro entero, no por capítulo. Comando separado. Neutral de modelo."
---

# Pasada global: formato + coherencia

La única pasada que NO es por capítulo: revisa lo que solo existe a nivel libro.
Se corre una vez, hacia el cierre, sobre toda la guía.

## Inputs

- Todos los capítulos en `chapters/`, el glosario consolidado y el `plan.md`. La
  coherencia se contrasta contra las **descripciones encadenadas** de `plan.md`
  (conexión anterior/siguiente y ejemplo recurrente por capítulo): son el hilo
  narrativo del método (sustituyen al antiguo `HILO-NARRATIVO.md` del flujo
  artesanal).

## Qué verificas

- **Formato**: índice navegable, cajas visuales útiles y consistentes, títulos
  claros, ejemplos diferenciados del cuerpo, sin bloques de texto excesivos.
- **Coherencia entre capítulos**: que ninguno contradiga o redefina términos ya
  fijados, que el glosario esté consolidado sin colisiones, que las referencias
  cruzadas ("como vimos en el cap. X") apunten bien, y que el ejemplo recurrente
  se mantenga consistente de principio a fin.

## Salida

Añade a `findings.md` un bloque `## Pasada 5 — Formato + coherencia` conforme a
`.specify/presets/writeonmars/contracts/pass-output-schema.md`, con
`capitulos_cubiertos: global` (la dimensión `pasada_5_formato`, extendida con la
coherencia entre capítulos). Incidencias `flagged` por severidad; las críticas
bloquean el cierre.
## Huellas (ambos modos)

El bloque emitido MUST incluir `<!-- pass-output-schema: v1.2 -->` y terminar
con `<!-- huellas: {"global": "<sha256-hex>"} -->`, donde el valor global es
`sha256(concat(sha256(cap_i)))` en orden ordinal.

## Modo estudio

Si el manifiesto declara `mode: estudio`, esta pasada opera sobre la obra humana.
PROHIBIDO editar `chapters/` o `README.md`; la única salida es el bloque de
hallazgos en `findings.md`. PROHIBIDO cambiar `estado` de hallazgos existentes:
las transiciones son exclusivas de `scripts/dispose.py`.

## Pista corta

Si el manifiesto declara `track: corta` (`.writeonmars-manifest.json`), el formato
viaja en la **pasada combinada** (`speckit.review-structure`), que registra el
bloque `## Pasada 5 — Formato` con `**Capítulos cubiertos**: global`. La mitad de
coherencia entre capítulos es vacua en pieza única —hay un solo capítulo—, así que
el bloque solo cubre formato. Este comando queda operativo como **red de
reparación** (FR-006): si la combinada no registró el bloque 5, el ejecutor
despacha esta pasada suelta y lo escribe.

