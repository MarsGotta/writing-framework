# Feature Specification: Pista corta editorial (ceremonia adaptativa)

**Feature Branch**: `006-pista-corta-editorial`
**Created**: 2026-07-09
**Status**: Draft
**Input**: User description: "Pista corta editorial: ceremonia adaptativa a escala para piezas únicas (artículo, post, tutorial breve, ensayo corto). Hoy el método cobra el mismo rito a una pieza de 2.000 palabras que a un libro de 12 capítulos (~13 pasos LLM; la corrida BYOM real gastó 26 despachos en 2 capítulos). Alcance: (1) campo `track` en el manifiesto (`estandar`/`corta`); (2) brief compacto que materializa el temario degenerado de una fila; (3) revisión en dos relevos (pasada combinada 1·2·3·5 + precisión 4) SIN tocar pass-output ni status.py; (4) export digno de pieza única sin intro; (5) escalado corta→estandar sin tirar trabajo. Adoptado del análisis de BMAD v6 § Quick Flow (docs/comparativa-bmad.md). Ortogonal a los modos produccion/estudio (005)."

> **Restricción de ejecución (no negociable)**: la implementación la hará un
> agente distinto del que redactó esta spec. Spec, plan y tareas deben ser
> autocontenidos y agente-neutrales (Principio VI): rutas explícitas,
> contratos por archivo y criterios de aceptación verificables por script
> (`python3 -m pytest tests/unit -q`, `bash tests/smoke/run-all.sh`,
> `cd vivarium && cargo test --workspace`).

## Contexto

El método ejecuta hoy una sola ceremonia, dimensionada para libro: adendas →
brief → research → temario → redacción por capítulo → 3 pasadas locales + 1
global → intro → export → feedback → close. Para una guía de 10 capítulos ese
rito es la garantía de calidad; para un artículo de 2.000 palabras es un
impuesto que deja las piezas cortas fuera del método (se escriben "a mano",
sin voz calibrada, sin factualidad, sin registro). La evidencia de coste es
propia: la validación BYOM real (2026-07-08) necesitó 26 despachos para 2
capítulos; el camino feliz de una pieza única por la ceremonia estándar son
~13 pasos, de los cuales al menos dos (temario multi-capítulo, README de
presentación) son vacuos en pieza única.

BMAD v6 resolvió este mismo problema en su dominio con pistas de ceremonia
adaptativas a escala (Quick Flow / Method / Enterprise) y escalado que
arrastra el trabajo hecho (`docs/comparativa-bmad.md`, § "Qué adoptamos").
Esta feature trae esa idea al método editorial **sin abrir ningún contrato**:
la pista corta degenera artefactos (temario de una fila, dos relevos de
revisión), no elimina garantías (brief firmado, cinco dimensiones, voz ≠
precisión, escribe-uno-revisa-otro, claims en produccion, dos checkpoints
humanos, gates deterministas).

## Clarifications

### Session 2026-07-09

- Q: ¿Cómo despacha el ejecutor la pasada combinada (1·2·3·5) en pista corta? → A: El despacho existente de la pasada 1 se vuelve consciente de pista y registra los bloques 1·2·3·5 en un único run; el ejecutor no cambia (ve el bloque 1 y pasa a la 4).
- Q: ¿Corre `constitution` como despacho en el camino corto? → A: No en el camino feliz: `bootstrap --sector` fija sector y adendas con los defaults del sector; `constitution` solo se despacha si `sector` queda null (o para ajustar a mano).
- Q: ¿Cómo se ve el PDF de pieza única? → A: Portada compacta (título, autora, fecha), sin índice; la sección Fuentes conserva el estilo `.chapter-sources`.
- Q: ¿Mecanismo del escalado corta→estandar? → A: Script determinista dedicado (`scripts/track.py`), patrón `dispose.py`: identidad humana de git, validación de legalidad y escritura atómica de `track` + `track_history`.
- Q: ¿Quién fija título y promesa del temario degenerado? → A: La operadora, dentro del brief compacto: son campos firmables del checkpoint 1 y se materializan tal cual en `plan.md`.

## User Stories

### User Story 1 - Declarar la pista y recorrer el ciclo corto (Priority: P1)

Una operadora quiere publicar un artículo técnico con la voz y las garantías
de la casa. Crea el proyecto declarando pista corta, firma un brief compacto
(los ocho campos más el título y la promesa de la pieza, en una sola ronda de
preguntas) y, con la firma, el sistema materializa el temario degenerado: una
fila con ese título y esa promesa. A partir de ahí el ciclo corre como siempre — research con citas,
redacción con la pirámide de prosa, revisión, export — pero sin paso de
temario, sin README de presentación y con el export produciendo un PDF digno
de pieza única. El camino feliz cuesta como máximo 8 despachos donde la
ceremonia estándar costaría ~13.

