# Arquitectura del capítulo y de la obra larga

<!-- Origen: McPhee Draft No. 4, Yan Why-What-How, Boykis grounding histórico, Klinkenborg arquitectura del párrafo, Pinker postura del autor. Síntesis de propuestas 6, 15, 25 del CRITIQUE (research/) -->

La skill cubre frase y sección. Este documento cubre lo siguiente: el capítulo como unidad arquitectónica, la transición entre capítulos, el ritmo de la obra larga. Aplicable cuando estás escribiendo guías de muchos capítulos, libros o series.

---

## El capítulo tiene huesos

McPhee, *Draft No. 4*: "Readers are not supposed to notice the structure." La estructura del capítulo es esqueleto invisible. Tres huesos:

- **Lead** (apertura). La decisión que ilumina el resto.
- **Cuerpo** (organización deliberada). Sub-secciones que sostienen una unidad nueva cada una.
- **Salida** (cierre que abre el siguiente).

Cada hueso pide su propia atención. La skill v1 cubría apertura y cierre como puntos sueltos; aquí van como decisiones arquitectónicas.

---

## El lead

McPhee: "Always write your lead before you go at the big pile of raw material."

El lead no es solo el primer párrafo. Es la decisión que ilumina la arquitectura del resto. Cuando dudes entre dos aperturas posibles, escribe la que te obliga a estructurar el capítulo de la forma que quieres. Si el lead funciona, el resto se ordena casi solo.

**Reglas operativas**:

1. **Escribe el lead primero, antes que el cuerpo.** Si lo dejas para el final, lo escribes desde el cansancio.
2. **El lead promete y cobra.** Lo que prometes en la primera frase es lo que el lector cobra después; si la frase 5 ya cambió de tono, el lead estaba mal.
3. **Cinco tipos de lead validados** (los de la skill + uno):
   - Escena: "Cline acaba de proponer un cambio que toca seis archivos."
   - Objeto: "Este AGENTS.md tiene 312 líneas. Es el problema."
   - Dato: "Apiiro analizó 50 empresas Fortune. El código IA tenía 322 % más vulnerabilidades."
   - Pregunta concreta: "¿Por qué tu refactor con tests verdes pasó a producción?"
   - Pacto de continuidad: "Ya hemos acabado con la parte teórica. Ahora montamos el harness."
4. **Cuatro tipos prohibidos**: tesis genérica abstracta, "imagina que…" sin caso real, "en este capítulo veremos", "let's dive in".

Para guías técnicas, hay dos tipos adicionales que valen pero conviene usar con cuidado por su especificidad:

5. **Apertura como anuncio del hecho fechado** (Willison): "GPT-5 salió en abril. La forma de redactar agentes cambió esa semana." Útil cuando el contexto temporal es parte del argumento. Riesgo: envejece.
6. **Apertura como respuesta directa** (Hamel): título "¿Más context window resuelve la falta de atención?" → primera línea: "No." Útil para capítulos cuya tesis es contraintuitiva.

---

## El cuerpo

Klinkenborg: "All writing is revision."

El cuerpo es organización de detalle, no acumulación. Cada subsección sostiene una unidad nueva.

**Reglas operativas**:

1. **Una subsección, un gap** (Evans). "Address one major gap at a time and make clear what specific gap you're addressing." Si una subsección cubre dos gaps, parte.
2. **Worked example al inicio del cuerpo cuando es tutorial** (Renkl & Atkinson). Primero ejemplo resuelto entero; después ejemplo parcial; después en blanco. La progresión es backward fading.
3. **Frase declarativa-tesis intercalada** (Boykis). Una frase corta de tesis en mitad del cuerpo, no solo en el cierre. "Components are code, and that code has to run somewhere." Ancla el argumento sin esperar al final.
4. **Conceder antes de aseverar** (Pinker, Abramov). Cuando sostienes tesis fuerte, concede el matiz contrario brevemente antes. "Está claro que cada caso es distinto, pero…"
5. **Decisión de exclusión** (McPhee). Antes de sumar más al capítulo, pregunta: ¿qué de lo que ya está debería no estar? La poda de capítulo es la decisión más alta del oficio.

---

## La salida

La salida es bisagra: cierra este capítulo y abre el siguiente. En guías largas, la transición es continuidad, no resumen.

**Reglas operativas**:

1. **Cinco tipos de cierre validados** (los de la skill v1 + tres):
   - Instrucción accionable: "Antes del siguiente capítulo, audita tu AGENTS.md."
   - Pregunta abierta concreta: "¿Cuál de los seis antipatrones ya viste en una PR este mes?"
   - Bisagra al siguiente: "El cap. 20 te da el AGENTS.md operativo. Aquí cerramos viendo por qué tu repo lo necesita."
   - Cierre lapidario: "La segunda pregunta es la que define el oficio."
   - Cierre proyectivo en condicional (tutorial): "Con esto tendríamos un agente mínimo. El siguiente paso natural sería…"
   - Cierre de cuándo NO hacer (how-to): "Si el agente está en mitad de una transacción crítica, espera y recorta entre transacciones."
