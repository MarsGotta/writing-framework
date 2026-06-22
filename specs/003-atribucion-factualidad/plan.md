# Implementation Plan: Atribución por afirmación y gate de factualidad

**Branch**: `003-atribucion-factualidad` | **Date**: 2026-06-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/003-atribucion-factualidad/spec.md`
**Project type**: software (feature de framework)

## Summary

Llevar la verificación de fuentes del grano capítulo al grano afirmación, persistiendo en `claims.md` el trabajo que la pasada 4 ya hace, clasificando la relación cita↔afirmación (smart citation) y exponiendo un índice de factualidad determinista con gate configurable en `status.py`. Enfoque técnico (de `research.md`): un contrato nuevo (`ClaimRecord`) + cómputo determinista en el script, sin lógica acoplada al orquestador. La regla que preserva la transparencia con Paperclip: **juicio en la referencia agnóstica de la pasada 4; conteo en `status.py`; el déficit de factualidad se enruta por la maquinería de findings→revise que ya existe**.

## Technical Context

**Language/Version**: Python 3.11 (scripts), Markdown + JSON (contratos y referencias), Bash (helpers de test).
**Primary Dependencies**: ninguna nueva en runtime de producción. Validación de esquema con `jsonschema>=4.18` (ya usada por los helpers de test; el script `status.py` NO depende de jsonschema, parsea JSON embebido con la stdlib).
**Storage**: ficheros versionados en git (`specs/<feature>/claims.md`, `findings.md`, `.writeonmars-manifest.json`).
**Testing**: smoke tests en `tests/smoke/`, helpers en `tests/lib/`, piloto editorial en `tests/editorial-pilot/`.
**Target Platform**: agnóstico de modelo y de orquestador (corre con un solo agente o bajo Paperclip; en Linux/Paperclip, Chrome = chromium).
**Project Type**: editorial-framework (software).
**Constraints**: retrocompatibilidad estricta de `status.py --json` (campos aditivos); cero APIs nuevas de Paperclip; determinismo del cómputo (sin LLM en el script).
**Scale/Scope**: guías de pocas decenas de capítulos; `claims.md` del orden de 10²–10³ ClaimRecord por guía.

## Constitution Check

*GATE: pasa antes de Phase 0. Re-evaluar tras Phase 1.*

| Principio | Conformidad | Evidencia |
|---|---|---|
| **I. Voz natural y sobria** (NO NEGOCIABLE) | pasa | La feature no toca redacción ni pasadas de voz (1·2·3); no altera prosa. |
| **II. Estructura situación→explicación→consecuencia** | pasa | Sin cambios en la plantilla de capítulo ni en el temario. |
| **III. Brief obligatorio** (NO NEGOCIABLE) | pasa | No toca el brief ni el research-gate del plan. |
| **IV. Precisión léxica** | pasa (se refuerza) | Añade grano de afirmación + veredicto de relación; conserva "Fuentes por capítulo" derivándola. Requiere bump MINOR de constitución (FR-015). |
| **V. Revisión multi-pasada** (NO NEGOCIABLE) | pasa (se refuerza) | La pasada 4 gana métrica y veredicto; conserva las 5 dimensiones y el "detector ≠ corrector". |
| **VI. Neutralidad de agente y modelo** (NO NEGOCIABLE) | pasa | Juicio en referencia agnóstica; conteo determinista en script; sin dependencia de proveedor (FR-017). |

Sin desviaciones que registrar en Complexity Tracking (ver § final).

## Project Structure (archivos que toca la feature)

```text
contracts/
├── claim-record.schema.json          # NUEVO (espejo de specs/003/contracts/)
├── pass-output-schema.md             # EDIT → v1.1 (añade claims + trazabilidad claim_id)
└── manifest-schema.json              # EDIT → MINOR (añade quality_gates)

writeonmars/
├── contracts/
│   ├── claim-record.schema.json      # NUEVO (espejo)
│   ├── pass-output-schema.md         # EDIT → v1.1 (espejo)
│   └── manifest-schema.json          # EDIT → MINOR (espejo)
├── references/metodo/writeonmars-contraste/SKILL.md   # EDIT (clasificar relación + persistir claims.md)
├── commands/speckit.review-precision.md               # EDIT (documentar salida claims.md)
├── scripts/
│   ├── status.py                     # EDIT (parse claims.md + factualidad + g4)
│   └── export.py                     # EDIT (validar/derivar "Fuentes por capítulo" — decisión D1)
└── memory/constitution.md            # EDIT → bump MINOR (requisito de atribución + factualidad)

paperclip/agents/documentalista/bundle.md   # EDIT (reflejar relación + claims.md; rol sin cambios)
paperclip/agents/editora-jefa/HEARTBEAT.md  # EDIT menor (§5 guardarraíles: mencionar factualidad en --gate)

