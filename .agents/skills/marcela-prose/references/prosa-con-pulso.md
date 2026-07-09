# Las 10 reglas de prosa con pulso — detalle

Cada regla con before/after, diagnóstico y casos límite.

<!-- Origen: harness-engineering-guide/STYLE.md §"Prosa con pulso" (2026-04), expandido con ejemplos de los STYLE.md y de spanish-prose-craft -->

---

## 1. Aperturas concretas, no tesis abstracta

Cada sección y cada capítulo arranca con una escena, una observación de primera mano, un objeto o un dato. La apertura es contrato: lo que prometes en la primera frase es lo que el lector cobra. Si abres con tesis abstracta sobre un campo ("la disciplina X consiste en…"), el lector adulto cierra antes de la segunda frase.

**Antes (tesis genérica):**
> La inteligencia artificial está transformando la forma en que los desarrolladores escriben código. En este capítulo veremos cómo aprovechar estas herramientas en nuestro flujo diario.

**Después (escena):**
> Cline acaba de proponer un cambio que toca seis archivos. Antes de aceptar, miramos el diff de uno por uno. Tres de las modificaciones son lo que pediste; las otras tres son refactors que nadie pidió. Bienvenido al primer problema del trabajo con agentes.

**Después (objeto):**
> Este AGENTS.md tiene 312 líneas. Es el problema.

**Después (dato):**
> Apiiro analizó 50 empresas Fortune. El código generado por IA tenía 322 % más vulnerabilidades de privilege escalation que el escrito por humanos.

**Después (pregunta concreta):**
> ¿Por qué tu refactor con tests verdes pasó a producción y rompió el flujo de pago?

**Diagnóstico**: si el primer párrafo describe el campo en abstracto, no la escena del lector, está mal. La apertura es contrato: lo que prometes en la primera frase es lo que el lector cobra.

---

## 2. Voz autorial: nosotros dominante + tú puntual + (yo)

La calibración con los 4 samples de Marcela demuestra una proporción real: ~95 % nosotros, ~5 % tú implícito puntual, ~0 % yo. La voz por defecto es plural inclusivo, no tú implícito como decían versiones anteriores de esta skill.

**Nosotros inclusivo (forma por defecto, ~95 %):**
> Imaginemos que nuestro equipo empieza a trabajar con agentes. Tenemos tres opciones cuando el context window se llena. Vamos a montar el harness mínimo: un loop, una herramienta, un evaluador.

Aparece incluso en reference: "podemos ver la comparación", "consultemos esta tabla". El nosotros es el plano sobre el que escribes.

**Tú implícito puntual (~5 %):**
> Si pierdes el hilo, has recortado de más. Lanza el evaluador con `--rubric`. Marca claramente la frontera entre resumen y historial vivo.

Reservado para operaciones aisladas, normalmente rodeadas de plural inclusivo. Nunca como vocativo ("tú, lector").

**Yo (casi nunca):**
> Mi sospecha es que el problema no era el modelo. Era yo metiendo el contexto en el orden equivocado. Lo descubrí gastando tres días.

Reservado para confesión costosa que el "nosotros" no podría sostener. Puede ser cero en un capítulo entero. Sube en prefacio, post personal o columna; baja a cero en reference y how-to.

**Antes (vocativo explícito + plural mayestático):**
> Tú, lector, debes recordar que en este libro nos proponemos enseñarte a usar agentes con seriedad.

**Después:**
> Si llegamos con la pregunta de cómo usar agentes en serio, esta guía la responde por etapas. Empezamos por el contexto, terminamos en governance.

**Diagnóstico**: el vocativo explícito ("tú, lector", "amigo desarrollador") suena a libro de autoayuda. El plural mayestático ("nos proponemos") suena a tesis. El impersonal sostenido ("se debe recordar") suena a manual genérico. Los tres rompen el contrato autoral.

---

## 3. Definir en una frase y seguir

El término técnico llega con definición seca y se sigue. Sin párrafo de calentamiento previo, sin sinónimos repetidos detrás.

**Antes:**
> Antes de adentrarnos en el concepto, conviene que reflexionemos sobre qué es realmente un prompt. En el ámbito del trabajo con LLMs, un prompt podríamos definirlo, en términos generales, como una entrada o input que le proporcionamos al modelo, también conocido como instrucción, mensaje o consulta, con el fin de obtener una respuesta.

**Después:**
> Un *prompt* es la entrada de texto que damos al modelo para que genere una respuesta. A partir de ahí, todo el trabajo de prompt engineering es decidir qué metes y en qué orden.

**Diagnóstico**: cualquier párrafo de "antes de definir, reflexionemos sobre…" es relleno. El lector adulto no necesita el calentamiento. Define y sigue.

---

## 4. Validar la intuición ingenua antes de afilarla

Si el lector llega con una idea aproximada de algo, primero la nombras, luego muestras dónde se queda corta, y solo entonces traes el término técnico exacto. La corrección llega después de la confusión, no antes.

**Antes (corrección antes de confusión):**
> El context window es el conjunto de tokens que el modelo procesa en una sola pasada. No debe confundirse con la memoria a largo plazo, que es un mecanismo aparte.

