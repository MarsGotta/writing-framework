# Tu primer agente con tool use en el SDK de Anthropic

> Modalidad: tutorial. Objetivo: que el lector tenga un agente mínimo funcionando con una herramienta personalizada.
> Duración estimada: 15 minutos.

En este tutorial veremos cómo construir un agente básico que utiliza tool use. Tool use es la funcionalidad que le permite al modelo invocar funciones que tú defines, recibir el resultado y usarlo para continuar la generación. Es un mecanismo importante para conectar al modelo con sistemas externos.

Antes de comenzar, asegúrate de tener instalado el SDK de Anthropic y configurada tu API key como variable de entorno.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=tu-key
```

A continuación, vamos a definir nuestra herramienta. En este caso, será una herramienta simple que devuelve la temperatura actual de una ciudad. En un caso real, esta función llamaría a una API meteorológica, pero para los efectos del tutorial devolveremos un valor simulado.

```python
def get_temperature(city: str) -> dict:
    return {"city": city, "temperature": 22, "unit": "celsius"}
```

Ahora definimos el esquema de la herramienta para que el modelo sepa cómo invocarla. El esquema sigue el formato JSON Schema y describe los parámetros que la función espera.

```python
tools = [{
    "name": "get_temperature",
    "description": "Devuelve la temperatura actual de una ciudad",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Nombre de la ciudad"}
        },
        "required": ["city"]
    }
}]
```

Con la herramienta definida, podemos crear el cliente y hacer la primera llamada al modelo. El modelo recibirá la pregunta del usuario, decidirá si necesita usar la herramienta, y en caso afirmativo nos devolverá una solicitud de invocación.

```python
from anthropic import Anthropic
client = Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "¿Qué temperatura hace en Madrid?"}]
)
```

Si revisamos la respuesta, veremos que el modelo ha decidido usar la herramienta. La respuesta contiene un `tool_use` block con el nombre de la herramienta y los argumentos.

A continuación, ejecutamos la función localmente y le devolvemos el resultado al modelo en una segunda llamada, esta vez incluyendo el historial completo y el bloque `tool_result`.

```python
result = get_temperature(city="Madrid")
followup = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "¿Qué temperatura hace en Madrid?"},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": response.content[0].id,
            "content": str(result)
        }]}
    ]
)
```

El modelo ahora tiene el dato y puede generar una respuesta final en lenguaje natural para el usuario. Con esto tienes un agente mínimo que sabe usar una herramienta. El siguiente paso natural es añadir un loop para que el modelo pueda encadenar varias invocaciones de herramientas hasta resolver la tarea completa.
