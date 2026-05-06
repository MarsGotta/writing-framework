# Ciclo editorial Write.OnMars

**Audiencia**: persona mantenedora del framework + agentes que ejecutan el
ciclo. **Cobertura**: FR-001..FR-029, constitución v1.1.0.

Este documento describe el flujo editorial canónico de ocho etapas, con
entradas, salidas, skill responsable, requisito funcional / principio
cubierto y condiciones de bloqueo. Termina con el diagrama del flujo y un
mapeo a Spec Kit.

## Etapa 0: Instalación

**Skill responsable**: `writeonmars-install` (T023, ya en `ready`).

**Entrada**: repositorio Git inicializado (vacío o con Spec Kit previo).

**Salida**:

- `.specify/memory/constitution.md` (copiada).
- `.specify/templates/{spec,plan,tasks,checklist}-template.md` (modo dual
  software/editorial).
- `.specify/extensions.yml` y `.specify/extensions/git/*` registrados.
- `.claude/skills/marcela-prose/`, `.claude/skills/technical-guide-design/`,
  `.claude/skills/writeonmars-*/` instaladas.
- `CLAUDE.md` o `AGENTS.md` con bloque WriteOnMars entre marcadores.
- `.writeonmars-manifest.json` generado y validado contra
  `contracts/manifest-schema.json`.

**Constitución / FR**: FR-001, FR-002, FR-003, FR-004, FR-028.

**Bloqueo**: la instalación bloquea ante:

- Bash < 5, Git < 2.30 o destino que no es repo Git (`exit 10`).
- Conflictos detectados por `detect-existing.sh` sin `--force` (`exit 20`).
- Falla en cualquier paso de copy-skills, render-context, render-manifest o
  hook registration (`exit 30..60`).

## Etapa 1: Brief

**Skill responsable**: `writeonmars-brief` (T034, planned).

**Entrada**:

- Tema natural en lenguaje libre que la persona operadora indica al ejecutar
  `/speckit-specify`.
- Cuestionario inicial del instalador, ya archivado en el manifiesto y en
  el contexto del agente.

**Salida**:

- `specs/[###-feature]/spec.md` con los nueve campos del brief obligatorio
  (audiencia, problema, resultado_esperado, nivel, tono,
  conceptos_obligatorios, ejemplo_recurrente, riesgos, acciones_practicas).
- Actualización del bloque WriteOnMars en `CLAUDE.md` / `AGENTS.md` con la
  audiencia, el ejemplo recurrente y el tono del brief (FR-007).

**Constitución / FR**: Principio III (NO NEGOCIABLE), FR-005, FR-007.

**Bloqueo**: el avance a la etapa 2 (investigación) bloquea mientras la
spec contenga `[NEEDS CLARIFICATION]` no resuelto en campos críticos:
audiencia, ejemplo recurrente, resultado esperado (FR-006).

## Etapa 2: Contexto del proyecto

**Skill responsable**: `writeonmars-brief` (la misma; FR-007 forma parte del
mismo ciclo de creación del brief).

**Entrada**: brief aprobado.

**Salida**: bloque WriteOnMars actualizado en `CLAUDE.md` / `AGENTS.md` con
los campos derivados del brief (audiencia, ejemplo recurrente, glosario
inicial, tono, reglas microestilísticas heredadas, referencias al plan y a
la constitución).

**Constitución / FR**: FR-002, FR-007.

**Bloqueo**: si el bloque entre marcadores `<!-- WRITEONMARS START -->` y
`<!-- WRITEONMARS END -->` no se actualiza, el agente arrancará la sesión
sin contexto editorial y producirá texto genérico.

## Etapa 3: Investigación con fuentes

**Skill responsable**: `writeonmars-research` (T035, planned). Modo BYOM por
defecto; opción de activar el módulo bundled `writeonmars-research-mcp`
(FR-009b) cuando el proyecto exige coherencia uniforme de citación.

**Entrada**:

- Brief aprobado.
- Conceptos obligatorios del brief (campo 6).
- `resources/` (fuente local obligatoria).
- MCPs externos compatibles con el contrato de citación (`context7`, web
  search, `fetch`, etc.).

**Salida**: `specs/[###-feature]/research.md` con `CitationRecord`
conformes al contrato `contracts/citation-contract.md` v1.0. Cada concepto
obligatorio del brief tiene al menos una cita (SC-009).

**Constitución / FR**: FR-008, FR-009, FR-009a, FR-009b, SC-009.

