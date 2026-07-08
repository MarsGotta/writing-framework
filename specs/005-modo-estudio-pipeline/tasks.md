# Tasks: Pipeline del modo estudio en el preset

**Input**: Design documents from `/specs/005-modo-estudio-pipeline/`
**Prerequisites**: plan.md, research.md (R1-R8), data-model.md, contracts/
(disposition-record.schema.json, cli-estudio.md, pass-output-v1.2-delta.md),
quickstart.md

> **LA IMPLEMENTACIÓN LA HARÁ CODEX.** Cada tarea es autocontenida: rutas
> absolutas dentro del repo, contrato de referencia y criterio verificable
> por script. Ante ambigüedad mandan `contracts/` y `research.md`.
> Regla transversal (FR-011): NINGUNA aserción de test existente se edita;
> los proyectos `mode: produccion` conservan su comportamiento exacto.

**Organización**: por user story para que cada una sea implementable y
testeable de forma independiente.

## Phase 1: Setup

- [ ] T001 Publicar los contratos v1.2: (a) aplicar
  `specs/005-modo-estudio-pipeline/contracts/pass-output-v1.2-delta.md` sobre
  `writeonmars/contracts/pass-output-schema.md` (enum `estado` + `aplazado`,
  reglas de transición por modo, huellas por bloque, marcador v1.2, cláusulas
  de modo § 5); (b) copiar
  `specs/005-modo-estudio-pipeline/contracts/disposition-record.schema.json` a
  `writeonmars/contracts/disposition-record.schema.json` (fuente única: la del
  preset); (c) añadir la sección "Modo estudio" a
  `writeonmars/contracts/executor-contract.md` con el contenido de
  `contracts/cli-estudio.md` § 5 (write/dispose ⇒ exit 10, intro humano en
  estudio, guardarraíl intacto, convención de identidad
  `<rol>@agents.writeonmars.invalid`).
- [ ] T002 [P] Fixtures en `tests/fixtures/005-estudio/`: proyecto editorial
  con `.writeonmars-manifest.json` (`mode: "estudio"`, `project_type:
  "editorial"`, resto de campos como los fixtures de
  `tests/fixtures/003-factualidad/`), `specs/001-estudio/spec.md` +
  `plan.md` con temario de 3 capítulos, `specs/001-estudio/findings.md` con
  bloques de pasada v1.2 (huellas correctas para el capítulo 1, hallazgos
  F-1.1 crítico / F-1.2 medio / F-1.3 bajo) y variantes de manifiesto
  (`manifests/produccion.json`) para los tests de retrocompatibilidad. Los
  capítulos fixture en `chapters/`.

## Phase 2: Foundational (bloquea todas las stories)

- [ ] T003 Extraer el parseo tabular de findings a un helper importable
  compartido: crear `writeonmars/scripts/findings_lib.py` con
  `parse_findings(path)` y `iter_finding_rows(text)` movidos/reexportados
  desde `status.py` (que pasa a importarlos; `sys.path` del propio
  directorio, patrón ya usado por los scripts). Prohibido duplicar el parser
  en `dispose.py`. Gate: `uvx --with pytest --with pyyaml python -m pytest
  tests/unit -q` sigue verde sin editar aserciones.
- [ ] T004 `writeonmars/scripts/status.py`: helper único
  `project_mode(manifest) -> "produccion"|"estudio"` (ausencia/None =
  produccion; valor inválido = fail con mensaje claro) y campo `"mode"` en la
  salida `--json` (data-model § 4). Solo aditivo.

## Phase 3: User Story 1 — La brújula entiende el modo estudio (P1)

**Goal**: con `mode: estudio`, `next_step` distingue turno humano
(`write`/`dispose`, no despachables) de pasadas despachables; retrocompat
total en produccion.

**Independent Test**: quickstart § 1 — fixture estudio con 0 capítulos ⇒
`next_step == "write"` y `pending_chapters == [1,2,3]`; con capítulo 1 en
disco ⇒ `next_step == "review"`; fixture produccion ⇒ salida idéntica a la
actual.

