---
description: "Captura el brief editorial obligatorio (9 campos) haciendo preguntas, y bloquea hasta que los campos críticos estén resueltos. Checkpoint humano 1. Neutral de modelo."
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

1. Crea o actualiza `specs/<###-feature>/spec.md` con los **nueve campos**:
   audiencia, problema, resultado esperado, nivel, tono, conceptos obligatorios,
   ejemplo recurrente, riesgos, acciones prácticas.
2. Lo que no puedas inferir, márcalo `[NEEDS CLARIFICATION]` y **pregúntaselo a la
   persona** en lenguaje claro. No inventes audiencia ni ejemplo recurrente.
3. Espera las respuestas y la firma. Esto es un checkpoint humano: no sigas sin él.

## Bloqueo

No avances a `speckit.research` mientras sigan sin resolver los campos críticos:
**audiencia, ejemplo recurrente, resultado esperado**.

## Output

`specs/<###-feature>/spec.md` con los nueve campos completos y un bloque de
contexto del proyecto (audiencia, ejemplo recurrente, tono) para los pasos
siguientes.
