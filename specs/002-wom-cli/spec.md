# Feature Specification: CLI `wom` para operar Write.OnMars

**Feature Branch**: `002-wom-cli`
**Created**: 2026-05-07
**Status**: Draft
**Input**: User description: "CLI wom para operar Write.OnMars desde el shell. Una sola interfaz unificada para arrancar proyectos editoriales, observar el estado de capítulos × pasadas × severidad, firmar pasadas humanas, validar el entorno y cerrar el proyecto."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Arrancar un proyecto editorial nuevo en un solo comando (Priority: P1)

Una operadora editorial decide producir una guía sobre un tema. Hoy tiene que correr `mkdir`, `cd`, `git init`, ejecutar `install.sh` con cinco flags y abrir el agente para invocar `/speckit-specify`. La CLI `wom` colapsa esos pasos en `wom new <nombre>`, que pide solo el tipo de proyecto y la audiencia, y deja el repositorio listo para el siguiente paso editorial.

**Why this priority**: la fricción de arranque es la barrera de entrada más alta. Mientras la operadora tenga que recordar ocho comandos para empezar, postergará empezar.

**Independent Test**: ejecutar `wom new mi-guia-x` en un directorio vacío; verificar que (a) existe el repositorio Git, (b) `install/install.sh` corrió completo, (c) `.writeonmars-manifest.json` valida contra el schema, (d) la operadora puede correr `wom status` inmediatamente y obtener un dashboard coherente.

**Acceptance Scenarios**:

1. **Given** un directorio padre vacío, **When** la operadora ejecuta `wom new mi-guia` y responde el cuestionario mínimo, **Then** se crea `mi-guia/` con repositorio Git inicializado, framework instalado y manifest válido.
2. **Given** una instalación completa, **When** la operadora ejecuta `wom status` desde la raíz del proyecto, **Then** el dashboard se renderiza sin errores aunque el proyecto esté vacío de capítulos.
3. **Given** un nombre de proyecto que ya existe como directorio, **When** la operadora ejecuta `wom new`, **Then** el comando falla con mensaje claro y no toca el directorio existente.

---

### User Story 2 — Ver el estado de la guía completa de un vistazo (Priority: P1)

Durante la producción de una guía de varios capítulos, la operadora necesita saber rápidamente qué capítulos están redactados, qué pasadas pasaron, dónde quedaron hallazgos críticos y qué firmas humanas faltan. Sin la CLI, tiene que abrir `findings.md`, contar manualmente, abrir cada checklist y cruzar referencias con el manifest. `wom status` produce un dashboard ASCII en una sola pantalla.

**Why this priority**: el dashboard es la interfaz principal de seguimiento. Sin él, la operadora pierde contexto entre sesiones y la coordinación con sub-agentes se vuelve frágil.

**Independent Test**: producir un proyecto sintético con cuatro capítulos en estados mixtos (uno completo y firmado, dos con pasadas parciales, uno sin redactar); verificar que `wom status` muestra correctamente el estado de cada capítulo × pasada y los conteos agregados.

**Acceptance Scenarios**:

1. **Given** un proyecto con capítulos en distintos estados de pasada, **When** la operadora ejecuta `wom status`, **Then** ve una tabla `capítulos × 5 pasadas` con estados (completo, pendiente firma, bloqueador crítico, no ejecutado) y conteo de firmas humanas pendientes.
2. **Given** un proyecto con un hallazgo crítico abierto en pasada 4, **When** la operadora ejecuta `wom status`, **Then** ese hallazgo aparece marcado con severidad y referencia al capítulo afectado.
3. **Given** un proyecto sin manifest válido, **When** la operadora ejecuta `wom status`, **Then** el comando reporta el problema sin asumir estado.

---

### User Story 3 — Cerrar el proyecto editorial sin invocar el agente (Priority: P1)

Cuando todas las pasadas pasaron y los hallazgos críticos están resueltos o justificados, la operadora ejecuta `wom close` desde la consola. El comando ejecuta la lógica de `writeonmars-close-project` y devuelve `exit 0` con un mensaje breve si el proyecto cierra, o lista los blockers concretos con exit code distinto de cero.

**Why this priority**: el cierre es el momento más sensible del ciclo (FR-020 + FR-020a del framework). Que se haga desde la consola con auditoría clara reduce errores.

**Independent Test**: producir dos proyectos sintéticos, uno cerrable y otro con un crítico abierto; verificar que `wom close` exit 0 vs exit ≠ 0 con la lista de blockers correcta.

**Acceptance Scenarios**:

