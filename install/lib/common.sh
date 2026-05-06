#!/usr/bin/env bash
# common.sh — utilidades compartidas para los scripts del instalador Write.OnMars.
#
# Provee:
#   - logging consistente (info / warn / err) en español, sin emojis
#   - resolución de WRITING_FRAMEWORK_HOME desde la ruta del script invocador
#   - helpers de detección (es repo Git, archivo existe, etc.)
#   - chequeo de prerequisites (Bash 5+, Git 2.30+)
#
# Uso:
#   source "$(dirname "$0")/lib/common.sh"
#   common::resolve_framework_home "$0"
#
# Cubre: FR-001..FR-004 (instalación reproducible).

set -euo pipefail

# ---------------------------------------------------------------------------
# Variables globales (exportadas para los scripts hijos del instalador)
# ---------------------------------------------------------------------------

# WRITING_FRAMEWORK_HOME: raíz del repo canónico de Write.OnMars.
# Se calcula con `common::resolve_framework_home` a partir del path del script.
: "${WRITING_FRAMEWORK_HOME:=}"

# WOM_LOG_PREFIX: prefijo legible para los mensajes de log.
: "${WOM_LOG_PREFIX:=writeonmars}"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

common::info() {
    printf '[%s][info] %s\n' "$WOM_LOG_PREFIX" "$*" >&2
}

common::warn() {
    printf '[%s][warn] %s\n' "$WOM_LOG_PREFIX" "$*" >&2
}

common::err() {
    printf '[%s][err] %s\n' "$WOM_LOG_PREFIX" "$*" >&2
}

common::die() {
    local exit_code="$1"
    shift
    common::err "$*"
    exit "$exit_code"
}

# ---------------------------------------------------------------------------
# Resolución de paths
# ---------------------------------------------------------------------------

