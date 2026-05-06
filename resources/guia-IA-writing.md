# Guía editorial para crear guías claras, naturales y útiles con IA

Esta guía sirve para dos cosas:

1. **Que tú tengas claro qué tipo de redacción estás buscando.**
2. **Que puedas explicárselo a un modelo de IA sin que te devuelva texto plano, robótico o demasiado comprimido.**

La idea central es esta:

> Una buena guía no debe sonar como una IA intentando parecer humana. Debe sonar como una persona experta explicando algo con orden, criterio y respeto por el tiempo del lector.

No buscamos un texto informal, gracioso o “con personalidad” forzada. Buscamos una redacción que sea **natural, clara, útil y conectada**.

---

# 1. Qué tipo de guía quieres conseguir

La guía ideal para ti debería tener estas características:

```text
- Tono experto, pero no académico.
- Frases claras, no comprimidas.
- Explicaciones conectadas, no saltos bruscos.
- Ejemplos concretos, no bullets genéricos.
- Criterio práctico, no teoría flotando.
- Transiciones suaves entre ideas.
- Menos frases de eslogan.
- Menos anglicismos innecesarios.
- Más orientación al lector.
- Más “qué hago con esto”.
```

No quieres esto:

```text
La economía no es opcional: es estructural.
Quedan tres categorías.
Cabe en la cabeza.
La herramienta estaba. El procedimiento, no.
```

Ese estilo puede sonar contundente, pero si se repite demasiado, parece texto resumido por una IA o notas internas convertidas en párrafo final.

Quieres más bien esto:

```text
El coste forma parte del diseño del agente. Cada archivo que el agente lee, cada resultado de herramienta que recibe y cada respuesta que genera consume contexto y presupuesto. Por eso conviene medir una sesión real antes de decidir si un flujo es viable.
```

La segunda versión es más larga, pero también más clara. No obliga al lector a reconstruir la intención.

---

# 2. Principio editorial base

La regla principal es:

```text
No ahorrar palabras si eso rompe la comprensión.
```

Una frase corta no siempre es mejor. Una frase breve puede ser buena si es clara. Pero una frase demasiado comprimida puede volverse ambigua, seca o robótica.

La IA suele fallar cuando intenta hacer esto:

```text
Idea técnica + frase ingeniosa + cierre contundente.
```

Ejemplo malo:

```text
Cuando el presupuesto importa, no se estima: se mide.
```

Ejemplo mejor:

```text
Si el coste importa, mide una sesión real. Las estimaciones a ojo suelen fallar porque el gasto depende del contexto, del historial, de las herramientas y de la salida generada.
```

La segunda frase no intenta sonar brillante. Explica mejor.

---

# 3. La voz que debe usar la IA

Puedes definir la voz así:

```text
Escribe como una persona experta que quiere ayudar a otra persona técnica a entender y aplicar una idea. Usa un tono claro, directo y sobrio. No escribas como un manual burocrático, pero tampoco como una charla informal. Evita frases de eslogan. Explica lo suficiente para que el lector no tenga que adivinar la conexión entre ideas.
```

## Rasgos de la voz deseada

| Rasgo         | Cómo debe verse en el texto                                         |
| ------------- | ------------------------------------------------------------------- |
| **Natural**   | Frases que suenan como explicación final, no como notas internas.   |
| **Clara**     | Sujetos concretos, referentes claros, pocos pronombres vagos.       |
| **Útil**      | Cada sección termina en una decisión, una advertencia o una acción. |
| **Sobria**    | Sin entusiasmo artificial ni frases promocionales.                  |
| **Conectada** | Las ideas no saltan; una lleva a la siguiente.                      |
| **Técnica**   | No simplifica de más ni pierde precisión.                           |
| **Práctica**  | Usa ejemplos reales, síntomas, errores comunes y checklists.        |

---

# 4. Lo que la IA debe evitar

Esta lista es importante porque los modelos tienden a repetir patrones.

## Evitar frases demasiado sentenciosas

No abusar de estructuras como:

```text
No es X: es Y.
No se estima: se mide.
No es magia: es sistema.
Delegar sin criterio no es delegar.
La economía no es opcional: es estructural.
```

No están prohibidas, pero deben usarse poco. Como regla:

```text
Máximo una frase sentenciosa por capítulo, y solo si realmente cierra una idea importante.
```

## Evitar frases comprimidas

Malo:

```text
Cabe en la cabeza, deja sitio para que cada concepto técnico aterrice en algo reconocible.
```

Mejor:

```text
Usaremos un ejemplo pequeño para que el lector pueda seguirlo sin aprender un dominio nuevo. Además, al mantener el mismo caso durante toda la guía, cada concepto técnico se puede explicar sobre una situación ya conocida.
```

## Evitar pronombres vagos

Revisar con cuidado:

```text
lo
eso
esto
aquello
esa capa
esa decisión
ese problema
```

Malo:

