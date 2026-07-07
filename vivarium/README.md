# Vivarium — ejecutor orquestado del método (app local-first)

Vivarium es la aplicación de escritura local-first donde un equipo editorial de
agentes trabaja para quien escribe. En este repo es, además, el **ejecutor
orquestado de referencia** del método Write.OnMars (constitución v1.6.0
§ Ejecutores del método): sustituye a Paperclip (`paperclip/`, archivado).

- **Producto (fuente de verdad)**: `docs/vivarium.md` — visión, modelo botánico
  (Zeed/Root/Tree/Branch/Leaf/Forest), los dos modos, mercado y roadmap.
- **Contrato de flujo que implementa**: `paperclip/FLOW-CONTRACT.md` §§ 0-2
  (ciclo por capítulo, estados derivados de archivos, etapas globales). La
  spec 004 lo promueve a contrato del ejecutor.
- **Método al que sirve**: el preset `writeonmars/` (comandos, scripts,
  referencias, contratos).

## La frontera dura (regla de este directorio)

Vivarium habla con el método **solo a través de archivos, scripts y comandos**
— el mismo contrato que cualquier agente:

- Lee el estado con `status.py --json` (`next_step`, `by_chapter`,
  `all_chapters_approved`); jamás computa estado editorial por su cuenta.
- La verdad vive en el repo del proyecto editorial (manifiesto, `specs/`,
  `chapters/`, `findings.md`, `claims.md`); Vivarium no guarda estado de
  negocio propio (constitución § Ejecutores del método).
- Ninguna lógica editorial (qué revisar, cuándo aprobar, cuándo cerrar) se
  implementa aquí; aquí viven la orquestación de relevos, la creación de
  proyectos y, después, la interfaz.

Si esa disciplina se mantiene, extraer `vivarium/` a su propio repositorio es
un movimiento de carpetas, no una refactorización.

## Layout previsto (lo materializa la spec 004; implementación: Codex)

```
vivarium/
  crates/
    vivarium-core/    # dominio: bootstrap de proyecto, runner por estados
    vivarium-cli/     # binario headless: valida el core sin UI
  app/                # shell Tauri (etapa posterior; solo llama a vivarium-core)
```

Stack fijado en `docs/vivarium.md` § 10: Rust + Tauri; git vía libgit2; agentes
vía MCP/CLIs (BYOM); scripts Python del preset como sidecar (no se portan).

## Estado

Pre-scaffolding (2026-07-07). Secuencia acordada: backend primero (bootstrap +
runner headless), editor visual después. La spec `specs/004-vivarium-core/`
define contrato del ejecutor, bootstrap de proyecto (repo + preset + manifest
con `mode` + `roots/` + `decisions.jsonl`) y runner.
