# [CHECKLIST TYPE] Checklist: [FEATURE NAME]

**Purpose**: descripción breve de lo que cubre esta checklist.
**Created**: [DATE]
**Feature**: [Link a spec.md o documentación relevante]

**Note**: este template lo genera el comando `/speckit-checklist`. Cuando el
manifiesto declara `project_type: editorial`, las cinco secciones marcadas como
**Pasada N** materializan el Principio V de la constitución y deben dividirse
en archivos separados (`pasada-1.md` … `pasada-5.md`) bajo
`checklists/[###-feature]/`.

<!--
  ============================================================================
  IMPORTANT: la sección "Categorías genéricas" es para el modo software.
  Las secciones "Pasada 1" a "Pasada 5" son para el modo editorial.

  Cuando el operador genera un único archivo `pasada-N.md`, debe extraer SOLO
  la sección correspondiente a su pasada y rellenar el bloque de firma al
  final. El procedimiento manual es:

    1. Copia este template completo a `checklists/[###-feature]/template.md`.
    2. Por cada N en {1..5}, copia la sección "## Pasada N — ..." junto con
       el bloque de firma a `checklists/[###-feature]/pasada-N.md`.
    3. Rellena los items conforme avanza la pasada.

  Alternativamente, una skill `writeonmars-pasada-N` puede generar el archivo
  `pasada-N.md` directamente desde el marcador
  `<!-- PASADA-N START -->` / `<!-- PASADA-N END -->`.

  El bloque de firma corresponde a `data-model.md § 12` (Checklist de pasada).
  ============================================================================
-->

## Categorías genéricas (modo software)

<!--
  En modo software, sustituye estas categorías por las reales del proyecto.
-->

### [Categoría 1]

- [ ] CHK001 Primer item con acción clara
- [ ] CHK002 Segundo item
- [ ] CHK003 Tercer item

### [Categoría 2]

- [ ] CHK004 Item de otra categoría
- [ ] CHK005 Item con criterio específico
- [ ] CHK006 Último item de esta categoría

---

# Modo editorial — Cinco pasadas (Principio V)

<!-- PASADA-1 START -->

## Pasada 1 — Estructura

**Lente**: promesa clara, audiencia explícita, función de cada capítulo,
progresión lógica, acción final. (Constitución § V.1, FR-018.)

**Skill principal**: `/technical-guide-design`.

**Default de firma (matriz v1)**: autonomous.

### Items

- [ ] CHK101 La promesa global de la guía es declarable en una frase y aparece
  en `index.md`.
- [ ] CHK102 La audiencia del brief se reconoce sin esfuerzo en cada capítulo
  (no se contradice ni se diluye).
- [ ] CHK103 Cada capítulo tiene una función única dentro del temario; no hay
  capítulos redundantes.
- [ ] CHK104 La progresión entre capítulos es lógica: cada uno se apoya en lo
  anterior y prepara lo siguiente (descripciones encadenadas coherentes).
- [ ] CHK105 La guía completa termina con una acción concreta (no con una
  reflexión abstracta o una invitación a "seguir explorando").
- [ ] CHK106 No existen secciones huérfanas (que no cumplan la plantilla
  problema → idea clave → consecuencia práctica).
- [ ] CHK107 Hallazgos críticos abiertos en `findings.md` para esta pasada: 0.

### Firma

- **firma_tipo**: [autonomous | human]
- **firma_actor**: [id del agente o `human:{id}`]
- **firma_fecha**: [YYYY-MM-DD]
- **referencia_findings**: `specs/[###-feature]/findings.md` § "Pasada 1 — Estructura"

<!-- PASADA-1 END -->

---

<!-- PASADA-2 START -->

## Pasada 2 — Utilidad

**Lente**: ejemplos por concepto, acción práctica por capítulo, checklists,
errores comunes, síntomas reales, criterios de éxito. (Constitución § V.2,
FR-018.)

**Skill principal**: `/technical-guide-design`.

**Default de firma (matriz v1)**: autonomous.

