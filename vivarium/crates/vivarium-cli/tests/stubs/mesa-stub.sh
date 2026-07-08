#!/usr/bin/env bash
set -euo pipefail

prompt="${1:?prompt_file}"
project="$(awk -F': ' '/^project_dir:/ {print $2}' "$prompt")"
step="$(awk -F': ' '/^step:/ {print $2}' "$prompt")"
chapter="$(awk -F': ' '/^chapter:/ {print $2}' "$prompt")"
spec="$(find "$project/specs" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1)"
mkdir -p "$spec"
findings="$spec/findings.md"
[[ -f "$findings" ]] || printf '# Findings\n\n' > "$findings"

pass="${step#review-}"
if [[ "$pass" == "5" ]]; then
  caps="global"
else
  caps="[$chapter]"
fi

cat >> "$findings" <<EOF

## Pasada $pass - Stub

<!-- pass-output-schema: v1.1 -->

**Estado pasada**: passed
**Capítulos cubiertos**: $caps
**Firma**:
  - tipo: autonomous
  - actor: mesa-stub

### Hallazgos

| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |
|----|----------|-----------|-------|----------|-------------|--------|-------|
EOF
