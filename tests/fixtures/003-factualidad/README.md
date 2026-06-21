# Fixtures — 003 atribución por afirmación / factualidad

Insumos deterministas para `tests/smoke/test-factuality.sh`. No es un proyecto
editorial real: está calibrado para ejercitar `status.py` en aislamiento.

## `project/`

Proyecto mínimo (manifest baseline **sin** `quality_gates`), con:

- `chapters/01..03` — tres capítulos triviales con su `## Fuentes`.
- `specs/001-fact/plan.md` — temario de 3 filas (`chapters_expected = 3`).
- `specs/001-fact/claims.md` — capítulos 1 y 2 medidos; **capítulo 3 sin sección**
  (caso "no medido"/`unmeasured`).
  - cap 1 y 2: 4 afirmaciones `soportado` (`apoya`) + 1 `dato_duro` cuya única cita
    solo `menciona` → `sin_fuente`. Índice por capítulo 4/5 = 0.8; **global 8/10 = 0.8**.
  - Esa afirmación `dato_duro`-`menciona` **tiene cita** pero no la sostiene: por eso
    el índice (0.8) baja respecto al ingenuo `tiene_cita / total` (1.0) — SC-006.
- `specs/001-fact/findings.md` — pasadas 1·4 por capítulo, autónomas y **sin
  hallazgos abiertos a propósito**.

> Inconsistencia deliberada: en una guía real, cada `sin_fuente`/`contradicho` de
> `claims.md` aparecería como hallazgo crítico/medio en `findings.md` (FR-009). El
> fixture la omite para (a) aislar el gate g4 del gate de críticos g1 y (b) ejercitar
> el `warning` de inconsistencia (g4 rojo con `revise_pending == 0`).

## `manifests/`

Variantes que el smoke intercambia como `.writeonmars-manifest.json`:

- `blocking.json` — `quality_gates.factuality_min = 0.9`, modo `blocking`.
- `advisory.json` — `0.9`, modo `advisory` (informa, no bloquea).
- `pass.json` — `0.7`, modo `blocking` (el 0.8 lo supera).