2. **Cierres prohibidos**: moraleja, "espero que hayas disfrutado", "el viaje no termina aquí", emoji de confeti, "ahora tienes las herramientas para…".
3. **El cierre se decide antes que el cuerpo, no después.** Como el lead.

---

## Transición entre capítulos

Para guías de muchos capítulos, la transición es la costura de la obra. Mal hecha, el lector siente saltos; bien hecha, no se nota.

**Reglas operativas**:

1. **Un capítulo cierra abriendo el siguiente, el siguiente abre cerrando el anterior.** No con resumen, con uso. "Antes vimos cómo definir tools. Ahora montamos el loop que las invoca en cadena." El lector no lee el resumen; lee el siguiente paso.
2. **Continuidad por dominio único.** Si el cap. 4 usa CartApp como ejemplo, el cap. 5 sigue con CartApp. Cambiar de dominio entre capítulos es coste cognitivo gratuito.
3. **Continuidad por voz.** El primer capítulo de un libro y el último no deben sonar idénticos — la voz puede madurar — pero la continuidad de tono se debe sostener. Si el cap. 1 es cálido y el cap. 30 es lacónico sin razón, hay deriva.
4. **Pre-anuncio cuando una idea madurará en otro capítulo.** "Veremos en el cap. 14, después de ver evals, cómo esto cambia." Pacto pequeño con el lector.

---

## Ritmo de la obra larga

Una guía de 30+ capítulos tiene ritmo macro. Capítulos densos seguidos de capítulos ligeros. Capítulos largos seguidos de capítulos cortos.

**Reglas operativas**:

1. **Densidad declarada en frontmatter.** Si un capítulo es densidad alta (catálogo, marco, anexo), el lector lo sabe antes de entrar. Misma cortesía que en formación presencial.
2. **No tres capítulos densos seguidos.** Si los tres siguientes son catálogo, mete un capítulo de aplicación entre medio.
3. **Capítulos puente.** A veces un capítulo no introduce concepto nuevo; sostiene el ritmo y prepara el siguiente. Son legítimos. Marcarlos como tales en el OUTLINE.

---

## Postura del autor

Pinker: "classic style" como conversación entre escritor y lector que dirigen su atención conjunta a algo en el mundo. Klinkenborg: "practice noticing". Esto es radicalmente distinto del frame "colega hablando" — el autor no improvisa; escribe porque ha visto algo y orienta la mirada del lector hacia ello.

**Reglas operativas**:

1. **Antes de escribir un capítulo, pregunta: ¿qué he visto que el lector no ha visto todavía?** Si no tienes respuesta, el capítulo no está listo para escribirse.
2. **Curse of knowledge**: el autor sabe demasiado y olvida lo que es no saber. Pregunta diagnóstica: "¿Qué doy por sabido aquí que un lector no asume?"
3. **La voz autorial aparece en arquitectura, no solo en confesión** (Fowler, Böckeler). Qué decides incluir, qué decides excluir, qué decides nombrar primero. Eso es voz.
4. **Acuñación de términos vívidos** (Karpathy). Cuando un concepto merece nombre propio, dáselo con palabra física o dicotomía clara. Si el lector lo recuerda al día siguiente sin volver al texto, has firmado el concepto.

---

## Paratexto y géneros propios

Lugares de la obra que tienen sus propias reglas:

- **Prefacio / introducción**: aquí sí aparece "yo" más libre. Es donde la autora se firma. La cuota de "yo" sube; el "nosotros" baja.
- **Glosario**: registro catálogo puro. Sin metáforas, sin paréntesis honesto, sin antropomorfización.
- **Anexos**: registro de soporte. Pueden ser referenciales o ejemplos extendidos. Se citan desde el cuerpo.
- **TLDR final** (Karpathy): cuando un capítulo es largo, un bloque de cierre marcado como "TLDR" puede recoger 3-5 puntos. No reemplaza el cierre lapidario; lo complementa.
- **Notas a pie**: para precisión sin romper el flujo. En español técnico, raras pero útiles.
- **Sobre la autora / agradecimientos**: registro propio. Aquí el "yo" es protagonista.

---

## Síntesis operativa

Cuando empieces un capítulo nuevo:

1. ¿Qué he visto que el lector no ha visto? (postura)
2. ¿Cuál es el lead? (escribe primero)
3. ¿Cuál es la salida? (decide segundo)
4. ¿Qué tres a cinco unidades nuevas (gaps) cubre el cuerpo? (terceiro)
5. ¿Qué se queda fuera y por qué? (poda antes de escribir)
6. ¿Cómo conecta con el capítulo anterior y con el siguiente? (continuidad)

Solo entonces empieza la prosa.
