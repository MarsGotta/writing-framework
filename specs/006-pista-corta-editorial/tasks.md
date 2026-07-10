# Tasks: Pista corta editorial (ceremonia adaptativa)

**Input**: Design documents from `/specs/006-pista-corta-editorial/`
**Prerequisites**: plan.md, research.md (R1-R10), data-model.md, contracts/
(manifest-v1.4.0-delta.md, track-cli.md, ceremonia-corta.md), quickstart.md

> **LA IMPLEMENTACIÓN LA HARÁ UN AGENTE DISTINTO DEL QUE REDACTÓ SPEC Y PLAN.**
> Cada tarea es autocontenida: rutas dentro del repo, contrato de referencia y
> criterio verificable por script. Ante ambigüedad mandan `contracts/` y
> `research.md`.
>
> **Regla transversal (FR-010)**: NINGUNA aserción de test existente se edita.
> Los proyectos sin `track` o con `track: estandar` conservan su comportamiento
> exacto. Baseline al planificar: **169 tests unitarios en verde**.
>
> **Invocador de pytest**: el `python3` del sistema no trae pytest. Usa
> `uvx --with pytest --with pyyaml --with jsonschema python -m pytest tests/unit -q`.
>
> **Contratos que NO se tocan**: `writeonmars/contracts/pass-output-schema.md`
> queda en v1.2 sin una sola línea nueva (FR-005). `preset.yml` no necesita
> cambios: no registra scripts ni assets (viajan por directorio; ver su línea 201).

**Organización**: por user story, para que cada una sea implementable y
testeable de forma independiente.

## Phase 1: Setup (contratos y constitución antes que el código)

- [ ] T001 Enmendar la constitución a **v1.7.0** (MINOR) en las **dos** copias,
  que deben quedar byte-idénticas: `.specify/memory/constitution.md` y
  `writeonmars/memory/constitution.md` (`bootstrap.py` lee la del preset).
  Añadir la sección **"Pistas de ceremonia"** en paralelo a "Modos de proyecto"
  (FR-011): la pista gobierna cuánto rito y el modo quién escribe; en pista
  corta las cinco dimensiones del Principio V se verifican en dos relevos
  (combinada 1·2·3·5 + precisión 4) sin debilitar ningún NO NEGOCIABLE —
  **voz ≠ precisión**, **escribe-uno-revisa-otro** y **detector ≠ corrector** se
  preservan; defaults opinados sin candados; el cambio de pista es solo humano y
  registrado. Actualizar el sync impact report de la cabecera (v1.6.1 → v1.7.0,
  bump rationale, trazabilidad a `docs/comparativa-bmad.md` y a la evidencia de
  coste `tests/editorial-pilot/evidence/2026-07-08-vivarium-byom/`) y el pie
  `**Version**: 1.7.0 | … | **Last Amended**: <fecha>`. Propagar la fila
  **"Pista de ceremonia"** al Constitution Check de las **dos** copias de
  `plan-template.md` (`.specify/templates/` y `writeonmars/templates/`).
  Gate: `python3 -c "import re,pathlib; a=pathlib.Path('.specify/memory/constitution.md').read_bytes(); b=pathlib.Path('writeonmars/memory/constitution.md').read_bytes(); assert a==b"`.
- [ ] T002 [P] Publicar los contratos, aplicando los deltas de esta feature sobre
  la **fuente única** (`writeonmars/contracts/`; la raíz `contracts/` y
  `specs/001-*/contracts/` son punteros — no editar ahí):
  (a) `writeonmars/contracts/manifest-schema.json` v1.3.0 → **v1.4.0** aplicando
  `specs/006-pista-corta-editorial/contracts/manifest-v1.4.0-delta.md` (`$id`,
  `title`, `$comment`, propiedades `track` y `track_history` tras `mode_history`;
  `additionalProperties` sigue en `false`, por eso ambas deben declararse);
  (b) `writeonmars/contracts/executor-contract.md`: añadir `track` a la lista de
  campos garantizados de § 3 y la nueva **§ 7 "Pista corta"** con el contenido de
  `contracts/ceremonia-corta.md` § 4.
  Gate: los 5 checks del delta § 5 (schema válido; manifiesto sin `track` valida;
  con `"track": "corta"` valida; con `"track": "rapida"` **no** valida; entrada de
  `track_history` sin `actor` **no** valida).
