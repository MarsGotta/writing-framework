# Catálogo de prohibiciones — detalle

Cada prohibición con ejemplo, reescritura y diagnóstico. La calibración con los 4 samples de Marcela introduce matices: algunas palabras antes prohibidas valen en contextos específicos. La distinción está en cada entrada.

<!-- Origen: ambas STYLE.md §Prohibiciones + spanish-prose-craft §catálogo + humanizer §1-29 + calibration-digest.md §F, I, N (relajaciones) -->

---

## A. Léxico inflado

### A1. `magic`, `mágico`, `milagroso`

**Prohibido como tesis propia:**
- *Cline tiene un comportamiento casi mágico cuando lee tu codebase.*
**Reescritura:** *Cline lee tu codebase entera antes de proponer cambios. Eso explica por qué acierta más que un completion básico.*

**Permitido en boca del lector ingenuo (calibración):**
- *Cuando todo va bien parece que es magia o existe algun desarrollador diminuto que susurra al modelo. Pero cuando falla…* (Marcela, explanation samples)
- Aquí "magia" es atribución a la posición del lector ingenuo, marcada como tal y desmontada en las frases siguientes. Es la regla 4 de prosa con pulso.

**Diagnóstico:** la palabra prohibida cuando es afirmación; permitida cuando es la palabra que el lector usaría y la autora la trae para desmontarla.

### A2. `potente`, `revolucionario`, `transformador`, `disruptivo`

**Antes:** *El nuevo modelo es revolucionario y potente.*
**Después:** *El nuevo modelo procesa 200k tokens en menos de 3 segundos.*
**Diagnóstico:** adjetivos promocionales sin métrica. Sustituye por dato. Esta categoría no tiene relajación — siempre vende, no es voz.

### A2b. Léxico lúdico-coloquial (PERMITIDO, distinto del promocional)

La calibración demuestra que palabras como "superpoder", "arsenal", "parte aburrida", "nuestro ingenio" valen en la voz de Marcela. La distinción:

| Categoría | Ejemplo | Estado |
|---|---|---|
| Promocional vacío | "potente", "robusto", "holístico" | Prohibido (A1-A5) |
| Lúdico-coloquial | "superpoder", "arsenal", "parte aburrida" | Permitido |

**Ejemplo permitido (calibración):**
- *En este tutorial desbloquearemos un superpoder que antes no teníamos en nuestro arsenal.* (Marcela, tutorial sample)

**Diagnóstico:** el promocional vende, el lúdico baja registro y crea cercanía. La diferencia es función. Cuando dudes, pregunta: ¿estoy vendiendo o bajando el registro?

### A3. `holístico`, `integral`, `robusto`, `escalable`, `elegante`

**Antes:** *Una solución robusta, holística y escalable.*
**Después:** *Una solución que arranca en menos de un segundo y no requiere configuración para el caso por defecto.*
**Diagnóstico:** terna de adjetivos vacíos. Reemplaza por un dato concreto.

### A4. `aprovechar`, `potenciar`, `empoderar`, `unlock`, `leverage`

**Antes:** *Esta técnica te permite aprovechar al máximo el potencial del modelo.*
**Después:** *Con esta técnica, el modelo responde con un 30 % menos de tokens. La factura baja.*
**Diagnóstico:** verbos vacíos de marketing. Sustituye por efecto concreto.

### A5. `de vanguardia`, `state-of-the-art`, `última generación`

**Antes:** *Vitest es un framework de vanguardia para testing moderno.*
**Después:** *Vitest es la opción por defecto en proyectos con Vite. Arranca en menos de un segundo y soporta ESM nativo.*
**Diagnóstico:** sin fecha, "vanguardia" envejece en seis meses. Sustituye por hecho fechable.

---

## B. Verbos vacíos / cópula evasiva

### B1. `representar`, `constituir`, `suponer`

**Antes:** *Esto representa un avance.*
**Después:** *Esto es un avance.*
**Diagnóstico:** sustituyen `ser` por parecer más cultos. Vuelve al `ser`.

### B2. `erigirse como`, `emerger como`, `destacar por`

**Antes:** *Vitest se erige como la solución estándar para testing moderno.*
**Después:** *Vitest es la opción estándar en proyectos actuales.*
**Diagnóstico:** verbos promocionales de spec-sheet. Usa `ser` y acompaña con concreción.

### B3. `juega un papel`, `desempeña un rol`

**Antes:** *Los tests unitarios juegan un papel fundamental en la calidad.*
**Después:** *Los tests unitarios sostienen la calidad del código.*
**Diagnóstico:** calco de *play a role*. En español, "tienen un papel" o, mejor, verbo plenо.

