# Data Model (Phase 1) — ClaimRecord, factualidad y adiciones de esquema

**Feature**: `003-atribucion-factualidad`
**Fecha**: 2026-06-21

Define el modelo de datos nuevo (`ClaimRecord`), las adiciones a contratos existentes (`pass-output-schema` v1.1, `manifest-schema` MINOR) y el algoritmo determinista de factualidad. El JSON Schema canónico vive en `contracts/claim-record.schema.json` (junto a este archivo y espejado en `writeonmars/contracts/` al implementar).

---

## 1. ClaimRecord v1.0

### 1.1 Modelo conceptual

Un **ClaimRecord** es la representación digital de una **afirmación verificable** de un capítulo y de la evidencia que la sostiene. Es el gemelo, a nivel de afirmación, del `CitationRecord` (que está a nivel de fuente). Permite a un mantenedor o a `status.py`:

1. Saber qué afirmación concreta del capítulo se está verificando (`frase` anclada).
2. Conocer qué fuentes la sostienen y **con qué relación** (`evidencia[]`).
3. Saber el veredicto agregado (`soporte`) y si se verificó en vivo.
4. Recomputar el índice de factualidad sin re-ejecutar el juicio.

Vive en `specs/<###-feature>/claims.md`, agrupado por capítulo. Es estado durable, versionado en git, recomputable; nunca fuente de verdad de la prosa (eso es el capítulo) ni de las fuentes (eso es `research.md`).

### 1.2 Campos del ClaimRecord

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `claim_id` | string | sí | Identificador estable dentro del proyecto. Recomendado: `claim-c{capitulo}-{n}` (p. ej. `claim-c3-07`). |
| `capitulo` | entero o `"global"` | sí | Capítulo al que pertenece la afirmación (ordinal del temario) o `global`. |
| `frase` | string | sí | Cita literal anclada del capítulo (la oración/segmento que contiene la afirmación). ≥ 20 caracteres salvo dato estructurado concreto (una versión). |
| `tipo_afirmacion` | enum | sí | `dato_duro` \| `afirmacion_blanda`. `dato_duro` = versión, comando, precio, estándar, estadística, fecha, endpoint/API, nombre de paquete. `afirmacion_blanda` = afirmación verificable no numérica/no exacta. (Gobierna la severidad, FR-009.) |
| `evidencia` | lista de `Evidencia` | sí (puede ser `[]` si `sin_fuente`) | Aristas afirmación↔fuente. Ver § 1.4. |
| `soporte` | enum | sí | `soportado` \| `parcial` \| `sin_fuente` \| `contradicho` \| `pendiente`. **Derivado** de `evidencia[]` por las reglas de § 1.3. |
| `verificado_en_vivo` | boolean | sí | `true` si al menos una fuente se abrió en vivo (web/fetch) para esta afirmación. |
| `url_verificada` | string | si `verificado_en_vivo = true` | URL efectivamente abierta en la verificación en vivo. |
| `fecha_verificacion` | string (ISO-8601 fecha) | si `verificado_en_vivo = true` | `YYYY-MM-DD` de la verificación en vivo. |
| `pasada_schema` | string (semver) | sí | Versión de `pass-output-schema` bajo la que se emitió (`"1.1"`). |
| `notas` | string | no | Comentario libre (p. ej. por qué se eligió la peor relación). |

### 1.3 Derivación de `soporte` (determinista, la fija la pasada 4)

`soporte` se calcula a partir de `evidencia[]` tomando la **peor** relación presente (orden de peor a mejor: `contradice` > (`menciona`|sin evidencia) > `matiza` > `apoya`), modulado por `tipo_afirmacion`:

```
si alguna arista.relacion == "contradice"            → soporte = "contradicho"
si no, si evidencia == []                            → soporte = "sin_fuente"
si no, si toda arista es "menciona"                  → soporte = "sin_fuente" si dato_duro, "parcial" si blanda
si no, si la mejor arista es "matiza"                → soporte = "parcial"
si no (existe al menos una "apoya")                  → soporte = "soportado"
excepción: dato volátil sin poder abrir la fuente    → soporte = "pendiente" (sin web), independientemente de lo anterior
```

