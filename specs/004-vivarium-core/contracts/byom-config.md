# Contrato de configuración BYOM — `.vivarium/config.toml` (v1)

Vive en la raíz del proyecto editorial, **no versionado** (el bootstrap añade
`.vivarium/` al `.gitignore`: contiene rutas locales de la operadora).
`vivarium new` deja `.vivarium/config.toml.example` con esta plantilla
comentada; la operadora la copia a `config.toml` y ajusta sus órdenes
(`vivarium check` valida el resultado).

## Formato

```toml
# .vivarium/config.toml
version = 1

[python]
# Opcional. Precedencia: $VIVARIUM_PYTHON (env) > este campo > `python3` del PATH.
interpreter = "/usr/local/bin/python3"

# Tres roles OBLIGATORIOS. `command` es una plantilla: lista de argv donde los
# placeholders se sustituyen literalmente (sin shell, sin quoting frágil).
# Placeholders soportados: {prompt_file} {project_dir} {chapter}

[roles.redactora]
command = ["claude", "-p", "@{prompt_file}", "--permission-mode", "acceptEdits"]

[roles.editora_mesa]
command = ["codex", "exec", "--cd", "{project_dir}", "-", "<", "{prompt_file}"]  # ejemplo; ver nota de stdin

[roles.documentalista]
command = ["codex", "exec", "--cd", "{project_dir}", "{prompt_file}"]
```

Nota de stdin: la plantilla es argv puro; si un agente exige el prompt por
stdin, se usa la forma `stdin = "prompt_file"` en la tabla del rol y el runner
conecta el archivo a stdin (no se interpreta shell):

```toml
[roles.editora_mesa]
command = ["codex", "exec", "--cd", "{project_dir}", "-"]
stdin = "prompt_file"
```

## Semántica

- **Roles**: `redactora` (implement/revise), `editora_mesa` (pasadas 1·2·3 y
  5), `documentalista` (research y pasada 4). El orquestador no es un rol: es
  el propio runner (research.md R5).
- **Sustitución**: `{prompt_file}` = ruta absoluta del archivo de tarea que el
  runner escribe en `.vivarium/tasks/` (contenido: encargo del paso, capítulo,
  rutas relevantes, contrato de salida); `{project_dir}` = raíz absoluta del
  proyecto; `{chapter}` = ordinal (vacío en pasos globales).
- **Preset**: la ruta del preset para `vivarium new` NO va en este archivo (el
  config vive dentro del proyecto, que aún no existe al crear): se pasa con el
  flag `--preset` (default: la copia local del framework).
- **Validación (`vivarium check` y arranque de `step|run`)**: los tres roles
  presentes; el binario (primer elemento de `command`) resoluble en PATH o
  ruta absoluta existente; la plantilla contiene `{prompt_file}` o declara
  `stdin = "prompt_file"`. Fallo ⇒ exit 3/5 antes de despachar nada.
- **Éxito de un despacho**: exit code 0 del agente **y** efecto esperado en
  disco (research.md R6). La salida de texto del agente no se parsea.
- **Neutralidad (Principio VI)**: los ejemplos usan `claude` y `codex` porque
  son los adaptadores de referencia del repo (`agents/claude/`,
  `agents/codex/`), pero cualquier CLI que acepte un prompt y trabaje sobre el
  repo sirve. Los tests usan stubs de shell, no proveedores reales.
- **Recomendación cruzada** (no gate): `redactora` y `editora_mesa` con agente
  o modelo distinto (voz ≠ precisión, roster de Paperclip como precedente).
