# Write.OnMars — Roadmap y estado

> Estado al **2026-07-09**. Resumen de lo construido, lo validado de verdad y lo
> que queda. Punto de retorno para no perder el hilo entre sesiones.

## En una frase

El método editorial es un **preset de Spec Kit agente-agnóstico** (`writeonmars/`),
instalable con `specify preset add` y **probado de punta a punta**. La voz, la
didáctica y el método viajan como **referencias** neutrales de modelo; la lógica,
como **comandos**; lo determinista, como **scripts**. La orquestación de
referencia ya es **Vivarium headless** (`vivarium/`): bootstrap, runner por
estados, BYOM, modos y contrato publicado. Paperclip queda archivado como
referencia histórica.

El pipeline de **modo estudio** ya está operativo en el preset: `status.py`
propone checkpoints humanos de escritura y disposición, `dispose.py` registra
decisiones auditables, `authorship.py` emite el informe de autoría humana y
Vivarium espera en `write`/`dispose`/`intro` sin despachar redacción.

## Cómo está montado (capas)

- **Método** — el preset `writeonmars/`, que corre *dentro* de un agente (Claude,
  Codex, Gemini…) vía comandos `speckit.*`.
- **Orquestación** — **desde 2026-07-07: Vivarium** (`vivarium/`, Rust+Tauri,
  backend primero) es el ejecutor orquestado de referencia; Paperclip queda
  **archivado** en `paperclip/` (su FLOW-CONTRACT §§ 0-2 es el contrato que
  Vivarium implementa). Lo que sigue describe ese primer corte, hoy histórico:
  el "ejecutor orquestado" concreto sobre Paperclip. UNA sola Company "Write.OnMars" (la casa, equipo
  permanente); cada guía = un **Project** de Paperclip (su goal, workspace y
  tablero); el workspace es el repo local (`sourceType=local_path`, sin GitHub).
  Roster de 4 roles por oficio: **Editora jefa** (orquestador / "CEO":
  constitution/specify/plan/intro/gates/close, decide leyendo `status.py --json`
  y delega, no escribe prosa, heartbeat event-driven), **Documentalista**
  (research + pasada de precisión, puede correr en Codex), **Redactora**
  (implement en paralelo + revise) y **Editora de mesa** (pasadas de estructura /
  utilidad / naturalidad / formato, con modelo distinto al de la Redactora).
  Preserva las reglas: escribe-uno-revisa-otro, voz ≠ precisión, detector ≠
  corrector.
- **Regla rectora**: un solo método, dos ejecutores — a mano (un agente) o
  orquestado (Paperclip lanza agentes/modelos por paso).

## Inventario del preset (`writeonmars/`)

- **6 plantillas** (modo dual editorial/software + `adendas-template` para la capa
  por guía de la constitución).
- **18 comandos**:
  - arranque: `setup` → `constitution` (adendas del proyecto: sector + tono +
    terminología + gobernanza, guiado con defaults por sector; `replaces` el core)
  - ciclo: `specify`, `research`, `plan`, `implement`, `intro` (specify/plan/implement
    **reemplazan** a los core; `intro` genera el README de presentación del PDF)
  - revisión: `review` (agrupado) + `review-structure` / `review-voice` /
    `review-precision` / `review-global` (sueltos, un modelo por pasada) + `revise`
    (aplica los hallazgos al texto y cierra el loop)
  - operación: `status`, `export`, `feedback`, `close`, `memory`
- **8 scripts deterministas**: `bootstrap`, `status`, `dispose`, `authorship`,
  `export`, `feedback_intake`, `close`, `index`. `status.py` ahora expone **`--json`** con el campo `next_step`
  (`setup` → `constitution` → `specify` → `research` → `plan` → `implement` →
  `review` → `revise` → `close`; en estudio también `write` y `dispose`): la
  **brújula del heartbeat** del orquestador. Tolera la ausencia de `specs/` y
  detecta `sector=null` → `constitution`.
- **`references/`**: voz (`marcela-prose`), didáctica (`technical-guide-design`),
  método (`writeonmars-*`), **sectores** (`sectores/<slug>.md`: defaults por dominio
  para las adendas; hoy `tecnologia`, ampliable con solo añadir un archivo).
  **`contracts/`**: citación, manifest, pass-output.
  **`memory/constitution.md`** (bundled).
