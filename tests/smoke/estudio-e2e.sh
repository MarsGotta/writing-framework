#!/usr/bin/env bash
# Smoke e2e del modo estudio: Vivarium + preset + stubs deterministas.

set -euo pipefail

if ! command -v cargo >/dev/null 2>&1; then
  echo "skip: cargo no disponible"
  exit 99
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/estudio-e2e.XXXXXX")"
PROJECT="$TMP/estudio"
STUBS="$TMP/stubs"
mkdir -p "$STUBS"

cleanup() {
  rm -rf "$TMP"
}
trap cleanup EXIT

cargo build --manifest-path "$REPO_ROOT/vivarium/Cargo.toml" -p vivarium-cli
VIVARIUM="$REPO_ROOT/vivarium/target/debug/vivarium"

"$VIVARIUM" new "$PROJECT" --kind guia --preset "$REPO_ROOT/writeonmars" --operator smoke --email smoke@example.com
git -C "$PROJECT" config user.name "Smoke Human"
git -C "$PROJECT" config user.email "smoke@example.com"

python3 - "$PROJECT/.writeonmars-manifest.json" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
data = json.loads(p.read_text(encoding="utf-8"))
data["mode"] = "estudio"
data["sector"] = "tecnologia"
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

mkdir -p "$PROJECT/specs/001-estudio"
cat > "$PROJECT/specs/001-estudio/spec.md" <<'EOF'
# Feature Specification: Estudio smoke

Brief firmado por la humana.
EOF
cat > "$PROJECT/specs/001-estudio/research.md" <<'EOF'
# Research

Fuentes del proyecto.
EOF
cat > "$PROJECT/specs/001-estudio/plan.md" <<'EOF'
# Plan

## Temario

| # | Titulo | Promesa |
|---|--------|---------|
| 1 | Uno humano | Validar estudio |
| 2 | Dos humano | Cubrir SC-002 con dos capítulos |
EOF

cat > "$STUBS/review-stub.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
prompt="${1:?prompt_file}"
project="$(awk -F': ' '/^project_dir:/ {print $2}' "$prompt")"
step="$(awk -F': ' '/^step:/ {print $2}' "$prompt")"
chapter="$(awk -F': ' '/^chapter:/ {print $2}' "$prompt")"
spec="$(find "$project/specs" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1)"
findings="$spec/findings.md"
mkdir -p "$spec"
[[ -f "$findings" ]] || printf '# Findings\n\n' > "$findings"
pass="${step#review-}"
if [[ "$pass" == "5" ]]; then
  caps="global"
  key="global"
  hash="$(python3 - "$project/chapters" <<'PY'
import hashlib, sys
from pathlib import Path
hashes = []
for p in sorted(Path(sys.argv[1]).glob("*.md")):
    hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
print(hashlib.sha256("".join(hashes).encode()).hexdigest())
PY
)"
else
  caps="[$chapter]"
  key="$chapter"
  hash="$(python3 - "$project/chapters" "$chapter" <<'PY'
import hashlib, sys
from pathlib import Path
chapter = int(sys.argv[2])
for p in sorted(Path(sys.argv[1]).glob("*.md")):
    if p.name.startswith(f"{chapter:03}") or p.name.startswith(f"{chapter:02}") or p.name.startswith(str(chapter)):
        print(hashlib.sha256(p.read_bytes()).hexdigest())
        break
PY
)"
fi
# Un único hallazgo accionable, en la pasada 1 del capítulo 1: ejercita el
# checkpoint dispose exactamente una vez. El capítulo 2 sale limpio.
row=""
if [[ "$pass" == "1" && "$chapter" == "1" ]]; then
  row="| F-1.1 | $chapter | medio | frase | problema | propuesta | abierto | [] |"
fi
cat >> "$findings" <<EOF

## Pasada $pass - Stub

<!-- pass-output-schema: v1.2 -->

**Estado pasada**: passed
**Capítulos cubiertos**: $caps
**Firma**:
  - tipo: autonomous
  - actor: estudio-stub

### Hallazgos

| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |
|----|----------|-----------|-------|----------|-------------|--------|-------|
$row

<!-- huellas: {"$key": "$hash"} -->
EOF
SH
chmod +x "$STUBS/review-stub.sh"

cat > "$PROJECT/.vivarium/config.toml" <<EOF
version = 1
[roles.redactora]
command = ["$STUBS/review-stub.sh", "{prompt_file}"]
[roles.editora_mesa]
command = ["$STUBS/review-stub.sh", "{prompt_file}"]
[roles.documentalista]
command = ["$STUBS/review-stub.sh", "{prompt_file}"]
EOF

cat > "$PROJECT/.specify/presets/writeonmars/scripts/export.py" <<'PY'
from pathlib import Path
Path("estudio.pdf").write_bytes(b"%PDF-1.4\n")
PY

