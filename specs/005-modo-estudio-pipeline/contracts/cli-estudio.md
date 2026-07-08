# Contrato CLI — scripts del modo estudio (005)

Dos scripts deterministas nuevos en `writeonmars/scripts/` (sin LLM, stdlib
Python; `authorship.py` puede invocar el binario `git`). Comparten la
convención de exit codes del preset: 0 ok · 1 fallo de validación editorial ·
2 uso inválido · 3 entorno incompleto.

## 1. `dispose.py` — disposición humana de hallazgos

```text
python3 scripts/dispose.py <finding_id> (--aceptar | --rechazar --motivo "…" | --aplazar)
                           [--nota "…"] [--project-dir DIR] [--json]
```

| Caso | Exit | Efecto |
|------|------|--------|
| Disposición válida | 0 | Actualiza `estado` del hallazgo en `specs/<feature>/findings.md` **y** añade DispositionRecord a `specs/<feature>/disposiciones.jsonl` (ambos o ninguno: escribe primero el JSONL con un registro provisional en memoria, aplica la edición de findings.md y solo entonces persiste la línea; si la edición falla no queda línea nueva). |
| `finding_id` inexistente | 1 | stderr lo dice; nada se escribe. |
| Estado actual no dispone (`resuelto`/`desviacion_justificada`) | 1 | Transición inválida; nada se escribe. |
| `--rechazar` sin `--motivo` | 2 | Uso inválido. |
| `mode != estudio` en el manifiesto | 1 | El ciclo de disposición es del modo estudio; en produccion el flujo es `revise`. |
| `git config user.name` vacío/ausente | 3 | Sin identidad humana no hay disposición auditable. |

Transiciones permitidas: `abierto → {resuelto, desviacion_justificada,
aplazado}`; `aplazado → {resuelto, desviacion_justificada}`.

Resolución del directorio de spec: la misma regla que `status.py` — primer
directorio de `specs/` (orden lexicográfico) que contenga `spec.md`. Sin
spec ⇒ exit 1.

`--json` imprime el DispositionRecord escrito. La actualización de findings.md
toca **solo** la celda `estado` (y `decision_humana` en rechazo) de la fila
del hallazgo; el resto del archivo queda byte a byte intacto.

## 2. `authorship.py` — informe de autoría humana

```text
python3 scripts/authorship.py [--project-dir DIR] [--json] [--out PATH]
```

| Caso | Exit | Efecto |
|------|------|--------|
| Informe generado | 0 | Escribe `specs/<feature>/authorship-report.md` (o `--out`); con `--json`, imprime el AuthorshipReport a stdout. |
| No es repo git / sin commits en `chapters/` | 1 | Mensaje claro: sin historial no hay evidencia que informar. |
| `decisions.jsonl` ilegible (línea malformada) | 1 | Nombra archivo:línea. |
| `git` no disponible | 3 | Entorno incompleto. |

Clasificación por commit que toca `chapters/` (data-model § 6):
`agente` ⟺ email `*@agents.writeonmars.invalid` ∨ commit dentro de una
ventana dispatch→disposition de `implement|revise|intro` para ese capítulo en
`decisions.jsonl`. Reglas de resolución fijas: (a) el ordinal de capítulo de
un archivo es su prefijo numérico (`chapters/NNN-*.md` → `NNN` sin ceros a la
izquierda); archivos bajo `chapters/` sin prefijo numérico se reportan en una
sección "sin ordinal" con su clasificación, sin romper; (b) el instante del
commit comparado con la ventana es el **committer date en UTC** (`%cI` de
git). Determinismo: la salida depende solo de (HEAD, decisions.jsonl); sin
timestamps de generación.

## 3. `status.py` — cambios de contrato (v de salida no versionada; aditivo)

- Campo nuevo `mode` en `--json`.
- Valores nuevos de `next_step`: `write`, `dispose` (solo `mode: estudio`).
- Campos nuevos: `pending_chapters`, `pending_dispositions`,
  `deferred_findings`, `reopened_chapters` (listas; ver data-model § 4).
- Verificación de huellas y del cruce findings↔disposiciones **solo** en
  estudio; warnings ante inconsistencia (nunca crash por datos legacy).
- Con `mode: produccion` o sin campo `mode`: salida idéntica a la actual
  salvo los campos aditivos (FR-011); `--gate` no cambia.

## 4. `close.py` — cambio aditivo

Al cerrar un proyecto (ambos modos), si existen hallazgos `aplazado`, el
resumen de cierre los enumera como "deuda declarada" (id, severidad,
capítulo). No bloquean el cierre.

## 5. Ejecutor (vivarium) — mapeo de los pasos nuevos

Delta sobre `writeonmars/contracts/executor-contract.md` (se añade como
sección "Modo estudio" del contrato publicado):

- `next_step ∈ {write, dispose}` ⇒ checkpoint humano (exit 10), **no**
  despacho. Mensajes: `write` → "faltan capítulos por escribir (modo
  estudio)"; `dispose` → "hallazgos a la espera de disposición humana
  (scripts/dispose.py)".
- Etapa global `intro` con `mode: estudio` ⇒ checkpoint humano (exit 10), no
  despacho a Redactora (el README de presentación es prosa publicada).
- El guardarraíl de modo (exit 11 ante pasos que escriben manuscrito) no se
  modifica: sigue siendo la red de seguridad ante estados imposibles.
- Convención de identidad: si un ejecutor comitea trabajo de agentes, el
  autor del commit MUST ser `<rol>@agents.writeonmars.invalid`.
