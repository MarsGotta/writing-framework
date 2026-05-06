# Phase 0 Research: Arquitectura del harness Write.OnMars

**Feature**: 001-framework-architecture | **Date**: 2026-05-06

Este documento resuelve las decisiones técnicas que el plan deja "fijas" antes de pasar a Phase 1 (data model, contratos y quickstart). Cada decisión sigue el formato Decision / Rationale / Alternatives / Coverage.

---

## R1. Mecanismo de instalación: script Bash con detección de Spec Kit existente

**Decision**: el comando de instalación se implementa como un script Bash (`install/install.sh`) ejecutable directamente o invocable desde una skill `writeonmars-install`. El script verifica precondiciones (Git, Bash 5+), detecta si el repositorio destino ya tiene Spec Kit instalado, copia la constitución, las plantillas adaptadas, las skills bundled, registra los hooks Git y dispara un cuestionario interactivo para generar el manifiesto y el archivo de contexto del agente.

**Rationale**:

- Spec Kit ya se instala con un esquema basado en scripts Bash (`.specify/scripts/bash/*.sh`); replicar la misma cultura reduce fricción cognitiva para mantenedores.
- Bash es el común denominador en macOS/Linux y no introduce dependencias adicionales (Node, Python global, etc.). El módulo opcional `writeonmars-research` (FR-009b) sí requiere Python, pero solo cuando un proyecto lo activa.
- Permite invocación tanto desde una skill como desde el shell directamente (`bash install/install.sh`), lo que sirve a operadores humanos y a agentes por igual.

**Alternatives considered**:

- **Binario compilado** (Go/Rust). Descartado: introduce un binario que mantener por plataforma; el framework es texto + scripts, no requiere binarios.
- **CLI Node/npm** (`npx writeonmars init`). Descartado: añade dependencia de Node y no aporta sobre Bash en este caso.
- **Plugin nativo de Spec Kit**. Aún no existe un mecanismo formal de plugins en Spec Kit más allá de `.specify/extensions/`, así que la integración real ya pasa por scripts y hooks; el script es esencialmente un instalador de extensiones Spec Kit.

**Coverage**: FR-001, FR-002, FR-003, FR-004, SC-001 (instalación <5 min).

---

## R2. Distribución de skills bundled: copia por defecto, `--symlink` opcional

**Decision**: el script de instalación copia las skills bundled (`/marcela-prose`, `/technical-guide-design`, todas las `writeonmars-*`) desde el repositorio canónico al directorio `.claude/skills/` (o equivalente del agente) del proyecto destino. Acepta un flag opcional `--symlink` que crea enlaces simbólicos en lugar de copias para casos de desarrollo local.

**Rationale**:

- La opción A elegida en clarificación (empaquetar) implica que el repo canónico es la fuente de verdad. Copiar archivos es la implementación más simple y predecible: el proyecto destino queda autónomo y las actualizaciones son explícitas.
- El flag `--symlink` cubre el caso de un mantenedor que desarrolla skills localmente y prueba en un proyecto piloto sin tener que repetir el `install`.
- Las copias respetan el principio de la constitución de "fuente de verdad = repositorio del proyecto" (FR-021): el proyecto editorial puede operar offline y reproducir su producción incluso si el repo canónico desaparece.

**Alternatives considered**:

- **Submódulo Git**. Descartado: complica el flujo del operador (clone con `--recurse-submodules`, sync explícito) y nubla la versión exacta de cada skill.
- **Subtree Git**. Descartado: facilita la sincronización pero arrastra historia ajena al proyecto editorial.
- **Paquete versionado** (npm/pip/brew). Descartado para v1: no aporta sobre la copia mientras Write.OnMars no se publique fuera del entorno controlado.

**Coverage**: FR-027, FR-028.

---

## R3. Contrato de citación: Markdown narrativo + JSON Schema mínimo

**Decision**: el contrato FR-009a se publica como un documento Markdown (`docs/citation-contract.md` y espejo en `contracts/citation-contract.md`) con la especificación narrativa, ejemplos y casos límite, acompañado de un `contracts/citation-record.schema.json` que define la forma exacta de cada cita registrada. Cualquier MCP que produzca records conformes al JSON Schema se considera compatible.