**Why this priority**: es la feature — sin el ciclo corto operativo de punta
a punta no hay nada que revisar ni escalar. Las otras dos stories dependen de
que la pista exista y la brújula la recorra.

**Independent Test**: con un proyecto fixture `track: corta` en produccion,
un script recorre brief → research → redacción → pasadas → export → close
verificando que la brújula jamás devuelve `plan` ni exige intro, y que el
total de despachos del camino feliz (sin ciclos de revise) es ≤ 8.
Verificable con stubs, sin agentes reales.

**Acceptance Scenarios**:

1. **Given** un proyecto con `track: corta` en el manifiesto y brief firmado,
   **When** se consulta el estado, **Then** el temario degenerado ya existe
   (1 fila derivada del brief), `chapters_expected == 1` y la brújula nunca
   devuelve el paso `plan`.
2. **Given** el mismo proyecto con research y pieza redactada y revisada,
   **When** el ejecutor corre las etapas globales, **Then** no exige README
   de presentación (intro omitido) y el export produce un PDF de pieza única
   (portada compacta — título, autora, fecha —; sin índice de capítulos).
3. **Given** el camino feliz completo (0 ciclos de revise), **When** se
   cuentan los despachos en `decisions.jsonl`, **Then** son ≤ 8 (agentes +
   sidecar), frente a ~13 de la ceremonia estándar para la misma pieza.
4. **Given** un proyecto sin campo `track` o con `track: estandar`, **When**
   se consulta el estado en cualquier fase, **Then** la salida es idéntica a
   la actual (retrocompatibilidad total, espejo de FR-011 de la 005).
5. **Given** un manifiesto con `track` desconocido, **When** cualquier script
   lo lee, **Then** falla con mensaje claro (mismo patrón que `mode`
   desconocido).

---

### User Story 2 - Cinco dimensiones, dos relevos (Priority: P2)

Con la pieza redactada, la revisión corre en dos relevos en lugar de cuatro:
una **pasada combinada** verifica estructura, utilidad, naturalidad y formato
(dimensiones 1·2·3·5 — la coherencia entre capítulos es vacua en pieza
única), y la **pasada de precisión** (dimensión 4) sigue aparte, con otro
agente/modelo, verificando fuentes en vivo y emitiendo `claims.md` en
produccion. Los hallazgos van al `findings.md` de siempre, con los bloques de
pasada de siempre: ninguna herramienta del método nota la diferencia.

**Why this priority**: la revisión es donde vive la mitad del ahorro y todo
el riesgo constitucional — colapsar mal las pasadas rompería voz ≠ precisión
o dejaría dimensiones sin verificar. Depende de US1 (la pista debe existir).

**Independent Test**: sobre un fixture con la pieza escrita, se simula la
pasada combinada (un solo run que registra los bloques 1, 2, 3 y 5) y la de
precisión (bloque 4 + claims); un script verifica que `status.py` — sin
ninguna modificación en su parser — marca el capítulo `approved` y el
proyecto cerrable, y que las cinco dimensiones constan en `findings.md`.

**Acceptance Scenarios**:

1. **Given** la pieza redactada, **When** un agente ejecuta la pasada
   combinada, **Then** `findings.md` gana los bloques estándar de las pasadas
   1, 2, 3 y 5 (esquema pass-output intacto, "Capítulos cubiertos: 1" y
   "global" para la 5), en un único despacho.
2. **Given** la pasada combinada registrada, **When** el ejecutor consulta el
   estado, **Then** el siguiente despacho es la pasada 4 (precisión) para
   otro rol/modelo, que en produccion emite además `claims.md`; con las cinco
   dimensiones registradas y sin accionables abiertos, `by_chapter["1"]`
   queda `approved` **sin cambio alguno en `status.py`**.
3. **Given** hallazgos accionables (crítico/medio) de cualquiera de los dos
   relevos, **When** se consulta el estado, **Then** el ciclo es el de
   siempre: `revise` despachable en produccion, checkpoint de disposición en
   estudio (005).
4. **Given** una pasada combinada que solo registró parte de sus bloques (el
   agente se quedó a medias), **When** el ejecutor continúa, **Then** los
   comandos sueltos por dimensión (`review-structure`, `review-voice`,
   `review-global`) siguen disponibles y rellenan los huecos — la pasada
   combinada es una comodidad, no un punto único de fallo.
