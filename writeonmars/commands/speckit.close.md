---
description: "Cierre del proyecto editorial: evalúa los gates (críticos abiertos + firmas humanas) y, si pasa, genera el PDF. Si está bloqueado, lista los blockers y no exporta."
---

# Cerrar la guía

Cierre determinista en un paso: comprueba que el proyecto puede cerrarse y, solo
entonces, genera el PDF final. Equivale a `wom close` + `export` encadenados.

## Prerequisites

- `specs/<###-feature>/findings.md` (estado de las pasadas).
- `.writeonmars-manifest.json` con `signing_matrix` (para el gate de firmas).
- Para el PDF: `pandoc` y Chrome/Chromium (ver `speckit.export`).

## Execution

```bash
python3 <ruta-preset>/scripts/close.py
```

(En desarrollo: `python3 writeonmars/scripts/close.py`.)

Flujo:

1. Ejecuta `status.py --gate`. Si hay un crítico abierto (FR-020) o falta una
   firma humana donde la matriz la exige (FR-020a) → imprime los blockers y sale
   con exit 1 **sin exportar**.
2. Si el gate pasa → ejecuta `export.py` y genera el PDF.

Opciones:

- `--no-export` — solo evalúa el gate (útil en CI o como check rápido).
- Flags de `export.py` (título, salida, `--chrome`…) se pasan tal cual.

## Automatización (opcional)

Como es determinista, Paperclip puede llamarlo en el cierre de cada guía. Para
dispararlo dentro del ciclo Spec Kit, el evento más cercano es `after_analyze`
(en el ciclo editorial, `/speckit-analyze` es el gate final). El registro de
hooks vive en `.specify/extensions.yml` y pertenece a una extensión, no al
preset; mientras tanto, llamar a `close.py` cubre el caso en ambos modos.
