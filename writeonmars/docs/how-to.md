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
Gemini `.toml`); y hace el commit inicial, que queda como **base ref** del proyecto.
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
bloque en `findings.md` sin depender del que lo escribió. En orquestación (Vivarium),
cada rol declara su propio CLI, así que la redacción va a un modelo y las pasadas a otro.

## Cómo correr la review completa en otro agente (Codex/Gemini)

Si el otro agente **no tiene los comandos registrados** (p. ej. Codex en un proyecto
inicializado para Claude), apúntale al **archivo del comando agrupado**. En Codex o
Gemini, dentro de la guía, pega un prompt así:

```text
Lee y ejecuta .specify/presets/writeonmars/commands/speckit.review.md sobre el
capítulo 1 (chapters/01-...md): corre las CUATRO pasadas leyendo cada archivo en
.specify/presets/writeonmars/commands/ (speckit.review-structure.md,
speckit.review-voice.md, speckit.review-precision.md, speckit.review-global.md) y
sus referencias (references/prosa para el hilo, references/registros/<registro>
para el registro del manifiesto, references/voz para la voz, research.md para
precisión, contracts/ para el formato de salida). Escribe el bloque de cada pasada en
specs/<###-feature>/findings.md según pass-output-schema (numeración: 1 estructura,
2 utilidad, 3 naturalidad, 4 precisión, 5 formato). Solo marca hallazgos, no
reescribas el texto, no finjas firma humana.
```

Para una sola pasada, apunta a su archivo (`...precision.md`) en vez del agrupado.
Después, para **aplicar** lo que marcó, usa `speckit-revise` con el modelo redactor
(o dile que lea `findings.md` y aplique los hallazgos abiertos).

Cuando registres los comandos para ese agente (ver `ROADMAP.md`), esto se reduce a
`/speckit-review 1` nativo, sin pegar rutas.

El mismo patrón vale para **cualquier comando del ciclo**, no solo la review: cada
`speckit.*.md` de `.specify/presets/writeonmars/commands/` es un prompt plano en
markdown que cualquier agente puede leer y ejecutar. Antes del primer comando, el
agente debe leer el contrato (`.specify/presets/writeonmars/AGENTS.md`): ahí están
las reglas de neutralidad y qué referencia cargar en cada paso. Ejemplo con la
redacción en un agente cualquiera:

```text
Lee .specify/presets/writeonmars/AGENTS.md (contrato) y ejecuta
.specify/presets/writeonmars/commands/speckit.implement.md sobre el capítulo 2:
carga la pirámide de prosa (references/prosa, references/registros/<registro> del
manifiesto, references/voz), el temario en specs/<###-feature>/plan.md y el
research.md, y escribe chapters/02-...md según la plantilla de capítulo.
```

La sintaxis `/speckit-x` de los ejemplos de esta guía es solo el atajo de Claude:
el comando real es siempre el fichero markdown, igual para todos los agentes.

## Cómo generar el PDF con otro título o salida

```bash
python3 writeonmars/scripts/export.py \
  --title "Prompts efectivos" --subtitle "Guía rápida" \
  --eyebrow "Edición 2026" --output ~/Desktop/prompts.pdf
```

Sin flags, el título sale del brief y el nombre del archivo del título. El índice
sale siempre del temario de `plan.md`.

## Cómo exportar en Linux (sin Chrome de macOS)

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

Sale con código 1 si el proyecto está bloqueado (útil en CI o en un check previo al
cierre).

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

## Cómo correr todo desatendido con Vivarium

**Vivarium** (`vivarium/`) es el ejecutor orquestado de referencia: un binario headless
en Rust que recorre el ciclo solo, lanzando un CLI de agente por rol editorial. No
sustituye al método, lo conduce: cuando quiere saber qué toca, ejecuta `status.py --json`.

**1. Crea el proyecto.** Con el ejecutor, en un solo comando:

```bash
vivarium new ~/Projects/mi-guia --kind guia --preset ~/Projects/writing-framework/writeonmars
```

Para una **pieza única**, declara la pista y el sector con variables de entorno
(no con el flag `--sector` del ejecutor; ver el aviso más abajo):

```bash
WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia \
  vivarium new ~/Projects/mi-articulo --kind guia --preset ~/Projects/writing-framework/writeonmars
```

