# Cómo funciona Write.OnMars por dentro

Documentación interna. Explica **cómo está construido el repositorio** y **qué flujos
recorre** un proyecto editorial. Si lo que quieres es *producir una guía*, ve al
[tutorial](../writeonmars/docs/tutorial-primera-guia.md); si quieres las *razones* de
cada decisión de diseño del preset, a
[arquitectura.md](../writeonmars/docs/arquitectura.md). Esto es el plano del edificio.

Todo lo que sigue está contrastado contra el código a fecha **2026-07-10**, no contra
la documentación anterior.

## La idea, en un párrafo

Write.OnMars gobierna a un agente de IA para que escriba como una autora
especializada. No es un modelo ni una aplicación: es un **método empaquetado como
preset de Spec Kit**. El método viaja en documentos que cualquier modelo puede leer
(comandos y referencias), lo que hay que calcular sin ambigüedad viaja en scripts de
Python, y las reglas innegociables viven en una constitución versionada. Encima de
todo eso, opcional, hay un **ejecutor** que recorre el ciclo solo, repartiendo cada
paso entre modelos distintos.

La consecuencia práctica: puedes correr el método a mano con un agente delante, o
dejar que el ejecutor lo haga desatendido, y **es el mismo método**. No hay dos
pipelines que mantener.

## Las cuatro capas

```
   ┌──────────────────────────────────────────────────────────┐
   │  GOBIERNO      constitución v1.7.0 + contracts/          │  ← qué no se puede romper
   ├──────────────────────────────────────────────────────────┤
   │  MÉTODO        writeonmars/commands/ + references/       │  ← lo que lee el modelo
   ├──────────────────────────────────────────────────────────┤
   │  DETERMINISMO  writeonmars/scripts/*.py                  │  ← lo que no necesita modelo
   ├──────────────────────────────────────────────────────────┤
   │  EJECUCIÓN     a mano (un agente)  │  vivarium/ (Rust)   │  ← quién mueve la manivela
   └──────────────────────────────────────────────────────────┘
```

La regla que sostiene el reparto: **si una tarea no necesita criterio, no la hace un
modelo**. Leer `findings.md`, evaluar los gates de cierre, ensamblar un PDF o extraer
las anotaciones de un PDF es código. El agente entra donde sí aporta, que es redactar
y revisar con voz.

## Mapa del repositorio

| Directorio | Qué es | Estado |
|---|---|---|
| `writeonmars/` | **El preset.** La unidad instalable: comandos, scripts, referencias, contratos, plantillas | Activo — el foco |
| `vivarium/` | El ejecutor orquestado, en Rust. Dos crates: `vivarium-core` (dominio) y `vivarium-cli` (binario headless) | Activo — ejecutor de referencia |
| `tests/` | `unit/` (pytest), `smoke/` (end-to-end con stubs), `fixtures/`, `lib/`, `editorial-pilot/evidence/` | Activo — es el gate |
| `docs/` | Lo transversal del repo y los docs de producto de Vivarium (`vivarium.md` es su fuente de verdad) | Activo |
| `specs/` | Las seis specs de Spec Kit (001–006). Ninguna activa; valen como registro de diseño | Referencia |
| `tools/` | `new-guide.sh`: monta un proyecto editorial entero en un comando | Activo |
| `mcp/` | Servidor MCP de research, opcional | Activo |
| `paperclip/` | El ejecutor anterior | **Archivado** (2026-07-07) |
| `contracts/` (raíz) | Punteros. La fuente única es `writeonmars/contracts/` | No editar |
| `_to_delete/` | Basura pendiente de borrar (instalador legacy, locks huérfanos) | A borrar |

Un detalle que confunde a quien llega: **este repo no es un proyecto editorial**. Aquí
vive el método. Cada guía o artículo que escribas es *otro repositorio*, donde instalas
el preset.

## El preset por dentro

### Comandos (18)

Son archivos markdown en `writeonmars/commands/`. Cada uno es un guion que el agente
lee y ejecuta. Se agrupan en cuatro familias:

