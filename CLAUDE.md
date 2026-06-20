<!-- SPECKIT START -->
**Foco actual**: el preset agente-agnóstico `writeonmars/`
**Preset**: writeonmars/preset.yml · **Contrato del agente**: writeonmars/AGENTS.md
**Constitution**: .specify/memory/constitution.md (v1.3.0)

Write.OnMars se distribuye y ejecuta como un preset de Spec Kit. La lógica vive en
comandos (`writeonmars/commands/speckit.*`) y las reglas en referencias
(`writeonmars/references/`: voz, didáctica, método), neutrales de modelo: lo corre
cualquier agente. Empieza por:

- writeonmars/AGENTS.md — contrato para ejecutar el pipeline con cualquier modelo.
- writeonmars/docs/ — tutorial, how-to, referencia, arquitectura.
- writeonmars/README.md — qué empaqueta el preset y cómo se instala.

**Capa de orquestación (opcional, por encima del preset)**: `paperclip/` materializa
el ejecutor orquestado sobre Paperclip — una Company "Write.OnMars" (la casa), cada
guía un Project, equipo de 4 roles editoriales (Editora jefa, Documentalista,
Redactora, Editora de mesa). Ver `paperclip/README.md`. Scaffolding de una guía nueva
en un comando: `tools/new-guide.sh`.

Specs (referencia, NO activas):
- 001-framework-architecture — base del harness editorial (v1.0.0). Vive en `specs/001-framework-architecture/`.
- 002-wom-cli — **superseded**: el `wom` CLI se descartó; `scripts/status.py` y
  `scripts/close.py` cubren su función.
<!-- SPECKIT END -->