```text
Desarrolladores que sienten que lo aceptan a ciegas y quieren cambiar eso.
```

Mejor:

```text
Desarrolladores que reciben PRs generados por agentes, pero sienten que a veces aprueban cambios que no entienden del todo.
```

## Evitar transiciones secas

Malo:

```text
Quedan tres categorías.
Vamos a verlo.
Pasemos al siguiente punto.
```

Mejor:

```text
Con esa distinción, podemos separar tres casos.
```

```text
Para entender por qué ocurre, hay que mirar qué entra realmente en el contexto.
```

```text
Ese problema nos lleva al siguiente componente: la memoria.
```

## Evitar metáforas mezcladas

Malo:

```text
Deja sitio para que cada concepto técnico aterrice.
```

Mejor:

```text
Permite explicar cada concepto con el mismo ejemplo.
```

## Evitar anglicismos innecesarios

Mantener términos técnicos cuando sean necesarios:

```text
harness
MCP
skill
system prompt
tool use
context window
```

Pero traducir los que no aportan precisión:

| Evitar            | Mejor                                    |
| ----------------- | ---------------------------------------- |
| mental model      | modelo mental                            |
| bullet hipotético | ejemplo inventado                        |
| scope             | alcance                                  |
| baseline          | punto de partida / línea base            |
| inline            | dentro del endpoint / en la misma lógica |
| datasource        | fuente de datos                          |
| built-in          | integrado / nativo                       |

---

# 5. Estructura mental que debe seguir la IA

La IA no debe escribir directamente. Primero debe entender cuatro cosas:

```text
1. Quién va a leer la guía.
2. Qué problema tiene esa persona.
3. Qué debe poder hacer después de leerla.
4. Qué tono y nivel de detalle necesita.
```

Antes de redactar, el modelo debería construir este brief:

```text
Audiencia:
[quién lee]

Problema:
[qué le pasa ahora]

Resultado esperado:
[qué podrá hacer después]

Nivel:
[principiante, intermedio, avanzado]

Tono:
[experto, directo, natural, sobrio]

Conceptos obligatorios:
[lista]

Ejemplo recurrente:
[caso que se usará durante toda la guía]

Riesgos:
[qué malentendidos hay que evitar]

Acciones prácticas:
[qué debe hacer el lector al terminar]
```

Sin este brief, la IA tiende a escribir genérico.

---

# 6. La fórmula de cada explicación

Usa esta secuencia:

```text
Situación → explicación → consecuencia práctica
```

Es la regla más útil para que el texto suene natural.

## Ejemplo

Malo:

```text
La memoria entra al contexto. El contexto, sin memoria que lo respalde, se evapora.
```

Mejor:

```text
La memoria solo ayuda cuando el harness la carga en el contexto. Si una decisión no se guarda fuera de la sesión, el agente no podrá recuperarla después. Por eso las instrucciones estables del proyecto deben vivir en un archivo o sistema de memoria persistente.
```

La segunda versión hace tres cosas:

1. Explica la situación.
2. Aclara el mecanismo.
3. Dice qué hacer con esa idea.

---

# 7. Cómo debe organizarse una guía completa

Una buena guía no debería ser solo una lista de capítulos. Debe tener una progresión clara.

Estructura recomendada:

```text
1. Portada o título claro
2. Promesa de la guía
3. Para quién es
4. Para quién no es
5. Qué vas a aprender
6. Ruta rápida de lectura
7. Conceptos base
8. Desarrollo por capítulos
9. Checklists prácticos
10. Plantillas reutilizables
11. Errores comunes
12. Glosario
13. Fuentes o notas técnicas
```

## Ejemplo de apertura

```text
Esta guía es para personas que ya escriben código profesional y quieren delegar tareas a agentes de IA sin aceptar cambios a ciegas.

No enseña a programar desde cero. Enseña a mirar el sistema completo: modelo, contexto, memoria, herramientas, permisos, skills y specs.

Al terminar deberías poder revisar mejor un PR generado por IA, entender por qué un agente falla y preparar tu repositorio para trabajar con más criterio.
```

Esta apertura funciona porque:

- dice para quién es;
- dice para qué sirve;
- dice qué no promete;
- conecta con una preocupación real.

---

# 8. Estructura recomendada para cada capítulo

Cada capítulo debería seguir este patrón:

```text
1. Problema real
2. Definición breve
3. Por qué importa
4. Cómo funciona
5. Ejemplo concreto
6. Error frecuente
7. Qué hacer en la práctica
8. Checklist rápido
9. Puente al siguiente capítulo
```

## Plantilla de capítulo

```markdown
# [Nombre del capítulo]

## El problema

[Describe una situación que el lector pueda reconocer.]

## La idea clave

[Define el concepto sin hacerlo demasiado abstracto.]

## Por qué importa

[Explica qué cambia en la práctica.]

## Cómo funciona

[Explicación técnica suficiente, sin exceso.]

## Ejemplo

[Usa el caso recurrente de la guía.]

## Error frecuente

[Explica el malentendido más probable.]

## Qué hacer en la práctica

- [Acción 1]
- [Acción 2]
- [Acción 3]

## Checklist rápido

- [ ] [Comprobación concreta]
- [ ] [Comprobación concreta]
- [ ] [Comprobación concreta]

## Puente

[Explica por qué el siguiente capítulo continúa esta idea.]
```

