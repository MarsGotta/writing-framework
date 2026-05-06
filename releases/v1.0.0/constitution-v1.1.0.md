<!--
  Snapshot archivado para release framework v1.0.0.
  Fuente: .specify/memory/constitution.md
  Constitución: v1.1.0 (Ratified 2026-05-06).
  No editar este archivo. Las modificaciones a la constitución
  ocurren en .specify/memory/constitution.md y se archivan en una
  nueva release.
-->

<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 1.1.0
Bump rationale: MINOR — el framework recibe nombre formal (Write.OnMars), un
preámbulo de "Propósito y alcance" y una nueva sección "Arquitectura del
framework" que codifica decisiones materiales (distribución como skills + MCP +
plugins, agnosticismo respecto al agente subyacente, memoria externa
vectorizada opcional, investigación basada en fuentes). No se redefinen ni
eliminan principios, por lo que no procede MAJOR; se añade material sustantivo,
por lo que no es PATCH.

Modified principles: ninguno. Los cinco principios I–V mantienen título y
contenido normativo.

Added sections:
- "Propósito y alcance" — preámbulo que nombra el framework como Write.OnMars
  y declara la audiencia primaria (agentes de IA), los tipos de salida (guías,
  manuales, artículos, libros, tutoriales) y la posición frente a Spec Kit.
- "Arquitectura del framework" — codifica la distribución (skills, MCP,
  plugins), el agnosticismo de agente, la memoria externa opcional y la
  trazabilidad documental con `resources/`.

Removed sections: ninguna.

Templates requiring updates:
- ⚠ pending  .specify/templates/plan-template.md   — sigue orientado a
  proyectos de software (Language/Version, Storage, Testing). Requiere variante
  editorial o adaptación de "Technical Context" para guías y capítulos.
- ⚠ pending  .specify/templates/spec-template.md   — las "User Stories" deben
  reinterpretarse como "Trayectos de lector"; "Functional Requirements" como
  requisitos editoriales (audiencia, promesa, ejemplo recurrente, riesgos).
- ⚠ pending  .specify/templates/tasks-template.md  — categorías deben reflejar
  fases editoriales (brief, esqueleto, redacción, revisión multi-pasada,
  pulido) en lugar de Setup/Foundational/Stories de software.
- ⚠ pending  .specify/templates/checklist-template.md — debe incorporar las
  cinco checklists del Principio V (estructura, utilidad, naturalidad,
  precisión, formato).
- ✅ updated  .specify/memory/constitution.md       — este archivo.

Follow-up TODOs: ninguno. Todas las fechas y placeholders quedan resueltos.
-->

# Write.OnMars Constitution

## Propósito y alcance

**Write.OnMars** es un framework editorial diseñado para que un agente de IA
produzca guías, manuales, artículos, libros y tutoriales técnicos al nivel de
calidad esperado de una autora especializada. No es un motor de redacción
aislado: es un *harness* que gobierna al agente seleccionado mediante skills,
servidores MCP y plugins instalables sobre cualquier proyecto.

Esta constitución se dirige en primera instancia al agente que ejecuta las
tareas y, en segunda instancia, a la persona que mantiene el framework. Toda
regla redactada con MUST, SHOULD o MAY se interpreta como obligación, fuerte
recomendación o permiso explícito tanto para humanos como para agentes.

Decisiones de alcance:

- **Salidas cubiertas**: guías técnicas, manuales, artículos, libros y
  tutoriales. Cualquier formato adicional MUST declararse en el brief antes
  de redactar.
- **Idioma primario**: español. Otras lenguas se tratan como excepción
  declarada.
- **Integración base**: el framework opera sobre el ciclo de Spec Kit
  (`/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`)
  y reutiliza sus extensiones (auto-commit, validación de rama).
- **Investigación de respaldo**: las decisiones editoriales se derivan de
  fuentes documentadas en `resources/` (actualmente
  `guia-IA-writing.md` y *Manual Maestro para la Producción de Textos
  Especializados*). Cualquier principio nuevo MUST citar al menos una fuente
  o justificar explícitamente la ausencia de antecedente.

## Core Principles

### I. Voz natural y sobria (NO NEGOCIABLE)

Toda guía, capítulo o fragmento producido bajo este framework MUST sonar como
una persona experta explicando algo con orden y criterio, no como una IA
intentando parecer humana ni como notas internas convertidas en prosa final.

Reglas obligatorias:

