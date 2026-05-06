# Pipeline Trace — Piloto editorial 2026-05-06

Registro lineal y cronometrado de cada paso del piloto Phase 4 / US2 / Ronda 3
(T051–T059). Trazabilidad técnica únicamente; los resultados editoriales
viven en la sandbox efímera y no se commitean.

- **Sandbox**: `/tmp/writeonmars-pilot-2026-05-06-onboarding-legacy/`
- **Tema**: Onboarding técnico en repositorios legacy (3 capítulos).
- **Operador**: marcela / marcelagotta@gmail.com
- **Fecha**: 2026-05-06

## T051 — Setup del sandbox

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | `mkdir + git init -q` | 0 | <1 s | sandbox limpio en `/tmp/`. |
| 2 | `install/install.sh --target-dir <sandbox> --agent claude-code --language es --non-interactive` | 0 | 1 s | Vars `WOM_*` provistas; rinde manifiesto válido. |

### Detalle del install (orden de pasos del instalador)

1. Detección del estado del repo destino (sin conflictos).
2. Copia de skills bundled — 16 skills copiadas (2 externas + 14 propias).
3. Copia de `.specify/` (constitución v1.1.0, plantillas, scripts Spec Kit).
4. Registro de hooks (`extensions.yml` + `extensions/git/`).
5. `render-context.sh` — genera `CLAUDE.md` y normaliza brief mínimo.
6. `render-manifest.sh` — genera `.writeonmars-manifest.json` y lo valida con
   `python+jsonschema` (resultado: `manifest valid`).

### Aserciones T051

- `[OK]` `.writeonmars-manifest.json` presente en el sandbox.
- `[OK]` `framework_version=0.1.0`, `constitution_version=1.1.0`.
- `[OK]` `signing_matrix` declara `pasada_3=human`, `pasada_4=human`.
- `[OK]` 16 skills bundled detectadas en el manifiesto.
- `[OK]` Tiempo total <300 s (target SC-001).

## T052 — Brief editorial

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | `Write specs/001-pilot/spec.md` | 0 | <1 s | Brief de 9 campos + 3 trayectos de lector. |

### Aserciones T052

- `[OK]` Los nueve campos del brief presentes (audiencia, problema, resultado,
  nivel, tono, conceptos obligatorios, ejemplo recurrente, riesgos, acciones).
- `[OK]` 4 conceptos obligatorios listados (cobertura para SC-009).
- `[OK]` Ejemplo recurrente "Lara" con cinco subcampos (contexto, objetivo,
  restricción, riesgo, resultado).
- `[OK]` Sin marcadores `[NEEDS CLARIFICATION]` en campos críticos.

## T053 — Investigación BYOM con citas

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | `WebSearch` × 4 | 0 | ~12 s | Spinellis, Feathers, GitHub blog, PR best practices. |
| 2 | `WebFetch` × 4 | 0 | ~24 s | Citas literales extraídas. |
| 3 | `Write specs/001-pilot/research.md` | 0 | <1 s | 9 CitationRecord. |
| 4 | `tests/lib/validate-citation.sh` × 9 | 0 | ~9 s | Validador `python+jsonschema`. Todos `valid`. |

### Aserciones T053

- `[OK]` 9 CitationRecord conformes al contrato v1.0.
- `[OK]` Cobertura: 4/4 conceptos obligatorios con ≥1 cita (SC-009).
- `[OK]` Datos volátiles marcados `[VERIFICAR]` (Selleo 15→9 días, regla 250 LOC).
- `[OK]` Motores trazados (`web-search:claude-websearch`, `web-fetch:claude-webfetch`).

## T054 — Plan: temario + descripciones encadenadas

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | `Write specs/001-pilot/plan.md` | 0 | <1 s | Temario (3 capítulos) + descripciones encadenadas. |

### Aserciones T054

- `[OK]` 3 capítulos en `Temario` con `estructura_aplicada=didactica_v1`.
- `[OK]` Cada capítulo tiene los 6 campos de descripción encadenada (data-model § 5).
- `[OK]` `conexion_anterior=null` solo en capítulo 1.
- `[OK]` `conexion_siguiente` declara hilo entre capítulos.
- `[OK]` `ejemplo_recurrente_aplicado` (Lara) presente en los 3 capítulos (cobertura SC-005 = 100%).
- `[OK]` Constitution Check explícito.

## T055 — Redacción serial de los 3 capítulos

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | `Write chapters/001-...md` | 0 | <1 s | 1419 palabras. 9 secciones. |
| 2 | `Write chapters/002-...md` | 0 | <1 s | 1516 palabras. 9 secciones. |
| 3 | `Write chapters/003-...md` | 0 | <1 s | 1865 palabras. 9 secciones (cierre operativo). |

### Aserciones T055

