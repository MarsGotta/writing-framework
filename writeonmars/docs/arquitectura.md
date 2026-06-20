# Arquitectura y decisiones

Por qué el preset está montado así. Esto no enseña a usarlo (para eso está el
[tutorial](tutorial-primera-guia.md)); explica las decisiones para quien lo
mantiene o lo extiende.

## Un método, dos ejecutores

El método editorial es uno solo: el ciclo Spec Kit en modo editorial más las
skills de voz y método. Se ejecuta de dos formas, con el mismo código debajo:

- **Directo**: tú con Claude Code y los comandos `speckit.*`. Para guías donde
  quieres mimar la voz.
- **Orquestado**: Paperclip lanza Claude Code como proceso hijo en heartbeats.
  Para producir varias guías sin estar delante.

No hay dos pipelines que mantener: Paperclip envuelve el mismo método. Por eso los
scripts son deterministas y no asumen un agente delante.

## Agente-agnóstico: la lógica en comandos, no en skills

El pipeline lo lanzan distintos agentes con distintos modelos, no solo Claude. Por
eso la lógica NO vive en skills de Claude (que se autodisparan y son de un
proveedor), sino en **comandos** del preset (`speckit.*`) y **referencias**
neutrales (`references/voz`, `references/didactica`, `references/metodo`) que
cualquier modelo lee y aplica. Es el modelo del preset de ficción, que no usa
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

## El re-despacho quirúrgico

`feedback_intake.py` ata cada anotación a la frase resaltada y busca esa frase en
`chapters/*.md` para saber a qué capítulo pertenece. Por eso un comentario en el
capítulo 7 reescribe solo ese pasaje y nunca toca el 1–6. El mapeo va por texto
anclado, no por número de página, que es frágil.

## Fuentes del diseño

Diátaxis (estructura de esta documentación y de las guías), la constitución del
framework (`.specify/memory/constitution.md`, v1.3.0), el contrato pass-output v1.0
y el manifest v1.0, y el patrón del preset de ficción de la comunidad
(`speckit-preset-fiction-book-writing`) para el empaquetado y los comandos
neutrales de género.
