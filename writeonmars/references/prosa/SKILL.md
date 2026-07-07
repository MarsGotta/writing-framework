---
name: prosa-base
description: |
  Cimiento de prosa fluida para todo texto generado por el pipeline,
  en cualquier género y registro. Enseña a conectar: progresión de
  información conocida a nueva (tema-rema), frases completas, eco
  léxico entre frases y párrafos, transiciones con porqué, párrafo
  como movimiento del argumento y ritmo de crucero. Es la capa 1 de
  la pirámide de prosa (prosa-base → registro de guía → voz del
  autor). Se carga SIEMPRE en redacción y en pasada 3, antes que la
  skill de voz. No impone voz ni personalidad: hace que el texto se
  lea como un tejido y no como frases pegadas.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# prosa-base

Toda la pila de estilo del framework dice qué no hacer: no frases largas, no
conectores cultos, no lenguaje promocional, no muletillas LLM. Esta skill dice
qué hacer. Un agente que solo conoce prohibiciones juega seguro y produce
frases cortas, correctas y muertas, puestas una detrás de otra como cuentas
sin hilo. El lector nota las costuras, lee tres párrafos y abandona.

La prosa-base es el hilo. Se aplica antes que cualquier registro (académico,
narrativo, poético) y antes que cualquier voz de autor. Ningún estilo legítimo
la contradice: una prosa académica fluye, una prosa poética fluye, la voz de
Marcela fluye. Lo que cambia por encima es el color, no la costura.

## Dónde encaja (la pirámide)

1. **Capa 1, prosa-base (esta skill).** Cohesión, fluidez, frases completas.
   Universal, siempre cargada, innegociable.
2. **Capa 2, registro de la guía.** El contrato estilístico del género
   (`../registros/<slug>/SKILL.md`): formalidad, densidad, figuras,
   aserción. Se declara en las adendas y el manifiesto; disponible:
   `tecnico-divulgativo` (pendientes: académico, narrativo, poético). Se
   carga después de esta.
3. **Capa 3, voz del autor.** `marcela-prose` u otra skill de voz personal.
   Decide léxico, humor, aperturas, cierres, firma.

En conflicto, la capa superior gana en todo salvo en dos innegociables de la
capa 1: frases completas y progresión conocido → nuevo. Un cierre lapidario de
la voz puede ser cortísimo; lo que no puede es dejar una enumeración huérfana
o arrancar de cero ignorando la frase anterior.

## Cuándo aplicar

- Siempre que el pipeline redacta prosa nueva (capítulos, secciones, posts).
- En pasada 3 (naturalidad), como criterio de diagnóstico y reescritura.
- Al reparar texto que suena a "frases pegadas" o a esquema disfrazado.

## Cuándo NO aplicar

- Contenido de catálogo puro (tablas, glosarios, listas de referencia): ahí
  no hay hilo narrativo que proteger.
- Citas textuales de otros autores.
- Código y comentarios de código.

---

## Principio rector: cada frase nace de la anterior

Un texto fluido no es una colección de frases correctas: es una cadena donde
cada eslabón engancha con el anterior. El lector nunca debería ensamblar las
piezas; el texto llega ensamblado. La pregunta de diagnóstico es siempre la
misma: ¿esta frase recoge algo de la anterior, o arranca en frío?

**Test del barajado**: si puedes cambiar de orden las frases de un párrafo y
se entiende igual, el párrafo no tiene hilo. Es una lista con puntos en vez
de viñetas. Un párrafo cosido no sobrevive al barajado: cada frase necesita
a la anterior.

---

## Las 7 reglas del hilo

### 1. Frases completas: el fragmento es firma de nota, no de prosa

Toda oración lleva verbo conjugado y sujeto recuperable. El fragmento sin
verbo ("Convertir el texto en algo contable, elegir cómo representarlo.")
es la firma del esquema que nadie redactó.

El caso más frecuente en el pipeline: la enumeración de infinitivos soltada
tras punto. Se repara enganchándola con dos puntos a la frase que la anuncia,
o dándole un verbo matriz.

**Antes (enumeración huérfana, caso real del pipeline):**
> Entre esa reseña y un modelo que la clasifique como positiva hay un trecho,
> y ese trecho tiene pasos con nombre. Convertir el texto en algo contable,
> elegir cómo representarlo, entrenar un modelo encima y comprobar si acierta.

**Después (enganchada con dos puntos):**
> Entre esa reseña y un modelo que la clasifique como positiva hay un trecho,
> y ese trecho tiene pasos con nombre: convertir el texto en algo contable,
> elegir cómo representarlo, entrenar un modelo encima y comprobar si acierta.

**Después (con verbo matriz, si la frase anterior ya quedó larga):**
> Ese trecho tiene pasos con nombre. Hay que convertir el texto en algo
> contable, elegir cómo representarlo, entrenar un modelo encima y comprobar
> si acierta.

