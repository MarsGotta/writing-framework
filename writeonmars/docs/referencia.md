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
| `speckit.review-voice` | Pasada local: voz (`marcela-prose`). |
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

### `status.py`

| Flag | Descripción |
|---|---|
| `--project-dir` | Raíz del proyecto. |
| `--spec` | Spec a evaluar. |
| `--gate` | Exit 1 si el proyecto NO cierra. |
| `--json` | Emite el estado completo del proyecto en JSON, incluido el campo `next_step` (`setup`→`constitution`→`specify`→`research`→`plan`→`implement`→`review`→`revise`→`close`) que el orquestador (heartbeat de Paperclip) usa para decidir a qué rol delegar. |

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

## Herramientas de scaffolding y orquestación

Viven en la raíz del repo del framework (fuera del preset). Levantan una guía nueva
y contratan el equipo ejecutor en Paperclip.

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

### `paperclip/hire-team.sh`

Contrata el equipo ejecutor (Documentalista, Redactora, Editora de mesa) en la Company
de Paperclip vía su CLI. Idempotente; modelos cruzados (Redactora = Opus, revisoras =
Sonnet).

| Flag | Default | Descripción |
|---|---|---|
| `--no-headless` | off | Crea los agentes sin `dangerouslySkipPermissions`. |
| `--company` | `Write.OnMars` | Nombre de la Company. |

### Capa `paperclip/`

Modelo de orquestación sobre Paperclip: una Company **Write.OnMars** (la casa), cada
guía es un **Project** (workspace local) y un roster de 4 roles editoriales con bundles
de instrucciones en `paperclip/agents/<rol>/`. Detalle en `paperclip/README.md`.

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
| `export` / `close` | `pandoc` + Chrome/Chromium |
| `feedback` | `pymupdf` (recomendado) o `pypdf` |
| `memory` | nada (TF); `rank-bm25` opcional para BM25 |

## Salidas generadas (caché, gitignorables)

`<slug>.pdf`, `specs/<spec>/feedback.md`, `feedback-changeset.json`,
`.writeonmars-index.json`.
