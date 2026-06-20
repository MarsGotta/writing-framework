---
name: writeonmars-constitution
description: Fija las adendas del proyecto (capa por guía) sobre el núcleo de la constitución durante /speckit-constitution. Elige sector, calibra tono, terminología, anglicismos y gobernanza con valores por defecto. Trigger cuando la persona diga "constitución del proyecto", "configura la constitución", "adendas del proyecto", "/speckit-constitution", o al arrancar una guía nueva tras /speckit-setup.
allowed-tools: Bash, Read, Write, Edit
---

# writeonmars-constitution

Materializa la separación **núcleo / adendas** de la constitución. El núcleo
(Principios I–VI, estándares, gobernanza) es universal y se rige por versión: no
se edita por guía. Las **adendas** son la capa por guía con lo normativo que sí
varía. Este es el primer paso del ciclo editorial, después de `/speckit-setup`.

## Modelo conceptual

Tres niveles, no dos:

- **Núcleo** (preset, versionado): voz, estructura, brief, revisión 3+1,
  neutralidad de modelo. No cambia entre guías. Garantiza que toda guía suene
  igual de bien y comparta el método.
- **Adendas del proyecto** (esta skill): lo normativo propio de la guía — tono
  calibrado, contrato terminológico, anglicismos admitidos, matices léxicos,
  relajaciones estructurales, gobernanza. Lo verifica la revisión.
- **Brief** (`/speckit-specify`): lo descriptivo — audiencia, problema, resultado,
  ejemplo recurrente, riesgos. No son reglas, son datos.

Regla de frontera: *¿una pasada de revisión citaría esto para rechazar un
capítulo?* Si sí y es igual para todas las guías → núcleo. Si sí pero es propio de
esta guía → adendas. Si describe al lector o la meta → brief.

## Bases de sector

Cada guía pertenece a un sector (tecnología, veterinaria, medicina, ciencia,
humanidades, literatura…). Cada sector tiene una base en
`references/sectores/<slug>.md` que **propone los valores por defecto** de las
adendas: tono, anglicismos, matices léxicos, fuentes de autoridad, forma del
ejemplo recurrente, citación. Una base nunca debilita los principios NO
NEGOCIABLES; solo calibra lo que el núcleo deja al proyecto.

El sistema es ampliable sin tocar código: añadir un sector = crear su archivo
siguiendo el esquema de `references/sectores/_index.md`. El comando lista los
archivos de esa carpeta y los ofrece. Hoy solo existe `tecnologia.md`.

## Procedimiento

1. Verifica el núcleo: `.specify/memory/constitution.md` debe existir. Si no,
   detente y pide `/speckit-setup`.
2. Descubre sectores: lista `references/sectores/*.md` salvo `_index.md`. Muestra
   nombre + alcance, numerados. Pide elegir (si hay uno solo, confírmalo).
3. Carga la base del sector → defaults de todas las preguntas.
4. Ofrece camino rápido: aceptar el estándar del sector tal cual, o cuestionario.
5. Si cuestionario: pregunta **una a una**, mostrando el default entre corchetes.
   Enter mantiene el default; respuesta lo cambia. Permite reintento sin reiniciar.
   Campos: tono calibrado, anglicismos admitidos, matices léxicos, contrato
   terminológico inicial, relajaciones estructurales, idioma/excepciones,
   gobernanza/firmas.
6. Compón el bloque de adendas desde `templates/adendas-template.md` y escríbelo en
   `.specify/memory/constitution.md`. El bloque empieza por el centinela
   `<!-- WRITEONMARS:ADENDAS -->` (frontera núcleo/adendas; la usa `bootstrap.py
   --force` para re-sellar sin perder las adendas):
   - No toques el núcleo (todo lo anterior al centinela).
   - Si ya hay centinela, diff + confirmación antes de reemplazar desde él al final.
   - Si no, añade el bloque al final.
7. Actualiza `.writeonmars-manifest.json`: `sector` = slug; `signing_matrix` según
   gobernanza (por defecto sin cambios). Fechas ISO-8601.

## Defaults y no bloqueo

Toda pregunta tiene valor por defecto del sector. El comando **siempre** puede
cerrarse aceptando defaults: ese es el estándar de la casa. Nunca bloquea por dejar
defaults. Lo único que lo detiene es la ausencia del núcleo.

## Inputs

- `.specify/memory/constitution.md` — núcleo (precondición).
- `references/sectores/*.md` — bases de sector y sus defaults.
- `templates/adendas-template.md` — plantilla de la capa por guía.
- `.writeonmars-manifest.json` — para escribir `sector` y `signing_matrix`.
- Respuestas del cuestionario (o aceptación del estándar).

## Outputs

- `.specify/memory/constitution.md` con "## Adendas del proyecto" sobre el núcleo
  intacto.
- `.writeonmars-manifest.json` con `sector` (y `signing_matrix` si cambió).

## Errores comunes

- Editar el núcleo en vez de las adendas: prohibido. Las adendas viven en su propia
  sección; el núcleo se actualiza por versión, no a mano por guía.
- Sector inexistente: si el slug pedido no tiene archivo, ofrece la lista real y
  sugiere crear la base (`references/sectores/_index.md` explica cómo).
- Adendas previas sobrescritas sin avisar: siempre diff + confirmación.

## Versión

v0.1.0 — 2026-06-20
