# Implementation Plan: Pipeline del modo estudio en el preset

**Branch**: `005-modo-estudio-pipeline` | **Date**: 2026-07-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-modo-estudio-pipeline/spec.md`

> **LA IMPLEMENTACIÓN LA HARÁ CODEX.** Este plan es autocontenido y
> agente-neutral (Principio VI): no depende de skills de ningún proveedor.
> Todo criterio de aceptación es verificable por script. Ante ambigüedad,
> los contratos de `contracts/` y las decisiones de `research.md` mandan.

## Summary

El modo estudio (constitución v1.6.0: el humano escribe, la IA MUST NOT
redactar prosa del manuscrito) existe como norma y como guardarraíl del
ejecutor, pero el preset no sabe operarlo: `status.py` pide "delegar a
Redactora" ante capítulos faltantes y no hay ciclo para que el humano
disponga de los hallazgos. Esta feature completa el pipeline: (1) brújula
consciente de modo con dos checkpoints humanos nuevos (`write`, `dispose`);
(2) pasadas 1-5 sobre texto humano con huella de contenido que ancla la
aprobación a lo revisado; (3) `dispose.py` — único camino para resolver
hallazgos, con registro auditable (`disposiciones.jsonl`); (4)
`authorship.py` — informe de autoría humana desde git + `decisions.jsonl`;
(5) mapeo en el ejecutor Vivarium (checkpoints exit 10) sin tocar el
guardarraíl exit 11.

## Technical Context

**Language/Version**: Python 3.9+ (scripts del preset, stdlib; `authorship.py`
invoca el binario `git`); Rust 1.75 (mapeo en `vivarium/`); Bash 3.2-compatible
(smoke).
**Primary Dependencies**: ninguna nueva. Preset: stdlib. Vivarium: las del
workspace existente (serde_json preserve_order, fd-lock, git2…).
**Storage**: archivos del proyecto editorial — `findings.md` (esquema
pass-output v1.2), `disposiciones.jsonl` (nuevo, append-only),
`authorship-report.md` (derivado), `.writeonmars-manifest.json` (campo `mode`
ya existente, v1.3.0).
**Testing**: `uvx --with pytest --with pyyaml python -m pytest tests/unit -q`;
`bash tests/smoke/run-all.sh` (nuevo `estudio-e2e.sh`, skip 99 sin cargo);
`cd vivarium && cargo test --workspace`.
**Target Platform**: macOS + Linux, CLI.
**Project Type**: software (preset + ejecutor). Sin secciones editoriales.
**Performance Goals**: `status.py` sigue siendo instantáneo (<1 s en proyectos
de ~50 capítulos); el hash sha256 por capítulo es O(tamaño del capítulo).
**Constraints**: retrocompatibilidad total en `mode: produccion` (FR-011:
ninguna aserción existente se edita); determinismo (sin LLM) en dispose.py,
authorship.py y toda la lógica de estado; frontera dura preset↔ejecutor.
**Scale/Scope**: 2 scripts nuevos, 1 script extendido (`status.py`), 1 cambio
aditivo (`close.py`), ~6 comandos con cláusula de modo, contrato pass-output
v1.2, 1 schema nuevo, mapeo en `runner.rs`, ~3 archivos de test nuevos + 1
smoke.

## Constitution Check

| Principio | Conformidad | Evidencia |
|-----------|-------------|-----------|
| **I. Voz natural y sobria** (NO NEGOCIABLE) | pasa | Feature de tooling; no produce prosa. Los textos de `next_detail` y mensajes de checkpoint siguen el tono sobrio existente. |
| **II. Estructura situación → explicación → consecuencia** | pasa (N/A editorial) | Sin capítulos nuevos. La plantilla didáctica no se toca. |
| **III. Brief obligatorio** (NO NEGOCIABLE) | pasa | El checkpoint 1 (brief firmado) se mantiene idéntico en modo estudio (FR-012). |
| **IV. Precisión léxica** | pasa | Términos nuevos definidos una sola vez en contratos: disposición, huella, deuda declarada, checkpoint de escritura. |
| **V. Revisión multi-pasada** (NO NEGOCIABLE) | pasa | Las 5 pasadas se conservan en estudio operando sobre texto humano; "detector ≠ corrector" se refuerza: el corrector es el humano (§ Modos). |
| **VI. Neutralidad de agente y modelo** (NO NEGOCIABLE) | pasa | Toda la lógica nueva vive en scripts deterministas y comandos Markdown del preset; el ejecutor solo mapea. Implementación por Codex exigida. |
| **Modo de proyecto** (§ Modos) | pasa — es el objeto de la feature | Ninguna tarea del plan redacta prosa; los pasos que la redactarían se convierten en checkpoints humanos. El guardarraíl del ejecutor no se modifica. |

Sin desviaciones → Complexity Tracking vacío.

## Project Structure

### Documentation (this feature)

```text
specs/005-modo-estudio-pipeline/
├── plan.md              # Este archivo
├── research.md          # R1-R8: decisiones fijadas
├── data-model.md        # DispositionRecord, estados v1.2, huellas, JSON de status, AuthorshipReport
├── quickstart.md        # Recorrido de validación por escenario
├── contracts/
│   ├── disposition-record.schema.json   # Schema canónico del registro de disposición
│   ├── cli-estudio.md                   # Contrato CLI de dispose.py/authorship.py + deltas status/close/ejecutor
│   └── pass-output-v1.2-delta.md        # Delta del contrato de pasadas (estado aplazado, huellas, cláusulas de modo)
└── tasks.md             # Output de /speckit-tasks
```

### Source Code (repository root)

```text
writeonmars/
├── scripts/
│   ├── status.py        # EXTENDER: mode, write/dispose, huellas, cruce disposiciones, campos JSON nuevos
│   ├── dispose.py       # NUEVO: disposición humana (contracts/cli-estudio.md § 1)
│   ├── authorship.py    # NUEVO: informe de autoría (contracts/cli-estudio.md § 2)
│   └── close.py         # ADITIVO: deuda declarada (aplazados) en el resumen de cierre
├── contracts/
│   ├── pass-output-schema.md            # ACTUALIZAR a v1.2 (aplicar pass-output-v1.2-delta.md)
│   ├── disposition-record.schema.json   # NUEVO (copiar del contrato de la feature; fuente única aquí)
│   └── executor-contract.md             # AÑADIR sección "Modo estudio" (cli-estudio.md § 5)
├── commands/
│   ├── speckit.review-structure.md      # Cláusula de modo (pass-output-v1.2-delta.md § 5)
│   ├── speckit.review-voice.md          # ídem
│   ├── speckit.review.md                # ídem (pasada 3 / genérica)
│   ├── speckit.review-precision.md      # ídem + emisión de huellas
│   ├── speckit.review-global.md         # ídem (huella "global")
│   ├── speckit.revise.md                # Cláusula de no-aplicación en estudio
│   └── speckit.implement.md             # Cláusula: en estudio NO aplica (la escritura es humana)
└── docs/
    └── how-to-modo-estudio.md           # NUEVO: guía de la escritora (nombrar capítulos, dispose, informe)

