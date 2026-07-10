# Contrato de la pista corta — comandos, pasada combinada y delta del ejecutor

**Feature**: 006-pista-corta-editorial · **Fecha**: 2026-07-10

Qué hace cada comando cuando el manifiesto declara `track: corta`, qué bloques
emite la pasada combinada y cuál es el único cambio admisible en el ejecutor.

**El contrato `pass-output-schema.md` no se modifica** (queda en v1.2). Esta
feature no abre ningún contrato de pasadas.

---

## 1. Cláusula de pista para los comandos

Todo comando afectado gana una sección `## Pista corta` que empieza así:

> Si el manifiesto declara `track: corta` (`.writeonmars-manifest.json`), …

Y si el comando no aplica en corta, una sección `## Pista corta` que dice
explícitamente que se auto-anula y por qué. Los comandos leen `track` del
manifiesto igual que hoy leen `mode`.

| Comando | Comportamiento en `track: corta` |
|---|---|
| `speckit.constitution` | **Opcional.** `bootstrap --sector` ya dejó sector, registro y adendas por referencia. Sigue disponible para calibrar tono, anglicismos y matices a mano. |
| `speckit.specify` | Ronda compacta: los 8 campos descriptivos **más título y promesa** de la pieza, en una sola tanda de preguntas. Al firmar, materializa el temario degenerado (§ 2). |
| `speckit.research` | Research exprés: acota el alcance a los conceptos obligatorios del brief. Sin panorama ni estado del arte. El contrato de citación se conserva **íntegro** (una cita por concepto; bloquea si alguno queda sin respaldo). |
| `speckit.plan` | No se despacha en el camino feliz. Si se invoca a mano, **MUST preservar** la sección `## Temario` existente: no la regenera ni la sobrescribe. |
| `speckit.implement` | Sin cambios (redacta el capítulo 1). En `mode: estudio` sigue auto-anulándose. |
| `speckit.review-structure` | **Vehicula la pasada combinada** (§ 2). Un único run verifica y registra las dimensiones 1·2·3·5. |
| `speckit.review` | Agrupado = combinada + precisión. Dos relevos, no cuatro. |
| `speckit.review-voice` | Red de reparación (FR-006): rellena el bloque 3 si la combinada lo dejó incompleto. |
| `speckit.review-global` | Red de reparación: rellena el bloque 5 si falta. |
| `speckit.review-precision` | Sin cambios: siempre es relevo aparte (dimensión 4). |
| `speckit.revise` | Sin cambios. |
| `speckit.intro` | **No aplica.** En pieza única no hay README de presentación. El comando se auto-anula explicando que `export.py` produce la portada compacta. |
| `speckit.export` | Sin cambios en la invocación; `export.py` detecta la pista. |

---

## 2. La pasada combinada

### 2.1 Quién la vehicula

El despacho existente de la **pasada 1** (`speckit.review-structure`,
`step: review-1`, rol `editora_mesa`). El ejecutor no cambia: ve el bloque 1
registrado y pasa a la 4 (clarificación 2026-07-09).

### 2.2 Qué registra

Cuatro bloques pass-output **estándar**, en un único run, en
`specs/<###-feature>/findings.md`:

| Bloque | Dimensión | `**Capítulos cubiertos**` | Huella |
|---|---|---|---|
| `## Pasada 1 — Estructura` | 1 | `1` | `<!-- huellas: {"1": "<sha256>"} -->` |
| `## Pasada 2 — Utilidad` | 2 | `1` | `<!-- huellas: {"1": "<sha256>"} -->` |
| `## Pasada 3 — Naturalidad` | 3 | `1` | `<!-- huellas: {"1": "<sha256>"} -->` |
| `## Pasada 5 — Formato` | 5 | `global` | `<!-- huellas: {"global": "<sha256>"} -->` |

Cada bloque lleva `<!-- pass-output-schema: v1.2 -->` y respeta la
`signing_matrix` del manifiesto (una pasada que exige firma `human` no se cierra
como `autonomous`).