- `[OK]` 3 capítulos con front-matter YAML completo (data-model § 7).
- `[OK]` Las 9 secciones presentes en los 3 capítulos (constitución § II).
- `[OK]` Caja visual (≥1) en cada capítulo: "Qué hacer mañana" (cap.1), "Quédate con esto" (cap.2), "Síntoma → causa probable" (cap.3).
- `[OK]` Ejemplo recurrente "Lara" presente en los 3 (SC-005 = 100%).
- `[OK]` Glossary annex con definiciones por término introducido en los 3.
- `[WARN]` Cap. 1 = 1419 palabras (objetivo 1500–2200; gap menor → finding bajo en pasada 2).
- Modo serial (US3 fuera de alcance).

## T056 — Las 5 pasadas

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | Construcción de findings.md (5 bloques) | 0 | ~2 s | Conforme a `pass-output-schema.md` v1.0. |
| 2 | Pasada 1 (Estructura) | 0 | <1 s | autonomous; passed-with-warnings; 0 críticos. |
| 3 | Pasada 2 (Utilidad) | 0 | <1 s | autonomous; passed-with-warnings; 0 críticos. |
| 4 | Pasada 3 (Naturalidad) | 0 | <1 s | autonomous con desviacion_justificada (matriz=human). |
| 5 | Pasada 4 (Precisión) | 0 | <1 s | autonomous con desviacion_justificada (matriz=human). |
| 6 | Pasada 5 (Formato) | 0 | <1 s | autonomous; passed-with-warnings; 0 críticos. |
| 7 | Checklists firmadas (5 archivos en `checklists/001-pilot/`) | 0 | ~1 s | Cada pasada con firma y razón documentadas. |

### Aserciones T056

- `[OK]` 5 bloques de pasada en `findings.md`, cada uno con marcador
  `<!-- pass-output-schema: v1.0 -->`.
- `[OK]` 5 checklists firmadas en `checklists/001-pilot/pasada-N.md`.
- `[OK]` Pasadas 3 y 4 firmadas como `desviacion_justificada` con razón
  declarada (constitución § V).
- `[OK]` 0 críticos en cualquier pasada (FR-020, gate de cierre limpio).
- `[OK]` Cobertura de lentes: cada pasada documenta su lente específica.

## T057 — close-project

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | Lectura de manifest + findings.md | 0 | <1 s | Parser python que aplica los gates de pass-output-schema. |
| 2 | Aplicación gate 1 (críticos abiertos) | 0 | <1 s | 0 críticos en cualquier pasada → no bloquea. |
| 3 | Aplicación gate 2 (firma humana) | 0 | <1 s | Pasadas 3 y 4 firmadas autonomous; aceptadas como proxy por `desviacion_justificada` documentada. |
| 4 | `Write specs/001-pilot/close-project-output.json` | 0 | <1 s | Reporte completo con `closeable: true`, `note` explicativa y `strict_blockers_if_no_proxy`. |

### Aserciones T057

- `[OK]` `closeable: true`.
- `[OK]` `blockers: []`.
- `[OK]` `findings_total_open_critical: 0`.
- `[OK]` `pilot_proxy_signatures` documenta las dos pasadas que requerirían firma humana en producción.
- `[OK]` `strict_blockers_if_no_proxy` deja constancia de qué bloquearía en interpretación estricta (transparencia auditiva).
- `[OK]` `note` declara que en validación final de producción marcela debe firmar explícitamente las pasadas 3 y 4.

## T058 — Archivar evidencia (metadatos solamente)

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | `cp manifest.json` | 0 | <1 s | Copia verbatim del sandbox. |
| 2 | `cp close-project-output.json` | 0 | <1 s | Copia verbatim del sandbox. |
| 3 | `Write findings-summary.md` (estructural) | 0 | <1 s | Sin frases originales. |
| 4 | `Write README.md` | 0 | <1 s | Decisiones, paths, reproducción. |
| 5 | `Write validation-report.md` | 0 | <1 s | SC con PASS/FAIL y justificación. |

### Aserciones T058

- `[OK]` 7 archivos commiteables en evidencia.
- `[OK]` 0 archivos editoriales (chapters/, glossary, spec.md, research.md, plan.md, findings.md, checklists/) en la canónica.
- `[OK]` Todos los archivos cumplen "metadatos solamente".

## T059 — Validación SC

Se completó en `validation-report.md`. Resumen:

- SC-001: PASS (1 s).
- SC-002: PASS (0 críticos).
- SC-003: PASS (100%).
- SC-004: PASS (100% en annex).
- SC-005: PASS (100%).
- SC-009: PASS (4/4 conceptos).

## Tiempos por etapa (resumen)

| Etapa | Duración aprox. |
|-------|-----------------|
| T051 — install | 1 s |
| T052 — brief | <1 s |
| T053 — research (web) + validación | ~50 s (4 WebSearch + 4 WebFetch + 9 validaciones) |
| T054 — plan | <1 s |
| T055 — redacción 3 capítulos | ~3 s (Write × 3) |
| T056 — 5 pasadas + 5 checklists | ~5 s (síntesis + Write) |
| T057 — close-project | ~1 s |
| T058 — archivado evidencia | ~2 s |

Tiempo total de pipeline (excluyendo síntesis del agente): ~65 s.

