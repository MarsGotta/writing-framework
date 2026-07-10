# Arquitectura y decisiones

Por qué el preset está montado así. Esto no enseña a usarlo (para eso está el
[tutorial](tutorial-primera-guia.md)) ni describe el repositorio pieza a pieza (para
eso, [cómo funciona por dentro](../../docs/como-funciona.md)): explica las
**decisiones** para quien lo mantiene o lo extiende.

## Un método, dos ejecutores

El método editorial es uno solo: el ciclo Spec Kit en modo editorial más las
referencias de voz y método. Se ejecuta de dos formas, con el mismo código debajo:

- **Directo**: tú con un agente y los comandos `speckit.*`. Para piezas donde
  quieres mimar la voz.
- **Orquestado**: **Vivarium** (`vivarium/`, Rust headless) recorre el ciclo solo,
  lanzando un CLI de agente por rol. Para producir sin estar delante.

No hay dos pipelines que mantener: el ejecutor envuelve el mismo método. Por eso los
scripts son deterministas y no asumen un agente delante.

## La capa de orquestación: el equipo y el reparto

El ejecutor orquestado de referencia es **Vivarium** desde el 2026-07-07. Paperclip
fue el primer corte y queda **archivado** en `paperclip/`; sus §§ 0-2 de
`FLOW-CONTRACT.md` sobrevivieron como el contrato agnóstico del ejecutor, que es
justo lo que Vivarium implementa.

La decisión que sostiene la capa es de **reparto**: el equipo son cuatro roles
agrupados **por oficio**, no una tarea por paso. Agrupar por oficio da menos relevos y
un contexto coherente por rol. Y ese reparto es justo el que preserva las reglas duras
del método —escribe uno, revisa otro (`writer ≠ reviewer`); voz separada de precisión;
detector distinto de corrector—, a nivel de roles y modelos cruzados en vez de a nivel
de pasada:

- **Documentalista**: `constitution`, `research` y la pasada 4 (precisión). Corre en
  otro proveedor (p. ej. Codex) para reforzar la independencia frente a quien escribe.
- **Redactora**: `plan`, `implement`, `revise` e `intro`.
- **Editora de mesa**: pasadas 1, 2, 3 y 5, con un modelo **distinto** al de la
  Redactora.
- **Sidecar**: `setup`, `export` y `close` — los scripts de Python, sin modelo.

Ese mapeo de paso a rol vive cableado en el runner (`vivarium-core/src/runner.rs`), y
los binarios concretos los declara el proyecto en `.vivarium/config.toml` (BYOM: un
CLI por rol). Que la Redactora y la Editora de mesa apunten a modelos distintos no es
una preferencia de estilo; es lo que hace estructural el `writer ≠ reviewer`.

La pieza que hace todo esto barato es `status.py --json`. El ejecutor **no razona sobre
prosa**: sigue `next_step`, calculado desde el estado en disco (el manifest, `chapters/`
contra el temario, `findings.md`). El estado por capítulo lo expone `by_chapter`
(`drafted`, `passes_done`, `revise_pending`, `approved`) —que también deja el ciclo
seguible por un solo agente sin ejecutor—, y `all_chapters_approved` es la señal de que
tocan las etapas globales. Es la **brújula del flujo**: una máquina de estados sin
memoria, que delega y vuelve a leer del disco en vez de acumular en su contexto el
ruido de la redacción.

Política de severidad: **crítico y medio desvían la brújula a `revise`; bajo es aviso**.
Solo el crítico baja `closeable` en producción (ver «Gates de cierre» en la referencia).

### La frontera dura

Vivarium habla con el método **solo por archivos, scripts y comandos**. Nunca computa
estado editorial propio: cuando quiere saber qué toca, ejecuta `status.py --json`. El
reparto exacto es que **la verdad de estado la produce el método** y **el cómo
despachar cada paso lo conoce el ejecutor**. Mientras esa frontera aguante, sacar
`vivarium/` a su propio repositorio es mover carpetas, no refactorizar.