`sha256` de los bloques 1-3 se calcula sobre los bytes actuales de
`chapters/01-*.md`. El de la pasada 5 es `sha256(concat(sha256(cap_i)))` en orden
ordinal, que con un solo capítulo es `sha256(sha256(cap_1))`.

### 2.3 Qué NO registra

La **dimensión 4 (precisión)**. Viaja en relevo aparte, con otro rol/modelo
(`documentalista`), y en `mode: produccion` emite además `claims.md`. Es la regla
dura **voz ≠ precisión** del Principio V: reescribir prosa y contrastar datos son
tareas opuestas que se degradan al mezclarse.

**MUST**: la configuración BYOM (`.vivarium/config.toml`) asigna
`roles.editora_mesa` y `roles.documentalista` a modelos distintos. Un ejecutor que
los colapse en el mismo modelo viola el Principio V.

### 2.4 Por qué la coherencia inter-capítulos no se pierde

La dimensión 5 tiene dos mitades: **formato** (cajas, títulos, bloques de texto,
índice navegable) y **coherencia entre capítulos** (sin contradicciones ni
redefiniciones, glosario consolidado, referencias cruzadas). En pieza única la
segunda mitad es vacua: no hay dos capítulos entre los que contradecirse. El
formato se verifica igual, en el bloque 5.

### 2.5 Por qué esto no abre el contrato

`speckit.review-structure.md` **ya emite hoy dos bloques** (`## Pasada 1` y
`## Pasada 2`) en una sola ejecución: *"cubre las dos dimensiones en una sola
ejecución, según el `signing_matrix`"*. El esquema pass-output nunca ató un
bloque a un proceso: ata un bloque a una **dimensión**. La combinada extiende ese
precedente de dos a cuatro dimensiones.

`parse_findings` no conoce el origen del bloque. `_passes_by_chapter` solo mira
las pasadas 1-4 para `approved`. `plan_global` solo comprueba que exista un
bloque de pasada 5. Nada distingue una combinada de cuatro pasadas sueltas.

### 2.6 Degradación grácil (US2, escenario 4)

La combinada es una **comodidad, no un punto único de fallo**. Si el agente se
queda a medias y registra solo los bloques 1 y 2:

- `choose_review_action` (`runner.rs:265`) encuentra la pasada 3 ausente y
  despacha `review-3` → `speckit.review-voice`.
- `plan_global` (`runner.rs:282`) encuentra la pasada 5 ausente y despacha
  `review-5` → `speckit.review-global`.

El proyecto converge a ceremonia estándar sin intervención humana y sin perder
ninguna dimensión. Los comandos sueltos siguen operativos como red de reparación
(FR-006).

---

## 3. Recuento de despachos (SC-001)

Sobre `decisions.jsonl`, registros con `event == "dispatch"`, camino feliz
(0 ciclos de `revise`), tras `vivarium new`:

| Paso | `corta` | `estandar` |
|---|---|---|
| `constitution` | omitido (sector fijado) | ✓ |
| `research` | ✓ | ✓ |
| `plan` | omitido (temario degenerado) | ✓ |
| `implement` cap 1 | ✓ | ✓ |
| `review-1` | ✓ combinada (1·2·3·5) | ✓ (1·2) |
| `review-3` | omitido | ✓ |
| `review-4` | ✓ precisión | ✓ |
| `review-5` | omitido (bloque ya presente) | ✓ |
| `intro` | omitido | ✓ |
| `export` | ✓ | ✓ |
| `close` | ✓ | ✓ |
| **Total** | **6** | **11** |

Los checkpoints humanos (`specify`, `feedback`) se registran con
`event == "checkpoint"` y no cuentan. El umbral de SC-001 es ≤ 8: quedan 2 de
margen (el `setup` sería el séptimo si el proyecto no se crea con `vivarium new`).

---

## 4. Delta del contrato del ejecutor — nueva § 7

Añadir a `writeonmars/contracts/executor-contract.md`:

