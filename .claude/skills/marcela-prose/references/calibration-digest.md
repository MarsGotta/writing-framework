# Calibration digest — moves extraídos de la pasada de Marcela

<!-- Origen: 4 *-despues.md editados por Marcela el 2026-05-05 sobre los 4 *-antes.md generados por Claude. Análisis crítico contrastado con la skill v1, el CRITIQUE de research/ y la tradición canónica (Klinkenborg, Pinker, Strunk, Sword, Vivaldi). -->

Cuatro pares antes/después editados por Marcela: tutorial, how-to, reference, explanation. Lo que sigue son los moves recurrentes con etiqueta, ejemplo literal y regla operativa para el agente.

---

## A. Voz autorial: la proporción real

La skill v1 declaraba "tú implícito por defecto, nosotros para invitar, yo esporádico". La calibración la invierte. La proporción real en los 4 samples:

- **Nosotros inclusivo: ~95 % de los verbos.** "Imaginemos", "tenemos tres opciones", "podemos sustituir", "estemos migrando", "vamos a definir", "volvemos al historial", "no debemos recortar".
- **Tú implícito: ~5 %, puntual.** Aparece cuando hay segunda persona técnica de instrucción aislada ("lanza una llamada", "Marca claramente la frontera"), normalmente rodeada de plural inclusivo.
- **Yo: 0 % en los 4 samples.** No aparece. Probablemente porque el "nosotros" absorbe el espacio que en otros autores ocupa el "yo". El "yo" queda reservado para géneros más ensayísticos (prefacio, post personal, columna).

**Regla operativa**: la voz por defecto es plural inclusivo. El "tú" implícito se reserva para instrucción puntual aislada. El "yo" casi nunca aparece — solo cuando aporta cicatriz que el "nosotros" no podría sostener.

---

## B. Aperturas: cinco tipos validados

A los cuatro tipos de la skill v1 (escena, objeto, dato, pregunta) se añade un quinto, recurrente en los samples:

**Apertura como pacto de continuidad.** Sitúa el bloque dentro de un viaje compartido con el lector.

> *"Ya hemos acabado con la parte más aburrida (imaginando que ha habido una apartado teorico previo) es momento de ponernos manos a la obra."* (tutorial)

Usable cuando el capítulo es continuación natural de otro. Pide que en el libro real exista la sección anterior — no funciona como apertura del primer capítulo.

**Apertura en dos beats antes del qué (tutorial).** Beat emocional + beat cognitivo, después el contenido técnico.

> *"Ya hemos acabado con la parte más aburrida […] En este tutorial desbloquearemos un superpoder que antes no teniamos en nuestro arsenal […] veremos cómo construir un agente básico que utiliza tool use."*

Beat 1 cierra lo anterior y prepara emocionalmente. Beat 2 nombra lo que viene en clave lúdica ("superpoder"). Solo entonces baja al qué técnico.

---

## C. Cierres: tres formas validadas más

A los cierres de la skill v1 (instrucción accionable, pregunta abierta, bisagra) se añaden estos tres, todos presentes en los samples:

**Cierre lapidario** (explanation). Una frase corta que recoge todo el capítulo en un movimiento de lengua.

> *"La segunda pregunta es la que define el oficio."*

**Cierre proyectivo en condicional** (tutorial). No cierra: proyecta hacia el siguiente paso.

> *"Con esto tendríamos un agente mínimo que sabe usar una herramienta. El siguiente paso natural sería añadir un loop para que el modelo pueda encadenar varias invocaciones."*

**Cierre de cuándo NO hacer** (how-to). En vez de recapitular qué hacer, marca el caso límite.

> *"Si el agente está en mitad de una transacción crítica (un commit, un pago, una llamada irreversible), no debemos recortar durante dicha transacción. Hay que esperar a que la transacción cierre o falle, y recortar entre transacciones."*

---

## D. Paréntesis: tres modalidades de la firma

El paréntesis honesto Karpathy es solo una forma. Los samples documentan tres usos distintos, todos consistentes:

**Paréntesis didáctico Karpathy.** Aside que reconoce dificultad o aporta ejemplo.

> *"(un commit, un pago, una llamada irreversible)"*

**Paréntesis irónico.** Aside que confirma con humor lo dicho.

> *"o que pienses que el modelo no tiene idea de lo que estás hablando (Algo completamente cierto)."*

**Paréntesis editorial.** Aside que flagea honestamente un pendiente metodológico, en lugar de inventar fuente o saltarlo.

> *"Según varias investigaciones (habria que añadir aqui investigaciones, siempre poner citas de sitios donde se han encontrado), los modelos actuales muestran…"*

Los tres son legítimos. El editorial es típico de borradores trabajados; en versión final pasa a SOURCES.md o se completa.

---

## E. Antropomorfización del agente

