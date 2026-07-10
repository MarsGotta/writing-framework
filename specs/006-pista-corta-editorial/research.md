# Research — Pista corta editorial (feature 006)

**Fecha**: 2026-07-10 · **Estado**: cerrado, sin `NEEDS CLARIFICATION` pendientes.

Este documento fija las decisiones que el plan da por resueltas. Ante cualquier
ambigüedad entre `spec.md` y el código, **manda este archivo**. Cada decisión
sigue el formato Decisión / Razón / Alternativas descartadas.

Las cinco preguntas de la sesión de clarificación (2026-07-09) ya están en
`spec.md` § Clarifications y no se repiten aquí; R1-R10 resuelven lo que quedó
abierto al aterrizar la spec sobre el código real.

---

## R1 — Los cuatro pasos omitidos no requieren tocar la brújula ni el ejecutor

**Decisión**: la pista corta se implementa sin modificar `_next_step`,
`_build_by_chapter`, `choose_review_action` ni `effect_satisfied`.

**Razón** (verificado en el código, 2026-07-10):

- `writeonmars/scripts/status.py:384` — `if not manifest.get("sector"): return
  "constitution"`. Fijar `sector` en `bootstrap` basta para omitir el paso.
- `writeonmars/scripts/status.py:389` — `if expected == 0: return "plan"`.
  Materializar una fila de temario basta para omitirlo. Y como la comprobación
  de `research.md` precede a esta, el orden queda `specify → research →
  implement`.
- `vivarium/crates/vivarium-core/src/runner.rs:265` —
  `choose_review_action` itera `for pass in 1..=4` y despacha la **primera
  ausente**. Si un run registra los bloques 1, 2 y 3, el siguiente despacho es
  la pasada 4 automáticamente.
- `vivarium/crates/vivarium-core/src/runner.rs:282` — `plan_global` solo
  despacha `review-5` `if !status.passes.iter().any(|p| p.num == 5)`. Si la
  combinada ya escribió el bloque 5, no lo despacha.

**Alternativas descartadas**: (a) una rama `if track == "corta"` en `_next_step`
— multiplicaría por dos los caminos de la brújula y rompería SC-003; (b) un
`next_step` nuevo (`combined-review`) — obligaría a cambiar el ejecutor y
rompería la retrocompatibilidad de FR-010.

---

## R2 — Adendas por referencia en `bootstrap --sector`

**Decisión**: `bootstrap.py --sector <slug>` escribe `sector` y `registro` en el
manifiesto y materializa, tras el centinela `<!-- WRITEONMARS:ADENDAS -->`, un
bloque de adendas **por referencia**: declara sector, base aplicada, registro y
núcleo vigente, y remite a `references/sectores/<slug>.md` para tono,
anglicismos, matices y relajaciones. No destila prosa. `/speckit-constitution`
sigue disponible para calibrar a mano y reescribe el bloque completo.

Forma exacta del bloque:

```markdown
<!-- WRITEONMARS:ADENDAS -->

## Adendas del proyecto

**Sector**: <Nombre> · **Base aplicada**: `references/sectores/<slug>.md`
**Registro (capa 2)**: `<registro-slug>` · Base aplicada:
`references/registros/<registro-slug>/SKILL.md`
**Núcleo vigente**: Write.OnMars Constitution v<X.Y.Z>
**Última edición de adendas**: <YYYY-MM-DD>

**Adendas aplicadas POR REFERENCIA.** Este proyecto adopta íntegros los valores
por defecto de la base del sector (tono calibrado, anglicismos admitidos,
matices léxicos, relajaciones estructurales, contrato terminológico inicial).
Las pasadas de revisión cargan `references/sectores/<slug>.md` directamente.

### Tono calibrado

**Por referencia**: el tono de esta guía es el de la sección
`## Tono por defecto` de `references/sectores/<slug>.md`, matizado por la
persona gramatical de su sección `## Persona gramatical y registro`. El marco
general lo pone el registro `<registro-slug>` (capa 2 de la pirámide de prosa).

