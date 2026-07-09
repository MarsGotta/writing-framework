---
name: writeonmars-brief
description: Captura el brief editorial obligatorio de nueve campos (Constitución § III) durante /speckit-specify para proyectos editoriales. Trigger cuando la persona diga "brief editorial", "captura el brief", "arma el brief", "spec editorial", "/speckit-specify para una guía", o cuando `project_type=editorial` y la spec todavía no tenga las nueve secciones.
allowed-tools: Bash, Read, Write, Edit
---

# writeonmars-brief

Skill que materializa el Principio III de la constitución: ninguna pieza
arranca redacción sin un brief explícito. Se dispara durante
`/speckit-specify` cuando el manifiesto del proyecto declara
`project_type: editorial` y produce/actualiza la sección Brief en
`specs/[###-feature]/spec.md`. Bloquea el avance si los campos críticos no
están resueltos (FR-006).

## Cuándo dispararse

- "brief editorial"
- "captura el brief"
- "arma el brief"
- "spec editorial"
- "/speckit-specify para una guía"
- Inicio de un proyecto cuyo `.writeonmars-manifest.json` declara
  `project_type: editorial` y `specs/[###-feature]/spec.md` carece de las
  nueve secciones obligatorias.

NO actives la skill en proyectos de software (`project_type: software`); en
ese caso `/speckit-specify` opera con la plantilla clásica.

## Qué hace

1. Verifica que existe `.writeonmars-manifest.json` y que
   `project_type` esté presente. Si falta, propone correr
   `writeonmars-install --reconfigure`.
2. Lanza un cuestionario en español que cubre los nueve campos de
   data-model.md §1: audiencia, problema, resultado_esperado, nivel, tono,
   conceptos_obligatorios, ejemplo_recurrente, riesgos, acciones_practicas.
3. Valida el contenido por campo:
   - audiencia: ≥ 20 caracteres, sin `[NEEDS CLARIFICATION]`.
   - problema: ≥ 30 caracteres.
   - resultado_esperado: sin `[NEEDS CLARIFICATION]`.
   - nivel: enum `principiante|intermedio|avanzado`.
   - tono: declara la combinación admitida (experto/directo/natural/sobrio).
   - conceptos_obligatorios: lista cerrada con ≥ 1 elemento.
   - ejemplo_recurrente: contexto, objetivo, restricción, riesgo,
     resultado esperado.
   - riesgos: lista no vacía.
   - acciones_practicas: lista no vacía.
4. Bloquea avance (exit no-cero, mensaje claro al operador) si alguno de
   los campos críticos contiene `[NEEDS CLARIFICATION]` o no cumple su
   validación. Campos críticos para FR-006: audiencia, ejemplo_recurrente,
   resultado_esperado.
5. Renderiza la sección Brief en `specs/[###-feature]/spec.md` siguiendo
   la plantilla editorial (`.specify/templates/spec-template.md`).
6. Actualiza el archivo de contexto del agente (`CLAUDE.md` o `AGENTS.md`)
   entre los marcadores `<!-- WRITEONMARS START -->` y
   `<!-- WRITEONMARS END -->` con: audiencia, ejemplo_recurrente,
   tono, glosario inicial derivado de conceptos_obligatorios y referencia
   al plan activo.

## Inputs

- `.writeonmars-manifest.json` — para confirmar `project_type=editorial` y
  `agent_target`.
- `.specify/templates/spec-template.md` — plantilla editorial adaptada por
  T030.
- `.specify/memory/constitution.md` — Principio III y § IV (microestilo).
- Respuestas del cuestionario.

## Outputs

- `specs/[###-feature]/spec.md` con sección Brief de nueve campos.
- `CLAUDE.md` o `AGENTS.md` con bloque `<!-- WRITEONMARS ... -->`
  actualizado.

## Procedimiento

1. Detectar la rama feature activa (`git branch --show-current`) y derivar
   `[###-feature]`.
2. Si `specs/[###-feature]/spec.md` no existe, crearlo a partir de la
   plantilla editorial.
3. Lanzar el cuestionario campo por campo. Mostrar la regla violada
   inmediatamente cuando una respuesta no valide; permitir reintento sin
   reiniciar.
4. Componer la sección Brief en formato markdown con encabezados claros
   por campo y listas para los campos plurales.
5. Renderizar el bloque del archivo de contexto. Si el bloque ya existe,
   actualizarlo; si no, añadirlo al final del archivo.
6. Imprimir un resumen al operador: ruta del spec, ruta del CLAUDE.md y
   advertencias pendientes (campos `[NEEDS CLARIFICATION]` no críticos).

## Errores comunes

- Cuestionario abortado a media respuesta: la skill no escribe parcialmente
  el spec; conserva un borrador en `specs/[###-feature]/.brief-draft.md` y
  reporta para retomarlo.
- Conflicto con un brief previo: si `spec.md` ya tiene una sección Brief,
  la skill genera un diff y pide confirmación antes de sobrescribir.
- `project_type` no declarado en el manifiesto: la skill se detiene y
  sugiere `writeonmars-install --reconfigure`.
- Bloque `<!-- WRITEONMARS START -->` ausente en `CLAUDE.md`: la skill lo
  añade respetando contenido previo del archivo.

## FR cubierta

- FR-005 (brief de nueve campos materializado).
- FR-006 (bloqueo cuando audiencia, ejemplo_recurrente o
  resultado_esperado tienen `[NEEDS CLARIFICATION]`).
- FR-007 (actualización de `CLAUDE.md` o `AGENTS.md`).

## Versión

v0.1.0-mvp — 2026-05-06
