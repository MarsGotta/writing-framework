# Tu primera pieza, de principio a fin

Al terminar este recorrido tendrás un PDF maquetado, revisado y con sus fuentes, y
entenderás el ciclo lo bastante como para repetirlo sin releer nada. Se tarda una tarde.

No hace falta que sepas nada del framework por dentro. Solo dos ideas:

- **Tu guía es su propio repositorio.** El repo de Write.OnMars contiene el método; tu
  guía vive aparte, y allí instalas el método como un preset.
- **Tú firmas dos veces.** Al principio, el brief. Al final, el PDF anotado. Todo lo de
  en medio corre solo.

Cada paso es un comando que ejecuta tu agente. El detalle de cada uno está en
[referencia.md](referencia.md); el porqué, en [arquitectura.md](arquitectura.md).

> **Nota de invocación.** El nombre canónico de los comandos lleva punto
> (`speckit.specify`), pero Claude los registra como skills con guion. Si usas Claude,
> escribe `/speckit-specify`. En este tutorial verás la forma con punto.

## Antes de empezar

| Necesitas | Para qué |
|---|---|
| **Spec Kit** (`specify`) ≥ 0.5.0 | Instalar el preset |
| **pandoc** y **Chrome** o Chromium | Generar el PDF |
| **pymupdf** (`pip install pymupdf`) | El loop de feedback sobre el PDF anotado |

No instales skills aparte. La voz, la didáctica y el método viajan dentro del preset como
documentos que cualquier modelo lee.

## Paso 0. Decide la pista (30 segundos, ahorra horas)

Antes de crear nada, responde a una pregunta: **¿esto es una pieza o es un libro?**

- Una **pieza única** —un artículo, un post, un tutorial breve, un ensayo— va en **pista
  corta**. Seis despachos, temario de una línea, revisión en dos relevos, sin README de
  presentación.
- Una **guía, un manual o un libro** con varios capítulos va en **pista estándar**, que es
  el valor por defecto. Once despachos sobre la misma pieza.

Ante la duda, **empieza en corta**. Escalar después conserva el cien por cien del trabajo
(no se mueve ni un archivo); arrancar en estándar «por si acaso» te cobra el rito completo
desde el primer día.

La pista no tiene nada que ver con quién escribe la prosa. Eso es el *modo*, y lo verás al
final.

## Paso 1. Crea el proyecto

Un solo comando monta la carpeta, el repositorio git, `specify init`, el preset y el
bootstrap, heredando tu nombre y correo de la configuración de git.

En **pista estándar** (un libro, una guía):

```bash
bash ~/Projects/writing-framework/tools/new-guide.sh ~/Projects/mi-guia
```

En **pista corta** (una pieza única), declara la pista y el sector *al crear el proyecto*,
con dos variables de entorno:

```bash
WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia \
  bash ~/Projects/writing-framework/tools/new-guide.sh ~/Projects/mi-articulo
```

El destino debe quedar **fuera del repo del framework**.

> **La pista se fija al crear y solo al crear.** Volver a lanzar el bootstrap más tarde no
> la cambia: te dirá «`.writeonmars-manifest.json` ya existe» y se quedará en `estandar`. Si
> te has equivocado, no reinstales nada — usa `track.py`, que es el camino previsto (lo
> verás al final del tutorial).

Con el sector fijado de entrada, el ciclo se salta el paso de la constitución: las adendas
del sector ya quedaron escritas, y el registro (`tecnico-divulgativo`) también.

<details>
<summary>Hacerlo a mano, sin el atajo</summary>

```bash
mkdir ~/Projects/mi-guia && cd ~/Projects/mi-guia && git init
specify init --integration claude .
specify preset add --dev ~/Projects/writing-framework/writeonmars
/speckit.setup     # o: python3 .specify/presets/writeonmars/scripts/bootstrap.py
```

`speckit.setup` copia el núcleo de la constitución y crea el `.writeonmars-manifest.json`.
Es lo único que un preset no puede instalar por su cuenta. Se corre una vez.

Para pista corta, el bootstrap directo acepta los flags equivalentes:

```bash
python3 .specify/presets/writeonmars/scripts/bootstrap.py --track corta --sector tecnologia
```
</details>

## Paso 2. La constitución del proyecto

> **Pista corta:** sáltate este paso. `bootstrap --sector` ya lo hizo.

```text
/speckit.constitution
```

El núcleo de la constitución —voz, revisión, neutralidad— es universal y nadie lo toca.
Aquí defines la capa que sí cambia de una guía a otra: el **sector**, el tono calibrado, los
anglicismos que admites, el contrato terminológico.

