---
description: "Task list for the wom CLI (feature 002)"
project_type: software
---

# Tasks: CLI `wom` para operar Write.OnMars

**Input**: Design documents from `/specs/002-wom-cli/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: incluidos. La spec declara smoke tests como estrategia de testing (FR-002, FR-013, SC-003, SC-008). Tareas de testing aparecen marcadas `[Test]` cuando aplica.

**Organization**: tareas agrupadas por user story para implementación y testeo independientes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: puede ejecutarse en paralelo (archivos distintos, sin dependencias).
- **[Story]**: a qué user story pertenece (`US1`–`US7`); ausente en Setup/Foundational/Polish.
- Cada tarea incluye ruta de archivo exacta.

## Path Conventions

Repo canónico de Write.OnMars (este repo). Rutas relevantes para feature 002:

- Entry point: `bin/wom`
- Subcomandos: `bin/wom-lib/<sub>.sh`
- Helpers compartidos: `bin/wom-lib/common.sh`
- Smokes: `tests/smoke/wom/<sub>.sh` + `run-all.sh`
- Doc operativa: `docs/wom-cli.md`
- Instalador (modificar para symlink): `install/install.sh`
- Contrato de comandos: `specs/002-wom-cli/contracts/command-schema.md`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: scaffolding del binario y los helpers compartidos.

- [ ] T001 Create directory structure for the CLI: `bin/`, `bin/wom-lib/`, `tests/smoke/wom/`. Add `.gitkeep` only where needed (los directorios se poblarán con scripts en T002+).
- [ ] T002 [P] Create `bin/wom` dispatcher script (executable, `#!/usr/bin/env bash`, `set -euo pipefail`). Header con shebang, descripción y referencia a `specs/002-wom-cli/contracts/command-schema.md`. Lógica: parsear primer arg como subcomando, validar contra lista canónica, dispatchear a `bin/wom-lib/<sub>.sh`. Si arg ausente o `--help`, llamar a `help.sh`. Si subcomando desconocido, exit 2 con mensaje.
- [ ] T003 [P] Create `bin/wom-lib/common.sh` con utilidades compartidas: logging `wom::info`, `wom::warn`, `wom::err` (todos a stderr); `wom::find_project_root` (busca `.writeonmars-manifest.json` subiendo desde `$PWD`); `wom::read_manifest` (jq wrapper); `wom::feature_dir` (lee `.specify/feature.json`); detección de herramientas opcionales (`wom::has_gum`, `wom::has_fzf`).
- [ ] T004 [P] Create `bin/wom-lib/help.sh` que imprime uso global (`wom --help`) y ayuda por subcomando (`wom <sub> --help`). Texto derivado de `contracts/command-schema.md` § cada subcomando. Sin emojis, español.
- [ ] T005 [P] Add `bin/` to repo `.gitignore` exceptions (no es necesario; el ignore actual no afecta `bin/`). Verificar que `git status` muestra `bin/wom` como tracked tras chmod +x.

**Checkpoint**: dispatcher operativo (`./bin/wom --help` muestra el catálogo de subcomandos aún sin implementar; cada subcomando responde con "no implementado" hasta que su fase complete).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: abstracciones que TODAS las user stories consumen (lockfile, manifest reader, project root). Sin esto los subcomandos no pueden arrancar.

**⚠️ CRITICAL**: ninguna user story puede arrancar hasta completar esta fase.

