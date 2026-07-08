# Tasks: Núcleo headless de Vivarium (ejecutor del método)

**Input**: Design documents from `/specs/004-vivarium-core/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

> **Para quien implementa (Codex)**: lee `quickstart.md` primero (orden de
> lectura y de trabajo). Cada tarea es autocontenida: cita el artefacto que la
> define. Los tests van incluidos porque la spec los exige (SC-006: todo
> criterio verificable por script). Ningún test llama a un proveedor de IA:
> los agentes de test son stubs (research.md R11). Commit por tarea o grupo
> lógico.

**Organization**: fases Setup / Foundational / User Stories (US1→US3) / Polish.
Formato: `- [ ] [ID] [P?] [Story?] Descripción con ruta exacta`.

## Phase 1: Setup

**Purpose**: workspace compilable y verificable desde el minuto uno.

- [x] T001 Crear el workspace Cargo: `vivarium/Cargo.toml` (members =
  crates/vivarium-core, crates/vivarium-cli; edition 2021, rust-version 1.75) +
  `vivarium/crates/vivarium-core/{Cargo.toml,src/lib.rs}` +
  `vivarium/crates/vivarium-cli/{Cargo.toml,src/main.rs}` (stub clap con
  `--version`). Dependencias según plan.md § Technical Context. Gate:
  `cargo test --workspace` verde (trivial) y `cargo clippy` sin warnings.
- [x] T002 [P] Tipos de error base: `vivarium/crates/vivarium-core/src/error.rs`
  (thiserror; variantes para entorno incompleto, validación, lock, sidecar,
  despacho — alineadas 1:1 con los exit codes de contracts/cli-vivarium.md) y
  mapeo error→exit code en `vivarium/crates/vivarium-cli/src/main.rs`.

**Checkpoint**: `cd vivarium && cargo test --workspace` compila y pasa.

---

## Phase 2: Foundational (bloquea todas las user stories)

**Purpose**: los tres contratos de lectura/escritura que todo lo demás consume
(sidecar, manifiesto, registro de decisiones) + el bump del manifest-schema.

- [x] T003 Implementar `vivarium/crates/vivarium-core/src/sidecar.rs`:
  resolución del intérprete (`VIVARIUM_PYTHON` → `python3`, research.md R3),
  invocación de `.specify/presets/writeonmars/scripts/status.py --json` con
  cwd = proyecto, deserialización serde de TODOS los campos del
  executor-contract § 3 (`next_step`, `by_chapter`, `all_chapters_approved`,
  `revise_by_chapter`, `gates`, `closeable`, …). Unit tests contra el fixture
  real `tests/fixtures/003-factualidad-project/` (copiar a
  `vivarium/crates/vivarium-core/tests/fixtures/` si hace falta aislar).
- [x] T004 [P] Implementar `vivarium/crates/vivarium-core/src/manifest.rs`:
  lectura/escritura de `.writeonmars-manifest.json`, tipos `Mode`
  (`produccion`|`estudio`) y `ModeChange {from,to,date}`, regla ausencia =
  `produccion`, valor inválido = error de validación (edge case de spec.md).
  Unit tests: con `mode`, sin `mode`, `mode` inválido.
- [x] T005 [P] Extender el manifest-schema según
  `specs/004-vivarium-core/contracts/manifest-mode.md`: editar
  `writeonmars/contracts/manifest-schema.json` (v1.2.1 → v1.3.0, `$id`,
  `title`, `$comment`, propiedades `mode` y `mode_history`); añadir el paso de
  `mode` a `writeonmars/scripts/bootstrap.py` (argumento/entorno, default
  `produccion`); casos nuevos en `tests/unit/test_bootstrap.py` (manifest con
  cada modo valida; sin modo valida) y fixture `estudio` en
  `tests/unit/conftest.py`; entrada en `CHANGELOG.md`. Gate:
  `uvx --with pytest --with pyyaml python -m pytest tests/unit -q` verde.
- [x] T006 [P] Implementar `vivarium/crates/vivarium-core/src/decisions.rs`:
  append-only de líneas conforme a
  `specs/004-vivarium-core/contracts/decision-record.schema.json` (v1, eventos
  dispatch/disposition/mode_change/checkpoint), lectura para computar
  `in_flight` (dispatch sin disposition, correlación step+chapter+orden).
  Unit tests de escritura, lectura y correlación.

**Checkpoint**: `cargo test --workspace` + `pytest tests/unit` verdes; el core
lee estado real, manifiesto y decisions.

---

## Phase 3: User Story 1 — Crear un proyecto editorial listo en una orden (P1) 🎯 MVP

**Goal**: `vivarium new` deja un repo editorial operativo (FR-001/FR-002),
paridad con `tools/new-guide.sh`.

**Independent Test**: sobre un directorio vacío, `vivarium new` produce un
proyecto donde el manifiesto valida contra el schema, `status.py --json`
responde y el commit base existe — sin editar nada a mano (SC-001).

- [x] T007 [US1] Implementar
  `vivarium/crates/vivarium-core/src/bootstrap.rs`: verificación de entorno
  (git, python3, `specify` — error accionable, exit 3), git2 init + commit
  base, subprocesos `specify init` / `specify preset add` (research.md R4),
  invocación de `bootstrap.py` con el modo resuelto, mapeo `--kind`→`mode`
  (data-model § 2) y `--sector` (default `tecnologia` en kinds de producción),
  creación de `roots/README.md` (convención de fichas, data-model § 5),
  `decisions.jsonl` vacío, `.vivarium/` en `.gitignore`,
  `.vivarium/config.toml.example` (plantilla de contracts/byom-config.md).
  Idempotente: re-ejecutar no duplica ni destruye.
- [x] T008 [US1] Cablear el subcomando `vivarium new` en
  `vivarium/crates/vivarium-cli/src/main.rs` con los flags del contrato
  (contracts/cli-vivarium.md § new) y exit codes 0/2/3/5.
- [x] T009 [US1] Tests de integración de `new` en
  `vivarium/crates/vivarium-cli/tests/new.rs` (assert_cmd + tempfile + stub de
  `specify` en `vivarium/crates/vivarium-cli/tests/stubs/specify`): escenarios
  AS1 (kind guia → `mode: produccion` + estructura completa + status
  responde), AS2 (kind novela → `mode: estudio`), AS3 (manifiesto sin `mode`
  se lee como `produccion`), idempotencia (segunda ejecución inocua), SC-001.

**Checkpoint**: US1 entregable sola — se puede crear un proyecto real y
continuarlo a mano con el preset.

---

## Phase 4: User Story 2 — Producir una guía sin vigilar el pipeline (P2)

**Goal**: runner por estados sobre `status.py --json` con despachos BYOM,
idempotencia estructural y checkpoints humanos (FR-003..FR-008, FR-010,
FR-012, FR-013).

**Independent Test**: proyecto sintético de 3 capítulos con agentes stub llega
a `all_chapters_approved` + etapa global, con kill+relaunch a mitad y 0
despachos duplicados (SC-002); retirado el runner, `status.py` propone el
mismo `next_step` (SC-003).

- [x] T010 [P] [US2] Implementar
  `vivarium/crates/vivarium-core/src/state.rs`: derivación de estados por
  capítulo desde `by_chapter` (tabla data-model § 3) + señal global. Unit
  tests por cada estado y transición.
- [x] T011 [US2] Implementar
  `vivarium/crates/vivarium-core/src/dispatch.rs`: parseo/validación de
  `.vivarium/config.toml` (contracts/byom-config.md: tres roles, placeholders,
  `stdin`), escritura del archivo de tarea en `.vivarium/tasks/`, ejecución
  argv puro (sin shell), verificación del éxito **por efecto en disco**
  (research.md R6), reglas de relevo (FR-005) y guardarraíl de modo estudio
  (FR-008 → `blocked_by_mode`). Unit tests con órdenes stub, incluido el
  rechazo de redacción en `estudio`.
- [x] T012 [US2] Implementar
  `vivarium/crates/vivarium-core/src/runner.rs`: mapa `next_step`→acción
  completo (data-model § 4, **incluida la fila global `intro`**), lock fd-lock
  sobre `.vivarium/lock` (exit 6), re-verificación de estado antes de cada
  despacho + no avanzar globales con `in_flight` (FR-006, research.md R7),
  paradas de checkpoint (exit 10) y `blocked_by_mode` (exit 11), registro
  dispatch/disposition/checkpoint en decisions.jsonl (FR-010), modos
  step-único y run-hasta-bloqueo.
- [x] T013 [US2] Cablear subcomandos `vivarium status|step|run|check` en
  `vivarium/crates/vivarium-cli/src/main.rs` según contracts/cli-vivarium.md
  (status con campos propios `mode`/`in_flight`/`blocked_by_mode` y exit 5 si
  ilegible; check valida entorno + config sin despachar).
- [x] T014 [P] [US2] Crear los agentes stub deterministas en
  `vivarium/crates/vivarium-cli/tests/stubs/`: `redactora-stub.sh` (escribe
  `chapters/NN-*.md` mínimo válido), `mesa-stub.sh` (añade bloque pass-output
  1·2·3 a `findings.md`), `doc-stub.sh` (bloque pasada 4 + variante que abre
  un accionable medio para forzar un ciclo de revise), más una segunda
  configuración BYOM distinta (FR-007: dos configs stub corren el mismo
  ciclo).
- [x] T015 [US2] Tests de integración del runner en
  `vivarium/crates/vivarium-cli/tests/runner.rs`: ciclo completo 3 capítulos
  (AS1, incluye un NEEDS_REVISE→IN_REVIEW→APPROVED), kill+relaunch sin
  duplicados contando líneas dispatch de decisions.jsonl (AS2, SC-002),
  etapas globales en orden con parada en checkpoint (AS3, exit 10), agente que
  falla deja estado intacto y reintento seguro (AS4, exit 12), paridad de
  `next_step` tras retirar el runner (SC-003), y el mismo ciclo con la segunda
  config BYOM (FR-007).

**Checkpoint**: US1+US2 — una guía sintética se produce de punta a punta sin
vigilancia.

---

## Phase 5: User Story 3 — Cambiar de modo con consecuencias claras (P3)

**Goal**: cambio de modo explícito, registrado y en caliente (FR-009); cierre
de la garantía de procedencia (SC-004, SC-005).

**Independent Test**: script que verifica exit 4 sin `--yes`, registro
completo con `--yes`, y que un runner en `estudio` rechaza redacción.

- [x] T016 [US3] Implementar el cambio de modo en
  `vivarium/crates/vivarium-core/src/manifest.rs` (append a `mode_history`,
  escritura atómica del manifiesto) + evento `mode_change` en
  `vivarium/crates/vivarium-core/src/decisions.rs` (detail `"from→to"`).
- [x] T017 [US3] Cablear `vivarium mode set` en
  `vivarium/crates/vivarium-cli/src/main.rs`: sin `--yes` imprime la
  consecuencia de procedencia y sale con 4; con `--yes` aplica y registra
  (contracts/cli-vivarium.md § mode set).
- [x] T018 [US3] Tests de integración en
  `vivarium/crates/vivarium-cli/tests/mode.rs`: AS1 (sin confirmación no
  aplica, exit 4, mensaje de consecuencia), AS2 (con `--yes` registra
  manifiesto + decisions), AS3 + SC-004 (proyecto `estudio`: el runner nunca
  despacha redacción; 0 contenido de manuscrito escrito por agentes,
  verificado por git log y decisions.jsonl), SC-005 (100 % de cambios
  registrados con from/to/date).

**Checkpoint**: las tres stories funcionan de forma independiente.

---

## Phase 6: Polish & Cross-Cutting

**Purpose**: publicación del contrato, smoke e2e, docs y gate final.

- [x] T019 [P] Publicar el contrato del ejecutor (FR-011): copiar
  `specs/004-vivarium-core/contracts/executor-contract.md` →
  `writeonmars/contracts/executor-contract.md` (quitando la nota de borrador),
  dejar en el original un puntero al destino (política de fuente única,
  CLAUDE.md), y registrar el contrato nuevo en `CHANGELOG.md`.
- [x] T020 Crear `tests/smoke/vivarium-e2e.sh` (SC-002 de punta a punta:
  compila el CLI, crea proyecto sintético de 3 capítulos con stubs, corre
  hasta `all_chapters_approved` con kill+relaunch a mitad, verifica 0
  duplicados) e integrarlo en `tests/smoke/run-all.sh` con guard
  `command -v cargo >/dev/null || { echo "skip: cargo no disponible"; exit 0; }`
  (quickstart § 3.9).
- [x] T021 [P] Docs: actualizar `vivarium/README.md` § Estado (de
  pre-scaffolding a núcleo implementado), añadir la entrada de la feature a
  `CHANGELOG.md` y el estado nuevo a `ROADMAP.md` (ejecutor Vivarium
  operativo headless).
- [x] T022 Validación manual documentada de FR-007: correr una guía corta con
  dos agentes reales (`claude` y `codex`, adaptadores de `agents/claude/` y
  `agents/codex/`), archivar la evidencia en
  `tests/editorial-pilot/evidence/<YYYY-MM-DD>-vivarium-byom/` (config usada,
  decisions.jsonl, status final). No es test automatizado.
- [x] T023 Gate final (SC-006): `cd vivarium && cargo test --workspace` +
  `uvx --with pytest --with pyyaml python -m pytest tests/unit -q` +
  `bash tests/smoke/run-all.sh` — todo verde, sin pasos manuales no
  documentados.

---

## Dependencies & Execution Order

- **Phase 1 → Phase 2**: T001 bloquea todo; T002 puede solaparse con Phase 2.
- **Phase 2 bloquea las tres stories**: T003 (sidecar) y T004 (manifest) son
  prerrequisito de US1 y US2; T006 (decisions) de US2 y US3; T005 (schema)
  de US1 (el manifiesto generado debe validar).
- **US1 (T007-T009)** solo depende de Foundational.
- **US2 (T010-T015)** depende de Foundational + US1 (los tests del runner
  crean proyectos con `vivarium new`). T010 y T014 son paralelizables entre
  sí y con T011.
- **US3 (T016-T018)** depende de T004/T006; su test AS3 reutiliza el runner
  (T012), así que se integra tras US2.
- **Polish**: T019/T021 en cualquier momento tras US2; T020 y T022-T023 al
  final.

## Parallel Examples

```bash
# Tras T001 (workspace), en paralelo:
T002 (error.rs) · T003 (sidecar.rs) · T004 (manifest.rs) · T005 (schema+bootstrap.py) · T006 (decisions.rs)

# Dentro de US2, en paralelo:
T010 (state.rs) · T014 (stubs de test)   # T011/T012 los consumen después
```

## Implementation Strategy

**MVP = US1** (T001-T009): con solo eso, Vivarium ya crea proyectos operativos
que se continúan a mano — valor entregable y validable. Después US2 (el
reemplazo real de Paperclip), US3 (la garantía de modos), Polish. **STOP and
VALIDATE** en cada checkpoint: cada fase deja el workspace verde
(`cargo test --workspace`) y las suites del repo intactas.