Quien necesite el tono —el brief (`/speckit-specify`, campo 5, que lo refleja
como eco) y la pasada de naturalidad— lo lee de ahí. Para fijarlo literalmente
aquí, corre `/speckit-constitution`.

---

Para calibrar cualquiera de esos valores a mano, corre `/speckit-constitution`:
reescribe este bloque con las respuestas del cuestionario, sin tocar el núcleo.
```

**El encabezado `### Tono calibrado` es obligatorio, no decorativo.**
`writeonmars/commands/speckit.specify.md` (líneas 31-33) resuelve el campo 5 del
brief leyendo `.specify/memory/constitution.md → Tono calibrado` y, si no lo
encuentra, "sugiere correr `/speckit-constitution` primero" — justo el paso que
la pista corta omite. Sin ese encabezado, el checkpoint humano 1 se atasca en
pista corta y el Principio III queda sin satisfacer. `speckit.specify` gana la
instrucción de seguir el puntero hasta la base del sector cuando las adendas
estén por referencia. La pasada 3 (`speckit.review-voice.md`, líneas 26-28) ya
resuelve así su registro (`registro` del manifiesto, con el default del sector
como respaldo): esta decisión sigue ese precedente en lugar de inventar uno.

`registro` se obtiene del propio archivo del sector: la sección
`## Registro por defecto` abre con el slug entre backticks (en `tecnologia.md`,
`` `tecnico-divulgativo` ``). Si no se encuentra un slug, `registro` queda
ausente del manifiesto (campo opcional) y el bloque lo declara "sin registro
declarado".

Validación: si `references/sectores/<slug>.md` no existe, `bootstrap.py` falla
con exit 1 y mensaje claro listando los sectores disponibles.

**Razón**: `bootstrap.py` es un script determinista. Rellenar `[TONO]`,
`[ANGLICISMOS]`, `[MATICES]` y `[RELAJACIONES]` desde la prosa del sector exige
juicio — es precisamente el trabajo que el Principio VI manda dejar en comandos,
no en scripts. Aplicar por referencia entrega la capa normativa completa (las
pasadas ya cargan la base del sector) con cero juicio en el script, y satisface
FR-002 sin abrir contratos nuevos. La brújula omite `constitution` porque
`sector` deja de ser nulo, que es la condición literal de `status.py:384`.

**Alternativas descartadas**:

- *Extracción por encabezado* (copiar verbatim las secciones "Tono por defecto",
  "Anglicismos y extranjerismos admitidos"… a los marcadores mediante un mapa
  fijo): convertiría los encabezados de `references/sectores/*.md` en contrato.
  Un renombrado de sección rompería el bootstrap de todo proyecto nuevo, y el
  fallo sería silencioso (un marcador vacío). Coste de mantenimiento
  desproporcionado para una comodidad.
- *Solo manifiesto* (fijar `sector`/`registro` y no escribir adendas): la
  brújula omitiría `constitution` y el proyecto quedaría sin capa normativa
  escrita. La pasada 3 no tendría contra qué verificar el tono, y el centinela
  `WRITEONMARS:ADENDAS` no existiría — `bootstrap.py --force` perdería su punto
  de re-sellado.

*(Decisión de la operadora, sesión 2026-07-10.)*

---

## R3 — `--track` y `--sector` entran por variable de entorno en el camino del ejecutor

**Decisión**: `bootstrap.py` acepta `--track` y `--sector` como argumentos, con
defaults `os.environ.get("WRITEONMARS_TRACK", "estandar")` y
`os.environ.get("WRITEONMARS_SECTOR")`. Ni `vivarium/crates/vivarium-core/src/bootstrap.rs`
ni `run_sidecar_action` de `runner.rs` se modifican.

**Razón**: `vivarium new` invoca `bootstrap.py` pasando solo `--mode`
(`bootstrap.rs:195`), y el paso `setup` del runner lo invoca **sin argumentos**
(`runner.rs:445`). Las variables de entorno viajan al proceso hijo en ambos
casos, así que `WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia vivarium
new …` crea un proyecto corta sin tocar una línea del ejecutor. Es el mismo
patrón que `WRITEONMARS_MODE` ya usa, y mantiene FR-007 literal: el único cambio
admisible en el ejecutor es `plan_global`.

