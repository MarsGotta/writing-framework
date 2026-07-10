#!/usr/bin/env bash
# Smoke e2e de la pista corta (feature 006): Vivarium + preset + stubs
# deterministas DISTINGUIBLES POR ROL. Espejo de estudio-e2e.sh.
#
# Qué mide (quickstart § 6):
#   - Camino feliz de una pieza única en corta+produccion: <= 8 despachos
#     (SC-001), esperado 6 (research, implement, review-1, review-4, export,
#     close). Cero despachos de plan/constitution/review-2/3/5/intro.
#   - voz != precisión: review-1 lo vehicula editora_mesa (combinada 1·2·3·5),
#     review-4 la documentalista (precisión 4 + claims.md) — roles distintos.
#   - Recorrido en mode: estudio: checkpoints write/dispose/feedback (exit 10),
#     jamás implement/revise/intro, sin checkpoint intro (R6).
#   - Escalado del proyecto cerrado: solo cambia el manifiesto.
#
# NOTA sobre decisions.jsonl: decisions.rs lo escribe en la RAÍZ del proyecto
# ("decisions.jsonl"), no en ".vivarium/". Este smoke lee la ruta real.
#
# Portable a Bash 3.2 (el /bin/bash de macOS): sin arrays asociativos.
# Convención de exit codes: 0 = PASS, 99 = SKIP (sin cargo), otro = FAIL.
# Solo export.py está stubeado (PDF falso): así el despacho `export` cuenta sin
# exigir pandoc/Chrome en CI. status.py, close.py, dispose.py y track.py son
# los reales del preset — el smoke ejercita los gates de verdad.

set -euo pipefail

if ! command -v cargo >/dev/null 2>&1; then
  echo "skip: cargo no disponible"
  exit 99
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/corta-e2e.XXXXXX")"
STUBS="$TMP/stubs"
mkdir -p "$STUBS"

cleanup() {
  rm -rf "$TMP"
}
trap cleanup EXIT

cargo build --manifest-path "$REPO_ROOT/vivarium/Cargo.toml" -p vivarium-cli
VIVARIUM="$REPO_ROOT/vivarium/target/debug/vivarium"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

# Ejecuta `vivarium run` y comprueba el exit code esperado (10 = checkpoint,
# 11 = guardarraíl de modo, 0 = progreso/cierre).
run_expect() {
  local project="$1" want="$2" label="$3" rc=0
  set +e
  "$VIVARIUM" run --project "$project"
  rc=$?
  set -e
  [[ "$rc" -eq "$want" ]] || fail "$label: esperaba exit $want, obtuvo $rc"
}

# --------------------------------------------------------------------------- #
# Stubs deterministas, DISTINGUIBLES POR ROL. Cada uno lee `step:` del fichero
# de tarea que Vivarium le pasa (dispatch.rs::write_task_file).
# --------------------------------------------------------------------------- #

# Redactora: redacta el capítulo único (solo se despacha en produccion).
cat > "$STUBS/redactora-stub.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
prompt="${1:?prompt_file}"
project="$(awk -F': ' '/^project_dir:/ {print $2}' "$prompt")"
step="$(awk -F': ' '/^step:/ {print $2}' "$prompt")"
case "$step" in
  implement)
    mkdir -p "$project/chapters"
    cat > "$project/chapters/01-la-pieza.md" <<'EOF'
# La pieza

Capítulo único de una pieza en pista corta. El temario degenerado tiene una
sola fila y esta pieza la materializa.

## Fuentes

- Fuente única del ejemplo
EOF
    ;;
  *)
    echo "redactora-stub: step no soportado en corta: $step" >&2
    exit 2
    ;;
esac
SH

# Editora de mesa: vehicula la PASADA COMBINADA. Un único run (review-1)
# registra los bloques 1·2·3 (Capítulos cubiertos: 1) y 5 (global), cada uno con
# su huella sha256 correcta. En estudio emite además UN hallazgo accionable en la
# pasada 1 para ejercitar el checkpoint dispose. Las pasadas 2/3/5 sueltas quedan
# como red de reparación (FR-006), nunca despachadas en el camino feliz.
cat > "$STUBS/mesa-combinada.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
prompt="${1:?prompt_file}"
project="$(awk -F': ' '/^project_dir:/ {print $2}' "$prompt")"
step="$(awk -F': ' '/^step:/ {print $2}' "$prompt")"
spec="$(find "$project/specs" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1)"
mkdir -p "$spec"
findings="$spec/findings.md"
[[ -f "$findings" ]] || printf '# Findings\n\n' > "$findings"

