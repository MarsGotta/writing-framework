# Write.OnMars

Harness editorial para que un agente de IA produzca guías técnicas,
manuales, artículos, libros y tutoriales al nivel de calidad esperado de
una autora especializada. No reemplaza al agente: lo gobierna mediante
skills, contratos publicados, plantillas Spec Kit adaptadas y un manifest
del proyecto.

Audiencia primaria: agentes de IA que ejecutan el flujo. Audiencia
secundaria: la persona que mantiene el framework y la que opera un
proyecto editorial.

## Arquitectura en una pantalla

```
+------------------+       +-------------------------+       +-------------------+
|     Agente       | --->  |        Skills           | --->  |  Contratos        |
|  (Claude Code,   |       |  .claude/skills/        |       |  contracts/       |
|   Codex futuro)  |       |  - marcela-prose        |       |  - citation v1.0  |
+------------------+       |  - technical-guide-...  |       |  - manifest v1.0  |
        |                  |  - writeonmars-*        |       |  - pass-output    |
        v                  +-------------------------+       +-------------------+
+------------------+                  |                              |
|  Spec Kit ciclo  |                  v                              v
|  /speckit-*      |       +-------------------------+       +-------------------+
|  + hooks Git     | --->  |   Manifest del proyecto |  -->  |  Repo editorial   |
+------------------+       |  .writeonmars-manifest  |       |  specs/, chapters/|
                           |  signing matrix,         |       |  glossary.md,     |
                           |  human_operators,        |       |  findings.md,     |
                           |  research_mode           |       |  index.md         |
                           +-------------------------+       +-------------------+
```

- **Skills** envuelven cada paso del flujo editorial (brief, investigación,
  temario, descripciones encadenadas, redacción, cinco pasadas, cierre).
  Bundled en `.claude/skills/`.
- **Contratos publicados** en `contracts/` (citación, manifest,
  pass-output) hacen al framework agnóstico de proveedor: cualquier MCP o
  agente que respete los contratos encaja.
- **Manifest del proyecto** declara versiones de skills, política de
  firmas por pasada y operadores humanos autorizados. Lo emite
  `writeonmars-install` y lo respeta toda la pipeline.
- **Spec Kit** vehicula el ciclo (`/speckit-specify`, `/speckit-plan`,
  `/speckit-tasks`, `/speckit-implement`) reutilizado para producción
  editorial mediante plantillas adaptadas.

## Estado por user story

| User Story | Alcance | Estado |
|------------|---------|--------|
| US1 — Instalación | Install reproducible <5 min sobre repo Git vacío | OK |
| US2 — Producción editorial | Pipeline completa: brief → 5 pasadas firmadas → cierre | OK |
| US3 — Paralelización | Redacción y contraste paralelos para guías ≥4 capítulos | OK |
| US4 — Mantenimiento | Bump de skill propaga a proyectos instalados <15 min | OK |
| Polish & cross-cutting | MCP de referencia, scaffolding Codex, docs finales | in-progress |
| Tag v1.0.0 | Release pública del framework | pending |

## Quickstart

```bash
# 1. Crear el repo editorial
mkdir mi-guia && cd mi-guia && git init

# 2. Instalar Write.OnMars (clonado canónico en ~/repos/writing-framework)
bash ~/repos/writing-framework/install/install.sh \
  --target-dir "$(pwd)" \
  --agent claude-code \
  --language es

# 3. Iniciar el primer brief editorial
/speckit-specify "Tu guia tecnica aqui"
```

Recorrido completo paso a paso en
[`specs/001-framework-architecture/quickstart.md`](specs/001-framework-architecture/quickstart.md).

## Enlaces principales

- Constitución: [`.specify/memory/constitution.md`](.specify/memory/constitution.md)
- Spec activa: [`specs/001-framework-architecture/spec.md`](specs/001-framework-architecture/spec.md)
- Plan: [`specs/001-framework-architecture/plan.md`](specs/001-framework-architecture/plan.md)
- Tareas: [`specs/001-framework-architecture/tasks.md`](specs/001-framework-architecture/tasks.md)
- Quickstart: [`specs/001-framework-architecture/quickstart.md`](specs/001-framework-architecture/quickstart.md)
- Catálogo de skills: [`docs/skill-catalog.md`](docs/skill-catalog.md)
- Ciclo editorial completo: [`docs/editorial-cycle.md`](docs/editorial-cycle.md)
- Instalación: [`docs/installation.md`](docs/installation.md)
- Paralelización: [`docs/parallel-execution.md`](docs/parallel-execution.md)
- Portabilidad entre agentes: [`docs/portability-validation.md`](docs/portability-validation.md)
- Contributing: [`docs/contributing.md`](docs/contributing.md)
- CHANGELOG: [`CHANGELOG.md`](CHANGELOG.md)

## Versión actual

- Framework: **0.x.0** (pre-tag; v1.0.0 pendiente).
- Constitución: **v1.1.0** (Ratified 2026-05-06).
- Contrato de citación: **v1.0**.
- Schema del manifest: **v1.0**.

## Idioma primario

Español. Toda excepción (siglas, citas en otra lengua, fragmentos de
código) se declara en el brief del proyecto editorial. Ver constitución §
"Propósito y alcance" y § IV "Precisión léxica".

## Licencia

TBD. Pendiente de elegir antes de la release v1.0.0.
