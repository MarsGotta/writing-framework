---
description: "Cierra el loop de revisión: ingiere un PDF anotado, lo convierte en change-set y re-despacha quirúrgicamente solo los capítulos afectados. Reescribe únicamente los pasajes señalados."
---

# Aplicar feedback del PDF anotado

Toma el PDF que la revisora anotó, extrae las anotaciones, las mapea a su
capítulo de origen y aplica los cambios SOLO donde hacen falta. No reescribe la
guía entera: re-despacha capítulo por capítulo según el change-set.

## User Input

```text
$ARGUMENTS
```

Debe contener la ruta del PDF anotado. Si no, pídela.

## Prerequisites

- `pymupdf` (recomendado) o `pypdf` instalado: `pip install pymupdf`.
- El proyecto debe tener `chapters/<NN>-*.md` y `specs/<###-feature>/`.

## Execution

### Paso 1 — Extraer el change-set (determinista, sin agente)

```bash
python3 <ruta-preset>/scripts/feedback_intake.py --pdf "<ruta-al-pdf-anotado>"
```

(En desarrollo: `python3 writeonmars/scripts/feedback_intake.py --pdf ...`.)

Genera `specs/<spec>/feedback.md` (log legible) y
`specs/<spec>/feedback-changeset.json` (lista de items con capítulo, línea,
tipo, severidad, texto anclado y comentario). Convención de etiquetas en los
comentarios del PDF: `#dato #voz #estructura #claridad #cobertura` (tipo),
`#recortar #ampliar` (acción), `#critico #medio #bajo` (severidad).

### Paso 2 — Aplicar los cambios (agente, quirúrgico)

Lee `feedback-changeset.json`. Para cada `item` con `estado: abierto`:

1. Abre `chapters/<chapter_file>` y localiza el pasaje por `anchor_text` (o
   `line`).
2. Aplica el cambio según `tipo`:
   - **Voz** → aplica las reglas de `.specify/presets/writeonmars/references/prosa/SKILL.md` (hilo), `.specify/presets/writeonmars/references/registros/<registro>/SKILL.md` (registro del manifiesto) y `.specify/presets/writeonmars/references/voz/SKILL.md` (voz) SOLO sobre ese pasaje.
   - **Dato/precisión** → verifica contra `research.md`; si falta cita, búscala
     o marca el finding como bloqueante; nunca inventes el dato.
   - **Estructura / Claridad / Cobertura / Recortar / Ampliar** → reescribe el
     pasaje aplicando el comentario, manteniendo la voz.
3. Marca el item como `resuelto` en `feedback.md`.

### Paso 3 — Re-correr las pasadas locales de los capítulos tocados

Para cada capítulo en `affected_chapters`, re-ejecuta SOLO sus 3 pasadas locales
(estructura+utilidad, naturalidad, precisión). No toques los capítulos no
afectados.

### Paso 4 — Verificar cierre

Ejecuta `python3 <ruta-preset>/scripts/status.py --gate`. Un `#critico` del
feedback (p.ej. dato sin fuente) bloquea el cierre hasta resolverse.

## Output

- `feedback.md` con los items marcados `resuelto`/`abierto`.
- Los capítulos afectados reescritos solo en los pasajes señalados, con sus
  pasadas locales al día.

## Por qué quirúrgico

El `anchor_text` ata cada cambio a una frase concreta de un archivo concreto, así
que un comentario en el capítulo 7 nunca reescribe el 1–6. Es el equivalente a
`speckit.revise` del preset de ficción, guiado por tu PDF en vez de notas sueltas.
