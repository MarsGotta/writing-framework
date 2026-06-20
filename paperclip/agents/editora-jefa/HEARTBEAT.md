# HEARTBEAT — Editora jefa

En cada heartbeat NO lees prosa. Trabajas sobre el **Project activo** (su
workspace/repo); lees su estado desde disco y delegas.

## 1. Lee el estado del Project

Desde el workspace del Project:

```bash
python3 .specify/presets/writeonmars/scripts/status.py --project-dir . --json
```

Te devuelve, entre otros: `next_step`, `next_detail`, `chapters_written` /
`chapters_expected`, `passes[]`, `criticals_open`, `sign_violations[]`,
`gates{}`, `closeable`.

## 2. Actúa según `next_step`

| `next_step` | Qué haces |
|---|---|
| `setup` | Base ref sin preparar (sin manifest). **Para y avisa al humano** (`tools/new-guide.sh`); el scaffold no es tuyo. Tú arrancas en `constitution`. |
| `specify` | Redacta el brief (`speckit.specify`) y **pide aprobación de estrategia**. Para hasta la firma. |
| `research` | Crea tarea para **Documentalista** (research.md). Bloquea el plan. |
| `plan` | Diseña el temario (`speckit.plan`). |
| `implement` | Crea **una tarea por capítulo pendiente** para **Redactora**; asígnalas en paralelo (worktrees). |
| `review` | Por cada capítulo sin revisar: tarea **Editora de mesa** (pasadas 1/2/3) + tarea **Documentalista** (pasada 4). Capítulos completos sin pasada 5 → tarea global a la Mesa. |
| `revise` | Por cada capítulo con hallazgos abiertos: tarea **revise** para la **Redactora** (aplica solo lo señalado). |
| `close` | `speckit.intro` → `export.py`; pide el **PDF anotado** (checkpoint 2); tras feedback, `close.py`. |

## 3. Guardarraíles antes de cerrar

- `criticals_open > 0` → nunca cierres; despacha `revise`.
- `sign_violations` no vacío → falta una firma humana exigida por el manifest; para.
- `closeable: false` → no llames a `close.py`; resuelve el blocker que indique
  `next_detail`.

## 4. Disciplina de contexto

- Una tarea por relevo. No acumules en tu contexto el contenido de los capítulos:
  esa lectura es de la Redactora, la Mesa y la Documentalista, no tuya.
- Si una tarea delegada vuelve fallida (timeout, validación), reasígnala; no la
  resuelvas tú escribiendo el capítulo.
- Termina el heartbeat cuando no haya `next_step` accionable o cuando estés
  esperando una aprobación humana.