mode="$(python3 -c "import json,sys;print((json.load(open(sys.argv[1])).get('mode') or 'produccion'))" "$project/.writeonmars-manifest.json")"

# Huella por capítulo (sha256 de los bytes del capítulo 1).
chash="$(python3 - "$project/chapters" <<'PY'
import hashlib, re, sys
from pathlib import Path
for p in sorted(Path(sys.argv[1]).glob("*.md")):
    m = re.match(r"\s*(\d+)", p.name)
    if m and int(m.group(1)) == 1:
        print(hashlib.sha256(p.read_bytes()).hexdigest()); break
PY
)"
# Huella global de la pasada 5: sha256(concat de los hexdigests por capítulo).
ghash="$(python3 - "$project/chapters" <<'PY'
import hashlib, sys
from pathlib import Path
hs = [hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(sys.argv[1]).glob("*.md"))]
print(hashlib.sha256("".join(hs).encode()).hexdigest())
PY
)"

emit() {  # $1 num  $2 nombre  $3 caps  $4 huella-json  $5 filas-hallazgo (opcional)
  local num="$1" nombre="$2" caps="$3" huella="$4" filas="${5:-}"
  cat >> "$findings" <<EOF

## Pasada $num — $nombre

<!-- pass-output-schema: v1.2 -->

**Estado pasada**: passed
**Capítulos cubiertos**: $caps
**Firma**:
  - tipo: autonomous
  - actor: editora-mesa-stub

### Hallazgos

| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |
|----|----------|-----------|-------|----------|-------------|--------|-------|
$filas

<!-- huellas: $huella -->
EOF
}

row1=""
if [[ "$mode" == "estudio" ]]; then
  row1='| F-1.1 | 1 | medio | frase | problema | propuesta | abierto | [] |'
fi

case "$step" in
  review-1)
    emit 1 "Estructura"  1      "{\"1\": \"$chash\"}"         "$row1"
    emit 2 "Utilidad"    1      "{\"1\": \"$chash\"}"         ""
    emit 3 "Naturalidad" 1      "{\"1\": \"$chash\"}"         ""
    emit 5 "Formato"     global "{\"global\": \"$ghash\"}"    ""
    ;;
  review-2) emit 2 "Utilidad"    1      "{\"1\": \"$chash\"}"      "" ;;
  review-3) emit 3 "Naturalidad" 1      "{\"1\": \"$chash\"}"      "" ;;
  review-5) emit 5 "Formato"     global "{\"global\": \"$ghash\"}" "" ;;
  *)
    echo "mesa-combinada: step no soportado: $step" >&2
    exit 2
    ;;
esac
SH

# Documentalista: research exprés + PASADA DE PRECISIÓN (dimensión 4, relevo
# aparte + claims.md). Nunca escribe prosa del manuscrito.
cat > "$STUBS/doc-precision.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
prompt="${1:?prompt_file}"
project="$(awk -F': ' '/^project_dir:/ {print $2}' "$prompt")"
step="$(awk -F': ' '/^step:/ {print $2}' "$prompt")"
spec="$(find "$project/specs" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1)"
mkdir -p "$spec"

case "$step" in
  research)
    cat > "$spec/research.md" <<'EOF'
# Research exprés (pista corta)

Conceptos obligatorios del brief, sin panorama ni estado del arte. Una cita por
concepto (contrato de citación íntegro).
EOF
    ;;
  review-4)
    findings="$spec/findings.md"
    [[ -f "$findings" ]] || printf '# Findings\n\n' > "$findings"
    chash="$(python3 - "$project/chapters" <<'PY'
import hashlib, re, sys
from pathlib import Path
for p in sorted(Path(sys.argv[1]).glob("*.md")):
    m = re.match(r"\s*(\d+)", p.name)
    if m and int(m.group(1)) == 1:
        print(hashlib.sha256(p.read_bytes()).hexdigest()); break
PY
)"
    cat >> "$findings" <<EOF

## Pasada 4 — Precisión

<!-- pass-output-schema: v1.2 -->