- **Arranque**: `setup` (bootstrap), `constitution` (las adendas del proyecto).
- **Ciclo**: `specify` (el brief), `research` (las fuentes), `plan` (el temario),
  `implement` (redactar un capítulo), `intro` (el README de presentación).
- **Revisión**: `review` (agrupado) y los cuatro sueltos —`review-structure`,
  `review-voice`, `review-precision`, `review-global`— más `revise`, que aplica al
  texto los hallazgos abiertos.
- **Operación**: `status`, `export`, `feedback`, `close`, `memory`.

Están en comandos y no en *skills* de un proveedor a propósito: una skill de Claude no
la lee Codex. Un comando en markdown lo lee cualquiera.

### Scripts (9 + una librería)

En `writeonmars/scripts/`. Deterministas, sin modelo, casi todo con la librería
estándar:

| Script | Para qué |
|---|---|
| `bootstrap.py` | Crea el manifiesto y copia la constitución. Lo único que un preset no puede instalar solo |
| `status.py` | **La brújula.** Lee el estado del disco y dice qué toca ahora |
| `export.py` | Ensambla el PDF (pandoc + Chrome headless) |
| `close.py` | Encadena el gate de cierre y el export |
| `feedback_intake.py` | Convierte un PDF anotado en un change-set quirúrgico |
| `dispose.py` | Registra decisiones humanas sobre hallazgos (solo en modo estudio) |
| `track.py` | Único camino para cambiar de pista de ceremonia |
| `authorship.py` | Informe de autoría humana frente a IA, cruzando git y `decisions.jsonl` |
| `index.py` | Memoria de búsqueda sobre lo ya escrito |
| `findings_lib.py` | Librería compartida (parser de `findings.md`, manifiesto, temario) |

`dispose.py` y `track.py` comparten un rasgo poco habitual: **exigen identidad humana**.
Leen `git config`, y si el nombre o el correo huelen a agente (`@agents.writeonmars.invalid`)
se niegan a actuar. Hay decisiones que un modelo no puede tomar por ti.

### Referencias: la pirámide de prosa

En `writeonmars/references/`. Son las reglas de escritura, neutrales de modelo. La
prosa se construye en **tres capas que se apilan**:

```
        ╱ voz ╲           capa 3 · references/voz/       léxico, humor, cierres
      ╱─────────╲                                        (marcela-prose)
    ╱  registro   ╲       capa 2 · references/registros/ formalidad, densidad, figuras
  ╱─────────────────╲                                    (tecnico-divulgativo)
╱    prosa-base       ╲   capa 1 · references/prosa/     cohesión y fluidez
────────────────────────                                 SIEMPRE ACTIVA
```

La capa 1 es innegociable y siempre está encendida: frases completas y progresión de lo
conocido a lo nuevo. La capa 2 la declara el manifiesto (campo `registro`) y fija el
contrato del género. La capa 3 es la voz de la autora.

Cuando chocan, el orden de precedencia está escrito: **la voz gana en sabor, el registro
gana en formalidad y densidad, y a la prosa-base no la deroga nadie** en sus dos
innegociables.

Junto a ellas viven `didactica/` (diseño de la guía), `metodo/` (14 documentos, uno por
paso) y `sectores/` (los valores por defecto de cada dominio; hoy solo `tecnologia`).
Añadir un sector nuevo es crear un archivo, sin tocar código.

### Contratos

`writeonmars/contracts/` es la **fuente única**. Todo lo demás que parezca un contrato
es un puntero.

| Contrato | Versión | Qué fija |
|---|---|---|
| `manifest-schema.json` | v1.4.0 | Los campos del `.writeonmars-manifest.json` |
| `pass-output-schema.md` | v1.2 | La forma de un bloque de pasada en `findings.md` |
| `citation-contract.md` | v1.0 | Cómo se cita una fuente |
| `executor-contract.md` | v1.0 | Qué debe cumplir cualquier ejecutor |

