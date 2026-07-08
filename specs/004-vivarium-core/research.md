# Research — 004-vivarium-core (Phase 0)

Decisiones técnicas resueltas antes del diseño. Formato: decisión / porqué /
alternativas. No quedan `NEEDS CLARIFICATION` abiertos.

## R1. Toolchain Rust

- **Decisión**: Rust estable, MSRV 1.75, edition 2021. Sin nightly, sin
  features inestables.
- **Rationale**: 1.75 es la referencia que ya usa la plantilla del plan del
  repo; edition 2021 evita exigir toolchains recientes a colaboradores.
- **Alternativas**: edition 2024 (exige rustc ≥1.85; no aporta nada que esta
  feature necesite).

## R2. Dependencias del workspace

- **Decisión**: `clap` 4 (derive) para el CLI; `serde` + `serde_json` para los
  contratos JSON (status.py, manifiesto, decisions); `toml` para
  `.vivarium/config.toml`; `git2` para init/add/commit del bootstrap;
  `fd-lock` para el lock de proyecto; `thiserror` (core) + `anyhow` (cli);
  `assert_cmd` + `tempfile` como dev-dependencies de los tests de integración.
- **Rationale**: todas son crates maduras y estándar; `git2` está fijada por
  `docs/vivarium.md` § 10 (libgit2). `fd-lock` da lock advisory del SO que se
  libera solo si el proceso muere — resuelve el edge case de lock huérfano sin
  inventar staleness a mano.
- **Alternativas**: git por subproceso (más simple, pero el doc de producto ya
  decidió libgit2 y el bootstrap necesita robustez de errores); lockfile con
  PID + comprobación de vida (frágil, reinventa lo que el SO ya da).

## R3. Sidecar Python: descubrimiento e invocación

- **Decisión**: el intérprete se resuelve en este orden: variable de entorno
  `VIVARIUM_PYTHON` → `python3` en PATH. Los scripts se invocan por subproceso
  con cwd = raíz del proyecto editorial:
  `<python> .specify/presets/writeonmars/scripts/status.py --json`. El
  contrato es la salida JSON y el exit code; stderr se propaga al log del
  runner. Si el script o el intérprete no existen → error explícito antes de
  iniciar el ciclo (edge case "agente/herramienta inexistente").
- **Rationale**: FR-003 y la frontera de `vivarium/README.md`: los scripts son
  la verdad compartida de todos los ejecutores. Cualquier puerto a Rust
  duplicaría lógica de negocio y rompería la neutralidad (Principio VI).
- **Alternativas**: portar `status.py` a Rust (rechazado: acoplamiento y doble
  fuente de verdad); embeber Python (problema de distribución, fuera de
  alcance — anotado como decisión abierta de empaquetado en la spec).

## R4. Instalación del preset en el bootstrap

- **Decisión**: el bootstrap invoca el CLI `specify` por subproceso, igual que
  `tools/new-guide.sh` (`specify init --integration <agente> --here --force
  --ignore-agent-tools` + `specify preset add --dev <ruta-al-preset>`), y
  después `python3 .specify/presets/writeonmars/scripts/bootstrap.py`.
  Herramientas requeridas (git, python3, specify) se verifican al arrancar con
  mensajes de error accionables. La ruta del preset se toma de config/flag,
  con default a la copia local del framework.
- **Rationale**: paridad funcional exigida por FR-001; `specify` es dueño de
  su layout (`.specify/`) y replicarlo a mano acoplaría a internals (la
  estrategia "fachada" de `docs/vivarium.md` § 7 lo prohíbe).
- **Alternativas**: copiar el preset a mano (frágil ante cambios de Spec Kit);
  vendorizar Spec Kit (fuera de alcance).

## R5. Configuración BYOM

- **Decisión**: `.vivarium/config.toml` en la raíz del proyecto editorial
  (formato exacto en `contracts/byom-config.md`). Tres roles obligatorios —
  `redactora`, `editora_mesa`, `documentalista` — cada uno con su plantilla de
  orden de CLI y placeholders (`{prompt_file}`, `{project_dir}`, `{chapter}`).
  El rol de orquestación (la "Editora jefa" de Paperclip) **no es un agente**:
  es el propio runner. `.vivarium/` se añade al `.gitignore` del proyecto en
  el bootstrap (contiene rutas locales; el lock tampoco se versiona).
- **Rationale**: FR-007 (BYOM sin acoplarse a proveedor); el mapeo rol→modelo
  cruzado (Redactora ≠ Editora de mesa) se hereda del roster de Paperclip pero
  como configuración, no como código. Que la jefa sea el runner elimina la
  clase entera de bugs de heartbeat/idempotencia instruccional (ROADMAP
  2026-06-20).
- **Alternativas**: config global en `~/.config/vivarium` (peor: cada proyecto
  puede querer agentes distintos; se puede añadir después como fallback); JSON
  (TOML es más editable a mano, y la config es de la operadora).

## R6. Despacho de agentes: prompt y contrato de salida

- **Decisión**: para cada relevo el runner (1) resuelve el prompt canónico del
  paso — los comandos del preset (`writeonmars/commands/speckit.*.md`) y los
  prompts de `agents/<agente>/prompts/*.md` como referencia de adaptación —,
  (2) escribe un archivo de tarea temporal bajo `.vivarium/tasks/` con el
  encargo concreto (paso, capítulo, rutas), (3) ejecuta la plantilla de orden
  del rol sustituyendo placeholders, (4) valida el resultado **por el estado
  en disco** (¿apareció `chapters/NN-*.md`? ¿`findings.md` ganó el bloque de la
  pasada?), nunca por la salida de texto del agente.
