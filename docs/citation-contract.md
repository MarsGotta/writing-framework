# Guía del contrato de citación

Audiencia: personas que mantienen Write.OnMars y autores de MCPs que quieren ser compatibles con el harness. Para la especificación formal y autoritativa, ver `contracts/citation-contract.md`. Esta guía explica el contrato en términos prácticos.

## Qué es el contrato y por qué importa

El contrato de citación define el formato canónico que todo MCP de investigación o contraste debe producir para integrarse con el harness. Cualquier MCP cuya salida pueda mapearse a un `CitationRecord` válido se considera compatible.

El contrato actúa como frontera: separa el harness (estable, versionado) del ecosistema externo (volátil, heterogéneo). Sin esa frontera, cada MCP traería su propio dialecto y la consolidación en `research.md` y `findings.md` sería frágil.

Tres beneficios concretos:

1. **Trazabilidad**: cada cita declara su `motor`, fecha de consulta y fragmento literal. Un mantenedor puede reabrir la fuente meses después.
2. **Auditabilidad**: el conjunto de citas de un proyecto se valida contra un único schema (`contracts/citation-record.schema.json`). Una pasada 4 (precisión) puede comprobar afirmaciones contra citas de forma automatizable.
3. **Independencia del agente**: el contrato vive fuera de Claude Code. Un puerto a Codex o Cursor consume el mismo formato sin reescribir la lógica de validación.

## Cómo certificar un MCP como compatible

Un MCP se considera certificado cuando cumple cuatro requisitos. El procedimiento resume `contracts/citation-contract.md` § "Cómo certificar un MCP como compatible":

1. Implementar la salida en formato `CitationRecord` v1.0. Cada llamada al MCP que devuelve evidencia debe poder transformarse en uno o varios records.
2. Pasar el schema mínimo (`contracts/citation-record.schema.json`) con `ajv` o equivalente. Un record que falla el schema no es certificable.
3. Documentar en el README del MCP qué valor declara en `motor` (por ejemplo `context7`, `web-search:tavily`, `fetch`) y bajo qué `tipo` clasifica sus resultados (`documentacion_oficial`, `web_publica`, `archivo_local`, `cita_bibliografica`).
4. Añadir el MCP a `docs/compatibility-matrix.md` mediante PR contra el repositorio canónico. La matriz declara estado (`v1`, `planned`, `manual`) y notas operativas.

Un MCP que cumple los cuatro pasos puede usarse en proyectos con `research_mode: byom` sin tocar código del harness.

## Ejemplo paso a paso de cómo emitir un `CitationRecord`

Supongamos que el MCP `context7` resolvió documentación oficial de React 19 sobre `useEffect`. El record correcto se construye así:

1. **Asignar un `citation_id` estable**. La convención recomendada es `{tipo}-{slug}-{fecha}`. Para este ejemplo: `doc-react-19-effect-2026-05-06`. El ID debe ser único dentro del proyecto y reutilizable si la misma cita se referencia desde varios capítulos.

2. **Declarar `tipo` y `referencia`**. La fuente es documentación oficial publicada en una URL absoluta:

   ```
   tipo: documentacion_oficial
   referencia: https://react.dev/reference/react/useEffect
   ```

3. **Recortar el `fragmento` literal**. El record almacena el texto que se va a citar, no un resumen. Si excede 500 caracteres, se permite usar `[...]` para marcar elisiones siempre que se conserve el sentido.

4. **Registrar `fecha_consulta` en formato ISO**. Solo `YYYY-MM-DD`. La fecha debe ser hoy o anterior; las skills rechazan fechas futuras.

5. **Declarar `motor` exacto**. Para este ejemplo: `context7`. Nunca usar `unknown`: si el agente no sabe qué motor trajo el dato, no puede emitir el record.

6. **Marcar `contract_version`**. En v1 siempre `"1.0"`.

7. **Añadir metadatos opcionales relevantes**. Si la fuente tiene versión propia (docs de librería, releases), declarar `versionado_aplicable: true` y la `version_aplicable` exacta. Si el dato es volátil (precios, comandos, versiones), marcar `volatil: true` para que `research.md` lo trate como `[VERIFICAR]`.

