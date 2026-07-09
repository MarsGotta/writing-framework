---
name: writeonmars-update
description: Actualiza una skill canónica del framework Write.OnMars en un proyecto editorial instalado. Compara versiones, presenta diff y aplica la actualización preservando configuración local. Trigger cuando la persona diga "actualiza writeonmars", "writeonmars update", "bump skill X", "sincroniza framework con canónico".
allowed-tools: Bash, Read, Write, Edit
---

# writeonmars-update

Skill canónica que sincroniza un proyecto editorial instalado con el repo
canónico de Write.OnMars. Compara las versiones declaradas en
`<target>/.writeonmars-manifest.json#skills[]` contra los archivos `VERSION`
del repo canónico, presenta el diff por skill y aplica la actualización con
confirmación, preservando la configuración local del manifiesto.

Cubre SC-008 (un bump de versión de skill se propaga a un proyecto instalado
en menos de 15 minutos sin pérdida de configuración local) y FR-028.

## Cuándo dispararse

Activate esta skill si la persona dice cualquiera de las frases siguientes (o
equivalentes):

- "actualiza writeonmars"
- "writeonmars update"
- "bump skill X"
- "sincroniza framework con canónico"
- "trae las skills nuevas del repo canónico"
- "propaga el bump de la skill X al proyecto"

NO actives la skill si:

- El destino no tiene `.writeonmars-manifest.json` (es decir, el proyecto no
  está instalado). En ese caso redirige a `writeonmars-install`.
- La variable `WRITEONMARS_HOME` no está definida y no se pasa `--framework-home`.

## Qué hace, en alto nivel

1. Lee `<target>/.writeonmars-manifest.json` y construye un mapa
   `nombre_skill → versión_proyecto`.
2. Resuelve `WRITEONMARS_HOME` (env var) o `--framework-home <path>` (flag) y
   lee los archivos `VERSION` de cada `.claude/skills/<skill>/VERSION` del repo
   canónico para construir el mapa `nombre_skill → versión_canónica`.
3. Calcula el diff por skill: `same`, `update_available`,
   `local_ahead_of_canonical` (raro; warning), `missing_in_canonical`.
4. Imprime una tabla con: skill, versión proyecto, versión canónica, acción
   propuesta, archivos que se añadirían o sobreescribirían.
5. Pide confirmación interactiva. Saltable con `--yes`.
6. Aplica las actualizaciones:
   - Para cada skill con `update_available`, copia los archivos del canónico al
     destino reemplazando `SKILL.md` y `VERSION` y añadiendo cualquier archivo
     nuevo. NO borra archivos huérfanos del destino salvo `--prune`.
   - Bumpea la entrada correspondiente en `manifest.skills[]`.
7. Re-valida el manifiesto contra `contracts/manifest-schema.json`.
8. **Preservación de configuración local**: los siguientes campos del
   manifiesto se conservan tal como estén en el proyecto, aunque el canónico
   declare otros defaults: `signing_matrix` (cualquier customización),
   `human_operators[]` (lista completa), `language_primary`, `project_type`,
   `memory_external`, `writeonmars_research_module`, `research_mode`.

## Cómo invocar el script (sin script todavía: ejecución manual de los pasos)

La skill no envuelve un binario único en v1: ejecuta los pasos vía Bash. Se
implementa como serie de comandos:

```bash
# 1. Resolver canónico.
: "${WRITEONMARS_HOME:?Define WRITEONMARS_HOME o pasa --framework-home}"

# 2. Leer manifest del proyecto.
jq '.skills[] | {name, version}' "$TARGET/.writeonmars-manifest.json"

# 3. Para cada skill canónica, leer VERSION.
grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+' "$WRITEONMARS_HOME/.claude/skills/<skill>/VERSION"

# 4. Calcular diff (script o bucle interactivo).
# 5. Pedir confirmación.
# 6. cp -R "$WRITEONMARS_HOME/.claude/skills/<skill>/" "$TARGET/.claude/skills/<skill>/"
# 7. jq actualiza .skills[<i>].version en el manifest.
# 8. ajv-cli o python+jsonschema valida el manifest.
```

Flags soportados:

| Flag | Descripción |
|------|-------------|
| `--target-dir <path>` | Repo Git destino con manifest existente (obligatorio). |
| `--framework-home <path>` | Repo canónico de Write.OnMars. Default: `$WRITEONMARS_HOME`. |
| `--only <skill>[,<skill>...]` | Restringe la actualización a un subconjunto de skills. |
| `--yes` | Salta la confirmación interactiva. |
| `--dry-run` | Muestra el diff sin aplicar cambios. |
| `--prune` | Borra archivos huérfanos en el destino que no existan en el canónico. |

## Procedimiento (numerado)

1. **Leer manifest del proyecto.** Cargar
   `<target>/.writeonmars-manifest.json` con `jq` y construir
   `proyecto_skills`. Si el archivo no existe o no valida, abortar con exit 10.
2. **Resolver `WRITEONMARS_HOME`.** Tomar la variable de entorno o el flag
   `--framework-home`. Verificar que exista
   `$WRITEONMARS_HOME/.claude/skills/`. Si no, abortar con exit 11.
