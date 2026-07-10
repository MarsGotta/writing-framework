# Implementation Plan: Pista corta editorial (ceremonia adaptativa)

**Branch**: `main` (feature fijada por `.specify/feature.json` → `specs/006-pista-corta-editorial`) | **Date**: 2026-07-10 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/006-pista-corta-editorial/spec.md`

> **LA IMPLEMENTACIÓN LA HARÁ UN AGENTE DISTINTO DEL QUE REDACTÓ LA SPEC.**
> Este plan es autocontenido y agente-neutral (Principio VI): no depende de
> skills de ningún proveedor. Todo criterio de aceptación es verificable por
> script. Ante ambigüedad, mandan los contratos de `contracts/` y las
> decisiones de `research.md`.

## Summary

El método cobra hoy una sola ceremonia, dimensionada para libro. Esta feature
añade una **pista** (`track`) al manifiesto: `estandar` (lo actual) o `corta`
(pieza única). La pista corta **degenera artefactos** en lugar de eliminar
garantías: temario de una fila materializado por la firma del brief, revisión
en dos relevos (combinada 1·2·3·5 + precisión 4), sin paso `plan`, sin
`constitution` y sin `intro`, con export de pieza única.

El hallazgo que ordena todo el diseño: **la brújula y el ejecutor ya saben
recorrer la pista corta sin cambiar de lógica**. `status.py:_next_step` devuelve
`constitution` solo si `manifest.sector` es falsy, y `plan` solo si
`chapters_expected == 0`; `runner.rs:choose_review_action` despacha la primera
pasada ausente del rango 1..4, y `runner.rs:plan_global` omite `review-5` si ya
existe un bloque de pasada 5. Fijar el sector en `bootstrap`, materializar una
fila de temario y registrar los bloques 1·2·3·5 en un solo run bastan para que
los cuatro pasos desaparezcan. La feature se reduce entonces a: un campo de
manifiesto, un script de escalado, comandos conscientes de pista, un export
compacto y **un único cambio de comportamiento en el ejecutor** (saltar `intro`).

El precedente ya existe en el método: `speckit.review-structure` emite hoy
**dos** bloques (`## Pasada 1` y `## Pasada 2`) en una sola ejecución. La pasada
combinada no inventa un contrato; extiende ese precedente a 1·2·3·5.

## Technical Context

**Language/Version**: Python 3.9+ (scripts del preset, stdlib; `track.py` invoca
el binario `git` como `dispose.py`); Rust 1.75 (`vivarium-core`);
Bash 3.2-compatible (smoke, por el `/bin/bash` de macOS).
**Primary Dependencies**: ninguna nueva. Preset: stdlib. Vivarium: las del
workspace existente.
**Storage**: archivos del proyecto editorial — `.writeonmars-manifest.json`
(campos nuevos `track` y `track_history`; schema sube a v1.4.0),
`specs/<feature>/plan.md` (§ Temario, ya leído por `count_temario`),
`findings.md` (esquema pass-output v1.2, **sin cambios**), `claims.md`.
**Testing**: `uvx --with pytest --with pyyaml --with jsonschema python -m pytest
tests/unit -q` (el `python3` del sistema no trae pytest; CI y CLAUDE.md lo
abrevian como `python3 -m pytest tests/unit`); `bash tests/smoke/run-all.sh`
(nuevo `corta-e2e.sh`, convención skip 99 sin cargo);
`cd vivarium && cargo test --workspace`.
**Baseline verificado** (2026-07-10, antes de tocar nada): **169 tests unitarios
en verde**. La mudanza a `findings_lib.py` (R10) debe conservar esa cifra sin
editar una sola aserción.
**Target Platform**: macOS + Linux, CLI.
**Project Type**: software (preset + ejecutor). Sin secciones editoriales
(Temario / Descripciones encadenadas no aplican: esta feature no produce prosa).
**Performance Goals**: `status.py` sigue siendo instantáneo; `track.py` es O(1)
sobre el manifiesto más una lectura de `plan.md` y un `glob` de `chapters/`.
**Constraints**: retrocompatibilidad total sin `track` o con `track: estandar`
(FR-010, espejo de FR-011 de la 005: ninguna aserción existente se edita);
`status.py` no cambia su lógica de estado (SC-003); el contrato `pass-output`
no se toca (FR-005); el ejecutor solo cambia en `plan_global` (FR-007).
**Scale/Scope**: 1 script nuevo (`track.py`), 3 scripts extendidos
(`bootstrap.py`, `status.py`, `export.py`), 1 helper compartido ampliado
(`findings_lib.py`), 1 schema a v1.4.0, ~6 comandos con cláusula de pista,
1 plantilla de assets nueva, 2 archivos de `vivarium-core`, 1 enmienda de
constitución (MINOR), ~4 archivos de test nuevos + 1 smoke.

