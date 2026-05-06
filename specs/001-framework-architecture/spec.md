# Feature Specification: Arquitectura y flujo de trabajo del harness Write.OnMars

**Feature Branch**: `001-framework-architecture`
**Created**: 2026-05-06
**Status**: Draft
**Input**: User description: "lo primero quiero crear la arquitectura de este harness, he pensado que quizá podemos utilizar las extensiones y los presets de spec kit para ayudaros con esto, además de una serie de skills, o no sé si eso sería redundante, necesito que me ayudes a investigar todas las opciones para crear la estructura, y un flujo de trabajo, normalmente es 1. investigar sobre el tema en cuestion 2. generar archivos agent.md o archivos para configurar el repositorio que ayuden a dar contexto 3. generar un temario 4. generar descripciones del temario para que todo tenga un mismo hilo conductor 5. enviar a sub agentes a generar el contenido siempre siñendose a una estructura didactica 5. enviar sub agentes a contrastar la informacion."

## Clarifications

### Session 2026-05-06

- Q: Encaje de las skills existentes (`/marcela-prose`, `/technical-guide-design`) con las skills nuevas del framework → A: Envolver (opción B). El framework declara ambas como dependencias canónicas, las invoca en los pasos del flujo donde su alcance ya cubre el resultado esperado, y solo desarrolla lo que falta (instalación, brief, investigación, contraste, sub-agentes, hooks, orquestación de las cinco pasadas).
- Q: Distribución de las skills envueltas hacia el proyecto destino → A: Empaquetar (opción A). El repositorio canónico de Write.OnMars distribuye copias bundled de `/marcela-prose` y `/technical-guide-design`. La instalación del framework copia o enlaza esas skills al proyecto destino. La sincronización con otras fuentes (p. ej., el Obsidian vault original) se trata como procedimiento de mantenimiento separado, no como ruta de distribución.
- Q: Validación humana en pasadas críticas del Principio V → A: Configurable con default B (opción D). v1 trae como default la firma humana obligatoria en pasada 3 (naturalidad) y pasada 4 (precisión); las pasadas 1, 2 y 5 pueden cerrar autónomamente con checklist verde. El manifiesto del proyecto MAY declarar una matriz alternativa de firmas (autónoma / humana) por pasada; cualquier desviación del default se justifica en el plan.
- Q: Modo de orquestación de las cinco pasadas → A: Sub-agente fresco por pasada (opción B). Cada pasada se delega a un sub-agente independiente con prompt específico, skills propias de la pasada (`/technical-guide-design` para 1 y 2; `/marcela-prose` para 3; skill de contraste para 4; skill de formato para 5) y contexto mínimo (capítulo objetivo + brief + glosario consolidado + descripciones encadenadas vecinas). Las pasadas siguen siendo secuenciales; el sub-agente no hereda el contexto de redacción previo, lo que reduce el sesgo de "ya conozco este texto".
- Q: Salida final de v1 — solo markdown o compilación → A: Solo markdown (opción A). v1 produce capítulos en `chapters/[###]-titulo.md`, un `index.md` con la ruta de lectura, `glossary.md`, archivo de errores comunes y plantillas reutilizables. La compilación a PDF, sitio estático, ePub u otros formatos de distribución queda fuera del alcance de v1 y se aborda como feature separada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Instalación inicial del harness en un repositorio editorial nuevo (Priority: P1)

Una persona mantenedora editorial (o un agente delegado) abre un repositorio Git vacío o ya inicializado y aplica el framework Write.OnMars. Al terminar, el repositorio queda con: la constitución copiada, las plantillas Spec Kit listas, las skills editoriales registradas, los hooks Git configurados, un archivo de contexto de agente generado a partir de un cuestionario inicial y un manifiesto declarando la versión del framework instalada.

**Why this priority**: sin instalación reproducible no hay framework aplicable. Todo el resto del flujo depende de que el repositorio quede en un estado conocido y verificable.

