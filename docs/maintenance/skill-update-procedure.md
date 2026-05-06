# Procedimiento de actualización de una skill bundled

Audiencia: persona mantenedora del framework Write.OnMars. Cubre el ciclo
"detectar bump → propagar al canónico → validar → release". Complementa
`docs/maintenance/sync-from-vault.md` y se ejecuta antes de que cualquier
proyecto editorial corra `writeonmars-update`.

## Cuándo aplicar este procedimiento

Aplica cuando se necesita bumpear la versión de una skill bundled
(`marcela-prose`, `technical-guide-design`, `writeonmars-*`) por alguna de
estas causas:

- Cambio sustantivo en la fuente externa (vault Obsidian para
  `marcela-prose` y `technical-guide-design`; este mismo repo para
  `writeonmars-*`).
- Refinamiento de un anti-pattern, regla microestilística o checklist
  derivado de feedback recurrente en pilotos editoriales.
- Adopción de una nueva regla de la constitución que toca una pasada.
- Bug fix puro (corrección de una instrucción ambigua, fallo de plantilla,
  etc.).

## Pasos

1. **Detectar bump necesario.** Documentar en una issue o nota interna la
   causa: cambio en origen externo, hallazgo recurrente del piloto,
   actualización de la constitución, bug.
2. **Sync del origen al repo canónico.** Para `marcela-prose` y
   `technical-guide-design`, seguir `docs/maintenance/sync-from-vault.md` y
   registrar en ese mismo archivo la fecha y el hash importado. Para
   `writeonmars-*`, editar directamente el `SKILL.md` en este repo.
3. **Bump VERSION según semver.** Tocar el archivo
   `.claude/skills/<skill>/VERSION`. Reglas:
   - **MAJOR (X.0.0)**: cambia el contrato de entrada/salida o se elimina
     una sección obligatoria. Rompe compatibilidad con prompts canónicos y
     plantillas Spec Kit.
   - **MINOR (0.Y.0)**: nueva sección, nuevo anti-pattern declarado, nuevo
     ejemplo canónico, expansión de un checklist. No rompe contrato.
   - **PATCH (0.0.Z)**: typo, aclaración, refraseo neutro semánticamente.
4. **Actualizar `docs/compatibility-matrix.md` si aplica.** Si la skill
   declara una nueva dependencia (MCP, agente o librería) o cambia un
   contrato de citación, registrar la nueva entrada en la matriz.
5. **Correr smoke tests.** Ejecutar `tests/smoke/run-all.sh` (US1) y
   `tests/smoke/update-skill-on-installed-project.sh` (US4). Ambos deben
   terminar verdes antes de seguir.
6. **Commit dedicado.** Mensaje canónico:
   `chore: bump <skill> to vX.Y.Z (<motivo corto>)`. Ejemplo:
   `chore: bump writeonmars-pasada-1 to v0.2.0 (worked-example checklist)`.
7. **(Opcional) Etiquetar release del framework.** Cuando un conjunto de
   bumps tenga sentido como release del framework (varias skills tocadas,
   nueva versión de la constitución), correr el procedimiento de release y
   etiquetar `vX.Y.Z`.
8. **Notificar a proyectos instalados.** El bump no es destructivo: cada
   proyecto editorial decide cuándo correr `writeonmars-update`. Documentar
   el bump en `CHANGELOG.md` para que las personas operadoras lo descubran.

## Performance

SC-008 exige que un bump de skill se propague a un proyecto instalado en
menos de **15 minutos**, conservando la configuración local del manifiesto.

| Métrica | Resultado | Target SC-008 | Estado |
|---------|-----------|---------------|--------|
| Tiempo total medido por `tests/smoke/update-skill-on-installed-project.sh` (precondición + bump + writeonmars-update + asserts) | 2 s en macOS 15 (Darwin 25.2.0) | <900 s | PASS |
| Configuración local preservada | `language_primary` custom y operador adicional sobreviven al update | Manifest field preservation 100% | PASS |
| Manifest re-validado contra `contracts/manifest-schema.json` | Validación verde tras el bump | Validación verde obligatoria | PASS |

El smoke test corre íntegramente en 2 s sobre macOS 15 (Darwin 25.2.0) con
Bash 5, Git ≥ 2.30 y `jq`. El target SC-008 se sostiene con margen amplio:
incluso sumando el cuello de botella humano (revisar el diff antes de
confirmar, 2-3 minutos en escenarios típicos), el procedimiento queda muy
por debajo de los 15 minutos.

Resultado SC-008: **PASS** (resultado de T071 / T072).

## Errores comunes

- **Bump aplicado pero el manifest no valida.** Suele indicar que se editó
  manualmente la skill sin actualizar `VERSION`, o que el VERSION no respeta
  semver. Re-ejecuta el bump tras corregir.
- **`writeonmars-update` borra una customización del manifest.** No debería
  pasar; si pasa, restaurar el backup `.bak` y abrir issue. La skill respeta
  `signing_matrix`, `human_operators[]`, `language_primary`, `project_type`,
  `memory_external`, `writeonmars_research_module` y `research_mode`.
- **Conflicto entre versión canónica y versión local del proyecto.** Si el
  proyecto declara una versión más reciente que la canónica
  (`local_ahead_of_canonical`), revisar si la persona operadora editó la
  skill localmente. Reconciliar antes de propagar más bumps.

## Referencias

- `.claude/skills/writeonmars-update/SKILL.md` — skill que aplica el bump
  en el lado del proyecto editorial.
- `docs/maintenance/sync-from-vault.md` — origen externo de
  `marcela-prose` y `technical-guide-design`.
- `tests/smoke/update-skill-on-installed-project.sh` — validación
  automatizada de SC-008.
- Constitución § Governance — política semver editorial general.