### B4. `sirve como`, `funciona como`, `actúa como`

**Antes:** *Gallery 825 sirve como espacio de exposición.*
**Después:** *Gallery 825 es el espacio de exposición.*
**Diagnóstico:** copula avoidance. Vuelve al `ser`.

---

## C. Frases relleno

### C1. "Es importante destacar que…"

**Antes:** *Es importante destacar que los mocks aíslan la unidad bajo prueba.*
**Después:** *Los mocks aíslan la unidad bajo prueba.*
**Diagnóstico:** meta-lenguaje vacío. Si es importante, se ve.

### C2. "Cabe mencionar / vale la pena / huelga decir"

**Antes:** *Cabe mencionar que el modelo soporta function calling.*
**Después:** *El modelo soporta function calling.*
**Diagnóstico:** firma de la frase relleno sólida. Quitar.

### C2b. Hedging blando (calibración: tolerado puntual)

Frases como "hoy en día", "cada vez más", "lo más probable es que" se cuelan en la prosa de Marcela cuando baja el piloto automático. La calibración las tolera puntualmente como modulación de ritmo, pero las flagea cuando aparecen dos veces en la misma sección o cuando el contexto sostiene la afirmación directa.

**Tolerada (una vez por sección, modulación):**
- *"Hoy en día existen tres técnicas que podemos aplicar para este tipo de casos."*

**A reescribir cuando se acumula:**
- *"Hoy en día, cada vez más, está cogiendo relevancia."* → *"Desde 2024 es la base de cualquier integración seria."*
- *"Lo más probable es que nuestros prompts mejoren mucho de calidad."* → si llevas dos páginas sosteniendo argumento, afirma directo: *"Nuestros prompts mejoran de calidad."*
- *"Es interesante tenerlo en cuenta"* → quitar siempre. Es la firma del relleno blando.

**Diagnóstico:** las tres palabras ("hoy en día", "cada vez más", "es interesante") son patrón a vigilar de Marcela, no prohibición absoluta. La regla operativa: tolerar una vez como modulación, quitar la segunda aparición en la misma sección.

### C3. "A continuación vamos a / let's dive in / vamos a explorar"

**Antes:** *A continuación, vamos a proceder a analizar los resultados obtenidos.*
**Después:** *Analicemos los resultados.* / *Mira los resultados:*
**Diagnóstico:** anunciar lo que vas a hacer en vez de hacerlo. Elimina.

### C4. "Como bien sabemos / como ya hemos visto / sin más preámbulos"

**Antes:** *Como ya hemos visto, el harness es el conjunto de…*
**Después:** *El harness, como vimos en cap. 4, es el conjunto de… [enlace].*
**Diagnóstico:** si refieres material previo, enlaza concreto. Si no, no anuncies.

---

## D. Construcciones perfume IA

### D1. Em dash (—) por defecto

**Antes:** *Vitest —rápido, ESM nativo— es la opción —moderna y consolidada— para proyectos actuales.*
**Después:** *Vitest es rápido, funciona con ESM nativo y es la opción estándar en proyectos actuales.*
**Diagnóstico:** la raya está sobreusada en prosa LLM. En español, paréntesis o comas dobles son más naturales. Máximo una raya por párrafo. Cuando ninguna otra puntuación funciona y la raya es la mejor opción, úsala sin culpa — el "idealmente cero" anterior era rebote del antipatrón LLM, no diagnóstico.

### D2. Regla de tres decorativa

**Antes:** *Una solución rápida, clara y eficaz.*
**Después:** *Una solución rápida y clara.* / *Una solución que arranca en un segundo, no requiere configuración, no rompe el watch mode y se integra con Vite.*
**Diagnóstico:** ternas vacías son perfume IA. Pasa a dos elementos o a cuatro.

### D3. "No solo X sino también Y"

**Antes:** *No solo es rápido, sino también eficiente y escalable.*
**Después:** *Es rápido y eficiente. Escala bien.*
**Diagnóstico:** paralelismo negativo solo funciona si hay contraste real. Si es enumeración, cambia.

### D4. Paralelismos negativos en cadena

**Antes:** *No es un framework, es una filosofía. No es una herramienta, es un movimiento. No es código, es cultura.*
**Después:** *Vitest es un framework de testing. Lo que cambia respecto a Jest es la integración con Vite y el arranque por debajo del segundo.*
**Diagnóstico:** este patrón es el más reconocible de la prosa LLM. Cero tolerancia. Como mucho, una vez por capítulo.

### D5. Gerundio de posterioridad al cierre de frase

