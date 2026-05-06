---
prompt-version: 0.1.0-scaffold
applies-to: writeonmars-redaccion (codex)
last-reviewed: 2026-05-06
---

# Prompt — Redacción de capítulo (Codex, scaffolding)

TODO: portar el prompt canónico de
`agents/claude/prompts/redaccion.md` a la sintaxis y convenciones de Codex.

Mientras el placeholder esté presente, Codex no puede ejecutar la skill
`writeonmars-redaccion`. La persona operadora debe completar este archivo o
mantener el agente prioritario en `claude-code` (default v1).

Consideraciones específicas a resolver al portar:

- ¿Cómo despacha Codex un sub-agente con contexto fresco equivalente al
  Agent tool de Claude Code? Documentar el mecanismo o la limitación.
- ¿Cómo consume Codex skills externas? ¿Tiene equivalente al
  descubrimiento por `description` triggers de `.claude/skills/`?
- ¿Cómo lee Codex el manifest `.writeonmars-manifest.json`? La spec del
  capítulo, el temario y las descripciones encadenadas deben llegar al
  sub-agente igual que en el adaptador Claude Code.
