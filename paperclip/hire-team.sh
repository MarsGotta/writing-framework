#!/usr/bin/env bash
# paperclip/hire-team.sh
#
# Contrata (o actualiza) el equipo ejecutor de la Editora jefa en la Company
# Write.OnMars de Paperclip: Documentalista, Redactora y Editora de mesa. Cada uno
# con su bundle de instrucciones (paperclip/agents/<rol>/bundle.md como AGENTS.md)
# y modelos CRUZADOS: la Redactora escribe en Opus; las revisoras en Sonnet — para
# que "escribe uno, revisa otro" con modelo distinto.
#
# Idempotente: si un agente con ese nombre ya existe en la Company, no lo duplica;
# solo (re)carga su bundle. Resuelve los IDs por nombre, así sirve también tras una
# reinstalación (no hay IDs hardcodeados).
#
# HEADLESS: por defecto los agentes se crean con dangerouslySkipPermissions=true
# (igual que la Editora jefa que creó el wizard) para que corran desatendidos en los
# heartbeats. Es un permiso sensible: con --no-headless se crean en modo seguro
# (pedirán confirmación de herramientas). Tú decides al ejecutar.
#
# Uso:
#   bash paperclip/hire-team.sh
#   bash paperclip/hire-team.sh --no-headless
#   bash paperclip/hire-team.sh --company "Write.OnMars"
#   PAPERCLIP_BIN=/ruta/al/paperclipai bash paperclip/hire-team.sh

set -euo pipefail

company_name="Write.OnMars"
headless=1

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-headless) headless=0; shift ;;
        --company) company_name="${2:?--company necesita un nombre}"; shift 2 ;;
        -h|--help) sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "opción desconocida: $1" >&2; exit 1 ;;
    esac
done

# --- localizar el CLI -------------------------------------------------------
BIN="${PAPERCLIP_BIN:-}"
if [[ -z "$BIN" ]]; then
    if command -v paperclipai >/dev/null 2>&1; then
        BIN="paperclipai"
    else
        BIN="$(ls -d "$HOME"/.npm/_npx/*/node_modules/.bin/paperclipai 2>/dev/null | head -1 || true)"
    fi
fi
[[ -n "$BIN" ]] || { echo "[hire] no encuentro el CLI 'paperclipai' (exporta PAPERCLIP_BIN)" >&2; exit 1; }

R="$(cd "$(dirname "${BASH_SOURCE[0]}")/agents" && pwd)"

# --- resolver Company y Editora jefa (CEO) ----------------------------------
CID="$("$BIN" company list --json 2>/dev/null | python3 -c "import sys,json
d=json.load(sys.stdin); items=d if isinstance(d,list) else d.get('items',[])
print(next((c['id'] for c in items if c.get('name')==sys.argv[1]),''))" "$company_name")"
[[ -n "$CID" ]] || { echo "[hire] no existe la Company '$company_name'" >&2; exit 1; }

agents_json="$("$BIN" agent list --company-id "$CID" --json 2>/dev/null)"
CEO="$(printf '%s' "$agents_json" | python3 -c "import sys,json
d=json.load(sys.stdin); items=d if isinstance(d,list) else d.get('items',[])
print(next((a['id'] for a in items if a.get('role')=='ceo'),''))")"
[[ -n "$CEO" ]] || { echo "[hire] no encuentro la Editora jefa (rol ceo) en '$company_name'" >&2; exit 1; }

echo "[hire] Company '$company_name' ($CID) · Editora jefa $CEO · headless=$headless"

# --- contratar/actualizar cada rol ------------------------------------------
# nombre | modelo | carpeta-bundle
roster=(
    "Documentalista|claude-sonnet-4-6|documentalista"
    "Redactora|claude-opus-4-8|redactora"
    "Editora de mesa|claude-sonnet-4-6|editora-de-mesa"
)

for row in "${roster[@]}"; do
    IFS='|' read -r nm md dr <<< "$row"
    bundle="$R/$dr/bundle.md"
    [[ -f "$bundle" ]] || { echo "  [$nm] sin bundle en $bundle; salto" ; continue; }

    # ¿ya existe por nombre? (idempotencia)
    id="$(printf '%s' "$agents_json" | python3 -c "import sys,json
d=json.load(sys.stdin); items=d if isinstance(d,list) else d.get('items',[])
print(next((a['id'] for a in items if a.get('name')==sys.argv[1]),''))" "$nm")"

    if [[ -n "$id" ]]; then
        echo "  [$nm] ya existe ($id); recargo bundle"
    else
        payload="$(python3 -c "import json,sys
hl = sys.argv[4]=='1'
ac = {'model': sys.argv[2], 'instructionsBundleMode':'managed'}
if hl: ac['dangerouslySkipPermissions']=True
print(json.dumps({
 'name': sys.argv[1], 'role':'general', 'reportsTo': sys.argv[3],
 'adapterType':'claude_local', 'adapterConfig': ac,
 'runtimeConfig':{'heartbeat':{'enabled':False,'wakeOnDemand':True}},
 'permissions':{'canCreateAgents':False}}))" "$nm" "$md" "$CEO" "$headless")"
        resp="$("$BIN" agent create --company-id "$CID" --payload-json "$payload" --json 2>&1)"
        id="$(printf '%s' "$resp" | python3 -c "import sys,json
try: print(json.load(sys.stdin).get('id',''))
except: print('')" 2>/dev/null)"
        if [[ -z "$id" ]]; then
            echo "  [$nm] FALLO create:"; printf '%s\n' "$resp" | head -4; continue
        fi
        echo "  [$nm] creado ($id · $md)"
    fi

    "$BIN" agent instructions-file:put "$id" --path AGENTS.md --content-file "$bundle" >/dev/null \
        && echo "    bundle AGENTS.md cargado ($(wc -c < "$bundle" | tr -d ' ') b)" \
        || echo "    FALLO al cargar bundle"
done

echo
echo "[hire] equipo en '$company_name':"
"$BIN" agent list --company-id "$CID" 2>/dev/null