**Independent Test**: ejecutar la instalación contra un repositorio Git vacío y comprobar que (a) los seis artefactos —constitución, plantillas Spec Kit, skills editoriales, hooks Git, archivo de contexto del agente, manifiesto de versión— están presentes; (b) el operador puede ejecutar `/speckit-specify` inmediatamente y obtener un brief válido; (c) los hooks responden a los eventos definidos sin error.

**Acceptance Scenarios**:

1. **Given** un repositorio vacío recién inicializado con `git init`, **When** se ejecuta el comando de instalación del framework, **Then** el repositorio contiene la constitución vigente, las plantillas Spec Kit, las skills editoriales, los hooks Git activos, un archivo de contexto de agente y un manifiesto con la versión del framework.
2. **Given** un repositorio con `CLAUDE.md` o `AGENTS.md` previo, **When** se ejecuta la instalación, **Then** el archivo previo se preserva o se fusiona sin pérdida de instrucciones del operador.
3. **Given** una instalación completada, **When** el operador ejecuta `/speckit-specify "Guía sobre X"`, **Then** se crea la rama y la spec con los nueve campos del brief obligatorio del Principio III.

---

### User Story 2 - Producción de una guía completa siguiendo el flujo editorial (Priority: P1)

Un operador (humano + agente) dispara un proyecto editorial con un tema y avanza por el flujo del framework: brief → investigación con fuentes → contexto del proyecto → temario → descripciones encadenadas → redacción capítulo a capítulo siguiendo la estructura didáctica → contraste de información → revisión multi-pasada (cinco pasadas).

**Why this priority**: este es el ciclo nuclear del framework. Si no produce guías que pasen las cinco pasadas del Principio V con calidad demostrable, ningún otro componente vale.

**Independent Test**: producir una guía de prueba (≥3 capítulos) sobre un tema acotado, verificando que cada etapa del flujo deja artefactos auditables (`brief`, `research.md`, `temario`, `descripciones`, capítulos individuales, checklists firmadas por pasada) y que las cinco checklists del Principio V pasan al cierre.

**Acceptance Scenarios**:

1. **Given** un repositorio instalado con Write.OnMars, **When** el operador ejecuta el ciclo completo Spec Kit (`/speckit-specify` → `/speckit-clarify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement`), **Then** se generan los artefactos correspondientes a cada etapa del flujo editorial.
2. **Given** la etapa de investigación, **When** la skill correspondiente se ejecuta, **Then** se produce un `research.md` con fuentes citadas, fechadas y con marca [VERIFICAR] en datos volátiles.
3. **Given** el temario aprobado, **When** se generan las descripciones de capítulo, **Then** cada descripción cita el ejemplo recurrente del brief y declara la promesa específica del capítulo y su conexión con el anterior y el siguiente.
4. **Given** un capítulo redactado, **When** se ejecuta la pasada 3 (naturalidad), **Then** se produce una checklist firmada que enumera frases comprimidas, pronombres vagos sin referente, eslóganes excesivos y transiciones secas detectadas.
5. **Given** un capítulo redactado, **When** se ejecuta la pasada 4 (precisión), **Then** se contrasta cada afirmación verificable contra al menos una fuente y se marca cada item como verificado, pendiente o desviación justificada.
6. **Given** las cinco pasadas completadas, **When** el operador cierra el proyecto, **Then** la salida final adjunta las cinco checklists firmadas y ningún hallazgo crítico queda sin resolver.

---

### User Story 3 - Paralelización de redacción y contraste por capítulos (Priority: P2)

Para guías de tamaño medio o grande (≥4 capítulos), el operador puede delegar la redacción de capítulos a sub-agentes que trabajan en paralelo siguiendo la estructura didáctica del Principio II y respetando el ejemplo recurrente y el glosario consolidado del proyecto. Análogamente, el contraste de información (pasada 4) puede paralelizarse capítulo a capítulo.

**Why this priority**: la paralelización mejora productividad pero no bloquea v1: una guía corta puede producirse en serie. Forma parte del ciclo nuclear pero no del primer caso a soportar.

**Independent Test**: producir una guía de ≥4 capítulos donde 2+ capítulos se redactan en paralelo y verificar que (a) usan el mismo ejemplo recurrente, (b) mantienen univocidad terminológica con el glosario, (c) las descripciones encadenadas conservan el hilo conductor entre capítulos vecinos.

