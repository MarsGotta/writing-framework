---
description: "Pasada local de revisión: precisión. Contrasta el capítulo contra research.md Y verifica EN VIVO los datos volátiles abriendo la fuente real (web/fetch). Comando separado, idealmente con un modelo con acceso a web. Neutral de modelo."
---

# Pasada: precisión

Una de las pasadas locales, y la más independiente: verifica hechos, no estilo.
**No basta con que el capítulo coincida con `research.md`**: para lo volátil, abre
la fuente real y comprueba que sigue siendo cierto. `research.md` pudo citar mal o
la fuente pudo cambiar. Idealmente la corre un modelo distinto al que redactó y con
acceso a web.

## User Input

```text
$ARGUMENTS
```

Capítulo(s) a revisar. Sin argumento: todos.

## Inputs

- El/los capítulo(s) en `chapters/`.
- `specs/<###-feature>/research.md` con los `CitationRecord` (cada uno trae su `url`).
- **Acceso a búsqueda web / `fetch` / context7** para abrir las fuentes.
- Contrato y detalle: `.specify/presets/writeonmars/contracts/citation-contract.md`
  y `.specify/presets/writeonmars/references/metodo/writeonmars-contraste/SKILL.md`.

## Qué verificas

1. **Consistencia interna**: cada cifra, versión, nombre de paquete, comando o
   afirmación factual del capítulo tiene respaldo en `research.md`. Lo que no, se
   marca.
2. **Verificación EN VIVO contra la fuente** (lo importante): no te fíes solo de
   `research.md`. Para cada dato volátil —versiones, nombres de paquete, comandos,
   precios, endpoints/APIs, y todo lo marcado `volatil: true` o `[VERIFICAR]`—
   **abre la `url` del `CitationRecord` (o busca la fuente en la web) y confirma el
   dato contra la fuente actual**. Si la fuente contradice el capítulo o el
   `research.md` → `critico`, anotando la discrepancia y la URL consultada (y, si
   procede, actualiza `research.md`).
3. Sin datos inventados; afirmaciones absolutas matizadas; principios estables
   distinguidos de datos temporales.

Si **no** tienes acceso a web, contrasta solo contra `research.md`, marca los datos
volátiles como "no verificado en vivo" (`medio`) y dilo — **no finjas** la
verificación.

## Salida

Añade a `findings.md` un bloque `## Pasada 4 — Precisión` conforme a
`.specify/presets/writeonmars/contracts/pass-output-schema.md`. Cada hallazgo
incluye `referencias_cita` (y la URL verificada cuando hiciste check en vivo). Un
dato sin fuente, o contradicho por la fuente actual, es `critico` y **bloquea el
cierre**.
