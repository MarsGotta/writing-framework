# Quickstart — validación de la pista corta (feature 006)

**Fecha**: 2026-07-10

Recorrido de verificación, escenario a escenario. Cada sección mapea a una user
story o a un criterio de éxito y termina en una comprobación **ejecutable por
script**, sin agentes reales. Un implementador puede escribir estos checks antes
que el código.

Gates globales (los tres deben quedar en verde al cerrar la feature, SC-006):

```bash
# El python3 del sistema no trae pytest: usa uvx (o el venv que prefieras).
uvx --with pytest --with pyyaml --with jsonschema python -m pytest tests/unit -q
bash tests/smoke/run-all.sh
cd vivarium && cargo test --workspace
```

**Baseline al planificar** (2026-07-10): 169 tests unitarios en verde. Toda cifra
posterior debe ser ≥ 169 y ninguna aserción preexistente puede editarse (FR-010).

---

## 0. Preparar los fixtures

```text
tests/fixtures/006-corta/
├── produccion/                  # track: corta, mode: produccion
│   ├── .writeonmars-manifest.json
│   ├── .specify/memory/constitution.md
│   ├── specs/001-mi-pieza/spec.md          # brief compacto firmado
│   ├── specs/001-mi-pieza/research.md
│   ├── specs/001-mi-pieza/plan.md          # § Temario con UNA fila
│   ├── specs/001-mi-pieza/findings.md      # bloques 1·2·3·5 + 4, con huellas
│   ├── specs/001-mi-pieza/claims.md
│   └── chapters/01-la-pieza.md
└── estudio/                     # track: corta, mode: estudio (misma forma)
```

El fixture `estandar` de referencia para las regresiones ya existe:
`tests/fixtures/005-estudio/` y `tests/fixtures/003-factualidad/`.

---

## 1. Retrocompatibilidad — SC-003, FR-010

**Lo que se afirma**: un proyecto sin `track` (o con `track: estandar`) se
comporta exactamente igual que antes de la feature.

```bash
# 1a. El dashboard humano es BYTE-IDÉNTICO.
python3 writeonmars/scripts/status.py --project-dir tests/fixtures/003-factualidad > /tmp/after.txt
diff /tmp/before.txt /tmp/after.txt   # capturado antes de tocar nada → sin diferencias
```

```bash
# 1b. --json gana EXACTAMENTE una clave: "track": "estandar". Ninguna otra diferencia.
python3 writeonmars/scripts/status.py --json --project-dir tests/fixtures/003-factualidad \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["track"]=="estandar", d["track"]; print("OK")'
```

```bash
# 1c. Ninguna aserción existente se edita.
uvx --with pytest --with pyyaml --with jsonschema python -m pytest tests/unit -q
```

**Criterio**: 1a sin diferencias; 1b imprime `OK`; 1c en verde **sin haber
modificado una sola línea de test preexistente**. La mudanza de `count_temario`
y `drafted_ordinals` a `findings_lib.py` (R10) debe pasar este gate antes de
tocar nada más.

Regresión adicional: `python3 status.py --json` sobre un manifiesto con
`"track": "rapida"` falla con exit 2 y mensaje claro (espejo de `mode`).

---

## 2. US1 — Declarar la pista y recorrer el ciclo corto

**Lo que se afirma**: el ciclo corto existe de punta a punta, la brújula nunca
pide `plan`, el ejecutor nunca exige `intro`, y el camino feliz cuesta ≤ 8
despachos.

### 2.1 Crear un proyecto corta sin tocar el ejecutor (R3)

```bash
WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia \
  vivarium new "$PROJECT" --kind guia --preset "$REPO_ROOT/writeonmars" \
    --operator smoke --email smoke@example.com
```

Comprobaciones:

```bash
python3 -c '
import json; m=json.load(open("'"$PROJECT"'/.writeonmars-manifest.json"))
assert m["track"] == "corta", m.get("track")
assert m["sector"] == "tecnologia", m.get("sector")
assert m["registro"] == "tecnico-divulgativo", m.get("registro")
print("OK manifiesto")'

grep -q "WRITEONMARS:ADENDAS" "$PROJECT/.specify/memory/constitution.md"
grep -q "POR REFERENCIA" "$PROJECT/.specify/memory/constitution.md"
```

Sector inexistente → exit 1 y lista de sectores disponibles:

```bash
WRITEONMARS_SECTOR=inventado python3 writeonmars/scripts/bootstrap.py --project-dir "$P2"; echo $?   # → 1
```

### 2.2 La brújula no pide `constitution` ni `plan` (AS-1)

Con el brief firmado y el temario degenerado de una fila:

```bash
python3 writeonmars/scripts/status.py --json --project-dir tests/fixtures/006-corta/produccion \
  | python3 -c '
import json,sys; d=json.load(sys.stdin)
assert d["chapters_expected"] == 1, d["chapters_expected"]
assert d["next_step"] not in ("plan", "constitution"), d["next_step"]
print("OK brújula")'
```

