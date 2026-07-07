# Feature Specification: Núcleo headless de Vivarium (ejecutor del método)

**Feature Branch**: `004-vivarium-core`
**Created**: 2026-07-07
**Status**: Draft
**Input**: User description: "Núcleo headless de Vivarium (ejecutor del método Write.OnMars): contrato del ejecutor promovido desde paperclip/FLOW-CONTRACT.md §§0-2; bootstrap de proyecto con manifest `mode`, roots/ y decisions.jsonl; runner por estados sobre status.py --json con agentes BYOM; cambio de modo en caliente. La implementación la hará Codex: spec, plan y tareas autocontenidos y agente-neutrales (Principio VI)."

> **Restricción de ejecución (no negociable para plan y tareas)**: la
> implementación la realizará **Codex** (u otro agente distinto de quien
> redacta esta spec). Todo artefacto derivado (plan, tasks, contratos) MUST ser
> autocontenido y agente-neutral: rutas explícitas, contratos citados por
> archivo, criterios de aceptación verificables por script (`cargo test`,
> `pytest`, shell), sin depender de skills, memoria o convenciones de un agente
> concreto. Es la misma regla del Principio VI de la constitución (v1.6.0)
> aplicada al propio desarrollo del framework.

## User Stories *(modo software)*

### User Story 1 - Crear un proyecto editorial listo en una orden (Priority: P1)

Marcela (operadora, futura usuaria de la app) crea un proyecto nuevo de
Vivarium con una sola orden del CLI headless. El resultado es un repositorio
editorial operativo: preset Write.OnMars instalado, manifiesto válido con el
modo declarado (`produccion` o `estudio`, con default según el tipo de
proyecto), carpeta de fuentes (`roots/`) con su convención documentada,
registro de decisiones (`decisions.jsonl`) inicializado y un commit base. Es la
generalización de `tools/new-guide.sh` como capacidad del núcleo, no como
script suelto.