---

# 9. Cómo usar ejemplos sin que parezcan genéricos

Los ejemplos deben ser pequeños, concretos y reutilizables.

Malo:

```text
Imagina una aplicación compleja con múltiples funcionalidades.
```

Mejor:

```text
Imagina una API REST de tareas con endpoints para crear, listar, actualizar y eliminar tareas. El agente debe modificar `POST /tasks` para añadir validación, mantener los tests verdes y no tocar la paginación de `GET /tasks`.
```

El segundo ejemplo es mejor porque tiene límites. El lector puede imaginar el problema.

## Regla para buenos ejemplos

Un buen ejemplo debe incluir:

```text
- Contexto
- Objetivo
- Restricción
- Riesgo
- Resultado esperado
```

Ejemplo:

```text
Contexto: API REST de tareas.
Objetivo: añadir validación al endpoint POST /tasks.
Restricción: no cambiar la estructura general del proyecto.
Riesgo: romper tests existentes o modificar archivos fuera del alcance.
Resultado esperado: el endpoint rechaza entradas inválidas y los tests siguen verdes.
```

---

# 10. Cómo hacer que una guía sea útil, no solo interesante

Una guía útil debe responder constantemente:

```text
¿Qué hago con esto?
¿Qué debo revisar?
¿Qué error evita?
¿Cuándo no aplica?
¿Cómo sé que funcionó?
```

Por eso cada capítulo debería incluir cajas como estas.

## Caja: Quédate con esto

```text
Quédate con esto

Un agente no falla solo por el modelo. También puede fallar por el contexto que recibió, las herramientas disponibles, los permisos, la memoria cargada o la spec que estaba siguiendo.
```

## Caja: Qué hacer mañana

```text
Qué hacer mañana

- Revisa si tu repositorio tiene instrucciones para agentes.
- Comprueba si esas instrucciones contienen decisiones estables del equipo.
- Elimina datos temporales, secretos o credenciales.
- Añade comandos de test y convenciones de revisión.
```

## Caja: Síntoma → causa probable

```text
Síntoma:
El agente repite una decisión que ya corregiste ayer.

Causa probable:
Esa decisión no quedó guardada en memoria persistente o no se cargó en el contexto actual.

Qué revisar:
Comprueba si existe un archivo tipo AGENTS.md, CLAUDE.md o equivalente, y si el harness lo está leyendo.
```

Este tipo de caja vuelve la guía más operativa.

---

# 11. Microestilo: cómo escribir cada frase

Aquí está el núcleo de lo que estás buscando.

## Regla 1: sujeto claro

Malo:

```text
Eso cambia la forma de revisar.
```

Mejor:

```text
Tener una spec cambia la forma de revisar.
```

Mejor todavía:

```text
Tener una spec cambia la revisión: ya no preguntas si el código “parece bien”, sino si cumple lo acordado.
```

## Regla 2: una idea principal por frase

Malo:

```text
Cabe en la cabeza, deja sitio para que cada concepto técnico aterrice en algo reconocible y evita el bullet hipotético.
```

Mejor:

```text
El ejemplo es pequeño a propósito. Permite seguir la guía sin aprender un dominio nuevo. También nos deja explicar cada concepto sobre el mismo caso, en lugar de usar ejemplos inventados en cada capítulo.
```

## Regla 3: no convertir todo en eslogan

Malo:

```text
No se estima: se mide.
```

Mejor:

```text
Si el coste importa, mide una sesión real. Las estimaciones a ojo suelen fallar.
```

## Regla 4: explicar la conexión entre ideas

Malo:

```text
Quedan tres categorías.
```

Mejor:

```text
Con esa distinción, podemos separar tres categorías.
```

Mejor todavía:

```text
Con esa distinción, podemos separar tres categorías que suelen mezclarse: el modelo, el workflow y el agente.
```

## Regla 5: evitar frases que parezcan notas internas

Malo:

```text
Tres razones operativas, ninguna decorativa.
```

Mejor:

```text
Entender los tokens importa por tres razones prácticas.
```

## Regla 6: usar transiciones con intención

Malo:

```text
Vamos a verlo.
```

Mejor:

```text
Para entender por qué ocurre, hay que mirar primero qué entra en el contexto.
```

## Regla 7: mantener precisión sin sonar seco

Malo:

```text
La herramienta estaba. El procedimiento, no.
```

Mejor:

```text
El agente tenía acceso a la herramienta, pero no al procedimiento que el equipo esperaba que siguiera.
```

---

# 12. Transformaciones útiles

Esta tabla resume cambios típicos que deberías pedirle a la IA.