1. **Given** un proyecto con todas las pasadas completas y firmadas, **When** la operadora ejecuta `wom close`, **Then** sale con exit 0 y mensaje "Proyecto cerrable".
2. **Given** un proyecto con un crítico abierto en pasada 4, **When** la operadora ejecuta `wom close`, **Then** sale con exit 1 y la lista de blockers (capítulo, pasada, finding ID).
3. **Given** una pasada con firma `autonomous` cuando el manifest exige `human`, **When** la operadora ejecuta `wom close`, **Then** sale con exit 1 reportando la firma faltante.

---

### User Story 4 — Firmar pasadas humanas desde la consola (Priority: P2)

Las pasadas 3 (naturalidad) y 4 (precisión) exigen firma humana por defecto. Hoy implica abrir `checklists/pasada-N.md`, editar el bloque de firma, guardar y verificar que el campo coincida con un operador del manifest. `wom sign 3 1` (pasada 3 sobre capítulo 1) hace la edición de manera atómica: pide al operador, valida que esté en `human_operators`, escribe la firma con fecha ISO-8601 y deja el checklist en estado consistente.

**Why this priority**: lo hacemos varias veces por proyecto. Reducirlo de "abrir markdown + buscar bloque + escribir firma + guardar" a un solo comando ahorra tiempo y elimina errores de tipeo.

**Independent Test**: en un proyecto con pasada 3 capítulo 2 sin firmar, ejecutar `wom sign 3 2`; verificar que el checklist queda con `firma_tipo: human`, `firma_actor` igual al operador del manifest y `firma_fecha` con la fecha actual.

**Acceptance Scenarios**:

1. **Given** un checklist sin firmar, **When** la operadora ejecuta `wom sign 3 2`, **Then** el archivo queda firmado por el operador del manifest con fecha ISO actual.
2. **Given** un checklist ya firmado, **When** la operadora ejecuta `wom sign 3 2` de nuevo, **Then** el comando reporta que ya está firmado y no sobrescribe sin `--force`.
3. **Given** un manifest sin operador humano declarado, **When** la operadora ejecuta `wom sign`, **Then** el comando falla con mensaje claro.

---

### User Story 5 — Orquestar los pasos editoriales con prompts pre-formateados (Priority: P2)

Para los pasos que requieren generación editorial real (research, draft, review), la CLI no compite con el agente: imprime un prompt completo y bien formateado que la operadora pega en su agente. `wom draft 2 --parallel 2` imprime el prompt para `/writeonmars-redaccion` con el contexto del capítulo 2 y la indicación de paralelismo. `wom brief` abre `spec.md` en `$EDITOR` con la plantilla de los nueve campos pre-rellenada.

**Why this priority**: reduce fricción de tipeo y olvido (qué flags pasar, qué archivo leer, dónde guardar). La operadora sigue siendo la dueña del paso editorial; la CLI solo prepara el terreno.

**Independent Test**: ejecutar `wom draft 1 --parallel 2`; verificar que el prompt impreso (a) referencia los archivos correctos del proyecto activo, (b) incluye el flag de paralelismo, (c) es directamente pegable en el agente sin edición.

**Acceptance Scenarios**:

1. **Given** un proyecto con brief y plan completos, **When** la operadora ejecuta `wom draft 2`, **Then** se imprime un prompt completo con paths absolutos al brief, descripción del capítulo 2 y descripciones contiguas.
2. **Given** un proyecto sin spec.md aún creado, **When** la operadora ejecuta `wom brief`, **Then** se abre `$EDITOR` con la plantilla de nueve campos lista para rellenar.
3. **Given** un proyecto con research.md presente, **When** la operadora ejecuta `wom review 4 1`, **Then** se imprime el prompt para pasada 4 sobre capítulo 1 con referencia al research y al pass-output-schema.

---

### User Story 6 — Validar el entorno y los artefactos (Priority: P3)

Antes de empezar un proyecto o como parte de un troubleshooting, la operadora ejecuta `wom doctor` para verificar que el entorno tiene Bash, Git, jq, validador de schema (ajv o python+jsonschema) y al menos un MCP de investigación detectado. `wom validate` corre los smoke tests del framework, valida el manifest del proyecto activo y valida cada `CitationRecord` en el research.md.

**Why this priority**: útil para diagnóstico, pero no bloquea el flujo nuclear. La operadora puede operar sin invocar nunca doctor/validate hasta que algo falle.

