# Tutorial: tu primera guía de principio a fin

Este recorrido produce una guía técnica corta desde cero usando el preset
`writeonmars`. Al terminar tendrás un PDF maquetado y entenderás el ciclo. Sigue
los pasos en orden; cada uno deja el proyecto listo para el siguiente.

Todo va por **comandos del preset** (`/speckit.*`), pensados para que los ejecute
cualquier agente con cualquier modelo (ver [`../AGENTS.md`](../AGENTS.md)). El
detalle de cada comando está en [`referencia.md`](referencia.md); el porqué, en
[`arquitectura.md`](arquitectura.md).

## Antes de empezar

- **Spec Kit** (`specify`) ≥ 0.5.0.
- **Dependencias de salida**: `pandoc` y Chrome o Chromium (PDF).
- Para el loop de feedback: `pymupdf` (`pip install pymupdf`).

No necesitas instalar skills aparte: la voz, la didáctica y el método viajan
dentro del preset como referencias (`writeonmars/references/`), así cualquier
modelo las aplica.

## 1. Crea el proyecto e instala el preset

**Atajo recomendado**: un solo comando deja la guía montada (carpeta, repo git,
`specify init`, preset y bootstrap), heredando operador y email de tu configuración
de git, con un commit de base y el contexto multi-agente unificado por symlinks
(`AGENTS.md` ← `CLAUDE.md`, `GEMINI.md`):

```bash
bash ~/Projects/writing-framework/tools/new-guide.sh ~/Projects/guia-prueba
```

El destino debe quedar **fuera del repo del framework**: cada guía es su propio
repositorio. Si usas el atajo, sáltate al paso 3 (la constitución); el script ya
hizo el bootstrap por ti.

A mano, los mismos pasos son:

```bash
mkdir ~/Projects/guia-prueba && cd ~/Projects/guia-prueba && git init
specify init --integration claude .
specify preset add --dev ~/Projects/writing-framework/writeonmars
```

Instala las plantillas editoriales, los comandos y los scripts. (Verifica que tu versión de `specify` copia también `references/`; si no, ese directorio debe quedar accesible para los comandos.)

## 2. Bootstrap del proyecto

(Si usaste `new-guide.sh` en el paso 1, esto ya está hecho: continúa en el paso 3.)

```text
/speckit.setup
```

Copia el **núcleo de la constitución** (las reglas universales: voz, brief,
revisión, neutralidad) y crea el `.writeonmars-manifest.json` (versiones,
`signing_matrix`, operadores, sector) — lo que el preset no puede instalar solo. Se
corre una vez, justo después de instalar. (También como script:
`python3 .specify/presets/writeonmars/scripts/bootstrap.py`.) Por defecto todas las
pasadas quedan **autónomas**: el control humano son los dos checkpoints (brief y PDF
anotado), no pasada por pasada.

## 3. La constitución del proyecto (sector + tono)

```text
/speckit.constitution
```

Es el **primer paso del ciclo**. El núcleo de la constitución es universal y no se
toca; aquí defines la **capa por guía** (las *adendas*): lo normativo que sí cambia
de una guía a otra. El comando te guía con preguntas y **un valor por defecto en
cada una** — pulsar Enter mantiene el estándar:

1. **Sector** — tecnología, y los que vayas creando (veterinaria, medicina…). El
   sector carga sus *defaults* (tono, anglicismos, estructura de capítulo).
2. **Camino rápido**: aceptar el estándar del sector tal cual, o ir pregunta por
   pregunta (tono calibrado, anglicismos admitidos, contrato terminológico,
   relajaciones estructurales, idioma, gobernanza).

Escribe la sección `## Adendas del proyecto` sobre el núcleo intacto y guarda el
`sector` en el manifest. A partir de aquí, el tono y la terminología que la guía
usará ya están fijados: el brief y las pasadas de revisión los leen de ahí.

## 4. El brief, con preguntas (checkpoint humano 1)

```text
/speckit.specify "una guía básica de prompts efectivos para developers"
```

Rellena el brief de **ocho campos descriptivos** (audiencia, problema, resultado,
nivel, conceptos, ejemplo recurrente, riesgos, acciones) y te pregunta lo que
falte. El **tono no se pregunta aquí**: ya está calibrado en las adendas (paso 3) y
el brief solo lo refleja. El avance se bloquea hasta que audiencia, ejemplo
recurrente y resultado esperado estén claros. Cuando el brief te convenza, es tu
firma.

