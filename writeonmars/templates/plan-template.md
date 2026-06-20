# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: Este template lo rellena el comando `/speckit-plan`. El comportamiento
condicional según `project_type` (ver `.writeonmars-manifest.json`):

- `editorial`: las secciones "Temario" y "Descripciones encadenadas" son
  obligatorias (FR-010); el "Constitution Check" verifica los cinco principios
  editoriales.
- `software` (default Spec Kit): omite las secciones editoriales; el
  "Constitution Check" verifica los principios técnicos del proyecto.
- `mixed`: rellena ambas zonas.

## Summary

[Extracto de la spec: requisito primario + enfoque técnico desde la
investigación.]

## Technical Context

<!--
  ACTION REQUIRED: Reemplaza esta sección por los detalles técnicos reales del
  proyecto. La estructura es orientativa.
-->

**Language/Version**: [ej. Python 3.11, Swift 5.9, Rust 1.75 o NEEDS CLARIFICATION]  
**Primary Dependencies**: [ej. FastAPI, UIKit, LLVM o NEEDS CLARIFICATION]  
**Storage**: [si aplica, ej. PostgreSQL, CoreData, ficheros o N/A]  
**Testing**: [ej. pytest, XCTest, cargo test o NEEDS CLARIFICATION]  
**Target Platform**: [ej. Linux server, iOS 15+, WASM o NEEDS CLARIFICATION]
**Project Type**: [ej. library / cli / web-service / mobile-app / compiler / desktop-app / **editorial** o NEEDS CLARIFICATION]  
**Performance Goals**: [ej. 1000 req/s, 10k lines/sec, 60 fps o NEEDS CLARIFICATION]  
**Constraints**: [ej. <200ms p95, <100MB memory, offline-capable o NEEDS CLARIFICATION]  
**Scale/Scope**: [ej. 10k users, 1M LOC, 50 screens o NEEDS CLARIFICATION]

## Constitution Check

*GATE: debe pasar antes de Phase 0 research. Re-evaluar después de Phase 1
design.*

<!--
  La tabla siguiente verifica conformidad con los cinco principios editoriales
  (constitución v1.3.0). Cuando `project_type=software`, sustituye o amplía
  esta tabla con los principios técnicos del proyecto.
-->

| Principio | Conformidad | Evidencia |
|-----------|-------------|-----------|
| **I. Voz natural y sobria** (NO NEGOCIABLE) | [pasa / desviación justificada] | [Frases comprimidas evitadas, transiciones explicadas, ausencia de eslóganes. Apunta secciones del plan donde se garantiza.] |
| **II. Estructura situación → explicación → consecuencia** | [pasa / desviación justificada] | [Cada capítulo del temario aplica la estructura de capítulo que fije la base del sector (references/sectores/). Listar excepciones aquí.] |
| **III. Brief obligatorio** (NO NEGOCIABLE) | [pasa / desviación justificada] | [Brief (8 campos descriptivos; tono en las adendas) archivado en `specs/[###-feature]/spec.md` y citado en este plan. Confirmar campos críticos sin `[NEEDS CLARIFICATION]`.] |
| **IV. Precisión léxica y arquitectura sintáctica** | [pasa / desviación justificada] | [Glosario inicial, anglicismos justificados, univocidad terminológica garantizada en las descripciones encadenadas.] |
| **V. Revisión multi-pasada** (NO NEGOCIABLE) | [pasa / desviación justificada] | [Cinco pasadas declaradas como tareas en `tasks.md`; matriz de firmas alineada con `.writeonmars-manifest.json`.] |

Cualquier desviación MUST registrarse en `Complexity Tracking` con justificación
operativa (FR-011).

## Temario *(modo editorial — obligatorio)*

<!--
  Cobertura: FR-010, data-model § 4. Cada capítulo es secuencial empezando en 1.
  La columna `estructura_aplicada` debe ser siempre `didactica_v1` (la del
  Principio II).
-->

| Número | Título | Promesa | Estructura aplicada |
|--------|--------|---------|---------------------|
| 1 | [Título claro, sin emoji] | [Una frase declarando qué resuelve este capítulo.] | didactica_v1 |
| 2 | [Título] | [Promesa.] | didactica_v1 |
| 3 | [Título] | [Promesa.] | didactica_v1 |
| ... | ... | ... | didactica_v1 |

## Descripciones encadenadas *(modo editorial — obligatorio)*

<!--
  Cobertura: FR-010, SC-005, data-model § 5. Una entrada por capítulo. Las
  conexiones `null` solo se permiten en el primer capítulo (`conexion_anterior`)
  y en el último (`conexion_siguiente`).
-->

### Capítulo 1 — [Título]

- **Promesa específica**: [Refina la promesa del temario para este capítulo.]
- **Conexión anterior**: `null` (primer capítulo).
- **Conexión siguiente**: [Cómo prepara el capítulo 2.]
- **Ejemplo recurrente aplicado**: [Cómo se usa el ejemplo del brief en este capítulo.]
- **Conceptos introducidos**: [Lista de términos nuevos que entran al glosario.]

### Capítulo 2 — [Título]

- **Promesa específica**: [...]
- **Conexión anterior**: [Recoge / amplía qué del capítulo 1.]
- **Conexión siguiente**: [Prepara qué del capítulo 3.]
- **Ejemplo recurrente aplicado**: [...]
- **Conceptos introducidos**: [...]

### Capítulo N — [Título]

- **Promesa específica**: [...]
- **Conexión anterior**: [...]
- **Conexión siguiente**: `null` (último capítulo).
- **Ejemplo recurrente aplicado**: [...]
- **Conceptos introducidos**: [...]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # Este archivo (output de /speckit-plan)
├── research.md          # Output Phase 0 (/speckit-plan)
├── data-model.md        # Output Phase 1 (/speckit-plan) — modo software
├── glossary.md          # Output Phase 1 (/speckit-plan) — modo editorial
├── quickstart.md        # Output Phase 1 (/speckit-plan)
├── contracts/           # Output Phase 1 (/speckit-plan)
├── findings.md          # Output durante /speckit-implement — modo editorial
└── tasks.md             # Output Phase 2 (/speckit-tasks)
```

### Source Code (repository root) / Editorial output (repository root)

<!--
  ACTION REQUIRED: Reemplaza el árbol siguiente por el layout concreto.
  Borra opciones no usadas y expande la estructura elegida.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT modo software)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (cuando se detecta "frontend" + "backend")
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (cuando se detecta "iOS/Android")
api/
└── [igual al backend]

ios/ or android/
└── [estructura específica de la plataforma]

# [REMOVE IF UNUSED] Option 4: Editorial (modo editorial)
chapters/
├── 001-titulo.md
├── 002-titulo.md
└── ...

glossary.md              # Glosario consolidado del proyecto.
index.md                 # Ruta de lectura.
common-errors.md         # Errores comunes agregados.
templates/               # Plantillas reutilizables que la guía expone.
checklists/[###-feature]/
├── pasada-1.md
├── pasada-2.md
├── pasada-3.md
├── pasada-4.md
└── pasada-5.md
```

**Structure Decision**: [Documenta la estructura elegida y referencia los
directorios reales capturados arriba.]

## Complexity Tracking

> **Rellenar SOLO si el Constitution Check tiene desviaciones que justificar.**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [ej. cuarto proyecto] | [necesidad actual] | [por qué tres proyectos no bastan] |
| [ej. Repository pattern] | [problema concreto] | [por qué acceso directo a DB no basta] |
| [ej. desviación de la matriz de firmas] | [proyecto interno; pasada 4 firmable autónoma] | [recuperar firma humana retrasaba dos semanas] |
