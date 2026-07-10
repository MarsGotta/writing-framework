# Contrato CLI — `track.py` y deltas de `bootstrap.py` / `status.py` / `export.py`

**Feature**: 006-pista-corta-editorial · **Fecha**: 2026-07-10

Todo lo determinista vive en scripts (Principio VI). Este contrato fija sus
interfaces exactas: argumentos, exit codes, efectos en disco. Un implementador
debe poder escribir los tests antes que el código.

---

## 1. `writeonmars/scripts/track.py` (NUEVO)

Único camino para cambiar la pista de un proyecto. Patrón `dispose.py`:
identidad humana desde git, validación de legalidad, escritura atómica.

### 1.1 Interfaz

```text
python3 scripts/track.py --escalar     [--project-dir DIR] [--spec SPEC] [--json]
python3 scripts/track.py --desescalar  [--project-dir DIR] [--spec SPEC] [--json]
python3 scripts/track.py --check       [--project-dir DIR] [--spec SPEC] [--json]
```

`--escalar`, `--desescalar` y `--check` forman un grupo mutuamente excluyente y
**obligatorio** (`add_mutually_exclusive_group(required=True)`).

| Argumento | Default | Descripción |
|---|---|---|
| `--project-dir` | `.` | Raíz del proyecto editorial |
| `--spec` | el más reciente | `specs/<dir>` concreto, vía `findings_lib.newest_spec_dir` |
| `--json` | `false` | Emite el registro (o el diagnóstico de `--check`) como JSON en stdout |

### 1.2 Identidad humana (idéntica a `dispose.py:45`)

```python
actor = git_config(project, "user.name")
email = git_config(project, "user.email")
if not actor:
    die("sin git config user.name; no hay identidad humana auditable", 3)
if actor.endswith("@agents.writeonmars.invalid") or email.endswith("@agents.writeonmars.invalid"):
    die("la identidad git pertenece a un agente; el cambio de pista debe ser humano", 3)
```

`--check` **no** exige identidad humana (es read-only).

### 1.3 Legalidad de las transiciones

Pista actual vía `findings_lib.project_track(manifest)`.

| Operación | Precondición | Si falla |
|---|---|---|
| `--escalar` | `track == "corta"` | exit 1: `"el proyecto ya está en pista estandar"` |
| `--desescalar` | `track == "estandar"` (o ausente) | exit 1: `"el proyecto ya está en pista corta"` |
| `--desescalar` | `findings_lib.count_temario(spec_dir) <= 1` | exit 1: `"el temario tiene N filas; la pista corta exige pieza única"` |
| `--desescalar` | ningún `chapters/NN-*.md` con `NN >= 2` | exit 1: `"existen capítulos fuera de pieza única: 2, 3"` |
| cualquiera | manifiesto presente | exit 1: `"falta <ruta>/.writeonmars-manifest.json"` |
| cualquiera | `track` del manifiesto es válido | exit 1 (propaga el `ValueError` de `project_track`) |

`--escalar` es **siempre legal** desde `corta`. No comprueba nada del disco: la
conservación del trabajo es emergente (data-model § 6).

### 1.4 Efecto en disco (`--escalar` / `--desescalar`)

Escritura **atómica** del manifiesto (tmp + `os.replace`, rollback ante
excepción, patrón `dispose.py:135`):

1. `manifest["track"] = <destino>`
2. `manifest.setdefault("track_history", []).append(record)`, con

```json
{"from": "<origen>", "to": "<destino>", "date": "<UTC ISO-8601 Z, sin microsegundos>", "actor": "<git user.name>", "email": "<git user.email si existe>"}
```

3. Se preserva el orden de claves existente y el `indent=2` con
   `ensure_ascii=False` (como `bootstrap.py:171`).

**No se toca ningún otro archivo.** Ni `plan.md`, ni `chapters/`, ni
`findings.md`, ni `claims.md`.

### 1.5 `--check` (read-only)

Valida el invariante `track == "corta"` ⟺ (temario ≤ 1 fila ∧ sin capítulos con
ordinal ≥ 2).

| Resultado | Exit | Salida |
|---|---|---|
| Coherente | 0 | `[track] corta: coherente (temario 1 fila, 1 capítulo)` |
| Temario > 1 fila en corta | 1 | `[track] error: track: corta con temario de N filas; corrige el temario o escala` |
| Capítulos ≥ 2 en corta | 1 | `[track] error: track: corta con capítulos fuera de pieza única: 2, 3` |
| `track == estandar` | 0 | `[track] estandar: sin invariante de pieza única que verificar` |

