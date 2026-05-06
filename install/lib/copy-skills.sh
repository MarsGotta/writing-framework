#!/usr/bin/env bash
# copy-skills.sh — copia (o enlaza) las skills bundled en el destino.
#
# Cubre FR-028 (skills bundled distribuidas con el framework) y la regla de
# idempotencia de la instalación (FR-001).
#
# Skills cubiertas:
#   - marcela-prose
#   - technical-guide-design
#   - todas las writeonmars-* presentes en <source>/.claude/skills/
#
# Uso:
#   copy-skills.sh <source_skills_dir> <target_dir> [--symlink] [--force]
#
# Argumentos:
#   <source_skills_dir>   Directorio fuente de las skills (típicamente
#                         <framework_home>/.claude/skills).
#   <target_dir>          Repo destino. La skill se copia a
#                         <target_dir>/.claude/skills/<skill_name>/.
#   --symlink             En lugar de copiar, crea un enlace simbólico (R2).
#   --force               Sobreescribe la skill destino aunque exista una
#                         versión distinta.
#
# Salida (stdout): tabla simple con una línea por skill:
#   <action>\t<skill_name>\t<version_source>\t<version_target_anterior_o_->
# action ∈ {copied, linked, skipped, warned, replaced}.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
WOM_LOG_PREFIX="copy-skills"

usage() {
    cat <<EOF
Uso: copy-skills.sh <source_skills_dir> <target_dir> [--symlink] [--force]
EOF
}

if [[ $# -lt 2 ]]; then
    usage
    exit 2
fi

SOURCE_SKILLS="$1"
TARGET_DIR="$2"
shift 2

USE_SYMLINK=0
FORCE=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        --symlink) USE_SYMLINK=1 ;;
        --force) FORCE=1 ;;
        -h|--help) usage; exit 0 ;;
        *)
            common::err "Argumento desconocido: $1"
            usage
            exit 2
            ;;
    esac
    shift
done

if [[ ! -d "$SOURCE_SKILLS" ]]; then
    common::die 30 "Directorio fuente de skills no existe: $SOURCE_SKILLS"
fi
if [[ ! -d "$TARGET_DIR" ]]; then
    common::die 30 "Directorio destino no existe: $TARGET_DIR"
fi

mkdir -p "$TARGET_DIR/.claude/skills"

# Determinar lista de skills a procesar.
candidate_skills=()
[[ -d "$SOURCE_SKILLS/marcela-prose" ]] && candidate_skills+=("marcela-prose")
[[ -d "$SOURCE_SKILLS/technical-guide-design" ]] && candidate_skills+=("technical-guide-design")

# Iterar buscando writeonmars-*.
shopt -s nullglob
for dir in "$SOURCE_SKILLS"/writeonmars-*; do
    if [[ -d "$dir" ]]; then
        candidate_skills+=("$(basename "$dir")")
    fi
done
shopt -u nullglob

if [[ ${#candidate_skills[@]} -eq 0 ]]; then
    common::warn "No se encontró ninguna skill bundled en $SOURCE_SKILLS."
    exit 0
fi

for skill in "${candidate_skills[@]}"; do
    src="$SOURCE_SKILLS/$skill"
    dst="$TARGET_DIR/.claude/skills/$skill"

    src_version="$(common::skill_semver "$src/VERSION")"
    if [[ -z "$src_version" ]]; then
        # Si la skill canónica no tiene un VERSION semver explícito, igual la
        # copiamos pero advertimos.
        src_version="0.0.0"
        common::warn "Skill $skill sin VERSION semver válido; se asume 0.0.0."
    fi

    target_version="-"
    if [[ -e "$dst" ]]; then
        target_version="$(common::skill_semver "$dst/VERSION")"
        target_version="${target_version:-0.0.0}"
    fi

    if [[ -e "$dst" ]]; then
        if [[ "$src_version" == "$target_version" ]]; then
            printf 'skipped\t%s\t%s\t%s\n' "$skill" "$src_version" "$target_version"
            continue
        fi
        if [[ $FORCE -eq 0 ]]; then
            common::warn "Skill $skill: versión destino ($target_version) difiere de canónica ($src_version). Use --force para sobreescribir."
            printf 'warned\t%s\t%s\t%s\n' "$skill" "$src_version" "$target_version"
            continue
        fi
        # FORCE: borrar destino antes de re-crear.
        rm -rf "$dst"
    fi

    if [[ $USE_SYMLINK -eq 1 ]]; then
        ln -s "$src" "$dst"
        if [[ -e "$dst.tmp" ]]; then rm -rf "$dst.tmp"; fi
        if [[ "$target_version" == "-" ]]; then
            printf 'linked\t%s\t%s\t-\n' "$skill" "$src_version"
        else
            printf 'replaced\t%s\t%s\t%s\n' "$skill" "$src_version" "$target_version"
        fi
    else
        cp -R "$src" "$dst"
        if [[ "$target_version" == "-" ]]; then
            printf 'copied\t%s\t%s\t-\n' "$skill" "$src_version"
        else
            printf 'replaced\t%s\t%s\t%s\n' "$skill" "$src_version" "$target_version"
        fi
    fi
done
