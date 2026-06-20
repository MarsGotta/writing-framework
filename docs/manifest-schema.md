# Manifiesto del proyecto editorial

Audiencia: personas que mantienen Write.OnMars y operadores que crean o auditan proyectos editoriales. Para el schema autoritativo, ver `contracts/manifest-schema.json`. Este documento explica cada campo con ejemplos y notas operativas.

El manifiesto vive en la raíz del proyecto editorial (no de este repo canónico) en `.writeonmars-manifest.json`. Lo produce `bootstrap.py` (`/speckit-setup`) tras instalar el preset y se actualiza cuando cambian versiones, matriz de firmas u operadores autorizados.

## Estructura general

El manifiesto es un único objeto JSON con campos obligatorios y opcionales. La validación se hace contra `contracts/manifest-schema.json` con `ajv`. La política `additionalProperties: false` significa que campos desconocidos rompen la validación: para añadir un campo nuevo hay que bumpear el schema (ver § "Notas de migración").

Ejemplo mínimo válido:

```json
{
  "framework_version": "1.0.0",
  "constitution_version": "1.1.0",
  "agent_target": "claude-code",
  "language_primary": "es",
  "skills": [
    {"name": "marcela-prose", "version": "0.1.0", "source": "bundled"},
    {"name": "technical-guide-design", "version": "0.1.0", "source": "bundled"}
  ],
  "research_mode": "byom",
  "signing_matrix": {
    "pasada_1_estructura": "autonomous",
    "pasada_2_utilidad": "autonomous",
    "pasada_3_naturalidad": "human",
    "pasada_4_precision": "human",
    "pasada_5_formato": "autonomous"
  },
  "human_operators": [
    {"id": "marcela", "email": "marcela@example.com", "role": "author"}
  ],
  "citation_contract_version": "1.0",
  "project_type": "editorial",
  "sector": "tecnologia"
}
```

> **Nota (constitución por capas, v1.3.0).** El `bootstrap.py` actual escribe
> `project_type` y `sector` (este último `null` hasta que `speckit.constitution`
> lo fije). `constitution_version` referencia el **núcleo** versionado; las
> **adendas del proyecto** (tono, terminología, relajaciones por sector) viven en
> `.specify/memory/constitution.md` § Adendas, no en el manifiesto.

## Campos obligatorios

### `framework_version`

- **Tipo**: string semver (`X.Y.Z`).
- **Default**: `bootstrap.py` lo rellena con la versión del preset desde el que se instaló.
- **Ejemplo**: `"1.0.0"`.
- **Notas**: identifica la versión de Write.OnMars instalada en este proyecto. Permite calcular el diff cuando el preset sube de versión.

### `constitution_version`

- **Tipo**: string semver.
- **Default**: la versión declarada al final de `.specify/memory/constitution.md` en el repo canónico al instalar.
- **Ejemplo**: `"1.1.0"`.
- **Notas**: la constitución y el framework versionan por separado. Un proyecto puede operar con una constitución más antigua que la última publicada si lo decide explícitamente.

### `agent_target`

- **Tipo**: string del enum `claude-code` | `codex` | `cursor` | `other`.
- **Default**: `claude-code` (única implementación canónica en v1; el resto figura como `planned` en `docs/compatibility-matrix.md`).
- **Ejemplo**: `"claude-code"`.
- **Notas**: define qué adaptador en `agents/<name>/prompts/` se carga. Para `other`, el operador debe portar adaptador y declararlo manualmente.

### `language_primary`

- **Tipo**: string ISO-639 con región opcional (`^[a-z]{2}(-[A-Z]{2})?$`).
- **Default**: `es`.
- **Ejemplo**: `"es"`, `"es-AR"`, `"en-US"`.
- **Notas**: el framework está calibrado en español por defecto (constitución § IV). Otros idiomas son posibles pero la voz (`references/voz`) está afinada para español.

### `skills`

- **Tipo**: array de objetos con campos `name`, `version`, `source` (obligatorios) y `path` (opcional).
- **Default**: el array que `bootstrap.py` puebla con las referencias bundled del preset (la voz y la didáctica).
- **Ejemplo**:

  ```json
  "skills": [
    {"name": "marcela-prose", "version": "2.0.0", "source": "bundled"},
    {"name": "technical-guide-design", "version": "1.0.0", "source": "bundled"}
  ]
  ```

- **Valores de `source`**:
  - `bundled`: viaja en el preset como referencia (`references/voz`, `references/didactica`). La lógica del método vive en comandos + referencias, no en skills de un proveedor.
  - `external`: declarada por el operador desde otra fuente. El framework la respeta pero no la versiona.

### `research_mode`

- **Tipo**: enum `byom` | `bundled`.
- **Default**: `byom` en v1.
- **Ejemplo**: `"byom"`.
- **Notas**:
  - `byom` (Bring Your Own MCPs): el proyecto usa MCPs externos compatibles con el contrato de citación. Es el modo por defecto.
  - `bundled`: activa el módulo opcional `mcp/writeonmars-research/` como MCP canónico de investigación y contraste. Requiere también declarar `writeonmars_research_module.enabled: true`.

### `signing_matrix`

- **Tipo**: objeto con cinco claves obligatorias, una por pasada. Cada valor es un enum `autonomous` | `human`.
- **Default del bootstrap del preset**: **todas las pasadas `autonomous`** (el
  control humano es el PDF anotado al final, no pasada por pasada). El esquema
  admite `human` en cualquier pasada para guías que quieran firma humana explícita.
- **Ejemplo**:

  ```json
  "signing_matrix": {
    "pasada_1_estructura": "autonomous",
    "pasada_2_utilidad": "autonomous",
    "pasada_3_naturalidad": "human",
    "pasada_4_precision": "human",
    "pasada_5_formato": "autonomous"
  }
  ```

