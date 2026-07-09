# Modo estudio

El modo estudio sirve para proyectos donde la prosa del manuscrito la escribe la
humana. La IA revisa, anota y acompaña; no redacta capítulos ni aplica
correcciones.

## Preparar el proyecto

Declara el modo en `.writeonmars-manifest.json`:

```json
{
  "mode": "estudio"
}
```

La ausencia del campo equivale a `produccion`. En estudio, `status.py --json`
puede devolver dos checkpoints humanos nuevos:

- `write`: faltan capítulos por escribir.
- `dispose`: hay hallazgos accionables que esperan decisión humana.

## Escribir capítulos

Escribe cada capítulo en `chapters/NNN-slug.md`, usando el ordinal del temario de
`specs/<feature>/plan.md`. Por ejemplo, el capítulo 1 puede vivir en
`chapters/001-inicio.md`.

Cuando exista al menos un capítulo, las pasadas de revisión pueden ejecutarse.
Los agentes deben producir hallazgos en `findings.md` y huellas de contenido,
pero no editar `chapters/` ni `README.md`.

## Disponer hallazgos

Revisa cada hallazgo abierto y registra tu decisión:

```bash
python3 writeonmars/scripts/dispose.py F-1.1 --aceptar --project-dir .
python3 writeonmars/scripts/dispose.py F-1.2 --rechazar --motivo "no aplica a este género" --project-dir .
python3 writeonmars/scripts/dispose.py F-1.3 --aplazar --project-dir .
```

Aceptar significa que ya aplicaste tú la corrección en el manuscrito. Rechazar
exige motivo. Aplazar deja deuda declarada: no bloquea el cierre, pero aparece
en el resumen de `close.py`.

## Informe de autoría

Genera evidencia de procedencia cuando quieras:

```bash
python3 writeonmars/scripts/authorship.py --project-dir . --json
```

El informe se escribe en `specs/<feature>/authorship-report.md` y clasifica los
cambios de `chapters/` a partir de git y `decisions.jsonl`. Si aparece prosa
comiteada por un agente o dentro de una ventana de despacho de redacción, el
veredicto lo refleja.