**Estado pasada**: passed
**Capítulos cubiertos**: 1
**Firma**:
  - tipo: autonomous
  - actor: documentalista-stub

### Hallazgos

| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |
|----|----------|-----------|-------|----------|-------------|--------|-------|

<!-- huellas: {"1": "$chash"} -->
EOF
    cat > "$spec/claims.md" <<'EOF'
<!-- claim-record-schema: v1.0 -->
<!-- pass-output-schema: v1.1 -->

## Claims — Capítulo 1

```json
[]
```
EOF
    ;;
  *)
    echo "doc-precision: step no soportado en corta: $step" >&2
    exit 2
    ;;
esac
SH

chmod +x "$STUBS/redactora-stub.sh" "$STUBS/mesa-combinada.sh" "$STUBS/doc-precision.sh"

# Config BYOM: roles.editora_mesa y roles.documentalista a stubs DISTINTOS
# (voz != precisión estructural). export.py stubeado (PDF falso).
write_project_config() {
  local project="$1"
  cat > "$project/.vivarium/config.toml" <<EOF
version = 1
[roles.redactora]
command = ["$STUBS/redactora-stub.sh", "{prompt_file}"]
[roles.editora_mesa]
command = ["$STUBS/mesa-combinada.sh", "{prompt_file}"]
[roles.documentalista]
command = ["$STUBS/doc-precision.sh", "{prompt_file}"]
EOF
  cat > "$project/.specify/presets/writeonmars/scripts/export.py" <<'PY'
from pathlib import Path
Path("corta.pdf").write_bytes(b"%PDF-1.4\n")
PY
}

write_brief() {  # spec.md + plan.md (temario de UNA fila). NO research (se despacha).
  local project="$1" spec="$1/specs/001-mi-pieza"
  mkdir -p "$spec"
  cat > "$spec/spec.md" <<'EOF'
# Feature Specification: Mi pieza (pista corta)

Brief compacto de una pieza única, firmado en una sola ronda (checkpoint humano 1).

- **Título**: La pieza
- **Promesa**: Explicar la pista corta en una sola pieza

**Firma del brief**: smoke · 2026-07-10
EOF
  cat > "$spec/plan.md" <<'EOF'
# Plan

## Temario

| Número | Título | Promesa | Estructura aplicada |
|--------|--------|---------|---------------------|
| 1 | La pieza | Explicar la pista corta en una sola pieza | didactica_v1 |
EOF
}

# =========================================================================== #
# 1. PRODUCCIÓN — camino feliz, <= 8 despachos (esperado 6)
# =========================================================================== #
PROJECT="$TMP/corta-prod"
WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia \
  "$VIVARIUM" new "$PROJECT" --kind guia --preset "$REPO_ROOT/writeonmars" \
    --operator smoke --email smoke@example.com
git -C "$PROJECT" config user.name "Smoke Human"
git -C "$PROJECT" config user.email "smoke@example.com"

# 1a. Manifiesto: track/sector/registro. Constitución: centinela + POR REFERENCIA.
python3 - "$PROJECT/.writeonmars-manifest.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
assert m["track"] == "corta", m.get("track")
assert m["sector"] == "tecnologia", m.get("sector")
assert m["registro"] == "tecnico-divulgativo", m.get("registro")
print("OK manifiesto: track=corta sector=tecnologia registro=tecnico-divulgativo")
PY
grep -q "WRITEONMARS:ADENDAS" "$PROJECT/.specify/memory/constitution.md" \
  || fail "la constitución del proyecto no trae el centinela WRITEONMARS:ADENDAS"
grep -q "POR REFERENCIA" "$PROJECT/.specify/memory/constitution.md" \
  || fail "la constitución del proyecto no trae la cadena POR REFERENCIA"

write_project_config "$PROJECT"

# 1b. run → checkpoint specify (exit 10). No hay despacho de setup (bootstrap
# corrió en `vivarium new`) ni de constitution (sector ya fijado).
run_expect "$PROJECT" 10 "prod run1 (checkpoint specify)"
grep -q '"step":"specify"' "$PROJECT/decisions.jsonl" || fail "prod: no hubo checkpoint specify"

# 1c. La operadora firma el brief y materializa el temario de una fila.
write_brief "$PROJECT"

