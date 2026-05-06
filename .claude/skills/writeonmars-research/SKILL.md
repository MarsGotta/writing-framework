---
name: writeonmars-research
description: Orquesta investigación editorial sobre MCPs compatibles con el contrato de citación (modo BYOM por defecto). Lee `resources/` como fuente local obligatoria y emite `research.md` con CitationRecord validados. Trigger cuando la persona diga "investiga el tema", "research con fuentes", "/speckit-plan paso 1", "trae fuentes para esta guía".
allowed-tools: Bash, Read, Write, Edit, Agent
---

# writeonmars-research

Skill que materializa los Principios III y IV en su dimensión investigativa
y la Arquitectura del framework (trazabilidad documental). Se dispara tras
aprobar el brief y antes de redactar el plan. Emite `research.md` con
`CitationRecord` v1.0 conformes al contrato de citación.

## Cuándo dispararse

- "investiga el tema"
- "research con fuentes"
- "/speckit-plan paso 1"
- "trae fuentes para esta guía"
- "consolida la investigación"
- Tras `/speckit-clarify` cuando el plan todavía no tiene `research.md`.

NO actives la skill si el `research.md` actual ya cubre todos los
`conceptos_obligatorios` del brief con al menos una cita por concepto
(SC-009). En ese caso, sugiere ejecutar `writeonmars-contraste` para
validar coherencia.

## Qué hace

1. Lee el brief (`specs/[###-feature]/spec.md`) y extrae
   `conceptos_obligatorios`, `audiencia`, `ejemplo_recurrente`, `riesgos`.
2. Detecta MCPs disponibles compatibles con el contrato de citación
   (sección "BYOM dispatch" más abajo).
3. Carga `resources/` del proyecto como fuente local obligatoria. Si la
   carpeta está vacía, advierte; si no existe, crea la entrada y emite
   warning.
4. Para cada concepto obligatorio, lanza una consulta orientada al MCP más
   apropiado (preferencia: `documentacion_oficial` > `archivo_local` >
   `web_publica`) y normaliza la respuesta como `CitationRecord`.
5. Valida cada record con `tests/lib/validate-citation.sh` antes de
   añadirlo a `research.md`.
6. Marca datos volátiles (versiones, precios, comandos) con `[VERIFICAR]`
   y `volatil: true`.
7. Emite `specs/[###-feature]/research.md` con la estructura de
   data-model.md §2: temas_explorados, fuentes (lista de
   `CitationRecord`), datos_volatiles, fecha_consulta_global,
   motor_principal.

## Inputs

- `specs/[###-feature]/spec.md` — brief editorial.
- `resources/` — fuente local obligatoria.
- `.writeonmars-manifest.json` — `research_mode`, `citation_contract_version`.
- `docs/compatibility-matrix.md` — lista de MCPs reconocidos.
- `contracts/citation-record.schema.json` — para validación.

## Outputs

- `specs/[###-feature]/research.md` con todas las fuentes citables.
- Cada `CitationRecord` validado por `tests/lib/validate-citation.sh`
  antes de persistirse.

## Procedimiento

1. Resolver `[###-feature]` desde la rama activa.
2. Cargar `conceptos_obligatorios` del brief. Si faltan, detener y exigir
   `writeonmars-brief` previo.
3. Detectar MCPs disponibles (ver "BYOM dispatch"). Si ninguno responde,
   abortar con el mensaje de fallback documentado.
4. Para cada concepto: consultar fuente, normalizar a `CitationRecord`,
   validar con el helper, anexar a la lista.
5. Adjuntar las citas locales obligatorias de `resources/` (al menos
   `guia-IA-writing.md` y *Manual Maestro* cuando existan en la carpeta).
6. Componer `research.md` y dejar enlaces internos cruzados (cada
   `CitationRecord` referenciable por su `citation_id` desde
   `findings.md` durante la pasada 4).
7. Imprimir resumen: número de citas por concepto, motores usados, datos
   volátiles detectados.

## BYOM dispatch

El framework opera por defecto en modo BYOM (Bring Your Own MCP). Esta
sección documenta cómo la skill detecta MCPs disponibles, normaliza sus
salidas a `CitationRecord` v1.0 y maneja el fallback cuando no hay
ninguno.

### Detección de MCPs disponibles

La skill consulta el cliente del agente (Claude Code: lista de MCP
servers conectados; Codex/Cursor: equivalentes documentados en
`agents/<agent>/`) y compara contra los nombres reconocidos en
`docs/compatibility-matrix.md` § "MCPs investigación compatibles":

- `context7`
- `web-search:tavily`
- `fetch`
- `local:resources` (siempre disponible si existe la carpeta `resources/`)

### Mapping de salida → CitationRecord

| MCP | `tipo` | `motor` | Notas |
|-----|--------|---------|-------|
| `context7` | `documentacion_oficial` | `context7` | `versionado_aplicable: true` cuando la librería expone versión; rellenar `version_aplicable` desde el contexto de la consulta (ej. `react@19.2.0`). `confianza: oficial`. |
| `web-search:tavily` | `web_publica` | `web-search:tavily` | `volatil: true` si la consulta toca versiones, precios, comandos o disponibilidad de servicios. `confianza: comunidad_alta` por defecto. |
| `fetch` | `web_publica` | `fetch` | Sin reranker. La cita debe venir de la URL directa consultada. Mismas reglas de volatilidad. |
| `local:resources` | `archivo_local` | `local:resources` | `referencia` con path relativo a la raíz del proyecto (`resources/<archivo>#L<linea>` cuando aplique). `confianza: oficial`. |

Cualquier MCP nuevo MUST añadirse a `docs/compatibility-matrix.md` con su
mapping antes de que esta skill lo consuma.

### Validación

Cada `CitationRecord` candidato pasa por
`tests/lib/validate-citation.sh` antes de persistirse en `research.md`.
Records que no validan se descartan y se reporta el error al operador
(`[research][warn] CitationRecord rechazado: <motivo>`).

### Fallback cuando no hay MCP compatible

Si la detección no encuentra ningún MCP de la matriz Y `resources/` está
vacía o ausente, la skill aborta con el mensaje literal:

```
[research][err] Ningún MCP compatible con el contrato de citación
encontrado. Instala al menos uno de: context7, web-search:tavily, fetch.
También puedes activar el módulo bundled writeonmars-research declarando
research_mode: bundled en .writeonmars-manifest.json (FR-009b).
```

Si solo `local:resources` está disponible y la carpeta tiene contenido,
la skill continúa pero advierte: la investigación queda restringida a
fuentes locales y SC-009 (≥1 cita por concepto obligatorio) puede no
satisfacerse.

## Errores comunes

- `resources/` ausente: crear la carpeta y reintentar.
- MCP que devuelve resultados sin URL absoluta: la skill rechaza y pide al
  operador reformular la consulta.
- Citas duplicadas (mismo `citation_id`): la skill añade sufijo
  `-dup-<n>` y advierte.
- Versiones no declaradas en `documentacion_oficial`: la skill exige
  `version_aplicable` o rebaja a `web_publica`.

## FR cubierta

- FR-008 (investigación basada en MCPs compatibles).
- FR-009 (cada `CitationRecord` validado contra el schema).
- FR-009a (BYOM por defecto, `resources/` obligatorio).
- FR-009b (fallback hacia el módulo bundled MCP cuando se active).
- FR-027 (versionado de skills y contrato registrado en cada cita).
- SC-009 (≥1 cita por concepto obligatorio).

## Versión

v0.1.0-mvp — 2026-05-06
