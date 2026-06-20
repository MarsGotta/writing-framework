---
description: "Memoria de búsqueda del proyecto: indexa el markdown (capítulos, research, glosario, findings) y permite buscar contenido previo para no contradecir ni redefinir lo ya escrito."
---

# Memoria del proyecto

Construye y consulta un índice del contenido del proyecto. Úsalo antes de
redactar o en las pasadas para comprobar si un término ya se definió, si un dato
ya se citó o si un capítulo previo ya cubre algo.

## Execution

```bash
# Construir / refrescar el índice (caché, reconstruible desde el repo):
python3 <ruta-preset>/scripts/index.py build

# Buscar:
python3 <ruta-preset>/scripts/index.py query "context window" --top 5
```

(En desarrollo: `python3 writeonmars/scripts/index.py ...`.)

## Cuándo usarlo

- **Antes de redactar un capítulo**: busca el término clave para ver dónde se
  definió y enlazar en lugar de redefinir (Principio IV, univocidad).
- **En la pasada de precisión**: comprueba si una afirmación ya tiene cita en
  `research.md`.
- **En la pasada de coherencia global**: detecta solapamientos entre capítulos.

## Backends

Autodetecta `rank-bm25` (ranking BM25) y, si no está, usa un cosine sobre TF sin
dependencias. El índice es caché: nunca fuente de verdad, siempre reconstruible
con `build` (constitución § Arquitectura del framework). Conviene reconstruirlo
tras cambios grandes.
