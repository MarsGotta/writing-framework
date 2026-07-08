# Data Model — 004-vivarium-core (Phase 1)

Entidades, derivaciones y transiciones del núcleo. La regla de oro (FR-003):
ninguna de estas entidades se **almacena** en el ejecutor; se **derivan** de
archivos del proyecto o son configuración/registro en el propio repo editorial.

## 1. Proyecto editorial

Un repositorio git con el preset instalado. El bootstrap (FR-001) lo deja así:

```text
<proyecto>/
├── .git/                        # git2: init + commit base
├── .specify/                    # lo escribe `specify init` + `preset add`
│   └── presets/writeonmars/     # scripts sidecar (status.py, bootstrap.py, …)
├── .writeonmars-manifest.json   # manifiesto v1.3.0 (con mode)
├── .vivarium/                   # NO versionado (.gitignore); config + lock + tasks
│   └── config.toml              # BYOM (contracts/byom-config.md)
├── roots/                       # fuentes de grounding (§ 5)
│   └── README.md                # convención de fichas (la escribe el bootstrap)
├── decisions.jsonl              # registro append-only (§ 6), vacío al crear
└── (specs/, chapters/, findings.md … los crean los pasos del método)
```

Validaciones al crear: git/python3/specify disponibles; manifiesto resultante
valida contra `writeonmars/contracts/manifest-schema.json`; `status.py --json`
responde con `next_step` ∈ enum conocido; commit base existe.

## 2. Manifiesto: `mode` y `mode_history`

Extensión exacta en `contracts/manifest-mode.md` (schema v1.2.1 → v1.3.0).

- `mode`: `"produccion"` | `"estudio"`; **opcional**; ausencia ⇒ `produccion`.
- `mode_history`: array append-only de `{from, to, date}` (ISO 8601). Vacío o
  ausente si nunca hubo cambio.

Default por tipo de proyecto al crear (`vivarium new --kind <kind>`), siempre
sobrescribible con `--mode`:

| `--kind` | `mode` default |
|---|---|
| `guia` (guía técnica), `tutorial`, `documentacion`, `no-ficcion` | `produccion` |
| `novela`, `relato`, `poesia`, `guion`, `academico` | `estudio` |

Valor de `mode` fuera del enum ⇒ error de validación explícito (edge case de
la spec), nunca interpretación silenciosa.

## 3. Estado por capítulo (derivado, jamás almacenado)

Fuente: `status.py --json` campo `by_chapter` (contrato en
`paperclip/FLOW-CONTRACT.md` § 3.7, que el executor-contract § 3 recoge):
`{ "drafted": bool, "passes_done": [int], "revise_pending": int,
"advisory": int, "approved": bool }` keyado por ordinal en string.

Derivación del estado conceptual:

| Estado | Condición sobre `by_chapter[N]` |
|---|---|
| `DRAFTING` | `!drafted` |
| `IN_REVIEW` | `drafted && !approved && revise_pending == 0` (faltan pasadas) |
| `NEEDS_REVISE` | `drafted && revise_pending > 0` |
| `APPROVED` | `approved` (= drafted ∧ {1,2,3,4} ⊆ passes_done ∧ revise_pending == 0) |

Transiciones válidas (executor-contract § 1):
`DRAFTING → IN_REVIEW → (NEEDS_REVISE → IN_REVIEW)* → APPROVED`. El runner
nunca fuerza una transición escribiendo archivos de estado: despacha el relevo
cuyo efecto esperado es la transición, y re-deriva.

Señal global: `all_chapters_approved == true` dispara las etapas globales
(§ 4), **solo si** no hay despachos propios sin disposición (R7).

## 4. Mapa `next_step` → acción (el corazón del runner)

`next_step` enum (contrato de `status.py`): `setup → constitution → specify →
research → plan → implement → review → revise → close`.

