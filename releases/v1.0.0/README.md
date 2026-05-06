# Release v1.0.0 (pendiente de tag)

Primera release del harness Write.OnMars. Esta carpeta archiva el material
inmutable de la release: snapshot de la constitución bajo la que se firmó y
hashes de las skills bundled. El tag `v1.0.0` lo aplica la persona
mantenedora manualmente; esta carpeta queda preparada antes del tag.

## Notas de release

Write.OnMars v1.0.0 materializa los cinco principios de la constitución
v1.1.0 en una pipeline ejecutable, agnóstica de agente, validada con dos
pilotos editoriales (3 capítulos seriales + 4 capítulos paralelo vs serial)
que demuestran SC-001 a SC-009.

Componentes incluidos:

- 17 skills bundled (`marcela-prose`, `technical-guide-design`, 15 skills
  `writeonmars-*`).
- 4 contratos publicados (`citation-contract.md` v1.0,
  `citation-record.schema.json`, `manifest-schema.json`,
  `pass-output-schema.md`).
- Instalador shell (`install/install.sh` + `install/lib/*.sh`).
- Plantillas Spec Kit adaptadas (`spec-template.md`, `plan-template.md`,
  `tasks-template.md`, `checklist-template.md`).
- 6 prompts canónicos por agente (`agents/claude/prompts/`).
- Scaffolding Codex (`agents/codex/`).
- MCP de referencia (`mcp/writeonmars-research/`).
- 4 smoke tests (US1 install + US4 update + run-all aggregator).
- 2 pilotos editoriales archivados con findings, manifest, traza y
  validación.
- Documentación operativa: `docs/installation.md`,
  `docs/editorial-cycle.md`, `docs/skill-catalog.md`,
  `docs/parallel-execution.md`, `docs/portability-validation.md`,
  `docs/contributing.md`, `docs/memory-external.md`,
  `docs/maintenance/skill-update-procedure.md`,
  `docs/maintenance/constitution-update-procedure.md`.

## Hashes de skills bundled

Hash SHA-256 del archivo `SKILL.md` de cada skill bundled al momento de la
release. Permite verificar integridad post-tag.

| Skill | Versión | SHA-256 SKILL.md |
|-------|---------|------------------|
| marcela-prose | v0.1.0-import-2026-05-06 | 52a4c11f2f20f5058f3d8e036315e04d1450278dca466aef1523c0e7fd253561 |
| technical-guide-design | v0.1.0-import-2026-05-06 | 2387cabf94110651a3eb5570cfaaf16b06f82f05c1f24a0d0d64f82a7a9454e8 |
| writeonmars-brief | v0.1.0-mvp-2026-05-06 | 6c4b9df7e8fc4280b1dbd03fbe0cdc98a771a68b33b68b117f1fe9e761188b49 |
| writeonmars-close-project | v0.1.0-mvp-2026-05-06 | 31669d12f9784dcf9a902591661cfd0bf95840e81322a529807cc70023f66f67 |
| writeonmars-contraste | v0.2.0-mvp-2026-05-06 | e8edfe977eb89005e886570dd73bb093d2db01e9ce3881d8faee29b274d1b183 |
| writeonmars-descripciones | v0.1.0-mvp-2026-05-06 | d0a9bf2edb73408b92593b3c45cc0d9f7cad8ea934728eee6be712bf6e66dc10 |
| writeonmars-glossary | v0.2.0-mvp-2026-05-06 | cf7552354f4ba814b61062c429f1b9e40ac22d89ac220a61fe4ee465d10d7cec |
| writeonmars-install | v0.1.0-mvp | 08d5775c779720627eed083bedcd7b9bd9f81b12d1b072f40ec4f3d3695ac3ce |
| writeonmars-pasada-1 | v0.1.0-mvp-2026-05-06 | 14c806b59d8ed74023691440b122a7d2637e688eb49e6305ff65dc0b59cabba7 |
| writeonmars-pasada-2 | v0.1.0-mvp-2026-05-06 | c4e70ceab3bf9a6a80aca74124edae3453bf8a82543b9b8d73d6255e52f859f9 |
| writeonmars-pasada-3 | v0.1.0-mvp-2026-05-06 | 20e213e82f9e6e3c6acf557bf2b6ba2fab80fc9033b9a9571ed23f28dc070dff |
| writeonmars-pasada-4 | v0.1.0-mvp-2026-05-06 | 52a8651c8be2d9729676d52b2ec7fb674ed740f417b25b9e56c89d8f16f96492 |
| writeonmars-pasada-5 | v0.1.0-mvp-2026-05-06 | 4061aef29c02b2a9ed31f5d866ee64e77936ca471cbb659724a4a116032d7d84 |
| writeonmars-redaccion | v0.2.0-mvp-2026-05-06 | 4cbaff8c49de2c8e47ce0c918d43359078515906282d708b9d85d65392ba5314 |
| writeonmars-research | v0.1.0-mvp-2026-05-06 | 33d0f335f4652a8cb1eda5aeb7f7e7ddb3c9530dd634564f7afba6dc1486997e |
| writeonmars-temario | v0.1.0-mvp-2026-05-06 | f2da5f727c803aafaaae7c143febf03d315937a0fbbc7cbc1a23b1d156e59a61 |
| writeonmars-update | v0.1.0-mvp-2026-05-06 | c415a63e0f989bf364dd41ae46127411464822621e3e40662c4fcca61523b72b |

Reproducir los hashes localmente:

```bash
shasum -a 256 .claude/skills/<skill>/SKILL.md
```

## Constitución bajo la que se firma esta release

`constitution-v1.1.0.md` en este mismo directorio. Snapshot inmutable de
`.specify/memory/constitution.md` al momento de la release. Las enmiendas
posteriores al tag v1.0.0 generan una release nueva, no modifican este
archivo.

## Referencia al CHANGELOG

El detalle por user story de qué entra en esta release vive en
`/CHANGELOG.md`. La sección `[1.0.0] - 2026-05-06 (pendiente de tag)`
describe los cambios desglosados por US1, US2, US3, US4 y Polish, además
de los fixes documentados durante la implementación.

## Reproducción

Para verificar que un clone del repo coincide con esta release:

1. Comparar `.specify/memory/constitution.md` con `constitution-v1.1.0.md`.
2. Recalcular los hashes SHA-256 de cada skill y contrastar con la tabla
   anterior.
3. Correr `tests/smoke/run-all.sh` y
   `tests/smoke/update-skill-on-installed-project.sh`. Ambos deben pasar.
4. Verificar que `mcp/writeonmars-research/pyproject.toml` declara version
   `0.1.0`.
