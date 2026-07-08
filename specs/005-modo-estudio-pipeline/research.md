# Research — Pipeline del modo estudio (005)

Decisiones de diseño que la spec difirió al plan. Cada una fija un contrato
que la implementación (Codex) debe respetar tal cual; las alternativas
descartadas quedan documentadas para no relitigarlas.

## R1 — Semántica de `next_step` en modo estudio

**Decision**: `status.py` gana dos valores nuevos de `next_step`, ambos
checkpoints humanos no-despachables:

- `write` — hay capítulos del temario sin escribir. Sustituye a `implement`
  cuando `mode: estudio`. `next_detail` enumera los ordinales pendientes.
- `dispose` — hay hallazgos accionables (crítico/medio) abiertos. Sustituye a
  `revise` cuando `mode: estudio`. `next_detail` enumera los hallazgos por id.

El resto de pasos no cambia de nombre ni de semántica: `setup`,
`constitution`, `specify`, `research`, `plan`, `review`, `close` son idénticos
en ambos modos (las pasadas de revisión son despachables también en estudio:
producen hallazgos, no prosa). La salida `--json` gana el campo `"mode"`
(`"produccion"` | `"estudio"`, derivado del manifiesto con ausencia =
`produccion`).

**Rationale**: reutiliza el mecanismo existente de checkpoint (el ejecutor ya
trata `specify` como Checkpoint, exit 10); dos nombres nuevos son el cambio
mínimo que hace el estado despachable-vs-humano decidible por máquina sin
parsear `next_detail`.

**Alternatives considered**: (a) mantener `implement`/`revise` y añadir un
flag `dispatchable: false` — descartado: todo consumidor existente que haga
match por nombre despacharía igualmente; el nombre nuevo rompe en seguro.
(b) Un solo paso genérico `human` — descartado: pierde qué acción concreta
se espera y complica los mensajes del ejecutor.

## R2 — Registro de disposiciones humanas

**Decision**: nuevo script determinista `writeonmars/scripts/dispose.py` (sin
LLM), único escritor autorizado de transiciones de estado de hallazgos en modo
estudio. Uso:

```bash
python3 scripts/dispose.py F-1.2 --aceptar [--nota "..."]
python3 scripts/dispose.py F-1.3 --rechazar --motivo "..."   # motivo obligatorio
python3 scripts/dispose.py F-2.1 --aplazar [--nota "..."]
```

Efectos (ambos o ninguno):
1. Actualiza la columna `estado` del hallazgo en `specs/<feature>/findings.md`:
   `--aceptar` → `resuelto` (la humana ya aplicó su corrección al capítulo
   antes de disponer); `--rechazar` → `desviacion_justificada` (el motivo va a
   `decision_humana`); `--aplazar` → `aplazado` (estado nuevo, v1.2).
2. Añade una línea a `specs/<feature>/disposiciones.jsonl` (append-only) con
   el DispositionRecord v1: `{v, ts, finding_id, disposicion, actor, motivo?,
   nota?}`. `actor` se resuelve de `git config user.name` (obligatorio: sin
   identidad git el script falla con exit 3).

`status.py` en modo estudio cuenta como `revise_pending` los hallazgos
crítico/medio con `estado = abierto`; cualquier estado no-abierto sin línea
correspondiente en `disposiciones.jsonl` genera un warning de inconsistencia
(un agente editó findings.md a mano) y el hallazgo se sigue contando como
pendiente — el atajo no avanza el estado (SC-005).

**Rationale**: findings.md sigue siendo la vista única de hallazgos (no se
duplica la tabla); el JSONL da el registro auditable con actor y fecha,
paralelo a `decisions.jsonl` del ejecutor; y el cruce tabla↔registro convierte
la prohibición constitucional ("ningún agente resuelve hallazgos") en un
invariante verificable, no una súplica en un prompt.

**Alternatives considered**: (a) editar findings.md a mano sin script —
descartado: sin registro de actor/fecha no hay auditabilidad ni forma de
detectar el atajo de un agente. (b) Archivo de disposiciones separado como
única fuente (findings.md intacto) — descartado: dos fuentes de verdad para
el estado de un hallazgo; todos los parsers existentes leen findings.md.

