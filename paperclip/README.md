# Capa de orquestación — Write.OnMars sobre Paperclip

Esta carpeta envuelve el método editorial (el preset `writeonmars/`) en una
**Company de Paperclip**: una organización AI autocontenida con un goal, un equipo
de agentes, un tablero de tareas y un presupuesto. No reescribe el método —lo
orquesta—. La regla rectora del ROADMAP se mantiene: *un solo método, dos
ejecutores* (a mano con un agente, o orquestado con Paperclip).

Paperclip aporta lo que Spec Kit no tiene (scheduler, heartbeats, tablero,
worktrees, presupuestos, gates de aprobación). El preset aporta el qué y el cómo
(comandos `speckit.*`, scripts deterministas, voz y método en `references/`). El
encaje es directo: ver la tabla de mapeo abajo.

## Una sola Company: Write.OnMars · cada Project es una guía

Hay **una única Company, "Write.OnMars"** —la casa editorial—, no una por guía. El
equipo se contrata **una vez** y persiste entre guías: acumula la voz y el método,
comparte instrucciones y presupuesto. Cada guía es un **Project** dentro de la casa.

- **Company** = Write.OnMars (la casa). **Goal** = su misión permanente: producir
  guías técnicas con la voz de la casa y el rigor del método.
- **Project** = una guía. Tiene su propio **goal/brief**, su workspace y su árbol de
  tareas. La Editora jefa abre un Project nuevo por cada guía y lo lleva a cierre.
- **Workspace** = el repo git de ESE Project (Paperclip aísla cada tarea en un git
  worktree: branch fresco por capítulo, sin choques de escritura).
- **Budget** = sobre de la Company + tope por agente (persistentes); opcional, un
  tope por Project para acotar el coste de una guía.
- **Approvals** = los dos checkpoints humanos del método (brief y PDF anotado), por
  Project.

El equipo (los cuatro roles de abajo) es el **mismo para todas las guías**: una
Documentalista sirve a todos los Projects, una Redactora toma capítulos de
cualquiera, etc. Producir en volumen = abrir varios Projects en paralelo bajo la
misma casa.

## El equipo (cuatro oficios)

Agrupamos por **oficio**, no una tarea-por-paso: menos relevos y contexto
coherente por rol (quien investiga es quien verifica; quien escribe es quien
corrige). Cada rol es un agente **permanente** de la Company (se contrata una vez y
sirve a todos los Projects) con su adapter/modelo y su bundle de instrucciones en
`agents/<rol>/`.

| Rol | Oficio · pasos que posee | Adapter sugerido |
|---|---|---|
| **Editora jefa** (orquestador, antes "CEO") | Plan editorial: `setup` · `constitution` · `specify` · `plan` · `intro` · gates · `close`. **No escribe capítulos.** | Claude Code |
| **Documentalista** | `research` (resources/ + web de alta veracidad) + **pasada 4 precisión** (verifica en vivo) | con acceso web; modelo distinto al de redacción |
| **Redactora** | `implement` (capítulos en paralelo) + `revise` (aplica hallazgos a su propio texto) | Claude Code |
| **Editora de mesa** | Pasadas **1·2·3·5** (estructura, utilidad, voz, formato/global) | **modelo distinto** al de la Redactora |

Reglas duras del método que el reparto respeta:

- **Escribe uno, revisa otro**: Redactora ≠ (Editora de mesa, Documentalista).
- **Voz y precisión separadas**: mesa (voz/estructura) vs documentalista (datos).
- **Detector ≠ corrector**: quien revisa anota en `findings.md`; quien corrige es
  la Redactora vía `revise`.

## El flujo, en actos

El modelo es **una tarea por capítulo que se mueve por estados**, no una tarea por
pasada. La Editora jefa hace **un único fan-out** (1 tarea padre = el libro, 1 tarea
hija por capítulo) tras plan+research; a partir de ahí, cada hija recorre su ciclo de
forma **peer-to-peer** entre Redactora, Editora de mesa y Documentalista, sin que la
jefa vuelva a intervenir hasta las etapas globales. La spec detallada del flujo y el
mapeo a la API de Paperclip está en [`FLOW-CONTRACT.md`](FLOW-CONTRACT.md) (fuente de
verdad).

Abres un **Project nuevo** en la Company (goal del Project = "guía sobre X"). Eso
despierta a la **Editora jefa** sobre ese Project:

