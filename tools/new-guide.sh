#!/usr/bin/env bash
# tools/new-guide.sh
#
# Scaffolding de una guía Write.OnMars: prepara el "base ref" que Paperclip
# conecta como Project. Hace de un tirón los pasos de instalación de la guía:
#
#   1. crea la carpeta y el repo git
#   2. inicializa Spec Kit (`specify init`)            [omitible]
#   3. añade el preset writeonmars (`specify preset add`)
#   4. corre bootstrap.py (= speckit.setup: constitución núcleo + manifest)
#   5. commit inicial → ese commit es el base ref de Paperclip
#
# A partir de aquí el agente (Editora jefa) toma el relevo: su primer paso es
# `speckit.constitution` (adendas: sector + tono). El scaffold NO es trabajo
# editorial; es infra de una sola vez, por eso lo corre el humano.
#
# El operador y el email se heredan de tu identidad de git por defecto
# (`git config user.name/.email`); solo usa los flags para sobrescribirlos.
#
# Uso:
#   bash tools/new-guide.sh mi-guia
#   bash tools/new-guide.sh ~/guias/context-window --operator otro.id --email otro@correo
#   bash tools/new-guide.sh mi-guia --skip-init        # si ya corriste `specify init`
#   bash tools/new-guide.sh mi-guia --preset /ruta/al/writeonmars
#   bash tools/new-guide.sh mi-guia --agents claude,gemini,codex   # 1º = primario de init
#
# Multi-agente: la lógica del pipeline es compartida (todos leen el preset por
# ruta). El script unifica el contexto raíz con symlinks (AGENTS.md canónico ←
# CLAUDE.md, GEMINI.md). NO symlinkea las carpetas de comandos: formatos distintos
# (Claude .md, Gemini .toml). `specify init` usa el agente primario vía `--integration`.
#
# `specify init` puede ser interactivo (pide el agente). Si tu versión necesita
# flags distintos, exporta SPECIFY_INIT_CMD o usa --skip-init y córrelo a mano:
#   SPECIFY_INIT_CMD="specify init --here --integration claude" bash tools/new-guide.sh mi-guia
#
# Exit 0 si el base ref queda listo; exit 1 si falta un prerrequisito o un paso
# no produjo lo esperado (no deja la guía a medias en silencio).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# --- defaults ---------------------------------------------------------------
preset="$REPO_ROOT/writeonmars"
operator=""   # vacío = hereda la identidad de git (≈ tu identidad de GitHub)
email=""      # idem
skip_init=0
refresh_preset=0   # con --refresh-preset re-copia el preset sobre una guía ya instalada (dev loop)
agents="claude,gemini,codex"   # 1º = agente primario de `specify init`; todos reciben symlink de contexto
target=""

fail() {
    printf '[new-guide] error: %s\n' "$1" >&2
    exit 1
}

usage() {
    # Imprime la cabecera de comentarios (tras el shebang) hasta la primera línea no-comentario.
    awk 'NR==1{next} /^#/{sub(/^# ?/,""); print; next} {exit}' "${BASH_SOURCE[0]}"
    exit "${1:-0}"
}

# --- parseo de argumentos ---------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help) usage 0 ;;
        --skip-init) skip_init=1; shift ;;
        --refresh-preset) refresh_preset=1; shift ;;
        --agents) agents="${2:?--agents necesita una lista CSV}"; shift 2 ;;
        --preset) preset="${2:?--preset necesita una ruta}"; shift 2 ;;
        --operator) operator="${2:?--operator necesita un id}"; shift 2 ;;
        --email) email="${2:?--email necesita un valor}"; shift 2 ;;
        --*) fail "opción desconocida: $1 (usa --help)" ;;
        *)
            [[ -z "$target" ]] || fail "solo se admite una guía a la vez (ya diste '$target')"
            target="$1"; shift ;;
    esac
done

[[ -n "$target" ]] || usage 1
[[ -d "$preset" ]] || fail "no encuentro el preset en '$preset' (usa --preset <ruta>)"
[[ -f "$preset/scripts/bootstrap.py" ]] || fail "'$preset' no parece el preset writeonmars (falta scripts/bootstrap.py)"

# --- prerrequisitos ---------------------------------------------------------
command -v git >/dev/null 2>&1 || fail "git no está en PATH"
command -v python3 >/dev/null 2>&1 || fail "python3 no está en PATH"
if [[ "$skip_init" -eq 0 ]]; then
    command -v specify >/dev/null 2>&1 || fail "el CLI 'specify' no está en PATH (instala Spec Kit, o usa --skip-init)"
fi

# --- 1. carpeta + repo ------------------------------------------------------
if [[ -e "$target" && ! -d "$target" ]]; then
    fail "'$target' existe y no es una carpeta"
