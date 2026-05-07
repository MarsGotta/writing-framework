# Phase 0 Research: CLI `wom` para operar Write.OnMars

**Feature**: 002-wom-cli | **Date**: 2026-05-07

Decisiones técnicas que el plan deja "fijas" antes de Phase 1. Cada una sigue Decision / Rationale / Alternatives / Coverage.

---

## R1. Distribución del binario en el `$PATH` del proyecto destino

**Decision**: el instalador (`install/install.sh`) crea un **symlink** desde `<target>/bin/wom` apuntando al `bin/wom` del repo canónico (path absoluto), y añade `<target>/bin` al `$PATH` mediante una entrada en el archivo de contexto del agente (`CLAUDE.md`/`AGENTS.md`) y un comentario en `README.md` del proyecto destino. La operadora puede invocar `wom <sub>` desde cualquier subdirectorio del proyecto sin shell munging adicional.

**Rationale**:

- El symlink resuelve siempre el mismo binario canónico; bumps al canónico se propagan sin re-instalar.
- `<target>/bin` es local al proyecto editorial — no contamina el `$PATH` del sistema ni requiere `sudo`.
- Consistente con la convención Spec Kit (`<target>/.specify/scripts/bash/*.sh` también son scripts locales al proyecto).
- La instrucción de añadir al `$PATH` queda visible en el archivo de contexto del agente, que la operadora ya consulta.

**Alternatives considered**:

- **Instalación global del sistema** (`/usr/local/bin/wom`). Descartada: requiere `sudo`, pisa otras instalaciones, dificulta tener varias versiones del framework en distintos proyectos.
- **`eval "$(./bin/wom env)"`** que exporta el `$PATH` desde un comando del propio binario. Descartada: añade un paso no obvio para la operadora; el symlink es más directo.
- **Script shim que re-ejecuta el binario canónico**. Descartada: añade una capa sin valor sobre el symlink directo.

**Coverage**: FR-001, FR-003, SC-001.

---

## R2. Lockfile concurrente

**Decision**: lockfile en `<target>/.wom/lock` con formato JSON `{"pid": N, "subcommand": "...", "started_at": "..."}`. La adquisición usa `mkdir <target>/.wom/lock.d 2>/dev/null` (atómica en POSIX) como guardián; el archivo `.wom/lock` se escribe DENTRO del directorio. Liberación: `rm -rf .wom/lock.d` + `rm .wom/lock`. Stale detection: si el `pid` registrado ya no existe (`kill -0 $pid` falla), la siguiente invocación limpia el lock con un warning. Solo los subcomandos que escriben (`new`, `sign`, `update`, `close` con side effects) adquieren lock; los de lectura (`status`, `validate`, `doctor`, `brief` sin escritura) no.

**Rationale**:

- `mkdir` es atómico en todos los sistemas POSIX; no requiere `flock` (no portable a macOS sin Homebrew).
- El archivo JSON dentro del directorio guarda metadatos para diagnóstico sin complicar la atomicidad.
- Stale detection con `kill -0` es POSIX y funciona sin permisos elevados.
- Lectura sin lock evita falsos bloqueos cuando la operadora consulta `wom status` mientras otro proceso firma.

**Alternatives considered**:

- **`flock`**. Descartada: en macOS requiere `coreutils` o `util-linux` instalados aparte; rompe el principio de dependencias mínimas.
- **PID file plano sin atomicidad**. Descartada: race condition real cuando dos `wom sign` se invocan simultáneamente.
- **No usar lockfile**. Descartada: los pilotos editoriales pueden tener varias sesiones (operadora + asistente automatizado); corrupción del checklist por escritura concurrente es plausible.

**Coverage**: FR-017, edge case "dos sesiones simultáneas".

---

## R3. Renderizado del dashboard de `wom status`

**Decision**: `printf` + `awk` para alineación de columnas. Sin colores ANSI por defecto (consistente con sobriedad de la constitución § I); símbolos ASCII para estado: `OK`, `--`, `!`, `>` (pendiente firma humana). Si `gum` está disponible y `WOM_STATUS_RENDER=gum`, se usa `gum table` con bordes, pero sin emojis ni colores fuera del estricto contraste. Default: ASCII puro.

Formato fijo del dashboard:

```text
Proyecto: <nombre>  |  framework <vX.Y.Z>  |  pasadas humanas <firmadas>/<requeridas>
─────────────────────────────────────────────────────────────────
Cap  Título                          P1  P2  P3  P4  P5  Críticos
─────────────────────────────────────────────────────────────────
01   <título acortado a 30 chars>    OK  OK  >   --  --  0
02   ...
─────────────────────────────────────────────────────────────────
Leyenda: OK completado | > pendiente firma | ! bloqueador | -- no ejecutado
```

**Rationale**:

- Zero dependencias para el caso default (SC-006).
- El formato es pegable a cualquier issue, PR o nota; `gum` añade ergonomía sin convertirse en requisito.
- ASCII puro funciona en cualquier terminal (CI logs, ssh, terminales sin TrueColor).
- Alineación con `awk` es ~50 ms incluso con 20 capítulos; respeta SC-002 (<1 s).

**Alternatives considered**:

- **TUI completo con `textual` (Python)**. Descartada: viola dependencias mínimas.
- **`gum table` siempre**. Descartada: `gum` no es estándar; convertirlo en requisito rompería SC-006.
- **Colores ANSI por defecto**. Descartada: la constitución § I prefiere sobriedad; los colores aportan ruido cuando el operador tiene la salida pegada en un terminal o en un log.

**Coverage**: FR-011, FR-012, FR-019, SC-002, SC-006.

---

## R4. Mecanismo de firma en `wom sign`