## 5. Investigación con fuentes

Pon tus fuentes en `resources/` y:

```text
/speckit.research
```

Produce `specs/<###>/research.md` con una cita por concepto obligatorio. Bloquea
si algún concepto queda sin respaldo.

## 6. Temario y descripciones encadenadas

```text
/speckit.plan
```

Genera el temario (`Número | Título | Promesa`) y las descripciones encadenadas.
El temario es además el índice de tu futuro PDF.

## 7. Redacción (un capítulo cada vez)

```text
/speckit.implement 1
```

Redacta UN capítulo en `chapters/<NN>-titulo.md` con la voz de la autora y la
**estructura que fija la base del sector**. Cada capítulo **cierra con su sección
`## Fuentes`** (nombre, enlace y fecha de lo citado en ese capítulo): es requisito,
no opcional. El número elige el capítulo (`1`); **sin número**, escribe el siguiente
pendiente (el primero del temario que aún no tiene archivo). Si el archivo ya
existe, lo **rehace**. **Solo escribe**: no se revisa a sí mismo.

## 8. Revisión (idealmente con OTRO modelo)

La revisión va aparte, para que quien escribe no se autoevalúe. Agrupada:

```text
/speckit.review 1
```

O cada pasada por separado, para asignarla a un modelo distinto:

```text
/speckit.review-structure 1
/speckit.review-voice 1
/speckit.review-precision 1
/speckit.review-global
```

Cada pasada escribe su bloque en `findings.md`. Las tres locales son por capítulo;
la global, una vez sobre el libro entero. La de precisión no solo confía en
`research.md`: **abre la fuente en vivo** (URL/web) para contrastar los datos
volátiles, y comprueba que cada capítulo tiene su `## Fuentes`.

## 9. Aplica los hallazgos

```text
/speckit.revise 1
```

Lee los hallazgos abiertos de `findings.md` y reescribe SOLO los pasajes señalados,
marcándolos como resueltos. Cierra el loop revisión → corrección. Lo puede correr el
modelo que escribió; un hallazgo `critico` sin resolver bloquea el cierre.

## 10. Mira el estado

```text
/speckit.status
```

Tablero de capítulos × pasadas × firmas y los gates de cierre (críticos abiertos,
firmas humanas pendientes y completitud del temario). (También como script:
`python3 ~/Projects/writing-framework/writeonmars/scripts/status.py`.)

## 11. Genera el PDF

Primero, la **presentación** de la guía (lo que abre el PDF):

```text
/speckit.intro
```

Crea el `README.md` (Acerca de / para quién es / qué aprenderás / cómo leer). Luego
el PDF:

```text
/speckit.export
```

Toma el título del brief, el índice del temario y ensambla los capítulos con el
estilo editorial. El PDF sale con portada, índice navegable y page-break por
capítulo. Las `## Fuentes` de cada capítulo se mantienen, atenuadas como aparato de
cierre (no como cuerpo).

## 12. Anótalo y aplica el feedback (checkpoint humano 2)

Abre el PDF, resalta y comenta (puedes etiquetar `#voz`, `#dato`, `#critico`…):

```text
/speckit.feedback guia.pdf
```

Cada anotación se mapea a su capítulo por el texto resaltado, y los cambios se
aplican SOLO en los pasajes señalados. Un comentario en el capítulo 5 no reescribe
el 1–4.

## 13. Cierra

```text
/speckit.close
```

Comprueba que no quedan críticos abiertos ni firmas humanas pendientes y, si pasa,
regenera el PDF final. Si está bloqueado, te dice qué resolver y no exporta.

## Qué tienes ahora

Una guía redactada con voz coherente, revisada, contrastada con fuentes (con su
bloque de fuentes por capítulo), exportada a PDF y cerrada con tu visto bueno —
producida por comandos que cualquier modelo puede lanzar.

Lo que acabas de hacer es el **modo directo**: tú, con un agente, lanzando los
comandos uno a uno. Sobre ese mismo método hay una **capa de orquestación opcional**:
el ciclo entero puede correr **desatendido bajo Paperclip**, con un equipo de cuatro
roles editoriales (editora jefa orquestadora, documentalista, redactora y editora de
mesa). El detalle operativo está en [`how-to.md`](how-to.md) ("Cómo correr todo
desatendido bajo Paperclip") y en [`../paperclip/README.md`](../paperclip/README.md).