fi
mkdir -p "$target"
target_abs="$(cd "$target" && pwd)"
cd "$target_abs"
printf '[new-guide] guía en: %s\n' "$target_abs"

if [[ -d .git ]]; then
    printf '[new-guide] repo git ya inicializado\n'
else
    git init -q
    printf '[new-guide] git init\n'
fi

# --- 2. specify init --------------------------------------------------------
# Agente primario = primero de la lista. Lo pasamos por `--integration` para NO
# entrar al menú interactivo, `--force` para saltar el "directory not empty" (ya
# hay .git), e `--ignore-agent-tools` porque los agentes corren en Paperclip, no
# aquí: solo queremos las plantillas, no que verifique el CLI del agente instalado.
primary="${agents%%,*}"
if [[ -d .specify ]]; then
    printf '[new-guide] .specify/ ya presente; salto specify init\n'
elif [[ "$skip_init" -eq 1 ]]; then
    fail "--skip-init pero no hay .specify/; corre 'specify init' aquí y reintenta"
else
    init_cmd="${SPECIFY_INIT_CMD:-specify init --here --force --ignore-agent-tools --integration $primary}"
    printf '[new-guide] %s\n' "$init_cmd"
    # shellcheck disable=SC2086
    $init_cmd || fail "specify init falló (agente '$primary'). Ajusta SPECIFY_INIT_CMD o usa --skip-init tras correrlo a mano"
    [[ -d .specify ]] || fail "specify init no creó .specify/ (¿flags distintos en tu versión? usa SPECIFY_INIT_CMD o --skip-init)"
fi

# --- 3. preset add ----------------------------------------------------------
if [[ -d .specify/presets/writeonmars ]]; then
    if [[ "$refresh_preset" -eq 1 ]]; then
        cp -R "$preset/." .specify/presets/writeonmars/
        printf '[new-guide] preset re-copiado en sitio (--refresh-preset)\n'
    else
        printf '[new-guide] preset writeonmars ya instalado; salto (--refresh-preset para actualizar)\n'
    fi
else
    printf '[new-guide] specify preset add --dev %s\n' "$preset"
    specify preset add --dev "$preset" || fail "specify preset add falló"
    [[ -d .specify/presets/writeonmars ]] || fail "el preset no quedó en .specify/presets/writeonmars tras 'preset add'"
fi

# --- 4. bootstrap (= speckit.setup) -----------------------------------------
# Identidad del operador: si no la diste por flag, hereda la de git
# (`git config user.email/.name`, que suele ser tu identidad de GitHub).
[[ -n "$email" ]] || email="$(git config user.email 2>/dev/null || true)"
if [[ -z "$operator" ]]; then
    operator="$(git config user.email 2>/dev/null | sed 's/@.*//' || true)"   # parte local del email
    [[ -n "$operator" ]] || operator="$(git config user.name 2>/dev/null || true)"
    [[ -n "$operator" ]] || operator="autor"
fi
printf '[new-guide] operador: %s%s\n' "$operator" "${email:+ <$email>}"

# `specify init` planta una constitución PLACEHOLDER de spec-kit, y bootstrap.py no
# sobrescribe una existente (sin --force). La descartamos para que bootstrap copie el
# NÚCLEO writeonmars. Solo borramos el placeholder ([PROJECT_NAME]); nunca un núcleo
# real ya sellado (que no contiene ese marcador), así el re-run preserva adendas.
const=".specify/memory/constitution.md"
if [[ -f "$const" ]] && grep -q '\[PROJECT_NAME\]' "$const"; then
    rm -f "$const"
    printf '[new-guide] descarto la constitución placeholder de spec-kit\n'
fi

boot_args=(--operator "$operator")
[[ -n "$email" ]] && boot_args+=(--email "$email")
printf '[new-guide] bootstrap.py (constitución núcleo + manifest)\n'
python3 .specify/presets/writeonmars/scripts/bootstrap.py "${boot_args[@]}" \
    || fail "bootstrap.py falló"
[[ -f .writeonmars-manifest.json ]] || fail "bootstrap no generó .writeonmars-manifest.json"
[[ -f "$const" ]] || fail "no se escribió la constitución"
if grep -q '\[PROJECT_NAME\]' "$const"; then
    fail "la constitución sigue siendo el placeholder de spec-kit (bootstrap no copió el núcleo)"
fi

