#!/usr/bin/env bash
# install-preserves-claudemd.sh — smoke test: el instalador no destruye un
# CLAUDE.md preexistente.
#
# Cubre US1 §AC2.
#
# Pre-condición: crear CLAUDE.md con un marker único en el destino.
# Asserts post-install:
#   - El marker original sigue presente.
#   - El bloque <!-- WRITEONMARS START --> ... <!-- WRITEONMARS END --> se
#     añadió al archivo.
#   - El contenido fuera del bloque WriteOnMars se conserva intacto.

set -euo pipefail

FRAMEWORK_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_NAME="install-preserves-claudemd"

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

# 1. Pre-crear CLAUDE.md con marker.
MARKER="CUSTOM-USER-MARKER-XYZ123"
cat >CLAUDE.md <<EOF
# Mi CLAUDE.md previo

Este archivo lo mantengo yo a mano. Línea con marker: $MARKER

## Mis convenciones

- regla 1
- regla 2
EOF
ORIGINAL_HASH="$(shasum -a 256 CLAUDE.md | awk '{print $1}')"

# 2. Instalar.
WOM_PROJECT_TYPE=guia \
WOM_AUDIENCE="Personas desarrolladoras técnicas que necesitan onboarding" \
WOM_DOMAIN="Repositorios legacy" \
WOM_OPERATOR_ID=smoke.test \
WOM_OPERATOR_EMAIL=smoke@example.com \
bash "$FRAMEWORK_HOME/install/install.sh" \
    --target-dir "$TMP" \
    --agent claude-code \
    --language es \
    --non-interactive >"$TMP/install.log" 2>&1 \
    || { cat "$TMP/install.log"; fail "install.sh devolvió código distinto de 0"; }

# 3. Verificar que el marker sigue presente.
if ! grep -q "$MARKER" CLAUDE.md; then
    fail "el marker '$MARKER' no aparece en CLAUDE.md tras la instalación"
fi
pass "marker original preservado"

# 4. Verificar que se añadió el bloque WriteOnMars.
if ! grep -q "<!-- WRITEONMARS START -->" CLAUDE.md; then
    fail "no se encontró <!-- WRITEONMARS START --> en CLAUDE.md"
fi
if ! grep -q "<!-- WRITEONMARS END -->" CLAUDE.md; then
    fail "no se encontró <!-- WRITEONMARS END --> en CLAUDE.md"
fi
pass "bloque WriteOnMars añadido"

# 5. Verificar que las convenciones originales del usuario siguen ahí.
if ! grep -q "## Mis convenciones" CLAUDE.md; then
    fail "la sección '## Mis convenciones' del usuario fue removida"
fi
if ! grep -q "regla 1" CLAUDE.md || ! grep -q "regla 2" CLAUDE.md; then
    fail "las reglas del usuario fueron alteradas"
fi
pass "contenido original fuera del bloque WriteOnMars intacto"

# 6. Confirmar que el archivo creció (no es idéntico al original).
NEW_HASH="$(shasum -a 256 CLAUDE.md | awk '{print $1}')"
if [[ "$NEW_HASH" == "$ORIGINAL_HASH" ]]; then
    fail "CLAUDE.md no fue modificado; se esperaba la inyección del bloque"
fi
pass "CLAUDE.md fue extendido sin sobreescribirse"

printf '[%s][OK] todos los asserts pasaron\n' "$TEST_NAME"
