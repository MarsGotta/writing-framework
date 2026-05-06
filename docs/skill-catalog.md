# Catálogo de skills — Write.OnMars

**Audiencia**: persona mantenedora del framework + portadores hacia Codex /
Cursor. **Cobertura**: FR-025..FR-028.

Este documento enumera cada skill bundled en el repositorio canónico de
Write.OnMars (incluidas las dos skills externas que el framework envuelve)
con su estado, requisitos funcionales cubiertos, qué envuelve, entradas,
salidas y trigger phrases. La fuente de verdad para versiones es el archivo
`VERSION` de cada `.claude/skills/<name>/`.

## Estados

- **ready**: skill implementada y verificable mediante smoke tests o piloto.
- **planned**: skill definida en `tasks.md` pero todavía no implementada.
- **deferred**: skill mencionada en spec pero pospuesta a futuras releases.

## Skills propias (`writeonmars-*`)

| Nombre | Estado | FR cubiertas | Wraps | Inputs | Outputs | Trigger phrases |
|--------|--------|--------------|-------|--------|---------|-----------------|
| `writeonmars-install` | ready | FR-001, FR-002, FR-003, FR-004, FR-028 | — | repo Git destino, cuestionario inicial (`tipo de proyecto`, `agente`, `idioma`, `audiencia`, `dominio`, operador, email) | `.specify/`, `.claude/skills/`, `.writeonmars-manifest.json`, `CLAUDE.md` / `AGENTS.md` con bloque WriteOnMars | "instala write.onmars", "writeonmars init", "configura write.onmars en este repo", "agrega write.onmars al proyecto" |
| `writeonmars-brief` | planned (T034) | FR-005, FR-006, FR-007 | — | tema natural, manifiesto, contexto del agente | `specs/[###-feature]/spec.md` con los nueve campos del brief; bloque WriteOnMars actualizado | "haz el brief de la guía", "completa el brief Write.OnMars", "/speckit-specify [tema]" |
| `writeonmars-research` | planned (T035) | FR-008, FR-009, FR-009a, FR-009b, SC-009 | — | brief, conceptos obligatorios, `resources/`, MCPs externos | `specs/[###-feature]/research.md` con `CitationRecord` validados contra `contracts/citation-record.schema.json` | "investiga las fuentes", "produce research.md", "verifica fuentes con citation contract" |
| `writeonmars-temario` | planned (T036) | FR-010 | `/technical-guide-design` | brief, `research.md` | sección "Temario" en `plan.md` (data-model § 4) | "genera el temario", "diseña la estructura de la guía" |
| `writeonmars-descripciones` | planned (T037) | FR-010, SC-005 | `/technical-guide-design` | temario, brief, glosario inicial | sección "Descripciones encadenadas" en `plan.md` (data-model § 5) | "genera las descripciones encadenadas", "conecta los capítulos del temario" |
| `writeonmars-glossary` | planned (T038) | FR-015, FR-021, SC-004 | — | anexos de glosario de cada capítulo, glosario consolidado vigente | `specs/[###-feature]/glossary.md` y `glossary.md` raíz; reporte de colisiones y términos huérfanos | "consolida el glosario", "detecta términos huérfanos", "resuelve colisiones del glosario" |
| `writeonmars-redaccion` | planned (T039) | FR-014, FR-015 | `/technical-guide-design`, `/marcela-prose` | brief, temario, descripción objetivo, descripciones contiguas, ejemplo recurrente, glosario consolidado, prompt `agents/claude/prompts/redaccion.md` | `chapters/[###]-titulo.md` + anexo de glosario | "redacta el capítulo N", "despacha sub-agente de redacción", "redacción --parallel N" (US3) |
| `writeonmars-contraste` | planned (T040) | FR-016, FR-017 | — (motor base de pasada 4) | capítulo, `research.md`, glosario | bloque preliminar de contraste en `findings.md` | "contrasta las afirmaciones", "verifica contra el research.md" |
| `writeonmars-pasada-1` | planned (T041) | FR-018, FR-019, Principio V.1 | `/technical-guide-design` | capítulo, brief, glosario, descripciones vecinas, prompt `agents/claude/prompts/pasada-1.md` | bloque pasada 1 en `findings.md` + `checklists/[###-feature]/pasada-1.md` | "ejecuta la pasada 1", "revisa estructura del capítulo" |
| `writeonmars-pasada-2` | planned (T042) | FR-018, FR-019, Principio V.2 | `/technical-guide-design` | igual que pasada 1 + prompt `pasada-2.md` | bloque pasada 2 en `findings.md` + `checklists/[###-feature]/pasada-2.md` | "ejecuta la pasada 2", "revisa utilidad del capítulo" |
| `writeonmars-pasada-3` | planned (T043) | FR-018, FR-019, FR-020a, Principio V.3, Principio I | `/marcela-prose` | igual que pasada 1 + prompt `pasada-3.md` | bloque pasada 3 en `findings.md` + `checklists/[###-feature]/pasada-3.md` (firma humana por defecto) | "ejecuta la pasada 3", "revisa naturalidad del capítulo" |
| `writeonmars-pasada-4` | planned (T044) | FR-016, FR-018, FR-019, FR-020a, Principio V.4 | `writeonmars-contraste` | capítulo, brief, `research.md`, glosario, descripciones vecinas, prompt `pasada-4.md` | bloque pasada 4 en `findings.md` con `referencias_cita` por hallazgo + `checklists/[###-feature]/pasada-4.md` (firma humana por defecto) | "ejecuta la pasada 4", "verifica precisión del capítulo" |
| `writeonmars-pasada-5` | planned (T045) | FR-018, FR-019, FR-029, Principio V.5 | — | todos los capítulos, glosario, descripciones, prompt `pasada-5.md` | bloque pasada 5 en `findings.md` + `checklists/[###-feature]/pasada-5.md` + `index.md`, `common-errors.md`, `templates/*` agregados | "ejecuta la pasada 5", "construye index y common-errors", "valida formato global" |
| `writeonmars-close-project` | planned (T046) | FR-020, FR-020a | — | `findings.md`, manifiesto | reporte `{closeable: bool, blockers: [...]}` | "cierra el proyecto editorial", "evalúa el gate de cierre" |
| `writeonmars-update` | planned (T068) | SC-008 | — | manifiesto del proyecto, versiones canónicas en repo Write.OnMars | manifiesto actualizado sin pérdida de configuración local | "actualiza las skills writeonmars", "sincroniza con la versión canónica" |

