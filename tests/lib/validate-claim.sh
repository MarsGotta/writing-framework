#!/usr/bin/env bash
# validate-claim.sh — valida un ClaimRecord contra el schema canónico.
#
# Uso:
#   validate-claim.sh <path-a-archivo.json>
#   cat record.json | validate-claim.sh -
#
# Estrategia (gemelo de validate-citation.sh):
#   1. Localiza WRITING_FRAMEWORK_HOME relativo al script (dos niveles arriba).
#   2. Resuelve SCHEMA_PATH = $WRITING_FRAMEWORK_HOME/writeonmars/contracts/claim-record.schema.json.
#   3. Valida con python3 + jsonschema (draft 2020-12 sin configuración extra).
#   4. Fallback a `npx ajv-cli --spec=draft2020` si no hay jsonschema.
#   5. Si ninguno está disponible, sale con error claro.
#
# Los condicionales del schema (allOf/if-then) garantizan que se rechacen:
#   - una arista `relacion: apoya` sin `cita_fragmento_soporte`,
#   - `verificado_en_vivo: true` sin `url_verificada` ni `fecha_verificacion`.
#
# Exit codes:
#   0  — record válido
#   1  — record inválido o input ilegible
#   2  — sin validador disponible (ni ajv, ni python+jsonschema)
#   3  — uso incorrecto / argumentos faltantes
#
# Cubre: FR-020 (feature 003-atribucion-factualidad).

set -euo pipefail

log_err()  { printf '[validate-claim][err] %s\n'  "$*" >&2; }
log_warn() { printf '[validate-claim][warn] %s\n' "$*" >&2; }
log_info() { printf '[validate-claim][info] %s\n' "$*" >&2; }

resolve_framework_home() {
    local script_path="$1"
    while [[ -L "$script_path" ]]; do
        local link_target
        link_target="$(readlink "$script_path")"
        if [[ "$link_target" == /* ]]; then
            script_path="$link_target"
        else
            script_path="$(cd "$(dirname "$script_path")" && pwd)/$link_target"
        fi
    done
    local script_dir
    script_dir="$(cd "$(dirname "$script_path")" && pwd)"
    # script vive en tests/lib/, raíz del framework dos niveles arriba.
    (cd "$script_dir/../.." && pwd)
}

# validate_with_ajv <schema_path> <data_path>
validate_with_ajv() {
    local schema_path="$1"
    local data_path="$2"
    if ! command -v npx >/dev/null 2>&1; then
        return 127
    fi
    if npx --yes ajv-cli validate \
        --spec=draft2020 \
        -s "$schema_path" \
        -d "$data_path" >/dev/null 2>&1; then
        return 0
    fi
    npx --yes ajv-cli validate --spec=draft2020 -s "$schema_path" -d "$data_path" >&2 || return 1
}

# validate_with_python <schema_path> <data_path>
validate_with_python() {
    local schema_path="$1"
    local data_path="$2"
    if ! command -v python3 >/dev/null 2>&1; then
        return 127
    fi
    python3 - "$schema_path" "$data_path" <<'PY' || return 1
import json
import sys

try:
    import jsonschema
except ImportError:
    print("[validate-claim][err] python3 jsonschema no instalado", file=sys.stderr)
    sys.exit(127)

schema_path = sys.argv[1]
data_path = sys.argv[2]

try:
    with open(schema_path, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
except (OSError, json.JSONDecodeError) as exc:
    print(f"[validate-claim][err] schema ilegible: {exc}", file=sys.stderr)
    sys.exit(1)

try:
    with open(data_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
except (OSError, json.JSONDecodeError) as exc:
    print(f"[validate-claim][err] data ilegible: {exc}", file=sys.stderr)
    sys.exit(1)

validator_cls = jsonschema.validators.validator_for(schema)
validator = validator_cls(schema)
errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
if not errors:
    print("valid")
    sys.exit(0)

for err in errors:
    path = "/".join(str(p) for p in err.absolute_path) or "<root>"
    print(f"[validate-claim][err] {path}: {err.message}", file=sys.stderr)
sys.exit(1)
PY
}

usage() {
    cat <<'USAGE' >&2
Uso:
  validate-claim.sh <path-a-archivo.json>
  cat record.json | validate-claim.sh -

Valida un ClaimRecord (claim-record v1.0) contra
writeonmars/contracts/claim-record.schema.json.
USAGE
}

main() {
    if [[ $# -ne 1 ]]; then
        usage
        exit 3
    fi

    local input="$1"
    local data_path
    local cleanup_tmp=""

    if [[ "$input" == "-" ]]; then
        data_path="$(mktemp -t claim-record.XXXXXX.json)"
        cleanup_tmp="$data_path"
        cat - >"$data_path"
    else
        if [[ ! -f "$input" ]]; then
            log_err "archivo no encontrado: $input"
            exit 1
        fi
        data_path="$input"
    fi

    if [[ -n "$cleanup_tmp" ]]; then
        # shellcheck disable=SC2064
        trap "rm -f '$cleanup_tmp'" EXIT
    fi

    local framework_home
    framework_home="$(resolve_framework_home "${BASH_SOURCE[0]}")"
    local schema_path="$framework_home/writeonmars/contracts/claim-record.schema.json"
    if [[ ! -f "$schema_path" ]]; then
        log_err "schema ausente: $schema_path"
        exit 1
    fi

    if command -v python3 >/dev/null 2>&1; then
        if validate_with_python "$schema_path" "$data_path"; then
            exit 0
        else
            local rc=$?
            if [[ $rc -ne 127 ]]; then
                exit 1
            fi
            log_warn "python3 no tiene jsonschema; intentando con ajv-cli"
        fi
    fi

    if command -v npx >/dev/null 2>&1; then
        if validate_with_ajv "$schema_path" "$data_path"; then
            echo "valid"
            exit 0
        else
            local rc=$?
            if [[ $rc -ne 127 ]]; then
                exit 1
            fi
        fi
    fi

    log_err "ningún validador disponible. Instala python3+jsonschema (pip install jsonschema) o ajv-cli (npm install -g ajv-cli)."
    exit 2
}

main "$@"
