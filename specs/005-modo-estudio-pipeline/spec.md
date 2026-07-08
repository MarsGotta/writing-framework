# Feature Specification: Pipeline del modo estudio en el preset

**Feature Branch**: `005-modo-estudio-pipeline`
**Created**: 2026-07-08
**Status**: Draft
**Input**: User description: "Pipeline del modo estudio en el preset writeonmars (el humano escribe, la IA revisa y acompaña; constitución v1.6.0 § Modos de proyecto). Alcance: (1) semántica de status.py con mode: estudio; (2) pasadas editoriales sobre texto humano con hallazgos, nunca prosa; (3) ciclo de aceptación por archivos con registro auditable; (4) informe de autoría humana desde git + decisions.jsonl; (5) integración con Vivarium sin tocar el guardarraíl exit 11. LA IMPLEMENTACIÓN LA HARÁ CODEX: artefactos autocontenidos y agente-neutrales."

> **Restricción de ejecución (no negociable)**: la implementación la hará un
> agente distinto del que redactó esta spec (Codex). Spec, plan y tareas deben
> ser autocontenidos y agente-neutrales (Principio VI): rutas explícitas,
> contratos por archivo y criterios de aceptación verificables por script
> (`uvx --with pytest --with pyyaml python -m pytest tests/unit -q`,
> `bash tests/smoke/run-all.sh`, `cd vivarium && cargo test --workspace`).

## Contexto

La constitución v1.6.0 define el modo `estudio` (el humano escribe; la IA
MUST NOT redactar prosa del manuscrito) y el ejecutor Vivarium ya lo protege
con un guardarraíl (bloquea `implement`/`revise`/`intro`, exit 11). Pero el
preset no sabe operar en ese modo: `status.py` ignora el campo `mode` y, ante
capítulos faltantes, pide "delegar a Redactora" — una instrucción que en
estudio ningún agente puede cumplir. Resultado: un proyecto `estudio` hoy se
queda clavado en el guardarraíl sin camino hacia adelante. Esta feature da al
modo estudio su pipeline completo: estado, pasadas sobre texto humano, ciclo
de aceptación de hallazgos y garantía de autoría demostrable.

## User Stories

### User Story 1 - La brújula entiende el modo estudio (Priority: P1)

Una escritora crea un proyecto en modo estudio y escribe sus capítulos a su
ritmo. Cada vez que consulta el estado (directamente o a través del ejecutor),
el sistema le dice con precisión qué toca: si faltan capítulos, el paso es
**suyo** (escribir), nunca una delegación a la IA; si hay capítulos listos sin
revisar, el paso es despachable a los agentes revisores. El ejecutor puede
correr el ciclo completo deteniéndose en los pasos humanos sin quedarse nunca
bloqueado ni intentar redactar.

**Why this priority**: sin una brújula consciente del modo, todo lo demás es
inoperable — el ejecutor se estrella contra el guardarraíl y el proyecto
estudio no tiene siquiera un "siguiente paso" válido. Es el prerrequisito de
las otras dos stories.

**Independent Test**: con un proyecto fixture en modo estudio y capítulos
faltantes, la salida de estado declara un paso de escritura humana (no
despachable); al añadir un capítulo escrito a mano, el paso pasa a ser una
pasada de revisión despachable. Verificable por script sin agentes.

**Acceptance Scenarios**:

1. **Given** un proyecto con `mode: estudio`, brief y temario de 3 capítulos
   y 0 capítulos escritos, **When** se consulta el estado, **Then** el
   siguiente paso es un checkpoint humano de escritura (identificable por
   máquina como no-despachable) que nombra los capítulos pendientes, y ningún
   texto del estado instruye delegar redacción a un agente.
2. **Given** el mismo proyecto con el capítulo 1 escrito por la humana,
   **When** se consulta el estado, **Then** el siguiente paso es la primera
   pasada de revisión del capítulo 1, despachable a un agente revisor.
3. **Given** un proyecto con `mode: produccion` (o sin campo `mode`),
   **When** se consulta el estado, **Then** la salida es idéntica a la del
   comportamiento actual (retrocompatibilidad total).
4. **Given** un proyecto estudio con capítulos pendientes de escritura,
   **When** el ejecutor orquestado corre su ciclo, **Then** se detiene en el
   checkpoint de escritura con la señal de "checkpoint humano" existente (la
   misma que usa para el brief), sin despachar nada y sin activar el
   guardarraíl de modo.

