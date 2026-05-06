#!/usr/bin/env bash
# render-context.sh — cuestionario inicial + render de CLAUDE.md / AGENTS.md.
#
# Cubre FR-002 (cuestionario inicial obligatorio) y FR-007 (contexto de
# proyecto que el agente leerá antes de redactar).
#
# Uso:
#   render-context.sh <target_dir> <agent> <language> [--non-interactive]
#
# Si se pasa --non-interactive, las respuestas vienen de env vars:
#   WOM_PROJECT_TYPE      (guia|manual|libro|articulo|tutorial)
#   WOM_AUDIENCE          (texto libre, ≥20 caracteres)
#   WOM_DOMAIN            (texto libre)
#   WOM_OPERATOR_ID       (identificador estable; ej. nombre.apellido)
#   WOM_OPERATOR_EMAIL    (email del operador para signing matrix)
#
# Salida principal: archivo CLAUDE.md (si agent=claude-code) o AGENTS.md
# (resto). Si ya existía, fusiona entre <!-- WRITEONMARS START --> y
# <!-- WRITEONMARS END --> sin tocar el resto del documento.
#
# Salida secundaria (stdout): JSON {operator_id, operator_email, project_type,
# audience, domain} para que render-manifest.sh lo consuma.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
WOM_LOG_PREFIX="render-context"

usage() {
    cat <<EOF
Uso: render-context.sh <target_dir> <agent> <language> [--non-interactive]
EOF
}

if [[ $# -lt 3 ]]; then
    usage
    exit 2
fi

TARGET_DIR="$1"
AGENT="$2"
LANGUAGE="$3"
shift 3

NON_INTERACTIVE=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        --non-interactive) NON_INTERACTIVE=1 ;;
        -h|--help) usage; exit 0 ;;
        *) common::err "Argumento desconocido: $1"; exit 2 ;;
    esac
    shift
done

if [[ ! -d "$TARGET_DIR" ]]; then
    common::die 40 "Directorio destino no existe: $TARGET_DIR"
fi

# ---------------------------------------------------------------------------
# Helpers de cuestionario
# ---------------------------------------------------------------------------

ask() {
    local prompt="$1"
    local default="${2:-}"
    local response=""
    if [[ -n "$default" ]]; then
        printf '%s [%s]: ' "$prompt" "$default" >&2
    else
        printf '%s: ' "$prompt" >&2
    fi
    IFS= read -r response || response=""
    if [[ -z "$response" && -n "$default" ]]; then
        response="$default"
    fi
    printf '%s' "$response"
}

validate_project_type() {
    case "$1" in
        guia|manual|libro|articulo|tutorial) return 0 ;;
        *) return 1 ;;
    esac
}

# ---------------------------------------------------------------------------
# Recolección de respuestas
# ---------------------------------------------------------------------------

PROJECT_TYPE=""
AUDIENCE=""
DOMAIN=""
OPERATOR_ID=""
OPERATOR_EMAIL=""

