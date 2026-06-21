<!--
SYNC IMPACT REPORT
==================
Version change: 1.3.0 → 1.4.0
Bump rationale: MINOR — añade un requisito (atribución por afirmación + índice de
factualidad derivado) sin invalidar guías ni redefinir principios. Refuerza IV y V;
"Fuentes por capítulo" se conserva (MUST) y pasa a derivarse/validarse contra
claims.md. Feature 003-atribucion-factualidad.

Added standards:
- Atribución por afirmación (MUST en pasada 4): cada afirmación verificable de un
  capítulo se registra con su(s) cita(s) y el veredicto de relación en claims.md
  (ClaimRecord v1.0). "Fuentes por capítulo" se valida/deriva desde ahí.
- Índice de factualidad (derivado, determinista): status.py expone factualidad por
  capítulo y global; gate de cierre opcional (manifest.quality_gates).

Modified principles:
- IV. Precisión léxica — gana grano de afirmación y veredicto de relación
  (apoya/matiza/contradice/menciona). Sin redefinición incompatible.
- V. Revisión multi-pasada — la pasada 4 (precisión) persiste claims.md y produce
  métrica; conserva las cinco dimensiones y "detector ≠ corrector".

Historial previo
----------------
Version change: 1.2.1 → 1.3.0
Bump rationale: MINOR — relaja estándares y añade un requisito, sin invalidar
guías. (1) "Plantilla de capítulo" y "Qué hacer en la práctica" pasan de MUST a
SHOULD, y el checklist puede centralizarse, cuando las adendas del proyecto lo
declaren (calibrado contra la guía de referencia guide-ai-developers-basic, que
centraliza el checklist y no usa cajas). (2) Las cajas visuales pasan de
"obligatoria al menos una" a SHOULD-según-sector. (3) NUEVO requisito: "Fuentes por
capítulo" — cada capítulo MUST cerrar con su sección Fuentes. Añadir requisito +
relajar estándares = MINOR.

Modified standards (Estándares editoriales):
- Plantilla de capítulo: MUST → SHOULD; checklist/“qué hacer” centralizable por adendas.
- Cajas visuales: obligatorias → SHOULD según sector.
- Principio II: la salida operativa por capítulo pasa a SHOULD condicional.

Added standards:
- "Fuentes por capítulo" (MUST): trazabilidad de fuentes al cierre de cada capítulo.

Historial previo
----------------
Version change: 1.2.0 → 1.2.1
Bump rationale: PATCH — aclaración, sin redefinir ningún principio. (1) El
Principio III precisa que el "tono" se calibra una vez por guía en las adendas del
proyecto (no campo a campo en cada brief); el brief lo refleja como eco. El brief
sigue exigiendo las mismas dimensiones. (2) Se documenta el modelo núcleo + adendas
+ bases de sector en "Arquitectura del framework". No se añade ni elimina principio,
no se invalidan guías: PATCH, no MINOR.

Modified principles:
- III. Brief obligatorio — el campo "tono" se declara en las adendas (constitución
  § Adendas) vía /speckit-constitution; el brief lo refleja. Sigue NO NEGOCIABLE.

Added sections:
- "Arquitectura del framework" § Núcleo y adendas — formaliza la separación entre
  el núcleo universal (versionado) y la capa por guía (adendas), con bases de
  sector para los valores por defecto.

Historial previo
----------------
Version change: 1.1.0 → 1.2.0
Bump rationale: MINOR — se añade un principio nuevo (VI. Neutralidad de agente y
modelo) y se expande materialmente el Principio V para fijar el modelo de
ejecución de la revisión (3 pasadas locales por capítulo + 1 global) sin eliminar
ninguna de sus cinco dimensiones. No hay redefinición incompatible ni se invalidan
guías publicadas, por lo que no procede MAJOR; se añade material normativo, por lo
que no es PATCH.

Modified principles:
- V. Revisión multi-pasada — sigue NO NEGOCIABLE y conserva las cinco dimensiones,
  pero su ejecución pasa de "cinco pasadas secuenciales" a "3 locales por capítulo
  + 1 global". Las dimensiones siguen siendo verificaciones obligatorias.

Added sections:
- VI. Neutralidad de agente y modelo (NO NEGOCIABLE) — el pipeline MUST poder
  ejecutarse con cualquier agente y modelo; la lógica vive en comandos y
  referencias neutrales (no en skills de un proveedor) y lo determinista en
  scripts.

