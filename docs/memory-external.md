# Memoria externa vectorizada (opcional)

Audiencia: persona mantenedora o operadora que quiera activar la memoria
externa declarada en la constitución § Arquitectura del
framework. La memoria externa es **opcional, caché acelerada y nunca fuente
de verdad**. Esta página documenta el esquema mínimo, el procedimiento de
activación y la regla de reconstrucción.

## Esquema mínimo

La constitución exige documentar el esquema cuando la memoria externa se
active. El esquema canónico v1 declara cada entrada con cuatro campos
obligatorios:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `entidad` | string | Nombre canónico del concepto, término o fragmento. Debe coincidir con un término del glosario, un capítulo o un finding firmado. |
| `fuente` | string | Path relativo al repo (`glossary.md#L42`, `chapters/003-redaccion.md`, `findings.md#pasada-2-cap-3`) o URL canónica de un recurso bajo `resources/`. |
| `fecha` | string ISO-8601 | Fecha de captura (`YYYY-MM-DD`). Permite invalidar entradas obsoletas tras un bump de la constitución o un edit estructural. |
| `etiquetas` | array<string> | Tags libres pero canónicos: `glosario`, `ejemplo-recurrente`, `caja-visual`, `error-frecuente`, `pasada-3:naturalidad`, etc. |

Campos opcionales recomendados:

- `vector` (array<float>): embedding del fragmento. La dimensionalidad la
  decide el `provider`.
- `texto` (string): fragmento literal indexado, máx. 1 000 caracteres.
- `hash_origen` (string): hash del archivo fuente al momento de la captura;
  permite detectar obsolescencia.

Cualquier campo adicional MUST documentarse en este archivo antes de
guardarlo.

## Procedimiento de activación

1. **Editar el manifest** del proyecto editorial:

   ```json
   {
     "memory_external": {
       "enabled": true,
       "provider": "qdrant",
       "uri": "http://localhost:6333",
       "rebuildable_from_repo": true
     }
   }
   ```

   `provider` admite cualquier motor que implemente la API mínima
   (búsqueda por vector + filtrado por etiqueta). Ejemplos probados:
   `qdrant`, `weaviate`, `pinecone`. La elección no es prescriptiva.

2. **Declarar `rebuildable_from_repo: true`**. La constitución exige que la
   memoria pueda reconstruirse desde los artefactos del repo. Si el
   provider elegido no permite reconstrucción (por dependencia rígida de
   un dataset propietario), no se admite como memoria externa de
   Write.OnMars.

3. **Validar el manifest** contra `contracts/manifest-schema.json` tras la
   edición:

   ```bash
   ajv validate -s contracts/manifest-schema.json -d .writeonmars-manifest.json
   ```

4. **Inicializar el provider**: crear la colección o índice con dimensión
   y métrica adecuadas al modelo de embeddings elegido. Documentar la
   configuración en una nota interna del proyecto.

5. **Sembrar la memoria** ejecutando el script de reconstrucción descrito
   abajo. Sin sembrado inicial, la memoria queda vacía y los capítulos
   ignorarán el caché.

## Procedimiento de reconstrucción

La memoria es **caché acelerada**. Si diverge del repo, gana el repo. Para
reconstruir desde cero:

```bash
tools/rebuild-memory.sh   # script especificado pero no implementado en v1
```

**Estado v1**: el script `tools/rebuild-memory.sh` queda especificado en
este documento, no implementado. Cuando se implemente, debe iterar
exactamente las siguientes fuentes y reinsertarlas en el provider:

1. `glossary.md` — cada término como entidad. Etiqueta `glosario`.
2. `specs/[###-feature]/glossary.md` (por feature) — entidades
   `glosario-feature`.
3. `chapters/*.md` — front-matter `terminos_introducidos` cruzado con el
   cuerpo. Etiqueta `concepto-capitulo`.
4. Sección "Ejemplo recurrente" del brief
   (`specs/[###-feature]/spec.md` campo 7) — entidad
   `ejemplo-recurrente`. Etiqueta `ejemplo-recurrente`.
5. `findings.md` — cada finding firmado como entidad
   `finding-cap-N-pasada-M`. Etiqueta `pasada-M:<lente>`.
6. `common-errors.md` — cada error como entidad. Etiqueta `error-frecuente`.

Cada entrada lleva `fecha` = fecha de ejecución del script y `hash_origen`
del archivo fuente.

## Aviso explícito

> **La memoria externa es caché acelerada, nunca fuente de verdad.**

Reglas operativas que materializan la regla:

- Cualquier afirmación en una guía MUST sostenerse en `glossary.md`,
  `findings.md` o `resources/`. La memoria externa solo acelera la
  recuperación.
- Si una pasada detecta una contradicción entre la memoria y el repo, la
  memoria se invalida (entrada borrada o re-sembrada) y el repo prevalece.
- El bump de la constitución MAY invalidar memoria sembrada antes del
  bump. La persona operadora decide si reconstruye o filtra por fecha.
- La memoria NO se commitea al repo. El estado del provider vive fuera de
  Git.

## Cross-links

- `contracts/manifest-schema.json` § `memory_external` — campo opcional
  del manifest que activa la memoria.
- `docs/manifest-schema.md` — descripción humana del schema.
- Constitución § Arquitectura del framework — política normativa de la
  memoria externa.
- `tools/rebuild-memory.sh` — script de reconstrucción (especificado, no
  implementado en v1).
