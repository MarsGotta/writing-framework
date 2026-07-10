---
description: "Primer paso del ciclo. Te guía con preguntas (y valores por defecto) para fijar las adendas del proyecto sobre el núcleo de la constitución: sector, tono, terminología, anglicismos, gobernanza. Neutral de modelo."
replaces: "speckit.constitution"
---

# Constitución del proyecto editorial

Es **lo primero** que se hace en una guía, después de `/speckit-setup`. El núcleo
de la constitución es universal y no se toca: lo que aquí decides es la **capa por
guía** (las *adendas*) — lo normativo que sí cambia entre una guía y otra. Lo
descriptivo (audiencia, problema, ejemplo recurrente) NO va aquí: eso es el brief
de `/speckit-specify`.

Tú no tienes que recordar qué preguntar. Al activar este comando, **el agente te
hace las preguntas una a una, con un valor por defecto en cada una**. Pulsar Enter
mantiene el estándar; escribir algo lo cambia.

## User Input

```text
$ARGUMENTS
```

Opcional. Si trae un sector (p. ej. `tecnologia`) o `--defaults`, el agente lo usa
para acortar el camino. Si está vacío, el agente arranca el cuestionario igual.

## Precondición

Debe existir `.specify/memory/constitution.md` (el núcleo, que copia
`/speckit-setup`). Si no existe, detente y pide correr `/speckit-setup` primero.

## Detalle del método

`.specify/presets/writeonmars/references/metodo/writeonmars-constitution/SKILL.md`

## Qué haces

### 1. Elegir sector

Lista los sectores disponibles leyendo `references/sectores/*.md` (ignora
`_index.md`). Muestra cada uno con su nombre y una línea de alcance, numerados.
Pregunta cuál aplica.

- Si solo hay uno (hoy, `tecnologia`), proponlo como opción 1 y pide confirmación.
- El sector elegido carga su **base de defaults** (`references/sectores/<slug>.md`):
  de ahí salen los valores por defecto de las preguntas siguientes.

### 1b. Elegir registro (capa 2 de la pirámide de prosa)

Lista los registros disponibles leyendo `references/registros/*/SKILL.md`
(ignora `_index.md`). El sector propone su default (sección "Registro por
defecto" de la base; tecnología propone `tecnico-divulgativo`). Pide
confirmación o elección. El registro fija formalidad, densidad, figuras y
aserción del género; la voz del autor (capa 3) va encima y la prosa-base
(capa 1) debajo, siempre.

### 2. Camino rápido (opcional)

Ofrece: *"¿Acepto el estándar de `<sector>` tal cual y escribo las adendas con los
valores por defecto, o prefieres ir pregunta por pregunta?"*

- Si acepta el estándar → rellena las adendas con los defaults del sector y salta
  al paso 4.
- Si prefiere el cuestionario → paso 3.

### 3. Cuestionario guiado (cada pregunta con su valor por defecto)

Hazlas **una a una**, mostrando entre corchetes el valor por defecto del sector.
Enter mantiene el default; una respuesta lo sustituye. No las inventes en bloque.

1. **Tono calibrado** — persona gramatical (plural inclusivo / tú / usted),
   humor sí o no, cercanía; matices sobre el registro elegido en 1b.
   `[default: Tono por defecto del sector + registro del paso 1b]`.
2. **Anglicismos admitidos** — confirma la lista del sector; permite añadir o
   quitar. `[default: lista del sector]`.
3. **Matices léxicos** — sustituciones del Principio IV que esta guía mantiene,
   relaja o invierte. `[default: matices del sector]`.
4. **Contrato terminológico inicial** — concepto → término único que ya quieras
   fijar. `[default: vacío; se completa en /speckit-research]`.
5. **Relajaciones estructurales** — excepciones a los estándares (cajas, checklist
   por capítulo, "qué hacer en la práctica"). `[default: las que declare el sector;
   p. ej. tech relaja cajas y centraliza el checklist]`.
6. **Idioma y excepciones** — `[default: español; excepciones = citas, código,
   términos sin equivalente]`.
7. **Gobernanza / firmas** — ¿alguna pasada exige firma humana? `[default: todas
   autónomas; el control es el PDF anotado al cierre]`.

Permite reintento sin reiniciar el cuestionario. Un campo vacío = se queda el
default; nunca bloquees por dejar defaults.

### 4. Escribir las adendas

Compón el bloque de adendas a partir de `templates/adendas-template.md`,
sustituyendo los marcadores con las respuestas (o los defaults). El bloque empieza
**siempre** por el centinela `<!-- WRITEONMARS:ADENDAS -->`: es la frontera que
separa el núcleo de la capa por guía (y la que `bootstrap.py --force` usa para
re-sellar el núcleo sin perder las adendas). No lo borres ni lo dupliques.
Escríbelo en `.specify/memory/constitution.md`:

- Si ya existe el centinela, muestra el bloque como diff y pide confirmación antes
  de reemplazar **desde el centinela hasta el final**. **No toques el núcleo**
  (todo lo anterior al centinela).
- Si no existe, **añade el bloque al final** del archivo, después del núcleo.

Actualiza también `.writeonmars-manifest.json`:
- `sector`: el slug elegido.
- `registro`: el slug del registro elegido en 1b (capa 2).
- `signing_matrix`: según la respuesta de gobernanza (por defecto, sin cambios).

Fechas en ISO-8601.

## Bloqueo

Ninguno. Este paso siempre puede cerrarse con los valores por defecto: ese es el
estándar. Lo único que detiene el comando es la falta del núcleo (corre
`/speckit-setup`).

## Output

- `.specify/memory/constitution.md` con la sección "## Adendas del proyecto"
  rellena, sobre el núcleo intacto.
- `.writeonmars-manifest.json` con `sector`, `registro` (y `signing_matrix`
  si cambió).

## Después

Ya tienes la identidad normativa de la guía. Sigue con el brief:
`/speckit-specify "tema"` → `/speckit-research` → `/speckit-plan`.

## Pista corta

Si el manifiesto declara `track: corta` (`.writeonmars-manifest.json`), este paso es
**opcional**. Al crear el proyecto, `bootstrap --sector` ya dejó sector, registro y
adendas por referencia, y la brújula no pide `constitution` mientras el sector tenga
valor. El comando sigue disponible para calibrar a mano el tono, los anglicismos y los
matices cuando la pieza lo pida: si lo corres, reescribe el bloque de adendas como de
costumbre, sustituyendo la referencia por valores literales.
