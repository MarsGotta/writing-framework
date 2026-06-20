---
description: "Task list template for feature implementation. Coexistente: modo software (default Spec Kit) y modo editorial (Write.OnMars)."
project_type: software
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Modos disponibles**: este template coexiste en dos modos seleccionados por el
front-matter `project_type`:

- `project_type: software` (default Spec Kit): expone fases Setup / Foundational
  / User Stories / Polish.
- `project_type: editorial`: expone fases editoriales (Brief / Investigación /
  Plan / Redacción / Pasada 1–5 / Cierre) que reflejan los Principios II y V de
  la constitución y FR-005..FR-029. La detección la realiza `/speckit-tasks`
  leyendo `.writeonmars-manifest.json` (campo `project_type`).
- `project_type: mixed`: rellena ambas zonas; útil cuando una feature mezcla
  trabajo de framework con trabajo editorial.

**Tests**: incluidos solo si los pide la spec. En modo editorial, las pasadas
del Principio V actúan como tests obligatorios.

**Organization**: tareas agrupadas por fase. En modo software, además se
agrupan por user story; en modo editorial, por etapa del flujo editorial.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: puede ejecutarse en paralelo (archivos distintos, sin dependencias).
- **[Story]**: solo en modo software; mapea a US1, US2, US3...
- Cada tarea incluye ruta de archivo exacta.

## Path Conventions

- **Modo software / Single project**: `src/`, `tests/` en raíz del repo.
- **Modo software / Web app**: `backend/src/`, `frontend/src/`.
- **Modo software / Mobile**: `api/src/`, `ios/src/` o `android/src/`.
- **Modo editorial**: `chapters/`, `glossary.md`, `index.md`, `common-errors.md`,
  `templates/`, `checklists/[###-feature]/`, `specs/[###-feature]/findings.md`.

<!--
  ============================================================================
  IMPORTANT: las tareas siguientes son MUESTRAS ilustrativas. El comando
  /speckit-tasks (modo software) o la skill writeonmars-tasks (modo editorial,
  cuando exista) DEBE reemplazarlas por tareas reales basadas en:

  - User stories / Trayectos de lector de spec.md (con sus prioridades).
  - Requisitos de plan.md (incluido el temario en modo editorial).
  - Entidades del data-model.md / glosario inicial en modo editorial.
  - Endpoints de contracts/ / contrato de citación en modo editorial.

  Las tareas DEBEN organizarse por fase + (story | etapa editorial) para que
  cada bloque sea independientemente entregable.

  NO conserves estas tareas de muestra en el tasks.md generado.
  ============================================================================
-->

# Modo software (default Spec Kit)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: inicialización del proyecto y estructura básica.

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: infraestructura nuclear que todas las user stories consumen.

**⚠️ CRITICAL**: ninguna user story puede arrancar hasta completar esta fase.

- [ ] T004 Setup database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Setup API routing and middleware structure
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation lista — las user stories pueden arrancar en paralelo.

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Qué entrega esta historia.]

**Independent Test**: [Cómo verificarla en aislamiento.]

### Tests for User Story 1 (OPTIONAL — solo si la spec pide tests) ⚠️

> **NOTA: Escribe estos tests PRIMERO; deben FALLAR antes de implementar.**

- [ ] T010 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T011 [P] [US1] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create [Entity1] model in src/models/[entity1].py
- [ ] T013 [P] [US1] Create [Entity2] model in src/models/[entity2].py
- [ ] T014 [US1] Implement [Service] in src/services/[service].py (depends on T012, T013)
- [ ] T015 [US1] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T016 [US1] Add validation and error handling
- [ ] T017 [US1] Add logging for user story 1 operations

**Checkpoint**: User Story 1 totalmente funcional y testable de forma independiente.

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Qué entrega.]

**Independent Test**: [Cómo verificarla.]

### Tests for User Story 2 (OPTIONAL) ⚠️

- [ ] T018 [P] [US2] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T019 [P] [US2] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 2

- [ ] T020 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T021 [US2] Implement [Service] in src/services/[service].py
- [ ] T022 [US2] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T023 [US2] Integrate with User Story 1 components (if needed)