**Independent Test**: ejecutar `wom doctor` en una máquina con todas las dependencias y luego en una máquina sin jq; verificar que reporta el estado correcto en cada caso. Ejecutar `wom validate` en un proyecto con manifest manipulado y un research.md con un CitationRecord inválido; verificar que reporta ambos errores con paths concretos.

**Acceptance Scenarios**:

1. **Given** un entorno con todas las dependencias, **When** la operadora ejecuta `wom doctor`, **Then** sale con exit 0 y un reporte por dependencia.
2. **Given** un entorno sin jq, **When** la operadora ejecuta `wom doctor`, **Then** sale con exit ≠ 0 reportando jq como faltante con la pista de instalación.
3. **Given** un research.md con un CitationRecord sin `motor`, **When** la operadora ejecuta `wom validate`, **Then** el comando reporta el record concreto y el campo violado.

---

### User Story 7 — Actualizar skills canónicas en proyectos instalados (Priority: P3)

Cuando una skill canónica del framework recibe un bump (p. ej., `marcela-prose` v0.2.0), la operadora ejecuta `wom update` desde un proyecto instalado y la CLI propaga el cambio preservando la configuración local del manifest.

**Why this priority**: deseable pero no urgente. v1 ya tiene `writeonmars-update` como skill; el wrap CLI mejora ergonomía.

**Independent Test**: bumpear la VERSION de una skill canónica, ejecutar `wom update` en un sandbox; verificar que la versión en el proyecto sube y que un campo custom del manifest sobrevive.

**Acceptance Scenarios**:

1. **Given** una skill canónica con versión nueva, **When** la operadora ejecuta `wom update`, **Then** las versiones se sincronizan y campos custom (signing_matrix, language_primary, human_operators) se preservan.
2. **Given** un proyecto sin updates pendientes, **When** la operadora ejecuta `wom update`, **Then** sale con mensaje "no hay actualizaciones" y exit 0.

---

### Edge Cases

- ¿Qué ocurre si la operadora ejecuta `wom` fuera de un proyecto Write.OnMars instalado? La CLI MUST detectar la ausencia de `.writeonmars-manifest.json` y, según el subcomando: `new` lo permite (es el caso esperado), todos los demás fallan con mensaje claro y exit ≠ 0.
- ¿Qué ocurre si el manifest está corrupto o no valida? `wom status`, `wom close`, `wom sign`, `wom update` MUST detectar la corrupción y abortar con exit ≠ 0 antes de tocar artefactos. `wom validate` MUST reportar el campo violado.
- ¿Qué ocurre si `findings.md` no sigue el `pass-output-schema.md`? `wom status` y `wom close` MUST tolerar bloques mal formados saltándolos y reportando el problema en el dashboard, sin caer.
- ¿Qué ocurre si la operadora intenta firmar como un operador no listado en `human_operators`? `wom sign` MUST rechazar la firma con mensaje específico que liste los operadores válidos.
- ¿Qué ocurre si el sandbox de un piloto editorial vive dentro del proyecto activo? La CLI MUST excluir cualquier ruta gitignored (`tests/editorial-pilot/sandbox/` y similares) del cómputo de `wom status`.
- ¿Qué ocurre si `gum` o `fzf` no están instalados? Los subcomandos que los usan opcionalmente MUST hacer fallback a `read` o salida estándar sin fallar.
- ¿Qué ocurre si `$EDITOR` no está configurado? `wom brief` MUST hacer fallback a `vi` y, si tampoco está, reportar y salir con exit ≠ 0.
- ¿Qué ocurre si dos sesiones de `wom` corren simultáneamente sobre el mismo proyecto? Subcomandos que escriben (`sign`, `update`, `close`) MUST usar lockfile o equivalente para evitar corrupción; lectura (`status`, `validate`, `doctor`) puede correr concurrentemente sin bloqueo.

## Requirements *(mandatory)*

### Functional Requirements

**Distribución y entry point**

- **FR-001**: El sistema MUST proveer un binario ejecutable `bin/wom` en el repositorio canónico que despache subcomandos a scripts Bash en `bin/wom-lib/<subcomando>.sh`.
- **FR-002**: El binario `wom` MUST aceptar `--help` global y por subcomando (`wom <sub> --help`), produciendo uso, flags y exit codes documentados.
- **FR-003**: El instalador del framework (`install/install.sh`) MUST hacer disponible `wom` en el `$PATH` del proyecto destino mediante symlink o entrada en el script de activación, sin requerir instalación global del sistema.

**Subcomando `new`**