**Acceptance Scenarios**:

1. **Given** un temario de 4 capítulos con descripciones aprobadas, **When** se delega la redacción a sub-agentes en paralelo, **Then** los capítulos producidos comparten el ejemplo recurrente y el glosario consolidado.
2. **Given** capítulos redactados en paralelo, **When** se ejecuta la pasada 1 (estructura), **Then** se detecta cualquier ruptura del hilo conductor o duplicación temática entre capítulos.

---

### User Story 4 - Mantenimiento y propagación de cambios del framework (Priority: P3)

La persona mantenedora del framework actualiza una skill, una plantilla o la constitución. Los cambios se propagan a los proyectos editoriales que ya usan Write.OnMars de forma trazable: cada proyecto declara la versión del framework con la que opera y puede actualizarse de forma controlada.

**Why this priority**: es deseable a medio plazo, pero v1 puede vivir con instalación única por proyecto. La actualización entre versiones es una mejora de gobernanza.

**Independent Test**: aplicar un cambio menor a una skill canónica, ejecutar el procedimiento de actualización en un proyecto instalado, y comprobar que el proyecto declara la nueva versión y que las guías existentes no se rompen.

**Acceptance Scenarios**:

1. **Given** un proyecto instalado con Write.OnMars vX.Y.Z, **When** se publica una skill vX.Y.Z+1 y se ejecuta el procedimiento de actualización, **Then** el proyecto refleja la nueva versión sin perder configuración local.
2. **Given** una enmienda a la constitución, **When** se actualiza el proyecto, **Then** las plantillas afectadas se sincronizan según el "Sync Impact Report" de la enmienda.

---

### Edge Cases

- ¿Qué ocurre si la instalación se ejecuta sobre un repositorio que ya tiene Spec Kit pero no Write.OnMars? La instalación MUST detectar Spec Kit existente y solo añadir las skills y extensiones específicas del framework, sin sobreescribir configuraciones.
- ¿Qué ocurre si el operador intenta saltar etapas (p. ej., redactar sin temario aprobado)? El framework MUST bloquear la transición a redacción mientras las etapas previas no tengan artefactos válidos firmados.
- ¿Qué ocurre si una pasada de revisión falla? La pasada MUST devolver una lista accionable de hallazgos y bloquear el cierre hasta que cada hallazgo crítico esté resuelto o documentado como desviación justificada.
- ¿Qué ocurre si la fuente externa de verificación no está disponible? La pasada 4 (precisión) MUST marcar cada afirmación pendiente y bloquear el cierre del proyecto hasta que la verificación se realice manualmente.
- ¿Qué ocurre si el operador trabaja con un agente distinto a Claude Code? Las skills MUST ser portables a cualquier agente compatible con skills/MCP; las dependencias específicas de un agente MUST aislarse en archivos identificados.
- ¿Qué ocurre con guías producidas antes de una enmienda mayor de la constitución? El proyecto MUST declarar la versión de constitución bajo la que se cerró cada guía y conservar esa versión salvo migración explícita.
- ¿Qué ocurre si dos sub-agentes en paralelo introducen el mismo término técnico con definiciones distintas? El framework MUST detectar la colisión durante la consolidación del glosario y bloquear el cierre hasta resolución.

## Requirements *(mandatory)*

### Functional Requirements

**Instalación y configuración del repositorio**

- **FR-001**: El sistema MUST proporcionar un comando de instalación que, sobre un repositorio Git inicializado, deje disponible: la constitución, las plantillas Spec Kit (spec, plan, tasks, checklist), las skills editoriales canónicas (incluidas las copias bundled de `/marcela-prose` y `/technical-guide-design`), los hooks Git registrados, un archivo de contexto de agente y un manifiesto declarando la versión del framework instalada.
- **FR-002**: El comando de instalación MUST generar el archivo de contexto de agente (`AGENTS.md`/`CLAUDE.md` o equivalente) a partir de un cuestionario inicial que cubra: tipo de proyecto editorial, agente prioritario, idioma primario, audiencia general y dominio técnico del proyecto.
- **FR-003**: El sistema MUST detectar instalaciones previas (Spec Kit u otros) y fusionar configuraciones sin pérdida.
- **FR-004**: El sistema MUST declarar la versión del framework, la versión de la constitución, la lista de skills habilitadas y la matriz de firmas por pasada (Principio V) en un archivo manifiesto del proyecto. La matriz de firmas indica para cada pasada (1–5) si admite cierre autónomo o requiere firma humana explícita; el default de v1 es: pasadas 1, 2 y 5 autónomas; pasadas 3 (naturalidad) y 4 (precisión) requieren firma humana.

