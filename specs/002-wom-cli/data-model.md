# Data Model: CLI `wom` para operar Write.OnMars

**Feature**: 002-wom-cli | **Date**: 2026-05-07

La CLI no introduce nuevos formatos de archivo del framework: opera sobre el manifest, los findings, los chapters y los checklists ya definidos en feature 001. Este documento detalla las **entidades derivadas** que la CLI manipula internamente.

---

## 1. EstadoProyecto

**Origen**: representación derivada en memoria, recalculada en cada invocación de `wom status` o `wom close`. No se persiste.

**Construcción**:

1. Lee `.writeonmars-manifest.json` del proyecto activo.
2. Resuelve `feature_directory` desde `.specify/feature.json`.
3. Lee `<feature_directory>/findings.md` agrupando bloques por pasada × capítulo.
4. Lee `<feature_directory>/checklists/pasada-{1..5}.md` para extraer firmas (bloque WOM-SIGN).
5. Lista `<repo_root>/chapters/[###]-*.md` excluyendo paths gitignored.
6. Cruza datos para producir la matriz `capítulos × pasadas`.

**Esquema interno** (no se serializa; se renderiza directamente):

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `proyecto_nombre` | string | basename del directorio raíz del repositorio |
| `framework_version` | string (semver) | leído de `manifest.framework_version` |
| `signing_matrix` | mapping pasada → enum | leído de `manifest.signing_matrix` |
| `human_operators` | lista de objetos | leído de `manifest.human_operators` |
| `capitulos[]` | lista de `EstadoCapitulo` | reconstruida desde `chapters/` + `findings.md` + checklists |
| `firmas_humanas_requeridas` | int | conteo de pasadas con `signing_matrix[pasada]=human` × capítulos |
| `firmas_humanas_completadas` | int | conteo de checklists con bloque WOM-SIGN válido en pasadas humanas |
| `criticos_abiertos_total` | int | findings con `severidad=critico` y `estado=abierto` |

**EstadoCapitulo**:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `numero` | int | extraído del nombre de archivo `chapters/[###]-...` |
| `titulo` | string | leído del front-matter del capítulo (campo `titulo`) |
| `pasadas` | mapping `1..5` → `EstadoCelda` | una entrada por pasada |
| `criticos_abiertos` | int | findings críticos abiertos sumados sobre las cinco pasadas para ese capítulo |

**EstadoCelda** (una celda del dashboard):

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `estado` | enum | `no_ejecutado` \| `passed` \| `passed_with_warnings` \| `pendiente_firma` \| `bloqueador_critico` |
| `firma_tipo` | enum opcional | `autonomous` \| `human` (cuando aplica) |
| `firma_actor` | string opcional | id del firmante (cuando aplica) |
| `findings_count` | int | total de findings de esa celda |

**Reglas de transición de `estado`**:

```text
no_ejecutado    → passed                : sin findings nuevos críticos/medios + pasada cerrada en findings.md
no_ejecutado    → passed_with_warnings  : findings medios/bajos sin críticos abiertos
no_ejecutado    → bloqueador_critico    : ≥ 1 finding crítico abierto
passed          → pendiente_firma       : pasada con signing_matrix[pasada]=human y sin bloque WOM-SIGN
passed          → passed                : pasada con signing_matrix[pasada]=autonomous (cierre directo)
```

**Cobertura**: FR-011, FR-012, FR-014.

---

## 2. Lockfile

**Archivo**: `<target>/.wom/lock` (archivo) + `<target>/.wom/lock.d/` (directorio guardián atómico).

**Ciclo de vida**:

1. **Adquisición**: `mkdir <target>/.wom/lock.d` (atómico). Si falla, otro proceso tiene el lock; se lee el archivo `<target>/.wom/lock` para diagnóstico.
2. **Escritura del archivo**: dentro del lock, escribir `<target>/.wom/lock` con metadatos.
3. **Stale detection**: si el `pid` del lock no responde a `kill -0 $pid`, el lock se considera stale; se limpia con warning y se re-adquiere.
4. **Liberación**: `rm <target>/.wom/lock` + `rm -rf <target>/.wom/lock.d` al terminar (vía `trap` en cada subcomando que escribe).

**Esquema del archivo `<target>/.wom/lock`** (JSON):

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| `pid` | int | sí | PID del proceso que adquirió el lock |
| `subcommand` | string | sí | nombre del subcomando que tiene el lock (`new`, `sign`, `update`, `close`) |
| `started_at` | ISO-8601 datetime | sí | timestamp de adquisición |
| `host` | string | no | hostname del sistema (auditoría) |
| `operator` | string | no | id del operador desde el manifest si aplica |

**Subcomandos que adquieren lock** (escritores): `new`, `sign`, `update`, `close`.
**Subcomandos sin lock** (lectores): `status`, `validate`, `doctor`, `brief` cuando solo abre el editor, `research` / `plan` / `draft` / `review` cuando solo imprimen prompt.

**Cobertura**: FR-017, edge case "dos sesiones simultáneas".

