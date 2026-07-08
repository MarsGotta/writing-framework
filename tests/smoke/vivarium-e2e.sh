#!/usr/bin/env bash
# Smoke e2e de Vivarium: CLI Rust + proyecto sintetico + agentes stub.

set -euo pipefail

# Exit 99 = SKIP para run-all.sh (nunca un falso PASS).
if ! command -v cargo >/dev/null 2>&1; then
  echo "skip: cargo no disponible"
  exit 99
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STUBS="$REPO_ROOT/vivarium/crates/vivarium-cli/tests/stubs"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/vivarium-e2e.XXXXXX")"
PROJECT="$TMP/guia"
export PATH="$STUBS:$PATH"

cleanup() {
  rm -rf "$TMP"
}
trap cleanup EXIT

cargo build --manifest-path "$REPO_ROOT/vivarium/Cargo.toml" -p vivarium-cli
VIVARIUM="$REPO_ROOT/vivarium/target/debug/vivarium"

"$VIVARIUM" new "$PROJECT" --kind guia --preset "$REPO_ROOT/writeonmars" --operator smoke --email smoke@example.com

mkdir -p "$PROJECT/specs/001-demo"
cat > "$PROJECT/specs/001-demo/spec.md" <<'EOF'
# Feature Specification: Demo smoke

Brief firmado para el smoke.
EOF
cat > "$PROJECT/specs/001-demo/research.md" <<'EOF'
# Research

Fuentes sinteticas.
EOF
cat > "$PROJECT/specs/001-demo/plan.md" <<'EOF'
# Plan

## Temario

| # | Titulo | Promesa |
|---|--------|---------|
| 1 | Uno | A |
| 2 | Dos | B |
| 3 | Tres | C |
EOF

cat > "$PROJECT/.vivarium/config.toml" <<EOF
version = 1
[roles.redactora]
command = ["$STUBS/redactora-stub.sh", "{prompt_file}"]
[roles.editora_mesa]
command = ["$STUBS/mesa-stub.sh", "{prompt_file}"]
[roles.documentalista]
command = ["$STUBS/doc-stub.sh", "{prompt_file}"]
EOF

cat > "$PROJECT/.specify/presets/writeonmars/scripts/export.py" <<'PY'
from pathlib import Path
Path("demo.pdf").write_bytes(b"%PDF-1.4\n")
PY

set +e
VIVARIUM_STUB_DOC_REVISE_ONCE=1 "$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 10 ]]; then
  echo "FAIL: vivarium run esperaba exit 10 (checkpoint), obtuvo $rc" >&2
  exit 1
fi

for n in 1 2 3; do
  test -f "$PROJECT/chapters/0${n}-capitulo-${n}.md"
done
test -f "$PROJECT/README.md"
test -f "$PROJECT/demo.pdf"

"$VIVARIUM" status --project "$PROJECT" --json > "$TMP/status.json"
python3 - "$PROJECT/decisions.jsonl" "$TMP/status.json" <<'PY'
import json
import sys
from pathlib import Path

decisions = [
    json.loads(line)
    for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
    if line.strip()
]
dispatches = [
    (d.get("step"), d.get("chapter") or "global")
    for d in decisions
    if d.get("event") == "dispatch"
]
dupes = sorted({x for x in dispatches if dispatches.count(x) > 1})
if dupes:
    raise SystemExit(f"dispatch duplicado: {dupes}")
status = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
if not status.get("all_chapters_approved"):
    raise SystemExit("all_chapters_approved no esta en true")
PY

# Checkpoint 2: la operadora anota el PDF y feedback_intake.py deja feedback.md.
# Simulado aqui; con feedback.md presente, run debe despachar close.py y salir 0.
cat > "$PROJECT/specs/001-demo/feedback.md" <<'EOF'
# Feedback — PDF anotado

Sin observaciones; visto bueno de la operadora.
EOF

cat > "$PROJECT/.specify/presets/writeonmars/scripts/close.py" <<'PY'
print("[close] OK: proyecto cerrado (stub)")
PY

set +e
"$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 0 ]]; then
  echo "FAIL: vivarium run tras feedback esperaba exit 0 (close), obtuvo $rc" >&2
  exit 1
fi

# Idempotencia del cierre: un run posterior no re-despacha close.py.
set +e
"$VIVARIUM" run --project "$PROJECT"
rc=$?
set -e
if [[ "$rc" -ne 0 ]]; then
  echo "FAIL: run tras el cierre esperaba exit 0, obtuvo $rc" >&2
  exit 1
fi
closes=$(grep -c '"event":"dispatch","step":"close"' "$PROJECT/decisions.jsonl" || true)
if [[ "$closes" -ne 1 ]]; then
  echo "FAIL: esperaba exactamente 1 dispatch de close, hubo $closes" >&2
  exit 1
fi

echo "PASS vivarium-e2e"
