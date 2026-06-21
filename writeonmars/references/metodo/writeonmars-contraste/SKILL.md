---
name: writeonmars-contraste
description: Verifica las afirmaciones del capítulo contra los CitationRecord del research.md Y contra la fuente real abierta en vivo (web) para los datos volátiles (pasada 4 — precisión). Trigger cuando la persona diga "verifica las afirmaciones del capítulo", "contraste de fuentes", "pasada 4", "valida precisión".
allowed-tools: Bash, Read, Write, Edit, WebFetch, WebSearch
---

# writeonmars-contraste

Skill que implementa la pasada 4 (precisión) en su capa de contraste:
verifica cada afirmación verificable del capítulo contra al menos un
`CitationRecord` de `research.md` Y, para lo volátil, contra la **fuente real
abierta en vivo** (la `url` de la cita o búsqueda web). No basta con que el
capítulo coincida con `research.md`: pudo citar mal o la fuente pudo cambiar.
Materializa FR-016 y FR-017 (+ feature 003: FR-005, FR-006, FR-007, FR-009).

Emite **dos** salidas (pass-output-schema v1.1):
- el bloque "Pasada 4" en `findings.md` (los hallazgos accionables), y
- el artefacto durable `claims.md` con un `ClaimRecord` por **cada** afirmación
  verificable evaluada (no solo las que fallan), clasificando la **relación** de
  cada cita con la afirmación (atribución por afirmación, grano de frase).

## Cuándo dispararse

- "verifica las afirmaciones del capítulo"
- "contraste de fuentes"
- "pasada 4"
- "valida precisión"
- Antes de invocar `writeonmars-pasada-4` (esta skill es su núcleo
  operativo; pasada-4 wrappea esta + la firma humana).

## Qué hace

1. Lee el capítulo objetivo y el `research.md` con todos los
   `CitationRecord`.
2. Extrae afirmaciones verificables del capítulo (heurística: oraciones
   con datos cuantitativos, versiones, comandos, precios, citas a
   estándares, fechas, nombres de productos).
