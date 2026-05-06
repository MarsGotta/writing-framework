# Data Model: Arquitectura del harness Write.OnMars

**Feature**: 001-framework-architecture | **Date**: 2026-05-06

Este documento detalla cada entidad declarada en la spec (sección Key Entities) con sus campos, validaciones y relaciones. Las entidades se materializan como archivos markdown o JSON dentro del repositorio del proyecto editorial, salvo cuando se indique lo contrario.

---

## 1. Brief editorial

**Archivo**: `specs/[###-feature]/spec.md` (sección "Brief" o equivalente).
**Fuente**: salida de `/speckit-specify` adaptada por la skill `writeonmars-brief`.

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| audiencia | texto libre | sí | ≥ 20 caracteres; sin marcadores `[NEEDS CLARIFICATION]` (FR-006) |
| problema | texto libre | sí | ≥ 30 caracteres |
| resultado_esperado | texto libre | sí | sin `[NEEDS CLARIFICATION]` (FR-006) |
| nivel | enum | sí | `principiante` \| `intermedio` \| `avanzado` |
| tono | texto libre | sí | declara variantes admitidas (experto / directo / natural / sobrio) |
| conceptos_obligatorios | lista de texto | sí | lista cerrada, ≥ 1 elemento |
| ejemplo_recurrente | texto libre | sí | sin `[NEEDS CLARIFICATION]` (FR-006); incluye contexto, objetivo, restricción, riesgo, resultado esperado |
| riesgos | lista de texto | sí | malentendidos a evitar |
| acciones_practicas | lista de texto | sí | qué debe poder hacer el lector al terminar |

**Relaciones**: el brief alimenta el `Contexto del proyecto` (entidad 3) y se referencia en cada `Capítulo` (entidad 7) producido bajo la spec.

**Cobertura**: FR-005, FR-006, Constitución § III.

---

## 2. Investigación

**Archivo**: `specs/[###-feature]/research.md`.
**Fuente**: skill `writeonmars-research`.

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| temas_explorados | lista de texto | sí | ≥ 1 por concepto obligatorio del brief (SC-009) |
| fuentes | lista de `CitationRecord` | sí | conformes al contrato `citation-contract.md` v1 |
| datos_volatiles | lista de texto con marca [VERIFICAR] | si aplica | versiones, precios, comandos |
| fecha_consulta_global | ISO-8601 | sí | YYYY-MM-DD |
| motor_principal | texto | sí | nombre del MCP / fuente local utilizada |

**Relaciones**: cada `Hallazgo de revisión` (entidad 11) en pasada 4 referencia uno o más `CitationRecord` del campo `fuentes`.

**Cobertura**: FR-008, FR-009, FR-009a, SC-009.

---

## 3. Contexto del proyecto

**Archivo**: `CLAUDE.md` o `AGENTS.md` en la raíz del proyecto editorial.
**Fuente**: skill `writeonmars-brief` tras aprobación del brief.

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| audiencia | texto | sí | copiado del brief |
| ejemplo_recurrente | texto | sí | copiado del brief |
| glosario_inicial | lista | sí | términos del brief con definición provisional |
| tono | texto | sí | copiado del brief |
| reglas_microestilisticas | lista | sí | derivadas de la constitución § I y § IV |
| referencia_plan | path | sí | apunta al `plan.md` activo entre marcadores `<!-- SPECKIT START -->` / `<!-- SPECKIT END -->` |
| referencia_constitucion | path | sí | `.specify/memory/constitution.md` |

**Relaciones**: se carga automáticamente en cada sesión del agente del proyecto editorial.

**Cobertura**: FR-002, FR-007.

---

## 4. Temario

**Archivo**: sección "Temario" dentro de `specs/[###-feature]/plan.md`.
**Fuente**: skill `writeonmars-temario` (envuelve `/technical-guide-design`).

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| capitulos[] | lista | sí | ≥ 1 |
| capitulos[].numero | entero | sí | secuencial empezando en 1 |
| capitulos[].titulo | texto | sí | claridad antes que ingenio (constitución § Estándares: títulos) |
| capitulos[].promesa | texto | sí | una frase declarando qué resuelve el capítulo |
| capitulos[].estructura_aplicada | enum | sí | `didactica_v1` (la del Principio II) |

**Cobertura**: FR-010, FR-011.

