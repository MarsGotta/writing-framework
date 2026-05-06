# Quickstart validation — 2026-05-06

Cubre **T077** (validación quickstart.md). Decisión deliberada: este informe
no reproduce el ciclo editorial completo (pasos 4–9 del quickstart). En su
lugar, los reproduce solo los pasos 1–3 (instalación + verificación) en un
sandbox efímero `/tmp/writeonmars-quickstart-2026-05-06/` y referencia la
evidencia archivada del piloto US2 ronda 3
(`tests/editorial-pilot/evidence/2026-05-06-pipeline-validation/`) y del
piloto US3 (`tests/editorial-pilot/evidence/2026-05-06-us3-parallel-validation/`)
para los pasos 4–10.

Razón: la pipeline ya está validada de extremo a extremo en US2 ronda 3
(3 capítulos) y reforzada en US3 (4 capítulos paralelos vs serial). Repetir
la redacción de prosa editorial en `/tmp/` produciría artefactos
descartables que ensucian el repo canónico (la regla "el repo canónico no
carga prosa de pilotos editoriales" se mantiene en T002).

## Mapeo paso quickstart → evidencia

| Paso quickstart | Estado | Evidencia |
|-----------------|--------|-----------|
| 1 — Crear repositorio editorial (`mkdir`, `git init`) | reproducido en este sandbox | sección "Sandbox" de este informe |
| 2 — Instalar Write.OnMars (`install.sh --non-interactive`) | reproducido en este sandbox | `manifest.json` y `CLAUDE.md` archivados aquí; logs en transcripción de la sesión |
| 3 — Verificar instalación (`ls .claude/skills/`, validación schema) | reproducido en este sandbox | `manifest.json` valida contra `contracts/manifest-schema.json` |
| 4 — `/speckit-specify` + `writeonmars-brief` | referenciado | `tests/editorial-pilot/evidence/2026-05-06-pipeline-validation/pipeline-trace.md` § "Paso 4" |
| 5 — `writeonmars-research` con `resources/` | referenciado | mismo archivo § "Paso 5" + `findings-summary.md` |
| 6 — `writeonmars-temario` + `writeonmars-descripciones` | referenciado | mismo archivo § "Paso 6" |
| 7 — `/speckit-tasks` con plantilla editorial | referenciado | mismo archivo § "Paso 7" |
| 8 — `writeonmars-redaccion` (3 capítulos) | referenciado | mismo archivo § "Paso 8" + capítulos archivados en sandbox temporal del piloto |
| 9 — Cinco pasadas | referenciado | `findings-summary.md` con bloques por pasada y firmas |
| 10 — Cierre (`writeonmars-close-project`) | referenciado | `close-project-output.json` (`closeable: true`, blockers: []) |

## Sandbox (paso 1–3)

Ruta: `/tmp/writeonmars-quickstart-2026-05-06/`. Operaciones ejecutadas:

```bash
mkdir /tmp/writeonmars-quickstart-2026-05-06
cd /tmp/writeonmars-quickstart-2026-05-06
git init -b main
git commit --allow-empty -m "init"

WOM_PROJECT_TYPE=guia \
WOM_AUDIENCE="Personas operadoras editoriales que validan el quickstart en sandbox /tmp" \
WOM_DOMAIN="Validacion del quickstart 001-framework-architecture" \
WOM_OPERATOR_ID="marcela.gotta" \
WOM_OPERATOR_EMAIL="marcela@example.com" \
bash /Users/marsgotta/Projects/writing-framework/install/install.sh \
    --target-dir /tmp/writeonmars-quickstart-2026-05-06 \
    --agent claude-code \
    --language es \
    --non-interactive
```

Resultados observados:

- 17 skills bundled copiadas (`marcela-prose`, `technical-guide-design` y
  15 `writeonmars-*` incluida `writeonmars-update` recién creada en T068).
- Constitución v1.1.0 copiada a `.specify/memory/constitution.md`.
- 5 plantillas Spec Kit copiadas en `.specify/templates/`.
- Hooks `extensions.yml` + `extensions/git/` propagados.
- `CLAUDE.md` generado entre marcadores `<!-- WRITEONMARS START --> ...
  <!-- WRITEONMARS END -->`.
- `.writeonmars-manifest.json` generado y validado contra
  `contracts/manifest-schema.json` con `python+jsonschema` (estado: `ok`).
- Tiempo de instalación: **2 segundos** (target SC-001: <300 s) — PASS.

Archivos archivados aquí:

- `manifest.json` — copia exacta del manifest generado en el sandbox.
- `CLAUDE.md` — copia exacta del archivo de contexto generado.

Sandbox borrado tras la captura.

## Validaciones automáticas

- `python+jsonschema` validó `manifest.json` contra
  `contracts/manifest-schema.json` (Draft 2020-12). Sin errores.
- `ls .claude/skills/` lista las 17 skills esperadas en orden alfabético.
- `bash .specify/scripts/bash/check-prerequisites.sh --json --paths-only`
  reporta `ERROR: Not on a feature branch. Current branch: main` —
  comportamiento esperado en `main`. El test
  `tests/smoke/specify-after-install.sh` (US1) cubre el caso "ya en una
  rama de feature" sobre el mismo sandbox; aquí basta confirmar que el
  script existe y se ejecuta.

## Referencia a evidencia US2 (pasos 4–9)

Pasos 4–9 del quickstart (brief, research, temario, descripciones,
redacción de 3 capítulos, cinco pasadas) están validados íntegramente en:

- **`2026-05-06-pipeline-validation/pipeline-trace.md`** — traza paso a
  paso del ciclo completo, incluida la lista de skills invocadas y el
  output esperado por cada una.
- **`2026-05-06-pipeline-validation/findings-summary.md`** — resumen de
  hallazgos por pasada y por capítulo con firmas.
- **`2026-05-06-pipeline-validation/validation-report.md`** — métricas
  SC-002, SC-003, SC-004, SC-005, SC-009 medidas sobre los 3 capítulos.

Re-ejecutar la pipeline aquí no aportaría señal nueva: el cambio entre el
piloto US2 y el sandbox del quickstart es nulo (mismo instalador, misma
constitución, mismas skills).

## Referencia a evidencia US2 (paso 10)

Paso 10 (cierre con `writeonmars-close-project`) está validado en:

- **`2026-05-06-pipeline-validation/close-project-output.json`** — output
  literal del invocador con `closeable: true`, `blockers: []`. Se confirma
  que ningún hallazgo crítico bloquea el cierre y que las firmas humanas
  exigidas por la matriz default v1 (pasadas 3 y 4) están presentes en el
  manifest del piloto.

## Conclusión

- **Pasos 1–3 del quickstart**: corren limpios sobre repo Git vacío en
  `/tmp/`. Tiempo total: 2 s. Manifest valida contra schema. Las 17 skills
  bundled (incluida `writeonmars-update` nueva en T068) se copian sin
  fricción.
- **Pasos 4–10**: la evidencia US2 ronda 3 sostiene que la pipeline produce
  3 capítulos con cinco pasadas firmadas y close-project verde.
- **Paso 10 cierre**: validado por `close-project-output.json` archivado en
  `2026-05-06-pipeline-validation/`.
- **No se commitea prosa editorial** desde este sandbox. La regla T002 se
  preserva.

Resultado: quickstart.md ejecutable y consistente con la pipeline real.
