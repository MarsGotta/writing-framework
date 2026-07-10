---
description: "Genera el temario (Número | Título | Promesa) y las descripciones encadenadas en plan.md. El temario es además el índice del PDF. No pisa el speckit.plan de Spec Kit. Neutral de modelo."
---

# Temario y descripciones encadenadas

Diseñas la estructura de la guía: el orden de capítulos como argumento, no como
índice, y cómo conecta cada uno con el anterior y el siguiente.

## Inputs

- Brief aprobado y `research.md`.
- Diseño didáctico: `.specify/presets/writeonmars/references/didactica/SKILL.md`.
- Detalle del método: `.specify/presets/writeonmars/references/metodo/writeonmars-temario/SKILL.md` y
  `.specify/presets/writeonmars/references/metodo/writeonmars-descripciones/SKILL.md`.

## Qué haces

1. Escribe en `specs/<###-feature>/plan.md` la sección **Temario** como tabla
   `Número | Título | Promesa | Estructura aplicada` (estructura siempre
   `didactica_v1`). Esta tabla la usa `export.py` como índice del PDF: cuida las
   promesas, son las descripciones del índice.
2. Escribe la sección **Descripciones encadenadas**: por capítulo, promesa
   específica, conexión anterior, conexión siguiente, ejemplo recurrente aplicado,
   conceptos introducidos. Las conexiones `null` solo valen en el primer y último
   capítulo.

## Bloqueo

No avances a redacción si hay capítulos sin promesa, títulos vacíos, o conexiones
`null` fuera de frontera.

## Output

`plan.md` con Temario + Descripciones encadenadas. Pasa el Constitution Check
editorial (los cinco principios) antes de seguir.

## Pista corta

Si el manifiesto declara `track: corta` (`.writeonmars-manifest.json`), este comando no
se despacha en el camino feliz: la firma del brief en `speckit.specify` ya materializó
el temario degenerado de una fila. Si se invoca a mano, **MUST preservar la sección
`## Temario` existente**: no la regeneres ni la sobrescribas. La pieza única ya es el
capítulo 1 del temario.