---

## 3. BloqueFirma

**Archivo**: bloque dentro de `<feature_directory>/checklists/pasada-N.md` (uno por checklist).

**Formato** (entre marcadores HTML):

```markdown
<!-- WOM-SIGN START -->
firma_tipo: human
firma_actor: marcela
firma_fecha: 2026-05-07
referencia_findings: ../../specs/[###-feature]/findings.md#pasada-N
<!-- WOM-SIGN END -->
```

| Campo | Tipo | Obligatorio | Validación |
|-------|------|-------------|-----------|
| `firma_tipo` | enum | sí | `human` \| `autonomous` \| `desviacion_justificada` |
| `firma_actor` | string | sí | id del firmante; debe estar en `manifest.human_operators[].id` cuando `firma_tipo=human` |
| `firma_fecha` | ISO-8601 fecha | sí | `YYYY-MM-DD` en hora local; ≤ fecha actual |
| `referencia_findings` | path relativo | sí | apunta al bloque de pasada en findings.md |
| `nota` | string | no | razón cuando `firma_tipo=desviacion_justificada` |

**Reglas**:

- **Idempotencia**: `wom sign` reescribe el bloque entre marcadores; no añade duplicados.
- **Append si ausente**: si el archivo no tiene marcadores, se añaden al final con un encabezado `## Firma`.
- **Validación de `firma_actor`**: la CLI rechaza la firma si el id no está en `manifest.human_operators[].id` (a menos que `firma_tipo=autonomous`).
- **Reescritura controlada**: ningún otro contenido del checklist se modifica.

**Cobertura**: FR-009, FR-010, SC-004.

---

## 4. PromptFormateado

**Origen**: salida de los subcomandos `wom research`, `wom plan`, `wom draft`, `wom review`. No se persiste; se imprime por stdout.

**Estructura**: bloque markdown listo para pegar en el agente.

```markdown
[Cabecera]
Prompt para skill: writeonmars-redaccion
Capítulo objetivo: 2
Modo: paralelo (--parallel 2)

[Contexto requerido por la skill]
- Brief: /Users/.../specs/[###]/spec.md
- Temario: /Users/.../specs/[###]/plan.md § Temario
- Descripciones encadenadas: /Users/.../specs/[###]/plan.md § Descripciones
- Glosario consolidado: /Users/.../specs/[###]/glossary.md
- Capítulo objetivo: capítulo 2 — "Mapa mental del dominio"

[Instrucción al agente]
Invoca /writeonmars-redaccion con --parallel 2 sobre el capítulo 2.
Sigue el prompt canónico en agents/claude/prompts/redaccion.md.
La salida esperada es chapters/002-mapa-mental.md con front-matter YAML
y las nueve secciones obligatorias.
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `cabecera` | string | nombre de la skill + parámetros principales |
| `contexto[]` | lista | rutas absolutas a los archivos que la skill necesita leer |
| `instruccion` | string | comando exacto (con flags) que la operadora pega en el agente |

**Cobertura**: FR-007, FR-008.

---

## 5. ResultadoCierre

**Origen**: salida de `wom close`. Se imprime por stdout con exit code distinto según el resultado.

**Esquema** (JSON cuando `--format=json`, texto humano por defecto):

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `closeable` | bool | sí | `true` solo si no hay blockers |
| `blockers[]` | lista de objetos | sí (puede estar vacía) | lista estructurada de bloqueadores |
| `note` | string | no | mensaje libre para auditoría |

**Estructura de cada blocker**:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `type` | enum | `critical_finding_open` \| `human_signature_missing` |
| `pasada` | string | id de la pasada (`pasada_3_naturalidad`, etc.) |
| `capitulo` | int o `global` | capítulo afectado |
| `finding_id` | string opcional | si es crítico, el id `F-N.M` |
| `expected` | string opcional | para firma faltante: valor esperado (`human`) |
| `got` | string opcional | para firma faltante: valor actual (`autonomous` o ausente) |

**Exit codes**:

- `0`: closeable=true.
- `1`: closeable=false con blockers (caso normal).
- `2`: error de invocación o manifest corrupto.

**Cobertura**: FR-014, SC-003.

---

## Resumen de relaciones

```text
.writeonmars-manifest.json
  ├─→ EstadoProyecto (signing_matrix, human_operators, framework_version)
  ├─→ ResultadoCierre (gate FR-020a)
  └─→ BloqueFirma (validación de firma_actor)

specs/[###]/findings.md
  ├─→ EstadoProyecto (matriz de celdas)
  └─→ ResultadoCierre (gate FR-020)

checklists/[###]/pasada-N.md
  ├─→ EstadoProyecto (firma_tipo de cada celda)
  ├─→ BloqueFirma (escritura idempotente por wom sign)
  └─→ ResultadoCierre (verificación de firma humana)

chapters/[###]-titulo.md
  └─→ EstadoProyecto (lista de capítulos del dashboard)

.wom/lock
  └─→ Lockfile (concurrencia entre subcomandos escritores)
```
