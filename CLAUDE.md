<!-- SPECKIT START -->
**Foco actual**: el preset agente-agnóstico `writeonmars/`
**Preset**: writeonmars/preset.yml · **Contrato del agente**: writeonmars/AGENTS.md
**Constitution**: .specify/memory/constitution.md (v1.6.1)

Write.OnMars se distribuye y ejecuta como un preset de Spec Kit. La lógica vive en
comandos (`writeonmars/commands/speckit.*`) y las reglas en referencias
(`writeonmars/references/`: prosa, registros, voz, didáctica, método), neutrales de
modelo: lo corre cualquier agente. La prosa sigue una pirámide de tres capas:
prosa-base (`references/prosa`, cohesión y fluidez, siempre activa) → registro por
género (`references/registros/<slug>`, declarado en manifiesto y adendas;
disponible `tecnico-divulgativo`) → voz de la autora (`references/voz`). Empieza por:

- writeonmars/AGENTS.md: contrato para ejecutar el pipeline con cualquier modelo.
- writeonmars/docs/: tutorial, how-to, referencia, arquitectura.
- writeonmars/README.md: qué empaqueta el preset y cómo se instala.

**Fuente única de contratos**: `writeonmars/contracts/`. La raíz `contracts/`,
`specs/001-framework-architecture/contracts/` y los espejos de `docs/` son
punteros (desde 2026-07-04): no edites ahí. Las skills del método tampoco viven
en `.claude/skills/` ni `.agents/skills/` (copias retiradas 2026-07-09): la
fuente única es `writeonmars/references/`.

**Tests como gate**: `python3 -m pytest tests/unit` (unitarios de los scripts) y
`bash tests/smoke/run-all.sh` (factualidad + e2e de Vivarium y modo estudio).
Ambos deben quedar en verde tras tocar `writeonmars/scripts/` o contratos. CI
(`.github/workflows/ci.yml`) corre ambos más `cargo test` en cada push.

**Vivarium (producto)**: sus docs viven en `docs/` (índice en `docs/README.md`);
`docs/vivarium.md` es la fuente de verdad del producto.

**Ejecutor orquestado**: `vivarium/` (Rust + Tauri, backend primero; ver
`vivarium/README.md`; producto en `docs/vivarium.md`). Frontera dura: Vivarium
solo habla con el método vía archivos + scripts + comandos. `paperclip/` queda
**archivado** como ejecutor de referencia (2026-07-07); sus lecciones viven en
`paperclip/FLOW-CONTRACT.md` (§§ 0-2 = contrato agnóstico del ejecutor).
Scaffolding de una guía nueva en un comando: `tools/new-guide.sh`.

**Feature activa**: **006-pista-corta-editorial** (planificada 2026-07-10).
Plan: `specs/006-pista-corta-editorial/plan.md` · Decisiones: `research.md`
(R1-R10) · Contratos: `contracts/{manifest-v1.4.0-delta,track-cli,ceremonia-corta}.md`
· Validación: `quickstart.md`. Siguiente paso: `/speckit-tasks`.
La implementación la hará **un agente distinto** del que redactó spec y plan.

Otros próximos pasos (ver ROADMAP.md): validación BYOM del modo estudio con
agentes reales (pendiente), biblia narrativa en `roots/` + ejes de continuidad
(candidata a spec 007, ver `docs/inspiracion-bookwright-profundizada.md`),
interfaz Tauri sobre `vivarium-core`.

Specs (referencia, NO activas):
- 001-framework-architecture: base del harness editorial (v1.0.0). Vive en `specs/001-framework-architecture/`.
- 002-wom-cli, **superseded**: el `wom` CLI se descartó; `scripts/status.py` y
  `scripts/close.py` cubren su función.
- 003-atribucion-factualidad: **integrada y validada e2e** (claims.md, índice de
  factualidad, gate g4); el directorio queda como referencia de diseño.
- 004-vivarium-core: **integrada y validada con agentes reales** (2026-07-08) —
  núcleo headless de Vivarium (`vivarium new|status|check|step|run|mode set`).
  Evidencia BYOM: `tests/editorial-pilot/evidence/2026-07-08-vivarium-byom/`.
  Gate extra al tocar `vivarium/`: `cd vivarium && cargo test --workspace`.
- 005-modo-estudio-pipeline: **integrada** (2026-07-09) — pipeline del modo
  estudio en el preset (`dispose.py`, `authorship.py`, huellas, checkpoints
  write/dispose). Revisada (8 ángulos, 10 correcciones). Validación BYOM con
  agentes reales aún pendiente.
- 006-pista-corta-editorial: **planificada** (2026-07-10) — ceremonia adaptativa
  para piezas únicas (`track: corta`: temario degenerado, pasada combinada
  1·2·3·5 + precisión, escalado sin tirar trabajo vía `scripts/track.py`).
  Fundamento: docs/comparativa-bmad.md. spec → clarify → **plan** hechos;
  pendiente: tasks → implement. Enmienda la constitución a v1.7.0 (§ "Pistas
  de ceremonia") y el manifest-schema a v1.4.0 (`track`, `track_history`).
<!-- SPECKIT END -->