tests/
├── lib/validate-claim.sh             # NUEVO (gemelo de validate-citation.sh)
├── smoke/test-factuality.sh          # NUEVO (status.py contra fixtures)
└── fixtures/003-factualidad/         # NUEVO (findings.md + claims.md + manifest de prueba)

docs/compatibility-matrix.md          # EDIT (anotar que los MCP de contraste pueden emitir ClaimRecord)
CHANGELOG.md                          # EDIT (entrada de la feature)
```

> Recordatorio de la casa: los contratos viven por duplicado (raíz `contracts/` = espejo del spec 001; `writeonmars/contracts/` = el que viaja en el preset). Mantener ambos sincronizados; el preset es el que consume `specify preset add`.

---

## Diffs por archivo (al detalle, para el implementador)

### D-A. `contracts/claim-record.schema.json` y `writeonmars/contracts/claim-record.schema.json` — NUEVO

Copiar `specs/003-atribucion-factualidad/contracts/claim-record.schema.json` (ya validado contra el meta-schema Draft 2020-12 y con casos positivos/negativos) a ambas ubicaciones. Sin cambios de contenido.

### D-B. `pass-output-schema.md` → v1.1 (ambas copias)

1. Cabecera: cambiar la versión a v1.1 y añadir al `SYNC IMPACT`/nota la adición.
2. Nueva sección "## Salida de claims (pasada 4)": la pasada 4, además del bloque de findings, emite/actualiza `specs/<feature>/claims.md` con `ClaimRecord` v1.0 (referencia a `claim-record.schema.json` y a `data-model.md` § 1–2 de esta feature).
3. En "Estructura de cada Finding": permitir trazabilidad `claim_id` en hallazgos de pasada 4 (columna `Citas` admite `claim:<id>` junto a `citation_id`; o columna opcional). NO romper el orden de la tabla v1.0.
4. Añadir a "Versionado del schema" la entrada v1.1 y exigir el comentario `<!-- pass-output-schema: v1.1 -->` en bloques de pasada 4 de la feature.

### D-C. `manifest-schema.json` → MINOR (ambas copias)

Añadir a `properties` el objeto `quality_gates` exactamente como en `data-model.md` § 5 (con `additionalProperties: false`). NO añadirlo a `required`. Subir la versión MINOR en el `$id`/`$comment`/título. Verificar que un manifest existente sigue validando (test).

### D-D. `writeonmars/references/metodo/writeonmars-contraste/SKILL.md` — EDIT (núcleo del cambio de juicio)

Esta es la pieza de **juicio** (Principio VI: vive aquí, no en el script). Cambios en el "Procedimiento" y "Qué hace":

1. **Persistir todo** (FR-005): el paso que hoy solo emite findings de lo que falla pasa a emitir un `ClaimRecord` por **cada** afirmación verificable evaluada en `claims.md`. Reusar la detección de afirmaciones verificables existente como denominador.
2. **Clasificar la relación** (FR-006, US2): tras abrir la fuente (en vivo para volátiles), decidir `relacion ∈ {apoya, matiza, contradice, menciona}` y registrar `cita_fragmento_soporte` (la oración exacta de la fuente). Instrucción explícita de juicio tipo entailment: ¿la fuente *implica* la afirmación (apoya), la sostiene *con caveats* (matiza), la *contradice* (contradice) o es solo *temática* (menciona)?
3. **Derivar `soporte`** por las reglas de `data-model.md` § 1.3 (peor relación + modulación por `tipo_afirmacion`).
4. **Mapear severidad** (FR-009): emitir el finding con la severidad de la tabla. Casos nuevos respecto a hoy: `menciona`-solo en dato duro → `critico`; `matiza` → `medio`. El resto ya existe (contradice → critico; sin fuente dato duro → critico; volátil no verificado → medio; ambigüedad → bajo).
5. **Idempotencia por capítulo** (FR-007): al re-correr, reemplazar en bloque los `ClaimRecord` del capítulo objetivo; no duplicar ni tocar otros capítulos. (Análogo a cómo el modo paralelo ya consolida por capítulo sin pisar bloques previos.)
6. **No inventar fuentes**: si un `citation_id` candidato no resuelve en `research.md`, no emitir la arista; reportar (regla 2 de validación del data-model).
7. Bump de versión de la skill (sección "Versión") + actualizar "FR cubierta" con las FR de esta feature.
8. **Modo paralelo**: el dispatch por capítulo ya existente debe emitir, por sub-agente, su fragmento de `claims.md` (bloque del capítulo) y el orquestador consolidar, igual que con findings (evitar race en `claims.md`).

### D-E. `writeonmars/commands/speckit.review-precision.md` — EDIT

En "## Salida": documentar que la pasada 4 ahora produce **dos** salidas: el bloque de `findings.md` (como hoy) y el `claims.md` (nuevo). Añadir a "Inputs" la referencia a `claim-record.schema.json`. Mantener el aviso de "sin web no se finge la verificación" (ahora se traduce en `soporte: pendiente`).

### D-F. `writeonmars/scripts/status.py` — EDIT (núcleo del conteo, determinista)

Cambios acotados y aditivos (no tocar la lógica de g1·g2·g3 ni la fórmula de `approved`):

1. **`parse_claims(claims_md: Path) -> dict[str, list[dict]]`**: nuevo, gemelo de `parse_findings`. Lee los bloques ```json por capítulo (el contrato de parseo es el JSON embebido, `data-model.md` § 2). Tolera ausencia/JSON inválido → capítulo a `unmeasured`.
2. **`compute_factuality(claims_by_chapter) -> dict`**: implementa `data-model.md` § 3.1 (micro-promedio; excluye `pendiente` del denominador; `parcial` no cuenta como soportada). Devuelve `factuality_by_chapter`, `factuality_global`, `factuality_unmeasured`, `factuality_pending`.
3. **`evaluate()`**: cargar `claims.md` del `spec_dir`, llamar a `compute_factuality`, leer `manifest.quality_gates`, calcular `g4` y `gates.factuality` según § 3.2. `closeable = g1 and g2 and g3 and (g4 if blocking else True)`. Añadir los campos nuevos al dict de retorno (§ 3.3). Si g4 en rojo con `revise_pending == 0`, añadir un `warnings: [...]` (inconsistencia claims↔findings).
4. **`print_dashboard()`**: añadir una línea de factualidad (global + por capítulo + pendientes + "no medido"); añadir el gate g4 al bloque "Gates de cierre" SOLO si hay umbral.
5. **`_next_step()`**: si `gates.factuality == false` (blocking) y hay capítulos por debajo, el `next_detail` debe apuntar a que el déficit ya está (o debe estar) como findings → revise; no inventar un paso nuevo. El `next_step` sigue siendo `revise`/`review` por la vía existente.
6. **NO** añadir factualidad a la fórmula de `by_chapter[c].approved` (se mantiene `drafted ∧ {1,2,3,4} ⊆ passes_done ∧ revise_pending == 0`). Opcional aditivo: `by_chapter[c].factuality`.