**Después (validar primero, afilar después):**
> Cuando empiezas, piensas que el modelo "se acuerda" de lo que le has dicho. Hasta cierto punto. Lo que tiene es una ventana abierta delante: todo lo que cabe ahí, lo ve. Lo que no cabe, no existe para él. A esa ventana se la llama *context window*, y su tamaño cambia el juego.

**Diagnóstico**: cuando el término técnico llega antes que la intuición, el lector lo memoriza sin entenderlo. Cuando llega después de la confusión nombrada, el término aterriza.

---

## 5. El paréntesis honesto — tres modalidades

Aside autorial que reconoce dificultad, costo, ejemplo concreto o pendiente honesto, sin romper la línea principal del argumento. La calibración de los 4 samples documenta tres modalidades distintas, todas legítimas. El paréntesis es recurso escrito por excelencia (no se puede entonar bien hablado), por eso es marca de prosa autorial.

### 5a. Paréntesis didáctico (Karpathy)

Aclara, ejemplifica o reconoce dificultad. Bajada de voz dentro del argumento.

- "(esto es lo que más confunde al principio)"
- "(el caso clásico es un agente que reescribe tu test en vez de hacer el cambio)"
- "(en mi experiencia, ocurre la primera vez que tocas una codebase ajena)"
- "(un commit, un pago, una llamada irreversible)"
- "(cuesta más de lo que parece)"

### 5b. Paréntesis irónico (firma propia)

Confirma con humor lo dicho, normalmente al cierre de una frase con tono cómplice.

- "(Algo completamente cierto)" — después de afirmar que el modelo no entiende
- "(spoiler: sí)" — después de plantear si una sospecha se va a confirmar
- "(no, no es coincidencia)"

### 5c. Paréntesis editorial (en draft)

Flagea honestamente un pendiente metodológico en lugar de inventar fuente o saltarlo. Típico de borradores trabajados; en versión final pasa a SOURCES.md o se completa.

- "(habría que añadir aquí investigaciones — pendiente)"
- "(pendiente: confirmar fecha exacta del estudio Apiiro)"
- "(este caso necesita ejemplo real, no inventado)"

**Antes (sin paréntesis honesto):**
> El prompt caching reduce coste y latencia, pero requiere que la parte cacheable del prompt se mantenga estable.

**Después (con didáctico):**
> El prompt caching reduce coste y latencia (el ahorro real depende del tamaño del bloque cacheable), pero requiere que la parte cacheable se mantenga estable. Si cambiamos el system prompt cada llamada, no cacheamos nada.

**Diagnóstico**: el paréntesis honesto no es muletilla. Es señal de que la autora sabe lo que pasa cuando esto se aplica fuera del aula, o reconoce honestamente lo que aún no sabe. Una vez por sub-sección como criterio; el editorial puede aparecer más en draft, menos en versión final.

---

## 6. Conectores casuales, no cultos

Los conectores marcan ritmo. Los cultos enfrían.

**Conectores que sí (casuales):**
"Pero", "Así que", "Lo raro es que", "Hasta aquí", "Vuelve al ejemplo", "Aquí está la cosa", "Lo que pasa es que", "Y entonces", "El truco está en que", "Volvemos al principio".

**Conectores que no (cultos / burocráticos):**
"Asimismo", "en consecuencia", "cabe destacar", "por ende", "es menester", "no obstante" (acotado, raro), "huelga decir", "a saber", "en virtud de".

**Antes:**
> El context window tiene un tamaño finito. Asimismo, la latencia aumenta con el número de tokens procesados. En consecuencia, debemos optimizar el contenido del prompt.

**Después:**
> El context window tiene un tamaño finito. Cuanto más metes, más tarda en responder. Así que toca elegir qué entra y qué se queda fuera.

**Diagnóstico**: el conector culto sube el registro sin aportar precisión. El casual baja el registro y mantiene el argumento.

---

## 7. Autoridad por especificidad

Un caso real con nombre, fecha, comando o número convence más que diez frases generales.

**Antes (genérico):**
> Existen estudios que muestran que el código generado por IA tiende a tener más vulnerabilidades. Es importante revisarlo cuidadosamente antes de mergear.

**Después (específico):**
> Apiiro analizó 50 empresas Fortune en 2025. El código generado por IA tenía un 322 % más de vulnerabilidades de privilege escalation que el escrito por humanos. La conclusión no es no usarlo; es revisar el diff antes de aceptar, sobre todo en código que toca permisos.

**Antes (escena vaga):**
> Imagina que tienes un sistema con varias APIs.

**Después (escena concreta):**
> Tu repo tiene tres servicios: `auth`, `billing` y `notifications`. El agente acaba de meter una llamada de `notifications` a `billing` saltándose `auth`. ¿La aceptas?

**Diagnóstico**: "imagina que…" es señal de que la autora no tiene caso real a mano. Toda escena hipotética se beneficia de un caso documentado o de cicatriz propia.

---

## 8. Variación de longitud sin frase larga adornada

Mezcla de frase corta, media y larga. La larga reservada para construir argumento concreto, no para lucir subordinación. Si una frase tiene más de tres incisos, romperla.