Te guía con preguntas y **una respuesta por defecto en cada una**. Pulsar Enter mantiene el
estándar del sector, así que puedes despacharlo en un minuto o afinarlo durante veinte.

A partir de aquí, el tono está fijado. No te lo volverán a preguntar.

## Paso 3. El brief — tu primera firma

```text
/speckit.specify "una guía básica de prompts efectivos para developers"
```

Rellena **ocho campos descriptivos** (audiencia, problema, resultado, nivel, conceptos,
ejemplo recurrente, riesgos y acciones) y te pregunta lo que falte. El tono no se pregunta:
ya está en las adendas.

El avance **se bloquea** hasta que tres cosas estén claras: quién es tu lector, cuál es el
ejemplo que recorrerá la guía y qué sabrá hacer al terminar. Cinco minutos aquí ahorran
horas después.

Cuando el brief te convenza, es tu firma. **Este es el checkpoint humano número uno.**

> En pista corta, el mismo comando recoge además el título y la promesa de la pieza, y
> escribe con ellos un temario de una sola fila. Por eso más adelante no hay paso de plan:
> el temario ya existe.

## Paso 4. La investigación

Deja tus fuentes en `resources/` y:

```text
/speckit.research
```

Produce un `research.md` con **una cita por cada concepto obligatorio**. Si algún concepto
se queda sin respaldo, bloquea. No hay guía sin fuentes.

## Paso 5. El temario

> **Pista corta:** sáltate este paso. Tu temario ya es la pieza.

```text
/speckit.plan
```

Genera el temario —número, título y promesa por capítulo— y las descripciones encadenadas,
para que cada capítulo sepa de dónde viene el lector. Ese temario será además el índice de
tu PDF.

## Paso 6. La redacción

```text
/speckit.implement 1
```

Redacta **un** capítulo, con la voz de la autora y la estructura que fija el sector. El
número elige el capítulo; sin número, escribe el siguiente pendiente. Si el archivo ya
existe, lo rehace.

Cada capítulo cierra con su sección `## Fuentes`. Es un requisito, no una cortesía: la
trazabilidad va donde el lector la necesita.

Este comando **solo escribe**. No se revisa a sí mismo, y esa es la idea.

## Paso 7. La revisión, idealmente con otro modelo

Quien escribe no se corrige. Si puedes, lanza la revisión con un agente distinto del que
redactó. Agrupada:

```text
/speckit.review 1
```

O pasada por pasada, para repartirlas entre modelos:

```text
/speckit.review-structure 1     # estructura y utilidad
/speckit.review-voice 1         # naturalidad
/speckit.review-precision 1     # precisión — abre las fuentes en vivo
/speckit.review-global          # formato y coherencia, una vez sobre el libro
```

Cada pasada escribe su bloque en `findings.md`. La de precisión no se limita a confiar en
`research.md`: **abre las URL y contrasta**, porque una cita pudo envejecer entre la
investigación y la redacción. Un dato que la fuente contradice es un hallazgo crítico.

> En **pista corta** son solo dos relevos. `review-structure` hace una *pasada combinada*
> que cubre estructura, utilidad, naturalidad y formato de una vez. La precisión corre
> siempre aparte, con otro modelo: pulir prosa y verificar datos son tareas opuestas y no se
> mezclan nunca.

## Paso 8. Aplica los hallazgos

```text
/speckit.revise 1
```

Lee los hallazgos abiertos y reescribe **solo** los pasajes señalados, marcándolos como
resueltos. Esto sí lo puede correr el modelo que escribió.

Un hallazgo `medio` abierto no te impedirá cerrar, pero el sistema te mandará aquí antes de
dejarte llegar al cierre. Uno `critico` bloquea el cierre de verdad.

## Paso 9. Mira dónde estás

```text
/speckit.status
```

Un tablero de capítulos por pasadas, con los hallazgos abiertos y los tres gates de cierre:
que no queden críticos, que no falten firmas, que el temario esté completo. Cuando dudes qué
toca ahora, pregúntale a él: es la brújula del método y siempre responde mirando el disco.

## Paso 10. El PDF

Primero la presentación, que es lo que abre el libro:

```text
/speckit.intro
```

> **Pista corta:** sáltate este paso. Una pieza única no lleva README de presentación, y el
> export lo sabe: te dará una portada compacta, sin índice.

Y ahora sí:

```text
/speckit.export
```

Toma el título del brief y el índice del temario, y ensambla los capítulos con el estilo
editorial: portada, índice navegable, un salto de página por capítulo. Las secciones
`## Fuentes` se conservan, atenuadas como aparato de cierre y no como cuerpo del texto.

## Paso 11. Anótalo — tu segunda firma

