---
name: writeonmars-contraste
description: Verifica las afirmaciones del capítulo contra los CitationRecord del research.md (pasada 4 — precisión). Trigger cuando la persona diga "verifica las afirmaciones del capítulo", "contraste de fuentes", "pasada 4", "valida precisión".
allowed-tools: Bash, Read, Write, Edit
---

# writeonmars-contraste

Skill que implementa la pasada 4 (precisión) en su capa de contraste:
verifica cada afirmación verificable del capítulo contra al menos un
`CitationRecord` registrado en `research.md`. Materializa FR-016 y FR-017.
Emite el bloque "Pasada 4" en `findings.md` conforme a
`contracts/pass-output-schema.md` v1.0.

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
3. Para cada afirmación, busca al menos un `CitationRecord` que la
   sustente. Marca el resultado como:
   - `verificado` cuando hay ≥ 1 cita compatible.
   - `pendiente` cuando no encuentra cita y el dato es verificable
     (genera finding `severidad: medio`).
   - `desviacion_justificada` cuando el operador firma una decisión
     editorial declarada en `Complexity Tracking` del plan.
4. Verifica volatilidad: afirmaciones marcadas `[VERIFICAR]` o citas
   con `volatil: true` reciben warning si la `fecha_consulta` supera 90
   días.
5. Emite el bloque "Pasada 4" en `findings.md` con un finding por
   afirmación no verificada y `referencias_cita` por afirmación
   verificada (campo obligatorio en pasada 4 según
   pass-output-schema § Finding).

## Inputs

- `chapters/[###]-titulo.md`.
- `specs/[###-feature]/research.md`.
- `specs/[###-feature]/findings.md` (existente; se añaden bloques al
  final).
- `contracts/pass-output-schema.md` v1.0.

## Outputs

- Bloque "Pasada 4 — Precisión" añadido a
  `specs/[###-feature]/findings.md`, con `pasada: 4_precision` y la
  tabla de hallazgos completa.

## Procedimiento

1. Cargar `CitationRecord` del `research.md` e indexarlos por
   `citation_id` y por palabras clave del `fragmento`.
2. Tokenizar el cuerpo del capítulo y detectar afirmaciones verificables.
3. Para cada afirmación, calcular candidatos por similitud léxica con
   los fragmentos. Pedir confirmación al operador en casos ambiguos.
4. Para cada cita usada, verificar:
   - `versionado_aplicable: true` requiere `version_aplicable`.
   - `fecha_consulta` no supera 90 días para datos `volatil`.
   - `motor` no es `unknown`.
5. Generar findings:
   - `severidad: critico` si la afirmación contradice una cita oficial.
   - `severidad: medio` si la afirmación carece de cita.
   - `severidad: bajo` si solo es ambigua.
6. Componer el bloque markdown según el esquema de pasada y añadirlo al
   final de `findings.md` sin sobreescribir bloques previos.
7. Reportar al operador: total de afirmaciones evaluadas, verificadas,
   pendientes y críticas.

## Errores comunes

- `research.md` ausente o vacío: aborta y exige ejecutar
  `writeonmars-research`.
- Afirmaciones que no se pueden mapear a una cita por desfase de
  vocabulario: se sugieren al operador para reformulación o ampliación
  del research.
- Citas con `motor: unknown` (regla 2 del contrato): se descartan y se
  reporta.

## FR cubierta

- FR-016 (toda afirmación verificable contra al menos una cita).
- FR-017 (datos volátiles marcados [VERIFICAR]).

## Versión

v0.1.0-mvp — 2026-05-06
