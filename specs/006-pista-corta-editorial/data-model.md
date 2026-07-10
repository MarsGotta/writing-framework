# Data model — Pista corta editorial (feature 006)

**Fecha**: 2026-07-10 · Deriva de `spec.md` § Key Entities y de las decisiones
de `research.md`. Las entidades nuevas son **dos** (`track`, `track_history`);
las otras dos (temario degenerado, pasada combinada) son *formas degeneradas de
artefactos existentes*, no estructuras nuevas — y esa es la tesis de la feature.

---

## 1. `track` — pista de ceremonia

Cuánto rito paga el proyecto. Ortogonal al modo (`mode` decide *quién escribe*;
`track` decide *cuánto rito*).

**Dónde vive**: `.writeonmars-manifest.json`, campo raíz `track`.

| Propiedad | Valor |
|---|---|
| Tipo | `string` |
| Valores | `"estandar"` \| `"corta"` |
| Obligatorio | no |
| Ausencia | se interpreta como `"estandar"` |
| Valor desconocido | error duro, mensaje claro (espejo exacto de `mode`) |
| Quién lo escribe | `bootstrap.py` al crear; `track.py` al escalar. **Nunca un agente**, nunca a mano |

**Semántica por valor**:

- `estandar` — ceremonia completa actual: adendas → brief → research → temario →
  redacción por capítulo → 3 pasadas locales + 1 global → intro → export →
  feedback → close.
- `corta` — pieza única: temario degenerado de una fila, dos relevos de revisión
  (combinada 1·2·3·5 + precisión 4), sin paso `plan`, sin `constitution` en el
  camino feliz, sin `intro`. Export de pieza única.

**Accesor canónico** (`writeonmars/scripts/findings_lib.py`, gemelo de
`project_mode`):

```python
def project_track(manifest: dict | None) -> str:
    """Pista del proyecto: ausencia/None = estandar; valor desconocido → ValueError."""
    if manifest is None:
        return "estandar"
    track = manifest.get("track", "estandar")
    if track is None:
        return "estandar"
    if track not in {"estandar", "corta"}:
        raise ValueError("manifest.track debe ser 'estandar' o 'corta'")
    return track
```

Todo consumidor (`status.py`, `export.py`, `track.py`) usa este accesor. Ningún
script lee `manifest["track"]` directamente.

---

## 2. `track_history` — registro de escalado

Apéndice append-only del manifiesto con cada cambio de pista.

**Dónde vive**: `.writeonmars-manifest.json`, campo raíz `track_history`.

| Propiedad | Valor |
|---|---|
| Tipo | `array` de objetos |
| Obligatorio | no (ausencia = ningún cambio de pista registrado) |
| Quién lo escribe | **solo** `scripts/track.py`, de forma atómica |

**Forma de cada entrada**:

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `from` | `"estandar"` \| `"corta"` | sí | Pista anterior |
| `to` | `"estandar"` \| `"corta"` | sí | Pista nueva. `from != to` |
| `date` | `string` (date-time, UTC, `Z`) | sí | Instante del cambio |
| `actor` | `string` (no vacío) | sí | Identidad humana (`git config user.name`) |
| `email` | `string` (email) | no | `git config user.email` si existe |

Ejemplo:

```json
{
  "track": "estandar",
  "track_history": [
    {
      "from": "corta",
      "to": "estandar",
      "date": "2026-07-10T09:14:00Z",
      "actor": "Mars Gotta",
      "email": "mgotta@uoc.edu"
    }
  ]
}
```

### Divergencia deliberada respecto a `mode_history` (R8)

`mode_history` registra `{from, to, date}`. `track_history` añade `actor` (y
`email` opcional) porque FR-008 exige actor humano y `track.py` rechaza
identidades de agente (`*@agents.writeonmars.invalid`). La spec dice "espejo de
`mode_history`" refiriéndose a la **forma** —array append-only en el manifiesto,
escrito solo por script, nunca a mano—, no al conjunto de campos.

`mode_history` **no** se retro-modifica en esta feature.

---

## 3. Temario degenerado

No es una entidad nueva: es la tabla `## Temario` de
`specs/<###-feature>/plan.md` **con exactamente una fila**.

