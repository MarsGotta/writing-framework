# Contributing — Write.OnMars

Audiencia: personas que quieran proponer una nueva skill, certificar un MCP
contra el contrato de citación, contribuir a `resources/` o enmendar la
constitución. Esta guía complementa
`docs/maintenance/skill-update-procedure.md` y
`docs/maintenance/constitution-update-procedure.md`.

## Reglas generales

- **Idioma**: español. Excepciones (siglas, términos técnicos) declaradas en
  el glosario o front-matter.
- **Sin emojis** en archivos canónicos. Constitución § I.
- **Smoke tests verdes** antes de proponer un PR.
- **Sync impact report** cuando el cambio afecte plantillas Spec Kit o la
  constitución.

## Cómo proponer una nueva skill

1. **Justificar la necesidad**: documentar en una issue qué falta o qué
   skill existente no cubre el caso. Si la skill nueva sustituye o
   solapa a una existente, declarar la migración.
2. **Crear el directorio** `.claude/skills/<nombre>/` con dos archivos
   mínimos:
   - `SKILL.md` con front-matter YAML (`name`, `description`,
     `allowed-tools`) y cuerpo siguiendo el patrón de
     `writeonmars-install/SKILL.md`: cuándo dispararse, qué hace, inputs,
     outputs, procedimiento numerado, errores comunes, FR cubierta.
   - `VERSION` con primera línea `vX.Y.Z` o `vX.Y.Z-suffix-fecha`.
3. **Añadir entrada en `docs/skill-catalog.md`**: nombre, qué envuelve,
   inputs, outputs, FR coverage. La tabla del catálogo es fuente de verdad
   para mantenedores y para portar a otros agentes.
4. **Documentar el principio que materializa**. Cada skill MUST mapear a un
   principio o regla de la constitución (FR-024). Si no mapea a ninguno,
   reabrir la justificación.
5. **Ajustar el instalador si la skill es bundled**: las skills bundled
   las copia `install/lib/copy-skills.sh` automáticamente cuando el nombre
   empieza por `writeonmars-` o coincide con la lista hardcoded
   (`marcela-prose`, `technical-guide-design`). Si la skill nueva no
   encaja en ese patrón, ampliar la lista del script.
6. **Smoke tests**: añadir o adaptar al menos un test bajo
   `tests/smoke/` que valide la activación de la skill end-to-end. PR sin
   test de invocación se rechaza.

## Cómo certificar un nuevo MCP para el contrato de citación

El contrato canónico vive en `contracts/citation-contract.md` § "Cómo
certificar". Resumen operativo:

1. **Construir un fixture mínimo**: tres CitationRecord representativos
   (uno `documentacion_oficial`, uno `web_publica`, uno `archivo_local`)
   serializados como JSON.
2. **Validar contra el schema**:

   ```bash
   ajv validate \
     --spec=draft2020 \
     -s contracts/citation-record.schema.json \
     -d <fixture>.json
   ```

3. **Documentar el motor** en `docs/compatibility-matrix.md` §
   "MCPs investigación compatibles": nombre, versión mínima, tipo de
   `motor`, ejemplo de `referencia` y notas operativas (tasa de fallo
   conocida, latencia, costo).
4. **Smoke test**: añadir un script bajo `tests/smoke/` que invoque al MCP
   nuevo y verifique que las citas que emite validan. Sin smoke test, el
   MCP queda como "compatible declarado, no certificado".

## Cómo contribuir a `resources/`

`resources/` aloja las fuentes documentales que sostienen las decisiones
normativas del framework (constitución § Trazabilidad documental).
Criterios:

- **Tipo de fuente admitido**: documentación oficial, manuales editoriales,
  papers académicos, material editorial propio (estándares Marcela).
- **Metadatos requeridos** en el front-matter o en una nota inicial:
  fecha de incorporación, autoría original, ruta de origen (URL o vault),
  licencia o permiso de uso, versión consultada.
- **Sin material confidencial**. `resources/` queda commiteado en el repo
  canónico; cualquier persona con acceso al repo lo lee.
- **Naming**: `<dominio-corto>-<tema>.md`. Ejemplos: `guia-IA-writing.md`,
  `manual-textos-especializados.md`.
- **Cross-link al uso**: si la fuente sostiene un principio o regla de la
  constitución, añadir una referencia explícita desde la constitución a la
  fuente en `resources/`.

## Cómo proponer una enmienda a la constitución

Sigue `docs/maintenance/constitution-update-procedure.md` paso a paso. Resumen:

1. Trigger documentado.
2. Rama dedicada con prefijo `constitution/`.
3. `/speckit-constitution` con la propuesta.
4. Sync impact report en la cabecera del archivo.
5. Plan de migración para guías ya publicadas si aplica.
6. Bump semver editorial (MAJOR/MINOR/PATCH) según las reglas de § Governance.
7. Commit `docs: amend constitution to vX.Y.Z (motivo)`.
8. Entrada en `CHANGELOG.md` § "Constitution".

## Política de PRs

- **Rama dedicada** con prefijo descriptivo:
  - `feat/` para nuevas skills, MCPs o features.
  - `fix/` para bug fixes en scripts.
  - `docs/` para cambios documentales puros.
  - `chore/` para bumps de versión y mantenimiento.
  - `constitution/` para enmiendas constitucionales.
- **Smoke tests verdes** localmente antes del PR. Si los tests requieren
  Python, ajv o herramientas adicionales, declararlas en el PR.
- **Sync impact report** cuando el cambio toque
  `.specify/templates/*.md` o `.specify/memory/constitution.md`.
- **Sin emojis** en archivos canónicos.
- **Una feature por PR**. Cambios mezclados (skill nueva + bump de
  constitución + bug fix) se separan en PRs distintos para revisión limpia.

## Referencias

- `.specify/memory/constitution.md` — fuente de verdad editorial.
- `docs/skill-catalog.md` — catálogo de skills bundled.
- `docs/maintenance/skill-update-procedure.md` — bumps y propagación.
- `docs/maintenance/constitution-update-procedure.md` — enmiendas
  constitucionales.
- `contracts/citation-contract.md` — § "Cómo certificar".
- `docs/compatibility-matrix.md` — MCPs y agentes soportados.
