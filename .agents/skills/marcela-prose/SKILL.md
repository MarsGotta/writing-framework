---
name: marcela-prose
description: |
  Edita prosa técnica española aplicando la voz de Marcela: autora
  escribiendo prosa deliberada para libro, guía o artículo. Plural
  inclusivo dominante, paréntesis honesto en tres modalidades
  (didáctico, irónico, editorial), antropomorfización del agente,
  metáforas sensoriales únicas, cierres bajos. Cubre estructura
  pedagógica (Diátaxis), arquitectura de capítulo (McPhee, Yan, Boykis),
  postura del autor (Pinker, Klinkenborg), prosa española natural
  (RAE/Fundéu/Cassany/Grijelmo) y limpieza de patrones LLM en una sola
  pasada. Calibrada con 4 muestras antes/después editadas por Marcela.
  No reescribir voces ajenas (citas, prosa de otros autores): solo
  material propio o explícitamente marcado como suyo.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# marcela-prose

Edita prosa técnica española para que suene a Marcela como autora: prosa escrita y deliberada, con ritmo, sin marketing, sin moralina, con cicatriz propia cuando aporta. No es transcripción de una conversación; es texto compuesto para libro, guía, capítulo o artículo largo. La skill es autónoma: no depende de `humanizer`, `spanish-prose-craft` ni `technical-guide-design`. Absorbe lo necesario de las tres y cierra con la voz personal calibrada.

## Cuándo aplicar

- Redacción de capítulos, secciones o posts técnicos largos en español.
- Revisión de drafts (propios o de un agente) antes de commit.
- Reescritura de material que suena a "limpio genérico" pero sin pulso.
- Auditoría de prohibiciones explícitas en un documento existente.

## Cuándo NO aplicar

- Citas textuales de otros autores. Se mantienen tal cual.
- Prosa de otros autores (Willison, Karpathy, Yan, Peirano…) traída al manual: corrige solo errores objetivos (anglicismos forzados, longitud excesiva), respeta la voz original.
- Material legal, formal o de contrato. Otra voz, otro registro.
- Código y comentarios de código. Esta skill es prosa.

---

## Principio rector

Una autora con experiencia escribiendo para un lector adulto profesional. Lo asume como par inteligente, no como aprendiz pasivo. Tono cálido y directo, prosa deliberada con ritmo. Frase corta, media y larga conviven sin acrobacia: la larga construye argumento, la corta cierra y golpea, ninguna luce.

La autora ha visto algo que el lector no ha visto, y le orienta la mirada (Pinker: joint attention; Klinkenborg: noticing). La prosa es esa orientación: con qué empieza, qué se enseña a notar, qué se deja fuera. Editar no es solo quitar antipatrones — es decidir lo que se mira.

La prosa pasa el test de lectura en voz alta no porque busque sonar hablada, sino porque el oído detecta lo que el ojo perdona: frases sin aire, conectores forzados, ritmo plano. Es texto escrito, compuesto, no transcripción.

> Flujo no es frase larga. Flujo es frases cortas-medias que conectan con beats lógicos, con alguna larga deliberada cuando construye argumento. ([principio absorbido de `spanish-prose-craft`])

<!-- Origen: harness-engineering-guide/STYLE.md §Voz, calibration-digest.md §A, Pinker (Sense of Style), Klinkenborg (Several Short Sentences), spanish-prose-craft -->

---

## Las 10 reglas de prosa con pulso

Las reglas vienen de estudiar a divulgadores técnicos del sector que más calidez logran sin pose: Willison, Evans, Karpathy, Yan, Boykis, Abramov, Husain. Lo que comparten es lo que esta skill imita.

1. **Aperturas concretas, no tesis abstracta.** Cada sección y cada capítulo arranca con una escena, un objeto, un dato, una pregunta concreta o un pacto de continuidad. La apertura es contrato: lo que prometes en la primera frase es lo que el lector cobra.
2. **Voz autorial nosotros-dominante** (calibrada). Plural inclusivo por defecto vía conjugación verbal ("imaginemos", "tenemos", "vemos"). Tú implícito puntual para instrucción aislada. Yo solo cuando aporta cicatriz que el "nosotros" no podría sostener — puede ser cero en un capítulo entero.
3. **Definir en una frase y seguir.** El término técnico llega con definición seca y se sigue. Sin párrafo de calentamiento previo, sin sinónimos repetidos detrás. Aplica cuando el lector ya conoce el término aproximadamente.
4. **Validar la intuición ingenua antes de afilarla.** Si el lector llega con una idea aproximada, primero la nombras (incluso usando palabras como "imaginemos" o "magia" si es la palabra que el lector usaría), luego muestras dónde se queda corta, y solo entonces traes el término técnico exacto. La corrección llega después de la confusión, no antes. La regla 4 invierte la regla 3 cuando hay intuición previa que disolver.
5. **El paréntesis honesto.** Aside autorial que reconoce dificultad, costo o aporta ejemplo concreto, sin romper la línea principal del argumento. Tres modalidades: didáctica (Karpathy: "esto es lo que más confunde al principio"), irónica ("Algo completamente cierto"), editorial ("habría que añadir aquí investigaciones — pendiente"). Las tres son legítimas.
6. **Conectores casuales, no cultos.** "Pero", "Así que", "Lo raro es que", "Hasta aquí", "Aquí está la cosa". Nada de "asimismo", "en consecuencia", "cabe destacar", "por ende".
7. **Autoridad por especificidad.** Un caso real con nombre, fecha, comando o número convence más que diez frases generales. Comandos pegados con su salida. Nombres y enlaces, no "expertos dicen".
8. **Variación de longitud sin frase larga adornada.** Mezcla de corta, media y larga. La larga construye argumento que no cabe en frases más cortas; aparece como mucho una vez por sección y se justifica leyéndola en voz alta. Si tiene más de tres incisos, se rompe.
9. **Cierres bajos.** Sección y capítulo cierran con observación seca, instrucción accionable, pregunta abierta concreta, bisagra al siguiente, cierre lapidario, cierre proyectivo (tutorial) o cierre de cuándo NO hacer (how-to). Nada de moralejas, nada de "el viaje no termina aquí".
10. **Una metáfora sensorial / física por concepto fuerte.** Doméstica o mecánica, nunca cósmica. Puede volver una vez para complicarse, no es obligación. Si vuelve, que aporte; si no vuelve, también vale.

