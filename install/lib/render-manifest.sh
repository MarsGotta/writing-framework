#!/usr/bin/env bash
# render-manifest.sh — genera y valida .writeonmars-manifest.json en el destino.
#
# Cubre FR-004 (manifiesto del proyecto editorial) + FR-027 (matriz de firmas
# por defecto: pasadas 1, 2, 5 = autonomous; pasadas 3, 4 = human).
#
# Uso:
#   render-manifest.sh <target_dir> <agent_target> <language_primary> <operator_id> <operator_email> [project_type]
#
# `project_type` es opcional. Cuando se pasa, se registra en el manifiesto como
# campo opcional (enum: editorial|software|mixed) que selecciona el modo de las
# plantillas Spec Kit consumidas. Si se omite, el manifiesto no incluye el
# campo (comportamiento por defecto = software para Spec Kit).
#
# Salida: <target_dir>/.writeonmars-manifest.json validado contra
# contracts/manifest-schema.json del repo canónico.
#
# Validación:
#   1. npx ajv (vía ajv-cli) si está disponible.
#   2. python3 -c "import jsonschema" como fallback.
#   3. Si ninguno funciona, se emite warning y se continúa: la validación es
#      ideal pero no debe bloquear el MVP en entornos mínimos.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
WOM_LOG_PREFIX="render-manifest"

usage() {
    cat <<EOF
Uso: render-manifest.sh <target_dir> <agent_target> <language_primary> <operator_id> <operator_email> [project_type]
EOF
}

if [[ $# -lt 5 ]]; then
    usage
    exit 2
fi

TARGET_DIR="$1"
AGENT_TARGET="$2"
LANGUAGE_PRIMARY="$3"
OPERATOR_ID="$4"
OPERATOR_EMAIL="$5"
PROJECT_TYPE_RAW="${6:-}"

# Mapear el tipo de proyecto editorial recolectado por render-context.sh al
# enum del manifiesto. Cualquier tipo editorial canónico (guía, manual, libro,
# artículo, tutorial) se registra como `editorial`. Si llega ya un valor
# canónico (editorial|software|mixed) se respeta tal cual. Si llega vacío, el
# campo no se emite.
PROJECT_TYPE_MANIFEST=""
case "$PROJECT_TYPE_RAW" in
    "") PROJECT_TYPE_MANIFEST="" ;;
    editorial|software|mixed) PROJECT_TYPE_MANIFEST="$PROJECT_TYPE_RAW" ;;
    guia|manual|libro|articulo|tutorial) PROJECT_TYPE_MANIFEST="editorial" ;;
    *) common::warn "project_type='$PROJECT_TYPE_RAW' desconocido; se omite del manifiesto." ;;
esac

if [[ -z "${WRITING_FRAMEWORK_HOME:-}" ]]; then
    WRITING_FRAMEWORK_HOME="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

framework_version="$(common::framework_version)"
constitution_version="$(common::constitution_version "$TARGET_DIR")"

# ---------------------------------------------------------------------------
# Construir array skills[] iterando .claude/skills/ del destino.
# ---------------------------------------------------------------------------

skills_dir="$TARGET_DIR/.claude/skills"
if [[ ! -d "$skills_dir" ]]; then
    common::die 50 "No existe $skills_dir; ejecuta copy-skills.sh antes de render-manifest.sh."
fi

