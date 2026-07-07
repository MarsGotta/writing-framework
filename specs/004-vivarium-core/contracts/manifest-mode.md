# Extensión del manifest-schema: campo `mode` (v1.2.1 → v1.3.0, MINOR)

Archivo a editar: `writeonmars/contracts/manifest-schema.json` (única fuente
editable; `contracts/` raíz y `specs/001` son punteros — CLAUDE.md). El schema
tiene `additionalProperties: false`, por eso los campos nuevos DEBEN
declararse.

## Cambios exactos

1. `$id`: `https://write-on-mars.dev/contracts/manifest/v1.3.0.json`
2. `title`: `Write.OnMars Project Manifest v1.3.0`
3. `$comment`: añadir al historial:
   `v1.3 (MINOR, feature 004-vivarium-core): adds optional mode and
   mode_history (constitución v1.6.0 § Modos de proyecto; ausencia de mode =
   produccion).`
4. En `properties`, añadir:

```json
"mode": {
  "type": "string",
  "enum": ["produccion", "estudio"],
  "description": "Modo de trabajo del proyecto (constitución v1.6.0 § Modos de proyecto). Ausencia = produccion. produccion: la IA redacta anclada en fuentes. estudio: el humano escribe; la IA no redacta prosa del manuscrito."
},
"mode_history": {
  "type": "array",
  "description": "Registro append-only de cambios de modo. Cada cambio lo escribe una acción humana explícita (vivarium mode set --yes o edición manual documentada).",
  "items": {
    "type": "object",
    "required": ["from", "to", "date"],
    "additionalProperties": false,
    "properties": {
      "from": {"type": "string", "enum": ["produccion", "estudio"]},
      "to": {"type": "string", "enum": ["produccion", "estudio"]},
      "date": {"type": "string", "format": "date-time"}
    }
  }
}
```

`mode` y `mode_history` NO entran en `required` (compatibilidad: todos los
manifiestos existentes siguen validando; ausencia = `produccion`).

## Consumidores a actualizar en la implementación

- `writeonmars/scripts/bootstrap.py`: escribir `mode` en el manifiesto default
  (el valor llega por argumento/entorno desde `vivarium new`; default
  `produccion` si no se indica). Los tests de bootstrap
  (`tests/unit/test_bootstrap.py`) ganan un caso por modo.
- `writeonmars/scripts/status.py`: **sin cambios de lógica** (capa agnóstica;
  el guardarraíl de modo vive en el ejecutor). Solo tolerar el campo si valida
  el manifiesto.
- `tests/unit/conftest.py`: fixtures pueden seguir sin `mode` (prueba la
  compatibilidad de ausencia); añadir una fixture con `mode: estudio` para el
  guardarraíl.
- Validadores de contratos (`tests/lib/validate-*.sh`, smoke): re-ejecutar; el
  bump es MINOR y no rompe nada existente.
- `CHANGELOG.md`: entrada del bump v1.3.0 del manifest-schema.