**Brief y especificación editorial**

- **FR-005**: La spec generada por `/speckit-specify` MUST cubrir los nueve campos del brief obligatorio (Principio III): audiencia, problema, resultado esperado, nivel, tono, conceptos obligatorios, ejemplo recurrente, riesgos y acciones prácticas.
- **FR-006**: El sistema MUST bloquear el avance a `/speckit-plan` mientras la spec contenga marcadores `[NEEDS CLARIFICATION]` no resueltos en los campos críticos del brief (audiencia, ejemplo recurrente, resultado esperado).
- **FR-007**: Tras aprobar el brief, el framework MUST generar o actualizar un archivo de contexto específico del proyecto editorial que cargue automáticamente en cada sesión del agente: audiencia, ejemplo recurrente, glosario inicial, tono y reglas microestilísticas heredadas de la constitución.

**Investigación con fuentes**

- **FR-008**: El framework MUST proporcionar una skill de investigación que orqueste sobre cualquier MCP compatible con el contrato de citación del framework (FR-009a) y produzca un `research.md` con: temas explorados, fuentes citadas con URL/referencia, fecha de consulta y marca [VERIFICAR] en datos volátiles (versiones, precios, comandos).
- **FR-009**: La skill de investigación MUST aceptar `resources/` como fuente local obligatoria y MAY consultar MCPs externos compatibles (p. ej., `context7` para documentación de librerías, MCPs de web search o `fetch`). El motor utilizado y la fecha de cada consulta MUST registrarse en `research.md`.
- **FR-009a**: El framework MUST publicar un contrato de citación que cualquier MCP de investigación o contraste DEBE cumplir para integrarse. Campos mínimos: identificador estable, tipo (documentación oficial / web pública / archivo local / cita bibliográfica), URL o ruta, fecha de consulta, fragmento citado y motor de origen.
- **FR-009b**: El framework MAY distribuir un módulo opcional `writeonmars-research` que implementa el contrato de citación de extremo a extremo (búsqueda + fetch + verificación contra `resources/`). El módulo se activa por proyecto vía manifiesto; v1 funciona en modo BYOM (bring your own MCP) por defecto.

**Plan editorial: temario y descripciones encadenadas**

- **FR-010**: La salida de `/speckit-plan` MUST incluir el temario completo de la guía y un mapa de descripciones encadenadas donde cada capítulo declara: promesa específica, conexión con el capítulo anterior, conexión con el siguiente, ejemplo recurrente aplicado y conceptos del glosario que introduce.
- **FR-011**: El plan MUST verificar conformidad con los cinco principios de la constitución (Constitution Check) antes de emitirse y MUST registrar cualquier desviación en `Complexity Tracking`.

**Tareas y estructura didáctica**

- **FR-012**: La salida de `/speckit-tasks` MUST descomponer la producción en tareas que respetan la estructura de capítulo del Principio II (problema → idea clave → por qué importa → cómo funciona → ejemplo → error frecuente → qué hacer en la práctica → checklist → puente).
- **FR-013**: Cada pasada del Principio V MUST aparecer como una tarea independiente, secuencialmente ordenada (estructura → utilidad → naturalidad → precisión → formato), con su checklist asociada.

**Redacción y delegación a sub-agentes**

- **FR-014**: El framework MUST permitir delegar la redacción de capítulos individuales a sub-agentes que reciben: el brief completo, el temario, la descripción del capítulo objetivo, las descripciones de capítulos contiguos, el ejemplo recurrente y el glosario consolidado.
- **FR-015**: Cada sub-agente de redacción MUST devolver el capítulo y un anexo de términos nuevos introducidos para integrarse al glosario; las colisiones de definición entre capítulos paralelos MUST detectarse al consolidar.

