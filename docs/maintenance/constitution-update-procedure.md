# Procedimiento de enmienda de la constitución

Audiencia: persona mantenedora del framework Write.OnMars. Cubre el ciclo
"detectar discrepancia → enmendar → propagar plantillas → comunicar a
proyectos instalados". Complementa la sección **Governance § Procedimiento
de enmienda** de `.specify/memory/constitution.md`.

## Cuándo aplicar este procedimiento

Aplica cuando aparezca alguna de estas señales:

- **Discrepancia recurrente** entre la constitución y las guías reales
  publicadas (un anti-pattern detectado en pasada 3 que no está codificado,
  una checklist que en la práctica todas las personas operadoras deben
  modificar, un campo del brief que sistemáticamente queda vacío).
- **Nuevo estándar editorial** validado en uno o varios pilotos: una nueva
  caja visual obligatoria, un cierre de capítulo distinto, una pasada
  adicional, un campo nuevo del brief.
- **Refinamiento normativo de una regla existente**: aclaración o expansión
  que cambia el comportamiento esperable del agente o de la persona
  operadora (ej. extender la lista de anglicismos a sustituir, redefinir
  qué cuenta como "ejemplo recurrente").
- **Cambio en la arquitectura del framework** (sección "Arquitectura del
  framework"): nueva integración con MCPs, nueva fuente obligatoria, nueva
  política de memoria externa.

## Pasos

1. **Trigger documentado.** Antes de tocar la constitución, documentar la
   causa en una issue o nota: discrepancia detectada, evidencia que la
   sostiene, alcance estimado del cambio.
2. **Crear rama dedicada.** Prefijo obligatorio `constitution/`. Ejemplos:
   `constitution/v1-2-add-pasada-six` o
   `constitution/v1-1-1-clarify-pasada-3`.
3. **Ejecutar `/speckit-constitution`.** Lanzar la skill con la propuesta
   redactada en lenguaje editorial natural. La skill generará el sync
   impact report dentro del propio archivo de la constitución.
4. **Sync impact report.** Identificar qué plantillas de
   `.specify/templates/*.md` quedan afectadas. La constitución exige marcar
   cada plantilla como `pending` o `updated` en la cabecera del archivo.
   Plantillas a revisar siempre:
   - `spec-template.md` (brief de nueve campos, "Trayectos de lector").
   - `plan-template.md` ("Temario", "Descripciones encadenadas",
     Constitution Check editorial).
   - `tasks-template.md` (fases editoriales y software).
   - `checklist-template.md` (checklist por pasada).
5. **Plan de migración para guías ya publicadas.** Si la enmienda afecta
   guías que ya pasaron las cinco pasadas, declarar:
   - Lista de guías impactadas.
   - Criterio de re-revisión (¿se reescribe la pasada afectada?, ¿se añade
     un anexo?, ¿se deja como "guía bajo constitución vX.Y.Z" sin tocar?).
   - Plazo razonable para la re-revisión.
6. **Bump de versión semver editorial.** Reglas explicitadas en la
   constitución § Governance:
   - **MAJOR**: eliminación o redefinición incompatible de un principio o
     sección de gobierno; cambios que invalidan guías publicadas.
   - **MINOR**: nuevo principio, nueva sección de estándares editoriales o
     expansión material de una regla existente.
   - **PATCH**: aclaraciones, correcciones tipográficas, refinamientos no
     semánticos.
7. **Commit dedicado.** Mensaje canónico:
   `docs: amend constitution to vX.Y.Z (<motivo>)`. Ejemplo histórico:
   `docs: amend constitution to v1.1.0 (Write.OnMars naming + arquitectura del framework)`.
8. **Propagación a proyectos instalados.** Tras el merge:
   - El campo `constitution_version` del manifest del repo canónico se
     bumpea automáticamente cuando una persona operadora corre
     `writeonmars-update`.
   - `writeonmars-update` notifica el bump de `constitution_version`,
     muestra el diff de la sección "Sync Impact Report" y propone copiar
     las plantillas afectadas (`.specify/templates/*.md`) sin sobreescribir
     personalizaciones que el proyecto haya hecho. La persona operadora
     decide qué plantillas adoptar.
   - Las pasadas en curso (en estado `blocked` o `pending`) se vuelven a
     evaluar bajo la nueva constitución solo si la persona operadora lo
     declara explícitamente. Por defecto, una pasada cerrada bajo una
     constitución previa se considera firme.
9. **Comunicar el cambio.** Añadir entrada al `CHANGELOG.md` del framework
   describiendo el bump (sección "Constitution") y enlazar el sync impact
   report. Si el bump es MAJOR, abrir un aviso explícito invitando a las
   personas operadoras a re-correr las pasadas afectadas en sus guías.

## Errores comunes

- **Plantillas no actualizadas tras una MINOR.** El sync impact report queda
  incompleto si una plantilla afectada se marca como `updated` sin haberla
  tocado. Re-correr `/speckit-constitution` tras modificar la plantilla.
- **Bump confundido con bump de skill.** El bump de la constitución
  (`constitution_version` en el manifest) y el bump de skills
  (`skills[].version`) son independientes. Una enmienda de la constitución
  no implica bumpear todas las skills; sí implica revisar si alguna skill
  cambia de comportamiento normativo.
- **Rama sin prefijo `constitution/`.** El hook Spec Kit `validate-branch`
  no rechaza el push, pero la persona mantenedora debería rechazarlo en
  revisión: el prefijo es la única señal automatizada de que la rama
  modifica la constitución.

## Referencias

- `.specify/memory/constitution.md` § Governance § "Procedimiento de
  enmienda" — fuente normativa.
- `.claude/skills/writeonmars-update/SKILL.md` — propagación a proyectos
  instalados (incluye `constitution_version`).
- `docs/maintenance/skill-update-procedure.md` — procedimiento análogo
  para skills bundled.
- `CHANGELOG.md` — registro histórico de enmiendas.
