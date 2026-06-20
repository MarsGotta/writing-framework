# Preset `writeonmars`

Empaquetado nativo de Write.OnMars como preset de Spec Kit. Esta carpeta es la
unidad instalable: lo que consume `specify preset add`.

## Documentación

Organizada por lo que necesitas en cada momento (modelo Diátaxis):

| Necesitas | Documento |
|---|---|
| Aprender el flujo completo de cero | [docs/tutorial-primera-guia.md](docs/tutorial-primera-guia.md) |
| Resolver una tarea concreta | [docs/how-to.md](docs/how-to.md) |
| Consultar comandos, flags y esquemas | [docs/referencia.md](docs/referencia.md) |
| Entender las decisiones de diseño | [docs/arquitectura.md](docs/arquitectura.md) |

## Qué empaqueta este preset

Es **agente-agnóstico**: lo ejecuta cualquier agente con cualquier modelo, no solo
Claude. Por eso la lógica vive en los comandos y las reglas en `references/`, no en
skills de un proveedor. Se instala con `specify preset add`.

| Pieza | Dónde | Para qué |
|---|---|---|
| Plantillas editoriales | `templates/` | spec/plan/tasks/checklist/constitution en modo editorial |
| Comandos (ciclo + operación) | `commands/` | `speckit.setup/specify/research/plan/implement/intro/review (+pasadas)/revise` + `status/export/feedback/close/memory` |
| Scripts deterministas | `scripts/` | export, status, feedback, close, index |
| Referencias neutrales de modelo | `references/` | voz (`voz/`), didáctica (`didactica/`), método (`metodo/`) que cualquier agente aplica |
| Contrato del agente | `AGENTS.md` | reglas para ejecutar el pipeline con cualquier modelo |

Lo único que un preset no puede traer y aún necesita un bootstrap mínimo en el
proyecto: el `.writeonmars-manifest.json`, los hooks de git y (opcional) el MCP de
research.

Regla mental: **el preset trae el qué, el cómo y la voz; el proyecto solo aporta su
manifest y sus hooks.**

## Decisión de arquitectura: sin `wom` CLI

El spec `002-wom-cli` queda **superseded**. El CLi servía para operar el
framework sin agente (`wom new/status/sign/close`), pero:

- la firma humana por pasada se sustituyó por el checkpoint del PDF anotado, así
  que `wom sign` sobra;
- los dos modos de ejecución (speckit+agentes, speckit+paperclip+agentes)
  siempre tienen agente, así que "operar sin agente" no aplica;
- lo determinista que sí valía (status, close, validación) pasa a `scripts/` de
  este preset, invocable por el agente o por Paperclip.

Una sola vía: `specify preset add` + skills + agente, con Paperclip por encima
para volumen.

## Instalación

```bash
# Local / desarrollo (desde la raíz del repo writing-framework):
specify preset add --dev ./writeonmars

# Publicado (cuando se etiquete una release):
specify preset add --from https://github.com/MarsGotta/writing-framework/...
```

No hace falta instalar skills ni `install.sh`: la voz, la didáctica y el método
viajan en `references/` (confirmado: `specify preset add` copia todo el preset,
incluidas las referencias, e instala los comandos como skills del agente).

Tras instalar, corre **una vez** el bootstrap — instala lo que un preset no puede
(la constitución y el manifest del proyecto):

```bash
python3 .specify/presets/writeonmars/scripts/bootstrap.py
# o, como comando del agente:  /speckit-setup
```

Nota de invocación: para Claude, los comandos se registran como skills con guion,
así que se llaman `/speckit-setup`, `/speckit-specify`, etc. (no con punto).

## Estado

Probado de punta a punta en un proyecto real (`guia-prueba`). **5 plantillas +
17 comandos + 6 scripts**, neutral de modelo. Instala con `specify preset add
--dev ./writeonmars`.

Ciclo editorial: `speckit.setup` → `speckit.specify` → `speckit.research` →
`speckit.plan` → `speckit.implement` → `speckit.review` (+ pasadas sueltas) →
`speckit.revise` → `speckit.intro`. Operación:

| Comando | Script | Qué hace |
|---|---|---|
| `speckit.status` | `status.py` | tablero pasadas × estado × firma + gates de cierre |
| `speckit.export` | `export.py` | PDF editorial (estilo `markdown-to-pdf`); portada del brief, índice del temario |
| `speckit.feedback` | `feedback_intake.py` | PDF anotado → change-set quirúrgico (mapea por texto anclado) |
| `speckit.close` | `close.py` | gate de cierre + export en un paso |
| `speckit.memory` | `index.py` | indexa y busca el contenido del proyecto (BM25 / TF) |

(Las 5 plantillas no llevan comando: las consume Spec Kit directamente.)

Dependencias por pieza: `pandoc` + Chrome/Chromium (`export`); `pymupdf` o
`pypdf` (`feedback`); `rank-bm25` opcional (`memory`, si no usa TF sin
dependencias). En Linux/Paperclip, Chrome = `chromium`.

**Pendiente opcional** (no bloquea producir guías):

- Búsqueda **semántica** real en `index.py` (embeddings vía chromadb +
  sentence-transformers); hoy es keyword (BM25/TF).
- Registrar `close`/`export` como **hook nativo** (`after_analyze`) dentro de una
  extensión; hoy se llaman por comando/script, que cubre ambos modos.

**Nota:** la skill `markdown-to-pdf` se queda como front-end interactivo; su motor
y `style.css` se comparten con `export.py` (una sola fuente de estilo).

Los comandos se declaran en `preset.yml` dentro de `provides.templates` con
`type: command` (es la lista que `specify preset add` lee). Los scripts viajan en
`scripts/` y los comandos los invocan por ruta: Spec Kit aún no registra scripts vía
preset ("reserved for future use").

## Modelo de revisión (Principio V)

3 pasadas locales por capítulo (estructura+utilidad / naturalidad con
`marcela-prose` / precisión con `writeonmars-contraste`) + 1 pasada global
(formato + coherencia entre capítulos). Las cinco dimensiones se conservan como
ítems de checklist; bajan de 5 ejecuciones a 4.