## Constitution Check

*GATE: pasa antes de Phase 0. Re-evaluado tras Phase 1 — sin cambios.*

Constitución vigente: `.specify/memory/constitution.md` v1.6.1 → esta feature la
enmienda a **v1.7.0** (MINOR, sección "Pistas de ceremonia", FR-011).

| Principio | Conformidad | Evidencia |
|-----------|-------------|-----------|
| **I. Voz natural y sobria** (NO NEGOCIABLE) | pasa | Feature de tooling; no produce prosa del manuscrito. Los mensajes nuevos (`track.py`, warnings de `status.py`) siguen el tono sobrio existente. |
| **II. Estructura situación → explicación → consecuencia** | pasa (N/A editorial) | Sin capítulos nuevos. La plantilla didáctica no se toca. En pista corta la pieza única sigue aplicando la estructura del sector. |
| **III. Brief obligatorio** (NO NEGOCIABLE) | pasa | El checkpoint humano 1 se conserva intacto (FR-003). El brief compacto **añade** dos campos firmables (título, promesa); no retira ninguno de los ocho descriptivos. El temario degenerado no se materializa sin firma. |
| **IV. Precisión léxica** | pasa | Términos nuevos definidos una sola vez en `data-model.md`: pista de ceremonia, temario degenerado, pasada combinada, registro de escalado. |
| **V. Revisión multi-pasada** (NO NEGOCIABLE) | pasa — **con enmienda declarada** | Las cinco dimensiones se verifican íntegras en pista corta (SC-002: bloques 1-5 en `findings.md`). Lo que cambia es el *modelo de ejecución* del Principio V ("3 locales + 1 global"), que en pista corta pasa a "1 combinada + 1 de precisión". Esa expansión es exactamente la enmienda MINOR de FR-011. Las tres reglas duras se preservan: **voz ≠ precisión** (la dimensión 3 va en la combinada, la 4 en relevo aparte con otro rol/modelo), **escribe-uno-revisa-otro** (Redactora escribe; Mesa y Documentalista revisan), **detector ≠ corrector**. |
| **VI. Neutralidad de agente y modelo** (NO NEGOCIABLE) | pasa | Lo determinista va a scripts (`track.py`, `bootstrap.py`, `export.py`); el juicio, a comandos Markdown. El ejecutor solo mapea: su único cambio de comportamiento es omitir un paso. Las adendas por sector se aplican **por referencia** (R2) para no meter juicio en un script determinista. |
| **Modo de proyecto** (§ Modos de proyecto) | pasa | La pista es ortogonal al modo (FR-009). En `corta`+`estudio`, los checkpoints `write`/`dispose`, las huellas sha256 y el guardarraíl exit 11 operan sin cambios. Ninguna tarea del plan redacta prosa. |
| **Pista de ceremonia** (§ nueva, v1.7.0) | pasa — es el objeto de la feature | La pista gobierna *cuánto rito*; el modo, *quién escribe*. Defaults opinados sin candados; el cambio de pista es acción humana registrada (`track.py`, identidad git humana obligatoria). |

**Enmienda constitucional como parte de la feature**: la conformidad del
Principio V está condicionada a que la enmienda v1.7.0 se publique **antes** que
el código que la ejerce. Por eso la fase 1 del orden de implementación son los
contratos y la constitución. Ningún NO NEGOCIABLE se debilita: la enmienda
amplía el modelo de ejecución sin retirar ninguna de las cinco dimensiones ni
ninguna de las tres reglas duras.

Sin desviaciones → **Complexity Tracking vacío**.

## Project Structure

### Documentation (this feature)

```text
specs/006-pista-corta-editorial/
├── plan.md              # Este archivo
├── research.md          # R1-R10: decisiones fijadas (Phase 0)
├── data-model.md        # track, track_history, temario degenerado, pasada combinada, JSON de status
├── quickstart.md        # Recorrido de validación por escenario (US1, US2, US3, matriz track × mode)
├── contracts/
│   ├── manifest-v1.4.0-delta.md   # Delta del manifiesto: track + track_history
│   ├── track-cli.md               # Contrato CLI de track.py + deltas de bootstrap.py / status.py / export.py
│   └── ceremonia-corta.md         # Contrato de la pista: pasada combinada, comandos, delta del ejecutor
└── tasks.md             # Output de /speckit-tasks
```