- [ ] T006 Implement lockfile abstraction in `bin/wom-lib/common.sh` (extender T003): `wom::lock_acquire` (mkdir atómico de `<root>/.wom/lock.d`; escribir `.wom/lock` JSON con pid, subcommand, started_at, host, operator); `wom::lock_release` (rm archivo + rmdir directorio); `wom::lock_stale_check` (`kill -0` sobre el pid leído). Trap en cada subcomando escritor para liberar al salir. Cubre R2 + FR-017.
- [ ] T007 [P] Implement manifest validation helper in `bin/wom-lib/common.sh`: `wom::validate_manifest` que ejecuta `python3 + jsonschema` o `npx ajv-cli --spec=draft2020` (orden de fallback igual a `install/lib/render-manifest.sh`). Devuelve 0 si valida, 1 si no, con mensaje específico.
- [ ] T008 [P] Implement EstadoProyecto reader in `bin/wom-lib/state.sh` (nuevo archivo, sourced por status, close, sign): `wom::state_read` recibe feature_directory y devuelve JSON estructurado siguiendo data-model.md §1 (proyecto_nombre, framework_version, signing_matrix, capitulos[] con estado por pasada, firmas_humanas_*, criticos_abiertos_total). Excluye paths gitignored (FR-012).
- [ ] T009 [P] Implement findings.md parser in `bin/wom-lib/findings.sh` (nuevo archivo, sourced por state, close): parsea bloques `## Pasada N — ...` siguiendo `contracts/pass-output-schema.md` v1.0; extrae findings con campos id, capitulo, severidad, estado. Tolera bloques mal formados saltándolos con warning a stderr.
- [ ] T010 [P] Implement BloqueFirma reader/writer in `bin/wom-lib/firma.sh` (nuevo archivo, sourced por sign, close): `wom::firma_read` parsea el bloque entre `<!-- WOM-SIGN START -->` y `<!-- WOM-SIGN END -->` (data-model.md §3); `wom::firma_write` reescribe ese bloque idempotentemente con awk + redirección atómica + mv.

**Checkpoint**: helpers cargables. `bash -n bin/wom-lib/*.sh` pasa sin syntax errors. Las funciones se pueden invocar desde un script de prueba ad-hoc.

---

## Phase 3: User Story 1 — `wom new` (Priority: P1) 🎯 MVP

**Goal**: una operadora arranca un proyecto editorial nuevo en un solo comando (<30s, SC-001).

**Independent Test**: `bash tests/smoke/wom/new.sh` crea un sandbox tmp, ejecuta `wom new` con env vars y asserta los seis artefactos del install + tiempo total <30s.

### Implementation for User Story 1

- [ ] T011 [US1] Create `bin/wom-lib/new.sh`: parsea `<nombre>` + flags (`--agent`, `--language`, `--non-interactive`); valida que `<nombre>` no exista o esté vacío (FR-005); ejecuta `mkdir <nombre> && cd <nombre> && git init -q`; invoca `<canonical>/install/install.sh --target-dir "$PWD" --agent "$agent" --language "$lang" [--non-interactive]`. NO adquiere lockfile (no hay manifest aún). Cubre FR-004.
- [ ] T012 [US1] Update `install/install.sh` para añadir un symlink desde `<target>/bin/wom` apuntando al `bin/wom` del repo canónico. Vía: tras `copy-skills`, ejecutar `mkdir -p <target>/bin && ln -sf <canonical>/bin/wom <target>/bin/wom`. Añadir entrada en CLAUDE.md generado: `Para usar la CLI desde este proyecto: export PATH="$PWD/bin:$PATH"`. Cubre R1 + FR-003.
- [ ] T013 [P] [US1] [Test] Create `tests/smoke/wom/new.sh`: crea sandbox padre con `mktemp -d`; ejecuta `<canonical>/bin/wom new mi-piloto --agent claude-code --language es --non-interactive` con env vars `WOM_*`; asserta que existe `<sandbox>/mi-piloto/.writeonmars-manifest.json`, `<sandbox>/mi-piloto/.specify/`, `<sandbox>/mi-piloto/.claude/skills/`, `<sandbox>/mi-piloto/bin/wom` (symlink); cronometra y reporta si <30s.

**Checkpoint**: US1 cierra. La operadora va de directorio vacío a proyecto listo para `wom status` con un comando.

---

## Phase 4: User Story 2 — `wom status` (Priority: P1)

**Goal**: la operadora ve estado completo de la guía en una pantalla (<1s con 8 capítulos, SC-002).

**Independent Test**: `bash tests/smoke/wom/status.sh` produce un proyecto sintético con 8 capítulos en estados mixtos, ejecuta `wom status`, valida la salida contra fixture esperado y cronometra.