Más tres esquemas JSON: `citation-record`, `claim-record` y `disposition-record`.

### El manifiesto

`.writeonmars-manifest.json`, en la raíz de cada proyecto editorial. Los campos que
gobiernan el comportamiento:

- **`mode`** (`produccion` | `estudio`) — *quién escribe la prosa*. Ausente = producción.
- **`track`** (`estandar` | `corta`) — *cuánto rito*. Ausente = estándar.
- **`sector`** y **`registro`** — qué defaults de dominio y qué capa 2 de la pirámide.
- **`signing_matrix`** — qué pasadas exigen firma humana. Por defecto, las cinco autónomas.
- **`quality_gates`** — opcional; activa el gate de factualidad.
- **`mode_history`** y **`track_history`** — append-only, con la fecha del cambio.
  `track_history` guarda además el `actor` humano; `mode_history` todavía no (deuda anotada).

`mode` y `track` son **ortogonales**: gobiernan cosas distintas y se combinan libremente.

## La brújula: `status.py`

Es la pieza que hace barato todo lo demás. `status.py --json` lee el estado del disco
—el manifiesto, los archivos de `chapters/` contra el temario, `findings.md`,
`claims.md`— y responde a una pregunta: **¿qué toca ahora?** No guarda memoria, no
razona sobre prosa, no llama a ningún modelo. Se le pregunta otra vez y vuelve a mirar
el disco.

Ese campo se llama `next_step`, y es lo que permite que un orquestador delegue sin
acumular en su contexto el ruido de la redacción.

### La máquina de estados

Son guardas secuenciales: **gana la primera que se cumple** (`status.py:368-449`).

| Si… | `next_step` |
|---|---|
| no hay manifiesto ni constitución | `setup` |
| el sector está sin fijar | `constitution` |
| no hay `spec.md` | `specify` |
| no hay `research.md` | `research` |
| el temario está vacío | `plan` |
| faltan capítulos por escribir | `implement` · en estudio, `write` |
| hay capítulos pero ningún `findings.md` | `review` |
| quedan hallazgos accionables | `revise` · en estudio, `dispose` |
| hay capítulos reabiertos, firmas pendientes o factualidad en rojo | `review` |
| todos los gates en verde | `close` |

El camino feliz, en producción y pista estándar:

```
setup → constitution → specify → research → plan → implement → review → revise → close
                                     ▲                    │
                                     │                    │  (por capítulo)
                                     └────────────────────┘
```

### Los gates de cierre

| Gate | Comprueba |
|---|---|
| `g1 no_open_criticals` | Cero hallazgos críticos abiertos |
| `g2 human_signatures` | Ninguna pasada que exija firma humana está firmada como autónoma |
| `g3 guide_complete` | Hay tantos capítulos como filas en el temario |
| `g4 factuality` | *Opcional.* Solo si el manifiesto declara `quality_gates.factuality_min` |

`closeable = g1 ∧ g2 ∧ g3` (y `g4` cuando está en modo `blocking`). El índice de
factualidad se calcula sin modelo, contando en `claims.md` cuántas afirmaciones
verificables acabaron soportadas.

### Severidad: qué bloquea qué

Aquí es donde la documentación se desfasa con facilidad, así que conviene ser exacto.
El contrato dice «solo `critico` bloquea el cierre», y es verdad **del flag `closeable`
en producción**. Pero la brújula frena antes:

| Severidad | ¿Desvía `next_step` a `revise`/`dispose`? | ¿Baja `closeable` en producción? | ¿Y en estudio? |
|---|---|---|---|
| `critico` | Sí | **Sí** (tumba `g1`) | Sí |
| `medio` | **Sí** | **No** — no toca ningún gate | **Sí** (vía `all_chapters_approved`) |
| `bajo` | No, es un aviso | No | No |

Dicho de otro modo: en producción, un hallazgo `medio` abierto no te impide cerrar, pero
la brújula te mandará a `revise` antes de dejarte llegar a `close`. En estudio sí baja
`closeable`, porque allí el cierre se ancla a que cada capítulo esté aprobado.

