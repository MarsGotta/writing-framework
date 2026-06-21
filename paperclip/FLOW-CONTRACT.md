# Contrato de diseño — flujo por capítulo (Write.OnMars)

> Fuente de verdad para reescribir el flujo. Todos los subagentes de implementación
> consumen ESTE documento para salir coherentes. Verificado contra el CLI
> `paperclipai` + su OpenAPI (2026-06-21); lo marcado "no verificado" se prueba en
> implementación.

## 0. Principio rector — agnóstico

El método funciona **sin Paperclip**. La verdad del estado vive en **archivos**:
`chapters/NN-*.md`, `specs/<id>/findings.md`, `plan.md` (temario),
`.writeonmars-manifest.json`. `status.py` computa el estado; cualquier runner (un
solo agente, otro orquestador) sigue el mismo `status.py` + comandos.

Paperclip es una **capa de orquestación opcional** que MAPEA este ciclo a tareas. Si
se quita, **nada del método se pierde**. Por tanto: ninguna lógica de negocio (qué
revisar, qué corregir, cuándo está aprobado) vive solo en Paperclip — vive en el
método; Paperclip solo orquesta relevos.

Reglas duras del método que se preservan: **escribe-uno-revisa-otro** (Redactora ≠
revisores), **voz ≠ precisión** (Mesa vs Documentalista), **detector ≠ corrector**
(el revisor anota en `findings.md`; la Redactora corrige).

## 1. Ciclo de vida de UN capítulo (agnóstico)

Estados conceptuales (derivables de archivos):
- **DRAFTING** — no existe `chapters/NN-*.md` → la Redactora escribe.
- **IN_REVIEW** — capítulo escrito, pendiente de pasadas → Mesa (1·2·3), luego Doc (4).
- **NEEDS_REVISE** — `findings.md` tiene ≥1 accionable (crítico+medio) abierto para
  ese capítulo → la Redactora aplica.
- **APPROVED** — el capítulo ha pasado por Mesa **y** Doc sin accionables abiertos.

Bucle: `DRAFTING → IN_REVIEW → (si accionables) NEEDS_REVISE → IN_REVIEW → … → APPROVED`.

`findings.md` (esquema pass-output v1.0) es el **registro durable** (citación + gate).
Severidad: **crítico + medio fuerzan revise; bajo = aviso** (no bloquea).

## 2. Etapas globales (agnóstico)

Cuando **todos** los capítulos del temario están APPROVED:
1. **Pasada 5 global** (Mesa) — coherencia/formato; puede abrir accionables globales
   (p. ej. glosario) → vuelven al ciclo del capítulo afectado o a un revise global.
2. **Export PDF** (jefa) — `speckit.intro` + `export.py`.
3. **Checkpoint humano** (PDF anotado) — el **único revisor humano**.
4. **Feedback** → revise quirúrgico → **close**.

`status.py --gate` sigue siendo el guardarraíl de cierre (críticos abiertos + firmas
+ completitud del temario).

## 3. Mapeo a Paperclip (capa opcional)

### 3.1 Estructura de tareas
- **1 tarea PADRE** por guía (el libro), asignada a la jefa.
- **1 tarea HIJA por capítulo** (sub-task del padre), creada por la jefa **tras
  `plan` + `research` OK**. Es el **fan-out ÚNICO**.
- **NUNCA** una tarea por pasada/estado. Una hija = el capítulo entero moviéndose por
  estados. (Esto corrige el bug de "una tarea por estado → se pierde el hilo".)

### 3.2 Mapa estado-conceptual → `status` + `assigneeAgentId`
| Transición | status | assignee | quién la ejecuta |
|---|---|---|---|
| Arranque hija | `in_progress` | Redactora | jefa (al crear) |
| Redactora termina de escribir | `in_review` | Mesa | Redactora |
| Mesa termina pasadas 1·2·3 (→ `findings.md` + comentario-puntero) | `in_review` | Documentalista | Mesa |
| Doc termina pasada 4 → **DECIDE** | ver abajo | — | Documentalista |
| → si ≥1 accionable abierto (Mesa o Doc) en el capítulo | `in_progress` | Redactora | Documentalista (comenta "revise: ver findings.md") |
| → si 0 accionables | `done` (APPROVED) | — | Documentalista; si es la última hija done → **despierta a la jefa** |
| Redactora aplica revise | `in_review` | Mesa | Redactora (nueva ronda) |

### 3.3 Idempotencia / concurrencia (estructural, no instruccional)
- `maxConcurrentRuns=1` en la jefa (ya aplicado).
- Antes de crear o transicionar, cada agente **lee el estado actual** de la tarea; si
  ya está en el estado destino o ya hay otra acción en curso, **no duplica**.