Detalle por regla con ejemplos before/after: `references/prosa-con-pulso.md`.

<!-- Origen: harness-engineering-guide/STYLE.md §"Prosa con pulso" + calibration-digest.md (regla 2, 4, 5, 8, 9, 10 calibradas) + referentes.md -->

---

## Voz autorial: nosotros + tú + (yo)

La calibración con los 4 samples editados por Marcela demuestra una proporción real distinta de la declarada en versiones anteriores:

- **Nosotros inclusivo: por defecto.** Es el plano sobre el que escribes, no la invitación puntual. Vía conjugación verbal: "imaginemos", "tenemos", "vamos a", "vemos", "podemos", "estemos", "volvemos", "aplicamos". Aparece incluso en reference ("podemos ver la comparación", "consultemos"). Es ~95 % de los verbos en los samples.
- **Tú implícito: puntual.** Vía conjugación verbal en operaciones aisladas: "lanza una llamada", "Marca claramente la frontera", "Si pierde el hilo, has recortado de más". Nunca como vocativo explícito ("tú, lector", "amigo desarrollador") y nunca como registro dominante.
- **Yo: casi nunca.** En los 4 samples no aparece. Probablemente porque el "nosotros inclusivo" absorbe el espacio del "yo". Reservado para géneros más ensayísticos (prefacio, post personal, columna), o para confesión costosa que el "nosotros" no podría sostener. Puede ser cero en un capítulo entero.

Lo prohibido: vocativo explícito, plural mayestático, impersonal sostenido, pseudo-coloquial gratuito, chistes de oficina. El humor seco enrollado en la propia frase técnica, una vez por capítulo, sí.

<!-- Origen: calibration-digest.md §A (proporción real) + harness STYLE.md §Voz -->

---

## Aperturas — cinco tipos

Cualquiera de estos cinco vale. Los cuatro primeros son los de la skill original; el quinto entra por calibración.

1. **Una escena.** "Cline acaba de proponer un cambio que toca seis archivos. Antes de aceptar, miramos…"
2. **Un objeto.** "Este AGENTS.md tiene 312 líneas. Es el problema."
3. **Un dato.** "Apiiro analizó 50 empresas Fortune. El código generado por IA tenía 322 % más vulnerabilidades de privilege escalation que el escrito por humanos."
4. **Una pregunta concreta.** "¿Por qué tu refactor con tests verdes pasó a producción y rompió el flujo de pago?"
5. **Un pacto de continuidad.** "Ya hemos acabado con la parte teórica. Ahora montamos el harness." Sitúa el bloque en una secuencia mayor. Solo funciona si el bloque anterior existe en la obra.

Dos tipos extra para casos específicos (ver `references/arquitectura-capitulo.md`):

6. Apertura como anuncio del hecho fechado (modelo Willison).
7. Apertura como respuesta directa (modelo Hamel: título-pregunta → primera línea-respuesta).

### Aperturas prohibidas

- "En este capítulo veremos…"
- "La inteligencia artificial está transformando…"
- "Como developers, sabemos que…"
- "Imagina que tu equipo…" como tesis abstracta sin caso real (distinto de "imaginemos que…" cuando sirve para validar intuición).
- "En el corazón de X…"
- "Let's dive in" / "Vamos a explorar" / "Profundicemos" como signposting vacío.

---

## Cierres — seis tipos

1. **Instrucción accionable.** "Antes del siguiente capítulo, audita tu AGENTS.md con el rubric del anexo."
2. **Pregunta abierta concreta.** "¿Cuál de los seis antipatrones ya viste en una PR de tu equipo este mes?"
3. **Bisagra al siguiente.** "El cap. 20 te da el AGENTS.md operativo. Aquí cerramos viendo por qué tu repo lo necesita."
4. **Cierre lapidario.** Una frase corta que recoge todo el capítulo en un movimiento de lengua. "Y las dos cosas escalan mal." "La segunda pregunta es la que define el oficio."
5. **Cierre proyectivo en condicional** (tutorial). "Con esto tendríamos un agente mínimo. El siguiente paso natural sería añadir un loop."
6. **Cierre de cuándo NO hacer** (how-to). Marca el caso límite en lugar de recapitular. "Si el agente está en mitad de una transacción crítica, espera y recorta entre transacciones."

### Cierres prohibidos

- "Espero que hayas disfrutado", "¡a por el siguiente!", emoji de confeti.
- "El viaje no termina aquí", "el futuro es ahora", "estás listo para conquistar X".
- "Ahora tienes las herramientas para…".
- "En definitiva" + frase lapidaria (duplica función — quitar el "en definitiva").

