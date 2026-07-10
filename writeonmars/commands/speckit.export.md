---
description: "Genera el PDF editorial de la guía (portada + índice navegable + capítulos) reutilizando el estilo de markdown-to-pdf. Determinista: no necesita decisiones del agente."
---

# Exportar la guía a PDF

Genera el PDF final de la guía editorial ensamblando los capítulos en orden, con
portada derivada del brief e índice derivado del temario. Reutiliza la hoja de
estilo editorial del preset (`writeonmars/assets/style.css`, compartida con la
skill global `markdown-to-pdf`).

## User Input

```text
$ARGUMENTS
```

Considera el input del usuario antes de proceder: puede traer título, subtítulo,
eyebrow, año o ruta de salida.

## Prerequisites

- `pandoc` instalado (`which pandoc`).
- Chrome o Chromium para el render headless. En macOS, Google Chrome; en
  Linux/Paperclip, `chromium`. Si no está en una ruta estándar, pásalo con
  `--chrome <ruta>` o la variable `WOM_CHROME`.
- El proyecto debe tener `specs/<###-feature>/spec.md` (brief), `plan.md`
  (temario) y `chapters/<NN>-titulo.md`.

## Execution

Ejecuta el script de export del preset desde la raíz del proyecto editorial:

```bash
python3 <ruta-preset>/scripts/export.py
```

(En desarrollo dentro del repo del framework: `python3 writeonmars/scripts/export.py`.)

El script, sin más argumentos:

1. Localiza el spec de número más alto y lee el título del brief (`spec.md`).
2. Lee el temario de `plan.md` (`Número | Título | Promesa`) y lo usa como índice
   (la promesa es la descripción de cada entrada).
3. Convierte `README.md`, cada `chapters/<NN>-*.md` y el material de referencia
   (`glosario.md`/`glossary.md`, `anexos.md`, `common-errors.md`) con pandoc.
4. Ensambla portada + índice + cuerpo y genera el PDF con Chrome/Chromium.

Flags útiles (todos opcionales; el usuario puede pedirlos):

- `--title`, `--subtitle`, `--eyebrow`, `--meta` — sobrescriben la portada.
- `--output <ruta.pdf>` — ruta de salida (default: `<slug-título>.pdf`).
- `--spec <dir>`, `--chapters-dir <dir>` — si el layout no es el estándar.
- `--chrome <ruta>` — binario de Chrome/Chromium.
- `--keep-temp` — conserva el HTML intermedio para depurar.

## Output

Un PDF A4 con tipografía serif, portada sin número de página, índice navegable
con enlaces internos clicables, page-break por capítulo y numeración en pie.
Reporta la ruta del PDF, el título y el número de capítulos.

## Automatización

Como es determinista, puede dispararse en un hook `after_close` o por Paperclip
sin intervención. No requiere decisiones del agente salvo que el usuario quiera
sobrescribir portada o rutas.

## Pista corta

Si el manifiesto declara `track: corta` (`.writeonmars-manifest.json`), la invocación no
cambia: `export.py` detecta la pista por sí solo. Produce un PDF de pieza única con
portada compacta —título, autora y fecha—, sin índice de capítulos, conservando la
sección `## Fuentes` con el estilo `.chapter-sources`.