Patrón consistente en los 4 samples. El agente / modelo es entidad con personalidad.

> *"el modelo se ha vuelto loco, que no entiende lo que le decimos, que se ha olvidado de cosas que le dijimos hace un rato"*
> *"el agente las olvida"*
> *"para el, los últimos tokens son los que 'tiene presentes'"*
> *"que pienses que el modelo no tiene idea de lo que estás hablando"*

**Regla operativa**: en explanation y tutorial, antropomorfizar al sistema como entidad con voluntad y memoria es tu firma. En reference, no aplica (registro catálogo). El agente debe imitar este uso — verbos de percepción y memoria sobre el modelo — pero sin caer en metáfora cósmica ni en personajes inventados con nombre.

---

## F. Validación de intuición ingenua usando palabras "prohibidas"

La skill v1 prohíbe "imagina que", "magia", "potente". La calibración demuestra que esas palabras valen en un caso: cuando la autora las pone en boca del lector ingenuo para luego desmontarlas.

> *"Imaginemos que nuestro equipo empieza a trabajar con agentes. Cuando todo va bien parece que es magia o existe algun desarrollador diminuto que susurra al modelo lo que tiene que hacer."*

Aquí "imaginemos" + "magia" no son tesis abstracta ni adjetivo promocional: son la intuición ingenua que la autora va a afilar. Es exactamente la regla 4 de prosa con pulso.

**Regla operativa**: las palabras "prohibidas" valen cuando son atribución a la posición ingenua del lector, marcadas claramente como tales, y desmontadas en las frases siguientes. Nunca como tesis propia.

---

## G. Metáforas sensoriales / físicas

Cuatro metáforas en explanation, todas físicas, ninguna cósmica, ninguna sostenida (algunas vuelven, otras viven solas):

> *"existe algun desarrollador diminuto que susurra al modelo"*
> *"como si nosotros tuvieramos muchas ideas en la cabeza y viene alguien a preguntarnos algo"*
> *"un muro que recubre todo el comportamiento del agente, la primera linea será aquella barrera de piedra impenetrable"*
> *"como cuando no has escuchado nada de lo que te han dicho y solo logras retener lo justo para responder a la pregunta 'me has escuchado? qué te he dicho?'"*

**Regla operativa**: una por concepto fuerte, sensorial o física, doméstica o mecánica. Si vuelve, que aporte (la del muro vuelve como "esta capa más robusta del prompt"); si no vuelve, también vale (la del "no haber escuchado" rinde sola). La obligación de retorno de la skill v1 es excesiva.

---

## H. Vocabulario emocional sobre actos técnicos

Marcela mete vocabulario humano sobre operaciones de máquina. Esto es lo que Zinsser llama "humanidad en escritura técnica".

> *"brillará nuestro ingenio como desarrolladores"*
> *"sin quedar como un desconsiderado"*
> *"la parte más aburrida"*
> *"complicado en muchas ocasiones, el priorizar"*

**Regla operativa**: cuando una operación técnica tiene un correlato emocional honesto, nómbralo. No es marketing — es validación de la experiencia del lector que también siente cuando programa.

---

## I. Léxico lúdico-coloquial

Marcela usa palabras que la skill v1 prohibiría como inflado promocional. La distinción que hay que hacer:

| Léxico | Ejemplo en samples | Estado |
|---|---|---|
| Promocional vacío | "potente", "robusto", "mágico", "elegante" | Prohibido (sigue) |
| Lúdico-coloquial | "superpoder", "arsenal", "parte aburrida" | Permitido |

> *"En este tutorial desbloquearemos un superpoder que antes no teniamos en nuestro arsenal."*

La diferencia es función: el promocional vende, el lúdico baja el registro y crea cercanía. El segundo es voz, el primero es marketing.

---

## J. Conceder antes de aseverar

Técnica retórica clásica. Marcela la hace sin pensar:

> *"Está claro que cada caso es distinto pero existen tres principios operativos que nos pueden guiar."*
> *"podemos ampliar la ventana de contexto aunque esta no siempre posible y siempre es más caro, resetear la conversación, pero en este caso perderíamos el estado; o bien, recortar."*

**Regla operativa**: cuando sostienes una tesis fuerte, concede el matiz contrario brevemente antes de aseverar. La skill v1 no la nombra; debe documentarla.

---

## K. Pregunta retórica como bisagra entre bloques

> *"¿Y cómo podemos saber el orden correcto que debemos utilizar para organizar el contexto de un modelo? Está claro que cada caso es distinto pero…"*

Distinto de la pregunta concreta como apertura: aquí la pregunta abre el siguiente bloque dentro de un argumento ya en curso. Funciona en explanation. La skill v1 solo recoge la pregunta como apertura de capítulo.

---

## L. Imperativo en how-to: matizado

