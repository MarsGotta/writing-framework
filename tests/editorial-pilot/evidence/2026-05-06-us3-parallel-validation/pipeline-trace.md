# Pipeline Trace — Experimento US3 (alto nivel)

Cronograma del experimento Phase 5 / US3. Para detalle por modo ver
`baseline-serial/pipeline-trace-serial.md` y
`parallel/pipeline-trace-parallel.md`.

- **Fecha**: 2026-05-06.
- **Operador**: marcela / marcelagotta@gmail.com.
- **Cobertura**: T062–T067 + T064a.

## Fases del experimento

| Fase | Tarea | Acción | Tiempo aprox. |
|------|-------|--------|---------------|
| 1 | T062 | Editar `writeonmars-redaccion` — añadir `--parallel N`. Bump v0.2.0-mvp-2026-05-06. | 1 min |
| 2 | T063 | Editar `writeonmars-contraste` — añadir dispatch paralelo por capítulo. Bump v0.2.0-mvp-2026-05-06. | 1 min |
| 3 | T064 | Editar `writeonmars-glossary` — añadir ingestión paralela y resolución de colisiones. Bump v0.2.0-mvp-2026-05-06. | 1 min |
| 4 | T064a | Setup sandbox serial; producir spec + research + plan; redactar 4 capítulos en serie. | 2 s install + 83 s redacción wall-clock |
| 5 | T065 | Setup sandbox paralelo; copiar spec/research/plan; redactar 4 capítulos en paralelo. | 2 s install + 62 s redacción wall-clock |
| 6 | T066 | Validar SC-006 — calcular reducción y equivalencia. | <1 min |
| 7 | T067 | Crear `docs/parallel-execution.md`. | 2 min |
| 8 | T058-equivalente | Archivar metadatos en evidencia (esta carpeta). | 1 min |

## Sandboxes (efímeros, /tmp/)

| Sandbox | Path | Contenido |
|---------|------|-----------|
| Serial | `/tmp/writeonmars-pilot-2026-05-06-us3-baseline-serial/` | spec, research, plan, 4 chapters serial |
| Paralelo | `/tmp/writeonmars-pilot-2026-05-06-us3-parallel/` | spec/research/plan copiados, 4 chapters paralelo |

Ningún sandbox cruza al canónico; solo los metadatos de esta carpeta.

## Resultado consolidado

- **SC-006**: PASS — 42.9% reducción modelada, equivalencia ±10%.
- **SC-002**: PASS — 0 críticos en ambos modos.
- **SC-004**: PASS — 100% cobertura glosario, 0 colisiones críticas.

## Métricas clave

| Métrica | Serial | Paralelo |
|---------|--------|----------|
| `time_total_seconds_real` (wall-clock orquestador) | 83 | 62 |
| `time_total_seconds_modeled` (sub-agente real `[SIMULATED]`) | 1680 (28 min) | 960 (16 min) |
| `criticos_total` | 0 | 0 |
| `medios_total` | 6 | 6 |
| `bajos_total` | 31 | 32 |
| `cobertura_glosario_pct` | 100 | 100 |
| `colisiones_glosario_criticas` | 0 | 0 |

## Aserciones globales

- `[OK]` Mismo brief, mismo manifiesto, mismo plan en ambos pilotos.
- `[OK]` Solo cambia la topología de redacción (serial vs paralelo).
- `[OK]` SC-006 PASS metodológico con modelado declarado.
- `[OK]` 0 archivos editoriales (chapters/, glosario, findings.md
  completo) en el repo canónico.
- `[OK]` Los tres skills (`writeonmars-redaccion`, `-contraste`,
  `-glossary`) bumped a `v0.2.0-mvp-2026-05-06`.