### Implementation for User Story 2

- [ ] T014 [US2] Create `bin/wom-lib/status.sh`: invoca `wom::state_read` (T008); renderiza dashboard ASCII con `printf` + `awk` siguiendo el formato de `command-schema.md § wom status`; soporta `--format=json` (vuelca el JSON crudo del state) y `--format=text` (default, dashboard). Si `WOM_STATUS_RENDER=gum` y `gum` está disponible, usar `gum table`; si no, fallback ASCII. Cubre FR-011, FR-012, FR-019.
- [ ] T015 [US2] [Test] Create `tests/smoke/wom/status.sh`: crea sandbox tmp con install + escribe manualmente `chapters/00{1..8}-test.md` con front-matter mínimo + `findings.md` sintético con bloques de pasadas mixtas + checklists con WOM-SIGN selectivos; ejecuta `wom status` y asserta que la salida contiene los 8 capítulos, los conteos correctos de firmas humanas, y el total de críticos abiertos. Cronometra (target <1s).

**Checkpoint**: US2 cierra. Dashboard utilizable durante producción real.

---

## Phase 5: User Story 3 — `wom close` (Priority: P1)

**Goal**: cerrar el proyecto editorial desde la consola con paridad 100% vs `writeonmars-close-project` (SC-003).

**Independent Test**: `bash tests/smoke/wom/close-parity.sh` ejecuta `wom close` sobre los pilotos archivados de feature 001 (US2 ronda 3 + US3) y compara el veredicto contra el `close-project-output.json` archivado. PASS si coincide en 100%.

### Implementation for User Story 3

- [ ] T016 [US3] Create `bin/wom-lib/close.sh`: invoca `wom::state_read` + `wom::findings_parse`; aplica gates FR-020 (críticos abiertos) y FR-020a (firmas humanas pendientes según signing_matrix); produce `ResultadoCierre` (data-model.md §5) con exit 0/1; soporta `--format=json|text` y `--strict` (trata `desviacion_justificada` como blocker). NO adquiere lockfile (solo lectura). Cubre FR-014.
- [ ] T017 [US3] [Test] Create `tests/smoke/wom/close-parity.sh`: itera sobre `tests/editorial-pilot/evidence/*/close-project-output.json` (los archivados de feature 001); para cada uno, reconstruye un sandbox mínimo desde los metadatos (manifest.json + findings-summary.md) y ejecuta `wom close`; compara `closeable` y `blockers[]` contra el JSON archivado. Falla si algún caso difiere. Valida SC-003.

**Checkpoint**: US3 cierra. La operadora cierra proyectos sin invocar el agente y la lógica espeja la skill nativa.

---

## Phase 6: User Story 4 — `wom sign` (Priority: P2)

**Goal**: firmar pasadas humanas desde la consola sin abrir markdown manualmente (SC-004 + SC-007).

**Independent Test**: `bash tests/smoke/wom/sign.sh` con un sandbox que tiene un checklist sin firmar, ejecuta `wom sign 3 2`, verifica el bloque WOM-SIGN escrito y que `writeonmars-close-project` (skill nativa) lo reconoce.

### Implementation for User Story 4

- [ ] T018 [US4] Create `bin/wom-lib/sign.sh`: parsea `<pasada> <capítulo>` + flags (`--operator`, `--force`, `--note`, `--type`); valida `pasada ∈ [1..5]`, `capítulo` existe en `chapters/`, `--operator` (default `human_operators[0].id`) está en `manifest.human_operators[]`; adquiere lockfile (T006); invoca `wom::firma_write` (T010); libera lockfile. Cubre FR-009, FR-010.
- [ ] T019 [US4] [Test] Create `tests/smoke/wom/sign.sh`: sandbox con manifest válido + un `checklists/[###]/pasada-3.md` sin firmar; ejecuta `wom sign 3 2`; asserta que (a) el archivo tiene el bloque WOM-SIGN con `firma_actor=marcela` y fecha actual, (b) reintentar sin `--force` falla con exit 1, (c) reintentar con `--force` sobreescribe la fecha, (d) usar `--operator desconocido` falla con exit 1 listando operadores válidos.