**Verificación fuerte**: recorrer todos los estados intermedios del fixture
(sin research, con research, con capítulo, con pasadas) y comprobar que
`next_step` **nunca** vale `plan` ni `constitution`.

### 2.3 Sin `intro`, con PDF de pieza única (AS-2)

```bash
cd vivarium && cargo test plan_global_omite_intro_en_corta
```

```bash
# export: sin índice, con portada compacta
python3 writeonmars/scripts/export.py --project-dir tests/fixtures/006-corta/produccion --keep-temp
# el HTML intermedio no contiene toc-page y sí cover-compact
```

Test unitario sin Chrome (`tests/unit/test_export.py`):

- `build_cover_compact("T","A","2026")` contiene `cover-compact`, no contiene
  `cover-eyebrow` ni `cover-subtitle`.
- Sobre el fixture corta, el HTML ensamblado no contiene `toc-page`.
- Sobre un fixture estándar, **sí** contiene `toc-page` y `cover-eyebrow`.

### 2.4 ≤ 8 despachos (AS-3, SC-001)

Tras el `vivarium run` completo del smoke:

```bash
python3 - <<'PY'
import json
n = sum(1 for line in open("$PROJECT/.vivarium/decisions.jsonl")
        if json.loads(line).get("event") == "dispatch")
assert n <= 8, f"{n} despachos, esperaba <= 8"
print(f"OK {n} despachos")
PY
```

Valor esperado: **6** (`research`, `implement`, `review-1`, `review-4`,
`export`, `close`). Los checkpoints (`specify`, `feedback`) tienen
`event == "checkpoint"` y no cuentan.

### 2.5 `track` desconocido falla claro (AS-5)

```bash
python3 writeonmars/scripts/status.py --project-dir "$BROKEN"; echo $?   # → 2, mensaje claro
python3 writeonmars/scripts/track.py --check --project-dir "$BROKEN"; echo $?   # → 1
```

---

## 3. US2 — Cinco dimensiones, dos relevos

**Lo que se afirma**: las cinco dimensiones constan en `findings.md`, el
capítulo llega a `approved` **sin cambio alguno en `status.py`**, y la combinada
no es un punto único de fallo.

### 3.1 Las cinco dimensiones y el `approved` (AS-1, AS-2, SC-002)

Con la combinada (bloques 1·2·3·5) y la precisión (bloque 4 + `claims.md`)
registradas:

```bash
python3 writeonmars/scripts/status.py --json --project-dir tests/fixtures/006-corta/produccion \
  | python3 -c '
import json,sys; d=json.load(sys.stdin)
nums = sorted(p["num"] for p in d["passes"])
assert nums == [1,2,3,4,5], nums                    # cinco dimensiones
assert d["by_chapter"]["1"]["approved"] is True     # con el parser ACTUAL
assert d["closeable"] is True
print("OK cinco dimensiones, cap 1 approved")'

test -f tests/fixtures/006-corta/produccion/specs/001-mi-pieza/claims.md
```

Comprobación estructural: los bloques 1-3 declaran `Capítulos cubiertos: 1`; el
bloque 5, `global`. Todos llevan `<!-- pass-output-schema: v1.2 -->` y su huella.

### 3.2 Precisión en relevo aparte, con otro rol

En el smoke, `roles.editora_mesa` y `roles.documentalista` apuntan a **stubs
distinguibles**. Se verifica que `decisions.jsonl` registra:

- `review-1` con `role == "editora_mesa"`
- `review-4` con `role == "documentalista"`

Es la regla dura **voz ≠ precisión** hecha aserción.

### 3.3 Degradación grácil (AS-4)

Fixture con la combinada a medias (solo bloques 1 y 2):

```bash
python3 writeonmars/scripts/status.py --json --project-dir "$HALF" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["next_step"]=="review"; print("OK")'
```

Y el ejecutor despacha `review-3` (no se atasca):

```bash
cd vivarium && cargo test choose_review_action   # cubre la primera pasada ausente
```

### 3.4 Hallazgos accionables (AS-3)

Con un hallazgo `critico` o `medio` abierto en cualquiera de los dos relevos:

- `mode: produccion` → `next_step == "revise"`.
- `mode: estudio` → `next_step == "dispose"` (checkpoint humano, exit 10).

### 3.5 Matriz `corta` + `estudio` (AS-5, SC-005)

```bash
bash tests/smoke/corta-e2e.sh   # incluye la variante estudio
```

Se verifica que el ejecutor se detiene en `write`, `dispose` y `feedback`
(exit 10) sin despachar redacción, que **no** hay checkpoint `intro`, que las
huellas sha256 aplican igual, y que el guardarraíl exit 11 sigue intacto.

---

## 4. US3 — Escalar sin tirar trabajo

**Lo que se afirma**: el escalado conserva el 100 % del trabajo, queda registrado
con actor humano, y el des-escalado ilegal se rechaza.

### 4.1 Escalar (AS-1, SC-004)

Partiendo del fixture corta con la pieza aprobada:

```bash
python3 writeonmars/scripts/track.py --escalar --project-dir "$P" --json
```

