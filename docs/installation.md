# Guía de instalación de Write.OnMars

Audiencia: mantenedores del framework y operadores que instalan el harness
sobre un repositorio editorial nuevo. El recorrido extremo a extremo del
flujo editorial vive en `specs/001-framework-architecture/quickstart.md`;
este documento se concentra en la instalación.

---

## 1. Prerrequisitos

| Componente | Versión mínima | Cómo verificar |
|------------|----------------|----------------|
| Bash | 5.0 | `bash --version` |
| Git | 2.30 | `git --version` |
| jq | 1.6 (recomendado) | `jq --version` |
| ajv-cli (opcional) | 5.x | `npx ajv-cli --version` |
| python3 + jsonschema (fallback opcional) | Python 3.11 | `python3 -c "import jsonschema"` |

`jq` no es estrictamente obligatorio: la instalación funciona sin él, pero la
detección de conflictos y la lectura del manifiesto se vuelven menos robustas.

`ajv-cli` o `python3 + jsonschema` son requisitos suaves: si ninguno de los dos
está disponible, el instalador genera el manifiesto y emite un warning sin
bloquear el flujo. La validación contra el JSON Schema es ideal pero no es
crítica para el MVP.

---

## 2. Instalación rápida (un comando)

Asume que el repositorio canónico de Write.OnMars vive en
`~/Projects/writing-framework` y que el repo destino ya está inicializado con
`git init`.

```bash
bash ~/Projects/writing-framework/install/install.sh \
  --target-dir "$(pwd)" \
  --agent claude-code \
  --language es
```

El script lanza un cuestionario de cinco preguntas (más identificador y email
del operador humano) y deja el repositorio listo en bajo cinco minutos.

---

## 3. Instalación manual (paso a paso)

Si quieres ejecutar cada fase por separado, los scripts del directorio
`install/lib/` se pueden invocar de forma independiente:

```bash
# 1. Detectar artefactos preexistentes.
bash install/lib/detect-existing.sh /ruta/al/destino

# 2. Copiar las skills bundled.
bash install/lib/copy-skills.sh \
    /ruta/al/canonical/.claude/skills /ruta/al/destino

# 3. Copiar la constitución y plantillas (manualmente, sin sobreescribir).
cp /ruta/al/canonical/.specify/memory/constitution.md \
   /ruta/al/destino/.specify/memory/constitution.md

# 4. Copiar extensions.yml + extensions/git/.
cp /ruta/al/canonical/.specify/extensions.yml \
   /ruta/al/destino/.specify/extensions.yml
cp -R /ruta/al/canonical/.specify/extensions/git \
      /ruta/al/destino/.specify/extensions/

# 5. Generar el bloque de contexto y recolectar datos del operador.
bash install/lib/render-context.sh /ruta/al/destino claude-code es

# 6. Generar y validar el manifiesto.
bash install/lib/render-manifest.sh /ruta/al/destino claude-code es \
    nombre.apellido nombre@example.com
```

El modo manual existe para depuración. En operación normal usa `install.sh`,
que orquesta los pasos en el orden correcto y reporta exit codes consistentes.

---

## 4. Flags y variables de entorno

### Flags de `install.sh`

| Flag | Descripción | Default |
|------|-------------|---------|
| `--target-dir <path>` | Repo Git destino. Obligatorio. | — |
| `--agent <name>` | `claude-code` (v1), `codex`, `cursor`, `other`. | `claude-code` |
| `--language <iso>` | Idioma primario (ISO-639). | `es` |
| `--symlink` | Enlaza skills bundled en lugar de copiarlas. | desactivado |
| `--non-interactive` | Salta el cuestionario; usa env vars `WOM_*`. | desactivado |
| `--force` | Sobreescribe skills aunque la versión destino difiera. | desactivado |
| `-h`, `--help` | Imprime la ayuda y sale 0. | — |

### Variables de entorno relevantes en modo `--non-interactive`

| Variable | Descripción | Validación |
|----------|-------------|------------|
| `WOM_PROJECT_TYPE` | `guia`, `manual`, `libro`, `articulo`, `tutorial`. | Enum cerrado. |
| `WOM_AUDIENCE` | Audiencia general en texto libre. | Mínimo 20 caracteres. |
| `WOM_DOMAIN` | Dominio técnico. | No vacío. |
| `WOM_OPERATOR_ID` | Identificador estable del operador (ej. `marcela.gotta`). | No vacío. |
| `WOM_OPERATOR_EMAIL` | Email del operador para la matriz de firmas. | Formato `local@host.dom`. |

---