set +e
"$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 10 ]]; then
  echo "FAIL: primer run esperaba checkpoint write (10), obtuvo $rc" >&2
  exit 1
fi
grep -q '"step":"write"' "$PROJECT/decisions.jsonl"
if grep -q '"event":"dispatch","step":"implement"' "$PROJECT/decisions.jsonl"; then
  echo "FAIL: estudio despachó implement" >&2
  exit 1
fi

# La humana escribe LOS DOS capítulos pendientes que nombró el checkpoint write.
mkdir -p "$PROJECT/chapters"
cp "$REPO_ROOT/tests/fixtures/005-estudio/chapters/001-uno-humano.md" "$PROJECT/chapters/001-uno-humano.md"
cat > "$PROJECT/chapters/002-dos-humano.md" <<'EOF'
# Dos humano

Texto humano del capítulo dos.

## Fuentes

- Fuente B
EOF
git -C "$PROJECT" add chapters/001-uno-humano.md chapters/002-dos-humano.md
git -C "$PROJECT" commit -m "human writes chapters 1 and 2" >/dev/null

set +e
"$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 10 ]]; then
  echo "FAIL: segundo run esperaba checkpoint dispose (10), obtuvo $rc" >&2
  exit 1
fi
grep -q '"step":"dispose"' "$PROJECT/decisions.jsonl"

python3 "$PROJECT/.specify/presets/writeonmars/scripts/dispose.py" F-1.1 --aplazar --project-dir "$PROJECT"

set +e
"$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 10 ]]; then
  echo "FAIL: tercer run esperaba checkpoint intro/feedback (10), obtuvo $rc" >&2
  exit 1
fi
grep -q '"step":"intro"' "$PROJECT/decisions.jsonl"
if grep -q '"event":"dispatch","step":"intro"' "$PROJECT/decisions.jsonl"; then
  echo "FAIL: estudio despachó intro" >&2
  exit 1
fi

cat > "$PROJECT/README.md" <<'EOF'
# Presentación humana

Texto escrito por la humana.
EOF

set +e
"$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 10 ]]; then
  echo "FAIL: cuarto run esperaba checkpoint feedback (10), obtuvo $rc" >&2
  exit 1
fi

cat > "$PROJECT/specs/001-estudio/feedback.md" <<'EOF'
# Feedback

Visto bueno humano.
EOF
# close.py REAL (no stub): ejercita el gate real. Solo export.py está stubeado
# (PDF falso) para no exigir pandoc/chrome en CI.
set +e
"$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 0 ]]; then
  echo "FAIL: cierre esperaba exit 0, obtuvo $rc" >&2
  exit 1
fi
# FR-007: el hallazgo aplazado se enumera como deuda declarada. El runner traga
# el stdout del sidecar, así que se comprueba invocando close.py directamente
# (mismo script del preset, --no-export para no repetir el PDF).
debt="$(python3 "$PROJECT/.specify/presets/writeonmars/scripts/close.py" \
  --project-dir "$PROJECT" --no-export 2>&1)"
if ! printf '%s' "$debt" | grep -q "Deuda declarada"; then
  echo "FAIL: close no enumeró la deuda declarada (F-1.1 aplazado)" >&2
  printf '%s\n' "$debt" >&2
  exit 1
fi

python3 "$PROJECT/.specify/presets/writeonmars/scripts/authorship.py" --project-dir "$PROJECT" --json > "$TMP/authorship.json"
python3 - "$PROJECT/decisions.jsonl" "$TMP/authorship.json" <<'PY'
import json, sys
from pathlib import Path
records = [json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if line.strip()]
bad = [r for r in records if r.get("event") == "dispatch" and r.get("step") in {"implement", "revise", "intro"}]
if bad:
    raise SystemExit(f"dispatch prohibido en estudio: {bad}")
checkpoints = [r.get("step") for r in records if r.get("event") == "checkpoint"]
if checkpoints.count("write") != 1 or checkpoints.count("dispose") != 1:
    raise SystemExit(f"checkpoints inesperados: {checkpoints}")
report = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
if report.get("veredicto_global") != "autoria_humana_demostrada":
    raise SystemExit(report)
PY

# Idempotencia (SC-002 / quickstart §5.6): un segundo run sobre el proyecto
# cerrado no despacha nada nuevo — decisions.jsonl no crece.
before="$(wc -l < "$PROJECT/decisions.jsonl")"
set +e
"$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 0 ]]; then
  echo "FAIL: segundo cierre esperaba exit 0, obtuvo $rc" >&2
  exit 1
fi
after="$(wc -l < "$PROJECT/decisions.jsonl")"
if [[ "$before" -ne "$after" ]]; then
  echo "FAIL: el re-run sobre proyecto cerrado añadió despachos ($before → $after)" >&2
  exit 1
fi

echo "PASS estudio-e2e"
