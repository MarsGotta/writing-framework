# Bookwright en profundidad — diseños de adopción para Write.OnMars

**Fecha**: 2026-07-08 · Continuación de `comparativa-bookwright-sloop.md` con
el código real leído a fondo (protocolo PENDING, fichas de biblia, contrato de
research, tabla de reglas del status, skill de continuidad, receta de
dogfooding). Cada sección: qué hace Bookwright, el diseño concreto de adopción
en nuestro repo, y cuándo.

## 1. Protocolo `[PENDING]` — el hueco declarado como contrato de tres sistemas

**Qué hace** (`references/pending-protocol.md`): un único token
`[PENDING: ¿pregunta concreta?]` con una regla de decisión nítida — *"si el
hueco solo te falta, márcalo y sigue; si rellenarlo te obliga a decidir el
rumbo de la obra, detente y pregunta"* (canon estructural = load-bearing). Tres
sistemas lo entienden: las skills lo estampan, los validadores lo tratan como
"no decidido" (se apagan con no-evaluado en vez de dar falsa alarma), y un
comando (`clarify`) enumera todos los abiertos. Detalle operativo incluido:
en YAML de tipo cadena va entre comillas o los corchetes se leen como lista y
la ficha se descarta en silencio.

**Nuestro estado**: ya tenemos `[NEEDS CLARIFICATION]` en briefs (FR-006 de la
001 bloquea el plan con marcadores en campos críticos), pero es un token de
*una* fase; no existe en fichas de roots/, ni en el temario, ni la brújula lo
cuenta.

**Adopción propuesta** (spec futura, junto con § 2):
- Mantener `[NEEDS CLARIFICATION: …]` como token único (no inventar un segundo
  sentinel: la lección es precisamente un solo acuerdo).
- Extender su semántica a fichas de `roots/` y `plan.md`: los comandos lo
  estampan con la regla load-bearing; `status.py` gana un campo
  `pending_questions` (lista {archivo, pregunta}) derivado por grep
  determinista.
- La pasada 4 (ambos modos) trata una ficha con marcador como "no decidido":
  su verificación contra esa ficha se declara no-evaluada, nunca hallazgo
  inventado.
- Regla de comillas YAML documentada en las plantillas de ficha.

## 2. Biblia de historia en `roots/` — las fichas del modo estudio narrativo

**Qué hace** (`templates/bible/character.md.tmpl` y hermanas): fichas con
frontmatter **cerrado y tipado duro** (clave extra = warning del indexador;
`born`/`died` solo enteros o se omiten — nunca texto) + secciones de prosa
guiadas por comentarios. Las dos secciones geniales: **"Diálogo de muestra"**
(2-3 réplicas que capturan la voz, para mantenerla constante) y **"Patrones de
lenguaje corporal"** (qué gestos delatan al personaje bajo presión). Además:
`timeline.md`, `relationships.md` y `pov-structure.md` con un "Calendario de
POV" por capítulo — el ancla del juicio de head-hopping.