5. **Given** un proyecto `track: corta` + `mode: estudio` con la pieza
   escrita por la humana, **When** corren los dos relevos, **Then** producen
   solo hallazgos (jamás prosa), las huellas sha256 de la 005 aplican igual y
   la disposición sigue siendo humana (matriz track × mode completa).

---

### User Story 3 - Escalar sin tirar trabajo (Priority: P3)

A mitad de camino la pieza revela que quiere ser guía. La operadora escala el
proyecto a pista estándar con una acción explícita: el brief se conserva, la
pieza pasa a ser el capítulo 1 del temario ampliado, los hallazgos y claims
existentes siguen valiendo, y el cambio queda registrado en el manifiesto con
fecha y actor. Ningún agente puede escalar o des-escalar por su cuenta.

**Why this priority**: el escalado es lo que hace segura la elección inicial
— sin él, elegir pista corta sería una trampa y la operadora elegiría siempre
estándar "por si acaso", matando la feature. Es P3 porque exige US1/US2
operativas.

**Independent Test**: sobre un fixture corta con pieza + findings + claims,
se ejecuta `scripts/track.py --escalar` y se verifica que el manifiesto registra
`track: estandar` + historial, que el temario admite N filas manteniendo la
pieza como capítulo 1, y que `status.py` pide los capítulos 2..N sin
invalidar las pasadas ya registradas del 1.

**Acceptance Scenarios**:

1. **Given** un proyecto corta con pieza aprobada, **When** la humana escala
   a estándar y amplía el temario a 4 capítulos, **Then** el manifiesto
   registra el cambio (pista nueva, fecha, actor humano) en un historial
   apéndice (espejo de `mode_history`), y la brújula pasa a pedir los
   capítulos 2-4 conservando `approved` del 1.
2. **Given** un proyecto estándar con temario de más de una fila, **When**
   alguien intenta des-escalar a corta, **Then** la operación se rechaza con
   mensaje claro (la pista corta exige pieza única; des-escalar solo es
   legal antes de ampliar el temario).
3. **Given** cualquier proyecto, **When** un agente intenta cambiar `track`,
   **Then** el cambio requiere acción humana explícita (misma política que el
   cambio de modo: los defaults son opinados, no candados; el cambio es del
   humano operador).

---

### Edge Cases

- Pieza que crece en disco sin escalar (la operadora añade `02-*.md` a
  `chapters/` con temario de 1): la brújula reporta el capítulo fuera de
  temario sin romperse (mismo comportamiento tolerante que la 005) y el
  detalle del estado sugiere escalar; no bloquea.
- `track: corta` con temario editado a mano a más de una fila: estado
  inconsistente detectado con mensaje claro — la pista corta declara pieza
  única; o se corrige el temario o se escala.
- Brief compacto rechazado en el checkpoint 1: mismo contrato que hoy — el
  ciclo no avanza sin firma humana; el temario degenerado no se materializa
  hasta que el brief queda firmado (nace del brief, no antes).
- Pasada combinada y de precisión ejecutadas por el mismo agente/modelo en
  BYOM mal configurado: misma exposición que hoy tiene el reparto Mesa/Doc —
  la config BYOM asigna roles distintos y el smoke lo verifica con stubs
  distinguibles; el método lo declara MUST en los comandos.
- Export de pieza única: portada compacta y sin índice (clarificado
  2026-07-09); el plan fija solo los detalles de la hoja de estilo de la
  cabecera compacta (tipografía, márgenes), no la decisión.
- Proyecto legado (sin `track`) que quiere volverse corta antes de empezar:
  legal mientras el temario tenga ≤ 1 fila y no haya capítulos 2+; misma
  acción humana registrada.

## Requirements

### Functional Requirements

- **FR-001**: El manifiesto (`.writeonmars-manifest.json`) MUST admitir el
  campo opcional `track` con valores `estandar` | `corta` (ausencia =
  `estandar`; valor desconocido = error claro, espejo de `mode`), más un
  historial de cambios (`track_history`, espejo de `mode_history`).
  `manifest-schema.json` sube MINOR. `status.py` MUST exponer `track` en
  `--json` (espejo de `mode`); ningún otro cambio en la brújula es admisible
  para esta feature.
- **FR-002**: `bootstrap.py` MUST aceptar `--track` (y variable de entorno
  `WRITEONMARS_TRACK`) con default `estandar`, escribiéndolo en el manifiesto
  al crear el proyecto. MUST aceptar también `--sector`, que fija el sector
  del manifiesto y deja las adendas con los defaults de
  `references/sectores/<sector>.md`: con sector fijado, la brújula no pide el
  paso `constitution` en el camino corto (ya lo omite con `sector` no nulo) y
  el comando queda disponible para calibrar adendas a mano.