- **Notas**: `autonomous` permite que la pasada cierre cuando el checklist queda en verde. `human` exige firma de un operador listado en `human_operators`. El cierre (`close.py` / `speckit.close`) usa esta matriz para decidir si el proyecto puede cerrarse.

### `human_operators`

- **Tipo**: array no vacío de objetos con `id` y `role` obligatorios; `email` opcional.
- **Roles válidos**: `editor` | `author` | `reviewer` | `maintainer`.
- **Ejemplo**:

  ```json
  "human_operators": [
    {"id": "marcela", "email": "marcela@example.com", "role": "author"},
    {"id": "rev-jose", "role": "reviewer"}
  ]
  ```

- **Notas**: los `id` se usan como `actor` en las firmas de pasada (`pass-output-schema.md`). Deben ser estables a lo largo del proyecto; renombrar un operador exige reescribir las firmas históricas.

### `citation_contract_version`

- **Tipo**: string en formato `X.Y` (sin patch, alineado con el contrato).
- **Default**: `"1.0"`.
- **Ejemplo**: `"1.0"`.
- **Notas**: declara qué versión del contrato de citación soporta el proyecto. Records emitidos por MCPs con `contract_version` MAJOR distinto se rechazan. Ver `docs/citation-contract.md` § "Cuándo bumpear `contract_version`".

## Campos opcionales

### `project_type`

- **Tipo**: string del enum `editorial` | `software` | `mixed`.
- **Default**: `editorial` (lo escribe `bootstrap.py`).
- **Notas**: las plantillas en modo dual (spec/plan/tasks/checklist) se comportan
  según este campo. En `editorial` el brief del Principio III es obligatorio.

### `sector`

- **Tipo**: string (slug del sector) o `null`.
- **Default**: `null` tras el bootstrap; lo fija `speckit.constitution` al elegir
  sector (p. ej. `"tecnologia"`).
- **Notas**: apunta a la base de defaults `references/sectores/<sector>.md` desde la
  que se derivaron las adendas del proyecto (tono, anglicismos, estructura de
  capítulo, relajaciones). Ampliable creando un archivo de sector nuevo.

### `memory_external`

- **Tipo**: objeto con `enabled`, `provider`, `uri`, `rebuildable_from_repo`.
- **Default**: ausente (memoria externa desactivada).
- **Ejemplo**:

  ```json
  "memory_external": {
    "enabled": true,
    "provider": "engram",
    "uri": "engram://writeonmars/<project-id>",
    "rebuildable_from_repo": true
  }
  ```

- **Notas**: la memoria externa es caché, nunca fuente de verdad (constitución § "Arquitectura del framework"). El campo `rebuildable_from_repo` está fijado a `true` por el schema: el proyecto debe poder reconstruir la memoria desde sus artefactos sin información adicional. Para más detalle, ver `docs/memory-external.md`.

### `writeonmars_research_module`

- **Tipo**: objeto con `enabled` y `version`.
- **Default**: ausente (módulo desactivado).
- **Ejemplo**:

  ```json
  "writeonmars_research_module": {
    "enabled": true,
    "version": "0.1.0"
  }
  ```

- **Notas**: activa el MCP de investigación bundled. Requiere coherencia con `research_mode: bundled`. Ver `mcp/writeonmars-research/README.md`.

## Notas de migración

El manifiesto sigue semver. Las reglas para bumpear el schema:

- **MAJOR (`v2.0`)**: cualquier cambio que rompa manifiestos existentes. Por ejemplo: renombrar `signing_matrix.pasada_1_estructura`, cambiar el tipo de `language_primary`, hacer obligatorio un campo que antes era opcional. Un bump MAJOR exige que cada proyecto instalado migre su manifiesto; `bootstrap.py --force` re-sella lo que puede y el resto se documenta en `docs/maintenance/`.
- **MINOR (`v1.y`)**: añadir campos opcionales (como `memory_external` en su día), ampliar enums (añadir un nuevo `agent_target` cuando se porte). Los manifiestos existentes siguen siendo válidos sin tocar nada.
- **PATCH (`v1.0.z`)**: aclaraciones en `description`, ejemplos nuevos, correcciones de patrones regex que no cambian el universo aceptado.

### Procedimiento de bump

1. Editar `specs/001-framework-architecture/contracts/manifest-schema.json` (fuente de verdad).
2. Refrescar el espejo en `contracts/manifest-schema.json` (manual o vía script de mirror).
3. Actualizar este documento (`docs/manifest-schema.md`) con el campo nuevo o el cambio.
4. Actualizar `install/lib/render-manifest.sh` para que rellene el campo nuevo en proyectos nuevos.
5. Para MAJOR: documentar la migración del manifiesto en `docs/maintenance/`.
6. Bumpear `framework_version` en consecuencia (un cambio MAJOR del manifiesto suele implicar MAJOR del framework).
7. Documentar en `CHANGELOG.md` y, si aplica, en `releases/<version>/`.

### Compatibilidad hacia atrás

Dentro de la misma MAJOR, un manifiesto generado por una versión MINOR anterior debe seguir siendo válido. Esto implica:

- No eliminar campos opcionales en un MINOR.
- No restringir un patrón regex existente en un MINOR (solo ampliarlo).
- No reducir un enum en un MINOR (solo añadir valores).

## Para profundizar

- Schema autoritativo: `contracts/manifest-schema.json`.
- Contrato de citación referenciado: `docs/citation-contract.md`.
- Enmienda de la constitución (núcleo + propagación): `docs/maintenance/constitution-update-procedure.md`.
- Memoria externa opcional: `docs/memory-external.md`.
