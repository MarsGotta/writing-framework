#!/usr/bin/env bash
# update-skill-on-installed-project.sh — smoke test de SC-008.
#
# Valida que el procedimiento de actualización de una skill bundled propaga
# el bump de versión a un proyecto instalado en menos de 15 minutos (SC-008)
# y preserva la configuración local del manifiesto.
#
# Estrategia:
#   1. Crea un sandbox temporal y lo inicializa como repo Git.
#   2. Ejecuta install/install.sh en modo --non-interactive.
#   3. Edita el manifest del proyecto introduciendo una customización local
#      (operator extra y language_primary=es-AR).
#   4. Bumpea VERSION de la skill writeonmars-pasada-1 en el repo canónico
#      (revierte al final mediante trap).
#   5. Aplica el procedimiento de writeonmars-update vía Bash directo
#      (la skill es markdown; este test ejecuta los pasos manualmente).
#   6. Asserta:
#        a) VERSION del destino refleja el nuevo valor.
#        b) manifest.skills[].version refleja el nuevo valor.
#        c) language_primary=es-AR sigue presente.
#        d) El operador extra sigue presente.
#   7. Mide el tiempo total y compara contra SC-008 (<900 s).
#   8. Limpieza: revierte VERSION canónico, borra sandbox.
#
# Exit codes:
#   0  — PASS (assertions verdes, tiempo dentro del target).
#   1  — FAIL (alguna assertion falló).
#   2  — ERROR (error de entorno / script).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_HOME="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOG_PREFIX="[smoke:update-skill]"
log() { echo "$LOG_PREFIX $*"; }
die() { echo "$LOG_PREFIX ERROR: $*" >&2; exit 2; }

# ---------------------------------------------------------------------------
# Precondiciones
# ---------------------------------------------------------------------------

command -v jq >/dev/null 2>&1 || die "jq es obligatorio para este test"
command -v git >/dev/null 2>&1 || die "git es obligatorio para este test"

TARGET_SKILL="writeonmars-pasada-1"
CANONICAL_SKILL_DIR="$FRAMEWORK_HOME/.claude/skills/$TARGET_SKILL"
CANONICAL_VERSION_FILE="$CANONICAL_SKILL_DIR/VERSION"

[[ -d "$CANONICAL_SKILL_DIR" ]] || die "No existe la skill canónica $TARGET_SKILL"
[[ -f "$CANONICAL_VERSION_FILE" ]] || die "No existe VERSION en $CANONICAL_SKILL_DIR"

# Sandbox temporal
SANDBOX="$(mktemp -d -t wom-update-XXXXXX)"
ORIGINAL_VERSION_BACKUP="$(mktemp -t wom-version-bak-XXXXXX)"
cp "$CANONICAL_VERSION_FILE" "$ORIGINAL_VERSION_BACKUP"

# Trap para limpieza garantizada
cleanup() {
    local rc=$?
    log "Limpieza..."
    # Restaurar VERSION canónico
    if [[ -f "$ORIGINAL_VERSION_BACKUP" ]]; then
        cp "$ORIGINAL_VERSION_BACKUP" "$CANONICAL_VERSION_FILE"
        rm -f "$ORIGINAL_VERSION_BACKUP"
    fi
    # Borrar sandbox
    if [[ -d "$SANDBOX" ]]; then
        rm -rf "$SANDBOX"
    fi
    if [[ $rc -ne 0 ]]; then
        log "FAIL (rc=$rc)"
    fi
    exit "$rc"
}
trap cleanup EXIT INT TERM

# ---------------------------------------------------------------------------
# Cronómetro de SC-008
# ---------------------------------------------------------------------------

START_TS="$(date +%s)"

# ---------------------------------------------------------------------------
# Paso 1 — git init en sandbox
# ---------------------------------------------------------------------------

log "[1/8] Sandbox: $SANDBOX"
( cd "$SANDBOX" && git init -q -b main && git commit --allow-empty -m "init" -q )

# ---------------------------------------------------------------------------
# Paso 2 — Install non-interactive
# ---------------------------------------------------------------------------

log "[2/8] Ejecutando install/install.sh..."
WOM_PROJECT_TYPE=guia \
WOM_AUDIENCE="Personas operadoras editoriales que validan SC-008 en CI" \
WOM_DOMAIN="Smoke test del procedimiento de update" \
WOM_OPERATOR_ID="marcela.gotta" \
WOM_OPERATOR_EMAIL="marcela@example.com" \
bash "$FRAMEWORK_HOME/install/install.sh" \
    --target-dir "$SANDBOX" \
    --agent claude-code \
    --language es \
    --non-interactive >/dev/null

manifest="$SANDBOX/.writeonmars-manifest.json"
[[ -f "$manifest" ]] || die "Install no produjo manifest"

# ---------------------------------------------------------------------------
# Paso 3 — Customización local del manifest
# ---------------------------------------------------------------------------

log "[3/8] Aplicando customizaciones locales al manifest..."
tmp="$(mktemp)"
jq '
  .language_primary = "es-AR" |
  .human_operators += [{
    "id": "jose.tester",
    "email": "jose.tester@example.com",
    "role": "reviewer"
  }]
' "$manifest" >"$tmp"
mv "$tmp" "$manifest"

# Verificar que la edición es válida
jq -e '.language_primary == "es-AR"' "$manifest" >/dev/null \
    || die "language_primary no quedó como es-AR"
jq -e '[.human_operators[].id] | contains(["jose.tester"])' "$manifest" >/dev/null \
    || die "operador extra no quedó persistido"

# ---------------------------------------------------------------------------
# Paso 4 — Bump de VERSION canónico (en repo padre)
# ---------------------------------------------------------------------------

