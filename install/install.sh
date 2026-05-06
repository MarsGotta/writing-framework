#!/usr/bin/env bash
# install.sh — entry point del instalador Write.OnMars.
#
# Autor: Write.OnMars
# Cubre: FR-001 (instalación reproducible), FR-002 (cuestionario inicial),
#        FR-003 (detección y fusión no destructiva), FR-004 (manifiesto del
#        proyecto editorial).
#
# Exit codes:
#   0  — instalación completa.
#   10 — precondición fallida (Bash <5, Git ausente o <2.30, target no es repo Git).
#   20 — la detección reportó un conflicto irresoluble.
#   30 — falla en copy-skills.
#   40 — falla en render-context (cuestionario abortado o respuestas inválidas).
#   50 — falla en render-manifest (validación contra el JSON Schema).
#   60 — falla en hook registration.
#
# Uso:
#   install.sh --target-dir <path> [--agent <claude-code|codex|cursor|other>]
#              [--language <iso>] [--symlink] [--non-interactive] [--force]
#
# Variables de entorno (modo --non-interactive):
#   WOM_PROJECT_TYPE    guia|manual|libro|articulo|tutorial
#   WOM_AUDIENCE        texto libre, mínimo 20 caracteres
#   WOM_DOMAIN          texto libre
#   WOM_OPERATOR_ID     identificador estable (ej. nombre.apellido)
#   WOM_OPERATOR_EMAIL  email del operador

set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

WOM_LOG_PREFIX="install"
common::resolve_framework_home "$SCRIPT_PATH"

# ---------------------------------------------------------------------------
# Defaults y parseo de flags
# ---------------------------------------------------------------------------

TARGET_DIR=""
AGENT="claude-code"
LANGUAGE="es"
USE_SYMLINK=0
NON_INTERACTIVE=0
FORCE=0

usage() {
    cat <<'EOF'
Uso: install.sh --target-dir <path> [opciones]

Opciones:
  --target-dir <path>       Directorio del repo Git destino (obligatorio).
  --agent <name>            claude-code (default), codex, cursor, other.
  --language <iso>          Idioma primario (default: es).
  --symlink                 Crear enlaces simbólicos a las skills bundled
                            en lugar de copiarlas.
  --non-interactive         Saltar el cuestionario; usar variables de entorno
                            WOM_PROJECT_TYPE, WOM_AUDIENCE, WOM_DOMAIN,
                            WOM_OPERATOR_ID, WOM_OPERATOR_EMAIL.
  --force                   Sobreescribir skills aunque la versión destino
                            difiera de la canónica.
  -h, --help                Mostrar esta ayuda y salir.

Variables de entorno relevantes en modo --non-interactive:
  WOM_PROJECT_TYPE    guia|manual|libro|articulo|tutorial
  WOM_AUDIENCE        texto libre, mínimo 20 caracteres
  WOM_DOMAIN          texto libre
  WOM_OPERATOR_ID     identificador estable (ej. marcela.gotta)
  WOM_OPERATOR_EMAIL  email del operador (formato válido)

Exit codes:
  0  instalación completa
  10 precondición fallida
  20 conflicto de detección irresoluble
  30 falla en copy-skills
  40 falla en render-context
  50 falla en render-manifest
  60 falla en hook registration
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target-dir) TARGET_DIR="${2:-}"; shift 2 ;;
        --agent) AGENT="${2:-}"; shift 2 ;;
        --language) LANGUAGE="${2:-}"; shift 2 ;;
        --symlink) USE_SYMLINK=1; shift ;;
        --non-interactive) NON_INTERACTIVE=1; shift ;;
        --force) FORCE=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) common::err "Argumento desconocido: $1"; usage; exit 10 ;;
    esac
done

# ---------------------------------------------------------------------------
# Validación de precondiciones (exit 10)
# ---------------------------------------------------------------------------

if [[ -z "$TARGET_DIR" ]]; then
    common::err "--target-dir es obligatorio."
    usage
    exit 10
fi

# Convertir a path absoluto para evitar ambigüedades.
TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd || true)"
if [[ -z "$TARGET_DIR" ]]; then
    common::err "El directorio destino no existe."
    exit 10
fi

if ! common::bash_min_version 5; then
    common::err "Se requiere Bash 5+. Versión actual: ${BASH_VERSION}."
    exit 10
fi

if ! common::git_min_version "2.30"; then
    common::err "Se requiere Git ≥ 2.30."
    exit 10
fi

