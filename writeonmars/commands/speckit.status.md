---
description: "Dashboard determinista del proyecto editorial: estado de pasadas, firmas, hallazgos por severidad y los tres gates de cierre (críticos, firmas, completitud). Read-only. Sustituye wom status y wom close."
---

# Estado de la guía

Muestra en una pantalla el estado de la producción: capítulos redactados, cada
pasada de revisión con su estado y firma, hallazgos por severidad, y si el
proyecto puede cerrarse (gates de críticos abiertos + firmas humanas faltantes).

## Prerequisites

- El proyecto debe tener `specs/<###-feature>/findings.md` (esquema
  pass-output v1.0). Si aún no existe, el comando lo indica sin asumir estado.
- Opcional: `.writeonmars-manifest.json` con `signing_matrix` para evaluar el
  gate de firma humana.

## Execution

```bash
python3 <ruta-preset>/scripts/status.py
```

(En desarrollo: `python3 writeonmars/scripts/status.py`.)

Flags:

- `--gate` — además de imprimir el dashboard, devuelve exit 1 si el proyecto NO
  cierra. Útil en hooks y en Paperclip para frenar la publicación.
- `--spec <dir>` — fuerza un spec concreto (default: el de número más alto).
- `--project-dir <ruta>` — raíz del proyecto.

## Output

Tabla `pasada × estado × firma × hallazgos` y un bloque de cierre con los dos
gates:

1. **Sin hallazgos críticos abiertos** (FR-020).
2. **Firmas humanas completas** donde la matriz del manifiesto exige `human`
   (FR-020a) — típicamente naturalidad y precisión.

Veredicto final: `PROYECTO CERRABLE` o `BLOQUEADO`, con la lista de motivos.

## Relación con el cierre

Este comando absorbe lo que hacía `wom status` y el gate de `wom close`. Para
cerrar formalmente, usa `--gate`: exit 0 = cerrable, exit 1 = bloqueado con la
lista de blockers.