### 1.6 Exit codes (espejo de `dispose.py`)

| Code | Significado |
|---|---|
| 0 | OK |
| 1 | Error de estado o de legalidad (manifiesto ausente, transición ilegal, `track` inválido) |
| 2 | Error de uso (argumentos) — lo produce `argparse` |
| 3 | Identidad no humana o ausente |

### 1.7 Salida `--json`

`--escalar` / `--desescalar` emiten el `record` recién anexado, con
`sort_keys=True`, una línea. `--check` emite:

```json
{"track": "corta", "temario_filas": 1, "capitulos_fuera": [], "coherente": true}
```

---

## 2. `writeonmars/scripts/bootstrap.py` (EXTENDER)

### 2.1 Argumentos nuevos

```python
ap.add_argument("--track",
                default=os.environ.get("WRITEONMARS_TRACK", "estandar"),
                choices=["estandar", "corta"],
                help="Pista de ceremonia: estandar (default) o corta.")
ap.add_argument("--sector", default=os.environ.get("WRITEONMARS_SECTOR"),
                help="Slug del sector (references/sectores/<slug>.md). Fija adendas por referencia.")
```

**Obligatorio**: revalidar `--track` fuera de `choices`, porque `argparse` no
valida el default. Es el mismo bug que `bootstrap.py:133` ya evita para `--mode`:

```python
if args.track not in ("estandar", "corta"):
    fail(f"track inválido: {args.track!r} (esperado estandar|corta; revisa WRITEONMARS_TRACK)")
```

### 2.2 Efecto de `--track`

`default_manifest()` gana el parámetro `track` y escribe la clave `track` en el
manifiesto (siempre, también con `estandar`: explícito es mejor que implícito, y
el schema lo admite).

### 2.3 Efecto de `--sector`

Con `--sector <slug>`:

1. Verifica que existe `PRESET / "references" / "sectores" / f"{slug}.md"`. Si
   no, `fail()` con exit 1 listando los slugs disponibles (todos los `*.md` del
   directorio salvo `_index.md`).
2. `manifest["sector"] = slug`.
3. Extrae el slug del registro de la sección `## Registro por defecto` de ese
   archivo — primer texto entre backticks tras el encabezado. Si lo encuentra,
   `manifest["registro"] = <registro-slug>`.
4. Materializa el bloque de adendas **por referencia** al final de
   `.specify/memory/constitution.md`, empezando por el centinela
   `<!-- WRITEONMARS:ADENDAS -->`. Forma exacta en `research.md` § R2.
   - Si el centinela ya existe, **no** se reescribe (respeta adendas calibradas
     a mano). Se imprime un aviso.
   - Si no existe, se anexa tras el núcleo.

Sin `--sector` (default `None`): comportamiento actual intacto —
`manifest["sector"] = None`, ninguna adenda, la brújula pide `constitution`.

### 2.4 Lo que NO cambia

`vivarium/crates/vivarium-core/src/bootstrap.rs` no se modifica: `vivarium new`
sigue pasando solo `--mode`. `WRITEONMARS_TRACK` y `WRITEONMARS_SECTOR` viajan al
proceso hijo por entorno (R3). El paso `setup` del runner (`runner.rs:445`)
tampoco cambia.

---

## 3. `writeonmars/scripts/status.py` (MÍNIMO)

### 3.1 Un campo nuevo

`evaluate()` añade `"track": findings_lib.project_track(manifest)` al dict de
salida, junto a `"mode"`. **Siempre presente, nunca `null`.**

Se añade el wrapper `project_track(manifest)` local que convierte `ValueError` en
`fail()`, espejo exacto de `project_mode` (`status.py:66`).

### 3.2 Dos warnings advisory

Solo cuando `track == "corta"`, se anexan a la lista `warnings` existente:

```python
if track == "corta":
    if expected > 1:
        warnings.append(
            f"track: corta declara pieza única pero el temario tiene {expected} filas: "
            "corrige el temario o escala (scripts/track.py --escalar)"
        )
    fuera = sorted(n for n in drafted_ordinals if n >= 2)
    if fuera:
        warnings.append(
            "track: corta con capítulos fuera de pieza única ("
            + ", ".join(str(n) for n in fuera)
            + "): sugiere escalar (scripts/track.py --escalar)"
        )
```

