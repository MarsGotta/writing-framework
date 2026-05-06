# Registros por modalidad Diátaxis — detalle

Cada modalidad pide su propio registro de prosa. Este documento expande los cuatro registros con ejemplos before/after y reglas de detección.

<!-- Origen: guide-ai-developers/STYLE.md §2 + technical-guide-design (Diátaxis: Tutorial, How-to, Reference, Explanation) -->

---

## Identificar la modalidad antes de editar

Antes de aplicar registro, identifica la modalidad del bloque. Pregunta por bloque:

- **Tutorial**: ¿el lector está aprendiendo a hacer algo siguiéndome paso a paso? → registro escena.
- **How-to**: ¿el lector tiene un problema concreto y quiere la receta? → registro instrucción.
- **Reference**: ¿el lector busca dato, sintaxis, tabla, equivalencia? → registro catálogo.
- **Explanation**: ¿el lector quiere entender por qué algo es como es? → registro argumento.

Un bloque que mezcla dos modalidades se parte. Un capítulo entero que mezcla las cuatro se replantea.

---

## Tutorial → registro escena

### Reglas

- Narración paso a paso.
- Primera persona plural ("vamos a", "abrimos", "vemos").
- Presente del indicativo.
- El lector va con nosotros, no detrás.
- Cada paso muestra el resultado completo antes de pedir transferencia (worked example effect).
- Worked example efecto: primer paso, todo resuelto. Segundo paso, parcial. Tercero, blanco.
- Las anécdotas ("la primera vez que hice esto fallé en X") son bienvenidas.

### Antes (mezcla con explanation)

> El testing unitario es la práctica de validar el comportamiento de unidades aisladas de código. Para empezar, instalaremos Vitest, que es un framework moderno basado en ESM. Vitest se diferencia de Jest principalmente en la velocidad de arranque y en su integración con Vite, lo cual veremos en detalle. Vamos a configurarlo.

### Después (escena pura)

> Vamos a escribir tu primer test con Vitest. Empezamos por instalar el paquete:
>
> ```bash
> npm install --save-dev vitest
> ```
>
> Vitest se instala. Ahora abrimos `package.json` y añadimos un script:
>
> ```json
> "scripts": {
>   "test": "vitest"
> }
> ```
>
> Lo lanzamos:
>
> ```bash
> npm test
> ```
>
> Vitest arranca, busca archivos `*.test.ts`, no encuentra ninguno y se queda en watch mode. Está listo. Ahora le damos algo que ejecutar.

### Diagnóstico

- Si el bloque "tutorial" pasa más de dos párrafos sin un comando o un fragmento de código, está derivando a explanation.
- Si la voz se vuelve impersonal ("se ejecuta el comando"), perdió la primera persona plural. Vuelve a "ejecutamos".

---

## How-to → registro instrucción (plural inclusivo modal)

### Reglas

- **Plural inclusivo modal por defecto**: "podemos", "tenemos que", "vamos a", "volvemos", "aplicamos". No imperativo seco como registro dominante.
- **Imperativo puntual** cuando la operación es una sola línea ("lanza", "Marca", "Verifica"). Rodeado de plural inclusivo.
- Pasos numerados o con bullets.
- Sin preámbulo largo. Asume lector competente que ya sabe qué quiere conseguir.
- Sin escena de tutorial: el lector no quiere historia, quiere receta.
- Bloques de código self-contained y mínimos.
- Una receta = un objetivo. Si la receta tiene dos objetivos, parte en dos how-tos.

### Antes (imperativo seco como registro dominante)

> Para estabilizar un pipeline de evaluación con resultados inconsistentes:
>
> 1. Define la rúbrica en `eval-rubric.md`. Una métrica por línea, criterio binario.
> 2. Lanza el evaluador con `--rubric eval-rubric.md`.
> 3. Repite la corrida tres veces sobre el mismo dataset.
> 4. Si la varianza entre corridas supera el 5 %, baja la temperatura a 0.
> 5. Si la nota media baja de 7, recalibra la rúbrica.

### Después (plural inclusivo modal con imperativo puntual, calibración)

> Para estabilizar un pipeline de evaluación con resultados inconsistentes, vamos a hacer cinco movimientos:
>
> 1. Definimos la rúbrica en `eval-rubric.md`. Una métrica por línea, criterio binario.
> 2. Lanza el evaluador con `--rubric eval-rubric.md`.
> 3. Repetimos la corrida tres veces sobre el mismo dataset.
> 4. Si la varianza entre corridas supera el 5 %, bajamos la temperatura a 0.
> 5. Si la nota media baja de 7, recalibramos la rúbrica.

Plural inclusivo en los movimientos colectivos ("definimos", "repetimos", "bajamos"); imperativo en la operación atómica de una línea (paso 2). Esta mezcla es la voz how-to de Marcela según los samples editados.

### Antes prohibido (con escena de tutorial)

> Imagínate que estás en una situación donde tu pipeline de evaluación está dando resultados inconsistentes…

### Diagnóstico

