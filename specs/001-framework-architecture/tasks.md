---
description: "Task list for the Write.OnMars harness architecture (feature 001)"
---

# Tasks: Arquitectura y flujo de trabajo del harness Write.OnMars

**Input**: Design documents from `/specs/001-framework-architecture/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: incluidos. Las pruebas no son opcionales: la spec declara acceptance scenarios verificables (US1) y el `research.md` §R6 establece una estrategia de testing en dos capas (smoke shell + guía piloto editorial). Tareas de testing aparecen marcadas `[Test]` cuando aplica.

**Organization**: tareas agrupadas por user story para implementación y testeo independientes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: puede ejecutarse en paralelo (archivos distintos, sin dependencias).
- **[Story]**: a qué user story pertenece (`US1`–`US4`); ausente en Setup/Foundational/Polish.
- Cada tarea incluye ruta de archivo exacta.

## Path Conventions

Repo canónico de Write.OnMars (este repo). Rutas relevantes:

- Skills bundled: `.claude/skills/<skill-name>/SKILL.md`
- Scripts de instalación: `install/install.sh`, `install/lib/*.sh`
- Contratos publicados: `contracts/` (mirrors de `specs/001-framework-architecture/contracts/`) y `docs/`
- Plantillas Spec Kit adaptadas: `.specify/templates/*.md`
- Constitución: `.specify/memory/constitution.md`
- Recursos editoriales: `resources/`
- Tests: `tests/smoke/*.sh`, `tests/editorial-pilot/`
- Prompts canónicos por agente: `agents/claude/prompts/`
- Módulo MCP opcional: `mcp/writeonmars-research/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: scaffolding del repositorio canónico + tooling de desarrollo.

- [X] T001 Create framework directory structure per plan.md: `install/lib/`, `mcp/`, `contracts/`, `docs/maintenance/`, `tools/`, `tests/smoke/`, `tests/lib/`, `tests/editorial-pilot/evidence/`, `tests/editorial-pilot/sandbox/`, `agents/claude/prompts/`, `releases/`, `.claude/skills/` (already exists from Spec Kit hooks but ensure is present).
- [X] T002 Add `.gitignore` entries for editorial outputs that should not be committed in canonical repo: `chapters/`, `glossary.md` (project-level), `index.md` (project-level), `common-errors.md`, `templates/`, `.writeonmars-manifest.json`. The canonical repo should not carry editorial artefacts.
- [X] T003 [P] Create `tools/dev-bootstrap.sh` that documents and verifies dev prerequisites: Bash 5+, Git ≥2.30, `jq`, `ajv` (via npm/npx) and `shellcheck`. Exit non-zero if any missing.
- [X] T004 [P] Create `tests/editorial-pilot/README.md` describing the 3-chapter pilot scope, topic, and links to evidence directory; mirror SC validations table from `quickstart.md`.
- [X] T005 [P] Create `README.md` skeleton at repo root with: short pitch, links to `.specify/memory/constitution.md`, `specs/001-framework-architecture/`, and `docs/`.

**Checkpoint**: estructura del repo lista; tooling de desarrollo verificable.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: artefactos canónicos compartidos que TODAS las user stories consumen (skills bundled de origen externo, contratos publicados, documentación de mantenimiento).

**⚠️ CRITICAL**: ninguna user story puede arrancar hasta completar esta fase.

- [X] T006 Copy `/marcela-prose` from the Obsidian vault canonical source into `.claude/skills/marcela-prose/` and freeze a `VERSION` file declaring the imported version (FR-028). Document the import procedure (date, source, hash) in `docs/maintenance/sync-from-vault.md`.
- [X] T007 Copy `/technical-guide-design` from the Obsidian vault canonical source into `.claude/skills/technical-guide-design/` and freeze a `VERSION` file (FR-028). Append to `docs/maintenance/sync-from-vault.md`.
- [X] T008 [P] Mirror `specs/001-framework-architecture/contracts/citation-contract.md` to `contracts/citation-contract.md` (canonical published location).
- [X] T009 [P] Extract the JSON Schema from `contracts/citation-contract.md` § "JSON Schema (referencia mínima)" into `contracts/citation-record.schema.json` so it can be validated independently with `ajv`.
- [X] T010 [P] Mirror `specs/001-framework-architecture/contracts/manifest-schema.json` to `contracts/manifest-schema.json` (canonical published location).
- [X] T011 [P] Mirror `specs/001-framework-architecture/contracts/pass-output-schema.md` to `contracts/pass-output-schema.md` (canonical published location).
- [X] T012 [P] Create `docs/citation-contract.md` as a human-friendly walkthrough of the citation contract (audience: maintainers and MCP authors), linking to `contracts/citation-contract.md` for the formal spec.
- [X] T013 [P] Create `docs/manifest-schema.md` documenting each manifest field with examples, defaults and migration notes.
- [X] T014 [P] Create `docs/compatibility-matrix.md` scaffold with sections: "MCPs investigación compatibles" (initial entries: `context7`, `web-search:tavily`, `fetch`, `local:resources`), "Agentes soportados" (claude-code marked v1, codex/cursor marked planned).
- [X] T015 [P] Document the canonical maintenance procedure in `docs/maintenance/sync-from-vault.md`: when, why and how to refresh the bundled `/marcela-prose` and `/technical-guide-design` from the vault, including version bump rules.

**Checkpoint**: contratos publicados, skills externas bundled y documentación de mantenimiento listas. Las user stories pueden arrancar.

---

## Phase 3: User Story 1 — Instalación inicial del harness (Priority: P1) 🎯 MVP

**Goal**: un operador (humano o agente) puede instalar Write.OnMars sobre un repo Git vacío en <5 minutos y obtener el repositorio listo para `/speckit-specify`.

**Independent Test**: ejecutar `tests/smoke/install-on-empty-repo.sh`, `tests/smoke/install-preserves-claudemd.sh` y `tests/smoke/specify-after-install.sh`; verificar que pasan los tres acceptance scenarios de US1.

### Implementation for User Story 1

- [X] T016 [US1] Create `install/install.sh` entry point: parse flags (`--target-dir`, `--agent`, `--language`, `--symlink`), verify prerequisites (Bash 5+, Git, target dir exists and is a Git repo), and call helpers in `install/lib/` in order. Exit codes documented in script header.
- [X] T017 [P] [US1] Create `install/lib/detect-existing.sh`: detects pre-existing Spec Kit installation and pre-existing `CLAUDE.md`/`AGENTS.md`; outputs JSON with detection results to be consumed by other libs (FR-003).
- [X] T018 [P] [US1] Create `install/lib/copy-skills.sh`: copies (or symlinks if `--symlink` flag) all skills under `.claude/skills/` from canonical repo to target project. Skills covered: `marcela-prose`, `technical-guide-design` and all `writeonmars-*` (FR-028). Idempotent.
- [X] T019 [P] [US1] Create `install/lib/render-context.sh`: launches the interactive questionnaire (tipo de proyecto editorial, agente prioritario, idioma primario, audiencia general, dominio técnico) and renders/merges `CLAUDE.md` or `AGENTS.md` according to detected agent (FR-002, FR-007).
- [X] T020 [P] [US1] Create `install/lib/render-manifest.sh`: generates `.writeonmars-manifest.json` populating `framework_version`, `constitution_version`, `agent_target`, `language_primary`, `skills[]` (with versions read from each skill's `VERSION` file), `research_mode: byom`, default `signing_matrix` (1, 2, 5 = autonomous; 3, 4 = human), `human_operators[]` from prompt, and `citation_contract_version: "1.0"` (FR-004). Validate output against `contracts/manifest-schema.json` via `ajv`.
- [X] T021 [US1] Wire `install/install.sh` to call `install/lib/*.sh` in correct order: detect → copy-skills → copy `.specify/` (constitution, templates, extensions) → register Spec Kit Git hooks → render-context → render-manifest. Depends on T016–T020.
- [X] T022 [US1] Implement Spec Kit hook registration inside `install/install.sh`: copy `.specify/extensions.yml` and `.specify/extensions/git/` from canonical repo to target. Verify no destructive overwrite when target already has Spec Kit (uses detection from T017).
- [X] T023 [US1] Create `.claude/skills/writeonmars-install/SKILL.md` so the install can also be invoked as an agent skill. The SKILL.md describes: trigger phrases ("instala write.onmars", "writeonmars init"), the `install.sh` invocation, and the questionnaire format.
- [X] T024 [P] [US1] [Test] Create `tests/smoke/install-on-empty-repo.sh`: creates a temp repo with `git init`, runs `install/install.sh --target-dir <tmp> --agent claude-code --language es` non-interactively (use env vars to skip questionnaire), then asserts: `.specify/memory/constitution.md` exists; `.specify/templates/*.md` exist; `.claude/skills/marcela-prose/`, `.claude/skills/technical-guide-design/`, all `.claude/skills/writeonmars-*/` exist; `.writeonmars-manifest.json` exists and validates against `contracts/manifest-schema.json`; `.specify/extensions.yml` is registered. Covers US1 §AC1 and SC-001.
- [X] T025 [P] [US1] [Test] Create `tests/smoke/install-preserves-claudemd.sh`: pre-creates `CLAUDE.md` in temp repo with custom content marker, runs install, asserts custom content is preserved (merged, not overwritten). Covers US1 §AC2.
- [X] T026 [P] [US1] [Test] Create `tests/smoke/specify-after-install.sh`: after a successful install, asserts that `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` returns valid output, and that `.specify/templates/spec-template.md` is the editorial-adapted version (Phase US2 will adapt; this test should pass with both default and adapted templates). Covers US1 §AC3.
- [X] T027 [US1] Create `tests/smoke/run-all.sh` that runs T024, T025, T026 and prints a summary report.
- [X] T028 [US1] Create `docs/installation.md` documenting: prerequisites, default install command, flags, troubleshooting and validation against the JSON Schema. Reference `quickstart.md` for end-to-end usage.
- [X] T029 [US1] Time the install on a clean macOS machine and on a clean Linux container; record in `docs/installation.md` § "Performance" to validate SC-001 (<5 minutes).

**Checkpoint**: US1 cierra. El framework instala reproduciblemente sobre repos vacíos y preserva configuración previa. Listo para deploy/demo MVP.

---

## Phase 4: User Story 2 — Producción de una guía completa siguiendo el flujo editorial (Priority: P1)

**Goal**: un operador, sobre un proyecto instalado, puede ejecutar el ciclo Spec Kit completo y obtener una guía técnica markdown con cinco pasadas firmadas y `findings.md` limpio.

**Independent Test**: producir la guía piloto de tres capítulos en `tests/editorial-pilot/` y validar SC-002 (hallazgos críticos), SC-003 (estructura didáctica), SC-004 (cobertura glosario), SC-005 (ejemplo recurrente) y SC-009 (fuentes por concepto).

### Implementation for User Story 2 — Spec Kit template adaptation

- [X] T030 [P] [US2] Adapt `.specify/templates/spec-template.md` to incorporate the nine-field editorial brief (audiencia, problema, resultado_esperado, nivel, tono, conceptos_obligatorios, ejemplo_recurrente, riesgos, acciones_practicas) as mandatory sections (FR-005). Preserve the "User Stories → Trayectos de lector" mental model documented in the constitution sync impact report.
- [X] T031 [P] [US2] Adapt `.specify/templates/plan-template.md` to include explicit "Temario" and "Descripciones encadenadas" sections plus the editorial-oriented Constitution Check (FR-010, FR-011).
- [X] T032 [P] [US2] Adapt `.specify/templates/tasks-template.md` to support an **editorial mode** activado por front-matter (`project_type: editorial`) que expone fases editoriales (Brief / Investigación / Plan / Redacción / Pasada 1–5 / Cierre) **adicionalmente** al modo software por defecto (Setup / Foundational / Stories / Polish). El modo software permanece intacto para features de framework como esta. La detección del modo se basa en `project_type` que `writeonmars-install` registra en el manifiesto del proyecto editorial durante la instalación inicial (FR-004).
- [X] T033 [P] [US2] Adapt `.specify/templates/checklist-template.md` to materialise the five pasadas as separate templated sections (`pasada-1.md` … `pasada-5.md`), each with its checklist items derived from the constitution § V.

### Implementation for User Story 2 — Editorial skills (writeonmars-*)

- [X] T034 [P] [US2] Create `.claude/skills/writeonmars-brief/SKILL.md`: triggers from `/speckit-specify`; runs the editorial questionnaire, emits the spec.md with the nine-field brief (FR-005), blocks if critical fields contain `[NEEDS CLARIFICATION]` (FR-006), and updates the project context file `CLAUDE.md`/`AGENTS.md` (FR-007).
- [X] T035 [P] [US2] Create `.claude/skills/writeonmars-research/SKILL.md`: orchestrates over MCPs compatible with the citation contract (BYOM mode), accepts `resources/` as mandatory local source, emits `research.md` with citation records validated against `contracts/citation-record.schema.json` (FR-008, FR-009, FR-009a). Document supported MCPs and how to add new ones.
- [X] T036 [P] [US2] Create `.claude/skills/writeonmars-temario/SKILL.md`: wraps `/technical-guide-design` for chapter list design; emits the "Temario" section into `plan.md`. Each chapter declares numero, titulo, promesa and estructura_aplicada per data-model.md §4.
- [X] T037 [P] [US2] Create `.claude/skills/writeonmars-descripciones/SKILL.md`: wraps `/technical-guide-design` for inter-chapter connection design; emits the "Descripciones encadenadas" section per data-model.md §5. Validates that null `conexion_anterior`/`conexion_siguiente` only appear at boundaries.
- [X] T038 [P] [US2] Create `.claude/skills/writeonmars-glossary/SKILL.md`: consolidates `terminos_introducidos` from all chapters, detects collisions (FR-015), detects **términos huérfanos** (técnicos usados en cuerpo de capítulo pero ausentes del glosario, requerido por SC-004), emits/updates `specs/[###-feature]/glossary.md` and the project-wide `glossary.md`. Handles `anglicismo_admitido` justifications (constitución § IV).
- [X] T039 [P] [US2] Create `.claude/skills/writeonmars-redaccion/SKILL.md`: dispatches a sub-agent (Claude Code Agent tool, `subagent_type: general-purpose` by default) per chapter, passing brief, temario, descripción objetivo, descripciones contiguas, ejemplo recurrente y glosario consolidado (FR-014). The sub-agent invokes `/technical-guide-design` for chapter architecture and `/marcela-prose` for voice. Returns chapter markdown + glossary annex (FR-015).
- [X] T040 [P] [US2] Create `.claude/skills/writeonmars-contraste/SKILL.md`: pasada 4 implementation; verifies each verifiable claim against at least one citation record (FR-016) and emits a Pasada 4 block in `findings.md` per `contracts/pass-output-schema.md`.
- [X] T041 [P] [US2] Create `.claude/skills/writeonmars-pasada-1/SKILL.md`: pasada 1 (estructura) wrapping `/technical-guide-design`; emits a Pasada 1 block in `findings.md` and a checklist in `checklists/[###-feature]/pasada-1.md`.
- [X] T042 [P] [US2] Create `.claude/skills/writeonmars-pasada-2/SKILL.md`: pasada 2 (utilidad) wrapping `/technical-guide-design`; emits a Pasada 2 block + checklist.
- [X] T043 [P] [US2] Create `.claude/skills/writeonmars-pasada-3/SKILL.md`: pasada 3 (naturalidad) wrapping `/marcela-prose`; emits a Pasada 3 block + checklist; default signing policy in matrix = `human`.
- [X] T044 [P] [US2] Create `.claude/skills/writeonmars-pasada-4/SKILL.md`: pasada 4 (precisión) wrapping `writeonmars-contraste`; default signing policy = `human`.
- [X] T045 [P] [US2] Create `.claude/skills/writeonmars-pasada-5/SKILL.md`: pasada 5 (formato); **agrega** las secciones "Error frecuente" de cada capítulo en `common-errors.md` con el esquema de data-model.md §9 (error, capitulo_origen, sintoma, causa_probable, que_revisar); construye/valida `index.md` (promesa global, "Para quién es / no es", ruta de lectura, enlaces); valida `glossary.md`, `templates/`, presencia de cajas visuales y formateo de capítulos.
- [X] T046 [US2] Create `.claude/skills/writeonmars-close-project/SKILL.md`: implements the close gate. Reads `findings.md` + manifest; outputs `{closeable: bool, blockers: [...]}` based on FR-020 (critical findings) and FR-020a (missing human signatures). Depends on T040–T045 to define how findings are read.

### Implementation for User Story 2 — Sub-agent prompts and citation orchestration

- [X] T047 [P] [US2] Create `agents/claude/prompts/redaccion.md`: canonical prompt for the redaction sub-agent. Includes role, files to read, allowed skills, output format and acceptance criteria. Versioned (filename includes version or has front-matter version).
- [X] T048 [P] [US2] Create `agents/claude/prompts/pasada-1.md` … `agents/claude/prompts/pasada-5.md`: one canonical prompt per pasada with the specific lens of each. Wired by the corresponding skill via T041–T045.
- [X] T049 [US2] Create `tests/lib/validate-citation.sh`: shell helper that runs `ajv` against `contracts/citation-record.schema.json` for a given JSON file or stream. Used by `writeonmars-research` and CI.
- [X] T050 [US2] Implement BYOM dispatch logic inside `writeonmars-research` SKILL: documents how the skill normalises outputs from `context7`, web search and `fetch` into citation records. Add a fallback that surfaces a clear error when no compatible MCP is available (edge case from spec).

### Implementation for User Story 2 — Editorial pilot validation

- [ ] T051 [US2] [Test] In a fresh test project under `tests/editorial-pilot/sandbox/`, run `install/install.sh` and capture artefacts. Confirms US1 still passes against the editorial-adapted templates from T030–T033.
- [ ] T052 [US2] [Test] Define the pilot guide topic (a small, bounded technical subject — e.g. "Onboarding técnico en repositorios legacy") and produce its brief via `writeonmars-brief`. Save to `tests/editorial-pilot/sandbox/specs/001-pilot/spec.md`.
- [ ] T053 [US2] [Test] Run `writeonmars-research` against `resources/` and any available external MCP; produce `tests/editorial-pilot/sandbox/specs/001-pilot/research.md` with at least one citation per concepto obligatorio (SC-009).
- [ ] T054 [US2] [Test] Run `writeonmars-temario` and `writeonmars-descripciones` to produce the Temario + Descripciones encadenadas in `plan.md` (3 chapters).
- [ ] T055 [US2] [Test] Run `writeonmars-redaccion` serially (parallelisation is US3) to draft the three chapter files in `tests/editorial-pilot/sandbox/chapters/`. Verify each chapter has the nine didactic sections (SC-003) and uses the recurring example (SC-005).
- [ ] T056 [US2] [Test] Execute the five pasadas in order over each chapter. Pasadas 3 and 4 require human signature in the default matrix; in the pilot, the maintainer signs them or documents `desviacion_justificada`. Captures `findings.md` and `checklists/001-pilot/pasada-N.md`.
- [ ] T057 [US2] [Test] Run `writeonmars-close-project` over the pilot. Must report `closeable: true` with no blockers. Validates SC-002.
- [ ] T058 [US2] Archive the pilot evidence (spec, research, plan, chapters, findings, checklists, manifest) in `tests/editorial-pilot/evidence/<YYYY-MM-DD>-pilot-onboarding/` for future reference and constitution audits.
- [ ] T059 [US2] Validate metrics: SC-003 (nine sections in 100% of chapters), SC-004 (glossary covers 100% of technical terms), SC-005 (recurring example in ≥80% of chapters), SC-009 (≥1 citation per concepto obligatorio). Document results in `tests/editorial-pilot/evidence/<YYYY-MM-DD>-pilot-onboarding/validation-report.md`.

### Implementation for User Story 2 — Documentation

- [X] T060 [P] [US2] Create `docs/editorial-cycle.md`: the canonical eight-step flow (install → brief → context → research → temario → descripciones → redacción → contraste → 5 pasadas) with cross-references to skills, contracts and the constitution.
- [X] T061 [P] [US2] Create `docs/skill-catalog.md`: enumerates each `writeonmars-*` skill, what it wraps (if any), inputs, outputs and FR coverage. Useful for maintainers and for new agent ports.

**Checkpoint**: US2 cierra. El framework produce guías que pasan las cinco pasadas con métricas auditables. Hay evidencia archivada que demuestra el ciclo completo end-to-end.

---

## Phase 5: User Story 3 — Paralelización de redacción y contraste por capítulos (Priority: P2)

**Goal**: para guías de ≥4 capítulos, el framework permite redactar y contrastar en paralelo, conservando el ejemplo recurrente, el glosario consolidado y el hilo conductor.

**Independent Test**: producir una guía de 4+ capítulos con 2+ capítulos redactados en paralelo; comprobar SC-006 (≥40% reducción de tiempo) y que la pasada 1 no detecta ruptura del hilo conductor.

### Implementation for User Story 3

- [ ] T062 [US3] Extend `.claude/skills/writeonmars-redaccion/SKILL.md` with a `--parallel N` mode: dispatches up to N sub-agents concurrently using Claude Code's parallel Agent tool calls (single message, multiple tool uses). Each sub-agent receives the same shared context (brief, temario, glosario, descripciones contiguas) and writes to its dedicated chapter file (no shared writes).
- [ ] T063 [US3] Extend `.claude/skills/writeonmars-contraste/SKILL.md` with parallel-per-chapter dispatch (each chapter's contrast runs in its own sub-agent), then consolidates findings into `findings.md`. Conflicts in citation interpretations between chapters surface as a consolidated note.
- [ ] T064 [US3] Enhance `.claude/skills/writeonmars-glossary/SKILL.md` collision detection for parallel ingestion: detects when two chapters introduce the same term with divergent definitions, flags it as `critico`, blocks consolidation until resolved (FR-015 edge case from spec).
- [ ] T064a [US3] [Test] Establecer baseline serial de 4 capítulos sobre el mismo tema del piloto US3 ejecutando `writeonmars-redaccion` en modo secuencial (sin `--parallel`); cronometrar y archivar evidencia en `tests/editorial-pilot/evidence/<YYYY-MM-DD>-pilot-parallel-baseline/`. Capturar métricas: tiempo total, hallazgos críticos por pasada, cobertura de glosario.
- [ ] T065 [US3] [Test] Pilot a 4-chapter guide with 2 chapters drafted in parallel via `--parallel 2` sobre el mismo tema y manifiesto que T064a. Cronometrar y capturar las mismas métricas de calidad (críticos/pasada, cobertura de glosario).
- [ ] T066 [US3] [Test] Validate SC-006: paralelo ≥40% más rápido que el baseline T064a **y** equivalencia ±10% en (a) hallazgos críticos por pasada y (b) cobertura de glosario. Document evidence in `tests/editorial-pilot/evidence/<YYYY-MM-DD>-pilot-parallel/parallel-validation.md`.
- [ ] T067 [P] [US3] Create `docs/parallel-execution.md`: when to use parallel mode, recommended N values, glossary collision handling and known limitations.

**Checkpoint**: US3 cierra. La paralelización está disponible y validada para guías medianas/grandes.

---

## Phase 6: User Story 4 — Mantenimiento y propagación de cambios del framework (Priority: P3)

**Goal**: una persona mantenedora puede actualizar una skill canónica y propagar el cambio a un proyecto instalado en <15 minutos sin pérdida de configuración local.

**Independent Test**: simular un bump de versión en una skill bundled, ejecutar el procedimiento de update sobre un proyecto piloto y validar SC-008.

### Implementation for User Story 4

- [ ] T068 [US4] Create `.claude/skills/writeonmars-update/SKILL.md`: compares the project manifest skill versions against the canonical repo's skills, presents a diff of what would change, and applies the update on confirmation. Preserves project-local configuration (manifest fields the user customised).
- [ ] T069 [US4] Create `docs/maintenance/skill-update-procedure.md`: step-by-step procedure for updating a bundled skill (version bump → vault sync → update entry in compatibility-matrix → run smoke tests → release notes).
- [ ] T070 [US4] Create `docs/maintenance/constitution-update-procedure.md`: step-by-step procedure for amending the constitution and propagating templates per the existing "Procedimiento de enmienda" of the constitution itself, plus how installed projects pick up the change.
- [ ] T071 [US4] [Test] Create `tests/smoke/update-skill-on-installed-project.sh`: installs the framework into a temp repo, bumps the version of a bundled skill in the canonical source, runs `writeonmars-update`, and asserts the project's manifest reflects the new version while a custom field set by the operator survives. Validates SC-008.
- [ ] T072 [US4] Document the time-to-update result in `docs/maintenance/skill-update-procedure.md` § "Performance" to validate SC-008 (<15 minutes).

**Checkpoint**: US4 cierra. Las actualizaciones del framework son trazables, no destructivas y verificables en CI.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: módulo MCP opcional, demostración de portabilidad, documentación final y release tagging.

- [ ] T073 [P] Implement `mcp/writeonmars-research/server.py` (FR-009b): Python 3.11 reference implementation that wraps web search + fetch + local resources into the citation contract; emits citation records validated against `contracts/citation-record.schema.json`. Include `mcp/writeonmars-research/pyproject.toml` and `mcp/writeonmars-research/README.md`.
- [ ] T074 [P] Create `agents/codex/` adapter scaffolding mirroring `agents/claude/`: empty prompt files matching the canonical names, plus a `README.md` explaining what needs to be filled in to support Codex. Demonstrates the agnosticism declared in FR-023/FR-024 even if not fully wired in v1.
- [ ] T075 [P] Document SC-007 portability readiness in `docs/portability-validation.md`: (a) qué partes del harness son agente-agnósticas (skills nucleares en `.claude/skills/`, contratos publicados, manifiesto), (b) qué partes requieren adaptador (`agents/<name>/prompts/`), (c) checklist de pasos para portar una skill a Codex/Cursor cuando exista soporte. SC-007 v1 = entrega de scaffolding + contratos; la validación end-to-end con un segundo agente se difiere a feature posterior.
- [ ] T076 [P] Create `docs/contributing.md`: how to propose a new skill, how to certify a new MCP for the citation contract (link `contracts/citation-contract.md` § "Cómo certificar"), how to contribute to `resources/` and how to amend the constitution.
- [ ] T076a [P] Document the optional external vector memory in `docs/memory-external.md`: esquema mínimo (entidad, fuente, fecha, etiquetas) per constitution § "Arquitectura del framework"; procedimiento de activación (`manifest.memory_external.enabled: true`, `provider`, `uri`); procedimiento de reconstrucción desde artefactos del repo (FR-022); aviso explícito de que la memoria es caché, nunca fuente de verdad. Cross-link a `contracts/manifest-schema.json` § `memory_external`.
- [ ] T077 Run the full `quickstart.md` end-to-end on a fresh test repository; record results in `tests/editorial-pilot/evidence/<YYYY-MM-DD>-quickstart/quickstart-validation.md`. Confirms the documented path matches reality after all phases.
- [ ] T078 [P] Polish `README.md`: pitch, architecture diagram (text), quickstart link, status of each user story, current version.
- [ ] T079 Archive a snapshot of `.specify/memory/constitution.md` (v1.1.0) into `releases/v1.0.0/constitution-v1.1.0.md` for historical reference. Naming aclara que el framework v1.0.0 ratifica la constitución v1.1.0; futuras releases pueden mantener la misma constitución sin renombrar.
- [ ] T080 Tag `v1.0.0` once all checkpoints pass and update `CHANGELOG.md` with the user-story-by-user-story summary.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies. Start immediately.
- **Foundational (Phase 2)**: depends on Setup. **BLOCKS** all user stories.
- **US1 (Phase 3)**: depends on Foundational.
- **US2 (Phase 4)**: depends on Foundational. Soft dep on US1: editorial pilot validation (T051–T059) needs `install/install.sh` working, but skill development (T034–T046) does not.
- **US3 (Phase 5)**: depends on US2 redacción + contraste + glossary skills (T039, T040, T038).
- **US4 (Phase 6)**: depends on US1 install + US2 manifest writer.
- **Polish (Phase 7)**: depends on all desired user stories complete.

### User Story Dependencies

- **US1 (P1)**: independent after Foundational. Provides the install entry point.
- **US2 (P1)**: independent after Foundational for skill development; needs US1 done before pilot validation. Most US2 skills can be built in parallel with US1 once Foundational is green.
- **US3 (P2)**: extends US2 skills. Cannot complete without US2 §Skills section.
- **US4 (P3)**: builds on US1 + US2 manifests.

### Within Each User Story

- US1: lib scripts (T017–T020) before wiring (T021); wiring before integration (T022) and skill wrapper (T023); smoke tests (T024–T026) after wiring.
- US2: template adaptation (T030–T033) and skill creation (T034–T046) are independent. Sub-agent prompts (T047–T048) and citation helpers (T049–T050) are needed before pilot validation (T051–T059).
- US3: T062 → T063 → T064 → baseline serial T064a → pilot paralelo (T065–T066) → docs (T067).
- US4: T068 → T069/T070 (docs) → smoke test (T071) → performance doc (T072).

### Parallel Opportunities

- All `[P]` tasks within a phase can run in parallel.
- Phase 2 has 8 parallel tasks (T008–T015) — bulk of foundational work parallelizable.
- US1 has 6 parallel tasks (T017–T020 install libs, T024–T026 smoke tests).
- US2 has 17 parallel skill-creation tasks (T030–T033 templates, T034–T045 skills, T047–T048 prompts, T060–T061 docs).
- US3 has 1 parallel task (T067 docs).
- Polish has 6 parallel tasks (T073–T076, T076a, T078).

---

## Parallel Example: User Story 2 — skill creation burst

```bash
# After Foundational (T006–T015) and template adaptation (T030–T033) complete,
# launch all skill-creation tasks together:

Task: "Create .claude/skills/writeonmars-brief/SKILL.md"
Task: "Create .claude/skills/writeonmars-research/SKILL.md"
Task: "Create .claude/skills/writeonmars-temario/SKILL.md"
Task: "Create .claude/skills/writeonmars-descripciones/SKILL.md"
Task: "Create .claude/skills/writeonmars-glossary/SKILL.md"
Task: "Create .claude/skills/writeonmars-redaccion/SKILL.md"
Task: "Create .claude/skills/writeonmars-contraste/SKILL.md"
Task: "Create .claude/skills/writeonmars-pasada-1/SKILL.md"
Task: "Create .claude/skills/writeonmars-pasada-2/SKILL.md"
Task: "Create .claude/skills/writeonmars-pasada-3/SKILL.md"
Task: "Create .claude/skills/writeonmars-pasada-4/SKILL.md"
Task: "Create .claude/skills/writeonmars-pasada-5/SKILL.md"

# Followed (sequentially) by:
Task: "Create .claude/skills/writeonmars-close-project/SKILL.md"  # depends on T040–T045
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1).
2. Stop and validate: smoke tests all green, install <5 minutes, `tests/smoke/run-all.sh` passes.
3. Tag a pre-release `v0.1.0-mvp` if helpful.

### Incremental Delivery

1. MVP (US1) → demo: framework instala y deja repo listo para Spec Kit.
2. + US2 → demo: producción end-to-end de la guía piloto.
3. + US3 → demo: paralelización en una guía de 4 capítulos.
4. + US4 → demo: actualización trazable de skills.
5. + Polish → release v1.0.0.

### Parallel Team Strategy

- After Foundational completes, three streams en paralelo:
  - Stream A: termina US1 (3 personas semana 1).
  - Stream B: arranca US2 skill burst (varias personas en paralelo, una skill cada una).
  - Stream C: comienza US3 design discussions (no bloquea US2 pero permite refinar la API de paralelización antes de implementarla).

---

## Notes

- `[P]` tasks = different files, no dependencies on incomplete tasks.
- `[Story]` label maps task to specific user story for traceability.
- `[Test]` flag (in description) marks validation tasks (smoke or pilot).
- Each user story closes at a checkpoint where the framework is independently demoable.
- Commit after each task or logical group; the Spec Kit `auto_commit.after_implement` hook can be enabled for this phase.
- Editorial pilot evidence is canonical: never reset or overwrite past pilot evidence; new pilots get new directories.
- Avoid: skipping the editorial pilot (T051–T059) — it is the only honest validation of US2 quality.