- [ ] T003 [P] Fixtures en `tests/fixtures/006-corta/` (quickstart § 0), dos
  variantes que solo difieren en `mode`: `produccion/` y `estudio/`. Cada una con
  `.writeonmars-manifest.json` (`track: "corta"`, `sector: "tecnologia"`,
  `registro: "tecnico-divulgativo"`, `project_type: "editorial"`, resto de campos
  como `tests/fixtures/003-factualidad/`), `specs/001-mi-pieza/spec.md` (brief
  compacto firmado), `research.md`, `plan.md` con `## Temario` de **una** fila,
  `findings.md` con los bloques 1·2·3 (`Capítulos cubiertos: 1`), 5
  (`Capítulos cubiertos: global`) y 4, todos con `<!-- pass-output-schema: v1.2 -->`
  y huellas sha256 correctas, `claims.md`, y `chapters/01-la-pieza.md`.
  Añadir dos fixtures degradados para los edge cases: `medias/` (combinada que solo
  registró los bloques 1 y 2) e `incoherente/` (`track: corta` con temario de 3
  filas y `chapters/02-*.md`).

## Phase 2: Foundational (bloquea todas las stories)

- [ ] T004 `writeonmars/scripts/findings_lib.py` (research R10, data-model § 1):
  (a) añadir `project_track(manifest) -> "estandar"|"corta"` — gemelo exacto de
  `project_mode`: `None`/ausencia ⇒ `"estandar"`; valor desconocido ⇒ `ValueError`
  con mensaje claro;
  (b) **mover** `count_temario(spec_dir)` y `_drafted_ordinals(chapters)` desde
  `status.py`, renombrando la segunda a `drafted_ordinals` (API compartida, sin
  guion bajo), porque `track.py` las necesita para validar el des-escalado;
  (c) en `writeonmars/scripts/status.py`, importarlas y conservar los alias
  módulo-locales `count_temario = findings_lib.count_temario` y
  `_drafted_ordinals = findings_lib.drafted_ordinals` para no romper importadores
  ni tests. Prohibido copiar-pegar el parser en `track.py`.
  Gate: `uvx --with pytest --with pyyaml --with jsonschema python -m pytest tests/unit -q`
  sigue en **169 verdes sin editar una sola aserción**.

**Checkpoint Foundational**: suite previa intacta; las stories pueden arrancar.

## Phase 3: User Story 1 — Declarar la pista y recorrer el ciclo corto (P1) 🎯 MVP

**Goal**: la pista existe, la brújula nunca pide `plan` ni `constitution`, el
brief compacto materializa el temario degenerado y el export produce un PDF de
pieza única.

**Independent Test**: quickstart § 2 — fixture `corta` en produccion; `next_step`
jamás vale `plan` ni `constitution` en ningún estado intermedio;
`chapters_expected == 1`; el HTML de export no contiene `toc-page`. El recuento
de despachos (≤ 8) se verifica en la Phase 7, que necesita el ejecutor.

- [ ] T005 [US1] `writeonmars/scripts/bootstrap.py` según `contracts/track-cli.md`
  § 2 y research R2/R3: argumentos `--track {estandar,corta}` (default
  `os.environ.get("WRITEONMARS_TRACK", "estandar")`) y `--sector <slug>` (default
  `os.environ.get("WRITEONMARS_SECTOR")`). **Revalidar `--track` fuera de
  `choices`**, porque `argparse` no valida el default y un `WRITEONMARS_TRACK` con
  typo acabaría escrito en el manifiesto (mismo bug que `bootstrap.py:133` ya
  evita para `--mode`). `default_manifest()` gana el parámetro `track` y escribe
  la clave siempre (también con `estandar`). Con `--sector`: verificar que existe
  `PRESET/references/sectores/<slug>.md` (si no, `fail()` con exit 1 listando los
  slugs disponibles, ignorando `_index.md`); escribir `sector`; extraer el slug del
  registro del primer texto entre backticks bajo el encabezado
  `## Registro por defecto` y escribir `registro` si aparece; materializar el
  bloque de **adendas por referencia** (forma literal en research.md § R2) al final
  de `.specify/memory/constitution.md`, empezando por el centinela
  `<!-- WRITEONMARS:ADENDAS -->`. Si el centinela ya existe, **no reescribir** —
  respeta adendas calibradas a mano — e imprimir aviso. Sin `--sector`:
  comportamiento actual intacto (`sector: null`).
