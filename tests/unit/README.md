# tests/unit: suite pytest de los scripts deterministas del preset

Tests unitarios de `writeonmars/scripts/`: fijan el contrato de los scripts que
no requieren agente (la parte determinista del método).

## Qué cubre

- `test_status.py`: parsers de `findings.md` y `claims.md`, índice de
  factualidad, gates de cierre (g1 críticos, g2 firmas, g3 completitud,
  g4 factualidad), ciclo por capítulo, escalera `next_step` y CLI
  (`--json`, `--gate`).
- `test_bootstrap.py`: `read_constitution_version` (pie `**Version**: X.Y.Z`),
  `default_manifest`, `validate_manifest` contra `contracts/manifest-schema.json`
  y flujo end-to-end en `tmp_path` (creación, `--force` preservando adendas).
- `test_export.py`: helpers puros (`slugify`, `newest_spec_dir`, parseo de
  título y temario, ensamblado de portada/índice) y validación de factualidad
  D1-A. Pandoc y Chrome se mockean: nunca se lanzan de verdad.
- `test_index.py`: `tokenize`, chunking por encabezados, scoring TF interno y
  ciclo `build`/`query` (forzando el backend sin dependencias).
- `test_close.py`: orquestación gate + export con subprocesos mockeados, y el
  gate real vía CLI con `--no-export`.

Los fixtures viven en `conftest.py`: un proyecto editorial mínimo y cerrable en
`tmp_path` (`mini_project`) y copias del fixture compartido
`tests/fixtures/003-factualidad/` (`fact_project`). Los scripts se cargan por
ruta con importlib, sin crear paquetes ni mover ficheros.

## Cómo correr

```bash
python3 -m pytest tests/unit -q
```

`pytest` es dependencia de desarrollo del repo, no del preset: el preset sigue
funcionando solo con la librería estándar (más los opcionales que ya documenta
`writeonmars/scripts/requirements.txt`). Instálalo con `pip install pytest`.

## Notas

- Los tests marcados `xfail` documentan bugs conocidos sin modificar los
  scripts; el motivo va en `reason`.
- La suite es hermética: escribe solo en `tmp_path` y trata
  `tests/fixtures/003-factualidad/` como solo lectura (siempre sobre copia).