`argparse` no valida `choices` sobre el valor por defecto, así que `--track`
repite la comprobación explícita que `bootstrap.py:133` ya hace con `--mode`
(un `WRITEONMARS_TRACK` con typo debe fallar, no acabar escrito en el manifiesto).

**Alternativas descartadas**: añadir `vivarium new --track/--sector` — más
ergonómico, pero amplía el cambio del ejecutor más allá de lo que FR-007 permite
y acopla el ejecutor a un concepto del método. Queda como idea de roadmap.

---

## R4 — "Salida byte-idéntica" (SC-003) se refiere al dashboard humano

**Decisión**: `evaluate()` gana **exactamente una clave** en su dict de salida:
`"track"`, junto a `"mode"`. Por tanto `status.py --json` **no** es
byte-idéntico: gana una línea. Lo que sí es byte-idéntico en proyectos
`estandar` (o sin `track`) es la salida de `print_dashboard()`.

Criterio verificable, fijado en `quickstart.md` § 1:

- `python3 status.py --project-dir <fixture-estandar>` produce bytes idénticos
  antes y después de la feature (test de regresión con salida capturada).
- `python3 status.py --json --project-dir <fixture-estandar>` produce el mismo
  JSON más la clave `"track": "estandar"`, y ninguna otra diferencia
  (comparación de dicts, no de bytes).

**Razón**: FR-001 obliga a exponer `track` en `--json`; SC-003 exige salida
byte-idéntica. Ambas no pueden ser ciertas del mismo flujo. La lectura coherente
—y la que respeta el propósito de SC-003, que es "la brújula no cambió de
opinión"— es que `--json` gana un campo aditivo (como ya hizo `mode` en la 004)
y el dashboard no cambia ni un carácter.

### Consecuencia obligatoria: el oráculo de la 005 gana una clave

`tests/unit/test_status_estudio.py:78-81` (`test_oraculo_json_estudio`) compara
el dict **completo** de `--json` contra `tests/fixtures/005-estudio/expected-status.json`
(30 claves; tiene `mode`, no tiene `track`). Añadir la clave `track` **rompe ese
test**. No es un efecto colateral evitable: es la contrapartida exacta de FR-001.

El oráculo MUST ganar `"track": "estandar"` y **nada más**. Esa edición es de
*dato*, no de aserción: la aserción (`state == oracle`) no se toca, ni se
debilita, ni se relaja el conjunto de claves comparadas. La regla de FR-010
("ninguna aserción existente se edita") se lee como "ninguna aserción se
**debilita**"; congelar un contrato con una clave nueva lo refuerza.

Diff único admisible sobre el oráculo: **una línea, `"track": "estandar"`**. El
fichero se genera con `sort_keys=True`, así que la clave cae en su posición
alfabética (entre `spec` y `warnings`), no junto a `mode`:

```diff
   "spec": "001-estudio",
+  "track": "estandar",
   "warnings": []
```

Si un implementador se ve editando cualquier otra línea de ese archivo, algo se
torció.

**Alternativas descartadas**: exponer `track` solo bajo un flag nuevo
(`--json --with-track`) — el ejecutor necesita el campo siempre, un flag
condicional multiplicaría los caminos de deserialización de `Status`, y el
oráculo quedaría igualmente desactualizado el día que el flag se vuelva default.

---

## R5 — Las incoherencias de pista se reportan como `warnings`, nunca como estado

**Decisión**: cuando `track == corta`, `evaluate()` añade a la lista `warnings`
(canal advisory que ya existe y que el modo estudio usa) hasta dos entradas:

1. Temario con más de una fila:
   `"track: corta declara pieza única pero el temario tiene N filas: corrige el temario o escala (scripts/track.py --escalar)"`
2. Capítulos con ordinal ≥ 2 en `chapters/`:
   `"track: corta con capítulos fuera de pieza única (2, 3): sugiere escalar (scripts/track.py --escalar)"`

