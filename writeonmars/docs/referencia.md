# Referencia

Detalle de comandos, scripts, archivos y esquemas del preset `writeonmars`.
Material de consulta, no de lectura lineal.

## Comandos del preset (slash, los ejecuta cualquier agente)

Arranque y ciclo editorial:

| Comando | Hace |
|---|---|
| `speckit.setup` | Bootstrap: copia el **núcleo** de la constitución + crea manifest (una vez tras instalar). |
| `speckit.constitution` | **Primer paso del ciclo.** Guiado con defaults por sector: elige sector y rellena las **adendas del proyecto** (tono, terminología, anglicismos, relajaciones, gobernanza) sobre el núcleo. `replaces` el core de Spec Kit. |
| `speckit.specify` | Brief de **8 campos descriptivos** con preguntas; el tono se hereda de las adendas (checkpoint humano 1). |
| `speckit.research` | `research.md` con cita por concepto obligatorio. |
| `speckit.plan` | Temario + descripciones encadenadas (índice del PDF). |
| `speckit.implement` | Redacta UN capítulo con la voz y la estructura del sector; cierra con su `## Fuentes`. SOLO escribe (la revisión es aparte). Acepta nº de capítulo; sin nº, el siguiente pendiente; rehace si ya existe. |
| `speckit.intro` | Genera el `README.md` de presentación (apertura del PDF) desde el brief y el temario. Antes del export. |

Revisión (escribe uno, revisa otro — cada pasada asignable a un modelo distinto):

| Comando | Hace |
|---|---|
| `speckit.review` | Agrupado: corre las 4 pasadas. |
| `speckit.review-structure` | Pasada local: estructura + utilidad. |
| `speckit.review-voice` | Pasada local: naturalidad (`prosa-base` para el hilo + registro del manifiesto + `marcela-prose` para la voz). |
| `speckit.review-precision` | Pasada local: contrasta contra `research.md` y **verifica las fuentes en vivo** (abre la URL/web) los datos volátiles. |
| `speckit.review-global` | Pasada global: formato + coherencia (libro entero). |
| `speckit.revise` | Aplica al texto los hallazgos abiertos de `findings.md` (cierra el loop). |

Operación (envuelven un script determinista):

| Comando | Envuelve | Hace |
|---|---|---|
| `speckit.status` | `status.py` | Tablero de estado + gates de cierre. |
| `speckit.export` | `export.py` | Genera el PDF editorial. |
| `speckit.feedback` | `feedback_intake.py` + agente | Aplica el feedback del PDF anotado. |
| `speckit.close` | `close.py` | Gate de cierre + export en un paso. |
| `speckit.memory` | `index.py` | Indexa y busca el contenido del proyecto. |

`speckit.constitution`, `speckit.specify`, `speckit.plan` y `speckit.implement`
**reemplazan** (`replaces`) a los comandos core de Spec Kit en modo editorial, así
el flujo estándar es editorial y el agente no duda entre dos comandos. `research`,
las `review.*` y la operación se suman. La voz, la didáctica y el método viajan en
`references/` para que cualquier modelo los aplique (ver `../AGENTS.md`).

## Constitución por capas: núcleo + adendas + sectores

La constitución de cada guía tiene dos capas:

- **Núcleo** (`.specify/memory/constitution.md`, versionado): las reglas universales
  (Principios I–VI, estándares, gobernanza). Lo copia `speckit.setup` y NO se edita
  por guía. `bootstrap.py --force` lo re-sella desde el preset **preservando las
  adendas** (frontera: el centinela `<!-- WRITEONMARS:ADENDAS -->`).
- **Adendas del proyecto** (sección `## Adendas del proyecto` del mismo archivo): lo
  normativo que varía por guía — sector, tono calibrado, contrato terminológico,
  anglicismos admitidos, matices léxicos, relajaciones estructurales y gobernanza.
  Las rellena `speckit.constitution`; la revisión las verifica.

Las **bases de sector** (`references/sectores/<slug>.md`) aportan los valores por
defecto de las adendas por dominio. Hoy: `tecnologia`. Ampliable creando un archivo
(esquema en `references/sectores/_index.md`). El brief (`spec.md`) queda para lo
descriptivo; las adendas, para lo normativo por guía.

La plantilla de la capa por guía es `templates/adendas-template.md`.