- **FR-004**: `wom new <nombre>` MUST crear el directorio, ejecutar `git init`, llamar a `install/install.sh` con los flags apropiados y dejar el proyecto listo para `wom status`. El cuestionario inicial MUST recolectar al menos `tipo de proyecto editorial`, `audiencia general`, `idioma primario` y datos del operador.
- **FR-005**: `wom new` MUST detectar si el directorio destino ya existe y abortar sin tocarlo si tiene contenido.

**Subcomando `brief`**

- **FR-006**: `wom brief` MUST abrir `specs/[###-feature]/spec.md` en `$EDITOR` con la plantilla del modo editorial pre-rellenada. Si no hay feature directory, MUST orientar a la operadora a ejecutar `/speckit-specify` o `wom new` antes.

**Subcomandos `research`, `plan`, `draft N`, `review pasada capítulo`**

- **FR-007**: Cada uno de estos subcomandos MUST imprimir por stdout un prompt completo y pegable que invoque la skill correspondiente (`writeonmars-research`, `writeonmars-temario` + `writeonmars-descripciones`, `writeonmars-redaccion`, `writeonmars-pasada-N`) con los paths absolutos del proyecto activo y los flags solicitados.
- **FR-008**: `wom draft N --parallel K` MUST validar que K ∈ [2, 8] y emitir el prompt para `writeonmars-redaccion --parallel K`.

**Subcomando `sign`**

- **FR-009**: `wom sign <pasada> <capítulo>` MUST escribir el bloque de firma en `checklists/[###-feature]/pasada-N.md` con `firma_tipo: human`, `firma_actor` tomado del manifest (`human_operators[0].id` por defecto, `--operator <id>` para override) y `firma_fecha` ISO-8601 (`YYYY-MM-DD`) en hora local.
- **FR-010**: `wom sign` MUST rechazar con mensaje específico (a) firmas para operadores no listados en `human_operators`, (b) firmas duplicadas (a menos que `--force`).

**Subcomando `status`**

- **FR-011**: `wom status` MUST renderizar un dashboard ASCII con: nombre del proyecto, versión del framework, conteo de pasadas humanas firmadas vs requeridas, tabla `capítulos × 5 pasadas` con estado por celda y un total de hallazgos críticos abiertos. La leyenda MUST acompañar la tabla.
- **FR-012**: `wom status` MUST excluir paths gitignored (sandboxes de piloto, etc.) del cómputo y MUST tolerar bloques `findings.md` mal formados saltándolos.

**Subcomando `validate`**

- **FR-013**: `wom validate` MUST ejecutar `tests/smoke/run-all.sh`, validar `.writeonmars-manifest.json` contra el schema y validar cada `CitationRecord` de `specs/[###-feature]/research.md` con `tests/lib/validate-citation.sh`. Reporta los errores con paths concretos y exit ≠ 0 si alguno falla.

**Subcomando `close`**

- **FR-014**: `wom close` MUST ejecutar la lógica de `writeonmars-close-project` (lectura de `findings.md` + manifest), devolver exit 0 si `closeable: true` y exit 1 con la lista estructurada de blockers si `closeable: false`.

**Subcomando `update`**

- **FR-015**: `wom update` MUST envolver `writeonmars-update` con flag `--yes` opcional para saltar la confirmación. La preservación de campos custom del manifest (signing_matrix, human_operators, language_primary, project_type) MUST mantenerse igual que en la skill envuelta.

**Subcomando `doctor`**

- **FR-016**: `wom doctor` MUST verificar la presencia y versión mínima de Bash 5, Git ≥2.30, jq, ajv-cli o python+jsonschema, y al menos un MCP de investigación detectado en la configuración del agente. Cada dependencia se reporta como `OK` con versión, `MISSING` con pista de instalación, o `WARN` con razón.

**Convenciones globales**

- **FR-017**: Los subcomandos que escriben (`new`, `brief`, `sign`, `update`, `close` cuando haga side effects) MUST usar lockfile en `.wom/lock` para evitar corrupción por sesiones concurrentes. Los de solo lectura (`status`, `validate`, `doctor`) corren sin bloqueo.
- **FR-018**: La salida de la CLI MUST ser localizable: español por defecto (idioma primario del framework), inglés cuando `LANG=en_*` o `WOM_LANG=en` esté seteado. v1 prioriza español; inglés puede diferirse a feature posterior si añade complejidad.
- **FR-019**: El binario `wom` MUST funcionar con dependencias mínimas obligatorias (Bash 5, jq, awk) y detectar herramientas opcionales (gum, fzf) en runtime para mejorar UX sin convertirlas en requisitos duros.