# 1d. run → despacha research, implement, review-1 (combinada), review-4
# (precisión), export; se detiene en el checkpoint feedback (exit 10).
run_expect "$PROJECT" 10 "prod run2 (checkpoint feedback)"
grep -q '"step":"feedback"' "$PROJECT/decisions.jsonl" || fail "prod: no hubo checkpoint feedback"
test -f "$PROJECT/corta.pdf" || fail "prod: no se generó el PDF"
[[ ! -f "$PROJECT/README.md" ]] || fail "prod: la pista corta NO debe generar README.md"

# 1e. Nunca se despacharon los pasos omitidos por la ceremonia corta.
for step in plan constitution review-2 review-3 review-5 intro; do
  if grep -q "\"event\":\"dispatch\",\"step\":\"$step\"" "$PROJECT/decisions.jsonl"; then
    fail "prod: se despachó '$step' (prohibido en pista corta)"
  fi
done

# 1f. feedback_intake.py deja feedback.md → run → close (exit 0).
# (Se escribe feedback.md directamente, como en estudio-e2e: feedback_intake.py
# exige un PDF anotado real con pymupdf, indisponible en CI.)
cat > "$PROJECT/specs/001-mi-pieza/feedback.md" <<'EOF'
# Feedback — PDF anotado

Sin observaciones; visto bueno de la operadora.
EOF
run_expect "$PROJECT" 0 "prod run3 (close)"

# 1g. Recuento de despachos (SC-001): <= 8, esperado 6, roles distintos.
PROJECT="$PROJECT" python3 - <<'PY'
import json, os
path = os.path.join(os.environ["PROJECT"], "decisions.jsonl")
disp = []
for line in open(path):
    line = line.strip()
    if not line:
        continue
    rec = json.loads(line)
    if rec.get("event") == "dispatch":
        disp.append(rec)
steps = [d.get("step") for d in disp]
n = len(steps)
print(f"despachos ({n}):", steps)
assert n <= 8, f"{n} despachos, SC-001 exige <= 8"
prohibidos = {"plan", "constitution", "review-2", "review-3", "review-5", "intro"}
bad = [s for s in steps if s in prohibidos]
assert not bad, f"despachos prohibidos: {bad}"
role = {}
for d in disp:
    role.setdefault(d.get("step"), d.get("role"))
assert role.get("review-1") == "editora_mesa", ("review-1 rol", role.get("review-1"))
assert role.get("review-4") == "documentalista", ("review-4 rol", role.get("review-4"))
assert n == 6, f"esperaba 6 despachos (research/implement/review-1/review-4/export/close), hubo {n}: {steps}"
print(f"OK {n} despachos; voz != precisión: review-1=editora_mesa review-4=documentalista")
PY

# 1h. Idempotencia: un segundo run sobre el proyecto cerrado no despacha nada.
before="$(wc -l < "$PROJECT/decisions.jsonl")"
run_expect "$PROJECT" 0 "prod run4 (idempotencia)"
after="$(wc -l < "$PROJECT/decisions.jsonl")"
[[ "$before" -eq "$after" ]] || fail "prod: el re-run añadió despachos ($before → $after)"

# =========================================================================== #
# 2. ESTUDIO — checkpoints write/dispose/feedback, jamás manuscrito, sin intro
# =========================================================================== #
PE="$TMP/corta-estudio"
WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia \
  "$VIVARIUM" new "$PE" --kind guia --preset "$REPO_ROOT/writeonmars" \
    --operator smoke --email smoke@example.com
git -C "$PE" config user.name "Smoke Human"
git -C "$PE" config user.email "smoke@example.com"
python3 - "$PE/.writeonmars-manifest.json" <<'PY'
import json, sys
p = sys.argv[1]
m = json.load(open(p))
m["mode"] = "estudio"
open(p, "w").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
PY
write_project_config "$PE"

# 2a. run → checkpoint specify. La humana firma el brief.
run_expect "$PE" 10 "estudio run1 (checkpoint specify)"
grep -q '"step":"specify"' "$PE/decisions.jsonl" || fail "estudio: no hubo checkpoint specify"
write_brief "$PE"

# 2b. run → despacha research (documentalista, no es manuscrito) y se detiene en
# el checkpoint write (la humana escribe). Jamás despacha implement.
run_expect "$PE" 10 "estudio run2 (checkpoint write)"
grep -q '"step":"write"' "$PE/decisions.jsonl" || fail "estudio: no hubo checkpoint write"
if grep -q '"event":"dispatch","step":"implement"' "$PE/decisions.jsonl"; then
  fail "estudio: se despachó implement (guardarraíl de modo roto)"
