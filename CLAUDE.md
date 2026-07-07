<!-- SPECKIT START -->
**Foco actual**: el preset agente-agnóstico `writeonmars/`
**Preset**: writeonmars/preset.yml · **Contrato del agente**: writeonmars/AGENTS.md
**Constitution**: .specify/memory/constitution.md (v1.6.0)

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
punteros (desde 2026-07-04): no edites ahí.

**Tests como gate**: `python3 -m pytest tests/unit` (unitarios de los scripts) y
`bash tests/smoke/run-all.sh` (instalación + factualidad). Ambos deben quedar en
verde tras tocar `writeonmars/scripts/` o contratos.

**Vivarium (producto)**: sus docs viven en `docs/` (índice en `docs/README.md`);
`docs/vivarium.md` es la fuente de verdad del producto.

**Ejecutor orquestado**: `vivarium/` (Rust + Tauri, backend primero; ver
`vivarium/README.md`; producto en `docs/vivarium.md`). Frontera dura: Vivarium
solo habla con el método vía archivos + scripts + comandos. `paperclip/` queda
**archivado** como ejecutor de referencia (2026-07-07); sus lecciones viven en
`paperclip/FLOW-CONTRACT.md` (§§ 0-2 = contrato agnóstico del ejecutor).
Scaffolding de una guía nueva en un comando: `tools/new-guide.sh`.

**Feature activa**: 004-vivarium-core (rama `004-vivarium-core`) — núcleo
headless de Vivarium. Plan: `specs/004-vivarium-core/plan.md` (research,
data-model, contratos y quickstart en el mismo directorio). La implementación
la hará Codex: los artefactos son autocontenidos y agente-neutrales.

Specs (referencia, NO activas):
- 001-framework-architecture: base del harness editorial (v1.0.0). Vive en `specs/001-framework-architecture/`.
- 002-wom-cli, **superseded**: el `wom` CLI se descartó; `scripts/status.py` y
  `scripts/close.py` cubren su función.
- 003-atribucion-factualidad: **integrada y validada e2e** (claims.md, índice de
  factualidad, gate g4); el directorio queda como referencia de diseño.
<!-- SPECKIT END -->
