# Contrato del ejecutor — Write.OnMars v1.0

## 0. Principio rector

El método funciona sin ejecutor. La verdad del estado vive en **archivos**:
`chapters/NN-*.md`, `specs/<id>/findings.md`, `specs/<id>/claims.md`,
`plan.md` (temario), `.writeonmars-manifest.json`. `status.py` computa el
estado desde disco; cualquier ejecutor (un agente único, Vivarium, otro
orquestador) sigue el mismo `status.py` + los comandos del preset.

Un ejecutor MAPEA este ciclo a su mecánica de trabajo (tareas, procesos,
issues). Si se retira, nada del método se pierde. Ninguna lógica de negocio
(qué revisar, qué corregir, cuándo está aprobado, cuándo cerrar) vive solo en
el ejecutor.

Reglas duras que todo ejecutor MUST preservar (constitución v1.6.0
§ Ejecutores del método):

- **escribe-uno-revisa-otro**: quien redacta una unidad de contenido no la
  revisa.
- **voz ≠ precisión**: las pasadas de naturalidad y de precisión se ejecutan
  por separado (idealmente agentes/modelos distintos).
- **detector ≠ corrector**: quien revisa anota en `findings.md`; quien corrige
  es quien redacta.

Y las obligaciones de modo (constitución § Modos de proyecto): con
`mode: estudio` el ejecutor MUST NOT despachar redacción de manuscrito; el
cambio de modo es humano, explícito y registrado.

## 1. Ciclo de vida de UNA unidad de contenido (capítulo)

Estados conceptuales, siempre **derivables de archivos**:

- **DRAFTING** — no existe `chapters/NN-*.md` → se redacta.
- **IN_REVIEW** — capítulo escrito, pendiente de pasadas → mesa (1·2·3),
  luego precisión (4).
- **NEEDS_REVISE** — `findings.md` tiene ≥1 accionable (crítico+medio) abierto
  para ese capítulo → se aplica la revisión.
- **APPROVED** — pasó mesa **y** precisión sin accionables abiertos.

Bucle: `DRAFTING → IN_REVIEW → (NEEDS_REVISE → IN_REVIEW)* → APPROVED`.

`findings.md` (esquema pass-output v1.0) es el registro durable. Severidad:
**crítico + medio fuerzan revise; bajo = aviso** (no bloquea).

Fan-out: las unidades de trabajo por capítulo se crean **una sola vez**, tras
`plan` + `research` correctos. Nunca una unidad por pasada/estado.

## 2. Etapas globales

Cuando **todos** los capítulos del temario están APPROVED
(`all_chapters_approved` en `status.py --json`):

1. **Pasada 5 global** (formato/coherencia) — puede abrir accionables que
   vuelven al ciclo del capítulo afectado o a un revise global.
2. **Export PDF** — `speckit.intro` + `export.py`.
3. **Checkpoint humano** (PDF anotado) — el único revisor humano.
4. **Feedback** (`feedback_intake.py`) → revise quirúrgico → **close**
   (`close.py`), solo con `status.py --gate` en verde.

Los dos checkpoints humanos del método (brief del Principio III; PDF anotado)
detienen a cualquier ejecutor: MUST NOT firmarse, aprobarse ni sintetizarse
por un agente.

## 3. Contrato de lectura de estado

El ejecutor MUST leer el estado exclusivamente de `status.py --json`. Campos
garantizados (nombres exactos; no inventar): `next_step`, `next_detail`,
`chapters`, `chapters_written`, `chapters_expected`, `passes`,
`criticals_open`, `open_findings_total`, `revise_pending`,
`revise_by_chapter`, `advisory_open_bajo`, `sign_violations`, `gates`,
`closeable`, `has_manifest`, `by_chapter`, `all_chapters_approved`, `track`.

