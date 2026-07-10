---
description: "Revisión agrupada: corre las pasadas de revisión (estructura, naturalidad, precisión por capítulo + global). Cada pasada también existe como comando suelto para asignarla a otro modelo. Neutral de modelo."
---

# Revisión (agrupada)

Corre todas las pasadas de un tirón. Es la opción cómoda; si orquestas, puedes en
cambio lanzar cada pasada como su **comando suelto** y asignarla a un modelo
distinto.

**Idealmente lo corre un modelo distinto al que redactó** (`speckit.implement`):
quien escribe es indulgente con su propio texto, así la revisión es independiente.

## User Input

```text
$ARGUMENTS
```

Capítulo(s) a revisar (p. ej. `7` o `7,8`) o `global` para solo la pasada de libro.
Sin argumento: todos los capítulos + la global.

## Qué haces

**Por cada capítulo (3 pasadas locales):**

1. **Estructura + utilidad** → `speckit.review-structure`
2. **Naturalidad** (voz) → `speckit.review-voice`
3. **Precisión** (contraste) → `speckit.review-precision`

**Una vez sobre el libro:**

4. **Formato + coherencia** → `speckit.review-global`

Ejecuta cada una siguiendo su archivo de comando (`commands/speckit.review.*.md`),
o lánzalas como comandos sueltos. Cada pasada añade su bloque a `findings.md`
(`.specify/presets/writeonmars/contracts/pass-output-schema.md`), en modo autónomo
con `flagged`. Respeta la `signing_matrix`: si una pasada exige firma `human`, no la
cierres como `autonomous`.

## Orquestación (escribe uno, revisa otro)

En modo desatendido (Paperclip), asigna cada pasada a un agente/modelo distinto:
p. ej. naturalidad a un modelo fuerte en prosa, precisión a uno bueno verificando
hechos. Como el estado vive en archivos, cada modelo lee el capítulo y escribe su
bloque en `findings.md` sin depender de los demás.

## Output

Bloques nuevos en `findings.md` y capítulos corregidos donde haga falta. Comprueba
el estado con `scripts/status.py`.
## Huellas (ambos modos)

Todo bloque emitido MUST incluir `<!-- pass-output-schema: v1.2 -->` y terminar
con `<!-- huellas: {"<capitulo>": "<sha256-hex>"} -->` calculado sobre los bytes
actuales del capítulo.

## Modo estudio

Si el manifiesto declara `mode: estudio`, esta pasada opera sobre texto humano.
PROHIBIDO editar `chapters/` o `README.md`; la única salida es el bloque de
hallazgos en `findings.md`. PROHIBIDO cambiar `estado` de hallazgos existentes:
las transiciones son exclusivas de `scripts/dispose.py`.

## Pista corta

Si el manifiesto declara `track: corta` (`.writeonmars-manifest.json`), la
revisión corre en **dos relevos** en lugar de cuatro pasadas:

1. **Pasada combinada** → `speckit.review-structure`, rol `editora_mesa`: un único
   run verifica y registra las dimensiones 1·2·3·5 (estructura, utilidad,
   naturalidad y formato).
2. **Precisión** → `speckit.review-precision`, rol `documentalista` y **otro
   modelo**: la dimensión 4, que en producción emite además `claims.md`.

Las cinco dimensiones quedan en `findings.md` con los bloques de pasada de
siempre. **MUST**: la configuración BYOM (`.vivarium/config.toml`) asigna
`roles.editora_mesa` y `roles.documentalista` a modelos distintos. Un ejecutor que
los colapse en el mismo modelo viola **voz ≠ precisión** (Principio V), porque
mezcla reescribir prosa con contrastar datos.