0. **Scaffold del Project (humano, una vez)** — preparas el base ref con
   `tools/new-guide.sh <guía>`: crea el repo, instala el preset, corre
   `bootstrap.py` (constitución núcleo + manifest) y hace el commit inicial. Conectas
   ese repo a un Project nuevo en Paperclip. La Editora jefa **asume** ese base ref;
   su primer paso es fijar las adendas (`speckit.constitution`: sector+tono).
1. **Encargo** — redacta el brief (`specify`) → **aprobación de estrategia =
   checkpoint 1** (humano firma).
2. **Documentación** — tarea → **Documentalista**: `research.md` con
   CitationRecord. Bloquea el plan.
3. **Arquitectura** — con research, la Editora jefa diseña el temario (`plan`).
4. **Fan-out único** — con el temario fijado, la Editora jefa crea **1 tarea padre**
   (el libro) y **1 tarea hija por capítulo** (`in_progress`, asignada a la
   Redactora). Es el único reparto que hace; no vuelve a crear tareas por capítulo.
   Cada hija corre en un worktree aislado (paralelo real).
5. **Ciclo de cada hija (peer-to-peer, event-driven)** — el capítulo entero vive en
   **una** tarea que cambia de estado:
   - **Redactora escribe** (DRAFTING) → al terminar, `in_review` y reasigna a la
     **Editora de mesa**.
   - **Mesa** corre las pasadas **1·2·3** → anota en `findings.md` → `in_review` y
     reasigna a la **Documentalista**.
   - **Documentalista** corre la pasada **4** y **DECIDE**: si hay accionables
     abiertos (crítico+medio, de Mesa o suyos) → `in_progress` de vuelta a la
     **Redactora** (revise quirúrgico, "ver `findings.md`"); si hay **0** → `done`
     (APPROVED). Severidad: crítico+medio fuerzan revise; **bajo = aviso** (no
     bloquea).
   - La Redactora aplica el revise → `in_review` a Mesa otra vez (nueva ronda) hasta
     que la hija quede `done`.
6. **Despertar para las globales** — la Documentalista que marca la **última** hija
   `done` despierta a la **Editora jefa** (`all_chapters_approved` en
   `status.py --json`). No hay routine por evento: las etapas globales las avanza la
   jefa al despertar.
7. **Cierre de libro** — la jefa corre las etapas globales en orden: **pasada 5
   global** (Mesa) → `status.py --gate` → `intro` + `export.py` → PDF.
8. **Galeradas = checkpoint 2** — humano anota el PDF → webhook/routine →
   `feedback_intake.py` → re-despacho quirúrgico de tareas a la Redactora.
9. **Imprenta** — `close.py` → gate + PDF final. Goal cumplido.

Cada relevo dentro del ciclo es un cambio de **estado + asignado** de la **misma**
tarea-capítulo, que despierta al rol siguiente (peer-to-peer); así no se pierde el
hilo del capítulo. El orquestador nunca acumula el ruido de la redacción: hace el
fan-out una vez y luego solo despierta para las globales, leyendo el estado desde
disco con `status.py --json` (`by_chapter`, `all_chapters_approved`).

## El grafo de tareas (dependencias)

Una tarea **padre** (el libro) y una **hija por capítulo**. La hija no se subdivide:
es el capítulo entero moviéndose por estados (el ciclo peer-to-peer va dentro de la
misma tarea, no en tareas hermanas).

```
scaffold           (humano · tools/new-guide.sh)   [una vez, base ref]
 └─ constitution    (Editora jefa · adendas: sector+tono)
     └─ specify     (Editora jefa)        ── approval: estrategia ──┐
         └─ research (Documentalista)                               │
             └─ plan (Editora jefa)                                 │
                 └─ FAN-OUT ÚNICO (Editora jefa, una vez):          │
                     padre = el libro                               │
                      ├─ hija cap-01 (worktree) ─┐                  │
                      ├─ hija cap-02 (worktree)  │ paralelo         │
                      └─ hija cap-NN (worktree) ─┘                  │
                           │   ciclo DENTRO de cada hija (1 tarea,  │
                           │   cambia estado+asignado, peer-to-peer):
                           │     in_progress → Redactora escribe    │
                           │     in_review   → Mesa (pasadas 1·2·3) │
                           │     in_review   → Doc (pasada 4·DECIDE)│
                           │       ├─ accionables → in_progress     │
                           │       │   (Redactora · revise) ↺ Mesa  │
                           │       └─ 0 accionables → done (APPROVED)
                           ▼                                        │
                  última hija done → despierta a la Editora jefa ───┘
                      └─ pasada 5 global (Mesa)
                          └─ status --gate
                              └─ intro+export (Editora jefa)
                                  └─ approval: PDF anotado (checkpoint 2)
                                      └─ feedback_intake → revise*
                                          └─ close (Editora jefa, job)
```