```markdown
## Temario

| Número | Título | Promesa | Estructura aplicada |
|--------|--------|---------|---------------------|
| 1 | <título firmado en el brief> | <promesa firmada en el brief> | didactica_v1 |
```

**Quién lo materializa**: `speckit.specify` en pista corta, **al quedar firmado
el brief** (checkpoint humano 1). No antes: nace del brief.

**Contenido**: título y promesa se copian **tal cual** de los dos campos
firmables que el brief compacto añade a los ocho descriptivos (clarificación
2026-07-09). El agente no los reescribe ni los "mejora".

**Consecuencias, todas emergentes** (ningún script cambia):

- `count_temario()` devuelve `1` ⇒ `chapters_expected == 1`.
- `status.py:_next_step` deja de devolver `plan` (su condición es `expected == 0`).
- `_build_by_chapter` construye la clave `"1"` y `all_chapters_approved` se
  evalúa sobre ella sola.
- `export.py:parse_temario()` obtiene título y promesa del capítulo 1 para la
  portada.

**Invariante**: `track == "corta"` ⟺ el temario tiene ≤ 1 fila y no existen
capítulos con ordinal ≥ 2. Romperlo produce `warnings` en `status.py` (R5) y
exit 1 en `track.py --check`.

---

## 4. Pasada combinada

No es una entidad nueva: es **un despacho que emite cuatro bloques pass-output
estándar**. El contrato `pass-output-schema` v1.2 no se toca (R7).

| Bloque emitido | Dimensión | `Capítulos cubiertos` | Huella |
|---|---|---|---|
| `## Pasada 1 — Estructura` | 1 | `1` | `{"1": "<sha256>"}` |
| `## Pasada 2 — Utilidad` | 2 | `1` | `{"1": "<sha256>"}` |
| `## Pasada 3 — Naturalidad` | 3 | `1` | `{"1": "<sha256>"}` |
| `## Pasada 5 — Formato` | 5 | `global` | `{"global": "<sha256>"}` |

La dimensión 4 (precisión) **no** va en la combinada: viaja en un relevo aparte,
con otro rol/modelo, y en `produccion` emite además `claims.md`. Es la regla
dura **voz ≠ precisión** del Principio V.

**Precedente**: `speckit.review-structure` ya emite hoy dos bloques (1 y 2) en
una sola ejecución. La combinada extiende ese precedente de dos a cuatro
dimensiones.

**Indistinguibilidad**: un bloque escrito por la combinada y uno escrito por su
comando suelto son idénticos byte a byte en estructura. `parse_findings` no
conoce el origen. Por eso la combinada es una comodidad, no un punto único de
fallo: si registra solo parte de sus bloques, `choose_review_action` despacha
los sueltos que falten y el proyecto converge igual.

---

## 5. Contrato de estado — `status.py --json`

**Único campo nuevo**, aditivo:

```json
{
  "spec": "001-mi-pieza",
  "mode": "produccion",
  "track": "corta",
  "chapters_expected": 1,
  "...": "resto sin cambios"
}
```

| Campo | Tipo | Valores | Notas |
|---|---|---|---|
| `track` | `string` | `"estandar"` \| `"corta"` | Siempre presente. Nunca `null`: la ausencia en el manifiesto se resuelve a `"estandar"` |

`warnings` (lista de `string`, ya existente) gana hasta dos entradas advisory en
pista corta (R5). No hay ningún otro cambio: `next_step`, `next_detail`, `gates`,
`closeable`, `by_chapter` y `all_chapters_approved` conservan su lógica exacta.

`print_dashboard()` **no cambia**: la salida humana de un proyecto `estandar` es
byte-idéntica a la anterior a esta feature (R4).

### Deserialización en el ejecutor

`vivarium/crates/vivarium-core/src/sidecar.rs`:

```rust
pub struct Status {
    // …
    #[serde(default)]
    pub track: Option<String>,
    // …
}
```

`#[serde(default)]` mantiene la tolerancia a `status.py` antiguos (`None` ⇒ el
helper `is_corta()` devuelve `false` ⇒ ceremonia estándar).

---

## 6. Máquina de estados de la pista