`pendiente` es un estado terminal de "no se pudo verificar en vivo", reservado a datos volátiles sin acceso web (FR-006). No es lo mismo que `sin_fuente` (que sí pudo verificarse y no hay respaldo).

### 1.4 Sub-entidad `Evidencia` (la arista)

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `citation_id` | string | sí | `citation_id` de un `CitationRecord` existente en `research.md`. |
| `relacion` | enum | sí | `apoya` \| `matiza` \| `contradice` \| `menciona`. Propiedad de la **arista**, contextual a esta afirmación. |
| `cita_fragmento_soporte` | string | si `relacion = apoya` | Oración/segmento exacto de la fuente que sostiene la afirmación. Obligatorio para `apoya`; recomendado para `matiza`/`contradice`. |
| `confianza_match` | enum | no | `alta` \| `media` \| `baja`. Confianza del agente en que esta fuente corresponde a esta afirmación (no la fiabilidad de la fuente, que ya está en `CitationRecord.confianza`). |

**Decisión de modelado clave**: la `relacion` vive en la arista (`Evidencia`), no en `CitationRecord`. La misma fuente puede `apoyar` la afirmación A y solo `mencionar` la B. Meter el veredicto en `CitationRecord` lo haría incorrecto por construcción. (Fundamento: Scite smart citations, `research.md` § 2.5.)

### 1.5 Ejemplo

```json
{
  "claim_id": "claim-c4-03",
  "capitulo": 4,
  "frase": "useEffect se ejecuta después de que el navegador haya pintado la pantalla.",
  "tipo_afirmacion": "afirmacion_blanda",
  "evidencia": [
    {
      "citation_id": "doc-react-19-effect-2026-05-06",
      "relacion": "apoya",
      "cita_fragmento_soporte": "Effects run after the browser has painted the screen.",
      "confianza_match": "alta"
    }
  ],
  "soporte": "soportado",
  "verificado_en_vivo": true,
  "url_verificada": "https://react.dev/reference/react/useEffect",
  "fecha_verificacion": "2026-06-21",
  "pasada_schema": "1.1"
}
```

```json
{
  "claim_id": "claim-c4-07",
  "capitulo": 4,
  "frase": "La versión estable actual de React es la 19.2.0.",
  "tipo_afirmacion": "dato_duro",
  "evidencia": [
    {
      "citation_id": "web-react-releases-2026-05-06",
      "relacion": "menciona",
      "cita_fragmento_soporte": "",
      "confianza_match": "media"
    }
  ],
  "soporte": "sin_fuente",
  "verificado_en_vivo": true,
  "url_verificada": "https://react.dev/versions",
  "fecha_verificacion": "2026-06-21",
  "pasada_schema": "1.1",
  "notas": "La fuente lista versiones pero no confirma 19.2.0 como estable actual → dato duro sin evidencia que lo sostenga → critico en findings."
}
```

### 1.6 Reglas de validación

1. `claim_id` único dentro del proyecto; colisión → sufijo `-dup-<n>` y warning (paralelo a la regla de `CitationRecord`).
2. Todo `evidencia[].citation_id` MUST resolver a un `CitationRecord` de `research.md`. Si no resuelve → la pasada 4 lo reporta y NO emite la arista (no inventa fuentes).
3. `relacion: apoya` requiere `cita_fragmento_soporte` no vacío.
4. `soporte` MUST ser consistente con `evidencia[]` según § 1.3 (validable por `validate-claim.sh` + un check de coherencia).
5. `verificado_en_vivo = true` ⇒ `url_verificada` y `fecha_verificacion` presentes; `fecha_verificacion` ≤ fecha actual.
6. Inmutabilidad blanda: al re-correr la pasada 4 de un capítulo, sus `ClaimRecord` se **reemplazan en bloque** (idempotencia por capítulo, FR-007); no se editan in situ ni se mezclan con la ronda anterior.