Otros cambios:
- "Arquitectura del framework" § Distribución: el empaquetado canónico es un preset
  de Spec Kit (plantillas + comandos + scripts + referencias); install.sh queda
  legacy.
- "Flujo de producción editorial con Spec Kit": referencia a los comandos
  editoriales del preset y al modelo 3+1.

Templates:
- ✅ updated  .specify/templates/* — ya en modo dual editorial/software.
- ✅ updated  .specify/memory/constitution.md — este archivo.

Follow-up TODOs:
- Verificar que `specify preset add` copie `writeonmars/references/`.
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
- Cada capítulo SHOULD ofrecer una salida operativa ("Qué hacer en la práctica",
  checklist, plantilla, síntoma → causa probable) cuando el tema tiene acción
  accionable real. Las adendas del proyecto declaran si esta salida es obligatoria
  por capítulo o se centraliza (p. ej. el sector tecnología la deja opcional por
  capítulo y centraliza el checklist en el cierre y los anexos).
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
   declaradas). Se calibra **una vez por guía en las adendas del proyecto**
   (constitución § Adendas, vía `/speckit-constitution`), no campo a campo en
   cada brief: el brief lo refleja como eco. Es lo único del brief que es
   normativo y por eso vive en la constitución, no en `spec.md`.
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
sin verificar las cinco dimensiones de revisión:

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

**Modelo de ejecución**: las cinco dimensiones se verifican en cuatro pasadas, no
en cinco secuenciales:

- **3 pasadas locales por capítulo**: estructura + utilidad (dimensiones 1 y 2),
  naturalidad (3) y precisión (4). Voz y precisión MUST mantenerse en pasadas
  separadas: reescribir prosa y contrastar datos son tareas opuestas que se
  degradan al mezclarse.
- **1 pasada global** sobre la obra: formato (dimensión 5) y coherencia entre
  capítulos (sin contradicciones ni redefiniciones de términos, glosario
  consolidado, referencias cruzadas).

Las pasadas se registran en `findings.md` con la numeración de dimensión del
contrato `pass-output-schema` (1 estructura, 2 utilidad, 3 naturalidad, 4 precisión,
5 formato), coherente con el `signing_matrix` del manifiesto.

Cada pasada MUST registrar su cumplimiento en `findings.md` conforme al contrato
`pass-output-schema` y en una checklist firmada (humano o agente declarado), que
vive en `checklists/[###-feature]/`. Las pasadas MAY ejecutarse de forma autónoma
marcando incidencias (`flagged`); la `signing_matrix` del manifiesto declara cuáles
exigen firma humana. El control humano se concentra en los dos checkpoints (el
brief del Principio III y la revisión del PDF anotado al cierre). Un hallazgo
`critico` abierto bloquea el cierre.

**Razón**: la revisión general "a ojo" no detecta los modos de fallo recurrentes
de la prosa generada con IA. Separar las dimensiones evita que defectos de un
dominio (p.ej. naturalidad) contaminen la evaluación de otro (p.ej. precisión);
agruparlas en 3 locales + 1 global baja coste y detecta los fallos temprano sin
perder ninguna verificación.

### VI. Neutralidad de agente y modelo (NO NEGOCIABLE)

El pipeline editorial MUST poder ejecutarse con cualquier agente y cualquier
modelo, no solo Claude, porque distintos agentes irán lanzando los pasos.

Reglas obligatorias:

- La lógica del método MUST vivir en **comandos** del preset y en **referencias**
  neutrales de modelo (voz, didáctica, método), no en skills propias de un único
  proveedor. Ningún comando MUST depender del autodisparo de skills de un agente
  concreto.
- Lo determinista (estado, export, feedback, cierre, memoria) MUST vivir en
  **scripts** reproducibles, no en prosa del agente.
- Las instrucciones que dependen del agente (rutas, formato de hooks) MUST
  aislarse y no contaminar los comandos de redacción.
- El contrato operativo para el agente vive en el `AGENTS.md` del preset y MUST
  respetarse con independencia del modelo.

**Razón**: si el método solo corre en un proveedor, el pipeline automatizado queda
atado a él. La neutralidad es lo que permite orquestar la producción con el modelo
que convenga en cada paso.

## Estándares editoriales

Restricciones materiales aplicables a todo artefacto del framework:

- **Plantilla de capítulo**: cada capítulo SHOULD seguir el patrón "Problema real →
  Idea clave → Por qué importa → Cómo funciona → Ejemplo → Error frecuente → Qué
  hacer en la práctica → Puente al siguiente capítulo". El checklist y la salida
  "Qué hacer en la práctica" pueden centralizarse u omitirse por capítulo cuando
  las adendas del proyecto lo declaren. La estructura concreta del capítulo la fija
  la base del sector (p. ej. `references/sectores/tecnologia.md`).
- **Fuentes por capítulo**: cada capítulo MUST cerrar con una sección "Fuentes"
  que nombre las fuentes citadas en ese capítulo (nombre, enlace y fecha cuando
  aplique), además del research consolidado. Es trazabilidad por capítulo, no solo
  un research.md central. Esta sección se **valida/deriva** contra `claims.md`
  (atribución por afirmación): la escribe la Redactora y `export.py` comprueba que
  ninguna afirmación `sin_fuente`/`contradicho` llegue al PDF sin marca.
- **Atribución por afirmación** (pasada 4): cada afirmación verificable de un
  capítulo MUST quedar registrada en `claims.md` (ClaimRecord v1.0) con su(s)
  cita(s) y el veredicto de relación (apoya/matiza/contradice/menciona). De ahí se
  deriva un **índice de factualidad** determinista (`status.py`), gate de cierre
  opcional vía `manifest.quality_gates`. El juicio vive en la referencia de la
  pasada 4; el conteo, en el script (Principio VI).
- **Cajas visuales**: las cajas "Quédate con esto", "Qué hacer mañana" o "Síntoma →
  causa probable" SHOULD usarse cuando aportan, y las adendas del proyecto declaran
  si alguna es obligatoria por capítulo. Algunos sectores (médico, veterinario) se
  benefician de "Síntoma → causa probable"; otros (tecnología) las omiten. No son
  obligatorias por defecto.
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
   las checklists de las pasadas (3 locales + 1 global) firmadas o registradas en
   `findings.md` antes de cerrar la rama.
6. **`/speckit-analyze`** → audita consistencia entre brief, plan y tareas.
   MUST ejecutarse antes de pasar a `implement` cuando la guía completa supere
   un capítulo.

El preset `writeonmars` materializa estos pasos como comandos editoriales
neutrales de modelo (`speckit.specify`, `speckit.research`, `speckit.plan`,
`speckit.implement`, `speckit.review`) más scripts deterministas (`status`,
`export`, `feedback`, `close`, `memory`). Es la vía de ejecución canónica; los
comandos core de Spec Kit siguen disponibles.

Las extensiones Git registradas en `.specify/extensions.yml` permanecen activas:
los hooks de auto-commit aplican igual a artefactos editoriales que a código.

## Arquitectura del framework

Write.OnMars se materializa como un conjunto de extensiones instalables sobre un
proyecto editorial nuevo. Esta sección codifica las decisiones de arquitectura
que sostienen los cinco principios.

**Núcleo y adendas**:

- La constitución de cada guía tiene dos capas. El **núcleo** (este documento:
  Principios I–VI, estándares, gobernanza) es universal y se rige por versión: NO
  se edita por guía. Garantiza que toda guía comparta la voz y el método.
- Las **adendas del proyecto** son la capa por guía, en su propia sección
  (`## Adendas del proyecto`) al final de `.specify/memory/constitution.md`.
  Recogen lo normativo que sí varía: sector, tono calibrado, contrato
  terminológico, anglicismos admitidos, matices léxicos, relajaciones y
  gobernanza. Las fija `/speckit-constitution` (primer paso del ciclo) y la
  revisión las verifica. Ninguna adenda MUST debilitar un principio NO NEGOCIABLE.
- Las **bases de sector** (`references/sectores/<slug>.md`) proponen los valores
  por defecto de las adendas según el dominio (tecnología, veterinaria, medicina,
  ciencia, humanidades, literatura…). Son ampliables: añadir un sector es crear su
  archivo. El brief (`spec.md`) queda para lo descriptivo (audiencia, problema,
  ejemplo recurrente); las adendas, para lo normativo por guía.

**Distribución**:

- El framework MUST distribuirse como un **preset de Spec Kit** (`specify preset
  add`) que empaqueta plantillas, comandos, scripts y referencias neutrales de
  modelo; opcionalmente servidores MCP. La lógica editorial MUST vivir en comandos
  y referencias, no en skills de un proveedor (Principio VI). Ninguna funcionalidad
  editorial nuclear MUST depender de modificaciones del agente subyacente.
  `install.sh` queda como vía legacy.
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

**Version**: 1.4.0 | **Ratified**: 2026-05-06 | **Last Amended**: 2026-06-21