## Scripts (deterministas, sin agente)

Son nueve, más `findings_lib.py` (librería compartida: parser de `findings.md`,
manifiesto, temario; no es CLI).

### `bootstrap.py`

Instala lo que el preset no puede: copia el núcleo de la constitución a
`.specify/memory/` y crea el `.writeonmars-manifest.json`. Se corre una vez, tras
`specify preset add`. Equivale a `/speckit-setup`.

| Flag | Default | Descripción |
|---|---|---|
| `--project-dir` | `.` | Raíz del proyecto. |
| `--operator`, `--email` | de `git config` | Identidad del operador. |
| `--mode` | `produccion` | `produccion` o `estudio` (env `WRITEONMARS_MODE`). |
| `--track` | `estandar` | `estandar` o `corta` (env `WRITEONMARS_TRACK`). |
| `--sector` | ninguno (`null`) | Slug de sector; fija `registro` y materializa las adendas (env `WRITEONMARS_SECTOR`). |
| `--force` | off | Regenera constitución y manifiesto existentes (preserva las adendas). |

Sin `--force`, sobre un proyecto ya bootstrapeado **no cambia nada**: `--track` y
`--sector` solo surten efecto al crear.

### `export.py`

Genera el PDF. Reutiliza `assets/style.css` (motor de `markdown-to-pdf`).

| Flag | Default | Descripción |
|---|---|---|
| `--project-dir` | `.` | Raíz del proyecto. |
| `--spec` | el de número más alto | Spec a usar. |
| `--chapters-dir` | `<proyecto>/chapters` | Carpeta de capítulos. |
| `--title` | del `spec.md` | Título de portada. |
| `--subtitle` | vacío | Subtítulo. |
| `--eyebrow` | vacío | Texto pequeño superior. |
| `--meta` | año actual | Meta de portada. |
| `--output` | `<slug-título>.pdf` | Ruta del PDF. |
| `--chrome` | autodetecta (`WOM_CHROME`) | Binario de Chrome/Chromium. |
| `--keep-temp` | off | Conserva el HTML intermedio. |
| `--strict-claims` | off | Falla si `claims.md` no cuadra con los capítulos. |

En `track: corta` detecta la pista solo y produce una portada compacta, sin índice.

### `status.py`

| Flag | Descripción |
|---|---|
| `--project-dir` | Raíz del proyecto. |
| `--spec` | Spec a evaluar. |
| `--gate` | Exit 1 si el proyecto NO cierra. |
| `--json` | Emite el estado completo del proyecto en JSON, incluido el campo `next_step` (`setup`→`constitution`→`specify`→`research`→`plan`→`implement`→`review`→`revise`→`close`; en estudio, también `write` y `dispose`) que el ejecutor orquestado usa para decidir a qué rol delegar. |

### `feedback_intake.py`

| Flag | Descripción |
|---|---|
| `--pdf` (requerido) | PDF anotado. |
| `--project-dir`, `--spec` | Proyecto y spec. |

Salida: `specs/<spec>/feedback.md` y `feedback-changeset.json`.

### `close.py`

| Flag | Descripción |
|---|---|
| `--project-dir`, `--spec` | Proyecto y spec. |
| `--no-export` | Solo evalúa el gate. |
| `export_args` | Flags que se pasan a `export.py`. |

### `index.py`

```
index.py build [--project-dir .]
index.py query "<texto>" [--top 5] [--project-dir .]
```

Genera/usa `.writeonmars-index.json` (caché reconstruible).

### `dispose.py` (solo en `mode: estudio`)

Registra tu decisión sobre un hallazgo abierto: edita la celda `estado` de `findings.md`
y añade una línea a `disposiciones.jsonl`. **Exige identidad humana**: la lee de
`git config` y rechaza las identidades de agente.

```
dispose.py F-1.1 --aceptar
dispose.py F-1.2 --rechazar --motivo "no aplica a este género"
dispose.py F-1.3 --aplazar
```

| Flag | Descripción |
|---|---|
| `--aceptar` / `--rechazar` / `--aplazar` | Exclusivos; uno es obligatorio. |
| `--motivo` | Obligatorio con `--rechazar` (mín. 3 caracteres). |
| `--nota` | Anotación libre opcional. |
| `--project-dir`, `--spec`, `--json` | Proyecto, spec y salida JSON. |

