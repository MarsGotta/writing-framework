---
description: "Genera el README.md de presentación de la guía (Acerca de / promesa / para quién es / para quién no / qué aprenderás / cómo leer) desde el brief y el temario, en la voz de la autora. Es la envoltura que el PDF usa como apertura. Neutral de modelo."
---

# Intro de la guía (README de presentación)

Genera la **presentación** de la guía: lo que el lector ve antes del capítulo 1.
`export` la toma de `README.md` como la sección de apertura "Acerca de esta guía".
Es contenido editorial, así que va con tu voz, no con plantilla genérica.

## User Input

```text
$ARGUMENTS
```

Opcional. `--refresh` para regenerar respetando ediciones manuales marcadas.

## Inputs

- Brief: `specs/<###-feature>/spec.md` (audiencia, problema, resultado esperado,
  nivel, tono, ejemplo recurrente, conceptos obligatorios).
- Temario: `specs/<###-feature>/plan.md` (para "qué vas a aprender").
- Voz: `.specify/presets/writeonmars/references/voz/SKILL.md`. Didáctica:
  `.specify/presets/writeonmars/references/didactica/SKILL.md`.

## Qué haces

Escribe `README.md` en la raíz del proyecto, en la voz de la autora, con:

1. **Título** de la guía + una frase de **promesa concreta** (no eslogan).
2. **Para quién es** — derivado de audiencia y nivel del brief.
3. **Para quién NO es** — el límite honesto (a quién no le sirve esta guía).
4. **Qué vas a aprender** — el resultado esperado, apoyado en las promesas del
   temario (`plan.md`).
5. **Cómo leer esta guía** — ruta rápida (remite a `index.md` si existe), el
   ejemplo recurrente que la atraviesa, y las convenciones (cajas, callouts).

Aperturas y cierres según `references/voz`: concreto y sobrio, **sin marketing** y
sin fórmulas tipo "en esta guía aprenderás…". Una página, no más. Respeta el tono
firmado en el brief.

## Cuándo

Cuando el temario esté fijado, y **antes del `export` final**. Si la corres de
nuevo, refresca el `README.md` sin pisar ediciones manuales marcadas.

## Output

`README.md` en la raíz del proyecto. `export` lo incluye como apertura ("Acerca de
esta guía", `id=intro-readme`). Pasa por la pasada de naturalidad como cualquier
texto de la guía.
