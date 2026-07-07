---
name: registro-tecnico-divulgativo
description: |
  Registro (capa 2) para guías técnicas divulgativas dirigidas a
  profesionales: formalidad profesional cercana, plural inclusivo,
  densidad de un concepto por movimiento con aterrizaje en artefacto,
  metáfora funcional con presupuesto, humor seco escaso, aserción con
  alcance y sin hedging, prosa que explica el porqué mientras código,
  tablas y datos muestran el qué. Se aplica sobre prosa-base (capa 1)
  y debajo de la voz del autor (capa 3). Es el default del sector
  tecnología; sirve para cualquier dominio técnico profesional.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# Registro: técnico-divulgativo

El género de este registro: la guía que enseña un tema técnico a profesionales
que lo van a aplicar. No es paper, no es post casual, no es documentación de
API. Su lector es un colega con criterio y con prisa: sabe leer, huele el
relleno, agradece que le hablen claro y abandona ante la solemnidad y ante el
colegueo por igual.

## Contrato del género

La prosa acompaña, no impresiona. Cada página deja al lector sabiendo hacer
algo o entendiendo por qué algo funciona como funciona, y se nota que quien
escribe ha pasado por ahí. La claridad manda sobre la exhaustividad: antes que
contarlo todo, contar lo que cambia decisiones. La precisión manda sobre el
brillo: antes que la frase memorable, la afirmación con su alcance. Y el texto
respeta el tiempo del lector: puede leerse entero o escanearse, y ambas
lecturas funcionan.

## Frontera de capas

Qué decide este registro y qué no:

| Decide este registro (capa 2) | Lo decide otra capa |
|---|---|
| Nivel de formalidad y cercanía del género | La firma personal (léxico lúdico, ironía concreta): voz, capa 3 |
| Persona gramatical y tiempo por defecto del género | Sus proporciones finas y excepciones calibradas: voz |
| Presupuesto de figuras (cuántas, de qué familia) | Qué metáfora concreta y si vuelve: voz |
| Densidad conceptual y ritmo prosa-artefacto | Cohesión entre frases y párrafos: prosa-base, capa 1 |
| Cómo se afirma (alcance, opinión técnica) | Qué es verificable y cómo se cita: contrato de citación y pasada 4 |
| Cadencia de definición de términos | Qué anglicismos admite el dominio: base de sector |
| Qué modula cada modalidad Diátaxis | La estructura del capítulo y la didáctica: sector y `technical-guide-design` |

## Diales

### 1. Formalidad: profesional cercana

Sin "usted", sin jerga administrativa ("procédase", "cabe señalar"), sin
solemnidad de tribunal. Y sin el extremo opuesto: sin colegueo de red social,
sin exclamaciones de entusiasmo, sin apelaciones tipo "amigo dev". El test:
¿esta frase se la dirías igual a una colega senior en una reunión de trabajo?
Si suena a ponencia leída o a hilo viral, está fuera de registro.

### 2. Persona y tiempo: plural inclusivo en presente

El plural inclusivo por conjugación ("montamos", "vemos", "medimos") es la
marca del género en divulgación técnica en español: lleva a autor y lector
juntos sin paternalismo. Presente del indicativo como tiempo base. El tú
implícito entra en instrucciones puntuales ("lanza el evaluador"); el
impersonal sostenido ("se configura", "se procede") queda fuera como registro
dominante. Las proporciones finas por autor las calibra la voz.

### 3. Densidad: un concepto por movimiento, con aterrizaje

Cada movimiento del texto introduce como mucho un concepto nuevo, y ningún
concepto se queda en el aire: antes de tres párrafos aterriza en un artefacto
concreto (un comando con su salida, un fragmento de código, una tabla, un
número con fuente, un caso con nombre). La abstracción sostenida sin
aterrizar es deriva académica; la lista de artefactos sin explicación del
porqué es deriva de changelog.

### 4. Figuras: metáfora funcional con presupuesto

Una metáfora por concepto fuerte, de familia doméstica o mecánica (mesa,
taller, tubería, mudanza), nunca cósmica ni épica. La metáfora se usa y se
cierra: si el context window es una mesa de trabajo, la frase siguiente
vuelve al término técnico. Presupuesto de género: si un capítulo acumula más
de tres metáforas, sobra alguna. Cero figuras ornamentales (aliteraciones,
personificaciones decorativas, imágenes que no explican nada).

### 5. Humor: seco, breve y al servicio de la comprensión

El género admite humor cuando libera tensión o fija una idea, siempre
enrollado en la frase técnica, nunca como chiste aparte ni como relleno
simpático. Presupuesto: una aparición por capítulo como criterio. El sabor
exacto (ironía entre paréntesis, observación cómplice) lo decide la voz.

### 6. Aserción: con alcance y sin hedging

