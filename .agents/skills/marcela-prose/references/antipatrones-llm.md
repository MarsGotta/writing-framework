# Antipatrones LLM en prosa española técnica — subset operativo

Este documento es el subset de patrones LLM relevantes para prosa española técnica de Marcela. Selección y adaptación de los patrones universales de `humanizer`, filtrados por relevancia y traducidos a contexto español + dominio técnico.

<!-- Origen: humanizer §1-29 (Wikipedia "Signs of AI writing") + observación directa en pasadas LLM sobre material español -->

---

## Por qué este documento existe

Los patrones de `humanizer` son universales pero están en inglés y enfocados a Wikipedia. Esta selección hace tres cosas:

1. **Filtra**: solo los patrones que aparecen en prosa técnica española.
2. **Traduce**: ejemplos en español, no en inglés.
3. **Prioriza**: los marcados como "alta frecuencia" aparecen en casi todo borrador LLM; los "ocasionales" solo en algunos.

---

## Alta frecuencia (revisión obligatoria en cada pase)

### LLM-1. Significance inflation (significancia inflada)

Patrón: anunciar que algo es importante / clave / pivotal sin mostrar por qué.

**Antes:** *El testing automatizado representa un pivote crucial en la madurez del equipo de desarrollo, marcando un momento decisivo en la evolución del oficio.*
**Después:** *El testing automatizado reduce el tiempo de regresión de tres días a cuatro horas. Eso es lo que cambia.*
**Diagnóstico:** "pivotal", "crucial", "decisivo", "marca un momento" sin métrica. Sustituye por efecto concreto.

### LLM-2. Promotional language (lenguaje promocional)

Patrón: prosa que suena a folleto de producto.

**Antes:** *Una solución potente, elegante y de vanguardia que transforma la forma en que trabajas.*
**Después:** *Arranca en un segundo, soporta ESM nativo y se integra con Vite sin configuración.*
**Diagnóstico:** adjetivos promocionales sin métrica. Sustituye por hecho.

### LLM-3. Vague attributions (atribuciones vagas)

Patrón: "expertos dicen", "estudios indican", sin nombre.

**Antes:** *Expertos del sector señalan que esta práctica está ganando terreno.*
**Después:** *Birgitta Böckeler, en su post de marzo de 2026 sobre harness engineering, argumenta que esta práctica define el siguiente nivel de madurez.*
**Diagnóstico:** atribución vaga = inventado. Nombre + fecha + enlace, o quítalo.

### LLM-4. -ing endings (gerundios decorativos al cierre)

Patrón: gerundio al final que añade pseudo-profundidad.

**Antes:** *El modelo procesa el contexto, optimizando los recursos disponibles, garantizando una respuesta coherente.*
**Después:** *El modelo procesa el contexto. Si está bien ordenado, la respuesta es coherente; si no, divaga.*
**Diagnóstico:** dos gerundios en cierre = firma LLM. Cero tolerancia. Sustituye por oración nueva con conector.

### LLM-5. Em dash overuse

Patrón: rayas en cadena para énfasis.

**Antes:** *Vitest —rápido, ESM nativo— es la opción —moderna y consolidada— para proyectos actuales.*
**Después:** *Vitest es rápido, funciona con ESM nativo y ya es la opción estándar en proyectos actuales.*
**Diagnóstico:** máximo una raya por párrafo. Idealmente cero.

### LLM-6. Rule of three (regla de tres decorativa)

Patrón: tres elementos para parecer comprehensivo.

**Antes:** *Una solución rápida, clara y eficaz.*
**Después:** *Una solución rápida y clara.*
**Diagnóstico:** si los tres elementos son sinónimos o vagos, pasa a dos. Si describen tres cosas distintas y concretas, mantén o pasa a cuatro.

### LLM-7. Negative parallelism ("no es X, es Y" en cadena)

Patrón: paralelismo negativo repetido. Perfume LLM más reconocible.

**Antes:** *No es un framework, es una filosofía. No es una herramienta, es un movimiento.*
**Después:** *Vitest es un framework de testing. Lo que cambia respecto a Jest es la integración con Vite.*
**Diagnóstico:** cero tolerancia en cadena. Como mucho, una vez por capítulo, y solo si hay contraste real.

### LLM-8. Copula avoidance (evitar `ser`/`estar`)

Patrón: sustituir `ser` por verbos elaborados.

**Antes:** *Vitest se erige como la opción estándar para testing en proyectos modernos.*
**Después:** *Vitest es la opción estándar.*
**Diagnóstico:** "se erige", "emerge", "constituye", "representa", "sirve como". Vuelve al `ser`.

### LLM-9. Signposting / let's dive in

Patrón: anunciar lo que vas a hacer en vez de hacerlo.

**Antes:** *A continuación vamos a profundizar en cómo funciona el agent loop. Primero veremos…*
**Después:** *El agent loop tiene cuatro fases: percibir, decidir, actuar, observar.*
**Diagnóstico:** "vamos a explorar", "let's dive in", "sin más preámbulos", "a continuación analizaremos". Quita y entra directo.

### LLM-10. Filler phrases / hedging (relleno y atenuación)

Patrón: relleno burocrático.

**Antes:** *Es importante destacar que vale la pena mencionar que cabe señalar que el modelo soporta function calling.*
**Después:** *El modelo soporta function calling.*
**Diagnóstico:** "es importante destacar", "cabe mencionar", "vale la pena", "como bien sabemos". Quita.

---

## Frecuencia media (revisión recomendada)

### LLM-11. Persuasive authority tropes ("at its core", "the real question is")