**Bloqueo**: el avance a la etapa 4 (temario) bloquea mientras quede algún
concepto obligatorio sin cita. La etapa también bloquea si los
`CitationRecord` no validan contra `contracts/citation-record.schema.json`
(verificable con `tests/lib/validate-citation.sh`).

## Etapa 4: Temario

**Skill responsable**: `writeonmars-temario` (T036, planned). Envuelve
`/technical-guide-design`.

**Entrada**:

- Brief aprobado.
- `research.md` con cobertura de conceptos obligatorios.

**Salida**: sección "Temario" en `specs/[###-feature]/plan.md` con tabla
`numero | titulo | promesa | estructura_aplicada` (data-model § 4). Cada
capítulo aplica `didactica_v1` (estructura del Principio II).

**Constitución / FR**: FR-010, Principio II.

**Bloqueo**: el avance a la etapa 5 (descripciones encadenadas) bloquea
mientras el temario tenga capítulos sin promesa o títulos vacíos.

## Etapa 5: Descripciones encadenadas

**Skill responsable**: `writeonmars-descripciones` (T037, planned). Envuelve
`/technical-guide-design`.

**Entrada**: temario aprobado, brief, glosario inicial.

**Salida**: sección "Descripciones encadenadas" en `plan.md` con, por
capítulo: `promesa_especifica`, `conexion_anterior`, `conexion_siguiente`,
`ejemplo_recurrente_aplicado`, `conceptos_introducidos` (data-model § 5).
Las conexiones `null` solo se permiten en frontera (capítulo 1 y último).

**Constitución / FR**: FR-010, FR-011 (Constitution Check editorial),
SC-005.

**Bloqueo**: el avance a la etapa 6 (redacción) bloquea ante:

- Conexión `null` fuera de frontera.
- Capítulos sin `ejemplo_recurrente_aplicado` cuando el ejemplo del brief
  cubre el caso (SC-005).
- Constitution Check con desviaciones no registradas en
  `Complexity Tracking`.

## Etapa 6: Redacción capítulo a capítulo

**Skill responsable**: `writeonmars-redaccion` (T039, planned). Despacha un
sub-agente fresco por capítulo siguiendo
`agents/claude/prompts/redaccion.md`. Modo paralelo `--parallel N` se
añade en US3 (T062).

**Entrada por sub-agente**:

- Brief completo.
- Sección "Temario".
- Descripción encadenada del capítulo objetivo.
- Descripciones encadenadas de los capítulos contiguos.
- Glosario consolidado vigente.
- Ejemplo recurrente.

**Salida por sub-agente**: `chapters/[###]-titulo.md` con front-matter YAML
(data-model § 7) + las nueve secciones obligatorias del Principio II + un
anexo de glosario marcado para `writeonmars-glossary`.

**Salida agregada**: glosario consolidado actualizado por
`writeonmars-glossary` (T038, planned), con detección de colisiones (FR-015)
y términos huérfanos (SC-004).

**Constitución / FR**: FR-012, FR-014, FR-015, Principios I–IV, SC-003,
SC-005.

**Bloqueo**: el avance a la etapa 7 bloquea ante:

- Capítulos sin las nueve secciones obligatorias.
- Colisiones de definición en el glosario consolidado sin resolver.
- Términos técnicos en el cuerpo ausentes del glosario.

## Etapa 7: Contraste de información

**Skill responsable**: `writeonmars-contraste` (T040, planned). Es el motor
que la pasada 4 invocará; también puede ejecutarse de forma anticipada
sobre afirmaciones puntuales.

**Entrada**: capítulos redactados, `research.md`, glosario consolidado.

**Salida**: bloque preliminar de contraste (no firmado) en `findings.md`
para que la pasada 4 lo refine y lo firme.

**Constitución / FR**: FR-016, FR-017, Principio V.4.

**Bloqueo**: la etapa puede repetirse hasta que `research.md` cubra cada
afirmación verificable.

## Etapa 8: Cinco pasadas + cierre

**Skills responsables**: `writeonmars-pasada-1`..`writeonmars-pasada-5`
(T041–T045, planned), `writeonmars-close-project` (T046, planned). Cada
pasada se delega a un sub-agente fresco siguiendo
`agents/claude/prompts/pasada-{1..5}.md`.

**Entrada por sub-agente** (común):

- Capítulo objetivo.
- Brief.
- Glosario consolidado.
- Descripciones encadenadas vecinas.
- `findings.md` actual.

**Salida por sub-agente**:

- Bloque añadido a `findings.md` conforme a
  `contracts/pass-output-schema.md` v1.0.
- `checklists/[###-feature]/pasada-N.md` firmado (autonomous o human según
  matriz del manifiesto).

