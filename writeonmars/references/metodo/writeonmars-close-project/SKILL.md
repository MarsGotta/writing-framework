---
name: writeonmars-close-project
description: Evalúa si el proyecto editorial puede cerrarse leyendo findings.md y el manifiesto. Devuelve {closeable, blockers}. Trigger cuando la persona diga "cierra el proyecto editorial", "valida el cierre", "se puede publicar la guía", "writeonmars close".
allowed-tools: Bash, Read
---

# writeonmars-close-project

Skill que materializa el "close gate" del flujo editorial. Lee
`specs/[###-feature]/findings.md` y `.writeonmars-manifest.json` y devuelve
un objeto `{closeable: bool, blockers: [...]}` que indica si la guía puede
publicarse o qué impedimentos quedan.

## Cuándo dispararse

- "cierra el proyecto editorial"
- "valida el cierre"
- "se puede publicar la guía"
- "writeonmars close"
- Tras completar la pasada 5.

## Qué hace

1. Carga `.writeonmars-manifest.json` y valida su `signing_matrix`.
2. Carga `specs/[###-feature]/findings.md` y parsea cada bloque de
   pasada según `contracts/pass-output-schema.md` v1.0.
3. Aplica los tres gates obligatorios:

   **Gate 1 — hallazgos críticos abiertos (FR-020)**.
   Bloquea si existe ≥ 1 finding con `severidad: critico` y `estado:
   abierto`.

   **Gate 2 — firma humana faltante (FR-020a)**.
   Bloquea si alguna pasada tiene `firma.tipo: autonomous` cuando el
   manifiesto declara `signing_matrix[pasada]: human`. Con el default
   (todas autónomas) este gate no aplica.

   **Gate 3 — completitud del temario**.
   Bloquea el cierre si faltan capítulos del temario de `plan.md`
   (`chapters/` < capítulos declarados). `export` sí permite un PDF
   parcial como preview; `close` exige la guía completa.

4. Devuelve un reporte estructurado:

```json
{
  "closeable": false,
  "blockers": [
    {
      "type": "critical_finding_open",
      "pasada": "1_estructura",
      "finding_id": "F-1.3",
      "capitulo": 2,
      "problema": "..."
    },
    {
      "type": "human_signature_missing",
      "pasada": "3_naturalidad",
      "expected": "human",
      "got": "autonomous"
    }
  ]
}
```

5. Si `closeable: true`, imprime "El proyecto puede cerrarse" y reporta
   la lista de checklists firmadas.

## Inputs

- `.writeonmars-manifest.json`.
- `specs/[###-feature]/findings.md`.
- `checklists/[###-feature]/pasada-{1..5}.md` (para validación cruzada
  de firma).

## Outputs

- Reporte estructurado al stdout en JSON.
- Mensaje legible al stderr resumiendo blockers o luz verde.

## Procedimiento

1. Resolver `[###-feature]` desde la rama activa (o argumento explícito).
2. Verificar existencia de `.writeonmars-manifest.json`. Si falta,
   abortar con error claro: el manifiesto es prerrequisito del flujo.
3. Verificar existencia de `findings.md`. Si falta, abortar: no se
   puede cerrar sin pasar las cinco pasadas.
4. Parsear bloques de pasada en `findings.md`. Cada bloque empieza con
   `## Pasada N — <nombre>` y termina cuando empieza el siguiente o el
   archivo termina.
5. Para cada pasada, extraer:
   - `pasada` (enum del schema).
   - `firma.tipo` (`autonomous` | `human`).
   - Filas de la tabla de hallazgos: id, severidad, estado.
6. Aplicar Gate 1: recorrer hallazgos. Cualquier finding crítico
   abierto añade un blocker.
7. Aplicar Gate 2: comparar `firma.tipo` con `signing_matrix` para cada
   pasada presente. Si la matriz exige `human` y el bloque declara
   `autonomous`, añadir blocker.
8. Componer JSON y mensaje legible. Salir con código 0 si
   `closeable: true`, código 1 si hay blockers.

## Errores comunes

- `findings.md` malformado (encabezado sin schema marker): la skill lo
  reporta como blocker `type: schema_violation`.
- `signing_matrix` con valores fuera del enum: blocker
  `type: manifest_invalid`.
- Pasada que aparece dos veces en el archivo: la skill toma la última
  ocurrencia y reporta warning de duplicado.
- Falta una pasada (ej. nunca se ejecutó la pasada 4): la skill lo
  reporta como blocker `type: pasada_missing`.

## FR cubierta

- FR-020 (gate de hallazgos críticos).
- FR-020a (gate de firma humana).
- FR-027 (versionado de skills referenciado en cada bloque, validable).

## Versión

v0.1.0-mvp — 2026-05-06