- **`AGENTS.md`** (contrato agente-agnóstico) + **`docs/`** (Diátaxis: tutorial,
  how-to, referencia, arquitectura) + **`smoke-test.sh`**.

## Inventario de la raíz (orquestación + tooling)

- **`tools/new-guide.sh`**: scaffolding de una guía en **un comando** — crea el
  repo, corre `specify init --integration <agente> --here --force
  --ignore-agent-tools`, `specify preset add --dev`, `bootstrap.py`, los symlinks
  de contexto multi-agente y un commit que queda como **base ref**. Operador y
  email **heredan de git**. Idempotente; flags `--agents` / `--skip-init` /
  `--refresh-preset` / `--preset` / `--operator` / `--email`.
- **`paperclip/`** — la capa de orquestación sobre Paperclip:
  - `README.md`: el modelo (Company única / Project por guía / workspace =
    repo local), el flujo, el grafo de roles y el mapeo paso→rol.
  - `agents/<rol>/`: los bundles de los 4 roles (`editora-jefa`,
    `documentalista`, `redactora`, `editora-de-mesa`).
  - `hire-team.sh`: contrata por CLI los **3 ejecutores** (idempotente, con
    modelos cruzados entre Redactora y Editora de mesa).
- **Operación**: Paperclip se maneja con su CLI `paperclipai`. Heartbeat
  event-driven (`runtimeConfig.heartbeat.enabled:false` + `wakeOnDemand:true`);
  headless con `dangerouslySkipPermissions:true`. Para usar Codex con suscripción
  se siembra un `CODEX_HOME` aislado con symlink a `~/.codex/auth.json`.

## Validado de verdad

Prueba en un repo aparte (`guia-prueba`), tema *servidor MCP en Node/TS*:

- `specify preset add` instala el preset y **copia `references/`** ✓
- bootstrap (`speckit-setup`): constitución + manifest ✓
- `/speckit-specify` → brief de 9 campos firmado, **en la voz de Marcela** ✓
- `/speckit-research` → 9/9 conceptos citados con fuente oficial; marcó un dato
  volátil; lo **verificamos y corregimos** (`@modelcontextprotocol/sdk`) ✓
- `/speckit-plan` → temario de 10 capítulos + descripciones encadenadas ✓
- `/speckit-implement` → capítulo 1 con voz y estructura de 9 secciones ✓
- **Cross-model**: Codex corrió la pasada de precisión, leyó todo el contexto (son
  archivos), **cazó un bug de numeración** (corregido) y **no fingió firma humana**.
  Confirma "escribe uno, revisa otro" y la neutralidad de modelo ✓

Y, ya en Paperclip:

- Se **montó la Company "Write.OnMars"**, un **Project** por guía y el **equipo de
  ejecutores** (`hire-team.sh`), y se **arrancó el flujo** con `guide-nlp` ✓

## Decisiones de arquitectura tomadas

- Un método, dos ejecutores (directo / Paperclip).
- Agente-agnóstico: lógica en comandos + referencias, no en skills de un proveedor.
- Revisión = 3 pasadas locales + 1 global; voz y precisión **separadas**;
  **quien escribe no se revisa** (writer ≠ reviewer).
- Firmas: **por defecto todas las pasadas son autónomas**. El control humano son los
  dos checkpoints (brief + **PDF anotado** del documento terminado), no pasada por
  pasada. Guardarraíl que se mantiene: un hallazgo `critico` abierto (p. ej. dato
  sin fuente de precisión) **siempre** bloquea el cierre.
- Pasadas como comandos sueltos (un modelo por pasada) + `review` agrupado.
- Comandos editoriales **reemplazan** (`replaces`) a los core → sin ambigüedad.
- Sin `wom` CLI (lo cubren `status.py` / `close.py`); spec `002-wom-cli` superseded.
- `speckit-setup` para lo que el preset no puede instalar (constitución, manifest).
- Constitución **v1.6.1** (Principio V 3+1; Principio VI neutralidad de modelo;
  desde v1.6.0: modos de proyecto `produccion`/`estudio` y § Ejecutores del
  método — Vivarium reemplaza a Paperclip como ejecutor orquestado).

