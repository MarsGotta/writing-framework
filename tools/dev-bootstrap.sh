#!/usr/bin/env bash
# tools/dev-bootstrap.sh
#
# Verifica los prerrequisitos de desarrollo del repositorio canónico de
# Write.OnMars. Está pensado para personas mantenedoras que clonan el repo
# y necesitan confirmar que su entorno local cumple con lo que describe la
# constitución § "Arquitectura del framework" y la tarea T003 de
# specs/001-framework-architecture/tasks.md.
#
# El script no instala nada. Reporta qué falta y cómo conseguirlo. Falla
# con exit code 1 si cualquier prerrequisito no se cumple, para que pueda
# usarse en CI o como gate previo a otras herramientas internas.
#
# Uso:
#   bash tools/dev-bootstrap.sh
#
# Salida:
#   - Una línea por herramienta verificada (OK o FAIL).
#   - Resumen final con el conteo de fallos.
#   - Exit 0 si todo está disponible; exit 1 si falta algo.

set -euo pipefail

# Acumulador de fallos. Las funciones de chequeo lo incrementan.
fallos=0

# imprime_fail <herramienta> <razon> <pista>
# Reporta un prerrequisito faltante con un mensaje uniforme.
imprime_fail() {
    local herramienta="$1"
    local razon="$2"
    local pista="$3"
    printf '[FAIL] %s: %s — instalar con %s\n' "$herramienta" "$razon" "$pista"
    fallos=$((fallos + 1))
}

# imprime_ok <herramienta> <detalle>
# Reporta un prerrequisito cumplido.
imprime_ok() {
    local herramienta="$1"
    local detalle="$2"
    printf '[OK]   %s: %s\n' "$herramienta" "$detalle"
}

# verifica_bash
# Bash 5+ es requisito de la constitución § Arquitectura del framework
# (idioma de los scripts de instalación) y de plan.md § Technical Context.
verifica_bash() {
    local version_mayor
    version_mayor="${BASH_VERSINFO[0]:-0}"
    if [[ "$version_mayor" -ge 5 ]]; then
        imprime_ok "bash" "version ${BASH_VERSION}"
    else
        imprime_fail "bash" \
            "se requiere Bash 5 o superior, detectado ${BASH_VERSION:-desconocido}" \
            "'brew install bash' en macOS o el gestor de paquetes del sistema en Linux"
    fi
}

# verifica_git
# Git ≥ 2.30 es la base mínima asumida por Spec Kit y por los hooks
# Git registrados en .specify/extensions/git/.
verifica_git() {
    if ! command -v git >/dev/null 2>&1; then
        imprime_fail "git" \
            "no se encontró el binario en PATH" \
            "'brew install git' o 'apt-get install git'"
        return
    fi
    local version_completa
    version_completa="$(git --version 2>/dev/null | awk '{print $3}')"
    local mayor menor
    mayor="$(printf '%s' "$version_completa" | awk -F. '{print $1}')"
    menor="$(printf '%s' "$version_completa" | awk -F. '{print $2}')"
    mayor="${mayor:-0}"
    menor="${menor:-0}"
    if (( mayor > 2 )) || { (( mayor == 2 )) && (( menor >= 30 )); }; then
        imprime_ok "git" "version ${version_completa}"
    else
        imprime_fail "git" \
            "se requiere Git 2.30 o superior, detectado ${version_completa}" \
            "actualizar con el gestor de paquetes del sistema"
    fi
}

# verifica_jq
# jq se usa para validar y manipular JSON (manifiesto, pass outputs).
verifica_jq() {
    if command -v jq >/dev/null 2>&1; then
        local version_completa
        version_completa="$(jq --version 2>/dev/null)"
        imprime_ok "jq" "${version_completa}"
    else
        imprime_fail "jq" \
            "no se encontró el binario en PATH" \
            "'brew install jq' o 'apt-get install jq'"
    fi
}

# verifica_ajv
# ajv valida JSON Schemas (contracts/manifest-schema.json,
# contracts/citation-record.schema.json). Se ejecuta vía npx para no
# exigir instalación global.
verifica_ajv() {
    if ! command -v npx >/dev/null 2>&1; then
        imprime_fail "ajv" \
            "no se encontró 'npx' en PATH (Node.js no instalado)" \
            "instalar Node.js 20+ desde https://nodejs.org o via 'brew install node'"
        return
    fi
    if version_completa="$(npx --no-install ajv --version 2>/dev/null)"; then
        imprime_ok "ajv" "version ${version_completa} (via npx)"
    elif version_completa="$(npx ajv --version 2>/dev/null)"; then
        imprime_ok "ajv" "version ${version_completa} (descargado por npx)"
    else
        imprime_fail "ajv" \
            "npx no pudo resolver el paquete 'ajv-cli'" \
            "'npm install -g ajv-cli' o garantizar acceso a la red para que npx lo descargue"
    fi
}

# verifica_shellcheck
# shellcheck audita los scripts Bash del framework (install/, tools/,
# tests/smoke/) y se invoca antes de cada release.
verifica_shellcheck() {
    if command -v shellcheck >/dev/null 2>&1; then
        local version_completa
        version_completa="$(shellcheck --version 2>/dev/null | awk '/^version:/ {print $2}')"
        imprime_ok "shellcheck" "version ${version_completa:-desconocida}"
    else
        imprime_fail "shellcheck" \
            "no se encontró el binario en PATH" \
            "'brew install shellcheck' o 'apt-get install shellcheck'"
    fi
}

# Cabecera informativa para que la salida sea identificable en logs.
printf 'Write.OnMars — verificación de entorno de desarrollo\n'
printf '====================================================\n'

verifica_bash
verifica_git
verifica_jq
verifica_ajv
verifica_shellcheck

printf '\n'
if (( fallos == 0 )); then
    printf '[OK] dev environment ready\n'
    exit 0
else
    printf '[FAIL] %d prerrequisito(s) sin cumplir. Resolver e intentar de nuevo.\n' "$fallos"
    exit 1
fi