<!-- Origen: ambas STYLE.md §3 + calibration-digest.md §B y §C + arquitectura-capitulo.md -->

---

## Arquitectura del capítulo

La skill cubre frase y sección. Arquitectura mayor (lead, cuerpo, salida, transición entre capítulos, ritmo de obra) detallada en `references/arquitectura-capitulo.md`. Resumen operativo:

- **El lead se escribe primero**, antes que el cuerpo (McPhee). La decisión que ilumina el resto.
- **Una subsección, un gap** (Evans). Si una subsección cubre dos gaps, parte.
- **Conceder antes de aseverar** (Pinker, Abramov) cuando sostienes tesis fuerte. "Está claro que cada caso es distinto, pero…"
- **Decisión de exclusión** (McPhee). Antes de sumar al capítulo, pregunta qué de lo que ya está debería no estar.
- **El cierre se decide antes que el cuerpo**, no después.
- **Continuidad por dominio único** entre capítulos (CartApp del cap. 4 sigue en el cap. 5).
- **Densidad declarada en frontmatter** para capítulos catálogo.

<!-- Origen: arquitectura-capitulo.md (McPhee, Yan, Boykis, Evans, Klinkenborg) -->

---

## Técnicas propias de la voz Marcela

Patrones documentados en los 4 samples editados (calibración 2026-05-05). El agente debe imitarlos al editar prosa de Marcela.

### Antropomorfización del agente

En explanation y tutorial, el modelo / agente es entidad con voluntad y memoria. Verbos de percepción y memoria sobre el sistema:

> *"el modelo se ha vuelto loco, no entiende lo que le decimos, se ha olvidado de cosas que le dijimos hace un rato"*
> *"el agente las olvida"*
> *"para él, los últimos tokens son los que tiene presentes"*

No aplica en reference (registro catálogo). Sin metáfora cósmica, sin personajes inventados con nombre.

### Validación de intuición ingenua usando palabras "prohibidas"

"Imaginemos que…", "magia", "potente" valen cuando son atribución a la posición ingenua del lector, marcadas como tales, y desmontadas en las frases siguientes.

> *"Imaginemos que nuestro equipo empieza a trabajar con agentes. Cuando todo va bien parece que es magia o existe algun desarrollador diminuto que susurra al modelo. Pero cuando falla…"*

Lo que prohíbe sigue prohibido: "imagina que tienes un sistema X" sin caso concreto; "potente y robusto" como tesis propia.

### Conceder antes de aseverar

Técnica retórica clásica. Cuando sostienes tesis fuerte, concede el matiz contrario brevemente.

> *"Está claro que cada caso es distinto pero existen tres principios operativos."*
> *"podemos ampliar la ventana de contexto aunque esta no siempre posible y siempre es más caro, resetear la conversación, pero en este caso perderíamos el estado; o bien, recortar."*

### "Vamos a" como firma de transición

"Vamos a" + infinitivo como bisagra entre bloques o introducción de un paso nuevo. Aparece en los 4 samples; tolerado varias veces por capítulo siempre que cada uso introduzca un movimiento real.

### Paréntesis honesto en tres modalidades

- **Didáctico** (Karpathy): "(esto es lo que más confunde al principio)".
- **Irónico** (firma propia): "(Algo completamente cierto)" después de una frase con tono cómplice.
- **Editorial** (en draft): "(habría que añadir aquí investigaciones — pendiente)". En versión final pasa a SOURCES.md o se completa.

### Vocabulario emocional sobre actos técnicos

Cuando una operación técnica tiene correlato emocional honesto, nómbralo.

> *"brillará nuestro ingenio como desarrolladores"*
> *"sin quedar como un desconsiderado"*
> *"la parte más aburrida"*

No es marketing; es validación de la experiencia del lector que también siente cuando programa.

### Léxico lúdico-coloquial

Permitido: "superpoder", "arsenal", "parte aburrida", "nuestro ingenio". Baja el registro y crea cercanía. Es voz, no inflado promocional.

Prohibido (sigue): "potente", "mágico" (como tesis propia), "robusto", "elegante", "holístico", "integral", "revolucionario".

### Pregunta retórica como bisagra entre bloques

Distinto de la pregunta concreta como apertura: aquí la pregunta abre el siguiente bloque dentro de un argumento ya en curso.

> *"¿Y cómo podemos saber el orden correcto…? Está claro que cada caso es distinto pero…"*

<!-- Origen: calibration-digest.md §E, F, G, H, I, J, K, M -->

---

## Registros por modalidad Diátaxis

Identifica primero la modalidad del bloque, luego aplica el registro. Detalle con ejemplos en `references/registros-por-modalidad.md`.

### Tutorial → registro escena

Narración paso a paso, **plural inclusivo dominante** ("vamos a montar", "abrimos", "vemos"), presente del indicativo. Cada paso muestra el resultado completo antes de pedir transferencia (worked example effect). Apertura típica: dos beats antes del qué (beat emocional + beat cognitivo). Cierre típico: proyectivo en condicional.

> *"Ya hemos acabado con la parte teórica. Vamos a desbloquear un superpoder que antes no teníamos en el arsenal: cómo construir un agente con tool use."*

### How-to → registro instrucción (plural inclusivo modal)

**No imperativo seco.** Plural inclusivo modal: "podemos", "tenemos que", "vamos a", "volvemos", "aplicamos". Imperativo puntual cuando la operación es una sola línea ("lanza", "Marca", "Verifica"). Sin preámbulo. Asume lector competente.