Abre el PDF, resalta lo que no te convenza y comenta. Puedes etiquetar los comentarios
(`#voz`, `#dato`, `#critico`).

```text
/speckit.feedback mi-guia.pdf
```

Cada anotación se ata a la frase que resaltaste y se aplica **solo** en su pasaje. Un
comentario en el capítulo 5 no reescribe el 1 al 4.

**Este es el checkpoint humano número dos**, y es el freno real del método: no una firma por
pasada, sino tu lectura del resultado terminado.

## Paso 12. Cierra

```text
/speckit.close
```

Comprueba los gates y, si pasan, regenera el PDF final. Si algo bloquea, te dice
exactamente qué y **no exporta**.

Ya está. Tienes una pieza con voz coherente, revisada por un modelo distinto del que la
escribió, contrastada con fuentes, exportada y cerrada con tu visto bueno.

---

## Si la pieza pide crecer

¿Empezaste en corta y aquello ya no cabe en un capítulo? Asciéndela:

```bash
python3 .specify/presets/writeonmars/scripts/track.py --escalar --project-dir .
```

**No se mueve un solo archivo.** Tu pieza pasa a ser el capítulo 1, el brief sigue siendo el
brief, y los hallazgos y las fuentes siguen valiendo. A partir de ahí amplías el temario y el
sistema te pedirá los capítulos que faltan.

El escalado exige identidad humana: lo lee de tu `git config` y rechaza las identidades de
agente. Ningún modelo asciende una pieza por su cuenta.

## Si la prosa la escribes tú

Todo lo anterior asume que la IA redacta. Si quieres lo contrario —que **tú escribas** y la
IA solo revise, anote y acompañe— eso es el **modo estudio**, y es independiente de la pista:

```bash
vivarium mode set estudio --yes    # o el campo "mode": "estudio" en el manifiesto
```

Cambian dos cosas. Donde había redacción automática, el ciclo se detiene y espera tus
capítulos. Y donde había corrección automática, los hallazgos esperan **tu decisión**:

```bash
python3 .specify/presets/writeonmars/scripts/dispose.py F-1.1 --aceptar --project-dir .
python3 .specify/presets/writeonmars/scripts/dispose.py F-1.2 --rechazar --motivo "no aplica al género"
python3 .specify/presets/writeonmars/scripts/dispose.py F-1.3 --aplazar
```

Además, cada pasada guarda una huella del capítulo que revisó. Si lo tocas después, la
revisión se invalida sola y el capítulo vuelve a la cola. Y `authorship.py` emite un informe
de autoría que distingue tu prosa de la de un agente cruzando los commits de git.

El detalle completo está en [how-to-modo-estudio.md](how-to-modo-estudio.md).

## Cuando quieras desatenderlo

Lo que acabas de hacer es el **modo directo**: tú, con un agente, lanzando comandos uno a
uno. Es como se entiende el método, y para una pieza a la que quieras mimar la voz sigue
siendo la mejor forma.

Cuando quieras producir sin estar delante, existe **Vivarium**, un ejecutor que recorre el
ciclo solo y reparte cada paso entre modelos distintos:

```bash
vivarium new mi-guia --kind guia   # crea el proyecto entero
vivarium check                     # valida el entorno, sin ejecutar nada
vivarium run                       # avanza hasta que te necesita
```

`vivarium run` **sale con el código 10** cuando llega a un checkpoint humano. Firmas lo que
te pide, vuelves a lanzarlo, y sigue. Al terminar, sale con 0.

Los modelos se declaran en `.vivarium/config.toml`, un CLI por rol:

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

Que la redactora y la editora de mesa apunten a modelos distintos no es un capricho: es lo
que hace que quien escribe no se revise.

> **Ojo con una trampa conocida.** Para crear un proyecto de pista corta con Vivarium, usa
> las variables de entorno, no el flag `--sector`:
>
> ```bash
> WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia \
>   vivarium new mi-articulo --kind guia --preset /ruta/al/writeonmars
> ```
>
> El flag del ejecutor escribe el sector *después* del bootstrap, y el proyecto se queda sin
> adendas. Está anotado como deuda en el ROADMAP.

## Dónde seguir

- **Resolver una tarea concreta**: [how-to.md](how-to.md).
- **Consultar comandos, flags y esquemas**: [referencia.md](referencia.md).
- **Entender por qué está montado así**: [arquitectura.md](arquitectura.md).
- **El plano completo del repositorio**: [docs/como-funciona.md](../../docs/como-funciona.md).
- **Pista corta al detalle**: [how-to-pista-corta.md](how-to-pista-corta.md).
- **Modo estudio al detalle**: [how-to-modo-estudio.md](how-to-modo-estudio.md).