3. **Comparar VERSION canónico vs proyecto.** Para cada skill listada en el
   manifest:
   - Leer `$WRITEONMARS_HOME/.claude/skills/<skill>/VERSION` y extraer la
     primera línea (formato `vX.Y.Z[-suffix]` o `X.Y.Z`).
   - Normalizar a semver `X.Y.Z` para comparación.
   - Determinar acción: `same`, `update_available`, `local_ahead_of_canonical`
     o `missing_in_canonical`.
4. **Mostrar diff.** Imprimir tabla:

   ```text
   skill                     proyecto    canónico    accion
   ------------------------- ----------- ----------- -------------------
   marcela-prose             0.1.0       0.1.0       same
   writeonmars-pasada-1      0.1.0       0.2.0       update_available
   writeonmars-glossary      0.1.0       0.1.0       same
   ```

   Para cada skill con `update_available`, hacer `diff -r` resumido entre el
   directorio canónico y el del destino y listar archivos añadidos /
   modificados.

5. **Pedir confirmación.** A menos que se haya pasado `--yes`, preguntar
   `¿Aplicar las actualizaciones? [y/N]`. Si la respuesta no es `y` ni `Y`,
   abortar con exit 0 (no es error).
6. **Aplicar.** Para cada skill con `update_available`:
   - `cp -R` del canónico al destino. Si se pasó `--prune`, borrar primero los
     archivos del destino que no existan en el canónico.
   - Bumpear la versión en `manifest.skills[]` mediante `jq` con un archivo
     temporal y luego `mv`.
7. **Preservación.** Los campos `signing_matrix`, `human_operators[]`,
   `language_primary`, `project_type`, `memory_external`,
   `writeonmars_research_module` y `research_mode` se conservan tal como
   estaban antes de la operación. Solo se modifica `.skills[].version` (y, si
   aplica, `.skills[].source` cuando una skill nueva se haya añadido al
   canónico).
8. **Re-validar.** Pasar el manifest actualizado por `ajv-cli` (o
   `python+jsonschema`) contra `contracts/manifest-schema.json`. Si falla,
   restaurar el backup y abortar con exit 50.
9. **Reporte final.** Imprimir la lista de skills actualizadas, las versiones
   nuevas y el diff resumido del manifest.

## Inputs

- `<target>` con `.writeonmars-manifest.json` válido.
- `WRITEONMARS_HOME` o `--framework-home` apuntando al repo canónico de
  Write.OnMars.

## Outputs

- Skills actualizadas en `<target>/.claude/skills/<skill>/`.
- `<target>/.writeonmars-manifest.json` con `.skills[].version` bumpeada.
- Backup del manifest previo en
  `<target>/.writeonmars-manifest.json.bak` (sobreescribe el bak anterior si
  existe).

## Errores comunes y exit codes

| Exit | Causa | Cómo resolver |
|------|-------|---------------|
| 0 | Operación cancelada por la persona o no había updates pendientes. | Sin acción. |
| 10 | Manifest del proyecto ausente o inválido. | Re-ejecuta `writeonmars-install` o repara el manifest. |
| 11 | `WRITEONMARS_HOME` no resoluble. | Define la env var o pasa `--framework-home`. |
| 30 | Falla al copiar archivos de la skill. | Revisa permisos de `<target>/.claude/skills/`. |
| 40 | Conflicto en `--prune` (archivos locales modificados que se perderían). | Re-ejecuta sin `--prune` o resuelve manualmente. |
| 50 | El manifest actualizado no validó contra el schema. | El backup `.bak` se restaura automáticamente; reporta el error. |

## Preservación: ejemplo

Antes:

```json
{
  "language_primary": "es-AR",
  "signing_matrix": {
    "pasada_1_estructura": "human",
    "pasada_2_utilidad": "autonomous",
    "pasada_3_naturalidad": "human",
    "pasada_4_precision": "human",
    "pasada_5_formato": "autonomous"
  },
  "human_operators": [
    {"id": "marcela.gotta", "email": "marcela@example.com", "role": "editor"},
    {"id": "jose.tester", "email": "jose@example.com", "role": "reviewer"}
  ],
  "skills": [
    {"name": "writeonmars-pasada-1", "version": "0.1.0", "source": "bundled"}
  ]
}
```

Después de bumpear `writeonmars-pasada-1` a `0.2.0`:

```json
{
  "language_primary": "es-AR",
  "signing_matrix": {
    "pasada_1_estructura": "human",
    "pasada_2_utilidad": "autonomous",
    "pasada_3_naturalidad": "human",
    "pasada_4_precision": "human",
    "pasada_5_formato": "autonomous"
  },
  "human_operators": [
    {"id": "marcela.gotta", "email": "marcela@example.com", "role": "editor"},
    {"id": "jose.tester", "email": "jose@example.com", "role": "reviewer"}
  ],
  "skills": [
    {"name": "writeonmars-pasada-1", "version": "0.2.0", "source": "bundled"}
  ]
}
```

`signing_matrix.pasada_1_estructura` quedó como `human` aunque el default
canónico sea `autonomous`. La regla: el canónico declara defaults; el
proyecto declara la verdad operativa.

## Referencias

- `docs/maintenance/skill-update-procedure.md` — procedimiento operativo del
  mantenedor del framework.
- `tests/smoke/update-skill-on-installed-project.sh` — smoke test de SC-008.
- `contracts/manifest-schema.json` — schema canónico que se vuelve a validar
  tras el bump.
- FR cubierta: SC-008.
