# Contrato del CLI `vivarium` (v1)

Binario: `vivarium` (crate `vivarium-cli`). Toda orden es no-interactiva salvo
donde se indica confirmación; toda salida informativa va a stdout, errores a
stderr. `--json` disponible en todas las órdenes para salida estructurada.

## Órdenes

### `vivarium new <dir> --kind <kind> [--mode <mode>] [--sector <slug>] [--preset <ruta>] [--operator <n>] [--email <e>] [--agents <lista>]`

Crea un proyecto editorial operativo (FR-001). `<kind>` ∈ `guia | tutorial |
documentacion | no-ficcion | novela | relato | poesia | guion | academico`
(fija el `mode` default, data-model § 2); `--mode` lo sobrescribe. Operador y
email heredan de `git config` si se omiten (paridad con `tools/new-guide.sh`).
Idempotente: re-ejecutar sobre un proyecto ya creado no duplica ni destruye.

- Efectos: git init + `specify init` + `specify preset add` + `bootstrap.py` +
  manifiesto con `mode` + `roots/README.md` + `decisions.jsonl` + `.vivarium/`
  en `.gitignore` + `.vivarium/config.toml.example` (plantilla BYOM comentada,
  ver `byom-config.md`) + commit base. Acepta `--sector <slug>` (base de
  sector para las adendas de `speckit.constitution`; default `tecnologia`
  para kinds de producción).
- Precondición verificada: `git`, `python3` (o `VIVARIUM_PYTHON`), `specify`
  disponibles; error accionable si falta alguno (exit 3).

### `vivarium status [--project <dir>]`

Passthrough de `status.py --json` + campos propios del ejecutor:
`mode` (efectivo), `in_flight` (despachos sin disposición según
`decisions.jsonl`), `blocked_by_mode` (bool). Exit 0 si el estado es legible;
exit 5 (validación) si el proyecto no es legible (sin manifiesto, JSON del
sidecar inválido o manifiesto que no valida contra el schema).

### `vivarium step [--project <dir>]`

Ejecuta **una** acción del mapa `next_step` → acción (data-model § 4) y
termina. Toma el lock; re-verifica estado antes de despachar (FR-006).

### `vivarium run [--project <dir>]`

Como `step`, en bucle, hasta: checkpoint humano (exit 10), `blocked_by_mode`
(exit 11), fallo de despacho (exit 12), `close` completado (exit 0).

### `vivarium mode set <produccion|estudio> --project <dir> [--yes]`

Cambio de modo (FR-009). Sin `--yes`: imprime la consecuencia de procedencia y
NO aplica (exit 4). Con `--yes`: actualiza `mode` + `mode_history` en el
manifiesto, añade `mode_change` a `decisions.jsonl`. El texto de consecuencia
al pasar a `produccion` MUST declarar la pérdida de demostrabilidad de autoría
humana para lo que la IA redacte desde ese momento.

### `vivarium check [--project <dir>]`

Valida el entorno y la config BYOM sin despachar (herramientas, roles,
binarios de agentes, manifiesto contra schema). Exit 0 = listo para `run`.

## Exit codes (globales, estables — los tests dependen de ellos)

| Código | Significado |
|---|---|
| 0 | Éxito / flujo completado |
| 2 | Uso inválido (argumentos) |
| 3 | Entorno incompleto (falta git/python3/specify/agente) |
| 4 | Confirmación requerida y ausente (`mode set` sin `--yes`) |
| 5 | Validación fallida (manifiesto/config/schema) |
| 6 | Lock tomado por otra instancia |
| 10 | Detenido en checkpoint humano (brief o PDF anotado) |
| 11 | Bloqueado por modo (`estudio` prohíbe el despacho requerido) |
| 12 | Fallo de despacho de agente (estado en disco intacto; reintento seguro) |

## Invariantes de toda orden

- Nunca escribe prosa de manuscrito por su cuenta (FR-013).
- Nunca modifica archivos del método fuera del efecto declarado (los cambios
  los hacen el sidecar o los agentes despachados).
- Todo despacho/disposición/cambio de modo queda en `decisions.jsonl` antes de
  devolver el control (FR-010).
