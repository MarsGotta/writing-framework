# Data Model — Pipeline del modo estudio (005)

## 1. DispositionRecord v1 (`specs/<feature>/disposiciones.jsonl`)

Una línea JSON por disposición humana, append-only. Único escritor:
`writeonmars/scripts/dispose.py`.

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `v` | entero | sí | Versión del registro. Siempre `1`. |
| `ts` | string | sí | Fecha-hora RFC 3339 de la disposición. |
| `finding_id` | string | sí | Id del hallazgo (`F-N.M`) en findings.md. |
| `disposicion` | enum | sí | `aceptado` \| `rechazado` \| `aplazado`. |
| `actor` | string | sí | `git config user.name` del humano que dispone. |
| `email` | string | no | `git config user.email` si existe. |
| `motivo` | string | si `disposicion = rechazado` | Razón del rechazo. |
| `nota` | string | no | Comentario libre. |

Validación (dispose.py, exit 5 en fallo):
- `finding_id` debe existir en `specs/<feature>/findings.md`.
- El hallazgo debe estar en estado `abierto` o `aplazado` (ver transiciones).
- `--rechazar` sin `--motivo` es uso inválido (exit 2).
- Sin identidad git (`user.name` vacío) → exit 3 (entorno incompleto).

## 2. Estados del Finding (pass-output-schema v1.2)

Enum `estado`: `abierto` | `resuelto` | `desviacion_justificada` | **`aplazado`** (nuevo).

Transiciones en modo estudio (solo vía dispose.py):

```text
abierto   ──aceptar──→ resuelto                  (la humana ya aplicó su corrección)
abierto   ──rechazar─→ desviacion_justificada    (motivo → decision_humana)
abierto   ──aplazar──→ aplazado                  (deuda declarada)
aplazado  ──aceptar──→ resuelto
aplazado  ──rechazar─→ desviacion_justificada
```

Reglas derivadas:
- `revise_pending` (estudio) = hallazgos crítico/medio con `estado = abierto`.
- `aplazado` no bloquea `close`; `close.py` lo lista como deuda declarada.
- Estado no-abierto **sin** DispositionRecord correspondiente (mismo
  `finding_id`, disposición compatible) ⇒ warning de inconsistencia en
  `status.py` y el hallazgo cuenta como pendiente (neutraliza el atajo de un
  agente, SC-005). En modo produccion esta verificación no aplica.

## 3. Huella de contenido por pasada (findings.md)

Cada bloque de pasada termina con un comentario de máquina:

```html
<!-- huellas: {"<capitulo>": "<sha256-hex>", ...} -->
```

- Clave: ordinal del capítulo cubierto (o `"global"` en la pasada 5, cuyo
  valor es la huella concatenada `sha256(concat(sha256(cap_i)))` en orden).
- Valor: sha256 de los bytes del archivo `chapters/NNN-*.md` en el momento de
  la pasada.
- En modo estudio, una pasada N cuenta en `passes_done[C]` solo si
  `huellas[C] == sha256(chapters/C actual)`. Huella ausente ⇒ la pasada NO
  cuenta para ese capítulo (no evaluado ≠ verde: no hay proyectos estudio
  legacy; en un proyecto convertido, re-pasar es barato y honesto) y
  `status.py` lo explica en el dashboard y como warning.
- En modo produccion las huellas se escriben pero no se verifican.

## 4. Salida `--json` de status.py — campos nuevos/cambiados

| Campo | Tipo | Cambio |
|-------|------|--------|
| `mode` | string | **Nuevo**: `"produccion"` \| `"estudio"` (ausencia en manifiesto = produccion). |
| `next_step` | string | Gana valores `write` y `dispose` (solo en estudio). |
| `pending_chapters` | lista de enteros | **Nuevo**: ordinales del temario sin capítulo en disco, como enteros (ambos modos; ya derivable, ahora explícito). |
| `pending_dispositions` | lista | **Nuevo** (estudio): ids de hallazgos crítico/medio abiertos. |
| `deferred_findings` | lista | **Nuevo**: ids con `estado = aplazado` (ambos modos; en produccion siempre `[]` salvo migraciones). |
| `reopened_chapters` | lista | **Nuevo** (estudio): capítulos cuya huella no coincide (pasadas invalidadas). |

Todo lo demás no cambia. Con `mode = produccion` los campos nuevos existen
pero `next_step` jamás vale `write`/`dispose` (FR-011).

## 5. Tabla next_step → acción del ejecutor (delta sobre 004)

| next_step | produccion | estudio |
|-----------|-----------|---------|
| `implement` | despacho Redactora | *(no ocurre; si ocurre → guardarraíl exit 11)* |
| `write` | *(no ocurre)* | **Checkpoint humano** (exit 10): escribir capítulos pendientes |
| `revise` | despacho Redactora | *(no ocurre; si ocurre → guardarraíl exit 11)* |
| `dispose` | *(no ocurre)* | **Checkpoint humano** (exit 10): correr dispose.py |
| `review` | despacho Mesa/Documentalista | igual (hallazgos, no prosa) |
| `intro` (etapa global del ejecutor) | despacho Redactora | **Checkpoint humano** (exit 10): la humana escribe README.md |
| resto (`setup`…`close`) | sin cambios | sin cambios |

## 6. AuthorshipReport (salida de authorship.py)

`specs/<feature>/authorship-report.md` + `--json`. Estructura JSON:

```json
{
  "head": "<sha del commit sobre el que se calculó>",
  "chapters": {
    "1": {
      "file": "chapters/001-slug.md",
      "commits": [
        {"sha": "…", "author": "…", "email": "…", "clase": "humano|agente", "razon": "identidad|ventana_dispatch"}
      ],
      "veredicto": "humana|mixta|ia"
    }
  },
  "veredicto_global": "autoria_humana_demostrada|mixta|ia"
}
```

- `clase = agente` si el email casa `*@agents.writeonmars.invalid` **o** el
  commit cae dentro de una ventana dispatch→disposition de
  `implement|revise|intro` en `decisions.jsonl` para ese capítulo.
- `veredicto_global = autoria_humana_demostrada` ⟺ todos los capítulos
  `humana`.
- Determinismo: sin timestamps de generación; mismo repo + mismo JSONL ⇒
  salida byte a byte idéntica (SC-003).
