---
description: "Aplica al texto los hallazgos abiertos de findings.md (los que marcó la revisión): reescribe SOLO los pasajes señalados (frase_original → reescritura_sugerida) y marca resuelto. Cierra el loop de revisión. Neutral de modelo."
---

# Corregir (aplicar los hallazgos de la revisión)

Cierra el loop. Las pasadas de `review` **marcan** hallazgos en `findings.md`; este
comando los **aplica** al texto. Es quirúrgico: toca solo los pasajes señalados, no
reescribe el capítulo entero.

Aplicar es redactar, así que **lo puede correr el modelo que escribió** (la
independencia importa en la revisión, no en la corrección).

## User Input

```text
$ARGUMENTS
```

Capítulo(s) o IDs de hallazgo (p. ej. `1`, `1,2` o `F-4.1`). Sin argumento: todos
los hallazgos con `estado: abierto`.

## Inputs

- `specs/<###-feature>/findings.md` (los hallazgos de las pasadas).
- Los capítulos en `chapters/`.
- Prosa-base: `.specify/presets/writeonmars/references/prosa/SKILL.md`,
  registro: `.specify/presets/writeonmars/references/registros/<registro>/SKILL.md`
  (del manifiesto o default del sector) y voz:
  `.specify/presets/writeonmars/references/voz/SKILL.md` (para hallazgos de
  naturalidad; la reescritura respeta el hilo, capa 1, el registro, capa 2,
  y la voz, capa 3). `research.md` (para hallazgos de precisión).

## Qué haces

Para cada hallazgo con `estado: abierto` (de los pedidos):

1. Abre `chapters/<capitulo>` y localiza la `frase_original`.
2. Aplica la `reescritura_sugerida` (o el arreglo que describe `problema`),
   **manteniendo la voz**. Para precisión: corrige el dato con su cita; si no hay
   fuente, **no inventes** — déjalo `abierto` (seguirá bloqueando el cierre).
3. Marca el hallazgo como `resuelto` en `findings.md` (no lo borres: trazabilidad,
   según `.specify/presets/writeonmars/contracts/pass-output-schema.md`).

Tras corregir, conviene re-correr la pasada afectada (`speckit.review.<dim> N`)
para confirmar que el arreglo cierra el hallazgo.

## Output

Capítulos corregidos solo en los pasajes señalados + `findings.md` con los
hallazgos marcados `resuelto`. Los `critico` sin fuente quedan `abierto` y bloquean
`speckit.close`.