El fragmento deliberado existe como recurso retórico ("Es el problema.") y
la capa de voz lo usa. Límite de esta capa: uno por sección, y solo si el
párrafo anterior lo prepara. Dos fragmentos por página es esquema, no estilo.

### 2. Progresión conocido → nuevo (tema-rema)

Cada frase arranca de algo que el lector ya tiene (el tema: lo mencionado en
la frase anterior o lo sabido del capítulo) y añade una cosa nueva (el rema).
Cuando una frase arranca directamente con información nueva, el lector frena
para recolocarse; tres frenazos seguidos y el texto "no engancha".

Tres patrones de progresión, los tres válidos:

**Lineal**: lo nuevo de una frase se vuelve lo conocido de la siguiente.
Ideal para explicar procesos y causas.

> El modelo no recibe frases: recibe matrices de números. Esas matrices salen
> de un paso previo llamado vectorización. La vectorización decide, antes de
> entrenar nada, qué información sobrevive y cuál se pierde.

(matrices → esas matrices; vectorización → la vectorización. Cadena.)

**De tema constante**: varias frases seguidas hablan del mismo sujeto y cada
una añade un dato. Ideal para describir un objeto o sistema.

> TF-IDF cuenta y pesa palabras. No sabe que dos palabras significan algo
> parecido, ni le hace falta para muchas tareas. Donde se queda corto es en
> la similitud: para TF-IDF, "bueno" y "excelente" son tan distintos como
> "bueno" y "cucaracha".

**De tema derivado**: un marco anunciado se despliega en partes. Ideal para
secciones con estructura anunciada ("tres opciones: A, B y C", y cada párrafo
abre con una).

Regla operativa: al escribir cada frase, pregunta con qué palabra o idea de la
frase anterior conecta. Si la respuesta es "con ninguna", o falta un eslabón
o la frase va en otro párrafo.

### 3. El eco: cohesión léxica explícita

El hilo se hace visible con material léxico, no solo con conectores. Tres
mecanismos, por orden de preferencia:

- **Repetir el término ancla.** "La vectorización decide… La vectorización
  también fija…". La repetición del término técnico exacto no es pobreza:
  es univocidad (constitución § IV) y es cohesión.
- **Demostrativo + sustantivo.** "ese trecho", "esa decisión", "este paso".
  Nunca el demostrativo suelto ("eso", "esto") sin sustantivo: el pronombre
  vago rompe el referente (constitución § I).
- **Conector casual con contenido.** "Así que", "Pero", "Por eso". El
  conector solo funciona si las dos frases ya comparten material; no pega
  frases que no se tocan.

Y la versión de párrafo: **la primera frase de cada párrafo recoge una
palabra o una idea del párrafo anterior antes de introducir la suya.** Es la
regla del eco. Sin eco, cada párrafo es un arranque en frío y el capítulo se
lee como fichas de estudio.

**Antes (párrafos sin eco):**
> …y para TF-IDF esas dos columnas no tienen nada que ver entre sí.
>
> Los embeddings son vectores densos entrenados sobre contextos.

**Después (con eco):**
> …y para TF-IDF esas dos columnas no tienen nada que ver entre sí.
>
> Ese "no tienen nada que ver" es el agujero que abrimos aquí: necesitamos
> una representación que sí sepa que dos palabras se parecen. Esa
> representación existe y se llama embedding.

### 4. Transiciones con porqué

Cada cambio de tema explica por qué ocurre ahora. "Vamos a verlo" y "Pasemos
al siguiente punto" son transiciones secas (constitución § I): anuncian
movimiento sin motivo. La transición con porqué nombra la causa del salto.

**Antes:** > Quedan tres categorías.
**Después:** > Con esa distinción podemos separar tres casos.

**Antes:** > Vamos a verlo.
**Después:** > Para entender por qué ocurre, hay que mirar qué entra
> realmente en el contexto.

La prueba: quita la transición. Si el texto se entiende igual, la transición
era ornamento; escríbela de nuevo con el motivo dentro.

### 5. El párrafo es un movimiento, no un contenedor

Un párrafo hace avanzar el argumento un paso: plantea, desarrolla, deja el
pie para el siguiente. Estructura por defecto:

- **Frase de apertura** que orienta: qué mira este párrafo (y con eco del
  anterior, regla 3).
- **Desarrollo**: dos a cinco frases encadenadas por tema-rema (regla 2).
- **Salida**: la última frase o cierra el movimiento o prepara el siguiente.
  No se abandona el párrafo en un dato suelto.

Síntoma de fallo: párrafos de una o dos frases en cadena. Uno vale como
golpe; tres seguidos son un esquema al que quitaron las viñetas.

