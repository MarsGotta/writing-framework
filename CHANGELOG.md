# Changelog

Todas las modificaciones notables del framework Write.OnMars se documentan
en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) y
el versionado adopta [Semver](https://semver.org/lang/es/) con dos
trayectorias paralelas: framework (`vX.Y.Z` del repo) y constitución
(`vX.Y.Z` en `.specify/memory/constitution.md`).

## [Unreleased] — refactor a preset agente-agnóstico

### Mantenimiento (2026-07-09, limpieza de la casa)

- **Copias muertas de skills retiradas**: `.agents/skills/` y `.claude/skills/`
  arrastraban 17 skills duplicadas por carpeta (marcela-prose,
  technical-guide-design, `writeonmars-*`) que ya habían divergido de la
  fuente canónica (`references/voz` del 2026-07-07 vs copia del 2026-05-06).
  Solo quedan las `speckit-*` de la integración Spec Kit; la fuente única del
  método es `writeonmars/references/`.
- **Vía legacy `install.sh` eliminada del árbol**: `install/` (instalador + 5
  libs), sus 4 smoke tests y las referencias `writeonmars-install` /
  `writeonmars-update` que envolvían ese flujo. `run-all.sh` queda con los
  smokes vigentes. La historia de git conserva todo.
- **`graphify-out/` fuera del versionado** (242 archivos, ~5,5 MB de salidas y
  caché de la herramienta de exploración): regenerable; la caché local se
  conserva en disco.
- **CI**: gates en GitHub Actions (`.github/workflows/ci.yml`) — pytest de
  `tests/unit`, `cargo test --workspace` y smokes con stubs (factualidad,
  vivarium-e2e, estudio-e2e, smoke del preset) en cada push/PR.
- **Licencia: Apache-2.0** (LICENSE en raíz; `preset.yml`, `pyproject.toml`
  del MCP y `Cargo.toml` del workspace actualizados). Desbloquea publicar el
  preset.
- Docs alineados con la realidad: el tag `v1.0.0` existe desde 2026-05-06
  (README y este CHANGELOG decían "pendiente de tag"), el preset son 8
  scripts (no 6) y el enlace del repo apunta a `MarsGotta/writing-framework`.

### Modo estudio operativo (feature 005, 2026-07-08)

- `status.py` entiende `mode: estudio`: expone `mode`, `pending_chapters`,
  `pending_dispositions`, `deferred_findings` y `reopened_chapters`, y enruta
  `write`/`dispose` como checkpoints humanos.
- Añadidos `dispose.py` (disposición humana auditable) y `authorship.py`
  (informe determinista desde git + `decisions.jsonl`).
- Publicado `pass-output-schema` v1.2, `disposition-record.schema.json` y la
  sección "Modo estudio" del contrato del ejecutor.
- Vivarium mapea `write`, `dispose` e `intro` en estudio como checkpoints
  humanos sin tocar el guardarraíl exit 11.
- **Revisión adversarial (2026-07-09, 8 ángulos)**: corregidas 3 regresiones de
  retrocompatibilidad (FR-011) reproducidas en vivo — cuenta de pendientes en
  produccion vuelve a ser por ficheros (un `intro.md` no reabre `implement`),
  `disposiciones.jsonl` solo se lee en estudio (una línea corrupta ya no tumba
  la brújula en produccion), `mode` desconocido en manifiesto legado degrada a
  produccion; y bugs de contrato: `dispose --rechazar` escribe el motivo en
  `decision_humana` (9ª columna), edición byte-intacta de findings.md (CRLF y
  padding preservados), resolución de spec-dir unificada en `findings_lib`
  (dispose usaba el spec más viejo), cierre en estudio anclado a la huella
  (editar un capítulo aprobado lo vuelve no-cerrable), sin livelock cuando un
  agente deja un estado incoherente, y `authorship.py` robusto a monorepos,
  renames y timestamps naive. Smoke `estudio-e2e` ampliado a 2 capítulos (SC-002)
  con `close.py` real e idempotencia verificada.

### Constitución v1.6.1 (2026-07-08, lente de modo en Estándares editoriales)

- **PATCH 1.6.0 → 1.6.1**: los bullets "Fuentes por capítulo" y "Atribución por
  afirmación" (texto de la era 003, previo a los modos) ganan la lente de modo
  que § Modos de proyecto ya establecía: el MUST de `claims.md` es del modo
  produccion; en estudio la pasada 4 verifica consistencia contra las fuentes
  del proyecto y `claims.md` solo se exige con umbral declarado. Detectado como
  conflicto C1 por el `/speckit-analyze` de la feature 005 (Codex). Las
  referencias de versión en plan-template pasan a ser agnósticas (anti-fósil).

### Vivarium headless (feature 004, 2026-07-07)

- Añadido workspace Rust `vivarium/` con `vivarium-core` y `vivarium-cli`:
  bootstrap `vivarium new`, `status|check`, runner `step|run`, config BYOM,
  lock de proyecto, `decisions.jsonl` y `mode set`.
- Publicado `writeonmars/contracts/executor-contract.md` como contrato del
  ejecutor; el borrador de `specs/004-vivarium-core/contracts/` quedó como
  puntero.
- **`manifest-schema` v1.3.0 (MINOR)**: campos opcionales `mode`
  (`produccion`/`estudio`) y `mode_history`; ausencia de `mode` =
  `produccion`. `bootstrap.py` acepta `--mode` / `WRITEONMARS_MODE`.
- Añadido smoke `tests/smoke/vivarium-e2e.sh` con stubs deterministas y skip
  automático si `cargo` no está disponible.

### Constitución v1.6.0 (2026-07-07, modos de proyecto + ejecutores del método)

- **MINOR 1.5.0 → 1.6.0**: nueva sección "Modos de proyecto" — todo proyecto
  declara `mode` en el manifiesto: `produccion` (la IA redacta anclada en
  fuentes; atribución y factualidad obligatorias) o `estudio` (el humano
  escribe; la IA MUST NOT redactar prosa del manuscrito y toda corrección
  exige aceptación humana). Cambio de modo solo por acción humana explícita,
  registrado y con consecuencias de procedencia declaradas.
- Nueva subsección "Ejecutores del método" (§ Arquitectura): la verdad del
  estado vive en archivos, `status.py` la computa, y el método corre íntegro
  con cualquier ejecutor; reglas duras de relevos codificadas
  (escribe-uno-revisa-otro, voz ≠ precisión, detector ≠ corrector). Contexto:
  **Vivarium** (Rust+Tauri, monorepo `vivarium/`) pasa a ser el ejecutor
  orquestado de referencia; Paperclip queda archivado como referencia con sus
  lecciones en `paperclip/FLOW-CONTRACT.md`. Sync impact report en la cabecera
  de la constitución.
- Constitution Check de `plan-template.md` (preset y copia instalada) ampliado
  a los seis principios + fila "Modo de proyecto"; corregida la referencia de
  versión fósil (v1.2.0/v1.3.0 → v1.6.0). El campo `mode` en
  `manifest-schema.json` quedó cubierto por la spec 004 (v1.3.0, arriba).

### Mantenimiento (2026-07-04, auditoría de estructura del repo)

- **Versionado a prueba de fósiles**: `bootstrap.py` deriva la versión de la
  constitución del pie de `memory/constitution.md` en vez de una constante (el
  hardcode ya se había desincronizado dos veces, en 1.3.0 y 1.4.0). El smoke
  `install-on-empty-repo.sh` verifica ahora que el `constitution_version` del
  manifiesto coincide con la constitución instalada.
- **Contratos con fuente única**: `writeonmars/contracts/` es la única copia
  editable. `contracts/` (raíz), `specs/001-framework-architecture/contracts/`
  y los espejos de `docs/` quedaron como punteros; consumidores repuntados
  (`tests/lib/validate-*.sh`, smoke tests, `install/lib/render-manifest.sh`).
- **`manifest-schema` v1.2.1 (PATCH)**: `sector` admite `null` (bootstrap
  escribe `null` hasta que `speckit.constitution` lo fija; con `jsonschema`
  instalado un proyecto recién creado no validaba). Bug cazado por la suite
  nueva de tests.
- **Suite de tests unitarios** en `tests/unit/` (pytest, 133 tests) para los
  scripts deterministas: parsers y gates de `status.py`, `bootstrap.py`
  (incluida la validación nueva del manifest contra el schema antes de
  escribirlo), helpers de `export.py`, backend TF de `index.py` y `close.py`.
  `writeonmars/scripts/requirements.txt` documenta las dependencias opcionales.
- **Robustez de `export.py`**: timeout de 180 s en Chrome headless y mensajes
  de error que documentan `--chrome` / `WOM_CHROME`.
- **Docs de producto (Vivarium) consolidados en `docs/`**: eliminadas las
  copias duplicadas de la raíz (la de `graphify-evaluacion.md` ya había
  divergido), `bookwright-contraste.md` movido a `docs/`, índice nuevo en
  `docs/README.md`. `specs/004-frontend/` (vacía) eliminada: el frontend de
  Vivarium irá en repo propio.
- **Claridad para recién llegados**: banner SUPERSEDED en
  `specs/002-wom-cli/README.md`; `README.md` en `.claude/skills/` (la fuente
  de verdad de las skills es `writeonmars/references/`); fallback de
  registro/sector no cubierto documentado en ambos `_index.md`; la pasada de
  precisión explicita con qué herramientas se verifica en vivo; el how-to
  generaliza la ejecución de cualquier comando en agentes no-Claude.
- **`agents/codex/`**: `pasada-3.md` portado a adaptador alineado con la
  constitución v1.5.0 y marca de sync corregida (`redaccion.md` ya estaba al
  día; la marca "pending" de la constitución era la obsoleta).

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
- **Atribución por afirmación y gate de factualidad (feature 003)**: la pasada 4
  emite, además de `findings.md`, el artefacto `claims.md` con un `ClaimRecord`
  (`contracts/claim-record.schema.json` v1.0) por cada afirmación verificable,
  clasificando la **relación** de cada cita (apoya/matiza/contradice/menciona). De
  ahí `status.py` deriva un **índice de factualidad** determinista (por capítulo y
  global) y un cuarto gate de cierre opcional (`manifest.quality_gates.factuality_*`,
  modo `advisory`/`blocking`). Cambios de contrato aditivos: `pass-output-schema`
  → **v1.1**, `manifest-schema` → MINOR, **constitución v1.3.0 → v1.4.0**. Todo
  retrocompatible: sin `quality_gates` ni `claims.md`, `status.py` se comporta como
  antes (dashboard byte-idéntico). Helpers: `tests/lib/validate-claim.sh`,
  `tests/smoke/test-factuality.sh`.
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

## [1.0.0] - 2026-05-06

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
  esta entrada del CHANGELOG es la marca de lectura para el tag. (Hecho:
  el tag existe y apunta al cierre de US4.)
- El adaptador Codex queda como scaffolding en v1; la validación
  end-to-end con un segundo agente real (Codex o Cursor produciendo una
  guía completa) se difiere a la feature `002-portability-codex` (o
  equivalente) cuando exista ancho de banda operativo.
- Memoria externa: documentada y opcional. El script
  `tools/rebuild-memory.sh` queda especificado en
  `docs/memory-external.md`, no implementado en v1.

[1.0.0]: https://github.com/MarsGotta/writing-framework/releases/tag/v1.0.0
