---
name: writeonmars-pasada-5
description: Pasada 5 (formato) sobre la guía completa. Skill propia que agrega errores comunes, construye index.md, valida glosario y plantillas, comprueba cajas visuales y formateo de capítulos. Trigger cuando la persona diga "pasada 5", "revisa el formato", "construye el índice", "consolida errores comunes".
allowed-tools: Bash, Read, Write, Edit
---

# writeonmars-pasada-5

Skill que materializa la pasada 5 (formato) del Principio V.5 y los
Estándares editoriales de la constitución. A diferencia de las pasadas
1–4, no envuelve una skill bundled: es propia y opera a nivel global de
la guía. Construye y valida los artefactos finales del proyecto editorial.

## Cuándo dispararse

- "pasada 5"
- "revisa el formato"
- "construye el índice"
- "consolida errores comunes"
- Última pasada antes de `writeonmars-close-project`.

## Qué hace

1. **Agrega errores comunes**: recorre la sección "Error frecuente" de
   cada capítulo y consolida `common-errors.md` en la raíz del proyecto
   editorial. Cada entrada cumple data-model.md §9: error,
   capitulo_origen, sintoma, causa_probable, que_revisar.
2. **Construye `index.md`**: en la raíz del proyecto, con:
   - Promesa global de la guía.
   - "Para quién es" / "Para quién no es" (derivado del brief).
   - "Qué vas a aprender" (resumen de promesas por capítulo).
   - Ruta de lectura rápida (orden de capítulos con su promesa).
   - Enlaces a `glossary.md`, `common-errors.md`, `templates/` y a cada
     capítulo.
3. **Valida `glossary.md`**: confirma que `writeonmars-glossary` lo
   produjo y que la cobertura SC-004 está al 100%.
4. **Valida `templates/`**: si existe la carpeta, comprueba que cada
   plantilla tenga nombre, propósito, campos a rellenar y ejemplo lleno
   (data-model.md §10).
5. **Verifica cajas visuales por capítulo**: al menos una de "Quédate
   con esto", "Qué hacer mañana", "Síntoma → causa probable".
6. **Verifica formateo**: títulos claros sin emoji, ejemplos
   diferenciados del cuerpo (bloques de código, callouts), sin bloques
   de texto excesivos (>~ 12 líneas seguidas sin pausa visual).
7. Emite bloque "Pasada 5 — Formato" en `findings.md` y checklist
   firmable.

## Inputs

- Todos los `chapters/[###]-titulo.md`.
- `specs/[###-feature]/glossary.md` y/o `glossary.md` raíz.
- `templates/` (si existe).
- `specs/[###-feature]/spec.md` para promesa global.
- `.specify/templates/checklist-template.md` § "Pasada 5 — Formato".
- `agents/claude/prompts/pasada-5.md`.

## Outputs

- `common-errors.md` en la raíz del proyecto editorial.
- `index.md` en la raíz del proyecto editorial.
- Bloque "Pasada 5 — Formato" en `findings.md`.
- `checklists/[###-feature]/pasada-5.md`.

## Procedimiento

1. Recorrer `chapters/`. Para cada capítulo extraer la sección "Error
   frecuente" (entre los encabezados sexto y séptimo del esquema de
   capítulo) y mapear a registro de errores comunes.
2. Componer `common-errors.md` con tabla o secciones por error,
   manteniendo `capitulo_origen` para trazabilidad.
3. Construir `index.md` a partir del brief y del temario aprobado.
4. Para cada capítulo, comprobar:
   - **Sección `## Fuentes` presente al cierre** (obligatoria desde v1.3.0). Su
     ausencia es un finding de formato.
   - Cajas visuales y "Qué hacer en la práctica" / checklist: **solo si las adendas
     del proyecto los declaran obligatorios** para el sector. No los marques como
     falta si el sector los relaja o centraliza (p. ej. tecnología).
   - Sin bloques de texto excesivos.
5. Validar `glossary.md` y `templates/`.
6. Emitir findings por incumplimiento. `severidad: medio` para faltas de
   formato; `severidad: critico` solo cuando la cobertura del glosario
   está rota o el `index.md` no se puede construir por falta de datos.
7. Materializar checklist y dejar firma `autonomous` (default).

## Lente específica (constitución § V.5 + § Estándares editoriales)

- Cajas visuales útiles, no decorativas.
- Ejemplos diferenciados del cuerpo expositivo.
- Títulos claros, sin ingenio gratuito ni emoji.
- Índice navegable.
- Sin bloques de texto excesivos.
- Estructura de guía completa: portada / promesa / "Para quién es" /
  "Para quién no es" / "Qué vas a aprender" / ruta de lectura /
  glosario / errores comunes / plantillas.

## Default signing

`autonomous` (signing_matrix v1).

## Errores comunes

- Capítulos sin sección "Error frecuente": warning, no se incluyen en
  `common-errors.md`.
- `templates/` con plantillas incompletas: warning con sugerencia de
  refactor.
- `index.md` con enlaces rotos: error crítico.
- Cajas visuales ausentes en > 20% de los capítulos: finding crítico
  porque viola el estándar editorial.

## FR cubierta

- FR-018, FR-019.
- FR-029 (artefactos editoriales finales: index, common-errors,
  templates, glossary).
- Constitución § V.5 y § Estándares editoriales.

## Versión

v0.1.0-mvp — 2026-05-06