## R3 — Estado `aplazado` (pass-output-schema v1.2)

**Decision**: el enum `estado` del Finding gana `aplazado`, válido solo cuando
el proyecto está en modo estudio. Un hallazgo `aplazado`: no cuenta en
`revise_pending`, no bloquea `close` (sea cual sea su severidad — la decisión
es humana y queda firmada), y aparece en el resumen de cierre como deuda
declarada (`close.py` lo lista). La transición documentada:

```text
abierto ──dispose --aceptar──→ resuelto
abierto ──dispose --rechazar──→ desviacion_justificada
abierto ──dispose --aplazar──→ aplazado
aplazado ──dispose --aceptar/--rechazar──→ resuelto / desviacion_justificada
```

**Rationale**: la spec exige que lo aplazado no desaparezca en silencio
(FR-007); un estado explícito en el esquema es más honesto que reinterpretar
`desviacion_justificada` (que significa "decidí no resolverlo", no "lo veré
después").

**Alternatives considered**: reutilizar `desviacion_justificada` con una
nota — descartado: pierde la distinción semántica y el resumen de cierre no
podría separar deuda de desviación firmada.

## R4 — "Cambio sustancial" de un capítulo aprobado (huella de contenido)

**Decision**: cada bloque de pasada en findings.md registra la huella del
contenido revisado como comentario de máquina al final del bloque:

```html
<!-- huellas: {"1": "<sha256-hex del archivo chapters/001-*.md>", "2": "..."} -->
```

La huella es `sha256` de los bytes del archivo del capítulo en el momento de
la pasada (sin normalización: cualquier byte distinto = contenido distinto).
En modo estudio, `status.py` considera válida una pasada N para el capítulo C
solo si la huella registrada coincide con la huella actual del archivo; si no
coincide, esa pasada deja de contar en `passes_done` para C (el capítulo se
"reabre" y `next_step` vuelve a `review`). El dashboard lo explica
(`"capítulo 2 cambió tras la pasada 3: pasadas 3-4 invalidadas"`). En modo
produccion la huella se escribe igualmente (los comandos la emiten siempre)
pero **no** se verifica — retrocompatibilidad total (FR-011).

**Rationale**: determinista, barato (un hash por capítulo por pasada), sin
estado nuevo fuera de findings.md, y ancla la aprobación al contenido revisado
como pide FR-008. Escribirla en ambos modos deja el terreno preparado para
extender la verificación a produccion en una feature futura sin migración.

**Alternatives considered**: (a) mtime del archivo — descartado: frágil
(cualquier checkout lo cambia). (b) Umbral de diff "sustancial" (n líneas) —
descartado: introduce un juicio arbitrario; si la humana corrigió una tilde
tras la pasada, re-pasar es barato y honesto. (c) Guardar huellas en un
archivo aparte — descartado: findings.md ya es el registro por pasada.

## R5 — Informe de autoría humana

**Decision**: nuevo script determinista `writeonmars/scripts/authorship.py`
(sin LLM) que genera `specs/<feature>/authorship-report.md` (+ `--json` a
stdout). Fuentes: historial git del proyecto (`git log --numstat --follow`
sobre `chapters/`) y `decisions.jsonl`. Clasificación por commit que toca
`chapters/`:

- **agente**: el email del autor del commit aparece en la convención de
  identidad de agentes (`*@agents.writeonmars.invalid`, ver abajo) **o** el
  commit está dentro de una ventana dispatch→disposition de un paso que
  escribe manuscrito (`implement`/`revise`/`intro`) registrada en
  `decisions.jsonl` con el mismo capítulo.
- **humano**: cualquier otro autor.

Convención de identidad (se publica en el contrato del ejecutor): cuando un
ejecutor orquestado comitea trabajo de un agente, MUST usar
`<rol>@agents.writeonmars.invalid` como email de autor. Los proyectos donde
los agentes no comitean (el caso actual: el ejecutor no comitea por paso)
quedan cubiertos por la ventana dispatch→disposition.

Veredicto por capítulo: `humana` (0 cambios de agente), `mixta` (hay ambos) o
`ia` (0 cambios humanos). Veredicto global: `autoría humana demostrada` solo
si todos los capítulos son `humana`. Reproducibilidad: la salida se deriva
exclusivamente de git + JSONL (sin timestamps de generación; el informe
declara el commit HEAD sobre el que se calculó).

**Rationale**: git es la única evidencia que un tercero puede auditar; el
cruce con decisions.jsonl cubre el hueco (agentes que comitean con la
identidad del operador o trabajo sin commit por paso) y hace el informe
honesto en proyectos convertidos (FR-009, escenario 2 de US3).

**Alternatives considered**: (a) solo autor git — descartado: un ejecutor que
comitea todo con la identidad de la operadora haría pasar prosa de IA por
humana. (b) Análisis estilométrico del texto — descartado: no determinista,
no auditable, fuera del espíritu del método (la evidencia es procedencia, no
adivinación).

## R6 — Integración con Vivarium (mapeo, sin tocar el guardarraíl)

**Decision**: `vivarium-core` mapea los estados nuevos sin cambiar
`writes_manuscript` ni el exit 11:

- `next_step = "write"` → `Planned::Checkpoint{step: "write"}` → exit 10 con
  mensaje "checkpoint humano: faltan capítulos por escribir (modo estudio)".
- `next_step = "dispose"` → `Planned::Checkpoint{step: "dispose"}` → exit 10
  con "checkpoint humano: hallazgos a la espera de disposición (dispose.py)".
- En `plan_global` (etapa de cierre), si `mode = estudio` y falta `README.md`,
  el paso `intro` se planifica como **Checkpoint** (la presentación es prosa
  del manuscrito publicado: la escribe la humana), no como despacho a la
  Redactora. `export` y `close` siguen siendo sidecar en ambos modos.
- `vivarium status` expone el `mode` que ya lee del manifiesto y los nuevos
  checkpoints en `--json`.

El guardarraíl `blocked_by_mode`/exit 11 queda como red de seguridad para
estados imposibles (p. ej. un `status.py` antiguo que devuelva `implement` en
un proyecto estudio), exactamente su papel actual.

**Rationale**: la frontera dura se mantiene — la lógica editorial (qué toca)
vive en el preset; el ejecutor solo traduce pasos a despachos o esperas. El
exit 10 ya significa "esperar al humano no es un error" (executor-contract).

**Alternatives considered**: tratar `write`/`dispose` como BlockedByMode
(exit 11) — descartado: el 11 significa "acción prohibida solicitada"; aquí
no hay nada prohibido, hay un turno humano. Confundirlos rompería la semántica
del contrato publicado.

## R7 — Pasada 4 y factualidad en estudio

**Decision**: la pasada 4 en modo estudio verifica la consistencia del texto
humano contra `roots/` y `research.md` (fuentes del proyecto) y emite
hallazgos; la emisión de `claims.md` es opcional y el gate g4 solo se evalúa
si el manifiesto declara `quality_gates.factuality_min` (el comportamiento
que ya tiene: sin umbral, `gates.factuality = null`). No se toca `status.py`
para esto: ya es la semántica actual.

**Rationale**: la obligación constitucional de atribución por afirmación es
del modo produccion; en estudio la IA no afirma nada en el manuscrito — señala
inconsistencias de quien sí escribe. Cero cambios = cero riesgo de regresión.

## R8 — Dónde escribe la humana y cómo se detecta

**Decision**: los capítulos humanos viven donde los de produccion:
`chapters/NNN-slug.md`, nombrados según el temario de `plan.md`. `status.py`
ya deriva `drafted` de la existencia del archivo; no distingue quién lo
escribió (eso es del informe de autoría). Un archivo de capítulo presente =
capítulo escrito, en ambos modos. La guía de uso para la escritora (cómo
nombrar el archivo, frontmatter mínimo) va en
`writeonmars/docs/how-to-modo-estudio.md`.

**Rationale**: reutiliza toda la maquinaria de detección existente; el modo
no cambia la forma del proyecto, cambia quién escribe.