---

### User Story 2 - Pasadas sobre texto humano y ciclo de aceptación (Priority: P2)

Con capítulos escritos, la escritora lanza (o el ejecutor despacha) las
pasadas de revisión. Los agentes leen su texto y producen hallazgos
priorizados con sugerencias concretas — pero jamás tocan el manuscrito. Ella
revisa cada hallazgo y **dispone**: lo acepta (y aplica el cambio ella misma),
lo rechaza (con motivo) o lo aplaza. Solo sus disposiciones desbloquean el
avance; ningún agente puede dar un hallazgo por resuelto.

**Why this priority**: es el corazón del valor del modo estudio — "la IA
detecta y propone; el humano dispone" (constitución § Modos de proyecto). Sin
el ciclo de aceptación, las pasadas serían o inertes (hallazgos que nadie
procesa) o inconstitucionales (agentes resolviendo hallazgos).

**Independent Test**: sobre un proyecto fixture con un capítulo humano y una
pasada con hallazgos registrados, un script simula las tres disposiciones
humanas y verifica que el estado solo avanza con disposición registrada;
un intento de resolución sin disposición humana no reduce los pendientes.

**Acceptance Scenarios**:

1. **Given** un capítulo escrito por la humana, **When** un agente ejecuta una
   pasada de revisión en modo estudio, **Then** el resultado son hallazgos
   priorizados (crítico/medio/bajo) con sugerencia accionable por hallazgo, y
   el contenido del capítulo permanece byte a byte intacto.
2. **Given** hallazgos accionables abiertos (crítico/medio), **When** se
   consulta el estado, **Then** el siguiente paso es un checkpoint humano de
   disposición (no-despachable): el sistema espera a la escritora, no envía
   una tarea `revise` a la Redactora.
3. **Given** un hallazgo aceptado por la humana (con su corrección aplicada
   por ella al capítulo) y otro rechazado con motivo, **When** se consulta el
   estado, **Then** ambos dejan de contar como pendientes y cada disposición
   queda registrada de forma auditable con autor humano y fecha.
4. **Given** un hallazgo aplazado, **When** se cierra el proyecto, **Then** el
   hallazgo aplazado queda documentado como deuda declarada (no bloquea el
   cierre pero tampoco desaparece en silencio).
5. **Given** un proyecto estudio, **When** cualquier agente intenta marcar un
   hallazgo como resuelto o editar el manuscrito, **Then** existe un control
   verificable que lo detecta o lo neutraliza (el estado no avanza y la
   violación es visible).

---

### User Story 3 - Informe de autoría humana (Priority: P3)

Al cerrar (o en cualquier momento), la escritora genera el informe de autoría
humana: un documento derivado del historial del repositorio y del registro de
decisiones que evidencia, capítulo a capítulo, que la prosa del manuscrito fue
escrita por humanos — la garantía de procedencia que diferencia el modo
estudio y habilita certificaciones de autoría humana.

**Why this priority**: es la recompensa del modo estudio y depende de que US1
y US2 hayan mantenido el manuscrito libre de prosa de IA; sin ellas el informe
no tendría nada que demostrar.

**Independent Test**: sobre un repositorio fixture con commits humanos en los
capítulos y despachos de revisión registrados, el informe clasifica el 100%
de los cambios del manuscrito y dos ejecuciones consecutivas producen el mismo
resultado (determinismo).

**Acceptance Scenarios**:

1. **Given** un proyecto estudio con capítulos escritos en commits humanos y
   pasadas de IA registradas en el log de decisiones, **When** se genera el
   informe, **Then** cada capítulo aparece con su evidencia de autoría (quién
   escribió cada cambio del manuscrito) y el veredicto global es "autoría
   humana demostrada".
2. **Given** un proyecto donde un agente redactó prosa antes de un cambio a
   modo estudio (proyecto convertido), **When** se genera el informe, **Then**
   los tramos con prosa de IA quedan señalados honestamente y el veredicto
   global lo refleja — el informe nunca certifica lo que el historial no
   soporta.
3. **Given** el mismo proyecto sin cambios, **When** se genera el informe dos
   veces, **Then** ambas salidas son idénticas.

---

### Edge Cases

- Proyecto estudio con capítulos en disco que no están en el temario (la
  escritora escribió de más o fuera de orden): el estado los reporta sin
  romperse y sin exigir revisión de capítulos no declarados.
