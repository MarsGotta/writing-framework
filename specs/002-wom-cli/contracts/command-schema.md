# Command Schema v1.0 — CLI `wom`

**Status**: stable for Write.OnMars CLI v1.
**Cobertura**: FR-001, FR-002, FR-018.

Contrato unificado de la CLI `wom`. Es la fuente de verdad de `--help`, de los smoke tests y de cualquier wrapper externo. Cada subcomando declara: nombre, sintaxis, flags, exit codes, precondiciones y side effects.

---

## Convenciones globales

- **Idioma**: español (v1).
- **Tono de mensajes**: sobrio (constitución § I). Sin emojis. Sin lenguaje promocional.
- **Estructura de errores**: `[wom][<sub>] error: <qué pasó>. <causa>. <acción sugerida>.`
- **Exit codes generales** (cualquier subcomando puede usarlos):
  - `0`: éxito.
  - `1`: fallo lógico esperado (validación, blocker, conflicto).
  - `2`: invocación incorrecta (flags malos, args faltantes).
  - `10`: precondición no cumplida (no es un proyecto Write.OnMars instalado, manifest corrupto).
  - `20`: lock no adquirible (otra sesión activa).
- **Flags compartidos**:
  - `--help`, `-h`: ayuda específica del subcomando.
  - `--version`: imprime la versión de `wom` y del framework.
  - `--non-interactive`: salta cuestionarios usando env vars `WOM_*` (consistente con `install.sh`).
  - `--format=json|text`: formato de salida. Default `text`.
- **Lectura de proyecto activo**: la CLI busca `.writeonmars-manifest.json` subiendo desde el `cwd` (`git rev-parse --show-toplevel` como fallback).

---

## `wom new <nombre>`

**Sintaxis**: `wom new <nombre> [--agent <id>] [--language <iso>] [--non-interactive]`

**Precondición**: `<nombre>` no existe como directorio o existe vacío.

**Flags**:

| Flag | Default | Descripción |
|------|---------|-------------|
| `--agent` | `claude-code` | Agente prioritario (consistente con `install.sh --agent`). |
| `--language` | `es` | Idioma primario del proyecto editorial. |
| `--non-interactive` | off | Lee env vars `WOM_*` en lugar de preguntar. |

**Side effects**:

1. `mkdir <nombre>`.
2. `cd <nombre> && git init`.
3. Invoca `install/install.sh --target-dir <pwd> --agent <agent> --language <lang>`.
4. Lockfile NO se adquiere (no hay manifest aún).

**Exit codes**: `0` éxito; `1` directorio existe con contenido; `2` flag inválido; `10` `install.sh` falló.

**Ejemplo**:

```bash
wom new mi-guia-onboarding --agent claude-code --language es
# → crea ./mi-guia-onboarding/, instala framework, deja repo listo para wom status.
```

---

## `wom brief`

**Sintaxis**: `wom brief [--feature <id>]`

**Precondición**: proyecto Write.OnMars instalado. Si no hay feature directory, abortar con sugerencia (`Ejecuta /speckit-specify primero, o wom new si arrancas un proyecto nuevo.`).

**Flags**:

| Flag | Default | Descripción |
|------|---------|-------------|
| `--feature` | feature activa de `.specify/feature.json` | Override del feature directory. |

**Side effects**: abre `<feature_directory>/spec.md` en `$EDITOR`. Si `$EDITOR` no está seteado, fallback a `vi`. Si tampoco existe, exit `10` con mensaje claro.

**Exit codes**: `0` editor cerró sin error; `10` precondición fallida; `2` flag inválido.

---

## `wom research`, `wom plan`, `wom draft N`, `wom review <pasada> <capítulo>`

**Sintaxis**:

- `wom research [--feature <id>]`
- `wom plan [--feature <id>]`
- `wom draft <N> [--parallel <K>] [--feature <id>]`
- `wom review <pasada> <capítulo> [--feature <id>]`

**Precondición**: proyecto Write.OnMars instalado.

**Flags específicos de `wom draft`**:

| Flag | Default | Descripción |
|------|---------|-------------|
| `--parallel` | off | Modo paralelo con K sub-agentes (K ∈ [2, 8]). |

**Side effects**: ninguno (solo lectura). Imprime por stdout un `PromptFormateado` (data-model.md § 4) listo para pegar en el agente.

**Exit codes**: `0` prompt impreso; `10` precondición; `2` argumento inválido (`<pasada>` ∉ [1..5], `<capítulo>` no existe en `chapters/`).

**Ejemplo de salida** (`wom draft 2 --parallel 2`):

```text
== Prompt para writeonmars-redaccion ==
Capítulo: 2 (parallel=2)

Contexto:
- Brief:    /Users/.../specs/001-mi-guia/spec.md
- Temario:  /Users/.../specs/001-mi-guia/plan.md § Temario
- Glosario: /Users/.../specs/001-mi-guia/glossary.md

Instrucción:
Invoca /writeonmars-redaccion --parallel 2 sobre el capítulo 2.
Sigue el prompt canónico en agents/claude/prompts/redaccion.md.
Salida esperada: chapters/002-<titulo>.md con front-matter + 9 secciones.
```

---

## `wom sign <pasada> <capítulo>`

**Sintaxis**: `wom sign <pasada> <capítulo> [--operator <id>] [--force] [--note "<razón>"] [--type <tipo>]`

**Precondición**: proyecto instalado; `<feature_directory>/checklists/pasada-<N>.md` existe; `manifest.human_operators[]` no está vacío.

**Flags**:

| Flag | Default | Descripción |
|------|---------|-------------|
| `--operator` | `human_operators[0].id` | id del firmante. |
| `--force` | off | Sobreescribe firma existente. |
| `--note` | (vacío) | Texto libre, requerido si `--type=desviacion_justificada`. |
| `--type` | `human` | `human` \| `autonomous` \| `desviacion_justificada`. |

**Side effects**: adquiere lockfile, reescribe el bloque entre marcadores `<!-- WOM-SIGN START --> ... END -->` en el checklist; libera lockfile.

**Exit codes**: `0` firma escrita; `1` firma duplicada sin `--force`; `1` `--operator` no listado en manifest; `2` argumento inválido; `10` precondición; `20` lock no adquirible.

**Ejemplo**:

```bash
wom sign 3 2                          # firma pasada 3 capítulo 2 con el primer operador del manifest
wom sign 3 2 --force                  # sobrescribe
wom sign 4 1 --type desviacion_justificada --note "fuente offline; verificación pendiente"
```

---

## `wom status`

**Sintaxis**: `wom status [--feature <id>] [--format=text|json]`

**Precondición**: proyecto instalado.

**Side effects**: ninguno. Lee manifest, findings, checklists, chapters; renderiza dashboard.

**Exit codes**: `0` dashboard impreso; `10` precondición.

**Ejemplo de salida** (`text`):

```text
Proyecto: mi-guia-onboarding  |  framework 1.0.0  |  pasadas humanas 2/6
─────────────────────────────────────────────────────────────────
Cap  Título                          P1  P2  P3  P4  P5  Críticos
─────────────────────────────────────────────────────────────────
01   Lectura estratégica             OK  OK  OK  OK  OK  0
02   Mapa mental del dominio         OK  OK  >   --  --  0
03   Primer cambio sin romper        OK  OK  --  --  --  1
─────────────────────────────────────────────────────────────────
Leyenda: OK completado | > pendiente firma | ! bloqueador | -- no ejecutado
Críticos abiertos totales: 1 (capítulo 3, pasada 1)
```

---

## `wom validate`

**Sintaxis**: `wom validate [--feature <id>] [--quick]`

**Precondición**: proyecto instalado.

**Flags**:

| Flag | Default | Descripción |
|------|---------|-------------|
| `--quick` | off | Salta los smoke tests del framework; solo valida manifest + citations. |

**Side effects**: ninguno. Ejecuta `tests/smoke/run-all.sh` (a menos que `--quick`), valida manifest contra schema, valida cada `CitationRecord` de `research.md`.

