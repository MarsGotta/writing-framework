# Procedimiento de enmienda de la constitución

Audiencia: persona mantenedora del framework Write.OnMars. Cubre el ciclo
"detectar discrepancia → enmendar el núcleo → propagar → comunicar". Complementa
la sección **Governance § Procedimiento de enmienda** de
`writeonmars/memory/constitution.md`.

## Núcleo vs adendas: qué se enmienda aquí

La constitución tiene dos capas:

- **Núcleo** (`writeonmars/memory/constitution.md`, versionado): las reglas
  universales. **Esto es lo que se enmienda con este procedimiento.**
- **Adendas del proyecto** (por guía, vía `/speckit-constitution`): lo normativo que
  varía por guía (tono, terminología, relajaciones por sector). No se enmienda aquí;
  se ajusta por proyecto.

Si lo que cambia es un default por dominio (p. ej. qué anglicismos admite
tecnología), no toques el núcleo: edita la **base de sector**
(`writeonmars/references/sectores/<slug>.md`).

## Cuándo aplicar este procedimiento

- **Discrepancia recurrente** entre el núcleo y las guías reales (un anti-pattern
  detectado en revisión que no está codificado, un estándar que todas las guías
  acaban relajando).
- **Nuevo estándar editorial** validado en uno o varios pilotos.
- **Refinamiento normativo** de una regla existente (aclaración o expansión que
  cambia el comportamiento esperable).
- **Cambio de arquitectura** del framework (nueva integración, nueva fuente
  obligatoria, nueva política de memoria).

## Pasos

1. **Trigger documentado.** Antes de tocar el núcleo, documenta la causa: la
   discrepancia, la evidencia que la sostiene, el alcance estimado.
2. **Rama dedicada.** Prefijo obligatorio `constitution/` (p. ej.
   `constitution/v1-3-0-fuentes-por-capitulo`).
3. **Ejecuta `/speckit-constitution`** (o edita el núcleo a mano para mantenedores):
   redacta la propuesta y genera el **sync impact report** en la cabecera del propio
   archivo de la constitución.
4. **Sync impact report.** Identifica qué plantillas de `writeonmars/templates/*.md`
   quedan afectadas y márcalas. Plantillas a revisar:
   - `spec-template.md` (brief de 8 campos descriptivos, "Trayectos de lector").
   - `plan-template.md` ("Temario", "Descripciones encadenadas", Constitution Check).
   - `tasks-template.md` (fases editoriales y software).
   - `checklist-template.md` (checklist por pasada).
   - `adendas-template.md` (capa por guía) si la enmienda toca lo que va en adendas.
5. **Bump de versión semver editorial** (reglas en § Governance):
   - **MAJOR**: eliminación o redefinición incompatible; invalida guías publicadas.
   - **MINOR**: nuevo principio, nuevo estándar o expansión material de una regla.
   - **PATCH**: aclaraciones y refinamientos no semánticos.
   Actualiza la línea `**Version**` al final del núcleo, `CONSTITUTION_VERSION` en
   `writeonmars/scripts/bootstrap.py`, y las menciones de versión en docs/plantillas.
6. **Commit dedicado.** Mensaje canónico:
   `docs: amend constitution to vX.Y.Z (<motivo>)`.
7. **Propagación a proyectos instalados.** El núcleo se rige por versión:
   - En cada guía instalada, `python3 .specify/presets/writeonmars/scripts/bootstrap.py --force`
     **re-sella el núcleo** desde el preset **preservando las adendas del proyecto**
     (la frontera es el centinela `<!-- WRITEONMARS:ADENDAS -->`). No hay que
     parchear copias a mano.
   - Las guías ya cerradas bajo una versión previa se consideran firmes salvo que se
     decida re-revisar explícitamente.
8. **Comunica el cambio.** Añade entrada al `CHANGELOG.md` describiendo el bump y
   enlazando el sync impact report.

## Errores comunes

- **Relajar un default de sector en el núcleo.** Si solo cambia para un dominio, va a
  la base de sector, no al núcleo.
- **Plantillas no actualizadas tras una MINOR.** El sync impact report queda
  incompleto si marcas una plantilla como `updated` sin tocarla.
- **`--force` sin centinela de adendas.** Si una guía tiene adendas pero falta el
  centinela `<!-- WRITEONMARS:ADENDAS -->`, el re-sellado no puede preservarlas:
  verifica que la sección de adendas empieza por el centinela.
- **Rama sin prefijo `constitution/`.** Es la única señal de que la rama toca el
  núcleo; recházala en revisión si falta.

## Referencias

- `writeonmars/memory/constitution.md` § Governance — fuente normativa.
- `writeonmars/scripts/bootstrap.py` — copia y re-sellado del núcleo.
- `writeonmars/references/sectores/` — defaults por sector (lo que NO va al núcleo).
- `CHANGELOG.md` — registro histórico de enmiendas.
