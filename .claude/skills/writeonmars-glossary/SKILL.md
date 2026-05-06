---
name: writeonmars-glossary
description: Consolida el glosario del proyecto, detecta colisiones de definición y términos huérfanos. Trigger cuando la persona diga "consolida el glosario", "detecta términos huérfanos", "actualiza glossary.md", "valida la cobertura de glosario".
allowed-tools: Bash, Read, Write, Edit
---

# writeonmars-glossary

Skill que materializa FR-015, FR-021 y SC-004. Consume los anexos de
glosario emitidos por cada capítulo (bloque
`<!-- glossary-annex START/END -->`) y los `conceptos_introducidos` del
plan, los consolida en `specs/[###-feature]/glossary.md` (feature) y
`glossary.md` (proyecto-wide), detecta colisiones de definición entre
capítulos y términos huérfanos (técnicos en cuerpo expositivo sin entrada
en glosario).

## Cuándo dispararse

- "consolida el glosario"
- "detecta términos huérfanos"
- "actualiza glossary.md"
- "valida la cobertura de glosario"
- Tras cada redacción de capítulo, antes de la pasada 1.
- Antes de cerrar el proyecto (validación SC-004).

## Qué hace

1. Carga los `chapters/*.md` redactados y extrae:
   - El front-matter YAML (`terminos_introducidos`).
   - El bloque `<!-- glossary-annex START -->` …
     `<!-- glossary-annex END -->`.
2. Carga los `conceptos_introducidos` declarados en
   `## Descripciones encadenadas` del plan.
3. Compara términos entre capítulos:
   - Si el mismo término aparece con definiciones distintas en dos
     capítulos, marca colisión `severidad: critico` (FR-015).
   - Si un término del cuerpo aparece sin entrada en el anexo de
     glosario, marca como huérfano (`severidad: medio`, fix de SC-004).
4. Detecta anglicismos: si un término es marcado `anglicismo_admitido:
   true`, exige `justificacion` (constitución § IV).
5. Renderiza `specs/[###-feature]/glossary.md` siguiendo data-model.md §6
   y propaga al `glossary.md` raíz cuando la guía supera tres capítulos
   (estándar editorial de la constitución).
6. Emite reporte de colisiones, huérfanos y anglicismos sin justificar
   para que la pasada 1 o 5 los aborde.

## Inputs

- `chapters/[###]-titulo.md` (todos los capítulos disponibles).
- `specs/[###-feature]/plan.md` — descripciones encadenadas.
- `.specify/memory/constitution.md` — § IV.

## Outputs

- `specs/[###-feature]/glossary.md` (feature-scope).
- `glossary.md` (project-wide), si ≥ 4 capítulos.
- Reporte con colisiones, términos huérfanos y anglicismos sin
  justificar.

## Procedimiento

1. Recopilar todos los anexos `<!-- glossary-annex -->` de los
   capítulos. Indexar por término.
2. Para cada término con múltiples definiciones, comparar texto y
   reportar colisión cuando difieran semánticamente. Solicitar
   resolución antes de persistir.
3. Para cada capítulo, escanear cuerpo expositivo y comparar contra el
   glosario consolidado. Si encuentra un término técnico (heurística:
   sustantivo capitalizado o término que aparece en
   `conceptos_obligatorios` del brief) sin entrada en el glosario,
   emitir warning de huérfano.
4. Validar que cada `anglicismo_admitido: true` tenga `justificacion`
   apuntando a constitución § IV.
5. Renderizar el glosario consolidado en orden alfabético, con
   `capitulo_origen` indicado.
6. Si el proyecto tiene ≥ 4 capítulos, escribir también `glossary.md`
   en la raíz como vista de proyecto.

## Errores comunes

- Anexo de glosario malformado: la skill lo reporta y deja el término
  fuera del consolidado hasta que el operador lo corrija.
- Colisiones sin resolver: bloquean cierre vía
  `writeonmars-close-project` cuando el finding queda crítico abierto.
- Términos huérfanos: warning, no bloqueante por sí solo, pero la pasada
  5 lo escala.
- Anglicismos sin justificar: warning, exigir justificación en el
  glosario antes de pasada 5.

## FR cubierta

- FR-015 (consolidación y detección de colisiones).
- FR-021 (estándar editorial de glosario obligatorio).
- SC-004 (cobertura del glosario y detección de huérfanos).
- Constitución § IV (anglicismos admitidos con justificación).

## Versión

v0.1.0-mvp — 2026-05-06