- [ ] T005 [US1] `writeonmars/scripts/status.py`: semántica estudio en
  `_next_step` (research R1, data-model §§ 4-5): la rama de capítulos
  pendientes devuelve `("write", detalle con ordinales)` y la rama de
  hallazgos accionables devuelve `("dispose", detalle con ids)` cuando
  `mode == "estudio"`; campos nuevos `pending_chapters` (ambos modos),
  `pending_dispositions` y `deferred_findings` en `--json`. En produccion
  `next_step` jamás vale `write`/`dispose`.
- [ ] T006 [US1] `writeonmars/scripts/status.py`: verificación de huellas en
  estudio (research R4, data-model § 3): leer el comentario
  `<!-- huellas: {...} -->` de cada bloque de pasada; huella registrada ≠
  sha256 actual del capítulo **o huella ausente** ⇒ esa pasada no cuenta en
  `passes_done` del capítulo, el capítulo entra en `reopened_chapters` y el
  dashboard lo explica (no evaluado ≠ verde: sin huella no hay forma de
  anclar la pasada al texto actual). En produccion no se verifica nada
  (bloques v1.1 siguen contando, FR-011).
- [ ] T007 [P] [US1] `tests/unit/test_status_estudio.py`: escenarios de
  aceptación de US1 (write con pendientes, review al aparecer capítulo,
  produccion intacta — comparar salida completa contra el fixture de
  produccion), huellas (capítulo editado tras pasada ⇒ reabierto, FR-008) y
  `mode` en JSON. Usa `tests/fixtures/005-estudio/`. Incluir un **test de
  oráculo**: la salida `--json` completa del fixture estudio comparada contra
  `tests/fixtures/005-estudio/expected-status.json` (byte a byte tras
  normalizar el orden de claves) — congela el contrato de la brújula.

**Checkpoint US1**: `pytest tests/unit/test_status_estudio.py` verde + suite
previa verde sin ediciones.

## Phase 4: User Story 2 — Pasadas sobre texto humano y disposición (P2)

**Goal**: hallazgos solo se resuelven por disposición humana registrada;
los agentes no tocan manuscrito ni estados; deuda declarada visible al cierre.

**Independent Test**: quickstart § 2 — las tres disposiciones funcionan con
sus exit codes; el atajo (editar `estado` a mano sin registro) no reduce
pendientes y produce warning.

- [ ] T008 [US2] Crear `writeonmars/scripts/dispose.py` según
  `contracts/cli-estudio.md` § 1 y data-model §§ 1-2: argumentos
  (`finding_id`, `--aceptar|--rechazar --motivo|--aplazar`, `--nota`,
  `--project-dir`, `--json`), transiciones válidas, DispositionRecord v1
  contra `writeonmars/contracts/disposition-record.schema.json`, actor de
  `git config user.name` (vacío ⇒ exit 3), rechazo sin motivo ⇒ exit 2,
  `mode != estudio` ⇒ exit 1, edición atómica de findings.md (tmp + rename)
  tocando solo la celda `estado` (+ `decision_humana` en rechazo), append a
  `specs/<feature>/disposiciones.jsonl` solo si la edición se aplicó.
- [ ] T009 [P] [US2] `tests/unit/test_dispose.py`: transiciones (las 5
  válidas y las inválidas), exit codes de la tabla del contrato, atomicidad
  (fallo simulado no deja línea huérfana), registro validable contra el
  schema, findings.md intacto salvo la celda editada.
- [ ] T010 [US2] `writeonmars/scripts/status.py`: cruce
  findings↔disposiciones en estudio (research R2, SC-005): estado no-abierto
  sin DispositionRecord compatible ⇒ warning de inconsistencia y el hallazgo
  cuenta como pendiente (`pending_dispositions`); `disposiciones.jsonl` con
  línea malformada ⇒ fail con archivo:línea (edge case de la spec). Añadir
  casos a `tests/unit/test_status_estudio.py`.