*Aceptar* significa que ya aplicaste tú la corrección. *Aplazar* deja deuda declarada:
no bloquea el cierre, pero `close.py` la enumera.

### `track.py`

Único camino para cambiar la pista de ceremonia. Escritura atómica del manifiesto más
una entrada en `track_history`. **Exige identidad humana**; ningún agente cambia `track`.

| Flag | Descripción |
|---|---|
| `--escalar` | `corta → estandar`. Siempre legal. No mueve ningún archivo. |
| `--desescalar` | `estandar → corta`. Solo con temario de ≤1 fila y sin capítulos de ordinal ≥2. |
| `--check` | Valida el invariante de pieza única. Read-only. |
| `--project-dir`, `--spec`, `--json` | Proyecto, spec y salida JSON. |

### `authorship.py`

Informe determinista de autoría humana frente a IA, por capítulo: cruza los commits de
git sobre `chapters/` (identidad del autor y ventanas de despacho de `decisions.jsonl`).
Emite un veredicto por capítulo (`humana`, `ia`, `mixta`) y uno global.

| Flag | Default | Descripción |
|---|---|---|
| `--project-dir` | `.` | Raíz del proyecto. |
| `--out` | `specs/<spec>/authorship-report.md` | Ruta del informe. |
| `--json` | off | Salida JSON. |

## Herramientas de scaffolding y orquestación

Viven en la raíz del repo del framework (fuera del preset). Levantan un proyecto
editorial nuevo y lo recorren desatendido.

### `tools/new-guide.sh`

Scaffolding de una guía en un comando: crea el repo, `specify init --integration`,
`preset add`, bootstrap, symlinks de contexto multi-agente y un commit que queda como
base ref. El destino está siempre fuera del repo del framework.

| Flag | Default | Descripción |
|---|---|---|
| `--agents` | `claude,gemini,codex` | CSV de agentes; el 1º es el primario de `specify init`. |
| `--skip-init` | off | Omite `specify init`. |
| `--refresh-preset` | off | Re-copia el preset en una guía ya scaffoldeada. |
| `--preset` | preset del repo | Ruta del preset a copiar. |
| `--operator` | de `git config` | Id del operador. |
| `--email` | de `git config` | Email del operador. |

La **pista** y el **sector** se declaran por entorno, porque el script no tiene flags
propios para ellos y `bootstrap.py` los toma como valores por defecto:
`WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia bash tools/new-guide.sh <dir>`.
Solo surten efecto **al crear**: sobre un proyecto ya bootstrapeado no cambian nada
(para eso está `track.py`).

### `vivarium` (ejecutor orquestado)

Binario headless en Rust (`vivarium/`). Recorre el ciclo solo, despachando cada paso al
CLI de agente que declare `.vivarium/config.toml`. Lee el estado con `status.py --json`;
nunca lo calcula por su cuenta.

| Comando | Descripción |
|---|---|
| `vivarium new <dir> --kind <kind>` | Crea el proyecto: git, `specify init`, preset, bootstrap y commit base. |
| `vivarium check` | Valida manifiesto, config BYOM y binarios de cada rol. No ejecuta nada. |
| `vivarium status` | Estado combinado (el de `status.py` + modo + despachos en vuelo). Read-only. |
| `vivarium step` | Ejecuta un solo paso. |
| `vivarium run` | Avanza hasta bloqueo o cierre. |
| `vivarium mode set <modo> --yes` | Cambia `produccion`/`estudio` con registro en el manifiesto. |

Códigos de salida: `0` progreso o cierre · `10` checkpoint humano · `11` guardarraíl de
modo estudio · `12` despacho fallido · `6` lock tomado · `2` uso inválido · `3` falta un
binario · `4` falta `--yes` · `5` validación.

Roles del BYOM y sus pasos: `redactora` (`plan`, `implement`, `revise`, `intro`),
`editora_mesa` (pasadas 1, 2, 3 y 5), `documentalista` (`constitution`, `research`,
pasada 4) y `sidecar` (`setup`, `export`, `close`: scripts, sin modelo).

> `vivarium new --sector` escribe el sector *después* del bootstrap y deja el proyecto sin
> adendas ni registro. Usa `WRITEONMARS_SECTOR`. Deuda anotada en el ROADMAP.