if [[ $NON_INTERACTIVE -eq 1 ]]; then
    PROJECT_TYPE="${WOM_PROJECT_TYPE:-guia}"
    AUDIENCE="${WOM_AUDIENCE:-}"
    DOMAIN="${WOM_DOMAIN:-}"
    OPERATOR_ID="${WOM_OPERATOR_ID:-operador-desconocido}"
    OPERATOR_EMAIL="${WOM_OPERATOR_EMAIL:-noreply@example.org}"

    if ! validate_project_type "$PROJECT_TYPE"; then
        common::die 40 "WOM_PROJECT_TYPE inválido: '$PROJECT_TYPE'. Esperado: guia|manual|libro|articulo|tutorial."
    fi
    if [[ ${#AUDIENCE} -lt 20 ]]; then
        common::die 40 "WOM_AUDIENCE debe tener al menos 20 caracteres."
    fi
    if [[ -z "$DOMAIN" ]]; then
        common::die 40 "WOM_DOMAIN no puede estar vacío."
    fi
else
    common::info "Cuestionario inicial Write.OnMars (5 preguntas)."
    while true; do
        PROJECT_TYPE="$(ask "Tipo de proyecto editorial (guia|manual|libro|articulo|tutorial)" "guia")"
        if validate_project_type "$PROJECT_TYPE"; then break; fi
        common::warn "Valor no válido. Intenta de nuevo."
    done
    # Agente: ya viene del flag de install.sh.
    PROJECT_AGENT="$(ask "Agente prioritario" "$AGENT")"
    AGENT="$PROJECT_AGENT"
    LANGUAGE="$(ask "Idioma primario (ISO-639, ej. es)" "$LANGUAGE")"
    while true; do
        AUDIENCE="$(ask "Audiencia general (texto libre, mínimo 20 caracteres)" "")"
        if [[ ${#AUDIENCE} -ge 20 ]]; then break; fi
        common::warn "Audiencia demasiado corta; describe a quién va dirigida la guía con detalle."
    done
    while true; do
        DOMAIN="$(ask "Dominio técnico" "")"
        if [[ -n "$DOMAIN" ]]; then break; fi
        common::warn "El dominio no puede estar vacío."
    done
    while true; do
        OPERATOR_ID="$(ask "Identificador del operador humano (ej. marcela.gotta)" "")"
        if [[ -n "$OPERATOR_ID" ]]; then break; fi
    done
    while true; do
        OPERATOR_EMAIL="$(ask "Email del operador humano" "")"
        if [[ "$OPERATOR_EMAIL" =~ ^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$ ]]; then
            break
        fi
        common::warn "Email no válido."
    done
fi

# ---------------------------------------------------------------------------
# Determinar archivo de contexto a usar.
# ---------------------------------------------------------------------------

context_file=""
if [[ "$AGENT" == "claude-code" ]]; then
    context_file="$TARGET_DIR/CLAUDE.md"
else
    context_file="$TARGET_DIR/AGENTS.md"
fi

START_MARKER="<!-- WRITEONMARS START -->"
END_MARKER="<!-- WRITEONMARS END -->"

# Bloque WriteOnMars que iremos a inyectar.
build_block() {
    cat <<EOF
$START_MARKER
# Contexto Write.OnMars

**Tipo de proyecto editorial**: $PROJECT_TYPE
**Audiencia**: $AUDIENCE
**Dominio técnico**: $DOMAIN
**Idioma primario**: $LANGUAGE
**Agente prioritario**: $AGENT

## Reglas microestilísticas heredadas (constitución § I y § IV)

- Voz natural y sobria: ninguna frase comprimida que obligue a reconstruir la intención.
- Evita "No es X: es Y" más de una vez por capítulo.
- Sin pronombres vagos sin referente explícito.
- Sin transiciones secas ("vamos a verlo", "pasemos al siguiente punto"); la transición explica por qué cambia el tema.
- Sin entusiasmo artificial ni lenguaje promocional.
- Univocidad terminológica: un término por concepto. La repetición exacta del término técnico es preferible a la variación sinonímica cuando ello compromete la precisión.
- Anglicismos solo cuando no exista equivalente preciso en español; justificar en el glosario.
- Pasiva refleja por defecto sobre la pasiva perifrástica.

## Referencias normativas

- Constitución vigente: \`.specify/memory/constitution.md\`
- Manifiesto del proyecto: \`.writeonmars-manifest.json\`
- Contrato de citación: \`contracts/citation-contract.md\` (en el repo canónico) o el espejo local si está copiado.

$END_MARKER
EOF
}

# ---------------------------------------------------------------------------
# Inyectar / fusionar bloque WriteOnMars en el archivo de contexto.
# ---------------------------------------------------------------------------

block_content="$(build_block)"

if [[ -f "$context_file" ]]; then
    if grep -q "$START_MARKER" "$context_file" && grep -q "$END_MARKER" "$context_file"; then
        # Reemplazar el bloque entre marcadores.
        tmp="$(mktemp)"
        awk -v start="$START_MARKER" -v end="$END_MARKER" -v block="$block_content" '
            BEGIN { inblock = 0; printed = 0 }
            {
                if ($0 == start) {
                    if (!printed) { print block; printed = 1 }
                    inblock = 1
                    next
                }
                if (inblock && $0 == end) {
                    inblock = 0
                    next
                }
                if (!inblock) print $0
            }
        ' "$context_file" >"$tmp"
        mv "$tmp" "$context_file"
    else
        # No hay bloque previo: anexamos al final, separado por blank line.
        {
            cat "$context_file"
            printf '\n'
            printf '%s\n' "$block_content"
        } >"$context_file.tmp"
        mv "$context_file.tmp" "$context_file"
    fi
else
    # Crear archivo nuevo solo con el bloque WriteOnMars.
    printf '%s\n' "$block_content" >"$context_file"
fi

common::info "Contexto agente actualizado: $context_file"

# ---------------------------------------------------------------------------
# Emisión JSON para render-manifest.sh.
# ---------------------------------------------------------------------------

# Escapar dobles comillas en strings antes de meterlas en JSON.
json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    printf '%s' "$s"
}

cat <<EOF
{
  "operator_id": "$(json_escape "$OPERATOR_ID")",
  "operator_email": "$(json_escape "$OPERATOR_EMAIL")",
  "project_type": "$(json_escape "$PROJECT_TYPE")",
  "audience": "$(json_escape "$AUDIENCE")",
  "domain": "$(json_escape "$DOMAIN")",
  "agent_target": "$(json_escape "$AGENT")",
  "language_primary": "$(json_escape "$LANGUAGE")"
}
EOF