**Checkpoint**: US4 cierra. Firmas auditables y reproducibles desde CLI.

---

## Phase 7: User Story 5 — Orquestación de prompts editoriales (Priority: P2)

**Goal**: reducir la fricción de tipeo cuando hay que coordinar con el agente para los pasos editoriales reales.

**Independent Test**: cada subcomando del grupo (brief, research, plan, draft, review) imprime un prompt válido y pegable; los smoke tests validan estructura de salida.

### Implementation for User Story 5

- [ ] T020 [P] [US5] Create `bin/wom-lib/brief.sh`: detecta feature_directory; si no existe, sugiere `wom new` o `/speckit-specify`; abre `<feature_dir>/spec.md` en `$EDITOR` (fallback `vi`, fallback exit 10 con mensaje). Cubre FR-006.
- [ ] T021 [P] [US5] Create `bin/wom-lib/research.sh`: imprime prompt para `/writeonmars-research` con paths absolutos al brief y a `resources/`. Sin lockfile. Cubre FR-007.
- [ ] T022 [P] [US5] Create `bin/wom-lib/plan.sh`: imprime prompt para `/writeonmars-temario` + `/writeonmars-descripciones` referenciando el brief y el research. Cubre FR-007.
- [ ] T023 [P] [US5] Create `bin/wom-lib/draft.sh`: parsea `<N>` + `--parallel <K>` (valida K ∈ [2,8]); imprime prompt para `/writeonmars-redaccion --chapter N [--parallel K]` con contexto (brief, temario, descripción objetivo, descripciones contiguas, glosario). Cubre FR-007, FR-008.
- [ ] T024 [P] [US5] Create `bin/wom-lib/review.sh`: parsea `<pasada> <capítulo>`; valida ranges; imprime prompt para `/writeonmars-pasada-N` con referencias al capítulo, al `findings.md` actual, al `pass-output-schema.md`, y al prompt canónico de `agents/claude/prompts/pasada-N.md`. Cubre FR-007.
- [ ] T025 [P] [US5] [Test] Create `tests/smoke/wom/prompts.sh`: ejecuta cada uno de los cinco subcomandos del grupo en un sandbox y verifica que la salida (a) contiene el nombre de la skill esperada, (b) lista paths absolutos, (c) no contiene placeholders sin resolver tipo `[capítulo]`. Idempotente.

**Checkpoint**: US5 cierra. La operadora copia-pega prompts en lugar de redactarlos.

---

## Phase 8: User Story 6 — `wom doctor` y `wom validate` (Priority: P3)

**Goal**: diagnóstico rápido del entorno (SC-005, <2s) y validación profunda de artefactos (FR-013).

**Independent Test**: smoke tests que ejecutan ambos subcomandos en escenarios verde y rojo.

### Implementation for User Story 6

- [ ] T026 [P] [US6] Create `bin/wom-lib/doctor.sh`: itera sobre la lista de verificaciones de `command-schema.md § wom doctor`; reporta `OK <versión>`, `MISSING <pista>`, `WARN <razón>` por cada una; soporta `--format=json|text`; exit 0 si solo warnings opcionales, exit 1 si falta hard. Cubre FR-016, SC-005.
- [ ] T027 [P] [US6] Create `bin/wom-lib/validate.sh`: ejecuta `tests/smoke/run-all.sh` (a menos que `--quick`); valida `.writeonmars-manifest.json` con `wom::validate_manifest` (T007); itera sobre `<feature_dir>/research.md` extrayendo bloques JSON de CitationRecord y validándolos con `tests/lib/validate-citation.sh`. Reporta errores con paths concretos. Cubre FR-013.
- [ ] T028 [P] [US6] [Test] Create `tests/smoke/wom/doctor.sh`: ejecuta `wom doctor` en la máquina; asserta exit 0 (asumiendo entorno completo) y verifica el patrón de salida. Cronometra para SC-005. Caso negativo: simula `jq` faltante con `PATH` filtrado y verifica exit ≠ 0.
- [ ] T029 [P] [US6] [Test] Create `tests/smoke/wom/validate.sh`: sandbox con un manifest válido + research.md con un CitationRecord intencionadamente inválido (motor vacío); ejecuta `wom validate` y asserta exit 1 con mensaje específico al record violado.