### Key Entities

- **Estado del proyecto**: representación derivada (no almacenada) que cruza `findings.md`, `checklists/pasada-N.md`, `chapters/[###]-titulo.md` y el manifest para producir el dashboard. La CLI no introduce un nuevo formato de archivo; solo lee y resume.
- **Lockfile**: archivo `.wom/lock` que registra el subcomando en curso, PID y timestamp. Se borra al terminar; si una sesión murió y dejó el lock, otra invocación detecta el PID y, si el proceso ya no existe, lo limpia.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: La operadora puede ir de un directorio vacío a un proyecto editorial listo para escribir el brief en menos de 30 segundos con `wom new` (target ambicioso; el cuello de botella real es el cuestionario).
- **SC-002**: `wom status` renderiza el dashboard de un proyecto con 8 capítulos en menos de 1 segundo en macOS / Linux modernos.
- **SC-003**: `wom close` produce el mismo veredicto (`closeable` + lista de blockers) que la skill nativa `writeonmars-close-project` en el 100% de los casos verificados (test de regresión sobre los pilotos archivados).
- **SC-004**: `wom sign` actualiza el checklist y deja el archivo en estado válido (parseable por `writeonmars-close-project`) sin pérdida de configuración del manifest en el 100% de las firmas válidas.
- **SC-005**: `wom doctor` reporta el estado de las cinco dependencias en menos de 2 segundos.
- **SC-006**: Los subcomandos núcleo (`new`, `brief`, `status`, `sign`, `close`, `validate`, `doctor`) MUST funcionar con dependencias estrictamente mínimas (Bash 5, jq, awk, Git). 0 dependencias adicionales hard-required.
- **SC-007**: La operadora completa un ciclo editorial completo (de `wom new` a `wom close`) sobre una guía de 3 capítulos sin abrir manualmente ningún archivo markdown del proyecto, salvo cuando la generación editorial real lo exija (brief, capítulos en redacción).
- **SC-008**: La CLI mantiene paridad de comportamiento con las skills envueltas: cualquier ajuste a `writeonmars-close-project`, `writeonmars-update` o `writeonmars-research` se refleja en los wrappers correspondientes mediante referencia al SKILL.md, no por duplicación de lógica.

## Assumptions

- **Idioma primario**: español. Inglés se difiere a feature posterior salvo que la complejidad sea baja (se evalúa en `/speckit-plan`).
- **Distribución de `wom`**: el binario se entrega dentro del repositorio canónico en `bin/wom`; el instalador hace el binario disponible en el `$PATH` del proyecto destino vía symlink o `eval "$(./bin/wom env)"` (decisión técnica de plan).
- **Sin reescritura de skills**: la CLI envuelve `writeonmars-*`; no duplica la lógica de las skills. Cualquier cambio en una skill se refleja automáticamente en la CLI vía referencia (FR-027 del framework).
- **Dependencias mínimas**: Bash 5, jq, awk, Git ≥2.30. Python 3 y/o ajv-cli son recomendados para `validate`. `gum` y `fzf` son opcionales para mejorar UX.
- **`$EDITOR`**: la operadora tiene un editor configurado o acepta `vi` como fallback.
- **Agente externo**: la CLI no lanza el agente; imprime prompts pegables. La operadora invoca el agente por separado (Claude Code, otro). Esto preserva la portabilidad declarada en FR-023/FR-024 del framework.
- **Sandbox del piloto**: las rutas gitignored se excluyen del cómputo de `status` (no contaminan la vista del proyecto principal).
- **Estado en memoria**: la CLI no mantiene estado persistente más allá del lockfile; cada invocación lee el repo desde cero. La fuente de verdad sigue siendo el repositorio (FR-021 del framework).
- **Operadores humanos**: la firma usa el primer operador de `human_operators[]` por defecto; se puede sobreescribir con `--operator <id>`. Si el manifest no declara operadores, los subcomandos que firman fallan con mensaje claro.

## Dependencies

- Framework Write.OnMars v1.0.0 instalado en el proyecto destino (skills, scripts, contratos).
- Constitución v1.1.0 vigente para la matriz default de firmas.
- `tests/smoke/run-all.sh` y `tests/smoke/update-skill-on-installed-project.sh` operativos como inputs de `wom validate`.
- `tests/lib/validate-citation.sh` operativo como input de `wom validate`.
- Las skills `writeonmars-{install, update, brief, research, redaccion, contraste, pasada-1..5, close-project}` operativas en `.claude/skills/` o agente equivalente.
