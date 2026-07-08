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
- Contrato y detalle: `.specify/presets/writeonmars/contracts/citation-contract.md`,
  `.specify/presets/writeonmars/contracts/claim-record.schema.json` y
  `.specify/presets/writeonmars/references/metodo/writeonmars-contraste/SKILL.md`.

## Qué verificas

1. **Consistencia interna**: cada cifra, versión, nombre de paquete, comando o
   afirmación factual del capítulo tiene respaldo en `research.md`. Lo que no, se
   marca.
2. **Verificación EN VIVO contra la fuente** (lo importante): no te fíes solo de
   `research.md`. Para cada dato volátil (versiones, nombres de paquete, comandos,
   precios, endpoints/APIs, y todo lo marcado `volatil: true` o `[VERIFICAR]`),
   **abre la `url` del `CitationRecord` (o busca la fuente en la web) y confirma el
   dato contra la fuente actual**. Si la fuente contradice el capítulo o el
   `research.md` → `critico`, anotando la discrepancia y la URL consultada (y, si
   procede, actualiza `research.md`).
3. Sin datos inventados; afirmaciones absolutas matizadas; principios estables
   distinguidos de datos temporales.

### Con qué se verifica en vivo (por orden de preferencia)

1. **La herramienta de web del propio agente**: `fetch`/`WebFetch` para abrir la
   `url` exacta del `CitationRecord`; búsqueda web solo si la URL murió y hay que
   relocalizar la fuente.
2. **context7 (MCP)** para documentación de librerías y APIs: da la versión actual
   sin raspar HTML.
3. **El MCP `writeonmars-research`** (`mcp/writeonmars-research/` en el repo
   canónico), si está montado: devuelve `CitationRecord` ya conformes al contrato.

Cualquiera de las tres vale; lo que no vale es citar de memoria del modelo. Cada
verificación anota la URL consultada y la fecha en el hallazgo o en el
`CitationRecord` actualizado.

Si **no** tienes acceso a web (ninguna de las tres vías), contrasta solo contra
`research.md`, marca los datos volátiles como "no verificado en vivo" (`medio`) y
dilo, **no finjas** la verificación. En `claims.md` esos datos quedan con
`soporte: pendiente` (no `sin_fuente`).

## Salida

Produces **dos** salidas (pass-output-schema v1.1):

1. **`findings.md`**: un bloque `## Pasada 4 — Precisión` con los hallazgos
   accionables. Cada hallazgo incluye `referencias_cita` (y la URL verificada cuando
   hiciste check en vivo) y, en v1.1, el `claim_id` afectado. Un dato sin fuente, o
   contradicho por la fuente actual, es `critico` y **bloquea el cierre**.
2. **`claims.md`**: un `ClaimRecord` por **cada** afirmación verificable evaluada (no
   solo las que fallan), con la **relación** de cada cita (`apoya`/`matiza`/
   `contradice`/`menciona`), el fragmento de soporte y el veredicto `soporte`. Idempotente
   por capítulo (reemplaza el bloque del capítulo, no duplica). La derivación de
   `soporte` y el mapeo veredicto→severidad están en la skill `writeonmars-contraste`.
## Modo estudio

Si el manifiesto declara `mode: estudio`, esta pasada opera sobre texto humano.
PROHIBIDO editar `chapters/` o `README.md`; la única salida es el bloque de
hallazgos en `findings.md` y, si procede, `claims.md`. PROHIBIDO cambiar
`estado` de hallazgos existentes: las transiciones son exclusivas de
`scripts/dispose.py`.

Todo bloque emitido MUST incluir `<!-- pass-output-schema: v1.2 -->` y terminar
con `<!-- huellas: {"<capitulo>": "<sha256-hex>"} -->` calculado sobre los bytes
actuales del capítulo. Si `roots/` no contiene fichas aplicables, declara
"no evaluable contra fuentes: roots/ sin fichas aplicables" en notas en vez de
emitir 0 hallazgos como si la verificación hubiera ocurrido.