### D-G. `writeonmars/scripts/export.py` — EDIT (decisión D1, ver abajo)

Implementar al menos la **validación** de la sección "Fuentes por capítulo" contra `claims.md` (FR-016). Si D1 = "generar", además regenerar la sección desde `claims.md`.

### D-H. `paperclip/agents/documentalista/bundle.md` — EDIT (refleja el juicio; rol intacto)

El bundle inlinea la tabla de severidad y apunta a la referencia agnóstica. Actualizar:
1. En "Pasada 4 · precisión": añadir que también escribe `claims.md` y clasifica la relación (apoya/matiza/contradice/menciona); reflejar la tabla de severidad ampliada (menciona-dato-duro → critico; matiza → medio).
2. En "HEARTBEAT" paso 3a: añadir "escribe `claims.md` además de `findings.md`".
3. **No** cambiar la sección de **decisión** (cuenta accionables abiertos crítico+medio → in_progress/Redactora o done/APPROVED + wake jefa). El rol en la topología es idéntico (US4/FR-018).

### D-I. `paperclip/agents/editora-jefa/HEARTBEAT.md` — EDIT menor

En "## 5 Guardarraíles antes de cerrar": añadir un bullet "`gates.factuality == false` (si el manifest declara `quality_gates` en modo blocking) → no cierres; el déficit debe estar como accionables (crítico+medio) en el ciclo por capítulo". No cambia la lógica (ya obedece `closeable`/`--gate`); es documentación para el operador/orquestador.

### D-J. `writeonmars/memory/constitution.md` y espejo — EDIT (bump MINOR)

Añadir el requisito (atribución por afirmación + índice de factualidad derivado, "Fuentes por capítulo" se conserva pero se deriva/valida). Actualizar el `SYNC IMPACT REPORT` con la versión nueva, rationale MINOR, principios tocados (IV y V) sin redefinición incompatible.

### D-K. Tests

- `tests/lib/validate-claim.sh`: valida un `ClaimRecord` contra `claim-record.schema.json` (reusar el patrón de `validate-citation.sh`; con `jsonschema` o `ajv`).
- `tests/smoke/test-factuality.sh`: corre `status.py --json` contra `tests/fixtures/003-factualidad/` con casos (a) sin `quality_gates` (retrocompat, SC-003), (b) blocking por debajo del umbral (g4 false, closeable false), (c) advisory (no bloquea), (d) capítulo `unmeasured`. Asserts sobre los campos de `data-model.md` § 3.3.
- Fixtures: un `findings.md` + `claims.md` + `.writeonmars-manifest.json` mínimos con factualidad conocida (p. ej. 8/10 → 0.8).

