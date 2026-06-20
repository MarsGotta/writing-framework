<!-- Mirror of specs/001-framework-architecture/contracts/pass-output-schema.md (single source of truth). Re-run T011 to refresh. -->

# Pass Output Schema v1.0

**Status**: stable for Write.OnMars v1.
**Cobertura de spec**: FR-018, FR-019, FR-020, FR-020a.

Este contrato define el formato unificado que cada una de las cinco pasadas del Principio V produce. Toda skill `writeonmars-pasada-N` MUST emitir su salida bajo este esquema para que (a) la consolidación en `findings.md` sea automatizable, (b) el cierre del proyecto pueda evaluar la matriz de firmas declarada en el manifiesto, y (c) un mantenedor pueda auditar pasadas históricas sin reconstruir contexto.

---

## Estructura del archivo `findings.md`

Un único `findings.md` por proyecto editorial, ubicado en `specs/[###-feature]/findings.md`. Cada pasada añade un bloque al final del archivo con el siguiente formato:

```markdown
## Pasada N — {nombre}

**Fecha**: YYYY-MM-DD
**Sub-agente**: {identificador del sub-agente o "human:{id}"}
**Skill principal**: {nombre y versión}
**Skills secundarias**: {lista de nombres y versiones}
**Capítulos cubiertos**: [1, 2, ...] o "global"
**Estado pasada**: passed | passed-with-warnings | blocked
**Firma**:
  - tipo: autonomous | human
  - actor: {id}
  - fecha: YYYY-MM-DD

### Hallazgos

| ID | Capítulo | Severidad | Frase original | Problema | Reescritura sugerida | Estado | Citas |
|----|----------|-----------|----------------|----------|---------------------|--------|-------|
| F-N.1 | 3 | critico | "..." | "..." | "..." | abierto | [doc-react-...] |
```

---

## Campos del bloque por pasada

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `pasada` | enum | sí | `1_estructura` \| `2_utilidad` \| `3_naturalidad` \| `4_precision` \| `5_formato` |
| `nombre` | string | sí | Etiqueta legible: "Estructura", "Utilidad", "Naturalidad", "Precisión", "Formato". |
| `fecha` | string ISO-8601 | sí | Fecha de ejecución. |
| `subagente` | string | sí | Identificador del sub-agente o `human:{id}` cuando ejecuta humano directo. |
| `skill_principal` | objeto | sí | `{name, version}` (FR-027). |
| `skills_secundarias` | lista de objetos | no | Skills auxiliares invocadas dentro de la pasada. |
| `capitulos_cubiertos` | lista de enteros o `global` | sí | Indica el alcance. |
| `estado_pasada` | enum | sí | `passed` \| `passed-with-warnings` \| `blocked`. |
| `firma` | objeto | sí | `tipo`, `actor`, `fecha`. |
| `hallazgos` | lista de `Finding` | sí (puede estar vacía si pasada limpia) | Ver siguiente sección. |

---

## Estructura de cada `Finding`

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `id` | string | sí | `F-N.M` donde N es la pasada y M es el orden secuencial dentro de la pasada. |
| `capitulo` | entero o `global` | sí | Capítulo afectado o `global` si afecta a la guía completa. |
| `severidad` | enum | sí | `critico` \| `medio` \| `bajo`. Solo `critico` bloquea el cierre. |
| `frase_original` | string | sí | Cita literal del texto problemático. Cuando aplica a estructura global (sin frase concreta), usar `null` y explicar en `problema`. |
| `problema` | string | sí | Qué falla y por qué (referenciar el principio o regla violada cuando se conozca). |
| `reescritura_sugerida` | string | sí, salvo `severidad = bajo` con decisión de no reescribir | Versión propuesta o paso accionable. |
| `estado` | enum | sí | `abierto` \| `resuelto` \| `desviacion_justificada`. |
| `referencias_cita` | lista de `citation_id` | sí cuando `pasada = 4_precision` | Enlaces al `research.md` que sustentan o contradicen la afirmación. |
| `decision_humana` | string | si `estado = desviacion_justificada` | Razón firmada por un operador humano para no resolver. |

---

## Reglas de transición de estado

```text
abierto ───(reescritura aplicada)───→ resuelto
abierto ───(operador firma desviación)───→ desviacion_justificada
resuelto ──(no permitido volver a abierto sin nuevo finding)
```

- Un finding `resuelto` no se borra; queda registrado para trazabilidad.
- Reabrir un finding requiere crear uno nuevo (`F-N.M+1`) con referencia al anterior.

---

## Reglas de bloqueo de cierre del proyecto

El cierre del proyecto editorial se evalúa mediante dos gates:

1. **Gate de hallazgos críticos** (FR-020): existe ≥ 1 finding con `severidad = critico` y `estado = abierto`. Si sí → bloquea.
2. **Gate de firma humana** (FR-020a): existe alguna pasada cuya `firma.tipo = autonomous` cuando el manifiesto declara `signing_matrix[pasada] = human`. Si sí → bloquea.

Una skill `writeonmars-close-project` (futura) consume `findings.md` + manifiesto y devuelve `{closeable: bool, blockers: [...]}`.

---

## Mapeo pasada → skill principal (default v1)

| Pasada | Nombre | Skill principal | Origen |
|--------|--------|-----------------|--------|
| 1 | Estructura | `/technical-guide-design` | bundled (FR-025) |
| 2 | Utilidad | `/technical-guide-design` | bundled (FR-025) |
| 3 | Naturalidad | `/marcela-prose` | bundled (FR-025) |
| 4 | Precisión | `writeonmars-contraste` | propia (FR-016) |
| 5 | Formato | `writeonmars-pasada-5` | propia (FR-029) |

El operador puede sobreescribir este mapeo en el manifiesto añadiendo un campo `signing_matrix.pasada_N.skill` (extensión MINOR del manifiesto, no incluida en v1.0).

---

## Versionado del schema

- **MAJOR** (v2.0): cambio de campos obligatorios, ruptura de orden de la tabla de hallazgos.
- **MINOR** (v1.y): añadir campos opcionales, ampliar enums.
- **PATCH** (v1.0.z): aclaraciones y ejemplos.

Cada bloque de pasada en `findings.md` MUST incluir un comentario HTML con la versión del schema usada: `<!-- pass-output-schema: v1.0 -->`.

---

## Ejemplo mínimo

```markdown
## Pasada 3 — Naturalidad

<!-- pass-output-schema: v1.0 -->

**Fecha**: 2026-05-10
**Sub-agente**: claude-code:agent:naturaleza-3a4f
**Skill principal**: marcela-prose v0.4.2
**Skills secundarias**: humanizer v1.1.0
**Capítulos cubiertos**: [3]
**Estado pasada**: passed-with-warnings
**Firma**:
  - tipo: human
  - actor: marcela
  - fecha: 2026-05-10

### Hallazgos

| ID | Capítulo | Severidad | Frase original | Problema | Reescritura sugerida | Estado | Citas |
|----|----------|-----------|----------------|----------|---------------------|--------|-------|
| F-3.1 | 3 | medio | "Cabe en la cabeza, deja sitio para que cada concepto técnico aterrice." | Frase comprimida + metáfora mezclada (constitución § I, regla 1). | "El ejemplo es pequeño a propósito. Permite seguir la guía sin aprender un dominio nuevo." | resuelto | [] |
| F-3.2 | 3 | bajo | "Vamos a verlo." | Transición seca (constitución § I, regla 5). | "Para entender por qué ocurre, hay que mirar primero qué entra en el contexto." | resuelto | [] |
```