**Antes:** *La verdadera pregunta es si los equipos pueden adaptarse. En el fondo, lo que realmente importa es la disposición organizacional.*
**Después:** *La pregunta es si los equipos pueden adaptarse. Eso depende de si la organización está dispuesta a cambiar sus hábitos.*
**Diagnóstico:** "la verdadera pregunta es", "en el fondo", "lo que realmente importa", "fundamentalmente". Pretenden cortar al grano y solo añaden ceremonia.

### LLM-12. Generic positive conclusions

**Antes:** *El futuro es prometedor. Vienen tiempos emocionantes mientras continuamos este camino hacia la excelencia.*
**Después:** *El equipo abre dos sucursales en Q3 y duplica plantilla en Q4.* (o cierre concreto)
**Diagnóstico:** "el futuro es prometedor", "vienen tiempos emocionantes", "esto es solo el comienzo". Sustituye por hecho concreto o por bisagra al siguiente bloque.

### LLM-13. Outline-like challenges sections

**Antes:** *## Retos y perspectivas futuras*
> *A pesar de su éxito, el sistema enfrenta varios retos típicos. A pesar de estos retos, sigue creciendo gracias a su ubicación estratégica.*

**Después:** *## Limitaciones conocidas*
> *El throughput cae por debajo de 100 req/s cuando el cache miss rate supera el 30 %. El equipo de SRE empezó la migración a Redis 7 en marzo de 2026 para corregirlo.*

**Diagnóstico:** "A pesar de... a pesar de...". Sustituye por limitaciones concretas con plan o sin plan, pero específicas.

### LLM-14. Boldface mechanically applied

**Antes:** *El **agent loop** consiste en cuatro fases: **percibir**, **decidir**, **actuar** y **observar**. Cada **fase** tiene su propia **lógica** y sus propios **componentes**.*
**Después:** *El **agent loop** tiene cuatro fases: percibir, decidir, actuar, observar. Cada fase tiene componentes propios.*
**Diagnóstico:** una negrita por párrafo, en la primera aparición del término canónico. El resto en redonda.

### LLM-15. Inline-header vertical lists

**Antes:**
> - **Velocidad:** Es rápido.
> - **Calidad:** Es de calidad.
> - **Adopción:** Tiene adopción.

**Después:** Prosa con datos concretos, o tabla si los elementos son comparables.

**Diagnóstico:** este formato es firma LLM. Si los elementos son tres y de una línea cada uno, pasa a prosa.

### LLM-16. Title case en titulares

**Antes:** *## Cómo Diseñar Un Harness Para Producción*
**Después:** *## Cómo diseñar un harness para producción*
**Diagnóstico:** sentence case en español.

### LLM-17. Curly quotes

**Antes:** *Dijo que "esto va bien".* (curvas)
**Después:** *Dijo que "esto va bien".* (rectas) o *Dijo que «esto va bien».* (latinas)
**Diagnóstico:** las curvas son ChatGPT. Convención del documento: rectas o latinas.

---

## Frecuencia baja (revisión ocasional)

### LLM-18. Knowledge-cutoff disclaimers

**Antes:** *Hasta donde alcanza la información disponible, el modelo soporta hasta 200k tokens.*
**Después:** *El modelo soporta 200k tokens (Anthropic, marzo 2026).*
**Diagnóstico:** "hasta donde alcanza la información disponible", "según los datos disponibles", "como información de mi última actualización". Quita y trae fecha + fuente.

### LLM-19. Sycophantic / servile tone

**Antes:** *¡Excelente pregunta! Estás absolutamente en lo cierto al preguntar esto.*
**Después:** (eliminar el meta-comentario, ir al contenido)
**Diagnóstico:** texto pensado como respuesta de chat pegado como contenido. Quita.

### LLM-20. Collaborative communication artifacts

**Antes:** *Aquí tienes una visión general de Vitest. ¡Espero que te ayude! Avísame si necesitas que profundice en algún tema.*
**Después:** (eliminar el cierre de chat, ir al siguiente bloque)
**Diagnóstico:** otro caso de output de chat pegado como contenido.

### LLM-21. False ranges ("from X to Y")

**Antes:** *Recorremos el viaje desde la concepción del modelo hasta su despliegue en producción, desde el primer prompt hasta la última métrica.*
**Después:** *El capítulo cubre tres fases: diseño del modelo, integración con el harness y métricas de producción.*
**Diagnóstico:** "desde X hasta Y" cuando X e Y no están en una escala real es decoración. Sustituye por enumeración concreta.

### LLM-22. Hyphenated word pair overuse

**Antes:** *Un equipo cross-funcional desarrolló un informe data-driven sobre nuestras herramientas client-facing.*
**Después:** *Un equipo de tres roles —diseño, datos y plataforma— hizo un informe basado en métricas sobre las herramientas que usan los clientes.*
**Diagnóstico:** los compuestos hyphenated en cadena son anglicismos pegados sin digerir. Reescribe a giro español.

---

## Mapa de ataque

Cuando heredas un texto con sospecha de prosa LLM, ataca por orden:

1. Em dash en cadena (LLM-5).
2. Paralelismo negativo (LLM-7).
3. Gerundios al cierre de frase (LLM-4).
4. Significance inflation (LLM-1) y promotional (LLM-2).
5. Vague attributions (LLM-3).
6. Copula avoidance (LLM-8).
7. Filler / hedging / signposting (LLM-9, LLM-10).
8. Inline-header vertical lists (LLM-15).
9. Negrita mecánica (LLM-14).
10. Lo demás según aparezca.

Si después del paso 5 el texto sigue oliendo a LLM, es voz: falta la pasada de `marcela-prose` completa, no solo la limpieza.