**Contraste y verificación**

- **FR-016**: El framework MUST proporcionar una skill de contraste (pasada 4) que verifique afirmaciones técnicas, versiones, comandos y citas contra al menos una fuente registrada bajo el contrato de citación (FR-009a). Cada afirmación queda marcada como verificada, pendiente o desviación justificada.
- **FR-017**: La skill de contraste MUST poder paralelizarse capítulo a capítulo y MUST consolidar los hallazgos en un `findings.md` único por proyecto.

**Revisión multi-pasada**

- **FR-018**: El framework MUST ejecutar las cinco pasadas del Principio V (estructura, utilidad, naturalidad, precisión, formato) como tareas separadas y secuenciales, cada una con su checklist firmable. Cada pasada MUST delegarse a un sub-agente independiente con: prompt específico de la pasada, skills aplicables (pasadas 1 y 2 → `/technical-guide-design`; pasada 3 → `/marcela-prose`; pasada 4 → skill de contraste; pasada 5 → skill de formato) y contexto mínimo (capítulo objetivo, brief, glosario consolidado, descripciones encadenadas vecinas). El sub-agente no hereda el contexto de redacción previo.
- **FR-019**: Cada pasada MUST producir una lista de hallazgos accionables con: frase original, problema, severidad (crítico/medio/bajo) y reescritura sugerida.
- **FR-020**: El cierre del proyecto MUST bloquearse mientras alguna pasada tenga hallazgos críticos abiertos no justificados.
- **FR-020a**: El cierre del proyecto MUST bloquearse adicionalmente mientras una pasada marcada como "firma humana requerida" en el manifiesto (FR-004) no tenga la firma del operador humano declarado. Por defecto en v1, esta condición aplica a pasadas 3 (naturalidad) y 4 (precisión). Cualquier desviación del default MUST justificarse en `Complexity Tracking` del plan.

**Memoria editorial**

- **FR-021**: El framework MUST conservar el glosario consolidado, el ejemplo recurrente y los hallazgos firmados como artefactos del repositorio (no como caché externa) para que cualquier mantenedor pueda reconstruir el estado del proyecto sin acceso a sistemas externos.
- **FR-022**: El framework MAY apoyarse en una memoria externa vectorizada para acelerar consultas a glosarios extendidos, fragmentos canónicos y feedback de revisión, siempre que esa memoria pueda reconstruirse desde los artefactos del repositorio. La memoria externa es caché, nunca fuente de verdad.

**Portabilidad y agnosticismo de agente**

- **FR-023**: Las skills editoriales MUST evitar dependencias rígidas de un único proveedor de agente cuando exista alternativa portable.
- **FR-024**: Las dependencias específicas de un agente MUST aislarse en directorios identificados (p. ej., `agents/claude/`, `agents/codex/`) y no contaminar las skills nucleares.

**Reuso de skills existentes (envoltura, no duplicación)**

- **FR-025**: El framework MUST declarar `/marcela-prose` y `/technical-guide-design` como dependencias canónicas e invocarlas en los pasos del flujo donde su alcance ya cubre el resultado esperado:
  - Plan editorial (temario, estructura de capítulos, descripciones encadenadas) → `/technical-guide-design`.
  - Redacción capítulo a capítulo (FR-014) → `/technical-guide-design` para arquitectura del capítulo y `/marcela-prose` para voz, microestilo y limpieza de patrones LLM.
  - Pasada 1 (estructura) y pasada 2 (utilidad) → `/technical-guide-design`.
  - Pasada 3 (naturalidad) → `/marcela-prose`.
