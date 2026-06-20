<!-- SPECKIT START -->
**Foco actual**: el preset agente-agnóstico `writeonmars/`
**Preset**: writeonmars/preset.yml · **Contrato del agente**: writeonmars/AGENTS.md
**Constitution**: .specify/memory/constitution.md (v1.2.0)

Write.OnMars se distribuye y ejecuta como un preset de Spec Kit. La lógica vive en
comandos (`writeonmars/commands/speckit.*`) y las reglas en referencias
(`writeonmars/references/`: voz, didáctica, método), neutrales de modelo: lo corre
cualquier agente. Empieza por:

- writeonmars/AGENTS.md — contrato para ejecutar el pipeline con cualquier modelo.
- writeonmars/docs/ — tutorial, how-to, referencia, arquitectura.
- writeonmars/README.md — qué empaqueta el preset y cómo se instala.

Specs (referencia, NO activas):
- 001-framework-architecture — base del harness editorial (v1.0.0). Vive en `specs/001-framework-architecture/`.
- 002-wom-cli — **superseded**: el `wom` CLI se descartó; `scripts/status.py` y
  `scripts/close.py` cubren su función.
<!-- SPECKIT END -->