| `next_step` | Acción del runner | Rol / ejecutor | Humano |
|---|---|---|---|
| `setup` | sidecar `bootstrap.py` (o ya hecho por `vivarium new`) | sidecar | no |
| `constitution` | despacho `speckit.constitution` **no-interactivo**: adendas desde los defaults de la base de sector (`references/sectores/<slug>.md`); el sector llega de `vivarium new --sector` (o del manifiesto). La operadora puede ajustar las adendas a mano después — decisión documentada, hallazgo U1 del análisis | `documentalista` | no |
| `specify` | **checkpoint 1**: detenerse; el brief lo firma la operadora | — | **sí** |
| `research` | despacho `speckit.research` | `documentalista` | no |
| `plan` | despacho `speckit.plan` | `redactora` | no |
| `implement` | por capítulo sin draft (`by_chapter`): despacho `speckit.implement N` | `redactora` | no |
| `review` | por capítulo drafted sin pasadas: 1-3 → `editora_mesa`; 4 → `documentalista` | mesa/doc | no |
| `revise` | por capítulo en `revise_by_chapter`: despacho `speckit.revise N` | `redactora` | no |
| global: pasada 5 | cuando `all_chapters_approved`: despacho `speckit.review-global` | `editora_mesa` | no |
| global: intro | despacho `speckit.intro` (README de presentación del PDF, antes del export — executor-contract § 2) | `redactora` | no |
| global: export | sidecar `export.py` | sidecar | no |
| global: feedback | **checkpoint 2**: detenerse; PDF anotado → `feedback_intake.py` manual. Atendido cuando existe `specs/<spec>/feedback.md`; hasta entonces el runner NO cierra aunque los gates estén verdes | — | **sí** |
| `close` | sidecar `close.py` solo con `closeable == true` y gates verdes | sidecar | no |

Guardarraíl de modo (FR-008): con `mode: estudio`, las filas `implement` y
`revise` (y cualquier despacho cuya salida esperada cree o reescriba
`chapters/`/`content/`) están **prohibidas**: el runner las reporta como
`blocked_by_mode` y se detiene. Las filas de revisión/verificación siguen
permitidas cuando la spec 005 las materialice.

Reglas de relevo (FR-005) aplicadas en la asignación: el rol que redactó una
unidad no recibe sus pasadas (con 3 roles esto es estructural: redactora
nunca revisa); pasadas 1-3 y 4 se despachan por separado; los revisores solo
escriben `findings.md`/`claims.md`, el `revise` siempre va a `redactora`.

## 5. Ficha de Root (`roots/*.md`) — solo convención en esta feature

Un concepto por archivo; la ruta es la identidad. Frontmatter mínimo:

```markdown
---
type: fuente        # personaje | lugar | fuente | cita | evento (tipos editoriales propios)
alias: []           # nombres alternativos declarados
---
(cuerpo libre en markdown)
```

Compatible con OKF v0.1 sin depender de él (`docs/vivarium.md` § 13, grafo de
Roots). Esta feature solo crea la carpeta y `roots/README.md` documentando la
convención; índice, matching y grafo son etapa 2 (fuera de alcance).

## 6. DecisionRecord (`decisions.jsonl`)

Una línea JSON por evento, append-only, versionada. Schema exacto:
`contracts/decision-record.schema.json`. Campos: `v` (int, =1), `ts` (ISO
8601), `event` (`dispatch` | `disposition` | `mode_change` | `checkpoint`),
`step`, `chapter` (string ordinal o `"global"` o null), `role`, `outcome`
(para disposition: `ok` | `revise` | `failed`), `detail` (string corto).

Invariantes: todo `dispatch` tiene a lo sumo una `disposition` posterior que
lo cierra (correlación por `step`+`chapter`+orden); un `mode_change` registra
`detail: "from→to"` y coincide con `mode_history` del manifiesto; el runner no
avanza etapas globales con `dispatch` sin `disposition` (R7).

## 7. Configuración BYOM (`.vivarium/config.toml`)

Formato exacto: `contracts/byom-config.md`. Tres roles obligatorios
(`redactora`, `editora_mesa`, `documentalista`), cada uno una plantilla de
orden con placeholders `{prompt_file}`, `{project_dir}`, `{chapter}`.
Validación al arrancar: los tres roles presentes, binarios resolubles,
plantillas con `{prompt_file}`. Recomendación operativa (no gate): agente o
modelo de `redactora` ≠ `editora_mesa` (voz ≠ precisión con modelos cruzados).

## 8. Lock de proyecto (`.vivarium/lock`)

Advisory lock del SO (fd-lock) tomado por `vivarium step|run`. Si está tomado:
exit code dedicado sin efectos. Se libera al morir el proceso (sin staleness
manual). Nunca se versiona.
