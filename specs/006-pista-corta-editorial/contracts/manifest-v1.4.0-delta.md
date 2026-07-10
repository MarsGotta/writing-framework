# Delta del manifiesto — v1.3.0 → v1.4.0

**Feature**: 006-pista-corta-editorial · **Tipo**: MINOR (aditivo) · **Fecha**: 2026-07-10

Fuente única a editar: `writeonmars/contracts/manifest-schema.json`. La raíz
`contracts/`, `specs/001-framework-architecture/contracts/` y los espejos de
`docs/` son punteros: **no edites ahí**.

---

## 1. Qué cambia

Dos propiedades opcionales nuevas en la raíz. Ninguna propiedad existente se
modifica, se renombra ni pasa a obligatoria. `additionalProperties: false` sigue
en `false`, por eso el schema **debe** declarar los campos: un manifiesto con
`track` no valida contra v1.3.0.

| Campo | Tipo | Obligatorio | Ausencia |
|---|---|---|---|
| `track` | `string`, enum `["estandar","corta"]` | no | equivale a `"estandar"` |
| `track_history` | `array` de objetos | no | ningún cambio de pista registrado |

## 2. Cambios exactos en `manifest-schema.json`

### 2.1 `$id` y `title`

```diff
-  "$id": "https://write-on-mars.dev/contracts/manifest/v1.3.0.json",
+  "$id": "https://write-on-mars.dev/contracts/manifest/v1.4.0.json",
-  "title": "Write.OnMars Project Manifest v1.3.0",
+  "title": "Write.OnMars Project Manifest v1.4.0",
```

### 2.2 `$comment` — añadir al final de la cadena existente

```text
 v1.4 (MINOR, feature 006-pista-corta-editorial): adds optional track and
 track_history (constitución v1.7.0 § Pistas de ceremonia; ausencia de track =
 estandar). track_history registra `actor` humano, a diferencia de mode_history:
 el escalado de pista exige identidad humana auditable (scripts/track.py).
```

### 2.3 `properties` — insertar tras `mode_history`

```json
"track": {
  "type": "string",
  "enum": ["estandar", "corta"],
  "description": "Pista de ceremonia del proyecto (constitución v1.7.0 § Pistas de ceremonia). Ausencia = estandar. estandar: ceremonia completa (temario multi-capítulo, 3 pasadas locales + 1 global, intro). corta: pieza única (temario degenerado de una fila, pasada combinada 1·2·3·5 + precisión 4, sin intro). Ortogonal a `mode`."
},
"track_history": {
  "type": "array",
  "description": "Registro append-only de cambios de pista. Lo escribe EXCLUSIVAMENTE scripts/track.py, que exige identidad humana desde git config y rechaza identidades de agente. Nunca se edita a mano.",
  "items": {
    "type": "object",
    "required": ["from", "to", "date", "actor"],
    "additionalProperties": false,
    "properties": {
      "from": {"type": "string", "enum": ["estandar", "corta"]},
      "to": {"type": "string", "enum": ["estandar", "corta"]},
      "date": {"type": "string", "format": "date-time"},
      "actor": {"type": "string", "minLength": 1, "description": "git config user.name del humano que ejecutó el cambio."},
      "email": {"type": "string", "format": "email"}
    }
  }
}
```

## 3. Por qué `actor` y `mode_history` no lo tiene

FR-008 exige que el escalado quede registrado con **actor humano** y que ningún
agente pueda cambiar la pista. Sin `actor`, el registro no es auditable. La spec
llama a `track_history` "espejo de `mode_history`" por su *forma* (array
append-only, escrito solo por script, nunca a mano), no por su lista de campos.

`mode_history` **no se retro-modifica** en esta feature: sería un cambio fuera de
alcance. Queda anotado en el ROADMAP.

## 4. Retrocompatibilidad

- Un manifiesto v1.3.0 (sin `track`) valida contra v1.4.0 sin cambios: ambos
  campos son opcionales.
- `findings_lib.project_track(manifest)` resuelve la ausencia a `"estandar"`, de
  modo que todo proyecto existente conserva su comportamiento exacto (FR-010).
- Un `track` con valor desconocido produce error duro y claro, igual que `mode`.

## 5. Criterio de aceptación (verificable por script)

1. `python3 -c "import json,jsonschema; s=json.load(open('writeonmars/contracts/manifest-schema.json')); jsonschema.Draft202012Validator.check_schema(s)"` → sin error.
2. Un manifiesto sin `track` valida.
3. Un manifiesto con `"track": "corta"` valida.
4. Un manifiesto con `"track": "rapida"` **no** valida.
5. Una entrada de `track_history` sin `actor` **no** valida.
6. `uvx --with pytest --with jsonschema python -m pytest tests/unit/test_bootstrap.py -q`
   en verde: el manifiesto que genera `bootstrap.py` valida contra el schema nuevo.