---

## Decisión D1 (obligatoria antes de implementar D-G) — autoría de "Fuentes por capítulo"

Hoy la **Redactora** escribe la sección "Fuentes" del capítulo (constitución MUST). Si `export.py` la **genera** desde `claims.md`, se mueve esa autoría y puede chocar con la prosa de la Redactora. Dos opciones:

- **D1-A (recomendada para v1): `claims.md` valida, no genera.** `export.py` comprueba coherencia (toda fuente del cuerpo aparece en claims; ninguna afirmación `sin_fuente`/`contradicho` llega al PDF sin marca) y falla/avisa si no cuadra. La Redactora sigue escribiendo la sección. Menor blast radius; no toca a la Redactora.
- **D1-B (v2): `claims.md` genera la sección.** `export.py` regenera "Fuentes por capítulo" desde `claims.md`. Requiere quitar esa responsabilidad de la Redactora (cambio en su bundle + constitución). Más limpio a largo plazo, mayor impacto.

El implementador DEBE confirmar D1-A salvo indicación contraria de la mantenedora. Esta es la **única** decisión que roza la frontera Redactora↔export; todo lo demás es aditivo.

---

## Transparencia con Paperclip (análisis de no-regresión)

Resumen: **transparente a la topología**. El motivo estructural (de `FLOW-CONTRACT.md` § 0): la verdad del estado vive en archivos y `status.py`; Paperclip solo orquesta relevos. `claims.md` es un archivo más del workspace, aislado por worktree como `findings.md`.

| Pieza Paperclip | ¿Cambia? | Detalle |
|---|---|---|
| Fan-out único (padre + 1 hija/capítulo) | No | La jefa hace el mismo reparto. |
| Ciclo peer-to-peer por capítulo | No | Mismos estados/relevos (`in_progress`→`in_review`→…→`done`). |
| Wake en última hija `done` → globales | No | `all_chapters_approved` se calcula igual (la fórmula de `approved` no cambia). |
| Estados/tipos/routines de Paperclip | No (0 nuevos) | FR-018; verificable contra `FLOW-CONTRACT.md` §4/§5. |
| `status.py --json` (contrato §3.7) | Aditivo | Campos nuevos; los existentes intactos (SC-003). |
| Documentalista (rol) | Solo el "cómo" | Escribe `claims.md` + clasifica relación; **decisión del ciclo idéntica**. |
| Editora jefa (HEARTBEAT) | Doc menor | Ya obedece `closeable`/`--gate`; g4 entra solo. |
| Redactora / Editora de mesa | No | Salvo D1-B (no recomendado v1). |
| Checkpoints humanos | No | Brief + PDF anotado intactos. |

**Por qué no hay deadlock** (clave del diseño): el déficit de factualidad se expresa **primero** como findings `critico`/`medio` (FR-009), así que `revise_pending > 0` y `by_chapter.approved == false` lo capturan dentro del ciclo por capítulo, **antes** de que la jefa despierte para las globales. g4 es un backstop numérico que la jefa ya enforcea vía `status.py --gate`. Si se enchufara la factualidad como gate desconectado de los findings, podrías tener "todos aprobados → jefa despierta → close falla en g4 → no hay accionable que enrutar". El diseño lo evita manteniendo el juicio dentro de la maquinería de findings.

**Sin Paperclip** (FR-019): el gate funciona igual para el runner de un solo agente vía `status.py --gate`; nada de la feature vive en la capa de orquestación.

---

## Orden de implementación (resumen; detalle en `tasks.md`)

1. Contratos (D-A, D-B, D-C) — base de datos del resto.
2. Núcleo de juicio (D-D, D-E, D-H) — la pasada 4 produce `claims.md` con relación/soporte.
3. Núcleo de conteo (D-F) — `status.py` lee y puntúa.
4. Export + constitución + jefa (D-G, D-J, D-I) — derivación/validación y gobernanza.
5. Tests (D-K) — validan 2–4.
6. Verificación de no-regresión Paperclip (US4) y docs/CHANGELOG.

Orden conceptual de las tres mejoras: **3 (relación) → 1 (persistir) → 2 (puntuar)**, pero comparten el artefacto, por eso los contratos van primero.

## Complexity Tracking

Sin desviaciones del Constitution Check que justificar. La única decisión con trade-off (D1) está acotada y resuelta hacia la opción de menor impacto (D1-A) para v1.
