# Procedimiento de sincronización desde el vault

Este documento describe cómo refrescar las skills bundled del repositorio canónico (`/marcela-prose`, `/technical-guide-design`) cuando sus fuentes externas reciben cambios sustantivos.

## Cuándo aplicar este procedimiento

Cuando una skill canónica recibe un cambio sustantivo en su origen externo y queremos propagarlo al repo canónico de Write.OnMars. Cambios sustantivos incluyen:

- Reglas nuevas o modificadas que afectan el comportamiento de la skill.
- Calibraciones nuevas (samples antes/después) que la skill consume.
- Reorganizaciones del SKILL.md o de su carpeta `references/`.

Cambios menores (typos, mejoras de redacción no calibrantes) pueden esperar a una sincronización rutinaria, semestral o anual.

## Por qué este flujo unidireccional

Las skills bundled son fuente de verdad del framework: lo que distribuye Write.OnMars es lo que vive en este repo. Las externas (vault de Obsidian, repos individuales) son fuente de evolución: ahí se experimenta, se itera y se calibra. La sincronización va siempre de la fuente externa al repo canónico, nunca al revés. Esto evita que el repo canónico arrastre experimentos a medio cocinar y mantiene un único rumbo de evolución.

## Cómo sincronizar

1. **Confirmar versión actual**. Leer el archivo `VERSION` de la skill en `.claude/skills/<skill>/VERSION`. Anotar el semver y el hash registrados.
2. **Hacer un dry-run**. Comparar origen y destino con `diff -r`:
   ```bash
   diff -r <ORIGEN> .claude/skills/<skill>
   ```
   El output indica qué archivos cambian. Revisar caso por caso.
3. **Decidir el bump de versión**. Aplicar semver:
   - MAJOR (`X+1.0.0`) cuando el cambio rompe el contrato de la skill (renombre de archivos referenciados por otras skills, eliminación de reglas que el harness asume).
   - MINOR (`X.Y+1.0`) cuando se añaden capacidades sin romper consumidores (reglas nuevas, calibraciones nuevas).
   - PATCH (`X.Y.Z+1`) cuando son aclaraciones, typos o reescrituras que no cambian el comportamiento.
4. **Copiar el contenido**. Usar `rsync -a` (sin `--delete` salvo justificación explícita) para preservar la estructura completa, incluida `references/`:
   ```bash
   rsync -a <ORIGEN>/ .claude/skills/<skill>/
   ```
5. **Actualizar `VERSION`**. Formato canónico: `vX.Y.Z-import-YYYY-MM-DD+<hash>`. Usar el commit hash full del origen si es git, o `sha256(SKILL.md, primeros 12 chars)` si la fuente es vault iCloud sin git. Documentar en el cuerpo del archivo: origen, tipo de fuente, hash, fecha de import y referencia a este documento para el procedimiento de re-sync.
6. **Actualizar `docs/compatibility-matrix.md`** si el cambio afecta a la matriz (por ejemplo, una skill nueva o un cambio que altera el contrato con el harness).
7. **Ejecutar smoke tests**. Cuando exista `tests/smoke/run-all.sh`, correrlo y archivar resultados. Si la sincronización rompe alguna skill `writeonmars-*` que envuelve a la sincronizada, hay que ajustar antes de cerrar.
8. **Commit dedicado**. Mensaje canónico: `chore: sync <skill> from vault to vX.Y.Z`. No mezclar la sincronización con cambios de código del framework: un commit limpio facilita el rollback.

## Reglas de oro

- Nunca editar el contenido de la skill en el repo canónico directamente. Siempre se edita en el origen externo y se sincroniza. Editar en el destino crea drift silencioso entre fuentes.
- El repo canónico no arrastra historia git del origen externo. Lo único que persiste es el hash en el `VERSION` file. Para auditar la evolución de la skill, hay que volver al repo o vault de origen.
- Pilotos editoriales que dependan de una versión específica deben pinear la versión en el manifiesto del proyecto destino (`skills[].version`). Una sincronización en el repo canónico no afecta a proyectos ya instalados hasta que ejecutan `writeonmars-update`.

## Bitácora del primer import (T006 + T007)

**Fecha**: 2026-05-06.

### `/marcela-prose` (T006)

- **Origen**: `/Users/marsgotta/Projects/mars-voice/skill/`.
- **Tipo de origen**: repositorio Git.
- **Commit hash de origen**: `8fd61b62c30c4e33f73521b028b4ac7c78cf5ff4` (2026-05-05 18:16:29 +0200).
- **sha256 (SKILL.md, primeros 12 chars)**: `52a4c11f2f20`.
- **Versión registrada**: `v0.1.0-import-2026-05-06+8fd61b62c30c`.
- **Contenido copiado**: `SKILL.md` y `references/` completo (incluye `antipatrones-llm.md`, `arquitectura-capitulo.md`, `calibration-digest.md`, `calibration-samples/`, `prohibiciones.md`, `prosa-con-pulso.md`, `referentes.md`, `registros-por-modalidad.md`).
- **Destino**: `.claude/skills/marcela-prose/`.
- **Decisiones**: se copió todo el contenido de `skill/` mediante `rsync -a` sin `--delete`. No se descartó ningún archivo. Los archivos de nivel superior del repo `mars-voice` (README.md, AGENTS.md, PLAN.md, scripts/, research/, .git/) no se copiaron porque pertenecen al repo de evolución, no a la skill ejecutable.

### `/technical-guide-design` (T007)

- **Origen**: `/Users/marsgotta/Library/Mobile Documents/iCloud~md~obsidian/Documents/Mars/skills/generals/technical-guide-design/`.
- **Tipo de origen**: Obsidian vault (iCloud, no versionado por git).
- **sha256 (SKILL.md, primeros 12 chars)**: `2387cabf9411`.
- **Versión registrada**: `v0.1.0-import-2026-05-06+2387cabf9411`.
- **Contenido copiado**: `SKILL.md` y `references/` (incluye `prose-pitfalls.md` y `research-digest.md`).
- **Destino**: `.claude/skills/technical-guide-design/`.
- **Decisiones**: se eliminaron los archivos `.DS_Store` introducidos por macOS Finder; no aportan información y contaminan el repo. El resto se copió íntegro mediante `rsync -a`.

Para futuras sincronizaciones, repetir el procedimiento descrito en este documento y añadir una entrada nueva en esta bitácora con la fecha, hashes y bump de versión aplicado.