| Texto débil                                    | Texto mejor                                                                                                       |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| “Eso cambia todo.”                             | “Esa decisión cambia la revisión del PR porque…”                                                                  |
| “Quedan tres categorías.”                      | “Con esa distinción, podemos separar tres casos.”                                                                 |
| “No es X: es Y.”                               | “Conviene no confundir X con Y. X sirve para…, mientras que Y…”                                                   |
| “Cabe en la cabeza.”                           | “Es pequeño y fácil de seguir.”                                                                                   |
| “Volvamos al ejemplo.”                         | “En la API de tareas, este problema aparece cuando…”                                                              |
| “Cuando importa, se mide.”                     | “Si el coste importa, mide una sesión real antes de decidir.”                                                     |
| “La memoria se evapora.”                       | “Si una decisión no se guarda fuera de la sesión, el agente no podrá recuperarla después.”                        |
| “La herramienta estaba. El procedimiento, no.” | “El agente podía usar la herramienta, pero no tenía instrucciones sobre cómo usarla según las reglas del equipo.” |

---

# 13. Cómo revisar una guía generada por IA

No hagas una sola revisión general. Haz varias pasadas, cada una con un objetivo.

## Pasada 1: estructura

Preguntas:

```text
- ¿La guía promete algo claro?
- ¿Está claro para quién es?
- ¿Cada capítulo tiene una función?
- ¿Hay una progresión lógica?
- ¿El lector sabe qué hacer al terminar?
```

## Pasada 2: utilidad

Preguntas:

```text
- ¿Cada concepto tiene un ejemplo?
- ¿Cada capítulo tiene una acción práctica?
- ¿Hay checklists?
- ¿Hay errores comunes?
- ¿Hay síntomas reales?
- ¿Hay criterios para saber si algo funcionó?
```

## Pasada 3: naturalidad

Preguntas:

```text
- ¿Hay frases que parecen notas internas?
- ¿Hay transiciones secas?
- ¿Hay pronombres vagos?
- ¿Hay demasiados eslóganes?
- ¿Hay metáforas raras?
- ¿El texto se puede leer en voz alta sin sonar artificial?
```

## Pasada 4: precisión

Preguntas:

```text
- ¿Hay datos inventados?
- ¿Hay versiones, precios o comandos que deben verificarse?
- ¿Hay afirmaciones demasiado absolutas?
- ¿Se distingue entre principio estable y dato temporal?
```

## Pasada 5: formato

Preguntas:

```text
- ¿Hay demasiado texto seguido?
- ¿Las cajas visuales ayudan?
- ¿Los ejemplos se distinguen del cuerpo?
- ¿Los títulos son claros?
- ¿El índice permite consultar rápido?
```

---

# 14. Checklist de naturalidad

Puedes usar esta lista antes de dar una guía por buena:

```text
- [ ] No hay frases comprimidas que obliguen a adivinar.
- [ ] Los pronombres “esto”, “eso” y “lo” tienen referente claro.
- [ ] Las transiciones explican por qué cambia el tema.
- [ ] No hay exceso de frases tipo “No es X: es Y”.
- [ ] Los anglicismos innecesarios están traducidos.
- [ ] Las metáforas no se mezclan.
- [ ] Cada capítulo incluye una consecuencia práctica.
- [ ] Los ejemplos son concretos.
- [ ] El texto no parece una lista de notas internas.
- [ ] Al leerlo en voz alta, suena como explicación final.
```

---

# 15. Checklist de utilidad

```text
- [ ] La guía explica para quién es.
- [ ] La guía explica para quién no es.
- [ ] Hay una promesa clara al inicio.
- [ ] Cada capítulo resuelve una duda real.
- [ ] Hay ejemplos reutilizables.
- [ ] Hay errores comunes.
- [ ] Hay “qué hacer en la práctica”.
- [ ] Hay checklists.
- [ ] Hay plantillas copiables.
- [ ] Hay criterios para revisar resultados.
- [ ] Hay advertencias sobre cuándo no aplicar el método.
```

---

# 16. Checklist de claridad técnica

```text
- [ ] Cada término técnico se define antes de usarse.
- [ ] Las diferencias importantes se explican con tablas o ejemplos.
- [ ] No se mezclan conceptos parecidos sin distinguirlos.
- [ ] Las afirmaciones absolutas están matizadas.
- [ ] Los datos temporales están marcados como verificables.
- [ ] Los comandos, versiones y precios no están enterrados en párrafos largos.
- [ ] Las fuentes o notas técnicas no interrumpen la lectura principal.
```

---

# 17. Cómo pedirle a una IA que escriba la guía desde cero

Este prompt sirve para generar una guía nueva con el estilo que buscas.

