# Equivalencias de parámetros de muestreo entre Anthropic, OpenAI y Google

> Modalidad: reference. Tabla comparativa de los parámetros más usados de los tres APIs principales.
> Última verificación: 2026-04.

En esta referencia podemos ver la comparación de los parámetros de muestreo y generación entre las tres APIs más usadas del mercado. Está pensada para que la consultemos de forma puntual siempre que estemos migrando código de un proveedor a otro o cuando estemos construyendo un cliente es agnostico a cualquiera de estos modelos.

## Parámetros principales

| Parámetro      | Anthropic                | OpenAI                  | Google (Gemini)              | Notas                                                                 |
| -------------- | ------------------------ | ----------------------- | ---------------------------- | --------------------------------------------------------------------- |
| Temperatura    | `temperature` (0.0–1.0)  | `temperature` (0.0–2.0) | `temperature` (0.0–2.0)      | OpenAI y Google admiten valores hasta 2.0; Anthropic limita a 1.0.    |
| Top-p          | `top_p` (0.0–1.0)        | `top_p` (0.0–1.0)       | `topP` (0.0–1.0)             | Misma semántica. Recomendación: usar uno u otro, no los dos a la vez. |
| Top-k          | `top_k` (entero)         | no soportado            | `topK` (entero)              | OpenAI no expone top-k.                                               |
| Tokens máximos | `max_tokens` (requerido) | `max_tokens` (opcional) | `maxOutputTokens` (opcional) | Anthropic exige `max_tokens` explícitamente.                          |
| Stop sequences | `stop_sequences` (lista) | `stop` (string o lista) | `stopSequences` (lista)      | Comportamiento equivalente.                                           |

## Parámetros de control determinista

| Parámetro                                  | Anthropic    | OpenAI          | Google                    | Notas                                              |
| ------------------------------------------ | ------------ | --------------- | ------------------------- | -------------------------------------------------- |
| Seed                                       | no soportado | `seed` (entero) | no soportado oficialmente | Solo OpenAI ofrece seed.                           |
| `system_fingerprint` para reproducibilidad | no           | sí (response)   | no                        | Indica si el modelo backend cambió entre llamadas. |

## Parámetros relacionados con tool use / function calling

| Parámetro                           | Anthropic                                      | OpenAI                                                           | Google                                            | Notas                                                            |
| ----------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| Definición de herramientas          | `tools`                                        | `tools`                                                          | `tools`                                           | Estructura JSON ligeramente distinta. Ver doc de cada proveedor. |
| Forzar uso de herramienta           | `tool_choice: {"type": "tool", "name": "..."}` | `tool_choice: {"type": "function", "function": {"name": "..."}}` | `tool_config.function_calling_config.mode: "ANY"` | Sintaxis distinta, semántica equivalente.                        |
| Forzar respuesta sin herramientas   | `tool_choice: {"type": "none"}`                | `tool_choice: "none"`                                            | `mode: "NONE"`                                    | —                                                                |
| Resultado de herramienta en mensaje | `tool_result` block                            | `role: "tool"` con `tool_call_id`                                | `function_response` part                          | Tres formatos distintos para lo mismo.                           |

## Parámetros de streaming

Podemos ver que los tres proveedores ofrecen streaming y que la activación se hace en parámetro distinto:

- Anthropic: `stream=True` en el método `messages.create`.
- OpenAI: `stream=True` en `chat.completions.create`.
- Google: usar el método `generate_content_stream` en lugar de `generate_content`.

## Tokens de razonamiento

| Proveedor | Parámetro                                           | Notas                                         |
| --------- | --------------------------------------------------- | --------------------------------------------- | ------- | ----------------------------------- |
| Anthropic | `thinking: {"type": "enabled", "budget_tokens": N}` | Disponible en modelos extended thinking.      |
| OpenAI    | `reasoning_effort: "low"                            | "medium"                                      | "high"` | Solo en modelos `o1` y posteriores. |
| Google    | no expuesto al usuario                              | Gemini gestiona el razonamiento internamente. |

## Notas de la migracion

Cuando migramos código de un proveedor a otro, los puntos de fricción más frecuentes son:

1. La estructura de mensajes con tool use (tres formatos distintos).
2. El parámetro `max_tokens` (obligatorio en Anthropic, opcional en los otros).
3. El rango de `temperature` (Anthropic limita a 1.0).
4. El manejo de mensajes del sistema (Anthropic los pasa como parámetro `system` separado; OpenAI y Google los meten en la lista de mensajes con `role: "system"`).

Si queremos construir un cliente que sea agnostico a cualquiera de estos modelos, conviene definir una capa interna que normalice estos puntos antes de delegar al SDK específico.