```bash
python3 - <<'PY'
import json, pathlib
m = json.load(open(f"{P}/.writeonmars-manifest.json"))
assert m["track"] == "estandar"
h = m["track_history"][-1]
assert h["from"] == "corta" and h["to"] == "estandar"
assert h["actor"] and not h["actor"].endswith("@agents.writeonmars.invalid")
assert h["date"].endswith("Z")
print("OK escalado registrado")
PY
```

Conservación (ningún archivo movido):

```bash
git -C "$P" status --porcelain   # solo .writeonmars-manifest.json modificado
```

Tras ampliar el temario a 4 filas a mano:

```bash
python3 writeonmars/scripts/status.py --json --project-dir "$P" \
  | python3 -c '
import json,sys; d=json.load(sys.stdin)
assert d["chapters_expected"] == 4
assert d["by_chapter"]["1"]["approved"] is True      # el capítulo 1 conserva approved
assert d["pending_chapters"] == [2,3,4]
print("OK trabajo conservado")'
```

### 4.2 Des-escalado ilegal (AS-2)

```bash
python3 writeonmars/scripts/track.py --desescalar --project-dir "$P"; echo $?   # → 1
# mensaje: "el temario tiene 4 filas; la pista corta exige pieza única"
```

Con capítulos 2+ en disco pero temario de 1 fila:

```bash
# → 1, "existen capítulos fuera de pieza única: 2, 3"
```

Des-escalado **legal** (proyecto legado sin `track`, temario ≤ 1 fila, sin
capítulos 2+): exit 0 y entrada en `track_history` con `from: "estandar"`.

### 4.3 Ningún agente escala (AS-3)

```bash
git -C "$P" config user.name  "redactora"
git -C "$P" config user.email "redactora@agents.writeonmars.invalid"
python3 writeonmars/scripts/track.py --escalar --project-dir "$P"; echo $?   # → 3
```

Sin `user.name` configurado: también exit 3.

### 4.4 Atomicidad

Simular fallo en la escritura (permisos, `os.replace` interceptado): el
manifiesto conserva sus bytes originales y no queda ningún `.tmp` huérfano.

---

## 5. Edge cases de la spec

| Caso | Comprobación | Resultado esperado |
|---|---|---|
| Pieza que crece sin escalar (`chapters/02-*.md` con temario de 1) | `status.py --json` | `warnings` gana la entrada de "capítulos fuera de pieza única"; `next_step`, `gates` y `closeable` **sin cambios**. No bloquea. |
| `track: corta` con temario editado a 3 filas | `status.py --json` | `warnings` gana la entrada de temario. `track.py --check` → exit 1 |
| Brief compacto sin firmar | `status.py --json` | `next_step == "specify"`; `plan.md` **no** existe; `chapters_expected == 0` |
| Combinada y precisión en el mismo modelo | smoke con stubs distinguibles | `decisions.jsonl` registra roles distintos; si no, el smoke falla |
| Proyecto legado sin `track` que quiere ser corta | `track.py --desescalar` | exit 0 si temario ≤ 1 fila y sin capítulos 2+ |
| `plan.md` regenerado a mano en corta | `speckit.plan` | preserva `## Temario` existente (cláusula del comando) |

---

## 6. `corta-e2e.sh` — contrato del smoke

Espejo de `tests/smoke/estudio-e2e.sh`. Convención de exit codes: `0` PASS,
`99` SKIP (sin `cargo`), otro FAIL. Alta en el array `tests=(...)` de
`tests/smoke/run-all.sh`.

Recorrido:

1. `WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia vivarium new …`
2. Verifica manifiesto (`track`, `sector`, `registro`) y adendas por referencia.
3. `vivarium run` → se detiene en el checkpoint `specify` (exit 10).
4. La operadora escribe `spec.md` **y** `plan.md` con el temario de una fila.
5. `vivarium run` → despacha `research`, `implement`, `review-1` (stub que emite
   los cuatro bloques), `review-4` (stub que emite bloque 4 + `claims.md`),
   `export`; se detiene en el checkpoint `feedback` (exit 10).
6. Verifica: **nunca** se despachó `plan`, `constitution`, `review-3`,
   `review-5` ni `intro`; el PDF existe; el HTML no tenía índice.
7. `feedback_intake.py` → `vivarium run` → `close` (exit 0).
8. Cuenta despachos en `decisions.jsonl`: **≤ 8**.
9. Repite el recorrido en `mode: estudio`: el ejecutor se detiene en `write`,
   `dispose` y `feedback`; jamás despacha `implement`, `revise` ni `intro`;
   guardarraíl exit 11 intacto.
10. `track.py --escalar` sobre el proyecto cerrado: manifiesto actualizado, el
    resto del disco intacto.

Los stubs son deterministas y **distinguibles por rol**: el stub de
`editora_mesa` escribe los bloques 1·2·3·5; el de `documentalista`, el 4 y
`claims.md`. Así el smoke prueba `voz ≠ precisión` estructuralmente.
