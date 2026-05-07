# Implementation Plan: CLI `wom` para operar Write.OnMars

**Branch**: `002-wom-cli` | **Date**: 2026-05-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-wom-cli/spec.md`

**Project type**: software CLI (no editorial). Las secciones "Temario" y "Descripciones encadenadas" del template no aplican y quedan declaradas como N/A.

## Summary

`wom` es una CLI Bash que unifica las operaciones de Write.OnMars desde el shell. No reescribe lógica de skills: las envuelve. Los subcomandos núcleo (`new`, `status`, `close`) eliminan la fricción de arranque, observación y cierre del proyecto editorial. Los secundarios (`brief`, `research`, `plan`, `draft`, `review`, `sign`) reducen el tipeo cuando hay que coordinar con el agente. Los de diagnóstico (`doctor`, `validate`, `update`) cubren troubleshooting y mantenimiento. v1 acepta solo español; inglés se difiere a feature posterior si la complejidad lo justifica.

La frontera con el agente es estricta: la CLI **no lanza el agente y no ejecuta sub-agentes**; orquesta estado, validación, firma y arranque. Para los pasos que requieren generación editorial real, imprime un prompt completo y pegable. Esto preserva la portabilidad declarada en FR-023/FR-024 del framework: la CLI funciona idéntica con Claude Code, Codex u otro agente compatible.

## Technical Context

**Language/Version**: Bash 5+ para todos los subcomandos. JSON intermediario via `jq`. Texto tabulado via `awk`. Sin Python, Node, Go, Rust ni binarios. Compatible con macOS / Linux modernos.
**Primary Dependencies**: Bash ≥5, Git ≥2.30, jq ≥1.6, awk (POSIX). Validación de schema vía `python3 + jsonschema` o `npx ajv-cli --spec=draft2020` (ya disponibles en el repo canónico para v1; reutilizadas).
**Optional Dependencies**: `gum` (selección interactiva en `wom review`), `fzf` (búsqueda fuzzy en `wom sign`). Detección en runtime; fallback a `read` y stdout estándar.
**Storage**: lectura del repositorio del proyecto activo (`.writeonmars-manifest.json`, `specs/[###]/findings.md`, `chapters/`, `checklists/`, `glossary.md`). Escritura solo en: lockfile `.wom/lock`, `checklists/[###]/pasada-N.md` (vía `wom sign`), opcionalmente `CLAUDE.md` y manifest (vía `wom new`/`wom update`).
**Testing**: smoke tests en Bash siguiendo el patrón de `tests/smoke/`. Tests por subcomando que crean sandboxes en `mktemp -d` y assertan side effects + exit codes. Reutilizan `tests/lib/validate-citation.sh` y `install/lib/common.sh`.
**Target Platform**: macOS y Linux con Bash 5+. Windows queda fuera (consistente con feature 001).
**Project Type**: CLI software single-binary. No web, no mobile, no editorial.
**Performance Goals**: `wom status` <1s con 8 capítulos (SC-002); `wom doctor` <2s (SC-005); `wom new` <30s incluyendo install (SC-001).
**Constraints**: 0 dependencias hard-required más allá de Bash 5, jq, awk, Git (SC-006). Idempotencia en operaciones que escriben. Lockfile para concurrencia.
**Scale/Scope**: proyectos editoriales de hasta 20 capítulos (consistente con feature 001 § Scale). Una operadora por sesión; lectura concurrente sin lock; escritura serializada con `.wom/lock`.

## Constitution Check

*GATE: debe pasar antes de Phase 0. Re-evaluar después de Phase 1.*

Esta CLI no produce contenido editorial directamente, pero su salida (mensajes de error, ayuda, dashboard) impacta a la operadora cuando opera la pipeline editorial. Los cinco principios se interpretan aplicados a la **superficie textual de la CLI**:

| Principio | Conformidad | Evidencia |
|-----------|-------------|-----------|
| **I. Voz natural y sobria** (NO NEGOCIABLE) | pasa | Mensajes en español sobrio, sin frases comprimidas, sin emojis, sin lenguaje promocional. `--help` y errores siguen el patrón de `install/install.sh`. |
| **II. Estructura situación → explicación → consecuencia** | pasa | Cada error de la CLI MUST seguir: qué pasó (situación) + por qué falla (explicación) + qué hacer (acción). El dashboard de `wom status` separa estado actual (situación), totales agregados (explicación) y blockers concretos (acción). |
| **III. Brief obligatorio** | N/A | El brief es un artefacto editorial; la CLI lo facilita (`wom brief` abre el spec.md en `$EDITOR`) pero no lo reemplaza. La CLI misma es software, no contenido editorial. |
| **IV. Precisión léxica** | pasa | Términos técnicos invariantes (`pasada`, `brief`, `findings`, `manifest`, `closeable`); sin sinónimos arbitrarios. Glosario embebido en `--help` cuando un término puede ser ambiguo. |
| **V. Revisión multi-pasada** | parcial | La CLI no se revisa con las cinco pasadas editoriales (no es prosa). Aplica revisión de software: tests por subcomando + smoke de regresión + paridad con skills envueltas (SC-003 y SC-008). Documentado en Phase 0 § R5. |

**Resultado del gate**: PASS. Dos N/A justificados (Principios III y V parcial); ninguna desviación que bloquee el plan.

`Complexity Tracking` queda vacío.

## Temario

> N/A. Feature 002 es software, no editorial. La sección queda declarada para mantener la estructura del template; el flujo editorial real es responsabilidad de los proyectos que **usan** esta CLI, no de la CLI en sí.

## Descripciones encadenadas

> N/A por la misma razón.

## Project Structure

### Documentation (this feature)

```text
specs/002-wom-cli/
├── plan.md              # Este archivo
├── research.md          # Phase 0 — decisiones técnicas resueltas
├── data-model.md        # Phase 1 — entidades derivadas (estado, lockfile)
├── quickstart.md        # Phase 1 — primer uso de la CLI
├── contracts/
│   └── command-schema.md  # Contrato de comandos: nombre, flags, exit codes
├── checklists/
│   └── requirements.md  # Spec quality checklist (creado en /speckit-specify)
└── tasks.md             # Phase 2 (creado por /speckit-tasks)
```

### Source Code (canonical repository)

```text
writing-framework/
├── bin/
│   └── wom                          # Entry point ejecutable (dispatcher)
│
├── bin/wom-lib/
│   ├── common.sh                    # Helpers compartidos (logging, lockfile, manifest)
│   ├── new.sh                       # `wom new <nombre>`
│   ├── brief.sh                     # `wom brief`
│   ├── research.sh                  # `wom research` (imprime prompt)
│   ├── plan.sh                      # `wom plan` (imprime prompt)
│   ├── draft.sh                     # `wom draft N [--parallel K]`
│   ├── review.sh                    # `wom review <pasada> <capítulo>`
│   ├── sign.sh                      # `wom sign <pasada> <capítulo>`
│   ├── status.sh                    # `wom status` (dashboard ASCII)
│   ├── validate.sh                  # `wom validate`
│   ├── close.sh                     # `wom close`
│   ├── update.sh                    # `wom update`
│   ├── doctor.sh                    # `wom doctor`
│   └── help.sh                      # `wom --help` y `wom <sub> --help`
│
├── tests/smoke/wom/
│   ├── new.sh                       # smoke de `wom new`
│   ├── status.sh                    # smoke de `wom status`
│   ├── close-parity.sh              # paridad vs writeonmars-close-project (SC-003)
│   ├── sign.sh                      # smoke de `wom sign`
│   ├── doctor.sh                    # smoke de `wom doctor`
│   ├── validate.sh                  # smoke de `wom validate`
│   └── run-all.sh                   # orquesta los anteriores
│
└── docs/
    └── wom-cli.md                   # Manual operativo de la CLI
```

**Structure Decision**: la CLI vive en `bin/wom` como dispatcher de una sola pantalla; cada subcomando es un script independiente en `bin/wom-lib/<sub>.sh`, importando `bin/wom-lib/common.sh` para utilidades compartidas. Los smoke tests de cada subcomando viven en `tests/smoke/wom/<sub>.sh` y un `run-all.sh` propio (separado del de feature 001 para evitar acoplamiento). El instalador (`install/install.sh`) añade un symlink de `bin/wom` en el `$PATH` del proyecto destino.

## Phase 0 — Outline & Research

Salida: `research.md` con seis decisiones técnicas resueltas:

1. **R1**: Distribución del binario en el `$PATH` del proyecto destino (symlink absoluto vs script shim vs `wom env` para `eval`).
2. **R2**: Lockfile concurrente (`flock` vs atomic `mkdir` vs PID file con stale-detection).
3. **R3**: Renderizado del dashboard de `wom status` (Bash printf + alineación awk vs `gum table` cuando esté disponible).
4. **R4**: Mecanismo de firma en `wom sign` (sed con marcadores HTML vs reemplazo por sección YAML front-matter).
5. **R5**: Estrategia de testing (bats vs Bash puro siguiendo el patrón de feature 001).
6. **R6**: Internacionalización (lookup table vs gettext vs deferida).

## Phase 1 — Design & Contracts

**Prerequisites**: `research.md` resuelto.

Salidas:

1. **`data-model.md`** — entidades derivadas de la CLI: `EstadoProyecto` (representación del status), `Lockfile` (formato y ciclo de vida), `BloqueFirma` (formato del bloque que `wom sign` escribe en checklists).
2. **`contracts/command-schema.md`** — contrato unificado: para cada subcomando, nombre, sintaxis, flags, exit codes y precondiciones. Es la fuente de verdad de `--help` y de los smoke tests.
3. **`quickstart.md`** — recorrido de extremo a extremo: instalar el framework, ejecutar `wom new`, `wom brief`, validar con `wom doctor`, escribir el primer capítulo, firmar pasadas, cerrar. 10 pasos con asserts.
4. **Actualización de `CLAUDE.md`** — añadir referencia a este plan entre los marcadores `<!-- SPECKIT START -->` y `<!-- SPECKIT END -->`, conservando feature 001 como referencia de framework base.

**Constitution Re-Check post-Phase 1**: la CLI no introduce dependencias rígidas a un agente (FR-024 framework); los contratos publicados (`command-schema.md`) son agente-agnósticos; el dashboard de `status` es ASCII puro, sin requerir terminal específico. PASS.

## Complexity Tracking

> Vacío. Constitution Check pasó sin desviaciones materiales.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (ninguno) | (n/a) | (n/a) |