- Si abres con "imagínate que" o "supón que" como tesis abstracta, estás contaminando con tutorial. Quítalo. (Distinto de "imaginemos que…" para validar intuición — ver `prosa-con-pulso.md` regla 4.)
- Si la receta no es escaneable (todo en prosa larga), conviértela en pasos numerados.
- Si la receta usa imperativo seco como registro dominante, está sin calibrar — pasa a plural inclusivo modal con imperativo puntual.
- Si un paso necesita más de dos frases para explicarse, parte en sub-pasos.

---

## Reference → registro catálogo

### Reglas

- Prosa mínima.
- Tablas, listas comparativas, definiciones secas.
- El lector busca dato, no argumento.
- Los anglicismos se introducen una vez en cursiva con definición seca; el resto, en redonda.
- Cero metáforas, cero anécdotas, cero conectores casuales largos.
- Si una entrada de tabla necesita explicación de más de una frase, mueve esa explicación a la columna "notas" o a una nota a pie.

### Antes (con argumento)

> Las temperaturas en LLMs son un parámetro fascinante. La temperatura controla cuán aleatorio es el muestreo del modelo, y eso tiene implicaciones profundas. Cuando ponemos temperature en 0, el modelo se comporta de manera totalmente determinista, lo cual es ideal para tareas donde necesitamos reproducibilidad, como por ejemplo en código. En cambio, cuando subimos la temperatura por encima de 0.7, el modelo se vuelve más creativo, lo que es útil para prosa o brainstorming.

### Después (catálogo)

> | Parámetro | Significado | Rango | Recomendado |
> |---|---|---|---|
> | `temperature` | Aleatoriedad del muestreo | 0.0–2.0 | 0.0–0.3 para código, 0.7 para prosa |
> | `top_p` | Probabilidad acumulada de muestreo | 0.0–1.0 | 0.9 por defecto, no tocar si tocas `temperature` |
> | `max_tokens` | Tokens máximos en la respuesta | 1–32k+ | El menor que cubra la respuesta esperada |

### Diagnóstico

- Si el reference tiene párrafos de más de tres oraciones, está derivando a explanation.
- Si una tabla tiene una columna "descripción" con explicaciones de varias líneas, parte en dos tablas o pasa esa columna a notas.
- Si tienes que explicar la columna, la columna está mal nombrada.

---

## Explanation → registro argumento

### Reglas

- Prosa con tensión: tesis, contraste, evidencia, conclusión.
- Ningún capítulo de explanation es solo "¿qué es X?". Es "por qué X cambia algo del oficio".
- Acepta paréntesis honesto, metáfora doméstica sostenida, conectores casuales.
- Variación de longitud de frase: corta, media, larga, conviven.
- Cierre con observación seca, no con resumen.

### Antes (definición plana)

> El context window es el conjunto de tokens que el modelo procesa en una sola pasada. Es importante entenderlo porque condiciona muchas decisiones técnicas. Los modelos modernos tienen context windows de 128k, 200k o incluso 1M tokens.

### Después (argumento)

> El context window no es solo un límite técnico. Es lo que decide qué del repo el modelo "sabe" y qué inventa. Y eso convierte el orden de lo que metes en una decisión de arquitectura.
>
> Cuando pides a un agente que refactorice un servicio, lo que cabe en el context window es lo que el modelo va a tener en cuenta. El resto, lo va a inferir. Y la inferencia, en código, se llama hallucinación.
>
> Hay dos formas de gestionar esto: ampliar la ventana (caro, lento, hay un techo) u ordenar mejor lo que entra. La segunda es harness engineering. La primera es resignarse.

### Diagnóstico

- Si la explanation no tiene tesis identificable en el primer párrafo, no es explanation. Es definición disfrazada.
- Si el cierre es "en resumen, hemos visto que…", no es cierre. Es resumen mecánico.
- Si no hay contraste (X vs Y, antes vs después, fácil vs costoso), falta tensión.

---

## Mezcla intencional vs. accidental

A veces una sub-sección de un capítulo cambia de modalidad y debe cambiar de registro. Eso es legítimo cuando es intencional y se señala. Por ejemplo, en un capítulo de explanation puede aparecer un mini how-to ("para verlo en tu repo, lanza:"). Cuando ocurre:

1. Marca el cambio visualmente: subtítulo, callout, bloque de código.
2. Aplica el registro correspondiente al bloque, no el del capítulo.
3. Vuelve al registro original al cerrar el bloque.

Mezcla accidental (el ejemplo "Antes" de Tutorial al inicio): el bloque deriva sin querer porque la autora se enredó. Síntoma: la prosa se hincha, el lector pierde el hilo. Solución: identificar la modalidad real del bloque y separarlo en sección propia.

---

## Tabla rápida

| Si dudas... | Modalidad | Registro |
|---|---|---|
| El lector va a copiar/pegar y ejecutar siguiéndome paso a paso | Tutorial | Escena, primera persona plural, worked example |
| El lector tiene un problema y quiere la receta | How-to | Instrucción, plural inclusivo modal con imperativo puntual, sin preámbulo |
| El lector busca un dato concreto | Reference | Catálogo, tabla, prosa mínima |
| El lector quiere entender por qué algo es como es | Explanation | Argumento, tesis-contraste-evidencia, paréntesis honesto |