### Source Code (repository root)

```text
writeonmars/
├── scripts/
│   ├── findings_lib.py  # EXTENDER: project_track(), count_temario(), drafted_ordinals()  [movidos desde status.py]
│   ├── bootstrap.py     # EXTENDER: --track / --sector (+ env WRITEONMARS_TRACK / WRITEONMARS_SECTOR); adendas por referencia
│   ├── status.py        # MÍNIMO: expone `track` en --json + warnings de coherencia. Lógica de estado INTACTA (SC-003)
│   ├── track.py         # NUEVO: escalado / des-escalado humano (contracts/track-cli.md § 1)
│   └── export.py        # EXTENDER: portada compacta + sin índice cuando track == corta
├── contracts/
│   ├── manifest-schema.json        # v1.3.0 → v1.4.0 (MINOR): track + track_history
│   └── executor-contract.md        # AÑADIR § 7 "Pista corta" (ceremonia-corta.md § 4)
│   # pass-output-schema.md         # NO SE TOCA (FR-005)
├── assets/
│   ├── cover-compact.html.template # NUEVO: portada de pieza única (título, autora, fecha)
│   └── style.css                   # AÑADIR clase .cover-compact (reusa @page cover)
├── commands/
│   ├── speckit.specify.md          # Pista corta: ronda compacta (8 campos + título + promesa) → temario degenerado
│   ├── speckit.research.md         # Pista corta: research exprés acotado a los conceptos del brief
│   ├── speckit.review-structure.md # Pista corta: vehicula la pasada combinada (bloques 1·2·3·5 en un run)
│   ├── speckit.review.md           # Pista corta: agrupado = combinada + precisión
│   ├── speckit.review-voice.md     # Cláusula: red de reparación en pista corta
│   ├── speckit.review-global.md    # Cláusula: red de reparación en pista corta
│   ├── speckit.intro.md            # Cláusula: NO aplica en pista corta
│   └── speckit.constitution.md     # Cláusula: opcional en pista corta (bootstrap --sector ya fija adendas)
├── memory/constitution.md          # SINCRONIZAR con .specify/memory/constitution.md (v1.7.0)
├── templates/plan-template.md      # SINCRONIZAR: Constitution Check gana la fila "Pista de ceremonia"
├── AGENTS.md                       # Contrato del agente: sección de pista
└── docs/how-to-pista-corta.md      # NUEVO: guía de la operadora (declarar pista, escalar)

.specify/
├── memory/constitution.md          # v1.6.1 → v1.7.0 (§ "Pistas de ceremonia", sync impact report en cabecera)
└── templates/plan-template.md      # ídem que el del preset

vivarium/crates/vivarium-core/src/
├── sidecar.rs           # Status gana `track: Option<String>` con #[serde(default)] — fontanería
└── runner.rs            # is_corta(status) + plan_global omite el bloque intro/README. ÚNICO cambio de comportamiento

tests/
├── unit/
│   ├── test_track.py            # NUEVO: escalado, des-escalado ilegal, identidad humana, atomicidad
│   ├── test_bootstrap.py        # AMPLIAR: --track / --sector, env vars, sector inexistente
│   ├── test_status.py           # AMPLIAR: `track` en --json; dashboard byte-idéntico
│   ├── test_status_corta.py     # NUEVO: fixture corta → approved/closeable con el parser actual
│   └── test_export.py           # AMPLIAR: portada compacta, sin índice
├── fixtures/006-corta/          # NUEVO: proyecto corta (produccion) + variante estudio
└── smoke/
    ├── corta-e2e.sh             # NUEVO: quickstart §§ 2-5 con stubs (skip 99 sin cargo)
    └── run-all.sh               # AÑADIR corta-e2e.sh al array `tests=(...)`
```

**Structure Decision**: opción "single project" adaptada al monorepo real —
método en `writeonmars/`, ejecutor en `vivarium/`, tests en `tests/`. Misma
partición que las features 004 y 005.

## Diseño (resumen ejecutable; detalle en research.md y contracts/)

### 1. El campo `track` y su historial

`manifest-schema.json` sube a **v1.4.0** (MINOR, aditivo): `track`
(`estandar` | `corta`, ausencia = `estandar`) y `track_history` (array
append-only). `findings_lib.project_track(manifest) -> str` es el gemelo exacto
de `project_mode`: ausencia/None ⇒ `estandar`; valor desconocido ⇒ `ValueError`.