- [ ] T006 [P] [US1] `tests/unit/test_bootstrap.py`: añadir casos (sin editar los
  existentes) — `--track corta` escribe la clave; `WRITEONMARS_TRACK=corta` la
  escribe; `WRITEONMARS_TRACK=rapida` falla con exit 1 y mensaje claro;
  `--sector tecnologia` escribe `sector` + `registro: "tecnico-divulgativo"` y deja
  el centinela `WRITEONMARS:ADENDAS` con la cadena "POR REFERENCIA" en la
  constitución; `--sector inventado` falla con exit 1 listando los disponibles;
  centinela preexistente ⇒ no se reescribe; el manifiesto generado valida contra
  `manifest-schema.json` v1.4.0.
- [ ] T007 [US1] `writeonmars/scripts/status.py` según `contracts/track-cli.md` § 3
  (research R4, R5) — **solo dos cambios**: (a) `evaluate()` añade la clave
  `"track"` al dict de salida, junto a `"mode"`, vía un wrapper local
  `project_track(manifest)` que convierte `ValueError` en `fail()` (espejo de
  `project_mode`, `status.py:66`); siempre presente, nunca `null`. (b) cuando
  `track == "corta"`, anexar a la lista `warnings` existente hasta dos entradas
  advisory: temario con más de una fila, y capítulos con ordinal ≥ 2 en disco
  (textos literales en el contrato § 3.2).
  **PROHIBIDO** tocar `_next_step` (ni sus ramas ni sus textos de `next_detail`),
  `_build_by_chapter`, `_passes_by_chapter`, `_passes_by_chapter_checked`, el
  cálculo de `gates`/`closeable`/`all_chapters_approved` ni `print_dashboard`.
- [ ] T008 [P] [US1] Tests de la brújula: (a) crear `tests/unit/test_status_corta.py`
  — con el fixture `006-corta/produccion`, `chapters_expected == 1`, `next_step`
  nunca vale `plan` ni `constitution` recorriendo los estados intermedios (sin
  research, con research, con capítulo, con pasadas); fixture `incoherente/` emite
  las dos entradas de `warnings` **sin** alterar `next_step`, `gates` ni
  `closeable`; manifiesto con `"track": "rapida"` ⇒ exit 2 y mensaje claro.
  (b) añadir a `tests/unit/test_status.py` (sin editar aserciones) un **test de
  oráculo de retrocompatibilidad**: sobre un fixture `estandar`, la salida de
  `print_dashboard` es byte-idéntica a la capturada antes de la feature, y el dict
  de `--json` difiere de la referencia **exactamente** en la clave `track ==
  "estandar"` y en nada más (SC-003, quickstart § 1).
- [ ] T009 [US1] `writeonmars/commands/speckit.specify.md` (FR-003,
  `contracts/ceremonia-corta.md` § 1): sección `## Pista corta` — si el manifiesto
  declara `track: corta`, capturar los ocho campos descriptivos **más título y
  promesa de la pieza** en **una sola ronda** de preguntas (checkpoint humano 1
  intacto: sin firma no hay avance) y, **al quedar firmado el brief**, materializar
  el temario degenerado escribiendo `specs/<###-feature>/plan.md` con una sección
  `## Temario` de una fila (`| 1 | <título firmado> | <promesa firmada> |
  didactica_v1 |`). Título y promesa se copian **tal cual**: el agente no los
  reescribe. No materializar el temario antes de la firma.
- [ ] T010 [P] [US1] Cláusulas de pista en el resto de comandos
  (`contracts/ceremonia-corta.md` § 1), sección `## Pista corta` en cada uno:
  `writeonmars/commands/speckit.research.md` (research exprés acotado a los
  conceptos obligatorios del brief; sin panorama ni estado del arte; el contrato de
  citación se conserva íntegro y sigue bloqueando si un concepto queda sin
  respaldo); `speckit.constitution.md` (opcional en corta: `bootstrap --sector` ya
  dejó sector, registro y adendas por referencia; sigue disponible para calibrar a
  mano); `speckit.plan.md` (si se invoca a mano en corta, **MUST preservar** la
  sección `## Temario` existente: no regenerarla ni sobrescribirla);
  `speckit.intro.md` (**no aplica** en corta: se auto-anula explicando que no hay
  README de presentación y que `export.py` produce la portada compacta);
  `speckit.export.md` (mención: `export.py` detecta la pista).