**Checkpoint**: User Stories 1 + 2 funcionan independientemente.

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Qué entrega.]

**Independent Test**: [Cómo verificarla.]

### Tests for User Story 3 (OPTIONAL) ⚠️

- [ ] T024 [P] [US3] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T025 [P] [US3] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create [Entity] model in src/models/[entity].py
- [ ] T027 [US3] Implement [Service] in src/services/[service].py
- [ ] T028 [US3] Implement [endpoint/feature] in src/[location]/[file].py

**Checkpoint**: las tres user stories funcionan independientemente.

---

[Añade más fases de user story según sea necesario.]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: mejoras que afectan a varias user stories.

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

# Modo editorial (Write.OnMars — activado por `project_type: editorial`)

<!--
  Estas fases sólo se materializan cuando el manifiesto declara
  `project_type: editorial` o `mixed`. La numeración E001..E0NN identifica
  tareas editoriales y NO debe colisionar con T### del modo software.
-->

## Phase E1: Brief (FR-005..FR-007)

**Purpose**: aterrizar el brief obligatorio del Principio III antes de
investigar o redactar.

- [ ] E001 Run `writeonmars-brief` (vía `/speckit-specify`) para producir el
  brief (8 campos descriptivos) en `specs/[###-feature]/spec.md`.
- [ ] E002 Resolver cualquier `[NEEDS CLARIFICATION]` en campos críticos
  (audiencia, ejemplo recurrente, resultado esperado) antes de avanzar a
  Investigación. Bloqueante por FR-006.
- [ ] E003 Generar / actualizar el contexto del proyecto (`CLAUDE.md` /
  `AGENTS.md`) entre marcadores `<!-- WRITEONMARS START -->` /
  `<!-- WRITEONMARS END -->`.

**Checkpoint**: brief firmado por la persona operadora; spec lista para
investigar.

---

## Phase E2: Investigación (FR-008..FR-009b)

**Purpose**: producir `research.md` con fuentes verificables conformes al
contrato de citación v1.0.

- [ ] E010 Ejecutar `writeonmars-research` sobre `resources/` (fuente local
  obligatoria) + MCPs externos compatibles (BYOM por defecto).
- [ ] E011 [P] Validar cada CitationRecord contra
  `contracts/citation-record.schema.json` con `tests/lib/validate-citation.sh`.
- [ ] E012 Asegurar ≥ 1 cita por concepto obligatorio del brief (SC-009).
- [ ] E013 Marcar datos volátiles (versiones, precios, comandos) con
  `[VERIFICAR]`.

**Checkpoint**: `specs/[###-feature]/research.md` cierra cobertura de
conceptos obligatorios.

---

## Phase E3: Plan editorial (FR-010, FR-011)

**Purpose**: temario + descripciones encadenadas + Constitution Check editorial.

- [ ] E020 [P] Ejecutar `writeonmars-temario` (envuelve `/technical-guide-design`)
  y rellenar la sección "Temario" de `plan.md`.
- [ ] E021 [P] Ejecutar `writeonmars-descripciones` y rellenar
  "Descripciones encadenadas" en `plan.md`. Validar que `conexion_anterior` /
  `conexion_siguiente` `null` solo aparece en frontera.
- [ ] E022 Constitution Check editorial: verificar Principios I–V; registrar
  desviaciones en `Complexity Tracking`.

**Checkpoint**: `plan.md` aprobado; cualquier desviación justificada.

---

## Phase E4: Redacción (FR-014, FR-015)

**Purpose**: producir cada capítulo bajo la estructura didáctica del Principio
II y consolidar el glosario sin colisiones.

- [ ] E030 [P] Despachar sub-agente de redacción por capítulo (o `--parallel N`
  cuando US3 esté activo) con el prompt canónico
  `agents/claude/prompts/redaccion.md`.
- [ ] E031 Cada sub-agente devuelve `chapters/[###]-titulo.md` con front-matter
  YAML (data-model § 7), la estructura de capítulo del sector y la sección `## Fuentes`.
- [ ] E032 Ejecutar `writeonmars-glossary` para consolidar
  `terminos_introducidos`; bloquear ante colisiones de definición (FR-015).