- MUST evitar frases comprimidas que obliguen al lector a reconstruir la
  intención (ej.: "Cabe en la cabeza"; "La herramienta estaba. El procedimiento, no.").
- MUST evitar la fórmula sentenciosa "No es X: es Y" más de una vez por capítulo,
  y solo cuando realmente cierre una idea importante.
- MUST evitar pronombres vagos ("eso", "esto", "lo", "esa decisión") sin
  referente explícito en la frase anterior.
- MUST evitar transiciones secas ("Vamos a verlo", "Pasemos al siguiente punto",
  "Quedan tres categorías") y reemplazarlas por transiciones que expliquen por
  qué cambia el tema.
- MUST evitar entusiasmo artificial, lenguaje promocional y metáforas mezcladas.

**Razón**: la voz es el principio fundacional del framework. Si el texto suena a
IA, eslogan o academicismo burocrático, ningún otro principio salva la guía.

### II. Estructura: situación → explicación → consecuencia práctica

Cada explicación significativa MUST seguir la secuencia *situación → explicación
→ consecuencia práctica*. Cada sección o capítulo MUST cerrar en una decisión,
una advertencia o una acción concreta para el lector.

Reglas obligatorias:

- Cada concepto técnico introducido MUST tener al menos un ejemplo concreto
  dentro del mismo capítulo.
- Cada capítulo MUST terminar con una sección "Qué hacer en la práctica" o
  equivalente operativa (checklist, plantilla, síntoma → causa probable).
- MUST existir un ejemplo recurrente compartido a lo largo de la guía. No se
  permiten ejemplos inventados nuevos en cada capítulo cuando el caso recurrente
  ya cubre la situación.

**Razón**: una guía útil responde de forma constante a "¿qué hago con esto?". Si
la sección no produce una acción, advertencia o decisión, no pertenece a la guía.

### III. Brief obligatorio antes de redactar (NO NEGOCIABLE)

Ninguna pieza de contenido —guía completa, capítulo nuevo o reescritura
sustantiva— MUST iniciar redacción sin un brief explícito que cubra los
siguientes campos:

1. **Audiencia**: quién lee.
2. **Problema**: qué le pasa ahora.
3. **Resultado esperado**: qué podrá hacer después.
4. **Nivel**: principiante, intermedio o avanzado.
5. **Tono**: experto, directo, natural, sobrio (variantes admitidas, pero
   declaradas).
6. **Conceptos obligatorios**: lista cerrada.
7. **Ejemplo recurrente**: caso que se usará durante toda la guía.
8. **Riesgos**: malentendidos a evitar.
9. **Acciones prácticas**: qué debe hacer el lector al terminar.

El brief MUST archivarse junto con la spec correspondiente (`specs/[###-feature]/`)
y MUST citarse en el plan y en las tareas.

**Razón**: sin brief, tanto las personas como los modelos generan texto
genérico. El brief es la traducción editorial del "Constitution Check" del flujo
Spec Kit.

### IV. Precisión léxica y arquitectura sintáctica integrada

El framework adopta el rigor terminológico de Cabré, RAE, Fundéu y AENOR, y el
estilo integrado (ciceroniano) para textos de alta especialización.

Reglas obligatorias:

- MUST mantener univocidad terminológica: un término por concepto dentro de un
  mismo dominio. La repetición exacta del término técnico es preferible a la
  variación sinonímica cuando ello compromete la precisión.
- MUST distinguir abreviaturas, símbolos, siglas y acrónimos según las normas
  ortotipográficas del español (puntuación, plural, mayúsculas).
- MUST sustituir anglicismos innecesarios por su equivalente en español
  (ej.: *return* → retorno; *socket* → zócalo; *display* → visualización;
  *librería* → biblioteca; *comando* → orden; *removible* → extraíble).
- MAY conservar términos técnicos en inglés (ej.: *harness*, *MCP*, *skill*,
  *system prompt*, *tool use*, *context window*) cuando no exista equivalente
  preciso o cuando el dominio profesional los use sin ambigüedad. Esta excepción
  MUST justificarse en el glosario de la guía.
- SHOULD favorecer la pasiva refleja sobre la pasiva perifrástica
  ("Se introducen los conceptos" frente a "Los conceptos son introducidos").
- SHOULD usar nominalizaciones, aposiciones y construcciones absolutas para
  ganar densidad informativa sin atomizar el pensamiento.

**Razón**: la autoridad profesional del texto depende de la coherencia entre
forma y significado. Un anglicismo gratuito o una sigla mal escrita erosiona la
confianza más rápido que un párrafo flojo.