- **FR-026**: Las skills nuevas que el framework desarrolle MUST limitarse a lo que `/marcela-prose` y `/technical-guide-design` no cubren: instalación, brief, investigación con contrato de citación, contraste/precisión, orquestación de las cinco pasadas, delegación a sub-agentes, hooks Git y manifiesto del proyecto.
- **FR-027**: Las invocaciones del framework a las skills envueltas MUST registrar la versión de cada skill empleada en el `findings.md` y en el manifiesto del proyecto, para que un proyecto pueda reproducirse aunque la skill evolucione.
- **FR-028**: El repositorio canónico de Write.OnMars MUST contener las copias bundled de `/marcela-prose` y `/technical-guide-design` como assets propios. La instalación del framework copia o enlaza esas skills al proyecto destino junto con las skills propias del framework. La sincronización entre el repositorio canónico y otras fuentes externas (p. ej., el Obsidian vault original) MUST documentarse como procedimiento de mantenimiento separado, fuera del ciclo de instalación.

**Salida del proyecto editorial**

- **FR-029**: La salida de v1 MUST limitarse a artefactos markdown del repositorio: capítulos en `chapters/[###]-titulo.md`, un `index.md` con la ruta de lectura ordenada y enlaces a cada capítulo, `glossary.md` con el glosario consolidado, un archivo de errores comunes y las plantillas reutilizables de la guía. La compilación a otros formatos (PDF, sitio estático, ePub) queda fuera del alcance de v1 y se aborda como feature separada.

### Key Entities

- **Brief editorial**: contrato inicial del proyecto. Cubre los nueve campos del Principio III. Vive en `specs/[###-feature]/spec.md`.
- **Investigación**: notas de exploración con fuentes citadas y fechadas. Vive en `specs/[###-feature]/research.md`.
- **Contexto del proyecto**: archivo cargado automáticamente por el agente en cada sesión, derivado del brief. Vive en la raíz del proyecto editorial (`AGENTS.md`/`CLAUDE.md` u homólogo).
- **Temario**: lista ordenada de capítulos con sus promesas individuales. Vive en `specs/[###-feature]/plan.md` (sección dedicada).
- **Descripciones encadenadas**: para cada capítulo, conexión con el anterior y con el siguiente, ejemplo recurrente aplicado y conceptos introducidos. Vive en `specs/[###-feature]/plan.md` (sección dedicada).
- **Glosario consolidado**: términos técnicos del proyecto, definición y origen (capítulo donde se introducen). Vive en `specs/[###-feature]/glossary.md`.
- **Capítulo**: artefacto de salida con la estructura didáctica del Principio II. Vive en `chapters/[###]-titulo.md`.
- **Index**: ruta de lectura ordenada de la guía con enlaces a cada capítulo. Vive en `index.md`.
- **Errores comunes**: catálogo de malentendidos y errores frecuentes asociados a la guía. Vive en `common-errors.md`.
- **Plantillas reutilizables**: snippets, checklists y formatos que la guía expone para reuso del lector. Viven en `templates/`.
- **Checklist de pasada**: registro firmado del cumplimiento de una de las cinco pasadas. Vive en `checklists/[###-feature]/pasada-N.md`.
- **Hallazgos de revisión**: lista accionable producida por las pasadas, con frase original, problema, severidad y reescritura sugerida. Vive en `specs/[###-feature]/findings.md`.
- **Manifiesto del proyecto**: declara la versión del framework, la versión de la constitución y las skills habilitadas. Vive en la raíz del proyecto editorial.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: La instalación inicial del framework en un repositorio Git vacío se completa en menos de 5 minutos en interacción humana, dejando el repositorio listo para `/speckit-specify`.
- **SC-002**: Una guía de 8 capítulos producida con el flujo completo pasa las cinco pasadas del Principio V con menos de 2 hallazgos críticos por capítulo en la pasada 3 (naturalidad) y cero hallazgos críticos sin resolver en la pasada 4 (precisión) al cierre.
- **SC-003**: El 100% de los capítulos publicados aplica la estructura didáctica del Principio II (las nueve secciones: problema, idea clave, por qué importa, cómo funciona, ejemplo, error frecuente, qué hacer en la práctica, checklist, puente).
- **SC-004**: El glosario del proyecto cubre el 100% de los términos técnicos introducidos en el cuerpo de los capítulos; ningún término técnico aparece definido implícitamente sin entrada en el glosario.
- **SC-005**: El ejemplo recurrente declarado en el brief aparece en al menos el 80% de los capítulos y no se introducen ejemplos inventados nuevos cuando el caso recurrente cubre la situación.
- **SC-006**: La paralelización de redacción reduce el tiempo total de producción al menos un 40% comparada con la ejecución serial, manteniendo los mismos resultados de revisión multi-pasada.
- **SC-007**: La portabilidad entre agentes se demuestra ejecutando el flujo completo sobre dos agentes distintos sin modificar las skills nucleares.
- **SC-008**: Una persona mantenedora del framework puede actualizar una skill canónica y propagar el cambio a un proyecto existente en menos de 15 minutos sin pérdida de configuración local.
- **SC-009**: La skill de investigación produce un `research.md` con al menos una fuente fechada por cada concepto técnico declarado en el brief.