**Rationale**:

- El contrato es a la vez documentación humana (qué significa cada campo, cómo elegir tipo) e interfaz máquina (validación automática). Markdown cubre el primer caso, JSON Schema el segundo.
- Permite el modo BYOM (FR-009 + FR-009b): cualquier proveedor de MCP puede leer el Markdown, mapear su salida al schema y declararse compatible sin coordinación con el equipo del framework.
- El versionado se gestiona con el campo `contract_version` en cada record; los proyectos declaran en el manifiesto qué versión soportan (FR-027).

**Alternatives considered**:

- **Solo Markdown**, sin JSON Schema. Descartado: dificulta validar automáticamente las salidas de MCPs externos en la pasada 4 (precisión).
- **OpenAPI / GraphQL schema**. Descartado: el contrato no describe un servicio en red; describe el formato de un record de cita. JSON Schema es la herramienta adecuada.
- **Implementación implícita** (cada skill define su propio formato). Descartado: violaría el espíritu de FR-009a (uniformidad de citación entre proyectos y MCPs).

**Coverage**: FR-009a, FR-009b, FR-016, FR-027.

---

## R4. Delegación a sub-agentes: Claude Code Agent tool con prompts canónicos por pasada

**Decision**: las skills `writeonmars-redaccion`, `writeonmars-pasada-1` ... `writeonmars-pasada-5` y `writeonmars-contraste` despachan sub-agentes invocando el Agent tool de Claude Code (subagent_type apropiado según contexto: `general-purpose` por defecto, `Plan` para diseño de capítulo si aplica). Cada skill incluye un prompt canónico con: rol del sub-agente, archivos que debe leer, skills permitidas, formato de salida esperado y criterios de aceptación. Las dependencias específicas de Claude Code se aíslan en el directorio `agents/claude/` para preservar la portabilidad declarada por FR-023 / FR-024.

**Rationale**:

- Claude Code (agente prioritario v1) ya expone un Agent tool con `subagent_type` estándar; los sub-agentes reciben contexto fresco, lo que cumple el requisito de "el sub-agente no hereda el contexto de redacción previo" (FR-018, decisión Q4).
- Centralizar los prompts canónicos en cada skill garantiza que la pasada se reproduzca igual en distintos proyectos y permite versionarlos junto con la skill (FR-027).
- La portabilidad a otros agentes (Codex, Cursor) se aborda en una feature posterior duplicando el adaptador de despacho en `agents/<name>/`; las skills nucleares no cambian.

**Alternatives considered**:

- **Sesiones humanas separadas por pasada**. Descartado: contradice la automatización requerida y SC-006 (paralelización ≥40%).
- **Despacho a través de MCP custom**. Considerado para portabilidad pero añade complejidad; el Agent tool nativo basta para v1.
- **Un único agente que ejecuta las cinco pasadas en serie sin reset**. Descartado en clarificación Q4 (opción A rechazada explícitamente por sesgo de "ya conozco este texto").

**Coverage**: FR-013, FR-014, FR-015, FR-018, FR-023, FR-024.

---

## R5. Esquema del manifiesto del proyecto

**Decision**: el manifiesto vive en `.writeonmars-manifest.json` en la raíz del proyecto editorial. Esquema mínimo:

```json
{
  "framework_version": "1.0.0",
  "constitution_version": "1.1.0",
  "agent_target": "claude-code",
  "language_primary": "es",
  "skills": [
    {"name": "marcela-prose", "version": "x.y.z", "source": "bundled"},
    {"name": "technical-guide-design", "version": "x.y.z", "source": "bundled"},
    {"name": "writeonmars-research", "version": "x.y.z", "source": "bundled"}
  ],
  "research_mode": "byom",
  "signing_matrix": {
    "pasada_1_estructura": "autonomous",
    "pasada_2_utilidad": "autonomous",
    "pasada_3_naturalidad": "human",
    "pasada_4_precision": "human",
    "pasada_5_formato": "autonomous"
  },
  "human_operators": [
    {"id": "marcela", "email": "marcelagotta@gmail.com", "role": "editor"}
  ],
  "citation_contract_version": "1.0"
}
```