vivarium/crates/vivarium-core/src/
├── runner.rs            # plan_action: write/dispose → Planned::Checkpoint; plan_global: intro → Checkpoint si estudio
└── sidecar.rs           # Status: deserializar campos nuevos (mode, pending_*, …) — aditivo, tolerante a ausencia

tests/
├── unit/
│   ├── test_status_estudio.py   # NUEVO: US1 + huellas + cruce disposiciones
│   ├── test_dispose.py          # NUEVO: transiciones, exit codes, atomicidad
│   └── test_authorship.py       # NUEVO: clasificación, determinismo, repo fixture
├── fixtures/005-estudio/        # NUEVO: proyecto estudio + findings con huellas + repo git fixture
└── smoke/
    ├── estudio-e2e.sh           # NUEVO: quickstart § 5 con stubs (skip 99 sin cargo)
    └── run-all.sh               # AÑADIR estudio-e2e.sh a la lista
```

**Structure Decision**: opción "single project" adaptada al monorepo real:
la lógica editorial en `writeonmars/` (preset), el mapeo en `vivarium/`
(ejecutor), tests en `tests/` — misma partición que la feature 004.

## Diseño (resumen ejecutable; detalle en research.md y contracts/)

1. **`status.py`** (R1, data-model § 4-5): lee `mode` del manifiesto (helper
   único `project_mode(manifest) -> str`). En `_next_step`, tras las ramas de
   `implement` y `revise`, si `mode == "estudio"` esas ramas devuelven
   `("write", …)` y `("dispose", …)` respectivamente. `revise_pending` en
   estudio se calcula sobre hallazgos abiertos **validados** contra
   `disposiciones.jsonl` (estado no-abierto sin registro ⇒ cuenta como
   abierto + warning). Verificación de huellas (R4) solo en estudio: pasada
   sin huella coincidente no entra en `passes_done` del capítulo y el
   capítulo entra en `reopened_chapters`.
2. **`dispose.py`** (R2, R3, cli-estudio § 1): parsea findings.md con la
   misma lógica tabular de `status.py` (extraer helper compartido si hace
   falta, sin duplicar parsers), valida transición, escribe JSONL + celda
   `estado` de forma atómica (tmp + rename para findings.md).
3. **`authorship.py`** (R5, data-model § 6): `git log --numstat` sobre
   `chapters/`, clasificación por identidad + ventanas de despacho,
   veredictos por capítulo y global, salida md + json determinista.
4. **`close.py`**: al componer el resumen de cierre, listar hallazgos
   `aplazado` como deuda declarada (id, severidad, capítulo).
5. **Comandos** (pass-output-v1.2-delta § 5): cláusula de modo en pasadas
   (prohibido editar `chapters/`/`README.md` y tocar `estado`), emisión de
   huellas en todos los bloques de pasada, `speckit.revise`/`speckit.implement`
   se auto-anulan en estudio explicando el flujo humano.
6. **Vivarium** (R6, cli-estudio § 5): en `plan_action`, brazos nuevos
   `"write"` y `"dispose"` → `Planned::Checkpoint` (mismo mecanismo que
   `specify`; `append_checkpoint_once` evita duplicados). En `plan_global`,
   si `mode == estudio` y falta README → `Planned::Checkpoint{step:"intro"}`.
   `Status` gana los campos nuevos con `#[serde(default)]` (tolerante a
   status.py antiguos). `writes_manuscript` y `blocked_by_mode` NO se tocan.