Los textos literales mandan desde `contracts/track-cli.md` § 3.2, no desde aquí.

Ninguna de las dos modifica `next_step`, `next_detail`, `gates`, `closeable`,
`by_chapter` ni `all_chapters_approved`. Son informativas y no bloquean.

La validación **dura** vive en `track.py --check`, que sí sale con exit 1.

**Razón**: FR-001 dice "ningún otro cambio en la brújula es admisible", pero los
Edge Cases de la spec piden que "el detalle del estado sugiere escalar" y que un
temario de más de una fila en pista corta se detecte "con mensaje claro". La
contradicción se resuelve delimitando *brújula* = máquina de estados
(`next_step`) + gates + `by_chapter`. `warnings` no es brújula: es el canal por
el que `status.py` ya avisa de huellas inválidas y disposiciones incoherentes
(005) sin alterar el estado. La excepción queda acotada, declarada y probada
(el fixture `estandar` no emite ninguna de las dos entradas, así que la
retrocompatibilidad de FR-010 se sostiene).

**Alternativas descartadas**: (a) tocar `next_detail` — cambiaría el texto que
el ejecutor registra en `decisions.jsonl` y rompería la byte-identidad de R4;
(b) dejar la detección solo en `track.py --check` — la operadora que corre
`status.py` (el gesto habitual) no vería nunca el aviso, y el edge case pide
justo eso.

---

## R6 — `intro` se omite en pista corta en **ambos** modos

**Decisión**: en `plan_global`, el bloque que exige `README.md` queda guardado
por `if !is_corta(status) && !project.join("README.md").is_file()`. En
`corta`+`estudio` **no hay checkpoint `intro`**: los checkpoints humanos son
`specify`, `write`, `dispose` y `feedback`.

