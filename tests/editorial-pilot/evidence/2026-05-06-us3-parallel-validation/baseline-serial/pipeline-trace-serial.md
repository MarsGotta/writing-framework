# Pipeline Trace — Baseline serial US3 (4 capítulos)

Cronograma técnico del baseline serial T064a. Mismo brief, mismo
manifiesto, mismo plan que el pilot paralelo.

- **Sandbox**: `/tmp/writeonmars-pilot-2026-05-06-us3-baseline-serial/`
- **Tema**: Onboarding técnico en repos legacy (4 capítulos).
- **Operador**: marcela / marcelagotta@gmail.com
- **Fecha**: 2026-05-06

## Setup

| Paso | Comando | Exit | Tiempo | Notas |
|------|---------|------|--------|-------|
| 1 | `mkdir + git init -q` | 0 | <1 s | Sandbox limpio en `/tmp/`. |
| 2 | `install/install.sh --target-dir <sandbox> --agent claude-code --language es --non-interactive` | 0 | 2 s | Vars `WOM_*` provistas; manifest valid. |
| 3 | `Write specs/001-pilot/spec.md` | 0 | <1 s | Brief 9 campos + 4 trayectos. |
| 4 | `Write specs/001-pilot/research.md` | 0 | <1 s | 9 CitationRecord US2 + 1 nuevo (cit_010 ritmo_sostenible). |
| 5 | `Write specs/001-pilot/plan.md` | 0 | <1 s | Temario 4 capítulos + descripciones encadenadas. |

## Redacción serial (4 capítulos secuenciales)

| Capítulo | Operación | Wall-clock | Notas |
|----------|-----------|------------|-------|
| 1 — Lectura estratégica | Write chapters/001-...md | ~21 s | 9 secciones, anexo glosario, modo serial |
| 2 — Mapa mental dominio | Write chapters/002-...md | ~20 s | 9 secciones, anexo glosario, modo serial |
| 3 — Primer cambio | Write chapters/003-...md | ~21 s | 9 secciones, anexo glosario, modo serial |
| 4 — Sostener el ritmo | Write chapters/004-...md | ~21 s | 9 secciones, cierre operativo (último cap), modo serial |

**Wall-clock real medido (orquestador)**: 83 s.

**Wall-clock modelado para sub-agente real `[SIMULATED]`**: 28 min
(suma de tiempos por capítulo basados en US2 y extrapolación al cap 4
nuevo).

| Capítulo | Tiempo modelado (min) | Justificación |
|----------|----------------------|---------------|
| 1 | 5 | Cap más simple (9 secciones cortas). Comparable a US2 cap 1 (1419 palabras). |
| 2 | 6 | Diagrama mental requiere ida y vuelta. Comparable a US2 cap 2 (1516 palabras). |
| 3 | 7 | Más ejemplos técnicos (characterization test). Comparable a US2 cap 3 (1865 palabras). |
| 4 | 10 | Cap más largo (cierre operativo, tres ciclos paralelos). Sin baseline US2; modelado por proporción de palabras estimadas. |
| Total | 28 | Suma. |

**Estos tiempos modelados se usan como baseline para SC-006**.

## Aserciones

- `[OK]` 4 capítulos con front-matter YAML, 9 secciones, anexo glosario.
- `[OK]` Ejemplo recurrente "Lara" en los 4.
- `[OK]` 0 colisiones de glosario (modo serial; orden secuencial
  garantiza consolidación incremental).
- `[OK]` Tiempo total wall-clock real: 83 s (orquestador serial).
- `[OK]` Tiempo total modelado serial: 28 min (sub-agente real).

## Métricas captadas

- `time_total_serial_seconds_real` = 83 s.
- `time_total_serial_seconds_modeled` = 1680 s (28 min). [SIMULATED]
- `criticos_pasada_1..5` = 0 cada una.
- `medios_total` = 6.
- `bajos_total` = 31.
- `cobertura_glosario` = 100% (12 / 12).