El JSON Schema completo vive en `contracts/manifest-schema.json` (Phase 1).

**Rationale**:

- Un manifiesto JSON único permite a las skills (especialmente las pasadas y el cierre de proyecto) leer su política con `jq` o cualquier parser sin dependencias.
- El campo `signing_matrix` materializa la decisión Q3 (D con default B): cualquier desviación del default queda visible en el commit que tocó el manifiesto, lo que satisface FR-004 y FR-020a.
- La lista de skills versionadas cubre FR-027 (reproducibilidad).
- `research_mode: byom | bundled` cubre la dualidad de la decisión D1 (FR-009b).

**Alternatives considered**:

- **YAML**. Descartado: más legible para humanos pero los hooks Git y el script de instalación ya consumen JSON (`.specify/feature.json`); mantener el formato unifica la stack.
- **Manifiesto distribuido por carpeta** (un fichero por feature). Descartado: complica la consolidación de versiones y el cierre del proyecto.

**Coverage**: FR-004, FR-020a, FR-022, FR-027.

---

## R6. Estrategia de testing: smoke shell + guía piloto editorial

**Decision**: el framework valida v1 con dos capas:

1. **Smoke tests en Bash** (`tests/smoke/`) que cubren los acceptance scenarios mecánicos de US1: instalación sobre repo vacío, preservación de `CLAUDE.md` previo y disponibilidad inmediata de `/speckit-specify` después del install.
2. **Guía piloto editorial** (`tests/editorial-pilot/`) que produce manualmente una guía de tres capítulos sobre un tema acotado y verifica end-to-end que las cinco pasadas pasan, los hallazgos se generan correctamente y el manifiesto refleja firmas humanas en pasadas 3 y 4. Esta capa es manual con apoyo del agente; los resultados se archivan como evidencia en `tests/editorial-pilot/evidence/`.

**Rationale**:

- La verificación funcional de un harness editorial no se puede reducir a unit tests: la calidad final depende de juicio humano sobre prosa. La guía piloto es la única forma honesta de validar US2 y SC-002 / SC-003 / SC-004 / SC-005.
- Los smoke tests automatizan lo automatizable (instalación, archivos creados, hooks registrados), reduciendo regresiones cuando el script de install evoluciona.
- Mantener evidencia archivada habilita revisiones bianuales (constitución § Governance) sin tener que reproducir cada guía.

**Alternatives considered**:

- **Solo smoke tests**. Descartado: no valida calidad editorial; v1 se daría por terminado sin haber producido nunca una guía completa.
- **Suite completa de unit tests** sobre las skills. Descartado: las skills son markdown narrativo; sus unit tests serían pruebas de prompt engineering que envejecen rápido.
- **Tests automáticos contra un agente real** en CI. Diferido: posible v2 cuando exista una matriz de agentes soportados con suficiente estabilidad.

**Coverage**: US1, US2, SC-001..SC-005, SC-009.

---

## Resumen de decisiones

| Ref | Decisión | FR/SC cubiertas |
|-----|----------|-----------------|
| R1  | Instalación vía script Bash con detección de Spec Kit | FR-001..FR-004, SC-001 |
| R2  | Skills bundled distribuidas por copia (`--symlink` opcional) | FR-027, FR-028 |
| R3  | Contrato de citación = Markdown + JSON Schema | FR-009a, FR-009b, FR-016, FR-027 |
| R4  | Sub-agentes vía Agent tool de Claude Code; portabilidad por adaptador | FR-013..FR-018, FR-023, FR-024 |
| R5  | Manifiesto JSON único con `signing_matrix` y skills versionadas | FR-004, FR-020a, FR-022, FR-027 |
| R6  | Testing = smoke shell + guía piloto editorial archivada | US1, US2, SC-001..SC-005, SC-009 |

Sin `NEEDS CLARIFICATION` pendientes. Phase 1 puede arrancar.