- [ ] T011 [US1] `writeonmars/scripts/export.py` + assets, según
  `contracts/track-cli.md` § 4 y research R9: (a) importar `findings_lib` con el
  mismo prólogo `sys.path` que usan `status.py` y `dispose.py`, y leer
  `track = findings_lib.project_track(findings_lib.load_manifest(project))`
  (tolerante: manifiesto ausente ⇒ `estandar`); (b) crear
  `writeonmars/assets/cover-compact.html.template` con el marcado literal del
  contrato § 4.4 (conserva la clase `.cover` para heredar `page: cover` y
  `page-break-after: always`); (c) añadir la función pura
  `build_cover_compact(title, author, meta) -> str`; (d) cuando `track == "corta"`,
  usar esa portada y **no invocar `build_toc()`**; `author` sale de
  `manifest["human_operators"][0]` (`id` si no hay `email`; cadena vacía si falta
  el manifiesto o la lista, y entonces la portada omite la línea); (e) en
  `writeonmars/assets/style.css` añadir **solo** `.cover-author` y los ajustes de
  `.cover-compact` — no tocar la regla `@page cover`. `wrap_chapter_sources` y la
  validación contra `claims.md` quedan idénticas.
- [ ] T012 [P] [US1] `tests/unit/test_export.py`: añadir casos (sin editar los
  existentes) — `build_cover_compact("T","A","2026")` contiene `cover-compact`, `T`,
  `A` y `2026`, y **no** contiene `cover-eyebrow` ni `cover-subtitle`; sobre el
  fixture `006-corta/produccion`, el HTML ensamblado **no** contiene la subcadena
  `toc-page`; sobre un fixture `estandar`, **sí** contiene `toc-page` y
  `cover-eyebrow` (regresión). Los tres se verifican sin Chrome, sobre las
  funciones puras y el HTML intermedio.

**Checkpoint US1**: `pytest tests/unit -q` verde (≥ 169, ninguna aserción previa
editada) y el fixture corta llega a `chapters_expected == 1` sin que la brújula
pida `plan`.

## Phase 4: User Story 2 — Cinco dimensiones, dos relevos (P2)

**Goal**: la revisión corre en dos relevos, las cinco dimensiones constan en
`findings.md`, el capítulo llega a `approved` **sin cambio alguno en `status.py`**,
y la combinada no es un punto único de fallo.

**Independent Test**: quickstart § 3 — sobre el fixture con la combinada y la
precisión registradas, `passes` contiene `[1,2,3,4,5]`, `by_chapter["1"].approved`
es `true` y `closeable` es `true`, todo con el parser actual. Sobre el fixture
`medias/`, `next_step == "review"` y la pasada 3 sigue ausente.

- [ ] T013 [US2] `writeonmars/commands/speckit.review-structure.md` (FR-005,
  `contracts/ceremonia-corta.md` § 2): sección `## Pista corta` — el comando se
  vuelve consciente de pista y en `corta` verifica y registra **cuatro bloques** en
  un único run: `## Pasada 1 — Estructura`, `## Pasada 2 — Utilidad` y
  `## Pasada 3 — Naturalidad` (los tres con `**Capítulos cubiertos**: 1`), más
  `## Pasada 5 — Formato` (con `global`). Cada bloque lleva su
  `<!-- pass-output-schema: v1.2 -->` y su huella; la de la pasada 5 es
  `sha256(concat(sha256(cap_i)))`, que con un capítulo es `sha256(sha256(cap_1))`.
  Declarar explícitamente que la dimensión 4 **no** va aquí (regla dura
  voz ≠ precisión) y que la coherencia inter-capítulos de la dimensión 5 es vacua
  en pieza única. Respetar la `signing_matrix`. El esquema pass-output **no se
  toca**: el comando ya emitía dos bloques en un run y esto extiende el precedente.
