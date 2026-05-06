#!/usr/bin/env bash
# specify-after-install.sh — smoke test: tras un install, los scripts de
# Spec Kit funcionan en el destino.
#
# Cubre US1 §AC3.
#
# Asserts:
#   - bash <tmp>/.specify/scripts/bash/check-prerequisites.sh --json --paths-only
#     retorna JSON parseable con jq.
#   - <tmp>/.specify/templates/spec-template.md existe (versión genérica de Spec
#     Kit hereda; el template editorial de T030 vendrá luego).

set -euo pipefail

FRAMEWORK_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_NAME="specify-after-install"

TMP="$(mktemp -d -t "writeonmars-smoke-XXXXXX")"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

fail() {
    printf '[%s][FAIL] %s\n' "$TEST_NAME" "$*" >&2
    exit 1
}
pass() {
    printf '[%s][PASS] %s\n' "$TEST_NAME" "$*"
}

cd "$TMP"
git init -q

WOM_PROJECT_TYPE=guia \
WOM_AUDIENCE="Personas desarrolladoras que evalúan Spec Kit en repos limpios" \
WOM_DOMAIN="Tooling de especificación" \
WOM_OPERATOR_ID=smoke.test \
WOM_OPERATOR_EMAIL=smoke@example.com \
bash "$FRAMEWORK_HOME/install/install.sh" \
    --target-dir "$TMP" \
    --agent claude-code \
    --language es \
    --non-interactive >"$TMP/install.log" 2>&1 \
    || { cat "$TMP/install.log"; fail "install.sh devolvió código distinto de 0"; }

# Para que check-prerequisites.sh pase su propia validación necesitamos que el
# repo destino esté en una rama tipo "###-name". Spec Kit valida ramas con un
# patrón que reconoce 'main' como branch principal pero exige feature branches
# para ciertos comandos. Para este smoke test basta con que el script corra y
# devuelva JSON parseable.

# Crear un commit inicial mínimo para que estamos en main con HEAD válido.
( cd "$TMP" && git add -A && git -c user.email="smoke@example.com" -c user.name="smoke" commit -q -m "init" ) || true

# Cambiar a una feature branch sintética para que check-prerequisites no
# rechace el contexto.
( cd "$TMP" && git checkout -q -b 001-smoke-test ) || true

CHECK_SCRIPT="$TMP/.specify/scripts/bash/check-prerequisites.sh"
if [[ ! -x "$CHECK_SCRIPT" ]]; then
    chmod +x "$CHECK_SCRIPT" 2>/dev/null || true
fi

if [[ ! -f "$CHECK_SCRIPT" ]]; then
    fail "check-prerequisites.sh no existe en $CHECK_SCRIPT"
fi

# El script puede no ser ejecutable directamente; invocar con bash.
out="$(cd "$TMP" && bash "$CHECK_SCRIPT" --json --paths-only 2>&1)" \
    || fail "check-prerequisites.sh falló: $out"

# Asegurar que la salida es JSON parseable.
if command -v jq >/dev/null 2>&1; then
    if ! echo "$out" | jq '.' >/dev/null 2>&1; then
        fail "check-prerequisites.sh no devolvió JSON parseable. Salida: $out"
    fi
    pass "check-prerequisites.sh devolvió JSON válido"
else
    # Fallback: chequear que parece JSON.
    if [[ "$out" != *"{"* ]] || [[ "$out" != *"}"* ]]; then
        fail "salida sin estructura JSON visible (jq no disponible para validar)"
    fi
    pass "check-prerequisites.sh devolvió contenido JSON-like (jq no disponible para validación estricta)"
fi

# Verificar que el spec-template existe.
if [[ ! -f "$TMP/.specify/templates/spec-template.md" ]]; then
    fail ".specify/templates/spec-template.md no existe"
fi
pass "spec-template.md disponible (versión heredada de Spec Kit; T030 la adaptará)"

printf '[%s][OK] todos los asserts pasaron\n' "$TEST_NAME"