---

## 5. Descripciones encadenadas

**Archivo**: sección "Descripciones encadenadas" dentro de `specs/[###-feature]/plan.md`.
**Fuente**: skill `writeonmars-descripciones` (envuelve `/technical-guide-design`).

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| capitulo_numero | entero | sí | corresponde a un capítulo del temario |
| promesa_especifica | texto | sí | refina la promesa del temario para este capítulo |
| conexion_anterior | texto o `null` | sí | `null` solo permitido para el capítulo 1 |
| conexion_siguiente | texto o `null` | sí | `null` solo permitido para el último capítulo |
| ejemplo_recurrente_aplicado | texto | sí | cómo se usa en este capítulo (≥ 80% capítulos por SC-005) |
| conceptos_introducidos | lista | sí | términos nuevos que entrarán al glosario consolidado (FR-015) |

**Cobertura**: FR-010, SC-005.

---

## 6. Glosario consolidado

**Archivo**: `specs/[###-feature]/glossary.md` (proyecto-feature) y/o `glossary.md` (proyecto-wide en raíz).
**Fuente**: skill `writeonmars-glossary`.

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| termino | texto | sí | único dentro del proyecto (FR-015 detección de colisiones) |
| definicion | texto | sí | sin tautologías; concreta |
| capitulo_origen | entero | sí | número de capítulo donde se introduce |
| sinonimos_admitidos | lista | no | con justificación si rompe univocidad (constitución § IV) |
| anglicismo_admitido | bool | no | `true` solo si se justifica en este registro |
| justificacion | texto | si `anglicismo_admitido = true` | enlace a constitución § IV |

**Validación de cobertura**: SC-004 exige 100% de términos técnicos del cuerpo registrados.

**Cobertura**: FR-015, FR-021, SC-004, Constitución § IV.

---

## 7. Capítulo

**Archivo**: `chapters/[###]-titulo.md`.
**Fuente**: sub-agente despachado por skill `writeonmars-redaccion`.

Estructura obligatoria (constitución § II + Estándares editoriales — patrón de capítulo):

1. Problema real
2. Idea clave
3. Por qué importa
4. Cómo funciona
5. Ejemplo (usa el `ejemplo_recurrente`)
6. Error frecuente
7. Qué hacer en la práctica
8. Checklist rápido (≥ 1 caja: "Quédate con esto" | "Qué hacer mañana" | "Síntoma → causa probable")
9. Puente al siguiente capítulo

| Campo (front-matter YAML) | Tipo | Obligatorio | Validación |
|--------------------------|------|-------------|-----------|
| numero | entero | sí | corresponde al temario |
| titulo | texto | sí | sin emoji; claridad antes que ingenio |
| promesa | texto | sí | copiada de descripciones encadenadas |
| terminos_introducidos | lista | sí | alimenta `Glosario consolidado` |
| ejemplo_aplicado_referencias | lista | sí | secciones donde aparece el ejemplo recurrente |
| estado_pasadas | objeto | sí | mapping pasada_N → `pending|passed|signed|blocked` |

**Cobertura**: FR-012, FR-014, FR-015, SC-003, SC-005, Constitución § II.

---

## 8. Index

**Archivo**: `index.md` en la raíz del proyecto editorial.
**Fuente**: skill `writeonmars-pasada-5` (formato) tras consolidar capítulos.

Contenido obligatorio:

- Promesa global de la guía
- Para quién es / para quién no es
- Qué vas a aprender
- Ruta rápida de lectura (orden de capítulos con su promesa)
- Enlaces a `glossary.md`, `common-errors.md`, `templates/`

**Cobertura**: FR-029, Constitución § Estándares editoriales (estructura de guía completa).

---

## 9. Errores comunes

**Archivo**: `common-errors.md` en la raíz del proyecto editorial.
**Fuente**: agregación de la sección "Error frecuente" de cada capítulo + complementos del operador.

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| error | texto | sí | descripción del malentendido |
| capitulo_origen | entero | no | si proviene de un capítulo concreto |
| sintoma | texto | sí | cómo lo detecta el lector |
| causa_probable | texto | sí | explicación operativa |
| que_revisar | texto | sí | acciones del lector |

**Cobertura**: FR-029, Constitución § Estándares editoriales (caja "Síntoma → causa probable").

---