# --- 6. compatibilidad multi-agente -----------------------------------------
# La LÓGICA del pipeline ya es compartida: todos los agentes leen el preset por
# ruta (.specify/presets/writeonmars/). NO replicamos las carpetas de comandos
# (formatos distintos: Claude .md, Gemini .toml). Solo unificamos el archivo de
# contexto raíz con symlinks, para que Claude (CLAUDE.md), Gemini (GEMINI.md) y
# Codex (AGENTS.md) lean lo mismo. El registro nativo de slash-commands en otros
# agentes es opcional: corre `specify init --here --integration <agente>` aparte si lo quieres.
canonical="AGENTS.md"
# spec-kit init suele crear AGENTS.md (contexto gestionado entre marcas SPECKIT).
# Si no existe pero hay un CLAUDE.md real, lo promovemos a canónico. Luego añadimos
# el bloque writeonmars UNA vez (sin pisar lo que gestione spec-kit).
if [[ ! -e "$canonical" && -f CLAUDE.md && ! -L CLAUDE.md ]]; then
    mv CLAUDE.md "$canonical"
    printf '[new-guide] CLAUDE.md → %s (contexto canónico)\n' "$canonical"
fi
[[ -e "$canonical" ]] || : > "$canonical"
if ! grep -q 'WRITEONMARS:CONTEXT' "$canonical" 2>/dev/null; then
    cat >> "$canonical" <<'CTX'

<!-- WRITEONMARS:CONTEXT -->
## Proyecto editorial Write.OnMars

Cualquier agente (Claude, Gemini, Codex…) ejecuta el pipeline leyendo, por ruta:

- Contrato del agente:  `.specify/presets/writeonmars/AGENTS.md`
- Reglas editoriales:   `.specify/memory/constitution.md`
- Comandos del preset:  skills `speckit-*` (o `.specify/presets/writeonmars/commands/`)

No dependas de skills propietarias: voz, didáctica y método viajan en
`.specify/presets/writeonmars/references/`.
<!-- /WRITEONMARS:CONTEXT -->
CTX
    printf '[new-guide] contexto writeonmars añadido a %s\n' "$canonical"
fi

link_ctx() {  # link_ctx <archivo>  —  symlink → AGENTS.md, respaldando si era real
    local f="$1"
    [[ "$f" == "$canonical" || -L "$f" ]] && return 0
    [[ -e "$f" ]] && { mv "$f" "$f.bak"; printf '[new-guide] %s existía; respaldado a %s.bak\n' "$f" "$f"; }
    ln -s "$canonical" "$f"
    printf '[new-guide] symlink %s → %s\n' "$f" "$canonical"
}

IFS=',' read -ra _agents_arr <<< "$agents"
for a in "${_agents_arr[@]}"; do
    case "$a" in
        claude) link_ctx CLAUDE.md ;;
        gemini) link_ctx GEMINI.md ;;
        codex)  : ;;  # Codex lee AGENTS.md de forma nativa; no necesita symlink
        *) printf '[new-guide] agente "%s": sin mapeo de contexto, salto\n' "$a" ;;
    esac
done

# --- 7. .gitignore + commit inicial = base ref ------------------------------
# Cachés y basura del SO no van al base ref. El manifest SÍ (es estado del Project).
for pat in '.DS_Store' '.writeonmars-index.json'; do
    grep -qxF "$pat" .gitignore 2>/dev/null || echo "$pat" >> .gitignore
done
# Destrackea cualquier .DS_Store ya commiteado (también los anidados que arrastra el
# preset al copiarse) y el índice-caché. El .gitignore evita que vuelvan a entrar.
git ls-files | { grep -E '(^|/)\.DS_Store$|(^|/)\.writeonmars-index\.json$' || true; } \
    | while IFS= read -r f; do
        git rm --cached -q --ignore-unmatch -- "$f" >/dev/null 2>&1 || true
    done

git add -A
if git diff --cached --quiet; then
    printf '[new-guide] nada que commitear (¿re-corrida sobre guía ya scaffoldeada?)\n'
else
    git commit -q -m "scaffold guía '$(basename "$target_abs")': preset + constitución + manifest"
    printf '[new-guide] commit inicial creado (este es el base ref)\n'
fi

# --- siguiente paso ---------------------------------------------------------
cat <<EOF

[new-guide] base ref listo en $target_abs
Agentes compatibles: $agents (contexto unificado vía AGENTS.md + symlinks)
Siguiente:
  1. (opcional) crea un remoto y empuja:   git remote add origin <url> && git push -u origin main
  2. En Paperclip: nuevo Project → conecta este repo (base ref: main)
     · provisioning sugerido:  pip install pymupdf rank-bm25
     · goal del Project: el tema/brief de la guía
  3. La Editora jefa arranca en 'speckit.constitution' (adendas: sector + tono).
  4. (opcional) slash-commands nativos en otro agente:  specify init --here --integration <agente>
EOF