El detalle del ejecutor está en `vivarium/README.md` y en
[`docs/como-funciona.md`](../../docs/como-funciona.md).

## Agente-agnóstico: la lógica en comandos, no en skills

El pipeline lo lanzan distintos agentes con distintos modelos, no solo Claude. Por
eso la lógica NO vive en skills de Claude (que se autodisparan y son de un
proveedor), sino en **comandos** del preset (`speckit.*`) y **referencias**
neutrales (`references/prosa`, `references/registros`, `references/voz`,
`references/didactica`, `references/metodo`) que cualquier modelo lee y
aplica. La prosa forma una pirámide de tres capas: `references/prosa` es la
base (cohesión y fluidez, siempre activa), `references/registros/<slug>` es
la capa 2 (el contrato del género, declarado en manifiesto y adendas;
disponible `tecnico-divulgativo`) y `references/voz` es la cúspide (voz de
la autora). Es el modelo del preset de ficción, que no usa
skills. El contrato para el agente está en `AGENTS.md`.

Reparto:

- **Preset** (`specify preset add`): plantillas + comandos + scripts + referencias.
  Es la unidad que instalas; lleva el qué, el cómo y la voz.
- **Proyecto**: solo su `.writeonmars-manifest.json` y los hooks de git (un preset
  no puede registrar hooks; eso sería una extensión aparte).

`marcela-prose` y `technical-guide-design` pueden seguir como skills globales para
tu trabajo a mano, pero el pipeline no depende de ellas: usa sus copias en
`references/`. Mantenimiento: si actualizas la voz en `mars-voice`, re-sincroniza
`references/voz/`.

## Constitución por capas: núcleo + adendas + sectores

Una guía nueva no debería tener una constitución *clonada y editable*: si cada guía
puede tocar las reglas, se pierde lo que hace que todas suenen igual de bien. Pero
tampoco una constitución idéntica para todas: una guía de desarrollo web no escribe
como una de veterinaria. La solución son tres niveles, no dos:

- **Núcleo** (versionado, en el preset): voz, brief, revisión, neutralidad,
  gobernanza. Universal. `speckit.setup` lo copia; nadie lo edita por guía. Cuando
  el método evoluciona, sube de versión y `bootstrap.py --force` lo re-sella en cada
  guía **sin tocar las adendas** (la frontera es el centinela
  `<!-- WRITEONMARS:ADENDAS -->`). Así las enmiendas se propagan por versión, no
  parcheando N copias.
- **Adendas del proyecto** (por guía, normativas): sector, tono calibrado, contrato
  terminológico, anglicismos, relajaciones, gobernanza. Las fija
  `speckit.constitution` y la revisión las verifica.
- **Brief** (`spec.md`, descriptivo): audiencia, problema, ejemplo recurrente. Datos,
  no reglas.

Regla de frontera: *¿una pasada de revisión citaría esto para rechazar un capítulo?*
Si sí y es igual para todas → núcleo. Si sí pero es propio de la guía → adendas. Si
describe al lector o la meta → brief.

Las **bases de sector** (`references/sectores/<slug>.md`) son los *defaults* de las
adendas por dominio. Ampliar el sistema es crear un archivo, sin tocar código. Por
eso el tono salió del brief: era normativo (gobierna cada pasada de voz), así que
sube a las adendas; el brief solo lo refleja. Las cajas y el checklist por capítulo
pasaron de obligatorios a opcionales por sector — calibrado contra la guía de
referencia `guide-ai-developers-basic`, que no usa cajas y centraliza el checklist.
Otros sectores (médico, veterinario) pueden activarlas: ese es el sentido de que el
default viva en el sector, no en el núcleo.

## Dos checkpoints humanos, el resto automático

La automatización es máxima salvo en los dos extremos, donde tu criterio cambia el
resultado:

1. **Brief + investigación**: el sistema te pregunta para encaminar la guía. Cinco
   minutos aquí ahorran horas. Es tu firma de arranque.
2. **PDF anotado**: lees el resultado y comentas. `feedback_intake.py` traduce tus
   anotaciones a cambios concretos. Es tu firma de cierre.