El género afirma. Cada afirmación lleva su alcance cuando lo necesita
(versión, fecha, condición: "con Vitest 4.x", "verificado en marzo de 2026",
"en repos con CI"), y a cambio no se protege con hedging blando ("podría
decirse", "en cierto modo", "es interesante tenerlo en cuenta"). La opinión
técnica es legítima marcada como tal ("mi criterio aquí:"). Lo que un senior
puede pinchar con un caso límite, se acota antes de publicar.

### 7. Terminología: definición operativa y sin ceremonia

El término técnico llega con una definición de una frase en su primer uso y
se sigue (la excepción, cuando hay intuición previa que desmontar, la regula
la voz). Un concepto, un término, toda la guía. Los anglicismos admitidos los
fija la base de sector; este registro solo exige la cadencia: definir al
entrar, no ceremonializar ("antes de definir, reflexionemos") ni duplicar con
sinónimos elegantes.

### 8. Prosa y artefacto: el porqué en prosa, el qué en el artefacto

La prosa explica decisiones, causas y consecuencias; el código, la tabla y la
traza muestran el objeto. Ni prosa que parafrasea línea a línea lo que el
código ya dice, ni bloques de código huérfanos sin una frase que diga qué
mirar. Después de cada artefacto, la primera frase recoge lo que el lector
acaba de ver y lo convierte en argumento (el eco de prosa-base aplica también
tras un bloque de código).

## La escala

El mismo contenido en tres registros. El del medio es el nuestro.

**Deriva académica (fuera de registro):**

> La gestión del contexto constituye uno de los desafíos fundamentales en el
> despliegue de sistemas basados en LLM. La literatura reciente ha señalado
> que la degradación del rendimiento asociada a la saturación de la ventana
> de contexto resulta significativa, por lo que se recomienda la adopción de
> estrategias de compactación.

(Nominalizaciones encadenadas, impersonal, "constituye", cero artefactos:
nadie hace nada y no se ve nada.)

**Deriva blog-casual (fuera de registro):**

> Ojo con el contexto, que se te llena en nada y el modelo empieza a
> alucinar cosas rarísimas. Nos ha pasado a todos, ¿no? La solución es
> facilísima: compactas y a correr.

(Colegueo, hipérbole, "facilísimo" promocional, cero alcance: un senior lo
pincha en dos segundos.)

**Técnico-divulgativo (nuestro registro):**

> Cuando el context window se acerca al límite, el modelo empieza a perder
> lo que le dijimos al principio. Lo vemos en la práctica con una sesión
> larga de refactor: hacia la iteración veinte, el agente reescribe un test
> que habíamos acordado no tocar. Tenemos tres salidas: ampliar la ventana
> (cara y con techo), resetear la conversación (perdemos estado) o
> compactar. Las dos primeras son parches; la tercera es la que se
> automatiza, y la montamos en el capítulo siguiente.

(Plural inclusivo, caso concreto aterrizado, opciones con su coste, cierre
que prepara el siguiente movimiento.)

## Deriva: síntomas y corrección

El texto de una guía técnica se desliza hacia tres imanes. Síntomas:

- **Hacia lo académico**: crecen las nominalizaciones ("la implementación de
  la solución"), aparece el impersonal sostenido, los párrafos pasan de
  cinco frases sin artefacto, el lector deja de aparecer en la conjugación.
  Corrección: verbos plenos, plural inclusivo, aterrizar en artefacto.
- **Hacia el blog casual**: exclamaciones, hipérboles ("brutal", "una
  pasada"), preguntas retóricas en cadena, afirmaciones sin alcance.
  Corrección: quitar el énfasis, poner el dato y su fuente, acotar.
- **Hacia el folleto**: adjetivos de producto ("potente", "robusto",
  "seamless"), beneficios sin mecanismo, entusiasmo por la herramienta en
  vez de por lo que el lector logra. Corrección: sustituir el adjetivo por
  el hecho que lo justificaría; si no hay hecho, fuera la frase.

La pasada de naturalidad marca la deriva citando el dial violado.

## Registro por modalidad Diátaxis

El registro modula distinto según la modalidad del bloque: tutorial en
registro escena (narración en plural inclusivo, cada paso muestra su
resultado), how-to en registro receta (plural inclusivo modal, imperativo
puntual, sin preámbulo), reference en registro catálogo (prosa mínima,
tablas, cero figuras, cero humor) y explanation en registro argumento
(tesis, contraste, evidencia; aquí viven las metáforas y el paréntesis).

El detalle con ejemplos antes/después vive en
`references/voz/references/registros-por-modalidad.md`. Ese documento está
calibrado con la voz de Marcela; su mapa modalidad → registro vale para
cualquier autor, sus proporciones exactas son de capa 3.

## Checklist de registro

1. ¿Cada frase pasaría en una reunión con una colega senior (ni ponencia ni
   hilo viral)?
2. ¿El plural inclusivo es el plano dominante y el impersonal no se
   sostiene más de una frase?
3. ¿Cada concepto nuevo aterriza en un artefacto concreto antes de tres
   párrafos?
4. ¿Ninguna metáfora es cósmica y ninguna se queda abierta? ¿Tres o menos
   por capítulo?
5. ¿El humor (si hay) va dentro de la frase técnica y no pasa de una
   aparición por capítulo?
6. ¿Toda afirmación fuerte lleva su alcance (versión, fecha, condición) y
   no hay hedging blando?
7. ¿Cada término técnico se define en una frase en su primer uso y no
   cambia de nombre después?
8. ¿Después de cada bloque de código o tabla, la primera frase recoge lo
   que se acaba de ver?
9. ¿El texto funciona leído entero y también escaneado?
10. ¿No hay deriva académica, casual ni de folleto (ver síntomas)?

## Origen

Decisión propia del proyecto (2026-07-04), calibrada contra la guía de
referencia del sector tecnología (`guide-ai-developers-basic`) y las fuentes
didácticas ya incorporadas al preset: andragogía (Knowles) para el trato de
par a par, Diátaxis para la modulación por modalidad, y el análisis de
divulgadores técnicos de `references/voz/references/referentes.md` (Willison,
Evans, Karpathy, Yan, Boykis) del que este registro toma lo común del género
y deja lo personal a la capa de voz.

## Versión

v1.0.0 (2026-07-04). Primer registro de la capa 2; default del sector
tecnología.
