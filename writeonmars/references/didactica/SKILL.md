---
name: technical-guide-design
description: >
  Diseña, revisa, reestructura o microedita guías técnicas, manuales,
  tutoriales, talleres y playbooks de ingeniería para desarrolladores
  profesionales. Combina enseñanza basada en evidencia (Diátaxis,
  andragogía, teoría de la carga cognitiva, worked examples) con el
  catálogo de microestilo de prosa. Trigger para trabajo estructural:
  "diseña una guía", "revisa este temario", "mejora el material de este
  taller", "estructura este tutorial", "cómo enseñar X", "crea un
  workshop sobre Y". Trigger para microedición: "haz que suene menos
  robótica", "frases comprimidas", "hazlo más natural", "mejora la
  prosa de la guía", "limpia el tono plano", "frases inconexas", "tono
  de eslogan". También al evaluar docs o guías existentes por eficacia
  didáctica o utilidad operativa.
user-invocable: true
---

# Technical Guide Design (diseño de guías técnicas)

Playbook basado en evidencia para diseñar, revisar y reestructurar material
técnico de aprendizaje dirigido a **desarrolladores profesionales** (no
estudiantes universitarios, no principiantes absolutos). Sintetiza Diátaxis,
andragogía (Knowles), teoría de la carga cognitiva (Sweller), worked examples
(Renkl y Atkinson) y guías de estilo de documentación (Google, Write the
Docs).

La skill cubre dos capas, en este orden de impacto:

1. **Estructural**: modalidades, carga cognitiva, ejercicios, organización de
   archivos. Es la mayor parte de este documento.
2. **Microestilo**: los defectos de prosa que hacen que una guía
   estructuralmente sólida suene mecánica o robótica. Catálogo con ejemplos
   antes/después en `./references/prose-pitfalls.md`.

Una guía que falla en estructura no se salva con buena prosa; una guía con
la estructura bien resuelta seguirá sonando artificial si se ignoran las
reglas de prosa.

Usa esta skill cuando:

- Creas una guía, tutorial, taller o conjunto de documentación técnica nuevo.
- Revisas material existente por solidez pedagógica.
- Reestructuras un documento de modalidades mezcladas que se ha vuelto
  difícil de navegar.
- Diseñas el complemento entre una sesión en vivo y material escrito
  asíncrono.
- Editas prosa de una guía estructuralmente sólida que se lee comprimida,
  robótica o de plantilla (salta directamente a
  `./references/prose-pitfalls.md`).

## Principio central: separar modalidades (Diátaxis)

Cada pieza de contenido técnico de aprendizaje sirve a **un propósito
dominante**. Mezclar modalidades a partes iguales en el mismo documento es la
causa número uno de las guías flojas.

| Modalidad | Orientación | Estado del lector | Ejemplo |
|---|---|---|---|
| **Tutorial** | Aprender haciendo | "Soy nuevo, llévame de la mano" | Tu primer test con Vitest |
| **How-to** | Orientado a tarea | "Tengo el problema X, cómo lo resuelvo" | Cómo mockear un servicio HTTP |
| **Reference** | Consulta de información | "Cuál es la sintaxis exacta de X" | Tabla de equivalencias Jasmine → Vitest |
| **Explanation** | Comprensión | "Por qué X funciona así" | Por qué mutation testing y no cobertura |

Debajo hay dos ejes ortogonales:

- **Práctica (acción) ↔ Teoría (cognición)**
- **Adquisición (aprender) ↔ Aplicación (trabajar)**

**Regla.** Etiqueta cada archivo o sección con **una modalidad dominante** en
su front-matter. Ante la mezcla, partir es el default.

