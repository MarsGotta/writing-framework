# Delta pass-output-schema v1.1 → v1.2 (005)

Cambios a aplicar sobre `writeonmars/contracts/pass-output-schema.md` (fuente
única). Este archivo es el diff de diseño; al implementar, el contrato
publicado se actualiza en su sitio y este documento queda como referencia.

## 1. Enum `estado` del Finding

```text
v1.1: abierto | resuelto | desviacion_justificada
v1.2: abierto | resuelto | desviacion_justificada | aplazado
```

`aplazado`: deuda declarada por disposición humana (modo estudio). No cuenta
en `revise_pending`, no bloquea el cierre, y `close.py` la enumera en el
resumen de cierre.

## 2. Reglas de transición (sustituyen al bloque v1.1)

```text
Modo produccion (sin cambios de fondo):
  abierto ──(reescritura aplicada)──→ resuelto
  abierto ──(operador firma desviación)──→ desviacion_justificada

Modo estudio (todas las transiciones vía scripts/dispose.py):
  abierto  ──aceptar──→ resuelto
  abierto  ──rechazar─→ desviacion_justificada   (motivo → decision_humana)
  abierto  ──aplazar──→ aplazado
  aplazado ──aceptar──→ resuelto
  aplazado ──rechazar─→ desviacion_justificada
```

- En modo estudio, toda transición MUST tener su DispositionRecord en
  `specs/<feature>/disposiciones.jsonl` (disposition-record.schema.json).
  Transición sin registro = inconsistencia: `status.py` la reporta como
  warning y sigue contando el hallazgo como pendiente.
- Sigue vigente: un finding `resuelto` no se borra; reabrir = crear
  `F-N.M+1` con referencia al anterior.

## 3. Huella de contenido por bloque de pasada (nuevo)

Todo bloque de pasada (1-5) termina con un comentario de máquina:

```html
<!-- huellas: {"<capitulo>": "<sha256-hex>", ...} -->
```

- Emisión: obligatoria en v1.2 en ambos modos (los comandos de pasada la
  calculan con `sha256sum chapters/NNN-*.md` o equivalente).
- Verificación: solo en modo estudio (`status.py`): huella registrada ≠
  huella actual **o huella ausente** ⇒ la pasada no cuenta para ese capítulo
  (capítulo reabierto; no evaluado ≠ verde). En produccion los bloques v1.1
  sin huella siguen contando (retrocompatibilidad FR-011).
- Pasada 5 (`global`): clave `"global"`, valor `sha256` de la concatenación
  de los sha256 de todos los capítulos en orden ordinal.

## 4. Marcador de versión

Los bloques emitidos bajo este esquema llevan
`<!-- pass-output-schema: v1.2 -->`.

## 5. Cláusula de modo para los comandos de pasada

Los comandos `speckit.review*` (pasadas 1-5) incorporan la cláusula:

> En proyectos con `mode: estudio` (manifiesto), esta pasada opera sobre
> texto escrito por humanos. PROHIBIDO editar cualquier archivo bajo
> `chapters/` o el `README.md`: la única salida es el bloque de hallazgos en
> `findings.md` (+ `claims.md` si la pasada 4 lo emite). PROHIBIDO cambiar el
> `estado` de hallazgos existentes: las transiciones son exclusivas de la
> disposición humana (`scripts/dispose.py`).

Adicional para la pasada 4 en estudio (no evaluado ≠ verde):

> Si `roots/` no contiene fichas de fuente aplicables al capítulo, el bloque
> de pasada MUST declararlo ("no evaluable contra fuentes: roots/ sin fichas
> aplicables") en el campo de notas del bloque, en vez de emitir 0 hallazgos
> como si la verificación hubiera ocurrido.

`speckit.revise` incorpora:

> En proyectos con `mode: estudio` este comando NO aplica: la corrección la
> decide y aplica el humano tras `dispose.py`. Si se invoca, debe detenerse
> sin tocar archivos y explicar el flujo de disposición.