`track_history` **no es espejo exacto** de `mode_history`: FR-008 exige `actor`
humano, que `mode_history` no registra. Divergencia documentada en
`data-model.md` § 2 y en el delta del schema.

### 2. Los cuatro pasos que desaparecen — y por qué salen gratis

| Paso omitido | Mecanismo | Fichero:línea que ya lo permite |
|---|---|---|
| `constitution` | `bootstrap --sector` deja `manifest.sector` no nulo | `status.py:384` (`if not manifest.get("sector")`) |
| `plan` | el brief firmado materializa 1 fila de temario ⇒ `chapters_expected == 1` | `status.py:389` (`if expected == 0`) |
| `review-2`, `review-3`, `review-5` | la combinada registra sus bloques; el ejecutor busca la primera pasada ausente | `runner.rs:265` y `runner.rs:282` |
| `intro` | **único cambio real**: `plan_global` salta el bloque `README.md` si `track == corta` | `runner.rs:291` |

Nada de esto toca `_next_step`, `_build_by_chapter`, `choose_review_action` ni
`effect_satisfied`.

### 3. `bootstrap.py` — pista y sector al crear el proyecto

Nuevos argumentos, simétricos con el `--mode` existente:

- `--track {estandar,corta}`, default `os.environ.get("WRITEONMARS_TRACK", "estandar")`.
- `--sector <slug>`, default `os.environ.get("WRITEONMARS_SECTOR")` (None ⇒ comportamiento actual: `sector: null`).

Con `--sector`: valida que existe `references/sectores/<slug>.md` (si no, falla
claro), escribe `sector` y `registro` en el manifiesto (el registro se lee del
propio manifiesto del sector, ver R2) y materializa un **bloque de adendas por
referencia** tras el centinela `<!-- WRITEONMARS:ADENDAS -->`. El script no
destila prosa: declara sector, base aplicada, registro y núcleo vigente, y
remite a `references/sectores/<slug>.md` (R2). `/speckit-constitution` sigue
disponible para calibrar tono, anglicismos y matices a mano.

**Ni `bootstrap.rs` ni `run_sidecar_action` cambian**: `vivarium new` invoca
`bootstrap.py` sin `--track`/`--sector`, y las variables de entorno viajan al
proceso hijo. Esa es la vía por la que el smoke crea un proyecto corta sin tocar
el ejecutor (FR-007).

### 4. El temario degenerado

`speckit.specify` en pista corta hace **una sola ronda** de preguntas: los ocho
campos descriptivos más **título** y **promesa** de la pieza. Al firmar el
brief (checkpoint humano 1, intacto), escribe `specs/<feature>/plan.md` con una
sección `## Temario` de una fila:

```markdown
## Temario

| Número | Título | Promesa | Estructura aplicada |
|--------|--------|---------|---------------------|
| 1 | <título firmado> | <promesa firmada> | didactica_v1 |
```

Título y promesa se copian **tal cual** de los campos firmados (clarificación
2026-07-09): el agente no los reescribe. `count_temario` lee esa tabla sin
cambios, `chapters_expected` pasa a 1 y el paso `plan` desaparece.

Orden en `_next_step`: `research` se evalúa **antes** que `expected == 0`, así
que el ciclo queda `specify → research → implement`, sin `plan` intermedio.

### 5. La pasada combinada

`speckit.review-structure` se vuelve consciente de pista. En `corta` verifica y
registra **cuatro bloques** en un único run: `## Pasada 1 — Estructura`,
`## Pasada 2 — Utilidad`, `## Pasada 3 — Naturalidad` (todos con
`Capítulos cubiertos: 1`) y `## Pasada 5 — Formato` (con `Capítulos cubiertos:
global`). Cada bloque es indistinguible de uno emitido por su comando suelto:
mismos campos, misma huella, `pass-output-schema: v1.2` sin cambios.

Esto **no es un contrato nuevo**: el comando ya emite hoy dos bloques (1 y 2) en
una sola ejecución. La coherencia entre capítulos (la otra mitad de la dimensión
5) es vacua en pieza única; la dimensión de formato se verifica igual.

Consecuencia en el ejecutor, sin tocarlo: tras `review-1`, `choose_review_action`
encuentra las pasadas 1, 2 y 3 hechas y despacha `review-4` (precisión) al rol
**Documentalista** — otro modelo. `voz ≠ precisión` sobrevive. Y `plan_global`
encuentra el bloque 5 ya presente y no despacha `review-5`.

