# Write.OnMars — Roadmap y estado

> Estado al **2026-06-15**. Resumen de lo construido, lo validado de verdad y lo
> que queda. Punto de retorno para no perder el hilo entre sesiones.

## En una frase

El método editorial es un **preset de Spec Kit agente-agnóstico** (`writeonmars/`),
instalable con `specify preset add` y **probado de punta a punta**. La voz, la
didáctica y el método viajan como **referencias** neutrales de modelo; la lógica,
como **comandos**; lo determinista, como **scripts**. Falta operacionalizar la
orquestación (Paperclip) y pulir la distribución.

## Cómo está montado (capas)

- **Método** — el preset `writeonmars/`, que corre *dentro* de un agente (Claude,
  Codex, Gemini…) vía comandos `speckit.*`.
- **Orquestación** — Paperclip, pendiente; envolverá el método para producir varias
  guías en volumen.
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
- **6 scripts deterministas**: `bootstrap`, `status`, `export`, `feedback_intake`,
  `close`, `index`.
- **`references/`**: voz (`marcela-prose`), didáctica (`technical-guide-design`),
  método (`writeonmars-*`), **sectores** (`sectores/<slug>.md`: defaults por dominio
  para las adendas; hoy `tecnologia`, ampliable con solo añadir un archivo).
  **`contracts/`**: citación, manifest, pass-output.
  **`memory/constitution.md`** (bundled).
- **`AGENTS.md`** (contrato agente-agnóstico) + **`docs/`** (Diátaxis: tutorial,
  how-to, referencia, arquitectura) + **`smoke-test.sh`**.

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
- Constitución **v1.3.0** (Principio V 3+1; Principio VI neutralidad de modelo).

## Pendiente (orden sugerido)

1. **Registrar los comandos para Codex/Gemini nativamente** (hoy se les apunta al
   archivo del comando; funciona, pero registrarlos evita pegar la ruta).
2. **Opcionales del preset**: búsqueda semántica real en `index.py` (embeddings,
   chromadb); hook `after_close` para auto-export.
3. **Capa Paperclip**: modelar la "empresa", un goal por guía, agentes por
   paso/modelo, presupuestos y heartbeats.
4. **Distribución**: elegir licencia, publicar el preset
   (`specify preset add --from <github>`), versionar releases.

## Deuda y cosas honestas a saber

- **Docs**: `writeonmars/docs/` es la fuente canónica de uso. Los docs raíz
  (`docs/`) llevan banner y quedan como referencia interna; algunos aún describen
  el mundo viejo (skills + install.sh) en el cuerpo.
- **Invocación**: para Claude los comandos se registran como skills **con guion**
  (`/speckit-specify`), aunque el nombre canónico lleva **punto** (`speckit.specify`).
  Los docs mezclan ambas formas; pendiente de unificar.
- **Sincronía de voz**: `references/voz/` es copia de `mars-voice`. Si actualizas la
  voz allí, re-sincroniza (`cp`) la del preset.
- **`guia-prueba`**: su `findings.md` quedó con numeración mezclada de pruebas
  previas; se limpia al re-correr `review` con el preset corregido.
- **`install.sh`**: legacy. La vía canónica es el preset.

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
