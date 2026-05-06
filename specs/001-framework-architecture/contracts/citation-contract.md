# Citation Contract v1.0

**Status**: stable for Write.OnMars v1.
**Cobertura de spec**: FR-009a, FR-009b, FR-016, FR-027.

Este contrato define el formato canónico que un MCP de investigación o de contraste DEBE producir para integrarse con Write.OnMars. Cualquier MCP cuya salida pueda mapearse a un `CitationRecord` válido se considera compatible con el framework. El contrato es la frontera entre el harness y el ecosistema externo.

---

## Modelo conceptual

Una **cita** es la representación digital de una fuente consultada en un momento concreto, con suficiente metadato para que un mantenedor pueda:

1. Reabrir la fuente más tarde (URL o ruta).
2. Conocer el contexto temporal (fecha de consulta, posible obsolescencia).
3. Saber qué fragmento concreto se usó (transcripción).
4. Identificar el motor que la trajo (auditabilidad).

---

## Campos del `CitationRecord`

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `citation_id` | string | sí | Identificador estable del registro dentro del proyecto. Recomendado: `{tipo}-{slug}-{fecha}` (p. ej. `web-context7-react-2026-05-06`). |
| `tipo` | enum | sí | `documentacion_oficial` \| `web_publica` \| `archivo_local` \| `cita_bibliografica` |
| `referencia` | string | sí | URL absoluta o ruta relativa al repositorio (`resources/Manual Maestro....md#section`). |
| `fragmento` | string | sí | Texto literal citado. Si excede 500 caracteres, se permite recortar con `[...]` siempre que se conserve el sentido. |
| `fecha_consulta` | string (ISO-8601 fecha) | sí | `YYYY-MM-DD` de cuando se consultó la fuente. |
| `motor` | string | sí | Identificador del MCP / herramienta / persona. Ejemplos: `context7`, `web-search:tavily`, `fetch`, `local:resources`, `human:marcela`. |
| `contract_version` | string (semver) | sí | Versión del contrato que cumple este record. v1 = `"1.0"`. |
| `versionado_aplicable` | boolean | no | `true` cuando la fuente tiene versión propia (docs de librería, releases). |
| `version_aplicable` | string | si `versionado_aplicable = true` | Versión exacta consultada (p. ej. `react@19.2.0`). |
| `volatil` | boolean | no | `true` cuando el dato puede cambiar (versiones, precios, comandos); el record se marca `[VERIFICAR]` en `research.md` automáticamente. |
| `confianza` | enum | no | `oficial` \| `comunidad_alta` \| `comunidad_baja` \| `personal`. Por defecto `oficial` para `documentacion_oficial` y `archivo_local`; `comunidad_alta` para `web_publica`. |
| `notas` | string | no | Comentarios libres del agente sobre el uso del fragmento. |

---

## Reglas de validación

1. **Inmutabilidad**: una vez registrado, un `CitationRecord` no se modifica; cualquier corrección genera un record nuevo con `citation_id` distinto y deja el original con sufijo `:superseded`.
2. **Trazabilidad de motor**: ningún `motor` puede ser `unknown`. Si el agente no sabe qué motor lo trajo, no puede emitir el record.
3. **Fechas en pasado**: `fecha_consulta` ≤ fecha actual. Las skills MUST rechazar fechas futuras.
4. **Fragmento no vacío**: el campo `fragmento` requiere texto significativo (≥ 20 caracteres, salvo cuando la fuente sea estructurada y la cita sea un valor concreto, p. ej. una versión).
5. **Tipos cerrados**: `tipo` y `confianza` solo aceptan los valores enumerados.
6. **Compatibilidad hacia atrás dentro de v1.x**: campos opcionales pueden añadirse en v1.y sin romper consumidores; campos obligatorios solo cambian con bump MAJOR a v2.0.

---

## Ejemplos

### Ejemplo 1 — documentación oficial vía context7

```json
{
  "citation_id": "doc-react-19-effect-2026-05-06",
  "tipo": "documentacion_oficial",
  "referencia": "https://react.dev/reference/react/useEffect",
  "fragmento": "useEffect lets you synchronize a component with an external system...",
  "fecha_consulta": "2026-05-06",
  "motor": "context7",
  "contract_version": "1.0",
  "versionado_aplicable": true,
  "version_aplicable": "react@19.2.0",
  "volatil": false,
  "confianza": "oficial",
  "notas": "Citado en capítulo 4 para introducir efectos."
}
```