## 5. Validación post-instalación

Tras una instalación exitosa, comprueba en el destino:

```bash
ls .claude/skills/marcela-prose/ \
   .claude/skills/technical-guide-design/ \
   .claude/skills/writeonmars-install/

ls .specify/memory/constitution.md \
   .specify/templates/spec-template.md \
   .specify/extensions.yml

cat .writeonmars-manifest.json | jq '.framework_version, .skills'
```

Validación opcional contra el JSON Schema (si tienes `npx` y `ajv-cli`
instalados):

```bash
npx ajv-cli validate \
  -s ~/Projects/writing-framework/contracts/manifest-schema.json \
  -d .writeonmars-manifest.json
```

Alternativa con Python:

```bash
python3 - <<'PY'
import json, jsonschema
with open(".writeonmars-manifest.json") as f: instance = json.load(f)
with open("/ruta/al/canonical/contracts/manifest-schema.json") as f: schema = json.load(f)
jsonschema.validate(instance=instance, schema=schema)
print("OK")
PY
```

Para correr el smoke suite completo del repo canónico:

```bash
bash tests/smoke/run-all.sh
```

---

## 6. Troubleshooting

### Spec Kit ya estaba instalado en el destino

`detect-existing.sh` reporta `spec_kit_present: true`. El instalador respeta
los archivos existentes y solo copia los que falten. Si quieres reemplazarlos,
hazlo manualmente fuera del flujo del instalador o ejecuta con `--force` (que
afecta sobre todo a las skills bundled, no al `.specify/`).

### CLAUDE.md previo con configuración propia

El instalador busca los marcadores `<!-- WRITEONMARS START -->` y
`<!-- WRITEONMARS END -->`. Si no existen, anexa el bloque al final del
archivo conservando el resto. Si ya existían, reemplaza solo el contenido
entre marcadores. El smoke test `install-preserves-claudemd.sh` cubre este
caso.

### Agente distinto a Claude Code

`--agent codex|cursor|other` genera `AGENTS.md` en lugar de `CLAUDE.md`. El
formato del bloque interno es idéntico. Las skills bundled siguen viviendo en
`.claude/skills/` por convención v1, hasta que la portabilidad cross-agent se
cierre formalmente (ver `docs/compatibility-matrix.md`).

### El manifiesto no valida contra el schema

Revisa que `framework_version` y `constitution_version` cumplan el patrón
semver `X.Y.Z`. El default del framework es `0.1.0` cuando el repo canónico no
tiene archivo `VERSION`. Si tu fork mantiene su propia VERSION con sufijos
tipo `0.1.0-mvp`, el script extrae el componente semver sin sufijo para no
romper la validación.

### `npx ajv-cli` no está disponible

El instalador detecta el caso "missing packages" y cae al fallback
`python3 + jsonschema`. Si ninguno está disponible, emite un warning y deja
pasar la instalación. Para un entorno auditable instala `ajv-cli` global o
`pip install jsonschema`.

### Exit code 60 (hook registration)

Suele indicar que `.specify/extensions/git/` del destino no tiene permisos de
escritura. Revisa permisos y reintenta.

---

## 7. Performance (SC-001)

Objetivo: instalación inicial en menos de cinco minutos (300 segundos) en
hardware razonable.

| Plataforma | Tiempo medio (3 corridas) | Notas |
|------------|---------------------------|-------|
| macOS 25 (Apple Silicon, M-series) | 1 s | Bash 5.3, Git 2.x, jq 1.7. Validación con `python3 + jsonschema`; `ajv-cli` no instalado globalmente. |
| Linux container | <pendiente: validar en container> | A medir en CI cuando exista. |

La instalación opera muy por debajo del techo SC-001. La medición se realizó
ejecutando `tests/smoke/install-on-empty-repo.sh` tres veces sobre directorios
temporales recién creados; ver `tests/smoke/run-all.sh` para el conjunto
completo de smoke tests.

---

## Referencias

- `install/install.sh` — entry point.
- `install/lib/common.sh` — utilidades compartidas.
- `install/lib/detect-existing.sh` — detección y reporte JSON.
- `install/lib/copy-skills.sh` — copia o enlace de skills bundled.
- `install/lib/render-context.sh` — cuestionario y `CLAUDE.md`/`AGENTS.md`.
- `install/lib/render-manifest.sh` — manifiesto JSON validado.
- `contracts/manifest-schema.json` — schema canónico del manifiesto.
- `specs/001-framework-architecture/quickstart.md` — flujo editorial completo.
- `tests/smoke/` — suite de smoke tests para validar la instalación.
