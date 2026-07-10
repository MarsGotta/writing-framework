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

## Pista corta

Si el manifiesto declara `track: corta` (`.writeonmars-manifest.json`), el brief se
recoge en una sola ronda y su firma materializa el temario degenerado.

- Captura los **ocho campos descriptivos más el título y la promesa de la pieza** en
  **una sola tanda** de preguntas. El checkpoint humano 1 sigue intacto: sin firma no
  hay avance, y no materializas el temario hasta que el brief queda firmado.
- Al quedar firmado el brief, escribe `specs/<###-feature>/plan.md` con una sección
  `## Temario` de **una sola fila**:

  ```markdown
  ## Temario

  | Número | Título | Promesa | Estructura aplicada |
  |--------|--------|---------|---------------------|
  | 1 | <título firmado en el brief> | <promesa firmada en el brief> | didactica_v1 |
  ```

  Copia el título y la promesa **tal cual** de los campos firmados; no los reescribes
  ni los "mejoras". Con esa fila, `chapters_expected == 1` y el paso `plan` desaparece
  del ciclo sin tocar `status.py`.

**Resolución del tono.** Cuando `bootstrap --sector` fija las adendas **por
referencia**, el bloque `### Tono calibrado` de `.specify/memory/constitution.md`
remite al sector en lugar de escribir el tono palabra por palabra. Si ese bloque
declara las adendas por referencia, sigue su puntero hasta
`.specify/presets/writeonmars/references/sectores/<slug>.md` —secciones
`## Tono por defecto` y `## Persona gramatical y registro`— y refleja ese tono como
eco en el campo 5. El bloque de adendas nombra la base en forma corta
(`references/sectores/<slug>.md`); la ruta de arriba es la que resuelve dentro de un
proyecto con el preset instalado. Mientras `manifest.sector` tenga valor, **no
sugieras correr `/speckit-constitution`**: el sector ya dejó la capa normativa escrita
y la pista corta omite ese paso. Es el mismo patrón con el que
`speckit.review-voice` resuelve su registro desde el default del sector.