### Ejemplo 2 — archivo local en `resources/`

```json
{
  "citation_id": "local-manual-maestro-aenor-2026-05-06",
  "tipo": "archivo_local",
  "referencia": "resources/Manual Maestro para la Producción de Textos Especializados.md#L20",
  "fragmento": "Para asegurar la vigencia internacional de los textos, el autor debe alinearse con los estándares de organismos como ISO e Infoterm.",
  "fecha_consulta": "2026-05-06",
  "motor": "local:resources",
  "contract_version": "1.0",
  "versionado_aplicable": false,
  "volatil": false,
  "confianza": "oficial"
}
```

### Ejemplo 3 — dato volátil marcado [VERIFICAR]

```json
{
  "citation_id": "web-pricing-anthropic-api-2026-05-06",
  "tipo": "web_publica",
  "referencia": "https://www.anthropic.com/pricing",
  "fragmento": "Claude Opus 4.7 input price: $15 / MTok",
  "fecha_consulta": "2026-05-06",
  "motor": "web-search:tavily",
  "contract_version": "1.0",
  "versionado_aplicable": false,
  "volatil": true,
  "confianza": "oficial",
  "notas": "Marcar [VERIFICAR] antes de publicar; precios cambian."
}
```

### Ejemplo 4 — cita bibliográfica

```json
{
  "citation_id": "biblio-cabre-1994-terminologia",
  "tipo": "cita_bibliografica",
  "referencia": "Cabré, M. T. (1994). La terminología. Empúries.",
  "fragmento": "El término es una unidad unívoca que denomina una noción precisa dentro de un campo conceptual determinado.",
  "fecha_consulta": "2026-05-06",
  "motor": "human:marcela",
  "contract_version": "1.0",
  "versionado_aplicable": false,
  "volatil": false,
  "confianza": "oficial"
}
```

---

## JSON Schema (referencia mínima)

Un schema completo vive en `contracts/citation-record.schema.json` (futuro). Esqueleto mínimo para validación con `jq` o `ajv`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://write-on-mars.dev/contracts/citation-record/v1.0.json",
  "type": "object",
  "required": ["citation_id", "tipo", "referencia", "fragmento", "fecha_consulta", "motor", "contract_version"],
  "properties": {
    "citation_id": {"type": "string", "minLength": 1},
    "tipo": {"enum": ["documentacion_oficial", "web_publica", "archivo_local", "cita_bibliografica"]},
    "referencia": {"type": "string", "minLength": 1},
    "fragmento": {"type": "string", "minLength": 1},
    "fecha_consulta": {"type": "string", "format": "date"},
    "motor": {"type": "string", "minLength": 1},
    "contract_version": {"type": "string", "pattern": "^\\d+\\.\\d+$"},
    "versionado_aplicable": {"type": "boolean"},
    "version_aplicable": {"type": "string"},
    "volatil": {"type": "boolean"},
    "confianza": {"enum": ["oficial", "comunidad_alta", "comunidad_baja", "personal"]},
    "notas": {"type": "string"}
  },
  "if": {"properties": {"versionado_aplicable": {"const": true}}, "required": ["versionado_aplicable"]},
  "then": {"required": ["version_aplicable"]}
}
```

---

## Versionado del contrato

- **MAJOR** (v2.0): cualquier cambio que rompa consumidores existentes (renombre de campo obligatorio, cambio de tipo).
- **MINOR** (v1.y): nuevos campos opcionales o ampliación de enums.
- **PATCH** (v1.0.z): aclaraciones y ejemplos.

Cada proyecto declara la versión soportada en `manifest.citation_contract_version`. Los MCPs que producen records emiten `contract_version` en cada record. Las skills del framework comparan ambos al recibir.

---

## Cómo certificar un MCP como compatible

1. Implementar la salida en formato `CitationRecord` v1.0.
2. Pasar el schema mínimo (`citation-record.schema.json`).
3. Documentar en el README del MCP qué `motor` declara y bajo qué `tipo` clasifica sus resultados.
4. Añadir el MCP a `docs/compatibility-matrix.md` del repositorio canónico mediante PR.