- [ ] T014 [US2] `writeonmars/commands/speckit.review.md`: sección `## Pista corta`
  — el agrupado ejecuta **dos** relevos en vez de cuatro: la combinada
  (`speckit.review-structure`, rol editora de mesa) y la precisión
  (`speckit.review-precision`, rol documentalista, **otro modelo**). Declarar MUST:
  la configuración BYOM asigna roles distintos; colapsarlos en el mismo modelo
  viola el Principio V.
- [ ] T015 [P] [US2] Cláusula de red de reparación (FR-006) en
  `writeonmars/commands/speckit.review-voice.md` y `speckit.review-global.md`:
  en pista corta siguen operativos para rellenar los bloques 3 y 5 que la combinada
  dejara incompletos. `speckit.review-precision.md` gana una nota: siempre es
  relevo aparte, en corta y en estándar. La combinada es una comodidad, no un punto
  único de fallo.
- [ ] T016 [P] [US2] Añadir a `tests/unit/test_status_corta.py`: (a) con el fixture
  `produccion` completo, `sorted(p["num"] for p in passes) == [1,2,3,4,5]`,
  `by_chapter["1"]["approved"] is True`, `closeable is True` y `claims.md` existe —
  **sin haber modificado `status.py` más allá de T007** (SC-002, SC-003);
  (b) con el fixture `medias/`, `next_step == "review"` y `4 not in
  by_chapter["1"]["passes_done"]` ni `3`; (c) con un hallazgo `medio` abierto,
  `next_step == "revise"` en produccion y `"dispose"` en estudio (fixture
  `estudio/`); (d) matriz corta+estudio: las huellas de la 005 siguen invalidando
  pasadas cuando el capítulo cambia.

**Checkpoint US2**: quickstart § 3 reproducible; `status.py` sin más cambios que
los de T007.

## Phase 5: User Story 3 — Escalar sin tirar trabajo (P3)

**Goal**: el escalado conserva el 100 % del trabajo, queda registrado con actor
humano, y el des-escalado ilegal se rechaza. Ningún agente puede escalar.

**Independent Test**: quickstart § 4 — sobre el fixture corta con la pieza
aprobada, `track.py --escalar` deja `track: estandar` + entrada en
`track_history`; `git status --porcelain` muestra **solo** el manifiesto
modificado; tras ampliar el temario a 4 filas, el capítulo 1 conserva `approved` y
`pending_chapters == [2,3,4]`.

- [ ] T017 [US3] Crear `writeonmars/scripts/track.py` según `contracts/track-cli.md`
  § 1 y data-model § 6, patrón `dispose.py`: grupo mutuamente excluyente y
  obligatorio `--escalar | --desescalar | --check`, más `--project-dir`, `--spec`,
  `--json`. Identidad humana idéntica a `dispose.py:45` (`git config user.name` /
  `user.email`; vacío o `*@agents.writeonmars.invalid` ⇒ exit 3); `--check` es
  read-only y no la exige. Legalidad: `--escalar` solo desde `corta` (siempre legal,
  **no toca ningún archivo salvo el manifiesto**); `--desescalar` solo desde
  `estandar`/ausente y únicamente si `findings_lib.count_temario(spec_dir) <= 1` y
  no hay `chapters/NN-*.md` con `NN >= 2`; misma pista de origen y destino ⇒ exit 1.
  Efecto: `track` + append a `track_history` con
  `{from, to, date (UTC ISO-8601 Z sin microsegundos), actor, email?}`, escritura
  **atómica** (tmp + `os.replace` con rollback, patrón `dispose.py:135`),
  preservando `indent=2` y `ensure_ascii=False`. `--check` valida el invariante
  (corta ⟺ temario ≤ 1 fila ∧ sin capítulos de ordinal ≥ 2) con los exit codes y
  mensajes de la tabla del contrato § 1.5. Exit codes: 0 OK, 1 estado/legalidad,
  2 uso, 3 identidad no humana.
