---
name: writeonmars-install
description: Instala el harness Write.OnMars sobre un repositorio Git destino. Trigger cuando el usuario diga "instala write.onmars", "writeonmars init", "configura write.onmars en este repo", "agrega write.onmars al proyecto" o frases equivalentes.
allowed-tools: Bash, Read, Write
---

# writeonmars-install

Skill canónica que envuelve `install/install.sh` para que un agente compatible
con skills (Claude Code v1) pueda instalar el harness Write.OnMars sobre un
repo Git destino sin que la persona operadora tenga que recordar la sintaxis
del script.

## Cuándo dispararse

Activate esta skill si la persona dice cualquiera de las frases siguientes (o
equivalentes en español):

- "instala write.onmars"
- "writeonmars init"
- "configura write.onmars en este repo"
- "agrega write.onmars al proyecto"
- "monta el harness editorial"

NO actives la skill si el repositorio destino ya tiene
`.writeonmars-manifest.json`; en ese caso confirma con la persona si quiere
re-ejecutar la instalación con `--force` antes de proceder.

## Qué hace, en alto nivel

1. Comprueba precondiciones: Bash 5+, Git 2.30+, repo Git inicializado en el
   directorio destino.
2. Detecta artefactos preexistentes (Spec Kit ya instalado, CLAUDE.md previo,
   `.writeonmars-manifest.json` previo) y emite un reporte JSON.
3. Copia las skills bundled (`marcela-prose`, `technical-guide-design`,
   `writeonmars-*`) al destino (o las enlaza si se pide `--symlink`).
4. Copia `.specify/memory/constitution.md` y las plantillas Spec Kit que
   falten (sin sobreescribir las que ya existan).
5. Registra los hooks Git de Spec Kit (`extensions.yml` + `extensions/git/`).
6. Lanza un cuestionario de cinco preguntas (tipo de proyecto, agente, idioma,
   audiencia, dominio, operador humano) y genera o fusiona `CLAUDE.md` /
   `AGENTS.md` entre los marcadores `<!-- WRITEONMARS START -->` y
   `<!-- WRITEONMARS END -->`.
7. Genera y valida `.writeonmars-manifest.json` contra
   `contracts/manifest-schema.json`.

## Cómo invocar el script

Ruta del script en el repo canónico:
`<framework_home>/install/install.sh`. Ejemplo de invocación:

```bash
bash "$WRITING_FRAMEWORK_HOME/install/install.sh" \
  --target-dir "$(pwd)" \
  --agent claude-code \
  --language es
```

Flags soportados:

| Flag | Descripción |
|------|-------------|
| `--target-dir <path>` | Repo Git destino (obligatorio). |
| `--agent <name>` | `claude-code` (default), `codex`, `cursor`, `other`. |
| `--language <iso>` | Idioma primario, por defecto `es`. |
| `--symlink` | Enlaza skills en lugar de copiarlas (modo desarrollo). |
| `--non-interactive` | Salta el cuestionario y usa env vars `WOM_*`. |
| `--force` | Sobreescribe skills aunque difiera la versión destino. |

Variables de entorno relevantes en modo no interactivo:

```bash
WOM_PROJECT_TYPE=guia        # guia|manual|libro|articulo|tutorial
WOM_AUDIENCE="..."           # ≥ 20 caracteres
WOM_DOMAIN="..."             # texto libre
WOM_OPERATOR_ID=marcela.gotta
WOM_OPERATOR_EMAIL=marcela@example.com
```

## Cuestionario interactivo

El script preguntará en orden:

1. Tipo de proyecto editorial (`guia` por defecto).
2. Agente prioritario (default tomado del flag `--agent`).
3. Idioma primario (default tomado del flag `--language`).
4. Audiencia general (texto libre, mínimo 20 caracteres).
5. Dominio técnico (texto libre).
6. Identificador del operador humano (ej. `marcela.gotta`).
7. Email del operador humano (formato válido).

## Cómo verificar que la instalación tuvo éxito

Tras ejecutar el script, comprueba que existan en el destino:

- `.writeonmars-manifest.json` (validado contra `contracts/manifest-schema.json`).
- `.claude/skills/marcela-prose/`
- `.claude/skills/technical-guide-design/`
- `.claude/skills/writeonmars-install/`
- `.specify/memory/constitution.md`
- `.specify/templates/spec-template.md` (y resto de plantillas)
- `.specify/extensions.yml`
- Bloque `<!-- WRITEONMARS START --> ... <!-- WRITEONMARS END -->` en
  `CLAUDE.md` (o `AGENTS.md`).

## Errores comunes y exit codes

| Exit | Causa | Cómo resolver |
|------|-------|---------------|
| 10 | Bash <5, Git ausente, target no es repo Git, flag desconocido. | Ejecuta `git init` o instala las herramientas requeridas. |
| 20 | Conflicto irresoluble de versión Write.OnMars previa. | Re-ejecuta con `--force` si es seguro. |
| 30 | Falla en copy-skills. | Revisa permisos del directorio `.claude/skills/`. |
| 40 | Cuestionario abortado o respuestas inválidas. | Re-ejecuta sin `--non-interactive` o corrige las env vars `WOM_*`. |
| 50 | El manifiesto no validó contra el JSON Schema. | Revisa la salida; suele indicar un campo faltante o mal formado. |
| 60 | Falla en hook registration. | Verifica que `.specify/extensions/git/` tenga permisos de escritura. |

## Referencias

- `install/install.sh` — entry point.
- `install/lib/common.sh` — utilidades compartidas.
- `install/lib/detect-existing.sh` — detección.
- `install/lib/copy-skills.sh` — copia de skills.
- `install/lib/render-context.sh` — cuestionario y `CLAUDE.md`.
- `install/lib/render-manifest.sh` — manifiesto JSON.
- `contracts/manifest-schema.json` — schema canónico del manifiesto.
- `docs/installation.md` — guía completa para mantenedores y operadores.