```markdown
## 7. Pista corta

Delta para proyectos con `.writeonmars-manifest.json` declarando `track: corta`.

- `status.py --json` expone `track` (`"estandar"` | `"corta"`, siempre presente).
  El ejecutor MUST leerlo de ahí, nunca del manifiesto directamente.
- En etapa global, el paso `intro` **no aplica**: el ejecutor MUST NOT exigir
  `README.md` antes del export, en ningún modo. Una pieza única no tiene README
  de presentación; `export.py` produce la portada compacta.
- El ejecutor MUST NOT cambiar `track` ni ofrecer un comando para hacerlo. El
  escalado vive en `scripts/track.py` y exige identidad humana (Principio VI).
- Ningún otro cambio es admisible. En particular: la pasada combinada (un
  despacho que registra los bloques 1·2·3·5) es transparente para el ejecutor —
  ve el bloque 1 registrado y continúa por la primera pasada ausente, la 4.
- Un ejecutor sin este delta ante un proyecto corta se quedará esperando en el
  paso `intro` (pide un `README.md` que nadie escribirá). Falla ruidosa y
  recuperable, no corrupción de estado.

Campo garantizado adicional en `status.py --json`: `track`.
```

También actualizar § 3 ("Contrato de lectura de estado") añadiendo `track` a la
lista de campos garantizados.

---

## 5. Delta de `vivarium-core`

### 5.1 `sidecar.rs` — fontanería

```rust
pub struct Status {
    // …
    #[serde(default)]
    pub track: Option<String>,
    // …
}
```

`#[serde(default)]` mantiene la tolerancia a `status.py` antiguos.

### 5.2 `runner.rs` — el único cambio de comportamiento

```rust
fn is_corta(status: &Status) -> bool {
    status.track.as_deref() == Some("corta")
}
```

Y en `plan_global`, guardar el bloque del README:

```diff
-    if !project.join("README.md").is_file() {
+    if !is_corta(status) && !project.join("README.md").is_file() {
         if is_estudio(status) {
             return Ok(Planned::Checkpoint { step: "intro", … });
         }
         return Ok(Planned::Act(Action { step: "intro".to_string(), … }));
     }
```

El salto aplica en **ambos modos** (R6): en `corta`+`estudio` no hay checkpoint
`intro` porque no hay README que escribir. Un checkpoint sobre un artefacto que
el método declara inexistente sería un callejón sin salida.

### 5.3 Lo que NO se toca

`writes_manuscript`, `blocked_by_mode`, el guardarraíl exit 11,
`choose_review_action`, `effect_satisfied`, `plan_action`, `bootstrap.rs`,
`dispatch.rs`. No existe `vivarium track set`.

### 5.4 Tests de `cargo` exigidos

1. `plan_global_omite_intro_en_corta`: `Status { track: Some("corta"), … }` sin
   `README.md` y con bloque 5 → `Planned::Act(export)`, no `intro`.
2. `plan_global_omite_intro_en_corta_estudio`: además `mode: Some("estudio")` →
   `Planned::Act(export)`, **no** `Planned::Checkpoint { step: "intro" }`.
3. `plan_global_sigue_pidiendo_intro_en_estandar`: `track: None` → checkpoint o
   dispatch de `intro` según modo (regresión de los tests actuales
   `intro_global_es_checkpoint_en_estudio` y siguientes, que **no se editan**).
4. `status_sin_track_deserializa`: un JSON de `status.py` sin la clave `track`
   deserializa con `track == None`.

---

## 6. Matriz `track × mode` (FR-009)

| | `mode: produccion` | `mode: estudio` |
|---|---|---|
| `track: estandar` | Ceremonia completa; IA redacta; `intro` a Redactora | Ceremonia completa; humana escribe; checkpoints `write`, `dispose`, `intro`, `feedback` |
| `track: corta` | Pieza única; IA redacta; combinada + precisión; `intro` omitido | Pieza única escrita por la humana; combinada y precisión producen **solo hallazgos**; huellas sha256 y exit 11 intactos; checkpoints `write`, `dispose`, `feedback` |

En `corta`+`estudio` la cláusula de modo de `pass-output-schema` v1.2 aplica sin
cambios: prohibido editar `chapters/` o `README.md`; prohibido tocar `estado` de
hallazgos (eso es `dispose.py`). La combinada emite hallazgos, jamás prosa.