## 10. Plantillas reutilizables

**Archivo**: `templates/` directory con archivos `.md` o snippets.
**Fuente**: extraídas durante la redacción cuando un capítulo expone una plantilla copiable.

Cada plantilla MUST incluir: nombre, propósito, campos a rellenar, ejemplo lleno.

**Cobertura**: FR-029, Constitución § Estándares editoriales (plantillas reutilizables).

---

## 11. Hallazgos de revisión

**Archivo**: `specs/[###-feature]/findings.md`.
**Fuente**: cada una de las cinco pasadas escribe en este archivo (formato unificado en `contracts/pass-output-schema.md`).

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| pasada | enum | sí | `1_estructura` \| `2_utilidad` \| `3_naturalidad` \| `4_precision` \| `5_formato` |
| capitulo | entero o `global` | sí | indica el alcance del hallazgo |
| frase_original | texto | sí | cita literal |
| problema | texto | sí | qué falla |
| severidad | enum | sí | `critico` \| `medio` \| `bajo` |
| reescritura_sugerida | texto | sí | versión propuesta (excepto cuando severidad = `bajo` y se decide ignorar) |
| estado | enum | sí | `abierto` \| `resuelto` \| `desviacion_justificada` |
| referencias_cita | lista de `citation_id` | si pasada = `4_precision` | enlaces al `research.md` |

**Validación de cierre**: ningún hallazgo `critico` con estado `abierto` permite cerrar el proyecto (FR-020).

**Cobertura**: FR-018, FR-019, FR-020, FR-027.

---

## 12. Checklist de pasada

**Archivo**: `checklists/[###-feature]/pasada-N.md`.
**Fuente**: skill `writeonmars-pasada-N` (con N de 1 a 5).

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| pasada | enum | sí | igual al de Hallazgos |
| items[] | lista de booleanos con etiqueta | sí | derivada de la constitución § V (preguntas por pasada) |
| firma_tipo | enum | sí | `autonoma` \| `humana` |
| firma_actor | texto | sí | id del agente o del operador humano |
| firma_fecha | ISO-8601 | sí | YYYY-MM-DD |
| referencia_findings | path | sí | enlace a `findings.md` |

**Validación**: si `signing_matrix[pasada] = human` en el manifiesto y `firma_tipo = autonoma`, el cierre del proyecto se bloquea (FR-020a).

**Cobertura**: FR-018, FR-020a, FR-027.

---

## 13. Manifiesto del proyecto

**Archivo**: `.writeonmars-manifest.json` en la raíz del proyecto editorial.
**Fuente**: skill `writeonmars-install` (creación) + actualizaciones manuales o vía skills específicas.

Esquema completo en `contracts/manifest-schema.json`. Campos clave:

- `framework_version` (semver)
- `constitution_version` (semver)
- `agent_target` (`claude-code` | `codex` | `cursor` | ...)
- `language_primary` (`es` por defecto)
- `skills[]` con `name`, `version`, `source` (`bundled` | `external`)
- `research_mode` (`byom` | `bundled`)
- `signing_matrix` (mapping pasada → `autonomous` | `human`)
- `human_operators[]` con `id`, `email`, `role`
- `citation_contract_version` (semver)

**Cobertura**: FR-004, FR-020a, FR-022, FR-027.

---

## Resumen de relaciones

```text
Brief
  ├─→ Contexto del proyecto (deriva)
  ├─→ Temario (alimenta promesa)
  └─→ Descripciones encadenadas (provee ejemplo recurrente)

Investigación
  └─→ Hallazgos de revisión (referencias en pasada 4)

Temario
  └─→ Descripciones encadenadas (1:1 por capítulo)

Descripciones encadenadas
  ├─→ Capítulo (input al sub-agente de redacción)
  └─→ Glosario consolidado (conceptos introducidos)

Capítulo
  ├─→ Glosario consolidado (términos introducidos)
  ├─→ Errores comunes (sección "Error frecuente")
  ├─→ Plantillas reutilizables (cuando aplica)
  └─→ Hallazgos de revisión (entrada de las cinco pasadas)

Hallazgos de revisión ⇄ Checklist de pasada (1:1 por pasada)

Manifiesto del proyecto
  ├─→ governanza de cierre (FR-020a)
  └─→ trazabilidad de versiones de skills (FR-027)
```