```
                    bootstrap --track corta
                              │
                              ▼
                        ┌──────────┐
   track.py --escalar   │  corta   │
        ┌───────────────┤          │
        │               └──────────┘
        │                     ▲
        ▼                     │ track.py --desescalar
  ┌──────────┐                │ (solo si temario ≤ 1 fila
  │ estandar │────────────────┘  y sin capítulos ordinal ≥ 2)
  └──────────┘
        ▲
        │ bootstrap (default, o --track estandar, o ausencia del campo)
```

**Transiciones legales**:

| Desde | Hacia | Condición | Efecto |
|---|---|---|---|
| `corta` | `estandar` | siempre | Escribe `track` + entrada en `track_history`. **No mueve ningún archivo** |
| `estandar` (o ausente) | `corta` | temario ≤ 1 fila **y** sin `chapters/NN-*.md` con `NN ≥ 2` | Escribe `track` + entrada en `track_history` |
| `X` | `X` | — | Rechazado: exit 1, "el proyecto ya está en pista X" |

**Quién puede ejecutarlas**: solo una identidad humana. `track.py` deriva actor
y email de `git config` y rechaza (`exit 3`) si `user.name` está vacío o si
actor/email terminan en `@agents.writeonmars.invalid`. Misma política que el
cambio de modo: los defaults son opinados, no candados; el cambio es del humano
operador.

### El escalado conserva el trabajo sin migrarlo

`--escalar` **no toca el disco más allá del manifiesto**. La conservación es
emergente:

| Artefacto | Qué le pasa |
|---|---|
| Brief (`spec.md`) | Nada: sigue siendo el brief de la obra |
| La pieza (`chapters/01-*.md`) | Nada: ya es el capítulo 1 del temario ampliado |
| `findings.md` | Nada: sus bloques 1-5 siguen cubriendo el capítulo 1 |
| `claims.md` | Nada: sus claims siguen atribuidos al capítulo 1 |
| Pasadas registradas | `_build_by_chapter` recalcula: cap 1 conserva `approved` |
| Temario | La humana lo amplía a N filas; `status.py` pide los capítulos 2..N |

Eso es exactamente lo que verifica SC-004. No hay script de migración porque no
hay nada que migrar: el temario degenerado ya era un temario, y la pieza ya era
un capítulo.

---

## 7. Matriz `track × mode` (FR-009)

Las dos dimensiones son ortogonales. Los cuatro cuadrantes son válidos.

| | `mode: produccion` | `mode: estudio` |
|---|---|---|
| **`track: estandar`** | Ceremonia completa. La IA redacta. `intro` despachado a Redactora. | Ceremonia completa. La humana escribe. Checkpoints `write`, `dispose`, `intro`, `feedback`. |
| **`track: corta`** | Pieza única. La IA redacta. Combinada + precisión. `intro` omitido. **6 despachos.** | Pieza única escrita por la humana. Combinada + precisión producen **solo hallazgos**. Huellas sha256 y guardarraíl exit 11 intactos. Checkpoints `write`, `dispose`, `feedback`. `intro` omitido (R6). |

En `corta`+`estudio`:

- La pasada combinada y la de precisión NUNCA redactan prosa (cláusula de modo
  de `pass-output-schema` v1.2, sin cambios).
- Las huellas de la 005 se calculan y verifican igual: una pasada sin huella
  coincidente no cuenta y reabre el capítulo.
- La disposición de hallazgos sigue siendo humana (`dispose.py`).
- `claims.md` es opcional (constitución § Estándares editoriales, lente de modo).

---

## 8. Glosario de la feature

Un término por concepto (Principio IV, univocidad). Estos son los cuatro:

| Término | Definición |
|---|---|
| **Pista de ceremonia** (`track`) | Cuánto rito paga el proyecto: `estandar` o `corta`. Ortogonal al modo. |
| **Temario degenerado** | La tabla `## Temario` de `plan.md` con exactamente una fila, materializada por la firma del brief. |
| **Pasada combinada** | Un despacho que verifica y registra las dimensiones 1·2·3·5 como cuatro bloques pass-output estándar. |
| **Registro de escalado** (`track_history`) | Apéndice append-only del manifiesto con cada cambio de pista (de, a, fecha, actor humano). |

Prohibido: "modo corto" (colisiona con `mode`), "pista rápida" (colisiona con el
"camino rápido" de `speckit.constitution`), "revisión fusionada" (el término es
*pasada combinada*).