## Pendiente (orden sugerido)

1. **Interfaz Tauri de Vivarium**: envolver `vivarium-core` sin duplicar lógica
   editorial, empezando por nuevo proyecto, estado y ejecución supervisada.
2. **Registrar los comandos para Codex/Gemini nativamente** (hoy se les apunta al
   archivo del comando; funciona, pero registrarlos evita pegar la ruta).
3. **Opcionales del preset**: búsqueda semántica real en `index.py` (embeddings,
   chromadb); hook `after_close` para auto-export.
4. **Checkpoint 2 en producto**: cerrar el lazo del segundo control humano — el
   **PDF anotado** del documento terminado debe entrar por `feedback_intake`
   (hoy ese paso es manual).
5. **Presupuestos**: topes de gasto/tokens por Project y por rol.
6. **Varias guías en paralelo**: hoy se corre **una guía a la vez**; falta operar
   varios proyectos a la vez.
7. **Distribución**: publicar el preset (`specify preset add --from <github>`)
   y versionar releases. (Licencia elegida: Apache-2.0, 2026-07-09.)
8. **Inspiración externa** (análisis 2026-07-08, ver
   `docs/comparativa-bookwright-sloop.md` y diseños de adopción en
   `docs/inspiracion-bookwright-profundizada.md` — candidata a spec 006:
   biblia narrativa en roots/ + ejes de continuidad): firma de fallo repetida como
   clasificador transitorio/determinista en el runner de Vivarium (S|Loop);
   late binding de prompts de capítulo contra estado real + decisions.jsonl
   (S|Loop); protocolo `[PENDING]` de tres sistemas para adendas/claims
   (Bookwright); hallazgo-vs-ancla con umbral de fiabilidad para el índice de
   factualidad (Bookwright); plantillas de fichas narrativas en `roots/` con
   "diálogo de muestra" para el modo estudio con novela (Bookwright).

## Bugs de orquestación — primera corrida real (guide-nlp, 2026-06-20)

