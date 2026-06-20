# Contrato para el agente que ejecuta el preset

Este preset está pensado para que **cualquier agente, con cualquier modelo** (no
solo Claude) ejecute el pipeline editorial. Estas reglas hacen los comandos
neutrales de modelo. Léelas antes de ejecutar cualquier `speckit.*` de este preset.

## Principios de neutralidad

- **No dependas de skills de un proveedor.** No invoques "la skill marcela-prose"
  ni nada específico de Claude. La voz, la didáctica y el método viajan dentro del
  preset como documentos en `.specify/presets/writeonmars/references/`. Léelos y aplícalos.
- **No asumas herramientas propietarias.** Usa solo: leer/escribir archivos,
  ejecutar los scripts de `scripts/`, y (cuando el comando lo diga) buscar en la
  web o en MCPs que cumplan el contrato de citación. Si una capacidad no está,
  decláralo y bloquea; no inventes.
- **Lo determinista va a un script.** Estado, export, feedback, cierre y memoria
  son `scripts/*.py`: ejecútalos, no los reimplementes en prosa. Así el resultado
  es reproducible entre modelos.
- **Respeta los contratos.** Las salidas siguen los esquemas de `.specify/presets/writeonmars/contracts/`
  (citación, manifest, pass-output). Las fechas en ISO-8601.
- **Idioma primario español**, salvo lo que el brief declare como excepción.

## Referencias que cargas según el paso

| Para… | Lee |
|---|---|
| Aplicar la voz al redactar/revisar | `.specify/presets/writeonmars/references/voz/SKILL.md` (+ su `.specify/presets/writeonmars/references/`) |
| Diseño didáctico (estructura, carga cognitiva) | `.specify/presets/writeonmars/references/didactica/SKILL.md` |
| Detalle de cada paso del método | `.specify/presets/writeonmars/references/metodo/writeonmars-<paso>/SKILL.md` |
| Defaults por sector para las adendas | `.specify/presets/writeonmars/references/sectores/<sector>.md` (esquema en `_index.md`) |
| Reglas editoriales: núcleo + adendas de la guía | `.specify/memory/constitution.md` |

## Orden del ciclo (comandos del preset, no pisan los de Spec Kit)

```
speckit.setup        → bootstrap: núcleo de la constitución + manifest (una vez tras instalar)
speckit.constitution → adendas del proyecto: sector + tono + terminología + gobernanza (primer paso, guiado con defaults)
speckit.specify      → brief con preguntas                  (checkpoint humano 1)
speckit.research   → research.md con citas
speckit.plan       → temario + descripciones encadenadas
speckit.implement  → redacción de UN capítulo (solo escribe; repetir por capítulo)
speckit.review     → pasadas de revisión (idealmente otro modelo); sueltas:
                     review-structure · review-voice · review-precision · review-global
speckit.revise     → aplica al texto los hallazgos abiertos de findings.md
speckit.intro      → README de presentación (apertura del PDF)
speckit.status     → tablero + gates (críticos · firmas · completitud)
speckit.export · speckit.feedback                         (checkpoint humano 2)
speckit.close      → gate + PDF final
```

Quien escribe (`implement`) no se revisa: la revisión va aparte y, en orquestación,
con otro modelo. Las pasadas locales (estructura+utilidad, voz, precisión) corren
por capítulo; la global (formato + coherencia), una vez sobre el libro entero. La
precisión **verifica las fuentes en vivo** (abre la URL/web), no solo confía en
`research.md`.

Todos son comandos de este preset, con nombres que **no colisionan** con los core
de Spec Kit (`specify`, `plan`, `tasks`, `implement`, `clarify`, `analyze`…), que
siguen disponibles si los quieres. El pipeline editorial usa los de arriba.

## Dos puntos donde para un humano (no automatizar del todo)

1. **Brief + investigación**: el agente formula preguntas y espera la firma
   humana antes de seguir. No las inventes ni las saltes.
2. **PDF anotado**: el humano anota; `feedback_intake.py` traduce; el agente
   aplica solo lo señalado.

Todo lo demás corre desatendido (apto para orquestación tipo Paperclip lanzando
estos comandos con el modelo que sea).
