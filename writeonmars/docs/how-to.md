# Guías how-to

Recetas para tareas concretas. Cada una asume que ya tienes un proyecto editorial
con el preset instalado (si no, ve al [tutorial](tutorial-primera-guia.md)).
Suponen que estás en la raíz del proyecto.

## Cómo instalar el preset en un proyecto nuevo

```bash
mkdir mi-guia && cd mi-guia && git init
specify preset add --dev /ruta/a/writing-framework/writeonmars
# o, publicado:
specify preset add --from https://github.com/MarsGotta/writing-framework/...
```

No hace falta instalar skills: la voz, la didáctica y el método viajan en el preset
(`references/`). Tras instalar, corre **una vez** `/speckit-setup` (o
`python3 .specify/presets/writeonmars/scripts/bootstrap.py`): copia el núcleo de la
constitución y crea el manifest, que el preset no puede instalar. Luego, el primer
paso del ciclo es `/speckit-constitution` (sector + tono + terminología).

## Cómo elegir el sector y ajustar la constitución del proyecto

```text
/speckit-constitution
```

El núcleo de la constitución es universal (voz, brief, revisión, neutralidad) y no
se edita por guía. Lo que sí cambia por guía vive en las **adendas del proyecto**,
que este comando rellena con un cuestionario guiado y **valores por defecto del
sector** elegido: tono calibrado, anglicismos admitidos, contrato terminológico,
relajaciones estructurales (p. ej. en tecnología, sin cajas obligatorias y checklist
centralizado) y gobernanza. Pulsa Enter para mantener el estándar; responde para
cambiarlo. Escribe `## Adendas del proyecto` sobre el núcleo intacto y guarda el
`sector` en el manifest.

Para repetirlo más tarde (cambiar de tono o de sector), vuelve a correrlo: detecta
las adendas existentes y pide confirmación antes de reemplazarlas.

## Cómo añadir un sector nuevo (veterinaria, medicina, ciencia…)

Cada sector es **un archivo** en `references/sectores/<slug>.md`. Para crear uno:

```bash
cp writeonmars/references/sectores/tecnologia.md \
   writeonmars/references/sectores/veterinaria.md
# edita las secciones del esquema (tono, anglicismos, estructura de capítulo, cajas…)
```

El esquema y las reglas están en `references/sectores/_index.md`. En cuanto el
archivo existe, `/speckit-constitution` lo ofrece como opción. No hay que tocar
código. Un sector puede activar lo que tecnología relaja (p. ej. médico/veterinario
suelen querer la caja "Síntoma → causa probable").

## Cómo escribir o rehacer un capítulo concreto

```text
/speckit-implement 3      # escribe (o REHACE) el capítulo 3
/speckit-implement        # escribe el SIGUIENTE pendiente
```

`implement` escribe UN capítulo. Con número, ese capítulo (lo rehace si ya existe en
`chapters/`); sin número, el primero del temario que aún no tiene archivo. Solo
redacta: no se revisa a sí mismo.

## Cómo revisar con otro modelo (escribe uno, revisa otro)

La revisión es independiente de la redacción. Asigna cada pasada al modelo que mejor
encaje (ejemplo sobre el capítulo 3):

```text
/speckit-review-voice 3     # voz
/speckit-review-precision 3       # hechos: research.md + verifica la fuente en vivo (web)
/speckit-review-structure 3      # estructura + utilidad
/speckit-review-global            # una vez, sobre todo el libro
/speckit-review 3                 # o las cuatro de golpe
```

Como el estado vive en archivos, el modelo revisor lee el capítulo y escribe su
bloque en `findings.md` sin depender del que lo escribió. En orquestación (Paperclip),
manda la redacción a un modelo y cada pasada a otro.

## Cómo correr la review completa en otro agente (Codex/Gemini)

Si el otro agente **no tiene los comandos registrados** (p. ej. Codex en un proyecto
inicializado para Claude), apúntale al **archivo del comando agrupado**. En Codex o
Gemini, dentro de la guía, pega un prompt así:

```text
Lee y ejecuta .specify/presets/writeonmars/commands/speckit.review.md sobre el
capítulo 1 (chapters/01-...md): corre las CUATRO pasadas leyendo cada archivo en
.specify/presets/writeonmars/commands/ (speckit.review-structure.md,
speckit.review-voice.md, speckit.review-precision.md, speckit.review-global.md) y
sus referencias (references/voz para voz, research.md para precisión, contracts/
para el formato de salida). Escribe el bloque de cada pasada en
specs/<###-feature>/findings.md según pass-output-schema (numeración: 1 estructura,
2 utilidad, 3 naturalidad, 4 precisión, 5 formato). Solo marca hallazgos, no
reescribas el texto, no finjas firma humana.
```

Para una sola pasada, apunta a su archivo (`...precision.md`) en vez del agrupado.
Después, para **aplicar** lo que marcó, usa `speckit-revise` con el modelo redactor
(o dile que lea `findings.md` y aplique los hallazgos abiertos).

Cuando registres los comandos para ese agente (ver `ROADMAP.md`), esto se reduce a
`/speckit-review 1` nativo, sin pegar rutas.

