# Quickstart — handoff para el agente implementador

**Feature**: `003-atribucion-factualidad` · Atribución por afirmación + gate de factualidad.

## Qué es esto

Un mini-spec completo y autocontenido para implementar tres mejoras (un solo modelo de datos) que llevan la verificación de fuentes de Write.OnMars del grano **capítulo** al grano **afirmación**, alineándola con el estado del arte en generación long-form con citas. Toda la justificación de diseño está respaldada por investigación de métodos en producción (`research.md`, con fuentes).

## Orden de lectura

1. **`spec.md`** — qué se construye y por qué: resumen, user stories, FRs, success criteria, alcance y out-of-scope.
2. **`research.md`** — la investigación que fundamenta cada decisión (STORM, Attribute-First, Citations API, FActScore/VeriScore/RARR, Scite) + tabla hallazgo→decisión. Con fuentes.
3. **`data-model.md`** — el `ClaimRecord` v1.0, las adiciones a `pass-output-schema` (v1.1) y `manifest-schema` (MINOR), y el algoritmo determinista de factualidad.
4. **`contracts/claim-record.schema.json`** — el JSON Schema canónico (ya validado contra Draft 2020-12 y con casos positivos/negativos).
5. **`plan.md`** — diffs por archivo, decisión D1, análisis de transparencia con Paperclip, orden de implementación.
6. **`tasks.md`** — lista de tareas T001…T042 con dependencias y DoD por tarea.

## La idea en una frase

La pasada 4 (`writeonmars-contraste`) **ya** extrae afirmaciones, las mapea a fuentes y verifica en vivo; hoy descarta ese trabajo salvo cuando algo falla. Esta feature lo **persiste** (`claims.md`), le añade el **veredicto de relación** (apoya/matiza/contradice/menciona) y lo **cuenta** en `status.py` como índice de factualidad con gate configurable.

## Las dos reglas que no se pueden romper

1. **Juicio ≠ conteo** (Principio VI): toda decisión de relación/soporte vive en la referencia agnóstica de la pasada 4; todo cálculo numérico vive en `status.py`. Nunca al revés.
2. **El déficit de factualidad se enruta por la maquinería de findings→revise existente** (FR-009). El gate g4 es un backstop, no una vía nueva. Esto es lo que mantiene el cambio transparente a Paperclip y evita deadlocks.

## Antes de escribir código

- Confirmar **Decisión D1** con la mantenedora (`plan.md` § D1; default D1-A: `claims.md` valida la sección "Fuentes", no la genera). Es lo único que roza la frontera Redactora↔export.
- Recordar que los contratos viven **por duplicado**: raíz `contracts/` (espejo del spec 001) y `writeonmars/contracts/` (el que viaja en el preset). Mantener ambos en sync.

## Cómo verificar el resultado

- `tests/smoke/test-factuality.sh` (T032): retrocompat sin `quality_gates`, blocking/advisory, `unmeasured`, y que `menciona`-en-dato-duro baja el índice.
- `tests/lib/validate-claim.sh` (T030): valida `ClaimRecord` contra el esquema.
- No-regresión Paperclip (T033): 0 tipos/estados/routines nuevos; la Documentalista decide igual.