### 6. Ritmo de crucero: la media manda, la corta remata, la larga despliega

La frase media (15 a 25 palabras) es el pulso base de la prosa. La corta
existe para rematar o girar, y solo golpea si la media la preparó. La larga
existe para desplegar un argumento que no cabe en dos frases, y se permite
una por sección.

Alarma de staccato: **tres frases de menos de 8 palabras seguidas** piden
revisión, salvo efecto retórico buscado y preparado. El staccato no es
sobriedad: es el modo de fallo de un redactor que teme a la subordinada.
Una subordinada bien puesta ("que", "cuando", "aunque", "porque") no es
frase amontonada: es el argumento respirando dentro de la frase.

**Antes (staccato, ritmo de fichas):**
> TF-IDF cuenta palabras. También las pesa. No entiende significados. Dos
> sinónimos son columnas distintas. Esto limita la similitud.

**Después (ritmo de crucero):**
> TF-IDF cuenta y pesa palabras, y con eso resuelve más tareas de las que
> parece. Lo que no sabe es que dos palabras significan algo parecido: para
> él, cada sinónimo vive en una columna distinta. Esa ceguera se paga al
> medir similitud.

### 7. Anclas de lectura, con cuentagotas

Frases que orientan la atención del lector adulto: "Quédate con esta idea",
"No necesitas memorizar esto", "En la práctica esto significa…", "El síntoma
típico es…". Bajan la carga cognitiva porque separan lo esencial de lo
ilustrativo. Una o dos por capítulo; más, y se vuelven tic.

---

## Playbook de cosido (para reparar texto ya escrito)

Cuando un texto suena a frases pegadas, en este orden:

1. **Busca fragmentos sin verbo.** Engancha con dos puntos o da verbo matriz
   (regla 1). Es la reparación más barata y la de mayor efecto.
2. **Pasa el test del barajado por párrafo.** Donde el orden dé igual, falta
   cadena: reescribe con progresión conocido → nuevo (regla 2).
3. **Revisa la primera frase de cada párrafo.** ¿Tiene eco del anterior? Si
   no, añádelo o justifica el corte (cambio de sección, regla 3).
4. **Caza transiciones secas** y reescríbelas con su porqué (regla 4).
5. **Funde párrafos-ficha.** Dos o más párrafos de una frase que hablan de lo
   mismo se cosen en un movimiento (regla 5).
6. **Mide el ritmo.** Donde haya tres cortas seguidas sin intención, funde
   dos con una subordinada o un conector con contenido (regla 6).

No lo hagas todo en una pasada: una regla por pasada conserva la voz y quita
la fricción.

## Checklist de generación (al redactar, no después)

1. ¿Cada frase tiene verbo conjugado, o el fragmento es deliberado y único?
2. ¿Cada frase recoge algo de la anterior (palabra, idea, demostrativo con
   sustantivo)?
3. ¿La primera frase del párrafo tiene eco del párrafo anterior?
4. ¿Cada transición lleva su porqué dentro?
5. ¿El párrafo termina cerrando o preparando, no en un dato suelto?
6. ¿El pulso es de frase media, con cortas que rematan y una larga como
   máximo por sección?
7. ¿Sobrevive el párrafo al test del barajado? (Si sobrevive, mal.)
8. ¿Se puede leer en voz alta sin notar las costuras?

## Interacción con otras skills

- **`marcela-prose` (capa 3)** decide voz, léxico, aperturas, cierres y
  prohibiciones finas. Se aplica después de esta skill sobre el mismo texto.
  Sus cierres lapidarios y fragmentos de firma están permitidos dentro del
  límite de la regla 1.
- **Skills de registro (capa 2, futuras)** modulan formalidad, densidad y
  figuras. Ninguna podrá derogar frases completas ni progresión conocido →
  nuevo.
- **`writeonmars-redaccion` y `writeonmars-pasada-3`** cargan esta skill
  siempre: el redactor para generar con hilo, la pasada 3 para diagnosticar
  con el playbook de cosido.

## Origen

Progresión tema-rema: perspectiva funcional de la oración (escuela de Praga)
y Joseph Williams (*Style*, principio known → new). Párrafo como movimiento:
Cassany (*La cocina de la escritura*). Arcos de coherencia: Pinker (*The
Sense of Style*). Transiciones con porqué y anclas de lectura:
`references/didactica/references/prose-pitfalls.md` (entradas 6 y bonus),
que este documento traduce y promueve a regla de generación. Casos antes /
después: capítulos reales del pipeline (julio 2026).

## Versión

v1.0.0 (2026-07-04). Nace del diagnóstico "frases pegadas" sobre guías
generadas: la pila era 90 % prohibición y 10 % construcción, y ningún
documento enseñaba a conectar frases. Esta skill es la capa que faltaba.
