# Defectos de prosa en guías técnicas

Catálogo de microestilo para escritura técnica dirigida a desarrolladores
profesionales. Compañero de `SKILL.md`. Úsalo al revisar prosa que es sólida
en estructura pero se lee comprimida, mecánica o robótica.

El diagnóstico general detrás de cada entrada: un problema de prosa casi
nunca viene de falta de información. Viene de **exceso de compresión**. Quien
escribe resumió sus propias notas en vez de guiar a quien lee.

El patrón de remedio, aplicable a todas las entradas:

> **situación → explicación → consecuencia práctica**

El lector no debería reconstruir la intención desde una frase apretada. Una
guía que merece el nombre, guía.

Siguen ocho defectos, cada uno con el patrón, por qué falla, ejemplos y la
regla de reescritura.

---

## 1. Frases comprimidas (concepto + metáfora + conclusión en una línea)

**Síntoma.** Una sola frase intenta entregar tres cosas a la vez: definir,
ilustrar y concluir.

**Por qué falla.** El lector tiene que desempaquetar la frase en su cabeza.
El texto se lee como notas internas del autor, no como una explicación
escrita para otra persona.

**Ejemplo malo:**

> Cabe en la cabeza, deja sitio para que cada concepto técnico aterrice en
> algo reconocible y evita el bullet hipotético del tipo "imaginemos un
> sistema X".

(Tres ideas, dos metáforas, un término en inglés, un ejemplo anidado. El
lector tiene que mapearlo todo.)

**Ejemplo mejor:**

> El ejemplo es pequeño a propósito. Una API REST de tareas es fácil de
> seguir y es suficiente para hablar de validación, tests, contexto,
> memoria, herramientas y revisión de PRs sin cambiar de escenario en cada
> capítulo.

**Regla de reescritura.** Si una frase contiene *concepto + metáfora +
conclusión*, pártela. Dos frases claras ganan a una ingeniosa.

---

## 2. Pronombres vagos ("lo", "eso", "esto", "aquello")

**Síntoma.** Un pronombre hace el trabajo que debería hacer el sustantivo.

**Por qué falla.** El lector tiene que volver atrás para averiguar a qué se
refiere. Aunque el referente sea técnicamente deducible, el coste cognitivo
es real y la prosa se siente inconexa.

**Ejemplos malos:**

> Eso cambia la forma de revisar.
>
> Desarrolladores que sienten que "lo aceptan a ciegas" cuando el agente
> entrega un PR y quieren cambiar eso.

**Ejemplos mejores:**

> Tener una _spec_ cambia la revisión: ya no preguntamos si el código
> "parece bien", preguntamos si cumple lo acordado.
>
> Personas que ya reciben PRs generados por agentes y sienten que a veces
> aprueban cambios que no entienden del todo.

**Regla de reescritura.** Sustituye `lo / eso / esto` por el sujeto concreto
la primera vez que aparece. La segunda mención puede pronominalizar sin
ambigüedad.

---

## 3. Cadenas de aforismos ("no es X: es Y" repetido)

**Síntoma.** Sección tras sección cerrando con un sentencioso "no es X: es
Y", "no se hace A: se hace B" o pareja negación-afirmación similar.

**Por qué falla.** Sueltas, estas frases funcionan. Apiladas, fabrican tono
de eslogan y el texto empieza a parecer un manifiesto escrito para pósteres.

**Ejemplos malos (en racimo):**

> La economía no es opcional: es estructural.
>
> Cuando el presupuesto importa, no se estima: se mide.
>
> Delegar lo que no podemos juzgar es no delegar: es aceptar a ciegas.

**Ejemplos mejores:**

> El coste forma parte del diseño del agente. Cada archivo leído, cada
> resultado de herramienta y cada respuesta generada vuelve a ocupar
> contexto y presupuesto.
>
> Si el coste importa, mide una sesión real. Las estimaciones a ojo suelen
> fallar porque el gasto depende del historial, las herramientas, las
> iteraciones y la salida generada.

**Regla de reescritura.** Máximo **una frase aforística por capítulo**, y
solo cuando se gana el sitio. El resto de frases-golpe se convierten en
explicaciones con sujeto + causa.

---

## 4. Metáforas mezcladas

**Síntoma.** Dos o más imágenes incompatibles en la misma frase (espacial +
aterrizaje + "en la mano" + "mueve la aguja").

**Por qué falla.** El lector tiene que reconciliar imágenes que no encajan
entre sí, y eso cuesta más de lo que la metáfora ahorra.

**Ejemplos malos:**

> deja sitio para que cada concepto técnico aterrice en algo reconocible
>
> Modelos parecidos, montados en harnesses distintos, dan agentes que se
> sienten radicalmente distintos en la mano.

**Ejemplos mejores:**

> permite explicar cada concepto con el mismo ejemplo
>
> El mismo modelo puede comportarse de forma muy distinta según el harness
> que lo rodee.

**Regla de reescritura.** Una metáfora por concepto, y solo si aclara. Si la
metáfora obliga a reinterpretar, quítala. Domésticas y mecánicas antes que
cósmicas o sensoriales.

---

## 5. Anglicismos que no añaden precisión

**Síntoma.** Términos en inglés salpicados por la prosa española donde
existe una palabra española limpia y sin ambigüedad.

**Lista blanca (se quedan en inglés):** `harness`, `MCP`, `tool use`,
`system prompt`, `context window`, `prompt`, `skill`, `spec`,
`output`/`input` solo al hablar de precios.

**A traducir por defecto:**

