#!/usr/bin/env bash
set -euo pipefail

prompt="${1:?prompt_file}"
project="$(awk -F': ' '/^project_dir:/ {print $2}' "$prompt")"
step="$(awk -F': ' '/^step:/ {print $2}' "$prompt")"
chapter="$(awk -F': ' '/^chapter:/ {print $2}' "$prompt")"

latest_spec() {
  find "$project/specs" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1
}

case "$step" in
  constitution)
    python3 - "$project/.writeonmars-manifest.json" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
data = json.loads(p.read_text(encoding="utf-8"))
data["sector"] = data.get("sector") or "tecnologia"
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
    ;;
  research)
    spec="$(latest_spec)"
    cat > "$spec/research.md" <<'EOF'
# Research

Fuentes sinteticas.
EOF
    ;;
  review-4)
    spec="$(latest_spec)"
    findings="$spec/findings.md"
    [[ -f "$findings" ]] || printf '# Findings\n\n' > "$findings"
    row=""
    marker="$project/.vivarium/doc-revise-once-$chapter"
    if [[ "${VIVARIUM_STUB_DOC_REVISE_ONCE:-0}" == "1" && ! -f "$marker" ]]; then
      row="| F-4.$chapter | $chapter | medio | frase | problema | propuesta | abierto | [src] |"
      : > "$marker"
    fi
    cat >> "$findings" <<EOF

## Pasada 4 - Precision

<!-- pass-output-schema: v1.1 -->

**Estado pasada**: passed
**Capítulos cubiertos**: [$chapter]
**Firma**:
  - tipo: autonomous
  - actor: doc-stub

### Hallazgos

| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |
|----|----------|-----------|-------|----------|-------------|--------|-------|
$row
EOF
    ;;
  *)
    echo "doc-stub: step no soportado: $step" >&2
    exit 2
    ;;
esac