3. Para cada afirmación, busca los `CitationRecord` candidatos y, **tras abrir la
   fuente**, clasifica la **relación** de cada cita con la afirmación (no basta con
   que exista la cita):
   - `apoya` — la fuente *implica/sostiene* la afirmación (registra el fragmento
     exacto de la fuente en `cita_fragmento_soporte`, obligatorio).
   - `matiza` — la sostiene **con caveats** (cierto en parte / con condiciones).
   - `contradice` — la fuente abierta **contradice** la afirmación.
   - `menciona` — la fuente es solo *temática*: toca el tema pero no sostiene el dato.
   De la relación se deriva el veredicto `soporte` del `ClaimRecord` (ver § "Atribución
   por afirmación"), que a su vez gobierna la severidad del finding.
4. **Verificación en vivo**: para datos volátiles (versiones, paquetes,
   comandos, precios, APIs; citas `volatil: true` o afirmaciones `[VERIFICAR]`),
   abre la `url` del `CitationRecord` (o busca la fuente en la web) y confirma el
   dato contra la fuente ACTUAL. Si la fuente contradice el capítulo o el
   `research.md` → `critico` (anota la URL y la discrepancia; actualiza
   `research.md` si procede). Sin acceso a web: marca "no verificado en vivo"
   (`medio`) sin fingir.
5. Emite el bloque "Pasada 4" en `findings.md` con un finding por
   afirmación no verificada y `referencias_cita` por afirmación
   verificada (campo obligatorio en pasada 4 según
   pass-output-schema § Finding).
6. Persiste/actualiza `claims.md` con un `ClaimRecord` por **cada** afirmación
   verificable evaluada (las que pasan también), reusando la misma detección de
   afirmaciones del paso 2 como denominador.

## Atribución por afirmación (claims.md)

Contrato: `claim-record.schema.json` v1.0 · estructura del fichero y algoritmo de
factualidad en `specs/003-atribucion-factualidad/data-model.md` § 1–3. `claims.md`
vive junto a `findings.md` en `specs/[###-feature]/`, agrupado por capítulo, con un
bloque ```json por capítulo (fuente de verdad de máquina para `status.py`) más una
tabla legible.

**Derivación de `soporte`** (peor relación presente, modulada por `tipo_afirmacion`):

```
alguna arista contradice            → contradicho
sin evidencia                       → sin_fuente
toda arista es 'menciona'           → sin_fuente si dato_duro, parcial si blanda
la mejor arista es 'matiza'         → parcial
existe al menos una 'apoya'         → soportado
dato volátil sin poder abrir fuente → pendiente   (sin web; NO se finge la verificación)
```

`pendiente` (no medible en vivo) ≠ `sin_fuente` (medible y sin respaldo).

**Mapeo de severidad del finding (FR-009)** — se enchufa al revise existente
(crítico+medio = accionable; bajo = aviso):

| Veredicto | Severidad |
|---|---|
| `contradicho` (cualquier afirmación) | `critico` |
| `sin_fuente` o `menciona`-solo en **dato duro** (versión, comando, precio, estándar, estadística, fecha, endpoint, paquete) | `critico` |
| `parcial` / `matiza`, o `sin_fuente` en afirmación blanda verificable | `medio` |
| dato volátil `pendiente` por falta de web | `medio` ("no verificado en vivo") |
| ambigüedad de mapeo afirmación↔cita | `bajo` (aviso) |

Reglas: una arista `apoya` exige `cita_fragmento_soporte` no vacío. Si un
`citation_id` candidato no resuelve en `research.md`, **no se emite la arista** y se
reporta (no se inventan fuentes). Trazabilidad: el finding de pasada 4 referencia el
`claim_id` afectado (campo `claim_id` o `claim:<id>` en la columna `Citas`).

**Idempotencia por capítulo (FR-007)**: re-ejecutar la pasada 4 sobre un capítulo
**reemplaza en bloque** sus `ClaimRecord` en `claims.md`; no duplica ni toca los de
otros capítulos.

## Inputs

- `chapters/[###]-titulo.md`.
- `specs/[###-feature]/research.md`.
- `specs/[###-feature]/findings.md` (existente; se añaden bloques al
  final).
- `specs/[###-feature]/claims.md` (existente o nuevo; se reemplaza por capítulo).
- `contracts/pass-output-schema.md` v1.1.
- `contracts/claim-record.schema.json` v1.0.

## Outputs

- Bloque "Pasada 4 — Precisión" añadido a
  `specs/[###-feature]/findings.md`, con `pasada: 4_precision` y la
  tabla de hallazgos completa.
- `specs/[###-feature]/claims.md` con un `ClaimRecord` por afirmación verificable
  del capítulo (relación + soporte + fragmento de soporte), reemplazado en bloque
  por capítulo (idempotente).

## Procedimiento

1. Cargar `CitationRecord` del `research.md` e indexarlos por
   `citation_id` y por palabras clave del `fragmento`.
2. Tokenizar el cuerpo del capítulo y detectar afirmaciones verificables.
3. Para cada afirmación, calcular candidatos por similitud léxica con
   los fragmentos. Pedir confirmación al operador en casos ambiguos.
4. Para cada cita usada, verificar:
   - `versionado_aplicable: true` requiere `version_aplicable`.
   - Para datos `volatil`/`[VERIFICAR]`: **abrir la fuente en vivo** y confirmar
     el dato contra la fuente actual (no basta `fecha_consulta`); registrar la URL.
   - `motor` no es `unknown`.
5. Para cada afirmación, fijar `relacion` por arista, derivar `soporte` y registrar
   el `ClaimRecord` (ver § "Atribución por afirmación"). Generar el finding con la
   severidad de la **tabla de severidad (FR-009)** de esa sección.
6. Componer el bloque markdown de findings según el esquema de pasada y añadirlo al
   final de `findings.md` sin sobreescribir bloques previos; escribir/reemplazar el
   bloque del capítulo en `claims.md` (idempotente por capítulo).
7. Reportar al operador: total de afirmaciones evaluadas, soportadas, parciales,
   sin fuente, contradichas, pendientes y críticas.

## Errores comunes

- `research.md` ausente o vacío: aborta y exige ejecutar
  `writeonmars-research`.
- Afirmaciones que no se pueden mapear a una cita por desfase de
  vocabulario: se sugieren al operador para reformulación o ampliación
  del research.
- Citas con `motor: unknown` (regla 2 del contrato): se descartan y se
  reporta.

## Modo paralelo por capítulo

Cuando la guía tiene ≥ 4 capítulos redactados, esta skill puede
despachar el contraste en paralelo (un sub-agente por capítulo). El
modo serial sigue disponible para guías cortas o cuando el operador
quiere revisión sincrónica capítulo a capítulo.

### Mecanismo

1. Identifica todos los `chapters/[###]-*.md` que requieren pasada 4.
2. En una única llamada, dispara un sub-agente de contraste por
   capítulo (`subagent_type: general-purpose`). Cada sub-agente recibe:
   - System prompt: contenido completo de
     `agents/claude/prompts/pasada-4.md`.
   - Mensaje inicial: payload con el capítulo objetivo, el `research.md`
     completo (todos los CitationRecord) y el bloque "Pasada 4" del
     `findings.md` actual (vacío en la primera ejecución).
3. Cada sub-agente devuelve **dos** fragmentos: su bloque "Pasada 4 — Capítulo N"
   (findings, `pass-output-schema.md` v1.1) y su bloque de `claims.md` del capítulo
   (los `ClaimRecord` del capítulo, `claim-record.schema.json` v1.0).
4. El orquestador NO permite que los sub-agentes escriban directamente
   a `findings.md` ni a `claims.md` (evita race conditions). Cada sub-agente devuelve
   los fragmentos y el orquestador consolida.

### Consolidación

Tras la última tanda:

1. Concatena los bloques "Pasada 4 — Capítulo N" en un único bloque
   "Pasada 4 — Precisión" en `findings.md`, ordenado por número de
   capítulo. En paralelo, escribe en `claims.md` el bloque "## Claims — Capítulo N"
   de cada capítulo (reemplazo en bloque por capítulo, sin duplicar ni tocar otros).
2. Detecta conflictos de citación: si dos capítulos citan la misma
   fuente (`citation_id` idéntico) con interpretaciones divergentes
   (campo `interpretacion` o glosa que diverge en cualquier dimensión
   semántica), surface una nota consolidada al final del bloque
   "Pasada 4 — global" en `findings.md`:
   - `severidad: medio` (la decisión final la toma el operador humano
     en la firma de pasada 4).
   - Lista: `citation_id`, capítulo origen 1 con su lectura, capítulo
     origen 2 con su lectura, sugerencia operativa (alinear ambas
     lecturas, declarar excepción justificada, ampliar `research.md`).
3. Reporta al operador: total por capítulo, total global, conflictos
   detectados.

### Cuándo usar paralelo por capítulo

- ≥ 4 capítulos redactados (umbral por defecto del modo paralelo de
  pasada 4).
- `research.md` estable (ningún `CitationRecord` en proceso de
  edición durante el despacho).

### Cuándo evitarlo

- < 4 capítulos: el modo serial es más simple y suficiente.
- `research.md` en mutación (concurrencia entre lectura del sub-agente
  y edición del operador).
- Sub-agentes con cuotas o latencia que hacen que el dispatch paralelo
  no compense.

Documentación operativa en `docs/parallel-execution.md`.

## FR cubierta

- FR-016 (toda afirmación verificable contra al menos una cita; modo
  serial o paralelo).
- FR-017 (datos volátiles marcados [VERIFICAR] y verificados en vivo contra la
  fuente cuando hay acceso a web).
- Feature 003 — FR-005 (un `ClaimRecord` por afirmación verificable), FR-006
  (clasificar `relacion` tras abrir la fuente; sin web → `pendiente`), FR-007
  (idempotencia por capítulo), FR-009 (mapeo veredicto→severidad).

## Versión

v0.4.0 — 2026-06-21 (feature 003): atribución por afirmación. Emite `claims.md`
(`ClaimRecord` v1.0) con la **relación** de cada cita (apoya/matiza/contradice/
menciona) y el veredicto `soporte`; la severidad del finding se deriva de la tabla
FR-009. pass-output-schema → v1.1. Idempotente por capítulo (serial y paralelo).
v0.3.0 — 2026-06-14: la pasada de precisión verifica los datos volátiles abriendo
la fuente real en vivo (web), no solo contra research.md.
v0.2.0-mvp-2026-05-06 — añade dispatch paralelo por capítulo (T063).
v0.1.0-mvp — 2026-05-06.
