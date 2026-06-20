---
description: "Bootstrap del proyecto editorial: instala la constitución y crea el manifest, que es lo que un preset no puede copiar. Correr UNA vez tras 'specify preset add'. Neutral de modelo."
---

# Setup del proyecto editorial

Un preset registra plantillas y comandos, pero no puede escribir la constitución
(`.specify/memory/`) ni el manifest del proyecto. Este comando cubre ese hueco en
un paso. Es lo primero que se corre en un proyecto nuevo, después de
`specify preset add`.

## Qué haces

Ejecuta el script de bootstrap del preset:

```bash
python3 .specify/presets/writeonmars/scripts/bootstrap.py
```

(En desarrollo dentro del repo del framework: `python3 writeonmars/scripts/bootstrap.py --project-dir <ruta>`.)

Hace dos cosas:

1. Copia el **núcleo de la constitución** a `.specify/memory/constitution.md`
   (el que trae el preset en `memory/constitution.md`). No lo regenera por proyecto:
   las reglas universales (voz, brief, revisión, neutralidad) son el núcleo. Lo que
   sí cambia por guía (sector, tono, terminología, gobernanza) lo fija el paso
   siguiente, `/speckit-constitution`, como una capa de **adendas** sobre el núcleo.
2. Crea un **`.writeonmars-manifest.json`** inicial con la matriz de firmas por
   defecto: **todas las pasadas autónomas**; el control humano es el PDF anotado al
   final, no pasada por pasada. (Para una guía delicada puedes poner `human` en
   alguna pasada.)

Flags útiles: `--operator <id>`, `--email <correo>`, `--force` (sobrescribe
constitución y manifest existentes).

## Después

Primer paso del ciclo: `/speckit-constitution` fija las adendas del proyecto
(sector, tono, terminología, gobernanza) con un cuestionario guiado y valores por
defecto. Luego: `speckit.specify` → `speckit.research` → `speckit.plan` →
`speckit.implement` → `speckit.review`.

## Por qué no es automático

`specify preset add` no ejecuta instaladores ni escribe en `.specify/memory/`. Por
eso este paso queda como un único comando explícito en vez de un copiado manual de
varios archivos.
