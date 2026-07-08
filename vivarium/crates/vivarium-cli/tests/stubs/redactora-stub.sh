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
  plan)
    spec="$(latest_spec)"
    cat > "$spec/plan.md" <<'EOF'
# Plan

## Temario

| # | Titulo | Promesa |
|---|--------|---------|
| 1 | Uno | Primer paso |
| 2 | Dos | Segundo paso |
| 3 | Tres | Tercer paso |
EOF
    ;;
  implement)
    mkdir -p "$project/chapters"
    printf -v nn "%02d" "$chapter"
    cat > "$project/chapters/${nn}-capitulo-${chapter}.md" <<EOF
# Capitulo $chapter

Texto sintetico del capitulo $chapter.

## Fuentes
- Fuente $chapter
EOF
    ;;
  revise)
    spec="$(latest_spec)"
    if [[ -f "$spec/findings.md" ]]; then
      python3 - "$spec/findings.md" "$chapter" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
chapter = sys.argv[2]
out = []
for line in p.read_text(encoding="utf-8").splitlines():
    if line.startswith("| F-"):
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 8 and cells[1] == chapter and cells[6] == "abierto":
            cells[6] = "cerrado"
            line = "| " + " | ".join(cells) + " |"
    out.append(line)
p.write_text("\n".join(out) + "\n", encoding="utf-8")
PY
    fi
    ;;
  intro)
    cat > "$project/README.md" <<'EOF'
# Acerca de esta guia

Intro sintetica para el PDF.
EOF
    ;;
  *)
    echo "redactora-stub: step no soportado: $step" >&2
    exit 2
    ;;
esac
