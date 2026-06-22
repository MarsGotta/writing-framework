#!/usr/bin/env bash
# test-factuality.sh — smoke test del índice de factualidad y el gate g4 (feature 003).
#
# Cubre: FR-010..FR-013, FR-020, SC-002, SC-003, SC-005, SC-006.
#
# Asserts (sobre fixtures en tests/fixtures/003-factualidad/):
#   a) Retrocompat sin quality_gates (SC-003): gates.factuality=null, closeable=g1·g2·g3,
#      campos nuevos presentes pero inertes salvo la medición.
#   b) Índice determinista 8/10 = 0.8 (SC-002); cap 3 sin claims = 'no medido' (no 0).
#   c) Blocking bajo umbral (0.9): gates.factuality=false, closeable=false, --gate exit 1,
#      warning de inconsistencia (revise_pending==0).
#   d) Advisory bajo umbral: g4=false pero closeable=true, --gate exit 0.
#   e) Blocking sobre umbral (0.7): g4=true, closeable=true.
#   f) SC-006: menciona-en-dato-duro deja de contar como soportada → 0.8 < naive(tiene_cita/total)=1.0.
#   g) validate-claim.sh: acepta válido; rechaza 'apoya' sin fragmento y verificado_en_vivo sin url.

set -euo pipefail

FRAMEWORK_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_NAME="test-factuality"
STATUS="$FRAMEWORK_HOME/writeonmars/scripts/status.py"
FIX="$FRAMEWORK_HOME/tests/fixtures/003-factualidad"
VALIDATE="$FRAMEWORK_HOME/tests/lib/validate-claim.sh"

TMP="$(mktemp -d -t "writeonmars-factuality-XXXXXX")"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

fail() { printf '[%s][FAIL] %s\n' "$TEST_NAME" "$*" >&2; exit 1; }
pass() { printf '[%s][PASS] %s\n' "$TEST_NAME" "$*"; }

# Copia del proyecto fixture a un sandbox escribible.
PROJ="$TMP/project"
cp -R "$FIX/project" "$PROJ"

run_json() { python3 "$STATUS" --project-dir "$PROJ" --json; }
swap_manifest() { cp "$FIX/manifests/$1.json" "$PROJ/.writeonmars-manifest.json"; }

# --- a + b: baseline (sin quality_gates) ---------------------------------- #
run_json > "$TMP/baseline.json"
python3 - "$TMP/baseline.json" <<'PY' || fail "baseline/retrocompat (a,b)"
import json,sys
s=json.load(open(sys.argv[1]))
assert s["gates"]["factuality"] is None, "g4 debería ser null sin umbral"
assert s["factuality_global"]==0.8, ("global", s["factuality_global"])
assert s["factuality_by_chapter"].get("1")==0.8 and s["factuality_by_chapter"].get("2")==0.8
assert s["factuality_by_chapter"].get("3") is None, "cap3 debe ser null (no medido)"
assert "3" in s["factuality_unmeasured"], "cap3 debe estar en unmeasured"
# cap3 NO cuenta como 0: el global sigue 0.8 (solo cap1+cap2 en el denominador)
assert s["closeable"] is True, "g1·g2·g3 verdes → closeable sin g4"
assert s["warnings"]==[], "sin umbral no hay warnings"
print("ok baseline 0.8, cap3 no medido, closeable por g1·g2·g3")
PY
pass "a/b retrocompat + índice 8/10=0.8 + cap3 no medido (SC-002, SC-003)"

# --- f: SC-006 (menciona-dato-duro < naive) ------------------------------- #
python3 - "$PROJ/specs/001-fact/claims.md" "$TMP/baseline.json" <<'PY' || fail "SC-006"
import json,sys,re
claims=open(sys.argv[1]).read()
recs=[r for blk in re.findall(r"```json\s*(.+?)```",claims,re.S) for r in json.loads(blk)]
verif=[r for r in recs if r["soporte"] in {"soportado","parcial","sin_fuente","contradicho"}]
naive=sum(1 for r in verif if r["evidencia"])/len(verif)   # "tiene_cita/total"
ours=json.load(open(sys.argv[2]))["factuality_global"]
assert naive==1.0, ("naive", naive)
assert ours < naive, (ours, naive)
print(f"ok SC-006: naive={naive} > nuestro={ours} (menciona-dato-duro no cuenta)")
PY
pass "f SC-006: el índice baja vs tiene_cita/total"

