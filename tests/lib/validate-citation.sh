#!/usr/bin/env bash
# validate-citation.sh — valida un CitationRecord contra el schema canónico.
#
# Uso:
#   validate-citation.sh <path-a-archivo.json>
#   cat record.json | validate-citation.sh -
#
# Estrategia:
#   1. Localiza WRITING_FRAMEWORK_HOME relativo al script (tres niveles arriba).
#   2. Resuelve SCHEMA_PATH = $WRITING_FRAMEWORK_HOME/contracts/citation-record.schema.json.
#   3. Intenta validar con python3 + jsonschema (soporta draft 2020-12 sin
#      configuración adicional).
#   4. Si python3 no tiene jsonschema, fallback a `npx ajv-cli` con
#      `--spec=draft2020`.
#   5. Si ninguno está disponible, sale con error claro.
#
# Exit codes:
#   0  — record válido
#   1  — record inválido o input ilegible
#   2  — sin validador disponible (ni ajv, ni python+jsonschema)
#   3  — uso incorrecto / argumentos faltantes
#
# Cubre: T049 (helper), FR-009 (validación), FR-016 (uso desde pasada 4).

set -euo pipefail

# ---------------------------------------------------------------------------
# Logging mínimo (mantiene salida útil hacia stderr; stdout queda para el
# resultado de validación cuando aplica).
# ---------------------------------------------------------------------------

log_err() {
    printf '[validate-citation][err] %s\n' "$*" >&2
}

log_warn() {
    printf '[validate-citation][warn] %s\n' "$*" >&2
}

log_info() {
    printf '[validate-citation][info] %s\n' "$*" >&2
}

# ---------------------------------------------------------------------------
# Resolución de paths
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Validadores
# ---------------------------------------------------------------------------

# validate_with_ajv <schema_path> <data_path>
validate_with_ajv() {
    local schema_path="$1"
    local data_path="$2"
    if ! command -v npx >/dev/null 2>&1; then
        return 127
    fi
    # Probar invocación silenciosa; ajv-cli devuelve 0 cuando es válido.
    if npx --yes ajv-cli validate \
        --spec=draft2020 \
        -s "$schema_path" \
        -d "$data_path" >/dev/null 2>&1; then
        return 0
    fi
    # Si falla la invocación, reintentar mostrando errores para que el
    # operador vea el motivo.
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
    print("[validate-citation][err] python3 jsonschema no instalado", file=sys.stderr)
    sys.exit(127)

schema_path = sys.argv[1]
data_path = sys.argv[2]

try:
    with open(schema_path, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
except (OSError, json.JSONDecodeError) as exc:
    print(f"[validate-citation][err] schema ilegible: {exc}", file=sys.stderr)
    sys.exit(1)

try:
    with open(data_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
except (OSError, json.JSONDecodeError) as exc:
    print(f"[validate-citation][err] data ilegible: {exc}", file=sys.stderr)
    sys.exit(1)

validator_cls = jsonschema.validators.validator_for(schema)
validator = validator_cls(schema)
errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
if not errors:
    print("valid")
    sys.exit(0)

for err in errors:
    path = "/".join(str(p) for p in err.absolute_path) or "<root>"
    print(f"[validate-citation][err] {path}: {err.message}", file=sys.stderr)
sys.exit(1)
PY
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

usage() {
    cat <<'USAGE' >&2
Uso:
  validate-citation.sh <path-a-archivo.json>
  cat record.json | validate-citation.sh -

Valida un CitationRecord (citation-contract v1.0) contra
contracts/citation-record.schema.json.
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
        data_path="$(mktemp -t citation-record.XXXXXX.json)"
        cleanup_tmp="$data_path"
        # Leer todo stdin al archivo temporal.
        cat - >"$data_path"
    else
        if [[ ! -f "$input" ]]; then
            log_err "archivo no encontrado: $input"
            exit 1
        fi
        data_path="$input"
    fi

    # cleanup hook
    if [[ -n "$cleanup_tmp" ]]; then
        # shellcheck disable=SC2064
        trap "rm -f '$cleanup_tmp'" EXIT
    fi

    local framework_home
    framework_home="$(resolve_framework_home "${BASH_SOURCE[0]}")"
    local schema_path="$framework_home/contracts/citation-record.schema.json"
    if [[ ! -f "$schema_path" ]]; then
        log_err "schema ausente: $schema_path"
        exit 1
    fi

    # 1) Preferir python3 + jsonschema: soporta draft 2020-12 sin flags
    #    extra y suele estar disponible en macOS y Linux.
    if command -v python3 >/dev/null 2>&1; then
        if validate_with_python "$schema_path" "$data_path"; then
            exit 0
        else
            local rc=$?
            if [[ $rc -ne 127 ]]; then
                # python3 corrió y el record es inválido.
                exit 1
            fi
            log_warn "python3 no tiene jsonschema; intentando con ajv-cli"
        fi
    fi

    # 2) Fallback a ajv-cli si npx está disponible.
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
