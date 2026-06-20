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
4. **Redacción** — **una tarea por capítulo** → **Redactoras** en worktrees
   aislados (paralelo real).
5. **Mesa** (event-driven) — capítulo `in_review` despierta en paralelo, con otro
   modelo: Editora de mesa (pasadas 1/2/3) + Documentalista (pasada 4). Hallazgos
   → `findings.md`.
6. **Corrección** — tarea `revise` por capítulo → la Redactora aplica solo lo
   señalado.
7. **Cierre de libro** — pasada 5 global → `status.py --gate` → `intro` +
   `export.py` → PDF.
8. **Galeradas = checkpoint 2** — humano anota el PDF → webhook/routine →
   `feedback_intake.py` → re-despacho quirúrgico de tareas a la Redactora.
9. **Imprenta** — `close.py` → gate + PDF final. Goal cumplido.

Cada relevo es un cambio de **estado de tarea** que despierta al rol siguiente. El
orquestador nunca acumula el ruido de la redacción: delega y lee el estado desde
disco con `status.py --json`.

## El grafo de tareas (dependencias)

```
scaffold           (humano · tools/new-guide.sh)   [una vez, base ref]
 └─ constitution    (Editora jefa · adendas: sector+tono)
     └─ specify     (Editora jefa)        ── approval: estrategia ──┐
         └─ research (Documentalista)                               │
             └─ plan (Editora jefa)                                 │
                 ├─ implement:cap-01 (Redactora · worktree) ─┐      │
                 ├─ implement:cap-02 (Redactora · worktree)  │ paralelo
                 └─ implement:cap-NN (Redactora · worktree) ─┘      │
                      └─ por capítulo, al pasar a in_review:        │
                          ├─ review:1-2-3 (Editora de mesa)         │
                          └─ review:4     (Documentalista)          │
                              └─ revise:cap-NN (Redactora)          │
                                  └─ review:5 global (Mesa) ────────┘
                                      └─ status --gate
                                          └─ intro+export (Editora jefa)
                                              └─ approval: PDF anotado (checkpoint 2)
                                                  └─ feedback_intake → revise*
                                                      └─ close (Editora jefa, job)
```

## El heartbeat: cómo decide la Editora jefa

El orquestador no razona sobre prosa: en cada heartbeat corre

```bash
python3 .specify/presets/writeonmars/scripts/status.py --project-dir . --json
```

y lee el campo `next_step` (`setup` → `specify` → `research` → `plan` →
`implement` → `review` → `revise` → `close`). Según el paso, crea/asigna la tarea
al rol correspondiente. Todo el estado vive en disco (manifest, `chapters/` vs
temario, `findings.md`); el orquestador es una máquina de estados sin memoria, por
eso su contexto se mantiene sin ruido. Detalle en `agents/editora-jefa/HEARTBEAT.md`.

## Mapeo Paperclip ↔ Write.OnMars

| Paperclip | Write.OnMars |
|---|---|
| Company / Goal | la casa "Write.OnMars" / su misión permanente |
| Project / goal del Project | una guía / su brief |
| Agent + adapter | rol editorial permanente + modelo (cross-model nativo) |
| Bundle AGENTS/SOUL/HEARTBEAT | `writeonmars/AGENTS.md` + `references/voz` + estos bundles |
| Task board (backlog→…→done) | capítulos + pasadas; `in_review` = pasada de revisión |
| Comentarios de la tarea | `findings.md` |
| Workspace del Project (repo local o git) | el repo de la guía; worktrees para aislar capítulos en paralelo |
| Runtime job (sin agente) | `status.py` / `close.py` / `export.py` / `feedback_intake.py` |
| Strategy approval | checkpoint 1 (brief/temario) |
| Approval previa a close | checkpoint 2 (PDF anotado) |
| Budget company/agente | presupuesto por guía y por rol |

## Estado

Primer corte de la capa #3 del ROADMAP, montado y arrancado (2026-06-20).

- **Construido en el repo**: el reparto de roles, los bundles de instrucciones,
  `status.py --json` (la brújula del heartbeat), `tools/new-guide.sh` (scaffolding
  de una guía en un comando) y `hire-team.sh` (contratar el equipo por CLI).
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