if ! common::is_git_repo "$TARGET_DIR"; then
    common::err "El destino no es un repositorio Git: $TARGET_DIR"
    common::err "Ejecuta 'git init' antes de invocar el instalador."
    exit 10
fi

case "$AGENT" in
    claude-code|codex|cursor|other) ;;
    *) common::err "Agente no soportado: $AGENT"; exit 10 ;;
esac

# ---------------------------------------------------------------------------
# Inicio (cronometrado para SC-001)
# ---------------------------------------------------------------------------

START_TS="$(date +%s)"
common::info "Iniciando instalación Write.OnMars en $TARGET_DIR"
common::info "Agente: $AGENT | Idioma: $LANGUAGE | Symlink: $USE_SYMLINK | Interactivo: $((1 - NON_INTERACTIVE))"

# ---------------------------------------------------------------------------
# Paso 1 — Detección
# ---------------------------------------------------------------------------

common::info "[1/6] Detectando estado del repo destino..."
detect_json="$(bash "$SCRIPT_DIR/lib/detect-existing.sh" "$TARGET_DIR")"
if command -v jq >/dev/null 2>&1; then
    n_conflicts="$(echo "$detect_json" | jq '.conflicts | length')"
else
    n_conflicts=0
fi
if [[ "$n_conflicts" -gt 0 && $FORCE -eq 0 ]]; then
    common::err "Detección reportó conflictos:"
    echo "$detect_json" | (command -v jq >/dev/null 2>&1 && jq -r '.conflicts[]' || cat) >&2
    common::err "Reintenta con --force o resuelve manualmente antes de continuar."
    exit 20
fi

# ---------------------------------------------------------------------------
# Paso 2 — Copy skills bundled
# ---------------------------------------------------------------------------

common::info "[2/6] Copiando skills bundled..."
copy_args=("$WRITING_FRAMEWORK_HOME/.claude/skills" "$TARGET_DIR")
[[ $USE_SYMLINK -eq 1 ]] && copy_args+=("--symlink")
[[ $FORCE -eq 1 ]] && copy_args+=("--force")
if ! bash "$SCRIPT_DIR/lib/copy-skills.sh" "${copy_args[@]}"; then
    common::err "copy-skills.sh falló."
    exit 30
fi

# ---------------------------------------------------------------------------
# Paso 3 — Copy .specify (constitution + templates), preservando lo que ya exista
# ---------------------------------------------------------------------------

common::info "[3/6] Copiando .specify (constitución, plantillas, extensiones)..."
mkdir -p "$TARGET_DIR/.specify/memory" "$TARGET_DIR/.specify/templates"

# Constitution: solo copia si el destino no la tiene; si la tiene, se respeta.
if [[ ! -f "$TARGET_DIR/.specify/memory/constitution.md" ]]; then
    if [[ -f "$WRITING_FRAMEWORK_HOME/.specify/memory/constitution.md" ]]; then
        cp "$WRITING_FRAMEWORK_HOME/.specify/memory/constitution.md" \
           "$TARGET_DIR/.specify/memory/constitution.md"
        common::info "  constitution.md copiada."
    else
        common::warn "  constitution.md no existe en el repo canónico; omitida."
    fi
else
    common::info "  constitution.md ya presente; se conserva."
fi

# Templates: copia los que falten en el destino. No sobreescribe.
if [[ -d "$WRITING_FRAMEWORK_HOME/.specify/templates" ]]; then
    shopt -s nullglob
    for tpl in "$WRITING_FRAMEWORK_HOME/.specify/templates/"*.md; do
        name="$(basename "$tpl")"
        if [[ ! -f "$TARGET_DIR/.specify/templates/$name" ]]; then
            cp "$tpl" "$TARGET_DIR/.specify/templates/$name"
            common::info "  $name copiada."
        else
            common::info "  $name ya presente; se conserva."
        fi
    done
    shopt -u nullglob
fi

# Spec Kit scripts (los hooks Git + check-prerequisites los necesitan).
if [[ -d "$WRITING_FRAMEWORK_HOME/.specify/scripts" ]]; then
    mkdir -p "$TARGET_DIR/.specify/scripts"
    cp -R "$WRITING_FRAMEWORK_HOME/.specify/scripts/." "$TARGET_DIR/.specify/scripts/"
    common::info "  scripts Spec Kit copiados."
fi

# ---------------------------------------------------------------------------
# Paso 4 — Hook registration (T022)
# ---------------------------------------------------------------------------