```text
Actúa como redactor técnico y editor exigente.

Quiero que escribas una guía clara, natural y útil. No quiero un texto que suene a IA, a notas internas ni a eslogan. Quiero una explicación que pueda leer una persona real sin tener que adivinar conexiones entre ideas.

Tema de la guía:
[tema]

Audiencia:
[quién va a leerla]

Nivel:
[principiante / intermedio / avanzado]

Objetivo del lector:
[qué debe poder hacer al terminar]

Ejemplo recurrente:
[caso que se usará durante toda la guía]

Tono:
Experto, claro, directo y sobrio. Algo conversacional, pero no informal. No académico. No promocional.

Reglas de redacción:
- Usa sujetos concretos.
- Evita pronombres vagos como “eso”, “esto” o “lo” cuando el referente no esté claro.
- No escribas frases comprimidas que parezcan notas internas.
- No abuses de frases tipo “No es X: es Y”.
- No uses frases de eslogan salvo que realmente cierren una idea importante.
- Evita metáforas forzadas o mezcladas.
- Usa anglicismos solo cuando sean términos técnicos necesarios.
- Explica la conexión entre una idea y la siguiente.
- Usa la estructura: situación → explicación → consecuencia práctica.
- Cada concepto importante debe tener un ejemplo.
- Cada capítulo debe terminar con una sección práctica.

Estructura de cada capítulo:
1. El problema
2. La idea clave
3. Por qué importa
4. Cómo funciona
5. Ejemplo concreto
6. Error frecuente
7. Qué hacer en la práctica
8. Checklist rápido
9. Puente al siguiente capítulo

Antes de escribir:
1. Crea un brief editorial.
2. Propón el índice.
3. Señala posibles dudas o datos que habría que verificar.

Después escribe la guía.
```

---

# 18. Cómo pedirle a la IA que mejore una guía existente

Este prompt sirve para reescribir una guía que ya existe.

```text
Haz una pasada de microedición sobre esta guía.

Objetivo:
Que el texto suene más natural, claro y útil, sin volverlo informal ni alargarlo de forma innecesaria.

Problema actual:
Algunas frases suenan comprimidas, inconexas, robóticas o como notas internas. Otras intentan sonar contundentes, pero quedan como eslóganes. Quiero que el texto respire más y que cada idea conecte mejor con la siguiente.

Corrige especialmente:
1. Frases comprimidas que mezclan varias ideas.
2. Pronombres vagos como “lo”, “eso” y “esto”.
3. Transiciones secas como “Vamos a verlo” o “Quedan tres categorías”.
4. Frases sentenciosas repetidas del tipo “No es X: es Y”.
5. Metáforas forzadas o mezcladas.
6. Anglicismos innecesarios.
7. Párrafos técnicos demasiado densos.
8. Cierres de sección que no preparan la siguiente idea.
9. Frases que parecen notas internas del autor.
10. Cambios bruscos de tono.

Reglas:
- Mantén el significado técnico.
- No inventes datos.
- No hagas el texto más informal.
- No llenes el texto de adornos.
- Añade contexto cuando una frase quede demasiado seca.
- Divide frases comprimidas.
- Sustituye eslóganes por explicaciones prácticas.
- Conserva solo las frases contundentes que realmente aporten.
- Prioriza claridad sobre brillo.

Patrón recomendado:
situación → explicación → consecuencia práctica.

Devuélveme:
1. Versión reescrita.
2. Lista de cambios importantes.
3. Frases que siguen necesitando verificación técnica.
```

---

# 19. Prompt específico para detectar frases robóticas

Este prompt es útil antes de reescribir.

```text
Analiza esta guía y detecta frases que suenan robóticas, comprimidas, inconexas o demasiado sentenciosas.

Busca:
- Pronombres vagos.
- Saltos lógicos.
- Frases tipo eslogan.
- Metáforas raras.
- Transiciones secas.
- Anglicismos innecesarios.
- Frases que parecen notas internas.
- Párrafos donde falte una consecuencia práctica.

Para cada caso, devuelve:
1. Frase original.
2. Problema.
3. Por qué puede sonar artificial.
4. Versión mejorada.
```

---

# 20. Prompt para revisar capítulo por capítulo

```text
Revisa este capítulo como editor técnico.

No hagas una reescritura superficial. Quiero que mejores claridad, naturalidad y utilidad.

Comprueba:
1. Si el capítulo empieza con un problema real.
2. Si cada concepto tiene un ejemplo.
3. Si hay frases comprimidas.
4. Si hay pronombres ambiguos.
5. Si hay demasiadas frases de eslogan.
6. Si las transiciones conectan las ideas.
7. Si el cierre deja una acción práctica.
8. Si hay algo que el lector pueda aplicar mañana.

Devuelve:
- Diagnóstico breve.
- Frases problemáticas.
- Reescritura recomendada.
- Checklist de mejoras pendientes.
```

---

# 21. Prompt para convertir una explicación en guía práctica