El centro (temario, redacción, pasadas) corre sin intervención. Las pasadas de
naturalidad y precisión corren autónomas pero marcan incidencias (`flagged`); el
freno real es el PDF anotado y los gates de cierre.

## Revisión: 3 pasadas locales + 1 global

Las cinco dimensiones del Principio V (estructura, utilidad, naturalidad,
precisión, formato) se conservan como verificaciones, pero se ejecutan en menos
agentes y en el nivel correcto:

- **Por capítulo** (local): estructura+utilidad fusionadas, naturalidad aislada
  (`marcela-prose`), precisión aislada. Lo que de verdad no se puede mezclar es voz
  y precisión: pulir prosa y verificar datos son tareas opuestas.
- **Al final** (global): formato y coherencia entre capítulos, que solo existen a
  nivel libro.

La precisión no se limita a confiar en `research.md`: para datos volátiles **abre la
fuente en vivo** (URL/web) y contrasta, porque una cita puede haber envejecido entre
la investigación y la redacción. Un dato que la fuente contradice es `critico`.

Detectar es una cosa y corregir, otra: la corrección va en un comando aparte,
`revise`, que aplica al texto solo los hallazgos abiertos de `findings.md` y los
marca resueltos. Así quien detecta no reescribe a ciegas y el loop revisión →
corrección queda cerrado y auditable.

Detectas el fallo temprano y barato, los capítulos se paralelizan, y la coherencia
del conjunto se revisa una vez al cierre.

## Dos ejes ortogonales: el modo y la pista

El manifiesto declara dos campos que gobiernan cosas distintas y **no se estorban**:

- **`mode`** (`produccion` | `estudio`) responde a *quién escribe la prosa*.
- **`track`** (`estandar` | `corta`) responde a *cuánto rito paga la pieza*.

Mantenerlos ortogonales fue deliberado: las cuatro combinaciones son legales y ninguna
necesita código especial. Un artículo escrito a mano es `corta` + `estudio`; un libro
redactado por la IA es `estandar` + `produccion`.

### El modo: quién escribe (constitución v1.6.0)

En `estudio`, la prosa del manuscrito la escribe la persona y la IA no la toca. La
decisión de diseño interesante es **dónde se pone el freno**. No basta con pedirle al
agente que no escriba: el pipeline convierte los pasos de redacción en checkpoints
(`implement` → `write`, `revise` → `dispose`), y el ejecutor añade un guardarraíl que
rechaza cualquier despacho que escriba manuscrito estando en estudio.

Dos consecuencias que valen la pena:

- **Las huellas.** Cada bloque de pasada registra el sha256 del capítulo que revisó. Si
  el capítulo cambia después, la pasada se invalida sola y el capítulo se reabre. Una
  revisión de un texto que ya no existe no vale nada.
- **La disposición es humana.** Las transiciones de estado de un hallazgo son exclusivas
  de `dispose.py`, que exige identidad humana desde `git config` y rechaza las de agente.
  En estudio, aceptar un hallazgo significa «ya lo he corregido yo».

`authorship.py` cierra el círculo: cruza los commits de git sobre `chapters/` con las
ventanas de despacho de `decisions.jsonl` y emite un veredicto de procedencia por
capítulo. La afirmación «lo escribí yo» deja de ser una promesa y pasa a ser evidencia.

### La pista: cuánto rito (constitución v1.7.0)

En `corta`, una pieza única cuesta **6 despachos** en vez de 11. La decisión de diseño
que más nos gusta es que **`status.py` no sabe nada de la pista**: no hay ni una rama por
`track` en la máquina de estados. Los pasos desaparecen *por construcción*.

- `plan` no se pide porque al firmar el brief ya se escribió un temario de una fila:
  `chapters_expected == 1`, y la guarda del temario vacío nunca dispara.
- `constitution` no se pide porque `bootstrap --sector` dejó el sector fijado, y la guarda
  mira si el sector es nulo.