common::info "[4/6] Registrando hooks Spec Kit..."
register_hooks() {
    local src_yml="$WRITING_FRAMEWORK_HOME/.specify/extensions.yml"
    local dst_yml="$TARGET_DIR/.specify/extensions.yml"
    local src_ext_dir="$WRITING_FRAMEWORK_HOME/.specify/extensions"
    local dst_ext_dir="$TARGET_DIR/.specify/extensions"

    if [[ ! -f "$src_yml" ]]; then
        common::warn "  extensions.yml no existe en el repo canónico; omitido."
        return 0
    fi

    if [[ ! -f "$dst_yml" ]]; then
        cp "$src_yml" "$dst_yml"
        common::info "  extensions.yml copiado."
    else
        common::info "  extensions.yml ya presente; se conserva (merge manual recomendado)."
    fi

    if [[ -d "$src_ext_dir/git" ]]; then
        mkdir -p "$dst_ext_dir/git"
        # Copiar los archivos que falten en el destino.
        ( cd "$src_ext_dir" && find . -type f -print0 ) | while IFS= read -r -d '' rel; do
            target_file="$dst_ext_dir/${rel#./}"
            if [[ ! -e "$target_file" ]]; then
                mkdir -p "$(dirname "$target_file")"
                cp "$src_ext_dir/${rel#./}" "$target_file"
            fi
        done
        common::info "  extensions/git/ propagado (sin sobreescritura)."
    fi
    return 0
}
if ! register_hooks; then
    common::err "register_hooks falló."
    exit 60
fi

# ---------------------------------------------------------------------------
# Paso 5 — Render context (CLAUDE.md / AGENTS.md)
# ---------------------------------------------------------------------------

common::info "[5/6] Generando contexto del agente y recolectando datos del operador..."
render_context_args=("$TARGET_DIR" "$AGENT" "$LANGUAGE")
[[ $NON_INTERACTIVE -eq 1 ]] && render_context_args+=("--non-interactive")

context_json="$(bash "$SCRIPT_DIR/lib/render-context.sh" "${render_context_args[@]}")" || {
    rc=$?
    common::err "render-context.sh falló (rc=$rc)."
    exit 40
}

# Parsear operator_id / operator_email / project_type del JSON devuelto.
if command -v jq >/dev/null 2>&1; then
    OPERATOR_ID="$(echo "$context_json" | jq -r '.operator_id')"
    OPERATOR_EMAIL="$(echo "$context_json" | jq -r '.operator_email')"
    EFFECTIVE_AGENT="$(echo "$context_json" | jq -r '.agent_target')"
    EFFECTIVE_LANGUAGE="$(echo "$context_json" | jq -r '.language_primary')"
    PROJECT_TYPE="$(echo "$context_json" | jq -r '.project_type')"
else
    OPERATOR_ID="$(echo "$context_json" | grep -Eo '"operator_id"[[:space:]]*:[[:space:]]*"[^"]+"' | head -n1 | sed 's/.*"\([^"]*\)"$/\1/')"
    OPERATOR_EMAIL="$(echo "$context_json" | grep -Eo '"operator_email"[[:space:]]*:[[:space:]]*"[^"]+"' | head -n1 | sed 's/.*"\([^"]*\)"$/\1/')"
    EFFECTIVE_AGENT="$AGENT"
    EFFECTIVE_LANGUAGE="$LANGUAGE"
    PROJECT_TYPE="$(echo "$context_json" | grep -Eo '"project_type"[[:space:]]*:[[:space:]]*"[^"]+"' | head -n1 | sed 's/.*"\([^"]*\)"$/\1/')"
fi

if [[ -z "$OPERATOR_ID" || -z "$OPERATOR_EMAIL" ]]; then
    common::err "render-context.sh no devolvió operator_id/operator_email."
    exit 40
fi

# ---------------------------------------------------------------------------
# Paso 6 — Render manifest
# ---------------------------------------------------------------------------

common::info "[6/6] Generando .writeonmars-manifest.json..."
if ! bash "$SCRIPT_DIR/lib/render-manifest.sh" \
        "$TARGET_DIR" "$EFFECTIVE_AGENT" "$EFFECTIVE_LANGUAGE" \
        "$OPERATOR_ID" "$OPERATOR_EMAIL" "${PROJECT_TYPE:-}"; then
    common::err "render-manifest.sh falló."
    exit 50
fi

# ---------------------------------------------------------------------------
# Cierre
# ---------------------------------------------------------------------------

END_TS="$(date +%s)"
ELAPSED=$((END_TS - START_TS))
common::info "Instalación completada en ${ELAPSED} segundos."

if (( ELAPSED > 300 )); then
    common::warn "El tiempo excedió el objetivo SC-001 (<300 s)."
fi