> *"Para estabilizar un pipeline con resultados inconsistentes, primero medimos el tamaño del contexto. Si supera el 70 % del límite, recortamos. Lanza el evaluador con `--rubric`."*

### Reference → registro catálogo

Prosa mínima. Tablas, listas comparativas, definiciones. El "nosotros" puede aparecer en la introducción de la sección ("podemos ver la comparación") pero la tabla en sí es contenido de catálogo. Cero metáforas, cero antropomorfización, cero paréntesis honesto.

### Explanation → registro argumento

Prosa con tensión: tesis, contraste, evidencia, conclusión. Acepta paréntesis honesto en sus tres modalidades, antropomorfización del agente, metáforas sensoriales, concesión antes de aseverar. Cierre típico: lapidario.

<!-- Origen: guide-ai-developers/STYLE.md §2 + technical-guide-design (Diátaxis) + calibration-digest.md §L (how-to corregido) -->

---

## Léxico — tres categorías

| Categoría | Ejemplo | Estado |
|---|---|---|
| Promocional vacío | "potente", "mágico", "robusto", "holístico", "integral", "elegante", "revolucionario", "transformador", "disruptivo" | Prohibido cuando es tesis propia |
| Lúdico-coloquial | "superpoder", "arsenal", "parte aburrida", "nuestro ingenio", "manos a la obra" | Permitido como voz |
| Promocional usado en boca del lector ingenuo | "magia", "increíble", "imaginemos" | Permitido cuando se desmonta en las frases siguientes |

La diferencia es función: el promocional vende, el lúdico baja registro, el "en boca del lector" valida intuición ingenua. Cuando dudes, pregunta: ¿estoy vendiendo, bajando el registro o validando una intuición ajena?

<!-- Origen: calibration-digest.md §F, I -->

---

## Prohibiciones (cero tolerancia)

Cualquier aparición se reescribe, sin excepción. Ojo: las palabras de la categoría "lúdico-coloquial" y "boca del lector ingenuo" están permitidas (ver sección anterior).

### Léxico promocional como tesis propia

`mágico` (como afirmación), `milagroso`, `increíble` (como afirmación), `potente`, `revolucionario`, `revoluciona`, `transformador`, `disruptivo`, `de vanguardia`, `state-of-the-art` (sin fecha), `última generación`, `holístico`, `integral` (sin contexto), `robusto` (sin métrica), `escalable` (sin contexto), `elegante` (en vez de simple), `sinergia`, `empoderar`, `unlock`, `leverage`, `aprovechar` (en sentido vago), `potenciar`.

### Verbos vacíos / cópula evasiva

`representar`, `constituir`, `erigirse como`, `emerger como`, `destacar por`, `juega un papel`, `sirve como`, `funciona como`. Reemplazar por `ser` + concreción.

### Frases relleno sólidas (cero tolerancia)

"Es importante destacar que", "cabe mencionar", "vale la pena", "en efecto", "por cierto", "como bien sabemos", "a continuación vamos a", "let's dive in", "vamos a explorar", "profundicemos".

### Construcciones perfume IA

- **Em dash (—)** salvo cuando ninguna otra puntuación funciona. Por defecto: coma, paréntesis, dos puntos o punto seguido. Máximo una raya por párrafo. Cuando es la mejor opción, sin culpa.
- **Regla de tres** decorativa ("rápido, claro y eficaz"). Reescribe con dos elementos o cuatro.
- **"No solo X sino también Y"** y parientes ("además de X, también Y"). Reescribe.
- **Paralelismos negativos en cadena** ("no es X, es Y; no es A, es B"): perfume IA. Como mucho, una vez por capítulo.
- **Gerundio de posterioridad al cierre de frase**: "Jest se integra con Vite, optimizando el rendimiento" → "Jest se integra con Vite: el rendimiento mejora".
- **"Permite al desarrollador…"** (calco de *allows the developer to*). Usa `poder` + infinitivo o verbo directo.
- **"En el corazón de…"**, **"juega un papel"**, **"se erige como"**, **"marca un antes y un después"**.

### Apertura y cierre

- Apertura con tesis genérica abstracta. Siempre escena, objeto, dato, pregunta o pacto de continuidad.
- Cierre motivacional o moraleja. Siempre instrucción, pregunta, bisagra, lapidario, proyectivo o de cuándo NO hacer.
- "En definitiva" antes de cierre lapidario (duplica función).

### Tipográficas

- Capitalización tipo inglés en titulares. Solo capitaliza la primera palabra y nombres propios.
- MAYÚSCULAS para énfasis: nunca. Cursiva sí, negrita con criterio.
- Negrita mecánica en cada término técnico. Negrita solo en primer uso o cuando la palabra es foco genuino. Código en backticks, no en negrita.
- Emojis decorativos: cero.
- Comillas curvas ("…"): usar rectas o latinas según convención del documento.

### Vocabulario LLM-frecuente (alerta de revisión)

`testament`, `pivotal`, `landscape` (abstracto), `tapestry`, `intricate`, `intricacies`, `delve`, `underscore` (verbo), `highlight` (verbo), `enhance`, `garner`, `foster`, `interplay`, `vibrant`, `enduring`, `align with`, `crucial` (sin matiz), `key` (adjetivo, abuso), `seamless`. Si aparece, justificar o sustituir.

### Citas y datos

- "Expertos dicen", "industria reporta", "estudios indican" sin nombre y fecha. Cero. Toda cita: nombre + fecha + enlace.
- Datos numéricos sin fuente. Cero. Toda cifra cita SOURCES.md o el origen explícito.
- "Como vimos antes" sin link. Si refieres, enlaza concreto.