# Solo incluimos las skills bundled de Write.OnMars, no las de speckit-*.
declare -a skill_entries=()
shopt -s nullglob
for dir in "$skills_dir"/*; do
    [[ -d "$dir" ]] || continue
    name="$(basename "$dir")"
    case "$name" in
        speckit-*) continue ;;
        marcela-prose|technical-guide-design|writeonmars-*) ;;
        *) continue ;;
    esac
    version_file="$dir/VERSION"
    version="$(common::skill_semver "$version_file")"
    if [[ -z "$version" ]]; then
        common::warn "Skill $name sin VERSION semver; se omite del manifiesto."
        continue
    fi
    skill_entries+=("{\"name\":\"$name\",\"version\":\"$version\",\"source\":\"bundled\"}")
done
shopt -u nullglob

if [[ ${#skill_entries[@]} -eq 0 ]]; then
    common::die 50 "No se encontró ninguna skill bundled válida en $skills_dir."
fi

skills_json="["
for ((i = 0; i < ${#skill_entries[@]}; i++)); do
    if [[ $i -gt 0 ]]; then skills_json+=","; fi
    skills_json+="${skill_entries[$i]}"
done
skills_json+="]"

# ---------------------------------------------------------------------------
# Construir manifiesto completo.
# ---------------------------------------------------------------------------

manifest_path="$TARGET_DIR/.writeonmars-manifest.json"

# Construir línea opcional `"project_type": "..."` con coma final correcta.
project_type_line=""
if [[ -n "$PROJECT_TYPE_MANIFEST" ]]; then
    project_type_line=$',\n  "project_type": "'"$PROJECT_TYPE_MANIFEST"'"'
fi

cat >"$manifest_path" <<EOF
{
  "framework_version": "$framework_version",
  "constitution_version": "$constitution_version",
  "agent_target": "$AGENT_TARGET",
  "language_primary": "$LANGUAGE_PRIMARY",
  "skills": $skills_json,
  "research_mode": "byom",
  "signing_matrix": {
    "pasada_1_estructura": "autonomous",
    "pasada_2_utilidad": "autonomous",
    "pasada_3_naturalidad": "human",
    "pasada_4_precision": "human",
    "pasada_5_formato": "autonomous"
  },
  "human_operators": [
    {
      "id": "$OPERATOR_ID",
      "email": "$OPERATOR_EMAIL",
      "role": "editor"
    }
  ],
  "citation_contract_version": "1.0"${project_type_line}
}
EOF

# Re-formatear con jq si está disponible para asegurar JSON válido.
if command -v jq >/dev/null 2>&1; then
    if ! jq '.' "$manifest_path" >"$manifest_path.tmp"; then
        common::die 50 "El manifiesto generado no es JSON válido."
    fi
    mv "$manifest_path.tmp" "$manifest_path"
fi

common::info "Manifiesto escrito en $manifest_path"

# ---------------------------------------------------------------------------
# Validación contra el JSON Schema.
# ---------------------------------------------------------------------------

schema_path="$WRITING_FRAMEWORK_HOME/contracts/manifest-schema.json"
if [[ ! -f "$schema_path" ]]; then
    common::warn "No se encontró $schema_path; se omite la validación."
    exit 0
fi

validate_with_ajv() {
    if ! command -v npx >/dev/null 2>&1; then
        return 2
    fi
    # Intentar con ajv-cli ya cacheado vía --no-install. Si el paquete no
    # está disponible localmente, npx falla con un mensaje "missing
    # packages" que tratamos como "ajv no disponible" (rc=2) para que el
    # caller pueda caer al fallback de python+jsonschema.
    local out rc
    set +e
    out="$(npx --no-install ajv-cli validate --spec=draft2020 -s "$schema_path" -d "$manifest_path" 2>&1)"
    rc=$?
    set -e
    if [[ $rc -ne 0 ]]; then
        # ajv ausente, schema no soportado o ref interna no resoluble: tratar como
        # "ajv no disponible" (rc=2) para que el caller caiga al fallback python.
        if echo "$out" | grep -q -E "missing packages|could not determine executable to run|command not found|no schema with key or ref|schema .* is invalid|unknown keyword"; then
            return 2
        fi
        echo "$out" >&2
        return 1
    fi
    echo "$out"
    return 0
}

validate_with_python() {
    if ! command -v python3 >/dev/null 2>&1; then
        return 2
    fi
    python3 - "$schema_path" "$manifest_path" <<'PYEOF' 2>&1
import json, sys
try:
    import jsonschema
except ImportError:
    sys.exit(2)

schema_path, instance_path = sys.argv[1], sys.argv[2]
with open(schema_path, encoding="utf-8") as f:
    schema = json.load(f)
with open(instance_path, encoding="utf-8") as f:
    instance = json.load(f)

try:
    jsonschema.validate(instance=instance, schema=schema)
except jsonschema.exceptions.ValidationError as e:
    print(f"validation error: {e.message} at {list(e.absolute_path)}", file=sys.stderr)
    sys.exit(1)
print("manifest valid")
PYEOF
}

validation_status="unknown"
if out="$(validate_with_ajv 2>&1)"; then
    common::info "Validación ajv: $out"
    validation_status="ok"
else
    rc=$?
    if [[ $rc -eq 1 ]]; then
        common::err "ajv reportó errores de validación."
        common::err "$out"
        exit 50
    fi
    # rc == 2 → ajv no disponible; probar python3+jsonschema.
    if py_out="$(validate_with_python 2>&1)"; then
        common::info "Validación python+jsonschema: $py_out"
        validation_status="ok"
    else
        py_rc=$?
        if [[ $py_rc -eq 1 ]]; then
            common::err "python+jsonschema reportó errores de validación."
            common::err "$py_out"
            exit 50
        fi
        common::warn "Ni ajv ni python jsonschema disponibles. La validación del manifiesto se omitió."
        validation_status="skipped"
    fi
fi

common::info "Estado de validación: $validation_status"