- **Rationale**: FR-003 (verdad en archivos) aplicado también a la
  verificación de despachos; es la misma disciplina de FLOW-CONTRACT § 3.6
  (el comentario es puntero, el archivo es la verdad).
- **Alternativas**: parsear stdout del agente (frágil y dependiente del
  proveedor — violaría el Principio VI).

## R7. Idempotencia y concurrencia

- **Decisión**: lock advisory sobre `.vivarium/lock` (fd-lock) tomado por
  `step`/`run`; si está tomado, salida inmediata con exit code propio (ver
  `contracts/cli-vivarium.md`). Antes de cada despacho, re-lectura completa de
  `status.py --json` + verificación de que la salida esperada del despacho no
  existe ya (p. ej. no redactar un capítulo cuyo archivo ya existe). Los
  despachos en vuelo se registran en `decisions.jsonl` (evento `dispatch` sin
  `disposition` aún) y el runner no avanza etapas globales con despachos sin
  disposición.
- **Rationale**: FR-006 y las lecciones pagadas: bugs #2/#3 de guide-nlp
  (re-despacho por tanda), doble heartbeat WRI-44 (race check-then-create), y
  "la jefa no cierra con hijas abiertas". La idempotencia estructural vive en
  código, no en instrucciones a un agente.
- **Alternativas**: dedup por fingerprint de tarea en un almacén propio
  (rechazado: sería estado de negocio del ejecutor, FR-003).

## R8. Mapeo `next_step` → acción del runner

- **Decisión**: tabla determinista (detalle en `data-model.md` § 4):
  `setup`/`constitution`/`specify` → pasos con humano en el bucle (el runner
  se detiene y lo dice: checkpoint 1 = brief firmado); `research`, `plan` →
  despacho a `documentalista`/`redactora` según el paso; `implement` → fan-out
  por capítulo (`by_chapter`); `review` → pasadas 1-3 a `editora_mesa`, 4 a
  `documentalista`; `revise` → `redactora` por capítulo con hallazgos; global:
  pasada 5 → `editora_mesa`, export → sidecar `export.py`, feedback → humano
  (checkpoint 2), `close` → sidecar `close.py` solo con gates en verde.
- **Rationale**: FR-004/FR-005/FR-013; es FLOW-CONTRACT §§ 1-2 con el runner
  ocupando el lugar de la jefa.
- **Alternativas**: dejar que un agente orquestador decida (rechazado: la
  orquestación debe ser determinista; el juicio editorial ya vive en las
  pasadas).

## R9. Modo en el manifiesto

- **Decisión**: `manifest-schema.json` bump MINOR (1.2.1 → 1.3.0): campo
  opcional `mode` (`enum: ["produccion", "estudio"]`) y `mode_history` (array
  de `{from, to, date}`); ausencia de `mode` = `produccion` (compatibilidad
  total con proyectos existentes). Detalle exacto en
  `contracts/manifest-mode.md`. El default al crear se deriva del tipo de
  proyecto (tabla en `data-model.md` § 2), siempre sobrescribible con flag.
- **Rationale**: FR-002/FR-009; constitución v1.6.0 § Modos de proyecto ya
  fija la semántica; el sync impact report de la constitución dejó este campo
  como pendiente explícito de esta feature.
- **Alternativas**: archivo de modo aparte (fragmenta la identidad del
  proyecto que ya vive en el manifiesto).

## R10. Secuencialidad v1

- **Decisión**: el runner v1 despacha **un relevo a la vez** (sin capítulos en
  paralelo). El diseño deja el paralelismo por worktrees como extensión
  (interfaz de despacho que no asume exclusividad del working tree), pero no
  se implementa.
- **Rationale**: SC-002 se cumple sin paralelismo; los worktrees paralelos de
  Paperclip fueron fuente de complejidad y el valor v1 es fiabilidad
  (idempotencia + reanudación). "Varias guías en paralelo" ya está fuera de
  alcance en la spec.
- **Alternativas**: paralelismo por capítulo desde v1 (más rápido de reloj,
  pero multiplica los modos de fallo antes de tener la base validada).

## R11. Estrategia de tests

- **Decisión**: (a) unit tests en `vivarium-core` (parseo de status JSON con
  fixtures reales copiadas de `tests/fixtures/003-factualidad-project/`,
  derivación de estados, reglas de despacho, guardarraíl de estudio, registro
  de decisiones); (b) integración en `vivarium-cli` con `assert_cmd` +
  agentes stub (scripts de shell deterministas en
  `vivarium/crates/vivarium-cli/tests/stubs/`) que simulan redacción/pasadas
  escribiendo archivos; (c) smoke e2e `tests/smoke/vivarium-e2e.sh` que compila
  el CLI, crea un proyecto sintético de 3 capítulos y lo lleva a
  `all_chapters_approved` con kill+relaunch a mitad (SC-002), integrado en
  `tests/smoke/run-all.sh`; (d) suites existentes (`pytest tests/unit`,
  smokes) intactas y en verde (SC-006).
- **Rationale**: cada SC de la spec queda cubierto por un test ejecutable por
  script; ningún paso de verificación depende de un agente concreto.
- **Alternativas**: mocks de status.py en Rust (rechazado: el contrato real es
  el script; los fixtures del repo ya dan proyectos sintéticos válidos).