> **Direccionado por el rediseño del flujo (2026-06-21).** Estos cuatro bugs son
> síntomas de un mismo defecto de raíz: el modelo viejo creaba **una tarea por
> estado/pasada** (`review:1-2-3`, `revise:cap-N` como tareas separadas que el
> orquestador re-despachaba en cada heartbeat), así que el orquestador tenía que
> loopear y reconciliar, y perdía el hilo del capítulo. El rediseño ataca la causa:
> **una tarea por capítulo que se mueve por estados** (fan-out único de la jefa tras
> plan+research; ciclo peer-to-peer Redactora→Mesa→Doc→Redactora dentro de la misma
> tarea; globales disparadas por el wake de la última hija `done`), más
> `status.py --json` con `by_chapter`/`all_chapters_approved`, los bundles de los 4
> roles reescritos y `maxConcurrentRuns:1` en la jefa para idempotencia
> **estructural** (no instruccional). Con ello: no hay re-despacho que duplicar (#2),
> no hay tarea-contenedor que vigilar (#3), el revise es una transición de estado de
> la propia hija y no un barrido (#1, #4a), y la jefa no necesita loopear ociosa
> porque solo despierta para las globales (#4b). El historial de abajo se conserva
> como evidencia de la corrida que motivó el rediseño. Spec del flujo nuevo:
> [`paperclip/FLOW-CONTRACT.md`](paperclip/FLOW-CONTRACT.md).

Detectados al correr el flujo de verdad con Paperclip. Misma familia: el orquestador
lee `next_step` pero **no reconcilia contra el estado real** (hallazgos no críticos /
tareas en vuelo).

**Estado del fix (2026-06-20)** — implementado y verificado:
- **#1 (gate de revise)**: ✅ arreglado en `status.py` (preset + guide-nlp). Política
  **crítico+medio fuerzan revise; bajo = aviso**. Nuevos campos `--json`:
  `revise_pending`, `revise_by_chapter`, `advisory_open_bajo`. El `revise` enumera
  capítulos (barrido).
- **#2 (idempotencia) / #3 (contenedor sin disposición) / #4a (revise por capítulo)**:
  ✅ vía reglas nuevas en `paperclip/agents/editora-jefa/HEARTBEAT.md` (recargado en
  la jefa en vivo): comprobar tarea existente antes de crear, no crear contenedores
  que vigila, y barrido `revise:cap-N` por capítulo a medida que cada uno queda
  revisado. (Mitigación a nivel instrucción; no hay enforcement duro en código.)
- **#4b (anti-parada)**: ❌ el heartbeat periódico **NO sirve**. Verificado en vivo
  (2026-06-20): con `heartbeat.enabled:true`, el wake por timer corre en un
  **workspace de fallback** (`.../workspaces/<agentId>`), NO en el repo del Project
  → la jefa no puede leer `status.py` de guide-nlp, mira su inbox (vacío) y concluye
  "no hay trabajo". Revertido a `enabled:false`. **Causa real**: Paperclip es
  *issue-driven* — el workspace con `cwd=<repo de la guía>` solo se monta cuando el
  agente trabaja **un issue del Project** (`sourceIssueId`). *Fix correcto (dos
  opciones)*: (1) **routine scoped al Project** (event-driven sobre
  `issue_children_completed` de la revisión de cada capítulo → crea `revise:cap-N`
  directamente, sin depender de que la jefa loopee); o (2) un **issue de
  orquestación** asignado a la jefa en el Project que la despierta EN el workspace de
  la guía, donde corre `status.py` y despacha. La (1) es la durable; requiere el
  schema real del payload de routines (vía `paperclipai openapi`, no inventar).
- **Verificación en vivo (2026-06-20)**: la opción (2) —issue de orquestación
  asignado a la jefa (WRI-44)— **funcionó**: la despertó en el workspace de la guía,
  corrió `status.py`, despachó `revise:cap-1..7` + `revise:global` a la Redactora
  (política crítico+medio) y **cerró el contenedor WRI-44** (fix #3 ✅). PERO **se
  duplicó**: dos heartbeats casi concurrentes (auto-wake al asignar + un
  `heartbeat:invoke` manual de más, 47 s después) crearon DOS barridos (16 tareas).
  La idempotencia a nivel **instrucción NO sobrevive a runs concurrentes** (race
  check-then-create). Batch 2 cancelado a mano. **Lecciones**: (i) no invocar
  heartbeat a mano si asignar el issue ya despierta al agente (`wakeOnDemand`); (ii)
  la idempotencia debe ser **estructural**: `maxConcurrentRuns:1` en el orquestador, o
  dedup nativo por `originFingerprint` (create-if-not-exists), o single-flight. Esto
  refuerza por qué la routine event-driven (1) es lo correcto.

1. **El `revise` no se dispara salvo con críticos.** `status.py::_next_step` solo
   devuelve `revise` cuando `crit_open > 0`; los hallazgos `medio`/`mayor` abiertos
   (p. ej. F-4.1/F-4.2 del cap. 1 de guide-nlp) se detectan, se anotan en
   `findings.md` y **quedan huérfanos** — nadie los aplica. Contradice la
   `HEARTBEAT.md` de la Editora jefa (línea 28: "por cada capítulo con hallazgos
   abiertos → revise"). Rompe *detector ≠ corrector* para todo lo no-crítico, y una
   guía podría llegar a `close` con hallazgos reales sin aplicar.
   *Fix parcial ✅ (2026-06-20)*: `status.py::_next_step` ya devuelve `revise` con
   **cualquier** hallazgo abierto y **enumera los capítulos** afectados (barrido, no
   one-off); expone `open_by_chapter` en `--json`. Aplicado al preset y a guide-nlp.
   Severidad real en guide-nlp: **8 críticos + 73 medios + 39 bajos** abiertos →
   pendiente decidir si `bajo` fuerza revise o queda como aviso (hoy fuerza). **Pero
   esto es solo la red de seguridad global**: el disparo correcto es por capítulo
   tras su revisión (ver bug #4). `status.py` evita que `close` ocurra con hallazgos
   abiertos; no sustituye al encadenado por evento.
2. **Despacho no idempotente → tareas solapadas.** Cada heartbeat que ve
   `implement` re-crea la tanda completa sin comprobar si ya hay tareas `implement`
   abiertas para esos capítulos. En guide-nlp se crearon **3 tandas de redacción en
   3 min** (17:15/17:17/17:18): cap. 1 despachado 3× (WRI-5/9/16), caps 2-7 2× cada
   uno → duplicación que WRI-25/26 tuvieron que consolidar. Además se despachó
   `review`/`precisión` del cap. 1 (WRI-6/7) **a la vez** que su redacción, antes de
   que el capítulo existiera.
   *Fix*: reconciliación previa al despacho (¿ya hay tarea abierta para este
   paso+capítulo?) en la lógica del heartbeat de la Editora jefa; opcionalmente un
   helper en `status.py` que liste pasos ya en vuelo para que el orquestador no los
   duplique.
3. **Las tareas-contenedor de despacho se quedan sin disposición → bucle.** La
   Editora jefa crea una tarea de despacho (p. ej. WRI-29 "Despachar revisión por
   capítulo") asignada a sí misma, crea los hijos, y al terminar **no le da una
   disposición válida de Paperclip**: la deja `in_progress` sin blocker. El harness
   la marca `blocked` ("MISSING DISPOSITION"), no puede auto-recuperarla ("recovery
   blocked on a recovery owner"), y la jefa la devuelve a `in_progress` → ping-pong
   que **quema heartbeats/coste** sin producir nada. En guide-nlp se resolvió a mano
   cerrando WRI-29 (`issue update --status done`): no cascadeó (los 14 hijos
   sobrevivieron, la pasada 5 WRI-42 se desbloqueó sola) y destapó el `next_step`
   real (`revise`). *Fix*: enseñar a la Editora jefa (bundle/HEARTBEAT) a **marcar
   `done` la tarea-contenedor en cuanto crea los hijos** —el despacho es el
   entregable—, en vez de vigilarla. Los hijos llevan su propio cierre; la barrera
   (pasada 5) es un hijo bloqueado por hermanos, no por el padre.
4. **El orquestador se queda PARADO con trabajo abierto; el revise no ocurre tras
   cada revisión.** El heartbeat de la Editora jefa es *event-driven puro*
   (`heartbeat.enabled:false` + `wakeOnDemand:true`): cuando acaba y no le queda
   ninguna tarea abierta asignada, **se duerme y no vuelve a evaluar** —aunque
   `status.py` diga `revise`—. En guide-nlp despachó todas las revisiones pero solo
   **un** revise (cap. 3) y se quedó ociosa con 120 hallazgos abiertos; hubo que
   despertarla a mano. Causa de fondo: **el revise no está encadenado por evento a
   la revisión** de cada capítulo. *Fix (dos partes)*:
   - **(a) Revise por capítulo, dirigido por evento** — en cuanto las pasadas 1-4 de
     un capítulo quedan `done` y tiene hallazgos abiertos, crear `revise:cap-N` **de
     inmediato** (rutina de Paperclip sobre `issue_children_completed` del subárbol
     del capítulo, o regla en la `HEARTBEAT` de la jefa que en cada wake barra los
     capítulos con revisión completa + hallazgos abiertos + sin revise). Así el
     revise ocurre *tras cada revisión*, no como barrido final.
   - **(b) Anti-parada (watchdog)** — que la jefa se re-evalúe mientras
     `next_step ≠ close`: heartbeat **periódico** (o un monitor del Project) además
     de `wakeOnDemand`, para que un evento perdido no congele el flujo. El
     `next_step` de `status.py` es la condición de parada natural del watchdog.

## Feature 003 (atribución por afirmación + factualidad) — e2e validado (2026-06-21)

Rama `003-atribucion-factualidad` (spec de claude cowork, revisada e implementada por
fases) **probada end-to-end** en una guía fresca orquestada (`usar-biome`, "cómo usar
Biome"). El pipeline completo corrió solo: constitution → brief+checkpoint 1 → research
(22 citas, 24 volátiles) → temario (3 caps) → fan-out (1 hija/cap, sin duplicados) →
ciclo por capítulo con `claims.md`/factualidad → pasada 5 global → revise global →
export PDF. **La feature cazó deuda factual real de Biome** (config `quickfix.biome`
inexistente, comandos `migrate` sin fuente, narración de `diff`/semicolons contradicha
por `@biomejs/biome@2.5.0`) y el ciclo la corrigió. Factualidad final 1.0; export D1-A
sin avisos. Confirma SC-001/SC-004 (0 tipos/estados/routines nuevos de Paperclip).

- **Bug encontrado y ARREGLADO en caliente**: con una tarea por capítulo, la pasada 4
  **reescribía `claims.md` entero** con su capítulo y borraba los demás (cap1 perdido al
  medir cap2). `findings.md` se acumulaba bien (append) pero `claims.md` no. *Fix
  (commit en la rama)*: bundle Documentalista + skill `writeonmars-contraste` exigen
  **leer y FUSIONAR** (`reemplaza solo "## Claims — Capítulo N", conserva las demás`),
  espejo del append de findings. Validado: los 3 capítulos conviven tras el fix.
- **Pendiente menor #1 — refresco de claims tras revise**: ✅ arreglado (instrucción,
  bundle Documentalista). La Doc re-ejecuta la pasada 4 sobre el texto **actual** cada
  vez que recibe el capítulo (incluido tras un revise) y **no aprueba con un `claims.md`
  desfasado**; así la factualidad no queda pesimista por un `contradicho`/`parcial` ya
  corregido. (Antes se autocorregía solo en el pase global.)
- **Pendiente menor #2 — `status.py` va por delante del tablero**: ✅ arreglado
  (instrucción, HEARTBEAT jefa §5). `all_chapters_approved`/`closeable` se calculan desde
  los archivos y pueden adelantar al tablero; la jefa ahora **no cierra mientras alguna
  hija de capítulo no esté `done`**, aunque `status.py` diga que sí. `status.py` (capa
  agnóstica) se mantiene sin cambios; el guardarraíl vive en el orquestador.

## Deuda y cosas honestas a saber

- **Docs**: `writeonmars/docs/` es la fuente canónica de uso. En `docs/` conviven
  dos familias (índice en `docs/README.md`): los docs de producto de **Vivarium**
  (`docs/vivarium.md` es su fuente de verdad) y lo transversal del framework;
  `docs/citation-contract.md` y `docs/manifest-schema.md` son punteros a
  `writeonmars/contracts/` (fuente única de contratos desde 2026-07-04).
- **Invocación**: para Claude los comandos se registran como skills **con guion**
  (`/speckit-specify`), aunque el nombre canónico lleva **punto** (`speckit.specify`).
  Los docs mezclan ambas formas; pendiente de unificar.
- **Sincronía de voz**: `references/voz/` es copia de `mars-voice`. Si actualizas la
  voz allí, re-sincroniza (`cp`) la del preset. Las copias en `.claude/skills/` y
  `.agents/skills/` se retiraron (2026-07-09, habían divergido): la fuente única
  en el repo es `writeonmars/references/`.
- **CI**: desde 2026-07-09 los gates corren en GitHub Actions
  (`.github/workflows/ci.yml`): pytest, `cargo test` y smokes con stubs en cada
  push. En local siguen siendo obligatorios antes de commitear (CLAUDE.md).
- **`guia-prueba`**: su `findings.md` quedó con numeración mezclada de pruebas
  previas; se limpia al re-correr `review` con el preset corregido.
- **`install.sh`**: retirado del árbol (2026-07-09; vive en la historia de git). La vía canónica es el preset.

## Cómo retomar (mínimo)

```bash
# 1. una guía nueva es un repo aparte
mkdir mi-guia && cd mi-guia && git init
# 2. instalar el método
specify preset add --dev ~/Projects/writing-framework/writeonmars
# 3. bootstrap (núcleo de la constitución + manifest)  →  /speckit-setup  (o:)
python3 .specify/presets/writeonmars/scripts/bootstrap.py
# 4. ciclo (en el agente):
#   /speckit-constitution (sector + tono + terminología; guiado, con defaults)
#   /speckit-specify "tema" → /speckit-research → /speckit-plan
#   /speckit-implement N → /speckit-review N (idealmente otro modelo)
#   /speckit-revise N (aplica los hallazgos) → /speckit-intro
#   /speckit-status → /speckit-export
#   (anotas el PDF) /speckit-feedback → /speckit-close
```

Guía paso a paso: [`writeonmars/docs/tutorial-primera-guia.md`](writeonmars/docs/tutorial-primera-guia.md).