`by_chapter`: objeto keyado por ordinal del temario en string (`"1"`..`"N"`,
más `"global"`), valor `{ "drafted": bool, "passes_done": [int],
"revise_pending": int, "advisory": int, "approved": bool }`.

Cautela obligatoria: `status.py` computa desde archivos y puede ir **por
delante** del trabajo en vuelo del ejecutor. El ejecutor MUST NOT cerrar ni
avanzar etapas globales mientras tenga despachos propios sin disposición.

## 4. Idempotencia y concurrencia (estructurales)

- Antes de crear o despachar, el ejecutor MUST re-verificar el estado en disco
  (¿la salida esperada ya existe?).
- El ejecutor MUST impedir dos instancias concurrentes sobre el mismo proyecto
  (lock, single-flight o equivalente estructural).
- Relanzar el ejecutor tras una interrupción MUST NOT duplicar trabajo ni
  corromper estado: el estado vive en archivos y se re-deriva.

## 5. Conformidad

Una implementación es conforme si: (a) satisface §§ 0-4; (b) retirada del
ejecutor, el proyecto continúa a mano con los mismos comandos del preset y
`status.py` propone el mismo `next_step`; (c) sus despachos y disposiciones
quedan registrados de forma auditable (en Vivarium: `decisions.jsonl`).

Implementaciones conocidas: **Vivarium** (`vivarium/`, primera implementación
conforme, feature 004); Paperclip (archivada, referencia histórica:
`paperclip/FLOW-CONTRACT.md` § 3-6 documenta su mapeo).

## 6. Modo estudio

Delta para proyectos con `.writeonmars-manifest.json` declarando
`mode: estudio`:

- `status.py --json` puede devolver `next_step = "write"` cuando faltan
  capítulos del temario. El ejecutor MUST mapearlo a checkpoint humano
  (exit 10), no a despacho: mensaje recomendado "faltan capítulos por escribir
  (modo estudio)".
- `status.py --json` puede devolver `next_step = "dispose"` cuando hay
  hallazgos accionables a la espera de disposición humana. El ejecutor MUST
  mapearlo a checkpoint humano (exit 10), no a despacho: mensaje recomendado
  "hallazgos a la espera de disposición humana (scripts/dispose.py)".
- En etapa global, si falta `README.md`, el paso `intro` también es checkpoint
  humano en estudio. El README de presentación es prosa publicada.
- El guardarraíl de modo no se elimina: si por un estado imposible el ejecutor
  llega a despachar `implement`, `revise` o `intro` en estudio, sigue aplicando
  el bloqueo de modo (exit 11).
- Si un ejecutor comitea trabajo de agentes, el autor del commit MUST usar la
  convención `<rol>@agents.writeonmars.invalid` para que
  `scripts/authorship.py` pueda clasificar la procedencia.

## 7. Pista corta

Delta para proyectos con `.writeonmars-manifest.json` declarando `track: corta`.

- `status.py --json` expone `track` (`"estandar"` | `"corta"`, siempre presente).
  El ejecutor MUST leerlo de ahí, nunca del manifiesto directamente.
- En etapa global, el paso `intro` **no aplica**: el ejecutor MUST NOT exigir
  `README.md` antes del export, en ningún modo. Una pieza única no tiene README
  de presentación; `export.py` produce la portada compacta.
- El ejecutor MUST NOT cambiar `track` ni ofrecer un comando para hacerlo. El
  escalado vive en `scripts/track.py` y exige identidad humana (Principio VI).
- Ningún otro cambio es admisible. En particular: la pasada combinada (un
  despacho que registra los bloques 1·2·3·5) es transparente para el ejecutor —
  ve el bloque 1 registrado y continúa por la primera pasada ausente, la 4.
- Un ejecutor sin este delta ante un proyecto corta se quedará esperando en el
  paso `intro` (pide un `README.md` que nadie escribirá). Falla ruidosa y
  recuperable, no corrupción de estado.

Campo garantizado adicional en `status.py --json`: `track`.
