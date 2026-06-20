# Changelog

Todas las modificaciones notables del framework Write.OnMars se documentan
en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) y
el versionado adopta [Semver](https://semver.org/lang/es/) con dos
trayectorias paralelas: framework (`vX.Y.Z` del repo) y constitución
(`vX.Y.Z` en `.specify/memory/constitution.md`).

## [Unreleased] — refactor a preset agente-agnóstico

### Cambiado

- El método se distribuye y ejecuta como **preset de Spec Kit** (`writeonmars/`),
  instalable con `specify preset add`. La lógica pasó de skills a **comandos**
  (`speckit.specify`, `speckit.research`, `speckit.plan`, `speckit.implement`,
  `speckit.review` + `status`, `export`, `feedback`, `close`, `memory`) y las reglas
  (voz, didáctica, método) a **referencias** neutrales de modelo
  (`writeonmars/references/`), para que lo ejecute cualquier agente, no solo Claude.
- Revisión: de 5 pasadas secuenciales a **3 locales por capítulo + 1 global** (las
  cinco dimensiones se conservan como checklist).
- `install.sh` pasa a **legacy**; `specify preset add` es la vía canónica.
- **Constitución v1.2.0**: Principio V → 3 pasadas locales + 1 global; nuevo
  Principio VI (neutralidad de agente y modelo); distribución canónica = preset.
- **Constitución por capas (v1.2.1 → v1.3.0)**: el núcleo deja de copiarse
  íntegro y editable. Ahora núcleo universal versionado + **adendas del proyecto**
  por guía. El **tono** sale de los 9 campos del brief (pasa a 8 descriptivos) y se
  calibra en las adendas (Principio III). Las **cajas** y el **checklist por
  capítulo** pasan de obligatorios a opcionales por sector. Nuevo requisito
  **`## Fuentes` por capítulo** (cada capítulo cierra con sus fuentes nombradas).
- `bootstrap.py --force` re-sella el núcleo preservando las adendas (centinela
  `<!-- WRITEONMARS:ADENDAS -->`). El PDF mantiene las `## Fuentes` por capítulo,
  atenuadas como aparato de cierre (`.chapter-sources`).

### Añadido

- Scripts deterministas: `export.py` (PDF, reusa el estilo de `markdown-to-pdf`),
  `status.py` (tablero + gates), `feedback_intake.py` (PDF anotado → change-set),
  `close.py` (gate + export), `index.py` (memoria BM25/TF).
- Comando `speckit.constitution` (primer paso del ciclo, guiado con defaults por
  sector; `replaces` el core), plantilla `adendas-template`, y **bases de sector**
  en `references/sectores/` (hoy `tecnologia`, ampliable creando un archivo).
- Campo `sector` en el manifiesto del proyecto.
- Documentación de uso en `writeonmars/docs/` (Diátaxis) y `writeonmars/AGENTS.md`.

### Eliminado (limpieza de docs legacy)

- Docs raíz que describían el mundo pre-preset (skills, `install.sh`, T-numbers,
  scaffolding SC-007) y duplicaban en versión vieja los docs canónicos de
  `writeonmars/docs/`: `docs/editorial-cycle.md`, `docs/skill-catalog.md`,
  `docs/installation.md`, `docs/portability-validation.md`,
  `docs/maintenance/sync-from-vault.md`, `docs/maintenance/skill-update-procedure.md`.
- `docs/contributing.md`, `docs/compatibility-matrix.md`,
  `docs/maintenance/constitution-update-procedure.md`, `docs/citation-contract.md` y
  `docs/manifest-schema.md` reescritos/scrubeados al modelo de preset (comandos +
  referencias + sectores; sin skills/install.sh). La copia de dogfooding
  `.specify/memory/constitution.md` se sincronizó al núcleo v1.3.0.

### Obsoleto

- Spec `002-wom-cli` **superseded**: el `wom` CLI se descarta; `status.py` y
  `close.py` cubren su función.

### Pendiente

- Verificar que `specify preset add` copie `references/`.

## [1.0.0] - 2026-05-06 (pendiente de tag)

Primera release del harness Write.OnMars. Materializa los cinco principios
de la constitución (v1.1.0) en una pipeline ejecutable, agnóstica de
agente, validada con dos pilotos editoriales (3 y 4 capítulos) que
demuestran SC-001..SC-009.

### Added (US1 — Instalación)

- `install/install.sh`: instalador entry point con flags `--target-dir`,
  `--agent`, `--language`, `--symlink`, `--non-interactive`, `--force` y
  exit codes documentados (0, 10, 20, 30, 40, 50, 60).
- `install/lib/detect-existing.sh`: detecta Spec Kit, `CLAUDE.md` y
  manifest preexistentes; emite JSON consumible.
- `install/lib/copy-skills.sh`: copia o enlaza skills bundled (`marcela-prose`,
  `technical-guide-design`, `writeonmars-*`) sin sobreescribir versiones
  divergentes salvo `--force`.
- `install/lib/render-context.sh`: cuestionario interactivo (5 preguntas)
  + render no destructivo de `CLAUDE.md`/`AGENTS.md` entre marcadores
  `<!-- WRITEONMARS START --> ... <!-- WRITEONMARS END -->`.
- `install/lib/render-manifest.sh`: emite `.writeonmars-manifest.json`
  con framework_version, constitution_version, skills[] auto-detectadas,
  signing matrix default v1, operadores y citation_contract_version 1.0.
- Skill `writeonmars-install` para invocación desde el agente.
- Hooks Spec Kit registrados: `extensions.yml` + `extensions/git/`.
- Smoke tests `tests/smoke/install-on-empty-repo.sh`,
  `install-preserves-claudemd.sh`, `specify-after-install.sh` +
  `run-all.sh` aggregator.
- `docs/installation.md` con prerrequisitos, flags, troubleshooting y
  performance SC-001 (<5 min).

### Added (US2 — Producción editorial)

- Plantillas Spec Kit adaptadas en modo dual editorial+software:
  `spec-template.md` (brief de nueve campos),
  `plan-template.md` (Temario + Descripciones encadenadas + Constitution
  Check editorial), `tasks-template.md` (fases editoriales activadas por
  `project_type=editorial`), `checklist-template.md` (cinco checklists del
  Principio V).
- 13 skills `writeonmars-*` para el ciclo editorial completo:
  `writeonmars-brief`, `writeonmars-research`, `writeonmars-temario`,
  `writeonmars-descripciones`, `writeonmars-glossary`,
  `writeonmars-redaccion`, `writeonmars-contraste`,
  `writeonmars-pasada-1` ... `writeonmars-pasada-5`,
  `writeonmars-close-project`.
- 6 prompts canónicos en `agents/claude/prompts/` (redacción + cinco
  pasadas).
- Helpers de validación: `tests/lib/validate-citation.sh`.
- Pilotaje editorial completo de 3 capítulos (`tests/editorial-pilot/`)
  con findings firmados, manifest del piloto, traza paso a paso,
  validation-report contra SC-002, SC-003, SC-004, SC-005, SC-009 y
  close-project verde (`closeable: true`).
- Documentación: `docs/editorial-cycle.md` (flujo de ocho pasos) y
  `docs/skill-catalog.md` (catálogo con FR coverage).

### Added (US3 — Paralelización)

- Modo `--parallel N` en `writeonmars-redaccion`: dispatch concurrente de
  sub-agentes en una sola tool call, sin escrituras compartidas.
- Modo paralelo en `writeonmars-contraste`: contraste por capítulo en
  sub-agente independiente con consolidación de findings.
- Detección de colisiones léxicas para ingestión paralela en
  `writeonmars-glossary`: dos capítulos que introducen el mismo término
  con definiciones divergentes disparan finding crítico.
- Baseline serial (T064a) y piloto paralelo (T065) sobre 4 capítulos del
  mismo manifest; validación SC-006 (paralelo ≥40% más rápido y
  equivalencia ±10% en críticos por pasada y cobertura de glosario).
- Documentación: `docs/parallel-execution.md` (cuándo usar, valores
  recomendados de N, manejo de colisiones, limitaciones conocidas).

### Added (US4 — Mantenimiento)

- Skill `writeonmars-update` para sincronizar un proyecto editorial
  instalado con el repo canónico, preservando configuración local
  (`signing_matrix`, `human_operators[]`, `language_primary`,
  `project_type`, `memory_external`, `writeonmars_research_module`,
  `research_mode`).
- `docs/maintenance/skill-update-procedure.md`: procedimiento operativo
  paso a paso (sync vault → bump VERSION → smoke tests → commit) con
  performance SC-008 medida (PASS).
- `docs/maintenance/constitution-update-procedure.md`: procedimiento
  para enmendar la constitución y propagar el bump a proyectos
  instalados.
- Smoke test `tests/smoke/update-skill-on-installed-project.sh` que
  valida SC-008 en menos de 90 s sobre macOS 15 (target <900 s).

### Added (Polish)

- Implementación de referencia Python 3.11+ del MCP opcional
  `mcp/writeonmars-research/` con `server.py`, `citation.py`,
  `sources.py` y `pyproject.toml`. Cubre FR-009b.
- Scaffolding `agents/codex/` con README operativo y prompts placeholder
  (`prompt-version: 0.1.0-scaffold`) para demostrar el agnosticismo de
  FR-023/FR-024.
- `docs/portability-validation.md`: estado SC-007, checklist para portar a
  un nuevo agente y diferimiento explícito de la validación end-to-end
  con un segundo agente real.
- `docs/contributing.md`: cómo proponer skills, certificar MCPs,
  contribuir a `resources/`, enmendar la constitución y política de PRs.
- `docs/memory-external.md`: esquema mínimo (entidad, fuente, fecha,
  etiquetas), procedimiento de activación, regla de reconstrucción y
  aviso explícito "caché acelerada, nunca fuente de verdad" (FR-022).
- `releases/v1.0.0/`: snapshot inmutable de la constitución v1.1.0 y
  hashes SHA-256 de las 17 skills bundled.
- README operativo con diagrama de arquitectura en ASCII, estado por
  user story (tabla) y quickstart de tres comandos.
- Validación del quickstart end-to-end archivada en
  `tests/editorial-pilot/evidence/2026-05-06-quickstart/quickstart-validation.md`
  (pasos 1-3 reproducidos en sandbox `/tmp/`; pasos 4-10 referenciados a
  evidencia US2 ronda 3 y US3).

### Fixed

- `ajv-cli` invocado con `--spec=draft2020` en
  `install/lib/render-manifest.sh` para reconocer el `$schema` Draft
  2020-12 del manifest. Sin el flag, `ajv` rechazaba el schema y la
  validación caía al fallback python silenciosamente.
- Bloque `if/then` en `contracts/citation-record.schema.json`: requiere
  `versionado_aplicable` en el `if` para evitar match vacuo cuando el
  campo es opcional. Sin el fix, `version_aplicable` no era forzado
  cuando `versionado_aplicable=true`.
- Patrones de `.gitignore` anclados a la raíz para no afectar
  `.specify/templates/` ni rutas que coincidieran accidentalmente con
  `chapters/`, `glossary.md` o `templates/` dentro de carpetas anidadas.

### Notes

- US2/US3 pilotos commitean solo metadatos (manifest, findings resumen,
  pipeline-trace, validation-report). El contenido editorial placeholder
  vive en sandboxes efímeros bajo `/tmp/` y NO se commitea: el repo
  canónico no carga prosa de pilotos editoriales (regla T002).
- T080 (`git tag v1.0.0`) queda como acción manual del mantenedor —
  esta entrada del CHANGELOG es la marca de lectura para el tag.
- El adaptador Codex queda como scaffolding en v1; la validación
  end-to-end con un segundo agente real (Codex o Cursor produciendo una
  guía completa) se difiere a la feature `002-portability-codex` (o
  equivalente) cuando exista ancho de banda operativo.
- Memoria externa: documentada y opcional. El script
  `tools/rebuild-memory.sh` queda especificado en
  `docs/memory-external.md`, no implementado en v1.

[1.0.0]: https://github.com/marcela-gotta/writing-framework/releases/tag/v1.0.0