La skill v1 prescribía "registro instrucción → imperativo, paso numerado". La calibración del how-to demuestra otra cosa: el registro instrucción de Marcela es **plural inclusivo modal** ("podemos", "tenemos que", "vamos a", "volvemos", "aplicamos") con imperativo puntual cuando la operación es una sola línea ("lanza una llamada", "Marca claramente la frontera").

> *"Hoy en día, existen tres técnicas que podemos aplicar […] podemos sustituirlo por un resumen […] podemos sustituir el bloque entero […] Si A y B no son suficientes, lanza una llamada al modelo."*

**Regla operativa**: how-to en plural inclusivo modal por defecto. Imperativo seco solo en operaciones puntuales que se sostienen en una línea. Nunca como registro dominante.

---

## M. "Vamos a" como firma de transición

Aparece en los 4 samples como bisagra entre secciones o introducción de un nuevo paso:

> *"vamos a definir nuestra herramienta"*
> *"vamos a calcular el tamaño actual del contexto"*
> *"Y es justo esta técnica, la que vamos a cubrir en esta guía"*
> *"es momento de ponernos manos a la obra"*

**Regla operativa**: "vamos a" + infinitivo como firma propia de tránsito entre bloques. Tolerada incluso varias veces por capítulo, siempre que cada uso introduzca un movimiento real.

---

## N. Reglas de la skill v1 que la calibración relaja

Lista cerrada. Cada una pasa de prohibición o cuota a permiso matizado:

| Regla v1 | Estado tras calibración |
|---|---|
| "Imagina que…" prohibido | Permitido cuando es validación de intuición ingenua |
| "Magia" prohibido | Permitido en boca del lector ingenuo, marcado como tal |
| "Dicho/a" prohibido como anafórico | Permitido en uso natural de lengua |
| "Hoy en día / lo más probable es que" prohibido | Tolerado como modulación de ritmo, no como relleno repetido |
| Léxico inflado prohibido | Distinguido: promocional sigue prohibido, lúdico permitido |
| Yo "una o dos veces por capítulo" | Cualitativo: cuando aporta cicatriz; puede ser cero |
| Frase máxima 40 palabras | Excepción cuando construye argumento, una por sección |
| Em dash "idealmente cero" | Una por párrafo cuando es la mejor puntuación, sin culpa |
| Imperativo en how-to | Plural inclusivo modal por defecto, imperativo puntual |
| Metáfora doméstica obligatoria + retorno | Permiso, no obligación; retorno opcional |

---

## O. Patrones a vigilar en la propia prosa

La calibración también revela tres patrones que se cuelan en los samples y que el canon (Klinkenborg, Pinker, Strunk) marcaría como mejorables. Esto es para que el agente, al editar prosa de Marcela, los flagee:

**1. Frase amontonada con comas cuando hay carga emocional** (Klinkenborg, Vivaldi). Aparece cuando explicas algo cercano. Cuatro ideas pegadas con comas en una frase.

> *"Según varias investigaciones […], los modelos actuales muestran un patrón conocido como atención no uniforme a lo largo del prompt, se despistan de lo importante cuando existe mucho ruido, como si nosotros tuvieramos muchas ideas en la cabeza y viene alguien a preguntarnos algo, seguramente, si no priorizaramos la información de nuestra cabeza, podríamos fallar en la respuesta."*

**Regla operativa**: cuando una frase mete tesis + descripción + analogía + consecuencia con comas, parte en 2-3 frases. Especialmente cuando el `que` subordinado pasa de dos.

**2. Hedging blando heredado del registro tech-blog-español** (Pinker). Se cuela cuando bajas el piloto automático.

> *"hoy en dia, cada vez más, está cogiendo relevancia"*
> *"lo más probable es que nuestros prompts mejoren mucho de calidad"*
> *"es interesante tenerlo encuenta"*

**Regla operativa**: si llevas dos páginas sosteniendo argumento, la siguiente frase afirma; no hedge. "Es interesante tenerlo en cuenta" es la firma del relleno blando — quitar siempre.

**3. Pleonasmos y palabras-eco** (Strunk). Atajos de redundancia que el lector adulto detecta.

> *"si o si […] siempre"*
> *"aquella barrera de piedra impenetrable"*
> *"lo que cambia, en definitiva, es la pregunta"* (cuando la frase siguiente ya es lapidaria)

**Regla operativa**: dos palabras dicen lo mismo, una se va. "En definitiva" antes de cierre lapidario duplica función — quitar.

---

## Cómo usa el agente este digest

1. Cuando dudes entre dos opciones de reescritura, gana la que coincide con un move documentado aquí.
2. Cuando edites prosa de Marcela, aplica también los patrones de la sección O — no solo los antipatrones LLM.
3. Cuando una regla del SKILL.md parezca chocar con un sample real, gana el sample. Las reglas son aproximación; la voz es la evidencia.