**Decision**: cada `checklists/[###-feature]/pasada-N.md` lleva un bloque de firma delimitado por marcadores HTML al final del archivo:

```markdown
<!-- WOM-SIGN START -->
firma_tipo: human
firma_actor: marcela
firma_fecha: 2026-05-07
referencia_findings: ../../specs/[###-feature]/findings.md#pasada-N
<!-- WOM-SIGN END -->
```

`wom sign` reescribe el bloque entre los marcadores con `awk`. Si los marcadores no existen, los añade al final del archivo con un encabezado `## Firma`. La validación verifica que `firma_actor` esté en `manifest.human_operators[].id`.

**Rationale**:

- Marcadores HTML son robustos: parseables por la CLI y por humanos sin alterar el render markdown.
- `awk` reemplaza el rango entre marcadores de forma idempotente; reescribir el archivo entero con un patrón de sustitución es atómico.
- Convive con cualquier estructura previa del checklist (la skill `writeonmars-pasada-N` puede llenar el resto del archivo libremente).

**Alternatives considered**:

- **Front-matter YAML al inicio del archivo**. Considerada pero descartada: el resto del checklist (preguntas con `- [ ]`) no es YAML; mezclarlos crea fricción de parseo. El bloque al final es más limpio.
- **Archivo separado de firma** (`pasada-N.signature.json`). Descartada: rompe la coherencia del checklist; la operadora tendría que abrir dos archivos.
- **Editar in-place con `sed`**. Descartada: `sed -i` tiene incompatibilidades macOS/Linux (`sed -i ''` vs `sed -i`); `awk` con redirección a archivo temporal + `mv` es portable.

**Coverage**: FR-009, FR-010, SC-004.

---

## R5. Estrategia de testing

**Decision**: smoke tests en Bash puro siguiendo el patrón de `tests/smoke/install-on-empty-repo.sh`. Cada subcomando tiene su propio smoke en `tests/smoke/wom/<sub>.sh` que crea un sandbox con `mktemp -d`, ejecuta el subcomando con el flag `--non-interactive` o env vars `WOM_*`, y assertan side effects + exit codes. Un `tests/smoke/wom/run-all.sh` orquesta y reporta tabla de resultados. Reutilizan `install/lib/common.sh` para logging.

Test específico de paridad (`close-parity.sh`): toma los pilotos archivados de feature 001 (US2 ronda 3, US3) como fixture, ejecuta `wom close` sobre cada uno y verifica que el veredicto coincide con el `close-project-output.json` archivado.

**Rationale**:

- Bash puro mantiene cero dependencias adicionales (consistente con SC-006).
- El patrón ya está validado por feature 001 (`tests/smoke/run-all.sh`); reutilizar lo conocido reduce mantenimiento.
- La paridad con la skill nativa (SC-003) se verifica con datos reales de pilotos archivados, no con fixtures sintéticos.

**Alternatives considered**:

- **`bats`** (Bash Automated Testing System). Considerada y descartada: añade dependencia (instalar bats); el patrón Bash puro de feature 001 es suficiente para el alcance de la CLI.
- **`shunit2`**. Descartada por la misma razón.
- **Tests de integración con un agente real**. Descartada para v1: `wom` no invoca al agente; los smoke tests solo verifican la frontera CLI ↔ filesystem ↔ scripts del framework.

**Coverage**: FR-002, FR-013, SC-003, SC-008.

---

## R6. Internacionalización

**Decision**: v1 es **monolingüe en español**. Los mensajes están escritos directamente en los scripts. Si en el futuro `LANG=en_*` o `WOM_LANG=en` se detecta, la CLI muestra los mensajes en inglés vía un lookup table simple (`bin/wom-lib/i18n/<lang>.sh` con función `t "key"`). v1 NO implementa el lookup; solo declara la convención y deja `bin/wom-lib/i18n/es.sh` como base implícita (mensajes literales en los scripts).

**Rationale**:

- Internacionalización con gettext + `.po` files añade complejidad sustancial para un beneficio incierto (la operadora primaria es hispanohablante).
- Diferir es honesto: el día que haya un usuario monolingüe en inglés, se introduce el lookup en feature 003.
- No se cierra la puerta: la convención `WOM_LANG` queda documentada y los scripts se redactan con un único idioma por archivo, lo que facilita el switch posterior.

**Alternatives considered**:

- **gettext con `.po` files**. Descartada para v1: mantener traducciones frescas requiere disciplina que no compensa antes de tener al menos un usuario que las pida.
- **Lookup table embebido en cada script**. Descartada: contamina cada subcomando con lógica de i18n innecesaria.
- **Hardcodear inglés en lugar de español**. Descartada: el framework es primordialmente español por constitución § Propósito y alcance.

**Coverage**: FR-018, Assumption "v1 español".

---

## Resumen de decisiones

| Ref | Decisión | FR/SC cubiertas |
|-----|----------|-----------------|
| R1  | Symlink en `<target>/bin` + entrada `$PATH` documentada | FR-001, FR-003, SC-001 |
| R2  | Lockfile con `mkdir` atómico + JSON metadata + stale detection | FR-017 |
| R3  | Dashboard con `printf` + `awk` (ASCII default; `gum` opcional) | FR-011, FR-012, FR-019, SC-002, SC-006 |
| R4  | Bloque de firma con marcadores HTML reescrito por `awk` | FR-009, FR-010, SC-004 |
| R5  | Smoke tests en Bash puro reutilizando el patrón de feature 001 | FR-002, FR-013, SC-003, SC-008 |
| R6  | v1 monolingüe español; convención `WOM_LANG` documentada para futuro | FR-018 |

Sin `NEEDS CLARIFICATION` pendientes. Phase 1 puede arrancar.