- La escritora edita sustancialmente un capítulo ya aprobado: el sistema
  detecta que el texto cambió después de las pasadas y reabre la necesidad de
  revisión de ese capítulo (una aprobación no puede referirse a texto que ya
  no existe).
- Un hallazgo rechazado reaparece en una pasada posterior (el agente vuelve a
  detectar lo mismo): el registro de la disposición previa permite
  identificarlo como ya-dispuesto y no reabre el ciclo en bucle.
- Registro de disposiciones editado a mano con un estado inválido: el estado
  falla con mensaje claro, no con silencio ni con interpretación creativa.
- Cambio de modo en caliente con hallazgos abiertos o capítulos a medias: el
  estado del pipeline sobrevive al cambio en ambas direcciones y las
  consecuencias de procedencia quedan registradas (lo ya escrito conserva su
  autoría).
- Proyecto estudio donde el humano nunca dispone de los hallazgos: el sistema
  espera indefinidamente en el checkpoint (esperar al humano no es un error),
  y cada consulta de estado lo recuerda con claridad.

## Requirements

### Functional Requirements

- **FR-001**: La brújula del método (`writeonmars/scripts/status.py`) MUST
  leer el campo `mode` del manifiesto (`.writeonmars-manifest.json`; ausencia
  = `produccion`) y exponerlo en su salida de máquina (`--json`).
- **FR-002**: En modo estudio, cuando falten capítulos del temario, la brújula
  MUST devolver un paso de **escritura humana** distinguible por máquina como
  checkpoint no-despachable (mismo mecanismo de señal que el checkpoint del
  brief), nombrando los capítulos pendientes; MUST NOT devolver ningún paso
  que instruya a un agente a redactar.
- **FR-003**: En modo estudio, cuando existan hallazgos accionables abiertos
  (crítico/medio), la brújula MUST devolver un paso de **disposición humana**
  (checkpoint no-despachable) en lugar del paso `revise` despachable del modo
  producción.
- **FR-004**: Las pasadas de revisión (1-4 locales, 5 global) MUST operar en
  modo estudio sobre los capítulos escritos por el humano produciendo
  exclusivamente hallazgos priorizados (crítico/medio/bajo) con sugerencia
  accionable, en el registro de hallazgos existente
  (`specs/<feature>/findings.md`, esquema pass-output); los comandos de pasada
  MUST declarar explícitamente la prohibición de editar `chapters/` cuando
  `mode: estudio`.
- **FR-005**: El sistema MUST ofrecer un mecanismo por archivos para que el
  humano registre la **disposición** de cada hallazgo — aceptado / rechazado
  (con motivo) / aplazado — con autor humano y fecha, procesado por un script
  determinista (sin LLM) que valide estados y actualice el registro de
  hallazgos de forma auditable.
- **FR-006**: Un hallazgo accionable MUST dejar de contar como pendiente
  únicamente mediante una disposición humana registrada (FR-005). Ningún
  agente MUST poder marcar hallazgos como resueltos: las instrucciones de los
  comandos lo prohíben y el formato del registro de disposiciones exige el
  actor humano declarado.
- **FR-007**: Los hallazgos aplazados MUST quedar documentados como deuda
  declarada en el cierre del proyecto: no bloquean `close`, pero aparecen en
  el resumen de cierre y permanecen en el registro.
- **FR-008**: En modo estudio, si un capítulo aprobado cambia sustancialmente
  después de su última pasada, la brújula MUST reabrir la necesidad de
  revisión de ese capítulo (la aprobación se ancla al contenido revisado, no
  al nombre del archivo).
- **FR-009**: El preset MUST incluir un script determinista de **informe de
  autoría humana** que derive, del historial git del proyecto y de
  `decisions.jsonl`, la clasificación de cada cambio del manuscrito
  (`chapters/`) por autor; el informe MUST señalar honestamente cualquier
  prosa de origen agente (proyectos convertidos) y MUST ser reproducible (dos
  ejecuciones sin cambios = salida idéntica).
- **FR-010**: El pipeline de estudio MUST integrarse con el ejecutor Vivarium
  **sin modificar su guardarraíl de modo** (bloqueo de pasos que escriben
  manuscrito, exit 11): el runner despacha las pasadas de revisión y se
  detiene en los checkpoints humanos de escritura y disposición usando su
  mecanismo de checkpoint existente (exit 10). Un proyecto estudio MUST poder
  recorrerse de punta a punta con `vivarium run` + acciones humanas.
