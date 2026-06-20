# Contributing — Write.OnMars

Audiencia: personas que quieran extender el método (un comando, una referencia, un
sector), certificar un MCP contra el contrato de citación, contribuir a `resources/`
o enmendar la constitución.

El método se distribuye como **preset de Spec Kit** (`writeonmars/`): la lógica vive
en **comandos** neutrales de modelo, las reglas en **referencias**, lo determinista
en **scripts**. No hay skills de un proveedor. Cualquier extensión sigue ese reparto.

## Reglas generales

- **Idioma**: español. Excepciones (siglas, términos técnicos) declaradas en el
  glosario o front-matter.
- **Sin emojis** en archivos canónicos (constitución § I).
- **Smoke test verde** antes de proponer un PR (`bash writeonmars/smoke-test.sh`).
- **Sync impact report** cuando el cambio afecte plantillas o la constitución.

## Cómo añadir una capacidad al método (un comando)

1. **Justifica la necesidad**: qué falta o qué comando existente no cubre el caso.
   Si la capacidad mapea a un principio de la constitución, decláralo.
2. **Crea el comando** `writeonmars/commands/speckit.<nombre>.md` (neutral de
   modelo). Si reemplaza a un core de Spec Kit, usa `replaces:` en su front-matter.
3. **Si hay detalle de método**, añade una referencia en
   `writeonmars/references/metodo/writeonmars-<nombre>/SKILL.md`.
4. **Lo determinista va a un script** en `writeonmars/scripts/`, invocado por el
   comando por ruta (no reimplementado en prosa).
5. **Decláralo en `writeonmars/preset.yml`** dentro de `provides.templates` con
   `type: command`.
6. **Smoke test**: adapta `writeonmars/smoke-test.sh` si el comando tiene parte
   determinista.

## Cómo añadir un sector

Cada sector es un archivo `writeonmars/references/sectores/<slug>.md` con los
*defaults* de las adendas para ese dominio (tono, anglicismos, estructura de
capítulo, cajas, citación). Copia `tecnologia.md`, rellena el esquema de
`references/sectores/_index.md` y listo: `/speckit-constitution` lo ofrece sin tocar
código. Ver también `docs/how-to.md` § "Cómo añadir un sector nuevo".

## Cómo mantener la voz

`references/voz/` es una copia de la voz canónica (`mars-voice`). Si la actualizas
allí, re-sincroniza la del preset (`cp`). No edites la voz directamente en el preset
sin reflejarlo en la fuente.

## Cómo certificar un MCP para el contrato de citación

El contrato canónico vive en `contracts/citation-contract.md` § "Cómo certificar".
Resumen operativo:

1. **Fixture mínimo**: tres `CitationRecord` representativos (uno
   `documentacion_oficial`, uno `web_publica`, uno `archivo_local`) en JSON.
2. **Valida contra el schema**:

   ```bash
   ajv validate --spec=draft2020 \
     -s contracts/citation-record.schema.json -d <fixture>.json
   ```

3. **Documenta el motor** en `docs/compatibility-matrix.md`: nombre, tipo de
   `motor`, ejemplo de `referencia`, notas operativas (latencia, coste, fallo
   conocido).

## Cómo contribuir a `resources/`

`resources/` aloja las fuentes que sostienen las decisiones normativas (constitución
§ Trazabilidad documental). Criterios:

- **Tipo admitido**: documentación oficial, manuales editoriales, papers, material
  editorial propio.
- **Metadatos**: fecha de incorporación, autoría, origen (URL o vault), licencia,
  versión consultada.
- **Sin material confidencial** (`resources/` se commitea al repo canónico).
- **Naming**: `<dominio-corto>-<tema>.md`.
- **Cross-link**: si la fuente sostiene un principio, enlázala desde la constitución.

## Cómo proponer una enmienda a la constitución

Sigue `docs/maintenance/constitution-update-procedure.md`. En corto: trigger
documentado → rama `constitution/` → `/speckit-constitution` → sync impact report →
bump semver editorial → commit `docs: amend constitution to vX.Y.Z (motivo)` →
entrada en `CHANGELOG.md`.

## Política de PRs

- **Rama dedicada** con prefijo: `feat/` (comando/sector/feature), `fix/` (scripts),
  `docs/` (documentación), `chore/` (bumps/mantenimiento), `constitution/`
  (enmiendas).
- **Smoke test verde** localmente; declara dependencias (Python, `ajv`) en el PR.
- **Sync impact report** cuando toques `writeonmars/templates/*` o
  `writeonmars/memory/constitution.md`.
- **Sin emojis**. **Una feature por PR**.

## Referencias

- `writeonmars/AGENTS.md` — contrato del agente.
- `.specify/memory/constitution.md` — fuente de verdad editorial.
- `writeonmars/docs/referencia.md` — comandos, scripts y esquemas del preset.
- `contracts/citation-contract.md` — § "Cómo certificar".
- `docs/compatibility-matrix.md` — MCPs y agentes soportados.
- `docs/maintenance/constitution-update-procedure.md` — enmiendas constitucionales.