**Híbrido permitido.** Una modalidad dominante puede alojar una
**micro-sección de otra modalidad** al cierre del archivo cuando sirve
directamente a la dominante. Caso típico: un capítulo de *explanation* sobre
un concepto que cierra con un bloque pequeño de *reference* ("dónde implementa
esto cada herramienta") para que el lector no salga de contexto a buscar el
detalle operativo. Marca la micro-sección visualmente (H2 propio, tabla o
callout) para que se pueda escanear o saltar.

Lo que sigue sin funcionar: la mezcla a partes iguales (un tutorial montado a
medias como tabla de referencia). Si el archivo hace dos modalidades a partes
iguales, parte en dos.

## Principios pedagógicos para devs adultos (andragogía)

Los desarrolladores profesionales son aprendices adultos:

1. **Necesitan el porqué** antes del qué: abre cada sección con el dolor o el
   problema, no con teoría.
2. **Valoran la autonomía**: ofrece rutas ("camino rápido" y "a fondo"),
   nunca un único orden forzado.
3. **Traen experiencia previa**: apóyate en lo que ya saben ("si vienes de
   Jest, `vi.fn` te resultará familiar").
4. **Piensan en problemas, no en temarios**: organiza por "cómo testeo un
   formulario asíncrono", no por "capítulo 3: matchers".
5. **Tienen motivación interna**: conecta con KPIs reales (menos bugs en
   producción, PRs más rápidas, menos flakiness).
6. **Aprenden just-in-time, no just-in-case**: el contenido llega cuando lo
   van a aplicar esta semana.
7. **Agradecen las señales de orientación**: indicaciones explícitas como
   "quédate con esta idea", "no necesitas memorizar X", "el síntoma típico es
   Y", "si solo lees una sección, lee esta" bajan la carga cognitiva sin
   resultar condescendientes. Úsalas al cierre de párrafos densos.

**Nunca** con profesionales: tono paternalista, "qué es una función",
soluciones bloqueadas "para que piensen", ánimo con emojis, explicar la
terminal.

## Carga cognitiva: las tres cargas

- **Intrínseca**: complejidad inherente al tema. Irreducible; solo se
  secuencia.
- **Extrínseca**: fricción añadida por malas decisiones de diseño. Minimízala
  con agresividad.
- **Pertinente**: el esfuerzo útil de construir esquemas mentales. Maximízala
  con worked examples y fading.

Efectos que conviene conocer:

- **Worked example effect** (Sweller y Cooper, 1985): estudiar un ejemplo
  totalmente resuelto es más eficiente que resolver desde cero, para novatos.
- **Expertise reversal effect** (Kalyuga, 2003): los MISMOS worked examples
  confunden a los expertos. Ofrece "si ya sabes X, salta al reto Y".
- **Backward fading** (Renkl y Atkinson, 2003): paso 1 completo → paso 2
  parcial → paso 3 en blanco. Andamiaje gradual.

## Diseño de ejemplos de código

Reglas para todo fragmento de código:

1. **MVCE** (ejemplo mínimo viable): ejecutable, completo, representativo,
   sin nada de más.
2. **Autocontenido**: imports visibles (o declarados una vez como convención
   del capítulo). El lector no debería inferir más de 3 líneas.
3. **Revelado progresivo**: el primer fragmento, trivial; añade capas de una
   en una. Nunca abras con el "final realista".
4. **Un solo dominio en toda la guía** (p. ej. "CartApp"): reutilizar el
   dominio reduce carga.
5. **Nombres reales frente a placeholders**: `user/cart/order` al mostrar
   patrones aplicados; `foo/bar` solo para sintaxis pura.
6. **Longitud**: 5 a 15 líneas ideal, 30 como máximo. Más largo: parte o
   enlaza a un repo ejecutable.
7. **Explícito antes que ingenioso**: `const r = add(2,3);
   expect(r).toBe(5);` gana a `expect(add(2,3)).toBe(5)` en primera
   aparición.
8. **Contigüidad**: la explicación pegada al código, no después. Los
   comentarios inline `// ← esta es la línea clave` ganan a los párrafos.
9. **Versionado**: encabeza cada capítulo con versiones del stack y fecha de
   validación ("Validado 2026-04 con Vitest 4.x").
10. **Sin fallos de compilación**: incluye todos los imports. Valida los
    fragmentos en CI si es posible.

### Patrón antes/después

Úsalo al mostrar anti-patterns comunes en la audiencia:

- Marca lo malo con señales visuales: `// ❌ frágil` / `// ✅ resiliente`.
- Nunca dejes un anti-pattern en una página sin su corrección.
- Riesgo: efecto de familiaridad (el lector memoriza la versión mala).
  Mitiga con distinción visual.

## Durabilidad: principios estables frente a datos versionados

Las guías técnicas envejecen. Los precios cambian, las versiones de modelo se
mueven, las listas de comandos se reescriben entre releases. El cuerpo de la
guía debería sobrevivir a la mayoría de esos cambios; los datos fechados se
ponen en cuarentena para poder actualizarlos sin reescribir la prosa.

**Regla.** Separa principios estables de datos versionados.

- **Cuerpo de la guía.** Principios que cambian despacio (la asimetría de
  coste input/output, la atención no uniforme, memoria ≠ contexto). Es lo que
  el lector debería recordar dentro de unos años.
- **Datos versionados.** Precios concretos, números de versión, nombres
  exactos de comandos, fechas de lanzamiento de features. Viven en:
  - **Callouts inline** con fecha de verificación: `> Verificado el
    2026-05-06. Confirmar contra docs antes de publicar.`
  - **Un bloque "Fuentes" o "Datos versionados" al final de cada capítulo**,
    para que quien revise en el futuro actualice un bloque en vez de rastrear
    la prosa.
  - **Un anexo** para tablas de comandos y referencias rápidas.

El coste de confundir ambos: una guía con precios concretos en cada párrafo
se lee como un informe temporal, no como un manual. Una guía sin ningún dato
concreto se lee vaga. La disciplina: principios dentro, datos fechados y
señalizados.

## Plantilla de estructura de guía

Aplícala a cada archivo mayor:

1. **Título + propósito en una línea** (para quién es, qué sabrá hacer
   después).
2. **Prerrequisitos** (enlaces a material previo o recursos externos).
3. **Estimación de tiempo**.
4. **Contexto / motivación**: por qué importa (el dolor sin este
   conocimiento).
5. **Cuerpo**: secciones pequeñas, cada una con explicación → ejemplo →
   micro-ejercicio o pregunta de autochequeo.
6. **Síntesis**: ver "Tácticas de síntesis" abajo; elige un formato concreto,
   no un párrafo-resumen vago.
7. **Ejercicio de consolidación**: problema aplicado, más abierto.
8. **Referencias**: enlaces de profundización, docs oficiales.

### Opcional de alto impacto: anexo de plantillas reutilizables

Para guías dirigidas a equipos que van a *operar* con el material (no solo
leerlo), añade un anexo final que reúna las plantillas que el cuerpo mostró
por piezas:

- Esqueletos de `AGENTS.md` / `CLAUDE.md` / configuración.
- Plantilla de *spec*.
- *Prompts* operativos listos para copiar.
- *Checklists* de revisión (PR, auditoría, despliegue).
- Tablas de decisión.

El anexo es la pieza más reutilizada de una guía operativa. El cuerpo explica
el porqué; el anexo da lo que el equipo pegará en su repo el lunes.

Estructura consistente entre archivos = previsibilidad = menos carga
cognitiva. Combínala con **redacción variada** en títulos y encabezados (ver
prose-pitfalls, entrada 7) para que el esqueleto previsible no produzca piel
de plantilla.

## Tácticas de síntesis

El punto 6 de la plantilla ("síntesis") se ejecuta demasiado a menudo como
párrafo-resumen genérico. Elige en su lugar uno de estos formatos, en este
orden de utilidad para devs adultos:

- **Tabla de decisión.** "Síntoma → causa probable → capítulo donde se
  trata". La pieza más reutilizada de una guía operativa.
- **Tabla comparativa.** Opción A frente a B frente a C, con columnas "cuándo
  usar", "cuándo no", "qué cuesta". Gana a la comparación discursiva.
- **Checklist operativa.** De 5 a 9 ítems. Para "antes de mergear una PR",
  "antes de desplegar", "antes de publicar".
- **Formulario de autoevaluación.** Preguntas cortas que el lector responde;
  revela huecos en su propia comprensión.

Un "párrafo de resumen" rara vez se gana el sitio. Si la síntesis puede
expresarse como tabla o checklist, debería serlo.

## Combinar sesión en vivo y material asíncrono

Cuando el material acompaña a una sesión en vivo:

- **Sesión en vivo**: motivación, debate, preguntas colectivas, energía
  compartida. Lo mejor en vivo: *tutorial* y *explanation*.
- **Guía asíncrona**: profundidad, ritmo propio, relectura, consulta
  just-in-time. Lo mejor por escrito: *how-to* y *reference*.
- **Regla**: la guía asíncrona debe ser *autosuficiente* (quien faltó a la
  sesión puede seguirla) Y *complementaria* (añade lo que el directo no da:
  profundidad, casos límite, tablas de referencia).
- La sesión en vivo señala explícitamente los archivos asíncronos: "cuando te
  encuentres el caso X, ve al archivo Y".

## Voz y estilo de prosa

**Esta skill es dueña de la estructura, no de la prosa.** En el pipeline
writeonmars las reglas de prosa viven en la pirámide de prosa y se cargan por
separado; no las reapliques desde aquí o el texto tendrá tres jefes:

- **Capa 1, cohesión y fluidez**: `../prosa/SKILL.md` (`prosa-base`): frases
  completas, progresión conocido → nuevo, eco entre párrafos, transiciones
  con porqué, ritmo de crucero.
- **Capa 2, registro del género**: `../registros/<slug>/SKILL.md` (para
  guías técnicas: `tecnico-divulgativo`): formalidad, densidad, presupuesto
  de figuras, aserción con alcance, persona del género.
- **Capa 3, voz del autor**: `../voz/SKILL.md` (`marcela-prose`): léxico,
  humor, aperturas, cierres, limpieza de patrones LLM.

**Regla central que esta skill conserva** (es estructural, constitución
§ II): cada párrafo que explica algo sigue **situación → explicación →
consecuencia práctica**. Una línea comprimida que funde los tres pasos se lee
como nota interna, no como guía.

**Reglas de estilo de nivel estructural que se quedan aquí:**

- [ ] Títulos de tarea con verbo ("Configura Jest", no "Configuración de
  Jest").
- [ ] Pasos numerados cuando el orden importa; viñetas cuando no.
- [ ] Los encabezados forman un esquema escaneable.
- [ ] Estructura previsible entre archivos; **redacción variada** en títulos
  y encabezados (que la estructura no se vuelva plantilla).
- [ ] Terminología consistente: un concepto = un término, siempre. Mantén
  glosario. (El registro y el sector fijan la cadencia de definición y los
  anglicismos admitidos.)

**Catálogo concreto de defectos de prosa** con ejemplos y reglas de
reescritura: `./references/prose-pitfalls.md`. Sigue siendo la fuente
histórica de varias reglas de la pirámide (prosa-base lo acredita); al editar
prosa dentro del pipeline, usa las capas de la pirámide.

## Checklist de revisión

Al revisar una guía existente, comprueba en cada archivo:

**Estructura**

- [ ] Tiene una modalidad dominante declarada (tutorial / how-to / reference
  / explanation).
- [ ] No mezcla modalidades a partes iguales; micro-secciones de otra
  modalidad solo al cierre, marcadas.
- [ ] Abre con el porqué importa, no con teoría.
- [ ] Tiene objetivos de aprendizaje explícitos arriba.
- [ ] Tiene tiempo estimado.

**Carga cognitiva**

- [ ] Ninguna sección introduce más de un concepto nuevo.
- [ ] Los ejemplos usan un dominio consistente entre archivos.
- [ ] Los fragmentos de código son autocontenidos (imports visibles).
- [ ] El andamiaje se desvanece a lo largo de los ejercicios.
- [ ] Hay worked examples antes de los ejercicios autónomos.
- [ ] Señales de orientación al cierre de párrafos densos.

**Respeto al aprendiz adulto**

- [ ] El tono es de par a par, no parental.
- [ ] Se apoya en la experiencia previa del lector.
- [ ] Ofrece rutas alternativas (rápida / a fondo).
- [ ] Las soluciones están disponibles (no bloqueadas "para que piensen").
- [ ] Los ejercicios se atan a tareas reales, no a problemas de juguete.

**Ejemplos de código**

- [ ] Mínimos viables, ejecutables, autocontenidos.
- [ ] Un solo dominio en toda la guía.
- [ ] Nombres reales salvo contexto de sintaxis pura.
- [ ] ≤ 30 líneas por fragmento.
- [ ] Anotaciones inline antes que párrafos.
- [ ] Versiones + fecha de validación en el encabezado.
- [ ] Anti-patterns marcados visualmente y seguidos de su corrección.

**Durabilidad**

- [ ] El cuerpo habla en principios estables.
- [ ] Los datos fechados (precios, versiones, comandos) viven en callouts,
  bloque de fuentes o anexo.
- [ ] Cada bloque versionado tiene fecha de verificación.

**Síntesis**

- [ ] La sección de síntesis usa un formato concreto (tabla de decisión,
  comparativa, checklist, autoevaluación), no un resumen genérico.
- [ ] Si la guía es operativa, existe el anexo de plantillas reutilizables.

**Microestilo (nivel prosa)**

Pasa el catálogo (`./references/prose-pitfalls.md`) en el orden recomendado
al final de ese archivo. Chequeo rápido:

- [ ] Sin pronombres vagos sin referente claro.
- [ ] Sin frases que mezclen más de dos ideas.
- [ ] Como mucho una frase aforística por capítulo.
- [ ] Los títulos de sección varían a lo largo de la guía (no cinco capítulos
  con la misma sección de cierre).
- [ ] Las entradas al ejemplo recurrente varían (no cinco capítulos abriendo
  con "Volvamos a…").
- [ ] Las transiciones explican el porqué-ahora, no solo "vamos a verlo".
- [ ] Sin metáforas mezcladas.
- [ ] Anglicismos solo donde son canónicos.

**Navegación**

- [ ] Estructura consistente entre archivos.
- [ ] Cada archivo enlaza a los relacionados (tutorial → how-to para
  avanzado, how-to → reference para detalle).
- [ ] El índice enruta por intención del lector ("quiero aprender" / "quiero
  resolver X" / "quiero consultar").
- [ ] Nada importante se encuentra solo buscando.

## Anti-patterns comunes a señalar

### Estructurales

1. **Modalidades mezcladas**: tutorial con tabla de referencia exhaustiva
   incrustada como socio a partes iguales.
2. **Teoría antes del dolor**: 3 párrafos definiendo términos antes de
   cualquier código o ejemplo.
3. **Muro de texto**: párrafos de más de 5 líneas, sin H2/H3, sin callouts.
4. **Ejemplos Frankenstein**: un test de `User` que de repente renderiza
   `<ProductList>`.
5. **Terminología inconsistente**: "test", "spec", "caso" usados como
   sinónimos.
6. **Fragmentos rotos**: imports que faltan, tipos incorrectos.
7. **Versiones desactualizadas sin marcar**: sin encabezado de versión de
   stack, sin fecha de validación.
8. **Soluciones bloqueadas**: ejercicios sin respuesta accesible (hostil con
   profesionales).
9. **Tono condescendiente**: "Aprendamos juntos qué es una función".
10. **Referencias cruzadas sin enlace**: "como vimos antes" sin link.
11. **Datos fechados en la prosa del cuerpo**: precios, versiones y comandos
    exactos espolvoreados inline en vez de en callouts o anexo.
12. **Párrafos de resumen genéricos**: secciones de síntesis que podrían ser
    una tabla de decisión y son prosa.

### De nivel prosa

Catálogo con ejemplos en `./references/prose-pitfalls.md`. Titulares:

13. **Frases comprimidas**: concepto + metáfora + conclusión en una línea.
14. **Pronombres vagos**: `lo / eso / esto` sin referente claro.
15. **Cadenas de aforismos**: "no es X: es Y" repetido sección tras sección.
16. **Metáforas mezcladas**: imágenes incompatibles apiladas.
17. **Anglicismos innecesarios**: `mental model`, `scope`, `baseline`,
    `inline` donde el español se lee más limpio.
18. **Transiciones secas**: "Vamos a verlo", "Quedan tres categorías" sin
    porqué-ahora.
19. **Títulos recurrentes mecánicos**: "La trampa común…" cinco capítulos
    seguidos; "Volvamos al…" como única entrada al ejemplo recurrente.
20. **Afirmaciones absolutas**: enunciados de sonido universal que un lector
    senior puede pinchar.

## Proceso para diseñar una guía nueva

1. **Define resultados de aprendizaje** con verbos de Bloom: "Al terminar
   sabrás [aplicar/configurar/migrar/evaluar] X".
2. **Identifica el estado de la audiencia**: qué sabe ya, su stack, su dolor
   diario.
3. **Elige modalidades**: normalmente tutorial + how-to + reference +
   explanation, cada una en archivo propio. Una dominante por archivo.
4. **Elige un único dominio** para todos los ejemplos.
5. **Esquema por archivo**: título, propósito, prerrequisitos, tiempo,
   secciones.
6. **Decide el formato de síntesis por archivo** (tabla de decisión /
   comparativa / checklist / autoevaluación) antes de escribir.
7. **Planifica el anexo** si la guía es operativa: qué plantillas copiará el
   equipo.
8. **Diseña ejercicios con fading**: guiado → semi-guiado → autónomo.
9. **Escribe un archivo de punta a punta primero** para calibrar tono y
   profundidad.
10. **Pasada de microestilo** con `./references/prose-pitfalls.md` antes de
    pilotar.
11. **Pilota con 2 o 3 usuarios reales** y recoge puntos de fricción (tiempo
    frente a estimación, dudas repetidas, errores frecuentes).
12. **Itera incrementalmente**, no reescribas.

## Proceso para revisar material existente

1. Mapea cada archivo a una modalidad dominante. Señala los que mezclan a
   partes iguales.
2. Revisa el índice: ¿enruta por intención del lector? ¿Ofrece rutas rápida y
   a fondo?
3. Revisa durabilidad: ¿datos fechados en el cuerpo o en callouts/anexo?
4. Pasa la checklist estructural en cada archivo.
5. Pasa el catálogo de prose-pitfalls en cada archivo, en el orden del final
   de ese documento. Pasadas de una sola regla, no "humanizar todo a la vez".
6. Puntúa: ¿cuántos principios satisface cada archivo?
7. Prioriza arreglos: estructural primero (separar modalidades, índice que
   falta, datos fechados por todas partes), después formato de síntesis,
   después microestilo, después pulido (terminología, enlaces).
8. Entrega una lista de tareas con archivo + problema + arreglo propuesto,
   no una reescritura completa.

## Proceso para microeditar solo prosa

**En el pipeline writeonmars este trabajo es de la pasada 3** (naturalidad),
que carga la pirámide de prosa (`prosa-base` → registro → `marcela-prose`);
usa este proceso solo para material suelto fuera del pipeline.

Cuando la petición es microedición (la estructura es sólida; la prosa se lee
comprimida, robótica, de plantilla o de eslogan), no toques la estructura.
Pasa solo la revisión de prosa.

Entrega tres cosas, en este orden:

1. **Diagnóstico.** Cuáles de los ocho defectos de
   `./references/prose-pitfalls.md` aplican, con archivo y línea de dos o
   tres ejemplos concretos cada uno. No un genérico "la prosa suena rara".
2. **Prioridades.** Qué defectos arreglar primero en esta guía (típicamente
   pronombres vagos, después frases comprimidas, después cadenas de
   aforismos). Justifica por impacto en este texto concreto.
3. **Reescrituras concretas.** Antes/después de cada prioridad, sacados del
   archivo real. No plantillas genéricas.

Restricciones durante una pasada de microedición:

- **Sin cambios estructurales.** No partas archivos, no reordenes secciones,
  no añadas anexos. Si hacen falta, señálalo pero no lo ejecutes en esta
  pasada.
- **Sin contenido nuevo.** No añadas cajas, *callouts* ni secciones que no
  estaban.
- **Una regla por pasada.** Cada edición aplica una de las ocho reglas. Una
  pasada que mezcla "arreglar pronombres + añadir señales de orientación +
  traducir anglicismos" pierde la voz; las pasadas son secuenciales.
- **Preserva la voz.** Si la guía tiene voz estable (plural inclusivo en
  español, segunda persona en inglés…), mantenla. La microedición arregla
  prosa, no registro.

Cierre de una pasada de microedición: lista qué reglas se aplicaron, sobre
cuántas frases, y cuáles se dejaron intactas a propósito (y por qué). La
persona debe poder validar el diff contra la regla, no contra el gusto.

## Referencias

Digest completo de investigación con citas: `./references/research-digest.md`
(se conserva en inglés: es material de consulta con fuentes originales).

Catálogo de defectos de prosa con ejemplos: `./references/prose-pitfalls.md`.

Fuentes clave:

- Diátaxis framework: https://diataxis.fr/
- Knowles, *The Adult Learner*: https://www.sciencedirect.com/book/9780128117583
- Sweller, Cognitive Load Theory: https://link.springer.com/article/10.1007/s10648-019-09465-5
- Google Developer Style: https://developers.google.com/style
- Write the Docs: https://www.writethedocs.org/guide/
- Mayer, *Multimedia Learning*: https://www.cambridge.org/core/books/multimedia-learning/
- Kent C. Dodds, *Common mistakes with React Testing Library*: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library

---

Traducción al español: 2026-07-04 (el original nació en inglés; el pipeline
es en español y las referencias operativas deben leerse en el idioma en que
se escribe). El id `technical-guide-design` se conserva: lo citan prompts,
manifiestos y docs.