**Exit codes**: `0` todo verde; `1` algún fallo (lista los archivos y campos violados); `10` precondición.

---

## `wom close`

**Sintaxis**: `wom close [--feature <id>] [--format=text|json] [--strict]`

**Precondición**: proyecto instalado.

**Flags**:

| Flag | Default | Descripción |
|------|---------|-------------|
| `--strict` | off | Trata `firma_tipo=desviacion_justificada` como blocker (más estricto que la skill nativa). |

**Side effects**: adquiere lockfile lectura-segura (no escribe). Computa `ResultadoCierre`.

**Exit codes**: `0` `closeable=true`; `1` `closeable=false`; `10` precondición; `20` lock.

**Ejemplo de salida** (`text`):

```text
Proyecto cerrable: NO
Blockers (2):
  1. Crítico abierto: pasada 1, capítulo 3, finding F-1.2
     "<frase original>"
  2. Firma humana faltante: pasada 4, capítulo 2 (firma autonomous donde matriz exige human)
```

---

## `wom update`

**Sintaxis**: `wom update [--yes] [--dry-run]`

**Precondición**: proyecto instalado.

**Flags**:

| Flag | Default | Descripción |
|------|---------|-------------|
| `--yes` | off | Salta la confirmación interactiva. |
| `--dry-run` | off | Muestra el diff sin aplicar. |

**Side effects**: adquiere lockfile, ejecuta lógica de la skill `writeonmars-update`, libera lockfile.

**Exit codes**: `0` actualización aplicada o sin cambios; `1` conflicto irresoluble; `10` precondición; `20` lock.

---

## `wom doctor`

**Sintaxis**: `wom doctor [--format=text|json]`

**Precondición**: ninguna; el comando funciona incluso fuera de un proyecto.

**Side effects**: ninguno. Verifica disponibilidad y versiones.

**Verificaciones**:

| Verificación | Tipo | Falla si |
|--------------|------|---------|
| Bash ≥ 5 | hard | versión menor |
| Git ≥ 2.30 | hard | binario faltante o versión menor |
| jq ≥ 1.6 | hard | binario faltante o versión menor |
| awk (POSIX) | hard | binario faltante |
| Validador de schema | soft | ni `python3+jsonschema` ni `npx ajv-cli` disponibles |
| `gum` | optional | binario faltante (warning, no falla) |
| `fzf` | optional | binario faltante (warning, no falla) |
| MCP de investigación | soft | ningún MCP detectable en la configuración del agente |

**Exit codes**: `0` todo OK o solo warnings opcionales; `1` falta una dependencia hard; `10` falla soft + bandera `--strict` (futuro).

---

## `wom --help` / `wom <sub> --help`

**Comportamiento**: imprime uso, descripción, flags, exit codes y un ejemplo. Para `wom --help` lista todos los subcomandos con una línea cada uno.

**Exit codes**: siempre `0`.

---

## Variables de entorno reconocidas

| Variable | Subcomandos | Descripción |
|----------|-------------|-------------|
| `WOM_LANG` | global | `es` (default) o `en` (futuro). |
| `WOM_PROJECT_TYPE` | `new` | `guia|manual|libro|articulo|tutorial`. |
| `WOM_AUDIENCE` | `new` | Audiencia general (≥20 chars). |
| `WOM_DOMAIN` | `new` | Dominio técnico. |
| `WOM_OPERATOR_ID` | `new`, `sign` | id del operador humano. |
| `WOM_OPERATOR_EMAIL` | `new` | email del operador humano. |
| `WOM_STATUS_RENDER` | `status` | `ascii` (default) o `gum` si está disponible. |
| `WOM_NO_LOCK` | escritores | Si está set, salta el lockfile (solo testing/CI; produce warning). |
| `EDITOR` | `brief` | Editor para abrir spec.md. |

---

## Versionado del schema

- **MAJOR**: cambio incompatible (rename de subcomando, cambio de exit code).
- **MINOR**: nuevo subcomando o flag opcional.
- **PATCH**: aclaraciones, ejemplos, mensajes.

`wom --version` imprime la versión del schema seguida de la versión del framework.
