# Quickstart: primer uso de la CLI `wom`

**Feature**: 002-wom-cli | **Date**: 2026-05-07

Recorrido de extremo a extremo desde un directorio vacío hasta cerrar un proyecto editorial usando `wom` para todo lo que no requiere generación editorial real.

---

## Prerrequisitos

- Repo canónico de Write.OnMars clonado en `~/repos/writing-framework` (o equivalente).
- Bash ≥ 5, Git ≥ 2.30, jq ≥ 1.6, awk POSIX.
- Un agente compatible (Claude Code v1) corriendo en otra ventana o invocable desde el shell.
- Opcionales: `gum`, `fzf`.

Verifica con:

```bash
~/repos/writing-framework/bin/wom doctor
```

Esperado: cinco entradas `OK` (Bash, Git, jq, awk, validador) y al menos una soft `MCP detectado`.

---

## Paso 1 — Arrancar un proyecto editorial

```bash
cd ~/proyectos
~/repos/writing-framework/bin/wom new mi-guia-onboarding \
  --agent claude-code \
  --language es \
  --non-interactive
```

Con `--non-interactive` y env vars `WOM_*`:

```bash
WOM_PROJECT_TYPE=guia \
WOM_AUDIENCE="developers con 2+ años que llegan a un repo legacy" \
WOM_DOMAIN="developer onboarding" \
WOM_OPERATOR_ID=marcela \
WOM_OPERATOR_EMAIL=marcelagotta@gmail.com \
~/repos/writing-framework/bin/wom new mi-guia-onboarding ...
```

Resultado: `./mi-guia-onboarding/` con repo Git inicializado, framework instalado, manifest válido y `bin/wom` disponible vía symlink en `./mi-guia-onboarding/bin/wom`.

**Acceptance**: US1 §AC1 + SC-001 (<30 segundos).

---

## Paso 2 — Verificar el estado inicial

```bash
cd mi-guia-onboarding
./bin/wom status
```

Esperado: dashboard con 0 capítulos, 0 firmas humanas (target 0/0 en proyecto vacío) y 0 críticos abiertos. La leyenda aparece debajo de la tabla.

---

## Paso 3 — Capturar el brief editorial

```bash
./bin/wom brief
```

Abre `specs/[###-feature]/spec.md` en `$EDITOR` con la plantilla de los nueve campos pre-rellenada. La operadora rellena los nueve campos (audiencia, problema, resultado, nivel, tono, conceptos obligatorios, ejemplo recurrente, riesgos, acciones prácticas) y guarda.

**Acceptance**: US5 §AC2.

---

## Paso 4 — Investigar con fuentes

```bash
./bin/wom research
```

Imprime un prompt completo para `/writeonmars-research`. La operadora lo pega en el agente. El agente ejecuta la skill, consulta MCPs y produce `specs/[###]/research.md`. Cuando termina, la operadora vuelve al shell.

---

## Paso 5 — Producir temario y descripciones encadenadas

```bash
./bin/wom plan
```

Imprime el prompt para `/writeonmars-temario` + `/writeonmars-descripciones`. La operadora lo pega en el agente. El agente actualiza `plan.md` con las dos secciones.

---

## Paso 6 — Redactar capítulo a capítulo

Para cada capítulo:

```bash
./bin/wom draft 1                  # serial
./bin/wom draft 1 --parallel 2     # paralelo (cuando hay >= 4 capítulos)
```

Imprime el prompt para `/writeonmars-redaccion`. La operadora lo pega en el agente. El agente redacta `chapters/001-titulo.md`.

Puede consultar el estado en cualquier momento:

```bash
./bin/wom status
```

---

## Paso 7 — Ejecutar las cinco pasadas

Para cada capítulo, secuencialmente:

```bash
./bin/wom review 1 1   # pasada 1 sobre capítulo 1
./bin/wom review 2 1
./bin/wom review 3 1
./bin/wom review 4 1
./bin/wom review 5 1
```

Cada `review` imprime el prompt canónico de `agents/claude/prompts/pasada-N.md` con referencias al capítulo objetivo y al `findings.md` actual. El agente ejecuta la pasada, escribe en `findings.md` y deja el checklist correspondiente.