Los comandos sueltos (`review-voice`, `review-global`, `review-precision`) quedan
como **red de reparación** (FR-006): si la combinada se queda a medias, rellenan
los huecos. La combinada es una comodidad, no un punto único de fallo.

### 6. `status.py` — mínimo indispensable

Dos cambios, ninguno en la lógica de estado (SC-003):

1. `evaluate()` añade la clave `"track"` al dict de salida (aditiva, junto a
   `"mode"`).
2. `warnings` gana dos entradas **advisory** cuando `track == corta`:
   temario con más de una fila, y capítulos con ordinal ≥ 2 en disco.

Ninguna de las dos toca `next_step`, `next_detail`, `gates`, `closeable` ni
`by_chapter`. `print_dashboard` sigue produciendo salida byte-idéntica en
proyectos `estandar` (R4). El delta de `--json` es exactamente una clave.

`count_temario` y `_drafted_ordinals` se **mueven** a `findings_lib.py` (con
alias finos en `status.py` para no romper importadores ni tests) porque
`track.py` los necesita para validar el des-escalado. Refactor sin cambio de
salida.

### 7. `track.py` — el escalado, patrón `dispose.py`

Único camino para cambiar de pista. Reusa la identidad humana de `dispose.py`
(git config `user.name`/`user.email`, rechaza `*@agents.writeonmars.invalid`,
exit 3), valida legalidad y escribe el manifiesto de forma atómica
(`os.replace` con rollback).

- `--escalar` (`corta → estandar`): siempre legal. **No mueve un solo archivo**:
  el brief sigue donde está, la pieza ya es `chapters/01-*.md` (capítulo 1 del
  temario ampliado), y `findings.md`/`claims.md` conservan sus bloques. La
  conservación del trabajo es *emergente*, no una migración: la humana amplía el
  temario a N filas y `status.py` pide los capítulos 2..N manteniendo el
  `approved` del 1. Eso es lo que verifica SC-004.
- `--desescalar` (`estandar → corta`): legal solo si el temario tiene ≤ 1 fila y
  no hay capítulos con ordinal ≥ 2. Si no, exit 1 con mensaje claro.
- `--check`: valida coherencia `track` ↔ temario ↔ `chapters/`. Exit 1 si la
  pista corta declara pieza única y el disco dice otra cosa.

Ningún agente cambia `track`: misma política que `mode`.

### 8. `export.py` — pieza única

Cuando `project_track(manifest) == "corta"`:

- Portada compacta desde `assets/cover-compact.html.template` (título, autora,
  fecha) en lugar de `cover.html.template`. La autora sale de
  `manifest.human_operators[0]`; la fecha, de `--meta` (default: año actual).
- **Sin índice**: no se invoca `build_toc()`.
- La sección Fuentes conserva el estilo `.chapter-sources` (`wrap_chapter_sources`
  no se toca), y la validación contra `claims.md` sigue idéntica.
- `README.md` ya era condicional (`if readme.exists()`), así que su ausencia no
  requiere cambio.

### 9. Vivarium — el único cambio de comportamiento

`sidecar.rs`: `Status` gana `track: Option<String>` con `#[serde(default)]`
(tolerante a `status.py` antiguos). Fontanería de deserialización.

`runner.rs`: helper `is_corta(status)` espejo de `is_estudio(status)`, y en
`plan_global` el bloque `if !project.join("README.md").is_file()` queda guardado
por `if !is_corta(status) && ...`. El salto aplica **en ambos modos**: en
`corta`+`estudio` no hay checkpoint `intro` porque no hay README que escribir
(R6). `writes_manuscript`, `blocked_by_mode` y el guardarraíl exit 11 no se
tocan.

No hay `vivarium track set`: el escalado vive en el preset (`track.py`), como
manda el Principio VI.

### 10. Recuento de despachos (SC-001)

Medido en `decisions.jsonl` sobre registros `event == "dispatch"`, tras
`vivarium new` (que hace el bootstrap fuera del runner) y con 0 ciclos de
`revise`:

| # | Pista corta | Pista estándar (misma pieza) |
|---|---|---|
| 1 | — (`constitution` omitido: sector fijado) | `constitution` |
| 2 | `research` | `research` |
| 3 | — (`plan` omitido: temario degenerado) | `plan` |
| 4 | `implement` cap 1 | `implement` cap 1 |
| 5 | `review-1` **combinada** (bloques 1·2·3·5) | `review-1` (bloques 1·2) |
| 6 | — | `review-3` |
| 7 | `review-4` precisión | `review-4` precisión |
| 8 | — (bloque 5 ya registrado) | `review-5` global |
| 9 | — (`intro` omitido) | `intro` |
| 10 | `export` | `export` |
| 11 | `close` | `close` |
| | **6 despachos** | **11 despachos** |

