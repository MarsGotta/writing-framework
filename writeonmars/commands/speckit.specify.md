---
description: "Captura el brief editorial (8 campos descriptivos) haciendo preguntas; el tono se hereda de las adendas del proyecto. Bloquea hasta que los campos críticos estén resueltos. Checkpoint humano 1. Neutral de modelo."
---

# Brief editorial

Materializa el Principio III: ninguna guía arranca sin un brief explícito. Tú, el
agente (cualquier modelo), recoges el brief preguntando lo que falte y lo dejas
firmado por la persona.

## User Input

```text
$ARGUMENTS
```

El tema en lenguaje natural. Si está vacío, pídelo.

## Inputs

- El tema. Las fuentes en `resources/` si las hay. El manifiesto del proyecto
  (`.writeonmars-manifest.json`).
- Detalle del método: `.specify/presets/writeonmars/references/metodo/writeonmars-brief/SKILL.md`.

## Qué haces

1. Crea o actualiza `specs/<###-feature>/spec.md` con los **ocho campos
   descriptivos** que capturas preguntando: audiencia, problema, resultado
   esperado, nivel, conceptos obligatorios, ejemplo recurrente, riesgos, acciones
   prácticas. El **tono** (campo 5) NO se pregunta aquí: es normativo y ya está
   calibrado en las adendas del proyecto (`.specify/memory/constitution.md` →
   Tono calibrado, fijado por `/speckit-constitution`). Léelo de ahí y refléjalo
   en el campo 5 como eco; si no existen adendas, sugiere correr
   `/speckit-constitution` primero.
2. Lo que no puedas inferir, márcalo `[NEEDS CLARIFICATION]` y **pregúntaselo a la
   persona** en lenguaje claro. No inventes audiencia ni ejemplo recurrente.
3. Espera las respuestas y la firma. Esto es un checkpoint humano: no sigas sin él.

## Bloqueo

No avances a `speckit.research` mientras sigan sin resolver los campos críticos:
**audiencia, ejemplo recurrente, resultado esperado**.

## Output

`specs/<###-feature>/spec.md` con los ocho campos descriptivos completos, el campo
5 reflejando el tono de las adendas, y un bloque de contexto del proyecto
(audiencia, ejemplo recurrente, tono heredado) para los pasos siguientes.
