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
framework (`.specify/memory/constitution.md`, v1.2.0), el contrato pass-output v1.0
y el manifest v1.0, y el patrón del preset de ficción de la comunidad
(`speckit-preset-fiction-book-writing`) para el empaquetado y los comandos
neutrales de género.