- [ ] T018 [P] [US3] `tests/unit/test_track.py`: construye en tmp un repo git real
  (`subprocess` git init/config/commit) — escalado legal registra `from`/`to`/`date`
  (termina en `Z`)/`actor` y el manifiesto valida contra el schema v1.4.0;
  des-escalado con temario de 4 filas ⇒ exit 1 con el mensaje del contrato;
  des-escalado con `chapters/02-*.md` ⇒ exit 1 enumerando los ordinales; escalar dos
  veces ⇒ exit 1 ("ya está en pista estandar"); identidad
  `redactora@agents.writeonmars.invalid` ⇒ exit 3; sin `user.name` ⇒ exit 3;
  atomicidad (fallo simulado en `os.replace` deja el manifiesto con sus bytes
  originales y sin `.tmp` huérfano); `--check` sobre el fixture `incoherente/` ⇒
  exit 1; conservación del trabajo: tras escalar y ampliar el temario a 4 filas,
  `status.py --json` da `by_chapter["1"]["approved"] is True` y
  `pending_chapters == [2,3,4]` (SC-004).

**Checkpoint US3**: `pytest tests/unit/test_track.py` verde; ningún archivo
movido por el escalado.

## Phase 6: Integración con el ejecutor (depende de US1)

- [ ] T019 `vivarium/crates/vivarium-core/src/sidecar.rs`: `Status` gana
  `#[serde(default)] pub track: Option<String>`. Fontanería de deserialización,
  tolerante a `status.py` antiguos (`None` ⇒ ceremonia estándar). Test:
  `status_sin_track_deserializa` — un JSON de `status.py` sin la clave `track`
  deserializa con `track == None`.
- [ ] T020 `vivarium/crates/vivarium-core/src/runner.rs` según
  `contracts/ceremonia-corta.md` § 5 y research R6 — **único cambio de
  comportamiento del ejecutor**: helper `is_corta(status)` espejo de
  `is_estudio(status)`, y en `plan_global` guardar el bloque del README con
  `if !is_corta(status) && !project.join("README.md").is_file() { … }`. El salto
  aplica en **ambos modos**: en `corta`+`estudio` no hay checkpoint `intro`, porque
  un checkpoint sobre un artefacto que el método declara inexistente sería un
  callejón sin salida. **PROHIBIDO** tocar `writes_manuscript`, `blocked_by_mode`,
  el guardarraíl exit 11, `choose_review_action`, `effect_satisfied`, `plan_action`,
  `bootstrap.rs` y `dispatch.rs`. No crear `vivarium track set`: el escalado vive
  en el preset. Tests unitarios junto a los existentes (que **no se editan**):
  `plan_global_omite_intro_en_corta` (⇒ `Act(export)`),
  `plan_global_omite_intro_en_corta_estudio` (⇒ `Act(export)`, **no**
  `Checkpoint{step:"intro"}`), `plan_global_sigue_pidiendo_intro_en_estandar`.
- [ ] T021 [P] Tests de integración del ejecutor en
  `vivarium/crates/vivarium-cli/tests/runner.rs` (stubs de `tests/common/mod.rs`):
  `vivarium run` sobre un proyecto `track: corta` sin `README.md` con la pasada 5
  registrada ⇒ despacha `export`, nunca `intro`; y ante la combinada registrada,
  el siguiente despacho es `review-4` con rol `documentalista` (no `review-2` ni
  `review-3`) — prueba de que `choose_review_action` no necesitó cambios.
  Gate: `cd vivarium && cargo test --workspace`.

## Phase 7: Polish & e2e

- [ ] T022 Smoke `tests/smoke/corta-e2e.sh` implementando quickstart § 6 (espejo de
  `tests/smoke/estudio-e2e.sh`; Bash 3.2; skip exit 99 sin `cargo`) y alta del test
  en el array `tests=(...)` de `tests/smoke/run-all.sh`. Crea el proyecto con
  `WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia vivarium new …` — sin tocar
  el ejecutor (research R3). **Stubs distinguibles por rol**: el de `editora_mesa`
  escribe los bloques 1·2·3·5; el de `documentalista`, el 4 y `claims.md` — así el
  smoke prueba `voz ≠ precisión` estructuralmente. Asserts: manifiesto con `track`,
  `sector` y `registro`; adendas con "POR REFERENCIA"; **cero despachos** de `plan`,
  `constitution`, `review-2`, `review-3`, `review-5` e `intro`; el PDF existe y su
  HTML no tenía índice; **≤ 8 despachos** contando `event == "dispatch"` en
  `.vivarium/decisions.jsonl` (valor esperado: 6); segundo `run` exit 0 sin
  despachos nuevos. Repetir en `mode: estudio`: checkpoints `write`, `dispose` y
  `feedback`, jamás `intro`, guardarraíl exit 11 intacto. Cerrar con
  `track.py --escalar` sobre el proyecto cerrado: solo el manifiesto cambia.