**Checkpoint**: capítulos redactados, glosario consolidado, ejemplo recurrente
aplicado en ≥ 80 % de capítulos (SC-005).

---

## Phase E5: Pasada 1 — Estructura (FR-018, Constitución § V.1)

**Purpose**: detectar promesa difusa, capítulos sin función, progresión rota.

- [ ] E040 Ejecutar `writeonmars-pasada-1` (envuelve `/technical-guide-design`).
- [ ] E041 Anexar bloque a `findings.md` conforme a `pass-output-schema` v1.0.
- [ ] E042 Firmar `checklists/[###-feature]/pasada-1.md` (default: autonomous).

**Checkpoint**: pasada 1 verde o hallazgos críticos resueltos.

---

## Phase E6: Pasada 2 — Utilidad (FR-018, Constitución § V.2)

**Purpose**: ejemplos por concepto, acción práctica por capítulo, checklists,
errores comunes, criterios de éxito.

- [ ] E050 Ejecutar `writeonmars-pasada-2` (envuelve `/technical-guide-design`).
- [ ] E051 Anexar bloque a `findings.md`.
- [ ] E052 Firmar `checklists/[###-feature]/pasada-2.md` (default: autonomous).

**Checkpoint**: pasada 2 verde o hallazgos críticos resueltos.

---

## Phase E7: Pasada 3 — Naturalidad (FR-018, Constitución § V.3)

**Purpose**: detectar frases comprimidas, "No es X: es Y", pronombres vagos,
transiciones secas, entusiasmo artificial, metáforas mezcladas.

- [ ] E060 Ejecutar `writeonmars-pasada-3` (envuelve `/marcela-prose`).
- [ ] E061 Anexar bloque a `findings.md`.
- [ ] E062 Firmar `checklists/[###-feature]/pasada-3.md`. **Firma humana
  requerida** por defecto (FR-020a). Cualquier desviación se justifica en
  `Complexity Tracking`.

**Checkpoint**: pasada 3 firmada por operador humano; hallazgos críticos
resueltos.

---

## Phase E8: Pasada 4 — Precisión (FR-016, FR-018, Constitución § V.4)

**Purpose**: contrastar cada afirmación verificable contra ≥ 1 CitationRecord.

- [ ] E070 Ejecutar `writeonmars-pasada-4` (envuelve `writeonmars-contraste`).
- [ ] E071 Anexar bloque a `findings.md` con `referencias_cita` por hallazgo.
- [ ] E072 Firmar `checklists/[###-feature]/pasada-4.md`. **Firma humana
  requerida** por defecto.

**Checkpoint**: cero hallazgos críticos abiertos en pasada 4 al cierre (SC-002).

---

## Phase E9: Pasada 5 — Formato (FR-018, FR-029, Constitución § V.5)

**Purpose**: cajas visuales útiles, ejemplos diferenciados, títulos claros,
índice navegable, glosario completo, plantillas extraídas.

- [ ] E080 Ejecutar `writeonmars-pasada-5`. Agrega `common-errors.md`,
  construye / valida `index.md`, valida `glossary.md` y `templates/`.
- [ ] E081 Anexar bloque a `findings.md`.
- [ ] E082 Firmar `checklists/[###-feature]/pasada-5.md` (default: autonomous).

**Checkpoint**: pasada 5 verde; estructura de guía completa lista.

---

## Phase E10: Cierre (FR-020, FR-020a)

**Purpose**: gate final de cierre del proyecto editorial.

- [ ] E090 Ejecutar `writeonmars-close-project`. Devuelve
  `{closeable: bool, blockers: [...]}`.
- [ ] E091 Resolver blockers (críticos abiertos, firmas humanas faltantes) o
  archivar `desviacion_justificada`.
- [ ] E092 Archivar evidencia del ciclo (spec, research, plan, chapters,
  findings, checklists, manifest) en
  `tests/editorial-pilot/evidence/<YYYY-MM-DD>-<topic>/` cuando aplique.

**Checkpoint**: cierre del proyecto editorial; guía publicable.

---

