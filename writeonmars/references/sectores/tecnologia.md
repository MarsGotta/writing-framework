# Sector: Tecnología

Base por defecto para guías técnicas de software. Es el sector más habitual y el
que mejor encaja con la voz y las referencias actuales del preset (`marcela-prose`,
`technical-guide-design`).

**Modelo de referencia**: `~/Projects/guide-ai-developers-basic/` — guía publicada
y validada con lectores. Los defaults de abajo están calibrados para que el
resultado base se le parezca. La voz (`marcela-prose`) ya está calibrada sobre su
guía hermana; este sector fija la **estructura** y el **léxico**.

## Alcance

Inteligencia artificial y agentes, desarrollo web y de software, datos,
infraestructura y DevOps, APIs y SDKs, herramientas de línea de comandos.
Lectores profesionales: desarrolladores, ingenieras, personas técnicas que ya
trabajan en el dominio.

## Tono por defecto

Experto, directo, natural y sobrio. Una persona que domina el tema explicando
con orden y criterio, sin entusiasmo de folleto ni solemnidad académica. Se
permite una metáfora sensorial puntual cuando aclara (no como adorno). Cierres
bajos, sin moraleja.

## Persona gramatical y registro

Plural inclusivo dominante ("vemos", "montamos", "lo que buscamos"), con tú
ocasional dirigido al lector cuando hay una acción concreta ("si lo ejecutas,
verás…"). Sin "usted". Sin humor forzado; la ironía editorial puntual entre
paréntesis es admisible si es seca.

## Anglicismos y extranjerismos admitidos

La **convención tipográfica manda y vive en `marcela-prose`** (§ "Cómo se
introducen anglicismos" + § Convenciones tipográficas): primera aparición en
cursiva con definición seca de una frase; siguientes en redonda. Código,
identificadores, comandos y nombres de archivo en backticks; también `harness` y
`MCP` van en backticks (son nombres de sistema/protocolo, no prosa).

Lista admitida por defecto en tech, sin traducir: `harness`, `MCP`, `skill`,
_prompt_, _system prompt_, _tool use_, _token_, _context window_, _endpoint_,
_framework_, _runtime_, _deploy_ / _deployment_, _commit_, _branch_, _merge_,
_diff_, _patch_, _spec_, _workflow_, _output_ / _input_, _sandbox_, _scope_,
_repo_, _backend_ / _frontend_, _stack_, _log_, _parser_, _wrapper_. Cada guía
amplía o recorta en sus adendas; lo admitido se justifica en el glosario
(Principio IV.4).

## Matices léxicos del sector

El Principio IV pide sustituir anglicismos innecesarios con ejemplos genéricos.
En tecnología varios de esos ejemplos **no aplican**, y la guía de referencia lo
confirma:

- `comando` es término legítimo del dominio: **no** se fuerza a "orden".
- `socket` se mantiene: **no** se traduce a "zócalo".
- **`librería`**: la comunidad de desarrollo y la guía de referencia usan
  "librería" (`la librería tiktoken`), aunque sea calco de _library_. Default del
  sector: **se admite "librería"** (invierte la sustitución del núcleo). Si una
  guía concreta prefiere el registro estricto, lo declara en sus adendas y vuelve
  a "biblioteca".
- `return` → **retorno**, `display` → **visualización** se mantienen fuera de
  bloques de código.
- `harness` **nunca** se traduce ("arnés" prohibido). `context window` es la forma
  canónica; "ventana de contexto" puede aparecer una vez como aclaración.

## Fuentes de autoridad esperadas

Documentación oficial del producto, SDK o lenguaje; especificaciones formales
(RFC, W3C/WHATWG, IETF, la especificación de MCP); changelogs y notas de versión
oficiales. Para la lengua: RAE y Fundéu. Blogs y foros valen como pista, no como
fuente primaria de una afirmación verificable.

## Datos volátiles típicos

Versiones de SDK, bibliotecas y runtimes; nombres de paquetes; flags y subcomandos
de CLI; precios y límites de APIs; rutas de configuración. Todo esto se marca como
verificable y se fecha la última comprobación (la pasada de precisión abre la
fuente en vivo). La guía de referencia añade una **nota de durabilidad** en el
README ("verificado al AAAA-MM-DD; estos datos envejecen rápido"): conviene
replicarla.

## Forma típica del ejemplo recurrente

Un sistema concreto y pequeño que se construye a lo largo de la guía: en la guía
de referencia, una API REST de gestión de tareas en Node/Express con tres
_endpoints_ y cuatro tests. El mismo caso atraviesa todos los capítulos desde un
ángulo distinto; no se inventan ejemplos nuevos cuando el recurrente ya cubre la
situación.

## Estructura de capítulo por defecto (modelo de la guía de referencia)

El capítulo NO usa la plantilla de cajas. Sigue este ritmo, que es el de la guía
de referencia:

1. **Apertura con escena** concreta del ejemplo recurrente (una traza, un número,
   una orden ejecutándose). Nada de tesis abstracta.
2. **Definición operativa** en cursiva, una frase, y se sigue.
3. **Por qué importa** — dos o tres razones prácticas enumeradas.
4. **Cómo funciona por dentro** — el mecanismo.
5. **Un caso concreto** con el ejemplo recurrente (tabla, traza de iteraciones o
   código).
6. **Error frecuente** / **dónde se escapa** — la trampa típica.
7. **(Opcional) qué hacer en la práctica** — solo si el capítulo tiene acción
   accionable real (p. ej. "cómo gastar menos"). No se fuerza en todos.
8. **Puente al siguiente** capítulo (cierre bajo).
9. **`## Fuentes`** — al final de **cada** capítulo, con nombre, enlace y fecha.

**Mini-ejercicio opcional** al cierre de algunos capítulos (en la guía de
referencia, en los de MCP, skills y SDD).

## Relajaciones estructurales por defecto

Respecto a los Estándares editoriales del núcleo, en tech por defecto:

- **Sin cajas decorativas obligatorias** ("Quédate con esto", "Qué hacer mañana",
  "Síntoma → causa probable"). La guía de referencia no usa ninguna. Si una guía
  las quiere, las activa en sus adendas.
- **Checklist centralizado**, no por capítulo: vive en el capítulo de cierre y en
  los anexos (plantillas reutilizables). Cada capítulo cierra en puente + Fuentes,
  no en checklist.
- La sección "Qué hacer en la práctica" es **opcional** por capítulo (ver punto 7
  de la estructura), no obligatoria.

(Estas relajaciones aplican a tech porque la guía de referencia lo valida. Otros
sectores —médico, veterinario— pueden querer las cajas "Síntoma → causa probable";
ese es el sentido de que sean defaults por sector, no del núcleo.)

## Convenciones de citación

Contrato de citación del preset (modo BYOM). Cada afirmación verificable apunta a
una fuente oficial fechada. Los datos volátiles llevan fecha de comprobación.
Además, **`## Fuentes` por capítulo** (no solo un research.md central): replica la
trazabilidad de la guía de referencia.