## Assumptions

- **Idioma**: el idioma primario del framework y de las guías producidas es el español; cualquier excepción se declara en el brief (constitución § "Propósito y alcance").
- **Salidas v1**: la unidad canónica de v1 es la guía técnica (1+ capítulos) en formato markdown. Manuales = secuencia ordenada de guías; libros = guía con ≥10 capítulos; artículos = guía de 1 capítulo. La clasificación se revisa en futuras enmiendas. Cualquier compilación a PDF, sitio web o ePub queda fuera de v1.
- **Agente prioritario v1**: la primera implementación opera sobre Claude Code. Las skills se diseñan agnósticas para portarse a otros agentes (Codex, Cursor, etc.) sin reescritura nuclear.
- **Memoria externa vectorizada**: en v1 se define la interfaz y se documenta como capability OPCIONAL; no se incluye implementación funcional por defecto. La fuente de verdad sigue siendo el repositorio.
- **Spec Kit como base**: el framework reutiliza el ciclo Spec Kit existente y sus extensiones (auto-commit, validación de rama, generación de feature branch).
- **Distribución**: el framework se distribuye como un repositorio canónico que combina skills, MCP y plugins. La instalación copia o enlaza los assets en el proyecto destino.
- **Operador humano**: el flujo asume al menos un humano responsable del proyecto editorial. v1 trae como default firma humana obligatoria en pasadas 3 (naturalidad) y 4 (precisión); pasadas 1, 2 y 5 pueden cerrar autónomamente. El operador puede sobreescribir la matriz de firmas en el manifiesto del proyecto.
- **Investigación externa**: la skill de investigación opera en modo BYOM por defecto. El operador instala MCPs compatibles con el contrato de citación (`context7`, web search, `fetch`, etc.) y el framework orquesta sobre ellos. Un proyecto MAY activar el módulo opcional bundled `writeonmars-research` cuando necesite coherencia uniforme de citación o quiera evitar dependencias externas. Ningún MCP concreto se asume obligatorio.
- **Orden de las pasadas**: las cinco pasadas del Principio V se ejecutan secuencialmente (estructura → utilidad → naturalidad → precisión → formato); defectos detectados en una pasada se resuelven antes de avanzar a la siguiente.

## Resolved Decisions

- **D1 — MCP de investigación y contraste: híbrido (BYOM por defecto + módulo opcional)**. v1 declara un contrato de citación (FR-009a) y opera en modo BYOM con MCPs existentes (context7, web search, fetch). El framework MAY activar un módulo bundled `writeonmars-research` (FR-009b) por proyecto cuando se requiera coherencia uniforme de citación o ausencia de dependencias externas. Resuelto el 2026-05-06.

## Dependencies

- Spec Kit (versión instalada en `.specify/`).
- Extensión Git de Spec Kit (instalada en `.specify/extensions/git/`).
- Constitución del framework v1.1.0 o superior (`.specify/memory/constitution.md`).
- Recursos editoriales en `resources/` (`guia-IA-writing.md`, *Manual Maestro para la Producción de Textos Especializados*).
- Skill `/marcela-prose` (voz, microestilo, limpieza de patrones LLM, prosa española natural) — distribuida como copia bundled del repositorio canónico.
- Skill `/technical-guide-design` (diseño didáctico, estructura de guía y capítulo, microedición pedagógica) — distribuida como copia bundled del repositorio canónico.