- [ ] T011 [P] [US2] Cláusulas de modo en los comandos del preset
  (pass-output-v1.2-delta § 5): `writeonmars/commands/speckit.review-structure.md`,
  `speckit.review-voice.md`, `speckit.review.md`, `speckit.review-precision.md`,
  `speckit.review-global.md` (prohibido editar `chapters/`/`README.md` y
  cambiar `estado`; emitir el comentario de huellas en TODOS los bloques de
  pasada, `"global"` en la 5; la pasada 4 en estudio sin fichas aplicables en
  `roots/` declara "no evaluable contra fuentes" en vez de 0 hallazgos —
  delta § 5); `speckit.revise.md` y `speckit.implement.md`
  (en estudio no aplican: detenerse sin tocar archivos y explicar el flujo
  humano — write/dispose).
- [ ] T012 [US2] `writeonmars/scripts/close.py`: al componer el resumen de
  cierre, enumerar hallazgos `aplazado` como "deuda declarada" (id,
  severidad, capítulo) en ambos modos (FR-007). Test en
  `tests/unit/test_close.py` (añadir casos, sin editar los existentes).

**Checkpoint US2**: quickstart § 2 reproducible; pytest verde.

## Phase 5: User Story 3 — Informe de autoría humana (P3)

**Goal**: informe determinista por capítulo desde git + decisions.jsonl,
honesto en proyectos convertidos.

**Independent Test**: quickstart § 4 — dos ejecuciones idénticas; fixture
mixto clasifica agente/humano correctamente.

- [ ] T013 [US3] Crear `writeonmars/scripts/authorship.py` según
  `contracts/cli-estudio.md` § 2 y data-model § 6: `git log --numstat
  --follow` sobre `chapters/`, clasificación por identidad
  (`*@agents.writeonmars.invalid`) ∨ ventana dispatch→disposition de
  `implement|revise|intro` en `decisions.jsonl`, veredicto por capítulo
  (`humana|mixta|ia`) y global (`autoria_humana_demostrada` solo si todos
  humanos), salida `authorship-report.md` + `--json`, sin timestamps de
  generación (declara HEAD), exit 1 sin repo/commits, exit 3 sin git.
- [ ] T014 [P] [US3] `tests/unit/test_authorship.py`: construye en tmp un
  repo git real (subprocess git init/commit con autores humanos y
  `redactora@agents.writeonmars.invalid`) + `decisions.jsonl` con ventanas de
  despacho; asserts de clasificación, veredictos, determinismo (dos corridas
  byte a byte iguales, SC-003) y honestidad en proyecto convertido (US3
  escenario 2).

**Checkpoint US3**: pytest verde.

## Phase 6: Integración con el ejecutor (depende de US1; US2 para el e2e)

- [ ] T015 `vivarium/crates/vivarium-core/src/sidecar.rs`: campos nuevos de
  `Status` con `#[serde(default)]` — `mode: Option<String>`,
  `pending_chapters: Vec<u32>`, `pending_dispositions: Vec<String>`,
  `deferred_findings: Vec<String>`, `reopened_chapters: Vec<String>` —
  tolerante a salidas de status.py antiguas (campos ausentes = default).
- [ ] T016 `vivarium/crates/vivarium-core/src/runner.rs` (research R6,
  cli-estudio § 5): brazos `"write"` y `"dispose"` en `plan_action` ⇒
  `Planned::Checkpoint` (mensajes del contrato; `append_checkpoint_once`
  evita duplicados, mismo patrón que `specify`); en la rama de
  **normalización** (`next_step == "close"` con capítulos sin aprobar), si
  `mode == estudio`: capítulo sin redactar ⇒ Checkpoint `write` y revise
  pendiente ⇒ Checkpoint `dispose` (nunca `Act(implement/revise)`, que
  chocaría con el guardarraíl en vez de esperar al humano); en `plan_global`,
  si el manifiesto declara `mode == estudio` y falta `README.md` ⇒
  `Planned::Checkpoint{step: "intro"}` en lugar de despachar a la Redactora.
  PROHIBIDO tocar `writes_manuscript`, `blocked_by_mode` y los exit codes.
  Unit tests del planificador junto a los existentes en `runner.rs`
  (incluido el caso de normalización en estudio).