Reglas relajadas por calibración:

- **"Dicho/a"** anafórico: permitido en uso natural ("dicha transacción"). Solo se reescribe si la frase suena claramente burocrática ("la mencionada implementación").
- **"Hoy en día / cada vez más / lo más probable es que"**: tolerado como modulación puntual de ritmo. Si aparece dos veces en la misma sección, se reduce.

Detalle exhaustivo con before/after en `references/prohibiciones.md`.

<!-- Origen: humanizer §1-29 + spanish-prose-craft §antipatrones + ambas STYLE.md + calibration-digest.md §N (relajaciones) -->

---

## Patrones a vigilar en la propia prosa

Tres patrones que se cuelan en la prosa de Marcela cuando está escribiendo desde la carga emocional. El canon (Klinkenborg, Pinker, Strunk) los marcaría como mejorables. El agente debe flagearlos al editar.

### 1. Frase amontonada con comas

**Síntoma**: tesis + descripción técnica + analogía + consecuencia, todo en una frase pegada con comas.

> *"Según varias investigaciones, los modelos actuales muestran un patrón conocido como atención no uniforme a lo largo del prompt, se despistan de lo importante cuando existe mucho ruido, como si nosotros tuvieramos muchas ideas en la cabeza y viene alguien a preguntarnos algo, seguramente, si no priorizaramos la información de nuestra cabeza, podríamos fallar en la respuesta."*

**Diagnóstico**: cuatro ideas en una frase. La analogía no respira.

**Reescritura**:
> *"Los modelos actuales muestran un patrón conocido como atención no uniforme a lo largo del prompt: se despistan de lo importante cuando hay ruido. Imagínalo como tener muchas ideas en la cabeza cuando alguien te interrumpe — si no priorizas, fallas la respuesta."*

**Regla**: cuando una frase mete tesis + descripción + analogía + consecuencia con comas, parte en 2-3 frases. Especialmente cuando el `que` subordinado pasa de dos.

### 2. Hedging blando heredado del registro tech-blog-español

**Síntoma**: relleno tipo "hoy en día, cada vez más", "lo más probable es que", "es interesante tenerlo en cuenta". Aparece cuando bajas el piloto automático.

> *"lo más probable es que nuestros prompts mejoren mucho de calidad, y es interesante tenerlo encuenta"*

**Diagnóstico**: si llevas dos páginas sosteniendo argumento, la siguiente frase afirma; no hedge. "Es interesante tenerlo en cuenta" es la firma del relleno blando.

**Regla**: el agente quita "es interesante tenerlo en cuenta" siempre. "Lo más probable es que" se reduce a la afirmación directa cuando el contexto la sostiene. "Hoy en día / cada vez más" se tolera una vez; dos en la misma sección, se quita una.

### 3. Pleonasmos y palabras-eco

**Síntoma**: dos palabras dicen lo mismo, una sobra.

> *"si o si […] siempre"*
> *"aquella barrera de piedra impenetrable"* (si es de piedra, ya es impenetrable)
> *"lo que cambia, en definitiva, es la pregunta"* (cuando la frase siguiente ya es lapidaria)

**Regla**: dos palabras dicen lo mismo, una se va. "En definitiva" antes de cierre lapidario duplica función — quitar.

<!-- Origen: análisis crítico contrastado con Klinkenborg, Pinker, Strunk sobre los 4 *-despues.md (sesión 2026-05-05) -->

---

## Núcleo de prosa española

Reglas mínimas para que la prosa suene a español natural, no a traducción del inglés ni a máquina.

### Longitud y ritmo

- Media de palabras por oración entre 15 y 25.
- **Ninguna oración pasa de 40 palabras salvo cuando construye argumento que no cabe en frases más cortas; esa excepción aparece como mucho una vez por sección y se justifica leyéndola en voz alta.**
- Párrafos de 3-7 oraciones por defecto. Una idea ramificada puede sostener un párrafo más largo si los conectores casuales mantienen el hilo.
- Si lees en voz alta y pierdes el aire, la frase es larga.

### Verbo y sujeto

- Verbos plenos sobre cópulas. "Realizar el análisis" → "analizar". "Proceder a la ejecución" → "ejecutar".
- Sujeto concreto siempre que se pueda. "Tú configuras", "Vitest ejecuta". Evita el sujeto difuminado en `se`.
- Pasiva refleja con moderación. Cuando se puede, plural inclusivo: "se está portando código" → "estamos portando código".
- Pasiva con `ser` casi nunca. "El componente es renderizado por `render`" → "`render` renderiza el componente".

### Gerundio

- Solo cuando es simultáneo, causal o modal. Nunca de posterioridad.
- Cero gerundios al final de frase: *destacando*, *garantizando*, *reflejando*, *permitiendo* son huella LLM.
- Cero gerundios adjetivos ("un componente recibiendo props" → "un componente que recibe props").

### Subordinación y conexión

- Conectores explícitos casuales mejor que subordinación anidada. Un punto + "Por tanto", "En cambio", "Así que" rinde más que una subordinada de tercer nivel.
- **Más de dos `que` subordinantes en una frase: rompe.** Patrón a vigilar (ver sección anterior).
- No abras tres párrafos seguidos con el mismo conector.

### Léxico

