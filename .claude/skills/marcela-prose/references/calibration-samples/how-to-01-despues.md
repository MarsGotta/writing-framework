# Cómo recortar el contexto cuando el agente se acerca al límite

> Modalidad: how-to. Objetivo: dar al lector una receta concreta para reducir el tamaño del contexto sin perder información crítica.

Cuando estamos trabajando con un agente de IA corremos el riesgo saturar su contexto, para ello es recomendado analizar qué es lo mejor para nuestro caso, cuando el agente se acerca al límite de su context window. Y para ello tenemos tres opciones: podemos ampliar la ventana de contexto aunque esta no siempre posible y siempre es más caro, resetear la conversación, pero en este caso perderíamos el estado; o bien, recortar el contexto manteniendo lo esencial. Y es justo esta técnica, la que vamos a cubrir en esta guía.

Antes de ponernos manos a la obra, siempre es recomendable medir antes de aplicar cualquier técnica de recorte. Si no medimos, corremos el riesgo de recortar de más o de menos.

## Paso 1: medir

Primero vamos a calcular el tamaño actual del contexto en tokens. La mayoría de SDKs ofrece una utilidad para contar tokens sin enviar la petición.

```python
from anthropic import Anthropic
client = Anthropic()

count = client.messages.count_tokens(
    model="claude-opus-4-7",
    messages=conversation_history
).input_tokens
```

Si el resultado supera el 70 % del límite del modelo, es el momento de recortar. Por debajo de ese umbral, el recorte es prematuro.

## Paso 2: identificar lo prescindible

Luego de haber hecho la medicicón, tenemos que recorrer el historial y clasificar cada mensaje en una de estas categorías:

- **Crítico**: instrucciones del usuario, decisiones que afectan al estado actual, resultados de herramientas que el agente sigue usando.
- **Útil pero recuperable**: outputs largos de herramientas que pueden re-ejecutarse si se necesitan.
- **Prescindible**: pasos intermedios de razonamiento del agente, respuestas que ya quedaron superadas, tool results de hace muchos turnos cuyo valor ya está reflejado en mensajes posteriores.

## Paso 3: aplicar la técnica adecuada

Hoy en día, existen tres técnicas que podemos aplicar para este tipo de casos, abajo te las enseño muestro de menor a mayor agresividad.

**Técnica A: truncar tool results largos.** Si un `tool_result` ocupa más de 2.000 tokens y su valor ya está sintetizado en una respuesta posterior del agente, podemos sustituirlo por un resumen de una línea (`[truncated: 5.000 tokens, summary: 23 entries returned]`).

**Técnica B: comprimir bloques de pasos intermedios.** Si el agente ha dado vueltas razonando sobre un subproblema antes de llegar a una conclusión, podemos sustituir el bloque entero por un mensaje de sistema sintético (`[el agente exploró tres opciones y descartó dos, ver mensajes #12-18]`).

**Técnica C: compaction completa.** Si A y B no son suficientes, lanza una llamada al modelo pidiendo un resumen de todo el historial salvo los últimos 3-4 turnos. Podemos sustituir el historial recortado por ese resumen como mensaje de sistema. Marca claramente la frontera entre resumen y historial vivo.

## Paso 4: verificar

Después de cualquier recorte, ejecuta dos verificaciones rápidas:

1. ¿El siguiente turno del agente sigue teniendo sentido? Si pierde el hilo, has recortado de más.
2. ¿El recuento de tokens bajó al rango deseado? Si quedó por debajo del 50 % del límite, posiblemente recortaste demasiado.

Si alguna de las dos falla, volvemos al historial original y aplicamos una técnica menos agresiva.

## Cuándo no usar esta receta

Si el agente está en mitad de una transacción crítica (un commit, un pago, una llamada irreversible), no debemos recortar durante dicha transacción. Hay que esperar a que la transacción cierre o falle, y recortar entre transacciones.
