# Implementation Plan: Núcleo headless de Vivarium (ejecutor del método)

**Branch**: `004-vivarium-core` | **Date**: 2026-07-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-vivarium-core/spec.md`

> **Para quien implementa (Codex u otro agente)**: este plan es autocontenido.
> Todo lo que necesitas está en artefactos del repo: la spec (requisitos y
> criterios), este plan (stack y estructura), `research.md` (decisiones
> técnicas con su porqué), `data-model.md` (entidades y transiciones),
> `contracts/` (superficies exactas) y `quickstart.md` (cómo compilar,
> probar y verificar). No dependas de skills, memoria de sesión ni
> convenciones de un agente concreto. Ante ambigüedad: la spec manda; después
> el contrato del ejecutor; después este plan.

## Summary

Vivarium sustituye a Paperclip como ejecutor orquestado del método
Write.OnMars (constitución v1.6.0 § Ejecutores del método). Esta feature
construye su núcleo headless en `vivarium/` (workspace Cargo, sin UI):

1. **Bootstrap** de proyecto editorial en una orden (repo + preset + manifiesto
   con `mode` + `roots/` + `decisions.jsonl` + commit base), generalizando
   `tools/new-guide.sh`.
2. **Runner por estados** que lee `status.py --json`, despacha agentes BYOM
   (órdenes de CLI configurables por rol) respetando las reglas de relevo del
   método, con idempotencia estructural (lock + re-verificación en disco).
3. **Modos** `produccion`/`estudio` en el manifiesto, con guardarraíl duro en
   estudio (jamás despachar redacción) y cambio de modo explícito y registrado.
4. **Contrato del ejecutor** promovido de `paperclip/FLOW-CONTRACT.md` §§ 0-2 a
   `writeonmars/contracts/executor-contract.md`.

## Technical Context

**Language/Version**: Rust estable (MSRV 1.75, edition 2021) para el núcleo;
Python 3.11+ existente como sidecar (scripts del preset, **no se portan**)
**Primary Dependencies**: `clap` v4 (CLI, derive), `serde`/`serde_json`
(contratos JSON), `toml` (config BYOM), `git2` (operaciones git del bootstrap),
`fd-lock` (lock de proyecto), `thiserror`/`anyhow` (errores). Subprocesos:
`python3` (sidecar), `specify` CLI (instalación del preset), órdenes BYOM de
los agentes
**Storage**: solo archivos en el repo del proyecto editorial (manifiesto,
`decisions.jsonl`, `findings.md`, …). El ejecutor no tiene base de datos ni
estado propio persistente (FR-003); su única escritura fuera del método es
`.vivarium/` (config BYOM y lock, no versionado)
**Testing**: `cargo test` (unit + integración con agentes stub vía
`assert_cmd`) + suite existente del repo (`pytest tests/unit`, smoke). Gate:
todo en verde (SC-006)
**Target Platform**: macOS y Linux (desarrollo local-first); Windows queda
fuera de esta feature
**Project Type**: cli/library (workspace Cargo: `vivarium-core` librería +
`vivarium-cli` binario)
**Performance Goals**: sin metas de rendimiento propias; el cuello es la
inferencia de los agentes. Único límite: la evaluación de estado
(status.py + decisión de despacho) < 2 s por iteración
**Constraints**: implementación por Codex (artefactos autocontenidos y
agente-neutrales); frontera dura de `vivarium/README.md` (solo archivos +
scripts + comandos); scripts Python como sidecar por subproceso; Tauri fuera
de alcance
**Scale/Scope**: un proyecto editorial a la vez por runner (lock); guías de
hasta ~20 capítulos; 2 crates, ~6 órdenes de CLI

## Constitution Check

*GATE: debe pasar antes de Phase 0 research. Re-evaluar después de Phase 1
design.* `project_type=software`: los Principios I-V gobiernan la prosa que el
método produce; a esta feature le aplican como **obligación de preservarlos**
(el runner ejecuta el método, no lo redefine). VI y Modo aplican de lleno.

| Principio | Conformidad | Evidencia |
|-----------|-------------|-----------|
| **I. Voz natural y sobria** (NO NEGOCIABLE) | pasa | El runner no genera prosa (FR-013, US2-AS4: "jamás escribe prosa del manuscrito por su cuenta"); despacha los comandos del preset, que cargan la pirámide de prosa. |
| **II. Estructura situación → explicación → consecuencia** | pasa | Sin efecto: la estructura la imponen los comandos `speckit.*` despachados, no el ejecutor. |
| **III. Brief obligatorio** (NO NEGOCIABLE) | pasa | El runner se detiene en el checkpoint del brief y no avanza sin la acción humana (FR-013); no puede saltarse `specify`. |
| **IV. Precisión léxica y sintaxis al servicio de la cohesión** | pasa | Sin efecto directo; la pasada 4 y `claims.md` siguen siendo despachos del método (FR-004/FR-005). |
| **V. Revisión multi-pasada** (NO NEGOCIABLE) | pasa | El ciclo por capítulo del runner implementa exactamente 3 locales + 1 global con voz ≠ precisión y detector ≠ corrector (FR-004, FR-005); crítico+medio fuerza revise. |
| **VI. Neutralidad de agente y modelo** (NO NEGOCIABLE) | pasa | BYOM por configuración (FR-007, ≥2 agentes demostrados); ninguna lógica de negocio en el ejecutor (FR-003, § Ejecutores del método); el propio desarrollo es agente-neutral (implementa Codex). |
| **Modo de proyecto** (§ Modos de proyecto) | pasa | `mode` en el manifiesto (FR-002), guardarraíl de estudio (FR-008), cambio explícito registrado (FR-009). Ninguna tarea del plan redacta prosa de manuscrito. |

**Post-design re-check (tras Phase 1)**: pasa — los contratos generados
(`contracts/`) mantienen toda la lógica editorial en el método (preset +
sidecar) y el ejecutor solo orquesta relevos. Sin desviaciones que justificar.

## Project Structure

### Documentation (this feature)

```text
specs/004-vivarium-core/
├── spec.md              # Especificación (cerrada, checklist 16/16)
├── plan.md              # Este archivo
├── research.md          # Phase 0 — decisiones técnicas resueltas
├── data-model.md        # Phase 1 — entidades, estados, transiciones
├── quickstart.md        # Phase 1 — cómo compilar, probar, verificar (para Codex)
├── contracts/           # Phase 1 — superficies exactas
│   ├── executor-contract.md      # borrador a publicar en writeonmars/contracts/
│   ├── cli-vivarium.md           # órdenes y exit codes del CLI
│   ├── byom-config.md            # formato .vivarium/config.toml
│   ├── decision-record.schema.json  # línea de decisions.jsonl (v1)
│   └── manifest-mode.md          # extensión exacta del manifest-schema
├── checklists/requirements.md   # checklist de la spec
└── tasks.md             # Phase 2 (/speckit-tasks, siguiente comando)
```

### Source Code (repository root)

```text
vivarium/
├── Cargo.toml           # workspace: members = ["crates/vivarium-core", "crates/vivarium-cli"]
├── README.md            # ya existe: frontera dura (no tocar la regla)
└── crates/
    ├── vivarium-core/   # librería de dominio (sin I/O de terminal)
    │   ├── Cargo.toml
    │   └── src/
    │       ├── lib.rs
    │       ├── bootstrap.rs   # FR-001/FR-002: creación de proyecto
    │       ├── manifest.rs    # lectura/escritura del manifiesto, mode + mode_history
    │       ├── sidecar.rs     # invocación de python3/status.py, parseo del JSON
    │       ├── state.rs       # derivación de estados por capítulo (data-model § 3)
    │       ├── dispatch.rs    # relevos: plantillas BYOM, reglas de asignación
    │       ├── runner.rs      # bucle step/run, lock, idempotencia, checkpoints
    │       ├── decisions.rs   # append a decisions.jsonl (schema v1)
    │       └── error.rs
    └── vivarium-cli/    # binario `vivarium` (clap)
        ├── Cargo.toml
        └── src/main.rs  # subcomandos → llamadas a vivarium-core (shell fino)

tests/smoke/vivarium-e2e.sh   # e2e con agentes stub (SC-002); se suma a run-all.sh
writeonmars/contracts/executor-contract.md   # contrato promovido (FR-011)
writeonmars/contracts/manifest-schema.json   # + campo mode / mode_history (FR-002)
```

**Structure Decision**: workspace Cargo en `vivarium/` con la lógica en
`vivarium-core` (librería testeable) y `vivarium-cli` como shell fino — es el
patrón que permitirá a la app Tauri consumir el mismo crate sin reescritura.
Los tests de integración viven en `vivarium/crates/*/tests/`; el smoke e2e en
`tests/smoke/` junto a los existentes. Nada fuera de `vivarium/` salvo los dos
contratos del preset (FR-011, FR-002) y el smoke.

## Complexity Tracking

Sin desviaciones del Constitution Check: tabla vacía.