**Checkpoint**: US6 cierra. Diagnóstico operable.

---

## Phase 9: User Story 7 — `wom update` (Priority: P3)

**Goal**: actualizar skills canónicas en proyectos instalados desde la CLI (SC-008).

**Independent Test**: smoke test reusa `tests/smoke/update-skill-on-installed-project.sh` de feature 001 pero invocando vía `wom update --yes` en lugar de la skill directa.

### Implementation for User Story 7

- [ ] T030 [US7] Create `bin/wom-lib/update.sh`: adquiere lockfile (T006); invoca la lógica de la skill `writeonmars-update` (lectura del manifest, comparación de versiones, copia de archivos, actualización del manifest preservando campos custom); soporta `--yes` y `--dry-run`; libera lockfile. Cubre FR-015.
- [ ] T031 [US7] [Test] Create `tests/smoke/wom/update.sh`: replica el escenario de `tests/smoke/update-skill-on-installed-project.sh` (feature 001) pero invocando `wom update --yes`; asserta que (a) la skill bumpeada se actualiza en el sandbox, (b) language_primary custom y operador extra se preservan, (c) tiempo total <900s (SC-008). Trap revierte la VERSION canónica al final.

**Checkpoint**: US7 cierra. Mantenimiento desde CLI.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: orquestación de smokes, documentación, integración con el repo canónico.

- [ ] T032 [P] Create `tests/smoke/wom/run-all.sh`: ejecuta T013, T015, T017, T019, T025, T028, T029, T031 en orden; imprime tabla de resumen PASS/FAIL; exit con la suma lógica. Sin emojis.
- [ ] T033 [P] Create `docs/wom-cli.md`: manual operativo de la CLI. Secciones: instalación (post-install del framework hace el symlink), referencia rápida (tabla con cada subcomando + uso típico), workflows comunes (arrancar proyecto, ciclo de revisión, troubleshooting), variables de entorno, exit codes, ejemplos completos de salida. Tono operativo, español, sin emojis. ≤ 500 líneas.
- [ ] T034 [P] Update `README.md` raíz para añadir sección "CLI `wom`" con tres bullets (qué es, cómo se invoca, link a `docs/wom-cli.md`). Mantener sección existente de feature 001 intacta.
- [ ] T035 [P] Update `docs/installation.md` (de feature 001) para mencionar que tras `install.sh`, el binario `wom` queda disponible en `<target>/bin/wom`. Añadir entrada en § Performance con el tiempo medido en T012.
- [ ] T036 [P] Update `docs/skill-catalog.md` (de feature 001) para añadir una sección "CLI complementaria" que liste `wom` y referencie `docs/wom-cli.md`.
- [ ] T037 [P] Add entry to `CHANGELOG.md`: nueva sección `[1.1.0] - <fecha>` (pendiente de tag) con resumen de la CLI por user story (US1..US7) y la lista de subcomandos implementados. Mantener `[1.0.0]` intacta.
- [ ] T038 Run the full quickstart.md end-to-end on a fresh test repository; record results in `tests/editorial-pilot/evidence/<YYYY-MM-DD>-wom-quickstart/quickstart-validation.md`. Confirma que los 10 pasos funcionan y los SC se cumplen sobre un proyecto sintético.
- [ ] T039 Tag pre-release (manual, no ejecutado por la CLI): preparar texto del tag `v1.1.0-wom-cli` para que la mantenedora lo aplique con `git tag -a` cuando decida.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sin dependencias. Empieza inmediatamente.
- **Foundational (Phase 2)**: depende de Setup. **BLOQUEA** todas las user stories.
- **US1 (Phase 3)**: depende de Foundational + T012 (modificación de install.sh).
- **US2 (Phase 4)**: depende de Foundational (state.sh, findings.sh).
- **US3 (Phase 5)**: depende de Foundational (state.sh, findings.sh) + US2 reusa parsers.
- **US4 (Phase 6)**: depende de Foundational (firma.sh, lockfile).
- **US5 (Phase 7)**: depende de Foundational (manifest reader, project root). Independiente de US1–US4.
- **US6 (Phase 8)**: depende de Foundational. Independiente del resto.
- **US7 (Phase 9)**: depende de Foundational + lockfile + skill `writeonmars-update` ya operativa (de feature 001).
- **Polish (Phase 10)**: depende de TODAS las user stories deseadas.