```text
Convierte esta explicación en una guía práctica.

No quiero solo una explicación conceptual. Quiero que el lector pueda aplicar la idea.

Añade:
- Problema inicial.
- Definición breve.
- Ejemplo concreto.
- Error frecuente.
- Síntomas reales.
- Qué revisar.
- Qué hacer.
- Checklist final.

Mantén un tono experto, natural y sobrio.
No uses frases de eslogan ni transiciones secas.
```

---

# 22. Prompt para reducir estilo “IA”

```text
Reescribe este texto para que suene menos a IA y más a una explicación humana experta.

No lo hagas más informal. No añadas humor. No uses frases decorativas.

Haz estos cambios:
- Sustituye frases genéricas por observaciones concretas.
- Añade sujetos claros.
- Cambia pronombres vagos por referencias explícitas.
- Divide frases demasiado comprimidas.
- Añade transiciones donde haya saltos.
- Sustituye frases sentenciosas por explicaciones prácticas.
- Mantén la precisión técnica.
- Elimina repeticiones de estructura.

Antes de reescribir, identifica qué frases producen el efecto artificial.
```

---

# 23. Cómo evaluar si una frase está bien escrita

Usa esta prueba rápida:

```text
¿La frase dice quién hace qué?
¿Está claro a qué se refiere “esto” o “eso”?
¿La frase explica algo o solo suena contundente?
¿Conecta con la frase anterior?
¿Prepara la siguiente idea?
¿El lector puede aplicar algo?
¿Suena bien leída en voz alta?
```

Si falla dos o más preguntas, hay que reescribirla.

---

# 24. Ejemplos de antes y después

## Ejemplo 1

Malo:

```text
Desarrolladores que sienten que “lo aceptan a ciegas” cuando el agente entrega un PR y quieren cambiar eso.
```

Bueno:

```text
Desarrolladores que ya reciben PRs generados por agentes, pero sienten que a veces aprueban cambios que no entienden del todo.
```

Mejor:

```text
Desarrolladores que quieren revisar PRs generados por IA con más criterio: qué cambió, por qué cambió, qué riesgos introduce y qué pruebas lo sostienen.
```

---

## Ejemplo 2

Malo:

```text
Cabe en la cabeza, deja sitio para que cada concepto técnico aterrice en algo reconocible.
```

Bueno:

```text
El ejemplo es pequeño a propósito. Una API REST de tareas es fácil de seguir, pero suficiente para mostrar problemas reales.
```

Mejor:

```text
Usaremos una API REST de tareas durante toda la guía. Es un caso pequeño, pero suficiente para hablar de validación, tests, contexto, memoria, herramientas y revisión de PRs sin cambiar de escenario en cada capítulo.
```

---

## Ejemplo 3

Malo:

```text
Quedan tres categorías.
```

Bueno:

```text
Con esa distinción, podemos separar tres categorías.
```

Mejor:

```text
Con esa distinción, podemos separar tres casos que suelen confundirse: el modelo, el workflow y el agente.
```

---

## Ejemplo 4

Malo:

```text
Cuando el presupuesto importa, no se estima: se mide.
```

Bueno:

```text
Si el coste importa, mide una sesión real.
```

Mejor:

```text
Si el coste importa, mide una sesión real. El gasto no depende solo del prompt inicial, sino también del historial, de las herramientas, de las iteraciones y de la salida generada.
```

---

## Ejemplo 5

Malo:

```text
La herramienta estaba. El procedimiento, no.
```

Bueno:

```text
El agente tenía la herramienta, pero no el procedimiento.
```

Mejor:

```text
El agente podía usar la herramienta, pero no tenía instrucciones sobre cómo usarla según las reglas del equipo.
```

---

# 25. Cómo debe pensar el modelo antes de escribir

Dale esta instrucción al modelo:

```text
Antes de escribir, no pienses solo en “qué información incluir”. Piensa en la experiencia del lector.

Para cada sección, responde internamente:
- Qué duda tiene el lector aquí.
- Qué malentendido puede cometer.
- Qué ejemplo le ayudaría.
- Qué decisión práctica debe sacar.
- Qué transición necesita para llegar al siguiente punto.
```

Esto es clave. La IA suele escribir ordenando información. Tú necesitas que escriba **acompañando al lector**.

---

# 26. Reglas para títulos

Los títulos deben ser claros antes que ingeniosos.

Malo:

```text
MCP: enchufar el mundo al agente
```

Bueno:

```text
MCP: conectar herramientas y datos al agente
```

También puedes combinar ambos:

```text
MCP: conectar herramientas y datos al agente
Cómo el agente consulta sistemas externos sin integrar cada caso a mano
```

## Buen título de capítulo

Un buen título debe decir:

```text
- De qué trata.
- Por qué importa.
- Qué problema resuelve.
```

Ejemplos:

```text
Contexto: qué ve el modelo en cada llamada
Memoria: qué puede conservar el agente entre sesiones
Harness: la capa que convierte un modelo en un agente operativo
Skills: procedimientos reutilizables para que el agente trabaje como el equipo espera
Specs: cómo fijar el objetivo antes de pedir código
```

---

