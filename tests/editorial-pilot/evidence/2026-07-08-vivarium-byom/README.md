# Validación BYOM real — T022 / FR-007 (2026-07-08)

Guía corta real ejecutada de punta a punta por `vivarium run` con **dos
agentes reales cruzados**: `claude` (redactora) y `codex` (editora de mesa y
documentalista). Proyecto: `~/Projects/vivarium-t022-guia` — «Guía express de
Markdown para escritores», 2 capítulos, sector `tecnologia`, `mode:
produccion`. Sustituye a `2026-07-07-vivarium-byom/BLOCKED.md` (aquel entorno
no tenía toolchain Rust; este sí).

## Recorrido observado

1. `vivarium new` → proyecto con preset, manifest (`mode: produccion`,
   `sector: tecnologia`), `roots/`, `decisions.jsonl`, commit base.
2. `vivarium check` → exit 0 con la config BYOM real (`config.toml` adjunto).
3. `vivarium run` → **exit 10** en checkpoint 1 (falta brief). La operadora
   firmó `specs/001-markdown-express/spec.md`.
4. `vivarium run` → research (codex) → plan (claude) → por capítulo:
   implement (claude) + pasadas 1-3 (codex/mesa) + pasada 4 (codex/
   documentalista) + ciclos de revise reales (claude) → pasada 5 global →
   intro → export (sidecar, pandoc + Chromium vía `WOM_CHROME`) →
   **exit 10** en checkpoint 2 (falta feedback).
5. Feedback firmado (`specs/001-markdown-express/feedback.md`) →
   `vivarium run` → close.py → **exit 0** («proyecto cerrado»).
6. Re-ejecución de `vivarium run` → **exit 0** con «proyecto ya cerrado
   (close.py OK)» y **cero despachos nuevos** (idempotencia del cierre).

## Incidencias reales cubiertas por el contrato

- **Interrupción a mitad de despacho** (timeout del harness durante
  `revise` cap. 2): al relanzar, la reconciliación marcó el in-flight como
  `failed` («interrumpido sin efecto en disco; re-despacho seguro») y lo
  re-despachó con éxito — FR-006 validado con agentes reales.
- **Fallos de entorno en export/close** (faltaban `pandoc` y Chrome):
  exit 12 en cada intento, estado en disco intacto, reintento seguro tras
  instalar la dependencia. Las 3 tuplas dispatch/failed de `export` y
  `close` en `decisions.jsonl` son ese rastro honesto.

## Matriz de relevos (26 despachos)

| Paso | Rol | Agente | Nº |
|------|-----|--------|----|
| research | documentalista | codex | 1 |
| plan, implement, revise, intro | redactora | claude | 1+2+6+1 |
| review-1..3, review-5 | editora_mesa | codex | 6+1 |
| review-4 | documentalista | codex | 2 |
| export, close | sidecar | scripts Python | 3+3 |

Escribe-uno-revisa-otro y voz ≠ precisión respetados en todos los relevos:
ningún capítulo fue revisado por el agente que lo redactó.

## Archivos

- `config.toml` — config BYOM usada (sin credenciales; los agentes usan la
  sesión local de cada CLI).
- `decisions.jsonl` — traza completa: 1 checkpoint specify, 26 despachos con
  sus disposiciones (19 ok, 7 revise, 5 failed reconciliados/reintentados).
- `status-final.json` — estado final: `all_chapters_approved: true`,
  `closeable: true`.