| Inglés           | Mejor en español                                  |
| ---------------- | ------------------------------------------------- |
| mental model     | modelo mental                                     |
| scope            | alcance                                           |
| baseline         | línea base / punto de partida                     |
| inline           | dentro del propio código / mezclada en lógica     |
| datasource       | fuente de datos                                   |
| built-in         | nativa / integrada                                |
| bullet           | viñeta / lista                                    |
| fork             | duplicación de mantenimiento (cuando es figurado) |

**Regla.** Inglés solo cuando el término es el canónico de la disciplina o
cuando traducir crea ambigüedad. La inercia no es una razón. (La lista
admitida por dominio la fija la base de sector; esta tabla es el criterio
general.)

---

## 6. Transiciones secas ("Vamos a verlo", "Quedan tres categorías")

**Síntoma.** Conector pelado al inicio de un párrafo o tras una lista, sin
explicar por qué pasamos de la idea A a la idea B.

**Por qué falla.** El texto se lee como un esquema, no como un documento
terminado. El lector nota las costuras.

**Ejemplos malos:**

> Vamos a ese tema.
>
> Quedan tres categorías:
>
> Vamos a verlo.

**Ejemplos mejores:**

> Ese presupuesto nos lleva al siguiente problema: los tokens.
>
> Con esa distinción podemos separar tres casos:
>
> Para entender por qué ocurre, hay que mirar qué entra realmente en el
> contexto.

**Regla de reescritura.** Toda transición responde al **porqué ahora**: por
qué esta idea sigue a aquella, por qué esta lista de tres aparece aquí.

---

## 7. Repetición mecánica de títulos de sección y entradas

**Síntoma A.** Todos los capítulos cierran con una sección llamada igual:
"## La trampa común" cinco capítulos seguidos. Todos los capítulos entran al
ejemplo recurrente con "Volvamos a…".

**Por qué falla.** El esqueleto previsible baja la carga cognitiva. La
*piel* previsible fabrica sensación de plantilla.

**Mecánico (malo):**

```
## La trampa común: confundir A con B
## La trampa común: confundir C con D
## La trampa común: confundir E con F
```

**Variado (mejor):**

```
## A no es B
## Dónde se suele escapar el coste
## Lo que una ventana grande no soluciona
```

**Síntoma B.** Toda entrada al ejemplo recurrente usa "Volvamos al ejemplo
de…".

**Variado (mejor):**

> En la API de tareas, esto aparece de forma concreta cuando…
>
> El mismo problema se ve en el _endpoint_ POST /tasks.
>
> Pensemos en la paginación de GET /tasks.

**Regla de reescritura.** Misma estructura entre archivos; redacción variada
en títulos y entradas. Tres formulaciones alternativas por bloque recurrente
ganan a una formulación fija.

---

## 8. Afirmaciones absolutas que la audiencia puede pinchar

**Síntoma.** Una frase suena limpia y citable, pero un desarrollador senior
que la lee conoce el caso límite que la rompe.

**Por qué falla.** Pérdida de confianza. El lector deja de leer la frase y
empieza a discutir con ella.

**Ejemplos malos:**

> Si algo no está en el contexto, para el modelo no existe.
>
> El agente no recibió un script.

**Ejemplos mejores:**

> Si algo no está en el contexto ni puede recuperarse mediante una
> herramienta, el modelo no puede usarlo de forma fiable en esa llamada.
>
> En esta sesión, el agente no recibió un script: decidió cada paso a partir
> del estado del repositorio.

**Regla de reescritura.** Añade palabras de alcance cuando la versión
universal se pasa: *en una sesión típica, normalmente, en muchos
`harnesses`, en este ejemplo*. La precisión gana más confianza que el
eslogan.

---

## Extra: señales de orientación al lector

No es un defecto, es una táctica. El movimiento opuesto a la compresión.
Frases periódicas que bajan la carga cognitiva señalando qué retener y qué
escanear.

Ejemplos que funcionan en español técnico:

- **"Quédate con esta idea."** Cuando un párrafo carga todo el argumento.
- **"No necesitas memorizar X."** Cuando un detalle se muestra por
  completitud.
- **"En la práctica esto significa…"** Puente del concepto a la acción.
- **"El síntoma típico es…"** Ancla la abstracción a un caso reconocible.
- **"Si solo lees esta sección, lee esto."** Ruta rápida explícita.

Una guía para profesionales adultos respeta más su atención señalando lo que
importa que siendo uniformemente densa.

---

## Pasada de microedición: el orden de aplicación

Al auditar prosa sólida en estructura pero que se lee rara, pasa en este
orden:

1. **Pronombres vagos** (entrada 2). El arreglo más barato y el de mayor
   impacto en legibilidad.
2. **Frases comprimidas** (entrada 1). Parte todo lo que mezcle más de dos
   ideas.
3. **Cadenas de aforismos** (entrada 3). Deja como mucho una por capítulo.
4. **Repetición mecánica** (entrada 7). Varía títulos y entradas.
5. **Transiciones secas** (entrada 6). Añade el porqué-ahora a cada
   conector.
6. **Metáforas mezcladas** (entrada 4). Degrada o elimina.
7. **Anglicismos innecesarios** (entrada 5).
8. **Afirmaciones absolutas** (entrada 8).

No las pases todas en una sola pasada con el objetivo de "humanizar". Cada
pasada con una sola regla en mente. El texto conservará su voz y perderá la
fricción.

---

Traducción al español: 2026-07-04. En el pipeline, el cosido de frases y
párrafos lo gobierna `references/prosa/SKILL.md` (prosa-base), que acredita
este catálogo como fuente de sus reglas de transiciones y señales de
orientación; las entradas siguen valiendo como catálogo de diagnóstico.
