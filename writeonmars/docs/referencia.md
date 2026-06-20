# Referencia

Detalle de comandos, scripts, archivos y esquemas del preset `writeonmars`.
Material de consulta, no de lectura lineal.

## Comandos del preset (slash, los ejecuta cualquier agente)

Arranque y ciclo editorial:

| Comando | Hace |
|---|---|
| `speckit.setup` | Bootstrap: copia constitución + crea manifest (una vez tras instalar). |
| `speckit.specify` | Brief de 9 campos con preguntas (checkpoint humano 1). |
| `speckit.research` | `research.md` con cita por concepto obligatorio. |
| `speckit.plan` | Temario + descripciones encadenadas (índice del PDF). |
| `speckit.implement` | Redacta UN capítulo con la voz. SOLO escribe (la revisión es aparte). Acepta nº de capítulo; sin nº, el siguiente pendiente; rehace si ya existe. |
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

`speckit.specify`, `speckit.plan` y `speckit.implement` **reemplazan** (`replaces`)
a los comandos core de Spec Kit en modo editorial, así el flujo estándar es
editorial y el agente no duda entre dos comandos. `research`, las `review.*` y la
operación se suman. La voz, la didáctica y el método viajan en `references/` para
que cualquier modelo los aplique (ver `../AGENTS.md`).

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
├── .writeonmars-manifest.json     # versiones, signing_matrix, operadores
├── README.md                      # intro (entra al PDF como "Acerca de…")
├── chapters/
│   ├── 00-titulo.md               # capítulos (<NN>-titulo.md)
│   └── 01-titulo.md
├── glossary.md | glosario.md      # glosario consolidado
├── anexos.md, common-errors.md    # referencia (entran al PDF)
└── specs/<###-feature>/
    ├── spec.md                    # brief (9 campos) — título del PDF
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