## El heartbeat: cómo decide la Editora jefa

El orquestador no razona sobre prosa: cuando despierta corre

```bash
python3 .specify/presets/writeonmars/scripts/status.py --project-dir . --json
```

y lee el estado desde disco. Hasta el fan-out, sigue `next_step` (`setup` →
`specify` → `research` → `plan`) y, al llegar a `plan` OK, hace el **fan-out único**
(padre + 1 hija por capítulo). A partir de ahí **no loopea por pasos**: el ciclo de
cada capítulo es peer-to-peer entre los workers, y la jefa solo vuelve a actuar
cuando la última hija `done` la despierta. Entonces lee `all_chapters_approved` (y el
desglose `by_chapter`: `drafted`, `passes_done`, `revise_pending`, `approved`) y
avanza las **etapas globales** en orden (pasada 5 → gate → intro+export → checkpoint
→ close). Todo el estado vive en disco (manifest, `chapters/` vs temario,
`findings.md`); la jefa es una máquina de estados sin memoria, por eso su contexto se
mantiene sin ruido. Detalle en `agents/editora-jefa/HEARTBEAT.md`.

## Mapeo Paperclip ↔ Write.OnMars

| Paperclip | Write.OnMars |
|---|---|
| Company / Goal | la casa "Write.OnMars" / su misión permanente |
| Project / goal del Project | una guía / su brief |
| Agent + adapter | rol editorial permanente + modelo (cross-model nativo) |
| Bundle AGENTS/SOUL/HEARTBEAT | `writeonmars/AGENTS.md` + `references/voz` + estos bundles |
| Task board (backlog→…→done) | 1 tarea padre (libro) + 1 hija por capítulo; el estado de la hija (`in_progress`/`in_review`/`done`) = la fase del ciclo del capítulo |
| Reasignar tarea (`assigneeAgentId`) | relevo peer-to-peer Redactora→Mesa→Doc→Redactora dentro de la misma tarea-capítulo |
| Comentarios de la tarea | puntero corto a `findings.md` (la verdad vive en `findings.md`, no en el comentario) |
| Workspace del Project (repo local o git) | el repo de la guía; worktrees para aislar capítulos en paralelo |
| Runtime job (sin agente) | `status.py` / `close.py` / `export.py` / `feedback_intake.py` |
| Strategy approval | checkpoint 1 (brief/temario) |
| Approval previa a close | checkpoint 2 (PDF anotado) |
| Budget company/agente | presupuesto por guía y por rol |

## Estado

Primer corte de la capa #3 del ROADMAP, montado y arrancado (2026-06-20).

- **Modelo de flujo**: tarea-por-capítulo que se mueve por estados (fan-out único +
  ciclo peer-to-peer + globales por wake), con `maxConcurrentRuns:1` en la jefa para
  idempotencia estructural. La spec viva está en
  [`FLOW-CONTRACT.md`](FLOW-CONTRACT.md).
- **Construido en el repo**: el reparto de roles, los bundles de instrucciones,
  `status.py --json` (con `by_chapter` y `all_chapters_approved`, la brújula del
  fan-out y de las globales), `tools/new-guide.sh` (scaffolding de una guía en un
  comando) y `hire-team.sh` (contratar el equipo por CLI).
- **Montado en Paperclip**: la Company "Write.OnMars", el equipo permanente de 4
  roles (Editora jefa en Claude/Opus; Documentalista en Codex; Redactora en Opus;
  Editora de mesa en Sonnet) y el primer Project (`guide-nlp`) con workspace local
  (`sourceType=local_path`, sin GitHub). El flujo se arranca asignando un issue a la
  Editora jefa, que despierta sola (heartbeat event-driven).
- **Cómo se opera**: por el CLI `paperclipai` (company/agent/project/workspace/
  issue/goal). Paso a paso en `../writeonmars/docs/how-to.md` ("Cómo correr todo
  desatendido bajo Paperclip"), incluida la autenticación de Codex con suscripción.

Pendiente: el webhook del checkpoint 2 (PDF anotado → `feedback_intake`),
presupuestos por Project, y varias guías en paralelo (hoy, una a la vez).