### V. Revisión multi-pasada antes de publicar (NO NEGOCIABLE)

Ningún contenido MUST publicarse, fusionarse en `main` ni declararse "listo"
sin completar las cinco pasadas de revisión definidas:

1. **Estructura**: promesa clara, audiencia explícita, función de cada capítulo,
   progresión lógica, acción final.
2. **Utilidad**: ejemplos por concepto, acción práctica por capítulo, checklists,
   errores comunes, síntomas reales, criterios de éxito.
3. **Naturalidad**: ausencia de notas internas, transiciones explicadas,
   referentes claros, sin abuso de eslóganes ni metáforas mezcladas. El texto
   MUST poder leerse en voz alta sin sonar artificial.
4. **Precisión**: sin datos inventados; versiones, comandos y precios verificados;
   afirmaciones absolutas matizadas; principios estables distinguidos de datos
   temporales.
5. **Formato**: cajas visuales útiles, ejemplos diferenciados del cuerpo, títulos
   claros, índice navegable, sin bloques de texto excesivos.

Cada pasada MUST registrar su cumplimiento en una checklist firmada (humano o
agente declarado). Las checklists viven en `checklists/[###-feature]/` y se
referencian desde `plan.md` y `tasks.md`.

**Razón**: la revisión general "a ojo" no detecta los modos de fallo recurrentes
de la prosa generada con IA. Cinco pasadas con preguntas distintas evitan que
defectos de un dominio (p.ej., naturalidad) contaminen la evaluación de otro
(p.ej., precisión).

## Estándares editoriales

Restricciones materiales aplicables a todo artefacto del framework:

- **Plantilla de capítulo**: cada capítulo MUST seguir el patrón "Problema real →
  Idea clave → Por qué importa → Cómo funciona → Ejemplo → Error frecuente → Qué
  hacer en la práctica → Checklist → Puente al siguiente capítulo".
- **Cajas obligatorias por capítulo**: al menos una de las siguientes cajas
  MUST aparecer: "Quédate con esto", "Qué hacer mañana", "Síntoma → causa
  probable".
- **Estructura de guía completa**: portada, promesa, "Para quién es", "Para
  quién no es", "Qué vas a aprender", ruta rápida de lectura, conceptos base,
  desarrollo por capítulos, checklists prácticos, plantillas reutilizables,
  errores comunes, glosario y notas/fuentes técnicas.
- **Glosario**: cada término técnico MUST definirse antes de usarse en cuerpo
  expositivo y MUST aparecer en el glosario final cuando la guía supere los tres
  capítulos.
- **Datos verificables**: versiones de software, precios, comandos y citas
  bibliográficas MUST marcarse como verificables y fechar su última comprobación.
- **Idioma**: el idioma primario del framework es el español. Excepciones
  (citas, fragmentos de código, términos técnicos sin equivalente) MUST
  declararse en el brief.

## Flujo de producción editorial con Spec Kit

Este framework reutiliza el ciclo Spec Kit (`/speckit-specify`, `/speckit-plan`,
`/speckit-tasks`, `/speckit-implement`) traducido a la producción de guías:

1. **`/speckit-specify`** → produce el brief obligatorio del Principio III y los
   trayectos de lector (equivalente editorial de "user stories"). El brief vive
   en `specs/[###-feature]/spec.md`.
2. **`/speckit-clarify`** → resuelve ambigüedades del brief antes de planificar.
   MUST usarse cuando la audiencia, el ejemplo recurrente o el resultado
   esperado contengan campos `[NEEDS CLARIFICATION]`.
3. **`/speckit-plan`** → produce el esqueleto editorial: estructura de la guía
   completa o del capítulo, conceptos base, ejemplo recurrente y mapa de cajas.
   El "Constitution Check" del plan MUST verificar conformidad con los cinco
   principios.
4. **`/speckit-tasks`** → desglosa la producción en tareas editoriales
   (redacción de secciones, generación de ejemplos, construcción de checklists,
   pasadas de revisión). Cada pasada del Principio V MUST aparecer como una
   tarea explícita.
5. **`/speckit-implement`** → ejecuta las tareas. La salida final MUST adjuntar
   las cinco checklists firmadas antes de cerrar la rama.
6. **`/speckit-analyze`** → audita consistencia entre brief, plan y tareas.
   MUST ejecutarse antes de pasar a `implement` cuando la guía completa supere
   un capítulo.