Los dos checkpoints humanos (`specify`, `feedback`) no son despachos: los
registra `append_checkpoint_once` con `event == "checkpoint"`. El umbral de
SC-001 (≤ 8) queda con **2 despachos de margen**; el `setup` cuenta como séptimo
si el proyecto se crea sin `vivarium new`. La estimación de "~13 pasos" de la
spec incluye checkpoints y `setup`; la cifra dura y verificable es la de esta
tabla.

## Orden de implementación sugerido

1. **Contratos y constitución primero** — fijan la verdad antes del código:
   enmienda v1.7.0 (§ "Pistas de ceremonia") en las **dos** copias, fila nueva
   en las **dos** copias de `plan-template.md`, `manifest-schema.json` v1.4.0,
   `executor-contract.md` § 7.
2. **`findings_lib.py`**: `project_track()` + mudanza de `count_temario` y
   `drafted_ordinals`. `pytest tests/unit` en verde sin editar aserciones.
3. **`bootstrap.py`** `--track`/`--sector` + adendas por referencia +
   `test_bootstrap.py`.
4. **`status.py`**: clave `track` + warnings; `test_status.py` (byte-identidad
   del dashboard) y `test_status_corta.py` con el fixture (US1 verde).
5. **Comandos** conscientes de pista (`specify` con temario degenerado,
   `review-structure` con la combinada, `review` agrupado, cláusulas en el
   resto) — US2 a nivel de contrato.
6. **`export.py`** + plantilla compacta + `style.css` + `test_export.py`.
7. **`track.py`** + `test_track.py` (US3).
8. **Vivarium**: `sidecar.rs` + `plan_global` + tests de `cargo`.
9. **`corta-e2e.sh`** + alta en `run-all.sh`; gates completos (SC-006).
10. **Docs**: `docs/how-to-pista-corta.md`, sección de pista en `AGENTS.md`,
    ROADMAP y CLAUDE.md.

Los pasos 2-4 desbloquean US1; el 5, US2; el 7, US3. El 8 puede correr en
paralelo al 5-7 (frontera dura por archivos).

## Riesgos y mitigaciones

- **Regresión en `estandar`**: mitigado por FR-010 como contrato (ninguna
  aserción existente se edita), campos JSON solo aditivos y toda verificación
  nueva condicionada a `track == corta`. `test_status.py` gana un caso de
  byte-identidad del dashboard.
- **La combinada se queda a medias** (el agente registra 1 y 2, no 3 ni 5): el
  ejecutor despacha `review-3` por su cuenta — `choose_review_action` busca la
  primera pasada ausente. Degradación grácil a ceremonia estándar, sin
  intervención. Es exactamente el escenario 4 de US2.
- **BYOM mal configurado** (combinada y precisión en el mismo modelo): misma
  exposición que hoy tiene el reparto Mesa/Documentalista. El smoke lo verifica
  con stubs distinguibles y los comandos lo declaran MUST.
- **Ejecutor antiguo ante un proyecto corta**: un `vivarium` sin el salto de
  `intro` pediría un `README.md` que nadie va a escribir → se queda esperando en
  el paso `intro`. Falla ruidosa y recuperable (la operadora escribe un README o
  actualiza el binario), no corrupción de estado. Documentado en
  `executor-contract.md` § 7.
- **`plan.md` sobrescrito por `/speckit-plan` core** en un proyecto corta: el
  temario degenerado vive en el mismo archivo que el plan de la feature. El
  camino feliz no despacha `plan`, pero una invocación manual lo pisaría. El
  comando `speckit.plan` gana una cláusula: en pista corta, **preservar** la
  sección `## Temario` existente.
- **Adendas por referencia percibidas como "sin adendas"**: el bloque escrito
  por `bootstrap --sector` es explícito sobre qué aplica y cómo calibrarlo. R2
  registra la alternativa descartada (extracción por encabezado) y por qué.

## Complexity Tracking

*Vacío: el Constitution Check no registra desviaciones.* La enmienda MINOR de la
constitución (v1.7.0) no es una desviación sino el procedimiento previsto en
§ Governance para expandir material normativo.
