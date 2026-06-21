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

## Cómo crear una guía nueva (en un comando)

El paso anterior (carpeta, `git init`, `specify init`, `preset add`, bootstrap…) está
automatizado. Para arrancar una guía desde cero:

```bash
bash tools/new-guide.sh ~/guias/context-window
```

El destino va **siempre fuera del repo del framework**: cada guía es su propio repo.
En un comando, el script: crea la carpeta y hace `git init`; corre `specify init`
(con `--here --force --ignore-agent-tools --integration <agente>` —ojo, el flag es
`--integration`, no `--ai`); instala el preset con `specify preset add --dev`; corre
`bootstrap.py` (= `speckit.setup`: constitución núcleo + manifest); cablea el contexto
multi-agente (un `AGENTS.md` canónico, con `CLAUDE.md` y `GEMINI.md` como symlinks; las
carpetas de comandos **no** se symlinkean porque los formatos difieren —Claude usa `.md`,
Gemini `.toml`); y hace el commit inicial, que es el **base ref** que Paperclip conecta.
El operador y el email se heredan de tu `git config`.

Es idempotente: puedes repetirlo sin romper nada. Flags útiles:

```bash
bash tools/new-guide.sh ~/guias/x --agents claude,gemini,codex  # 1º = primario de init
bash tools/new-guide.sh ~/guias/x --skip-init       # ya corriste `specify init` a mano
bash tools/new-guide.sh ~/guias/x --refresh-preset  # re-copia el preset en una guía ya creada
bash tools/new-guide.sh ~/guias/x --preset /ruta/al/writeonmars
bash tools/new-guide.sh ~/guias/x --operator otro.id --email otro@correo
```

Al terminar, entra en la carpeta y sigue con `/speckit-constitution` (sector + tono).

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

La capa `paperclip/` envuelve el método en una **Company de Paperclip**: una casa
editorial "Write.OnMars" (una sola, no una por guía) con un equipo de cuatro roles y
un tablero de tareas. Cada guía es un **Project** con workspace **local**
(`sourceType=local_path`: no necesita GitHub). El modelo de flujo es **una tarea por
capítulo que se mueve por estados** (no una tarea por paso). La especificación
detallada está en `paperclip/FLOW-CONTRACT.md`; el panorama, en `paperclip/README.md`.

**1. Crea la guía (base ref).** Es el scaffold del Project: lo prepara
`tools/new-guide.sh` (ver arriba), que deja el repo con el preset, la constitución
núcleo y el commit inicial. Pon los materiales fuente en `<guía>/resources/` (uno por
clase, numerados `01-`, `02-`…).

**2. Monta o sincroniza el equipo.** Paperclip se opera por su CLI `paperclipai`. La
Company y la Editora jefa (orquestadora) se crean una vez (asistente de onboarding);
los tres ejecutores se contratan —y sus bundles se (re)cargan— con:

```bash
bash paperclip/hire-team.sh                # idempotente; modelos cruzados
bash paperclip/hire-team.sh --no-headless  # modo seguro (sin saltar permisos)
```

Contrata a la **Documentalista** (research + pasada 4 de precisión + **decisión** del
ciclo; puede correr en Codex), la **Redactora** (escribe y aplica revise) y la
**Editora de mesa** (pasadas 1·2·3 + pasada 5, con un modelo **distinto** al de la
Redactora). El equipo es **permanente**: persiste entre guías. Cada rol lleva su
bundle en `paperclip/agents/<rol>/`. **Si actualizas el método**, recarga los bundles:
`hire-team.sh` recarga los tres ejecutores; la **Editora jefa** se recarga aparte
(`paperclipai agent instructions-file:put <jefa> --path HEARTBEAT.md --content-file
paperclip/agents/editora-jefa/HEARTBEAT.md`, ídem `AGENTS.md`). La jefa lleva
`maxConcurrentRuns:1` (evita el doble despacho).

**3. Conecta el Project.** Crea el Project de la guía y conéctale el repo como
workspace local; fija el goal.

**4. Arranca: fan-out único.** Crea la **tarea padre** (el libro) asignada a la
Editora jefa: eso la despierta sobre el Project. Ella avanza los pasos que son suyos
—`constitution` → `specify` (**checkpoint 1**) → `research` → `plan`— y, con plan +
research OK, hace el **fan-out ÚNICO**: **1 tarea padre + 1 hija por capítulo**
(`in_progress`, asignadas a la Redactora). No crea una tarea por estado ni por pasada.

**5. El ciclo por capítulo (peer-to-peer, sin la jefa).** Cada hija es el capítulo
entero moviéndose por estados; los workers se la pasan entre ellos:

```text
Redactora (in_progress: escribe / aplica revise)
  → in_review + Editora de mesa   (pasadas 1·2·3: estructura, utilidad, voz)
    → in_review + Documentalista   (pasada 4: precisión) → DECIDE:
        ≥1 accionable (crítico+medio) → in_progress + Redactora (revise)  ⟲
        0 accionables                 → done  (capítulo APROBADO)
```

El relevo es cambiar `status` + `assigneeAgentId` (reasignar despierta al siguiente);
el comentario de la tarea es un **puntero** a `findings.md` (la fuente de verdad), no
una copia. Severidad: **crítico+medio fuerzan revise; bajo = aviso**. El estado real
vive en disco: `python3 .../status.py --project-dir . --json` expone `by_chapter`
(por capítulo: `drafted`, `passes_done`, `revise_pending`, `approved`) y
`all_chapters_approved`.

**6. Etapas globales.** Cuando **todas** las hijas están `done`
(`all_chapters_approved`), el que cierra la última despierta a la jefa (`agent wake`),
que avanza: **pasada 5 global** (Mesa) → **export PDF** (`speckit.intro` + `export.py`)
→ **checkpoint 2** (PDF anotado: el único revisor humano, una `approval` de board) →
feedback → `close.py`.

Los **dos checkpoints humanos** no cambian: **checkpoint 1** = firmas el brief
(`specify`); **checkpoint 2** = anotas el PDF (`feedback_intake.py` lo traduce y la
Redactora aplica el re-despacho quirúrgico).

Todo es **event-driven**: los agentes se crean con `heartbeat.enabled:false` +
`wakeOnDemand:true` (sin polling ciego; ningún heartbeat por timer). No se usan
*routines* (no tienen trigger por evento) ni los campos "Reviewers/Approvers" del
issue (son del board humano; reservados al checkpoint del PDF).

## Cómo autenticar un agente Codex con tu suscripción

Si pones a la Documentalista (u otro rol) a correr en Codex con tu suscripción de
ChatGPT, ten en cuenta que Paperclip **aísla el `CODEX_HOME` por agente**: ese Codex
no ve tu `~/.codex/` y arranca sin sesión. Siémbralo enlazando tus credenciales al
`CODEX_HOME` aislado del agente:

```bash
ln -s ~/.codex/auth.json   "$CODEX_HOME/auth.json"
ln -s ~/.codex/config.toml "$CODEX_HOME/config.toml"
```

(`$CODEX_HOME` es la ruta que Paperclip asigna a ese agente.) Con el symlink, el Codex
del agente hereda tu suscripción sin copiar el secreto.

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