**Acceptance**: US5 §AC3.

---

## Paso 8 — Firmar las pasadas humanas

Para cada checklist de pasadas 3 y 4 (matriz default v1: ambas humanas):

```bash
./bin/wom sign 3 1                          # firma pasada 3 capítulo 1
./bin/wom sign 4 1                          # firma pasada 4 capítulo 1
./bin/wom sign 3 1 --force                  # sobreescribir si ya firmada
./bin/wom sign 4 1 --type desviacion_justificada --note "fuente offline"
```

`wom sign` adquiere lockfile, escribe el bloque WOM-SIGN entre marcadores HTML al final del checklist y libera el lockfile.

**Acceptance**: US4 §AC1, §AC2, §AC3.

---

## Paso 9 — Validar el proyecto

```bash
./bin/wom validate
```

Ejecuta:

1. `tests/smoke/run-all.sh` (si los smokes existen en el proyecto destino).
2. Validación de `.writeonmars-manifest.json` contra el schema.
3. Validación de cada `CitationRecord` en `specs/[###]/research.md` con `tests/lib/validate-citation.sh`.

Sale con `exit 0` si todo verde, `exit 1` con la lista de archivos y campos violados si algo falla.

---

## Paso 10 — Cerrar el proyecto

```bash
./bin/wom close
```

Lee `findings.md` + manifest. Devuelve:

- `exit 0` con mensaje `Proyecto cerrable` cuando no hay críticos abiertos ni firmas humanas pendientes.
- `exit 1` con lista estructurada de blockers cuando hay alguno.

**Acceptance**: US3 §AC1, §AC2, §AC3.

---

## Validación de éxito (mapeo a Success Criteria)

| Criterio | Cómo se valida |
|----------|----------------|
| SC-001 (`wom new` <30 s) | Cronometrar Paso 1 con `time`. |
| SC-002 (`wom status` <1 s con 8 capítulos) | Producir un proyecto sintético con 8 caps; cronometrar. |
| SC-003 (paridad con writeonmars-close-project) | `tests/smoke/wom/close-parity.sh` sobre los pilotos archivados de feature 001. |
| SC-004 (`wom sign` deja archivo válido) | `tests/smoke/wom/sign.sh` verifica que el bloque WOM-SIGN se escribe correctamente y `writeonmars-close-project` lo lee. |
| SC-005 (`wom doctor` <2 s) | Cronometrar Paso 0 con `time`. |
| SC-006 (deps mínimas) | Ejecutar la pipeline en un container alpine con solo Bash, jq, awk, Git. |
| SC-007 (ciclo completo sin abrir markdown manual) | Recorrer Pasos 1–10 contando archivos abiertos manualmente (esperado: solo `spec.md` en Paso 3 y los chapters durante redacción real). |
| SC-008 (paridad con skills envueltas) | Tests de regresión sobre los pilotos archivados; cualquier diff con la skill nativa falla el test. |

---

## Resolución de problemas frecuentes

- **`wom` no se encuentra**: el symlink no se añadió al `$PATH`. Solución: `export PATH="$PWD/bin:$PATH"` desde la raíz del proyecto, o añadir esa línea al `CLAUDE.md`/perfil del shell.
- **`Lock no adquirible`** (exit 20): otra sesión de `wom` está activa. Si el PID reportado ya no existe, `wom` lo limpia automáticamente en la siguiente invocación. Si persiste, `rm -rf .wom/lock.d .wom/lock` manualmente y reintenta.
- **`Manifest corrupto`** (exit 10): valida con `wom validate`. Si el campo violado es identificable, edita el manifest manualmente; si no, restaura desde el último commit.
- **`firma_actor no listado en human_operators`**: añade el operador al manifest (`jq '.human_operators += [{...}]' manifest.json`) o usa `--operator <id>` con un id ya listado.
- **`$EDITOR no configurado`**: `export EDITOR=nano` (o tu favorito) antes de invocar `wom brief`.
- **`gum table` falla pero el dashboard funciona**: ignora; el render gum es opcional.