## Los tres flujos

### Pista estándar, modo producción

El ciclo completo. La IA redacta cada capítulo (`implement`), otro modelo lo revisa en
cuatro relevos y `revise` aplica los hallazgos. Sobre una pieza de un capítulo cuesta
**11 despachos**.

Las cinco dimensiones del Principio V se reparten así:

| Pasada | Dimensión | Comando | Rol |
|---|---|---|---|
| 1 y 2 | Estructura y utilidad | `review-structure` (un run, dos bloques) | editora de mesa |
| 3 | Naturalidad | `review-voice` | editora de mesa |
| 4 | Precisión | `review-precision` | **documentalista** |
| 5 | Formato y coherencia | `review-global` (una vez, sobre el libro) | editora de mesa |

La pasada 4 va siempre aparte, con otro rol y otro modelo, por una regla dura:
**voz ≠ precisión**. Pulir prosa y contrastar datos son tareas opuestas que se degradan
al mezclarse.

### Pista corta (`track: corta`)

Para una **pieza única**: un artículo, un post, un ensayo. Mismo rigor, menos ceremonia.
Cuesta **6 despachos**: `research`, `implement`, `review-1` (combinada), `review-4`
(precisión), `export`, `close`.

Lo elegante del diseño es cómo se consigue. **`status.py` no sabe nada de la pista**: no
hay ni una rama por `track` en la máquina de estados. Los pasos desaparecen *por
construcción*:

- **`plan` se salta solo** porque al firmar el brief, `speckit.specify` ya escribe un
  temario de una sola fila. Como `chapters_expected == 1`, la guarda del temario vacío
  nunca se dispara.
- **`constitution` se salta** porque `bootstrap --sector` dejó el sector fijado, y la
  guarda del sector mira si es nulo.
- **`intro` se auto-anula** en el propio comando: una pieza única no tiene README de
  presentación.
- **`review-3` y `review-5`** no se despachan sueltas porque las registra la *pasada
  combinada*.

La **pasada combinada** viaja en el despacho de la pasada 1 y registra en un solo run
cuatro bloques —dimensiones 1, 2, 3 y 5—. La precisión nunca se absorbe ahí: sigue en su
relevo, con otro modelo. Si la combinada se queda a medias, `review-voice` y
`review-global` siguen disponibles como red de reparación.

Lo único que `status.py` hace con `track: corta` es emitir **avisos** si el temario creció
por encima de una fila. No toca `next_step`, ni los gates, ni `closeable`.

Si la pieza pide crecer, `track.py --escalar` la asciende a estándar **sin mover un solo
archivo**: la pieza ya es el capítulo 1, los hallazgos y las claims siguen valiendo. Exige
identidad humana. El camino inverso solo es legal mientras siga siendo una pieza única.

### Modo estudio (`mode: estudio`)

Para cuando **la prosa la escribe la persona**. La IA revisa, anota y acompaña; no redacta
capítulos ni aplica correcciones. El ciclo cambia en cuatro puntos:

- Donde había `implement`, aparece el checkpoint **`write`**: te toca a ti.
- Donde había `revise`, aparece **`dispose`**: los hallazgos esperan tu decisión, que
  registras con `dispose.py` (aceptar, rechazar con motivo, o aplazar).
- Cada bloque de pasada guarda una **huella sha256** del capítulo revisado. Si el capítulo
  cambia después, la pasada se invalida y el capítulo se reabre.
- `authorship.py` emite un informe de autoría cruzando los commits de git con las ventanas
  de despacho de `decisions.jsonl`. Si aparece prosa comiteada por un agente, el veredicto
  lo dice.

### La matriz

Pista y modo son ortogonales. Las cuatro combinaciones son legales:

|  | `produccion` | `estudio` |
|---|---|---|
| **`estandar`** | La IA escribe un libro | Tú escribes un libro, la IA revisa |
| **`corta`** | La IA escribe una pieza | Tú escribes una pieza, la IA revisa |

