# Codex adapter

Adaptador de Write.OnMars para [Codex](https://openai.com/codex/).
**Estado**: port parcial. Los prompts canónicos del adaptador Claude Code
(`agents/claude/prompts/`) se mantienen como fuente de verdad. `redaccion.md`
y `pasada-3.md` ya son adaptadores reales, alineados con la constitución
v1.5.0: aplican el contrato compartido del prompt canónico y definen solo lo
que difiere en Codex. Las pasadas 1, 2, 4 y 5 siguen siendo placeholders que
demuestran el agnosticismo declarado en FR-023 y FR-024.

## Qué falta para portar a Codex

Esta lista está pensada como checklist operativa para una persona
mantenedora que quiera completar el adaptador.

1. **Reproducir cada prompt canónico** de `agents/claude/prompts/*.md` en
   este directorio (`agents/codex/prompts/*.md`) traduciendo la sintaxis
   específica de Claude Code (Agent tool, `subagent_type`, formato de Skills)
   a la sintaxis o convenciones de Codex.
2. **Verificar que Codex expone un mecanismo equivalente** para sub-agentes
   con contexto fresco. Si no lo expone, documentar la limitación: las
   pasadas dejarían de poder ejecutarse en sub-agente y la persona operadora
   debería confirmar manualmente la ausencia de cross-contamination.
3. **Verificar que Codex respeta el manifiesto** en lectura: las skills
   `writeonmars-*` consultan `.writeonmars-manifest.json` (signing matrix,
   research mode, etc.). Si Codex no permite leer arbitrariamente el
   workspace del proyecto, declarar la fricción.
4. **Adaptar `install/install.sh`** para registrar el contexto del agente en
   `AGENTS.md` en lugar de `CLAUDE.md` cuando se pase `--agent codex`. El
   instalador ya reconoce el flag; solo falta el render exacto del bloque
   `<!-- WRITEONMARS START --> ... <!-- WRITEONMARS END -->`.
5. **Correr smoke tests adaptados** al agente: T024–T027 deberían poder
   ejecutarse contra Codex sin modificación, salvo el archivo de contexto
   (`AGENTS.md` en vez de `CLAUDE.md`).
6. **Pilotar 3 capítulos** sobre el mismo tema del piloto editorial Claude
   Code. Comparar:
   - Cobertura de glosario.
   - Hallazgos críticos por pasada.
   - Tiempo total.
   La equivalencia ±10% en cobertura y críticos demuestra portabilidad
   funcional (SC-007).

## Estructura del adaptador

```
agents/codex/
├── README.md            # este archivo
└── prompts/
    ├── redaccion.md           # adaptador (constitución v1.5.0)
    ├── pasada-1.md            # placeholder
    ├── pasada-2.md            # placeholder
    ├── pasada-3.md            # adaptador (constitución v1.5.0)
    ├── pasada-4.md            # placeholder
    └── pasada-5.md            # placeholder
```

Cada placeholder pendiente declara `prompt-version: 0.1.0-scaffold` en el
front-matter y el cuerpo es un TODO explícito que apunta al prompt canónico
correspondiente en `agents/claude/prompts/`. Los adaptadores completados
declaran `prompt-version: 1.0`, remiten al canónico como contrato compartido
y documentan las diferencias propias de Codex (sin sub-agentes, skills
resueltas como referencias por ruta, lectura del manifiesto).

## Referencias

- `agents/claude/prompts/` — prompts canónicos en sintaxis Claude Code.
- `docs/portability-validation.md` — checklist completa de portabilidad
  SC-007 y diferimiento de la validación end-to-end.
- Constitución § Arquitectura del framework — agnosticismo de agente
  (FR-023, FR-024).
