#!/usr/bin/env bash
# detect-existing.sh — detecta artefactos preexistentes en el repo destino.
#
# Cubre FR-003 (detección y fusión, no sobreescritura).
# Emite por stdout un objeto JSON parseable por jq con las siguientes claves:
#   spec_kit_present
#   writeonmars_present
#   claude_md_present
#   agents_md_present
#   claude_skills_dir_present
#   conflicts             (array de strings)
#
# Uso:
#   detect-existing.sh <target_dir>
#
# El script no toma decisiones; solo reporta. La política de qué hacer ante
# cada conflicto la decide install.sh.

set -euo pipefail

# Permitir ejecución directa o sourcing desde install.sh.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
WOM_LOG_PREFIX="detect"

if [[ $# -lt 1 ]]; then
    common::err "Uso: detect-existing.sh <target_dir>"
    exit 2
fi

TARGET_DIR="$1"

if [[ ! -d "$TARGET_DIR" ]]; then
    common::err "Directorio destino no existe: $TARGET_DIR"
    exit 2
fi

# Necesitamos saber dónde está el repo canónico para comparar versiones.
# Si install.sh nos llamó, ya exportó WRITING_FRAMEWORK_HOME; si nos invocan
# directamente, lo deducimos del path del script.
if [[ -z "${WRITING_FRAMEWORK_HOME:-}" ]]; then
    WRITING_FRAMEWORK_HOME="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

bool_json() {
    if [[ "$1" == "true" ]]; then
        echo "true"
    else
        echo "false"
    fi
}

spec_kit_present="false"
if [[ -f "$TARGET_DIR/.specify/memory/constitution.md" \
   || -f "$TARGET_DIR/.specify/templates/spec-template.md" ]]; then
    spec_kit_present="true"
fi

writeonmars_present="false"
if [[ -f "$TARGET_DIR/.writeonmars-manifest.json" ]]; then
    writeonmars_present="true"
fi

claude_md_present="false"
if [[ -f "$TARGET_DIR/CLAUDE.md" ]]; then
    claude_md_present="true"
fi

agents_md_present="false"
if [[ -f "$TARGET_DIR/AGENTS.md" ]]; then
    agents_md_present="true"
fi

claude_skills_dir_present="false"
if [[ -d "$TARGET_DIR/.claude/skills" ]]; then
    claude_skills_dir_present="true"
fi

# ---------------------------------------------------------------------------
# Detectar conflictos
# ---------------------------------------------------------------------------
conflicts=()

if [[ "$writeonmars_present" == "true" ]]; then
    # Comparar framework_version del manifiesto contra el canónico.
    canonical_version="$(common::framework_version)"
    target_version=""
    if command -v jq >/dev/null 2>&1; then
        target_version="$(jq -r '.framework_version // ""' "$TARGET_DIR/.writeonmars-manifest.json" 2>/dev/null || true)"
    else
        # Fallback grep si jq no está disponible.
        target_version="$(grep -Eo '"framework_version"[[:space:]]*:[[:space:]]*"[^"]+"' \
            "$TARGET_DIR/.writeonmars-manifest.json" \
            | head -n 1 \
            | grep -Eo '"[0-9.]+[^"]*"$' \
            | tr -d '"' || true)"
    fi
    if [[ -n "$target_version" && "$target_version" != "$canonical_version" ]]; then
        conflicts+=("writeonmars: version mismatch (target=$target_version vs canonical=$canonical_version)")
    fi
fi

# ---------------------------------------------------------------------------
# Emisión JSON
# ---------------------------------------------------------------------------

# Construimos el array de conflicts como JSON array safe.
conflicts_json="[]"
if [[ ${#conflicts[@]} -gt 0 ]]; then
    if command -v jq >/dev/null 2>&1; then
        conflicts_json="$(printf '%s\n' "${conflicts[@]}" | jq -R . | jq -s .)"
    else
        # Construcción manual rudimentaria; los strings no llevan comillas internas.
        conflicts_json="["
        local_first=1
        for c in "${conflicts[@]}"; do
            if [[ $local_first -eq 1 ]]; then
                conflicts_json+="\"$c\""
                local_first=0
            else
                conflicts_json+=",\"$c\""
            fi
        done
        conflicts_json+="]"
    fi
fi

cat <<EOF
{
  "spec_kit_present": $(bool_json "$spec_kit_present"),
  "writeonmars_present": $(bool_json "$writeonmars_present"),
  "claude_md_present": $(bool_json "$claude_md_present"),
  "agents_md_present": $(bool_json "$agents_md_present"),
  "claude_skills_dir_present": $(bool_json "$claude_skills_dir_present"),
  "conflicts": $conflicts_json
}
EOF