- **FR-003**: En pista corta, el comando de brief (`speckit.specify`) MUST
  capturar los ocho campos descriptivos **más el título y la promesa de la
  pieza** en una sola ronda compacta (checkpoint humano 1 intacto: sin firma
  no hay avance) y, al quedar firmado el brief, MUST materializar el
  **temario degenerado** — una fila con el título y la promesa firmados, tal
  cual — en el artefacto que la brújula ya lee
  (`plan.md` § Temario), de modo que `chapters_expected == 1` y el paso
  `plan` desaparezca del ciclo sin modificar `status.py`.
- **FR-004**: El research en pista corta MUST conservar íntegro el contrato
  de citación (una cita por concepto obligatorio del brief; bloquea si un
  concepto queda sin respaldo) y MUST limitar su alcance a los conceptos del
  brief (research exprés: sin panorama ni estado del arte).
- **FR-005**: La revisión en pista corta MUST ejecutarse en dos relevos: (a)
  **pasada combinada** que verifica las dimensiones 1 (estructura), 2
  (utilidad), 3 (naturalidad) y 5 (formato; la coherencia inter-capítulos es
  vacua en pieza única) y las registra como los bloques de pasada estándar
  existentes (esquema pass-output sin cambios, un bloque por dimensión),
  **vehiculada por el despacho existente de la pasada 1** (consciente de
  pista: ese run verifica y registra 1·2·3·5; el ejecutor no cambia — ve el
  bloque 1 registrado y pasa a la 4); (b)
  **pasada de precisión** (dimensión 4) en relevo aparte, con rol/modelo
  distinto, que en produccion emite `claims.md` (feature 003 íntegra). Las
  reglas duras se preservan: escribe-uno-revisa-otro, voz ≠ precisión,
  detector ≠ corrector.
- **FR-006**: Los comandos sueltos por dimensión (`review-structure`,
  `review-voice`, `review-precision`, `review-global`) MUST seguir operativos
  en pista corta como red de reparación (rellenar bloques que la combinada
  dejara incompletos, re-pasar una dimensión suelta).
- **FR-007**: En pista corta el paso `intro` (README de presentación) MUST
  omitirse: el ejecutor MUST NOT exigir `README.md` antes del export (cambio
  acotado a `plan_global` en `vivarium-core`, único cambio admisible en el
  ejecutor), y `export.py` MUST producir el PDF de pieza única con **portada
  compacta** (título, autora, fecha) en lugar de la portada de libro, **sin
  índice** de capítulos, conservando la sección Fuentes con el estilo
  `.chapter-sources`.
- **FR-008**: El escalado `corta → estandar` MUST ejecutarse con un script
  determinista dedicado (`scripts/track.py`, patrón `dispose.py`: identidad
  humana desde git config con rechazo de identidades de agente, validación de
  legalidad, escritura atómica) que registra el cambio en el manifiesto
  (pista nueva, fecha, actor humano) y conserva todo el trabajo: brief, pieza (pasa a capítulo 1 del temario
  ampliado), findings, claims y pasadas registradas. El des-escalado
  `estandar → corta` MUST rechazarlo el mismo script si el temario tiene más de una fila o
  existen capítulos 2+. Ningún agente MUST cambiar `track` (misma política
  que `mode`).
- **FR-009**: La pista MUST ser ortogonal al modo (matriz 2×2 completa): en
  `corta`+`estudio`, los checkpoints de escritura y disposición de la 005,
  las huellas sha256 y el guardarraíl exit 11 operan sin cambios sobre la
  pieza única; la pasada combinada y la de precisión producen solo hallazgos.
- **FR-010**: Retrocompatibilidad total: para proyectos sin `track` o con
  `track: estandar`, la salida de la brújula, los comandos y el ejecutor son
  los actuales; la suite existente (unitarios + smoke + cargo) pasa sin
  modificar ninguna aserción previa (solo adiciones).
- **FR-011**: La constitución MUST enmendarse en MINOR con una sección
  **"Pistas de ceremonia"** paralela a "Modos de proyecto" (la pista gobierna
  cuánto rito; el modo, quién escribe): en pista corta las cinco dimensiones
  del Principio V se verifican en dos relevos (combinada 1·2·3·5 + precisión
  4) sin debilitar ningún NO NEGOCIABLE; defaults opinados sin candados;
  cambio de pista solo humano y registrado. Sync impact report en cabecera y
  propagación a plantillas (`plan-template` § Constitution Check gana la fila
  "Pista de ceremonia").