---

## 2. Estructura de `claims.md`

Un único `claims.md` por proyecto, en `specs/<###-feature>/claims.md`. Bloque por capítulo. Cada bloque: una tabla legible + el JSON embebido (para parseo robusto por `status.py` sin depender del markdown). Comentario de versión obligatorio.

```markdown
<!-- claim-record-schema: v1.0 -->
<!-- pass-output-schema: v1.1 -->

## Claims — Capítulo 4

| claim_id | frase (recorte) | tipo | soporte | relaciones | en vivo |
|----------|-----------------|------|---------|-----------|---------|
| claim-c4-03 | "useEffect se ejecuta después…" | blanda | soportado | apoya | sí |
| claim-c4-07 | "La versión estable actual es 19.2.0" | dato_duro | sin_fuente | menciona | sí |

```json
[
  { "claim_id": "claim-c4-03", "capitulo": 4, "...": "..." },
  { "claim_id": "claim-c4-07", "capitulo": 4, "...": "..." }
]
```
```

**Contrato de parseo para `status.py`**: el bloque ```json de cada capítulo es la fuente de verdad de máquina; la tabla es para humanos. `status.py` lee los bloques ```json (FR-010). Si un bloque JSON falta o no parsea, `status.py` marca ese capítulo como `factuality_unmeasured` y NO lo cuenta como 0 (edge case del spec).

---

## 3. Algoritmo de factualidad (determinista, en `status.py`)

### 3.1 Denominador y numerador

Por capítulo `c`:

```
verificables(c)  = ClaimRecord de c con soporte ∈ {soportado, parcial, sin_fuente, contradicho}
                   (es decir, excluye 'pendiente': no se pudo medir)
soportadas(c)    = ClaimRecord de c con soporte == soportado
factuality(c)    = soportadas(c) / verificables(c)     (si verificables(c) == 0 → None, "no medido")
pendientes(c)    = ClaimRecord de c con soporte == pendiente   (se reportan aparte)
```

Global:

```
factuality_global = Σ_c soportadas(c) / Σ_c verificables(c)   (micro-promedio; None si denominador 0)
```

Se usa **micro-promedio** (suma de soportadas / suma de verificables) para que capítulos con más afirmaciones pesen proporcionalmente. `factuality_by_chapter` reporta el valor por capítulo para diagnóstico.

`parcial` cuenta como **no soportada** en el numerador (es una afirmación que necesita matizarse o cuya evidencia no es plena). Esto es deliberado: el índice mide "afirmaciones con evidencia plena", consistente con FActScore (`research.md` § 2.4).

### 3.2 Gate g4

```
si manifest.quality_gates ausente:
    gates.factuality = None        # no se evalúa; closeable = g1 ∧ g2 ∧ g3 (como hoy)
si no:
    min      = quality_gates.factuality_min                       # 0..1
    min_cap  = quality_gates.factuality_min_per_chapter (opcional)
    mode     = quality_gates.factuality_mode (default "blocking")
    g4 = (factuality_global is not None and factuality_global >= min)
         and (min_cap ausente or todo factuality(c) medido >= min_cap)
    si mode == "advisory": closeable = g1 ∧ g2 ∧ g3   (g4 solo informa)
    si mode == "blocking": closeable = g1 ∧ g2 ∧ g3 ∧ g4
```

Nota de no-deadlock: el déficit de factualidad **ya** debe estar expresado como findings `critico`/`medio` vía FR-009, de modo que `revise_pending > 0` y `by_chapter.approved == false` lo capturan **antes** de que la jefa llegue al cierre. g4 es un **backstop numérico**, no la vía primaria de enrutado. Si g4 estuviera en rojo pero `revise_pending == 0`, es señal de inconsistencia entre `claims.md` y `findings.md` y `status.py` lo reporta como warning (no debería ocurrir si la pasada 4 cumple FR-008/FR-009).

