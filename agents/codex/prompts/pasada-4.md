---
prompt-version: 0.1.0-scaffold
applies-to: writeonmars-pasada-4 (codex)
last-reviewed: 2026-05-06
---

# Prompt — Pasada 4 precisión (Codex, scaffolding)

TODO: portar el prompt canónico de
`agents/claude/prompts/pasada-4.md` a la sintaxis y convenciones de Codex.

Pasada 4 verifica afirmaciones contra `CitationRecord` declarados en
`research.md`. Firma humana obligatoria por defecto. El prompt portado MUST
seguir el contrato de citación
(`contracts/citation-record.schema.json`) y emitir output en formato
`pass-output-schema.md` v1.0.