- **FR-012**: El preset MUST incluir un smoke e2e de pista corta con stubs
  deterministas (espejo de `estudio-e2e.sh`): produccion camino feliz (≤ 8
  despachos, exit 10 en los dos checkpoints, close verde) + verificación de
  la matriz con estudio. Se registra en `tests/smoke/run-all.sh`.

### Key Entities

- **Pista de ceremonia (`track`)**: cuánto rito paga el proyecto — `estandar`
  (ceremonia completa actual) o `corta` (pieza única, temario degenerado, dos
  relevos de revisión, sin intro). Ortogonal al modo. Vive en el manifiesto
  con historial de cambios.
- **Temario degenerado**: la fila única (título + promesa firmados en el
  brief) que la firma del checkpoint 1 materializa en `plan.md`; hace `chapters_expected == 1` sin tocar
  la brújula y da al export su portada/estructura.
- **Pasada combinada**: un despacho que verifica y registra las dimensiones
  1·2·3·5 como bloques pass-output estándar. Comodidad de ceremonia, no
  contrato nuevo: sus bloques son indistinguibles de los de pasadas sueltas.
- **Registro de escalado (`track_history`)**: apéndice del manifiesto con
  cada cambio de pista (de, a, fecha, actor humano), espejo de
  `mode_history`. Lo escribe `scripts/track.py`; nunca se edita a mano.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Una pieza única en `corta`+`produccion` se recorre de punta a
  punta (brief → close) con **≤ 8 despachos** en el camino feliz (0 revise),
  contados en `decisions.jsonl`, frente a ~13 de la ceremonia estándar para
  la misma pieza; reproducible como smoke con stubs.
- **SC-002**: Las cinco dimensiones del Principio V constan en `findings.md`
  (bloques 1-5) también en pista corta, y `claims.md` existe en produccion:
  cero garantías perdidas, verificable por script sobre el fixture.
- **SC-003**: `status.py` no cambia su lógica de estado (solo expone
  `track`): los fixtures existentes producen salida byte-idéntica y el
  fixture corta alcanza `approved`/`closeable` con el parser actual.
- **SC-004**: El escalado del fixture corta conserva el 100% del trabajo
  previo (brief, pieza como capítulo 1, findings, claims, pasadas) y queda
  registrado con actor humano; el des-escalado ilegal se rechaza con mensaje
  claro.
- **SC-005**: Matriz track × mode: el fixture `corta`+`estudio` se recorre
  con el ejecutor deteniéndose en los checkpoints humanos (escritura,
  disposición, feedback) sin despachar redacción (guardarraíl exit 11
  intacto).
- **SC-006**: Gate final en verde: unitarios, smoke (`run-all.sh` con el
  nuevo e2e) y `cargo test --workspace`, en local y en CI, sin pasos manuales
  no documentados.

## Assumptions

- **Una pieza por proyecto**: la pista corta modela un repo = una pieza
  (igual que un repo = una guía). El multi-pieza (blog/columna con N
  artículos en un repo) queda explícitamente fuera de alcance; si algún día
  llega, será otra feature con su propia semántica de temario.
- **Sin detección automática de escala**: la pista se declara a mano en
  `bootstrap` y se cambia por escalado explícito. Las "alertas de alcance"
  automáticas al estilo BMAD (detectar que una pieza pide ser guía) quedan
  como idea de roadmap, no de esta spec.
- **El reparto de roles BYOM no cambia**: combinada → editora de mesa,
  precisión → documentalista, redacción/revise → redactora. La config
  `.vivarium/config.toml` existente sirve tal cual.
- **Los comandos de pasada se vuelven conscientes de pista** (clarificado
  2026-07-09): el despacho de la pasada 1 (`review-structure`) vehicula la
  combinada en corta — un run que verifica y registra los bloques 1·2·3·5 —,
  el agrupado `review` ejecuta combinada + precisión, y los sueltos restantes
  quedan como red de reparación.
- **`speckit.constitution` queda opcional en pista corta** (clarificado
  2026-07-09): `bootstrap --sector` deja las adendas con los defaults del
  sector al crear el proyecto y la brújula no lo pide (sector no nulo); el
  comando sigue disponible para calibrar las adendas a mano cuando la pieza
  lo pida.
- **Trazabilidad documental** (constitución § Arquitectura): decisión propia
  del proyecto con fundamento externo en el análisis de BMAD v6
  (`docs/comparativa-bmad.md`: pistas Quick Flow / Method / Enterprise,
  escalado con arrastre de trabajo) y en la evidencia de coste propia
  (`tests/editorial-pilot/evidence/2026-07-08-vivarium-byom/`: 26 despachos
  para 2 capítulos).