- [ ] T017 [P] Tests de integración del ejecutor en
  `vivarium/crates/vivarium-cli/tests/runner.rs` (stubs existentes de
  `tests/common/mod.rs` + fixture estudio): `vivarium run` sobre proyecto
  estudio con capítulos pendientes ⇒ exit 10 y checkpoint `write` en
  decisions.jsonl (sin dispatch de `implement`); con hallazgos abiertos ⇒
  exit 10 checkpoint `dispose`; etapa global sin README ⇒ exit 10 checkpoint
  `intro`. Gate: `cd vivarium && cargo test --workspace`.

## Phase 7: Polish & e2e

- [ ] T018 Smoke `tests/smoke/estudio-e2e.sh` implementando quickstart § 5
  (stubs deterministas; los stubs de pasada emiten findings v1.2 CON
  huellas correctas; skip exit 99 si falta `cargo`, convención de
  `tests/smoke/run-all.sh`) y alta del test en la lista `tests` de
  `tests/smoke/run-all.sh`. Asserts finales: cero dispatch de
  `implement|revise|intro`, checkpoints `write`/`dispose` sin duplicados,
  `authorship.py` ⇒ `autoria_humana_demostrada`, segundo run exit 0 sin
  despachos nuevos.
- [ ] T019 [P] Crear `writeonmars/docs/how-to-modo-estudio.md` (research R8):
  cómo nombrar capítulos según el temario, correr pasadas (a mano o vía
  ejecutor), disponer hallazgos con `dispose.py`, leer el informe de
  autoría; enlazado desde `writeonmars/docs/README.md` si existe índice.
- [ ] T020 [P] Docs: entrada de la feature en `CHANGELOG.md`, estado en
  `ROADMAP.md` (pipeline estudio operativo) y mención del modo estudio en
  `vivarium/README.md` § Estado (checkpoints write/dispose/intro).
- [ ] T021 Gate final (SC-006): `uvx --with pytest --with pyyaml python -m
  pytest tests/unit -q` + `bash tests/smoke/run-all.sh` + `cd vivarium &&
  cargo test --workspace` — todo verde, sin pasos manuales no documentados.

## Dependencies & Execution Order

- **Phase 1 → todo**: T001 (contratos) precede al código; T002 es
  paralelizable con T001.
- **Phase 2 bloquea las stories**: T003 (helper) es prerrequisito de T005-T006
  (status) y T008 (dispose); T004 de T005.
- **US1 (T005-T007)** solo depende de Foundational. **MVP = US1**.
- **US2 (T008-T012)**: T008 depende de T003; T010 depende de T005 y T008;
  T011 y T012 son paralelizables entre sí y con T008-T010.
- **US3 (T013-T014)**: independiente de US1/US2 (solo T002 como apoyo);
  paralelizable con la Phase 4.
- **Phase 6**: T015-T016 dependen de US1 (contrato de status); T017 de T016.
  El checkpoint `dispose` de T017 requiere T008 para el flujo completo del
  smoke, pero el test de integración puede fijar el estado con fixtures.
- **Phase 7**: T018 depende de todo lo anterior; T019/T020 en cualquier
  momento tras US2; T021 al final.

## Parallel Examples

```bash
# Tras Phase 2, tres frentes independientes:
#   Frente A (US1): T005 → T006 → T007
#   Frente B (US3): T013 → T014
#   Frente C (docs/comandos): T011, T019
# Tras US1: Phase 6 (T015 → T016 → T017) en paralelo con US2 (T008-T012).
```

## Implementation Strategy

MVP primero: US1 deja un proyecto estudio con estado veraz (aunque el ciclo de
disposición aún no exista, la brújula ya no pide redactar a la IA). Cada
checkpoint de fase exige la suite completa en verde antes de avanzar — la
regla FR-011 (retrocompat produccion) se verifica en cada checkpoint, no solo
al final.