- Sin adjetivos-tapón: *importante, clave, fundamental* sin cuantificar.
- Sin variación elegante (sinónimo cycling). Repetir "test" es correcto.
- **Repetición estratégica permitida**: misma palabra clave en posición fija (verbo, sujeto) ancla el argumento. Modelo: "Components are code, and that code has to run somewhere" (Abramov). Distinto de variación elegante; es contraparte positiva.

<!-- Origen: spanish-prose-craft §10 principios + calibration-digest.md §N + Abramov (referentes.md) -->

---

## Bilingüismo y glosario operativo

Cuerpo en español neutro. Términos en inglés cuando son nombres propios o jerga consolidada.

### Anglicismos que se mantienen (jerga del stack)

`prompt`, `context window`, `tool use`, `function calling`, `agent`, `agent loop`, `harness`, `MCP`, `system prompt`, `few-shot`, `zero-shot`, `chain-of-thought`, `RAG`, `golden dataset`, `eval`, `HITL`, `drift`, `prompt injection`, `jailbreak`, `prompt caching`, `vibe coding`, `spec-driven`, `EARS`, `feedforward`, `sprint contract`, `context reset`, `compaction`, `hallucination`, `refactoring avoidance`, `context blindness`, `shotgun surgery`, `reward hacking`, `generator-evaluator`, `agnostic` (cuando refiere a infraestructura agnóstica de proveedor).

También: `test`, `mock`, `snapshot`, `framework`, `plugin`, `API`, `endpoint`, `hook`, `prop`, `state`, `stub`, `spy`, `async`, `promise`, `commit`, `push`, `pull request`, `linter`, `bundler`, `tool_use`, `tool_result`, `stream`.

### Anglicismos con matiz

- `feature` → en escrito mejor "funcionalidad"; en habla técnica pasa.
- `deploy` → en escrito mejor "despliegue".
- `performance` → mantener solo si refiere a Web Performance APIs; si es rendimiento general, traducir.

### Traducir

`rollout` → lanzamiento, `deadline` → fecha límite, `feedback` → comentario / respuesta, `target` → objetivo, `issue` → incidencia / ticket. `bug` aceptado.

### Verbos castellanizados

Tolerados: `mockear`, `testear`, `dockerizar`. Rechazados: `commitear` (mejor "hacer commit"), `deployar` (mejor "desplegar").

### Términos prohibidos como traducción

- `arnés` para `harness`. Siempre `harness`.
- `ventana de contexto` como sustituto canónico de `context window`. Puede aparecer una vez como aclaración; el término canónico es `context window`.

### Cómo se introducen anglicismos

- **Primera aparición** en un capítulo: en cursiva con definición seca de una frase.
- **Siguientes apariciones**: en redonda, sin cursiva, sin definir.

Excepción: si el lector objetivo da el término por sentado (`prompt`, `context window`, `agnostic`), se puede omitir la definición y la cursiva. Decisión consciente, no descuido.

<!-- Origen: spanish-prose-craft §taxonomía anglicismos + ambas STYLE.md + calibration-digest.md (`agnostic`) -->

---

## Convenciones tipográficas

- **Cursiva** (`*texto*`): primera aparición de un término canónico, anglicismos sueltos en su primera aparición, títulos de obra, énfasis prosódico con mesura.
- **Negrita** (`**texto**`): término canónico en su primera aparición en el capítulo. Una negrita por párrafo como criterio, dos en taxonomías densas.
- **Backticks** (`` `texto` ``): nombres de archivos, comandos, variables, identificadores de código.
- **Bloques de código**: lenguaje declarado siempre. Ruta de archivo cuando aplique.
- **Citas en bloque** (`>`): definiciones canónicas, advertencias, cita textual de fuente.
- **Comillas**: latinas («…») para citas largas, rectas ("…") para inline cortas.
- **Tablas**: para reference. No abusar en explanation o tutorial.
- **Listas**: solo cuando los ítems son paralelos (todos verbo, todos sustantivo). Si la sección tiene 3 bullets de una palabra, vuelve a prosa.
- **Diagramas**: Mermaid embebido. Texto alternativo en prosa describiendo el flujo, antes del bloque.
- **TLDR** (Karpathy): bloque opcional al cierre de capítulos largos, marcado en negrita o como cita en bloque.

---

## Carga cognitiva

- **Una unidad nueva por sub-sección.** Introduce un solo concepto canónico nuevo.
- **Una subsección, un gap** (Evans): si una subsección cubre dos gaps, parte.
- **Excepción**: capítulos cuya función explícita es definir un marco de vocabulario completo. Declárenlo en frontmatter o cabecera.
- **Reuso explícito**: si reusas un concepto del cap. anterior, dilo y enlaza.
- **Worked example effect** en tutoriales: cada paso muestra resultado completo antes de pedir transferencia.
- **Backward fading**: paso 1 completo → paso 2 parcial → paso 3 en blanco.
- **Expertise reversal effect**: la audiencia "developers experienced" puede irritarse con worked examples completos cuando ya saben el primer paso. Ofrecer "si ya sabes X, salta a Y" cuando aplica.
- **Curse of knowledge** (Pinker): pregunta diagnóstica antes de cerrar — "¿qué doy por sabido aquí que un lector no asume?".

<!-- Origen: technical-guide-design §cognitive load + Evans + Pinker (curse of knowledge) -->

---

## Checklist de edición

Aplica en este orden. Cada punto es pregunta diagnóstica; si la respuesta es no, corrige.

### A. Voz y registro