- [ ] T023 [P] Crear `writeonmars/docs/how-to-pista-corta.md` (hermano de
  `how-to-modo-estudio.md`): cuándo elegir pista corta, cómo declararla
  (`--track`/`--sector` o las env vars), qué pasos desaparecen y por qué, cómo
  corren los dos relevos, cómo escalar con `track.py` y qué se conserva. Añadir la
  sección de pista a `writeonmars/AGENTS.md` (contrato del agente: leer `track` del
  manifiesto; la combinada; `intro` no aplica; ningún agente cambia `track`).
- [ ] T024 [P] Docs del repo: entrada de la feature en `CHANGELOG.md`; estado en
  `ROADMAP.md` (pista corta operativa; nota pendiente de retro-modificar
  `mode_history` con `actor`, research R8); actualizar `CLAUDE.md` (constitución
  v1.7.0, spec 006 integrada) y `writeonmars/README.md` si enumera scripts.
- [ ] T025 Gate final (SC-006): `uvx --with pytest --with pyyaml --with jsonschema
  python -m pytest tests/unit -q` + `bash tests/smoke/run-all.sh` + `cd vivarium &&
  cargo test --workspace` — los tres en verde, en local y en CI
  (`.github/workflows/ci.yml`), sin pasos manuales no documentados. Verificar que el
  conteo de tests unitarios es **≥ 169** y que `git diff` no muestra ninguna
  aserción preexistente modificada (FR-010).

## Dependencies & Execution Order

- **Phase 1 → todo**: T001 (constitución) y T002 (contratos) fijan la verdad antes
  del código; el Constitution Check del plan depende de que la enmienda v1.7.0 se
  publique **antes** que el código que la ejerce. T003 es paralelizable con ambas.
- **Phase 2 bloquea las stories**: T004 es prerrequisito de T007 (status), T011
  (export) y T017 (track.py). Su gate — 169 verdes sin editar aserciones — es la
  prueba de que la mudanza fue neutral.
- **US1 (T005-T012)**: depende de Foundational. **MVP = US1**. Dentro: T005 → T006;
  T007 → T008; T009 y T010 son paralelizables entre sí; T011 → T012.
- **US2 (T013-T016)**: depende de US1 (la pista debe existir). T013 → T014;
  T015 y T016 paralelizables. **No toca `status.py`**: si lo necesitara, algo se
  entendió mal.
- **US3 (T017-T018)**: depende de T004 (helpers) y del fixture T003; independiente
  de US2. Paralelizable con la Phase 4.
- **Phase 6 (T019-T021)**: T019 → T020 → T021. Depende de US1 (contrato de status),
  no de US2 ni US3. Paralelizable con las Phases 4 y 5.
- **Phase 7**: T022 depende de todo lo anterior; T023/T024 en cualquier momento tras
  US2; T025 al final.

## Parallel Examples

```bash
# Tras Phase 2, tres frentes independientes:
#   Frente A (US1, MVP):   T005 → T006 → T007 → T008 → T009 → T011 → T012
#   Frente B (US3):        T017 → T018
#   Frente C (comandos):   T010, T015, T023
# Tras US1: Phase 6 (T019 → T020 → T021) en paralelo con US2 (T013-T016).
```

## Implementation Strategy

**MVP primero (US1)**: al cerrarla, un proyecto corta ya se declara, salta
`constitution` y `plan`, y exporta un PDF de pieza única. La revisión aún corre en
cuatro pasadas (ceremonia estándar sobre una pieza) — que es exactamente la
degradación grácil que el diseño promete: US2 es una optimización de coste, no un
requisito de corrección.

Cada checkpoint de fase exige la suite completa en verde antes de avanzar. La regla
FR-010 (retrocompatibilidad en `estandar`) se verifica en **cada** checkpoint, no
solo al final: el test de oráculo de T008 es el que la congela.

**Señal de que algo se torció**: si una tarea de US2 o de la Phase 6 te empuja a
modificar `_next_step`, `choose_review_action` o `effect_satisfied`, para y relee
research.md § R1. El diseño entero descansa en que esos tres no cambian.