**Why this priority**: sin proyecto no hay nada que orquestar; el bootstrap es
además la primera superficie que la app Tauri envolverá ("nuevo proyecto sin
terminal", `docs/vivarium.md` § 13 etapa 2). Todo lo demás depende de él.

**Independent Test**: ejecutar la orden de creación sobre un directorio vacío
y verificar por script que el repo queda operativo (manifiesto válido contra
su schema, `status.py --json` responde con `next_step`, estructura de carpetas
presente, commit base existente), sin editar ningún archivo a mano.

**Acceptance Scenarios**:

1. **Given** un directorio vacío, **When** la operadora crea un proyecto de
   tipo "guía técnica", **Then** el repo queda con preset instalado, manifiesto
   válido con `mode: produccion`, `roots/`, `decisions.jsonl` y commit base, y
   `status.py --json` devuelve un `next_step` accionable.
2. **Given** un directorio vacío, **When** la operadora crea un proyecto de
   tipo "novela", **Then** el manifiesto queda con `mode: estudio` y el resto
   de la estructura es idéntica.
3. **Given** un manifiesto sin campo `mode` (proyecto anterior a esta feature),
   **When** cualquier componente del núcleo lo lee, **Then** lo interpreta como
   `produccion` sin error.

---

### User Story 2 - Producir una guía sin vigilar el pipeline (Priority: P2)

La operadora lanza el runner sobre un proyecto en modo producción. El runner
lee el estado desde disco (`status.py --json`), despacha a los agentes
configurados (BYOM: cada rol tiene su orden de CLI configurable) los relevos
del ciclo por capítulo —redacción → revisión de mesa → precisión → revise si
hay accionables— y las etapas globales cuando todos los capítulos quedan
aprobados. Los dos checkpoints humanos (brief y PDF anotado) detienen el flujo
y esperan a la persona. Si el runner se interrumpe y se relanza, continúa donde
estaba sin duplicar trabajo.

**Why this priority**: es el reemplazo funcional de Paperclip — el motivo de la
feature. Depende del bootstrap (US1) para tener proyectos sobre los que correr.

**Independent Test**: sobre un proyecto sintético con agentes stub (órdenes de
CLI falsas que escriben salidas deterministas), el runner lleva 3 capítulos de
DRAFTING a APPROVED y dispara la etapa global, con 0 despachos duplicados
incluso matando y relanzando el runner a mitad del ciclo.

**Acceptance Scenarios**:

1. **Given** un proyecto con temario de N capítulos y agentes configurados,
   **When** el runner corre, **Then** cada capítulo avanza
   DRAFTING → IN_REVIEW → (NEEDS_REVISE → IN_REVIEW)* → APPROVED y las reglas
   de relevo se cumplen: quien redacta una unidad no la revisa, voz y precisión
   se despachan por separado, quien revisa anota hallazgos y quien corrige es
   quien redacta.
2. **Given** un runner interrumpido a mitad de un despacho, **When** se
   relanza, **Then** no crea trabajo duplicado (idempotencia estructural:
   verifica el estado en disco antes de cada despacho) y el proyecto termina en
   el mismo estado que sin interrupción.
3. **Given** todos los capítulos APPROVED, **When** el runner evalúa el estado,
   **Then** dispara las etapas globales en orden (pasada global → export →
   checkpoint humano → feedback/cierre) y se detiene en el checkpoint hasta la
   acción humana.
4. **Given** un agente que falla o no produce salida, **When** el runner
   procesa el resultado, **Then** el estado en disco queda intacto, el reintento
   es seguro y el fallo queda registrado; el runner jamás escribe prosa del
   manuscrito por su cuenta.

---

### User Story 3 - Cambiar de modo con consecuencias claras (Priority: P3)

La operadora cambia el modo de un proyecto (por ejemplo, de `estudio` a
`produccion` para encargar una parte documental). El cambio exige confirmación
explícita que declara la consecuencia de procedencia (perder la demostrabilidad
de autoría humana para lo que la IA redacte desde ese momento), queda
registrado en el manifiesto (modo nuevo, fecha, modo anterior) y el runner
ajusta su comportamiento inmediatamente ("en caliente"): en `estudio` no
despacha redacción de manuscrito bajo ninguna circunstancia.

**Why this priority**: es la garantía de producto (constitución v1.6.0
§ Modos de proyecto); sin ella el hot-swap sería un footgun de certificación.
Depende de que exista el campo `mode` (US1).

**Independent Test**: script que intenta el cambio sin confirmación (debe
fallar), con confirmación (debe registrar), y verifica que un runner sobre un
proyecto `estudio` rechaza cualquier despacho de redacción.

**Acceptance Scenarios**:

1. **Given** un proyecto `estudio`, **When** se solicita el cambio a
   `produccion` sin confirmación explícita, **Then** el cambio no se aplica y
   se muestra la consecuencia de procedencia.
2. **Given** la confirmación explícita, **When** el cambio se aplica, **Then**
   el manifiesto registra modo nuevo, fecha y modo anterior, y el evento queda
   en `decisions.jsonl`.
3. **Given** un proyecto `estudio`, **When** el runner evalúa qué despachar,
   **Then** ninguna tarea de redacción de manuscrito se despacha (aunque el
   pipeline de revisión de estudio aún no exista, el guardarraíl aplica ya).

---

### Edge Cases

- Runner interrumpido (kill) en cualquier punto → el relanzamiento es seguro:
  el estado vive en archivos y cada despacho re-verifica antes de crear
  (lección de los bugs #2/#3 de guide-nlp, `ROADMAP.md`).
- Dos runners concurrentes sobre el mismo proyecto → el segundo detecta el
  primero (lock/single-flight) y no duplica (lección del doble heartbeat
  WRI-44).
- `status.py` va por delante del trabajo en vuelo → el runner no cierra ni
  avanza etapas globales mientras tenga despachos sin disposición (lección
  "la jefa no cierra con hijas abiertas").
- Proyecto recién creado sin `specs/` → `status.py` ya lo tolera; el runner
  debe proponer el siguiente paso (constitution/specify), no fallar.
- Cambio de modo con un capítulo a medio ciclo → el cambio se registra pero no
  interrumpe despachos en vuelo; el comportamiento nuevo aplica desde el
  siguiente despacho.
- Agente configurado inexistente o sin permisos → error claro antes de empezar
  el ciclo, no a mitad.
- Manifiesto con `mode` inválido (valor fuera del enum) → error de validación
  explícito, nunca interpretación silenciosa.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (bootstrap)**: el núcleo MUST crear un proyecto editorial operativo
  en una orden: repositorio git inicializado, preset `writeonmars` instalado,
  manifiesto válido contra `writeonmars/contracts/manifest-schema.json`,
  carpeta `roots/` con su convención documentada (fichas markdown
  OKF-compatibles: un concepto por archivo, frontmatter con `type` y `alias`;
  solo la convención y la carpeta, sin índice ni grafo), `decisions.jsonl`
  vacío con su formato documentado, y commit base. Paridad funcional con
  `tools/new-guide.sh` (operador/email heredados de git, idempotencia).
- **FR-002 (modo en el manifiesto)**: el manifest-schema MUST incorporar el
  campo `mode` (`produccion` | `estudio`; ausencia = `produccion`). El default
  al crear se deriva del tipo de proyecto declarado (guía técnica, tutorial,
  documentación, no-ficción fundamentada → `produccion`; novela, relato,
  poesía, guion, académico personal → `estudio`), siempre sobrescribible por
  la operadora.
- **FR-003 (estado solo desde disco)**: el runner MUST leer el estado editorial
  exclusivamente de `status.py --json` (`next_step`, `by_chapter`,
  `all_chapters_approved`, `revise_pending`, gates) y de los archivos del
  proyecto. MUST NOT mantener estado de negocio propio: retirar el runner deja
  el proyecto continuable a mano con los mismos comandos del preset.
- **FR-004 (ciclo por capítulo)**: el runner MUST implementar el contrato de
  flujo: una unidad de trabajo por capítulo que transita
  DRAFTING → IN_REVIEW → NEEDS_REVISE → APPROVED (estados derivados de
  archivos, `paperclip/FLOW-CONTRACT.md` § 1), fan-out único tras plan+research,
  etapas globales al aprobar el último capítulo (§ 2), y severidad
  crítico+medio fuerza revise / bajo avisa.
- **FR-005 (reglas de relevo)**: en cada despacho el runner MUST garantizar
  escribe-uno-revisa-otro (el agente que redactó una unidad no la revisa),
  voz ≠ precisión (pasadas despachadas por separado, con agentes/modelos
  distintos cuando la configuración lo permita) y detector ≠ corrector (los
  revisores anotan en `findings.md`; corrige quien redacta).
- **FR-006 (idempotencia estructural)**: el runner MUST re-verificar el estado
  en disco antes de cada despacho y MUST impedir ejecuciones concurrentes
  sobre el mismo proyecto (lock). La idempotencia es estructural, no
  instruccional: relanzar tras una interrupción nunca duplica trabajo.
- **FR-007 (BYOM)**: los agentes MUST ser configurables por rol como órdenes de
  CLI (con variables para el prompt/archivo de entrada), sin acoplarse a un
  proveedor. La configuración MUST validarse antes de iniciar el ciclo y MUST
  demostrarse con al menos dos agentes distintos (los adaptadores existentes en
  `agents/claude/` y `agents/codex/` son la referencia).
- **FR-008 (guardarraíl de modo)**: con `mode: estudio`, el runner MUST NOT
  despachar redacción de manuscrito (comandos que crean o reescriben
  `chapters/` / `content/`); solo revisión, verificación y anotación. El
  guardarraíl aplica aunque el pipeline de revisión de estudio (spec 005) no
  exista aún.
- **FR-009 (cambio de modo)**: el cambio de modo MUST ser una acción humana
  explícita con confirmación que declare la consecuencia de procedencia; MUST
  registrarse en el manifiesto (modo nuevo, modo anterior, fecha) y en
  `decisions.jsonl`; MUST aplicar en caliente al siguiente despacho.
- **FR-010 (registro de decisiones)**: todo despacho, disposición (aprobado /
  revise / fallo) y cambio de modo MUST quedar como línea append-only en
  `decisions.jsonl` con formato versionado (base del flywheel y de la
  procedencia, `docs/vivarium.md` § 9).
- **FR-011 (contrato del ejecutor)**: las §§ 0-2 de `paperclip/FLOW-CONTRACT.md`
  MUST promoverse a contrato publicado en `writeonmars/contracts/`
  (executor-contract), del que este runner es la primera implementación
  conforme; la conformidad MUST ser verificable por los criterios de este spec.
- **FR-012 (superficie headless)**: el núcleo MUST exponer un CLI con, como
  mínimo: crear proyecto, ver estado (passthrough de `status.py --json`),
  ejecutar un paso, ejecutar hasta bloquearse (checkpoint humano o fallo), y
  cambiar de modo. Cada orden MUST devolver códigos de salida verificables por
  script.
- **FR-013 (checkpoints humanos)**: el runner MUST detenerse en los dos
  checkpoints del método (brief firmado; PDF anotado tras export) y MUST NOT
  firmar, aprobar ni sintetizar feedback humano por su cuenta.

### Key Entities

- **Proyecto editorial**: repositorio git con preset instalado; toda su verdad
  de estado vive en sus archivos (manifiesto, `specs/`, `chapters/`,
  `findings.md`, `claims.md`).
- **Manifiesto** (`.writeonmars-manifest.json`): identidad del proyecto; gana
  el campo `mode` y el registro de cambios de modo.
- **Unidad de contenido (capítulo)**: la unidad que transita los estados del
  ciclo; sus estados se derivan de archivos, nunca se almacenan aparte.
- **Despacho (relevo)**: invocación de un agente con rol, entrada y salida
  esperada; efímero, registrado en `decisions.jsonl`.
- **Registro de decisiones** (`decisions.jsonl`): log append-only versionado de
  despachos, disposiciones y cambios de modo.
- **Ficha de Root** (`roots/*.md`): fuente/entidad de grounding,
  OKF-compatible (un concepto por archivo, frontmatter `type` + `alias`); en
  esta feature solo existe la convención y la carpeta.
- **Contrato del ejecutor**: documento normativo en `writeonmars/contracts/`
  que fija estados, relevos, etapas globales e idempotencia para cualquier
  ejecutor.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: un proyecto nuevo pasa de orden de creación a "listo para el
  primer paso del método" en menos de 2 minutos, sin editar archivos a mano, y
  su manifiesto valida contra el schema.
- **SC-002**: una guía sintética de 3 capítulos con agentes stub llega de cero
  a `all_chapters_approved` y etapa global disparada sin intervención humana
  (salvo checkpoints simulados) y con **0 despachos duplicados**, incluida una
  interrupción y relanzamiento del runner a mitad del ciclo.
- **SC-003**: retirar el runner no pierde nada: tras cualquier punto de parada,
  `status.py --json` propone el mismo `next_step` que antes de introducirlo y
  el proyecto puede continuarse a mano con los comandos del preset.
- **SC-004**: en un proyecto `estudio`, cero contenido de manuscrito escrito
  por agentes (verificable con el historial git y `decisions.jsonl`).
- **SC-005**: el 100 % de los cambios de modo quedan registrados (modo
  anterior, nuevo, fecha) y ningún cambio ocurre sin confirmación explícita.
- **SC-006**: todos los criterios anteriores se verifican por scripts de test
  ejecutables por cualquier agente o humano (sin pasos manuales no
  documentados); la suite existente del repo (`pytest` + smoke) sigue en verde.

## Assumptions

- **Implementación por Codex**: el plan y las tareas se redactarán para que un
  agente distinto los ejecute sin contexto de esta conversación; toda decisión
  vive en artefactos del repo (spec, plan, contratos), no en memoria del
  agente.
- **Monorepo**: el núcleo vive en `vivarium/` de este repo (frontera documentada
  en `vivarium/README.md`); la extracción a repo propio es posterior y no
  condiciona el diseño.
- **Sidecar Python**: los scripts del preset (`status.py`, `bootstrap.py`,
  `export.py`, …) son la verdad compartida y **no se portan**; el núcleo los
  invoca como procesos y consume su JSON. El empaquetado del sidecar para
  distribución de la app queda explícitamente fuera de esta feature.
- **Fuera de alcance**: la app Tauri y el editor visual; el pipeline de
  revisión del modo estudio (spec 005 — aquí solo su guardarraíl); el índice y
  grafo de Roots (etapa 2 del roadmap de producto); presupuestos por proyecto;
  varias guías en paralelo; el anclaje persistente (Core) — los findings usan
  el régimen efímero `fichero:línea` ya decidido.
- **Compatibilidad**: los proyectos existentes (sin `mode`) siguen funcionando
  como `produccion`; `tools/new-guide.sh` permanece hasta que el bootstrap del
  núcleo demuestre paridad (se retira en una feature posterior).
- **Checkpoint 2 manual**: el PDF anotado sigue entrando por
  `feedback_intake.py` manualmente; el webhook queda como pendiente del
  ROADMAP, no de esta feature.