7. **Docs**: `how-to-modo-estudio.md` — cómo nombra la escritora sus
   capítulos (según temario), cómo corre las pasadas (o deja que el ejecutor
   las despache), cómo dispone (`dispose.py`), cómo genera el informe.

## Orden de implementación sugerido

1. Contratos publicados (pass-output v1.2, disposition schema, sección modo
   estudio del executor-contract) — fijan la verdad antes del código.
2. `status.py` + fixtures + `test_status_estudio.py` (US1 verde).
3. `dispose.py` + `test_dispose.py` (US2 núcleo).
4. Comandos con cláusulas + huellas (US2 completo a nivel de contrato).
5. `authorship.py` + `test_authorship.py` (US3).
6. `close.py` aditivo.
7. Vivarium: mapeo + tests de integración con stubs.
8. `estudio-e2e.sh` + alta en `run-all.sh`; gates completos (SC-006).

## Riesgos y mitigaciones

- **Regresión en produccion**: mitigado por FR-011 como contrato (ningún test
  existente se edita) + campos JSON solo aditivos + verificaciones nuevas
  condicionadas a `mode == estudio`.
- **Parsers duplicados de findings.md** (status.py vs dispose.py): extraer la
  función de parseo tabular a un helper importable dentro de `scripts/`
  (p. ej. `findings_lib.py`) usado por ambos; prohibido copiar-pegar el parser.
- **Ejecutores antiguos ante `write`/`dispose`**: un vivarium 004 sin el mapeo
  devolvería `Validation("next_step desconocido")` (exit 5) — falla ruidosa y
  segura, no silenciosa; documentado en el contrato del ejecutor.
- **findings.md editado a mano**: el cruce con disposiciones.jsonl degrada a
  warning + hallazgo pendiente; nunca crash (edge case de la spec).