**Antes (larga adornada):**
> El harness, entendido como el conjunto de mecanismos que rodean al modelo —incluyendo el loop de ejecución, las herramientas disponibles, la gestión de contexto, la observabilidad y los evaluadores—, constituye, en última instancia, el verdadero diferencial entre un prototipo y un sistema en producción, dado que es ahí donde se definen las garantías operativas.

**Después (variación):**
> El harness es lo que rodea al modelo. Loop, herramientas, contexto, observabilidad, evaluadores. Todo lo que decide si el modelo hace algo útil o destruye un repo. Y todo lo que un prototipo no tiene.

**Diagnóstico**: la frase larga vale cuando construye argumento que no cabe en frases cortas. Si está adornada (incisos, restatement, parentéticos), es vanidad.

---

## 9. Cierres bajos

Sección y capítulo cierran con observación seca, instrucción accionable, deseo de buena suerte o pregunta abierta concreta. Nada de moralejas, nada de "el viaje no termina aquí".

**Antes (moraleja):**
> En definitiva, vivimos un momento extraordinario en la historia del software. Las herramientas que tenemos hoy nos permiten construir lo que ayer parecía imposible. ¡Adelante! El futuro está en tus manos.

**Después (observación seca):**
> Y las dos cosas escalan mal.

**Después (instrucción accionable):**
> Antes del siguiente capítulo, audita tu AGENTS.md con el rubric del anexo.

**Después (pregunta abierta concreta):**
> ¿Cuál de los seis antipatrones ya viste en una PR de tu equipo este mes?

**Después (bisagra al siguiente):**
> El cap. 20 te da el AGENTS.md operativo. Aquí cerramos viendo por qué tu repo lo necesita.

**Diagnóstico**: el cierre alto deja al lector con energía falsa que se evapora en cinco minutos. El cierre bajo le deja un pendiente concreto que aterriza en su semana.

---

## 10. Una metáfora sensorial / física por concepto fuerte (con o sin retorno)

Cocina, oficina, tráfico, taller, cuerpo humano. Sensorial o física, doméstica o mecánica. Nunca cósmica. Puede volver una vez para complicarse — no es obligación. La calibración de los 4 samples documenta cuatro metáforas en explanation, algunas vuelven, otras viven solas. Las dos formas funcionan.

**Antes (metáfora cósmica desechable):**
> El context window es como una galaxia: cuanto más grande, más cosas puedes meter en ella, pero también más fácil te pierdes en su inmensidad.

**Después (metáfora doméstica que vuelve):**
> El context window es la mesa de trabajo del modelo. Todo lo que cabe encima, lo ve y lo usa. Lo que no cabe, no existe. Cuando empezamos a meter el repo entero, la mesa se llena de papeles que tapan los importantes. Es entonces cuando el modelo "olvida" la instrucción inicial: no la olvida, la tiene tapada por tres archivos que pesan más.
>
> [tres párrafos después]
>
> Volvamos a la mesa. Si tuviéramos que decidir qué papeles se quedan encima cuando la pila amenaza con caerse, ¿qué descartaríamos? Esa decisión es la que toma `compaction`.

**Después (metáfora doméstica que vive sola, también vale):**
> Pensemos en un muro que recubre todo el comportamiento del agente. La primera línea es aquella barrera de piedra impenetrable que construye las instrucciones base y las restricciones que sí o sí debe seguir el modelo bajo ese contexto.

**Diagnóstico**: la metáfora cósmica es decoración. La metáfora doméstica vale tanto si vuelve como si no. Si vuelve, que aporte (complicada, reformulada). Si no vuelve, también vale — la del "no haber escuchado" en explanation rinde sola y aterriza.

### Cuándo NO usar metáfora doméstica

- En reference: registro catálogo, no hay sitio.
- En how-to: la receta no necesita imagen, el paso es la imagen.
- Cuando el concepto técnico es transparente sin metáfora (`max_tokens` = tokens máximos; `seed` = semilla aleatoria).

---

## Casos de duda

### ¿Y si la apertura concreta suena demasiado costumbrista?

Equilibra con la siguiente frase: la primera es escena, la segunda nombra el problema técnico que la escena ilustra. Sin la segunda, la apertura queda de blog personal.

### ¿Cuánto yo es demasiado?

Una o dos apariciones de yo por capítulo. Tres ya es exceso. El yo se reserva para confesión costosa o juicio personal con cicatriz, no para "yo creo que" como muletilla.

### ¿La metáfora doméstica funciona en reference?

No. Reference es catálogo, no narrativa. La metáfora doméstica vive en explanation y en ciertos pasajes de tutorial. En reference y how-to, prosa mínima.

### ¿Conector casual en explanation académica?

Sí. La explanation no es ensayo académico; es argumento técnico. "Pero" y "Así que" funcionan en explanation; "asimismo" no.

### ¿Y si el paréntesis honesto se siente forzado?

Si tienes que inventarte la cicatriz, no lo metas. El paréntesis honesto es honesto: si no hay anécdota real ni ejemplo concreto a mano, mejor frase plena.