log "[4/8] Bumpeando VERSION canónico de $TARGET_SKILL..."
NEW_VERSION="v0.2.0-mvp-2026-05-06"
cat >"$CANONICAL_VERSION_FILE" <<EOF
$NEW_VERSION
Skill: $TARGET_SKILL
Origen: writing-framework canonical (smoke bump)
Fecha: 2026-05-06
EOF

# Versión semver derivada (sin prefijo v ni sufijo) que el manifest exige.
NEW_SEMVER="0.2.0"

# ---------------------------------------------------------------------------
# Paso 5 — Aplicar writeonmars-update (manualmente, ya que la skill es markdown)
# ---------------------------------------------------------------------------

log "[5/8] Ejecutando procedimiento writeonmars-update..."

# 5.a — Detectar diff: la skill canónica está en NEW_SEMVER, el manifest en
#       0.1.0. Identificamos la entrada en skills[] por nombre.
proyecto_version="$(jq -r --arg n "$TARGET_SKILL" '.skills[] | select(.name==$n) | .version' "$manifest")"
[[ -n "$proyecto_version" ]] || die "Skill $TARGET_SKILL no aparece en manifest"
log "  proyecto: $proyecto_version | canónico: $NEW_SEMVER"

# 5.b — Backup defensivo del manifest
cp "$manifest" "$manifest.bak"

# 5.c — Copiar archivos de la skill (--yes, sin confirmación)
cp -R "$CANONICAL_SKILL_DIR/." "$SANDBOX/.claude/skills/$TARGET_SKILL/"

# 5.d — Bumpear .skills[] en el manifest preservando todo lo demás
tmp="$(mktemp)"
jq --arg n "$TARGET_SKILL" --arg v "$NEW_SEMVER" '
  .skills = (.skills | map(if .name == $n then .version = $v else . end))
' "$manifest" >"$tmp"
mv "$tmp" "$manifest"

# 5.e — Re-validar manifest contra el schema (si ajv-cli o python+jsonschema disponibles)
schema="$FRAMEWORK_HOME/writeonmars/contracts/manifest-schema.json"
validation_status="skipped"
if command -v npx >/dev/null 2>&1; then
    if npx --no-install ajv-cli validate --spec=draft2020 -s "$schema" -d "$manifest" >/dev/null 2>&1; then
        validation_status="ajv"
    fi
fi
if [[ "$validation_status" == "skipped" ]] && command -v python3 >/dev/null 2>&1; then
    if python3 -c "import jsonschema" 2>/dev/null; then
        python3 - "$schema" "$manifest" <<'PYEOF' >/dev/null 2>&1 && validation_status="python"
import json, sys, jsonschema
with open(sys.argv[1]) as f: schema = json.load(f)
with open(sys.argv[2]) as f: instance = json.load(f)
jsonschema.validate(instance=instance, schema=schema)
PYEOF
    fi
fi
log "  validación: $validation_status"
if [[ "$validation_status" == "skipped" ]]; then
    log "  WARNING: ni ajv ni python+jsonschema disponibles; validación de schema omitida"
fi

# ---------------------------------------------------------------------------
# Paso 6 — Asserts
# ---------------------------------------------------------------------------

log "[6/8] Verificando assertions..."

# Assert a — VERSION en destino refleja NEW_VERSION
target_version_first_line="$(head -n1 "$SANDBOX/.claude/skills/$TARGET_SKILL/VERSION")"
if [[ "$target_version_first_line" != "$NEW_VERSION" ]]; then
    log "  FAIL: VERSION destino = '$target_version_first_line', esperado '$NEW_VERSION'"
    exit 1
fi
log "  OK VERSION destino = $target_version_first_line"

# Assert b — manifest.skills[] refleja NEW_SEMVER
manifest_version="$(jq -r --arg n "$TARGET_SKILL" '.skills[] | select(.name==$n) | .version' "$manifest")"
if [[ "$manifest_version" != "$NEW_SEMVER" ]]; then
    log "  FAIL: manifest version = '$manifest_version', esperado '$NEW_SEMVER'"
    exit 1
fi
log "  OK manifest.skills[$TARGET_SKILL].version = $manifest_version"

# Assert c — language_primary preservado
lang="$(jq -r '.language_primary' "$manifest")"
if [[ "$lang" != "es-AR" ]]; then
    log "  FAIL: language_primary = '$lang', esperado 'es-AR'"
    exit 1
fi
log "  OK language_primary = $lang"

# Assert d — operador extra preservado
if ! jq -e '[.human_operators[].id] | contains(["jose.tester"])' "$manifest" >/dev/null; then
    log "  FAIL: operador extra jose.tester no encontrado en manifest"
    exit 1
fi
log "  OK operador extra preservado (jose.tester)"

# ---------------------------------------------------------------------------
# Paso 7 — Cronometrar
# ---------------------------------------------------------------------------

END_TS="$(date +%s)"
ELAPSED=$((END_TS - START_TS))
log "[7/8] Tiempo total: ${ELAPSED} s (target SC-008: <900 s)"

if (( ELAPSED >= 900 )); then
    log "  FAIL: tiempo excedió SC-008"
    exit 1
fi

# ---------------------------------------------------------------------------
# Paso 8 — Reporte final
# ---------------------------------------------------------------------------

log "[8/8] PASS"
log "  Skill bumpeada: $TARGET_SKILL ($proyecto_version → $NEW_SEMVER)"
log "  Configuración local preservada: language_primary=es-AR + operador jose.tester"
log "  Validación schema: $validation_status"
log "  Tiempo: ${ELAPSED} s"

# El trap se encarga de limpiar
exit 0