### 3.3 Campos nuevos en `status.py --json` (aditivos, FR-011)

```jsonc
{
  // ... todos los campos actuales, sin cambios ...
  "factuality_global": 0.86,                 // float | null
  "factuality_by_chapter": {                  // por ordinal en string
    "1": 1.0, "2": 0.9, "3": null, "4": 0.7
  },
  "factuality_unmeasured": ["3"],             // capítulos sin claims.md/JSON parseable
  "factuality_pending": { "4": 1 },           // afirmaciones 'pendiente' por capítulo (informativo)
  "gates": {
    "no_open_criticals": true,
    "human_signatures": true,
    "guide_complete": true,
    "factuality": false                       // bool | null (null si no hay umbral)
  },
  "closeable": false
}
```

`by_chapter[c]` puede ganar, opcionalmente y de forma aditiva, `"factuality": float|null` para que el dashboard por capítulo lo muestre; NO se añade a la fórmula de `approved` (esa sigue siendo `drafted ∧ {1,2,3,4} ⊆ passes_done ∧ revise_pending == 0`).

---

## 4. Adiciones a `pass-output-schema.md` → v1.1 (MINOR)

Cambios aditivos, sin eliminar nada (FR-008, FR-015):

1. Nueva sección "Salida de claims de la pasada 4": además del bloque de `findings.md`, la pasada 4 emite/actualiza `claims.md` con el modelo de § 1–2.
2. El campo `referencias_cita` de cada `Finding` de pasada 4 (ya existente) se relaciona explícitamente con los `claim_id`: un finding de precisión DEBE referenciar el `claim_id` afectado además de los `citation_id` (trazabilidad finding↔claim). Se admite un campo opcional `claim_id` en la fila de hallazgo o, sin romper la tabla, en la columna `Citas` se permite listar `claim:<id>` junto a los `citation_id`.
3. Comentario de versión: los bloques de pasada 4 emitidos bajo la feature llevan `<!-- pass-output-schema: v1.1 -->`.

> Compatibilidad: un `findings.md` v1.0 sigue siendo válido; v1.1 solo añade la obligación de `claims.md` para pasada 4 y la trazabilidad opcional al `claim_id`. `status.py` debe tolerar ambos (v1.0 sin claims → factualidad "no medida").

---

## 5. Adiciones a `manifest-schema.json` (MINOR)

Nuevo objeto opcional `quality_gates` (recordar `additionalProperties: false` en el manifest → hay que declararlo explícitamente):

```jsonc
"quality_gates": {
  "type": "object",
  "additionalProperties": false,
  "description": "Optional quality gates beyond criticals/signatures/completeness. Cache de política, no fuente de verdad.",
  "properties": {
    "factuality_min":            { "type": "number", "minimum": 0, "maximum": 1 },
    "factuality_min_per_chapter":{ "type": "number", "minimum": 0, "maximum": 1 },
    "factuality_mode":           { "type": "string", "enum": ["advisory", "blocking"], "default": "blocking" }
  }
}
```

Se añade a `properties` del manifest **sin** incluirlo en `required` (retrocompatibilidad: manifests existentes siguen validando). Bump del `$comment`/versión del schema a la siguiente MINOR.

---

## 6. Trazabilidad con la constitución

La feature toca el Principio IV (precisión léxica → ahora con grano de afirmación y veredicto de relación) y el Principio V (revisión → la pasada 4 produce métrica). Conserva "Fuentes por capítulo" (MUST) pero la **deriva/valida** desde `claims.md`. Es un bump **MINOR** de la constitución: añade un requisito (atribución por afirmación + índice de factualidad) sin invalidar guías existentes ni redefinir principios. El `SYNC IMPACT REPORT` de la constitución debe registrarlo.
