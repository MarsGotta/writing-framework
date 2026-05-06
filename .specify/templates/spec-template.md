<!-- writeonmars-brief consume este template cuando project_type=editorial. El modo software conserva la estructura clásica de Spec Kit; el modo editorial añade el brief obligatorio del Principio III y reinterpreta "User Stories" como "Trayectos de lector". -->

# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

<!--
  El comportamiento de este template depende de `project_type` declarado en
  `.writeonmars-manifest.json` (campo opcional `project_type`):

  - `editorial`: el brief de nueve campos del Principio III es OBLIGATORIO.
    "User Stories" se renombra como "Trayectos de lector" (sync impact
    constitución v1.1.0).
  - `software` (default Spec Kit): conserva "User Stories" tal cual.
  - `mixed`: rellena ambas secciones.

  El comando `/speckit-specify` (o la skill `writeonmars-brief` cuando esté
  activa) debe eliminar la sección que no aplique al proyecto.
-->

## Brief editorial *(modo editorial — obligatorio)*

<!--
  Esta sección materializa el Principio III de la constitución (FR-005). Los
  nueve campos son obligatorios. Ningún campo MUST contener marcadores
  `[NEEDS CLARIFICATION]` cuando se cierre la spec; mientras existan, el avance
  a `/speckit-plan` queda bloqueado por FR-006 en los campos críticos
  (audiencia, ejemplo recurrente, resultado esperado).

  Esquema completo en `specs/001-framework-architecture/data-model.md` § 1.
-->

### 1. Audiencia

<!-- Mínimo 20 caracteres. Quién lee. -->

[Describe a la persona lectora con detalle: rol, nivel de experiencia, contexto de trabajo, herramientas habituales.]

### 2. Problema

<!-- Mínimo 30 caracteres. Qué le pasa hoy a la persona lectora. -->

[Describe el problema concreto que la guía resuelve. Sin generalidades.]

### 3. Resultado esperado

<!-- Sin `[NEEDS CLARIFICATION]`. Qué podrá hacer la persona lectora al terminar. -->

[Acción o capacidad demostrable que se gana al leer la guía completa.]

### 4. Nivel

<!-- Enum: principiante | intermedio | avanzado. Selecciona uno. -->

[principiante | intermedio | avanzado]

### 5. Tono

<!-- Declarar variantes admitidas: experto / directo / natural / sobrio. -->

[Lista de variantes permitidas en la guía. La constitución § I exige sobriedad como base.]

### 6. Conceptos obligatorios

<!-- Lista cerrada, mínimo un elemento. Cada concepto entrará al glosario. -->

- [Concepto 1]
- [Concepto 2]
- [Concepto 3]

### 7. Ejemplo recurrente

<!--
  Sin `[NEEDS CLARIFICATION]`. El ejemplo se reutilizará durante toda la guía
  (constitución § II + SC-005). Describe los cinco subcampos.
-->

- **Contexto**: [Situación de partida del ejemplo.]
- **Objetivo**: [Qué intenta lograr la persona protagonista del ejemplo.]
- **Restricción**: [Limitaciones reales del caso.]
- **Riesgo**: [Qué sale mal si no se aplica la guía.]
- **Resultado esperado**: [Qué se obtiene al aplicar la guía.]

### 8. Riesgos

<!-- Malentendidos a evitar durante la lectura. Lista. -->

- [Malentendido frecuente 1.]
- [Malentendido frecuente 2.]

### 9. Acciones prácticas

<!-- Qué podrá hacer la persona lectora al terminar. Lista, ≥ 1 elemento. -->

- [Acción concreta 1.]
- [Acción concreta 2.]

---

## Trayectos de lector *(modo editorial)* / User Stories *(modo software)*

<!--
  IMPORTANT: Cada trayecto de lector / user story debe estar PRIORIZADO y ser
  INDEPENDIENTEMENTE TESTABLE.

  - Modo editorial: cada "Trayecto de lector" describe un recorrido lectivo
    completo (capítulos consultados, preguntas que responde, decisión que toma).
  - Modo software: cada "User Story" describe un journey de usuario.

  Asigna prioridades (P1, P2, P3...) donde P1 es el más crítico.
-->

### Trayecto de lector 1 / User Story 1 - [Brief Title] (Priority: P1)

[Modo editorial: describe el recorrido lectivo. Modo software: describe el user journey.]

**Why this priority**: [Por qué este trayecto / story va primero.]

**Independent Test**: [Cómo se valida sin depender de los otros trayectos / stories.]

**Acceptance Scenarios**:

1. **Given** [estado inicial], **When** [acción], **Then** [resultado esperado]
2. **Given** [estado inicial], **When** [acción], **Then** [resultado esperado]

---

### Trayecto de lector 2 / User Story 2 - [Brief Title] (Priority: P2)

[Modo editorial: describe el segundo recorrido lectivo. Modo software: el segundo user journey.]

**Why this priority**: [Justificación.]

**Independent Test**: [Cómo testearlo.]

**Acceptance Scenarios**:

1. **Given** [estado inicial], **When** [acción], **Then** [resultado esperado]

---

### Trayecto de lector 3 / User Story 3 - [Brief Title] (Priority: P3)

[Tercer recorrido / journey.]

**Why this priority**: [Justificación.]

**Independent Test**: [Cómo testearlo.]

**Acceptance Scenarios**:

1. **Given** [estado inicial], **When** [acción], **Then** [resultado esperado]

---

[Añade más trayectos / stories según necesidad, cada uno con su prioridad.]

### Edge Cases

<!--
  ACTION REQUIRED: Reemplaza estos placeholders por los edge cases reales.
  En modo editorial, considera: lectores que entran por la mitad, lectores que
  saltan capítulos, términos sin glosario, ejemplo recurrente que no aplica.
-->

- ¿Qué ocurre cuando [boundary condition]?
- ¿Cómo gestiona el sistema [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: Rellena con los requisitos funcionales reales.
-->

### Functional Requirements

- **FR-001**: System MUST [capacidad concreta, ej. "validar el brief de nueve campos antes de planificar"]
- **FR-002**: System MUST [capacidad concreta]
- **FR-003**: Users MUST be able to [interacción clave]
- **FR-004**: System MUST [requisito de datos]
- **FR-005**: System MUST [comportamiento]

*Ejemplo de marcado de requisitos no resueltos:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [Qué representa, atributos clave sin implementación.]
- **[Entity 2]**: [Qué representa, relaciones con otras entidades.]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define criterios medibles, agnósticos de tecnología.
  En modo editorial, prioriza métricas auditables: cobertura del glosario,
  presencia del ejemplo recurrente, hallazgos críticos por pasada.
-->

### Measurable Outcomes

- **SC-001**: [Métrica medible.]
- **SC-002**: [Métrica medible.]
- **SC-003**: [Métrica de éxito de la persona lectora / usuaria.]
- **SC-004**: [Métrica de impacto, ej. cobertura del glosario.]

## Assumptions

<!--
  ACTION REQUIRED: Lista las suposiciones razonables que se hicieron al
  redactar la spec.
-->

- [Suposición sobre la audiencia / usuarios.]
- [Suposición sobre alcance, ej. "compilación a PDF queda fuera de v1".]
- [Suposición sobre el entorno o las herramientas existentes.]
- [Dependencia de un sistema externo.]