## Vivarium: el ejecutor

`vivarium/` es un binario headless en Rust que recorre el ciclo solo. No sustituye al
método: lo **conduce**.

```bash
vivarium new mi-guia --kind guia   # crea el proyecto (git, specify, preset, bootstrap)
vivarium check                     # valida entorno y config, sin ejecutar nada
vivarium run                       # avanza hasta que necesita a un humano
vivarium mode set estudio --yes    # cambia de modo, con registro
```

### Los códigos de salida son la interfaz

`vivarium run` no imprime «espera aquí»: **sale con un código**, y eso lo hace
scriptable.

| Código | Significa |
|---|---|
| `0` | Progresó, o el proyecto quedó cerrado |
| `10` | **Checkpoint humano.** El flujo espera algo tuyo (firmar el brief, escribir un capítulo, anotar el PDF) |
| `11` | Guardarraíl de modo: se pretendía despachar prosa de manuscrito estando en estudio |
| `12` | Un despacho falló (el agente devolvió error, o no dejó el efecto esperado en disco) |
| `2` `3` `4` `5` `6` | Uso inválido · falta un binario · falta confirmación · validación · el lock está tomado |

El **10** es una espera legítima; el **11** es una red de seguridad que en el camino feliz
nunca se dispara, porque los pasos de prosa en estudio ya se convierten en checkpoint
antes de llegar ahí.

### BYOM: un modelo por rol

`.vivarium/config.toml` asigna un CLI a cada rol. Vivarium no habla con ninguna API: lanza
procesos.

```toml
version = 1
[roles.redactora]
command = ["claude", "-p", "--permission-mode", "acceptEdits"]
stdin = "prompt_file"
[roles.editora_mesa]
command = ["codex", "exec", "--cd", "{project_dir}", "--sandbox", "workspace-write", "-"]
stdin = "prompt_file"
[roles.documentalista]
command = ["codex", "exec", "--cd", "{project_dir}", "--sandbox", "workspace-write", "-"]
stdin = "prompt_file"
```

El reparto de pasos entre roles está cableado en Rust:

| Rol | Pasos |
|---|---|
| `redactora` | `plan`, `implement`, `revise`, `intro` |
| `editora_mesa` | `review-1`, `review-2`, `review-3`, `review-5` |
| `documentalista` | `constitution`, `research`, `review-4` |
| `sidecar` | `setup`, `export`, `close` (scripts de Python, sin modelo) |

Que la redactora y la editora de mesa apunten a **modelos distintos** no es una
preferencia: es lo que hace cumplir «escribe uno, revisa otro».

### Cómo sabe que un paso funcionó

Después de cada despacho, Vivarium no se fía de que el agente diga «hecho»: comprueba el
**efecto en disco** (`effect_satisfied`). Que `implement` dejó el capítulo escrito, que
`review-N` añadió su bloque a `findings.md`, que `export` produjo un PDF.

Cada acción deja dos líneas en `decisions.jsonl`: un `dispatch` al empezar y una
`disposition` al acabar (`ok`, `revise` o `failed`). Si el proceso muere a mitad, queda un
`dispatch` huérfano. Al relanzar, la **reconciliación** lo resuelve mirando el disco: si el
efecto está, lo cierra como `ok`; si no está, lo cierra como `failed` y lo vuelve a
despachar. Un runner interrumpido nunca deja el proyecto bloqueado.

Dos runners a la vez tampoco pueden coexistir: `.vivarium/lock` es un lock advisory no
bloqueante, y el segundo sale limpio con código 6.

## La frontera dura

Esta es la regla de arquitectura más importante del repo:

> **Vivarium solo habla con el método a través de archivos, scripts y comandos.**

Nunca calcula estado editorial por su cuenta. Cuando quiere saber qué toca, ejecuta
`status.py --json` y deserializa la respuesta. Cuando quiere exportar, invoca `export.py`.

