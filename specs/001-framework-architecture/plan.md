# Implementation Plan: Arquitectura y flujo de trabajo del harness Write.OnMars

**Branch**: `001-framework-architecture` | **Date**: 2026-05-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-framework-architecture/spec.md`

## Summary

Write.OnMars es un harness editorial que se distribuye como un repositorio canónico de assets (skills + servidores MCP opcionales + plugins + plantillas + hooks) y se instala sobre repositorios Spec Kit existentes. v1 produce guías técnicas en markdown a través de un flujo de ocho etapas: instalación → brief → contexto del proyecto → investigación con contrato de citación → temario → descripciones encadenadas → redacción capítulo a capítulo (delegada a sub-agentes) → contraste de información → revisión multi-pasada (cinco pasadas secuenciales con sub-agente fresco por pasada). Las pasadas 1, 2 y 5 cierran autónomamente; las pasadas 3 (naturalidad) y 4 (precisión) requieren firma humana por defecto.

El framework apoya el ciclo en dos skills existentes empaquetadas (`/marcela-prose` para voz/microestilo/limpieza LLM, `/technical-guide-design` para diseño didáctico) y desarrolla solo lo que falta: instalación, brief, investigación, contraste, orquestación de pasadas, sub-agentes y manifiesto. La fuente de verdad es siempre el repositorio del proyecto editorial; cualquier memoria externa es caché reconstruible.

## Technical Context

**Language/Version**: Bash 5+ (scripts de instalación e integración con Spec Kit), Markdown (skills, plantillas, salidas), YAML (configuración de extensiones y hooks), JSON (manifiestos de proyecto y outputs de pasada). Python 3.11+ opcional para el módulo `writeonmars-research` (FR-009b) cuando un proyecto lo active.
**Primary Dependencies**: Spec Kit (ciclo `/speckit-*`), agente compatible con skills/MCP (Claude Code v1), skills bundled `/marcela-prose` y `/technical-guide-design`, MCPs externos compatibles con el contrato de citación (modo BYOM por defecto: `context7`, web search, `fetch`).
**Storage**: sistema de archivos del proyecto editorial. Artefactos en markdown/JSON dentro del repo Git. Memoria vectorizada externa OPCIONAL (FR-022), nunca fuente de verdad.
**Testing**: smoke tests en Bash para los acceptance scenarios de instalación (US1); tests editoriales manuales sobre una guía piloto de tres capítulos (US2); validación de schemas JSON (manifiesto, citation contract, pass outputs) con `jq` o equivalente.
**Target Platform**: macOS y Linux con Bash 5+, Git ≥2.30 y un agente de IA con soporte de skills (Claude Code prioritario v1). Windows queda fuera de v1 hasta validar PowerShell scripts.
**Project Type**: harness editorial multi-componente. Combinación de (a) skills markdown distribuidas como assets, (b) servidor MCP opcional, (c) plantillas Spec Kit adaptadas, (d) hooks Git y (e) scripts de instalación.
**Performance Goals**: instalación inicial <5 minutos en interacción humana (SC-001); paralelización de redacción reduce tiempo total ≥40% sobre serial (SC-006).
**Constraints**: agnosticismo de agente para skills nucleares; idioma primario español; fuente de verdad = repo Git; cero dependencias rígidas a un MCP concreto.
**Scale/Scope**: v1 cubre guías técnicas de 1–20 capítulos. Manuales (secuencias de guías) y libros (≥10 capítulos) son agregaciones; artículos (1 capítulo) son caso límite. Producción simultánea de varios capítulos vía sub-agentes en paralelo (US3).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitución vigente: v1.1.0 (`.specify/memory/constitution.md`). Verificación principio a principio:

| Principio | Evidencia de cumplimiento en el plan | Status |
|-----------|---------------------------------------|--------|
| I. Voz natural y sobria (NO NEGOCIABLE) | Pasada 3 (naturalidad) delegada a `/marcela-prose` con sub-agente fresco (FR-018, US2 §4). Reglas microestilísticas embebidas en el archivo de contexto del proyecto (FR-007). | PASS |
| II. Estructura situación → explicación → consecuencia | Plantilla de capítulo aplicada por `/technical-guide-design` en redacción y pasadas 1–2 (FR-012, FR-014, FR-018). Cada capítulo termina en "Qué hacer en la práctica + checklist + puente" (KE Capítulo). | PASS |
| III. Brief obligatorio antes de redactar (NO NEGOCIABLE) | Brief obligatorio cubre los nueve campos (FR-005). Avance bloqueado si quedan `[NEEDS CLARIFICATION]` críticos (FR-006). Contexto del proyecto se deriva del brief (FR-007). | PASS |
| IV. Precisión léxica y arquitectura sintáctica integrada | Reglas de Cabré/RAE/Fundéu/AENOR aplicadas vía `/marcela-prose`. Glosario consolidado obligatorio (FR-021, KE Glosario; SC-004 = 100% cobertura). Detección de colisiones léxicas entre capítulos paralelos (FR-015). | PASS |
| V. Revisión multi-pasada antes de publicar (NO NEGOCIABLE) | Cinco pasadas secuenciales con sub-agente fresco por pasada (FR-018). Hallazgos accionables (FR-019). Cierre bloqueado por hallazgos críticos abiertos (FR-020) y por firmas humanas pendientes en pasadas 3 y 4 según matriz default (FR-020a). | PASS |

Estándares editoriales de la constitución también respetados: plantilla de capítulo (KE Capítulo + FR-012), cajas obligatorias (referenciadas desde la skill de redacción), estructura de guía completa (FR-029 + KE Index/Errores comunes/Plantillas), datos verificables (contrato de citación FR-009a + skill de contraste FR-016).

**Resultado del gate**: PASS sin violaciones. `Complexity Tracking` queda vacío.

## Project Structure

### Documentation (this feature)

```text
specs/001-framework-architecture/
├── plan.md              # Este archivo
├── research.md          # Phase 0 — decisiones técnicas resueltas
├── data-model.md        # Phase 1 — esquemas de entidades del framework
├── quickstart.md        # Phase 1 — primer uso del harness instalado
├── contracts/
│   ├── citation-contract.md       # Contrato FR-009a
│   ├── manifest-schema.json       # Esquema JSON del manifiesto del proyecto
│   └── pass-output-schema.md      # Formato de salida de cada pasada
├── checklists/
│   └── requirements.md  # Spec quality checklist (ya generado en /speckit-specify)
└── tasks.md             # Phase 2 output (creado por /speckit-tasks)
```

### Source Code (framework canonical repository)

Este plan describe la estructura del **repositorio canónico de Write.OnMars** (el repo donde se desarrolla el framework, el actual). Cuando el framework se instala sobre un proyecto editorial, una buena parte de esta estructura se replica/enlaza en el destino.

```text
writing-framework/   # Repositorio canónico (este repo)
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   └── checklist-template.md
│   └── extensions/
│       └── git/                          # Hooks de Spec Kit ya instalados
│
├── .claude/skills/                       # Skills bundled distribuidas con el framework
│   ├── marcela-prose/                    # Bundled (FR-028); voz/microestilo/limpieza LLM
│   ├── technical-guide-design/           # Bundled (FR-028); diseño didáctico
│   │
│   ├── speckit-*/                        # Skills nativas de Spec Kit (ya instaladas)
│   │
│   ├── writeonmars-install/              # FR-001..FR-004; comando de instalación
│   ├── writeonmars-brief/                # FR-005..FR-007; cuestionario y context build
│   ├── writeonmars-research/             # FR-008..FR-009b; orquestador de citación
│   ├── writeonmars-temario/              # FR-010 (envuelve /technical-guide-design)
│   ├── writeonmars-descripciones/        # FR-010 (envuelve /technical-guide-design)
│   ├── writeonmars-redaccion/            # FR-014..FR-015; despacha sub-agentes
│   ├── writeonmars-contraste/            # FR-016..FR-017; pasada 4 implementación
│   ├── writeonmars-pasada-1/             # Estructura (envuelve /technical-guide-design)
│   ├── writeonmars-pasada-2/             # Utilidad (envuelve /technical-guide-design)
│   ├── writeonmars-pasada-3/             # Naturalidad (envuelve /marcela-prose)
│   ├── writeonmars-pasada-4/             # Precisión (envuelve writeonmars-contraste)
│   ├── writeonmars-pasada-5/             # Formato (skill propia)
│   └── writeonmars-glossary/             # Consolidación + detección de colisiones (FR-015)
│
├── mcp/
│   └── writeonmars-research/             # FR-009b: módulo MCP opcional bundled
│       ├── server.py                     # Implementación de referencia
│       ├── pyproject.toml
│       └── README.md
│
├── install/
│   ├── install.sh                        # Entry point de instalación (FR-001)
│   └── lib/                              # Funciones reutilizables
│       ├── detect-existing.sh            # FR-003: detección y fusión
│       ├── copy-skills.sh                # FR-028: copia de skills bundled
│       ├── render-context.sh             # FR-002: cuestionario inicial
│       └── render-manifest.sh            # FR-004: generación del manifiesto
│
├── contracts/                            # Contratos canónicos publicados
│   ├── citation-contract.md              # Espejo del FR-009a publicado para terceros
│   ├── manifest-schema.json              # Espejo del manifiesto v1
│   └── pass-output-schema.md             # Formato de hallazgos
│
├── docs/
│   ├── installation.md                   # Guía de instalación para mantenedores
│   ├── citation-contract.md              # Documentación del contrato
│   ├── manifest-schema.md                # Documentación del manifiesto
│   ├── compatibility-matrix.md           # MCPs compatibles + agentes soportados
│   └── maintenance/
│       └── sync-from-vault.md            # Procedimiento de sincronización con Obsidian vault (FR-028)
│
├── resources/                            # Fuentes editoriales canónicas
│   ├── guia-IA-writing.md
│   └── Manual Maestro para la Producción de Textos Especializados.md
│
├── tests/
│   ├── smoke/
│   │   ├── install-on-empty-repo.sh      # US1 §AC1
│   │   ├── install-preserves-claudemd.sh # US1 §AC2
│   │   └── specify-after-install.sh      # US1 §AC3
│   └── editorial-pilot/
│       └── README.md                      # Plan de la guía piloto de 3 capítulos (US2)
│
├── CLAUDE.md                              # Contexto agente para el desarrollo del framework
├── README.md                              # Entrada al framework
└── specs/                                 # Specs del propio framework (incluye este 001)
```

**Estructura de un proyecto editorial instalado** (resultado de ejecutar `writeonmars-install` sobre un repo destino):

```text
my-guide-project/
├── .specify/                              # Spec Kit copiado o enlazado
├── .claude/skills/                        # Skills bundled copiadas (incluye /marcela-prose, /technical-guide-design, writeonmars-*)
├── .writeonmars-manifest.json             # FR-004: versiones, skills, matriz de firmas
├── CLAUDE.md o AGENTS.md                  # FR-002 + FR-007: contexto del agente
├── resources/                             # Fuentes locales del proyecto (puede importar de canónicas)
├── specs/[###-feature]/
│   ├── spec.md                            # Brief (FR-005)
│   ├── research.md                        # FR-008
│   ├── plan.md                            # Temario + descripciones (FR-010)
│   ├── tasks.md
│   ├── glossary.md                        # FR-021 (KE Glosario consolidado)
│   ├── findings.md                        # FR-019 + FR-027
│   └── checklists/
│       ├── requirements.md
│       ├── pasada-1.md ... pasada-5.md    # FR-018
│
├── chapters/
│   └── [###]-titulo.md                    # FR-029
├── index.md                               # FR-029
├── glossary.md                            # FR-029 (proyecto-wide)
├── common-errors.md                       # FR-029
└── templates/                             # FR-029
```

**Structure Decision**: el repositorio canónico de Write.OnMars (este repo) sigue la organización descrita arriba. Las skills bundled, el módulo MCP opcional, los scripts de instalación, los contratos publicados, la documentación del mantenedor, los recursos editoriales canónicos y los tests viven en directorios de primer nivel. La instalación sobre un proyecto destino replica las skills, el manifiesto y la infraestructura Spec Kit; el contenido editorial (specs, chapters, index, glossary, common-errors, templates) lo genera el operador a medida que ejecuta el flujo.

## Phase 0 — Outline & Research

Salida: `research.md` (en este mismo directorio) con seis decisiones técnicas que el plan deja resueltas para evitar arrastrar `NEEDS CLARIFICATION` a Phase 1:

1. Mecanismo de instalación (script Bash, no binario; reutiliza Spec Kit init).
2. Distribución de skills bundled (copia por defecto, `--symlink` opcional).
3. Implementación del contrato de citación (Markdown spec + JSON schema; ningún MCP queda atado).
4. Mecanismo de delegación a sub-agentes (Claude Code Agent tool con prompts canónicos por pasada).
5. Esquema del manifiesto del proyecto (JSON con `framework_version`, `constitution_version`, `skills[]`, `signing_matrix`).
6. Estrategia de testing editorial (smoke shell para instalación + guía piloto para flujo completo).

Cada decisión incluye: qué se eligió, por qué, alternativas consideradas y enlace a las FR/SC que cubre.

## Phase 1 — Design & Contracts

**Prerequisites**: `research.md` resuelto.

Salidas:

1. **`data-model.md`** — esquemas detallados de las entidades clave declaradas en la spec (Brief, Investigación, Contexto del proyecto, Temario, Descripciones encadenadas, Glosario consolidado, Capítulo, Index, Errores comunes, Plantillas reutilizables, Checklist de pasada, Hallazgos de revisión, Manifiesto del proyecto) con campos obligatorios, validaciones derivadas de los FR y transiciones de estado donde aplique.
2. **`contracts/citation-contract.md`** — contrato canónico FR-009a (campos, ejemplos, JSON schema mínimo, reglas de versionado).
3. **`contracts/manifest-schema.json`** — JSON Schema del manifiesto del proyecto editorial (FR-004 + FR-027).
4. **`contracts/pass-output-schema.md`** — formato unificado del output de cada una de las cinco pasadas (FR-018, FR-019).
5. **`quickstart.md`** — recorrido de primer uso del harness instalado: desde `writeonmars-install` hasta producir el primer capítulo.
6. **Actualización de `CLAUDE.md`** — entre los marcadores `<!-- SPECKIT START -->` y `<!-- SPECKIT END -->`, referencia explícita a este plan.

**Constitution Re-Check post-Phase 1**: ningún artefacto de Phase 1 introduce dependencias rígidas a un agente concreto, ningún contrato obliga a usar memoria externa como fuente de verdad, y todos los outputs de pasada conservan el formato accionable (frase original + problema + severidad + reescritura sugerida) exigido por FR-019. PASS.

## Complexity Tracking

> Vacío. Constitution Check pasó sin violaciones. La complejidad inherente del framework (varias skills, sub-agentes, contrato de citación, MCP opcional) se justifica por el alcance funcional de la spec y no contraviene ningún principio.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (ninguno)  | (n/a)      | (n/a)                                |