El record completo queda así:

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

Para validarlo desde la consola:

```bash
ajv validate -s contracts/citation-record.schema.json -d /tmp/record.json
```

Si la validación falla, el record no entra en `research.md`. La skill correspondiente debe rechazarlo y devolver el error al operador o al sub-agente.

## Errores comunes

Estos casos aparecen con frecuencia cuando un MCP empieza a emitir records. Conviene revisarlos antes de proponer la certificación:

- **`motor: "unknown"` o vacío**. El contrato lo prohíbe explícitamente (regla 2 de validación). Si el MCP envuelve a otro motor, debe declarar el suyo propio (por ejemplo `mi-mcp:tavily-wrapper`).
- **`fragmento` con menos de 20 caracteres**. La regla 4 exige texto significativo, salvo cuando la fuente sea estructurada y la cita sea un valor concreto (una versión, un precio). Para casos generales, fragmentos demasiado cortos suelen indicar que se citó un encabezado en lugar del cuerpo.
- **`fecha_consulta` en el futuro**. Las skills rechazan estas fechas (regla 3). Suele ocurrir cuando un script normaliza zonas horarias mal o cuando se reutiliza una plantilla con fecha placeholder.
- **`tipo` o `confianza` con un valor fuera del enum**. Los enums son cerrados (regla 5). Si una fuente no encaja en `documentacion_oficial`, `web_publica`, `archivo_local` o `cita_bibliografica`, el MCP no puede emitir el record en v1; debe esperar a una extensión MINOR del enum o reclasificar.
- **Editar un record existente**. Está prohibido (regla 1: inmutabilidad). Una corrección genera un record nuevo con `citation_id` distinto y deja el original con sufijo `:superseded`. Esto preserva el historial completo de la investigación.
- **Olvidar `version_aplicable` cuando `versionado_aplicable: true`**. El schema lo exige condicionalmente (`if`/`then`). Si el MCP marca la fuente como versionable, debe poder declarar la versión exacta.

## Cuándo bumpear `contract_version`

El contrato sigue semver. Las reglas de versionado vienen de `contracts/citation-contract.md` § "Versionado del contrato":

- **MAJOR (`v2.0`)**: cualquier cambio que rompa consumidores existentes. Por ejemplo: renombrar un campo obligatorio (`fragmento` → `texto_citado`), cambiar el tipo de un campo (de `string` a `object`), eliminar un valor del enum `tipo`. Un bump MAJOR exige que cada MCP migre su salida; los proyectos pinean `citation_contract_version` en su manifiesto y no se ven forzados a actualizar de golpe.
- **MINOR (`v1.y`)**: añadir campos opcionales nuevos (por ejemplo, `idioma_original`) o ampliar enums sin romper los valores existentes (añadir `cita_pre_print` al enum `tipo`). Los consumidores existentes siguen funcionando porque los campos opcionales se pueden ignorar.
- **PATCH (`v1.0.z`)**: aclaraciones en la documentación, ejemplos nuevos, correcciones tipográficas. No cambia la forma de los records ni los campos.

Cada proyecto declara la versión soportada en `manifest.citation_contract_version` (ver `docs/manifest-schema.md`). Los MCPs que producen records emiten `contract_version` en cada record. Las skills del framework comparan ambos al recibir y rechazan mismatches MAJOR.

Antes de proponer un bump, conviene revisar:

1. **Coste para los consumidores**: cuántos MCPs deben adaptarse y cuántos proyectos quedan en v1.x.
2. **Alternativa MINOR posible**: muchas mejoras se pueden expresar como campos opcionales sin romper compatibilidad.
3. **Actualización en cadena**: un bump MAJOR obliga a actualizar `contracts/citation-contract.md`, `contracts/citation-record.schema.json`, todas las skills que emiten records y `docs/compatibility-matrix.md`.

## Para profundizar

- Especificación formal: `contracts/citation-contract.md`.
- JSON Schema validable: `contracts/citation-record.schema.json`.
- Matriz de compatibilidad: `docs/compatibility-matrix.md`.
- Manifiesto del proyecto: `docs/manifest-schema.md` (sección `citation_contract_version`).