El reparto exacto, que conviene tener claro: **la verdad de estado la produce `status.py`**
(`next_step`, `by_chapter`, `closeable`); **el mapeo de cada paso a un rol y un despacho lo
conoce Vivarium** en Rust. Deriva del método *qué* toca ahora, y sabe por su cuenta *cómo*
despacharlo.

El beneficio prometido: mientras la frontera aguante, sacar `vivarium/` a su propio
repositorio es mover carpetas, no refactorizar.

## Las reglas que nunca se rompen

Vienen de la constitución (v1.7.0) y las verifica el código, no la buena voluntad:

1. **Escribe uno, revisa otro.** Quien redacta un capítulo no lo revisa. El reparto de
   roles de Vivarium lo hace estructural.
2. **Voz ≠ precisión.** La pasada de precisión corre siempre con otro rol y otro modelo,
   incluso en pista corta, donde todo lo demás se fusiona.
3. **Dos checkpoints humanos.** Firmas el brief al arrancar y anotas el PDF al cerrar. El
   centro corre solo.
4. **Un crítico abierto bloquea el cierre.** Siempre, en cualquier modo y cualquier pista.
5. **La precisión abre la fuente en vivo.** No basta con confiar en `research.md`: una cita
   pudo envejecer entre la investigación y la redacción.
6. **Ningún agente cambia `track` ni dispone hallazgos.** Esos scripts exigen identidad
   humana y rechazan las de agente.

## Cómo se verifica

Tres gates, los tres obligatorios antes de commitear y los tres en CI
(`.github/workflows/ci.yml`):

```bash
uvx --with pytest --with pyyaml --with jsonschema python -m pytest tests/unit -q
bash tests/smoke/run-all.sh
cd vivarium && cargo test --workspace
```

> Si el `python3` de tu sistema no trae pytest, el primer comando falla. Usa la forma con
> `uvx` de arriba.

Los **unitarios** (218, en 10 módulos) cubren cada script. Los **smoke** recorren proyectos
reales de punta a punta con agentes falsos:

| Smoke | Qué demuestra |
|---|---|
| `test-factuality.sh` | El índice de factualidad y el gate g4, con retrocompatibilidad |
| `vivarium-e2e.sh` | El ciclo completo bajo el ejecutor |
| `estudio-e2e.sh` | Que en modo estudio la IA no redacta manuscrito |
| `corta-e2e.sh` | Que la pista corta cuesta 6 despachos, que voz ≠ precisión y que escalar no mueve archivos |

Los stubs son deterministas: no hacen falta agentes, ni pandoc, ni Chrome. La contrapartida
es que **un stub no puede falsar que un modelo real entienda un comando**. Para eso está la
validación BYOM, cuya evidencia se commitea en
`tests/editorial-pilot/evidence/<fecha>-<slug>/`.

## Qué está archivado

- **`paperclip/`** — fue el ejecutor orquestado; archivado el 2026-07-07. Su
  `FLOW-CONTRACT.md` (§§ 0-2) sobrevive como el contrato agnóstico que Vivarium implementa.
- **Spec `002-wom-cli`** — superseded. El CLI `wom` se descartó: `status.py` y `close.py`
  cubren su función.
- **`install.sh`** — retirado del árbol el 2026-07-09. La vía canónica es el preset.
- **Copias de las skills** en `.claude/skills/` y `.agents/skills/` — retiradas el
  2026-07-09 porque habían divergido. Fuente única: `writeonmars/references/`.

## Dónde seguir

- **Producir una guía**: [tutorial](../writeonmars/docs/tutorial-primera-guia.md).
- **Las razones de diseño del preset**: [arquitectura.md](../writeonmars/docs/arquitectura.md).
- **Comandos, flags y esquemas**: [referencia.md](../writeonmars/docs/referencia.md).
- **Contrato para el agente que ejecuta el método**: [AGENTS.md](../writeonmars/AGENTS.md).
- **El ejecutor**: [vivarium/README.md](../vivarium/README.md) · producto en [vivarium.md](vivarium.md).
- **Estado y qué queda**: [ROADMAP.md](../ROADMAP.md).