- `intro` se auto-anula en el propio comando: una pieza única no tiene presentación.
- Las pasadas 3 y 5 no se despachan sueltas porque las registra la **pasada combinada**,
  que viaja en el despacho de la pasada 1 y emite los cuatro bloques `pass-output` de
  siempre. El esquema no cambia.

La precisión (dimensión 4) **nunca** se absorbe en la combinada: sigue en relevo aparte,
con otro rol y otro modelo. Es la regla dura «voz ≠ precisión» sobreviviendo a la
compresión de la ceremonia. Cuando algo se recorta, lo que se conserva revela qué es
esencial.

Escalar `corta → estandar` no mueve un solo archivo: la pieza ya es el capítulo 1 del
temario ampliado, y los hallazgos y las claims conservan sus bloques. Por eso el consejo
operativo es empezar en corta ante la duda. `track.py` es el único camino, y exige
identidad humana: **ningún agente cambia la pista**.

## Por qué el PDF es el motor de markdown-to-pdf

Ya tenías una skill `markdown-to-pdf` (pandoc + Chrome headless, estilo editorial
que te gusta). En lugar de reinventarla, `export.py` reutiliza su `style.css` y
deriva lo editorial de tus propios artefactos: la portada del brief, el índice del
temario. Así el export es determinista y corre sin agente. La skill sigue viva como
front-end interactivo; el script es el motor headless. Una sola hoja de estilo.

## Fuentes por capítulo (y cómo no quedan toscas en PDF)

Cada capítulo cierra con su propia sección `## Fuentes` (nombre, enlace, fecha), no
solo un `research.md` central. Es trazabilidad donde el lector la necesita: al pie
del capítulo que está leyendo. La emite `speckit.implement` y la verifican las
pasadas de precisión y formato; es requisito del núcleo (Estándares editoriales).

En markdown, con un archivo por capítulo, esto se lee natural. En el PDF, diez
bloques "Fuentes" seguidos podrían pesar. La decisión: **misma estructura en MD y en
PDF**, sin formatos divergentes; lo único que cambia es el estilo. `export.py`
envuelve el bloque de cierre en `.chapter-sources` y la hoja de estilo lo presenta
atenuado (más pequeño, gris, con filete arriba), como aparato de cierre de capítulo
y no como cuerpo. Es la convención de "notas al final de capítulo" de cualquier
libro, y mantiene un solo modelo mental MD↔PDF.

## Por qué scripts deterministas para status, close, export, feedback

Esas funciones no necesitan un modelo: leer `findings.md`, evaluar gates, ensamblar
un PDF o extraer anotaciones es código. Hacerlo con scripts (no con el agente)
ahorra tokens, corre en Paperclip y da resultados reproducibles. El agente entra
donde sí aporta: redactar y reescribir con voz.

Esto también sustituye al `wom` CLI que estuvo planificado: `status.py` cubre
`wom status` y el gate de `wom close`; `close.py` añade el export. No hace falta una
CLI aparte.

Hay una excepción a «determinista = sin criterio»: `dispose.py` y `track.py` son
scripts, pero **exigen identidad humana**. Leen `git config` y rechazan las identidades
de agente. No están automatizando una decisión: están registrando la tuya, con
escritura atómica y un historial append-only. Un script es aquí la forma de garantizar
que nadie más la tome.

## El re-despacho quirúrgico

`feedback_intake.py` ata cada anotación a la frase resaltada y busca esa frase en
`chapters/*.md` para saber a qué capítulo pertenece. Por eso un comentario en el
capítulo 7 reescribe solo ese pasaje y nunca toca el 1–6. El mapeo va por texto
anclado, no por número de página, que es frágil.

## Fuentes del diseño

Diátaxis (estructura de esta documentación y de las guías), la constitución del
framework (`.specify/memory/constitution.md`, **v1.7.0**), el contrato pass-output
**v1.2** y el manifest **v1.4.0**, y el patrón del preset de ficción de la comunidad
(`speckit-preset-fiction-book-writing`) para el empaquetado y los comandos
neutrales de género.