# 27. Reglas para cierres de sección

Evita cierres que parezcan eslóganes. Un buen cierre debe hacer una de estas tres cosas:

```text
- resumir la decisión práctica;
- advertir de un error común;
- preparar el siguiente concepto.
```

Malo:

```text
No es magia. Es sistema.
```

Mejor:

```text
Cuando un agente falla, no basta con cambiar de modelo. Conviene revisar qué contexto recibió, qué herramientas tenía disponibles y qué instrucciones estaba siguiendo.
```

Malo:

```text
Vamos al siguiente tema.
```

Mejor:

```text
Una vez entendido el contexto, falta separar otra idea cercana: la memoria. El contexto explica lo que el modelo ve ahora; la memoria explica qué puede recuperar de una sesión a otra.
```

---

# 28. Reglas para párrafos técnicos

Cuando haya datos técnicos, no los metas todos en una sola frase.

Usa esta estructura:

```text
1. Principio estable.
2. Dato concreto.
3. Advertencia de mantenimiento.
4. Consecuencia práctica.
```

Ejemplo:

```text
No conviene calcular tokens a ojo.

En algunos proveedores puedes usar herramientas oficiales para estimar o medir tokens antes de enviar una solicitud. Los nombres, endpoints y precios cambian con el tiempo, así que estos datos deben verificarse antes de publicar una versión final.

Lo importante es el hábito: mide una sesión real cuando el coste importe.
```

Esto evita que el texto parezca una nota técnica pegada sin editar.

---

# 29. Cómo usar checklists sin que parezcan relleno

Las checklists deben servir para decidir, no para decorar.

Mala checklist:

```text
- Entender tokens.
- Revisar contexto.
- Usar memoria.
- Aplicar MCP.
```

Buena checklist:

```text
Antes de aceptar un PR generado por IA

- [ ] ¿El agente siguió una spec explícita?
- [ ] ¿El diff toca solo los archivos esperados?
- [ ] ¿Los tests cubren el caso nuevo?
- [ ] ¿Hay cambios que el agente no justificó?
- [ ] ¿Se modificó lógica fuera del alcance?
- [ ] ¿Puedes explicar por qué cada cambio era necesario?
```

La diferencia es que la segunda checklist permite actuar.

---

# 30. Cómo dar instrucciones al modelo sobre longitud

No le digas simplemente:

```text
Hazlo más humano.
```

Tampoco:

```text
Hazlo más corto.
```

Mejor:

```text
No alargues por decorar, pero tampoco comprimas ideas que necesitan contexto. Añade una frase cuando ayude a explicar el sujeto, la causa o la consecuencia práctica.
```

Esta instrucción es importante porque tu problema no es que el texto sea largo. Tu problema es que algunas frases están **demasiado comprimidas**.

---

# 31. Qué significa “natural” en tu caso

Para ti, natural no significa:

```text
- usar humor;
- escribir de forma informal;
- meter expresiones coloquiales;
- usar frases emocionales;
- sonar como una conversación de WhatsApp.
```

Natural significa:

```text
- que la frase tenga sujeto claro;
- que las ideas estén conectadas;
- que el lector no tenga que adivinar;
- que los ejemplos parezcan reales;
- que el texto explique en vez de posar;
- que haya criterio práctico;
- que el ritmo sea humano.
```

Esta definición conviene dársela al modelo.

---

# 32. El perfil editorial que debes darle a la IA

Puedes pegar esto como “guía de estilo” permanente:

```text
Guía de estilo

Queremos una redacción experta, clara, natural y útil.

El texto debe sonar como una persona técnica explicando con calma, no como una IA resumiendo notas.

Preferimos:
- sujetos concretos;
- frases conectadas;
- ejemplos reales;
- consecuencias prácticas;
- advertencias útiles;
- transiciones explícitas;
- tono sobrio;
- precisión técnica.

Evitamos:
- frases comprimidas;
- pronombres vagos;
- eslóganes;
- metáforas forzadas;
- anglicismos innecesarios;
- saltos lógicos;
- tono promocional;
- títulos demasiado ingeniosos;
- bullets genéricos;
- cierres secos.

Regla central:
Cada sección debe ayudar al lector a entender mejor, decidir mejor o hacer algo mejor.
```

---

# 33. Prompt maestro final

Este es el prompt más completo para generar una guía con el estilo que buscas.