## Dependencies & Execution Order

### Phase Dependencies (modo software)

- **Setup (Phase 1)**: sin dependencias.
- **Foundational (Phase 2)**: depende de Setup. **BLOQUEA** todas las stories.
- **User Stories (Phase 3+)**: dependen de Foundational.
  - Pueden avanzar en paralelo si hay equipo.
  - O secuencialmente por prioridad (P1 → P2 → P3).
- **Polish (Final Phase)**: depende de las stories deseadas completas.

### Phase Dependencies (modo editorial)

- **E1 Brief**: sin dependencias.
- **E2 Investigación**: depende de E1.
- **E3 Plan editorial**: depende de E2.
- **E4 Redacción**: depende de E3.
- **E5..E9 Pasadas 1–5**: secuenciales en este orden (constitución § V).
- **E10 Cierre**: depende de E5..E9 verdes.

### Within Each User Story (modo software)

- Tests (si se incluyen) DEBEN escribirse y FALLAR antes de implementar.
- Modelos antes de servicios.
- Servicios antes de endpoints.
- Implementación nuclear antes de integración.

### Within Each Editorial Phase

- Cada pasada bloquea la siguiente: defectos detectados se resuelven antes de
  avanzar (constitución § V).
- Las pasadas con firma humana requieren al operador declarado en
  `human_operators[]` del manifiesto.

### Parallel Opportunities

- Tareas marcadas `[P]` dentro de una fase pueden ejecutarse en paralelo.
- Modo software: una vez Foundational verde, todas las stories pueden empezar
  en paralelo si la capacidad lo permite.
- Modo editorial: la redacción (E030) puede paralelizarse capítulo a capítulo
  cuando US3 esté activo (US3 entrega `--parallel N`).

---

## Parallel Example: User Story 1 (modo software)

```bash
# Lanzar todos los tests de la US1 a la vez (si la spec los pide):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Lanzar todos los modelos de la US1 a la vez:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

## Parallel Example: Redacción editorial (modo editorial, US3)

```bash
# Después de E20–E22 (plan editorial cerrado), lanzar redacción paralela
# de capítulos independientes:
Task: "Redactar chapters/001-titulo.md siguiendo agents/claude/prompts/redaccion.md"
Task: "Redactar chapters/002-titulo.md siguiendo agents/claude/prompts/redaccion.md"
Task: "Redactar chapters/003-titulo.md siguiendo agents/claude/prompts/redaccion.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 / Brief + Pasada 5)

1. Modo software: Phase 1 → Phase 2 → Phase 3.
2. Modo editorial: E1 → E2 → E3 → un solo capítulo en E4 → E5..E9 sobre ese
   capítulo → E10.
3. **STOP and VALIDATE** antes de extender.

### Incremental Delivery

- Modo software: Setup + Foundational → US1 → US2 → US3 → Polish.
- Modo editorial: brief → investigación → plan → un capítulo redactado y
  pasado por las cinco pasadas → ampliar al resto del temario.

### Parallel Team Strategy

Modo software (con varios developers):

1. Equipo completa Setup + Foundational.
2. Una vez Foundational verde:
   - Persona A: User Story 1.
   - Persona B: User Story 2.
   - Persona C: User Story 3.
3. Las stories integran independientemente.

Modo editorial (con un agente y un humano):

1. Operador humano firma brief y pasadas 3 + 4.
2. Agente redacta y ejecuta pasadas 1, 2, 5 en autónomo.
3. La paralelización de redacción (`--parallel N`) acelera guías de ≥ 4
   capítulos.

---

## Notes

- `[P]` = archivos distintos, sin dependencias incompletas.
- `[Story]` mapea la tarea a una user story (solo modo software).
- Verifica que los tests fallan antes de implementar.
- Commit después de cada tarea o grupo lógico; el hook `auto_commit.after_implement`
  de Spec Kit aplica igual a artefactos editoriales que a código.
- Modo editorial: nunca borres pasadas históricas en `findings.md`; cada pasada
  añade su bloque al final.
- Evita: tareas vagas, conflictos de archivo, dependencias cruzadas que rompan
  la independencia de stories o de pasadas.