- El fan-out (crear hijas) lo hace **solo la jefa, una vez**; comprueba si ya existen
  hijas del padre antes de crear.

### 3.4 Wake / eventos
- Reasignar una tarea **despierta al nuevo asignado** (verificado empíricamente:
  asignar WRI-44 despertó a la jefa sola, vía `wakeOnDemand`). Si no fuera fiable, el
  que reasigna hace `agent wake <nuevoAsignado>` explícito.
- **"Todas las hijas done → jefa"**: el agente que marca la **última** hija `done`
  hace `agent wake <jefa>` (push). Alternativa a verificar: blocker del padre sobre
  las hijas (`issue_children_completed`).
- **Ningún heartbeat por timer** (`enabled:false` en los 4 agentes; ya verificado).

### 3.5 Etapas globales en Paperclip
La jefa, al despertar por "todas done", corre `status.py` y según el `next_step`
global: crea tarea **pasada-5** (Mesa) → al `done`, tarea **export-PDF** (jefa) → al
`done`, **`approval` de board** (checkpoint humano del PDF) → al resolverse,
**revise/close**.

### 3.6 `findings.md` vs comentarios
- `findings.md` = **fuente de verdad** (agnóstico). Los revisores escriben ahí.
- El **comentario de la tarea** = puntero corto ("revise: ver `findings.md`, cap-N,
  F-x/F-y"). **No duplica** el contenido. Si se quita Paperclip, `findings.md` basta.

### 3.7 Contrato de salida de `status.py --json` (nombres EXACTOS, no inventar)
Campos NUEVOS que añade el núcleo (además de los actuales: `next_step`,
`next_detail`, `chapters`, `chapters_written`, `chapters_expected`, `passes`,
`criticals_open`, `open_findings_total`, `revise_pending`, `revise_by_chapter`,
`advisory_open_bajo`, `sign_violations`, `gates`, `closeable`, `has_manifest`):

- `by_chapter`: objeto keyado por **ordinal del temario en string** (`"1"`..`"N"`, y
  `"global"` si hay hallazgos globales). Valor:
  `{ "drafted": bool, "passes_done": [int], "revise_pending": int, "advisory": int, "approved": bool }`.
  - `drafted` = existe `chapters/NN-*.md` para ese ordinal.
  - `passes_done` = pasadas (1·2·3·4) que cubren ese capítulo según los bloques de
    `findings.md` ("Capítulos cubiertos").
  - `revise_pending` = accionables (crítico+medio) abiertos de ese capítulo.
  - `advisory` = abiertos 'bajo' de ese capítulo.
  - `approved` = `drafted AND {1,2,3,4} ⊆ passes_done AND revise_pending == 0`.
- `all_chapters_approved`: bool = todos los capítulos del temario tienen
  `approved == true`. **Es la señal que la jefa usa para disparar las etapas globales.**

Estos campos hacen el ciclo por capítulo seguible por un solo agente (agnóstico) y dan
a la jefa la condición global. Los workers de Paperclip se guían por el `status` de su
tarea + `findings.md`; no necesitan `by_chapter`.

## 4. Qué NO usar (verificado contra OpenAPI/CLI)
- **NO** los campos "Reviewers"/"Approvers" de la UI para agentes: no existen en la
  API; el subsistema `approval`/`work-product` es para el **board humano**. Reservar
  `approval` de board **solo** para el checkpoint humano del PDF.
- **NO** routines para etapas globales: sus triggers son solo `cron`/`webhook`/`api`,
  **sin** trigger por evento de dominio. Usar el wake de la jefa.
- **NO** heartbeat por timer.

## 5. Estados Paperclip válidos (enum real)
`backlog, todo, in_progress, in_review, done, blocked, cancelled`.

## 6. Reparto de la implementación (un subagente por pieza, este contrato compartido)
1. **`status.py` (núcleo agnóstico)** — exponer por capítulo el estado del ciclo
   (`pass_coverage` 1-4, `revise_pending`, `approved`) para que un solo agente lo
   siga; mantener el gate global. Define los campos `--json` nuevos.
2. **bundle Jefa** — fan-out único (padre + 1 hija/capítulo) + avance de etapas
   globales por evento.
3. **bundle Redactora** — DRAFTING + NEEDS_REVISE; al terminar → `in_review` + Mesa.
4. **bundle Editora de mesa** — pasadas 1·2·3 + `findings.md` + relevo a Doc.
5. **bundle Documentalista** — pasada 4 + decisión APPROVED/NEEDS_REVISE + wake jefa
   en la última; (research sin cambios).
6. **docs + ROADMAP** — flujo nuevo + separación núcleo/Paperclip.

Regla para todos: **no inventar APIs de Paperclip** — usar solo lo de §4/§5.