### Items

- [ ] CHK201 Cada concepto técnico introducido tiene al menos un ejemplo
  concreto dentro del mismo capítulo.
- [ ] CHK202 La salida operativa ("Qué hacer en la práctica" / checklist) aparece
  según lo declaren las adendas del proyecto: por capítulo, o centralizada en el
  cierre y los anexos (p. ej. tecnología la centraliza). No exigir por capítulo si
  el sector lo relaja.
- [ ] CHK205 Cada capítulo cierra con su sección "## Fuentes" (nombre, enlace y
  fecha de las fuentes citadas en ese capítulo). Obligatoria desde v1.3.0.
- [ ] CHK203 La sección "Error frecuente" de cada capítulo describe síntomas
  observables (no abstracciones).
- [ ] CHK204 Cada capítulo declara criterios de éxito verificables (qué debe
  poder hacer la persona lectora al terminar).
- [ ] CHK205 Las plantillas reutilizables que el capítulo expone están en
  `templates/` con nombre, propósito, campos a rellenar y ejemplo lleno.
- [ ] CHK206 Los checklists del capítulo no son genéricos: están redactados
  para el dominio concreto del proyecto.
- [ ] CHK207 Hallazgos críticos abiertos en `findings.md` para esta pasada: 0.

### Firma

- **firma_tipo**: [autonomous | human]
- **firma_actor**: [id del agente o `human:{id}`]
- **firma_fecha**: [YYYY-MM-DD]
- **referencia_findings**: `specs/[###-feature]/findings.md` § "Pasada 2 — Utilidad"

<!-- PASADA-2 END -->

---

<!-- PASADA-3 START -->

## Pasada 3 — Naturalidad

**Lente**: ausencia de notas internas convertidas en prosa, transiciones
explicadas, referentes claros, sin abuso de eslóganes ni metáforas mezcladas.
El texto debe poder leerse en voz alta sin sonar artificial. (Constitución
§ V.3 y § I, FR-018.)

**Skill principal**: `/marcela-prose`.

**Default de firma (matriz v1)**: human (FR-020a).

### Items

- [ ] CHK301 No quedan notas internas, comentarios de agente o frases de
  proceso en el cuerpo de los capítulos.
- [ ] CHK302 Cada transición explica por qué cambia el tema (no
  "vamos a verlo", "pasemos al siguiente punto", "quedan tres categorías").
- [ ] CHK303 Todos los pronombres ("eso", "esto", "lo", "esa decisión")
  tienen referente explícito en la frase anterior.
- [ ] CHK304 La fórmula "No es X: es Y" no aparece más de una vez por
  capítulo, y solo cuando cierra una idea importante.
- [ ] CHK305 No hay frases comprimidas que obliguen a la persona lectora a
  reconstruir la intención.
- [ ] CHK306 No hay entusiasmo artificial, lenguaje promocional ni metáforas
  mezcladas.
- [ ] CHK307 El texto se ha leído en voz alta (o se ha simulado la lectura)
  sin sonar artificial.
- [ ] CHK308 Hallazgos críticos abiertos en `findings.md` para esta pasada: 0.

### Firma

- **firma_tipo**: [autonomous | human] — default v1: `human`.
- **firma_actor**: [id del agente o `human:{id}`]
- **firma_fecha**: [YYYY-MM-DD]
- **referencia_findings**: `specs/[###-feature]/findings.md` § "Pasada 3 — Naturalidad"

<!-- PASADA-3 END -->

---

<!-- PASADA-4 START -->

## Pasada 4 — Precisión

**Lente**: sin datos inventados; versiones, comandos y precios verificados;
afirmaciones absolutas matizadas; principios estables distinguidos de datos
temporales. (Constitución § V.4, FR-016, FR-018.)

**Skill principal**: `writeonmars-contraste`.

**Default de firma (matriz v1)**: human (FR-020a).

### Items