**Razón**: el checkpoint `intro` de la 005 existe porque el README de
presentación es prosa publicada que en modo estudio debe escribir la humana. En
pista corta no hay README de presentación en absoluto (FR-007: "el ejecutor MUST
NOT exigir `README.md` antes del export"), así que no hay prosa que proteger. Un
checkpoint sobre un artefacto que el método declara inexistente sería un
callejón sin salida: la humana no tendría nada que escribir para desbloquearlo.

La ortogonalidad de FR-009 se conserva: la matriz `track × mode` completa es

| | `produccion` | `estudio` |
|---|---|---|
| `estandar` | intro despachado a Redactora | intro = checkpoint humano |
| `corta` | intro omitido | intro omitido |

**Alternativas descartadas**: mantener el checkpoint `intro` en `corta`+`estudio`
— dejaría el pipeline colgado; contradice FR-007.

---

## R7 — La pasada combinada no toca el contrato `pass-output`

**Decisión**: `writeonmars/contracts/pass-output-schema.md` permanece en **v1.2
sin modificar**. La pasada combinada emite cuatro bloques estándar
(`## Pasada 1 — Estructura`, `## Pasada 2 — Utilidad`,
`## Pasada 3 — Naturalidad`, `## Pasada 5 — Formato`) en un único run. Cada uno
lleva su `<!-- pass-output-schema: v1.2 -->` y su huella; los bloques 1-3
declaran `Capítulos cubiertos: 1` y el 5, `global`.

**Razón**: el precedente ya existe en el método. `speckit.review-structure.md`
emite hoy **dos** bloques (Pasada 1 y Pasada 2) en una sola ejecución — "cubre
las dos dimensiones en una sola ejecución, según el `signing_matrix`". El
esquema nunca ha atado un bloque a un proceso: ata un bloque a una dimensión.
La combinada extiende ese precedente de dos a cuatro dimensiones. `parse_findings`
no distingue el origen; `_passes_by_chapter` ignora la pasada 5 (solo 1-4
gobiernan `approved`); `plan_global` solo comprueba la existencia del bloque 5.

Por eso la combinada es una **comodidad de ceremonia**, no un contrato: si el
agente registra solo parte de los bloques, el ejecutor despacha los sueltos que
falten (US2, escenario 4) y el proyecto converge igual.

**Alternativas descartadas**: un bloque nuevo `## Pasada combinada` — obligaría
a cambiar `parse_findings`, `_passes_by_chapter`, `status.py`, el ejecutor y el
schema. Exactamente lo que FR-005 prohíbe.

---

## R8 — `track_history` no es espejo exacto de `mode_history`

**Decisión**: cada entrada de `track_history` es
`{"from", "to", "date", "actor"}` más `"email"` opcional. `mode_history` solo
tiene `{"from", "to", "date"}`.

**Razón**: FR-008 exige que el escalado registre "pista nueva, fecha y **actor
humano**", y que el script rechace identidades de agente. Sin `actor` el
registro no es auditable y `--escalar` no podría demostrar que lo hizo una
persona. La spec dice "espejo de `mode_history`" refiriéndose a la *forma*
(array append-only en el manifiesto, escrito solo por script, nunca a mano), no
al conjunto de campos.

La divergencia se documenta en `data-model.md` § 2 y en el delta del schema. No
se retro-modifica `mode_history`: sería un cambio fuera del alcance de esta
feature (queda como nota en el ROADMAP).

**Alternativas descartadas**: omitir `actor` para simetría literal — dejaría el
registro sin la propiedad que FR-008 declara su razón de ser.

---

## R9 — Portada compacta: plantilla nueva, clase nueva, `@page cover` reusado

**Decisión**: se añade `writeonmars/assets/cover-compact.html.template`:

```html
<div class="cover cover-compact">
  <h1 class="cover-title">{{TITLE}}</h1>
  <div class="cover-author">{{AUTHOR}}</div>
  <div class="cover-meta">{{META}}</div>
</div>
```

En `style.css` se añade **solo** la regla `.cover-author` y los ajustes de
`.cover-compact` (centrado vertical más alto, sin `eyebrow` ni `subtitle`). La
clase `.cover` se conserva en el elemento, de modo que `page: cover` y
`page-break-after: always` siguen aplicando sin duplicar la `@page`.

`export.py` gana `build_cover_compact(title, author, meta) -> str` (función pura,
gemela de `build_cover`) y, cuando `track == corta`, no invoca `build_toc()`.

`AUTHOR` sale de `manifest.human_operators[0]`: `id` si no hay `email`, y si el
manifiesto no existe, cadena vacía (la portada omite la línea).

**Razón**: reusar `.cover` evita tocar `@page cover` y los saltos de página ya
probados. Sin `.toc-page` intermedia, el primer capítulo abre página por la
regla `page-break-after: always` de la portada: no hace falta CSS nuevo de
paginación.

Criterio de aceptación **sin Chrome** (test unitario): `build_cover_compact()`
devuelve HTML que contiene `cover-compact` y no contiene `cover-eyebrow` ni
`cover-subtitle`; y el HTML intermedio de `main()` con `--keep-temp` sobre el
fixture corta no contiene la subcadena `toc-page`.

**Alternativas descartadas**: un modificador CSS sobre la plantilla existente
(dejando `{{EYEBROW}}` y `{{SUBTITLE}}` vacíos y ocultos por CSS) — genera
elementos vacíos en el DOM y hace la portada dependiente de un `display: none`
que un cambio de hoja de estilo puede reactivar.

---

## R10 — `count_temario` y `_drafted_ordinals` se mudan a `findings_lib.py`

**Decisión**: ambas funciones pasan a `writeonmars/scripts/findings_lib.py`
(`count_temario`, `drafted_ordinals` — sin guion bajo, es API compartida).
`status.py` las importa y conserva alias módulo-locales
(`count_temario = findings_lib.count_temario`,
`_drafted_ordinals = findings_lib.drafted_ordinals`) para no romper importadores
ni los tests existentes.

**Razón**: `track.py` necesita las dos para validar la legalidad del
des-escalado (temario ≤ 1 fila, sin capítulos de ordinal ≥ 2). Copiarlas sería
duplicar un parser — el riesgo que el plan de la 005 ya identificó y resolvió
creando `findings_lib.py`. El módulo existe justo para esto: "prohibido
copiar-pegar el parser".

La mudanza no cambia ninguna salida. `pytest tests/unit -q` debe pasar sin
editar una sola aserción antes de tocar nada más.

**Alternativas descartadas**: que `track.py` importe de `status.py` — arrastraría
el `argparse` y el `sys.exit(2)` de `fail()` de un script pensado para correr
como CLI.

---

## R11 — En produccion, `next_step` vale `close`, no `review`, en cuanto hay un bloque

**Decisión**: ninguna aserción de esta feature comprueba `next_step == "review"`
sobre un proyecto en produccion con pasadas parcialmente registradas. El estado
de la revisión se comprueba con `all_chapters_approved` y `by_chapter[c].passes_done`.

**Razón** (verificado empíricamente contra `status.py`, 2026-07-10, fixture corta
en produccion con un capítulo y temario de una fila):

| Bloques en `findings.md` | `next_step` | `closeable` | `all_chapters_approved` | `passes_done` |
|---|---|---|---|---|
| ninguno | `review` | `True` | `False` | `[]` |
| 1, 2 (combinada a medias) | **`close`** | `True` | `False` | `[1, 2]` |
| 1, 2, 3, 5 (combinada completa) | **`close`** | `True` | `False` | `[1, 2, 3]` |
| 1, 2, 3, 5 + 4 | `close` | `True` | `True` | `[1, 2, 3, 4]` |

En `_next_step`, la rama `if not blocks: return "review"` solo dispara con
`findings.md` vacío. A partir del primer bloque, y sin críticos ni hallazgos
accionables, los tres gates (`g1` sin críticos, `g2` firmas, `g3` capítulos ≥
temario) están en verde y la función devuelve `close`. En produccion `closeable`
**no** exige `all_chapters_approved`; solo lo exige en estudio.

Lo que conduce el bucle de pasadas por capítulo es, por tanto, la **rama de
normalización del ejecutor** (`runner.rs:162`):

```rust
if status.next_step == "close" && !status.all_chapters_approved {
    …
    if let Some(action) = choose_review_action(status)? { return Ok(Planned::Act(action)); }
}
```

Su propio comentario lo dice: *"status.py puede decir 'close' con capítulos aún
incompletos (va por delante del trabajo en vuelo): normaliza al paso por capítulo
pendiente."*

**Consecuencias para esta feature**:

1. Tras la pasada combinada, el despacho de `review-4` llega por normalización,
   no por la rama `"review"` de `plan_action`. El resultado es el mismo (6
   despachos) y ningún archivo del ejecutor cambia — pero quien implemente debe
   saberlo o escribirá tests que fallan.
2. El fixture de combinada a medias (`medias/`) se verifica con
   `all_chapters_approved is False` y `passes_done == [1, 2]`, **jamás** con
   `next_step == "review"`.
3. La degradación grácil (US2, escenario 4) sigue intacta: `choose_review_action`
   encuentra la pasada 3 ausente y la despacha, se llegue por la rama que se
   llegue.

**Alternativas descartadas**: endurecer `closeable` en produccion para que exija
`all_chapters_approved` — haría `next_step` más legible, pero es un cambio de la
lógica de estado que SC-003 y FR-001 prohíben, rompería la retrocompatibilidad
de todos los proyectos existentes y dejaría sin sentido la rama de normalización
que el ejecutor ya tiene probada. Queda anotado en el ROADMAP como limpieza
futura, fuera del alcance de esta feature.

---

## Fundamento externo y trazabilidad

Constitución § Arquitectura ("Trazabilidad documental"): decisión propia del
proyecto con fundamento externo en el análisis de BMAD v6
(`docs/comparativa-bmad.md`: pistas Quick Flow / Method / Enterprise y escalado
con arrastre de trabajo) y en evidencia de coste propia
(`tests/editorial-pilot/evidence/2026-07-08-vivarium-byom/`: 26 despachos para
2 capítulos). El recuento verificable de la ceremonia estándar sobre una pieza
única (11 despachos) está en `plan.md` § 10.