**Antes:** *Jest se integra con Vite, optimizando el rendimiento.*
**Después:** *Jest se integra con Vite: el rendimiento mejora.*
**Diagnóstico:** el gerundio final es el tic LLM más reconocible. Sustituye por dos puntos + oración, o por conector causal.

### D6. "Permite al desarrollador…" (calco de *allows the developer to*)

**Antes:** *Esto permite al desarrollador iterar más rápidamente.*
**Después:** *Con esto iteras más rápido.* / *El desarrollador puede iterar más rápido.*
**Diagnóstico:** `permitir + infinitivo` es calco. Prefiere `poder + infinitivo`, o verbo directo.

### D7. "En el corazón de…"

**Antes:** *En el corazón de Vitest hay un motor optimizado.*
**Después:** *El motor de Vitest está optimizado para ESM y arranque rápido.*
**Diagnóstico:** calco directo de *at the heart of*.

### D8. "Marca un antes y un después"

**Antes:** *La llegada de los agentes marca un antes y un después en el desarrollo.*
**Después:** *Con los agentes, el flujo cambia: ya no escribes el código, lo revisas. Eso reordena prioridades.*
**Diagnóstico:** cliché de marketing tecnológico. Sustituye por diferencia concreta.

### D9. "Dicho/a" anafórico (calibración: permitido en uso natural)

**Reescribir cuando suena claramente burocrático:**
- *La mencionada implementación representa un avance.* → *Esta implementación avanza: el arranque es la mitad de rápido.*

**Permitido en uso natural (calibración):**
- *No debemos recortar durante dicha transacción.* (Marcela, how-to sample)

**Diagnóstico:** "dicho/a" es jerga administrativa solo cuando va con verbo vacío ("representa", "constituye") o cuando se siente impostado. En frase corta funcional ("dicha transacción") la calibración demuestra uso natural. La prohibición v1 era excesiva — solo aplica cuando suma a otros patrones burocráticos.

---

## E. Apertura y cierre

### E1. Apertura con tesis genérica abstracta

**Antes:** *La inteligencia artificial está transformando la forma en que los desarrolladores escriben código.*
**Después:** *Cline acaba de proponer un cambio que toca seis archivos. Antes de aceptar, miramos el diff de uno por uno.*
**Diagnóstico:** la tesis genérica es contrato vacío. Apertura concreta: escena, objeto, dato o pregunta.

### E2. Apertura "imagina que…" (matizado)

**Prohibido cuando es tesis abstracta sin caso real:**
- *Imagina que tu equipo necesita procesar 10.000 documentos al día.*
**Reescritura:** *Tu equipo procesa 10.000 documentos al día. El pipeline actual tarda seis horas. La pregunta es si un modelo lo bajaría a una.*

**Permitido cuando es validación de intuición ingenua (calibración):**
- *Imaginemos que nuestro equipo empieza a trabajar con agentes. Cuando todo va bien parece que es magia o existe algun desarrollador diminuto que susurra al modelo. Pero cuando falla…* (Marcela, explanation sample)

Aquí "imaginemos" no es tesis abstracta: es invitación a un escenario compartido para luego desmontar la intuición. Es la regla 4 de prosa con pulso.

**Diagnóstico:** distinción de función. El "imagina que tienes un sistema X" sin caso concreto sigue siendo tesis vacía. El "imaginemos que…" como apertura de escenario que se va a afilar en las siguientes frases vale.

### E3. Cierre motivacional

**Antes:** *¡Ahora tienes las herramientas para conquistar cualquier reto! El futuro es brillante.*
**Después:** *Antes del siguiente capítulo, audita tu AGENTS.md con el rubric del anexo.*
**Diagnóstico:** cierre alto se evapora. Cierre bajo aterriza en la semana del lector.

### E4. "El viaje no termina aquí"

**Antes:** *El viaje no termina aquí. Esto es solo el comienzo de tu camino con la IA.*
**Después:** *El cap. 12 entra en el siguiente nivel: golden datasets y evals automatizados.*
**Diagnóstico:** moraleja-puente sustituida por bisagra concreta al siguiente capítulo.

---

## F. Tipográficas

### F1. Capitalización tipo inglés en titulares

**Antes:** *## Cómo Diseñar Un Harness Para Producción*
**Después:** *## Cómo diseñar un harness para producción*
**Diagnóstico:** sentence case en español. Solo capitaliza la primera palabra y los nombres propios.

### F2. MAYÚSCULAS para énfasis

**Antes:** *NUNCA hagas commit sin pasar por el linter.*
**Después:** *Nunca hagas commit sin pasar por el linter.* / *Nunca, sin excepción, hagas commit sin pasar por el linter.*
**Diagnóstico:** mayúsculas como énfasis es señal de prosa amateur. Cursiva si hace falta énfasis prosódico, o palabra de refuerzo.