# common::resolve_framework_home <path-al-script-de-entrada>
# Establece WRITING_FRAMEWORK_HOME asumiendo que el script vive en
# `<framework_home>/install/install.sh`.
common::resolve_framework_home() {
    local script_path="$1"
    local script_dir
    # Resolver enlaces simbólicos; sin readlink -f en macOS por defecto, así que
    # iteramos manualmente hasta agotar enlaces.
    while [[ -L "$script_path" ]]; do
        local link_target
        link_target="$(readlink "$script_path")"
        if [[ "$link_target" == /* ]]; then
            script_path="$link_target"
        else
            script_path="$(cd "$(dirname "$script_path")" && pwd)/$link_target"
        fi
    done
    script_dir="$(cd "$(dirname "$script_path")" && pwd)"
    # script vive en install/, parent es el framework home.
    WRITING_FRAMEWORK_HOME="$(cd "$script_dir/.." && pwd)"
    export WRITING_FRAMEWORK_HOME
}

# ---------------------------------------------------------------------------
# Detección
# ---------------------------------------------------------------------------

common::is_git_repo() {
    local target="$1"
    [[ -d "$target/.git" ]] || (cd "$target" && git rev-parse --is-inside-work-tree >/dev/null 2>&1)
}

common::file_exists() {
    [[ -f "$1" ]]
}

common::dir_exists() {
    [[ -d "$1" ]]
}

# ---------------------------------------------------------------------------
# Versionado
# ---------------------------------------------------------------------------

# common::semver_compare <a> <b>
# Imprime  0 si a == b, 1 si a > b, -1 si a < b.
common::semver_compare() {
    local a="$1" b="$2"
    if [[ "$a" == "$b" ]]; then
        echo 0
        return
    fi
    local a_major a_minor a_patch b_major b_minor b_patch
    IFS='.' read -r a_major a_minor a_patch <<<"$a"
    IFS='.' read -r b_major b_minor b_patch <<<"$b"
    a_major="${a_major:-0}"; a_minor="${a_minor:-0}"; a_patch="${a_patch:-0}"
    b_major="${b_major:-0}"; b_minor="${b_minor:-0}"; b_patch="${b_patch:-0}"
    if (( a_major > b_major )); then echo 1; return; fi
    if (( a_major < b_major )); then echo -1; return; fi
    if (( a_minor > b_minor )); then echo 1; return; fi
    if (( a_minor < b_minor )); then echo -1; return; fi
    if (( a_patch > b_patch )); then echo 1; return; fi
    if (( a_patch < b_patch )); then echo -1; return; fi
    echo 0
}

# common::git_min_version <required>  ej. "2.30"
common::git_min_version() {
    local required="$1"
    if ! command -v git >/dev/null 2>&1; then
        return 1
    fi
    local current
    current="$(git --version | awk '{print $3}')"
    # comparar como semver con patch=0 si falta.
    local current_major current_minor
    IFS='.' read -r current_major current_minor _ <<<"$current"
    local req_major req_minor
    IFS='.' read -r req_major req_minor <<<"$required"
    if (( current_major > req_major )); then return 0; fi
    if (( current_major < req_major )); then return 1; fi
    if (( current_minor >= req_minor )); then return 0; fi
    return 1
}

# common::bash_min_version <major>
common::bash_min_version() {
    local required="$1"
    if [[ "${BASH_VERSINFO[0]}" -ge "$required" ]]; then
        return 0
    fi
    return 1
}

# ---------------------------------------------------------------------------
# Manifest VERSION lookup
# ---------------------------------------------------------------------------

# common::framework_version  -> imprime versión leída de <home>/VERSION o un default.
common::framework_version() {
    if [[ -f "$WRITING_FRAMEWORK_HOME/VERSION" ]]; then
        # Aceptar líneas tipo "0.1.0", "v0.1.0" o "v0.1.0-mvp" y devolver
        # solo el semver puro X.Y.Z para satisfacer el schema del manifiesto.
        local raw
        raw="$(head -n 1 "$WRITING_FRAMEWORK_HOME/VERSION" | tr -d '[:space:]')"
        raw="${raw#v}"
        local semver
        semver="$(echo "$raw" | grep -Eo '^[0-9]+\.[0-9]+\.[0-9]+' || true)"
        if [[ -n "$semver" ]]; then
            echo "$semver"
        else
            echo "0.1.0"
        fi
    else
        echo "0.1.0"
    fi
}

# common::constitution_version  -> parsea **Version**: X.Y.Z del archivo de constitución
# en el destino o, si no existe, en el repo canónico.
common::constitution_version() {
    local target_dir="$1"
    local constitution=""
    if [[ -f "$target_dir/.specify/memory/constitution.md" ]]; then
        constitution="$target_dir/.specify/memory/constitution.md"
    elif [[ -f "$WRITING_FRAMEWORK_HOME/.specify/memory/constitution.md" ]]; then
        constitution="$WRITING_FRAMEWORK_HOME/.specify/memory/constitution.md"
    else
        echo "0.0.0"
        return
    fi
    # Buscar la primera ocurrencia de **Version**: X.Y.Z (al final del archivo).
    local version
    version="$(grep -Eo '\*\*Version\*\*:[[:space:]]*[0-9]+\.[0-9]+\.[0-9]+' "$constitution" \
        | head -n 1 \
        | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' || true)"
    if [[ -z "$version" ]]; then
        echo "0.0.0"
    else
        echo "$version"
    fi
}

# ---------------------------------------------------------------------------
# Skill VERSION parsing
# ---------------------------------------------------------------------------

# common::skill_semver <ruta-VERSION>
# Devuelve la versión semver pura (ej "0.1.0") parseada de la primera línea
# de un archivo VERSION con el formato "vX.Y.Z-import-..." o "X.Y.Z".
common::skill_semver() {
    local version_file="$1"
    if [[ ! -f "$version_file" ]]; then
        echo ""
        return
    fi
    local first_line
    first_line="$(head -n 1 "$version_file" | tr -d '[:space:]')"
    # quitar prefijo v si existe.
    first_line="${first_line#v}"
    # extraer X.Y.Z al inicio.
    local semver
    semver="$(echo "$first_line" | grep -Eo '^[0-9]+\.[0-9]+\.[0-9]+' || true)"
    if [[ -z "$semver" ]]; then
        echo ""
    else
        echo "$semver"
    fi
}