## Cómo generar el PDF con otro título o salida

```bash
python3 writeonmars/scripts/export.py \
  --title "Prompts efectivos" --subtitle "Guía rápida" \
  --eyebrow "Edición 2026" --output ~/Desktop/prompts.pdf
```

Sin flags, el título sale del brief y el nombre del archivo del título. El índice
sale siempre del temario de `plan.md`.

## Cómo exportar en Linux o en Paperclip (sin Chrome de macOS)

Indica el binario de Chromium:

```bash
python3 writeonmars/scripts/export.py --chrome chromium
# o por variable de entorno:
WOM_CHROME=chromium python3 writeonmars/scripts/export.py
```

## Cómo ver el estado de la guía

```bash
python3 writeonmars/scripts/status.py
```

Tablero de capítulos × pasadas × firmas, hallazgos por severidad y los tres gates
de cierre (críticos abiertos, firmas humanas pendientes y completitud del temario).
Es read-only: no toca nada.

## Cómo cerrar el proyecto (gate + PDF en un paso)

```bash
python3 writeonmars/scripts/close.py
```

Evalúa los gates y, si pasa, genera el PDF. Para solo comprobar sin exportar:

```bash
python3 writeonmars/scripts/close.py --no-export
```

Sale con código 1 si el proyecto está bloqueado (útil en CI o en un check de
Paperclip).

## Cómo aplicar el feedback de un PDF anotado

1. Anota el PDF (resalta y comenta). Opcional: etiqueta el comentario con
   `#voz`, `#dato`, `#estructura`, `#claridad`, `#cobertura`, `#recortar`,
   `#ampliar`, y la severidad con `#critico`, `#medio`, `#bajo`.
2. Extrae el change-set:

   ```bash
   python3 writeonmars/scripts/feedback_intake.py --pdf mi-guia.pdf
   ```

3. Aplica los cambios solo donde tocan:

   ```text
   /speckit.feedback mi-guia.pdf
   ```

El re-despacho es quirúrgico: cada cambio se ata a la frase resaltada en su
capítulo, no a la página.

## Cómo buscar en lo ya escrito (memoria)

```bash
python3 writeonmars/scripts/index.py build
python3 writeonmars/scripts/index.py query "context window" --top 5
```

Útil antes de redactar (¿este término ya se definió?) o en la pasada de precisión
(¿este dato ya tiene cita?). Reconstruye el índice tras cambios grandes.

## Cómo correr todo desatendido bajo Paperclip

Todos los scripts son deterministas y no necesitan agente, así que Paperclip puede
encadenarlos en heartbeats. El reparto humano se mantiene en los dos extremos:

1. **Checkpoint 1** — el brief con preguntas: lo resuelves tú antes de soltar la
   automatización.
2. **Centro automático** — research, redacción, pasadas locales, pasada global.
3. **Checkpoint 2** — anotas el PDF; `feedback_intake.py` lo traduce y el agente
   aplica los cambios.

Para el cierre desatendido, usa `close.py`: solo exporta si los gates pasan.

## Cómo cambiar la política de firmas

Edita `signing_matrix` en `.writeonmars-manifest.json`. **Por defecto todas las
pasadas son `autonomous`**: el control humano es el PDF anotado al final, no pasada
por pasada (las pasadas de naturalidad y precisión las hace el agente con tu voz y
las formas correctas de guía). Si una guía delicada quiere firma humana en alguna
pasada, pon `human` ahí; entonces `status.py`/`close.py` bloquean hasta que un
operador la firme. Aparte de la firma, un hallazgo `critico` abierto **siempre**
bloquea el cierre (p. ej. un dato sin fuente), sea cual sea la política.

## Cómo probar que todo funciona

Tres niveles, de lo más rápido a lo más completo.

**Smoke test (2 min, sin agente).** Monta un proyecto demo temporal y corre los
cinco scripts. No toca tu repo ni tus guías:

```bash
bash writeonmars/smoke-test.sh
```

Salta `export` si no hay Chrome y `feedback` si no hay `pymupdf`, avisando. Debe
terminar con `Smoke test correcto.`

**Sobre una guía real (solo el PDF).** Apunta `export.py` a una guía que ya
tengas para ver el motor + tu estilo con contenido de verdad:

```bash
python3 writeonmars/scripts/export.py \
  --project-dir /ruta/a/tu-guia --chapters-dir /ruta/a/tu-guia \
  --title "Título de la guía"
```

Si la guía tiene `specs/<x>/plan.md`, el índice sale del temario; si no, sale de
los `<h1>` de cada capítulo.

**Ciclo completo (con agente).** Instala el preset (`specify preset add --dev
./writeonmars`), confirma que las skills están en su sitio y corre el ciclo
`speckit.*` (ver [tutorial](tutorial-primera-guia.md)). Verifica en orden: (1)
`specify preset add` no da error y aparecen los comandos; (2) `/speckit.constitution`
te deja elegir sector y rellena las adendas; (3) `/speckit.specify` te hace las
preguntas del brief (ocho campos; el tono ya viene de las adendas); (4)
`/speckit.implement` crea `chapters/` con su `## Fuentes` por capítulo y
`findings.md`.