### F3. Negrita mecánica en cada término

**Antes:** *El **render** de **Testing Library** monta el **componente** con sus **props**.*
**Después:** *La función `render` de Testing Library monta el componente con sus props.*
**Diagnóstico:** negrita solo en primer uso o cuando la palabra es foco genuino de la frase. Código → backticks, no negrita.

### F4. Emojis decorativos

**Antes:** *🚀 **Launch Phase:** El producto se lanza en Q3*
**Después:** *Fase de lanzamiento: el producto se lanza en Q3.*
**Diagnóstico:** cero emojis decorativos. Solo en tablas funcionales como icono de estado, raro y declarado.

### F5. Comillas curvas

**Antes:** *Dijo que "el proyecto va bien".*
**Después:** *Dijo que "el proyecto va bien".* (rectas) o *Dijo que «el proyecto va bien».* (latinas)
**Diagnóstico:** las curvas son ChatGPT. Convención del documento: rectas en ASCII, latinas en español formal.

---

## G. Vocabulario LLM-frecuente (alerta de revisión)

Si aparece, justificar o sustituir.

| Palabra | Sustitución típica |
|---|---|
| `testament` | (eliminar) / "muestra" / "señal" |
| `pivotal` | "decisivo", "clave" (con métrica) |
| `landscape` (abstracto) | "panorama", "campo", o concreto |
| `tapestry` (abstracto) | "conjunto", "mezcla", o concreto |
| `intricate`, `intricacies` | "complejo", "detalles", concreción |
| `delve` | "entrar en", "abrir", "mirar" |
| `underscore` (verbo) | "subraya", "muestra" |
| `highlight` (verbo) | "destaca" (con cuidado), "señala" |
| `enhance` | "mejora" + métrica |
| `garner` | "consigue", "obtiene" |
| `foster`, `fostering` | "fomenta", "ayuda a" |
| `interplay` | "relación", "conexión" |
| `vibrant` | "activo", "vivo" + dato |
| `enduring` | "duradero" (con cuidado), "que persiste" |
| `align with` | "coincidir con", "encajar con" |
| `crucial` (sin matiz) | "necesario", "imprescindible" + porqué |
| `key` (adjetivo, abuso) | concreción |
| `seamless` | "sin fricción", "directo" |

---

## H. Citas y datos

### H1. "Expertos dicen / industria reporta / estudios indican"

**Antes:** *Expertos del sector señalan que la IA cambiará el desarrollo.*
**Después:** *Simon Willison, en su post de marzo de 2026, argumenta que la IA cambia el desarrollo en tres dimensiones concretas: contexto, herramientas y observabilidad.*
**Diagnóstico:** atribución vaga = cero credibilidad. Toda cita: nombre + fecha + enlace.

### H2. Datos numéricos sin fuente

**Antes:** *El 70 % de los desarrolladores ya usa IA en su flujo diario.*
**Después:** *Stack Overflow Developer Survey 2025 reporta un 70 % de desarrolladores que usan IA en su flujo diario, sobre 65.000 respuestas.*
**Diagnóstico:** dato sin fuente = inventado. Toda cifra cita SOURCES.md o el origen explícito.

### H3. "Como vimos antes" sin link

**Antes:** *Como vimos antes, el context window condiciona el diseño del harness.*
**Después:** *Como vimos en cap. 04 §"context window y harness", el tamaño de la ventana condiciona el diseño del resto del sistema.*
**Diagnóstico:** referencia sin enlace = referencia perdida. Enlaza al sitio concreto.

---

## I. Lista vs. prosa

### I1. Bullet de tres puntos al inicio de sección

**Antes:**
> ## El context window
> - Es finito.
> - Tiene coste.
> - Decide qué sabe el modelo.

**Después:**
> ## El context window
>
> Es finito, tiene coste, y decide qué sabe el modelo. Tres restricciones que cualquier diseño de harness asume desde la primera línea.

**Diagnóstico:** si una sección tiene 3 bullets de una palabra, vuelve a prosa. Los bullets son para enumeración paralela larga, no para descomponer una frase.

### I2. Inline-header vertical lists con bullets bold + colon

**Antes:**
> - **Velocidad:** El sistema es rápido.
> - **Calidad:** El output es de alta calidad.
> - **Adopción:** Los usuarios lo adoptan.

**Después:**
> El sistema arranca en menos de un segundo, los outputs pasan los evals con una nota media de 8.4, y el equipo de plataforma ha desplegado el cliente en los 12 servicios en menos de un sprint.

**Diagnóstico:** inline-header vertical lists son firma LLM. Pasa a prosa.