### 3.3 Prohibiciones explícitas (SC-003, FR-001)

`status.py` **MUST NOT** modificar, para esta feature:

- `_next_step` (ni su firma, ni sus ramas, ni sus textos de `next_detail`)
- `_build_by_chapter`, `_passes_by_chapter`, `_passes_by_chapter_checked`
- el cálculo de `gates`, `closeable`, `all_chapters_approved`
- `print_dashboard` — la salida humana de un proyecto `estandar` es
  **byte-idéntica** a la anterior

Las dos entradas de `warnings` son informativas y no bloquean (R5). En un
proyecto `estandar` no se emite ninguna, así que la retrocompatibilidad se
sostiene.

### 3.4 Mudanza a `findings_lib.py` (R10)

`count_temario` y `_drafted_ordinals` pasan a `findings_lib.py` como
`count_temario(spec_dir)` y `drafted_ordinals(chapters)`. `status.py` conserva
alias módulo-locales para no romper importadores ni tests:

```python
count_temario = findings_lib.count_temario
_drafted_ordinals = findings_lib.drafted_ordinals
```

`findings_lib.py` gana también `project_track(manifest)` (data-model § 1).

**Gate de la mudanza**: `python3 -m pytest tests/unit -q` pasa sin editar una
sola aserción existente.

---

## 4. `writeonmars/scripts/export.py` (EXTENDER)

### 4.1 Detección de pista

```python
manifest = findings_lib.load_manifest(project)   # tolerante: None si no existe
track = findings_lib.project_track(manifest)
```

`export.py` es standalone y hoy no importa `findings_lib`. Añadir el import con
el mismo prólogo `sys.path` que usan `status.py` y `dispose.py`.

### 4.2 Comportamiento cuando `track == "corta"`

| Aspecto | Estándar | Corta |
|---|---|---|
| Portada | `build_cover(eyebrow, title, subtitle, meta)` | `build_cover_compact(title, author, meta)` |
| Plantilla | `assets/cover.html.template` | `assets/cover-compact.html.template` |
| Índice | `build_toc(...)` | **no se invoca** |
| `README.md` | se incluye si existe | se incluye si existe (ya condicional) |
| Fuentes | `.chapter-sources` | `.chapter-sources` (idéntico) |
| Validación `claims.md` | idéntica | idéntica |

`author` sale de `manifest["human_operators"][0]`: `id` si no hay `email`; si el
manifiesto falta o la lista está vacía, cadena vacía y la portada omite la línea.

### 4.3 `build_cover_compact` — función pura

```python
def build_cover_compact(title: str, author: str, meta: str) -> str:
    tpl = (ASSETS / "cover-compact.html.template").read_text(encoding="utf-8")
    return (tpl.replace("{{TITLE}}", html.escape(title))
               .replace("{{AUTHOR}}", html.escape(author))
               .replace("{{META}}", html.escape(meta)))
```

### 4.4 `assets/cover-compact.html.template` (NUEVO)

```html
<div class="cover cover-compact">
  <h1 class="cover-title">{{TITLE}}</h1>
  <div class="cover-author">{{AUTHOR}}</div>
  <div class="cover-meta">{{META}}</div>
</div>
```

Conserva la clase `.cover` para heredar `page: cover` y
`page-break-after: always`. `style.css` gana solo `.cover-author` y los ajustes
de `.cover-compact`; no se toca la regla `@page cover` (R9).

### 4.5 Criterio de aceptación sin Chrome

1. `build_cover_compact("T", "A", "2026")` contiene `cover-compact`, `T`, `A`,
   `2026`; **no** contiene `cover-eyebrow` ni `cover-subtitle`.
2. Sobre el fixture corta, el HTML intermedio de `main()` con `--keep-temp`
   **no** contiene la subcadena `toc-page`.
3. Sobre un fixture `estandar`, el HTML intermedio **sí** contiene `toc-page` y
   `cover-eyebrow` (regresión).

---

## 5. Resumen de exit codes del contrato

| Script | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `track.py` | OK | estado / legalidad | uso (argparse) | identidad no humana |
| `bootstrap.py` | OK | error (sector inexistente, track inválido) | — | — |
| `status.py` | OK | `--gate` y no cerrable | error de lectura (`fail`) | — |
| `export.py` | OK | error (`fail`, `--strict-claims`) | — | — |