**Mapeo skill principal por pasada**:

| Pasada | Nombre | Skill principal |
|--------|--------|-----------------|
| 1 | Estructura | `/technical-guide-design` |
| 2 | Utilidad | `/technical-guide-design` |
| 3 | Naturalidad | `/marcela-prose` |
| 4 | Precisión | `writeonmars-contraste` |
| 5 | Formato | `writeonmars-pasada-5` |

**Cierre del proyecto**: `writeonmars-close-project` consume `findings.md`
+ manifiesto y devuelve `{closeable: bool, blockers: [...]}`. Bloquea ante:

- ≥ 1 finding con `severidad = critico` y `estado = abierto` (FR-020).
- Pasada con `firma.tipo = autonomous` cuando la matriz declara `human`
  (FR-020a).

**Constitución / FR**: FR-018, FR-019, FR-020, FR-020a, Principio V.

## Diagrama del flujo

```text
┌──────────────────┐
│ 0. Instalación   │  writeonmars-install
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 1. Brief         │  /speckit-specify → writeonmars-brief
└────────┬─────────┘  bloquea si [NEEDS CLARIFICATION] en campos críticos
         │
         ▼
┌──────────────────┐
│ 2. Contexto      │  writeonmars-brief (FR-007)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 3. Investigación │  /speckit-clarify (si aplica) → writeonmars-research
└────────┬─────────┘  bloquea si concepto obligatorio sin cita
         │
         ▼
┌──────────────────┐
│ 4. Temario       │  /speckit-plan → writeonmars-temario
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 5. Descripciones │  /speckit-plan → writeonmars-descripciones
│    encadenadas   │
└────────┬─────────┘  Constitution Check editorial
         │
         ▼
┌──────────────────┐
│ 6. Redacción     │  /speckit-tasks + /speckit-implement →
│                  │  writeonmars-redaccion (sub-agentes frescos)
└────────┬─────────┘  + writeonmars-glossary (consolidación)
         │
         ▼
┌──────────────────┐
│ 7. Contraste     │  writeonmars-contraste (preliminar)
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│ 8. Cinco pasadas (sub-agente fresco por pasada)          │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐        │
│  │ P1   │→ │ P2   │→ │ P3   │→ │ P4   │→ │ P5   │        │
│  │estr. │  │util. │  │nat.  │  │prec. │  │form. │        │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘        │
│   auton.    auton.    HUMAN     HUMAN     auton.         │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
                 ┌──────────────────┐
                 │ Cierre proyecto  │  writeonmars-close-project
                 └──────────────────┘  bloquea por críticos abiertos
                                       o firmas humanas faltantes
```

## Mapeo a Spec Kit

El ciclo editorial reutiliza los comandos Spec Kit existentes. Equivalencias
canónicas:

| Comando Spec Kit | Etapa editorial | Skill que envuelve / activa |
|------------------|-----------------|------------------------------|
| `/speckit-specify` | 1 (Brief) + 2 (Contexto) | `writeonmars-brief` |
| `/speckit-clarify` | refinamiento del brief | `writeonmars-brief` (modo clarify) |
| `/speckit-plan` | 4 (Temario) + 5 (Descripciones) | `writeonmars-temario`, `writeonmars-descripciones` |
| `/speckit-tasks` | descomposición editorial | `writeonmars-redaccion`, pasadas como tareas |
| `/speckit-implement` | 6 (Redacción) + 7 (Contraste) + 8 (Pasadas) | `writeonmars-redaccion`, `writeonmars-contraste`, `writeonmars-pasada-{1..5}` |
| `/speckit-analyze` | auditoría brief / plan / tareas | `writeonmars-close-project` (bloqueo final) |
| `/speckit-checklist` | materialización de pasadas | `writeonmars-pasada-{1..5}` |
| `/speckit-constitution` | actualización de la constitución | (mantenimiento, fuera del ciclo de proyecto) |

Las extensiones Git registradas en `.specify/extensions.yml` (auto-commit
y validación de rama) aplican igual a artefactos editoriales que a código.

## Referencias

- Constitución vigente: `.specify/memory/constitution.md` (v1.1.0).
- Esquemas de entidades: `specs/001-framework-architecture/data-model.md`.
- Contrato de citación: `contracts/citation-contract.md` (v1.0).
- Esquema de pasadas: `contracts/pass-output-schema.md` (v1.0).
- Esquema del manifiesto: `contracts/manifest-schema.json`.
- Catálogo de skills: `docs/skill-catalog.md`.
- Procedimiento de instalación: `docs/installation.md`.
