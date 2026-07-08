#!/usr/bin/env bash
# install-on-empty-repo.sh — smoke test: instalación sobre repo Git vacío.
#
# Cubre US1 §AC1 + SC-001 (<5 minutos / <300 s).
#
# Asserts:
#   - .specify/memory/constitution.md existe
#   - .specify/templates/spec-template.md, plan-template.md, tasks-template.md,
#     checklist-template.md existen (los heredados de Spec Kit que el repo
#     canónico tenga)
#   - .claude/skills/marcela-prose/, technical-guide-design/, writeonmars-install/
#     existen
#   - .writeonmars-manifest.json existe y valida contra el schema (si hay validador)
#   - .specify/extensions.yml existe
#   - El timing reporta <300 segundos.

set -euo pipefail

# install.sh (legacy) exige Bash 5: en un bash mas viejo este smoke se salta
# con exit 99 (SKIP en run-all.sh), nunca un falso PASS ni un FAIL espurio.
if [ "${BASH_VERSINFO[0]:-0}" -lt 5 ]; then
    echo "skip: install.sh requiere Bash 5+ (actual: $BASH_VERSION)"
    exit 99
fi

FRAMEWORK_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_NAME="install-on-empty-repo"

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

# 1. Crear repo vacío.
cd "$TMP"
git init -q

# 2. Ejecutar instalador no-interactivo.
START_TS="$(date +%s)"
WOM_PROJECT_TYPE=guia \
WOM_AUDIENCE="Personas desarrolladoras que mantienen guías técnicas internas" \
WOM_DOMAIN="Onboarding técnico en monorepos" \
WOM_OPERATOR_ID=smoke.test \
WOM_OPERATOR_EMAIL=smoke@example.com \
bash "$FRAMEWORK_HOME/install/install.sh" \
    --target-dir "$TMP" \
    --agent claude-code \
    --language es \
    --non-interactive >"$TMP/install.log" 2>&1 \
    || { cat "$TMP/install.log"; fail "install.sh devolvió código distinto de 0"; }

END_TS="$(date +%s)"
ELAPSED=$((END_TS - START_TS))

# 3. Asserts de existencia.
required_files=(
    ".specify/memory/constitution.md"
    ".specify/templates/spec-template.md"
    ".specify/templates/plan-template.md"
    ".specify/templates/tasks-template.md"
    ".specify/templates/checklist-template.md"
    ".specify/extensions.yml"
    ".writeonmars-manifest.json"
    "CLAUDE.md"
)

for f in "${required_files[@]}"; do
    if [[ ! -e "$TMP/$f" ]]; then
        fail "Archivo faltante: $f"
    fi
done
pass "todos los archivos requeridos existen"

required_dirs=(
    ".claude/skills/marcela-prose"
    ".claude/skills/technical-guide-design"
    ".claude/skills/writeonmars-install"
)

for d in "${required_dirs[@]}"; do
    if [[ ! -d "$TMP/$d" ]]; then
        fail "Directorio faltante: $d"
    fi
done
pass "todas las skills bundled están instaladas"

# 4. Validar manifiesto contra el schema si tenemos validador.
if command -v python3 >/dev/null 2>&1; then
    if python3 -c "import jsonschema" 2>/dev/null; then
        if ! python3 - "$FRAMEWORK_HOME/writeonmars/contracts/manifest-schema.json" "$TMP/.writeonmars-manifest.json" <<'PYEOF' >/dev/null 2>&1
import json, sys, jsonschema
with open(sys.argv[1]) as f: schema = json.load(f)
with open(sys.argv[2]) as f: instance = json.load(f)
jsonschema.validate(instance=instance, schema=schema)
PYEOF
        then
            fail "manifiesto no valida contra el schema"
        fi
        pass "manifiesto valida contra writeonmars/contracts/manifest-schema.json"
    else
        printf '[%s][skip] python jsonschema no disponible; validación schema omitida.\n' "$TEST_NAME"
    fi
else
    printf '[%s][skip] python3 no disponible; validación schema omitida.\n' "$TEST_NAME"
fi

# 4b. La versión del manifiesto DEBE coincidir con el pie de la constitución
# instalada. Bootstrap la deriva del fichero (nunca de una constante): este check
# caza cualquier regresión a hardcode, que ya se desincronizó dos veces.
const_v="$(grep -oE '^\*\*Version\*\*: [0-9]+\.[0-9]+\.[0-9]+' "$TMP/.specify/memory/constitution.md" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)"
man_v="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['constitution_version'])" "$TMP/.writeonmars-manifest.json")"
if [[ -z "$const_v" || "$const_v" != "$man_v" ]]; then
    fail "constitution_version del manifiesto ($man_v) no coincide con el pie de la constitución instalada ($const_v)"
fi
pass "constitution_version del manifiesto coincide con la constitución instalada ($const_v)"

# 5. SC-001: timing <300 s.
if (( ELAPSED >= 300 )); then
    fail "instalación tomó ${ELAPSED} s; SC-001 exige <300 s"
fi
pass "instalación completada en ${ELAPSED} s (SC-001 OK)"

# Exportar timing para que run-all.sh lo recolecte si quiere.
printf '%s\n' "$ELAPSED" >"$TMP/elapsed.txt"
printf '[%s][OK] todos los asserts pasaron (%ss)\n' "$TEST_NAME" "$ELAPSED"
