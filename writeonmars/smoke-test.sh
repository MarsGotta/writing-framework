#!/usr/bin/env bash
# Smoke test del preset writeonmars: monta un proyecto editorial demo en un
# directorio temporal y corre los cinco scripts. No toca tu repo ni tus guías.
# Las piezas con dependencias externas (export → Chrome; feedback → pymupdf/pypdf)
# se saltan con aviso si la dependencia no está.
#
#   bash writeonmars/smoke-test.sh
#
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SCR="$HERE/scripts"
PY="${PYTHON:-python3}"
DEMO="$(mktemp -d)"; trap 'rm -rf "$DEMO"' EXIT
pass=0; skip=0; failc=0
ok(){ echo "  [OK]   $1"; pass=$((pass+1)); }
sk(){ echo "  [skip] $1"; skip=$((skip+1)); }
ko(){ echo "  [FAIL] $1"; failc=$((failc+1)); }

echo "== Montando proyecto demo en $DEMO =="
mkdir -p "$DEMO/specs/001-demo" "$DEMO/chapters"
cat > "$DEMO/specs/001-demo/spec.md" <<'EOF'
# Feature Specification: Prompts efectivos para developers
## Brief editorial
- Audiencia: developers
EOF
cat > "$DEMO/specs/001-demo/plan.md" <<'EOF'
## Temario
| Número | Título | Promesa | Estructura aplicada |
|--------|--------|---------|---------------------|
| 0 | Qué es un prompt | Define prompt y su anatomía | didactica_v1 |
| 1 | Contexto y tokens | Cómo el modelo ve el texto | didactica_v1 |
## Descripciones encadenadas
EOF
printf '# Qué es un prompt\n\nUn prompt es la entrada que damos al modelo.\n' > "$DEMO/chapters/00-prompt.md"
printf '# Contexto y tokens\n\nEl context window limita lo que el modelo ve.\n' > "$DEMO/chapters/01-contexto.md"
printf '# Prompts efectivos\n\nGuía de ejemplo.\n' > "$DEMO/README.md"
printf '# Glosario\n\n- prompt: entrada al modelo.\n' > "$DEMO/glosario.md"
cat > "$DEMO/.writeonmars-manifest.json" <<'EOF'
{ "signing_matrix": { "pasada_1_estructura":"autonomous","pasada_2_utilidad":"autonomous","pasada_3_naturalidad":"human","pasada_4_precision":"human","pasada_5_formato":"autonomous" } }
EOF
cat > "$DEMO/specs/001-demo/findings.md" <<'EOF'
## Pasada 1 — Estructura
**Estado pasada**: passed
**Firma**:
  - tipo: autonomous
**Capítulos cubiertos**: [0, 1]
### Hallazgos
| ID | Capítulo | Severidad | Frase original | Problema | Reescritura sugerida | Estado | Citas |
|----|----------|-----------|----------------|----------|---------------------|--------|-------|
| F-1.1 | 0 | bajo | "x" | "y" | "z" | resuelto | [] |
EOF

echo ""; echo "== 1) status =="
$PY "$SCR/status.py" --project-dir "$DEMO" >/dev/null 2>&1 && ok "status corre" || ko "status"

echo ""; echo "== 2) index (build + query) =="
if $PY "$SCR/index.py" build --project-dir "$DEMO" >/dev/null 2>&1; then
  $PY "$SCR/index.py" query "context window" --project-dir "$DEMO" | grep -q "01-contexto" \
    && ok "index encuentra el capítulo correcto" || ko "index query"
else ko "index build"; fi

echo ""; echo "== 3) close --no-export (demo cerrable: sin críticos abiertos) =="
$PY "$SCR/close.py" --project-dir "$DEMO" --no-export >/dev/null 2>&1 && ok "close evalúa el gate" || ko "close"

echo ""; echo "== 4) feedback-intake (necesita pymupdf o pypdf) =="
if $PY -c "import fitz" 2>/dev/null; then
  $PY - "$DEMO" <<'PY'
import sys, fitz
d=sys.argv[1]; doc=fitz.open(); p=doc.new_page()
p.insert_text((72,100),"Un prompt es la entrada")
for r in p.search_for("Un prompt es la entrada"):
    a=p.add_highlight_annot(r); a.set_info(content="#voz revisar"); a.update()
doc.save(d+"/demo.pdf")
PY
  $PY "$SCR/feedback_intake.py" --pdf "$DEMO/demo.pdf" --project-dir "$DEMO" | grep -q "00-prompt" \
    && ok "feedback mapea la anotación a su capítulo" || ko "feedback"
elif $PY -c "import pypdf" 2>/dev/null; then
  sk "feedback: pypdf solo lee comentarios; instala pymupdf para el texto resaltado"
else
  sk "feedback: instala pymupdf  (pip install pymupdf)"
fi

echo ""; echo "== 5) export (necesita pandoc + Chrome/Chromium) =="
CHROME=""
for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" chromium google-chrome google-chrome-stable chromium-browser; do
  command -v "$c" >/dev/null 2>&1 && CHROME="$c" && break
  [ -x "$c" ] && CHROME="$c" && break
done
if command -v pandoc >/dev/null 2>&1 && [ -n "$CHROME" ]; then
  $PY "$SCR/export.py" --project-dir "$DEMO" --chrome "$CHROME" >/dev/null 2>&1 \
    && ls "$DEMO"/*.pdf >/dev/null 2>&1 && ok "export genera el PDF" || ko "export"
else
  sk "export: falta pandoc o Chrome/Chromium"
fi

echo ""; echo "== Resumen: $pass OK, $skip omitidos, $failc fallos =="
[ "$failc" -eq 0 ] && echo "Smoke test correcto." || { echo "Hay fallos."; exit 1; }