Las extensiones Git registradas en `.specify/extensions.yml` permanecen activas:
los hooks de auto-commit aplican igual a artefactos editoriales que a código.

## Arquitectura del framework

Write.OnMars se materializa como un conjunto de extensiones instalables sobre un
proyecto editorial nuevo. Esta sección codifica las decisiones de arquitectura
que sostienen los cinco principios.

**Distribución**:

- El framework MUST distribuirse como una combinación de skills (`.claude/skills/`
  o equivalente del agente), servidores MCP y plugins. Ninguna funcionalidad
  editorial nuclear MUST depender de modificaciones del agente subyacente.
- Cada componente MUST documentar en su carpeta el principio o estándar que
  implementa, de modo que un mantenedor pueda mapear "skill X → Principio Y".
- La instalación sobre un proyecto nuevo MUST dejar el repositorio operativo
  con: constitución copiada, plantillas Spec Kit disponibles, hooks Git
  registrados y, si procede, MCPs configurados.

**Agnosticismo de agente**:

- El framework SHOULD funcionar sobre cualquier agente que soporte skills/MCP
  (Claude Code, Codex, Cursor, etc.). Las skills MUST evitar dependencias
  rígidas de un único proveedor cuando exista alternativa portable.
- Las instrucciones que sí dependen del agente (p.ej., rutas de configuración,
  formato de hooks) MUST aislarse en archivos claramente identificados por
  agente y no contaminar las skills de redacción.

**Memoria externa**:

- El framework MAY apoyarse en una memoria externa vectorizada para conservar
  ejemplos recurrentes, glosarios extendidos, fragmentos canónicos y feedback
  de revisión a lo largo de proyectos.
- Cuando se active, la memoria externa MUST documentar su esquema mínimo
  (entidad, fuente, fecha, etiquetas) y MUST poder reconstruirse a partir de
  los artefactos del repositorio. La memoria es caché acelerada, no fuente de
  verdad.
- El uso de memoria externa MUST declararse en el plan del trayecto editorial
  y respetar las reglas de "Datos verificables" de los Estándares editoriales.

**Trazabilidad documental**:

- Toda decisión normativa nueva (principio, regla de estilo, plantilla) MUST
  citar al menos una fuente del directorio `resources/` o registrar
  explícitamente que se trata de una decisión propia del proyecto.
- Las fuentes incorporadas a `resources/` MUST conservar metadatos de origen y
  fecha de incorporación cuando provengan de material externo.

## Governance

**Supremacía**: esta constitución supersede cualquier convención editorial
informal previa. Toda guía, plantilla, plan y revisión MUST verificar
cumplimiento explícito antes de cerrarse.

**Procedimiento de enmienda**:

1. Propuesta documentada en una rama dedicada con prefijo `constitution/`.
2. Revisión por la persona mantenedora del framework (actualmente Marcela
   Gotta) y, cuando aplique, por el equipo editorial extendido.
3. Plan de migración cuando la enmienda afecte guías ya publicadas: lista de
   guías impactadas, criterio de re-revisión y plazo.
4. Ejecución de `/speckit-constitution` para actualizar este archivo y propagar
   cambios a las plantillas (`plan-template.md`, `spec-template.md`,
   `tasks-template.md`, `checklist-template.md`).
5. Commit con mensaje `docs: amend constitution to vX.Y.Z (motivo)`.

**Política de versionado** (semver editorial):

- **MAJOR**: eliminación o redefinición incompatible de un principio o sección
  de gobierno; cambios que invalidan guías publicadas.
- **MINOR**: nuevo principio, nueva sección de estándares editoriales o
  expansión material de una regla existente.
- **PATCH**: aclaraciones, correcciones tipográficas, refinamientos no
  semánticos.

**Cadencia de cumplimiento**:

- Cada PR que toque `specs/`, `guides/`, `chapters/` o cualquier artefacto
  publicable MUST referenciar la versión de la constitución vigente y declarar
  conformidad o desviación justificada en `Complexity Tracking` del plan.
- Revisión bianual obligatoria de la constitución contra guías publicadas;
  desviaciones recurrentes disparan enmienda formal.
- La guía operativa de runtime para agentes (p.ej., `CLAUDE.md`, `AGENTS.md`)
  MUST citar esta constitución como fuente de verdad editorial.

**Version**: 1.1.0 | **Ratified**: 2026-05-06 | **Last Amended**: 2026-05-06