fi

# 2c. La humana escribe el capítulo único.
mkdir -p "$PE/chapters"
cat > "$PE/chapters/01-la-pieza.md" <<'EOF'
# La pieza

Pieza única escrita por la humana en modo estudio.

## Fuentes

- Fuente humana
EOF

# 2d. run → despacha review-1 (combinada, solo hallazgos) y se detiene en el
# checkpoint dispose (hay un hallazgo accionable abierto).
run_expect "$PE" 10 "estudio run3 (checkpoint dispose)"
grep -q '"step":"dispose"' "$PE/decisions.jsonl" || fail "estudio: no hubo checkpoint dispose"

# 2e. La humana dispone el hallazgo (aplazar). dispose.py es el real del preset.
python3 "$PE/.specify/presets/writeonmars/scripts/dispose.py" F-1.1 --aplazar --project-dir "$PE"

# 2f. run → despacha review-4 (precisión) y export; se detiene en feedback.
# JAMÁS checkpoint intro (R6): la pieza única no tiene README de presentación.
run_expect "$PE" 10 "estudio run4 (checkpoint feedback)"
grep -q '"step":"feedback"' "$PE/decisions.jsonl" || fail "estudio: no hubo checkpoint feedback"
if grep -q '"event":"checkpoint","step":"intro"' "$PE/decisions.jsonl"; then
  fail "estudio corta: apareció un checkpoint intro (R6 roto)"
fi
[[ ! -f "$PE/README.md" ]] || fail "estudio corta: no debe generar README.md"

# 2g. feedback.md → run → close (exit 0).
cat > "$PE/specs/001-mi-pieza/feedback.md" <<'EOF'
# Feedback

Visto bueno humano.
EOF
run_expect "$PE" 0 "estudio run5 (close)"

# 2h. Invariantes globales del recorrido de estudio.
PE="$PE" python3 - <<'PY'
import json, os
recs = []
for line in open(os.path.join(os.environ["PE"], "decisions.jsonl")):
    line = line.strip()
    if line:
        recs.append(json.loads(line))
disp = [r.get("step") for r in recs if r.get("event") == "dispatch"]
cps = [r.get("step") for r in recs if r.get("event") == "checkpoint"]
print("estudio despachos:", disp)
print("estudio checkpoints:", cps)
bad = [s for s in disp if s in {"implement", "revise", "intro"}]
assert not bad, f"estudio despachó manuscrito (prohibido): {bad}"
for need in ("write", "dispose", "feedback"):
    assert need in cps, f"falta el checkpoint {need}: {cps}"
assert "intro" not in cps, f"checkpoint intro presente (R6 roto): {cps}"
print("OK estudio: checkpoints write/dispose/feedback, sin intro, sin manuscrito")
PY

# =========================================================================== #
# 3. CIERRE — escalar el proyecto cerrado: solo cambia el manifiesto
# =========================================================================== #
git -C "$PROJECT" add -A
git -C "$PROJECT" commit -q -m "artefactos de la corrida corta"
python3 "$PROJECT/.specify/presets/writeonmars/scripts/track.py" \
  --escalar --project-dir "$PROJECT" --json
python3 - "$PROJECT/.writeonmars-manifest.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
assert m["track"] == "estandar", m.get("track")
h = m["track_history"][-1]
assert h["from"] == "corta" and h["to"] == "estandar", h
assert h["actor"] and not h["actor"].endswith("@agents.writeonmars.invalid"), h
assert h["date"].endswith("Z"), h["date"]
print("OK escalado registrado: corta → estandar, actor humano, fecha UTC Z")
PY
porcelain="$(git -C "$PROJECT" status --porcelain)"
n_lines="$(printf '%s\n' "$porcelain" | grep -c . || true)"
[[ "$n_lines" -eq 1 ]] || fail "escalar tocó más que el manifiesto: [$porcelain]"
printf '%s' "$porcelain" | grep -q '\.writeonmars-manifest\.json' \
  || fail "el único cambio no es el manifiesto: [$porcelain]"
echo "OK escalado: solo cambió .writeonmars-manifest.json"

echo "PASS corta-e2e"