1. ¿La voz dominante es plural inclusivo ("vamos a", "tenemos", "podemos")?
2. ¿Hay vocativo explícito ("tú, lector")? Quítalo.
3. ¿La modalidad del bloque (tutorial / how-to / reference / explanation) tiene su registro?
4. ¿El how-to está en plural inclusivo modal y no en imperativo seco como registro dominante?
5. ¿Hay pose académica, plural mayestático o impersonal sostenido?

### B. Apertura y cierre

6. ¿La apertura es escena, objeto, dato, pregunta concreta o pacto de continuidad?
7. ¿Hay tesis genérica abstracta, "imagina que… [sin caso real]" o "en este capítulo veremos"?
8. ¿El cierre es instrucción, pregunta abierta, bisagra, lapidario, proyectivo o de cuándo NO hacer?
9. ¿Hay moraleja o "el viaje no termina"? ¿Hay "en definitiva" antes de cierre lapidario?

### C. Postura del autor

10. ¿Hay decisión autorial visible — qué se mira, qué se nombra primero, qué se deja fuera?
11. ¿Qué doy por sabido aquí que un lector no asume? (curse of knowledge)
12. ¿Tengo claro qué he visto que el lector no ha visto?

### D. Técnicas propias

13. En explanation/tutorial, ¿antropomorfizo al agente cuando aporta?
14. Si hay intuición ingenua del lector, ¿la valido antes de afilarla?
15. Antes de aseverar tesis fuerte, ¿concedo el matiz contrario brevemente?
16. ¿El paréntesis honesto aparece donde aporta — didáctico, irónico o editorial?

### E. Prohibiciones (cero tolerancia)

17. ¿Léxico promocional como tesis propia ("potente", "robusto", "mágico" afirmado)?
18. ¿Verbos vacíos ("representar", "erigirse")?
19. ¿Frases relleno sólidas ("es importante destacar", "vale la pena")?
20. ¿Em dash usado por defecto? Reduce a coma, paréntesis, dos puntos.
21. ¿Regla de tres decorativa? Pasa a dos o cuatro.
22. ¿Paralelismos negativos en cadena? Máximo uno por capítulo.
23. ¿Gerundios al final de frase? Cero.
24. ¿Calcos: "permite al desarrollador", "en el corazón de"?

### F. Patrones a vigilar (los tuyos)

25. ¿Hay frase amontonada con comas (cuatro ideas pegadas)? Parte en 2-3.
26. ¿Hay hedging blando ("hoy en día / lo más probable / es interesante tenerlo en cuenta")? Quita.
27. ¿Hay pleonasmos ("si o si... siempre", "barrera de piedra impenetrable")?
28. ¿Más de dos `que` subordinantes en alguna frase?

### G. Prosa española

29. ¿Media de palabras por frase 15-25, ninguna mayor de 40 (salvo excepción justificada)?
30. ¿Verbos plenos sobre cópulas y nominalizaciones?
31. ¿Sujeto concreto siempre que se puede?
32. ¿Pasivas con `ser` solo cuando el agente es irrelevante?

### H. Patrones LLM

33. ¿Vocabulario LLM-frecuente (testament, pivotal, landscape, intricate, vibrant)?
34. ¿Copula avoidance ("serves as", "stands as")? Vuelve a `ser`.
35. ¿Sycophantic / signposting ("let's dive in", "great question")?
36. ¿Curly quotes? Pasa a rectas o latinas.
37. ¿Inline-header vertical lists con bullets bold + colon? Reescribe.

### I. Tipografía y citas

38. ¿Cursiva solo en primera aparición de término / anglicismo / título?
39. ¿Negrita máximo una por párrafo (dos en taxonomías)?
40. ¿Capitalización tipo inglés en titulares? Pasa a sentence case.
41. ¿Toda cifra cita fuente? ¿Toda referencia a "experto" o "estudio" tiene nombre y enlace?

### J. Lectura en voz alta (test final)

42. ¿Pierdes el aire en alguna frase?
43. ¿Tropiezas con alguna palabra o transición?
44. ¿Hay decisión autorial en cada movimiento, o hay reglas aplicadas mecánicamente?

<!-- Origen: ambas STYLE.md + calibration-digest.md + arquitectura-capitulo.md (postura del autor) -->

---

## Playbook de reescritura

Cuando un párrafo suena a máquina o falta voz, aplica en este orden.

### Paso 0 — Decisión de exclusión

Antes de tocar el párrafo, pregunta: ¿qué de lo que aquí está debería no estar? La poda de capítulo (no de párrafo) es la decisión más alta.

### Paso 1 — Diagnóstico

Lee en voz alta. Pregúntate:

1. ¿Cuál es la idea del párrafo en una frase? Si no la identificas, no tiene unidad temática.
2. ¿Dónde pierdo el aire?
3. ¿Hay tres ideas distintas? Probablemente son tres párrafos.
4. ¿Hay gerundio al final de alguna frase?
5. ¿Hay alguna oración de más de 30 palabras? ¿De más de 40?
6. ¿La apertura es concreta? ¿El cierre es bajo?
7. ¿La voz es nosotros inclusivo, o se cuela impersonal?

### Paso 2 — Movimientos de corte

Para frases amontonadas:

1. Identifica la idea-núcleo.
2. Identifica ideas-satélite.
3. Convierte cada satélite en oración corta.
4. Añade conector explícito casual entre oraciones ("Pero", "Así que", "Lo raro es que").
5. Relee: si suena entrecortado, funde dos con punto y coma.

### Paso 3 — Movimientos de expansión

Para stubs telegráficos:

1. Añade un ejemplo concreto en línea.
2. Explicita el porqué con una segunda frase corta.
3. Añade la consecuencia ("y por eso…").
4. Considera un paréntesis honesto.
5. Nunca rellenes con adjetivos-tapón.