```text
Actúa como redactor técnico senior y editor de guías prácticas.

Quiero que escribas una guía clara, natural y útil sobre:

[TEMA]

Audiencia:
[AUDIENCIA]

Nivel:
[NIVEL]

Objetivo:
[QUÉ DEBE PODER HACER EL LECTOR AL TERMINAR]

Contexto:
[CONTEXTO DEL PROYECTO, PRODUCTO O PROCESO]

Ejemplo recurrente:
[EJEMPLO QUE SE USARÁ DURANTE TODA LA GUÍA]

Tono:
Experto, claro, directo y sobrio. Algo conversacional, pero no informal. No académico. No promocional. No uses frases artificialmente brillantes.

Definición de “natural”:
Natural significa que el texto tiene sujetos claros, ideas conectadas, ejemplos concretos y consecuencias prácticas. No significa hacerlo gracioso ni coloquial.

Reglas de redacción:
1. No escribas frases comprimidas que parezcan notas internas.
2. No ahorres palabras si eso rompe la comprensión.
3. Usa sujetos concretos.
4. Evita pronombres vagos como “lo”, “eso” o “esto” cuando el referente no esté claro.
5. No abuses de estructuras tipo “No es X: es Y”.
6. Evita frases de eslogan.
7. Evita metáforas forzadas o mezcladas.
8. Usa anglicismos solo cuando sean términos técnicos necesarios.
9. Explica la conexión entre una idea y la siguiente.
10. Usa el patrón: situación → explicación → consecuencia práctica.
11. Cada concepto debe tener un ejemplo.
12. Cada capítulo debe cerrar con una parte práctica.
13. No inventes datos, versiones, precios, comandos ni fuentes.
14. Marca como [VERIFICAR] cualquier dato que pueda cambiar.
15. Mantén precisión técnica.

Estructura de la guía:
1. Título claro
2. Promesa de la guía
3. Para quién es
4. Para quién no es
5. Qué aprenderás
6. Ruta rápida de lectura
7. Capítulos principales
8. Checklists
9. Plantillas
10. Errores comunes
11. Glosario
12. Notas técnicas o fuentes

Estructura de cada capítulo:
1. El problema
2. La idea clave
3. Por qué importa
4. Cómo funciona
5. Ejemplo concreto
6. Error frecuente
7. Qué hacer en la práctica
8. Checklist rápido
9. Puente al siguiente capítulo

Antes de escribir:
- Crea un brief editorial.
- Propón el índice.
- Señala dudas o datos que habría que verificar.

Después:
- Escribe la guía.
- Haz una pasada de microedición.
- Lista las frases que podrían sonar comprimidas o artificiales.
- Propón mejoras.
```

---

# 34. Prompt maestro para reescribir una guía ya generada

```text
Actúa como editor técnico senior.

Voy a darte una guía ya escrita. Quiero que hagas una revisión profunda de naturalidad, claridad y utilidad.

Objetivo:
Que la guía deje de sonar como notas comprimidas o texto de IA, y pase a sonar como una explicación humana experta, clara y útil.

No busco:
- hacerla más informal;
- añadir humor;
- hacerla más promocional;
- meter frases bonitas;
- reducirla a toda costa.

Busco:
- sujetos claros;
- transiciones naturales;
- ejemplos concretos;
- consecuencias prácticas;
- menos eslóganes;
- menos frases comprimidas;
- más orientación al lector;
- más utilidad real.

Detecta y corrige:
1. Pronombres vagos.
2. Frases comprimidas.
3. Frases sentenciosas excesivas.
4. Metáforas mezcladas.
5. Anglicismos innecesarios.
6. Transiciones secas.
7. Párrafos técnicos densos.
8. Cambios bruscos de tono.
9. Cierres de sección que no conectan.
10. Ejemplos demasiado genéricos.

Reglas de reescritura:
- Mantén el significado técnico.
- No inventes datos.
- No cambies la tesis.
- No alargues por rellenar.
- Añade contexto solo cuando mejore la comprensión.
- Divide frases cuando mezclen demasiadas ideas.
- Sustituye eslóganes por explicaciones prácticas.
- Mantén un tono experto, directo y sobrio.

Devuelve:
1. Diagnóstico general.
2. Problemas por categoría.
3. Frases originales problemáticas.
4. Reescritura recomendada.
5. Checklist de mejoras pendientes.
6. Versión reescrita del texto.
```

---

# 35. La idea final que debe recordar el modelo

La instrucción más importante para la IA sería esta:

```text
No escribas para demostrar que entiendes el tema. Escribe para que el lector lo entienda sin esfuerzo innecesario.
```

Y la segunda:

```text
No conviertas cada idea en una frase brillante. Convierte cada idea en una explicación clara, conectada y aplicable.
```

---

# Resumen operativo

Para generar guías como te gustan, el modelo debe seguir esta fórmula:

```text
Brief claro
+ voz experta y sobria
+ ejemplo recurrente
+ estructura práctica
+ frases con sujeto claro
+ transiciones explícitas
+ menos eslóganes
+ menos compresión
+ más consecuencias prácticas
+ revisión de microestilo
```

El punto más importante es no pedir simplemente:

```text
Hazlo más humano.
```

Eso es demasiado vago.

Pídele esto:

```text
Hazlo más natural, claro y útil. Elimina frases comprimidas, pronombres vagos, transiciones secas y eslóganes. Usa sujetos concretos, conecta las ideas y convierte cada concepto en una consecuencia práctica para el lector.
```

Ese es el estilo que estás buscando.