# --- c: blocking bajo umbral (0.9) ---------------------------------------- #
swap_manifest blocking
run_json > "$TMP/blocking.json"
python3 - "$TMP/blocking.json" <<'PY' || fail "blocking (c)"
import json,sys
s=json.load(open(sys.argv[1]))
assert s["gates"]["factuality"] is False, s["gates"]["factuality"]
assert s["closeable"] is False
assert s["warnings"], "esperaba warning de inconsistencia (g4 rojo, revise_pending 0)"
print("ok blocking@0.9 → g4 false, closeable false, warning presente")
PY
if python3 "$STATUS" --project-dir "$PROJ" --gate >/dev/null 2>&1; then
    fail "blocking: --gate debería salir 1"
fi
pass "c blocking@0.9: g4 false, closeable false, --gate exit 1, warning"

# --- d: advisory bajo umbral ---------------------------------------------- #
swap_manifest advisory
run_json > "$TMP/advisory.json"
python3 - "$TMP/advisory.json" <<'PY' || fail "advisory (d)"
import json,sys
s=json.load(open(sys.argv[1]))
assert s["gates"]["factuality"] is False, "g4 informa false"
assert s["closeable"] is True, "advisory NO bloquea closeable"
assert s["factuality_mode"]=="advisory"
print("ok advisory@0.9 → g4 false, closeable true")
PY
python3 "$STATUS" --project-dir "$PROJ" --gate >/dev/null 2>&1 || fail "advisory: --gate debería salir 0"
pass "d advisory@0.9: g4 false pero closeable true, --gate exit 0"

# --- e: blocking sobre umbral (0.7) --------------------------------------- #
swap_manifest pass
run_json > "$TMP/pass.json"
python3 - "$TMP/pass.json" <<'PY' || fail "pass (e)"
import json,sys
s=json.load(open(sys.argv[1]))
assert s["gates"]["factuality"] is True, s["gates"]["factuality"]
assert s["closeable"] is True
print("ok blocking@0.7 → g4 true, closeable true")
PY
python3 "$STATUS" --project-dir "$PROJ" --gate >/dev/null 2>&1 || fail "pass: --gate debería salir 0"
pass "e blocking@0.7: g4 true, closeable true, --gate exit 0"

# --- g: validate-claim.sh (positivo + negativos) -------------------------- #
cat > "$TMP/valid.json" <<'JSON'
{"claim_id":"c1","capitulo":1,"frase":"afirmacion verificable larga de prueba","tipo_afirmacion":"afirmacion_blanda","evidencia":[{"citation_id":"s","relacion":"apoya","cita_fragmento_soporte":"la fuente lo dice"}],"soporte":"soportado","verificado_en_vivo":true,"url_verificada":"https://e.com","fecha_verificacion":"2026-06-21","pasada_schema":"1.1"}
JSON
cat > "$TMP/bad-apoya.json" <<'JSON'
{"claim_id":"c2","capitulo":1,"frase":"afirmacion verificable larga de prueba","tipo_afirmacion":"dato_duro","evidencia":[{"citation_id":"s","relacion":"apoya"}],"soporte":"soportado","verificado_en_vivo":false,"pasada_schema":"1.1"}
JSON
cat > "$TMP/bad-envivo.json" <<'JSON'
{"claim_id":"c3","capitulo":1,"frase":"afirmacion verificable larga de prueba","tipo_afirmacion":"dato_duro","evidencia":[],"soporte":"sin_fuente","verificado_en_vivo":true,"pasada_schema":"1.1"}
JSON
if ! bash "$VALIDATE" "$TMP/valid.json" >/dev/null 2>&1; then
    rc=$?; [ "$rc" -eq 2 ] && { pass "g validate-claim: sin validador instalado, salto (exit 2)"; SKIP_VALIDATE=1; } || fail "g: claim válido rechazado"
fi
if [ -z "${SKIP_VALIDATE:-}" ]; then
    bash "$VALIDATE" "$TMP/bad-apoya.json" >/dev/null 2>&1 && fail "g: 'apoya' sin fragmento debió fallar"
    bash "$VALIDATE" "$TMP/bad-envivo.json" >/dev/null 2>&1 && fail "g: verificado_en_vivo sin url/fecha debió fallar"
    pass "g validate-claim.sh: acepta válido, rechaza apoya-sin-fragmento y en_vivo-sin-url"
fi

printf '[%s] TODOS LOS ASSERTS OK\n' "$TEST_NAME"