### Paso 4 — Sustituciones léxicas

Reemplaza en este orden:

1. Gerundios de posterioridad → oración nueva con conector.
2. Nominalizaciones → verbos plenos.
3. Verbos inflados (representar, erigirse, emerger) → `ser` + concreción.
4. Adjetivos-tapón → dato concreto o eliminar.
5. Calcos sintácticos → giro nativo.
6. Vocabulario LLM-frecuente → término llano.
7. Hedging blando ("es interesante tenerlo en cuenta", "hoy en día", "lo más probable") → quitar o sustituir por afirmación directa.
8. Pleonasmos → quitar uno de los dos.

### Paso 5 — Voz y registro

1. ¿La voz dominante es plural inclusivo? Si hay impersonal sostenido o "tú" como vocativo, ajusta.
2. ¿Hay decisión autorial visible? Si todo es genérico, decide qué se mira.
3. ¿Hay paréntesis honesto donde aporta?

### Paso 6 — Apertura y cierre

1. ¿La apertura es concreta? Si no, sustituye por escena, objeto, dato, pregunta o pacto.
2. ¿El cierre es bajo? Si es moraleja, sustituye por instrucción, pregunta, bisagra, lapidario, proyectivo o de cuándo NO hacer.

### Paso 7 — Verificación final

1. Lee el párrafo reescrito en voz alta.
2. Mira la transición con el párrafo anterior y el siguiente: ¿hay hilo?
3. Cuenta las oraciones de más de 30 palabras: idealmente cero, una si construye argumento.
4. Busca "importante", "clave", "fundamental", "es interesante": idealmente cero.
5. Busca "en definitiva" antes de cierre lapidario: quita.

---

## Cuándo lista, cuándo prosa

Convierte prosa en lista cuando:

- Enumeras 3+ elementos homogéneos.
- El lector va a escanear, no a leer lineal.
- Cada elemento se sostiene en una línea.
- Los elementos tienen paralelismo estructural.

Mantén prosa cuando:

- La relación entre elementos es argumental, no enumerativa.
- Hay matices que se pierden en bullets.
- Es explicación narrativa.
- La sección tiene 3 bullets de una palabra: vuelve a prosa.

---

## Calibración y evidencia de voz

La skill se sostiene en tres tipos de evidencia, no solo en reglas declarativas:

1. **`references/calibration-digest.md`** — moves nombrables extraídos de los 4 samples antes/después editados por Marcela (2026-05-05). Cuando dudes entre dos formas, gana la coincide con un move documentado.
2. **`references/calibration-samples/`** — los pares antes/después literales para consulta. Cuando un sample real choca con una regla, gana el sample.
3. **`references/referentes.md`** — perfiles de Willison, Karpathy, Yan, Boykis, Abramov, Evans, Husain, Böckeler/Fowler con técnicas reproducibles. Cuando dudes en lo grande, mira cómo lo haría el referente cuyo registro coincide más con el bloque que escribes.

La calibración se actualiza cuando Marcela edita material nuevo. Si un capítulo real recibe edición sustantiva, sus moves alimentan futuras revisiones del digest.

<!-- Origen: PLAN.md Fase 2 + calibration-digest.md + referentes.md -->

---

## Interacción con otras skills

Esta skill es autónoma. No invoques `humanizer`, `spanish-prose-craft` ni `technical-guide-design` además de esta para el mismo material; duplicarías reglas y la voz se diluye.

Casos en los que sí conviene la otra skill por separado:

- **`humanizer` solo (en inglés)**: si el material es inglés.
- **`spanish-prose-craft` solo**: si el material es español pero NO de Marcela (colaborador externo cuya voz queremos respetar). `spanish-prose-craft` corrige errores objetivos sin imponer voz personal.
- **`technical-guide-design` solo**: cuando estás diseñando estructura sin escribir prosa todavía (índice, modalidades, secuencia, exercise design).

Si dudas: en duda, esta skill.

---

## Referencias

Material consultable bajo demanda:

- `references/prosa-con-pulso.md` — Las 10 reglas con before/after detallados.
- `references/registros-por-modalidad.md` — Diátaxis aplicado a la prosa.
- `references/prohibiciones.md` — Catálogo completo con diagnóstico y reescritura.
- `references/antipatrones-llm.md` — Subset de patrones LLM relevantes.
- `references/calibration-digest.md` — Moves extraídos de la pasada de Marcela.
- `references/calibration-samples/` — Pares antes/después literales.
- `references/referentes.md` — Perfiles de Willison, Karpathy, Yan, Boykis, Abramov, Evans, Husain, Böckeler/Fowler.
- `references/arquitectura-capitulo.md` — Lead, cuerpo, salida, transición, ritmo de obra.

Fuentes externas vivas:

- `~/Projects/guide-ai-developers/STYLE.md`
- `~/Projects/harness-engineering-guide/STYLE.md`
- `~/.claude/skills/humanizer/SKILL.md`
- `~/.claude/skills/spanish-prose-craft/SKILL.md`
- `~/.claude/skills/technical-guide-design/SKILL.md`
- `~/Projects/mars-voice/research/CRITIQUE.md` — investigación profunda y crítica que motivó la v2.

Si una fuente externa evoluciona, esta skill se revisa.

---

Si la skill se queda corta, el lector está pidiendo prosa con voz. Si se pasa, el lector pide manual. La diferencia se decide leyendo en voz alta.
