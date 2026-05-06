# Portabilidad entre agentes (SC-007 readiness)

Audiencia: persona mantenedora del framework Write.OnMars y personas que
quieran portar el harness a un agente distinto de Claude Code (Codex,
Cursor, otros). Cubre el estado de SC-007 en v1 y el plan de validación
end-to-end diferido.

## Qué es agente-agnóstico

Las siguientes piezas no asumen un LLM concreto y MUST permanecer
agnósticas:

- **Skills nucleares en `.claude/skills/`**. Aunque la ruta usa el
  convenio de Claude Code, cada skill es un archivo markdown autoexplicativo
  con front-matter YAML (`name`, `description`, `allowed-tools`). Cualquier
  agente que respete el formato puede consumirlas.
- **Contratos publicados en `contracts/`**:
  - `citation-contract.md` v1.0 + `citation-record.schema.json`.
  - `manifest-schema.json` v1.0.
  - `pass-output-schema.md` v1.0.
  Ningún contrato menciona Claude Code. Son JSON Schema o markdown
  declarativo.
- **Manifest del proyecto** (`.writeonmars-manifest.json`): declara qué
  skills están instaladas, con qué versión, bajo qué constitución y con
  qué matriz de firmas. La estructura no es propietaria.
- **Scripts del instalador** (`install/install.sh`, `install/lib/*.sh`):
  shell estándar Bash 5+. No invocan APIs propietarias. El único punto
  específico de agente es elegir el archivo de contexto (`CLAUDE.md` vs
  `AGENTS.md`), seleccionable vía flag `--agent`.
- **Plantillas Spec Kit** (`.specify/templates/*.md`): markdown puro.
  Spec Kit es transversal; cualquier agente que ejecute sus comandos las
  consume sin cambios.

## Qué requiere adaptador por agente

Estas piezas dependen de cómo un agente concreto consume contexto y
despacha sub-agentes:

- **Prompts canónicos por agente** (`agents/<nombre>/prompts/`). Cada
  agente tiene su sintaxis para roles, herramientas permitidas y reglas de
  no-acción. Los prompts viven en su carpeta, NO en las skills, para no
  contaminar el cuerpo agnóstico del framework.
- **Mecanismo de despacho de sub-agentes**. Claude Code ofrece el Agent
  tool con `subagent_type`. Codex y Cursor tendrán equivalentes (o
  carecerán de uno; en ese caso, las pasadas dejan de poder ejecutarse en
  contexto fresco automáticamente).
- **Detección de skills**. Claude Code indexa `.claude/skills/` y dispara
  por `description`. Codex podría requerir un manifiesto explícito de
  herramientas. El adaptador debe traducir el descubrimiento.
- **Hooks Spec Kit**. Los hooks Git de `.specify/extensions/git/` son
  shell puro y funcionan en cualquier agente. El renderizado del archivo
  de contexto (`CLAUDE.md` vs `AGENTS.md`) es lo único específico.

## Checklist para portar a un nuevo agente

Cada paso es una casilla independiente. La portabilidad SC-007 se
considera cumplida cuando todas estén marcadas.

- [ ] **Reproducir `agents/<nuevo>/prompts/`**: traducir cada
  `agents/claude/prompts/*.md` (redaccion + pasada-1..5) a la sintaxis del
  agente nuevo, manteniendo el contrato de output (`pass-output-schema.md`
  v1.0) y la lente de cada pasada.
- [ ] **Verificar despacho de sub-agente**: confirmar que el agente expone
  una herramienta equivalente al Agent tool de Claude Code para
  contexto fresco. Si no la expone, documentar la limitación en el
  README del adaptador.
- [ ] **Verificar lectura del manifest**: el agente puede leer
  `.writeonmars-manifest.json` y respetar `signing_matrix`,
  `human_operators[]`, `research_mode` y `language_primary` durante la
  ejecución del flujo editorial.
- [ ] **Adaptar `install/install.sh`** para que el cuestionario y el
  render del archivo de contexto produzcan la salida correcta para el
  agente nuevo (ej. `AGENTS.md` para Codex, `.cursor/rules/` para Cursor,
  etc.).
- [ ] **Correr smoke tests adaptados**:
  - `tests/smoke/install-on-empty-repo.sh` debe pasar contra el agente
    nuevo (con la adaptación de archivo de contexto).
  - `tests/smoke/specify-after-install.sh` debe pasar.
  - `tests/smoke/update-skill-on-installed-project.sh` debe pasar.
- [ ] **Pilotar 3 capítulos** sobre el mismo tema del piloto Claude Code y
  comparar findings, cobertura de glosario y críticos por pasada con la
  baseline. Equivalencia ±10% sostiene SC-007.

## Estado v1

| Agente | Estado | Notas |
|--------|--------|-------|
| `claude-code` | ready | Prompts canónicos + skills + smoke tests + dos pilotos editoriales validados (3 y 4 capítulos). |
| `codex` | scaffolding | `agents/codex/` con prompts placeholder (`prompt-version: 0.1.0-scaffold`). El instalador acepta `--agent codex` y produce `AGENTS.md`, pero los prompts están sin portar. |
| `cursor` | TBD | No iniciado en v1. La estructura del repo lo permite (`agents/cursor/` cuando exista) sin tocar las skills nucleares. |
| `other` | TBD | El flag `--agent other` se acepta como escape hatch; no hay prompts ni adaptador. |

## Diferimiento de la validación end-to-end

SC-007 v1 entrega scaffolding + contratos + checklist. La validación
**end-to-end con un segundo agente real** (Codex o Cursor produciendo una
guía completa que pasa las cinco pasadas) queda diferida a una feature
posterior. La razón: portar los prompts canónicos requiere acceso operativo
al agente nuevo y un piloto editorial dedicado, lo cual excede el alcance
de la feature `001-framework-architecture`.

La decisión es explícita: separar el scaffolding (que demuestra que el
framework no encadena la arquitectura a Claude Code) del piloto real (que
demostraría equivalencia funcional). El primero entra en v1; el segundo se
abre como `002-portability-codex` (o equivalente) cuando la persona
mantenedora tenga ancho de banda para Codex.

## Referencias

- `agents/claude/prompts/` — prompts canónicos en sintaxis Claude Code.
- `agents/codex/prompts/` — placeholders de Codex.
- Constitución § Arquitectura del framework — agnosticismo de agente.
- `contracts/manifest-schema.json` § `agent_target` — enum de agentes
  soportados.