### Capa `paperclip/` (archivada)

Fue el primer ejecutor orquestado: una Company **Write.OnMars** con un roster de 4 roles
editoriales. **Archivada el 2026-07-07**; `hire-team.sh` y los bundles de
`paperclip/agents/` ya no se usan. Sus §§ 0-2 de `paperclip/FLOW-CONTRACT.md` sobreviven
como el contrato agnóstico del ejecutor que Vivarium implementa.

## Etiquetas de feedback (en los comentarios del PDF)

| Categoría | Etiquetas |
|---|---|
| Tipo | `#dato` `#voz` `#estructura` `#claridad` `#cobertura` |
| Acción | `#recortar` `#ampliar` |
| Severidad | `#critico` `#medio` `#bajo` |

Sin etiqueta: el tipo se infiere del subtipo de anotación (resaltado → Voz,
tachado → Recortar…) y la severidad por defecto es `medio`.

## Estructura de un proyecto editorial

```text
mi-guia/
├── .writeonmars-manifest.json     # versiones, signing_matrix, operadores, sector
├── .specify/memory/constitution.md# núcleo (versionado) + ## Adendas del proyecto
├── README.md                      # intro (entra al PDF como "Acerca de…")
├── chapters/
│   ├── 00-titulo.md               # capítulos (<NN>-titulo.md); cierran con ## Fuentes
│   └── 01-titulo.md
├── glossary.md | glosario.md      # glosario consolidado
├── anexos.md, common-errors.md    # referencia (entran al PDF)
└── specs/<###-feature>/
    ├── spec.md                    # brief (8 campos; tono heredado) — título del PDF
    ├── plan.md                    # temario + descripciones — índice del PDF
    ├── research.md                # citas por concepto
    ├── findings.md                # salida de las pasadas
    ├── feedback.md                # log del PDF anotado
    └── feedback-changeset.json    # change-set para re-despacho
```

## Esquema de `findings.md` (pass-output v1.0)

Cada pasada añade un bloque:

```markdown
## Pasada N — {nombre}
**Estado pasada**: passed | passed-with-warnings | blocked
**Firma**:
  - tipo: autonomous | human
**Capítulos cubiertos**: [1, 2] o "global"

### Hallazgos
| ID | Capítulo | Severidad | Frase original | Problema | Reescritura | Estado | Citas |
```

Severidad: `critico | medio | bajo` (solo `critico` bloquea). Estado:
`abierto | resuelto | desviacion_justificada`.

## `signing_matrix` del manifiesto

Claves: `pasada_1_estructura`, `pasada_2_utilidad`, `pasada_3_naturalidad`,
`pasada_4_precision`, `pasada_5_formato`. Valor: `autonomous` | `human`.
Default del bootstrap: **todas autónomas** (el control humano es el PDF anotado al
final). Pon `human` en una pasada solo si una guía delicada lo pide. Aparte, un
hallazgo `critico` abierto bloquea el cierre sea cual sea la firma.

## Gates de cierre

1. **Críticos** (FR-020): ≥ 1 finding `critico` + `abierto` → bloquea.
2. **Firmas** (FR-020a): una pasada que la matriz exige `human` sin firmar por un
   operador real (actor vacío o `pendiente`) → bloquea. Con el default (todas
   autónomas) este gate no aplica.
3. **Completitud**: faltan capítulos del temario (`plan.md`) → bloquea `close`.
   `export` sí permite un PDF parcial (preview).

## Dependencias por pieza

| Pieza | Necesita |
|---|---|
| `export` / `close` | `pandoc` + Chrome/Chromium (ruta con `--chrome` o `WOM_CHROME` si no está en las habituales) |
| `feedback` | `pymupdf` (recomendado) o `pypdf` |
| `memory` | nada (TF); `rank-bm25` opcional para BM25 |
| `bootstrap` | nada; `jsonschema` opcional para validación completa del manifest |

Las dependencias de Python se instalan juntas con
`pip install -r scripts/requirements.txt` (todas opcionales: cada pieza degrada
o avisa si le falta la suya).

## Salidas generadas (caché, gitignorables)

`<slug>.pdf`, `specs/<spec>/feedback.md`, `feedback-changeset.json`,
`.writeonmars-index.json`.