### User Story Dependencies

- **US1, US2, US3 (P1)**: independientes entre sí tras Foundational. Cualquier orden.
- **US4 (P2)**: independiente; usa lockfile y firma.sh, ambos en Foundational.
- **US5 (P2)**: cinco subcomandos completamente independientes (5 archivos distintos); paralelizable internamente.
- **US6 (P3)**: dos subcomandos independientes; paralelizable.
- **US7 (P3)**: depende del lockfile y de la skill envuelta.

### Within Each User Story

- US1: T011 → T012 → T013.
- US2: T014 → T015.
- US3: T016 → T017.
- US4: T018 → T019.
- US5: T020–T024 paralelos → T025.
- US6: T026 + T027 paralelos → T028 + T029 paralelos.
- US7: T030 → T031.

### Parallel Opportunities

- Phase 1: 4 paralelos (T002–T005).
- Phase 2: 4 paralelos (T007–T010, T006 va primero porque define el lockfile usado por los demás).
- US5 implementación: 5 paralelos (T020–T024).
- Polish: 6 paralelos (T032–T037).

---

## Parallel Example: User Story 5 — orquestación de prompts

```bash
# Tras Foundational (T006–T010) completo, los cinco wrappers de prompt se
# crean en paralelo:

Task: "Create bin/wom-lib/brief.sh"
Task: "Create bin/wom-lib/research.sh"
Task: "Create bin/wom-lib/plan.sh"
Task: "Create bin/wom-lib/draft.sh"
Task: "Create bin/wom-lib/review.sh"

# Después (sequencial):
Task: "Create tests/smoke/wom/prompts.sh"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 — todos P1)

1. Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3).
2. Stop y validar: smokes T013, T015, T017 verdes; `wom status` <1s con 8 caps; `wom close` paridad 100%.
3. Tag pre-release `v1.1.0-mvp` si conviene.

### Incremental Delivery

1. MVP (US1+US2+US3) → demo: arranque + dashboard + cierre.
2. + US4 → demo: firma desde CLI.
3. + US5 → demo: ciclo editorial completo sin tipear prompts manualmente.
4. + US6 → demo: doctor + validate.
5. + US7 → demo: update.
6. + Polish → release v1.1.0.

### Parallel Team Strategy

- Tras Foundational, tres streams en paralelo:
  - Stream A: cierra US1+US2+US3 (P1) — una persona o sub-agente.
  - Stream B: arranca US5 burst de cinco subcomandos en paralelo.
  - Stream C: prepara US6 doctor+validate.

---

## Notes

- Toda la CLI usa Bash 5+, jq, awk, Git. Cero dependencias adicionales hard-required (SC-006).
- `gum` y `fzf` son optional; cada uso debe tener fallback explícito.
- El binario `wom` no lanza el agente; orquesta. Los subcomandos editoriales (research, plan, draft, review) imprimen prompts pegables.
- Lockfile solo en escritores (`new`, `sign`, `update`); lectores corren concurrentemente.
- Smoke tests reusan el patrón de feature 001 (`tests/smoke/run-all.sh`).
- Paridad 100% con `writeonmars-close-project` es no negociable (SC-003).
- v1.1.0 monolingüe español; inglés diferido a feature posterior si la complejidad lo justifica (R6).
- No commits durante la implementación de un sub-agente; commit por phase al final, igual que feature 001.
