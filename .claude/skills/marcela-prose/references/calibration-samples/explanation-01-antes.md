# Por qué el orden del contexto importa más que el tamaño

> Modalidad: explanation. Objetivo: argumentar que en harness engineering la decisión de qué meter al principio del contexto y qué meter al final es más determinante que el tamaño total disponible.

Cuando un equipo empieza a trabajar con agentes, la primera reacción ante un comportamiento inconsistente del modelo suele ser pedir más context window. Es la lectura intuitiva: si el modelo se confunde, debe ser porque no le cabe lo que necesita. Pero los datos disponibles sobre cómo los modelos atienden a la información del prompt sugieren que esta lectura es incompleta. El tamaño importa, sí, pero el orden importa más.

Los modelos actuales muestran un patrón conocido como atención no uniforme a lo largo del prompt. La información colocada al principio (el llamado lost-in-the-middle es exactamente lo opuesto) y al final tiene más probabilidad de ser recuperada con precisión que la información colocada en el medio. Esto significa que un prompt de 100k tokens donde la instrucción crítica está en la posición 50k puede comportarse peor que un prompt de 30k tokens donde la misma instrucción está en la posición inicial.

La consecuencia práctica es que el diseño del orden del contexto se convierte en una decisión de arquitectura, no en una decisión de relleno. Tres principios operativos derivan de esta observación.

Primero, las instrucciones de sistema y las restricciones duras van al principio. Aunque la mayoría de SDKs tienen un parámetro `system` específico, hay implementaciones donde acaba mezclado con el resto del historial. Cuando esto pasa, las instrucciones se diluyen y el agente las olvida. Conviene verificar dónde acaba realmente el `system` en cada proveedor.

Segundo, lo más reciente y lo más crítico va al final. Los últimos tokens son los que el modelo "tiene presentes" cuando empieza a generar la respuesta. Si el agente está en mitad de una conversación larga y la siguiente decisión depende de un dato que apareció veinte turnos atrás, ese dato debe re-aparecer en los turnos recientes (vía resumen, vía tool result, vía mensaje de sistema sintético) o el modelo lo tratará como información lejana.

Tercero, el medio del prompt es el sitio donde van los detalles que el modelo solo necesita "ver" para construir contexto general, pero que no son críticos para la decisión inmediata. Documentación de fondo, ejemplos de pocos-shot que ilustran el formato esperado, snippets de código que solo se citan ocasionalmente.

La derivada interesante de esta forma de pensar es que harness engineering deja de ser una práctica de "cuánto le doy" y se convierte en una práctica de "en qué orden". Y eso, a diferencia del tamaño del context window, no depende del proveedor ni del modelo: depende de cómo el equipo organiza la información que el agente recibe en cada turno. Un equipo que entiende esto saca el doble de partido a un context window de 32k que el que no lo entiende a uno de 200k.

Lo que cambia, en definitiva, es la pregunta. Deja de ser "¿cuánto contexto necesito?" y pasa a ser "¿qué pongo dónde?". La segunda pregunta es la que define el oficio.