Pon los materiales fuente en `<proyecto>/resources/` (uno por clase, numerados `01-`, `02-`…).

**2. Declara tus modelos (BYOM).** En `.vivarium/config.toml`, un CLI por rol. Vivarium
lanza esos binarios como subprocesos, **heredando tu entorno**: si ya tienes sesión
iniciada en `claude` o en `codex`, funcionan sin configurar credenciales.

```toml
version = 1
[roles.redactora]                                  # plan, implement, revise, intro
command = ["claude", "-p", "--permission-mode", "acceptEdits"]
stdin = "prompt_file"
[roles.editora_mesa]                               # pasadas 1, 2, 3 y 5
command = ["codex", "exec", "--cd", "{project_dir}", "--sandbox", "workspace-write", "-"]
stdin = "prompt_file"
[roles.documentalista]                             # constitution, research, pasada 4
command = ["codex", "exec", "--cd", "{project_dir}", "--sandbox", "workspace-write", "-"]
stdin = "prompt_file"
```

Que la **redactora** y la **editora de mesa** apunten a modelos distintos no es una
preferencia: es lo que hace estructural el `writer ≠ reviewer`. Y la **documentalista**
(precisión) debe ser distinta de la editora de mesa, por la regla `voz ≠ precisión`.

Los `setup`, `export` y `close` no llevan rol: son scripts de Python (*sidecar*), sin modelo.

**3. Valida antes de gastar tokens.**

```bash
vivarium check      # manifiesto, config BYOM y binarios de cada rol; no ejecuta nada
```

**4. Corre el ciclo.**

```bash
vivarium run        # avanza hasta que necesita a un humano
```

Lee el **código de salida**, que es la interfaz:

| Código | Qué significa | Qué haces |
|---|---|---|
| `0` | Progresó, o el proyecto quedó cerrado | Nada, o vuelve a lanzarlo |
| `10` | **Checkpoint humano** | Firma el brief, escribe el capítulo o anota el PDF, y relanza |
| `11` | Guardarraíl de modo estudio | Revisa por qué se intentó despachar prosa de manuscrito |
| `12` | Un despacho falló | Mira `decisions.jsonl`; el disco quedó intacto, es seguro reintentar |
| `6` | Otro runner tiene el lock | Espera a que termine |

`vivarium step` hace un solo paso, útil para depurar. `vivarium status` imprime el estado
combinado (el de `status.py`, más el modo y los despachos en vuelo) sin efectos laterales.

**5. Los dos checkpoints humanos no cambian.** El **1** es firmar el brief; el **2**,
anotar el PDF. Entre ellos, el ejecutor no te necesita.

### Si un despacho se interrumpe

No pasa nada: relanza `vivarium run`. Al arrancar, la **reconciliación** revisa los
despachos que quedaron sin cerrar y mira el disco. Si el efecto está (el capítulo se
escribió, el bloque llegó a `findings.md`), lo cierra como `ok`; si no está, lo cierra
como `failed` y lo vuelve a despachar. Un runner muerto nunca deja el proyecto bloqueado.

> **Aviso: `vivarium new --sector` no hace lo que parece.** Escribe el sector en el
> manifiesto *después* del bootstrap, así que el proyecto se queda con sector pero **sin
> adendas y sin registro**: la brújula deja de pedir `constitution` y la capa 2 de la
> pirámide de prosa nunca se materializa. Usa `WRITEONMARS_SECTOR` (y `WRITEONMARS_TRACK`),
> que sí llegan a `bootstrap.py`. Está anotado en el ROADMAP como deuda del ejecutor.

El detalle interno del ejecutor está en [`../../docs/como-funciona.md`](../../docs/como-funciona.md)
y en [`../../vivarium/README.md`](../../vivarium/README.md).

> **Nota histórica.** El primer ejecutor orquestado corrió sobre **Paperclip** (una
> Company con cuatro roles y un tablero de tareas). Quedó **archivado** el 2026-07-07:
> vive en `paperclip/`, y sus §§ 0-2 de `FLOW-CONTRACT.md` son el contrato agnóstico del
> ejecutor que Vivarium implementa. Si vienes de aquel montaje, `hire-team.sh` y los
> bundles de `paperclip/agents/` ya no se usan.

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