- [ ] CHK401 Cada afirmación verificable está respaldada por al menos un
  `CitationRecord` del `research.md` (referencias en `referencias_cita` del
  finding).
- [ ] CHK402 Versiones, comandos, precios y fechas tienen marca de última
  comprobación (`[VERIFICAR YYYY-MM-DD]`) o están firmadas por la persona
  operadora.
- [ ] CHK403 Las afirmaciones absolutas ("siempre", "nunca", "todos") están
  matizadas o respaldadas por una fuente que las sostenga.
- [ ] CHK404 Los principios estables (cómo funciona algo) están separados de
  los datos temporales (precios, versiones, URLs).
- [ ] CHK405 Cada hallazgo de pasada 4 marca su afirmación como
  `verificado | pendiente | desviacion_justificada`.
- [ ] CHK406 No hay afirmaciones inventadas (sin fuente y sin marca de
  pendiente).
- [ ] CHK407 Hallazgos críticos abiertos en `findings.md` para esta pasada: 0.

### Firma

- **firma_tipo**: [autonomous | human] — default v1: `human`.
- **firma_actor**: [id del agente o `human:{id}`]
- **firma_fecha**: [YYYY-MM-DD]
- **referencia_findings**: `specs/[###-feature]/findings.md` § "Pasada 4 — Precisión"

<!-- PASADA-4 END -->

---

<!-- PASADA-5 START -->

## Pasada 5 — Formato

**Lente**: cajas visuales útiles, ejemplos diferenciados del cuerpo, títulos
claros, índice navegable, glosario completo, plantillas extraídas, sin bloques
de texto excesivos. (Constitución § V.5, FR-018, FR-029.)

**Skill principal**: `writeonmars-pasada-5`.

**Default de firma (matriz v1)**: autonomous.

### Items

- [ ] CHK501 Cajas visuales ("Quédate con esto", "Qué hacer mañana", "Síntoma →
  causa probable") presentes **solo si las adendas del proyecto las declaran
  obligatorias** para el sector. No son obligatorias por defecto (constitución §
  Estándares editoriales, v1.3.0). Tecnología las omite.
- [ ] CHK502 Los ejemplos están visualmente diferenciados del cuerpo
  expositivo (bloque, recuadro, tipografía o etiqueta clara).
- [ ] CHK503 Los títulos son claros antes que ingeniosos; sin emojis; sin
  juegos de palabras opacos.
- [ ] CHK504 `index.md` cubre: promesa global, "Para quién es / no es",
  "Qué vas a aprender", ruta rápida de lectura y enlaces a `glossary.md`,
  `common-errors.md`, `templates/`.
- [ ] CHK505 `glossary.md` cubre el 100 % de los términos técnicos del cuerpo
  (SC-004); cada entrada tiene definición concreta y capítulo de origen.
- [ ] CHK506 `common-errors.md` agrega la sección "Error frecuente" de cada
  capítulo bajo el esquema de data-model § 9.
- [ ] CHK507 `templates/` contiene cada plantilla expuesta por la guía con
  nombre, propósito, campos y ejemplo lleno.
- [ ] CHK508 No quedan bloques de texto excesivos sin caja, lista o ejemplo
  intercalados.
- [ ] CHK509 Hallazgos críticos abiertos en `findings.md` para esta pasada: 0.

### Firma

- **firma_tipo**: [autonomous | human]
- **firma_actor**: [id del agente o `human:{id}`]
- **firma_fecha**: [YYYY-MM-DD]
- **referencia_findings**: `specs/[###-feature]/findings.md` § "Pasada 5 — Formato"

<!-- PASADA-5 END -->

---

## Notes

- Marca items como completados con `[x]`.
- Añade comentarios o hallazgos en línea cuando un item necesite contexto.
- Los items están numerados secuencialmente para referencia rápida.
- Modo editorial: cada `pasada-N.md` independiente vive en
  `checklists/[###-feature]/pasada-N.md` y se firma en su bloque de firma; el
  cierre del proyecto consume estas firmas vía `writeonmars-close-project`.