**Adopción propuesta** (candidata a **spec 006 — biblia narrativa en roots/**):
- Plantillas OKF-compatibles en `writeonmars/templates/roots/`:
  `personaje.md` (frontmatter: `type: personaje`, `alias`, `nacido`/`muerto`
  enteros, `rasgos`, `roles_narrativos` + secciones: biográficos, psicológicos,
  físicos, rol, **diálogo de muestra**, **lenguaje corporal**), `lugar.md`,
  `objeto.md`, `timeline.md`, `relaciones.md`, `pov.md` (calendario de POV).
- Un chequeo determinista mínimo en `status.py` o script propio: frontmatter
  parseable, claves dentro del vocabulario, tipos duros. Nada de grafo RDF:
  archivos planos computables (la trampa a evitar quedó documentada).
- Estas fichas son el sustrato de la pasada de consistencia del modo estudio
  (§ 3): sin fichas, la pasada declara "no evaluable" (ya en la 005).

## 3. Los seis ejes de continuidad — el prompt de la pasada 4 en estudio narrativo

**Qué hace** (`bookwright-continuity.md`): la skill de revisión de continuidad
juzga seis ejes, cada uno con su **anclaje declarado y citable**: cumplimiento
de fichas, coherencia de arcos, coherencia temporal, personajes usados sin
ficha (contra el *roster* = campo `name:` de las fichas), head-hopping (contra
voz declarada + calendario de POV + roster) y deslizamiento a 1ª persona
(contra la voz declarada, incluida la morfología pro-drop del español —
`Caminé`, `Me senté` — que ningún regex ve). Tres reglas de oro transversales:
1. **Ante ancla ausente o `[PENDING]`, reporta el hueco y NO adivines** (un
   ancla ausente es hueco de entrada del juicio, nunca un hallazgo inventado).
2. **Es juicio, no error de gate**: de estos ejes no nace ningún `error`
   bloqueante automático.
3. **Cita siempre el anclaje**: cada desviación lleva la cita del manuscrito +
   el hecho de la ficha que contradice + sugerencia.

**Adopción propuesta**: cuando exista la biblia de § 2, el comando de pasada 4
en modo estudio narrativo (`speckit.review-precision` con adenda de género, o
comando propio del registro narrativo) adopta los seis ejes adaptados:
- roster desde `roots/` (`type: personaje`), POV desde `roots/pov.md`, voz
  desde las adendas de la constitución del proyecto.
- Salida en nuestro formato: bloque findings.md v1.2 con huellas — mejor que
  Bookwright (sus reportes son prosa efímera; los nuestros entran al ciclo de
  disposición de la 005).
- Severidad mapeada a nuestra política: desviación de continuidad = `medio`
  (fuerza disposición humana), hueco de anclaje = nota "no evaluable", nunca
  `critico` automático (el crítico queda para contradicción factual con ancla
  firme).

## 4. Hallazgo vs ancla — refinar el contrato de citación (produccion)

**Qué hace** (`references/research-format.md`): separación estricta entre
**hallazgo** (información con fuentes, `id` + `claim` + `sources`) y **ancla**
(restricción vinculante sobre la obra: `promotes` un hallazgo + `constrains`
una entidad o la timeline + rango temporal). Promoción solo si la mejor fuente
alcanza `min_reliability_for_anchor` del manifiesto. Facetas de fuente
obligatorias y fatales si faltan: cita literal **en lengua original** +
**traducción obligatoria** si el idioma difiere del libro + fiabilidad
justificada + fecha de acceso. Y una regla editorial de oro: *"cuando las
fuentes discrepen, escribe dos hallazgos, cada uno con su fuente; nunca los
fundas en uno"*.

**Adopción propuesta** (iteración futura del citation-contract, feature
aparte):
- `CitationRecord` gana facetas: `cita_original` (lengua original),
  `traduccion` (obligatoria si idioma ≠ es — **muy relevante**: nuestras guías
  son en español y las fuentes técnicas casi siempre en inglés),
  `fiabilidad` (alta/media/baja) + `justificacion_fiabilidad`.
- `ClaimRecord` de `dato_duro`: exigir que al menos una evidencia `apoya`
  provenga de fuente con fiabilidad ≥ umbral del manifiesto
  (`quality_gates.min_fiabilidad_dato_duro`) — la versión nuestra de
  "promover a ancla".
- Regla de discrepancia al prompt de la pasada 4: fuentes en conflicto = dos
  registros, nunca uno fundido.

## 5. `next_actions` + test de oráculo — cerrar el bucle de la brújula

**Qué hace** (`status/rules.py`): una tabla de reglas **pura** (sin I/O, sin
reloj) donde el orden es la prioridad; cada regla emite
`{skill, prompt listo-para-pegar, reason}` parametrizado solo por hechos del
estado → mismo corpus, bytes idénticos. Testeado contra un **oráculo
co-localizado en el fixture** (`expected-status.md`: la salida entera comparada
byte a byte). Y el cierre del bucle: cada skill materializada **arranca
ejecutando `status --json`** para auto-orientarse.

**Adopción propuesta**:
- **Ya (barato, gran retorno)**: test de oráculo para `status.py` — un fixture
  de proyecto con su `expected-status.json` al lado; el test compara la salida
  `--json` completa (no aserciones campo a campo). Congela el contrato de la
  brújula contra regresiones accidentales. Encaja como refuerzo del T007 de la
  005 o test suelto en `tests/unit/`.
- **Futuro**: `next_detail` evoluciona a `next_actions`
  `[{step, role, prompt, reason}]` — el prompt de despacho lo sintetiza la
  brújula (tabla pura, determinista) y Vivarium deja de componer el `detail` a
  mano. Un solo origen para "qué se le dice al agente".

## 6. Receta de dogfooding con defectos plantados

**Qué hace** (`docs/dogfooding.md`): práctica repetible — un proyecto real a
escala (no fixtures finos), **matriz de cobertura con un defecto deliberado
por validador** para confirmar que cada uno dispara, log de fricción como
salida principal, y el proyecto de prueba es **desechable** (lo que se
commitea es el repro mínimo de cada hallazgo, nunca el libro).

**Adopción propuesta** (documento de práctica, sin código): añadir a
`tests/editorial-pilot/` una receta equivalente para validaciones como la
T022: matriz de defectos por gate — un `critico` abierto (g1), una firma
autónoma donde el manifiesto exige humana (g2), un capítulo fuera de temario
(g3), un claim `sin_fuente` bajo umbral (g4), y con la 005: un `estado` editado
sin disposición, un capítulo editado tras pasada (huella), un commit de agente
en `chapters/` (autoría). Cada validación e2e futura confirma que **todos**
los guardarraíles disparan, no solo que el camino feliz cierra.

## Resumen de destino

| Idea | Dónde | Cuándo |
|------|-------|--------|
| Test de oráculo de status.py | tests/unit + fixture | con la 005 (refuerzo de T007) |
| Ejes de continuidad + reglas de oro | comando pasada 4 estudio narrativo | spec 006 |
| Fichas de biblia en roots/ | writeonmars/templates/roots/ | spec 006 |
| PENDING de tres sistemas | comandos + status.py | spec 006 (o junto a fichas) |
| Facetas de fuente + umbral dato_duro | citation-contract | feature aparte (evolución de 003) |
| Receta de defectos plantados | tests/editorial-pilot/ | documento, oportunista |