## Skills bundled de origen externo (envueltas)

El framework distribuye copias canónicas de dos skills externas porque son
dependencias declaradas (FR-025, FR-028). Su sincronización con la fuente
original (Obsidian vault) se trata como mantenimiento separado
(`docs/maintenance/sync-from-vault.md`).

| Nombre | Estado | FR cubiertas | Wraps | Inputs | Outputs | Trigger phrases |
|--------|--------|--------------|-------|--------|---------|-----------------|
| `/marcela-prose` | ready (bundled) | FR-025 (componente), Principio I, Principio IV | — | texto en español a editar | texto editado con voz Marcela: plural inclusivo, paréntesis honesto, antropomorfización del agente, metáforas sensoriales únicas, cierres bajos; limpieza de patrones LLM | "haz que suene a Marcela", "limpia el tono plano", "frases inconexas", "tono de eslogan", "marcela-prose este capítulo" |
| `/technical-guide-design` | ready (bundled) | FR-025 (componente), Principio II | — | brief, temario, capítulo o material de taller | diseño didáctico aplicando Diátaxis, andragogía, carga cognitiva, worked examples; arquitectura de capítulo y microedición pedagógica | "diseña una guía", "revisa este temario", "estructura este tutorial", "cómo enseñar X", "crea un workshop sobre Y" |

## Cómo proponer una nueva skill

Una nueva skill `writeonmars-*` se propone cuando cubre una capacidad que
ni `/marcela-prose` ni `/technical-guide-design` resuelven y que no encaja
en las skills existentes (FR-026). El procedimiento:

1. Abrir un issue / propuesta documentada en una rama dedicada con prefijo
   `skill/<nombre>`.
2. Justificar la skill contra el catálogo: qué FR cubre, qué evita duplicar,
   qué envuelve si aplica, qué inputs y outputs declara.
3. Redactar el `SKILL.md` y, si la skill orquesta sub-agentes, el prompt
   canónico en `agents/claude/prompts/<nombre>.md`.
4. Añadir entry en este catálogo con estado `planned` y tareas asociadas en
   `tasks.md` (si la propuesta forma parte de un ciclo activo).
5. Pasar revisión por la persona mantenedora del framework.

El procedimiento detallado vivirá en `docs/contributing.md` (T076) cuando
se publique. Mientras tanto, esa propuesta se discute con la persona
mantenedora antes de abrir el PR.

## Referencias

- Constitución vigente: `.specify/memory/constitution.md` (v1.1.0).
- Manifiesto del proyecto: `contracts/manifest-schema.json`.
- Contrato de citación: `contracts/citation-contract.md`.
- Esquema de pasadas: `contracts/pass-output-schema.md`.
- Procedimiento de mantenimiento de skills bundled:
  `docs/maintenance/sync-from-vault.md`.
- Procedimiento futuro de actualización de skills:
  `docs/maintenance/skill-update-procedure.md` (T069, planned).