- **FR-011**: El comportamiento del modo producción MUST permanecer
  inalterado: para cualquier proyecto sin `mode` o con `mode: produccion`,
  la salida de la brújula y el flujo de pasadas son los actuales (los tests
  existentes siguen en verde sin modificarse, salvo adiciones).
- **FR-012**: El cierre en modo estudio MUST exigir los mismos checkpoints
  humanos globales del método (brief firmado; feedback sobre el artefacto
  exportado) y MUST poder completarse sin claims de factualidad: la pasada 4
  en estudio verifica consistencia contra las fuentes del proyecto (`roots/`)
  y el gate de factualidad solo aplica si el proyecto declara umbral.

### Key Entities

- **Disposición de hallazgo**: decisión humana sobre un hallazgo de pasada —
  aceptado / rechazado (con motivo) / aplazado — con identificador del
  hallazgo, actor humano, fecha y comentario opcional. Es el único mecanismo
  que resuelve hallazgos en modo estudio.
- **Checkpoint de escritura**: estado no-despachable que nombra los capítulos
  del temario pendientes de escritura humana.
- **Checkpoint de disposición**: estado no-despachable que enumera los
  hallazgos accionables a la espera de decisión humana.
- **Informe de autoría humana**: documento derivado (git + decisions.jsonl)
  que clasifica cada cambio del manuscrito por autor y emite un veredicto de
  autoría por capítulo y global. Se regenera bajo demanda; nunca se edita a
  mano.

## Success Criteria

### Measurable Outcomes

- **SC-001**: En un proyecto estudio recorrido de punta a punta, el 100% de
  los cambios de contenido bajo `chapters/` provienen de acciones humanas
  (verificable por el historial del repositorio); cero prosa del manuscrito
  generada por agentes.
- **SC-002**: Un proyecto estudio con temario de 2 capítulos se recorre
  completo con el ejecutor orquestado deteniéndose exactamente en los
  checkpoints humanos (brief, escritura por capítulo pendiente, disposiciones,
  feedback) y termina cerrado; reproducible como smoke test con stubs
  deterministas.
- **SC-003**: El informe de autoría clasifica el 100% de los commits que tocan
  el manuscrito del fixture y dos ejecuciones consecutivas producen salida
  byte a byte idéntica.
- **SC-004**: Los proyectos en modo producción no cambian: la suite de tests
  existente (unitarios + smoke) pasa sin modificar ninguna aserción previa.
- **SC-005**: Ningún hallazgo accionable pasa a resuelto sin disposición
  humana registrada: existe un test que intenta el atajo (resolver sin
  disposición) y demuestra que el estado no avanza.
- **SC-006**: Gate final en verde: unitarios, smoke y tests del ejecutor
  (`cargo test --workspace`) sin pasos manuales no documentados.

## Assumptions

- **La pasada 4 en modo estudio** verifica consistencia del texto humano
  contra las fuentes del proyecto (`roots/`) y produce hallazgos; el índice de
  factualidad con claims (feature 003) queda como opcional en estudio — solo
  se activa si el manifiesto declara umbral (`quality_gates`). La obligación
  constitucional de atribución por afirmación aplica al modo producción.
- **El mecanismo de disposición vive en archivos del repo** (registro junto a
  findings.md o en él), editado por el humano y validado por script; la
  interfaz gráfica de disposición es de Vivarium/Tauri y queda fuera de
  alcance.
- **"Cambio sustancial" de un capítulo aprobado** se define de forma
  determinista y barata (p. ej. huella del contenido registrada al aprobar);
  el umbral exacto lo fija el plan, no esta spec.
- **El informe de autoría usa la identidad de los commits** (autor git) más el
  registro de despachos (`decisions.jsonl`) para distinguir humano de agente;
  supone que los agentes comitean con identidad propia o que sus acciones
  constan como despachos — la convención exacta la fija el plan.
- **El guardarraíl de Vivarium no se toca**: `writes_manuscript`
  (implement/revise/intro) sigue bloqueado en estudio; los pasos nuevos del
  pipeline estudio son de revisión (despachables) o checkpoints (exit 10),
  nunca redacción.
- **Alcance del ejecutor**: los cambios en `vivarium/` se limitan a mapear los
  pasos/checkpoints nuevos que exponga la brújula; la lógica editorial vive en
  el preset (frontera dura de CLAUDE.md).
